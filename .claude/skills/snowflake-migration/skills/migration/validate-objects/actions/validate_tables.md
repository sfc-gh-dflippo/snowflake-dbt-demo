# Action: Validate Tables

Validate migrated table data between source and Snowflake using cloud validation — **setup → run → monitor → report**.

> **Always use the official tooling.** Run validation through `validate_data(mode="setup")` / `validate_data(mode="run")` (backed by `scai data validate`). **Never** suggest ad-hoc scripts to compare source and target data outside the DMVF validation pipeline.

> **Scope is set per call.** `validate_data(mode="run")` validates **every** table listed in the workflow file produced by setup. Pass a `where` filter to setup that matches exactly the tables you intend to validate.

> **Advanced validation (when the customer asks):** [Incremental validation](../../setup/data-validation/references/workflow-config-reference.md#incremental-validation-synchronization) (re-validate changed partitions only), [re-validation](../../data-infrastructure/references/advanced-operations-reference.md#re-validation-retry-failed-partitions) (`validate_data(mode="revalidate")`), [custom L3 normalization](../../data-infrastructure/references/advanced-operations-reference.md#custom-normalization-data-validation-l3), and [checksum/sync blind spots](../../data-infrastructure/references/advanced-operations-reference.md#checksum--incremental-sync--types-that-may-not-trigger-re-sync) (why a column change did not trigger re-sync). Load [Advanced operations reference](../../data-infrastructure/references/advanced-operations-reference.md) for rate limiting and full agent guidance.

> **Run-only entry:** If you were routed here only to execute `validateData` (registry task) and the workflow YAML already exists, skip Step 1 and complete **Step 2** (display the existing `workflow_path` and offer optional updates) before **Step 3**. Complete **Steps 4–5** (background Monitor and error-first validation report), then return the result to the parent. Per-object subagents do not manage shared infrastructure or teardown.

## Step 1: Choose validation approach + generate workflow

### 1.A — Validation mode and sync (captured at setup)

Validation mode (full vs incremental) and sync strategy are **captured once at setup** by the `dataStrategy` task (executor [`../../setup/data-strategy/SKILL.md`](../../setup/data-strategy/SKILL.md)) and committed, so they are **already set** when you dispatch — do not re-ask. If they are unexpectedly missing or the user requests a change, return to the main agent; it owns the setup change and redispatch. The choices:

| Choice | Meaning |
|--------|---------|
| **Full** | Validate all partitions every run (`synchronization.strategy: none`) |
| **Incremental** | Re-validate only partitions that changed since the prior baseline |
| Sync **Checksum** | Hash partitions; re-validate changed ones (supported on all platforms, including Oracle) |
| Sync **Watermark** | Track a monotonic column; re-validate partitions with newer values |

After the machine completes, confirm with the user:

```
Validation approach:
  Tables (where): <registry filter or "all in scope">
  Mode:           <full | incremental>
  Sync:           <none | checksum | watermark>
```

For **watermark**, ask which column to use (`watermarkColumn`, e.g. `UPDATED_AT` / `SignupDate` / `SIGNATURE`) before editing YAML. Remind the user that the **first** incremental run still validates everything (establishes the sync baseline); later unchanged runs skip validation.

### 1.B — Generate the validation workflow

Translate the user's choices into a `validate_data(mode="setup", ...)` call.

For a Snowflake-source project, omit `where`.
`scai data validate generate-config` writes a Snowflake-to-Snowflake template
from project metadata. Read that template, ask for the source and target fully
qualified object names and any mappings needed, and fill the YAML before
running. Do not query or require the Code Unit Registry.

For the `where` filter, in order of preference:

1. **You already have the claimed object IDs** (e.g. from a `transition_status(status="begin", ...)` response). Use them verbatim — `where="id IN ('<id1>', '<id2>', ...)"`.
2. **Specific table names.** `where="source.canonicalName IN ('dbo.Customers', 'dbo.Orders')"`.
3. **A whole schema or wave.** `where="source.schema = 'dbo'"` or `where="planning.wave = 'wave_1'"`.
4. **All deployed tables.** Omit `where`. Only do this if the user explicitly asked to validate everything.

If you're unsure of the registry filter columns, run `scai code where` for the syntax reference.

```
validate_data(
  mode="setup",
  where="<registry filter>",
  validation_type="full" | "incremental",   # from state machine; persisted
  sync_strategy="none" | "checksum" | "watermark",  # from state machine; persisted
  schema_validation=true | false,    # optional; persisted as a session default
  metrics_validation=true | false,   # optional; scai default is false — pass true only if user wants metrics
  row_validation=true | false,       # optional; scai default is true
  continue_on_failure=true | false,  # optional; persisted as a session default
)
```

Do **not** prompt for `metrics_validation` unless the user asks for aggregate-statistics comparison. Omit the param to keep scai's default (`false`).

**"Full" ≠ metrics on.** `validation_type=full` (vs incremental) only means re-validate the whole table — it does **not** mean enable L2 metrics. Keep `metrics_validation` / `metricsValidation` **false** unless the user explicitly asked for metrics / aggregate statistics.

Setup patches known `validation_configuration` toggles and, when mode/sync are known, `defaultTableConfiguration.synchronization.strategy`. For watermark, still edit `watermarkColumn` (and ensure partition columns) per `edit_hints` before run.

If setup returns `status: "error"` with a message about validation not being configured, load `../../setup/data-validation/SKILL.md` to complete the one-time infrastructure setup, then retry.

## Step 2: Display, optional edits, confirm

The setup response contains:

- `workflow_path` — `artifacts/data_validation/workflows/<hash>.yaml`. Same `where` always maps to the same file; distinct filters produce distinct files.
- `regenerated` — `false` means scai re-used an existing file.
- `defaults` — the merged session defaults applied to this call (includes `validation_type` / `sync_strategy`).
- `applied_overrides` — toggle values that were patched into `validationConfiguration`.
- `applied_synchronization` — sync strategy patched into `defaultTableConfiguration.synchronization` when known.
- `edit_hints` — use as a guide when the user is unsure what can be changed.

1. Read `workflow_path`.
2. **Display** the workflow file to the user:
   - **Small/medium files** — show the full YAML in chat.
   - **Large files** — show the path, `validationConfiguration`, sync block, `tables:` count, and table names; offer to show the full file or specific tables on request.
   - Note whether setup **reused** an existing file (`regenerated: false`).
3. **Summarize:** table count, validation mode/sync, effective validation toggles (`schema_validation`, `metrics_validation`, `row_validation`, `continue_on_failure`), and which levels will run (e.g. schema + row; metrics off unless enabled).
4. Ask verbatim:

> Here is the validation workflow at `<workflow_path>`.
>
> **Would you like to update any fields before we run?**
> 1. **Proceed**
> 2. **Change something** (tell me which table, section, or field names)

5. **If the user chooses "Change something":** apply the user's requested edits using `../../setup/data-validation/references/workflow-config-reference.md` (prefer camelCase — for example `columnMappings`, `indexColumnList`, `sourceWhereClause` + `targetWhereClause`, `targetDatabase` / `targetSchema` / `targetName`, `synchronization.watermarkColumn`; snake_case aliases such as `index_column_list` and legacy `whereClause` still parse). Re-display the sections you changed. Repeat the question in step 4 until the user chooses **Proceed** or says they are done editing.

   **Common scenarios → fields to edit:**

   | User goal | Workflow fields |
   |-----------|-----------------|
   | Limit compared rows | `sourceWhereClause` + `targetWhereClause` (both required; set matching predicates on each side) |
   | Skip L2 on wide tables | `excludeMetrics` or disable `metricsValidation` |
   | Whitelist known diffs | `acceptedTransformations` |
   | Rename / remap columns | `columnMappings`, `indexColumnList`, `targetIndexColumnList` |
   | Faster L3 on huge tables | `earlyStoppingForRowHashing`, `maxFailedRowsNumber` |
   | Reduce source locking | `queryModifiers` |
   | Incremental watermark | `synchronization.watermarkColumn` (+ `columnNamesToPartitionBy`) |

   For stalled or partially finished runs, see [Task model reference](../../migrate-objects/actions/data-migration/references/task-model-reference.md) and [Troubleshooting reference](../../migrate-objects/actions/data-migration/references/troubleshooting-reference.md).

6. **If the user chooses "Proceed":** skip discretionary edits unless agent-only blockers remain (step 7).
7. **Agent-only blockers** — apply without re-prompting unless you need a value from the user:
   - When `row_validation` is on: ensure each table has usable `indexColumnList` (and `targetIndexColumnList` when names differ) per `edit_hints`.
   - When incremental **watermark**: ensure `watermarkColumn` is set on `defaultTableConfiguration.synchronization` (or per table).
   - When incremental: ensure partition columns (`columnNamesToPartitionBy`) are present.
   - Verify `targetDatabase` / per-table targets match the deployed Snowflake objects.
   - Tell the user what you changed and why before confirming.
8. **Apply user-requested edits before run (hard gate).** If the user already asked to change the workflow (turn metrics off, narrow tables, etc.), those edits are **not optional**:
   - Write them into `workflow_path`, re-display the changed sections, and only then accept “Proceed” / confirmation to run.
   - **Do not** call `validate_data(mode="run")` while a user-requested edit is still unapplied.
   - **Never flip metrics on for "Full" mode.** If setup wrote `metricsValidation: false` (or the user said metrics off / schema+row only), leave it false — do not set `metricsValidation: true` because the mode is Full or because you want "all three levels." Full vs incremental is orthogonal to schema/metrics/row toggles.
9. **Do not weaken L3 heuristically.** Do not infer exclusions from column
   names or source/target type pairs. Validate the configured columns and
   report mismatches. Any deterministic normalization or exclusion belongs in
   product configuration, not agent guesswork.
10. **Pre-run verification (hard gate).** Before calling `validate_data(mode="run")`, **re-read `workflow_path`** and confirm every user-requested edit from steps 5/8 is actually written to the file and `metricsValidation` matches the agreed value. If a requested edit is missing, apply it now; do not run until the on-disk YAML matches what the user asked for. Then get **explicit confirmation** to run with the final workflow and continue to Step 3.

**Optional — explain validation levels:** After the “update any fields?” question (or while the user is reviewing), offer a brief explanation unless they are clearly repeating a prior run or only asked to execute:

> Would you like a quick explanation of what schema, row, and metrics validation mean before we run?

- **Yes** — summarize from [Validation levels reference](./references/validation-levels-reference.md) (setup toggles table); mention only levels that are **on** in this workflow, plus note that metrics is off by default when disabled.
- **No / skip** — continue the Step 2 flow.

Also answer ad-hoc questions about levels at any time using the same reference; do not block the run on the offer.

## Step 2b: Doctor gate (ran at infrastructure bring-up)

The `scai data doctor` gate runs during `data_infrastructure(mode="up")`
(the prerequisite), **not** on `validate_data(mode="run")` — dispatch is pure.
If setup reported `doctor_failures`, do not repair or bypass them here. Return
the exact remediation to the main agent, which owns infrastructure setup.

## Step 3: Run validation

```
validate_data(mode="run", workflow_path="<path from setup>")
```

On success, returns a `job_id` immediately. Validation runs in the background
through the orchestrator. Non-Snowflake sources also use a Data Exchange
Worker; Snowflake-to-Snowflake validation runs in warehouse without one.

**Show the user the `cost_reminder` from the response** (or relay this if absent):

> **Cost note:** The orchestrator and local worker are running. They can keep using Snowflake credits while idle (the worker polls the warehouse on an interval). When this wave is done, suspend the orchestrator, compute pool, and stop all workers — accept teardown when offered at the end. The local worker started via MCP stops when this Coco session ends; the orchestrator does not.

Retain `workflow_path` for the report in Step 5.

After run starts, go to **Step 4**.

---

## Step 4: Wait for completion with Monitor

Use Monitor for the asynchronous wait. Its `terminal` event carries the
authoritative compact result under `detail.completion`; that event ends the
wait and is sufficient for the final report. `job_status` is for a
user-requested status, lost-watch recovery, or deeper failure diagnostics —
not a required second handoff and not a polling loop.

**Arming Monitor ends your turn.** Say one line to the user and stop. The
event wakes you; nothing you do in the meantime makes the job finish sooner.
Between arming Monitor and its event, run **zero** Bash commands.

**Never wait with Bash.** Do not run `sleep`, shell polling loops, or delayed
shell status checks for a validation job. A long Bash sleep consumes the agent
turn while bypassing the relay. Arm Monitor instead. If its watch is lost,
recover it with `job_status(job_id, monitor=true)` as described below; do not
compensate with `sleep`.

**Never read the reports by hand.** Do not `cat` / `grep` / `head` the CSVs
under `reports/data-validation/`, and do not query the target with
`sql_execute`, to decide whether validation finished or passed. Those files
are side effects of status collection and may be mid-write. The relay fetches
status and reports when the job becomes terminal, then distills them into
`detail.completion` on the Monitor event.

**Status tool:**

```
job_status(job_id="<JOB_ID>")                 # cheap summary
job_status(job_id="<JOB_ID>", details=true)   # + full progress and failure reports
```

`job_id` is `monitor.job_id` from the `validate_data(mode="run")` / `mode="revalidate"` response. Use `migration_status(mode="summary")` for wave-level progress — per-table detail always comes from `job_status(..., details=true)`.

`details` may report `details_unavailable` until `create-workflow` returns a workflow name; that is normal early in the run.

### 4.A — Background monitoring

1. **Phase A — Monitor:** Start the **Monitor** tool (`persistent: true`) with `monitor.watch_command` from the run response, verbatim, from the project root. No wait for a workflow name, and no hand-built command — the cursor baked into it is what prevents replays and gaps.
2. **Phase B — Monitor fire:** Branch on the event's `phase`. `failure` / `stalled` / `relay_error` are warnings — surface them and keep watching. On `terminal`, read `detail.completion` (`verdict`, `terminal`, `failed`, `summary`, `report_row_counts`, optional `failures` / `stale_reports`) → Step 4.B if failed → **Step 5**. Do not call `job_status` merely to confirm the terminal event.

**No progress loop.** Do not start `/loop` or a cron to poll for progress. The relay emits a `stalled` event once a job has gone **30 minutes** without changing, so a quiet job reports itself. A healthy run is silent by design — progress lands in the log, and `job_status(job_id, details=true)` names the tables in flight whenever the user asks (see [Per-table progress narration](./references/background-monitoring.md#per-table-progress-narration-all-paths)).

The watch fires only on terminal, first failure, a 30-minute stall, or relay error — not on ordinary progress. It exits by itself on its job's terminal record.

Tell the user once (plain language) that you'll report back when validation finishes or hits trouble. Do not require them to understand Monitor tool chrome.

**If the watch goes silent,** re-arm with `job_status(job_id, monitor=true)` — it returns a fresh cursor and watch command and restores the relay's poller if it was lost. With no progress loop there is no second timer cross-checking the watch, so this is the recovery path after a compaction, a session restart, or an answer that looks stale.

### 4.A.1 — Health monitoring

Monitor emits `stalled` and `failure` events. On either event, call
`job_status(job_id, details=true)` once to inspect the current state, surface
the warning, and keep the Monitor armed.

| Signal | Severity |
|--------|----------|
| `stalled` event | **Warning** |
| Repeated unresolved `stalled` event | **Critical** |
| `failure` event or failed table state | **Warning** (immediate) |

**What to tell the user** (short; do not block waiting unless they ask to stop):

```markdown
**Validation health** — `<workflowName or "starting…">`
- Tables: <validated+failed>/<total> resolved (<validated> OK, <failed> failed)
- **Warning:** No table progress in <N> minutes.  <!-- stall -->
- **Critical:** No table progress in <N> minutes.  <!-- stuck -->
```

On **Warning** or **Critical**, point to [Troubleshooting Reference](../../migrate-objects/actions/data-migration/references/troubleshooting-reference.md) (stale `TASK_QUEUE` tasks, worker DB mismatch, affinity). Do **not** auto-cancel the workflow — offer: keep waiting, open troubleshooting, or pause/teardown if the user wants to stop cost.

A stall or stuck warning does **not** end monitoring — only a `terminal` event does.

When a job fails before a workflow exists, the failure text is in the job's `summary` — surface it under **Execution** (or **Infrastructure** when no table progress exists) in Step 5.

### 4.B — Finished workflow with pending tables (anomaly)

The terminal event already classifies pending tables as `failed`. If
`detail.completion.failed == true`, call
`job_status(job_id, details=true)` once for per-table diagnostics, then check
whether `details.progress.output.isFinished == true` **and** any of:

- `validatedTables + failedTables < totalTables`
- any `tableStates[].status == "Pending"`

**Do not report “Passed”.** Treat as failures (matches scai `HasErrors` — tables left pending when the workflow finished).

1. List pending tables under **Execution** as “never validated” — use `errorMessage` when set; otherwise `details.reports.files.data_validation_errors` or “Table not validated — check task errors”.
2. Pull detail from `details.reports.files` before guessing. Do **not** treat `metricsValidated: null` as failure when metrics was disabled.
3. If messages are thin, follow [Workflow finished but tables incomplete](../../migrate-objects/actions/data-migration/references/troubleshooting-reference.md#workflow-finished-but-tables-incomplete) — query `TASK_QUEUE` for the workflow. Worker/orchestrator issues are one cause, not the only one.
4. Do **not** suggest re-run until prerequisites are identified.

---

## Step 5: Report — data validation summary

**Do not skip.** Present an **error-first** summary in chat (markdown). Build
the headline from the Monitor terminal event's `detail.completion`. On
failure, use the optional `job_status(job_id, details=true)` response
(`details.progress`, `details.reports`) for deeper classification — **not** a
per-table results grid unless the user asks.

### 5.A — Read inputs

Read **`validationConfiguration`** from the workflow YAML (or `defaults` / `applied_overrides` from setup) to know which levels ran: `schemaValidation`, `metricsValidation`, `rowValidation`.

| Source | Fields |
|--------|--------|
| Monitor terminal `detail.completion` | `verdict`, `status`, `terminal`, `failed`, `summary`, `report_row_counts`, optional `failures` / `stale_reports` |
| Workflow toggles | `validationConfiguration.metricsValidation` — when **false**, metrics were **not executed**; do not discuss or report them |
| Optional `job_status` `details.progress.output` | Failure diagnostics: `workflowName`, `isFinished`, `workflowStatus`, `totalTables`, `validatedTables`, `failedTables`, `tableStates` |
| Optional `job_status` `details.reports.files` | Failure diagnostics: `schema_validation_results`, `metrics_validation_results`, `row_validation_summary`, `row_validation_results`, `data_validation_errors`, `results` |

`metricsValidated`: `true` = passed; `null` = not run (N/A); do **not** treat `null` as a metrics failure when `metrics_validation` was false in the workflow.

`detail.completion` is authoritative and always exists on a terminal event,
even when the source has no full report. `job_status(job_id, details=true)`
remains available when a failed completion needs the full per-table report.

### 5.B — Derive headline **Result** (header only)

| Outcome | **Result** line |
|---------|-----------------|
| All passed | `Passed — <N>/<N> tables OK` |
| Some failures | `<N_ok>/<N_total> tables OK — <F> failed` |
| **Finished but pending** (Step 4.B) | `<N_ok>/<N_total> tables OK — <F> never validated` |
| Job failed / no meaningful progress | `Failed — no tables validated` (adjust counts if partial) |

**Never** use the all-passed **Result** when Step 4.B applies — even if the job reached `terminal` without `failed`.

**Workflow** line: `` `details.progress.output.workflowName` ``.

**Header shows only `Result` and `Workflow`** — no elapsed time, check toggles, workflow file path, or job id in the header.

### 5.C — Classify errors (fixed category order)

List categories **only when they have at least one error** and that check **was enabled** in the workflow (except **Execution**, which applies whenever infra/runtime failed), always in this order:

| Order | Category | When to include | Sources |
|-------|----------|-----------------|---------|
| 1 | **Schema** | `schema_validation == true` | `schemaValidated == false`, `details.reports.files.schema_validation_results`, schema-related `errorMessage` |
| 2 | **Metrics** | **`metrics_validation == true` only** | `metricsValidated == false` (not `null`), `details.reports.files.metrics_validation_results` |
| 3 | **Row** | `row_validation == true` | `rowsValidated == false`, `row_validation_summary`, `row_validation_results`, `cell_validation_results` |
| 4 | **Execution** | always when applicable | `status == "Pending"` with `isFinished` (Step 4.B), `status == EXECUTION_ERROR`, `data_validation_errors`, connectivity/infra `errorMessage` |

**Never** add a **Metrics** subsection when `metrics_validation` was false — missing metrics CSV rows and `metricsValidated: null` are expected, not failures.

A table may appear in more than one category when multiple checks failed — place each issue under the appropriate category.

**Deduplicate within a category:** identical messages → one bullet + `- Affects: \`table1\`, \`table2\`, …`. Prefer concrete text from `details.reports.files` (e.g. `ColumnValidated`, `SourceValue`, `SnowflakeValue`) over generic `errorMessage` when available.

**Category gloss (optional, first use in this conversation):** When a category subsection appears under `### Errors`, you may add one short line under the header using the glosses in [Validation levels reference](./references/validation-levels-reference.md). Skip glosses if you already explained levels at Step 2 or the user declined.

### 5.D — Suggested fixes

Number fixes in the **same order** as **Errors** (skip categories that were disabled or had no errors): Schema → Metrics → Row → Execution. One item per error group when deduped. Prefer prerequisite actions over blind re-run — include workflow YAML mapping overrides, re-migration when data is wrong, and `../../data-infrastructure/SKILL.md` for execution/infra failures.

Do **not** include a per-table markdown table unless the user asks.

### 5.E — Template (present to the user)

**All passed:**

```markdown
## Data validation complete

**Result:** Passed — <N>/<N> tables OK
**Workflow:** `<workflowName>`

No validation mismatches or execution errors.
```

**Failures:**

```markdown
## Data validation — passed with failures

**Result:** <N_ok>/<N_total> tables OK — <F> failed
**Workflow:** `<workflowName>`

### Errors

**Schema**
<!-- optional one-line gloss: column definition mismatches, not cell values -->
- `<table>` — <column/type mismatch or message>
- <shared message>
  - Affects: `<table>`, …

**Metrics**
<!-- omit entire Metrics subsection when metrics_validation was false -->
- <message>
  - Affects: `<table>`, …

**Row**
<!-- optional one-line gloss: specific cell values differ on matched keys -->
- <message>
  - Affects: `<table>`, …

**Execution**
<!-- optional one-line gloss: infra/runtime, not a data comparison -->
- <message>
  - Affects: `<table>`, …

### Suggested fixes

1. **Schema (<tables>)** — …
2. **Metrics (<tables>)** — …  <!-- omit when metrics_validation was false -->
3. **Row (<tables>)** — …
4. **Execution (<tables>)** — …
```

Omit empty category subsections. On full success **and when Step 4.B does not apply**, omit `### Errors` and failure fixes. If the job failed before any progress existed, use a **failed** title and put the job's `summary` under **Execution**.

### 5.F — After failures (optional follow-up)

Do **not** prompt before presenting the Step 5 summary. **After** the error-first report, when there were validation failures, optionally offer:

> Want a brief explanation of what the Schema / Row / Execution sections mean, or help prioritizing fixes?

Use [Validation levels reference](./references/validation-levels-reference.md) for report-category definitions; focus on categories that actually appeared in `### Errors`. Skip this offer if you already explained levels at Step 2 and the user did not ask.

### 5.G — Offer re-validation when data mismatches remain

**After** the Step 5 summary (and optional 5.F follow-up), **before Step 6 (teardown)**, offer a retry menu when **all** of the following hold:

| Condition | Required? |
|-----------|-----------|
| `details.progress.output.isFinished == true` | Yes |
| `failedTables > 0` **or** Schema / Row / Metrics errors in `### Errors` | Yes |
| Step 4.B pending-tables anomaly | **No** — investigate first; do not offer re-validation |
| **Execution** failures only (infra, worker, orchestrator, connectivity) | **No** — fix via `../../data-infrastructure/SKILL.md` first |

Re-validation retries **failed partitions only** from the finished parent workflow — it is **not** a full re-run of every table. Chain resolution is automatic: pass the workflow name from the run that just finished (`details.progress.output.workflowName`).

By default, schema-failed tables **reuse** the parent's partition metadata and re-run only their failing data partitions (schema is **not** re-checked, so a table whose only failure was schema is skipped). If the failures were schema/target-definition issues you have since fixed and want re-checked, add **`recheck_schema=true`** — it re-runs the full pipeline for schema-failed tables. Leave it off for data-mismatch retries.

Ask verbatim when eligible:

> Some tables still have validation failures. How would you like to proceed?
>
> 1. **Retry failed partitions only** (recommended when data fixes are done) — re-validation from workflow `<workflowName>`
> 2. **Apply fixes first** — edit workflow YAML / fix source data / re-migrate, then retry
> 3. **Re-run full validation** — `validate_data(mode="setup", where=...)` then `mode="run"` (new workflow, all tables in scope)
> 4. **Investigate further** — TASK_QUEUE, worker/orchestrator health (`../../data-infrastructure/SKILL.md`)
> 5. **Stop** — proceed to Step 6 (teardown)

**If the user picks option 1:**

```
validate_data(mode="revalidate", workflow_name="<details.progress.output.workflowName>")
```

Add `recheck_schema=true` when the fixes were to schema / target definitions and you want schema re-checked (otherwise schema-failed tables re-run only their failing data partitions and are not schema-checked).

Then repeat **Steps 4–5** (background Monitor, then present a new error-first report). Skip Step 6 teardown until the user picks **Stop** or all tables pass. Relay the `cost_reminder` from the revalidate response when infrastructure starts.

**If the user picks option 2:** guide fixes from `### Suggested fixes`, then offer this menu again when ready.

**If the user picks option 3:** return to Step 1 (setup) with a `where` filter scoped to failed tables when possible.

**If the user picks option 4 or 5:** continue to Step 6 when wave data work is done for this pass.

When all tables passed on the first run, skip 5.G and continue to Step 6.

---

## Step 6: Offer to Suspend Infrastructure (Cost Saving)

This step belongs to the main agent that owns the wave/session, never a
per-object subagent. A per-object subagent returns its Step 5 report and stops.

After every active slot has returned and the wave's data work is complete, the
main agent offers to tear down the shared infrastructure to save idle cost — a
single prompt regardless of placement (default **Yes**):

> Tear down the shared data infrastructure now to stop accruing SPCS / warehouse cost? Bring it back for the next wave with `data_infrastructure(mode="up")` (dispatch does not auto-resume).
>
> 1. **Yes (default)** — call `data_infrastructure(mode="down")`.
> 2. **No, keep running** — useful if you're starting the next wave immediately and want to avoid the ~60s warm-up.

On **Yes** (or no response), call `data_infrastructure(mode="down")` and relay the returned `execution` + `orchestrator`/`worker` actions. Load `../../data-infrastructure/teardown/SKILL.md` **only** for what the tool can't cover: the cross-machine `TASK_QUEUE` check before suspending shared SPCS, a local process started outside MCP (Ctrl+C / `pkill`), or a `partial` payload with an SPCS privilege failure. Then return to the parent skill.

---

## Checklist

```
- [ ] Validation workflow YAML generated via validate_data(mode="setup", ...) (or existing file reviewed at Step 2)
- [ ] User saw workflow YAML and was offered optional field updates (Step 2)
- [ ] User confirmed the final workflow YAML and validation toggles before run
- [ ] validate_data(mode="run") started
- [ ] Monitor armed with the run response's watch command (Step 4)
- [ ] Waited until the job reported a `terminal` event
- [ ] Read the authoritative verdict from Monitor `terminal.detail.completion`
- [ ] Finished-but-pending anomaly checked (Step 4.B — do not report passed if tables still Pending)
- [ ] Health monitoring handled when Monitor emitted an event (Step 4.A.1)
- [ ] Error-first data validation summary presented (Step 5 — Result + Workflow, Errors, Suggested fixes)
- [ ] Re-validation menu offered when eligible (Step 5.G — before teardown, not on Step 4.B or execution-only failures)
- [ ] Teardown offered when wave data work is done (Step 6)
```

Return control to the parent skill (../SKILL.md).

## Reference

- [Advanced operations reference](../../data-infrastructure/references/advanced-operations-reference.md) — rate limiting, incremental DV, revalidate
- [Background monitoring](./references/background-monitoring.md)
- [Validation levels reference](./references/validation-levels-reference.md) — what schema, metrics, row, and execution mean (setup + report)
- [Workflow Config Reference](../../setup/data-validation/references/workflow-config-reference.md)
- [Data validation setup](../../setup/data-validation/SKILL.md)
- [Migration troubleshooting (TASK_QUEUE, worker/orchestrator)](../../migrate-objects/actions/data-migration/references/troubleshooting-reference.md#workflow-finished-but-tables-incomplete)
- [Teardown (cost-saving suspend)](../../data-infrastructure/teardown/SKILL.md)
