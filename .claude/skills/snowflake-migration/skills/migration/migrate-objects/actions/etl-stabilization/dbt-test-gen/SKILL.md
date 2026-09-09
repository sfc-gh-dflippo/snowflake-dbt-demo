---
name: dbt-test-gen
parent_skill: etl-stabilization
description: >
  Generate dbt tests (seeds, schema tests, singular assertions) for ETL-to-Snowflake
  ETL dbt sub-projects. Scoped to dbt projects assigned to the current phase. Use when
  the stabilization skill invokes dbt test generation.
license: Proprietary. See License-Skills for complete terms
---

# dbt Test Generator

Generate and run semantic test cases for dbt project models based on the original dataflow logic in the source definition file. Tests are generated BEFORE fixes are applied, serving as an independent oracle derived from the source-of-truth (the source definition file). All generated test artifacts are stored in `<UNIT>/stabilization/tests/dbt/` to keep the original dbt project clean.

> **Autonomous mode:** When spawned as a team agent, skip all interactive stopping points, make reasonable defaults for user-facing decisions, and document assumptions in the completion report. When done, send a `send_message` to `main` summarizing your results, and respond to any `shutdown_request` with `send_message` using `type: "shutdown_response"` and `approve: true`.

## Main Mode (interactive / standalone use)

Tests follow the **Arrange-Act-Assert (AAA)** pattern: Arrange (dbt seeds), Act (build models), Assert (singular and schema tests). Tests are generated BEFORE fixes, derived from the source definition file — not the dbt model SQL.

## Scope Filtering

> **Concurrent execution note:** You may be spawned concurrently with other agents targeting different dbt projects in the same package. Each agent operates on its own project — do not access or modify files belonging to other dbt projects. Writing test/fix artifacts for another agent's project (even to be helpful) breaks that project's own validator lookup and causes a false missing-artifact failure at phase completion.

Read ROADMAP.md for current phase (authored by stabilization with package-specific reasoning). Process only the dbt project(s) assigned to this phase.

## Input

This sub-skill expects:
- `session_status.json` -- with `source_file_path` set, `migration_object_path`, and dbt projects in status `pending` or `dbt-tested`
- The dbt project folder path (from `dbt_projects` in session status)
- The source definition file path (from `source_file_path` in session status)

## Prerequisites

- `dbt-snowflake` installed and available on PATH
- Active Snowflake connection with a warehouse configured in `~/.dbt/profiles.yml`
- The warehouse can use an empty dummy database -- no pre-populated data or tables are required
- The source definition file must be accessible and readable

## Output Location

All generated test artifacts go into the stabilization folder, NOT into the dbt project itself:

```
<UNIT>/stabilization/tests/dbt/<project_name>/
  seeds/
    <source_name>__<table_name>.csv
    ...
  tests/
    assert_<model_name>_<what>.sql
    ...
  stabilization_test_schema.yml
  stabilization_test_sources.yml
  dbt_project_patch.yml
  test_report.md
```

Before execution, these files are copied into the dbt project (Phase 4). After execution, only the report persists -- the copied files can be cleaned up or kept for re-runs.

## Phase 0: Bootstrap Validation

Before analyzing models, validate that the dbt project's structure and document findings for the dbt-fixer. This phase is READ-ONLY — it identifies and documents blockers but does NOT fix anything. Fixing is exclusively the dbt-fixer's job.

### Step 0.1: Validate dbt_project.yml

Read `dbt_project.yml` and check for:
- Placeholder values (YOUR_PROJECT_NAME, YOUR_PROFILE_NAME) — note as bootstrap blocker
- Missing or invalid `profile` key — note as bootstrap blocker
- Missing `model-paths` — use default `["models"]`

### Step 0.2: Validate Macros

List all `.sql` files under `macros/`. For each:
- Check for obvious syntax errors (unclosed `{% macro %}` / `{% endmacro %}` blocks)
- Check for `!!!RESOLVE EWI!!!` markers — note as fixable by dbt-fixer

### Step 0.3: Attempt dbt parse (quick validation)

```bash
dbt parse --project-dir <DBT_PROJECT_PATH> --profiles-dir ~/.dbt 2>&1
```

