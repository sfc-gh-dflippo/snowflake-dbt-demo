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

Produces a dbt quality assessment: a deterministic Python analyzer emits findings as JSON, then you
render an HTML report with prioritised remediation.

The split is deliberate. Scores and findings must be reproducible run to run, so a customer can
re-audit after a sprint and see movement — that is the analyzer's job. The remediation narrative has
to reflect _this_ project, so it is yours.

---

## What this audits

Ten rule packs. Run `rules` to list the current catalogue with tiers and severities.

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
finding.

---

## Lift-and-shift is scored differently — read this before reporting

Rules carry a tier, and the engine suppresses one of them for converted projects:

- **UNIVERSAL** — always applies. A truncate-and-load is wrong whether a person wrote it or a
  converter emitted it.
- **ARCHITECTURE** — medallion folders, layer naming, layer-crossing lineage. **Suppressed** when
  the project is detected as mechanically converted from Informatica or SSIS. That layout was never
  the customer's choice, and burying real findings under naming violations on generated code makes
  the report useless.
- **MIGRATION** — fires _because_ the code was converted: unresolved `SSC-EWI`/`SSC-FDM` markers,
  ETL control columns, shipped scaffolding. Never suppressed.

Two things to hold onto when you write the report:

1. **Suppression is not absolution.** Detecting that code was machine-generated excuses it from
   architectural expectations, not from defects. Converter output routinely contains genuine
   anti-patterns — a project per data flow, `DELETE FROM {{ this }}` in a `pre_hook`, folder hooks
   that truncate once per model, per-transformation model chains. Report all of those.
2. **Say what was suppressed.** The report must state the count and the reason, so nobody reads a
   good grade as "no architectural debt". Present it as a modernisation opportunity, separate from
   the defect list.

Provenance detection is automatic and evidence-based. If the user disputes the classification, show
them `projects[].provenance.signals` from the JSON and offer `.dbt-audit.yml`
(`migration.mode: native | lift_and_shift`, `migration.paths`).

---

## Workflow

### Step 1 — Establish scope

Ask what to audit if it is not already clear, and remember tree mode exists: pointing at a parent
directory discovers every `dbt_project.yml` beneath it. That is the only way the fragmentation
findings can fire, so prefer the estate root over a single project when the user has more than one.

### Step 2 — Check the manifest, then offer `dbt parse`

```bash
cd .claude/skills/dbt-audit/scripts
uv run audit.py manifest-status <path>
```

Several of the highest-value checks need `target/manifest.json`: ephemeral fan-out, pass-through
model chains, layer-crossing dependencies, single-consumer models. Without it they are reported as
**skipped**, never as passing.

If the command reports projects needing a parse, **ask the user before running it** via
`ask_user_question`. Give them the trade-off plainly: `dbt parse` executes no models and uses no
warehouse compute, but it needs a working profile and it writes to `target/`. Offer three options —
run it now, audit without the graph checks, or they will run it themselves.

Never run `dbt parse` unprompted. It writes inside their project.

### Step 3 — Run the audit

```bash
uv run audit.py audit <path> --out <scratch>/findings.json
```

The analyzer never runs dbt, never connects to a warehouse, and writes nothing inside the audited
project except the findings file you name. Put `findings.json` in scratch, not in the user's repo.

If `uv` cannot reach its index (common on configured corporate installs), fall back to:

```bash
UV_DEFAULT_INDEX=https://pypi.org/simple uv run --no-config --no-project \
  --with pyyaml --with typer --with rich python audit.py audit <path> --out <path>
```

### Step 4 — Read the findings before writing anything

Open `findings.json` and work from `summary`, `remediation` and `suppressed`. `remediation` is
already grouped by rule and ranked by impact over effort — trust that ordering; it is what makes the
report actionable rather than a list.

Spot-check two or three findings against the actual files before reporting them. The analyzer is
text-level by design and can misread unusual formatting. You are the check on that, and a report
containing one obviously wrong finding loses the reader's trust in all of them.

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

Summarise in two or three sentences: the grade, the single highest-leverage fix, and anything that
was suppressed or skipped. Then offer to fix the top finding — most are a few lines, and a customer
who watches one get fixed engages with the rest.

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
- **Concede genuine trade-offs.** Some findings are defensible choices. A single large project may
  be intentional. Ask rather than assert when the evidence is ambiguous, and record the decision so
  the next audit does not re-raise it.

Do not inflate. If a project is in good shape, say so and keep the report short. An audit that
manufactures concern to look thorough is worse than no audit.

---

## Configuration

`.dbt-audit.yml` at the audit root, all optional — thresholds, `migration.mode` and
`migration.paths`, `naming.mode`, `disabled_rules`. Full schema in `scripts/README.md`.

`naming.mode` defaults to `auto` on purpose. This repo's own guidance conflicts: `dbt-architecture`
mandates `stg_`/`dim_`/`fct_` prefixes while `dbt-modeling`'s Name-Retention Policy forbids them in
favour of original source object names. `auto` infers the project's dominant convention and flags
deviation from that, rather than picking a side and generating noise for whichever the customer
chose.

---

## References

| File                         | Load when                                                                  |
| ---------------------------- | -------------------------------------------------------------------------- |
| `references/rule-catalog.md` | A user asks why a rule fired, disputes a finding, or you are adding a rule |
| `references/report-spec.md`  | Rendering the HTML report                                                  |
| `scripts/README.md`          | Configuring thresholds, or running the analyzer directly                   |

## Related skills

`dbt-architecture`, `dbt-modeling`, `dbt-materializations`, `dbt-testing`, `dbt-performance` state
the practices this audit inverts — cite them when a user wants the positive guidance behind a
finding.
