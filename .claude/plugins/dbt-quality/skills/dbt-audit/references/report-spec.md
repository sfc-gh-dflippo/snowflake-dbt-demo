# HTML Report Specification

Structure and constraints for the dbt quality assessment. Read alongside the `html-authoring` skill,
which is authoritative on the sandbox.

## Hard constraints

Snowflake renders shared reports in a locked-down sandbox with a strict CSP and no network access.
Violating any of these produces a blank section, not an error:

- **No CDN, no remote fonts, no remote images.** Everything inline or from `/libs/`.
- **No inline event handlers.** No `onclick=`; attach with `addEventListener` inside an inline
  `<script>`.
- **No `fetch` / `XMLHttpRequest` / `WebSocket`.** All data embedded in the HTML.
- **No `eval` / `new Function`.**
- **No `localStorage` / cookies / `<iframe>` / `<form>` submission.**
- **Charts from `/libs/chart.js@4.4.4/chart.umd.js`** — the pinned path, nothing else.
- **Theme-adaptive colours.** `:root { color-scheme: light dark; }` plus `light-dark(...)`. A
  hard-coded light background with dark text is unreadable in dark mode.

Required in `<head>`:

```html
<meta name="snowflake-source" content="cortex-agent-authored" />
```

Plus a `snowflake-report-metadata` JSON block recording the audit root, the analyzer command, and
one `sections[]` entry per anchor id, so a later run can refresh the report.

Save to a durable location — the workspace by default. Never `/tmp`.

## Sections

Ordered so a reader who stops after the first screen still has the important part.

### 1. Header and summary

Project count, model count, and suggestion counts by level (`error`, `warning`, `information`) and
by severity (`critical`, `high`, `medium`, `low`) from `summary.counts`. Show `summary.per_model`
(suggestions per model) prominently alongside the counts — raw counts are not comparable across
projects of different sizes. Use `metric_card`-style tiles or a simple flex row of large numbers.

State the audit scope and date. If manifest coverage is partial, say so here rather than only in the
appendix — it qualifies everything below.

### 2. Category breakdown

Horizontal bar chart of per-category suggestion counts from `summary.categories`, plus a table with
`error`/`warning`/`information` counts per category. Sort by `error` count descending so the
category with the most urgent items leads.

### 3. Portfolio view — only when `summary.project_count > 1`

One row per project: name, path, model count, and whether provenance detected a migration.
Per-project suggestion counts are in `projects[].tally`. Call out micro-projects (PRJ001)
explicitly, and if PRJ002 or PRJ006 fired, describe the consolidation opportunity in prose — it is
usually the single largest structural improvement available and deserves more than a table row.

Omit this section entirely for a single project. Do not render an empty shell.

### 4. Prioritised remediation

The centre of the report. Iterate `remediation` in the order given — already ranked by impact over
effort — and render each entry as a card with:

- Rule ID, title, level and severity badges, affected count, effort

Each remediation and each suggestion renders both axes as badges: a level badge (`error` / `warning`
/ `information`) and a severity badge (`critical` / `high` / `medium` / `low`). Show both — they are
independent and a reader needs each to triage.

- The rationale (why this matters, from `rationale`)
- The remediation, rendered as markdown with fenced code blocks intact
- One concrete example: file, line, and the evidence string
- Affected files, collapsed behind a `<details>` when more than about five

Lead with the top five. Anything below that can sit in a lower-density list.

### 5. Suggestions by category

Grouped tables, one per category, from `suggestions`. Columns: kind, level, severity, rule, file,
line, message. Use `<details>` per category so the page opens readable rather than as a wall of
rows. Every suggestion carries a `line` number; render it as a link or plain text alongside the file
path. A `column` offset is present when the rule matched a precise character position.

Escape file paths and evidence — evidence is raw SQL and will contain `<`, `>` and `&`.

### 6. Suppressed suggestions — only when `suppressed.count > 0`

Its own section, clearly framed. State the count, the reason from `suppressed.reason`, and reproduce
`suppressed.note`.

Frame these as a modernisation opportunity, not a defect list: they are architectural expectations
that mechanically converted code never adopted, and they are excluded from the `per_model` rate. Do
not bury this section, and do not present it as failure — the point is that the team did not
introduce these.

### 7. Appendix: skipped checks

From `skipped_checks`. Name each rule and why it could not run, and give the exact command that
would enable it (`dbt parse` in the named project).

This section is not optional when anything was skipped. "We could not check X" and "X is clean" are
different claims, and conflating them overstates the project's health.

Also list `errors` here if non-empty — files that could not be parsed are gaps in coverage.

## Chart guidance

Keep it to two or three charts. This is a report to act on, not a dashboard.

- **Category suggestion counts** — horizontal bar, most useful single chart.
- **Level and severity mix** — doughnut(s), only if there is a meaningful spread.
- **Suggestions per project** — stacked bar, only in tree mode with 3+ projects.

Set `options: { responsive: false }` with explicit `width`/`height` on the canvas. Pull colours from
the chart palette rather than hard-coding, and ensure they are distinguishable in both themes.

## Tone

- Lead with what to fix, not with how much is wrong.
- Quote evidence rather than paraphrasing it. A reader who can see the offending line does not have
  to trust the tool.
- State consequence, not compliance: "reprocessing silently duplicates rows" rather than "violates
  best practice".
- Where a suggestion is a defensible trade-off, say so. Credibility across the whole report depends
  on not overstating any single item.
- If the project is in good shape, keep the report short and say that.
