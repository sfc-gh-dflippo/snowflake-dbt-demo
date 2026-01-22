---
auto_generated: true
description: Snowflake supports most basic SQL data types (with some restrictions)
  for use in columns, local variables, expressions, parameters, and any other appropriate/suitable
  locations.
last_scraped: '2026-01-14T16:54:06.541993+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/transact/transact-data-types
title: SnowConvert AI - SQL Server-Azure Synapse - Data Types | Snowflake Documentation
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
          + [SQL Server-Azure Synapse](README.md)

            - [ANSI NULLS](transact-ansi-nulls.md)
            - [QUOTED\_IDENTIFIER](transact-quoted-identifier.md)
            - [Built-in Functions](transact-built-in-functions.md)
            - [Built-in Procedures](transact-built-in-procedures.md)
            - Data Definition Language

              - [ALTER TABLE](transact-alter-statement.md)
              - [CONTINUE HANDLER](transact-continue-handler.md)
              - [EXIT HANDLER](transact-exit-handler.md)
              - [CREATE FUNCTION](transact-create-function.md)
              - [CREATE INDEX](transact-create-index.md)
              - [CREATE MATERIALIZED VIEW](transact-create-materialized-view.md)
              - [CREATE PROCEDURE (JavaScript)](transact-create-procedure.md)")
              - [CREATE PROCEDURE (Snowflake Scripting)](transact-create-procedure-snow-script.md)")
              - [CREATE TABLE](transact-create-table.md)
              - [CREATE VIEW](transact-create-view.md)
            - [Data Types](transact-data-types.md)
            - [Data Manipulation Language](transact-dmls.md)
            - [General Statements](transact-general-statements.md)
            - [SELECT](transact-select.md)
            - [SYSTEM TABLES](transact-system-tables.md)
            - ETL And BI Repointing

              - [Power BI Transact and Synapse Repointing](etl-bi-repointing/power-bi-transact-repointing.md)
          + [Sybase IQ](../sybase/README.md)
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)Translation References[SQL Server-Azure Synapse](README.md)Data Types

# SnowConvert AI - SQL Server-Azure Synapse - Data Types[¶](#snowconvert-ai-sql-server-azure-synapse-data-types "Link to this heading")

Snowflake supports most basic SQL data types (with some restrictions) for use in columns, local variables, expressions, parameters, and any other appropriate/suitable locations.

Applies to

* SQL Server
* Azure Synapse Analytics

## Exact and approximate numerics[¶](#exact-and-approximate-numerics "Link to this heading")

| T-SQL | Snowflake | Notes |
| --- | --- | --- |
| BIGINT | BIGINT | ​Note that BIGINT in Snowflake is an alias for NUMBER(38,0)  [See note on this conversion below.] |
| BIT | BOOLEAN | SQLServer only accepts ​1, 0, or NULL |
| DECIMAL | DECIMAL | ​Snowflake’s DECIMAL is synonymous with NUMBER |
| FLOAT | FLOAT | ​This data type behaves equally on both systems.  Precision 7-15 digits, float (1-24)  Storage 4 - 8 bytes, float (25-53) |
| INT | INT | Note that INT in Snowflake is an alias for NUMBER(38,0)  [See note on this conversion below.] |
| MONEY | NUMBER(38, 4) | [See note on this conversion below.] |
| REAL​ | REAL | Snowflake’s REAL is synonymous with FLOAT |
| SMALLINT | SMALLINT​ | ​This data type behaves equally |
| SMALLMONEY | NUMBER(38, 4) | [See note on this conversion below.] |
| TINYINT​ | TINYINT | Note that TINYINT in Snowflake is an alias for NUMBER(38,0)  [See note on this conversion below.] |
| NUMERIC | NUMERIC | ​Snowflake’s NUMERIC is synonymous with NUMBER |

**NOTE:**

* For the conversion of integer data types (INT, SMALLINT, BIGINT, TINYINT), each is converted to the alias in Snowflake with the same name. Each of those aliases is actually converted to NUMBER(38,0), a data type that is considerably larger than the integer datatype. Below is a comparison of the range of values that can be present in each data type:

  + Snowflake NUMBER(38,0): -99999999999999999999999999999999999999 to +99999999999999999999999999999999999999
  + SQLServer TINYINT: 0 to 255
  + SQLServer INT: -2^31 (-2,147,483,648) to 2^31-1 (2,147,483,647)
  + SQLServer BIGINT: -2^63 (-9,223,372,036,854,775,808) to 2^63-1 (9,223,372,036,854,775,807)
  + SQLServer SMALLINT: -2^15 (-32,768) to 2^15-1 (32,767)
