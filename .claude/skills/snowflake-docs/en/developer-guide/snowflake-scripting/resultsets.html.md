---
auto_generated: true
description: This topic explains how to use a RESULTSET in Snowflake Scripting.
last_scraped: '2026-01-14T16:56:43.607382+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/developer-guide/snowflake-scripting/resultsets.html
title: Working with RESULTSETs | Snowflake Documentation
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

[Developer](../../developer.md)[Snowflake Scripting Developer Guide](index.md)RESULTSETs

# Working with RESULTSETs[¶](#working-with-resultsets "Link to this heading")

This topic explains how to use a RESULTSET in Snowflake Scripting.

## Introduction[¶](#introduction "Link to this heading")

In Snowflake Scripting, a RESULTSET is a SQL data type that points to the result set of a query.

Because a RESULTSET is just a pointer to the results, you must do one of the following to access the results through the
RESULTSET:

* Use the `TABLE(...)` syntax to retrieve the results as a table.
* Iterate over the RESULTSET with a [cursor](cursors).

Examples of both of these are included below.

## Understanding the differences between a cursor and a RESULTSET[¶](#understanding-the-differences-between-a-cursor-and-a-resultset "Link to this heading")

A RESULTSET and a [cursor](cursors) both provide access to the result set of a query. However, these objects differ in the
following ways:

* The point in time when the query is executed.

  + For a cursor, the query is executed when you execute the [OPEN](../../sql-reference/snowflake-scripting/open) command on the
    cursor.
  + For a RESULTSET, the query is executed when you assign the query to the RESULTSET (either in the DECLARE section
    or in the BEGIN … END block).
* Support for binding in the OPEN command.

  + When you declare a cursor, you can specify bind parameters (`?` characters). Later, when you execute the
    [OPEN](../../sql-reference/snowflake-scripting/open) command, you can bind variables to those parameters in the USING clause.
  + RESULTSET does not support the OPEN command. However, you can bind variables in SQL commands before returning the
    result set.

