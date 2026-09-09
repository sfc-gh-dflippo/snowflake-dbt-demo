# Validate View

Compare a deployed view between source and Snowflake to verify the migration produced equivalent results.

**IMPORTANT:** Run this validation as a foreground subagent to avoid polluting the parent context window.

## Inputs

- `<schema>.<view_name>` — the view to validate
- `<snowflake_connection>` — attach `snowflake_connection:` / first-prompt
  `snowflakeConnection`. Pass it as `sql_execute` `connection` (`-c`).
- `<snowflake_database>` — the Snowflake **target** from `configure` attach
  (`snowflake_database:`) / the walker's first prompt. Not `source.database`
  and not the workload catalog name.

## Step 1: Row Count Comparison

```
query_source("SELECT COUNT(*) FROM <source_schema>.<view_name>")
```

Compare with:

```
sql_execute(
  connection="<snowflake_connection>",
  sql="SELECT COUNT(*) FROM <snowflake_database>.<SCHEMA>.<VIEW_NAME>",
  description="Count rows in the deployed target view"
)
```

`query_source` is the source database. `sql_execute` is Cortex Snowflake and
does not inherit `configure` — pass `connection` from attach
`snowflake_connection:` / the first-prompt `snowflakeConnection`, and qualify
with `<snowflake_database>`. Do not fall back to shell, `snow sql`, Python, or
an unqualified query.

## Step 2: Spot Check

```
query_source("SELECT TOP 10 * FROM <source_schema>.<view_name>")
```

Compare with:

```
sql_execute(
  connection="<snowflake_connection>",
  sql="SELECT * FROM <snowflake_database>.<SCHEMA>.<VIEW_NAME> LIMIT 10",
  description="Sample rows from the deployed target view"
)
```

Check for:
- Column name mismatches
- Data type differences (e.g. datetime precision, numeric scale)
- NULL handling differences
- Character encoding or collation issues

## Step 3: Report

Return a structured result:
- **Row count match:** yes/no (source count vs Snowflake count)
- **Column differences:** any mismatched column names or types
- **Data differences:** any value mismatches from the spot check
- **Verdict:** pass/fail
- **If fail, classify the cause** — see Step 4.

## Step 4: Classify the Failure

Before reporting fail, identify *why*. The classification drives how the parent advances the task and how the user is told about it.

| Cause | Signal | `error` code |
|---|---|---|
| The view's DDL is wrong (compile error, column missing, type mismatch, bad expression) | Snowflake-side query errors, or values diverge despite full data | `sql` |
| Snowflake side has 0 rows (or far fewer) because base tables haven't had data migrated yet | Source has rows; Snowflake-side count is 0 or anomalously low; the view's `dependencies` in the registry list tables whose live `migrateData` job is not completed | *(do not stamp)* |
| Validation couldn't run (connection drop, query timeout, permissions) | Tool-level error, not a row-count divergence; do not substitute a shell query | `infra` |

When the parent calls `transition_status(... outcome="failed", error=<code>)`:
- `error="sql"` routes to the rule engine + fix loop (`applyRules` → `fixCode`). Use ONLY when the SQL needs editing.
- Do not stamp a dependency wait. The walk already surfaces those tables on `blockedOn`; name them in your reply and leave the task unstamped.
- `error="infra"` lands in the errored bucket; the user retries.

If validation passes, return success and the parent will call `transition_status(... outcome="completed")` with no `error`.
