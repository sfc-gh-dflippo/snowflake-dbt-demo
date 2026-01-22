---
auto_generated: true
description: Snowflake supports most basic SQL data types (with some restrictions)
  for use in columns, local variables, expressions, parameters, and any other appropriate/suitable
  locations.
last_scraped: '2026-01-14T16:54:11.794272+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/vertica/vertica-data-types
title: SnowConvert AI - Vertica - Data types | Snowflake Documentation
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
          + [Hive-Spark-Databricks SQL](../hive/README.md)
          + [Redshift](../redshift/README.md)
          + [PostgreSQL-Greenplum-Netezza](../postgres/README.md)
          + [BigQuery](../bigquery/README.md)
          + [Vertica](README.md)

            - [CREATE TABLE](vertica-create-table.md)
            - [CREATE VIEW](vertica-create-view.md)
            - [Built-in Functions](vertica-built-in-functions.md)
            - [Data Types](vertica-data-types.md)
            - [Operators](vertica-operators.md)
            - [Predicates](vertica-predicates.md)
            - [Identifier differences between Vertica and Snowflake](vertica-identifier-between-vertica-and-snowflake.md)
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)Translation References[Vertica](README.md)Data Types

# SnowConvert AI - Vertica - Data types[¶](#snowconvert-ai-vertica-data-types "Link to this heading")

Snowflake supports most basic [SQL data types](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types) (with some restrictions) for use in columns, local variables, expressions, parameters, and any other appropriate/suitable locations.

## Binary Data Type[¶](#binary-data-type "Link to this heading")

