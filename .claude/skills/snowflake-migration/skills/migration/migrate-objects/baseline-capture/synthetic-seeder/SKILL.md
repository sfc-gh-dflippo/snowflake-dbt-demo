---
name: synthetic-seeder
description: >
  Generate two-sided synthetic data tests (source + Snowflake) for migrated stored
  procedures and functions. Derives test scenarios from source SQL branch analysis,
  writes step-based validation YAML artifacts, and enriches them with isolation metadata.
  Use when generating or refreshing test cases for a migrated object.
  Delegates object repair to migrate-object. Triggers: generate tests, create tests,
  write test YAML, test generation, synthetic tests.
parent_skill: baseline-capture
---

# Synthetic Seeder Skill

Generate two-sided synthetic data tests for migrated stored procedures and functions.
Tests are derived from **source SQL analysis** — the source is the oracle, not the
converted code. Each test is a step-based YAML artifact directly consumable by
`scai test capture` and `scai test validate`.

> **YAML schema reference.** See [`../../references/step-based-yaml.md`](../../references/step-based-yaml.md) for the step types (SQL Query / Output Parameter / Table Read / Cursor Read), the `validate: true | false | [list]` semantics, and the `modifies_data` / `affected_tables` inference rules. This file describes *what* to generate for each procedure; the cheat sheet is the source of truth for the *shape* of each step. For special cases (multi-RS, OUT params, cursor reads, before/after capture) see [`../../migrate-object/EDIT_TEST_YAML.md`](../../migrate-object/EDIT_TEST_YAML.md).

> **Autonomous mode:** When spawned as a subagent, skip interactive stopping points,
> apply reasonable defaults, document assumptions in the completion report, and send
> a `send_message` to `main` when done.

---

## Scope and Boundaries

**This skill does:**
- Analyze source SQL to identify branches, NULL paths, boundary values
- Generate two-sided INSERT / CALL / SELECT steps in both source and Snowflake dialects
- Execute the Snowflake side to validate the test SQL (not the object)
- Write YAML artifacts with `test_cases: [[]]` for test-runner compatibility
- Enrich YAMLs with `modifies_data` and `affected_tables` for clone isolation
- Fix test SQL if Snowflake execution fails (up to 3 retries)

**This skill does NOT:**
- Repair the migrated object — delegate failures caused by object bugs to `migrate-object`
- Run `uv run migrate` or `run_migration_tests` — test execution is handled by `scai test capture` + `scai test validate`
- Generate tests for TABLEs or VIEWs (procedures and functions only)
- **Generate tests for BTEQ scripts.** Units with `kind: "script"` (BTEQ) author a `validation.steps[].script` block per [../seed-script/SKILL.md](../seed-script/SKILL.md) from user-provided bindings + import fixtures — they are not synthesized here. Do not invent `test_cases:` for them.

---

## Available MCP Tools

| Tool | Purpose |
|------|---------|
| `configure()` | Retrieve `project_dir`, `source_dialect`, `snowflake_database` |
| `query_registry` | Look up code unit metadata and transitive dependencies for isolation enrichment |
| `snowflake_sql_execute` | Execute SQL on Snowflake for validation |

---

## Output Format

Each test is a YAML file following the `ValidationMetadata` schema:

```yaml
validation:
  test_cases:
  - []
  steps:
  # Setup steps — validate: false
  - source_query: <source-dialect INSERT or DDL>
    target_query: <Snowflake INSERT or DDL>
    validate: false
  # Call steps — validate: true (default, key omitted)
  - source_query: <EXEC / source CALL>
    target_query: <Snowflake CALL>
  # Assertion steps — validate: true (default, key omitted)
  - source_query: <SELECT from modified table, source dialect>
    target_query: <SELECT from modified table, Snowflake>
```

**IMPORTANT:** Every YAML **must** include `test_cases: [[]]` (a list containing one empty list). This is required by `test-runner` discovery. Step-based tests embed all data inline in the steps, so the test case list contains a single empty-parameter entry.

**File layout:** The object's test directory is whatever `files.artifacts.path`
returns from the registry (Phase 0.4) with `/test/` appended — read it, do not
construct it. It may use a placeholder database segment (e.g.
`database_unspecified`) and lowercased names for some dialects; that is correct
and must be preserved. `files.artifacts.path` is PROJECT-RELATIVE, so prefix it
with `<project_dir>/` for all filesystem writes/reads (capture resolves it as
`project_root / files.artifacts.path / test`).

```
<project_dir>/<files.artifacts.path>/test/
  <sanitized_object_name>.0.yml   ← one data arrangement
  <sanitized_object_name>.1.yml   ← another data arrangement
```

`<sanitized_object_name>` (for the FILE name only) replaces non-alphanumeric
characters (except `.` and `-`) with `_`.

