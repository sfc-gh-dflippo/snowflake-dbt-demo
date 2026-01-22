---
auto_generated: true
description: This topic covers concepts and usage details that are specific to SQL
  UDFs (user-defined functions).
last_scraped: '2026-01-14T16:56:41.761692+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/developer-guide/udf/sql/udf-sql-scalar-functions.html
title: Scalar SQL UDFs | Snowflake Documentation
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

[Developer](../../../developer.md)[Functions and procedures](../../extensibility.md)[User-defined functions](../udf-overview.md)[SQL](udf-sql-introduction.md)Scalar functions

# Scalar SQL UDFs[¶](#scalar-sql-udfs "Link to this heading")

This topic covers concepts and usage details that are specific to SQL UDFs (user-defined functions).

## General usage[¶](#general-usage "Link to this heading")

A SQL UDF evaluates an arbitrary SQL expression and returns the result(s) of the expression.

The function definition can be a SQL expression that returns either a scalar (i.e. single) value or, if defined as a table function, a
set of rows. For example, here is a basic example of a scalar UDF that calculates the area of a circle:

```
CREATE FUNCTION area_of_circle(radius FLOAT)
  RETURNS FLOAT
  AS
  $$
    pi() * radius * radius
  $$
  ;
```

Copy

```
SELECT area_of_circle(1.0);
```

Copy

Output:

```
SELECT area_of_circle(1.0);
+---------------------+
| AREA_OF_CIRCLE(1.0) |
|---------------------|
|         3.141592654 |
+---------------------+
```

Copy

The expression can be a query expression (a [SELECT](../../../sql-reference/sql/select) expression). For example:

```
CREATE FUNCTION profit()
  RETURNS NUMERIC(11, 2)
  AS
  $$
    SELECT SUM((retail_price - wholesale_price) * number_sold)
        FROM purchases
  $$
  ;
```

Copy

When using a query expression in a SQL UDF, do not include a semicolon within the UDF body to terminate the query expression.

You can include only one query expression. The expression can include
UNION [ALL].

Note

Although the body of a UDF can contain a complete SELECT statement, it cannot contain DDL statements or any DML statement other
than SELECT.

Note

Scalar functions (UDFs) have a limit of 500 input arguments.

## Memoizable UDFs[¶](#memoizable-udfs "Link to this heading")

