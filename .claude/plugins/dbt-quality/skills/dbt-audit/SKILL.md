---
name: dbt-audit
description: >-
  Audit dbt projects for anti-patterns and produce an HTML quality assessment with prioritised
  remediation. Use when asked to review, audit, assess, grade, or health-check a dbt project or an
  estate of dbt projects; when asked what is wrong with a dbt project or where its technical debt
  is; or when asked to find dbt anti-patterns, check dbt best practices, or evaluate migrated dbt
  output. Covers project fragmentation (a separate project per one or two models),
  truncate/delete-load instead of incremental models, subqueries that should be CTEs or ephemeral
  models, macro over-use and under-use, materialization fitness, test and documentation coverage,
  and unresolved lift-and-shift conversion debt. Triggers - audit dbt, dbt audit, review my dbt
  project, dbt quality assessment, dbt anti-patterns, dbt health check, assess dbt project, grade
  dbt project, what is wrong with my dbt project, dbt technical debt, dbt best practice check, is my
  dbt project any good, too many dbt projects, dbt code review.
---

# dbt Anti-Pattern Audit

Produces a dbt quality assessment: a deterministic Python analyzer emits suggestions as JSON, then
you render an HTML report with prioritised remediation.

The split is deliberate. Suggestions must be reproducible run to run, so a customer can re-audit
after a sprint and see movement — that is the analyzer's job. The remediation narrative has to
reflect _this_ project, so it is yours.

---

## What this audits

Ten rule packs. Run `rules` to list the current catalogue with tiers and levels.

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

Detail per rule, including detection signal and the practice each protects, is in
`references/rule-catalog.md`. Load it when a user asks why something was flagged or disputes a
suggestion.

---

## Three entry points

The engine exposes three surfaces. Choose based on what you need:

|             | `dbt-validate`        | `dbt-lint`                        | `dbt-audit`                      |
| ----------- | --------------------- | --------------------------------- | -------------------------------- |
| Scope       | one model file        | a project or path                 | a project, or an estate          |
| Rules       | model-scoped only     | model-scoped                      | all rules                        |
| Output      | suggestions to stderr | one line per suggestion to stdout | `suggestions.json` + HTML report |
| Typical use | save hook             | editor task, CI                   | full assessment                  |

- **`dbt-validate`** — runs automatically on every save via the plugin hook. Use the `dbt-validate`
  skill for this surface.
- **`dbt-lint`** — runs the whole project and emits compiler-style output. Use it to populate the
  Problems panel in Cortex Code Desktop, or as a CI step with `--strict`. Fast: no HTML, no JSON,
  just lines.
- **`dbt-audit`** — the full assessment: generates `suggestions.json` then an HTML report with
  grouped remediation. Use it for customer-facing reviews, sprint retrospectives, or any time you
  want the narrative format.

---

## Lift-and-shift — read this before reporting

Rules carry a tier, and the engine suppresses one of them for converted projects:

- **UNIVERSAL** — always applies. A truncate-and-load is wrong whether a person wrote it or a
  converter emitted it.
- **ARCHITECTURE** — medallion folders, layer-crossing lineage. **Suppressed** when the project is
  detected as mechanically converted from Informatica or SSIS. That layout was never the customer's
  choice, and burying real suggestions under naming violations on generated code makes the report
  useless.
- **MIGRATION** — fires _because_ the code was converted: unresolved `SSC-EWI`/`SSC-FDM` markers,
  ETL control columns, shipped scaffolding. Never suppressed.

Two things to hold onto when you write the report:

1. **Suppression is not absolution.** Detecting that code was machine-generated excuses it from
   architectural expectations, not from defects. Converter output routinely contains genuine
   anti-patterns — a project per data flow, `DELETE FROM {{ this }}` in a `pre_hook`, folder hooks
   that truncate once per model, per-transformation model chains. Report all of those.
2. **Say what was suppressed.** The report must state the count and the reason, so nobody takes a
   clean suggestions summary as "no architectural debt". Present it as a modernisation opportunity,
   separate from the suggestion list.

