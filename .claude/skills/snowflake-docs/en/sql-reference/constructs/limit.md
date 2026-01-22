---
auto_generated: true
description: Query syntax
last_scraped: '2026-01-14T16:57:05.673288+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/constructs/limit
title: LIMIT / FETCH | Snowflake Documentation
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

[Reference](../../reference.md)[SQL command reference](../../sql-reference-commands.md)[Query syntax](../constructs.md)LIMIT

Categories:
:   [Query syntax](../constructs)

# LIMIT / FETCH[¶](#limit-fetch "Link to this heading")

Constrains the maximum number of rows returned by a statement or subquery. Both LIMIT (PostgreSQL syntax) and FETCH (ANSI syntax) are supported, and produce the same result.

See also:
:   [TOP <n>](top_n)

## Syntax[¶](#syntax "Link to this heading")

### PostgreSQL syntax[¶](#postgresql-syntax "Link to this heading")

```
SELECT ...
FROM ...
[ ORDER BY ... ]
LIMIT <count> [ OFFSET <start> ]
[ ... ]
```

Copy

### ANSI syntax[¶](#ansi-syntax "Link to this heading")

```
SELECT ...
FROM ...
[ ORDER BY ... ]
[ OFFSET <start> ] [ { ROW | ROWS } ] FETCH [ { FIRST | NEXT } ] <count> [ { ROW | ROWS } ] [ ONLY ]
[ ... ]
```

Copy

## Parameters[¶](#parameters "Link to this heading")

`count`
:   The number of rows returned. Must be a non-negative integer constant.

    The values NULL, empty string (`''`), and `$$$$` are also accepted and are treated as
    “unlimited”; this is useful primarily for connectors and drivers (such as the JDBC driver) if they
    receive an incomplete parameter list when dynamically binding parameters to a statement.

`OFFSET` `start`
:   The row number after which the limited/fetched rows are returned. Must be a non-negative integer constant.

    If `OFFSET` is omitted, the output starts from the first row in the result set.

    The values NULL, empty string (`''`) and `$$$$` are also accepted and are treated as 0
    (i.e. do not skip any rows); this is useful primarily for connectors and drivers (such as the JDBC
    driver) if they receive an incomplete parameter list when dynamically binding parameters to a statement.

`ONLY`
:   Optional keyword that does not affect the output. It is used for emphasis to the
    human reader.

## Usage notes[¶](#usage-notes "Link to this heading")

* An [ORDER BY](order-by) clause is not required; however, without an ORDER BY clause, the results are non-deterministic
  because query results are not necessarily in any particular order. To control the results returned, use an ORDER BY clause.
* Top-K pruning can improve the performance of queries that include both LIMIT and ORDER BY clauses. For more
  information, see [Top-K pruning for improved query performance](../../user-guide/querying-top-k-pruning-optimization).
* TOP `n` and LIMIT `count` are equivalent.
* Both the LIMIT clause and the [SAMPLE](sample) clause return a subset of rows from a table. When you use the
  LIMIT clause, Snowflake returns the specified number of rows in the fastest way possible. When you use the SAMPLE
  clause, Snowflake returns rows based on the sampling method specified in the clause.

## Examples[¶](#examples "Link to this heading")

The following examples show the effect of LIMIT. For simplicity, these
queries omit the `ORDER BY` clause and assume that the output order is
always the same as shown by the first query. **Real-world queries should
include ORDER BY.**

> ```
> select c1 from testtable;
>
> +------+
> |   C1 |
> |------|
> |    1 |
> |    2 |
> |    3 |
> |   20 |
> |   19 |
> |   18 |
> |    1 |
> |    2 |
> |    3 |
> |    4 |
> | NULL |
> |   30 |
> | NULL |
> +------+
>
> select c1 from testtable limit 3 offset 3;
>
> +----+
> | C1 |
> |----|
> | 20 |
> | 19 |
> | 18 |
> +----+
>
> select c1 from testtable order by c1;
>
> +------+
> |   C1 |
> |------|
> |    1 |
> |    1 |
> |    2 |
> |    2 |
> |    3 |
> |    3 |
> |    4 |
> |   18 |
> |   19 |
> |   20 |
> |   30 |
> | NULL |
> | NULL |
> +------+
>
> select c1 from testtable order by c1 limit 3 offset 3;
>
> +----+
> | ID |
> |----|
> |  2 |
> |  3 |
> |  3 |
> +----+
> ```
>
> Copy

The following example demonstrates the use of NULLs to indicate

* No limit to the number of rows.
* Start at row 1 (do not skip any rows)

  > ```
  > CREATE TABLE demo1 (i INTEGER);
  > INSERT INTO demo1 (i) VALUES (1), (2);
  > ```
  >
  > Copy
  >
  > ```
  > SELECT * FROM demo1 ORDER BY i LIMIT NULL OFFSET NULL;
  > +---+
  > | I |
  > |---|
  > | 1 |
  > | 2 |
  > +---+
  > ```
  >
  > Copy
  >
  > ```
  > SELECT * FROM demo1 ORDER BY i LIMIT '' OFFSET '';
  > +---+
  > | I |
  > |---|
  > | 1 |
  > | 2 |
  > +---+
  > ```
  >
  > Copy
  >
  > ```
  > SELECT * FROM demo1 ORDER BY i LIMIT $$$$ OFFSET $$$$;
  > +---+
  > | I |
  > |---|
  > | 1 |
  > | 2 |
  > +---+
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