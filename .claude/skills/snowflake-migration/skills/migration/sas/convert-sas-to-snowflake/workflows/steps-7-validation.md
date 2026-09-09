# Steps 7: Validation Protocol (Router)

## DEPRECATED — Use `workflows/validation-pipeline.md` Instead

This file is retained for backward compatibility. The validation logic has been refactored into modular phases in `workflows/validation-pipeline.md`.

**New architecture:**
- Phase 1 (Synthetic Data): Always runs after Step 6a
- Phase 2 (LLM Trace): `workflows/validation-pipeline.md` Phase 2 + `references/validation-execution.md`
- Phase 3 (Compilation): `references/snowflake-compile.md`
- Phase 4 (Snowflake Exec): `references/snowflake-execution.md`

## When to Load

Load `workflows/validation-pipeline.md` instead. This file should NOT be loaded for new conversions.

---

## Validation Decision Gate (MANDATORY — cannot be silently skipped)

Before beginning Step 7b (LLM tracing) or Step 9 (Snowflake execution), the user MUST be prompted for their validation scope. This prompt fires ONCE and governs both steps. It CANNOT be silently bypassed — if context is exhausted before this prompt fires, the next session MUST present it upon resume.

**Exception (consent propagation):** If `pre_approved_validation` is set in `conversion_state.json` (detected from user's initial request), skip this prompt and auto-select the pre-approved scope.

```
VALIDATION OPTIONS

Step 7b — LLM Logic Trace:
  Traces SAS logic row-by-row against synthetic data to produce expected baselines.
  Coverage: [N] representative files (batch) or all files (interactive).
  Cost: Zero credits (runs locally).

Step 9 — Snowflake Execution:
  Executes converted SQL against synthetic data on Snowflake. Compares actual vs expected.
  Coverage: All tiers (SQL + stored procedures).
  Cost: Moderate credits (Snowflake execution).

Select validation scope:
  [1. Full validation — Steps 7b + 9 (recommended)]
  [2. Trace only — Step 7b only, skip Snowflake execution]
  [3. Skip all validation — proceed to compilation and report]
```

**Behavior based on selection:**
- **Option 1 (Full):** Run Step 7a (test artifacts), Step 7b (trace), Step 7c (present results), then Step 9 (Snowflake execution).
- **Option 2 (Trace only):** Run Step 7a + 7b + 7c. Skip Step 9. Record `validation_status: "TRACE ONLY"` in `conversion_state.json`.
- **Option 3 (Skip):** Run Step 7a (test artifact generation is always required). Skip Steps 7b and 9. Record `validation_status: "SKIPPED BY USER"` for all files in `conversion_state.json`.
- In ALL cases, the conversion report (Step 10 Section 3) MUST reflect the user's choice — never silently omit the validation section.

**PREREQUISITE FOR STEP 7b:** The user's validation scope selection must be recorded in `conversion_state.json` under `metadata.validation_scope` ("full", "trace_only", or "skipped"). Step 7b CANNOT begin without this.

---

## Step 7a: Generate Test Artifacts

1. Generate `source_table_ddl.sql` using `references/schema-inference.md` type mapping rules.
   Parse SAS code (PROC IMPORT, INFILE/INPUT, PROC SQL CREATE TABLE, DATA step SET/MERGE).
   Write CREATE TABLE IF NOT EXISTS for every external source table.
2. Generate `synthetic_data.sql` using `references/synthetic-data-rules.md`.
   Row count: 50 rows via GENERATOR() (batch mode) or 5-8 rows via INSERT VALUES (interactive).
   Write all INSERT statements.
3. Write both files to `<output_dir>/`.

**HARD GATE (Step 7a → Step 7b):**
1. Verify `source_table_ddl.sql` and `synthetic_data.sql` both exist on disk
2. If ANY missing:
   - Print: `"BLOCKED: Cannot proceed to Step 7b. Missing: [list]"`
   - Update `conversion_state.json`: set `gates.step_7a_test_artifacts: "BLOCKED"`
   - Attempt to generate the missing file (re-run the relevant generation step above)
   - If generation fails after 1 attempt: surface to user — "Cannot infer schema for [tables]. Provide DDL or sample data."
   - DO NOT proceed until both files exist
3. If both present:
   - Update `conversion_state.json`: set `gates.step_7a_test_artifacts: "PASSED"`
   - Proceed to Step 7b

---

## Step 7b: SAS Logic Trace (Phase 3A) — Iterative Batch Protocol

Load `references/validation-execution.md` Phase 3A and `references/auto-validation.md` Phase 3.

**Interactive mode (<10 files):** Trace ALL converted files in a single pass.

**Batch mode (10+ files):** Trace a priority subset of 10-15 representative files using the **iterative batch protocol** below. This ensures tracing completes even when context windows are limited.

**Priority file selection** (see `references/auto-validation.md` Phase 3.2):
- 2-3 anti-join validation patterns (most common)
- 2-3 GROUP BY / aggregation patterns
- 2-3 multi-table JOIN + UNION ALL
- 1-2 CASE expression / product mapping
- 1-2 window function / ROW_NUMBER dedup
- 1-2 complex multi-step (>3 blocks)

**Iterative Batch Protocol (batch mode):**

Process files in batches of 5. Checkpoint after each batch to enable resume across context windows.

```
BATCH TRACE LOOP:
  1. Read conversion_state.json → check trace_progress
     - If trace_progress.files_remaining is empty: all files traced → go to Step 7c
     - If trace_progress does not exist: initialize it (select priority files, populate files_remaining)
  2. Take next 5 files from files_remaining (or fewer if <5 remain)
  3. For each file in current batch:
     a. Read original SAS code (the .sas source file)
     b. Read synthetic data for all source tables used by this file
     c. Trace SAS logic row-by-row against synthetic data:
        - DATA Step: Initialize PDV, process row-by-row, apply SAS missing semantics
        - PROC SQL: Standard SQL semantics, NULL propagation
        - MERGE: NOT equivalent to JOIN — interleave within BY-groups, track IN= flags
     d. Produce expected output for each output table
     e. Write to tests/<file>/expected/expected_<table>.csv
     f. Update conversion_state.json: move file from files_remaining to files_traced
     g. If tracing identifies a potential logic concern (e.g., NULL semantics divergence, MERGE many-to-many risk, missing value comparison difference), append it to `trace_progress.concerns_found` with `{file, concern, severity}`
  4. After batch of 5 completes:
     - Write conversion_state.json with updated trace_progress
     - If context budget allows: continue to next batch (go to step 2)
     - If context nearing limit: save state, inform user:
       "Traced [N]/[total] files. Progress saved. Resume with next session."
  5. When files_remaining is empty: proceed to Step 7c
```

**State tracking (conversion_state.json):**
```json
{
  "trace_progress": {
    "total_files_in_scope": 15,
    "files_traced": ["02_validate_customers", "07_validate_orders"],
    "files_remaining": ["41_build_summary_fact"],
    "current_batch": 2,
    "batch_size": 5,
    "concerns_found": []
  }
}
```

**Resume behavior:** When a new context window starts and `trace_progress.files_remaining` is non-empty, resume from step 1 of the batch loop. Do NOT re-trace files already in `files_traced`.

---

## Step 7c: Present Tracing Results

Present summary to user:
```
LOCAL VALIDATION (LLM SAS LOGIC TRACE)

Files traced: [N] / [total]
Output tables validated: [M]
Baselines generated: tests/<file>/expected/*.csv

Tracing identified [X] potential logic concerns:
  - [list any translation issues found during tracing]
```

**Consent-aware behavior:**
- **If compilation was pre-approved** (user already said "Yes - compile" at Step 8 prompt, OR `pre_approved_compilation: true` in conversion_state.json, OR batch mode with compilation consent): Auto-proceed to Step 8 without prompting. Print: `"Auto-proceeding to Snowflake compilation (pre-approved)."`
- **If compilation was NOT pre-approved** (interactive mode, no prior consent): Present the compilation gate prompt:
  ```
  Proceed to Snowflake compilation? [Yes] / [No - Review baselines first] / [Skip compilation]
  ```

This prompt gates entry to Step 8 (Snowflake Compilation) ONLY when consent has not been propagated.

**PREREQUISITE FOR STEP 8:** Update `conversion_state.json` — set `current_step: "7"`, update `gates.step_7a_test_artifacts`. Step 8 CANNOT begin until this write is confirmed.
