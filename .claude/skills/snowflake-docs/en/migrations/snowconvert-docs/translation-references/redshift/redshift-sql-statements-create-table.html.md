---
auto_generated: true
description: Create Table Syntax Grammar.
last_scraped: '2026-01-14T16:57:02.608347+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/redshift/redshift-sql-statements-create-table.html
title: SnowConvert AI - Redshift - CREATE TABLE | Snowflake Documentation
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)Translation References[Redshift](README.md)[SQL Statements](redshift-sql-statements.md)CREATE TABLE

# SnowConvert AI - Redshift - CREATE TABLE[¶](#snowconvert-ai-redshift-create-table "Link to this heading")

Create Table Syntax Grammar.

## Description[¶](#description "Link to this heading")

Creates a new table in the current database. You define a list of columns, which each hold data of a distinct type. The owner of the table is the issuer of the CREATE TABLE command.

For more information please refer to [`CREATE TABLE`](https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_TABLE_NEW.html) documentation.

## Grammar Syntax [¶](#grammar-syntax "Link to this heading")

```
 CREATE [ [LOCAL ] { TEMPORARY | TEMP } ] TABLE
[ IF NOT EXISTS ] table_name
( { column_name data_type [column_attributes] [ column_constraints ]
  | table_constraints
  | LIKE parent_table [ { INCLUDING | EXCLUDING } DEFAULTS ] }
  [, ... ]  )
[ BACKUP { YES | NO } ]
[table_attributes]

where column_attributes are:
  [ DEFAULT default_expr ]
  [ IDENTITY ( seed, step ) ]
  [ GENERATED BY DEFAULT AS IDENTITY ( seed, step ) ]
  [ ENCODE encoding ]
  [ DISTKEY ]
  [ SORTKEY ]
  [ COLLATE CASE_SENSITIVE | COLLATE CASE_INSENSITIVE  ]

and column_constraints are:
  [ { NOT NULL | NULL } ]
  [ { UNIQUE  |  PRIMARY KEY } ]
  [ REFERENCES reftable [ ( refcolumn ) ] ]

and table_constraints  are:
  [ UNIQUE ( column_name [, ... ] ) ]
  [ PRIMARY KEY ( column_name [, ... ] )  ]
  [ FOREIGN KEY (column_name [, ... ] ) REFERENCES reftable [ ( refcolumn ) ]


and table_attributes are:
  [ DISTSTYLE { AUTO | EVEN | KEY | ALL } ]
  [ DISTKEY ( column_name ) ]
  [ [COMPOUND | INTERLEAVED ] SORTKEY ( column_name [,...]) |  [ SORTKEY AUTO ] ]
  [ ENCODE AUTO ]
```

Copy

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

#### Input Code:[¶](#input-code "Link to this heading")

##### Redshift[¶](#redshift "Link to this heading")

```
 CREATE TABLE table1 (
    col1 INTEGER
)
BACKUP YES;
```

Copy

##### Output Code:[¶](#output-code "Link to this heading")

##### Snowflake[¶](#snowflake "Link to this heading")

```
 CREATE TABLE table1 (
    col1 INTEGER
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/17/2024" }}'
;
```

Copy

### Related EWIs[¶](#related-ewis "Link to this heading")

There are no known issues.

## IF NOT EXISTS[¶](#if-not-exists "Link to this heading")

### Description[¶](#id3 "Link to this heading")

In Amazon Redshift, `IF NOT EXISTS` is used in table creation commands to avoid errors if the table already exists. When included, it ensures that the table is created only if it does not already exist, preventing duplication and errors in your SQL script.

Click [here](https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_TABLE_NEW.html) to navigate to the Amazon Redshift docs page for this syntax.

### Grammar Syntax[¶](#id4 "Link to this heading")

```
 IF NOT EXISTS
```

Copy

### Sample Source Patterns[¶](#id5 "Link to this heading")

#### Input Code:[¶](#id6 "Link to this heading")

##### Redshift[¶](#id7 "Link to this heading")

```
 CREATE TABLE IF NOT EXISTS table1 (
    col1 INTEGER
);
```

Copy

##### Output Code:[¶](#id8 "Link to this heading")

##### Snowflake[¶](#id9 "Link to this heading")

