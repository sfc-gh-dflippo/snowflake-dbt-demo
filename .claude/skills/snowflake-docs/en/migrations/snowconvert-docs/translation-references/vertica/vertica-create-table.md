---
auto_generated: true
description: Creates a table in the logical schema. (Vertica SQL Language Reference
  Create Table).
last_scraped: '2026-01-14T16:54:11.166074+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/vertica/vertica-create-table
title: SnowConvert AI - Vertica - CREATE TABLE | Snowflake Documentation
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)Translation References[Vertica](README.md)CREATE TABLE

# SnowConvert AI - Vertica - CREATE TABLE[¶](#snowconvert-ai-vertica-create-table "Link to this heading")

## Description[¶](#description "Link to this heading")

Creates a table in the logical schema. ([Vertica SQL Language Reference Create Table](https://docs.vertica.com/23.3.x/en/sql-reference/statements/create-statements/create-table/)).

Warning

This syntax is partially supported in Snowflake. Translation pending for these clauses:

```
DISK_QUOTA quota
SET USING expression
ENCODING encoding-type 
ACCESSRANK integer
```

Copy

## Grammar Syntax[¶](#grammar-syntax "Link to this heading")

```
CREATE TABLE [ IF NOT EXISTS ] [[database.]schema.]table
   ( column-definition[,...] [, table-constraint [,...]] )
   [ ORDER BY column[,...] ]
   [ segmentation-spec ]
   [ KSAFE [safety] ]
   [ partition-clause]
   [ {INCLUDE | EXCLUDE} [SCHEMA] PRIVILEGES ]
   [ DISK_QUOTA quota ]
   
<column-definition> ::= 
column-name data-type
    [ column-constraint ][...]
    [ ENCODING encoding-type ]
    [ ACCESSRANK integer ]
    
<column-constraint> ::=
[ { AUTO_INCREMENT | IDENTITY } [ (args) ] ]
[ CONSTRAINT constraint-name ] {
   [ CHECK (expression) [ ENABLED | DISABLED ] ]
   [ [ DEFAULT expression ] [ SET USING expression } | DEFAULT USING expression ]
   [ NULL | NOT NULL ]
   [ { PRIMARY KEY [ ENABLED | DISABLED ] REFERENCES table [( column )] } ]
   [ UNIQUE [ ENABLED | DISABLED ] ]
}
    
<table-constraint>::=
[ CONSTRAINT constraint-name ]
{
... PRIMARY KEY (column[,... ]) [ ENABLED | DISABLED ]
... | FOREIGN KEY (column[,... ] ) REFERENCES table [ (column[,...]) ]
... | UNIQUE (column[,...]) [ ENABLED | DISABLED ]
... | CHECK (expression) [ ENABLED | DISABLED ]
}
```

Copy

## Tables Options[¶](#tables-options "Link to this heading")

### Order By[¶](#order-by "Link to this heading")

In Vertica, this `ORDER BY` clause specifies how data is physically sorted within a **superprojection**, an optimized storage structure for a table. This explicit physical ordering at table creation is not directly supported in Snowflake. For more information please refer to [SSC-EWI-VT0002.](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/verticaEWI.html#ssc-ewi-vt0002)

#### Sample Source[¶](#sample-source "Link to this heading")

##### Vertica[¶](#vertica "Link to this heading")

```
CREATE TABLE metrics 
(
  metric_id INT,
  business_unit VARCHAR(100),
  metric_category VARCHAR(50) NOT NULL,
  measurement_date DATE NOT NULL
)
ORDER BY measurement_date, business_unit, metric_category;
```

Copy

##### Snowflake[¶](#snowflake "Link to this heading")

```
CREATE TABLE metrics
(
  metric_id INT,
  business_unit VARCHAR(100),
  metric_category VARCHAR(50) NOT NULL,
  measurement_date DATE NOT NULL
)
!!!RESOLVE EWI!!! /*** SSC-EWI-VT0002 - ORDER BY TABLE OPTION IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
ORDER BY measurement_date, business_unit, metric_category
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "vertica",  "convertedOn": "06/17/2025",  "domain": "no-domain-provided" }}';
```

Copy

### Projections Clauses[¶](#projections-clauses "Link to this heading")

Vertica’s projections are a mechanism to define and maintain the physical sort order of data on disk, thereby optimizing query performance for specific access patterns. Snowflake, however, utilizes a fundamentally different storage and optimization strategy. Data in Snowflake is automatically broken down into immutable **micro-partitions**, which are then organized and managed by the cloud service.

While an inherent order might exist within these micro-partitions due to insertion or the application of **clustering keys**, Snowflake’s query optimizer and its underlying architecture are designed to efficiently prune these micro-partitions during query execution, regardless of a pre-defined global sort order. This approach, combined with automatic caching and a columnar storage format, allows Snowflake to achieve high performance without requiring users to manually define and manage physical data structures like Vertica’s projections, thus simplifying data management and optimizing for a broader range of query patterns without explicit physical sort definitions.

Due to these reasons, the following clauses aren’t necessary in Snowflake and are removed from the original code:

```
[ segmentation-spec ]
[ KSAFE [safety] ]
[ partition-clause]
```

Copy

### Inherited Schema Privileges Clause[¶](#inherited-schema-privileges-clause "Link to this heading")

`INCLUDE SCHEMA PRIVILEGES` is a Vertica-specific feature that governs how privileges are inherited, in this case, potentially from the schema level. Snowflake does not have a direct equivalent for this clause within its `CREATE TABLE` syntax. Privileges in Snowflake are managed explicitly through `GRANT` statements.

Warning

This syntax is not supported in Snowflake.

#### Sample Source[¶](#id1 "Link to this heading")

##### Vertica[¶](#id2 "Link to this heading")

```
CREATE TABLE metrics 
(
  metric_id INT,
  business_unit VARCHAR(100),
  metric_category VARCHAR(50) NOT NULL,
  measurement_date DATE NOT NULL
)
INCLUDE SCHEMA PRIVILEGES;
```

Copy

##### Snowflake[¶](#id3 "Link to this heading")

```
CREATE TABLE metrics
(
  metric_id INT,
  business_unit VARCHAR(100),
  metric_category VARCHAR(50) NOT NULL,
  measurement_date DATE NOT NULL
)
!!!RESOLVE EWI!!! /*** SSC-EWI-VT0001 - INHERITED PRIVILEGES CLAUSE IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
INCLUDE SCHEMA PRIVILEGES
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "vertica",  "convertedOn": "06/17/2025",  "domain": "no-domain-provided" }}';
```

Copy

## Constraints[¶](#constraints "Link to this heading")

### IDENTITY - AUTO\_INCREMENT[¶](#identity-auto-increment "Link to this heading")

Creates a table column whose values are automatically generated by and managed by the database. You cannot change or load values in this column. You can set this constraint on only one table column.

Success

This syntax is fully supported in Snowflake.

#### Sample Source[¶](#id4 "Link to this heading")

##### Vertica[¶](#id5 "Link to this heading")

```
CREATE TABLE customers (
  id AUTO_INCREMENT(1, 2),
  name VARCHAR(50)
);

CREATE TABLE customers2 (
  id IDENTITY(1, 2),
  name VARCHAR(50)
);
```

Copy

##### Snowflake[¶](#id6 "Link to this heading")

```
CREATE TABLE customers (
  id INT AUTOINCREMENT(1, 2) ORDER,
  name VARCHAR(50)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "vertica",  "convertedOn": "06/17/2025",  "domain": "no-domain-provided" }}';

CREATE TABLE customers2 (
  id INT IDENTITY(1, 2) ORDER,
  name VARCHAR(50)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "vertica",  "convertedOn": "06/17/2025",  "domain": "no-domain-provided" }}';
```

Copy

### CHECK Constraint[¶](#check-constraint "Link to this heading")

The `CHECK` clause in Vertica requires new or updated rows to satisfy a Boolean expression. Snowflake doesn’t have an equivalent to this clause; therefore, SnowConvert AI will add an EWI. This will be applied as a `CHECK` attribute or table constraint in the converted code.

Danger

This syntax is not supported in Snowflake.

#### Sample Source[¶](#id7 "Link to this heading")

##### Vertica[¶](#id8 "Link to this heading")

```
CREATE TABLE table1 (
    product_id INT PRIMARY KEY,
    quantity INT CHECK (quantity >= 0)
);
```

Copy

##### Snowflake[¶](#id9 "Link to this heading")

```
CREATE TABLE table1 (
    product_id INT PRIMARY KEY,
    quantity INT
                 !!!RESOLVE EWI!!! /*** SSC-EWI-0035 - CHECK STATEMENT NOT SUPPORTED ***/!!! CHECK (quantity >= 0)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "vertica",  "convertedOn": "06/17/2025",  "domain": "no-domain-provided" }}';
```

Copy

### DEFAULT Constraint[¶](#default-constraint "Link to this heading")

Warning

This syntax is partially supported in Snowflake.

The basic `DEFAULT` clause from Vertica is fully supported and translates directly to Snowflake. For Vertica’s `DEFAULT USING` clause, however, the translation is partial. Snowflake will correctly apply the `DEFAULT` value when new rows are inserted, but the deferred refresh capability from the `USING` portion has no direct equivalent and some expressions might not be supported in Snowflake. Therefore, a warning is added to highlight this functional difference.

#### Sample Source[¶](#id10 "Link to this heading")

##### Vertica[¶](#id11 "Link to this heading")

```
CREATE TABLE table1 (
    base_value INT,
    status_code INT DEFAULT 0,
    derived_value INT DEFAULT USING (base_value + 100)
);
```

Copy

##### Snowflake[¶](#id12 "Link to this heading")

```
CREATE TABLE table1 (
    base_value INT,
    status_code INT DEFAULT 0,
    derived_value INT DEFAULT (base_value + 100) /*** SSC-FDM-VT0001 - EXPRESSION IN USING CONSTRAINT MIGHT NOT BE SUPPORTED IN SNOWFLAKE ***/
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "vertica",  "convertedOn": "06/17/2025",  "domain": "no-domain-provided" }}';
```

Copy

### PRIMARY KEY - UNIQUE - FOREIGN KEY[¶](#primary-key-unique-foreign-key "Link to this heading")

SnowConvert AI keeps the constraint definitions; however, in Snowflake, these properties are provided to facilitate migrating from other databases. They are not enforced or maintained by Snowflake. This means that the defaults can be changed for these properties, but changing the defaults results in Snowflake not creating the constraint.

Warning

This syntax is partially supported in Snowflake.

#### Sample Source[¶](#id13 "Link to this heading")

##### Vertica[¶](#id14 "Link to this heading")

```
CREATE OR REPLACE TABLE employees (
    emp_id INTEGER,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    CONSTRAINT pk_employees_enabled PRIMARY KEY (emp_id) ENABLED
);
```

Copy

##### Snowflake[¶](#id15 "Link to this heading")

```
CREATE OR REPLACE TABLE employees (
    emp_id INTEGER,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    CONSTRAINT pk_employees_enabled PRIMARY KEY (emp_id) ENABLE
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "vertica",  "convertedOn": "06/17/2025",  "domain": "no-domain-provided" }}';
```

Copy

## Related EWIs[¶](#related-ewis "Link to this heading")

1. [SSC-EWI-0035](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0035): Check statement not supported.
2. [SSC-EWI-VT0001](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/verticaEWI.html#ssc-ewi-vt0001): Inherited privileges clause is not supported in Snowflake.
3. [SSC-EWI-VT0002](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/verticaEWI.html#ssc-ewi-vt0002): Order by table option is not supported in Snowflake.
4. [SSC-FDM-VT0001](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/verticaFDM.html#ssc-fdm-vt0001): Expression in USING constraint might not be supported in Snowflake.

## CREATE TABLE AS[¶](#create-table-as "Link to this heading")

### Description[¶](#id16 "Link to this heading")

Creates and loads a table from the [results of a query](https://docs.vertica.com/23.3.x/en/admin/working-with-native-tables/creating-table-from-other-tables/creating-table-from-query/). ([Vertica SQL Language Reference Create Table](https://docs.vertica.com/23.3.x/en/sql-reference/statements/create-statements/create-table/)).

Warning

This syntax is partially supported in Snowflake. Translation pending for the following clauses

```
[ /*+ LABEL */ ]
[ AT epoch ]
[ ENCODED BY column-ref-list ]
[ ENCODING encoding-type ]
[ ACCESSRANK integer ]
[ GROUPED ( column-reference[,...] ) ]
```

Copy

### Grammar Syntax[¶](#id17 "Link to this heading")

```
CREATE TABLE [ IF NOT EXISTS ] [[database.]schema.]table
[ ( column-name-list ) ]
[ {INCLUDE | EXCLUDE} [SCHEMA] PRIVILEGES ]
AS  [ /*+ LABEL */ ] [ AT epoch ] query [ ENCODED BY column-ref-list ] [ segmentation-spec ]

<column-name-list> ::=
column-name-list
    [ ENCODING encoding-type ]
    [ ACCESSRANK integer ]
    [ GROUPED ( column-reference[,...] ) ]
```

Copy

### Tables Options[¶](#id18 "Link to this heading")

#### Segmentation Clause[¶](#segmentation-clause "Link to this heading")

This syntax isn’t required in Snowflake and is removed from the original code. For more information, please refer to [**Projections Clauses**](#projections-clauses).

Note

This syntax is not required in Snowflake.

#### Inherited Schema Privileges Clause[¶](#id19 "Link to this heading")

`INCLUDE SCHEMA PRIVILEGES` is a Vertica-specific feature that governs how privileges are inherited, in this case, potentially from the schema level. Snowflake does not have a direct equivalent for this clause within its `CREATE TABLE` syntax. For more information please refer to [Inherited Schema Privileges Clause.](#inherited-schema-privileges-clause)

Warning

This syntax is not supported in Snowflake.

### Related EWIs[¶](#id20 "Link to this heading")

1. [SSC-EWI-VT0001](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/verticaEWI.html#ssc-ewi-vt0001): Inherited privileges clause is not supported in Snowflake.

## CREATE TABLE LIKE[¶](#create-table-like "Link to this heading")

### Description[¶](#id21 "Link to this heading")

Creates the table by [replicating an existing table](https://docs.vertica.com/23.3.x/en/admin/working-with-native-tables/creating-table-from-other-tables/replicating-table/). ([Vertica SQL Language Reference Create Table](https://docs.vertica.com/23.3.x/en/sql-reference/statements/create-statements/create-table/)).

Warning

This syntax is partially supported in Snowflake. Translation pending for the following clause:

```
DISK_QUOTA quota
```

Copy

### Grammar Syntax[¶](#id22 "Link to this heading")

```
CREATE TABLE [ IF NOT EXISTS ] [[database.]schema.]table
  LIKE [[database.]schema.]existing-table
  [ {INCLUDING | EXCLUDING} PROJECTIONS ]
  [ {INCLUDE | EXCLUDE} [SCHEMA] PRIVILEGES ]
  [ DISK_QUOTA quota ]
```

Copy

### Tables Options[¶](#id23 "Link to this heading")

#### Projections[¶](#projections "Link to this heading")

This syntax isn’t required in Snowflake and is removed from the original code. For more information, please refer to [**Projections Clauses**](#projections-clauses).

Warning

This syntax is not required in Snowflake.

#### Inherited Schema Privileges Clause[¶](#id24 "Link to this heading")

`INCLUDE SCHEMA PRIVILEGES` is a Vertica-specific feature that governs how privileges are inherited, in this case, potentially from the schema level. Snowflake does not have a direct equivalent for this clause within its `CREATE TABLE` syntax. For more information please refer to [Inherited Schema Privileges Clause.](#inherited-schema-privileges-clause)

Warning

This syntax is not supported in Snowflake.

### Related EWIs[¶](#id25 "Link to this heading")

1. [SSC-EWI-VT0001](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/verticaEWI.html#ssc-ewi-vt0001): Inherited privileges clause is not supported in Snowflake.

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
3. [Tables Options](#tables-options)
4. [Constraints](#constraints)
5. [Related EWIs](#related-ewis)
6. [CREATE TABLE AS](#create-table-as)
7. [CREATE TABLE LIKE](#create-table-like)