Provenance detection is automatic and evidence-based. If the user disputes the classification, show
them `projects[].provenance.signals` from the JSON and offer `.dbt-quality.yml`
(`migration.mode: native | lift_and_shift`, `migration.paths`).

---

## Workflow

### Step 1 — Establish scope

Ask what to audit if it is not already clear, and remember tree mode exists: pointing at a parent
directory discovers every `dbt_project.yml` beneath it. That is the only way the fragmentation
suggestions can fire, so prefer the estate root over a single project when the user has more than
one.

### Step 2 — Check artifacts, then offer generation

```bash
cd .claude/plugins/dbt-quality/scripts
uv run audit.py manifest-status <path>
```

Several checks need `target/manifest.json`: ephemeral fan-out, layer-crossing dependencies, and
single-consumer models. Without it they are reported as **skipped**, never as passing.

If the command reports projects needing a parse, **ask the user before running it** via
`ask_user_question`. Give them the trade-off plainly: `dbt parse` executes no models and uses no
warehouse compute, but it needs a working profile and it writes to `target/`. Offer three options —
run it now, audit without the graph checks, or they will run it themselves.

Never run `dbt parse` unprompted. It writes inside their project.

When the project has `target/catalog.json`, inspect it before making contextual recommendations:

- For clustering, use the Snowflake relation type, approximate rows, bytes, and last-modified time
  to explain whether the relation warrants investigation. Do not recommend a clustering key until
  query predicates and pruning behavior justify one.
- For `source()` versus `ref()`, compare exact catalog `database`, `schema`, and relation `name`
  values for sources and dbt nodes. An exact match is a candidate for `ref()` because it restores
  lineage and build ordering. Keep `source()` when the relation is an intentionally independently
  deployed contract boundary.

Catalog evidence guides the agent's report; it does not make a static lint finding by itself.

### Step 3 — Run the audit

```bash
uv run audit.py audit <path> --out <scratch>/suggestions.json
```

The analyzer never runs dbt, never connects to a warehouse, and writes nothing inside the audited
project except the suggestions file you name. Put `suggestions.json` in scratch, not in the user's
repo.

If `uv` cannot reach its index (common on configured corporate installs), fall back to:

```bash
UV_DEFAULT_INDEX=https://pypi.org/simple uv run --no-config --no-project \
  --with pyyaml --with typer --with rich python audit.py audit <path> --out <path>
```

### Step 4 — Read the suggestions before writing anything

Open `suggestions.json` and work from `summary`, `remediation` and `suppressed`. `remediation` is
already grouped by rule and ranked by impact over effort — trust that ordering; it is what makes the
report actionable rather than a list.

The summary prints like this:

```text
Projects: 1   Models: 41
Suggestions: 208 — 2 error, 7 warning, 199 information
Severity: 2 critical, 6 high, 111 medium, 89 low
Per model: 5.07
Manifest coverage: 1/1   Rules skipped: 0
```

`per_model` is the number to track across re-audits — raw counts are not comparable across projects
of different sizes. A grade or score is not produced: the engine lacks the context to justify a
verdict on heuristic rules whose applicability only the agent can settle.

Every suggestion carries three independent axes. `kind` says what the rule is — `EWI` (an issue),
`FDM` (a functional difference, where model results diverge from the source system), or `PRF`
(performance or cost). `level` is confidence that something is actually wrong: `error` admits no
legitimate condition, `warning` is a real problem in nearly all cases, `information` (the default)
is context-dependent and states the condition under which the code is already correct. `severity` is
blast radius if the rule is right: `critical`, `high`, `medium` or `low`. Level and severity are
orthogonal — a rule can be `information` level yet `critical` severity, because "likely fine, but
catastrophic if wrong" is a real position. Rule codes (`SSC-EWI-DBTOPS0002` etc.) use SnowConvert's
own `SSC`/`EWI` documentation convention: this project is part of the SnowConvert team in Snowflake
Engineering, adopting those conventions for consistency. Nothing here blocks a save at any level —
gate on errors in CI with `dbt-lint --strict` instead.

