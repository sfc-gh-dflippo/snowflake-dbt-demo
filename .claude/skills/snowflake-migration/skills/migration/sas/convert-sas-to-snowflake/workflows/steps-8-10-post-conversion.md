# Steps 8-10: Post-Conversion (Compilation, Testing, Report)

## When to Load

Load this file at Step 10 (Report Generation). Steps 8 and 9 are now handled by the modular validation pipeline in `workflows/validation-pipeline.md`.

**Validation phases (modular — load separately):**
- Phase 3 (Compilation): `references/snowflake-compile.md`
- Phase 4 (Snowflake Execution): `references/snowflake-execution.md`

---

## Snowflake Interaction Policy (CRITICAL)

ALL Snowflake operations that create objects or consume credits REQUIRE explicit user confirmation. Each validation phase (4 and 5) has its own mandatory prompt with credit impact estimate. See `workflows/validation-pipeline.md` for the prompt templates.

### Confirmation Categories

| Category | Examples | Confirmation Required |
|----------|----------|----------------------|
| Object Creation | CREATE TABLE, CREATE PROCEDURE, CREATE TASK | Yes — always |
| SQL Compilation | `snowflake_sql_execute` with `only_compile=true` | Yes — Phase 4 prompt |
| SQL Execution | Running converted code, validation queries | Yes — Phase 4 prompt |
| Stub Tables | CREATE/DROP scaffolding tables for compilation | Yes — part of Phase 4 |
| Testing | Synthetic data, expected baselines, comparison | Zero-cost (Phase 2) or Phase 4 |

### Confirmation Pattern

Before any Snowflake operation, present:
```
SNOWFLAKE OPERATION REQUIRED

Action: [description of what will happen]
Objects affected: [list of tables/procedures/objects]
Estimated credit impact: [minimal/moderate/significant]

Proceed? [Yes] / [No - Skip] / [Show SQL first]
```

If user selects "Show SQL first", display the exact SQL that will execute, then re-prompt.

### Testing Mode

Validation testing executes converted SQL against Snowflake using synthetic data. Covers all tiers (SQL + stored procedures). Requires credit confirmation per Snowflake Interaction Policy.

---

### Step 8: Compile Converted SQL

**MANDATORY STATE WRITE:** At the START of Step 8, set `current_step: "8"` in `conversion_state.json`. This ensures resume after context loss knows compilation was in progress.

**MANDATORY PROMPT** — Ask the user UNLESS consent propagation is active (user pre-approved compilation in Step 1 or at a prior prompt). Compilation proceeds unless user explicitly declines.

By this point, Step 7 (Local LLM Tracing) has already validated conversion logic against synthetic data. This step checks Snowflake SQL syntax via dry-run compilation.

**Consent-aware behavior:**
- **If consent propagation active** (`pre_approved_compilation: true` in conversion_state.json, OR user already said "Yes" at Step 7c compilation gate): Auto-proceed without prompting. Print: `"Auto-proceeding with Snowflake compilation (pre-approved). Compiling [N] files with only_compile=true."`
- **If no consent propagation:** Present the compilation prompt:

```
SNOWFLAKE COMPILATION

Files to compile: [N] .sql files
Method: only_compile=true (dry-run, no objects created)
Estimated credit impact: Minimal (compilation only)

[Batch mode: list files grouped by phase]
[Interactive mode: list all files with line counts]

Proceed? [Yes - Compile All (recommended)] / [No - Skip Compilation]
```

**If Yes (default path):**
1. **Check compilation environment** — attempt to compile ONE file as a probe:
   - If probe succeeds: proceed to step 3.
   - If error = "Database does not exist" or "Schema does not exist": proceed to **Step 8-pre (Compilation Environment Setup)** below.
   - If error = "Object does not exist" (table-level): proceed to Step 8a (stub tables per `references/batch-mode.md`).
2. After environment is ready (Step 8-pre or 8a completed): resume compilation.
3. Compile ALL files with `only_compile=true`. Do NOT stop on first failure.
4. For each failed file: enter the **Fix-and-Retry Loop** (Step 8b below).
5. Write `<output_dir>/compilation_results.json` with pass/fail per file.
6. Update `conversion_state.json` per file: `compilation_status`, `compilation_fix_attempts`, `compilation_errors`.
7. Present aggregate results.

