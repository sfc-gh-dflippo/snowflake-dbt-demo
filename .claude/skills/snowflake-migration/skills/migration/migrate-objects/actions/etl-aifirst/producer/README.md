# AI-first callable producer

This source-only .NET project adapts the existing SnowConvert engine assemblies to the AI-first
desktop migration driver. It does not contain or rebuild the engine.

## Build

Set `AIFIRST_ENGINE_BIN` to an existing engine output containing the runtime DLL closure, then run:

```bash
AIFIRST_ENGINE_BIN=/path/to/engine/bin/Debug/net10.0 ./build.sh
```

Pass `Release` as the first argument for a release build. Output is always written under this
directory at `bin/<Config>/net10.0/aifirst-migrate.dll`. `-p:EngineBin=...` is also supported when
invoking `dotnet build` directly.

## Use

```bash
export AIFIRST_EMITTER="$PWD/bin/Debug/net10.0/aifirst-migrate.dll"
bash ../scripts/aifirst-migrate.sh <platform-table.json> <source-document> <output-root>
```

The producer records the source platform in assessment reports, emits SSIS instrumentation only for
SSIS inputs, and preserves platform-derived model/reference names.
