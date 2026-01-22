---
auto_generated: true
description: Snowflake supports bulk unloading of data from a database table into
  flat, delimited text files. The following topics detail the processes and procedures
  associated with unloading data.
last_scraped: '2026-01-14T16:54:18.022836+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/guides-overview-unloading-data
title: Unload Data from Snowflake | Snowflake Documentation
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

      * [Overview](../user-guide/data-unload-overview.md)
      * [Features](../user-guide/intro-summary-unloading.md)
      * [Considerations](../user-guide/data-unload-considerations.md)
      * [Preparing to Unload Data](../user-guide/data-unload-prepare.md)
      * [Unloading into a Snowflake Stage](../user-guide/data-unload-snowflake.md)
      * [Unloading into Amazon S3](../user-guide/data-unload-s3.md)
      * [Unloading into Google Cloud Storage](../user-guide/data-unload-gcs.md)
      * [Unloading into Microsoft Azure](../user-guide/data-unload-azure.md)
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

[Guides](README.md)Data engineeringData Unloading

# Unload Data from Snowflake[¶](#unload-data-from-snowflake "Link to this heading")

Snowflake supports bulk unloading of data from a database table into flat, delimited text files.
The following topics detail the processes and procedures associated with unloading data.

[Overview of data unloading](user-guide/data-unload-overview)
:   Introduction and overview of unloading data.

[Summary of Data Unloading Features](user-guide/intro-summary-unloading)
:   Reference of the supported features for using the [COPY INTO <location>](sql-reference/sql/copy-into-location) command to unload data from Snowflake tables into flat files.

[Data unloading considerations](user-guide/data-unload-considerations)
:   Best practices, general guidelines, and important considerations for unloading data.

[Preparing to unload data](user-guide/data-unload-prepare)
:   Supported data file formats for unloading data.

[Unloading into a Snowflake stage](user-guide/data-unload-snowflake)
:   Instructions on using the COPY command to unload data from a table into an internal (i.e. Snowflake) stage.

[Unloading into Amazon S3](user-guide/data-unload-s3)
:   Instructions on using the COPY command to unload data from a table into an Amazon S3 bucket.

[Unloading into Google Cloud Storage](user-guide/data-unload-gcs)
:   Instructions on using the COPY command to unload data from a table into an Google Cloud Storage bucket.

[Unloading into Microsoft Azure](user-guide/data-unload-azure)
:   Instructions on using the COPY command to unload data from a table into an Azure container.

Was this page helpful?

YesNo

[Visit Snowflake](https://www.snowflake.com)

[Join the conversation](https://community.snowflake.com/s/)

[Develop with Snowflake](https://developers.snowflake.com)

[Share your feedback](/feedback)

[Read the latest on our blog](https://www.snowflake.com/blog/)

[Get your own certification](https://learn.snowflake.com)

[Privacy Notice](https://www.snowflake.com/privacy-policy/)[Site Terms](https://www.snowflake.com/legal/snowflake-site-terms/)Cookies Settings© 2026 Snowflake, Inc. All Rights Reserved.