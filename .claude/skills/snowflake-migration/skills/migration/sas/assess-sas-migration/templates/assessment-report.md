# Assessment Report Template

The skill renders this report when presenting results. It produces a single **merged report**
that combines the CLI's quantitative metrics (Parts 1-3) with the CoCo-native qualitative
analysis, migration wave plan, open questions, and recommendations (Parts 4-7).

**Output file:** `<output_dir>/assessment_complete.md` (the merged report). The CLI's raw
artifacts (`assessment.json`, `assessment_report.md`, `dependency_dag.mmd`) live alongside it.
Effort and staffing are NOT in this report — when requested they go to a separate
`effort_staffing_plan.md` (see `templates/effort-staffing-report.md`), which embeds the same
Migration Wave Plan shown in Part 5 here.

**Standalone mode (CLI not run):** Parts 1-3 are generated from direct source reading using
`references/complexity-analysis.md`. Title the report **"CoCo-native estimate (CLI not run)"**
and note that quantitative counts are LLM-derived.

---

## Report Header

```markdown
# SAS Migration Assessment — {portfolio_name}

**Source:** `{source_path}`
**CLI outputs:** `assessment.json`, `assessment_report.md`, `dependency_dag.mmd` (same folder)
**Date:** {date}
```

---

## Part 1 — Executive Summary

```markdown
# Part 1 — Executive Summary

| Metric | Value |
|--------|-------|
| Total SAS Files | {total_files} |
| Total Lines of Code | {total_lines:,} |
| Business Blocks | {total_blocks} ({n} macro-def · {n} DATA step · {n} PROC SQL) |
| Recommended Migration Waves | {wave_count} |

### Translation Tier Split

| Tier | Files | % | Approach |
|------|-------|---|----------|
| Tier 1 (SQL) | {t1_count} | {t1_pct}% | Pure SQL — CTAS / CTEs / window functions |
| Tier 2 (Stored Proc) | {t2_count} | {t2_pct}% | Snowflake stored procedures |
| Tier 3 (PySpark) | {t3_count} | {t3_pct}% | PySpark via Snowpark Connect |

### Complexity / Volume / Confidence

| Complexity | Count | % | | Volume | Count | % |
|---|---|---|---|---|---|---|
| LOW | {n} | {pct}% | | LOW | {n} | {pct}% |
| MEDIUM | {n} | {pct}% | | MEDIUM | {n} | {pct}% |
| HIGH | {n} | {pct}% | | HIGH | {n} | {pct}% |

- **Confidence:** {dist summary — e.g. MEDIUM 41 (100%), no LOW-confidence files}
- **Boilerplate:** {count flagged DI Studio / DataFlow-generated; note LOC inflation}

### Complexity × Volume Matrix

| | Low Volume | Medium Volume | High Volume |
|--|-----------|---------------|-------------|
| LOW Complexity | {n} | {n} | {n} |
| MEDIUM Complexity | {n} | {n} | {n} |
| HIGH Complexity | {n} | {n} | {n} |
```

---

## Part 2 — CLI Quantitative Detail

> Populate from `assessment.json`. In standalone mode, derive from direct source scanning and
> label counts as estimates.

```markdown
# Part 2 — CLI Quantitative Detail

## Block Type Distribution

| Block Type | Count |
|-----------|-------|
| DATA_STEP | {n} |
| PROC_SQL | {n} |
| MACRO_DEF | {n} |

## Top SAS Functions Used

| Function | Occurrences | | Function | Occurrences |
|----------|-------------|--|----------|-------------|
| {fn} | {n} | | {fn} | {n} |

## Per-File Details

| File | Lines | Blocks | Score | Complexity | Volume | Tier | Confidence |
|------|-------|--------|-------|------------|--------|------|------------|
| {filename} | {n} | {n} | {score} | {LOW/MED/HIGH} | {LOW/MED/HIGH} | {TIER_n} | {conf} |
```

---

## Part 3 — Dependency DAG

