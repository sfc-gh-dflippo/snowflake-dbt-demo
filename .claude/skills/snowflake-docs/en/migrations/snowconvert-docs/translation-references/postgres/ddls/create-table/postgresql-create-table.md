---
auto_generated: true
description: Translation from PostgreSql to Snowflake
last_scraped: '2026-01-14T16:53:33.242727+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/postgres/ddls/create-table/postgresql-create-table
title: SnowConvert AI - PostgreSQL - CREATE TABLE | Snowflake Documentation
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
          + [Oracle](../../../oracle/README.md)
          + [SQL Server-Azure Synapse](../../../transact/README.md)
          + [Sybase IQ](../../../sybase/README.md)
          + [Hive-Spark-Databricks SQL](../../../hive/README.md)
          + [Redshift](../../../redshift/README.md)
          + [PostgreSQL-Greenplum-Netezza](../../README.md)

            - [Built-in Functions](../../postgresql-built-in-functions.md)
            - [Data Types](../../data-types/postgresql-data-types.md)
            - [String Comparison](../../postgresql-string-comparison.md)
            - DDLs

              - [CREATE MATERIALIZED VIEW](../create-materialized-view/postgresql-create-materialized-view.md)
              - [CREATE TABLE](postgresql-create-table.md)

                * [Greenplum](greenplum-create-table.md)
                * [Netezza](netezza-create-table.md)
              - [CREATE VIEW](../postgresql-create-view.md)
            - [Expressions](../../postgresql-expressions.md)
            - [Interactive Terminal](../../postgresql-interactive-terminal.md)
            - ETL And BI Repointing

              - [Power BI PostgreSQL Repointing](../../etl-bi-repointing/power-bi-postgres-repointing.md)
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

[Guides](../../../../../../guides/README.md)[Migrations](../../../../../README.md)Tools[SnowConvert AI](../../../../overview.md)Translation References[PostgreSQL-Greenplum-Netezza](../../README.md)DDLsCREATE TABLE

# SnowConvert AI - PostgreSQL - CREATE TABLE[¶](#snowconvert-ai-postgresql-create-table "Link to this heading")

Translation from PostgreSql to Snowflake

## Applies to[¶](#applies-to "Link to this heading")

* PostgreSQL
* Greenplum
* Netezza

## Description[¶](#description "Link to this heading")

Creates a new table in PostgreSQL. You define a list of columns, each of which holds data of a distinct type. The owner of the table is the issuer of the CREATE TABLE command.

For more information, please refer to `CREATE TABLE` documentation.

## Grammar Syntax[¶](#grammar-syntax "Link to this heading")

