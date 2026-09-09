# Troubleshooting Guide

## All Tests Return 0 Rows

**Symptoms:** Every test case returns 0 actual rows when baseline has data.

**Possible causes:**

1. **Wrong schema prefix**
   - Check procedure calls use the correct schema prefix for the target environment
   - Verify the procedure was deployed with the expected prefix

2. **Missing base data**
   - Query the source tables directly to verify data exists:
   ```sql
   SELECT COUNT(*) FROM <SCHEMA>.TableName WHERE <filter>;
   ```

3. **Filter too restrictive**
   - Compare WHERE clauses between source and Snowflake target
   - Check date range parameters — timezone adjustments may exclude all data

4. **Missing dependency**
   - Check if the procedure calls another procedure that returns empty
   - Look for `CALL` statements and verify those procedures work

**Debug steps:**
```sql
-- Run procedure manually with same parameters
CALL <PREFIX><SCHEMA>.ProcedureName(param1 => value1, param2 => value2);

-- Check parameters from test case
SELECT parameters FROM VALIDATION.BASELINES 
WHERE code_unit_name = '<SCHEMA>.Name' AND params_hash = '<hash>';
```

## ERROR: Function/Procedure Not Found

**Symptoms:** `SQL compilation error: Unknown function` or similar.

**Fix:**
1. Find the missing function in the converted output:
   ```bash
   find snowflake/ -iname "*functionname*" -type f
   ```

2. Deploy it first:
   ```bash
   scai code deploy -c <CONNECTION_NAME> --where "source.canonicalName ILIKE '%<functionname>%'" --json
   ```

3. Then re-run the procedure's tests.

## ERROR: Table/View Not Found

**Symptoms:** `Object does not exist` error.

**Fix:**
1. Check if the object exists in Snowflake:
   ```sql
   SHOW TABLES LIKE '%tablename%' IN SCHEMA <SCHEMA>;
   SHOW VIEWS LIKE '%viewname%' IN SCHEMA <SCHEMA>;
   ```

2. If missing, deploy it:
   ```bash
   scai code deploy -c <CONNECTION_NAME> --where "source.canonicalName ILIKE '%<objectname>%'" --json
   ```

## Missing Schema Prefix (DBO and others)

**Symptoms:** Runtime error like `Object 'TABLENAME' does not exist`, or the deployed procedure compiles but every test returns 0 rows / fails against an unqualified name that exists under a specific schema.

**Cause:** SnowConvert and CoCo frequently drop the source schema qualifier (most often `dbo.`, but also `RPT.`, `MD.`, `PUBLIC.`, etc.) on tables, views, and user-defined functions. Snowflake requires an explicit schema just like SQL Server does, so the unqualified reference resolves incorrectly or not at all.

**Rule:** Every table, view, and function reference from the source must keep its schema prefix in the converted output. Schema prefixes other than `dbo` must also be preserved exactly as they appear in the source.

**Audit checklist.** Before accepting a converted procedure, scan every SQL object reference against the source:

1. Collect every `FROM`, `JOIN`, `INSERT INTO`, `UPDATE`, `MERGE INTO`, and function-call reference in the converted file.
2. Cross-check each against the source SQL. If the source has `dbo.X`, the converted output must have `dbo.X` — not just `X`.
3. Restore the schema prefix on any unqualified name (e.g., `Package`, `InventorySnapshot`, `tbl_LspLocations`).
4. After restoration, do a final grep-style pass across the file for bare table names from the source that still appear without a prefix.

**Common failure patterns:**

| Broken (CoCo output) | Correct |
|---|---|
| `FROM Package p` | `FROM dbo.Package p` |
| `FROM InventorySnapshot` | `FROM dbo.InventorySnapshot` |
| `FROM tbl_LspLocations` | `FROM dbo.tbl_LspLocations` |
| `JOIN AllocatedInventory ai` | `JOIN dbo.AllocatedInventory ai` |
| `INSERT INTO ReceiveInventoryHistory` | `INSERT INTO dbo.ReceiveInventoryHistory` |
| `dbo.myFunction(x)` | `dbo.myFunction(x)` (already qualified — do not change) |

## ERROR: Invalid Identifier

**Symptoms:** `invalid identifier 'COLUMNNAME'`

**Possible causes:**

1. **Column name case mismatch**
   - Snowflake uppercases unquoted identifiers
   - Check if column should be quoted: `"columnName"` vs `COLUMNNAME`

2. **Column doesn't exist**
   - Verify column exists in the table:
   ```sql
   DESC TABLE <SCHEMA>.TableName;
   ```

3. **Typo in column name**
   - Compare against source database code

4. **Dynamic PIVOT column names have quotes**
   - If error shows `invalid identifier '"ColumnName"'` with mixed quotes
   - This indicates PIVOT column naming issue
   - See "Hardcoded PIVOT Columns" section below

## Hardcoded PIVOT Columns

**Symptoms:** `invalid identifier 'G.MEDICAL'`, `invalid identifier '"Medical"'`, or similar errors referencing columns produced by a `PIVOT` clause.

**Cause:** In Snowflake, a static `PIVOT` with string literals in `IN(...)` creates output column names that **include the surrounding single quotes as part of the name**. The single quotes are not SQL delimiters — they are literal characters in the resulting column identifier.

