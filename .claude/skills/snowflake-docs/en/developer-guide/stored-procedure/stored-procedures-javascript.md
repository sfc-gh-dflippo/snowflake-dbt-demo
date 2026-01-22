---
auto_generated: true
description: This topic explains how to write the JavaScript code for a stored procedure.
last_scraped: '2026-01-14T16:55:12.724720+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/developer-guide/stored-procedure/stored-procedures-javascript
title: Writing stored procedures in JavaScript | Snowflake Documentation
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

    * [Function or procedure?](../stored-procedures-vs-udfs.md)
    * [Guidelines](../udf-stored-procedure-guidelines.md)
    * [Stored procedures](stored-procedures-overview.md)

      + [Usage](stored-procedures-usage.md)
      + [Caller and owner rights](stored-procedures-rights.md)
      + [Creating](stored-procedures-creating.md)
      + [Calling](stored-procedures-calling.md)
      + [Selecting from](stored-procedures-selecting-from.md)
      + [Passing in references](stored-procedures-calling-references.md)
      + Handler writing
      + [Java](java/procedure-java-overview.md)
      + [Javascript](stored-procedures-javascript.md)

        - [API](stored-procedures-api.md)
      + [Python](python/procedure-python-overview.md)
      + [Scala](scala/procedure-scala-overview.md)
      + [Snowflake Scripting](stored-procedures-snowflake-scripting.md)
    * [User-defined functions](../udf/udf-overview.md)
    * [Packaging handler code](../udf-stored-procedure-building.md)
    * [External network access](../external-network-access/external-network-access-overview.md)
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
27. [Snowflake Scripting Developer Guide](../snowflake-scripting/index.md)
28. Tools
29. [Snowflake CLI](../snowflake-cli/index.md)
30. [Git](../git/git-overview.md)
31. Drivers
32. [Overview](../drivers.md)
33. [Considerations when drivers reuse sessions](../driver-connections.md)
34. [Scala versions](../scala-version-differences.md)
35. Reference
36. [API Reference](../../api-reference.md)

[Developer](../../developer.md)[Functions and procedures](../extensibility.md)[Stored procedures](stored-procedures-overview.md)Javascript

# Writing stored procedures in JavaScript[¶](#writing-stored-procedures-in-javascript "Link to this heading")

This topic explains how to write the JavaScript code for a stored procedure.

Note

To both create and call an anonymous procedure, use [CALL (with anonymous procedure)](../../sql-reference/sql/call-with). Creating and calling an anonymous procedure does
not require a role with CREATE PROCEDURE schema privileges.

You can capture log and trace data as your handler code executes. For more information, refer to
[Logging, tracing, and metrics](../logging-tracing/logging-tracing-overview).

## Understanding the JavaScript API[¶](#understanding-the-javascript-api "Link to this heading")

The JavaScript API for stored procedures is similar to, but not identical to, the APIs in Snowflake connectors and drivers
(Node.js, JDBC, Python, etc.).

The API enables you to perform operations such as:

* Execute a SQL statement.
* Retrieve the results of a query (i.e. a result set).
* Retrieve metadata about the result set (number of columns, data types of the columns, etc.).

These operations are carried out by calling methods on the following objects:

* `snowflake`, which has methods to create a `Statement` object and execute a SQL command.
* `Statement`, which helps you execute prepared statements and access metadata for those prepared statements,
  and allows you to get back a ResultSet object.
* `ResultSet`, which holds the results of a query (e.g. the rows of data retrieved for a SELECT statement).
* `SfDate`, which is an extension of JavaScript Date (with additional methods) and serves as a return type for
  the Snowflake SQL data types TIMESTAMP\_LTZ, TIMESTAMP\_NTZ, and TIMESTAMP\_TZ.

These objects are described in detail in the [JavaScript stored procedures API](stored-procedures-api).

A typical stored procedure contains code similar to the following pseudo-code:

> ```
> var my_sql_command1 = "delete from history_table where event_year < 2016";
> var statement1 = snowflake.createStatement(my_sql_command1);
> statement1.execute();
>
> var my_sql_command2 = "delete from log_table where event_year < 2016";
> var statement2 = snowflake.createStatement(my_sql_command2);
> statement2.execute();
> ```
>
> Copy

This code uses an object named `snowflake`, which is a special object
that exists without being declared. The object is provided inside the context of each stored
procedure and exposes the API to allow you to interact with the server.

The other variables (e.g. `statement1`) are created with JavaScript `var` statements. For example:

> ```
> var statement1 = ...;
> ```
>
> Copy

As shown in the code sample above, the `snowflake` object allows you
to create a `Statement` object by calling one of the methods in the API.

Here’s an example that retrieves a `ResultSet` and iterates through it:

> ```
> CREATE OR REPLACE PROCEDURE read_result_set()
>   RETURNS FLOAT NOT NULL
>   LANGUAGE JAVASCRIPT
>   AS     
>   $$  
>     var my_sql_command = "select * from table1";
>     var statement1 = snowflake.createStatement( {sqlText: my_sql_command} );
>     var result_set1 = statement1.execute();
>     // Loop through the results, processing one row at a time... 
>     while (result_set1.next())  {
>        var column1 = result_set1.getColumnValue(1);
>        var column2 = result_set1.getColumnValue(2);
>        // Do something with the retrieved values...
>        }
>   return 0.0; // Replace with something more useful.
>   $$
>   ;
> ```
>
> Copy

