---
name: convert-sas-to-snowflake
parent_skill: sas
description: "Preview. Convert SAS code to Snowflake SQL and stored procedures. Use for: DATA steps, PROC SQL, macros, PROC steps, EGP projects (extracted .sas files only). Triggers: convert SAS, migrate SAS, SAS to Snowflake, translate SAS code, SAS migration, SAS analysis, SAS dependency diagram, validate SAS conversion. Note: For .egp files, extract the embedded .sas code first using SAS Enterprise Guide export."
license: Proprietary. See License-Skills for complete terms
---

# Convert SAS to Snowflake

> © Snowflake Inc. This skill and its contents are the proprietary intellectual property of Snowflake Inc.

Expert SAS to Snowflake migration - **ALWAYS outputs `.sql` by default**, with PySpark/SCOS as last resort.

**Output:** `.sql` by default (Tier 1 SQL + Tier 2 Stored Procedures). PySpark/SCOS notebook = LAST RESORT (HASH objects, CALL EXECUTE, statistical procs only). See SQL-First Classification below for full tier tables.

**Snowflake Interaction Policy:** ALL Snowflake operations (object creation, compilation, testing) require explicit user confirmation. See `workflows/steps-8-10-post-conversion.md` for confirmation patterns and testing mode selection.

**User Consent Propagation:** When a user confirms a high-level decision (validation scope, compilation approval), downstream sub-decisions that are direct consequences auto-resolve without re-prompting. See "Consent Propagation Rules" section below.

---

## Validation Prompt Policy (EXPLICIT — No Auto-Propagation)

Each validation phase requires its own explicit user confirmation. No phase auto-proceeds based on a prior selection. Snowflake operations ALWAYS show credit impact before executing.

| Phase | Prompt | Credits | Can Skip? |
|-------|--------|---------|-----------|
| Phase 1: Synthetic Data | Always runs (no prompt needed) | Zero | No |
| Phase 2: LLM Trace | "Run LLM trace?" | Zero | Yes |
| Phase 3: Snowflake Compilation | "Compile on Snowflake?" (with credit estimate) | Minimal | Yes |
| Phase 4: Snowflake Execution (Tier 2/3) | "Execute on Snowflake?" (with credit estimate) | Moderate | Yes |

**Hard Artifact Gates:** Each phase produces artifacts on disk. The NEXT phase CANNOT begin unless the prior phase's gate passes (artifacts verified to exist). State file updates without corresponding disk artifacts are INVALID.

| Phase | Required Artifacts |
|-------|-------------------|
| Phase 1 | `source_table_ddl.sql` + `synthetic_data.sql` |
| Phase 2 | `tests/<file>/expected/expected_<table>.csv` for each traced file |
| Phase 3 | `compilation_results.json` with per-file pass/fail |
| Phase 4 | `snowflake_execution_results.json` |

**Consent propagation is ONLY retained for:**
- Fix-and-retry loop within Phase 3 (auto-retry compilation fixes without re-prompting)
- Auto-drop of temporary compilation environment after Phase 3 completes
- These are sub-operations WITHIN a phase the user already approved

**No batch-mode amplifier.** Batch mode (10+ files) follows the same prompt rules as interactive mode.

---

## Intent Detection

```
Start
  ↓
Analyze User Request
  ↓
  ├─→ Convert intent → Follow Conversion Workflow (below)
  │     (convert, migrate, translate, transform)
  │
  ├─→ Assess intent → Load ../assess-sas-migration/SKILL.md
  │     (assess, analyze, size, estimate, complexity, volume, LOE, readiness, heatmap)
  │
  └─→ Validate intent → Load validate-sas-conversion/SKILL.md
        (validate, verify, test conversion, check migration)
```

---

## When to Use

- Convert SAS DATA steps to Snowflake SQL or stored procedures
- Translate PROC SQL to Snowflake SQL
- Migrate SAS macros to Snowflake scripting
- Convert PROC steps (SORT, MEANS, FREQ, TRANSPOSE, etc.)
- Validate converted code against test data

## Prerequisites

- Active Snowflake connection (for validation)
- Target schema exists (or user confirms schema)

---

## SQL-First Classification

### TIER 1: Pure SQL (Default - ALWAYS Try First)

**Use SQL for:**

| SAS Pattern | Snowflake SQL |
|-------------|---------------|
| PROC SQL | Direct SQL (strip PROC SQL/QUIT) |
| PROC SORT | `ORDER BY` or `QUALIFY ROW_NUMBER()` for NODUPKEY |
| Simple DATA step (SET, WHERE, IF≤3) | `CREATE TABLE AS SELECT` |
| PROC FREQ | `GROUP BY` with `COUNT(*)` |
| PROC MEANS (no OUTPUT) | Aggregate functions (AVG, SUM, etc.) |
| MERGE with simple BY | `JOIN` |
| FIRST./LAST. flags | Window functions: `ROW_NUMBER()`, `LEAD/LAG` |
| RETAIN (running totals) | `SUM() OVER (ROWS UNBOUNDED PRECEDING)` |
| Simple ARRAY (same operation) | `GREATEST()`, `LEAST()`, `COALESCE()` |

### TIER 2: Stored Procedures (When Pure SQL Insufficient)

**Use Snowflake Scripting when:**

| Pattern | Detection | Why Stored Procedure |
|---------|-----------|---------------------|
| RETAIN with conditional reset | `retain` + `if first.` + reset logic | State management across rows |
| FIRST./LAST. with complex calc | `first.` + accumulator + `last.` output | Multi-step BY-group logic |
| Multiple OUTPUT datasets | `output table1; output table2;` | Conditional routing |
| >5 IF/WHEN branches in a DATA step | DATA-step SELECT/WHEN or IF/THEN (not PROC SQL CASE WHEN) | Complex business logic |
| Row-by-row state changes | Previous row affects current | Cursor-like processing |
| Iterative calculations | Values build on prior iterations | Sequential dependency |

