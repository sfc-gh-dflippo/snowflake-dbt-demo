#!/bin/sh
# Copyright 2026 Snowflake Inc.
# SPDX-License-Identifier: Apache-2.0
#
# Locate migration-mcp-server (ships next to scai, not on PATH) and exec
# `hook <name>`. Must not start the .NET scai apphost — PreToolUse cannot
# pay CLR startup (~130ms).
#
# After the first successful locate, the absolute path is written to
# `$PWD/.scai/tmp/mcp-server-bin` so later hooks skip PATH / wrapper work.
# Cortex command hooks run with cwd = the project.

set -eu

name="${1:-}"
[ -n "$name" ] || {
  echo "usage: mcp-hook.sh <hook-name>" >&2
  exit 2
}

# First session (and any host without scai on PATH): do not fail the Cortex
# hook. SessionStart installs scai; later turns find it.
skip() {
  exit 0
}

# Follow one symlink. Production install.sh points ~/.local/bin/scai at the
# orchestrator apphost; `readlink -f` is GNU-only.
resolve_path() {
  target=$1
  if [ -L "$target" ]; then
    linked=$(readlink "$target")
    case "$linked" in
      /*) target=$linked ;;
      *) target="$(dirname "$target")/$linked" ;;
    esac
  fi
  printf '%s\n' "$target"
}

# install.sh only chmod +x's `scai`. The rust sibling is usually +x from
# the archive; if extract dropped the bit, recover it (user-owned install).
ensure_exec() {
  path=$1
  [ -f "$path" ] || return 1
  [ -x "$path" ] || chmod u+x "$path" 2>/dev/null || return 1
  [ -x "$path" ]
}

sibling_of() {
  dir=$(dirname "$1")
  for name in migration-mcp-server.exe migration-mcp-server; do
    if ensure_exec "$dir/$name"; then
      printf '%s\n' "$dir/$name"
      return 0
    fi
  done
}

# make-temp / wave-runs wrapper: export or exec line names the real binary.
bin_from_wrapper() {
  script=$1
  [ -f "$script" ] || return 0
  wrapped=$(sed -n 's/^export MIGRATION_MCP_SERVER_BIN="\([^"]*\)".*/\1/p' "$script" | tail -n 1)
  if [ -n "$wrapped" ] && ensure_exec "$wrapped"; then
    printf '%s\n' "$wrapped"
    return 0
  fi
  exec_line=$(sed -n 's/^exec "\([^"]*\)".*/\1/p' "$script" | tail -n 1)
  if [ -n "$exec_line" ]; then
    sibling_of "$exec_line"
  fi
}

cache="${PWD:-.}/.scai/tmp/mcp-server-bin"

read_cache() {
  [ -f "$cache" ] || return 1
  path=$(sed -n '1s/[[:space:]]*$//p' "$cache")
  [ -n "$path" ] && ensure_exec "$path" && printf '%s\n' "$path"
}

write_cache() {
  path=$1
  mkdir -p "$(dirname "$cache")" 2>/dev/null || return 0
  printf '%s\n' "$path" >"$cache" 2>/dev/null || true
}

if [ -n "${MIGRATION_MCP_SERVER_BIN:-}" ] && ensure_exec "$MIGRATION_MCP_SERVER_BIN"; then
  bin=$MIGRATION_MCP_SERVER_BIN
else
  bin=$(read_cache || true)
  if [ -z "$bin" ]; then
    scai=${SCAI_CLI:-}
    if [ -z "$scai" ]; then
      scai=$(command -v scai) || skip
    fi
    [ -n "$scai" ] || skip
    bin=$(bin_from_wrapper "$scai" || true)
    if [ -z "$bin" ]; then
      bin=$(sibling_of "$(resolve_path "$scai")" || true)
    fi
    [ -n "$bin" ] && [ -x "$bin" ] || skip
  fi
fi

write_cache "$bin"
exec "$bin" hook "$name"
