---
auto_generated: true
description: Query syntax
last_scraped: '2026-01-14T16:55:02.076494+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/querying-joins
title: Working with joins | Snowflake Documentation
---

1. [Overview](../guides/README.md)
2. [Snowflake Horizon Catalog](snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../guides/overview-connecting.md)
6. [Virtual warehouses](warehouses.md)
7. [Databases, Tables, & Views](../guides/overview-db.md)
8. [Data types](../data-types.md)
10. Data Integration

    - [Snowflake Openflow](data-integration/openflow/about.md)
    - Apache Iceberg™

      - [Apache Iceberg™ Tables](tables-iceberg.md)
      - [Snowflake Open Catalog](opencatalog/overview.md)
11. Data engineering

    - [Data loading](../guides/overview-loading-data.md)
    - [Dynamic Tables](dynamic-tables-about.md)
    - [Streams and Tasks](data-pipelines-intro.md)
    - [dbt Projects on Snowflake](data-engineering/dbt-projects-on-snowflake.md)
    - [Data Unloading](../guides/overview-unloading-data.md)
12. [Storage Lifecycle Policies](storage-management/storage-lifecycle-policies.md)
13. [Migrations](../migrations/README.md)
15. [Queries](../guides/overview-queries.md)

    * [Joins](querying-joins.md)

      + [Using lateral joins](lateral-join-using.md)
      + [Eliminating redundant joins](join-elimination.md)
    * [Subqueries](querying-subqueries.md)
    * [Querying Hierarchical Data](queries-hierarchical.md)
    * [Common Table Expressions (CTE)](queries-cte.md)")
    * [Querying Semi-structured Data](querying-semistructured.md)
    * [Using full-text search](querying-with-search-functions.md)
    * [Constructing SQL at Runtime](querying-construct-at-runtime.md)
    * [Analyzing time-series data](querying-time-series-data.md)
    * [Analyzing data with window functions](functions-window-using.md)
    * [Match Recognize](match-recognize-introduction.md)
    * [Sequences](querying-sequences.md)
    * [Persisted Query Results](querying-persisted-results.md)
    * [Distinct Counts](querying-distinct-counts.md)
    * [Similarity Estimation](querying-approximate-similarity.md)
    * [Frequency Estimation](querying-approximate-frequent-values.md)
    * [Estimating Percentile Values](querying-approximate-percentile-values.md)
    * [Monitor query activity with Query History](ui-snowsight-activity.md)
    * [Using query insights to improve performance](query-insights.md)
    * [Query Hash](query-hash.md)
    * [Top-K pruning](querying-top-k-pruning-optimization.md)
    * [Cancel Statements](querying-cancel-statements.md)
16. [Listings](../collaboration/collaboration-listings-about.md)
17. [Collaboration](../guides/overview-sharing.md)
19. [Snowflake AI & ML](../guides/overview-ai-features.md)
21. [Snowflake Postgres](snowflake-postgres/about.md)
23. [Alerts & Notifications](../guides/overview-alerts.md)
25. [Security](../guides/overview-secure.md)
26. [Data Governance](../guides/overview-govern.md)
27. [Privacy](../guides/overview-privacy.md)
29. [Organizations & Accounts](../guides/overview-manage.md)
30. [Business continuity & data recovery](replication-intro.md)
32. [Performance optimization](../guides/overview-performance.md)
33. [Cost & Billing](../guides/overview-cost.md)

[Guides](../guides/README.md)[Queries](../guides/overview-queries.md)Joins

Categories:
:   [Query syntax](../sql-reference/constructs)

# Working with joins[¶](#working-with-joins "Link to this heading")

A join combines rows from two tables to create a new combined row that can be used in the query.

## Introduction[¶](#introduction "Link to this heading")

Joins are useful when the data in the tables is related. For example, one table might hold information about projects,
and one table might hold information about employees working on those projects.

```
CREATE TABLE projects (
  project_id INT,
  project_name VARCHAR);

INSERT INTO projects VALUES
  (1000, 'COVID-19 Vaccine'),
  (1001, 'Malaria Vaccine'),
  (1002, 'NewProject');

CREATE TABLE employees (
  employee_id INT,
  employee_name VARCHAR,
  project_id INT);

INSERT INTO employees VALUES
  (10000001, 'Terry Smith', 1000),
  (10000002, 'Maria Inverness', 1000),
  (10000003, 'Pat Wang', 1001),
  (10000004, 'NewEmployee', NULL);
```

Copy

Query the tables to view the data:

```
SELECT * FROM projects ORDER BY project_ID;
```

Copy

