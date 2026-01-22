---
auto_generated: true
description: The following topics help guide efforts to improve the performance of
  Snowflake.
last_scraped: '2026-01-14T16:54:16.140159+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/guides-overview-performance
title: Optimizing performance in Snowflake | Snowflake Documentation
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

    * [Exploring execution times](../user-guide/performance-query-exploring.md)
    * [Optimizing query performance](../user-guide/performance-query-options.md)
    * [Optimizing warehouses for performance](../user-guide/performance-query-warehouse.md)
    * [Optimizing storage for performance](../user-guide/performance-query-storage.md)
    * [Analyzing query workloads for performance](../user-guide/performance-explorer.md)
    * [Snowflake Optima](../user-guide/snowflake-optima.md)
33. [Cost & Billing](overview-cost.md)

[Guides](README.md)Performance optimization

# Optimizing performance in Snowflake[¶](#optimizing-performance-in-snowflake "Link to this heading")

The following topics help guide efforts to improve the performance of Snowflake.

[Exploring execution times](user-guide/performance-query-exploring)
:   Gain insights into the historical performance of queries using the web interface or by writing queries against data in the ACCOUNT\_USAGE
    schema.

[Optimizing query performance](user-guide/performance-query-options)
:   Learn about options for optimizing Snowflake query performance.

[Optimizing warehouses for performance](user-guide/performance-query-warehouse)
:   Learn about strategies to fine-tune computing power in order to improve the performance of a query or set of
    queries running on a warehouse, including enabling the Query Acceleration Service.

[Optimizing storage for performance](user-guide/performance-query-storage)
:   Learn how storing similar data together, creating optimized data structures, and defining specialized data sets can improve the
    performance of queries.

    Helpful when choosing between Automatic Clustering, Search Optimization Service, and materialized views.

[Analyzing query workloads with Performance Explorer](user-guide/performance-explorer)
:   Learn how to use Performance Explorer in Snowsight to monitor interactive metrics for SQL workloads.

[Snowflake Optima](user-guide/snowflake-optima)
:   Learn how Snowflake Optima continuously analyzes workload patterns and implements the most effective strategies automatically.

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

1. [Managing cost in Snowflake](/user-guide/cost-management-overview)