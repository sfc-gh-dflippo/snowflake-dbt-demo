# dbt-quality

A local linter and MCP server for Snowflake dbt projects, including projects migrated by
SnowConvert. Its 126 rules cover project structure, relation dependencies, incremental loads,
macros, SQL, materialization, tests, documentation, column contracts against scai DDL, and conversion debt.

Use the **CLI** for terminal, editor, and CI checks. Use the **MCP server** to let an assistant
inspect findings and propose fixes. Both use the same Rust analyzer with dbt's Jinja parser and
local SQL analysis. The analyzer reads local files; it does not run dbt models or connect
to a warehouse. Findings are guidance to review, not automatic model rewrites.

## Quick start

### 1. Install the plugin

dbt-quality ships in the `snowflake-migration` plugin. The plugin release (`plugin-release.yml`) syncs the plugin to
[Snowflake-Labs/cortex-code-migrations](https://github.com/Snowflake-Labs/cortex-code-migrations).
Install the plugin from the URL of its `plugin` directory. To use a release tag, put the tag in the URL:

```bash
cortex plugin install "https://github.com/Snowflake-Labs/cortex-code-migrations/tree/<tag>/plugin"
```

During development, install the plugin from a branch of this repository:

```bash
cortex plugin install "https://github.com/snowflake-eng/migrations-snowconvert-desktop/tree/<branch>/ai/plugin"
```

To install from a local copy of the plugin, such as `ai/plugin` in a source checkout, give its path:

```bash
cortex plugin install "/absolute/path/to/plugin"
```

Run `cortex plugin list` to check the installation.

The plugin's `bin/dbt-quality` launcher (Windows: `bin\dbt-quality.cmd`) finds or downloads the
native `dbt-quality` executable for your machine. Users do not need a Rust, Python, uv, or Node
runtime. Annotation's clean-tree safeguard and the Git-aware checks need Git. The macOS and Windows
binaries are unsigned. To test an unreleased commit, build from source (see
[Build from source](#build-from-source)).

### 2. Audit a project or estate

The examples below use the source checkout's `ai/plugin/bin/dbt-quality` launcher. In an installed
plugin, use its `bin/dbt-quality` (Windows: `bin\dbt-quality.cmd`) instead.

The launchers use the first of these: `DBT_QUALITY_EXE`, a local build in `bin/<target>/`, or a
cached download. If none exists, they download the release archive for their `VERSION`. Then they
check its SHA-256 and cache the binary in `~/.cache/dbt-quality/` (`%LOCALAPPDATA%\dbt-quality\`
on Windows). To use a different release location, set `DBT_QUALITY_DOWNLOAD_BASE`. The checksum
comes from the same release. It detects a corrupt download, not a release that was built wrong.

From a built source checkout, try the included fixture without modifying it:

```bash
ai/plugin/bin/dbt-quality audit ai/crates/dbt-quality/tests/fixtures/ewi_estate --stdout --quiet
```

For your own project, replace `/absolute/path/to/dbt-project` with its directory. To detect
cross-project collisions, use the **parent directory containing all the projects**.

```bash
# JSON on stdout; no report files or project edits.
ai/plugin/bin/dbt-quality audit /absolute/path/to/dbt-project --stdout --quiet

# Save JSON and HTML outside the project. Create the output directory first.
mkdir -p ./reports
ai/plugin/bin/dbt-quality audit /absolute/path/to/dbt-project \
  --out ./reports/findings.json --html ./reports/report.html

# Editor-style diagnostics, or structured lint records.
ai/plugin/bin/dbt-quality lint /absolute/path/to/dbt-project
ai/plugin/bin/dbt-quality lint /absolute/path/to/dbt-project --format json
```

Open `reports/report.html` in a browser on a machine that can access that file. The JSON report
includes project summaries, suggestions, skipped checks, suppression information, and remediation
priorities. An ordinary CLI audit writes `dbt-audit-suggestions.json` under the audited root unless
`--out` or `--stdout` is supplied. HTML is written only when `--html` is supplied.

## Use the HTML report

Open the [sample report](sample-report.html) in a browser to try the report with synthetic test
data. It demonstrates the four-project `ewi_estate` fixture; it does not cover every rule.
Download the HTML file if your source browser shows its markup instead of the report.

The report has seven sections, in this order:

1. **Overview.** Seven tiles show Projects, Models, Active findings, Errors, Warnings,
   Information and Not reported. *Not reported* counts SnowConvert markers that the audit counts
   but does not list (`converter_markers: count`, see [Coverage, configuration, and waivers](#coverage-configuration-and-waivers)). The tiles
   cover the whole audit, not only the findings that the command filters returned.
2. **Categories.** Server-rendered stacked bars (error, warning, information) and a table.
3. **Findings.** Findings are grouped by rule, then by message, then by file. A message group
   replaces the quoted names and numbers with `...` and `N`; each file lists its line numbers, and
   the replaced values appear after the line number. Open a rule to see its message groups, and
   open a message group to see its files. The page builds each level when you open it, so a report
   with tens of thousands of findings stays small and fast. Search (rule, message or file path),
   category and level filters apply to groups.
4. **Column contract.** A summary of the `COL` findings: counts per rule and the most common
   type mismatches. The full list is in `column_issues.csv` (below).
5. **Suppressed.** Suppressed findings, grouped the same way, with no decision controls.
6. **Skipped checks.** Rules that could not run and read errors. These are not passed checks.
7. **Rule reference.** Guidance for each rule that returned a finding.

The report uses Okabe-Ito colors for levels: error `#D55E00` (with a striped pattern),
warning `#E69F00`, information `#56B4E9`. Every level badge also shows its name as text. The
report follows the browser's color preference. Use **Auto**, **Light**, or **Dark** to change it.
Theme controls, filters, and decisions need JavaScript. The page loads no remote script or style,
so a report works in a sandbox that blocks the network. If scripts are blocked, the overview,
category bars, column summary, skipped checks, and rule text stay readable, but the findings under
each rule stay closed.

### Column contract CSV

An audit with scai DDL (`--ddl`, or `ddl_paths`) writes every column contract finding to
`column_issues.csv` next to the HTML report. The columns are `project, model, file, line, column,
model_type, ddl_type, rule, message`. `model_type` is the cast type in the model and is empty when
the model has no cast. Use `--column-csv <path>` to write the file elsewhere; with
`--column-csv` the CSV is written even when `--html` is not set. The MCP `report` tool writes
`column_issues.csv` into `out_dir` next to the HTML report. The JSON report is unchanged. The CSV
lists each model's findings even when portfolio grouping (`group_threshold`) merged them in the JSON.

### View a model and record decisions

By default, a report contains finding evidence but no model files. To include model text in the
HTML, opt in explicitly:

```bash
ai/plugin/bin/dbt-quality audit /absolute/path/to/dbt-project \
  --out ./reports/findings.json --html ./reports/report.html --include-models
```

Create `./reports` first. `--include-models` requires `--html`. The MCP equivalent is
`include_models: true` on `report`; it cannot be combined with `html:false`. These options add
source text to HTML only, not to the normal findings JSON or the MCP response. With model text,
each file in a message group has a **Source** button. It opens the file below the entry, 400 lines
at a time, with the finding lines marked. The report marks lines only when the snapshot matches the
audited bytes; otherwise it says the line numbers are unverified. A report without model text has
no source viewer and no file picker.

**Sharing an HTML report with model text also shares that source.** Even without this option,
reports contain paths and finding evidence. Review the report before sharing it. Source inclusion
is limited to discovered SQL/Python models: at most 256 KiB per file, 4 MiB total, and 100 files.
The snapshot reader rejects ambiguous ownership, symlinks, paths outside the audit/project roots,
non-model files, non-regular files, binary-like content, and invalid UTF-8. It reports omissions
instead of silently truncating files. It does not include profiles or configuration files.
These limits protect source snapshots; they do not sandbox the audit's existing file reader.

A rule, a message group and a file each take one decision: *Will address*, *Ignore once* or
*Ignore permanently* (with an optional reason). A wider choice replaces the choices inside it, and
a narrower choice overrides the wider one for its own findings. The browser keeps decisions in
local storage under the audit root, so they survive a re-audit of the same root in the same
browser. The keys use the rule, the message template and the file path, not their position in the
page. *Export decisions* downloads `dbt-quality-decisions.json` with one item per decided finding
(`rule_id`, `project`, `file`, `line`, `message`, `decision`), so a decision on a rule or a message
expands to every finding in it. An *Ignore permanently* item carries its reason and the waiver
comment to add. In the export, a `message` is the template with the listed values put back; when
the report dropped a value that only repeated the file name, the values follow the template in
parentheses. The report never writes project files: an agent or you apply the exported decisions,
review the diff, run the dbt checks, then re-run the audit. This is a snapshot, not live linting or
SQL execution. It has no local write server.

The report loads no remote code. Its CSP allows only the embedded script (by hash) and inline
styles, blocks data connections, forms, frames, and objects, and it sends no referrer. Reference
links open only when the reader follows them.

## Connect the MCP server

The `snowflake-migration` plugin starts the MCP server, so installing it (see
[Install the plugin](#1-install-the-plugin)) connects the server. The server is the `mcp` subcommand
of `dbt-quality`. It needs no API key or Snowflake credentials.

Open a Cortex Code session in your dbt project, use `/mcp` to inspect the connection, and ask:

> Use dbt-quality to audit this project and show the highest-priority findings. Do not edit files.

The Rust tests cover the CLI and the stdio protocol. They do not test interactive use in each client.

This is a local **stdio** process, not an HTTP service; there is no port or URL to start. It accepts
newline-delimited JSON-RPC and advertises MCP protocol `2025-06-18`. The client launches the server
and keeps stdin open. Starting it alone in a terminal can appear idle because it is waiting for
protocol messages.

### Tools and example arguments

These JSON objects are tool arguments, not shell commands. Replace the example paths with paths
accessible to the server.

| Tool | Purpose | Example arguments |
|---|---|---|
| `version` | Server version, pinned dbt version/commit, rule count | `{}` |
| `report` | Save JSON and HTML; return their paths and counts | `{"path":"/work/my-project","out_dir":"/work/reports/dbt-quality"}` |
| `findings` | Return active findings with optional filters | `{"path":"/work/my-project","rule_ids":["SSC-EWI-DBTPRJ0020"]}` |
| `rules` | Explain one rule, including remediation and examples | `{"code":"SSC-EWI-DBTPRJ0020"}` |
| `annotate` | Preview or write markers; dry run by default | `{"path":"/work/my-project","dry_run":true}` |
| `fix_columns` | Preview or write casts to the scai DDL type and collation; dry run by default | `{"path":"/work/my-project","ddl":["/work/scai-project"]}` |

`report` accepts `category` (an array such as `["PRJ"]`), `min_level`, and `html:false` to omit HTML.
Without `out_dir`, it writes reports under the server's system temporary directory, outside the
project. Copy reports you need to retain to a durable location. `findings.files` is an array of
paths relative to the audited root. `rules` also accepts `pack` and `kind` filters.

**Filesystem permissions matter:** the server runs with its process user's access. The caller
chooses the audit root and report directory; those choices are not sandboxed by the server.
Connect it only to trusted clients. Annotation writes stay within the selected root, skip symlinks
that escape it, and require a clean Git tree unless `allow_dirty:true` is explicitly supplied.

## Review and fix safely

1. Audit the project or estate. Read the evidence and the relevant files.
2. Fetch `rules` for a finding's full code. Confirm target names, source locations, and original
   load semantics where the advice requires them.
3. Preview markers with `annotate` using `dry_run:true`; review the returned diff.
4. Approve the marker changes before using `dry_run:false`. The tool writes markers, not fixes.
5. Make and test the code changes, then re-audit. Refresh markers to remove resolved findings.

CLI equivalents:

```bash
ai/plugin/bin/dbt-quality rules --code SSC-EWI-DBTPRJ0020
ai/plugin/bin/dbt-quality annotate /absolute/path/to/dbt-project
# After reviewing the diff, with a clean Git tree:
ai/plugin/bin/dbt-quality annotate /absolute/path/to/dbt-project --write
# Remove only dbt-quality markers; preview by omitting --write.
ai/plugin/bin/dbt-quality annotate /absolute/path/to/dbt-project --remove --write
```

Use repeatable `--rule <full-code>` arguments (MCP: `rule_ids`) to scope annotation. `--allow-dirty`
(MCP: `allow_dirty:true`) overrides the clean-tree safeguard; use it deliberately, not by default.
Markers leave SnowConvert's original diagnostics intact. A finding that only reports an existing
converter marker (MIG0001, MIG0002, MIG0003) counts in the report but gets no second marker, so
`annotate` does not duplicate SnowConvert EWI or FDM markers. Without intervening edits, annotation
followed by removal restores the input bytes. Removal does not undo code fixes you made.

For the detailed agent workflow, see [dbt-quality skill](skills/dbt-quality/SKILL.md).

### Check and fix columns against scai DDL

The COL rules compare each model's outer SELECT with the Snowflake table that scai converted. They
report missing and extra columns, alias mismatches, type mismatches, and collation mismatches.
Point them at a scai project root (it reads `snowflake/<db>/<schema>/table/*.sql`), at any folder
with `table/` subfolders, or at `.sql` files:

```yaml
# .dbt-quality.yml
ddl_paths: [../scai-project]
type_compare: normalized   # or strict: TIMESTAMP_NTZ does not match TIMESTAMP_NTZ(3)
ddl_bindings: {E2E_DB: PROD}   # values for <%TOKEN%> and ${TOKEN} in DDL names
```

A model matches the DDL table with its `alias` or file name; `schema` and `database` config choose
between tables with the same name. If the scai project has a `registry/` folder, the parsed columns
are also compared with the registry signatures (COL0007). `fix-columns` rewrites a mismatched item
as `CAST(<expr> AS <DDL type>) COLLATE '<DDL collation>' AS <alias>`. It changes only types and
collations; missing and extra columns stay warnings.

```bash
ai/plugin/bin/dbt-quality lint /path/to/dbt-project --ddl /path/to/scai-project
ai/plugin/bin/dbt-quality fix-columns /path/to/dbt-project --ddl /path/to/scai-project   # diff only
ai/plugin/bin/dbt-quality fix-columns /path/to/dbt-project --ddl /path/to/scai-project --write
```

Without a catalog, a column type is known only from an outer `CAST`, `TRY_CAST`, or `::`. A column
with no cast is reported as "no explicit cast".

## Editor and CI usage

Install VS Code task definitions for an individual dbt project:

```bash
ai/plugin/bin/dbt-quality setup-tasks /absolute/path/to/dbt-project
```

This writes `.vscode/tasks.json`, retaining existing tasks and adding missing task labels. It
requires valid JSON, not JSON-with-comments. Run **dbt: quality suggestions** from the editor's
Tasks menu; findings appear in Problems. The second task runs every five minutes and requests
folder-open startup, subject to the editor's task trust/approval settings.

For CI, build or provision the binaries first, then use:

```bash
ai/plugin/bin/dbt-quality lint /absolute/path/to/dbt-project --strict
# Or save a report while gating on error-level findings:
ai/plugin/bin/dbt-quality audit /absolute/path/to/dbt-project \
  --stdout --quiet --fail-on-error > findings.json
```

Default audit/lint success does not mean no findings. `audit --fail-on-error`, `lint --strict`, and
`validate --strict` fail on active **error-level** findings; warnings do not fail these checks.
Command or I/O errors may also return nonzero. `lint` returns success when it finds no projects,
so verify your CI root; `audit` reports that condition as an error.

Other useful commands:

```bash
ai/plugin/bin/dbt-quality validate /absolute/path/to/dbt-project/models/orders.sql
ai/plugin/bin/dbt-quality audit /absolute/path/to/dbt-project \
  --category PRJ --min-level warning --stdout --quiet
```

## Coverage, configuration, and waivers

A root is a project or an estate containing `dbt_project.yml` files. Generated/dependency
directories such as `target`, `dbt_packages`, `.git`, and `logs` are excluded from source scanning.
Graph rules (ARC0005, MAT0001, MAT0002) build the model dependency graph from the `ref()` calls in
each model file. The analyzer does not run `dbt parse` and does not read `target/manifest.json`,
even when one is present, because a manifest can be out of date. A check is reported as skipped
only when it is disabled in `.dbt-quality.yml` or cannot run at the requested scope.

Rule IDs look like `SSC-EWI-DBTPRJ0020`. The pack identifies the area (`PRJ`, `INC`, `SQL`, `MAC`,
`TST`, `DOC`, `MAT`, `ARC`, `OPS`, `MIG`, `COL`); `kind`, diagnostic `level`, and impact `severity` are
separate fields. Architecture findings may be suppressed for detected lift-and-shift projects;
the report records this separately from active findings.

Put `.dbt-quality.yml` at the project or estate root. Lookup uses the nearest file, searching
ancestors up to eight levels and stopping at a Git boundary. For example:

```yaml
migration:
  mode: auto  # auto, native, or lift_and_shift
ignore:
  - paths: ["models/legacy/*"]
    rules: ["SSC-EWI-DBTSQL0006"]
```

Two more keys control report size on large estates:

```yaml
converter_markers: count   # count (default) or report
group_threshold: 25        # 0 turns portfolio grouping off
```

In the HTML report, `converter_markers` sets the *Not reported* tile, and `group_threshold` sets how many projects a finding must reach before the Findings section shows it once with a list of its projects.

`converter_markers: count` makes MIG0001, MIG0002 and MIG0003 emit no finding for markers that SnowConvert wrote (`SSC-EWI-*`, `SSC-FDM-*`, `!!!RESOLVE EWI!!!`). The audit JSON lists them in `summary.not_reported` (`{code, message, count}`, largest count first, summed over all projects) and `summary.not_reported_total`. A count is one per distinct marker text in each model. Markers that dbt-quality wrote (`SSC-*-DBT<PACK><NNNN>`) are never counted. MIG0004-MIG0010 are unchanged. Set `report` to get one finding per marker again; the JSON then has no `not_reported` keys.

When one rule and one message fire in more than `group_threshold` projects, the report holds one finding with `project: "portfolio"`, a message that ends `(N projects)`, and `projects`, the sorted project paths. The key is the rule ID plus the message with each project's path, label and name replaced by `<project>`. A suppressed or waived finding is not part of a group. Estate-level findings are not grouped.

Use full rule IDs. An ignore entry waives the matching finding; it is not a fix. A waived finding stays in the report as suppressed, with the waiver form and line as the reason (for example ``waived by `-- noqa: SSC-EWI-DBTSQL0002` (line 12)``). It does not count as active. You can also put
`-- dbt-quality: ignore SSC-EWI-DBTSQL0006` on the reported SQL line or immediately above it, or
`-- dbt-quality: ignore-file SSC-EWI-DBTSQL0006` to waive that rule throughout the file. Model SQL also accepts SQLFluff-style comments, for dbt-quality codes only: `-- noqa` (every rule on that line), `-- noqa: CODE[, CODE]` (that line), `-- noqa-file[: CODE[, CODE]]` (the whole file), and `-- noqa: disable=CODE` until `-- noqa: enable=CODE` or the file end (dbt-quality also accepts `-- sqlfluff:disable [CODE]` / `-- sqlfluff:enable [CODE]` for this range). As in SQLFluff, `noqa` must be the first word of its comment, so a comment that only mentions it waives nothing. A CODE is a full code (`SSC-EWI-DBTSQL0002`) or a short one (`SQL0002` or `DBTSQL0002`); `all` or no code means every rule. A code that names no dbt-quality rule, such as a SQLFluff `LT01`, waives nothing and is reported by `SSC-EWI-DBTMIG0010`, as is any waiver that matches no finding. Configuration
also supports `disabled_rules`, thresholds, and `exclude_dirs` (directory names to skip; replaces the default list of `target`, `dbt_packages`, `node_modules` and similar); see the [rule catalog](docs/rule-catalog.md).

## Troubleshooting and limits

| Symptom | Check |
|---|---|
| Source launcher says it cannot download | The launcher prints the URL. Check network access to GitHub, set `DBT_QUALITY_DOWNLOAD_BASE`, or build with `ai/crates/dbt-quality/scripts/build-plugin.sh` or `build-plugin.ps1`; binaries are Git-ignored. |
| Cargo cannot fetch `minijinja` | It is a Git dependency on `dbt-labs/dbt` at the rev in [DBT_PIN.md](DBT_PIN.md). Check network access to GitHub. Resolving the `ai/` workspace also needs the private Git dependencies of the other members; see `ai/scripts/require-cargo-git-cli.sh`. |
| Native dependency build fails | Check the Rust toolchain (edition 2024), the selected target, and the native linker: musl-tools on Linux, Xcode command-line tools on macOS, or Visual Studio C++ build tools on Windows. |
| MCP server fails to start or shows no tools | Run the plugin's `bin/dbt-quality --version` (Windows: `bin\dbt-quality.cmd --version`) and check its execute permission. Run `cortex plugin list` to check that the plugin is installed and enabled, then inspect the MCP logs and reconnect with `/mcp`. No HTTP URL is involved. |
| No projects or missing cross-project findings | Point at a directory containing `dbt_project.yml`; choose the common estate parent for cross-project analysis. |
| Checks are skipped | Inspect `skipped_checks`. Each entry gives the reason: the rule is disabled in `.dbt-quality.yml`, or `validate` cannot run a project-scoped rule on one file. |
| Annotation refuses to write | Commit or stash project changes first, including dirty nested repositories; review the dry-run diff. |
| An ignored rule still appears | Check its full code and project/audit-root-relative path, and which nearest config file was loaded. |

The linter performs static analysis. Custom naming macros and unresolved locations can prevent
physical producer matching; follow the confirmation steps rather than guessing. Review suggested
SQL changes and run your dbt tests before adopting them. Some cross-rule SQL/macro advice overlaps
remain. The release workflow runs the extracted-package smoke checks on each target; local builds do
not get them. Full interactive editor
integration and `dbt_external_tables` compatibility with native `EXECUTE DBT PROJECT` remain unverified.

## Build from source

dbt-quality is two crates in the `ai/` Cargo workspace. Developers need Git, Rustup with a stable
toolchain that supports edition 2024, and the platform's native linker/toolchain. Linux builds use
musl-tools; macOS uses Xcode command-line tools; Windows uses Visual Studio C++ build tools.
Initial Cargo downloads need network access. Python and uv are not part of the build or test workflow.

From the repository root:

```bash
rustup target add x86_64-unknown-linux-musl
ai/crates/dbt-quality/scripts/build-plugin.sh x86_64-unknown-linux-musl
ai/plugin/bin/dbt-quality --version
```

The supported targets are the six platforms of the other `snowflake-migration` plugin tools:
`x86_64-unknown-linux-musl`, `aarch64-unknown-linux-musl`, `x86_64-apple-darwin`,
`aarch64-apple-darwin`, `x86_64-pc-windows-msvc`, and `aarch64-pc-windows-msvc`. Build macOS
binaries on macOS and Windows binaries on Windows. The scripts do not install cross-linkers or
claim cross-compilation from any host. On Windows, `build-plugin.ps1` builds for the host
architecture unless you pass `-Target`:

```powershell
rustup target add x86_64-pc-windows-msvc   # aarch64-pc-windows-msvc on ARM64
.\ai\crates\dbt-quality\scripts\build-plugin.ps1
.\ai\plugin\bin\dbt-quality.cmd --version
```

PowerShell 7 (`pwsh`) drives archive packaging and extracted-package smoke tests; it is not
needed to run downloaded binaries.

## Maintainer reference

Before merging a large change here (a new or reworked rule, the SQL tokenizer or Jinja reading,
discovery, waivers, levels or the report), run the
[`judging-dbt-quality-reports`](../../.claude/skills/judging-dbt-quality-reports/SKILL.md) skill: it
audits snowflake-dbt-demo with and without the change and has an independent judge check the
findings.

| Path | Content |
|---|---|
| `ai/crates/dbt-quality/rules/` | Metadata and schema for 126 rules in 11 packs |
| `ai/crates/dbt-quality/dbt-quality-core` | Discovery, detectors, report generation, annotations |
| `ai/crates/dbt-quality/dbt-quality-cli` | Command-line interface; `dbt-quality mcp` runs the stdio JSON-RPC MCP server |
| `ai/plugin/bin`, `ai/plugin/skills/migration/dbt-quality` | Launchers and the dbt-quality skill in the `snowflake-migration` plugin |
| `ai/crates/dbt-quality/docs/` | The [product requirements](docs/prd.md), the generated [rule catalog](docs/rule-catalog.md) and the [HTML report specification](docs/report-spec.md) |
| `ai/crates/dbt-quality/package/` | Manifest template for the standalone release archive |
| [DBT_PIN.md](DBT_PIN.md) | The pinned dbt commit and build constraints |
| `ai/crates/dbt-quality/scripts/` | Native builds, packaging, artifact smoke tests, catalog and pin checks |
| `ai/crates/dbt-quality/tests/` | Fixture projects for the Rust tests |

Run these from the `ai/` directory:

```bash
cargo test -p dbt-quality-core -p dbt-quality-cli
cargo clippy -p dbt-quality-core -p dbt-quality-cli --all-targets -- -D warnings
crates/dbt-quality/scripts/check-catalog.sh
crates/dbt-quality/scripts/check-dbt-pin.sh
```

CI (`.github/workflows/plugin-ci-run.yml`) runs the tests, Clippy, and `make dbt-quality-checks`
(catalog, pin, and sample report drift) on Linux. The release workflow builds the other targets.

After changing rule metadata, regenerate the catalog with `crates/dbt-quality/scripts/build-catalog.sh`.
Build the plugin again after Rust or metadata changes.

### Publish a release

The plugin preview (`plugin-pr.yml`) and the plugin release (`plugin-release.yml`) publish the
binaries. Each one runs `.github/workflows/plugin-dbt-quality-release.yml` before it syncs the plugin
to [Snowflake-Labs/cortex-code-migrations](https://github.com/Snowflake-Labs/cortex-code-migrations).
On each of the six targets, that workflow runs the Rust tests and builds with `build-plugin.sh` or
`build-plugin.ps1`. Then it packages with `package.ps1` and runs `smoke-package.ps1` and
`smoke-launcher.ps1`. When every target passes, it publishes the archives and checksums as a release
in [Snowflake-Labs/cortex-code-migrations](https://github.com/Snowflake-Labs/cortex-code-migrations/releases):

| Channel | Release tag | Example |
|---|---|---|
| stable | `dbt-quality-v<Cargo version>` | `dbt-quality-v0.3.0` |
| preview (prerelease) | `dbt-quality-v<Cargo version>-preview.<run id>` | `dbt-quality-v0.3.0-preview.18000000001` |

The sync (`plugin-use-sync-snowlabs.yml`) writes that version and the Snowflake-Labs download base
into the copied launchers. An installed plugin then downloads the binaries of its own channel. If
the release exists already and its notes name the same `ai/crates/dbt-quality` tree, the workflow
reuses it, so a plugin release without dbt-quality changes builds nothing. A release of that tag built
from other sources stops the workflow; bump the version in `dbt-quality-cli/Cargo.toml`. A draft that a failed run left stops the workflow; delete the draft and run again.

Pushes to a branch do not publish binaries, because this repository is private and the launchers
download without credentials. To test a branch, build the binary with `build-plugin.sh` or
`build-plugin.ps1`. The launcher uses the local build in `bin/<target>/` before it downloads. A pull
request that changes dbt-quality or its launchers runs the full build and smoke tests on all six
targets, and publishes nothing. To run them by hand, start **Actions -> [Plugin] dbt-quality
Release** with channel `none`.

Keep the launcher `VERSION` in `ai/plugin/bin/dbt-quality` and `dbt-quality.cmd` equal to the Cargo
version of `dbt-quality-cli`. `smoke-launcher.ps1` checks this.

### Regenerate the sample report

From the repository root, run:

```bash
cargo run --locked --manifest-path ai/Cargo.toml -p dbt-quality-core --example sample_report
```

This writes `sample-report.html` beside this README. The generator uses a clean copy of tracked
files from `ai/crates/dbt-quality/tests/fixtures/ewi_estate` and a fixed date. It records the full path of each file
in this checkout. It embeds the text of each SQL, Python, YAML, or shell file that a finding names, and
never embeds profiles or credentials. It excludes local generated artifacts. Treat the output as
synthetic test data, not as a full rule-coverage report. Do not edit it by hand. Check for drift
without changing the file (the check ignores the checkout path, so it works in any clone):

```bash
cargo run --locked --manifest-path ai/Cargo.toml -p dbt-quality-core --example sample_report -- --check
```

The native archive includes the sample so the README link works after extraction. Sample generation
needs the source checkout and Rust; viewing it does not.

### Current implementation highlights

- Duplicate sources and models are checked within and across projects, with paths and mapped
  call sites. Same-project duplicate model names are error-level findings.
- Relation reads distinguish proven producers, external inputs, and unresolved candidates.
  Configured names alone are not physical identity proof. Quoted identities and source/table
  quoting inheritance are preserved in recommended replacements.
- PRJ0022 identifies prior-state cycles and recommends downstream `is_incremental()`-guarded
  `{{ this }}` logic with a no-prior-state full-refresh branch.
- External location advice uses literal schemas and literal or `target.name`-driven databases,
  with an `invalid_database` fallback. Keep variables still needed for non-location value reads.
- Markers, waivers, CLI, and MCP behavior share the same analyzer. Rust regression tests, strict
  Clippy, catalog checks, and extracted-package smoke tests check the builds.
