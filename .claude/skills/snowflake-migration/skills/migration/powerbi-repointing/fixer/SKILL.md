---
name: powerbi-fixer
description: "Complete SnowConvert Power BI repointing by fixing unsupported queries using LLM-based translation. Triggers: finish repointing, complete pbit migration, fix unsupported queries, power bi snowflake migration."
parent_skill: migration
license: Proprietary. See License-Skills for complete terms
---

# Fix Unsupported Power BI Queries

Complete the SnowConvert Power BI repointing process by converting "Unsupported" queries to Snowflake-compatible Power Query (M) code.

**Important**: Snowflake connection details (account, warehouse, database) are automatically extracted from PBIT parameters (`SF_SERVER_LINK`, `SF_WAREHOUSE_NAME`, `SF_DB_NAME`). Do NOT ask the user for these values.

## External Scripts

This skill uses external scripts in the `scripts/` directory and MCP tool modes:

- **Python scripts**: `extract-pbit.py`, `verify-output.py`, `verify-parameters.py`, `extract-current-pbit.py`, `prepare-queries-for-llm.py`, `reassemble-pbit.py`, `display-results.py`, `update-assessment-report.py`
- **MCP tool**: `pbit_repointing` (Rust, in the `snowflake-migration` MCP server) with modes: `apply_translations`, `build_inventory`, `cleanup`

All scripts use only standard library and run cross-platform (macOS / Linux / Windows). Intermediate files live under `<project_dir>/artifacts/pbit/` (set via `SCAI_PROJECT_DIR` env var).

## Parameters

| Parameter | Description | Source |
|-----------|-------------|--------|
| `<OUTPUT_FOLDER>` | Project root containing `artifacts/` and `reports/` | Auto-detected from MCP `configure` → `project_dir` |
| `<SOURCE_DIALECT>` | Source SQL dialect for translation | Auto-detected from MCP `configure` → `source_language` |
| `<SNOWFLAKE_ACCOUNT>` | Snowflake account identifier | Parameter reference in PBIT (`SF_SERVER_LINK`) |
| `<SNOWFLAKE_WAREHOUSE>` | Warehouse name | Parameter reference in PBIT (`SF_WAREHOUSE_NAME`) |
| `<SNOWFLAKE_DATABASE>` | Target database | Parameter reference in PBIT (`SF_DB_NAME`) |
| `<SNOWFLAKE_ROLE>` | Optional Snowflake role | Parameter reference in PBIT (`SF_ROLE`) — auto-injected if missing |

**Critical**:
- **DO NOT ask** the user for: Output folder, source dialect, Snowflake account, warehouse, database, or schema values
- All values are auto-detected from the MCP session configuration or extracted from the PBIT file

**SF_* Parameters May Be Empty**: The parameters in the PBIT file may have no value (empty/null). This is intentional — users fill these when opening the report in Power BI. The skill references these parameters in converted queries, never hard-codes values.

## Workflow Checklist

```
[ ] Step 1: Gather Parameters
[ ] Step 2: Build Ordered Inventory by PBIT File
[ ] Step 3: Process Each PBIT File (One File at a Time)
    [ ] 3a. Clean and Extract PBIT
    [ ] 3b. Verify Parameters
    [ ] 3c. Prepare Queries for LLM
    [ ] 3d. LLM Translation
    [ ] 3e. Apply Translations (MCP tool)
    [ ] 3f. Reassemble PBIT
    [ ] 3g. Update Assessment Report (MANDATORY)
    [ ] 3h. Verify Output
[ ] Step 4: Present Final Summary
```

### Step 1: Gather Parameters

Read the MCP `configure` response (call `configure()` with no params if not in context):
- `project_dir` → `<OUTPUT_FOLDER>`
- `source_language` → `<SOURCE_DIALECT>`

Only fall back to asking the user if `configure` returns no `project_dir`.

**Environment setup**: All `uv run scripts/` commands below require the project directory to be set:
```bash
export SCAI_PROJECT_DIR="<OUTPUT_FOLDER>"
```
This ensures all scripts write intermediate files to `<project_dir>/artifacts/pbit/` rather than the system temp directory.

### Step 2: Build Ordered Inventory by PBIT File

Find the SnowConvert report:
```bash
find <OUTPUT_FOLDER> -path "*/reports/SnowConvert/ETLAndBiRepointing*.csv" -type f
```

