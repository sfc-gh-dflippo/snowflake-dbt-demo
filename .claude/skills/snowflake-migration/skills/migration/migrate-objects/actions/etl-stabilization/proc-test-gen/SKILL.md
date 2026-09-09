---
name: proc-test-gen
parent_skill: etl-stabilization
description: "Derive source-of-truth functional-equivalence assertions for ONE converted Informatica-to-Snowflake-Scripting mapping procedure (data-flow), independent of the converted SQL. Seeds input, deploys+CALLs the proc in an isolated test schema, and grades its target table against expected contents computed from the source mapping. Use when the stabilization skill invokes test generation for a scripting-flavor mapping proc."
license: Proprietary. See License-Skills for complete terms
---

# Proc Test Generator (scripting flavor)

Generate and run a functional-equivalence check for a single converted **mapping procedure** — an
Informatica mapping converted to a standalone Snowflake Scripting stored procedure — from the original
data-flow logic in the source mapping. The expected target-table contents are computed **from the source
mapping applied to the seeded input**, NOT from the converted SQL under repair, so the assertions are an
independent oracle. All generated artifacts are stored in `<UNIT>/stabilization/tests/proc/<proc_name>/`.

> **Scope.** This is the data-flow counterpart to [orchestration-test-gen](../orchestration-test-gen/SKILL.md):
> orchestration-test-gen tests control-flow *elements* of a task graph; proc-test-gen tests the *output table*
> of one mapping proc. It is the scripting-flavor analog of dbt-test-gen. In dbt mode a mapping becomes a
> model (tested by dbt-test-gen); in scripting mode a mapping becomes its own `kind=etl` stored procedure,
> tested here.

> **Autonomous mode:** When spawned as a team agent, skip all interactive stopping points, make reasonable
> defaults, and document assumptions in the completion report. When done, `send_message` to `main` with your
> results, and respond to any `shutdown_request` with `type: "shutdown_response"`, `approve: true`.

## Where this sits in the fix loop

```
block-locate  ── the defective block + its source transform node (scripts/stabilization_tools.py block-locate, marker-scoped)
proc-fixer    ── [agentic] author the fixed block SQL from the source node (sibling sub-skill)
block-replace ── splice the fix back, marker-integrity checked (scripts/stabilization_tools.py block-replace)
deploy-and-call ─ deploy the one proc into the test schema + smoke-CALL it (scai code deploy-and-call)
proc-test-gen ── [THIS SKILL] derive the source-of-truth expected target contents + batched assertions
grade         ── run the assertions against the populated target; PASS/FAIL feeds the fixer loop
```

proc-test-gen owns the **ARRANGE (input seed)** and **ASSERT (expected target)** — the stable, source-derived
parts. The **ACT** (deploy + CALL the proc) is performed via `deploy-and-call`; the proc body itself is the
baseline snapshot the fixer iterates on.

## AAA for a single mapping proc

