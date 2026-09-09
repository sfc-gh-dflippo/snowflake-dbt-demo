# SSC-EWI-TS0087 - GOTO Is Not Supported in Snowflake

Snowflake Scripting does not support the GOTO statement for control flow. SQL Server code using GOTO and labels must be refactored using the **SnowConvert Label-to-Procedure Pattern**.

## Quick Reference

| SQL Server Pattern | Snowflake Transformation |
|-------------------|-------------------------|
| `LabelName:` | `LabelName PROCEDURE() RETURNS VARCHAR AS BEGIN ... END;` |
| `GOTO LabelName` | `CALL LabelName(); RETURN 'PROCESS FINISHED';` |
| Fall-through to next label | `CALL NextLabel();` at end of procedure |
| Error code checking | `STATUS_OBJECT['SQLCODE']` |
| Main entry point | `SC_PROCESS PROCEDURE()` |

## Identification

Look for the markers:
```
!!!RESOLVE EWI!!! /*** SSC-EWI-TS0087 - GOTO IS NOT SUPPORTED IN SNOWFLAKE. ***/!!!
GOTO LabelName;
```

And the related label marker:
```
!!!RESOLVE EWI!!! /*** SSC-EWI-TS0045 - LABELED STATEMENT IS NOT SUPPORTED IN SNOWFLAKE SCRIPTING ***/!!!
LabelName:
```

---

## SnowConvert Transformation Pattern

SnowConvert uses a consistent pattern to transform labels and GOTOs into Snowflake Scripting nested procedures. This pattern preserves the original control flow semantics.

### Core Components

| Component | Purpose |
|-----------|---------|
| `SC_EXIT_CODE` | Exit code variable for the script |
| `STATUS_OBJECT` | Object tracking `SQLCODE`, `SQLERRM`, `SQLSTATE` |
| `SC_PROCESS` | Main entry procedure (contains code before first label) |
| `LabelName PROCEDURE()` | Each label becomes a nested procedure |
| `EXCEPTION WHEN OTHER CONTINUE THEN` | Capture errors without stopping execution |

### Transformation Rules

1. **Each label becomes a nested procedure** with the same name
2. **GOTO becomes**: `CALL LabelName(); RETURN 'PROCESS FINISHED';`
3. **Fall-through behavior**: At the end of each label's code, call the next label procedure
4. **Error handling**: Use `EXCEPTION WHEN OTHER CONTINUE THEN` to capture errors
5. **Status tracking**: Store error info in `STATUS_OBJECT` for conditional checks

### Basic Pattern Structure

```sql
DECLARE
    SC_EXIT_CODE VARCHAR := 0;
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0);
    
    SC_PROCESS PROCEDURE ()
    RETURNS VARCHAR
    AS
    BEGIN
        -- Code before first label goes here
        -- ...
        
        -- Conditional GOTO becomes:
        IF (condition) THEN
            CALL LabelName();
            RETURN 'PROCESS FINISHED';
        END IF;
        
        -- Fall-through to first label:
        CALL FirstLabel();
    EXCEPTION
        WHEN OTHER CONTINUE THEN
            STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
    END;
    
    FirstLabel PROCEDURE ()
    RETURNS VARCHAR
    AS
    BEGIN
        -- Code under FirstLabel goes here
        -- ...
        
        -- Fall-through to next label:
        CALL SecondLabel();
    EXCEPTION
        WHEN OTHER CONTINUE THEN
            STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
    END;
    
    SecondLabel PROCEDURE ()
    RETURNS VARCHAR
    AS
    BEGIN
        -- Code under SecondLabel goes here
        -- (Last label - no fall-through call)
    EXCEPTION
        WHEN OTHER CONTINUE THEN
            STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
    END;

BEGIN
    CALL SC_PROCESS();
    RETURN SC_EXIT_CODE;
END
```

---

## Complete Transformation Example

### Before (SQL Server with GOTO)

