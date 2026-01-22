---
auto_generated: true
description: This topic provides an overview of supported data file formats for unloading
  data.
last_scraped: '2026-01-14T16:57:46.651025+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/data-unload-prepare
title: Preparing to unload data | Snowflake Documentation
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
    - [dbt Projects on Snowflake](data-engineering/dbt-projects-on-snowflake.md)
    - [Data Unloading](../guides/overview-unloading-data.md)

      * [Overview](data-unload-overview.md)
      * [Features](intro-summary-unloading.md)
      * [Considerations](data-unload-considerations.md)
      * [Preparing to Unload Data](data-unload-prepare.md)
      * [Unloading into a Snowflake Stage](data-unload-snowflake.md)
      * [Unloading into Amazon S3](data-unload-s3.md)
      * [Unloading into Google Cloud Storage](data-unload-gcs.md)
      * [Unloading into Microsoft Azure](data-unload-azure.md)
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

[Guides](../guides/README.md)Data engineering[Data Unloading](../guides/overview-unloading-data.md)Preparing to Unload Data

# Preparing to unload data[¶](#preparing-to-unload-data "Link to this heading")

This topic provides an overview of supported data file formats for unloading data.

## Supported file formats[¶](#supported-file-formats "Link to this heading")

The following file formats are supported:

> | Structured/Semi-structured | Type | Notes |
> | --- | --- | --- |
> | Structured | Delimited (CSV, TSV, etc.) | Any valid singlebyte delimiter is supported; default is comma (i.e. CSV). |
> | Semi-structured | JSON, Parquet |  |

File format options specify the type of data contained in a file, as well as other related characteristics about the format of the data. The file format options you can specify are different depending on the type of data you are unloading to. Snowflake provides a full set of file format option defaults.

### Semi-structured data[¶](#semi-structured-data "Link to this heading")

When unloading to JSON files, Snowflake outputs to the [NDJSON](https://github.com/ndjson/ndjson-spec) (newline delimited JSON) standard format.

## Specifying file format options[¶](#specifying-file-format-options "Link to this heading")

Individual file format options can be specified in any of the following places:

* In the definition of a table.
* In the definition of a named stage. For more information, see [CREATE STAGE](../sql-reference/sql/create-stage).
* Directly in a [COPY INTO <location>](../sql-reference/sql/copy-into-location) command when unloading data.

In addition, to simplify data unloading, Snowflake supports creating named file formats, which are database objects that encapsulate all of the required
format information. Named file formats can then be used as input in all the same places where you can specify individual file format options, thereby
helping to streamline the data unloading process for similarly-formatted data.

Named file formats are optional, but are recommended when you plan to regularly unload similarly-formatted data.

### Creating a named file format[¶](#creating-a-named-file-format "Link to this heading")

You can create a file format using either the web interface or SQL:

> Snowsight:
> :   In the navigation menu, select Catalog » Database Explorer. Then select the *<db\_name>* » File Formats.
>
> SQL:
> :   [CREATE FILE FORMAT](../sql-reference/sql/create-file-format)

For detailed descriptions of all the file format options, see [CREATE FILE FORMAT](../sql-reference/sql/create-file-format).

#### Examples[¶](#examples "Link to this heading")

The following example creates a named CSV file format with a specified field delimiter:

> ```
> CREATE OR REPLACE FILE FORMAT my_csv_unload_format
>   TYPE = 'CSV'
>   FIELD_DELIMITER = '|';
> ```
>
> Copy

The following example creates a named JSON file format:

> ```
> CREATE OR REPLACE FILE FORMAT my_json_unload_format
>   TYPE = 'JSON';
> ```
>
> Copy

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

1. [Supported file formats](#supported-file-formats)
2. [Specifying file format options](#specifying-file-format-options)

Related content

1. [Unloading into a Snowflake stage](/user-guide/data-unload-snowflake)
2. [Unloading into Amazon S3](/user-guide/data-unload-s3)