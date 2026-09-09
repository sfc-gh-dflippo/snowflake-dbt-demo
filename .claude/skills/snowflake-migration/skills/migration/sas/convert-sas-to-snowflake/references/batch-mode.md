# Batch Mode (10+ Files)

When converting 10 or more SAS files in a single session, **batch mode** is automatically enabled. Batch mode reduces interactive stopping points to keep large conversions efficient.

**NOTE**: All Snowflake operations (compilation, stub tables) require user confirmation per the Snowflake Interaction Policy in `workflows/steps-8-10-post-conversion.md`. Testing mode (Local or Snowflake) is selected by user prompt in Step 9b.

## Batch Mode Rules

| Step | Interactive (Default) | Batch Mode |
|------|----------------------|------------|
| Step 1: Gather Input | Ask per file | Gather ONCE for entire directory; apply same schema/mode to all files |
| Step 4: Block Analysis | STOP for review | Log classification per file; do NOT stop for confirmation. Present aggregate summary at end. |
| Step 7: LLM Tracing | N/A | Step 7a (test artifacts) always runs. For 7b (logic trace): prompt user via Validation Decision Gate ONCE (see SKILL.md) — user selects Full / Trace only / Skip. Once selected, auto-execute without further prompts (consent propagation). |
| Step 7c: Trace Results | STOP for review | Present summary. If compilation pre-approved (consent propagation): auto-proceed to Step 8 without "Proceed to compilation?" prompt. |
| Step 8: Compilation | STOP for results | Prompt ONCE. If user says Yes and DB doesn't exist, auto-create temporary compilation environment via Step 8-pre (consent propagation). Do NOT re-prompt for Step 8-pre options. Do NOT stop on first failure. |
| Step 8a: Stub Tables | N/A | If consent propagation active: auto-create stubs, auto-drop after compilation. Otherwise: confirm before creating stubs; confirm before dropping stubs. |
| Step 9: Validation | Ask per file | Follows validation scope from the Validation Decision Gate. Executes on Snowflake with credit confirmation. No separate "Select testing mode" prompt needed — scope is already determined. |
| Step 10: Report | STOP for review | Generate single consolidated report for all files with ALL 6 sections. Present once at end. |

## Batch Mode Detection

Batch mode activates when:
- User provides a **directory path** containing 10+ `.sas` files
- User provides a **file list** with 10+ entries
- User says "convert all", "batch convert", or "convert the directory"

## Context Budget (Large Batch)

When converting 50+ files, the context window may be exhausted during Steps 1-6. Split the workflow into phases:

**CONVERSION METHOD (MANDATORY):** Each SAS file MUST be individually read by the LLM, semantically analyzed for SAS-specific behavior (missing values, BY-group processing, MERGE semantics, RETAIN state), and converted to Snowflake SQL by the LLM directly writing the .sql output. Do NOT write a script/program to batch-convert files. When context is limited, process 10-20 files per context window and resume via `conversion_state.json`.

- **Phase A** (Steps 1-6): Convert all files, write `.sql` to disk
- **Phase B** (Step 7): LLM Tracing — generate DDL + synthetic data, trace SAS logic, produce expected baselines
- **Phase C** (Step 8): Read back files from disk, compile all, write `compilation_results.json`
- **Phase D** (Steps 9-10): Snowflake execution, comparison, conversion report

If context is exhausted during Phase A, save progress to disk and prompt:
> "Conversion files written to `<output_dir>`. Continue with compilation and testing? (Steps 7-9)"

This ensures Steps 7-9 always execute, even across multiple context windows.

**CRITICAL**: If context is exhausted before Steps 7-10, the `conversion_state.json` state tracker ensures the next session resumes from the earliest incomplete step. The prompt-based gates in Steps 7c and 8 still apply when resuming.

## Context Window Recovery

When a new context window starts after Step 6 (or mid-conversion):
1. Read `<output_dir>/` to list existing `.sql` files — confirm conversion files exist
2. Check for `compilation_results.json` — if missing, start at Step 7 (LLM tracing first, then compilation)
3. Check for `source_table_ddl.sql` + `synthetic_data.sql` — if missing, start at Step 7a
4. Check for `conversion_report.md` — if missing, start at Step 10
5. **Always pick up at the earliest missing step** — never re-run completed steps
6. If re-running a conversion (same source, new output), verify the new output has >= the file count of the previous version
7. **Check intra-phase progress** — read `conversion_state.json` for `trace_progress` and `execution_progress` fields. If either has non-empty `files_remaining`, resume within that phase.

## Intra-Phase Checkpointing (Large Batch)

When a phase cannot complete in a single context window, use these checkpoints to enable resume:

### Phase B (Step 7b — LLM Trace):
- **Batch size:** 5 files per checkpoint
- **Checkpoint trigger:** After each batch of 5 files traced and written to disk
- **State field:** `conversion_state.json` → `trace_progress`
- **Resume condition:** `trace_progress.files_remaining` is non-empty
- **Recovery:** Read `files_traced` list, skip those, continue with `files_remaining`
- **Output per batch:** `tests/<file>/expected/expected_<table>.csv` files written to disk

