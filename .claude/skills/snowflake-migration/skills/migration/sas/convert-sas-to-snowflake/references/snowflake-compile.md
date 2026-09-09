# Snowflake Compilation Module

## When to Load

Load this file when Phase 3 (Snowflake Compilation) is selected in the Validation Pipeline. This module handles compile-only testing with auto-creation of temporary environments when the target schema does not exist.

---

## Explicit Prompt (ALWAYS Required — Never Auto-Propagated)

Before ANY Snowflake interaction, present:

```
VALIDATION PHASE 3: Snowflake Compilation (Credits Will Be Consumed)

Action: Compile [N] .sql files with only_compile=true (dry-run syntax check)
Target schema: [TARGET_DB].[TARGET_SCHEMA]
Schema status: [EXISTS / DOES NOT EXIST]

If schema does not exist:
  → Will create temporary database: [TARGET_DB]_COMPILE_[YYYYMMDD]
  → Will load source tables from source_table_ddl.sql
  → Will populate with synthetic data for type-checking context
  → Will drop temporary database after compilation

Credit impact: MINIMAL (compilation metadata only, no data processing)

Proceed? [Yes - Compile] / [No - Skip] / [Show compilation plan]
```

**This prompt fires EVERY time Phase 3 runs** — regardless of any prior validation menu selection. Selecting Phase 3 in the menu indicates intent; this prompt confirms the action.

---

## Compilation Workflow

### Step 1: Probe Compilation

Compile ONE simple file (smallest Tier 1) to check environment readiness:

```python
# Select the smallest .sql file as probe
probe_file = min(sql_files, key=lambda f: os.path.getsize(os.path.join(output_dir, f)))
```

Execute with `snowflake_sql_execute(sql=probe_content, only_compile=true)`

**Interpret probe result:**
- SUCCESS → environment ready, proceed to Step 3
- ERROR "Database does not exist" → proceed to Step 2 (Auto-Create)
- ERROR "Schema does not exist" → proceed to Step 2 (Auto-Create)
- ERROR "Object does not exist" (table-level) → proceed to Step 2 (load stubs)
- ERROR (other) → log error, attempt with next file

### Step 2: Auto-Create Temporary Compilation Environment

When the target schema does not exist, create a temporary environment:

```sql
-- 2a. Create temporary database (timestamped to avoid conflicts)
CREATE DATABASE IF NOT EXISTS <TARGET_DB>_COMPILE_<YYYYMMDD>;

-- 2b. Set context
USE DATABASE <TARGET_DB>_COMPILE_<YYYYMMDD>;

-- 2c. Create target schema
CREATE SCHEMA IF NOT EXISTS <TARGET_SCHEMA>;

-- 2d. Set schema context
USE SCHEMA <TARGET_DB>_COMPILE_<YYYYMMDD>.<TARGET_SCHEMA>;
```

Then load source tables and synthetic data:

```sql
-- 2e. Execute source_table_ddl.sql (all CREATE TABLE IF NOT EXISTS)
-- 2f. Execute synthetic_data.sql (provides type context for compilation)
```

**Record in state:**
```json
{
  "compilation_env": {
    "type": "temporary",
    "database": "<TARGET_DB>_COMPILE_<YYYYMMDD>",
    "schema": "<TARGET_SCHEMA>",
    "created_at": "<ISO timestamp>"
  }
}
```

### Step 3: Compile All Files

For each .sql file in the output directory:

```python
results = []
for sql_file in sorted(sql_files):
    with open(os.path.join(output_dir, sql_file)) as f:
        sql_content = f.read()
    
    # If using temp environment, rewrite schema references
    if using_temp_env:
        sql_content = sql_content.replace(
            f"{target_db}.{target_schema}.",
            f"{temp_db}.{target_schema}."
        )
    
    # Compile
    result = snowflake_sql_execute(sql=sql_content, only_compile=True)
    
    if result.success:
        results.append({"file": sql_file, "status": "PASS"})
    else:
        results.append({
            "file": sql_file,
            "status": "FAIL",
            "error": result.error_message,
            "error_line": result.error_line
        })
```

**Do NOT stop on first failure** — compile ALL files and report aggregate results.

### Step 4: Fix-and-Retry Loop (Max 3 Attempts Per File)

For each failed file:

1. Parse error message
2. Map to known fix patterns:

| Error Pattern | Auto-Fix |
|--------------|----------|
| Unknown function X | Check function-mappings.md, replace |
| Invalid identifier | Check for SAS macro variable or vendor syntax |
| Syntax error near X | Check Snowflake Scripting rules |
| Object does not exist | Add TEMPORARY or check dependency order |
| Type mismatch | Add explicit CAST |
| Unexpected keyword | Quote identifier with double quotes |
| Missing column | Verify against source DDL |

3. Apply fix to .sql file on disk
4. Re-compile
5. If PASS: record success with fix details
6. If FAIL after 3 attempts: record as FAILED_AFTER_RETRIES

### Step 5: Write Compilation Results

```python
import json
from datetime import datetime

compilation_results = {
    "compiled_at": datetime.now().isoformat(),
    "environment": "temporary" if using_temp_env else "existing",
    "total_files": len(results),
    "passed": sum(1 for r in results if r["status"] == "PASS"),
    "failed": sum(1 for r in results if r["status"] != "PASS"),
    "pass_rate": f"{sum(1 for r in results if r['status'] == 'PASS') / len(results) * 100:.1f}%",
    "failures": [r for r in results if r["status"] != "PASS"],
    "fixes_applied": [r for r in results if r.get("fix_applied")]
}

with open(os.path.join(output_dir, "compilation_results.json"), "w") as f:
    json.dump(compilation_results, f, indent=2)
```

### Step 6: Cleanup Temporary Environment

If a temporary environment was created:

```
COMPILATION COMPLETE — Cleanup

Results: [PASSED]/[TOTAL] files compiled successfully
Temporary database: [TEMP_DB_NAME]

Drop temporary compilation database? [Yes - Drop] / [No - Keep for debugging]
```

If Yes:
```sql
DROP DATABASE IF EXISTS <TEMP_DB_NAME>;
```

Update state: `compilation_env.dropped: true`

---

## Resume Behavior

If `conversion_state.json` shows `compilation_env` is non-null and `dropped` is false:
- The temp environment already exists from a prior session
- Skip Steps 1-2, proceed directly to Step 3 (compile remaining files)
- Check per-file `compilation_status` to skip already-compiled files

---

## HARD GATE (Phase 3)

```python
import os, sys, json
output_dir = "<output_dir>"
results_path = os.path.join(output_dir, "compilation_results.json")
if not os.path.exists(results_path):
    print("BLOCKED: compilation_results.json does not exist")
    sys.exit(1)
with open(results_path) as f:
    results = json.load(f)
print(f"Phase 3 GATE PASSED: {results['passed']}/{results['total_files']} compiled")
```

Update `conversion_state.json`: `gates.phase_3_snowflake_compile: "PASSED"`
