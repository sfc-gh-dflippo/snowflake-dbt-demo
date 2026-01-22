---
auto_generated: true
description: Snowflake supports most basic SQL data types (with some restrictions)
  for columns, local variables, expressions, parameters, and other appropriate/suitable
  locations.
last_scraped: '2026-01-14T16:53:10.386216+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/hive/data-types
title: SnowConvert AI - Hive - Data Types | Snowflake Documentation
---

1. [Overview](../../../../guides/README.md)
2. [Snowflake Horizon Catalog](../../../../user-guide/snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../../../../guides/overview-connecting.md)
6. [Virtual warehouses](../../../../user-guide/warehouses.md)
7. [Databases, Tables, & Views](../../../../guides/overview-db.md)
8. [Data types](../../../../data-types.md)
10. Data Integration

    - [Snowflake Openflow](../../../../user-guide/data-integration/openflow/about.md)
    - Apache Iceberg™

      - [Apache Iceberg™ Tables](../../../../user-guide/tables-iceberg.md)
      - [Snowflake Open Catalog](../../../../user-guide/opencatalog/overview.md)
11. Data engineering

    - [Data loading](../../../../guides/overview-loading-data.md)
    - [Dynamic Tables](../../../../user-guide/dynamic-tables-about.md)
    - [Streams and Tasks](../../../../user-guide/data-pipelines-intro.md)
    - [dbt Projects on Snowflake](../../../../user-guide/data-engineering/dbt-projects-on-snowflake.md)
    - [Data Unloading](../../../../guides/overview-unloading-data.md)
12. [Storage Lifecycle Policies](../../../../user-guide/storage-management/storage-lifecycle-policies.md)
13. [Migrations](../../../README.md)

    * Tools

      * [SnowConvert AI](../../overview.md)

        + General

          + [About](../../general/about.md)
          + [Getting Started](../../general/getting-started/README.md)
          + [Terms And Conditions](../../general/terms-and-conditions/README.md)
          + [Release Notes](../../general/release-notes/release-notes/README.md)
          + User Guide

            + [SnowConvert AI](../../general/user-guide/snowconvert/README.md)
            + [Project Creation](../../general/user-guide/project-creation.md)
            + [Extraction](../../general/user-guide/extraction.md)
            + [Deployment](../../general/user-guide/deployment.md)
            + [Data Migration](../../general/user-guide/data-migration.md)
            + [Data Validation](../../general/user-guide/data-validation.md)
            + [Power BI Repointing](../../general/user-guide/power-bi-repointing-general.md)
            + [ETL Migration](../../general/user-guide/etl-migration-replatform.md)
          + [Technical Documentation](../../general/technical-documentation/README.md)
          + [Contact Us](../../general/contact-us.md)
          + Others

            + [Using SnowConvert AI In A Ubuntu Docker Image](../../general/others/using-snowconvert-in-a-ubuntu-docker-image.md)
          + [Frequently Asked Questions (FAQ)](../../general/frequently-asked-questions-faq.md)")
        + Translation References

          + [General](../general/README.md)
          + [Teradata](../teradata/README.md)
          + [Oracle](../oracle/README.md)
          + [SQL Server-Azure Synapse](../transact/README.md)
          + [Sybase IQ](../sybase/README.md)
          + [Hive-Spark-Databricks SQL](README.md)

            - [DDLs](ddls/README.md)
            - [Built-in Functions](built-in-functions.md)
            - [Data Types](data-types.md)
          + [Redshift](../redshift/README.md)
          + [PostgreSQL-Greenplum-Netezza](../postgres/README.md)
          + [BigQuery](../bigquery/README.md)
          + [Vertica](../vertica/README.md)
          + [IBM DB2](../db2/README.md)
          + [SSIS](../ssis/README.md)
        + [Migration Assistant](../../migration-assistant/README.md)
        + [Data Validation CLI](../../data-validation-cli/index.md)
        + [AI Verification](../../snowconvert-ai-verification.md)
      * [Snowpark Migration Accelerator](../../../sma-docs/README.md)
    * Guides

      * [Teradata](../../../guides/teradata.md)
      * [Databricks](../../../guides/databricks.md)
      * [SQL Server](../../../guides/sqlserver.md)
      * [Amazon Redshift](../../../guides/redshift.md)
      * [Oracle](../../../guides/oracle.md)
      * [Azure Synapse](../../../guides/azuresynapse.md)
