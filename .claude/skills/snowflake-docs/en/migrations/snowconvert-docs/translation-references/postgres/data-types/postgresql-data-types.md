---
auto_generated: true
description: Current Data types conversion for PostgreSQL to Snowflake.
last_scraped: '2026-01-14T16:53:31.460039+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/postgres/data-types/postgresql-data-types
title: SnowConvert AI - PostgreSQL - Data types | Snowflake Documentation
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
            - [Data Types](postgresql-data-types.md)

              * [Netezza](netezza-data-types.md)
            - [String Comparison](../postgresql-string-comparison.md)
            - DDLs

              - [CREATE MATERIALIZED VIEW](../ddls/create-materialized-view/postgresql-create-materialized-view.md)
              - [CREATE TABLE](../ddls/create-table/postgresql-create-table.md)
              - [CREATE VIEW](../ddls/postgresql-create-view.md)
            - [Expressions](../postgresql-expressions.md)
            - [Interactive Terminal](../postgresql-interactive-terminal.md)
            - ETL And BI Repointing

              - [Power BI PostgreSQL Repointing](../etl-bi-repointing/power-bi-postgres-repointing.md)
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

[Guides](../../../../../guides/README.md)[Migrations](../../../../README.md)Tools[SnowConvert AI](../../../overview.md)Translation References[PostgreSQL-Greenplum-Netezza](../README.md)Data Types

# SnowConvert AI - PostgreSQL - Data types[¶](#snowconvert-ai-postgresql-data-types "Link to this heading")

Current Data types conversion for PostgreSQL to Snowflake.

## Applies to[¶](#applies-to "Link to this heading")

* PostgreSQL
* Greenplum
* Netezza

Snowflake supports most basic [SQL data types](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types) (with some restrictions) for use in columns, local variables, expressions, parameters, and any other appropriate/suitable locations.

## Numeric Data Types [¶](#numeric-data-types "Link to this heading")

| PostgreSQL | Snowflake |
| --- | --- |
| INT | INT |
| INT2 | SMALLINT |
| INT4 | INTEGER |
| INT8 | INTEGER |
| INTEGER | INTEGER |
| BIGINT | BIGINT |
| DECIMAL | DECIMAL |
| DOUBLE PRECISION | DOUBLE PRECISION |
| NUMERIC​ | NUMERIC |
| SMALLINT | SMALLINT |
| FLOAT | FLOAT |
| FLOAT4 | FLOAT4 |
| FLOAT8 | FLOAT8 |
| REAL | REAL​ |
| BIGSERIAL/SERIAL8 | INTEGER  *Note: Snowflake supports defining columns as IDENTITY, which automatically generates sequential values. This is the more concise and often preferred approach in Snowflake.* |

## Character Types [¶](#character-types "Link to this heading")

| PostgreSQL | Snowflake |
| --- | --- |
| VARCHAR | VARCHAR  *Note: VARCHAR holds Unicode UTF-8 characters. If no length is specified, the default is the maximum allowed length (16,777,216).* |
| CHAR | CHAR |
| CHARACTER | CHARACTER  *Note:* Snowflake’s CHARACTER is an alias for VARCHAR. |
| NCHAR | NCHAR |
| BPCHAR | VARCHAR  *Note: BPCHAR data type is **not supported** in Snowflake. VARCHAR is used instead. For more information please refer to* [*SSC-FDM-PG0002*](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/postgresqlFDM.md#ssc-fdm-pg0002)*.* |
| CHARACTER VARYING | CHARACTER VARYING |
| NATIONAL CHARACTER | NCHAR |
| NATIONAL CHARACTER VARYING | NCHAR VARYING |
| TEXT | TEXT |
| [NAME](https://www.postgresql.org/docs/current/datatype-character.html) (Special character type) | VARCHAR |

## Boolean Types [¶](#boolean-types "Link to this heading")

| PostgreSQL | Snowflake |
| --- | --- |
| BOOL/BOOLEAN | BOOLEAN |

## Binary Types [¶](#binary-types "Link to this heading")

| PostgreSQL | Snowflake |
| --- | --- |
| BYTEA | BINARY |

## Bit String Types [¶](#bit-string-types "Link to this heading")

| PostgreSQL | Snowflake |
| --- | --- |
| BIT | CHARACTER |
| BIT VARYING | CHARACTER VARYING |
| VARBIT | CHARACTER VARYING |

## Date & Time Data [¶](#date-time-data "Link to this heading")

| PostgreSQL | Snowflake |
| --- | --- |
| DATE | DATE |
| TIME | TIME |
| TIME WITH TIME ZONE | TIME  *Note: Time zone not supported for time data type. For more information, please refer to* [*SSC-FDM-0005*](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.md#ssc-fdm-0005)*.* |
| TIME WITHOUT TIME ZONE | TIME |
| TIMESTAMP | TIMESTAMP |
| TIMESTAMPTZ | TIMESTAMP\_TZ |
| TIMESTAMP WITH TIME ZONE | TIMESTAMP\_TZ |
| TIMESTAMP WITHOUT TIME ZONE | TIMESTAMP\_NTZ |
| INTERVAL YEAR TO MONTH | VARCHAR  *Note: Data type is **not supported** in Snowflake. VARCHAR is used instead. For more information please refer to* [*SSC-EWI-0036*](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.md#ssc-ewi-0036)*.* |
| INTERVAL DAY TO SECOND | VARCHAR  *Note: Data type is **not supported** in Snowflake. VARCHAR is used instead. For more information please refer to* [*SSC-EWI-0036*](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.md#ssc-ewi-0036)*.* |

## Pseudo Types[¶](#pseudo-types "Link to this heading")

| PostgreSQL | Snowflake |
| --- | --- |
| UNKNOWN | TEXT  *Note: Data type is **not supported** in Snowflake. TEXT is used instead. For more information please refer to* [*SSC-EWI-0036*](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.md#ssc-ewi-0036)*.* |

## Array Types[¶](#array-types "Link to this heading")

| PostgreSQL | Snowflake |
| --- | --- |
| type [] | ARRAY  *Note: Strongly typed array transformed to ARRAY without type checking. For more information please refer to* [*SSC-FDM-PG0016*](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/postgresqlFDM.md#ssc-fdm-pg0016)*.* |

## Related EWIs[¶](#related-ewis "Link to this heading")

1. [SSC-FDM-PG0002](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/postgresqlFDM.html#ssc-fdm-pg0002): Bpchar converted to varchar.
2. [SSC-FDM-PG0003](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/postgresqlFDM.html#ssc-fdm-pg0003): Bytea Converted To Binary
3. [SSC-FDM-PG0014](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/postgresqlFDM.html#ssc-fdm-pg0014): Unknown Pseudotype transformed to Text Type
4. [SSC-FDM-0005](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0005): TIME ZONE not supported for time data type.
5. [SSC-EWI-0036](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0036): Data type converted to another data type.
6. [SSC-EWI-PG0016](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/postgresqlEWI.html#ssc-ewi-pg0016): Bit String Type converted to Varchar Type.
7. [SSC-FDM-PG0016](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/postgresqlFDM.html#ssc-fdm-pg0016): *Strongly typed array transformed to ARRAY without type checking*.

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

1. [Applies to](#applies-to)
2. [Numeric Data Types](#numeric-data-types)
3. [Character Types](#character-types)
4. [Boolean Types](#boolean-types)
5. [Binary Types](#binary-types)
6. [Bit String Types](#bit-string-types)
7. [Date & Time Data](#date-time-data)
8. [Pseudo Types](#pseudo-types)
9. [Array Types](#array-types)
10. [Related EWIs](#related-ewis)