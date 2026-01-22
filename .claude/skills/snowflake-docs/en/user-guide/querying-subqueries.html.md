---
auto_generated: true
description: A subquery is a query within another query. Subqueries in a FROM or WHERE
  clause are used to provide data that will be used to limit or compare/evaluate the
  data returned by the containing query.
last_scraped: '2026-01-14T16:55:23.763176+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/querying-subqueries.html
title: Working with Subqueries | Snowflake Documentation
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

[Guides](../guides/README.md)[Queries](../guides/overview-queries.md)Subqueries

# Working with Subqueries[¶](#working-with-subqueries "Link to this heading")

A subquery is a query within another query. Subqueries in a [FROM](../sql-reference/constructs/from) or [WHERE](../sql-reference/constructs/where)
clause are used to provide data that will be used to limit or compare/evaluate the data returned by the containing query.

## Types of Subqueries[¶](#types-of-subqueries "Link to this heading")

### Correlated vs. Uncorrelated Subqueries[¶](#correlated-vs-uncorrelated-subqueries "Link to this heading")

Subqueries can be categorized as *correlated* or *uncorrelated*:

* A correlated subquery refers to one or more columns from outside of
  the subquery. (The columns are typically referenced inside the `WHERE`
  clause of the subquery.) A correlated subquery can be thought of as a filter
  on the table that it refers to, as if the subquery were evaluated on each
  row of the table in the outer query.
* An uncorrelated subquery has no such external column references. It
  is an independent query, the results of which are returned to and used by
  the outer query once (not per row).

For example:

> ```
> -- Uncorrelated subquery:
> SELECT c1, c2
>   FROM table1 WHERE c1 = (SELECT MAX(x) FROM table2);
>
> -- Correlated subquery:
> SELECT c1, c2
>   FROM table1 WHERE c1 = (SELECT x FROM table2 WHERE y = table1.c2);
> ```
>
> Copy

### Scalar vs. Non-scalar Subqueries[¶](#scalar-vs-non-scalar-subqueries "Link to this heading")

Subqueries can also be categorized as *scalar* or *non-scalar*:

* A scalar subquery returns a single value (one column of one row).
  If no rows qualify to be returned, the subquery returns NULL.
* A non-scalar subquery returns 0, 1, or multiple rows, each of which
  may contain 1 or multiple columns. For each column, if there is no value to
  return, the subquery returns NULL. If no rows qualify to be returned, the
  subquery returns 0 rows (not NULLs).

### Types Supported by Snowflake[¶](#types-supported-by-snowflake "Link to this heading")

Snowflake currently supports the following types of subqueries:

* Uncorrelated scalar subqueries in any place that a value expression can be used.
* Correlated scalar subqueries in [WHERE](../sql-reference/constructs/where) clauses.
* EXISTS, ANY / ALL, and IN subqueries in [WHERE](../sql-reference/constructs/where) clauses. These subqueries can be correlated or uncorrelated.

## Subquery Operators[¶](#subquery-operators "Link to this heading")

[Subquery operators](../sql-reference/operators-subquery) operate on nested query expressions. They can be used to compute values that are:

* Returned in a [SELECT](../sql-reference/sql/select) list.
* Grouped in a [GROUP BY](../sql-reference/constructs/group-by) clause.
* Compared with other expressions in the [WHERE](../sql-reference/constructs/where) or [HAVING](../sql-reference/constructs/having) clause.

## Differences Between Correlated and Non-Correlated Subqueries[¶](#differences-between-correlated-and-non-correlated-subqueries "Link to this heading")

The following query demonstrates an uncorrelated subquery in a [WHERE](../sql-reference/constructs/where) clause.
The subquery gets the per capita GDP of Brazil, and the outer query
selects all the jobs (in any country) that pay less than the
per-capita GDP of Brazil. The subquery is uncorrelated because the value
that it returns does not depend upon any column of the outer query. The
subquery only needs to be called once during the entire execution of the
outer query.

> ```
> SELECT p.name, p.annual_wage, p.country
>   FROM pay AS p
>   WHERE p.annual_wage < (SELECT per_capita_GDP
>                            FROM international_GDP
>                            WHERE name = 'Brazil');
> ```
>
> Copy