```sql
-- Source PIVOT:
PIVOT(SUM(amount) FOR customerType IN('Medical', 'Recreational - Tax Exempt', 'Caregiver'))
-- Creates columns named:  'Medical'   'Recreational - Tax Exempt'   'Caregiver'
--   (the single quotes are PART OF the column name, not SQL delimiters)
```

**Rule:** Reference every PIVOT output column with double quotes wrapping the full name **including the embedded single quotes**.

```sql
-- WRONG:
g.medical                          -- unquoted — fails
g."Medical"                        -- missing embedded single quotes — fails
g."Recreational - Tax Exempt"      -- missing embedded single quotes — fails

-- CORRECT:
g."'Medical'"
g."'Recreational - Tax Exempt'"
g."'Caregiver'"
```

Apply this to every PIVOT column reference (SELECT list, `NVL`, `CASE`, aliases, etc.) in the converted procedure.

## All Rows Show as Different

**Symptoms:** Row counts match but every row shows as `missing_in_actual` and `extra_in_actual`.

**Possible causes:**

1. **Column ordering differs**
   - The comparison may be order-sensitive
   - Check SELECT list matches baseline column order

2. **Column name case**
   - Baseline may have `ColumnName`, actual has `COLUMNNAME`
   - Use aliases to match: `SELECT col AS "ColumnName"`

3. **Data type formatting**
   - Numbers: `1000` vs `1E+3`
   - Dates: `2024-01-01` vs `2024-01-01T00:00:00`
   - These may be normalization issues

## Small Row Count Differences

**Symptoms:** Baseline has 43 rows, actual has 45 (or similar small difference).

**Debug steps:**

1. **Find the extra/missing rows:**
   ```sql
   SELECT differences FROM VALIDATION.LATEST
   WHERE UPPER(procedure_name) = UPPER('RPT.Name') AND params_hash = 'abc123';
   ```

2. **Check for filter differences:**
   - Compare WHERE clauses in source vs Snowflake
   - Look for: `IS NOT NULL`, status filters, date ranges

3. **Check for data drift:**
   - Query source tables with the test parameters
   - Compare against baseline capture date if known

## Decimal/Rounding Differences

**Symptoms:** Values like `11.336666` vs `11.336667` (1 in last digit).

**Cause:** Some source databases (e.g., SQL Server) use banker's rounding, Snowflake uses standard rounding.

**Resolution:**
- If difference is always ≤1 in the last decimal place, use `MANUAL_PASS`
- Flag for normalization if this affects many procedures
- Consider reducing precision in the cast if business doesn't need 6 decimals

## Timestamp Differences

**Symptoms:** Dates off by hours, or different precision.

**Common causes:**

1. **Timezone offset**
   - Source GETDATE()/GETDATE()-equivalent may be in local time
   - Snowflake CURRENT_TIMESTAMP() may be UTC
   - Check timezone adjustment functions

2. **Precision differences**
   - Source: `2024-01-22 00:00:00`
   - Snowflake: `2024-01-22T00:00:00.000000`
   - May be formatting issue (flag for normalization)

## Connection Errors

**Symptoms:** Cannot connect to Snowflake.

**Fix:**
1. Verify connection config:
   ```bash
   snow connection test -c <CONNECTION_NAME>
   ```

2. Check `~/.snowflake/connections.toml` has correct settings

3. If using key-pair auth, verify private key path and permissions:
   ```bash
   ls -la ~/.ssh/rsa_key.p8
   ```

4. **Entra ID / OIDC:** `externalbrowser` is SAML SSO, not OIDC. Use
   `authenticator = "oauth_authorization_code"` with `user`, client id/secret,
   both HTTPS endpoints, `oauth_scope`, and a **fixed** loopback
   `oauth_redirect_uri` registered exactly in Entra. See
   `../connection/snowflake-connection/SKILL.md` and
   `Snowflake.SnowConvertDesktop/Snowflake.SnowConvert.Cli/docs/entra-oidc-oauth.md`.
   Headless/CI cannot complete this flow — switch to PAT or key-pair. Data
   validation and test generation do not support Authorization Code (`CNX0037`).

## Test Runner Errors

**Symptoms:** `scai test capture` or `scai test validate` fails.

**Fix:**
1. Verify a scai project is initialized:
   ```bash
   scai project info --json
   ```

2. Verify test YAML files exist:
   ```bash
   ls <project_dir>/artifacts/**/test/*.yml
   ```

3. Verify the Snowflake connection works:
   ```bash
   snow connection test -c <CONNECTION_NAME>
   ```

4. Verify the source connection works:
   ```bash
   scai connection test -l <sqlserver|redshift> -c <CONNECTION_NAME> --json
   ```

## Deploy Errors

**Symptoms:** Deployment fails with syntax error.

**Debug:**
1. Read the SQL file and check for obvious syntax issues:
   ```bash
   # View the file that failed
   cat snowflake/<type>/<schema>/<objectname>.sql
   ```

2. Check for Snowflake-incompatible syntax in the file

3. Look for SnowConvert EWI comments (`--** SSC-`) that indicate unresolved conversion issues

4. Try deploying directly to see the full error:
   ```bash
   scai code deploy -c <CONNECTION_NAME> --where "source.canonicalName ILIKE '%<objectname>%'" --json
```
