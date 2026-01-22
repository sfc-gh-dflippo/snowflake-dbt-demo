---
auto_generated: true
description: Query syntax
last_scraped: '2026-01-14T16:57:04.995978+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/constructs/order-by
title: ORDER BY | Snowflake Documentation
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

[Reference](../../reference.md)[SQL command reference](../../sql-reference-commands.md)[Query syntax](../constructs.md)ORDER BY

Categories:
:   [Query syntax](../constructs)

# ORDER BY[¶](#order-by "Link to this heading")

Specifies an ordering of the rows of the result table from a [SELECT](../sql/select) list.

## Syntax[¶](#syntax "Link to this heading")

**Sorting by specific columns**

```
SELECT ...
  FROM ...
  ORDER BY orderItem [ , orderItem , ... ]
  [ ... ]
```

Copy

Where:

```
orderItem ::= { <column_alias> | <position> | <expr> } [ { ASC | DESC } ] [ NULLS { FIRST | LAST } ]
```

Copy

**Sorting by all columns**

```
SELECT ...
  FROM ...
  ORDER BY ALL [ { ASC | DESC } ] [ NULLS { FIRST | LAST } ]
  [ ... ]
```

Copy

## Parameters[¶](#parameters "Link to this heading")

`column_alias`
:   Column alias appearing in the query block’s [SELECT](../sql/select) list.

`position`
:   Position of an expression in the [SELECT](../sql/select) list.

`expr`
:   Any expression on tables in the current scope.

`{ ASC | DESC }`
:   Optionally returns the values of the sort key in ascending (lowest to highest) or descending (highest to lowest) order.

    Default: ASC

`NULLS { FIRST | LAST }`
:   Optionally specifies whether NULL values are returned before/after non-NULL values, based on the sort order (ASC or DESC).

    Default: Depends on the sort order (ASC or DESC); see the usage notes below for details

`ALL`
:   Sorts the results by all of the columns specified in the SELECT list. The results are sorted by the columns in the order in
    which they appear.

    For example, suppose that the SELECT list contains:

    ```
    SELECT col_1, col_2, col_3
      FROM my_table
      ORDER BY ALL;
    ```

    Copy

    The results are sorted first by `col_1`, then by `col_2`, and then by `col_3`.

    Note

    You cannot specify ORDER BY ALL if a column in the SELECT list uses an aggregate function.

## Usage notes[¶](#usage-notes "Link to this heading")