If this fails, record the error but DO NOT STOP. The error is documented in the test report and the dbt-fixer will resolve it. Proceed to Phase 1 (source analysis and test file generation do not require dbt parse to succeed).

### Step 0.4: Document Bootstrap Status

Record findings in a `bootstrap_status` section of your test report:
- Config valid: yes/no
- Parse result: pass/fail (with error message if fail)
- Macro issues: list
- Blockers for dbt-fixer: list (these become fix targets)

## Phase 1: Analyze Source Dataflow and dbt Models

Read source and dbt materials in parallel.

### Step 1.1: Read the Source Dataflow

Read the source definition file and locate the dataflow task(s) matching the current dbt project. See `{PLATFORM_DIR}/{transformation_guide}` for source transformation analysis.

For each dataflow task: find `DTS:Executable` elements with `DTS:ExecutableType="Microsoft.Pipeline"` matching the dbt project name, extract pipeline component definitions and column definitions, trace data flow using `pipeline:path` elements.

### Step 1.2: Read the dbt Models

1. Read `dbt_project.yml`, `models/sources.yml` (source table definitions)
2. List all `.sql` files under `models/`; for each: identify `{{ source(...) }}` and `{{ ref(...) }}` references, output columns, and model layer (staging/intermediate/mart)

### Step 1.3: Map Source Components to dbt Models

Map pipeline components to dbt models using `{PLATFORM_DIR}/{transformation_guide}` for layer conventions. Determine for each model: expected output columns, transformations, filtering/routing logic, join conditions.

### Step 1.4: Present Summary

```
Test generation plan for <project_name>:
  Source dataflow: <dataflow_name>
  Source components found: N (K sources, L transforms, M destinations)
  dbt models to test: P
  Source tables to mock: Q

  Component -> Model mapping:
    OLE DB Source "<SourceTable>"       -> stg_raw__<source_name>
    <Transform> "<TransformName>"       -> int_<transform_name>
    Conditional Split "<SplitName>"     -> int_<split_name>_case_1, int_<split_name>_case_2
    OLE DB Destination "<DestTable>"    -> <destination_model>

  Proceed with test generation?
```

⚠️ **STOPPING POINT** (interactive mode): Ask user to confirm or adjust. Autonomous agents: skip — proceed with generated plan and document assumptions in the completion report.

## Phase 2: Arrange -- Generate dbt Seeds

For each source table identified in Phase 1, generate a CSV seed file.

### Step 2.1: Design Synthetic Rows

Use source component output columns (from source definition file) to define seed schema. See `{PLATFORM_DIR}/{transformation_guide}` for data type mapping. Design 3-5 rows per source table:

- At least one row matching every downstream transform condition; one that does NOT match
- Exhaustive NULL combinations for NULL-handling columns (all 2^K combos for K nullable columns)
- Edge cases where relevant (empty strings, boundary dates, zero values)
- **Variable-controlled branching (MANDATORY)**: for `{{ var(...) }}`-controlled routing, generate tests for at least two distinct variable values — separate test files per variable value, using `--vars '{"<var_name>": <alt_value>}'` at execution time

### Step 2.2: Write Seed CSV Files

Create seed files under `<UNIT>/stabilization/tests/dbt/<project_name>/seeds/`. Header: source column names exactly. Formatting: dates `YYYY-MM-DD`, timestamps `YYYY-MM-DD HH:MI:SS`, booleans `true`/`false`.

### Step 2.3: Configure Source Overrides

Create `<UNIT>/stabilization/tests/dbt/<project_name>/stabilization_test_sources.yml` to re-point source references to the seed tables:

```yaml
version: 2

sources:
  - name: <source_name>
    schema: "{{ target.schema }}"
    tables:
      - name: <table_name>
        identifier: <source_name>__<table_name>
```

**IMPORTANT**: Before generating the override, check the existing `sources.yml`: if it already uses `identifier: <source_name>__<table_name>` and `schema: "{{ target.schema }}"`, skip generating it. If the override IS needed, temporarily rename the original `sources.yml` to `sources.yml.bak` before deploying (restore during cleanup).