```sql
CREATE PROCEDURE ProcessData
AS
BEGIN
    -- Initial processing
    DROP TABLE IF EXISTS TempTable1;
    IF @@ERROR <> 0 GOTO ErrorHandler1;
    
    -- More processing
    DROP TABLE IF EXISTS TempTable2;
    IF @@ERROR <> 0 GOTO ErrorHandler2;
    
    -- Final step
    DROP TABLE IF EXISTS TempTable3;
    GOTO Cleanup;

ErrorHandler1:
    PRINT 'Error in step 1';
    GOTO Cleanup;

ErrorHandler2:
    PRINT 'Error in step 2';
    GOTO Cleanup;

Cleanup:
    PRINT 'Cleanup complete';
END
```

### After (Snowflake - SnowConvert Pattern)

```sql
CREATE OR REPLACE PROCEDURE ProcessData()
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
DECLARE
    SC_EXIT_CODE VARCHAR := '0';
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0);
    
    SC_PROCESS PROCEDURE ()
    RETURNS VARCHAR
    AS
    BEGIN
        -- Initial processing
        DROP TABLE IF EXISTS TempTable1;
        IF (STATUS_OBJECT['SQLCODE'] != 0) THEN
            CALL ErrorHandler1();
            RETURN 'PROCESS FINISHED';
        END IF;
        
        -- More processing
        DROP TABLE IF EXISTS TempTable2;
        IF (STATUS_OBJECT['SQLCODE'] != 0) THEN
            CALL ErrorHandler2();
            RETURN 'PROCESS FINISHED';
        END IF;
        
        -- Final step
        DROP TABLE IF EXISTS TempTable3;
        CALL Cleanup();
        RETURN 'PROCESS FINISHED';
    EXCEPTION
        WHEN OTHER CONTINUE THEN
            STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
    END;
    
    ErrorHandler1 PROCEDURE ()
    RETURNS VARCHAR
    AS
    BEGIN
        -- PRINT 'Error in step 1' equivalent
        SYSTEM$LOG_INFO('Error in step 1');
        CALL Cleanup();
        RETURN 'PROCESS FINISHED';
    EXCEPTION
        WHEN OTHER CONTINUE THEN
            STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
    END;
    
    ErrorHandler2 PROCEDURE ()
    RETURNS VARCHAR
    AS
    BEGIN
        -- PRINT 'Error in step 2' equivalent
        SYSTEM$LOG_INFO('Error in step 2');
        CALL Cleanup();
        RETURN 'PROCESS FINISHED';
    EXCEPTION
        WHEN OTHER CONTINUE THEN
            STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
    END;
    
    Cleanup PROCEDURE ()
    RETURNS VARCHAR
    AS
    BEGIN
        -- PRINT 'Cleanup complete' equivalent
        SYSTEM$LOG_INFO('Cleanup complete');
        -- Last label - no fall-through
    EXCEPTION
        WHEN OTHER CONTINUE THEN
            STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
    END;

BEGIN
    CALL SC_PROCESS();
    RETURN SC_EXIT_CODE;
END;
$$;
```

---

## Pattern: Sequential Labels with Fall-Through

This pattern handles the common case where labels follow each other and execution "falls through" from one to the next.

### Before (SQL Server)

```sql
-- Step 1
DROP TABLE TableA;
IF @@ERROR <> 0 GOTO Step2;

Step1Continue:
    INSERT INTO LogTable VALUES ('Step 1 complete');

Step2:
    DROP TABLE TableB;
    IF @@ERROR <> 0 GOTO Step3;

Step3:
    DROP TABLE TableC;
```

### After (Snowflake - SnowConvert Pattern)