**Stored Procedure Pattern:**
```sql
CREATE OR REPLACE PROCEDURE process_sas_logic(p_input STRING, p_output STRING)
RETURNS STRING
LANGUAGE SQL
AS
$$
DECLARE
  v_row_count INTEGER;
BEGIN
  -- Use CTEs and window functions where possible
  CREATE OR REPLACE TABLE IDENTIFIER(:p_output) AS
  WITH ranked AS (
    SELECT *,
      ROW_NUMBER() OVER (PARTITION BY group_col ORDER BY sort_col) AS rn,
      SUM(amount) OVER (PARTITION BY group_col ORDER BY sort_col 
                        ROWS UNBOUNDED PRECEDING) AS running_total
    FROM IDENTIFIER(:p_input)
  )
  SELECT * FROM ranked WHERE some_condition;
  
  SELECT COUNT(*) INTO :v_row_count FROM IDENTIFIER(:p_output);
  RETURN 'Processed ' || v_row_count || ' rows';
END;
$$;
```

### TIER 3: PySpark via SCOS (LAST RESORT ONLY)

**Use PySpark with Snowpark Connect (SCOS) ONLY when SQL/Stored Procedures CANNOT work:**

| Pattern | Detection | Why PySpark Required |
|---------|-----------|---------------------|
| HASH objects | `declare hash` | In-memory key-value lookups |
| CALL EXECUTE | `call execute` | Dynamic code generation at runtime |
| DO UNTIL/WHILE + external | `do until` + `symput`/`call` | True iteration with external state |
| External file I/O | `infile`/`file` non-Snowflake | Reading/writing local files |
| Complex SYMPUT chains | Multiple `call symput` with dependencies | Cross-step variable passing |
| PROC REG/GLM/LOGISTIC/CLUSTER/FACTOR/PHREG/LIFETEST/SURVEYSELECT/MIXED/GENMOD/NLMIXED | Statistical modeling | Regression/ML models |

**⚠️ These are SQL, NOT PySpark:**
- ARRAY iteration → CASE expressions
- RETAIN → window functions
- FIRST./LAST. → ROW_NUMBER()
- KEY= lookup → LEFT JOIN
- %DO loops → GENERATOR

See `references/pyspark-fallback.md` for full SCOS notebook setup template and patterns.

**Before using PySpark, ask:** "Can this be done with window functions, CTEs, or a stored procedure?"

---

## Critical Conversion Rules

**Load `references/conversion-rules.md` at Steps 5-6** (code generation and self-check). Contains the rules governing semantic correctness.

**Key rules summary (always in context):**
- NEVER generate converter scripts — LLM reads and converts directly
- NEVER truncate or use "similar pattern" shortcuts
- SAS missing (.) = NULL with different comparison semantics
- MERGE != JOIN (many-to-many risk, IN= flags, source precedence)
- WORK tables = TEMPORARY, bare name, no schema prefix
- Snowflake Scripting: `:var` only in SQL statements, SELECT INTO, named exceptions only
- Migrated-source type traps: cast join keys to a common type, `TRY_TO_DOUBLE` VARCHAR measures, `TO_DATE()` VARCHAR date columns
- Validation anti-joins must use master reference tables (never derived/subset)
- Output column count must match SAS; never silently drop columns
- Consolidation must preserve all output tables

**Known conflict — NOT adopted (pending verification):** An external ruleset claims `$VAR` session-variable syntax *fails* inside stored procedures and that `GETVARIABLE()` is mandatory. This is **not** adopted here — the verified guidance in `references/common-patterns.md` (Platform Constraints) is that `$VAR` **works** inside an `EXECUTE AS CALLER` procedure body, with `GETVARIABLE('VAR')` as an equivalent alternative. `GETVARIABLE()` is genuinely *required* only when the variable name is **computed at runtime** (you can write `GETVARIABLE('VAR' || i)` but never `$VAR || i`). Do not switch to mandatory `GETVARIABLE()` for the static case unless re-verified empirically on Snowflake.

---

## Batch Mode (10+ Files)

When 10+ files detected, load `references/batch-mode.md` for batch-specific rules,
context window recovery, and Step 8a compilation with stub tables.

---

## Context Budget Management

The LLM should minimize context usage by:
1. **Only load references relevant to the current step** — never pre-load all references at Step 2
2. **Do NOT re-read completed files** — use `conversion_state.json` to skip already-converted files
3. **Write state to disk before each step transition** — enables resume without context replay
4. **For batch mode, process in groups of 10-20 files** — write .sql to disk between groups
5. **When context exceeds 60% consumed:** finish current file, write state, inform user
6. **On resume:** read ONLY `conversion_state.json` + the reference files needed for the current step

**Step-to-reference mapping (load ONLY these at each step):**

| Step | Required References |
|------|-------------------|
| 1-2 | `common-patterns.md` only |
| 1 (state init) | `state-tracker-schema.md` + `checkpoint-logging.md` (load once; lightweight, governs all checkpoint writes) |
| 2.5 | `vendor-passthrough.md` (only if external LIBNAME/CONNECT TO detected) |
| 3-4 | `classification-logic.md` (if needed) |
| 5 | `conversion-rules.md` + construct-specific refs (data-steps, proc-sql, etc.); `multi-block-orchestration.md` if program has 3+ dependent blocks / macro `%DO` loops / `&&var&i` / `&SYSERR` / `FILEEXIST` / trigger-file gates |
| 6 | `conversion-rules.md` (for self-check items) |
| 7 | `steps-7-validation.md` + `schema-inference.md` + `synthetic-data-rules.md` |
| 8 | `steps-8-10-post-conversion.md` + `batch-mode.md` (if batch) |
| 9 | `steps-8-10-post-conversion.md` + `comparison-rules.md` |
| 10 | `steps-8-10-post-conversion.md` + `templates/conversion-report.md` |