#### Step 8-pre: Compilation Environment Setup (Auto-Create DB/Schema)

When compilation fails because the target database or schema does not exist, automatically offer to create it. This unblocks compilation for greenfield migrations where the target environment has not been provisioned.

**Detection:** The probe compile (step 1 above) returns one of:
- `SQL compilation error: Database 'X' does not exist or not authorized.`
- `SQL compilation error: Schema 'X.Y' does not exist or not authorized.`

**Consent-aware behavior:**
- **If user pre-approved compilation (consent propagation active):** Auto-select Option 1 (temporary compilation environment). Print: `"Target DB/schema does not exist. Auto-creating temporary compilation environment (will be dropped after compilation)."` Execute Steps 1-8 below without prompting. After compilation, auto-drop the temporary environment without prompting.
- **If user has NOT pre-approved (no consent propagation):** Present the 3-option prompt below.

**Action (when prompting required):**
```
COMPILATION ENVIRONMENT SETUP

Target database/schema [TARGET_DB].[TARGET_SCHEMA] does not exist in the connected account.

Options:
  [1. Create temporary compilation environment (auto-dropped after)]
     Creates: DATABASE + SCHEMA + source tables from source_table_ddl.sql
     Populated with synthetic data for realistic compilation
     Dropped automatically after compilation completes

  [2. Create persistent environment (kept for ongoing development)]
     Creates: DATABASE + SCHEMA + source tables from source_table_ddl.sql
     Kept after compilation for future testing and development

  [3. Skip compilation]
     Record compilation as SKIPPED. Proceed to validation.
```

**If option 1 (Temporary) or option 2 (Persistent) selected (or auto-selected via consent propagation):**

**Resume detection:** If `compilation_env` is already non-null in `conversion_state.json` (e.g., `"created_temp"`), the environment was already created in a prior context window. Skip creation steps 1-6 and proceed directly to compilation (step 8).

1. Execute: `CREATE DATABASE IF NOT EXISTS <target_db>;`
2. Execute: `USE DATABASE <target_db>;`
3. Execute: `CREATE SCHEMA IF NOT EXISTS <target_schema>;`
4. Execute: `USE SCHEMA <target_db>.<target_schema>;`
5. Execute the contents of `source_table_ddl.sql` (all CREATE TABLE IF NOT EXISTS statements)
6. Execute the contents of `synthetic_data.sql` (populates tables with test data for compilation context)
7. Record in `conversion_state.json`: `"compilation_env": "created_temp"` or `"created_persistent"`
8. Proceed to compile all files (step 3 of "If Yes" path above)

**After compilation completes (option 1 / temporary only):**

**Consent-aware cleanup:**
- **If consent propagation active:** Auto-drop temporary database without prompting. Print: `"Dropping temporary compilation environment [TARGET_DB]."`
- **If no consent propagation:** Present the cleanup prompt:

```
COMPILATION ENVIRONMENT CLEANUP

Action: Drop temporary database [TARGET_DB] (created for compilation only)
Objects: [N] tables in [TARGET_SCHEMA]

Proceed? [Yes - Drop All] / [No - Keep for debugging]
```
- If Yes: `DROP DATABASE IF EXISTS <target_db>;`
- If No: keep for user inspection, note in report

**If option 3 (Skip):**
- Write `compilation_results.json` with `"status": "SKIPPED BY USER - NO TARGET DB"`
- Proceed to Step 9

**Rules:**
- The `source_table_ddl.sql` from Step 7a is REUSED here — no new DDL inference needed
- Synthetic data provides realistic column values so type-checking during compilation is meaningful
- For option 1 (temporary): use a timestamped name if the user's target DB name conflicts with existing databases: `<target_db>_COMPILE_<YYYYMMDD>`
- NEVER silently create databases — always prompt per Snowflake Interaction Policy
- If `source_table_ddl.sql` does not exist at this point, generate it first (re-run Step 7a DDL generation)

**If No (user declines):**
1. Write `<output_dir>/compilation_results.json` with:
   ```json
   {
     "compiled_at": "<ISO timestamp>",
     "status": "SKIPPED BY USER",
     "total_files": <count>,
     "passed": 0,
     "failed": 0,
     "reason": "User declined compilation"
   }
   ```