- **Arrange:Setup** — create the test schema + the source/input tables the mapping reads (schema inferred
  from the source mapping's Source/Source-Qualifier definitions), and the target table shape. Run once.
- **Arrange:Seed** — `TRUNCATE` + `INSERT` synthetic input rows into the source tables. Run before every
  ACT/grade cycle to reset to a known state. The **seed is the fixed input** the expected output is computed
  from — it must not change once assertions are derived.
- **Act** — deploy the (current) converted proc into the test schema and `CALL` it, so its output lands in
  `<test_schema>.<TARGET>`. Done with `scai code deploy-and-call` (see Tooling); on the baseline run the proc
  may fail to CREATE or error at CALL — that is expected and recorded.
- **Assert** — a single batched query over **only the target table** that verifies its contents equal what the
  source mapping produces for the seeded input (see [proc-assertion-patterns.md](proc-assertion-patterns.md)).

### Input

- `session_status.json` — with `source_file_path`, the pending mapping proc unit, and `migration_object_path`
- The converted proc `.sql` file (a `kind=etl` unit's `files.converted.path`)
- The source mapping definition (Informatica `.xml`) at `source_file_path`
- The block FullName(s) under repair (from the block boundary markers / scan.json)

### Prerequisites

- Python 3.11+; the deterministic tool layer present (`scripts/stabilization_tools.py` — the block-locate /
  ewi-extract subcommands — and `scripts/scan_unit.py`)
- The headless executor available: `scai code deploy-and-call` (deploy one proc + CALL, returns a
  `ProcCallResult` JSON) — see Tooling
- An active Snowflake connection with a warehouse, and **CREATE TABLE / CREATE PROCEDURE** on a user-provided
  (test) database + schema

### Output Location

```
<UNIT>/stabilization/tests/proc/<proc_name>/
  <proc_name>.assert.sql     # the batched target-only assertion query (source-derived)
  <proc_name>.seed.sql       # ARRANGE:SETUP + ARRANGE:SEED (input tables + synthetic rows)
  test_report.md             # baseline result, consumed by proc-fixer
```

The value of this skill is the **seed** (the fixed input) and the **assert** (expected target contents from
source semantics). The proc body is the baseline; proc-fixer iterates it until the assert passes.

## Tooling (headless, no IDE / no `snowflake_sql_execute`)

Unlike orchestration-test-gen (which runs SQL via the CoCo `snowflake_sql_execute` MCP tool), the scripting
loop is **headless**:

| Step | Command |
|------|---------|
| locate the block + its span/body | `uv run --project {SKILL_DIR} python {SKILL_DIR}/scripts/stabilization_tools.py block-locate <proc.sql> --block '<FullName>' --json` |
| extract EWIs in the block | `uv run --project {SKILL_DIR} python {SKILL_DIR}/scripts/stabilization_tools.py ewi-extract <proc.sql> --code <SSC-...> --json` |
| deploy the proc + CALL it | `scai code deploy-and-call -c <conn> -d <db> --schema <test_schema> --proc-file <proc.sql> --call "CALL <proc>(...)"` → JSON `{deployed, called, errorText, rows}` |
| seed input / run the grade query | run `<proc_name>.seed.sql`, then the assert query, against `<db>.<test_schema>` |

> **Grade-query execution.** The batched assert query is run against the populated target and its PASS/FAIL
> rows read back with `snow sql -c <conn> --database <db> --schema <test_schema> --format json -q "<assert>"`
> — the same headless path the deploy-and-call executor itself shells to, so this step needs no extra plumbing.

## Workflow

```
Proc Test Gen Progress:
- [ ] Phase 1: Configure test env + read source mapping + block-locate the proc
- [ ] Phase 2: Design the input seed (ARRANGE) from the source mapping's sources
- [ ] Phase 3: Compute expected target contents from source semantics + write the batched assert
- [ ] Phase 4: Seed + deploy-and-CALL (baseline) + grade; record result
- [ ] Phase 5: Report (test_report.md)
```

### Phase 1: Configure + read source

1. **Test environment** — reuse `session_status.json`'s `test_environment` if present; else detect the current
   connection (`SELECT CURRENT_DATABASE(), CURRENT_SCHEMA(), CURRENT_WAREHOUSE()`) and store it via
   `track_status.py set-test-env`. Interactive mode: confirm with the user (⚠️ STOPPING POINT). Autonomous: use
   the current connection and proceed.
2. **Read the source mapping ONCE** — from `source_file_path`, extract for this mapping: the Source /
   Source-Qualifier definitions (input table shapes + columns), the transform chain (Filter / Aggregator /
   Lookup / Joiner / Expression / Rank / Union / Router / Update-Strategy …), and the Target definition
   (output table + column mapping). See `{PLATFORM_DIR}/{transformation_guide}` (Informatica: `mapping-guide.md`)
   for element names/paths/expressions and `{PLATFORM_DIR}/element-types.md` for what each transform type does.
3. **block-locate the proc** — run `stabilization_tools.py block-locate --json` to get the materialized block(s) and their source
   node(s). Build a mental map of source transform → block; do not re-read per assertion.

### Phase 2: Design the input seed (ARRANGE)

From the source mapping's Source/Source-Qualifier definitions, create the input tables and seed synthetic rows.
Design the seed to exercise the transform semantics that must be verified:

- at least one row that flows through to the target, and one that is dropped/filtered;
- for a Lookup: an input whose key matches and one whose key does NOT (no-match → NULL);
- for an Aggregator: enough rows per group to make the aggregate non-trivial (≥2 groups, ≥2 rows/group);
- NULL combinations for columns used in NULL-sensitive expressions;
- for Router/Update-Strategy: rows exercising ≥2 branches / ≥2 ops.

Write `ARRANGE:SETUP` (CREATE OR REPLACE input + target tables in the test schema) and `ARRANGE:SEED`
(`TRUNCATE` + `INSERT ... SELECT` the synthetic rows) to `<proc_name>.seed.sql`. The seed is now **frozen** —
the expected target is computed from exactly these rows.

### Phase 3: Compute expected target + write the batched assert

Apply the **source mapping semantics** to the seeded input **by hand** to compute the expected target contents —
do NOT read the converted SQL. Faithful Informatica semantics:

- **Lookup**: no-match → NULL for the looked-up columns.
- **Filter**: drops rows whose predicate is not TRUE (a NULL predicate drops the row).
- **Aggregator**: `GROUP BY` the group-by ports + the stated aggregates (SUM/AVG/COUNT/MIN/MAX); ungrouped
  aggregate = whole input.
- **Joiner**: the stated join type (Normal = inner, Master/Detail outer per the join condition).
- **Rank**: top/bottom N per the rank port, partitioned by the group ports.
- **Union**: concatenation of inputs (no dedup unless stated).
- **Expression / ports**: apply the port expressions in dependency order; preserve declared output types.

Then write a **single batched query** to `<proc_name>.assert.sql` in this exact shape:

```sql
  SELECT 'assert_01_<name>:' || CASE WHEN (<boolean>) THEN 'PASS' ELSE 'FAIL' END AS r
  UNION ALL SELECT 'assert_02_<name>:' || CASE WHEN (<boolean>) THEN 'PASS' ELSE 'FAIL' END
  UNION ALL ...
```

Cover, at minimum: the exact expected value(s) for each expected group/row in the target, the total expected
row count, and that dropped rows are ABSENT.

**Grade hardening (this is core — see [proc-assertion-patterns.md](proc-assertion-patterns.md)):** each
assertion MUST be a single, simple boolean referencing **only the target table** — a `COUNT(*)` comparison, a
scalar value comparison for one group, or a flat `NOT EXISTS (SELECT 1 FROM target WHERE …)`. **No nested or
correlated subqueries, no JOINs, no reference to source/lookup tables.** A simple assertion that runs is worth
far more than a clever one that errors — a malformed grade query is a false non-convergence that wastes fix
attempts.

### Phase 4: Baseline (seed → deploy-and-CALL → grade)

1. Run `<proc_name>.seed.sql` against `<db>.<test_schema>` (ARRANGE:SETUP once, then ARRANGE:SEED).
2. **ACT** — `scai code deploy-and-call … --proc-file <proc.sql> --call "CALL <proc>(...)"`. Read the
   `ProcCallResult`: `deployed=false` (failed to CREATE) or `called=false` (errored at CALL) is an expected
   baseline failure — record `errorText`.
3. **Grade** — if the proc CALLed clean, run `<proc_name>.assert.sql` and read the PASS/FAIL rows.
4. **Regenerate-on-erroring-grade (grade hardening):** if the assert query itself ERRORS (not FAIL — e.g. a
   bad column reference or an over-clever subquery), that is a test bug, not a proc bug. Simplify the offending
   assertion to a flat target-only form (per proc-assertion-patterns.md) and re-run — up to 2 regenerations —
   before recording any failure. Never let a malformed assertion count as a proc non-convergence.

### Phase 5: Report

Write `<UNIT>/stabilization/tests/proc/<proc_name>/test_report.md`:
- **Source→Proc mapping**: the transform chain and the target table.
- **Seed**: the frozen input rows (summary) and the hand-computed expected target.
- **Baseline result**: deployed / called / assert PASS-FAIL counts; per-failure `errorText` and which assertion
  failed; ACT-vs-ASSERT classification.
- **Coverage gaps**: transforms not reconstructable from source (dynamic SQL, external mapplets) → record the
  gap and escalate; do not fabricate an expected result.

**MANDATORY self-check before returning:** verify `<UNIT>/stabilization/tests/proc/<proc_name>/` contains
`<proc_name>.assert.sql`, `<proc_name>.seed.sql`, and `test_report.md`. If any is missing, generate it (or,
if you cannot write files, include full contents in your completion message). Then return to the parent skill
for proc-fixer.

## Reference Files (loaded on-demand)

| File | When to load |
|------|-------------|
| [proc-assertion-patterns.md](proc-assertion-patterns.md) | Phase 3 — the target-only batched assertion shape, per-transform worked examples, and the grade-hardening robustness rules |
| `{PLATFORM_DIR}/{transformation_guide}` (Informatica: `mapping-guide.md`) | Phase 1 — reading the source mapping structure (ports, expressions, join types, cache modes) |
| `{PLATFORM_DIR}/element-types.md` | Phase 1/3 — what each transform type does (active/passive, row-count effect, Aggregator/Lookup modes) |
| `{PLATFORM_DIR}/ewi/<CODE>.md` | when a block carries an EWI marker (resolve via `stabilization_tools.py ewi-guide-resolve`) |

---

## Task Mode (spawned by orchestrator)

### Input (provided at spawn time)
- Unit name + converted proc `.sql` path (READ-ONLY baseline)
- Source mapping `.xml` path (READ-ONLY)
- Target table name + the block FullName(s) under repair
- Test schema (`TEST_SCHEMA`) — pre-assigned; use for all created objects
- Database (`DATABASE`), connection name (`CONNECTION`)
- Skill directory (`SKILL_DIR`); platform directory (`PLATFORM_DIR`)
- Run all SQL headless via `scai code deploy-and-call` + `snow sql --format json` — no `snowflake_sql_execute`

### Autonomous behavior
- No user questions — reasonable defaults, documented in the report.
- On ambiguity (unclear transform semantics, missing source element): make a best-effort decision, document the
  assumption in test_report.md, continue. If a transform is genuinely non-reconstructable, record it as a
  coverage gap and escalate — do NOT fabricate an expected result.
- Write artifacts incrementally (seed, then assert, then report). Prefer stopping early with artifacts on disk
  over running to exhaustion.

### Team protocol
When complete, results return to the orchestrator automatically. Respond to a `shutdown_request` with
`send_message` `type: "shutdown_response"`, `approve: true`.
