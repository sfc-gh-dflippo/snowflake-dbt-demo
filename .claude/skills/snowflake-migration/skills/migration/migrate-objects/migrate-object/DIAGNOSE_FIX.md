# Diagnose & Fix

`fixCode` for one object. Read the failures, name a root cause, apply a
faithful fix or stop. The machine retries the failed task when you stamp
`completed` — do not jump to [SKILL.md](SKILL.md) by hand.

You diagnose. Do not spawn a review agent, and do not spawn investigators
because a later step is titled "swarm". Read `VALIDATION.LATEST`, the source
SQL, and the converted SQL yourself. The one
[`test_case_verifier`](../../../../agents/test_case_verifier.md) is spawned
from `runTests` after you stamp, not from here.

## Step 1: Iteration context

If this is the first pass, skip. Otherwise recall what you already tried
and do not repeat an unchanged approach.

```
Iteration: <N>
Previous attempts:
- Iteration 1: <what> → <error or diff>
Approaches to avoid:
- <failed approach>
```

## Step 2: Failure context

```
query_registry(where="id = '<objectId>'", fields="id,source,files,target")
```

Hold `files.source.path`, `files.converted.path`, `files.artifacts.path`.
Read `<metadata_database>.VALIDATION.LATEST` (attach names that
database; it is not the migration target). There is no
`<project_dir>/test-results/results.json`. For each `FAIL` / `ERROR` on
this object, take `params_hash`, `parameters`, `error_message`, and
`differences`. Then read the source SQL and the converted SQL. A deploy
error is the context when this loop entered from a compile failure.

## Step 3: Known shortcuts

Check these before inventing a new theory. A match is a fix (or a stop),
not a swarm.

**Documented conversion / load errors**

- Error 002232 (invalid virtual column) — inline the UDF.
- Mixed-quote PIVOT identifiers — fix quoting.
- All-rows-different from column order, case, or formatting — reorder /
  alias / cast when that still means what the source means.
- Decimal / rounding / timestamp precision — normalize only when that
  still means what the source means. A wall-clock expression (`GETDATE`,
  `CURRENT_TIMESTAMP`, age-from-today) is not a normalize: go to Step 5.
- Snowflake 001187 (`COPY INTO` refused on CHECK constraints) — delete
  the `CONSTRAINT … CHECK` clauses from the converted `snowflake/` file,
  then deploy. Do not `ALTER TABLE … DROP CONSTRAINT` on the live table.

**Dynamic SQL** in the error or the converted file (`EXECUTE IMMEDIATE`,
`IDENTIFIER(`, `sp_executesql`, `EXEC(` / `EXEC @`): read
[../../rule-engine/resolving-ewis/reference/SSC-EWI-0030.md](../../rule-engine/resolving-ewis/reference/SSC-EWI-0030.md)
and use those patterns in the edit.

**YAML `steps:` do not match the proc** — this is not a SQL bug. Load
[`EDIT_TEST_YAML.md`](EDIT_TEST_YAML.md) when the failure smells like:

| Smell | Recipe |
|---|---|
| Multiple result sets / "got N, expected M" | Multi-result-set validation |
| OUT / INOUT param column null or missing | OUT / INOUT parameter comparison |
| DML proc, "no rows captured" | Side-effect-only DML |
| Proc writes a table the YAML never reads | Table-read assertion |
| Redshift refcursor / `RESULT_SCAN` empty | Cursor-read step |
| `"ANONYMOUS BLOCK"` vs Redshift param name | Redshift scalar INOUT aliasing |
| Teradata 5315 on the source side | Teradata cross-database GRANTs |

Apply the recipe under `<project_dir>/<files.artifacts.path>/test/` (glob
`*.yml`; `files.artifacts.path` verbatim). Recapture with
`scai test capture --where "source.canonicalName ILIKE '%<object_name>%'"`,
then stamp `fixCode` completed so the machine retries `runTests`. Nothing
to redeploy.

**Rules.** `find_similar_rules` with the primary error or first diff.
`regex` → apply `replacement_find` / `replacement_replace` and
`record_rule_application`. `ai` → use `ai_context` as diagnosis, not as
an accept. A name starting `[AVOID]` is an approach not to repeat.

## Step 4: Name the root cause

| Finding | Action |
|---|---|
| Converted logic ≠ source | Edit converted SQL |
| Missing schema prefix | Add the prefix |
| Source function left as T-SQL | Snowflake equivalent |
| YAML `steps:` mismatch | Step 3 recipe, recapture |
| Precision / collation / padding, and a CAST or `RTRIM` still means what the source means | Edit converted SQL, then **note** (you chose among meanings) |
| Diffs are clock drift and the source (or a view it reads) computes from now | Step 5 — do not edit |
| Dialect error-code / SQLSTATE mismatch (`error_mismatch`) while both sides error | Do not delete the YAML case. Stamp and retry; a second verifier is allowed after a later code change. |
| Missing object, and `next_task` on that id is not terminal | Do not stamp. The walk derives the wait from that object's status. |
| Source cannot run as written (INSERT…EXEC column-count, missing source columns, source `EXEC` error) | Escalate. Do not edit converted SQL to invent columns the source file does not have, and do not `ALTER` source. |
| You cannot name a cause after reading the files and any matching rule | Escalate with the diffs and the readings you cannot choose between |

Override-accept is last. "The baseline moved by a day" is not enough if
CAST, a prefix, YAML shape, or a collation/`RTRIM` would make the case
pass.

A missing reference is an escalation, not a `-- NEEDS-USER:` comment and
not a stub (`NULL` / `WHERE FALSE`) or a borrowed object.

## Step 5: Wall-clock — stop, do not overlay here

When the only remaining failures are clock drift from an expression that
must stay (`GETDATE`, `CURRENT_TIMESTAMP`, `CURRENT_DATE`, `DATEDIFF`
against now, age-from-today), a code change would lie. Do not edit. Do
not call `override_accept_case` yourself. Do not spawn a verifier.

Stamp `fixCode` completed. The machine retries `runTests`; that guide
hands every remaining hash to one
[`test_case_verifier`](../../../../agents/test_case_verifier.md).
Rejected hashes come back as `error="sql"`.

## Step 6: Apply a code fix

Edit `files.converted.path` only. Minimal change. Keep source comments.
Do not strip `EXECUTE AS` or the SnowConvert `COMMENT` provenance block
unless the error named them.

Before deploy, also drop a leading `USE DATABASE <source_db>`. Do not
rewrite the database qualifier to the SNAP / configure name — `deploy -d`
does that.

If the edit chose among meanings (CHECK drop so COPY can run, `RTRIM` for
trailing-space collation), **note** per
[general-task.md](../../../../agents/general-task.md) §4, then stamp
`fixCode` completed. The machine's `retryEntry` is the redeploy / retest.
Do not spawn a reviewer for the note.
