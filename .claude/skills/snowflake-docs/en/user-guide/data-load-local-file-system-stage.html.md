---
auto_generated: true
description: Execute PUT using the Snowflake CLI client, the SnowSQL client, or Drivers
  to upload (stage) local data files into an internal stage.
last_scraped: '2026-01-14T16:55:29.500870+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/data-load-local-file-system-stage.html
title: Staging data files from a local file system | Snowflake Documentation
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

[Guides](../guides/README.md)Data engineering[Data loading](../guides/overview-loading-data.md)[Local File System](data-load-local-file-system.md)Staging Files

# Staging data files from a local file system[¶](#staging-data-files-from-a-local-file-system "Link to this heading")

Execute [PUT](../sql-reference/sql/put) using the [Snowflake CLI](../developer-guide/snowflake-cli/index) client, the [SnowSQL client](snowsql), or [Drivers](../developer-guide/drivers) to upload (stage) local data files into an internal stage.

If you want to load a few small local data files into a named internal stage, you can also use Snowsight.
Refer to [Staging files using Snowsight](data-load-local-file-system-stage-ui).

## Staging the data files[¶](#staging-the-data-files "Link to this heading")

User Stage
:   The following example uploads a file named `data.csv` in the `/data` directory on your local machine to
    your user stage and prefixes the file with a folder named `staged`.

    Note that the `@~` character combination identifies a user stage.

    * Linux or macOS

      > ```
      > PUT file:///data/data.csv @~/staged;
      > ```
      >
      > Copy
    * Windows

      > ```
      > PUT file://C:\data\data.csv @~/staged;
      > ```
      >
      > Copy

Table Stage
:   The following example uploads a file named `data.csv` in the `/data` directory on your local machine to
    the stage for a table named `mytable`.

    Note that the `@%` character combination identifies a table stage.

    * Linux or macOS

      > ```
      > PUT file:///data/data.csv @%mytable;
      > ```
      >
      > Copy
    * Windows

      > ```
      > PUT file://C:\data\data.csv @%mytable;
      > ```
      >
      > Copy

Named Stage
:   The following example uploads a file named `data.csv` in the `/data` directory on your local machine to a
    named internal stage called `my_stage`. See [Choosing an internal stage for local files](data-load-local-file-system-create-stage) for information on named stages.

    In SQL, note that the `@` character by itself identifies a named stage.

    * Linux or macOS

      SQLPython

      ```
      PUT file:///data/data.csv @my_stage;
      ```

      Copy

      ```
      my_stage_res = root.databases["<database>"].schemas["<schema>"].stages["my_stage"]
      my_stage_res.put("/data/data.csv", "/")
      ```

      Copy
    * Windows

      SQLPython

      ```
      PUT file://C:\data\data.csv @my_stage;
      ```

      Copy

      ```
      my_stage_res = root.databases["<database>"].schemas["<schema>"].stages["my_stage"]
      my_stage_res.put("C:/data/data.csv", "/")
      ```

      Copy

## Listing staged data files[¶](#listing-staged-data-files "Link to this heading")

To see files that have been uploaded to a Snowflake stage, use the [LIST](../sql-reference/sql/list) command:

User stage:

```
LIST @~;
```

Copy

Table stage:

```
LIST @%mytable;
```

Copy

Named stage:

SQLPython

```
LIST @my_stage;
```

Copy

```
stage_files = root.databases["<database>"].schemas["<schema>"].stages["my_stage"].list_files()
for stage_file in stage_files:
  print(stage_file)
```

Copy

**Next:** [Copying data from an internal stage](data-load-local-file-system-copy)

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

1. [Staging the data files](#staging-the-data-files)
2. [Listing staged data files](#listing-staged-data-files)

Related content

1. [Preparing to load data](/user-guide/data-load-prepare)
2. [Choosing an internal stage for local files](/user-guide/data-load-local-file-system-create-stage)
3. [Copying data from an internal stage](/user-guide/data-load-local-file-system-copy)
4. [Managing stages with Python](/user-guide/../developer-guide/snowflake-python-api/snowflake-python-managing-data-loading#label-snowflake-python-stages)