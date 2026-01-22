---
auto_generated: true
description: In a Snowflake Scripting block, you can raise an exception if an error
  occurs. You can also handle exceptions that occur in your Snowflake Scripting code.
last_scraped: '2026-01-14T16:55:45.235240+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/developer-guide/snowflake-scripting/exceptions
title: Handling exceptions | Snowflake Documentation
---

1. [Overview](../../developer.md)
2. Builders
3. [Snowflake DevOps](../builders/devops.md)
4. [Observability](../builders/observability.md)
5. Snowpark Library
6. [Snowpark API](../snowpark/index.md)
7. [Spark workloads on Snowflake](../snowpark-connect/snowpark-connect-overview.md)
8. Machine Learning
9. [Snowflake ML](../snowflake-ml/overview.md)
10. Snowpark Code Execution Environments
11. [Snowpark Container Services](../snowpark-container-services/overview.md)
12. [Functions and procedures](../extensibility.md)
13. [Logging, Tracing, and Metrics](../logging-tracing/logging-tracing-overview.md)
14. Snowflake APIs
15. [Snowflake Python APIs](../snowflake-python-api/snowflake-python-overview.md)
16. [Snowflake REST APIs](../snowflake-rest-api/snowflake-rest-api.md)
17. [SQL API](../sql-api/index.md)
18. Apps
19. Streamlit in Snowflake

    - [About Streamlit in Snowflake](../streamlit/about-streamlit.md)
    - Getting started

      - [Deploy a sample app](../streamlit/getting-started/overview.md)
      - [Create and deploy Streamlit apps using Snowsight](../streamlit/getting-started/create-streamlit-ui.md)
      - [Create and deploy Streamlit apps using SQL](../streamlit/getting-started/create-streamlit-sql.md)
      - [Create and deploy Streamlit apps using Snowflake CLI](../streamlit/getting-started/create-streamlit-snowflake-cli.md)
    - Streamlit object management

      - [Billing considerations](../streamlit/object-management/billing.md)
      - [Security considerations](../streamlit/object-management/security.md)
      - [Privilege requirements](../streamlit/object-management/privileges.md)
      - [Understanding owner's rights](../streamlit/object-management/owners-rights.md)
      - [PrivateLink](../streamlit/object-management/privatelink.md)
      - [Logging and tracing](../streamlit/object-management/logging-tracing.md)
    - App development

      - [Runtime environments](../streamlit/app-development/runtime-environments.md)
      - [Dependency management](../streamlit/app-development/dependency-management.md)
      - [File organization](../streamlit/app-development/file-organization.md)
      - [Secrets and configuration](../streamlit/app-development/secrets-and-configuration.md)
      - [Editing your app](../streamlit/app-development/editing-your-app.md)
    - Migrations and upgrades

      - [Identify your app type](../streamlit/migrations-and-upgrades/overview.md)
      - [Migrate to a container runtime](../streamlit/migrations-and-upgrades/runtime-migration.md)
      - [Migrate from ROOT\_LOCATION](../streamlit/migrations-and-upgrades/root-location.md)
    - Features

      - [Git integration](../streamlit/features/git-integration.md)
      - [External access](../streamlit/features/external-access.md)
      - [Row access policies](../streamlit/features/row-access.md)
      - [Sleep timer](../streamlit/features/sleep-timer.md)
    - [Limitations and library changes](../streamlit/limitations.md)
    - [Troubleshooting Streamlit in Snowflake](../streamlit/troubleshooting.md)
    - [Release notes](../../release-notes/streamlit-in-snowflake.md)
    - [Streamlit open-source library documentation](https://docs.streamlit.io/)
20. [Snowflake Native App Framework](../native-apps/native-apps-about.md)
21. [Snowflake Declarative Sharing](../declarative-sharing/about.md)
22. [Snowflake Native SDK for Connectors](../native-apps/connector-sdk/about-connector-sdk.md)
23. External Integration
24. [External Functions](../../sql-reference/external-functions.md)
25. [Kafka and Spark Connectors](../../user-guide/connectors.md)
26. Snowflake Scripting
27. [Snowflake Scripting Developer Guide](index.md)

    * [Blocks](blocks.md)
    * [Variables](variables.md)
    * [Returning a value](return.md)
    * [Conditional logic](branch.md)
    * [Loops](loops.md)
    * [Cursors](cursors.md)
    * [RESULTSETs](resultsets.md)
    * [Asynchronous child jobs](asynchronous-child-jobs.md)
    * [Exceptions](exceptions.md)
    * [Affected rows](dml-status.md)
    * [Getting a query ID](query-id.md)
    * [Examples for common use cases of Snowflake Scripting](use-cases.md)
    * [Using Snowflake Scripting in Snowflake CLI, SnowSQL, or the Python Connector](running-examples.md)
28. Tools
29. [Snowflake CLI](../snowflake-cli/index.md)
30. [Git](../git/git-overview.md)
31. Drivers
32. [Overview](../drivers.md)
33. [Considerations when drivers reuse sessions](../driver-connections.md)
34. [Scala versions](../scala-version-differences.md)
35. Reference
36. [API Reference](../../api-reference.md)

[Developer](../../developer.md)[Snowflake Scripting Developer Guide](index.md)Exceptions

# Handling exceptions[¶](#handling-exceptions "Link to this heading")

In a Snowflake Scripting block, you can raise an exception if an error occurs. You can also handle exceptions that occur in your
Snowflake Scripting code.

## Introduction to handling exceptions in Snowflake Scripting[¶](#introduction-to-handling-exceptions-in-snowflake-scripting "Link to this heading")

Snowflake Scripting raises an exception if an error occurs while executing a statement. For example, if a statement
attempts to drop a table that doesn’t exist, Snowflake Scripting raises an exception.

In a Snowflake Scripting block, you can write exception handlers that catch specific types of exceptions declared in that block
and in blocks nested inside that block. In addition, for errors that can occur in your code, you can define your own exceptions
that you can raise when errors occur.

After the statements in the handler are run, you can choose to exit the block or continue running the statements in the block.
For more information, see [Handling an exception in Snowflake Scripting](#label-snowscript-exception-handling).

When an exception is raised in a Snowflake Scripting block, either by your code or by a statement that fails to execute,
Snowflake Scripting attempts to find a handler for that exception:

* If the block in which the exception occurred has a handler for that exception, then execution resumes at the
  beginning of that exception handler.
* If the block doesn’t have its own exception handler, then the exception can be caught by the enclosing block.

  If the exception occurs more than one layer deep, then the exception is sent upward one layer at a time until either:

  + A layer with an appropriate exception handler handles the exception.
  + The outermost layer is reached, in which case an error occurs.
* If there is no handler for the exception in the current block or in any enclosing blocks, execution of the block stops, and the
  client that submits the block for execution (for example, Snowsight, SnowSQL, and so on) reports this as a Snowflake error.

An exception handler can contain its own exception handler in case an exception occurs while handling another exception.

## Declaring an exception in Snowflake Scripting[¶](#declaring-an-exception-in-snowflake-scripting "Link to this heading")

You can declare your own exception in the [DECLARE](../../sql-reference/snowflake-scripting/declare) section of the block. Use
the syntax described in [Exception declaration syntax](../../sql-reference/snowflake-scripting/declare.html#label-snowscript-declare-syntax-exception). For example:

```
DECLARE
  my_exception EXCEPTION (-20002, 'Raised MY_EXCEPTION.');
```

Copy

## Raising a declared exception in Snowflake Scripting[¶](#raising-a-declared-exception-in-snowflake-scripting "Link to this heading")

To raise an exception, execute the [RAISE](../../sql-reference/snowflake-scripting/raise) command. For example:

```
DECLARE
  my_exception EXCEPTION (-20002, 'Raised MY_EXCEPTION.');
BEGIN
  LET counter := 0;
  LET should_raise_exception := true;
  IF (should_raise_exception) THEN
    RAISE my_exception;
  END IF;
  counter := counter + 1;
  RETURN counter;
END;
```

Copy

Note: If you use [Snowflake CLI](../snowflake-cli/index), [SnowSQL](../../user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](../python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](running-examples)):

```
EXECUTE IMMEDIATE $$
DECLARE
  my_exception EXCEPTION (-20002, 'Raised MY_EXCEPTION.');
BEGIN
  LET counter := 0;
  LET should_raise_exception := true;
  IF (should_raise_exception) THEN
    RAISE my_exception;
  END IF;
  counter := counter + 1;
  RETURN counter;
END;
$$
;
```

Copy

If there is no handler, execution stops at the point when the exception is raised. In the example, `counter` is never
incremented and isn’t returned.

The client that submits this block for execution — for example, Snowsight — reports an error and indicates that the exception
was not caught:

```
-20002 (P0001): Uncaught exception of type 'MY_EXCEPTION' on line 8 at position 4 : Raised MY_EXCEPTION.
```

Copy

If you want to add code to handle any exceptions that you raise (as well as exceptions raised when statements fail to execute),
you can write exception handlers. See [Handling an exception in Snowflake Scripting](#label-snowscript-exception-handling).

Note

In an exception handler, if you need to raise the same exception again, see
[Raising the same exception again in an exception handler in Snowflake Scripting](#label-snowscript-exception-raising-same-handled).

## Handling an exception in Snowflake Scripting[¶](#handling-an-exception-in-snowflake-scripting "Link to this heading")

You can explicitly handle an exception by catching it with an [EXCEPTION](../../sql-reference/snowflake-scripting/exception)
clause, or you can allow the block to pass the exception on to the enclosing block.

Within the [EXCEPTION](../../sql-reference/snowflake-scripting/exception) clause, use a WHEN clause to handle an
exception by name. You can handle exceptions that you declare as well as built-in exceptions. Currently, Snowflake provides the
following built-in exceptions:

* STATEMENT\_ERROR: This exception indicates an error while executing a statement. For example, if you attempt to drop a table
  that does not exist, this exception is raised.
* EXPRESSION\_ERROR: This exception indicates an error related to an expression. For example, if you create an expression that
  evaluates to a VARCHAR, and you attempt to assign the value of the expression to a FLOAT, this error is raised.

Each WHEN clause in an exception block can be one of the following types:

* EXIT - The block runs the statements in the handler and then exits the current block. If the block runs an
  exception of this type, and the block contains statements after the statement that caused the error, those statements
  aren’t run.

  If the block is an inner block, and the exception handler doesn’t contain a RETURN statement, then
  execution exits the inner block and continues with the code in the outer block.

  EXIT is the default.
* CONTINUE - The block runs the statements in the exception block and continues with the statement
  immediately following the one that caused the error.

  A CONTINUE handler can catch and handle exceptions without ending the statement block that raised the exception.
  With the default EXIT handler, when an error occurs in a block, the flow is interrupted and the error is
  returned to the caller. However, you can use a CONTINUE handler when the error condition isn’t severe enough
  to warrant interrupting the flow.

An EXCEPTION clause can have WHEN clauses of both types — EXIT and CONTINUE.

When an exception occurs, you can get information about the exception by reading the following three built-in variables:

* SQLCODE: This is a 5-digit signed integer. For user-defined exceptions, this is the `exception_number` shown in
  the [syntax for declaring an exception](#label-syntax-for-declaring-an-exception).
* SQLERRM: This is an error message. For user-defined exceptions, this is the `exception_message` shown in
  the [syntax for declaring an exception](#label-syntax-for-declaring-an-exception).
* SQLSTATE: This is a 5-character code modeled on the ANSI SQL standard [SQLSTATE](https://en.wikipedia.org/wiki/SQLSTATE).
  Snowflake uses additional values beyond those in the ANSI SQL standard.

When you use a WHEN clause of the CONTINUE type, these built-in variables reflect the error that caused the exception
in the WHEN clause. After the statements in the WHEN clause complete, and statement execution continues in the block,
the values of these variables return the values they had before the exception was raised.

To handle all other exceptions that aren’t built-in or declared, use a WHEN OTHER THEN clause. The WHEN OTHER THEN
clause can be of type EXIT or CONTINUE.

For example, assume that you have the following error log table to track your exceptions:

```
CREATE OR REPLACE TABLE test_error_log(
  error_type VARCHAR,
  error_code VARCHAR,
  error_message VARCHAR,
  error_state VARCHAR,
  error_timestamp TIMESTAMP);
```

Copy

The following anonymous block inserts information about the exceptions into the table
and returns information about them to the user:

Tip

The example defines an exception in the DECLARE section and then handles that exception. For an example
that handles a STATEMENT\_ERROR exception, remove the comments (`--`) from this line:

```
-- SELECT 1/0;
```

Copy

For an example that handles other errors, remove the comments from this line:

```
-- LET var := 1/0;
```

Copy

```
DECLARE
  my_exception EXCEPTION (-20002, 'Raised MY_EXCEPTION.');
BEGIN
  -- SELECT 1/0;
  -- LET var := 1/0;
  LET counter := 0;
  LET should_raise_exception := true;
  IF (should_raise_exception) THEN
    RAISE my_exception;
  END IF;
  counter := counter + 1;
  RETURN 'My counter value: ' || counter;
EXCEPTION
  WHEN STATEMENT_ERROR THEN
    INSERT INTO test_error_log VALUES(
      'STATEMENT_ERROR', :sqlcode, :sqlerrm, :sqlstate, CURRENT_TIMESTAMP());
    RETURN OBJECT_CONSTRUCT('Error type', 'STATEMENT_ERROR',
                            'SQLCODE', sqlcode,
                            'SQLERRM', sqlerrm,
                            'SQLSTATE', sqlstate);
  WHEN my_exception THEN
    INSERT INTO test_error_log VALUES(
      'MY_EXCEPTION', :sqlcode, :sqlerrm, :sqlstate, CURRENT_TIMESTAMP());
    RETURN OBJECT_CONSTRUCT('Error type', 'MY_EXCEPTION',
                            'SQLCODE', sqlcode,
                            'SQLERRM', sqlerrm,
                            'SQLSTATE', sqlstate);
  WHEN OTHER THEN
    INSERT INTO test_error_log VALUES(
      'OTHER', :sqlcode, :sqlerrm, :sqlstate, CURRENT_TIMESTAMP());
    RETURN OBJECT_CONSTRUCT('Error type', 'Other error',
                            'SQLCODE', sqlcode,
                            'SQLERRM', sqlerrm,
                            'SQLSTATE', sqlstate);
END;
```

Copy

Note: If you use [Snowflake CLI](../snowflake-cli/index), [SnowSQL](../../user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](../python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](running-examples)):

```
EXECUTE IMMEDIATE $$
DECLARE
  my_exception EXCEPTION (-20002, 'Raised MY_EXCEPTION.');
BEGIN
  -- SELECT 1/0;
  -- LET var := 1/0;
  LET counter := 0;
  LET should_raise_exception := true;
  IF (should_raise_exception) THEN
    RAISE my_exception;
  END IF;
  counter := counter + 1;
  RETURN 'My counter value: ' || counter;
EXCEPTION
  WHEN STATEMENT_ERROR THEN
    INSERT INTO test_error_log VALUES(
      'STATEMENT_ERROR', :sqlcode, :sqlerrm, :sqlstate, CURRENT_TIMESTAMP());
    RETURN OBJECT_CONSTRUCT('Error type', 'STATEMENT_ERROR',
                            'SQLCODE', sqlcode,
                            'SQLERRM', sqlerrm,
                            'SQLSTATE', sqlstate);
  WHEN my_exception THEN
    INSERT INTO test_error_log VALUES(
      'MY_EXCEPTION', :sqlcode, :sqlerrm, :sqlstate, CURRENT_TIMESTAMP());
    RETURN OBJECT_CONSTRUCT('Error type', 'MY_EXCEPTION',
                            'SQLCODE', sqlcode,
                            'SQLERRM', sqlerrm,
                            'SQLSTATE', sqlstate);
  WHEN OTHER THEN
    INSERT INTO test_error_log VALUES(
      'OTHER', :sqlcode, :sqlerrm, :sqlstate, CURRENT_TIMESTAMP());
    RETURN OBJECT_CONSTRUCT('Error type', 'Other error',
                            'SQLCODE', sqlcode,
                            'SQLERRM', sqlerrm,
                            'SQLSTATE', sqlstate);
END;
$$
;
```

Copy

For the returned value, this example handles each type of exception by calling
[OBJECT\_CONSTRUCT](../../sql-reference/functions/object_construct) to construct and return an object that contains
the details about the exception. The example produces the following output:

```
+--------------------------------------+
| anonymous block                      |
|--------------------------------------|
| {                                    |
|   "Error type": "MY_EXCEPTION",      |
|   "SQLCODE": -20002,                 |
|   "SQLERRM": "Raised MY_EXCEPTION.", |
|   "SQLSTATE": "P0001"                |
| }                                    |
+--------------------------------------+
```

You can query the `test_error_log` table to confirm that the error was logged:

```
SELECT * FROM test_error_log;
```

Copy

```
+--------------+------------+----------------------+-------------+-------------------------+
| ERROR_TYPE   | ERROR_CODE | ERROR_MESSAGE        | ERROR_STATE | ERROR_TIMESTAMP         |
|--------------+------------+----------------------+-------------+-------------------------|
| MY_EXCEPTION | -20002     | Raised MY_EXCEPTION. | P0001       | 2025-09-05 12:15:00.068 |
+--------------+------------+----------------------+-------------+-------------------------+
```

The previous example used WHEN clauses of the default type (EXIT). If one of the WHEN clauses catches
an exception, it runs the statements in the WHEN clause and then exits. Therefore, the following
code isn’t run:

```
counter := counter + 1;
RETURN 'My counter value: ' || counter;
```

Copy

If you want to handle an exception and then continue running the code in the block, specify WHEN clauses
of the CONTINUE type. The following example is the same as the previous example, but it specifies WHEN
clauses of the CONTINUE type and removes the RETURN statement from each WHEN clause:

```
DECLARE
  my_exception EXCEPTION (-20002, 'Raised MY_EXCEPTION.');
BEGIN
  -- SELECT 1/0;
  -- LET var := 1/0;
  LET counter := 0;
  LET should_raise_exception := true;
  IF (should_raise_exception) THEN
    RAISE my_exception;
  END IF;
  counter := counter + 1;
  RETURN 'My counter value: ' || counter;
EXCEPTION
  WHEN STATEMENT_ERROR CONTINUE THEN
    INSERT INTO test_error_log VALUES(
      'STATEMENT_ERROR', :sqlcode, :sqlerrm, :sqlstate, CURRENT_TIMESTAMP());
  WHEN my_exception CONTINUE THEN
    INSERT INTO test_error_log VALUES(
      'MY_EXCEPTION', :sqlcode, :sqlerrm, :sqlstate, CURRENT_TIMESTAMP());
  WHEN OTHER CONTINUE THEN
    INSERT INTO test_error_log VALUES(
      'OTHER', :sqlcode, :sqlerrm, :sqlstate, CURRENT_TIMESTAMP());
END;
```

Copy

Note: If you use [Snowflake CLI](../snowflake-cli/index), [SnowSQL](../../user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](../python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](running-examples)):

```
EXECUTE IMMEDIATE $$
DECLARE
  my_exception EXCEPTION (-20002, 'Raised MY_EXCEPTION.');
BEGIN
  -- SELECT 1/0;
  -- LET var := 1/0;
  LET counter := 0;
  LET should_raise_exception := true;
  IF (should_raise_exception) THEN
    RAISE my_exception;
  END IF;
  counter := counter + 1;
  RETURN 'My counter value: ' || counter;
EXCEPTION
  WHEN STATEMENT_ERROR CONTINUE THEN
    INSERT INTO test_error_log VALUES(
      'STATEMENT_ERROR', :sqlcode, :sqlerrm, :sqlstate, CURRENT_TIMESTAMP());
  WHEN my_exception CONTINUE THEN
    INSERT INTO test_error_log VALUES(
      'MY_EXCEPTION', :sqlcode, :sqlerrm, :sqlstate, CURRENT_TIMESTAMP());
  WHEN OTHER CONTINUE THEN
    INSERT INTO test_error_log VALUES(
      'OTHER', :sqlcode, :sqlerrm, :sqlstate, CURRENT_TIMESTAMP());
END;
$$
;
```

Copy

```
+---------------------+
| anonymous block     |
|---------------------|
| My counter value: 1 |
+---------------------+
```

The output shows that the example continued running the following code after the exception was raised:

```
counter := counter + 1;
RETURN counter;
```

Copy

For more information about CONTINUE handlers, see [EXCEPTION (Snowflake Scripting)](../../sql-reference/snowflake-scripting/exception).

In rare cases, you might want to explicitly handle an exception by doing nothing. This enables you to continue, rather than terminate,
when the exception occurs. For more information, see the [NULL](../../sql-reference/snowflake-scripting/null) command.

Note

If you need to raise the same exception again, see [Raising the same exception again in an exception handler in Snowflake Scripting](#label-snowscript-exception-raising-same-handled).

If you don’t set up a handler for an exception, the client that submits the block for execution; for example,
Snowsight reports an error as explained in [Raising a declared exception in Snowflake Scripting](#label-snowscript-exception-raising).

```
-20002 (P0001): Uncaught exception of type 'MY_EXCEPTION' on line 8 at position 4 : Raised MY_EXCEPTION.
```

Copy

## Raising the same exception again in an exception handler in Snowflake Scripting[¶](#raising-the-same-exception-again-in-an-exception-handler-in-snowflake-scripting "Link to this heading")

In some cases, you might need to raise the same exception that you caught in your exception handler. In these cases, execute the
RAISE command without specifying any arguments.

For example, suppose that during exception handling, you need to capture some details about the exception before raising the same
exception again. After capturing the details, execute the RAISE command:

```
BEGIN
  SELECT * FROM non_existent_table;
EXCEPTION
  WHEN OTHER THEN
    LET LINE := SQLCODE || ': ' || SQLERRM;
    INSERT INTO myexceptions VALUES (:line);
    RAISE; -- Raise the same exception that you are handling.
END;
```

Copy

Note: If you use [Snowflake CLI](../snowflake-cli/index), [SnowSQL](../../user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](../python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](running-examples)):

```
EXECUTE IMMEDIATE $$
BEGIN
  SELECT * FROM non_existent_table;
EXCEPTION
  WHEN OTHER THEN
    LET LINE := SQLCODE || ': ' || SQLERRM;
    INSERT INTO myexceptions VALUES (:line);
    RAISE; -- Raise the same exception that you are handling.
END;
$$;
```

Copy

## Passing variables to an exception handler in Snowflake Scripting[¶](#passing-variables-to-an-exception-handler-in-snowflake-scripting "Link to this heading")

You can pass variables to an exception handler. The exception handler can execute code based
on the value of the variable, and the variable value can be returned in error messages.

For a variable to be passed to a handler in the EXCEPTION section, the variable must be declared
in the [DECLARE](../../sql-reference/snowflake-scripting/declare) section. If a variable is declared
in the [BEGIN … END](../../sql-reference/snowflake-scripting/begin) section of the block, it can’t
be accessed in the EXCEPTION section.

In addition, if you are writing a Snowflake Scripting stored procedure that accepts arguments, you can use those
arguments in an exception handler.

For example, the following anonymous block passes the value of the `counter_val` variable to
the exception handler:

```
DECLARE
  counter_val INTEGER DEFAULT 0;
  my_exception EXCEPTION (-20002, 'My exception text');
BEGIN
  WHILE (counter_val < 12) DO
    counter_val := counter_val + 1;
    IF (counter_val > 10) THEN
      RAISE my_exception;
    END IF;
  END WHILE;
  RETURN counter_val;
EXCEPTION
  WHEN my_exception THEN
    RETURN 'Error ' || sqlcode || ': Counter value ' || counter_val || ' exceeds the limit of 10.';
END;
```

Copy

Note: If you use [Snowflake CLI](../snowflake-cli/index), [SnowSQL](../../user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](../python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](running-examples)):

```
EXECUTE IMMEDIATE $$
DECLARE
  counter_val INTEGER DEFAULT 0;
  my_exception EXCEPTION (-20002, 'My exception text');
BEGIN
  WHILE (counter_val < 12) DO
    counter_val := counter_val + 1;
    IF (counter_val > 10) THEN
      RAISE my_exception;
    END IF;
  END WHILE;
  RETURN counter_val;
EXCEPTION
  WHEN my_exception THEN
    RETURN 'Error ' || sqlcode || ': Counter value ' || counter_val || ' exceeds the limit of 10.';
END;
$$
;
```

Copy

The block returns the following error message:

```
+---------------------------------------------------------+
| anonymous block                                         |
|---------------------------------------------------------|
| Error -20002: Counter value 11 exceeds the limit of 10. |
+---------------------------------------------------------+
```

The following is an example of a Snowflake Scripting stored procedure that passes in an argument. The example demonstrates
how you can use the argument in an exception handler:

```
CREATE OR REPLACE PROCEDURE exception_test_vars(amount INT)
  RETURNS TEXT
  LANGUAGE SQL
AS
DECLARE
  my_exception_1 EXCEPTION (-20002, 'Value too low');
  my_exception_2 EXCEPTION (-20003, 'Value too high');
BEGIN
  CREATE OR REPLACE TABLE test_order_insert(units INT);
  IF (amount < 1) THEN
    RAISE my_exception_1;
  ELSEIF (amount > 10) THEN
    RAISE my_exception_2;
  ELSE
    INSERT INTO test_order_insert VALUES (:amount);
  END IF;
  RETURN 'Order inserted successfully.';
EXCEPTION
  WHEN my_exception_1 THEN
    RETURN 'Error ' || sqlcode || ': Submitted amount ' || amount || ' is too low (1 or greater required).';
  WHEN my_exception_2 THEN
    RETURN 'Error ' || sqlcode || ': Submitted amount ' || amount || ' is too high (exceeds limit of 10).';
END;
```

Copy

Note: If you use [Snowflake CLI](../snowflake-cli/index), [SnowSQL](../../user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](../python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](running-examples)):

```
CREATE OR REPLACE PROCEDURE exception_test_vars(amount INT)
  RETURNS TEXT
  LANGUAGE SQL
AS
$$
DECLARE
  my_exception_1 EXCEPTION (-20002, 'Value too low');
  my_exception_2 EXCEPTION (-20003, 'Value too high');
BEGIN
  CREATE OR REPLACE TABLE test_order_insert(units INT);
  IF (amount < 1) THEN
    RAISE my_exception_1;
  ELSEIF (amount > 10) THEN
    RAISE my_exception_2;
  ELSE
    INSERT INTO test_order_insert VALUES (:amount);
  END IF;
  RETURN 'Order inserted successfully.';
EXCEPTION
  WHEN my_exception_1 THEN
    RETURN 'Error ' || sqlcode || ': Submitted amount ' || amount || ' is too low (1 or greater required).';
  WHEN my_exception_2 THEN
    RETURN 'Error ' || sqlcode || ': Submitted amount ' || amount || ' is too high (exceeds limit of 10).';
END;
$$
;
```

Copy

The following calls to the stored procedure show the expected output:

```
CALL exception_test_vars(7);
```

Copy

```
+------------------------------+
| EXCEPTION_TEST_VARS          |
|------------------------------|
| Order inserted successfully. |
+------------------------------+
```

```
CALL exception_test_vars(-3);
```

Copy

```
+-----------------------------------------------------------------------+
| EXCEPTION_TEST_VARS                                                   |
|-----------------------------------------------------------------------|
| Error -20002: Submitted amount -3 is too low (1 or greater required). |
+-----------------------------------------------------------------------+
```

```
CALL exception_test_vars(20);
```

Copy

```
+----------------------------------------------------------------------+
| EXCEPTION_TEST_VARS                                                  |
|----------------------------------------------------------------------|
| Error -20003: Submitted amount 20 is too high (exceeds limit of 10). |
+----------------------------------------------------------------------+
```

Was this page helpful?

YesNo

[Visit Snowflake](https://www.snowflake.com)

[Join the conversation](https://community.snowflake.com/s/)

[Develop with Snowflake](https://developers.snowflake.com)

[Share your feedback](/feedback)

[Read the latest on our blog](https://www.snowflake.com/blog/)

[Get your own certification](https://learn.snowflake.com)

[Privacy Notice](https://www.snowflake.com/privacy-policy/)[Site Terms](https://www.snowflake.com/legal/snowflake-site-terms/)Cookies Settings© 2026 Snowflake, Inc. All Rights Reserved.

On this page

1. [Introduction to handling exceptions in Snowflake Scripting](#introduction-to-handling-exceptions-in-snowflake-scripting)
2. [Declaring an exception in Snowflake Scripting](#declaring-an-exception-in-snowflake-scripting)
3. [Raising a declared exception in Snowflake Scripting](#raising-a-declared-exception-in-snowflake-scripting)
4. [Handling an exception in Snowflake Scripting](#handling-an-exception-in-snowflake-scripting)
5. [Raising the same exception again in an exception handler in Snowflake Scripting](#raising-the-same-exception-again-in-an-exception-handler-in-snowflake-scripting)
6. [Passing variables to an exception handler in Snowflake Scripting](#passing-variables-to-an-exception-handler-in-snowflake-scripting)

Related content

1. [DECLARE (Snowflake Scripting)](/developer-guide/snowflake-scripting/../../sql-reference/snowflake-scripting/declare)
2. [EXCEPTION (Snowflake Scripting)](/developer-guide/snowflake-scripting/../../sql-reference/snowflake-scripting/exception)
3. [RAISE (Snowflake Scripting)](/developer-guide/snowflake-scripting/../../sql-reference/snowflake-scripting/raise)