**Unload after use:** After completing a step, the reference files loaded for that step can be considered "consumed" — their content is materialized in the output artifacts. Do not re-read them unless the step needs to be re-executed.

---

## Conversion State Tracker (`conversion_state.json`)

A persistent JSON file written incrementally throughout the workflow to track per-file progress. Enables resume from ANY step across context windows. See `references/state-tracker-schema.md` for the full JSON schema, enforcement rules, and valid `current_step` values.

**Location:** `<output_dir>/conversion_state.json`

**Key fields:** `metadata.current_step`, `files.<name>.status`, `gates.*`, `trace_progress`, `execution_progress`, `compilation_env`

**Resume behavior (Step 1 pre-check):** If `conversion_state.json` exists, read it and offer Resume/Restart.

**File status progression:** `classified → converted → self_checked → compiled → validated → complete`

**Enforcement rule:** State writes are BLOCKING PREREQUISITES for step transitions. The NEXT step CANNOT begin until the state file reflects the current step's completion. Context pressure does NOT exempt state writes.

---

## Conversion Workflow

### Step 1: Gather Input

**Pre-check:** If `<output_dir>/conversion_state.json` exists, a prior session has in-progress conversion. Read the state file and offer:
- **Resume** from `current_step` (skip completed files/steps)
- **Restart fresh** (delete state file, begin from scratch)

**Ask user:**
1. SAS code source (file path, directory, or paste)
2. Target schema (e.g., `DATABASE.SCHEMA`)
3. Migration mode:
   - **1:1 Direct** (default) — Each SAS file converts to one .sql file. PySpark notebook generated ONLY for true Tier 3 edge cases (HASH objects, CALL EXECUTE, statistical procs).
   - **Optimize & Consolidate** — Merges related SAS files into fewer .sql files where dependencies allow. Same SQL-first tiering applies.

**⚠️ STOP**: Confirm understanding of SAS code.

**MANDATORY STATE WRITE (Step 1 → Step 2 transition):** Immediately after gathering input, write `conversion_state.json` with initial metadata:
```json
{
  "metadata": {
    "output_dir": "<path>",
    "target_schema": "<DATABASE.SCHEMA>",
    "migration_mode": "<1:1 or consolidate>",
    "created_at": "<ISO timestamp>",
    "last_updated": "<ISO timestamp>",
    "current_step": "1",
    "total_files": 0,
    "validation_scope": "pending_selection",
    "pre_approved_compilation": false,
    "pre_approved_validation": null
  }
}
```
This ensures metadata survives context loss between Steps 1 and 3. Step 2 CANNOT begin until this write is confirmed on disk.

**MANDATORY CHECKPOINT (every transition):** Alongside each `conversion_state.json` write throughout the workflow, append one line to `<output_dir>/checkpoint_log.jsonl` (create it here at Step 1 with the first `STARTED` line). This append-only audit trail records what happened and when — see `references/checkpoint-logging.md` for the schema and the per-checkpoint list. Appending the checkpoint line is a BLOCKING prerequisite to advancing, exactly like the state write.

### Step 2: Load References

**Always load:** `references/common-patterns.md` (Variable Binding Rules)

**Deferred load** (do NOT load at Step 2 — loaded when needed):
- `workflows/validation-pipeline.md` → loaded after Step 6a (single validation orchestrator)
- `workflows/steps-8-10-post-conversion.md` → loaded at Step 10 only (report generation)
- `templates/conversion-report.md` → loaded at Step 10
- `references/schema-inference.md` → loaded at Phase 1 (synthetic data gen)
- `references/synthetic-data-rules.md` → loaded at Phase 1
- `references/validation-execution.md` → loaded at Phase 2 (LLM trace)
- `references/snowflake-compile.md` → loaded at Phase 3 (Snowflake compilation)
- `references/snowflake-execution.md` → loaded at Phase 4 (Snowflake Tier 2/3 execution)
- `references/state-tracker-schema.md` → loaded on resume or when first writing state
- `references/checkpoint-logging.md` → loaded once at Step 1 (governs append-only `checkpoint_log.jsonl` written at every checkpoint)
- `references/batch-mode.md` → loaded only when 10+ files detected
- `references/classification-logic.md` → loaded at Step 3 if detailed pseudocode needed
- `references/comparison-rules.md` → loaded at Phase 4 (result comparison)
- `references/auto-validation.md` → loaded at Phase 2 (pipeline orchestration)
- `references/e2e-orchestration-test.md` → loaded only when Phase 5 (Integration & E2E) runs
- `references/consolidation-patterns.md` → loaded only in Optimize & Consolidate mode
- `references/multi-block-orchestration.md` → loaded at Step 5 only for multi-block programs (3+ dependent blocks, macro `%DO` loops, `&&var&i` indexed vars, `&SYSERR` gating, `FILEEXIST`/trigger-file gates)
- `references/pyspark-fallback.md` → loaded only when Tier 3 blocks detected
- `references/mermaid-diagrams.md` → loaded only at Step 10 (DAG generation)

**Then load based on constructs (Step 5 only):**

| Construct | Reference |
|-----------|-----------|
| DATA steps | `references/data-steps.md` |
| PROC SQL | `references/proc-sql.md` |
| Macros | `references/macros.md` |
| Multi-block programs / macro `%DO` loops / cross-block state (`&&var&i`, `&SYSERR`, `FILEEXIST`, trigger-file gates) | `references/multi-block-orchestration.md` |
| PROC steps | `references/proc-steps.md` |
| Function mappings | `references/function-mappings.md` |
| Oracle/DB2/SQL Server passthrough | `references/vendor-passthrough.md` + `references/vendor-function-mappings.md` |
| Large files (>500 lines) | `references/large-file-rules.md` |