```
+------------+------------------+
| PROJECT_ID | PROJECT_NAME     |
|------------+------------------|
|       1000 | COVID-19 Vaccine |
|       1001 | Malaria Vaccine  |
|       1002 | NewProject       |
+------------+------------------+
```

```
SELECT * FROM employees ORDER BY employee_ID;
```

Copy

```
+-------------+-----------------+------------+
| EMPLOYEE_ID | EMPLOYEE_NAME   | PROJECT_ID |
|-------------+-----------------+------------|
|    10000001 | Terry Smith     |       1000 |
|    10000002 | Maria Inverness |       1000 |
|    10000003 | Pat Wang        |       1001 |
|    10000004 | NewEmployee     |       NULL |
+-------------+-----------------+------------+
```

The two joined tables usually contain one or more columns in common so that the rows
in one table can be associated with the corresponding rows in the other table.
For example, in these sample tables, each row in the projects table has a unique project ID
number, and each row in the employees table includes the ID number of
the project that the employee is currently assigned to.

The join operation specifies, explicitly or implicitly, how to relate rows
in one table to the corresponding rows in the other table, typically by
referencing one or more common columns, such as `project_id`. For example, the following
joins the `projects` and `employees` tables that were created previously:

```
SELECT p.project_ID, project_name, employee_ID, employee_name, e.project_ID
  FROM projects AS p JOIN employees AS e
    ON e.project_ID = p.project_ID
  ORDER BY p.project_ID, e.employee_ID;
```

Copy

```
+------------+------------------+-------------+-----------------+------------+
| PROJECT_ID | PROJECT_NAME     | EMPLOYEE_ID | EMPLOYEE_NAME   | PROJECT_ID |
|------------+------------------+-------------+-----------------+------------|
|       1000 | COVID-19 Vaccine |    10000001 | Terry Smith     |       1000 |
|       1000 | COVID-19 Vaccine |    10000002 | Maria Inverness |       1000 |
|       1001 | Malaria Vaccine  |    10000003 | Pat Wang        |       1001 |
+------------+------------------+-------------+-----------------+------------+
```

Although a single join operation can join only two tables, joins can be chained together. The result of a join is
a table-like object, and that table-like object can then be joined to another table-like object. Conceptually,
the idea is similar to the following; this isn’t the actual syntax:

```
table1 JOIN (table2 JOIN table3)
```

Copy

In this pseudo-code, `table2` and `table3` are joined first. The table that results from that join is then joined with
`table1`.

Joins can be applied not only to tables, but also to other table-like objects. You can join:

* A table.
* A [view](views-introduction) (materialized or non-materialized).
* A [table literal](../sql-reference/literals-table).
* An expression that evaluates to the equivalent of a table (containing one or more columns and zero or more
  rows). For example:

  + The result set returned by a [table function](../sql-reference/functions-table).
  + The result set returned by a subquery that returns a table.

When this topic refers to joining a table, it generally means joining any table-like object.

Note

Snowflake can improve performance by eliminating unnecessary joins. For more information, see
[Understanding How Snowflake Can Eliminate Redundant Joins](join-elimination).

## Types of joins[¶](#types-of-joins "Link to this heading")

Snowflake supports the following types of joins:

