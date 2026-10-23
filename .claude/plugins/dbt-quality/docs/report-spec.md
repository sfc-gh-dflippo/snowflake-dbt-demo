# HTML report specification

This spec describes the standalone HTML export from dbt-quality. It covers the report layout,
source controls, and safety requirements. A saved report is an audit snapshot. It does not run
SQL, execute dbt, or validate edits.

## Standalone and shared-report surfaces

The standalone report opens in a browser from a file URL or a static HTTP origin. Local CSS,
JavaScript, and report data are embedded in the document. Chart.js loads from the exact CDN asset
below; no other runtime library, font, image, or data service is needed.

| Asset | Pin |
| --- | --- |
| Library | Chart.js 4.4.4, MIT license |
| URL | `https://cdn.jsdelivr.net/npm/chart.js@4.4.4/dist/chart.umd.js` |
| Integrity | `sha384-G436+Z2nlA8+PNoeRvWdxKbvOf8E/y+lYxqht2iBwNHTQDV5CJr3+AGVj8fGZi5t` |
| Cross-origin mode | `anonymous` |

Charts need CDN access. Filters and code panels use the embedded script and must work without
Chart.js. If JavaScript is blocked, keep the server-rendered findings, rule guidance, and chart
table readable. Show a notice that explains which controls are unavailable.

Snowflake's shared-report sandbox is a different surface. Its CSP may reject CDN imports or
scripts, and its supported library paths are not the standalone CDN URL. Follow the
`html-authoring` skill when adapting a report for that sandbox. Do not promise full interactive
support there or in an editor preview. Do not weaken the standalone CSP to work around a preview.

## Data and script safety

- Embed report data as escaped JSON. Escape HTML-sensitive characters, including closing script
  tags. Render model text, paths, evidence, and labels as text, never executable HTML.
- Use event listeners, not inline event-handler attributes. Do not use `eval`, `new Function`,
  executable templates, or model content as JavaScript.
- Hash the exact local script bytes in the CSP. Do not allow `unsafe-inline` scripts or
  `unsafe-eval`. Set `base-uri 'none'` and block script attributes.
- Deny data connections, form submission, frames, and objects. Do not use `fetch`,
  `XMLHttpRequest`, or `WebSocket` for report or model data. Blob URLs are for downloads only.
- Set a no-referrer policy. Permit only the pinned chart asset and the required local code/styles.
  SRI checks the library's bytes; it does not isolate that library from embedded page data.
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
counts by diagnostic level (`error`, `warning`, `information`) and impact severity (`critical`,
`high`, `medium`, `low`). These are separate fields; show both labels, not color alone.

Use a category chart with a table fallback. Keep the chart responsive within its container and
legible at narrow widths. Use theme tokens for chart text and colors. Do not impose a fixed canvas
width that overflows the page. Additional charts are optional if they help a reader choose work.

Show priority fixes from `remediation` in its given order. Each item needs its rule ID, affected
count, effort, rationale, remediation, and one concrete file/line/evidence example. Preserve code
blocks. Make long file lists expandable. Priority is a starting point for review, not a promise
that the highest-ranked change is safe or beneficial in every project.

For multiple projects, show names, paths, model counts, provenance, and per-project tallies.
If consolidation rules fire, explain the specific duplication or boundary concern. Separate
project boundaries may be intentional. Do not claim consolidation is always the largest benefit.

### Findings and rule detail

Provide search and project, pack, level, and severity filters. Provide stable sorting, a reset
control, matched/total counts, and an empty-result state. Bound the number of rendered rows with
paging or an equivalent limit. Active findings are the default; keep suppressed findings separate.

A selected finding shows its file, line, optional column, evidence, and diagnostic text. Include
the rule rationale, remediation, examples, and verified reference links. A rule explains a
pattern; confirm the finding against the project before applying that guidance. Treat local
thresholds and migration conventions as local policy, not upstream requirements.

### Models

Show a model's path and source status, line numbers, the selected finding, and relevant rule
guidance. Highlight a finding line as verified only when source alignment is verified. Stale or
unverified text needs a visible warning; do not present its line as confirmed.

Default reports contain evidence, not complete model files. Offer local file selection only for
findings linked to an exact discovered model. Other findings remain evidence-only. A file picker
cannot prove the original path of a selected file. Compare its bytes with the snapshot hash when
one is available. Otherwise require explicit association confirmation and label it unverified.
A mismatch must show stale locations.

