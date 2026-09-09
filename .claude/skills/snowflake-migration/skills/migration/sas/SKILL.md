---
name: sas
description: Preview. SAS to Snowflake parallel migration track — assess portfolios, convert .sas programs, or load .sas7bdat from a stage. Not SnowConvert / AIM registry. Triggers: SAS, sas migration, convert SAS, assess SAS, sas7bdat, PROC SQL, DATA step, load SAS datasets.
parent_skill: migration
license: Proprietary. See License-Skills for complete terms
---

# SAS → Snowflake (parallel track)

Tell the user:
> **SAS migration track (Preview)** — assessment, code conversion, or `.sas7bdat` load. This path does not use SnowConvert or the AIM object registry.

Do **not** call `configure` or `migration_status` as a prerequisite.

## Intent routing

| User intent | Load |
|-------------|------|
| Assess / size / complexity / volume / LOE / waves / readiness | `./assess-sas-migration/SKILL.md` |
| Convert / translate / migrate SAS **programs** (DATA step, PROC, macros) | `./convert-sas-to-snowflake/SKILL.md` |
| Load / ingest **`.sas7bdat`** from a Snowflake stage | `./migrate-sas7bdat-to-snowflake/SKILL.md` |
| Validate an **existing** SAS conversion | `./convert-sas-to-snowflake/validate-sas-conversion/SKILL.md` |
| Register SAS **source** units into the Code Unit Registry (make testable) | `./register-sas-source-units/SKILL.md` |
| Attach **converted** `.sql` to the CUR so `scai test` can validate it | `./register-sas-converted-units/SKILL.md` |

If the request is only "migrate SAS" and does not distinguish code vs datasets, ask:

> Do you want to (1) convert SAS **programs** (`.sas`), or (2) load SAS **datasets** (`.sas7bdat`) from a stage?

**Wait for the user's response — do not proceed until they choose.**

Then load exactly one child skill above and follow it end-to-end.

## Notes

- Recommended code flow: Assess → Convert (Convert reuses `assessment.json` when present).
- `.sas7bdat` load is independent of Assess/Convert.
- Snowflake credit-using steps stay gated by the child skill's consent rules.