Spot-check two or three suggestions against the actual files before reporting them. The analyzer is
text-level by design and can misread unusual formatting. You are the check on that, and a report
containing one obviously wrong suggestion loses the reader's trust in all of them.

### Step 5 — Render the HTML report

Follow `references/report-spec.md` for structure and the sandbox rules. The essentials, because
getting these wrong produces a blank page:

- Self-contained. No CDN, no remote fonts, no remote images, no `fetch`.
- Charts from `/libs/chart.js@4.4.4/chart.umd.js` only.
- No inline event handlers — `addEventListener` inside an inline `<script>`.
- `:root { color-scheme: light dark; }` and `light-dark()` colours, so it is readable in both
  themes.
- Include `<meta name="snowflake-source" content="cortex-agent-authored">` and the
  `snowflake-report-metadata` provenance block.

Save it somewhere durable — the workspace by default, never `/tmp`. Ask if no durable location is
obvious.

### Step 6 — Report and offer next steps

Summarise in two or three sentences: the counts and per-model rate, the single highest-leverage fix,
and anything that was suppressed or skipped. Then offer to fix the top suggestion — most are a few
lines, and a customer who watches one get fixed engages with the rest.

---

## Writing remediation that gets acted on

The analyzer supplies a remediation string per rule. Improve on it with what only you can see:

- **Use their identifiers.** "Add `unique_key='order_line_id'`" beats "add a unique key". Read the
  model and name the real column.
- **Group the work.** 43 models missing a primary-key test is one afternoon, not 43 tickets. Say so,
  and say which layer to start with.
- **Sequence dependent fixes.** Renaming ETL-named models is much cheaper after collapsing
  per-transformation chains, because there are fewer names left to choose. Point that out rather
  than listing both as peers.
- **Say what breaks if ignored.** Not "violates best practice" but "reprocessing duplicates rows
  silently, and no test would catch it".
- **Concede genuine trade-offs.** Some suggestions are defensible choices. A single large project
  may be intentional. Ask rather than assert when the evidence is ambiguous, and record the decision
  so the next audit does not re-raise it.

Do not inflate. If a project is in good shape, say so and keep the report short. An audit that
manufactures concern to look thorough is worse than no audit.

---

## Configuration

`.dbt-quality.yml` at the audit root, all optional — thresholds, `migration.mode` and
`migration.paths`, `disabled_rules`. Full schema in `../../scripts/README.md`.

`disabled_rules` accepts any exact registered rule ID. A disabled rule does not emit a suggestion or
affect lint counts and is reported as skipped with `disabled in .dbt-quality.yml`. Use it for
project-specific exceptions rather than adding inline suppression comments.

**Names are not audited**, and if someone asks why, this is the answer: a model may keep the name
its object had in the source database it was migrated from, and a dbt project records nowhere
machine-readable what that name was. The prescribed `/* Original Object: */` header is a comment
that never reaches `manifest.json`; `meta.original_object` and any crosswalk file do not exist; the
one real source-to-target mapping sits in SnowConvert's external registry and writes nothing back. A
naming rule would be guessing, so there isn't one. Full reasoning in `references/rule-catalog.md`.

---

## References

| File                         | Load when                                                                     |
| ---------------------------- | ----------------------------------------------------------------------------- |
| `references/rule-catalog.md` | A user asks why a rule fired, disputes a suggestion, or you are adding a rule |
| `references/report-spec.md`  | Rendering the HTML report                                                     |
| `../../scripts/README.md`    | Configuring thresholds, or running the analyzer directly                      |

## Related skills

`dbt-architecture`, `dbt-modeling`, `dbt-materializations`, `dbt-testing`, `dbt-performance` state
the practices this audit inverts — cite them when a user wants the positive guidance behind a
suggestion.
