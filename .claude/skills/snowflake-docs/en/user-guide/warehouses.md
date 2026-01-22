---
auto_generated: true
description: 'A virtual warehouse, often referred to simply as a “warehouse”, is a
  cluster of compute resources in Snowflake. A virtual warehouse is available in two
  types:'
last_scraped: '2026-01-14T16:54:13.231334+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/warehouses
title: Virtual warehouses | Snowflake Documentation
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

[Guides](../guides/README.md)Virtual warehouses

# Virtual warehouses[¶](#virtual-warehouses "Link to this heading")

A virtual warehouse, often referred to simply as a “warehouse”, is a cluster of compute resources in Snowflake. A virtual warehouse is
available in two types:

* Standard
* Snowpark-optimized

A warehouse provides the required resources, such as CPU, memory, and temporary storage, to
perform the following operations in a Snowflake session:

* Executing SQL [SELECT](../sql-reference/sql/select) statements that require compute resources (for example, retrieving rows from tables and views).
* Performing DML operations, such as:

  + Updating rows in tables ([DELETE](../sql-reference/sql/delete) , [INSERT](../sql-reference/sql/insert) , [UPDATE](../sql-reference/sql/update)).
  + Loading data into tables ([COPY INTO <table>](../sql-reference/sql/copy-into-table)).
  + Unloading data from tables ([COPY INTO <location>](../sql-reference/sql/copy-into-location)).

Note

To perform these operations, a warehouse must be running and in use for the session. While a warehouse is running, it consumes Snowflake
credits.

[Overview of warehouses](warehouses-overview)
:   Warehouses are required for queries, as well as all DML operations, including loading data into tables.
    In addition to being defined by its type as either Standard or Snowpark-optimized, a warehouse is defined by its size,
    as well as the other properties that can be set to help control and automate warehouse activity.

[Snowpark-optimized warehouses](warehouses-snowpark-optimized)
:   Snowpark workloads can be run on both Standard and Snowpark-optimized warehouses. Snowpark-optimized warehouses are recommended for workloads that have large memory requirements such as ML training use cases

[Warehouse considerations](warehouses-considerations)
:   Best practices and general guidelines for using virtual warehouses in Snowflake to process queries

[Multi-cluster warehouses](warehouses-multicluster)
:   Multi-cluster warehouses enable you to scale compute resources to manage your user and query concurrency needs as they change, such as during peak and off hours.

[Working with warehouses](warehouses-tasks)
:   Learn how to create, stop, start and otherwise manage Snowflake warehouses.

[Using the Query Acceleration Service (QAS)](query-acceleration-service)
:   The query acceleration service can accelerate parts of the query workload in a warehouse.
    When enabled for a warehouse, query acceleration can improve overall warehouse performance by reducing the impact of outlier queries
    (i.e. queries which use more resources then typical queries).

[Monitoring warehouse load](warehouses-load-monitoring)
:   Warehouse query load measures the average number of queries that were running or queued within a specific interval.

* [Overview of warehouses](warehouses-overview)
* [Snowpark-optimized warehouses](warehouses-snowpark-optimized)
* [Warehouse considerations](warehouses-considerations)
* [Multi-cluster warehouses](warehouses-multicluster)
* [Working with warehouses](warehouses-tasks)
* [Using the Query Acceleration Service (QAS)](query-acceleration-service)
* [Monitoring warehouse load](warehouses-load-monitoring)

Was this page helpful?

YesNo

[Visit Snowflake](https://www.snowflake.com)

[Join the conversation](https://community.snowflake.com/s/)

[Develop with Snowflake](https://developers.snowflake.com)

[Share your feedback](/feedback)

[Read the latest on our blog](https://www.snowflake.com/blog/)

[Get your own certification](https://learn.snowflake.com)

[Privacy Notice](https://www.snowflake.com/privacy-policy/)[Site Terms](https://www.snowflake.com/legal/snowflake-site-terms/)Cookies Settings© 2026 Snowflake, Inc. All Rights Reserved.

Related content

1. [Understanding compute cost](/user-guide/cost-understanding-compute)
2. [Working with resource monitors](/user-guide/resource-monitors)