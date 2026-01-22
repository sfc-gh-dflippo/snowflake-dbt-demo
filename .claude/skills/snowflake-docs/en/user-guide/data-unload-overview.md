---
auto_generated: true
description: Similar to data loading, Snowflake supports bulk export (i.e. unload)
  of data from a database table into flat, delimited text files.
last_scraped: '2026-01-14T16:57:46.984491+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/data-unload-overview
title: Overview of data unloading | Snowflake Documentation
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

[Guides](../guides/README.md)Data engineering[Data Unloading](../guides/overview-unloading-data.md)Overview

# Overview of data unloading[¶](#overview-of-data-unloading "Link to this heading")

Similar to data loading, Snowflake supports bulk export (i.e. unload) of data
from a database table into flat, delimited text files.

## Bulk unloading process[¶](#bulk-unloading-process "Link to this heading")

The process for unloading data into files is the same as the loading process, except in reverse:

Step 1:
:   Use the [COPY INTO <location>](../sql-reference/sql/copy-into-location) command to copy the data from the Snowflake database table into one or more files in a Snowflake or external stage.

Step 2:
:   Download the file from the stage:

    * From a Snowflake stage, use the [GET](../sql-reference/sql/get) command to download the data file(s).
    * From S3, use the interfaces/tools provided by Amazon S3 to get the data file(s).
    * From Azure, use the interfaces/tools provided by Microsoft Azure to get the data file(s).

## Bulk unloading using queries[¶](#bulk-unloading-using-queries "Link to this heading")

Snowflake supports specifying a SELECT statement instead of a table in the
[COPY INTO <location>](../sql-reference/sql/copy-into-location) command. The results of the query
are written to one or more files as specified in the command and the
file(s) are stored in the specified location (internal or external).

SELECT queries in COPY statements support the full syntax and semantics of Snowflake SQL queries, including JOIN clauses,
which enables downloading data from multiple tables.

## Bulk unloading into single or multiple files[¶](#bulk-unloading-into-single-or-multiple-files "Link to this heading")

The COPY INTO *<location>* command provides a copy option
(SINGLE) for unloading data into a single file or multiple files. The default
is SINGLE = FALSE (i.e. unload into multiple files).

Snowflake assigns each file a unique name. The location path specified for
the command can contain a filename prefix that is assigned to all the data files
generated. If a prefix is not specified, Snowflake prefixes the generated
filenames with `data_`.

Snowflake appends a suffix that ensures each file name is unique across
parallel execution threads; e.g. `data_stats_0_1_0`.

When unloading data into multiple files, use the MAX\_FILE\_SIZE copy option to
specify the maximum size of each file created.

## Partitioned data unloading[¶](#partitioned-data-unloading "Link to this heading")

The COPY INTO *<location>* command includes a PARTITION BY copy option for partitioned unloading of data to stages.

The ability to partition data during the unload operation enables a variety of use cases, such as using Snowflake to transform data for
output to a data lake. In addition, partitioning unloaded data into a directory structure in cloud storage can increase the efficiency with
which third-party tools consume the data.

The PARTITION BY copy option accepts an expression by which the unload operation partitions table rows into separate files unloaded to the
specified stage.

## Tasks for unloading data using the COPY command[¶](#tasks-for-unloading-data-using-the-copy-command "Link to this heading")

For more information about the tasks associated with unloading data, see:

* [Unloading into a Snowflake stage](data-unload-snowflake)
* [Unloading into Amazon S3](data-unload-s3)
* [Unloading into Google Cloud Storage](data-unload-gcs)
* [Unloading into Microsoft Azure](data-unload-azure)

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

1. [Bulk unloading process](#bulk-unloading-process)
2. [Bulk unloading using queries](#bulk-unloading-using-queries)
3. [Bulk unloading into single or multiple files](#bulk-unloading-into-single-or-multiple-files)
4. [Partitioned data unloading](#partitioned-data-unloading)
5. [Tasks for unloading data using the COPY command](#tasks-for-unloading-data-using-the-copy-command)

Related content

1. [Overview of data loading](/user-guide/data-load-overview)
2. [Data Manipulation Language (DML) commands](/user-guide/../sql-reference/sql-dml)