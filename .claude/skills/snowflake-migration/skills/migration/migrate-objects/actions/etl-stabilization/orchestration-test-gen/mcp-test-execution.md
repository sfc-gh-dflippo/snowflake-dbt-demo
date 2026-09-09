# MCP Test Execution Protocol

How to execute orchestration test files using the `snowflake_sql_execute` MCP tool. This is the ONLY way to run SQL against Snowflake — do NOT use Python scripts, `cortex source`, or `snowflake.connector`.

## Test File Structure

Test files contain four sections delimited by marker comments:

- `-- ============================================================` followed by `-- ARRANGE:SETUP`
- `-- ============================================================` followed by `-- ARRANGE:SEED`
- `-- ============================================================` followed by `-- ACT` (or `-- ACT: <element_name> (N of M in group <group>)`)
- `-- ============================================================` followed by `-- ASSERT` (or `-- ASSERT: <element_name> (N of M in group <group>)`)

Each section starts after its marker and ends at the next marker (or end of file).

## Section Execution Rules

| Section | How to execute | Result handling |
|---------|---------------|-----------------|
| ARRANGE:SETUP | Send entire section as one multi-statement `snowflake_sql_execute` call | No result needed — DDL only. Check for errors. |
| ARRANGE:SEED | Send entire section as one multi-statement `snowflake_sql_execute` call | No result needed — TRUNCATE+INSERT only. Check for errors. |
| ACT | Single `CALL` statement via `snowflake_sql_execute` | Check for errors. ACT failure on unfixed code is expected. |
| ASSERT | All assertions combined into a single UNION ALL query via one `snowflake_sql_execute` call | Parse result rows: each row is `assert_name:PASS` or `assert_name:FAIL: details`. Collect per-assertion. |

**Why batched ASSERT works:** Each SELECT in the UNION ALL returns one row prefixed with the assertion name (`assert_01_name:PASS` or `assert_01_name:FAIL: details`). A single `snowflake_sql_execute` call returns all rows, allowing per-assertion attribution without multiple round trips. Snowflake's parser handles `$$`-delimited blocks and `:variable` binds correctly — the agent never needs to split statements manually.

## Isolated Test Execution

For test files with a single element (`<element_name>.sql`):

1. Read the test file
2. Identify the four sections by their marker comments
3. Execute in order: ARRANGE:SETUP → ARRANGE:SEED → ACT → ASSERT
4. Execute ASSERT as one **batched** call — combine all assertions into a single UNION ALL query:
   ```sql
   SELECT 'assert_01_{name}:' || CASE WHEN ({query}) THEN 'PASS' ELSE 'FAIL: ' || {details} END AS result
   UNION ALL
   SELECT 'assert_02_{name}:' || CASE WHEN ({query}) THEN 'PASS' ELSE 'FAIL: ' || {details} END
   ```
   Parse result rows: each row is `assert_name:PASS` or `assert_name:FAIL: details`
5. Update element status via `track_status.py update`

## Grouped Test Execution

For test files with multiple elements (`grouped_<group_name>.sql`):

Grouped tests have **multiple ACT blocks** (one per element, executed in order) and **multiple ASSERT blocks** (one per element). Execution order matters because grouped elements share state.

1. Read the test file
2. Execute ARRANGE:SETUP (shared DDL for all elements) — one multi-statement call
3. Execute ARRANGE:SEED (shared data for all elements) — one multi-statement call
4. Execute each ACT block **in order** (ACT: element_1, then ACT: element_2, ...) — each is a single CALL
5. Execute each ASSERT block as one **batched** call per element — combine all assertions for that element into a single UNION ALL query:
   ```sql
   SELECT 'assert_01_{name}:' || CASE WHEN ({query}) THEN 'PASS' ELSE 'FAIL: ' || {details} END AS result
   UNION ALL
   SELECT 'assert_02_{name}:' || CASE WHEN ({query}) THEN 'PASS' ELSE 'FAIL: ' || {details} END
   ```
   Parse result rows: each row is `assert_name:PASS` or `assert_name:FAIL: details`
6. Attribute PASS/FAIL to the correct element based on the `-- ASSERT: <element_name>` marker
7. Update each element's status via `track_status.py update`

## Fix-Test Iteration Protocol (used by orchestration-fixer)

During the fix-test loop, the fixer modifies ACT and re-runs. The execution sequence changes after the first cycle:

**First cycle:**
1. ARRANGE:SETUP — create all test objects (run once)
2. ARRANGE:SEED — populate all tables
3. ACT — execute baseline or first fix attempt
4. ASSERT — collect results

**Subsequent cycles** (after modifying ACT in the test file):
1. **Re-read the test file** (content changed since ACT was edited)
2. ARRANGE:SEED — re-run (one call, resets all data)
3. ACT — re-run modified element (one call)
4. ASSERT — re-run batched assertions for that element (one call)

Skip ARRANGE:SETUP on iterations — objects already exist. Only re-run ARRANGE:SETUP if you modified the SETUP section itself (e.g., added a missing mock table).

## Infrastructure Deduplication

When `_infrastructure.sql` exists in the test directory (phases with 5+ isolated elements):

1. Execute `_infrastructure.sql` via `snowflake_sql_execute` **once** before any test files — send entire file as one multi-statement call
2. Infrastructure objects (control_variables, GetControlVariableUDF, UpdateControlVariable, and conditional helpers) are pre-created in the task schema by the orchestrator via `_infrastructure.sql`. Test files' ARRANGE:SETUP should contain only element-specific DDL.
3. Do NOT re-execute `_infrastructure.sql` for each test file

## Error Handling

| Section | Failure type | Action |
|---------|-------------|--------|
| ARRANGE:SETUP | Permission denied / object not found | Fix DDL, retry (max 3), then skip element |
| ARRANGE:SEED | Missing table / type mismatch | Fix seed data or SETUP, retry |
| ACT | EWI-related error | Expected baseline failure — record and proceed to ASSERT |
| ACT | Infrastructure error (missing UDF/SP) | Acceptable limitation — document in coverage gaps |
| ACT | Unexpected error | Possible test bug — fix ARRANGE or SP wrapping, retry |
| ASSERT | SQL error | Test bug — fix assertion query and retry |
| ASSERT | FAIL: result | Record failure details for test_report.md |
