# Validation Pipeline (Modular)

## When to Load

Load this file IMMEDIATELY after Step 6a passes (all .sql artifacts verified on disk). This is the single orchestrator for ALL validation phases.

---

## Two-Tier Consent Gate (MANDATORY — replaces opt-in menu)

Validation runs **end-to-end by default** once the user consents. There are only TWO prompts, gated by cost. The user does NOT hand-pick individual phases.

### Tier-1 Gate (Zero Cost) — present after Step 6a

```
VALIDATION — Tier 1 (Zero Cost, runs locally)

This will automatically run:
  Phase 1: Synthetic Data Generation (DDL + aligned synthetic data)
  Phase 2: LLM SAS Logic Trace (expected output baselines)

No Snowflake credits consumed. Recommended for every conversion.

Proceed? [Yes - run local validation (recommended)] / [Skip all validation]
```

- **Yes** → run Phase 1, then Phase 2, automatically (no prompt between them). Record `validation_selections.tier1_approved: true`.
- **Skip all validation** → set all gates to `SKIPPED`, append checkpoint, go straight to Step 10.

### Tier-2 Gate (Snowflake Credits) — present after Phase 2 completes

```
VALIDATION — Tier 2 (Snowflake Credits)

Local validation complete. The next stage runs the full pipeline ON Snowflake:
  Phase 3: Compilation (all files, only_compile — MINIMAL credits)
  Phase 4: Execution of Tier 2/3 stored procedures (MODERATE credits)
  Phase 5: Integration + End-to-End orchestration test (MODERATE credits)
           - generates a reusable orchestration harness on disk
           - runs the entire pipeline in DAG order
           - asserts terminal output tables are non-empty
           - compares terminal outputs to Phase 2 baselines

Credit impact: MODERATE (warehouse active for compile + execute + E2E run)

Proceed? [Yes - run full Snowflake validation end-to-end] / [No - stop after local] / [Show plan]
```

- **Yes** → run Phase 3 → Phase 4 → Phase 5 automatically, **no further per-phase prompts** (consent propagates across all three credit phases). Record `validation_selections.tier2_approved: true`. Each phase still enforces its HARD GATE.
- **No** → set gates 3/4/5 to `SKIPPED`, append checkpoint, go to Step 10.
- **Show plan** → display the file lists / DAG layers that each phase will touch, then re-prompt.

**Consent model rationale:** Tier-1 is always safe (zero credits) so it gets a low-friction prompt. Tier-2 bundles all credit-consuming work behind ONE informed decision — the user does not get nagged once per phase. This matches "run end-to-end by default if the user wants to proceed."

**Checkpoint logging:** at each gate decision, append an `INFO` line to `checkpoint_log.jsonl` recording the consent outcome (e.g. `notes: "Tier-2 gate: approved — Phases 3,4,5 will run"`). See `references/checkpoint-logging.md`.

**Phase 1 always runs** when Tier-1 is approved — DDL + synthetic data are prerequisites for all other phases.


---

## Phase 1: Synthetic Data Generation (Always Runs)

**Load:** `references/schema-inference.md` + `references/synthetic-data-rules.md`

### 1.1 Generate Source Table DDL

Parse all converted .sql files and original .sas files to identify source tables (tables read but never created). For each, infer columns and types using the schema inference rules.

Write to: `<output_dir>/source_table_ddl.sql`

Format:
```sql
-- Auto-generated source table DDL for validation testing
-- Tables listed are external inputs (read but not created by converted SQL)
CREATE TABLE IF NOT EXISTS <TABLE_NAME> (
  <COL1> <TYPE>,
  <COL2> <TYPE>
);
```

### 1.2 Generate Synthetic Data

For each source table, generate INSERT statements following `references/synthetic-data-rules.md`:
- Batch mode (10+ files): Use GENERATOR(ROWCOUNT => 50) for Snowflake
- Interactive mode (<10 files): Use 5-8 rows via INSERT VALUES

Write to: `<output_dir>/synthetic_data.sql`

### 1.3 HARD GATE (Phase 1)

```python
import os, sys
output_dir = "<output_dir>"
required = ["source_table_ddl.sql", "synthetic_data.sql"]
missing = [f for f in required if not os.path.exists(os.path.join(output_dir, f))]
if missing:
    print(f"BLOCKED: Phase 1 artifacts missing: {missing}")
    sys.exit(1)
print("Phase 1 GATE PASSED")
```

**The LLM MUST execute this gate script via Bash tool.** State cannot progress until exit code 0.

Update `conversion_state.json`: `gates.phase_1_synthetic_data: "PASSED"`

---

## Phase 2: LLM SAS Logic Trace (Zero Credits)

**Load:** `references/validation-execution.md` Phase 3A

