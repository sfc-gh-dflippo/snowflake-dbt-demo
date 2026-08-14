---
name: dbt-audit
description:
  "Audit dbt projects for anti-patterns and produce an HTML quality assessment with prioritized
  remediation. Use when: reviewing, auditing, assessing, grading, or health-checking a dbt project
  or an estate of projects; asking what is wrong with a dbt project or where its technical debt is;
  finding dbt anti-patterns; evaluating migrated dbt output. Covers project fragmentation,
  truncate/delete-load instead of incremental models, subqueries that should be CTEs or ephemeral
  models, macro over-use and under-use, materialization fitness, test and documentation coverage,
  and unresolved lift-and-shift conversion debt. Triggers: audit dbt, dbt audit, review my dbt
  project, dbt quality assessment, dbt anti-patterns, dbt health check, assess dbt project, grade
  dbt project, what is wrong with my dbt project, dbt technical debt, dbt best practice check, is my
  dbt project any good, too many dbt projects, dbt code review."
---

# dbt Anti-Pattern Audit

Produce a dbt quality assessment: a deterministic Python analyzer emits suggestions as JSON, then
you render an HTML report with prioritized remediation.

The split is deliberate. Suggestions must be reproducible run to run so a customer can re-audit
after a sprint and see movement — that is the analyzer's job. The remediation narrative must reflect
this specific project, so it is yours.

## Stopping Points

- **Before running `dbt parse`:** always ask via `ask_user_question`. It writes inside the user's
  project.
- **Before writing the HTML report:** confirm a durable output location if none is obvious. Never
  write the report or `suggestions.json` into the user's repo without asking; use scratch.
- **Before reporting a suggestion:** spot-check two or three against the actual files.

## Routing

| User intent                                                 | Surface                                                                               |
| ----------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| "Check this one model" / a save-time hook fired             | **`dbt-validate` skill** — one file, model-scoped rules                               |
| "Populate the Problems panel" / CI gate                     | **`dbt-lint`** — whole project, one line per suggestion, `--strict` exits 1 on errors |
| "Audit my project" / "assess this estate" / customer review | **`dbt-audit`** — this skill: all rules, `suggestions.json` plus HTML report          |

|             | `dbt-validate`        | `dbt-lint`                        | `dbt-audit`                         |
| ----------- | --------------------- | --------------------------------- | ----------------------------------- |
| Scope       | One model file        | A project or path                 | A project, or an estate             |
| Rules       | Model-scoped only     | Model-scoped                      | All rules                           |
| Output      | Suggestions to stderr | One line per suggestion to stdout | `suggestions.json` plus HTML report |
| Typical use | Save hook             | Editor task, CI                   | Full assessment                     |

---

## Reference: Rule Packs

Ten packs. Run `uv run audit.py rules` for the current catalog with tiers and levels.

| Pack | Concern                                          |
| ---- | ------------------------------------------------ |
| PRJ  | Project structure and fragmentation              |
| INC  | Load patterns and incremental correctness        |
| SQL  | Query construction: subquery vs CTE vs ephemeral |
| MAC  | Macro over-use and under-use                     |
| MAT  | Materialization fitness                          |
| TST  | Testing and constraint coverage                  |
| DOC  | Documentation coverage                           |
| ARC  | Architecture and lineage conventions             |
| MIG  | Unresolved conversion debt                       |
| OPS  | Operational hygiene                              |

**Load** [references/rule-catalog.md](references/rule-catalog.md) for per-rule detection signal and
the practice each protects — when a user asks why something was flagged or disputes a suggestion.

---

## Reference: Lift-and-Shift Tiers

Every rule carries a tier, and the engine suppresses one tier for converted projects.

| Tier             | Applies to                                                                                                                | Suppressed?                                                                          |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| **UNIVERSAL**    | Always. A truncate-and-load is wrong whether a person wrote it or a converter emitted it.                                 | Never                                                                                |
| **ARCHITECTURE** | Medallion folders, layer-crossing lineage — a greenfield ideal.                                                           | Yes, when the project is detected as mechanically converted from Informatica or SSIS |
| **MIGRATION**    | Fires _because_ the code was converted: unresolved `SSC-EWI`/`SSC-FDM` markers, ETL control columns, shipped scaffolding. | Never                                                                                |

Two rules for the report:

1. **Suppression is not absolution.** Detecting machine-generated code excuses it from architectural
   expectations, not from defects. Converter output routinely contains genuine anti-patterns — a
   project per data flow, `DELETE FROM {{ this }}` in a `pre_hook`, folder hooks that truncate once
   per model, per-transformation model chains. Report all of those.
