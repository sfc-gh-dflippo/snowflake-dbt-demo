---
name: dbt-quality
description: "Static quality checks for dbt projects with the dbt-quality MCP server and CLI (no dbt runs, no warehouse). Use whenever a user wants to audit, review, or health-check a dbt project or estate, get an HTML quality report, lint or validate a model, understand an SSC-EWI-DBT* finding, mark findings in the files, or check model columns against scai DDL, including SnowConvert-migrated dbt. Not for converting or repointing dbt to Snowflake. Triggers: audit dbt, dbt quality, dbt anti-patterns, review dbt project, validate dbt model, lint dbt, SSC-EWI-DBT, fix-columns."
---

# dbt quality

The Rust analyzer uses dbt's Jinja parser and local SQL analysis to produce JSON findings and an
HTML report. It can also write `SSC-EWI-DBT*` markers into dbt files. It does not execute models or
connect to a warehouse.

Use the findings to plan project-specific fixes. Check the evidence before changing code, test
each fix, and audit again. The same inputs and settings should produce the same findings; an
HTML edit alone does not change those results.

The tool decides what a finding is. Report what `report`, `findings`, `lint` or `validate` returned,
and get a rule's explanation and remediation from `rules` with its `code`. Do not apply the rules
by reading the code yourself, and do not report a finding the tool did not return.

## Tools

Prefer the `dbt-quality` MCP server. It is declared in this plugin's manifest.

| MCP tool   | Use                                                                                                   |
| ---------- | ----------------------------------------------------------------------------------------------------- |
| `report`   | Audit `path`; writes `dbt-audit-suggestions.json` and `dbt-audit-report.html` into `out_dir` (default: a durable per-user folder, `<user data dir>/dbt-quality/reports/<hash>/<timestamp>/`, never the project and never the temp dir; `background: true` returns a `job_id` for `report_status`); returns their paths, counts and `inputs` |
| `report_status` | State of a `report` job started with `background: true`: `running`, `done` (with the result) or `failed`; takes `job_id` |
| `findings` | Active findings as JSON, filtered by `rule_ids`, `files`, `min_level`                                  |
| `annotate` | Write markers above each finding. `dry_run: true` (default) returns the diff only. Writes need `dry_run: false` |
| `fix_columns` | Cast model output columns to the types and collations in scai DDL (`ddl` paths). `dry_run: true` (default) returns the diff only |
| `rules`    | The rule list, or one rule's full record (long description, remediation, examples) with `code`        |
| `version`  | Server version, the pinned dbt version and commit, and the rule count                                 |

The same operations are on the CLI: `${CLAUDE_PLUGIN_ROOT}/bin/dbt-quality audit|lint|validate|rules|annotate|fix-columns <path>`.
On Windows, use `bin\dbt-quality.cmd` in an installed plugin or `bin/dbt-quality.exe` in a release archive, with
PowerShell's `&` call operator; resolve the plugin's absolute path before invoking it. Prefer the MCP tools when shell conventions differ.

## Stopping points

- **Before `annotate` or `fix_columns` with `dry_run: false`:** show the diff from a dry run and get
  approval. Both refuse to write when the git tree has uncommitted changes (the two report files do
  not count). `annotate` writes only files inside `path`. In a migration project, `fix_columns`
  writes the dbt projects in scope (those under `path`, or all with `estate: true`): show the
  user which projects its diff touches, and get approval for all of them, before writing. Pass
  `select` (globs on the model path relative to the migration root) to limit it. With `rule_ids`, `annotate` replaces only those
  rules' markers. Pass `allow_dirty: true` only when the user explicitly asks; it bypasses the clean
  tree that makes the change reviewable and reversible.
- **Before writing reports:** use the tool's default report directory (durable, per user) or a location the user
  approved. Confirm a durable destination before retaining or sharing the report. Do not write
  into the user's repo without asking.
- **Before including model text:** explain that sharing the report shares that source. Set
  `include_models: true` only when the user approves source inclusion; it requires HTML output.
- **Before reporting a suggestion:** spot-check two or three against the actual files.
- **Before `setup-tasks`:** ask before it writes `.vscode/tasks.json`, unless the user already
  asked for editor setup.
