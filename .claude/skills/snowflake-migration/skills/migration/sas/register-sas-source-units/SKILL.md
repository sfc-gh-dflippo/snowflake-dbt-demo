---
name: register-sas-source-units
parent_skill: sas
description: "Preview. Populate the Code Unit Registry (CUR) from SAS source files so the scai test harness can see them. Writes one registry/<id>.json per SAS file (source-side) into the conversion output_dir, skill-side JSON only — no SnowConvert dialect, no .NET registry engine. Triggers: register SAS units, populate CUR from SAS, add SAS to code unit registry, make SAS testable, scai test SAS, register SAS source."
license: Proprietary. See License-Skills for complete terms
---

# Register SAS Source Units into the Code Unit Registry

> © Snowflake Inc. This skill and its contents are the proprietary intellectual property of Snowflake Inc.

**Purpose:** Bridge the isolated SAS conversion track to the existing `scai test`
regression harness by writing Code Unit Registry (CUR) entries **directly as JSON**
from the SAS source files. This is the first of two registration steps; the second
(`register-sas-converted-units`) attaches the converted `.sql`.

**Boundary (do not cross):** This writes `registry/<id>.json` files only. It does
**not** register a SnowConvert source dialect, touch the `.NET` `CodeUnitRegistry`
engine, add SAS to MCP state machines, or join AIM claims/waves. See
`../INTEGRATION.md`. The contract for the JSON it writes is `../references/cur-schema.md`.

## When to use

- After (or alongside) a SAS conversion, when the user wants to run `scai test`
  (seed/validate) against the converted output.
- Automatically invoked by `convert-sas-to-snowflake` post-conversion (see that
  skill's wiring), or run standalone against an existing `.sas` corpus.

## Inputs

1. **SAS source** — a `.sas` file or a directory of them.
2. **Project root** — the SAS conversion `<output_dir>`. Gains a `.scai/` marker
   plus sibling `registry/`, `source/`, `snowflake/`, `artifacts/` dirs so
   `scai test` recognizes it as a project.
3. **Target schema** (optional) — `DB.SCHEMA` the converted objects will live in.

## Workflow

1. **Resolve the project root.** Default to the conversion `<output_dir>`. If an
   existing `.scai/` project is present elsewhere, confirm with the user before
   scaffolding a new one (do not collide with an AIM project).
2. **Run the emitter** (deterministic, stdlib-only Python — no Snowflake needed):

   ```bash
   cd ../assess-sas-migration/tool
   python3 emit_cur.py source \
     --sas <dir_or_file> \
     --project-root <output_dir> \
     --source-root <dir> \
     --target-schema DB.SCHEMA
   ```

   For each SAS file it writes one source-side unit: `source.platform = "sas"`,
   `objectType` inferred from the parsed blocks (macro/DATA-step logic ->
   `procedure`; pure table-building -> `table`), file-level dependency edges from
   the cross-file graph, and a `signature` from any `%MACRO` parameters. The
   `.sas` file is copied under `source/` and md5-checksummed.
3. **Report** the counts by objectType and note that only `procedure` / `function`
   / `macro` units will produce `scai test` cases (tables register but are not
   proc-tested). Tier-3 (PySpark) files are not SQL objects and are left for the
   converted pass to skip.
4. **Next step:** run `register-sas-converted-units` once conversion output exists
   to attach `files.converted` and confirm objectType from the generated SQL.

## Notes

- **Idempotent.** Unit ids are UUIDv5 of `SAS.<NAME>`, so re-running overwrites the
  same files rather than duplicating.
- **objectType is provisional here.** The authoritative objectType comes from the
  converted SQL in `register-sas-converted-units`; this pass uses a block heuristic
  so units are registerable before conversion completes.
- Verify entries with `scai code where` (queryable fields) and
  `scai test seed --where "source.platform = 'sas'"`.