```markdown
# Part 3 — Dependency DAG ({node_count} nodes / {edge_count} edges)

{One-line topology description — e.g. "Fan-in funnel converging on the merge layer."}
Flow: `{stage1 → stage2 → ... → sink}`.
See `dependency_dag.mmd` for the full Mermaid diagram. External inputs: {count}.

| Most depended-on (fan-in) | Depends-on-most (fan-out) |
|---|---|
| {file} ({n}) | {file} ({n}) |

{Note the terminal sink / widest join if notable.}

### External Dependencies (referenced, not created in scope)

{Describe external inputs: macro variables, DICTIONARY tables, and — critically — real
external DB sources (Oracle/DB2/Teradata). Distinguish genuine external DB deps from
cross-file/control tables.}
```

---

## Part 4 — Complexity Analysis (CoCo-Native)

> Qualitative layer from reading `.sas` source directly (see `references/complexity-analysis.md`).
> Portfolio-level themes and hotspots — NOT a per-block dump.

```markdown
# Part 4 — Complexity Analysis

### Construct Hotspots

| Construct | Files | Recommended target |
|---|---|---|
| HASH objects (`declare hash`) | {n} | {SQL JOIN / PySpark} |
| CALL EXECUTE (dynamic loops) | {n} | {Stored proc / removable scaffolding} |
| PROC TRANSPOSE | {n} | CASE-WHEN pivot |
| PROC MEANS / SUMMARY (aggregation) | {n} | GROUP BY |
| INTNX / INTCK date logic | {n} occ | SQL date funcs (verify alignment) |
| External {engine} LIBNAME | {n} | Passthrough / pre-ingest to Snowflake |

### Top Complex Files

| File | Score | Tier | Dominant driver |
|---|---|---|---|
| {filename} | {score} | {T1/T2/T3} | {one-line driver} |

### Boilerplate Note

{e.g. "All N files are DataFlow-generated scaffolding (high line count, low business
complexity). After stripping M macro-def boilerplate blocks, ~K genuine business blocks remain."}

### Cross-Cutting Risks

1. {risk — e.g. single external dependency blocking DAG root}
2. {risk — e.g. CALL EXECUTE scaffolding, mostly deletable}
3. {risk — e.g. no statistical modeling → zero PySpark, de-risked}
4. {risk — e.g. uniform MEDIUM confidence drivers}
```

---

## Part 5 — Migration Wave Plan

> Apply `references/wave-planning.md`. Break the portfolio into dependency-aware blocks of scripts
> and sequence them into migration waves. NO effort, staffing, or durations here — those (when
> requested) go to the separate `effort_staffing_plan.md`, which embeds this same wave plan.

```markdown
# Part 5 — Migration Wave Plan

{One-line sequencing rationale — e.g. "Phased by dependency cluster: independent Tier 1 first,
external-DB-dependent scripts last (gated on source availability)."}

| Wave | Scripts | Tier mix | Rationale | Entry gate |
|------|---------|----------|-----------|------------|
| 0 — Pilot | {n}: {names or cluster} | {tier mix} | {representative slice to validate approach} | Start of engagement |
| 1 — Independent Tier 1 | {n}: {cluster} | Tier 1 | {self-contained, high automation} | Pilot validated |
| 2 — Procedural | {n}: {cluster} | Tier 2 | {state / BY-group review} | Wave 1 terminals validate |
| 3 — Complex / External | {n}: {names} | Tier 2/3 | {gated on external source X} | Wave 2 validated + source ready |

### Pilot Wave (Wave 0) Scripts

{List the 5-10 pilot scripts and why each was chosen — one from each tier, one HIGH complexity,
one cross-file dependency, one external-DB reference, the most business-critical.}

### Wave Gates

| Transition | Gate (qualitative — no calendar time) |
|------------|---------------------------------------|
| 0 → 1 | Pilot scripts compile and validate; patterns confirmed; no systemic issues |
| 1 → 2 | Wave 1 terminal tables validate; Tier 1 throughput stable |
| 2 → 3 | Procedural scripts validated; external-source access confirmed for the final wave |
```

> Tailor the wave count and membership to the actual DAG and tier mix. Collapse to fewer waves for
> small portfolios; split Wave 1 into per-cluster sub-waves (1a/1b/...) when independent clusters
> can ship separately. Do not invent empty waves.

