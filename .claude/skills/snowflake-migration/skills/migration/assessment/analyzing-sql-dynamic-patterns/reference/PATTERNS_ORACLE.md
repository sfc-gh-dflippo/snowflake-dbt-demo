# SQL Dynamic Pattern Definitions (Oracle → Snowflake)

Pattern catalog for **Oracle to Snowflake** dynamic SQL migration analysis.

## How to tag (critical for consistent classification)

- **Tag all that apply**: Real stored procedures frequently match multiple patterns.
- **If values are concatenated, always tag `Unsafe-Value-Concatenation`** even if other patterns are also present.
- **Distinguish values vs identifiers**:
  - **Values**: strings/numbers/dates used in predicates/expressions. Should be **bound parameters** (not injected into SQL text).
  - **Identifiers**: schema/table/column names, ORDER BY columns, procedure names. Should be **whitelisted** and properly quoted.
- **Dynamic ≠ unsafe**: `EXECUTE IMMEDIATE` with `USING` clause or `DBMS_SQL` with bind variables is dynamic but low risk.
- **Snowflake mapping shortcut**:
  - Oracle: `EXECUTE IMMEDIATE <sql_text> [INTO <var>] [USING <bind_vars>]`
  - Oracle low-level: `DBMS_SQL.PARSE` / `DBMS_SQL.EXECUTE` / `DBMS_SQL.FETCH_ROWS`
  - Snowflake Scripting: `EXECUTE IMMEDIATE <sql_text> [USING (...)]`
  - Snowflake identifiers: `IDENTIFIER(<string_expr>)`

## Oracle Language Context

**Key Oracle Characteristics:**
- Stored procedures and functions written in **PL/SQL**: `CREATE OR REPLACE PROCEDURE ... AS BEGIN ... END;`
- **Two dynamic SQL APIs** — a critical distinction unique to Oracle:
  - **Native Dynamic SQL (NDS)**: `EXECUTE IMMEDIATE` with `USING` (named bind variables `:varname`) — preferred modern approach
  - **DBMS_SQL package**: low-level cursor API (`DBMS_SQL.OPEN_CURSOR`, `PARSE`, `BIND_VARIABLE`, `EXECUTE`, `FETCH_ROWS`, `CLOSE_CURSOR`) — used when column count/types are unknown at compile time
- String concatenation: `||` operator (same as Teradata/Redshift/ANSI SQL)
- Named bind variables: `:variable_name` placeholders (not positional `?` or `$1`)
- **Identifier quoting**: `DBMS_ASSERT.ENQUOTE_NAME()` for safe identifier quoting; manual `'"' || name || '"'` also common
- **Metadata catalogs**: `ALL_TABLES`, `ALL_COLUMNS`, `ALL_OBJECTS`, `USER_TABLES`, `DBA_TABLES`, `ALL_PROCEDURES`, `ALL_SEQUENCES` — entirely different from SQL Server (`sys.*`), Redshift (`pg_catalog.*`), or Teradata (`DBC.*`)
- **Database Links**: `table_name@dblink_name` — Oracle's mechanism for cross-database/cross-instance queries
- **Autonomous Transactions**: `PRAGMA AUTONOMOUS_TRANSACTION` — executes a sub-procedure in its own independent transaction, invisible to the parent transaction
- **Global Temporary Tables (GTT)**: definition persists in data dictionary; data is session/transaction scoped
- **Object Types and Collections**: `TYPE ... IS TABLE OF ...`, `VARRAY`, used as bind variable types in `DBMS_SQL`
- **Oracle Sequences**: `seq_name.NEXTVAL` / `seq_name.CURRVAL` — often embedded in dynamic INSERT statements
- **`SYSDATE`** vs ANSI `CURRENT_DATE`; `NVL()` vs `COALESCE()`, `DECODE()` vs `CASE`
- **Bulk operations**: `FORALL` statement for bulk DML from collections; `BULK COLLECT INTO` for bulk fetch
- Exception handling: named exceptions (`NO_DATA_FOUND`, `TOO_MANY_ROWS`, `OTHERS`), `SQLERRM`, `SQLCODE`
- Transaction control: explicit `COMMIT`/`ROLLBACK` within procedures; DDL auto-commits in Oracle
- **`UTL_FILE`**: PL/SQL package for server-side file I/O — sometimes used to write/read dynamic SQL scripts

## Table of Contents