### Step 2.4: Generate dbt_project Patch

Create `<UNIT>/stabilization/tests/dbt/<project_name>/dbt_project_patch.yml`:

```yaml
seeds:
  <project_name>:
    stabilization_tests:
      +schema: "{{ target.schema }}"
      +tags: ["stabilization_test"]
```

### Step 2.5: Coverage Matrix

Before writing tests, produce a coverage matrix. Every model MUST appear — no skips without justification:
- Staging: row count + schema tests minimum
- Intermediate: row count + schema + singular tests per source transformation
- Mart: row count + schema minimum; add value assertion if mart applies any transformation

Present the matrix as part of the Phase 1 summary.

## Phase 3: Assert -- Generate dbt Tests

All test files go to `<UNIT>/stabilization/tests/dbt/<project_name>/tests/`. Generate tests for **every model** — staging, intermediate, AND mart.

### Step 3.1: Schema Tests

Create `<UNIT>/stabilization/tests/dbt/<project_name>/stabilization_test_schema.yml` with schema-level tests.

**All models (every layer):**
- `not_null` + `unique` on the primary key or identity column -- **mandatory**
- `not_null` on every non-key column that has no NULL values in the expected output

**Staging models additionally:**
- `accepted_values` on any column with fewer than 10 distinct values in the seed data

**Intermediate models additionally:**
- `not_null` with a `where` filter on columns produced by NULL-handling transforms
- `accepted_values` on output columns with known finite domains

**Mart models additionally:**
- `relationships` is **mandatory** when the mart references an upstream model via `ref()`
- `not_null` on all passthrough columns that are non-null in the upstream model

### Step 3.2: Singular Assertion Tests (AAA Pattern)

Create `.sql` test files under `<UNIT>/stabilization/tests/dbt/<project_name>/tests/`. Each test follows the AAA pattern with clearly labeled sections and dbt convention (returns rows that FAIL; 0 rows = pass).

**Template -- every singular test must follow this structure:**

```sql
-- tests/assert_<model_name>_<what_is_tested>.sql
{{ config(tags=["stabilization_test"]) }}

-- ARRANGE: describe the seed data setup for this test
-- ACT: describe the source transformation being tested
-- ASSERT: expected result and why (traced from source ETL logic)

SELECT *
FROM {{ ref('<model_name>') }}
WHERE <assertion_condition>
```

Generate the following test types as applicable:
- **Row count assertions**: verify expected row count after filtering/transforms
- **Value assertions**: verify derived column expression outputs
- **Conditional Split assertions**: verify row counts per split output
- **Join/Lookup assertions**: verify correct join behavior and row counts
- **NULL handling assertions**: verify COALESCE/NVL/CASE behavior on NULL inputs
- **Ranking/windowed query assertions**: verify correct best-match selection for Fuzzy Lookup patterns
- **Similarity/score range assertions**: verify scores are in valid range (mandatory for JAROWINKLER_SIMILARITY or similar)
- **Passthrough/identity model assertions**: verify staging/mart row counts match upstream

### Step 3.2a: Assertion Hardening Rules (MANDATORY)

These assertions are the fixer's convergence gate — `dbt-fixer` only accepts a node when they pass — so
they must be **impossible to break by accident**. An assertion whose own SQL errors is worse than a missing
assertion: it reads as a failed fix, and the fixer burns an attempt on a test bug instead of on the model.

Every generated assertion MUST obey all of the following:

1. **Reference only the model under test.** One `ref()`, to the target model. Do not join to upstream
   models, seeds or sources inside an assertion.
2. **Use only these shapes:**
   - a row count compared to a literal (`COUNT(*) <> 3`)
   - a single-group scalar compared to a literal
   - a flat `NOT EXISTS` / `WHERE` predicate returning offending rows
3. **No joins, no correlated subqueries, no nested cross-table subqueries, no window functions** inside
   the assertion.