```
CREATE [ [ GLOBAL | LOCAL ] { TEMPORARY | TEMP } | UNLOGGED ] TABLE [ IF NOT EXISTS ] table_name ( [
  { column_name data_type [ STORAGE { PLAIN | EXTERNAL | EXTENDED | MAIN | DEFAULT } ] [ COMPRESSION compression_method ] [ COLLATE collation ] [ column_constraint [ ... ] ]
    | table_constraint
    | LIKE source_table [ like_option ... ] }
    [, ... ]
] )
[ INHERITS ( parent_table [, ... ] ) ]
[ PARTITION BY { RANGE | LIST | HASH } ( { column_name | ( expression ) } [ COLLATE collation ] [ opclass ] [, ... ] ) ]
[ USING method ]
[ WITH ( storage_parameter [= value] [, ... ] ) | WITHOUT OIDS ]
[ ON COMMIT { PRESERVE ROWS | DELETE ROWS | DROP } ]
[ TABLESPACE tablespace_name ]

CREATE [ [ GLOBAL | LOCAL ] { TEMPORARY | TEMP } | UNLOGGED ] TABLE [ IF NOT EXISTS ] table_name
    OF type_name [ (
  { column_name [ WITH OPTIONS ] [ column_constraint [ ... ] ]
    | table_constraint }
    [, ... ]
) ]
[ PARTITION BY { RANGE | LIST | HASH } ( { column_name | ( expression ) } [ COLLATE collation ] [ opclass ] [, ... ] ) ]
[ USING method ]
[ WITH ( storage_parameter [= value] [, ... ] ) | WITHOUT OIDS ]
[ ON COMMIT { PRESERVE ROWS | DELETE ROWS | DROP } ]
[ TABLESPACE tablespace_name ]

CREATE [ [ GLOBAL | LOCAL ] { TEMPORARY | TEMP } | UNLOGGED ] TABLE [ IF NOT EXISTS ] table_name
    PARTITION OF parent_table [ (
  { column_name [ WITH OPTIONS ] [ column_constraint [ ... ] ]
    | table_constraint }
    [, ... ]
) ] { FOR VALUES partition_bound_spec | DEFAULT }
[ PARTITION BY { RANGE | LIST | HASH } ( { column_name | ( expression ) } [ COLLATE collation ] [ opclass ] [, ... ] ) ]
[ USING method ]
[ WITH ( storage_parameter [= value] [, ... ] ) | WITHOUT OIDS ]
[ ON COMMIT { PRESERVE ROWS | DELETE ROWS | DROP } ]
[ TABLESPACE tablespace_name ]

where column_constraint is:

[ CONSTRAINT constraint_name ]
{ NOT NULL |
  NULL |
  CHECK ( expression ) [ NO INHERIT ] |
  DEFAULT default_expr |
  GENERATED ALWAYS AS ( generation_expr ) STORED |
  GENERATED { ALWAYS | BY DEFAULT } AS IDENTITY [ ( sequence_options ) ] |
  UNIQUE [ NULLS [ NOT ] DISTINCT ] index_parameters |
  PRIMARY KEY index_parameters |
  REFERENCES reftable [ ( refcolumn ) ] [ MATCH FULL | MATCH PARTIAL | MATCH SIMPLE ]
    [ ON DELETE referential_action ] [ ON UPDATE referential_action ] }
[ DEFERRABLE | NOT DEFERRABLE ] [ INITIALLY DEFERRED | INITIALLY IMMEDIATE ]

and table_constraint is:

[ CONSTRAINT constraint_name ]
{ CHECK ( expression ) [ NO INHERIT ] |
  UNIQUE [ NULLS [ NOT ] DISTINCT ] ( column_name [, ... ] ) index_parameters |
  PRIMARY KEY ( column_name [, ... ] ) index_parameters |
  EXCLUDE [ USING index_method ] ( exclude_element WITH operator [, ... ] ) index_parameters [ WHERE ( predicate ) ] |
  FOREIGN KEY ( column_name [, ... ] ) REFERENCES reftable [ ( refcolumn [, ... ] ) ]
    [ MATCH FULL | MATCH PARTIAL | MATCH SIMPLE ] [ ON DELETE referential_action ] [ ON UPDATE referential_action ] }
[ DEFERRABLE | NOT DEFERRABLE ] [ INITIALLY DEFERRED | INITIALLY IMMEDIATE ]

and like_option is:

{ INCLUDING | EXCLUDING } { COMMENTS | COMPRESSION | CONSTRAINTS | DEFAULTS | GENERATED | IDENTITY | INDEXES | STATISTICS | STORAGE | ALL }

and partition_bound_spec is:

IN ( partition_bound_expr [, ...] ) |
FROM ( { partition_bound_expr | MINVALUE | MAXVALUE } [, ...] )
  TO ( { partition_bound_expr | MINVALUE | MAXVALUE } [, ...] ) |
WITH ( MODULUS numeric_literal, REMAINDER numeric_literal )

index_parameters in UNIQUE, PRIMARY KEY, and EXCLUDE constraints are:

[ INCLUDE ( column_name [, ... ] ) ]
[ WITH ( storage_parameter [= value] [, ... ] ) ]
[ USING INDEX TABLESPACE tablespace_name ]

exclude_element in an EXCLUDE constraint is:

{ column_name | ( expression ) } [ COLLATE collation ] [ opclass [ ( opclass_parameter = value [, ... ] ) ] ] [ ASC | DESC ] [ NULLS { FIRST | LAST } ]

referential_action in a FOREIGN KEY/REFERENCES constraint is:

{ NO ACTION | RESTRICT | CASCADE | SET NULL [ ( column_name [, ... ] ) ] | SET DEFAULT [ ( column_name [, ... ] ) ] }
```

Copy

## Tables Options[¶](#tables-options "Link to this heading")

### TEMPORARY | TEMP, or IF NOT EXISTS[¶](#temporary-temp-or-if-not-exists "Link to this heading")

Hint

This syntax is fully supported in Snowflake.