Build inventory using the MCP tool:
```
pbit_repointing(
  mode: "build_inventory",
  report_csv_path: "<report_path>",
  output_folder: "<OUTPUT_FOLDER>"
)
```

This filters for `Status = Unsupported`, groups by PBIT file, and returns JSON inventory.

**STOPPING POINT**: Display the inventory:
```
Found M PBIT files with unsupported queries:

1. A.pbit - 2 unsupported queries:
   - Query "X"
   - Query "Y"

Total: N unsupported queries in M files
Note: All other queries already converted by SnowConvert will not be modified.
```

Ask for confirmation before proceeding.

### Step 3: Process Each PBIT File (Sub-Agent Dispatch)

**CRITICAL**:
- Process PBIT files sequentially, one complete file at a time
- Complete ALL substeps for one PBIT before starting the next
- ONLY modify "Unsupported" queries — all others remain exactly as SnowConvert converted them

For each PBIT file in the inventory, dispatch a sub-agent with the full context needed to process it autonomously. This preserves main session context.

#### Sub-Agent Dispatch

For each PBIT file, dispatch a Task with this prompt:

```
Read and follow plugin/skills/migration/powerbi-repointing/fixer/SKILL.md.
You are running in sub-agent mode — do NOT ask the user any questions.

Context (from parent):
- project_dir: <absolute_path>
- source_dialect: <SOURCE_DIALECT>
- pbit_file: <pbit_file_name>
- pbit_path: <absolute_pbit_path>
- unsupported_queries: <list_of_query_names>
- report_csv_path: <absolute_report_path>
- scripts_dir: <absolute_scripts_dir>

Execute sub-steps 3a through 3h for this single PBIT file.
Report back JSON only: { "sub_skill": "powerbi-fixer", "pbit_file": "<name>", "status": "ok"|"error", "converted_count": N, "failed_queries": [...], "error": null|"<message>" }
```

Process PBIT files **sequentially** — dispatch one sub-agent, wait for its result, then dispatch the next. Each sub-agent handles one complete PBIT file.

#### Retry Logic

If a sub-agent returns `"status": "error"`, re-dispatch it once with the same context. If it fails again, log the failure and proceed to the next PBIT file.

## Sub-Agent Mode

When running as a sub-agent (prompt contains "sub-agent mode"), execute these steps silently without user interaction:

### On Entry
1. Call `configure()` with the provided `project_dir`
2. Set `SCAI_PROJECT_DIR` environment variable to `project_dir`

### Steps (for a single PBIT file)

#### 3a. Clean Working Directory and Extract PBIT

Clean the working directory via MCP tool:
```
pbit_repointing(
  mode: "cleanup",
  work_dir: "<project_dir>/artifacts/pbit/work"
)
```

Then extract the PBIT:
```bash
uv run scripts/extract-pbit.py "<PBIT_PATH_FROM_INVENTORY>"
```

#### 3b. Verify Parameters

```bash
uv run scripts/verify-parameters.py "<project_dir>/artifacts/pbit/work/DataModelSchema"
```

This verifies `SF_SERVER_LINK`, `SF_WAREHOUSE_NAME`, `SF_DB_NAME` exist and auto-injects `SF_ROLE` if missing. Parameters may be empty — that is expected.

#### 3c. Prepare Queries for LLM Translation

```bash
uv run scripts/extract-current-pbit.py "<CURRENT_PBIT_BASENAME>"
uv run scripts/prepare-queries-for-llm.py "<project_dir>/artifacts/pbit/work/DataModelSchema" "<project_dir>/artifacts/pbit/current_pbit.json"
```

Output: `<project_dir>/artifacts/pbit/queries_for_translation.json`

#### 3d. LLM Translation

For each query in `<project_dir>/artifacts/pbit/queries_for_translation.json`:

1. Read the original PowerQuery expression
2. Identify the source SQL dialect patterns (from `<SOURCE_DIALECT>`)
3. Translate to Snowflake-compatible PowerQuery using:
   - `Value.NativeQuery()` with `Snowflake.Databases()` connector
   - Parameter references: `SF_SERVER_LINK`, `SF_WAREHOUSE_NAME`, `SF_DB_NAME`
   - Source dialect → Snowflake SQL syntax translations

**See `reference/llm-translation-guide.md` for complete translation rules.**
**See `reference/multi-source-translation-guide.md` for multi-connection handling.**

