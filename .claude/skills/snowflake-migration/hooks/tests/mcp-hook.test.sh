#!/usr/bin/env sh
set -eu

script_dir="$(cd "$(dirname "$0")" && pwd)"
hook="$script_dir/../mcp-hook.sh"
test_root="$(mktemp -d)"
trap 'rm -rf "$test_root"' EXIT

fail() {
  echo "FAIL: $1" >&2
  exit 1
}

# Cortex hooks run with cwd = the project. Isolate so the cache file never
# lands in the repo.
project="$test_root/project"
mkdir -p "$project"
cd "$project"
cache="$project/.scai/tmp/mcp-server-bin"

clear_cache() {
  rm -rf "$project/.scai"
}

bin="$test_root/migration-mcp-server"
printf '%s\n' '#!/bin/sh' 'echo "BIN=$0"' 'echo "ARGS=$*"' >"$bin"
chmod +x "$bin"

mkdir -p "$test_root/bin" "$test_root/orch"

# Env pin wins over everything else, and records the path for later hooks.
other="$test_root/other-mcp"
cp "$bin" "$other"
chmod +x "$other"
clear_cache
out=$(MIGRATION_MCP_SERVER_BIN="$other" sh "$hook" stamp-agent-id </dev/null)
printf '%s\n' "$out" | grep -Fq "BIN=$other" || fail "env pin ignored: $out"
printf '%s\n' "$out" | grep -Fq "ARGS=hook stamp-agent-id" || fail "argv: $out"
[ -f "$cache" ] || fail "env pin did not write cache"
grep -Fxq "$other" "$cache" || fail "cache contents: $(cat "$cache")"

# Production: scai symlink next to the rust binary.
ln -s "$bin" "$test_root/orch/migration-mcp-server"
ln -s "$test_root/orch/scai-apphost" "$test_root/bin/scai"
printf '%s\n' '#!/bin/sh' 'echo apphost' >"$test_root/orch/scai-apphost"
chmod +x "$test_root/orch/scai-apphost"
# sibling of the symlink target (apphost) is orch/migration-mcp-server
clear_cache
out=$(
  env -u MIGRATION_MCP_SERVER_BIN -u SCAI_CLI PATH="$test_root/bin:$PATH" \
    sh "$hook" stamp-agent-id </dev/null
)
printf '%s\n' "$out" | grep -Fq "BIN=$test_root/orch/migration-mcp-server" \
  || fail "symlink sibling missed: $out"
grep -Fxq "$test_root/orch/migration-mcp-server" "$cache" \
  || fail "locate did not cache sibling: $(cat "$cache")"

# Cached path is used even when scai is gone from PATH.
out=$(
  env -u MIGRATION_MCP_SERVER_BIN -u SCAI_CLI PATH="/usr/bin:/bin" \
    sh "$hook" stamp-agent-id </dev/null
) || fail "cache hit must exit 0"
printf '%s\n' "$out" | grep -Fq "BIN=$test_root/orch/migration-mcp-server" \
  || fail "cache hit missed: $out"

# Stale cache falls back to locate and is rewritten.
printf '%s\n' "/no/such/migration-mcp-server" >"$cache"
out=$(
  env -u MIGRATION_MCP_SERVER_BIN -u SCAI_CLI PATH="$test_root/bin:$PATH" \
    sh "$hook" stamp-agent-id </dev/null
)
printf '%s\n' "$out" | grep -Fq "BIN=$test_root/orch/migration-mcp-server" \
  || fail "stale cache did not fall back: $out"
grep -Fxq "$test_root/orch/migration-mcp-server" "$cache" \
  || fail "stale cache was not rewritten: $(cat "$cache")"

# make-temp wrapper: export MIGRATION_MCP_SERVER_BIN, exec elsewhere.
wrapper="$test_root/wrapper-scai"
printf '%s\n' \
  '#!/usr/bin/env bash' \
  "export MIGRATION_MCP_SERVER_BIN=\"$other\"" \
  'exec /no/such/scai "$@"' \
  >"$wrapper"
chmod +x "$wrapper"
clear_cache
out=$(
  env -u MIGRATION_MCP_SERVER_BIN SCAI_CLI="$wrapper" PATH="$test_root/bin:$PATH" \
    sh "$hook" agent-ledger </dev/null
)
printf '%s\n' "$out" | grep -Fq "BIN=$other" || fail "wrapper export missed: $out"
printf '%s\n' "$out" | grep -Fq "ARGS=hook agent-ledger" || fail "wrapper argv: $out"

# No scai yet (first session): silent success, not a Cortex hook failure.
clear_cache
out=$(
  env -u MIGRATION_MCP_SERVER_BIN -u SCAI_CLI PATH="/usr/bin:/bin" \
    sh "$hook" session-context </dev/null
) || fail "missing scai must exit 0"
[ -z "$out" ] || fail "missing scai must be silent, got: $out"
[ ! -f "$cache" ] || fail "skip must not write a cache"

echo "mcp-hook.sh tests passed"
