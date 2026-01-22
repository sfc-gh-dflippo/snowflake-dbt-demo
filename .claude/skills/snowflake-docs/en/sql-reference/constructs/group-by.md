---
auto_generated: true
description: Query syntax
last_scraped: '2026-01-14T16:55:01.669577+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/constructs/group-by
title: GROUP BY | Snowflake Documentation
---

1. [Overview](../../reference.md)
2. [SQL data types reference](../../sql-reference-data-types.md)
3. [SQL command reference](../../sql-reference-commands.md)

   * [Query syntax](../constructs.md)

     + [SELECT](../sql/select.md)
     + [WITH](with.md)
     + [TOP <n>](top_n.md)
     + [INTO](into.md)
     + [FROM](from.md)
     + [AT](at-before.md)
     + [BEFORE](at-before.md)
     + [CHANGES](changes.md)
     + [CONNECT BY](connect-by.md)
     + [JOIN](join.md)
     + [ASOF JOIN](asof-join.md)
     + [LATERAL](join-lateral.md)
     + [MATCH\_RECOGNIZE](match_recognize.md)
     + [PIVOT](pivot.md)
     + [UNPIVOT](unpivot.md)
     + [VALUES](values.md)
     + [SAMPLE / TABLESAMPLE](sample.md)
     + [RESAMPLE](resample.md)
     + [SEMANTIC\_VIEW](semantic_view.md)
     + [WHERE](where.md)
     + [GROUP BY](group-by.md)
     + [GROUP BY CUBE](group-by-cube.md)
     + [GROUP BY GROUPING SETS](group-by-grouping-sets.md)
     + [GROUP BY ROLLUP](group-by-rollup.md)
     + [HAVING](having.md)
     + [QUALIFY](qualify.md)
     + [ORDER BY](order-by.md)
     + [LIMIT](limit.md)
     + [FETCH](limit.md)
     + [FOR UPDATE](for-update.md)
   * [Query operators](../operators.md)
   * [General DDL](../sql-ddl-summary.md)
   * [General DML](../sql-dml.md)
   * [All commands (alphabetical)](../sql-all.md)")
   * [Accounts](../commands-account.md)
   * [Users, roles, & privileges](../commands-user-role.md)
   * [Integrations](../commands-integration.md)
   * [Business continuity & disaster recovery](../commands-replication.md)
   * [Sessions](../commands-session.md)
   * [Transactions](../commands-transaction.md)
   * [Virtual warehouses & resource monitors](../commands-warehouse.md)
   * [Databases, schemas, & shares](../commands-database.md)
   * [Tables, views, & sequences](../commands-table.md)
   * [Functions, procedures, & scripting](../commands-function.md)
   * [Streams & tasks](../commands-stream.md)
   * [dbt Projects on Snowflake](../commands-dbt-projects-on-snowflake.md)
   * [Classes & instances](../commands-class.md)
   * [Machine learning](../commands-ml.md)
   * [Cortex](../commands-cortex.md)
   * [Listings](../commands-listings.md)
   * [Openflow data plane integration](../commands-ofdata-plane.md)
   * [Organization profiles](../commands-organization-profiles.md)
   * [Security](../commands-security.md)
   * [Data Governance](../commands-data-governance.md)
   * [Privacy](../commands-privacy.md)
   * [Data loading & unloading](../commands-data-loading.md)
   * [File staging](../commands-file.md)
   * [Storage lifecycle policies](../commands-storage-lifecycle-policies.md)
   * [Git](../commands-git.md)
   * [Alerts](../commands-alert.md)
   * [Native Apps Framework](../commands-native-apps.md)
   * [Streamlit](../commands-streamlit.md)
   * [Notebook](../commands-notebook.md)
   * [Snowpark Container Services](../commands-snowpark-container-services.md)
4. [Function and stored procedure reference](../../sql-reference-functions.md)
5. [Class reference](../../sql-reference-classes.md)
6. [Scripting reference](../../sql-reference-snowflake-scripting.md)
7. [General reference](../../sql-reference.md)
8. [API reference](../../api-reference.md)

[Reference](../../reference.md)[SQL command reference](../../sql-reference-commands.md)[Query syntax](../constructs.md)GROUP BY

Categories:
:   [Query syntax](../constructs)

# GROUP BY[¶](#group-by "Link to this heading")

Groups rows with the same group-by-item expressions and computes aggregate functions for the resulting group. A GROUP BY
expression can be:

