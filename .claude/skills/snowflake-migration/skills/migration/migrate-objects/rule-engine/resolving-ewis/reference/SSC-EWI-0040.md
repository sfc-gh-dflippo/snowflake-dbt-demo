# SSC-EWI-0040 - Simple SET Statement Not Supported

Snowflake does not support many SQL Server SET statements that control session behavior. These statements must be removed or replaced with Snowflake-equivalent patterns.

## Quick Reference

| SQL Server SET Statement | Snowflake Equivalent |
|-------------------------|---------------------|
| `SET NOCOUNT ON/OFF` | Not needed - remove |
| `SET XACT_ABORT ON/OFF` | Use explicit transaction control + EXCEPTION handling |
| `SET ANSI_NULLS ON/OFF` | Not needed - Snowflake always uses ANSI NULL behavior |
| `SET QUOTED_IDENTIFIER ON/OFF` | Not needed - use double quotes for identifiers |
| `SET ANSI_WARNINGS ON/OFF` | Not needed - remove |
| `SET ANSI_PADDING ON/OFF` | Not needed - remove |
| `SET CONCAT_NULL_YIELDS_NULL ON/OFF` | Not needed - use `NVL()` or `CONCAT_WS()` if needed |
| `SET ARITHABORT ON/OFF` | Not needed - remove |
| `SET NUMERIC_ROUNDABORT ON/OFF` | Not needed - remove |

## Identification

Look for the marker:
```
!!!RESOLVE EWI!!! /*** SSC-EWI-0040 - THE 'SIMPLE SET STATEMENT' CLAUSE IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
```

## Fix Process

1. **Identify the SET statement** following the EWI marker
2. **Determine if replacement is needed** using the Quick Reference above
3. **Remove the statement** if no replacement is needed
4. **Add equivalent logic** if behavior must be preserved (e.g., transaction control)
5. **Remove** the `!!!RESOLVE EWI!!!` marker

## Common Cases

### SET NOCOUNT ON/OFF

**SQL Server:** Prevents the "rows affected" message from being returned.

**Snowflake:** No equivalent needed. Simply remove the statement.

```sql
-- Remove this entirely
-- SET NOCOUNT ON;
```

### SET XACT_ABORT ON

**SQL Server:** Automatically rolls back the transaction when a run-time error occurs.

**Snowflake:** Use explicit transaction control with EXCEPTION handling.

#### Before (Invalid)
```sql
BEGIN
    SET XACT_ABORT ON;
    -- ... procedure logic ...
END;
```

#### After (Functional Equivalent)
```sql
BEGIN
    -- Start explicit transaction
    BEGIN TRANSACTION;
    
    -- ... procedure logic ...
    
    -- Commit on success
    COMMIT;
    
EXCEPTION
    WHEN OTHER THEN
        -- Rollback on error (equivalent to XACT_ABORT behavior)
        ROLLBACK;
        -- Re-raise or handle the error
        RAISE;
END;
```

#### Simplified (When Rollback Not Critical)
```sql
BEGIN
    -- Note: SET XACT_ABORT ON is not applicable in Snowflake.
    -- Use explicit transaction control if rollback-on-error is required.
    
    -- ... procedure logic ...
    
EXCEPTION
    WHEN OTHER THEN
        -- Handle error
        LET err_msg := SQLERRM;
        -- ... error handling ...
END;
```

### SET ANSI_NULLS ON

**SQL Server:** Controls NULL comparison behavior.

**Snowflake:** Always uses ANSI NULL behavior (NULL = NULL returns NULL, not TRUE/FALSE).

```sql
-- Remove this entirely - Snowflake is always ANSI compliant
-- SET ANSI_NULLS ON;
```

### SET QUOTED_IDENTIFIER ON

**SQL Server:** Allows double quotes for identifiers.

**Snowflake:** Always supports double-quoted identifiers.

```sql
-- Remove this entirely
-- SET QUOTED_IDENTIFIER ON;
```

## Transaction Control in Snowflake

If you need `SET XACT_ABORT ON` behavior, use explicit transaction control:

| SQL Server | Snowflake |
|------------|-----------|
| `SET XACT_ABORT ON` | `BEGIN TRANSACTION` at start |
| (implicit rollback on error) | `ROLLBACK` in EXCEPTION block |
| (implicit commit on success) | `COMMIT` before END |

### Example: Full Transaction Control

```sql
CREATE OR REPLACE PROCEDURE my_procedure()
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
DECLARE
    result VARCHAR;
BEGIN
    BEGIN TRANSACTION;
    
    -- Main logic here
    INSERT INTO target_table SELECT * FROM source_table;
    UPDATE another_table SET status = 'PROCESSED';
    
    COMMIT;
    result := 'SUCCESS';
    RETURN result;
    
EXCEPTION
    WHEN OTHER THEN
        ROLLBACK;
        result := 'ERROR: ' || SQLERRM;
        RETURN result;
END;
$$;
```

## Key Points

- Most SQL Server SET statements can simply be **removed**
- Snowflake is **ANSI-compliant by default** for NULL handling and identifier quoting
- For `SET XACT_ABORT ON`, add **explicit transaction control** if rollback behavior is required
- The `EXCEPTION WHEN OTHER THEN` block is Snowflake's error handling mechanism
- Use `SQLERRM` to capture error messages (equivalent to `ERROR_MESSAGE()`)

## Resources

**Snowflake:**
- [Transaction Control](https://docs.snowflake.com/en/sql-reference/transactions)
- [BEGIN TRANSACTION](https://docs.snowflake.com/en/sql-reference/sql/begin)
- [Exception Handling](https://docs.snowflake.com/en/developer-guide/snowflake-scripting/exceptions)
- [SQLERRM](https://docs.snowflake.com/en/developer-guide/snowflake-scripting/exceptions#sqlerrm)

**SQL Server:**
- [SET XACT_ABORT](https://learn.microsoft.com/en-us/sql/t-sql/statements/set-xact-abort-transact-sql)
- [SET NOCOUNT](https://learn.microsoft.com/en-us/sql/t-sql/statements/set-nocount-transact-sql)
- [SET ANSI_NULLS](https://learn.microsoft.com/en-us/sql/t-sql/statements/set-ansi-nulls-transact-sql)
