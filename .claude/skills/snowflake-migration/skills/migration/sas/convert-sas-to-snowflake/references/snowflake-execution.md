# Snowflake Execution Module (Tier 2/3 Only)

## When to Load

Load this file when Phase 4 (Snowflake Execution) is selected in the Validation Pipeline. Executes stored procedures and converted SQL against synthetic data on Snowflake.

---

## Prerequisite Checks

Before this phase can execute:
1. Phase 3 (Snowflake Compilation) must have PASSED for the target Tier 2/3 files
2. `source_table_ddl.sql` exists (from Phase 1)
3. `synthetic_data.sql` exists (from Phase 1)
4. Phase 2 expected baselines exist for the target files (recommended)

---

## Explicit Prompt (ALWAYS Required — Never Auto-Propagated)

```
VALIDATION PHASE 4: Snowflake Execution — Tier 2/3 Only (Credits Will Be Consumed)

Action: Execute [N] stored procedures / PySpark notebooks against synthetic data
Files:
  [list each Tier 2/3 file with name and tier classification]
  
Warehouse: [current warehouse name]
Credit impact: MODERATE (actual SQL execution, warehouse will be active)

This will:
  1. Create temporary tables with synthetic data in [SCHEMA]
  2. Execute each stored procedure via CALL
  3. Capture output tables produced by each SP
  4. Compare output against Phase 2 expected baselines
  5. Drop ALL temporary objects after completion

Proceed? [Yes - Execute on Snowflake] / [No - Skip Tier 2/3 testing] / [Show execution plan]
```

**This prompt fires EVERY time Phase 4 runs** — no consent propagation override exists for actual SQL execution.

---

## Execution Workflow

### Step 1: Prepare Temporary Environment

If a compilation environment still exists from Phase 3 (not dropped), reuse it.
Otherwise, create fresh:

```sql
-- Create or reuse temp schema
CREATE DATABASE IF NOT EXISTS <TARGET_DB>_VALIDATE_<YYYYMMDD>;
USE DATABASE <TARGET_DB>_VALIDATE_<YYYYMMDD>;
CREATE SCHEMA IF NOT EXISTS <TARGET_SCHEMA>;
USE SCHEMA <TARGET_DB>_VALIDATE_<YYYYMMDD>.<TARGET_SCHEMA>;
```

### Step 2: Load Source Tables and Synthetic Data

```sql
-- Execute source_table_ddl.sql (creates all source tables)
-- Execute synthetic_data.sql (populates with test data)
```

### Step 3: Create Intermediate Tables (Dependency Chain)

Tier 2/3 files often depend on output from earlier Tier 1 files. For each Tier 2/3 file:
1. Identify its input dependencies (tables it reads from)
2. If those tables are outputs of Tier 1 files: execute those Tier 1 files first (in dependency order) to populate the intermediate tables
3. This ensures the SP has realistic input data

```python
# Build dependency chain for each Tier 2/3 file
for tier23_file in tier23_files:
    dependencies = get_file_dependencies(tier23_file)
    tier1_deps = [d for d in dependencies if d in tier1_files]
    
    # Execute Tier 1 dependencies first (in order)
    for dep in topological_sort(tier1_deps):
        execute_sql_file(dep)
```

### Step 4: Execute Tier 2 (Stored Procedures)

For each Tier 2 file:

```sql
-- The .sql file contains CREATE OR REPLACE PROCEDURE ... + CALL
-- Execute the entire file (creates + calls the SP)
```

After execution:
- Identify output tables (tables created/modified by the SP)
- SELECT * FROM each output table → write to `tests/<file>/actual/<table>.csv`

### Step 5: Execute Tier 3 (PySpark/SCOS Notebooks)

For each Tier 3 file:
- If `.ipynb`: execute notebook cells against the Snowflake session
- If `.py`: execute the Python script with Snowpark Connect

After execution:
- Identify output tables
- SELECT * FROM each → write to CSV

### Step 6: Compare Against Expected Baselines

```python
import pandas as pd, os, json

comparison_results = []

for file_info in tier23_files:
    file_stem = file_info["name"].replace(".sql", "")
    expected_dir = os.path.join(output_dir, "tests", file_stem, "expected")
    actual_dir = os.path.join(output_dir, "tests", file_stem, "actual")
    
    if not os.path.isdir(expected_dir):
        comparison_results.append({
            "file": file_info["name"],
            "status": "NO_BASELINE",
            "note": "Phase 2 trace not run for this file"
        })
        continue
    
    file_pass = True
    mismatches = []
    
    for expected_csv in os.listdir(expected_dir):
        if not expected_csv.endswith(".csv"):
            continue
        table_name = expected_csv.replace("expected_", "").replace(".csv", "")
        actual_csv_path = os.path.join(actual_dir, f"{table_name}.csv")
        
        if not os.path.exists(actual_csv_path):
            mismatches.append(f"{table_name}: no actual output")
            file_pass = False
            continue
        
        expected_df = pd.read_csv(os.path.join(expected_dir, expected_csv))
        actual_df = pd.read_csv(actual_csv_path)
        
        # Schema comparison
        if set(expected_df.columns) != set(actual_df.columns):
            mismatches.append(f"{table_name}: column mismatch")
            file_pass = False
        
        # Row count comparison
        if len(expected_df) != len(actual_df):
            mismatches.append(f"{table_name}: row count {len(actual_df)} vs expected {len(expected_df)}")
            file_pass = False

        # Trivial-pass detection: empty expected AND empty actual is NOT a real pass.
        # It usually means an upstream join produced zero rows (e.g. range/unit mismatch).
        if len(expected_df) == 0 and len(actual_df) == 0:
            mismatches.append(f"{table_name}: TRIVIAL_PASS — both expected and actual are empty (0 rows). "
                              f"Verify upstream joins actually produced data; check range-join/unit alignment.")
            # Do not set file_pass=False, but surface as WARNING so it is never silently green.

        # Value comparison (with tolerance for numerics)
        # Apply comparison rules from references/comparison-rules.md
    
    comparison_results.append({
        "file": file_info["name"],
        "tier": file_info["tier"],
        "status": "PASS" if file_pass else "FAIL",
        "trivial_pass": any("TRIVIAL_PASS" in m for m in mismatches),
        "mismatches": mismatches
    })
```

