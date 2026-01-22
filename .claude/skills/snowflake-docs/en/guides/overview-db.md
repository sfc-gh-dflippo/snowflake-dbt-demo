---
auto_generated: true
description: All data in Snowflake is maintained in databases. Each database consists
  of one or more schemas, which are logical groupings of database objects, such as
  tables and views. Snowflake does not place any
last_scraped: '2026-01-14T16:54:23.810894+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/guides-overview-db
title: Databases, Tables and Views - Overview | Snowflake Documentation
---

1. [Overview](README.md)
2. [Snowflake Horizon Catalog](../user-guide/snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](overview-connecting.md)
6. [Virtual warehouses](../user-guide/warehouses.md)
7. [Databases, Tables, & Views](overview-db.md)

   * [Table Structures](../user-guide/tables-micro-partitions.md)
   * [Temporary And Transient Tables](../user-guide/tables-temp-transient.md)
   * [External Tables](../user-guide/tables-external-intro.md)
   * [Hybrid Tables](../user-guide/tables-hybrid.md)
   * [Interactive tables](../user-guide/interactive.md)
   * [Working with tables in Snowsight](../user-guide/ui-snowsight-data-databases-table.md)
   * [Search optimization service](../user-guide/search-optimization-service.md)
   * Views
   * [Views](../user-guide/views-introduction.md)
   * [Secure Views](../user-guide/views-secure.md)
   * [Materialized Views](../user-guide/views-materialized.md)
   * [Semantic Views](../user-guide/views-semantic/overview.md)
   * [Working with Views in Snowsight](../user-guide/ui-snowsight-data-databases-view.md)
   * Considerations
   * [Views, Materialized Views, and Dynamic Tables](../user-guide/overview-view-mview-dts.md)
   * [Table Design](../user-guide/table-considerations.md)
   * [Cloning](../user-guide/object-clone.md)
   * [Data Storage](../user-guide/tables-storage-considerations.md)
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
33. [Cost & Billing](overview-cost.md)

[Guides](README.md)Databases, Tables, & Views

# Databases, Tables and Views - Overview[¶](#databases-tables-and-views-overview "Link to this heading")

All data in Snowflake is maintained in databases. Each database consists of one or more schemas, which are logical groupings of database objects,
such as tables and views. Snowflake does not place any hard limits on the number of databases, schemas (within a database), or objects (within
a schema) you can create.

Use the following pages to learn about tables and table types, views, design considerations and other related content.

[Understanding Snowflake Table Structures](user-guide/tables-micro-partitions)
:   Introduction to *micro-partitions* and *data clustering*, two of the principal concepts utilized in Snowflake physical table structures.

[Temporary and Transient Tables](user-guide/tables-temp-transient)
:   Snowflake supports creating temporary tables for storing non-permanent, transitory data such as ETL data, session-specific
    or other short lived data.

[External Tables](user-guide/tables-external-intro)
:   Snowflake supports the concept of an external table. External tables are read-only, and their files are stored in an external stage.

[Hybrid Tables](user-guide/tables-hybrid)
:   Snowflake supports the concept of a hybrid table. Hybrid tables provide
    optimized performance for read and write operations in transactional and
    hybrid workloads.

[Apache Iceberg™ tables](user-guide/tables-iceberg)
:   Snowflake supports the Apache Iceberg™ open table format. Iceberg tables use data in external cloud
    storage and give you the option to use Snowflake as the Iceberg catalog, an external Iceberg catalog, or to create a table
    from files in object storage.

[Views](user-guide/views-introduction)
:   A view allows the result of a query to be accessed as if it were a table.
    Views serve a variety of purposes, including combining, segregating, and protecting data.

[Secure Views](user-guide/views-secure)
:   Snowflake supports the concept of a secure view. Secure views are specifically designed for data privacy.
    For example to limit access to sensitive data that should not be exposed to all users of the underlying table(s).

[Materialized Views](user-guide/views-materialized)
:   Materialized views are views precomputed from data derived from a query specification and stored for later use.
    Querying a materialized view is faster than executing a query against the base table of the view because the data is pre-computed.

[Table Design Best Practices](user-guide/table-considerations)
:   Best practices, general guidelines, and important considerations when designing and managing tables.

[Cloning Best Practices](user-guide/object-clone)
:   Best practices, general guidelines, and important considerations when cloning objects in Snowflake, particularly databases, schemas,
    and permanent tables.

[Data storage considerations](user-guide/tables-storage-considerations)
:   Best practices and guidelines for controlling data storage costs associated with Continuous Data Protection (CDP), particularly for tables.

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

1. [Data Definition Language (DDL) commands](/sql-reference/sql-ddl-summary)
2. [Managing Snowflake databases, schemas, tables, and views with Python](/developer-guide/snowflake-python-api/snowflake-python-managing-databases)