```sql
DECLARE
    SC_EXIT_CODE VARCHAR := '0';
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0);
    
    SC_PROCESS PROCEDURE ()
    RETURNS VARCHAR
    AS
    BEGIN
        -- Step 1
        DROP TABLE IF EXISTS TableA;
        IF (STATUS_OBJECT['SQLCODE'] != 0) THEN
            CALL Step2();
            RETURN 'PROCESS FINISHED';
        END IF;
        -- Fall-through to Step1Continue
        CALL Step1Continue();
    EXCEPTION
        WHEN OTHER CONTINUE THEN
            STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
    END;
    
    Step1Continue PROCEDURE ()
    RETURNS VARCHAR
    AS
    BEGIN
        INSERT INTO LogTable VALUES ('Step 1 complete');
        -- Fall-through to Step2
        CALL Step2();
    EXCEPTION
        WHEN OTHER CONTINUE THEN
            STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
    END;
    
    Step2 PROCEDURE ()
    RETURNS VARCHAR
    AS
    BEGIN
        DROP TABLE IF EXISTS TableB;
        IF (STATUS_OBJECT['SQLCODE'] != 0) THEN
            CALL Step3();
            RETURN 'PROCESS FINISHED';
        END IF;
        -- Fall-through to Step3
        CALL Step3();
    EXCEPTION
        WHEN OTHER CONTINUE THEN
            STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
    END;
    
    Step3 PROCEDURE ()
    RETURNS VARCHAR
    AS
    BEGIN
        DROP TABLE IF EXISTS TableC;
        -- Last label - no fall-through
    EXCEPTION
        WHEN OTHER CONTINUE THEN
            STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
    END;

BEGIN
    CALL SC_PROCESS();
    RETURN SC_EXIT_CODE;
END
```

---

## Pattern: Conditional GOTO with Error Checking

This pattern handles conditional jumps based on error codes.

### Before (SQL Server)

```sql
EXEC SomeOperation;
IF @@ERROR <> 0 GOTO HandleError;

-- Success path
EXEC AnotherOperation;
GOTO Finish;

HandleError:
    RAISERROR('Operation failed', 16, 1);

Finish:
    PRINT 'Done';
```

### After (Snowflake - SnowConvert Pattern)

```sql
DECLARE
    SC_EXIT_CODE VARCHAR := '0';
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0);
    
    SC_PROCESS PROCEDURE ()
    RETURNS VARCHAR
    AS
    BEGIN
        CALL SomeOperation();
        IF (STATUS_OBJECT['SQLCODE'] != 0) THEN
            CALL HandleError();
            RETURN 'PROCESS FINISHED';
        END IF;
        
        -- Success path
        CALL AnotherOperation();
        CALL Finish();
        RETURN 'PROCESS FINISHED';
    EXCEPTION
        WHEN OTHER CONTINUE THEN
            STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
    END;
    
    HandleError PROCEDURE ()
    RETURNS VARCHAR
    AS
    BEGIN
        -- RAISERROR equivalent
        SC_EXIT_CODE := '-1';
        SYSTEM$LOG_ERROR('Operation failed');
        -- Fall-through to Finish
        CALL Finish();
    EXCEPTION
        WHEN OTHER CONTINUE THEN
            STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
    END;
    
    Finish PROCEDURE ()
    RETURNS VARCHAR
    AS
    BEGIN
        SYSTEM$LOG_INFO('Done');
    EXCEPTION
        WHEN OTHER CONTINUE THEN
            STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
    END;

BEGIN
    CALL SC_PROCESS();
    RETURN SC_EXIT_CODE;
END
```

---

## Pattern: Multiple Error Handlers

When different error conditions jump to different handlers.

### Before (SQL Server)

```sql
BEGIN TRY
    DELETE FROM TableA WHERE ID = @ID;
END TRY
BEGIN CATCH
    IF ERROR_NUMBER() = 547  -- FK violation
        GOTO FKError;
    ELSE
        GOTO GenericError;
END CATCH

GOTO Success;

FKError:
    SET @Result = 'Foreign key violation';
    GOTO Cleanup;

GenericError:
    SET @Result = 'Unknown error';
    GOTO Cleanup;

Success:
    SET @Result = 'OK';

Cleanup:
    DROP TABLE IF EXISTS #Temp;
```

### After (Snowflake - SnowConvert Pattern)

