---
description:
  An EXIT handler terminates the current compound statement when the specified condition occurs.
  When a condition occurs and an exit handler is invoked, control is passed to the handler. When the
  handle
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/db2/db2-exit-handler
title: SnowConvert AI - IBM DB2 - EXIT HANDLER | Snowflake Documentation
---

## Description

> An EXIT handler terminates the current compound statement when the specified condition occurs.
> When a condition occurs and an exit handler is invoked, control is passed to the handler. When the
> handler completes, control returns to the caller of the compound statement.

In IBM DB2, the `DECLARE EXIT HANDLER` statement is used to define actions that should be taken when
specific SQL conditions or errors occur during procedure execution. Unlike CONTINUE handlers, EXIT
handlers terminate the execution of the current block and return control to the caller.

When migrating from DB2 to Snowflake, SnowConvert AI transforms EXIT HANDLER declarations into
equivalent Snowflake Scripting exception handling using EXCEPTION blocks with `WHEN OTHER EXIT THEN`
or specific exception types.

For more information about DB2 condition handlers, see
[IBM DB2 DECLARE HANDLER](https://www.ibm.com/docs/en/db2/11.5?topic=statements-declare-handler).

## Grammar Syntax

```sql
DECLARE EXIT HANDLER FOR condition_value [, ...]
  handler_action_statement;

-- Where condition_value can be:
-- SQLSTATE [VALUE] sqlstate_value
-- condition_name
-- SQLWARNING
-- SQLEXCEPTION
-- NOT FOUND
```

## Sample Source Patterns

### DECLARE EXIT HANDLER FOR SQLEXCEPTION

The most common use case is handling SQL exceptions and exiting the current block.

#### Input Code

##### IBM DB2

```sql
CREATE PROCEDURE error_exit_handler()
LANGUAGE SQL
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        INSERT INTO error_log VALUES (CURRENT_TIMESTAMP, 'Error occurred, exiting');
    END;

    -- These statements may cause errors
    INSERT INTO table1 VALUES (1/0);
    UPDATE table2 SET status = 'completed' WHERE id = -1;

    -- This will NOT execute if an error occurred above
    INSERT INTO success_log VALUES ('All operations completed');
END;
```

#### Output Code

##### Snowflake

```sql
CREATE OR REPLACE PROCEDURE error_exit_handler()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "01/15/2025" }}'
AS
$$
    BEGIN
        -- These statements may cause errors
        INSERT INTO table1 VALUES (1/0);
        UPDATE table2 SET status = 'completed' WHERE id = -1;

        -- This will NOT execute if an error occurred above
        INSERT INTO success_log VALUES ('All operations completed');

        EXCEPTION
            WHEN OTHER THEN
                BEGIN
                    INSERT INTO error_log VALUES (CURRENT_TIMESTAMP(), 'Error occurred, exiting');
                END;
    END;
$$;
```

### DECLARE EXIT HANDLER FOR SQLSTATE

Handling specific SQLSTATE codes with exit behavior.

#### Input Code 2

##### IBM DB2 2

```sql
CREATE PROCEDURE sqlstate_exit_handler()
LANGUAGE SQL
BEGIN
    DECLARE EXIT HANDLER FOR SQLSTATE '23505'
    BEGIN
        INSERT INTO error_log VALUES ('Duplicate key error, exiting procedure');
        ROLLBACK;
    END;

    -- Attempt to insert records
    INSERT INTO users VALUES (1, 'John');
    INSERT INTO users VALUES (1, 'Jane');  -- Duplicate key - will trigger handler
    INSERT INTO users VALUES (2, 'Bob');   -- Will NOT execute
END;
```

#### Output Code 2

##### Snowflake 2

```sql
CREATE OR REPLACE PROCEDURE sqlstate_exit_handler()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "01/15/2025" }}'
AS
$$
    BEGIN
        -- Attempt to insert records
        INSERT INTO users VALUES (1, 'John');
        INSERT INTO users VALUES (1, 'Jane');  -- Duplicate key - will trigger handler
        INSERT INTO users VALUES (2, 'Bob');   -- Will NOT execute

        EXCEPTION
            WHEN OTHER EXIT THEN
                CASE
                    WHEN (SQLSTATE = '23505') THEN
                        BEGIN
                            INSERT INTO error_log VALUES ('Duplicate key error, exiting procedure');
                            ROLLBACK;
                        END;
                END;
    END;
$$;
```

### DECLARE EXIT HANDLER FOR NOT FOUND

The NOT FOUND condition is commonly used with cursors and SELECT INTO statements.

#### Input Code 3

##### IBM DB2 3

```sql
CREATE PROCEDURE cursor_exit_handler()
LANGUAGE SQL
BEGIN
    DECLARE v_id INT;
    DECLARE v_name VARCHAR(100);

    DECLARE EXIT HANDLER FOR NOT FOUND
        INSERT INTO log_table VALUES ('No data found, exiting');

    -- This will trigger the handler if no rows found
    SELECT id, name INTO v_id, v_name
    FROM employees
    WHERE department = 'NonExistent';

    -- This will NOT execute if no rows were found
    INSERT INTO results VALUES (v_id, v_name);
END;
```

#### Output Code 3

##### Snowflake 3

```sql
CREATE OR REPLACE PROCEDURE cursor_exit_handler()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "01/15/2025" }}'
AS
$$
    DECLARE
        v_id INT;
        v_name VARCHAR(100);
    BEGIN
        -- This will trigger the handler if no rows found
        SELECT id, name INTO v_id, v_name
        FROM employees
        WHERE department = 'NonExistent';

        -- This will NOT execute if no rows were found
        INSERT INTO results VALUES (v_id, v_name);

        EXCEPTION
            WHEN NO_DATA_FOUND THEN
                INSERT INTO log_table VALUES ('No data found, exiting');
    END;
$$;
```

### Multiple EXIT Handlers

DB2 allows multiple EXIT HANDLERs with different priorities. In Snowflake, handler precedence must
be managed through explicit conditional logic using CASE statements.

#### Input Code 4

##### IBM DB2 4

```sql
CREATE PROCEDURE multiple_exit_handlers()
BEGIN
    DECLARE EXIT HANDLER FOR SQLSTATE '23505'
        INSERT INTO log VALUES ('Duplicate key error');

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
        INSERT INTO log VALUES ('General SQL exception');

    INSERT INTO table1 VALUES (1, 'test');
    INSERT INTO success_log VALUES ('Completed');
END;
```

#### Output Code 4

##### Snowflake 4

```sql
CREATE OR REPLACE PROCEDURE multiple_exit_handlers()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "01/15/2025" }}'
AS
$$
    BEGIN
        INSERT INTO table1 VALUES (1, 'test');
        INSERT INTO success_log VALUES ('Completed');

        EXCEPTION
            WHEN OTHER EXIT THEN
                CASE
                    WHEN (SQLSTATE = '23505') THEN
                        INSERT INTO log VALUES ('Duplicate key error')
                    ELSE
                        INSERT INTO log VALUES ('General SQL exception')
                END;
    END;
$$;
```

## Known Issues

### EXIT HANDLER Behavior

Applies to

- IBM DB2

#### Description 2

EXIT HANDLER in DB2 terminates the current compound statement and returns control to the caller. In
Snowflake, this is achieved using the EXCEPTION block, which automatically exits the current
BEGIN…END block when an exception occurs.

The main behavioral differences are:

1. **Execution Termination**: Both DB2 and Snowflake exit the current block when an EXIT handler is
   triggered.
2. **Statement-level Control**: In DB2, the EXIT handler activates at the statement that causes the
   error. In Snowflake, the entire remaining block is skipped.
3. **Nested Blocks**: Exit behavior in nested blocks is consistent between DB2 and Snowflake.

#### Related EWIs

1. [SSC-EWI-0114](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0114):
   MIXED CONTINUE AND EXIT EXCEPTION HANDLERS IN THE SAME BLOCK ARE NOT SUPPORTED BY SNOWFLAKE
   SCRIPTING

### Mixed CONTINUE and EXIT Handlers

Applies to

- IBM DB2

#### Description 3

DB2 allows declaring both CONTINUE and EXIT handlers in the same procedure block. However, Snowflake
Scripting does not support mixing CONTINUE and EXIT handlers in the same EXCEPTION block. When this
pattern is encountered, SnowConvert AI generates separate EXCEPTION blocks with an EWI warning.

See the [CONTINUE HANDLER documentation](db2-continue-handler.html#mixed-continue-and-exit-handlers)
for detailed examples of this limitation.

#### Input Code 5

##### IBM DB2 5

```sql
CREATE OR REPLACE PROCEDURE with_continueAndExit()
BEGIN
    DECLARE test_1 INTEGER DEFAULT 10;
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
        INSERT INTO error_test VALUES ('EXCEPTION');
    DECLARE EXIT HANDLER FOR SQLSTATE '20000'
        INSERT INTO error_test VALUES ('ERROR 2000');

    SET test_1 = 1 / 0;
    INSERT INTO error_test VALUES ('COMPLETED');
END;
```

#### Output Code 5

##### Snowflake 5

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
        INSERT INTO error_test VALUES ('COMPLETED');
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

### SQLSTATE Mapping

Not all DB2 SQLSTATE codes have direct equivalents in Snowflake. SnowConvert AI performs best-effort
mapping:

<!-- prettier-ignore -->
|DB2 SQLSTATE|Condition|Snowflake Equivalent|
|---|---|---|
|02000|NOT FOUND|NO_DATA_FOUND|
|23xxx|Integrity Constraint Violation|STATEMENT_ERROR|
|42xxx|Syntax Error|STATEMENT_ERROR|
|01xxx|Warning|OTHER|

## Best Practices

When working with converted EXIT HANDLER code:

1. **Understand Exit Behavior**: EXIT handlers terminate the current block. Ensure your application
   logic accounts for this behavior.
2. **Test Error Scenarios**: Thoroughly test all error conditions to verify that the EXIT handler
   behaves as expected.
3. **Use Transactions**: Leverage Snowflake’s transaction support to ensure data consistency when
   errors cause early exits.
4. **Logging**: Implement comprehensive logging in exception handlers to track when and why
   procedures exit early.
5. **Nested Blocks**: When using nested blocks, understand that EXIT handlers only exit the current
   block, not the entire procedure.
6. **Return Values**: Consider setting return values or output parameters in exception handlers to
   indicate the reason for exit.

## Related Documentation

- [IBM DB2 DECLARE HANDLER](https://www.ibm.com/docs/en/db2/11.5?topic=statements-declare-handler)
- [Snowflake Exception Handling](https://docs.snowflake.com/en/developer-guide/snowflake-scripting/exceptions)
- [Snowflake Stored Procedures](https://docs.snowflake.com/en/sql-reference/stored-procedures-overview)

## See Also

- [CONTINUE HANDLER](db2-continue-handler)
- [DB2 CREATE PROCEDURE](https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-procedure-sql)
- [DB2 SELECT Statement](db2-select-statement)
- [DB2 Data Types](db2-data-types)
