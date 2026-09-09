# SSC-EWI-0058 - Functionality Not Supported in Snowflake Scripting

Snowflake Scripting does not support certain SQL Server features. This EWI covers various unsupported functionalities that must be removed or replaced.

## Quick Reference

| SQL Server Feature | Snowflake Resolution |
|-------------------|---------------------|
| `@param TableType READONLY` | Remove READONLY - Snowflake VARIANT is immutable by nature |
| `DEALLOCATE cursor_name` | Remove - Snowflake cursors auto-deallocate |
| `DECLARE ... FOR UPDATE` | Remove FOR UPDATE - use alternative locking patterns |
| `FETCH ... INTO @var` with positioning | Use standard FETCH INTO |
| `GLOBAL` cursors | Not supported - use session-scoped cursors |

## Identification

Look for the marker:
```
!!!RESOLVE EWI!!! /*** SSC-EWI-0058 - FUNCTIONALITY FOR '<feature>' IS NOT CURRENTLY SUPPORTED BY SNOWFLAKE SCRIPTING ***/!!!
```

## Fix Process

1. **Identify the unsupported feature** from the EWI message
2. **Apply the appropriate resolution** from the sections below
3. **Test the logic** to ensure functional equivalence
4. **Remove** the `!!!RESOLVE EWI!!!` marker

---

## READONLY Parameters

SQL Server Table-Valued Parameters (TVPs) use the `READONLY` keyword to prevent modification. In Snowflake, parameters are immutable by default.

### Before (Invalid)
```sql
CREATE PROCEDURE my_proc (
    DATA VARIANT READONLY  -- READONLY not valid in Snowflake
)
```

### After (Valid)
```sql
CREATE PROCEDURE my_proc (
    DATA VARIANT  -- Parameters are immutable by default in Snowflake
)
```

**Resolution:** Simply remove the `READONLY` keyword. Snowflake procedure parameters cannot be modified within the procedure anyway.

---

## DEALLOCATE Cursor

SQL Server requires explicit cursor deallocation. Snowflake cursors are automatically deallocated when they go out of scope.

### Before (Invalid)
```sql
DECLARE my_cursor CURSOR FOR SELECT id FROM my_table;
OPEN my_cursor;
-- ... fetch loop ...
CLOSE my_cursor;
DEALLOCATE my_cursor;  -- Not supported
```

### After (Valid)
```sql
DECLARE my_cursor CURSOR FOR SELECT id FROM my_table;
OPEN my_cursor;
-- ... fetch loop ...
CLOSE my_cursor;
-- DEALLOCATE removed - cursor auto-deallocates when scope ends
```

**Resolution:** Remove the `DEALLOCATE` statement entirely.

---

## FOR UPDATE Cursors

SQL Server cursors with `FOR UPDATE` lock rows for modification. Snowflake does not support row-level locking through cursors.

### Before (Invalid)
```sql
DECLARE update_cursor CURSOR FOR 
    SELECT id, status FROM orders WHERE status = 'PENDING'
    FOR UPDATE;  -- Not supported

OPEN update_cursor;
FETCH update_cursor INTO :v_id, :v_status;
WHILE (SQLCODE = 0) DO
    UPDATE orders SET status = 'PROCESSING' WHERE CURRENT OF update_cursor;
    FETCH update_cursor INTO :v_id, :v_status;
END WHILE;
CLOSE update_cursor;
```

### After (Valid) - Option 1: Direct UPDATE
```sql
-- If simple update, avoid cursor entirely
UPDATE orders SET status = 'PROCESSING' WHERE status = 'PENDING';
```

### After (Valid) - Option 2: Cursor without FOR UPDATE
```sql
DECLARE update_cursor CURSOR FOR 
    SELECT id, status FROM orders WHERE status = 'PENDING';

OPEN update_cursor;
FETCH update_cursor INTO :v_id, :v_status;
WHILE (SQLCODE = 0) DO
    -- Update using primary key instead of WHERE CURRENT OF
    UPDATE orders SET status = 'PROCESSING' WHERE id = :v_id;
    FETCH update_cursor INTO :v_id, :v_status;
END WHILE;
CLOSE update_cursor;
```