**YAML granularity rule:**
- **One YAML per data arrangement** — scenarios that require distinct INSERT data get their own file
- **Multiple calls/selects in one YAML** — scenarios exercisable against the same data state are additional steps within the same file

---

## Qualities of a Good Test

Before generating, internalize these rules:

1. **Deterministic** — no `CURRENT_TIMESTAMP`, `NOW()`, `GETDATE()`, `RANDOM()` or similar. Use fixed constant dates and values only.
2. **Non-trivially non-empty** — each CALL or SELECT step must produce at least 3 distinct, non-empty output rows. Tests producing empty or single-row output rarely catch behavioral differences.
3. **Covers all modified tables** — include SELECT assertions for every table the procedure writes to, not just the return value or the primary output table.
4. **Branch-driven** — read the source SQL for `IF`/`CASE`/`WHILE` branches, NULL-handling paths, boundary values, and parameter variations. Each distinct data arrangement that exercises a different branch gets its own YAML file.
5. **Minimal data** — populate only columns required by the test logic plus `NOT NULL` constraints. Use short strings, small numbers, and brief identifiers.
6. **High-numbered keys** — use values like `9901`, `9902` to avoid colliding with production data.
7. **Idempotent setup** — prefer `INSERT ... SELECT ... WHERE NOT EXISTS (SELECT 1 FROM t WHERE pk = ?)` so tests are safe to re-run.
8. **Fully qualified names** — always use `SCHEMA.TABLE` in all SQL, both source and Snowflake sides.
9. **No object creation** — never `CREATE TABLE` or `CREATE VIEW` in test steps. Only insert into tables that already exist as dependencies. If a required table is missing, that is a dependency bug — report it and stop.
10. **Source is the oracle** — derive expected behavior by reading the source SQL logic, not the Snowflake conversion.

---

## Phase 0: Resolve Object

### 0.1 — Get session config

Call `configure()`. Extract:
- `project_dir` — root of the migration project
- `source_dialect` — e.g. `Teradata`, `MS SQL Server`
- `snowflake_database` — target Snowflake database

### 0.2 — Identify the object

This skill expects an `<object_name>`.

### 0.3 — Check skip condition

We skip objects that already have a seeded test YAML. The test directory is whatever
`files.artifacts.path` reports (fetched in 0.4) — do not reconstruct it from the object
name — so this check runs in 0.4 (Step 1.2), once that value is known.

### 0.4 — Locate SQL files

CUR is the source of truth for file paths — use `query_registry` instead of
`find` so we do not rely on filename heuristics.

**Step 1 — Get the object's files and dependency IDs.** Call `query_registry`
with:
- `where` = `"source.canonicalName ilike '%<object_name>%'"`
- `fields` = `"id,source,target,files,dependencies"`
- `include_dependencies` = `true`

From the response, read both SQL files (resolve paths relative to
`<project_dir>`):
- `files.source.path` — original source SQL
- `files.converted.path` — converted Snowflake SQL
- `files.artifacts.path` — base directory for this object's test artifacts (used in Phase 4)

Collect every `dependencies.dependsOn[*].id` for Step 2.

**Step 1.1 — Oracle package member check:** if `source.package` is non-empty in the
registry entry, this is a package member. Record:
- `source_package` = value of `source.package` (e.g. `"ITEM_MGMT"`)
- `source_schema` = value of `source.schema` (e.g. `"TEST"`)
- `target_schema` = value of `target.schema` (e.g. `"TEST_ITEM_MGMT"` — SnowConvert convention: `{source_schema}_{PACKAGE_NAME}`)

These three values are used in Phase 3 to construct the correct call syntax.

**Step 1.2 — Skip if already tested (the 0.3 check).** Now that `files.artifacts.path`
is known, check whether this object already has a seeded test YAML:

```bash
find <project_dir>/<files.artifacts.path>/test -name "*.yml" -type f
```

If any `.yml` is found: **skip this object**, report it as already tested, and (if
looping) call `next_object()` for the next candidate — no need to fetch dependencies.

**Step 2 — Get the dependency files in one call.** Call `query_registry`
again with:
- `where` = `"id in ('<id1>', '<id2>', ...)"` (comma-separated IDs from Step 1)
- `fields` = `"id,source,files"`

For each result, read `files.source.path` and `files.converted.path`. Skip
entries where `files` is missing (built-in or external object).

You now have the full picture of what tables exist, their columns,
constraints, and what the procedure modifies.

---

## Phase 1: Analyze and Plan

### 1.1 — Identify modified tables

From the source SQL, list every table the procedure writes to (INSERT, UPDATE, DELETE, MERGE, TRUNCATE). These tables **must** have SELECT assertion steps in every YAML.

### 1.2 — Identify branches and scenarios

