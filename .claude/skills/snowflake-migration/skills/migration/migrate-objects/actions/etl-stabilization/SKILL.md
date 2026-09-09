---
name: etl-stabilization
parent_skill: migrate-etl
description: >
  Phase-based orchestrator for fixing SnowConvert ETL conversion gaps in
  ETL-to-Snowflake migrations (SSIS, Informatica, and other platforms).
  Analyzes units holistically, creates a ROADMAP with test strategies,
  and executes fixes through phased TDD with cross-phase learning.
  Use when user says "fix ETL unit", "fix SSIS conversion", "fix Informatica conversion",
  "resume ETL fixing", "run next phase", or when processing a converted ETL unit folder
  containing orchestration SQL, optional dbt sub-projects, and the original
  source definition file (e.g., DTSX for SSIS, XML for Informatica). Do NOT
  use for non-ETL migrations or greenfield dbt projects.
license: Proprietary. See License-Skills for complete terms
---

# ETL Orchestrator

Fix SnowConvert ETL conversion gaps through phased execution with upfront unit analysis, agent-determined test strategies, and cross-phase learning.

## Prerequisites

- Converted ETL unit folder (orchestration `.sql` + optional dbt subfolders)
- Original source definition file (e.g., `.dtsx` for SSIS, `.xml` for Informatica)
- Active Snowflake connection with a warehouse
- DATABASE + SCHEMA with write privileges (`CREATE TABLE`, `CREATE FUNCTION`, `CREATE PROCEDURE`)

### When the converted-output folder is not isolated

The default contract above assumes one folder per unit. If instead you're handed a flat, whole-repository conversion output where a dbt project is referenced by more than one sibling unit's orchestration file (e.g. Informatica `SHORTCUT` mappings reused across workflows), do not edit the shared project in place:

1. Stage a real copy of the orchestration file and every dbt project it references under `{PACKAGE_FOLDER}/Output/ETL/{unit}/`. Treat the original location read-only until sync-back.
2. If a staged dbt project's `packages.yml` has a local `path:` dependency, do **not** edit the path to account for the extra staging depth — that breaks canonical when synced back. Instead, symlink the shared-assets directory into the unit folder at the depth `packages.yml` already expects.
3. Before syncing any fix back, run the leak gate on every touched file, then diff against the original — test-environment values (schema/database names, credentials) must never reach the canonical copy:
   ```bash
   uv run --project {SKILL_DIR} python {SKILL_DIR}/scripts/check_sync_leaks.py {SESSION_JSON} <file1> [<file2> ...]
   ```
   Do not copy until this exits 0.

## Persistent Files

All files stored in `{UNIT}/stabilization/`:

| File | Purpose |
|------|---------|
| `planning/scan.json` | Unit scan output (elements, EWIs, dbt projects) |
| `planning/orchestration-context.md` | Orchestration structural understanding (statements, element relationships, containers) |
| `planning/dbt-context.md` | dbt project analysis (model inventory, health, source mapping, bootstrap blockers). Only present when unit has dbt projects. |
| `planning/source-excerpts.md` | Source-definition excerpts for traceability (conditional — only if source file is large) |
| `planning/ROADMAP.md` | Phase plan (agent-authored from template; updated in-place during execution). Never delete content. |
| `tracking/STATE.md` | Resumption bookmark (GENERATED — use `track_status.py` commands, do not edit directly) |
| `tracking/progress.json` | Element-level tracking (machine-readable) |
| `tracking/fix-log.md` | Append-only record of every fix applied. Absent until Phase 1 completes. |
| `phases/phase-{N}/` | Per-phase artifacts: baselines, batch reports, learnings, infrastructure SQL |
| `report.html` | Self-contained HTML report aggregating all artifacts. Generated during Final Validation by `generate_report.py`. |
> **Progressive disclosure:** Reference files are loaded on-demand — only read a reference file when its content is needed for the current step.

## Agent Wait Protocol

**NEVER use `bash sleep`, `bash_output`, or `cortex agent output` to wait for agents.**

