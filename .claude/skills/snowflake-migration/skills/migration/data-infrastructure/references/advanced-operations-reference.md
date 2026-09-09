# Advanced operations reference

Use this when a customer asks about **protecting the source**, **bounded migration dry-runs**, **incremental validation**, **re-validating failed partitions**, **throttling concurrent tasks**, **custom L3 normalization**, or **why checksum/incremental sync missed a change**. These are optional — default migrate/validate flows do not require them.

**Related references:** [Metadata storage mode (Hybrid vs standard)](./metadata-storage-mode-reference.md), [DM workflow config](../../migrate-objects/actions/data-migration/references/workflow-config-reference.md), [DV workflow config](../../setup/data-validation/references/workflow-config-reference.md), [validate_tables.md](../../validate-objects/actions/validate_tables.md).

---

## Rate limiting (protect source or shared resources)

**When the customer asks:** source DB is overloaded during migration; they need to cap concurrent extractions/loads without stopping workers entirely; they want to pause one workflow while others continue.

**What it is:** Scope-pattern rules in Snowflake table `DATA_MIGRATION.RATE_LIMIT` (or your `CUSTOM_SNOWFLAKE_SCHEMA_FOR_DATA_MIGRATION_METADATA` schema). Each rule limits how many **executing** tasks whose `SCOPE` matches a SQL `LIKE` pattern can run at once.

**Agent guidance:**

1. Prefer explaining rate limits **before** lowering `max_parallel_tasks` globally or stopping workers — workers can stay up while matching tasks wait in `pending`.
2. `TARGET_CONCURRENT_TASKS` is a **target**, not a hard ceiling — eligibility is snapshot-based, so many workers polling together can overshoot before claims settle. Worst case is roughly **2× the target** (target `5` → up to ~10 executing). Set the target **below** a hard source limit with headroom for your worker count. **`TARGET_CONCURRENT_TASKS = 0`** is the one exact value — it reliably pauses matching scopes.
3. Enforcement applies to **worker (DEA) single-task pulls** only — not orchestrator batch pulls. Workers with `max_parallel_tasks > 1` batch-fetch bypass rate limiting; keep default single-task fetch when using limits.
4. Insert rules with SQL in a Snowflake session (admin on migration metadata schema):

```sql
-- At most 5 concurrent loading tasks (any table):
INSERT INTO SNOWCONVERT_AI.DATA_MIGRATION.RATE_LIMIT (SCOPE_PATTERN, TARGET_CONCURRENT_TASKS)
VALUES ('Table[%]::Loading', 5);

-- Cap one workflow's partition loads:
INSERT INTO SNOWCONVERT_AI.DATA_MIGRATION.RATE_LIMIT (SCOPE_PATTERN, WORKFLOW_ID, TARGET_CONCURRENT_TASKS)
VALUES ('Table[%]::Partition[%]::Loading', <workflow_id>, 2);

-- Pause all tasks matching a pattern:
INSERT INTO SNOWCONVERT_AI.DATA_MIGRATION.RATE_LIMIT (SCOPE_PATTERN, TARGET_CONCURRENT_TASKS)
VALUES ('Table[MY_DB.%]::%', 0);
```

| Column | Meaning |
|--------|---------|
| `SCOPE_PATTERN` | `LIKE` pattern on task scope (e.g. `Table[DB.SCHEMA.TABLE]::Partition[3]::Extraction`) |
| `WORKFLOW_ID` | Optional — restrict rule to one workflow |
| `AFFINITY` | Optional — restrict to one worker affinity |
| `TARGET_CONCURRENT_TASKS` | Target concurrent executing matches (~2× worst-case overshoot; `0` = exact pause) |
| `ENABLED` | Set `FALSE` to disable without deleting |

Remove with `DELETE FROM … RATE_LIMIT WHERE …` or disable with `ENABLED = FALSE`. Empty table = no limiting.

**Not in workflow YAML** — rate limits are metadata-table SQL, not `migrate_data` / `validate_data` parameters.

---

## Preflight workflows (bounded migration dry-run)

**When the customer asks:** test connectivity and pipeline end-to-end on a small slice before a full migration; validate types/partitioning without writing to production target schemas.

**What it is:** A **data migration** workflow flag — not validation, not `scai data doctor`. Each table runs as **one partition**; targets land in transient schema `PREFLIGHT_<workflowId>` instead of the configured target schema.

**Not the same as:**