### Step 2.5: External Source Resolution

**Scan SAS code for external database references:**
1. `LIBNAME` statements with engine keywords: `sqlsvr`, `oracle`, `teradata`, `odbc`, `oledb`, `postgres`, `mysql`, `mssql`
2. `PROC SQL CONNECT TO` statements: `connect to sqlsvr`, `connect to oracle`, etc.
3. Any `DSN=`, `authdomain=`, `qualifier=`, `schema=` parameters

**For each external reference found, extract:**
- Engine type (sqlsvr, oracle, etc.)
- DSN / qualifier (maps to source database name)
- Schema (maps to source schema name)
- Tables referenced via this LIBNAME (scan for `LIBNAME.table` patterns)

**Prompt user ONCE with all external sources:**
```
External data sources detected in SAS code:
| LIBNAME | Engine | DSN/Qualifier | Schema | Tables Referenced |
|---------|--------|---------------|--------|-------------------|
| EUDB    | sqlsvr | EUDB          | dbo    | Table1, Table2    |

These tables are sourced from an EXTERNAL database (not Snowflake).
They will eventually be migrated to Snowflake.

Please provide the target Snowflake location for these tables:
a) Use target schema already specified: {TARGET_SCHEMA}
b) Provide a different DATABASE.SCHEMA for these external tables: ___
c) Use placeholder names: {PLACEHOLDER_DB}.{PLACEHOLDER_SCHEMA}.{table}
```

**Store mapping in `conversion_state.json` under `source_mappings`** (see state-tracker-schema.md).

**During Step 5 (Generation):** Use the mapping to resolve external table references. If LIBNAME `EUDB` with `qualifier=ChargemasterEnforcement_Prod schema=dbo` references `dbo.MyTable`, convert to the user-provided `TARGET_DB.TARGET_SCHEMA.MYTABLE`.

**If NO external sources detected:** Skip this step silently. No prompt needed.

### Step 3: Classify Each Block (with Dependency Tracking)

**Assessment Auto-Discovery (no prompt):** A prior `/assess-sas-migration` run may have produced an
`assessment.json`. Search these candidate locations **in order** and use the FIRST readable match
(if several match, pick the one with the most recent modification time):