```sql
DECLARE
    SC_EXIT_CODE VARCHAR := '0';
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0);
    Result VARCHAR := '';
    
    SC_PROCESS PROCEDURE ()
    RETURNS VARCHAR
    AS
    BEGIN
        BEGIN
            DELETE FROM TableA WHERE ID = :ID;
        EXCEPTION
            WHEN OTHER CONTINUE THEN
                STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
        END;
        
        IF (STATUS_OBJECT['SQLCODE'] != 0) THEN
            -- Check for specific error (FK violation approximation)
            IF (STATUS_OBJECT['SQLSTATE'] = '23503') THEN
                CALL FKError();
                RETURN 'PROCESS FINISHED';
            ELSE
                CALL GenericError();
                RETURN 'PROCESS FINISHED';
            END IF;
        END IF;
        
        CALL Success();
        RETURN 'PROCESS FINISHED';
    EXCEPTION
        WHEN OTHER CONTINUE THEN
            STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
    END;
    
    FKError PROCEDURE ()
    RETURNS VARCHAR
    AS
    BEGIN
        Result := 'Foreign key violation';
        CALL Cleanup();
    EXCEPTION
        WHEN OTHER CONTINUE THEN
            STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
    END;
    
    GenericError PROCEDURE ()
    RETURNS VARCHAR
    AS
    BEGIN
        Result := 'Unknown error';
        CALL Cleanup();
    EXCEPTION
        WHEN OTHER CONTINUE THEN
            STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
    END;
    
    Success PROCEDURE ()
    RETURNS VARCHAR
    AS
    BEGIN
        Result := 'OK';
        -- Fall-through to Cleanup
        CALL Cleanup();
    EXCEPTION
        WHEN OTHER CONTINUE THEN
            STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
    END;
    
    Cleanup PROCEDURE ()
    RETURNS VARCHAR
    AS
    BEGIN
        DROP TABLE IF EXISTS t_Temp;
    EXCEPTION
        WHEN OTHER CONTINUE THEN
            STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
    END;

BEGIN
    CALL SC_PROCESS();
    RETURN SC_EXIT_CODE;
END
```

---

## Alternative Patterns (Simpler Cases)

For simpler scenarios where the full SnowConvert pattern is not needed, consider these alternatives.

---

### Simple Pattern: GOTO for Error/Cleanup Handling (Using Exception Block)

When there's only one GOTO target for cleanup, use a simple exception block.

#### Before (SQL Server)
```sql
CREATE PROCEDURE MyProc
AS
BEGIN
    DECLARE @ReturnCode INT = 0;
    
    -- Step 1
    IF (some_error_condition)
    BEGIN
        SET @ReturnCode = -1;
        GOTO CleanupAndExit;
    END
    
    -- Step 2
    IF (another_error)
    BEGIN
        SET @ReturnCode = -2;
        GOTO CleanupAndExit;
    END
    
    -- Main processing...
    
CleanupAndExit:
    -- Cleanup code
    DROP TABLE IF EXISTS #TempTable;
    RETURN @ReturnCode;
END
```

#### After (Snowflake) - Using Exception Block
```sql
CREATE OR REPLACE PROCEDURE MyProc()
RETURNS INT
LANGUAGE SQL
AS
$$
DECLARE
    return_code INT := 0;
    error_occurred BOOLEAN := FALSE;
BEGIN
    BEGIN
        -- Step 1
        IF (some_error_condition) THEN
            return_code := -1;
            RAISE EXCEPTION 'Error in Step 1';
        END IF;
        
        -- Step 2
        IF (another_error) THEN
            return_code := -2;
            RAISE EXCEPTION 'Error in Step 2';
        END IF;
        
        -- Main processing...
        
    EXCEPTION
        WHEN OTHER THEN
            error_occurred := TRUE;
            -- Error already set return_code
    END;
    
    -- Cleanup code (always runs)
    DROP TABLE IF EXISTS t_TempTable;
    
    RETURN return_code;
END;
$$;
```

---

### Simple Alternative: GOTO for Conditional Skipping

For very simple skipping patterns, use IF/ELSE instead of the full SnowConvert pattern.

#### Before (SQL Server)
```sql
IF (@SkipValidation = 1)
    GOTO AfterValidation;

-- Validation code...
-- ... lots of validation ...

AfterValidation:
-- Continue with main logic
```

#### After (Snowflake) - Using IF/ELSE
```sql
IF (NOT skip_validation) THEN
    -- Validation code...
    -- ... lots of validation ...
END IF;

-- Continue with main logic (no label needed)
```

---

