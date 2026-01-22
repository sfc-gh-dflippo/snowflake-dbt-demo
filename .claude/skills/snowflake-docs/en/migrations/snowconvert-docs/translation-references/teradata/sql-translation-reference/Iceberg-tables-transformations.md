---
auto_generated: true
description: This section covers the transformation of tables into Snowflake-managed
  Iceberg tables, performed by SnowConvert AI when the conversion setting Table Translation
  is used.
last_scraped: '2026-01-14T16:53:50.061588+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/teradata/sql-translation-reference/Iceberg-tables-transformations
title: SnowConvert AI - Teradata - Iceberg Tables Transformations | Snowflake Documentation
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

[Guides](../../../../../guides/README.md)[Migrations](../../../../README.md)Tools[SnowConvert AI](../../../overview.md)Translation References[Teradata](../README.md)[Sql Translation Reference](README.md)Iceberg Table Transformations

# SnowConvert AI - Teradata - Iceberg Tables Transformations[¶](#snowconvert-ai-teradata-iceberg-tables-transformations "Link to this heading")

This section covers the transformation of tables into Snowflake-managed Iceberg tables, performed by SnowConvert AI when the conversion setting [Table Translation](../../../general/getting-started/running-snowconvert/conversion/teradata-conversion-settings.html#table-translation) is used.

## Temporary tables[¶](#temporary-tables "Link to this heading")

The temporary option is not supported in Iceberg tables, they will be preserved as temporary.

### Teradata[¶](#teradata "Link to this heading")

```
CREATE VOLATILE TABLE myTable
(
  column1 NUMBER(15,0)
);
```

Copy

### Snowflake[¶](#snowflake "Link to this heading")

```
CREATE OR REPLACE TEMPORARY TABLE myTable
(
 column1 NUMBER(15,0)
)
;
```

Copy

## Other tables[¶](#other-tables "Link to this heading")

Other table types are going to be transformed into Iceberg tables.

### Teradata[¶](#id1 "Link to this heading")

```
CREATE TABLE myTable
(
  column1 NUMBER(15,0)
);
```

Copy

### Snowflake[¶](#id2 "Link to this heading")

```
CREATE OR REPLACE ICEBERG TABLE myTable (
  column1 NUMBER(15, 0)
)
CATALOG = 'SNOWFLAKE'
;
```

Copy

## Data types[¶](#data-types "Link to this heading")

The following column data type conversions are applied to comply with the Iceberg tables type requirements and restrictions.

Note

Data types in the first column are the **Snowflake** data types that would normally be created if the table target is not Iceberg, while second column shows the data type generated for Iceberg tables.

| Original target type | New target type |
| --- | --- |
| TIME(X)  TIMESTAMP(X)  DATETIME(X)  TIMESTAMP\_LTZ(X)  TIMESTAMP\_NTZ(X)  TIME  TIMESTAMP  DATETIME  TIMESTAMP\_LTZ  TIMESTAMP\_NTZ  where X != 6 | TIME(6)  TIMESTAMP(6)  DATETIME(6)  TIMESTAMP\_LTZ(6)  TIMESTAMP\_NTZ(6)  TIME(6)  TIMESTAMP(6)  DATETIME(6)  TIMESTAMP\_LTZ(6)  TIMESTAMP\_NTZ(6) |
| VARCHAR(X)  STRING(X)  TEXT(X)  NVARCHAR(X)  NVARCHAR2(X)  CHAR VARYING(X)  NCHAR VARYING(X) | VARCHAR  STRING  TEXT  NVARCHAR  NVARCHAR2  CHAR VARYING  NCHAR VARYING |
| CHAR[(n)]  CHARACTER[(n)]  NCHAR[(n)] | VARCHAR  VARCHAR  VARCHAR |
| NUMBER  DECIMAL  DEC  NUMERIC  INT  INTEGER  BIGINT  SMALLINT  TINYINT  BYTEINT | NUMBER(38,0)  DECIMAL(38,0)  DEC(38,0)  NUMERIC(38,0)  NUMBER(38,0)  NUMBER(38,0)  NUMBER(38,0)  NUMBER(38,0)  NUMBER(38,0)  NUMBER(38,0) |
| FLOAT  FLOAT4  FLOAT8 | DOUBLE  DOUBLE  DOUBLE |
| VARBINARY[(n)] | BINARY[(n)] |

## PARTITION BY[¶](#partition-by "Link to this heading")

The following PARTITION BY cases are supported:

### PARTITION BY name[¶](#partition-by-name "Link to this heading")

Left as is.

#### Teradata[¶](#id3 "Link to this heading")

```
CREATE TABLE myTable
(
  customerName VARCHAR(30),
  areaCode INTEGER
)
PARTITION BY areaCode;
```

Copy

#### Snowflake[¶](#id4 "Link to this heading")

```
CREATE OR REPLACE ICEBERG TABLE myTable (
  customerName VARCHAR,
  areaCode NUMBER(38, 0)
)
PARTITION BY (areaCode)
CATALOG = 'SNOWFLAKE'
;
```

Copy

### PARTITION BY CASE\_N (equality over single column)[¶](#partition-by-case-n-equality-over-single-column "Link to this heading")

When the CASE\_N function follows this pattern:

```
PARTITION BY CASE_N(
  column_name = value1,
  column_name = value2,
  ...
  column_name = valueN)
```

Copy

It will be transformed to a PARTITION BY column\_name.

#### Teradata[¶](#id5 "Link to this heading")

```
CREATE TABLE myTable
(
  customerName VARCHAR(30),
  weekDay VARCHAR(20)
)
PARTITION BY CASE_N(
weekDay =  'Sunday',
weekDay =  'Monday',
weekDay =  'Tuesday',
weekDay =  'Wednesday',
weekDay =  'Thursday',
weekDay =  'Friday',
weekDay =  'Saturday',
 NO CASE OR UNKNOWN);
```

Copy

#### Snowflake[¶](#id6 "Link to this heading")

```
CREATE OR REPLACE ICEBERG TABLE myTable (
  customerName VARCHAR,
  weekDay VARCHAR
)
PARTITION BY (weekDay)
CATALOG = 'SNOWFLAKE'
;
```

Copy

### PARTITION BY RANGE\_N[¶](#partition-by-range-n "Link to this heading")

PARTITION BY RANGE\_N is transformed when it matches one of these patterns:

#### Numeric range[¶](#numeric-range "Link to this heading")

Pattern:

```
RANGE_N(columnName BETWEEN x AND y EACH z) -- x, y and z must be numeric constants.
```

Copy

This case will be changed with a BUCKET partition transform.

##### Teradata[¶](#id7 "Link to this heading")

```
CREATE TABLE myTable
(
  customerName VARCHAR(30),
  totalPurchases INTEGER
)
PARTITION BY RANGE_N(totalPurchases BETWEEN 5 AND 200 EACH 10);
```

Copy

##### Snowflake[¶](#id8 "Link to this heading")

```
CREATE OR REPLACE ICEBERG TABLE myTable (
  customerName VARCHAR,
  totalPurchases NUMBER(38, 0)
)
PARTITION BY (BUCKET(20, totalPurchases))
CATALOG = 'SNOWFLAKE'
;
```

Copy

#### Datetime range[¶](#datetime-range "Link to this heading")

Pattern:

```
RANGE_N(columnName BETWEEN date_constant AND date_constant EACH interval_constant) -- Interval qualifier must be YEAR, MONTH, DAY or HOUR
```

Copy

This case will be changed with the YEAR, MONTH, DAY or HOUR partition transforms.

##### Teradata[¶](#id9 "Link to this heading")

```
CREATE TABLE myTable
(
  customerName VARCHAR(30),
  purchaseDate DATE
)
PARTITION BY RANGE_N(purchaseDate BETWEEN DATE '2000-01-01' AND '2100-12-31' EACH INTERVAL '1' MONTH);
```

Copy

##### Snowflake[¶](#id10 "Link to this heading")

```
CREATE OR REPLACE ICEBERG TABLE myTable (
  customerName VARCHAR,
  purchaseDate DATE
)
PARTITION BY (MONTH(purchaseDate))
CATALOG = 'SNOWFLAKE'
;
```

Copy

## Known Issues[¶](#known-issues "Link to this heading")

### 1. Unsupported data types[¶](#unsupported-data-types "Link to this heading")

Current Snowflake support for Iceberg tables does not allow data types like VARIANT or GEOGRAPHY to be used, tables with these types will be marked with an EWI.

### 2. Unsupported PARTITION BY cases[¶](#unsupported-partition-by-cases "Link to this heading")

PARTITION BY cases different than the ones shown in this documentation will not be transformed, instead, the PARTITION BY clause will be commented out with a PRF.

## Related EWIs[¶](#related-ewis "Link to this heading")

1. [SSC-EWI-0115](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0115): Iceberg table contains unsupported datatypes
2. [SSC-PRF-0010](../../../general/technical-documentation/issues-and-troubleshooting/performance-review/generalPRF.html#ssc-prf-0010): Partition by removed, at least one of the specified expressions have no iceberg partition transform equivalent

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

1. [Temporary tables](#temporary-tables)
2. [Other tables](#other-tables)
3. [Data types](#data-types)
4. [PARTITION BY](#partition-by)
5. [Known Issues](#known-issues)
6. [Related EWIs](#related-ewis)