Save all translations to `<project_dir>/artifacts/pbit/translated_queries.json` with this structure per query:
```json
{
  "query_name": "<name>",
  "source_file": "DataModelSchema",
  "translation_status": "completed",
  "translated_expression": "<translated M expression>"
}
```

#### 3e. Apply Translations (MCP Tool)

Call the MCP tool:
```
pbit_repointing(
  mode: "apply_translations",
  work_dir: "<project_dir>/artifacts/pbit/work",
  translated_queries_path: "<project_dir>/artifacts/pbit/translated_queries.json"
)
```

This tool (Rust):
- Reads `DataModelSchema` (UTF-16 LE) and `UnappliedChanges` if present
- Patches each query with its translated expression
- Writes both files back as UTF-16 LE without BOM
- Returns JSON with `converted_count`, `datamodel_converted`, `unapplied_converted`, `success`, `failed_queries`

Save the MCP tool's JSON response to `<project_dir>/artifacts/pbit/conversion_results.json` (used by `display-results.py` in Step 4).

If any queries failed, review the failure reasons and retry translation for those queries.

#### 3f. Reassemble PBIT

```bash
uv run scripts/reassemble-pbit.py "<ORIGINAL_PBIT_PATH>" "<project_dir>/artifacts/pbit/work"
```

Creates `.backup` of the original and replaces it with the updated version.

#### 3g. Update Assessment Report (MANDATORY — NEVER SKIP)

```bash
uv run scripts/update-assessment-report.py <report_path> "<project_dir>/artifacts/pbit/translated_queries.json" "<OUTPUT_FOLDER>"
```

Updates the ETLAndBiRepointing CSV: changes `Status` from "Unsupported" to "AI Repointed" for successfully translated queries.

#### 3h. Verify Output

```bash
uv run scripts/verify-output.py "<ORIGINAL_PBIT_PATH>"
```

Validates the reassembled PBIT is a valid ZIP with DataModelSchema present.

### JSON Return Contract

Return exactly:
```json
{
  "sub_skill": "powerbi-fixer",
  "pbit_file": "<filename>",
  "status": "ok"|"error",
  "converted_count": <number>,
  "failed_queries": [],
  "error": null
}
```

### Step 4: Present Final Summary

```bash
uv run scripts/display-results.py
```

Display the summary including:
- Total queries converted
- Any failed queries
- Path to updated assessment report
- Path to backup files

## Translation Rules Summary

When translating PowerQuery expressions:

1. **Connector**: Replace source-specific connectors with `Snowflake.Databases(SF_SERVER_LINK, SF_WAREHOUSE_NAME, [Role=SF_ROLE, Implementation="2.0"]){[Name=SF_DB_NAME]}[Data]`
2. **SQL**: Wrap in `Value.NativeQuery(<connector>, "<sql>", null, [EnableFolding=true])`
3. **Parameters**: Use Power BI parameter references (not string values)
4. **Dynamic SQL**: Preserve string concatenation with `&` operator for parameterized queries
5. **Column mapping**: Preserve expected column names from the original query
6. **Schema**: Use schema from original connection or default to the table's schema

## Critical Safety Rules

1. **Clean workspace**: `cleanup.py` before each PBIT file
2. **Fresh extraction**: Extract PBIT anew for each file
3. **Batch processing**: Fix ALL unsupported queries in a PBIT before reassembling
4. **Single write**: Write DataModelSchema and UnappliedChanges only once per PBIT
5. **In-place updates**: Replace SnowConvert output files (with backup)
6. **Sequential processing**: Complete ALL substeps for one PBIT before starting next
7. **No shared state**: Each PBIT file's variables and data are independent

**Never**:
- Reuse working directory without cleaning
- Process multiple PBIT files in parallel
- Mix data from different PBITs
- Modify queries that SnowConvert already successfully converted
- Work with original input files (only use SnowConvert output)
- Reassemble PBIT before all unsupported queries in that file are processed
- Modify parameter definitions in UnappliedChanges

## Output

**Updated** SnowConvert-processed PBIT files where:
- "Unsupported" queries in DataModelSchema have been converted to Snowflake connector
- "Unsupported" queries in UnappliedChanges have been converted (if file exists)
- Parameter definitions remain unchanged in both files
- All other queries remain exactly as SnowConvert converted them
- Original SnowConvert output backed up to `.backup` files
- Assessment report CSV updated with new status
