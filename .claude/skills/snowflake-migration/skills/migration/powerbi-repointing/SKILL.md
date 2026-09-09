---
name: powerbi-repointing
description: Repoint Power BI `.pbit` reports to Snowflake during conversion. Collects the `.pbit` folder path from the user and supplies the `--powerbi-repointing` flag for `scai code convert`. Load from `convert` or `code-conversion-only` only when the user confirms they have `.pbit` files.
parent_skill: migration
license: Proprietary. See License-Skills for complete terms
---

# Power BI Repointing

Load this skill from `convert` or `code-conversion-only` only when the user has answered **yes** to:
> "Do you have Power BI reports (`.pbit` files) you'd like to repoint to Snowflake?"

## Workflow

Do the following in order:

1. Say to the user (verbatim): *"Repointing rewrites the connection in each `.pbit` to point at Snowflake and translates any embedded SQL queries to Snowflake syntax."*
2. Ask the user (verbatim): *"Please provide the folder path containing your Power BI `.pbit` files. Only `.pbit` (Power BI template) files are supported — `.pbix` is not. If you only have `.pbix`, see https://github.com/Snowflake-Labs/SC.DDLExportScripts/tree/main/Power%20BI to export `.pbit`."*
3. Store the user's answer internally as `PBIT_PATH`.
4. Return to the calling skill. When it runs `scai code convert`, append `--powerbi-repointing <PBIT_PATH>` to the command. Do not emit the literal `<PBIT_PATH>` token to the shell.

## Convert Output for Power BI

When `--powerbi-repointing` is used, `scai code convert` writes:

- Repointed `.pbit` files → `artifacts/repointing_output/<timestamp>/<pbit_folder_name>/`
- Extracted embedded queries → `source/power_bi_sql_queries/`
- Converted Snowflake SQL for those queries → `snowflake/power_bi_sql_queries/`
- Per-query summary → `reports/SnowConvert/ETLAndBiRepointing.*.csv`

## Option Reference

| Option | Description |
|--------|-------------|
| `-p, --powerbi-repointing <PATH>` | Path to folder of Power BI `.pbit` files to repoint to Snowflake (also rewrites embedded queries to Snowflake-compatible syntax). `.pbix` files are not supported. |

## CHECKPOINT Addendum

After the calling skill's conversion CHECKPOINT, also confirm:
- [ ] Repointed `.pbit` files appear in `artifacts/repointing_output/<timestamp>/<pbit_folder_name>/`
- [ ] Per-query summary appears in `reports/SnowConvert/ETLAndBiRepointing.*.csv`

Then return to the calling skill.

## Post-Conversion Check: Unsupported Queries

After the conversion CHECKPOINT, scan the repointing report in the scai project:

```bash
grep -c "Unsupported" reports/SnowConvert/ETLAndBiRepointing*.csv
```

If any rows have `Status=Unsupported`, tell the user:

> *"SnowConvert successfully repointed your Power BI files, but some embedded queries could not be automatically converted. I can fix these using LLM-based translation. Would you like me to proceed?"*

If the user confirms, load `./fixer/SKILL.md` to complete the repointing process.

If no unsupported queries remain, the repointing is fully complete.
