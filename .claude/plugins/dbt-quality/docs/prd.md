# dbt-quality product requirements

This document says what dbt-quality is for, who uses it, and what it must do. It describes the
product as it ships in the `snowflake-migration` plugin. How to use it is in the
[README](../README.md); the rules are in the [rule catalog](rule-catalog.md); the HTML report is in
the [report specification](report-spec.md).

## Problem

SnowConvert and AIM convert SSIS and Informatica workloads into dbt projects for Snowflake.
Customers also write dbt projects by hand. Both kinds of project carry problems that dbt itself
does not catch until a model runs, or does not catch at all:

- duplicate models and sources, inside one project and across the projects of an estate;
- relations read by a hard-coded name instead of `ref()` or `source()`;
- incremental models that cannot prune, merge without a key, or depend on their own prior state;
- macros with hidden side effects, credentials in project files, and missing tests and docs;
- model columns that no longer match the Snowflake tables that scai converted;
- conversion debt: SnowConvert EWI and FDM markers that nobody has reviewed.

Engineers and coding agents need a check that finds these problems before the project runs. The
check must work on a laptop and in CI, without a warehouse connection, and it must give the same
answer every time.

## Users

| User | Need |
| --- | --- |
| Migration engineer | Review a converted dbt estate, find what to fix first, and track the fixes. |
| dbt developer | See findings in the editor while writing a model, and gate a pull request in CI. |
| Coding agent (Cortex Code, Claude Code) | Audit a project, explain each finding, and propose fixes that a person approves. |
| Field and delivery teams | Give a customer a readable report of a project's health. |

## Goals

- G1. One deterministic, local, static analyzer for Snowflake dbt projects. The same inputs and
  configuration give the same findings.
- G2. One analyzer behind every surface: CLI, MCP server, JSON and HTML reports, markers, and the
  agent skill. A finding means the same thing on every surface.
- G3. Each finding gives its evidence, its location, and a remediation that a person or agent can
  act on. Findings are guidance to review, not automatic rewrites.
- G4. Install with the `snowflake-migration` plugin and nothing else: no Rust, Python, uv, or Node
  runtime, and no Snowflake credentials.
- G5. Fit both migrated projects and native dbt projects. Migration-specific guidance is gated by
  migration signals, so a native project is not judged as a migration.

## Non-goals

- Running dbt, project macros, or warehouse queries, or claiming that suggested SQL is correct at
  run time.
- Rewriting models automatically, apart from the explicit `fix-columns` casts and the diagnostic
  markers that `annotate` writes.
- Fixing the converter. Converter defects that dbt-quality finds belong to SnowConvert tickets.
- Reading `target/manifest.json` or running `dbt parse`. A manifest can be out of date.

## Functional requirements

### Scope and discovery

- F1. An audit root is one dbt project or an estate: a directory that contains `dbt_project.yml`
  files at any depth. Cross-project checks run across every project under the root.
- F2. Discovery skips generated and dependency directories (`target`, `dbt_packages`, `logs`,
  `.git`, `node_modules` and similar). `exclude_dirs` replaces that list.
- F3. The analyzer reads model SQL and Python, YAML, macros, snapshots, tests and project
  files. It parses Jinja with dbt's own Jinja parser (the pinned dbt minijinja fork) and SQL with
  dbt's Snowflake lexer and the sqlparser fork that dbt uses. [DBT_PIN.md](../DBT_PIN.md) records
  the pinned dbt commit.
- F4. The model graph comes from the `ref()` calls in each model file.

### Rules

- F5. Rules are grouped in packs: PRJ (project structure and relations), INC (incremental loads),
  MAC (macros), SQL, MAT (materialization), TST (tests), DOC (documentation), ARC (architecture),
  OPS (operations and secrets), MIG (conversion debt) and COL (columns against scai DDL).
- F6. Each rule has a code of the form `SSC-{KIND}-DBT{PACK}{NNNN}`, a kind, a diagnostic level,
  an impact severity, a tier, a description, a remediation and examples. Rule metadata lives in
  `rules/*.json`, and the catalog is generated from it.
