---
name: dbt-audit
description:
  "Audit dbt projects for anti-patterns, produce an HTML quality assessment with prioritized
  remediation, and drive the marker-based fix loop. Use when: reviewing, auditing, assessing,
  grading, or health-checking a dbt project or an estate of projects; asking what is wrong with a
  dbt project or where its technical debt is; finding dbt anti-patterns; evaluating or consolidating
  migrated dbt output (SnowConvert Informatica, SSIS, DataStage); marking findings in the files so
  they can be fixed. Covers project fragmentation, var and parameter misuse, hooks that write,
  truncate/delete-load instead of incremental models, subqueries that should be CTEs or ephemeral
  models, macro over-use and under-use, materialization fitness, test and documentation coverage,
  and unresolved conversion debt. Triggers: audit dbt, dbt audit, review my dbt project, dbt
  quality assessment, dbt anti-patterns, dbt health check, assess dbt project, what is wrong with my
  dbt project, dbt technical debt, consolidate dbt projects, mark dbt findings, SSC-EWI-DBT, too
  many dbt projects, dbt code review."
---

# dbt anti-pattern audit

The Rust analyzer uses dbt's Jinja parser and local SQL analysis to produce JSON findings and an
HTML report. It can also write `SSC-EWI-DBT*` markers into dbt files. It does not execute models or
connect to a warehouse.

Use the findings to plan project-specific fixes. Check the evidence before changing code, test
each fix, and audit again. The same inputs and settings should produce the same findings; an
HTML edit alone does not change those results.

## Tools

Prefer the `dbt-quality` MCP server. It is declared in this plugin's manifest.

| MCP tool   | Use                                                                                                   |
| ---------- | ----------------------------------------------------------------------------------------------------- |
| `report`   | Audit `path`; writes `dbt-audit-suggestions.json` and `dbt-audit-report.html` into `out_dir` (default: a scratch dir under the system temp dir, never the project); returns their paths and counts |
| `findings` | Active findings as JSON, filtered by `rule_ids`, `files`, `min_level`                                  |
| `annotate` | Write markers above each finding. `dry_run: true` (default) returns the diff only. Writes need `dry_run: false` |
| `rules`    | The rule list, or one rule's full record (long description, remediation, examples) with `code`        |
| `version`  | Server version and the pinned dbt commit                                                              |

The same operations are on the CLI: `${CLAUDE_PLUGIN_ROOT}/bin/dbt-quality audit|lint|rules|annotate <path>`.
On Windows, use `bin\dbt-quality.cmd` in an installed plugin or `bin/dbt-quality.exe` in a release archive, with
PowerShell's `&` call operator; resolve the plugin's absolute path before invoking it. Prefer the MCP tools when shell conventions differ.

## Stopping points

- **Before `annotate` with `dry_run: false`:** show the diff from a dry run and get approval. The
  tool refuses to write when the git tree has uncommitted changes (the two report files do not
  count). It writes only files inside `path`. With `rule_ids` it replaces only those rules'
  markers. Never pass `allow_dirty: true`
  unless the user explicitly asks you to.
- **Before writing reports:** use the tool's default scratch directory or a location the user
  approved. Confirm a durable destination before retaining or sharing the report. Do not write
  into the user's repo without asking.
- **Before including model text:** explain that sharing the report shares that source. Set
  `include_models: true` only when the user approves source inclusion; it requires HTML output.
- **Before reporting a suggestion:** spot-check two or three against the actual files.

## Routing

| User intent                                       | Surface                                                     |
| ------------------------------------------------- | ----------------------------------------------------------- |
| "Check this one model"                            | **`dbt-validate` skill**: one file, model-scoped rules      |
| "Populate the Problems panel" / CI gate           | `dbt-quality lint`; `--strict` exits 1 on errors            |
| "Audit my project" / "assess this estate"         | **This skill**: `report`, then the HTML report              |
| "Fix / consolidate these migrated projects"       | **This skill**: the marker loop below                       |

---

## Workflow

### Step 1: Establish scope

Ask what to audit if it is not clear. Use the common estate root when the audit must compare
projects. Discovery looks for `dbt_project.yml` below that root and excludes generated/dependency
directories. A single-project root cannot reveal cross-project collisions. Estate checks include
fragmentation (PRJ0001-0003), conflicting var defaults (PRJ0012), macros copied across projects
(MAC0015/0016), and duplicated logic (MAC0010, SQL0002).

### Step 2: Run the audit

Call `report` with `path`. Omit `out_dir` to use the default scratch directory, or pass a
location the user approved (it can be outside `path`). It returns the paths it wrote,
the counts, and the top remediation items. The analyzer does not run dbt, read `target/manifest.json`, or connect to a warehouse. Graph checks use the `ref()` calls in the model files.
The tool writes JSON and HTML reports; `html:false` omits HTML. Default HTML contains evidence,
not complete model files. Opt in to bounded SQL/Python model snapshots with `include_models: true`;
never combine that option with `html:false`. Normal findings JSON remains unchanged.

### Step 3: Read before writing

Work from `summary`, `remediation` and `suppressed` in the JSON. `remediation` is already grouped
by rule and ranked by impact over effort. Read each finding on three independent axes:

