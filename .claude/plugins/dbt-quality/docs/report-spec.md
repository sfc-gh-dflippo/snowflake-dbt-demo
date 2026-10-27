# HTML report specification

This spec describes the standalone HTML export from dbt-quality. It covers the report layout,
source controls, and safety requirements. A saved report is an audit snapshot. It does not run
SQL, execute dbt, or validate edits.

## Standalone and shared-report surfaces

The standalone report opens in a browser from a file URL or a static HTTP origin. Local CSS,
JavaScript, and report data are embedded in the document. The page loads no remote script, style,
font, image or data service, so a network-blocked or script-restricted surface can still show it.

Filters, decisions and the source viewer use the embedded script. If JavaScript is blocked, keep
the server-rendered overview, category bars and table, column summary, skipped checks, and rule
reference readable. Show a notice that explains which controls are unavailable. The rule headings
and counts under Findings stay visible; the message groups under them need the script.

Snowflake's shared-report sandbox is a different surface. Follow the `html-authoring` skill when
adapting a report for that sandbox. Do not promise full interactive support there or in an editor
preview. Do not weaken the standalone CSP to work around a preview.

## Data and script safety

- Embed report data as escaped JSON. Escape HTML-sensitive characters, including closing script
  tags. Render model text, paths, evidence, and labels as text, never executable HTML.
- Use event listeners, not inline event-handler attributes. Do not use `eval`, `new Function`,
  executable templates, or model content as JavaScript.
- Hash the exact local script bytes in the CSP. Do not allow `unsafe-inline` scripts or
  `unsafe-eval`. Set `base-uri 'none'` and block script attributes.
- Deny data connections, form submission, frames, and objects. Do not use `fetch`,
  `XMLHttpRequest`, or `WebSocket` for report or model data. Blob URLs are for downloads only.
- Set a no-referrer policy. Permit only the hashed local script and inline styles. Load nothing
  from a remote origin.
- Accept safe absolute HTTPS reference URLs. Reject credentials, controls, whitespace, malformed
  escapes, backslashes, and unsafe schemes. Escape link labels and attributes separately.
  References are user-initiated navigation, not background requests.
- Do not upload source, reports, or selected files. Do not add a local write server.

Keep the provenance tag in `<head>`:

```html
<meta name="snowflake-source" content="cortex-agent-authored" />
```

Keep a `snowflake-report-metadata` JSON block with the audit root, analyzer command, and a
`sections[]` entry for each report anchor. The deterministic sample uses relative paths and a
fixed date. Normal reports retain their real audit provenance.

Use the report tool's scratch directory when no durable output location is approved. Before
sharing or retaining a report, agree on a destination and review its content. Even evidence-only
reports can contain sensitive paths and SQL. Including model text increases that exposure.

## Counts and coverage

Show audit-wide totals separately from the findings returned after generation filters and those
matched by browser filters. The HTML payload records the applied categories and minimum level;
do not infer those settings from the returned findings. Show active and suppressed counts
separately. Changing a browser filter must not change the reported audit-wide totals.

Show `summary.per_model` with the scope it describes. This is an active finding rate, not a grade
or proof of correctness. Skipped checks and read errors qualify the
results. State coverage gaps near the summary, not only at the end of the report.

## Report views

### Overview

Show the audit scope and date, project/model counts, active findings, and coverage status. Show
counts by diagnostic level (`error`, `warning`, `information`). Impact severity (`critical`,
`high`, `medium`, `low`) stays in the findings JSON; the grouped report orders and filters by level.

Show seven tiles: Projects, Models, Active findings, Errors, Warnings, Information and Not
reported. Draw the category breakdown as server-rendered stacked bars (error, warning,
information) with the exact values in a table. Set each bar width as an inline percentage; use no
chart library. Use the Okabe-Ito level colors: error `#D55E00` with a striped pattern, warning
`#E69F00`, information `#56B4E9`. A level badge always shows its name as text.

The report has no Projects table and no Top findings list. The grouped Findings view covers
both: a finding that fires in more than `group_threshold` projects appears once, with its project
list. Separate project boundaries may be intentional; do not claim consolidation is always the
largest benefit.

### Findings and rule detail

Section order: overview, categories, findings, columns, suppressed, checks, rules.

Group active findings by rule, then by message template, then by file. Replace the quoted names
and numbers of a message with `...` and `N`, and keep the replaced values as the detail of each
line. Cap a detail at 160 characters. Show the rule with its level, count and remediation. Build
the message groups when the reader opens the rule, and the file list when the reader opens the
message. Provide search (rule, message, file path), category and level filters at group level, a
reset control, a matched count, and an empty-result state. Render at most 500 files at once and
offer a control for the rest. Keep suppressed findings in their own section.