Read the source SQL carefully. For each logical branch, note:
- The condition that activates it (e.g. `IF @status = 'ACTIVE'`, `CASE WHEN amount > 1000`)
- What tables are modified differently per branch
- NULL or empty-input edge cases
- Boundary values (zero, negative, maximum, date boundaries)

### 1.3 — Produce coverage matrix

Before generating any SQL, produce a table of planned YAMLs. Each row is one file:

```
YAML index | Scenario description          | Key distinguishing data         | Branches covered
---------- | ----------------------------- | --------------------------------| ----------------
0          | Happy path — status ACTIVE    | status='ACTIVE', amount=500     | main INSERT branch
1          | High-value path               | status='ACTIVE', amount=1500    | threshold CASE branch
2          | NULL input                    | status=NULL                     | NULL guard / COALESCE branch
```

**STOPPING POINT** (interactive mode): Present the coverage matrix and ask the user to confirm or adjust before generating. Autonomous agents: proceed and document the matrix in the completion report.

---

## Phase 2: Arrange — Generate Insert Steps

For each YAML in the coverage matrix, generate the setup steps.

### Rules for insert steps

- Each INSERT statement is **one step** with `source_query` and `target_query`
- `validate: false` on every setup step
- Source and target inserts carry the same data values; only the SQL dialect differs
- Batch multiple rows in a single INSERT where possible (saves steps):
  ```sql
  INSERT INTO SCHEMA.T (col1, col2) VALUES (9901, 'A'), (9902, 'B');
  ```
- For columns where source dialect uses type casting or date literals differently, adapt per side
- Do **not** use time/date conversion functions inside `VALUES` clauses on the Snowflake side — use `SELECT ... AS col` pattern instead:
  ```sql
  -- Invalid in Snowflake inside VALUES
  INSERT INTO T (dt) VALUES (TO_TIMESTAMP_NTZ('2024-01-01'));
  -- Correct
  INSERT INTO T (dt) SELECT TO_TIMESTAMP_NTZ('2024-01-01') AS dt;
  ```
- Respect `NOT NULL` constraints — always populate those columns
- For `CHAR(N)` columns in source dialect, pad values with trailing spaces as required

---

## Phase 3: Act + Assert — Generate Call and Select Steps

### Call steps

- One `CALL` (Snowflake) / `EXEC` or `CALL` (source) step per scenario or parameter combination
- For procedures with multiple output parameters, include SELECT statements immediately after the call to read their values
- Use `:out_param` syntax on the Snowflake side for OUT parameters
- If the source uses `EXEC proc @param = value` syntax, translate to positional `CALL proc(value)` on the Snowflake side

**Dialect-specific call guidance:**
- **Oracle** — load [`./platforms/oracle.md`](./platforms/oracle.md) for: anonymous PL/SQL block execution model, `source_declare` syntax, package member three-part FQN, artifact path conventions, OUT params / SYS_REFCURSOR.
- **Teradata** — load [`./platforms/teradata.md`](./platforms/teradata.md) for: cross-database GRANT steps required before each CALL in clone-isolated environments.

### Assertion SELECT steps

For **every table identified as modified in Phase 1**, add a SELECT step:

```sql
SELECT <essential_columns> FROM SCHEMA.TABLE ORDER BY <pk_col>;
```

Rules:
- Always include `ORDER BY` for deterministic output comparison
- Select only columns relevant to the test scenario — avoid `SELECT *` when many columns are noise
- Do not add `WHERE` clauses that would hide the procedure's effects
- On the Snowflake side, align column names and aliases to match the source side (the runner does semantic comparison but matching names help)

---

## Phase 4: Write Artifacts

### 4.1 — Write YAML files

For each successfully validated YAML (index 0, 1, 2, ...), write to:

```
<project_dir>/<files.artifacts.path>/test/<sanitized_name>.<idx>.yml
```

`files.artifacts.path` is the value fetched from `query_registry` in Phase 0.4, Step 1 — use it as-is rather than reconstructing it. `<sanitized_name>` (for the FILE name only) replaces non-alphanumeric characters (except `.` and `-`) with `_`. Write each file under `<project_dir>/<files.artifacts.path>/test/`.

> **Fail fast when the CUR has no artifacts path.** If `files.artifacts.path` is missing or empty, stop and report a CUR/dependency bug. A `database_unspecified` database segment is NOT a bug — it is the legitimate source-DB placeholder emitted by the arranger; use it as-is.

**Oracle package members:** see [`./platforms/oracle.md`](./platforms/oracle.md) — the CUR `files.artifacts.path` already includes the package subdirectory; always read it from `query_registry`.

YAML content — **always include `test_cases: [[]]`**:
```yaml
validation:
  test_cases:
  - []
  steps:
  - ...
```

