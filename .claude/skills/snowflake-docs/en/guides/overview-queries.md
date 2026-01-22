---
auto_generated: true
description: 'Snowflake supports standard SQL, including a subset of ANSI SQL:1999
  and the SQL:2003 analytic extensions. Snowflake also supports common variations
  for a number of commands where those variations do '
last_scraped: '2026-01-14T16:54:19.209556+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/guides-overview-queries
title: Query Data in Snowflake | Snowflake Documentation
---

1. [Overview](README.md)
2. [Snowflake Horizon Catalog](../user-guide/snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](overview-connecting.md)
6. [Virtual warehouses](../user-guide/warehouses.md)
7. [Databases, Tables, & Views](overview-db.md)
8. [Data types](../data-types.md)
10. Data Integration

    - [Snowflake Openflow](../user-guide/data-integration/openflow/about.md)
    - Apache Iceberg™

      - [Apache Iceberg™ Tables](../user-guide/tables-iceberg.md)
      - [Snowflake Open Catalog](../user-guide/opencatalog/overview.md)
11. Data engineering

    - [Data loading](overview-loading-data.md)
    - [Dynamic Tables](../user-guide/dynamic-tables-about.md)
    - [Streams and Tasks](../user-guide/data-pipelines-intro.md)
    - [dbt Projects on Snowflake](../user-guide/data-engineering/dbt-projects-on-snowflake.md)
    - [Data Unloading](overview-unloading-data.md)
12. [Storage Lifecycle Policies](../user-guide/storage-management/storage-lifecycle-policies.md)
13. [Migrations](../migrations/README.md)
15. [Queries](overview-queries.md)

    * [Joins](../user-guide/querying-joins.md)
    * [Subqueries](../user-guide/querying-subqueries.md)
    * [Querying Hierarchical Data](../user-guide/queries-hierarchical.md)
    * [Common Table Expressions (CTE)](../user-guide/queries-cte.md)")
    * [Querying Semi-structured Data](../user-guide/querying-semistructured.md)
    * [Using full-text search](../user-guide/querying-with-search-functions.md)
    * [Constructing SQL at Runtime](../user-guide/querying-construct-at-runtime.md)
    * [Analyzing time-series data](../user-guide/querying-time-series-data.md)
    * [Analyzing data with window functions](../user-guide/functions-window-using.md)
    * [Match Recognize](../user-guide/match-recognize-introduction.md)
    * [Sequences](../user-guide/querying-sequences.md)
    * [Persisted Query Results](../user-guide/querying-persisted-results.md)
    * [Distinct Counts](../user-guide/querying-distinct-counts.md)
    * [Similarity Estimation](../user-guide/querying-approximate-similarity.md)
    * [Frequency Estimation](../user-guide/querying-approximate-frequent-values.md)
    * [Estimating Percentile Values](../user-guide/querying-approximate-percentile-values.md)
    * [Monitor query activity with Query History](../user-guide/ui-snowsight-activity.md)
    * [Using query insights to improve performance](../user-guide/query-insights.md)
    * [Query Hash](../user-guide/query-hash.md)
    * [Top-K pruning](../user-guide/querying-top-k-pruning-optimization.md)
    * [Cancel Statements](../user-guide/querying-cancel-statements.md)
16. [Listings](../collaboration/collaboration-listings-about.md)
17. [Collaboration](overview-sharing.md)
19. [Snowflake AI & ML](overview-ai-features.md)
21. [Snowflake Postgres](../user-guide/snowflake-postgres/about.md)
23. [Alerts & Notifications](overview-alerts.md)
25. [Security](overview-secure.md)
26. [Data Governance](overview-govern.md)
27. [Privacy](overview-privacy.md)
29. [Organizations & Accounts](overview-manage.md)
30. [Business continuity & data recovery](../user-guide/replication-intro.md)
32. [Performance optimization](overview-performance.md)
33. [Cost & Billing](overview-cost.md)

[Guides](README.md)Queries

# Query Data in Snowflake[¶](#query-data-in-snowflake "Link to this heading")

Snowflake supports standard SQL, including a subset of ANSI SQL:1999 and the SQL:2003 analytic extensions.
Snowflake also supports common variations for a number of commands where those variations do not conflict with each other.

Tip

You can use the search optimization service to improve query performance.
For details, see [Search optimization service](user-guide/search-optimization-service).

[Working with joins](user-guide/querying-joins)
:   A join combines rows from two tables to create a new combined row that can be used in the query.

    Learn join concepts, types of joins, and how to work with joins.

[Analyzing time-series data](user-guide/querying-time-series-data)
:   Analyze time-series data, using SQL functionality designed for this purpose, such as the ASOF JOIN feature, date and time
    helper functions, aggregate functions for downsampling, and functions that support sliding window frames.

    Using ASOF JOIN, learn how to join tables on timestamp columns when their values closely follow each other, precede each other,
    or match exactly.

[Eliminate Redundant Joins](user-guide/join-elimination)
:   A join on a key column can refer to tables that are not needed for the join. Such a join is referred to as a *redundant join*.

    Learn about redundant joins, and how to eliminate them to improve query performance.

