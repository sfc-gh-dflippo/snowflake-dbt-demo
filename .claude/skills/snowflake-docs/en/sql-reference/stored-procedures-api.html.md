---
auto_generated: true
description: This topic covers the JavaScript API for Snowflake stored procedures.
  The API consists of JavaScript objects and the methods in those objects.
last_scraped: '2026-01-14T16:56:32.277869+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/stored-procedures-api.html
title: JavaScript stored procedures API | Snowflake Documentation
---

1. [Overview](../developer.md)
2. Builders
3. [Snowflake DevOps](../developer-guide/builders/devops.md)
4. [Observability](../developer-guide/builders/observability.md)
5. Snowpark Library
6. [Snowpark API](../developer-guide/snowpark/index.md)
7. [Spark workloads on Snowflake](../developer-guide/snowpark-connect/snowpark-connect-overview.md)
8. Machine Learning
9. [Snowflake ML](../developer-guide/snowflake-ml/overview.md)
10. Snowpark Code Execution Environments
11. [Snowpark Container Services](../developer-guide/snowpark-container-services/overview.md)
12. [Functions and procedures](../developer-guide/extensibility.md)

    * [Function or procedure?](../developer-guide/stored-procedures-vs-udfs.md)
    * [Guidelines](../developer-guide/udf-stored-procedure-guidelines.md)
    * [Stored procedures](../developer-guide/stored-procedure/stored-procedures-overview.md)

      + [Usage](../developer-guide/stored-procedure/stored-procedures-usage.md)
      + [Caller and owner rights](../developer-guide/stored-procedure/stored-procedures-rights.md)
      + [Creating](../developer-guide/stored-procedure/stored-procedures-creating.md)
      + [Calling](../developer-guide/stored-procedure/stored-procedures-calling.md)
      + [Selecting from](../developer-guide/stored-procedure/stored-procedures-selecting-from.md)
      + [Passing in references](../developer-guide/stored-procedure/stored-procedures-calling-references.md)
      + Handler writing
      + [Java](../developer-guide/stored-procedure/java/procedure-java-overview.md)
      + [Javascript](../developer-guide/stored-procedure/stored-procedures-javascript.md)

        - [API](../developer-guide/stored-procedure/stored-procedures-api.md)
      + [Python](../developer-guide/stored-procedure/python/procedure-python-overview.md)
      + [Scala](../developer-guide/stored-procedure/scala/procedure-scala-overview.md)
      + [Snowflake Scripting](../developer-guide/stored-procedure/stored-procedures-snowflake-scripting.md)
    * [User-defined functions](../developer-guide/udf/udf-overview.md)
    * [Packaging handler code](../developer-guide/udf-stored-procedure-building.md)
    * [External network access](../developer-guide/external-network-access/external-network-access-overview.md)