The [Examples](#label-stored-procedure-examples) section (at the end of this topic) provides additional examples
that exercise each of the objects, and many of the methods, in the stored procedure JavaScript API.

## SQL and JavaScript data type mapping[¶](#sql-and-javascript-data-type-mapping "Link to this heading")

When calling, using, and getting values back from stored procedures, you often need to convert from a Snowflake SQL
data type to a JavaScript data type or vice versa.

SQL to JavaScript conversion can occur when:

* Calling a stored procedure with an argument. The argument is a SQL data type; when it is stored inside a
  JavaScript variable inside the stored procedure, it must be converted.
* When retrieving a value from a ResultSet object into a JavaScript variable. The ResultSet holds the value as a SQL
  data type, and the JavaScript variable must store the value as one of the JavaScript data types.

JavaScript to SQL conversion can occur when:

* Returning a value from the stored procedure. The `return` statement typically contains a JavaScript
  variable that must be converted to a SQL data type.
* When dynamically constructing a SQL statement that uses a value in a JavaScript variable.
* When binding a JavaScript variable’s value to a prepared statement.

For more information about how Snowflake maps JavaScript and SQL data types, see [SQL-JavaScript Data Type Mappings](../udf-stored-procedure-data-type-mapping.html#label-javascript-supported-snowpark-types).

## General tips[¶](#general-tips "Link to this heading")

### Line continuation[¶](#line-continuation "Link to this heading")

SQL statements can be quite long, and it is not always practical to fit them on a single line. JavaScript treats a
newline as the end of a statement. If you want to split a long SQL statement across multiple lines, you can use
the usual JavaScript techniques for handling long strings, including:

* Put a backslash (line continuation character) immediately prior to the end of the line. For example:

  ```
  var sql_command = "SELECT * \
                         FROM table1;";
  ```

  Copy
* Use backticks (single backquotes) rather than double quotes around the string. For example:

  ```
  var sql_command = `SELECT *
                         FROM table1;`;
  ```

  Copy
* Accumulate the string. For example:

  ```
  var sql_command = "SELECT col1, col2"
  sql_command += "     FROM table1"
  sql_command += "     WHERE col1 >= 100"
  sql_command += "     ORDER BY col2;"
  ```

  Copy

## JavaScript stored procedure considerations[¶](#javascript-stored-procedure-considerations "Link to this heading")

### JavaScript Number Range[¶](#javascript-number-range "Link to this heading")

The range for numbers with precision intact is from

> -(2^53 -1)

to

> (2^53 -1)

The range of valid values in Snowflake NUMBER(p, s) and DOUBLE data types is larger. Retrieving a value from Snowflake
and storing it in a JavaScript numeric variable can result in loss of precision. For example:

> ```
> CREATE OR REPLACE FUNCTION num_test(a double)
>   RETURNS string
>   LANGUAGE JAVASCRIPT
> AS
> $$
>   return A;
> $$
> ;
> ```
>
> Copy
>
> ```
> select hash(1) AS a, 
>        num_test(hash(1)) AS b, 
>        a - b;
> +----------------------+----------------------+------------+
> |                    A | B                    |      A - B |
> |----------------------+----------------------+------------|
> | -4730168494964875235 | -4730168494964875000 | -235.00000 |
> +----------------------+----------------------+------------+
> ```
>
> Copy

The first two columns should match, and the third should contain 0.0.

The problem applies to JavaScript user-defined functions (UDFs) and stored procedures.

If you experience the problem in stored procedures when using `getColumnValue()`, you might be able to avoid the
problem by retrieving a value as a string, e.g. with:

```
getColumnValueAsString()
```

Copy

You can then return the string from the stored procedure, and cast the string to a numeric data type in SQL.

### JavaScript error handling[¶](#javascript-error-handling "Link to this heading")

Because a stored procedure is written in JavaScript, it can use JavaScript’s try/catch syntax.

The stored procedure can throw a pre-defined exception or a custom exception. A simple example of throwing a
custom exception is [here](#label-stored-procedure-error-handling).

You can execute your SQL statements inside a try block. If an error occurs, then your catch block can roll back all of
the statements (if you put the statements in a transaction). The Examples section contains an example of
[rolling back a transaction in a stored procedure](#label-example-using-transaction-in-stored-procedures).

### Restrictions on stored procedures[¶](#restrictions-on-stored-procedures "Link to this heading")

Stored procedures have the following restrictions:

* The JavaScript code cannot call the JavaScript `eval()` function.
* JavaScript stored procedures support access to the standard JavaScript library. Note that this excludes many objects and methods
  typically provided by browsers. There is no mechanism to import, include, or call additional libraries.
  Allowing 3rd-party libraries could create security holes.
* JavaScript code is executed within a restricted engine, preventing system calls from the JavaScript
  context (e.g. no network and disk access), and constraining the system resources available to the engine, specifically memory.

### Case-sensitivity in JavaScript arguments[¶](#case-sensitivity-in-javascript-arguments "Link to this heading")

Argument names are case-insensitive in the SQL portion of the stored procedure code, but are
case-sensitive in the JavaScript portion.

For stored procedures (and UDFs) that use JavaScript, identifiers (such as
argument names) in the SQL portion of the statement are converted to uppercase automatically (unless you delimit the
identifier with double quotes), while argument names in the JavaScript portion
will be left in their original case. This can cause your stored procedure to
fail without returning an explicit error message because the arguments aren’t seen.

Here is an example of a stored procedure in which the name of an argument in the
JavaScript code does not match the name of the argument in the SQL code merely
because the case will be different:

In the example below, the first assignment statement is incorrect because the name `argument1` is in lower case.

```
CREATE PROCEDURE f(argument1 VARCHAR)
RETURNS VARCHAR
LANGUAGE JAVASCRIPT
AS
$$
var local_variable1 = argument1;  // Incorrect
var local_variable2 = ARGUMENT1;  // Correct
$$;
```

Copy

Using uppercase identifiers (especially argument names) consistently across
your SQL statements and JavaScript code tends to reduce silent errors.

### JavaScript delimiters[¶](#javascript-delimiters "Link to this heading")

The JavaScript portion of the stored procedure code must be enclosed within either single quotes `'` or
double dollar signs `$$`.

Using `$$` makes it easier to handle JavaScript code that contains single quotes without “escaping” those quotes.

### Overloading stored procedure names[¶](#overloading-stored-procedure-names "Link to this heading")

For information about overloading and naming conventions, see [Naming and overloading procedures and UDFs](../udf-stored-procedure-naming-conventions).

### Binding variables[¶](#binding-variables "Link to this heading")

[Binding](../../sql-reference/bind-variables) a variable to a SQL statement allows you to use the value of
the variable in the statement.

You can bind NULL values as well as non-NULL values.

The data type of the variable should be appropriate for the use of the value in the SQL statement. Currently, only
JavaScript variables of type number, string, and [SfDate](stored-procedures-api.html#label-sfdate) can be bound. (For details about the
mapping between SQL data types and JavaScript data types, see [SQL and JavaScript data type mapping](#label-stored-procedure-data-type-mapping).)

Here is a short example of binding:

```
var stmt = snowflake.createStatement(
  {
  sqlText: "INSERT INTO table2 (col1, col2) VALUES (?, ?);",
  binds:["LiteralValue1", variable2]
  }
);
```

Copy

Here is a more complete example. This example binds TIMESTAMP information. Because direct binding of SQL TIMESTAMP
data is not supported, this example passes the timestamp as a VARCHAR, then binds that to the statement. Note that
the SQL statement itself converts the VARCHAR to a TIMESTAMP by calling the TO\_TIMESTAMP() function:

> This simple function returns TRUE if the specified timestamp is prior to now, and FALSE otherwise.
>
> ```
> CREATE OR REPLACE PROCEDURE right_bind(TIMESTAMP_VALUE VARCHAR)
> RETURNS BOOLEAN
> LANGUAGE JAVASCRIPT
> AS
> $$
> var cmd = "SELECT CURRENT_DATE() > TO_TIMESTAMP(:1, 'YYYY-MM-DD HH24:MI:SS')";
> var stmt = snowflake.createStatement(
>           {
>           sqlText: cmd,
>           binds: [TIMESTAMP_VALUE]
>           }
>           );
> var result1 = stmt.execute();
> result1.next();
> return result1.getColumnValue(1);
> $$
> ;
> ```
>
> Copy
>
> ```
> CALL right_bind('2019-09-16 01:02:03');
> +------------+
> | RIGHT_BIND |
> |------------|
> | True       |
> +------------+
> ```
>
> Copy

This shows how to bind a VARCHAR, a TIMESTAMP\_LTZ, and other data types to an `INSERT` statement. The
TIMESTAMP\_LTZ binds an [SfDate](stored-procedures-api.html#label-sfdate) variable that is created inside the stored procedure.

> Create a table.
>
> ```
> CREATE TABLE table1 (v VARCHAR,
>                      ts1 TIMESTAMP_LTZ(9), 
>                      int1 INTEGER,
>                      float1 FLOAT,
>                      numeric1 NUMERIC(10,9),
>                      ts_ntz1 TIMESTAMP_NTZ,
>                      date1 DATE,
>                      time1 TIME
>                      );
> ```
>
> Copy
>
> Create a stored procedure. This procedure accepts a `VARCHAR`, and converts the VARCHAR to a `TIMESTAMP_LTZ`
> by using SQL. The procedure then retrieves the converted value from a ResultSet. The value is stored in a JavaScript
> variable of type [SfDate](stored-procedures-api.html#label-sfdate). The stored procedure then binds both the original `VARCHAR` and the `TIMESTAMP_LTZ` to an `INSERT` statement. This also demonstrates binding of JavaScript numeric data.
>
> ```
> CREATE OR REPLACE PROCEDURE string_to_timestamp_ltz(TSV VARCHAR) 
> RETURNS TIMESTAMP_LTZ 
> LANGUAGE JAVASCRIPT 
> AS 
> $$ 
>     // Convert the input varchar to a TIMESTAMP_LTZ.
>     var sql_command = "SELECT '" + TSV + "'::TIMESTAMP_LTZ;"; 
>     var stmt = snowflake.createStatement( {sqlText: sql_command} ); 
>     var resultSet = stmt.execute(); 
>     resultSet.next(); 
>     // Retrieve the TIMESTAMP_LTZ and store it in an SfDate variable.
>     var my_sfDate = resultSet.getColumnValue(1); 
>
>     f = 3.1415926;
>
>     // Specify that we'd like position-based binding.
>     sql_command = `INSERT INTO table1 VALUES(:1, :2, :3, :4, :5, :6, :7, :8);` 
>     // Bind a VARCHAR, a TIMESTAMP_LTZ, a numeric to our INSERT statement.
>     result = snowflake.execute(
>         { 
>         sqlText: sql_command, 
>         binds: [TSV, my_sfDate, f, f, f, my_sfDate, my_sfDate, '12:30:00.123' ] 
>         }
>         ); 
>
>     return my_sfDate; 
> $$ ;
> ```
>
> Copy
>
> Call the procedure.
>
> ```
> CALL string_to_timestamp_ltz('2008-11-18 16:00:00');
> +-------------------------------+
> | STRING_TO_TIMESTAMP_LTZ       |
> |-------------------------------|
> | 2008-11-18 16:00:00.000 -0800 |
> +-------------------------------+
> ```
>
> Copy
>
> Verify that the row was inserted.
>
> ```
> SELECT * FROM table1;
> +---------------------+-------------------------------+------+----------+-------------+-------------------------+------------+----------+
> | V                   | TS1                           | INT1 |   FLOAT1 |    NUMERIC1 | TS_NTZ1                 | DATE1      | TIME1    |
> |---------------------+-------------------------------+------+----------+-------------+-------------------------+------------+----------|
> | 2008-11-18 16:00:00 | 2008-11-18 16:00:00.000 -0800 |    3 | 3.141593 | 3.141593000 | 2008-11-18 16:00:00.000 | 2008-11-18 | 12:30:00 |
> +---------------------+-------------------------------+------+----------+-------------+-------------------------+------------+----------+
> ```
>
> Copy

For additional examples of binding data in JavaScript, see [Binding statement parameters](../node-js/nodejs-driver-execute.html#label-nodejs-binding).

### Code requirements[¶](#code-requirements "Link to this heading")

The JavaScript code must define a single literal JavaScript object for the stored procedure to be valid.

If the JavaScript code does not meet this requirement, the stored procedure will be created; however, it will fail when called.

### Code size[¶](#code-size "Link to this heading")

Snowflake limits the maximum size of the JavaScript source code in the body of a JavaScript stored procedure. Snowflake recommends
limiting the size to 100 KB. (The code is stored in a compressed form, and the exact limit depends on the compressibility of the
code.)

### Runtime errors[¶](#runtime-errors "Link to this heading")

Most errors in stored procedures show up at runtime because the JavaScript
code is interpreted at the time that the stored procedure runs rather than when
the stored procedure is created.

### Support for dynamic SQL[¶](#support-for-dynamic-sql "Link to this heading")

Stored procedures can be used to dynamically construct SQL statements. For example,
you could build a SQL command string that contains a mix of pre-configured
SQL and user inputs (e.g. a user’s account number).

For examples, see [Dynamically creating a SQL statement](#label-example-of-dynamic-sql-in-stored-procedure) and the [Examples](#label-stored-procedure-examples) section.

### Synchronous API[¶](#synchronous-api "Link to this heading")

The API for Snowflake stored procedures is synchronous. Within a stored
procedure, you can run only one thread at a time.

Note that this is different from the rule for the JavaScript executing with the Node.js
connector, which allows you to run asynchronous threads.

## Examples[¶](#examples "Link to this heading")

### Basic examples[¶](#basic-examples "Link to this heading")

The following example shows the basic syntax of creating and calling a stored procedure. It doesn’t execute any SQL
or procedural code. However, it provides a starting point for more realistic examples later:

> ```
> CREATE OR REPLACE PROCEDURE sp_pi()
>     RETURNS FLOAT NOT NULL
>     LANGUAGE JAVASCRIPT
>     AS
>     $$
>     return 3.1415926;
>     $$
>     ;
> ```
>
> Copy
>
> Note that the `$$` delimiter marks the beginning and end of the JavaScript code.
>
> Now call the procedure you just created:
>
> ```
> CALL sp_pi();
> +-----------+
> |     SP_PI |
> |-----------|
> | 3.1415926 |
> +-----------+
> ```
>
> Copy

The following example illustrates how to execute a SQL statement inside a stored procedure:

1. Create a table:

   > ```
   > CREATE TABLE stproc_test_table1 (num_col1 numeric(14,7));
   > ```
   >
   > Copy
2. Create a stored procedure. This inserts a row into
   an existing table named `stproc_test_table1` and returns the value “Succeeded.”.
   The returned value is not particularly useful from a SQL perspective, but it
   allows you to return status information (e.g. “Succeeded.” or “Failed.”) to the user.

   > ```
   > CREATE OR REPLACE PROCEDURE stproc1(FLOAT_PARAM1 FLOAT)
   >     RETURNS STRING
   >     LANGUAGE JAVASCRIPT
   >     STRICT
   >     EXECUTE AS OWNER
   >     AS
   >     $$
   >     var sql_command = 
   >      "INSERT INTO stproc_test_table1 (num_col1) VALUES (" + FLOAT_PARAM1 + ")";
   >     try {
   >         snowflake.execute (
   >             {sqlText: sql_command}
   >             );
   >         return "Succeeded.";   // Return a success/error indicator.
   >         }
   >     catch (err)  {
   >         return "Failed: " + err;   // Return a success/error indicator.
   >         }
   >     $$
   >     ;
   > ```
   >
   > Copy
3. Call the stored procedure:

   > ```
   > call stproc1(5.14::FLOAT);
   > +------------+
   > | STPROC1    |
   > |------------|
   > | Succeeded. |
   > +------------+
   > ```
   >
   > Copy
4. Confirm that the stored procedure inserted the row:

   > ```
   > select * from stproc_test_table1;
   > +-----------+
   > |  NUM_COL1 |
   > |-----------|
   > | 5.1400000 |
   > +-----------+
   > ```
   >
   > Copy

The following example retrieves a result:

1. Create a procedure to count the number of rows in a table (equivalent to `select count(*) from table`):

   > ```
   > CREATE OR REPLACE PROCEDURE get_row_count(table_name VARCHAR)
   >   RETURNS FLOAT NOT NULL
   >   LANGUAGE JAVASCRIPT
   >   AS
   >   $$
   >   var row_count = 0;
   >   // Dynamically compose the SQL statement to execute.
   >   var sql_command = "select count(*) from " + TABLE_NAME;
   >   // Run the statement.
   >   var stmt = snowflake.createStatement(
   >          {
   >          sqlText: sql_command
   >          }
   >       );
   >   var res = stmt.execute();
   >   // Get back the row count. Specifically, ...
   >   // ... get the first (and in this case only) row from the result set ...
   >   res.next();
   >   // ... and then get the returned value, which in this case is the number of
   >   // rows in the table.
   >   row_count = res.getColumnValue(1);
   >   return row_count;
   >   $$
   >   ;
   > ```
   >
   > Copy
2. Ask the stored procedure how many rows are in the table:

   > ```
   > call get_row_count('stproc_test_table1');
   > +---------------+
   > | GET_ROW_COUNT |
   > |---------------|
   > |             3 |
   > +---------------+
   > ```
   >
   > Copy
3. Check independently that you got the right number:

   > ```
   > select count(*) from stproc_test_table1;
   > +----------+
   > | COUNT(*) |
   > |----------|
   > |        3 |
   > +----------+
   > ```
   >
   > Copy

### Recursive stored procedure example[¶](#recursive-stored-procedure-example "Link to this heading")

The following example shows a basic, but not particularly realistic, recursive stored procedure:

> ```
> create or replace table stproc_test_table2 (col1 FLOAT);
> ```
>
> Copy
>
> ```
> create or replace procedure recursive_stproc(counter FLOAT)
>     returns varchar not null
>     language javascript
>     as
>     -- "$$" is the delimiter that shows the beginning and end of the stored proc.
>     $$
>     var counter1 = COUNTER;
>     var returned_value = "";
>     var accumulator = "";
>     var stmt = snowflake.createStatement(
>         {
>         sqlText: "INSERT INTO stproc_test_table2 (col1) VALUES (?);",
>         binds:[counter1]
>         }
>         );
>     var res = stmt.execute();
>     if (COUNTER > 0)
>         {
>         stmt = snowflake.createStatement(
>             {
>             sqlText: "call recursive_stproc (?);",
>             binds:[counter1 - 1]
>             }
>             );
>         res = stmt.execute();
>         res.next();
>         returned_value = res.getColumnValue(1);
>         }
>     accumulator = accumulator + counter1 + ":" + returned_value;
>     return accumulator;
>     $$
>     ;
> ```
>
> Copy
>
> ```
> call recursive_stproc(4.0::FLOAT);
> +------------------+
> | RECURSIVE_STPROC |
> |------------------|
> | 4:3:2:1:0:       |
> +------------------+
> ```
>
> Copy
>
> ```
> SELECT * 
>     FROM stproc_test_table2
>     ORDER BY col1;
> +------+
> | COL1 |
> |------|
> |    0 |
> |    1 |
> |    2 |
> |    3 |
> |    4 |
> +------+
> ```
>
> Copy

### Dynamically creating a SQL statement[¶](#dynamically-creating-a-sql-statement "Link to this heading")

The following example shows how to dynamically create a SQL statement:

Note

As stated in [SQL injection](stored-procedures-usage.html#label-sql-injection) (in this topic), be careful to guard against attacks when using dynamic SQL.

1. Create the stored procedure. This procedure allows you to pass the name of a table and get the number of rows in
   that table (equivalent to `select count(*) from table_name`):

   > ```
   > create or replace procedure get_row_count(table_name VARCHAR)
   >     returns float 
   >     not null
   >     language javascript
   >     as
   >     $$
   >     var row_count = 0;
   >     // Dynamically compose the SQL statement to execute.
   >     // Note that we uppercased the input parameter name.
   >     var sql_command = "select count(*) from " + TABLE_NAME;
   >     // Run the statement.
   >     var stmt = snowflake.createStatement(
   >            {
   >            sqlText: sql_command
   >            }
   >         );
   >     var res = stmt.execute();
   >     // Get back the row count. Specifically, ...
   >     // ... first, get the first (and in this case only) row from the
   >     //  result set ...
   >     res.next();
   >     // ... then extract the returned value (which in this case is the
   >     // number of rows in the table).
   >     row_count = res.getColumnValue(1);
   >     return row_count;
   >     $$
   >     ;
   > ```
   >
   > Copy
2. Call the stored procedure:

   > ```
   > call get_row_count('stproc_test_table1');
   > +---------------+
   > | GET_ROW_COUNT |
   > |---------------|
   > |             3 |
   > +---------------+
   > ```
   >
   > Copy
3. Show the results from `select count(*)` for the same table:

   > ```
   > SELECT COUNT(*) FROM stproc_test_table1;
   > +----------+
   > | COUNT(*) |
   > |----------|
   > |        3 |
   > +----------+
   > ```
   >
   > Copy

### Retrieving result set metadata[¶](#retrieving-result-set-metadata "Link to this heading")

This example demonstrates retrieving a small amount of metadata from a result set:

> ```
> create or replace table stproc_test_table3 (
>     n10 numeric(10,0),     /* precision = 10, scale = 0 */
>     n12 numeric(12,4),     /* precision = 12, scale = 4 */
>     v1 varchar(19)         /* scale = 0 */
>     );
> ```
>
> Copy
>
> ```
> create or replace procedure get_column_scale(column_index float)
>     returns float not null
>     language javascript
>     as
>     $$
>     var stmt = snowflake.createStatement(
>         {sqlText: "select n10, n12, v1 from stproc_test_table3;"}
>         );
>     stmt.execute();  // ignore the result set; we just want the scale.
>     return stmt.getColumnScale(COLUMN_INDEX); // Get by column index (1-based)
>     $$
>     ;
> ```
>
> Copy
>
> ```
> call get_column_scale(1);
> +------------------+
> | GET_COLUMN_SCALE |
> |------------------|
> |                0 |
> +------------------+
> ```
>
> Copy
>
> ```
> call get_column_scale(2);
> +------------------+
> | GET_COLUMN_SCALE |
> |------------------|
> |                4 |
> +------------------+
> ```
>
> Copy
>
> ```
> call get_column_scale(3);
> +------------------+
> | GET_COLUMN_SCALE |
> |------------------|
> |                0 |
> +------------------+
> ```
>
> Copy

### Catching an error using try/catch[¶](#catching-an-error-using-try-catch "Link to this heading")

This example demonstrates using a JavaScript try/catch block to catch an error inside a stored procedure:

> 1. Create the stored procedure:
>
>    ```
>        create procedure broken()
>          returns varchar not null
>          language javascript
>          as
>          $$
>          var result = "";
>          try {
>              snowflake.execute( {sqlText: "Invalid Command!;"} );
>              result = "Succeeded";
>              }
>          catch (err)  {
>              result =  "Failed: Code: " + err.code + "\n  State: " + err.state;
>              result += "\n  Message: " + err.message;
>              result += "\nStack Trace:\n" + err.stackTraceTxt; 
>              }
>          return result;
>          $$
>          ;
>    ```
>
>    Copy
> 2. Call the stored procedure. This should return an error showing the error
>    number and other information:
>
>    ```
>        -- This is expected to fail.
>        call broken();
>    +---------------------------------------------------------+
>    | BROKEN                                                  |
>    |---------------------------------------------------------|
>    | Failed: Code: 1003                                      |
>    |   State: 42000                                          |
>    |   Message: SQL compilation error:                       |
>    | syntax error line 1 at position 0 unexpected 'Invalid'. |
>    | Stack Trace:                                            |
>    | Snowflake.execute, line 4 position 20                   |
>    +---------------------------------------------------------+
>    ```
>
>    Copy

The following example demonstrates throwing a custom exception:

> 1. Create the stored procedure:
>
>    ```
>    CREATE OR REPLACE PROCEDURE validate_age (age float)
>    RETURNS VARCHAR
>    LANGUAGE JAVASCRIPT
>    EXECUTE AS CALLER
>    AS $$
>        try {
>            if (AGE < 0) {
>                throw "Age cannot be negative!";
>            } else {
>                return "Age validated.";
>            }
>        } catch (err) {
>            return "Error: " + err;
>        }
>    $$;
>    ```
>
>    Copy
> 2. Call the stored procedure with valid and invalid values:
>
>    ```
>    CALL validate_age(50);
>    +----------------+
>    | VALIDATE_AGE   |
>    |----------------|
>    | Age validated. |
>    +----------------+
>    CALL validate_age(-2);
>    +--------------------------------+
>    | VALIDATE_AGE                   |
>    |--------------------------------|
>    | Error: Age cannot be negative! |
>    +--------------------------------+
>    ```
>
>    Copy

### Using transactions in stored procedures[¶](#using-transactions-in-stored-procedures "Link to this heading")

The following example wraps multiple related statements in a transaction, and uses try/catch to commit or roll back.
The parameter `force_failure` allows the caller to choose between successful execution and deliberate error.

```
-- Create the procedure
CREATE OR REPLACE PROCEDURE cleanup(force_failure VARCHAR)
  RETURNS VARCHAR NOT NULL
  LANGUAGE JAVASCRIPT
  AS
  $$
  var result = "";
  snowflake.execute( {sqlText: "BEGIN WORK;"} );
  try {
      snowflake.execute( {sqlText: "DELETE FROM child;"} );
      snowflake.execute( {sqlText: "DELETE FROM parent;"} );
      if (FORCE_FAILURE === "fail")  {
          // To see what happens if there is a failure/rollback,
          snowflake.execute( {sqlText: "DELETE FROM no_such_table;"} );
          }
      snowflake.execute( {sqlText: "COMMIT WORK;"} );
      result = "Succeeded";
      }
  catch (err)  {
      snowflake.execute( {sqlText: "ROLLBACK WORK;"} );
      return "Failed: " + err;   // Return a success/error indicator.
      }
  return result;
  $$
  ;

CALL cleanup('fail');

CALL cleanup('do not fail');
```

Copy

### Logging an error[¶](#logging-an-error "Link to this heading")

You can capture log and trace data from JavaScript handler code by using the `snowflake` object in the JavaScript API. When you do,
log messages and trace data are stored in an event table that you can analyze with queries.

For more information, refer to the following:

* [Logging messages in JavaScript](../logging-tracing/logging-javascript)
* [Emitting trace events in JavaScript](../logging-tracing/tracing-javascript)

### Using RESULT\_SCAN to retrieve the result from a stored procedure[¶](#using-result-scan-to-retrieve-the-result-from-a-stored-procedure "Link to this heading")

The following example shows you how to use the [RESULT\_SCAN](../../sql-reference/functions/result_scan) function to retrieve and process the result from a
[CALL](../../sql-reference/sql/call) statement:

1. Create and load the table:

   > ```
   > CREATE TABLE western_provinces(ID INT, province VARCHAR);
   > ```
   >
   > Copy
   >
   > ```
   > INSERT INTO western_provinces(ID, province) VALUES
   >     (1, 'Alberta'),
   >     (2, 'British Columbia'),
   >     (3, 'Manitoba')
   >     ;
   > ```
   >
   > Copy
2. Create the stored procedure. This procedure returns a well-formatted string that looks like a result set of
   three rows, but is actually a single string:

   > ```
   > CREATE OR REPLACE PROCEDURE read_western_provinces()
   >   RETURNS VARCHAR NOT NULL
   >   LANGUAGE JAVASCRIPT
   >   AS
   >   $$
   >   var return_value = "";
   >   try {
   >       var command = "SELECT * FROM western_provinces ORDER BY province;"
   >       var stmt = snowflake.createStatement( {sqlText: command } );
   >       var rs = stmt.execute();
   >       if (rs.next())  {
   >           return_value += rs.getColumnValue(1);
   >           return_value += ", " + rs.getColumnValue(2);
   >           }
   >       while (rs.next())  {
   >           return_value += "\n";
   >           return_value += rs.getColumnValue(1);
   >           return_value += ", " + rs.getColumnValue(2);
   >           }
   >       }
   >   catch (err)  {
   >       result =  "Failed: Code: " + err.code + "\n  State: " + err.state;
   >       result += "\n  Message: " + err.message;
   >       result += "\nStack Trace:\n" + err.stackTraceTxt;
   >       }
   >   return return_value;
   >   $$
   >   ;
   > ```
   >
   > Copy
3. Call the stored procedure, then retrieve the results by using RESULT\_SCAN:

   > ```
   > CALL read_western_provinces();
   > +------------------------+
   > | READ_WESTERN_PROVINCES |
   > |------------------------|
   > | 1, Alberta             |
   > | 2, British Columbia    |
   > | 3, Manitoba            |
   > +------------------------+
   > SELECT * FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()));
   > +------------------------+
   > | READ_WESTERN_PROVINCES |
   > |------------------------|
   > | 1, Alberta             |
   > | 2, British Columbia    |
   > | 3, Manitoba            |
   > +------------------------+
   > ```
   >
   > Copy

You can perform more complex operations on the value returned by the RESULT\_SCAN function. In this case, because the
returned value is a single string, you might want to extract the individual “rows” that appear to be contained
within that string, and store those rows in another table.

Tip

You can also use the [pipe operator](../../sql-reference/operators-flow) (`->>`) instead of the RESULT\_SCAN function to
run a CALL statement and process its result set with a single command.

The following example, which is a continuation of the previous example, illustrates one way to do this:

1. Create a table for long-term storage. This table contains the province name and the province ID after you’ve
   extracted them from the string returned by the CALL command:

   > ```
   > CREATE TABLE all_provinces(ID INT, province VARCHAR);
   > ```
   >
   > Copy
2. Call the stored procedure, then retrieve the result by using RESULT\_SCAN, and then extract the three rows
   from the string and put those rows into the table:

   > ```
   > INSERT INTO all_provinces
   >   WITH 
   >     one_string (string_col) AS
   >       (SELECT * FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()))),
   >     three_strings (one_row) AS
   >       (SELECT VALUE FROM one_string, LATERAL SPLIT_TO_TABLE(one_string.string_col, '\n'))
   >   SELECT
   >          STRTOK(one_row, ',', 1) AS ID,
   >          STRTOK(one_row, ',', 2) AS province
   >     FROM three_strings
   >     WHERE NOT (ID IS NULL AND province IS NULL);
   > +-------------------------+
   > | number of rows inserted |
   > |-------------------------|
   > |                       3 |
   > +-------------------------+
   > ```
   >
   > Copy
3. Verify that this worked by showing the rows in the table:

   > ```
   > SELECT ID, province 
   >     FROM all_provinces;
   > +----+-------------------+
   > | ID | PROVINCE          |
   > |----+-------------------|
   > |  1 |  Alberta          |
   > |  2 |  British Columbia |
   > |  3 |  Manitoba         |
   > +----+-------------------+
   > ```
   >
   > Copy

Here’s approximately the same code, but in smaller steps:

1. Create a table named `one_string`. This table temporarily stores the result of the CALL command.
   The result of the CALL is a single string, so this table stores only a single VARCHAR value.

   > ```
   > CREATE TRANSIENT TABLE one_string(string_col VARCHAR);
   > ```
   >
   > Copy
2. Call the stored procedure, then retrieve the result (a string) by using RESULT\_SCAN, and then store that into
   the intermediate table named `one_string`:

   > ```
   > CALL read_western_provinces();
   > +------------------------+
   > | READ_WESTERN_PROVINCES |
   > |------------------------|
   > | 1, Alberta             |
   > | 2, British Columbia    |
   > | 3, Manitoba            |
   > +------------------------+
   > INSERT INTO one_string
   >     SELECT * FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()));
   > +-------------------------+
   > | number of rows inserted |
   > |-------------------------|
   > |                       1 |
   > +-------------------------+
   > ```
   >
   > Copy

   This shows the new row in the `one_string` table. Remember that although this is formatted to look like three rows,
   it is actually a single string:

   > ```
   > SELECT string_col FROM one_string;
   > +---------------------+
   > | STRING_COL          |
   > |---------------------|
   > | 1, Alberta          |
   > | 2, British Columbia |
   > | 3, Manitoba         |
   > +---------------------+
   > -- Show that it's one string, not three rows:
   > SELECT '>>>' || string_col || '<<<' AS string_col 
   >     FROM one_string;
   > +---------------------+
   > | STRING_COL          |
   > |---------------------|
   > | >>>1, Alberta       |
   > | 2, British Columbia |
   > | 3, Manitoba<<<      |
   > +---------------------+
   > SELECT COUNT(*) FROM one_string;
   > +----------+
   > | COUNT(*) |
   > |----------|
   > |        1 |
   > +----------+
   > ```
   >
   > Copy

   The following commands show how to extract multiple rows from the string:

   > ```
   > SELECT * FROM one_string, LATERAL SPLIT_TO_TABLE(one_string.string_col, '\n');
   > +---------------------+-----+-------+---------------------+
   > | STRING_COL          | SEQ | INDEX | VALUE               |
   > |---------------------+-----+-------+---------------------|
   > | 1, Alberta          |   1 |     1 | 1, Alberta          |
   > | 2, British Columbia |     |       |                     |
   > | 3, Manitoba         |     |       |                     |
   > | 1, Alberta          |   1 |     2 | 2, British Columbia |
   > | 2, British Columbia |     |       |                     |
   > | 3, Manitoba         |     |       |                     |
   > | 1, Alberta          |   1 |     3 | 3, Manitoba         |
   > | 2, British Columbia |     |       |                     |
   > | 3, Manitoba         |     |       |                     |
   > +---------------------+-----+-------+---------------------+
   > SELECT VALUE FROM one_string, LATERAL SPLIT_TO_TABLE(one_string.string_col, '\n');
   > +---------------------+
   > | VALUE               |
   > |---------------------|
   > | 1, Alberta          |
   > | 2, British Columbia |
   > | 3, Manitoba         |
   > +---------------------+
   > ```
   >
   > Copy
3. Next, create a table named `three_strings`. This table will hold the result after you’ve split it into individual
   lines/strings:

   > ```
   > CREATE TRANSIENT TABLE three_strings(string_col VARCHAR);
   > ```
   >
   > Copy
4. Now convert that one string in the `one_string` table into three separate strings, and show that it is
   now actually three strings:

   > ```
   > INSERT INTO three_strings
   >   SELECT VALUE FROM one_string, LATERAL SPLIT_TO_TABLE(one_string.string_col, '\n');
   > +-------------------------+
   > | number of rows inserted |
   > |-------------------------|
   > |                       3 |
   > +-------------------------+
   > SELECT string_col 
   >     FROM three_strings;
   > +---------------------+
   > | STRING_COL          |
   > |---------------------|
   > | 1, Alberta          |
   > | 2, British Columbia |
   > | 3, Manitoba         |
   > +---------------------+
   > SELECT COUNT(*) 
   >     FROM three_strings;
   > +----------+
   > | COUNT(*) |
   > |----------|
   > |        3 |
   > +----------+
   > ```
   >
   > Copy
5. Now convert the three strings into three rows in our long-term table named `all_provinces`:

   > ```
   > INSERT INTO all_provinces
   >   SELECT 
   >          STRTOK(string_col, ',', 1) AS ID, 
   >          STRTOK(string_col, ',', 2) AS province 
   >     FROM three_strings
   >     WHERE NOT (ID IS NULL AND province IS NULL);
   > +-------------------------+
   > | number of rows inserted |
   > |-------------------------|
   > |                       3 |
   > +-------------------------+
   > ```
   >
   > Copy
6. Show the three rows in the long-term table:

   > ```
   > SELECT ID, province 
   >     FROM all_provinces;
   > +----+-------------------+
   > | ID | PROVINCE          |
   > |----+-------------------|
   > |  1 |  Alberta          |
   > |  2 |  British Columbia |
   > |  3 |  Manitoba         |
   > +----+-------------------+
   > SELECT COUNT(*) 
   >     FROM all_provinces;
   > +----------+
   > | COUNT(*) |
   > |----------|
   > |        3 |
   > +----------+
   > ```
   >
   > Copy

### Returning an array of error messages[¶](#returning-an-array-of-error-messages "Link to this heading")

Your stored procedure might execute more than one SQL statement and you might want to return a status/error message
for each SQL statement. However, a stored procedure returns a single row; it is not designed to return multiple
rows.

If all of your messages fit into a single value of type ARRAY, you can get all the messages from a stored procedure
with some additional effort.

The following example shows one way to do this (the error messages shown are not real, but you can extend this code to
work with your actual SQL statements):

> ```
> CREATE OR REPLACE PROCEDURE sp_return_array()
>       RETURNS VARIANT NOT NULL
>       LANGUAGE JAVASCRIPT
>       AS
>       $$
>       // This array will contain one error message (or an empty string) 
>       // for each SQL command that we executed.
>       var array_of_rows = [];
>
>       // Artificially fake the error messages.
>       array_of_rows.push("ERROR: The foo was barred.")
>       array_of_rows.push("WARNING: A Carrington Event is predicted.")
>
>       return array_of_rows;
>       $$
>       ;
> ```
>
> Copy
>
> ```
> CALL sp_return_array();
> +-----------------------------------------------+
> | SP_RETURN_ARRAY                               |
> |-----------------------------------------------|
> | [                                             |
> |   "ERROR: The foo was barred.",               |
> |   "WARNING: A Carrington Event is predicted." |
> | ]                                             |
> +-----------------------------------------------+
> -- Now get the individual error messages, in order.
> SELECT INDEX, VALUE 
>     FROM TABLE(RESULT_SCAN(LAST_QUERY_ID())) AS res, LATERAL FLATTEN(INPUT => res.$1)
>     ORDER BY index
>     ;
> +-------+---------------------------------------------+
> | INDEX | VALUE                                       |
> |-------+---------------------------------------------|
> |     0 | "ERROR: The foo was barred."                |
> |     1 | "WARNING: A Carrington Event is predicted." |
> +-------+---------------------------------------------+
> ```
>
> Copy

Remember, this is not a general purpose solution. There is a limit on the maximum size of
ARRAY data types, and your entire result set must fit into a single ARRAY.

### Returning a result set[¶](#returning-a-result-set "Link to this heading")

This section extends the previous example described in [Returning an Array of Error Messages](#returning-an-array-of-error-messages). This example is more
general, and allows you to return a result set from a query.

A stored procedure returns a single row that contains a single column; it is not designed to return a result set.
However, if your result set is small enough to fit into a single value of type VARIANT or ARRAY, you can return
a result set from a stored procedure with some additional code:

> > ```
> > CREATE TABLE return_to_me(col_i INT, col_v VARCHAR);
> > INSERT INTO return_to_me (col_i, col_v) VALUES
> >     (1, 'Ariel'),
> >     (2, 'October'),
> >     (3, NULL),
> >     (NULL, 'Project');
> > ```
> >
> > Copy
> >
> > ```
> > -- Create the stored procedure that retrieves a result set and returns it.
> > CREATE OR REPLACE PROCEDURE sp_return_table(TABLE_NAME VARCHAR, COL_NAMES ARRAY)
> >       RETURNS VARIANT NOT NULL
> >       LANGUAGE JAVASCRIPT
> >       AS
> >       $$
> >       // This variable will hold a JSON data structure that holds ONE row.
> >       var row_as_json = {};
> >       // This array will contain all the rows.
> >       var array_of_rows = [];
> >       // This variable will hold a JSON data structure that we can return as
> >       // a VARIANT.
> >       // This will contain ALL the rows in a single "value".
> >       var table_as_json = {};
> >
> >       // Run SQL statement(s) and get a resultSet.
> >       var command = "SELECT * FROM " + TABLE_NAME;
> >       var cmd1_dict = {sqlText: command};
> >       var stmt = snowflake.createStatement(cmd1_dict);
> >       var rs = stmt.execute();
> >
> >       // Read each row and add it to the array we will return.
> >       var row_num = 1;
> >       while (rs.next())  {
> >         // Put each row in a variable of type JSON.
> >         row_as_json = {};
> >         // For each column in the row...
> >         for (var col_num = 0; col_num < COL_NAMES.length; col_num = col_num + 1) {
> >           var col_name = COL_NAMES[col_num];
> >           row_as_json[col_name] = rs.getColumnValue(col_num + 1);
> >           }
> >         // Add the row to the array of rows.
> >         array_of_rows.push(row_as_json);
> >         ++row_num;
> >         }
> >       // Put the array in a JSON variable (so it looks like a VARIANT to
> >       // Snowflake).  The key is "key1", and the value is the array that has
> >       // the rows we want.
> >       table_as_json = { "key1" : array_of_rows };
> >
> >       // Return the rows to Snowflake, which expects a JSON-compatible VARIANT.
> >       return table_as_json;
> >       $$
> >       ;
> > ```
> >
> > Copy
> >
> > ```
> > CALL sp_return_table(
> >         -- Table name.
> >         'return_to_me',
> >         -- Array of column names.
> >         ARRAY_APPEND(TO_ARRAY('COL_I'), 'COL_V')
> >         );
> > +--------------------------+
> > | SP_RETURN_TABLE          |
> > |--------------------------|
> > | {                        |
> > |   "key1": [              |
> > |     {                    |
> > |       "COL_I": 1,        |
> > |       "COL_V": "Ariel"   |
> > |     },                   |
> > |     {                    |
> > |       "COL_I": 2,        |
> > |       "COL_V": "October" |
> > |     },                   |
> > |     {                    |
> > |       "COL_I": 3,        |
> > |       "COL_V": null      |
> > |     },                   |
> > |     {                    |
> > |       "COL_I": null,     |
> > |       "COL_V": "Project" |
> > |     }                    |
> > |   ]                      |
> > | }                        |
> > +--------------------------+
> > -- Use "ResultScan" to get the data from the stored procedure that
> > -- "did not return a result set".
> > -- Use "$1:key1" to get the value corresponding to the JSON key named "key1".
> > SELECT $1:key1 FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()));
> > +------------------------+
> > | $1:KEY1                |
> > |------------------------|
> > | [                      |
> > |   {                    |
> > |     "COL_I": 1,        |
> > |     "COL_V": "Ariel"   |
> > |   },                   |
> > |   {                    |
> > |     "COL_I": 2,        |
> > |     "COL_V": "October" |
> > |   },                   |
> > |   {                    |
> > |     "COL_I": 3,        |
> > |     "COL_V": null      |
> > |   },                   |
> > |   {                    |
> > |     "COL_I": null,     |
> > |     "COL_V": "Project" |
> > |   }                    |
> > | ]                      |
> > +------------------------+
> > -- Now get what we really want.
> > SELECT VALUE:COL_I AS col_i, value:COL_V AS col_v
> >   FROM TABLE(RESULT_SCAN(LAST_QUERY_ID())) AS res, LATERAL FLATTEN(input => res.$1)
> >   ORDER BY COL_I;
> > +-------+-----------+
> > | COL_I | COL_V     |
> > |-------+-----------|
> > | 1     | "Ariel"   |
> > | 2     | "October" |
> > | 3     | null      |
> > | null  | "Project" |
> > +-------+-----------+
> > ```
> >
> > Copy
>
> This shows how to combine the previous two lines into a single line:
>
> > ```
> > CALL sp_return_table(
> >         -- Table name.
> >         'return_to_me',
> >         -- Array of column names.
> >         ARRAY_APPEND(TO_ARRAY('COL_I'), 'COL_V')
> >         );
> > +--------------------------+
> > | SP_RETURN_TABLE          |
> > |--------------------------|
> > | {                        |
> > |   "key1": [              |
> > |     {                    |
> > |       "COL_I": 1,        |
> > |       "COL_V": "Ariel"   |
> > |     },                   |
> > |     {                    |
> > |       "COL_I": 2,        |
> > |       "COL_V": "October" |
> > |     },                   |
> > |     {                    |
> > |       "COL_I": 3,        |
> > |       "COL_V": null      |
> > |     },                   |
> > |     {                    |
> > |       "COL_I": null,     |
> > |       "COL_V": "Project" |
> > |     }                    |
> > |   ]                      |
> > | }                        |
> > +--------------------------+
> > SELECT VALUE:COL_I AS col_i, value:COL_V AS col_v
> >        FROM (SELECT $1:key1 FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()))) AS res,
> >             LATERAL FLATTEN(input => res.$1)
> >        ORDER BY COL_I;
> > +-------+-----------+
> > | COL_I | COL_V     |
> > |-------+-----------|
> > | 1     | "Ariel"   |
> > | 2     | "October" |
> > | 3     | null      |
> > | null  | "Project" |
> > +-------+-----------+
> > ```
> >
> > Copy
>
> For convenience, you can wrap the preceding line in a view. This view also converts the string ‘null’ to a true NULL.
> You only need to create the view once. However, you must call the stored procedure immediately prior to
> selecting from this view every time you use the view. Remember, the call to RESULT\_SCAN in the view is pulling from the
> most recent statement, which must be the CALL:
>
> > ```
> > CREATE VIEW stproc_view (col_i, col_v) AS 
> >   SELECT NULLIF(VALUE:COL_I::VARCHAR, 'null'::VARCHAR), 
> >          NULLIF(value:COL_V::VARCHAR, 'null'::VARCHAR)
> >     FROM (SELECT $1:key1 AS tbl FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()))) AS res, 
> >          LATERAL FLATTEN(input => res.tbl);
> > ```
> >
> > Copy
> >
> > ```
> > CALL sp_return_table(
> >         -- Table name.
> >         'return_to_me',
> >         -- Array of column names.
> >         ARRAY_APPEND(TO_ARRAY('COL_I'), 'COL_V')
> >         );
> > +--------------------------+
> > | SP_RETURN_TABLE          |
> > |--------------------------|
> > | {                        |
> > |   "key1": [              |
> > |     {                    |
> > |       "COL_I": 1,        |
> > |       "COL_V": "Ariel"   |
> > |     },                   |
> > |     {                    |
> > |       "COL_I": 2,        |
> > |       "COL_V": "October" |
> > |     },                   |
> > |     {                    |
> > |       "COL_I": 3,        |
> > |       "COL_V": null      |
> > |     },                   |
> > |     {                    |
> > |       "COL_I": null,     |
> > |       "COL_V": "Project" |
> > |     }                    |
> > |   ]                      |
> > | }                        |
> > +--------------------------+
> > SELECT * 
> >     FROM stproc_view
> >     ORDER BY COL_I;
> > +-------+---------+
> > | COL_I | COL_V   |
> > |-------+---------|
> > | 1     | Ariel   |
> > | 2     | October |
> > | 3     | NULL    |
> > | NULL  | Project |
> > +-------+---------+
> > ```
> >
> > Copy
>
> You can even use it as a true view (i.e. select a subset of it):
>
> > ```
> > CALL sp_return_table(
> >         -- Table name.
> >         'return_to_me',
> >         -- Array of column names.
> >         ARRAY_APPEND(TO_ARRAY('COL_I'), 'COL_V')
> >         );
> > +--------------------------+
> > | SP_RETURN_TABLE          |
> > |--------------------------|
> > | {                        |
> > |   "key1": [              |
> > |     {                    |
> > |       "COL_I": 1,        |
> > |       "COL_V": "Ariel"   |
> > |     },                   |
> > |     {                    |
> > |       "COL_I": 2,        |
> > |       "COL_V": "October" |
> > |     },                   |
> > |     {                    |
> > |       "COL_I": 3,        |
> > |       "COL_V": null      |
> > |     },                   |
> > |     {                    |
> > |       "COL_I": null,     |
> > |       "COL_V": "Project" |
> > |     }                    |
> > |   ]                      |
> > | }                        |
> > +--------------------------+
> > SELECT COL_V 
> >     FROM stproc_view
> >     WHERE COL_V IS NOT NULL
> >     ORDER BY COL_V;
> > +---------+
> > | COL_V   |
> > |---------|
> > | Ariel   |
> > | October |
> > | Project |
> > +---------+
> > ```
> >
> > Copy

Remember, this is not a general purpose solution. There is a limit on the maximum size of VARIANT and
ARRAY data types, and your entire result set must fit into a single VARIANT or ARRAY.

### Protecting privacy[¶](#protecting-privacy "Link to this heading")

This example shows a stored procedure that is useful for an on-line retailer.
This stored procedure respects customers’ privacy, while protecting
legitimate interests of both the retailer and the customer.
If a customer asks the retailer to delete the customer’s data for privacy reasons,
then this stored procedure deletes most of the customer’s data, but leaves the customer’s
purchase history if either of the following is true:

* Any purchased item has a warranty that has not yet expired.
* The customer still owes money (or the customer is owed a refund).

A more real-world version of this would delete individual rows for which payment has been
made and the warranty has expired.

1. Start by creating the tables and loading them:

   > ```
   > create table reviews (customer_ID VARCHAR, review VARCHAR);
   > create table purchase_history (customer_ID VARCHAR, price FLOAT, paid FLOAT,
   >                                product_ID VARCHAR, purchase_date DATE);
   > ```
   >
   > Copy
   >
   > ```
   > insert into purchase_history (customer_ID, price, paid, product_ID, purchase_date) values 
   >     (1, 19.99, 19.99, 'chocolate', '2018-06-17'::DATE),
   >     (2, 19.99,  0.00, 'chocolate', '2017-02-14'::DATE),
   >     (3, 19.99,  19.99, 'chocolate', '2017-03-19'::DATE);
   >
   > insert into reviews (customer_ID, review) values (1, 'Loved the milk chocolate!');
   > insert into reviews (customer_ID, review) values (2, 'Loved the dark chocolate!');
   > ```
   >
   > Copy
2. Create the stored procedure:

   > ```
   > create or replace procedure delete_nonessential_customer_data(customer_ID varchar)
   >     returns varchar not null
   >     language javascript
   >     as
   >     $$
   >
   >     // If the customer posted reviews of products, delete those reviews.
   >     var sql_cmd = "DELETE FROM reviews WHERE customer_ID = " + CUSTOMER_ID;
   >     snowflake.execute( {sqlText: sql_cmd} );
   >
   >     // Delete any other records not needed for warranty or payment info.
   >     // ...
   >
   >     var result = "Deleted non-financial, non-warranty data for customer " + CUSTOMER_ID;
   >
   >     // Find out if the customer has any net unpaid balance (or surplus/prepayment).
   >     sql_cmd = "SELECT SUM(price) - SUM(paid) FROM purchase_history WHERE customer_ID = " + CUSTOMER_ID;
   >     var stmt = snowflake.createStatement( {sqlText: sql_cmd} );
   >     var rs = stmt.execute();
   >     // There should be only one row, so should not need to iterate.
   >     rs.next();
   >     var net_amount_owed = rs.getColumnValue(1);
   >
   >     // Look up the number of purchases still under warranty...
   >     var number_purchases_under_warranty = 0;
   >     // Assuming a 1-year warranty...
   >     sql_cmd = "SELECT COUNT(*) FROM purchase_history ";
   >     sql_cmd += "WHERE customer_ID = " + CUSTOMER_ID;
   >     // Can't use CURRENT_DATE() because that changes. So assume that today is 
   >     // always June 15, 2019.
   >     sql_cmd += "AND PURCHASE_DATE > dateadd(year, -1, '2019-06-15'::DATE)";
   >     var stmt = snowflake.createStatement( {sqlText: sql_cmd} );
   >     var rs = stmt.execute();
   >     // There should be only one row, so should not need to iterate.
   >     rs.next();
   >     number_purchases_under_warranty = rs.getColumnValue(1);
   >
   >     // Check whether need to keep some purchase history data; if not, then delete the data.
   >     if (net_amount_owed == 0.0 && number_purchases_under_warranty == 0)  {
   >         // Delete the purchase history of this customer ...
   >         sql_cmd = "DELETE FROM purchase_history WHERE customer_ID = " + CUSTOMER_ID;
   >         snowflake.execute( {sqlText: sql_cmd} );
   >         // ... and delete anything else that should be deleted.
   >         // ...
   >         result = "Deleted all data, including financial and warranty data, for customer " + CUSTOMER_ID;
   >         }
   >     return result;
   >     $$
   >     ;
   > ```
   >
   > Copy
3. Show the data in the tables before deleting any of that data:

   > ```
   > SELECT * FROM reviews;
   > +-------------+---------------------------+
   > | CUSTOMER_ID | REVIEW                    |
   > |-------------+---------------------------|
   > | 1           | Loved the milk chocolate! |
   > | 2           | Loved the dark chocolate! |
   > +-------------+---------------------------+
   > SELECT * FROM purchase_history;
   > +-------------+-------+-------+------------+---------------+
   > | CUSTOMER_ID | PRICE |  PAID | PRODUCT_ID | PURCHASE_DATE |
   > |-------------+-------+-------+------------+---------------|
   > | 1           | 19.99 | 19.99 | chocolate  | 2018-06-17    |
   > | 2           | 19.99 |  0    | chocolate  | 2017-02-14    |
   > | 3           | 19.99 | 19.99 | chocolate  | 2017-03-19    |
   > +-------------+-------+-------+------------+---------------+
   > ```
   >
   > Copy
4. Customer #1 has a warranty that is still in effect. The stored procedure deletes the review comments that they posted,
   but keeps their purchase record because of the warranty:

   > ```
   > call delete_nonessential_customer_data(1);
   > +---------------------------------------------------------+
   > | DELETE_NONESSENTIAL_CUSTOMER_DATA                       |
   > |---------------------------------------------------------|
   > | Deleted non-financial, non-warranty data for customer 1 |
   > +---------------------------------------------------------+
   > SELECT * FROM reviews;
   > +-------------+---------------------------+
   > | CUSTOMER_ID | REVIEW                    |
   > |-------------+---------------------------|
   > | 2           | Loved the dark chocolate! |
   > +-------------+---------------------------+
   > SELECT * FROM purchase_history;
   > +-------------+-------+-------+------------+---------------+
   > | CUSTOMER_ID | PRICE |  PAID | PRODUCT_ID | PURCHASE_DATE |
   > |-------------+-------+-------+------------+---------------|
   > | 1           | 19.99 | 19.99 | chocolate  | 2018-06-17    |
   > | 2           | 19.99 |  0    | chocolate  | 2017-02-14    |
   > | 3           | 19.99 | 19.99 | chocolate  | 2017-03-19    |
   > +-------------+-------+-------+------------+---------------+
   > ```
   >
   > Copy
5. Customer #2 still owes money. The stored procedure deletes their review comments, but keeps their purchase record:

   > ```
   > call delete_nonessential_customer_data(2);
   > +---------------------------------------------------------+
   > | DELETE_NONESSENTIAL_CUSTOMER_DATA                       |
   > |---------------------------------------------------------|
   > | Deleted non-financial, non-warranty data for customer 2 |
   > +---------------------------------------------------------+
   > SELECT * FROM reviews;
   > +-------------+--------+
   > | CUSTOMER_ID | REVIEW |
   > |-------------+--------|
   > +-------------+--------+
   > SELECT * FROM purchase_history;
   > +-------------+-------+-------+------------+---------------+
   > | CUSTOMER_ID | PRICE |  PAID | PRODUCT_ID | PURCHASE_DATE |
   > |-------------+-------+-------+------------+---------------|
   > | 1           | 19.99 | 19.99 | chocolate  | 2018-06-17    |
   > | 2           | 19.99 |  0    | chocolate  | 2017-02-14    |
   > | 3           | 19.99 | 19.99 | chocolate  | 2017-03-19    |
   > +-------------+-------+-------+------------+---------------+
   > ```
   >
   > Copy
6. Customer #3 does not owe any money (and is not owed any money). Their warranty expired, so the stored procedure
   deletes both the review comments and the purchase records:

   > ```
   > call delete_nonessential_customer_data(3);
   > +-------------------------------------------------------------------------+
   > | DELETE_NONESSENTIAL_CUSTOMER_DATA                                       |
   > |-------------------------------------------------------------------------|
   > | Deleted all data, including financial and warranty data, for customer 3 |
   > +-------------------------------------------------------------------------+
   > SELECT * FROM reviews;
   > +-------------+--------+
   > | CUSTOMER_ID | REVIEW |
   > |-------------+--------|
   > +-------------+--------+
   > SELECT * FROM purchase_history;
   > +-------------+-------+-------+------------+---------------+
   > | CUSTOMER_ID | PRICE |  PAID | PRODUCT_ID | PURCHASE_DATE |
   > |-------------+-------+-------+------------+---------------|
   > | 1           | 19.99 | 19.99 | chocolate  | 2018-06-17    |
   > | 2           | 19.99 |  0    | chocolate  | 2017-02-14    |
   > +-------------+-------+-------+------------+---------------+
   > ```
   >
   > Copy

### Using session variables with caller’s rights and owner’s rights stored procedures[¶](#using-session-variables-with-caller-s-rights-and-owner-s-rights-stored-procedures "Link to this heading")

These examples illustrate one of the key differences between caller’s rights and owner’s rights stored
procedures. They attempt to use session variables in two ways:

* Set a session variable before calling the stored procedure, then use the session variable inside the stored
  procedure.
* Set a session variable inside the stored procedure, then use the session variable after returning from the stored
  procedures.

Both using the session variable and setting the session variable work correctly in a caller’s rights stored procedure.
Both fail when using an owner’s rights stored procedure even if the caller is the owner.

#### Caller’s rights stored procedure[¶](#caller-s-rights-stored-procedure "Link to this heading")

The following example demonstrates a caller’s rights stored procedure.

1. Create and load a table:

   > ```
   > create table sv_table (f float);
   > insert into sv_table (f) values (49), (51);
   > ```
   >
   > Copy
2. Set a session variable:

   > ```
   > set SESSION_VAR1 = 50;
   > ```
   >
   > Copy
3. Create a caller’s rights stored procedure that uses one session variable and sets another:

   > ```
   > create procedure session_var_user()
   >   returns float
   >   language javascript
   >   EXECUTE AS CALLER
   >   as
   >   $$
   >   // Set the second session variable
   >   var stmt = snowflake.createStatement(
   >       {sqlText: "set SESSION_VAR2 = 'I was set inside the StProc.'"}
   >       );
   >   var rs = stmt.execute();  // we ignore the result in this case
   >   // Run a query using the first session variable
   >   stmt = snowflake.createStatement(
   >       {sqlText: "select f from sv_table where f > $SESSION_VAR1"}
   >       );
   >   rs = stmt.execute();
   >   rs.next();
   >   var output = rs.getColumnValue(1);
   >   return output;
   >   $$
   >   ;
   > ```
   >
   > Copy
4. Call the procedure:

   > ```
   > CALL session_var_user();
   > +------------------+
   > | SESSION_VAR_USER |
   > |------------------|
   > |               51 |
   > +------------------+
   > ```
   >
   > Copy
5. View the value of the session variable set inside the stored procedure:

   > ```
   > SELECT $SESSION_VAR2;
   > +------------------------------+
   > | $SESSION_VAR2                |
   > |------------------------------|
   > | I was set inside the StProc. |
   > +------------------------------+
   > ```
   >
   > Copy

Note

Although you can set a session variable inside a stored procedure and leave it set after the end of the procedure,
Snowflake does not recommend doing this.

#### Owner’s rights stored procedure[¶](#owner-s-rights-stored-procedure "Link to this heading")

The following example demonstrates an owner’s rights stored procedure.

1. Create an owner’s rights stored procedure that uses a session variable:

   > ```
   > create procedure cannot_use_session_vars()
   >   returns float
   >   language javascript
   >   EXECUTE AS OWNER
   >   as
   >   $$
   >   // Run a query using the first session variable
   >   var stmt = snowflake.createStatement(
   >       {sqlText: "select f from sv_table where f > $SESSION_VAR1"}
   >       );
   >   var rs = stmt.execute();
   >   rs.next();
   >   var output = rs.getColumnValue(1);
   >   return output;
   >   $$
   >   ;
   > ```
   >
   > Copy
2. Call the procedure (it should fail):

   > ```
   > CALL cannot_use_session_vars();
   > ```
   >
   > Copy
3. Create an owner’s rights stored procedure that tries to set a session variable:

   > ```
   > create procedure cannot_set_session_vars()
   >   returns float
   >   language javascript
   >   EXECUTE AS OWNER
   >   as
   >   $$
   >   // Set the second session variable
   >   var stmt = snowflake.createStatement(
   >       {sqlText: "set SESSION_VAR2 = 'I was set inside the StProc.'"}
   >       );
   >   var rs = stmt.execute();  // we ignore the result in this case
   >   return 3.0;   // dummy value.
   >   $$
   >   ;
   > ```
   >
   > Copy
4. Call the procedure (it should fail):

   > ```
   > CALL cannot_set_session_vars();
   > ```
   >
   > Copy

## Troubleshooting[¶](#troubleshooting "Link to this heading")

A general troubleshooting technique is to use a JavaScript try/catch block to
catch the error and display error information. The error object contains:

* Error code.
* Error message.
* Error state.
* Stack trace at the point of failure.

For more information, including an example, of how to use this information, see [Catching an error using try/catch](#label-stored-procedure-error-handling) (in this topic).

Th following sections provide additional suggestions to help debug specific problems.

### Stored procedure or UDF unexpectedly returns NULL[¶](#stored-procedure-or-udf-unexpectedly-returns-null "Link to this heading")

Cause:
:   Your stored procedure/UDF has a parameter, and inside the procedure/UDF, the parameter is referred to by its lowercase name, but Snowflake has
    automatically converted the name to uppercase.

Solution:
:   Either:

    * Use uppercase for the variable name inside the JavaScript code, or
    * Enclose the variable name in double quotes in the SQL code.

    For more details, see [JavaScript arguments and returned values](../udf/javascript/udf-javascript-introduction.html#label-js-udf-arguments).

### Stored procedure never finishes running[¶](#stored-procedure-never-finishes-running "Link to this heading")

Cause:
:   You might have an infinite loop in your JavaScript code.

Solution:
:   Check for and fix any infinite loops.

### Error: `Failed: empty argument passed`[¶](#error-failed-empty-argument-passed "Link to this heading")

Cause:
:   Your stored procedure might contain “sqltext” when it should have “sqlText”
    (the first is all lowercase; the second is mixed case).

Solution:
:   Use “sqlText”.

### Error: `JavaScript out of memory error: UDF thread memory limit exceeded`[¶](#error-javascript-out-of-memory-error-udf-thread-memory-limit-exceeded "Link to this heading")

Cause:
:   You might have an infinite loop in your JavaScript code.

Solution:
:   Check for and fix any infinite loops. In particular, ensure that you stop calling for the next row when the result set runs out (i.e. when
    `resultSet.next()` returns `false`).

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

1. [Understanding the JavaScript API](#understanding-the-javascript-api)
2. [SQL and JavaScript data type mapping](#sql-and-javascript-data-type-mapping)
3. [General tips](#general-tips)
4. [JavaScript stored procedure considerations](#javascript-stored-procedure-considerations)
5. [Examples](#examples)
6. [Troubleshooting](#troubleshooting)

Related content

1. [Working with stored procedures](/developer-guide/stored-procedure/stored-procedures-usage)
2. [Understanding caller’s rights and owner’s rights stored procedures](/developer-guide/stored-procedure/stored-procedures-rights)
3. [JavaScript stored procedures API](/developer-guide/stored-procedure/stored-procedures-api)
4. [Introduction to JavaScript UDFs](/developer-guide/stored-procedure/../udf/javascript/udf-javascript-introduction)