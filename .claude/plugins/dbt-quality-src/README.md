# dbt-quality

A local linter and MCP server for Snowflake dbt projects, including projects migrated by
SnowConvert. Its 124 rules cover project structure, relation dependencies, incremental loads,
macros, SQL, materialization, tests, documentation, column contracts against scai DDL, and conversion debt.

Use the **CLI** for terminal, editor, and CI checks. Use the **MCP server** to let an assistant
inspect findings and propose fixes. Both use the same Rust analyzer with dbt's Jinja parser and
local SQL analysis. The analyzer reads local files; it does not run dbt models or connect
to a warehouse. Findings are guidance to review, not automatic model rewrites.

## Quick start

### 1. Download a release

Releases are in the private `snowflake-eng/migrations-ai-skills` repository, so you need access
to that repository and the [GitHub CLI](https://cli.github.com/) logged in (`gh auth login`).
CI attaches each archive to the release only after that target's tests and extracted-package
smoke checks pass.

| Machine | Target |
|---|---|
| Linux Intel/AMD 64-bit | `x86_64-unknown-linux-musl` |
| Linux ARM64 | `aarch64-unknown-linux-musl` |
| macOS Intel | `x86_64-apple-darwin` |
| macOS Apple Silicon | `aarch64-apple-darwin` |
| Windows Intel/AMD 64-bit | `x86_64-pc-windows-msvc` |

Linux and macOS (set `TARGET` from the table):

```bash
TARGET=aarch64-apple-darwin
gh release download --repo snowflake-eng/migrations-ai-skills \
  --pattern "dbt-quality-$TARGET.tar.gz*" \
  "$(gh release list --repo snowflake-eng/migrations-ai-skills --json tagName \
      --jq '[.[] | select(.tagName | startswith("dbt-quality-v"))][0].tagName')"
shasum -a 256 -c "dbt-quality-$TARGET.tar.gz.sha256"
tar -xzf "dbt-quality-$TARGET.tar.gz"
cd "dbt-quality-$TARGET"
```

Windows PowerShell:

```powershell
$Repo = 'snowflake-eng/migrations-ai-skills'
$Tag = gh release list --repo $Repo --json tagName --jq '[.[] | select(.tagName | startswith("dbt-quality-v"))][0].tagName'
gh release download $Tag --repo $Repo --pattern 'dbt-quality-x86_64-pc-windows-msvc.zip*'
Expand-Archive dbt-quality-x86_64-pc-windows-msvc.zip -DestinationPath .
Set-Location dbt-quality-x86_64-pc-windows-msvc
```

The repository holds other releases too, so the commands pick the newest tag that starts with
`dbt-quality-v`. To pin a version, use the tag directly, for example `dbt-quality-v0.2.0`.
Compare the `.sha256` file with `Get-FileHash` on Windows. Keep the extracted directory intact:
it contains `bin/`, plugin manifests, skills, this README, and `SHA256SUMS`. Unix archives keep
executable bits.

The two programs are native executables: **no Rust, Python, uv, Node, or WASM runtime is required**
for users. Git is required for annotation's clean-tree safeguard and Git-aware checks.
macOS and Windows binaries are unsigned. To test an unreleased commit, download the same
archives from a successful **Actions -> dbt-quality native binaries** run; those artifacts expire
after 30 days.

From the extracted directory:

```bash
# Linux/macOS
bin/dbt-quality --version
bin/dbt-quality audit /absolute/path/to/dbt-project --stdout --quiet
```

```powershell
# Windows PowerShell
.\bin\dbt-quality.exe --version
.\bin\dbt-quality.exe audit C:\work\dbt-project --stdout --quiet
```

On Linux, verify the archive with `sha256sum -c <archive>.sha256`; on macOS use
`shasum -a 256 -c <archive>.sha256`. On Windows compare `Get-FileHash <archive>.zip -Algorithm SHA256`
with the adjacent checksum file. The inner `SHA256SUMS` also lists each executable's digest.

### 2. Audit a project or estate

The examples below use the **source checkout's** `plugin/bin/dbt-quality` launcher. In an extracted
release archive, use `bin/dbt-quality` (Windows: `.\bin\dbt-quality.exe`) instead.

The plugin launchers, `plugin/bin/dbt-quality` and `plugin/bin/dbt-quality.cmd` (Windows), use the first of:
`DBT_QUALITY_EXE`, a local build in `plugin/bin/<target>/`, or a cached download. Otherwise they
download the release archive for their `VERSION` from the public
[snowflake-dbt-demo releases](https://github.com/sfc-gh-dflippo/snowflake-dbt-demo/releases), check
its SHA-256, and cache the binary in `~/.cache/dbt-quality/` (`%LOCALAPPDATA%\dbt-quality\` on
Windows). Set `DBT_QUALITY_DOWNLOAD_BASE` to use a different release location. The checksum comes
from the same release, so it detects a corrupt download. Those releases are immutable; to check a
release's origin, run `gh release verify-asset <tag> <archive> -R sfc-gh-dflippo/snowflake-dbt-demo`.

From a built source checkout, try the included fixture without modifying it:

```bash
plugin/bin/dbt-quality audit rust/tests/fixtures/ewi_estate --stdout --quiet
```

For your own project, replace `/absolute/path/to/dbt-project` with its directory. To detect
cross-project collisions, use the **parent directory containing all the projects**.

```bash
# JSON on stdout; no report files or project edits.
plugin/bin/dbt-quality audit /absolute/path/to/dbt-project --stdout --quiet

# Save JSON and HTML outside the project. Create the output directory first.
mkdir -p ./reports
plugin/bin/dbt-quality audit /absolute/path/to/dbt-project \
  --out ./reports/findings.json --html ./reports/report.html

# Editor-style diagnostics, or structured lint records.
plugin/bin/dbt-quality lint /absolute/path/to/dbt-project
plugin/bin/dbt-quality lint /absolute/path/to/dbt-project --format json
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
plugin/bin/dbt-quality audit /absolute/path/to/dbt-project \
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
update the saved report. This is a snapshot, not live linting, SQL execution, or a WASM validator.
It has no local write server. Browser file selection still needs user action and permission;
WASM would not remove that requirement.

The report requests a fixed chart library, not a remote data service. Its CSP blocks data
connections, forms, frames, and objects, and it sends no referrer. Library code still runs in the
report's page context; the integrity check pins its bytes, not its access to embedded data.
Reference links open only when the reader follows them.

## Connect the MCP server

Choose **one** connection method to avoid registering the server twice. Download a release or
build the binary first. Use absolute paths. No API key or Snowflake credentials are needed by
this local server. The server is the `mcp` subcommand of `dbt-quality`. On Windows, point
directly to `bin/dbt-quality.exe` with the argument `mcp`.

### Cortex Code: plugin and skills

The release archive includes the MCP server plus `dbt-audit` and `dbt-validate` skills. From its extracted
root, validate it and start a Cortex Code session:

```bash
cortex plugin validate "$PWD"
cortex --workdir /absolute/path/to/dbt-project --plugin-dir "$PWD"
```

```powershell
cortex plugin validate "$PWD"
cortex --workdir C:\work\dbt-project --plugin-dir "$PWD"
```

For a source checkout, use its built `plugin/` directory instead of the extracted root.

In the session, use `/mcp` to inspect the connection. Ask:

> Use dbt-quality to audit this project and show the highest-priority findings. Do not edit files.

The packaged manifests also target Claude Code. CI validates the local CLI and stdio protocol on
each target; full interactive client integration remains a separate check.

### Cortex Code: MCP server only

Register the executable directly if you want the tools without the plugin skills:

```bash
cortex mcp add --transport stdio dbt-quality /absolute/path/to/extracted/dbt-quality/bin/dbt-quality mcp
cortex mcp get dbt-quality
cortex mcp list
```

```powershell
cortex mcp add --transport stdio dbt-quality "C:\tools\dbt-quality\bin\dbt-quality.exe" mcp
```

Restart the client or reconnect after registration. In Cortex Code, use `/mcp` or
`cortex mcp reconnect dbt-quality`. To remove a direct registration, use
`cortex mcp remove dbt-quality`.

### Other stdio MCP clients

For clients using an `mcpServers` configuration, merge this entry into their configuration,
keeping other servers intact. File locations and reload steps depend on the client.

```json
{
  "mcpServers": {
    "dbt-quality": {
      "type": "stdio",
      "command": "/absolute/path/to/extracted/dbt-quality/bin/dbt-quality",
      "args": ["mcp"]
    }
  }
}
```

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
plugin/bin/dbt-quality rules --code SSC-EWI-DBTPRJ0020
plugin/bin/dbt-quality annotate /absolute/path/to/dbt-project
# After reviewing the diff, with a clean Git tree:
plugin/bin/dbt-quality annotate /absolute/path/to/dbt-project --write
# Remove only dbt-quality markers; preview by omitting --write.
plugin/bin/dbt-quality annotate /absolute/path/to/dbt-project --remove --write
```

Use repeatable `--rule <full-code>` arguments (MCP: `rule_ids`) to scope annotation. `--allow-dirty`
(MCP: `allow_dirty:true`) overrides the clean-tree safeguard; use it deliberately, not by default.
Markers leave SnowConvert's original diagnostics intact. A finding that only reports an existing
converter marker (MIG0001, MIG0002, MIG0003) counts in the report but gets no second marker, so
`annotate` does not duplicate SnowConvert EWI or FDM markers. Without intervening edits, annotation
followed by removal restores the input bytes. Removal does not undo code fixes you made.

For the detailed agent workflow, see [dbt-audit](../dbt-quality/skills/dbt-audit/SKILL.md).

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
plugin/bin/dbt-quality lint /path/to/dbt-project --ddl /path/to/scai-project
plugin/bin/dbt-quality fix-columns /path/to/dbt-project --ddl /path/to/scai-project   # diff only
plugin/bin/dbt-quality fix-columns /path/to/dbt-project --ddl /path/to/scai-project --write
```

Without a catalog, a column type is known only from an outer `CAST`, `TRY_CAST`, or `::`. A column
with no cast is reported as "no explicit cast".

## Editor and CI usage

Install VS Code task definitions for an individual dbt project:

```bash
plugin/bin/dbt-quality setup-tasks /absolute/path/to/dbt-project
```

This writes `.vscode/tasks.json`, retaining existing tasks and adding missing task labels. It
requires valid JSON, not JSON-with-comments. Run **dbt: quality suggestions** from the editor's
Tasks menu; findings appear in Problems. The second task runs every five minutes and requests
folder-open startup, subject to the editor's task trust/approval settings.

For CI, build or provision the binaries first, then use:

```bash
plugin/bin/dbt-quality lint /absolute/path/to/dbt-project --strict
# Or save a report while gating on error-level findings:
plugin/bin/dbt-quality audit /absolute/path/to/dbt-project \
  --stdout --quiet --fail-on-error > findings.json
```

Default audit/lint success does not mean no findings. `audit --fail-on-error`, `lint --strict`, and
`validate --strict` fail on active **error-level** findings; warnings do not fail these checks.
Command or I/O errors may also return nonzero. `lint` returns success when it finds no projects,
so verify your CI root; `audit` reports that condition as an error.

Other useful commands:

```bash
plugin/bin/dbt-quality validate /absolute/path/to/dbt-project/models/orders.sql
plugin/bin/dbt-quality audit /absolute/path/to/dbt-project \
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
`TST`, `DOC`, `MAT`, `ARC`, `OPS`, `MIG`); `kind`, diagnostic `level`, and impact `severity` are
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
also supports `disabled_rules` and thresholds; see the [rule catalog](../dbt-quality/skills/dbt-audit/references/rule-catalog.md).

## Troubleshooting and limits

| Symptom | Check |
|---|---|
| Source launcher says it cannot download | The launcher prints the URL. Check network access to GitHub, set `DBT_QUALITY_DOWNLOAD_BASE`, or build with the platform's `scripts/build-plugin.sh` or `scripts/build-plugin.ps1`; binaries are Git-ignored. |
| Cargo cannot find a vendored crate | Initialize the pinned `vendor/dbt` submodule from the repository root. |
| Native dependency build fails | Check Rust 1.96, the selected target, and the native linker: musl-tools on Linux, Xcode command-line tools on macOS, or Visual Studio C++ build tools on Windows. |
| MCP server fails to start or shows no tools | Test the downloaded `bin/dbt-quality` (Windows: `bin/dbt-quality.exe`) with `--version`, check the absolute MCP command path and execute permission, then inspect the client's MCP logs/reconnect. No HTTP URL is involved. |
| No projects or missing cross-project findings | Point at a directory containing `dbt_project.yml`; choose the common estate parent for cross-project analysis. |
| Checks are skipped | Inspect `skipped_checks`. Each entry gives the reason: the rule is disabled in `.dbt-quality.yml`, or `validate` cannot run a project-scoped rule on one file. |
| Annotation refuses to write | Commit or stash project changes first, including dirty nested repositories; review the dry-run diff. |
| An ignored rule still appears | Check its full code and project/audit-root-relative path, and which nearest config file was loaded. |

The linter performs static analysis. Custom naming macros and unresolved locations can prevent
physical producer matching; follow the confirmation steps rather than guessing. Review suggested
SQL changes and run your dbt tests before adopting them. Some cross-rule SQL/macro advice overlaps
remain. Only release archives, or CI artifacts from successful target jobs, are validated builds. Full interactive editor
integration and `dbt_external_tables` compatibility with native `EXECUTE DBT PROJECT` remain unverified.

## Build from source

Developers need Git, Rustup with Rust 1.96, and the platform's native linker/toolchain. Linux CI
uses native x86-64/ARM64 runners with musl-tools; macOS uses Xcode command-line tools; Windows
uses Visual Studio C++ build tools. Initial Cargo downloads need network access. Python and uv
are not part of the build or test workflow.

From the repository root:

```bash
git submodule update --init --depth 1 experimentals/dflippo/dbt-quality/vendor/dbt
cd experimentals/dflippo/dbt-quality
rustup toolchain install 1.96 --profile minimal --component clippy
rustup target add --toolchain 1.96 x86_64-unknown-linux-musl
scripts/build-plugin.sh x86_64-unknown-linux-musl
```

Select the matching target from the table above; build macOS binaries on macOS and Windows on
Windows. The scripts do not install cross-linkers or claim cross-compilation from any host.
On Windows, after initializing the submodule:

```powershell
Set-Location experimentals/dflippo/dbt-quality
rustup toolchain install 1.96 --profile minimal --component clippy
rustup target add --toolchain 1.96 x86_64-pc-windows-msvc
.\scripts\build-plugin.ps1
.\plugin\bin\x86_64-pc-windows-msvc\dbt-quality.exe --version
```

PowerShell 7 (`pwsh`) drives archive packaging and extracted-package smoke tests on CI; it is not
needed to run downloaded binaries. The optional `lexer-spike` Cargo feature enables the standalone
Snowflake lexer experiment and its larger dependency graph. Ordinary builds keep those dependencies
inactive and retain all linter rules.

## WASM portability

Native binaries are the supported distribution. A WASI module could eventually share one artifact
across platforms, but would still need a runtime such as Wasmtime and explicitly granted filesystem
access. This code has not been built or tested for WASM. Git subprocesses used for annotation safety
and tracked-file checks need a host integration or replacement; disabling those safeguards is not
a portable substitute. Browser WASM additionally needs a different file-access interface.

See [Rust WASI](https://doc.rust-lang.org/rustc/platform-support/wasm32-wasip1.html) and
[Wasmtime CLI](https://docs.wasmtime.dev/cli-options.html) for runtime constraints. A future WASI
spike should begin with read-only auditing and verify dependencies, filesystem access, and stdio
before adding writes.

## Maintainer reference

| Path | Content |
|---|---|
| `rules/` | Metadata and schema for 124 rules in 11 packs |
| `rust/crates/dbt-quality-core` | Discovery, detectors, report generation, annotations |
| `rust/crates/dbt-quality-cli` | Command-line interface; `dbt-quality mcp` runs the stdio JSON-RPC MCP server |
| `plugin/` | Client manifests, launchers, and audit/validation skills |
| `vendor/dbt`, [DBT_PIN.md](vendor/DBT_PIN.md) | Pinned parser/lexer source and build constraints |
| `scripts/` | Native builds, packaging, artifact smoke tests, catalog and pin checks |

Run these from the `dbt-quality` directory:

```bash
cargo +1.96 test --manifest-path rust/Cargo.toml --workspace
cargo +1.96 clippy --manifest-path rust/Cargo.toml --workspace --all-targets -- -D warnings
RUSTUP_TOOLCHAIN=1.96 scripts/check-catalog.sh
```

After changing rule metadata, regenerate the catalog with
`RUSTUP_TOOLCHAIN=1.96 scripts/build-catalog.sh`. Keep the dbt submodule and Rust patches aligned
with `scripts/check-dbt-pin.sh`. Build the plugin again after Rust or metadata changes.

### Publish a release

1. Set the new version in `[workspace.package]` of `rust/Cargo.toml`, run the tests, and merge.
2. Tag the merged commit with `dbt-quality-v<version>` and push the tag:

   ```bash
   git tag dbt-quality-v0.2.0 <commit>
   git push origin dbt-quality-v0.2.0
   ```

The `dbt-quality release` workflow stops if the tag does not match the Cargo version. It then
runs the full build workflow, and creates the GitHub Release only when all five targets pass
their tests and smoke checks. The release holds those exact archives and their `.sha256` files.
To remove a bad release, delete the release and its tag; do not move a published tag.

### Regenerate the sample report

From the `dbt-quality` source directory, run:

```bash
cargo +1.96 run --locked --manifest-path rust/Cargo.toml -p dbt-quality-core --example sample_report
```

This writes `sample-report.html` beside this README. The generator uses a clean copy of tracked
files from `rust/tests/fixtures/ewi_estate` and a fixed date. It records the full path of each file
in this checkout. It embeds the text of each SQL, Python, YAML, or shell file that a finding names, and
never embeds profiles or credentials. It excludes local generated artifacts. Treat the output as
synthetic test data, not as a full rule-coverage report. Do not edit it by hand. Check for drift
without changing the file (the check ignores the checkout path, so it works in any clone):

```bash
cargo +1.96 run --locked --manifest-path rust/Cargo.toml -p dbt-quality-core --example sample_report -- --check
```

The native archive includes the sample so the README link works after extraction. Sample generation
needs the source checkout and Rust; viewing it does not. Browser-test tooling under `tests/browser`
is for development only. It is not a dependency of the downloaded executables.

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
  Clippy, catalog checks, and extracted-package smoke tests protect each platform build.
