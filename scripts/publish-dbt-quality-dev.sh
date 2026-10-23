#!/bin/sh
# Republishes a development build of the dbt-quality plugin to this repository.
#
# Input: the CI artifacts of one "[Plugin] dbt-quality Release" run in the monorepo.
# It does these steps:
#   1. Find the latest successful run for --pr, or use --run.
#   2. Download the 6 platform archives and check each SHA-256.
#   3. Replace .claude/plugins/dbt-quality with the plugin package from the archive.
#      Take the launchers from the run's commit.
#   4. Point the launchers at this repository's releases and set VERSION from --tag.
#   5. With --publish: commit, push, create the release, and test a first-use download.
# Without --publish it stops after step 4 and leaves the changes uncommitted.
#
# Usage: scripts/publish-dbt-quality-dev.sh --tag dbt-quality-v0.3.1-pr9528 (--pr 9528 | --run ID) [--publish]
# Needs: gh (signed in, read access to the source repo), git, tar, sha256sum or shasum.
set -eu

src_repo=snowflake-eng/migrations-snowconvert-desktop
workflow=plugin-dbt-quality-release.yml
targets="x86_64-unknown-linux-musl aarch64-unknown-linux-musl x86_64-apple-darwin aarch64-apple-darwin x86_64-pc-windows-msvc aarch64-pc-windows-msvc"
pr= run= tag= publish=

die() { echo "publish-dbt-quality-dev: $*" >&2; exit 1; }
while [ $# -gt 0 ]; do
  case "$1" in
    --pr) pr=${2:?}; shift 2 ;;
    --run) run=${2:?}; shift 2 ;;
    --tag) tag=${2:?}; shift 2 ;;
    --source-repo) src_repo=${2:?}; shift 2 ;;
    --publish) publish=1; shift ;;
    *) die "unknown argument $1 (see the usage line at the top of this script)" ;;
  esac
done
case "$tag" in dbt-quality-v?*) ;; *) die "--tag must look like dbt-quality-v<version>" ;; esac
[ -n "$pr$run" ] || die "give --pr or --run"
version=${tag#dbt-quality-v}

root=$(git -C "$(dirname -- "$0")" rev-parse --show-toplevel)
plugin="$root/.claude/plugins/dbt-quality"
cd "$root"
# gh hangs on an open stdin in some shells, so every gh call reads /dev/null.
this_repo=$(gh repo view --json nameWithOwner -q .nameWithOwner </dev/null)
if gh release view "$tag" -R "$this_repo" >/dev/null 2>&1 </dev/null; then
  die "release $tag exists in $this_repo; releases are immutable, so pick a new tag"
fi
if [ -n "$(git status --porcelain -- "$plugin" .claude-plugin)" ]; then
  die "uncommitted changes in $plugin or .claude-plugin; commit or discard them first"
fi
if command -v sha256sum >/dev/null; then sha_check="sha256sum -c"; else sha_check="shasum -a 256 -c"; fi

# 1. Resolve the run and its commit.
if [ -z "$run" ]; then
  sha=$(gh pr view "$pr" -R "$src_repo" --json headRefOid -q .headRefOid </dev/null)
  run=$(gh run list -R "$src_repo" --workflow "$workflow" --commit "$sha" --status success \
    --limit 1 --json databaseId -q '.[0].databaseId' </dev/null)
  [ -n "$run" ] || die "no successful $workflow run for PR $pr head $sha; push to the PR and wait for CI"
fi
sha=$(gh run view "$run" -R "$src_repo" --json headSha -q .headSha </dev/null)
echo "Run $run, commit $sha"

# 2. Download and verify every archive.
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
gh run download "$run" -R "$src_repo" -p 'dbt-quality-*' -D "$work/dl" </dev/null
mkdir "$work/dist"
find "$work/dl" -type f -exec mv {} "$work/dist/" \;
for t in $targets; do
  case $t in *windows*) a="dbt-quality-$t.zip" ;; *) a="dbt-quality-$t.tar.gz" ;; esac
  [ -f "$work/dist/$a" ] && [ -f "$work/dist/$a.sha256" ] || die "run $run has no $a"
