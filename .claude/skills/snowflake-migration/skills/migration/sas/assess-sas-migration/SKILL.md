---
name: assess-sas-migration
parent_skill: sas
description: "Preview. Assess SAS migration complexity and volume for Snowflake. Produces portfolio analysis with tier distribution, complexity heatmap, dependency DAG, a migration wave plan, and (on request) a separate effort/staffing plan. Triggers: assess SAS, SAS assessment, migration complexity, SAS analysis, SAS dependency diagram, migration waves, migration phases, migration sizing, LOE estimate SAS, SAS volume analysis, SAS migration readiness."
license: Proprietary. See License-Skills for complete terms
---

# Assess SAS Migration

> © Snowflake Inc. This skill and its contents are the proprietary intellectual property of Snowflake Inc.

Analysis-only tool for assessing SAS-to-Snowflake migration complexity, volume, and sequencing.

**Purpose:** Pre-conversion assessment that informs the `convert-sas-to-snowflake` skill with portfolio-level insights, per-file tier classification, and a migration wave plan.

**Output:** A merged assessment report (`assessment_complete.md`) covering executive
summary, CLI quantitative detail, dependency DAG, complexity analysis, a migration wave plan,
open questions & dependencies, and recommendations — backed by the CLI's JSON/Markdown/Mermaid
artifacts. On request, a separate `effort_staffing_plan.md` adds effort + staffing and embeds the
same wave plan.

---

## Architecture

```
User provides SAS files
        │
        ▼
┌─────────────────────────────┐
│  Python CLI (assess_sas.py) │  ← Standalone, no Snowflake needed
│  - Parse .sas files         │
│  - Score complexity         │
│  - Classify tiers           │
│  - Build dependency graph   │
└──────────────┬──────────────┘
               │ Produces:
               ▼
    assessment.json
    assessment_report.md
    assessment_report.html
    dependency_dag.mmd
               │
               ▼
┌─────────────────────────────┐
│  This Skill (CoCo layer)    │  ← Adds judgment + qualitative analysis
│  - Complexity analysis      │     (reads .sas source directly)
│  - Migration wave plan      │
│  - Effort estimation (opt-in)│
│  - Staffing model (opt-in)  │
│  - Executive summary        │
└─────────────────────────────┘
```

**Two analysis layers:**
1. **Python CLI (default, quantitative):** parses, scores, classifies, builds the DAG. Fast and deterministic.
2. **CoCo-native (additive, qualitative):** the skill reads the `.sas` files directly to explain *areas of complexity* — themes, construct hotspots, and risks — on top of the CLI numbers. If the CLI cannot run (no Python, or user opts out), this layer runs **standalone** using the heuristics in `references/complexity-analysis.md`.

---

## Workflow

### Step 1: Gather Input

Ask user for:
1. SAS source path (file, directory, or already-generated `assessment.json`)
2. Output location

**Default path:** Run the Python CLI for quantitative metrics, then add the CoCo-native
complexity layer (Step 4) on top.

Branch on what's available:
- **`assessment.json` already exists** → skip the CLI, present it (Step 3), then add CoCo analysis (Step 4).
- **SAS files provided + Python available** → run the CLI (Step 2), present (Step 3), add CoCo analysis (Step 4).
- **Python unavailable or user opts out** → skip Steps 2-3; run Step 4 in **standalone mode** (CoCo reads `.sas` directly and produces both distributions and the complexity narrative).

### Step 2: Run Assessment Tool

Execute the standalone Python CLI:

```bash
cd <skill_dir>/tool
python assess_sas.py <source_path> --output <output_dir>
```

**Expected output:**
- `<output_dir>/assessment.json` — structured metrics
- `<output_dir>/assessment_report.md` — human-readable report
- `<output_dir>/assessment_report.html` — self-contained, SCAI-themed HTML report (KPIs, tier mix, complexity/volume charts, dependency DAG, per-file detail). Open in a browser; share as the visual deliverable.
- `<output_dir>/dependency_dag.mmd` — Mermaid dependency graph

Use `--format html` to emit only the HTML report, or `--format all` (default) for every artifact.

If the tool fails, check:
- Python >= 3.8 available
- Source path contains `.sas` files
- Output directory is writable

### Step 3: Present Assessment Results

Read `assessment.json` and present:

