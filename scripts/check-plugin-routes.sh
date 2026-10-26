#!/bin/sh
# Check plugin layout and skill routes. Run from any directory.
root=$(cd "$(dirname "$0")/.." && pwd)
plug="$root/.claude/plugins"
mine="$plug/snowflake-dbt-migration"
fail=0
# Rule 1: each <plugin>:<skill> id must name an existing SKILL.md.
ids=$(find "$mine" -name '*.md' -exec grep -oh '`\(dbt\|snowflake\)[a-z0-9-]*:[a-z0-9-]\+`' {} + | tr -d '`' | sort -u)
for id in $ids; do
  p=${id%%:*}; s=${id#*:}
  [ -f "$plug/$p/skills/$s/SKILL.md" ] || { echo "FAIL: unknown skill id $id"; fail=1; }
done
# Rule 2: commands/ dirs are deprecated.
for d in $(find "$plug" -type d -name commands); do echo "FAIL: deprecated dir $d"; fail=1; done
# Rule 3: each SKILL.md needs name and description frontmatter.
for f in $(find "$mine" -name SKILL.md); do
  fm=$(sed -n '2,/^---$/p' "$f")
  for k in name description; do
    echo "$fm" | grep -q "^$k:" || { echo "FAIL: $f lacks $k:"; fail=1; }
  done
done
[ $fail -eq 0 ] && echo "OK: plugin routes valid"
exit $fail
