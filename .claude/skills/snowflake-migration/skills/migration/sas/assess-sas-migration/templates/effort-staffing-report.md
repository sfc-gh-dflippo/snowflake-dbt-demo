# Effort & Staffing Report Template

Defines the **separate** deliverable `effort_staffing_plan.md`. This file holds the effort and
staffing estimates that used to live in the main report's Part 5, plus an embedded copy of the
**same Migration Wave Plan** so it is self-contained.

**Output file:** `<output_dir>/effort_staffing_plan.md` (alongside `assessment_complete.md`).

**When produced:** only when the user opts in at the Step 4 stopping point. The Migration Wave Plan
in the main report (Part 5) is always produced; this file additionally layers effort + staffing
onto that same plan.

**Sourcing:**
- Effort + staffing → apply formulas in `references/sizing-model.md`.
- Migration Wave Plan section → embed the **identical** wave plan generated for the main report's
  Part 5 (from `references/wave-planning.md`). Do not regenerate a different plan — the two must match.

---

## Report Body

```markdown
# Effort & Staffing Plan — {portfolio_name}

**Companion to:** `assessment_complete.md`
**Source:** `{source_path}`
**Date:** {date}

> Effort and staffing are estimates derived from tier/complexity heuristics, not commitments.
> Calibrate after the pilot wave. Sequencing follows the Migration Wave Plan below (identical to
> Part 5 of the assessment report).

## Summary

| Metric | Value |
|--------|-------|
| Total SAS Files | {total_files} |
| Calibrated Effort | {low}–{high} hr |
| Recommended Migration Waves | {wave_count} |

## Effort by Tier

| Tier | Files | Avg Effort/File | Total Hours |
|------|-------|-----------------|-------------|
| Tier 1 | {n} | {avg} hrs | {total} hrs |
| Tier 2 | {n} | {avg} hrs | {total} hrs |
| Tier 3 | {n} | {avg} hrs | {total} hrs |
| **Total (×1.15 overhead)** | **{n}** | | **{grand_total} hrs** |

## Staffing

| Role | Allocation | Duration |
|------|------------|----------|
| Snowflake SE (advisory) | {se_fte} FTE | {duration} |
| Developer(s) | {dev_count} FTE | {duration} |
| QA / Validation | {qa_fte} FTE | {duration} |

> Timeline derived from `calendar_weeks = total_effort_hours / (developer_count × 30 × 0.8)`
> (see `references/sizing-model.md`).

## Migration Wave Plan

> EMBED the identical wave plan from the assessment report's Part 5 here, verbatim.
> See `references/wave-planning.md` for the format.

| Wave | Scripts | Tier mix | Rationale | Entry gate |
|------|---------|----------|-----------|------------|
| 0 — Pilot | {n}: {names or cluster} | {tier mix} | {why these first} | Start of engagement |
| 1 — Independent Tier 1 | {n}: {cluster} | Tier 1 | {independent, fast wins} | Pilot validated |
| 2 — Procedural | {n}: {cluster} | Tier 2 | {state/BY-group review} | Wave 1 terminals validate |
| 3 — Complex / External | {n}: {names} | Tier 2/3 | {gated on source X} | Wave 2 validated + source ready |

### Effort by Wave (optional roll-up)

| Wave | Files | Effort (hrs) |
|------|-------|--------------|
| 0 — Pilot | {n} | {hrs} |
| 1 — Independent Tier 1 | {n} | {hrs} |
| 2 — Procedural | {n} | {hrs} |
| 3 — Complex / External | {n} | {hrs} |
```

---

## Generation Rules

1. Produce this file **only** when the user opted into effort & staffing at the Step 4 stopping
   point. Otherwise skip it silently — the wave plan still appears in the main report's Part 5.
2. Apply `references/sizing-model.md` for all effort and staffing figures; always show the ×1.15
   overhead total.
3. The "Migration Wave Plan" section MUST be identical to the main report's Part 5 — generate the
   wave plan once and embed the same content in both files.
4. The optional "Effort by Wave" roll-up maps the per-tier effort onto the waves; include it only
   if it adds clarity for the portfolio.
