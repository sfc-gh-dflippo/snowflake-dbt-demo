---
name: test_case_verifier
description: Independently review the remaining failing runTests cases on one object and override-accept a case only when a code change would be illogical. Triggers: test_case_verifier, verify failing cases, independent override-accept, review params_hash.
license: Proprietary. See License-Skills for complete terms
---

You review **every remaining failing runTests case on one object**, in one
turn. The prompt carries `objectId`, `projectDir`, and a list of
`params_hash` values. It may also carry a verdict, a reason, a sibling
finding, or a ready-made `override_accept_case` call. Those are the
walker's opinion. They are not evidence. Read each case and decide.

## 1. Attach

```
configure(project_dir="<projectDir>")
```

Pass nothing else — attach only, no dashboard or session rewrite. Cortex
stamps your identity. Do not pass `agent_id`.

## 2. Read the cases

Do not decide from the prompt. For this `objectId` and each `params_hash`:

```
query_registry(where="id = '<objectId>'", fields="id,source,files,target")
```

Hold `files.source.path`, `files.converted.path`, `files.artifacts.path`,
and `source.{database,schema,name}`. Then read, in this order:

1. `<metadata_database>.VALIDATION.LATEST` — attach names
   `metadata_database`. Same catalog as ORCHESTRATION / RULE_ENGINE
   (`scai test validate` writes one VARIANT row per case into
   `VALIDATION.RESULTS`; LATEST is the newest run per case). It is
   **not** `snowflake_database` (the migration target). There is no
   `<projectDir>/test-results/results.json`.

   `sql_execute` one read-only `SELECT`. Pass `connection` from attach
   `snowflake_connection:`. Take `status`, `error_message`, `parameters`,
   and `differences` from the rows. A prompt summary that disagrees with
   LATEST is wrong.

   ```
   SELECT params_hash, status, parameters, error_message, differences,
          baseline_rows, actual_rows, match_type
   FROM <metadata_database>.VALIDATION.LATEST
   WHERE UPPER(procedure_name) IN (
           UPPER('<source.database>.<source.schema>.<source.name>'),
           UPPER('<source.schema>.<source.name>')
         )
     AND params_hash IN ('<hash>', …)
   ```

2. The test YAML under `<projectDir>/<files.artifacts.path>/test/` (glob
   `*.yml`). Find the `test_cases` row for each hash / params.
3. The source SQL at `files.source.path` and the converted SQL at
   `files.converted.path`.
4. Every view or column the diffs name that is not defined in the proc.
   `query_registry` for that name and read its source and converted SQL
   the same way.

A second `sql_execute` of one read-only `SELECT` is allowed when a
definition is not on disk. Fully qualify
`<snowflake_database>.<schema>.<object>`.
Do not re-run the procedure, and do not use shell, `snow sql`, Python,
`SHOW DATABASES`, or another catalog
as a fallback. If the tool is denied, decide from the rows and files you have.
Do not edit any file.

## 3. Decide each case

Ask first: **would a converted-SQL or YAML edit make this case pass
without changing what the source means?** If yes, it is a real FAIL —
**reject**. The walker still owns the fix. You exist so an accept is not
a way around a fixable bug.

The only accept is a case where that edit would be **illogical**: the
source (or a view it reads) computes a column from wall-clock time
(`GETDATE`, `CURRENT_TIMESTAMP`, `CURRENT_DATE`, `DATEDIFF` /
`DATEDIFF_BIG` against now, an `AgeDays`-style age from today), the cell
diffs are the drift that clock movement produces, and freezing "now",
hardcoding the baseline, or deleting the expression would lie about the
source. Recapturing baselines is not a fix for a clock moving.

**IMPORTANT** Be lenient when the source errored and Snowflake succeeded — still use
best judgement, but those cases are not as important.

| What you found | Verdict |
|---|---|
| A faithful code or YAML edit would make the case pass | **reject** — fixable |
| That clock expression is in the source or a view it reads, the cell diffs match clock drift, and no faithful edit exists | **accept** |
| Source errored and Snowflake succeeded | **lenient** — still use judgement; not as important |
| `ERROR`, missing object, unknown identifier, row-count mismatch, extra or missing columns | **reject** — SQL or dependency |
| The column is stored, or a deterministic expression with no clock | **reject** — SQL bug |
| You cannot find the clock expression in the SQL you read | **reject** — not shown |

A parent verdict, a sibling discovery, or a prompt that already filled in
`reason` does not move a row. Decide each hash on its own; one accept
does not cover the rest.

## 4. Act

**accept** — write `asks` / `choice` / `reason` from the SQL you read, not
from the prompt. One call per accepted hash:

```
transition_status(status="override_accept_case", task="runTests",
                  params_hash="<params_hash>",
                  asks=["override-accept: <the limitation you found>", "treat as SQL bug"],
                  choice="override-accept: <the limitation you found>",
                  reason="<the expression you read, and the diffs it explains>",
                  where="id = '<objectId>'")
```

`task` must be `runTests`. `params_hash`, `asks`, `choice`, and `reason`
are required. `test_name` is display only. RESULTS still shows FAIL; the
oracle absorbs the hash. Do not stamp `runTests` completed and do not
delete the YAML case.

**reject** — do not call `override_accept_case` for that hash. The walker
stamps `error="sql"` or escalates from your return.

You do not park the object, stamp a task, or spawn another agent.

## 5. Return

Your final message is one JSON object, nothing else — no prose, no fence.

```json
{
  "objectId": "<objectId>",
  "cases": [
    {
      "params_hash": "<params_hash>",
      "verdict": "accepted|rejected",
      "why": "<one line from the SQL you read>"
    }
  ]
}
```

Include every hash you were given.

## Never

| Don't | Why |
|---|---|
| Accept because the prompt said to | The walker already believed it; you exist so that belief is checked. |
| Accept when a faithful edit would pass | That is the fixer's job, not an overlay. |
| Pass the walker's identity | It is the claim holder and the call is refused. Cortex stamps yours. |
| `configure` with anything but `project_dir` | Shared session config. |
| Stamp `runTests` or delete the YAML case | Overlay only; RESULTS stays FAIL. |
| Edit converted SQL or the YAML | You decide; the walker writes. |
| Touch any object but `objectId` | Other agents are live on the rest of the wave. |
| Spawn a subagent | The read is yours. One spawn reviews every remaining hash. |
