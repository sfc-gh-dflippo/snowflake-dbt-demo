---
name: convert
description: Convert source code to Snowflake SQL using SnowConvert. Transforms full-migration sources and code-conversion-only sources to Snowflake-compatible syntax, and optionally repoints Power BI reports and Tableau workbooks. Triggers: convert, snowconvert, transform code, convert to snowflake, power bi, tableau.
parent_skill: migration
license: Proprietary. See License-Skills for complete terms
---

# Code Conversion

## On Entry

Tell the user:
> **Code Conversion.**
>
> Here's what I'll do:
> 1. Run SnowConvert against your source SQL files, transforming each into Snowflake SQL syntax (optionally tailoring conversion settings to your source first, or going with defaults).
> 2. Generate reports flagging anything that needs manual review (EWIs, FDMs, performance remarks, out-of-scope items).
> 3. Save converted code under `snowflake/` and reports under `reports/SnowConvert/`.

Convert source code to Snowflake SQL using SnowConvert.

Report the result from the `--json` envelope and hand off. Reading the generated
reports, counting EWIs by severity or judging what needs fixing is the
assessment's job — do that here only if the user asks a direct question.

## Prerequisites

- Migration project initialized (`scai init`)
- Source SQL in `source/` **or** Tableau repointing with `TABLEAU_PATH` set (Tableau-only is allowed with an empty `source/`; Step 3.5 applies the dialect gate)

## Workflow

### Step 1: Verify Source Code Exists

Confirm `source/` contains `.sql` files (use whichever portable form fits the host). Note whether SQL is present; do not stop yet.

If `source/` is empty, continue to Steps 2–3.5. After those steps, if there is still no SQL **and** `TABLEAU_PATH` is unset **and** `PBIT_PATH` is unset, return to the parent setup skill so it can re-query `progress_setup()`. Tableau-only conversions (Step 3.5 sets `TABLEAU_PATH`) are allowed with an empty `source/`.

### Step 2: Check for ETL Code

Any ETL in this project was imported during register (`scai code add`), which arranges the packages into `source/_etl/`. That is where `convert` reads them from.

Check whether `source/_etl/` exists and contains ETL files — `.dtsx` for SSIS, `.xml` for Informatica PowerCenter (use whichever portable form fits the host).

- If it is **missing or empty**, there is no ETL to convert; proceed to Step 3.
- If it contains **SSIS** packages only, no conversion-target prompt is needed; proceed to Step 3.
- If it contains **Informatica** PowerCenter XML, ask the remaining ETL questions up front, in one sequence, before running the conversion:
    1. Conversion target, via `ask_user_question` (`multiSelect = false`):
       > "How should Informatica mappings be converted?
       > 1. **dbt** (default): each mapping becomes a dbt model orchestrated by Snowflake Tasks. Supports ETL stabilization and deploy.
       > 2. **Snowflake Scripting** (preview): each mapping becomes a standalone Snowflake stored procedure the Task graph calls. Stabilization and deploy are skipped for this preview flavor."
    2. If the answer is **dbt**, also ask (`multiSelect = false`): "Consolidate dbt model chains to reduce the number of generated model files?". On yes, set `CONSOLIDATE_DBT = true` for Step 4.
    3. If the answer is **Snowflake Scripting**, set `SCRIPTING_MODE = true` for Step 4.

    Persist the choice with the MCP `configure` tool: `etl_informatica_target = "dbt"` or `"scripting"`. When the target is Snowflake Scripting, the `--informatica-to-snowflake-scripting` convert flag in Step 4 additionally records the project-level `etl_target` in `project.yml` that gates the scripting-preview routing.

These questions are still required: the conversion target is not something `scai code add` can infer from the imported files.

### Step 3: Check for Power BI Reports

Ask the user:

> "Do you have Power BI reports (`.pbit` files) you'd like to repoint to Snowflake?"

If **yes**, load `../powerbi-repointing/SKILL.md`. It collects `PBIT_PATH` and tells you to append `--powerbi-repointing <PBIT_PATH>` to the convert command in Step 4. Return here when complete.

If **no**, proceed to Step 3.5. `PBIT_PATH` remains unset; do not pass `--powerbi-repointing` to scai.

### Step 3.5: Check for Tableau Workbooks (Oracle only)

