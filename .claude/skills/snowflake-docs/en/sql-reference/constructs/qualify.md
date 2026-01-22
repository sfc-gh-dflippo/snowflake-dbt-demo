---
auto_generated: true
description: Query syntax
last_scraped: '2026-01-14T16:57:04.521132+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/constructs/qualify
title: QUALIFY | Snowflake Documentation
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

[Reference](../../reference.md)[SQL command reference](../../sql-reference-commands.md)[Query syntax](../constructs.md)QUALIFY

Categories:
:   [Query syntax](../constructs)

# QUALIFY[¶](#qualify "Link to this heading")

In a SELECT statement, the QUALIFY clause filters the results of window functions.

QUALIFY does with window functions what HAVING does with aggregate functions and GROUP BY clauses.

In the execution order of a query, QUALIFY is therefore evaluated after window functions are computed. Typically,
a SELECT statement’s clauses are evaluated in the order shown below:

> 1. From
> 2. Where
> 3. Group by
> 4. Having
> 5. Window
> 6. QUALIFY
> 7. Distinct
> 8. Order by
> 9. Limit

## Syntax[¶](#syntax "Link to this heading")

```
QUALIFY <predicate>
```

Copy

The general form of a statement with QUALIFY is similar to the following
(some variations in order are allowed, but are not shown):

```
SELECT <column_list>
  FROM <data_source>
  [GROUP BY ...]
  [HAVING ...]
  QUALIFY <predicate>
  [ ... ]
```

Copy

## Parameters[¶](#parameters "Link to this heading")

`column_list`
:   This generally follows the rules for the projection clause of a [SELECT](../sql/select) statement.

`data_source`
:   The data source is usually a table, but can be another table-like data source, such as a view, UDTF (user-defined table function),
    etc.

`predicate`
:   The predicate is an expression that filters the result after aggregates and window functions are computed.
    The predicate should look similar to a [HAVING](having) clause, but without the
    keyword `HAVING`. In addition, the predicate can also contain window functions.

    See the [Examples](#examples) section (in this topic) for predicate examples.

## Usage notes[¶](#usage-notes "Link to this heading")

* The QUALIFY clause requires at least one window function to be specified in at least one of the following clauses
  of the SELECT statement:

  + The SELECT column list.
  + The filter predicate of the QUALIFY clause.

  Examples of each of these are shown in the Examples section below.
* Expressions in the SELECT list, including window functions, can be referred to by the column alias defined in the
  SELECT list.
* QUALIFY supports aggregates and subqueries in the predicate. For aggregates, the same rules as for the HAVING clause
  apply.
* The word QUALIFY is a reserved word.
* The Snowflake syntax for QUALIFY is not part of the ANSI standard.

## Examples[¶](#examples "Link to this heading")

The QUALIFY clause simplifies queries that require filtering on the result of window functions. Without QUALIFY,
filtering requires nesting. The example below uses the ROW\_NUMBER() function to return only the first row in each
partition.

> Create and load a table:
>
> ```
> CREATE TABLE qt (i INTEGER, p CHAR(1), o INTEGER);
> INSERT INTO qt (i, p, o) VALUES
>     (1, 'A', 1),
>     (2, 'A', 2),
>     (3, 'B', 1),
>     (4, 'B', 2);
> ```
>
> Copy
>
> This query uses nesting rather than QUALIFY:
>
> ```
> SELECT * 
>     FROM (
>          SELECT i, p, o, 
>                 ROW_NUMBER() OVER (PARTITION BY p ORDER BY o) AS row_num
>             FROM qt
>         )
>     WHERE row_num = 1
>     ;
> +---+---+---+---------+
> | I | P | O | ROW_NUM |
> |---+---+---+---------|
> | 1 | A | 1 |       1 |
> | 3 | B | 1 |       1 |
> +---+---+---+---------+
> ```
>
> Copy
>
> This query uses QUALIFY:
>
> ```
> SELECT i, p, o
>     FROM qt
>     QUALIFY ROW_NUMBER() OVER (PARTITION BY p ORDER BY o) = 1
>     ;
> +---+---+---+
> | I | P | O |
> |---+---+---|
> | 1 | A | 1 |
> | 3 | B | 1 |
> +---+---+---+
> ```
>
> Copy

You can also use QUALIFY to reference window functions that are in the SELECT column list:

> ```
> SELECT i, p, o, ROW_NUMBER() OVER (PARTITION BY p ORDER BY o) AS row_num
>     FROM qt
>     QUALIFY row_num = 1
>     ;
> +---+---+---+---------+
> | I | P | O | ROW_NUM |
> |---+---+---+---------|
> | 1 | A | 1 |       1 |
> | 3 | B | 1 |       1 |
> +---+---+---+---------+
> ```
>
> Copy
>
> You can see how the QUALIFY acts as a filter by removing the QUALIFY from the previous query and comparing the
> output:
>
> ```
> SELECT i, p, o, ROW_NUMBER() OVER (PARTITION BY p ORDER BY o) AS row_num
>     FROM qt
>     ;
> +---+---+---+---------+
> | I | P | O | ROW_NUM |
> |---+---+---+---------|
> | 1 | A | 1 |       1 |
> | 2 | A | 2 |       2 |
> | 3 | B | 1 |       1 |
> | 4 | B | 2 |       2 |
> +---+---+---+---------+
> ```
>
> Copy

The QUALIFY clause can also be combined with aggregates and can have subqueries in the predicate. For example:

> ```
> SELECT c2, SUM(c3) OVER (PARTITION BY c2) as r
>   FROM t1
>   WHERE c3 < 4
>   GROUP BY c2, c3
>   HAVING SUM(c1) > 3
>   QUALIFY r IN (
>     SELECT MIN(c1)
>       FROM test
>       GROUP BY c2
>       HAVING MIN(c1) > 3);
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

### Alternative interfaces

[Snowflake Python APIs](/developer-guide/snowflake-python-api/snowflake-python-overview)[Snowflake REST APIs](/developer-guide/snowflake-rest-api/snowflake-rest-api)[Snowflake CLI](/developer-guide/snowflake-cli/index)

See all interfaces

On this page

1. [Syntax](#syntax)
2. [Parameters](#parameters)
3. [Usage notes](#usage-notes)
4. [Examples](#examples)