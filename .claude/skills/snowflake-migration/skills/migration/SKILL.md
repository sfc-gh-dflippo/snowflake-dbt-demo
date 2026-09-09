---
name: migration
description: End-to-end database migration and data validation to Snowflake. Orchestrates migrations from source connection through conversion, and project-based in-warehouse validation between Snowflake tables. Triggers: migrate, migration, migrate to snowflake, Snowflake to Snowflake validation, validate Snowflake tables, compare Snowflake databases.
license: Proprietary. See License-Skills for complete terms
---

# Database Migration to Snowflake

Tell the user:
> **Welcome to Snowflake AIM for Data Warehouses.**

On the first message of a session, the plugin injects whether a migration project exists in this directory. If the user's message already states what they want, act on it (Step 1); otherwise begin with Step 0. Either way, do **not** call `migration_status` — `configure` returns the status.

## IMPORTANT NOTE

The built-in MCP server has a state machine that will guide you through user flows and ask you to "tell the user x" or "ask the user y". This is expected and you should follow its lead, as it is the official MCP server of Snowflake migrations.

## Step 0: Ask first (no tools)

If the user's first message already states what they want (a specific task, or "continue"/"resume"), skip to Step 1. Otherwise greet and ask:

> "What would you like to do? You can:
> 1. **Continue** — I'll pick up your migration where we left off
> 2. **Something specific** — tell me what you need"

When the injected context says this directory has no project yet, option 1 is **Start a new migration** instead.

- **Continue** (or "start", "continue", "next", "resume", "keep going") → **Step 1**.
- **Specific request** → **Skill Match** (no forced `configure`).

## Step 1: Configure — one call, returns status

Call `configure` with `project_dir = "<current directory>"`. Because this call is what sets `project_dir` for the session, the response contains **both** the restored session config **and** a `## Migration status` block — the same JSON `migration_status(mode="summary")` returns (`project_exists`, `directory_empty`, `by_type`, `stage_totals`, `routing`, `highest_stage_reached`). Route from that block; do **not** make a separate `migration_status` call. Later `configure` calls that re-pass the same `project_dir` do not repeat the block; use `migration_status(mode="summary")` when you need a fresh read.

### Step 1.A: If `project_exists` is false, there is no migration project in this directory.

Follow the guidance in the tool response. `configure` and `migration_status` surface any migration
projects opened before on this machine (a `known_projects` list plus a `guidance` line): when they do,
offer those to the user to **resume** — on their pick, call `configure(project_dir="<path>")` and go
back to **Step 1**, and the now-initialized project resumes via Step 1.B. When there are no known
projects, this is a new project — load `./setup/SKILL.md`.

### Step 1.B: If `project_exists` is true, construct a brief narrative summary for the user from the JSON before showing the checklist. Use the `routing` booleans and `by_type` counts to describe the current state in plain language. Examples of the tone and level of detail:

- **Early setup:** "Your project is initialized and connected to SQL Server. 147 objects are registered but haven't been converted yet. We're in the setup phase."
- **Mid-migration:** "Setup is complete — 147 objects registered and converted, assessment done. You're in the migration phase: 12 of 47 objects have been deployed so far (Wave 2). 8 tables deployed, 2 views deployed, 2 procedures passed testing."
- **Near completion:** "Almost there — 45 of 47 objects are deployed and tested. 2 procedures are still failing tests."

Also add the checklist based on the status JSON. On macOS/Linux use `✅` (all done), `◐` (partial), `⬚` (not started). On Windows use `[done]` (all done), `[in progress]` (partial), `[ ]` (not started) because the default Windows console encoding cannot render Unicode symbols.