### Simple Alternative: GOTO for Retry Logic

For retry patterns, use WHILE loops.

#### Before (SQL Server)
```sql
DECLARE @RetryCount INT = 0;

RetryPoint:
SET @RetryCount = @RetryCount + 1;

BEGIN TRY
    -- Attempt operation
    INSERT INTO TargetTable SELECT * FROM Source;
END TRY
BEGIN CATCH
    IF @RetryCount < 3
        GOTO RetryPoint;
    ELSE
        THROW;
END CATCH
```

#### After (Snowflake) - Using WHILE Loop
```sql
DECLARE
    retry_count INT := 0;
    max_retries INT := 3;
    success BOOLEAN := FALSE;
BEGIN
    WHILE (retry_count < max_retries AND NOT success) DO
        retry_count := retry_count + 1;
        BEGIN
            -- Attempt operation
            INSERT INTO TargetTable SELECT * FROM Source;
            success := TRUE;
        EXCEPTION
            WHEN OTHER THEN
                IF (retry_count >= max_retries) THEN
                    RAISE;
                END IF;
                -- Wait before retry
                CALL SYSTEM$WAIT(1);
        END;
    END WHILE;
END;
```

---

## Complete Migration Example (SnowConvert Pattern)

### Before (SQL Server with GOTO)
```sql
CREATE PROCEDURE ProcessWithCleanup
    @InputID INT,
    @ReturnCode INT OUTPUT
AS
BEGIN
    SET @ReturnCode = 0;
    
    CREATE TABLE #WorkTable (ID INT, Value DECIMAL);
    
    -- Validation
    IF (@InputID IS NULL)
    BEGIN
        SET @ReturnCode = -1;
        GOTO CleanupAndExit;
    END
    
    -- Lock acquisition
    EXEC @LockResult = sp_getapplock @Resource = 'MyProcess';
    IF (@LockResult < 0)
    BEGIN
        SET @ReturnCode = -2;
        GOTO CleanupAndExit;
    END
    
    BEGIN TRY
        -- Main processing
        INSERT INTO #WorkTable SELECT ID, Value FROM Source WHERE ID = @InputID;
        UPDATE Target SET Processed = 1 WHERE ID = @InputID;
    END TRY
    BEGIN CATCH
        SET @ReturnCode = -3;
        GOTO CleanupAndExit;
    END CATCH
    
CleanupAndExit:
    -- Release lock if acquired
    IF (@LockResult >= 0)
        EXEC sp_releaseapplock @Resource = 'MyProcess';
    
    -- Cleanup
    DROP TABLE IF EXISTS #WorkTable;
    
    RETURN @ReturnCode;
END
```

### After (Snowflake - SnowConvert Pattern)
```sql
CREATE OR REPLACE PROCEDURE ProcessWithCleanup(input_id INT)
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
DECLARE
    SC_EXIT_CODE VARCHAR := '0';
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0);
    lock_result INT := -1;
    
    SC_PROCESS PROCEDURE ()
    RETURNS VARCHAR
    AS
    BEGIN
        -- Create work table
        CREATE OR REPLACE TEMPORARY TABLE t_WorkTable (ID INT, Value DECIMAL);
        
        -- Validation
        IF (input_id IS NULL) THEN
            SC_EXIT_CODE := '-1';
            CALL CleanupAndExit();
            RETURN 'PROCESS FINISHED';
        END IF;
        
        -- Lock acquisition (simulated)
        BEGIN
            INSERT INTO process_locks (resource_name, session_id, acquired_at)
            VALUES ('MyProcess', CURRENT_SESSION(), CURRENT_TIMESTAMP());
            lock_result := 0;
        EXCEPTION
            WHEN OTHER CONTINUE THEN
                STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
                lock_result := -1;
        END;
        
        IF (lock_result < 0) THEN
            SC_EXIT_CODE := '-2';
            CALL CleanupAndExit();
            RETURN 'PROCESS FINISHED';
        END IF;
        
        -- Main processing
        BEGIN
            INSERT INTO t_WorkTable SELECT ID, Value FROM Source WHERE ID = :input_id;
            UPDATE Target SET Processed = 1 WHERE ID = :input_id;
        EXCEPTION
            WHEN OTHER CONTINUE THEN
                STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
                SC_EXIT_CODE := '-3';
                CALL CleanupAndExit();
                RETURN 'PROCESS FINISHED';
        END;
        
        -- Success - fall through to cleanup
        CALL CleanupAndExit();
    EXCEPTION
        WHEN OTHER CONTINUE THEN
            STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
    END;
    
    CleanupAndExit PROCEDURE ()
    RETURNS VARCHAR
    AS
    BEGIN
        -- Release lock if acquired
        IF (lock_result >= 0) THEN
            DELETE FROM process_locks 
            WHERE resource_name = 'MyProcess' 
            AND session_id = CURRENT_SESSION();
        END IF;
        
        -- Cleanup
        DROP TABLE IF EXISTS t_WorkTable;
    EXCEPTION
        WHEN OTHER CONTINUE THEN
            STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
    END;

BEGIN
    CALL SC_PROCESS();
    RETURN SC_EXIT_CODE;
END;
$$;
```

