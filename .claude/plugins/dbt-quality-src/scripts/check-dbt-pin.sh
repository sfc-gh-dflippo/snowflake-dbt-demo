#!/usr/bin/env bash
# Check that rust/ matches the pinned dbt submodule.
# Fail when the submodule HEAD differs from DBT_PIN.md, the [patch.crates-io] blocks differ,
# or the toolchain channels differ. Exit 0 when all three match.
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
vendor="$root/vendor/dbt"
status=0

# Print the [patch.crates-io] block without comments or blank lines.
patch_block() {
  awk '/^\[patch\.crates-io\]/{p=1; print; next} p && /^\[/{exit} p' "$1" |
    sed -e 's/[[:space:]]*#.*$//' -e '/^[[:space:]]*$/d'
}
channel() { sed -n 's/^channel = "\(.*\)"/\1/p' "$1"; }

pinned="$(sed -n 's/^| SHA | `\([0-9a-f]\{40\}\)` |$/\1/p' "$root/vendor/DBT_PIN.md")"
head="$(git -C "$vendor" rev-parse HEAD)"
if [[ "$pinned" != "$head" ]]; then
  echo "FAIL: vendor/dbt HEAD is $head; DBT_PIN.md pins ${pinned:-<none>}" >&2
  status=1
fi

if ! diff <(patch_block "$vendor/Cargo.toml") <(patch_block "$root/rust/Cargo.toml") >&2; then
  echo "FAIL: [patch.crates-io] in rust/Cargo.toml differs from vendor/dbt/Cargo.toml" >&2
  status=1
fi

want="$(channel "$vendor/rust-toolchain.toml")"
have="$(channel "$root/rust/rust-toolchain.toml")"
if [[ "$want" != "$have" ]]; then
  echo "FAIL: toolchain channel is $have; vendor/dbt uses $want" >&2
  status=1
fi

[[ $status -eq 0 ]] && echo "OK: rust/ matches vendor/dbt at $head"
exit $status
