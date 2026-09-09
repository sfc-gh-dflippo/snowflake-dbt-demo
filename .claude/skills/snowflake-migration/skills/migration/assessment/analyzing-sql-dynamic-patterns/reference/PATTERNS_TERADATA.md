# SQL Dynamic Pattern Definitions (Teradata → Snowflake)

Pattern catalog for **Teradata to Snowflake** dynamic SQL migration analysis.

## How to tag (critical for consistent classification)

- **Tag all that apply**: Real stored procedures frequently match multiple patterns.
- **If values are concatenated, always tag `Unsafe-Value-Concatenation`** even if other patterns are also present.
- **Distinguish values vs identifiers**:
  - **Values**: strings/numbers/dates used in predicates/expressions. Should be **bound parameters** (not injected into SQL text).
  - **Identifiers**: database/table/column names, ORDER BY columns, procedure names. Should be **whitelisted** and properly quoted.
- **Dynamic ≠ unsafe**: `EXECUTE IMMEDIATE` with `USING` clause is dynamic but low risk.
- **Snowflake mapping shortcut**:
  - Teradata: `EXECUTE IMMEDIATE <sql_text> [USING (val1, val2, ...)]`
  - Snowflake Scripting: `EXECUTE IMMEDIATE <sql_text> [USING (...)]`
  - Snowflake identifiers: `IDENTIFIER(<string_expr>)`

## Teradata Language Context

**Key Teradata Characteristics:**
- Stored procedures written in **Teradata SPL** (Stored Procedure Language): `REPLACE PROCEDURE ... BEGIN ... END;`
- Native `EXECUTE IMMEDIATE` for dynamic SQL — closest of all source dialects to Snowflake syntax
- Parameter binding via `EXECUTE IMMEDIATE sql USING val1, val2` with positional `?` placeholders
- String concatenation: `||` operator (same as Redshift/ANSI SQL)
- **No `QUOTENAME()` / `QUOTE_IDENT()`**: identifiers are double-quoted manually — `'"' || name || '"'`
- **Metadata catalogs**: `DBC.TablesV`, `DBC.ColumnsV`, `DBC.DatabasesV`, `DBC.IndicesV` — entirely different from `sys.*` (SQL Server) or `pg_catalog.*` (Redshift)
- **Teradata Macros**: `REPLACE MACRO` / `EXEC macro_name(...)` — a Teradata-unique parameterized SQL object, commonly used as lightweight "parameterized views"
- **Workload management**: `SET QUERY_BAND` for TASM/TIWM routing and chargeback — no equivalent to Redshift WLM queues or SQL Server query hints
- **Table semantics**: `VOLATILE TABLE` (session-scoped, auto-dropped) vs `GLOBAL TEMPORARY TABLE` (persistent definition, session data); `MULTISET` (allows duplicates) vs `SET` (enforces uniqueness)
- **Data loading tools**: BTEQ scripts (`.RUN FILE`, `.IMPORT`), FastLoad, MultiLoad, Teradata Parallel Transporter (TPT) — often invoked from shell scripts with dynamic path/date substitution
- **Date/time**: proprietary default format `DATE FORMAT 'YY/MM/DD'`; explicit `CAST(x AS DATE FORMAT 'YYYY-MM-DD')` common
- **BTEQ substitution variables**: `&variable` expansion in scripts for environment-driven execution
- **Cursor lifecycle** (explicit, no `FOR rec IN SELECT` shorthand):
  ```sql
  DECLARE cur CURSOR FOR SELECT ...;
  OPEN cur;
  FETCH cur INTO :var1, :var2;
  CLOSE cur;
  ```
