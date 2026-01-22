---
auto_generated: true
description: 'Snowflake supports continuous data pipelines with Streams and Tasks:'
last_scraped: '2026-01-14T16:54:17.229943+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/data-pipelines-intro
title: Introduction to Streams and Tasks | Snowflake Documentation
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

      * [Streams](streams-intro.md)
      * [Tasks](tasks-intro.md)
      * [Data Pipeline Examples](data-pipelines-examples.md)
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

[Guides](../guides/README.md)Data engineeringStreams and Tasks

# Introduction to Streams and Tasks[¶](#introduction-to-streams-and-tasks "Link to this heading")

Snowflake supports continuous data pipelines with Streams and Tasks:

Streams:
:   A *stream* object records the delta of change data capture (CDC) information for a table (such as a staging table), including inserts and other data manipulation language (DML) changes. A stream allows querying and consuming a set of changes to a table, at the row level, between two transactional points of time.

    In a continuous data pipeline, table streams record when staging tables and any downstream tables are populated with data from business applications using continuous data loading and are ready for further processing using SQL statements.

    For more information, see [Introduction to Streams](streams-intro).

Tasks:
:   A *task* object runs a SQL statement, which can include calls to stored procedures. Tasks can run on a schedule or based on a trigger that you define, such as the arrival of data. You can use task graphs to chain tasks together, definining directed acyclic graphs (DAGs) to support more complex periodic processing. For more information, see [Introduction to tasks](tasks-intro) and [Create a sequence of tasks with a task graph](tasks-graphs).

    Combining tasks with table streams is a convenient and powerful way to continuously process new or changed data. A task can transform new or changed rows that a stream surfaces using [SYSTEM$STREAM\_HAS\_DATA](../sql-reference/functions/system_stream_has_data). Each time a task runs, it can either consume the change data or skip the current run if no change data exists.

For other continuous data pipeline features, see:

* Continuous data loading with [Snowpipe](data-load-snowpipe-intro), [Snowpipe Streaming](snowpipe-streaming/data-load-snowpipe-streaming-overview), or [Snowflake Connector for Kafka](kafka-connector).
* Continuous data transformation with [Dynamic tables](dynamic-tables-about).

Was this page helpful?

YesNo

[Visit Snowflake](https://www.snowflake.com)

[Join the conversation](https://community.snowflake.com/s/)

[Develop with Snowflake](https://developers.snowflake.com)

[Share your feedback](/feedback)

[Read the latest on our blog](https://www.snowflake.com/blog/)

[Get your own certification](https://learn.snowflake.com)

[Privacy Notice](https://www.snowflake.com/privacy-policy/)[Site Terms](https://www.snowflake.com/legal/snowflake-site-terms/)Cookies Settings© 2026 Snowflake, Inc. All Rights Reserved.