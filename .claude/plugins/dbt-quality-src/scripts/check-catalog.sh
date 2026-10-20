#!/bin/sh
# Fails when the committed rule catalog differs from a fresh generation.
set -e
cd "$(dirname "$0")/.."
committed=${DBT_QUALITY_PLUGIN_DIR:-plugin}/skills/dbt-audit/references/rule-catalog.md
fresh=$(mktemp)
(cd rust && cargo run -q -p dbt-quality-cli -- rules --format markdown) > "$fresh"
if ! diff -u "$committed" "$fresh"; then
  echo "rule-catalog.md is stale: run scripts/build-catalog.sh and commit it" >&2
  rm -f "$fresh"; exit 1
fi
rm -f "$fresh"; echo "rule-catalog.md is current"