> **Two independent axes** (see `../references/block-tiering-spec.md`):
> **Translation tier** (Tier 1/2/3) is *how* each block migrates (SQL / stored proc / notebook)
> and is computed identically to the `convert-sas-to-snowflake` skill — a file is Tier 3 if it
> has any Tier-3 block, else Tier 2 if any Tier-2 block, else Tier 1. **Complexity**
> (LOW/MEDIUM/HIGH) is a separate volume/effort score used only for sizing and wave planning. A
> file can be Tier 1 yet HIGH complexity, or Tier 3 yet LOW complexity. Do not conflate them.

1. **Executive Summary** (4 KPIs):
   - Total files / Total lines
   - Tier distribution (% Tier 1 / 2 / 3)
   - Complexity split (% LOW / MEDIUM / HIGH)

2. **Complexity x Volume Heatmap** (3x3 matrix)

3. **Tier Distribution** with approach descriptions

4. **Top Complex Files** (highest scoring, most likely to need manual review)

5. **Dependency DAG** (render Mermaid or describe topology)

### Step 4: CoCo-Native Complexity Analysis (additive)

After the CLI metrics are presented, **read the `.sas` source files directly** to add a
qualitative complexity narrative. This is the layer that explains *why* files are complex and
*what* will need attention — the numbers alone don't tell that story.

**Load `references/complexity-analysis.md`** for the construct catalog and heuristics. Keep
these aligned with the CLI so the narrative does not contradict `assessment.json`.

Produce a **portfolio-level summary** (not a per-file or per-block dump):

1. **Areas of Complexity (themes):** aggregate construct findings across files — report the
   theme, count of files affected, and migration implication (e.g. "Statistical modeling in 4 files → PySpark").
2. **Construct hotspots:** short table of the most impactful construct categories (HASH,
   CALL EXECUTE, stat PROCs, multi-OUTPUT, INTNX/INTCK) with file counts and target tier.
3. **Top complex files:** 5-10 highest-complexity files, one line each on the dominant driver.
   Rank by CLI `overall_score` when available; otherwise by Tier 3/2 construct density × volume.
4. **Boilerplate note:** flag DI Studio / DataFlow scaffolding as high-volume / low-complexity.
5. **Cross-cutting risks:** external DB dependencies, dynamic %INCLUDE, statistical modeling,
   circular cross-file dependencies.

Use the **Complexity Analysis Section** in `templates/assessment-report.md` for formatting.

**Standalone mode (CLI not run):** If the Python tool was not run (no Python available, or
the user is working purely through CoCo), generate this entire analysis from direct source
reading — including the Executive Summary tier/complexity distributions derived from the
heuristics. Label the report **"CoCo-native estimate (CLI not run)"** so consumers know the
counts are LLM-derived, not tool-computed.

### Step 5: Migration Wave Planning

**Load `references/wave-planning.md`.**

Always runs — the wave plan is core to the assessment report (Part 5). Break the portfolio into
**dependency-aware blocks of scripts** and sequence them into **migration waves**. NO effort,
staffing, or durations at this step.

Produce:
- A wave table (Wave · Scripts · Tier mix · Rationale · Entry gate)
- The pilot wave (Wave 0) script selection with rationale
- Qualitative wave gates (no calendar time)

Keep dependency clusters intact, isolate externally-blocked scripts into a later gated wave, and
sequence the rest Tier 1 → Tier 2 → Tier 3. This wave plan is generated **once** and reused
verbatim in both Part 5 of the report and (if requested) the effort & staffing file.

### Step 5b: Effort & Staffing (opt-in — separate deliverable)

Run **only if** the user opted in at the Step 4 stopping point. **Load `references/sizing-model.md`.**

Apply per-file effort based on:
- Tier: Tier 1 = base effort, Tier 2 = moderate, Tier 3 = highest
- Confidence: LOW confidence = multiplier
- Volume: HIGH volume files take longer

Produce (for the separate `effort_staffing_plan.md`, NOT the main report):
- Total estimated effort (hours) and effort by tier
- Suggested team composition (staffing)
- The **same** Migration Wave Plan from Step 5, embedded verbatim

This becomes the `effort_staffing_plan.md` file written in Step 8.

### Step 6: Open Questions & Dependencies to Clarify

Identify everything the customer must answer or provide before/early in the migration, with a
focus on **source availability and access gaps** — anything that would block conversion,
compilation, or validation if unresolved. Derive these from:
- The DAG's external inputs (`assessment.json` external refs / `dependency_dag.mmd`)
- External DB LIBNAMEs (Oracle/DB2/Teradata) and their source tables
- `%INCLUDE` references whose source is not in scope
- Control/reference tables of unknown provenance (static seed vs runtime-built)
- Unknown source schemas, row counts, and refresh cadence (affects orchestration)

