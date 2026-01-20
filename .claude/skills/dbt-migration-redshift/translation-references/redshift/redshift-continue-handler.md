---
description:
  Amazon Redshift, which uses PL/pgSQL for procedural logic, does not have a native DECLARE CONTINUE
  HANDLER statement in the same way as systems like DB2 or Teradata. In Redshift, exception handling
  is
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/redshift/redshift-continue-handler
title: SnowConvert AI - Redshift - CONTINUE HANDLER | Snowflake Documentation
---

## Description[¶](#description)

Amazon Redshift, which uses PL/pgSQL for procedural logic, does not have a native
`DECLARE CONTINUE HANDLER` statement in the same way as systems like DB2 or Teradata. In Redshift,
exception handling is managed through `EXCEPTION` blocks within procedures.

However, when migrating code from database systems that use CONTINUE HANDLERs (such as DB2,
Teradata, or other systems), SnowConvert AI transforms these constructs into equivalent Snowflake
Scripting exception handling mechanisms.

A CONTINUE HANDLER allows execution to continue after an error occurs, performing specific actions
when certain conditions are met. In Snowflake, this behavior is emulated using EXCEPTION blocks with
appropriate error handling logic.

For more information about Redshift exception handling, see
[Exception Handling in PL/pgSQL](https://docs.aws.amazon.com/redshift/latest/dg/c_PLpgSQL-statements.html#r_PLpgSQL-messages-errors).

## Grammar Syntax[¶](#grammar-syntax)

Redshift does not have native CONTINUE HANDLER syntax. However, when converting from other database
systems, the source pattern typically looks like:

```
-- Pattern from source systems (e.g., DB2, Teradata)
DECLARE CONTINUE HANDLER FOR condition_value
  handler_action_statement;
```

In Redshift, exception handling uses:

```
BEGIN
  -- statements
EXCEPTION
  WHEN condition THEN
    -- handler statements
END;
```

## Sample Source Patterns[¶](#sample-source-patterns)

### CONTINUE HANDLER Conversion to Snowflake[¶](#continue-handler-conversion-to-snowflake)

When migrating stored procedures from systems with CONTINUE HANDLER to Snowflake via Redshift,
SnowConvert AI transforms them into Snowflake-compatible exception handling.

#### Input Code:[¶](#input-code)

##### Source (DB2/Teradata Pattern)[¶](#source-db2-teradata-pattern)

```
-- Example pattern from source system
CREATE PROCEDURE example_handler_procedure()
BEGIN
    DECLARE CONTINUE HANDLER FOR SQLSTATE '02000'
    BEGIN
        -- Handler action: log the error
        INSERT INTO error_log VALUES (CURRENT_TIMESTAMP, 'No data found');
    END;

    -- Main procedure logic
    SELECT column1 INTO result_var FROM table1 WHERE id = 999;
    INSERT INTO results VALUES (result_var);
END;
```

#### Output Code:[¶](#output-code)

##### Snowflake Scripting[¶](#snowflake-scripting)

```
CREATE OR REPLACE PROCEDURE example_handler_procedure()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "01/15/2025" }}'
AS
$$
    DECLARE
        result_var VARCHAR;
    BEGIN
        BEGIN
            -- Main procedure logic
            SELECT column1 INTO result_var FROM table1 WHERE id = 999;
        EXCEPTION
            WHEN NO_DATA_FOUND THEN
                -- Handler action: log the error
                INSERT INTO error_log
                VALUES (CURRENT_TIMESTAMP(), 'No data found');
                -- Continue execution by not re-raising
        END;

        INSERT INTO results VALUES (result_var);
    END;
$$;
```

### CONTINUE HANDLER with SQLEXCEPTION[¶](#continue-handler-with-sqlexception)

#### Input Code:[¶](#id1)

##### Source (DB2/Teradata Pattern)[¶](#id2)

```
CREATE PROCEDURE multi_statement_handler()
BEGIN
    DECLARE error_count INT DEFAULT 0;

    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
    BEGIN
        SET error_count = error_count + 1;
    END;

    -- Multiple statements that might fail
    UPDATE table1 SET status = 'processed' WHERE id = -1;
    DELETE FROM table2 WHERE amount = 0/0;
    INSERT INTO table3 VALUES (1, 'Success');
END;
```

#### Output Code:[¶](#id3)

##### Snowflake Scripting[¶](#id4)

```
CREATE OR REPLACE PROCEDURE multi_statement_handler()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "01/15/2025" }}'
AS
$$
    DECLARE
        error_count INT := 0;
    BEGIN
        -- Multiple statements with individual exception handling
        BEGIN
            UPDATE table1 SET status = 'processed' WHERE id = -1;
        EXCEPTION
            WHEN OTHER THEN
                error_count := error_count + 1;
        END;

        BEGIN
            DELETE FROM table2 WHERE amount = 0/0;
        EXCEPTION
            WHEN OTHER THEN
                error_count := error_count + 1;
        END;

        INSERT INTO table3 VALUES (1, 'Success');
    END;
$$;
```

### CONTINUE HANDLER for NOT FOUND[¶](#continue-handler-for-not-found)

#### Input Code:[¶](#id5)

##### Source (DB2/Teradata Pattern)[¶](#id6)

```
CREATE PROCEDURE cursor_with_handler()
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE val INT;

    DECLARE CONTINUE HANDLER FOR NOT FOUND
        SET done = 1;

    DECLARE cur CURSOR FOR SELECT id FROM table1;

    OPEN cur;

    read_loop: LOOP
        FETCH cur INTO val;
        IF done = 1 THEN
            LEAVE read_loop;
        END IF;
        -- Process val
        INSERT INTO results VALUES (val);
    END LOOP;

    CLOSE cur;
END;
```

#### Output Code:[¶](#id7)

##### Snowflake Scripting[¶](#id8)

```
CREATE OR REPLACE PROCEDURE cursor_with_handler()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "01/15/2025" }}'
AS
$$
    DECLARE
        done INT := 0;
        val INT;
        cur CURSOR FOR SELECT id FROM table1;
    BEGIN
        OPEN cur;

        LOOP
            BEGIN
                FETCH cur INTO val;
            EXCEPTION
                WHEN NO_DATA_FOUND THEN
                    done := 1;
            END;

            IF (done = 1) THEN
                BREAK;
            END IF;

            -- Process val
            INSERT INTO results VALUES (val);
        END LOOP;

        CLOSE cur;
    END;
$$;
```

## Known Issues[¶](#known-issues)

### Limited CONTINUE HANDLER Emulation[¶](#limited-continue-handler-emulation)

The conversion from CONTINUE HANDLER to Snowflake exception handling has some limitations:

1. **Execution Flow**: True CONTINUE HANDLER behavior (continuing from the exact point of error)
   cannot be fully replicated in Snowflake.
2. **Performance**: Wrapping individual statements in exception blocks can impact performance.
3. **Granularity**: Statement-level exception handling may be required to properly emulate CONTINUE
   HANDLER behavior.

### SQLSTATE Mapping[¶](#sqlstate-mapping)

Not all SQLSTATE codes from source systems map directly to Snowflake exception types. SnowConvert AI
performs best-effort mapping:

- `SQLSTATE '02000'` (NO DATA) → `NO_DATA_FOUND`
- `SQLSTATE '23xxx'` (Integrity Constraint Violation) → `STATEMENT_ERROR`
- Generic SQLEXCEPTION → `OTHER`

#### Known Issues[¶](#id9)

When migrating CONTINUE HANDLER patterns from other systems to Redshift and then to Snowflake, be
aware that exception handling behavior may differ between systems. Thorough testing is recommended
to ensure the converted code maintains the intended behavior.

### SQLWARNING Handling[¶](#sqlwarning-handling)

Source systems that use CONTINUE HANDLER for SQLWARNING conditions present special challenges:

- Snowflake does not distinguish between warnings and errors in the same way
- Warnings in source systems may be errors in Snowflake
- Manual review of warning handling logic is recommended

#### Example[¶](#example)

##### Source Pattern[¶](#source-pattern)

```
DECLARE CONTINUE HANDLER FOR SQLWARNING
BEGIN
    INSERT INTO warning_log VALUES (SQLCODE, 'Warning occurred');
END;
```

##### Snowflake[¶](#snowflake)

```
-- Warning handling may need to be implemented through validation logic
BEGIN
    -- Perform validation before operation
    IF EXISTS (SELECT 1 FROM table1 WHERE condition) THEN
        INSERT INTO warning_log VALUES (0, 'Warning occurred');
    END IF;
EXCEPTION
    WHEN OTHER THEN
        -- Handle actual errors
        INSERT INTO error_log VALUES (:SQLCODE, :SQLERRM);
END;
```

## Best Practices[¶](#best-practices)

When working with converted CONTINUE HANDLER code in Snowflake:

1. **Test Thoroughly**: Verify that error handling behavior matches the original system’s behavior.
2. **Review Performance**: Multiple exception blocks can impact performance; consider refactoring
   where appropriate.
3. **Validate Error Conditions**: Ensure that all error conditions from the source system are
   properly handled.
4. **Use Transactions**: Leverage Snowflake’s transaction support for data consistency.
5. **Monitor Execution**: Use Snowflake’s logging capabilities to track exception handling.

## Related Documentation[¶](#related-documentation)

- [Snowflake Exception Handling](https://docs.snowflake.com/en/developer-guide/snowflake-scripting/exceptions)
- [Redshift Exception Handling](https://docs.aws.amazon.com/redshift/latest/dg/c_PLpgSQL-statements.html#r_PLpgSQL-messages-errors)
- [CREATE PROCEDURE](rs-sql-statements-create-procedure)

## See Also[¶](#see-also)

- [EXCEPTION](rs-sql-statements-create-procedure.html#exception)
- [RAISE](rs-sql-statements-create-procedure.html#raise)
- [DECLARE](rs-sql-statements-create-procedure.html#declare)