### Step 6b: Non-Empty Output Assertion

For each file that creates a **terminal** or otherwise expected-to-be-populated output table, assert it produced rows. A SP that runs cleanly but writes 0 rows is a likely defect, not a pass.

```python
# After execution, count rows in each output table
for tbl in output_tables_of(file_info):
    n = run_scalar(f"SELECT COUNT(*) FROM {schema}.{tbl}")
    if n == 0:
        # Distinguish justified empties (genuinely empty source) from defects
        empty_source = first_empty_upstream(tbl)  # walk reads[] chain
        comparison_results.append({
            "file": file_info["name"], "table": tbl,
            "status": "EMPTY_JUSTIFIED" if empty_source else "EMPTY_DEFECT",
            "empty_source": empty_source,
            "note": f"output table {tbl} has 0 rows"
        })
```

`EMPTY_DEFECT` (empty despite populated sources) almost always indicates a join that did not overlap — re-check range-join / unit-consistency in the synthetic data (`references/synthetic-data-rules.md`).

### Step 7: Write Results

```python
sf_results = {
    "executed_at": datetime.now().isoformat(),
    "warehouse": "<warehouse_name>",
    "total_files": len(tier23_files),
    "passed": sum(1 for r in comparison_results if r["status"] == "PASS"),
    "failed": sum(1 for r in comparison_results if r["status"] == "FAIL"),
    "no_baseline": sum(1 for r in comparison_results if r["status"] == "NO_BASELINE"),
    "results": comparison_results
}

with open(os.path.join(output_dir, "snowflake_execution_results.json"), "w") as f:
    json.dump(sf_results, f, indent=2)
```

### Step 8: Cleanup

```sql
-- Drop all temporary objects
DROP DATABASE IF EXISTS <TARGET_DB>_VALIDATE_<YYYYMMDD>;
```

Present cleanup confirmation:
```
PHASE 4 COMPLETE — Cleanup

Results: [PASSED]/[TOTAL] Tier 2/3 files validated
Temporary database: [TEMP_DB_NAME]

Drop temporary execution database? [Yes - Drop] / [No - Keep for debugging]
```

---

## Modular Execution (Context-Aware — prevents timeouts)

Executing dozens of files (deploy + CALL each) in one pass exhausts context and causes subagent timeouts. Process in layer-batches with checkpoint resume — the same pattern used for Phase 2 tracing.

1. Order files by dependency layer (Layer 0 → terminal). Initialize `execution_progress` in `conversion_state.json`:
   ```json
   {"execution_progress": {"files_executed": [], "files_remaining": ["<all files in layer order>"], "batch_size": 5}}
   ```
2. Execute in batches of ~5 files (respecting layer order — never run a file before its dependencies):
   - Deploy + CALL each file in the batch
   - Capture outputs, run comparison + non-empty assertion
   - Move each file from `files_remaining` to `files_executed`
   - Update `conversion_state.json` AND append a checkpoint line (`step:"phase_4" status:"INFO" notes:"batch N executed"`)
3. After each batch, check context budget:
   - Sufficient → continue to next batch
   - Nearing limit → write `snowflake_execution_results.json` (partial), save state, inform user, exit gracefully
4. Resume: read `execution_progress`, skip `files_executed`, continue from `files_remaining`.

When delegating to subagents, give each subagent ONE layer-batch (not the whole pipeline) so no single agent runs more than ~5 files.

---

## HARD GATE (Phase 4)

```python
import os, sys, json
output_dir = "<output_dir>"
results_path = os.path.join(output_dir, "snowflake_execution_results.json")
if not os.path.exists(results_path):
    print("BLOCKED: snowflake_execution_results.json does not exist")
    sys.exit(1)
with open(results_path) as f:
    results = json.load(f)
print(f"Phase 4 GATE PASSED: {results['passed']}/{results['total_files']} Tier 2/3 files validated")
```

Update `conversion_state.json`: `gates.phase_4_snowflake_execute: "PASSED"`

---

## Files That Require Phase 4

These are identified during Step 3 (Classification) and recorded in `conversion_state.json`:

| Classification | Reason | Phase 4 Required |
|---------------|--------|-----------------|
| Tier 2 SP | Stored procedures with DECLARE/BEGIN/END | Yes |
| Tier 3 SCOS | PySpark notebooks | Yes |
| Compilation FAILED | Files that failed compilation in Phase 3 | Yes |

The validation summary from Phase 3 (`compilation_results.json`) identifies files that failed compilation — those may need manual review before Phase 4 execution.