- F7. Tiers decide when a rule applies. `universal` rules apply to every project. `architecture`
  findings can be suppressed for a detected lift-and-shift project, and the report counts them
  apart. `migration` rules run on migration signals and are never suppressed by migration
  detection.
- F8. A rule reports what the files show. Where a match is uncertain, such as an unresolved
  producer for a hard-coded relation, the finding says so and gives the steps to confirm it.
- F9. A rule that checks executable SQL does not match inside a SQL comment, a string literal or
  a quoted identifier. Rules whose subject is that text are exempt and read it by design: the MIG
  rules that find converter markers and placeholder comments (for example MIG0002 and MIG0003,
  which report `SSC-EWI` and `SSC-FDM` markers left in comments), and MIG0010, which checks that
  waivers (F13), comment waivers included, suppress something.
- F10. A check that cannot run is reported as skipped with its reason, never counted as passed.

### Configuration

- F11. `.dbt-quality.yml` at the project or estate root configures the audit. Lookup takes the
  nearest file in the root's ancestors, up to eight levels, and stops at a Git boundary.
- F12. Configuration supports `migration.mode` (`auto`, `native` or `lift_and_shift`),
  `disabled_rules`, `ignore` entries by path and rule, rule `thresholds`, `exclude_dirs`, and the
  column inputs `ddl_paths`, `type_compare` and `ddl_bindings`.
- F12a. Two keys control report size on large estates. `converter_markers: count` (the default)
  counts SnowConvert's own markers in `summary.not_reported` instead of one finding per marker;
  `report` lists each marker. `group_threshold` (default 25, `0` turns it off) merges one rule and
  message that fires in more projects than the threshold into one `portfolio` finding with its
  project list.

### Waivers and suppressions

- F13. A person can waive a finding with an `ignore` entry, a `-- dbt-quality: ignore <code>` line
  comment, a `-- dbt-quality: ignore-file <code>` comment, or a SQLFluff-style `-- noqa` comment
  (line, file, and `disable=`/`enable=` ranges). Waivers apply to dbt-quality codes only.
- F14. A waived finding stays in the report as suppressed, with the waiver form and line. It does
  not count as active.
- F15. A waiver that names no dbt-quality rule, or that matches no finding, is itself reported, so
  a typo or a stale waiver is visible.

### Surfaces

- F16. The CLI is one `dbt-quality` binary with these commands:

  | Command | Does |
  | --- | --- |
  | `audit` | Audit a root and write the JSON report, and HTML on request |
  | `lint` | Editor-style diagnostics, or JSON lint records |
  | `validate` | Run the model-scoped rules on one file |
  | `rules` | List the rules, or explain one |
  | `annotate` | Preview, write or remove `SSC-EWI-DBT*` markers in the files |
  | `fix-columns` | Preview or write casts to the scai DDL type and collation |
  | `setup-tasks` | Add VS Code tasks that run the linter |
  | `mcp` | Run the stdio MCP server |

- F17. The MCP server is the `mcp` command. It speaks newline-delimited JSON-RPC over stdio and
  offers the tools `version`, `report`, `findings`, `rules`, `annotate` and `fix_columns`. The
  plugin declares it, so installing the plugin connects it.
- F18. The `dbt-quality` skill in the plugin routes a user's intent to the right tool, reports only
  what the tool returned, and stops for approval before any write.
- F19. `audit --fail-on-error`, `lint --strict` and `validate --strict` exit nonzero on active
  error-level findings. Warnings do not fail them.
- F19a. `audit --timings` prints the wall time of each audit phase to stderr. `audit --column-csv`
  writes the column contract CSV to a chosen path, with or without `--html`.

### Reports

- F20. The JSON report lists active findings with evidence and location, project summaries,
  suggestions, skipped checks, suppressed findings, read errors and remediation priorities.
- F21. The HTML report is one standalone file. It shows the audit scope and coverage gaps,
  a category breakdown, findings grouped by rule, message and file with search and filters, and a
  column contract summary. Suppressed findings, skipped checks and read errors have their own
  views. Column contract findings are also written to `column_issues.csv`. The embedded data uses
  interned tables, and the page builds each group when the reader opens it, so a report with tens
  of thousands of findings stays small.
