---
auto_generated: true
description: Feature — Generally Available
last_scraped: '2026-01-14T16:57:38.227390+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/interactive
title: Snowflake interactive tables and interactive warehouses | Snowflake Documentation
---

1. [Overview](../guides/README.md)
2. [Snowflake Horizon Catalog](snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../guides/overview-connecting.md)
6. [Virtual warehouses](warehouses.md)

   * [Overview](warehouses-overview.md)
   * [Multi-cluster](warehouses-multicluster.md)
   * [Considerations](warehouses-considerations.md)
   * [Working with warehouses](warehouses-tasks.md)
   * [Next-generation standard warehouses](warehouses-gen2.md)
   * [Query Acceleration Service](query-acceleration-service.md)
   * [Monitoring load](warehouses-load-monitoring.md)
   * [Snowpark-optimized warehouses](warehouses-snowpark-optimized.md)
   * [Interactive tables and warehouses](interactive.md)
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

[Guides](../guides/README.md)[Virtual warehouses](warehouses.md)Interactive tables and warehouses

# Snowflake interactive tables and interactive warehouses[¶](#snowflake-interactive-tables-and-interactive-warehouses "Link to this heading")

Feature — Generally Available

This feature is generally available in select Amazon Web Services (AWS) regions only. For details,
see [Region availability](#label-interactive-region-availability).

This topic introduces Snowflake *interactive tables* and *interactive warehouses*. They deliver low-latency query performance for
high-concurrency, interactive workloads.

Note

Interactive tables now support join queries.

## Overview of interactive warehouses and interactive tables[¶](#overview-of-interactive-warehouses-and-interactive-tables "Link to this heading")

The following are the new kinds of Snowflake objects that you use with this feature.
You can expect better query performance when you run queries on interactive tables
using interactive warehouses.

Interactive warehouse
:   A new type of warehouse that’s optimized for low-latency, interactive workloads.

    An interactive warehouse tunes the Snowflake engine specially for low-latency, interactive workloads.
    It leverages additional metadata and index information in the underlying interactive tables to accelerate queries.
    This type of warehouse is optimized to run continuously, serving high volumes of concurrent queries.
    All interactive warehouses run on the latest generation of hardware.

Interactive table
:   A new type of Snowflake table, specialized for low-latency, interactive queries.

    You get the best performance gains when you query these tables through interactive warehouses. Interactive tables have different methods for data ingestion and
    support a more limited set of SQL statements and query operators than standard Snowflake tables.

![Diagram showing how users work with Interactive warehouses and Interactive tables.](../_images/interactive-warehouses.png)

## Use cases for interactive tables[¶](#use-cases-for-interactive-tables "Link to this heading")

Snowflake interactive tables are optimized for fast, simple queries when you require consistent
low-latency responses. Interactive warehouses provide the compute resources required to serve these
queries efficiently. Together, they enable use cases such as real-time dashboards, data-powered
APIs, and serving high-concurrency workloads.

The simple queries that work best with interactive tables are usually SELECT statements with
selective WHERE clauses, optionally including a GROUP BY clause on a few dimensions. Avoid queries
involving large joins and large subqueries. The performance of queries that use other features, such
as window functions, is highly dependent on the data shapes that you are querying.

## Region availability[¶](#region-availability "Link to this heading")

Interactive tables and interactive warehouses are available in the following Amazon Web Services (AWS) regions. For more information about Snowflake regions, see [Supported cloud regions](intro-regions).

* `us-east-1` - US East (N. Virginia)
* `us-west-2` - US West (Oregon)
* `us-east-2` - US East (Ohio)
* `ca-central-1` - Canada (Central)
* `ap-northeast-1` - Asia Pacific (Tokyo)
* `ap-southeast-2` - Asia Pacific (Sydney)
* `eu-central-1` - EU (Frankfurt)
* `eu-west-1` - EU (Ireland)
* `eu-west-2` - Europe (London)

## Limitations of interactive warehouses and interactive tables[¶](#limitations-of-interactive-warehouses-and-interactive-tables "Link to this heading")

The following limitations apply to interactive warehouses and interactive tables. Some limitations
are due to architectural differences between interactive tables and standard Snowflake tables;
those limitations are intended to be permanent.

### Limitations of interactive warehouses[¶](#limitations-of-interactive-warehouses "Link to this heading")

* Snowflake interactive warehouses don’t support long-running queries. The query timeout for SELECT
  commands defaults to five seconds. After five seconds, the query is canceled. You can reduce the
  query timeout value but you can’t increase it. Other kinds of commands, such as SHOW and INSERT
  OVERWRITE, aren’t subject to the five-second timeout interval.

  Interactive warehouses aren’t intended for use with long-running queries. If a query consistently
  times out, that’s a signal that it might not be suitable for use with interactive warehouses.
  Otherwise, you need to apply some of the performance tuning techniques to reduce the time to less
  than five seconds.
* An interactive warehouse is always up and running by design. It doesn’t automatically suspend when
  idle. Although you can manually suspend an interactive warehouse, expect significant query latency
  when you resume the warehouse.
* You can’t query standard Snowflake tables from an interactive warehouse. To query both standard
  tables and interactive tables in the same session, run USE WAREHOUSE to switch to the appropriate
  warehouse type depending on the type of table.
* If an interactive warehouse is a multi-cluster warehouse, it doesn’t auto-scale. In a multi-cluster
  interactive warehouse, always keep MIN\_CLUSTER\_COUNT and MAX\_CLUSTER\_COUNT set to the same value.
* You can’t run CALL commands to call stored procedures in an interactive warehouse.
* You can’t use the `->>` pipe operator. This operator uses stored procedures behind the scenes.
* Interactive warehouses currently don’t support replication. They aren’t included in failover
  groups and replication groups.

### Limitations of interactive tables[¶](#limitations-of-interactive-tables "Link to this heading")

* Interactive tables don’t support the following features:

  + Data manipulation language (DML) commands such as UPDATE and DELETE. The only DML that you can
    perform is INSERT OVERWRITE.
  + Replication. They aren’t included in failover groups and replication groups.
* Query insights are currently not collected or available for queries executing on interactive tables.
* You can’t perform the following operations:

  + Use an interactive table as the source for a materialized view.
  + Modify properties of an interactive table by using ALTER TABLE clauses such as ADD
    COLUMN or REMOVE COLUMN. The only ALTER TABLE change that you can make is to rename the table.
  + Use data masking policies with an interactive table.
  + Use join policies with an interactive table.
  + Use aggregation policies with an interactive table.
  + Use row access policies with an interactive table.
  + Use streams with an interactive table.
  + Create a dynamic table with an interactive table as a base table.
  + Use the RESAMPLE clause for queries on an interactive table.

## Getting started with interactive tables[¶](#getting-started-with-interactive-tables "Link to this heading")

To get started with interactive tables, complete the following sequence of steps:

1. Create an interactive table, using a standard warehouse. For more information, see
   [Creating an interactive table](#label-interactive-create-an-interactive-table).
2. Create an interactive warehouse. For more information, see
   [Creating an interactive warehouse](#label-interactive-create-an-interactive-warehouse).
3. Resume the interactive warehouse. For more information, see
   [Resuming and suspending a warehouse](#label-interactive-resume-and-suspend-a-warehouse).
4. Add the interactive table to the interactive warehouse. For more information, see
   [Adding an interactive table to an interactive warehouse](#label-interactive-adding-table-to-an-interactive-warehouse).
5. Start querying the interactive table through the interactive warehouse. For more information, see
   [Querying an interactive table](#label-interactive-querying-an-interactive-table).

## Working with interactive tables and interactive warehouses[¶](#working-with-interactive-tables-and-interactive-warehouses "Link to this heading")

The following procedures explain how to create and manage all the required
objects to run queries using interactive tables. When you are trying this
feature for the first time, perform these procedures in the following order.

### Creating an interactive table[¶](#creating-an-interactive-table "Link to this heading")

Table creation follows the standard CTAS ([CREATE TABLE AS SELECT](../sql-reference/sql/create-table.html#label-ctas-syntax)) syntax,
with the additional INTERACTIVE keyword that defines the table type.

The CREATE INTERACTIVE TABLE command also requires a CLUSTER BY clause.
Specify one or more columns in the CLUSTER BY clause to match the WHERE clauses in your most time-critical queries.
The columns you specify in the CLUSTER BY clause can significantly affect the performance
of queries on the interactive table. Therefore, choose the clustering columns carefully.
For more information about choosing the best clustering columns, see [Clustering Keys & Clustered Tables](tables-clustering-keys).

Note

You run the CREATE INTERACTIVE TABLE command with a standard warehouse.
You only use the interactive warehouse in later steps, to query the interactive table.

The following command creates an interactive table containing the same columns and data
as a standard table. The CLUSTER BY clause refers to a column named `id` from the source table.

```
CREATE INTERACTIVE TABLE
  IF NOT EXISTS orders
  CLUSTER BY (id)
AS
  SELECT * FROM demoSource;
```

Copy

### Specifying auto-refresh for an interactive table[¶](#specifying-auto-refresh-for-an-interactive-table "Link to this heading")

To make an interactive table automatically refresh using data from some
other table, specify the TARGET\_LAG clause with an interval.
When you specify TARGET\_LAG, you must also specify the WAREHOUSE clause
and the name of a standard warehouse that Snowflake will use to perform
refresh operations.

The time interval for the TARGET\_LAG clause lets you specify the maximum
lag in terms of some number of seconds, minutes, hours, or days:

```
TARGET_LAG = '<num> { seconds | minutes | hours | days }'
```

Copy

If you don’t specify a unit, the number represents seconds. The minimum value
is 60 seconds, or 1 minute.

For example, the following CREATE INTERACTIVE TABLE statement defines a dynamic interactive table
that lags no more than 20 minutes behind a specified source table, and uses a standard warehouse
named `my_standard_warehouse` to perform refresh operations:

```
CREATE INTERACTIVE TABLE my_dynamic_interactive_table
  CLUSTER BY (c1, c2)
  TARGET_LAG = '20 minutes'
  WAREHOUSE = my_standard_warehouse
AS SELECT c1, SUM(c2) FROM my_source_table GROUP BY c1;
```

Copy

For more information about choosing an appropriate lag time that balances costs and freshness of data,
see [Determine the optimal target lag for a dynamic table](dynamic-tables-target-lag.html#label-dynamic-tables-lag-time). Similar considerations apply to interactive tables as to
dynamic tables.

### Creating an interactive warehouse[¶](#creating-an-interactive-warehouse "Link to this heading")

After you create an interactive table, querying that table with optimal performance requires an interactive warehouse.
Specify the keyword INTERACTIVE in the [CREATE WAREHOUSE](../sql-reference/sql/create-warehouse) or CREATE OR REPLACE WAREHOUSE command.

Optionally, you can specify a TABLES clause with a comma-separated list of interactive table names.
Using that clause immediately associates those interactive tables with the interactive warehouse.

The following command creates an interactive warehouse that’s associated with the interactive table
named `orders`. In this case, you can immediately run a [USE WAREHOUSE](../sql-reference/sql/use-warehouse)
command for the interactive warehouse, and begin running queries for the interactive table:

```
CREATE OR REPLACE INTERACTIVE WAREHOUSE interactive_demo
  TABLES (orders)
  WAREHOUSE_SIZE = 'XSMALL';
```

Copy

The following command creates an interactive warehouse with no associated interactive tables.
In this case, you run ALTER WAREHOUSE commands afterward to associate interactive tables
with the interactive warehouse:

```
CREATE or REPLACE INTERACTIVE WAREHOUSE interactive_demo
  WAREHOUSE_SIZE = 'XSMALL';
```

Copy

After you create an interactive warehouse, the warehouse remains active indefinitely by default.
Unlike a traditional warehouse, an interactive warehouse doesn’t include an option to automatically
suspend it if it’s idle for some period of time.

## Interactive Table Performance Considerations[¶](#interactive-table-performance-considerations "Link to this heading")

The following sections explain how to solve performance issues that you might encounter due to
the special characteristics of interactive tables and the workloads they’re best suited for.

### Query best practices for interactive warehouses[¶](#query-best-practices-for-interactive-warehouses "Link to this heading")

Interactive warehouses are optimized for queries with **selective workloads**. This means queries
with good selectivity see substantially more improvements on performance than other query types.

| Expect more performance benefits with interactive warehouses | Expect limited performance benefits with interactive warehouses |
| --- | --- |
| ``` SELECT col1, col4, AVG(col_x)   FROM my_table   GROUP BY col1, col2; ```  Copy  This query is highly selective because it only requires a few columns. Snowflake can optimize loading only columns required for this one query. | ``` SELECT * FROM my_table; ```  Copy  This query processes all columns. Although the query is simple, Snowflake must process a large amount of data, which might exceed the size of the cache. Even if the contents of the table can fit in the cache, that leaves less room to cache data from other queries, leading to lower concurrency. |
| ``` SELECT col1, col2   FROM my_table   WHERE     col_x IN (1,4,7,8)     AND event_time >=       DATEADD(hour, -1, CURRENT_TIMESTAMP()); ```  Copy  The conditions in the WHERE clause make this query highly selective. The IN clause limits the results to a relatively few items, and the time comparison further limits the data to a certain time period. | ``` SELECT col1, col2   FROM my_table   WHERE     event_time >=       DATEADD(day, -365, CURRENT_TIMESTAMP()); ```  Copy  Asking for data for an entire year makes this query less selective. If your dataset is big, this query might process all rows in the table. |

Other complexities such as large joins (such as joining two fact tables), or compute-intensive expressions such
as regular expressions, might result in lower concurrency due to higher use of compute resources.
See [Choosing a size for an interactive warehouse](#label-interactive-warehouse-size-considerations) for information about optimizing for
those situations.

### Data layout best practices for interactive tables[¶](#data-layout-best-practices-for-interactive-tables "Link to this heading")

Interactive tables follow standard Snowflake best practices for performance. In particular,
interactive tables benefit from a **well-clustered table**, a table that’s sorted based on the same
column or columns that you are filtering on. For example, if your query often filters on a TIMESTAMP
column such as `sale_date`, then it makes sense to use that column as the clustering key when creating
the interactive table. For example, you might create the interactive table as follows:

```
CREATE INTERACTIVE TABLE product_sales (<column definitions>) CLUSTER BY (sale_date);
```

Copy

That way, SELECT queries that filter on `sale_date` can quickly skip all irrelevant data
and return results. For example, the following query filters on a date range by testing the
`sale_date` column:

```
SELECT... WHERE sale_date > '2025-10-24' AND ...
```

Copy

For more details about choosing the best clustering keys, see
[Clustering Keys & Clustered Tables](tables-clustering-keys).

### Using Search Optimization for point lookups[¶](#using-search-optimization-for-point-lookups "Link to this heading")

We recommend adding [Search Optimization](search-optimization/enabling) when you
perform point lookup queries on your interactive table. Point lookups are queries that filter on a
single column to retrieve one or a few rows of data. A good example is `WHERE some_id =
some_UUID`.

### Choosing a size for an interactive warehouse[¶](#choosing-a-size-for-an-interactive-warehouse "Link to this heading")

Once you’ve completed all your queries and layout optimizations, consider **scaling your warehouse**
to meet demand. Interactive warehouses have a range of sizes from XSMALL to 3XLARGE, as well as
[Multi-cluster warehouses](warehouses-multicluster).

We recommend that you start by sizing your warehouse based on the approximate size of the *working
data set* in the interactive table. The working data set refers to the portion of the data that is
frequently queried. For example, if your queries typically only query the last seven days of sales data,
the working set is the fraction of the interactive table corresponding to those seven days.

This is because the interactive warehouse utilizes *local storage caching*. While the data for
your entire data set (table) is always accessible, accessing non-cached data does incur higher read
latency on the first read.

Choose a warehouse size to fit the needs of your workloads. Experiment with your particular data and
workload to determine the optimal size for your interactive warehouse. You can make a multi-cluster
warehouse that’s interactive. However, currently the minimum and maximum cluster count must be
equal. That is, the interactive multi-cluster warehouse doesn’t automatically scale.

Tip

For good performance, you don’t need to fit the entire working set of your queries in the cache.
Pick a cache size that’s sufficient to hold your *hot data*, that is, the data from your
frequently accessed rows.

We recommend starting with the following warehouse sizes based on the working data set size.

| Working Set | Warehouse Size |
| --- | --- |
| Less than 500 GB | XSMALL |
| 500 GB to 1 TB | SMALL |
| 1 TB to 2 TB | MEDIUM |
| 2 TB to 4 TB | LARGE |
| 4 TB to 8 TB | XLARGE |
| 8 TB to 16 TB | 2XLARGE |
| Greater than 16 TB | 3XLARGE |

#### Performance troubleshooting for interactive tables[¶](#performance-troubleshooting-for-interactive-tables "Link to this heading")

##### Problem 1: My single query is taking too long[¶](#problem-1-my-single-query-is-taking-too-long "Link to this heading")

This is likely due to your query requiring more computing resources to finish. It’s possible that your
query has a lot of complex processing, thus requiring more CPUs. For example, queries with a lot of
regular expression filters and CASE clauses. It’s also possible that your queries require a lot of memory, such
as queries that do a lot of `COUNT(DISTINCT ...)`. To lower the run time of a single query,
consider a **larger warehouse size**. Start with the recommended size above, and keep
increasing the size of the warehouse until you are satisfied with a single query’s latency.

##### Problem 2: My queries are suddenly taking a long time to run (High tail latency, high P95 latency)[¶](#problem-2-my-queries-are-suddenly-taking-a-long-time-to-run-high-tail-latency-high-p95-latency "Link to this heading")

A sudden increase in query time is likely due to insufficient caching. Each warehouse size has a
local SDD cache that we use to cache the most recently used data. Snowflake manages the cache to
only store parts of the table that are accessed frequently. If your queries are selective, then
increasing warehouse size can potentially reduce tail latency.

Also note, the newly spun-up warehouse takes a while to **warm the cache**. Snowflake proactively
warms the newly added data. For benchmarking, wait for a while before starting the benchmark so that
the cache has time to warm up. Cache warm-up speed is based on warehouse size and table size. The
bigger your interactive table is, the longer Snowflake takes to warm the cache. On the other hand,
the larger the size you specify for the interactive warehouse, the shorter the warming time.

##### Problem 3: My query is queuing or I’m not able to fulfill the query concurrency[¶](#problem-3-my-query-is-queuing-or-i-m-not-able-to-fulfill-the-query-concurrency "Link to this heading")

You can scale out your warehouse by setting the MIN\_CLUSTER\_COUNT and MAX\_CLUSTER\_COUNT parameters.
That way, you can create a multi-cluster interactive warehouse. Currently, multi-cluster interactive
warehouses don’t support auto-scaling. Therefore, specify the same value for both the minimum and
maximum cluster count. Because it takes time to warm a warehouse, manual scaling tends to provide
better economics for our users while still enabling predictable performance.

### Adding an interactive table to an interactive warehouse[¶](#adding-an-interactive-table-to-an-interactive-warehouse "Link to this heading")

To get optimal query performance for an interactive table, you should use an interactive warehouse.

Before you can query the interactive table from an interactive warehouse, you must perform a one-time operation to add the interactive
table to the interactive warehouse. Otherwise, you’ll see “object not found” error when running a query against such a table from the interactive warehouse.
If you didn’t specify the interactive tables to associate with the interactive warehouses by using the
TABLES clause in your CREATE INTERACTIVE WAREHOUSE command, you can do that later by using an [ALTER WAREHOUSE](../sql-reference/sql/alter-warehouse) command.

The following command associates the `orders` table with the `interactive_demo` warehouse. You can specify multiple table
names, separated by commas, with the ADD TABLES clause.

```
ALTER WAREHOUSE interactive_demo ADD TABLES (orders);
```

Copy

This action starts the cache-warming process. That process might take significant time.

If the interactive table is already associated with the interactive warehouse, the command
succeeds but has no effect.

You can associate an interactive table with multiple interactive warehouses.

### Removing an interactive table from an interactive warehouse[¶](#removing-an-interactive-table-from-an-interactive-warehouse "Link to this heading")

You can detach one or more interactive tables from an interactive warehouse by running an [ALTER WAREHOUSE](../sql-reference/sql/alter-warehouse) command
with the DROP TABLES clause.

```
ALTER WAREHOUSE interactive_demo DROP TABLES (orders, customers);
```

Copy

Note

The interactive tables still exist after this operation. This ALTER WAREHOUSE clause isn’t the same as performing the SQL command DROP TABLE.

### Resuming and suspending a warehouse[¶](#resuming-and-suspending-a-warehouse "Link to this heading")

The following command resumes an interactive warehouse. You must do this after creating the warehouse, because it’s
created in a suspended state:

```
ALTER WAREHOUSE interactive_demo RESUME;
```

Copy

You also do this to start running queries through the warehouse, if you manually suspended the warehouse.

Queries will be slow while the cache is being warmed after resuming. It might take a
few minutes to an hour or so, depending on how much data you have in that table.

The following command suspends an interactive warehouse:

```
ALTER WAREHOUSE interactive_demo SUSPEND;
```

Copy

You might suspend the warehouse in development and test environments where it won’t be used for many hours. In a production
environment, you typically use interactive warehouses for workloads running many concurrent queries 24x7, or where low latency is
crucial for queries. Thus, you typically don’t suspend interactive warehouses that you use in production. Snowflake doesn’t
automatically suspend interactive warehouses.

### Dropping an interactive warehouse[¶](#dropping-an-interactive-warehouse "Link to this heading")

You can run the [DROP WAREHOUSE](../sql-reference/sql/drop-warehouse) command to remove an interactive warehouse entirely. Dropping an
interactive warehouse removes the associations between that warehouse and any interactive tables. However, you can still use other
interactive warehouses to query those same interactive tables.

### Querying an interactive table[¶](#querying-an-interactive-table "Link to this heading")

In your query session, make sure that the warehouse for your current session is an interactive warehouse:

```
USE WAREHOUSE interactive_demo;
```

Copy

After this, you can query your interactive table normally.

Note

* In an interactive warehouse, you can only query interactive tables. To query other types of Snowflake tables, such as standard
  tables or hybrid tables, switch to a standard warehouse first.
* Certain types of queries are especially suited for interactive tables. For more information, see
  [Use cases for interactive tables](#label-interactive-when-should-i-use-them).

## Cost and billing considerations[¶](#cost-and-billing-considerations "Link to this heading")

Interactive warehouses incur compute charges when active. Currently, the minimum billable period for
an interactive warehouse is one minute. Starting later in 2025, the minimum billable period for
an interactive warehouse will be set to one hour, and at one-second granularity thereafter.

Note

If you resume an interactive warehouse that was paused, that operation results in a new minimum
billable period charge. That charge applies even if you were already being billed for that period
because of other recent activity in the warehouse. Therefore, avoid pausing and resuming an
interactive warehouse multiple times within a short period, for example to adjust the number of
clusters in a multi-cluster interactive warehouse.

Interactive tables incur standard storage costs. The price for storage of interactive tables is the
same as for standard tables. Interactive tables may be larger than equivalent standard tables, due to
differences in data encoding and additional indexes. The larger data size and indexes are factored into
the storage volume.

For more information about cost and billing for interactive warehouses and interactive tables, see the
[Snowflake service consumption table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

## Affected SQL statements[¶](#affected-sql-statements "Link to this heading")

This feature introduces changes to the following Snowflake SQL commands:

* [ALTER WAREHOUSE](../sql-reference/sql/alter-warehouse): new ADD TABLES and DROP TABLES clauses.
* [CREATE INTERACTIVE TABLE](../sql-reference/sql/create-interactive-table): creates interactive tables with required CLUSTER BY clause.
* [CREATE INTERACTIVE WAREHOUSE](../sql-reference/sql/create-interactive-warehouse): creates interactive warehouses with an
  optional TABLES clause.

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

1. [Overview of interactive warehouses and interactive tables](#overview-of-interactive-warehouses-and-interactive-tables)
2. [Use cases for interactive tables](#use-cases-for-interactive-tables)
3. [Region availability](#region-availability)
4. [Limitations of interactive warehouses and interactive tables](#limitations-of-interactive-warehouses-and-interactive-tables)
5. [Getting started with interactive tables](#getting-started-with-interactive-tables)
6. [Working with interactive tables and interactive warehouses](#working-with-interactive-tables-and-interactive-warehouses)
7. [Interactive Table Performance Considerations](#interactive-table-performance-considerations)
8. [Cost and billing considerations](#cost-and-billing-considerations)
9. [Affected SQL statements](#affected-sql-statements)