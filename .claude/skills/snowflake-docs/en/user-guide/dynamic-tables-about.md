---
auto_generated: true
description: Dynamic tables are tables that automatically refresh based on a defined
  query and target freshness, simplifying data transformation and pipeline management
  without requiring manual updates or custom s
last_scraped: '2026-01-14T16:54:14.289766+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/dynamic-tables-about
title: Dynamic tables | Snowflake Documentation
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

      * Key concepts

        * [Understanding target lag](dynamic-tables-target-lag.md)
        * [Understanding initialization and refresh](dynamic-tables-refresh.md)
        * [Using immutability constraints on dynamic tables](dynamic-tables-immutability-constraints.md)
        * [Understanding warehouse usage for dynamic tables](dynamic-tables-warehouses.md)
        * [Comparison with streams & tasks, and materialized views](dynamic-tables-comparison.md)
      * Dynamic table operations

        * [Creating dynamic tables](dynamic-tables-create.md)
        * [Creating dynamic Apache Iceberg™ tables](dynamic-tables-create-iceberg.md)
        * [Cloning dynamic tables](dynamic-tables-clone.md)
        * [Altering dynamic tables](dynamic-tables-alter.md)
        * [Dropping and undropping dynamic tables](dynamic-tables-drop-undrop.md)
        * [Suspending and resuming dynamic tables](dynamic-tables-suspend-resume.md)
        * [Manually refreshing dynamic tables](dynamic-tables-manual-refresh.md)
      * Monitoring and observability

        * [Monitor dynamic tables](dynamic-tables-monitor.md)
        * [Event table monitoring and alerts for dynamic tables](dynamic-tables-monitor-event-table-alerts.md)
      * [Data sharing with dynamic tables](dynamic-tables-data-sharing.md)
      * [Dynamic table access control](dynamic-tables-privileges.md)
      * [Cost considerations](dynamic-tables-cost.md)
      * Performance considerations

        * [Best practices for optimizing performance](dynamic-table-performance-guide.md)
        * [How operators incrementally refresh](dynamic-tables-performance-incremental-operators.md)
        * [Query performance](dynamic-tables-performance-queries.md)
        * [Refresh performance](dynamic-tables-performance-refresh.md)
      * Supported queries and limitations

        * [Supported queries](dynamic-tables-supported-queries.md)
        * [Limitations](dynamic-tables-limitations.md)
      * Troubleshooting

        * [Troubleshooting skipped, slow, or failed refreshes](dynamic-tables-troubleshoot-refresh.md)
        * [Diagnosing common refresh issues](dynamic-tables-troubleshooting.md)
        * [Debugging dynamic tables](dynamic-tables-debug.md)
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

[Guides](../guides/README.md)Data engineeringDynamic Tables

# Dynamic tables[¶](#dynamic-tables "Link to this heading")

Dynamic tables are tables that automatically refresh based on a defined query and target freshness, simplifying data transformation and
pipeline management without requiring manual updates or custom scheduling.

When you create a dynamic table, you define a query that specifies how data should be transformed from base objects. Snowflake handles the
refresh schedule of the dynamic table and updates the table automatically to reflect the changes made to the base objects based on the query.

## Key considerations and general best practices[¶](#key-considerations-and-general-best-practices "Link to this heading")

**Immutability constraints**: Use immutability constraints to let you control dynamic table updates. The constraints keep specific rows static
while enabling incremental updates to the rest of the table. They prevent unwanted changes to marked data while they let normal refreshes occur
for other parts of the table. For more information, see [Use immutability constraints on dynamic tables](dynamic-tables-immutability-constraints).

**Performance considerations:** Dynamic tables use incremental processing for workloads that support it, which can improve performance by
recomputing only the data that has changed, rather than performing a full refresh. For more information, see [Best practices for optimizing dynamic table performance](dynamic-table-performance-guide).

**Break down complex dynamic tables:** Break your pipeline into smaller, focused dynamic tables to improve performance and simplify
troubleshooting. For more information, see [Best practices for creating dynamic tables](dynamic-tables-create.html#label-best-practices-create).

## How dynamic tables work[¶](#how-dynamic-tables-work "Link to this heading")

Snowflake runs the definition query specified in your CREATE DYNAMIC TABLE statement and your dynamic tables are updated through an automated
refresh process.

The following diagram shows how this process computes the changes made to the base objects and merges them into the dynamic table by using
compute resources associated with the table.

![Visual representation of automated refresh process between base objects and dynamic tables](../_images/dynamic-tables.png)

### Target lag[¶](#target-lag "Link to this heading")

Use *target lag* to set how fresh you want your data to be. Usually, the table data freshness won’t be more than that far behind the base table
data freshness. With target lag, you control how often the table refreshes and how up-to-date the data stays.

For more information, see [Understanding dynamic table target lag](dynamic-tables-target-lag).

### Dynamic table refresh[¶](#dynamic-table-refresh "Link to this heading")

Dynamic tables aim to refresh within the target lag you specify. For example, a target lag of five minutes ensures that the data in the dynamic
table is no more than five minutes behind data updates to the base table. You set the refresh mode when you create the table and, afterward,
refreshes can happen on a schedule or manually.

For more information, see [Understanding dynamic table initialization and refresh](dynamic-tables-refresh) and [Manually refresh dynamic tables](dynamic-tables-manual-refresh).

## When to use dynamic tables[¶](#when-to-use-dynamic-tables "Link to this heading")

Dynamic tables are ideal for the following scenarios:

* You want to materialize query results without writing custom code.
* You want to avoid manually tracking data dependencies and managing refresh schedules. Dynamic tables enable you to define pipeline outcomes
  declaratively, without managing transformation steps manually.
* You want to chain together multiple tables for data transformations in a pipeline.
* You don’t need fine-grained control over refresh schedules, and you only need to specify a target freshness for the pipeline. Snowflake
  handles the orchestration of data refreshes, including scheduling and execution, based on your target freshness requirements.

### Example use cases[¶](#example-use-cases "Link to this heading")

* **Slowly changing dimensions (SCDs):** Dynamic tables can be used to implement Type 1 and Type 2 SCDs by reading from a change stream and
  using window functions over per-record keys ordered by a change timestamp. This method handles insertions, deletions, and updates that occur
  out of order, simplifying the creation of SCDs. For more information, see
  [Slowly Changing Dimensions with Dynamic Tables](https://medium.com/snowflake/slowly-changing-dimensions-with-dynamic-tables-d0d76582ff31).
* **Joins and aggregations:** You can use dynamic tables to incrementally precompute slow joins and aggregations to enable fast queries.
* **Batch to streaming transitions**: Dynamic tables support seamless transitions from batch to streaming with a single ALTER DYNAMIC TABLE
  command. You can control the refresh frequency in your pipeline to balance cost and data freshness.

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

1. [Key considerations and general best practices](#key-considerations-and-general-best-practices)
2. [How dynamic tables work](#how-dynamic-tables-work)
3. [When to use dynamic tables](#when-to-use-dynamic-tables)