- **Before changing model code or adding a waiver:** get approval. A finding is evidence to review,
  not permission to rewrite the model.

## Routing

| User intent                                       | Surface                                                     |
| ------------------------------------------------- | ----------------------------------------------------------- |
| "Check this one model"                            | [Validate one file](#validate-one-file): model-scoped rules |
| "Populate the Problems panel" / CI gate           | `dbt-quality lint`; `--strict` exits 1 on errors; [editor tasks](#editor-tasks) |
| "Why did this fire?" / "What does this code mean?" | `rules` with the finding's `code`                          |
| "Audit my project" / "assess this estate"         | The workflow below: `report`, then the HTML report          |
| "Fix / consolidate these migrated projects"       | The marker loop below                                       |
| "Do the model columns match the converted tables" | Step 6: `fix_columns` with scai `ddl` paths (COL rules) |
| "Which rules should we enforce?" / tune `.dbt-quality.yml` | The `dbt-standards` skill of the `snowflake-migration` plugin |

---

## Workflow

### Step 1: Establish scope

Ask what to audit if it is not clear. Use the common estate root when the audit must compare
projects. Discovery looks for `dbt_project.yml` below that root and excludes generated/dependency
directories. A single-project root cannot reveal cross-project collisions. Estate checks include
fragmentation (PRJ0001-0003), conflicting var defaults (PRJ0012), macros copied across projects
(MAC0015/0016), and duplicated logic (MAC0010, SQL0002).

### Step 2: Run the audit

In a migration project (a `.scai/config/project.yml` at or above `path`), pass any path inside it
and nothing else: `report`, `findings` and `fix_columns` audit the dbt projects under `path` (the
whole registry when `path` is the migration root, or when you pass `estate: true`), and take the
converted table DDL the registry lists, the `snow:` bindings and the project's
`.dbt-quality.yml`. `ddl`, `projects`, `bindings` and `config` only add to those. Outside a
migration project they are the only inputs. Tell the user every line in `inputs.gaps`: each one is
a project, table or binding the run could not use, so a check did not run.
Also tell the user what `inputs.skipped` lists (build output under `bin/` and `obj/`, stabilization
backups, `.dbtignore`, `exclude_paths`): those folders are skipped on purpose and are not gaps.
`exclude_paths`, `include_backups` and `.dbtignore` change that; `exclude_dirs` adds to the defaults.

A `missing_dbt_project` gap, an "unregistered project" gap, or a non-zero `inputs.registry_check` means the registry and the dbt folders disagree: a unit targets a folder that is gone, or a project exists that no unit targets (it is not audited). Do not treat these as audit noise. Follow [registry-consolidation](references/registry-consolidation.md).

Call `report` with `path`. Omit `out_dir` to use the default durable report directory, or pass a
location the user approved (it can be outside `path`). It returns the paths it wrote,
the counts, and the top remediation items. Graph checks use the `ref()` calls in the model files;
`target/manifest.json` is not read.
The tool writes JSON and HTML reports; `html:false` omits HTML. Default HTML contains evidence,
not complete model files. Opt in to bounded SQL/Python model snapshots with `include_models: true`;
never combine that option with `html:false`. Normal findings JSON remains unchanged.

### Step 3: Read before writing

Work from `summary`, `remediation` and `suppressed` in the JSON. `summary.counts` counts entries; a grouped portfolio entry stands for `count` findings at the `sites` it lists, so quote `summary.findings_total` and `summary.tally_findings` as the number of findings. Pass `no_group: true` to `report` for one entry per finding. `remediation` is already grouped
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

`report` writes standalone HTML: an overview, category bars, findings grouped by rule, then
message, then file, a column-contract summary, suppressed findings, skipped checks, and the rule
reference, with Auto/Light/Dark themes. It loads nothing remote. Filters, decisions, and the source
viewer need JavaScript; with JavaScript blocked, the overview, categories, column summary, skipped
checks, and rule text stay readable, but the groups under each rule do not open. A Snowflake
shared-report sandbox or editor preview may block the script. Do not promise full interactive
support there. Follow the `html-authoring` skill if adapting HTML for the shared-report sandbox.

The report keeps `snowflake-source` and `snowflake-report-metadata` provenance. Its CSP allows only
the embedded script (by hash) and inline styles and blocks data connections. Review paths and
evidence before sharing, even when complete model text is not included.

With `include_models: true`, each file in a message group has a source viewer with the finding
lines marked; it marks them only when the snapshot matches the audited bytes, and otherwise says the
lines are unverified. A report without model text has no source viewer. Source snapshots have
limits of 256 KiB/file, 4 MiB total, and 100 files; they exclude profiles/configuration files,
unsafe paths, and unsupported content. These controls do not sandbox the audit reader.

Edits affect a copy in the report. The reader can preview changes, copy text, or download a new
file; the report never overwrites project files. Mixed or CR-only line endings are read-only.
Use downloads when exact bytes matter, and use manual text copy if clipboard access fails. Apply
changes separately, review the diff, test, then audit again. Do not mark a finding resolved from
a browser edit. There is no live linter, SQL execution, local write server, or WASM validator.

### Step 5: Use markers to fix and consolidate

1. `report` on the root.
2. `annotate` with `dry_run: true`. **⚠️ Stop:** show the diff and get approval before writing.
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
SnowConvert's own markers, such as `SSC-EWI-DBT0001` or `SSC-EWI-INF0039`, are left alone. MIG0001,
MIG0002 and MIG0003 report them. By default (`converter_markers: count`), a marker inside a
comment is only counted, in `summary.not_reported` with its files and lines. A
`!!!RESOLVE EWI!!!` marker outside a comment is executable text. It is always a MIG0001 error.

Use this order as a starting point for migrated estates, then adjust it to the actual dependencies:

1. Vars and parameters (PRJ0009-0018): verify sentinel defaults and required values before changing load behavior.
2. Hooks that write (INC0001-0003, INC0010, INC0016-0020).
3. Macro duplication across projects (MAC0010, MAC0015-0017).
4. Review project consolidation (PRJ0001-0003, PRJ0006) after confirming ownership and deployment boundaries. In a migration project, a merge must also retarget the registry: follow [registry-consolidation](references/registry-consolidation.md). **⚠️ Stop:** show the user the affected units and get approval before any registry patch (the `cur_reconciler` retarget).

### Step 6: Check model columns against scai DDL

1. In a migration project the DDL comes from the registry. Outside one, ask for the scai DDL paths
   if `.dbt-quality.yml` has no `ddl_paths`.
2. `fix_columns` with `path` (and `ddl` outside a migration project), dry run by default. It casts mismatched output columns to
   the DDL type and collation and changes nothing else. In a migration project the diff spans the dbt projects under `path`
   (every registry project with `estate: true`). **⚠️ Stop:** show the diff and get approval.
3. `fix_columns` with `dry_run: false`, then run the project's dbt tests and `report` again.

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

## Validate one file

Run the model-scoped rules against one file. The rules, codes, and remediation are the same as in
the project audit; only the scope differs. This does not build models, connect to a warehouse, or
prove that the SQL returns correct results.

```bash
DQ=${CLAUDE_PLUGIN_ROOT}/bin/dbt-quality

$DQ validate path/to/models/gold/dim_customers.sql     # one file
$DQ validate --strict path/to/model.sql                # exit 1 on any error-level finding
$DQ lint <project> [--format json] [--min-level warning] [--strict]   # whole project, one line per finding
```

Replace example paths and optional arguments before running these commands. If the launcher path
contains spaces, quote `"$DQ"`. On Windows, set `$DQ` to the absolute `bin\dbt-quality.cmd` path
(installed plugin) or `bin/dbt-quality.exe` path (release archive) and invoke it with
`& $DQ validate <path>`.

`validate` exits 0 for a path that is not a discovered dbt model, including a missing path. Check
that the intended `.sql` or `.py` file is under the project's configured model paths. A literal
`$FILE_PATH` argument is read from the environment. If the validator reports nothing on a file with
known problems, check its path first: the engine must find an enclosing `dbt_project.yml` and
discover the file as a model.

Project- and portfolio-scoped rules are skipped for a single-file check; they did not pass. For
example, `SSC-EWI-DBTSQL0001` compares subquery fingerprints across models, and fragmentation checks
need the estate. Report "No active findings from the model-scoped checks that ran" when that is what
the output shows. Do not call a model fully validated on that basis. Use `lint` or the project audit
when the question needs broader coverage.

### Editor tasks

Run once per dbt project, when the user asks for editor setup:

```bash
$DQ setup-tasks [PATH]
```

It adds two tasks to `.vscode/tasks.json` at the dbt project root: `dbt: quality suggestions` and
`dbt: quality suggestions (watch, every 5 min)`. It keeps existing tasks and adds only missing
dbt-quality labels. It exits 1 if `dbt_project.yml` is missing or `tasks.json` is not valid JSON
(JSON-with-comments is not supported). Tasks call the launcher by its absolute path, with process
execution and the platform shell for the watcher.

The linter emits `path:line:col:endLine:endCol: level: [RULE-ID] message -> fix`. If the Problems
panel is empty or points at missing paths, check that the `pattern` block in `.vscode/tasks.json`
maps `file` (1), `line` (2), `column` (3), `endLine` (4), `endColumn` (5), `severity` (6), `code` (7)
and `message` (8).

Diagnostics appear after the task runs, not as you type. The watch task requests folder-open
startup, subject to editor trust and task-approval settings. Reload the window after setup.
Findings do not fail the task by default. Use `lint --strict` to fail CI on active error-level
findings; warnings do not fail that gate. Command errors can still return nonzero.

## Configuration and waivers

One `.dbt-quality.yml` (or `.yaml`) applies to the whole audit: the first one at the audit root or up
to eight folders above it, stopping at the Git root. A project's own file is not read when you audit
its estate. Keys: `thresholds`, `migration`, `disabled_rules`, `ignore`, `exclude_dirs`, `ddl_paths`,
`type_compare`, `ddl_bindings`. To choose these settings rule by rule from the project's findings,
use the `dbt-standards` skill of the `snowflake-migration` plugin. For a false positive or an
accepted trade-off, prefer a narrow waiver to disabling the rule:

```sql
select id from analytics.public.orders  -- dbt-quality: ignore SSC-EWI-DBTSQL0006
-- dbt-quality: ignore-file SSC-EWI-DBTDOC0002
```

```yaml
# .dbt-quality.yml — waives findings with no single line, such as project- and estate-wide ones
ignore:
  - paths: ["models/legacy/**"]
    rules: [SSC-EWI-DBTARC0001]
```

Waiver directives count only inside comments. A directive after code applies to that line; a
directive on its own line applies to its own line and the next non-blank line. Config-related findings often anchor at
`{{ config() }}`; other rules can have a precise read-site anchor. Use the reported location, not a
pack-wide assumption. Waived findings stay in the report as suppressed, with the waiver as the
reason, and do not count as active. Record why the waiver is acceptable.

If an expected finding is missing, search for `dbt-quality: ignore` directives and the `ignore:`
block in the nearest `.dbt-quality.yml`, which can be in an ancestor directory, and the report's
`suppressed` section. Also check `disabled_rules`, which produces skipped checks rather than findings.
To choose which rules a team enforces, see the rule tiers in
[references/rule-catalog.md](references/rule-catalog.md).

## Limits

There is no general naming-convention validator. A migrated model may keep its original object
name; do not infer a naming defect without a reliable source-to-target mapping. MIG0007 can still
flag ETL-instance names for review.

Static rules do not provide complete SQL dialect validation or business-result validation. Run the
project's dbt build and tests after a change. A successful build does not prove all business logic
correct either.

## References

- [README.md](README.md): the user guide (install, first audit, configuration, CI gating, troubleshooting, limits). Point users to it.
- [references/rule-catalog.md](references/rule-catalog.md): every rule with its tier and signal. Load it when a user disputes a finding or asks which rules exist.

## Output

Return the report paths (or the checked file), scope, coverage gaps, and a short list of fixes
supported by the evidence. State whether complete model text was included and whether the output
is in a durable folder. Do not claim that edits are validated until the project's checks and a fresh audit
have run.