### GLOBAL | LOCAL[¶](#global-local "Link to this heading")

Note

This syntax is not needed in Snowflake.

According to PostgreSQL’s documentation, GLOBAL | LOCAL are present for SQL Standard compatibility, but have no effect in PostgreSQL and are deprecated. For that reason, SnowConvert AI will remove these keyworks during the migration process.

#### Sample Source[¶](#sample-source "Link to this heading")

Input Code:

##### PostgreSQL[¶](#postgresql "Link to this heading")

```
CREATE GLOBAL TEMP TABLE TABLE1 (
   COL1 integer
);
```

Copy

Output Code:

##### Snowflake[¶](#snowflake "Link to this heading")

```
CREATE TEMPORARY TABLE TABLE1 (
   COL1 integer
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "postgresql",  "convertedOn": "05/09/2025",  "domain": "no-domain-provided" }}';
```

Copy

### UNLOGGED TABLE[¶](#unlogged-table "Link to this heading")

Note

This syntax is not needed in Snowflake.

UNLOGGED tables offer a significant speed advantage because they are not written to the write-ahead log. Snowflake doesn’t support this functionality, so the `UNLOGGED` clause will be commented out.

### Code Example[¶](#code-example "Link to this heading")

#### Input Code:[¶](#input-code "Link to this heading")

##### Greenplum[¶](#greenplum "Link to this heading")

```
CREATE UNLOGGED TABLE TABLE1 (
  COL1 integer
);
```

Copy

#### Output Code:[¶](#output-code "Link to this heading")

##### Snowflake[¶](#id1 "Link to this heading")

```
CREATE
--       --** SSC-FDM-PG0005 - UNLOGGED TABLE IS NOT SUPPORTED IN SNOWFLAKE, DATA WRITTEN MAY HAVE DIFFERENT PERFORMANCE. **
--       UNLOGGED
                TABLE TABLE1 (
   COL1 integer
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "postgresql",  "convertedOn": "05/09/2025",  "domain": "no-domain-provided" }}';
```

Copy

## Column Attributes[¶](#column-attributes "Link to this heading")

### CHECK Attribute[¶](#check-attribute "Link to this heading")

Danger

This syntax is not supported in Snowflake.

The CHECK clause specifies an expression producing a Boolean result that new or updated rows must satisfy for an insert or update operation to succeed. Snowflake does not have an equivalence with this clause; SnowConvert AI will add an EWI. This will be applied as a CHECK attribute or table constraint.

Grammar Syntax

```
CHECK  ( <expression> )
```

Copy

#### Sample Source[¶](#id2 "Link to this heading")

Input Code:

##### PostgreSQL[¶](#id3 "Link to this heading")

```
CREATE TABLE table1 (
    product_id INT PRIMARY KEY,
    quantity INT CHECK (quantity >= 0)
);
```

Copy

Output Code:

##### Snowflake[¶](#id4 "Link to this heading")

```
CREATE TABLE table1 (
    product_id INT PRIMARY KEY,
    quantity INT
                 !!!RESOLVE EWI!!! /*** SSC-EWI-0035 - CHECK STATEMENT NOT SUPPORTED ***/!!! CHECK (quantity >= 0)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "postgresql",  "convertedOn": "05/09/2025",  "domain": "no-domain-provided" }}';
```

Copy

### GENERATED BY DEFAULT AS IDENTITY[¶](#generated-by-default-as-identity "Link to this heading")

Hint

This syntax is fully supported in Snowflake.

Specifies that the column is a default IDENTITY column and enables you to assign a unique value to the column automatically.

Grammar Syntax

```
 GENERATED { ALWAYS | BY DEFAULT } AS IDENTITY [ ( <sequence_options> ) ]
```

Copy

#### Sample Source[¶](#id5 "Link to this heading")

Input Code:

##### PostgreSQL[¶](#id6 "Link to this heading")

```
CREATE TABLE table1 (
idValue INTEGER GENERATED ALWAYS AS IDENTITY)
```

Copy

Output Code:

##### Snowflake[¶](#id7 "Link to this heading")

```
CREATE TABLE table1 (
idValue INTEGER IDENTITY(1, 1) ORDER
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "postgresql",  "convertedOn": "05/09/2025",  "domain": "no-domain-provided" }}'
```

Copy