### Phase C (Step 8 — Compilation):
- **Batch size:** 20 files per checkpoint
- **Checkpoint trigger:** After each batch of 20 files compiled
- **State field:** `conversion_state.json` → per-file `compilation_status`
- **Resume condition:** Any file has `compilation_status: "PENDING"`
- **Recovery:** Compile only PENDING files (skip those already SUCCESS/FAILED)

### Phase D (Step 9 — Snowflake Execution):
- **Batch size:** 10-15 files per checkpoint (respecting dependency order)
- **Checkpoint trigger:** After each batch executed and compared
- **State field:** `conversion_state.json` → per-file `validation_status`
- **Resume condition:** Any Tier 2/3 file has `validation_status: "PENDING"`
- **Recovery:** Execute only PENDING files (skip those already PASS/FAIL)

### Context Budget Heuristic

The LLM should monitor its own context consumption and apply this heuristic:

```
IF context_consumed > 60% AND current_phase is NOT complete:
  1. Finish current batch (do NOT leave mid-file — partial traces are invalid)
  2. Write all state to disk (conversion_state.json + any output CSVs)
  3. Inform user: "Context budget nearing limit. [N]/[total] files processed.
     Progress saved to conversion_state.json. Resume in next session."
  4. If user says "continue": attempt ONE more batch, then re-evaluate
  5. If user says "stop" or context exhausted: exit gracefully
```

**Rules:**
- NEVER leave a file half-traced or half-executed — complete the current file before checkpointing
- ALWAYS write state to disk before yielding — unsaved progress is lost
- The batch sizes (5 for trace, 20 for compile) are defaults — adjust downward if files are very large (>500 lines) or context is tight

## Batch Mode Output

In batch mode, the conversion report includes:
- **Aggregate compilation status** (X/Y files compiled, Z failures)
- **Per-phase summary table** (not per-file — group by pipeline phase)
- **Top error categories** (e.g., "15 files: PROC IMPORT stub", "3 files: PROC TRANSPOSE manual")
- **Single consolidated DAG** (not per-file DAGs)
- **Single orchestration recommendation** with full Tasks DAG SQL

---

## Step 8a: Batch-Mode Compilation (when target tables do not exist)

When compiling against an empty schema (greenfield migration), target tables referenced in FROM/JOIN clauses will not exist. Use stub tables to unblock compilation:

1. **Scan all output `.sql` files** for table references in FROM, JOIN, and IDENTIFIER() clauses
2. **Build a dependency-ordered list** of tables — tables created by earlier scripts are inputs to later scripts
3. **For each referenced table not yet created by a prior script**:
   - Infer column names and types from the SELECT that populates it upstream (CREATE TABLE AS SELECT)
   - If no upstream definition exists (external source table), generate a stub using `references/schema-inference.md`
   - Prepare the stub DDL: `CREATE TABLE IF NOT EXISTS <schema>.<table> (<col1> VARIANT, ...)`
4. **Confirm stub creation (per Snowflake Interaction Policy):**
   ```
   SNOWFLAKE OBJECT CREATION

   Action: Create [N] temporary stub tables for compilation
   Schema: TARGET_SCHEMA
   Tables:
     - STUB_TABLE_1
     - STUB_TABLE_2
     - ...
   Purpose: Scaffolding only -- will be dropped after compilation
   Credit impact: Minimal

   Proceed? [Yes] / [No - Skip stub compilation] / [Show DDL]
   ```
5. If approved: **execute stubs in dependency order** (using the DAG from Step 10)
6. If declined: skip stub creation and compile without stubs (expect missing-table errors)
7. **Compile each `.sql` file** with `only_compile=true`
8. **Record pass/fail per file** — include in the conversion report (Section 1 Compilation Status column)
9. **Confirm stub cleanup:**
   ```
   SNOWFLAKE CLEANUP

   Action: Drop [N] stub tables created for compilation
   Tables:
     - STUB_TABLE_1
     - STUB_TABLE_2
     - ...

   Proceed? [Yes - Drop All] / [No - Keep for debugging]
   ```
10. If approved: **drop all stub tables** (they were scaffolding only)
11. If declined: keep stubs for user inspection

```sql
-- Stub table pattern (when column types cannot be inferred)
CREATE TABLE IF NOT EXISTS TARGET_SCHEMA.SOURCE_TABLE (
  _STUB_COL VARIANT
);
-- NOTE: This stub exists only for compilation. Drop after validation.
```

**Batch compilation rules:**
- Do NOT stop on first failure — compile ALL files and report aggregate results
- Group compilation errors by type (missing table, syntax error, type mismatch)
- If >80% of files compile successfully, report as PASS with exceptions listed
- If <80% compile, flag as WARNING and list the top error categories