done
(cd "$work/dist" && $sha_check ./*.sha256)

# 3. Replace the plugin. The package in each archive is the same apart from bin/; use the Linux x64 one.
tar xzf "$work/dist/dbt-quality-x86_64-unknown-linux-musl.tar.gz" -C "$work"
pkg="$work/dbt-quality-x86_64-unknown-linux-musl"
# Keep the plugin's .gitignore and .gitattributes. Plugin paths have no spaces.
git ls-files -- "$plugin" | grep -v -e '/\.gitignore$' -e '/\.gitattributes$' | while read -r f; do rm -f "$f"; done
find "$plugin" -type d -empty -delete
(cd "$pkg" && tar cf - --exclude=./bin --exclude=./SHA256SUMS .) | (mkdir -p "$plugin" && cd "$plugin" && tar xf -)
mkdir -p "$plugin/bin"
for f in dbt-quality dbt-quality.cmd; do
  # The .cmd can arrive with LF line ends. The plugin .gitattributes checks it out with CRLF.
  gh api -H 'Accept: application/vnd.github.raw' "repos/$src_repo/contents/ai/plugin/bin/$f?ref=$sha" \
    </dev/null >"$work/$f"
done

# 4. Point the launchers at this repository and set the versions.
base="https://github.com/$this_repo/releases/download"
LC_ALL=C sed -e "s/^VERSION=.*/VERSION=$version/" \
  -e "s#https://github.com/[^}\"]*/releases/download#$base#" "$work/dbt-quality" >"$plugin/bin/dbt-quality"
# '"' ends each match, so a CR at the line end is kept.
LC_ALL=C sed -e "s/set \"VERSION=[^\"]*\"/set \"VERSION=$version\"/" \
  -e "s#https://github.com/[^\"]*/releases/download#$base#" "$work/dbt-quality.cmd" >"$plugin/bin/dbt-quality.cmd"
chmod +x "$plugin/bin/dbt-quality"
grep -q "^VERSION=$version\$" "$plugin/bin/dbt-quality" || die "could not set VERSION in bin/dbt-quality"
grep -q "set \"VERSION=$version\"" "$plugin/bin/dbt-quality.cmd" || die "could not set VERSION in bin/dbt-quality.cmd"
grep -q "$base" "$plugin/bin/dbt-quality" && grep -q "$base" "$plugin/bin/dbt-quality.cmd" \
  || die "could not set the download base in the launchers"
for m in "$plugin/.claude-plugin/plugin.json" "$plugin/.cortex-plugin/plugin.json"; do
  sed "s/\"version\": \"[^\"]*\"/\"version\": \"$version\"/" "$m" >"$work/m" && mv "$work/m" "$m"
done
# Change only the version line of the dbt-quality entry in the marketplace.
sed "/\"name\": \"dbt-quality\"/,/\"version\"/s/\"version\": \"[^\"]*\"/\"version\": \"$version\"/" \
  .claude-plugin/marketplace.json >"$work/m" && mv "$work/m" .claude-plugin/marketplace.json
git status --short -- "$plugin" .claude-plugin

if [ -z "$publish" ]; then
  echo "Staged $tag from run $run. Check the diff, then run again with --publish."
  exit 0
fi

# 5. Commit, push, and publish. The release is immutable, so attach assets to a draft, then publish it.
git add -A -- "$plugin" .claude-plugin/marketplace.json
git commit -m "chore(dbt-quality): publish development build $tag

Binaries and plugin package from $src_repo run $run (commit $sha)."
git push origin HEAD </dev/null
target=$(git rev-parse HEAD)
gh release create "$tag" "$work"/dist/* -R "$this_repo" --draft --prerelease --target "$target" --title "$tag" \
  --notes "Development build of dbt-quality from $src_repo commit $sha, CI run $run. Not an official release. macOS and Windows binaries are unsigned." </dev/null
gh release edit "$tag" -R "$this_repo" --draft=false </dev/null

# Test a first-use download through the launcher with an empty cache.
XDG_CACHE_HOME="$work/cache" "$plugin/bin/dbt-quality" --version
echo "Published $tag."
