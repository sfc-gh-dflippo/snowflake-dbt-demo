# Migration Wave Planning

How to break a SAS portfolio into **blocks of scripts** and sequence them into **migration
waves**. This reference is purely about *what migrates together and in what order* — it contains
**no effort, no staffing, and no durations**. (Effort and staffing live in `sizing-model.md`.)

The wave plan is the single source of truth for sequencing. It is generated **once** and embedded
verbatim in both the main report's "Part 5 — Migration Wave Plan" and the separate
`effort_staffing_plan.md` deliverable.

---

## Wave Grouping Principles

Assign every script to a wave using these rules, in priority order:

1. **Keep dependency clusters intact.** Scripts that share intermediate tables or form a connected
   sub-DAG migrate together, so each wave is independently testable and deployable. A cluster
   moves to the wave of its latest-ready / highest-tier member.
2. **Isolate externally-blocked scripts.** Any script that reads an external DB source
   (Oracle/DB2/Teradata), a dynamic `%INCLUDE`, or an unverified control table that is not yet
   available in Snowflake goes into a later wave, gated on that source becoming available.
3. **Sequence by tier, then confidence.** Within what remains, migrate Tier 1 before Tier 2 before
   Tier 3, and HIGH-confidence before LOW-confidence — front-loading fast, automatable wins.
4. **Pilot first.** Carve a small representative slice out of the above into a Wave 0 pilot to
   validate the approach before bulk conversion.

---

## Standard Wave Sequence

| Wave | Scope | Purpose |
|------|-------|---------|
| Wave 0 — Pilot | 5-10 representative scripts (mix of tiers + 1 complex stress test + 1 cross-file dependency) | Validate the conversion approach and patterns end-to-end before scaling |
| Wave 1 — Independent Tier 1 | Tier 1 scripts with no external blockers, in self-contained clusters | High automation, fast throughput, low risk |
| Wave 2 — Procedural | Tier 2 stored-procedure scripts and their dependency clusters | Manual review of state/BY-group logic |
| Wave 3 — Complex / Externally-dependent | Tier 3, highest-complexity, and external-DB-dependent scripts | Hardest work last; gated on source availability |

Waves are **logical groupings**, not a fixed count. A small portfolio may collapse to 2 waves; a
large one with several independent clusters may split Wave 1 into 1a/1b/1c so each cluster ships on
its own. Do not invent waves that have no scripts.

---

## Per-Script Wave Assignment Procedure

For each script, derive four attributes and bucket accordingly:

1. `cluster_id` — the connected sub-DAG it belongs to (from the dependency graph).
2. `tier` — TIER_1 / TIER_2 / TIER_3.
3. `confidence` — HIGH / MEDIUM / LOW.
4. `external_blocked` — true if it reads an external/unavailable source.

Assignment:
- If the script is in the curated pilot sample → **Wave 0**.
- Else if `external_blocked` → **final wave** (gated on source availability).
- Else assign by the cluster's highest tier: TIER_1 → Wave 1, TIER_2 → Wave 2, TIER_3 → Wave 3.
- Keep every member of a `cluster_id` in the **same** wave (use the latest wave any member requires).

---

## Pilot Selection Criteria

Select 5-10 scripts for Wave 0 that cover:
- At least 1 script from each tier present in the portfolio
- At least 1 HIGH complexity script
- At least 1 script with cross-file dependencies
- At least 1 script with external database references (if any)
- The most business-critical script (ask the customer)

---

## Wave Gate Criteria (qualitative — no calendar time)

| Transition | Gate |
|------------|------|
| Wave 0 → Wave 1 | Pilot scripts compile and pass validation; conversion patterns confirmed; no systemic issues |
| Wave 1 → Wave 2 | All Wave 1 terminal tables validate; Tier 1 throughput pattern is stable |
| Wave 2 → Wave 3 | Procedural scripts validated; external-source access for the final wave is confirmed available |

Each gate is a readiness condition, not a date. A wave begins when the prior wave's terminal
outputs validate and its blocking dependencies are resolved.

---

## Output Table Format (for the report)

Render the wave plan as:

```markdown
| Wave | Scripts | Tier mix | Rationale | Entry gate |
|------|---------|----------|-----------|------------|
| 0 — Pilot | {n}: {names or cluster} | {tier mix} | {why these first} | Start of engagement |
| 1 — Independent Tier 1 | {n}: {cluster} | Tier 1 | {independent, fast wins} | Pilot validated |
| 2 — Procedural | {n}: {cluster} | Tier 2 | {state/BY-group review} | Wave 1 terminals validate |
| 3 — Complex / External | {n}: {names} | Tier 2/3 | {gated on source X} | Wave 2 validated + source ready |
```

Tailor wave count and membership to the actual DAG and tier mix. Note any cluster that ships as its
own sub-wave, and call out the external source each gated wave depends on.
