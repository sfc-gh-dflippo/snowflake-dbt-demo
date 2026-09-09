# Phase Execution Protocol

## Phase Type Routing

When the orchestrator begins a phase, read the ROADMAP phase metadata to determine the type, then follow the corresponding protocol below.

| Type | Protocol | When Used |
|------|----------|-----------|
| full-tdd | [Full TDD Phase](#full-tdd-phase) | CREATE TASK/PROCEDURE needing test generation and fixing from scratch |
| lightweight | [Lightweight Phase](#lightweight-phase) | Duplicate/similar procedure — apply known fix patterns |
| dbt | [dbt Phase](#dbt-phase) | dbt project test/fix cycle |
| final-validation | [Final Validation Phase](#final-validation-phase) | Last phase — artifact review and sanity check |

> **Auto-compact resilience:** Auto-compact (context summarization) may occur at any time during execution. Resilience is achieved via **cortex task chaining**: every phase (except Final Validation) ends with a Phase Transition step that reads the ROADMAP for the next phase and directly creates the next phase's cortex task (via `cortex ctx task add` + `cortex ctx step add`). The Execution Workflow (SKILL.md § Step 2) also enforces task creation as a mandatory gate on every invocation. Since cortex ctx data is persisted externally and re-injected via system-reminders every turn, the execution chain survives compaction. Additionally, each phase type starts with a **Preamble** that re-reads canonical state from disk for session-restart recovery. Wave checkpoints between agent waves verify artifacts and tracking persisted.

---

## Full TDD Phase

**Progress tracking:** Cortex task creation is enforced by the Execution Workflow (SKILL.md § Step 2) and by each phase's Phase Transition step. The ROADMAP template defines the step list per phase type. Mark steps done in grouped calls (`cortex ctx step done <id> <id> ...`), flushed before each agent wave, before ending a turn, and at the Phase Transition — not one call per step (see SKILL.md § Step 3). Mark the task done after step k (Phase Transition). Final-validation phases end at step j instead.

### Preamble: Re-verify state from disk

Auto-compact may have occurred since the last action. Re-read canonical state before proceeding.

**Round 1** (single read):
- Read `artifacts/tracking/STATE.md` — extract current phase number and next action. If this phase is already marked complete, skip to the next pending phase.

**Round 2** (parallel tool calls):
- Read `ROADMAP.md` `## Phase {N}` section — extract phase type, tasks, elements, strategies
- Read `artifacts/tracking/session_status.json` — check element statuses for this phase's elements
- `ls artifacts/phases/phase_{N}/` — check what artifacts already exist from a prior partial run

> **Batch ID format:** `B{P}.{M}` (e.g., `B1.1` = Phase 1 Batch 1). The `{B}` placeholder throughout this document represents the full phase-qualified batch ID.

**Resume logic:**
- If `STATE.md` says "Ready to execute" and this phase has no `start-phase` / no artifacts yet → you are stalled after ROADMAP approval. Run SKILL.md Execution Step 2 in this turn. Do not wait for a subagent.
- If `baseline_batch_*.md` files already exist for all tasks → skip step b (test-gen already ran), proceed to step c
- If `batch_*.md` files already exist for all tasks → skip steps b-e (fixes already ran), proceed to step f
- If `apply_report.md` exists → skip steps b-f, proceed to step g
- If element statuses are stuck in non-terminal states that conflict with existing artifacts, log a warning and re-derive statuses from the artifacts on disk

### a. Setup
1. Mark phase as started: `track_status.py start-phase {SESSION_JSON} {N}`
2. Read ROADMAP phase definition — extract tasks, schemas, elements, strategies
3. Create task schemas: `CREATE SCHEMA IF NOT EXISTS {DATABASE}.{TASK_SCHEMA}` for each task via `snowflake_sql_execute`
4. Deploy infrastructure: read `artifacts/phases/phase_{N}/_infrastructure.sql`, replace `{SCHEMA}` with each task schema, execute via `snowflake_sql_execute`

### b. Spawn test-gen agents (MANDATORY — non-negotiable for full-tdd phases)
For EACH task, MUST spawn a test-gen agent. This is unconditional — no exceptions based on proven patterns, clean SQL, or prior phase success.

For each task, spawn a test-gen agent with:
- Phase number, task ID, schema name
- Element names, test strategy, archetype/clone status
- File paths: orch SQL, source file, platform directory, artifact directory
- Instruction: read `{SKILL_DIR}/orchestration-test-gen/SKILL.md` Task Mode section

Max 5 agents per wave. If >5 tasks, spawn the first 5 in one message, wait for that batch to complete, then spawn the remaining tasks.

### c. Wait for test-gen completion
For each completed agent:
- VERIFY `artifacts/phases/phase_{N}/baseline_batch_{B}.md` exists for EVERY task
- If any baseline is missing, the protocol was violated — do not proceed. Respawn the missing agent.
- Parse baseline summary table: count passed/failed/skipped per element
- **Update tracking from baselines:** For each element in the baseline summary, call `track_status.py update` with `--status orch-tested`. Include `--reason "baseline: N of M assertions failed"` when failures exist. Run these calls **sequentially** (one per bash invocation).

### c.1 Wave checkpoint: verify test-gen artifacts persisted
Before spawning fix agents, verify the test-gen wave's outputs actually reached disk:
1. Glob `artifacts/phases/phase_{N}/baseline_batch_*.md` — confirm one file per batch
2. Re-read `artifacts/tracking/session_status.json` — confirm all phase elements have status `orch-tested` (or `no-fix-needed`/`skipped`)
3. If any baseline is missing or any element is still `pending`: trigger partial-artifact recovery sub-protocol before proceeding

### d. Spawn fix agents
For each task where baseline has >=1 failing element:
- Spawn fix agent with same context as test-gen plus:
  - Pointer to `artifacts/phases/phase_{N}/baseline_batch_{B}.md` (enriched baseline)
  - Instruction: read `{SKILL_DIR}/orchestration-fixer/SKILL.md` Task Mode section

For tasks where ALL elements passed or were skipped: no fix agent needed. Orchestrator writes a minimal `artifacts/phases/phase_{N}/batch_{B}.md` with no-fix-needed statuses and an empty `artifacts/phases/phase_{N}/learnings_batch_{B}.md`.

### e. Wait for fix completion
For each completed fix agent:
- Verify `artifacts/phases/phase_{N}/batch_{B}.md` exists
- Verify `artifacts/phases/phase_{N}/learnings_batch_{B}.md` exists
- **Update tracking from fix artifacts:** For each element section in `batch_{B}.md`, parse the `Status` and `Reason` fields. Call `track_status.py update` with the parsed status and reason. Run these calls **sequentially** (one per bash invocation).

If validation fails for any agent: apply the **partial-artifact recovery sub-protocol** for fix agents (see below).

### e.1 Wave checkpoint: verify fix artifacts persisted
Before spawning the apply-fixes agent, verify the fix wave's outputs actually reached disk:
1. Glob `artifacts/phases/phase_{N}/batch_*.md` — confirm one file per batch that had a fix agent
2. Glob `artifacts/phases/phase_{N}/learnings_batch_*.md` — confirm one file per batch
3. Re-read `artifacts/tracking/session_status.json` — confirm all fixed elements have terminal status (`test-passed`, `auto-fixed-needs-review`, `skipped`, etc.)
4. If any artifact is missing or any element status is still `orch-tested` after fix agents completed: trigger partial-artifact recovery sub-protocol before proceeding

### f. Apply fixes (MANDATORY — after ALL fix agents complete)
**Prerequisite:** ALL fix agents from step d must have completed and been processed in step e before this step begins.

Spawn single apply-fixes agent:
- Input: all `artifacts/phases/phase_{N}/batch_*.md` files
- Instruction: read `{SKILL_DIR}/reference/agent-prompts/apply-fixes.md`
- Agent reads task artifacts, extracts Replacement SQL, applies to orch SQL by tag matching

### g. Post-apply validation (lightweight — no test re-runs)
Orchestrator performs directly (no agent):
1. Count `!!!RESOLVE EWI!!!` markers in orch SQL — should have decreased for fixed elements
2. Verify tag integrity: all `---- Start block` tags have matching `---- End block` tags; all `---- Start` (non-block) tags are present and followed by another tag before the procedure ends
3. Count all tags (`---- Start block`, `---- Start`, `---- End block`) and verify counts match pre-replacement values
4. If issues found: log warning, do NOT re-run tests (TDD already verified fixes)

### h. Merge learnings
1. Read all `artifacts/phases/phase_{N}/learnings_batch_*.md`
2. For each learning entry: extract EWI code and pattern name
3. Append new patterns to the body of `artifacts/tracking/fix_log.md` (do not duplicate existing patterns — add only new variants)
4. Rebuild the EWI code index at the top of fix_log.md per the format in `reference/templates/fix-log-format.md`

### i. Update tracking
- Verify `artifacts/tracking/session_status.json` has correct element statuses (already updated in steps c and e)
- Call `track_status.py complete-phase` and `track_status.py update-state`
- Update `artifacts/tracking/STATE.md` with phase completion
- Mark phase as `[x] Complete` in ROADMAP

> **Concurrency rule:** ALL `track_status.py` calls in this protocol are made by the orchestrator, never by agents. Run them **sequentially** — one per bash invocation, never batched in the same message.

### j. Checkpoint (optional)
Create `checkpoints/phase_{N}/` with copies of orch SQL and session_status.json for recovery.

### k. Phase Transition
Read the ROADMAP's next phase section (`## Phase {NEXT_N}`). Create the cortex task for the next phase directly: `cortex ctx task add "Phase {NEXT_N}: {NEXT_PHASE_NAME}"`, `cortex ctx task start <task_id>`, then add every ROADMAP step in ONE `cortex ctx step add -t <task_id> "step 1" "step 2" ...` call (it accepts multiple step texts). Verify with `cortex ctx show tasks` that the task exists. Mark Step {NEXT_N}.0 as `[x]` in the ROADMAP. Mark this cortex step done (which completes the current phase's cortex task). Continue with Step {NEXT_N}.1.

Final-validation phases do NOT have this step — they end at step j.

---

## Lightweight Phase

A lightweight phase applies known fix patterns from a prior phase. Test generation is SKIPPED — the patterns are already proven.

**Progress tracking:** Cortex task creation is enforced by the Execution Workflow (SKILL.md § Step 2) and by each phase's Phase Transition step. The ROADMAP template defines the step list per phase type. Mark steps done in grouped calls (`cortex ctx step done <id> <id> ...`), flushed before each agent wave, before ending a turn, and at the Phase Transition — not one call per step (see SKILL.md § Step 3). Mark the task done after step k (Phase Transition).

### Preamble: Re-verify state from disk

Same as Full TDD preamble:

**Round 1**: Read `artifacts/tracking/STATE.md` — if phase already complete, skip to next pending phase.

**Round 2** (parallel): Read `ROADMAP.md` phase section, read `session_status.json`, `ls artifacts/phases/phase_{N}/`.

**Resume logic:**
- If `batch_*.md` files already exist for all tasks → skip step b (fixes already ran), proceed to step c
- If `apply_report.md` exists → skip steps b-f, proceed to step g

### a. Setup
Same as Full TDD: create schemas, deploy infrastructure.

### b. Spawn fix agents (apply known patterns)
For each task, spawn fix agent with:
- Same context as Full TDD fix agents
- Additionally: `pattern_source: Phase {SOURCE_PHASE} fix_log` (tells agent to consult fix_log for proven patterns)
- Instruction: read `{SKILL_DIR}/orchestration-fixer/SKILL.md` Task Mode section

Fix agents read `artifacts/tracking/fix_log.md`, find matching EWI patterns from the source phase, and apply them. Each fix agent creates test files in its own task schema (same SEED/ACT/ASSERT structure as full-tdd) and runs them to verify the pattern applies correctly to the clone elements. Fix agents write Replacement SQL to their task artifacts — they do NOT edit the orchestration SQL directly.

### c-k. Same as Full TDD
Steps c through k follow the same protocol as Full TDD (wait for fix, apply fixes, post-apply validation, merge learnings, update tracking, checkpoint, phase transition).

> **Note:** Lightweight fix agents produce their own test files per-element (using the proven pattern as a template). The apply-fixes agent (step f) applies Replacement SQL from task artifacts — same as full-tdd.
> **Wave checkpoints:** The Full TDD wave checkpoints (c.1 and e.1) apply to lightweight phases through the "Same as Full TDD" reference above.

---

## dbt Phase

**Progress tracking:** Cortex task creation is enforced by the Execution Workflow (SKILL.md § Step 2) and by each phase's Phase Transition step. The ROADMAP template defines the step list per phase type. Mark steps done in grouped calls (`cortex ctx step done <id> <id> ...`), flushed before each agent wave, before ending a turn, and at the Phase Transition — not one call per step (see SKILL.md § Step 3). Mark the task done after step h (Phase Transition).

### Preamble: Re-verify state from disk

**Round 1**: Read `artifacts/tracking/STATE.md` — if phase already complete, skip to next pending phase.

**Round 2** (parallel): Read `ROADMAP.md` phase section, read `session_status.json`, `ls artifacts/phases/phase_{N}/`.

**Resume logic:**
- If `test_report.md` exists for all projects → skip step b (dbt-test-gen already ran), proceed to step c
- If `dbt_learnings_*.md` exists for all projects → skip steps b-e (dbt-fix already ran), proceed to step f

### a. Setup
No schema creation needed — dbt projects use their own target schemas.

Register nodes for each project (sequentially):
```bash
uv run --project {SKILL_DIR} python {SKILL_DIR}/scripts/track_status.py init-dbt {SESSION_JSON} {PROJECT_NAME} {DBT_PROJECT_PATH}
```

### b. Spawn dbt-test-gen agents (UNCONDITIONAL — one per project, always)

**This step is non-negotiable.** One agent per dbt project, ALWAYS, regardless of:
- Known EWI codes or data-source blockers
- Placeholder config values (YOUR_PROJECT_NAME)
- Broken macros or missing source definitions
- Any other perceived reason to skip

Test generation IS the assessment mechanism. The dbt-test-gen agent handles broken projects internally:
1. Generates test file scaffolding (seeds + test SQL) from source definition analysis — this does NOT require dbt compile
2. Attempts execution (dbt seed → dbt run → dbt test) — if this fails, documents WHY in test_report.md
3. Returns baseline artifacts with documented blockers

**Early exit WITHOUT test artifacts is a protocol violation.**

For each dbt project, spawn an agent with:
- Project path, database, target schema
- Source definition file path
- Platform transformation guide path
- ROADMAP.md path, session_status.json path
- Instruction: read `{SKILL_DIR}/dbt-test-gen/SKILL.md` Task Mode section

Max 5 agents per wave.

### c. Wait for dbt-test-gen completion — VALIDATE ARTIFACTS

For EACH project, verify ALL of these exist:
- `{UNIT}/stabilization/tests/dbt/{PROJECT_NAME}/seeds/` — at least 1 .csv file
- `{UNIT}/stabilization/tests/dbt/{PROJECT_NAME}/tests/` — at least 1 .sql file
- `{UNIT}/stabilization/tests/dbt/{PROJECT_NAME}/test_report.md`

**If ANY artifact is missing for ANY project**: respawn the agent for that project. Cap at 2 retries. After 2 retries with missing artifacts, mark the project's nodes as `failed` with reason `test-gen-exhaustion` and proceed to dbt-fix for remaining projects that have valid artifacts.

Parse each project's `test_report.md` Baseline Results table. Update tracking:
- `track_status.py update-dbt --status dbt-tested` per project
- `track_status.py update-dbt-node` per node with test-passed/test-failed
Run sequentially.

### c.1 Wave checkpoint: verify dbt-test-gen artifacts persisted
Before spawning dbt-fix agents, verify test-gen outputs reached disk:
1. For each project: glob `stabilization/tests/dbt/{PROJECT_NAME}/seeds/*.csv`, `stabilization/tests/dbt/{PROJECT_NAME}/tests/*.sql`, and check `stabilization/tests/dbt/{PROJECT_NAME}/test_report.md` exists
2. Re-read `artifacts/tracking/session_status.json` — confirm all dbt projects have status `dbt-tested`
3. If any artifact is missing after retries: mark project nodes as `failed` per the retry boundary rule above

### d. Spawn dbt-fix agents

One agent per project with:
- Failing tests (test-failed nodes), OR
- Compilation errors (documented in test_report.md), OR
- Bootstrap issues (placeholder config, broken macros — documented in test_report.md)

Each agent receives:
- Same context as dbt-test-gen plus baseline test results path
- Instruction: read `{SKILL_DIR}/dbt-fixer/SKILL.md` Task Mode section

Projects where ALL nodes passed and NO compilation errors exist: no fix agent needed. Orchestrator writes a minimal `artifacts/phases/phase_{N}/dbt_learnings_{project_name}.md` with no-fix-needed.

### e. Wait for dbt-fix completion

For each completed fix agent:
- Verify `artifacts/phases/phase_{N}/dbt_learnings_{project_name}.md` exists
- Parse per-node outcomes (fixed/failed with reason)
- Update tracking: `track_status.py update-dbt-node` per node, `track_status.py update-dbt` per project
Run sequentially.

### e.0 Semantic gate: re-run the source-derived tests after fixing

The fix wave is not complete because the models compile. `dbt compile` renders Jinja only; it cannot tell
a correct fix from one that compiles and returns wrong data. The gate is the source-derived tests that
`dbt-test-gen` produced from the source definition **before** any fix existed.

For each project the fix wave touched, with a warehouse available:

1. Drop/recreate the affected relations (or build with `--full-refresh`) so a failed build cannot leave a
   previous attempt's rows in place — stale relations make the tests pass against old data and report a
   fix that did not happen.
2. `dbt build --select tag:stabilization_test` then `dbt test --select tag:stabilization_test`.
3. **Any FAILING assertion means the node is not fixed.** Send it back to a fix agent with the failing
   assertion text (bounded by the fixer's per-node attempt cap). Never resolve a failure by weakening,
   narrowing or deleting the assertion — the assertion is the specification derived from the source.
4. **A test that ERRORS is a defective test, not a failed fix.** Regenerate/simplify it (see
   `dbt-test-gen/SKILL.md` § Step 3.2a) and re-run; do not charge the node an attempt for it.

If no warehouse is available this gate cannot run: record every affected node with status
`unverified` (plus a reason) via `track_status.py update-dbt-node`, and say so in the phase report. Do not report such nodes as fixed.

### e.1 Wave checkpoint: verify dbt-fix artifacts persisted
Before merging learnings, verify fix outputs reached disk:
1. Glob `artifacts/phases/phase_{N}/dbt_learnings_*.md` — confirm one file per project that had a fix agent
2. Re-read `artifacts/tracking/session_status.json` — confirm all dbt nodes have terminal status
3. If any learning file is missing: log warning and proceed (learning merge is best-effort)

### f. Merge dbt learnings
Read per-project learning files at `artifacts/phases/phase_{N}/dbt_learnings_*.md` and append to `artifacts/tracking/fix_log.md`.

### g. Update tracking
- Verify `artifacts/tracking/session_status.json` has correct dbt project and node statuses
- Call `track_status.py complete-phase` and `track_status.py update-state`
- Update `artifacts/tracking/STATE.md` with phase completion
- Mark phase as `[x] Complete` in ROADMAP

> **Concurrency rule:** ALL `track_status.py` calls are orchestrator-only, run sequentially.

### h. Phase Transition
Read the ROADMAP's next phase section (`## Phase {NEXT_N}`). Create the cortex task for the next phase directly: `cortex ctx task add "Phase {NEXT_N}: {NEXT_PHASE_NAME}"`, `cortex ctx task start <task_id>`, then add every ROADMAP step in ONE `cortex ctx step add -t <task_id> "step 1" "step 2" ...` call (it accepts multiple step texts). Verify with `cortex ctx show tasks` that the task exists. Mark Step {NEXT_N}.0 as `[x]` in the ROADMAP. Mark this cortex step done (which completes the current phase's cortex task). Continue with Step {NEXT_N}.1.

Final-validation phases do NOT have this step — they end at step g.

---

## Final Validation Phase

**Progress tracking:** Cortex task creation is enforced by the Execution Workflow (SKILL.md § Step 2). The ROADMAP template defines the step list. Mark steps done in grouped calls (`cortex ctx step done <id> <id> ...`), flushed before each agent wave, before ending a turn, and at the Phase Transition — not one call per step (see SKILL.md § Step 3). Mark the task done after step 5.

### Preamble: Re-verify state from disk

**Round 1**: Read `artifacts/tracking/STATE.md` — if final validation already complete, report completion.

**Round 2** (parallel): Read `ROADMAP.md` final phase section, read `session_status.json`.

No resume logic needed — final validation is idempotent (re-running checks is safe).

No schema creation. No infrastructure deployment. No test execution. No agent spawning. Orchestrator performs artifact review directly.

### Validation Checks

1. **Element status check:** Read `artifacts/tracking/session_status.json` — verify ALL elements across all phases have terminal status (test-passed, fixed, no-fix-needed, skipped, needs-user, auto-fixed-needs-review, failed). Zero elements with `pending` or `orch-tested` status. For dbt projects: every project must have a terminal status.
2. **EWI marker check:** Count remaining `!!!RESOLVE EWI!!!` markers in orch SQL — compare against expected count (skipped + needs-user elements)
3. **Fix log consistency:** Read `artifacts/tracking/fix_log.md` — verify no contradicting patterns across phases
4. **Artifact completeness:** Verify each phase has: baseline + batch + learnings artifacts for all tasks
5. **Generate HTML report:**

```bash
uv run --project {SKILL_DIR} python {SKILL_DIR}/scripts/generate_report.py {UNIT_FOLDER}
```

Output: `{UNIT}/stabilization/report.html`

The report aggregates data from `scan.json`, `session_status.json`, `ROADMAP.md`, `orchestration-context.md`, `dbt-context.md`, `fix_log.md`, and `STATE.md` into a single HTML file with executive summary, phase-by-phase status, per-element details, dbt project status, fix log, and full artifact contents.

### Completion
Mark final validation as `[x] Complete` in ROADMAP. Update `artifacts/tracking/STATE.md`: `status: complete`.

---

## Partial-Artifact Recovery Sub-Protocol

**test-gen partial failure**: When a `orchestration-test-gen-{B}` agent returns failed status or its baseline report is missing or incomplete:
1. Parse the baseline report (if any) to identify elements that already have a terminal status entry
2. Determine remaining unprocessed elements: assigned to this task in ROADMAP but absent from the baseline report
3. Spawn a continuation agent `orchestration-test-gen-{B}-r{R}` (R starts at 1) with **only the remaining elements** in the element list, same schema, same prompt
4. Cap at **2 retry spawns per batch** (R = 1 and R = 2 max). After 2 retries, mark remaining elements `failed` with reason `"context-exhaustion-after-retries"` and proceed

**fix partial failure**: When a `orchestration-fixer-{B}` agent returns failed status or its task artifact is missing or incomplete:
1. Parse `artifacts/phases/phase_{N}/batch_{B}.md` (if any) for elements that already have a terminal status
2. Determine remaining unprocessed elements
3. Spawn a continuation agent `orchestration-fixer-{B}-r{R}` (R starts at 1) with **only the remaining elements**, providing the baseline report path and existing test files. Same schema, same prompt
4. Cap at **2 retry spawns per batch**. After 2 retries, mark remaining elements `failed` with reason `"context-exhaustion-after-retries"` and proceed

**Simple retry rule**: After spawning retry agents, wait for task notifications. NEVER use `bash sleep` or `bash_output`. If a retry agent fails, spawn the next retry immediately — no narration between retries.

---

## Validation Gate (MANDATORY)

After executing a phase, run the validation gate before marking it complete. Do NOT proceed to complete-phase until this passes:

```bash
uv run --project {SKILL_DIR} python {SKILL_DIR}/scripts/track_status.py validate-phase {SESSION_JSON} {PHASE_NUM} --list-test-files
```

This checks: EWI marker count, file line count, element status breakdown (zero pending/failed), and lists test SQL files for regression detection.

If validation fails (exit code 1), review failing elements before proceeding.
