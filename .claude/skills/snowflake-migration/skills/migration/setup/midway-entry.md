---
name: midway-entry
description: Bring an existing migration project into scai when you already have both source SQL and pre-converted Snowflake SQL on disk. Skips registration; runs conversion to build the registry, auto-pairs your converted files, then you review a small mapping file and apply. SQL Server and Redshift only. Triggers: midway entry, existing project, already converted, bring project to snowflake, import converted project, pre-converted code, code sync, sync --continue, remaining mappings.
parent_skill: setup
license: Proprietary. See License-Skills for complete terms
---

# Midway Entry

## On Entry

Tell the user:
> **Midway Entry.**
>
> Here's what I'll do:
> 1. Collect your project paths (target directory, source SQL, pre-converted Snowflake SQL).
> 2. Audit the source files and split any that contain multiple `CREATE` statements (sync requires one object per source file).
> 3. Run `scai code sync` to initialize the project, populate `source/` and `snowflake/`, build the registry, and auto-pair source files with their converted counterparts.
> 4. Review anything sync couldn't auto-pair with you, and finalize the pairings.
> 5. Apply the resolutions with `scai code sync --continue`.
> 6. Verify the project state, then return to setup so Snowflake/source/git can run before assessment.

## When To Use This Skill

Use midway entry when **all** of the following are true:
- You already have source SQL files on disk.
- You already have converted Snowflake SQL files on disk.
- Your source dialect is **SQL Server** or **Redshift**. Other dialects are not supported by this path.

If any of these is not true, use the normal setup flow (`./SKILL.md`) instead.

## Prerequisites

- **Target directory is empty.** `scai code sync` initializes a new project in place.
- **Source dialect**: `sqlserver` or `redshift`.
- **One `CREATE ___` per source file.** This is a hard requirement of `scai code sync`; multi-object source files are rejected and the project is rolled back. Step 2b walks through splitting them when the customer's source doesn't already meet this.
- **No mirrored layout required.** Sync auto-pairs source and converted files even when paths don't match (renames, moves, database renames are tolerated). Anything it can't auto-pair lands in a small file you review.

## Workflow

### Step 1: Collect Inputs

Ask the user for each input separately.

**1.1: Target project directory.** Default to the current working directory. Must be empty. If not empty, offer to create a subdirectory (e.g. `<cwd>/<name>-migration`).

**1.2: Source dialect.** Do **not** re-ask if setup already persisted one.

1. Call `configure()` / read project state (or reuse the dialect from `chooseSourceDialect` / `.scai/config/project.yml`).
2. If the dialect is **SQL Server** or **Redshift**, continue with that value.
3. If it is missing, ask via `ask_user_question` (`multiSelect = false`):

> "Which source dialect?"
>
> 1. **SQL Server**
> 2. **Redshift**

4. If it is any other dialect (Oracle, Teradata, PostgreSQL, …), stop midway: tell the user midway supports only SQL Server / Redshift, call `configure(entry_mode="fresh")`, then return to the parent setup skill so `progress_setup()` can continue on the fresh path.

(Oracle/Teradata/PostgreSQL are not supported for midway entry; fall back to the normal setup path.)

**1.3: Path to source SQL files.** The customer's source directory. Layout does **not** need to match the converted side.

**1.4: Path to converted Snowflake SQL files.** The customer's previously converted directory. Pass it as-is; do not pre-process or rearrange it.

### Step 2: Audit The Source Side

The only structural rule is **one `CREATE ___` per source file**. The converted side has no such requirement: `scai code sync` parses converted files by SQL object identity, while source files become registry entries 1:1 with their file path, so duplicate source paths break registration but the converted side can hold multi-object files freely.

Run a quick audit. The intent is portable — agents on Windows should reach the same answers via PowerShell or stdlib Python; agents on POSIX can use the shell snippets verbatim.

1. **Count files** in `<SOURCE_PATH>` and `<SNOWFLAKE_PATH>`.

   POSIX: `find <SOURCE_PATH> -type f | wc -l`
   Windows: `(Get-ChildItem -Recurse -File <SOURCE_PATH>).Count`

