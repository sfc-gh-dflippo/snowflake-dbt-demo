---
auto_generated: true
description: The Power BI repointing is a feature that provides an easy way to redefine
  the connections from the M language in the Power Query Editor. This means that the
  connection parameters will be redefined to
last_scraped: '2026-01-14T16:53:36.103606+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/redshift/etl-bi-repointing/power-bi-redshift-repointing
title: SnowConvert AI - Redshift - Power BI Repointing | Snowflake Documentation
---

1. [Overview](../../../../../guides/README.md)
2. [Snowflake Horizon Catalog](../../../../../user-guide/snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../../../../../guides/overview-connecting.md)
6. [Virtual warehouses](../../../../../user-guide/warehouses.md)
7. [Databases, Tables, & Views](../../../../../guides/overview-db.md)
8. [Data types](../../../../../data-types.md)
10. Data Integration

    - [Snowflake Openflow](../../../../../user-guide/data-integration/openflow/about.md)
    - Apache Iceberg™

      - [Apache Iceberg™ Tables](../../../../../user-guide/tables-iceberg.md)
      - [Snowflake Open Catalog](../../../../../user-guide/opencatalog/overview.md)
11. Data engineering

    - [Data loading](../../../../../guides/overview-loading-data.md)
    - [Dynamic Tables](../../../../../user-guide/dynamic-tables-about.md)
    - [Streams and Tasks](../../../../../user-guide/data-pipelines-intro.md)
    - [dbt Projects on Snowflake](../../../../../user-guide/data-engineering/dbt-projects-on-snowflake.md)
    - [Data Unloading](../../../../../guides/overview-unloading-data.md)
12. [Storage Lifecycle Policies](../../../../../user-guide/storage-management/storage-lifecycle-policies.md)
13. [Migrations](../../../../README.md)

    * Tools

      * [SnowConvert AI](../../../overview.md)

        + General

          + [About](../../../general/about.md)
          + [Getting Started](../../../general/getting-started/README.md)
          + [Terms And Conditions](../../../general/terms-and-conditions/README.md)
          + [Release Notes](../../../general/release-notes/release-notes/README.md)
          + User Guide

            + [SnowConvert AI](../../../general/user-guide/snowconvert/README.md)
            + [Project Creation](../../../general/user-guide/project-creation.md)
            + [Extraction](../../../general/user-guide/extraction.md)
            + [Deployment](../../../general/user-guide/deployment.md)
            + [Data Migration](../../../general/user-guide/data-migration.md)
            + [Data Validation](../../../general/user-guide/data-validation.md)
            + [Power BI Repointing](../../../general/user-guide/power-bi-repointing-general.md)
            + [ETL Migration](../../../general/user-guide/etl-migration-replatform.md)
          + [Technical Documentation](../../../general/technical-documentation/README.md)
          + [Contact Us](../../../general/contact-us.md)
          + Others

            + [Using SnowConvert AI In A Ubuntu Docker Image](../../../general/others/using-snowconvert-in-a-ubuntu-docker-image.md)
          + [Frequently Asked Questions (FAQ)](../../../general/frequently-asked-questions-faq.md)")
        + Translation References

          + [General](../../general/README.md)
          + [Teradata](../../teradata/README.md)
          + [Oracle](../../oracle/README.md)
          + [SQL Server-Azure Synapse](../../transact/README.md)
          + [Sybase IQ](../../sybase/README.md)
          + [Hive-Spark-Databricks SQL](../../hive/README.md)
          + [Redshift](../README.md)

            - [Basic Elements](../redshift-basic-elements.md)
            - [Expressions](../redshift-expressions.md)
            - [Conditions](../redshift-conditions.md)
            - [Data types](../redshift-data-types.md)
            - [SQL Statements](../redshift-sql-statements.md)
            - [Functions](../redshift-functions.md)
            - [System Catalog Tables](../redshift-system-catalog.md)
            - ETL And BI Repointing

              - [Power BI Redshift Repointing](power-bi-redshift-repointing.md)
          + [PostgreSQL-Greenplum-Netezza](../../postgres/README.md)
          + [BigQuery](../../bigquery/README.md)
          + [Vertica](../../vertica/README.md)
          + [IBM DB2](../../db2/README.md)
          + [SSIS](../../ssis/README.md)
        + [Migration Assistant](../../../migration-assistant/README.md)
        + [Data Validation CLI](../../../data-validation-cli/index.md)
        + [AI Verification](../../../snowconvert-ai-verification.md)
      * [Snowpark Migration Accelerator](../../../../sma-docs/README.md)
    * Guides

      * [Teradata](../../../../guides/teradata.md)
      * [Databricks](../../../../guides/databricks.md)
      * [SQL Server](../../../../guides/sqlserver.md)
      * [Amazon Redshift](../../../../guides/redshift.md)
      * [Oracle](../../../../guides/oracle.md)
      * [Azure Synapse](../../../../guides/azuresynapse.md)
15. [Queries](../../../../../guides/overview-queries.md)
16. [Listings](../../../../../collaboration/collaboration-listings-about.md)
17. [Collaboration](../../../../../guides/overview-sharing.md)
19. [Snowflake AI & ML](../../../../../guides/overview-ai-features.md)
21. [Snowflake Postgres](../../../../../user-guide/snowflake-postgres/about.md)
23. [Alerts & Notifications](../../../../../guides/overview-alerts.md)
25. [Security](../../../../../guides/overview-secure.md)
26. [Data Governance](../../../../../guides/overview-govern.md)
27. [Privacy](../../../../../guides/overview-privacy.md)
29. [Organizations & Accounts](../../../../../guides/overview-manage.md)
30. [Business continuity & data recovery](../../../../../user-guide/replication-intro.md)
32. [Performance optimization](../../../../../guides/overview-performance.md)
33. [Cost & Billing](../../../../../guides/overview-cost.md)

