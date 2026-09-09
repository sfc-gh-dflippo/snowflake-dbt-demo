---
name: migrate-etl
description: Stabilize an ETL code unit (SSIS, Informatica, or other platforms) by handing the converted artifacts off to etl-stabilization and recording the result on the registry entry.
parent_skill: migrate-objects
license: Proprietary. See License-Skills for complete terms
---

# Migrate ETL

Wraps [actions/etl-stabilization/SKILL.md](../actions/etl-stabilization/SKILL.md) so it runs as a state-machine task on a single ETL code unit.

The platform of an ETL code unit is recorded on its registry entry as `source.platform` (`ssis`, `informatica`, …). `etl-stabilization` already covers every supported platform via per-platform profiles in `actions/etl-stabilization/platforms/`. This skill does not replicate that work — it only:

1. Resolves the converted-artifacts folder and source-definition paths from the registry entry.
2. Invokes `etl-stabilization` against them.
3. Updates `codeStatus.stabilization` on the registry entry when etl-stabilization finishes (or the unit is excluded).

## Scope

**Stabilization** for this version means: run `etl-stabilization` until its Final Validation phase reports clean. That covers everything `etl-stabilization` does — scan, ROADMAP, phased TDD across orchestration elements and dbt sub-projects, EWI fixes, etc.

**After stabilization:** the unit advances to `deploy`. Deploying the stabilized ETL to Snowflake is handled by `scai code deploy` through the `deploy` tool (see Step 4), not by this skill and not by hand-running `snow`. Deploy is no longer terminal for ETL — once deployed, the unit advances to `etlSeed` and `etlValidate` to compare the live source package against the Snowflake output.

This skill is the **orchestrated (registry-backed) entry point** for ETL stabilization. It claims the unit and records the result on the registry, then delegates the actual fixing to `etl-stabilization`.

## Step 0: Claim Ownership

The ETL unit must be claimed before stabilization begins, so it is registered in `MIGRATION_REGISTRY.claims`, shows the current user as owner, and appears in `my_objects_summary` alongside SQL objects. Resolve `<etl_id>` first: the executor passes `object_id`; if entered by name ("fix ETL package …"), locate the unit via `migration_status(mode="my_objects_summary")` (already-claimed) or `migration_status(mode="next_objects")` (not yet claimed).

**Resumption check first.** If `{UNIT}/stabilization/tracking/STATE.md` already exists, stabilization is already in progress and the unit was claimed on a prior run — **skip claiming** and go to Step 1.

**Otherwise claim it:**

```
transition_status(status="begin", where="id = '<etl_id>'")
```

`begin` is idempotent (it refreshes the claim if the unit was already claimed via the picker), so it is safe to call whenever no `STATE.md` exists. Surface any error and stop without retry.

## Step 1: Resolve Inputs From the Registry

Read the unit (the executor passes `object_id`, or call `migration_status(mode="my_objects_details", group=<id>)`):

| Field | Used as |
|---|---|
| `files.source.path` | source definition file (e.g. `.dtsx` for SSIS, `.xml` for Informatica) — `{SOURCE_FILE_PATH}` for `etl-stabilization` |
| `source.platform` | `{PLATFORM_ID}` for `etl-stabilization` (skip its Step 1b auto-detect prompt) |
| `parts[]` → derived converted folder | `{PACKAGE_FOLDER}` for `etl-stabilization` |

**Deriving the converted folder.** Where the converted output lives depends on the conversion flavor:

**dbt / SSIS ETL** — recorded per part in `parts[].target`:
- Data-flow parts (e.g. `partType: "Microsoft.Pipeline"` for SSIS) → `target.format: "dbt"`, `target.path` points to a **dbt project folder** (one per data flow).
- Other part types (e.g. `Microsoft.ExecuteSQLTask` for SSIS) → `target.format: "snowflakeSQL"`, `target.path` points to a single **orchestration `.sql` file** shared by every non-dbt part of this code unit.

Resolve `{PACKAGE_FOLDER}` as the parent directory of any part whose `target.format == "snowflakeSQL"`. The dbt sub-project folders should sit alongside that orchestration file under the same parent — verify before handing off. If `parts[]` is empty or no part has a `target` yet, the converted output has not been produced — the `convert` task should have run first. Surface that to the user and stop; do not try to stabilize an unconverted ETL unit.

**Snowflake Scripting ETL** (project `etl_target = snowflake_scripting`) — each converted mapping is its own `kind=etl` unit with an **empty `parts[]`**; the converted stored procedure is on the code-unit root at `files.converted.path` (`target.format: "snowflakeSQL"`), and there are **no dbt sub-project folders**. Resolve `{PACKAGE_FOLDER}` as the parent directory of `files.converted.path`. An empty `parts[]` here is **expected** — not a sign of missing conversion; only treat the unit as unconverted if `files.converted.path` is also absent.

## Step 2: Hand Off to `etl-stabilization`

Load [../actions/etl-stabilization/SKILL.md](../actions/etl-stabilization/SKILL.md) and run its workflow with the inputs from Step 1. You are skipping its Step 1 (Gather Inputs) prompt because the registry already provides every value it would have asked for.

Follow `etl-stabilization` end-to-end:
- no `STATE.md` yet → its Planning Workflow (scan → context-mapping → ROADMAP → user approval at Step 9) → Execution Workflow.
- existing `STATE.md` → straight into Execution Workflow at the next pending phase.

Stay there through Final Validation. **Do not exit back to this skill phase-by-phase** — `etl-stabilization` is autonomous between its declared stopping points.

## Step 3: Mark Completion