`--include-models` on CLI `audit` and `include_models: true` on MCP `report` opt in to source
snapshots. CLI use requires `--html`; MCP use requires HTML to remain enabled. Source text belongs
only in the HTML payload, not in normal findings JSON or default MCP responses. Warn that sharing
the HTML shares the included source text.

Collect only exact discovered SQL/Python models. Require regular files inside both the canonical
audit and project roots. Reject ambiguous ownership, symlinks in any path component, unsupported
extensions, profiles/configuration files, binary-like bytes, and invalid UTF-8. Limits are:

| Limit | Value |
| --- | ---: |
| Source bytes per file | 256 KiB |
| Total included source bytes | 4 MiB |
| Included model files | 100 |

Use a bounded read before decoding. Record omissions with a reason; never silently truncate
editable source. These controls protect source snapshots, not the audit's existing file reader.
Store each source once under its stable project/file identity, not under an ambiguous basename.
Retain original markers, encoding/BOM, line endings, final-newline state, and a hash of the bytes.
Verify alignment against the audited text after blanking owned markers. If the file changed
between audit and collection, mark its source stale.

Local file selection uses a bounded byte read and the same encoding checks. Feature-detect browser
picker APIs and retain a normal file-input fallback. Handle cancel, denied access, unavailable
source, and unsupported browser features without discarding the current source or edits.

Let the reader edit a copy, preview changes, copy text, and download a new file. Bound change-preview
work. Preserve UTF-8, BOM, and LF/CRLF on export. Mixed and CR-only line endings remain read-only;
explain the restriction rather than normalize them silently. Clipboard text is not a byte-preserving
file export. Provide a download and manual copy fallback when clipboard access is unavailable.

Show unsaved state. Confirm before an in-report switch or reset discards edits. Do not promise
reliable tab-close protection. Never overwrite the original project file or offer a Save-to-project
action. The browser cannot enforce the linter's clean-Git-tree safeguard. Tell the reader to apply
the edit, test it, and run the audit again. Do not mark findings resolved after an unverified edit.

### Suppressed findings, skipped checks, and errors

List suppressed architecture findings with their recorded reasons and counts. They remain review
items, but are excluded from active defaults and the active `per_model` rate. Suppression is not
proof that the code is correct, nor is it a reason to label converted code defective.

For `skipped_checks`, show each rule and why it could not run. A rule disabled in
`.dbt-quality.yml` needs that setting reviewed. A detector failure is a tool defect to report.
The audit never needs a manifest or `dbt parse`. List read/parse errors as coverage gaps.

## Themes and access

Provide Auto, Light, and Dark controls. Auto follows the browser color preference. Use complete
theme tokens for text, surfaces, inputs, badges, code, charts, menus, and focus states. Manual
controls need JavaScript; static content must remain readable without it. Do not depend on
storage permission for theme selection.

Use compact navigation at narrow widths. Keep long paths and code inside their containers. Support
keyboard navigation, visible focus, accessible labels, live result counts, Escape to close a panel,
and focus return to its opener. Respect reduced-motion preferences. Do not identify severity by
color alone.

## Sample and verification

The README links to `sample-report.html`, generated from the tracked synthetic `ewi_estate` fixture.
Regenerate it from the repository root:

```bash
cargo run --locked --manifest-path ai/Cargo.toml -p dbt-quality-core --example sample_report
```

Append `-- --check` to check drift without rewriting the sample. Never hand-edit generated HTML.
The sample does not claim all-rule coverage. Its sources must exclude profiles and configuration
files, and its provenance must not expose machine-specific absolute paths.

Test the report in real browsers from file URLs and static HTTP, including no-JavaScript,
CDN-blocked, and failed-integrity cases. Check light/dark themes, keyboard use, narrow layouts,
source selection, stale-file warnings, edit downloads, and exact exported bytes. Confirm that
report/model data cause no external network requests. Native tests alone do not verify these
browser behaviors.

## Writing style

Lead with the action and its condition. Use short sentences, active voice, and consistent terms.
Apply humanizer and ASD-STE100 principles without claiming certified compliance. Preserve exact
identifiers and executable examples. Quote evidence. State consequences only when the evidence
supports them, and explain valid exceptions. A successful build does not prove all business logic.