[Guides](../../../../../guides/README.md)[Migrations](../../../../README.md)Tools[SnowConvert AI](../../../overview.md)Translation References[Redshift](../README.md)ETL And BI RepointingPower BI Redshift Repointing

# SnowConvert AI - Redshift - Power BI Repointing[¶](#snowconvert-ai-redshift-power-bi-repointing "Link to this heading")

## Description[¶](#description "Link to this heading")

The Power BI repointing is a feature that provides an easy way to redefine the connections from the M language in the Power Query Editor. This means that the connection parameters will be redefined to point to the Snowflake migration database context. For Redshift, the method in M Language that defined the connection is `AmazonRedshift.Database(...).` In Snowflake, there is a connector that depends on some other parameters and the main connection is defined by `Snowflake.Database(...)` method.

## Source Pattern Samples[¶](#source-pattern-samples "Link to this heading")

### Entity Repointing Case: Table[¶](#entity-repointing-case-table "Link to this heading")

This case refers to connections that do not contain embedded SQL. This means that the user has established a connection from Power BI to a table.

**Redshift Connection in the Power Query Editor**

```
let
    Source = AmazonRedshift.Database("your_connection","snowconvert"),
    public = Source{[Name="public"]}[Data],
    authors1 = public{[Name="authors"]}[Data]
in
    authors1
```

Copy

**Snowflake Connection in the Power Query Editor**

```
let
    Source = Snowflake.Databases(SF_SERVER_LINK, SF_WAREHOUSE_NAME),
    SourceSfDb = Source{[Name=SF_DB_NAME, Kind="Database"]}[Data],
    SourceSfSchema = SourceSfDb{[Name="public", Kind="Schema"]}[Data],
    SourceSfTbl = SourceSfSchema{[Name="AUTHORS", Kind="Table"]}[Data],
    authors1 = Table.RenameColumns(SourceSfTbl, {{ "AUTHOR_ID", "author_id"}, { "FIRST_NAME", "first_name"}, { "LAST_NAME", "last_name"}, { "BIRTH_YEAR", "birth_year"}})
in
    authors1
```

Copy

### Entity Repointing Case: View[¶](#entity-repointing-case-view "Link to this heading")

This case refers to connections that do not contain embedded SQL. This means that the user has established a connection from Power BI to a view.

**Redshift Connection in the Power Query Editor**

```
let
    Source = AmazonRedshift.Database("your_connection","snowconvert"),
    public = Source{[Name="public"]}[Data],
    author_books_view1 = public{[Name="author_books_view"]}[Data]
in
    author_books_view1
```

Copy

**Snowflake Connection in the Power Query Editor**

```
let
    Source = Snowflake.Databases(SF_SERVER_LINK, SF_WAREHOUSE_NAME),
    SourceSfDb = Source{[Name=SF_DB_NAME, Kind="Database"]}[Data],
    SourceSfSchema = SourceSfDb{[Name="public", Kind="Schema"]}[Data],
    SourceSfTbl = SourceSfSchema{[Name="AUTHOR_BOOKS_VIEW", Kind="Table"]}[Data],
    author_books_view1 = Table.RenameColumns(SourceSfTbl, {{ "BOOK_TITLE", "book_title"}, { "AUTHOR_FULL_NAME", "author_full_name"}, { "PUBLICATION_YEAR", "publication_year"}, { "GENRE", "genre"}})
in
    author_books_view1
```

Copy

### Embedded SQL Case[¶](#embedded-sql-case "Link to this heading")

This case refers to connections that contain embedded SQL inside them. This sample shows a simple query, but SnowConvert AI covers a range of larger scenarios. Besides, depending on the migrated query, there may be warning messages known as EWI—PRF—FDM. This will help the user identify patterns that need extra attention.

**Redshift Connection in the Power Query Editor**

```
let
    Source = Value.NativeQuery(AmazonRedshift.Database("your_connection","snowconvert"), "SELECT * FROM authors LIMIT 5", null, [EnableFolding=true])
in
    Source
```

Copy

**Snowflake Connection in the Power Query Editor**

```
let
    SfSource = Value.NativeQuery(Snowflake.Databases(SF_SERVER_LINK,SF_WAREHOUSE_NAME,[Implementation="2.0"]){[Name=SF_DB_NAME]}[Data], "--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT ""authors"" **
SELECT * FROM
authors
LIMIT 5", null, [EnableFolding=true]),
    Source = Table.RenameColumns(SfSource, {{ "AUTHOR_ID", "author_id"}, { "FIRST_NAME", "first_name"}, { "LAST_NAME", "last_name"}, { "BIRTH_YEAR", "birth_year"}})
in
    Source
```

Copy

Was this page helpful?

YesNo

[Visit Snowflake](https://www.snowflake.com)

[Join the conversation](https://community.snowflake.com/s/)

[Develop with Snowflake](https://developers.snowflake.com)

[Share your feedback](/feedback)

[Read the latest on our blog](https://www.snowflake.com/blog/)

[Get your own certification](https://learn.snowflake.com)

[Privacy Notice](https://www.snowflake.com/privacy-policy/)[Site Terms](https://www.snowflake.com/legal/snowflake-site-terms/)Cookies Settings© 2026 Snowflake, Inc. All Rights Reserved.

Terms of Use

The SnowConvert AI tool is subject to the [Conversion Software Terms of Use](https://www.snowflake.com/en/legal/technical-services-and-education/conversion-software-terms/).

On this page

1. [Description](#description)
2. [Source Pattern Samples](#source-pattern-samples)