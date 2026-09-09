---
name: proc-fixer
parent_skill: etl-stabilization
description: "Repair the defective blocks of ONE converted Informatica-to-Snowflake-Scripting mapping procedure by reconstructing each block's SQL from the source transformation node, block-scoped and minimal-change, then deploy+CALL and grade against the source-derived assertions until the procedure creates clean and passes. Use when the stabilization skill invokes fixing for a scripting-flavor mapping procedure."
license: Proprietary. See License-Skills for complete terms
---

# Proc Fixer (scripting flavor)

Repair a single converted **mapping procedure** — an Informatica mapping converted to a standalone Snowflake
Scripting stored procedure — that still contains unsupported-transform stubs (`!!!RESOLVE EWI!!!`). Each
materialized transformation is a **block** delimited by boundary markers; the fixer reconstructs each defective
block's SQL **from the source transformation node it was converted from**, splices it back, then deploys, CALLs,
and grades the procedure against the source-derived assertions until it creates clean and all assertions pass.

The fix is authored from **source semantics**, not guessed from the broken SQL, and the expected result the fix
is graded against is computed by the test generator from the source — so the loop has an independent target.

> **Scope.** This is the data-flow counterpart to [orchestration-fixer](../orchestration-fixer/SKILL.md)
> (which repairs control-flow elements of a task graph) and the scripting-flavor analog of
> [dbt-fixer](../dbt-fixer/SKILL.md) (which repairs dbt models). In dbt mode a mapping becomes a model repaired
> by dbt-fixer; in scripting mode a mapping becomes its own stored procedure repaired here. It consumes the
> assertions authored by [proc-test-gen](../proc-test-gen/SKILL.md) — that pair owns the ARRANGE + ASSERT; this
> skill owns the ACT (the fix) and drives the repair loop.

> **Autonomous mode:** When spawned as a team agent, skip all interactive stopping points, make reasonable
> defaults, and document assumptions in the completion report. When done, `send_message` to `main` with your
> results, and respond to any `shutdown_request` with `type: "shutdown_response"`, `approve: true`.

## Where this sits in the fix loop

```
block-locate  ── the defective block + its span/body (scripts/stabilization_tools.py block-locate, marker-scoped)
ewi-extract   ── the block's !!!RESOLVE EWI!!! / SSC-* defects (scripts/stabilization_tools.py ewi-extract)
proc-fixer    ── [THIS SKILL] reconstruct the fixed block SQL from the source transformation node
block-replace ── splice the fix back between the markers, integrity-checked (scripts/stabilization_tools.py block-replace)
deploy-and-call ─ deploy the one proc into the test schema + CALL it (scai code deploy-and-call)
grade         ── run the source-derived assertions against the populated target; PASS/FAIL feeds this loop
```

proc-fixer owns the **ACT**: for each defective block it authors a minimal, source-faithful replacement,
splices it in, and drives the deploy → CALL → grade cycle. The seed (ARRANGE) and the assertions (ASSERT) come
from proc-test-gen and are treated as fixed inputs the fix must satisfy — never edited to make a fix pass.

## AAA framing

- **Arrange** — the input seed and the target table shape are already created and seeded by proc-test-gen
  (`<proc_name>.seed.sql`). Re-run the seed before each grade to reset to the known state.
- **Act** — deploy the current procedure into the test schema and `CALL` it, so its output lands in
  `<test_schema>.<TARGET>`. This is what the fix changes.
- **Assert** — run proc-test-gen's batched target-only assertions (`<proc_name>.assert.sql`); any non-`PASS`
  (or a query that errors) means not-yet-converged.

### Input

- `session_status.json` — with `source_file_path`, the mapping proc unit, and `migration_object_path`
- The converted proc `.sql` file (a mapping unit's converted output, with boundary markers + `!!!RESOLVE EWI!!!`
  stubs) — this is the file the fixer edits in place, via block-replace
- The source mapping definition (Informatica `.xml`) at `source_file_path`
- The proc-test-gen artifacts under `<UNIT>/stabilization/tests/proc/<proc_name>/`:
  `<proc_name>.seed.sql`, `<proc_name>.assert.sql`, `test_report.md` (the baseline result + which assertions
  failed) — **required.** If they are absent, tests have not been generated yet: STOP and return to the parent
  skill to run proc-test-gen first.

