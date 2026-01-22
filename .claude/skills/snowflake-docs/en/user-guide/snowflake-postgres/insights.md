---
auto_generated: true
description: Preview Feature — Open
last_scraped: '2026-01-14T16:57:52.731052+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/snowflake-postgres/insights
title: Snowflake Postgres Insights | Snowflake Documentation
---

1. [Overview](../../guides/README.md)
2. [Snowflake Horizon Catalog](../snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../../guides/overview-connecting.md)
6. [Virtual warehouses](../warehouses.md)
7. [Databases, Tables, & Views](../../guides/overview-db.md)
8. [Data types](../../data-types.md)
10. Data Integration

    - [Snowflake Openflow](../data-integration/openflow/about.md)
    - Apache Iceberg™

      - [Apache Iceberg™ Tables](../tables-iceberg.md)
      - [Snowflake Open Catalog](../opencatalog/overview.md)
11. Data engineering

    - [Data loading](../../guides/overview-loading-data.md)
    - [Dynamic Tables](../dynamic-tables-about.md)
    - [Streams and Tasks](../data-pipelines-intro.md)
    - [dbt Projects on Snowflake](../data-engineering/dbt-projects-on-snowflake.md)
    - [Data Unloading](../../guides/overview-unloading-data.md)
12. [Storage Lifecycle Policies](../storage-management/storage-lifecycle-policies.md)
13. [Migrations](../../migrations/README.md)
15. [Queries](../../guides/overview-queries.md)
16. [Listings](../../collaboration/collaboration-listings-about.md)
17. [Collaboration](../../guides/overview-sharing.md)
19. [Snowflake AI & ML](../../guides/overview-ai-features.md)
21. [Snowflake Postgres](about.md)

    * [Creating instances](postgres-create-instance.md)
    * [Connecting](connecting-to-snowflakepg.md)
    * [Managing instances](managing-instances.md)
    * Monitoring
    * [Evaluate cost](postgres-cost.md)
    * [Insights](insights.md)
    * [Logging](postgres-logging.md)
    * Security and networking
    * [Networking](postgres-network.md)
    * [Tri-Secret Secure](postgres-tss.md)
    * Reference
    * [Instance sizes](postgres-instance-sizes.md)
    * [Extensions](postgres-extensions.md)
    * [Server settings](postgres-server-settings.md)
23. [Alerts & Notifications](../../guides/overview-alerts.md)
25. [Security](../../guides/overview-secure.md)
26. [Data Governance](../../guides/overview-govern.md)
27. [Privacy](../../guides/overview-privacy.md)
29. [Organizations & Accounts](../../guides/overview-manage.md)
30. [Business continuity & data recovery](../replication-intro.md)
32. [Performance optimization](../../guides/overview-performance.md)
33. [Cost & Billing](../../guides/overview-cost.md)

[Guides](../../guides/README.md)[Snowflake Postgres](about.md)Insights

# Snowflake Postgres Insights[¶](#snowflake-postgres-insights "Link to this heading")

[![Snowflake logo in black (no text)](../../_images/logo-snowflake-black.png)](../../_images/logo-snowflake-black.png) [Preview Feature](../../release-notes/preview-features) — Open

Available to all accounts.

The database insights available on each Snowflake Postgres instance’s Snowsight details page provide point in time insights into your database along with recommendations on actions you can take to improve performance.

To view an instance’s insights:

1. In the navigation menu, select Postgres
2. Select your instance from the list of instance’s shown to load its details page.
3. Choose the insight to view with the Insight select box shown just under the Details tab heading.

The available insights are:

* Cache and index hit rates
* Unused indexes
* Bloat
* Outlier queries
* Long running queries
* Vacuum statistics
* Table sizes
* Connections

## Cache hit[¶](#cache-hit "Link to this heading")

Postgres generally tries to keep the data you access most often in its shared buffers cache. The cache hit ratio measures how many content requests the buffer cache is able to handle compared to how many requests it receives. A cache hit is a request that is successfully handled and a miss is one that is not. A miss will go beyond the cache to the file system to fulfill the request.

So if you have 100 cache hits and 2 misses, you’ll have a cache hit ratio of 100/102 which equals 98%.

For normal operations of Postgres and performance, you’ll want to have your Postgres cache hit ratio about 99%.

If you see your cache hit ratio below that, you may need to look at moving to an instance with larger memory.

## Index hit[¶](#index-hit "Link to this heading")

Adding indexes to your database is critical to query and application performance. Indexes are particularly valuable across large tables.

The index hit rate is measured as a ratio or percentage of the total number of queries or query executions that successfully utilize an index versus the total number of queries executed. A higher index hit rate suggests better index utilization and overall query performance.

In general, you are looking for 99%+ on tables larger than 10,000 rows. If you see a table larger than 10,000 with no or low index usage, that’s your best bet on where to start with adding an index.

## Unused indexes[¶](#unused-indexes "Link to this heading")

Unused indexes in PostgreSQL refer to indexes that are created on tables but are not actively used. These indexes consume disk space, require maintenance, and can negatively affect the performance.

Here are a few reasons why you should care about unused indexes in Postgres:

