---
auto_generated: true
description: Equivalents for DBC objects and columns
last_scraped: '2026-01-14T16:53:51.315487+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/teradata/sql-translation-reference/database-dbc
title: SnowConvert AI - Teradata - Database DBC | Snowflake Documentation
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
          + [Teradata](../README.md)

            - [Data Migration Considerations](../data-migration-considerations.md)
            - [Session Modes in Teradata](../session-modes.md)
            - [Sql Translation Reference](README.md)

              * [Built-in Functions](teradata-built-in-functions.md)
              * [Data Types](data-types.md)
              * [Database DBC](database-dbc.md)
              * [DDL Statements](ddl-teradata.md)
              * [DML Statements](dml-teradata.md)
              * [Analytic](analytic.md)
              * [Iceberg Table Transformations](Iceberg-tables-transformations.md)
            - [SQL to JavaScript (Procedures)](../teradata-to-javascript-translation-reference.md)")
            - [SQL to Snowflake Scripting (Procedures)](../teradata-to-snowflake-scripting-translation-reference.md)")
            - [Scripts To Python](../scripts-to-python/README.md)
            - [Scripts to Snowflake SQL](../scripts-to-snowflake-sql-translation-reference/README.md)
            - ETL And BI Repointing

              - [Power BI Teradata Repointing](../etl-bi-repointing/power-bi-teradata-repointing.md)
          + [Oracle](../../oracle/README.md)
          + [SQL Server-Azure Synapse](../../transact/README.md)
          + [Sybase IQ](../../sybase/README.md)
          + [Hive-Spark-Databricks SQL](../../hive/README.md)
          + [Redshift](../../redshift/README.md)
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

[Guides](../../../../../guides/README.md)[Migrations](../../../../README.md)Tools[SnowConvert AI](../../../overview.md)Translation References[Teradata](../README.md)[Sql Translation Reference](README.md)Database DBC

# SnowConvert AI - Teradata - Database DBC[¶](#snowconvert-ai-teradata-database-dbc "Link to this heading")

Equivalents for DBC objects and columns

Note

The DBC database contains critical system tables that define the user databases in the Analytics Database / Teradata Database. In the next segments, you can see the **supported** objects and columns of DBC database, the ones missing are **not supported** yet.

## DBC database[¶](#dbc-database "Link to this heading")

| Teradata | Snowflake | Notes |
| --- | --- | --- |
| DBC | INFORMATION\_SCHEMA |  |

> See [DBC database](https://docs.teradata.com/r/Teradata-DSA-User-Guide/November-2022/Database-DBC-Info/Database-DBC)

## DBC tables[¶](#dbc-tables "Link to this heading")

| Teradata | Snowflake | Notes |
| --- | --- | --- |
| COLUMNS | COLUMNS |  |
| COLUMNSV | COLUMNS |  |
| DATABASES | DATABASES |  |
| DBQLOGTBL | TABLE(INFORMATION\_SCHEMA.QUERY\_HISTORY()) |  |
| TABLES | TABLES |  |

## DBC columns[¶](#dbc-columns "Link to this heading")

| Teradata | Snowflake | Notes |
| --- | --- | --- |
| ALLRIGHTS | APPLICABLE\_ROLES |  |
| COLUMNNAME | COLUMN\_NAME |  |
| COLUMNUDTNAME | UDT\_NAME |  |
| COMMENT\_STRING | COMMENT |  |
| CREATETIMESTAMP | CREATED |  |
| COLUMNTYPE | DATA\_TYPE |  |
| COLUMNLENGTH | CHARACTER\_MAXIMUM\_LENGTH |  |
| CONSTRAINTNAME | CONSTRAINT\_NAME |  |
| CONSTRAINTTEXT | CONSTRAINT\_TYPE |  |
| DATABASENAME | TABLE\_SCHEMA |  |
| FINALWDNAME | SESSION\_ID |  |
| FIRSTSTEPTIME | DATEADD(MILLISECOND, TOTAL\_ELAPSED\_TIME - EXECUTION\_TIME, START\_TIME) |  |
| LASTALTERTIMESTAMP | LAST\_ALTERED |  |
| NULLABLE | IS\_NULLABLE |  |
| STARTTIME | START\_TIME |  |
| TABLEKIND | TABLE\_TYPE |  |
| TABLE\_LEVELCONSTRAINTS | TABLE\_CONSTRAINTS |  |
| TABLENAME | TABLE\_NAME |  |
| USER\_NAME | GRANTEE |  |

> For more information about DBC tables and columns see the [Teradata documentation.](https://docs.teradata.com/r/hNI_rA5LqqKLxP~Y8vJPQg/jwOyftGqfH5vIH1ZRVNW6A)

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

1. [DBC database](#dbc-database)
2. [DBC tables](#dbc-tables)
3. [DBC columns](#dbc-columns)