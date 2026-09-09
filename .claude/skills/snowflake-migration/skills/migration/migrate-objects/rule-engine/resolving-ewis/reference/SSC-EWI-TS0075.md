# SSC-EWI-TS0075 - Built-In Procedure Not Supported

Certain SQL Server system stored procedures have no direct equivalent in Snowflake. This EWI identifies procedures that require manual replacement with Snowflake-compatible patterns.

## Quick Reference

| SQL Server Procedure | Snowflake Alternative |
|---------------------|----------------------|
| `sp_getapplock` | Use Streams, Tasks, or external locking |
| `sp_releaseapplock` | Remove - not needed with Snowflake alternatives |
| `sp_xml_preparedocument` | Use PARSE_XML() or XMLGET() functions |
| `sp_xml_removedocument` | Remove - not needed in Snowflake |
| `sp_executesql` | Use EXECUTE IMMEDIATE |
| `sp_addmessage` | Not supported - use custom error handling |

## Identification

Look for the marker:
```
!!!RESOLVE EWI!!! /*** SSC-EWI-TS0075 - TRANSLATION FOR BUILT-IN PROCEDURE '<proc_name>' IS NOT CURRENTLY SUPPORTED. ***/!!!
```

---

## Application Locking (sp_getapplock / sp_releaseapplock)

SQL Server uses `sp_getapplock` and `sp_releaseapplock` for application-level locking to coordinate concurrent access. Snowflake has a different concurrency model.

### SQL Server Pattern
```sql
-- Acquire lock
EXEC @result = sp_getapplock 
    @Resource = 'MyProcess',
    @LockMode = 'Exclusive',
    @LockOwner = 'Session',
    @LockTimeout = 30000;

IF @result < 0
    RAISERROR('Could not acquire lock', 16, 1);

-- Do work...

-- Release lock
EXEC sp_releaseapplock 
    @Resource = 'MyProcess',
    @LockOwner = 'Session';
```

### Snowflake Alternatives

#### Option 1: Locking Table Pattern (Recommended)

Create a locking table to coordinate access:

```sql
-- Create locking table (one-time setup)
CREATE TABLE IF NOT EXISTS process_locks (
    resource_name VARCHAR PRIMARY KEY,
    locked_by VARCHAR,
    locked_at TIMESTAMP_NTZ,
    lock_expires_at TIMESTAMP_NTZ
);

-- Acquire lock
CREATE OR REPLACE PROCEDURE acquire_lock(resource_name VARCHAR, timeout_seconds INT)
RETURNS BOOLEAN
LANGUAGE SQL
AS
$$
DECLARE
    lock_acquired BOOLEAN := FALSE;
    start_time TIMESTAMP_NTZ := CURRENT_TIMESTAMP();
BEGIN
    -- Try to acquire lock
    WHILE (NOT lock_acquired AND TIMESTAMPDIFF(SECOND, start_time, CURRENT_TIMESTAMP()) < timeout_seconds) DO
        BEGIN
            -- Clean expired locks
            DELETE FROM process_locks 
            WHERE resource_name = :resource_name 
            AND lock_expires_at < CURRENT_TIMESTAMP();
            
            -- Try to insert lock
            INSERT INTO process_locks (resource_name, locked_by, locked_at, lock_expires_at)
            VALUES (:resource_name, CURRENT_SESSION(), CURRENT_TIMESTAMP(), 
                    TIMESTAMPADD(MINUTE, 30, CURRENT_TIMESTAMP()));
            
            lock_acquired := TRUE;
        EXCEPTION
            WHEN OTHER THEN
                -- Lock exists, wait and retry
                CALL SYSTEM$WAIT(1);  -- Wait 1 second
        END;
    END WHILE;
    
    RETURN lock_acquired;
END;
$$;

-- Release lock
CREATE OR REPLACE PROCEDURE release_lock(resource_name VARCHAR)
RETURNS BOOLEAN
LANGUAGE SQL
AS
$$
BEGIN
    DELETE FROM process_locks 
    WHERE resource_name = :resource_name 
    AND locked_by = CURRENT_SESSION();
    RETURN TRUE;
END;
$$;
```

**Usage:**
```sql
-- In your procedure
LET lock_result BOOLEAN := (CALL acquire_lock('CostAllocation_Process', 30));

IF (NOT lock_result) THEN
    -- Handle lock failure
    RETURN 'Could not acquire lock';
END IF;

-- Do work...

CALL release_lock('CostAllocation_Process');
```

#### Option 2: Using Tasks for Serialization

For scheduled processes, use Snowflake Tasks with non-overlapping schedules:

```sql
CREATE OR REPLACE TASK my_process_task
    WAREHOUSE = my_warehouse
    SCHEDULE = 'USING CRON 0 */1 * * * UTC'  -- Every hour
    ALLOW_OVERLAPPING_EXECUTION = FALSE      -- Prevents concurrent runs
AS
    CALL my_process_procedure();
```

#### Option 3: Stream-Based Processing

Use Streams for change data capture to avoid concurrent processing of the same data:

```sql
CREATE OR REPLACE STREAM my_stream ON TABLE source_table;

-- Process only new/changed rows
INSERT INTO target_table
SELECT * FROM my_stream;
-- Stream is automatically consumed after successful transaction
```

---

## XML Document Handling (sp_xml_preparedocument / sp_xml_removedocument)

SQL Server uses these procedures with OPENXML for shredding XML into relational format. Snowflake uses different XML parsing functions.

