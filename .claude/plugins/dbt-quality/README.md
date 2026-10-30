# dbt-quality

A local linter and MCP server for Snowflake dbt projects, including projects migrated by
SnowConvert. Its 127 rules cover project structure, relation dependencies, incremental loads,
macros, SQL, materialization, tests, documentation, column contracts against scai DDL, and conversion debt.

The **CLI** serves terminal, editor, and CI checks; the **MCP server** (`dbt-quality mcp`) lets an
assistant inspect findings and propose fixes. Both use the same Rust analyzer with dbt's Jinja
parser and local SQL analysis. It reads local files only: it does not run dbt models or connect to
a warehouse. Findings are guidance to review, not automatic model rewrites.

This file is for people who build and maintain dbt-quality. To install and use it, read the
[dbt-quality README](skills/dbt-quality/README.md) that ships in the
`snowflake-migration` plugin: installation, a first audit from Cortex Code and Claude Code, the MCP
tools, the CLI, the HTML report, safe annotation, `fix-columns`, `.dbt-quality.yml` and waivers,
editor tasks, CI gating, troubleshooting, and limits. Snowflake field teams who audit SnowConvert
output for a customer start from `ai/crates/dbt-quality/FIELD_GUIDE.md` in the source repository.

| Document | Content |
|---|---|
| [dbt-quality skill](skills/dbt-quality/SKILL.md) | How the agent runs dbt-quality and when it stops for approval |
| [Rule catalog](docs/rule-catalog.md) | Every rule, generated from `rules/*.json`; the plugin ships a copy in `references/` |
| [Sample report](sample-report.html) | The HTML report on the synthetic `ewi_estate` fixture; download it if your browser shows its markup |
| [DBT_PIN.md](DBT_PIN.md) | The pinned dbt commit and build constraints |
| [Product requirements](docs/prd.md), [report specification](docs/report-spec.md) | Design |

## Try it from a source checkout

