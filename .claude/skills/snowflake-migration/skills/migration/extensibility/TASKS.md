# Customizing the migration plugin

The plugin walks each object through a sequence of tasks (register → convert → deploy → validate → ...). You can replace the skill that runs for any task with your own — useful when your team has a non-standard step (custom auth, in-house deploy tooling, extra validation, ...) without re-implementing the whole plugin.

This page is the contract you need: the list of overridable task ids, what each task is expected to do, and how to signal completion.

## How to override a task

Drop a `SKILL.md` under either path; the plugin loads it instead of the built-in skill the next time that task runs.

| Path | When to use |
|---|---|
| `<project_dir>/.scai/skills/<task_id>/SKILL.md` | Override scoped to a single project. Project-local overrides take precedence. |
| `$AIM_SKILL_EXT_DIR/<task_id>/SKILL.md` | Set `AIM_SKILL_EXT_DIR` to a directory you maintain (e.g. a shared internal skills repo). Used as a fallback when the project does not carry the override. |

Your override SKILL.md is loaded as a normal agent skill — write it the same way you would any other skill. There is no template to subclass and no required imports.

To replace the entire `main` pipeline for one `customKind` (FiveTran, Airflow, …), discovery writes `<project_dir>/.scai/skills/<customKind>.md` with the customer — see [Custom code units](#custom-code-units-kindcustom). That is a file, not a `<task_id>/SKILL.md` directory.

To check what's currently in effect, run:

```
migration_status(mode='extensions')
```

It returns the catalog of every overridable task, the default executor the plugin would use, and the path of any active override.

## How to exclude a task

Some tasks aren't relevant to every project. Disable one with the `configure` tool's `tasks` parameter — the plugin then treats it as `excluded` and follows the task's `excluded` branch instead of running it:

```
configure(tasks={"validateView": false})
```

The choice persists to `<project_dir>/.scai/config/plugin.yml` under `tasks.*`, so it holds across sessions.

- **Locked tasks can't be disabled.** Load-bearing steps are marked `locked` in the machine — `configure` rejects disabling them (the core setup steps, plus `registration`, `convert`, `deploy`, `etlStabilization`, `seedSynthetic`, `fixCode`).
- **Structural nodes can't be disabled.** Internal prompts, routers, and terminals have no executor to override — `configure` rejects attempts to exclude them too.

## Task catalog

Tasks fall into two categories: `setup` (one-time per project) and `main` (per-object migration). Below is every task id you can override; internal routing nodes and setup prompts are not listed.

<cat>

### `setup` (one-time per project)

| Task id | What it does |
|---|---|
| `midwayEntry` | Imports an existing pre-converted Snowflake project to be compatible with AIM projects. |
| `configureGit` | Configures git integration (main branch, remote, housekeeping commits). |
| `configureSourceConnectionExtract` | Configures the source database connection. |
| `registerCode` | Pulls source SQL into the project. |
| `convertCode` | Runs the source → Snowflake conversion. |
| `runAssessment` | Generates a migration assessment report. |
| `configureSourceConnectionTesting` | Configures the source database connection (needed for source-data testing path). |
| `configureTesting` | Verifies the Snowflake side is ready for the chosen testing path (source data vs synthetic). |
| `generateTestbed` | Builds the synthetic testbed for the workload (mine → validate → compile → generate). Reached only on the synthetic testing path. |
| `configureSourceConnectionData` | Configures the source database connection (needed for data migration/validation infrastructure). |
| `setupDataInfrastructure` | Configures the shared Data Migration & Validation infrastructure (compute pool for SPCS, or local) and generates the worker config, so it can be brought up at migration time with data_infrastructure(mode="up"). |
| `dataStrategy` | Captures the project's data migration and validation strategy (migration type, sync strategy, extraction strategy, target table type; validation type + sync strategy) during setup so the choices are committed to the git main branch and shared with the team, instead of being decided ad hoc at first migration/validation. Snowflake-source projects skip the migration wizard and complete on validation type only. |

### `main` (per-object migration)

| Task id | What it does |
|---|---|
| `registration` | Register (or update) one object's source DDL (per-object). |
| `convert` | Converts one object via SnowConvert (per-object). |
| `etlStabilization` | Stabilizes a converted ETL code unit (SSIS, Informatica, ...) and validates the functionality. |
| `etlSeed` | Runs `scai test seed` to generate the per-unit ETL test YAML (pipeline + validation.tables) with the source/target table pairs filled from the Code Unit Registry write-dependencies; the agent fills index_columns and the user confirms before validation runs. |
| `etlValidate` | Runs `scai test etl-validate --platform <platform>` to compare source package output with the converted Snowflake output. |
| `generateTestCases` | Generates a per-object test-case YAML from source-connected inputs (via `scai test seed`); reads source to build the cases, never writes to source. |
| `seedSynthetic` | Generates synthetic test inputs. |
| `seedScript` | Writes a BTEQ script's test YAML, resolving binding values and staging .IMPORT fixtures from the shell script that runs it via `scai test seed --bindings-from`; values that can't be resolved statically become `{ eval }` recipes or stay `__REPLACE_ME__` for manual fill, and bindings shared across scripts are hoisted to the global test_config.yaml. Requires the bteq binary on PATH. |
| `captureBaseline` | Captures a source object's output as a test baseline (procedures, functions, and BTEQ scripts). |
| `deploy` | Deploys one object to Snowflake. |
| `validateView` | Validates a deployed view against its source. |
| `migrateData` | Migrates data into a deployed table (pure dispatch — requires the shared orchestrator+worker to be up). |
| `validateData` | Validates migrated data against the source (pure dispatch — requires the shared orchestrator+worker to be up). |
| `runTests` | Runs the scai test suite for an object. |
| `verify` | Catch-all verification for a converted object whose type has no deploy/test path of its own (Oracle PACKAGE, PACKAGE_BODY, TYPE, TYPE_BODY, SYNONYM, ...), and for procedures/functions with no source side after they deploy (SnowConvert UDF helpers). Reached via convert's unfiltered `completed` transition (must stay last) or via deploy when `source IS NULL`. |
| `extractRules` | Extracts reusable migration rules from a fix. |
| `applyRules` | Applies matched migration rules to an object. |
| `fixCode` | Diagnoses and fixes a failing object. |

</cat>

## Outcome vocabulary

Every task resolves to one **outcome**. Read-only detection (the resolver seeing a status source satisfied) and the `transition_status(status='advance', outcome=…)` write speak the same vocabulary:

| Outcome | Meaning |
|---|---|
| `completed` | The task finished successfully. |
| `failed` | The task could not finish; carries an `error` class (below). Routes into the fix loop, or the errored bucket. |
| `excluded` | The task was disabled for this project/object (see [How to exclude a task](#how-to-exclude-a-task)); the machine follows the task's `excluded` branch. |
| `skipped` | Deferred for now (not disabled) — the task may still run later. |
| `inProgress` | The task has started but has not completed. It remains the current blocking task. |

**`error` classes** (required on `failed`):

| Class | Use for |
|---|---|
| `sql` | A SQL/DDL bug the fix loop can address. |
| `infra` | A transient environment failure (timeout, connection drop, cancelled run) — retry with `reset`. |
| `human` | Only a person can resolve it. Don't set this class by hand — call `transition_status(status='escalate', task=…, asks=[…])`, which sets it for you. Passing `outcome='failed'` without an error class instead sends the object into the fix loop, where no code change resolves it. A judgment you *can* make is `status='note'` (does not park; review later), not this class. |

## Per-task contracts

Every entry below names the task id, what your override needs as input, and the signal that tells the plugin the task is complete. "Done when" is the only completion contract — once the listed condition holds, the plugin moves on.

> **Signaling completion.** After the work, call `migration_status` to pick up the next task. The plugin reads the "Done when" condition (a registry field, a file on disk, an object in Snowflake) and advances. Call `transition_status(status='advance', task='<task_id>', outcome=…)` to report a failure, a judged outcome the plugin cannot observe, or an override (`bypass` / `reset` / `skip`). A registry-field "Done when" reads completed when `status = 'completed'` (or when the field exists, if it has no `status`).

> **Signaling completion via session config.** Setup tasks that gather user choices complete by calling the `configure` MCP tool with the relevant field set (e.g. `configure(source_language='sqlserver')`). The plugin reads from the session config to know the task is done.

<cntrc>

### `setup` (one-time per project)

#### `midwayEntry`
- **Inputs:** An existing project tree containing source SQL and pre-converted Snowflake SQL.
- **Done when:** Project is initialized (`.scai/config/project.yml`) and at least one file exists under both `source/**/*.sql` and `snowflake/**/*.sql` (produced by `scai code sync`).

#### `configureGit`
- **Inputs:** A user who has opted into git, or a project directory that was already a git repository at setup start.
- **Done when:** Session config has `git_main_branch` set, or a pending init is parked until `scai init`.

#### `configureSourceConnectionExtract`
- **Done when:** Session config has `source_connection` set — call `configure(source_connection=...)`.

#### `registerCode`
- **Inputs:** Either a configured source connection (extracted via scai) or a folder of `.sql` files to register as-is.
- **Done when:** Project is initialized and at least one file exists at `<project_dir>/source/**/*.sql`.

#### `convertCode`
- **Inputs:** Registered source code from the `registerCode` task.
- **Done when:** Project is initialized and at least one file exists at `<project_dir>/snowflake/**/*.sql`.

#### `runAssessment`
- **Inputs:** A converted project from the `convertCode` task.
- **Done when:** At least one assessment report HTML exists under `<project_dir>/**/assessment/**/*report*.html`.

#### `configureSourceConnectionTesting`
- **Done when:** Session config has `source_connection` set — call `configure(source_connection=...)`.

#### `configureTesting`
- **Inputs:** A Snowflake connection and target database from `configureSnowflakeTarget`; the testing path choice from `chooseTestingPath`; optionally a query-log CSV.
- **Done when:** Session config has `testing_data_source` set — call `configure(testing_data_source=...)`.

#### `generateTestbed`
- **Inputs:** A converted, assessed workload with testbed mining artifacts under `artifacts/**/testbed/*.testbed.json`. A source connection is still required downstream.
- **Done when:** The generate deliverable exists at `**/testbed/generate/summary-view.json` (synthetic-data summary; each table's CSV lands under its object's `<artifacts>/testbed/` folder and `manifest.json` beside `state.bin`).

#### `configureSourceConnectionData`
- **Done when:** Session config has `source_connection` set — call `configure(source_connection=...)`.

#### `setupDataInfrastructure`
- **Inputs:** A configured Snowflake target and source connection.
- **Done when:** Either `.scai/config/dew_configuration.toml` (worker config, written for both local and SPCS) or `.scai/settings/cloud-migration.yaml` (SPCS compute pool) exists. The setup walkthrough writes the worker config, so local completes here too — unlike the dashboard `dataInfrastructure` tile, which still requires a compute pool.

#### `dataStrategy`
- **Inputs:** A source language chosen in setup and the intent to migrate/validate table data (the data-infrastructure step establishes that intent).
- **Done when:** Session config has `data_validation_type` set. Non-Snowflake sources also need `data_migration_type` — the data-migration-setup and data-validation-setup wizards (`progress_setup(mode="data_migration"|"data_validation")`) have both run to completion. Snowflake-source projects skip the migration wizard.

### `main` (per-object migration)

#### `registration`
- **Inputs:** Object id with source DDL available.
- **Done when:** Registry field `codeStatus.registration` reads completed.

#### `convert`
- **Inputs:** Registered object.
- **Done when:** Registry field `codeStatus.conversion` reads completed.

#### `etlStabilization`
- **Inputs:** A converted ETL code unit (converted artifacts + source definition resolved from its registry entry); its dependency tables deployed.
- **Done when:** Registry field `codeStatus.stabilization` reads completed.

#### `etlSeed`
- **Inputs:** Stabilized ETL unit deployed to Snowflake (deploy enforced via precondition).
- **Done when:** Registry field `codeStatus.etlSeed` reads completed.

#### `etlValidate`
- **Inputs:** ETL test YAML present (from etlSeed or hand-authored); ETL unit deployed to Snowflake and source/Snowflake connections configured — all enforced via preconditions.
- **Done when:** `scai test etl-validate` stamps registry field `codeStatus.etlValidate` completed (failed runs stamp failed + error). Units skipped for a missing YAML stay pending.

#### `generateTestCases`
- **Inputs:** Object that needs test inputs; configured source connection.
- **Done when:** Per-object YAML exists at `<project_dir>/<files.artifacts.path>/test/<name>.yml`.

#### `seedSynthetic`
- **Inputs:** Object that needs test inputs (no source connection required).
- **Done when:** Per-object YAML exists at `<project_dir>/<files.artifacts.path>/test/<name>.yml`.

#### `seedScript`
- **Inputs:** A converted BTEQ script unit; the shell script(s) that set its variables and run bteq (plus any invocation args); configured source connection; bteq binary installed.
- **Done when:** Per-object YAML exists at `<project_dir>/<files.artifacts.path>/test/<name>.yml`.

#### `captureBaseline`
- **Inputs:** Object with seed data; configured source connection.
- **Done when:** Procedures/functions: `VALIDATION.BASELINE_METADATA` has a row for the object's target name whose `ROW_COUNTS` sum to more than zero. BTEQ scripts have no rows in that table, so they fall through to registry field `extensions.tasks.captureBaseline`.

#### `deploy`
- **Inputs:** Converted SQL for the object.
- **Done when:** Registry field `cloudStatus.deployment` is set, or the deployed-object metadata exists in Snowflake.

#### `validateView`
- **Inputs:** Deployed view; configured source connection.
- **Done when:** Registry field `extensions.tasks.validateView` reads completed.

#### `migrateData`
- **Inputs:** Deployed table; configured source connection; shared data infrastructure brought up once via data_infrastructure(mode="up").
- **Done when:** Live cloud migration job reports the table loaded (DATA_MIGRATION.TABLE_PROGRESS).

#### `validateData`
- **Inputs:** Object with migrated data; shared data infrastructure brought up once via data_infrastructure(mode="up").
- **Done when:** Live cloud validation job reports every enabled level done (DATA_VALIDATION.TABLE_PROGRESS_DETAIL).

#### `runTests`
- **Inputs:** Object with a captured baseline; procedures and functions are also deployed first (BTEQ scripts are not).
- **Done when:** The latest run of every test case in `VALIDATION.RESULTS` passed. Procedures and functions are judged there; BTEQ scripts have no rows in that table, so they fall through to registry field `codeStatus.testing`.

#### `verify`
- **Inputs:** A converted object of a type the machine routes nowhere else, or a deployed procedure/function with no source counterpart.
- **Done when:** Registry field `extensions.tasks.verify` reads completed.

#### `extractRules`
- **Inputs:** A fixed object's diff (the change you want to make reusable).
- **Done when:** Registry field `extensions.tasks.extractRules` is set, or the object's converted SQL is unchanged since its last conversion.

#### `applyRules`
- **Inputs:** An object with outstanding issues that one or more migration rules apply to.
- **Done when:** Registry field `extensions.tasks.applyRules` is set.

#### `fixCode`
- **Inputs:** A failing object (compilation error, EWI, test failure).
- **Done when:** Registry field `extensions.tasks.fixCode` is set.

</cntrc>

## Custom code units (`kind=custom`)

Per-task overrides and custom machines are about **how** work runs. Custom code units are about **what** work runs on. The conversion engine generates a known set of object kinds (tables, views, procedures, functions, SSIS packages, …); anything outside that — orchestration tools (FiveTran, Airflow, Informatica), BI assets (SSAS cubes, Tableau extracts, dbt models), object kinds the engine doesn't generate yet (Oracle PACKAGE bodies, SQL Server triggers in some flows), or hand-maintained scripts — won't show up in the registry unless you put it there yourself.

The registry's top-level `kind` is a closed enum with four values: `"databaseObject"`, `"script"`, `"etl"` (the three the conversion engine emits) and `"custom"` (everything else). Custom units carry an additional `customKind` discriminator on `source` and `target` — that's the free-form string the agent uses to group, filter, and route. Each custom unit carries:

- **`kind`** — always `"custom"` for these units. The closed enum keeps registry queries and bindings simple.
- **`source.customKind` / `target.customKind`** — the free-form discriminator (`"fivetran"`, `"ssasCube"`, `"oraclePackage"`, `"airflowDag"`, …). Pick a stable name; this is what `query_registry where="source.customKind = '<x>'"` filters on. Cannot be one of the four reserved Kind values.
- **`source.name`** — display name.
- **`source.objectType`** — *optional*. When the asset maps cleanly to a built-in `ObjectType` (e.g. an Oracle PACKAGE → `package`), set it so the unit groups with its siblings in `migration_status`. `"other"` is fine when nothing fits.
- **`files.source.path`** — *optional* path to a config file or definition, **relative to the project root** (e.g. `"source/fivetran/orders_sync/connector.py"`). Assets living outside the project must be copied under `<project_dir>/source/` first; an absolute or escaping path is reported in `warnings[]` because it breaks for every other checkout.
- **`dependencies.dependsOn[]`** — ids of other units (built-in or custom) this one reads/writes. `requiredBy` back-edges and `planning.topologicalRank` are derived from this by the registry on every write — never hand-write either.
- **`extensions.machine`** — name of the state machine that drives this unit, as a plain string. Only the four compiled-in machines resolve (`main`, `setup`, `data-migration-setup`, `data-validation-setup`); see the gap note below. When unset or unresolvable, a `.scai/skills/<customKind>.md` skill (if present) replaces `main`; otherwise the unit walks `main`.

### Registering custom units

One tool, `register_units`, three shapes. Search that name if the tool is not already loaded — there is no `register_custom_unit` / `register_custom_units_from_manifest`.

| Shape | Call | When |
|---|---|---|
| One unit | `register_units(custom_kind, name, ...)` | Walking the user through one item. |
| A list | `register_units(entries=[...])` | Manifest with many entries (CSV/JSON/YAML the user has on hand). |
| Findings | `register_units(expected_slugs=[...])` | Investigation agents already wrote `.scai/tmp/extras/findings/<slug>.json`. |

It rejects the four reserved Kind values (`databaseObject`, `script`, `etl`, `custom`) as a `customKind`. Built-in kinds go through the regular `scai code add` / `scai code extract` paths. Per-row failures are collected into `failed[]` rather than aborting the run.

Snake_case (`custom_kind`, `source_path`, `depends_on`, `expected_slugs`) and camelCase (`customKind`, `sourcePath`, `dependsOn`, `expectedSlugs`) both work. `dependsOn` takes either a JSON array of ids or a comma/newline-separated string.

Every shape returns the same envelope — `registered[]` (each row has `id`, `customKind`, `name`, `machine`, `dependsOnResolved`, `dependsOnMissing`, `warnings`) plus `failed[]` / `withMissingDependencies[]` / `withWarnings[]`. Read `dependsOnMissing`: ids in it are recorded but match no unit, which is expected when the dependency is registered later and a typo otherwise. Read `warnings`: an unresolvable machine name (unit uses a `.scai/skills/<customKind>.md` skill if present, otherwise `main`) or a `sourcePath` that isn't repo-relative. Don't re-query to confirm the write — `query_registry`'s default projection is `id` / `source` / `files`, so `dependencies` and `extensions` come back absent and the unit looks empty. Pass `fields=["*"]` if you do need to read them back.

Investigation fans out; the write does not. Investigation agents write one JSON fragment each under `.scai/tmp/extras/findings/<slug>.json`. The orchestrator calls `register_units(expected_slugs=[...])`, which merges those files and registers — it does not concatenate fragments in context. Registry writes take an exclusive lock and each triggers a registry-wide graph refresh, so parallel writes from the agents themselves are slower than one batch and fragment the failure report.

### Per-customKind skills

Discovery writes `<project_dir>/.scai/skills/<customKind>.md` with the customer (one cookbook per kind, reused for every object of that kind). When that file exists, those units skip `main` (register → convert → …) and run the skill as their whole workflow. Completion is the same stamp `verify` already uses:

```
transition_status(status='advance', task='verify', outcome='completed', where="id IN ('<id>')")
```

Done when `extensions.tasks.verify` reads completed. `next_objects` / `next_task` carry `skillPath` pointing at the file. The file must be a procedure (On Entry → steps → stamp); see `setup/discover-extras/cookbook-template.md`.

A loaded `extensions.machine` still wins when that name is compiled in. A `verify/SKILL.md` task override does not steal these units.

### Gap: per-customKind machines are not implemented

`Machines` loads only the four machines compiled into the server. Nothing reads `<project_dir>/.scai/machines/`, so a machine file written there is inert, and `extensions.machine` naming it resolves to nothing — `machine_for_unit` then uses a `.scai/skills/<customKind>.md` skill if present, otherwise `main`.

Consequences to keep in mind when extending this area:

- Don't author a per-`customKind` machine file and report the flow as wired. The fallback is silent at resolve time; the only signals are `warnings[]` on each `registered[]` row (`withWarnings[]` on the `register_units` report) and the `Warning:` line from `update_registry(field="extensions.machine", ...)`.
- The executor kinds are `mcpTool`, `shell`, and `agent`. There is no `manual` kind and no `instructions` field — a machine using them fails to deserialize, which is a second reason a hand-written machine never takes effect.
- Making this real means loading and validating `.scai/machines/*.json` into `by_name` alongside the built-ins, and threading `project_dir` into the ~15 `Machines::load_builtin()` call sites. That's a feature, not a doc fix.

### Invoking discovery

The skill at `setup/discover-extras/SKILL.md` registers the units, then co-authors a `.scai/skills/<customKind>.md` cookbook per kind with the customer. Load it when the user has extras to register — it is not a step in the compiled `setup` machine.

Re-entering the skill at any time afterward is safe — it picks up where the user left off and lets them add more units.

### Worked example: FiveTran sync depends on a table

1. Register the FiveTran sync as a custom unit pointing at the table it reads from:
   ```
   register_units(
     custom_kind="fivetran",
     name="orders_sync",
     source_path="source/fivetran/orders_sync.yaml",
     depends_on=["<id-of-dbo.Orders-table>"],
     description="Daily ingest from Shopify",
   )
   ```
   Check `dependsOnMissing` on the registered row — if the table id is in there, look it up again with `query_registry` before moving on. `requiredBy` on the table and `topologicalRank` on the sync are filled in by the registry; don't touch them.
2. Discovery writes `.scai/skills/fivetran.md` with the customer (what "done" means, how one connector is migrated). Leave `machine` unset — a `fivetran-flow` machine can't load (see the gap above).
3. Run `migration_status(mode="next_objects")` — once the table the sync depends on is migrated, the FiveTran sync appears in the queue with `skillPath` pointing at that cookbook.
