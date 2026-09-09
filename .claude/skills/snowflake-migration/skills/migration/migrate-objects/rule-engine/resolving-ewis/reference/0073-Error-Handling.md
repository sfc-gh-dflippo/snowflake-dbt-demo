# SSC-EWI-0073: Error Handling Functions

SnowConvert marks SQL Server TRY...CATCH error-handling functions
with this EWI because they have no direct 1:1 equivalent in
Snowflake. Convert to `BEGIN...EXCEPTION...END` with `SQLCODE`,
`SQLERRM`, and `SQLSTATE`.

## Quick Reference

| SQL Server | Snowflake | Notes |
|------------|-----------|-------|
| `BEGIN TRY...END TRY BEGIN CATCH...END CATCH` | `BEGIN...EXCEPTION WHEN OTHER THEN...END` | Structural replacement |
| `ERROR_NUMBER()` | `SQLCODE` | Numeric error code (signed integer) |
| `ERROR_MESSAGE()` | `SQLERRM` | Error message text |
| `ERROR_STATE()` | `SQLSTATE` | 5-char ANSI SQL state code |
| `ERROR_SEVERITY()` | No equivalent | Drop or hardcode a default |
| `ERROR_LINE()` | No equivalent | `SQLERRM` may include context |
| `ERROR_PROCEDURE()` | No equivalent | Hardcode procedure name |
| `@@ERROR` | `SQLCODE` | Legacy SQL Server error check |
| `RAISERROR` / `THROW` | `RAISE` | Raise exceptions |
| `CONVERT(VARCHAR, expr)` | `expr::VARCHAR` | Type casting syntax |

## Identification

```
!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'ERROR_NUMBER' NODE ***/
!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'ERROR_SEVERITY' NODE ***/
!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'ERROR_STATE' NODE ***/
!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'ERROR_LINE' NODE ***/
!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'ERROR_MESSAGE' NODE ***/
!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'ERROR_PROCEDURE' NODE ***/
```

## Decision Tree

```
Is the error data logged or returned?
├── YES → What functions are used?
│   ├── ERROR_NUMBER() only → Replace with SQLCODE (Case 1)
│   ├── ERROR_MESSAGE() only → Replace with SQLERRM (Case 2)
│   ├── Multiple functions (common) → Combine SQLCODE + SQLERRM + SQLSTATE (Case 3)
│   └── ERROR_LINE() / ERROR_PROCEDURE() → Drop or hardcode (Case 4)
├── NO (empty CATCH / CATCH only re-throws) → Simplify to RAISE or remove (Case 5)
└── Structured error object needed → OBJECT_CONSTRUCT pattern (Case 6)
```

## Fix Process

1. **Identify the TRY...CATCH block**
2. **Catalog error functions used** in the CATCH block
3. **Check error logging** — logged to table, returned, or both
4. **Replace structure** — `BEGIN...EXCEPTION WHEN OTHER THEN...END`
5. **Map functions** — see Quick Reference
6. **Fix type casting** — `CONVERT(VARCHAR, expr)` → `expr::VARCHAR`
7. **Remove markers** — delete all `!!!RESOLVE EWI!!!` lines
8. **Verify** — ensure error log table schema matches new types

---

## Case 1: Simple Error Number Logging

### Before (SQL Server)
```sql
BEGIN TRY
    INSERT INTO target_table SELECT * FROM source_table;
END TRY
BEGIN CATCH
    INSERT INTO ErrorLog (ErrorCode)
    SELECT CONVERT(VARCHAR, ERROR_NUMBER());
END CATCH
```

### After (Snowflake)
```sql
BEGIN
    INSERT INTO target_table SELECT * FROM source_table;
EXCEPTION
    WHEN OTHER THEN
        INSERT INTO ErrorLog (ErrorCode)
            VALUES (SQLCODE::VARCHAR);
END;
```

---

## Case 2: Error Message Only

### Before (SQL Server)
```sql
BEGIN TRY
    DELETE FROM staging_table;
END TRY
BEGIN CATCH
    PRINT ERROR_MESSAGE();
END CATCH
```

### After (Snowflake)
```sql
BEGIN
    DELETE FROM staging_table;
EXCEPTION
    WHEN OTHER THEN
        RETURN SQLERRM;
END;
```

---

## Case 3: Multiple Error Functions (Most Common)

### Before (SQL Server)
```sql
CREATE PROCEDURE dbo.usp_Load_Data
AS
BEGIN
    BEGIN TRY
        TRUNCATE TABLE target_table;
        INSERT INTO target_table SELECT * FROM source_view;
    END TRY
    BEGIN CATCH
        INSERT INTO LogZTrackErrors (ErrorCode, ErrorDescription)
        SELECT CONVERT(VARCHAR, ERROR_NUMBER()),
               'ErrLine - ' + CONVERT(VARCHAR, ERROR_LINE())
               + ' : ' + ERROR_MESSAGE()
               + ' Proc Name : ' + ERROR_PROCEDURE();
    END CATCH
END
```

