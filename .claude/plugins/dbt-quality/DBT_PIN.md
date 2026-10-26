# dbt pin

| Field | Value |
|---|---|
| Dependency | `minijinja` in `ai/crates/dbt-quality/dbt-quality-core/Cargo.toml` (Cargo Git dependency) |
| Repository | https://github.com/dbt-labs/dbt |
| SHA | `be18b6572ffd2066ffb038dee5d82bbbe9cdfc1a` |
| Commit date | 2026-10-12 |
| Commit title | chore: bring 2.0.8 changelog to main and set version to 2.0.8 |
| dbt version | 2.0.8 (by the commit title and changelog) |
| sqlparser patch | `[patch.crates-io]` in `ai/Cargo.toml`, equal to dbt's own at this SHA |

## Why a commit instead of a tag

At the 2026-10-13 pin review, dbt Labs built releases in the private `dbt-labs/fs` repository and
Copybara copied source into the public repository. The newest public tag found was `v2.0.5`
(`a3bdd96b`); public tags for `v2.0.6` through `v2.0.8` were not found. This public commit was
selected for its 2.0.8 changelog and title. It is a source pin, not proof that it matches the
shipped dbt 2.0.8 binary.

## Known differences from a release

- The workspace `Cargo.toml` at this commit still says `version = "2.0.5"`. Only the changelog files say 2.0.8.
- The commit has no `Cargo.lock`. `ai/Cargo.lock` is resolved by Cargo, not seeded from dbt.
- The code can differ from the shipped 2.0.8 build. This cannot be checked from outside dbt Labs.

## What is pinned

Three crates are built from the dbt repository: its `minijinja` fork, that fork's in-repo
`minijinja-typecheck-builtins` dependency, and `dbt-lexer-snowflake` (see SQL lexer below).
Cargo fetches the dbt repository at the SHA above; `ai/Cargo.lock` records the same SHA. dbt's
workspace patches are not inherited by dependents, so `ai/Cargo.toml` carries the one patch the
analyzer needs: the sdf-labs `sqlparser` 0.58 fork used for DDL parsing. It applies only to
`^0.58` requirements, so other `ai/` crates keep their own `sqlparser`. dbt's other patches
(`ring`, arrow, datafusion) are deliberately not copied: in a shared workspace they would replace
those crates for every member.

## Bump procedure

1. Update the SHA and dbt version in the table above, the `rev` of `minijinja` and of
   `dbt-lexer-snowflake` in `ai/crates/dbt-quality/dbt-quality-core/Cargo.toml`, and `DBT_PIN_SHA` and `DBT_PIN_VERSION` in
   `ai/crates/dbt-quality/dbt-quality-core/src/lib.rs`.
2. Run `cargo update -p minijinja` from `ai/`, and check that only dbt-quality entries change in `ai/Cargo.lock`.
3. If dbt's `[patch.crates-io]` `sqlparser` line changed, copy it into `ai/Cargo.toml`.
4. Run `ai/crates/dbt-quality/scripts/check-dbt-pin.sh`, the Rust tests, and the native package checks.
5. Commit the pin change in its own PR.

## SQLFluff-style suppression comments

`dbt-quality-core/src/waivers.rs` parses `-- noqa`, `-- noqa: CODE`, `-- noqa-file`,
`-- noqa: disable=|enable=CODE`, and dbt-quality's own `-- sqlfluff:disable|enable` range form. No dbt crate is added. The dbt file that parses these comments,
`crates/dbt-frontend-common/src/fix.rs`, does not exist at the pinned SHA, so nothing is ported
from dbt. The parser is an independent implementation of the SQLFluff comment syntax
(Apache-2.0-compatible, original code).

## SQL lexer

`dbt-quality-core/Cargo.toml` takes two more crates for `sqlutil::tokenize`:

| Crate | Source | Licence |
|---|---|---|
| `dbt-lexer-snowflake` | Git dependency on the same SHA as `minijinja` | Apache-2.0 |
| `dbt-antlr4` 2.0.3 | crates.io | BSD-3-Clause |

`dbt-quality-core` asks for default features of both. The lexer's own manifest inherits dbt's
workspace `dbt-antlr4` dependency, which enables `arena-allocation-limit` and `recursion-limit`
(with `stacker`), so the resolved build has them on; `cargo tree -p dbt-quality-core -e features
-i dbt-antlr4` from `ai/` shows it. These features bound ANTLR parsing; dbt-quality runs only the
lexer. The `[patch]` blocks of dbt are not needed. `check-dbt-pin.sh` checks that the lexer `rev` equals the pin. A bump of the SHA changes
both `rev` values.