Read `source_language` from `configure()` (already called this session). If it is **not** Oracle (compare case-insensitively), skip this step: `TABLEAU_PATH` stays unset; do not pass `--tableauRepointing`.

If it **is** Oracle, ask the user:

> "Do you have Tableau workbooks (`.twb` or `.tds` files) you'd like to repoint to Snowflake?"

If **yes**, load `../tableau-repointing/SKILL.md` in path-only mode. It collects `TABLEAU_PATH` and tells you to append `--tableauRepointing <TABLEAU_PATH>` to the convert command in Step 4. Return here when complete.

If **no**, proceed to Step 3.6. `TABLEAU_PATH` remains unset; do not pass `--tableauRepointing` to scai.

### Step 3.6: Offer Custom Conversion Settings

Keep this quick — most users just want defaults. Ask via `ask_user_question` (`multiSelect = false`):

> "SnowConvert supports custom conversion settings tailored to your source language. Want to tailor them, or go with the defaults?"
>
> 1. **Tailor settings** — I'll suggest options based on your code; you confirm.
> 2. **Go with defaults**

- On **Go with defaults**: `<SETTINGS_FLAGS>` stays empty; proceed to Step 4.
- On **Tailor settings**: load `./recommend-settings/SKILL.md`. It scans the source, proposes dialect-specific settings, and — after the user confirms — returns a flag string. Store it as `<SETTINGS_FLAGS>` for Step 4. If the user declines all suggestions or the catalog can't be loaded, `<SETTINGS_FLAGS>` stays empty. Return here when complete. If `source/` is empty (Tableau-only), skip tailoring and leave `<SETTINGS_FLAGS>` empty.

### Step 4: Run Conversion

Before running, tell the user what the conversion will cover: the SQL and ETL already in the project (`source/`, plus `source/_etl/` when present), Power BI repointing if `PBIT_PATH` was set, and Tableau repointing if `TABLEAU_PATH` was set. Tableau-only (empty `source/`, `TABLEAU_PATH` set) is valid.

Start from the base command:

```bash
scai code convert <SETTINGS_FLAGS> --json
```

`--json` is always required so you can parse the result envelope. Substitute `<SETTINGS_FLAGS>` with the confirmed flags from Step 3.6 (or omit the token when empty). Then append one flag per decision already recorded in the steps above — nothing else. Do **not** pass `--etl-replatform-sources-path`; ETL already lives under `source/_etl/` from register.

| Append | When |
|--------|------|
| `--informatica-to-snowflake-scripting` | `SCRIPTING_MODE` was set in Step 2 (Informatica target is Snowflake Scripting) |
| `--consolidate-dbt-model-chains` | `CONSOLIDATE_DBT` was set in Step 2 (Informatica target is dbt and the user chose to consolidate model chains) |
| `--powerbi-repointing <PBIT_PATH>` | `PBIT_PATH` was set in Step 3 |
| `--tableauRepointing <TABLEAU_PATH>` | `TABLEAU_PATH` was set in Step 3.5 |

The two Informatica flags are mutually exclusive — they come from the same single-select answer, so at most one can apply. Either combines with `--powerbi-repointing` and/or `--tableauRepointing`. If none of the conditions hold, run the base command as-is.

Substitute `<PBIT_PATH>` and `<TABLEAU_PATH>` with the actual paths you stored. Do not emit literal placeholder tokens to the shell.

### Step 5: Read the Result Envelope

`--json` returns the result. That envelope is the whole story for this step —
**don't open the reports, the CSVs or the logs to work out what happened.**

Conversion writes:
- **Converted code** in `snowflake/`
- **Reports** in `reports/SnowConvert/`
- **Logs** in `logs/`

Name those locations so the user knows where to look. Reading them is the
assessment's job, or something to do later if the user asks a question the
envelope can't answer.

### Conversion Options

| Option | Description |
|--------|-------------|
| `-x, --show-ewis` | Show detailed EWI breakdown |
| `--overwrite-working-directory` | Overwrite output files in `snowflake/` and registry |
| `--informatica-to-snowflake-scripting` | Convert Informatica mappings to standalone Snowflake stored procedures (Snowflake Scripting) instead of dbt projects. Preview flavor; ETL stabilization and deploy are skipped for these units. |
| `--consolidate-dbt-model-chains` | Consolidate Informatica dbt model chains to reduce the number of generated model files. Applies when the Informatica target is dbt. |