[Working with Subqueries](user-guide/querying-subqueries)
:   A subquery is a query within another query.

    Learn about subqueries and how to use them.

[Querying Hierarchical Data](user-guide/queries-hierarchical)
:   Relational databases often store hierarchical data by using different tables.

    Learn about querying hierarchical data using joins, Common Table Expressions(CTEs) and CONNECT BY.

[Working with CTEs (Common Table Expressions)](user-guide/queries-cte)
:   A CTE (common table expression) is a named subquery defined in a WITH clause, the result of which is effectively a table.

    Learn how to write and work with CTE expressions.

[Querying Semi-structured Data](user-guide/querying-semistructured)
:   Semi-structured data represents arbitrary hierarchical data structures, which can be used to load and operate on
    data in semi-structured formats (e.g. JSON, Avro, ORC, Parquet, or XML).

    Learn how to use special operators and functions to query complex hierarchical data stored in a VARIANT.

[Using full-text search](user-guide/querying-with-search-functions)
:   You can use full-text search to find character data (text) in specified columns
    from one or more tables, including fields in VARIANT, OBJECT, and ARRAY columns.

    Learn how to run queries that use full-text search.

[Constructing SQL at runtime](user-guide/querying-construct-at-runtime)
:   You can create programs that construct SQL statements dynamically at runtime.

    Learn about different options for constructing SQL at runtime.

[Analyzing data with window functions](user-guide/functions-window-using)
:   Window functions operate on windows, which are groups of rows that are related in some way.

    Learn about windows, window functions, and how to use window functions to examine data.

[Identifying Sequences of Rows That Match a Pattern](user-guide/match-recognize-introduction)
:   In some cases, you might need to identify sequences of table rows that match a pattern.

    Learn about pattern matching, and how to use MATCH\_RECOGNIZE to work with table rows matching patterns.

[Using Sequences](user-guide/querying-sequences)
:   Sequences are used to generate unique numbers across sessions and statements, including concurrent statements.

    Learn what are sequences, and how to use them.

[Using Persisted Query Results](user-guide/querying-persisted-results)
:   When a query is executed, the result is persisted for a period of time.

    Learn how query results are persisted, how long persisted results are available,
    and how to use persisted query results to improve performance.

[Computing the Number of Distinct Values](user-guide/querying-distinct-counts)
:   Various methods exist to determine the count of distinct elements within a column.

    Learn methods to identify and report distinct elements in data.

[Estimating Similarity of Two or More Sets](user-guide/querying-approximate-similarity)
:   Snowflake provides mechanisms to compare data sets for similarity.

    Learn how Snowflake determines similarity and how to compare multiple data sets for similarity.

[Estimating Frequent Values](user-guide/querying-approximate-frequent-values)
:   Snowflake can examine data to determine how frequent values are within the data.

    Learn how frequency is determined and how to query data to determine data frequency using the through the APPROX\_TOP\_K family of functions.

[Estimating Percentile Values](user-guide/querying-approximate-percentile-values)
:   Snowflake can estimate percentages of values using an improved version of the t-Digest algorithm.

    Learn how to estimate percentages using the APPROX\_PERCENTILE family of functions

[Monitor query activity with Query History](user-guide/ui-snowsight-activity)
:   Monitor the query activity in your account.

    Learn how examine queries, using query profiles, to understand and improve performance.

[Using query insights to improve performance](user-guide/query-insights)
:   Review the insights produced for a query.

    Learn how to improve the performance of a query.

[Using the Query Hash to Identify Patterns and Trends in Queries](user-guide/query-hash)
:   To identify patterns and trends in queries, you can use the hash of the query text, which is included in the `query_hash` and
    `query_parameterized_hash` columns in selected Account Usage view and in the output of selected Information Schema table
    functions.

    Learn how to use the query hash in these columns to identify repeated queries and detect patterns and trends in queries.

[Top-K pruning for improved query performance](user-guide/querying-top-k-pruning-optimization)
:   Instead of scanning all eligible rows in SELECT statements that contain LIMIT and ORDER BY clauses, SELECT statements
    that use top-K pruning scan a subset of rows, which can improve performance.

    Learn how to use top-K pruning to improve the performance of SELECT statements that contain LIMIT and ORDER BY clauses.

[Canceling Statements](user-guide/querying-cancel-statements)
:   Executing statements are typically cancelled using the interface used to start the query.

    Learn how to use system functions to cancel a specific query or all currently executing queries.

Was this page helpful?

YesNo

[Visit Snowflake](https://www.snowflake.com)

[Join the conversation](https://community.snowflake.com/s/)

[Develop with Snowflake](https://developers.snowflake.com)

[Share your feedback](/feedback)

[Read the latest on our blog](https://www.snowflake.com/blog/)

[Get your own certification](https://learn.snowflake.com)

[Privacy Notice](https://www.snowflake.com/privacy-policy/)[Site Terms](https://www.snowflake.com/legal/snowflake-site-terms/)Cookies Settings© 2026 Snowflake, Inc. All Rights Reserved.