### Prerequisites

- Python 3.11+; the deterministic tool layer present (`scripts/stabilization_tools.py` — the block-locate /
  ewi-extract / block-replace / task-error-locate subcommands — and `scripts/scan_unit.py`)
- The headless executor available: `scai code deploy-and-call` (deploy one proc + CALL, returns a
  `ProcCallResult` JSON) — see Tooling
- An active Snowflake connection with a warehouse, and CREATE PROCEDURE on the user-provided (test) database +
  schema that proc-test-gen used
- A backup: ensure `<UNIT>/stabilization/original/` holds the pre-fix procedure. The parent skill creates it
  during setup; create it if missing before the first edit.

### Output Location

- The **repaired converted `.sql`** — edited in place via block-replace (boundary markers preserved).
- `<UNIT>/stabilization/tracking/fix_log.md` (Main Mode) — one record per fix attempt, successes and failures.
  Task Mode writes fix records to its learnings artifact instead; the orchestrator merges them.

## Tooling (headless, no IDE / no `snowflake_sql_execute`)

Like proc-test-gen, this loop is headless — the mechanical steps are deterministic scripts and the deploy/grade
steps shell to the executor / `snow sql`, never the interactive `snowflake_sql_execute` MCP tool.

| Step | Command |
|------|---------|
| locate a block + its span/body | `uv run --project {SKILL_DIR} python {SKILL_DIR}/scripts/stabilization_tools.py block-locate <proc.sql> --block '<FullName>' --json` |
| list a block's EWIs (grouped by block) | `uv run --project {SKILL_DIR} python {SKILL_DIR}/scripts/stabilization_tools.py ewi-extract <proc.sql> --grouped --json` |
| resolve an EWI's fix guide | `uv run --project {SKILL_DIR} python {SKILL_DIR}/scripts/stabilization_tools.py ewi-guide-resolve <SSC-...> --platform <p>` |
| splice a reconstructed block back | `uv run --project {SKILL_DIR} python {SKILL_DIR}/scripts/stabilization_tools.py block-replace <proc.sql> --block '<FullName>' --replacement-file <fix.sql>` |
| map a CALL error to its block | `uv run --project {SKILL_DIR} python {SKILL_DIR}/scripts/stabilization_tools.py task-error-locate <proc.sql> --error-file <errfile>` |
| deploy the proc + CALL it | `scai code deploy-and-call -c <conn> -d <db> --schema <test_schema> --proc-file <proc.sql> --call "CALL <proc>(...)"` → JSON `{deployed, called, errorText, rows}` |
| seed / run the grade query | run `<proc_name>.seed.sql`, then `<proc_name>.assert.sql`, via `snow sql -c <conn> --database <db> --schema <test_schema> --format json` |

block-replace integrity-checks the marker pair and refuses to write if the reconstruction would drop or add a
marker; treat a non-zero exit as a failed splice, not a fixed block.

## Reconstruction rules

The core of the fix is reconstructing a block from the source transformation node. These rules are
non-negotiable; the per-transform recipes are in
[block-reconstruction-patterns.md](block-reconstruction-patterns.md).

**Author from source, not from the broken SQL.**
- Reconstruct only from the source mapping semantics + the block's role. Do NOT invent behavior and do NOT
  hardcode result rows or mock constants (`0`, `NULL`, a literal expected value) to make a grade pass — that is
  never a valid fix.
- Read the source transformation node behind the block. The broken stub embeds the source `<TRANSFORMATION>` /
  `<CONNECTOR>` XML as comments; use it, and the source `.xml`, to recover ports, expressions, join/lookup
  conditions, and group-by keys. See `{PLATFORM_DIR}/{transformation_guide}` (Informatica: `mapping-guide.md`)
  and `{PLATFORM_DIR}/element-types.md`.

**Preserve the block's role and output shape.**
- Same INSERT target and column list; same final SELECT column set and order; same block boundary markers.
- Minimal change — keep the surrounding statement, sensible CTE/temp-table names, and any code not related to
  the defect. Do NOT reformat or rename beyond what the fix requires.

**Faithful Informatica semantics** (recipes + worked examples in the patterns file):
- **Lookup** (connected) → `LEFT OUTER JOIN` to the lookup table; no-match → NULL outputs; no fan-out when the
  lookup key is unique; honor the multiple-match policy only when the key can duplicate.