---

## Phase 5: Enrich YAMLs with Isolation Metadata

After writing YAMLs, populate `modifies_data` and `affected_tables` by combining
DML tables extracted from the test steps with the code unit's transitive
dependencies from CUR.

The bundled script handles only the YAML scan and rewrite — **the agent must
fetch CUR dependencies via the `query_registry` MCP tool** and pass them to the
script via `--extra-tables`.

### 5.1 — Fetch dependency tables from CUR

Call the `query_registry` MCP tool with:
- `where` = `"source.canonicalName ilike '%<object_name>%'"`
- `fields` = `"id,source,target,dependencies"`
- `include_dependencies` = `true`

From the returned JSON, take entries in `dependencies.dependsOn[*]` whose
`source.objectType == 'table'`, and use each entry's `target.canonicalName`
as the FQN (e.g. `["DBO.CUSTOMERS", "DBO.ORDERS"]`). Non-table dependencies
(views, procedures, functions) are dropped — `affected_tables` must contain
tables only.

If the unit has no table dependencies, this list is empty — the script will
still enrich based on DML in the steps.

### 5.2 — Run the enrichment script

```bash
python <SKILL_DIR>/enrich_yamls.py <project_dir> "<object_name>" \
  --extra-tables "<fqn>,<fqn>,..."
```

Where `<SKILL_DIR>` is the directory containing this SKILL.md (use the
absolute path), and `--extra-tables` is the comma-separated list of FQNs from
Step 5.1. Omit `--extra-tables` (or pass an empty string) when CUR returned
no dependencies.

The script:
1. Scans each YAML for INSERT/UPDATE/DELETE/MERGE in source/target query steps
2. Unions those with the FQNs from `--extra-tables` into `affected_tables`
3. Sets `modifies_data: true` if any affected tables found, `false` otherwise

---

## Phase 6: Self-Check and Report

### 6.1 — Self-check

Before returning, verify every committed YAML exists on disk and contains isolation metadata:

```bash
find <project_dir>/<files.artifacts.path>/test -name "*.yml" -type f
```

Count must equal the number of YAMLs in the coverage matrix that passed validation. If any file is missing: generate it before returning.

### 6.2 — Report

Report to the user (or `send_message` to `main` in autonomous mode):

```
Test generation complete for <object_name>:

  YAMLs planned:    N  (coverage matrix)
  YAMLs validated:  M  (Snowflake execution passed)
  YAMLs written:    M
  YAMLs enriched:   M  (modifies_data + affected_tables added)
  Object bugs found: K  (if any — needs migrate-object)

  Scenarios covered:
    0: <scenario description>
    1: <scenario description>
    ...

  Artifacts: <project_dir>/<files.artifacts.path>/test/

  Next: run `scai test capture` and `scai test validate` to execute the tests.
```

> **Note (when called from `migrate-objects/baseline-capture/SKILL.md`):** the caller loads `baseline-capture/CAPTURE.md` immediately after this skill returns to run `scai test capture` and upload baselines. The migrate-object loop then runs `scai test validate` each iteration. Do not run capture/validate yourself in that flow — just report completion so the parent can continue.

---

## Snowflake SQL Dialect Rules

Apply these when writing `target_query` steps:

- Use `CALL` to invoke procedures — never `SELECT` or `EXEC`
- For table-returning functions: `SELECT * FROM TABLE(fn(args))`
- OUT parameters in CALL: `CALL proc(in_val, :out_var)`
- `DECIMAL`/`NUMERIC`/`DEC` are synonyms for `NUMBER` — do not replace them
- `TRUNC(x)` before `CAST(x AS INT)` when source T-SQL uses integer truncation
- Date/time values in INSERTs: use `SELECT ... AS col` pattern (not inside `VALUES`)
- Do not construct identifiers from string concatenation with `IDENTIFIER()`
- Fully qualify all object references: `DATABASE.SCHEMA.OBJECT`

---

## Troubleshooting

### INSERT fails: "column does not exist"
Read the dependency DDL file again — column name may differ between source and Snowflake sides. Use the Snowflake DDL column names in `target_query`, source DDL names in `source_query`.

### INSERT fails: "NOT NULL constraint"
Identify the NOT NULL columns from the DDL and add them to the INSERT. Use minimal placeholder values (`0`, `'X'`, `'1900-01-01'`).

### CALL fails: "object does not exist"
The procedure or a dependency is not deployed. This is an **object bug** — stop and report. Do not retry.

### CALL produces empty output
The test data does not satisfy the procedure's WHERE clauses or join conditions. Trace the source SQL logic and adjust the INSERT values so the rows match the procedure's filter predicates.

### Row count less than 3
Add more INSERT rows covering additional input combinations. Each row should produce a distinct output row.
