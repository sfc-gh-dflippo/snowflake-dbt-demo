---
auto_generated: true
description: This section shows equivalents between data types in Oracle and Snowflake,
  as well as some notes on arithmetic differences.
last_scraped: '2026-01-14T16:53:13.368942+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/oracle/basic-elements-of-oracle-sql/data-types/README
title: SnowConvert AI - Oracle - Data Types | Snowflake Documentation
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
          + [Oracle](../../README.md)

            - [Sample Data](../../sample-data.md)
            - Basic Elements of Oracle SQL

              - [Literals](../literals.md)
              - [Data Types](README.md)

                * [Any types](any-types.md)
                * [Built-in types](oracle-built-in-data-types.md)
                * [ROWID types](rowid-types.md)
                * [Spatial types](spatial-types.md)
                * [User Defined types](user-defined-types.md)
                * [XML types](xml-types.md)
            - [Pseudocolumns](../../pseudocolumns.md)
            - [Built-in Functions](../../functions/README.md)
            - [Built-in Packages](../../built-in-packages.md)
            - [SQL Queries and Subqueries](../../sql-queries-and-subqueries/selects.md)
            - [SQL Statements](../../sql-translation-reference/README.md)
            - [PL/SQL to Snowflake Scripting](../../pl-sql-to-snowflake-scripting/README.md)
            - [PL/SQL to Javascript](../../pl-sql-to-javascript/README.md)
            - [SQL Plus](../../sql-plus.md)
            - [Wrapped Objects](../../wrapped-objects.md)
            - ETL And BI Repointing

              - [Power BI Oracle Repointing](../../etl-bi-repointing/power-bi-oracle-repointing.md)
          + [SQL Server-Azure Synapse](../../../transact/README.md)
          + [Sybase IQ](../../../sybase/README.md)
          + [Hive-Spark-Databricks SQL](../../../hive/README.md)
          + [Redshift](../../../redshift/README.md)
          + [PostgreSQL-Greenplum-Netezza](../../../postgres/README.md)
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

[Guides](../../../../../../guides/README.md)[Migrations](../../../../../README.md)Tools[SnowConvert AI](../../../../overview.md)Translation References[Oracle](../../README.md)Basic Elements of Oracle SQLData Types

# SnowConvert AI - Oracle - Data Types[¶](#snowconvert-ai-oracle-data-types "Link to this heading")

This section shows equivalents between data types in Oracle and Snowflake, as well as some notes on arithmetic differences.