A scalar SQL UDF can be memoizable. A memoizable function caches the result of calling a scalar SQL UDF and then returns the
cached result when the output is needed at a later time. The benefit of using a memoizable function is to improve performance for complex
queries, such as multiple column lookups in [mapping tables](https://en.wikipedia.org/wiki/Associative_entity) referenced within a row
access policy or masking policy.

Policy owners (e.g. the role with the OWNERSHIP privilege on the row access policy) can update their policy conditions to replace
subqueries that have mapping tables with a memoizable function. When users reference the policy-protected column in a query later, the
cached results from the memoizable function are available to use as needed.

### Create a memoizable function[¶](#create-a-memoizable-function "Link to this heading")

You can define a scalar SQL UDF to be memoizable in the [CREATE FUNCTION](../../../sql-reference/sql/create-function) statement by specifying the
`MEMOIZABLE` keyword. You can create a memoizable to function with or without arguments. By using arguments, you have more freedom to
define the SQL UDF. When you write a policy to call the memoizable function, you have more freedom in terms of how to define the policy.

If you specify arguments, the arguments must be constant values with one of the following data types:

* VARCHAR and other string data types.
* NUMBER and other numeric data types.
* TIMESTAMP and other date data types.
* BOOLEAN.

Nonconstant values and their data types, such as [semi-structured data types](../../../user-guide/semistructured-data-formats) and table
columns are not supported.

When you write a memoizable function:

* Specify BOOLEAN or other scalar data types as the `result_data_type`.

  Exercise caution when specifying ARRAY as the `result_data_type` because there are limits to cache size.
* Do not specify other data types such as OBJECT and VARIANT.
* Do not reference another memoizable function in any way.

### Call a memoizable function[¶](#call-a-memoizable-function "Link to this heading")

A memoizable function can be called in a SELECT statement or be included in a policy definition, which then calls the memoizable function
based on the policy conditions.

When calling a memoizable function, note:

* For SQL UDFs that return the ARRAY data type or specify a non-scalar value, use the memoizable function as an argument in the
  [ARRAY\_CONTAINS](../../../sql-reference/functions/array_contains) function.
* Cache size limit:

  Each memoizable function has a 10 KB limit for the current Snowflake session.

  If the memoizable function exceeds this limit for result set cache, Snowflake does not cache the result of calling the
  memoizable function. Instead, the UDF acts as a normal scalar UDF based on how the function is written.
* Cache usage:

  Memoizable functions have a reusable result cache for different SQL statements when the query environment and context do not
  change. Generally, this means the result cache applies to different SQL statements provided that:

  + The access control authorization on objects and columns referenced in a query remain the same.
  + The objects referenced in the query are not modified (e.g. through DML statements).

  The CHILD\_QUERIES\_WAIT\_TIME column in the Account Usage [QUERY\_HISTORY](../../../sql-reference/account-usage/query_history) view records
  the time (in milliseconds) to complete the cached lookup when calling a memoizable function.
* Memoizable functions do not reuse cached results when:

  + The function references a table or other object and there is an update to the referenced table.
  + There is a change in access control to the table.
  + The function calls nondeterministic function.
  + The function calls an external function or a UDF that is not a SQL UDF.

## Examples[¶](#examples "Link to this heading")

### Basic SQL scalar UDF example(s)[¶](#basic-sql-scalar-udf-example-s "Link to this heading")

This example returns a hard-coded approximation of the mathematical constant pi.

```
CREATE FUNCTION pi_udf()
  RETURNS FLOAT
  AS '3.141592654::FLOAT'
  ;
```

Copy

```
SELECT pi_udf();
```

Copy

Output:

```
SELECT pi_udf();
+-------------+
|    PI_UDF() |
|-------------|
| 3.141592654 |
+-------------+
```

Copy

### Common SQL examples[¶](#common-sql-examples "Link to this heading")

#### Query expression with [SELECT](../../../sql-reference/sql/select) statement[¶](#query-expression-with-sql-reference-sql-select-statement "Link to this heading")

Create the table and data to use:

```
CREATE TABLE purchases (number_sold INTEGER, wholesale_price NUMBER(7,2), retail_price NUMBER(7,2));
INSERT INTO purchases (number_sold, wholesale_price, retail_price) VALUES 
   (3,  10.00,  20.00),
   (5, 100.00, 200.00)
   ;
```

Copy

Create the UDF:

```
CREATE FUNCTION profit()
  RETURNS NUMERIC(11, 2)
  AS
  $$
    SELECT SUM((retail_price - wholesale_price) * number_sold)
        FROM purchases
  $$
  ;
```

Copy

Call the UDF in a query:

```
SELECT profit();
```

Copy

Output:

```
SELECT profit();
+----------+
| PROFIT() |
|----------|
|   530.00 |
+----------+
```

Copy

#### UDF in a WITH clause[¶](#udf-in-a-with-clause "Link to this heading")

```
CREATE TABLE circles (diameter FLOAT);

INSERT INTO circles (diameter) VALUES
    (2.0),
    (4.0);

CREATE FUNCTION diameter_to_radius(f FLOAT) 
  RETURNS FLOAT
  AS 
  $$ f / 2 $$
  ;
```

Copy

```
WITH
    radii AS (SELECT diameter_to_radius(diameter) AS radius FROM circles)
  SELECT radius FROM radii
    ORDER BY radius
  ;
```

Copy

Output:

```
+--------+
| RADIUS |
|--------|
|      1 |
|      2 |
+--------+
```

Copy

#### JOIN operation[¶](#join-operation "Link to this heading")

This example uses a more complex query, which includes a JOIN operation:

Create the table and data to use:

```
CREATE TABLE orders (product_ID varchar, quantity integer, price numeric(11, 2), buyer_info varchar);
CREATE TABLE inventory (product_ID varchar, quantity integer, price numeric(11, 2), vendor_info varchar);
INSERT INTO inventory (product_ID, quantity, price, vendor_info) VALUES 
  ('X24 Bicycle', 4, 1000.00, 'HelloVelo'),
  ('GreenStar Helmet', 8, 50.00, 'MellowVelo'),
  ('SoundFX', 5, 20.00, 'Annoying FX Corporation');
INSERT INTO orders (product_id, quantity, price, buyer_info) VALUES 
  ('X24 Bicycle', 1, 1500.00, 'Jennifer Juniper'),
  ('GreenStar Helmet', 1, 75.00, 'Donovan Liege'),
  ('GreenStar Helmet', 1, 75.00, 'Montgomery Python');
```

Copy

Create the UDF:

```
CREATE FUNCTION store_profit()
  RETURNS NUMERIC(11, 2)
  AS
  $$
  SELECT SUM( (o.price - i.price) * o.quantity) 
    FROM orders AS o, inventory AS i 
    WHERE o.product_id = i.product_id
  $$
  ;
```

Copy

Call the UDF in a query:

```
SELECT store_profit();
```

Copy

Output:

```
SELECT store_profit();
+----------------+
| STORE_PROFIT() |
|----------------|
|         550.00 |
+----------------+
```

Copy

The topic [CREATE FUNCTION](../../../sql-reference/sql/create-function) contains additional examples.

### Using UDFs in different clauses[¶](#using-udfs-in-different-clauses "Link to this heading")

A scalar UDF can be used any place a scalar expression can be used. For example:

```
-- ----- These examples show a UDF called from different clauses ----- --

select MyFunc(column1) from table1;

select * from table1 where column2 > MyFunc(column1);
```

Copy

### Using SQL variables in a UDF[¶](#using-sql-variables-in-a-udf "Link to this heading")

This example shows how to set a SQL variable and use that variable inside a UDF:

```
SET id_threshold = (SELECT COUNT(*)/2 FROM table1);
```

Copy

```
CREATE OR REPLACE FUNCTION my_filter_function()
RETURNS TABLE (id int)
AS
$$
SELECT id FROM table1 WHERE id > $id_threshold
$$
;
```

Copy

### Memoizable functions[¶](#memoizable-functions "Link to this heading")

For examples, see:

* Memoizable function without arguments in a [row access policy](../../../user-guide/security-row-using.html#label-security-row-using-example-memoizable-function).
* Memoizable function with arguments in a [masking policy](../../../user-guide/security-column-ddm-use.html#label-security-column-memoizable-function).

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
2. [Memoizable UDFs](#memoizable-udfs)
3. [Examples](#examples)

Related content

1. [User-defined functions overview](/developer-guide/udf/sql/../udf-overview)
2. [Tabular SQL UDFs (UDTFs)](/developer-guide/udf/sql/udf-sql-tabular-functions)
3. [Scalar JavaScript UDFs](/developer-guide/udf/sql/../javascript/udf-javascript-scalar-functions)
4. [Introduction to Java UDFs](/developer-guide/udf/sql/../java/udf-java-introduction)
5. [Function and stored procedure reference](/developer-guide/udf/sql/../../../sql-reference-functions)