---

## Part 6 — Open Questions & Dependencies to Clarify

> Items the customer must answer or provide before/early in the migration. Focus on
> **source availability and access gaps** — anything that would block conversion, compilation,
> or validation if unresolved. Derive these from the DAG's external inputs, missing %INCLUDE
> references, external DB LIBNAMEs, and unknown source schemas/volumes.

```markdown
# Part 6 — Open Questions & Dependencies to Clarify

### Source Availability & Access

| # | Question / Dependency | Why it matters | Blocks | Owner |
|---|----------------------|----------------|--------|-------|
| 1 | {e.g. Can we get read access + connection details for the Oracle source database?} | {DAG root depends on it} | Pilot | Customer |
| 2 | {e.g. Are the N external source tables (`X`, `Y`...) available in Snowflake, or must they be ingested?} | {Compilation will fail without them} | Pilot | Customer |
| 3 | {e.g. %INCLUDE 'lib.sas' references — can the source be provided?} | {Logic unavailable; stub only} | Conversion | Customer |
| 4 | {e.g. What are the row counts / refresh cadence of the top source tables?} | {Warehouse sizing + orchestration cadence} | Orchestration | Customer |
| 5 | {e.g. Are control tables (`&ETLS_CONTROLTABLE`, GROUP_1..6) static reference data or runtime-populated?} | {Affects whether they're seeded or pipeline-built} | Conversion | Customer |

### Missing / Unverified Inputs

| Input | Type | Status | Action Needed |
|-------|------|--------|---------------|
| {table/file/macro var} | {External DB / %INCLUDE / control table} | {Not in scope / unverified} | {Provide / grant access / confirm} |

### Resolution Priority

| Priority | Item | Needed By |
|----------|------|-----------|
| P1 (blocks pilot) | {external DB access, root source tables} | Before Phase 1 |
| P2 (blocks batch) | {schemas, volumes, control-table semantics} | Before Phase 2 |
| P3 (clarification) | {refresh cadence, naming conventions} | During pilot |
```

---

## Part 7 — Recommendations & Next Steps

```markdown
# Part 7 — Recommendations & Next Steps

1. **{Migration approach}** — {e.g. phased by dependency cluster given fan-in funnel}.
2. **{Risk posture}** — {e.g. de-risked: 0 Tier-3, 0 statistical modeling, 0 LOW-confidence}.
3. **{Unblock first}** — {e.g. ingest the N external source tables before pilot}.

### Pilot File Suggestions (representative mix)

- {file} — Tier 1, baseline
- {file} — Tier 2, stored proc
- {file} — HIGH complexity, stress test
- {file} — cross-file dependency, integration test

### Handoff to Conversion

To begin conversion, ask to **convert the SAS programs to Snowflake** — the migration router
loads the `convert-sas-to-snowflake` skill.

The conversion skill consumes `assessment.json` at Step 3 to skip re-classification, saving
time on large portfolios.
```

---

## Generation Rules

1. **Always produce the merged report** as a single `assessment_complete.md`, using the part
   ordering above.
2. **Parts 1-3 (quantitative):** populate from `assessment.json` when the CLI ran; otherwise
   derive from direct source reading and label as a CoCo-native estimate.
3. **Part 4 (complexity):** portfolio-level themes and hotspots only — no per-block table.
4. **Part 5 (wave plan):** apply `references/wave-planning.md`; break scripts into dependency-aware
   blocks and sequence into waves. NO effort/staffing in this report. When the user opted into
   effort & staffing, also write `effort_staffing_plan.md` (per `templates/effort-staffing-report.md`)
   embedding this same wave plan.
5. **Part 6 (open questions):** ALWAYS include. Focus on source & access gaps that would block
   pilot/conversion/validation. If nothing is outstanding, state "No open dependencies — all
   sources available in scope."
6. **Part 7 (recommendations):** tailor to the data (tier mix, DAG shape, external deps).
7. **Mermaid:** reference `dependency_dag.mmd`; do not inline large diagrams.