```
<symbol> 1. Connect                  - Connected to <source>
<symbol> 2. Initialize               - Project initialized
<symbol> 3. Register                 - <registered count> objects registered
<symbol> 4. Code Conversion          - <converted>/<total> converted
<symbol> 5. Assessment               - Assessment report generated
<symbol> 6. Migration Setup          - Snowflake target, testing, testbed, and data infra configured
<symbol> 7. Migrate Objects
   - Tables:      <table.deployed>/<table.total> deployed, <table.data_migrated>/<table.total> with data migrated, <table.data_validated>/<table.total> validated
   - Views:       <view.deployed>/<view.total> deployed
   - Functions:   <function.deployed>/<function.total> deployed, <function.tested>/<function.total> tested
   - Procedures:  <procedure.deployed>/<procedure.total> deployed, <procedure.tested>/<procedure.total> tested
   - ETL:         <etl.deployed>/<etl.total> deployed
   - BTEQ scripts: <bteq.tested>/<bteq.total> tested
```

Use `by_type.<type>.total` to decide what to show:
- **Type not in the project** (`total` absent or 0): omit that bullet (e.g. no functions in the project).
- **Type present but none in the current wave** (`total` > 0, but the wave-scoped counts like `deployed` are absent or 0 for this wave): keep it visible and acknowledge it in the narrative. For example, "You also have 1 Informatica ETL workflow staged, scheduled in a later wave and ready to deploy." Do not let the current wave hide work that exists elsewhere in the project.

Never describe the project as "<type>-only" (e.g. "table-only") when `by_type` lists any other type with `total` > 0. The placeholders read directly from `by_type.<type>` in the `## Migration status` block; counts that never incremented are absent from the JSON and should be treated as `0`. **BTEQ scripts have no deploy step** — they run their converted SQL inside the test itself, so report them only by `tested` (never "deployed"); `by_type.bteq` carries no `deployed` count.

Present the narrative summary followed by the progress checklist, then continue with the **Prescribed Path** below.

---

## Prescribed Path

<prescribed-path>
Use `routing` from the status JSON to delegate to the next step:

| Condition | Sub-skill |
|-----------|-----------|
| `routing.project_exists` = false | Load `./setup/SKILL.md` |
| `routing.data_validation_only` = true | Load `./validate-objects/SKILL.md` |
| `routing.code_conversion_only` = true | Load `./code-conversion-only/SKILL.md` |
| `routing.assessed` = false | Load `./setup/SKILL.md` |
| `routing.assessed` = true | Load `./migrate-objects/SKILL.md` |

Each sub-skill handles its own internal routing based on the full `routing` object.
</prescribed-path>

---

## State Queries

These answer common questions about project state without loading a sub-skill:

- **"What is the current state?"** — Call `migration_status(mode="summary")`, construct the narrative summary (as in Step 1), and present the progress checklist.
- **"What should I work on next?"** — Call `migration_status(mode="my_objects_summary")` to get per-`(task, object_type)` counts plus `errored_count` and `done_count`. Present the list and **ask the user what they want to work on — do not pick for them**. When the user picks a group, drill down with `migration_status(mode="my_objects_details", group=<id>)`.

- **"Show me objects that match rule X"** — Load `./migrate-objects/rule-engine/propagate/SKILL.md`.

- **"How do I extend / customize the migration plugin?"** / **"How do I override task X?"** — Load `./extensibility/TASKS.md` for the full reference: overridable task ids, per-task contracts, the project-local + `$AIM_SKILL_EXT_DIR` paths, and registering code units with `kind=custom` plus a free-form `customKind` discriminator. Optionally call `migration_status(mode='extensions')` to show which overrides are active.

- **"My migration also has FiveTran / SSAS / dbt / Airflow / Oracle PACKAGE bodies / scripts the engine doesn't generate"** / **"How do I track <non-built-in asset> in the migration?"** — Load `./setup/discover-extras/SKILL.md`. Registers each asset as a code unit with `kind=custom` and a `customKind` discriminator, then writes a `.scai/skills/<customKind>.md` cookbook with the customer so every object of that kind runs the same playbook (see `./extensibility/TASKS.md` → "Custom code units").

