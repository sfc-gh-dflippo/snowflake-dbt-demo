#!/bin/sh
# Regenerates <plugin>/skills/dbt-audit/references/rule-catalog.md from rules/*.json.
set -e
cd "$(dirname "$0")/.."
catalog=${DBT_QUALITY_PLUGIN_DIR:-plugin}/skills/dbt-audit/references/rule-catalog.md
(cd rust && cargo run -q -p dbt-quality-cli -- rules --format markdown) > "$catalog"
echo "wrote $catalog"