Use the **Part 6** format in `templates/assessment-report.md`: an Open Questions table
(question · why it matters · what it blocks · owner), a Missing/Unverified Inputs table, and a
Resolution Priority (P1 blocks pilot wave / P2 blocks later waves / P3 clarification). If nothing
is outstanding, state "No open dependencies — all sources available in scope."

### Step 7: Recommendations

Based on assessment data, provide:

1. **Migration approach recommendation:**
   - If >80% Tier 1: "Highly automatable — bulk conversion in early waves"
   - If >20% Tier 3: "High complexity — pilot with complex scripts first, defer the rest to a later wave"
   - If many cross-file dependencies: "Wave-based migration by dependency cluster"

2. **Risk areas:**
   - Files with LOW confidence
   - External database dependencies
   - Statistical PROCs requiring PySpark

3. **Wave recommendation:**
   - Reference the Migration Wave Plan from Step 5 (Wave 0 pilot → independent Tier 1 → procedural
     Tier 2 → complex/external Tier 3). Do not restate effort or staffing here.

4. **Handoff to conversion skill:**
   - "Ask to convert the SAS programs to Snowflake to begin conversion" (routes to `convert-sas-to-snowflake`)
   - The conversion skill can consume `assessment.json` at Step 3 to skip re-classification

### Step 8: Assemble Final Merged Report

Write the complete assessment to `<output_dir>/assessment_complete.md` using the **merged
multi-part format** in `templates/assessment-report.md`:

1. Part 1 — Executive Summary
2. Part 2 — CLI Quantitative Detail (block types, top functions, per-file table)
3. Part 3 — Dependency DAG (topology + fan-in/fan-out + external deps)
4. Part 4 — Complexity Analysis (themes, hotspots, top complex files, risks)
5. Part 5 — Migration Wave Plan (dependency-aware blocks + wave sequence; NO effort/staffing)
6. Part 6 — Open Questions & Dependencies to Clarify
7. Part 7 — Recommendations & Next Steps

This single file is the primary deliverable. The CLI's raw artifacts (`assessment.json`,
`assessment_report.md`, `assessment_report.html`, `dependency_dag.mmd`) remain alongside it as
supporting detail — `assessment_report.html` is the shareable, SCAI-styled visual report. Point the
user to it as the browser-friendly counterpart to `assessment_complete.md`.

**Effort & staffing file (opt-in):** If the user opted into effort & staffing at Step 4, ALSO
write `<output_dir>/effort_staffing_plan.md` using `templates/effort-staffing-report.md` — effort
by tier, staffing, and the **same** Migration Wave Plan embedded verbatim from Part 5. If the user
did not opt in, skip this file; the wave plan still appears in Part 5 of the main report.

**Standalone mode:** When the CLI was not run, generate Parts 1-3 from direct source reading
and title the report "CoCo-native estimate (CLI not run)".

---

## Stopping Points

- ✋ Step 1: Confirm source path and output location
- ✋ Step 3: Present CLI assessment results — confirm before deeper analysis
- ✋ Step 4: Present complexity analysis — the Migration Wave Plan is always produced; ask whether to ALSO produce the separate effort & staffing file (`effort_staffing_plan.md`)
- ✋ Step 7: Present recommendations
- ✋ Step 8: Confirm before writing the final merged report (and the effort & staffing file if opted in)

---

## Integration with convert-sas-to-snowflake

The assessment output (`assessment.json`) can be consumed by the conversion skill:
- **Auto-discovered — no manual co-location needed.** At Step 3 the conversion skill searches common
  locations (its own output dir, the SAS source dir, `assessment_output/`, and a shallow glob) for
  `assessment.json` and consumes the most recent readable match. If none is found it proceeds
  silently with fresh classification (no prompt).
- At Step 3 (Classify Each Block): pre-computed tier classifications are available
- At Step 4 (Present Block Analysis): dependency graph already built
- **Baseline reconciliation:** conversion compares its own per-file block counts and tiers against
  the assessment and flags any mismatch (a signal the assessment is stale or a bug) — informational,
  never blocking. Both skills share `../references/block-tiering-spec.md`, so a current assessment
  should match exactly.
- Reduces conversion startup time for large portfolios

---

## Python Tool Location

The standalone CLI lives at: `assess-sas-migration/tool/assess_sas.py`

**No Snowflake connection required.** The tool uses Python standard library only (no pip install needed).

See `tool/README.md` for CLI usage, threshold tuning, and architecture details.
