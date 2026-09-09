## Examples

### Example 1: New package (first run)

User says: "Fix this ETL package at /data/packages/SalesLoad"

Actions:
1. No STATE.md found → run Planning Workflow
2. Scan package, initialize tracking, gather test env (user provides DATABASE with CREATE SCHEMA privileges)
3. Use the `task` tool to spawn `name="context-mapper"` with `run_in_background=false` (no team during planning) → process the tool result in this turn → verify `orchestration-context.md` and `dbt-context.md`
4. Author ROADMAP.md from template (Write tool) with 3 phases (2 orchestration + 1 final validation), each with task definitions (task table, element-to-task assignments, schema names)
5. Register phases in `artifacts/tracking/session_status.json` via `init-roadmap --phases-json`, assign elements via `assign-phases`
6. Present ROADMAP for approval → user approves
7. **Same turn:** Execution Step 2 (cortex task) + `start-phase` + Phase 1 Setup. Do not spawn an orchestrator subagent and wait.
   - Create schemas: `ETL_FIX_P1_B1`, `ETL_FIX_P1_B2`, `ETL_FIX_P1_B3` (batches B1.1, B1.2, B1.3)
   - Use `team_create` tool: team_name="etl-fix-SalesLoad-p1"
   - Use `task` tool to spawn 3 test-gen agents in single message: `orchestration-test-gen-B1.1`, `orchestration-test-gen-B1.2`, `orchestration-test-gen-B1.3`
   - Wait for all 3 task notifications (no sleep, no narration)
   - Validate baseline reports → use `task` tool to spawn 3 fix agents: `orchestration-fixer-B1.1`, `orchestration-fixer-B1.2`, `orchestration-fixer-B1.3`
   - Wait for all 3 task notifications
   - Validate each batch artifact → update `artifacts/tracking/session_status.json` + `artifacts/tracking/STATE.md` → spawn `apply-fixes` agent → post-apply validation → merge learnings
   - Shutdown team → drop schemas → checkpoint

Result: Phase 1 complete, proceed to Phase 2.

### Example 2: Resume after interruption

User says: "Resume ETL fixing" (after session was interrupted mid-execution)

Actions:
1. STATE.md found → read current position (Phase 2, ready to execute)
2. Execute Phase 2:
   - Create schemas: `ETL_FIX_P2_B1`, `ETL_FIX_P2_B2` (batches B2.1, B2.2)
   - Use `team_create` tool: team_name="etl-fix-SalesLoad-p2"
   - Use `task` tool to spawn 2 batch agents → wait for task notifications → process artifacts → apply fixes → merge learnings
   - Shutdown team → drop schemas → checkpoint

Result: Phase 2 complete, progress updated.

### Example 3: Parallel dbt phases

User says: "Run next phase" (ROADMAP has Phase 3 and Phase 4 as dbt phases, both `parallel_safe: true`, `depends_on: [1, 2]`, Phases 1-2 complete)

Actions:
1. STATE.md shows Phase 3 ready, Phase 4 also unblocked
2. Use `team_create` tool: team_name="etl-fix-SalesLoad-p3p4"
3. Use `task` tool to spawn dbt-test-gen agents for both **in a single message** (parallel):
   - name="dbt-test-gen-projectA", team_name="etl-fix-SalesLoad-p3p4", run_in_background=false
   - name="dbt-test-gen-projectB", team_name="etl-fix-SalesLoad-p3p4", run_in_background=false
4. Wait for all task notifications (no sleep) → verify test artifacts
5. Use `task` tool to spawn dbt-fixer agents for both **in a single message** (parallel):
   - name="dbt-fixer-projectA", team_name="etl-fix-SalesLoad-p3p4", run_in_background=false
   - name="dbt-fixer-projectB", team_name="etl-fix-SalesLoad-p3p4", run_in_background=false
6. Wait for all task notifications (no sleep) → validate → checkpoint both
7. Shutdown team → proceed to Final Validation phase

Result: Two dbt phases completed concurrently, saving time.

### Example 4: Phase retry after failure

User says: "Run next phase" (after a prior session failed mid-phase)

Actions:
1. STATE.md shows Phase 2 in-progress, batch artifacts show 2 of 3 batches completed
2. Resume Phase 2 — create schemas, create team, spawn only the failed batch agent (batches with existing artifacts are skipped)
3. Process remaining batch artifact → batch-update → apply fixes → merge learnings
4. Shutdown team → drop schemas → checkpoint

Result: Phase 2 completed, blockers cleared.

### Example 5: Context-exhaustion recovery with single-element isolation

User says: "Run next phase" (Phase 3 has Task 2 with 4 elements assigned)

Scenario: `orchestration-test-gen-B3.2` processes 2 of 4 elements but runs out of context mid-work. It wrote artifacts for the first 2 elements before dying, but the last 2 are absent from `batch_B3.2.md`.

Actions:
1. Task notification arrives for `orchestration-test-gen-B3.2` with `failed` status
2. Orchestrator reads `artifacts/phases/phase_3/batch_B3.2.md` — finds `element_A` (test-passed) and `element_B` (auto-fixed-needs-review); `element_C` and `element_D` are absent
3. Remaining count = 2 → use `task` tool to spawn continuation agent: name="orchestration-test-gen-B3.2-r1", team_name="etl-fix-PackageName-p3", run_in_background=false, with `{ELEMENT_LIST}` = `element_C, element_D` only (not the full original 4-element list)
4. `orchestration-test-gen-B3.2-r1` processes `element_C` (test-passed) but also runs out of context before `element_D`
5. Orchestrator reads updated artifact — `element_D` still absent; remaining count = 1 → use `task` tool to spawn dedicated single-element agent: name="orchestration-test-gen-B3.2-r2", with `{ELEMENT_LIST}` = `element_D` only — the full context budget goes to one hard element
6. `orchestration-test-gen-B3.2-r2` completes successfully — `element_D` test-passed (complex ScriptTask requiring 4 fix-test iterations)
7. All 4 elements now have terminal statuses → proceed to apply-fixes

Result: All elements resolved across 3 agent lifetimes. No work repeated. The 2-retry cap was not reached.