### After (Valid) - Option 3: Batch processing with temp table
```sql
-- Capture rows to process
CREATE TEMPORARY TABLE rows_to_process AS
SELECT id FROM orders WHERE status = 'PENDING';

-- Process in batch
UPDATE orders o
SET status = 'PROCESSING'
WHERE EXISTS (SELECT 1 FROM rows_to_process r WHERE r.id = o.id);

DROP TABLE rows_to_process;
```

**Resolution:** 
- Remove `FOR UPDATE` clause from cursor declaration
- Replace `WHERE CURRENT OF cursor` with `WHERE primary_key = :captured_key`
- Consider replacing cursor with set-based operations

---

## GLOBAL Cursors

SQL Server `GLOBAL` cursors are accessible across batches. Snowflake only supports session-scoped cursors.

### Before (Invalid)
```sql
DECLARE GLOBAL my_cursor CURSOR FOR SELECT * FROM my_table;
```

### After (Valid)
```sql
-- Remove GLOBAL keyword - Snowflake cursors are session-scoped
DECLARE my_cursor CURSOR FOR SELECT * FROM my_table;
```

**Resolution:** Remove the `GLOBAL` keyword.

---

## Cursor Fetch Options

SQL Server supports various FETCH options not available in Snowflake.

| SQL Server FETCH | Snowflake Support |
|------------------|-------------------|
| `FETCH NEXT` | ✅ Supported |
| `FETCH PRIOR` | ❌ Not supported |
| `FETCH FIRST` | ❌ Not supported |
| `FETCH LAST` | ❌ Not supported |
| `FETCH ABSOLUTE n` | ❌ Not supported |
| `FETCH RELATIVE n` | ❌ Not supported |

### Workaround for Positional Fetch

If you need positional access, load data into a temp table with row numbers:

```sql
CREATE TEMPORARY TABLE numbered_rows AS
SELECT ROW_NUMBER() OVER (ORDER BY sort_column) AS row_num, *
FROM source_table;

-- Then query by position
SELECT * FROM numbered_rows WHERE row_num = :target_position;
```

---

## Snowflake Cursor Best Practices

### Cursor Declaration and Usage
```sql
DECLARE
    v_id INT;
    v_name VARCHAR;
    my_cursor CURSOR FOR SELECT id, name FROM my_table WHERE status = 'ACTIVE';
BEGIN
    OPEN my_cursor;
    LOOP
        FETCH my_cursor INTO v_id, v_name;
        IF (SQLNOTFOUND) THEN
            LEAVE;
        END IF;
        -- Process row
        INSERT INTO results VALUES (:v_id, :v_name);
    END LOOP;
    CLOSE my_cursor;
END;
```

### Using FOR Loop (Simpler)
```sql
DECLARE
    rec RECORD;
BEGIN
    FOR rec IN (SELECT id, name FROM my_table WHERE status = 'ACTIVE') DO
        -- Process row - rec.id, rec.name are available
        INSERT INTO results VALUES (rec.id, rec.name);
    END FOR;
END;
```

---

## Key Points

- **READONLY**: Remove keyword - Snowflake parameters are immutable
- **DEALLOCATE**: Remove statement - cursors auto-deallocate
- **FOR UPDATE**: Remove clause, use key-based updates instead
- **GLOBAL**: Remove keyword - use session-scoped cursors
- **Positional FETCH**: Use temp tables with row numbers
- **Prefer set-based operations** over cursors when possible
- **Use FOR loops** for simpler cursor patterns

## Resources

**Snowflake:**
- [Cursors in Snowflake Scripting](https://docs.snowflake.com/en/developer-guide/snowflake-scripting/cursors)
- [DECLARE Cursor](https://docs.snowflake.com/en/sql-reference/snowflake-scripting/declare#cursor-declaration)
- [FETCH Statement](https://docs.snowflake.com/en/sql-reference/snowflake-scripting/fetch)
- [FOR Loop with Cursor](https://docs.snowflake.com/en/developer-guide/snowflake-scripting/loops#for-loop-cursor)

**SQL Server:**
- [DECLARE CURSOR](https://learn.microsoft.com/en-us/sql/t-sql/language-elements/declare-cursor-transact-sql)
- [DEALLOCATE](https://learn.microsoft.com/en-us/sql/t-sql/language-elements/deallocate-transact-sql)
- [FETCH](https://learn.microsoft.com/en-us/sql/t-sql/language-elements/fetch-transact-sql)
