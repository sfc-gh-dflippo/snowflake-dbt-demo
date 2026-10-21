#!/bin/sh
# Copies dbt-quality from a migrations-ai-skills checkout into the snowflake-dbt-demo layout:
#   <upstream>/plugin/   -> .claude/plugins/dbt-quality/      (plugin root)
#   everything else      -> .claude/plugins/dbt-quality-src/  (this tree)
# It copies only the files that git tracks upstream and deletes copies that upstream no longer
# tracks. It keeps local builds (bin/<target>/, rust/target/) and the vendor/dbt submodule, and
# checks out the submodule commit that the upstream vendor/DBT_PIN.md names. It does not commit.
set -eu
src=$(CDPATH= cd -- "${1:?usage: $0 <migrations-ai-skills>/experimentals/dflippo/dbt-quality}" && pwd)
dest=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
case "$dest" in
  */.claude/plugins/dbt-quality-src) ;;
  *) echo "Run this script from the snowflake-dbt-demo copy, not from $dest." >&2; exit 1 ;;
esac
if [ ! -f "$src/rust/Cargo.toml" ] || [ ! -d "$src/plugin" ]; then
  echo "$src is not a dbt-quality source tree." >&2; exit 1
fi
plugin="$(dirname -- "$dest")/dbt-quality"
tracked=$(mktemp) present=$(mktemp)
trap 'rm -f "$tracked" "$present"' EXIT
git -C "$src" ls-files | grep -v '^vendor/dbt$' | sort > "$tracked"

mkdir -p "$plugin"
grep '^plugin/' "$tracked" | sed 's#^plugin/##' | rsync -a --files-from=- "$src/plugin/" "$plugin/"
grep -v '^plugin/' "$tracked" | rsync -a --files-from=- "$src/" "$dest/"
{
  (cd "$plugin" && find . -type f ! -path './bin/*/*' | sed 's#^\./#plugin/#')
  (cd "$dest" && find . -type f ! -path './vendor/dbt/*' ! -path './rust/target/*' ! -path '*/node_modules/*' | sed 's#^\./##')
} | sort > "$present"
comm -13 "$tracked" "$present" | while IFS= read -r stale; do
  case "$stale" in
    plugin/*) rm -f "$plugin/${stale#plugin/}" ;;
    *) rm -f "$dest/$stale" ;;
  esac
done
find "$plugin" "$dest" -type d -empty ! -path "$dest/vendor/*" -delete

# Upstream README links point into plugin/; here the plugin root is a sibling directory.
sed 's#](plugin/#](../dbt-quality/#g' "$dest/README.md" > "$dest/README.md.tmp"
mv "$dest/README.md.tmp" "$dest/README.md"

sha=$(sed -n 's/^| SHA | `\([0-9a-f]\{40\}\)` |$/\1/p' "$src/vendor/DBT_PIN.md")
if [ -e "$dest/vendor/dbt/.git" ]; then
  git -C "$dest/vendor/dbt" fetch -q --depth 1 origin "$sha"
  git -C "$dest/vendor/dbt" checkout -q "$sha"
else
  echo "vendor/dbt is not initialized. Run: git submodule update --init, then rerun this script." >&2
fi
git -C "$dest" status --short -- "$dest" "$plugin"

# Ignore rules in the demo repo (for example profiles.yml) would silently leave copied files untracked.
ignored=$( {
  grep '^plugin/' "$tracked" | sed "s#^plugin/#$plugin/#"
  grep -v '^plugin/' "$tracked" | sed "s#^#$dest/#"
} | git -C "$dest" check-ignore --no-index --stdin || true)
if [ -n "$ignored" ]; then
  echo "These copied files are ignored by the demo repo; add negation rules to .claude/plugins/.gitignore:" >&2
  echo "$ignored" >&2
  exit 1
fi