---

## Skill Match

<skill-match>
Match the user's request to the most relevant skill and load it.

**Routing rules:**
- Prefer the **parent (router)** skill when the child is ambiguous — it will route.
- Indentation = parent/child. A child only applies when its parent's domain already fits.
- If the request is ambiguous between siblings, ask one clarifying question.
- If no skill matches, fall back to the section below.

### SAS (Preview — parallel track, not SnowConvert)
- **sas** (Preview) — SAS → Snowflake: assess portfolios, convert `.sas` programs, or load `.sas7bdat` from a stage → `./sas/SKILL.md`
  - **assess-sas-migration** — portfolio complexity, dependency DAG, migration waves → `./sas/assess-sas-migration/SKILL.md`
  - **convert-sas-to-snowflake** — convert SAS programs to Snowflake SQL / stored procedures → `./sas/convert-sas-to-snowflake/SKILL.md`
  - **migrate-sas7bdat-to-snowflake** — bulk-load `.sas7bdat` from a stage into tables → `./sas/migrate-sas7bdat-to-snowflake/SKILL.md`
  - **validate-sas-conversion** — validate an existing SAS conversion → `./sas/convert-sas-to-snowflake/validate-sas-conversion/SKILL.md`
  - **register-sas-source-units** — populate the Code Unit Registry from `.sas` source files so `scai test` can see them → `./sas/register-sas-source-units/SKILL.md`
  - **register-sas-converted-units** — attach converted `.sql` to the CUR so `scai test` can validate the SAS conversion → `./sas/register-sas-converted-units/SKILL.md`

### Setup & onboarding
- **setup** — full setup, steps 1–5: connect, init, register, convert, assess → `./setup/SKILL.md`
  - **midway-entry** — existing project with source + pre-converted Snowflake SQL (SQL Server / Redshift only) → `./setup/midway-entry.md`
  - **configure-snowflake-target** — set or change the Snowflake connection and target database for object migration. Triggers: "change the target database", "deploy to a different database", "switch Snowflake connection" → `./setup/configure-snowflake-target.md`
  - **snowflake-connection** — create or repair a Snowflake target authenticator. Use for Microsoft Entra ID / Azure AD / OIDC (`oauth_authorization_code`); do not use `externalbrowser` for Entra → `./connection/snowflake-connection/SKILL.md`
  - **configure-testing** — pick or change the testing path (source-data vs synthetic) for procedure/function equivalence tests. Triggers: "change testing path", "switch to synthetic tests", "use query logs" → `./setup/configure-testing.md`
  - **data-validation-setup** — configure cloud data validation: schema, metrics, row-level checks → `./setup/data-validation/SKILL.md`
  - **data-infrastructure-teardown** — suspend SPCS service + compute pool, stop local worker (cost-saving) → `./data-infrastructure/teardown/SKILL.md`

### Data infrastructure (reusable actions)
- **data-infrastructure** — shared infrastructure for data migration and validation: compute pools, workers, network access → `./data-infrastructure/SKILL.md`
  - **worker-local-setup** — install and start the worker on a user-managed machine (laptop, VM, or on-prem) → `./data-infrastructure/worker-local-setup/SKILL.md`

### Source code: register & convert
- **register-code-units** — router for getting source code into the project → `./register-code-units/SKILL.md`
  - **extract-code-units** — extract DDL/code from a connected source database → `./register-code-units/extract-code-units/SKILL.md`
  - **add-code-units** — import local SQL files into the project → `./register-code-units/add-code-units/SKILL.md`
