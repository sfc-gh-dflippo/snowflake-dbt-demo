# SSC-EWI-0030 - Dynamic SQL Conversion

Convert SQL Server dynamic SQL strings to valid Snowflake syntax.

## Quick Reference

| SQL Server | Snowflake |
|------------|-----------|
| `[identifier]` | Unquoted or `"identifier"` (see rules below) |
| `'a' + 'b'` | `'a' \|\| 'b'` |
| `@variable` | `:variable` |
| `#temp_table` | `t_temp_table` |
| `EXEC(@sql)` | `sp_executesql` | `EXECUTE IMMEDIATE :sql` |
| `LIKE '[A-Z]%'` | `REGEXP_LIKE(col, '^[A-Z].*')` |
| `LIKE '%[^abc]%'` | `REGEXP_LIKE(col, '.*[^abc].*')` |
| `COLLATE Latin1_General_CI_AI` | `COLLATE 'en-ci'` or use `'i'` flag in REGEXP |

## Identifier Quoting Rules

When converting `[identifier]` from SQL Server:

| Condition | Action | Example |
|-----------|--------|---------|
| Simple alphanumeric | Remove brackets, leave unquoted | `[MyTable]` → `MyTable` |
| Contains spaces | Use double quotes | `[My Table]` → `"My Table"` |
| Contains special chars | Use double quotes | `[Order-Details]` → `"Order-Details"` |
| Snowflake reserved word | Use double quotes | `[SELECT]` → `"SELECT"` |
| Starts with number | Use double quotes | `[123Table]` → `"123Table"` |

**Common Snowflake reserved words:** `SELECT`, `FROM`, `WHERE`, `ORDER`, `GROUP`, `TABLE`, `VIEW`, `DATABASE`, `SCHEMA`, `COLUMN`, `ROW`, `VALUES`, `SET`, `UPDATE`, `DELETE`, `INSERT`, `CREATE`, `DROP`, `ALTER`, `GRANT`, `REVOKE`, `JOIN`, `LEFT`, `RIGHT`, `INNER`, `OUTER`, `CROSS`, `UNION`, `CASE`, `WHEN`, `TRUE`, `FALSE`, `NULL`, `AND`, `OR`, `NOT`, `IN`, `BETWEEN`, `LIKE`, `ILIKE`, `REGEXP`, `RLIKE`

