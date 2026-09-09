# Task Model Reference (DMVF)

Condensed reference for debugging migration and validation workflows. Full internal docs: `dmvf/docs/data-migration-orchestrator/task-model.md` and `scopes.md`.

## Executors

| Executor | Runs on | Typical tasks |
|----------|---------|---------------|
| `orchestrator` | SPCS (or local) | Partition strategy, task fan-out, staged-data processing, validation evaluate |
| `data-exchange-agent` | Worker (local or SPCS) | Source extraction, checksum collection, validation query execution |
| `warehouse` | Snowflake warehouse | `COPY INTO`, DDL, Snowpipe drain barriers |

## Task structure

| Field | Description |
|-------|-------------|
| `id` | Unique task id |
| `workflow_id` | Owning workflow |
| `executor_type` | Which executor pulls this task |
| `task_name` | Human-readable label (use in reports) |
| `payload` | Task-specific JSON |
| `status` | Lifecycle state (see below) |
| `priority` | Lower number = higher priority |
| `scope` | Hierarchical purpose identifier |
| `successor_task_id` | Task to unblock when this completes |
| `is_blocked` | Waiting on predecessor(s) |
| `last_error_message` | Failure reason when `status` is `failed` |

## Task lifecycle

| Status | Meaning |
|--------|---------|
| `pending` | Ready to be pulled |
| `blocked` | Waiting for predecessor |
| `executing` | In progress |
| `completed` | Success |
| `failed` | Execution failed |
| `abandoned` | Lease expired without completion |
| `paused` | Manually suspended — not pullable |

Typical migration flow per table:

```
Preprocessing (metadata + schema + partition strategy)
    → Extraction (per partition, DEA, parallel)
    → Loading (process staged data + COPY INTO / Snowpipe)
    → Complete partition metadata
```

Validation adds L1/L2/L3 chains with Snowpipe drain barriers when `useSnowpipeForResults` is true.

## Scope grammar

Every task has a `SCOPE`: a hierarchical string of `::`-joined fragments, ordered least → most specific, describing the task's purpose and target. Scopes drive prefix queries, **rate limiting** (`RATE_LIMIT.SCOPE_PATTERN`), and the pause/resume/cancel procedures — all match `SCOPE` with SQL `LIKE`. The owning workflow is tracked separately in `TASK_QUEUE.WORKFLOW_ID` (not embedded in table/partition scopes).

### Data migration scopes

| Pattern | Meaning |
|---------|---------|
| `Table[DB.SCHEMA.TABLE]::Preprocessing` | Table setup phase (metadata + partition strategy) |
| `Table[DB.SCHEMA.TABLE]::Partition[N]::Extraction` | Partition extraction (DEA) |
| `Table[DB.SCHEMA.TABLE]::Partition[N]::DeletionKeysExtraction` | Primary-key extraction for `trackDeletions` (distinct from `Extraction`) |
| `Table[DB.SCHEMA.TABLE]::Partition[N]::Loading` | Partition load (`COPY INTO` / Snowpipe) |
| `Table[DB.SCHEMA.TABLE]::Preprocessing::SnowpipeSetup` / `::SnowpipeTeardown` | Snowpipe pipe create / drop |
| `Table[DB.SCHEMA.TABLE]::Preprocessing::PreflightSetup` | Preflight (bounded dry-run) setup |
| `preflight::<workflowId>::schema_drop` | Drop transient `PREFLIGHT_<workflowId>` schema |
| `workflow::<workflowId>::transient_cleanup` | Clean up transient resources at workflow end |

The table identifier in `Table[...]` is the **normalized source FQN** (for example `MY_DB.DBO.CUSTOMERS`).

### Data validation scopes

Validation tasks are prefixed with `DV::` so they never collide with migration scopes.

| Pattern | Meaning |
|---------|---------|
| `DV::Table[ID]::Preprocessing` | Validation metadata / table prep |
| `DV::Table[ID]::SchemaValidation` | L1 schema validation |
| `DV::Table[ID]::Partition[N]::MetricsValidation` | L2 metrics validation |
| `DV::Table[ID]::Partition[N]::RowValidation` | L3 row-hash validation |
| `DV::Table[ID]::Partition[N]::CellDrilldown` | Hybrid L3 cell drill-down (may carry `Batch[k]` before the op) |
| `DV::Table[ID]::Partition[N]::WriteResults[row\|cell]` | Write results (row-hash or cell); batched as `...::Batch[k]::WriteResults[cell]` |
| `DV::Table[ID]::Evaluate[LEVEL]` | Evaluate a completed level |
| `DV::Table[ID]::ReconcilePossibleMismatches` | Post-drilldown reconcile of `POSSIBLE_MISMATCH` |
| `DV::Table[ID]::L3EarlyStopMonitor` | Periodic L3 early-stop monitor |
| `DV::Table[ID]::DetectionComplete` / `::SyncBaseline` / `::SyncFinalize` | Incremental validation bookkeeping |
| `DV::Pipe[KEY]::SnowpipeSetup\|SnowpipeTeardown\|SnowpipeDrain\|SnowpipePrepareDrain` | Snowpipe ops for validation results |
| `DV::ObjectTypeDetection::Preprocessing` | Object-type dispatch task |

