# SSC-EWI-0056 - User-Defined Types Not Supported

Snowflake does not support SQL Server User-Defined Types (UDTs) or Table-Valued Parameters (TVPs). SnowConvert changes the type to `VARIANT`, but additional code changes are required for functional equivalence.

## Quick Reference

| SQL Server | Snowflake Equivalent |
|------------|---------------------|
| `@param TableType READONLY` | `PARAM VARIANT` containing ARRAY of objects |
| `SELECT ... FROM @param` | `SELECT ... FROM LATERAL FLATTEN(INPUT => :PARAM) f` |
| `col` from TVP | `f.VALUE:col::datatype` |

## Identification

Look for the marker:
```
!!!RESOLVE EWI!!! /*** SSC-EWI-0056 - USER-DEFINED TYPES ARE NOT SUPPORTED IN SNOWFLAKE. REFERENCES WERE CHANGED TO VARIANT. ***/!!!
```

## The Problem

SnowConvert changes TVP parameters to `VARIANT`, but the code that reads from the TVP still tries to `SELECT FROM` it as if it were a table:

```sql
-- This doesn't work in Snowflake
INSERT INTO staging_table (col1, col2)
SELECT col1, col2
FROM T_ParameterName;  -- References non-existent table
```

## Fix Process

1. **Identify the TVP parameter** and note its expected columns from the original SQL Server code
2. **Update the parameter declaration** to document the expected JSON structure
3. **Find all usages** of the TVP (SELECT FROM, INSERT...SELECT, etc.)
4. **Replace table references** with `LATERAL FLATTEN` pattern
5. **Cast each column** to the appropriate Snowflake data type
6. **Remove** the `!!!RESOLVE EWI!!!` marker

## Data Type Mappings

| SQL Server Type | Snowflake Cast |
|-----------------|----------------|
| `INT` | `::INT` |
| `BIGINT` | `::BIGINT` |
| `SMALLINT` | `::SMALLINT` |
| `DECIMAL(p,s)` | `::DECIMAL(p,s)` |
| `VARCHAR(n)` | `::VARCHAR(n)` |
| `NVARCHAR(n)` | `::VARCHAR(n)` |
| `BIT` | `::BOOLEAN` |
| `DATETIME`, `DATETIME2` | `::TIMESTAMP_NTZ` |
| `DATE` | `::DATE` |
| `UNIQUEIDENTIFIER` | `::VARCHAR(36)` |

## Example

### Before (Invalid - References Non-Existent Table)
```sql
CREATE OR REPLACE PROCEDURE my_procedure (
    DATA VARIANT  -- Was: @Data MyTableType READONLY
)
...
BEGIN
    INSERT INTO staging (col1, col2, col3)
    SELECT col1, col2, col3
    FROM T_Data;  -- ERROR: T_Data doesn't exist
END;
```

### After (Functional Equivalent)
```sql
CREATE OR REPLACE PROCEDURE my_procedure (
    DATA VARIANT  -- Pass ARRAY of objects: [{"col1":1,"col2":"a","col3":100.00},...]
)
...
BEGIN
    INSERT INTO staging (col1, col2, col3)
    SELECT
        f.VALUE:col1::INT,
        f.VALUE:col2::VARCHAR(50),
        f.VALUE:col3::DECIMAL(19,4)
    FROM LATERAL FLATTEN(INPUT => :DATA) f;
END;
```

## Caller Migration

Callers must change how they pass data to the procedure.

### SQL Server (Original)
```sql
DECLARE @data MyTableType;
INSERT INTO @data (col1, col2, col3) VALUES (1, 'a', 100.00);
INSERT INTO @data (col1, col2, col3) VALUES (2, 'b', 200.00);

EXEC my_procedure @Data = @data;
```

### Snowflake (Equivalent)
```sql
CALL my_procedure(
    PARSE_JSON('[
        {"col1": 1, "col2": "a", "col3": 100.00},
        {"col2": 2, "col2": "b", "col3": 200.00}
    ]')
);
```

### Building VARIANT from a Table
```sql
-- If data is already in a table, build the ARRAY first
SET data_array = (SELECT ARRAY_AGG(OBJECT_CONSTRUCT(
    'col1', col1,
    'col2', col2,
    'col3', col3
)) FROM source_table);

CALL my_procedure($data_array);
```

## LATERAL FLATTEN Syntax

```sql
SELECT
    f.VALUE:column_name::DATATYPE AS alias
FROM LATERAL FLATTEN(INPUT => :VARIANT_PARAM) f
WHERE f.VALUE:filter_column::INT > 0;
```

| Component | Description |
|-----------|-------------|
| `LATERAL FLATTEN(INPUT => :PARAM)` | Expands ARRAY into rows |
| `f` | Alias for the flattened result |
| `f.VALUE` | The current array element (an OBJECT) |
| `f.VALUE:column_name` | Access a property from the object |
| `::DATATYPE` | Cast to the appropriate type |

## Handling NULL Values

JSON nulls are preserved. Use `NVL` or `COALESCE` if defaults are needed:

```sql
SELECT
    NVL(f.VALUE:optional_col::INT, 0) AS optional_col
FROM LATERAL FLATTEN(INPUT => :DATA) f;
```

## Key Points

- The VARIANT must contain an **ARRAY of OBJECTS** (not a single object)
- Column names in JSON are **case-sensitive** - match the original column names
- Always **cast** extracted values to the correct type
- Use `LATERAL FLATTEN` for every TVP reference in the code
- Update caller code to pass data as JSON ARRAY

## Resources

**Snowflake:**
- [VARIANT Data Type](https://docs.snowflake.com/en/sql-reference/data-types-semistructured)
- [FLATTEN Function](https://docs.snowflake.com/en/sql-reference/functions/flatten)
- [LATERAL Join](https://docs.snowflake.com/en/sql-reference/constructs/join-lateral)
- [PARSE_JSON Function](https://docs.snowflake.com/en/sql-reference/functions/parse_json)
- [OBJECT_CONSTRUCT Function](https://docs.snowflake.com/en/sql-reference/functions/object_construct)
- [ARRAY_AGG Function](https://docs.snowflake.com/en/sql-reference/functions/array_agg)

**SQL Server:**
- [Table-Valued Parameters](https://learn.microsoft.com/en-us/sql/relational-databases/tables/use-table-valued-parameters-database-engine)
- [User-Defined Types](https://learn.microsoft.com/en-us/sql/relational-databases/clr-integration-database-objects-user-defined-types/clr-user-defined-types)