- **Filter** → `WHERE <condition>`; a NULL predicate is not TRUE, so that row is **dropped** — do NOT rewrite
  `x != 'Y'` as `x != 'Y' OR x IS NULL`.
- **Aggregator** → `GROUP BY` the GROUPBY port(s) with the stated aggregates (`SUM`/`COUNT`/`AVG`/`MIN`/`MAX`).
- **Joiner** → the stated join type (Normal = inner; Master/Detail/Full Outer keep the named side).
- **Router** → one output per group condition (`WHERE`), unmatched rows to the default group.
- **Rank** → window function with `QUALIFY`, partitioned by the group ports.
- **Union** → `UNION ALL` (no dedup unless stated).
- **Expression** → apply the port expressions in dependency order; translate `IIF`→`IFF`, `DECODE`→`CASE`.
- **Update Strategy** → the DD_INSERT/UPDATE/DELETE/REJECT operations against the target.
- **Preserve transformation ORDER** — e.g. lookup, then filter (which may test a looked-up column), then
  aggregate. Reordering changes the result.

**EWI markers.** Remove `!!!RESOLVE EWI!!!` marker lines when applying the fix (they break compilation). Keep
`--** SSC-EWI-*` / `--** SSC-FDM-*` one-line comment markers — they are documentation. Replace the entire stub
body (marker line + the commented-out source XML below it) with working SQL; do not leave dead commented code.

## Workflow

```
Proc Fixer Progress:
- [ ] Step 1: Analyze & plan — read proc-test-gen report + block-locate the defective blocks; order them
- [ ] Step 2: Reconstruct → splice each defective block (block-scoped, source-derived, minimal change)
- [ ] Step 3: Deploy + CALL (smoke); on error, locate the block and re-reconstruct
- [ ] Step 4: Grade against the assertions; on FAIL, identify the block and re-reconstruct (bounded, then escalate)
- [ ] Step 5: Report (fix log, return to parent skill)
```

### Step 1: Analyze & plan

1. Read `test_report.md` for the baseline: did the proc deploy/CALL, which assertions failed, and the
   source→block mapping proc-test-gen recorded. Read `session_status.json` and the test environment.
2. `stabilization_tools.py block-locate --json` over the converted `.sql` to enumerate blocks; `stabilization_tools.py ewi-extract` to find which
   blocks carry `!!!RESOLVE EWI!!!` / structural defects. Those are the work items.
3. Order the defective blocks by data-flow dependency (a block that feeds another is fixed first), so a
   downstream block is reconstructed against a fixed upstream one.
4. Interactive mode: present the plan (defective blocks, their source transforms, baseline failures) and
   confirm (⚠️ STOPPING POINT). Autonomous: proceed and document.

### Step 2: Reconstruct and splice each defective block

For each defective block, in dependency order:

1. `stabilization_tools.py block-locate` to read the current block body; read the source transformation node behind it (from the
   embedded XML + the source `.xml`).
2. Reconstruct the block SQL per the Reconstruction rules + the patterns file — minimal change, source-faithful,
   same output shape, no hardcoded rows.
3. Write the reconstruction to a temp file and splice with `stabilization_tools.py block-replace`. A non-zero exit (marker integrity
   violation) means the reconstruction is malformed — fix it, do not force the write.
4. `stabilization_tools.py ewi-extract` on the block to confirm no `!!!RESOLVE EWI!!!` remains in it.

### Step 3: Deploy + CALL (smoke loop)

1. Re-run `<proc_name>.seed.sql` to reset the input + target state.
2. `scai code deploy-and-call … --proc-file <proc.sql> --call "CALL <proc>(...)"`. Read the `ProcCallResult`:
   - `deployed=false` → the proc failed to CREATE (a syntax/structural error). Read `errorText`.
   - `called=false` → it errored at CALL. Read `errorText`.
3. On a deploy/CALL error, map it back to the offending block with `stabilization_tools.py task-error-locate --error-file <errfile>`,
   and return to Step 2 for that block, feeding the error text into the reconstruction. This is the inner
   (compile/smoke) loop; iterate until the proc creates clean and CALLs without error.

