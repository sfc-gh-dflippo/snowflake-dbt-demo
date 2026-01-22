---
auto_generated: true
description: Snowflake supports SQL user-defined functions (UDFs) that contain Snowflake
  Scripting procedural language. These UDFs are called Snowflake Scripting UDFs.
last_scraped: '2026-01-14T16:54:40.825279+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/developer-guide/udf/sql/udf-sql-procedural-functions
title: Snowflake Scripting UDFs | Snowflake Documentation
---

1. [Overview](../../../developer.md)
2. Builders
3. [Snowflake DevOps](../../builders/devops.md)
4. [Observability](../../builders/observability.md)
5. Snowpark Library
6. [Snowpark API](../../snowpark/index.md)
7. [Spark workloads on Snowflake](../../snowpark-connect/snowpark-connect-overview.md)
8. Machine Learning
9. [Snowflake ML](../../snowflake-ml/overview.md)
10. Snowpark Code Execution Environments
11. [Snowpark Container Services](../../snowpark-container-services/overview.md)
12. [Functions and procedures](../../extensibility.md)

    * [Function or procedure?](../../stored-procedures-vs-udfs.md)
    * [Guidelines](../../udf-stored-procedure-guidelines.md)
    * [Stored procedures](../../stored-procedure/stored-procedures-overview.md)
    * [User-defined functions](../udf-overview.md)

      + [Privileges](../udf-access-control.md)
      + [Creating](../udf-creating-sql.md)
      + [Executing](../udf-calling-sql.md)
      + [Viewing in Snowsight](../../../user-guide/ui-snowsight-data-databases-function.md)
      + Handler writing
      + [Java](../java/udf-java-introduction.md)
      + [Javascript](../javascript/udf-javascript-introduction.md)
      + [Python](../python/udf-python-introduction.md)
      + [Scala](../scala/udf-scala-introduction.md)
      + [SQL](udf-sql-introduction.md)

        - [Limitations](udf-sql-limitations.md)
        - [Scalar functions](udf-sql-scalar-functions.md)
        - [Table functions](udf-sql-tabular-functions.md)
        - [Snowflake Scripting functions](udf-sql-procedural-functions.md)
        - [Troubleshooting](udf-sql-troubleshooting.md)
    * [Packaging handler code](../../udf-stored-procedure-building.md)
    * [External network access](../../external-network-access/external-network-access-overview.md)