15. [Queries](../../../../guides/overview-queries.md)
16. [Listings](../../../../collaboration/collaboration-listings-about.md)
17. [Collaboration](../../../../guides/overview-sharing.md)
19. [Snowflake AI & ML](../../../../guides/overview-ai-features.md)
21. [Snowflake Postgres](../../../../user-guide/snowflake-postgres/about.md)
23. [Alerts & Notifications](../../../../guides/overview-alerts.md)
25. [Security](../../../../guides/overview-secure.md)
26. [Data Governance](../../../../guides/overview-govern.md)
27. [Privacy](../../../../guides/overview-privacy.md)
29. [Organizations & Accounts](../../../../guides/overview-manage.md)
30. [Business continuity & data recovery](../../../../user-guide/replication-intro.md)
32. [Performance optimization](../../../../guides/overview-performance.md)
33. [Cost & Billing](../../../../guides/overview-cost.md)

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)Translation References[Hive-Spark-Databricks SQL](README.md)Data Types

# SnowConvert AI - Hive - Data Types[¶](#snowconvert-ai-hive-data-types "Link to this heading")

Snowflake supports most basic SQL data types (with some restrictions) for
columns, local variables, expressions, parameters, and other
appropriate/suitable locations.

Applies to

* Hive SQL
* Spark SQL
* Databricks SQL

## Exact and approximate numerics[¶](#exact-and-approximate-numerics "Link to this heading")

| SparkSQL-DatabricksSQL | Snowflake | Notes |
| --- | --- | --- |
| TINYINT, SHORT | SMALLINT | ​Snowflake's SMALLINT has a larger range (-32768 to +32767) than Spark's TINYINT (-128 to +127). This should generally be a safe transformation. |
| SMALLINT | SMALLINT | Direct equivalent in terms of range. |
| INT, INTEGER | INT, INTEGER | ​Direct equivalent in terms of range. |
| BIGINT | BIGINT​ | Direct equivalent in terms of range. |
| DECIMAL(p, s)​ | NUMBER(p, s) | Snowflake's NUMBER(p, s) is the direct equivalent for fixed-precision and scale numbers. p is the precision (total number of digits) and s is the scale (number of digits to the right of the decimal point). |
| NUMERIC(p, s) | NUMBER(p, s) | Synonym for DECIMAL(p, s), maps directly to Snowflake's NUMBER(p, s). |
| FLOAT | FLOAT | Direct equivalent in terms of range. |
| DOUBLE, DOUBLE PRECISION | DOUBLE | Generally a good equivalent for double-precision floating-point numbers. |
| REAL | REAL | If REAL in your Spark context is strictly single-precision, be mindful of potential precision differences. |

## Date and time [¶](#date-and-time "Link to this heading")

| Hive-Spark-Databricks SQL | Snowflake | Notes |
| --- | --- | --- |
| DATE | DATE | Direct equivalent for storing calendar dates (year, month, day). |
| TIMESTAMP | TIMESTAMP\_NTZ | Snowflake offers several timestamp variations. TIMESTAMP\_NTZ (no time zone) is often the best general equivalent if your Spark TIMESTAMP doesn’t have specific time zone information tied to the data itself. |

## Character strings [¶](#character-strings "Link to this heading")

| Hive-Spark-Databricks SQL | Snowflake | Notes |
| --- | --- | --- |
| STRING | VARCHAR | ​Snowflake’s VARCHAR is the most common and flexible string type. It can store variable-length strings. |
| VARCHAR(n)​ | VARCHAR(n) | Direct equivalent for variable-length strings with a maximum length. |
| CHAR(n) | CHAR(n) | Direct equivalent for fixed-length strings. |

## Binary strings [¶](#binary-strings "Link to this heading")

| Hive-Spark-Databricks SQL | Snowflake | Notes |
| --- | --- | --- |
| BINARY | ​BINARY | Direct equivalent for storing raw byte sequences. |

## Boolean type [¶](#boolean-type "Link to this heading")

| Hive-Spark-Databricks SQL | Snowflake | Notes |
| --- | --- | --- |
| BOOLEAN, BOOL | ​BOOLEAN | Direct equivalent for storing boolean (TRUE/FALSE) values. |

## Complex type [¶](#complex-type "Link to this heading")

| Hive-Spark-Databricks SQL | Snowflake | Notes |
| --- | --- | --- |
| ARRAY<DataType> | ​ARRAY | Snowflake’s ARRAY type can store ordered lists of elements of a specified data type. The dataType within the array should also be mapped accordingly. |
| MAP<keyType, valueType> | VARIANT |  |
| STRUCT<name: dataType, …> | VARIANT |  |
| INTERVAL | VARCHAR(30) | INTERVAL data type is **not supported** in Snowflake. VARCHAR is used instead. |

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

1. [Exact and approximate numerics](#exact-and-approximate-numerics)
2. [Date and time](#date-and-time)
3. [Character strings](#character-strings)
4. [Binary strings](#binary-strings)
5. [Boolean type](#boolean-type)
6. [Complex type](#complex-type)