#!/usr/bin/env bash
# Build the producer to a fixed, in-repo path so a caller can point
# AIFIRST_EMITTER at something this repo just built, instead of a POC bin someone hand-rsynced
# from a one-off /tmp staging directory.
#
# WHAT THIS DOES NOT DO. It does not build the engine (migrations-snowconvert). It assumes that
# repo is already built at least once (`dotnet build` there, or CI having done it) -- this
# project's whole dependency shape is "reference the closed set of assemblies a real engine build
# already produced", and rebuilding the engine here would be a second, much slower way to get the
# same bin/Debug/net10.0 directory the engine's own build already leaves behind.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG="${1:-Debug}"

if [[ -z "${AIFIRST_ENGINE_BIN:-}" ]]; then
  echo "build.sh: set AIFIRST_ENGINE_BIN to an existing SnowConvert engine bin directory" >&2
  exit 2
fi
if [[ ! -d "$AIFIRST_ENGINE_BIN" ]]; then
  echo "build.sh: AIFIRST_ENGINE_BIN does not exist: $AIFIRST_ENGINE_BIN" >&2
  exit 2
fi

dotnet build "$HERE/CallableMigrator.csproj" -c "$CONFIG"

OUT="$HERE/bin/$CONFIG/net10.0/aifirst-migrate.dll"
if [ ! -f "$OUT" ]; then
  echo "build.sh: expected $OUT after a successful build and did not find it" >&2
  exit 1
fi

echo ""
echo "built: $OUT"
echo "run:   export AIFIRST_EMITTER=\"$OUT\""
