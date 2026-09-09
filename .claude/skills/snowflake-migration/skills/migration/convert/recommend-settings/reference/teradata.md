# Teradata conversion-setting hints

Signal → setting mappings. Grep `source/` for each signal; if found, consider the setting.
Only propose settings that appear in the `scai code convert --list-settings --json` catalog for this project.

| Signal (grep in source/) | Setting (`--longName`) | Proposed | Why |
|---|---|---|---|
| `PERIOD(` datatype in DDL | `--splitperioddatatype` | enable | Snowflake has no PERIOD type; split into begin/end DATE-TIME columns. |
| `.bteq` files, or BTEQ dot-commands (`.LOGON`, `.EXPORT`, `.IMPORT`, `.RUN`, `.LABEL`) | `--scripttargetlanguage` | `Python` or `SnowScript` | Choose the target for BTEQ scripts. Default SnowScript; pick Python if the shop prefers Python orchestration. |
| `CREATE MACRO`, `CREATE PROCEDURE`, `REPLACE PROCEDURE` | `--pltargetlanguage` | `SnowScript` | Target language for procedures/macros. SnowScript is the modern default; JavaScript only if the team relies on it. |
| `DELETE <table> ALL`, `DELETE ALL` | `--replacedeletealltotruncate` | enable | Turn "delete all rows" into TRUNCATE for performance parity. |
| `CASESPECIFIC`, `NOT CASESPECIFIC`, or comparisons that assume case-insensitive behavior | `--sessionMode` | `Tera` or `Ansi` | TERA vs ANSI changes default character-comparison case sensitivity. Match the source's session mode. |
| Heavy case-insensitive string comparisons where COLLATE would be generated | `--disableCollateForCaseSpecification` | enable | Use UPPER/RTRIM instead of COLLATE for case-insensitive comparisons. |
| Many databases used as schema containers (multiple `DATABASE ` prefixes) | `--displacedatabaseasschema` (with `--customschema`) | enable | Displace Teradata databases from becoming Snowflake schemas. Requires `-s/--customschema`. |
| `CREATE JOIN INDEX`, materialized views | `--warehouse` | `<WAREHOUSE_NAME>` | Materialized views become Dynamic Tables; set the refresh warehouse (default is a placeholder). |
| Non-ISO date/time literals (e.g. `'YYYY/MM/DD'` formats) | `--defaultdateformat` / `--defaulttimeformat` / `--defaulttimestampformat` | matching format | Set default DATE/TIME/TIMESTAMP formats to match the source data. |
| Implicit CHAR→number conversions | `--charactertoapproximatenumber` | integer 0–37 | Controls the CHARACTER→approximate-number transformation length. |

Notes:
- When a signal is ambiguous (e.g. session mode), surface it as a question rather than guessing.
- Re-check each candidate against the catalog's `options`/`min`/`max` before proposing a value.