2. **Flag source files with >1 top-level `CREATE`** — those must be split before sync. The pattern is `^\s*(CREATE|ALTER)\s+(OR\s+REPLACE\s+)?(TABLE|VIEW|PROCEDURE|FUNCTION|TRIGGER|SEQUENCE|SCHEMA|TYPE|INDEX|DATABASE|SYNONYM|ROLE)`, case-insensitive, counted per file.

   POSIX:
   ```bash
   grep -ciE '^[[:space:]]*(CREATE|ALTER)[[:space:]]+(OR[[:space:]]+REPLACE[[:space:]]+)?(TABLE|VIEW|PROCEDURE|FUNCTION|TRIGGER|SEQUENCE|SCHEMA|TYPE|INDEX|DATABASE|SYNONYM|ROLE)' \
     <SOURCE_PATH>/**/*.sql 2>/dev/null | awk -F: '$2>1'
   ```

   Windows or any host without grep/awk: use `Select-String` or a small Python snippet — `re.MULTILINE` + `re.IGNORECASE` + count matches per file.

Branch:

- **(A) Clean already.** Every source file has exactly one top-level `CREATE`. Skip to Step 3 using the customer paths directly.
- **(B) Multi-object source files.** Go to Step 2b. Do **not** touch the customer's converted directory in either case.

### Step 2b: Split Multi-Object Source Files

**Goal:** produce `<WORK_DIR>/source_processed/` where every `.sql` file contains exactly one top-level `CREATE ___`. Do not modify the customer's original directory.

> **Important:** the work dir must live **outside** `<TARGET_DIR>`. `scai code sync` requires the target to be completely empty, and a nested `.midway_work/` will trip the "Project directory is not empty" check (error `PRJ0001`). Default to `tmp/.midway_work/` or another path the user prefers. **Never use `<TARGET_DIR>/.midway_work/`.**

**Plan first, then act.** Present a short plan that includes:

1. **Inventory.** Total source files, file types, sample nested layout.
2. **Split candidates.** Count of source files containing multiple top-level CREATEs.
3. **Naming convention for outputs.** Recommend one of:
   - `<database>/<schema>/<object_type>/<object_name>.sql` (good for SnowConvert-style inputs),
   - `<schema>/<object_name>.sql` (flatter),
   - flat `<object_name>.sql` (only if no schema collisions).

   When two objects share the same name across schemas (e.g. `dbo.users` and `audit.users`), include the schema in the file path or filename so each split file ends up at a unique relative path.

Ask the user to confirm the plan before proceeding.

**Execution rules:**

- Walk the source tree; for every `.sql` file, detect top-level `CREATE ___` boundaries and split, preserving comments and any leading `USE DATABASE/SCHEMA` or `SET` statements that apply to each block. Write each piece to its own file under the chosen relative path.
- Drop non-SQL files and note them to the user. Never silently discard a file containing a `CREATE`.
- Re-run the multi-CREATE grep against `<WORK_DIR>/source_processed/` to confirm every file now has exactly one CREATE before calling sync.
- For non-trivial splits, prefer a small scripted pass (python/awk) over ad-hoc sed.

After splitting, pass `<WORK_DIR>/source_processed/` as `--input` in Step 3. The customer's converted directory still goes in unchanged via `--snowflake`.

### Step 3: Run `scai code sync` (generate)

```bash
scai code sync <TARGET_DIR> -l <sqlserver|redshift> \
  --input <SOURCE_PATH> \
  --snowflake <SNOWFLAKE_PATH> --json
```

Example:

```bash
scai code sync . -l sqlserver \
  --input ../source_processed \
  --snowflake ../legacy/converted/SnowConvert --json
```

Sync creates the project in `<TARGET_DIR>`, populates `source/` and `snowflake/`, builds the registry, and pairs each source object with a converted file. It writes two files into `<TARGET_DIR>/.scai/config/`:

- `complete-mappings.yml`: auto-paired entries (informational, no action).
- `remaining-mappings.yml`: entries that need a decision (only created if any).

**Read the CLI output before continuing:**
- If you see `All code units auto-resolved. No manual mapping needed.` → skip Step 4 and go straight to Step 5.
- Otherwise the CLI prints counts (`Auto-resolved`, `Unmatched source`, etc.) and points you at `remaining-mappings.yml`; go to Step 4.

### Step 4: Review `remaining-mappings.yml`

Open `<TARGET_DIR>/.scai/config/remaining-mappings.yml`. Entries are grouped by object type (`Table`, `Procedure`, `View`, …) under `unmatched_source`. For each entry, choose **one** outcome:

| Outcome | What to set on the entry | Use when |
|---------|--------------------------|----------|
| Resolve | `snowflake_path: <relative path>` (pick from `possible_matches`, or type one) | The converted file exists; sync just couldn't auto-pick. |
| Ignore  | `action: ignore` | This source object intentionally has no Snowflake counterpart. |
| Adopt   | `action: adopt`  | The Snowflake side has an object you want to register fresh. |