For Power BI options, see `../powerbi-repointing/SKILL.md`. For Tableau options, see `../tableau-repointing/SKILL.md`.

**Example with options:**
```bash
scai code convert --show-ewis --overwrite-working-directory --json
```

## Understanding EWIs

Reference for answering a question the user asks — not a prompt to go analyze
the run. EWIs (Early Warning Issues) indicate conversion items needing attention:

| Severity | Action Required |
|----------|----------------|
| **Critical** | Must fix before deployment |
| **High** | Should fix, may cause runtime errors |
| **Medium** | Review recommended |
| **Low** | Minor issues, optional fixes |

**Common EWI codes:**
- `SSC-EWI-0030`: Dynamic SQL (requires manual review)
- `SSC-FDM-*`: Functional differences (behavior may differ)
- `SSC-PRF-*`: Performance remarks (optimization suggested)

## Output Structure

```
snowflake/
├── <database>/
│   └── <schema>/
│       ├── table/
│       ├── view/
│       ├── procedure/
│       └── function/
└── _etl/                              # Converted ETL code (Task graph + stored procedures for scripting; dbt models for dbt)
    └── <package_name>/
        ├── <package_name>.sql         # Snowflake Task graph
        └── <data_pipeline>/
            └── models/                # dbt models (staging, intermediate, marts) when target is dbt
reports/
├── SnowConvert/
│   ├── TopLevelCodeUnits.*.csv
│   ├── Issues.*.csv
│   ├── ObjectReferences.*.csv
│   ├── Assessment.*.json
│   ├── ETL.Elements.*.csv             # ETL elements processed (packages, tasks, data flows)
│   └── ETL.Issues.*.csv               # ETL-specific conversion issues
├── ArrangeReports/
└── GenericScanner/
logs/
artifacts/
└── repointing_output/
    └── tableauResults/                 # Durable repointed .twb/.tds output when Tableau was requested
```

For Power BI output paths, see `../powerbi-repointing/SKILL.md`. For Tableau, use only
`result.tableauRepointing.outputPath` from the JSON envelope; it resolves to
`artifacts/repointing_output/tableauResults/`. Never report the temporary
`.scai/.snowconvert/tableauResults` engine path.

## CHECKPOINT

The envelope's own status is the check — don't go looking for corroboration.

- [ ] The convert command exited successfully and the envelope reports no conversion errors
- [ ] If Power BI reports were included, follow the CHECKPOINT addendum in `../powerbi-repointing/SKILL.md`
- [ ] If Tableau workbooks were included, follow the CHECKPOINT addendum in `../tableau-repointing/SKILL.md`

If the envelope reports errors, surface them verbatim and stop. Otherwise move on
— don't ask the user to review EWI counts or confirm that files landed.

## On Completion

Show the JSON envelope from `scai code convert --json` **as-is**, in a fenced
`json` block, under one line:

> **Conversion complete.** Converted code is in `snowflake/`, reports in `reports/SnowConvert/`.

When Tableau was requested, the envelope's `result.tableauRepointing` block is
authoritative: success contains `processedFiles` and the durable `outputPath`;
`{"message":"None found"}` means no Tableau result was processed. Do not construct
or infer a different output path.

Then one line on what's next, and move on:

> Next, we'll run an assessment to plan your migration: dependency waves, object categorization, and a deployment plan.

Do not restate the envelope's numbers in prose, break issues down by severity,
rank them, or say which ones need fixing — the assessment does that with the
full picture, and a summary here is one more thing that can disagree with it.
If the user asks about a number, an EWI code, or a specific file, dig in *then*;
the reference sections above are for that.

*If `SCRIPTING_MODE` was set*, also tell the user:
> Informatica mappings were converted to Snowflake Scripting stored procedures (preview). **ETL Stabilization is not supported for Snowflake Scripting conversions (dbt only)**, and deploy is not part of this preview flow - both are skipped for these ETL units. The generated procedures and Task graph are under `snowflake/_etl/` for review.

There is now enough converted code for the local dashboard to be worth looking
at. If `configure` reported a dashboard URL at session start, mention it once:
> You can watch progress at `<url>` — read-only, and only on your machine.

Skip the line if no URL came back (the user opted out, or the port was busy).
Don't guess a URL, and don't repeat this every step.

Then return to the calling skill.