### 2.1 Explicit Prompt

```
VALIDATION PHASE 2: LLM SAS Logic Trace (Zero Credits)

Action: Trace original SAS logic row-by-row against synthetic data
Files in scope: [N] (batch: 10-15 representative / interactive: all)
Output: tests/<file>/expected/expected_<table>.csv
Cost: Zero (runs locally — no Snowflake interaction)

Run LLM trace? [Yes (recommended)] / [Skip]
```

If user selects Skip: set `gates.phase_2_trace_artifacts: "SKIPPED"`, proceed to Phase 3 prompt.

### 2.2 File Selection (Batch Mode)

For batch (10+ files), select 10-15 representative files covering:
- 2-3 anti-join validation patterns
- 2-3 GROUP BY / aggregation patterns
- 2-3 multi-table JOIN + UNION ALL
- 1-2 CASE expression / product mapping
- 1-2 window function / ROW_NUMBER dedup
- 1-2 complex multi-step (>3 blocks)

### 2.3 Trace Execution (Per File)

For EACH file in scope:

1. **Read** the original .sas source file
2. **Read** the synthetic data rows for all source tables used by this file
3. **Trace** SAS logic row-by-row:
   - DATA Step: Initialize PDV, apply SAS missing semantics, track RETAIN, FIRST./LAST.
   - PROC SQL: Standard SQL semantics, NULL propagation
   - MERGE: NOT equivalent to JOIN — interleave within BY-groups
4. **Present** expected output as a visible table:
   ```
   TRACE: <filename>.sas
   Input tables: TABLE_A (N rows), TABLE_B (M rows)
   Logic summary: [brief description of what the SAS does]
   
   Expected output (<OUTPUT_TABLE>):
   | COL1 | COL2 | COL3 |
   |------|------|------|
   | val  | val  | val  |
   ```
5. **Write** expected output to CSV:
   ```python
   import os, csv
   test_dir = os.path.join(output_dir, "tests", file_stem, "expected")
   os.makedirs(test_dir, exist_ok=True)
   with open(os.path.join(test_dir, f"expected_{output_table}.csv"), "w", newline="") as f:
       writer = csv.writer(f)
       writer.writerow(columns)
       writer.writerows(data)
   ```
6. **Verify** the file was written (read it back):
   ```python
   assert os.path.exists(csv_path) and os.path.getsize(csv_path) > 0
   ```

### 2.4 Batch Processing (Context-Aware)

Process in batches of 5 files. After each batch:
- Write state: move files from `files_remaining` to `files_traced`
- If context nearing limit: save state, inform user, exit gracefully

### 2.5 HARD GATE (Phase 2) — BLOCKING

After ALL files traced, execute this verification:

```python
import os, sys
output_dir = "<output_dir>"
traced_files = [<files from trace_progress.files_traced>]
missing = []
for f in traced_files:
    stem = f.replace(".sas", "")
    expected_dir = os.path.join(output_dir, "tests", stem, "expected")
    if not os.path.isdir(expected_dir):
        missing.append(f"{stem}: expected/ directory missing")
    else:
        csvs = [x for x in os.listdir(expected_dir) if x.endswith(".csv")]
        if not csvs:
            missing.append(f"{stem}: no .csv files in expected/")
        else:
            for csv_file in csvs:
                size = os.path.getsize(os.path.join(expected_dir, csv_file))
                if size == 0:
                    missing.append(f"{stem}/{csv_file}: empty file (0 bytes)")
if missing:
    print(f"BLOCKED: Phase 2 artifacts missing or empty:")
    for m in missing:
        print(f"  - {m}")
    sys.exit(1)
print(f"Phase 2 GATE PASSED: {len(traced_files)} files verified")
```

**The LLM MUST execute this gate script.** If exit code != 0: re-trace missing files.

Update `conversion_state.json`: `gates.phase_2_trace_artifacts: "PASSED"`, `gates.phase_2_csv_count: <count>`

---

## Phase 3: Snowflake Compilation (CREDITS — covered by Tier-2 consent)

**Load:** `references/snowflake-compile.md`

### 3.1 Consent

Phase 3 runs automatically when the Tier-2 gate was approved (`validation_selections.tier2_approved: true`) — do NOT re-prompt per phase. If Tier-2 was NOT approved, this phase does not run (gate = `SKIPPED`).

Append checkpoint: `step:"phase_3" status:"STARTED"`.

### 3.2 Execution

Follow `references/snowflake-compile.md`:
1. Probe: compile one simple file
2. If target schema missing: auto-create temp environment
3. Compile all files
4. Fix-and-retry loop (max 3 per file)
5. Write `compilation_results.json`
6. Drop temp environment (if created)

### 3.3 HARD GATE (Phase 3)

Verify `compilation_results.json` exists with per-file results.