* All data is sorted according to the numeric byte value of each character in the ASCII table. UTF-8 encoding is supported.
* For numeric values, leading zeros before the decimal point and trailing zeros (`0`) after the decimal point have no effect on sort order.
* When NULLS FIRST or NULLS LAST isn’t specified, the ordering of NULL values depends on the setting of the
  [DEFAULT\_NULL\_ORDERING](../parameters.html#label-default-null-ordering) parameter and the sort order:

  + When the sort order is ASC (the default) and the DEFAULT\_NULL\_ORDERING parameter is set to `LAST`
    (the default), NULL values are returned last. Therefore, unless specified otherwise, NULL values are considered to be higher than
    any non-NULL values.
  + When the sort order is ASC and the DEFAULT\_NULL\_ORDERING parameter is set to `FIRST`, NULL values are returned first.
  + When the sort order is DESC and the DEFAULT\_NULL\_ORDERING parameter is set to `FIRST`, NULL values are returned last.
  + When the sort order is DESC and the DEFAULT\_NULL\_ORDERING parameter is set to `LAST`, NULL values are returned first.
* The sort order isn’t guaranteed to be consistent for values of different data types in
  [semi-structured](../data-types-semistructured) data, such as an array that contains elements of
  different data types.
* Top-K pruning can improve the performance of queries that include both [LIMIT](limit) and ORDER BY clauses. For more
  information, see [Top-K pruning for improved query performance](../../user-guide/querying-top-k-pruning-optimization).
* An ORDER BY can be used at different levels in a query, for example in a subquery or inside an OVER() subclause.
  An ORDER BY inside a subquery or subclause applies only within that subquery or subclause. For example, the ORDER BY
  in the following query orders results only within the subquery, not the outermost level of the query:

  ```
  SELECT * 
    FROM (
      SELECT branch_name
        FROM branch_offices
        ORDER BY monthly_sales DESC
        LIMIT 3
    );
  ```

  Copy

  In this example, the ORDER BY is specified in the subquery, so the subquery returns the names in order of monthly
  sales. The ORDER BY in the subquery does not apply to the outer query. This query returns the names of the three
  branches that had the highest monthly sales, but not necessarily in order by monthly sales.

  Sorting can be expensive. If you want the results of the outer query sorted, use an `ORDER BY` clause only at the
  top level of the query, and avoid using `ORDER BY` clauses in subqueries unless necessary.

## Examples[¶](#examples "Link to this heading")

The following examples demonstrate how to use ORDER BY to sort the results:

* [Sorting by string values](#label-order-by-examples-strings)
* [Sorting by numeric values](#label-order-by-examples-numbers)
* [Sorting NULLS first or last](#label-order-by-examples-nulls)

### Sorting by string values[¶](#sorting-by-string-values "Link to this heading")

The following example sorts the results by string values:

```
SELECT column1
  FROM VALUES
    ('a'), ('1'), ('B'), (null), ('2'), ('01'), ('05'),
    (' this'), ('this'), ('this and that'), ('&'), ('%')
  ORDER BY column1;
```

Copy

```
+---------------+
| COLUMN1       |
|---------------|
|  this         |
| %             |
| &             |
| 01            |
| 05            |
| 1             |
| 2             |
| B             |
| a             |
| this          |
| this and that |
| NULL          |
+---------------+
```

### Sorting by numeric values[¶](#sorting-by-numeric-values "Link to this heading")

The following example sorts the results by numeric values:

```
SELECT column1
  FROM VALUES
    (3), (4), (null), (1), (2), (6),
    (5), (0005), (.05), (.5), (.5000)
  ORDER BY column1;
```

Copy

```
+---------+
| COLUMN1 |
|---------|
|    0.05 |
|    0.50 |
|    0.50 |
|    1.00 |
|    2.00 |
|    3.00 |
|    4.00 |
|    5.00 |
|    5.00 |
|    6.00 |
|    NULL |
+---------+
```

### Sorting NULLS first or last[¶](#sorting-nulls-first-or-last "Link to this heading")

The following example configures all queries in the session to sort NULLS last by setting the [DEFAULT\_NULL\_ORDERING](../parameters.html#label-default-null-ordering)
parameter to `LAST`.

```
ALTER SESSION SET DEFAULT_NULL_ORDERING = 'LAST';
```

Copy

```
SELECT column1
  FROM VALUES (1), (null), (2), (null), (3)
  ORDER BY column1;
```

Copy

```
+---------+
| COLUMN1 |
|---------|
|       1 |
|       2 |
|       3 |
|    NULL |
|    NULL |
+---------+
```

```
SELECT column1
  FROM VALUES (1), (null), (2), (null), (3)
  ORDER BY column1 DESC;
```

Copy

```
+---------+
| COLUMN1 |
|---------|
|    NULL |
|    NULL |
|       3 |
|       2 |
|       1 |
+---------+
```

The following example overrides the DEFAULT\_NULL\_ORDERING parameter by specifying NULLS FIRST in a query:

```
SELECT column1
  FROM VALUES (1), (null), (2), (null), (3)
  ORDER BY column1 NULLS FIRST;
```

Copy

```
+---------+
| COLUMN1 |
|---------|
|    NULL |
|    NULL |
|       1 |
|       2 |
|       3 |
+---------+
```

The following example sets the DEFAULT\_NULL\_ORDERING parameter to `FIRST` to sort NULLS first:

```
ALTER SESSION SET DEFAULT_NULL_ORDERING = 'FIRST';
```

Copy

```
SELECT column1
  FROM VALUES (1), (null), (2), (null), (3)
  ORDER BY column1;
```

Copy

```
+---------+
| COLUMN1 |
|---------|
|    NULL |
|    NULL |
|       1 |
|       2 |
|       3 |
+---------+
```

```
SELECT column1
  FROM VALUES (1), (null), (2), (null), (3)
  ORDER BY column1 DESC;
```

Copy

```
+---------+
| COLUMN1 |
|---------|
|       3 |
|       2 |
|       1 |
|    NULL |
|    NULL |
+---------+
```

The following example overrides the DEFAULT\_NULL\_ORDERING parameter by specifying NULLS LAST in a query:

```
SELECT column1
  FROM VALUES (1), (null), (2), (null), (3)
  ORDER BY column1 NULLS LAST;
```

Copy

```
+---------+
| COLUMN1 |
|---------|
|       1 |
|       2 |
|       3 |
|    NULL |
|    NULL |
+---------+
```

### Sorting by all columns in the SELECT list[¶](#sorting-by-all-columns-in-the-select-list "Link to this heading")

To run the examples in this section, create the following table:

```
CREATE OR REPLACE TABLE my_sort_example(a NUMBER, s VARCHAR, b BOOLEAN);

INSERT INTO my_sort_example VALUES
  (0, 'abc', TRUE),
  (0, 'abc', FALSE),
  (0, 'abc', NULL),
  (0, 'xyz', FALSE),
  (0, NULL, FALSE),
  (1, 'xyz', TRUE),
  (NULL, 'xyz', FALSE);
```

Copy

The following example sorts the results by all columns in the table:

```
SELECT * FROM my_sort_example
  ORDER BY ALL;
```

Copy

As shown below, the results are sorted first by the `a` column, then by the `s` column, and then by the `b` column (the
order in which the columns were defined in the table).

```
+------+------+-------+
| A    | S    | B     |
|------+------+-------|
| 0    | abc  | False |
| 0    | abc  | True  |
| 0    | abc  | NULL  |
| 0    | xyz  | False |
| 0    | NULL | False |
| 1    | xyz  | True  |
| NULL | xyz  | False |
+------+------+-------+
```

The following example sorts the results in ascending order:

```
SELECT * FROM my_sort_example
  ORDER BY ALL ASC;
```

Copy

```
+------+------+-------+
| A    | S    | B     |
|------+------+-------|
| 0    | abc  | False |
| 0    | abc  | True  |
| 0    | abc  | NULL  |
| 0    | xyz  | False |
| 0    | NULL | False |
| 1    | xyz  | True  |
| NULL | xyz  | False |
+------+------+-------+
```

The following example sets the DEFAULT\_NULL\_ORDERING parameter to sort NULL values last for all queries executed during the
session:

```
ALTER SESSION SET DEFAULT_NULL_ORDERING = 'LAST';
```

Copy

```
SELECT * FROM my_sort_example
  ORDER BY ALL;
```

Copy

```
+------+------+-------+
| A    | S    | B     |
|------+------+-------|
| NULL | xyz  | False |
| 0    | NULL | False |
| 0    | abc  | NULL  |
| 0    | abc  | False |
| 0    | abc  | True  |
| 0    | xyz  | False |
| 1    | xyz  | True  |
+------+------+-------+
```

The following example specifies NULLS FIRST in a query to override that setting:

```
SELECT * FROM my_sort_example
  ORDER BY ALL NULLS FIRST;
```

Copy

```
+------+------+-------+
| A    | S    | B     |
|------+------+-------|
| NULL | xyz  | False |
| 0    | NULL | False |
| 0    | abc  | NULL  |
| 0    | abc  | False |
| 0    | abc  | True  |
| 0    | xyz  | False |
| 1    | xyz  | True  |
+------+------+-------+
```

The following example returns the columns in the order `b`, `s`, and `a`. The results are sorted first by `b`, then by
`s`, and then by `a`:

```
SELECT b, s, a FROM my_sort_example
  ORDER BY ALL NULLS LAST;
```

Copy

```
+-------+------+------+
| B     | S    | A    |
|-------+------+------|
| False | abc  | 0    |
| False | xyz  | 0    |
| False | xyz  | NULL |
| False | NULL | 0    |
| True  | abc  | 0    |
| True  | xyz  | 1    |
| NULL  | abc  | 0    |
+-------+------+------+
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
5. [Sorting by string values](#sorting-by-string-values)
6. [Sorting by numeric values](#sorting-by-numeric-values)
7. [Sorting NULLS first or last](#sorting-nulls-first-or-last)
8. [Sorting by all columns in the SELECT list](#sorting-by-all-columns-in-the-select-list)