Minimal example of an entry the reviewer touches:

```yaml
unmatched_source:
  Table:
    - source_canonical_id: '[schema].[my_table]'
      source_path: source/EDW/PROD_EDW_DB/schema/Tables/my_table.sql
      snowflake_path:                 # ← set this, OR set action: ignore / action: adopt
      possible_matches:
        - snowflake/DEV_EDW_DB/schema/Tables/my_table.sql
```

Rules of thumb for the agent:

- Prefer `snowflake_path` from `possible_matches` first; those are the engine's identity-based suggestions.
- Don't delete entries to "skip" them; use `action: ignore` instead. Empty/removed entries are reported as unresolved.
- `unmatched_snowflake`, `summary`, and `possible_matches` are informational; the engine ignores them when applying.

When a batch is too large to walk one-by-one with the user, summarize and ask: present counts per object type, sample a few entries with their `possible_matches`, and propose a default policy (e.g. "accept all single-`possible_matches` candidates, flag the rest"). Apply only after the user confirms.

### Step 5: Run `scai code sync --continue` (apply)

From inside `<TARGET_DIR>`:

```bash
scai code sync --continue --json
```

This reads `remaining-mappings.yml` and applies the outcomes. Read its output:

- `All entries resolved. Remaining mappings file removed.` → done, go to Step 6.
- `Remaining entries: <N>` → some entries are still unresolved. Re-edit `remaining-mappings.yml` (set `snowflake_path`, `action: ignore`, or `action: adopt` on each remaining entry) and re-run `scai code sync --continue`. Repeat until clean or the user explicitly accepts the remaining as ignored.

### Step 6: Verify

Confirm the project scaffolding exists (`.scai`, `source`, `snowflake`, `artifacts` directories) and count `.sql` files in each side. Use whichever portable command fits the host: `ls -la` + `find ... | wc -l` on POSIX, `Get-ChildItem` on PowerShell, or `Path.iterdir()` from a Python helper.

Then call `migration_status(mode="summary")`. Expect:
- `routing.project_exists = true`
- `routing.registered = true`
- `routing.converted = true`
- `routing.assessed = false`

### Step 7: Checkpoint

Confirm with the user:
- [ ] `scai code sync` completed without errors
- [ ] `remaining-mappings.yml` was reviewed and applied (or the run reported all auto-resolved)
- [ ] `scai code sync --continue` ended with `All entries resolved` (or remaining entries are intentional ignores)
- [ ] `migration_status` reports registered + converted + not assessed

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Target directory not empty | Pick (or create) an empty target. Make sure any `.midway_work/` lives **outside** the target. |
| Unsupported source dialect | Oracle/Teradata are not supported; use the standard setup flow (`./SKILL.md`). |
| Source has multiple objects per file | The project rolls back. Split each source file so it contains a single `CREATE ___` (Step 2b), then re-run sync. |
| `scai code sync` reports many `Unmatched source` despite layouts that look mirrored | Common when database names differ (e.g. `PROD_DB` vs `DEV_DB`). Sync will still identity-match most of them; review `possible_matches` in `remaining-mappings.yml` to clear the rest. |
| `scai code sync --continue` says it can't find the mapping file | Run `scai code sync` first, or run `--continue` from inside `<TARGET_DIR>`. |
| `scai code sync --continue` reports unresolved entries | Open `remaining-mappings.yml`; on each remaining entry set `snowflake_path`, or `action: ignore`, or `action: adopt`; re-run. Don't delete entries to skip them. |

## On Completion

After the CHECKPOINT passes, tell the user. Fill placeholders from `scai code sync --json` (and `scai code sync --continue --json`) outputs.

The setup machine treats midway as done only when the project is initialized **and** both `source/**/*.sql` and `snowflake/**/*.sql` exist (`allOf`). Do not return until the CHECKPOINT confirms that.

> **Midway entry complete** in `<duration>`. Your project is initialized with `<N>` source files and `<M>` converted files paired (`<X>` auto-resolved, `<Y>` reviewed and applied).
> *If `ignored > 0`:* `<Z>` ignored.
> *If `adopted > 0`:* `<W>` adopted.
> Registration and conversion were skipped because pre-converted code was already present. Next, setup will configure Snowflake (and optional source/git) before assessment.

Before returning, call `configure(code_source="local")` — midway already placed source files on disk, so the setup graph must route past the source-connection step (which only applies to the "extract from database" path).

Return to the parent setup skill and call `progress_setup()` so the state machine picks the next task.