* [Inner join](#label-querying-join-inner)
* [Outer join](#label-querying-join-outer)
* [Cross join](#label-querying-join-cross)
* [Natural join](#label-querying-join-natural)

Note

Snowflake also supports ASOF JOIN for analyzing time-series data. For more information,
see [ASOF JOIN](../sql-reference/constructs/asof-join) and [Analyzing time-series data](querying-time-series-data).

### Inner join[¶](#inner-join "Link to this heading")

An inner join pairs each row in one table with the matching rows in the other table.

The following example shows an inner join:

```
SELECT p.project_ID, project_name, employee_ID, employee_name, e.project_ID
  FROM projects AS p INNER JOIN employees AS e
    ON e.project_id = p.project_id
  ORDER BY p.project_ID, e.employee_ID;
```

Copy

```
+------------+------------------+-------------+-----------------+------------+
| PROJECT_ID | PROJECT_NAME     | EMPLOYEE_ID | EMPLOYEE_NAME   | PROJECT_ID |
|------------+------------------+-------------+-----------------+------------|
|       1000 | COVID-19 Vaccine |    10000001 | Terry Smith     |       1000 |
|       1000 | COVID-19 Vaccine |    10000002 | Maria Inverness |       1000 |
|       1001 | Malaria Vaccine  |    10000003 | Pat Wang        |       1001 |
+------------+------------------+-------------+-----------------+------------+
```

In this example, the output contains two columns named `PROJECT_ID`. One `PROJECT_ID` column is from
the `projects` table, and one is from the `employees` table. For each row in the output, the values
in the two `PROJECT_ID` columns match because the query specified `e.project_id = p.project_id`.

The output includes only valid pairs; that is, rows that match the join condition. In this example, there is
no row for the project named `NewProject`, which has no employees assigned yet, or the employee named
`NewEmployee`, who hasn’t been assigned to any projects yet.

### Outer join[¶](#outer-join "Link to this heading")

An outer join lists all rows in the specified table, even if those rows have no match in the other table. For
example, a left outer join between projects and employees lists all projects, including projects that don’t
yet have any employee assigned.

```
SELECT p.project_name, e.employee_name
  FROM projects AS p LEFT OUTER JOIN employees AS e
    ON e.project_ID = p.project_ID
  ORDER BY p.project_name, e.employee_name;
```

Copy

```
+------------------+-----------------+
| PROJECT_NAME     | EMPLOYEE_NAME   |
|------------------+-----------------|
| COVID-19 Vaccine | Maria Inverness |
| COVID-19 Vaccine | Terry Smith     |
| Malaria Vaccine  | Pat Wang        |
| NewProject       | NULL            |
+------------------+-----------------+
```

The project named `NewProject` is included in this output, even though there is no matching row in the
`employees` table. Because there are no matching employee names for the project named `NewProject`, the
employee name is NULL.

A right outer join lists all employees (regardless of project).

```
SELECT p.project_name, e.employee_name
  FROM projects AS p RIGHT OUTER JOIN employees AS e
    ON e.project_ID = p.project_ID
  ORDER BY p.project_name, e.employee_name;
```

Copy

```
+------------------+-----------------+
| PROJECT_NAME     | EMPLOYEE_NAME   |
|------------------+-----------------|
| COVID-19 Vaccine | Maria Inverness |
| COVID-19 Vaccine | Terry Smith     |
| Malaria Vaccine  | Pat Wang        |
| NULL             | NewEmployee     |
+------------------+-----------------+
```

A full outer join lists all projects and all employees.

```
SELECT p.project_name, e.employee_name
  FROM projects AS p FULL OUTER JOIN employees AS e
    ON e.project_ID = p.project_ID
  ORDER BY p.project_name, e.employee_name;
```

Copy

```
+------------------+-----------------+
| PROJECT_NAME     | EMPLOYEE_NAME   |
|------------------+-----------------|
| COVID-19 Vaccine | Maria Inverness |
| COVID-19 Vaccine | Terry Smith     |
| Malaria Vaccine  | Pat Wang        |
| NewProject       | NULL            |
| NULL             | NewEmployee     |
+------------------+-----------------+
```

### Cross join[¶](#cross-join "Link to this heading")

A cross join combines each row in the first table with each row in the second table, creating every possible
combination of rows, which is called a *Cartesian product*. Because most of the result rows contain parts of
rows that aren’t actually related, a cross join is rarely useful by itself. In fact, cross joins are usually
the result of accidentally omitting the join condition.

The result of a cross join can be very large and expensive. If the first table has N rows and the second table
has M rows, then the result is N x M rows. For example, if the first table has 100 rows and the second table
has 1000 rows, then the result set contains 100,000 rows.

The following query shows a cross join:

Note

This query contains no `ON` clause and no filter.

```
SELECT p.project_name, e.employee_name
  FROM projects AS p CROSS JOIN employees AS e
  ORDER BY p.project_ID, e.employee_ID;
```

Copy

```
+------------------+-----------------+
| PROJECT_NAME     | EMPLOYEE_NAME   |
|------------------+-----------------|
| COVID-19 Vaccine | Terry Smith     |
| COVID-19 Vaccine | Maria Inverness |
| COVID-19 Vaccine | Pat Wang        |
| COVID-19 Vaccine | NewEmployee     |
| Malaria Vaccine  | Terry Smith     |
| Malaria Vaccine  | Maria Inverness |
| Malaria Vaccine  | Pat Wang        |
| Malaria Vaccine  | NewEmployee     |
| NewProject       | Terry Smith     |
| NewProject       | Maria Inverness |
| NewProject       | Pat Wang        |
| NewProject       | NewEmployee     |
+------------------+-----------------+
```

You can make the output of a cross join more useful by applying a filter in the `WHERE` clause:

```
SELECT p.project_name, e.employee_name
  FROM projects AS p CROSS JOIN employees AS e
  WHERE e.project_ID = p.project_ID
  ORDER BY p.project_ID, e.employee_ID;
```

Copy

```
+------------------+-----------------+
| PROJECT_NAME     | EMPLOYEE_NAME   |
|------------------+-----------------|
| COVID-19 Vaccine | Terry Smith     |
| COVID-19 Vaccine | Maria Inverness |
| Malaria Vaccine  | Pat Wang        |
+------------------+-----------------+
```

The result of this cross join and filter is the same as the result of the following inner join:

```
SELECT p.project_name, e.employee_name
  FROM projects AS p INNER JOIN employees AS e
    ON e.project_ID = p.project_ID
  ORDER BY p.project_ID, e.employee_ID;
```

Copy

```
+------------------+-----------------+
| PROJECT_NAME     | EMPLOYEE_NAME   |
|------------------+-----------------|
| COVID-19 Vaccine | Terry Smith     |
| COVID-19 Vaccine | Maria Inverness |
| Malaria Vaccine  | Pat Wang        |
+------------------+-----------------+
```

Important

Although the two queries in this example produce the same output when they use the same condition
(`e.project_id = p.project_id`) in different clauses (`WHERE` and `FROM ... ON ...`), it is possible to
construct pairs of queries that use the same condition but that don’t produce the same output.

The most common examples involve outer joins. If you run `table1 LEFT OUTER JOIN table2`, then for rows in
`table1` that have no match, the columns that would have come from `table2` contain NULL. A filter
such as `WHERE table2.ID = table1.ID` filters out rows in which either `table2.id` or `table1.id` contains a
NULL, while an explicit outer join in the `FROM ... ON ...` clause doesn’t filter out rows with NULL values.
In other words, an outer join with a filter might not act like an outer join.

### Natural join[¶](#natural-join "Link to this heading")

A natural join joins two tables on columns that have the same names and compatible data types. Both the
`employees` and the `projects` table created previously, have a column named `project_ID`. A natural
join implicitly constructs the `ON` clause: `ON projects.project_ID = employees.project_ID`.

If two tables have multiple columns in common, then a natural join uses all of the common columns in the constructed
`ON` clause. For example, if two tables each have columns named `city` and `province`, then a natural join
constructs the following `ON` clause:

```
ON table2.city = table1.city AND table2.province = table1.province
```

Copy

The output of a natural join includes only one copy of each of the shared columns. For example, the following query
produces a natural join that contains all of columns in the two tables, except that it omits all but one copy of the
redundant `project_id` columns:

```
SELECT *
  FROM projects NATURAL JOIN employees
  ORDER BY employee_id;
```

Copy

```
+------------+------------------+-------------+-----------------+
| PROJECT_ID | PROJECT_NAME     | EMPLOYEE_ID | EMPLOYEE_NAME   |
|------------+------------------+-------------+-----------------|
|       1000 | COVID-19 Vaccine |    10000001 | Terry Smith     |
|       1000 | COVID-19 Vaccine |    10000002 | Maria Inverness |
|       1001 | Malaria Vaccine  |    10000003 | Pat Wang        |
+------------+------------------+-------------+-----------------+
```

You can combine a natural join with an outer join.

You can’t combine a natural join `ON` clause because the join condition is already implied. However, you
can use a `WHERE` clause to filter the results of a natural join.

## Implementing joins[¶](#implementing-joins "Link to this heading")

Syntactically, there are two ways to join tables:

* Use the [JOIN](../sql-reference/constructs/join) subclause in the `ON` subclause of the
  [FROM](../sql-reference/constructs/from) clause.
* Use the [WHERE](../sql-reference/constructs/where) clause with the [FROM](../sql-reference/constructs/from) clause.

Snowflake recommends using the `ON` subclause in the `FROM` clause because the syntax is more flexible.
Also, specifying the predicate in the `ON` subclause avoids the problem of accidentally filtering rows
with NULL values when using a `WHERE` clause to specify the join condition for an outer join.

In addition, you can use the `DIRECTED` keyword to enforce the join order of the tables. When you
specify this keyword, the first, or left, table is scanned before the second, or right, table. For example,
`o1 INNER DIRECTED JOIN o2` scans the `o1` table before the `o2` table. If the
`DIRECTED` keyword is added, the join type — for example, `INNER` or `OUTER` — is required.
For more information, see [JOIN](../sql-reference/constructs/join).

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
2. [Types of joins](#types-of-joins)
3. [Implementing joins](#implementing-joins)

Related content

1. [JOIN](/user-guide/../sql-reference/constructs/join)
2. [ASOF JOIN](/user-guide/../sql-reference/constructs/asof-join)
3. [FROM](/user-guide/../sql-reference/constructs/from)
4. [WHERE](/user-guide/../sql-reference/constructs/where)
5. [LATERAL](/user-guide/../sql-reference/constructs/join-lateral)