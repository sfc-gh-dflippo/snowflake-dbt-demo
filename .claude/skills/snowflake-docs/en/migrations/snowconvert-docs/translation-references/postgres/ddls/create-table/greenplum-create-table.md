---
auto_generated: true
description: Translation from Greenplum to Snowflake
last_scraped: '2026-01-14T16:53:32.452553+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/postgres/ddls/create-table/greenplum-create-table
title: SnowConvert AI - Greenplum - CREATE TABLE | Snowflake Documentation
---

1. [Overview](../../../../../../guides/README.md)
2. [Snowflake Horizon Catalog](../../../../../../user-guide/snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../../../../../../guides/overview-connecting.md)
6. [Virtual warehouses](../../../../../../user-guide/warehouses.md)
7. [Databases, Tables, & Views](../../../../../../guides/overview-db.md)
8. [Data types](../../../../../../data-types.md)
10. Data Integration

    - [Snowflake Openflow](../../../../../../user-guide/data-integration/openflow/about.md)
    - Apache Iceberg™

      - [Apache Iceberg™ Tables](../../../../../../user-guide/tables-iceberg.md)
      - [Snowflake Open Catalog](../../../../../../user-guide/opencatalog/overview.md)
11. Data engineering

    - [Data loading](../../../../../../guides/overview-loading-data.md)
    - [Dynamic Tables](../../../../../../user-guide/dynamic-tables-about.md)
    - [Streams and Tasks](../../../../../../user-guide/data-pipelines-intro.md)
    - [dbt Projects on Snowflake](../../../../../../user-guide/data-engineering/dbt-projects-on-snowflake.md)
    - [Data Unloading](../../../../../../guides/overview-unloading-data.md)
12. [Storage Lifecycle Policies](../../../../../../user-guide/storage-management/storage-lifecycle-policies.md)
13. [Migrations](../../../../../README.md)

    * Tools

      * [SnowConvert AI](../../../../overview.md)

        + General

          + [About](../../../../general/about.md)
          + [Getting Started](../../../../general/getting-started/README.md)
          + [Terms And Conditions](../../../../general/terms-and-conditions/README.md)
          + [Release Notes](../../../../general/release-notes/release-notes/README.md)
          + User Guide

            + [SnowConvert AI](../../../../general/user-guide/snowconvert/README.md)
            + [Project Creation](../../../../general/user-guide/project-creation.md)
            + [Extraction](../../../../general/user-guide/extraction.md)
            + [Deployment](../../../../general/user-guide/deployment.md)
            + [Data Migration](../../../../general/user-guide/data-migration.md)
            + [Data Validation](../../../../general/user-guide/data-validation.md)
            + [Power BI Repointing](../../../../general/user-guide/power-bi-repointing-general.md)
            + [ETL Migration](../../../../general/user-guide/etl-migration-replatform.md)
          + [Technical Documentation](../../../../general/technical-documentation/README.md)
          + [Contact Us](../../../../general/contact-us.md)
          + Others

            + [Using SnowConvert AI In A Ubuntu Docker Image](../../../../general/others/using-snowconvert-in-a-ubuntu-docker-image.md)
          + [Frequently Asked Questions (FAQ)](../../../../general/frequently-asked-questions-faq.md)")
        + Translation References

          + [General](../../../general/README.md)
          + [Teradata](../../../teradata/README.md)
          + [Oracle](../../../oracle/README.md)
          + [SQL Server-Azure Synapse](../../../transact/README.md)
          + [Sybase IQ](../../../sybase/README.md)
          + [Hive-Spark-Databricks SQL](../../../hive/README.md)
          + [Redshift](../../../redshift/README.md)
          + [PostgreSQL-Greenplum-Netezza](../../README.md)

            - [Built-in Functions](../../postgresql-built-in-functions.md)
            - [Data Types](../../data-types/postgresql-data-types.md)
            - [String Comparison](../../postgresql-string-comparison.md)
            - DDLs

              - [CREATE MATERIALIZED VIEW](../create-materialized-view/postgresql-create-materialized-view.md)
              - [CREATE TABLE](postgresql-create-table.md)

                * [Greenplum](greenplum-create-table.md)
                * [Netezza](netezza-create-table.md)
              - [CREATE VIEW](../postgresql-create-view.md)
            - [Expressions](../../postgresql-expressions.md)
            - [Interactive Terminal](../../postgresql-interactive-terminal.md)
            - ETL And BI Repointing

              - [Power BI PostgreSQL Repointing](../../etl-bi-repointing/power-bi-postgres-repointing.md)
          + [BigQuery](../../../bigquery/README.md)
          + [Vertica](../../../vertica/README.md)
          + [IBM DB2](../../../db2/README.md)
          + [SSIS](../../../ssis/README.md)
        + [Migration Assistant](../../../../migration-assistant/README.md)
        + [Data Validation CLI](../../../../data-validation-cli/index.md)
        + [AI Verification](../../../../snowconvert-ai-verification.md)
      * [Snowpark Migration Accelerator](../../../../../sma-docs/README.md)
    * Guides

      * [Teradata](../../../../../guides/teradata.md)
      * [Databricks](../../../../../guides/databricks.md)
      * [SQL Server](../../../../../guides/sqlserver.md)
      * [Amazon Redshift](../../../../../guides/redshift.md)
      * [Oracle](../../../../../guides/oracle.md)
      * [Azure Synapse](../../../../../guides/azuresynapse.md)
