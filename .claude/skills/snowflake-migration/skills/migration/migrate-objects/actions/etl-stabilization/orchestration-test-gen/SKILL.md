---
name: orchestration-test-gen
parent_skill: etl-stabilization
description: "Generate AAA orchestration tests (isolated or grouped) for ETL-to-Snowflake elements. Scoped to elements assigned to the current phase in ROADMAP.md. Use when the stabilization skill invokes test generation for an orchestration phase."
license: Proprietary. See License-Skills for complete terms
---

# Orchestration Test Generator

Generate and run functional equivalence tests for orchestration SQL (task graphs and stored procedures) based on the original control flow logic in the source definition file. Tests are generated BEFORE fixes are applied, serving as an independent oracle derived from the source-of-truth (the source definition file). All generated test artifacts are stored in `<UNIT>/stabilization/tests/orchestration/`.

> **Autonomous mode:** When spawned as a team agent, skip all interactive stopping points, make reasonable defaults for user-facing decisions, and document assumptions in the completion report. When done, send a `send_message` to `main` summarizing your results, and respond to any `shutdown_request` with `send_message` using `type: "shutdown_response"` and `approve: true`.

## Main Mode (interactive / standalone use)

Tests follow the **Arrange-Act-Assert (AAA)** pattern with a two-phase Arrange:
- **Arrange:Setup**: Create all test objects (DDL) — `etl_configuration` infrastructure, mock dependency tables, schemas, ACT stored procedures. Run once per test file.
- **Arrange:Seed**: Populate all tables with test data — `TRUNCATE` + `INSERT` for control variables and synthetic rows. Run before every ACT/ASSERT cycle to reset data to a known state.
- **Act**: Extract the task body from the current (unfixed) orchestration SQL, wrap it for standalone execution, and run it against the test environment
- **Assert**: Run SQL queries that verify side effects (row counts, column values, variable state) match the expected behavior defined by the source control flow logic

### Input

This sub-skill expects:
- `session_status.json` — with `source_file_path` set, pending orchestration elements, and `migration_object_path`
- The orchestration `.sql` file path (from session status `orchestration_file` field)
- The source definition file path (from `source_file_path` in session status)
- `ROADMAP.md` — defines phases, element assignments, and test strategies (authored by stabilization)

### Prerequisites

- Python 3.11+ installed
- The source definition file must be accessible and readable
- Active Snowflake connection with a warehouse configured
- The `etl_configuration/` directory must exist at `<CONVERTED_OUTPUT>/ETL/etl_configuration/` (SnowConvert output root is typically the project `snowflake/` directory; legacy trees may use `Output/SnowConvert/ETL/etl_configuration/`)
- **Snowflake privileges**: `CREATE TABLE`, `CREATE FUNCTION`, and `CREATE PROCEDURE` on a user-provided database and schema

### Output Location

```
<UNIT>/stabilization/tests/orchestration/
  <schema>/                         # Snowflake schema tests create objects in (typically public)
    <short_element_name>.sql        # Isolated test (segment after last '.' in session_status name)
    grouped_<group_name>.sql        # Grouped test (shared ARRANGE for group)
    ...
  test_report.md                    # Report consumed by orchestration-fixer
```

The value of this skill is in the ARRANGE and ASSERT sections — they encode what the element needs (infrastructure, seed data) and what correct behavior looks like (functional equivalence checks from the source definition file). The ACT section is a snapshot of the current orchestration SQL (the baseline). It is updated by the orchestration-fixer during the fix-test loop.

### Test Lifecycle

```
This skill (orchestration-test-gen):
  ARRANGE:SETUP + ARRANGE:SEED + ASSERT written from source definition file (stable, written once)
  ACT extracted from unfixed orchestration SQL (baseline snapshot)
  Execute: ARRANGE:SETUP → ARRANGE:SEED → ACT → ASSERT
  ACT may fail (expected), ASSERT may fail (expected)
  Record baseline failures in test_report.md

Orchestration-fixer uses test file as workbench:
  Fixer modifies ACT in the test file with proposed fix
  First cycle: ARRANGE:SETUP → ARRANGE:SEED → ACT → ASSERT
  Subsequent cycles: ARRANGE:SEED → ACT → ASSERT (SEED resets data)
  If ASSERT fails → iterates (modifies ACT, re-runs SEED → ACT → ASSERT)
  If ASSERT passes → applies proven fix to orchestration SQL file
  Test file now contains the verified fix in its ACT section

Validation:
  Re-runs test file as-is (ARRANGE:SETUP → ARRANGE:SEED → ACT → ASSERT)

Final artifact:
  Test file with fixed ACT + source-derived assertions
  Users can re-run this file at any time to verify functional equivalence
```