| Axis       | Values                            | Meaning                                                                    |
| ---------- | --------------------------------- | -------------------------------------------------------------------------- |
| `kind`     | `EWI`, `FDM`, `PRF`               | Issue / possible functional difference / performance concern              |
| `level`    | `error`, `warning`, `information` | Diagnostic level; confirm the evidence and conditions before changing code |
| `severity` | `critical`, `high`, `medium`, `low` | Potential impact if the concern applies                                  |

Compare `per_model` across re-audits only when scope, settings, and coverage are comparable. No
grade is produced. HTML labels all-audit counts separately from returned or browser-filtered
findings. Skipped checks and read errors are coverage gaps, not passes.

### Step 4: Review or share the report

`report` writes standalone HTML following [references/report-spec.md](references/report-spec.md).
It has Auto/Light/Dark themes, findings filters, rule detail, and model source panels. The pinned
Chart.js asset needs CDN access; filters and code panels do not need Chart.js. Static findings and
rule text remain readable when JavaScript is blocked. A Snowflake shared-report sandbox or editor
preview may block these assets. Do not promise full interactive support there. Follow the
`html-authoring` skill if adapting HTML for the shared-report sandbox.

The report keeps `snowflake-source` and `snowflake-report-metadata` provenance. Its CSP blocks data
connections and uses script hashes. The CDN library still runs in the page context. Review paths
and evidence before sharing, even when complete model text is not included.

A source panel can show included text or a user-selected local file. A selected file's path is not
proof of identity. Without a matching snapshot hash, confirm its association and label locations
unverified or stale. Source snapshots have limits of 256 KiB/file, 4 MiB total, and 100 files; they
exclude profiles/configuration files, unsafe paths, and unsupported content. These controls do not
sandbox the audit reader.

Edits affect a copy in the report. The reader can preview changes, copy text, or download a new
file; the report never overwrites project files. Mixed or CR-only line endings are read-only.
Use downloads when exact bytes matter, and use manual text copy if clipboard access fails. Apply
changes separately, review the diff, test, then audit again. Do not mark a finding resolved from
a browser edit. There is no live linter, SQL execution, local write server, or WASM validator.

### Step 5: Use markers to fix and consolidate

1. `report` on the root.
2. `annotate` with `dry_run: true`. Show the diff and get approval.
3. `annotate` with `dry_run: false`.
4. For each marker `--** SSC-EWI-DBT<PACK><NNNN> - <name>: <subject> **` (YAML: `# ** … **`),
   call `rules` with that `code` for its remediation and examples. Fix the construct the marker
   sits above. Leave the marker in place. The next `annotate` run removes markers of fixed findings.
5. Test the code changes. Run `report` again, then preview `annotate` again and approve any writes.
   With the same inputs, a second `annotate` changes nothing. `remove: true` removes dbt-quality
   markers in scope. With no intervening edits, removal restores the pre-annotation bytes; it does
   not undo code changes.

Markers carry only dbt-quality codes (`SSC-{EWI|FDM|PRF}-DBT<three letters><four digits>`). The
engine ignores them when it scans, so findings do not change because markers are present.
SnowConvert's own markers, such as `SSC-EWI-DBT0001` or `SSC-EWI-INF0039`, are left alone. MIG0002
and MIG0003 still report them.

Use this order as a starting point for migrated estates, then adjust it to the actual dependencies:

1. Vars and parameters (PRJ0009-0018): verify sentinel defaults and required values before changing load behavior.
2. Hooks that write (INC0001-0003, INC0010, INC0016-0020).
3. Macro duplication across projects (MAC0010, MAC0015-0017).
4. Review project consolidation (PRJ0001-0003, PRJ0006) after confirming ownership and deployment boundaries.

---

## Write actionable remediation

- Use actual identifiers, such as `unique_key='order_line_id'`, once you have confirmed the key.
- Group findings that share a fix; several models missing a key test may be one piece of work.
- Sequence dependent fixes and explain those dependencies.
- State a supported consequence, such as duplicate rows on reprocessing, rather than "violates best practice".
- Record accepted trade-offs with narrow waivers and their reasons.

Keep the summary proportional to the findings and coverage. Do not inflate either the risks or
the confidence of a clean result.

## Lift-and-shift tiers

Migration detection does not suppress `universal` or `migration` rules. `architecture` findings
can be suppressed for detected converted code and are counted separately for later review.
Suppression is a scope policy, not proof that the code is correct. Disabled rules and waivers
still apply. If the user disputes the classification, show `projects[].provenance.signals` and
offer `.dbt-quality.yml` (`migration.mode: native | lift_and_shift`, `migration.paths`).

## Configuration and waivers

`.dbt-quality.yml`, found by walking up from the audit root: `thresholds`, `migration`,
`disabled_rules`, `ignore`. Inline waivers are `-- dbt-quality: ignore <codes>` on the reported line
or the line above, and `-- dbt-quality: ignore-file <codes>`. Prefer the narrowest waiver.

## Output

Return the report paths, scope, coverage gaps, and a short list of fixes supported by the evidence.
State whether complete model text was included and whether the output is temporary. Do not claim
that edits are validated until the project's checks and a fresh audit have run.

## References

| File                                                     | Load when                                                       |
| -------------------------------------------------------- | --------------------------------------------------------------- |
| [references/rule-catalog.md](references/rule-catalog.md) | A user asks why a rule fired, disputes a finding, or adds a rule |
| [references/report-spec.md](references/report-spec.md)   | Authoring or reviewing the HTML report                          |