15. [Queries](../../../../../../guides/overview-queries.md)
16. [Listings](../../../../../../collaboration/collaboration-listings-about.md)
17. [Collaboration](../../../../../../guides/overview-sharing.md)
19. [Snowflake AI & ML](../../../../../../guides/overview-ai-features.md)
21. [Snowflake Postgres](../../../../../../user-guide/snowflake-postgres/about.md)
23. [Alerts & Notifications](../../../../../../guides/overview-alerts.md)
25. [Security](../../../../../../guides/overview-secure.md)
26. [Data Governance](../../../../../../guides/overview-govern.md)
27. [Privacy](../../../../../../guides/overview-privacy.md)
29. [Organizations & Accounts](../../../../../../guides/overview-manage.md)
30. [Business continuity & data recovery](../../../../../../user-guide/replication-intro.md)
32. [Performance optimization](../../../../../../guides/overview-performance.md)
33. [Cost & Billing](../../../../../../guides/overview-cost.md)

[Guides](../../../../../../guides/README.md)[Migrations](../../../../../README.md)Tools[SnowConvert AI](../../../../overview.md)Translation References[PostgreSQL-Greenplum-Netezza](../../README.md)DDLs[CREATE TABLE](postgresql-create-table.md)Greenplum

# SnowConvert AI - Greenplum - CREATE TABLE[¶](#snowconvert-ai-greenplum-create-table "Link to this heading")

Translation from Greenplum to Snowflake

## Description[¶](#description "Link to this heading")

This section explains features exclusive to Greenplum.

