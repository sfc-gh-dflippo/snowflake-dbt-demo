---
name: add-code-units
description: Add local source code files to a migration project using scai code add. Use when source SQL files are already available on disk instead of extracting from a live database. Triggers: add code, import files, local files, add source, scai code add.
parent_skill: register-code-units
license: Proprietary. See License-Skills for complete terms
---

# Add Local Source Code

## On Entry

Tell the user:
> **Importing local SQL files.**
>
> I'll handle this for you — importing your local SQL files and organizing them by type into `source/`, ready for conversion. It's a single automated step; you won't need to copy, arrange, or move anything yourself.

## Prerequisites

- Migration project initialized (`scai init`)
- Local directory containing SQL source files

## Workflow

### Step 1: Get Source Path

Ask the user for the path to their source SQL files:

> "Where are your SQL source files located? Please provide the full path to the directory."

### Step 2: Annotate Multi-Object Files with sc-tags

`scai code add` uses the arrange engine to split files into one object per code unit. For non-T-SQL dialects the engine splits on `/* <sc-...> */` boundary tags. Before importing, call the `split_code` MCP tool to detect files that contain more than one top-level object and inject those tags automatically.

```
split_code(input_path="<INPUT_PATH>")
```

- If all files are single-object, the tool says so and you can skip ahead to Step 3 using `<INPUT_PATH>` directly.
- If multi-object files are found, the tool copies all `.sql` files to `artifacts/source_split/`, injects the sc-tags, verifies the result, and tells you to use `artifacts/source_split` as the input for Step 3.

The tool handles the full detect → inject → verify cycle in one call. It is OS-agnostic and does not require Python.

**Example** — what the tool injects before each object in a multi-object file:

```sql
/* <sc-table>sales.public.customers</sc-table> */
CREATE TABLE sales.public.customers (
  id INT,
  name VARCHAR(100)
);

/* <sc-view>sales.public.v_active_customers</sc-view> */
CREATE VIEW sales.public.v_active_customers AS
SELECT * FROM sales.public.customers WHERE active = 1;
```

> **T-SQL note:** T-SQL files do not need this step — the engine has a native T-SQL splitter. Skip Step 2 for T-SQL source files.

### Step 3: Add Code to Project

Use the path returned by `split_code` (or `<INPUT_PATH>` directly if no multi-object files were found):

```bash
scai code add -i <INPUT_PATH> --json
```

This will:
- Copy all files from the input path to `artifacts/source_raw/`
- Arrange and process the source code
- Merge processed output into `source/`

**If files already exist** and you need to overwrite:
```bash
scai code add -i <INPUT_PATH> --overwrite --json
```

### Step 4: Import ETL

ETL belongs in the project from register onward — the conversion picks it up from `source/_etl/` with no external path flag. Ask via `ask_user_question` (`multiSelect = false`):

> "Do you have any ETL code (SSIS or Informatica Power Center) to include?"
>
> 1. **Yes**
> 2. **No**

- If **no**, proceed to Step 5.
- If **yes**, ask for the folder path and compare it to `<INPUT_PATH>`:
  - If it is **the same as, or inside, `<INPUT_PATH>`**, Step 3 already imported it — `code add` classifies and promotes ETL anywhere under the input path, not just at its root. Proceed to Step 5 without running a second `code add`.
  - Otherwise (a genuinely separate folder) run:

```bash
scai code add -i <ETL_PATH> --json
```

Do **not** pass `--overwrite` here — the SQL is already in `source/` and would be wiped.

Getting the containment check wrong is not silently destructive: re-adding files already in `source/` fails with `ADD0007` (a conflict listing the offending files) rather than creating duplicate registry entries. But it is a dead end for the user, so check containment rather than plain path equality.

`code add` arranges the packages into `source/_etl/`. Confirm they landed there before continuing.

### Step 5: Verify Files Were Added

Check that `source/` contains the expected `.sql` files and report a count. Use whichever portable form fits the host:

```bash
# macOS / Linux
find source/ -name "*.sql" | head -20
find source/ -name "*.sql" | wc -l
```

```powershell
# Windows PowerShell
Get-ChildItem -Recurse -Filter *.sql source/ | Select-Object -First 20
(Get-ChildItem -Recurse -Filter *.sql source/).Count
```

## Output Structure

```
artifacts/source_raw/    Original files copied from input path
artifacts/source_split/  sc-tag annotated copies (only created when multi-object files exist)
source/                  Arranged source files ready for conversion
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "conflicting files" error | Use `--overwrite` flag to replace existing files |
| No `.sql` files found after add | Verify input path contains valid SQL files |
| Unexpected file arrangement | Check `artifacts/source_raw/` for the original copies |
| `split_code` reports verification errors | Manually inspect flagged files; the tool lists each with its boundary and tag counts |

## CHECKPOINT

Confirm with user:
- [ ] `scai code add` completed without errors
- [ ] Expected number of files appear in `source/`
- [ ] File structure looks correct

## On Completion

After the CHECKPOINT passes, tell the user. Fill placeholders from the JSON envelope returned by `scai code add --json`.

> **Import complete.** `<filesCopied>` SQL files imported as `<codeUnitsAdded>` code units, broken down by type (filled from `byType`). Files in `source/`.
> *If `etlFilesAdded > 0`:* ETL: `<etlFilesAdded>` files added.
> *If `etlFilesSkippedInvalidSchema > 0`:* `<etlFilesSkippedInvalidSchema>` ETL files skipped due to invalid schema.
> Next, we'll convert these to Snowflake SQL.

Then return to the calling skill.
