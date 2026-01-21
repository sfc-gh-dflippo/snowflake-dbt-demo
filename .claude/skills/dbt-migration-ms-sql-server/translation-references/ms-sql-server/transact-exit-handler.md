---
description:
  "In SQL Server and Azure Synapse Analytics, exception handling is primarily managed through
  TRY...CATCH blocks. Unlike some other database systems (such as Teradata or DB2), SQL Server does
  not have a "
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/transact/transact-exit-handler
title: SnowConvert AI - SQL Server-Azure Synapse - EXIT HANDLER | Snowflake Documentation
---

## Description[¶](#description)

In SQL Server and Azure Synapse Analytics, exception handling is primarily managed through
`TRY...CATCH` blocks. Unlike some other database systems (such as Teradata or DB2), SQL Server does
not have a native `DECLARE EXIT HANDLER` statement.

However, when migrating code from other database systems that use EXIT HANDLERs, SnowConvert AI
transforms these constructs into equivalent Snowflake Scripting exception handling mechanisms.

An EXIT HANDLER in source systems terminates the current block when a specific condition is met and
transfers control to the handler code before returning to the caller. In Snowflake, this is achieved
using EXCEPTION blocks with appropriate exit behavior.

For more information about SQL Server error handling, see
[TRY…CATCH (Transact-SQL)](https://docs.microsoft.com/en-us/sql/t-sql/language-elements/try-catch-transact-sql).

## Grammar Syntax[¶](#grammar-syntax)

SQL Server does not have native EXIT HANDLER syntax. However, when converting from other database
systems, the source pattern typically looks like:

```
-- Pattern from source systems (e.g., DB2, Teradata)
DECLARE EXIT HANDLER FOR condition_value
  handler_action_statement;
```

## Sample Source Patterns[¶](#sample-source-patterns)

### EXIT HANDLER Conversion from DB2/Teradata[¶](#exit-handler-conversion-from-db2-teradata)

When migrating stored procedures from DB2 or Teradata that contain EXIT HANDLER declarations,
SnowConvert AI transforms them into Snowflake-compatible exception handling.

#### Input Code:[¶](#input-code)

##### Source (DB2/Teradata Pattern)[¶](#source-db2-teradata-pattern)

```
-- Example pattern from source system
CREATE PROCEDURE exit_handler_example()
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        INSERT INTO error_log VALUES (SQLCODE, SQLERRM, CURRENT_TIMESTAMP);
        ROLLBACK;
    END;

    -- Main procedure logic
    INSERT INTO orders VALUES (1, 100.00);
    UPDATE inventory SET quantity = quantity - 1 WHERE product_id = 1;

    -- This will NOT execute if an error occurred
    INSERT INTO audit_log VALUES ('Transaction completed successfully');
END;
```

#### Output Code:[¶](#output-code)

##### Snowflake Scripting[¶](#snowflake-scripting)

```
CREATE OR REPLACE PROCEDURE exit_handler_example()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        -- Main procedure logic
        INSERT INTO orders VALUES (1, 100.00);
        UPDATE inventory SET quantity = quantity - 1 WHERE product_id = 1;

        -- This will NOT execute if an error occurred
        INSERT INTO audit_log VALUES ('Transaction completed successfully');

        EXCEPTION
            WHEN OTHER THEN
                BEGIN
                    INSERT INTO error_log
                    VALUES (:SQLCODE, :SQLERRM, CURRENT_TIMESTAMP());
                    ROLLBACK;
                END;
    END;
$$;
```

### EXIT HANDLER with Specific Error Codes[¶](#exit-handler-with-specific-error-codes)

#### Input Code:[¶](#id1)

##### Source (DB2/Teradata Pattern)[¶](#id2)

```
CREATE PROCEDURE specific_error_handler()
BEGIN
    DECLARE EXIT HANDLER FOR SQLSTATE '23505'
    BEGIN
        INSERT INTO error_log VALUES ('Duplicate key error');
        RETURN -1;
    END;

    INSERT INTO users VALUES (1, 'John Doe');
    INSERT INTO users VALUES (1, 'Jane Doe');  -- Will trigger handler

    -- This will NOT execute
    INSERT INTO success_log VALUES ('All inserts completed');
END;
```

#### Output Code:[¶](#id3)

##### Snowflake Scripting[¶](#id4)

```
CREATE OR REPLACE PROCEDURE specific_error_handler()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        INSERT INTO users VALUES (1, 'John Doe');
        INSERT INTO users VALUES (1, 'Jane Doe');  -- Will trigger handler

        -- This will NOT execute
        INSERT INTO success_log VALUES ('All inserts completed');

        EXCEPTION
            WHEN OTHER THEN
                LET errcode := :SQLCODE;
                LET sqlerrmsg := :SQLERRM;
                IF (errcode = '100183' OR CONTAINS(sqlerrmsg, 'duplicate key')) THEN
                    INSERT INTO error_log VALUES ('Duplicate key error');
                    RETURN -1;
                ELSE
                    RAISE;
                END IF;
    END;
$$;
```

### EXIT HANDLER with NOT FOUND[¶](#exit-handler-with-not-found)

#### Input Code:[¶](#id5)

##### Source (DB2/Teradata Pattern)[¶](#id6)

```
CREATE PROCEDURE not_found_handler()
BEGIN
    DECLARE v_name VARCHAR(100);

    DECLARE EXIT HANDLER FOR NOT FOUND
    BEGIN
        INSERT INTO log_table VALUES ('Record not found');
        RETURN 0;
    END;

    SELECT name INTO v_name FROM employees WHERE id = 9999;

    -- This will NOT execute if no record found
    INSERT INTO results VALUES (v_name);
END;
```

#### Output Code:[¶](#id7)

##### Snowflake Scripting[¶](#id8)

```
CREATE OR REPLACE PROCEDURE not_found_handler()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        v_name VARCHAR(100);
    BEGIN
        SELECT name INTO v_name FROM employees WHERE id = 9999;

        -- This will NOT execute if no record found
        INSERT INTO results VALUES (v_name);

        EXCEPTION
            WHEN NO_DATA_FOUND THEN
                BEGIN
                    INSERT INTO log_table VALUES ('Record not found');
                    RETURN 0;
                END;
    END;
$$;
```

## Known Issues[¶](#known-issues)

### EXIT HANDLER Behavior[¶](#exit-handler-behavior)

Applies to

- SQL Server
- Azure Synapse Analytics

SQL Server’s native `TRY...CATCH` mechanism provides similar functionality to EXIT HANDLER. When an
error occurs in a TRY block, control passes to the CATCH block, and execution does not continue
after the CATCH block in the current scope.

SnowConvert AI transforms EXIT HANDLER patterns to Snowflake EXCEPTION blocks, which provide
equivalent exit behavior:

1. **Execution Termination**: The current block is terminated when an exception occurs.
2. **Control Flow**: Control passes to the exception handler, executes the handler code, then exits
   the block.
3. **Return Behavior**: The procedure can return a value or status from within the exception
   handler.

### Multiple EXIT Handlers[¶](#multiple-exit-handlers)

When multiple EXIT HANDLERs are defined in the source system, they must be merged into a single
EXCEPTION block with conditional logic:

#### Source Pattern[¶](#source-pattern)

```
DECLARE EXIT HANDLER FOR SQLSTATE '23505'
    INSERT INTO log VALUES ('Duplicate key');

DECLARE EXIT HANDLER FOR SQLEXCEPTION
    INSERT INTO log VALUES ('General error');
```

#### Snowflake[¶](#snowflake)

```
EXCEPTION
    WHEN OTHER THEN
        LET errcode := :SQLCODE;
        LET sqlerrmsg := :SQLERRM;
        IF (errcode = '100183' OR CONTAINS(sqlerrmsg, 'duplicate key')) THEN
            INSERT INTO log VALUES ('Duplicate key');
        ELSE
            INSERT INTO log VALUES ('General error');
        END IF;
```

### Mixed CONTINUE and EXIT Handlers[¶](#mixed-continue-and-exit-handlers)

Applies to

- SQL Server
- Azure Synapse Analytics

Source systems may allow mixing CONTINUE and EXIT handlers in the same block. This pattern cannot be
directly replicated in Snowflake, as EXCEPTION blocks handle errors uniformly.

When this pattern is encountered:

- Separate EXCEPTION blocks may be generated
- An EWI warning (`SSC-EWI-0114`) is added
- Manual review is recommended

#### Related EWIs[¶](#related-ewis)

1. [SSC-EWI-0114](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0114):
   MIXED CONTINUE AND EXIT EXCEPTION HANDLERS IN THE SAME BLOCK ARE NOT SUPPORTED BY SNOWFLAKE
   SCRIPTING

## Best Practices[¶](#best-practices)

When working with converted EXIT HANDLER code:

1. **Understand Exit Semantics**: EXIT handlers terminate the current block. Verify this matches
   your application’s requirements.
2. **Test Error Scenarios**: Thoroughly test all error conditions to ensure proper exit behavior.
3. **Use Transactions**: Leverage Snowflake’s transaction support for data consistency.
4. **Return Values**: Use RETURN statements in exception handlers to communicate exit status to
   callers.
5. **Logging**: Implement comprehensive error logging to track when and why procedures exit.
6. **Nested Blocks**: Remember that EXIT behavior only affects the current block, not outer blocks.

## Related Documentation[¶](#related-documentation)

- [Snowflake Exception Handling](https://docs.snowflake.com/en/developer-guide/snowflake-scripting/exceptions)
- [SQL Server TRY…CATCH](https://docs.microsoft.com/en-us/sql/t-sql/language-elements/try-catch-transact-sql)
- [TRY CATCH Translation Reference](transact-create-procedure-snow-script.html#try-catch)

## See Also[¶](#see-also)

- [CONTINUE HANDLER](transact-continue-handler)
- [CREATE PROCEDURE](transact-create-procedure)
- [CREATE PROCEDURE - Snowflake Scripting](transact-create-procedure-snow-script)
- [General Statements](transact-general-statements)
