#!/bin/bash
# Copyright 2026 Snowflake Inc.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# SessionStart hook — installs system dependencies (uv, scai CLI). The migration
# MCP server binary ships inside the scai CLI and is launched via `scai mcp`.
# Wrapped in { ...; exit; } so bash reads the entire script into memory before
# executing, making it safe to overwrite this file during updates.

{
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLUGIN_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
mkdir -p "$PLUGIN_ROOT/logs"
LOG="$PLUGIN_ROOT/logs/install-dependencies.log"

HOOK_START=$SECONDS
log() {
  local elapsed=$(( SECONDS - HOOK_START ))
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] [${elapsed}s] $*" 2>/dev/null | tee -a "$LOG" >&2
}

VERSION=$(cat "$PLUGIN_ROOT/VERSION" 2>/dev/null | tr -d '[:space:]')
if [ -z "$VERSION" ]; then
  log "ERROR: plugin/VERSION not found or empty"
  exit 1
fi

export SCAI_CHANNEL="${SCAI_CHANNEL:-stable}"

log "SessionStart hook running (v$VERSION, plugin root: $PLUGIN_ROOT)"
log "SCAI_CHANNEL=$SCAI_CHANNEL, CORTEX_CHANNEL=${CORTEX_CHANNEL:-(not set)}"

# Optional runtime override (opt-in): pin a specific scai version via the shared
# config file. Absent config = default behavior (update to the channel's latest).
SCAI_VERSION_PIN=""
MIGRATION_CONFIG="$HOME/.snowflake/migration-plugin/config.json"
if [ -f "$MIGRATION_CONFIG" ]; then
  if command -v python3 &>/dev/null; then
    # `if VAR=$(...)` keeps `set -e` from aborting when the JSON is unparseable.
    if SCAI_VERSION_PIN=$(python3 - "$MIGRATION_CONFIG" <<'PY'
import json, sys
with open(sys.argv[1], encoding="utf-8") as f:
    cfg = json.load(f)
v = (cfg.get("scai") or {}).get("version")
print(v if isinstance(v, str) else "")
PY
    ); then
      [ -n "$SCAI_VERSION_PIN" ] && log "Config pins scai.version=$SCAI_VERSION_PIN"
    else
      SCAI_VERSION_PIN=""
      log "WARNING: could not parse $MIGRATION_CONFIG — ignoring, using default scai version"
    fi
  else
    log "WARNING: python3 not found — ignoring $MIGRATION_CONFIG, using default scai version"
  fi
fi

# System dependencies

# uv
if command -v uv &>/dev/null; then
  log "uv already installed"
else
  start=$SECONDS
  log "Installing uv..."
  curl -LsSf https://astral.sh/uv/install.sh | bash
  log "Installed uv ($(( SECONDS - start ))s)"
fi

# Remove legacy brew-based snowconvert-ai casks (replaced by scai CLI)
if command -v brew &>/dev/null; then
  LEGACY_CASKS=(snowconvert-ai snowconvert-ai-pr snowconvert-ai-dev)
  INSTALLED_CASKS=$(brew list --cask 2>/dev/null | tr '\n' ' ')
  for cask in "${LEGACY_CASKS[@]}"; do
    if [[ " $INSTALLED_CASKS " == *" $cask "* ]]; then
      start=$SECONDS
      log "Uninstalling legacy cask $cask..."
      brew uninstall --cask "$cask" 2>&1 | tee -a "$LOG" >&2 || log "Failed to uninstall $cask"
      log "Uninstalled $cask ($(( SECONDS - start ))s)"
    fi
  done
fi

# scai CLI (bundles the migration MCP server binary)
start=$SECONDS
if command -v scai &>/dev/null; then
  if [ -n "$SCAI_VERSION_PIN" ]; then
    log "scai already installed, pinning to v$SCAI_VERSION_PIN..."
    scai update "$SCAI_VERSION_PIN" 2>&1 | tee -a "$LOG" >&2 || log "scai pin to v$SCAI_VERSION_PIN failed"
    log "scai pinned to v$SCAI_VERSION_PIN ($(( SECONDS - start ))s)"
  else
    log "scai already installed, running explicit update..."
    scai update 2>&1 | tee -a "$LOG" >&2 || log "scai update failed"
    log "scai up to date ($(( SECONDS - start ))s)"
  fi
else
  log "Installing scai CLI${SCAI_VERSION_PIN:+ (pinned v$SCAI_VERSION_PIN)}..."
  # SCAI_VERSION empty = install latest; set = pin. install.sh honors it.
  curl -fsSL https://snowconvert.snowflake.com/storage/linux/prod/cli/install.sh | SCAI_VERSION="$SCAI_VERSION_PIN" bash 2>&1 | tee -a "$LOG" >&2
  log "Installed scai CLI ($(( SECONDS - start ))s)"
fi

# Disable scai auto-update (we manage updates explicitly above)
SCAI_SETTINGS="$HOME/.snowflake/scai/settings.json"
mkdir -p "$(dirname "$SCAI_SETTINGS")"
if [ ! -f "$SCAI_SETTINGS" ]; then
  echo '{}' > "$SCAI_SETTINGS"
fi
TMP_SETTINGS="${SCAI_SETTINGS}.tmp"
if grep -q '"autoUpdate"' "$SCAI_SETTINGS" 2>/dev/null; then
  sed 's/"autoUpdate"[[:space:]]*:[[:space:]]*true/"autoUpdate": false/' "$SCAI_SETTINGS" > "$TMP_SETTINGS" && mv "$TMP_SETTINGS" "$SCAI_SETTINGS"
else
  sed 's/^{$/{"autoUpdate": false,/' "$SCAI_SETTINGS" > "$TMP_SETTINGS" && mv "$TMP_SETTINGS" "$SCAI_SETTINGS"
fi

log "SessionStart hook complete (total: $(( SECONDS - HOOK_START ))s)"
exit
}