For more information, please refer to [`CREATE TABLE`](https://techdocs.broadcom.com/us/en/vmware-tanzu/data-solutions/tanzu-greenplum/7/greenplum-database/ref_guide-sql_commands-CREATE_TABLE.html) the documentation.

## Grammar Syntax[¶](#grammar-syntax "Link to this heading")

```
CREATE TABLE <table_name> ( 
  [ <column_name> <data_type> [ ENCODING ( <storage_directive> [, ...] ) ]
] )
[ DISTRIBUTED BY ( <column> [<opclass>] [, ... ] ) 
    | DISTRIBUTED RANDOMLY
    | DISTRIBUTED REPLICATED ]
```

Copy

## ENCODING[¶](#encoding "Link to this heading")

Note

This syntax is not needed in Snowflake.

The compression encoding for a column. In Snowflake, defining ENCODING is unnecessary because it automatically handles data compression, unlike Greenplum, which could set up the encoding manually. For this reason, the ENCODING statement is removed during migration.

### Grammar Syntax[¶](#id1 "Link to this heading")

```
ENCODING ( <storage_directive> [, ...] )
```

Copy

### Sample Source[¶](#sample-source "Link to this heading")

#### Input Code:[¶](#input-code "Link to this heading")

##### Greenplum[¶](#greenplum "Link to this heading")

```
CREATE TABLE TABLE1 (
   COL1 integer ENCODING (compresstype = quicklz, blocksize = 65536)
);
```

Copy

#### Output Code:[¶](#output-code "Link to this heading")

##### Snowflake[¶](#snowflake "Link to this heading")

```
CREATE TABLE TABLE1 (
   COL1 integer
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "greenplum",  "convertedOn": "03/26/2025",  "domain": "test" }}'
;
```

Copy

## DISTRIBUTED BY[¶](#distributed-by "Link to this heading")

Hint

This syntax is fully supported in Snowflake.

The DISTRIBUTED BY clause in Greenplum controls how table data is physically distributed across the system’s segments. Meanwhile, CLUSTER BY is a subset of columns in a table (or expressions on a table) that are explicitly designated to co-locate the data in the table in the same micro-partitions.

### Grammar Syntax[¶](#id2 "Link to this heading")

```
DISTRIBUTED BY ( <column> [<opclass>] [, ... ] )
```

Copy

### Sample Source Patterns[¶](#sample-source-patterns "Link to this heading")

#### Input Code:[¶](#id3 "Link to this heading")

##### Greenplum[¶](#id4 "Link to this heading")

```
CREATE TABLE table1 (colum1 int, colum2 int, colum3 smallint, colum4 int )
DISTRIBUTED BY (colum1, colum2);
```

Copy

#### Output Code:[¶](#id5 "Link to this heading")

##### Snowflake[¶](#id6 "Link to this heading")

```
CREATE TABLE table1 (colum1 int, colum2 int, colum3 smallint, colum4 int )
--** SSC-FDM-GP0001 - THE PERFORMANCE OF THE CLUSTER BY MAY VARY COMPARED TO THE PERFORMANCE OF DISTRIBUTED BY **
CLUSTER BY (colum1, colum2)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "greenplum",  "convertedOn": "03/26/2025",  "domain": "test" }}'
;
```

Copy

## DISTRIBUTED RANDOMLY - REPLICATED[¶](#distributed-randomly-replicated "Link to this heading")

Note

This syntax is not needed in Snowflake.

The DISTRIBUTED REPLICATED or DISTRIBUTED RANDOMLY clause in Greenplum controls how table data is physically distributed across the system’s segments. As Snowflake automatically handles data storage, these options will be removed in the migration.

### Grammar Syntax[¶](#id7 "Link to this heading")

```
DISTRIBUTED RANDOMLY | DISTRIBUTED REPLICATED
```

Copy

### Sample Source Patterns[¶](#id8 "Link to this heading")

#### Input Code:[¶](#id9 "Link to this heading")

##### Greenplum[¶](#id10 "Link to this heading")

```
CREATE TABLE table1 (colum1 int, colum2 int, colum3 smallint, colum4 int )
DISTRIBUTED RANDOMLY;
```

Copy

#### Output Code:[¶](#id11 "Link to this heading")

##### Snowflake[¶](#id12 "Link to this heading")

```
CREATE TABLE table1 (colum1 int, colum2 int, colum3 smallint, colum4 int )
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "greenplum",  "convertedOn": "03/26/2025",  "domain": "test" }}'
;
```

Copy

## Related EWIs[¶](#related-ewis "Link to this heading")

1. [SSC-FDM-GP0001](../../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/greenplumFDM.html#ssc-fdm-gp0001): The performance of the CLUSTER BY may vary compared to the performance of Distributed By.

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
2. [Grammar Syntax](#grammar-syntax)
3. [ENCODING](#encoding)
4. [DISTRIBUTED BY](#distributed-by)
5. [DISTRIBUTED RANDOMLY - REPLICATED](#distributed-randomly-replicated)
6. [Related EWIs](#related-ewis)