4. **No bare scalar subqueries.** `(SELECT col FROM model WHERE key = 'x') = 'y'` ERRORS the moment a wrong
   fix produces duplicate rows for that key — precisely when you most need a clean failure. Express it as a
   predicate instead:
   ```sql
   -- Fragile: errors (not fails) if the model returns duplicates for PARTY_ID = '1'
   -- WHERE (SELECT PARTY_NAME FROM {{ ref('mart_parties') }} WHERE PARTY_ID = '1') <> 'Alice New'

   -- Robust: fails cleanly whether the row is wrong, missing or duplicated
   SELECT * FROM {{ ref('mart_parties') }}
   WHERE PARTY_ID = '1' AND PARTY_NAME <> 'Alice New'
   ```
5. **Expected values are literals derived by hand from the source definition.** Never recompute the
   expected value inside the assertion from the same model you are testing — that passes trivially. Never
   read it from the converted SQL; derive it from the source ETL logic.
6. **State the expected value in the ASSERT comment** so a reviewer can check the derivation without
   re-reading the source.

### Step 3.2b: Discriminating Case Rule (MANDATORY)

A test suite that only a correct fix can pass is the point; a suite that a *wrong* fix also passes is
worthless. So for **every model with real transformation logic** (filter, lookup/join, aggregation,
de-duplication, ranking, conditional split, NULL handling):

- Include at least one assertion that a **nameable plausible-but-wrong** implementation would FAIL.
- Name that wrong implementation in the ASSERT comment, with the wrong answer it produces.

Worked example — a de-duplication that must keep the most recent row per key:

```sql
-- ARRANGE: seed has two rows for PARTY_ID '1' (LOAD_TS 2024-01-01 'Alice Old', 2024-06-01 'Alice New')
-- ACT: source Rank transformation keeps the single most recent row per PARTY_ID by LOAD_TS DESC
-- ASSERT: PARTY_ID '1' survives exactly once, with PARTY_NAME 'Alice New'.
--   Catches: no de-duplication at all (both rows survive -> duplicate PARTY_ID),
--            and ordering ASC instead of DESC (keeps 'Alice Old').
SELECT PARTY_ID
FROM {{ ref('mart_parties') }}
WHERE PARTY_ID = '1'
GROUP BY PARTY_ID
HAVING COUNT(*) <> 1 OR MIN(PARTY_NAME) <> 'Alice New'
```

Models with no real logic (pure passthrough) still get the row-count and key assertions from Step 3.3, but
need no discriminating case.

Record in the test report's Coverage Gaps section any model where you could not construct a discriminating
assertion, and why — that is a known blind spot in the gate, and the fixer's "passed" verdict for that
model is correspondingly weaker.

### Step 3.3: Staging and Mart Model Tests

Staging/mart models still require: a row count assertion verifying output matches upstream, `not_null` + `unique` on the primary key, and a value assertion if the model applies any transformation.

### Step 3.4: One Test File Per Logical Case

Each distinct logical case MUST get its own test file. Do NOT consolidate — failures must immediately identify which case broke.

### Step 3.5: Comment Discipline

Every singular test MUST include AAA comment sections:
1. **ARRANGE**: Relevant seed rows and their values
2. **ACT**: Source component/transformation being tested and the dbt model implementing it
3. **ASSERT**: Expected output with step-by-step derivation traced from the source ETL logic

## Phase 4: Act -- Deploy and Execute Tests

### Step 4.1: Deploy Test Artifacts

Copy the generated files from stabilization into the dbt project:

```
<UNIT>/stabilization/tests/dbt/<project_name>/seeds/*    -> <DBT_PROJECT>/seeds/stabilization_tests/
<UNIT>/stabilization/tests/dbt/<project_name>/tests/*    -> <DBT_PROJECT>/tests/stabilization/
<UNIT>/stabilization/tests/dbt/<project_name>/stabilization_test_sources.yml -> <DBT_PROJECT>/models/stabilization_test_sources.yml
<UNIT>/stabilization/tests/dbt/<project_name>/stabilization_test_schema.yml -> <DBT_PROJECT>/models/stabilization_test_schema.yml
```

Apply the seed configuration from `dbt_project_patch.yml` to `<DBT_PROJECT>/dbt_project.yml`.

**Verify deployment**: After copying, confirm each file exists at its destination.

### Step 4.2: Seed the Test Data (Arrange)