---

## Transformation Rules Summary

| Original Code | SnowConvert Transformation |
|--------------|---------------------------|
| Code before first label | Goes in `SC_PROCESS` procedure |
| `LabelName:` | `LabelName PROCEDURE () RETURNS VARCHAR AS BEGIN ... END;` |
| `GOTO LabelName` | `CALL LabelName(); RETURN 'PROCESS FINISHED';` |
| `IF condition GOTO Label` | `IF (condition) THEN CALL Label(); RETURN 'PROCESS FINISHED'; END IF;` |
| `@@ERROR <> 0` | `STATUS_OBJECT['SQLCODE'] != 0` |
| Fall-through to next label | `CALL NextLabel();` at end of procedure |
| Error capture in TRY/CATCH | `EXCEPTION WHEN OTHER CONTINUE THEN STATUS_OBJECT := ...` |
| Return code | Use `SC_EXIT_CODE` variable |

## Key Points

- **GOTO and labels are not supported** in Snowflake Scripting
- **SnowConvert uses nested stored procedures** to transform labels and GOTOs
- Each **label becomes a nested procedure** with the same name
- **GOTO becomes** `CALL LabelName(); RETURN 'PROCESS FINISHED';`
- **Fall-through behavior** is preserved by calling the next label at the end of each procedure
- **STATUS_OBJECT** tracks error state (`SQLCODE`, `SQLERRM`, `SQLSTATE`)
- **SC_EXIT_CODE** is the return value of the script
- **SC_PROCESS** is the entry point procedure containing code before the first label
- Use `EXCEPTION WHEN OTHER CONTINUE THEN` to capture errors without stopping execution
- Nested procedures can **access parent variables** declared before them

## Nested Stored Procedure Limitations

- Cannot be defined inside other nested procedures or control structures (FOR, WHILE)
- Each nested procedure must have a **unique name** within its block
- Do not support **OUTPUT (OUT) arguments** - use shared variables instead
- Do not support **optional arguments with DEFAULT values**
- Cannot be called in `EXECUTE IMMEDIATE` statements

## Resources

**Snowflake:**
- [Nested Stored Procedures](https://docs.snowflake.com/en/developer-guide/stored-procedure/stored-procedures-snowflake-scripting#using-nested-stored-procedures) - **Recommended reading**
- [Writing Stored Procedures in Snowflake Scripting](https://docs.snowflake.com/en/developer-guide/stored-procedure/stored-procedures-snowflake-scripting)
- [Exception Handling](https://docs.snowflake.com/en/developer-guide/snowflake-scripting/exceptions)
- [Branching Constructs](https://docs.snowflake.com/en/developer-guide/snowflake-scripting/branching)
- [Looping Constructs](https://docs.snowflake.com/en/developer-guide/snowflake-scripting/loops)
- [Block Labels and LEAVE](https://docs.snowflake.com/en/developer-guide/snowflake-scripting/blocks#label)

**SQL Server:**
- [GOTO Statement](https://learn.microsoft.com/en-us/sql/t-sql/language-elements/goto-transact-sql)