1. `<output_dir>/assessment.json`
2. `<source_dir>/assessment.json`
3. `<source_dir>/assessment_output/assessment.json` (the assess CLI's default `--output ./assessment_output`)
4. `<output_dir>/../assessment_output/assessment.json`
5. a shallow glob (depth ≤ 2) for `assessment.json` under `<source_dir>` and `<output_dir>`

A match is valid only if it parses as JSON and contains `metadata.generated_at` and a `files[]`
array; otherwise treat it as not found (record `reason: "unreadable"`).

- **If found:** seed per-file `primary_tier` / `tier_distribution` and the dependency graph from it
  to skip re-scanning. Note which path was used. If `metadata.generated_at` is older than the newest
  source-file modification time, set `stale: true` (still consume — the reconciliation below will
  surface any drift).
- **If NONE found:** proceed silently with fresh classification. **Do NOT prompt** for an assessment
  file. Record `assessment.consumed: false, reason: "not_found"` in state.

Record the outcome in `conversion_state.json` under `assessment` (see `references/state-tracker-schema.md`).

**Still verify the dependency map is current** — source files may have changed since assessment.

**CRITICAL: Before classifying, build a dependency map:**
1. Track which tables/datasets each block CREATES (output tables)
2. Track which tables/datasets each block READS (input tables)
3. Track macro variables set (CALL SYMPUT, %LET, INTO :var) and where they are consumed
4. Identify inter-block dependencies: if block N creates table X and block M reads table X, note the dependency
5. For repeated macro invocations: track parameter combinations separately — do NOT assume same behavior

**Input Table Existence Check (optional, requires active Snowflake connection):**

After building the dependency map, identify all TRUE external inputs — tables that appear in READ lists but are NOT created by any block in this conversion:
1. Collect unique source tables from all blocks' READ lists
2. Subtract tables that appear in any block's CREATES list (these are intermediate/temp tables)
3. The remainder = true external inputs that must pre-exist in Snowflake
4. If a Snowflake connection is active, verify these tables exist: `SHOW TABLES LIKE '<name>' IN SCHEMA <target_schema>`
5. If tables are NOT found, prompt user ONCE:
   ```
   These source tables are referenced but not found in {TARGET_SCHEMA}:
   - TABLE_A (used in blocks 1, 3)
   - TABLE_B (used in block 2)
   
   Options:
   a) Provide the correct DATABASE.SCHEMA for these tables
   b) They will be created before this script runs (proceed with current names)
   c) They were already mapped in Step 2.5 (use those mappings)
   d) Skip check (proceed as-is, may fail at compilation)
   ```
6. Store any user-provided mappings in `conversion_state.json` under `source_mappings`

**If no Snowflake connection available:** Skip silently. Compilation (Phase 4) will surface missing tables later.

**For EACH block, apply SQL-First classification using the quick-reference table below.** For detailed classification pseudocode and confidence assessment logic, load `references/classification-logic.md`.

**Block counting (must match the assessment CLI):** Follow the canonical
`../references/block-tiering-spec.md`. Enumerate **each DATA/PROC step inside a macro** as its
own block, and **exclude DI Studio / DataFlow boilerplate** (macros named `etls_*`, `rcset`,
`rcsetds`; content markers `etls_`, `perfinit`, `log4sas`, `armsubsys`, `sas data integration
studio`) from both the block count and tiering. This keeps the conversion's block count and
per-file tier identical to what `/assess-sas-migration` reports.

**Quick Classification:**

| SAS Pattern | Tier | Snowflake Approach |
|-------------|------|--------------------|
| `declare hash` | 3-SCOS | No SQL equivalent |
| `call execute` | 3-SCOS | Dynamic code generation |
| `do until/while` + `symput` + external state | 3-SCOS | Iteration with external state |
| `proc reg/glm/logistic/cluster/factor/phreg/lifetest/surveyselect/mixed/genmod/nlmixed` | 3-SCOS | Statistical modeling |
| `retain` + `first.` + reset | 2-SP | State management across rows |
| `first./last.` + multiple `output` | 2-SP | Multi-step BY-group logic |
| Multiple `output` destinations | 2-SP | Conditional routing |
| >5 `if`/`when` branches in a DATA step (not PROC SQL CASE WHEN) | 2-SP | Complex business logic |
| 3+ sequential dependent DML (DELETE→INSERT→UPDATE) | 2-SP | Orchestration + error handling |
| Everything else (PROC SQL, SORT, simple DATA step, MERGE, ARRAY, RETAIN running total, %DO loops) | 1-SQL | Window functions, CTEs, GENERATOR |

**Confidence:** LOW = nested macros, %INCLUDE with dynamic path, external LIBNAME. MEDIUM = INTCK/INTNX, NOTSORTED. HIGH = everything else.

**Assessment Reconciliation (only if `assessment.json` was consumed):** After computing this
conversion's own per-file block count and tier, compare them against the assessment as a baseline.
Both skills follow the same canonical `../references/block-tiering-spec.md`, so a current assessment
should match; a mismatch signals a stale assessment (source changed since it ran) or a bug — it is
**informational and does NOT block** conversion.

For each file present in BOTH this conversion's scope and the assessment, compare:
- `blocks` (countable block count)
- `primary_tier`
- `tier_distribution` (T1 / T2 / T3 counts)

Also note coverage deltas: files in the assessment but not in this conversion's scope, and vice versa.
Record the result in `conversion_state.json` under `assessment.reconciliation` (files_compared,
files_matched, files_mismatched, and a `mismatches` list of `{file, field, assessment, convert}`).
Present the summary in Step 4.

**PREREQUISITE FOR STEP 4:** Write `conversion_state.json` with initial entries for all files (`status: "classified"`, tier, block count). Set `current_step: "3"`. Also persist the dependency map per file: `"dependencies": {"creates": [...], "reads": [...]}`, and the `assessment` object (discovery outcome + reconciliation, or `consumed: false`). Verify the file exists on disk before presenting block analysis. Step 4 CANNOT begin until this write is confirmed.

### Step 4: Present Block Analysis

```markdown
## Block Analysis: script_name.sas

| Block | Type | Tier | Lines | Creates | Reads | Reason |
|-------|------|------|-------|---------|-------|--------|
| 1 | PROC SQL | 🔷 SQL | 10-25 | staging_data | source_table | Direct SQL mapping |
| 2 | DATA step | 🔷 SQL | 27-45 | summary | staging_data | Window functions |
| 3 | DATA step | 🔶 Stored Proc | 47-80 | flagged | summary | RETAIN + FIRST./LAST. |
| 4 | DATA step | 🔴 PySpark | 82-95 | lookup | ext_file | HASH object |

**Dependencies:** Block 2 depends on Block 1 (staging_data). Block 3 depends on Block 2 (summary).
**Output:** script_name.sql (all blocks as SQL/SP, block 4 commented if truly needs Python)
```

**Assessment reconciliation (only when `assessment.json` was consumed in Step 3):** Present a
compact comparison so drift from the assessment baseline is visible. Omit this section entirely
when no assessment was consumed.

```markdown
## Assessment Reconciliation  (baseline: <assessment source_path>, generated <generated_at>)

| File | Assessment (blocks / tier) | Conversion (blocks / tier) | Match? |
|------|----------------------------|----------------------------|--------|
| a.sas | 22 / TIER_1_SQL | 22 / TIER_1_SQL | ✅ |
| b.sas | 22 / TIER_2_SP  | 20 / TIER_1_SQL | ⚠️ blocks, tier |

**Summary:** 8 matched, 1 mismatched. (⚠️ assessment is STALE — generated before the latest
source edit; re-run `/assess-sas-migration` to refresh.)  [show the stale note only if `stale: true`]
Coverage: 0 files in assessment but not in this conversion; 0 the other way.
```

Mismatches are informational (source may legitimately have changed) and do not block conversion.

**⚠️ STOP**: Review classification. If user disagrees with PySpark assignment, attempt SQL/Stored Proc alternative.

**Permission Check (when Tier 2 blocks exist):**

If any blocks are classified as Tier 2 (Stored Procedure), prompt:
```
Some blocks require stored procedures (CREATE PROCEDURE).
Does your Snowflake role have CREATE PROCEDURE privilege on the target schema?
- Yes → proceed with stored procedure generation
- No → fall back to PySpark/SCOS notebook for these blocks (preserves logic fidelity)
- Unsure → proceed with stored procedures; compilation (Phase 4) will catch permission errors
```

**If user selects "No":**
- Reclassify affected blocks from Tier 2 to Tier 3 (PySpark/SCOS notebook)
- Generate a `.ipynb` notebook for those blocks using the SCOS template from `references/pyspark-fallback.md`
- Tier 1 (SQL) blocks remain as `.sql` output
- Update `conversion_state.json`: set `metadata.sp_permission: false`

**If user selects "Unsure":**
- Proceed with Tier 2 stored procedures as normal
- Phase 4 (Snowflake Compilation) will surface permission errors
- At that point, offer the same PySpark/SCOS fallback

**STATE WRITE on reclassification:** If the user reclassifies a file's tier (e.g., Tier 3 → Tier 2), update `conversion_state.json` immediately with the revised tier before proceeding to Step 5.

### Step 5: Generate Conversion

**For TIER 1 (SQL) blocks:**
- Use `references/function-mappings.md`
- Generate clean SQL with CREATE OR REPLACE TABLE
- Use explicit column lists (not SELECT *) when ROW_NUMBER() helpers are used
- WORK datasets → CREATE OR REPLACE TEMPORARY TABLE (no schema prefix)

**For TIER 2 (Stored Procedure) blocks:**
- Follow Variable Binding Rules from `references/common-patterns.md`
- Use CTEs and window functions inside the procedure
- Include proper EXCEPTION handling (named exceptions ONLY)
- Use SELECT INTO :var (NEVER LET := SELECT)
- Persist cross-block variables via EXECUTE IMMEDIATE SET

**For TIER 3 (PySpark/SCOS) blocks:**
- ONLY for HASH objects, CALL EXECUTE, DO UNTIL with external state, or PROC REG/GLM
- Use Snowpark Connect (SCOS) template from TIER 3 section
- Generate .ipynb notebook with SCOS setup cell
- Keep PySpark scope minimal - only the blocks that truly need it

**Generation Rules:**
- Convert EVERY column derivation — no "similar pattern" shortcuts
- Convert EVERY branch in conditional logic — no skipped branches
- Preserve the exact output table count from the SAS block
- Preserve all CALL SYMPUT/SYMPUTX assignments
- For PROC FORMAT: use CASE expressions for simple value mappings, lookup tables for complex ranges
- For Oracle/DB2 passthrough (CONNECT USING): strip vendor wrappers, convert vendor-specific functions (DECODE→COALESCE, NVL→COALESCE, TO_DATE format strings) to Snowflake native SQL
- For %INCLUDE without source: generate CALL to stored procedure stub with MANUAL_REVIEW_REQUIRED
- For external macros without source: generate parameterized stub comment with inferred behavior
- **NEVER** delegate conversion to a subagent that writes a converter script — if using subagents for context management, each subagent must read SAS files and write SQL directly (not write a program that writes SQL)

**PREREQUISITE FOR STEP 6:** As each file's .sql is written to disk, update its entry in `conversion_state.json` to `status: "converted"`. Set `current_step: "5"`. Step 6 CANNOT begin until all converted files are reflected in the state file.

### Step 6: Post-Generation Self-Check (MANDATORY before compilation)

Before submitting to Snowflake for compilation, verify the generated SQL for:
1. **No qualified WORK/temp table names** — temp tables must be bare names, never DATABASE.SCHEMA.TABLE
2. **TEMPORARY keyword preserved** — every CREATE OR REPLACE for a WORK dataset must include TEMPORARY
3. **No RAISE USING MESSAGE syntax** — only named exceptions with RAISE
4. **No unresolved SAS macro variables** — no `&var` or `&&var` in output
5. **No `:var` in scripting control flow** — `:var` only in SQL statements, not in IF/WHILE/assignment
6. **Cross-block variable persistence** — if a variable set in block N is used in block N+1, it must be persisted via SET session variable
7. **No SELECT * leaking helper columns** — ROW_NUMBER() dedup patterns must use explicit column lists
8. **All output tables accounted for** — count matches SAS block's output tables
9. **No vendor-specific SQL syntax remaining** — no DECODE, NVL, CONNECT TO, DISCONNECT FROM
10. **No "similar pattern" / "same as above" shortcuts** — every derivation must be explicit
11. **All validation source tables preserved** — every source table in the SAS validation block appears in the converted SQL validation query; no sources silently dropped
12. **Output table count matches SAS** — every CREATE TABLE/INSERT INTO target in the converted SQL maps to a SAS output dataset; count(DISTINCT output tables in SQL) >= count(DISTINCT output datasets in SAS)
13. **Output column count matches SAS** — column count of each converted output table >= column count of the corresponding SAS output dataset; no columns silently dropped
14. **No files dropped from prior version** (batch/re-run mode) — if re-running a conversion, verify the new output directory has >= the file count of the previous version; any reduction must be explicitly justified by consolidation
15. **Validation reference tables match SAS** — for each anti-join validation check, the reference table in the converted SQL must match the reference table in the SAS source; a master table (e.g., `CUSTOMER_MASTER`) must not be replaced with a derived/subset table (e.g., `CUSTOMER_SUBSET`)
16. **Referential checks not downgraded to value checks** — if SAS checks whether a key EXISTS in a reference table (anti-join), the converted SQL must also use an anti-join, not a simple `WHERE value IS NULL OR value = 0` check
17. **No unresolved stored procedure references** — if the converted SQL calls a stored procedure (e.g., `CALL SP_NAME()`), that SP must either be defined in the output files or explicitly flagged as MANUAL_REVIEW_REQUIRED
18. **No invented elements** — every variable, parameter, column name, and filter condition in the output must trace to the source SAS code; nothing fabricated or "assumed helpful" (see conversion-rules.md Anti-Hallucination rule)
19. **No session variables in VALUES()** — `$VAR` is invalid in `INSERT ... VALUES(...)`; use `INSERT ... SELECT` instead (see common-patterns.md Platform Constraints)
20. **EXECUTE AS CALLER on procs using session vars/temp tables** — any procedure that reads/sets a session variable or shares temp tables across the orchestration chain must be `EXECUTE AS CALLER`, never owner's rights
21. **Reserved-word columns quoted** — SAS column names that are Snowflake reserved words (DESC, TYPE, VALUE, LOCATION, NAME, FILE, STATUS, etc.) must be double-quoted
22. **XLSX I/O uses stored proc + CALL** — PROC IMPORT/EXPORT for XLSX must generate a Python stored procedure + CALL (never `COPY INTO`/`INFER_SCHEMA` on a native `.xlsx`); CSV/pipe stays native SQL
23. **Type-safe joins on migrated keys** — when joining key columns from tables migrated from different sources, both sides are cast to a common type (`::VARCHAR`) to avoid silent NUMBER-vs-VARCHAR zero-row failures (see conversion-rules.md → Migrated-Source Type Traps)
24. **Numeric aggregation guards VARCHAR measures** — `SUM`/`AVG`/etc. on measure columns from migrated tables are wrapped in `TRY_TO_DOUBLE`/`TRY_TO_NUMBER` when the column may be VARCHAR
25. **VARCHAR date columns wrapped in TO_DATE** — date-range comparisons on migrated `*_DT` columns wrap the **column** in `TO_DATE(col, fmt)`, not just the compared value

If any check fails, fix the SQL before proceeding to compilation.

**PREREQUISITE FOR STEP 6a:** After self-check passes for each file, update `conversion_state.json` with `self_check_passed: true`. Set `current_step: "6"`. Step 6a CANNOT begin until all files show `self_check_passed: true`.

### Step 6a: Artifact Presence Verification (HARD GATE)

Before proceeding to Step 7, verify these artifacts exist on disk:
- All converted `.sql` files written to `<output_dir>/`
- Count of output `.sql` files matches expected count from Step 4 classification

**Enforcement:**
1. Check each artifact via filesystem read
2. If ANY missing:
   - Print: `"BLOCKED: Cannot proceed to Step 7. Missing: [list of missing files]"`
   - Update `conversion_state.json`: set `gates.step_6a_artifacts: "BLOCKED"`
   - Attempt to generate missing files (re-run Step 5 for the specific missing file)
   - If generation fails: surface to user with specific remediation action
   - DO NOT proceed until gate passes
3. If all present:
   - Update `conversion_state.json`: set `gates.step_6a_artifacts: "PASSED"`
   - Proceed to Step 7

### Step 6b: State Persistence (automatic — no separate step needed)

The `conversion_state.json` file has been incrementally updated throughout Steps 3-6a. At this point it contains the full classification, conversion status, and gate results. If context is exhausted here, the next session can resume from the earliest incomplete step by reading this file (see Step 1 pre-check).

### Validation Decision Gate (MANDATORY — cannot be silently skipped)

**Load `workflows/validation-pipeline.md`** — the single authoritative validation orchestrator.

After Step 6a passes, present the **two-tier consent gate** (validation runs end-to-end by default once approved — the user does NOT hand-pick phases):
- **Tier-1 (zero cost):** "Run local validation (synthetic data + LLM trace)?" → Yes runs Phase 1 + Phase 2 automatically.
- **Tier-2 (Snowflake credits):** after Phase 2, ONE combined prompt: "Run full Snowflake validation end-to-end (compile + execute + integration/E2E orchestration)?" → Yes runs Phase 3 + Phase 4 + Phase 5 automatically, no further per-phase prompts.

Phases:
- Phase 1: Synthetic Data (always runs under Tier-1) — with range-join/unit alignment (see `synthetic-data-rules.md`)
- Phase 2: LLM Trace (0 credits)
- Phase 3: Snowflake Compilation (minimal credits)
- Phase 4: Snowflake Execution — Tier 2/3 procedures (moderate credits)
- Phase 5: Integration & End-to-End Orchestration Test (moderate credits) — generates a reusable orchestration harness, runs the full pipeline in DAG order, asserts terminal tables non-empty

Each phase has a HARD ARTIFACT GATE that verifies output files exist on disk before allowing the next phase to begin. At each gate, append a line to `checkpoint_log.jsonl`. See `workflows/validation-pipeline.md` for full protocol.

**Phase-specific reference loading:**

| Phase | Reference to Load |
|-------|-------------------|
| Phase 1 | `references/schema-inference.md` + `references/synthetic-data-rules.md` |
| Phase 2 | `references/validation-execution.md` Phase 3A |
| Phase 3 | `references/snowflake-compile.md` |
| Phase 4 | `references/snowflake-execution.md` |
| Phase 5 | `references/e2e-orchestration-test.md` |

**PREREQUISITE:** The user's tier consent decisions must be recorded in `conversion_state.json` under `validation_selections` (`tier1_approved`, `tier2_approved`).

### TRANSITION GATE: Steps 7-10 Are NOT Optional

⛔ The conversion workflow is **NOT complete** after Step 6.
Steps 7, 8, 9, and 10 are **MANDATORY continuations** — not optional quality gates:

- **Validation Pipeline**: Load `workflows/validation-pipeline.md`. Present the two-tier consent gate. Once a tier is approved, its phases execute sequentially and automatically (no per-phase prompts). At every checkpoint, append a line to `checkpoint_log.jsonl`.
  - Phase 1 (Synthetic Data): Runs under Tier-1. Zero credits. HARD GATE on `source_table_ddl.sql` + `synthetic_data.sql`.
  - Phase 2 (LLM Trace): Runs under Tier-1. Zero credits. HARD GATE on `tests/<file>/expected/*.csv`.
  - Phase 3 (Snowflake Compilation): Runs under Tier-2. Minimal credits. HARD GATE on `compilation_results.json`.
  - Phase 4 (Snowflake Execution Tier 2/3): Runs under Tier-2. Moderate credits. HARD GATE on `snowflake_execution_results.json`.
  - Phase 5 (Integration & E2E Orchestration): Runs under Tier-2. Moderate credits. Generates reusable harness (`orchestration/sp_e2e_pipeline.sql`, `task_dag.sql`, `adf_pipeline.sql`, `testing/setup_test_data.sql`, `testing/expected_results.sql`). HARD GATE on `e2e_test_results.json`.
- **Step 10**: Generate `conversion_report.md` with ALL sections. Generate `conversion_report.docx` (best effort).

**DO NOT** present final output to the user until Step 10 is complete.

If context window is nearly exhausted after Step 6, **save all converted files to disk**. The `conversion_state.json` file already captures progress — the next session will resume from the earliest incomplete step.

**Load `workflows/steps-8-10-post-conversion.md`** for Step 10 (Report Generation) only. Steps 8 and 9 are now handled by the modular validation pipeline.

### POST-STEP-10 ARTIFACT GATE (HARD GATE)

After Step 10, verify these artifacts exist on disk:

**Required artifacts:**
- `conversion_state.json` with `current_step: "complete"` (the state tracker is the primary proof of workflow completion)
- `checkpoint_log.jsonl` (append-only audit trail; must contain at least the Step 1 STARTED line and a final `complete` line)
- `compilation_results.json` (even if compilation skipped, file must exist with status)
- `source_table_ddl.sql` (required in batch mode)
- `synthetic_data.sql` (required in batch mode)
- `e2e_test_results.json` + `orchestration/sp_e2e_pipeline.sql` (required when Phase 5 ran)
- `conversion_report.md` with all 6 mandatory sections

**Best-effort artifacts:**
- `conversion_report.docx` (if missing, print: `"DOCX not generated. Install with: pip install python-docx OR brew install pandoc"`)

**Enforcement:**
1. Check each required artifact via filesystem read
2. If ANY required artifact missing:
   - Print: `"BLOCKED: Conversion incomplete. Missing: [list]"`
   - Update `conversion_state.json`: set `gates.step_10_final_artifacts: "BLOCKED"`
   - Attempt to generate missing artifacts (re-run the specific generation step)
   - If generation fails after 1 attempt: surface to user with specific action
   - DO NOT declare conversion complete until gate passes
3. If all required artifacts present:
   - Update `conversion_state.json`: set `current_step: "complete"`, `gates.step_10_final_artifacts: "PASSED"`
   - Append final checkpoint line to `checkpoint_log.jsonl`: `step:"complete" status:"PASSED" notes:"conversion complete"`
   - Print: `"All required artifacts verified. Conversion complete."`

---

## Output Formats

See `templates/output-sql.md` for pure SQL and stored procedure output format, and `templates/output-mixed.md` for mixed SQL + PySpark.
All output files MUST include the standard file header (Converted from, Target Schema, Translation Tier).

---

## Stopping Points

**Interactive mode (< 10 files):**
- ✋ Step 1: Confirm SAS code understanding
- ✋ Step 4: Review block classification and dependency map (especially any PySpark assignments)
- ✋ Step 7: Review LLM tracing results, confirm proceed to compilation
- ✋ Step 8: Confirm compilation results
- ✋ Step 9: User choice on validation testing
- ✋ Step 10: Present conversion report

**Batch mode (10+ files):**
- ✋ Step 1: Confirm target schema and migration mode (ONCE for all files)
- ✋ Step 10: Present consolidated conversion report (ONCE at end)

## Success Criteria

- ✅ ALL blocks attempted as SQL first
- ✅ Stored Procedures used before PySpark
- ✅ PySpark only for true edge cases (HASH, CALL EXECUTE, statistical procs)
- ✅ All code compiles successfully
- ✅ Confidence levels documented
- ✅ Low-confidence blocks clearly marked with MANUAL_REVIEW_REQUIRED
- ✅ Inter-block dependencies tracked and correct
- ✅ Every column derivation explicit — no "similar pattern" shortcuts
- ✅ Every macro branch converted — no skipped branches
- ✅ WORK tables use TEMPORARY keyword with no schema prefix
- ✅ Snowflake Scripting syntax correct (named exceptions, :var only in SQL, SELECT INTO)
- ✅ Post-generation self-check passed (Step 6)
- ✅ Conversion report generated with all applicable sections (Step 10)
- ✅ Cross-file DAG and orchestration recommendation provided (when 2+ files)
- ✅ All manual remediation items catalogued with priority
- ✅ Validation checks use data-driven lookups — no hardcoded value lists replacing dimension table references
- ✅ All validation source tables preserved — no sources silently dropped from SAS checks
- ✅ Output column count matches SAS — no columns silently dropped from output tables
- ✅ Consolidation preserves all output tables — no SAS output datasets lost during file merging
- ✅ All mandatory artifacts present (Step 6a checklist passed)

## Mandatory Output Artifacts

At the end of every conversion, verify these files exist before declaring completion:

| Artifact | File | Required |
|----------|------|----------|
| Converted SQL | `<output_dir>/*.sql` | Always |
| Conversion state | `<output_dir>/conversion_state.json` | Always |
| Checkpoint log | `<output_dir>/checkpoint_log.jsonl` | Always (append-only audit trail) |
| Source table DDL | `<output_dir>/source_table_ddl.sql` | Batch mode |
| Synthetic data | `<output_dir>/synthetic_data.sql` | Batch mode |
| Compilation results | `<output_dir>/compilation_results.json` | Always (even if skipped: status field required) |
| Snowflake execution results | `<output_dir>/snowflake_execution_results.json` | When Phase 4 runs |
| E2E test results | `<output_dir>/e2e_test_results.json` | When Phase 5 runs |
| E2E orchestration harness | `<output_dir>/orchestration/sp_e2e_pipeline.sql`, `task_dag.sql`, `adf_pipeline.sql` | When Phase 5 runs |
| E2E test harness | `<output_dir>/testing/setup_test_data.sql`, `expected_results.sql` | When Phase 5 runs |
| Conversion report | `<output_dir>/conversion_report.md` | Always |
| Conversion report DOCX | `<output_dir>/conversion_report.docx` | Best effort |

**Enforced by POST-STEP-10 HARD GATE** — if any required artifact is missing, the gate blocks completion and attempts generation.

---

## Output

Snowflake SQL or Stored Procedures with:
- Tier classification documented
- Conversion notes per block
- Compilation status per file (from `compilation_results.json`)
- Test artifacts (`source_table_ddl.sql`, `synthetic_data.sql`)
- Conversion report (always generated) with:
  - Difficult/unremediated block inventory
  - Test results summary
  - Cross-file DAG diagram (when applicable)
  - Snowflake-native orchestration recommendation with SQL
  - Manual remediation action items with priorities