When `etl-stabilization` finishes its Final Validation cleanly, advance the state machine:

```
transition_status(status="advance", task="etlStabilization", outcome="completed", where="id = '<etl_id>'")
```

`etlStabilization` is not terminal: on `completed` the machine advances the unit to `deploy` (which deploys the converted ETL via `scai code deploy`). Continue to Step 4 to deploy. After a successful deploy the unit advances to `etlSeed` and then `etlValidate` for the live source-vs-Snowflake comparison (see `etl-seed/SKILL.md` and `etl-validate/SKILL.md`, loaded automatically by the executor).

## Step 4: Deploy

Once `etlStabilization` is `completed`, the unit sits at the `deploy` task. Deploy it with the `deploy` MCP tool, selecting the ETL by `where = "kind = 'etl'"` (the canonical ETL selector) or by `object_name` / `where = "id = '<etl_id>'"`. The tool runs `scai code deploy`, which understands ETL code units end to end.

**Select the ETL by `kind`, not `objectType`.** ETL units are matched by `kind = 'etl'` (lowercase, case-sensitive). They are NOT matched by `source.objectType` / `target.objectType`, which report `other` for ETL, so `source.objectType = 'etl'` matches nothing. If the `deploy` tool is unavailable (e.g. deferred, reachable only via `tool_search` / `python_repl`) or a `configure` call stalls, do not keep fighting it: run the equivalent command directly. It is self-contained (takes the connection with `-c`, needs no prior `configure`): `scai code deploy -c <connection> -d <database> --where "kind = 'etl'"` (never `source.objectType = 'etl'`, and still no hand-rolling).

**Do NOT hand-roll the deployment, and do NOT run the pipeline by hand.** No manual `snow dbt deploy`; no executing the orchestration SQL or helper DDL by hand; no building or recreating the task graph yourself (`CREATE OR REPLACE TASK`); no seeding tables or running models (`EXECUTE DBT PROJECT`); no `EXECUTE TASK`. Deploy only **creates** the objects (the task graph is left suspended) - running it is a separate, later step (see Activation), and only when the user asks. `scai code deploy` already does the deploy, in order:

- **Supporting helpers first:** the `control_variables` transient table and any shared `etl_configuration` functions/procedures and `file_formats` the packages depend on.
- **The dbt project(s):** each converted data flow registered as a dbt project.
- **The orchestration task graph:** created **suspended**, so nothing runs until you choose to activate it. These are Snowflake Task Graphs (Snowflake owns the scheduling); the converted SQL only defines the tasks.
- **Telemetry:** a `COMMENT` is set on each deployed object to record that it came from this tool.

After a successful deploy with the graph left suspended, the tool reports the suspended tasks so the user knows the graph will not run on its own.

**Tell the user WHERE it deployed (proactively, and never guess the account).** Right after a successful deploy, print a short "Deployed to" summary so the user does not have to ask, and so no connection detail is ever invented:

- **Connection / account:** the connection you deployed with (the `-c` value). Read its `account` and `host` from `snow connection list` or `~/.snowflake/connections.toml`. NEVER guess or assume the account, account locator, region, or Snowsight server. If you cannot read it from the connection, say so. Do not fabricate one (a wrong link is worse than none).
- **Database / schema:** the `-d` database and the schema the package deployed into (schema defaults to the connection's schema, else `PUBLIC`).
- **Deployed objects:** list each by fully-qualified name `DATABASE.SCHEMA.NAME` - the task-graph root task, its child tasks, and each dbt project - from the deploy result.
- **Snowsight link:** when the account is in `ORG-ACCOUNT` form, the base is `https://app.snowflake.com/<ORG>/<ACCOUNT>/`; link to the schema's object browser by appending `#/data/databases/<DATABASE>/schemas/<SCHEMA>`. If the account is a bare locator (no `ORG-ACCOUNT`), give the account, the FQNs, and the Snowsight home only, and note the deep path may need adjusting. Still never invent a locator or region.

The task graph is suspended, so this link is for inspecting the created objects, not a running pipeline.

**Activation (only when the user asks to run or activate the tasks).** Pass `snowflake_task_activate = true` to the `deploy` tool. It resumes each task graph's child tasks. The converted root tasks have no SCHEDULE or AFTER clause, so Snowflake will not resume the root itself; that is expected and is reported as a note, not an error. Run a suspended-root graph on demand with `EXECUTE TASK`.

When the deploy returns success, advance the machine:

```
transition_status(status="advance", task="deploy", outcome="completed", where="id = '<etl_id>'")
```

On `completed` the machine routes the ETL unit to `etlSeed` (scaffold the test YAML), then `etlValidate` (live comparison). The executor loads those skills automatically.

If the deploy fails and you cannot resolve it, call the same transition with `outcome="failed"` and a short `error=` summary, then surface it to the user.

## Step 5: Failures

If `etl-stabilization` halts because of an issue it cannot resolve on its own, mark the task as failed:

```
transition_status(status="advance", task="etlStabilization", outcome="failed", error="<short summary>", where="id = '<etl_id>'")
```

Then surface the issue to the user for resolution. When resolved, retry from Step 2 — `etl-stabilization` will resume from `STATE.md`.

Anything that is **not** resolvable within `etl-stabilization` (corrupt converted output, missing source file, Snowflake-side infrastructure problem) should be handled as an Error Recovery case within that skill before retrying.

## Step 6: Exclusion

If the user decides this ETL unit is out of scope (deprecated, replaced, manual migration), mark it out of scope:

```
update_registry(field="inScope", status="false", objects="<etl_id>")
```

Out-of-scope units stop appearing in `next_objects` and stop counting toward migration totals.