```
 CREATE TABLE IF NOT EXISTS table1 (
    col1 INTEGER
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/17/2024" }}';
```

Copy

### Related EWIs[¶](#id10 "Link to this heading")

There are no known issues.

## LOCAL[¶](#local "Link to this heading")

### Description[¶](#id11 "Link to this heading")

In Amazon Redshift, `LOCAL TEMPORARY` or `TEMP` are used to create temporary tables that exist only for the duration of the session. These tables are session-specific and automatically deleted when the session ends. They are useful for storing intermediate results or working data without affecting the permanent database schema.

Click [here](https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_TABLE_NEW.html) to navigate to the Amazon Redshift docs page for this syntax.

### Grammar Syntax[¶](#id12 "Link to this heading")

```
 LOCAL { TEMPORARY | TEMP }
```

Copy

### Sample Source Patterns[¶](#id13 "Link to this heading")

#### Input Code:[¶](#id14 "Link to this heading")

##### Redshift[¶](#id15 "Link to this heading")

```
 CREATE LOCAL TEMPORARY TABLE table1 (
    col1 INTEGER
);
```

Copy

##### Output Code:[¶](#id16 "Link to this heading")

##### Snowflake[¶](#id17 "Link to this heading")

```
 CREATE LOCAL TEMPORARY TABLE table1 (
    col1 INTEGER
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/17/2024" }}';
```

Copy

### Related EWIs[¶](#id18 "Link to this heading")

There are no known issues.

## DISTKEY[¶](#distkey "Link to this heading")

### Description[¶](#id19 "Link to this heading")

In Amazon Redshift, `DISTKEY` is used to distribute data across cluster nodes to optimize query performance. Snowflake, however, automatically handles data distribution and storage without needing explicit distribution keys. Due to differences in architecture and data management approaches, Snowflake does not have a direct equivalent to Redshift’s `DISTKEY`.