2. Proceed to Step 9.

**HARD GATE:** `compilation_results.json` MUST exist before Step 9 begins. If it does not, halt and generate it.

#### Compilation Results File

After compilation (or skip), write `<output_dir>/compilation_results.json`:
```json
{
  "compiled_at": "<ISO timestamp>",
  "total_files": 91,
  "passed": 88,
  "failed": 3,
  "pass_rate": "96.7%",
  "failures": [
    {"file": "example.sql", "error": "Object 'TABLE' does not exist", "category": "missing_table"}
  ]
}
```
Step 10 reads this file. If it does not exist, Section 1 Compile Status = "COMPILATION NOT PERFORMED".

#### Step 8b: Fix-and-Retry Loop (max 3 attempts per file)

When a file fails compilation, automatically attempt to fix known error patterns before escalating to the user.

**Loop logic (per failed file):**
1. Parse the Snowflake error message (line number, error code, description)
2. Map error to known fix patterns:

| Error Pattern | Auto-Fix Action |
|--------------|-----------------|
| Unknown function X | Check `references/function-mappings.md`, replace with Snowflake equivalent |
| Invalid identifier | Check for unresolved SAS macro variable or vendor-specific syntax |
| Syntax error near X | Check Snowflake Scripting rules (named exceptions, `:var` usage, SELECT INTO) |
| Object does not exist | Check temp table references — add TEMPORARY or reorder block dependencies |
| Type mismatch / incompatible types | Add explicit CAST or COALESCE wrapper |
| Unexpected keyword | Check for reserved word collision — quote identifier with double quotes |
| Missing column | Verify against source DDL — add column or flag MANUAL_REVIEW_REQUIRED |

3. Apply fix to the .sql file on disk
4. Re-compile with `only_compile=true`
5. **Write state to disk IMMEDIATELY after each attempt** — update `compilation_fix_attempts` and append to `compilation_errors` in `conversion_state.json`. This prevents retry-counter loss on context exhaustion.
6. Evaluate result:
   - **PASS:** Set `compilation_status: "SUCCESS"`, record fix in `compilation_errors` array. Done.
   - **FAIL, attempts < 3:** Increment `compilation_fix_attempts`, loop back to step 1.
   - **FAIL, attempts >= 3:** Set `compilation_status: "FAILED_AFTER_RETRIES"`. Log all errors. Continue to next file.

**Rules:**
- NEVER modify the original SAS interpretation — only fix syntax/function/type issues, not logic
- Each fix attempt is logged: `{"attempt": N, "error": "...", "fix_applied": "..."}`
- If the error does not match any known pattern, skip auto-fix and set `compilation_status: "FAILED_UNKNOWN_ERROR"`
- After all files processed, present summary:
  ```
  COMPILATION RESULTS

  Total files: [N]
  Passed (first try): [X]
  Passed (after auto-fix): [Y] 
  Failed (max retries exceeded): [Z]

  Auto-fixes applied:
    - [file]: [error] → [fix description]
  
  Unresolved (require manual review):
    - [file]: [error message]
  ```

#### Step 8a: Greenfield / Stub-Table Compilation

When target tables do not exist (greenfield migration):
1. Use `source_table_ddl.sql` (from Step 7a) to create stub tables.
2. Confirm stub creation per Snowflake Interaction Policy.
3. Compile all files against stubs.
4. Confirm stub cleanup (drop after compilation).

See `references/batch-mode.md` Step 8a for full stub table workflow.

### Step 9: Validation Testing (Snowflake Execution)

**MANDATORY STATE WRITE:** At the START of Step 9, set `current_step: "9"` in `conversion_state.json`.

#### Step 9a: Verify Test Artifacts (from Step 7)

Step 7 already generated `source_table_ddl.sql` and `synthetic_data.sql`. Verify both files exist in `<output_dir>/`. If missing, generate them now using `references/schema-inference.md` and `references/synthetic-data-rules.md`.

#### Step 9b: Test Execution

**Check Validation Decision Gate selection** (from `conversion_state.json` → `metadata.validation_scope`):
- If `"skipped"`: record `validation_status: "SKIPPED BY USER"` for all files. Skip to Step 10.
- If `"trace_only"`: record `validation_status: "TRACE ONLY"` for all files. Skip to Step 10.
- If `"full"`: proceed with Snowflake execution below.