- **convert** — convert source → Snowflake SQL via SnowConvert (incl. optional Power BI `.pbit` and Tableau `.twb`/`.tds` repointing) → `./convert/SKILL.md`
  - **code-conversion-only** — convert local source files for code-conversion-only source systems (incl. optional Power BI `.pbit` repointing) → `./code-conversion-only/SKILL.md`
  - **powerbi-repointing** — collect `.pbit` folder path and `--powerbi-repointing` flag for Power BI repointing → `./powerbi-repointing/SKILL.md`
  - **tableau-repointing** — collect `.twb`/`.tds` folder path and `--tableauRepointing` flag for Tableau repointing. Triggers: tableau, tableau migration, tableau repointing, migrate tableau, repoint tableau → `./tableau-repointing/SKILL.md`
- **assessment** — analyze workloads: waves, object exclusion, dynamic SQL, ETL → `./assessment/SKILL.md`

### Migration & validation
- **migrate-objects** — deploy tables, views, functions, procedures wave-by-wave → `./migrate-objects/SKILL.md`
  - **migrate-etl** — claim an ETL code unit, then stabilize it. Entry point for "fix ETL package", "fix SSIS/Informatica conversion", "proceed with stabilization", "resume ETL fixing" — it claims the unit (so it appears in `my_objects_summary` with the current user as owner) before delegating to the phase-based etl-stabilization engine. → `./migrate-objects/migrate-etl/SKILL.md`
  - **data-migration-setup** — choose approach, generate workflow YAML, create target database for `migrate_data` → `./migrate-objects/actions/data-migration/SKILL.md`
  - **testbed-generator** — mine → validate → compile → generate the synthetic testbed for a workload: run/resume each phase, inspect unsolved constraints, readiness, and data-coupling clusters. Triggers: generate testbed, mine testbed, validate testbed, compile testbed, testbed data source → `./migrate-objects/baseline-capture/testbed-generator/SKILL.md`
- **validate-objects** — validate data between a source and Snowflake, including project-based Snowflake-to-Snowflake validation. Triggers: "validate Snowflake to Snowflake", "compare Snowflake tables/databases", "run SF-to-SF DV" → `./validate-objects/SKILL.md`

### Object metadata
- **tag-objects** — tag or untag code units with the user's own labels (`extensions.tags`), and find objects by tag. Triggers: "tag this table", "label these objects", "untag", "which objects are tagged" → `./tag-objects/SKILL.md`

### Rules
- **rule-engine** — search, apply, and manage migration rules → `./migrate-objects/rule-engine/SKILL.md`
  - **extract-rule** — extract a reusable rule from a code fix (interactive or git history) → `./migrate-objects/rule-engine/extract/SKILL.md`
  - **propagate-rule** — find all code units matching a rule for batch application → `./migrate-objects/rule-engine/propagate/SKILL.md`

### Customization
- **task-overrides** — replace the skill that runs for any built-in task with the user's own `SKILL.md`, scoped to the project or to a global directory via `$AIM_SKILL_EXT_DIR`. Triggers: "extend the plugin", "customize task X", "swap out the skill for Y", "override registerCode/convertCode/deploy/...". Reference: `./extensibility/TASKS.md`
- **discover-extras** — register assets the conversion engine doesn't generate (FiveTran, dbt, Airflow, Informatica, SSAS cubes, Oracle PACKAGE bodies, custom shell scripts) as code units with `kind=custom` and a free-form `customKind` discriminator (any string outside the reserved `databaseObject` / `script` / `etl` / `custom` set) so they flow through orchestration alongside built-in units. Triggers: "I have FiveTran / SSAS / dbt / a script that touches the database", "register custom asset", "track <non-built-in> in the migration". Skill: `./setup/discover-extras/SKILL.md`. Reference: `./extensibility/TASKS.md` (Custom code units).

## Fallback

If no skill matches, say so explicitly, then help with your own knowledge.
</skill-match>


## Rules

1. **Configure returns status** — `configure(project_dir=...)` includes the `## Migration status` block; route from it. No separate `migration_status` call on the continue path.
2. **Follow sub-skill instructions** — Complete each sub-skill fully before returning
3. **Confirm transitions** — Ask user before moving to next stage
