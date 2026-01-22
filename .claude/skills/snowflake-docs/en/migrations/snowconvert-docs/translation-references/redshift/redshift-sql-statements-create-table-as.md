---
auto_generated: true
description: Create Table As Syntax Grammar.
last_scraped: '2026-01-14T16:53:40.869380+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/redshift/redshift-sql-statements-create-table-as
title: SnowConvert AI - Redshift - CREATE TABLE AS | Snowflake Documentation
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
          + [Redshift](README.md)

            - [Basic Elements](redshift-basic-elements.md)
            - [Expressions](redshift-expressions.md)
            - [Conditions](redshift-conditions.md)
            - [Data types](redshift-data-types.md)
            - [SQL Statements](redshift-sql-statements.md)

              * [CONTINUE HANDLER](redshift-continue-handler.md)
              * [EXIT HANDLER](redshift-exit-handler.md)
              * [CREATE TABLE](redshift-sql-statements-create-table.md)
              * [CREATE TABLE AS](redshift-sql-statements-create-table-as.md)
              * [CREATE PROCEDURE](rs-sql-statements-create-procedure.md)
              * [SELECT](rs-sql-statements-select.md)
              * [SELECT INTO](rs-sql-statements-select-into.md)
            - [Functions](redshift-functions.md)
            - [System Catalog Tables](redshift-system-catalog.md)
            - ETL And BI Repointing

              - [Power BI Redshift Repointing](etl-bi-repointing/power-bi-redshift-repointing.md)
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)Translation References[Redshift](README.md)[SQL Statements](redshift-sql-statements.md)CREATE TABLE AS

# SnowConvert AI - Redshift - CREATE TABLE AS[¶](#snowconvert-ai-redshift-create-table-as "Link to this heading")

Create Table As Syntax Grammar.

## Description[¶](#description "Link to this heading")

Creates a new table based on a query. The owner of this table is the user that issues the command.

For more information please refer to [`CREATE TABLE AS`](https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_TABLE_AS.html) documentation.

## Grammar Syntax [¶](#grammar-syntax "Link to this heading")

```
 CREATE [ [ LOCAL ] { TEMPORARY | TEMP } ]
TABLE table_name
[ ( column_name [, ... ] ) ]
[ BACKUP { YES | NO } ]
[ table_attributes ]
AS query

where table_attributes are:
[ DISTSTYLE { AUTO | EVEN | ALL | KEY } ]
[ DISTKEY( distkey_identifier ) ]
[ [ COMPOUND | INTERLEAVED ] SORTKEY( column_name [, ...] ) ]
```

Copy

# SnowConvert AI - Redshift - Table Start[¶](#snowconvert-ai-redshift-table-start "Link to this heading")

## BACKUP[¶](#backup "Link to this heading")

### Description[¶](#id1 "Link to this heading")

Enables Amazon Redshift to automatically adjust the encoding type for all columns in the table to optimize query performance. In Snowflake, the concept of `BACKUP` as seen in other databases is not directly applicable. Snowflake automatically handles data backup and recovery through its built-in features like Time Travel and Fail-safe, eliminating the need for manual backup operations. For these reasons, the statement `BACKUP` is removed during the transformation process