**Snowflake Execution:**
1. Confirm per Snowflake Interaction Policy:
   ```
   SNOWFLAKE TEST EXECUTION

   Action: Run synthetic data + converted SQL on Snowflake
   Objects: [N] temporary tables (auto-dropped after testing)
   Warehouse: [current warehouse]
   Credit impact: Moderate (depends on warehouse size)

   Proceed? [Yes] / [No - Skip] / [Show SQL]
   ```
2. If approved: execute `source_table_ddl.sql`, `synthetic_data.sql`, then each converted file in dependency order.
3. Compare outputs against Phase 2 expected baselines using `references/comparison-rules.md`.
4. Write `snowflake_execution_results.json`.
5. Drop temporary test objects.

**If Skip:**
1. Test artifacts are already written — these are the deliverable.
2. Record testing status as "SKIPPED BY USER" in report data.
3. Proceed to Step 10.

### Step 10: Generate Conversion Report (MANDATORY)

**MANDATORY STATE WRITE:** At the START of Step 10, set `current_step: "10-in-progress"` in `conversion_state.json`. This distinguishes "report generation started but not finished" from "not yet started." On successful completion, set `current_step: "10"`.

**Batch mode (10+ files):** Generate consolidated report with ALL sections populated. This is the ONLY stopping point in batch mode (besides Step 1).

**ALWAYS generate a conversion report at the end of every conversion session.**

Load `templates/conversion-report.md` and generate the report with:

**PRE-CONDITION CHECK** (before generating):
- Read `<output_dir>/compilation_results.json` → populate Section 1 Compile Status. If file missing → "COMPILATION NOT PERFORMED"
- Read Step 7 tracing results → populate Section 3a. If tracing not run → "LLM TRACING NOT PERFORMED"
- Check if `source_table_ddl.sql` and `synthetic_data.sql` exist → populate Section 3. If missing → "Test artifacts not generated"
- Read `<output_dir>/snowflake_execution_results.json` if it exists → populate Section 3 with Snowflake validation results (per-file status counts, error categories). Override any "NOT TESTED" / "skipped" / "not generated" placeholders in Section 3, 3a, and 3b with actual results. This file may be generated in a later session (e.g., when user runs validation separately); always check for it.

**MANDATORY sections** (MUST be populated, never silently omitted):
- ✅ Section 1 (Conversion Summary) — always
- ✅ Section 2 (Difficult Blocks) — always (even if empty: "No difficult blocks identified")
- ✅ Section 3 (Testing) — batch: list test artifact files; interactive: full results or "NOT TESTED"
- ✅ Section 3a (Data Validation Summary) — when validation performed
- ✅ Section 3b (Data Quality Gate Readiness) — when validation performed
- ✅ Section 4 (Consolidation) — when 2+ files or Optimize & Consolidate mode
- ✅ Section 5 (DAG + Orchestration) — when 2+ files with dependencies; MUST include mermaid diagram, DAG properties, CREATE TASK SQL, Dynamic Table alternative
- ✅ Section 5c (Orchestration Deployment Checklist) — when orchestration recommended
- ✅ Section 5d (Runtime/Sizing) — when orchestration recommended
- ✅ Section 5e (Monitoring Recommendations) — when orchestration recommended
- ✅ Section 6 (Manual Remediation) — always (even if empty: "No remediation required")

Generate the report with:

1. **Conversion Summary** — files processed, blocks analyzed, tier distribution, compile/test status per file
2. **Difficult / Unremediated Blocks** — every block not classified as Tier 1 HIGH confidence: PySpark blocks, low/medium confidence, MANUAL_REVIEW_REQUIRED markers, missing %INCLUDE sources, external LIBNAME, HASH/CALL EXECUTE, statistical procs
3. **Testing Results** — per-file test pass/fail (from Step 8), root cause analysis for failures. Mark "NOT TESTED" if user skipped validation. Include test artifact map linking to `tests/<script>/` subfolders (synthetic data, expected baselines, actual results, per-script validation reports)
4. **Multi-Script Consolidation** — flag when multiple SAS files produce the same output artifact; include traceability matrix
5. **Cross-File DAG** — if 2+ SAS files share data dependencies, generate a mermaid dependency diagram following `references/mermaid-diagrams.md` rules. Include DAG properties (critical path, parallelizable groups, independent pipelines)
6. **Orchestration Recommendation** — for each DAG, recommend a Snowflake-native orchestration approach:
   - **Snowflake Tasks DAG** (default): for pipelines with stored procedures, side effects, or mixed SQL/PySpark
   - **Dynamic Tables**: for pure SQL pipelines where incremental refresh is preferred
   - **Tasks + Streams**: when pipeline should react to new data arrivals
   - Generate the actual CREATE TASK / CREATE DYNAMIC TABLE SQL for the recommended approach
   - **Orchestration deployment is REPORT-ONLY** — the SQL is generated in the report for reference. DO NOT execute CREATE TASK / CREATE DYNAMIC TABLE unless the user explicitly requests deployment. If deployment is requested, confirm per the Snowflake Interaction Policy before executing:
     ```
     SNOWFLAKE OBJECT CREATION

     Action: Deploy orchestration objects
     Objects: [list of CREATE TASK / CREATE DYNAMIC TABLE statements]
     Credit impact: Moderate (ongoing scheduled execution)

     Proceed? [Yes] / [No - Keep as report only] / [Show SQL first]
     ```
7. **Manual Remediation** — consolidate ALL items needing human attention with priority (P1/P2/P3) and specific action required

**Output Formats**: Generate the report in TWO formats:
1. **Markdown** — write to `<output_dir>/conversion_report.md`
2. **DOCX** — write to `<output_dir>/conversion_report.docx` using Python:

```python
# Generate DOCX from the markdown report
import subprocess
# Use pandoc if available
subprocess.run(['pandoc', 'conversion_report.md', '-o', 'conversion_report.docx',
                '--from=markdown', '--to=docx'], check=True)
```

If `pandoc` is not available, use `python-docx` as fallback — parse the generated `.md` file
(single source of truth) and convert to DOCX following the code pattern in `templates/conversion-report.md`
(the "Fallback method" section). Do NOT generate DOCX content independently from the markdown;
always derive it from the `.md` file to ensure full fidelity.

If neither `pandoc` nor `python-docx` is available, inform the user and output .md only.

**Post-report state update:** Update `conversion_state.json` with `current_step: "10"`. The final artifact gate (Post-Step-10) will set it to `"complete"`.

**⚠️ STOP**: Present the report to the user. Confirm both files were written.

---

### Post-Step-10: Artifact Verification (MANDATORY)

Before declaring conversion complete, verify all required artifacts exist on disk.

**Required artifacts (must exist):**
- [ ] `conversion_state.json` — must show `current_step: "complete"` (primary proof of workflow completion)
- [ ] `compilation_results.json` — even if compilation was skipped, file must exist with a status field
- [ ] `source_table_ddl.sql` — required in batch mode (10+ files)
- [ ] `synthetic_data.sql` — required in batch mode (10+ files)
- [ ] `conversion_report.md` — must contain all 6 mandatory section headings

**Best-effort artifacts:**
- [ ] `conversion_report.docx` — if missing, print: `"DOCX not generated. Install with: pip install python-docx OR brew install pandoc"`

**Report section headings check** — verify `conversion_report.md` contains these headings:
1. "Conversion Summary" or "Summary"
2. "Difficult" or "Unremediated"
3. "Testing" or "Test"
4. "Consolidation" (if Optimize & Consolidate mode was used)
5. "DAG" or "Orchestration" (if 2+ files with dependencies)
6. "Manual Remediation" or "Remediation"

**If ANY required artifact is missing:**
```
INCOMPLETE: Missing required artifacts: [list]
Generate missing artifacts before declaring conversion done.
```

**If all required artifacts present:**
```
All required artifacts verified. Conversion complete.
```

**Post-verification state update:** If all artifacts present, update `conversion_state.json` — set `current_step: "complete"`, `gates.step_10_final_artifacts: "PASSED"`.

---

### Workflow Summary (Steps 8-10)

```
Step 7 (LLM Tracing) complete
  ↓
Step 8: Snowflake Compilation (user-prompted)
  ↓
Step 9: Snowflake Execution (compares against Step 7 baselines)
  ↓
Step 10: Conversion Report (always generated)
  ↓
Post-Step-10: Artifact Verification
```