Build the binary for your machine (see [Build from source](#build-from-source)). The source
launcher `ai/plugin/bin/dbt-quality` (Windows: `bin\dbt-quality.cmd`) uses the first of
`DBT_QUALITY_EXE`, a local build in `bin/<target>/`, or a cached download, so a local build wins
over the release. Then audit the included fixture without modifying it:

```bash
ai/plugin/bin/dbt-quality audit ai/crates/dbt-quality/tests/fixtures/ewi_estate --stdout --quiet
```

To try the plugin from a branch, install it from the branch's `ai/plugin` directory:

```bash
cortex plugin install "https://github.com/snowflake-eng/migrations-snowconvert-desktop/tree/<branch>/ai/plugin"
```

A branch has no published binaries (see [Publish a release](#publish-a-release)), so build them first
or set `DBT_QUALITY_EXE`.

To find where an audit spends its time, run `audit --timings` (phases) or `audit --timings=rules`
(phases and the 10 slowest rules). Both print to stderr. See F19a in the [product requirements](docs/prd.md).

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

`dbt-quality --version` prints `dbt-quality <version> (<commit>)`. CI sets
`DBT_QUALITY_RELEASE_VERSION` (the release tag without `dbt-quality-v`, which replaces the Cargo
version) and `DBT_QUALITY_BUILD_COMMIT`. Without them, the build uses the Cargo version and the
commit from Git. With neither, the output is `dbt-quality <version>`.

| Symptom | Check |
|---|---|
| Cargo cannot fetch `minijinja` | It is a Git dependency on `dbt-labs/dbt` at the rev in [DBT_PIN.md](DBT_PIN.md). Check network access to GitHub. Resolving the `ai/` workspace also needs the private Git dependencies of the other members; see `ai/scripts/require-cargo-git-cli.sh`. |
| Native dependency build fails | Check the Rust toolchain (edition 2024), the selected target, and the native linker: musl-tools on Linux, Xcode command-line tools on macOS, or Visual Studio C++ build tools on Windows. |
| The source launcher downloads instead of using your build | Check that the binary is in `ai/plugin/bin/<target>/`; binaries there are Git-ignored. |

## Maintainer reference

Before merging a large change here (a new or reworked rule, the SQL tokenizer or Jinja reading,
discovery, waivers, levels or the report), run the `judging-dbt-quality-reports` skill
(`ai/.claude/skills/judging-dbt-quality-reports/`): it
audits snowflake-dbt-demo with and without the change and has an independent judge check the
findings.

| Path | Content |
|---|---|
| `ai/crates/dbt-quality/rules/` | Metadata and schema for 127 rules in 11 packs |
| `ai/crates/dbt-quality/dbt-quality-core` | Discovery, detectors, report generation, annotations |
| `ai/crates/dbt-quality/dbt-quality-cli` | Command-line interface; `dbt-quality mcp` runs the stdio JSON-RPC MCP server |
| `ai/plugin/bin`, `ai/plugin/skills/migration/dbt-quality` | Launchers, and the dbt-quality skill, user README and rule catalog copy in the `snowflake-migration` plugin |
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
It writes `docs/rule-catalog.md` and the plugin's copy; `check-catalog.sh` fails when either is stale.
`make dbt-quality-checks` also checks that every relative link in these docs resolves in the source
tree, in the installed plugin (a copy of `ai/plugin` alone), and in the release archive.
Build the plugin again after Rust or metadata changes.

### Publish a release

The plugin preview (`plugin-pr.yml`) and the plugin release (`plugin-release.yml`) publish the
binaries. Each one runs `.github/workflows/plugin-dbt-quality-release.yml` before it syncs the plugin
to [Snowflake-Labs/cortex-code-migrations](https://github.com/Snowflake-Labs/cortex-code-migrations).
On each of the six targets, that workflow runs the Rust tests, strict Clippy for the target, and the
catalog, pin, and sample report checks, and builds with `build-plugin.sh` or `build-plugin.ps1`. Then
it packages with `package.ps1`, which adds every third-party crate's license under `licenses/` with
`licenses/THIRD-PARTY.md` as the index, and runs `smoke-package.ps1` and `smoke-launcher.ps1`. When every target passes, it publishes the archives and checksums as a release
in [Snowflake-Labs/cortex-code-migrations](https://github.com/Snowflake-Labs/cortex-code-migrations/releases):

| Channel | Release tag | Example |
|---|---|---|
| stable | `dbt-quality-v<Cargo version>` | `dbt-quality-v0.3.0` |
| preview (prerelease) | `dbt-quality-v<Cargo version>-preview.<run id>` | `dbt-quality-v0.3.0-preview.18000000001` |

The sync (`plugin-use-sync-snowlabs.yml`) writes that version and the Snowflake-Labs download base
into the copied launchers. An installed plugin then downloads the binaries of its own channel. If
the release exists already and its notes name the same dbt-quality sources (the `ai/crates/dbt-quality`
tree, and dbt-quality's part of `ai/Cargo.lock` and `ai/Cargo.toml`), the workflow reuses it, so a
plugin release without dbt-quality changes builds nothing. A preview reuses the last preview of the
same Cargo version and sources in the same way. A release of that tag built
from other sources stops the workflow; bump the version in `dbt-quality-cli/Cargo.toml`. A draft that a failed run left stops the workflow; delete the draft and run again.
A published or reused release must download without a token, pass its checksums and be immutable, or
the workflow fails before the sync, so a rerun never ships a release that failed that check.

Pushes to a branch do not publish binaries, because this repository is private and the launchers
download without credentials. To test a branch, build the binary with `build-plugin.sh` or
`build-plugin.ps1`. The launcher uses the local build in `bin/<target>/` before it downloads. A pull
request with the `ready_to_merge` label that changes dbt-quality, its launchers, or `ai/Cargo.lock`
runs the full build and smoke tests on all six targets, and publishes nothing. It fails when its
Cargo version is already published from other sources: bump the version. To run them by hand, start **Actions -> [Plugin] dbt-quality
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
