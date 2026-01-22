---
auto_generated: true
description: 'This set of topics describes how to use the COPY command to bulk load
  data from a local file system into tables using an internal (i.e. Snowflake-managed)
  stage. For instructions on loading data from '
last_scraped: '2026-01-14T16:57:45.771907+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/data-load-local-file-system
title: Bulk loading from a local file system | Snowflake Documentation
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

      * [Overview](data-load-overview.md)
      * [Feature summary](intro-summary-loading.md)
      * [Considerations](data-load-considerations.md)
      * [Preparing to load data](data-load-prepare.md)
      * [Staging files using Snowsight](data-load-local-file-system-stage-ui.md)
      * [Loading data using the web interface](data-load-web-ui.md)
      * [Monitor data loading activity](data-load-monitor.md)
      * Bulk Loading
      * [Local File System](data-load-local-file-system.md)

        + [Choosing an Internal Stage](data-load-local-file-system-create-stage.md)
        + [Staging Files](data-load-local-file-system-stage.md)
        + [Copying Data from a Local File System](data-load-local-file-system-copy.md)
      * [Amazon S3](data-load-s3.md)
      * [Google Cloud Storage](data-load-gcs.md)
      * [Microsoft Azure](data-load-azure.md)
      * [Troubleshooting](data-load-bulk-ts.md)
      * Snowpipe
      * [Overview](data-load-snowpipe-intro.md)
      * [Auto Ingest](data-load-snowpipe-auto.md)
      * [REST Endpoints](data-load-snowpipe-rest-overview.md)
      * [Error Notifications](data-load-snowpipe-errors.md)
      * [Troubleshooting](data-load-snowpipe-ts.md)
      * [Managing](data-load-snowpipe-manage.md)
      * [Monitoring Events for Snowpipe](data-load-snowpipe-monitor-events.md)
      * [Managing Snowpipe in Snowsight](data-load-snowpipe-snowsight.md)
      * [Snowpipe Costs](data-load-snowpipe-billing.md)
      * Snowpipe Streaming
      * [Overview](snowpipe-streaming/data-load-snowpipe-streaming-overview.md)
      * [High-performance Architecture](snowpipe-streaming/snowpipe-streaming-high-performance-overview.md)
      * [Classic Architecture](snowpipe-streaming/snowpipe-streaming-classic-overview.md)
      * Semi-Structured Data
      * [Introduction](semistructured-intro.md)
      * [Supported Formats](semistructured-data-formats.md)
      * [Considerations](semistructured-considerations.md)
      * Unstructured Data
      * [Introduction](unstructured-intro.md)
      * [Directory Tables](data-load-dirtables.md)
      * [REST API](data-load-unstructured-rest-api.md)
      * [Processing with UDF and Procedure Handlers](unstructured-data-java.md)
      * [Sharing](unstructured-data-sharing.md)
      * [Troubleshooting](unstructured-ts.md)
      * [Loading Unstructured Data with Document AI](data-load-unstructured-data.md)
      * Accessing Data in Other Storage
      * [Amazon S3-compatible Storage](data-load-s3-compatible-storage.md)
      * Querying and Transforming Data
      * [Querying Data in Staged Files](querying-stage.md)
      * [Querying Metadata for Staged Files](querying-metadata.md)
      * [Transforming Data During Load](data-load-transform.md)
      * [Evolving Table Schema Automatically](data-load-schema-evolution.md)
      * Integrate Snowflake into external applications
      * Snowflake Connector for Microsoft Power Apps

        * [About the connector](../connectors/microsoft/powerapps/about.md)
        * [Tasks](../connectors/microsoft/powerapps/tasks.md)
      * Loading data from third-party systems
      * [Loading data using Native Applications](https://other-docs.snowflake.com/en/connectors "Loading data using Native Applications")
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

[Guides](../guides/README.md)Data engineering[Data loading](../guides/overview-loading-data.md)Local File System

# Bulk loading from a local file system[¶](#bulk-loading-from-a-local-file-system "Link to this heading")

This set of topics describes how to use the COPY command to bulk load data from a local file system into tables using an internal (i.e.
Snowflake-managed) stage. For instructions on loading data from a cloud storage location that you manage, refer to [Bulk loading from Amazon S3](data-load-s3), [Bulk loading from Google Cloud Storage](data-load-gcs), or [Bulk loading from Microsoft Azure](data-load-azure).

As illustrated in the diagram below, loading data from a local file system is performed in two, separate steps:

Step 1:
:   Upload (i.e. stage) one or more data files to a Snowflake stage (named internal stage or table/user stage) using the [PUT](../sql-reference/sql/put) command.

Step 2:
:   Use the [COPY INTO <table>](../sql-reference/sql/copy-into-table) command to load the contents of the staged file(s) into a Snowflake database table.

    Regardless of the stage you use, this step requires a running virtual warehouse that is also the current (i.e. in use) warehouse for the session. The warehouse provides the compute resources to
    perform the actual insertion of rows into the table.

![Data loading overview](../_images/data-load-bulk-file-system.png)

Tip

The instructions in this set of topics assume you have read [Preparing to load data](data-load-prepare) and have created a named file format, if desired.

Before you begin, you may also want to read [Data loading considerations](data-load-considerations) for best practices, tips, and other guidance.

**Next Topics:**

* **Configuration tasks (complete as needed):**

  + [Choosing an internal stage for local files](data-load-local-file-system-create-stage)
* **Data loading tasks (complete for each set of files you load):**

  + [Staging data files from a local file system](data-load-local-file-system-stage)
  + [Copying data from an internal stage](data-load-local-file-system-copy)

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

1. [Unloading into a Snowflake stage](/user-guide/data-unload-snowflake)