### After (Snowflake)
```sql
CREATE OR REPLACE PROCEDURE usp_Load_Data()
    RETURNS VARCHAR
    LANGUAGE SQL
AS
DECLARE
    v_proc_name VARCHAR DEFAULT 'usp_Load_Data';
BEGIN
    TRUNCATE TABLE target_table;
    INSERT INTO target_table SELECT * FROM source_view;
    RETURN 'Success';
EXCEPTION
    WHEN OTHER THEN
        INSERT INTO LogZTrackErrors (ErrorCode, ErrorDescription)
            VALUES (
                SQLCODE::VARCHAR,
                'SQLSTATE - ' || SQLSTATE || ' : '
                || SQLERRM || ' Proc Name : ' || v_proc_name
            );
        RETURN 'Error: ' || SQLCODE || ' - ' || SQLERRM;
END;
```

**Key changes:**
- `ERROR_NUMBER()` → `SQLCODE`
- `ERROR_MESSAGE()` → `SQLERRM`
- `ERROR_LINE()` → dropped; `SQLSTATE` added as context
- `ERROR_PROCEDURE()` → hardcoded `v_proc_name`
- `CONVERT(VARCHAR, x)` → `x::VARCHAR`
- `+` (concat) → `||`

---

## Case 4: ERROR_LINE / ERROR_PROCEDURE Workarounds

| Function | Strategy | Example |
|----------|----------|---------|
| `ERROR_LINE()` | Drop — `SQLERRM` includes context | Remove from concat |
| `ERROR_PROCEDURE()` | Hardcode procedure name | `LET v_proc := 'my_proc';` |
| `ERROR_PROCEDURE()` | `CURRENT_STATEMENT()` | Partial context only |

### Before
```sql
SELECT ERROR_PROCEDURE() + ':' + CONVERT(VARCHAR, ERROR_LINE())
       + ' - ' + ERROR_MESSAGE();
```

### After
```sql
LET v_error_detail := v_proc_name || ' - ' || SQLERRM;
```

---

## Case 5: Empty or Re-throw CATCH

### Before (SQL Server)
```sql
BEGIN TRY
    EXEC usp_inner_proc;
END TRY
BEGIN CATCH
    THROW;
END CATCH
```

### After (Snowflake)
```sql
BEGIN
    CALL usp_inner_proc();
EXCEPTION
    WHEN OTHER THEN
        RAISE;
END;
```

Or remove the handler entirely if default propagation is acceptable:

```sql
BEGIN
    CALL usp_inner_proc();
END;
```

---

## Case 6: Structured Error Object (Advanced)

```sql
EXCEPTION
    WHEN OTHER THEN
        RETURN OBJECT_CONSTRUCT(
            'ErrorCode', SQLCODE,
            'ErrorMessage', SQLERRM,
            'SQLState', SQLSTATE,
            'ProcName', v_proc_name,
            'Timestamp', CURRENT_TIMESTAMP()
        );
```

---

## Error Log Table Migration

### SQL Server
```sql
CREATE TABLE LogZTrackErrors (
    ErrorCode     VARCHAR(50),
    ErrorDescription VARCHAR(4000)
);
```

### Snowflake (enhanced)
```sql
CREATE TABLE IF NOT EXISTS LogZTrackErrors (
    ErrorCode        VARCHAR(50),
    ErrorDescription VARCHAR(4000),
    SQLState         VARCHAR(5),
    ProcName         VARCHAR(200),
    ErrorTimestamp   TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);
```

---

## Key Points

- `SQLCODE`, `SQLERRM`, `SQLSTATE` only available inside EXCEPTION handler
- Variables in EXCEPTION block must be declared in `DECLARE`
- Use `:SQLCODE` / `:SQLERRM` / `:SQLSTATE` as bind variables in SQL
- Use without colon in expressions (`RETURN SQLERRM;`)
- `SQLCODE` is signed integer — cast `::VARCHAR` for VARCHAR columns
- `SQLSTATE` is 5-char ANSI code, differs from SQL Server numeric state
- No `ERROR_SEVERITY()` equivalent — redesign or remove
- `WHEN OTHER THEN` catches all exceptions (generic CATCH)
- Snowflake supports: `STATEMENT_ERROR`, `EXPRESSION_ERROR`, user-defined

## Resources

- [Snowflake Exception Handling](https://docs.snowflake.com/en/developer-guide/snowflake-scripting/exceptions)
- [EXCEPTION Syntax](https://docs.snowflake.com/en/sql-reference/snowflake-scripting/exception)
- [RAISE Statement](https://docs.snowflake.com/en/sql-reference/snowflake-scripting/raise)
- [SQL Server ERROR_NUMBER()](https://learn.microsoft.com/en-us/sql/t-sql/functions/error-number-transact-sql)
- [SQL Server TRY...CATCH](https://learn.microsoft.com/en-us/sql/t-sql/language-elements/try-catch-transact-sql)
- [SnowConvert SSC-EWI-0073](https://docs.snowconvert.com/sc/general/technical-documentation/issues-and-troubleshooting/conversion-issues/general/ssc-ewi-0073)
