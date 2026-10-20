# dbt pin

| Field | Value |
|---|---|
| Submodule | `vendor/dbt` |
| Repository | https://github.com/dbt-labs/dbt.git |
| SHA | `be18b6572ffd2066ffb038dee5d82bbbe9cdfc1a` |
| Commit date | 2026-10-12 |
| Commit title | chore: bring 2.0.8 changelog to main and set version to 2.0.8 |
| dbt version | 2.0.8 (by the commit title and changelog) |
| Toolchain | 1.96 (`vendor/dbt/rust-toolchain.toml`) |

## Why a commit instead of a tag

At the 2026-10-13 pin review, dbt Labs built releases in the private `dbt-labs/fs` repository and
Copybara copied source into the public repository. The newest public tag found was `v2.0.5`
(`a3bdd96b`); public tags for `v2.0.6` through `v2.0.8` were not found. This public commit was
selected for its 2.0.8 changelog and title. It is a source pin, not proof that it matches the
shipped dbt 2.0.8 binary.

## Known differences from a release

- The workspace `Cargo.toml` at this commit still says `version = "2.0.5"`. Only the changelog files say 2.0.8.
- The commit has no `Cargo.lock`. Our `rust/Cargo.lock` is resolved by Cargo, not seeded from dbt.
- `crates/snowflake-rs` is absent. No vendored crate depends on `snowflake-api`.
- The code can differ from the shipped 2.0.8 build. This cannot be checked from outside dbt Labs.

## Bump procedure

1. In `vendor/dbt`, fetch and check out the new SHA, or a public `v2.x.y` tag.
2. Update the table above.
3. Copy any changed `[patch.crates-io]` lines and the toolchain channel into `rust/`.
4. Run `scripts/check-dbt-pin.sh`, the Rust tests, and the five-target CI workflow.
5. Commit the new submodule pointer in its own PR.

## Spike results (2026-10-13)

These are historical measurements from the initial investigation. Keep their dates and results
when updating the pin. In particular, `OPEN` below describes the spike's status on that date,
not the current status of a native CI target. Use the workflow for the exact commit to check
current build support.

| Spike | Result |
|---|---|
| S1: link dbt crates, static binaries | `minijinja` (dbt fork), `dbt-lexer-snowflake`, `dbt-sql-utils`, `dbt-frontend-common` and `dbt-yaml` link and build. `dbt-parser` also builds (`cargo check`, under a minute) but is not linked, see S2. `cargo tree` shows no `snowflake-api`. Linux static build: `x86_64-unknown-linux-musl` with `CC_x86_64_unknown_linux_musl=gcc` for `zstd-sys` (`scripts/build-plugin.sh` sets it). **OPEN:** `aarch64-apple-darwin` is not built yet. It needs a Mac (`scripts/build-plugin.sh aarch64-apple-darwin`). Linux musl release build: see "Build measurements". |
| S2: parse projects in process, no profile | **Failed the gate.** `dbt_parser::resolver::resolve` needs a `DbtState` from `dbt_loader::load`, which loads `profiles.yml`, and an adapter factory and Jinja factory from `dbt-compilation`. Per the plan's gate, we link only the Jinja and SQL crates, and graph rules read `target/manifest.json` from `dbt parse` (3 rules: ARC0005, MAT0001 and MAT0002, `requires_manifest: true`, the same as the Python linter). |
| S3: Jinja AST with spans | Passed. `minijinja::machinery::parse` gives the full AST with line, column and byte spans. `crate::jinja` finds `var('k','k')`, `config()` under `{% if %}` with the condition text, macro calls inside hook strings (re-parsed), `{% set %}` bindings and macro definitions. All 60 fixture files parse. |
| S4: Snowflake lexer; host rules in dbt-sql lint | Lexer passed: `dbt_sql_utils::sql_lex_tokens` tokenizes all 60 fixture files after Jinja is blanked with the Jinja tokenizer (offsets kept). The "linter like a sqlfluff" code is not in the public crates (no lint rule trait or registry), so rules use dbt-quality's own registry. |

## Build measurements (2026-10-13)

Measured with `scripts/build-plugin.sh` (release, `x86_64-unknown-linux-musl`), after `cargo test`.
These sizes and times describe that build only; later dependencies and embedded report assets
can change them.

| Target | Build time | `dbt-quality` | `dbt-quality-mcp` |
|---|---|---|---|
| `x86_64-unknown-linux-musl` | 45 s wall, 7 min 49 s CPU (clean target dir, dependencies already downloaded, 2026-10-13) | 5.6 MB | 5.2 MB |
| `aarch64-apple-darwin` | OPEN (needs a Mac) | OPEN | OPEN |

## Current native distribution

The five-target CI workflow builds Linux x86-64/ARM64, macOS Intel/Apple Silicon,
and Windows x86-64 binaries on matching runners. Artifacts are uploaded only after tests,
catalog checks where applicable, and extracted-package CLI/MCP smoke checks pass.
Use the workflow result for the exact commit as the build status.

Normal builds link the pinned Jinja parser and Rust rule engine. The SQL lexer spike is opt-in:
`cargo +1.96 run --manifest-path rust/Cargo.toml -p dbt-quality-core --example spike --features lexer-spike`.
Its optional dependencies retain the original dependency patches but do not enter normal builds.

The MCP server uses newline-delimited JSON-RPC over stdio with `serde_json`. Its integration test
covers initialization, tool discovery, report output, and annotation. Plugin binaries stay out of
Git; per-platform CI archives contain both binaries, manifests, skills, README, and checksums.
