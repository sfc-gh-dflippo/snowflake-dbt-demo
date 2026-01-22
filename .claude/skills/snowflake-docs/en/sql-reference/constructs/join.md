---
auto_generated: true
description: Query syntax
last_scraped: '2026-01-14T16:55:02.559730+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/constructs/join
title: JOIN | Snowflake Documentation
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

[Reference](../../reference.md)[SQL command reference](../../sql-reference-commands.md)[Query syntax](../constructs.md)JOIN

Categories:
:   [Query syntax](../constructs)

# JOIN[¶](#join "Link to this heading")

A `JOIN` operation combines rows from two tables — or other table-like sources, such as
views or table functions — to create a new combined row that can be used in the query.
For a conceptual explanation of joins, see [Working with joins](../../user-guide/querying-joins).

This topic describes how to use the `JOIN` subclause in the [FROM](from) clause.
The `JOIN` subclause specifies, explicitly or implicitly, how to relate rows
in one table to the corresponding rows in the other table. You can also use the [ASOF JOIN](asof-join)
subclause, which is used to join time-series data on timestamp columns when their values closely follow each other,
precede each other, or match exactly.

Although the recommended way to join tables is to use `JOIN` with the `ON` subclause of the `FROM` clause,
an alternative way to join tables is to use the `WHERE` clause. For details, see the documentation for the
[WHERE](where) clause.

## Syntax[¶](#syntax "Link to this heading")

Use one of the following:

```
SELECT ...
FROM <object_ref1> [
                     {
                       INNER
                       | { LEFT | RIGHT | FULL } [ OUTER ]
                     }
                     [ DIRECTED ]
                   ]
                   JOIN <object_ref2>
  [ ON <condition> ]
[ ... ]
```

Copy

```
SELECT *
FROM <object_ref1> [
                     {
                       INNER
                       | { LEFT | RIGHT | FULL } [ OUTER ]
                     }
                     [ DIRECTED ]
                   ]
                   JOIN <object_ref2>
  [ USING( <column_list> ) ]
[ ... ]
```

Copy

```
SELECT ...
FROM <object_ref1> [
                     {
                       NATURAL [
                                 {
                                   INNER
                                   | { LEFT | RIGHT | FULL } [ OUTER ]
                                 }
                                 [ DIRECTED ]
                               ]
                       | CROSS  [ DIRECTED ]
                     }
                   ]
                   JOIN <object_ref2>
[ ... ]
```

Copy

## Parameters[¶](#parameters "Link to this heading")

`object_ref1` and `object_ref2`
:   Each object reference is a table or table-like data source.

