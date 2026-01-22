---
auto_generated: true
description: Some stored procedures return tabular data. To select and manipulate
  this tabular data, you can call these stored procedures in the FROM clause of a
  SELECT statement.
last_scraped: '2026-01-14T16:55:56.348744+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/developer-guide/stored-procedure/stored-procedures-selecting-from
title: Selecting from a stored procedure | Snowflake Documentation
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

[Developer](../../developer.md)[Functions and procedures](../extensibility.md)[Stored procedures](stored-procedures-overview.md)Selecting from

# Selecting from a stored procedure[¶](#selecting-from-a-stored-procedure "Link to this heading")

Some stored procedures return tabular data. To select and manipulate this tabular data, you can call these
stored procedures in the [FROM](../../sql-reference/constructs/from) clause of a SELECT statement.

## Run a SELECT statement with the TABLE keyword[¶](#run-a-select-statement-with-the-table-keyword "Link to this heading")

When calling the stored procedure, omit the [CALL](../../sql-reference/sql/call) command. Instead, use the TABLE keyword,
and name the procedure inside parentheses:

```
SELECT ... FROM TABLE( <stored_procedure_name>( <arg> [ , <arg> ... ] ) );
```

Copy

## Example that selects from a stored procedure[¶](#example-that-selects-from-a-stored-procedure "Link to this heading")

This example uses the data in the following table:

```
CREATE OR REPLACE TABLE orders (
  order_id INT,
  u_id VARCHAR,
  order_date DATE,
  order_amount NUMBER(12,2));

INSERT INTO orders VALUES (1, 'user_id_001', current_date, 500.00);
INSERT INTO orders VALUES (2, 'user_id_003', current_date, 225.00);
INSERT INTO orders VALUES (3, 'user_id_001', current_date, 725.00);
INSERT INTO orders VALUES (4, 'user_id_002', current_date, 150.00);
INSERT INTO orders VALUES (5, 'user_id_002', current_date, 900.00);
```

Copy

The following stored procedure returns order information based on a user ID:

```
CREATE OR REPLACE PROCEDURE find_orders_by_user_id(user_id VARCHAR)
RETURNS TABLE (
  order_id INT, order_date DATE, order_amount NUMBER(12,2)
)
LANGUAGE SQL AS
DECLARE
  res RESULTSET;
BEGIN
  res := (SELECT order_id, order_date, order_amount FROM orders WHERE u_id = :user_id);
  RETURN TABLE(res);
END;
```

Copy

Note: If you use [Snowflake CLI](../snowflake-cli/index), [SnowSQL](../../user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](../python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](../snowflake-scripting/running-examples)):

```
CREATE OR REPLACE PROCEDURE find_orders_by_user_id(user_id VARCHAR)
RETURNS TABLE (
  order_id INT, order_date DATE, order_amount NUMBER(12,2)
)
LANGUAGE SQL AS
$$
DECLARE
  res RESULTSET;
BEGIN
  res := (SELECT order_id, order_date, order_amount FROM orders WHERE u_id = :user_id);
  RETURN TABLE(res);
END;
$$
;
```

Copy

The following SELECT statement retrieves the stored procedure’s results:

```
SELECT * FROM TABLE(find_orders_by_user_id('user_id_001'));
```

Copy

```
+----------+------------+--------------+
| ORDER_ID | ORDER_DATE | ORDER_AMOUNT |
|----------+------------+--------------|
|        1 | 2024-08-30 |       500.00 |
|        3 | 2024-08-30 |       725.00 |
+----------+------------+--------------+
```

## Limitations for selecting from a stored procedure[¶](#limitations-for-selecting-from-a-stored-procedure "Link to this heading")

The following limitations apply to selecting from a stored procedure:

* Only stored procedures that perform SELECT, SHOW, DESCRIBE, or CALL statements can be placed in the FROM clause
  of a SELECT statement. Stored procedures that make modifications using DDL or DML operations aren’t allowed.
  For stored procedures that issue CALL statements, these limitations apply to the stored procedures that are called.
* Only stored procedures that return tabular data with a static output schema can be placed in the FROM clause
  of a SELECT statement. The output columns must be named and typed. For example, a stored procedure with the
  following RETURNS clause is supported:

  ```
  RETURNS TABLE (col1 INT, col2 STRING)
  ```

  Copy

  A stored procedure with the following RETURNS clause is not supported because it doesn’t return tabular data:

  ```
  RETURNS STRING
  ```

  Copy

  A stored procedure with the following RETURNS clause is not supported because it doesn’t provide
  a fixed output schema:

  ```
  RETURNS TABLE()
  ```

  Copy
* The stored procedure must be called in the FROM clause of a SELECT block in one of the following statements:

  + [SELECT](../../sql-reference/sql/select)
  + [INSERT](../../sql-reference/sql/insert), [UPDATE](../../sql-reference/sql/update), [DELETE](../../sql-reference/sql/delete), or [MERGE](../../sql-reference/sql/merge)
  + [CREATE TABLE AS SELECT](../../sql-reference/sql/create-table.html#label-ctas-syntax)
* The stored procedure can’t accept correlated input arguments from their outer scope, such as a reference to any
  [CTE](../../user-guide/queries-cte) defined outside of the SELECT statement.
* If an argument contains a subquery, then that subquery can’t use a CTE defined by the WITH clause.
* A SELECT statement containing a stored procedure call can’t be used in the body of a view, a user-defined function (UDF),
  a user-defined table function (UDTF), or in objects such as [row access policies](../../user-guide/security-row-intro) and
  [data masking policies](../../user-guide/security-column-intro).
* You can’t use [bind variables](../../sql-reference/bind-variables) in a SELECT statement that calls a stored
  procedure. For example, the following SELECT statements aren’t allowed:

  ```
  SELECT * FROM TABLE(my_stored_procedure(?));

  SELECT * FROM TABLE(my_stored_procedure('a')) WHERE my_var = :var2;
  ```

  Copy

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

1. [Run a SELECT statement with the TABLE keyword](#run-a-select-statement-with-the-table-keyword)
2. [Example that selects from a stored procedure](#example-that-selects-from-a-stored-procedure)
3. [Limitations for selecting from a stored procedure](#limitations-for-selecting-from-a-stored-procedure)

Related content

1. [CREATE PROCEDURE](/developer-guide/stored-procedure/../../sql-reference/sql/create-procedure)