### Step 4: Grade (outer loop)

1. Run `<proc_name>.assert.sql` and read the PASS/FAIL rows.
2. **All PASS** → the procedure is stabilized. Go to Step 5.
3. **Any FAIL** → identify which block is responsible from the failing assertion (e.g. a wrong total points at
   the aggregator or the filter; a spurious/missing row points at the lookup/filter order) and return to Step 2
   for that block, feeding the failing assertions in as grader feedback.
4. **Bounded retry:** at most **5** proc-level grade attempts. If still failing, revert the proc to
   `<UNIT>/stabilization/original/`, record the failure with the last error/assertion summary, and escalate —
   do NOT leave a partially-fixed proc or weaken the assertions to force a pass.
5. **If the assert query itself ERRORS** (not FAIL) — that is a test-generation bug, not a proc bug. Do NOT
   edit the proc for it; return to the parent skill to have proc-test-gen simplify the assertion.

### Step 5: Report

Append a fix record to `<UNIT>/stabilization/tracking/fix_log.md` (Main Mode) or the learnings artifact
(Task Mode):

```markdown
## Fix Record
- **Unit**: <unit_name>
- **Procedure**: <proc_name>
- **Block(s) fixed**: <FullName>, …
- **Source transform(s)**: <e.g. LKP_Customer (Lookup), FIL_NotStandard (Filter), AGG_ByRegion (Aggregator)>
- **Fix summary**: <what each block was reconstructed to — e.g. "LEFT JOIN → WHERE tier!='STANDARD' → GROUP BY region">
- **Deploy/CALL**: deployed=<bool> called=<bool>
- **Grade**: N of M assertions PASS
- **Attempts**: <k of 5>
- **Outcome**: SUCCESS | FAILED | ESCALATED
```

Then return to the parent skill.

> **Do NOT call `track_status.py` directly.** Record statuses in your task artifact; the orchestrator updates
> `session_status.json` after fix agents complete.

## Reference Files (loaded on-demand)

| File | When to load |
|------|-------------|
| [block-reconstruction-patterns.md](block-reconstruction-patterns.md) | Step 2 — per-transform source→block reconstruction recipes + the minimal-change / semantic-preservation rules |
| [../proc-test-gen/proc-assertion-patterns.md](../proc-test-gen/proc-assertion-patterns.md) | Step 4 — to read a failing assertion's intent (the assertion shape proc-test-gen emits) |
| `{PLATFORM_DIR}/{transformation_guide}` (Informatica: `mapping-guide.md`) | Step 2 — reading the source transformation node (ports, expressions, join/lookup conditions) |
| `{PLATFORM_DIR}/element-types.md` | Step 2 — what each transform type does (active/passive, row-count, cache/aggregator modes) |
| `{PLATFORM_DIR}/ewi/<CODE>.md` | when a block carries a specific EWI marker (resolve via `stabilization_tools.py ewi-guide-resolve`) |

---

## Task Mode (spawned by orchestrator)

### Input (provided at spawn time)
- Unit name + converted proc `.sql` path (edited in place via block-replace)
- Source mapping `.xml` path (READ-ONLY)
- The proc-test-gen artifacts (seed / assert / test_report) for this proc
- The defective block FullName(s) to repair
- Test schema (`TEST_SCHEMA`), database (`DATABASE`), connection (`CONNECTION`)
- Skill directory (`SKILL_DIR`); platform directory (`PLATFORM_DIR`)
- Run all SQL headless via `scai code deploy-and-call` + `snow sql --format json` — no `snowflake_sql_execute`

### Autonomous behavior
- No user questions — reasonable defaults, documented in the report.
- On ambiguity (unclear transform semantics, missing source element): make a best-effort source-faithful
  reconstruction and document the assumption. If a transform is genuinely non-reconstructable from source
  (dynamic SQL, external mapplet), revert the block, record it as a coverage gap, and escalate — do NOT
  fabricate a fix or hardcode the expected rows.
- Respect the bounded retry (5 proc-level grade attempts). Prefer reverting + escalating over an unbounded loop.
- Write the fix record incrementally after each proc completes.

### Team protocol
When complete, results return to the orchestrator automatically. Respond to a `shutdown_request` with
`send_message` `type: "shutdown_response"`, `approve: true`.
