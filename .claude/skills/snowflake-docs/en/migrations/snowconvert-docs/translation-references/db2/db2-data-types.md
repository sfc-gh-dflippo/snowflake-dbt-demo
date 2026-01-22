---
auto_generated: true
description: Specifies the data type of the column
last_scraped: '2026-01-14T16:53:07.853879+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/db2/db2-data-types
title: SnowConvert AI - IBM DB2 - Data Types | Snowflake Documentation
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
          + [Vertica](../vertica/README.md)
          + [IBM DB2](README.md)

            - [CONTINUE HANDLER](db2-continue-handler.md)
            - [EXIT HANDLER](db2-exit-handler.md)
            - [CREATE TABLE](db2-create-table.md)
            - [CREATE VIEW](db2-create-view.md)
            - [CREATE PROCEDURE](db2-create-procedure.md)
            - [CREATE FUNCTION](db2-create-function.md)
            - [Data Types](db2-data-types.md)
            - [SELECT](db2-select-statement.md)
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)Translation References[IBM DB2](README.md)Data Types

# SnowConvert AI - IBM DB2 - Data Types[¶](#snowconvert-ai-ibm-db2-data-types "Link to this heading")

## Description[¶](#description "Link to this heading")

> Specifies the data type of the column

Click [here](https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-table#sdx-synid_built-in-type) to navigate to the IBM DB2 documentation page for this syntax.

## Transformations[¶](#transformations "Link to this heading")

The following table shows the transformation from Db2 to Snowflake.

| Db2 | Snowflake | EWI |
| --- | --- | --- |
| SMALLINT | SMALLINT |  |
| INTEGER | INTEGER |  |
| INT | INT |  |
| BIGINT | BIGINT |  |
| DECIMAL | DECIMAL |  |
| DEC | DEC |  |
| NUMERIC | NUMERIC |  |
| NUM | NUMERIC |  |
| FLOAT | FLOAT |  |
| REAL | REAL |  |
| DOUBLE | DOUBLE |  |
| DECFLOAT | DECFLOAT |  |
| CHARACTER | CHARACTER |  |
| CHAR | CHAR |  |
| VARCHAR | VARCHAR |  |
| CHARACTER VARYING | CHARACTER VARYING |  |
| CHAR VARYING | CHAR VARYING |  |
| CLOB | VARCHAR |  |
| CHARACTER LARGE OBJECT | VARCHAR |  |
| CHAR LARGE OBJECT | VARCHAR |  |
| CLOB | VARCHAR |  |
| CHARACTER LARGE OBJECT | VARCHAR |  |
| CHAR LARGE OBJECT | VARCHAR |  |
| GRAPHIC | BINARY |  |
| VARGRAPHIC | BINARY |  |
| DBCLOB | VARCHAR |  |
| NCHAR | NCHAR |  |
| NATIONAL CHAR | NCHAR |  |
| NATIONAL CHARACTER | NCHAR |  |
| NVARCHAR | NVARCHAR |  |
| NCHAR VARYING | NCHAR VARYING |  |
| NATIONAL CHAR VARYING | NCHAR VARYING |  |
| NATIONAL CHARACTER VARYING | NCHAR VARYING |  |
| NCLOB | VARCHAR |  |
| NCHAR LARGE OBJECT | VARCHAR |  |
| NATIONAL CHARACTER LARGE OBJECT | VARCHAR |  |
| BINARY | BINARY |  |
| VARBINARY | VARBINARY |  |
| BINARY VARYING | BINARY VARYING |  |
| BLOB | BINARY |  |
| BINARY LARGE OBJECT | BINARY |  |
| DATE | DATE |  |
| TIME | TIME |  |
| TIMESTAMP | TIMESTAMP |  |
| XML | VARIANT | [SSC-EWI-0036](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0036) |
| BOOLEAN | BOOLEAN |  |

## Sample Source Patterns[¶](#sample-source-patterns "Link to this heading")

### IBM DB2[¶](#ibm-db2 "Link to this heading")

```
 CREATE TABLE T1
(
	COL1 SMALLINT,
	COL2 INTEGER,
	COL3 INT,
	COL4 BIGINT,
	COL55 DECIMAL,
	COl5 DECIMAL(5,0),
	COL66 DEC,
	COL6 DEC(5,0),
	COL77 NUMERIC,
	COL7 NUMERIC(5,0),
	COL88 NUM,
	COL8 NUM(5,0),
	COL9 FLOAT,
	COL10 FLOAT(53),
	COL11 REAL,
	COL12 DOUBLE,
	COL13 DOUBLE PRECISION,
	COL14 DECFLOAT(34),
	COL144 DECFLOAT,
	COL153 CHARACTER(8 OCTETS) FOR BIT DATA,
	COL163 CHAR(8 OCTETS) FOR BIT DATA,
	COL164 CHAR(8 OCTETS) CCSID ASCII,
	COL171 VARCHAR(8 OCTETS),
	COL172 VARCHAR(8) FOR BIT DATA,
	COL18 CHARACTER VARYING(8),
	COL180 CHARACTER VARYING(8) FOR BIT DATA,
	COL19 CHAR VARYING(8),
	COL199 CHAR VARYING(8) FOR BIT DATA,
	COL20 CLOB(1M),
	COL21 CHARACTER LARGE OBJECT(8K OCTETS),
	COL22 CHAR LARGE OBJECT,
	COL23 GRAPHIC(1),
	COL233 GRAPHIC(1 CODEUNITS16),
	COL234 GRAPHIC(1 CODEUNITS32),
	COL24 VARGRAPHIC(8 CODEUNITS16),
	COL25 DBCLOB(1M),
	COL255 DBCLOB(1K),
	COL26 NCHAR(1),
	COL27 NATIONAL CHAR(2),
	COL28 NATIONAL CHARACTER(3),
	COL29 NVARCHAR(8),
	COL30 NCHAR VARYING(8),
	COL31 NATIONAL CHAR VARYING(8),
	COL32 NATIONAL CHARACTER VARYING(8),
	COL333 NCLOB(1M),
	COL334 NCHAR LARGE OBJECT(5),
	COL335 NATIONAL CHARACTER LARGE OBJECT(1M),
	COL33 BINARY,
	COL34 VARBINARY(14),
	COL35 BINARY VARYING(10),
	COL36 BLOB(1M),
	COL37 BINARY LARGE OBJECT(1M),
	COL38 DATE,
	COL39 TIME,
	COL40 TIMESTAMP,
	COL41 XML,
	COL42 BOOLEAN
);
```

Copy

#### Snowflake[¶](#snowflake "Link to this heading")

```
 CREATE TABLE T1
 (

	COL88 NUMERIC,
	COL8 NUMERIC(5,0),
	COL9 FLOAT,
	COL10 FLOAT(53),
	COL11 REAL,
	COL12 DOUBLE,
	COL13 DOUBLE PRECISION,
	COL14 DECFLOAT,
	COL144 DECFLOAT,
	COL153 BINARY,
	COL163 BINARY,
	COL164 CHAR(8),
	COL171 VARCHAR(8),
	COL172 BINARY,
	COL18 CHARACTER VARYING(8),
	COL180 BINARY,
	COL19 CHAR VARYING(8),
	COL199 BINARY,
	COL20 VARCHAR,
	COL21 VARCHAR,
	COL22 VARCHAR,
	COL23 BINARY,
	COL233 BINARY,
	COL234 BINARY,
	COL24 BINARY,
	COL25 VARCHAR,
	COL255 VARCHAR,
	COL26 NCHAR(1),
	COL27 NCHAR(2),
	COL28 NCHAR(3),
	COL29 NVARCHAR(8),
	COL30 NCHAR VARYING(8),
	COL31 NCHAR VARYING(8),
	COL32 NCHAR VARYING(8),
	COL333 VARCHAR,
	COL334 VARCHAR,
	COL335 VARCHAR,
	COL33 BINARY,
	COL34 VARBINARY(14),
	COL35 BINARY VARYING(10),
	COL36 BINARY,
	COL37 BINARY,
	COL38 DATE,
	COL39 TIME,
	COL40 TIMESTAMP,
	COL41 VARIANT !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - XMLTYPE DATA TYPE CONVERTED TO VARIANT ***/!!!,
	COL42 BOOLEAN
)
 COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "08/29/2025",  "domain": "no-domain-provided" }}';
```

Copy

## DECFLOAT Data Type[¶](#decfloat-data-type "Link to this heading")

### Description[¶](#id1 "Link to this heading")

The `DECFLOAT` data type in IBM DB2 is a decimal floating-point data type that can store decimal numbers with high precision. DB2 supports `DECFLOAT(16)` and `DECFLOAT(34)` precisions.

SnowConvert AI transforms DB2 `DECFLOAT` columns to Snowflake’s native `DECFLOAT` data type in table column definitions and `CAST` expressions.

### Supported Contexts[¶](#supported-contexts "Link to this heading")

`DECFLOAT` is supported in the following contexts:

* **Table column definitions**: `DECFLOAT` columns in `CREATE TABLE` statements are transformed to Snowflake `DECFLOAT`
* **CAST expressions**: `CAST(value AS DECFLOAT)` is preserved in Snowflake

### Unsupported Contexts[¶](#unsupported-contexts "Link to this heading")

`DECFLOAT` is **not** supported in the following contexts and will be transformed to `NUMBER(38, 37)` with an FDM warning:

* Procedure parameters
* Function parameters
* Local variable declarations

### INSERT Statement Handling[¶](#insert-statement-handling "Link to this heading")

When inserting data into `DECFLOAT` columns, SnowConvert AI automatically adds `CAST` expressions to ensure proper data type handling:

#### INSERT with VALUES[¶](#insert-with-values "Link to this heading")

Numeric literals in `INSERT ... VALUES` statements targeting `DECFLOAT` columns are wrapped with `CAST(... AS DECFLOAT)`:

##### DB2[¶](#db2 "Link to this heading")

```
CREATE TABLE prices (
    product_id INT,
    price DECFLOAT(34)
);

INSERT INTO prices VALUES (1, 99.99);
```

Copy

##### Snowflake[¶](#id2 "Link to this heading")

```
CREATE OR REPLACE TABLE prices (
    product_id INT,
    price DECFLOAT
);

INSERT INTO prices VALUES (1, CAST(99.99 AS DECFLOAT));
```

Copy

#### INSERT with SELECT[¶](#insert-with-select "Link to this heading")

Column references in `INSERT ... SELECT` statements are also cast when the target column is `DECFLOAT`:

##### DB2[¶](#id3 "Link to this heading")

```
CREATE TABLE prices (
    product_id INT,
    price DECFLOAT(34)
);

INSERT INTO prices (product_id, price)
SELECT id, amount FROM source_table;
```

Copy

##### Snowflake[¶](#id4 "Link to this heading")

```
CREATE OR REPLACE TABLE prices (
    product_id INT,
    price DECFLOAT
);

INSERT INTO prices (product_id, price)
SELECT id, CAST(amount AS DECFLOAT) FROM source_table;
```

Copy

### Related EWIs[¶](#related-ewis "Link to this heading")

1. [SSC-FDM-DB0002](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/db2FDM.html#ssc-fdm-db0002): DECFLOAT is not supported in this context.

## Related EWIs[¶](#id5 "Link to this heading")

1. [SSC-EWI-0036](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0036): Data type converted to another data type.

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
2. [Transformations](#transformations)
3. [Sample Source Patterns](#sample-source-patterns)
4. [DECFLOAT Data Type](#decfloat-data-type)
5. [Related EWIs](#id5)