```bash
dbt seed --select tag:stabilization_test --project-dir <DBT_PROJECT_PATH> --profiles-dir ~/.dbt
```

### Step 4.3: Build the Models (Act)

```bash
dbt run --select tag:stabilization_test --project-dir <DBT_PROJECT_PATH> --profiles-dir ~/.dbt
```

> **Location-override layer (SnowConvert `sc_override_*` vars):** Applies only when
> `dbt_project.yml` declares `sc_override_*` vars. When present, the marts materialize at those
> vars' placeholder defaults, so they won't build. As with variable-controlled branching (Step 2.1),
> override the `sc_override_*` vars at execution time via `--vars` so the marts build in the test
> environment.

### Step 4.4: Run the Tests (Assert)

```bash
dbt test --select tag:stabilization_test --project-dir <DBT_PROJECT_PATH> --profiles-dir ~/.dbt
```

### Step 4.5: Handle Failures

Since tests run BEFORE fixes are applied, some failures are expected. Categorize each failing test:

1. **Expected failure (model has known EWI/conversion gap)** -- record as baseline failure
2. **Test bug (incorrect expected value or seed data)** -- fix and re-run (up to 3 retries)
3. **Seed data bug (missing or wrong seed row)** -- fix seed CSV, re-seed, re-run

### Step 4.6: Update Status

Record per-node test results (test-passed / test-failed with reason) in your `test_report.md` Baseline Results table.

> **Do NOT call `track_status.py` directly.** The orchestrator reads your test report and updates `session_status.json` after all dbt-test-gen agents complete.

## Phase 5: Report

After all tests are executed:

1. Read `session_status.json` to check dbt project status.

2. Present the summary to the user:
   ```
   dbt test generation complete for <unit_name>:

   Project: <project_name>
     Source dataflow: <dataflow_name>
     Source components mapped: N
     Seeds generated: M
     Schema tests: K
     Singular assertion tests: L
     Tests passed (baseline): P
     Tests failed (expected -- model unfixed): F
     Tests failed (test bug -- fixed): B

   Baseline failures (to be resolved by dbt-fixer):
     - <test_name>: <failure reason> (maps to source component <name>)

   Test artifacts: <UNIT>/stabilization/tests/dbt/<project_name>/
   ```

3. Write detailed test report to `<UNIT>/stabilization/tests/dbt/<project_name>/test_report.md` including:
   - **Source-to-dbt Mapping**: component mapping from Phase 1
   - **Baseline Results**: per-test table with PASS/FAIL for every test
   - **Coverage Gaps**: honest assessment of what the test suite does and does not cover

4. **MANDATORY self-check before returning** -- verify all artifacts exist by checking each path:
   ```
   {UNIT}/stabilization/tests/dbt/{PROJECT_NAME}/seeds/       -- must contain at least 1 .csv file
   {UNIT}/stabilization/tests/dbt/{PROJECT_NAME}/tests/        -- must contain at least 1 .sql file
   {UNIT}/stabilization/tests/dbt/{PROJECT_NAME}/stabilization_test_schema.yml   -- must exist
   {UNIT}/stabilization/tests/dbt/{PROJECT_NAME}/stabilization_test_sources.yml  -- must exist
   {UNIT}/stabilization/tests/dbt/{PROJECT_NAME}/test_report.md              -- must exist
   ```
   If ANY file is missing, generate it before returning. Do NOT return to the parent skill until ALL artifacts exist. If you cannot write files due to sandbox restrictions, include the full file contents in your completion message so the orchestrator can write them.

5. Return to the parent skill (stabilization) for next steps.

## Troubleshooting

### `dbt seed` fails with column type mismatch
- Check seed CSV headers match the column names in `stabilization_test_sources.yml`
- Verify data types: dbt infers from CSV values — use consistent formats (dates as `YYYY-MM-DD`, numbers without commas)
- If a column should be `VARIANT` or `TIMESTAMP_NTZ`, add explicit column types in `stabilization_test_schema.yml`

### `dbt run` fails with "model not found" or `ref()` error
- Verify the model file exists in the dbt project and is not disabled
- Check that `ref()` targets match actual model filenames (case-sensitive)
- dbt resolves dependencies automatically — if a dependency fails, downstream models will also fail