The next query demonstrates a correlated subquery in a [WHERE](../sql-reference/constructs/where) clause.
The query lists jobs where the annual pay of the job is less than the
per-capita GDP in that country.
This subquery is correlated because it is called once for each row in the
outer query and is passed a value, `p.country` (country name), from the row.

> ```
> SELECT p.name, p.annual_wage, p.country
>   FROM pay AS p
>   WHERE p.annual_wage < (SELECT MAX(per_capita_GDP)
>                            FROM international_GDP i
>                            WHERE p.country = i.name);
> ```
>
> Copy

Note

The [MAX](../sql-reference/functions/max) aggregate function is not logically necessary in this case because the
`international_GDP` table has only one row per country; however, because the server doesn’t know that, and because the server
requires that the subquery return no more than one row, the query uses the aggregate function to force the server to recognize that the
subquery will return only one row each time that the subquery is executed.

The functions [MIN](../sql-reference/functions/min) and [AVG](../sql-reference/functions/avg) also work because
applying either of these to a single value returns that value unchanged.

## Scalar Subqueries[¶](#scalar-subqueries "Link to this heading")

A scalar subquery is a subquery that returns at most one row. A scalar subquery can appear anywhere that a value expression can appear, including
the [SELECT](../sql-reference/sql/select) list, [GROUP BY](../sql-reference/constructs/group-by) clause, or as an argument to a function in a
[WHERE](../sql-reference/constructs/where) or [HAVING](../sql-reference/constructs/having) clause.

### Usage Notes[¶](#usage-notes "Link to this heading")

* A scalar subquery can contain only one item in the [SELECT](../sql-reference/sql/select) list.
* If a scalar subquery returns more than one row, a runtime error is generated.
* Correlated scalar subqueries are currently supported only if they can be statically determined to return one row (e.g. if the
  [SELECT](../sql-reference/sql/select) list contains an aggregate function with no [GROUP BY](../sql-reference/constructs/group-by)).
* Uncorrelated scalar subqueries are supported anywhere that a value expression is allowed.
* Subqueries with a correlation inside of [FLATTEN](../sql-reference/functions/flatten) are currently unsupported.
* The [LIMIT / FETCH](../sql-reference/constructs/limit) clause is allowed only in uncorrelated scalar subqueries.

### Examples[¶](#examples "Link to this heading")

This example shows a basic uncorrelated subquery in a WHERE clause:

> ```
> SELECT employee_id
> FROM employees
> WHERE salary = (SELECT max(salary) FROM employees);
> ```
>
> Copy

This example shows an uncorrelated subquery in a FROM clause; this basic subquery
returns a subset of the information in the `international_GDP` table.
The overall query lists jobs in “high-wage” countries where the annual pay
of the job is the same as the per\_capita\_GDP in that country.

> ```
> SELECT p.name, p.annual_wage, p.country
>   FROM pay AS p INNER JOIN (SELECT name, per_capita_GDP
>                               FROM international_GDP
>                               WHERE per_capita_GDP >= 10000.0) AS pcg
>     ON pcg.per_capita_GDP = p.annual_wage AND p.country = pcg.name;
> ```
>
> Copy

## Limitations[¶](#limitations "Link to this heading")

Although subqueries can contain a wide range of SELECT statements, they have the following limitations:

* Some clauses are not allowed inside of ANY/ALL/NOT EXISTS subqueries.
* The only type of subquery that allows a
  [LIMIT / FETCH](../sql-reference/constructs/limit) clause is an uncorrelated scalar
  subquery. Also, because an uncorrelated scalar subquery returns only 1 row,
  the LIMIT clause has little or no practical value inside a subquery.

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

1. [Types of Subqueries](#types-of-subqueries)
2. [Subquery Operators](#subquery-operators)
3. [Differences Between Correlated and Non-Correlated Subqueries](#differences-between-correlated-and-non-correlated-subqueries)
4. [Scalar Subqueries](#scalar-subqueries)
5. [Limitations](#limitations)

Related content

1. [Subquery operators](/user-guide/../sql-reference/operators-subquery)