* Storage and disk space: Unused indexes occupy disk space that could be better utilized for other purposes. This can result in increased storage costs and reduce the available space for other database objects.
* Performance impact: Indexes incur overhead during data modification operations, such as inserts, updates, and deletes. When there are many unused indexes, these operations take longer because the database must update multiple indexes in addition to the table.
* Slower query execution: Postgres’ query optimizer considers all available indexes when generating an execution plan for a query. If there are unused indexes, the optimizer may spend additional time considering these indexes, leading to suboptimal query plans and slower query execution.
* Maintenance overhead: Maintaining indexes requires resources, including CPU and disk I/O. If you have a large number of unused indexes, these resources are wasted on unnecessary index maintenance tasks.

Important

Note that you might have indexes that are not used on a primary instance but are used on a replica.

## Bloat[¶](#bloat "Link to this heading")

Bloat refers to the accumulation of dead and unused rows in a database, resulting in disk space consumption and performance degradation. It primarily affects databases with high transaction workloads. Postgres’ MVCC system creates multiple versions of a row to handle concurrent transactions. When a row is updated or deleted, a new version is created, while the old version is marked as dead. These dead rows are not immediately removed from the table to preserve transactional integrity and ensure data consistency during concurrent operations.

To reclaim the disk space occupied by dead rows, Postgres periodically performs vacuuming. This process identifies and eliminates dead rows from the table, freeing up the disk space for reuse. Bloat occurs when high transactions generate a substantial number of dead rows between vacuum processes.

We provide a percentage of bloat to show the amount of space taken up by dead rows compared to the total size of the table or index. The bloat displayed is an estimate or approximation. If you need a more data on bloat in your tables, you can use the extension [pgstattuple](https://www.postgresql.org/docs/current/pgstattuple.html), though this can be a resource intensive operation.

**Low Bloat**: Bloat below 50% is generally considered acceptable and does not normally require action. It is still recommended to monitor bloat for further growth and check vacuum configurations and settings.

**High Bloat**: Bloat above 50% suggests a high level of bloat that can begin to severely impact performance and disk space utilization. You may need to consider action, such as performing a manual vacuum operation, or changing vacuum settings, if you notice slow queries or performance issues.

We do not display a bloat percentage for tables under 1GB or with a bloat percentage less than 10%.

## Outlier queries[¶](#outlier-queries "Link to this heading")

These are the queries with the highest proportional execution time. This may
include very slow but relatively infrequent queries, as well as slightly slow
but extremely common queries. The queries with the highest proportional
execution time are the best starting point for database query tuning at the
application level or indexing.

## Long running queries[¶](#long-running-queries "Link to this heading")

Long-running queries in PostgreSQL can have several negative implications for
your database and application. Here are some reasons why long-running queries
are generally considered undesirable:

* Performance impact: Long-running queries tie up database resources, including
  CPU, memory, and disk I/O, for an extended period.
* Increased contention: Long-running queries can lead to increased contention
  for shared resources, such as locks and concurrent access to database objects.
* Reduced throughput: When a query takes a long time to complete, it can limit
  the number of queries that can be executed within a given timeframe.
* Poor user experience: If your application relies on timely query execution,
  long-running queries can negatively impact user experience. Users may
  experience delays or unresponsiveness, leading to frustration and
  dissatisfaction with your application.
* Resource exhaustion: Long-running queries can consume excessive memory,
  leading to increased memory usage and potential out-of-memory errors. They can
  also generate large temporary files on disk, potentially causing disk space
  issues.

## Vacuum[¶](#vacuum "Link to this heading")

The insights panel also includes vacuum statistics. You can check on the table names, the last vacuum and last autovacuum. You can also get insights on how many dead rows exist, when vacuum last cleaned up dead rows, and more.

Vacuum statistics include:

* Table name
* Last vacuum: last time a manual vacuum operation was run
* Last autovacuum: last time autovacuum ran
* Row count: total row count for the table
* Dead row count: number of un-vacuumed / dead rows in the table presently
* Scale factor: the current scale factor set in the autovacuum settings
* Threshold: the total number of rows, using the scale factor, that would require a vacuum operation
* Should vacuum: if you should manually vacuum the table

## Table sizes[¶](#table-sizes "Link to this heading")

Details about your Postgres table sizes is available under Table Sizes in instance insights. This shows table information like:

* table names
* approximate row counts
* total table size
* size of indexes on the table
* number of table bytes in TOAST tables
* raw row table size

## Connections[¶](#connections "Link to this heading")

The connections insight displays all currently active and idle connections in the database instance. Active connections are in a session that is currently connected to the database and is executing a query or waiting to execute one.

Idle connections are common and they aren’t inherently a problem, but they can become an issue depending on your workload and configuration. Idle connections consume memory, so a large number of them can lead to excessive memory usage. High idle connections is typically an indication that the database would benefit from connection pooling.

Each running session has a `pid` which is the process id - a unique identifier assigned to each active backend connection.

To cancel a connection, query, or process but leave the session open use this statement:

```
SELECT pg_cancel_backend(<pid>);
```

Copy

A more forceful action, which will close the connection and roll back any transactions, is:

```
SELECT pg_terminate_backend(<pid>);
```

Copy

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

1. [Cache hit](#cache-hit)
2. [Index hit](#index-hit)
3. [Unused indexes](#unused-indexes)
4. [Bloat](#bloat)
5. [Outlier queries](#outlier-queries)
6. [Long running queries](#long-running-queries)
7. [Vacuum](#vacuum)
8. [Table sizes](#table-sizes)
9. [Connections](#connections)