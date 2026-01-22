---
auto_generated: true
description: Apache Iceberg™ tables for Snowflake combine the performance and query
  semantics of typical Snowflake tables with external cloud storage that you manage.
  They are ideal for existing data lakes that yo
last_scraped: '2026-01-14T16:54:15.091213+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/tables-iceberg
title: Apache Iceberg™ tables | Snowflake Documentation
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

        * [Storage](tables-iceberg-storage.md)
        * [Metadata And Retention](tables-iceberg-metadata.md)
        * [Transactions](tables-iceberg-transactions.md)
        * [Data Types](tables-iceberg-data-types.md)
        * Tutorials
        * [Tutorial: Create Your First Apache Iceberg™ Table](tutorials/create-your-first-iceberg-table.md)
        * [Tutorial: Set Up Bidirectional Access to Unity Catalog](tutorials/tables-iceberg-set-up-bidirectional-access-to-unity-catalog.md)
        * Work With Apache Iceberg™ Tables
        * [Best Practices](tables-iceberg-best-practices.md)
        * [Configure An External Volume](tables-iceberg-configure-external-volume.md)
        * [Configure A Catalog Integration](tables-iceberg-configure-catalog-integration.md)
        * [Automated Refresh](tables-iceberg-auto-refresh.md)
        * [Create a Table](tables-iceberg-create.md)
        * [Load Data](tables-iceberg-load.md)
        * [Manage Tables](tables-iceberg-manage.md)
        * [Convert a Table](tables-iceberg-conversion.md)
        * [Use an external query engine](tables-iceberg-use-external-query-engine.md)
        * [Snowflake Open Catalog](tables-iceberg-open-catalog.md)
        * [Snowflake Catalog SDK](tables-iceberg-catalog.md)
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

[Guides](../guides/README.md)Data IntegrationApache Iceberg™Apache Iceberg™ Tables

# Apache Iceberg™ tables[¶](#iceberg-tm-tables "Link to this heading")

Apache Iceberg™ tables for Snowflake combine the performance and query semantics of typical
Snowflake tables with external cloud storage that you manage. They are
ideal for existing data lakes that you cannot, or choose not to, store in Snowflake.