You are the orchestrator. Do **not** spawn a subagent whose job is "run etl-stabilization" or "execute Phase N". Named teammates (context mappers, test-gen, fixer, apply-fixes) are the only valid spawns.

**Claim in-flight work only from this turn's spawn tool results.** If this turn did not return live agent ids, nothing is running. Do not tell the user a subagent is executing.

How to wait, by spawn mode:

- **`run_in_background=false`** (planning mappers, and any blocking spawn): results return in **this** turn. Process them here. Do **not** end the turn to wait.
- **`run_in_background=true`**: spawn all agents in one message (parallel tool calls). Confirm each spawn returned an agent id. **Then** end the turn — no extra tool calls, no "still running" narration. A new turn arrives when each agent finishes. Process that result, then verify output files exist.

Do not attempt to call `agent_output` — it may not be available and failed attempts waste a turn.

**Stall:** If `STATE.md` / phase artifacts have not changed and you have no live agent ids, you are stalled. Resume from `STATE.md` (Execution Workflow) or tell the user it stalled — do not keep claiming work is in progress.

## Entry Point

On every invocation:

0. **Detect the conversion flavor.** Before anything else, determine whether this unit is a **Snowflake Scripting** conversion or a **dbt** conversion:
   - **Scripting** — the code unit's `extensions.conversionMode` is `snowflakeScripting`, or the unit folder holds standalone mapping stored procedures (`CREATE OR REPLACE PROCEDURE`) with no dbt projects (no `dbt_project.yml`).
   - **dbt** — otherwise (dbt sub-projects present).

   Store the flavor in session. **dbt flavor** runs the standard path below unchanged. **Scripting flavor** replaces the data-flow half of stabilization with the mapping-procedure pair (proc-test-gen → proc-fixer) while keeping the orchestration half identical — see [Scripting Flavor Routing](#scripting-flavor-routing). In the guided flow, whether a scripting unit reaches this skill is controlled upstream by the migration state machine; when it does — or on direct invocation — proceed with the scripting path.
1. Check if `{UNIT}/stabilization/tracking/STATE.md` exists
2. **If no STATE.md** → new unit → run **Planning Workflow**
3. **If STATE.md exists** → read it → run **Execution Workflow** for next pending phase. If status is "Ready to execute" (or next-action is Execute Phase N) and Phase N has no cortex task / `start-phase` has not run, that is the post-ROADMAP stall: **start Execution Step 2 in this turn**. Do not wait for a subagent.

---

## Scripting Flavor Routing

For a **Snowflake Scripting** unit (detected in Entry Point Step 0), each converted Informatica mapping is a
standalone stored procedure (a `kind=etl` unit) whose transformation blocks are delimited by boundary markers
(`---- Start block '<FullName>'` / `---- End block …`) and may carry `!!!RESOLVE EWI!!!` stubs. The **data-flow
half** of stabilization operates on these mapping procedures instead of dbt models; the **orchestration half**
(the workflow task graph) is handled by the orchestration pair exactly as in the dbt path.

**Cut and rebuild — only the data-flow half changes. The dbt and orchestration paths are untouched:**

| Step | dbt flavor | Scripting flavor |
|------|-----------|------------------|
| Context mapping (Step 6) | dbt context mapper over dbt projects | mapping-procedure discovery: each converted mapping proc, its source mapping, and its defective blocks |
| Readiness (Step 6b) | dbt project readiness | per mapping proc: defective-block inventory (from block-locate / ewi-extract) |
| ROADMAP phases (Step 7) | `dbt` phases (scope `dbt`) | `dataflow-proc` phases (scope `dataflow-proc`) — one item per mapping procedure |
| Per-phase dispatch (Execution) | dbt-test-gen → dbt-fixer | proc-test-gen → proc-fixer |
| Orchestration half | orchestration pair (unchanged) | orchestration pair (unchanged) |

A `dataflow-proc` phase runs the mapping-procedure pair exactly as a `dbt` phase runs the dbt pair:
[proc-test-gen](proc-test-gen/SKILL.md) derives the source-of-truth assertions for a mapping procedure, then
[proc-fixer](proc-fixer/SKILL.md) reconstructs its defective blocks and grades against those assertions until
the procedure creates clean and passes. Use the `dataflow-proc` phase-type template in the ROADMAP template.

> **Discovery input.** Identifying which procedures are converted mappings and enumerating their defective
> blocks comes from the unit scan plus the boundary markers. Where the scan does not classify a procedure as a
> mapping unit, fall back to the source mapping `.xml` + the boundary markers to identify each mapping procedure
> and its blocks.

---

## Planning Workflow

### Step 0: Create Progress Task

Create the task and register all its steps in **two calls** — `cortex ctx step add` accepts
multiple step texts at once, so do not issue one call per step:

```bash
cortex ctx task add "Planning: {unit_name}"
cortex ctx task start <task_id>
cortex ctx step add -t <task_id> \
  "Step 1: Gather inputs" \
  "Step 2: Scan unit" \
  "Step 3: Initialize tracking" \
  "Step 4: Configure test environment" \
  "Step 5: Backup and strip dead code" \
  "Step 6: Context mapping — spawn parallel blocking agents, process results this turn" \
  "Step 6b: Classify dbt project readiness" \
  "Step 7: Create ROADMAP (7a-7c)" \
  "Step 8: Create STATE.md" \
  "Step 9: Present ROADMAP for approval"
```

**Marking steps done — group them.** `cortex ctx step done` accepts multiple step IDs
(`cortex ctx step done <id> <id> ...`), so mark completed steps in groups rather than one
call per step. Every such call is a separate agent round-trip that does not change any
file, so grouping them is measurably faster with no effect on the work performed.

Flush the pending group (mark everything completed so far as done) at these points, so
externally-persisted progress is never stale when it matters:
- before spawning any agent wave, and before ending a turn to wait for notifications
- at each phase transition, and before any stopping point that asks the user a question

The authoritative resumption state is on disk regardless: the ROADMAP's `[x]` step
checkboxes plus `STATE.md`. Cortex progress is the live display and the auto-compact
re-injection channel, not the source of truth — which is why grouping is safe and why the
task itself must still exist (see the Execution Workflow gate).

Mark the task done after Step 9 approval.

### Step 1: Gather Inputs

Ask the user for:
- Unit folder path (containing orchestration `.sql` and optional dbt subfolders)
- Original source definition file path (e.g., `.dtsx` for SSIS, `.xml` for Informatica)
- Source platform (if not obvious from file extension)

**STOPPING POINT**: Use `ask_user_question` to get the user's answer before proceeding.

### Step 1b: Detect Platform

1. **Auto-detect from file extension**: `.dtsx` → `ssis`, `.xml` → ask user to confirm platform
2. **If ambiguous**, ask the user which platform via `ask_user_question`
3. **Read the platform profile** from `{SKILL_DIR}/platforms/{PLATFORM_ID}/platform-profile.md`
4. **Store the platform** in session — subsequent steps use `{PLATFORM_ID}`, `{PLATFORM_DIR}` (`{SKILL_DIR}/platforms/{PLATFORM_ID}`), and `{SOURCE_FILE_PATH}`

The platform profile defines: source file label, traceability comment format, guide file paths, dead code stripping script, element classification rules, and platform-specific vocabulary.

### Step 2: Scan Unit

```bash
uv run --project {SKILL_DIR} python {SKILL_DIR}/scripts/scan_unit.py {UNIT_FOLDER} {SOURCE_FILE} --platform {PLATFORM_ID}
```

Output: `{UNIT}/stabilization/planning/scan.json`

If scan_unit.py fails, check: (1) unit folder contains a `.sql` orchestration file, (2) source file path is correct, (3) `uv` is installed. See Troubleshooting below.

### Step 3: Initialize Tracking

```bash
uv run --project {SKILL_DIR} python {SKILL_DIR}/scripts/track_status.py init {SCAN_JSON}
```

Output: `{UNIT}/stabilization/tracking/progress.json` — all elements start `pending`.

### Step 4: Configure Test Environment

Check `session_status.json` for existing `test_environment`. If not found, ask the user via `ask_user_question` with two options:
1. **"Use current connection's database"** — run `SELECT CURRENT_DATABASE()` to get it
2. The user can type a different database name via "Something else"

The question text:
```
Which database should be used for test schemas? You need CREATE SCHEMA, CREATE TABLE, CREATE FUNCTION, and CREATE PROCEDURE privileges. Each phase creates per-batch schemas automatically and drops them when done.
```

After getting the database name:
```bash
uv run --project {SKILL_DIR} python {SKILL_DIR}/scripts/track_status.py set-test-env {SESSION_JSON} {DATABASE} PUBLIC
```

### Step 5: Backup and Strip Dead Code

Snapshot the unit directory before stripping:

```bash
uv run --project {SKILL_DIR} python {SKILL_DIR}/scripts/backup_unit.py {UNIT}
```

This creates `{UNIT}/stabilization/original/` with a copy of the unit excluding the `stabilization/` sub-tree.

If the platform profile defines a `strip_script` (not null), run dead code stripping:
```bash
uv run --project {SKILL_DIR} python {PLATFORM_DIR}/{STRIP_SCRIPT} {ORCHESTRATION_SQL_FILE}
```

### Step 6: Context Mapping (parallel agents)

Use `team_create` tool: team_name="etl-plan-{unit_name}".

**Orchestration context mapper** (always):
Spawn a teammate with `name="context-mapper"`, `run_in_background=false`, and the prompt template at `{SKILL_DIR}/reference/agent-prompts/context-mapper.md` (substitute `{ORCH_SQL_PATH}`, `{SOURCE_FILE_PATH}`, `{UNIT}`, `{SKILL_DIR}`, `{PLATFORM_DIR}`, `{ORCHESTRATION_GUIDE}` placeholders).

Output: `orchestration-context.md` — element inventory, duplicate groups, behavioral patterns, container hierarchy.

**dbt context mapper** (conditional — dbt flavor only, when dbt_projects exist):
Spawn a teammate with `name="dbt-context-mapper"`, `run_in_background=false`, and the prompt template at `{SKILL_DIR}/reference/agent-prompts/dbt-context-mapper.md` (substitute `{UNIT}`, `{SOURCE_FILE_PATH}`, `{SKILL_DIR}`, `{TRANSFORMATION_GUIDE}` placeholders).

Output: `dbt-context.md` — project health, model inventory, macro inventory, source mapping, bootstrap blockers.

**Scripting flavor:** skip the dbt context mapper. Instead, discover the mapping procedures per
[Scripting Flavor Routing](#scripting-flavor-routing) — for each converted mapping proc, record its source
mapping and its defective blocks (block-locate / ewi-extract). The orchestration context mapper still runs for
the workflow task graph.

**Spawn both agents in a single message** (parallel tool calls) with `run_in_background=false`. Process both tool results in this turn. Verify both output files exist and are non-empty before continuing. Do not end the turn to wait — blocking spawns are not background jobs.

Use `team_delete` tool after verifying outputs.

### Step 6b: Classify dbt Project Readiness (if dbt projects exist)

If `scan.json` contains dbt_projects:

1. **Read the health signals** from `scan.json` — for each dbt project, check `has_valid_config`, `has_placeholder_config`, `ewi_count`, `ewi_codes`, `health_issues`
2. **Read dbt-context.md** — the dbt-context-mapper has analyzed model structure, macros, source definitions, and bootstrap blockers
3. **Classify each project's readiness:**
   - **Ready**: `has_valid_config=true`, zero or low EWI count → standard dbt phase
   - **Needs bootstrap**: `has_valid_config=false` or `has_placeholder_config=true` → dbt phase with bootstrap sub-phase (config + macro fixes before model testing)
   - **Heavy EWI**: high EWI count relative to model count → dbt phase with expected baseline failures, longer fix cycle
   - **Reused (pre-existing) project**: if the dbt project directory predates this unit — more than one sibling unit's orchestration file references it, or `dbt-context.md` shows it wasn't newly generated for this unit — cross-check every var default the models actually read (`sources.yml`, `dbt_project.yml` vars) against *this* unit's own source-XML identity (folder/repository/workflow name), even when `has_valid_config=true`. A previously-stabilized shared project is not a smoke-check target; wrong-but-valid-looking defaults are a silent data-correctness defect, not a compile error.

These classifications inform the ROADMAP phase design in Step 7. Do NOT mark projects as `needs-user` at planning time — that decision is made by the dbt-test-gen agent after attempting test generation.

### Step 7: Create ROADMAP

Using orchestration-context.md, dbt-context.md (if dbt projects exist), and scan.json, design the phase plan. The ROADMAP is **agent-authored** — write it directly using the Write tool from the template at `{SKILL_DIR}/reference/templates/ROADMAP_TEMPLATE.md`.

**orchestration-context.md is CRUCIAL** for orchestration phases — it contains structural understanding (statement inventory, container hierarchy, element relationships, shared variables, event handler patterns). **dbt-context.md is CRUCIAL** for dbt phases — it contains model inventory, health signals, source mapping, and bootstrap blocker analysis. Use both as primary inputs.

**Phase design principles:**
- Phases align with CREATE TASK/PROCEDURE boundaries
- Phase types: `full-tdd`, `lightweight`, `dbt`, `dataflow-proc`, `final-validation` (`dataflow-proc` is the scripting-flavor data-flow phase; see [Scripting Flavor Routing](#scripting-flavor-routing))
- **Item sizing caps** (an "item" is one orchestration element or one dbt project — caps apply to both):
  - **Small-medium item**: a dbt project with ≤20 models (from `scan.json` `health.model_count`); OR any orchestration element (elements are atomic — 1 element = 1 item against the phase cap, regardless of internal complexity)
  - **Large item**: a dbt project with >20 models. **Only dbt projects can be classified as large** — orchestration elements are always small-medium
  - **Phase cap**: pack up to **40-50 small-medium items per phase** OR up to **20 large items per phase**
  - **Do NOT mix classes in the same phase** — route small-medium and large items into separate phases so sizing stays predictable
    *(This mixing rule governs phases approaching the item cap — for a phase with only a handful of items, keep them together even if one crosses a size threshold; splitting a 3-item phase into two is needless fragmentation.)*
  - **Batch cap**: ~10 small-medium items per batch, ~5 large items per batch
  - **Concurrency cap**: max 5 parallel batches per phase regardless of item size
- Push each phase toward its cap rather than creating many small phases — a 48-project small-medium phase is preferable to two 24-project phases when the items share patterns
- Never split `grouped:{name}` element sets across batches
- Archetype elements get `full-tdd`; clones get `lightweight` phases applying the archetype's patterns
- Orchestration phases are sequential (edit the same SQL file); batches within a phase are parallel
- dbt phases on different projects may run in parallel
- dbt phases receive the SAME rigor as orchestration phases: health assessment, explicit batch assignments, completion criteria
- dbt projects with `has_placeholder_config=true` or `has_valid_config=false` need a bootstrap sub-step (the dbt-test-gen agent handles this internally — document the blocker in the ROADMAP phase metadata)
- Every dbt project MUST be assigned to a dbt phase — no project may be omitted or deferred to "manual" resolution
- **Scripting flavor:** every mapping procedure MUST be assigned to a `dataflow-proc` phase — one mapping proc is one small-medium item (atomic, like an orchestration element). Do NOT create dbt phases for a scripting unit
- The ROADMAP must include dbt project health summaries in the phase metadata (from scan.json health fields and dbt-context.md)

**Phase sizing factors** (refine assignment within the caps above — not a substitute for the caps):
1. Post-strip orchestration file size
2. EWI density and type complexity per statement
3. Statement topology (don't break loops, containers, event handler groups)
4. Element count per statement
5. dbt project boundaries
6. Cross-element dependencies (shared variables, shared tables)

**Always include a Final Validation phase** as the last phase.

**Step 7a: Write ROADMAP.md** — Read template at `{SKILL_DIR}/reference/templates/ROADMAP_TEMPLATE.md`, fill all sections, write to `{UNIT}/stabilization/planning/ROADMAP.md`.

**Step 7b: Register phases in session_status.json:**
```bash
uv run --project {SKILL_DIR} python {SKILL_DIR}/scripts/track_status.py init-roadmap {SESSION_JSON} --phases-json '[{"phase":1,"name":"...","goal":"...","scope":"orchestration","parallel_safe":false,"depends_on":[]}, ...]'
```

**Step 7c: Assign elements to phases (single batch call):**

Write a JSON file with all phase→element→strategy mappings, then call `batch-assign-phases` once:
```bash
# Write assignments to a temp file, then:
uv run --project {SKILL_DIR} python {SKILL_DIR}/scripts/track_status.py batch-assign-phases {SESSION_JSON} --assignments-file {ASSIGNMENTS_FILE}
```

The JSON file format:
```json
[
  {"phase": 1, "elements": ["Package\\El_A", "Package\\El_B"], "strategy": "isolated"},
  {"phase": 2, "elements": ["Package\\El_C"], "strategy": "grouped:core"}
]
```

> **Do NOT call `assign-phases` multiple times in parallel.** Use `batch-assign-phases` to assign all phases atomically in one invocation.

**Step 7d: Generate _infrastructure.sql per phase** — For each phase:
1. Determine the superset of infrastructure tags needed across all batches
2. Write `{UNIT}/stabilization/phases/phase-{N}/_infrastructure.sql`
   - Core: control_variables table, GetControlVariableUDF, UpdateControlVariable
   - Tagged conditionals: CLEAR_VARIABLES, INIT_FROM_CONFIG, BUILD_DBT_VARS (only if phase needs them)
   - Use `{SCHEMA}` placeholder (orchestrator does string replacement at execution time)
   - See `orchestration-test-gen/infrastructure-dedup.md` for full DDL

### Step 8: Create STATE.md

```bash
uv run --project {SKILL_DIR} python {SKILL_DIR}/scripts/track_status.py update-state {SESSION_JSON} --current-phase 1 --phase-status "Ready to execute" --next-action "Execute Phase 1 ({phase_name})"
```

### Step 9: Present ROADMAP for Approval

Display the ROADMAP to the user. Highlight:
- Number of phases and batches per phase
- Phase types and procedure alignment
- Test strategies (grouped vs isolated, and why)

**STOPPING POINT**: Use `ask_user_question` to get the user's approval or revision requests.

### Step 10: Begin Execution

After user approval, **in the same turn** (before any wait, and without spawning an orchestrator subagent):

1. Run Execution Workflow **Step 2** (create/verify the Phase 1 cortex task).
2. Run `track_status.py start-phase` as Step {1}.1 requires.
3. Continue Execution Step 3 for Phase 1.

`STATE.md` saying "Ready to execute" is not evidence that work is running. If you stop after Step 8/9 without Step 2, the session is stalled at 0%.

---

## Cortex Task Invariant

A cortex task MUST exist for the current phase at all times during execution.
This is the auto-compact resilience mechanism — cortex ctx data is persisted
externally and re-injected via system-reminders every turn.

- **Created by:** Execution Workflow Step 2 (for the first phase or after restart)
  or the previous phase's Phase Transition step (for subsequent phases)
- **Verified by:** `cortex ctx show tasks` — must show a task matching "Phase {P}:"
- **Never skip:** If no task exists, create it before any phase work begins

---

## Execution Workflow

Phase execution is continuous and autonomous. Do NOT stop between phases
to ask the user. The only approved stopping points are in the Planning
Workflow (Steps 1, 4, 9) and when an error requires user input.

### Step 1: Read State
Read `{UNIT}/stabilization/tracking/STATE.md`
→ identify current phase number and status.

### Step 2: Ensure Cortex Task Exists (MANDATORY GATE)

Run `cortex ctx show tasks` via bash.

**Branch A — Task already exists:** A task matching "Phase {P}:" is found
with unchecked steps. Continue from its first unchecked step at Step 3.
Each step description says "(see ROADMAP.md § Phase {P})" — read those
instructions from disk before executing.

**Branch B — No task exists (MANDATORY creation before ANY phase work):**

1. Read `ROADMAP.md` § Phase {P} → extract phase name, type, and step list
2. Create the cortex task and steps — execute these bash commands directly
   (substitute actual values for all placeholders). `cortex ctx step add` takes
   multiple step texts, so register every step in ONE call, not one call per step:
   ```bash
   cortex ctx task add "Phase {P}: {PHASE_NAME}"
   cortex ctx task start <task_id>
   # One call, one text per ROADMAP execution step (Steps {P}.1 through {P}.{LAST}):
   cortex ctx step add -t <task_id> \
     "Step {P}.1: {step_description} (see ROADMAP.md § Phase {P})" \
     "Step {P}.2: {step_description} (see ROADMAP.md § Phase {P})" \
     "... one text per remaining ROADMAP step"
   ```
3. **Verify creation:** Run `cortex ctx show tasks` again — confirm a task
   matching "Phase {P}:" exists. If not, STOP and repeat this step.
4. Mark Step {P}.0 as `[x]` in the ROADMAP
5. If some later steps are already `[x]` in the ROADMAP (session restart),
   mark those cortex steps done — in a single grouped call
   (`cortex ctx step done <id> <id> ...`). Also check disk artifacts for
   the current phase: if step outputs exist (e.g., `baseline_batch_*.md`
   for test-gen, `batch_*.md` for fix wave) but the ROADMAP checkbox was
   not marked, include those steps in the same grouped call.

**GATE CHECK:** Do NOT proceed to Step 3 until `cortex ctx show tasks`
confirms a task for "Phase {P}:" exists with at least one unchecked step.

### Step 3: Execute Steps
For each pending cortex step:
1. Read the step's instructions from ROADMAP.md
2. Execute them
3. Mark `[x]` next to the step in the ROADMAP — this is the authoritative
   resumption record and is always written per step
4. Accumulate the cortex step ID as pending-done; do NOT issue a separate
   `cortex ctx step done` call per step
5. **Multi-unit / package runs — track per unit as you go, never batch to the end.** After each unit or phase completes, mark the ROADMAP `[x]` (item 3) immediately, flush the pending cortex step-done group (item 4 — a unit or phase boundary is a mandatory flush point, see below), AND run `track_status.py update <element> --status <fixed|test-passed|...>` for the element plus `track_status.py update-state --current-phase <N> ...`. Also confirm the unit's `proc-test-gen` seed + assertion files were written under `{UNIT}/stabilization/tests/proc/<unit>/`. Deferring ROADMAP ticks or state updates to the end leaves `STATE.md` and the generated `report.html` under-reporting progress mid-run (element count and percent both stale).

**Flush pending cortex step-done calls in one grouped call**
(`cortex ctx step done <id> <id> ...`) at these points:
- **after each unit or phase completes** (item 5 above — never carry pending
  step-dones across a unit boundary)
- before spawning an agent wave, and before ending a turn to await notifications
- at the Phase Transition step, and before any stopping point that asks the user

Rationale: each `cortex ctx step done` call is a separate agent round-trip that
writes no file and cannot change the outcome of the work. Grouping them is
measurably faster and leaves the on-disk record unchanged — ROADMAP checkboxes,
`track_status.py` element/state updates and `STATE.md` are all still written per
step and per unit as item 5 requires, so `report.html` progress never goes stale.
Flushing at unit boundaries, before waves, turn ends and stopping points keeps the
externally-persisted cortex progress current whenever auto-compact or a session
restart could intervene.

The last step of each phase (except Final Validation) is a **Phase Transition**
that creates the next phase's cortex task inline (see ROADMAP step instructions)
and continues execution. This creates a continuous chain — cortex tasks for
Phase {NEXT_P} are created before Phase {P}'s task completes, so the agent
always has a pending task.

### Error Recovery
- **Catastrophic file corruption**: Restore from `checkpoints/phase_{N}/` or `original/`.
- **Snowflake connection failure**: Verify connection. Re-run `track_status.py set-test-env` if credentials changed.
- **ROADMAP amendment needed**: Log via `track_status.py add-decision`, amend future phases only, document reasoning.
- **Stalled after ROADMAP / fake subagent progress**: `STATE.md` still "Ready to execute", no new artifacts, agent claiming a subagent is running. Nothing is running. Resume at Execution Step 2 in this turn. Tell the user it stalled if you cannot start.

---

## Batch Output Format

See [reference/templates/batch-artifacts.md](reference/templates/batch-artifacts.md).

## Sub-Skills

- **[orchestration-test-gen](orchestration-test-gen/SKILL.md)** — Generate AAA tests for orchestration elements (isolated or grouped per ROADMAP)
- **[orchestration-fixer](orchestration-fixer/SKILL.md)** — Fix orchestration elements using test-file workbench
- **[dbt-test-gen](dbt-test-gen/SKILL.md)** — Generate dbt tests (seeds, schema tests, singular assertions)
- **[dbt-fixer](dbt-fixer/SKILL.md)** — Fix dbt models via iterative compile-fix loop
- **[proc-test-gen](proc-test-gen/SKILL.md)** — Generate source-derived AAA tests for a scripting-flavor mapping procedure (data-flow); target-only, grade-hardened
- **[proc-fixer](proc-fixer/SKILL.md)** — Repair a scripting-flavor mapping procedure by reconstructing each defective block from its source transformation, then deploy+CALL and grade until it passes

## Reference Files

See [reference/index.md](reference/index.md) for the full index of all reference files.

Sub-skill guides:
- **[orchestration-test-gen/assertion-patterns.md](orchestration-test-gen/assertion-patterns.md)** — SQL assertion templates
- **[orchestration-test-gen/stored-procedure-wrapping.md](orchestration-test-gen/stored-procedure-wrapping.md)** — SP template and Snowflake quirks
- **[orchestration-test-gen/test-categorization.md](orchestration-test-gen/test-categorization.md)** — Isolated vs grouped test strategy
- **[proc-test-gen/proc-assertion-patterns.md](proc-test-gen/proc-assertion-patterns.md)** — Target-only batched assertion shape + grade-hardening rules (scripting mapping procs)
- **[proc-fixer/block-reconstruction-patterns.md](proc-fixer/block-reconstruction-patterns.md)** — Per-transform source→block reconstruction recipes + minimal-change rules (scripting mapping procs)

Platform-specific guides (loaded from `{PLATFORM_DIR}/`, filenames defined in the platform profile):
- **`{PLATFORM_DIR}/{orchestration_guide}`** — Source file navigation for orchestration structure
- **`{PLATFORM_DIR}/{transformation_guide}`** — Source file navigation for transformation logic
- **`{PLATFORM_DIR}/element-types.md`** — Element type to Snowflake mapping
- **`{PLATFORM_DIR}/ewi/`** — Platform-specific EWI/FDM fix guides

## Examples

See [reference/examples.md](reference/examples.md).

## Troubleshooting

See [reference/troubleshooting.md](reference/troubleshooting.md).

`scan_unit.py` fails, or the unit folder doesn't match Prerequisites → check whether the input is a flat, multi-unit conversion output rather than an isolated per-unit folder; see "When the converted-output folder is not isolated" above.

## Output

- Fixed orchestration `.sql` file with EWI gaps resolved
- Fixed dbt model files (per sub-project)
- Test artifacts in `{UNIT}/stabilization/tests/`
- `{UNIT}/stabilization/report.html` — self-contained HTML report aggregating all artifacts (generated during Final Validation)
- `artifacts/tracking/fix_log.md` — append-only record of every fix applied. Each entry carries per-instance anchors (file + stable symbol/tag anchor into the fixed tree and the `stabilization/original/` backup) plus a `Classification` — `engine-defect | conversion-improvement | intentional-decline | context-dependent`. **An `!!!RESOLVE EWI!!!` breaking wrapper (or any correctly emitted supported EWI/FDM) is `intentional-decline`, resolved manually — never log it as `engine-defect`.** See [reference/templates/fix-log-format.md](reference/templates/fix-log-format.md) and [reference/templates/batch-artifacts.md](reference/templates/batch-artifacts.md).
- `artifacts/phases/phase_{N}/` — per-phase baselines, batch reports, learnings