## Table Constraints[¶](#table-constraints "Link to this heading")

### Primary Key, Foreign Key, and Unique[¶](#primary-key-foreign-key-and-unique "Link to this heading")

Warning

This syntax is partially supported in Snowflake.

SnowConvert AI keeps the constraint definitions; however, in Snowflake, unique, primary, and foreign keys are used for documentation and do not enforce constraints or uniqueness. They help describe table relationships but don’t impact data integrity or performance.

## Table Attributes[¶](#table-attributes "Link to this heading")

### LIKE option[¶](#like-option "Link to this heading")

Warning

This syntax is partially supported in Snowflake.

The `LIKE` clause specifies a table from which the new table automatically copies all column names, their data types, and their not-null constraints. PostgreSQL supports several options, while Snowflake does not so that SnowConvert AI will remove the options like.

#### Grammar Syntax[¶](#id8 "Link to this heading")

```
  LIKE source_table { INCLUDING | EXCLUDING }
  { AM | COMMENTS | CONSTRAINTS | DEFAULTS | ENCODING | GENERATED | IDENTITY | INDEXES | RELOPT | STATISTICS | STORAGE | ALL }
```

Copy

#### Sample Source Patterns[¶](#sample-source-patterns "Link to this heading")

Input Code:

##### PostgreSQL[¶](#id9 "Link to this heading")

```
CREATE TABLE source_table (
    id INT,
    name VARCHAR(255),
    created_at TIMESTAMP,
    status BOOLEAN
);

CREATE TABLE target_table_no_constraints (LIKE source_table INCLUDING DEFAULTS EXCLUDING CONSTRAINTS EXCLUDING INDEXES);
```

Copy

Output Code:

##### Snowflake[¶](#id10 "Link to this heading")

```
CREATE TABLE source_table (
    id INT,
    name VARCHAR(255),
    created_at TIMESTAMP,
    status BOOLEAN
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "postgresql",  "convertedOn": "05/12/2025",  "domain": "no-domain-provided" }}';
CREATE TABLE target_table_no_constraints LIKE source_table;
```

Copy

### ON COMMIT[¶](#on-commit "Link to this heading")

Warning

This syntax is partially supported.

Specifies the behaviour of the temporary table when a commit is done.

#### Grammar Syntax[¶](#id11 "Link to this heading")

```
ON COMMIT { PRESERVE ROWS | DELETE ROWS | DROP }
```

Copy

## Sample Source Patterns[¶](#id12 "Link to this heading")

### Input Code:[¶](#id13 "Link to this heading")

#### PostgreSQL[¶](#id14 "Link to this heading")

```
CREATE GLOBAL TEMPORARY TABLE temp_data_delete (
    id INT,
    data TEXT
) ON COMMIT DELETE ROWS;
```

Copy

#### Output Code:[¶](#id15 "Link to this heading")

##### Snowflake[¶](#id16 "Link to this heading")

```
CREATE TEMPORARY TABLE temp_data_delete (
    id INT,
    data TEXT
)
----** SSC-FDM-0008 - ON COMMIT NOT SUPPORTED **
--ON COMMIT DELETE ROWS
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "postgresql",  "convertedOn": "05/12/2025",  "domain": "no-domain-provided" }}';
```

Copy

### PARTITION BY, USING, TABLESPACE, and WITH[¶](#partition-by-using-tablespace-and-with "Link to this heading")

Note

This syntax is not needed in Snowflake.

These clauses in Snowflake are unnecessary because they automatically handle the data storage, unlike PostgreSQL, which could be set up manually. For this reason, these clauses are removed during migration.

## Related EWIs[¶](#related-ewis "Link to this heading")

1. [SSC-EWI-0035](../../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0035): Check statement not supported.
2. [SSC-FDM-PG0005](../../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/postgresqlFDM.html#ssc-fdm-pg0005): UNLOGGED Table is not supported in Snowflake; data written may have different performance.
3. [SSC-FDM-0008](../../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0008): On Commit not supported.

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
2. [Description](#description)
3. [Grammar Syntax](#grammar-syntax)
4. [Tables Options](#tables-options)
5. [Column Attributes](#column-attributes)
6. [Table Constraints](#table-constraints)
7. [Table Attributes](#table-attributes)
8. [Sample Source Patterns](#id12)
9. [Related EWIs](#related-ewis)