| Concept | Purpose |
|---------|---------|
| **Preflight workflow** (`preflight: true`) | Bounded DM dry-run to transient schema |
| **Preliminary migration type** | Row-limited full migration via `whereClauseCriteria` to real target |
| **`scai data doctor`** | Infra/config health before start — blocks local start on fail |

**Agent guidance:**

1. Offer preflight when the user wants a **pipeline smoke test**, not when they only need row sampling to production (use **Preliminary** + `whereClauseCriteria` instead).
2. Set in workflow YAML at top level (Step 2a edit after `migrate_data(mode="setup")`):

```yaml
preflight: true
preflightKeepSchema: false   # true = leave PREFLIGHT_<id> for manual inspection
```

3. Run with normal `migrate_data(mode="run", workflow_path=...)`. Inspect transient schema objects; production target schemas are not used.
4. For a real migration, turn `preflight` off (or generate a new workflow without it) before production load.

See [workflow-config-reference.md](../../migrate-objects/actions/data-migration/references/workflow-config-reference.md#preflight-bounded-dry-run).

---

## Incremental data validation

**When the customer asks:** re-run validation without scanning every partition; validate only what changed since last run; ongoing validation after initial full pass.

**What it is:** DV **`synchronization`** block (`watermark` or `checksum`) — same JSON shape as DM incremental sync, but **read-only** (no data movement, no duplicate rows on target).

**Agent guidance:**

1. Capture mode at setup: `validation_type=incremental` + `sync_strategy=watermark|checksum` via `validate_data(mode="setup", …)` (or `progress_setup(mode="data_validation")` wizard). Setup patches `defaultTableConfiguration.synchronization.strategy`.
2. **Prerequisites:** table partitioned (`columnNamesToPartitionBy`); **at least one prior full validation** completed for baseline metadata. First incremental-configured run still validates everything (establishes baseline).
3. Edit YAML for `watermarkColumn` or `checksumExpression` as needed — see [DV workflow config reference](../../setup/data-validation/references/workflow-config-reference.md#incremental-validation-synchronization).
4. Later unchanged runs may report **Not validated** (skipped partitions) — that is expected, not a failure.
5. DV ignores DM-only sync fields (`trackModifications`, `trackDeletions`) — do not copy DM incremental examples that rely on them.
6. **Checksum blind spots:** default partition checksums skip or round some types (SQL Server `text`/`ntext`/`image`, Oracle LOBs, float rounding, etc.) — a change only in those columns may **not** trigger re-validation. See [Checksum / incremental sync — types that may not trigger re-sync](#checksum--incremental-sync--types-that-may-not-trigger-re-sync).

---

## Re-validation (retry failed partitions)

**When the customer asks:** validation finished but some tables/partitions failed; fix data and retry without re-running the whole workflow; cheaper retry after YAML or source fixes.

**What it is:** **`validate_data(mode="revalidate", workflow_name=…)`** — creates a child `data-re-validate` workflow that re-runs **only failed partitions/levels** from a **finished** parent workflow. Not a full `mode="run"` replay.

**Agent guidance:**

1. Parent workflow must be **finished** with failures — use `details.progress.output.workflowName` from the run report.
2. After data or config fixes, offer revalidate before full re-setup:

```
validate_data(mode="revalidate", workflow_name="<parentWorkflowName>")
```

3. Repeat monitor + error-first report (same as `mode="run"`). Shared orchestrator + worker must still be up.
4. **Not the same as incremental validation** — revalidate retries **failed** work from one run; incremental skips **unchanged** partitions on subsequent scheduled runs.
5. Task-queue automatic retries (`MAX_RETRIES`, lease expiry) happen inside a single workflow — revalidate is an explicit user/agent action after the parent completes.
6. **Schema failures, by default, do not force a full re-run.** Re-validation reuses the parent's already-computed partition metadata and re-runs **only the failing data partitions**, skipping schema re-checks — so a table whose *only* failure was schema (its data partitions all passed) is not retried. Pass **`recheck_schema=true`** (CLI `--recheck-schema`) to instead re-run the full pipeline for schema-failed tables so their schema is re-checked. Leave it off (default) when the failures are data mismatches and the schema diff is benign or already understood; turn it on when you fixed the schema/target definitions and want confirmation.

```
validate_data(mode="revalidate", workflow_name="<parentWorkflowName>", recheck_schema=true)
```

See [validate_tables.md](../../validate-objects/actions/validate_tables.md) Step 5.G and [background-monitoring.md](../../validate-objects/actions/references/background-monitoring.md).

CLI equivalent: `scai data validate revalidate <WORKFLOW_NAME>` (add `--recheck-schema` to re-check schema for schema-failed tables).

---

## Custom normalization (Data Validation L3)

**When the customer asks:** known benign formatting differences (case, trim, spatial WKT, Teradata PERIOD cast strings); L3 row-hash fails but values are "effectively equal"; how to whitelist normalization without `acceptedTransformations` per cell.

**What it is:** SQL expressions applied **before** L3 row-hash and cell compare so source and target values hash/compare on a common form. Configured in DV workflow YAML — **not** DM `columnTypeMappings` (those affect extraction/load only).

**Key fields** (workflow root, `validationConfiguration`, or per-table):

| Field | Purpose |
|-------|---------|
| `validationCustomNormalizationRules` | **Preferred** — per `column`, `columnPattern`, or `dataType`; `sourceExpression` / `targetExpression` with `{{ col_name }}` placeholder |
| `validationCustomNormalizations` | Legacy datatype-keyed lists (still supported; granular rules win when both match) |
| `validationCustomTypes` / `validationCustomTypeRules` | L1 schema type expectations — pair with normalization when types differ but values should compare equal |

**Agent guidance:**

1. **Hybrid L3 requires L1** (`schemaValidation: true`) — normalization rules need L1 column metadata.
2. Use **`validationCustomNormalizationRules`** for new edits. Example — case-insensitive text:

```yaml
validationCustomNormalizationRules:
  - column: STATUS_CODE
    sourceExpression: 'UPPER("{{ col_name }}")'
    targetExpression: 'UPPER("{{ col_name }}")'
```

3. **`acceptedTransformations`** is for known source→target *value pairs*; **normalization rules** are for *expressions* applied to both sides.
4. DM **`columnTypeMappings` do not apply to DV** — do not copy migration type overrides into validation YAML expecting L3 to follow them.

Workflow fields: [DV workflow config reference](../../setup/data-validation/references/workflow-config-reference.md#custom-normalization-l3).

---

## Checksum / incremental sync — types that may not trigger re-sync

**When the customer asks:** "I changed column X but incremental migration/validation did not re-run the partition"; checksum stayed the same; only `text`/`ntext`/`datetime`/`float`/spatial columns changed.

**What it is:** **DM partition checksums** (and **DV incremental checksum** probes) hash a **normalized subset** of columns — not always every byte of every type. Some types are **skipped**, **rounded**, or **canonicalized** so small or lossy changes do not change the checksum.

**Common blind spots (DM checksum):**

| Category | Examples | Effect |
|----------|----------|--------|
| Skipped legacy LOBs | SQL Server `text`, `ntext`, `image`; Oracle LOBs, `LONG`, `XMLTYPE`, `VECTOR` | Column excluded from checksum input — changes invisible to default checksum |
| Float rounding | SQL Server float (`CONVERT(,2)`), Redshift REAL, VECTOR TME | Binary noise or tail bits may not change hash |
| Timestamp precision | High-precision `datetime2`, Redshift TIMESTAMP | Sub-nanosecond / readback truncation |
| Spatial as WKT | SQL Server / Redshift / Oracle geometry | Compared as despaced WKT; Oracle L3 WKT truncated at 4000 chars |
| Redshift `HLLSKETCH` | Redshift only | Hashed via `HLL_CARDINALITY` — distinct sketches with the same cardinality are invisible |
| Custom expression only | `checksumExpression: MAX(ORA_ROWSCN)` | Only that expression drives change detection — data edits elsewhere ignored |

**DV vs DM:** DM checksum skipped columns may still appear in **DV L3 row-hash** (different pipeline). Do not tell the user "DV will catch it" without checking column selection and L3 config.

**Agent guidance when user is confused:**

1. Confirm **sync strategy** — watermark only sees rows above the watermark; checksum only sees partition aggregate change.
2. Identify column **data type** — if in skipped/lossy list, explain that default checksum may not detect the edit.
3. **Remediation options:** run a **full** migration/validation once; set a custom **`checksumExpression`** covering the column (DM/DV incremental checksum); switch affected columns to **watermark** if a monotonic column exists; use **DV L3** with `validationCustomNormalizationRules` when the issue is compare semantics, not sync detection.
4. For SQL Server **`text`/`ntext`/`datetime`** specifically: legacy LOBs are checksum-excluded; datetime formatting uses ODBC-style text — sub-second or timezone-only edits may not move the hash.

DM sync field reference: [SynchronizationStrategy](../../migrate-objects/actions/data-migration/references/workflow-config-reference.md#synchronizationstrategy).
