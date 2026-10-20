#!/bin/sh
# Build dbt-quality for the selected targets and install it beside the launcher.
set -eu
root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
# The plugin root. The snowflake-dbt-demo copy keeps it outside this tree.
plugin=${DBT_QUALITY_PLUGIN_DIR:-$root/plugin}
toolchain=${RUSTUP_TOOLCHAIN:-1.96}
if [ "$#" -eq 0 ]; then
  host=$(rustup run "$toolchain" rustc -vV | sed -n 's/^host: //p')
  case "$host" in *-unknown-linux-gnu) host=${host%-gnu}-musl ;; esac
  set -- "$host"
fi
for target in "$@"; do
  case "$target" in
    x86_64-unknown-linux-musl|aarch64-unknown-linux-musl|x86_64-apple-darwin|aarch64-apple-darwin) ;;
    *) printf 'Unsupported Unix target: %s\nUse build-plugin.ps1 for Windows.\n' "$target" >&2; exit 1 ;;
  esac
  cargo "+$toolchain" build --locked --release --manifest-path "$root/rust/Cargo.toml" \
    --target "$target" -p dbt-quality-cli
  destination="$plugin/bin/$target"
  mkdir -p "$destination"
  cp "$root/rust/target/$target/release/dbt-quality" "$destination/dbt-quality"
  chmod +x "$destination/dbt-quality"
  printf 'Built %s in %s\n' "$target" "$destination"
done