2. **State what was suppressed.** Give the count and the reason, so nobody reads a clean summary as
   "no architectural debt." Present it as a modernization opportunity, separate from the suggestion
   list.

Provenance detection is automatic and evidence-based. If the user disputes the classification, show
them `projects[].provenance.signals` from the JSON and offer `.dbt-quality.yml`
(`migration.mode: native | lift_and_shift`, `migration.paths`).

---

## Workflow

### Step 1: Establish Scope

**Goal:** Know what to audit before running anything.

**Actions:**

1. Ask what to audit if it is not already clear.
2. Prefer the estate root over a single project when the user has more than one. Pointing at a
   parent directory discovers every `dbt_project.yml` beneath it, and that tree mode is the only way
   fragmentation suggestions can fire.

### Step 2: Check Artifacts, Then Offer Generation

**Goal:** Know which rules can actually be evaluated.

**Actions:**

1. Check manifest coverage:

   ```bash
   cd .claude/plugins/dbt-quality/scripts
   uv run audit.py manifest-status <path>
   ```

   Ephemeral fan-out, layer-crossing dependencies, and single-consumer models need
   `target/manifest.json`. Without it they are reported as **skipped**, never as passing.

2. If any project needs a parse, **ask the user first** via `ask_user_question`. State the trade-off
   plainly: `dbt parse` executes no models and uses no warehouse compute, but it needs a working
   profile and it writes to `target/`. Offer three options — run it now, audit without the graph
   checks, or the user runs it themselves.

   ⛔ **Never run `dbt parse` unprompted.** It writes inside the user's project.

3. If `target/catalog.json` exists, inspect it before making contextual recommendations:
   - **Clustering:** use the Snowflake relation type, approximate rows, bytes, and last-modified
     time to explain whether the relation warrants investigation. Do not recommend a clustering key
     until query predicates and pruning behavior justify one.
   - **`source()` vs `ref()`:** compare exact catalog `database`, `schema`, and relation `name`
     values for sources and dbt nodes. An exact match is a `ref()` candidate because it restores
     lineage and build ordering. Keep `source()` when the relation is an intentionally independently
     deployed contract boundary.

   Catalog evidence guides your report; it is not a static lint finding by itself.

### Step 3: Run the Audit

**Goal:** Produce `suggestions.json`.

**Actions:**

1. Run the analyzer, writing output to scratch:

   ```bash
   uv run audit.py audit <path> --out <scratch>/suggestions.json
   ```

   The analyzer never runs dbt, never connects to a warehouse, and writes nothing inside the audited
   project except the suggestions file you name. Keep `suggestions.json` out of the user's repo.

2. If `uv` cannot reach its index — common on configured corporate installs — fall back to:

   ```bash
   UV_DEFAULT_INDEX=https://pypi.org/simple uv run --no-config --no-project \
     --with pyyaml --with typer --with rich python audit.py audit <path> --out <path>
   ```

### Step 4: Read the Suggestions Before Writing Anything

**Goal:** Understand the findings well enough to rank them.

**Actions:**

1. Open `suggestions.json` and work from `summary`, `remediation`, and `suppressed`. `remediation`
   is already grouped by rule and ranked by impact over effort — trust that ordering; it is what
   makes the report actionable rather than a list.

   The summary prints like this:

   ```text
   Projects: 1   Models: 41
   Suggestions: 208 — 2 error, 7 warning, 199 information
   Severity: 2 critical, 6 high, 111 medium, 89 low
   Per model: 5.07
   Manifest coverage: 1/1   Rules skipped: 0
   ```

   `per_model` is the number to track across re-audits; raw counts are not comparable across
   projects of different sizes. No grade or score is produced — the engine lacks the context to
   justify a verdict on heuristic rules whose applicability only you can settle.

2. Read each suggestion on its three independent axes:

   | Axis       | Values                              | Meaning                                                                                                                                                                                                                                        |
   | ---------- | ----------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
   | `kind`     | `EWI`, `FDM`, `PRF`                 | What the rule is: an issue, a functional difference where model results diverge from the source system, or performance/cost                                                                                                                    |
   | `level`    | `error`, `warning`, `information`   | Confidence that something is wrong: `error` admits no legitimate condition, `warning` is a real problem in nearly all cases, `information` (the default) is context-dependent and states the condition under which the code is already correct |
   | `severity` | `critical`, `high`, `medium`, `low` | Blast radius if the rule is right                                                                                                                                                                                                              |

   Level and severity are orthogonal: a rule can be `information` level and `critical` severity,
   because "likely fine, but catastrophic if wrong" is a real position. Rule codes such as
   `SSC-EWI-DBTOPS0002` follow SnowConvert's `SSC`/`EWI` documentation convention — this project is
   part of the SnowConvert team in Snowflake Engineering and adopts those conventions for
   consistency. Nothing blocks a save at any level; gate on errors in CI with `dbt-lint --strict`.