In general, it is simpler to use a RESULTSET when you want to return a table that contains the result set of a query. However,
you can also return a table from a Snowflake Scripting block with a cursor. To do so, you can pass the cursor to
`RESULTSET_FROM_CURSOR(cursor)` to return a RESULTSET and pass that RESULTSET to `TABLE(...)`. See
[Returning a table for a cursor](cursors.html#label-snowscript-cursors-return-table).

## Declaring a RESULTSET[¶](#declaring-a-resultset "Link to this heading")

You can declare a RESULTSET in the [DECLARE](../../sql-reference/snowflake-scripting/declare) section of a block or in the
[BEGIN … END](../../sql-reference/snowflake-scripting/begin) section of the block.

* Within the DECLARE section, use the syntax described in [RESULTSET declaration syntax](../../sql-reference/snowflake-scripting/declare.html#label-snowscript-declare-syntax-resultset). For example:

  ```
  DECLARE
    ...
    res RESULTSET DEFAULT (SELECT col1 FROM mytable ORDER BY col1);
  ```

  Copy
* Within the BEGIN … END block, use the syntax described in [RESULTSET assignment syntax](../../sql-reference/snowflake-scripting/let.html#label-snowscript-let-syntax-resultset). For example:

  ```
  BEGIN
    ...
    LET res RESULTSET := (SELECT col1 FROM mytable ORDER BY col1);
  ```

  Copy

## Assigning a query to a declared RESULTSET[¶](#assigning-a-query-to-a-declared-resultset "Link to this heading")

To assign the result of a query to a RESULTSET that has already been declared, use the following syntax:

```
<resultset_name> := [ ASYNC ] ( <query> ) ;
```

Copy

Where:

> `resultset_name`
> :   The name of the RESULTSET.
>
>     The name must be unique within the current scope.
>
>     The name must follow the naming rules for [Object identifiers](../../sql-reference/identifiers).
>
> `ASYNC`
> :   Runs the query as an [asynchronous child job](asynchronous-child-jobs).
>
> `query`
> :   The query to assign to the RESULTSET.

To assign a query to a RESULTSET:

```
DECLARE
  res RESULTSET;
BEGIN
  res := (SELECT col1 FROM mytable ORDER BY col1);
  ...
```

Copy

To assign a query to a RESULTSET and run the query as an asynchronous child job:

```
DECLARE
  res RESULTSET;
BEGIN
  res := ASYNC (SELECT col1 FROM mytable ORDER BY col1);
  ...
```

Copy

To build a SQL string dynamically for the query, set `query` to
`(EXECUTE IMMEDIATE string_of_sql)`. For example:

```
DECLARE
  res RESULTSET;
  col_name VARCHAR;
  select_statement VARCHAR;
BEGIN
  col_name := 'col1';
  select_statement := 'SELECT ' || col_name || ' FROM mytable';
  res := (EXECUTE IMMEDIATE :select_statement);
  RETURN TABLE(res);
END;
```

Copy

Although you can set `query` to an EXECUTE IMMEDIATE statement for a RESULTSET, you can’t do this for a
cursor.

## Using a RESULTSET[¶](#using-a-resultset "Link to this heading")

The query for a RESULTSET is executed when the object is associated with that query. For example:

* When you declare a RESULTSET and set the DEFAULT clause to a query, the query is executed at that point in time.
* When you use the `:=` operator to assign a query to a RESULTSET, the query is executed at that point in time.

Note

Because a RESULTSET points to the result set of a query (and does not contain the result set of a query), a RESULTSET
is valid only as long as the query results are cached (typically 24 hours). For details about query result caching,
see [Using Persisted Query Results](../../user-guide/querying-persisted-results).

Once the query is executed, you can access the results by using a cursor. You can also return the results as a table from a stored
procedure.

* [Using a cursor to access data from a RESULTSET](#label-snowscript-resultsets-use-cursor)
* [Returning a RESULTSET as a table](#label-snowscript-resultsets-use-return-table)

### Using a cursor to access data from a RESULTSET[¶](#using-a-cursor-to-access-data-from-a-resultset "Link to this heading")

To use a cursor to access the data from a RESULTSET, [declare the cursor](cursors.html#label-snowscript-cursors-declare) on the
object. For example:

```
DECLARE
  ...
  res RESULTSET DEFAULT (SELECT col1 FROM mytable ORDER BY col1);
  c1 CURSOR FOR res;
```

Copy

When you declare a cursor on a RESULTSET, the cursor gets access to the data already in the RESULTSET. Executing
the [OPEN](../../sql-reference/snowflake-scripting/open) command on the cursor does not execute the query for the RESULTSET
again.

You can then [open the cursor](cursors.html#label-snowscript-cursors-open) and use the cursor to
[fetch the data](cursors.html#label-snowscript-cursors-fetch).

Note

If the results include GEOGRAPHY values, you must cast the values to the GEOGRAPHY type before passing the values to any
functions that expect GEOGRAPHY input values. See [Using a cursor to retrieve a GEOGRAPHY value](cursors.html#label-snowscript-cursors-geography).

### Returning a RESULTSET as a table[¶](#returning-a-resultset-as-a-table "Link to this heading")

If you want to return the results that the RESULTSET points to, pass the RESULTSET to `TABLE(...)`. For example:

```
CREATE PROCEDURE f()
  RETURNS TABLE(column_1 INTEGER, column_2 VARCHAR)
  ...
    RETURN TABLE(my_resultset_1);
  ...
```

Copy

This is similar to the way that `TABLE(...)` is used with
[table functions](../../sql-reference/functions-table) (such as [RESULT\_SCAN](../../sql-reference/functions/result_scan)).

As shown in the example, if you write a stored procedure that returns a table, you must declare the stored procedure as returning
a table.

Note

Currently, the `TABLE(resultset_name)` syntax is supported only in the
[RETURN](../../sql-reference/snowflake-scripting/return) statement.

Even if you have used a cursor to [fetch rows from the RESULTSET](#label-snowscript-resultsets-use-cursor), the
table returned by `TABLE(resultset_name)` still contains all of the rows (not just the rows starting from the cursor’s
internal row pointer).

## Limitations of the RESULTSET data type[¶](#limitations-of-the-resultset-data-type "Link to this heading")

Although RESULTSET is a data type, Snowflake does not yet support:

* Declaring a column of type RESULTSET.
* Declaring a parameter of type RESULTSET.
* Declaring a stored procedure’s return type as a RESULTSET.

Snowflake supports RESULTSET only inside Snowflake Scripting.

In addition, you can’t use a RESULTSET directly as a table. For example, the following is invalid:

```
SELECT * FROM my_result_set;
```

Copy

## Examples of using a RESULTSET[¶](#examples-of-using-a-resultset "Link to this heading")

The following sections provide examples of using a RESULTSET:

* [Setting up the data for the examples](#label-snowscript-resultsets-example-setup)
* [Example: Returning a table from a stored procedure](#label-snowscript-resultsets-example-sp-table)
* [Example: Constructing the SQL statement dynamically](#label-snowscript-resultsets-example-dynamic-sql)
* [Example: Declaring a RESULTSET variable without a DEFAULT clause](#label-snowscript-resultsets-example-resultset-no-default)
* [Example: Using a CURSOR with a RESULTSET](#label-snowscript-resultsets-example-resultset-cursor)
* [Additional examples that use a RESULTSET](#label-snowscript-resultsets-additional-examples)

For examples that use the ASYNC keyword to run queries specified for RESULTSETs as asynchronous child jobs,
see [Examples of using asynchronous child jobs](asynchronous-child-jobs.html#label-snowscript-asynchronous-child-jobs-examples).

### Setting up the data for the examples[¶](#setting-up-the-data-for-the-examples "Link to this heading")

Many of the examples below use the table and data shown below:

```
CREATE OR REPLACE TABLE t001 (a INTEGER, b VARCHAR);
INSERT INTO t001 (a, b) VALUES
  (1, 'row1'),
  (2, 'row2');
```

Copy

### Example: Returning a table from a stored procedure[¶](#example-returning-a-table-from-a-stored-procedure "Link to this heading")

The following code shows how to declare a RESULTSET and return the results that the RESULTSET points to. The RETURNS
clause in the CREATE PROCEDURE command declares that the stored procedure returns a table, which contains one column of
type INTEGER.

The RETURN statement inside the block uses the `TABLE(...)` syntax to return the results as a table.

Create the stored procedure:

```
CREATE OR REPLACE PROCEDURE test_sp()
RETURNS TABLE(a INTEGER)
LANGUAGE SQL
AS
  DECLARE
    res RESULTSET DEFAULT (SELECT a FROM t001 ORDER BY a);
  BEGIN
    RETURN TABLE(res);
  END;
```

Copy

Note: If you use [Snowflake CLI](../snowflake-cli/index), [SnowSQL](../../user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](../python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](running-examples)):

```
CREATE OR REPLACE PROCEDURE test_sp()
RETURNS TABLE(a INTEGER)
LANGUAGE SQL
AS
$$
  DECLARE
      res RESULTSET default (SELECT a FROM t001 ORDER BY a);
  BEGIN
      RETURN TABLE(res);
  END;
$$;
```

Copy

Call the stored procedure:

```
CALL test_sp();
```

Copy

```
+---+
| A |
|---|
| 1 |
| 2 |
+---+
```

You can use the [pipe operator](../../sql-reference/operators-flow) (`->>`) to process the results of the stored procedure
call:

```
CALL test_sp()
  ->> SELECT *
        FROM $1
        WHERE a > 1;
```

Copy

```
+---+
| A |
|---|
| 2 |
+---+
```

You can also use the [RESULT\_SCAN](../../sql-reference/functions/result_scan) function to process the results after you call the
stored procedure:

```
CALL test_sp();
```

Copy

```
+---+
| A |
|---|
| 1 |
| 2 |
+---+
```

```
SELECT *
  FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()))
  WHERE a < 2;
```

Copy

```
+---+
| A |
|---|
| 1 |
+---+
```

### Example: Constructing the SQL statement dynamically[¶](#example-constructing-the-sql-statement-dynamically "Link to this heading")

You can construct the SQL dynamically. The following is an example that executes the same query as the previous stored procedure
but that uses a SQL statement that is constructed dynamically:

```
CREATE OR REPLACE PROCEDURE test_sp_dynamic(table_name VARCHAR)
  RETURNS TABLE(a INTEGER)
  LANGUAGE SQL
AS
DECLARE
  res RESULTSET;
  query VARCHAR DEFAULT 'SELECT a FROM IDENTIFIER(?) ORDER BY a;';
BEGIN
  res := (EXECUTE IMMEDIATE :query USING(table_name));
  RETURN TABLE(res);
END;
```

Copy

Note: If you use [Snowflake CLI](../snowflake-cli/index), [SnowSQL](../../user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](../python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](running-examples)):

```
CREATE OR REPLACE PROCEDURE test_sp_dynamic(table_name VARCHAR)
RETURNS TABLE(a INTEGER)
LANGUAGE SQL
AS
$$
  DECLARE
    res RESULTSET;
    query VARCHAR DEFAULT 'SELECT a FROM IDENTIFIER(?) ORDER BY a;';
  BEGIN
    res := (EXECUTE IMMEDIATE :query USING(table_name));
    RETURN TABLE(res);
  END
$$
;
```

Copy

To run the example, call the stored procedure and pass in the table name:

```
CALL test_sp_dynamic('t001');
```

Copy

```
+---+
| A |
|---|
| 1 |
| 2 |
+---+
```

### Example: Declaring a RESULTSET variable without a DEFAULT clause[¶](#example-declaring-a-resultset-variable-without-a-default-clause "Link to this heading")

The following code shows how to declare a RESULTSET without a DEFAULT clause (i.e. without associating a query with the RESULTSET),
and then associate the RESULTSET with a query later.

```
CREATE OR REPLACE PROCEDURE test_sp_02()
RETURNS TABLE(a INTEGER)
LANGUAGE SQL
AS
  DECLARE
    res RESULTSET;
  BEGIN
    res := (SELECT a FROM t001 ORDER BY a);
    RETURN TABLE(res);
  END;
```

Copy

Note: If you use [Snowflake CLI](../snowflake-cli/index), [SnowSQL](../../user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](../python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](running-examples)):

```
CREATE OR REPLACE PROCEDURE test_sp_02()
RETURNS TABLE(a INTEGER)
LANGUAGE SQL
AS
$$
  DECLARE
      res RESULTSET;
  BEGIN
      res := (SELECT a FROM t001 ORDER BY a);
      RETURN TABLE(res);
  END;
$$;
```

Copy

To run the example, call the stored procedure:

```
CALL test_sp_02();
```

Copy

```
+---+
| A |
|---|
| 1 |
| 2 |
+---+
```

### Example: Using a CURSOR with a RESULTSET[¶](#example-using-a-cursor-with-a-resultset "Link to this heading")

The following code shows how to use a [cursor](cursors) to iterate over the rows in a RESULTSET:

Create the stored procedure:

```
CREATE OR REPLACE PROCEDURE test_sp_03()
RETURNS VARCHAR
LANGUAGE SQL
AS

DECLARE
  accumulator INTEGER DEFAULT 0;
  res1 RESULTSET DEFAULT (SELECT a FROM t001 ORDER BY a);
  cur1 CURSOR FOR res1;
BEGIN
  FOR row_variable IN cur1 DO
    accumulator := accumulator + row_variable.a;
  END FOR;
  RETURN accumulator::VARCHAR;
END;
```

Copy

Note: If you use [Snowflake CLI](../snowflake-cli/index), [SnowSQL](../../user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](../python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](running-examples)):

```
CREATE OR REPLACE PROCEDURE test_sp_03()
RETURNS INTEGER
LANGUAGE SQL
AS
$$
  DECLARE
    accumulator INTEGER DEFAULT 0;
    res1 RESULTSET DEFAULT (SELECT a FROM t001 ORDER BY a);
    cur1 CURSOR FOR res1;
  BEGIN
    FOR row_variable IN cur1 DO
        accumulator := accumulator + row_variable.a;
    END FOR;
    RETURN accumulator;
  END;
$$;
```

Copy

Call the stored procedure, and the results add the values for `a` in the table (1 + 2):

```
CALL test_sp_03();
```

Copy

```
+------------+
| TEST_SP_03 |
|------------|
| 3          |
+------------+
```

### Additional examples that use a RESULTSET[¶](#additional-examples-that-use-a-resultset "Link to this heading")

Here are additional examples that use a RESULTSET:

* [Use a RESULTSET-based FOR loop](loops.html#label-snowscript-loop-for-resultset)

  This example shows you how to use a FOR loop that iterates over a RESULTSET.
* [Return a table for a cursor](cursors.html#label-snowscript-cursors-return-table)

  This example shows you how to use a cursor to return a table of data in a RESULTSET.
* [Update table data with user input](use-cases.html#label-snowscript-loop-for-conditional-logic-bind-variables)

  This example shows you how to use bind variables based on user input to update
  data in a table. It uses a FOR loop with conditional logic to iterate over the rows
  in a RESULTSET.
* [Filter and collect data](use-cases.html#label-snowscript-example-filter-and-collect-data)

  This example shows you how to use a RESULTSET to collect data and insert that
  data into a table to track historical trends.

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

1. [Introduction](#introduction)
2. [Understanding the differences between a cursor and a RESULTSET](#understanding-the-differences-between-a-cursor-and-a-resultset)
3. [Declaring a RESULTSET](#declaring-a-resultset)
4. [Assigning a query to a declared RESULTSET](#assigning-a-query-to-a-declared-resultset)
5. [Using a RESULTSET](#using-a-resultset)
6. [Limitations of the RESULTSET data type](#limitations-of-the-resultset-data-type)
7. [Examples of using a RESULTSET](#examples-of-using-a-resultset)

Related content

1. [DECLARE (Snowflake Scripting)](/developer-guide/snowflake-scripting/../../sql-reference/snowflake-scripting/declare)
2. [LET (Snowflake Scripting)](/developer-guide/snowflake-scripting/../../sql-reference/snowflake-scripting/let)
3. [RETURN (Snowflake Scripting)](/developer-guide/snowflake-scripting/../../sql-reference/snowflake-scripting/return)
4. [Working with cursors](/developer-guide/snowflake-scripting/cursors)
5. [Writing stored procedures in Snowflake Scripting](/developer-guide/snowflake-scripting/../stored-procedure/stored-procedures-snowflake-scripting)