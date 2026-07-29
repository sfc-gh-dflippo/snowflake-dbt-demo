---
description:
  "Amazon Redshift, which uses PL/pgSQL for procedural logic, supports EXIT handlers in stored
  procedures through EXCEPTION blocks. An EXIT handler terminates the current block when a specific
  condition "
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/redshift/redshift-exit-handler
title: SnowConvert AI - Redshift - EXIT HANDLER | Snowflake Documentation
---

## Description

Amazon Redshift, which uses PL/pgSQL for procedural logic, supports EXIT handlers in stored
procedures through EXCEPTION blocks. An EXIT handler terminates the current block when a specific
condition is met and transfers control to the handler code.

When migrating code from database systems that use EXIT HANDLERs (such as DB2, Teradata, or other
systems) to Snowflake, SnowConvert AI transforms these constructs into equivalent Snowflake
Scripting exception handling mechanisms.

An EXIT HANDLER causes the procedure to exit the current block and return control to the caller
after executing the handler code. In Snowflake, this behavior is emulated using EXCEPTION blocks
with appropriate logic.

For more information about Redshift exception handling, see
[Exception Handling in PL/pgSQL](https://docs.aws.amazon.com/redshift/latest/dg/c_PLpgSQL-statements.html#r_PLpgSQL-messages-errors).

## Grammar Syntax

Redshift does not have native `DECLARE EXIT HANDLER` syntax. However, when converting from other
database systems, the source pattern typically looks like:

```sql
-- Pattern from source systems (e.g., DB2, Teradata)
DECLARE EXIT HANDLER FOR condition_value
  handler_action_statement;
```

In Redshift, exception handling uses:

```sql
BEGIN
  -- statements
EXCEPTION
  WHEN condition THEN
    -- handler statements that exit the block
END;
```

## Sample Source Patterns

### EXIT HANDLER Conversion to Snowflake

When migrating stored procedures from systems with EXIT HANDLER to Snowflake via Redshift,
SnowConvert AI transforms them into Snowflake-compatible exception handling.

#### Input Code

##### Source (DB2/Teradata Pattern)

```sql
-- Example pattern from source system
CREATE PROCEDURE exit_handler_procedure()
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        INSERT INTO error_log VALUES (CURRENT_TIMESTAMP, 'Error occurred, exiting');
        ROLLBACK;
    END;

    -- Main procedure logic
    INSERT INTO orders VALUES (1, 100.00);
    UPDATE inventory SET quantity = quantity - 1 WHERE product_id = 1;

    -- This will NOT execute if an error occurred
    INSERT INTO audit_log VALUES ('Transaction completed');
END;
```

#### Output Code

##### Snowflake Scripting

```sql
CREATE OR REPLACE PROCEDURE exit_handler_procedure()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "01/15/2025" }}'
AS
$$
    BEGIN
        -- Main procedure logic
        INSERT INTO orders VALUES (1, 100.00);
        UPDATE inventory SET quantity = quantity - 1 WHERE product_id = 1;

        -- This will NOT execute if an error occurred
        INSERT INTO audit_log VALUES ('Transaction completed');

        EXCEPTION
            WHEN OTHER THEN
                BEGIN
                    INSERT INTO error_log
                    VALUES (CURRENT_TIMESTAMP(), 'Error occurred, exiting');
                    ROLLBACK;
                END;
    END;
$$;
```

### EXIT HANDLER with Specific SQLSTATE

#### Input Code 2

##### Source (DB2/Teradata Pattern) 2

```sql
CREATE PROCEDURE specific_error_exit()
BEGIN
    DECLARE EXIT HANDLER FOR SQLSTATE '23505'
    BEGIN
        INSERT INTO error_log VALUES ('Duplicate key error');
    END;

    INSERT INTO users VALUES (1, 'John');
    INSERT INTO users VALUES (1, 'Jane');  -- Duplicate key

    -- This will NOT execute
    INSERT INTO success_log VALUES ('Completed');
END;
```

#### Output Code 2

##### Snowflake Scripting 2

```sql
CREATE OR REPLACE PROCEDURE specific_error_exit()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "01/15/2025" }}'
AS
$$
    BEGIN
        INSERT INTO users VALUES (1, 'John');
        INSERT INTO users VALUES (1, 'Jane');  -- Duplicate key

        -- This will NOT execute
        INSERT INTO success_log VALUES ('Completed');

        EXCEPTION
            WHEN OTHER EXIT THEN
                CASE
                    WHEN (SQLSTATE = '23505') THEN
                        INSERT INTO error_log VALUES ('Duplicate key error')
                END;
    END;
$$;
```

### EXIT HANDLER for NOT FOUND

#### Input Code 3

##### Source (DB2/Teradata Pattern) 3

```sql
CREATE PROCEDURE not_found_exit()
BEGIN
    DECLARE v_name VARCHAR(100);

    DECLARE EXIT HANDLER FOR NOT FOUND
        INSERT INTO log_table VALUES ('No data found, exiting');

    SELECT name INTO v_name FROM employees WHERE id = 9999;

    -- This will NOT execute if no data found
    INSERT INTO results VALUES (v_name);
END;
```

#### Output Code 3

##### Snowflake Scripting 3

```sql
CREATE OR REPLACE PROCEDURE not_found_exit()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "01/15/2025" }}'
AS
$$
    DECLARE
        v_name VARCHAR(100);
    BEGIN
        SELECT name INTO v_name FROM employees WHERE id = 9999;

        -- This will NOT execute if no data found
        INSERT INTO results VALUES (v_name);

        EXCEPTION
            WHEN NO_DATA_FOUND THEN
                INSERT INTO log_table VALUES ('No data found, exiting');
    END;
$$;
```

### EXIT HANDLER with Cursor

#### Input Code 4

##### Source (DB2/Teradata Pattern) 4

```sql
CREATE PROCEDURE cursor_exit_handler()
BEGIN
    DECLARE v_id INT;
    DECLARE v_name VARCHAR(100);
    DECLARE v_count INT := 0;

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        INSERT INTO error_log VALUES ('Error in cursor processing');
        RETURN -1;
    END;

    DECLARE cur CURSOR FOR SELECT id, name FROM employees;

    OPEN cur;
    LOOP
        FETCH cur INTO v_id, v_name;
        EXIT WHEN NOT FOUND;

        -- Process each row
        INSERT INTO processed_employees VALUES (v_id, v_name);
        v_count := v_count + 1;
    END LOOP;
    CLOSE cur;

    RETURN v_count;
END;
```

#### Output Code 4

##### Snowflake Scripting 4

```sql
CREATE OR REPLACE PROCEDURE cursor_exit_handler()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "01/15/2025" }}'
AS
$$
    DECLARE
        v_id INT;
        v_name VARCHAR(100);
        v_count INT := 0;
        cur CURSOR FOR SELECT id, name FROM employees;
    BEGIN
        OPEN cur;
        LOOP
            FETCH cur INTO v_id, v_name;
            IF (SQLCODE != 0) THEN
                BREAK;
            END IF;

            -- Process each row
            INSERT INTO processed_employees VALUES (v_id, v_name);
            v_count := v_count + 1;
        END LOOP;
        CLOSE cur;

        RETURN v_count;

        EXCEPTION
            WHEN OTHER THEN
                BEGIN
                    INSERT INTO error_log VALUES ('Error in cursor processing');
                    RETURN -1;
                END;
    END;
$$;
```

## Known Issues

### EXIT HANDLER Behavior

The conversion from EXIT HANDLER to Snowflake exception handling provides equivalent termination
behavior:

1. **Block Termination**: Both EXIT HANDLER and Snowflake EXCEPTION blocks terminate the current
   BEGIN…END block.
2. **Return Control**: After executing the handler code, control returns to the caller.
3. **Execution Flow**: Statements after the error point are not executed.

### Multiple EXIT Handlers

When multiple EXIT HANDLERs are defined with different conditions, they must be merged into
conditional logic:

#### Source Pattern

```sql
DECLARE EXIT HANDLER FOR SQLSTATE '23505'
    INSERT INTO log VALUES ('Duplicate key');

DECLARE EXIT HANDLER FOR SQLEXCEPTION
    INSERT INTO log VALUES ('General error');
```

#### Snowflake

```sql
EXCEPTION
    WHEN OTHER EXIT THEN
        CASE
            WHEN (SQLSTATE = '23505') THEN
                INSERT INTO log VALUES ('Duplicate key')
            ELSE
                INSERT INTO log VALUES ('General error')
        END;
```

### Mixed CONTINUE and EXIT Handlers

Source systems that allow mixing CONTINUE and EXIT handlers in the same block present special
challenges. Snowflake does not support this pattern in a single EXCEPTION block.

#### Related EWIs

1. [SSC-EWI-0114](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0114):
   MIXED CONTINUE AND EXIT EXCEPTION HANDLERS IN THE SAME BLOCK ARE NOT SUPPORTED BY SNOWFLAKE
   SCRIPTING

### SQLSTATE Mapping

Not all SQLSTATE codes from source systems map directly to Snowflake exception types. SnowConvert AI
performs best-effort mapping:

<!-- prettier-ignore -->
|Source SQLSTATE|Condition|Snowflake Equivalent|
|---|---|---|
|02000|NO DATA|NO_DATA_FOUND|
|23xxx|Integrity Constraint|STATEMENT_ERROR|
|42xxx|Syntax Error|STATEMENT_ERROR|
|Other|General|OTHER|

## Best Practices

When working with converted EXIT HANDLER code in Snowflake:

1. **Understand Exit Semantics**: EXIT handlers terminate the current block. Verify this matches
   your requirements.
2. **Test Error Conditions**: Thoroughly test all error scenarios to ensure proper exit behavior.
3. **Use Return Values**: Consider using RETURN statements in exception handlers to communicate
   status.
4. **Implement Logging**: Add comprehensive logging to track when and why procedures exit.
5. **Transaction Management**: Use Snowflake’s transaction support to maintain data consistency.
6. **Nested Blocks**: Remember that EXIT only affects the current block, not outer blocks or the
   entire procedure.
7. **Error Information**: Capture error details (SQLCODE, SQLERRM, SQLSTATE) in exception handlers
   for debugging.

## Related Documentation

- [Snowflake Exception Handling](https://docs.snowflake.com/en/developer-guide/snowflake-scripting/exceptions)
- [Redshift Exception Handling](https://docs.aws.amazon.com/redshift/latest/dg/c_PLpgSQL-statements.html#r_PLpgSQL-messages-errors)
- [CREATE PROCEDURE](rs-sql-statements-create-procedure)

## See Also

- [CONTINUE HANDLER](redshift-continue-handler)
- [EXCEPTION](rs-sql-statements-create-procedure.html#exception)
- [RAISE](rs-sql-statements-create-procedure.html#raise)
- [DECLARE](rs-sql-statements-create-procedure.html#declare)
