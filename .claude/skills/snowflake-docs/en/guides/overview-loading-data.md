---
auto_generated: true
description: Data can be loaded into Snowflake in a number of ways. The following
  topics provide an overview of data loading concepts, tasks, tools, and techniques
  to quick and easily load data into your Snowflake
last_scraped: '2026-01-14T16:54:17.019063+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/guides-overview-loading-data
title: Load data into Snowflake | Snowflake Documentation
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

      * [Overview](../user-guide/data-load-overview.md)
      * [Feature summary](../user-guide/intro-summary-loading.md)
      * [Considerations](../user-guide/data-load-considerations.md)
      * [Preparing to load data](../user-guide/data-load-prepare.md)
      * [Staging files using Snowsight](../user-guide/data-load-local-file-system-stage-ui.md)
      * [Loading data using the web interface](../user-guide/data-load-web-ui.md)
      * [Monitor data loading activity](../user-guide/data-load-monitor.md)
      * Bulk Loading
      * [Local File System](../user-guide/data-load-local-file-system.md)
      * [Amazon S3](../user-guide/data-load-s3.md)
      * [Google Cloud Storage](../user-guide/data-load-gcs.md)
      * [Microsoft Azure](../user-guide/data-load-azure.md)
      * [Troubleshooting](../user-guide/data-load-bulk-ts.md)
      * Snowpipe
      * [Overview](../user-guide/data-load-snowpipe-intro.md)
      * [Auto Ingest](../user-guide/data-load-snowpipe-auto.md)
      * [REST Endpoints](../user-guide/data-load-snowpipe-rest-overview.md)
      * [Error Notifications](../user-guide/data-load-snowpipe-errors.md)
      * [Troubleshooting](../user-guide/data-load-snowpipe-ts.md)
      * [Managing](../user-guide/data-load-snowpipe-manage.md)
      * [Monitoring Events for Snowpipe](../user-guide/data-load-snowpipe-monitor-events.md)
      * [Managing Snowpipe in Snowsight](../user-guide/data-load-snowpipe-snowsight.md)
      * [Snowpipe Costs](../user-guide/data-load-snowpipe-billing.md)
      * Snowpipe Streaming
      * [Overview](../user-guide/snowpipe-streaming/data-load-snowpipe-streaming-overview.md)
      * [High-performance Architecture](../user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-overview.md)
      * [Classic Architecture](../user-guide/snowpipe-streaming/snowpipe-streaming-classic-overview.md)
      * Semi-Structured Data
      * [Introduction](../user-guide/semistructured-intro.md)
      * [Supported Formats](../user-guide/semistructured-data-formats.md)
      * [Considerations](../user-guide/semistructured-considerations.md)
      * Unstructured Data
      * [Introduction](../user-guide/unstructured-intro.md)
      * [Directory Tables](../user-guide/data-load-dirtables.md)
      * [REST API](../user-guide/data-load-unstructured-rest-api.md)
      * [Processing with UDF and Procedure Handlers](../user-guide/unstructured-data-java.md)
      * [Sharing](../user-guide/unstructured-data-sharing.md)
      * [Troubleshooting](../user-guide/unstructured-ts.md)
      * [Loading Unstructured Data with Document AI](../user-guide/data-load-unstructured-data.md)
      * Accessing Data in Other Storage
      * [Amazon S3-compatible Storage](../user-guide/data-load-s3-compatible-storage.md)
      * Querying and Transforming Data
      * [Querying Data in Staged Files](../user-guide/querying-stage.md)
      * [Querying Metadata for Staged Files](../user-guide/querying-metadata.md)
      * [Transforming Data During Load](../user-guide/data-load-transform.md)
      * [Evolving Table Schema Automatically](../user-guide/data-load-schema-evolution.md)
      * Integrate Snowflake into external applications
      * Snowflake Connector for Microsoft Power Apps

        * [About the connector](../connectors/microsoft/powerapps/about.md)
        * [Tasks](../connectors/microsoft/powerapps/tasks.md)
      * Loading data from third-party systems
      * [Loading data using Native Applications](https://other-docs.snowflake.com/en/connectors "Loading data using Native Applications")
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

[Guides](README.md)Data engineeringData loading

# Load data into Snowflake[¶](#load-data-into-snowflake "Link to this heading")

Data can be loaded into Snowflake in a number of ways.
The following topics provide an overview of data loading concepts, tasks, tools, and techniques to quick and easily load data into your Snowflake database.

[Overview of data loading](user-guide/data-load-overview)
:   Options available to load data into Snowflake.

[Summary of data loading features](user-guide/intro-summary-loading)
:   Reference of the supported features for using the [COPY INTO <table>](sql-reference/sql/copy-into-table) command to load data from files.

[Data loading considerations](user-guide/data-load-considerations)
:   Best practices, general guidelines, and important considerations for bulk data loading.

[Working with Amazon S3-compatible storage](user-guide/data-load-s3-compatible-storage)
:   Instructions for accessing data in other storage.

[Load data using the web interface](user-guide/data-load-web-ui)
:   Instructions for loading limited amounts of data using the web interface.

[Introduction to Loading Semi-structured Data](user-guide/semistructured-intro)
:   Considerations for loading semi-structured data.

[Introduction to unstructured data](user-guide/unstructured-intro)
:   Considerations for loading unstructured data.

[Bulk loading from a local file system](user-guide/data-load-local-file-system)
:   Instructions for loading data in bulk using the COPY command.

[Snowpipe](user-guide/data-load-snowpipe-intro)
:   Instructions for loading data continuously using Snowpipe.

[Snowpipe Streaming](user-guide/snowpipe-streaming/data-load-snowpipe-streaming-overview)
:   Instructions for loading data streams continuously using Snowpipe Streaming.

[Transforming data during a load](user-guide/data-load-transform)
:   Instructions for transforming data while loading it into a table using the COPY INTO command.

[Querying Data in Staged Files](user-guide/querying-stage)
:   Instructions on using standard SQL to query internal and external named stages.

[Querying Metadata for Staged Files](user-guide/querying-metadata)
:   Instructions on querying metadata in internal and external stages.

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

1. [Snowflake Partner Connect](/user-guide/ecosystem-partner-connect)
2. [Overview of data unloading](/user-guide/data-unload-overview)
3. [Data Manipulation Language (DML) commands](/sql-reference/sql-dml)
4. [Load data into Apache Iceberg™ tables](/user-guide/tables-iceberg-load)