### Workflow

Copy this checklist and track your progress:

```
Orchestration Test Gen Progress:
- [ ] Phase 1: Configure test environment + analyze source definition file and orchestration SQL (phase-scoped)
- [ ] Phase 2: Arrange — generate test infrastructure (isolated or grouped)
- [ ] Phase 3: Assert — generate test assertions
- [ ] Phase 4: Act — build complete test files and execute
- [ ] Phase 5: Report results and write test_report.md
```

### Phase 1: Configure Test Environment and Analyze

#### Step 1.0: Configure Test Environment

Check `session_status.json` for an existing `test_environment` key. If found, reuse the stored configuration (this happens during re-runs). If not found, detect the current connection details:

```sql
SELECT CURRENT_DATABASE(), CURRENT_SCHEMA(), CURRENT_ROLE(), CURRENT_WAREHOUSE();
```

Present them to the user:

```
Current connection details:
  Database:  <CURRENT_DATABASE>
  Schema:    <CURRENT_SCHEMA>
  Role:      <CURRENT_ROLE>
  Warehouse: <CURRENT_WAREHOUSE>

All test objects will be created with CREATE OR REPLACE in this database and schema.
Would you like to use this connection for test execution?
If not, provide an alternative: DATABASE_NAME.SCHEMA_NAME
```

⚠️ **STOPPING POINT** (interactive mode): Use `ask_user_question` to get the user's answer. If running as an autonomous team agent, skip — detect the current connection and proceed with it as the test environment.

Store the configuration via CLI:

```bash
uv run --project <SKILL_DIR> python <SKILL_DIR>/scripts/track_status.py set-test-env <SESSION_JSON> <DATABASE> <SCHEMA>
```

Verify access by running a simple probe:

```sql
USE DATABASE <database>;
USE SCHEMA <schema>;
SELECT 1;
```

If this fails, ask the user to correct the database/schema name.

#### Step 1.1: Scope to Current Phase

Read `ROADMAP.md` to identify the current phase number, then scope to the assigned elements:

Read `session_status.json` and filter elements where `phase == <phase_num>`. **Only generate tests for these elements.** Elements from other phases are ignored entirely in this invocation.

Skip test generation for elements that already have test files from a prior phase. Check for existing files at:
- Isolated: `<UNIT>/stabilization/tests/orchestration/<schema>/<short_element_name>.sql`
  (`<schema>` = the Snowflake schema the test objects are created in, typically `public`;
  `<short_element_name>` = the segment after the last `.` in the element's dotted
  `session_status.json` name — e.g. `s_m_last_run_date`, not the fully-qualified
  `f_Warehouse_presentation.wf_bs_facts_fl_to_pl.s_m_last_run_date`)
- Grouped: `<UNIT>/stabilization/tests/orchestration/<schema>/grouped_<group_name>.sql`

If a test file already exists, mark the element as `already-tested` and skip it.

#### Step 1.2: Read Source Materials

Read the source definition file (extract: package variables, executable hierarchy, precedence constraints, event handlers — see `{PLATFORM_DIR}/{orchestration_guide}` for paths and namespaces) and the orchestration SQL in a single pass:

1. Read `session_status.json` for the `elements` list and statuses; read `scan.json` for the `statements` array (each `CREATE TASK`/`CREATE PROCEDURE` and its child elements, delimited by `---- Start`/`---- End` tags)
2. Extract the root task `CONFIG` block — contains variable definitions needed by child tasks
3. Note database names in fully-qualified references (`DB.SCHEMA.TABLE`) — these need rewriting in ACT

Read both files ONCE. Build a mental index of element names → SQL bodies. Do NOT re-read per element during Phases 2-4.

#### Step 1.3: Map Source Elements to Orchestration Statements

