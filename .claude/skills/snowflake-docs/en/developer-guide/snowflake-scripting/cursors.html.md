---
auto_generated: true
description: You can use a cursor to iterate through query results one row at a time.
last_scraped: '2026-01-14T16:56:42.987267+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/developer-guide/snowflake-scripting/cursors.html
title: Working with cursors | Snowflake Documentation
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

[Developer](../../developer.md)[Snowflake Scripting Developer Guide](index.md)Cursors

# Working with cursors[¶](#working-with-cursors "Link to this heading")

You can use a cursor to iterate through query results one row at a time.

## Introduction[¶](#introduction "Link to this heading")

To retrieve data from the results of a query, you can use a cursor. To iterate over the rows in the results,
you can use a cursor in <loops>.

To use a cursor, do the following:

1. In the [DECLARE](../../sql-reference/snowflake-scripting/declare) section,
   [declare the cursor](#label-snowscript-cursors-declare). The declaration includes the query for the cursor.
2. Before you use the cursor for the first time, execute the [OPEN](../../sql-reference/snowflake-scripting/open) command to
   [open the cursor](#label-snowscript-cursors-open). This executes the query and loads the results into the cursor.
3. Execute the [FETCH](../../sql-reference/snowflake-scripting/fetch) command to
   [fetch one or more rows](#label-snowscript-cursors-fetch) and process those rows.
4. When you are done with the results or the cursor is no longer needed, execute the [CLOSE](../../sql-reference/snowflake-scripting/close)
   command to [close the cursor](#label-snowscript-cursors-close).

Note

You can also use a RESULTSET to retrieve the results of a query when you use Snowflake Scripting. For information
about the differences between a cursor and a RESULTSET, see [Understanding the differences between a cursor and a RESULTSET](resultsets.html#label-snowscript-resultsets-cursor-diff).

## Setting up the data for the examples[¶](#setting-up-the-data-for-the-examples "Link to this heading")

The examples in this section uses the following data:

```
CREATE OR REPLACE TABLE invoices (id INTEGER, price NUMBER(12, 2));

INSERT INTO invoices (id, price) VALUES
  (1, 11.11),
  (2, 22.22);
```

Copy

## Declaring a cursor[¶](#declaring-a-cursor "Link to this heading")

You can declare a cursor for a SELECT statement or a [RESULTSET](resultsets).

You declare a cursor in the [DECLARE](../../sql-reference/snowflake-scripting/declare) section of a block or in the
[BEGIN … END](../../sql-reference/snowflake-scripting/begin) section of the block:

* Within the DECLARE section, use the syntax described in [Cursor declaration syntax](../../sql-reference/snowflake-scripting/declare.html#label-snowscript-declare-syntax-cursor).

  For example, to declare a cursor for a query:

  ```
  DECLARE
    ...
    c1 CURSOR FOR SELECT price FROM invoices;
  ```

  Copy

  To declare a cursor for a RESULTSET:

  ```
  DECLARE
    ...
    res RESULTSET DEFAULT (SELECT price FROM invoices);
    c1 CURSOR FOR res;
  ```

  Copy
* Within the BEGIN … END block, use the syntax described in [Cursor assignment syntax](../../sql-reference/snowflake-scripting/let.html#label-snowscript-let-syntax-cursor). For example:

  ```
  BEGIN
    ...
    LET c1 CURSOR FOR SELECT price FROM invoices;
  ```

  Copy

In the SELECT statement, you can specify bind parameters (`?` characters) that you can bind to variables when opening the
cursor. To bind variables to the parameters, specify the variables in the USING clause of the OPEN command. For example:

```
DECLARE
  id INTEGER DEFAULT 0;
  minimum_price NUMBER(13,2) DEFAULT 22.00;
  maximum_price NUMBER(13,2) DEFAULT 33.00;
  c1 CURSOR FOR SELECT id FROM invoices WHERE price > ? AND price < ?;
BEGIN
  OPEN c1 USING (minimum_price, maximum_price);
  FETCH c1 INTO id;
  RETURN id;
END;
```

Copy

Note: If you use [Snowflake CLI](../snowflake-cli/index), [SnowSQL](../../user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](../python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](running-examples)):

```
EXECUTE IMMEDIATE $$
DECLARE
  id INTEGER DEFAULT 0;
  minimum_price NUMBER(13,2) DEFAULT 22.00;
  maximum_price NUMBER(13,2) DEFAULT 33.00;
  c1 CURSOR FOR SELECT id FROM invoices WHERE price > ? AND price < ?;
BEGIN
  OPEN c1 USING (minimum_price, maximum_price);
  FETCH c1 INTO id;
  RETURN id;
END;
$$
;
```

Copy

```
+-----------------+
| anonymous block |
|-----------------|
|               2 |
+-----------------+
```

## Opening a cursor[¶](#opening-a-cursor "Link to this heading")

Although the statement that declares a cursor defines the query associated with that cursor, the query is not executed until you
open the cursor by executing the [OPEN](../../sql-reference/snowflake-scripting/open) command. For example:

```
OPEN c1;
```

Copy

Note

* When using a cursor in a [FOR](loops.html#label-snowscript-loop-for) loop, you do not need to open the cursor explicitly.
* If you declare a cursor for a RESULTSET object, the query is executed when you associate the object with the query. In this
  case, opening the cursor does not cause the query to be executed again.

If your query contains any bind parameters (`?` characters), add a USING clause to specify the list of variables to bind
to those parameters. For example:

```
LET c1 CURSOR FOR SELECT id FROM invoices WHERE price > ? AND price < ?;
OPEN c1 USING (minimum_price, maximum_price);
```

Copy

Opening the cursor executes the query, retrieves the specified rows into the cursor, and sets up an internal pointer that points
to the first row. You can use the FETCH command to
[fetch (read) individual rows using the cursor](#label-snowscript-cursors-fetch).

As with any SQL query, if the query definition does not contain an ORDER BY at the outermost level, then the result set has no
defined order. When the result set for the cursor is created, the order of the rows is persistent until the cursor is closed.
If you declare or open the cursor again, the rows might be in a different order. Similarly, if you close the cursor and
the underlying table is updated before you open the cursor again, the result set can change.

## Using a cursor to fetch data[¶](#using-a-cursor-to-fetch-data "Link to this heading")

Use the [FETCH](../../sql-reference/snowflake-scripting/fetch) command to retrieve the current row from the result set and
advance the internal current row pointer to point to the next row in the result set.

In the INTO clause, specify the variables that hold the values from the row.

For example:

```
FETCH c1 INTO var_for_column_value;
```

Copy

If the number of variables does not match the number of expressions in the SELECT clause of the cursor declaration, Snowflake
attempts to match the variables with the columns by position:

* If there are more variables than columns, Snowflake leaves the remaining variables unset.
* If there are more columns than variables, Snowflake ignores the remaining columns.

Each subsequent FETCH command that you execute gets the next row until the last row has been fetched. If you try to FETCH
a row after the last row, you get NULL values.

A RESULTSET or cursor does not necessarily cache all the rows of the result set at the time that the query is executed. FETCH operations can experience latency.

## Using a cursor to retrieve a GEOGRAPHY value[¶](#using-a-cursor-to-retrieve-a-geography-value "Link to this heading")

If the results include a column of the type GEOGRAPHY, the type of the value in the column is OBJECT, not GEOGRAPHY. This means
that you cannot directly pass this value to [geospatial functions](../../sql-reference/functions-geospatial) that accept a
GEOGRAPHY object as input:

```
DECLARE
  geohash_value VARCHAR;
BEGIN
  LET res RESULTSET := (SELECT TO_GEOGRAPHY('POINT(1 1)') AS GEOGRAPHY_VALUE);
  LET cur CURSOR FOR res;
  FOR row_variable IN cur DO
    geohash_value := ST_GEOHASH(row_variable.geography_value);
  END FOR;
  RETURN geohash_value;
END;
```

Copy

```
001044 (42P13): Uncaught exception of type 'EXPRESSION_ERROR' on line 7 at position 21 : SQL compilation error: ...
Invalid argument types for function 'ST_GEOHASH': (OBJECT)
```

Copy

To work around this, cast the column value to the GEOGRAPHY type:

```
geohash_value := ST_GEOHASH(TO_GEOGRAPHY(row_variable.geography_value));
```

Copy

## Returning a table for a cursor[¶](#returning-a-table-for-a-cursor "Link to this heading")

If you need to return a table of data from a cursor, you can pass the cursor to `RESULTSET_FROM_CURSOR(cursor)`, which in
turn you can pass to `TABLE(...)`.

The following block returns a table of data from a cursor:

```
DECLARE
  c1 CURSOR FOR SELECT * FROM invoices;
BEGIN
  OPEN c1;
  RETURN TABLE(RESULTSET_FROM_CURSOR(c1));
END;
```

Copy

Note: If you use [Snowflake CLI](../snowflake-cli/index), [SnowSQL](../../user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](../python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](running-examples)):

```
EXECUTE IMMEDIATE $$
DECLARE
  c1 CURSOR FOR SELECT * FROM invoices;
BEGIN
  OPEN c1;
  RETURN TABLE(RESULTSET_FROM_CURSOR(c1));
END;
$$
;
```

Copy

```
+----+-------+
| ID | PRICE |
|----+-------|
|  1 | 11.11 |
|  2 | 22.22 |
+----+-------+
```

Even if you have already used the cursor to [fetch rows](#label-snowscript-cursors-fetch),
`RESULTSET_FROM_CURSOR` still returns a RESULTSET containing all of the rows, not just the rows starting from the internal
row pointer.

As shown above, the example fetches the first row and sets the internal row pointer to the second row.
`RESULTSET_FROM_CURSOR` returns a RESULTSET containing both rows (not just the second row).

## Closing a cursor[¶](#closing-a-cursor "Link to this heading")

When you are done with the result set, close the cursor by executing the [CLOSE](../../sql-reference/snowflake-scripting/close)
command. For example:

```
CLOSE c1;
```

Copy

Note

When using a cursor in a [FOR](loops.html#label-snowscript-loop-for) loop, you do not need to close the cursor explicitly.

You cannot execute the FETCH command on a cursor that has been closed.

In addition, after you close a cursor, the current row pointer becomes invalid. If you open the cursor again, the pointer points
to the first row in the new result set.

## Example of using a cursor[¶](#example-of-using-a-cursor "Link to this heading")

This example uses data that you set up in [Setting up the data for the examples](#label-snowscript-cursors-example-setup).

Here is an anonymous block that uses a cursor to read two rows and sum the prices in those rows:

```
DECLARE
  row_price FLOAT;
  total_price FLOAT;
  c1 CURSOR FOR SELECT price FROM invoices;
BEGIN
  row_price := 0.0;
  total_price := 0.0;
  OPEN c1;
  FETCH c1 INTO row_price;
  total_price := total_price + row_price;
  FETCH c1 INTO row_price;
  total_price := total_price + row_price;
  CLOSE c1;
  RETURN total_price;
END;
```

Copy

Note: If you use [Snowflake CLI](../snowflake-cli/index), [SnowSQL](../../user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](../python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](running-examples)):

```
EXECUTE IMMEDIATE $$
DECLARE
    row_price FLOAT;
    total_price FLOAT;
    c1 CURSOR FOR SELECT price FROM invoices;
BEGIN
    row_price := 0.0;
    total_price := 0.0;
    OPEN c1;
    FETCH c1 INTO row_price;
    total_price := total_price + row_price;
    FETCH c1 INTO row_price;
    total_price := total_price + row_price;
    CLOSE c1;
    RETURN total_price;
END;
$$
;
```

Copy

```
+-----------------+
| anonymous block |
|-----------------|
|           33.33 |
+-----------------+
```

You can achieve the same result by using a cursor with a [FOR loop](loops.html#label-snowscript-loop-for):

```
DECLARE
  total_price FLOAT;
  c1 CURSOR FOR SELECT price FROM invoices;
BEGIN
  total_price := 0.0;
  FOR record IN c1 DO
    total_price := total_price + record.price;
  END FOR;
  RETURN total_price;
END;
```

Copy

Note: If you use [Snowflake CLI](../snowflake-cli/index), [SnowSQL](../../user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](../python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](running-examples)):

```
EXECUTE IMMEDIATE $$
DECLARE
  total_price FLOAT;
  c1 CURSOR FOR SELECT price FROM invoices;
BEGIN
  total_price := 0.0;
  FOR record IN c1 DO
    total_price := total_price + record.price;
  END FOR;
  RETURN total_price;
END;
$$
;
```

Copy

```
+-----------------+
| anonymous block |
|-----------------|
|           33.33 |
+-----------------+
```

## Troubleshooting problems with cursors[¶](#troubleshooting-problems-with-cursors "Link to this heading")

The following section describes common problems with cursors and identifies a possible cause and solution in each case.

### Symptom: Cursor retrieves every second row rather than every row[¶](#symptom-cursor-retrieves-every-second-row-rather-than-every-row "Link to this heading")

* **Possible cause:** You might have executed FETCH inside a FOR `<record>` IN `<cursor>` loop. A FOR loop over a cursor
  automatically fetches the next row. If you do another fetch inside the loop, you get every second row.
* **Possible solution:** Remove any unneeded FETCH commands inside a FOR loop.

### Symptom: FETCH command retrieves unexpected NULL values[¶](#symptom-fetch-command-retrieves-unexpected-null-values "Link to this heading")

* **Possible cause:** You might have executed FETCH inside a FOR `<record>` IN `<cursor>` loop. A FOR loop over a cursor
  automatically fetches the next row. If you do another fetch inside the loop, you get every second row. If
  there is an odd number of rows, the last fetch will try to fetch a row beyond the last row, and the
  values will be NULL.
* **Possible solution:** Remove any unneeded FETCH commands inside a FOR loop.

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
2. [Setting up the data for the examples](#setting-up-the-data-for-the-examples)
3. [Declaring a cursor](#declaring-a-cursor)
4. [Opening a cursor](#opening-a-cursor)
5. [Using a cursor to fetch data](#using-a-cursor-to-fetch-data)
6. [Using a cursor to retrieve a GEOGRAPHY value](#using-a-cursor-to-retrieve-a-geography-value)
7. [Returning a table for a cursor](#returning-a-table-for-a-cursor)
8. [Closing a cursor](#closing-a-cursor)
9. [Example of using a cursor](#example-of-using-a-cursor)
10. [Troubleshooting problems with cursors](#troubleshooting-problems-with-cursors)

Related content

1. [DECLARE (Snowflake Scripting)](/developer-guide/snowflake-scripting/../../sql-reference/snowflake-scripting/declare)
2. [LET (Snowflake Scripting)](/developer-guide/snowflake-scripting/../../sql-reference/snowflake-scripting/let)
3. [OPEN (Snowflake Scripting)](/developer-guide/snowflake-scripting/../../sql-reference/snowflake-scripting/open)
4. [FETCH (Snowflake Scripting)](/developer-guide/snowflake-scripting/../../sql-reference/snowflake-scripting/fetch)
5. [CLOSE (Snowflake Scripting)](/developer-guide/snowflake-scripting/../../sql-reference/snowflake-scripting/close)
6. [Working with loops](/developer-guide/snowflake-scripting/loops)
7. [Working with RESULTSETs](/developer-guide/snowflake-scripting/resultsets)