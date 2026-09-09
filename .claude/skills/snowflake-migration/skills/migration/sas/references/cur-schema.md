# Code Unit Registry (CUR) — write contract for SAS

Single source of truth for how the SAS track writes Code Unit Registry entries so
the existing `scai test` harness (`seed` -> `capture`/`validate`) can pick them up.
The SAS track writes these JSON files **directly** (skill-side); it does **not**
register a SnowConvert dialect or touch the `.NET` `CodeUnitRegistry` engine. See
`INTEGRATION.md` for the boundary.

Grounded in two confirmed real fixtures:

- `Snowflake.SnowConvert.Testbed.Test/TestData/workloads/tbg-sales/registry/1891b321-153e-4f2a-9368-e5b8791f3a5f.json` (table)
- `testing-infrastructure/e2e/sample_data/teradata/result-sets/registry/b2c3d4e5-f6a7-8901-bcde-f12345678901.json` (procedure)

## 1. Project-root layout

`scai test` resolves a project root by the `.scai/` marker directory. The registry
is a **flat directory of `<id>.json` files** at `<root>/registry/`, a **sibling**
of `.scai/`. File paths inside each entry are **relative to the project root**.

```
<project_root>/
  .scai/              # project marker (created if absent)
  registry/           # one <uuid>.json per code unit
    <id>.json
  source/             # source .sas files (files.source.path points here)
    <...>/<name>.sas
  snowflake/          # converted .sql (files.converted.path points here)
    <...>/<name>.sql
  artifacts/          # created by `scai test`
```

For the SAS track, the project root is the conversion `<output_dir>`.

## 2. Code unit JSON schema

One `<id>.json` per unit. Fields the emitter writes (superset of the minimum `scai
test seed` needs):

```json
{
  "id": "<uuidv5 string, == filename stem>",
  "schemaVersion": 1,
  "kind": "databaseObject",
  "inScope": true,
  "isMissing": false,
  "source": {
    "canonicalName": "SAS.<NAME>",
    "name": "<NAME>",
    "objectType": "procedure|function|table|view",
    "schema": "SAS",
    "platform": "sas",
    "format": "sas"
  },
  "target": {
    "canonicalName": "<DB>.<SCHEMA>.<NAME>",
    "database": "<DB>",
    "schema": "<SCHEMA>",
    "name": "<NAME>",
    "objectType": "procedure|function|table|view",
    "format": "snowflakeSQL"
  },
  "files": {
    "source":    { "path": "source/<...>/<name>.sas", "checksum": "<md5>" },
    "converted": { "path": "snowflake/<...>/<name>.sql", "checksum": "<md5>" },
    "artifacts": { "path": "artifacts/<DB>/<SCHEMA>/<objectType>/<name>" }
  },
  "dependencies": {
    "dependsOn": [ { "id": "<dep id>", "isMissing": false, "relationTypes": ["SET"] } ],
    "requiredBy": [ "<dependent id>" ],
    "hasTransitiveMissingDependencies": false
  },
  "codeStatus": {
    "registration": { "status": "completed", "sourceId": "", "updatedAt": "<ISO>" },
    "conversion":   { "status": "completed", "converterVersion": "sas-skill", "updatedAt": "<ISO>" },
    "assessment":   { "status": "completed" }
  },
  "signature": {
    "parameters": { "arguments": [ { "name": "p_x", "type": "VARCHAR", "targetName": "p_x", "targetType": "VARCHAR", "direction": "in", "required": true, "isCursor": false } ] }
  },
  "extensions": {},
  "planning": { "topologicalRank": 0 },
  "updatedAt": "<ISO>"
}
```

Notes:
- `id` is a **UUIDv5** derived from `source.canonicalName`, so re-runs are idempotent
  and the converted-attach pass can re-find the same unit. Filename is `<id>.json`.
- `files.converted` is present only after conversion (Skill B / integrated flow).
  A source-only registration (Skill A first pass) may omit it.
- Checksums are **md5** hex of the referenced file's bytes.

## 3. What `scai test seed` requires

From `testing-infrastructure/test-seed/.../Services/CodeUnitRegistryService.cs`:

- Reads fields: `id, source, target, signature, dependencies, kind, files, parts,
  scriptBindings, scriptMetadata, cloudStatus` (absent optional fields read back null).
- **Only** seeds units whose `objectType` is one of `procedure`, `function`, `macro`.
- A unit needs a populated `target` and `files.converted.path` to be validated.

`--where` filters the CUR (same grammar as `scai code deploy --where`). SAS units
carry `source.platform = "sas"`, so `scai test seed --where "source.platform = 'sas'"`
selects them.

## 4. Unit granularity (file-level)

One code unit per **converted object**, which in the SAS 1:1 flow is **one per SAS
file** (consolidate mode: one per merged group). Rationale: conversion and
`conversion_state.json` are per file, and `dependency.py` already builds a
**file-level** cross-file graph (nodes = files, edges via shared datasets) that maps
directly onto `dependencies.dependsOn` / `requiredBy`. Blocks (from `parser.py`) are
used to classify `objectType` and derive the `signature`, not as separate units.

## 5. objectType classification

Authoritative source is the converted `.sql` when available (Skill B): scan for
`CREATE [OR REPLACE] PROCEDURE|FUNCTION|TABLE|VIEW`. Provisional fallback from the
assessment/conversion tier when converting hasn't happened yet (Skill A):

| Tier (`conversion_state.json` `files.*.tier`) | Provisional `objectType` | Seeded by `scai test`? |
|---|---|---|
| `2-SP` (stored procedure) | `procedure` | Yes |
| `1-SQL` (pure DDL/DML) | `table` (or `view`) | No |
| `3-PYSPARK` | skipped (not a SQL object) | No |

Tier-1/3 units still register as valid CUR entries (useful for the dashboard and
dependency graph); they simply do not produce `scai test` cases.

## 6. Mapping `conversion_state.json` -> CUR fields

`conversion_state.json` (see `convert-sas-to-snowflake/references/state-tracker-schema.md`)
supplies everything the converted-attach pass needs:

| CUR field | Source in `conversion_state.json` |
|---|---|
| `files.converted.path` | `files.<name>.output_file` (placed under `snowflake/`) |
| provisional `objectType` | `files.<name>.tier` |
| `dependencies` (creates/reads) | `files.<name>.dependencies.{creates,reads}` |
| `target.database` / `target.schema` | split of `metadata.target_schema` (`DB.SCHEMA`) |
| `codeStatus.conversion.status` | `completed` once `files.<name>.status == "complete"` |
