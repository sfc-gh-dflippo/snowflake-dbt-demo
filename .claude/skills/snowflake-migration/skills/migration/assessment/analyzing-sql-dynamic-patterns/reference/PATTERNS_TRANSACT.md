# SQL Dynamic Pattern Definitions (SQL Server → Snowflake)

Pattern catalog for **SQL Server to Snowflake** dynamic SQL migration analysis.

## How to tag (critical for consistent classification)

- **Tag all that apply**: Real stored procedures frequently match multiple patterns.
- **If values are concatenated, always tag `Unsafe-Value-Concatenation`** even if other patterns are also present.
- **Distinguish values vs identifiers**:
  - **Values**: strings/numbers/dates used in predicates/expressions. Should be **bound parameters** (not injected into SQL text).
  - **Identifiers**: schema/table/column names, ORDER BY columns, procedure names. Should be **whitelisted** and properly quoted.
- **Dynamic ≠ unsafe**: parameterized `sp_executesql` is dynamic but low risk.
- **Snowflake mapping shortcut**:
  - SQL Server: `EXEC(@sql)` / `sp_executesql`
  - Snowflake Scripting: `EXECUTE IMMEDIATE <sql_text> [USING (...)]`
  - Snowflake identifiers: `IDENTIFIER(<string_expr>)`

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
11. [Trigger/Procedural Embedded](#11-triggerprocedural-embedded)
12. [Template/Token Replacement](#12-templatetoken-replacement)
13. [Hint/Option-Driven](#13-hintoption-driven)

[Multi-Pattern Classification](#multi-pattern-classification)

---

## 1. Unsafe-Value-Concatenation

**Risk Level:** HIGH (75/100)

**Description:** Direct concatenation of **data values** into SQL text (especially predicates) without parameterization, creating SQL injection vulnerabilities.

**Characteristics:**
- Direct value concatenation into SQL strings
- No `sp_executesql` parameter declaration
- `EXEC(@sql)` without bound parameters
- String concatenation with `'''` quote escaping

**Example:**
```sql
DECLARE @sql NVARCHAR(MAX)
SET @sql = 'SELECT * FROM Users WHERE Username = ''' + @Username + ''''
EXEC(@sql)
```

**Detection Signals:**
- Pattern: `@sql = '...' + @parameter + '...'` (data values)
- `CAST(@param AS VARCHAR)` for concatenation
- No `@params` declaration with `sp_executesql`
- Quote helpers near concatenation: `CHAR(39)`, `REPLACE(x,'''','''''')`

**Migration Considerations:**
- Refactor to proper parameter binding
- Add input validation
- Use `IDENTIFIER()` for object names only, never values

**Effort Estimation:** 8-16 hours

**Complexity Score:** 75/100

---

## 2. Parameter-Driven

**Risk Level:** LOW (15/100)

**Description:** Fixed SQL structure with only values varying through proper parameterization. No string concatenation.

**Characteristics:**
- Static SQL structure
- Uses `sp_executesql` with parameter declaration
- No concatenation of keywords/clauses/identifiers
- Excellent query plan reuse

**Example:**
```sql
DECLARE @sql NVARCHAR(MAX), @params NVARCHAR(MAX)
SET @params = N'@StartDate DATE, @Status VARCHAR(50)'
SET @sql = N'SELECT * FROM Orders WHERE OrderDate >= @StartDate AND Status = @Status'
EXEC sp_executesql @sql, @params, @StartDate = @StartDate, @Status = @Status
```

**Detection Signals:**
- `sp_executesql` with `@params` declaration
- Parameter placeholders: `@p0`, `@paramName`
- No SQL keyword/clause concatenation

**Migration Considerations:**
- Straightforward conversion to Snowflake (Snowflake Scripting `EXECUTE IMMEDIATE ... USING`)
- Minimal refactoring needed

**Effort Estimation:** 2-4 hours

**Complexity Score:** 15/100

---

## 3. Identifier-Driven

**Risk Level:** MEDIUM (45/100)

**Description:** Dynamic **identifiers** (tables, columns, schemas, ORDER BY columns, procedure names) built at runtime.

**Characteristics:**
- Dynamic table/column/schema names
- Uses `QUOTENAME()` for escaping
- Requires whitelist validation
- Platform identifier handling differences

**Example:**
```sql
DECLARE @sql NVARCHAR(MAX)
SET @sql = N'SELECT ' + QUOTENAME(@ColumnName) + 
           N' FROM ' + QUOTENAME(@SchemaName) + '.' + QUOTENAME(@TableName)
EXEC sp_executesql @sql
```

**Detection Signals:**
- `QUOTENAME(@table|@col|@schema)`
- String concatenation: `'FROM ' + @tbl`
- Dynamic column selection
- Concatenation near `ORDER BY`, `JOIN`, or `EXEC` that injects an identifier

**Migration Considerations:**
- Use Snowflake `IDENTIFIER()` function
- Implement whitelist validation
- Handle identifier case sensitivity differences

**Effort Estimation:** 6-12 hours

**Complexity Score:** 45/100

---

## 4. Clause-Assembly

**Risk Level:** MEDIUM (55/100)

**Description:** Conditional addition of `WHERE`/`ORDER BY`/`GROUP BY` fragments based on runtime conditions (query text structure changes across executions).

**Characteristics:**
- Base SQL with conditional clause additions
- Common: `WHERE 1=1` + conditional ANDs
- Runtime-determined filtering/sorting
- Query structure changes per execution

**Example:**
```sql
DECLARE @sql NVARCHAR(MAX)
DECLARE @params NVARCHAR(MAX) = N'@Name NVARCHAR(100), @City NVARCHAR(100)'

SET @sql = N'SELECT CustomerId, Name, City FROM dbo.Customers WHERE 1=1'
IF @Name IS NOT NULL
    SET @sql += N' AND Name LIKE ''%'' + @Name + ''%'''
IF @City IS NOT NULL
    SET @sql += N' AND City = @City'

-- NOTE: dynamic ORDER BY is Identifier-Driven; keep it separate (whitelist + QUOTENAME) if present.
EXEC sp_executesql @sql, @params, @Name = @Name, @City = @City
```

**Detection Signals:**
- `WHERE 1=1` pattern
- Conditional concatenation: `IF @param IS NOT NULL SET @sql = @sql + ...`
- Dynamic `ORDER BY`/`GROUP BY`

**Migration Considerations:**
- Refactor to `WHERE` with `OR NULL` pattern
- Use `CASE` for conditional ordering
- Proper parameter binding

**Effort Estimation:** 8-16 hours

**Complexity Score:** 55/100

---

## 5. Data-Driven

**Risk Level:** MEDIUM-HIGH (70/100)

**Description:** SQL assembled from database metadata or configuration tables (object lists, column lists, config-driven filters, etc.).

**Characteristics:**
- Queries `sys.*` or `INFORMATION_SCHEMA.*`
- Uses `STRING_AGG`/`FOR XML PATH` to build SQL
- Loop-based SQL construction from data
- Environment-dependent behavior

**Example:**
```sql
DECLARE @sql NVARCHAR(MAX) = N''
SELECT @sql = @sql + 
    'SELECT ''' + TABLE_NAME + ''' AS Source, * FROM ' + 
    QUOTENAME(TABLE_SCHEMA) + '.' + QUOTENAME(TABLE_NAME) + ' UNION ALL '
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_TYPE = 'BASE TABLE'
SET @sql = LEFT(@sql, LEN(@sql) - 11)
EXEC sp_executesql @sql
```

**Detection Signals:**
- Queries to `sys.*` or `INFORMATION_SCHEMA.*`
- `STRING_AGG()` into `@sql` variable
- Cursor/loop with SQL string appends
- Often co-occurs with `Identifier-Driven` (object names) and sometimes `DDL-Driven`

**Migration Considerations:**
- Metadata catalog differences
- Use `LISTAGG` instead of `FOR XML PATH`
- Test across environments
- Document metadata dependencies

**Effort Estimation:** 16-32 hours

**Complexity Score:** 70/100

---

## 6. DDL-Driven

**Risk Level:** HIGH (80/100)

**Description:** Dynamic DDL (CREATE/ALTER/DROP) generation and execution.

**Characteristics:**
- Dynamic schema modifications
- CREATE/ALTER/DROP in dynamic SQL
- Often paired with metadata queries
- Platform-specific DDL syntax

**Example:**
```sql
DECLARE @sql NVARCHAR(MAX)
SET @sql = N'ALTER TABLE ' + QUOTENAME(@TableName) + 
           N' ADD AuditDate DATETIME2 DEFAULT GETDATE()'
EXEC sp_executesql @sql
```

**Detection Signals:**
- `CREATE TABLE/VIEW/INDEX` in dynamic string
- `ALTER TABLE/COLUMN` statements
- `DROP` statements
- Schema evolution patterns

**Migration Considerations:**
- Review if DDL should be procedural or deploy-time
- Snowflake DDL differences (no clustered indexes)
- Consider Schema Evolution features
- May move to CI/CD pipeline

**Effort Estimation:** 12-24 hours

**Complexity Score:** 80/100

---

## 7. Cursor-Driven DDL

**Risk Level:** HIGH (85/100)

**Description:** Cursor/loop iterating over objects executing DDL per object.

**Characteristics:**
- `CURSOR` or `WHILE` loop over metadata
- DDL execution inside loop
- Bulk schema operations
- Error handling complexity

**Example:**
```sql
DECLARE @TableName SYSNAME, @sql NVARCHAR(MAX)
DECLARE table_cursor CURSOR FOR
    SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'dbo'
OPEN table_cursor
FETCH NEXT FROM table_cursor INTO @TableName
WHILE @@FETCH_STATUS = 0
BEGIN
    SET @sql = N'ALTER TABLE ' + QUOTENAME(@TableName) + N' ADD UpdatedDate DATETIME2'
    EXEC sp_executesql @sql
    FETCH NEXT FROM table_cursor INTO @TableName
END
CLOSE table_cursor
DEALLOCATE table_cursor
```

**Detection Signals:**
- `DECLARE CURSOR` + `ALTER/CREATE/DROP`
- `WHILE @@FETCH_STATUS` patterns
- `EXEC(@sql)` inside loop
- Metadata query as cursor source

**Migration Considerations:**
- Convert to `EXECUTE IMMEDIATE` in loop
- Use Snowflake scripting (ResultSet iteration)
- Consider refactoring to set-based operations
- Manual review for optimization

**Effort Estimation:** 16-32 hours (or 8-16h with optimization)

**Complexity Score:** 85/100

---

## 8. Shape-Changing

**Risk Level:** MEDIUM (50/100)

**Description:** Dynamic column lists, PIVOT targets, or UNION builders.

**Characteristics:**
- Dynamic SELECT column list
- PIVOT with runtime-determined IN list
- UNION ALL builders across tables
- Column list from metadata/config

**Example:**
```sql
DECLARE @sql NVARCHAR(MAX), @cols NVARCHAR(MAX)
SELECT @cols = STRING_AGG(QUOTENAME(CategoryName), ',') FROM Categories
SET @sql = N'SELECT * FROM (
    SELECT ProductName, ' + QUOTENAME(@CategoryColumn) + ', Sales FROM ProductSales
) AS src PIVOT (SUM(Sales) FOR ' + QUOTENAME(@CategoryColumn) + ' IN (' + @cols + ')) AS pvt'
EXEC sp_executesql @sql
```

**Detection Signals:**
- Dynamic `@cols` list from data
- `STRING_AGG()` for column names
- Dynamic `PIVOT ... IN (...)`
- `SELECT ' + @columnList + ' FROM`

**Migration Considerations:**
- Snowflake supports dynamic PIVOT
- Use `LISTAGG()` for column list building
- Consider materialized views
- May leverage VARIANT type

**Effort Estimation:** 8-16 hours

**Complexity Score:** 50/100

---

## 9. Cross-System I/O

**Risk Level:** MEDIUM (50/100)

**Description:** Dynamic cross-system access (linked servers / remote execution), typically via `OPENQUERY`, `OPENROWSET`, `OPENDATASOURCE`, or four-part names.

**Characteristics:**
- Linked server queries to external instances
- Dynamic server/database names
- Distributed query patterns across systems
- Common in legacy/hybrid data ecosystems

**Example:**
```sql
DECLARE @sql NVARCHAR(MAX)
SET @sql = N'SELECT * FROM OPENQUERY(' + QUOTENAME(@ServerName) + ', 
    ''SELECT * FROM ' + @DatabaseName + '.dbo.Customers'')'
EXEC sp_executesql @sql
```

**Detection Signals:**
- `OPENQUERY(` in dynamic SQL
- `OPENROWSET(` with dynamic parameters
- Linked server references
- Cross-instance distributed queries

**Migration Considerations:**
Snowflake often replaces linked-server patterns through logical organization and sharing:
- Use databases/schemas within same account for logical separation
- Cross-database queries native (no linked servers needed)
- Data Sharing for zero-copy sharing across accounts/regions
- Reader Accounts for external consumer access
- Snowpipe or Streams + Tasks for real-time ingestion
- External Tables for external data sources
- Database Replication for cross-region data

Often requires workflow/architecture changes in addition to SQL rewrites.

**Effort Estimation:** 8-16 hours

**Complexity Score:** 50/100

---

## 10. Security/Context Switching

**Risk Level:** MEDIUM-HIGH (75/100)

**Description:** Dynamic `EXECUTE AS`, `GRANT/REVOKE`, or other runtime security/context switching.

**Characteristics:**
- Dynamic privilege management
- Context switching (`EXECUTE AS`)
- Role/permission manipulation
- Database switching

**Example:**
```sql
DECLARE @sql NVARCHAR(MAX)
SET @sql = N'EXECUTE AS USER = ' + QUOTENAME(@UserName, '''') + '; ' + @Query + '; REVERT;'
EXEC sp_executesql @sql
```

**Detection Signals:**
- `EXECUTE AS` in dynamic string
- `GRANT`/`REVOKE` statements
- Dynamic user/role names
- `USE database` switching

**Migration Considerations:**
- Snowflake RBAC model differences
- No `EXECUTE AS` (use role switching)
- Different privilege model
- Security model redesign may be required
- Compliance review needed

**Effort Estimation:** 12-24 hours

**Complexity Score:** 75/100

---

## 11. Trigger/Procedural Embedded

**Risk Level:** HIGH (95/100)

**Description:** Dynamic SQL inside triggers or complex procedural blocks. This is typically the hardest to migrate due to platform semantic differences.

**Characteristics:**
- Dynamic SQL within triggers
- Complex control flow (cursors, TRY/CATCH)
- Trigger-specific variables (`inserted`, `deleted`)
- Platform semantic differences

**Example:**
```sql
CREATE TRIGGER AuditChanges ON Customers AFTER UPDATE
AS BEGIN
    DECLARE @sql NVARCHAR(MAX)
    -- Example intentionally uses parameterization; real-world triggers often mix multiple patterns.
    SET @sql = N'INSERT INTO dbo.AuditLog(TableName, Action, Actor)
                 SELECT @TableName, ''UPDATE'', SYSTEM_USER FROM inserted'
    EXEC sp_executesql @sql, N'@TableName SYSNAME', @TableName = @TableName
END
```

**Detection Signals:**
- `CREATE TRIGGER ... EXEC(@sql)`
- Dynamic SQL inside `TRY/CATCH`
- References to `inserted`/`deleted` tables
- Complex nested transaction logic

**Migration Considerations:**
- Snowflake trigger support limited
- Convert to Streams + Tasks
- Use Snowflake Scripting
- Semantic differences require testing
- Consider event-driven alternatives

**Effort Estimation:** 24-48 hours

**Complexity Score:** 95/100

---

## 12. Template/Token Replacement

**Risk Level:** MEDIUM-HIGH (65/100)

**Description:** SQL is built from a template by replacing tokens (macros/placeholders) such as `{WHERE}`, `<<Schema>>`, `@TOKEN@`, or `/*PLACEHOLDER*/`.

**Characteristics:**
- Uses `REPLACE()` / `STUFF()` / `FORMATMESSAGE()` or custom string functions to inject fragments
- Template may come from a config table or be composed across multiple variables
- Can hide whether the replacement is a **value** (unsafe) or an **identifier** (needs whitelist)

**Example:**
```sql
DECLARE @template NVARCHAR(MAX) = N'SELECT * FROM dbo.Orders WHERE /*FILTER*/'
DECLARE @sql NVARCHAR(MAX) = REPLACE(@template, '/*FILTER*/', N'Status = @Status')
EXEC sp_executesql @sql, N'@Status NVARCHAR(50)', @Status = @Status
```

**Detection Signals:**
- `REPLACE(@sql|@template, ...)`, `STUFF(...)` used to inject SQL fragments
- Token-like markers in SQL text: `{...}`, `/*...*/`, `<<...>>`, `@TOKEN@`

**Migration Considerations:**
- Prefer refactoring to explicit logic (often becomes Clause-Assembly)
- If templates remain, strictly separate:
  - **Values** → bound parameters
  - **Identifiers** → whitelist + quoting / Snowflake `IDENTIFIER()`

**Effort Estimation:** 8-20 hours

**Complexity Score:** 65/100

---

## 13. Hint/Option-Driven

**Risk Level:** MEDIUM (55/100)

**Description:** Dynamic SQL is used primarily to choose hints/options at runtime (index hints, `OPTION(...)`, join hints, table hints like `WITH (NOLOCK)`).

**Characteristics:**
- Appends or toggles hints based on parameters/environment
- Often co-occurs with Clause-Assembly, but the motivation is plan/perf control

**Example:**
```sql
DECLARE @sql NVARCHAR(MAX) = N'SELECT * FROM dbo.FactSales WHERE SaleDate >= @StartDate'
IF @ForceRecompile = 1
  SET @sql += N' OPTION (RECOMPILE)'
EXEC sp_executesql @sql, N'@StartDate DATE', @StartDate = @StartDate
```

**Detection Signals:**
- `OPTION (` in dynamic strings
- `WITH (` table hints in dynamic strings
- `INDEX(` hints / join hints constructed at runtime

**Migration Considerations:**
- Many SQL Server hints do not exist in Snowflake; reassess intent and remove first
- Reintroduce Snowflake-native performance controls if needed (clustering, pruning-friendly predicates, caching behavior)

**Effort Estimation:** 6-16 hours

**Complexity Score:** 55/100

---

## Multi-Pattern Classification

Objects often exhibit multiple patterns. Tag with all applicable patterns.

**Example:**
```sql
-- Patterns: Data-Driven + DDL-Driven + Cursor-Driven DDL
DECLARE table_cursor CURSOR FOR
    SELECT TABLE_NAME FROM sys.tables WHERE type = 'U'  -- Data-Driven
OPEN table_cursor
FETCH NEXT FROM table_cursor INTO @table
WHILE @@FETCH_STATUS = 0  -- Cursor-Driven DDL
BEGIN
    SET @sql = 'ALTER TABLE ' + @table + ' ADD AuditCol DATETIME'  -- DDL-Driven
    EXEC(@sql)
    FETCH NEXT FROM table_cursor INTO @table
END
```