For the complete list, see [Snowflake Reserved Keywords](https://docs.snowflake.com/en/sql-reference/reserved-keywords).

## System Catalog Mappings

| SQL Server | Snowflake |
|------------|-----------|
| `sys.objects` | `sys.tables` | `INFORMATION_SCHEMA.TABLES` |
| `sys.schemas` | `INFORMATION_SCHEMA.SCHEMATA` |
| `sys.columns` | `INFORMATION_SCHEMA.COLUMNS` |
| `sys.procedures` | `INFORMATION_SCHEMA.PROCEDURES` |
| `sys.views` | `INFORMATION_SCHEMA.VIEWS` |
| `sys.databases` | `INFORMATION_SCHEMA.DATABASES` |

**Column mappings:**
- `so.name` → `TABLE_NAME`
- `ss.name` → `TABLE_SCHEMA`
- `so.type_desc` → `TABLE_TYPE`
- `schema_id` joins → Not needed (schema included in view)

## Variable Transformation

SQL Server variables (`@variable`) must be converted to Snowflake syntax:

| Context | SQL Server | Snowflake |
|---------|------------|-----------|
| Variable reference in procedure | `@myvar` | `:myvar` |
| Variable in dynamic SQL string (interpolated) | `' + @myvar + '` | `' \|\| :myvar \|\| '` |
| Variable declaration | `DECLARE @myvar INT` | `myvar INT` (in DECLARE block) |
| Variable assignment | `SET @myvar = 1` | `myvar := 1` |

**Important:** Apply this transformation to ALL variable occurrences - in the procedure code AND inside dynamic SQL strings.

## Temp Table Transformation

SQL Server temp tables (`#table_name`) must be converted to Snowflake temporary tables with `t_` prefix:

| SQL Server | Snowflake |
|------------|-----------|
| `#temp_table` | `t_temp_table` |
| `#MyTemp` | `t_MyTemp` |
| `##global_temp` | `t_global_temp` |

**Important:** Apply this transformation to ALL occurrences in the dynamic SQL string - table creation, inserts, selects, joins, drops, etc.

## Commented-Out Dynamic SQL

SnowConvert may comment out dynamic SQL statements that it couldn't fully convert. Look for patterns like:

```sql
EXECUTE IMMEDIATE '--CREATE SCHEMA Planning';
```

The `--` inside the string makes the SQL a no-op. If the original intent was to execute valid SQL, you should:

1. **Check if the commented SQL is valid Snowflake grammar**
2. **Uncomment if valid** - remove the `--` prefix from inside the string
3. **Convert if needed** - apply transformations from Quick Reference before uncommenting

### Before (Commented - No-Op)
```sql
EXECUTE IMMEDIATE '--CREATE SCHEMA Planning';
```

### After (Uncommented - Valid Snowflake)
```sql
EXECUTE IMMEDIATE 'CREATE SCHEMA IF NOT EXISTS Planning';
```

### Validation Checklist

Before uncommenting, verify the SQL is valid Snowflake:

| Element | Valid in Snowflake? |
|---------|---------------------|
| `CREATE SCHEMA name` | ✅ Yes |
| `CREATE TABLE ...` | ✅ Check column types |
| `CREATE INDEX ...` | ❌ No - Snowflake auto-indexes |
| `CREATE TRIGGER ...` | ❌ No - Use Streams + Tasks |
| `EXEC stored_proc` | ❌ No - Use `CALL procedure()` |
| `SELECT INTO #temp` | ❌ No - Use `CREATE TEMP TABLE AS SELECT` |
| `BULK INSERT ...` | ❌ No - Use `COPY INTO` |

### Common Patterns to Uncomment

| Commented (No-Op) | Uncommented (Valid) |
|-------------------|---------------------|
| `'--CREATE SCHEMA x'` | `'CREATE SCHEMA IF NOT EXISTS x'` |
| `'--CREATE TABLE x (...)'` | `'CREATE TABLE IF NOT EXISTS x (...)'` after type conversion |
| `'--DROP TABLE x'` | `'DROP TABLE IF EXISTS x'` |
| `'--TRUNCATE TABLE x'` | `'TRUNCATE TABLE IF EXISTS x'` |

**Note:** Add `IF NOT EXISTS` / `IF EXISTS` for idempotent execution where appropriate.

## Fix Process

1. **Locate the SQL string to fix:**
   - **Variable assignment ABOVE the EWI** - Search upward from the `!!!RESOLVE EWI!!!` marker to find where the variable (e.g., `SQL_VAR := '...'`) is defined or concatenated
   - **Literal string IN the statement with the EWI** - Check if the statement itself contains a literal SQL string argument that needs conversion
2. **Check for commented-out SQL** - If the string starts with `--`, evaluate if it should be uncommented (see above)
3. **Transform** SQL Server syntax inside the string using Quick Reference (identifiers, concatenation, variables, temp tables, patterns)
4. **Rewrite** system catalog queries (`sys.*`) to `INFORMATION_SCHEMA`
5. **Validate** variable syntax: `:var_name` for references, `var := value` for assignment
6. **Remove** the `!!!RESOLVE EWI!!!` marker

## Key Points

- The EWI marker and the SQL string to fix are on **different lines** - the string is ABOVE the marker
- Edit the **variable assignment lines**, not the marker line
- **Check for `--` comments** inside dynamic SQL strings - uncomment if the SQL is valid Snowflake
- **Validate grammar** before uncommenting - not all SQL Server statements have Snowflake equivalents
- Apply ALL transformations from Quick Reference INSIDE the string literal
- Remove the `!!!RESOLVE EWI!!!` marker only AFTER applying the fixes above

## Unmapped Elements

For SQL Server elements not in the tables above:
1. Check SQL Server documentation to understand original behavior
2. Find equivalent in Snowflake documentation
3. Test the conversion

## Resources

**SQL Server:**
- [Functions](https://learn.microsoft.com/en-us/sql/t-sql/functions/functions?view=sql-server-ver17)
- [Data Types](https://learn.microsoft.com/en-us/sql/t-sql/data-types/data-types-transact-sql?view=sql-server-ver17)
- [COLLATE](https://learn.microsoft.com/en-us/sql/t-sql/statements/collations?view=sql-server-ver17)
- [System Catalog Views](https://learn.microsoft.com/en-us/sql/relational-databases/system-catalog-views/catalog-views-transact-sql?view=sql-server-ver17)

**Snowflake:**
- [EXECUTE IMMEDIATE](https://docs.snowflake.com/en/sql-reference/sql/execute-immediate)
- [INFORMATION_SCHEMA](https://docs.snowflake.com/en/sql-reference/info-schema)
- [Reserved Keywords](https://docs.snowflake.com/en/sql-reference/reserved-keywords)
- [Functions](https://docs.snowflake.com/en/sql-reference/functions)
- [Data Types](https://docs.snowflake.com/en/sql-reference/data-types)
- [Regular Expressions](https://docs.snowflake.com/en/sql-reference/functions-regexp)
- [COLLATE](https://docs.snowflake.com/en/sql-reference/functions/collate)