`JOIN`
:   Use the `JOIN` keyword to specify that the tables should be joined. Combine `JOIN` with other join-related
    keywords — for example, `INNER` or `OUTER` — to specify the type of join.

    The semantics of joins are as follows (for brevity, this topic uses `o1` and
    `o2` for `object_ref1` and `object_ref2`, respectively).

    | Join Type | Semantics |
    | --- | --- |
    | `o1 INNER JOIN o2` | For each row of `o1`, a row is produced for each row of `o2` that matches according to the `ON condition` subclause. (You can also use a comma to specify an inner join. For an example, see the [examples section](#label-join-examples).) If you use `INNER JOIN` without the `ON` clause, or if you use a comma without a `WHERE` clause, the result is the same as using `CROSS JOIN`: a Cartesian product; every row of `o1` paired with every row of `o2`. |
    | `o1 LEFT OUTER JOIN o2` | The result of the inner join is augmented with a row for each row of `o1` that has no matches in `o2`. The result columns referencing `o2` contain null. |
    | `o1 RIGHT OUTER JOIN o2` | The result of the inner join is augmented with a row for each row of `o2` that has no matches in `o1`. The result columns referencing `o1` contain null. |
    | `o1 FULL OUTER JOIN o2` | Returns all joined rows, plus one row for each unmatched left side row (extended with nulls on the right), plus one row for each unmatched right side row (extended with nulls on the left). |
    | `o1 CROSS JOIN o2` | For every possible combination of rows from `o1` and `o2` (that is, Cartesian product), the joined table contains a row consisting of all columns in `o1` followed by all columns in `o2`. A `CROSS JOIN` can’t be combined with an `ON condition` clause. However, you can use a `WHERE` clause to filter the results. |
    | `o1 NATURAL JOIN o2` | A `NATURAL JOIN` is identical to an explicit `JOIN` on the common columns of the two tables, except that the common columns are included only once in the output. (A natural join assumes that columns with the same name, but in different tables, contain corresponding data.) For examples, see the [examples section](#label-join-examples). A `NATURAL JOIN` can be combined with an `OUTER JOIN`. A `NATURAL JOIN` can’t be combined with an `ON condition` clause because the `JOIN` condition is already implied. However, you can use a `WHERE` clause to filter the results. |

    The `DIRECTED` keyword specifies a *directed join*, which enforces the join order of the tables. The first, or left,
    table is scanned before the second, or right, table. For example, `o1 INNER DIRECTED JOIN o2` scans the `o1`
    table before the `o2` table. Directed joins are useful in the following situations:

    * You are migrating workloads into Snowflake that have join order directives.
    * You want to improve performance by scanning join tables in a specific order.

    Default: `INNER JOIN`

    If the word `JOIN` is used without specifying `INNER` or `OUTER`, then the `JOIN` is an inner join.

    If the `DIRECTED` keyword is added, the join type — for example, `INNER`, `LEFT`,
    `RIGHT`, or `FULL` — is required.

    See also:

    * [LATERAL](join-lateral)
    * [ASOF JOIN](asof-join)

`ON condition`
:   A [Boolean expression](../data-types-logical) that defines the rows from the two sides of the `JOIN`
    that are considered to match, for example:

    ```
    ON object_ref2.id_number = object_ref1.id_number
    ```

    Copy

    Conditions are discussed in more detail in the [WHERE](where) clause documentation.



    The `ON` clause is prohibited for `CROSS JOIN`.

    The `ON` clause is unnecessary, and prohibited, for
    `NATURAL JOIN` because the join columns are implied.

    For other joins, the `ON` clause is optional. However, omitting
    the `ON` clause results in a Cartesian product; every row of
    `object_ref1` paired with every row of `object_ref2`. A
    Cartesian product can produce a very large volume of output, almost all of
    which consists of pairs of rows that aren’t actually related, which consumes
    a lot of resources and is often a user error.

`USING( column_list )`
:   A list of columns in common between the two tables being joined. These
    columns are used as the join columns. The columns must have the same
    name and meaning in each of the tables being joined.

    For example, suppose that the SQL statement contains:

    ```
    ... o1 JOIN o2
        USING (key_column)
    ```

    Copy

    In the simple case, this would be equivalent to:

    ```
    ... o1 JOIN o2
        ON o2.key_column = o1.key_column
    ```

    Copy

    In the standard JOIN syntax, the projection list (the list of columns
    and other expressions after the SELECT keyword) is `*`. This causes
    the query to return the `key_column` exactly once. The columns
    are returned in the following order:

    * The columns in the `USING` clause in the order specified.
    * The left table columns not specified in the `USING` clause.
    * The right table columns not specified in the `USING` clause.

    For examples of standard and nonstandard usage, see the [examples section](#label-join-examples).

## Usage notes[¶](#usage-notes "Link to this heading")

* The following restrictions apply to table functions other than SQL UDTFs:

  + You can’t specify the `ON`, `USING`, or `NATURAL JOIN` clause in a lateral table
    function, other than a SQL UDTF.

    For example, the following syntax is not allowed:

    ```
    SELECT ... FROM my_table
      JOIN TABLE(FLATTEN(input=>[col_a]))
      ON ... ;
    ```

    Copy

    ```
    SELECT ... FROM my_table
      INNER JOIN TABLE(FLATTEN(input=>[col_a]))
      ON ... ;
    ```

    Copy

    ```
    SELECT ... FROM my_table
      JOIN TABLE(my_js_udtf(col_a))
      ON ... ;
    ```

    Copy

    ```
    SELECT ... FROM my_table
      INNER JOIN TABLE(my_js_udtf(col_a))
      ON ... ;
    ```

    Copy
  + You can’t specify the `ON`, `USING`, or `NATURAL JOIN` clause in an outer lateral join
    to a table function, other than a SQL UDTF.

    For example, the following syntax is not allowed:

    ```
    SELECT ... FROM my_table
      LEFT JOIN TABLE(FLATTEN(input=>[a]))
      ON ... ;
    ```

    Copy

    ```
    SELECT ... FROM my_table
      FULL JOIN TABLE(FLATTEN(input=>[a]))
      ON ... ;
    ```

    Copy

    ```
    SELECT ... FROM my_table
      LEFT JOIN TABLE(my_js_udtf(a))
      ON ... ;
    ```

    Copy

    ```
    SELECT ... FROM my_table
      FULL JOIN TABLE(my_js_udtf(a))
      ON ... ;
    ```

    Copy

    Using this syntax results in the following error:

    ```
    000002 (0A000): Unsupported feature
      'lateral table function called with OUTER JOIN syntax
       or a join predicate (ON clause)'
    ```
  + These restrictions don’t apply if you are using a comma, rather than a JOIN keyword:

    ```
    SELECT ... FROM my_table,
      TABLE(FLATTEN(input=>[col_a]))
      ON ... ;
    ```

    Copy

## Examples[¶](#examples "Link to this heading")

Many of the `JOIN` examples use two tables: `t1` and `t2`. Create these tables and insert data:

```
CREATE TABLE t1 (col1 INTEGER);

INSERT INTO t1 (col1) VALUES
  (2),
  (3),
  (4);

CREATE TABLE t2 (col1 INTEGER);

INSERT INTO t2 (col1) VALUES
  (1),
  (2),
  (2),
  (3);
```

Copy

The following examples run queries with joins:

* [Run a query with an inner join](#label-join-examples-inner-join)
* [Run a query with a left outer join](#label-join-examples-left-outer-join)
* [Run a query with a right outer join](#label-join-examples-right-outer-join)
* [Run a query with a full outer join](#label-join-examples-full-outer-join)
* [Run a query with a cross join](#label-join-examples-cross-join)
* [Run a query with a natural join](#label-join-examples-natural-join)
* [Run a query that combines joins in the FROM clause](#label-join-examples-combine-joins-in-from-clause)
* [Run queries with joins that use the USING clause](#label-join-examples-using-clause)

### Run a query with an inner join[¶](#run-a-query-with-an-inner-join "Link to this heading")

The following example runs a query with an inner join:

```
SELECT t1.col1, t2.col1
  FROM t1 INNER JOIN t2
    ON t2.col1 = t1.col1
  ORDER BY 1,2;
```

Copy

```
+------+------+
| COL1 | COL1 |
|------+------|
|    2 |    2 |
|    2 |    2 |
|    3 |    3 |
+------+------+
```

Run the same query with an inner-directed join to enforce the join order so that the left table is scanned first:

```
SELECT t1.col1, t2.col1
  FROM t1 INNER DIRECTED JOIN t2
    ON t2.col1 = t1.col1
  ORDER BY 1,2;
```

Copy

```
+------+------+
| COL1 | COL1 |
|------+------|
|    2 |    2 |
|    2 |    2 |
|    3 |    3 |
+------+------+
```

### Run a query with a left outer join[¶](#run-a-query-with-a-left-outer-join "Link to this heading")

The following example runs a query with a left outer join:

```
SELECT t1.col1, t2.col1
  FROM t1 LEFT OUTER JOIN t2
    ON t2.col1 = t1.col1
  ORDER BY 1,2;
```

Copy

In the output, there is a NULL value for the row in table `t1` that doesn’t have a matching row
in table `t2`:

```
+------+------+
| COL1 | COL1 |
|------+------|
|    2 |    2 |
|    2 |    2 |
|    3 |    3 |
|    4 | NULL |
+------+------+
```

### Run a query with a right outer join[¶](#run-a-query-with-a-right-outer-join "Link to this heading")

The following example runs a query with a right outer join:

```
SELECT t1.col1, t2.col1
  FROM t1 RIGHT OUTER JOIN t2
    ON t2.col1 = t1.col1
  ORDER BY 1,2;
```

Copy

In the output, there is a NULL value for the row in table `t1` that doesn’t have a matching
row in table `t2`.

```
+------+------+
| COL1 | COL1 |
|------+------|
|    2 |    2 |
|    2 |    2 |
|    3 |    3 |
| NULL |    1 |
+------+------+
```

### Run a query with a full outer join[¶](#run-a-query-with-a-full-outer-join "Link to this heading")

The following example runs a query with a full outer join:

```
SELECT t1.col1, t2.col1
  FROM t1 FULL OUTER JOIN t2
    ON t2.col1 = t1.col1
  ORDER BY 1,2;
```

Copy

Each table has a row that doesn’t have a matching row in the other table, so the output contains two
rows with NULL values:

```
+------+------+
| COL1 | COL1 |
|------+------|
|    2 |    2 |
|    2 |    2 |
|    3 |    3 |
|    4 | NULL |
| NULL |    1 |
+------+------+
```

### Run a query with a cross join[¶](#run-a-query-with-a-cross-join "Link to this heading")

The following example runs a query with a cross join:

Note

A cross join doesn’t have an ON clause.

```
SELECT t1.col1, t2.col1
  FROM t1 CROSS JOIN t2
  ORDER BY 1, 2;
```

Copy

The output shows that the query produces a Cartesian product:

```
+------+------+
| COL1 | COL1 |
|------+------|
|    2 |    1 |
|    2 |    2 |
|    2 |    2 |
|    2 |    3 |
|    3 |    1 |
|    3 |    2 |
|    3 |    2 |
|    3 |    3 |
|    4 |    1 |
|    4 |    2 |
|    4 |    2 |
|    4 |    3 |
+------+------+
```

A cross join can be filtered by a `WHERE` clause, as shown in the following example:

```
SELECT t1.col1, t2.col1
  FROM t1 CROSS JOIN t2
  WHERE t2.col1 = t1.col1
  ORDER BY 1, 2;
```

Copy

```
+------+------+
| COL1 | COL1 |
|------+------|
|    2 |    2 |
|    2 |    2 |
|    3 |    3 |
+------+------+
```

### Run a query with a natural join[¶](#run-a-query-with-a-natural-join "Link to this heading")

The following example shows a query with a natural join. First, create two tables and
insert data:

```
CREATE OR REPLACE TABLE d1 (
  id NUMBER,
  name VARCHAR);

INSERT INTO d1 (id, name) VALUES
  (1,'a'),
  (2,'b'),
  (4,'c');

CREATE OR REPLACE TABLE d2 (
  id NUMBER,
  value VARCHAR);

INSERT INTO d2 (id, value) VALUES
  (1,'xx'),
  (2,'yy'),
  (5,'zz');
```

Copy

Run a query with a natural join:

```
SELECT *
  FROM d1 NATURAL INNER JOIN d2
  ORDER BY id;
```

Copy

The output shows that a natural join produces the same output as the corresponding inner join,
except that the output doesn’t include a second copy of the join column:

```
+----+------+-------+
| ID | NAME | VALUE |
|----+------+-------|
|  1 | a    | xx    |
|  2 | b    | yy    |
+----+------+-------+
```

The following example shows that you can combine natural joins with outer joins:

```
SELECT *
  FROM d1 NATURAL FULL OUTER JOIN d2
  ORDER BY id;
```

Copy

```
+----+------+-------+
| ID | NAME | VALUE |
|----+------+-------|
|  1 | a    | xx    |
|  2 | b    | yy    |
|  4 | c    | NULL  |
|  5 | NULL | zz    |
+----+------+-------+
```

### Run a query that combines joins in the FROM clause[¶](#run-a-query-that-combines-joins-in-the-from-clause "Link to this heading")

You can combine in the `FROM` clause. Create a third table:

```
CREATE TABLE t3 (col1 INTEGER);

INSERT INTO t3 (col1) VALUES
  (2),
  (6);
```

Copy

Run a query that chains together two joins in the FROM clause:

```
SELECT t1.*, t2.*, t3.*
  FROM t1
    LEFT OUTER JOIN t2 ON (t1.col1 = t2.col1)
    RIGHT OUTER JOIN t3 ON (t3.col1 = t2.col1)
  ORDER BY t1.col1;
```

Copy

```
+------+------+------+
| COL1 | COL1 | COL1 |
|------+------+------|
|    2 |    2 |    2 |
|    2 |    2 |    2 |
| NULL | NULL |    6 |
+------+------+------+
```

In such a query, the results are determined based on the joins taking place from left to right,
although the optimizer might reorder the joins if a different join order produces the same result. If the
right outer join is meant to take place before the left outer join, then write the query in the following
way:

```
SELECT t1.*, t2.*, t3.*
FROM t1
  LEFT OUTER JOIN
    (t2 RIGHT OUTER JOIN t3 ON (t3.col1 = t2.col1))
  ON (t1.col1 = t2.col1)
ORDER BY t1.col1;
```

Copy

```
+------+------+------+
| COL1 | COL1 | COL1 |
|------+------+------|
|    2 |    2 |    2 |
|    2 |    2 |    2 |
|    3 | NULL | NULL |
|    4 | NULL | NULL |
+------+------+------+
```

### Run queries with joins that use the USING clause[¶](#run-queries-with-joins-that-use-the-using-clause "Link to this heading")

The next two examples show standard (ISO 9075) and nonstandard usage of
the `USING` clause. Both are supported by Snowflake.

This first example shows standard usage. Specifically, the projection list
contains exactly `*`:

```
WITH
  l AS (
       SELECT 'a' AS userid
       ),
  r AS (
       SELECT 'b' AS userid
       )
SELECT *
  FROM l LEFT JOIN r USING(userid);
```

Copy

Even though the example query joins two tables, and each table has one column,
and the query asks for all columns, the output contains one column, not two:

```
+--------+
| USERID |
|--------|
| a      |
+--------+
```

The following example shows nonstandard usage. The projection list contains
something other than `*`:

```
WITH
  l AS (
       SELECT 'a' AS userid
     ),
  r AS (
       SELECT 'b' AS userid
       )
SELECT l.userid as UI_L,
       r.userid as UI_R
  FROM l LEFT JOIN r USING(userid);
```

Copy

The output contains two columns, and the second column contains either a value
from the second table or NULL:

```
+------+------+
| UI_L | UI_R |
|------+------|
| a    | NULL |
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

### Alternative interfaces

[Snowflake Python APIs](/developer-guide/snowflake-python-api/snowflake-python-overview)[Snowflake REST APIs](/developer-guide/snowflake-rest-api/snowflake-rest-api)[Snowflake CLI](/developer-guide/snowflake-cli/index)

See all interfaces

On this page

1. [Syntax](#syntax)
2. [Parameters](#parameters)
3. [Usage notes](#usage-notes)
4. [Examples](#examples)
5. [Run a query with an inner join](#run-a-query-with-an-inner-join)
6. [Run a query with a left outer join](#run-a-query-with-a-left-outer-join)
7. [Run a query with a right outer join](#run-a-query-with-a-right-outer-join)
8. [Run a query with a full outer join](#run-a-query-with-a-full-outer-join)
9. [Run a query with a cross join](#run-a-query-with-a-cross-join)
10. [Run a query with a natural join](#run-a-query-with-a-natural-join)
11. [Run a query that combines joins in the FROM clause](#run-a-query-that-combines-joins-in-the-from-clause)
12. [Run queries with joins that use the USING clause](#run-queries-with-joins-that-use-the-using-clause)