Update `conversion_state.json`: `gates.phase_3_snowflake_compile: "PASSED"`

---

## Phase 4: Snowflake Execution — Tier 2/3 (CREDITS — covered by Tier-2 consent)

**Load:** `references/snowflake-execution.md`

### 4.1 Consent

Phase 4 runs automatically when the Tier-2 gate was approved — do NOT re-prompt per phase. If Tier-2 was NOT approved, gate = `SKIPPED`.

Append checkpoint: `step:"phase_4" status:"STARTED"`.

### 4.2 Execution

Follow `references/snowflake-execution.md`:
1. Create temp tables from source_table_ddl.sql
2. Load synthetic data
3. Execute each Tier 2/3 file
4. Capture outputs
5. Compare against expected baselines
6. Write `snowflake_execution_results.json`
7. Drop all temp objects

### 4.3 HARD GATE (Phase 4)

Verify `snowflake_execution_results.json` exists.

Update `conversion_state.json`: `gates.phase_4_snowflake_execute: "PASSED"`. Append checkpoint `step:"phase_4" gate:"phase_4_snowflake_execute" status:"PASSED"`.

---

## Phase 5: Integration & End-to-End Orchestration Test (CREDITS — covered by Tier-2 consent)

**Load:** `references/e2e-orchestration-test.md`

Phase 4 executes Tier 2/3 procedures in *isolation* (each with its own mini dependency chain). Phase 5 is different: it runs the **entire pipeline in topological DAG order as one integrated flow**, generates a **reusable orchestration harness on disk**, and asserts that **terminal output tables are non-empty**. This is the test that proves the conversion works end-to-end — not just that individual files compile/run.

### 5.1 Consent

Phase 5 runs automatically when the Tier-2 gate was approved — do NOT re-prompt. If Tier-2 was NOT approved, gate = `SKIPPED`.

Append checkpoint: `step:"phase_5" status:"STARTED"`.

### 5.2 Execution

Follow `references/e2e-orchestration-test.md`:
1. Topologically sort all converted files from the cross-file DAG into layers.
2. Generate the reusable harness: `orchestration/sp_e2e_pipeline.sql`, `orchestration/task_dag.sql`, `orchestration/adf_pipeline.sql`, `testing/setup_test_data.sql`, `testing/expected_results.sql`.
3. Load aligned synthetic data, execute the master E2E procedure in DAG order.
4. Assert `steps_failed = 0` AND every terminal table is non-empty (or its empty source is justified).
5. Compare terminal outputs to Phase 2 baselines.
6. Write `e2e_test_results.json`.

### 5.3 HARD GATE (Phase 5)

Verify `e2e_test_results.json` exists and `orchestration/sp_e2e_pipeline.sql` was written.

Update `conversion_state.json`: `gates.phase_5_e2e_orchestration: "PASSED"`. Append checkpoint `step:"phase_5" gate:"phase_5_e2e_orchestration" status:"PASSED"`.

---

## Phase Completion → Step 10

After all approved phases complete (or are skipped):
- Proceed to Step 10 (Report Generation) in `workflows/steps-8-10-post-conversion.md`
- The report reads all gate statuses and artifact files (including `e2e_test_results.json`) to populate validation sections

---

## State Schema

```json
{
  "validation_selections": {
    "tier1_approved": true,
    "tier2_approved": false
  },
  "gates": {
    "phase_1_synthetic_data": "PASSED|BLOCKED|NOT_RUN",
    "phase_2_trace_artifacts": "PASSED|BLOCKED|SKIPPED|NOT_RUN",
    "phase_2_csv_count": 0,
    "phase_3_snowflake_compile": "PASSED|BLOCKED|SKIPPED|NOT_RUN",
    "phase_4_snowflake_execute": "PASSED|BLOCKED|SKIPPED|NOT_RUN",
    "phase_5_e2e_orchestration": "PASSED|BLOCKED|SKIPPED|NOT_RUN"
  },
  "trace_progress": {
    "total_files_in_scope": 15,
    "files_traced": [],
    "files_remaining": [],
    "batch_size": 5,
    "concerns_found": []
  },
  "execution_progress": {
    "files_executed": [],
    "files_remaining": [],
    "batch_size": 5
  }
}
```

---

## Resume Behavior

When a new context window starts and validation is incomplete:
1. Read `conversion_state.json`
2. Check each gate status
3. Resume from the earliest phase with status != "PASSED" and != "SKIPPED"
4. If mid-phase (trace_progress / execution_progress has files_remaining): continue from there
5. Re-present the relevant TIER gate (Tier-1 or Tier-2) before continuing if consent was not yet recorded
6. `checkpoint_log.jsonl` is informational for the resume — read its last line to show the user where the prior session stopped