13. [Logging, Tracing, and Metrics](../developer-guide/logging-tracing/logging-tracing-overview.md)
14. Snowflake APIs
15. [Snowflake Python APIs](../developer-guide/snowflake-python-api/snowflake-python-overview.md)
16. [Snowflake REST APIs](../developer-guide/snowflake-rest-api/snowflake-rest-api.md)
17. [SQL API](../developer-guide/sql-api/index.md)
18. Apps
19. Streamlit in Snowflake

    - [About Streamlit in Snowflake](../developer-guide/streamlit/about-streamlit.md)
    - Getting started

      - [Deploy a sample app](../developer-guide/streamlit/getting-started/overview.md)
      - [Create and deploy Streamlit apps using Snowsight](../developer-guide/streamlit/getting-started/create-streamlit-ui.md)
      - [Create and deploy Streamlit apps using SQL](../developer-guide/streamlit/getting-started/create-streamlit-sql.md)
      - [Create and deploy Streamlit apps using Snowflake CLI](../developer-guide/streamlit/getting-started/create-streamlit-snowflake-cli.md)
    - Streamlit object management

      - [Billing considerations](../developer-guide/streamlit/object-management/billing.md)
      - [Security considerations](../developer-guide/streamlit/object-management/security.md)
      - [Privilege requirements](../developer-guide/streamlit/object-management/privileges.md)
      - [Understanding owner's rights](../developer-guide/streamlit/object-management/owners-rights.md)
      - [PrivateLink](../developer-guide/streamlit/object-management/privatelink.md)
      - [Logging and tracing](../developer-guide/streamlit/object-management/logging-tracing.md)
    - App development

      - [Runtime environments](../developer-guide/streamlit/app-development/runtime-environments.md)
      - [Dependency management](../developer-guide/streamlit/app-development/dependency-management.md)
      - [File organization](../developer-guide/streamlit/app-development/file-organization.md)
      - [Secrets and configuration](../developer-guide/streamlit/app-development/secrets-and-configuration.md)
      - [Editing your app](../developer-guide/streamlit/app-development/editing-your-app.md)
    - Migrations and upgrades

      - [Identify your app type](../developer-guide/streamlit/migrations-and-upgrades/overview.md)
      - [Migrate to a container runtime](../developer-guide/streamlit/migrations-and-upgrades/runtime-migration.md)
      - [Migrate from ROOT\_LOCATION](../developer-guide/streamlit/migrations-and-upgrades/root-location.md)
    - Features

      - [Git integration](../developer-guide/streamlit/features/git-integration.md)
      - [External access](../developer-guide/streamlit/features/external-access.md)
      - [Row access policies](../developer-guide/streamlit/features/row-access.md)
      - [Sleep timer](../developer-guide/streamlit/features/sleep-timer.md)
    - [Limitations and library changes](../developer-guide/streamlit/limitations.md)
    - [Troubleshooting Streamlit in Snowflake](../developer-guide/streamlit/troubleshooting.md)
    - [Release notes](../release-notes/streamlit-in-snowflake.md)
    - [Streamlit open-source library documentation](https://docs.streamlit.io/)
20. [Snowflake Native App Framework](../developer-guide/native-apps/native-apps-about.md)
21. [Snowflake Declarative Sharing](../developer-guide/declarative-sharing/about.md)
22. [Snowflake Native SDK for Connectors](../developer-guide/native-apps/connector-sdk/about-connector-sdk.md)
23. External Integration
24. [External Functions](external-functions.md)
25. [Kafka and Spark Connectors](../user-guide/connectors.md)
26. Snowflake Scripting
27. [Snowflake Scripting Developer Guide](../developer-guide/snowflake-scripting/index.md)
28. Tools
29. [Snowflake CLI](../developer-guide/snowflake-cli/index.md)
30. [Git](../developer-guide/git/git-overview.md)
31. Drivers
32. [Overview](../developer-guide/drivers.md)
33. [Considerations when drivers reuse sessions](../developer-guide/driver-connections.md)
34. [Scala versions](../developer-guide/scala-version-differences.md)
35. Reference
36. [API Reference](../api-reference.md)

[Developer](../developer.md)[Functions and procedures](../developer-guide/extensibility.md)[Stored procedures](../developer-guide/stored-procedure/stored-procedures-overview.md)[Javascript](../developer-guide/stored-procedure/stored-procedures-javascript.md)API

# JavaScript stored procedures API[¶](#javascript-stored-procedures-api "Link to this heading")

This topic covers the JavaScript API for Snowflake stored procedures.
The API consists of JavaScript objects and the methods in those objects.

## Object: `snowflake`[¶](#object-snowflake "Link to this heading")

The `snowflake` object is accessible by default to the JavaScript code in a stored procedure; you do not need to create the object.
This object contains the methods in the stored procedure API. For example:

> ```
> CREATE PROCEDURE stproc1()
>   RETURNS STRING NOT NULL
>   LANGUAGE JAVASCRIPT
>   AS
>   -- "$$" is the delimiter for the beginning and end of the stored procedure.
>   $$
>   // The "snowflake" object is provided automatically in each stored procedure.
>   var statement = snowflake.createStatement(...);
>   ...
>   $$
>   ;
> ```
>
> Copy

More extensive code examples are provided in [Working with stored procedures](stored-procedures-usage).

### Constants[¶](#constants "Link to this heading")

None.

### Methods[¶](#methods "Link to this heading")

addEvent(*name*[, *attributes*])[¶](#addEvent "Link to this definition")
:   Adds an event for tracing.

    For more information about trace events with JavaScript, refer to [Emitting trace events in JavaScript](../logging-tracing/tracing-javascript)

    Parameters:
    :   `name`

        > The name of the event to add.

        `attributes`

        > An object specifying attributes to associate with the event.

    Errors:
    :   Throws a JavaScript Error if:

        * `name` is not a string.
        * There are zero or more than two arguments.

    Examples:
    :   Add a `my_event` event with `score` and `pass` attributes.

        ```
        snowflake.addEvent('my_event', {'score': 89, 'pass': true});
        ```

        Copy

createStatement(*sql\_command\_object*)[¶](#createStatement "Link to this definition")
:   Creates a `Statement` object representing the statement specified by `sql_command_object`. You can use the
    `Statement.execute()` method to execute the statement.

    Parameter(s):
    :   `sql_command_object`

        > A JSON object (dictionary) that contains the text of the SQL statement to execute and values to bind to that statement.
        > Properties of the `sql_command_object` JSON object include:
        >
        > * `sqlText`: A string containing the SQL statement to execute.
        > * `binds`: An array of values to bind to placeholders in the SQL statement specified by `sqlText`.

    Returns:
    :   A `Statement` object.

    Errors:
    :   Throws a JavaScript Error if:

        * `sqlText` is missing or contains an empty query text.
        * The statement tries to bind an argument whose data type is not supported. For information about data type
          mapping, see [SQL and JavaScript data type mapping](stored-procedures-javascript.html#label-stored-procedure-data-type-mapping).
          For more information about binding, see [Binding variables](stored-procedures-javascript.html#label-stored-procedures-binding-variables).

    Examples:
    :   The following example does not bind any values:

        ```
        var stmt = snowflake.createStatement(
          {sqlText: "INSERT INTO table1 (col1) VALUES (1);"}
        );
        ```

        Copy

        The following example binds values. Values in the `binds` property array are bound to `?` placeholders in the SQL text
        in the order they appear in the array.

        ```
        var stmt = snowflake.createStatement(
          {
          sqlText: "INSERT INTO table2 (col1, col2) VALUES (?, ?);",
          binds:["LiteralValue1", variable2]
          }
        );
        ```

        Copy

        For more information about binding, including additional examples,
        see [Binding variables](stored-procedures-javascript.html#label-stored-procedures-binding-variables).

execute(*sql\_command\_object*)[¶](#execute "Link to this definition")
:   Executes the SQL statement specified as the argument.

    `snowflake.execute` differs from `Statement.execute`, which you use to execute the statement represented by the
    `Statement` object, rather than executing the method’s argument.

    Parameters:
    :   `sql_command_object`

        > A JSON object (dictionary) that contains the text of the SQL statement to execute and values to bind to that statement.
        > Properties of the `sql_command_object` JSON object include:
        >
        > * `sqlText`: A string containing the SQL statement to execute.
        > * `binds`: An array of values to bind to placeholders in the SQL statement specified by `sqlText`.

    Returns:
    :   A result set in the form of a `ResultSet` object.

    Errors:
    :   Throws a JavaScript Error if:

        * An error, such as a compile error, occurred while executing the query.
        * `sqlText` is missing or contains an empty query text.
        * The statement tries to bind an argument whose data type is not supported. For information about data type
          mapping, see [SQL and JavaScript data type mapping](stored-procedures-javascript.html#label-stored-procedure-data-type-mapping).
          For more information about binding, including additional examples,
          see [Binding variables](stored-procedures-javascript.html#label-stored-procedures-binding-variables).

log(*level*, *message*[, *attributes*])[¶](#log "Link to this definition")
:   Logs a message at the specified severity level, optionally with attributes.

    For more information, see [Logging messages in JavaScript](../logging-tracing/logging-javascript).

    Parameters:
    :   `level`

        > The severity level at which to log the message. You can specify one of the following strings:
        >
        > * `'off'`
        > * `'trace'`
        > * `'debug'`
        > * `'info'`
        > * `'warn'`
        > * `'error'`
        > * `'fatal'`

        `message`

        > The message to log.

        `attributes`

        > Optional. A JSON object with key-value pairs.

    Errors:
    :   Throws a JavaScript error if:

        * `level` is not a string.
        * `level` is not one of the supported `level` values listed above.

    Examples:
    :   ```
        snowflake.log("error", "Error message", {"custom1": "value1", "custom2": "value2"});
        ```

        Copy

setSpanAttribute(*key*, *value*)[¶](#setSpanAttribute "Link to this definition")
:   Sets an attribute for the current span when tracing events.

    For more information about trace events with JavaScript, refer to [Emitting trace events in JavaScript](../logging-tracing/tracing-javascript)

    Parameters:
    :   `key`

        > The attribute’s key.

        `value`

        > The attribute’s value.

    Errors:
    :   Throws a JavaScript error if:

        * Two arguments aren’t specified.
        * `key` is not a string.

    Examples:
    :   Set an attribute whose key is `example.boolean` and whose value is `true`.

        ```
        snowflake.setSpanAttribute("example.boolean", true);
        ```

        Copy

## Object: `Statement`[¶](#object-statement "Link to this heading")

A stored procedure `Statement` object provides the methods for executing a query statement and accessing
metadata (such as column data types) about the statement.

At the time the Statement object is created, the SQL is parsed, and a prepared statement is created.

### Constants[¶](#id1 "Link to this heading")

None.

### Methods[¶](#id2 "Link to this heading")

execute()
:   This method executes the prepared statement stored in this `Statement` object.

    `Statement.execute` differs from `snowflake.execute`, which you use to execute the method’s argument, rather than
    a statement represented by the `Statement` object.

    Parameters:
    :   None because the method uses information that is already stored in the `Statement` object.

    Returns:
    :   A result set in the form of a `ResultSet` object.

    Errors:
    :   Throws a JavaScript Error if the query fails.

    Examples:
    :   See [Working with stored procedures](stored-procedures-usage).

getColumnCount()[¶](#getColumnCount "Link to this definition")
:   This method returns the number of columns in the result set for an executed query. If the query has not yet been executed, this method throws an Error.

    Parameters:
    :   None.

    Returns:
    :   The number of columns.

    Errors:
    :   Throw a JavaScript Error if the statement has not yet been executed (and thus the number of returned columns cannot necessarily
        be determined).

    Examples:
    :   ```
        var column_count = statement.getColumnCount();
        ```

        Copy

getColumnName(*colIdx*)[¶](#getColumnName "Link to this definition")
:   This method returns the name of the specified column.

    Parameters:
    :   The index number of the column (starting from `1`, not `0`).

    Returns:
    :   The name of the column.

    Errors:
    :   Throws a JavaScript Error if:

        * The `Statement` has not yet been executed.
        * No column with the specified index exists.

getColumnScale(*colIdx*)[¶](#getColumnScale "Link to this definition")
:   This method returns the scale of the specified column. The scale is the number of digits after the decimal point. The scale of the column was specified
    in the CREATE TABLE or ALTER TABLE statement. For example:

    > ```
    > CREATE TABLE scale_example  (
    >     n10_4 NUMERIC(10, 4)    // Precision is 10, Scale is 4.
    >     );
    > ```
    >
    > Copy

    Although this method can be called for any data type, it is intended for use with numeric data types.

    Parameters:
    :   The index of the column for which you want the scale (starting from `1`, not `0`).

    Returns:
    :   The scale of the column (for numeric columns); `0` for non-numeric (columns).

    Errors:
    :   Throws a JavaScript Error if:

        * The `Statement` has not yet been executed.
        * No column with the specified index exists.

    Examples:
    :   See [Working with stored procedures](stored-procedures-usage) (search for `getColumnScale()`).

getColumnSqlType(*colIdx|colName*)[¶](#getColumnSqlType "Link to this definition")
:   This method returns the SQL data type of the specified column.

    Parameters:
    :   Either the index number of the column (starting from `1`, not `0`) or the name of the column. (The method is overloaded to accept different
        data types as parameters.)

        The column name should be all uppercase unless double quotes were used in the column name when the table was created (i.e. the case of the column
        name was preserved).

    Returns:
    :   The SQL data type of the column.

    Errors:
    :   Throws a JavaScript Error if:

        * The `Statement` has not yet been executed.
        * No column with the specified name or index exists.

getColumnType(*colIdx|colName*)[¶](#getColumnType "Link to this definition")
:   This method returns the JavaScript data type of the specified column.

    Parameters:
    :   Either the index number of the column (starting from `1`, not `0`) or the name of the column. (The method is overloaded to accept different
        data types as parameters.)

        The column name should be all uppercase unless double quotes were used in the column name when the table was created (i.e. the case of the column
        name was preserved).

    Returns:
    :   The JavaScript data type of the column.

    Errors:
    :   Throws a JavaScript Error if:

        * The `Statement` has not yet been executed.
        * No column with the specified index or name exists.

getNumDuplicateRowsUpdated()[¶](#getNumDuplicateRowsUpdated "Link to this definition")
:   This method returns the number of “duplicate” rows (often called *multi-joined rows*) updated by this Statement.
    (For information about how multi-joined rows are formed, see the
    [Usage Notes and Examples for the UPDATE statement](../../sql-reference/sql/update.html#label-update-statement-usage-notes).)

    Parameters:
    :   None.

    Returns:
    :   A value of type Number that indicates the number of multi-joined rows updated.

    Errors:
    :   Throws a JavaScript error if the statement has not yet been executed.

getNumRowsAffected()[¶](#getNumRowsAffected "Link to this definition")
:   This method returns the number of rows affected (e.g. inserted/updated/deleted) by this Statement.

    If more than one type of change applies (e.g. a [MERGE](../../sql-reference/sql/merge) operation inserted some rows and
    updated others), then the number is the total number of rows affected by all of the changes.

    Parameters:
    :   None.

    Returns:
    :   A value of type Number that indicates the number of rows affected.

    Errors:
    :   Throws a JavaScript error if the statement has not yet been executed.

getNumRowsDeleted()[¶](#getNumRowsDeleted "Link to this definition")
:   This method returns the number of rows deleted by this Statement.

    Parameters:
    :   None.

    Returns:
    :   A value of type Number that indicates the number of rows deleted.

    Errors:
    :   Throws a JavaScript error if the statement has not yet been executed.

getNumRowsInserted()[¶](#getNumRowsInserted "Link to this definition")
:   This method returns the number of rows inserted by this Statement.

    Parameters:
    :   None.

    Returns:
    :   A value of type Number that indicates the number of rows inserted.

    Errors:
    :   Throws a JavaScript error if the statement has not yet been executed.

getNumRowsUpdated()[¶](#getNumRowsUpdated "Link to this definition")
:   This method returns the number of rows updated by this Statement.

    Parameters:
    :   None.

    Returns:
    :   A value of type Number that indicates the number of rows updated.

    Errors:
    :   Throws a JavaScript error if the statement has not yet been executed.

getRowCount()[¶](#getRowCount "Link to this definition")
:   This method returns the number of rows in the result set for an executed query. If the query has not yet been executed, this method throws an Error.

    Parameters:
    :   None.

    Returns:
    :   The number of rows.

    Errors:
    :   Throw a JavaScript Error if the statement has not yet been executed (and thus the number of returned rows cannot be determined).

    Examples:
    :   ```
        var row_count = statement.getRowCount();
        ```

        Copy

getQueryId()[¶](#getQueryId "Link to this definition")
:   This method returns the UUID of the most recent query executed.

    Parameters:
    :   None.

    Returns:
    :   A string containing a UUID, which is the query ID.

    Errors:
    :   If no query has been executed yet by this statement, the method throws the error
        “Statement is not executed yet.”

    Examples:
    :   ```
        var queryId = statement.getQueryId();
        ```

        Copy

getSqlText()[¶](#getSqlText "Link to this definition")
:   This method returns the text of the prepared query in the `Statement` object.

    Parameters:
    :   None.

    Returns:
    :   A string of the prepared query text.

    Errors:
    :   None.

    Examples:
    :   ```
        var queryText = statement.getSqlText();
        ```

        Copy

isColumnNullable(*colIdx*)[¶](#isColumnNullable "Link to this definition")
:   This method returns whether the specified column allows SQL NULL values.

    Parameters:
    :   The index of the column (starting from `1`, not `0`).

    Returns:
    :   `true` if the column allows SQL NULL values; otherwise, `false`.

    Errors:
    :   Throws a JavaScript Error if:

        * The `Statement` has not yet been executed.
        * No column with the specified index exists.

isColumnText(*colIdx*)[¶](#isColumnText "Link to this definition")
:   This method returns true if the column data type is one of the following SQL text data types:

    * CHAR or CHAR(N), as well as their synonyms CHARACTER and CHARACTER(N)
    * VARCHAR or VARCHAR(N)
    * STRING
    * TEXT

    Otherwise, it returns false.

    Parameters:
    :   The index of the column (starting from `1`, not `0`).

    Returns:
    :   `true` if the column data type is one of the SQL text data types; `false` for all other data types.

    Errors:
    :   Throws a JavaScript Error if:

        * The `Statement` has not yet been executed.
        * No column with the specified index exists.

    Note

    The API provides several methods for determining the data type of a column. The first method is described in detail above. The remaining methods have
    the same parameters and errors; the only difference is the return value.

isColumnArray(*colIdx*)[¶](#isColumnArray "Link to this definition")
:   Returns:
    :   `true` if the column data type is ARRAY (for semi-structured data); `false` for all other data types.

isColumnBinary(*colIdx*)[¶](#isColumnBinary "Link to this definition")
:   Returns:
    :   `true` if the column data type is BINARY or VARBINARY; `false` for all other data types.

isColumnBoolean(*colIdx*)[¶](#isColumnBoolean "Link to this definition")
:   Returns:
    :   `true` if the column data type is BOOLEAN; `false` for all other data types.

isColumnDate(*colIdx*)[¶](#isColumnDate "Link to this definition")
:   Returns:
    :   `true` if the column data type is DATE; `false` for all other data types.

isColumnNumber(*colIdx*)[¶](#isColumnNumber "Link to this definition")
:   Returns:
    :   `true` if the column data type is one of the SQL numeric types (NUMBER, NUMERIC, DECIMAL, INT, INTEGER, BIGINT, SMALLINT, TINYINT, BYTEINT,
        FLOAT, FLOAT4, FLOAT8, DOUBLE, DOUBLE PRECISION, or REAL); `false` for all other data types.

isColumnObject(*colIdx*)[¶](#isColumnObject "Link to this definition")
:   Returns:
    :   `true` if the column data type is OBJECT (for semi-structured data); `false` for all other data types.

isColumnTime(*colIdx*)[¶](#isColumnTime "Link to this definition")
:   Returns:
    :   `true` if the column data type is TIME or DATETIME; `false` for all other data types.

isColumnTimestamp(*colIdx*)[¶](#isColumnTimestamp "Link to this definition")
:   Returns:
    :   `true` if the column data type is one of the SQL timestamp types (TIMESTAMP, TIMESTAMP\_LTZ, TIMESTAMP\_NTZ, or TIMESTAMP\_TZ); `false`
        for all other data types, including other date and time data types (DATE, TIME, or DATETIME).

isColumnVariant(*colIdx*)[¶](#isColumnVariant "Link to this definition")
:   Returns:
    :   `true` if the column data type is VARIANT (for semi-structured data); `false` for all other data types.

## Object: `ResultSet`[¶](#object-resultset "Link to this heading")

This object contains the results returned by a query. The results are treated as a set of zero or more rows, each of which contains one or more columns. The term
“set” is not used here in the mathematical sense. In mathematics, a set is unordered, whereas a `ResultSet` has an order.

A `ResultSet` is similar in some ways to the concept of a SQL cursor. For example, you can see one row at a time in a `ResultSet`, just as you can see
one row at a time in a cursor.

Typically, after you retrieve a `ResultSet`, you iterate through it by repeating the following operations:

* Call `next()` to get the next row.
* Retrieve data from the current row by calling methods such as `getColumnValue()`.

If you do not know enough about the data in the `ResultSet` (e.g. you do not know the data type of each column), then you can call other methods that provide information about
the data.

Some of the methods of the `ResultSet` object are similar to the methods of the `Statement` object. For example, both objects have a
`getColumnSqlType(colIdx)` method.

### Constants[¶](#id3 "Link to this heading")

None.

### Methods[¶](#id4 "Link to this heading")

getColumnCount()
:   This method returns the number of columns in this ResultSet.

    Parameters:
    :   None.

    Returns:
    :   A value of type Number that indicates the number of columns.

    Errors:
    :   None.

getColumnSqlType(*colIdx|colName*)
:   This method returns the SQL data type of the specified column.

    Parameters:
    :   Either the index number of the column (starting from `1`, not `0`) or the name of the column. (The method is overloaded to accept different
        data types as parameters.)

        The column name should be all uppercase unless double quotes were used in the column name when the table was created (i.e. the case of the column
        name was preserved).

    Returns:
    :   The SQL data type of the column.

    Errors:
    :   Throws a JavaScript Error if:

        * `ResultSet` is empty or `next()` has not yet been called.
        * No column with the specified index or name exists.

getColumnValue(*colIdx|colName*)[¶](#getColumnValue "Link to this definition")
:   This method returns the value of a column in the current row (i.e. the row most recently retrieved by `next()`).

    Parameters:
    :   Either the index number of the column (starting from `1`, not `0`) or the name of the column. (The method is overloaded to accept different
        data types as parameters.)

        The column name should be all uppercase unless double quotes were used in the column name when the table was created (i.e. the case of the column
        name was preserved).

    Returns:
    :   The value of the specified column.

    Errors:
    :   Throws a JavaScript Error if:

        * `ResultSet` is empty or `next()` has not yet been called.
        * No column with the specified index or name exists.

    Examples:
    :   Convert a row in the database into a JavaScript array:

        > ```
        > var valueArray = [];
        > // For each row...
        > while (myResultSet.next())  {
        >     // Append each column of the current row...
        >     valueArray.push(myResultSet.getColumnValue('MY_COLUMN_NAME1'));
        >     valueArray.push(myResultSet.getColumnValue('MY_COLUMN_NAME2'));
        >     ...
        >     // Do something with the row of data that we retrieved.
        >     f(valueArray);
        >     // Reset the array before getting the next row.
        >     valueArray = [];
        >     }
        > ```
        >
        > Copy

        Also, a column’s value can be accessed as a property of the `ResultSet` object (e.g. `myResultSet.MY_COLUMN_NAME`).

        > ```
        > var valueArray = [];
        > // For each row...
        > while (myResultSet.next())  {
        >     // Append each column of the current row...
        >     valueArray.push(myResultSet.MY_COLUMN_NAME1);
        >     valueArray.push(myResultSet.MY_COLUMN_NAME2);
        >     ...
        >     // Do something with the row of data that we retrieved.
        >     f(valueArray);
        >     // Reset the array before getting the next row.
        >     valueArray = [];
        >     }
        > ```
        >
        > Copy

    Note

    Remember that unless the column name was delimited with double quotes in the CREATE TABLE statement, the column name should be all uppercase in the
    JavaScript code.

getColumnValueAsString(*colIdx|colName*)[¶](#getColumnValueAsString "Link to this definition")
:   This method returns the value of a column as a string, which is useful when you need a column value regardless of the original data type in the table.

    The method is identical to the method `getColumnValue()` except that it returns a string value.

    For more details, see `getColumnValue()`.

getNumRowsAffected()
:   This method returns the number of rows affected (e.g. inserted/updated/deleted) by the Statement that generated this ResultSet.

    If more than one type of change applies (e.g. a [MERGE](../../sql-reference/sql/merge) operation inserted some rows and
    updated others), then the number is the total number of rows affected by all of the changes.

    Parameters:
    :   None.

    Returns:
    :   A value of type Number that indicates the number of rows affected.

    Errors:
    :   None.

getQueryId()
:   This method returns the UUID of the most recent query executed.

    Parameters:
    :   None.

    Returns:
    :   A string containing a UUID, which is the query ID.

    Examples:
    :   ```
        var queryId = resultSet.getQueryId();
        ```

        Copy

getRowCount()
:   This method returns the number of rows in this ResultSet. (This is the total number of rows, not the number of rows that
    haven’t been consumed yet.)

    Parameters:
    :   None.

    Returns:
    :   A value of type Number that indicates the number of rows.

    Errors:
    :   None.

next()[¶](#next "Link to this definition")
:   This method gets the next row in the `ResultSet` and makes it available for access.

    This method does not return the new data row. Instead, it makes the row available so that you can call methods such as `ResultSet.getColumnValue()` to
    retrieve the data.

    Note that you must call `next()` for each row in the result set, including the first row.

    Parameters:
    :   None.

    Returns:
    :   `true` if it retrieved a row and `false` if there are no more rows to retrieve.

        Thus, you can iterate through `ResultSet` until `next()` returns false.

    Errors:
    :   None.

## Object: `SfDate`[¶](#object-sfdate "Link to this heading")

JavaScript does not have a native data type that corresponds to the Snowflake SQL data types
TIMESTAMP\_LTZ, TIMESTAMP\_NTZ, and TIMESTAMP\_TZ. When you retrieve a value of type TIMESTAMP from the database
and want to store it as a JavaScript variable (for example, copy the value from a ResultSet to a JavaScript variable),
use the Snowflake-defined JavaScript data type `SfDate`.
The `SfDate` (“SnowFlake Date”) data type is an extension of the JavaScript date data type.
`SfDate` has extra methods, which are documented below.

### Constants[¶](#id5 "Link to this heading")

None.

### Methods[¶](#id6 "Link to this heading")

Unless otherwise specified, the examples below assume UTC time zone.

getEpochSeconds()[¶](#getEpochSeconds "Link to this definition")
:   This method returns the number of seconds since the beginning of “the epoch” (midnight January 1, 1970).

    Parameters:
    :   None.

    Returns:
    :   The number of seconds between midnight January 1, 1970 and the timestamp stored in the variable.

    Examples:
    :   Create the stored procedure:

        > ```
        > CREATE OR REPLACE PROCEDURE test_get_epoch_seconds(TSV VARCHAR)
        >     RETURNS FLOAT
        >     LANGUAGE JAVASCRIPT
        >     AS
        >     $$
        >     var sql_command = "SELECT '" + TSV + "'::TIMESTAMP_NTZ;";
        >     var stmt = snowflake.createStatement( {sqlText: sql_command} );
        >     var resultSet = stmt.execute();
        >     resultSet.next();
        >     var my_sfDate = resultSet.getColumnValue(1);
        >     return my_sfDate.getEpochSeconds();
        >     $$
        >     ;
        > ```
        >
        > Copy

        Pass the procedure different timestamps and retrieve the number of seconds since the epoch for each timestamp.

        > ```
        > CALL test_get_epoch_seconds('1970-01-01 00:00:00.000000000');
        > +------------------------+
        > | TEST_GET_EPOCH_SECONDS |
        > |------------------------|
        > |                      0 |
        > +------------------------+
        > ```
        >
        > Copy
        >
        > ```
        > CALL test_get_epoch_seconds('1970-01-01 00:00:01.987654321');
        > +------------------------+
        > | TEST_GET_EPOCH_SECONDS |
        > |------------------------|
        > |                      1 |
        > +------------------------+
        > ```
        >
        > Copy
        >
        > ```
        > CALL test_get_epoch_seconds('1971-01-01 00:00:00');
        > +------------------------+
        > | TEST_GET_EPOCH_SECONDS |
        > |------------------------|
        > |               31536000 |
        > +------------------------+
        > ```
        >
        > Copy

getNanoSeconds()[¶](#getNanoSeconds "Link to this definition")
:   This method returns the value of the nanoseconds field of the object. Note that this is just the fractional
    seconds, not the nanoseconds since the beginning of the epoch. Thus the value is always between 0 and 999999999.

    Parameters:
    :   None.

    Returns:
    :   The number of nanoseconds.

    Examples:
    :   Create the stored procedure:

        > ```
        > CREATE OR REPLACE PROCEDURE test_get_nano_seconds2(TSV VARCHAR)
        >     RETURNS FLOAT
        >     LANGUAGE JAVASCRIPT
        >     AS
        >     $$
        >     var sql_command = "SELECT '" + TSV + "'::TIMESTAMP_NTZ;";
        >     var stmt = snowflake.createStatement( {sqlText: sql_command} );
        >     var resultSet = stmt.execute();
        >     resultSet.next();
        >     var my_sfDate = resultSet.getColumnValue(1);
        >     return my_sfDate.getNanoSeconds();
        >     $$
        >     ;
        > -- Should be 0 nanoseconds.
        > -- (> SNIPPET_TAG=query_03_01
        > CALL test_get_nano_seconds2('1970-01-01 00:00:00.000000000');
        > ```
        >
        > Copy

        Pass the procedure different timestamps and retrieve the number of nanoseconds from each.

        > ```
        > CALL test_get_nano_seconds2('1970-01-01 00:00:00.000000000');
        > +------------------------+
        > | TEST_GET_NANO_SECONDS2 |
        > |------------------------|
        > |                      0 |
        > +------------------------+
        > ```
        >
        > Copy
        >
        > ```
        > CALL test_get_nano_seconds2('1970-01-01 00:00:01.987654321');
        > +------------------------+
        > | TEST_GET_NANO_SECONDS2 |
        > |------------------------|
        > |              987654321 |
        > +------------------------+
        > ```
        >
        > Copy
        >
        > ```
        > CALL test_get_nano_seconds2('1971-01-01 00:00:00.000123456');
        > +------------------------+
        > | TEST_GET_NANO_SECONDS2 |
        > |------------------------|
        > |                 123456 |
        > +------------------------+
        > ```
        >
        > Copy

getScale()[¶](#getScale "Link to this definition")
:   This method returns the precision of the data type, i.e. the number of digits after the decimal point.
    For example, the precision of TIMESTAMP\_NTZ(3) is 3 (milliseconds). The precision of TIMESTAMP\_NTZ(0) is 0 (no
    fractional seconds). The precision of TIMESTAMP\_NTZ is 9 (nanoseconds).

    The minimum is 0. The maximum is 9 (precision is to 1 nanosecond). The default precision is 9.

    Parameters:
    :   None.

    Returns:
    :   The number of digits after the decimal place (number of digits in the fractional seconds field).

    Examples:
    :   Create the stored procedure:

        > ```
        > CREATE OR REPLACE PROCEDURE test_get_scale(TSV VARCHAR, SCALE VARCHAR)
        >     RETURNS FLOAT
        >     LANGUAGE JAVASCRIPT
        >     AS
        >     $$
        >     var sql_command = "SELECT '" + TSV + "'::TIMESTAMP_NTZ(" + SCALE + ");";
        >     var stmt = snowflake.createStatement( {sqlText: sql_command} );
        >     var resultSet = stmt.execute();
        >     resultSet.next();
        >     var my_sfDate = resultSet.getColumnValue(1);
        >     return my_sfDate.getScale();
        >     $$
        >     ;
        >
        > -- Should be 0.
        > -- (> SNIPPET_TAG=query_04_01
        > CALL test_get_scale('1970-01-01 00:00:00', '0');
        > ```
        >
        > Copy

        In this example, the timestamp is defined as TIMESTAMP\_NTZ(0), so the precision is 0.

        > ```
        > CALL test_get_scale('1970-01-01 00:00:00', '0');
        > +----------------+
        > | TEST_GET_SCALE |
        > |----------------|
        > |              0 |
        > +----------------+
        > ```
        >
        > Copy

        In this example, the timestamp is defined as TIMESTAMP\_NTZ(2), so the precision is 2.

        > ```
        > CALL test_get_scale('1970-01-01 00:00:01.123', '2');
        > +----------------+
        > | TEST_GET_SCALE |
        > |----------------|
        > |              2 |
        > +----------------+
        > ```
        >
        > Copy

        In this example, the timestamp is defined as TIMESTAMP\_NTZ, so the precision is 9, which is the default.

        > ```
        > CALL test_get_scale('1971-01-01 00:00:00.000123456', '9');
        > +----------------+
        > | TEST_GET_SCALE |
        > |----------------|
        > |              9 |
        > +----------------+
        > ```
        >
        > Copy

getTimezone()[¶](#getTimezone "Link to this definition")
:   This method returns the timezone as the number of minutes before or after UTC.

    Parameters:
    :   None.

    Returns:
    :   The timezone as a number of minutes before or after UTC.

    Examples:
    :   Create the stored procedure:

        > ```
        > CREATE OR REPLACE PROCEDURE test_get_Timezone(TSV VARCHAR)
        >     RETURNS FLOAT
        >     LANGUAGE JAVASCRIPT
        >     AS
        >     $$
        >     var sql_command = "SELECT '" + TSV + "'::TIMESTAMP_TZ;";
        >     var stmt = snowflake.createStatement( {sqlText: sql_command} );
        >     var resultSet = stmt.execute();
        >     resultSet.next();
        >     var my_sfDate = resultSet.getColumnValue(1);
        >     return my_sfDate.getTimezone();
        >     $$
        >     ;
        > ```
        >
        > Copy

        In this example, the time zone is 8 hours (480 minutes) behind UTC.

        > ```
        > CALL test_get_timezone('1970-01-01 00:00:01-08:00');
        > +-------------------+
        > | TEST_GET_TIMEZONE |
        > |-------------------|
        > |              -480 |
        > +-------------------+
        > ```
        >
        > Copy

        In this example, the time zone is 11 hours (660 minutes) ahead of UTC.

        > ```
        > CALL test_get_timezone('1971-01-01 00:00:00.000123456+11:00');
        > +-------------------+
        > | TEST_GET_TIMEZONE |
        > |-------------------|
        > |               660 |
        > +-------------------+
        > ```
        >
        > Copy

toString()[¶](#toString "Link to this definition")
:   Parameters:
    :   None.

    Returns:
    :   This method returns a string representation of the timestamp.

    Examples:
    :   This shows a simple example of creating an `SfDate` and calling its `toString` method:

        > ```
        > CREATE OR REPLACE PROCEDURE test_toString(TSV VARCHAR)
        >     RETURNS VARIANT
        >     LANGUAGE JAVASCRIPT
        >     AS
        >     $$
        >     var sql_command = "SELECT '" + TSV + "'::TIMESTAMP_TZ;";
        >     var stmt = snowflake.createStatement( {sqlText: sql_command} );
        >     var resultSet = stmt.execute();
        >     resultSet.next();
        >     var my_sfDate = resultSet.getColumnValue(1);
        >     return my_sfDate.toString();
        >     $$
        >     ;
        > ```
        >
        > Copy
        >
        > ```
        > CALL test_toString('1970-01-02 03:04:05');
        > +------------------------------------------------------------------+
        > | TEST_TOSTRING                                                    |
        > |------------------------------------------------------------------|
        > | "Fri Jan 02 1970 03:04:05 GMT+0000 (Coordinated Universal Time)" |
        > +------------------------------------------------------------------+
        > ```
        >
        > Copy

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

1. [Object: snowflake](#object-snowflake)
2. [Object: Statement](#object-statement)
3. [Object: ResultSet](#object-resultset)
4. [Object: SfDate](#object-sfdate)

Related content

1. [Stored procedures overview](/developer-guide/stored-procedure/stored-procedures-overview)
2. [Working with stored procedures](/developer-guide/stored-procedure/stored-procedures-usage)
3. [Introduction to JavaScript UDFs](/developer-guide/stored-procedure/../udf/javascript/udf-javascript-introduction)