### Querying / matching by scope

```sql
-- All tasks for one table (migration):
SELECT ID, NAME, STATUS, LAST_ERROR_MESSAGE
FROM SNOWCONVERT_AI.DATA_MIGRATION.TASK_QUEUE
WHERE WORKFLOW_ID = <id>
  AND SCOPE LIKE 'Table[MY_DB.MY_SCHEMA.MY_TABLE]::%'
ORDER BY ID;
```

The same `LIKE` matching powers rate-limit `SCOPE_PATTERN` rules (e.g. `Table[%]::Loading` caps concurrent loads) and scope-filtered queries or pause/cancel (e.g. `DV::Table[%]::Partition%::RowValidation` selects L3 tasks). See [rate limiting](../../../../data-infrastructure/references/advanced-operations-reference.md#rate-limiting-protect-source-or-shared-resources).

## Dependency model

- Tasks start `blocked` when they depend on predecessors; the orchestrator unblocks successors on `COMPLETE_TASK`.
- Fan-out tasks (partition strategy, create partition tasks) use higher priority and unblock many children.
- Cleanup tasks (Snowpipe teardown, preflight schema drop) are `.blocked().cleanup()` — they run after all non-cleanup tasks reach a terminal state.
- A task stuck in `blocked` with no `executing`/`pending` predecessor often indicates a **missing or failed predecessor** — inspect earlier tasks in the same scope chain.

## Debugging heuristics

### 1. Dependency / ordering anomalies

**Symptoms:** Tasks remain `blocked` long after earlier phases should have finished; workflow shows `Finished` but tables incomplete.

**Steps:**
1. List non-terminal tasks: `STATUS IN ('pending','executing','blocked')`.
2. For each `blocked` task, find tasks in the same `SCOPE` prefix with lower `ID` that are not `completed`.
3. Check whether a failed extraction left load tasks permanently blocked.

### 2. Per-task failure reasons

```sql
SELECT ID, NAME, EXECUTOR_TYPE, STATUS, FAILURES, LAST_ERROR_MESSAGE, SCOPE
FROM SNOWCONVERT_AI.DATA_MIGRATION.TASK_QUEUE
WHERE WORKFLOW_ID = <id>
  AND STATUS = 'failed'
ORDER BY ID;
```

Cross-reference `TaskName` / `LastErrorMessage` with MCP `reports.files.errors`.

### 3. Source-connectivity classification

| Error pattern | Likely cause |
|---------------|--------------|
| `TableNotFoundError`, zero-row metadata | Worker `database` ≠ workflow `source.databaseName` |
| `Engine 'X' not found in source connections` | Worker claiming wrong workflow / stale tasks / missing connection section |
| ODBC / network timeout | Firewall, wrong host/port, missing egress allowlist for SPCS worker |
| Syntax error near `TOP`/`LIMIT` in extraction | Invalid `whereClauseCriteria` |

### 4. `POSSIBLE_MISMATCH` after completion

Hybrid L3 may stop early when `earlyStoppingForRowHashing` or `maxFailedRowsNumber` triggers. A finished workflow can report `POSSIBLE_MISMATCH` — this is **not** a clean pass. Review L3 result rows before signing off.

## Workflow management procedures

Procedures live in the migration metadata schema (default `SNOWCONVERT_AI.DATA_MIGRATION`):

| Procedure | Effect |
|-----------|--------|
| `PAUSE_WORKFLOW(workflow_id)` | Pause all active tasks; set workflow status `paused` |
| `PAUSE_TABLE(workflow_id, source_table_fqn)` | Pause tasks for one table scope |
| `RESUME_WORKFLOW(workflow_id)` | Unpause workflow tasks |
| `RESUME_TABLE(workflow_id, source_table_fqn)` | Unpause one table |
| `CANCEL_WORKFLOW(workflow_id)` | Fail active tasks, cascade to blocked successors, cancel workflow |
| `CANCEL_TABLE(workflow_id, source_table_fqn)` | Cancel one table's tasks |

`source_table_fqn` must match the identifier inside `Table[...]` in task scopes.

## Priority system

Lower number = higher priority. Fan-out / strategy tasks ≈ 1; extraction spread across 2–3; default ≈ 3.

## Related references

- [Troubleshooting reference](./troubleshooting-reference.md)
- [Workflow config reference](./workflow-config-reference.md)
- [Data Doctor reference](../../../../data-infrastructure/references/data-doctor-reference.md)
