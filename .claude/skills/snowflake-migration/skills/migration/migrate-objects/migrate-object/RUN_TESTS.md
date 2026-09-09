# Run Tests

Guide for the `runTests` task. The machine invokes this after deployment succeeds for procedures and functions, and after baseline capture for BTEQ scripts (which are not deployed).

## Run validation

The `scai test validate` tool compares Snowflake output against captured baselines. Baselines were captured during the prep phase — this step only re-runs validation.

`scai test validate` writes each case into
`<metadata_database>.VALIDATION.RESULTS`. Read the latest run from
`VALIDATION.LATEST` (attach names `metadata_database` — same catalog as
ORCHESTRATION, not the migration target). There is no
`<project_dir>/test-results/results.json`.

```
sql_execute:
SELECT params_hash, status, parameters, error_message, differences,
       baseline_rows, actual_rows, match_type
FROM <metadata_database>.VALIDATION.LATEST
WHERE UPPER(procedure_name) IN (
        UPPER('<source.database>.<source.schema>.<source.name>'),
        UPPER('<source.schema>.<source.name>')
      )
```

Each row has `procedure_name`, `status`, `match_type`, `error_message`, and `differences`. Focus on rows where `status` is not `PASS`. BTEQ result rows carry `metadata.kind: "bteq"` and compare file I/O + table deltas rather than a return value.

## Test statuses

| Status | Meaning |
|--------|---------|
| `PASS` | Output matches baseline |
| `FAIL` | Output differs from baseline |
| `ERROR` | Exception during execution |
| `NO_BASELINE` | No captured baseline exists for this test case. Run `scai test capture` first. |

## Check for dependency failures first

Before attempting a fix, check whether the failure is caused by a **missing dependency** (table, view, function, or procedure that hasn't been migrated yet). Fixing code won't help if the real problem is a missing object.

### Dependency failure patterns

Scan the `error` field from failing test entries for these patterns:

| Pattern | Likely Cause |
|---------|-------------|
| "does not exist" | Missing table, view, or schema |
| "object does not exist" | Missing dependency object |
| "unknown function" | Function not yet migrated |
| "unknown procedure" | Procedure not yet migrated |
| "invalid identifier" | Column from unmigrated table/view |
| "unresolved reference" | Unresolved cross-object reference |
| "cannot resolve" | Missing schema or object |

### If a dependency failure is detected

1. **Identify the missing object** from the error message (e.g., `Unknown function: dbo.HelperFunc`).
2. **Find it in the registry** with `query_registry` — you need its `id`:
   ```
   query_registry(
     where="source.canonicalName ILIKE '%<missing_name>%'",
     fields="id,source"
   )
   ```
3. **Ask the resolver where that object stands**, rather than reading a status field yourself:
   ```
   migration_status(mode="next_task", object_ids=["<dependency id>"])
   ```
   It consults whichever source is authoritative for each task and object type — a test-results query, a Snowflake probe, a registry field — and which one that is differs per task and changes. A field you read yourself is not the verdict.
4. **Route on what it says:**

| Resolver result | Action |
|---|---|
| `query_registry` returned no row | **Skip this object.** Report: "Blocked on `<dependency>` — not in registry." |
| `errored`, or `blocked: true` | **Skip this object.** Report: "Blocked on `<dependency>` — " plus its error, or the reason on its `blockedOn` entry. |
| `nextTask` is not null | **Skip this object.** Report: "Blocked on `<dependency>` — still at `<nextTask>`." It has not finished its own walk, so it is not what you should be testing against yet. |
| `nextTask: null`, not errored, not blocked | The dependency is done. If the FAIL is still a defect **in that code unit** (wrong column type, bad view body, missing CAST on *its* SQL), do **not** patch this procedure around it. Spawn one foreground [`task-invalidate`](../../../../agents/task-invalidate.md) (`subagent_type="task-invalidate"`) with that code unit's `id`, the resume task (`validateView` on a view, `runTests` on a procedure), and why — plus this waiter's `objectId` and `runTests` so its verification is also reopened. Then **return** `result: "reopened"` with `reopenedCodeUnits`. Do not stay in the fix loop. If the dependency's SQL is faithful and the FAIL is in *this* code unit, this is not a dependency failure — proceed to fix the code. |

If blocked on a dependency, **do not stamp this task**. Name the specific dependency in your user-facing reply so the user knows what to migrate. The next walk derives `blocked` / `blockedOn` from that dependency's live status.

### If not a dependency failure

Proceed — the machine will route to the fix loop.

## After tests complete

- **All pass:** call `transition_status(status='advance', task='runTests', outcome='completed')`.
- **Any fail (not dependency):** call `transition_status(status='advance', task='runTests', outcome='failed', error='sql')` — the machine routes to rule application and the fix loop. Try to make the cases pass there before any overlay. Use `error='sql'` only when the test failure is caused by a SQL/DDL bug the fix loop can address; for transient infrastructure issues (timeouts, connection drops) use `error='infra'` instead.
- **Still failing after the fix loop, and a code change would be illogical** (source wall-clock expression; freezing "now" would lie): spawn **one** foreground [`test_case_verifier`](../../../../agents/test_case_verifier.md) (`subagent_type="test_case_verifier"`) with fresh context for **all** remaining hashes on this object. Hand `objectId`, `projectDir`, the `params_hash` list, and the RESULTS diffs — not a verdict. That child reads each case and decides. Do **not** call `configure(subagent_mode=true)` for this — that latch is the autonomous orchestrator's, before dispatching walkers. Call it yourself only if the project set `require_independent_override_accept: false`. See [general-task.md](../../../../agents/general-task.md) §4. Do not stamp `runTests` completed and do not delete the YAML case. The oracle joins the overlay on `(procedure, params_hash, target)`; RESULTS still shows FAIL. The call is also a `note` (same unreviewed queue). If that child **rejects** and you then change the converted SQL, a later FAIL on the same hash gets a **new** verifier — the first child judged the pre-fix SQL. A second override-accept is allowed.
- **Never delete a YAML test case** (overflow, short-input, leftover RESULTS FAIL). Keep the row; overlay or fix SQL.
