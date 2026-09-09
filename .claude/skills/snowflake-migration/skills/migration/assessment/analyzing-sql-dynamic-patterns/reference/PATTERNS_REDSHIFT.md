# SQL Dynamic Pattern Definitions (Redshift → Snowflake)

Pattern catalog for **Amazon Redshift to Snowflake** dynamic SQL migration analysis.

## How to tag (critical for consistent classification)

- **Tag all that apply**: Real stored procedures frequently match multiple patterns.
- **If values are concatenated, always tag `Unsafe-Value-Concatenation`** even if other patterns are also present.
- **Distinguish values vs identifiers**:
  - **Values**: strings/numbers/dates used in predicates/expressions. Should be **bound parameters** (not injected into SQL text).
  - **Identifiers**: schema/table/column names, ORDER BY columns, procedure names. Should be **whitelisted** and properly quoted.
- **Dynamic ≠ unsafe**: parameterized `EXECUTE` with USING clause is dynamic but low risk.
- **Snowflake mapping shortcut**:
  - Redshift: `EXECUTE <sql_text> [USING (...)]`
  - Snowflake Scripting: `EXECUTE IMMEDIATE <sql_text> [USING (...)]`
  - Snowflake identifiers: `IDENTIFIER(<string_expr>)`

## Redshift Language Context

**Key Redshift Characteristics:**
- Based on PostgreSQL 8.0.2 with proprietary extensions
- Stored procedures use PL/pgSQL language (`LANGUAGE plpgsql`)
- Parameter binding with `EXECUTE ... USING` and `$1, $2, ...` placeholders
- Identifier quoting: `QUOTE_IDENT()` for object names
- Literal quoting: `QUOTE_LITERAL()` for string values
- String concatenation: `||` operator
- Metadata catalogs: `pg_catalog.*` and `information_schema.*`
- Session context switching: `SET SESSION AUTHORIZATION`
- Workload management: `query_group`, `wlm_query_slot_count`
- **No user-defined triggers** on tables (key limitation vs PostgreSQL)
- Transaction control: `COMMIT`/`ROLLBACK` within procedures
- External data access: External schemas (Federated Query), Redshift Spectrum (S3)

## Table of Contents

