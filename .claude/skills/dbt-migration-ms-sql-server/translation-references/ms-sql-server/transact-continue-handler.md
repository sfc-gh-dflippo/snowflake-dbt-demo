---
description:
  "In SQL Server and Azure Synapse Analytics, exception handling is primarily managed through
  TRY...CATCH blocks. Unlike some other database systems (such as Teradata or DB2), SQL Server does
  not have a "
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/transact/transact-continue-handler
title: SnowConvert AI - SQL Server-Azure Synapse - CONTINUE HANDLER | Snowflake Documentation
---

## Description[¶](#description)

In SQL Server and Azure Synapse Analytics, exception handling is primarily managed through
`TRY...CATCH` blocks. Unlike some other database systems (such as Teradata or DB2), SQL Server does
not have a native `DECLARE CONTINUE HANDLER` statement.

However, when migrating code from other database systems that use CONTINUE HANDLERs, SnowConvert AI
transforms these constructs into equivalent Snowflake Scripting exception handling mechanisms.

A CONTINUE HANDLER in the source system allows execution to continue after an error occurs,
performing specific actions when certain conditions are met. In Snowflake, this is achieved using
EXCEPTION blocks with conditional logic.

For more information about SQL Server error handling, see
[TRY…CATCH (Transact-SQL)](https://docs.microsoft.com/en-us/sql/t-sql/language-elements/try-catch-transact-sql).

## Grammar Syntax[¶](#grammar-syntax)

SQL Server does not have native CONTINUE HANDLER syntax. However, when converting from other
database systems, the source pattern typically looks like:

```
-- Pattern from source systems (e.g., DB2, Teradata)
DECLARE CONTINUE HANDLER FOR condition_value
  handler_action_statement;
```

## Sample Source Patterns[¶](#sample-source-patterns)

### CONTINUE HANDLER Conversion from DB2/Teradata[¶](#continue-handler-conversion-from-db2-teradata)

When migrating stored procedures from DB2 or Teradata that contain CONTINUE HANDLER declarations,
SnowConvert AI transforms them into Snowflake-compatible exception handling.

#### Input Code:[¶](#input-code)

##### Source (DB2/Teradata Pattern)[¶](#source-db2-teradata-pattern)

```
-- Example pattern from source system
CREATE PROCEDURE example_procedure()
BEGIN
    DECLARE CONTINUE HANDLER FOR SQLSTATE '02000'
    BEGIN
        -- Handler action
        SET error_count = error_count + 1;
    END;

    -- Main procedure logic
    SELECT * FROM non_existent_table;
END;
```

#### Output Code:[¶](#output-code)

##### Snowflake Scripting[¶](#snowflake-scripting)

```
CREATE OR REPLACE PROCEDURE example_procedure()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        error_count INTEGER := 0;
    BEGIN
        BEGIN
            -- Main procedure logic
            SELECT * FROM non_existent_table;
        EXCEPTION
            WHEN OTHER THEN
                -- Handler action
                error_count := error_count + 1;
                -- Continue execution
        END;
    END;
$$;
```

### CONTINUE HANDLER with SQLEXCEPTION[¶](#continue-handler-with-sqlexception)

#### Input Code:[¶](#id1)

##### Source (DB2/Teradata Pattern)[¶](#id2)

```
CREATE PROCEDURE handler_example()
BEGIN
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
        INSERT INTO error_log VALUES (SQLCODE, SQLERRM);

    -- Procedure body with multiple statements
    DELETE FROM table1 WHERE id = 0/0;
    INSERT INTO table2 VALUES (1, 'Success');
END;
```

#### Output Code:[¶](#id3)

##### Snowflake Scripting[¶](#id4)

```
CREATE OR REPLACE PROCEDURE handler_example()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        BEGIN
            -- Procedure body with multiple statements
            DELETE FROM table1 WHERE id = 0/0;
        EXCEPTION
            WHEN OTHER THEN
                INSERT INTO error_log
                SELECT :SQLCODE, :SQLERRM;
                -- Continue execution
        END;

        INSERT INTO table2 VALUES (1, 'Success');
    END;
$$;
```

## Known Issues[¶](#known-issues)

### Limited CONTINUE HANDLER Support[¶](#limited-continue-handler-support)

Applies to

- SQL Server
- Azure Synapse Analytics

SQL Server’s native `TRY...CATCH` mechanism does not have an exact equivalent to CONTINUE HANDLER.
When an error occurs in a TRY block, control immediately passes to the CATCH block, and execution
does not continue from the point of error.

SnowConvert AI attempts to emulate CONTINUE HANDLER behavior in Snowflake, but there are
limitations:

1. **Execution Flow**: True CONTINUE HANDLER behavior (continuing from the exact point of error)
   cannot be fully replicated.
2. **Statement-level Wrapping**: Individual statements may need to be wrapped in separate exception
   blocks.
3. **Performance**: Multiple nested exception blocks can impact performance.

#### Known Issues[¶](#id5)

When migrating CONTINUE HANDLER patterns from other database systems through SQL Server to
Snowflake, be aware that exception handling behavior may differ. The TRY…CATCH pattern in SQL Server
is converted to Snowflake’s EXCEPTION blocks, but semantic differences may exist. Thorough testing
is recommended to ensure the converted code maintains the intended behavior.

### SQLWARNING and NOT FOUND Conditions[¶](#sqlwarning-and-not-found-conditions)

Applies to

- SQL Server
- Azure Synapse Analytics

CONTINUE HANDLERs for SQLWARNING and NOT FOUND conditions require special handling in Snowflake:

- **SQLWARNING**: Snowflake does not distinguish between warnings and errors in the same way as
  source systems.
- **NOT FOUND**: Typically used for cursor operations or SELECT INTO statements that return no rows.

#### Example[¶](#example)

##### Source Pattern[¶](#source-pattern)

```
DECLARE CONTINUE HANDLER FOR NOT FOUND
    SET done = TRUE;
```

##### Snowflake[¶](#snowflake)

```
-- Handled through conditional logic rather than exception handling
IF (SELECT COUNT(*) FROM table1) = 0 THEN
    done := TRUE;
END IF;
```

## Best Practices[¶](#best-practices)

When working with converted CONTINUE HANDLER code:

1. **Review Exception Handling**: Verify that the converted exception handling logic matches the
   intended behavior.
2. **Test Error Scenarios**: Thoroughly test error conditions to ensure the application behavior is
   correct.
3. **Consider Refactoring**: In some cases, refactoring the error handling logic may provide better
   performance and maintainability.
4. **Use Transactions**: Leverage Snowflake’s transaction support to ensure data consistency.

## Related Documentation[¶](#related-documentation)

- [Snowflake Exception Handling](https://docs.snowflake.com/en/developer-guide/snowflake-scripting/exceptions)
- [SQL Server TRY…CATCH](https://docs.microsoft.com/en-us/sql/t-sql/language-elements/try-catch-transact-sql)
- [TRY CATCH Translation Reference](transact-create-procedure-snow-script.html#try-catch)

## See Also[¶](#see-also)

- [CREATE PROCEDURE](transact-create-procedure)
- [CREATE PROCEDURE - Snowflake Scripting](transact-create-procedure-snow-script)
- [General Statements](transact-general-statements)