The data block holds interned tables: `folders` (project roots), `labels` (project names),
`rules` (title, level, category, remediation), `groups` and `suppressed`. A group is
`[rule, template, rows]`; a row is `[folder, file, [[line, detail?], ...]]`. A portfolio row is
`[-1, "", [[0, detail?]], [folder, ...]]`. The findings JSON is not changed.

The rule reference states the rationale, remediation, examples and verified reference links. A
rule explains a pattern; confirm the finding against the project before applying that guidance.
Treat local thresholds and migration conventions as local policy, not upstream requirements.

Decisions (*Will address*, *Ignore once*, *Ignore permanently*) apply to a rule, a message group
or a file. The most specific decision wins; *No decision* inside a wider decision clears it for
that scope. Store decisions by a key built from the rule, the message template and the file path.
The export expands every decision to one item per finding.

### Column contract

Show the `COL` findings as a summary only: counts per rule (with distinct models, DDL tables and
projects) and the most common type mismatches. Write every column finding to `column_issues.csv`
(`project, model, file, line, column, model_type, ddl_type, rule, message`) next to the HTML
report, or to the path given with `--column-csv`. The CSV lists each model's findings, even when
portfolio grouping merged them in the findings JSON.

### Models

Default reports contain evidence, not model files. `--include-models` on CLI `audit` and
`include_models: true` on MCP `report` opt in to source snapshots. CLI use requires `--html`; MCP
use requires HTML to remain enabled. Source text belongs only in the HTML payload, not in normal
findings JSON or default MCP responses. Warn that sharing the HTML shares the included source text.

When the report includes a file, show a **Source** button on that file's entry. It opens the file
below the entry, 400 lines at a time, with the finding lines marked. Mark a line as verified only
when source alignment is verified; otherwise say the line numbers are unverified. Without
`--include-models` there is no source viewer, no file picker and no editing.

Collect only exact discovered SQL/Python models. Require regular files inside both the canonical
audit and project roots. Reject ambiguous ownership, symlinks in any path component, unsupported
extensions, profiles/configuration files, binary-like bytes, and invalid UTF-8. Limits are:

| Limit | Value |
| --- | ---: |
| Source bytes per file | 256 KiB |
| Total included source bytes | 4 MiB |
| Included model files | 100 |

Use a bounded read before decoding. Record omissions with a reason; never silently truncate
source. These controls protect source snapshots, not the audit's existing file reader. Store each
source once under its stable project/file identity, not under an ambiguous basename. Retain
original markers, encoding/BOM, line endings, final-newline state, and a hash of the bytes. Verify
alignment against the audited text after blanking owned markers. If the file changed between audit
and collection, mark its source stale. Never overwrite the original project file or offer a
Save-to-project action. Tell the reader to apply the edit, test it, and run the audit again.

### Suppressed findings, skipped checks, and errors

List suppressed architecture findings with their recorded reasons and counts. They remain review
items, but are excluded from active defaults and the active `per_model` rate. Suppression is not
proof that the code is correct, nor is it a reason to label converted code defective.

For `skipped_checks`, show each rule and why it could not run. A rule disabled in
`.dbt-quality.yml` needs that setting reviewed. A detector failure is a tool defect to report.
The audit never needs a manifest or `dbt parse`. List read/parse errors as coverage gaps.

## Themes and access

Provide Auto, Light, and Dark controls. Auto follows the browser color preference. Use complete
theme tokens for text, surfaces, inputs, badges, code, bars, menus, and focus states. Set explicit
surface and background colors with `light-dark()`. Manual
controls need JavaScript; static content must remain readable without it. Do not depend on
storage permission for theme selection.

Use compact navigation at narrow widths. Keep long paths and code inside their containers. Support
keyboard navigation, visible focus, accessible labels and live result counts. Respect
reduced-motion preferences. Do not identify severity by color alone.

## Sample and verification

The README links to `sample-report.html`, generated from the tracked synthetic `ewi_estate` fixture.
Regenerate it from the repository root:

```bash
cargo run --locked --manifest-path ai/Cargo.toml -p dbt-quality-core --example sample_report
```

Append `-- --check` to check drift without rewriting the sample. Never hand-edit generated HTML.
The sample does not claim all-rule coverage. Its sources must exclude profiles and configuration
files, and its provenance must not expose machine-specific absolute paths.

Test the report in real browsers from file URLs and static HTTP, including no-JavaScript
cases. Check light/dark themes, keyboard use, narrow layouts, and the source viewer. Confirm that
report/model data cause no external network requests. Native tests alone do not verify these
browser behaviors.

## Writing style

Lead with the action and its condition. Use short sentences, active voice, and consistent terms.
Apply humanizer and ASD-STE100 principles without claiming certified compliance. Preserve exact
identifiers and executable examples. Quote evidence. State consequences only when the evidence
supports them, and explain valid exceptions. A successful build does not prove all business logic.