Iceberg tables use the [Apache Iceberg™](https://iceberg.apache.org/) open table
format specification, which provides an abstraction layer on data files stored in open formats and supports features such as:

* ACID (atomicity, consistency, isolation, durability) transactions
* Schema evolution
* Hidden partitioning
* Table snapshots

Snowflake supports Iceberg tables that use the [Apache Parquet™](https://parquet.apache.org/) file format.

## Getting started[¶](#getting-started "Link to this heading")

To get started with Iceberg tables, see [Tutorial: Create your first Apache Iceberg™ table](tutorials/create-your-first-iceberg-table).

## How it works[¶](#how-it-works "Link to this heading")

This section provides information specific to working with Iceberg tables *in Snowflake*.
To learn more about the Iceberg table format specification,
see the official [Apache Iceberg documentation](https://iceberg.apache.org/docs/latest/) and the
[Iceberg Table Spec](https://iceberg.apache.org/spec/).

* [Data storage](#label-tables-iceberg-data-storage)
* [Catalog](#label-tables-iceberg-catalog-def)
* [Metadata and snapshots](#label-tables-iceberg-snapshots)
* [Cross-cloud/cross-region support](#label-tables-iceberg-cross-cloud-support)
* [Billing](#label-tables-iceberg-billing)

### Data storage[¶](#data-storage "Link to this heading")

Iceberg tables store their data and metadata files in an external cloud storage location
(Amazon S3, Google Cloud Storage, or Azure Storage). The external storage is not part of Snowflake. You are responsible
for all management of the external cloud storage location, including the configuration of data protection and recovery.
Snowflake does not provide [Fail-safe](data-failsafe) storage for Iceberg tables.

Snowflake connects to your storage location using an [external volume](#label-tables-iceberg-external-volume-def), and
Iceberg tables incur no Snowflake storage costs. For more information, see [Billing](#label-tables-iceberg-billing).

To learn more about storage for Iceberg tables, see [Storage for Apache Iceberg™ tables](tables-iceberg-storage).

#### External volume[¶](#external-volume "Link to this heading")

An external volume is a named, account-level Snowflake object that you use to connect Snowflake to your
external cloud storage for Iceberg tables. An external volume stores an identity and access management (IAM) entity
for your storage location. Snowflake uses the IAM entity to securely connect to your storage for accessing
table data, Iceberg metadata, and manifest files that store the table schema, partitions, and other metadata.

A single external volume can support one or more Iceberg tables.

To set up an external volume for Iceberg tables, see [Configure an external volume](tables-iceberg-configure-external-volume).

### Catalog[¶](#catalog "Link to this heading")

An Iceberg catalog enables a compute engine to manage and load Iceberg tables.
The catalog forms the first architectural layer in the [Iceberg table specification](https://iceberg.apache.org/spec/#overview) and
must support:

* Storing the current metadata pointer for one or more Iceberg tables.
  A metadata pointer maps a table name to the location of that table’s current metadata file.
* Performing atomic operations so that you can update the current metadata pointer for a table.

To learn more about Iceberg catalogs, see the [Apache Iceberg documentation](https://iceberg.apache.org/terms/#catalog-implementations).

Snowflake supports different [catalog options](#label-tables-iceberg-catalog-options). For example, you can use Snowflake as the
Iceberg catalog, or use a [catalog integration](#label-tables-iceberg-catalog-integration-def) to connect Snowflake to
an external Iceberg catalog.

#### Catalog integration[¶](#catalog-integration "Link to this heading")

A catalog integration is a named, account-level Snowflake object that stores information about how your table metadata is organized for the
following scenarios:

* When you don’t use [Snowflake as the Iceberg catalog](#label-tables-iceberg-snowflake-as-catalog). For example, you need a
  catalog integration if your table is managed by AWS Glue.
* When you want to integrate with [Snowflake Open Catalog](https://other-docs.snowflake.com/en/opencatalog/overview) to:

  + Query an Iceberg table in Snowflake Open Catalog using Snowflake.
  + Sync a Snowflake-managed Iceberg table with Snowflake Open Catalog so that third-party compute engines can query the table.

A single catalog integration can support one or more Iceberg tables that use the same external catalog.

To set up a catalog integration, see [Configure a catalog integration](tables-iceberg-configure-catalog-integration).

### Metadata and snapshots[¶](#metadata-and-snapshots "Link to this heading")

Iceberg uses a snapshot-based querying model, where data files are mapped using manifest and metadata files.
A snapshot represents the state of a table at a point in time and is used to access the complete set of data files in the table.

To learn about table metadata and Time Travel support, see [Metadata and retention for Apache Iceberg™ tables](tables-iceberg-metadata).

### Cross-cloud/cross-region support[¶](#cross-cloud-cross-region-support "Link to this heading")

Snowflake supports using an external volume storage location with a different cloud provider (in a different region)
from the one that hosts your Snowflake account.

| Table type | Cross-cloud/cross-region support | Notes |
| --- | --- | --- |
| Tables that use an external catalog with a [catalog integration](#label-tables-iceberg-catalog-integration) | ✔ | If your Snowflake account and external volume are in different regions, your external cloud storage account incurs egress costs when you query the table. |
| Tables that use [Snowflake as the catalog](#label-tables-iceberg-snowflake-as-catalog) | ✔ | If your Snowflake account and external volume are in different regions, your external cloud storage account incurs egress costs when you query the table.  These tables incur costs for cross-region data transfer usage. For more information, see [Billing](#label-tables-iceberg-billing). |

### Billing[¶](#billing "Link to this heading")

Snowflake bills your account for virtual warehouse (compute) usage and cloud services when you work with Iceberg tables.
Snowflake also bills your account if you use [automated refresh](tables-iceberg-auto-refresh.html#label-tables-iceberg-auto-refresh-billing) or an
[external query engine through Snowflake Horizon Catalog](tables-iceberg-query-using-external-query-engine-snowflake-horizon.html#label-tables-iceberg-query-using-external-query-engine-snowflake-horizon-billing).

If a [Snowflake-managed](#label-tables-iceberg-snowflake-as-catalog) Iceberg table is cross-cloud/cross-region, Snowflake bills your
cross-region data transfer usage under the TRANSFER\_TYPE of DATA\_LAKE. To learn more, see:

* [DATA\_TRANSFER\_HISTORY view](../sql-reference/organization-usage/data_transfer_history) in the ORGANIZATION\_USAGE schema.
* [DATA\_TRANSFER\_HISTORY view](../sql-reference/account-usage/data_transfer_history) in the ACCOUNT\_USAGE schema.

Snowflake does not bill your account for the following:

* Iceberg table storage costs. Your cloud storage provider bills you directly for data storage usage.
* Active bytes used by Iceberg tables. However,
  the [INFORMATION\_SCHEMA.TABLE\_STORAGE\_METRICS](../sql-reference/info-schema/table_storage_metrics) and
  [ACCOUNT\_USAGE.TABLE\_STORAGE\_METRICS](../sql-reference/account-usage/table_storage_metrics) views display ACTIVE\_BYTES for Iceberg tables
  to help you track how much storage a table occupies. To view an example, see [Retrieve storage metrics](tables-iceberg-manage.html#label-tables-iceberg-get-storage-metrics).

Note

If your Snowflake account and external volume are in different regions,
your external cloud storage account incurs egress costs when you query the table.

## Catalog options[¶](#catalog-options "Link to this heading")

Snowflake supports the following Iceberg catalog options:

* Use Snowflake as the [Iceberg catalog](#label-tables-iceberg-catalog-def)
* Use an external Iceberg catalog

The following table summarizes the differences between these catalog options.

|  | [Use Snowflake as the catalog](#label-tables-iceberg-snowflake-as-catalog) | [Use an external catalog](#label-tables-iceberg-catalog-integration) |
| --- | --- | --- |
| Read access | ✔ | ✔ |
| Write access | ✔ | ✔ |
| Catalog-vended credentials |  | ✔ |
| Write access across regions | ✔ | ✔ with [Write support for externally managed tables](tables-iceberg-externally-managed-writes) |
| Data and metadata storage | External volume (cloud storage) | External volume (cloud storage) |
| Snowflake platform support | ✔ |  |
| Integrates with Snowflake Open Catalog | ✔  You can sync a Snowflake-managed table with Open Catalog to query a table using other compute engines. | ✔  You can use Snowflake to query or write to Iceberg tables managed by Open Catalog. |
| Works with the [Snowflake Catalog SDK](tables-iceberg-catalog) | ✔ | ✔ |
| Replication for tables | ✔  See [Configure replication for Snowflake-managed Apache Iceberg™ tables](tables-iceberg-replication). |  |

### Use Snowflake as the catalog[¶](#use-snowflake-as-the-catalog "Link to this heading")

An Iceberg table that uses Snowflake as the Iceberg catalog (Snowflake-managed Iceberg table) provides full Snowflake platform support with
read and write access. The table data and metadata are stored in external cloud storage, which Snowflake accesses using an
[external volume](#label-tables-iceberg-external-volume-def). Snowflake
handles all life-cycle maintenance, such as compaction, for the table. However, you can [disable compaction for the table](tables-iceberg-manage.html#label-tables-iceberg-manage-set-data-compaction)
, if needed.

[![How Iceberg tables that use Snowflake as the Iceberg catalog work](../_images/tables-iceberg-snowflake-as-catalog.svg)](../_images/tables-iceberg-snowflake-as-catalog.svg)

### Use an external catalog[¶](#use-an-external-catalog "Link to this heading")

An Iceberg table that uses an external catalog provides limited Snowflake platform support.

With this table type, Snowflake uses a [catalog integration](#label-tables-iceberg-catalog-integration-def)
to retrieve information about your Iceberg metadata and schema.

You can use this option to create an Iceberg table for the following sources:

* [Remote Iceberg REST catalog](tables-iceberg-configure-catalog-integration-rest), including
  [AWS Glue](tables-iceberg-configure-catalog-integration-rest-glue) and [Snowflake Open Catalog](tables-iceberg-open-catalog).
  Snowflake supports writes to externally managed tables that use a remote Iceberg REST catalog.
* [Delta table files in object storage](tables-iceberg-configure-catalog-integration-object-storage.html#label-tables-iceberg-create-cat-int-delta)
* [Iceberg metadata files in object storage](tables-iceberg-configure-catalog-integration-object-storage.html#label-tables-iceberg-create-cat-int-iceberg-files)

Snowflake does not assume any life-cycle management on the table.

The table data and metadata are stored in external cloud storage, which Snowflake accesses using an
[external volume](#label-tables-iceberg-external-volume-def).

Note

If you want full Snowflake platform support for an Iceberg table that uses an external catalog, you can convert it to use Snowflake as
the catalog. For more information, see [Convert an Apache Iceberg™ table to use Snowflake as the catalog](tables-iceberg-conversion).

The following diagram shows how an Iceberg table uses a catalog integration with an external
Iceberg catalog.

[![How Iceberg tables that use a catalog integration work](../_images/tables-iceberg-external-catalog.svg)](../_images/tables-iceberg-external-catalog.svg)

## Considerations and limitations[¶](#considerations-and-limitations "Link to this heading")

The following considerations and limitations apply to Iceberg tables, and are subject to change:

**Clouds and regions**

> * Iceberg tables are available for all Snowflake accounts, on all cloud platforms and in all regions.
> * Cross-cloud/cross-region tables are supported. For more information, see [Cross-cloud/cross-region support](#label-tables-iceberg-cross-cloud-support).

**Iceberg**

> * Versions 1 and 2 of the Apache Iceberg specification are supported, excluding the following [features](https://iceberg.apache.org/spec/):
>
>   + Row-level equality deletes. However, tables that use Snowflake as the catalog support Snowflake
>     [DELETE](../sql-reference/sql/delete) statements.
>   + Using the `history.expire.min-snapshots-to-keep`
>     [table property](https://iceberg.apache.org/docs/1.2.1/configuration/#table-behavior-properties)
>     to specify the default minimum number of snapshots to keep. For more information, see [Metadata and snapshots](#label-tables-iceberg-snapshots).
> * Iceberg partitioning with the `bucket` transform function impacts performance for queries that use conditional clauses
>   to filter results.
> * For Iceberg tables that aren’t managed by Snowflake, be aware of the following:
>
>   + Time travel to any snapshot generated after table creation is supported
>     as long as you periodically refresh the table before the snapshot expires.
>   + Converting a table that has an un-materialized identity partition column isn’t supported.
>     An un-materialized identity partition column is created when a table defines an identity transform
>     using a source column that doesn’t exist in a Parquet file.
>   + For [row-level deletes](tables-iceberg-manage.html#label-tables-iceberg-row-level-deletes):
>
>     - Snowflake supports [position deletes](https://iceberg.apache.org/spec/#position-delete-files) only.
>     - For the best read performance when you use row-level deletes, perform regular compaction and table maintenance to remove old delete files. For
>       information, see [Maintain tables that use an external catalog](tables-iceberg-manage.html#label-tables-iceberg-manage-external-catalog).
>     - Excessive position deletes, especially dangling position deletes, might prevent table creation and refresh operations.
>       To avoid this issue, perform table maintenance to remove extra position deletes.
>
>       The table maintenance method to use depends on your external Iceberg engine. For example, you can use the `rewrite_data_files` method
>       for Spark with the `delete-file-threshold` or `rewrite-all` options. For more information, see
>       [rewrite\_data\_files](https://iceberg.apache.org/docs/latest/spark-procedures/#rewrite_data_files) in the Apache Iceberg™ documentation.

**File formats**

> * Iceberg tables support Apache Parquet files.
> * Parquet files that use the unsigned integer logical type aren’t supported.
> * For Parquet files that use the `LIST` logical type, be aware of the following:
>
>   + The three-level annotation structure with the `element` keyword is supported. For more
>     information, see [Parquet Logical Type Definitions](https://github.com/apache/parquet-format/blob/master/LogicalTypes.md#lists). If your
>     Parquet file uses an obsolete format with the `array` keyword, you must regenerate your data based on the supported format.

**External volumes**

> * You can’t access the cloud storage locations in external volumes using a storage integration.
> * You must configure a separate trust relationship for each external volume that you create.
> * You can use [outbound private connectivity](private-connectivity-outbound) to access Snowflake-managed Iceberg tables
>   and Iceberg tables that use a catalog integration for object storage, but cannot use it to access Iceberg tables that use other catalog
>   integrations.
> * After you create a Snowflake-managed table,
>   the path to its files in external storage does not change, even if you rename the table.
> * Snowflake can’t support external volumes with S3 bucket names that contain dots (for example, `my.s3.bucket`).
>   S3 doesn’t support SSL for virtual-hosted-style buckets with dots in the name, and
>   Snowflake uses virtual-host-style paths and HTTPS to access data in S3.

**Metadata files**

> * The metadata files don’t identify the most recent snapshot of an Iceberg table.
> * You can’t modify the location of the data files or snapshot using the ALTER ICEBERG TABLE command.
>   To modify either of these settings, you must recreate the table (using the CREATE OR REPLACE ICEBERG TABLE syntax).
> * For tables that use an external catalog:
>
>   > + Ensure that manifest files don’t contain duplicates.
>   >   If duplicate files are present in the *same* snapshot, Snowflake returns an error that includes the path of the duplicate file.
>   > + You can’t create a table if the Parquet metadata contains invalid UTF-8 characters. Ensure that your Parquet metadata is UTF-8 compliant.
> * Snowflake detects corruptions and inconsistencies in Parquet metadata produced outside of Snowflake,
>   and surfaces issues through error messages.
>
>   It’s possible to create, refresh, or query externally managed (or converted) tables, even if the table metadata is inconsistent.
>   When writing Iceberg data, ensure that the table’s metadata statistics (for example, `RowCount` or `NullCount`) match the data content.
> * For tables that use Snowflake as the catalog, Snowflake processes DDL statements individually and produces metadata in a way that might differ from other catalogs.
>   For more information, see [DDL statements](tables-iceberg-transactions.html#label-tables-iceberg-transactions-ddl).

**Clustering**

> [Clustering](tables-clustering-keys) support depends on the type of Iceberg table.
>
> | Table type | Notes |
> | --- | --- |
> | Tables that use Snowflake as the Iceberg catalog | Set a clustering key by using either the CREATE ICEBERG TABLE or the ALTER ICEBERG TABLE command. To set or manage a clustering key, see [CREATE ICEBERG TABLE (Snowflake as the Iceberg catalog)](../sql-reference/sql/create-iceberg-table-snowflake) and [ALTER ICEBERG TABLE](../sql-reference/sql/alter-iceberg-table). |
> | Tables that use an external catalog | Clustering is not supported. |
> | Converted tables | Snowflake only clusters files if they were created after converting the table, or if the files have since been modified using a DML statement. |

**Delta**

> * Snowflake supports Delta reader version 2 and can read all tables written by engines using Delta Lake version 2.2.0.
> * Snowflake streams aren’t supported for Iceberg tables created from Delta table files with partition columns.
>   However, insert-only streams for tables created from Delta files *without* partition columns are supported.
> * Iceberg tables created from Delta files that were created before the [2024\_04](../release-notes/bcr-bundles/2025_04_bundle) release bundle are not supported in dynamic tables.
> * Snowflake doesn’t support creating Iceberg tables from Delta table definitions in the AWS Glue Data Catalog.
>
> * Parquet files (data files for Delta tables) that use any of the following features or data types aren’t supported:
>
>   + Field IDs.
>   + The INTERVAL data type.
>   + The DECIMAL data type with precision higher than 38.
>   + LIST or MAP types with one-level or two-level representation.
>   + Unsigned integer types (INT(signed = false)).
>   + The FLOAT16 data type.
> * You can use the Parquet physical type `int96` for TIMESTAMP, but Snowflake doesn’t support `int96` for TIMESTAMP\_NTZ.
>
> * For more information about Delta data types and Iceberg tables, see [Delta data types](tables-iceberg-data-types.html#label-tables-iceberg-delta-source-data-types).
> * Snowflake processes a maximum of 1000 Delta commit files each time you refresh a table using CREATE/ALTER … REFRESH.
>   If your table has over 1000 commit files, you can do additional manual refreshes.
>   Each time, the refresh process continues from where the last one stopped.
>
>   Note
>
>   Snowflake uses Delta checkpoint files when creating an Iceberg table.
>   The 1,000 commit file limit only applies to commits after the latest checkpoint.
>
>   When you refresh an existing table, Snowflake processes Delta commit files, but not checkpoint files. If table maintenance removes stale log and data files for the source
>   Delta table, you should refresh Delta-based
>   Iceberg tables in Snowflake more frequently than the retention period of Delta logs and data files.
> * The following Delta Lake features aren’t currently supported: Row tracking, deletion vector files, change data files, change metadata,
>   DataChange, CDC, protocol evolution.

**Automated refresh**

> * For catalog integrations created before Snowflake version 8.22 (or 9.2 for Delta-based tables), you must manually set the `REFRESH_INTERVAL_SECONDS` parameter
>   before you enable automated refresh on tables that depend on that catalog integration.
>   For instructions, see [ALTER CATALOG INTEGRATION … SET AUTO\_REFRESH](../sql-reference/sql/alter-catalog-integration).
> * For [catalog integrations for object storage](tables-iceberg-configure-catalog-integration-object-storage), automated refresh is only supported
>   for integrations with `TABLE_FORMAT = DELTA`.
> * For tables with frequent updates, using a shorter polling interval (`REFRESH_INTERVAL_SECONDS`) can cause performance degradation.

**Catalog-linked databases and automatic table discovery**

> * Supported only when you use a catalog integration for Iceberg REST (for example, Snowflake Open Catalog).
> * To limit automatic table discovery to a specific set of namespaces, use the ALLOWED\_NAMESPACES parameter. You can also use the
>   BLOCKED\_NAMESPACES parameter to block a set of namespaces.
> * Snowflake doesn’t sync remote catalog access control for users or roles.
> * You can create schemas or externally managed Iceberg tables in a catalog-linked database. Creating other Snowflake objects
>   isn’t currently supported.
> * You can’t create database roles in a catalog-linked database.
> * Latency:
>
>   + For databases linked to 7,500 namespaces in a remote catalog, namespace and table discovery takes about one hour.
>   + For remote catalogs with 500,000 tables, the automated refresh process takes about one hour to complete.
>     For namespaces with different latency requirements, we recommend that you create separate catalog-linked databases.
>     Each database should reference a catalog integration with an appropriate auto-refresh interval (REFRESH\_INTERVAL\_SECONDS).
> * For Iceberg tables in a catalog-linked database:
>
>   + Snowflake doesn’t copy remote catalog table properties (such as retention policies or buffers), and doesn’t currently support altering table properties.
>   + [Automated refresh](tables-iceberg-auto-refresh) is enabled by default. If the `table-uuid` of an external table
>     and the catalog-linked database table don’t match, refresh fails and Snowflake drops the table from the catalog-linked database; Snowflake doesn’t change the remote table.
>   + If you drop a table from the remote catalog, Snowflake drops the table from the catalog-linked database.
>     This action is asynchronous, so you might not see the change in the remote catalog right away.
>   + If you rename a table in the remote catalog, Snowflake drops the existing table from the catalog-linked database and creates a table with the new name.
>   + Masking policies and tags are supported. Other Snowflake-specific features, including replication and cloning, aren’t supported.
>   + The character that you choose for the NAMESPACE\_FLATTEN\_DELIMITER parameter can’t appear in your remote namespaces. During the auto discovery process,
>     Snowflake skips any namespace that contains the delimiter, and doesn’t create a corresponding schema in your catalog-linked database.
>   + If you specify anything other than `_`, `$`, or numbers for the NAMESPACE\_FLATTEN\_DELIMITER parameter,
>     you must put the schema name in quotes when you query the table.
>   + For databases linked to AWS Glue, you must use lowercase letters and surround the schema, table, and column names in double quotes.
>     This is also required for other Iceberg REST catalogs that only support lowercase identifiers.
>
>     The following example shows a valid query:
>
>     ```
>     CREATE SCHEMA "s1";
>     ```
>
>     Copy
>
>     The following statements aren’t valid, because they use uppercase letters or omit the double quotes:
>
>     ```
>     CREATE SCHEMA s1;
>     CREATE SCHEMA "Schema1";
>     ```
>
>     Copy
>   + Using UNDROP ICEBERG TABLE isn’t supported.
>   + Sharing:
>
>     - Sharing with a listing isn’t currently supported
>     - Direct sharing is supported
> * For writing to tables in a catalog-linked database:
>
>   + Creating tables in nested namespaces isn’t currently supported.
>   + Writing to tables in nested namespaces isn’t currently supported.
>   + Position [row-level deletes](https://iceberg.apache.org/spec/#row-level-deletes) are supported for tables stored
>     on Amazon S3, Azure, or Google Cloud. Row-level deletes with equality delete files aren’t supported. For more information about row-level deletes,
>     see [Use row-level deletes](tables-iceberg-manage.html#label-tables-iceberg-row-level-deletes). To turn off position deletes, which enable
>     running the Data Manipulation Language (DML) operations in copy-on-write mode, set the `ENABLE_ICEBERG_MERGE_ON_READ` parameter to FALSE at the table, schema, or
>     database level.

**Externally managed write support**

> * Snowflake supports externally managed writes for Iceberg tables that use version 2 of the
>   [Iceberg table specification](https://iceberg.apache.org/spec/).
> * Snowflake provides Data Definition Language (DDL) and Data Manipulation Language (DML) commands for externally managed tables. However,
>   you configure metadata and data retention using your external catalog and the tools provided by your external storage provider.
>   For more information, see [Tables that use an external catalog](tables-iceberg-metadata.html#label-tables-iceberg-metadata-externally-managed).
>
>   For writes, Snowflake ensures that changes are committed to your remote catalog before updating the table in Snowflake.
> * If you use a catalog-linked database, you can use the CREATE ICEBERG TABLE syntax with column definitions to create a table in Snowflake
>   *and* in your remote catalog. If you use a standard Snowflake database (not linked to a catalog), you must first create a
>   table in your remote catalog. After that, you can use the [CREATE ICEBERG TABLE (Iceberg REST catalog)](../sql-reference/sql/create-iceberg-table-rest) syntax to create
>   an Iceberg table in Snowflake and write to it.
> * For the AWS Glue Data Catalog: Dropping an externally managed table through Snowflake doesn’t delete
>   the underlying table files. This behavior is specific to the AWS Glue Data Catalog implementation.
> * Position [row-level deletes](https://iceberg.apache.org/spec/#row-level-deletes) are supported for tables stored on
>   Amazon S3, Azure, or Google Cloud. Row-level deletes with equality delete files aren’t supported. For more information about row-level deletes,
>   see [Use row-level deletes](tables-iceberg-manage.html#label-tables-iceberg-row-level-deletes). To turn off position deletes, which enable
>   running the DML operations in copy-on-write mode, set the
>   `ENABLE_ICEBERG_MERGE_ON_READ` parameter to FALSE at the table, schema, or database level.
> * Writing to externally managed tables with the following Iceberg data types isn’t supported:
>
>   + `uuid`
>   + `fixed(L)`
> * The following features aren’t currently supported when you use Snowflake to write to externally managed Iceberg tables:
>
>   + Server-side encryption (SSE) for Azure external volumes.
>   + Multi-statement transactions. Snowflake supports autocommit transactions only.
>   + Conversion to Snowflake-managed tables.
>   + External Iceberg catalogs that don’t conform to the Iceberg REST protocol.
>   + Using the OR REPLACE option when creating a table.
>   + Using the CREATE ICEBERG TABLE (catalog-linked database) … AS SELECT syntax if you use one of the following catalogs as your remote catalog:
>
>     - AWS Glue
>     - Databricks Unity Catalog
>
>     Alternatively, you can use the [CREATE ICEBERG TABLE (Iceberg REST catalog)](../sql-reference/sql/create-iceberg-table-rest) syntax to create an empty Iceberg table and then use
>     an [INSERT INTO … SELECT](../sql-reference/sql/insert) statement to insert data into the empty table. However, this alternative
>     uses two separate transactions, so it doesn’t guarantee atomicity.
> * For creating schemas in a catalog-linked database, be aware of the following:
>
>   + The CREATE SCHEMA command creates a corresponding namespace in your remote catalog only when you use a catalog-linked database.
>   + The ALTER and CLONE options aren’t supported.
>   + Delimiters aren’t supported for schema names. Only alphanumeric schema names are supported.
>
> * You can set a target file size for a table’s Parquet files. For more information, see [Set a target file size](tables-iceberg-manage.html#label-tables-iceberg-target-file-size).
> * For Azure cloud storage services: Snowflake only supports externally managed writes for Iceberg tables that use the following services for external storage:
>
>   + Blob storage
>   + Data Lake Storage Gen2
>   + General-purpose v1
>   + General-purpose v2
>   + Microsoft Fabric OneLake
>
>   These services use blob endpoints. Services that use distributed file system (DFS) endpoints, including Azure Data Lake Storage Gen2 (ADLS), aren’t supported. When
>   you create your external Iceberg REST catalog, make sure you use a service for external storage that supports blob endpoints.
> * Sharing:
>
>   + Sharing with a listing isn’t currently supported.
>   + Direct sharing isn’t currently supported.

**Access by third-party clients to Iceberg data, metadata**

> * Third-party clients can’t append to, delete from, or upsert data to Iceberg tables that use Snowflake as the catalog.

**Table optimization**

* Snowflake doesn’t support orphan file deletion for Snowflake-managed Iceberg tables. If you see a mismatch between storage usage for your
  external cloud storage and Snowflake, you might have orphan files in your external cloud storage. To see your storage usage for Snowflake,
  you can use the [TABLE\_STORAGE\_METRICS view](../sql-reference/info-schema/table_storage_metrics) or [TABLE\_STORAGE\_METRICS view](../sql-reference/account-usage/table_storage_metrics).
  If you see a mismatch, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support) for assistance with determining whether you have orphan files and removing them.
* For Snowflake-managed Iceberg tables, if a DML operation fails unexpectedly and rolls back, some Parquet files might get written to your
  external cloud storage but won’t be tracked or referenced by your Iceberg table metadata. These Parquet files are orphan files.

**External query engines through Snowflake Horizon Catalog**

* For tables in Snowflake:

  + Only Snowflake-managed Iceberg tables are supported.
  + Querying remote or externally managed Iceberg tables including Delta Direct and Parquet Direct tables and Snowflake native tables,
    aren’t supported.
* You can query but can’t write to Iceberg tables.
* The external reads are supported only on Iceberg version 2 or earlier.
* This feature is only supported for Snowflake-managed Iceberg tables stored on Amazon S3, Google Cloud, or Azure for all public cloud
  regions. S3-compatible non-AWS storage is not yet supported.
* You can’t query an Iceberg table through the Horizon Iceberg REST API if the following fine-grained access control (FGAC) policies are
  defined on the table:

  + Row access policies
  + Column-level security
* Snowflake roles that include the hyphen character (-) in the role name aren’t supported when you access Iceberg tables through the Horizon
  Catalog endpoint.
* Explicitly granting the Horizon Catalog endpoint access to your storage accounts isn’t supported. We recommend that you use private connectivity for
  secure connectivity from external engines to Horizon Catalog and from Horizon Catalog to storage account.

**Unsupported features**

> The following Snowflake features aren’t currently supported for all Iceberg tables:
>
> * [Collation](../sql-reference/collation)
> * [Fail-safe](data-failsafe)
> * [Hybrid tables](tables-hybrid)
> * Snowflake encryption
> * [Snowflake Native App Framework](../developer-guide/native-apps/native-apps-about)
> * [Snowflake schema evolution](data-load-schema-evolution)
> * [Tagging](object-tagging/introduction) using the
>   [ASSOCIATE\_SEMANTIC\_CATEGORY\_TAGS](../sql-reference/stored-procedures/associate_semantic_category_tags) stored procedure
> * [Temporary and transient tables](tables-temp-transient)
>
> The following features aren’t supported for externally managed Iceberg tables:
>
> * [Cloning](tables-storage-considerations.html#label-cloning-tables)
> * [Clustering](tables-clustering-micropartitions)
> * Standard and append-only [streams](streams-intro). Insert-only streams are supported.
> * [Replication](account-replication-intro) of Iceberg tables, external volumes, or catalog integrations

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

1. [Getting started](#getting-started)
2. [How it works](#how-it-works)
3. [Data storage](#data-storage)
4. [Catalog](#catalog)
5. [Metadata and snapshots](#metadata-and-snapshots)
6. [Cross-cloud/cross-region support](#cross-cloud-cross-region-support)
7. [Billing](#billing)
8. [Catalog options](#catalog-options)
9. [Use Snowflake as the catalog](#use-snowflake-as-the-catalog)
10. [Use an external catalog](#use-an-external-catalog)
11. [Considerations and limitations](#considerations-and-limitations)

Related content

1. [Quickstart: Getting Started with Iceberg Tables](https://quickstarts.snowflake.com/guide/getting_started_iceberg_tables/index.html)
2. [Configure an external volume](/user-guide/tables-iceberg-configure-external-volume)
3. [Configure a catalog integration](/user-guide/tables-iceberg-configure-catalog-integration)
4. [Create an Apache Iceberg™ table in Snowflake](/user-guide/tables-iceberg-create)
5. [Manage Apache Iceberg™ tables](/user-guide/tables-iceberg-manage)