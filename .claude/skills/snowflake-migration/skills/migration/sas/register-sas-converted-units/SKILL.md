---
name: register-sas-converted-units
parent_skill: sas
description: "Preview. Attach converted Snowflake SQL to existing SAS Code Unit Registry entries so scai test can validate them. Reads conversion_state.json, sets files.converted + confirms objectType from the generated SQL, stamps codeStatus.conversion. Skill-side JSON only — no SnowConvert dialect, no .NET registry engine. Triggers: attach converted SAS SQL, register converted SAS, complete SAS CUR, make converted SAS testable, scai test SAS validate."
license: Proprietary. See License-Skills for complete terms
---

# Register Converted SAS SQL into the Code Unit Registry

> © Snowflake Inc. This skill and its contents are the proprietary intellectual property of Snowflake Inc.

**Purpose:** The second of two registration steps. After `register-sas-source-units`
has written source-side CUR entries, this attaches each converted `.sql` file
(`files.converted`), confirms the `objectType` from the generated SQL, and stamps
`codeStatus.conversion` — so `scai test seed`/`validate` can run against the SAS
conversion in Snowflake self-consistency mode.

**Boundary (do not cross):** Writes/updates `registry/<id>.json` only. No
SnowConvert dialect, no `.NET` `CodeUnitRegistry` engine, no MCP state machines,
no AIM claims/waves. See `../INTEGRATION.md`; contract in `../references/cur-schema.md`.

## When to use

- After a SAS conversion has produced `.sql` output and its
  `conversion_state.json` marks files `complete`.
- Invoked automatically by `convert-sas-to-snowflake` post-conversion, or run
  standalone.

## Inputs

1. **Project root** — the SAS conversion `<output_dir>` (already registered by
   `register-sas-source-units`).
2. **conversion_state.json** (optional path) — defaults to
   `<project-root>/conversion_state.json`. Supplies, per file: `output_file`
   (the converted `.sql`), `tier`, and `dependencies`.

## Workflow

1. **Ensure source units exist.** If `registry/` is empty, run
   `register-sas-source-units` first (this pass updates existing entries; it does
   not create them).
2. **Run the emitter:**

   ```bash
   cd ../assess-sas-migration/tool
   python3 emit_cur.py converted \
     --project-root <output_dir> \
     --state <path/to/conversion_state.json>
   ```

   For each file with `status == "complete"` (and not a `3-PYSPARK` tier), it:
   - locates `output_file`, copies it under `snowflake/`, md5-checksums it, and
     sets `files.converted.path` (root-relative);
   - reads the converted SQL and sets the authoritative `objectType` from
     `CREATE [OR REPLACE] PROCEDURE|FUNCTION|TABLE|VIEW` (falling back to the tier
     mapping if the pattern is absent);
   - fills `target.database`/`target.schema` from `metadata.target_schema`;
   - stamps `codeStatus.conversion.status = "completed"`.
3. **Report** attached counts and which units are now `procedure`/`function`
   (seedable) vs `table`/`view` (registered but not proc-tested).
4. **Run the harness (self-consistency):** see `../convert-sas-to-snowflake/workflows/scai-test-selfconsistency.md`.
   In short: `scai test seed --where "source.platform = 'sas'"` then
   `scai test validate` against Snowflake. Note: `scai test capture` from a source
   system is **not applicable** to SAS — the baseline is the converted code's own
   stable Snowflake run (or the convert skill's validation expected-outputs).

## Notes

- **Idempotent.** Re-running re-attaches to the same UUIDv5 units.
- Units whose source was never registered are skipped without error (run Skill A
  first). PySpark (Tier 3) units remain source-only — they are not SQL objects.