1. [Unsafe-Value-Concatenation](#1-unsafe-value-concatenation)
2. [Parameter-Driven](#2-parameter-driven)
3. [Identifier-Driven](#3-identifier-driven)
4. [Clause-Assembly](#4-clause-assembly)
5. [Data-Driven](#5-data-driven)
6. [DDL-Driven](#6-ddl-driven)
7. [Cursor-Driven DDL](#7-cursor-driven-ddl)
8. [Shape-Changing](#8-shape-changing)
9. [Cross-System I/O](#9-cross-system-io)
10. [Security/Context Switching](#10-securitycontext-switching)
11. [DBMS_SQL API-Driven](#11-dbms_sql-api-driven)
12. [Template/Token Replacement](#12-templatetoken-replacement)
13. [Autonomous-Transaction-Driven](#13-autonomous-transaction-driven)
14. [Session-Parameter-Driven](#14-session-parameter-driven)

[Multi-Pattern Classification](#multi-pattern-classification)

---

## 1. Unsafe-Value-Concatenation

**Risk Level:** HIGH (75/100)

**Description:** Direct concatenation of **data values** into SQL text (especially predicates) without parameterization, creating SQL injection vulnerabilities.

**Characteristics:**
- Direct value concatenation into SQL strings using `||` operator
- No `USING` clause for parameter binding
- `EXECUTE IMMEDIATE` without bind variables
- String concatenation with `''''` quote escaping
- Values embedded directly in WHERE clauses, INSERT statements, or UPDATE operations
- Named bind variable notation (`:varname`) absent when it should be present

**Example:**
```sql
CREATE OR REPLACE PROCEDURE search_employee(p_name IN VARCHAR2)
AS
  v_sql VARCHAR2(4000);
BEGIN
  -- UNSAFE: Direct value concatenation
  v_sql := 'SELECT employee_id, salary FROM employees WHERE last_name = '''
           || p_name || '''';
  EXECUTE IMMEDIATE v_sql;
END;
/
```

**Detection Signals:**
- Pattern: `v_sql := '...' || variable || '...'` where variable is a data value
- `TO_CHAR(numeric_var)` or `TO_DATE(date_var)` used for concatenation
- No `USING` clause with `EXECUTE IMMEDIATE`
- Quote-escaping patterns: `''''` or `CHR(39)` near concatenated values
- `REPLACE(val, '''', '''''')` to escape single quotes for concatenation
- Concatenation inside WHERE predicates, VALUES lists, or SET clauses

**Migration Considerations:**
- **Critical**: Refactor to proper parameter binding using `EXECUTE IMMEDIATE ... USING :var`
- Add input validation and sanitization
- Never use `IDENTIFIER()` for data values in Snowflake
- Oracle named bind variables (`:varname`) → Snowflake positional bind variables (`$1`, `$2`, ...)
- Review procedure `AUTHID` clause: `AUTHID CURRENT_USER` (caller rights) vs `AUTHID DEFINER` (owner rights) — maps to Snowflake `EXECUTE AS CALLER` vs `EXECUTE AS OWNER`
- Test with SQL injection attack vectors to verify fixes

**Effort Estimation:** 8-16 hours per procedure

**Complexity Score:** 75/100

---

## 2. Parameter-Driven

**Risk Level:** LOW (15/100)

**Description:** Fixed SQL structure with only values varying through proper parameterization using named bind variables. No string concatenation of SQL structure.

**Characteristics:**
- Static SQL structure
- Uses `EXECUTE IMMEDIATE ... USING :bind_var1, :bind_var2` with named placeholders
- No concatenation of keywords, clauses, or identifiers
- Oracle named bind variables allow same placeholder used multiple times in SQL

**Example:**
```sql
CREATE OR REPLACE PROCEDURE get_orders_by_status(
  p_status     IN  VARCHAR2,
  p_start_date IN  DATE,
  p_result     OUT SYS_REFCURSOR
)
AS
  v_sql VARCHAR2(4000);
BEGIN
  v_sql :=
    'SELECT order_id, customer_id, total_amount
     FROM orders
     WHERE status = :p_status
       AND order_date >= :p_start_date
     ORDER BY order_date DESC';

  OPEN p_result FOR v_sql USING p_status, p_start_date;
END;
/
```

**Single-row fetch variant:**
```sql
CREATE OR REPLACE PROCEDURE get_employee_salary(
  p_emp_id IN  NUMBER,
  p_salary OUT NUMBER
)
AS
  v_sql VARCHAR2(1000);
BEGIN
  v_sql := 'SELECT salary FROM employees WHERE employee_id = :emp_id';
  EXECUTE IMMEDIATE v_sql INTO p_salary USING p_emp_id;
END;
/
```

**Detection Signals:**
- `EXECUTE IMMEDIATE ... USING :varname` pattern with no concatenation
- `OPEN cursor FOR sql_string USING :var` — REF CURSOR pattern
- Named `:varname` placeholders in SQL string
- `INTO` clause with `EXECUTE IMMEDIATE` for single-row results
- No SQL keyword or clause concatenation

**Migration Considerations:**
- Oracle named bind variables (`:varname`) → Snowflake positional bind variables (`$1`, `$2`, ...)
  - If same `:name` appears multiple times in Oracle SQL, each occurrence needs a separate `$N` in Snowflake
- `OPEN cursor FOR sql USING v` (REF CURSOR) → Snowflake returns RESULTSET from stored procedure
- `EXECUTE IMMEDIATE sql INTO var` (single-row) → add `INTO` equivalent in Snowflake scripting
- Minimal refactoring needed beyond placeholder syntax change
- Consider whether dynamic SQL is even needed — may be replaceable with static SQL

**Effort Estimation:** 2-4 hours per procedure

**Complexity Score:** 15/100

---

## 3. Identifier-Driven

**Risk Level:** MEDIUM (45/100)

**Description:** Dynamic **identifiers** (schemas, tables, columns, ORDER BY columns, procedure names) built at runtime.

**Characteristics:**
- Dynamic schema/table/column names
- Uses `DBMS_ASSERT.ENQUOTE_NAME()` for safe identifier quoting (in well-written code)
- Manual double-quoting: `'"' || name || '"'`
- Requires whitelist validation for security
- Case sensitivity: Oracle identifiers are UPPERCASE by default (unquoted); Snowflake also defaults to uppercase — generally easier transition than other platforms

**Example:**
```sql
CREATE OR REPLACE PROCEDURE query_partition(
  p_schema  IN VARCHAR2,
  p_table   IN VARCHAR2,
  p_column  IN VARCHAR2
)
AS
  v_sql     VARCHAR2(4000);
  v_schema  VARCHAR2(100);
  v_table   VARCHAR2(100);
  v_column  VARCHAR2(100);
BEGIN
  -- Use DBMS_ASSERT for safe identifier quoting
  v_schema := DBMS_ASSERT.SCHEMA_NAME(p_schema);   -- validates schema exists
  v_table  := DBMS_ASSERT.SQL_OBJECT_NAME(p_schema || '.' || p_table);
  v_column := DBMS_ASSERT.ENQUOTE_NAME(p_column, FALSE);

  v_sql := 'SELECT ' || v_column
        || ' FROM ' || v_schema || '.' || DBMS_ASSERT.ENQUOTE_NAME(p_table, FALSE)
        || ' WHERE ROWNUM <= 1000';

  EXECUTE IMMEDIATE v_sql;
END;
/
```

**Detection Signals:**
- `DBMS_ASSERT.ENQUOTE_NAME()` / `DBMS_ASSERT.SCHEMA_NAME()` / `DBMS_ASSERT.SQL_OBJECT_NAME()` calls
- Manual double-quoting: `'"' || var || '"'`
- String concatenation near `FROM`, `JOIN`, `ORDER BY`, or `GROUP BY`
- Variables named `v_table`, `v_schema`, `v_owner`, `v_column`, `v_object_name`
- Dynamic column selection or ORDER BY

**Migration Considerations:**
- Use Snowflake `IDENTIFIER()` function instead of `DBMS_ASSERT.ENQUOTE_NAME()`
- **Implement strict whitelist validation** (query `INFORMATION_SCHEMA` to validate before use)
- Case sensitivity is relatively straightforward: both Oracle and Snowflake default to uppercase for unquoted identifiers — but quoted identifiers are case-sensitive in both
- Use fully-qualified names: `database.schema.table` in Snowflake (Oracle uses `schema.table` two-part names)
- `DBMS_ASSERT.SCHEMA_NAME()` validation → replace with `SELECT COUNT(*) FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = :v`

**Effort Estimation:** 6-12 hours per procedure

**Complexity Score:** 45/100

---

## 4. Clause-Assembly

**Risk Level:** MEDIUM (55/100)

**Description:** Conditional addition of `WHERE`/`ORDER BY`/`GROUP BY` fragments based on runtime conditions. Query structure changes across executions.

**Characteristics:**
- Base SQL with conditional clause additions
- Common pattern: `WHERE 1=1` + conditional `AND` appends
- Runtime-determined filtering and sorting
- Often paired with parameter binding via `USING`
- Oracle commonly uses `NVL`/`DECODE` in static SQL as alternative — worth detecting both

**Example:**
```sql
CREATE OR REPLACE PROCEDURE search_customers(
  p_name_filter   IN VARCHAR2,
  p_city_filter   IN VARCHAR2,
  p_active_only   IN NUMBER,        -- 1 = active only
  p_result        OUT SYS_REFCURSOR
)
AS
  v_sql    VARCHAR2(4000);
  v_params VARCHAR2(1000) := '';
BEGIN
  v_sql := 'SELECT customer_id, name, city, status
            FROM customers
            WHERE 1=1';

  IF p_name_filter IS NOT NULL THEN
    v_sql := v_sql || ' AND UPPER(name) LIKE UPPER(:p_name)';
  END IF;

  IF p_city_filter IS NOT NULL THEN
    v_sql := v_sql || ' AND city = :p_city';
  END IF;

  IF p_active_only = 1 THEN
    v_sql := v_sql || ' AND status = ''ACTIVE''';
  END IF;

  v_sql := v_sql || ' ORDER BY name';

  OPEN p_result FOR v_sql USING p_name_filter, p_city_filter;
END;
/
```

**Detection Signals:**
- `WHERE 1=1` pattern as base
- Conditional string appends: `IF condition THEN v_sql := v_sql || ...`
- Dynamic `ORDER BY` or `GROUP BY` clauses
- `OPEN cursor FOR v_sql USING ...` with variable parameter counts
- Static literal injection mixed with bind variables

**Migration Considerations:**
- Snowflake alternative: `WHERE (:p_name IS NULL OR UPPER(name) LIKE UPPER(:p_name))` pattern eliminates dynamic SQL in simple cases
- Note: Oracle `UPPER(name) LIKE UPPER(:param)` → Snowflake supports same `ILIKE` for case-insensitive matching
- `OPEN p_result FOR v_sql USING ...` → Snowflake stored procedure returns RESULTSET
- REF CURSOR output parameters → Snowflake procedure returns `TABLE(...)` or uses RESULTSET type
- Test all conditional path combinations
- Oracle bind variable count must match USING arg count — any variable-count USING usage needs careful porting

**Effort Estimation:** 8-16 hours per procedure

**Complexity Score:** 55/100

---

## 5. Data-Driven

**Risk Level:** MEDIUM-HIGH (70/100)

**Description:** SQL assembled from Oracle data dictionary views (`ALL_*`, `USER_*`, `DBA_*`) or application configuration tables. Object lists, column lists, config-driven filters.

**Characteristics:**
- Queries `ALL_TABLES`, `ALL_COLUMNS`, `ALL_OBJECTS`, `USER_TABLES`, `DBA_TAB_COLUMNS`, etc.
- Uses `LISTAGG()` or cursor loops to build SQL fragments
- Loop-based SQL construction from dictionary results
- Environment-dependent behavior (different schemas yield different SQL)

**Example:**
```sql
CREATE OR REPLACE PROCEDURE union_schema_tables(p_owner IN VARCHAR2)
AS
  v_sql   CLOB := '';
  v_sep   VARCHAR2(12) := '';
  CURSOR c_tables IS
    SELECT table_name
    FROM   all_tables
    WHERE  owner = UPPER(p_owner)
    ORDER  BY table_name;
BEGIN
  FOR rec IN c_tables LOOP
    v_sql := v_sql || v_sep
          || 'SELECT ''' || rec.table_name || ''' AS source_tbl, t.* '
          || 'FROM "' || p_owner || '"."' || rec.table_name || '" t';
    v_sep := ' UNION ALL ';
  END LOOP;

  IF DBMS_LOB.GETLENGTH(v_sql) > 0 THEN
    EXECUTE IMMEDIATE v_sql;
  END IF;
END;
/
```

**LISTAGG variant:**
```sql
DECLARE
  v_cols VARCHAR2(4000);
  v_sql  VARCHAR2(4000);
BEGIN
  SELECT LISTAGG('"' || column_name || '"', ', ')
         WITHIN GROUP (ORDER BY column_id)
  INTO   v_cols
  FROM   all_tab_columns
  WHERE  owner      = 'HR'
    AND  table_name = 'EMPLOYEES';

  v_sql := 'SELECT ' || v_cols || ' FROM hr.employees';
  EXECUTE IMMEDIATE v_sql;
END;
/
```

**Detection Signals:**
- Queries to `ALL_TABLES`, `USER_TABLES`, `DBA_TABLES`, `ALL_TAB_COLUMNS`, `DBA_TAB_COLUMNS`, `ALL_OBJECTS`, `ALL_PROCEDURES`
- `LISTAGG(...) WITHIN GROUP (ORDER BY ...)` building SQL fragments
- `FOR rec IN (SELECT ... FROM all_*)` cursor loops with SQL string appends
- `CLOB` type used for long dynamic SQL (Oracle-specific for strings > 32 KB)
- Often co-occurs with `Identifier-Driven`

**Migration Considerations:**
- **Metadata catalog mapping** (entirely different from SQL Server/Redshift/Teradata):
  - `ALL_TABLES` / `USER_TABLES` → `INFORMATION_SCHEMA.TABLES`
  - `ALL_TAB_COLUMNS` / `USER_TAB_COLUMNS` → `INFORMATION_SCHEMA.COLUMNS`
  - `ALL_OBJECTS` → `INFORMATION_SCHEMA.TABLES` + `PROCEDURES` + `VIEWS`
  - `ALL_PROCEDURES` → `INFORMATION_SCHEMA.PROCEDURES`
  - `ALL_SEQUENCES` → `INFORMATION_SCHEMA.SEQUENCES`
  - `ALL_CONSTRAINTS` → `INFORMATION_SCHEMA.TABLE_CONSTRAINTS`
  - `DBA_*` views → `SNOWFLAKE.ACCOUNT_USAGE.*` (account-level equivalent)
- `LISTAGG` → Snowflake `LISTAGG` (identical syntax and semantics)
- `CLOB` for long SQL → Snowflake `VARCHAR` (up to 16 MB) or `STRING`
- Use Snowflake `GET_DDL()` for object definitions instead of `DBMS_METADATA.GET_DDL()`
- **Test across environments** — dev/test/prod may have different schemas

**Effort Estimation:** 16-32 hours per procedure

**Complexity Score:** 70/100

---

## 6. DDL-Driven

**Risk Level:** HIGH (75/100)

**Description:** Dynamic DDL (CREATE/ALTER/DROP) generation and execution for schema modifications.

**Characteristics:**
- Dynamic schema modifications executed at runtime
- `CREATE`/`ALTER`/`DROP` statements built as strings
- **DDL auto-commits in Oracle** — any `EXECUTE IMMEDIATE` DDL statement implicitly commits the current transaction (critical difference vs DML)
- Oracle-specific DDL options (tablespace, storage clauses, partitioning, `NOLOGGING`) require translation
- Often combined with `ALL_TABLES` / `ALL_COLUMNS` catalog queries

**Example:**
```sql
CREATE OR REPLACE PROCEDURE add_audit_columns(p_owner IN VARCHAR2, p_table IN VARCHAR2)
AS
  v_sql       VARCHAR2(4000);
  v_col_exists NUMBER;
BEGIN
  SELECT COUNT(*)
  INTO   v_col_exists
  FROM   all_tab_columns
  WHERE  owner       = UPPER(p_owner)
    AND  table_name  = UPPER(p_table)
    AND  column_name = 'CREATED_AT';

  IF v_col_exists = 0 THEN
    v_sql := 'ALTER TABLE ' || DBMS_ASSERT.ENQUOTE_NAME(p_owner, FALSE) || '.'
          || DBMS_ASSERT.ENQUOTE_NAME(p_table, FALSE)
          || ' ADD (created_at DATE DEFAULT SYSDATE NOT NULL,'
          || '      updated_at DATE DEFAULT SYSDATE NOT NULL)';
    EXECUTE IMMEDIATE v_sql;
    -- Note: DDL auto-commits; no explicit COMMIT needed or safe here
  END IF;
END;
/
```

**Detection Signals:**
- `CREATE TABLE/VIEW/INDEX/SEQUENCE/SYNONYM` in dynamic strings
- `ALTER TABLE/COLUMN` statements
- `DROP TABLE/VIEW/INDEX` statements
- `TRUNCATE TABLE` in dynamic SQL (Oracle: TRUNCATE is DDL, auto-commits)
- Schema evolution patterns driven by catalog queries
- Oracle-specific DDL keywords: `TABLESPACE`, `STORAGE`, `NOLOGGING`, `PARALLEL`, `PARTITION BY`

**Migration Considerations:**
- **Question if DDL should be procedural**: many cases better handled by CI/CD pipelines (Flyway, Liquibase)
- **Oracle-specific DDL translation required**:
  - Remove: `TABLESPACE`, `STORAGE (INITIAL ... NEXT ...)`, `NOLOGGING`, `PARALLEL`, `PCTFREE`, `PCTUSED`
  - Translate: `PARTITION BY RANGE/LIST/HASH` → Snowflake automatic micro-partitioning (usually remove; add clustering key if needed)
  - Remove: `ENABLE ROW MOVEMENT`, `COMPRESS`, `NOCOMPRESS`
  - Replace: `CREATE GLOBAL TEMPORARY TABLE ... ON COMMIT DELETE/PRESERVE ROWS` → Snowflake `CREATE TEMPORARY TABLE`
  - Replace: `SEQUENCE` objects → Snowflake `AUTOINCREMENT` / `SEQUENCE` (different syntax)
- **DDL auto-commit**: Oracle DDL implicitly commits; Snowflake DDL also auto-commits — behavior is consistent
- `SYSDATE` → `CURRENT_DATE` or `CURRENT_TIMESTAMP` in Snowflake
- Consider Snowflake Zero-Copy Cloning as alternative to dynamic table recreation patterns

**Effort Estimation:** 12-24 hours per procedure

**Complexity Score:** 75/100

---

## 7. Cursor-Driven DDL

**Risk Level:** HIGH (85/100)

**Description:** Cursor or loop iterating over data dictionary or application tables, executing DDL per row. Oracle supports both implicit `FOR rec IN (SELECT ...)` cursor loops and explicit `DECLARE CURSOR` / `OPEN` / `FETCH` / `CLOSE` lifecycle.

**Characteristics:**
- `FOR rec IN (SELECT ... FROM all_tables ...)` implicit cursor loop (most common in Oracle)
- Explicit cursor (`DECLARE CURSOR`, `OPEN`, `FETCH`, `CLOSE`) for complex cases
- DDL execution inside loop via `EXECUTE IMMEDIATE`
- Bulk schema operations across many objects
- Error handling complexity per iteration
- **DDL auto-commits** per loop iteration — transaction boundaries fragmented

**Example:**
```sql
CREATE OR REPLACE PROCEDURE add_column_to_schema(
  p_owner       IN VARCHAR2,
  p_column_spec IN VARCHAR2
)
AS
  v_sql         VARCHAR2(4000);
  v_success_cnt NUMBER := 0;
  v_error_cnt   NUMBER := 0;
BEGIN
  FOR rec IN (
    SELECT table_name
    FROM   all_tables
    WHERE  owner     = UPPER(p_owner)
    ORDER  BY table_name
  ) LOOP
    BEGIN
      v_sql := 'ALTER TABLE "' || p_owner || '"."' || rec.table_name || '"'
            || ' ADD (' || p_column_spec || ')';
      EXECUTE IMMEDIATE v_sql;
      v_success_cnt := v_success_cnt + 1;
    EXCEPTION
      WHEN OTHERS THEN
        INSERT INTO ddl_error_log (table_name, error_msg, log_time)
        VALUES (rec.table_name, SQLERRM, SYSDATE);
        -- Note: this INSERT may be implicitly committed by next DDL
        v_error_cnt := v_error_cnt + 1;
    END;
  END LOOP;

  DBMS_OUTPUT.PUT_LINE('Done: ' || v_success_cnt || ' ok, ' || v_error_cnt || ' errors');
END;
/
```

**Detection Signals:**
- `FOR rec IN (SELECT ... FROM all_tables/all_objects/...)` with `EXECUTE IMMEDIATE` inside loop
- Explicit cursor lifecycle: `DECLARE ... CURSOR`, `OPEN`, `FETCH`, `CLOSE` with DDL
- `WHEN OTHERS THEN` exception handling per iteration
- `DBMS_OUTPUT.PUT_LINE` progress reporting inside loop
- `SQLERRM` / `SQLCODE` in error logging within cursor loop

**Migration Considerations:**
- Oracle implicit `FOR rec IN (SELECT ...)` → Snowflake scripting `FOR rec IN (SELECT ...)` — very similar syntax
- `EXECUTE IMMEDIATE` inside loop → `EXECUTE IMMEDIATE` inside loop (same)
- `WHEN OTHERS THEN` → `EXCEPTION WHEN OTHER THEN` in Snowflake scripting
- `SQLERRM` → `SQLERRM` (Snowflake scripting supports this)
- `DBMS_OUTPUT.PUT_LINE` → remove or replace with logging table inserts
- **Consider refactoring to set-based operations** where possible
- DDL auto-commit behavior consistent between Oracle and Snowflake
- May benefit from Snowflake Tasks for scheduled bulk DDL

**Effort Estimation:** 16-32 hours per procedure

**Complexity Score:** 85/100

---

## 8. Shape-Changing

**Risk Level:** MEDIUM (50/100)

**Description:** Dynamic column lists, PIVOT targets, or UNION builders where the result set structure varies at runtime.

**Characteristics:**
- Dynamic SELECT column list built from `ALL_TAB_COLUMNS` or config
- Runtime-determined result set shape
- Dynamic `PIVOT` with IN-list derived from data (Oracle 11g+ supports `PIVOT XML` for fully dynamic pivots)
- Column list derived from metadata at runtime
- Often used for generic reporting or comparison procedures

**Example:**
```sql
CREATE OR REPLACE PROCEDURE get_typed_columns(
  p_owner      IN  VARCHAR2,
  p_table      IN  VARCHAR2,
  p_data_type  IN  VARCHAR2,    -- e.g., 'NUMBER', 'VARCHAR2'
  p_result     OUT SYS_REFCURSOR
)
AS
  v_cols  VARCHAR2(4000);
  v_sql   VARCHAR2(4000);
BEGIN
  SELECT LISTAGG('"' || column_name || '"', ', ')
         WITHIN GROUP (ORDER BY column_id)
  INTO   v_cols
  FROM   all_tab_columns
  WHERE  owner      = UPPER(p_owner)
    AND  table_name = UPPER(p_table)
    AND  data_type  = UPPER(p_data_type);

  IF v_cols IS NULL THEN
    RAISE_APPLICATION_ERROR(-20001,
      'No ' || p_data_type || ' columns found in ' || p_owner || '.' || p_table);
  END IF;

  v_sql := 'SELECT ' || v_cols || ' FROM "' || p_owner || '"."' || p_table || '"';

  OPEN p_result FOR v_sql;
END;
/
```

**Dynamic PIVOT Example:**
```sql
DECLARE
  v_pivot_cols VARCHAR2(4000);
  v_sql        VARCHAR2(4000);
BEGIN
  SELECT LISTAGG('''' || department_name || '''', ', ')
         WITHIN GROUP (ORDER BY department_name)
  INTO   v_pivot_cols
  FROM   departments;

  v_sql :=
    'SELECT * FROM ('
    || '  SELECT employee_id, department_name, salary FROM emp_dept_v'
    || ') PIVOT (SUM(salary) FOR department_name IN (' || v_pivot_cols || '))';

  EXECUTE IMMEDIATE v_sql;
END;
/
```

**Detection Signals:**
- `LISTAGG(column_name, ...) WITHIN GROUP (ORDER BY ...)` building column lists
- Pattern: `v_sql := 'SELECT ' || v_cols || ' FROM'`
- `FOR rec IN (SELECT column_name FROM all_tab_columns ...)` with string concatenation
- Dynamic `PIVOT ... IN (...)` where IN-list is built from data
- `SYS_REFCURSOR` return type with dynamically shaped result set

**Migration Considerations:**
- Snowflake `LISTAGG` is identical in syntax to Oracle — straightforward migration
- `PIVOT XML` (Oracle's fully dynamic pivot) → Snowflake dynamic PIVOT with string-built IN clause
- `SYS_REFCURSOR` output → Snowflake stored procedure RESULTSET return type
- Consider Snowflake `VARIANT` type for semi-structured data — may eliminate need for dynamic column lists in some reporting patterns
- **Result set shape testing critical** — downstream consumers (BI tools, reports) may break
- `RAISE_APPLICATION_ERROR(-20001, msg)` → `RAISE` with message in Snowflake scripting

**Effort Estimation:** 8-16 hours per procedure

**Complexity Score:** 50/100

---

## 9. Cross-System I/O

**Risk Level:** MEDIUM-HIGH (65/100)

**Description:** Dynamic cross-system access via Oracle Database Links (`@dblink_name`). Used to query or write to remote Oracle instances, or occasionally heterogeneous data sources, with dynamic link names or table paths.

**Characteristics:**
- `@dblink_name` suffix on table/view references
- Dynamic database link names built at runtime
- Distributed query patterns across Oracle instances
- Integration with non-Oracle sources via heterogeneous services (HS) or Transparent Gateways
- Performance considerations: distributed query optimization differs from local queries

**Example:**
```sql
CREATE OR REPLACE PROCEDURE sync_from_remote(
  p_link_name  IN VARCHAR2,
  p_source_tbl IN VARCHAR2,
  p_filter_dt  IN DATE
)
AS
  v_sql VARCHAR2(4000);
BEGIN
  -- Validate link name against whitelist
  -- ...

  v_sql :=
    'INSERT INTO local_staging '
    || 'SELECT * FROM "' || p_source_tbl || '"@' || p_link_name
    || ' WHERE last_updated > :filter_dt';

  EXECUTE IMMEDIATE v_sql USING p_filter_dt;
  COMMIT;
END;
/
```

**Multi-Instance Consolidation Example:**
```sql
CREATE OR REPLACE PROCEDURE consolidate_regional_sales(p_report_date IN DATE)
AS
  v_sql VARCHAR2(4000);
  CURSOR c_links IS
    SELECT db_link
    FROM   all_db_links
    WHERE  db_link LIKE 'REGION_%';
BEGIN
  FOR lnk IN c_links LOOP
    v_sql :=
      'INSERT INTO global_sales '
      || 'SELECT ''' || lnk.db_link || ''' AS region, s.* '
      || 'FROM sales@' || lnk.db_link || ' s '
      || 'WHERE s.sale_date = :dt';
    EXECUTE IMMEDIATE v_sql USING p_report_date;
    COMMIT;
  END LOOP;
END;
/
```

**Detection Signals:**
- `@dblink_name` or `@' || v_link` suffix in dynamic SQL strings
- `ALL_DB_LINKS` / `USER_DB_LINKS` queries for available links
- `DBMS_HS_PASSTHROUGH` calls for heterogeneous gateway queries
- Dynamic server/instance names in SQL text
- `DATABASE LINK` references in connection strings

**Migration Considerations:**
- **Snowflake replaces Database Links entirely**:
  - Multiple Oracle instances → multiple Snowflake databases within same account (cross-database queries are native — no link needed)
  - Heterogeneous Oracle gateways → Snowflake External Tables, partner ETL tools, or Snowflake Data Loading
  - Cross-instance replication → Snowflake Database Replication or Data Sharing
- **Common migration paths**:
  1. Oracle DB Link to sibling Oracle instance → Snowflake database in same account (`DB.SCHEMA.TABLE`)
  2. Oracle to non-Oracle via gateway → ETL pipeline + Snowflake External Tables
  3. Cross-region DB Links → Snowflake Data Sharing across accounts
- `ALL_DB_LINKS` catalog → no equivalent needed (no link concept in Snowflake)
- Often requires **workflow and architecture changes** beyond SQL rewrites
- Enumerate all database links (`SELECT * FROM ALL_DB_LINKS`) before migration planning

**Effort Estimation:** 12-24 hours per procedure

**Complexity Score:** 65/100

---

## 10. Security/Context Switching

**Risk Level:** MEDIUM-HIGH (75/100)

**Description:** Dynamic `GRANT`/`REVOKE`, `EXECUTE AS` context switching using Oracle's `DBMS_SESSION` or `SYS_CONTEXT`, role manipulation, or runtime security changes.

**Characteristics:**
- Dynamic privilege management (`GRANT`/`REVOKE` with runtime object/user names)
- `DBMS_SESSION.SET_CONTEXT` for application context values
- `EXECUTE AS` for procedure-level identity switching
- `AUTHID CURRENT_USER` vs `AUTHID DEFINER` (invoker rights vs definer rights)
- Virtual Private Database (VPD) policies — dynamic predicates injected per session

**Example:**
```sql
CREATE OR REPLACE PROCEDURE grant_table_access(
  p_schema    IN VARCHAR2,
  p_table     IN VARCHAR2,
  p_grantee   IN VARCHAR2,
  p_privilege IN VARCHAR2   -- 'SELECT', 'INSERT', 'ALL'
)
AS
  v_sql VARCHAR2(4000);
BEGIN
  -- Validate privilege value against whitelist
  IF p_privilege NOT IN ('SELECT','INSERT','UPDATE','DELETE','ALL') THEN
    RAISE_APPLICATION_ERROR(-20002, 'Invalid privilege: ' || p_privilege);
  END IF;

  v_sql := 'GRANT ' || p_privilege
        || ' ON "' || p_schema || '"."' || p_table || '"'
        || ' TO "' || p_grantee || '"';

  EXECUTE IMMEDIATE v_sql;
END;
/
```

**Application Context Example:**
```sql
CREATE OR REPLACE PROCEDURE set_app_context(
  p_namespace IN VARCHAR2,
  p_attribute IN VARCHAR2,
  p_value     IN VARCHAR2
)
AS
BEGIN
  DBMS_SESSION.SET_CONTEXT(p_namespace, p_attribute, p_value);
END;
/

-- Used later in row-level security predicates:
-- WHERE department_id = SYS_CONTEXT('HR_CTX', 'DEPT_ID')
```

**Detection Signals:**
- `GRANT`/`REVOKE` in dynamic strings
- `DBMS_SESSION.SET_CONTEXT(...)` calls
- `SYS_CONTEXT(namespace, attribute)` in WHERE predicates of dynamic SQL
- `AUTHID CURRENT_USER` in procedure/function declaration
- `EXECUTE AS` patterns or `DBMS_SYS_SQL` usage
- VPD policy functions referenced in dynamic SQL

**Migration Considerations:**
- **Snowflake RBAC model differs fundamentally**:
  - Oracle: user-based and role-based grants; `AUTHID` for invoker/definer rights
  - Snowflake: strict RBAC — all grants assigned to roles, not users directly
- **Privilege model differences**:
  - Oracle: `GRANT SELECT ON schema.table TO user` (direct user grants allowed)
  - Snowflake: `GRANT SELECT ON TABLE ... TO ROLE ...` (role-only grants)
- **`AUTHID CURRENT_USER`** → Snowflake `EXECUTE AS CALLER`; **`AUTHID DEFINER`** → Snowflake `EXECUTE AS OWNER`
- **Application context / VPD** → Snowflake Row Access Policies (built-in feature, very different implementation)
  - Oracle VPD policy functions → Snowflake row access policy using `CURRENT_ROLE()` / session context
  - `DBMS_SESSION.SET_CONTEXT` → Snowflake session variables: `SET variable = value`
  - `SYS_CONTEXT('NS','ATTR')` → `$variable` or `GETVARIABLE('var')` in Snowflake
- **Compliance review required** for security-sensitive procedures
- Enumerate all VPD policies and application contexts before migration planning

**Effort Estimation:** 12-24 hours per procedure

**Complexity Score:** 75/100

---

## 11. DBMS_SQL API-Driven

**Risk Level:** HIGH (80/100)

**Description:** Oracle's low-level `DBMS_SQL` package — a cursor-based dynamic SQL API used when the number or types of columns/bind variables are unknown at compile time. This is Oracle-unique and has no direct equivalent anywhere outside Oracle.

**Characteristics:**
- `DBMS_SQL.OPEN_CURSOR` → `DBMS_SQL.PARSE` → `DBMS_SQL.BIND_VARIABLE` → `DBMS_SQL.EXECUTE` → `DBMS_SQL.FETCH_ROWS` → `DBMS_SQL.CLOSE_CURSOR`
- Used when column count or bind variable count is determined dynamically at runtime
- `DBMS_SQL.DESCRIBE_COLUMNS` to introspect result set structure
- Can convert between `DBMS_SQL` cursors and `SYS_REFCURSOR` via `DBMS_SQL.TO_REFCURSOR`
- Supports bulk array operations with `DBMS_SQL.BIND_ARRAY`

**Example:**
```sql
CREATE OR REPLACE PROCEDURE execute_dynamic_query(
  p_sql       IN  VARCHAR2,
  p_col_count OUT NUMBER
)
AS
  v_cursor    INTEGER;
  v_rows      INTEGER;
  v_col_descs DBMS_SQL.DESC_TAB;
  v_col_val   VARCHAR2(4000);
BEGIN
  v_cursor := DBMS_SQL.OPEN_CURSOR;

  DBMS_SQL.PARSE(v_cursor, p_sql, DBMS_SQL.NATIVE);

  -- Describe result columns dynamically
  DBMS_SQL.DESCRIBE_COLUMNS(v_cursor, p_col_count, v_col_descs);

  -- Define output columns
  FOR i IN 1..p_col_count LOOP
    DBMS_SQL.DEFINE_COLUMN(v_cursor, i, v_col_val, 4000);
  END LOOP;

  v_rows := DBMS_SQL.EXECUTE(v_cursor);

  WHILE DBMS_SQL.FETCH_ROWS(v_cursor) > 0 LOOP
    FOR i IN 1..p_col_count LOOP
      DBMS_SQL.COLUMN_VALUE(v_cursor, i, v_col_val);
      DBMS_OUTPUT.PUT_LINE('Col ' || i || ': ' || v_col_val);
    END LOOP;
  END LOOP;

  DBMS_SQL.CLOSE_CURSOR(v_cursor);
EXCEPTION
  WHEN OTHERS THEN
    IF DBMS_SQL.IS_OPEN(v_cursor) THEN
      DBMS_SQL.CLOSE_CURSOR(v_cursor);
    END IF;
    RAISE;
END;
/
```

**Detection Signals:**
- `DBMS_SQL.OPEN_CURSOR` / `DBMS_SQL.CLOSE_CURSOR` calls
- `DBMS_SQL.PARSE(cursor, sql, ...)` calls
- `DBMS_SQL.BIND_VARIABLE(cursor, ':name', value)` calls
- `DBMS_SQL.DESCRIBE_COLUMNS` for runtime column introspection
- `DBMS_SQL.DEFINE_COLUMN` / `DBMS_SQL.COLUMN_VALUE` patterns
- `DBMS_SQL.IS_OPEN` in exception handlers
- `DBMS_SQL.TO_REFCURSOR` conversion calls

**Migration Considerations:**
- **No DBMS_SQL equivalent in Snowflake** — requires full rewrite
- **Migration strategy by use case**:
  - Fixed column count, runtime values → rewrite to `EXECUTE IMMEDIATE ... USING :v`
  - Dynamic column count (rare): consider returning JSON/VARIANT and parsing in application layer
  - Column introspection (`DESCRIBE_COLUMNS`) → query `INFORMATION_SCHEMA.COLUMNS` before dynamic execution
  - Bulk array operations (`BIND_ARRAY`) → consider set-based SQL or Snowflake scripting loops
- `DBMS_SQL.BIND_VARIABLE(cur, ':name', val)` → `EXECUTE IMMEDIATE sql USING $1, $2, ...`
- `DBMS_OUTPUT.PUT_LINE` → remove or replace with logging table inserts
- `DBMS_SQL.IS_OPEN` cleanup in exception handler → Snowflake handles cursor lifecycle automatically
- **Highest effort pattern** — requires understanding the runtime column/bind variable shapes before choosing migration approach

**Effort Estimation:** 20-48 hours per procedure

**Complexity Score:** 80/100

---

## 12. Template/Token Replacement

**Risk Level:** MEDIUM-HIGH (65/100)

**Description:** SQL built from templates by replacing tokens or placeholders — such as `{SCHEMA}`, `<<TABLE>>`, or `#FILTER#` — using `REPLACE()` or `REGEXP_REPLACE()`.

**Characteristics:**
- Uses `REPLACE()` or `REGEXP_REPLACE()` to inject SQL fragments
- Template may come from an application configuration table or be hardcoded
- Can obscure whether replacements are values or identifiers
- Common in report-generation frameworks and metadata-driven ETL systems

**Example:**
```sql
CREATE OR REPLACE PROCEDURE execute_report_template(
  p_template_name IN VARCHAR2,
  p_schema        IN VARCHAR2,
  p_filter        IN VARCHAR2
)
AS
  v_template VARCHAR2(32767);
  v_sql      VARCHAR2(32767);
BEGIN
  SELECT template_sql
  INTO   v_template
  FROM   report_templates
  WHERE  template_name = p_template_name;

  v_sql := v_template;
  v_sql := REPLACE(v_sql, '<<SCHEMA>>',  p_schema);
  v_sql := REPLACE(v_sql, '<<FILTER>>',  p_filter);
  v_sql := REPLACE(v_sql, '<<TODAY>>',   TO_CHAR(SYSDATE, 'YYYY-MM-DD'));
  v_sql := REPLACE(v_sql, '<<VERSION>>', '2');

  EXECUTE IMMEDIATE v_sql;
END;
/
```

**REGEXP_REPLACE Variant:**
```sql
-- Replace all <<PARAM_N>> tokens with positional values
v_sql := REGEXP_REPLACE(v_template, '<<([A-Z_]+)>>', ':token');
```

**Detection Signals:**
- `REPLACE(v_sql, ...)` / `REPLACE(v_template, ...)` calls to inject SQL fragments
- Token-like markers: `{...}`, `<<...>>`, `#...#`, `[PLACEHOLDER]`, `/*TOKEN*/`
- Template queries from a config/metadata table before `EXECUTE IMMEDIATE`
- Multiple `REPLACE()` calls on the same SQL variable
- `REGEXP_REPLACE` used on SQL strings

**Migration Considerations:**
- `REPLACE()` → Snowflake `REPLACE()` (identical syntax)
- `REGEXP_REPLACE()` → Snowflake `REGEXP_REPLACE()` (identical syntax)
- **Prefer refactoring to explicit logic** (transforms naturally into Clause-Assembly pattern)
- If templates must remain:
  - **Strictly separate value vs identifier replacements**
  - **Values** → convert to bound parameters with `USING`
  - **Identifiers** → whitelist + `IDENTIFIER()` in Snowflake
- `TO_CHAR(SYSDATE, 'YYYY-MM-DD')` → `TO_CHAR(CURRENT_DATE, 'YYYY-MM-DD')` in Snowflake
- **Security review critical**: `<<FILTER>>` tokens accepting arbitrary SQL are injection vectors
- Consider dbt or Jinja templating as a managed alternative

**Effort Estimation:** 8-20 hours per procedure

**Complexity Score:** 65/100

---

## 13. Autonomous-Transaction-Driven

**Risk Level:** MEDIUM-HIGH (65/100)

**Description:** Dynamic SQL executed inside an **autonomous transaction** (`PRAGMA AUTONOMOUS_TRANSACTION`). This Oracle-specific feature allows a sub-procedure to commit or roll back independently from the calling transaction — commonly used for audit logging, error tracking, or DDL execution within a DML transaction.

**Characteristics:**
- `PRAGMA AUTONOMOUS_TRANSACTION` declaration in procedure/function header
- Independent `COMMIT`/`ROLLBACK` inside the autonomous block
- Used when dynamic DDL (which auto-commits) must not affect the parent transaction
- Common for audit log inserts that must survive a parent rollback
- Dynamic SQL inside autonomous procedures inherits the same isolation

**Example (Audit Logger):**
```sql
CREATE OR REPLACE PROCEDURE log_ddl_action(
  p_object_name IN VARCHAR2,
  p_action      IN VARCHAR2,
  p_sql_text    IN VARCHAR2
)
AS
  PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN
  INSERT INTO ddl_audit_log (object_name, action, sql_text, log_time, log_user)
  VALUES (p_object_name, p_action, p_sql_text, SYSDATE, USER);
  COMMIT;   -- commits only the INSERT above; parent transaction unaffected
END;
/
```

**Dynamic DDL with Autonomous Logging:**
```sql
CREATE OR REPLACE PROCEDURE create_partition_table(
  p_base_table IN VARCHAR2,
  p_partition  IN VARCHAR2,
  p_range_val  IN VARCHAR2
)
AS
  v_sql VARCHAR2(4000);
BEGIN
  v_sql :=
    'CREATE TABLE "' || p_base_table || '_' || p_partition || '" '
    || 'PARTITION OF "' || p_base_table || '" '
    || 'FOR VALUES FROM (''' || p_range_val || ''') TO (MAXVALUE)';

  EXECUTE IMMEDIATE v_sql;   -- DDL auto-commits; parent tx has already been committed implicitly

  log_ddl_action(p_base_table || '_' || p_partition, 'CREATE', v_sql);  -- autonomous log
END;
/
```

**Detection Signals:**
- `PRAGMA AUTONOMOUS_TRANSACTION` in procedure/function spec
- `COMMIT` or `ROLLBACK` inside a called procedure that is declared autonomous
- Audit/logging procedures called from within dynamic DDL procedures
- Exception handlers that call logging procedures with their own `COMMIT`
- `SAVEPOINT` usage around dynamic SQL blocks

**Migration Considerations:**
- **No `PRAGMA AUTONOMOUS_TRANSACTION` equivalent in Snowflake**
- **Migration strategy by use case**:
  - **Audit logging**: convert to regular inserts into logging tables; Snowflake autocommit ensures inserts commit with the statement; or use a separate Snowflake Task for async logging
  - **DDL isolation**: not needed — Snowflake DDL auto-commits, same as Oracle
  - **Error logging that must survive rollback**: use Snowflake `EXCEPTION WHEN OTHER THEN` to log before re-raising; or write to an external table/stage
- `COMMIT` inside procedures → usually removable (Snowflake autocommit); keep only if explicit transaction control is needed
- Review all procedures called within autonomous procedures — they may need restructuring
- **Compliance review**: autonomous transactions are sometimes used in security-auditing chains

**Effort Estimation:** 8-16 hours per procedure

**Complexity Score:** 65/100

---

## 14. Session-Parameter-Driven

**Risk Level:** LOW-MEDIUM (35/100)

**Description:** Dynamic SQL used to set Oracle session parameters, NLS settings, or query optimizer hints at runtime.

**Characteristics:**
- `ALTER SESSION SET ...` in dynamic SQL strings
- NLS parameter tuning: `NLS_DATE_FORMAT`, `NLS_NUMERIC_CHARACTERS`, `NLS_LANGUAGE`
- Optimizer parameter setting: `OPTIMIZER_MODE`, `DB_FILE_MULTIBLOCK_READ_COUNT`
- `DBMS_SESSION.SET_NLS` / `DBMS_SESSION.SET_ROLE` calls
- Session-level initialization for locale-aware queries

**Example:**
```sql
CREATE OR REPLACE PROCEDURE configure_session_locale(
  p_date_format    IN VARCHAR2,
  p_numeric_chars  IN VARCHAR2,   -- e.g., '.,'
  p_language       IN VARCHAR2
)
AS
BEGIN
  -- Set NLS parameters dynamically
  EXECUTE IMMEDIATE 'ALTER SESSION SET NLS_DATE_FORMAT = '''
                 || p_date_format || '''';

  EXECUTE IMMEDIATE 'ALTER SESSION SET NLS_NUMERIC_CHARACTERS = '''
                 || p_numeric_chars || '''';

  DBMS_SESSION.SET_NLS('NLS_LANGUAGE', '''' || p_language || '''');
END;
/
```

**Optimizer Parameter Example:**
```sql
CREATE OR REPLACE PROCEDURE run_with_hints(
  p_optimizer_mode IN VARCHAR2,   -- 'ALL_ROWS' or 'FIRST_ROWS'
  p_query          IN VARCHAR2
)
AS
BEGIN
  EXECUTE IMMEDIATE 'ALTER SESSION SET OPTIMIZER_MODE = ' || p_optimizer_mode;
  EXECUTE IMMEDIATE p_query;
  EXECUTE IMMEDIATE 'ALTER SESSION SET OPTIMIZER_MODE = ALL_ROWS';  -- reset
END;
/
```

**Detection Signals:**
- `ALTER SESSION SET NLS_DATE_FORMAT` in dynamic strings
- `ALTER SESSION SET NLS_NUMERIC_CHARACTERS` / `NLS_LANGUAGE` / `NLS_TERRITORY`
- `DBMS_SESSION.SET_NLS(...)` calls
- `ALTER SESSION SET OPTIMIZER_MODE` / `CURSOR_SHARING` in dynamic SQL
- `DBMS_SESSION.SET_ROLE(...)` for runtime role activation

**Migration Considerations:**
- **Most Oracle session parameters can be removed**: Snowflake handles NLS/locale automatically
- **NLS parameter mapping**:
  - `NLS_DATE_FORMAT` → Snowflake session parameter `DATE_INPUT_FORMAT` / `DATE_OUTPUT_FORMAT`
  - `NLS_NUMERIC_CHARACTERS` → Snowflake handles standard decimal notation; no direct equivalent
  - `NLS_LANGUAGE` → Snowflake uses Unicode; no NLS language setting needed
  - `NLS_TIMESTAMP_FORMAT` → Snowflake `TIMESTAMP_INPUT_FORMAT` / `TIMESTAMP_OUTPUT_FORMAT`
- **Optimizer parameters**: remove entirely — Snowflake's optimizer is automatic and has no user-configurable modes
- `DBMS_SESSION.SET_NLS` → `ALTER SESSION SET parameter = value` (Snowflake syntax)
- `DBMS_SESSION.SET_ROLE` → `USE ROLE role_name` in Snowflake
- Review if dynamic session configuration is still needed post-migration

**Effort Estimation:** 2-8 hours per procedure

**Complexity Score:** 35/100

---

## Multi-Pattern Classification

Objects often exhibit multiple patterns. **Tag with all applicable patterns**.

**Example — Multiple Patterns:**
```sql
CREATE OR REPLACE PROCEDURE rebuild_schema_objects(p_owner IN VARCHAR2)
AS
  v_sql VARCHAR2(4000);
BEGIN
  FOR rec IN (
    SELECT table_name                -- Data-Driven: ALL_TABLES catalog query
    FROM   all_tables
    WHERE  owner = UPPER(p_owner)
    ORDER  BY table_name
  ) LOOP                             -- Cursor-Driven DDL: iterate over objects
    EXECUTE IMMEDIATE                -- DDL-Driven: dynamic DROP
      'DROP TABLE "' || p_owner || '"."' || rec.table_name || '" CASCADE CONSTRAINTS';
                                     -- Identifier-Driven: runtime object names
    EXECUTE IMMEDIATE                -- DDL-Driven: dynamic CREATE
      'CREATE TABLE "' || p_owner || '"."' || rec.table_name || '" '
      || '(id NUMBER NOT NULL, data VARCHAR2(4000)) '
      || 'TABLESPACE users';
  END LOOP;
END;
/
```

**Patterns Present:** `Data-Driven | DDL-Driven | Cursor-Driven DDL | Identifier-Driven`

**Tagging Guidelines:**
- Identify **all** applicable patterns
- Use pipe separator: `"Pattern1 | Pattern2 | Pattern3"`
- List primary pattern first, additional patterns following
- Document rationale in justification notes
- If `Unsafe-Value-Concatenation` is present, **always include it**

---

## Oracle → Snowflake Migration Quick Reference

### Syntax Translation

| Oracle | Snowflake | Notes |
|--------|-----------|-------|
| `EXECUTE IMMEDIATE sql` | `EXECUTE IMMEDIATE sql` | Identical syntax |
| `EXECUTE IMMEDIATE sql USING :v1, :v2` | `EXECUTE IMMEDIATE sql USING ($1, $2)` | Change named `:var` to positional `$N`; add parentheses |
| `EXECUTE IMMEDIATE sql INTO :out_var USING :v` | Assign result in scripting block | No INTO clause in Snowflake EXECUTE IMMEDIATE |
| `OPEN cur FOR sql USING :v` | Return RESULTSET from procedure | REF CURSOR → RESULTSET type |
| `DBMS_SQL.*` package | No equivalent; rewrite to EXECUTE IMMEDIATE | Full rewrite required |
| `DBMS_ASSERT.ENQUOTE_NAME(name, FALSE)` | `IDENTIFIER(name)` | Built-in function |
| `DBMS_ASSERT.SCHEMA_NAME(schema)` | Query `INFORMATION_SCHEMA.SCHEMATA` | Validate existence explicitly |
| `ALL_TABLES` / `USER_TABLES` | `INFORMATION_SCHEMA.TABLES` | Catalog rewrite |
| `ALL_TAB_COLUMNS` / `DBA_TAB_COLUMNS` | `INFORMATION_SCHEMA.COLUMNS` | Catalog rewrite |
| `ALL_OBJECTS` / `USER_OBJECTS` | `INFORMATION_SCHEMA.TABLES` + `PROCEDURES` + `VIEWS` | Combine queries |
| `DBMS_METADATA.GET_DDL(...)` | `GET_DDL(object_type, name)` | Different function name/syntax |
| `PRAGMA AUTONOMOUS_TRANSACTION` | No equivalent; restructure | See Pattern 13 |
| `AUTHID CURRENT_USER` | `EXECUTE AS CALLER` | Invoker rights |
| `AUTHID DEFINER` | `EXECUTE AS OWNER` | Definer rights (Snowflake default) |
| `SYSDATE` | `CURRENT_DATE` / `CURRENT_TIMESTAMP` | ANSI standard |
| `NVL(x, y)` | `NVL(x, y)` or `COALESCE(x, y)` | Both supported in Snowflake |
| `DECODE(expr, when, then, ...)` | `CASE expr WHEN ... THEN ... END` | Use CASE expression |
| `LISTAGG(x, ',') WITHIN GROUP (ORDER BY y)` | `LISTAGG(x, ',') WITHIN GROUP (ORDER BY y)` | Identical syntax |
| `RAISE_APPLICATION_ERROR(-20001, msg)` | `RAISE` with message | Different syntax |
| `SQLERRM` | `SQLERRM` | Supported in Snowflake scripting |
| `DBMS_OUTPUT.PUT_LINE(msg)` | Remove or use logging table insert | No console output in Snowflake |
| `TABLESPACE / STORAGE / PCTFREE` DDL | Remove | Not applicable in Snowflake |
| `PARTITION BY RANGE/LIST/HASH` DDL | Remove; use clustering key if needed | Snowflake auto-partitions |
| `CREATE GLOBAL TEMPORARY TABLE ... ON COMMIT DELETE ROWS` | `CREATE TEMPORARY TABLE` | Similar session-scoped semantics |
| `table_name@dblink` | `DATABASE.SCHEMA.TABLE` | No DB links; cross-DB queries native |
| `SET variable := value` (PL/SQL) | `variable := value` (Snowflake scripting) | Drop SET keyword |
| `CHR(39)` | `''''` or `CHR(39)` | Both work; use literal quoting consistently |
| `CLOB` variable | `VARCHAR` (up to 16 MB) or `STRING` | CLOB not needed for SQL strings |

### Architecture Translation

| Oracle Feature | Snowflake Equivalent | Migration Notes |
|----------------|---------------------|-----------------|
| Database Links (`@dblink`) | Cross-database queries (`DB.SCHEMA.TABLE`) | No link concept; native cross-DB |
| Heterogeneous DB Links (Oracle HS) | External Tables + ETL pipelines | Architecture decision required |
| Autonomous Transactions | Restructure; use EXCEPTION handlers | No PRAGMA equivalent |
| VPD / Row-Level Security | Snowflake Row Access Policies | Very different implementation |
| Application Context (`DBMS_SESSION.SET_CONTEXT`) | Session variables (`SET var = val`) | Different mechanism |
| `SYS_CONTEXT('NS','ATTR')` | `$variable` or `GETVARIABLE('var')` | Session variable access |
| Oracle Sequences | `AUTOINCREMENT` or Snowflake `SEQUENCE` | Different syntax |
| Global Temporary Tables | Temporary Tables | Similar semantics; syntax differs |
| Oracle Partitioning (DDL) | Automatic micro-partitioning | Remove partitioning DDL; consider clustering |
| DBMS_SQL package | No equivalent; rewrite to NDS | Full rewrite required |
| `DBMS_METADATA.GET_DDL` | `GET_DDL(type, name)` | Different syntax |
| Tablespaces | Not applicable | Remove all tablespace references |
| Oracle SQL*Loader | `COPY INTO` + `PUT` | Stage files then load |
| Data Pump (expdp/impdp) | `COPY INTO` + `CREATE TABLE AS SELECT` | Different loading paradigm |
| Oracle Scheduler (`DBMS_SCHEDULER`) | Snowflake Tasks | Managed serverless scheduling |
| NLS settings | Session parameters + `DATE_INPUT_FORMAT` etc. | Most auto-handled; remove NLS code |
| `OPTIMIZER_MODE` hints | Remove; Snowflake optimizer automatic | No user-configurable optimizer mode |
| `DBMS_STATS` | Automatic statistics | Snowflake maintains statistics automatically |

### Common Refactoring Patterns

1. **Parameter binding**: Change named `:varname` placeholders to positional `$1`, `$2`, ...; add parentheses around `USING` args
2. **Identifier handling**: Replace `DBMS_ASSERT.ENQUOTE_NAME()` with `IDENTIFIER()`
3. **Catalog rewrites**: Replace all `ALL_*` / `USER_*` / `DBA_*` queries with `INFORMATION_SCHEMA.*` equivalents
4. **DBMS_SQL rewrite**: Convert low-level OPEN_CURSOR/PARSE/EXECUTE/FETCH to `EXECUTE IMMEDIATE` or scripting loops
5. **Remove Oracle DDL options**: Strip `TABLESPACE`, `STORAGE`, `PCTFREE`, `PARTITION BY`, `NOLOGGING`, `COMPRESS`
6. **Cursor loop simplification**: Oracle `FOR rec IN (SELECT ...)` → Snowflake `FOR rec IN (SELECT ...)` — nearly identical
7. **REF CURSOR migration**: Convert `OUT SYS_REFCURSOR` parameters to Snowflake procedure `RETURNS TABLE(...)` or RESULTSET
8. **Remove DBMS_OUTPUT**: Replace `DBMS_OUTPUT.PUT_LINE` with logging table inserts or remove
9. **Autonomous transaction restructure**: Move audit logging to `EXCEPTION WHEN OTHER THEN` blocks
10. **NLS cleanup**: Remove `ALTER SESSION SET NLS_*`; use Snowflake session parameters where needed

### Testing Checklist

- [ ] Named `:varname` bind variables converted to positional `$1`, `$2`, ... and USING parentheses added
- [ ] `EXECUTE IMMEDIATE sql INTO var` converted (no INTO clause in Snowflake)
- [ ] All `DBMS_SQL` code fully rewritten (no equivalent exists)
- [ ] `SYS_REFCURSOR` OUT parameters migrated to RESULTSET return type
- [ ] All `ALL_*` / `USER_*` / `DBA_*` catalog queries rewritten to `INFORMATION_SCHEMA.*`
- [ ] No Oracle-specific DDL remains (`TABLESPACE`, `STORAGE`, `PCTFREE`, `PARTITION BY`, `NOLOGGING`)
- [ ] Oracle sequences replaced with `AUTOINCREMENT` or Snowflake `SEQUENCE`
- [ ] `PRAGMA AUTONOMOUS_TRANSACTION` procedures restructured
- [ ] `AUTHID` clause mapped to `EXECUTE AS CALLER` / `EXECUTE AS OWNER`
- [ ] VPD policies migrated to Snowflake Row Access Policies
- [ ] Application contexts migrated to session variables
- [ ] Database Links replaced with cross-database queries (`DB.SCHEMA.TABLE`)
- [ ] `SYSDATE` replaced with `CURRENT_DATE` / `CURRENT_TIMESTAMP`
- [ ] `DBMS_OUTPUT.PUT_LINE` removed or replaced
- [ ] `RAISE_APPLICATION_ERROR` replaced with `RAISE`
- [ ] Error handling ported correctly (`WHEN OTHERS THEN` → `EXCEPTION WHEN OTHER THEN`)
- [ ] Identifier case sensitivity verified (both Oracle and Snowflake uppercase unquoted — generally safe)
- [ ] Performance acceptable (verify clustering keys where Oracle partitioning was relied upon)
- [ ] Security model validated (Oracle GRANT to user → Snowflake GRANT to role)
- [ ] All code paths tested including error/exception branches
