# Oracle / DB2 / SQL Server Passthrough SQL Conversion

## When to Load

Load when SAS code contains `CONNECT TO`, `CONNECT USING`, `DISCONNECT FROM` wrappers, or `LIBNAME` with external database engines (`sqlsvr`, `oracle`, `odbc`, etc.).

---

## SQL Server (sqlsvr / ODBC) Passthrough

When SAS uses `LIBNAME lib sqlsvr dsn=...` or `CONNECT TO sqlsvr`:

**LIBNAME parsing:**
- `qualifier=` → maps to the SQL Server DATABASE name (future Snowflake DATABASE)
- `schema=` → maps to the SQL Server SCHEMA (future Snowflake SCHEMA)
- `dsn=` → data source name (connection identifier — informational only)
- `authdomain=` → authentication config (strip, not relevant for Snowflake)

**Critical:** Tables referenced via an external LIBNAME or CONNECT TO are NOT Snowflake objects. They are external source tables that will eventually be migrated. Do NOT generate Snowflake references like `DATABASE.SCHEMA.TABLE` unless the user has provided the target mapping (see Step 2.5 in SKILL.md).

**Conversion steps for SQL Server passthrough:**
1. Strip `LIBNAME`, `CONNECT TO sqlsvr`, `DISCONNECT FROM` wrappers
2. Extract the inner SQL body
3. Convert SQL Server-specific functions (see `vendor-function-mappings.md`)
4. Replace table references with user-provided Snowflake target (from Step 2.5 source mapping)
5. If no target mapping provided, use placeholder: `{TARGET_SCHEMA}.table_name`

---

## Oracle / DB2 Passthrough

When SAS uses CONNECT USING / CONNECT TO for passthrough SQL:

1. Remove CONNECT TO / DISCONNECT wrappers
2. Convert vendor-specific functions:

| Vendor Function | Snowflake Equivalent |
|----------------|---------------------|
| `DECODE(col, val1, res1, val2, res2, default)` | `CASE col WHEN val1 THEN res1 WHEN val2 THEN res2 ELSE default END` or `COALESCE` for null checks |
| `NVL(a, b)` | `COALESCE(a, b)` |
| `NVL2(a, b, c)` | `CASE WHEN a IS NOT NULL THEN b ELSE c END` |
| `TO_DATE('01/01/2024', 'DD/MM/YYYY')` | `TO_DATE('01/01/2024', 'DD/MM/YYYY')` (verify format) |
| `TO_CHAR(date, 'YYYYMMDD')` | `TO_VARCHAR(date, 'YYYYMMDD')` |
| `SYSDATE` | `CURRENT_DATE()` or `CURRENT_TIMESTAMP()` |
| `ROWNUM` | `ROW_NUMBER() OVER ()` |
| `(+)` outer join syntax | Use explicit `LEFT JOIN` / `RIGHT JOIN` |
| `SUBSTR(str, pos, len)` | `SUBSTR(str, pos, len)` (compatible) |
| `TRUNC(date)` | `DATE_TRUNC('day', date)` |
| `ADD_MONTHS(date, n)` | `DATEADD('month', n, date)` |
| `MONTHS_BETWEEN(a, b)` | `DATEDIFF('month', b, a)` |

3. Resolve table references using Step 2.5 source mapping (or placeholder if no mapping provided)
4. Convert vendor-specific date/null/string functions explicitly
5. Do NOT leave vendor-specific syntax in the output