1. [Unsafe-Value-Concatenation](#1-unsafe-value-concatenation)
2. [Parameter-Driven](#2-parameter-driven)
3. [Identifier-Driven](#3-identifier-driven)
4. [Clause-Assembly](#4-clause-assembly)
5. [Data-Driven](#5-data-driven)
6. [DDL-Driven](#6-ddl-driven)
7. [Loop-Driven DDL](#7-loop-driven-ddl)
8. [Shape-Changing](#8-shape-changing)
9. [Cross-System I/O](#9-cross-system-io)
10. [Security/Context Switching](#10-securitycontext-switching)
11. [Data-Loading](#11-data-loading)
12. [Template/Token Replacement](#12-templatetoken-replacement)
13. [Session-Parameter-Driven](#13-session-parameter-driven)
14. [Temporary-Table-Driven](#14-temporary-table-driven)

[Multi-Pattern Classification](#multi-pattern-classification)

---

## 1. Unsafe-Value-Concatenation

**Risk Level:** MEDIUM (40/100)

**Description:** Direct concatenation of **data values** into SQL text (especially predicates) without parameterization, creating SQL injection vulnerabilities.

**Characteristics:**
- Direct value concatenation into SQL strings using `||` operator
- No `USING` clause for parameter binding
- `EXECUTE` without bound parameters
- String concatenation with `'''` quote escaping or `QUOTE_LITERAL()`
- Values embedded directly in WHERE clauses, INSERT statements, or UPDATE operations

**Example:**
```sql
CREATE OR REPLACE PROCEDURE search_user(p_username VARCHAR(100))
AS $$
DECLARE
  sql_text VARCHAR(65535);
BEGIN
  -- UNSAFE: Direct value concatenation
  sql_text := 'SELECT user_id, email FROM users WHERE username = ''' || p_username || '''';
  EXECUTE sql_text;
END;
$$ LANGUAGE plpgsql;
```

**Detection Signals:**
- Pattern: `sql_text := '...' || variable || '...'` where variable is a data value
- `variable::VARCHAR` for concatenation
- No `USING` clause with `EXECUTE`
- `QUOTE_LITERAL()` used for values (still unsafe if input unvalidated)
- Quote escaping patterns: `'''` or `''''`
- Concatenation in WHERE predicates, VALUES lists, or SET clauses

**Migration Considerations:**
- **Critical**: Refactor to proper parameter binding using `EXECUTE IMMEDIATE ... USING`
- Add input validation and sanitization
- Never use `IDENTIFIER()` for data values in Snowflake
- Consider stored procedure privilege changes (owner rights vs caller rights)
- Test with SQL injection attack vectors to verify fixes

**Effort Estimation:** 4-8 hours per procedure

**Complexity Score:** 40/100

---

## 2. Parameter-Driven

**Risk Level:** LOW (15/100)

**Description:** Fixed SQL structure with only values varying through proper parameterization using `USING` clause. No string concatenation of SQL structure.

**Characteristics:**
- Static SQL structure
- Uses `EXECUTE ... USING` with bind parameters
- No concatenation of keywords/clauses/identifiers
- Excellent query plan reuse in Redshift
- Best practice for dynamic SQL

**Example:**
```sql
CREATE OR REPLACE PROCEDURE get_orders_by_date(
  p_start_date DATE,
  p_status VARCHAR(50)
)
AS $$
DECLARE
  sql_text VARCHAR(65535);
BEGIN
  sql_text := 'SELECT order_id, customer_id, total_amount
               FROM orders
               WHERE order_date >= $1 AND status = $2
               ORDER BY order_date DESC';

  EXECUTE sql_text USING p_start_date, p_status;
END;
$$ LANGUAGE plpgsql;
```

**Detection Signals:**
- `EXECUTE ... USING` pattern with no concatenation
- Parameter placeholders: `$1`, `$2`, `$3`, etc.
- No SQL keyword/clause concatenation
- Fixed query structure
- Bind variables passed to `USING` clause

**Migration Considerations:**
- **Easiest migration path**: Direct conversion to Snowflake `EXECUTE IMMEDIATE ... USING`
- Minimal refactoring needed
- Parameter syntax identical (`$1`, `$2`, etc.)
- May not require dynamic SQL at all in Snowflake (consider static SQL alternative)

**Effort Estimation:** 2-4 hours per procedure

**Complexity Score:** 15/100

---

## 3. Identifier-Driven

**Risk Level:** MEDIUM (45/100)

**Description:** Dynamic **identifiers** (tables, columns, schemas, ORDER BY columns, procedure names) built at runtime.

**Characteristics:**
- Dynamic table/column/schema/database names
- Uses `QUOTE_IDENT()` for proper escaping
- Requires whitelist validation for security
- Case sensitivity considerations (Redshift lowercase vs Snowflake uppercase default)

**Example:**
```sql
CREATE OR REPLACE PROCEDURE query_table(
  p_schema_name VARCHAR(100),
  p_table_name VARCHAR(100),
  p_column_name VARCHAR(100)
)
AS $$
DECLARE
  sql_text VARCHAR(65535);
BEGIN
  -- Validate identifiers against whitelist here
  sql_text := 'SELECT ' || QUOTE_IDENT(p_column_name) ||
              ' FROM ' || QUOTE_IDENT(p_schema_name) || '.' || QUOTE_IDENT(p_table_name) ||
              ' LIMIT 100';

  EXECUTE sql_text;
END;
$$ LANGUAGE plpgsql;
```

**Detection Signals:**
- `QUOTE_IDENT(variable)` function calls
- String concatenation: `'FROM ' || table_var`
- Dynamic column selection or ORDER BY columns
- Concatenation near `FROM`, `JOIN`, `ORDER BY`, or `GROUP BY`
- Variables containing object names

**Migration Considerations:**
- Use Snowflake `IDENTIFIER()` function instead of `QUOTE_IDENT()`
- **Implement strict whitelist validation** (query `INFORMATION_SCHEMA` to validate)
- Handle identifier case sensitivity:
  - Redshift: unquoted identifiers default to lowercase
  - Snowflake: unquoted identifiers default to uppercase
- Consider using fully-qualified names: `database.schema.table`
- Test with mixed-case object names

**Effort Estimation:** 6-12 hours per procedure

**Complexity Score:** 45/100

---

## 4. Clause-Assembly

**Risk Level:** MEDIUM (55/100)

**Description:** Conditional addition of `WHERE`/`ORDER BY`/`GROUP BY` fragments based on runtime conditions. Query structure changes across executions.

**Characteristics:**
- Base SQL with conditional clause additions
- Common pattern: `WHERE 1=1` + conditional ANDs
- Runtime-determined filtering/sorting/grouping
- Query structure varies per execution path
- Often paired with parameter binding

**Example:**
```sql
CREATE OR REPLACE PROCEDURE search_customers(
  p_name_filter VARCHAR(100),
  p_city_filter VARCHAR(100),
  p_status_filter VARCHAR(50)
)
AS $$
DECLARE
  sql_text VARCHAR(65535);
  param_count INT := 0;
BEGIN
  sql_text := 'SELECT customer_id, name, city, status FROM customers WHERE 1=1';

  -- Conditionally add filter clauses
  IF p_name_filter IS NOT NULL THEN
    param_count := param_count + 1;
    sql_text := sql_text || ' AND name ILIKE $' || param_count::VARCHAR;
  END IF;

  IF p_city_filter IS NOT NULL THEN
    param_count := param_count + 1;
    sql_text := sql_text || ' AND city = $' || param_count::VARCHAR;
  END IF;

  IF p_status_filter IS NOT NULL THEN
    param_count := param_count + 1;
    sql_text := sql_text || ' AND status = $' || param_count::VARCHAR;
  END IF;

  sql_text := sql_text || ' ORDER BY name';

  EXECUTE sql_text USING p_name_filter, p_city_filter, p_status_filter;
END;
$$ LANGUAGE plpgsql;
```

**Detection Signals:**
- `WHERE 1=1` pattern (common starting point)
- Conditional concatenation: `IF condition THEN sql_text := sql_text || ...`
- Dynamic `ORDER BY` or `GROUP BY` clauses
- `USING` clause with variable parameter counts
- Building parameter placeholders dynamically: `'$' || counter::VARCHAR`

**Migration Considerations:**
- Snowflake alternative: Use `WHERE` with `OR NULL` pattern for simpler cases
- Use `CASE` expressions for conditional ordering
- Consider Snowflake's flexible `WHERE` clause patterns
- May not need dynamic SQL if using `WHERE (condition OR input IS NULL)`
- Test all conditional paths thoroughly

**Effort Estimation:** 8-16 hours per procedure

**Complexity Score:** 55/100

---

## 5. Data-Driven

**Risk Level:** MEDIUM-HIGH (70/100)

**Description:** SQL assembled from database metadata or configuration tables. Object lists, column lists, config-driven filters.

**Characteristics:**
- Queries `pg_catalog.*` or `information_schema.*` tables
- Uses `LISTAGG()` or `STRING_AGG()` to build SQL fragments
- Loop-based SQL construction from query results
- Environment-dependent behavior (different databases/schemas produce different SQL)

**Example:**
```sql
CREATE OR REPLACE PROCEDURE union_all_tables(p_schema VARCHAR(100))
AS $$
DECLARE
  sql_text VARCHAR(65535) := '';
  table_rec RECORD;
  first_table BOOLEAN := TRUE;
BEGIN
  -- Build UNION ALL query from all tables in schema
  FOR table_rec IN
    SELECT table_schema, table_name
    FROM information_schema.tables
    WHERE table_type = 'BASE TABLE'
      AND table_schema = p_schema
    ORDER BY table_name
  LOOP
    IF NOT first_table THEN
      sql_text := sql_text || ' UNION ALL ';
    END IF;

    sql_text := sql_text ||
      'SELECT ''' || table_rec.table_name || ''' AS source_table, * FROM ' ||
      QUOTE_IDENT(table_rec.table_schema) || '.' || QUOTE_IDENT(table_rec.table_name);

    first_table := FALSE;
  END LOOP;

  IF sql_text = '' THEN
    RAISE EXCEPTION 'No tables found in schema %', p_schema;
  END IF;

  EXECUTE sql_text;
END;
$$ LANGUAGE plpgsql;
```

**Detection Signals:**
- Queries to `pg_catalog.*` or `information_schema.*`
- `LISTAGG()` or `STRING_AGG()` functions building SQL text
- `FOR ... LOOP` iterating over metadata with SQL string appends
- Often co-occurs with `Identifier-Driven` pattern
- Environment-specific logic

**Migration Considerations:**
- **Metadata catalog mapping**:
  - `pg_catalog.pg_tables` → `INFORMATION_SCHEMA.TABLES`
  - `pg_catalog.pg_columns` → `INFORMATION_SCHEMA.COLUMNS`
  - `pg_catalog.pg_views` → `INFORMATION_SCHEMA.VIEWS`
- Snowflake `INFORMATION_SCHEMA` is standard SQL compliant
- Consider Snowflake's `SHOW` commands for metadata access
- Use `GET_DDL()` function for object definitions
- **Test across environments** (dev, test, prod may have different schemas)
- Document metadata dependencies clearly
- Consider what happens with schema evolution

**Effort Estimation:** 16-32 hours per procedure

**Complexity Score:** 70/100

---

## 6. DDL-Driven

**Risk Level:** HIGH (70/100)

**Description:** Dynamic DDL (CREATE/ALTER/DROP) generation and execution for schema modifications.

**Characteristics:**
- Dynamic schema modifications
- CREATE/ALTER/DROP statements in dynamic SQL
- Often paired with metadata queries
- Platform-specific DDL syntax differences
- Transaction behavior differences

**Example:**
```sql
CREATE OR REPLACE PROCEDURE add_audit_column(p_table_name VARCHAR(100))
AS $$
DECLARE
  sql_text VARCHAR(65535);
BEGIN
  -- Add audit column to specified table
  sql_text := 'ALTER TABLE ' || QUOTE_IDENT(p_table_name) ||
              ' ADD COLUMN last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP';

  EXECUTE sql_text;
  COMMIT;

  -- Log the change
  INSERT INTO ddl_audit_log (table_name, ddl_type, executed_at)
  VALUES (p_table_name, 'ALTER_TABLE', CURRENT_TIMESTAMP);
  COMMIT;
END;
$$ LANGUAGE plpgsql;
```

**Detection Signals:**
- `CREATE TABLE/VIEW/INDEX/FUNCTION/PROCEDURE` in dynamic strings
- `ALTER TABLE/COLUMN` statements
- `DROP` statements
- Schema evolution patterns
- `COMMIT`/`ROLLBACK` within procedures

**Migration Considerations:**
- **Question if DDL should be procedural**: Many cases better handled by CI/CD pipelines
- **Redshift-specific DDL translation**:
  - Remove: `DISTSTYLE`, `DISTKEY`, `SORTKEY`, `ENCODE`
  - Add: Clustering keys if needed (different syntax and semantics)
- Snowflake DDL differences:
  - No distribution/sort keys
  - Different data types (some automatic conversions)
  - Different default behaviors
- Snowflake's Time Travel and Zero-Copy Cloning may replace some patterns
- Review transaction control (Redshift explicit COMMIT vs Snowflake autocommit)
- Consider moving to Flyway/Liquibase/dbt for schema management

**Effort Estimation:** 12-24 hours per procedure

**Complexity Score:** 70/100

---

## 7. Loop-Driven DDL

**Risk Level:** HIGH (85/100)

**Description:** Loop iterating over objects (typically from metadata queries), executing DDL per object. Bulk schema operations. Most commonly uses `FOR...LOOP` in Redshift (idiomatic), though explicit cursors (DECLARE CURSOR, OPEN, FETCH, CLOSE) are also supported but rarely used.

**Characteristics:**
- `FOR ... LOOP` over metadata queries (most common)
- Explicit cursor iteration (DECLARE/OPEN/FETCH/CLOSE - less common)
- DDL execution inside loop
- Bulk schema operations
- Error handling complexity
- Transaction management across iterations

**Example:**
```sql
CREATE OR REPLACE PROCEDURE add_column_to_all_tables(
  p_schema VARCHAR(100),
  p_column_spec VARCHAR(1000)
)
AS $$
DECLARE
  sql_text VARCHAR(65535);
  table_rec RECORD;
  success_count INT := 0;
  error_count INT := 0;
BEGIN
  FOR table_rec IN
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = p_schema
      AND table_type = 'BASE TABLE'
    ORDER BY table_name
  LOOP
    BEGIN
      sql_text := 'ALTER TABLE ' || QUOTE_IDENT(p_schema) || '.' ||
                  QUOTE_IDENT(table_rec.table_name) ||
                  ' ADD COLUMN ' || p_column_spec;

      EXECUTE sql_text;
      COMMIT;

      success_count := success_count + 1;

    EXCEPTION WHEN OTHERS THEN
      -- Log error and continue
      INSERT INTO ddl_error_log (table_name, error_message, failed_at)
      VALUES (table_rec.table_name, SQLERRM, CURRENT_TIMESTAMP);
      COMMIT;

      error_count := error_count + 1;
    END;
  END LOOP;

  RAISE INFO 'Completed: % success, % errors', success_count, error_count;
END;
$$ LANGUAGE plpgsql;
```

**Detection Signals:**
- `FOR ... LOOP` with `ALTER/CREATE/DROP` inside (most common pattern)
- Explicit cursor patterns: `DECLARE ... CURSOR`, `OPEN`, `FETCH`, `CLOSE` with DDL
- `EXECUTE` inside loop or cursor body
- Metadata query as loop source
- Exception handling per iteration
- Transaction control within loop

**Migration Considerations:**
- Convert to `EXECUTE IMMEDIATE` in Snowflake scripting loops
- Use Snowflake scripting RESULTSET iteration
- **Consider refactoring to set-based operations** where possible
- Review error handling strategy (continue on error vs fail fast)
- Snowflake transaction semantics differ
- Manual review for optimization opportunities
- Consider parallelization for large-scale operations
- May benefit from Snowflake Tasks for scheduling

**Effort Estimation:** 16-32 hours per procedure

**Complexity Score:** 85/100

---

## 8. Shape-Changing

**Risk Level:** MEDIUM (50/100)

**Description:** Dynamic column lists, PIVOT targets, or UNION builders. Result set structure varies at runtime.

**Characteristics:**
- Dynamic SELECT column list
- Runtime-determined result set shape
- UNION ALL builders across tables
- Column list from metadata/config
- Often used for generic reporting procedures

**Example:**
```sql
CREATE OR REPLACE PROCEDURE get_numeric_columns(p_table_name VARCHAR(100))
AS $$
DECLARE
  sql_text VARCHAR(65535);
  cols VARCHAR(65535);
BEGIN
  -- Build column list from metadata
  SELECT LISTAGG(QUOTE_IDENT(column_name), ', ')
  INTO cols
  FROM information_schema.columns
  WHERE table_name = p_table_name
    AND table_schema = 'public'
    AND data_type IN ('integer', 'bigint', 'numeric', 'double precision')
  ORDER BY ordinal_position;

  IF cols IS NULL THEN
    RAISE EXCEPTION 'No numeric columns found in table %', p_table_name;
  END IF;

  sql_text := 'SELECT ' || cols || ' FROM ' || QUOTE_IDENT(p_table_name);

  EXECUTE sql_text;
END;
$$ LANGUAGE plpgsql;
```

**Detection Signals:**
- Dynamic column list construction
- `LISTAGG()` or `STRING_AGG()` for column names
- Pattern: `'SELECT ' || column_list || ' FROM'`
- Metadata queries determining result shape
- PIVOT/UNPIVOT with dynamic targets

**Migration Considerations:**
- Snowflake supports similar dynamic SQL patterns
- Use `LISTAGG()` (Snowflake native) for column list building
- Consider Snowflake `VARIANT` type for semi-structured data
- May leverage Snowflake's PIVOT/UNPIVOT syntax
- **Result set structure testing critical** - downstream consumers may break
- Consider materialized views for stable result shapes
- Document expected result set variations

**Effort Estimation:** 8-16 hours per procedure

**Complexity Score:** 50/100

---

## 9. Cross-System I/O

**Risk Level:** MEDIUM-HIGH (65/100)

**Description:** Dynamic cross-system access via external schemas (Federated Query), Redshift Spectrum (S3 data), or cross-database queries.

**Characteristics:**
- External schema/database queries
- Dynamic database/schema/external source names
- Distributed query patterns
- Integration with external systems (RDS, Aurora, S3)
- Performance considerations for remote data

**Example:**
```sql
CREATE OR REPLACE PROCEDURE query_external_data(
  p_external_schema VARCHAR(100),
  p_table_name VARCHAR(100),
  p_filter VARCHAR(1000)
)
AS $$
DECLARE
  sql_text VARCHAR(65535);
BEGIN
  -- Query external schema (Federated Query) or Spectrum
  sql_text := 'SELECT * FROM ' ||
              QUOTE_IDENT(p_external_schema) || '.' || QUOTE_IDENT(p_table_name);

  IF p_filter IS NOT NULL THEN
    sql_text := sql_text || ' WHERE ' || p_filter;
  END IF;

  sql_text := sql_text || ' LIMIT 1000';

  EXECUTE sql_text;
END;
$$ LANGUAGE plpgsql;
```

**Spectrum Example:**
```sql
CREATE OR REPLACE PROCEDURE query_s3_data(
  p_year INT,
  p_month INT
)
AS $$
DECLARE
  sql_text VARCHAR(65535);
  partition_path VARCHAR(100);
BEGIN
  -- Query Redshift Spectrum external table with dynamic partitions
  partition_path := 'year=' || p_year::VARCHAR || '/month=' || p_month::VARCHAR;

  sql_text := 'SELECT event_type, COUNT(*) as event_count ' ||
              'FROM spectrum.events ' ||
              'WHERE partition_path = ''' || partition_path || ''' ' ||
              'GROUP BY event_type';

  EXECUTE sql_text;
END;
$$ LANGUAGE plpgsql;
```

**Detection Signals:**
- External schema references in dynamic SQL
- `spectrum.` schema prefix
- Dynamic database/schema names for federated queries
- Cross-database query patterns
- S3 path construction
- Partition filtering logic

**Migration Considerations:**
**Snowflake architecture differs significantly**:
- **Native cross-database queries**: No external schemas needed for intra-account queries
  - Use: `DATABASE.SCHEMA.TABLE` syntax
- **External Tables**: Replace Redshift Spectrum
  - Create external tables pointing to S3/Azure/GCS
  - Use external stages for data location
- **Data Sharing**: Zero-copy data sharing across accounts/regions
  - Consider for cross-account data access
- **Database Replication**: For cross-region scenarios
- **Snowpipe**: For continuous data ingestion from external sources
- **Streams + Tasks**: For event-driven processing

**Common migration paths**:
1. Federated Query to RDS → Snowflake database within same account
2. Redshift Spectrum → Snowflake External Tables
3. External schemas → Snowflake Data Sharing (if cross-account)

Often requires **workflow/architecture changes** in addition to SQL rewrites.

**Effort Estimation:** 12-24 hours per procedure

**Complexity Score:** 65/100

---

## 10. Security/Context Switching

**Risk Level:** MEDIUM-HIGH (75/100)

**Description:** Dynamic `SET SESSION AUTHORIZATION`, `GRANT/REVOKE`, role switching, or runtime security/context changes.

**Characteristics:**
- Dynamic privilege management
- Session context switching
- Role/permission manipulation at runtime
- Schema/search path switching
- Security-critical operations

**Example:**
```sql
CREATE OR REPLACE PROCEDURE execute_as_user(
  p_username VARCHAR(100),
  p_query VARCHAR(65535)
)
AS $$
DECLARE
  sql_text VARCHAR(65535);
  original_user VARCHAR(100);
BEGIN
  -- Save current user
  SELECT CURRENT_USER INTO original_user;

  -- Switch session authorization
  sql_text := 'SET SESSION AUTHORIZATION ' || QUOTE_IDENT(p_username);
  EXECUTE sql_text;

  -- Execute query as switched user
  EXECUTE p_query;

  -- Restore original authorization
  sql_text := 'SET SESSION AUTHORIZATION ' || QUOTE_IDENT(original_user);
  EXECUTE sql_text;

EXCEPTION WHEN OTHERS THEN
  -- Always restore authorization on error
  sql_text := 'SET SESSION AUTHORIZATION ' || QUOTE_IDENT(original_user);
  EXECUTE sql_text;
  RAISE;
END;
$$ LANGUAGE plpgsql;
```

**Grant/Revoke Example:**
```sql
CREATE OR REPLACE PROCEDURE grant_table_access(
  p_table_name VARCHAR(100),
  p_user_name VARCHAR(100),
  p_privilege VARCHAR(50)
)
AS $$
DECLARE
  sql_text VARCHAR(65535);
BEGIN
  -- Dynamic GRANT statement
  sql_text := 'GRANT ' || p_privilege ||
              ' ON TABLE ' || QUOTE_IDENT(p_table_name) ||
              ' TO ' || QUOTE_IDENT(p_user_name);

  EXECUTE sql_text;
  COMMIT;

  -- Audit the grant
  INSERT INTO access_audit_log (table_name, user_name, privilege, granted_at)
  VALUES (p_table_name, p_user_name, p_privilege, CURRENT_TIMESTAMP);
  COMMIT;
END;
$$ LANGUAGE plpgsql;
```

**Detection Signals:**
- `SET SESSION AUTHORIZATION` in dynamic strings
- `SET ROLE` switching
- `GRANT`/`REVOKE` statements
- Dynamic user/role names
- `SET search_path` modifications
- Security context changes

**Migration Considerations:**
- **Snowflake RBAC model fundamentally different**:
  - No `SET SESSION AUTHORIZATION` equivalent
  - Use `USE ROLE` for role switching (but limited context)
  - Stored procedures execute with **owner rights** or **caller rights**
- **Privilege model differences**:
  - Redshift: User and group-based permissions
  - Snowflake: Role-based access control (RBAC)
- **Migration strategy**:
  1. Map Redshift users/groups to Snowflake roles
  2. Review which procedures need owner vs caller rights
  3. Consider stored procedure `EXECUTE AS` clause
  4. May require architecture redesign for security model
- **Compliance review required** for security-sensitive procedures
- Test privilege escalation scenarios thoroughly

**Effort Estimation:** 12-24 hours per procedure

**Complexity Score:** 75/100

---

## 11. Data-Loading

**Risk Level:** MEDIUM-HIGH (60/100)

**Description:** Dynamic `COPY` commands for loading data from S3, Redshift Spectrum, or other sources. Common in ETL procedures.

**Characteristics:**
- Dynamic COPY FROM commands
- S3 path construction
- Dynamic credential management
- File format variations
- Error handling for data loads

**Example:**
```sql
CREATE OR REPLACE PROCEDURE load_daily_data(
  p_table_name VARCHAR(100),
  p_date DATE,
  p_file_format VARCHAR(50)
)
AS $$
DECLARE
  sql_text VARCHAR(65535);
  s3_path VARCHAR(1000);
  copy_options VARCHAR(1000);
BEGIN
  -- Build S3 path
  s3_path := 's3://my-bucket/data/' || p_table_name || '/' ||
             'year=' || EXTRACT(YEAR FROM p_date)::VARCHAR || '/' ||
             'month=' || LPAD(EXTRACT(MONTH FROM p_date)::VARCHAR, 2, '0') || '/' ||
             'day=' || LPAD(EXTRACT(DAY FROM p_date)::VARCHAR, 2, '0') || '/';

  -- Set copy options based on format
  IF p_file_format = 'CSV' THEN
    copy_options := 'CSV IGNOREHEADER 1 DELIMITER '','' REMOVEQUOTES';
  ELSIF p_file_format = 'JSON' THEN
    copy_options := 'JSON ''auto''';
  ELSIF p_file_format = 'PARQUET' THEN
    copy_options := 'FORMAT AS PARQUET';
  ELSE
    RAISE EXCEPTION 'Unsupported file format: %', p_file_format;
  END IF;

  -- Build and execute COPY command
  sql_text := 'COPY ' || QUOTE_IDENT(p_table_name) ||
              ' FROM ''' || s3_path || ''' ' ||
              ' IAM_ROLE ''arn:aws:iam::123456789012:role/RedshiftCopyRole'' ' ||
              copy_options ||
              ' MAXERROR 100 ' ||
              ' COMPUPDATE OFF ' ||
              ' STATUPDATE OFF';

  EXECUTE sql_text;
  COMMIT;

  -- Log successful load
  INSERT INTO data_load_log (table_name, load_date, s3_path, rows_loaded, loaded_at)
  VALUES (p_table_name, p_date, s3_path,
          (SELECT pg_last_copy_count()), CURRENT_TIMESTAMP);
  COMMIT;

END;
$$ LANGUAGE plpgsql;
```

**Detection Signals:**
- `COPY ... FROM` in dynamic strings
- S3 path construction with `'s3://'` prefix
- IAM role or credential references
- Format specifications: `CSV`, `JSON`, `PARQUET`, `AVRO`, `ORC`
- COPY options: `DELIMITER`, `IGNOREHEADER`, `MAXERROR`, `COMPUPDATE`, etc.
- `pg_last_copy_count()` or `pg_last_copy_id()` function calls

**Migration Considerations:**
- **Redshift COPY → Snowflake COPY equivalents**:
  - Similar syntax but different options
  - Snowflake uses Stages instead of direct S3 paths (though external locations supported)
- **Key differences**:
  - Redshift: `IAM_ROLE` for authentication
  - Snowflake: Storage integrations or direct credentials
- **File format mapping**:
  - CSV: Similar, different option names
  - JSON: Snowflake has powerful JSON parsing
  - Parquet: Supported, better performance in Snowflake
- **Consider Snowflake alternatives**:
  - **Snowpipe**: Automated, continuous loading
  - **External Tables**: Query without loading
  - **Streams + Tasks**: Event-driven loads
- **Error handling**: Snowflake's `VALIDATION_MODE` for dry runs
- **Monitoring**: Different metadata functions

**Example Snowflake equivalent:**
```sql
-- Snowflake version
COPY INTO IDENTIFIER(:p_table_name)
FROM (SELECT * FROM @my_stage/path/)
FILE_FORMAT = (TYPE = CSV FIELD_DELIMITER = ',' SKIP_HEADER = 1)
ON_ERROR = 'CONTINUE'
RETURN_FAILED_ONLY = FALSE;
```

**Effort Estimation:** 8-20 hours per procedure

**Complexity Score:** 60/100

---

## 12. Template/Token Replacement

**Risk Level:** MEDIUM-HIGH (65/100)

**Description:** SQL built from templates by replacing tokens/macros such as `{WHERE}`, `<<Schema>>`, or `/*PLACEHOLDER*/`.

**Characteristics:**
- Uses `REPLACE()` to inject SQL fragments
- Template may come from configuration table
- Can obscure whether replacements are values or identifiers
- Often uses custom functions for template processing
- May load templates from external sources

**Example:**
```sql
CREATE OR REPLACE PROCEDURE execute_template(
  p_template_name VARCHAR(100),
  p_schema_name VARCHAR(100),
  p_filter_clause VARCHAR(1000)
)
AS $$
DECLARE
  template VARCHAR(65535);
  sql_text VARCHAR(65535);
BEGIN
  -- Load template from config table
  SELECT template_sql INTO template
  FROM sql_templates
  WHERE template_name = p_template_name;

  IF template IS NULL THEN
    RAISE EXCEPTION 'Template not found: %', p_template_name;
  END IF;

  -- Replace tokens
  sql_text := template;
  sql_text := REPLACE(sql_text, '/*SCHEMA*/', QUOTE_IDENT(p_schema_name));
  sql_text := REPLACE(sql_text, '/*FILTER*/', p_filter_clause);
  sql_text := REPLACE(sql_text, '/*DATE*/', CURRENT_DATE::VARCHAR);

  EXECUTE sql_text;
END;
$$ LANGUAGE plpgsql;
```

**Template Example:**
```sql
-- Template stored in sql_templates table:
-- template_name: 'daily_summary'
-- template_sql:
SELECT
  DATE_TRUNC('day', transaction_date) AS day,
  COUNT(*) AS transaction_count,
  SUM(amount) AS total_amount
FROM /*SCHEMA*/.transactions
WHERE /*FILTER*/
  AND transaction_date = '/*DATE*/'
GROUP BY 1
ORDER BY 1 DESC
```

**Detection Signals:**
- `REPLACE(sql_text, ...)` to inject SQL fragments
- Token-like markers: `{...}`, `/*...*/`, `<<...>>`, `{{TOKEN}}`
- Template variables or template table queries
- Config-driven SQL construction
- Multiple `REPLACE()` calls on same SQL string

**Migration Considerations:**
- **Prefer refactoring to explicit logic** (Clause-Assembly pattern)
- If templates must remain:
  - **Strictly separate value vs identifier replacements**
  - **Values** → convert to bound parameters with `USING`
  - **Identifiers** → whitelist + proper quoting / Snowflake `IDENTIFIER()`
- **Security review critical**: Templates can hide injection vulnerabilities
- Document template sources and replacement logic
- Consider Snowflake JavaScript UDFs for complex templating
- May benefit from external templating engine (dbt, etc.)

**Effort Estimation:** 8-20 hours per procedure

**Complexity Score:** 65/100

---

## 13. Session-Parameter-Driven

**Risk Level:** LOW-MEDIUM (40/100)

**Description:** Dynamic SQL to control query execution behavior through session parameters, workload management, or query settings.

**Characteristics:**
- Runtime query behavior control
- Workload management configuration
- Query group/slot assignment
- Session parameter tuning
- Execution parameter control

**Example:**
```sql
CREATE OR REPLACE PROCEDURE run_heavy_query(
  p_query_group VARCHAR(100),
  p_slot_count INT,
  p_query VARCHAR(65535)
)
AS $$
DECLARE
  sql_text VARCHAR(65535);
BEGIN
  -- Set query group for workload management
  sql_text := 'SET query_group TO ' || QUOTE_LITERAL(p_query_group);
  EXECUTE sql_text;

  -- Allocate more slots for large query
  sql_text := 'SET wlm_query_slot_count TO ' || p_slot_count::VARCHAR;
  EXECUTE sql_text;

  -- Enable result caching
  EXECUTE 'SET enable_result_cache_for_session TO ON';

  -- Execute the query
  EXECUTE p_query;

  -- Reset parameters
  EXECUTE 'RESET query_group';
  EXECUTE 'RESET wlm_query_slot_count';
  EXECUTE 'RESET enable_result_cache_for_session';

EXCEPTION WHEN OTHERS THEN
  -- Always reset on error
  EXECUTE 'RESET query_group';
  EXECUTE 'RESET wlm_query_slot_count';
  EXECUTE 'RESET enable_result_cache_for_session';
  RAISE;
END;
$$ LANGUAGE plpgsql;
```

**Detection Signals:**
- `SET query_group` in dynamic strings
- `SET wlm_query_slot_count` patterns
- `SET enable_result_cache_for_session`
- Dynamic session parameter settings
- `RESET` statements for cleanup
- Query execution control patterns

**Migration Considerations:**
- **Workload management paradigm shift**:
  - Redshift: WLM with query groups and slot counts
  - Snowflake: Virtual warehouse sizing and resource monitors
- **Parameter mapping**:
  - `query_group` → Snowflake query tags or warehouse selection
  - `wlm_query_slot_count` → Snowflake warehouse size (not direct equivalent)
  - `enable_result_cache_for_session` → Snowflake has automatic result caching
- **Snowflake alternatives**:
  - Use different warehouses for different workloads
  - Set warehouse size dynamically: `ALTER WAREHOUSE ... SET WAREHOUSE_SIZE = ...`
  - Use query tags for monitoring: `ALTER SESSION SET QUERY_TAG = '...'`
  - Resource monitors for cost control
- **Most Redshift session parameters can be removed** - Snowflake handles automatically
- Review if dynamic parameter setting still needed

**Effort Estimation:** 4-12 hours per procedure

**Complexity Score:** 40/100

---

## 14. Temporary-Table-Driven

**Risk Level:** MEDIUM (50/100)

**Description:** Dynamic creation and manipulation of temporary tables for intermediate processing.

**Characteristics:**
- Dynamic `CREATE TEMP TABLE` statements
- Temp table names generated at runtime
- Session-scoped temporary storage
- ETL staging patterns
- Multi-step data transformations

**Example:**
```sql
CREATE OR REPLACE PROCEDURE process_with_temp_tables(
  p_source_table VARCHAR(100),
  p_filter_date DATE
)
AS $$
DECLARE
  sql_text VARCHAR(65535);
  temp_table_name VARCHAR(100);
  session_id VARCHAR(50);
BEGIN
  -- Generate unique temp table name
  SELECT CURRENT_SESSION_ID()::VARCHAR INTO session_id;
  temp_table_name := 'temp_processing_' || session_id;

  -- Create temp table dynamically
  sql_text := 'CREATE TEMP TABLE ' || QUOTE_IDENT(temp_table_name) || ' AS ' ||
              'SELECT * FROM ' || QUOTE_IDENT(p_source_table) ||
              ' WHERE process_date = $1';
  EXECUTE sql_text USING p_filter_date;

  -- Process data in temp table
  sql_text := 'UPDATE ' || QUOTE_IDENT(temp_table_name) ||
              ' SET processed_flag = TRUE, processed_at = CURRENT_TIMESTAMP ' ||
              'WHERE status = ''PENDING''';
  EXECUTE sql_text;

  -- Copy results back
  sql_text := 'INSERT INTO ' || QUOTE_IDENT(p_source_table) ||
              ' SELECT * FROM ' || QUOTE_IDENT(temp_table_name);
  EXECUTE sql_text;
  COMMIT;

  -- Temp table automatically dropped at session end
END;
$$ LANGUAGE plpgsql;
```

**Detection Signals:**
- `CREATE TEMP TABLE` or `CREATE TEMPORARY TABLE` in dynamic SQL
- Dynamic temp table name generation
- `DROP TABLE IF EXISTS` for temp tables
- Session ID or timestamp-based naming
- Multi-step processing with intermediate storage

**Migration Considerations:**
- **Snowflake temp tables**:
  - Similar concept but different lifetime semantics
  - `TEMPORARY` keyword supported
  - Automatically dropped at session end
- **Snowflake transient tables** as alternative:
  - Persist beyond session but no Time Travel/Fail-safe
  - Better for short-term storage
- **Consider Snowflake CTEs** (WITH clauses) as alternative:
  - May eliminate need for temp tables
  - Better performance for simple cases
- **Transaction behavior**:
  - Redshift: Explicit COMMIT needed
  - Snowflake: Autocommit by default
- **Naming conventions**: Ensure uniqueness across concurrent sessions

**Effort Estimation:** 6-12 hours per procedure

**Complexity Score:** 50/100

---

## Multi-Pattern Classification

Objects often exhibit multiple patterns. **Tag with all applicable patterns**.

**Example - Multiple Patterns:**
```sql
CREATE OR REPLACE PROCEDURE rebuild_schema_tables(p_schema VARCHAR(100))
AS $$
DECLARE
  sql_text VARCHAR(65535);
  table_rec RECORD;
BEGIN
  FOR table_rec IN
    SELECT table_name                    -- Data-Driven: Metadata query
    FROM information_schema.tables
    WHERE table_schema = p_schema
      AND table_type = 'BASE TABLE'
  LOOP                                   -- Loop-Driven DDL: Iterate over objects
    -- Drop and recreate table
    sql_text := 'DROP TABLE IF EXISTS ' ||
                QUOTE_IDENT(p_schema) || '.' ||
                QUOTE_IDENT(table_rec.table_name);
    EXECUTE sql_text;                    -- DDL-Driven: Dynamic DDL
    COMMIT;

    sql_text := 'CREATE TABLE ' ||
                QUOTE_IDENT(p_schema) || '.' ||
                QUOTE_IDENT(table_rec.table_name) ||
                ' (id INT, data VARCHAR(1000))';
    EXECUTE sql_text;                    -- DDL-Driven: Dynamic DDL
    COMMIT;
  END LOOP;
END;
$$ LANGUAGE plpgsql;
```

**Patterns Present:** `Data-Driven | DDL-Driven | Loop-Driven DDL`

**Tagging Guidelines:**
- Identify **all** applicable patterns
- Use pipe separator: `"Pattern1 | Pattern2 | Pattern3"`
- List primary pattern first, additional patterns following
- Document rationale in justification notes
- If `Unsafe-Value-Concatenation` present, **always include it**

---

## Redshift → Snowflake Migration Quick Reference

### Syntax Translation

| Redshift | Snowflake | Notes |
|----------|-----------|-------|
| `EXECUTE sql_text` | `EXECUTE IMMEDIATE sql_text` | Add IMMEDIATE keyword |
| `QUOTE_IDENT()` | `IDENTIFIER()` | Different function name |
| `QUOTE_LITERAL()` | Avoid; use `USING` binding | Prefer parameters |
| `$1, $2, $3` | `$1, $2, $3` | Same parameter syntax |
| `LANGUAGE plpgsql` | Snowflake Scripting | Different language |
| `pg_catalog.*` | `INFORMATION_SCHEMA.*` | Metadata catalog |
| `information_schema.*` | `INFORMATION_SCHEMA.*` | Case may differ |
| `COMMIT` within proc | Not needed | Autocommit default |
| `FOR rec IN SELECT` | `FOR rec IN (SELECT)` | Slight syntax difference |
| `RECORD` type | Explicit types or RESULTSET | No generic RECORD type |

### Architecture Translation

| Redshift Feature | Snowflake Equivalent | Migration Notes |
|------------------|---------------------|-----------------|
| Distribution keys (DISTKEY) | Clustering keys | Different purpose and behavior |
| Sort keys (SORTKEY) | Clustering keys | Different implementation |
| Workload Management (WLM) | Warehouse sizing + Resource Monitors | Paradigm shift |
| Query groups | Query tags + Warehouse selection | Different approach |
| External schemas (Federated) | Cross-database queries or Data Sharing | Usually not needed |
| Redshift Spectrum | External Tables | Similar concept |
| IAM roles for COPY | Storage Integrations | Different auth model |
| `pg_last_copy_count()` | Query history or COPY result | Different metadata access |

### Common Refactoring Patterns

1. **Parameter binding**: Convert unsafe concatenation to `USING` clause
2. **Identifier handling**: Replace `QUOTE_IDENT()` with `IDENTIFIER()`
3. **Remove WLM code**: Replace with warehouse sizing decisions
4. **Simplify DDL**: Remove Redshift-specific DDL options
5. **Metadata queries**: Update catalog references
6. **Transaction control**: Remove explicit COMMITs (unless needed)
7. **RECORD type**: Replace with explicit column types

### Testing Checklist

- [ ] All parameter bindings work correctly
- [ ] Identifier case sensitivity handled (lowercase vs uppercase)
- [ ] No Redshift-specific DDL remains (DISTKEY, SORTKEY, etc.)
- [ ] Metadata queries return expected results
- [ ] Error handling works as expected
- [ ] Transaction boundaries correct
- [ ] Performance acceptable (may need warehouse sizing)
- [ ] Security model properly implemented
- [ ] All code paths tested (including error cases)
- [ ] External data access works (if applicable)
