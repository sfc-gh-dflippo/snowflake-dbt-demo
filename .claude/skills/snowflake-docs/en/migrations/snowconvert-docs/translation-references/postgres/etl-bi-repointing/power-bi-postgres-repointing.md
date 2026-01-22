---
auto_generated: true
description: The Power BI repointing is a feature that provides an easy way to redefine
  the connections from the M language in the Power Query Editor. This means that the
  connection parameters will be redefined to
last_scraped: '2026-01-14T16:53:34.047643+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/postgres/etl-bi-repointing/power-bi-postgres-repointing
title: SnowConvert AI - PostgreSQL - Power BI Repointing | Snowflake Documentation
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
          + [Redshift](../../redshift/README.md)
          + [PostgreSQL-Greenplum-Netezza](../README.md)

            - [Built-in Functions](../postgresql-built-in-functions.md)
            - [Data Types](../data-types/postgresql-data-types.md)
            - [String Comparison](../postgresql-string-comparison.md)
            - DDLs

              - [CREATE MATERIALIZED VIEW](../ddls/create-materialized-view/postgresql-create-materialized-view.md)
              - [CREATE TABLE](../ddls/create-table/postgresql-create-table.md)
              - [CREATE VIEW](../ddls/postgresql-create-view.md)
            - [Expressions](../postgresql-expressions.md)
            - [Interactive Terminal](../postgresql-interactive-terminal.md)
            - ETL And BI Repointing

              - [Power BI PostgreSQL Repointing](power-bi-postgres-repointing.md)
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

[Guides](../../../../../guides/README.md)[Migrations](../../../../README.md)Tools[SnowConvert AI](../../../overview.md)Translation References[PostgreSQL-Greenplum-Netezza](../README.md)ETL And BI RepointingPower BI PostgreSQL Repointing

# SnowConvert AI - PostgreSQL - Power BI Repointing[¶](#snowconvert-ai-postgresql-power-bi-repointing "Link to this heading")

## Description[¶](#description "Link to this heading")

The Power BI repointing is a feature that provides an easy way to redefine the connections from the M language in the Power Query Editor. This means that the connection parameters will be redefined to point to the Snowflake migration database context. For Postgres, the method in M Language that defined the connection is `PostgreSQL.Database(...).` In Snowflake, there is a connector that depends on some other parameters and the main connection is defined by `Snowflake.Database(...)` method.

## Source Pattern Samples[¶](#source-pattern-samples "Link to this heading")

### Entity Repointing Case: Table[¶](#entity-repointing-case-table "Link to this heading")

This case refers to connections that do not contain embedded SQL. This means that the user has established a connection from Power BI to a table.

**PostgreSQL Connection in the Power Query Editor**

```
let
    Source = PostgreSQL.Database("your_connection", "mydatabase"),
    public_products = Source{[Schema="public",Item="products"]}[Data]
in
    public_products
```

Copy

**Snowflake Connection in the Power Query Editor**

```
let
    Source = Snowflake.Databases(SF_SERVER_LINK, SF_WAREHOUSE_NAME),
    SourceSfDb = Source{[Name=SF_DB_NAME, Kind="Database"]}[Data],
    SourceSfSchema = SourceSfDb{[Name="public", Kind="Schema"]}[Data],
    SourceSfTbl = SourceSfSchema{[Name="PRODUCTS", Kind="Table"]}[Data],
    public_products = Table.RenameColumns(SourceSfTbl, {{ "PRODUCT_ID", "product_id"}, { "PRODUCT_NAME", "product_name"}, { "PRICE", "price"}, { "STOCK_QUANTITY", "stock_quantity"}})
in
    public_products
```

Copy

### Entity Repointing Case: View[¶](#entity-repointing-case-view "Link to this heading")

This case refers to connections that do not contain embedded SQL. This means that the user has established a connection from Power BI to a view. The view uses the same pattern as the tables. It will only be validated with the symbol table; otherwise, it will be converted to a table. DDLs are important to this pattern.

**PostgreSQL Connection in the Power Query Editor**

```
let
    Source = PostgreSQL.Database("your_connection", "mydatabase"),
    public_expensive_products = Source{[Schema="public",Item="expensive_products"]}[Data]
in
    public_expensive_products
```

Copy

**Snowflake Connection in the Power Query Editor**

```
let
    Source = Snowflake.Databases(SF_SERVER_LINK, SF_WAREHOUSE_NAME),
    SourceSfDb = Source{[Name=SF_DB_NAME, Kind="Database"]}[Data],
    SourceSfSchema = SourceSfDb{[Name="public", Kind="Schema"]}[Data],
    SourceSfTbl = SourceSfSchema{[Name="EXPENSIVE_PRODUCTS", Kind="View"]}[Data],
    public_expensive_products = Table.RenameColumns(SourceSfTbl, {{ "PRODUCT_ID", "product_id"}, { "PRODUCT_NAME", "product_name"}, { "PRICE", "price"}})
in
    public_expensive_products
```

Copy

### Embedded SQL Case[¶](#embedded-sql-case "Link to this heading")

This case refers to connections that contain embedded SQL inside them. This sample shows a simple query, but SnowConvert AI covers a range of larger scenarios. Besides, depending on the migrated query, there may be warning messages known as EWI—PRF—FDM. This will help the user identify patterns that need extra attention.

**PostgreSQL Connection in the Power Query Editor**

```
let
    Source = Value.NativeQuery(PostgreSQL.Database("your_connection", "mydatabase"), "SELECT * FROM expensive_products", null, [EnableFolding=true])
in
    Source
```

Copy

**Snowflake Connection in the Power Query Editor**

```
let
    SfSource = Value.NativeQuery(Snowflake.Databases(SF_SERVER_LINK,SF_WAREHOUSE_NAME,[Implementation="2.0"]){[Name=SF_DB_NAME]}[Data], "SELECT * FROM
expensive_products", null, [EnableFolding=true]),
    Source = Table.RenameColumns(SfSource, {{ "PRODUCT_ID", "product_id"}, { "PRODUCT_NAME", "product_name"}, { "PRICE", "price"}})
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