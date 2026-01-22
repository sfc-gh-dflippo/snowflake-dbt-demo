---
auto_generated: true
description: Snowflake supports most basic SQL data types (with some restrictions)
  for columns, local variables, expressions, parameters, and other appropriate/suitable
  locations.
last_scraped: '2026-01-14T16:53:57.292915+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/sybase/sybase-data-types
title: SnowConvert AI - Sybase IQ - Data Types | Snowflake Documentation
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
          + [Sybase IQ](README.md)

            - Statements

              - [CREATE TABLE](sybase-create-table.md)
              - [CREATE VIEW](sybase-create-view.md)
              - [SELECT](sybase-select-statement.md)
            - [Data Types](sybase-data-types.md)
            - [Built-in Functions](sybase-built-in-functions.md)
          + [Hive-Spark-Databricks SQL](../hive/README.md)
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)Translation References[Sybase IQ](README.md)Data Types

# SnowConvert AI - Sybase IQ - Data Types[¶](#snowconvert-ai-sybase-iq-data-types "Link to this heading")

Snowflake supports most basic SQL data types (with some restrictions) for columns, local variables, expressions, parameters, and other appropriate/suitable locations.

## Exact and approximate numerics[¶](#exact-and-approximate-numerics "Link to this heading")

| Sybase | Snowflake | Notes |
| --- | --- | --- |
| Sybase | Snowflake | Notes |
| BIGINT | BIGINT | ​Note that BIGINT in Snowflake is an alias for NUMBER(38,0)  [See note on this conversion below.] |
| BIT | BOOLEAN | Sybase only accepts ​1, 0, or NULL |
| DECIMAL | DECIMAL | ​Snowflake's DECIMAL is synonymous with NUMBER |
| FLOAT | FLOAT | ​This data type behaves equally on both systems.  Precision 7-15 digits, float (1-24)  Storage 4 - 8 bytes, float (25-53) |
| INT | INT | Note that INT in Snowflake is an alias for NUMBER(38,0)  [See note on this conversion below.] |
| SMALLINT | SMALLINT​ | ​This data type behaves equally |
| TINYINT​ | TINYINT | Note that TINYINT in Snowflake is an alias for NUMBER(38,0)  [See note on this conversion below.] |
| NUMERIC | NUMERIC | ​Snowflake's NUMERIC is synonymous with NUMBER |

**NOTE:**

* Each is converted to the alias in Snowflake with the same name for the conversion of integer data types (INT, SMALLINT, BIGINT, TINYINT). Each of those aliases is converted to NUMBER(38,0), a data type considerably larger than the integer datatype. Below is a comparison of the range of values that can be present in each data type:

  + Snowflake NUMBER(38,0): -99999999999999999999999999999999999999 to +99999999999999999999999999999999999999
  + Sybase TINYINT: 0 to 255
  + Sybase INT: -2^31 (-2,147,483,648) to 2^31-1 (2,147,483,647)
  + Sybase BIGINT: -2^63 (-9,223,372,036,854,775,808) to 2^63-1 (9,223,372,036,854,775,807)
  + Sybase SMALLINT: -2^15 (-32,768) to 2^15-1 (32,767)

## Date and time [¶](#date-and-time "Link to this heading")

| Sybase | Snowflake | Notes |
| --- | --- | --- |
| DATE | DATE | Sybase accepts range from 0001-01-01 to 9999-12-31 |
| DATETIME | TIMESTAMP\_NTZ(3) | Snowflake’s DATETIME is an alias for TIMESTAMP\_NTZ​ |
| SMALLDATETIME | TIMESTAMP\_NTZ | Snowflake’s DATETIME truncates the TIME information  i.e. 1955-12-13 12:43:10 is saved as 1955-12-13 |
| TIME | TIME | ​This data type behaves equally on both systems.  Range 00:00:00.0000000 through 23:59:59.9999999 |
| TIMESTAMP | TIMESTAMP |  |

## Character strings [¶](#character-strings "Link to this heading")

| Sybase | Snowflake | Notes |
| --- | --- | --- |
| CHAR | CHAR | ​Snowflake’s max string size in bytes is 167772161. |
| TEXT​ | TEXT |  |
| VARCHAR​ | VARCHAR | Snowflake’s max string size in bytes is 167772161. |

## Unicode character strings [¶](#unicode-character-strings "Link to this heading")

| Sybase | Snowflake | Notes |
| --- | --- | --- |
| NCHAR | NCHAR | Synonymous with VARCHAR except default length is VARCHAR(1). |
| NTEXT | TEXT | NTEXT is an Sybase domain type, implemented as a LONG NVARCHAR. |
| NVARCHAR | VARCHAR | Snowflake’s max string size in bytes is 167772161. |

## Binary strings [¶](#binary-strings "Link to this heading")

| Sybase | Snowflake | Notes |
| --- | --- | --- |
| BINARY | ​BINARY | In Snowflake the maximum length is 8 MB (8,388,608 bytes) and length is always measured in terms of bytes. |
| VARBINARY | VARBINARY | Snowflake use this data type as a synonymous with BINARY.  Snowflake often represents each byte as 2 hexadecimal characters |

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
4. [Unicode character strings](#unicode-character-strings)
5. [Binary strings](#binary-strings)