- **Host variable notation**: `:variable` used in embedded SQL contexts (BTEQ, JDBC) alongside SPL `DECLARE` variables
- Transaction control: `BT` / `ET` (Begin/End Transaction) in BTEQ; `BEGIN TRANSACTION` / `END TRANSACTION` in SPL

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
11. [Data-Loading](#11-data-loading)
12. [Template/Token Replacement](#12-templatetoken-replacement)
13. [Macro-Driven](#13-macro-driven)
14. [Query-Band/Session-Parameter-Driven](#14-query-bandsession-parameter-driven)

[Multi-Pattern Classification](#multi-pattern-classification)

---

## 1. Unsafe-Value-Concatenation

**Risk Level:** HIGH (75/100)

**Description:** Direct concatenation of **data values** into SQL text (especially predicates) without parameterization, creating SQL injection vulnerabilities.

**Characteristics:**
- Direct value concatenation into SQL strings using `||` operator
- No `USING` clause for parameter binding
- `EXECUTE IMMEDIATE` without bound parameters
- String concatenation with `''''` quote escaping or `CHAR(39)`
- Values embedded directly in WHERE clauses, INSERT statements, or UPDATE operations
- Occasionally uses `:variable` host-variable notation mixed with string-built SQL

**Example:**
```sql
REPLACE PROCEDURE search_customer(IN p_name VARCHAR(100))
BEGIN
  DECLARE sql_text VARCHAR(10000);

  -- UNSAFE: Direct value concatenation
  SET sql_text = 'SELECT customer_id, email FROM customers WHERE last_name = '''
                 || p_name || '''';
  EXECUTE IMMEDIATE sql_text;
END;
```

**Detection Signals:**
- Pattern: `sql_text = '...' || variable || '...'` where variable is a data value
- `CAST(:var AS VARCHAR(...))` for concatenation
- No `USING` clause with `EXECUTE IMMEDIATE`
- Quote-escaping patterns: `''''` or `CHAR(39)` near concatenated values
- Concatenation inside WHERE predicates, VALUES lists, or SET clauses
- `:variable` notation used in manually assembled SQL strings

**Migration Considerations:**
- **Critical**: Refactor to proper parameter binding using `EXECUTE IMMEDIATE ... USING`
- Add input validation and sanitization
- Never use `IDENTIFIER()` for data values in Snowflake
- Teradata stored procedures execute with **owner rights** by default; review caller vs owner rights in Snowflake
- Test with SQL injection attack vectors to verify fixes

**Effort Estimation:** 8-16 hours per procedure

**Complexity Score:** 75/100

---

## 2. Parameter-Driven

**Risk Level:** LOW (15/100)

**Description:** Fixed SQL structure with only values varying through proper parameterization using the `USING` clause. No string concatenation of SQL structure.

**Characteristics:**
- Static SQL structure
- Uses `EXECUTE IMMEDIATE ... USING` with positional `?` placeholders
- No concatenation of keywords, clauses, or identifiers
- Teradata's native dynamic SQL is the closest source-dialect syntax to Snowflake

**Example:**
```sql
REPLACE PROCEDURE get_orders_by_status(
  IN p_status     VARCHAR(50),
  IN p_start_date DATE
)
BEGIN
  DECLARE sql_text VARCHAR(10000);

  SET sql_text =
    'SELECT order_id, customer_id, total_amount
     FROM orders
     WHERE status = ?
       AND order_date >= ?
     ORDER BY order_date DESC';

  EXECUTE IMMEDIATE sql_text USING p_status, p_start_date;
END;
```

**Detection Signals:**
- `EXECUTE IMMEDIATE ... USING` pattern with no concatenation
- Positional `?` placeholders in SQL string
- No SQL keyword or clause concatenation
- Fixed query structure — only bound values vary

**Migration Considerations:**
- **Easiest migration path**: Teradata `EXECUTE IMMEDIATE ... USING` maps almost directly to Snowflake `EXECUTE IMMEDIATE ... USING`
- Change positional `?` placeholders to `$1`, `$2`, ... in Snowflake
- Minimal refactoring needed — verify data type compatibility
- Consider whether dynamic SQL is even required: static SQL may suffice in Snowflake

**Effort Estimation:** 2-4 hours per procedure

**Complexity Score:** 15/100

---

## 3. Identifier-Driven

**Risk Level:** MEDIUM (45/100)

**Description:** Dynamic **identifiers** (databases, tables, columns, ORDER BY columns, procedure names) built at runtime.

**Characteristics:**
- Dynamic database/table/column/schema names
- No built-in quoting function — identifiers double-quoted manually: `'"' || name || '"'`
- Requires whitelist validation for security
- Case sensitivity: Teradata is case-insensitive by default; Snowflake defaults to uppercase

**Example:**
```sql
REPLACE PROCEDURE query_table(
  IN p_database   VARCHAR(100),
  IN p_table_name VARCHAR(100),
  IN p_column     VARCHAR(100)
)
BEGIN
  DECLARE sql_text VARCHAR(10000);

  -- Validate identifiers against whitelist before use
  SET sql_text =
    'SELECT "' || p_column || '"'
    || ' FROM "' || p_database || '"."' || p_table_name || '"'
    || ' SAMPLE 100';

  EXECUTE IMMEDIATE sql_text;
END;
```

**Dynamic ORDER BY Example:**
```sql
REPLACE PROCEDURE sorted_report(
  IN p_table    VARCHAR(100),
  IN p_order_by VARCHAR(100)   -- must be whitelisted
)
BEGIN
  DECLARE sql_text VARCHAR(10000);

  SET sql_text =
    'SELECT * FROM ' || p_table
    || ' ORDER BY "' || p_order_by || '"';

  EXECUTE IMMEDIATE sql_text;
END;
```

**Detection Signals:**
- Manual double-quote injection: `'"' || variable || '"'`
- String concatenation near `FROM`, `JOIN`, `ORDER BY`, or `GROUP BY`
- Dynamic column selection or dynamic ORDER BY
- Variables named `*_table`, `*_schema`, `*_db`, `*_col`, `*_column`

**Migration Considerations:**
- Use Snowflake `IDENTIFIER()` function instead of manual double-quoting
- **Implement strict whitelist validation** (query `INFORMATION_SCHEMA` to validate before use)
- Handle identifier case sensitivity carefully:
  - Teradata: case-insensitive (no default-case folding)
  - Snowflake: unquoted identifiers uppercased; quoted identifiers are case-sensitive
- Use fully-qualified names: `database.schema.table` in Snowflake
- Test with mixed-case object names

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

**Example:**
```sql
REPLACE PROCEDURE search_products(
  IN p_category   VARCHAR(100),
  IN p_min_price  DECIMAL(10,2),
  IN p_active_only BYTEINT        -- 1 = active only
)
BEGIN
  DECLARE sql_text   VARCHAR(10000);
  DECLARE param_list VARCHAR(5000);

  SET sql_text = 'SELECT product_id, name, price, category
                  FROM products
                  WHERE 1=1';

  IF p_category IS NOT NULL THEN
    SET sql_text = sql_text || ' AND category = ?';
  END IF;

  IF p_min_price IS NOT NULL THEN
    SET sql_text = sql_text || ' AND price >= ?';
  END IF;

  IF p_active_only = 1 THEN
    SET sql_text = sql_text || ' AND is_active = 1';
  END IF;

  SET sql_text = sql_text || ' ORDER BY name';

  EXECUTE IMMEDIATE sql_text USING p_category, p_min_price;
END;
```

**Detection Signals:**
- `WHERE 1=1` pattern as base
- Conditional string appends: `IF condition THEN SET sql_text = sql_text || ...`
- Dynamic `ORDER BY` or `GROUP BY` clauses
- `USING` clause with variable number of parameters
- `NULL` checks driving clause inclusion

**Migration Considerations:**
- Snowflake alternative: `WHERE (p_category IS NULL OR category = :p_category)` pattern eliminates dynamic SQL in simple cases
- Use `CASE` expressions for conditional ordering
- Note: Teradata BYTEINT boolean flags may need mapping to Snowflake `BOOLEAN`
- Test all conditional path combinations
- Review parameter count in USING clause — must match `?` count exactly

**Effort Estimation:** 8-16 hours per procedure

**Complexity Score:** 55/100

---

## 5. Data-Driven

**Risk Level:** MEDIUM-HIGH (70/100)

**Description:** SQL assembled from Teradata system catalog tables (`DBC.*`) or application configuration tables. Object lists, column lists, and config-driven filters.

**Characteristics:**
- Queries `DBC.TablesV`, `DBC.ColumnsV`, `DBC.DatabasesV`, `DBC.IndicesV`
- Uses string aggregation (`XMLAGG`/loop concatenation) to build SQL fragments
- Loop-based SQL construction from cursor results
- Environment-dependent behavior (different databases/schemas yield different SQL)

**Example:**
```sql
REPLACE PROCEDURE union_schema_tables(IN p_database VARCHAR(100))
BEGIN
  DECLARE sql_text   VARCHAR(64000) DEFAULT '';
  DECLARE tbl_name   VARCHAR(100);
  DECLARE first_row  BYTEINT DEFAULT 1;

  DECLARE tbl_cur CURSOR FOR
    SELECT TableName
    FROM DBC.TablesV
    WHERE DatabaseName = p_database
      AND TableKind = 'T'
    ORDER BY TableName;

  OPEN tbl_cur;

  fetch_loop:
  LOOP
    FETCH tbl_cur INTO tbl_name;
    IF (SQLCODE <> 0) THEN LEAVE fetch_loop; END IF;

    IF first_row = 0 THEN
      SET sql_text = sql_text || ' UNION ALL ';
    END IF;

    SET sql_text = sql_text
      || 'SELECT ''' || tbl_name || ''' AS source_tbl, * '
      || 'FROM "' || p_database || '"."' || tbl_name || '"';

    SET first_row = 0;
  END LOOP fetch_loop;

  CLOSE tbl_cur;

  IF CHAR_LENGTH(sql_text) > 0 THEN
    EXECUTE IMMEDIATE sql_text;
  END IF;
END;
```

**Detection Signals:**
- Queries to `DBC.TablesV`, `DBC.ColumnsV`, `DBC.DatabasesV`, `DBC.IndicesV`, `DBC.All_RI_ChildrenV`
- Cursor iteration with SQL string concatenation
- `XMLAGG(... ORDER BY ...)` or `||` aggregation to build column/object lists
- Often co-occurs with `Identifier-Driven` (object names from catalog)
- Database/environment-specific logic based on catalog results

**Migration Considerations:**
- **Metadata catalog mapping** (critical — entirely different from SQL Server/Redshift):
  - `DBC.TablesV` → `INFORMATION_SCHEMA.TABLES`
  - `DBC.ColumnsV` → `INFORMATION_SCHEMA.COLUMNS`
  - `DBC.DatabasesV` → `INFORMATION_SCHEMA.SCHEMATA`
  - `DBC.IndicesV` → `INFORMATION_SCHEMA.TABLE_CONSTRAINTS` + `KEY_COLUMN_USAGE`
  - `DBC.All_RI_ChildrenV` → `INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS`
- Snowflake `INFORMATION_SCHEMA` is standard SQL compliant; `SHOW` commands available for broader metadata
- Use Snowflake `GET_DDL()` for object definitions
- **Test across environments** — dev/test/prod may have different databases
- Document all DBC catalog dependencies before migration

**Effort Estimation:** 16-32 hours per procedure

**Complexity Score:** 70/100

---

## 6. DDL-Driven

**Risk Level:** HIGH (75/100)

**Description:** Dynamic DDL (CREATE/ALTER/DROP) generation and execution for schema modifications.

**Characteristics:**
- Dynamic schema modifications executed at runtime
- `CREATE`/`ALTER`/`DROP` statements built as strings
- Often paired with `DBC.*` catalog queries
- Teradata-specific DDL options (PI, SI, PPI, FALLBACK, JOURNAL) require translation
- Transaction semantics: explicit `BT`/`ET` often wraps DDL in BTEQ; SPL uses `BEGIN TRANSACTION`

**Example:**
```sql
REPLACE PROCEDURE add_audit_column(
  IN p_database   VARCHAR(100),
  IN p_table_name VARCHAR(100)
)
BEGIN
  DECLARE sql_text VARCHAR(10000);
  DECLARE col_exists INTEGER DEFAULT 0;

  -- Check if column already exists
  SELECT COUNT(*) INTO col_exists
  FROM DBC.ColumnsV
  WHERE DatabaseName = p_database
    AND TableName   = p_table_name
    AND ColumnName  = 'last_modified_ts';

  IF col_exists = 0 THEN
    SET sql_text =
      'ALTER TABLE "' || p_database || '"."' || p_table_name || '"'
      || ' ADD last_modified_ts TIMESTAMP(0) DEFAULT CURRENT_TIMESTAMP(0)';

    EXECUTE IMMEDIATE sql_text;
  END IF;
END;
```

**Detection Signals:**
- `CREATE TABLE/VIEW/MACRO/PROCEDURE` in dynamic strings
- `ALTER TABLE` statements in dynamic SQL
- `DROP TABLE/VIEW` statements
- Schema evolution patterns driven by catalog queries
- `DBC.ColumnsV` / `DBC.TablesV` checks before DDL
- `BEGIN TRANSACTION` / `END TRANSACTION` wrapping DDL

**Migration Considerations:**
- **Question if DDL should be procedural**: many cases better handled by CI/CD pipelines
- **Teradata-specific DDL translation required**:
  - Remove: `PRIMARY INDEX (...)`, `UNIQUE PRIMARY INDEX`, `PARTITION BY (RANGE_N(...))`, `FALLBACK`, `BEFORE JOURNAL`, `AFTER JOURNAL`, `CHECKSUM`
  - Translate: `SET TABLE` / `MULTISET TABLE` → standard Snowflake table (no SET semantics)
  - Replace: `COMPRESS` column-level compression → not needed in Snowflake
- Snowflake DDL differences:
  - No distribution or sort keys (use clustering keys if needed)
  - Different data types (`BYTEINT` → `NUMBER(3,0)`, `CHAR(n)` padding behavior differs)
- Consider Snowflake's Zero-Copy Cloning as alternative to some dynamic table creation patterns
- Review transaction control: Teradata explicit `BT/ET` vs Snowflake autocommit

**Effort Estimation:** 12-24 hours per procedure

**Complexity Score:** 75/100

---

## 7. Cursor-Driven DDL

**Risk Level:** HIGH (85/100)

**Description:** Explicit cursor iteration over catalog or application tables, executing DDL per row. Teradata SPL uses an explicit cursor lifecycle — there is no `FOR rec IN SELECT` shorthand available in many other PL languages.

**Characteristics:**
- Explicit `DECLARE CURSOR` / `OPEN` / `FETCH` / `CLOSE` lifecycle
- DDL execution inside cursor loop
- Bulk schema operations across many objects
- Error handling complexity per iteration
- Transaction management across loop iterations

**Example:**
```sql
REPLACE PROCEDURE add_column_to_schema(
  IN p_database    VARCHAR(100),
  IN p_column_spec VARCHAR(1000)
)
BEGIN
  DECLARE sql_text    VARCHAR(10000);
  DECLARE tbl_name    VARCHAR(100);
  DECLARE success_cnt INTEGER DEFAULT 0;
  DECLARE error_cnt   INTEGER DEFAULT 0;
  DECLARE done        BYTEINT DEFAULT 0;

  DECLARE tbl_cur CURSOR FOR
    SELECT TableName
    FROM DBC.TablesV
    WHERE DatabaseName = p_database
      AND TableKind    = 'T'
    ORDER BY TableName;

  DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
  BEGIN
    SET error_cnt = error_cnt + 1;
    SET done = 0;
  END;

  OPEN tbl_cur;

  alter_loop:
  LOOP
    FETCH tbl_cur INTO tbl_name;
    IF (SQLCODE <> 0) THEN LEAVE alter_loop; END IF;

    SET sql_text =
      'ALTER TABLE "' || p_database || '"."' || tbl_name || '"'
      || ' ADD ' || p_column_spec;

    EXECUTE IMMEDIATE sql_text;
    SET success_cnt = success_cnt + 1;
  END LOOP alter_loop;

  CLOSE tbl_cur;
END;
```

**Detection Signals:**
- `DECLARE ... CURSOR FOR` combined with `ALTER`/`CREATE`/`DROP` inside cursor loop
- `OPEN cur; FETCH cur INTO ...; CLOSE cur;` lifecycle
- `EXECUTE IMMEDIATE` inside loop body
- `DBC.*` catalog query as cursor source
- `DECLARE CONTINUE HANDLER FOR SQLEXCEPTION` per-iteration error handling
- `LEAVE loop_label` exit pattern

**Migration Considerations:**
- Convert to `EXECUTE IMMEDIATE` in Snowflake scripting `FOR` loops (Snowflake scripting supports `FOR rec IN (SELECT ...)`)
- Use Snowflake scripting RESULTSET iteration for more complex cases
- **Consider refactoring to set-based operations** where possible — eliminates cursor overhead entirely
- Teradata `DECLARE CONTINUE HANDLER` → Snowflake `EXCEPTION WHEN OTHER THEN` block
- Snowflake transaction semantics differ: autocommit by default, DDL is auto-committed
- `LEAVE loop_label` → Snowflake uses `BREAK` to exit loops
- May benefit from Snowflake Tasks for scheduled bulk DDL operations

**Effort Estimation:** 16-32 hours per procedure

**Complexity Score:** 85/100

---

## 8. Shape-Changing

**Risk Level:** MEDIUM (50/100)

**Description:** Dynamic column lists, pivot targets, or UNION builders where the result set structure varies at runtime.

**Characteristics:**
- Dynamic SELECT column list built from catalog or config
- Runtime-determined result set shape
- UNION ALL builders across sibling tables
- Column list derived from `DBC.ColumnsV` metadata
- Often used for generic reporting stored procedures

**Example:**
```sql
REPLACE PROCEDURE get_numeric_columns(
  IN p_database   VARCHAR(100),
  IN p_table_name VARCHAR(100)
)
BEGIN
  DECLARE sql_text VARCHAR(64000) DEFAULT '';
  DECLARE col_name VARCHAR(100);
  DECLARE first_col BYTEINT DEFAULT 1;

  DECLARE col_cur CURSOR FOR
    SELECT ColumnName
    FROM DBC.ColumnsV
    WHERE DatabaseName = p_database
      AND TableName    = p_table_name
      AND ColumnType   IN ('I', 'I1', 'I2', 'I8', 'F', 'N', 'D')  -- numeric types
    ORDER BY ColumnId;

  OPEN col_cur;

  col_loop:
  LOOP
    FETCH col_cur INTO col_name;
    IF (SQLCODE <> 0) THEN LEAVE col_loop; END IF;

    IF first_col = 0 THEN
      SET sql_text = sql_text || ', ';
    END IF;

    SET sql_text = sql_text || '"' || col_name || '"';
    SET first_col = 0;
  END LOOP col_loop;

  CLOSE col_cur;

  IF CHAR_LENGTH(sql_text) > 0 THEN
    SET sql_text = 'SELECT ' || sql_text
                   || ' FROM "' || p_database || '"."' || p_table_name || '"';
    EXECUTE IMMEDIATE sql_text;
  END IF;
END;
```

**Detection Signals:**
- Cursor over `DBC.ColumnsV` building a column list string
- Pattern: `sql_text = 'SELECT ' || col_list || ' FROM'`
- `XMLAGG(ColumnName || ', ')` aggregation to build column lists
- Dynamic `PIVOT` targets built from distinct values
- Result shape determined by catalog or data at runtime

**Migration Considerations:**
- Use Snowflake `LISTAGG()` or cursor iteration for column list building
- Consider Snowflake `VARIANT` type for semi-structured data — may eliminate need for dynamic column lists in some reporting patterns
- Snowflake supports dynamic PIVOT
- **Teradata column type codes** must be translated to `INFORMATION_SCHEMA.COLUMNS.DATA_TYPE` strings when moving to Snowflake catalog queries (e.g., `'I'` → `'NUMBER'`, `'F'` → `'FLOAT'`)
- Result set structure testing critical — downstream consumers may break
- Document expected result set shape variations

**Effort Estimation:** 8-16 hours per procedure

**Complexity Score:** 50/100

---

## 9. Cross-System I/O

**Risk Level:** MEDIUM-HIGH (65/100)

**Description:** Dynamic cross-system access using Teradata QueryGrid (federated queries to external systems such as Hive, Oracle, or other Teradata systems), or linked-server-style four-part database paths.

**Characteristics:**
- QueryGrid foreign server queries to external data sources
- Dynamic database names across multiple Teradata systems
- Teradata-to-Teradata linked system queries
- Integration with Hadoop/Hive/Oracle via QueryGrid connectors
- Performance considerations for remote data access

**Example:**
```sql
REPLACE PROCEDURE query_foreign_system(
  IN p_foreign_server  VARCHAR(100),
  IN p_remote_database VARCHAR(100),
  IN p_table_name      VARCHAR(100),
  IN p_filter_date     DATE
)
BEGIN
  DECLARE sql_text VARCHAR(10000);

  -- QueryGrid: query across to Hive or remote Teradata
  SET sql_text =
    'SELECT * FROM "' || p_remote_database || '"."' || p_table_name || '"@' || p_foreign_server
    || ' WHERE load_date = ?';

  EXECUTE IMMEDIATE sql_text USING p_filter_date;
END;
```

**Cross-Database Example (within Teradata):**
```sql
REPLACE PROCEDURE consolidate_regions(IN p_report_date DATE)
BEGIN
  DECLARE sql_text VARCHAR(10000);
  DECLARE region   VARCHAR(50);
  DECLARE done     BYTEINT DEFAULT 0;

  DECLARE reg_cur CURSOR FOR
    SELECT DISTINCT DatabaseName
    FROM DBC.DatabasesV
    WHERE DatabaseName LIKE 'REGION_%';

  OPEN reg_cur;
  region_loop:
  LOOP
    FETCH reg_cur INTO region;
    IF (SQLCODE <> 0) THEN LEAVE region_loop; END IF;

    SET sql_text =
      'INSERT INTO consolidated.sales '
      || 'SELECT ''' || region || ''' AS region, * '
      || 'FROM "' || region || '".daily_sales '
      || 'WHERE sale_date = ?';

    EXECUTE IMMEDIATE sql_text USING p_report_date;
  END LOOP region_loop;

  CLOSE reg_cur;
END;
```

**Detection Signals:**
- `@server_name` or `@foreign_server` suffix in table references
- `QueryGrid` or `TD_SYSGPL` references
- Dynamic `DatabaseName` from `DBC.DatabasesV`
- Cross-system consolidation patterns (LIKE `'REGION_%'`, `'ENV_%'`)
- References to external connector names in dynamic SQL

**Migration Considerations:**
- **Snowflake architecture replaces QueryGrid patterns**:
  - Multiple Teradata databases → multiple Snowflake databases within same account (cross-database queries native, no linked-server concept needed)
  - QueryGrid to Hive/Oracle → Snowflake External Tables or partner ETL tools
  - Cross-Teradata-system queries → Snowflake Data Sharing (zero-copy) or database replication
- **Common migration paths**:
  1. Teradata multi-database patterns → Snowflake `DATABASE.SCHEMA.TABLE` three-part names
  2. QueryGrid to Hive → Snowflake External Tables on S3/ADLS/GCS
  3. QueryGrid to Oracle → dedicated ETL pipeline or Snowflake Data Loading
- Often requires **workflow and architecture changes** in addition to SQL rewrites
- Enumerate all foreign servers and connectors before migration planning

**Effort Estimation:** 12-24 hours per procedure

**Complexity Score:** 65/100

---

## 10. Security/Context Switching

**Risk Level:** MEDIUM-HIGH (75/100)

**Description:** Dynamic `GRANT`/`REVOKE`, role manipulation, profile assignment, or runtime security context changes.

**Characteristics:**
- Dynamic privilege management (`GRANT`/`REVOKE` with runtime object/user names)
- Profile and role assignment at runtime
- Database-level access control manipulation
- Teradata TDPID-based connection switching (rare in modern deployments)

**Example:**
```sql
REPLACE PROCEDURE grant_table_access(
  IN p_database  VARCHAR(100),
  IN p_table     VARCHAR(100),
  IN p_user      VARCHAR(100),
  IN p_privilege VARCHAR(50)   -- e.g., 'SELECT', 'INSERT', 'ALL'
)
BEGIN
  DECLARE sql_text VARCHAR(10000);

  SET sql_text =
    'GRANT ' || p_privilege
    || ' ON "' || p_database || '"."' || p_table || '"'
    || ' TO "' || p_user || '"';

  EXECUTE IMMEDIATE sql_text;
END;
```

**Role Switching Example:**
```sql
REPLACE PROCEDURE set_session_role(IN p_role VARCHAR(100))
BEGIN
  DECLARE sql_text VARCHAR(1000);

  SET sql_text = 'SET ROLE "' || p_role || '"';
  EXECUTE IMMEDIATE sql_text;
END;
```

**Detection Signals:**
- `GRANT`/`REVOKE` in dynamic strings
- `SET ROLE` in dynamic SQL
- Dynamic user or role names
- `MODIFY USER` / `CREATE USER` / `CREATE ROLE` in dynamic strings
- `GIVE` statements (Teradata ownership transfer) in dynamic SQL

**Migration Considerations:**
- **Snowflake RBAC model differs from Teradata**:
  - Teradata: user-based and role-based permissions on database/table objects
  - Snowflake: strict RBAC — all permissions assigned to roles, not directly to users
  - Teradata `GIVE` (ownership transfer) → no direct equivalent; use role grants
- **Privilege model differences**:
  - Teradata: `GRANT SELECT ON database TO user` (direct user grants common)
  - Snowflake: `GRANT SELECT ON TABLE ... TO ROLE ...` (role-only grants)
- **Migration strategy**:
  1. Map Teradata users to Snowflake roles
  2. Map Teradata database-level grants to Snowflake schema/table grants on roles
  3. Review stored procedure `EXECUTE AS CALLER` vs `EXECUTE AS OWNER`
  4. May require security model redesign
- **Compliance review required** for security-sensitive procedures
- Test privilege escalation and revocation scenarios

**Effort Estimation:** 12-24 hours per procedure

**Complexity Score:** 75/100

---

## 11. Data-Loading

**Risk Level:** HIGH (70/100)

**Description:** Dynamic data loading via BTEQ scripts with substitution variables, programmatically generated FastLoad/MultiLoad job scripts, or TPT script parameter substitution. Common in ETL procedures and shell-driven automation.

**Characteristics:**
- BTEQ `.IMPORT FILE` / `.RUN FILE` with dynamic file paths
- FastLoad / MultiLoad job scripts built with runtime substitution variables
- TPT operator scripts parameterized via environment variables or config files
- Dynamic `INSERT ... SELECT` from staging volatile tables
- Shell-level string substitution (`&variable` in BTEQ)

**Example (BTEQ with substitution):**
```bteq
/* BTEQ script: load_daily.btq */
.SET TITLEDASHES OFF
.LOGON ${TDPID}/${TDUSER},${TDPASSWD}

DATABASE ${TARGET_DB};

.IMPORT VARTEXT '|'
  FILE=${DATA_PATH}/sales_${LOAD_DATE}.txt
  SKIP 1

USING (
  sale_id        INTEGER,
  sale_date      CHAR(10),
  amount         DECIMAL(12,2)
)
INSERT INTO daily_sales_stg
VALUES (:sale_id, CAST(:sale_date AS DATE FORMAT 'YYYY-MM-DD'), :amount);

.LOGOFF
.QUIT
```

**Example (Dynamic volatile table staging in SPL):**
```sql
REPLACE PROCEDURE load_partitioned_data(
  IN p_database    VARCHAR(100),
  IN p_table_name  VARCHAR(100),
  IN p_load_date   DATE
)
BEGIN
  DECLARE sql_text VARCHAR(10000);

  -- Create volatile staging table
  SET sql_text =
    'CREATE VOLATILE TABLE vt_stage_'
    || CAST(HASHBUCKET(CURRENT_TIMESTAMP) AS VARCHAR(20))
    || ' AS ('
    || '  SELECT * FROM "' || p_database || '"."' || p_table_name || '"'
    || '  WHERE load_date = ?'
    || ') WITH DATA'
    || ' ON COMMIT PRESERVE ROWS';

  EXECUTE IMMEDIATE sql_text USING p_load_date;

  -- Further processing on volatile table...
END;
```

**Detection Signals:**
- BTEQ `.IMPORT` / `.RUN FILE` with `${}` or `&variable` substitution
- `FASTLOAD`/`MULTILOAD` script templates with runtime parameters
- TPT script references with `@variable` substitution
- `CREATE VOLATILE TABLE ... AS (SELECT ...)` with dynamic predicates
- `CAST(x AS DATE FORMAT ...)` for date-driven path construction
- Shell scripts calling `bteq < script.btq` with environment variable injection

**Migration Considerations:**
- **Teradata loading tools → Snowflake equivalents**:
  - BTEQ `.IMPORT` → Snowflake `COPY INTO` (batch) or Snowpipe (continuous)
  - FastLoad → Snowflake `COPY INTO` with parallel file loading
  - MultiLoad → Snowflake `MERGE` + `COPY INTO` pattern
  - TPT Export/Load → Snowflake Connector for Python/Spark, or `PUT` + `COPY`
- **Key differences**:
  - Teradata: file pushed directly into database from host
  - Snowflake: files staged first (`PUT` to internal stage or S3/ADLS/GCS), then `COPY INTO`
- **Volatile table patterns**:
  - Teradata `VOLATILE TABLE` (session-scoped) → Snowflake `TEMPORARY TABLE` (session-scoped)
  - Consider Snowflake CTEs as a simpler alternative for intermediate results
- **Date format handling**: Teradata `DATE FORMAT 'YYYY-MM-DD'` → Snowflake uses ISO 8601 by default
- **BTEQ substitution variables** (`&var`, `${var}`) → migrate to Snowflake scripting variables or SnowSQL variable substitution
- Consider Snowflake Tasks + Streams for event-driven continuous loading

**Effort Estimation:** 16-32 hours per job/procedure (higher if BTEQ orchestration logic is complex)

**Complexity Score:** 70/100

---

## 12. Template/Token Replacement

**Risk Level:** MEDIUM-HIGH (65/100)

**Description:** SQL built from templates by replacing tokens or placeholders — such as `{SCHEMA}`, `<<DATABASE>>`, or `/*FILTER*/` — using `OREPLACE()` or `OTRANSLATE()`.

**Characteristics:**
- Uses `OREPLACE()` (Teradata's `REPLACE()` equivalent) to inject SQL fragments
- Template may come from an application configuration table
- Can obscure whether replacements are values or identifiers
- Common in report-generation frameworks and ETL metadata-driven systems

**Example:**
```sql
REPLACE PROCEDURE execute_report_template(
  IN p_template_name VARCHAR(100),
  IN p_database      VARCHAR(100),
  IN p_filter_clause VARCHAR(1000)
)
BEGIN
  DECLARE template   VARCHAR(64000);
  DECLARE sql_text   VARCHAR(64000);

  -- Load template from config table
  SELECT template_sql INTO :template
  FROM report_templates
  WHERE template_name = p_template_name;

  IF template IS NULL THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Template not found';
  END IF;

  -- Replace tokens
  SET sql_text = template;
  SET sql_text = OREPLACE(sql_text, '<<DATABASE>>', p_database);
  SET sql_text = OREPLACE(sql_text, '<<FILTER>>', p_filter_clause);
  SET sql_text = OREPLACE(sql_text, '<<TODAY>>', CAST(CURRENT_DATE AS VARCHAR(10)));

  EXECUTE IMMEDIATE sql_text;
END;
```

**Template Example (stored in `report_templates`):**
```sql
-- template_name: 'daily_revenue'
SELECT
  CAST(txn_date AS DATE FORMAT 'YYYY-MM-DD') AS txn_day,
  SUM(amount) AS revenue
FROM "<<DATABASE>>".transactions
WHERE <<FILTER>>
  AND txn_date = DATE '<<TODAY>>'
GROUP BY 1
ORDER BY 1 DESC
```

**Detection Signals:**
- `OREPLACE(sql_text, ...)` calls to inject SQL fragments
- Token-like markers in SQL text: `{...}`, `<<...>>`, `/*...*/`, `[PLACEHOLDER]`
- Template variables fetched from a config/metadata table before `EXECUTE IMMEDIATE`
- Multiple `OREPLACE()` calls on the same SQL string variable
- `OTRANSLATE()` used for character-level substitution in SQL strings

**Migration Considerations:**
- `OREPLACE()` → Snowflake `REPLACE()` (same semantics, different function name)
- **Prefer refactoring to explicit logic** (transforms naturally into Clause-Assembly pattern)
- If templates must remain:
  - **Strictly separate value vs identifier replacements**
  - **Values** → convert to bound parameters with `USING`
  - **Identifiers** → whitelist + `IDENTIFIER()` in Snowflake
- **Security review critical**: templates can hide injection vulnerabilities when `<<FILTER>>` tokens accept arbitrary SQL
- Document all template sources and their replacement logic
- Consider dbt or Jinja templating as a managed alternative

**Effort Estimation:** 8-20 hours per procedure

**Complexity Score:** 65/100

---

## 13. Macro-Driven

**Risk Level:** MEDIUM (50/100)

**Description:** Teradata Macros (`REPLACE MACRO` / `EXEC macro_name(...)`) used as parameterized SQL templates. Macros are a Teradata-unique object type — they execute one or more SQL statements with typed parameters and are stored in the database like procedures.

**Characteristics:**
- `REPLACE MACRO` defines a parameterized SQL block stored as a database object
- Called via `EXEC macro_name(value1, value2)` or `EXECUTE macro_name(...)`
- Support multiple SQL statements separated by semicolons
- Often used as lightweight "parameterized views" or report runners
- Can be called dynamically: `EXECUTE IMMEDIATE 'EXEC ' || macro_name || '(' || params || ')'`

**Example (Static Macro Definition):**
```sql
REPLACE MACRO get_customer_orders (
  p_customer_id INTEGER,
  p_start_date  DATE
) (
  SELECT
    order_id,
    order_date,
    total_amount
  FROM sales.orders
  WHERE customer_id = :p_customer_id
    AND order_date  >= :p_start_date
  ORDER BY order_date DESC;
);
```

**Called as:**
```sql
EXEC get_customer_orders(12345, DATE '2024-01-01');
```

**Dynamic Macro Invocation Example:**
```sql
REPLACE PROCEDURE run_report_macro(
  IN p_macro_name VARCHAR(100),
  IN p_param1     VARCHAR(200),
  IN p_param2     VARCHAR(200)
)
BEGIN
  DECLARE sql_text VARCHAR(10000);

  -- Dynamically invoke a macro by name
  SET sql_text =
    'EXEC "' || p_macro_name || '"('
    || '''' || p_param1 || ''','
    || '''' || p_param2 || '''' || ')';

  EXECUTE IMMEDIATE sql_text;
END;
```

**Detection Signals:**
- `REPLACE MACRO` / `CREATE MACRO` DDL
- `EXEC macro_name(...)` or `EXECUTE macro_name(...)` calls
- Dynamic macro name construction: `'EXEC ' || macro_var || '(...)'`
- References to `DBC.TVM` or `DBC.TablesV WHERE TableKind = 'M'` (macros stored as kind 'M')
- Macro parameter references using `:param_name` notation

**Migration Considerations:**
- **No direct Snowflake equivalent** — macros must be migrated to one of:
  1. **Snowflake Stored Procedure**: best for multi-statement macros with logic
  2. **Snowflake Parameterized View** (via SQL expression): best for single SELECT macros
  3. **Snowflake UDF**: best for expression-level computation macros
- **Migration strategy by macro type**:
  - Single `SELECT` macro → Snowflake stored procedure returning a RESULTSET, or a view with parameters simulated via stored procedure
  - Multi-statement macro → Snowflake stored procedure
  - Reporting/summary macro → Snowflake stored procedure or dbt model
- **Dynamic macro invocation** (calling macro by name at runtime): convert to `CALL stored_proc_name(...)` with `EXECUTE IMMEDIATE 'CALL ' || proc_name || '(...)'`
- Enumerate all macros via `SELECT * FROM DBC.TablesV WHERE TableKind = 'M'` before migration
- Check macro ownership and privileges — map to Snowflake role-based grants on procedures

**Effort Estimation:** 4-12 hours per macro (simpler than stored procedures)

**Complexity Score:** 50/100

---

## 14. Query-Band/Session-Parameter-Driven

**Risk Level:** LOW-MEDIUM (35/100)

**Description:** Dynamic SQL used to set `SET QUERY_BAND` or other session-level parameters at runtime for workload identification, chargeback reporting, TASM/TIWM routing, or session behavior control.

**Characteristics:**
- `SET QUERY_BAND` with dynamically assembled key=value strings for workload management
- Runtime workload routing via TASM (Teradata Active System Management) / TIWM
- Session-level parameter tuning (`SET SESSION COLLATION`, `SET SESSION DATEFORM`, etc.)
- Often used by application frameworks to tag queries for chargeback and monitoring

**Example:**
```sql
REPLACE PROCEDURE run_tagged_query(
  IN p_app_name      VARCHAR(100),
  IN p_workload_name VARCHAR(100),
  IN p_query         VARCHAR(64000)
)
BEGIN
  DECLARE band_text VARCHAR(1000);

  -- Build query band string dynamically
  SET band_text =
    'AppName=' || p_app_name
    || ';WorkloadName=' || p_workload_name
    || ';UserName=' || USER
    || ';SubmitTime=' || CAST(CURRENT_TIMESTAMP AS VARCHAR(26))
    || ';';

  EXECUTE IMMEDIATE 'SET QUERY_BAND = ? FOR TRANSACTION' USING band_text;

  -- Execute the actual query
  EXECUTE IMMEDIATE p_query;
END;
```

**Session Parameter Example:**
```sql
REPLACE PROCEDURE configure_session(
  IN p_dateform  VARCHAR(20),  -- 'ANSIDATE' or 'INTEGERDATE'
  IN p_collation VARCHAR(50)   -- e.g., 'ASCII', 'EBCDIC'
)
BEGIN
  EXECUTE IMMEDIATE 'SET SESSION DATEFORM = ' || p_dateform;
  EXECUTE IMMEDIATE 'SET SESSION COLLATION ' || p_collation;
END;
```

**Detection Signals:**
- `SET QUERY_BAND = ... FOR SESSION/TRANSACTION` in dynamic strings
- `'AppName='` / `'WorkloadName='` / `'BillingCode='` string building patterns
- `SET SESSION DATEFORM` / `SET SESSION COLLATION` in dynamic SQL
- `SET SESSION ACCOUNT` for chargeback
- `SET TIME ZONE` or `SET SESSION TIME ZONE` in dynamic strings

**Migration Considerations:**
- **Workload management paradigm shift**:
  - Teradata: TASM/TIWM routes sessions based on QUERY_BAND key-value pairs
  - Snowflake: virtual warehouse selection + resource monitors control workloads
- **Parameter mapping**:
  - `SET QUERY_BAND 'AppName=X'` → `ALTER SESSION SET QUERY_TAG = 'AppName=X'`
  - TASM workload routing → use dedicated Snowflake warehouses per workload class
  - `SET SESSION DATEFORM = ANSIDATE` → not needed; Snowflake uses ISO 8601 by default
  - `SET SESSION COLLATION` → Snowflake uses Unicode collation; no direct equivalent
- **Most Teradata session parameters can be removed**: Snowflake handles date/collation automatically
- **`QUERY_TAG` in Snowflake**: `ALTER SESSION SET QUERY_TAG = '...'` for monitoring and cost attribution
- Review if dynamic session parameter setting is still needed post-migration

**Effort Estimation:** 2-8 hours per procedure

**Complexity Score:** 35/100

---

## Multi-Pattern Classification

Objects often exhibit multiple patterns. **Tag with all applicable patterns**.

**Example — Multiple Patterns:**
```sql
REPLACE PROCEDURE rebuild_schema(IN p_database VARCHAR(100))
BEGIN
  DECLARE sql_text VARCHAR(10000);
  DECLARE tbl_name VARCHAR(100);

  DECLARE tbl_cur CURSOR FOR
    SELECT TableName              -- Data-Driven: DBC catalog query
    FROM DBC.TablesV
    WHERE DatabaseName = p_database
      AND TableKind    = 'T'
    ORDER BY TableName;

  OPEN tbl_cur;

  rebuild_loop:
  LOOP                            -- Cursor-Driven DDL: iterate over objects
    FETCH tbl_cur INTO tbl_name;
    IF (SQLCODE <> 0) THEN LEAVE rebuild_loop; END IF;

    SET sql_text =
      'DROP TABLE "' || p_database || '"."' || tbl_name || '"';
    EXECUTE IMMEDIATE sql_text;   -- DDL-Driven: dynamic DROP

    SET sql_text =
      'CREATE SET TABLE "' || p_database || '"."' || tbl_name || '" '
      || '(id INTEGER NOT NULL, val VARCHAR(1000)) '
      || 'PRIMARY INDEX (id)';
    EXECUTE IMMEDIATE sql_text;   -- DDL-Driven: dynamic CREATE
  END LOOP rebuild_loop;

  CLOSE tbl_cur;
END;
```

**Patterns Present:** `Data-Driven | DDL-Driven | Cursor-Driven DDL | Identifier-Driven`

**Tagging Guidelines:**
- Identify **all** applicable patterns
- Use pipe separator: `"Pattern1 | Pattern2 | Pattern3"`
- List primary pattern first, additional patterns following
- Document rationale in justification notes
- If `Unsafe-Value-Concatenation` is present, **always include it**

---

## Teradata → Snowflake Migration Quick Reference

### Syntax Translation

| Teradata | Snowflake | Notes |
|----------|-----------|-------|
| `EXECUTE IMMEDIATE sql` | `EXECUTE IMMEDIATE sql` | Identical syntax — simplest migration |
| `EXECUTE IMMEDIATE sql USING v1, v2` | `EXECUTE IMMEDIATE sql USING (v1, v2)` | Add parentheses around USING args |
| `?` parameter placeholder | `$1`, `$2`, ... | Change positional placeholder syntax |
| `'"' \|\| name \|\| '"'` | `IDENTIFIER(name)` | Use built-in function |
| `OREPLACE(str, from, to)` | `REPLACE(str, from, to)` | Different function name |
| `DBC.TablesV` | `INFORMATION_SCHEMA.TABLES` | Entirely different catalog |
| `DBC.ColumnsV` | `INFORMATION_SCHEMA.COLUMNS` | Entirely different catalog |
| `DBC.DatabasesV` | `INFORMATION_SCHEMA.SCHEMATA` | Entirely different catalog |
| `DBC.IndicesV` | `INFORMATION_SCHEMA.TABLE_CONSTRAINTS` | Partial equivalent |
| `REPLACE MACRO m (p TYPE) (sql;)` | Stored procedure or view | No macro object type in Snowflake |
| `EXEC macro_name(val)` | `CALL proc_name(val)` | Call syntax change |
| `VOLATILE TABLE` | `TEMPORARY TABLE` | Similar semantics; auto-drop at session end |
| `CREATE SET TABLE` | `CREATE TABLE` | No SET/MULTISET in Snowflake |
| `BT` / `ET` (BTEQ) | `BEGIN TRANSACTION` / `COMMIT` | Explicit scripting equivalent |
| `SET QUERY_BAND = '...'` | `ALTER SESSION SET QUERY_TAG = '...'` | Workload tagging |
| `SET SESSION DATEFORM` | Not needed | Snowflake uses ISO 8601 |
| `LEAVE loop_label` | `BREAK` | Exit from loop |
| `DECLARE CONTINUE HANDLER FOR SQLEXCEPTION` | `EXCEPTION WHEN OTHER THEN` | Error handler syntax |
| `SIGNAL SQLSTATE '45000'` | `RAISE` | Raise user-defined exception |
| `HASHBUCKET(x)` | No direct equivalent; use `MD5()` or `UUID_STRING()` | For unique name generation |
| `CHAR_LENGTH(x)` | `LENGTH(x)` | String length function |
| `CAST(x AS DATE FORMAT 'YYYY-MM-DD')` | `TO_DATE(x, 'YYYY-MM-DD')` | Date parsing |

### Architecture Translation

| Teradata Feature | Snowflake Equivalent | Migration Notes |
|------------------|---------------------|-----------------|
| Primary Index (PI/UPI) | Clustering keys | Different purpose; PI is mandatory in Teradata, optional in Snowflake |
| Partition Primary Index (PPI) | Automatic micro-partitioning | Snowflake partitions automatically; no manual PPI needed |
| FALLBACK protection | Automatic replication | Snowflake replicates data automatically; remove FALLBACK |
| COMPRESS column values | Automatic compression | Snowflake compresses automatically; remove COMPRESS |
| Volatile tables | Temporary tables | Similar session-scoped semantics |
| Global Temporary Tables | Temporary tables | Definition persists in Snowflake; data per session |
| Teradata Macros | Stored procedures / Views | Migrate by type (SELECT → procedure/view, multi-stmt → procedure) |
| FastLoad | `COPY INTO` | Batch file load; stage files first with `PUT` |
| MultiLoad | `COPY INTO` + `MERGE` | For upsert patterns; use `MERGE` statement |
| BTEQ scripts | SnowSQL scripts / Python | Replace `.IMPORT`, `.RUN FILE` with Snowflake equivalents |
| TPT (Teradata PT) | Snowflake Connector / Spark | Replace TPT operators with Snowflake connectors |
| DBC catalog | INFORMATION_SCHEMA | Completely different; requires full catalog query rewrite |
| SET QUERY_BAND | ALTER SESSION SET QUERY_TAG | Simpler key=value string |
| TASM/TIWM workload routing | Warehouse selection + resource monitors | Architecture shift; use dedicated warehouses per workload |
| QueryGrid to Hive/Oracle | External Tables / ETL pipelines | Architecture decision required |
| Teradata sessions/TDPID | Snowflake connection strings | Connection model differs |

### Common Refactoring Patterns

1. **Parameter binding**: Change `?` placeholders to `$1`, `$2`, ... and add parentheses to `USING` clause
2. **Identifier handling**: Replace manual `'"' || name || '"'` with `IDENTIFIER(name)`
3. **Catalog rewrites**: Replace all `DBC.*` queries with `INFORMATION_SCHEMA.*` equivalents
4. **Macro migration**: Convert `REPLACE MACRO` to stored procedures or views based on macro type
5. **Remove Teradata DDL options**: Strip `PRIMARY INDEX`, `FALLBACK`, `COMPRESS`, `SET`/`MULTISET`, `JOURNAL` clauses
6. **Cursor conversion**: Replace `DECLARE/OPEN/FETCH/CLOSE` with Snowflake scripting `FOR rec IN (SELECT ...)` loops
7. **Volatile tables**: Change `VOLATILE TABLE` to `TEMPORARY TABLE`; review if CTE suffices
8. **Date formats**: Remove `DATE FORMAT` casts; use `TO_DATE()` / `TO_TIMESTAMP()` with explicit format strings
9. **Session parameters**: Remove `SET SESSION DATEFORM`, `SET SESSION COLLATION`; migrate `QUERY_BAND` to `QUERY_TAG`
10. **Loading migration**: Replace BTEQ/FastLoad/MultiLoad with `PUT` + `COPY INTO` + `MERGE` patterns

### Testing Checklist

- [ ] All `?` parameter bindings converted to `$1`, `$2`, ... and USING parentheses added
- [ ] Identifier case sensitivity handled (Teradata case-insensitive vs Snowflake uppercase default)
- [ ] No Teradata-specific DDL remains (PI, PPI, FALLBACK, COMPRESS, JOURNAL, SET/MULTISET)
- [ ] All `DBC.*` catalog queries rewritten to `INFORMATION_SCHEMA.*`
- [ ] All macros migrated to stored procedures or views
- [ ] Cursor loops converted to Snowflake scripting `FOR` loops or RESULTSET iteration
- [ ] Volatile tables converted to `TEMPORARY TABLE` or replaced with CTEs
- [ ] Date format handling verified (Teradata `DATE FORMAT` vs Snowflake `TO_DATE`)
- [ ] Error handling ported correctly (`DECLARE CONTINUE HANDLER` → `EXCEPTION WHEN OTHER THEN`)
- [ ] `LEAVE label` replaced with `BREAK`
- [ ] Data loading jobs tested end-to-end (`PUT` staging + `COPY INTO`)
- [ ] QUERY_BAND converted to QUERY_TAG and workload routing reviewed
- [ ] Performance acceptable (verify clustering keys replace critical Primary Index access patterns)
- [ ] Security model validated (Teradata user grants → Snowflake role-based grants)
- [ ] All code paths tested including error/exception branches
