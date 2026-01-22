---
auto_generated: true
description: In Snowflake Scripting, you can use variables in expressions, Snowflake
  Scripting statements, and SQL statements.
last_scraped: '2026-01-14T16:56:19.503170+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/developer-guide/snowflake-scripting/variables
title: Working with variables | Snowflake Documentation
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

[Developer](../../developer.md)[Snowflake Scripting Developer Guide](index.md)Variables

# Working with variables[¶](#working-with-variables "Link to this heading")

In Snowflake Scripting, you can use variables in expressions, Snowflake Scripting statements, and SQL statements.

## Declaring a variable[¶](#declaring-a-variable "Link to this heading")

Before you can use a variable, you must declare the variable. When you declare a variable, you must specify the type of the
variable in one of the following ways:

* Explicitly specify the data type.
* Specify an expression for the initial value of the variable. Snowflake Scripting uses the expression to determine the data
  type of the variable. See [How Snowflake Scripting infers the data type of a variable](#label-snowscript-variable-implicit-type).

You can declare a variable in the following ways:

* Within the [DECLARE](../../sql-reference/snowflake-scripting/declare) section of the block by using any of the following:

  ```
  <variable_name> <type> ;

  <variable_name> DEFAULT <expression> ;

  <variable_name> <type> DEFAULT <expression> ;
  ```

  Copy
* Within the [BEGIN … END](../../sql-reference/snowflake-scripting/begin) section of the block (before you use the variable)
  by using the [LET](../../sql-reference/snowflake-scripting/let) command in any of the following ways:

  ```
  LET <variable_name> <type> { DEFAULT | := } <expression> ;

  LET <variable_name> { DEFAULT | := } <expression> ;
  ```

  Copy

Where:

> `variable_name`
> :   The name of the variable. The name must follow the naming rules for [Object identifiers](../../sql-reference/identifiers).
>
> `type`
> :   The data type of the variable. The data type can be any of the following:
>
>     * A [SQL data type](../../sql-reference-data-types)
>
>     * [CURSOR](cursors)
>     * [RESULTSET](resultsets)
>     * [EXCEPTION](exceptions)
>
> `DEFAULT expression` or . `:= expression`
> :   Assigns the value of `expression` to the variable.
>
>     If both `type` and `expression` are specified, the expression must evaluate to a data type that matches.
>     If the types do not match, you can [cast](../../sql-reference/functions/cast) the value to the specified `type`.

The following example declares variables in the DECLARE section and in the BEGIN … END section of the block:

```
DECLARE
  profit number(38, 2) DEFAULT 0.0;
BEGIN
  LET cost number(38, 2) := 100.0;
  LET revenue number(38, 2) DEFAULT 110.0;

  profit := revenue - cost;
  RETURN profit;
END;
```

Copy

Note: If you use [Snowflake CLI](../snowflake-cli/index), [SnowSQL](../../user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](../python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](running-examples)):

```
EXECUTE IMMEDIATE 
$$
DECLARE
  profit number(38, 2) DEFAULT 0.0;
BEGIN
  LET cost number(38, 2) := 100.0;
  LET revenue number(38, 2) DEFAULT 110.0;

  profit := revenue - cost;
  RETURN profit;
END;
$$
;
```

Copy

```
+-----------------+
| anonymous block |
|-----------------|
|           10.00 |
+-----------------+
```

The next sections explain how the data type and scope of a variable are determined:

* [How Snowflake Scripting infers the data type of a variable](#label-snowscript-variable-implicit-type)
* [Understanding the scope of declarations](#label-snowscript-scope)

For information about assigning a value to a variable, see [Assigning a value to a declared variable](#label-snowscript-variables-assigning).

### How Snowflake Scripting infers the data type of a variable[¶](#how-snowflake-scripting-infers-the-data-type-of-a-variable "Link to this heading")

When you declare a variable without explicitly specifying the data type, Snowflake Scripting infers the
data type from the expression that you assign to the variable.

If you choose to omit the data type from the declaration, note the following:

* If the expression can resolve to different data types of different sizes, Snowflake typically chooses the type that is flexible
  (for example, FLOAT rather than NUMBER(3, 1)) and has a high storage capacity (for example, VARCHAR rather than VARCHAR(4)).

  For example, if you set a variable to the value `12.3`, Snowflake can choose one of several data types for the variable,
  including:

  + NUMBER(3, 1)
  + NUMBER(38, 1)
  + FLOAT

  In this example, Snowflake chooses FLOAT.

  If you need a specific data type for a variable (especially a numeric or timestamp type), Snowflake recommends that you specify
  the data type explicitly, even if you provide an initial value.
* If Snowflake is unable to infer the intended data type, Snowflake reports a SQL compilation error.

  For example, the following code declares a variable without explicitly specifying the data type. The code sets the variable to
  the value in a cursor.

  ```
  ...
  FOR current_row IN cursor_1 DO:
    LET price := current_row.price_column;
    ...
  ```

  Copy

  When the Snowflake Scripting block is compiled (for example, when the CREATE PROCEDURE command is executed), the cursor has not been
  opened, and the data type of the column in the cursor is unknown. As a result, Snowflake reports a SQL compilation error:

  ```
  092228 (P0000): SQL compilation error:
    error line 7 at position 4 variable 'PRICE' cannot have its type inferred from initializer
  ```

  Copy

### Understanding the scope of declarations[¶](#understanding-the-scope-of-declarations "Link to this heading")

Snowflake Scripting uses [lexical scoping](https://en.wikipedia.org/wiki/Scope_(computer_science)#Lexical_scope). When a
variable for a value, result set, cursor, or exception is declared in the DECLARE section of a block, the scope (or visibility)
of the declared object is that block and any blocks nested in that block.

If a block declares an object with the same name as an object declared in an outer block, then within the inner
block (and any blocks inside that block), only the inner block’s object is in scope. When an object name is
referenced, Snowflake looks for the object with that name by starting first in the current block, and then working
outward one block at a time until an object with a matching name is found.

For example, if an exception is declared inside a stored procedure, the exception’s scope is limited to that stored
procedure. Stored procedures called by that stored procedure cannot raise (or handle) that exception. Stored
procedures that call that procedure cannot handle (or raise) that exception.

## Assigning a value to a declared variable[¶](#assigning-a-value-to-a-declared-variable "Link to this heading")

To assign a value to a variable that has already been declared, use the `:=` operator:

```
<variable_name> := <expression> ;
```

Copy

Where:

> `variable_name`
> :   The name of the variable. The name must follow the naming rules for [Object identifiers](../../sql-reference/identifiers).
>
> `expression`
> :   The expression is evaluated and the resulting value is assigned to the variable.
>
>     The expression must evaluate to a data type that matches the type of the variable.
>     If the expression does not match the type, you can [cast](../../sql-reference/functions/cast) the value to the type of
>     the variable.
>
>     In the expression, you can use functions, including [built-in SQL functions](../../sql-reference-functions)
>     and [UDFs](../udf/udf-overview) (user-defined functions).

## Using a variable[¶](#using-a-variable "Link to this heading")

You can use variables in expressions and with Snowflake Scripting language elements (such as
[RETURN](../../sql-reference/snowflake-scripting/return)). You can add these language elements
to [stored procedures](../stored-procedure/stored-procedures-overview),
[Snowflake Scripting user-defined functions (UDF)](../udf/sql/udf-sql-procedural-functions),
and [anonymous blocks](blocks.html#label-snowscript-block-anonymous).

For example, the following code uses the variables `revenue` and `cost` in an expression and the
variable `profit` in a RETURN statement:

```
DECLARE
  profit NUMBER(38, 2);
  revenue NUMBER(38, 2);
  cost NUMBER(38, 2);
BEGIN
  ...
  profit := revenue - cost;
  ...
RETURN profit;
```

Copy

To use a variable in an exception handler (the [EXCEPTION](../../sql-reference/snowflake-scripting/exception) section of
a block), the variable must be declared in the [DECLARE](../../sql-reference/snowflake-scripting/declare) section or passed
as an argument to a stored procedure. It can’t be declared in the [BEGIN … END](../../sql-reference/snowflake-scripting/begin)
section. For more information, see [Passing variables to an exception handler in Snowflake Scripting](exceptions.html#label-snowscript-exception-raising-variables).

Tip

You can also use and set SQL (session) variables in Snowflake Scripting anonymous blocks and in stored procedures that run with
caller’s rights. For more information, see [Using and setting SQL variables in a stored procedure](../stored-procedure/stored-procedures-snowflake-scripting.html#label-stored-procedure-snowscript-sql-variables).

## Using a variable in a SQL statement (binding)[¶](#using-a-variable-in-a-sql-statement-binding "Link to this heading")

You can use a variable in a SQL statement, which is sometimes referred to as [binding](../../sql-reference/bind-variables)
a variable. To do so, prefix the variable name with a colon. For example:

```
INSERT INTO my_table (x) VALUES (:my_variable)
```

Copy

You can expand a bind variable that represents an [array](../../sql-reference/data-types-semistructured.html#label-data-type-array) into a list of individual values
by using the spread operator (`**`). For more information, see [Expansion operators](../../sql-reference/operators-expansion).

For information about binding variables in Snowflake Scripting stored procedures, see
[Using an argument in a SQL statement (binding)](../stored-procedure/stored-procedures-snowflake-scripting.html#label-stored-procedure-snowscript-arguments-binding).

If you are using the variable as the name of an object (for example, the name of a table in the FROM clause of a SELECT statement), use
the [IDENTIFIER](../../sql-reference/identifier-literal) keyword to indicate that the variable represents an object identifier.
For example:

```
SELECT COUNT(*) FROM IDENTIFIER(:table_name)
```

Copy

If you are using a variable in an expression or with a
[Snowflake Scripting language element](../../sql-reference-snowflake-scripting) (for example,
[RETURN](../../sql-reference/snowflake-scripting/return)), you do not need to prefix the variable with a colon.

For example, you do not need the colon prefix in the following cases:

* You are using the variable with RETURN. In this example, the variable `profit` is used with a Snowflake Scripting language
  element and does not need the colon prefix.

  ```
  RETURN profit;
  ```

  Copy
* You are building a string containing a SQL statement to execute. In this example, the variable `id_variable` is used in an
  expression and does not need the colon prefix.

  ```
  LET select_statement := 'SELECT * FROM invoices WHERE id = ' || id_variable;
  ```

  Copy

In addition, the [TO\_QUERY](../../sql-reference/functions/to_query) function provides a simple syntax for accepting a SQL string
directly in the FROM clause of a SELECT statement. For a comparison of the TO\_QUERY function with dynamic SQL,
see [Constructing SQL at runtime](../../user-guide/querying-construct-at-runtime).

## Setting variables to the results of a SELECT statement[¶](#setting-variables-to-the-results-of-a-select-statement "Link to this heading")

In a Snowflake Scripting block, you can use the [INTO](../../sql-reference/constructs/into) clause to set variables to the values of
expressions specified in a SELECT clause:

```
SELECT <expression1>, <expression2>, ... INTO :<variable1>, :<variable2>, ... FROM ... WHERE ...;
```

Copy

When you use this syntax:

* `variable1` is set to the value of `expression1`.
* `variable2` is set to the value of `expression2`.

The SELECT statement must return a single row.

The following example contains a SELECT statement that returns a single row. The example relies on data from this table:

```
CREATE OR REPLACE TABLE some_data (id INTEGER, name VARCHAR);
INSERT INTO some_data (id, name) VALUES
  (1, 'a'),
  (2, 'b');
```

Copy

The example sets the Snowflake Scripting variables `id` and `name` to the values returned for the columns with those names.

```
DECLARE
  id INTEGER;
  name VARCHAR;
BEGIN
  SELECT id, name INTO :id, :name FROM some_data WHERE id = 1;
  RETURN id || ' ' || name;
END;
```

Copy

Note: If you use [Snowflake CLI](../snowflake-cli/index), [SnowSQL](../../user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](../python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](running-examples)):

```
EXECUTE IMMEDIATE $$
DECLARE
  id INTEGER;
  name VARCHAR;
BEGIN
  SELECT id, name INTO :id, :name FROM some_data WHERE id = 1;
  RETURN :id || ' ' || :name;
END;
$$
;
```

Copy

The example prints out the `id` and `name` from the row returned by the SELECT statement.

```
+-----------------+
| anonymous block |
|-----------------|
| 1 a             |
+-----------------+
```

Copy

## Setting a variable to the return value of a stored procedure[¶](#setting-a-variable-to-the-return-value-of-a-stored-procedure "Link to this heading")

See [Using the value returned from a stored procedure call](../stored-procedure/stored-procedures-snowflake-scripting.html#label-stored-procedure-snowscript-call-sp-return-value).

## Using stored procedure arguments[¶](#using-stored-procedure-arguments "Link to this heading")

You can create [Snowflake Scripting stored procedures](../stored-procedure/stored-procedures-snowflake-scripting)
that are passed arguments when they are called. These arguments behave like declared variables in the body of the stored procedure.

Snowflake Scripting supports input (IN) and output (OUT) arguments. The argument type determines how you can use it in a stored
procedure.

For more information, see [Using arguments passed to a stored procedure](../stored-procedure/stored-procedures-snowflake-scripting.html#label-stored-procedure-snowscript-arguments).

## Examples of using variables[¶](#examples-of-using-variables "Link to this heading")

The following example shows how to declare a variable, assign a value or expression to a variable, and cast a value to the data
type of a variable:

```
DECLARE
  w INTEGER;
  x INTEGER DEFAULT 0;
  dt DATE;
  result_string VARCHAR;
BEGIN
  w := 1;                     -- Assign a value.
  w := 24 * 7;                -- Assign the result of an expression.
  dt := '2020-09-30'::DATE;   -- Explicit cast.
  dt := '2020-09-30';         -- Implicit cast.
  result_string := w::VARCHAR || ', ' || dt::VARCHAR;
  RETURN result_string;
END;
```

Copy

Note: If you use [Snowflake CLI](../snowflake-cli/index), [SnowSQL](../../user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](../python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](running-examples)):

```
EXECUTE IMMEDIATE $$
DECLARE
    w INTEGER;
    x INTEGER DEFAULT 0;
    dt DATE;
    result_string VARCHAR;
BEGIN
    w := 1;                     -- Assign a value.
    w := 24 * 7;                -- Assign the result of an expression.
    dt := '2020-09-30'::DATE;   -- Explicit cast.
    dt := '2020-09-30';         -- Implicit cast.
    result_string := w::VARCHAR || ', ' || dt::VARCHAR;
    RETURN result_string;
END;
$$
;
```

Copy

```
+-----------------+
| anonymous block |
|-----------------|
| 168, 2020-09-30 |
+-----------------+
```

The following example uses a built-in SQL function in the expression:

```
my_variable := SQRT(variable_x);
```

Copy

The following declaration implicitly specifies the data types of the variables `profit`, `cost`, and `revenue` by
specifying an initial value of the intended data type for each variable.

The example also demonstrates how to use the [LET](../../sql-reference/snowflake-scripting/let) statement to declare the
`cost` and `revenue` variables outside of the DECLARE portion of the block:

```
DECLARE
  profit number(38, 2) DEFAULT 0.0;
BEGIN
  LET cost number(38, 2) := 100.0;
  LET revenue number(38, 2) DEFAULT 110.0;

  profit := revenue - cost;
  RETURN profit;
END;
```

Copy

Note: If you use [Snowflake CLI](../snowflake-cli/index), [SnowSQL](../../user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](../python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](running-examples)):

```
EXECUTE IMMEDIATE $$
DECLARE
    profit DEFAULT 0.0;
BEGIN
    LET cost := 100.0;
    LET revenue DEFAULT 110.0;
    profit := revenue - cost;
    RETURN profit;
END;
$$
;
```

Copy

```
+-----------------+
| anonymous block |
|-----------------|
|              10 |
+-----------------+
```

The following example demonstrates the scope of a variable. This example includes two variables and a parameter that all have the
same name but different scope.

The example contains three blocks: the outermost, middle, and innermost blocks.

* Within the innermost block, PV\_NAME resolves to the variable declared and set in that innermost block
  (which is set to `innermost block variable`).
* Within the middle block (and outside of the innermost block), PV\_NAME resolves to the variable declared and set in the
  middle block (which is set to `middle block variable`).
* Within the outermost block (and outside any of the nested blocks), PV\_NAME resolves to the parameter passed to the stored
  procedure (which is set to `parameter` by the CALL statement).

The example relies on this table:

```
CREATE OR REPLACE TABLE names (v VARCHAR);
```

Copy

In this example, the assignment of the string `innermost block variable` to PV\_NAME in the innermost block does not affect the
value of the variable in the middle block. The variable in the innermost block is different from the variable in the middle block,
even if both variables have the same name.

```
CREATE OR REPLACE PROCEDURE duplicate_name(pv_name VARCHAR)
RETURNS VARCHAR
LANGUAGE SQL
AS
BEGIN
  DECLARE
    PV_NAME VARCHAR;
  BEGIN
    PV_NAME := 'middle block variable';
    DECLARE
      PV_NAME VARCHAR;
    BEGIN
      PV_NAME := 'innermost block variable';
      INSERT INTO names (v) VALUES (:PV_NAME);
    END;
    -- Because the innermost and middle blocks have separate variables
    -- named "pv_name", the INSERT below inserts the value
    -- 'middle block variable'.
    INSERT INTO names (v) VALUES (:PV_NAME);
  END;
  -- This inserts the value of the input parameter.
  INSERT INTO names (v) VALUES (:PV_NAME);
  RETURN 'Completed.';
END;
```

Copy

Note: If you use [Snowflake CLI](../snowflake-cli/index), [SnowSQL](../../user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](../python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](running-examples)):

```
CREATE OR REPLACE PROCEDURE duplicate_name(pv_name VARCHAR)
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
BEGIN
  DECLARE
    PV_NAME VARCHAR;
  BEGIN
    PV_NAME := 'middle block variable';
    DECLARE
    PV_NAME VARCHAR;
    BEGIN
      PV_NAME := 'innermost block variable';
      INSERT INTO names (v) VALUES (:PV_NAME);
    END;
    -- Because the innermost and middle blocks have separate variables
    -- named "pv_name", the INSERT below inserts the value
    -- 'middle block variable'.
    INSERT INTO names (v) VALUES (:PV_NAME);
  END;
  -- This inserts the value of the input parameter.
  INSERT INTO names (v) VALUES (:PV_NAME);
  RETURN 'Completed.';
END;
$$
;
```

Copy

Call the stored procedure:

```
CALL duplicate_name('parameter');
```

Copy

Check the values in the table:

```
SELECT *
    FROM names
    ORDER BY v;
```

Copy

```
+--------------------------+
| V                        |
|--------------------------|
| innermost block variable |
| middle block variable    |
| parameter                |
+--------------------------+
```

The output shows that:

* In the innermost nested block (which was nested two layers), the inner block’s variable `PV_NAME` was used.
* In the middle block (which was nested one layer), that middle block’s variable `PV_NAME` was used.
* In the outermost block, the parameter was used.

For an example of binding a variable when opening a cursor, see the
[examples of opening cursors](../../sql-reference/snowflake-scripting/open.html#label-open-cursor-examples).

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

1. [Declaring a variable](#declaring-a-variable)
2. [Assigning a value to a declared variable](#assigning-a-value-to-a-declared-variable)
3. [Using a variable](#using-a-variable)
4. [Using a variable in a SQL statement (binding)](#using-a-variable-in-a-sql-statement-binding)
5. [Setting variables to the results of a SELECT statement](#setting-variables-to-the-results-of-a-select-statement)
6. [Setting a variable to the return value of a stored procedure](#setting-a-variable-to-the-return-value-of-a-stored-procedure)
7. [Using stored procedure arguments](#using-stored-procedure-arguments)
8. [Examples of using variables](#examples-of-using-variables)

Related content

1. [DECLARE (Snowflake Scripting)](/developer-guide/snowflake-scripting/../../sql-reference/snowflake-scripting/declare)
2. [LET (Snowflake Scripting)](/developer-guide/snowflake-scripting/../../sql-reference/snowflake-scripting/let)
3. [INTO](/developer-guide/snowflake-scripting/../../sql-reference/constructs/into)
4. [Working with cursors](/developer-guide/snowflake-scripting/cursors)
5. [Working with RESULTSETs](/developer-guide/snowflake-scripting/resultsets)
6. [Handling exceptions](/developer-guide/snowflake-scripting/exceptions)
7. [Writing stored procedures in Snowflake Scripting](/developer-guide/snowflake-scripting/../stored-procedure/stored-procedures-snowflake-scripting)