- F22. The HTML report includes model source only when the user opts in (`--include-models` or
  `include_models: true`), within fixed size limits, and never includes profiles or configuration.
- F23. A reader can record one decision per rule, message group or file (*Will address*,
  *Ignore once*, *Ignore permanently*) and export them as one item per finding. The report never
  writes project files.
- F24. The report meets the safety rules in the [report specification](report-spec.md): escaped
  embedded data, a strict CSP, no data connections, and no remote script.

### Edits

- F25. `annotate` and `fix-columns` preview a diff by default. A write needs an explicit flag,
  refuses a dirty Git tree unless the user overrides it, and changes only files inside the root.
- F26. `annotate` writes markers, not fixes. It leaves SnowConvert's own markers alone and does not
  duplicate them. Annotating and then removing markers restores the input bytes. It writes only
  to files that are unchanged since the audit read them, and lists the files it skipped.
- F27. `fix-columns` changes only a column's type and collation, to match the scai DDL. Missing and
  extra columns stay findings.

## Non-functional requirements

- N1. **Static and local.** No dbt run, no warehouse connection, no credentials, and no network
  access during an audit.
- N2. **Deterministic.** Findings, their order and report counts depend only on the files and the
  configuration.
- N3. **Platforms.** Native binaries for `x86_64-unknown-linux-musl`, `aarch64-unknown-linux-musl`,
  `x86_64-apple-darwin`, `aarch64-apple-darwin`, `x86_64-pc-windows-msvc` and
  `aarch64-pc-windows-msvc`.
- N4. **Distribution.** The plugin's launchers find a local build or download the binary for their
  version from the public Snowflake-Labs release, check its SHA-256 and cache it. The plugin preview
  and release workflows build, test and smoke-test every target before they publish.
- N5. **Safety.** The MCP server runs with its user's file access and is for trusted clients only.
  Writes stay inside the chosen root and skip symlinks that leave it.
- N6. **Licensing.** Code taken from dbt is Apache-2.0, MIT or BSD-3-Clause, from the one pinned
  dbt commit. No ELv2 or proprietary dbt code.
- N7. **Performance.** An audit reads each file from disk at most once and walks the audit root
  once. Values derived from a project's files (source declarations, locations, profile targets,
  waivers) are computed at most once per project. The walk, the project build and rule
  evaluation run in parallel on all cores. Parallel work keeps the order that N2 requires.

## Quality

- Q1. Every rule has Rust tests for what it flags and what it leaves alone. A defect fix starts
  with a failing test. Discovery tests assert one read per file and one walk per audit (N7).
- Q2. CI runs the tests, Clippy, and the catalog, dbt pin and sample report drift checks on every
  pull request that changes dbt-quality. The release workflow runs the tests and the package and
  launcher smoke tests on every target.
- Q3. Before a large change merges (a new or reworked rule, the SQL tokenizer or Jinja reading,
  discovery, waivers, levels or the report), the
  [`judging-dbt-quality-reports`](../../../.claude/skills/judging-dbt-quality-reports/SKILL.md)
  skill audits snowflake-dbt-demo with and without the change, and an independent judge checks the
  findings for false positives and misses.

## Success criteria

- A customer who installs the `snowflake-migration` plugin can audit a dbt project from Cortex Code
  or Claude Code with no other install step.
- The monorepo pipelines build and publish the binaries for every supported target.
- On snowflake-dbt-demo, the judge confirms the findings as true positives, and every confirmed
  false positive or miss has a test that fixes it.

## Known limits

- Static analysis cannot follow custom naming macros or unresolved locations to a physical
  producer. Those findings ask the user to confirm.
- The macOS and Windows binaries are unsigned.
- Each MCP tool call runs a new audit. The server does not reuse an earlier call's files or DDL
  index.
- Full interactive editor integration and `dbt_external_tables` compatibility with native
  `EXECUTE DBT PROJECT` are unverified.
