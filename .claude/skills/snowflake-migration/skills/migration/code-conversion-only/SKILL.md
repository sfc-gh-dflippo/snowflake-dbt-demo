---
name: code-conversion-only
description: Convert local source code to Snowflake SQL for code-conversion-only source systems such as Sybase IQ, Azure Synapse, Spark SQL, Databricks SQL, Greenplum, Netezza, Vertica, and Hive. Optionally repoints Power BI reports. Use when configure returns project_type code_conversion_only for these sources.
parent_skill: migration
license: Proprietary. See License-Skills for complete terms
---

# Code Conversion Only

## On Entry

Tell the user:
> **Code Conversion Only** — I'll walk you through adding local source files, converting them to Snowflake SQL, and choosing what to do next with the converted output.

Guide users through SnowConvert's code-conversion-only path. This path uses local source files, not live source extraction.

## Supported Sources

If `configure()` does not already have source_language configured, use the CLI dialect directly for `configure(source_language=...)`. Azure Synapse is the exception: it uses `source_language="synapse"` while initializing the CLI dialect as `SqlServer` with `project_type: code_conversion_only`.

| User-facing source | `configure(source_language=...)` / CLI dialect |
|--------------------|-----------------------------------------------|
| Sybase IQ | `Sybase` |
| Azure Synapse | `synapse` / `SqlServer` with `project_type: code_conversion_only` |
| Spark SQL | `Spark` |
| Databricks SQL | `Databricks` |
| BigQuery | `BigQuery` |
| PostgreSQL | `Postgresql` |
| Greenplum | `Greenplum` |
| Netezza | `Netezza` |
| Vertica | `Vertica` |
| Hive | `Hive` |
| IBM DB2 | `Db2` |

If the user says "PostgreSQL & Based Languages" but does not specify one, ask whether they mean PostgreSQL, Greenplum, or Netezza.

> **Note on PostgreSQL, IBM DB2, and BigQuery:** New PostgreSQL, DB2, and BigQuery projects default to `project_type: full_migration` and are routed through `setup/SKILL.md`. They appear in this table only for **legacy** projects whose `project.yml` already has `project_type: code_conversion_only` persisted from before full-pipeline support shipped. If you reach this skill for PostgreSQL, DB2, or BigQuery, the legacy project configuration is being honored.

## Workflow

### Step 1: Confirm Project Routing

If `routing.converted = true` (from `configure()`), tell the user conversion output already exists in `snowflake/` and offer:

1. **Review converted output and reports**
2. **Re-run conversion**

Only continue to Step 2 if the user chooses to re-run conversion or source files are missing.

If the source system was not already selected by the calling skill, ask the user which supported source they are converting and map it using the table above.

If no project directory is configured, ask where to create/use the project.

Call the `configure` tool with:

```text
configure(project_dir="<PROJECT_DIR>", source_language="<SOURCE_KEY>")
```

Present the returned `user_overview` and `routing` metadata. Confirm it shows `project_type: code_conversion_only`.

### Step 2: Add Local Source Files

Check whether source files are already present in the project `source/` directory.

If no source files are present, ask:

> "Where are your source SQL/code files located? Please provide the full path to the directory or file."

Then run from the project directory:

```bash
scai code add -i <INPUT_PATH> --skip-split --json
```

If the user explicitly wants to replace existing source files, add `--overwrite`.

### Step 3: Check for ETL Code

Any ETL imported by `scai code add` lands in `source/_etl/`. That is where `convert` reads it from.

Check whether `source/_etl/` exists and contains ETL files — `.dtsx` for SSIS, `.xml` for Informatica PowerCenter (use whichever portable form fits the host).

- If it is **missing or empty**, there is no ETL to convert; proceed to Step 4.
- If it contains **SSIS** packages only, no conversion-target prompt is needed; proceed to Step 4.
- If it contains **Informatica** PowerCenter XML, ask the remaining ETL questions up front, in one sequence, before running the conversion:
    1. Conversion target, via `ask_user_question` (`multiSelect = false`):
       > "How should Informatica mappings be converted?
       > 1. **dbt** (default): each mapping becomes a dbt model orchestrated by Snowflake Tasks.
       > 2. **Snowflake Scripting** (preview): each mapping becomes a standalone Snowflake stored procedure the Task graph calls. Stabilization and deploy are skipped for this preview flavor."
    2. If the answer is **dbt**, also ask (`multiSelect = false`): "Consolidate dbt model chains to reduce the number of generated model files?". On yes, set `CONSOLIDATE_DBT = true` for Step 5.
    3. If the answer is **Snowflake Scripting**, set `SCRIPTING_MODE = true` for Step 5.

    Persist the choice with the MCP `configure` tool: `etl_informatica_target = "dbt"` or `"scripting"`.