Click [here](https://docs.aws.amazon.com/redshift/latest/dg/t_Distributing_data.html) to navigate to the Amazon Redshift docs page for this syntax.

### Grammar Syntax[¶](#id2 "Link to this heading")

```
 BACKUP { YES | NO }
```

Copy

### Sample Source Patterns[¶](#sample-source-patterns "Link to this heading")

#### NO option[¶](#no-option "Link to this heading")

An FDM is added since Snowflake, by default, always creates a backup of the created table.

##### Input Code:[¶](#input-code "Link to this heading")

##### Redshift[¶](#redshift "Link to this heading")

```
 CREATE TABLE table1
BACKUP NO
AS SELECT * FROM table_test;
```

Copy

##### Output Code:[¶](#output-code "Link to this heading")

##### Snowflake[¶](#snowflake "Link to this heading")

```
 CREATE TABLE table1
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/10/2025",  "domain": "test" }}'
----** SSC-FDM-RS0001 - BACKUP NO OPTION NOT SUPPORTED. DATA STORAGE IS AUTOMATICALLY HANDLED BY SNOWFLAKE. **
--BACKUP NO
AS SELECT * FROM
table_test;
```

Copy

#### YES option[¶](#yes-option "Link to this heading")

The option is removed since Snowflake, by default, applies a backup to the created table.

##### Input Code:[¶](#id3 "Link to this heading")

##### Redshift[¶](#id4 "Link to this heading")

```
 CREATE TABLE table1
BACKUP YES
AS SELECT * FROM table_test;
```

Copy

##### Output Code:[¶](#id5 "Link to this heading")

##### Snowflake[¶](#id6 "Link to this heading")

```
 CREATE TABLE table1
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/10/2025",  "domain": "test" }}'
AS SELECT * FROM
table_test;
```

Copy

### [¶](#id7 "Link to this heading")

### Related EWIs[¶](#related-ewis "Link to this heading")

* [SSC-FDM-RS0001](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/redshiftFDM.html#ssc-fdm-rs0001): “Option” not supported. Data storage is automatically handled by Snowflake.

## COLUMNS[¶](#columns "Link to this heading")

### Description[¶](#id8 "Link to this heading")

The name of a column in the new table. If no column names are provided, the column names are taken from the output column names of the query.

Click [here](https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_TABLE_NEW.html) to navigate to the Amazon Redshift docs page for this syntax.

### Grammar Syntax[¶](#id9 "Link to this heading")

```
 ( column_name [, ... ] )
```

Copy

### Sample Source Patterns[¶](#id10 "Link to this heading")

#### Input Code:[¶](#id11 "Link to this heading")

##### Redshift[¶](#id12 "Link to this heading")

```
 CREATE TABLE table1 
(
    col1, col2, col3
)
AS SELECT col1, col2, col3 FROM table_test;
```

Copy

##### Output Code:[¶](#id13 "Link to this heading")

##### Snowflake[¶](#id14 "Link to this heading")

```
 CREATE TABLE table1
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/17/2024" }}'
(
    col1, col2, col3
)
AS SELECT col1, col2, col3 FROM
        table_test;
```

Copy

### Related EWIs[¶](#id15 "Link to this heading")

There are no known issues.

## LOCAL[¶](#local "Link to this heading")

### Description[¶](#id16 "Link to this heading")

In Amazon Redshift, `LOCAL TEMPORARY` or `TEMP` are used to create temporary tables that exist only for the duration of the session. These tables are session-specific and automatically deleted when the session ends. They are useful for storing intermediate results or working data without affecting the permanent database schema.

Click [here](https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_TABLE_NEW.html) to navigate to the Amazon Redshift docs page for this syntax.

### Grammar Syntax[¶](#id17 "Link to this heading")

```
 LOCAL { TEMPORARY | TEMP }
```

Copy

### Sample Source Patterns[¶](#id18 "Link to this heading")

#### Input Code:[¶](#id19 "Link to this heading")

##### Redshift[¶](#id20 "Link to this heading")

```
 CREATE LOCAL TEMP TABLE table1
AS SELECT FROM table_test;
```

Copy

##### Output Code:[¶](#id21 "Link to this heading")

##### Snowflake[¶](#id22 "Link to this heading")

```
 CREATE LOCAL TEMP TABLE table1
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/17/2024" }}'
AS SELECT FROM
table_test;
```

Copy

### Related EWIs[¶](#id23 "Link to this heading")

There are no known issues.

# SnowConvert AI - Redshift - Tabla Attributes[¶](#snowconvert-ai-redshift-tabla-attributes "Link to this heading")

## DISTKEY[¶](#distkey "Link to this heading")

### Description[¶](#id24 "Link to this heading")

In Amazon Redshift, `DISTKEY` is used to distribute data across cluster nodes to optimize query performance. Snowflake, however, automatically handles data distribution and storage without needing explicit distribution keys. Due to differences in architecture and data management approaches, Snowflake does not have a direct equivalent to Redshift’s `DISTKEY`. For these reasons, the statement `DISTKEY` is removed during the transformation process

Click [here](https://docs.aws.amazon.com/redshift/latest/dg/t_Distributing_data.html) to navigate to the Amazon Redshift docs page for this syntax.

### Grammar Syntax[¶](#id25 "Link to this heading")

```
 DISTKEY ( column_name )
```

Copy

### Sample Source Patterns[¶](#id26 "Link to this heading")

#### Input Code:[¶](#id27 "Link to this heading")

##### Redshift[¶](#id28 "Link to this heading")

```
 CREATE TABLE table1
DISTKEY (col1)
AS SELECT * FROM table_test;
```

Copy

##### Output Code:[¶](#id29 "Link to this heading")

##### Snowflake[¶](#id30 "Link to this heading")

```
 CREATE TABLE table1
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/10/2025",  "domain": "test" }}'
----** SSC-FDM-RS0001 - DISTKEY OPTION NOT SUPPORTED. DATA STORAGE IS AUTOMATICALLY HANDLED BY SNOWFLAKE. **
--DISTKEY (col1)
AS SELECT * FROM
table_test;
```

Copy

### Related EWIs[¶](#id31 "Link to this heading")

* [SSC-FDM-RS0001](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/redshiftFDM.html#ssc-fdm-rs0001): “Option” not supported. Data storage is automatically handled by Snowflake.

## DISTSTYLE[¶](#diststyle "Link to this heading")

### Description[¶](#id32 "Link to this heading")

Keyword that defines the data distribution style for the whole table.

Click [here](https://docs.aws.amazon.com/redshift/latest/dg/t_Distributing_data.html) to navigate to the Amazon Redshift docs page for this syntax.

### Grammar Syntax[¶](#id33 "Link to this heading")

```
 DISTSTYLE { AUTO | EVEN | KEY | ALL }
```

Copy

### Sample Source Patterns[¶](#id34 "Link to this heading")

#### Input Code:[¶](#id35 "Link to this heading")

##### Redshift[¶](#id36 "Link to this heading")

```
 CREATE TABLE table1 
DISTSTYLE AUTO
AS SELECT * FROM table_test;

CREATE TABLE table2
DISTSTYLE EVEN
AS SELECT * FROM table_test;

CREATE TABLE table3
DISTSTYLE ALL
AS SELECT * FROM table_test;

CREATE TABLE table4
DISTSTYLE KEY
DISTKEY (col1)
AS SELECT * FROM table_test;
```

Copy

##### Output Code:[¶](#id37 "Link to this heading")

##### Snowflake[¶](#id38 "Link to this heading")

```
 CREATE TABLE table1
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/17/2024" }}'
----** SSC-FDM-RS0001 - DISTSTYLE AUTO OPTION NOT SUPPORTED. DATA STORAGE IS AUTOMATICALLY HANDLED BY SNOWFLAKE. **
--DISTSTYLE AUTO
AS SELECT * FROM
table_test;

CREATE TABLE table2
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/17/2024" }}'
----** SSC-FDM-RS0001 - DISTSTYLE EVEN OPTION NOT SUPPORTED. DATA STORAGE IS AUTOMATICALLY HANDLED BY SNOWFLAKE. **
--DISTSTYLE EVEN
AS SELECT * FROM
table_test;

CREATE TABLE table3
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/17/2024" }}'
----** SSC-FDM-RS0001 - DISTSTYLE ALL OPTION NOT SUPPORTED. DATA STORAGE IS AUTOMATICALLY HANDLED BY SNOWFLAKE. **
--DISTSTYLE ALL
AS SELECT * FROM
table_test;

CREATE TABLE table4
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/17/2024" }}'
----** SSC-FDM-RS0001 - DISTSTYLE KEY OPTION NOT SUPPORTED. DATA STORAGE IS AUTOMATICALLY HANDLED BY SNOWFLAKE. **
--DISTSTYLE KEY
----** SSC-FDM-RS0001 - DISTKEY OPTION NOT SUPPORTED. DATA STORAGE IS AUTOMATICALLY HANDLED BY SNOWFLAKE. **
--DISTKEY (col1)
AS SELECT * FROM
table_test;
```

Copy

### Related EWIs[¶](#id39 "Link to this heading")

1. [SSC-FDM-RS0001](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/redshiftFDM.html#ssc-fdm-rs0001): “Option” not supported. Data storage is automatically handled by Snowflake.

## SORTKEY[¶](#sortkey "Link to this heading")

### Description[¶](#id40 "Link to this heading")

The keyword that specifies that the column is the sort key for the table. In Snowflake, `SORTKEY` from Redshift can be migrated to `CLUSTER BY` because both optimize data storage for query performance. `CLUSTER BY` in Snowflake organizes data on specified columns, similar to how `SORTKEY` orders data in Redshift.

Click [here](https://docs.aws.amazon.com/redshift/latest/dg/t_Distributing_data.html) to navigate to the Amazon Redshift docs page for this syntax.

### Grammar Syntax[¶](#id41 "Link to this heading")

```
 [ COMPOUND | INTERLEAVED ] SORTKEY( column_name [, ...] )
```

Copy

### Sample Source Patterns[¶](#id42 "Link to this heading")

#### Input Code:[¶](#id43 "Link to this heading")

##### Redshift[¶](#id44 "Link to this heading")

```
 CREATE TABLE table1 (
    col1,
    col2,
    col3,
    col4
)
COMPOUND SORTKEY (col1, col3)
AS SELECT * FROM table_test;

CREATE TABLE table2 (
    col1
)
INTERLEAVED SORTKEY (col1)
AS SELECT * FROM table_test;

CREATE TABLE table3 (
    col1
)
SORTKEY (col1)
AS SELECT * FROM table_test;
```

Copy

##### Output Code:[¶](#id45 "Link to this heading")

##### Snowflake[¶](#id46 "Link to this heading")

```
 CREATE TABLE table1
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/17/2024" }}'
(
    col1,
    col2,
    col3,
    col4
)
--** SSC-FDM-RS0002 - THE PERFORMANCE OF THE CLUSTER BY MAY VARY COMPARED TO THE PERFORMANCE OF SORTKEY **
CLUSTER BY (col1, col3)
AS SELECT * FROM
        table_test;

CREATE TABLE table2
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/17/2024" }}'
(
    col1
)
--** SSC-FDM-RS0002 - THE PERFORMANCE OF THE CLUSTER BY MAY VARY COMPARED TO THE PERFORMANCE OF SORTKEY **
CLUSTER BY (col1)
AS SELECT * FROM
        table_test;

CREATE TABLE table3
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/17/2024" }}'
(
    col1
)
--** SSC-FDM-RS0002 - THE PERFORMANCE OF THE CLUSTER BY MAY VARY COMPARED TO THE PERFORMANCE OF SORTKEY **
CLUSTER BY (col1)
AS SELECT * FROM
        table_test;
```

Copy

### Related EWIs[¶](#id47 "Link to this heading")

1. [SSC-FDM-RS0002](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/redshiftFDM.html#ssc-fdm-rs0002): The performance of the CLUSTER BY may vary compared to the performance of Sortkey.

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
3. [BACKUP](#backup)
4. [COLUMNS](#columns)
5. [LOCAL](#local)
6. [DISTKEY](#distkey)
7. [DISTSTYLE](#diststyle)
8. [SORTKEY](#sortkey)