Map source definition executables to orchestration SQL statements (phase-scoped only). Match by element name using the platform's element naming convention ↔ `---- Start` tags. Classify each element as testable or skip per [test-categorization.md](test-categorization.md). Mark disabled elements as `skipped:disabled-in-source`, Pipeline/dbt as `skipped:dbt-dependency`, and external deps as skip with documented coverage gaps.

#### Step 1.4: Present Summary

```
Test generation plan for <unit_name> — Phase <N>:
  Test environment: <DATABASE>.<SCHEMA>
  Phase elements: P (of T total), already tested: A, testable: X, skip: U
  Element → Statement mapping: (list each with source element type, statement, test strategy)
  Test strategy: I isolated test files, H grouped test files (G elements)
  Proceed with test generation?
```

⚠️ **STOPPING POINT** (interactive mode): Ask user to confirm or adjust. If running as an autonomous agent, skip — proceed with the generated plan and document assumptions in the completion report.

#### Batch Processing Strategy

Group phase elements by similarity before generating test files: (1) same EWI code + element type — generate one template, replicate for the rest; (2) same statement — read once, extract all element bodies in a single pass; (3) same test strategy (grouped) — already share a single test file. Process grouped tests first, then isolated tests grouped by EWI similarity.

### Phase 2: Arrange — Generate Test Infrastructure

For each testable element in the current phase, build the ARRANGE section. Check each element's `test_strategy` in `session_status.json`:
- For `isolated` elements, create one test file per element.
- For `grouped:<name>` elements, create one test file per group with a shared ARRANGE that sets up infrastructure for all elements in the group.

#### Step 2.1: Design Test Data from Source Definitions

Identify what mock objects and data are needed:

1. **From the source SQL definition** (per the platform's `sql_source_attribute`):
   - Parse T-SQL to identify referenced tables, columns, and operations
   - Categorize: **Read** (`FROM`/`JOIN`) → DDL + data; **Write** (`INSERT INTO`/`MERGE INTO`) → DDL only; **Truncate** → DDL; **Call** → stub procedure
   - Infer column names/types from T-SQL column lists, JOINs, WHEREs, CASTs

2. **From source variable definitions** (for script/variable-dependent elements):
   - Map each package variable to a `control_variables` row using the platform's data type codes
   - Identify read/write variables per element

3. **From assessment CSVs** (supplementary): `SqlObjects.csv`, `ObjectDependencies.csv`, `ObjectReferences.csv`

For each read-dependency table, design 3-5 synthetic rows:
- At least one row matching all downstream conditions, one that does NOT match
- NULL combinations for columns used in NULL-handling expressions (all 2^K combos for K nullable columns)
- Edge cases where relevant (empty strings, boundary dates, zero values)
- Variable-controlled branching: exercise at least two distinct branches

T-SQL to Snowflake type mapping: `INT`/`BIGINT` → `NUMBER`, `VARCHAR(N)`/`NVARCHAR(N)` → `VARCHAR(N)`, `DATETIME`/`DATETIME2` → `TIMESTAMP_NTZ`, `DATE` → `DATE`, `BIT` → `BOOLEAN`, `FLOAT`/`REAL` → `FLOAT`, `DECIMAL(P,S)` → `NUMBER(P,S)`.

#### Step 2.2: Write Test SQL Files — ARRANGE Section

**Isolated:** `<element_name>.sql` per element. **Grouped:** `grouped_<group_name>.sql` per group — shared ARRANGE:SETUP + ARRANGE:SEED, then sequential ACT and ASSERT blocks per element.

Start each file with a metadata header (TEST, PACKAGE, GENERATED, ELEMENT(S), TEST STRATEGY, TARGET STATEMENT, SOURCE ELEMENT(S), TEST ENVIRONMENT). Build in two ARRANGE sub-sections:

##### ARRANGE:SETUP — DDL objects (run once)

> **Infrastructure Pre-Created:** `control_variables` table, `GetControlVariableUDF`, `UpdateControlVariable`, and tagged helpers are pre-created by the orchestrator via `_infrastructure.sql`. **Do NOT regenerate these.** ARRANGE:SETUP = element-specific DDL only.

```sql
-- ============================================================
-- ARRANGE:SETUP
-- ============================================================
USE DATABASE <database>;
USE SCHEMA <schema>;
```

Use `CREATE OR REPLACE` on all objects.

- **S1.** Create schemas referenced by the code: `CREATE SCHEMA IF NOT EXISTS <database>.<schema_name>`. If user lacks CREATE SCHEMA, create mock tables in current schema and rewrite ACT references.
- **S2.** Mock dependency DDLs — minimal tables/procedures for all references. Infer columns from: source SQL definition (primary), converted SQL (secondary), assessment CSVs (supplementary).
- **S3.** Create ACT stored procedures — see [stored-procedure-wrapping.md](stored-procedure-wrapping.md). Each element: `test_act_<element_name>()`.
- For grouped tests: create mock objects for ALL elements in the group; deduplicate shared dependencies.
- For phases with 5+ isolated elements: see [infrastructure-dedup.md](infrastructure-dedup.md) for the shared `_infrastructure.sql` pattern.

##### ARRANGE:SEED — Data population (run before every ACT/ASSERT cycle)

```sql
-- ============================================================
-- ARRANGE:SEED
-- ============================================================
```

Use `TRUNCATE` + `INSERT INTO ... SELECT` for all tables (Snowflake disallows `TO_VARIANT()` in `VALUES`). This is the **data reset** — runs before every ACT/ASSERT cycle.

- **D1.** Populate `control_variables` from root task CONFIG. For procedure-based packages (`SSC-FDM-SSIS0005`), extract from the `DELETE + INSERT ... UNION ALL` block instead.
- **D2.** Synthetic data for read-dependency tables. Do NOT populate write-target tables — assertions verify what ACT writes. TRUNCATE write-target tables to clear stale data.

#### Step 2.3: Coverage Matrix

Map every testable element (in this phase) to planned tests before writing assertions:

```
Coverage Matrix for <unit_name> — Phase <N>:
  Statement                    | Source Element Type            | Test Strategy | Planned Tests
  public.execute_sql_insert    | Microsoft.ExecuteSQLTask       | isolated      | row_count, column_values, null_handling
  public.script_set_variable   | Microsoft.ScriptTask           | grouped:setup | variable_assignment
  public.dbt_data_flow         | Microsoft.Pipeline             | (skip)        | dbt-test-gen
```

Rules: every phase element must appear; ExecuteSQLTask → row count + column values; ScriptTask → variable assertions; ForEachLoop → cumulative effects; Pipeline/external → explicitly marked with skip reason.

### Phase 3: Assert — Generate Test Assertions

Define correct behavior from the original ETL logic in the source definition file — NOT the converted Snowflake SQL.

#### Step 3.1: Derive Assertions from Source Intent

Trace synthetic input rows through the source SQL definition (per platform's `sql_source_attribute`) T-SQL logic to predict expected outputs. Generate assertions verifying the Snowflake code produces equivalent results (valid both before and after fixes).

#### Step 3.2: Generate Assertion SQL

For detailed templates by element type, see [assertion-patterns.md](assertion-patterns.md). Key types:

- **Execute SQL Task (DML)**: row count, column value, NULL handling, TRUNCATE+INSERT
- **Script Task**: variable value, variable existence
- **ForEach Loop**: cumulative iteration effects (row counts after all iterations)
- **Conditional Execution**: branch verification via side-effect checks

**Assertion density:** One assertion per side effect. Each must have a **positive** check (expected state exists) AND a **negative** check (stale/pre-fix state does not remain). Assert exact row counts (`COUNT(*) = N`). See [assertion-patterns.md](assertion-patterns.md) for positive + negative pair templates.

Generate all assertions for a single element as a **batched UNION ALL query** (one `snowflake_sql_execute` call per element):

```sql
SELECT 'assert_01_{name}:' || CASE WHEN ({query}) THEN 'PASS' ELSE 'FAIL: ...' END AS result
UNION ALL
SELECT 'assert_02_{name}:' || CASE WHEN ({query}) THEN 'PASS' ELSE 'FAIL: ...' END
-- ... all assertions for this element
;
```

See `assertion-patterns.md` § Batched Assertion Format for templates.

For grouped tests, label each element's ASSERT block: `-- ASSERT: <element_name> (1 of N in group <group_name>)`. Each element gets numbered assertions (`assert_01_`, `assert_02_`, etc.) when it has multiple side effects.

**Strict assertion rule:** Encode ONLY expected correct behavior from the source definition file. Do NOT write dual-outcome assertions. Pre-fix failures are expected and recorded in `test_report.md`.

#### Step 3.3: Comment Discipline

Every assertion MUST include:
```sql
-- Assert: <what is being checked>
-- (Trace: <source element> → <transformation logic> → <expected result>)
```
Use the platform profile's `traceability_format` for the exact format.

### Phase 4: Act — Build Test Files and Execute

#### Step 4.1: Build Complete Test Files

Add the ACT section to each test file. Extract the element body from the current orchestration SQL and wrap as a stored procedure:
1. Locate target statement by name
2. Copy `LET` variable declarations, business logic, and `UpdateControlVariable` calls
3. Rewrite all database references to the test environment (`<database>.<schema>`)
4. Comment out `EXECUTE DBT PROJECT` statements
5. Wrap in `CREATE OR REPLACE PROCEDURE <database>.<schema>.test_act_<element_name>() ...` (see [stored-procedure-wrapping.md](stored-procedure-wrapping.md))
6. Execute via `CALL <database>.<schema>.test_act_<element_name>();`

For grouped tests, include one ACT block per element executed sequentially, then one ASSERT block per element. No explicit CLEANUP section — data reset is handled by re-running ARRANGE:SEED.

#### Step 4.2: Execute Test Files

Execute each test file section-by-section using the `snowflake_sql_execute` MCP tool. See [mcp-test-execution.md](mcp-test-execution.md) for the full execution protocol (section ordering, grouped file handling, infrastructure dedup).

**Execution protocol (one `snowflake_sql_execute` call per step):**
- **ARRANGE:SETUP** — one multi-statement call with element-specific DDL only (mock dependency tables, cross-schema references, stub procedures). Infrastructure is pre-created; do not re-execute it.
- **ARRANGE:SEED** — one multi-statement call (TRUNCATE + INSERT for all seeded tables)
- **ACT per element** — one call: `CREATE OR REPLACE PROCEDURE` + `CALL`
- **ASSERT per element** — one batched call (UNION ALL query returning all assertion results)

**For grouped test files** (`grouped_<group_name>.sql`): execute all ACT blocks in order, then all ASSERT blocks separately, attributing results per element.

#### Step 4.3: Handle Failures

Categorize each failure:
1. **Expected (code has EWI/gap)** → baseline failure for orchestration-fixer to resolve
2. **Test bug (wrong mock/assertion)** → fix in `stabilization/tests/orchestration/`, retry up to 3 times
3. **Infrastructure limitation** → document in coverage gaps

#### Step 4.4: Update Status

> **Do NOT call `track_status.py` directly.** The orchestrator reads your baseline artifact and updates `session_status.json` after all test-gen agents complete. Your artifact's Status column is the source of truth.

### Phase 5: Report

1. Read `session_status.json` to verify all phase elements have terminal statuses.
2. **Session cleanup** — test objects remain in the user-provided schema. The user is responsible for cleanup; tests can be re-run (ARRANGE:SETUP is idempotent, ARRANGE:SEED resets data).
3. Present summary:
   ```
   Orchestration test generation complete for <unit_name> — Phase <N>:
     Test environment: <DATABASE>.<SCHEMA>
     Phase elements: P
     Already tested (prior phase): A
     Elements tested: T
     Elements skipped: U (dbt-dependency: D, external: E, disabled: B)
     Isolated tests: I (P passed, Q failed baseline)
     Grouped tests: G files covering H elements
     Infrastructure failures: R
     Baseline failures (to be resolved by orchestration-fixer):
       - <element_name> [isolated]: <failure reason> (source element: <source_name>)
       - <group_name> [grouped]: <failure reason> (elements: <list>)
   ```

4. Write `<UNIT>/stabilization/tests/orchestration/test_report.md` with:
   - **Source-to-Orchestration Mapping**: element mapping from Phase 1
   - **Baseline Results**: pass/fail per element, test strategy (isolated/grouped), source definition per failure, ACT vs ASSERT failure classification
   - **Coverage Gaps**: elements with external deps, opaque ScriptTasks, File Enumerator loops, ARRANGE:SETUP failures

5. **MANDATORY self-check before returning** — verify that `{UNIT}/stabilization/tests/orchestration/<schema>/` contains at least 1 `.sql` test file and `test_report.md` exists. If ANY file is missing, generate it before returning. If you cannot write files, include full contents in your completion message so the orchestrator can write them.

6. Return to parent skill (stabilization/SKILL.md) for orchestration fixing.

### Reference Files (loaded on-demand)

These files are NOT loaded upfront. Read them only when their content is needed for the current step:

| File | When to load |
|------|-------------|
| `{PLATFORM_DIR}/{orchestration_guide}` | Phase 1 — when reading the source orchestration structure |
| [assertion-patterns.md](assertion-patterns.md) | Phase 3 — when generating ASSERT SQL |
| [stored-procedure-wrapping.md](stored-procedure-wrapping.md) | Phase 2/4 — when wrapping element logic in stored procedures |
| [test-categorization.md](test-categorization.md) | ROADMAP creation — when understanding isolated vs grouped strategy |
| [infrastructure-dedup.md](infrastructure-dedup.md) | Phase 2 — when phase has 5+ isolated elements |
| [mcp-test-execution.md](mcp-test-execution.md) | Phase 4 — when executing test files against Snowflake |

---

## Task Mode (spawned by orchestrator)

### Input (provided by orchestrator at spawn time)

- Package name and path (`PACKAGE`)
- Phase number (`N`) and batch ID (`{B}`, format: `B{P}.{M}`, e.g., `B1.1`)
- Task schema (`TASK_SCHEMA`) — pre-assigned, use for ALL created objects
- Database (`DATABASE`)
- Elements to process (`ELEMENT_LIST`) with archetype/clone annotations
- Test strategy (`STRATEGY`): `isolated` or `grouped:<name>`
- File paths:
  - Orch SQL: read element bodies by tag boundaries. Container elements use `---- Start block`/`---- End block` pairs. Non-container elements use `---- Start` with no closing tag (body ends at next tag). See `reference/orchestration-tags.md`. (READ-ONLY)
  - Source definition file: read only if context beyond on-demand references is needed (READ-ONLY)
  - Orchestration guide: platform's source structure reference
  - Platform directory: `PLATFORM_DIR/` (element-types.md, ewi/)
  - Phases directory: `PHASES_DIR/`
  - Skill directory: `SKILL_DIR`
- `ROADMAP.md` batch context section (provided in prompt)
- Execute ALL SQL via `snowflake_sql_execute` MCP tool — no Python connections

### On-Demand References (read when needed)

- Source definition file: read only if provided context is insufficient
- EWI guides: from `PLATFORM_DIR/ewi/` when encountering markers
- [assertion-patterns.md](assertion-patterns.md): when generating ASSERT SQL
- [stored-procedure-wrapping.md](stored-procedure-wrapping.md): when wrapping element logic
- [mcp-test-execution.md](mcp-test-execution.md): when executing test files

### Infrastructure Pre-Created

The following objects are ALREADY created in the batch schema by the orchestrator before this agent starts:

- `control_variables` table
- `GetControlVariableUDF` function
- `UpdateControlVariable` procedure
- All tagged helper objects

Do NOT include any of these in ARRANGE:SETUP. **SETUP = element-specific DDL only.**

### Output

- Test files: `PACKAGE/stabilization/tests/orchestration/<schema>/`
- Baseline report: `PHASES_DIR/baseline_batch_{B}.md`

Write artifacts **incrementally** — one element section appended at a time. The orchestrator handles partial artifacts: completed elements are already on disk and will not be re-processed on retry.

### Mandatory Test Generation

This agent MUST generate and execute test files for ALL assigned elements in the ELEMENT_LIST. Test generation cannot be skipped based on:
- Elements having proven patterns from prior phases
- Elements showing only informational EWI codes (e.g., SSC-FDM-0007)
- Elements being "clean SQL" with no code gaps
- Assumptions about prior-phase success

Every element MUST appear in the baseline report with a status (test-passed, test-failed, skipped with valid reason). Silent omission is a protocol violation.

### Valid Skip Reasons

Only these skip reasons are accepted by track_status.py:
- `disabled-in-source` — element is disabled in the source definition
- `container-only` — element is a structural container with no executable logic
- `file-io-noop` — element performs file I/O not applicable in Snowflake
- `dbt-dependency` — element is an EXECUTE DBT PROJECT invocation
- `external-dependency` — element has unfixable external dependencies

ScriptTasks with no Snowflake equivalent (filesystem I/O, COM objects) are NOT skipped. They are `test-failed` with a reason. The TDD loop must be attempted.

### Workflow

Process one element at a time in the order provided:

1. **Skip check** — look for the platform's `disabled_marker` in the source definition for this element, or check if the element body in the orch SQL is entirely commented-out with the disabled marker visible. If disabled:
   - Record status `skipped`, reason `disabled-in-source`
   - Skip to next element (no test needed).

2. **Generate test file**:
   - Use `TASK_SCHEMA` as the test schema (not DATABASE.PUBLIC or any other schema)
   - Use **batched assertion format** (UNION ALL) for all assertions
   - For **clone elements**: adapt the archetype element's test file with appropriate substitutions (schema, table names, parameters) rather than generating from scratch
   - Write test files to: `PACKAGE/stabilization/tests/orchestration/<schema>/`
   - Follow the Main Mode workflow for ARRANGE:SETUP, ARRANGE:SEED, ACT, and ASSERT generation — applying these overrides:
     - Do NOT call `set-test-env` — use `TASK_SCHEMA` directly
     - ARRANGE:SETUP contains ONLY element-specific DDL (infrastructure is pre-created)

3. **Run baseline** — execute in order: ARRANGE:SETUP → ARRANGE:SEED → ACT → ASSERT (batched)
   - Record pass/fail counts and any failure details

4. **Write test file to disk immediately** after baseline run — do not defer.

5. **Append this element's section to the baseline report immediately** — do not defer.

6. Proceed to next element.

#### Baseline report format: `PHASES_DIR/baseline_batch_{B}.md`

For the **first element processed**, write the file header:
```
# Baseline Report — Batch {B}, Phase {N}

## Summary

| Element | Test File | Baseline Result | Failure Details |
|---------|-----------|-----------------|-----------------|
```

For **subsequent elements**, append the next table row directly.

Use this format for each row:

| `element_name` | `test_file_path` | `passed` / `failed` / `skipped` | failure summary or — |

After the summary table, write an **Element Details** section with enriched context for downstream fix agents:

```
## Element Details

### element_name — PASSED|FAILED|SKIPPED

- **EWI Codes**: {codes from ROADMAP task section, e.g. SSC-EWI-SSIS0004}
- **Issue Summary**: {one-line description}
- **Source Excerpt** (from source definition):
  {relevant source definition excerpt for this element}
- **Failing Assertions**: {list of assert names that failed and their FAIL messages, or "—" if passed}
- **Applicable EWI Guide Section**: {e.g. "SSC-EWI-SSIS0004 § ScriptTask with DATEDIFF pattern", or "—" if no EWI}
```

This enriched baseline report enables fix agents to start fixing immediately without re-reading source files.

### Autonomous Behavior

- Do NOT ask the user any questions — make reasonable defaults and proceed autonomously
- On ambiguity (e.g. unclear clone substitutions, missing source element): make a best-effort decision, document the assumption in the baseline report's Failure Details column, and continue
- If an element is completely blocked (infrastructure failure, not a test failure): record `failed` with a descriptive reason in the baseline report and move on

### Context Management

After completing each element, assess your remaining context. If you have processed several elements and feel context pressure — large accumulated test outputs, many SQL results loaded into memory — **stop after the current element's artifacts are written** and report partial completion. The orchestrator will spawn a continuation agent for the remaining elements.

**Prefer stopping early with artifacts on disk over running to exhaustion with nothing written.**

When stopping early, send a completion message that includes:
- Elements completed (and their baseline results)
- Elements NOT processed (list them explicitly)
- Reason: `"partial-completion: context pressure after N elements"`

### Team Protocol

When your work is complete, your agent will automatically return results to the orchestrator.
If you receive a `shutdown_request`, use `send_message` with `type: "shutdown_response"` and `approve: true`.
