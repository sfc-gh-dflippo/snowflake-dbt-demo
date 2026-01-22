---
auto_generated: true
description: Query syntax
last_scraped: '2026-01-14T16:54:30.157658+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/constructs/group-by-rollup
title: GROUP BY ROLLUP | Snowflake Documentation
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

[Reference](../../reference.md)[SQL command reference](../../sql-reference-commands.md)[Query syntax](../constructs.md)GROUP BY ROLLUP

Categories:
:   [Query syntax](../constructs)

# GROUP BY ROLLUP[¶](#group-by-rollup "Link to this heading")

GROUP BY ROLLUP is an extension of the [GROUP BY](group-by) clause that produces sub-total rows
(in addition to the grouped rows). Sub-total rows are rows that further aggregate whose values are derived
by computing the same aggregate functions that were used to produce the grouped rows.

You can think of rollup as generating multiple result sets, each of which
(after the first) is the aggregate of the previous result set. So, for example,
if you own a chain of retail stores, you might want to see the profit for:

* Each store.
* Each city (large cities might have multiple stores).
* Each state.
* Everything (all stores in all states).

You could create separate reports to get that information, but it is more
efficient to scan the data once.

If you are familiar with the concept of grouping sets
([GROUP BY GROUPING SETS](group-by-grouping-sets))
you can think of a ROLLUP grouping as equivalent to a series of grouping sets,
and which is essentially a shorter specification. The `N` elements of
a ROLLUP specification correspond to `N+1 GROUPING SETS`.

See also:
:   [GROUP BY GROUPING SETS](group-by-grouping-sets)

## Syntax[¶](#syntax "Link to this heading")

```
SELECT ...
FROM ...
[ ... ]
GROUP BY ROLLUP ( groupRollup [ , groupRollup [ , ... ] ] )
[ ... ]
```

Copy

Where:

> ```
> groupRollup ::= { <column_alias> | <position> | <expr> }
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

## Usage notes[¶](#usage-notes "Link to this heading")

* As the query is aggregated at higher and higher levels, it shows NULL values
  in more columns of each row. This is appropriate. For example, in the example
  below, for the aggregate at the state level, the city column is NULL;
  that’s because the value in the profit column does not correspond to one
  city. Similarly, in the final total, which aggregates data from all the
  states and all the cities, the revenue is not from one specific state or
  one specific city, so both the state and city columns in that row are NULL.
* The query should list the “most significant level” first in the parentheses
  after the ROLLUP. For example, states contain cities, so if you are rolling up
  data across states and cities, the clause should be

  > `...ROLLUP (state, city)`

  If you reverse the order of the column names, you get a result that is
  probably not what you want. In the example below, if you reversed the order
  of city and state in the ROLLUP clause, the result would be incorrect, at least in part because both California and
  Puerto Rico have a city named San Jose (“SJ”), and you probably would not want to
  combine the revenue from the two different San Joses, except in the final
  total of all revenue. (An alternative way to avoid combining data from different cities
  with the same name is to create a unique ID for each city and use the ID rather than the name in the query.)

## Examples[¶](#examples "Link to this heading")

Start by creating and loading a table with information about sales from
a chain store that has branches in different cities and states/territories.

> ```
> -- Create some tables and insert some rows.
> CREATE TABLE products (product_ID INTEGER, wholesale_price REAL);
> INSERT INTO products (product_ID, wholesale_price) VALUES 
>     (1, 1.00),
>     (2, 2.00);
>
> CREATE TABLE sales (product_ID INTEGER, retail_price REAL, 
>     quantity INTEGER, city VARCHAR, state VARCHAR);
> INSERT INTO sales (product_id, retail_price, quantity, city, state) VALUES 
>     (1, 2.00,  1, 'SF', 'CA'),
>     (1, 2.00,  2, 'SJ', 'CA'),
>     (2, 5.00,  4, 'SF', 'CA'),
>     (2, 5.00,  8, 'SJ', 'CA'),
>     (2, 5.00, 16, 'Miami', 'FL'),
>     (2, 5.00, 32, 'Orlando', 'FL'),
>     (2, 5.00, 64, 'SJ', 'PR');
> ```
>
> Copy

Run a rollup query that shows profit by city, state, and total across all
states.

The example below shows a query that has three “levels”:

* Each city.
* Each state.
* All revenue combined.

This example uses `ORDER BY state, city NULLS LAST` to ensure that each state’s rollup comes immediately after all of
the cities in that state, and that the final rollup appears at the end of the output.

> ```
> SELECT state, city, SUM((s.retail_price - p.wholesale_price) * s.quantity) AS profit 
>  FROM products AS p, sales AS s
>  WHERE s.product_ID = p.product_ID
>  GROUP BY ROLLUP (state, city)
>  ORDER BY state, city NULLS LAST
>  ;
> +-------+---------+--------+
> | STATE | CITY    | PROFIT |
> |-------+---------+--------|
> | CA    | SF      |     13 |
> | CA    | SJ      |     26 |
> | CA    | NULL    |     39 |
> | FL    | Miami   |     48 |
> | FL    | Orlando |     96 |
> | FL    | NULL    |    144 |
> | PR    | SJ      |    192 |
> | PR    | NULL    |    192 |
> | NULL  | NULL    |    375 |
> +-------+---------+--------+
> ```
>
> Copy

Some rollup rows contain NULL values. For example, the last row in the table contains a NULL value for the city and
a NULL value for the state because the data is for all cities and states, not a specific city and state.

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