3. Spot-check two or three suggestions against the actual files before reporting them. The analyzer
   is text-level by design and can misread unusual formatting. One obviously wrong suggestion costs
   the reader's trust in all of them.

### Step 5: Render the HTML Report

**Goal:** A self-contained report that renders in the Snowflake sandbox.

**Load** [references/report-spec.md](references/report-spec.md) for structure and the full sandbox
rules. The essentials, because getting these wrong produces a blank page:

- Self-contained: no CDN, no remote fonts, no remote images, no `fetch`.
- Charts from `/libs/chart.js@4.4.4/chart.umd.js` only.
- No inline event handlers — use `addEventListener` inside an inline `<script>`.
- `:root { color-scheme: light dark; }` and `light-dark()` colors, so it is readable in both themes.
- Include `<meta name="snowflake-source" content="cortex-agent-authored">` and the
  `snowflake-report-metadata` provenance block.

Save it somewhere durable — the workspace by default, never `/tmp`. Ask if no durable location is
obvious.

### Step 6: Report and Offer Next Steps

**Goal:** A summary the user can act on.

**Actions:**

1. Summarize in two or three sentences: the counts and per-model rate, the single highest-leverage
   fix, and anything suppressed or skipped.
2. Offer to fix the top suggestion. Most are a few lines, and a customer who watches one get fixed
   engages with the rest.

---

## Writing Remediation That Gets Acted On

The analyzer supplies a remediation string per rule. Improve on it with what only you can see:

- **Use their identifiers.** "Add `unique_key='order_line_id'`" beats "add a unique key." Read the
  model and name the real column.
- **Group the work.** 43 models missing a primary-key test is one afternoon, not 43 tickets. Say so,
  and say which layer to start with.
- **Sequence dependent fixes.** Renaming ETL-named models is much cheaper after collapsing
  per-transformation chains, because there are fewer names left to choose. Point that out rather
  than listing both as peers.
- **Say what breaks if ignored.** Not "violates best practice" but "reprocessing duplicates rows
  silently, and no test would catch it."
- **Concede genuine trade-offs.** Some suggestions are defensible choices; a single large project
  may be intentional. Ask rather than assert when the evidence is ambiguous, and record the decision
  so the next audit does not re-raise it.

Do not inflate. If a project is in good shape, say so and keep the report short. An audit that
manufactures concern to look thorough is worse than no audit.

---

## Configuration

`.dbt-quality.yml` at the audit root, all optional: thresholds, `migration.mode`, `migration.paths`,
`disabled_rules`. Full schema in [`../../scripts/README.md`](../../scripts/README.md).

`disabled_rules` accepts any exact registered rule ID. A disabled rule emits no suggestion, does not
affect lint counts, and is reported as skipped with `disabled in .dbt-quality.yml`. Use it for
project-specific exceptions rather than inline suppression comments.

**Names are not audited.** If someone asks why: a model may keep the name its object had in the
source database it was migrated from, and a dbt project records that name nowhere machine-readable.
The prescribed `/* Original Object: */` header is a comment that never reaches `manifest.json`;
`meta.original_object` and any crosswalk file do not exist; the one real source-to-target mapping
sits in SnowConvert's external registry and writes nothing back. A naming rule would be guessing, so
there is none. Full reasoning in [references/rule-catalog.md](references/rule-catalog.md).

---

## References

| File                                                     | Load when                                                                     |
| -------------------------------------------------------- | ----------------------------------------------------------------------------- |
| [references/rule-catalog.md](references/rule-catalog.md) | A user asks why a rule fired, disputes a suggestion, or you are adding a rule |
| [references/report-spec.md](references/report-spec.md)   | Rendering the HTML report                                                     |
| [`../../scripts/README.md`](../../scripts/README.md)     | Configuring thresholds, or running the analyzer directly                      |

## Related Skills

`dbt-architecture`, `dbt-modeling`, `dbt-materializations`, `dbt-testing`, and `dbt-performance`
state the practices this audit inverts. Cite them when a user wants the positive guidance behind a
suggestion.