### Singular test returns wrong result
- Verify seed data matches the source definition file (not the converted SQL)
- Trace expected values: source SQL definition → original query logic → expected output
- Check if the test is asserting against the unfixed model (expected baseline failure) vs a test bug

### All tests fail with "relation does not exist"
- Verify `dbt seed --full-refresh` ran before `dbt run`
- Check that `stabilization_test_sources.yml` points to the correct database/schema
- Verify Snowflake connection: `SELECT CURRENT_DATABASE(), CURRENT_SCHEMA()`

## Reference Files (loaded on-demand)

| File | When to load |
|------|-------------|
| `{PLATFORM_DIR}/{transformation_guide}` | Phase 1 — when reading the source transformations and mapping source components to dbt models |

---

## Task Mode (spawned by orchestrator)

### Input (provided by orchestrator at spawn time)

- Package name and path (`PACKAGE`)
- Phase number (`N`)
- dbt project path (`DBT_PROJECT_PATH`)
- Source definition file path: READ-ONLY — source of truth for ETL logic
- Source transformation guide path: platform's transformation reference
- Test environment: `DATABASE.SCHEMA`
- `ROADMAP.md` path — for identifying current phase and assigned dbt projects
- `session_status.json` path — for reading project/node status

### On-Demand References (read when needed)

- Source transformation guide: when reading source transformations
- Source definition file: when mapping source components to dbt models

### Output

- Seeds: `PACKAGE/stabilization/tests/dbt/<project_name>/seeds/`
- Singular tests: `PACKAGE/stabilization/tests/dbt/<project_name>/tests/`
- Schema test config: `stabilization_test_schema.yml`
- Source override config: `stabilization_test_sources.yml`
- Test report: `PACKAGE/stabilization/tests/dbt/<project_name>/test_report.md`

### Mandatory Test Scaffolding

This agent MUST produce test artifacts for every assigned dbt project, unconditionally. The workflow has two independent stages:

**Stage 1: Generate test files (ALWAYS possible)**
- Analyze the source definition file to understand dataflow transformations
- Generate seed CSVs from source component analysis
- Generate singular SQL test files from source transformation logic
- Generate schema test YAML from source column definitions
- Write all files to `{UNIT}/stabilization/tests/dbt/{PROJECT_NAME}/`

Stage 1 does NOT require dbt to compile. It reads the source definition file and writes test artifacts. This stage MUST complete for every project.

**Stage 2: Execute tests (may fail — that's expected)**
- Copy test artifacts into dbt project
- Run `dbt seed` → `dbt run` → `dbt test`
- If ANY step fails: record the failure in `test_report.md` as a baseline result and STOP execution (do not retry)
- If all steps pass: record baseline results per test

If a project cannot compile (broken config, bad macros, EWI markers), Stage 2 will fail. This is expected and normal — the test_report.md documents what failed and why, and the dbt-fixer uses this as input.

**Minimum artifact set (MANDATORY before returning):**
- `seeds/` — at least 1 .csv file
- `tests/` — at least 1 .sql file
- `test_report.md` — with bootstrap_status section and baseline results (even if all results are "execution failed")
- `stabilization_test_schema.yml`
- `stabilization_test_sources.yml`

Do NOT return to the orchestrator without these files. If you cannot generate meaningful seeds (e.g., no source definition file), generate minimal placeholder seeds with a single row and document the gap in test_report.md.

### Workflow

Follow the Main Mode workflow in full. Apply these behavioral overrides:
- Skip all interactive stopping points — proceed autonomously with reasonable defaults
- Document assumptions in the test report's Coverage Gaps section
- Process only the dbt project(s) assigned to the current phase in ROADMAP.md

### Context Management

If you feel context pressure after completing a model/node, **stop and report partial completion** — list which models have tests and which do not. Prefer stopping early over running to exhaustion.

### Team Protocol

When your work is complete:
1. Send a `send_message` to `main` summarizing: tests generated, baseline results, any coverage gaps
2. If you receive a `shutdown_request`, use `send_message` with `type: "shutdown_response"` and `approve: true`