### SQL Server Pattern
```sql
DECLARE @XMLHandle INT;
DECLARE @XMLData XML = '<Entities><Entity Code="A" Name="Alpha"/></Entities>';

-- Prepare XML document
EXEC sp_xml_preparedocument @XMLHandle OUTPUT, @XMLData;

-- Query using OPENXML
SELECT * FROM OPENXML(@XMLHandle, '/Entities/Entity', 2)
WITH (Code VARCHAR(10), Name VARCHAR(100));

-- Release document
EXEC sp_xml_removedocument @XMLHandle;
```

### Snowflake Alternative: PARSE_XML + FLATTEN

```sql
DECLARE
    xml_data VARCHAR := '<Entities><Entity Code="A" Name="Alpha"/><Entity Code="B" Name="Beta"/></Entities>';
    parsed_xml VARIANT;
BEGIN
    -- Parse XML to VARIANT (no prepare/remove needed)
    parsed_xml := PARSE_XML(:xml_data);
    
    -- Query using FLATTEN
    INSERT INTO entity_table (code, entity_name)
    SELECT 
        XMLGET(f.VALUE, '@Code')::VARCHAR AS code,
        XMLGET(f.VALUE, '@Name')::VARCHAR AS entity_name
    FROM LATERAL FLATTEN(INPUT => XMLGET(:parsed_xml, 'Entity')) f;
END;
```

### Snowflake Alternative: Direct XML Functions

For simpler XML access:

```sql
-- Parse XML
LET xml_var := PARSE_XML('<root><item id="1">Value1</item></root>');

-- Get element value
LET item_value := XMLGET(:xml_var, 'item'):"$"::VARCHAR;  -- Returns 'Value1'

-- Get attribute
LET item_id := XMLGET(:xml_var, 'item'):"@id"::VARCHAR;   -- Returns '1'
```

### XML with Namespaces

```sql
DECLARE
    xml_data VARCHAR := '<ns:Root xmlns:ns="http://example.com"><ns:Item>Value</ns:Item></ns:Root>';
    parsed VARIANT;
BEGIN
    parsed := PARSE_XML(:xml_data);
    
    -- Access with namespace prefix in path
    LET item_val := GET(:parsed, 'ns:Item'):"$"::VARCHAR;
END;
```

---

## Complete Migration Example

### Before (SQL Server with sp_getapplock)
```sql
CREATE PROCEDURE ProcessData
AS
BEGIN
    DECLARE @LockResult INT;
    
    EXEC @LockResult = sp_getapplock 
        @Resource = 'DataProcess', 
        @LockMode = 'Exclusive';
    
    IF @LockResult < 0
    BEGIN
        RAISERROR('Lock failed', 16, 1);
        RETURN -1;
    END
    
    -- Process data
    UPDATE target SET processed = 1 WHERE processed = 0;
    
    EXEC sp_releaseapplock @Resource = 'DataProcess';
    RETURN 0;
END
```

### After (Snowflake with Locking Table)
```sql
CREATE OR REPLACE PROCEDURE ProcessData()
RETURNS INT
LANGUAGE SQL
AS
$$
DECLARE
    lock_acquired BOOLEAN;
BEGIN
    -- Acquire lock using locking table
    lock_acquired := (CALL acquire_lock('DataProcess', 30));
    
    IF (NOT lock_acquired) THEN
        RETURN -1;  -- Lock failed
    END IF;
    
    BEGIN
        -- Process data
        UPDATE target SET processed = 1 WHERE processed = 0;
        
        -- Release lock
        CALL release_lock('DataProcess');
        RETURN 0;
    EXCEPTION
        WHEN OTHER THEN
            -- Ensure lock is released on error
            CALL release_lock('DataProcess');
            RAISE;
    END;
END;
$$;
```

---

## Key Points

- **sp_getapplock/sp_releaseapplock**: Use locking table pattern, Tasks, or Streams
- **sp_xml_preparedocument/removedocument**: Use PARSE_XML() - no handle management needed
- **OPENXML**: Replace with FLATTEN + XMLGET
- Consider Snowflake's different concurrency model - many locking scenarios aren't needed
- Tasks with `ALLOW_OVERLAPPING_EXECUTION = FALSE` prevent concurrent execution

## Resources

**Snowflake:**
- [PARSE_XML Function](https://docs.snowflake.com/en/sql-reference/functions/parse_xml)
- [XMLGET Function](https://docs.snowflake.com/en/sql-reference/functions/xmlget)
- [FLATTEN Function](https://docs.snowflake.com/en/sql-reference/functions/flatten)
- [Tasks](https://docs.snowflake.com/en/user-guide/tasks-intro)
- [Streams](https://docs.snowflake.com/en/user-guide/streams-intro)
- [Transactions](https://docs.snowflake.com/en/sql-reference/transactions)

**SQL Server:**
- [sp_getapplock](https://learn.microsoft.com/en-us/sql/relational-databases/system-stored-procedures/sp-getapplock-transact-sql)
- [sp_releaseapplock](https://learn.microsoft.com/en-us/sql/relational-databases/system-stored-procedures/sp-releaseapplock-transact-sql)
- [sp_xml_preparedocument](https://learn.microsoft.com/en-us/sql/relational-databases/system-stored-procedures/sp-xml-preparedocument-transact-sql)
- [OPENXML](https://learn.microsoft.com/en-us/sql/t-sql/functions/openxml-transact-sql)