Click [here](https://docs.aws.amazon.com/redshift/latest/dg/t_Distributing_data.html) to navigate to the Amazon Redshift docs page for this syntax.

### Grammar Syntax[¶](#id20 "Link to this heading")

```
 DISTKEY ( column_name )
```

Copy

### Sample Source Patterns[¶](#id21 "Link to this heading")

#### Input Code:[¶](#id22 "Link to this heading")

##### Redshift[¶](#id23 "Link to this heading")

```
 CREATE TABLE table1 (
    col1 INTEGER
)
DISTKEY (col1);
```

Copy

##### Output Code:[¶](#id24 "Link to this heading")

##### Snowflake[¶](#id25 "Link to this heading")

```
 CREATE TABLE table1 (
    col1 INTEGER
)
----** SSC-FDM-RS0001 - DISTKEY OPTION NOT SUPPORTED. DATA STORAGE IS AUTOMATICALLY HANDLED BY SNOWFLAKE. **
--DISTKEY (col1)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}';
```

Copy

### Related EWIs[¶](#id26 "Link to this heading")

1. [SSC-FDM-RS0001](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/redshiftFDM.html#ssc-fdm-rs0001): Option not supported. Data storage is automatically handled by Snowflake.

## DISTSTYLE[¶](#diststyle "Link to this heading")

### Description[¶](#id27 "Link to this heading")

Keyword that defines the data distribution style for the whole table.

Click [here](https://docs.aws.amazon.com/redshift/latest/dg/t_Distributing_data.html) to navigate to the Amazon Redshift docs page for this syntax.

### Grammar Syntax[¶](#id28 "Link to this heading")

```
 DISTSTYLE { AUTO | EVEN | KEY | ALL }
```

Copy

### Sample Source Patterns[¶](#id29 "Link to this heading")

#### Input Code:[¶](#id30 "Link to this heading")

##### Redshift[¶](#id31 "Link to this heading")

```
 CREATE TABLE table1 (
    col1 INTEGER
)
DISTSTYLE AUTO;

CREATE TABLE table2 (
    col1 INTEGER
)
DISTSTYLE EVEN;

CREATE TABLE table3 (
    col1 INTEGER
)
DISTSTYLE KEY
DISTKEY (col1);

CREATE TABLE table4 (
    col1 INTEGER
)
DISTSTYLE ALL;
```

Copy

##### Output Code:[¶](#id32 "Link to this heading")

##### Snowflake[¶](#id33 "Link to this heading")

```
 CREATE TABLE table1 (
    col1 INTEGER
)
----** SSC-FDM-RS0001 - DISTSTYLE AUTO OPTION NOT SUPPORTED. DATA STORAGE IS AUTOMATICALLY HANDLED BY SNOWFLAKE. **
--DISTSTYLE AUTO
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/17/2024" }}';

CREATE TABLE table2 (
    col1 INTEGER
)
----** SSC-FDM-RS0001 - DISTSTYLE EVEN OPTION NOT SUPPORTED. DATA STORAGE IS AUTOMATICALLY HANDLED BY SNOWFLAKE. **
--DISTSTYLE EVEN
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/17/2024" }}';

CREATE TABLE table3 (
    col1 INTEGER
)
----** SSC-FDM-RS0001 - DISTSTYLE KEY OPTION NOT SUPPORTED. DATA STORAGE IS AUTOMATICALLY HANDLED BY SNOWFLAKE. **
--DISTSTYLE KEY
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/17/2024" }}'
;

CREATE TABLE table4 (
    col1 INTEGER
)
----** SSC-FDM-RS0001 - DISTSTYLE ALL OPTION NOT SUPPORTED. DATA STORAGE IS AUTOMATICALLY HANDLED BY SNOWFLAKE. **
--DISTSTYLE ALL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/17/2024" }}';
```

Copy

### Related EWIs[¶](#id34 "Link to this heading")

1. [SSC-FDM-RS0001](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/redshiftFDM.html#ssc-fdm-rs0001): Option not supported. Data storage is automatically handled by Snowflake.

## ENCODE[¶](#encode "Link to this heading")

### Description[¶](#id35 "Link to this heading")

In Snowflake, defining `ENCODE` is unnecessary because it automatically handles data compression, unlike Redshift, which requires manual encoding settings. For this reason, the ENCODE statement is removed during migration.

Click [here](https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_TABLE_NEW.html) to navigate to the Amazon Redshift docs page for this syntax.

### Grammar Syntax[¶](#id36 "Link to this heading")

```
 ENCODE AUTO
```

Copy

### Sample Source Patterns[¶](#id37 "Link to this heading")

#### Input Code:[¶](#id38 "Link to this heading")

##### Redshift[¶](#id39 "Link to this heading")

```
 CREATE TABLE table1 (
    col1 INTEGER
)
ENCODE AUTO;
```

Copy

##### Output Code:[¶](#id40 "Link to this heading")

##### Snowflake[¶](#id41 "Link to this heading")

```
 CREATE TABLE table1 (
    col1 INTEGER
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/17/2024" }}'
;
```

Copy

### Related EWIs[¶](#id42 "Link to this heading")

There are no known issues.

## SORTKEY[¶](#sortkey "Link to this heading")

### Description[¶](#id43 "Link to this heading")

The keyword that specifies that the column is the sort key for the table. In Snowflake, `SORTKEY` from Redshift can be migrated to `CLUSTER BY` because both optimize data storage for query performance. `CLUSTER BY` in Snowflake organizes data on specified columns, similar to how `SORTKEY` orders data in Redshift.

Click [here](https://docs.aws.amazon.com/redshift/latest/dg/t_Distributing_data.html) to navigate to the Amazon Redshift docs page for this syntax.

### Grammar Syntax[¶](#id44 "Link to this heading")

```
 [COMPOUND | INTERLEAVED ] SORTKEY ( column_name [,...]) | [ SORTKEY AUTO ]
```

Copy

### Sample Source Patterns[¶](#id45 "Link to this heading")

#### Input Code:[¶](#id46 "Link to this heading")

##### Redshift[¶](#id47 "Link to this heading")

```
 CREATE TABLE table1 (
    col1 INTEGER,
    col2 VARCHAR,
    col3 INTEGER,
    col4 INTEGER
)
COMPOUND SORTKEY (col1, col3);

CREATE TABLE table2 (
    col1 INTEGER
)
INTERLEAVED SORTKEY (col1);

CREATE TABLE table3 (
    col1 INTEGER
)
SORTKEY AUTO;
```

Copy

##### Output Code:[¶](#id48 "Link to this heading")

##### Snowflake[¶](#id49 "Link to this heading")

```
 CREATE TABLE table1 (
    col1 INTEGER,
    col2 VARCHAR,
    col3 INTEGER,
    col4 INTEGER
)
--** SSC-FDM-RS0002 - THE PERFORMANCE OF THE CLUSTER BY MAY VARY COMPARED TO THE PERFORMANCE OF SORTKEY **
CLUSTER BY (col1, col3)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/17/2024" }}'
;

CREATE TABLE table2 (
    col1 INTEGER
)
--** SSC-FDM-RS0002 - THE PERFORMANCE OF THE CLUSTER BY MAY VARY COMPARED TO THE PERFORMANCE OF SORTKEY **
CLUSTER BY (col1)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/17/2024" }}'
;

CREATE TABLE table3 (
    col1 INTEGER
)
----** SSC-FDM-RS0001 - SORTKEY AUTO OPTION NOT SUPPORTED. DATA STORAGE IS AUTOMATICALLY HANDLED BY SNOWFLAKE. **
--SORTKEY AUTO
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/17/2024" }}';
```

Copy

### Related EWIs[¶](#id50 "Link to this heading")

1. [SSC-FDM-RS0001](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/redshiftFDM.html#ssc-fdm-rs0001): Option not supported. Data storage is automatically handled by Snowflake.
2. [SSC-FDM-RS0002](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/redshiftFDM.html#ssc-fdm-rs0002): The performance of the CLUSTER BY may vary compared to the performance of Sortkey.

## FOREIGN KEY[¶](#foreign-key "Link to this heading")

### Description[¶](#id51 "Link to this heading")

Constraint that specifies a foreign key constraint, which requires that a group of one or more columns of the new table must only contain values that match values in the referenced column or columns of some row of the referenced table.

Click [here](https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_TABLE_NEW.html) to navigate to the Amazon Redshift docs page for this syntax.

Warning

The translation for Foreign Key will be delivered in the future.

### Grammar Syntax[¶](#id52 "Link to this heading")

```
 FOREIGN KEY (column_name [, ... ] ) REFERENCES reftable [ ( refcolumn )
```

Copy

### Sample Source Patterns[¶](#id53 "Link to this heading")

#### Input Code:[¶](#id54 "Link to this heading")

##### Redshift[¶](#id55 "Link to this heading")

```
 CREATE TABLE table15 (
    col1 INTEGER,
    FOREIGN KEY (col1) REFERENCES table_test (col1)
);
```

Copy

##### Output Code:[¶](#id56 "Link to this heading")

##### Snowflake[¶](#id57 "Link to this heading")

```
 CREATE TABLE table15 (
    col1 INTEGER
--                ,
--    --** SSC-FDM-RS0003 - THE TRANSLATION FOR FOREIGN KEY IS NOT AVAILABLE, IT WILL BE PROVIDED IN THE FUTURE. **
--    FOREIGN KEY (col1) REFERENCES table_test (col1)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/26/2024" }}';
```

Copy

### Related EWIs[¶](#id58 "Link to this heading")

* [SSC-FDM-RSOOO3](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/redshiftFDM.html#ssc-fdm-rs0003): Foreign Key translation will be supported in the future.

## PRIMARY KEY[¶](#primary-key "Link to this heading")

### Description[¶](#id59 "Link to this heading")

Specifies that a column or a number of columns of a table can contain only unique non-null values

Click [here](https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_TABLE_NEW.html) to navigate to the Amazon Redshift docs page for this syntax.

Note

In Snowflake, unique, primary and foreign keys are used for documentation and do not enforce constraints or uniqueness. They help describe table relationships but don’t impact data integrity or performance.

### Grammar Syntax[¶](#id60 "Link to this heading")

```
 PRIMARY KEY ( column_name [, ... ] )
```

Copy

### Sample Source Patterns[¶](#id61 "Link to this heading")

#### Input Code:[¶](#id62 "Link to this heading")

##### Redshift[¶](#id63 "Link to this heading")

```
 CREATE TABLE table1 (
    col1 INTEGER, 
    col2 INTEGER,
    PRIMARY KEY (col1)
);
```

Copy

##### Output Code:[¶](#id64 "Link to this heading")

##### Snowflake[¶](#id65 "Link to this heading")

```
 CREATE TABLE table1 (
    col1 INTEGER,
    col2 INTEGER,
    PRIMARY KEY (col1)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/17/2024" }}'
;
```

Copy

### Related EWIs[¶](#id66 "Link to this heading")

There are no known issues.

## UNIQUE[¶](#unique "Link to this heading")

### Description[¶](#id67 "Link to this heading")

Specifies that a group of one or more columns of a table can contain only unique values.

Click [here](https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_TABLE_NEW.html) to navigate to the Amazon Redshift docs page for this syntax.

Note

In Snowflake, unique, primary and foreign keys are used for documentation and do not enforce constraints or uniqueness. They help describe table relationships but don’t impact data integrity or performance.

### Grammar Syntax[¶](#id68 "Link to this heading")

```
 UNIQUE ( column_name [, ... ] )
```

Copy

### Sample Source Patterns[¶](#id69 "Link to this heading")

#### Input Code:[¶](#id70 "Link to this heading")

##### Redshift[¶](#id71 "Link to this heading")

```
 CREATE TABLE table1 (
    col1 INTEGER, 
    col2 INTEGER,
    UNIQUE ( col1, col2 )
);
```

Copy

##### Output Code:[¶](#id72 "Link to this heading")

##### Snowflake[¶](#id73 "Link to this heading")

```
 CREATE TABLE table1 (
    col1 INTEGER,
    col2 INTEGER,
    UNIQUE ( col1, col2 )
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/17/2024" }}'
;
```

Copy

### Related EWIs[¶](#id74 "Link to this heading")

There are no known issues.

## NOT NULL | NULL[¶](#not-null-null "Link to this heading")

### Description[¶](#id75 "Link to this heading")

NOT NULL specifies that the column isn’t allowed to contain null values. NULL, the default, specifies that the column accepts null values.

Click [here](https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_TABLE_NEW.html) to navigate to the Amazon Redshift docs page for this syntax.

### Grammar Syntax[¶](#id76 "Link to this heading")

```
 NOT NULL | NULL
```

Copy

### Sample Source Patterns[¶](#id77 "Link to this heading")

#### Input Code:[¶](#id78 "Link to this heading")

##### Redshift[¶](#id79 "Link to this heading")

```
 CREATE TABLE table1 (
    col1 INTEGER NOT NULL, 
    col2 INTEGER NULL
);
```

Copy

##### Output Code:[¶](#id80 "Link to this heading")

##### Snowflake[¶](#id81 "Link to this heading")

```
 CREATE TABLE table1 (
    col1 INTEGER NOT NULL,
    col2 INTEGER NULL
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/17/2024" }}'
;
```

Copy

### Related EWIs[¶](#id82 "Link to this heading")

There are no known issues.

## REFERENCES[¶](#references "Link to this heading")

### Description[¶](#id83 "Link to this heading")

Specifies a foreign key constraint, which implies that the column must contain only values that match values in the referenced column of some row of the referenced table

Click [here](https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_TABLE_NEW.html) to navigate to the Amazon Redshift docs page for this syntax.

### Grammar Syntax[¶](#id84 "Link to this heading")

```
 REFERENCES reftable [ ( refcolumn ) ]
```

Copy

### Sample Source Patterns[¶](#id85 "Link to this heading")

#### Input Code:[¶](#id86 "Link to this heading")

##### Redshift[¶](#id87 "Link to this heading")

```
 CREATE TABLE table1 (
    col1 INTEGER REFERENCES table_test (col1)
);
```

Copy

##### Output Code:[¶](#id88 "Link to this heading")

##### Snowflake[¶](#id89 "Link to this heading")

```
 CREATE TABLE table1 (
    col1 INTEGER REFERENCES table_test (col1)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/17/2024" }}'
;
```

Copy

### Related EWIs[¶](#id90 "Link to this heading")

There are no known issues.

## UNIQUE | PRIMARY KEY[¶](#unique-primary-key "Link to this heading")

### Description[¶](#id91 "Link to this heading")

Specifies that the column can contain only unique values. In Snowflake, both UNIQUE and PRIMARY KEY are used to document and structure data, but they do not have active data validation functionality in the sense that you might expect in other database systems that enforce these restrictions at the storage level.

Click [here](https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_TABLE_NEW.html) to navigate to the Amazon Redshift docs page for this syntax.

Note

In Snowflake, unique, primary and foreign keys are used for documentation and do not enforce constraints or uniqueness. They help describe table relationships but don’t impact data integrity or performance.

### Grammar Syntax[¶](#id92 "Link to this heading")

```
 UNIQUE | PRIMARY KEY
```

Copy

### Sample Source Patterns[¶](#id93 "Link to this heading")

#### Input Code:[¶](#id94 "Link to this heading")

##### Redshift[¶](#id95 "Link to this heading")

```
 CREATE TABLE table1 (
    col1 INTEGER PRIMARY KEY,
    col2 INTEGER UNIQUE
);
```

Copy

##### Output Code:[¶](#id96 "Link to this heading")

##### Snowflake[¶](#id97 "Link to this heading")

```
 CREATE TABLE table1 (
    col1 INTEGER PRIMARY KEY,
    col2 INTEGER UNIQUE
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/17/2024" }}'
;
```

Copy

### Related EWIs[¶](#id98 "Link to this heading")

There are no known issues.

## COLLATE[¶](#collate "Link to this heading")

### Description[¶](#id99 "Link to this heading")

Specifies whether string search or comparison on the column is CASE\_SENSITIVE or CASE\_INSENSITIVE.

Click [here](https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_TABLE_NEW.html) to navigate to the Amazon Redshift docs page for this syntax.

Note

The default collation language is English. If your database uses a different language, please update the ‘en-’ prefix to match your database’s language. For more information, please refer to this [link](https://docs.snowflake.com/en/sql-reference/collation#label-collation-specification).

### Grammar Syntax[¶](#id100 "Link to this heading")

```
 COLLATE CASE_SENSITIVE | COLLATE CASE_INSENSITIVE
```

Copy

### Sample Source Patterns[¶](#id101 "Link to this heading")

#### Input Code:[¶](#id102 "Link to this heading")

##### Redshift[¶](#id103 "Link to this heading")

```
 CREATE TABLE table1 (
    col1 TEXT COLLATE CASE_SENSITIVE,
    col2 TEXT COLLATE CASE_INSENSITIVE
);
```

Copy

##### Output Code:[¶](#id104 "Link to this heading")

##### Snowflake[¶](#id105 "Link to this heading")

```
 CREATE TABLE table1 (
    col1 TEXT COLLATE 'en-cs',
    col2 TEXT COLLATE 'en-ci'
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/17/2024" }}'
;
```

Copy

### Known issues[¶](#known-issues "Link to this heading")

There are no known issues.

## DEFAULT[¶](#default "Link to this heading")

### Description[¶](#id106 "Link to this heading")

Assigns a default data value for the column.

Click [here](https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_TABLE_NEW.html#create-table-default) to navigate to the Amazon Redshift docs page for this syntax.

### Grammar Syntax[¶](#id107 "Link to this heading")

```
 DEFAULT default_expr
```

Copy

### Sample Source Patterns[¶](#id108 "Link to this heading")

#### Input Code:[¶](#id109 "Link to this heading")

##### Redshift[¶](#id110 "Link to this heading")

```
 CREATE TABLE table1 (
    col1 INTEGER DEFAULT 1
);
```

Copy

##### Output Code:[¶](#id111 "Link to this heading")

##### Snowflake[¶](#id112 "Link to this heading")

```
 CREATE TABLE table1 (
    col1 INTEGER DEFAULT 1
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/17/2024" }}'
;
```

Copy

### Related EWIs[¶](#id113 "Link to this heading")

There are no known issues.

## DISTKEY[¶](#id114 "Link to this heading")

### Description[¶](#id115 "Link to this heading")

In Amazon Redshift, `DISTKEY` is used to distribute data across cluster nodes to optimize query performance. Snowflake, however, automatically handles data distribution and storage without needing explicit distribution keys. Due to differences in architecture and data management approaches, Snowflake does not have a direct equivalent to Redshift’s `DISTKEY`. For these reasons, the statement `DISTKEY` is removed during the transformation process

Click [here](https://docs.aws.amazon.com/redshift/latest/dg/t_Distributing_data.html) to navigate to the Amazon Redshift docs page for this syntax.

### Grammar Syntax[¶](#id116 "Link to this heading")

```
 DISTKEY
```

Copy

### Sample Source Patterns[¶](#id117 "Link to this heading")

#### Input Code:[¶](#id118 "Link to this heading")

##### Redshift[¶](#id119 "Link to this heading")

```
 CREATE TABLE table1 (
    col1 INTEGER DISTKEY
);
```

Copy

##### Output Code:[¶](#id120 "Link to this heading")

##### Snowflake[¶](#id121 "Link to this heading")

```
 CREATE TABLE table1 (
    col1 INTEGER
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/17/2024" }}'
;
```

Copy

### Related EWIs[¶](#id122 "Link to this heading")

There are no known issues.

## ENCODE[¶](#id123 "Link to this heading")

### Description[¶](#id124 "Link to this heading")

The compression encoding for a column. In Snowflake, defining `ENCODE` is unnecessary because it automatically handles data compression, unlike Redshift, which requires manual encoding settings. For this reason, the ENCODE statement is removed during migration.

Click [here](https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_TABLE_NEW.html#create-table-encode) to navigate to the Amazon Redshift docs page for this syntax.

### Grammar Syntax[¶](#id125 "Link to this heading")

```
 ENCODE encoding
```

Copy

### Sample Source Patterns[¶](#id126 "Link to this heading")

#### Input Code:[¶](#id127 "Link to this heading")

##### Redshift[¶](#id128 "Link to this heading")

```
 CREATE TABLE table1 (
    col1 INTEGER ENCODE DELTA
);
```

Copy

##### Output Code:[¶](#id129 "Link to this heading")

##### Snowflake[¶](#id130 "Link to this heading")

```
 CREATE TABLE table1 (
    col1 INTEGER
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/17/2024" }}'
;
```

Copy

### Related EWIs[¶](#id131 "Link to this heading")

There are no known issues.

## GENERATED BY DEFAULT AS IDENTITY[¶](#generated-by-default-as-identity "Link to this heading")

### Description[¶](#id132 "Link to this heading")

Specifies that the column is a default IDENTITY column and enables you to automatically assign a unique value to the column.

Click [here](https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_TABLE_NEW.html#identity-generated-bydefault-clause) to navigate to the Amazon Redshift docs page for this syntax.

### Grammar Syntax[¶](#id133 "Link to this heading")

```
 GENERATED BY DEFAULT AS IDENTITY ( seed, step )
```

Copy

### Sample Source Patterns[¶](#id134 "Link to this heading")

#### Input Code:[¶](#id135 "Link to this heading")

##### Redshift[¶](#id136 "Link to this heading")

```
 CREATE TABLE table1 (
    col1 INTEGER GENERATED BY DEFAULT AS IDENTITY(1,1)
);
```

Copy

##### Output Code:[¶](#id137 "Link to this heading")

##### Snowflake[¶](#id138 "Link to this heading")

```
 CREATE TABLE table1 (
    col1 INTEGER IDENTITY(1,1) ORDER
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/17/2024" }}'
;
```

Copy

### Related EWIs[¶](#id139 "Link to this heading")

There are no known issues.

## IDENTITY[¶](#identity "Link to this heading")

### Description[¶](#id140 "Link to this heading")

> Clause that specifies that the column is an IDENTITY column. ([RedShift SQL Language Reference Identity](https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_TABLE_NEW.html#identity-clause)).

### Grammar Syntax[¶](#id141 "Link to this heading")

```
 IDENTITY ( seed, step )
```

Copy

### Sample Source Patterns[¶](#id142 "Link to this heading")

#### Input Code:[¶](#id143 "Link to this heading")

##### Redshift[¶](#id144 "Link to this heading")

```
 CREATE TABLE table1 (
    doc INTEGER,
    id1 INTEGER IDENTITY(1,1),
    id2 INTEGER  DEFAULT "identity"(674435, 0, ('5,3'::character varying)::text),
    id3 INTEGER  DEFAULT default_identity(963861, 1, '1,2'::text),
    id4 INTEGER  DEFAULT "default_identity"(963861, 1, '1,6'::text)
);

INSERT INTO table1 (doc) VALUES (1),(2),(3);

SELECT * FROM table1;
```

Copy

##### Results[¶](#results "Link to this heading")

| DOC | ID1 | ID2 | ID3 | ID4 |
| --- | --- | --- | --- | --- |
| 1 | 1 | 5 | 1 | 1 |
| 2 | 2 | 8 | 3 | 7 |
| 3 | 3 | 11 | 5 | 13 |

##### Output Code:[¶](#id145 "Link to this heading")

##### Snowflake[¶](#id146 "Link to this heading")

```
 CREATE TABLE table1 (
    doc INTEGER,
    id1 INTEGER IDENTITY(1,1) ORDER,
    id2 INTEGER IDENTITY(5,3) ORDER,
    id3 INTEGER IDENTITY(1,2) ORDER,
    id4 INTEGER IDENTITY(1,6) ORDER
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "12/04/2024",  "domain": "test" }}';

INSERT INTO table1 (doc) VALUES (1),(2),(3);

SELECT * FROM
 table1;
```

Copy

##### Results[¶](#id147 "Link to this heading")

| DOC | ID1 | ID2 | ID3 | ID4 |
| --- | --- | --- | --- | --- |
| 1 | 1 | 5 | 1 | 1 |
| 2 | 2 | 8 | 3 | 7 |
| 3 | 3 | 11 | 5 | 13 |

### Known Issues [¶](#id148 "Link to this heading")

No issues were found.

### Related EWIs[¶](#id149 "Link to this heading")

There are no known issues.

## SORTKEY[¶](#id150 "Link to this heading")

### Description[¶](#id151 "Link to this heading")

The keyword that specifies that the column is the sort key for the table. In Snowflake, `SORTKEY` from Redshift can be migrated to `CLUSTER BY` because both optimize data storage for query performance. `CLUSTER BY` in Snowflake organizes data on specified columns, similar to how `SORTKEY` orders data in Redshift.

Click [here](https://docs.aws.amazon.com/redshift/latest/dg/t_Sorting_data.html) to navigate to the Amazon Redshift docs page for this syntax.

### Grammar Syntax[¶](#id152 "Link to this heading")

```
 SORTKEY
```

Copy

### Sample Source Patterns[¶](#id153 "Link to this heading")

#### Input Code:[¶](#id154 "Link to this heading")

##### Redshift[¶](#id155 "Link to this heading")

```
 CREATE TABLE table1 (
    col1 INTEGER SORTKEY
);
```

Copy

##### Output Code:[¶](#id156 "Link to this heading")

##### Snowflake[¶](#id157 "Link to this heading")

```
 CREATE TABLE table1 (
    col1 INTEGER
)
--** SSC-FDM-RS0002 - THE PERFORMANCE OF THE CLUSTER BY MAY VARY COMPARED TO THE PERFORMANCE OF SORTKEY **
CLUSTER BY (col1)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/17/2024" }}';
```

Copy

### Known issues[¶](#id158 "Link to this heading")

1. [SSC-FDM-RS0002](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/redshiftFDM.html#ssc-fdm-rs0002): The performance of the CLUSTER BY may vary compared to the performance of the Sortkey or Distkey.

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
4. [IF NOT EXISTS](#if-not-exists)
5. [LOCAL](#local)
6. [DISTKEY](#distkey)
7. [DISTSTYLE](#diststyle)
8. [ENCODE](#encode)
9. [SORTKEY](#sortkey)
10. [FOREIGN KEY](#foreign-key)
11. [PRIMARY KEY](#primary-key)
12. [UNIQUE](#unique)
13. [NOT NULL | NULL](#not-null-null)
14. [REFERENCES](#references)
15. [UNIQUE | PRIMARY KEY](#unique-primary-key)
16. [COLLATE](#collate)
17. [DEFAULT](#default)
18. [DISTKEY](#id114)
19. [ENCODE](#id123)
20. [GENERATED BY DEFAULT AS IDENTITY](#generated-by-default-as-identity)
21. [IDENTITY](#identity)
22. [SORTKEY](#id150)