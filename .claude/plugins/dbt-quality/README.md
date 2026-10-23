# dbt-quality

A local linter and MCP server for Snowflake dbt projects, including projects migrated by
SnowConvert. Its 124 rules cover project structure, relation dependencies, incremental loads,
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

The overview shows the audit scope, coverage gaps, and priority fixes. The findings view supports
search, filters, and sorting. Open a finding to read its evidence, rule guidance, and references.
Audit-wide totals and the number of findings matched by the current filters have separate labels.
Suppressed findings, skipped checks, and read errors have separate views; none count as passed checks.

The report follows the browser's color preference. Use **Auto**, **Light**, or **Dark** to change
it. Theme controls, filters, and model panels need JavaScript. Chart.js 4.4.4 loads from a pinned
jsDelivr URL with an integrity check; charts need CDN access. The code panel does not need Chart.js.
If scripts are blocked, the static findings and rule text remain readable. Embedded previews and
Snowflake's shared-report sandbox may block scripts or CDN assets; full interactive support in
those surfaces is not promised.

### View a model or edit a copy

By default, a report contains finding evidence but no complete model files. Select a local file
from a model's source panel to view it. A browser file picker cannot prove the file's original
path. If a snapshot hash is available, the report can compare the selected bytes with it. Without
a verified match, confirm the association and treat finding locations as unverified or stale.
Only findings linked to an exact discovered model offer file selection; other findings show evidence.

To include model text when you generate HTML, opt in explicitly:

```bash
ai/plugin/bin/dbt-quality audit /absolute/path/to/dbt-project \
  --out ./reports/findings.json --html ./reports/report.html --include-models
```

Create `./reports` first. `--include-models` requires `--html`. The MCP equivalent is
`include_models: true` on `report`; it cannot be combined with `html:false`. These options add
source text to HTML only, not to the normal findings JSON or the MCP response.

**Sharing an HTML report with model text also shares that source.** Even without this option,
reports contain paths and finding evidence. Review the report before sharing it. Source inclusion
is limited to discovered SQL/Python models: at most 256 KiB per file, 4 MiB total, and 100 files.
The snapshot reader rejects ambiguous ownership, symlinks, paths outside the audit/project roots,
non-model files, non-regular files, binary-like content, and invalid UTF-8. It reports omissions
instead of silently truncating files. It does not include profiles or configuration files.
These limits protect source snapshots; they do not sandbox the audit's existing file reader.

The model panel lets you edit a copy, preview changes, and download a new file or copy the text.
Downloads preserve UTF-8, a source BOM, and LF/CRLF line endings. Mixed or CR-only line endings
are read-only. Use the download when exact bytes matter; clipboard and file-picker availability
depend on the browser. The report provides a normal file-input fallback and a manual text-copy
fallback. It warns before in-report actions discard edits; do not rely on a tab-close warning.

The report never overwrites project files. Apply the downloaded changes yourself, review the diff,
run the appropriate dbt checks, then re-run the audit. Editing a copy does not resolve a finding or
update the saved report. This is a snapshot, not live linting or SQL execution.
It has no local write server. Browser file selection still needs user action and permission.

The report requests a fixed chart library, not a remote data service. Its CSP blocks data
connections, forms, frames, and objects, and it sends no referrer. Library code still runs in the
report's page context; the integrity check pins its bytes, not its access to embedded data.
Reference links open only when the reader follows them.

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

Use full rule IDs. An ignore entry waives the matching finding; it is not a fix. You can also put
`-- dbt-quality: ignore SSC-EWI-DBTSQL0006` on the reported SQL line or immediately above it, or
`-- dbt-quality: ignore-file SSC-EWI-DBTSQL0006` to waive that rule throughout the file. Configuration
also supports `disabled_rules` and thresholds; see the [rule catalog](docs/rule-catalog.md).

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

| Path | Content |
|---|---|
| `ai/crates/dbt-quality/rules/` | Metadata and schema for 124 rules in 11 packs |
| `ai/crates/dbt-quality/dbt-quality-core` | Discovery, detectors, report generation, annotations |
| `ai/crates/dbt-quality/dbt-quality-cli` | Command-line interface; `dbt-quality mcp` runs the stdio JSON-RPC MCP server |
| `ai/plugin/bin`, `ai/plugin/skills/migration/dbt-quality` | Launchers and the dbt-quality skill in the `snowflake-migration` plugin |
| `ai/crates/dbt-quality/docs/` | The generated [rule catalog](docs/rule-catalog.md) and the [HTML report specification](docs/report-spec.md) |
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