| **Oracle** | **Snowflake** |
| --- | --- |
| [ANSI Data Types](#ansi-data-types) | *\*Go to the link to get more information* |
| [BFILE](oracle-built-in-data-types.html#bfile-data-type) | VARCHAR |
| [BINARY\_DOUBLE](oracle-built-in-data-types.html#binary-double) | FLOAT |
| [BINARY\_FLOAT](oracle-built-in-data-types.html#binary-float) | FLOAT |
| [BLOB](oracle-built-in-data-types.html#blob-data-type) | BINARY |
| [CHAR (N)](oracle-built-in-data-types.html#char-data-type) | CHAR (N) |
| [CLOB](oracle-built-in-data-types.html#clob-data-type) | VARCHAR |
| [DATE](oracle-built-in-data-types.html#date-data-type) | TIMESTAMP |
| [FLOAT](oracle-built-in-data-types.html#float-data-type) | FLOAT |
| [INTERVAL YEAR TO MONTH](oracle-built-in-data-types.html#interval-year-to-month-data-type) | VARCHAR(20) |
| [INTERVAL DAY TO SECOND](oracle-built-in-data-types.html#interval-day-to-second-data-type) | VARCHAR(20) |
| [JSON](oracle-built-in-data-types.html#json-data-type) | VARIANT |
| [LONG](oracle-built-in-data-types.html#long-data-type) | VARCHAR |
| [LONG RAW](oracle-built-in-data-types.html#raw-and-long-raw-data-types) | BINARY |
| [NCHAR (N)](oracle-built-in-data-types.html#nchar-data-type) | NCHAR (N) |
| [NCLOB](oracle-built-in-data-types.html#nclob-data-type) | VARCHAR |
| [NUMBER(p, s)](oracle-built-in-data-types.html#number-data-type) | NUMBER(p, s) |
| [NVARCHAR2 (N)](oracle-built-in-data-types.html#nvarchar2-data-type) | VARCHAR (N) |
| [RAW](oracle-built-in-data-types.html#raw-and-long-raw-data-types) | BINARY |
| [ROWID](rowid-types) | VARCHAR(18) |
| [VARCHAR2 (N)](oracle-built-in-data-types.html#varchar2-data-type) | VARCHAR (N) |
| [SDO\_GOMETRY](spatial-types.html#sdo-geometry) | Currently not supported |
| [SDO\_TOPO\_\_\_GEOMETRY](spatial-types.html#sdo-topo-geometry) | *\*to be defined* |
| [SDO\_GEORASTER](spatial-types.html#sdo-georaster) | *\*to be defined* |
| [SYS.ANYDATA](any-types.html#anydata) | VARIANT |
| [SYS.ANYDATASET](any-types.html#anydataset) | *\*to be defined* |
| [SYS.ANYTYPE](any-types.html#anytype) | *\*to be defined* |
| [TIMESTAMP](oracle-built-in-data-types.html#timestamp-data-type) | TIMESTAMP |
| [TIMESTAMP WITH TIME ZONE](oracle-built-in-data-types.html#timestamp-with-time-zone-data-type) | TIMESTAMP\_TZ |
| [TIMESTAMP WITH LOCAL TIME ZONE](oracle-built-in-data-types.html#timestamp-with-local-time-zone-data-type) | TIMESTAMP\_LTZ |
| [URITYPE](xml-types.html#uri-data-types) | *\*to be defined* |
| [UROWID](rowid-types.html#urowid-data-type) | VARCHAR(18) |
| [VARCHAR](oracle-built-in-data-types.html#varchar-data-type) | VARCHAR |
| [VARCHAR2](oracle-built-in-data-types.html#varchar2-data-type) | VARCHAR |
| [XMLType](xml-types.html#xmltype) | VARIANT |

## Notes on arithmetic operations[¶](#notes-on-arithmetic-operations "Link to this heading")

Please be aware that every operation performed on numerical datatypes is internally stored as a Number. Furthermore, depending on the operation performed it is possible to incur an error related to how intermediate values are stored within Snowflake, for more information please check this post on [Snowflake’s post on intermediate numbers in Snowflake](https://community.snowflake.com/s/question/0D50Z00008HhSHCSA3/sql-compilation-error-invalid-intermediate-datatype-number7148).

## ANSI Data Types[¶](#ansi-data-types "Link to this heading")

### Description[¶](#description "Link to this heading")

> SQL statements that create tables and clusters can also use ANSI data types and data types from the IBM products SQL/DS and DB2. Oracle recognizes the ANSI or IBM data type name that differs from the Oracle Database data type name. It converts the data type to the equivalent Oracle data type, records the Oracle data type as the name of the column data type, and stores the column data in the Oracle data type based on the conversions shown in the tables that follow. ([Oracle Language Reference ANSI, DB2, and SQL/DS Data Types](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/Data-Types.html#GUID-0BC16006-32F1-42B1-B45E-F27A494963FF)).

When creating a new table, Oracle and Snowflake handle some data types as synonyms and aliases and transform them into the default data type. As shown in the next table:

| ANSI | ORACLE | SNOWFLAKE |
| --- | --- | --- |
| CHARACTER (n) | CHAR (n) | VARCHAR |
| CHAR (n) | CHAR (n) | VARCHAR |
| CHARACTER VARYING (n) | VARCHAR2 (n) | VARCHAR |
| CHAR VARYING (n) | VARCHAR2 (n) | VARCHAR |
| NATIONAL CHARACTER (n) | NCHAR (n) | VARCHAR\* |
| NATIONAL CHAR (n) | NCHAR (n) | VARCHAR\* |
| NCHAR (n) | NCHAR (n) | VARCHAR |
| NATIONAL CHARACTER VARYING (n) | NVARCHAR2 (n) | VARCHAR\* |
| NATIONAL CHAR VARYING (n) | NVARCHAR2 (n) | VARCHAR\* |
| NCHAR VARYING (n) | NVARCHAR2 (n) | NUMBER (p, s) |
| NUMERIC [(p, s)] | NUMBER (p, s) | NUMBER (p, s) |
| DECIMAL [(p, s)] | NUMBER (p, s) | NUMBER (38) |
| INTEGER | NUMBER (38) | NUMBER (38) |
| INT | NUMBER (38) | NUMBER (38) |
| SMALLINT | NUMBER (38) | NUMBER (38) |
| FLOAT | FLOAT (126) | DOUBLE |
| DOUBLE PRECISION | FLOAT (126) | DOUBLE |
| REAL | FLOAT (63) | DOUBLE |

To get more information about the translation specification of the Oracle data types, go to [Oracle Built-in Data Types](oracle-built-in-data-types).

Note

VARCHAR\*: Almost all the ANSI datatypes compile in Snowflake, but those marked with an asterisk, are manually converted to VARCHAR.

### Known Issues[¶](#known-issues "Link to this heading")

No issues were found.

### Related EWIs[¶](#related-ewis "Link to this heading")

EWIs related to these data types are specified in the transformation of the [Oracle Built-in data types.](oracle-built-in-data-types)

## Data Type Customization[¶](#data-type-customization "Link to this heading")

SnowConvert AI enables Data Type Customization to specify rules for data type transformation based on data type origin and column name. This feature allows you to personalize data type conversions and set precision values more accurately during migration.

For complete documentation on configuring data type customization, including JSON structure, configuration options, and priority rules, see [Data type mappings](../../../../general/getting-started/running-snowconvert/conversion/oracle-conversion-settings.html#data-type-mappings) in the Oracle Conversion Settings documentation.

### NUMBER to DECFLOAT Transformation[¶](#number-to-decfloat-transformation "Link to this heading")

SnowConvert AI supports transforming Oracle `NUMBER` columns to Snowflake `DECFLOAT` data type. This is useful when you need to preserve the exact decimal precision of numeric values during migration.

When a `NUMBER` column is configured to be transformed to `DECFLOAT`:

1. The column data type in `CREATE TABLE` statements is transformed to `DECFLOAT`
2. Numeric literals in `INSERT` statements that target `DECFLOAT` columns are automatically wrapped with `CAST(... AS DECFLOAT)` to ensure proper data type handling
3. Column references in `INSERT ... SELECT` statements are also cast appropriately

#### Example[¶](#example "Link to this heading")

##### Oracle[¶](#oracle "Link to this heading")

```
CREATE TABLE products (
    product_id NUMBER(10),
    price NUMBER(15, 2)
);

INSERT INTO products VALUES (1, 99.99);
```

Copy

##### Snowflake (with DECFLOAT customization for price column)[¶](#snowflake-with-decfloat-customization-for-price-column "Link to this heading")

```
CREATE OR REPLACE TABLE products (
    product_id NUMBER(10),
    price DECFLOAT
);

INSERT INTO products VALUES (1, CAST(99.99 AS DECFLOAT));
```

Copy

Note

The TypeMappings report (TypeMappings.csv) provides a detailed view of all data type transformations applied during conversion. See [TypeMappings Report](../../../../general/getting-started/running-snowconvert/review-results/reports/type-mappings-report) for more information.

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

1. [Notes on arithmetic operations](#notes-on-arithmetic-operations)
2. [ANSI Data Types](#ansi-data-types)
3. [Data Type Customization](#data-type-customization)