These questions are still required: the conversion target is not something `scai code add` can infer from the imported files. Ask them on every conversion, re-runs included — `scai code convert` defaults to dbt, so a missing flag in Step 5 silently changes the output.

### Step 4: Check for Power BI Reports

Ask the user:

> "Do you have Power BI reports (`.pbit` files) you'd like to repoint to Snowflake?"

If **yes**, load `../powerbi-repointing/SKILL.md`. It collects `PBIT_PATH` and tells you to append `--powerbi-repointing <PBIT_PATH>` to the convert command in Step 5. Return here when complete.

If **no**, proceed to Step 5. `PBIT_PATH` remains unset; do not pass `--powerbi-repointing` to scai.

### Step 5: Convert

Before running, tell the user what the conversion will cover. If `PBIT_PATH` was set, mention Power BI repointing. If `SCRIPTING_MODE` was set, mention the Snowflake Scripting target.

Always include `--json` so the agent can parse the result envelope. Start from the base command and append one flag per decision already recorded in the steps above — nothing else:

```bash
scai code convert --json
```

| Append | When |
|--------|------|
| `--informatica-to-snowflake-scripting` | `SCRIPTING_MODE` was set in Step 3 (Informatica target is Snowflake Scripting) |
| `--consolidate-dbt-model-chains` | `CONSOLIDATE_DBT` was set in Step 3 (Informatica target is dbt and the user chose to consolidate model chains) |
| `--powerbi-repointing <PBIT_PATH>` | `PBIT_PATH` was set in Step 4 |

The two Informatica flags are mutually exclusive — they come from the same single-select answer, so at most one can apply. Either combines with `--powerbi-repointing`. If none of the conditions hold, run the base command as-is.

Substitute `<PBIT_PATH>` with the actual folder path you stored. Do not emit literal placeholder tokens to the shell.

Per-EWI details (code, description, severity) are written to `reports/SnowConvert/Issues.*.csv`; read those files in Step 6 when working on **Review EWIs** or **Resolve EWIs with Cortex Code**.

For Power BI output paths and the CHECKPOINT addendum, see `../powerbi-repointing/SKILL.md`.

### Conversion Options

| Option | Description |
|--------|-------------|
| `-x, --show-ewis` | Show detailed EWI breakdown |
| `--overwrite-working-directory` | Overwrite output files in `snowflake/` and registry |
| `--informatica-to-snowflake-scripting` | Convert Informatica mappings to standalone Snowflake stored procedures (Snowflake Scripting) instead of dbt projects. Preview flavor. |
| `--consolidate-dbt-model-chains` | Consolidate Informatica dbt model chains to reduce the number of generated model files. Applies when the Informatica target is dbt. |

For Power BI options, see `../powerbi-repointing/SKILL.md`.

### Step 6: Ask the user

After conversion, ask:

> "What would you like to do next?"
> 1. **Review converted output** — inspect `snowflake/`, `reports/SnowConvert/`, conversion logs, and (if Power BI repointing ran) `artifacts/repointing_output/` and `snowflake/power_bi_sql_queries/`
> 2. **Review EWIs** — summarize issues from the latest SnowConvert reports and identify high-priority items
> 3. **Resolve EWIs with Cortex Code** — work through selected converted files/issues and apply fixes
> 4. **Add more source files and re-run conversion** — return to Step 2
> 5. **Stop here** — leave the converted output ready for manual review

If the user chooses **Resolve EWIs with Cortex Code**, inspect the latest SnowConvert issue reports and converted files, then help fix the selected EWIs directly in the project. Keep the work scoped to code conversion output unless the user explicitly asks to move into deployment or broader migration workflows.

## Rules

1. Do not set up a source database connection for this path.
2. Do not route to data migration, data validation, assessment, or migrate-objects unless the user explicitly asks.
3. Do not use `scai code extract`; conversion-only sources use local files.
4. Preserve the CLI project type value `code_conversion_only`; do not introduce another project-type spelling.