| Vertica | Snowflake |
| --- | --- |
| [BINARY](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/binary-data-types-binary-and-varbinary/) | [BINARY](https://docs.snowflake.com/en/sql-reference/data-types-text#binary) |
| [VARBINARY (synonyms: BYTEA, RAW, BINARY VARYING)](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/binary-data-types-binary-and-varbinary/) | [BINARY (synonyms: VARBINARY, BINARY VARYING)](https://docs.snowflake.com/en/sql-reference/data-types-text#binary) |
| [LONG VARBINARY](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/long-data-types/) | [BINARY](https://docs.snowflake.com/en/sql-reference/data-types-text#binary)    *Notes: Vertica’s `LONG VARBINARY` supports up to 32,000,000 bytes (**~30.5MB)**, while Snowflake’s `BINARY` is limited to (8,388,608 bytes) **8MB**. This size difference means you might need an alternative solution for mapping larger `LONG VARBINARY` data.* |

## Boolean Data Type[¶](#boolean-data-type "Link to this heading")

| Vertica | Snowflake |
| --- | --- |
| [BOOLEAN](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/boolean-data-type/) | [BOOLEAN](https://docs.snowflake.com/en/sql-reference/data-types-logical#boolean) |

## Character Data Type[¶](#character-data-type "Link to this heading")

| Vertica | Snowflake |
| --- | --- |
| [CHAR](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/character-data-types-char-and-varchar/) | [CHAR](https://docs.snowflake.com/en/sql-reference/data-types-text#char-character-nchar) |
| [VARCHAR](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/character-data-types-char-and-varchar/) | [VARCHAR](https://docs.snowflake.com/en/sql-reference/data-types-text#varchar) |
| [LONG VARCHAR](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/long-data-types/) | [VARCHAR](https://docs.snowflake.com/en/sql-reference/data-types-text#varchar)    *Notes: Vertica’s `LONG VARCHAR` supports up to 32,000,000 bytes (**~30.5MB)**, while Snowflake’s `VARCHAR` is limited to 16,777,216 bytes (**16MB)**. This size difference means you might need an alternative solution for mapping larger `LONG VARCHAR` data.* |

## Date/Time Data Type[¶](#date-time-data-type "Link to this heading")

| Vertica | Snowflake |
| --- | --- |
| [DATE](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/datetime-data-types/date/) | [DATE](https://docs.snowflake.com/en/sql-reference/data-types-datetime#label-datatypes-date)    *Notes: Be aware of* [*Snowflake’s*](https://docs.snowflake.com/en/sql-reference/data-types-datetime#data-types) *recommended year range (1582-9999).* |
| [TIME](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/datetime-data-types/timetimetz/) | [TIME](https://docs.snowflake.com/en/sql-reference/data-types-datetime#label-datatypes-time) |
| [TIME WITH TIMEZONE (TIMETZ)](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/datetime-data-types/timestamptimestamptz/) | [TIME](https://docs.snowflake.com/en/sql-reference/data-types-datetime#label-datatypes-time)    *Notes: TIME data type in Snowflake does not persist this timezone attribute.* [*`SSC-FDM-0005`*](../general/technical-documentation/issues-and-troubleshooting/functional-difference/general/ssc-fdm-0005.md) *is added.* |
| [TIMESTAMP](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/datetime-data-types/timestamptimestamptz/) | [TIMESTAMP](https://docs.snowflake.com/en/sql-reference/data-types-datetime#timestamp) |
| [DATETIME](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/datetime-data-types/datetime/) | [DATETIME](https://docs.snowflake.com/en/sql-reference/data-types-datetime#datetime) |
| [SMALLDATETIME](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/datetime-data-types/smalldatetime/) | [TIMESTAMP\_NTZ](https://docs.snowflake.com/en/sql-reference/data-types-datetime#timestamp-ltz-timestamp-ntz-timestamp-tz) |
| [TIMESTAMP WITH TIMEZONE (TIMESTAMPTZ)](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/datetime-data-types/timestamptimestamptz/) | [TIMESTAMP\_TZ](https://docs.snowflake.com/en/sql-reference/data-types-datetime#timestamp-ltz-timestamp-ntz-timestamp-tz) |
| [TIMESTAMP WITHOUT TIME ZONE](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/datetime-data-types/timestamptimestamptz/) | [TIMESTAMP\_NTZ](https://docs.snowflake.com/en/sql-reference/data-types-datetime#timestamp-ltz-timestamp-ntz-timestamp-tz) |

## Approximate Numeric Data Type[¶](#approximate-numeric-data-type "Link to this heading")

| Vertica | Snowflake |
| --- | --- |
| [DOUBLE PRECISION](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/numeric-data-types/double-precision-float/) | [DOUBLE PRECISION](https://docs.snowflake.com/en/sql-reference/data-types-numeric#double-double-precision-real) |
| [FLOAT](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/numeric-data-types/double-precision-float/) | [FLOAT](https://docs.snowflake.com/en/sql-reference/data-types-numeric#float-float4-float8) |
| [FLOAT8](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/numeric-data-types/double-precision-float/) | [FLOAT8](https://docs.snowflake.com/en/sql-reference/data-types-numeric#float-float4-float8) |
| [REAL](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/numeric-data-types/double-precision-float/) | [REAL](https://docs.snowflake.com/en/sql-reference/data-types-numeric#double-double-precision-real) |

## Exact Numeric Data Type[¶](#exact-numeric-data-type "Link to this heading")

| Vertica | Snowflake |
| --- | --- |
| [INTEGER](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/numeric-data-types/integer/) | [INTEGER](https://docs.snowflake.com/en/sql-reference/data-types-numeric#int-integer-bigint-smallint-tinyint-byteint) |
| [INT](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/numeric-data-types/integer/) | [INT](https://docs.snowflake.com/en/sql-reference/data-types-numeric#int-integer-bigint-smallint-tinyint-byteint) |
| [BIGINT](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/numeric-data-types/integer/) | [BIGINT](https://docs.snowflake.com/en/sql-reference/data-types-numeric#int-integer-bigint-smallint-tinyint-byteint) |
| [INT8](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/numeric-data-types/integer/) | [INTEGER](https://docs.snowflake.com/en/sql-reference/data-types-numeric#int-integer-bigint-smallint-tinyint-byteint) |
| [SMALLINT](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/numeric-data-types/integer/) | [SMALLINT](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/numeric-data-types/integer/) |
| [TINYINT](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/numeric-data-types/integer/) | [TINYINT](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/numeric-data-types/integer/) |
| [DECIMAL](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/numeric-data-types/numeric/) | [DECIMAL](https://docs.snowflake.com/en/sql-reference/data-types-numeric#decimal-dec-numeric) |
| [NUMERIC](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/numeric-data-types/numeric/) | [NUMERIC](https://docs.snowflake.com/en/sql-reference/data-types-numeric#decimal-dec-numeric) |
| [NUMBER](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/numeric-data-types/numeric/) | [NUMBER](https://docs.snowflake.com/en/sql-reference/data-types-numeric#number) |
| [MONEY](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/numeric-data-types/numeric/) | [NUMERIC](https://docs.snowflake.com/en/sql-reference/data-types-numeric#decimal-dec-numeric) |

## Spatial Data Type[¶](#spatial-data-type "Link to this heading")

| Vertica | Snowflake |
| --- | --- |
| [GEOMETRY](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/spatial-data-types/) | [GEOMETRY](https://docs.snowflake.com/en/sql-reference/data-types-geospatial#label-data-types-geometry) |
| [GEOGRAPHY](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/spatial-data-types/) | [GEOGRAPHY](https://docs.snowflake.com/en/sql-reference/data-types-geospatial#label-data-types-geography) |

## UUID Data Type[¶](#uuid-data-type "Link to this heading")

| Vertica | Snowflake |
| --- | --- |
| [UUID](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/uuid-data-type/) | [VARCHAR(36)](https://docs.snowflake.com/en/sql-reference/data-types-text#varchar)    *Notes: Snowflake doesn’t have a native UUID data type. Instead, UUIDs are usually stored as either **VARCHAR(36)** (for string format) or **BINARY(16)** (for raw byte format).*  *You can generate RFC 4122-compliant UUIDs in Snowflake using the built-in* [***`UUID_STRING()`***](https://docs.snowflake.com/en/sql-reference/functions/uuid_string) *function.* |

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

1. [Binary Data Type](#binary-data-type)
2. [Boolean Data Type](#boolean-data-type)
3. [Character Data Type](#character-data-type)
4. [Date/Time Data Type](#date-time-data-type)
5. [Approximate Numeric Data Type](#approximate-numeric-data-type)
6. [Exact Numeric Data Type](#exact-numeric-data-type)
7. [Spatial Data Type](#spatial-data-type)
8. [UUID Data Type](#uuid-data-type)