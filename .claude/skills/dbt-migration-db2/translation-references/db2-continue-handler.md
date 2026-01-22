---
description:
  A CONTINUE handler allows the execution to continue after a condition is encountered. When a
  condition occurs and a continue handler is invoked, control is passed to the handler. When the
  handler comp
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/db2/db2-continue-handler
title: SnowConvert AI - IBM DB2 - CONTINUE HANDLER | Snowflake Documentation
---

## Description

> A CONTINUE handler allows the execution to continue after a condition is encountered. When a
> condition occurs and a continue handler is invoked, control is passed to the handler. When the
> handler completes, control returns to the statement following the statement that raised the
> condition.

In IBM DB2, the `DECLARE CONTINUE HANDLER` statement is used to define actions that should be taken
when specific SQL conditions or errors occur during procedure execution, while allowing the
procedure to continue running.

When migrating from DB2 to Snowflake, SnowConvert AI transforms CONTINUE HANDLER declarations into
equivalent Snowflake Scripting exception handling using EXCEPTION blocks with appropriate logic to
continue execution.

For more information about DB2 condition handlers, see
[IBM DB2 DECLARE HANDLER](https://www.ibm.com/docs/en/db2/11.5?topic=statements-declare-handler).

## Grammar Syntax

```sql
DECLARE CONTINUE HANDLER FOR condition_value [, ...]
  handler_action_statement;

-- Where condition_value can be:
-- SQLSTATE [VALUE] sqlstate_value
-- condition_name
-- SQLWARNING
-- SQLEXCEPTION
-- NOT FOUND
```

## Sample Source Patterns

### DECLARE CONTINUE HANDLER FOR SQLEXCEPTION

The most common use case is handling SQL exceptions while allowing the procedure to continue.

#### Input Code

##### IBM DB2

```sql
CREATE PROCEDURE error_handler_example()
LANGUAGE SQL
BEGIN
    DECLARE error_count INT DEFAULT 0;

    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
    BEGIN
        SET error_count = error_count + 1;
    END;

    -- These statements may cause errors
    INSERT INTO table1 VALUES (1/0);
    UPDATE table2 SET status = 'completed' WHERE id = -1;
    DELETE FROM table3 WHERE invalid_column = 'test';

    -- This will execute even if errors occurred above
    INSERT INTO error_summary VALUES (error_count);
END;
```

#### Output Code

##### Snowflake

```sql
CREATE OR REPLACE PROCEDURE error_handler_example()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "01/15/2025" }}'
AS
$$
    DECLARE
        error_count INT := 0;
    BEGIN
        -- Statements in procedure body
        INSERT INTO table1 VALUES (1/0);
        UPDATE table2 SET status = 'completed' WHERE id = -1;
        DELETE FROM table3 WHERE invalid_column = 'test';

        -- This will execute even if errors occurred above
        INSERT INTO error_summary VALUES (error_count);

        EXCEPTION
            WHEN OTHER CONTINUE THEN
                error_count := error_count + 1;
    END;
$$;
```

### DECLARE CONTINUE HANDLER FOR SQLSTATE

Handling specific SQLSTATE codes allows more granular control over error handling.

#### Input Code 2

##### IBM DB2 2

```sql
CREATE PROCEDURE sqlstate_handler_example()
LANGUAGE SQL
BEGIN
    DECLARE duplicate_key_count INT DEFAULT 0;

    -- Handle duplicate key errors (SQLSTATE 23505)
    DECLARE CONTINUE HANDLER FOR SQLSTATE '23505'
    BEGIN
        SET duplicate_key_count = duplicate_key_count + 1;
    END;

    -- Attempt to insert multiple records
    INSERT INTO users VALUES (1, 'John');
    INSERT INTO users VALUES (1, 'Jane');  -- Duplicate key
    INSERT INTO users VALUES (2, 'Bob');

    -- Log the results
    INSERT INTO process_log VALUES ('Duplicates found: ' || duplicate_key_count);
END;
```

#### Output Code 2

##### Snowflake 2

```sql
CREATE OR REPLACE PROCEDURE sqlstate_handler_example()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "01/15/2025" }}'
AS
$$
    DECLARE
        duplicate_key_count INT := 0;
    BEGIN
        -- Attempt to insert multiple records
        INSERT INTO users VALUES (1, 'John');
        INSERT INTO users VALUES (1, 'Jane');  -- Duplicate key
        INSERT INTO users VALUES (2, 'Bob');

        -- Log the results
        INSERT INTO process_log VALUES ('Duplicates found: ' || duplicate_key_count);

        EXCEPTION
            WHEN OTHER CONTINUE THEN
                CASE
                    WHEN (SQLSTATE = '23505') THEN
                        duplicate_key_count := duplicate_key_count + 1;
                END;
    END;
$$;
```

### DECLARE CONTINUE HANDLER FOR NOT FOUND

The NOT FOUND condition is commonly used with cursors and SELECT INTO statements.

#### Input Code 3

##### IBM DB2 3

```sql
CREATE PROCEDURE cursor_handler_example()
LANGUAGE SQL
BEGIN
    DECLARE v_id INT;
    DECLARE v_name VARCHAR(100);
    DECLARE v_done INT DEFAULT 0;

    DECLARE CONTINUE HANDLER FOR NOT FOUND
        SET v_done = 1;

    DECLARE cur1 CURSOR FOR
        SELECT id, name FROM employees WHERE department = 'Sales';

    OPEN cur1;

    fetch_loop:
    LOOP
        FETCH cur1 INTO v_id, v_name;

        IF v_done = 1 THEN
            LEAVE fetch_loop;
        END IF;

        INSERT INTO sales_employees VALUES (v_id, v_name);
    END LOOP fetch_loop;

    CLOSE cur1;
END;
```

#### Output Code 3

##### Snowflake 3

```sql
CREATE OR REPLACE PROCEDURE cursor_handler_example()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "01/15/2025" }}'
AS
$$
    DECLARE
        v_id INT;
        v_name VARCHAR(100);
        v_done INT := 0;
        cur1 CURSOR FOR
            SELECT id, name FROM employees WHERE department = 'Sales';
    BEGIN
        OPEN cur1;

        LOOP
            BEGIN
                FETCH cur1 INTO v_id, v_name;
            EXCEPTION
                WHEN NO_DATA_FOUND THEN
                    v_done := 1;
            END;

            IF (v_done = 1) THEN
                BREAK;
            END IF;

            INSERT INTO sales_employees VALUES (v_id, v_name);
        END LOOP;

        CLOSE cur1;
    END;
$$;
```

### DECLARE CONTINUE HANDLER FOR SQLWARNING

Handling warnings while allowing execution to continue.

#### Input Code 4

##### IBM DB2 4

```sql
CREATE PROCEDURE warning_handler_example()
LANGUAGE SQL
BEGIN
    DECLARE warning_count INT DEFAULT 0;

    DECLARE CONTINUE HANDLER FOR SQLWARNING
    BEGIN
        SET warning_count = warning_count + 1;
        INSERT INTO warning_log VALUES (CURRENT_TIMESTAMP, SQLSTATE, SQLCODE);
    END;

    -- Operations that might generate warnings
    UPDATE products SET price = price * 1.1 WHERE category = 'Electronics';
    DELETE FROM old_records WHERE record_date < CURRENT_DATE - 365 DAYS;

    INSERT INTO process_summary VALUES (warning_count);
END;
```

#### Output Code 4

##### Snowflake 4

```sql
CREATE OR REPLACE PROCEDURE warning_handler_example()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "01/15/2025" }}'
AS
$$
    DECLARE
        warning_count INT := 0;
    BEGIN
        -- Note: Snowflake doesn't distinguish warnings from errors in the same way
        -- Warning handling may need to be implemented through validation logic

        BEGIN
            UPDATE products SET price = price * 1.1 WHERE category = 'Electronics';
        EXCEPTION
            WHEN OTHER THEN
                warning_count := warning_count + 1;
                INSERT INTO warning_log
                VALUES (CURRENT_TIMESTAMP(), :SQLSTATE, :SQLCODE);
        END;

        BEGIN
            DELETE FROM old_records WHERE record_date < CURRENT_DATE - 365;
        EXCEPTION
            WHEN OTHER THEN
                warning_count := warning_count + 1;
                INSERT INTO warning_log
                VALUES (CURRENT_TIMESTAMP(), :SQLSTATE, :SQLCODE);
        END;

        INSERT INTO process_summary VALUES (warning_count);
    END;
$$;
```

## Known Issues

### CONTINUE HANDLER Behavior Differences

Applies to

- IBM DB2

#### Description 2

The exact behavior of DB2’s CONTINUE HANDLER cannot be fully replicated in Snowflake due to
architectural differences:

1. **Execution Continuation**: In DB2, a CONTINUE HANDLER allows execution to continue from the
   statement immediately following the one that raised the condition. In Snowflake, each statement
   must be wrapped in its own exception block to achieve similar behavior.
2. **Performance Impact**: Wrapping multiple statements in individual exception blocks can impact
   performance compared to a single handler declaration.
3. **Scope**: DB2 CONTINUE HANDLERs apply to all statements in their scope. In Snowflake, exception
   handling must be more explicit.

#### Related EWIs

1. [SSC-EWI-0114](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0114):
   MIXED CONTINUE AND EXIT EXCEPTION HANDLERS IN THE SAME BLOCK ARE NOT SUPPORTED BY SNOWFLAKE
   SCRIPTING
2. [SSC-FDM-0027](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0027):
   REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE (applies to FROM clause RETURN DATA UNTIL
   statements)

### SQLSTATE Mapping

Not all DB2 SQLSTATE codes have direct equivalents in Snowflake. SnowConvert AI performs best-effort
mapping:

<!-- prettier-ignore -->
|DB2 SQLSTATE|Condition|Snowflake Equivalent|
|---|---|---|
|02000|NOT FOUND|NO_DATA_FOUND|
|23xxx|Integrity Constraint Violation|STATEMENT_ERROR|
|42xxx|Syntax Error|STATEMENT_ERROR|
|01xxx|Warning|OTHER (requires validation)|

#### Input Code 5

##### IBM DB2 5

```sql
DECLARE CONTINUE HANDLER FOR SQLSTATE '42S02'
BEGIN
    -- Table doesn't exist
    CREATE TABLE missing_table (id INT, name VARCHAR(100));
END;
```

#### Output Code 5

##### Snowflake 5

```sql
BEGIN
    -- Operation that might fail
    SELECT * FROM missing_table;
EXCEPTION
    WHEN STATEMENT_ERROR THEN
        LET errcode := :SQLCODE;
        LET sqlerrmsg := :SQLERRM;
        IF (CONTAINS(sqlerrmsg, 'does not exist') OR CONTAINS(sqlerrmsg, 'Table')) THEN
            -- Table doesn't exist
            CREATE TABLE missing_table (id INT, name VARCHAR(100));
        ELSE
            RAISE;
        END IF;
END;
```

### Multiple CONTINUE Handlers

DB2 allows multiple CONTINUE HANDLERs with different priorities. In Snowflake, handler precedence
must be managed through explicit conditional logic using CASE statements.

#### Input Code 6

##### IBM DB2 6

```sql
CREATE PROCEDURE multiple_handlers()
BEGIN
    DECLARE CONTINUE HANDLER FOR SQLSTATE '23505'
        INSERT INTO log VALUES ('Duplicate key error');

    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
        INSERT INTO log VALUES ('General SQL exception');

    INSERT INTO table1 VALUES (1, 'test');
END;
```

#### Output Code 6

##### Snowflake 6

```sql
CREATE OR REPLACE PROCEDURE multiple_handlers()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "01/15/2025" }}'
AS
$$
    BEGIN
        INSERT INTO table1 VALUES (1, 'test');
        EXCEPTION
            WHEN OTHER CONTINUE THEN
                CASE
                    WHEN (SQLSTATE = '23505') THEN
                        INSERT INTO log VALUES ('Duplicate key error')
                    ELSE
                        INSERT INTO log VALUES ('General SQL exception')
                END;
    END;
$$;
```

### Mixed CONTINUE and EXIT Handlers

Applies to

- IBM DB2

#### Description 3

DB2 allows declaring both CONTINUE and EXIT handlers in the same procedure block. However, Snowflake
Scripting does not support mixing CONTINUE and EXIT handlers in the same EXCEPTION block. When this
pattern is encountered, SnowConvert AI generates separate EXCEPTION blocks with an EWI warning.

#### Input Code 7

##### IBM DB2 7

```sql
CREATE OR REPLACE PROCEDURE with_continueAndExit()
BEGIN
    DECLARE test_1 INTEGER DEFAULT 10;
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
        INSERT INTO error_test VALUES ('EXCEPTION');
    DECLARE EXIT HANDLER FOR SQLSTATE '20000'
        INSERT INTO error_test VALUES ('ERROR 2000');

    SET test_1 = 1 / 0;
    INSERT INTO error_test VALUES ('EXIT');
END;
```

#### Output Code 7

##### Snowflake 7

```sql
CREATE OR REPLACE PROCEDURE with_continueAndExit()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "01/15/2025" }}'
AS
$$
    DECLARE
        test_1 INTEGER DEFAULT 10;
    BEGIN
        test_1 := 1 / 0;
        INSERT INTO error_test VALUES ('EXIT');
        EXCEPTION
            WHEN OTHER CONTINUE THEN
                INSERT INTO error_test VALUES ('EXCEPTION')
        !!!RESOLVE EWI!!! /*** SSC-EWI-0114 - MIXED CONTINUE AND EXIT EXCEPTION HANDLERS IN THE SAME BLOCK ARE NOT SUPPORTED BY SNOWFLAKE SCRIPTING ***/!!!
        EXCEPTION
            WHEN OTHER EXIT THEN
                CASE
                    WHEN (SQLSTATE = '20000') THEN
                        INSERT INTO error_test VALUES ('ERROR 2000')
                END
    END;
$$;
```

#### Related EWIs 2

1. [SSC-EWI-0114](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0114):
   MIXED CONTINUE AND EXIT EXCEPTION HANDLERS IN THE SAME BLOCK ARE NOT SUPPORTED BY SNOWFLAKE
   SCRIPTING

## Best Practices

When working with converted CONTINUE HANDLER code:

1. **Validate Error Handling**: Thoroughly test all error scenarios to ensure the converted code
   behaves as expected.
2. **Review Performance**: Multiple exception blocks can impact performance. Consider refactoring
   when appropriate.
3. **Use Appropriate Exception Types**: Map DB2 conditions to the most specific Snowflake exception
   types available.
4. **Implement Logging**: Add comprehensive logging to track errors and ensure visibility into
   exception handling.
5. **Consider Transactions**: Use Snowflake’s transaction support to maintain data consistency when
   errors occur.
6. **Document Behavior Changes**: Document any differences in behavior between DB2 CONTINUE HANDLER
   and the Snowflake implementation.

## Related Documentation

- [IBM DB2 DECLARE HANDLER](https://www.ibm.com/docs/en/db2/11.5?topic=statements-declare-handler)
- [Snowflake Exception Handling](https://docs.snowflake.com/en/developer-guide/snowflake-scripting/exceptions)
- [Snowflake Stored Procedures](https://docs.snowflake.com/en/sql-reference/stored-procedures-overview)

## See Also

- [DB2 CREATE PROCEDURE](https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-procedure-sql)
- [DB2 FROM Clause](db2-from-clause)
- [DB2 SELECT Statement](db2-select-statement)
- [DB2 Data Types](db2-data-types)