13. [Logging, Tracing, and Metrics](../../logging-tracing/logging-tracing-overview.md)
14. Snowflake APIs
15. [Snowflake Python APIs](../../snowflake-python-api/snowflake-python-overview.md)
16. [Snowflake REST APIs](../../snowflake-rest-api/snowflake-rest-api.md)
17. [SQL API](../../sql-api/index.md)
18. Apps
19. Streamlit in Snowflake

    - [About Streamlit in Snowflake](../../streamlit/about-streamlit.md)
    - Getting started

      - [Deploy a sample app](../../streamlit/getting-started/overview.md)
      - [Create and deploy Streamlit apps using Snowsight](../../streamlit/getting-started/create-streamlit-ui.md)
      - [Create and deploy Streamlit apps using SQL](../../streamlit/getting-started/create-streamlit-sql.md)
      - [Create and deploy Streamlit apps using Snowflake CLI](../../streamlit/getting-started/create-streamlit-snowflake-cli.md)
    - Streamlit object management

      - [Billing considerations](../../streamlit/object-management/billing.md)
      - [Security considerations](../../streamlit/object-management/security.md)
      - [Privilege requirements](../../streamlit/object-management/privileges.md)
      - [Understanding owner's rights](../../streamlit/object-management/owners-rights.md)
      - [PrivateLink](../../streamlit/object-management/privatelink.md)
      - [Logging and tracing](../../streamlit/object-management/logging-tracing.md)
    - App development

      - [Runtime environments](../../streamlit/app-development/runtime-environments.md)
      - [Dependency management](../../streamlit/app-development/dependency-management.md)
      - [File organization](../../streamlit/app-development/file-organization.md)
      - [Secrets and configuration](../../streamlit/app-development/secrets-and-configuration.md)
      - [Editing your app](../../streamlit/app-development/editing-your-app.md)
    - Migrations and upgrades

      - [Identify your app type](../../streamlit/migrations-and-upgrades/overview.md)
      - [Migrate to a container runtime](../../streamlit/migrations-and-upgrades/runtime-migration.md)
      - [Migrate from ROOT\_LOCATION](../../streamlit/migrations-and-upgrades/root-location.md)
    - Features

      - [Git integration](../../streamlit/features/git-integration.md)
      - [External access](../../streamlit/features/external-access.md)
      - [Row access policies](../../streamlit/features/row-access.md)
      - [Sleep timer](../../streamlit/features/sleep-timer.md)
    - [Limitations and library changes](../../streamlit/limitations.md)
    - [Troubleshooting Streamlit in Snowflake](../../streamlit/troubleshooting.md)
    - [Release notes](../../../release-notes/streamlit-in-snowflake.md)
    - [Streamlit open-source library documentation](https://docs.streamlit.io/)
20. [Snowflake Native App Framework](../../native-apps/native-apps-about.md)
21. [Snowflake Declarative Sharing](../../declarative-sharing/about.md)
22. [Snowflake Native SDK for Connectors](../../native-apps/connector-sdk/about-connector-sdk.md)
23. External Integration
24. [External Functions](../../../sql-reference/external-functions.md)
25. [Kafka and Spark Connectors](../../../user-guide/connectors.md)
26. Snowflake Scripting
27. [Snowflake Scripting Developer Guide](../../snowflake-scripting/index.md)
28. Tools
29. [Snowflake CLI](../../snowflake-cli/index.md)
30. [Git](../../git/git-overview.md)
31. Drivers
32. [Overview](../../drivers.md)
33. [Considerations when drivers reuse sessions](../../driver-connections.md)
34. [Scala versions](../../scala-version-differences.md)
35. Reference
36. [API Reference](../../../api-reference.md)

[Developer](../../../developer.md)[Functions and procedures](../../extensibility.md)[User-defined functions](../udf-overview.md)[SQL](udf-sql-introduction.md)Snowflake Scripting functions

# Snowflake Scripting UDFs[¶](#snowflake-scripting-udfs "Link to this heading")

Snowflake supports SQL user-defined functions (UDFs) that contain Snowflake Scripting procedural language.
These UDFs are called *Snowflake Scripting UDFs*.

Snowflake Scripting UDFs can be called in a SQL statement, such as a SELECT statement or INSERT statement.
Therefore, they are more flexible than a Snowflake Scripting stored procedure, which can only be called in
a SQL [CALL](../../../sql-reference/sql/call) command.

## General usage[¶](#general-usage "Link to this heading")

A Snowflake Scripting UDF evaluates procedural code and returns a scalar (that is, single) value.

You can use the following subset of [Snowflake Scripting](../../snowflake-scripting/index)
syntax in Snowflake Scripting UDFs:

* [Blocks](../../snowflake-scripting/blocks)
* [Variables](../../snowflake-scripting/variables)
* [RETURN command](../../snowflake-scripting/return)
* [Conditional logic](../../snowflake-scripting/branch)
* [Loops](../../snowflake-scripting/loops)
* [Exceptions](../../snowflake-scripting/exceptions)

## Supported data types[¶](#supported-data-types "Link to this heading")

Snowflake Scripting UDFs support the following data types for both input arguments and
return values:

* [Numeric data types](../../../sql-reference/data-types-numeric) (for example, INTEGER, NUMBER, and FLOAT)
* [String & binary data types](../../../sql-reference/data-types-text) (for example, VARCHAR and BINARY)
* [Date & time data types](../../../sql-reference/data-types-datetime) (for example, DATE, TIME, and TIMESTAMP)
* [Logical data types](../../../sql-reference/data-types-logical) (for example, BOOLEAN)

Snowflake Scripting UDFs support the following data types for input arguments only:

* [Semi-structured data types](../../../sql-reference/data-types-semistructured) (for example, VARIANT, OBJECT, and ARRAY)
* [Structured data types](../../../sql-reference/data-types-structured) (for example, ARRAY, OBJECT, and MAP)

## Limitations[¶](#limitations "Link to this heading")

The following limitations apply to Snowflake Scripting UDFs:

* The following types of Snowflake Scripting syntax aren’t supported in Snowflake Scripting UDFs:

  + [Cursors](../../snowflake-scripting/cursors)
  + [RESULTSETs](../../snowflake-scripting/resultsets)
  + [Asynchronous child jobs](../../snowflake-scripting/asynchronous-child-jobs)
* SQL statements aren’t supported in Snowflake Scripting UDFs (including SELECT, INSERT, UPDATE, and so on).
* Snowflake Scripting UDFs can’t be defined as table functions.
* The following expression types aren’t supported in Snowflake Scripting UDFs:

  + User-defined functions
  + Aggregation functions
  + Window functions
* Snowflake Scripting UDFs can’t be used when creating a materialized view.
* Snowflake Scripting UDFs can’t be used when creating row access policies and masking policies.
* Snowflake Scripting UDFs can’t be used to specify a default column value.
* Snowflake Scripting UDFs can’t be used in a COPY INTO command for data loading and unloading.
* Snowflake Scripting UDFs can’t be memoizable.
* Snowflake Scripting UDFs have a limit of 500 input arguments.
* You can’t [log messages](../../logging-tracing/logging) for Snowflake Scripting UDFs.

## Examples[¶](#examples "Link to this heading")

The following examples create and call Snowflake Scripting UDFs:

* [Create a Snowflake Scripting UDF with variables](#label-udf-sql-snowflake-scripting-example-variables)
* [Create a Snowflake Scripting UDF with conditional logic](#label-udf-sql-snowflake-scripting-example-conditional-logic)
* [Create a Snowflake Scripting UDF with a loop](#label-udf-sql-snowflake-scripting-example-loop)
* [Create a Snowflake Scripting UDF with exception handling](#label-udf-sql-snowflake-scripting-example-exception-handling)
* [Create a Snowflake Scripting UDF that returns a value for an INSERT statement](#label-udf-sql-snowflake-scripting-example-insert-values)
* [Create a Snowflake Scripting UDF called in WHERE and ORDER BY clauses](#label-udf-sql-snowflake-scripting-example-use-in-clauses)

### Create a Snowflake Scripting UDF with variables[¶](#create-a-snowflake-scripting-udf-with-variables "Link to this heading")

Create a Snowflake Scripting UDF that calculates profit based on the values of two arguments:

```
CREATE OR REPLACE FUNCTION calculate_profit(
  cost NUMBER(38, 2),
  revenue NUMBER(38, 2))
RETURNS number(38, 2)
LANGUAGE SQL
AS
DECLARE
  profit NUMBER(38, 2) DEFAULT 0.0;
BEGIN
  profit := revenue - cost;
  RETURN profit;
END;
```

Copy

Note

If you use [Snowflake CLI](../../snowflake-cli/index), [SnowSQL](../../../user-guide/snowsql),
the Classic Console, or the `execute_stream` or `execute_string` method in
[Python Connector](../../python-connector/python-connector) code, this example requires minor
changes. For more information, see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](../../snowflake-scripting/running-examples).

Call `calculate_profit` in a query:

```
SELECT calculate_profit(100, 110);
```

Copy

```
+----------------------------+
| CALCULATE_PROFIT(100, 110) |
|----------------------------|
|                      10.00 |
+----------------------------+
```

You can use the same Snowflake Scripting UDF and specify columns for the arguments. First,
create a table and insert data:

```
CREATE OR REPLACE TABLE snowflake_scripting_udf_profit(
  cost NUMBER(38, 2),
  revenue NUMBER(38, 2));

INSERT INTO snowflake_scripting_udf_profit VALUES
  (100, 200),
  (200, 190),
  (300, 500),
  (400, 401);
```

Copy

Call `calculate_profit` in a query and specify the columns for the arguments:

```
SELECT calculate_profit(cost, revenue)
  FROM snowflake_scripting_udf_profit;
```

Copy

```
+---------------------------------+
| CALCULATE_PROFIT(COST, REVENUE) |
|---------------------------------|
|                          100.00 |
|                          -10.00 |
|                          200.00 |
|                            1.00 |
+---------------------------------+
```

### Create a Snowflake Scripting UDF with conditional logic[¶](#create-a-snowflake-scripting-udf-with-conditional-logic "Link to this heading")

Create a Snowflake Scripting UDF that uses conditional logic to determine the department name
based on an input INTEGER value:

```
CREATE OR REPLACE function check_dept(department_id INTEGER)
RETURNS VARCHAR
LANGUAGE SQL
AS
BEGIN
  IF (department_id < 3) THEN
    RETURN 'Engineering';
  ELSEIF (department_id = 3) THEN
    RETURN 'Tool Design';
  ELSE
    RETURN 'Marketing';
  END IF;
END;
```

Copy

Note

If you use [Snowflake CLI](../../snowflake-cli/index), [SnowSQL](../../../user-guide/snowsql),
the Classic Console, or the `execute_stream` or `execute_string` method in
[Python Connector](../../python-connector/python-connector) code, this example requires minor
changes. For more information, see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](../../snowflake-scripting/running-examples).

Call `check_dept` in a query:

```
SELECT check_dept(2);
```

Copy

```
+---------------+
| CHECK_DEPT(2) |
|---------------|
| Engineering   |
+---------------+
```

You can use a [SQL variable](../../../sql-reference/session-variables) in an argument when you
call a Snowflake Scripting UDF. The following example sets a SQL variable and then uses the
variable in a call to the `check_dept` UDF:

```
SET my_variable = 3;

SELECT check_dept($my_variable);
```

Copy

```
+--------------------------+
| CHECK_DEPT($MY_VARIABLE) |
|--------------------------|
| Tool Design              |
+--------------------------+
```

### Create a Snowflake Scripting UDF with a loop[¶](#create-a-snowflake-scripting-udf-with-a-loop "Link to this heading")

Create a Snowflake Scripting UDF that uses a loop to count all numbers up to a target number provided
in an argument and calculate the sum of all of the numbers counted:

```
CREATE OR REPLACE function count_to(
  target_number INTEGER)
RETURNS VARCHAR
LANGUAGE SQL
AS
DECLARE
  counter INTEGER DEFAULT 0;
  sum_total INTEGER DEFAULT 0;
BEGIN
  WHILE (counter < target_number) DO
    counter := counter + 1;
    sum_total := sum_total + counter;
  END WHILE;
  RETURN 'Counted to ' || counter || '. Sum of all numbers: ' || sum_total;
END;
```

Copy

Note

If you use [Snowflake CLI](../../snowflake-cli/index), [SnowSQL](../../../user-guide/snowsql),
the Classic Console, or the `execute_stream` or `execute_string` method in
[Python Connector](../../python-connector/python-connector) code, this example requires minor
changes. For more information, see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](../../snowflake-scripting/running-examples).

Call `count_to` in a query:

```
SELECT count_to(10);
```

Copy

```
+---------------------------------------+
| COUNT_TO(10)                          |
|---------------------------------------|
| Counted to 10. Sum of all numbers: 55 |
+---------------------------------------+
```

### Create a Snowflake Scripting UDF with exception handling[¶](#create-a-snowflake-scripting-udf-with-exception-handling "Link to this heading")

Create a Snowflake Scripting UDF that declares an exception and then raises the exception:

```
CREATE OR REPLACE FUNCTION raise_exception(input_value INTEGER)
RETURNS VARCHAR
LANGUAGE SQL
AS
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
    IF (input_value = 1) THEN
      RETURN 'My exception caught: ' || sqlcode;
    ELSEIF (input_value = 2) THEN
      RETURN 'My exception caught with different path: ' || sqlcode;
    END IF;
    RETURN 'Default exception handling path: ' || sqlcode;
END;
```

Copy

Note

If you use [Snowflake CLI](../../snowflake-cli/index), [SnowSQL](../../../user-guide/snowsql),
the Classic Console, or the `execute_stream` or `execute_string` method in
[Python Connector](../../python-connector/python-connector) code, this example requires minor
changes. For more information, see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](../../snowflake-scripting/running-examples).

Call `raise_exception` in a query and specify `1` for the input value:

```
SELECT raise_exception(1);
```

Copy

```
+-----------------------------+
| RAISE_EXCEPTION(1)          |
|-----------------------------|
| My exception caught: -20002 |
+-----------------------------+
```

Call `raise_exception` in a query and specify `2` for the input value:

```
SELECT raise_exception(2);
```

Copy

```
+-------------------------------------------------+
| RAISE_EXCEPTION(2)                              |
|-------------------------------------------------|
| My exception caught with different path: -20002 |
+-------------------------------------------------+t
```

Call `raise_exception` in a query and specify `NULL` for the input value:

```
SELECT raise_exception(NULL);
```

Copy

```
+-----------------------------------------+
| RAISE_EXCEPTION(NULL)                   |
|-----------------------------------------|
| Default exception handling path: -20002 |
+-----------------------------------------+
```

### Create a Snowflake Scripting UDF that returns a value for an INSERT statement[¶](#create-a-snowflake-scripting-udf-that-returns-a-value-for-an-insert-statement "Link to this heading")

Create a Snowflake Scripting UDF that returns a value that is used in an INSERT statement. Create the table
that the values will be inserted into:

```
CREATE OR REPLACE TABLE test_sql_udf_insert (num NUMBER);
```

Copy

Create a SQL UDF that returns a numeric value:

```
CREATE OR REPLACE FUNCTION value_to_insert(l NUMBER, r NUMBER)
RETURNS number
LANGUAGE SQL
AS
BEGIN
  IF (r < 0) THEN
    RETURN l/r * -1;
  ELSEIF (r > 0) THEN
    RETURN l/r;
  ELSE
    RETURN 0;
END IF;
END;
```

Copy

Note

If you use [Snowflake CLI](../../snowflake-cli/index), [SnowSQL](../../../user-guide/snowsql),
the Classic Console, or the `execute_stream` or `execute_string` method in
[Python Connector](../../python-connector/python-connector) code, this example requires minor
changes. For more information, see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](../../snowflake-scripting/running-examples).

Call `value_to_insert` in multiple INSERT statements:

```
INSERT INTO test_sql_udf_insert SELECT value_to_insert(10, 2);
INSERT INTO test_sql_udf_insert SELECT value_to_insert(10, -2);
INSERT INTO test_sql_udf_insert SELECT value_to_insert(10, 0);
```

Copy

Query the table to view the inserted values:

```
SELECT * FROM test_sql_udf_insert;
```

Copy

```
+-----+
| NUM |
|-----|
|   5 |
|   5 |
|   0 |
+-----+
```

### Create a Snowflake Scripting UDF called in WHERE and ORDER BY clauses[¶](#create-a-snowflake-scripting-udf-called-in-where-and-order-by-clauses "Link to this heading")

Create a Snowflake Scripting UDF that returns a value that is used in a WHERE or ORDER BY clause.
Create a table and insert values:

```
CREATE OR REPLACE TABLE test_sql_udf_clauses (p1 INT, p2 INT);

INSERT INTO test_sql_udf_clauses VALUES
  (100, 7),
  (100, 3),
  (100, 4),
  (NULL, NULL);
```

Copy

Create a SQL UDF that returns a numeric value that is the product of the multiplication
of two input values:

```
CREATE OR REPLACE FUNCTION get_product(a INTEGER, b INTEGER)
RETURNS VARCHAR
LANGUAGE SQL
AS
BEGIN
  RETURN a * b;
END;
```

Copy

Note

If you use [Snowflake CLI](../../snowflake-cli/index), [SnowSQL](../../../user-guide/snowsql),
the Classic Console, or the `execute_stream` or `execute_string` method in
[Python Connector](../../python-connector/python-connector) code, this example requires minor
changes. For more information, see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](../../snowflake-scripting/running-examples).

Call `get_product` in the WHERE clause of a query to return the rows
where the product is greater than `350`:

```
SELECT *
  FROM test_sql_udf_clauses
  WHERE get_product(p1, p2) > 350;
```

Copy

```
+-----+----+
|  P1 | P2 |
|-----+----|
| 100 |  7 |
| 100 |  4 |
+-----+----+
```

Call `get_product` in the ORDER BY clause of a query to order
the results from the lowest to the highest product returned by
the UDF:

```
SELECT *
  FROM test_sql_udf_clauses
  ORDER BY get_product(p1, p2);
```

Copy

```
+------+------+
|  P1  | P2   |
|------+------|
| 100  | 3    |
| 100  | 4    |
| 100  | 7    |
| NULL | NULL |
+------+------+
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

1. [General usage](#general-usage)
2. [Supported data types](#supported-data-types)
3. [Limitations](#limitations)
4. [Examples](#examples)

Related content

1. [Introduction to SQL UDFs](/developer-guide/udf/sql/udf-sql-introduction)
2. [User-defined functions overview](/developer-guide/udf/sql/../udf-overview)