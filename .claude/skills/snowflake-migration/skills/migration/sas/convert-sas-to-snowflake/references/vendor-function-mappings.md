# Oracle / DB2 / SQL Server Passthrough Function Mappings

## When to Load

Load when SAS code contains `CONNECT TO`, `CONNECT USING`, or `DISCONNECT FROM` wrappers, or `LIBNAME` with external database engines (`sqlsvr`, `oracle`, `odbc`, etc.).

---

When converting SAS CONNECT TO / CONNECT USING passthrough SQL:

### Oracle → Snowflake

| Oracle Function | Snowflake Equivalent | Notes |
|----------------|---------------------|-------|
| `DECODE(col, v1, r1, v2, r2, def)` | `CASE col WHEN v1 THEN r1 WHEN v2 THEN r2 ELSE def END` | Or `COALESCE` for null-check pattern |
| `NVL(a, b)` | `COALESCE(a, b)` | |
| `NVL2(a, b, c)` | `CASE WHEN a IS NOT NULL THEN b ELSE c END` | |
| `SYSDATE` | `CURRENT_DATE()` or `CURRENT_TIMESTAMP()` | |
| `SYSTIMESTAMP` | `CURRENT_TIMESTAMP()` | |
| `ROWNUM` | `ROW_NUMBER() OVER ()` | |
| `TO_CHAR(date, 'YYYYMMDD')` | `TO_VARCHAR(date, 'YYYYMMDD')` | |
| `TO_DATE('str', 'DD/MM/YYYY')` | `TO_DATE('str', 'DD/MM/YYYY')` | Verify format compatibility |
| `TO_NUMBER(str)` | `TRY_TO_NUMBER(str)` or `TO_NUMBER(str)` | |
| `TRUNC(date)` | `DATE_TRUNC('day', date)` | |
| `TRUNC(date, 'MM')` | `DATE_TRUNC('month', date)` | |
| `ADD_MONTHS(date, n)` | `DATEADD('month', n, date)` | |
| `MONTHS_BETWEEN(a, b)` | `DATEDIFF('month', b, a)` | Note argument order |
| `LAST_DAY(date)` | `LAST_DAY(date)` | Compatible |
| `NEXT_DAY(date, 'MON')` | `NEXT_DAY(date, 'MO')` | Day abbreviation may differ |
| `INSTR(str, sub, pos, nth)` | `REGEXP_INSTR(str, REGEXP_REPLACE(sub, '([\\[\\]().*+?{}^$|])', '\\\\\\1'), pos, nth)` | Or simpler: `CHARINDEX` for basic use |
| `LPAD(str, n, pad)` | `LPAD(str, n, pad)` | Compatible |
| `RPAD(str, n, pad)` | `RPAD(str, n, pad)` | Compatible |
| `(+)` outer join | Rewrite as explicit `LEFT JOIN` / `RIGHT JOIN` | |
| `CONNECT BY` hierarchical | Use recursive CTE | |
| `DUAL` | Remove — Snowflake allows `SELECT expr` without FROM | |

### DB2 → Snowflake

| DB2 Function | Snowflake Equivalent |
|-------------|---------------------|
| `CURRENT DATE` | `CURRENT_DATE()` |
| `CURRENT TIMESTAMP` | `CURRENT_TIMESTAMP()` |
| `VALUE(a, b)` | `COALESCE(a, b)` |
| `DIGITS(num)` | `LPAD(TO_VARCHAR(num), n, '0')` |
| `CHAR(date, ISO)` | `TO_VARCHAR(date, 'YYYY-MM-DD')` |
| `DATE(expr)` | `TO_DATE(expr)` |
| `TIMESTAMP(expr)` | `TO_TIMESTAMP(expr)` |
| `STRIP(str)` | `TRIM(str)` |
| `FETCH FIRST n ROWS ONLY` | `LIMIT n` |

### SQL Passthrough Conversion Steps
1. Remove `CONNECT TO / CONNECT USING / DISCONNECT FROM` wrappers
2. Extract the inner SQL body
3. Replace vendor-specific functions using tables above
4. Replace vendor-specific date literals and format strings
5. Resolve table references using Step 2.5 source mapping (or placeholder `{TARGET_SCHEMA}.table_name` if no mapping provided)
6. Verify column names and data types match Snowflake schema

### SQL Server → Snowflake

| SQL Server Function | Snowflake Equivalent | Notes |
|---|---|---|
| `GETDATE()` | `CURRENT_TIMESTAMP()` | |
| `SYSDATETIME()` | `CURRENT_TIMESTAMP()` | |
| `ISNULL(a, b)` | `COALESCE(a, b)` | |
| `CONVERT(VARCHAR, expr, 112)` | `TO_VARCHAR(expr, 'YYYYMMDD')` | Style 112 = YYYYMMDD |
| `CONVERT(VARCHAR, expr, 101)` | `TO_VARCHAR(expr, 'MM/DD/YYYY')` | Style 101 = US date |
| `CONVERT(INT, expr)` | `TRY_CAST(expr AS INT)` | |
| `CAST(expr AS type)` | `CAST(expr AS type)` | Compatible |
| `DATEADD(unit, n, date)` | `DATEADD(unit, n, date)` | Compatible |
| `DATEDIFF(unit, a, b)` | `DATEDIFF(unit, a, b)` | Compatible |
| `LEN(str)` | `LENGTH(str)` | |
| `CHARINDEX(sub, str)` | `CHARINDEX(sub, str)` | Compatible |
| `PATINDEX('%pattern%', str)` | `REGEXP_INSTR(str, 'pattern')` | Convert LIKE pattern to regex |
| `TOP n` (in SELECT) | `LIMIT n` (at end) | Move to end of query |
| `ISNUMERIC(expr)` | `TRY_TO_NUMBER(expr) IS NOT NULL` | |
| `STUFF(str, start, len, rep)` | `INSERT(str, start, len, rep)` | Or: `LEFT(str, start-1) \|\| rep \|\| SUBSTR(str, start+len)` |
| `STRING_AGG(col, ',')` | `LISTAGG(col, ',')` | |
| `FORMAT(date, 'yyyy-MM-dd')` | `TO_VARCHAR(date, 'YYYY-MM-DD')` | |
| `EOMONTH(date)` | `LAST_DAY(date)` | |
| `IIF(cond, a, b)` | `IFF(cond, a, b)` | |
| `NOLOCK` hint | Remove — Snowflake has no locking hints | |
| `WITH (NOLOCK)` | Remove entirely | |
| `@@ROWCOUNT` | Use `SQLROWCOUNT` in stored procedures | |
| `@@ERROR` | Use `SQLCODE` in exception handler | |