* For Money and Smallmoney: ​

  + Currency or monetary data does not need to be enclosed in single quotation marks ( ‘ ). It is important to remember that while you can specify monetary values preceded by a currency symbol, SQL Server does not store any currency information associated with the symbol, it only stores the numeric value.
  + Please take care on the translations for the DMLs

## Date and time[¶](#date-and-time "Link to this heading")

| T-SQL | Snowflake | Notes |
| --- | --- | --- |
| DATE | DATE | ​SQLServer accepts range from 0001-01-01 to 9999-12-31 |
| DATETIME2 | TIMESTAMP\_NTZ(7)​ | Snowflake’s DATETIME is an alias for TIMESTAMP\_NTZ |
| DATETIME | TIMESTAMP\_NTZ(3) | Snowflake’s DATETIME is an alias for TIMESTAMP\_NTZ​ |
| DATETIMEOFFSET | TIMESTAMP\_TZ(7) | Snowflake’s timestamp precision ranges from 0 to 9 (*this value’s the default*)  Snowflake’s operations are performed in the current session’s time zone, controlled by the TIMEZONE session parameter |
| SMALLDATETIME | TIMESTAMP\_NTZ | Snowflake’s DATETIME truncates the TIME information  i.e. 1955-12-13 12:43:10 is saved as 1955-12-13 |
| TIME | TIME | ​This data type behaves equally on both systems.  Range 00:00:00.0000000 through 23:59:59.9999999 |
| TIMESTAMP | TIMESTAMP | This is an user defined data type in TSQL so it’s converted to it’s equivalent in snowflake Timestamp. |

## Character strings[¶](#character-strings "Link to this heading")

| T-SQL | Snowflake | Notes |
| --- | --- | --- |
| CHAR | CHAR | ​SQLServer’s max string size in bytes is 8000 whereas Snowflake is 167772161. |
| TEXT​ | TEXT |  |
| VARCHAR​ | VARCHAR | SQLServer’s max string size in bytes is 8000 whereas Snowflake is 167772161. SQLServer’s VARCHAR(MAX) has no equivalent in SnowFlake, it is converted to VARCHAR to take the largest possible size by default. |

## Unicode character strings[¶](#unicode-character-strings "Link to this heading")

| T-SQL | Snowflake | Notes |
| --- | --- | --- |
| NCHAR | NCHAR | Synonymous with VARCHAR except default length is VARCHAR(1). |
| NTEXT | TEXT | Snowflake use TEXT data type as a synonymous with VARCHAR  ​SQLServer’s NTEXT(MAX) has no equivalent in SnowFlake, it is converted to VARCHAR to take the largest possible size by default. |
| NVARCHAR | VARCHAR | Snowflake use this data type as a synonymous with VARCHAR  ​SQLServer’s NVARCHAR(MAX) has no equivalent in SnowFlake, it is converted to VARCHAR to take the largest possible size by default. |

## Binary strings[¶](#binary-strings "Link to this heading")

| T-SQL | Snowflake | Notes |
| --- | --- | --- |
| BINARY | ​BINARY | In Snowflake the maximum length is 8 MB (8,388,608 bytes) and length is always measured in terms of bytes. |
| VARBINARY | VARBINARY | Snowflake use this data type as a synonymous with BINARY.  Snowflake often represents each byte as 2 hexadecimal characters |
| IMAGE | VARBINARY | ​Snowflake use this data type as a synonymous with BINARY.  Snowflake often represents each byte as 2 hexadecimal characters |

## Other data types[¶](#other-data-types "Link to this heading")

| T-SQL | Snowflake | Notes |
| --- | --- | --- |
| CURSOR | *\*to be defined* | Not supported by Snowflake.  Translate into Cursor helpers |
| HIERARCHYID | *\*to be defined* | Not supported by Snowflake |
| SQL\_VARIANT | VARIANT | Maximum size of 16 MB compressed.  A value of any data type can be implicitly cast to a VARIANT value |
| GEOMETRY | *\*to be defined* | Not supported by Snowflake |
| GEOGRAPHY | GEOGRAPHY | The objects store in Snowflake’s GEOGRAPHY data type must be WKT / WKB / EWKT / EWKB / GeoJSON geospatial objects to support LineString and Polygon objects |
| TABLE | *\*to be defined* | Not supported by Snowflake |
| ROWVERSION | *\*to be defined* | Not supported by Snowflake |
| UNIQUEIDENTIFIER | VARCHAR | ​​Snowflake use STRING type as a synonymous with VARCHAR. Because of conversion Snowflake often represents each byte as 2 hexadecimal characters |
| XML | VARIANT | ​Snowflake use VARIANT data type as a synonymous with XML |
| SYSNAME | VARCHAR(128) | NOT NULL constraint added to the column definition |

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
6. [Other data types](#other-data-types)