* A column name.
* A number referencing a position in the [SELECT](../sql/select) list.
* A general expression.

Extensions:
:   [GROUP BY CUBE](group-by-cube) , [GROUP BY GROUPING SETS](group-by-grouping-sets) , [GROUP BY ROLLUP](group-by-rollup)

## Syntax[¶](#syntax "Link to this heading")

```
SELECT ...
  FROM ...
  [ ... ]
  GROUP BY groupItem [ , groupItem [ , ... ] ]
  [ ... ]
```

Copy

```
SELECT ...
  FROM ...
  [ ... ]
  GROUP BY ALL
  [ ... ]
```

Copy

Where:

> ```
> groupItem ::= { <column_alias> | <position> | <expr> }
> ```
>
> Copy

## Parameters[¶](#parameters "Link to this heading")

`column_alias`
:   Column alias appearing in the query block’s [SELECT](../sql/select) list.

`position`
:   Position of an expression in the [SELECT](../sql/select) list.

`expr`
:   Any expression on tables in the current scope.

`GROUP BY ALL`
:   Specifies that all items in the SELECT list that do not use aggregate functions should be used for grouping.

    For examples, refer to [Group by all columns](#label-group-by-all-columns).

## Usage notes[¶](#usage-notes "Link to this heading")

* A GROUP BY clause can reference expressions in the projection clause by name or by position.
  If the GROUP BY clause references by name, then each reference is resolved as follows:

  + If the query contains a database object (e.g. table or view) with a matching column name, then the reference is resolved to the
    column name.
  + Otherwise, if the projection clause of the SELECT contains an expression alias with a matching name, then the reference is
    resolved to the alias.

  For an example, see [Precedence when a column name and an alias match](#label-group-by-precedence-when-shadowing).
* If all SELECT items use aggregate functions, specifying GROUP BY ALL is equivalent to specifying the statement without the
  GROUP BY clause.

  For example, the following statement only has SELECT items that use aggregate functions:

  ```
  SELECT SUM(amount)
    FROM mytable
    GROUP BY ALL;
  ```

  Copy

  The statement above is equivalent to not specifying the GROUP by clause:

  ```
  SELECT SUM(amount)
    FROM mytable;
  ```

  Copy

## Examples[¶](#examples "Link to this heading")

The following sections provide examples of using the GROUP BY clause:

* [Group by one column](#label-group-by-one-column)
* [Group by multiple columns](#label-group-by-multiple-columns)
* [Group by all columns](#label-group-by-all-columns)
* [Precedence when a column name and an alias match](#label-group-by-precedence-when-shadowing)

Note that the examples in each section use the data that you set up in [Setting up the data for the examples](#label-group-by-sample-data-setup).

### Setting up the data for the examples[¶](#setting-up-the-data-for-the-examples "Link to this heading")

The examples in this section use a table named `sales` and a table named `product`. To create these tables and insert the
data needed for the example, execute the following statements:

```
CREATE TABLE sales (
  product_ID INTEGER,
  retail_price REAL,
  quantity INTEGER,
  city VARCHAR,
  state VARCHAR);

INSERT INTO sales (product_id, retail_price, quantity, city, state) VALUES
  (1, 2.00,  1, 'SF', 'CA'),
  (1, 2.00,  2, 'SJ', 'CA'),
  (2, 5.00,  4, 'SF', 'CA'),
  (2, 5.00,  8, 'SJ', 'CA'),
  (2, 5.00, 16, 'Miami', 'FL'),
  (2, 5.00, 32, 'Orlando', 'FL'),
  (2, 5.00, 64, 'SJ', 'PR');

CREATE TABLE products (
  product_ID INTEGER,
  wholesale_price REAL);
INSERT INTO products (product_ID, wholesale_price) VALUES (1, 1.00);
INSERT INTO products (product_ID, wholesale_price) VALUES (2, 2.00);
```

Copy

### Group by one column[¶](#group-by-one-column "Link to this heading")

This example shows the gross revenue per product, grouped by `product_id` (i.e. the total amount of money received for
each product):

```
SELECT product_ID, SUM(retail_price * quantity) AS gross_revenue
  FROM sales
  GROUP BY product_ID;
```

Copy

```
+------------+---------------+
| PRODUCT_ID | GROSS_REVENUE |
+============+===============+
|          1 |          6    |
+------------+---------------+
|          2 |        620    |
+------------+---------------+
```

The following example builds on the previous example, showing the net profit per product, grouped by `product_id`:

```
SELECT p.product_ID, SUM((s.retail_price - p.wholesale_price) * s.quantity) AS profit
  FROM products AS p, sales AS s
  WHERE s.product_ID = p.product_ID
  GROUP BY p.product_ID;
```

Copy

```
+------------+--------+
| PRODUCT_ID | PROFIT |
+============+========+
|          1 |      3 |
+------------+--------+
|          2 |    372 |
+------------+--------+
```

### Group by multiple columns[¶](#group-by-multiple-columns "Link to this heading")

The following example demonstrates how to group by multiple columns:

```
SELECT state, city, SUM(retail_price * quantity) AS gross_revenue
  FROM sales
  GROUP BY state, city;
```

Copy

```
+-------+---------+---------------+
| STATE |   CITY  | GROSS REVENUE |
+=======+=========+===============+
|   CA  | SF      |            22 |
+-------+---------+---------------+
|   CA  | SJ      |            44 |
+-------+---------+---------------+
|   FL  | Miami   |            80 |
+-------+---------+---------------+
|   FL  | Orlando |           160 |
+-------+---------+---------------+
|   PR  | SJ      |           320 |
+-------+---------+---------------+
```

### Group by all columns[¶](#group-by-all-columns "Link to this heading")

The following example is equivalent to the example used in [Group by multiple columns](#label-group-by-multiple-columns).

```
SELECT state, city, SUM(retail_price * quantity) AS gross_revenue
  FROM sales
  GROUP BY ALL;
```

Copy

```
+-------+---------+---------------+
| STATE |   CITY  | GROSS REVENUE |
+=======+=========+===============+
|   CA  | SF      |            22 |
+-------+---------+---------------+
|   CA  | SJ      |            44 |
+-------+---------+---------------+
|   FL  | Miami   |            80 |
+-------+---------+---------------+
|   FL  | Orlando |           160 |
+-------+---------+---------------+
|   PR  | SJ      |           320 |
+-------+---------+---------------+
```

### Precedence when a column name and an alias match[¶](#precedence-when-a-column-name-and-an-alias-match "Link to this heading")

It is possible (but usually not recommended) to create a query that contains an alias that matches a column name:

```
SELECT x, some_expression AS x
  FROM ...
```

Copy

If a clause contains a name that matches both a column name and an alias, then the clause uses the column name. The following example demonstrates this behavior using a GROUP BY clause:

Create a table and insert rows:

```
CREATE TABLE employees (salary FLOAT, state VARCHAR, employment_state VARCHAR);
INSERT INTO employees (salary, state, employment_state) VALUES
  (60000, 'California', 'Active'),
  (70000, 'California', 'On leave'),
  (80000, 'Oregon', 'Active');
```

Copy

The following query returns the sum of the salaries of the employees who are active and the sum of the salaries of the employees who
are on leave:

```
SELECT SUM(salary), ANY_VALUE(employment_state)
  FROM employees
  GROUP BY employment_state;
```

Copy

```
+-------------+-----------------------------+
| SUM(SALARY) | ANY_VALUE(EMPLOYMENT_STATE) |
|-------------+-----------------------------|
|      140000 | Active                      |
|       70000 | On leave                    |
+-------------+-----------------------------+
```

The next query uses the alias `state`, which matches the name of a column of the table in the query. When `state` is used in
the GROUP BY clause, Snowflake interprets it as a reference to the column name, not the alias. This query therefore returns the sum of
the salaries of the employees in the state of California and the sum of the salaries of the employees in the state of Oregon,
yet displays `employment_state` information (that is, `Active`) rather than the names of states or provinces.

```
SELECT SUM(salary), ANY_VALUE(employment_state) AS state
  FROM employees
  GROUP BY state;
```

Copy

```
+-------------+--------+
| SUM(SALARY) | STATE  |
|-------------+--------|
|      130000 | Active |
|       80000 | Active |
+-------------+--------+
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

### Alternative interfaces

[Snowflake Python APIs](/developer-guide/snowflake-python-api/snowflake-python-overview)[Snowflake REST APIs](/developer-guide/snowflake-rest-api/snowflake-rest-api)[Snowflake CLI](/developer-guide/snowflake-cli/index)

See all interfaces

On this page

1. [Syntax](#syntax)
2. [Parameters](#parameters)
3. [Usage notes](#usage-notes)
4. [Examples](#examples)