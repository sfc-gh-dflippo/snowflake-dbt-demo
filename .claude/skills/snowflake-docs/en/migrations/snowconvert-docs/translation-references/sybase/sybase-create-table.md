---
auto_generated: true
description: Creates a new table in the current database. You define a list of columns,
  which each hold data of a distinct type. The owner of the table is the issuer of
  the CREATE TABLE command.
last_scraped: '2026-01-14T16:53:56.308499+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/sybase/sybase-create-table
title: SnowConvert AI - Sybase IQ - CREATE TABLE | Snowflake Documentation
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)Translation References[Sybase IQ](README.md)StatementsCREATE TABLE

# SnowConvert AI - Sybase IQ - CREATE TABLE[¶](#snowconvert-ai-sybase-iq-create-table "Link to this heading")

## Description[¶](#description "Link to this heading")

Creates a new table in the current database. You define a list of columns, which each hold data of a distinct type. The owner of the table is the issuer of the CREATE TABLE command.

For more information, please refer to [`CREATE TABLE`](https://help.sap.com/docs/SAP_IQ/a898e08b84f21015969fa437e89860c8/a619764084f21015b8039a8346dc622c.html) documentation.

## Grammar Syntax [¶](#grammar-syntax "Link to this heading")

```
 CREATE [ { GLOBAL | LOCAL } TEMPORARY ] TABLE
   [ IF NOT EXISTS ] [ <owner>. ]<table-name>
   … ( <column-definition> [ <column-constraint> ] … 
   [ , <column-definition> [ <column-constraint> ] …]
   [ , <table-constraint> ] … ) 
   |{ ENABLE | DISABLE } RLV STORE
  
   …[ IN <dbspace-name> ]
   …[ ON COMMIT { DELETE | PRESERVE } ROWS ]
   [ AT <location-string> ]
   [PARTITION BY 
     <range-partitioning-scheme>
     | <hash-partitioning-scheme> 
     | <composite-partitioning-scheme> ]

<column-definition> ::=
   <column-name> <data-type> 
    [ [ NOT ] NULL ] 
    [ DEFAULT <default-value> | IDENTITY ] 
    [ PARTITION | SUBPARTITION ( <partition-name> IN  <dbspace-name> [ , ... ] ) ]

<default-value> ::=
   <special-value>
   | <string>
   | <global variable>
   | [ - ] <number>
   | ( <constant-expression> )
   | <built-in-function>( <constant-expression> )
   | AUTOINCREMENT
   | CURRENT DATABASE
   | CURRENT REMOTE USER
   | NULL
   | TIMESTAMP
   | LAST USER

<special-value> ::=
   CURRENT 
   { DATE | TIME | TIMESTAMP | USER | PUBLISHER }
   | USER

<column-constraint> ::=
   IQ UNIQUE ( <integer> )
   | { [ CONSTRAINT <constraint-name> ] 
     { UNIQUE  
        | PRIMARY KEY  
        | REFERENCES <table-name> [ ( <column-name> ) ] [ ON { UPDATE | DELETE } RESTRICT ] }
      [ IN <dbspace-name> ]
      | CHECK ( <condition> )
   }

<table-constraint> ::=
    [ CONSTRAINT <constraint-name> ] 
   {  { UNIQUE | PRIMARY KEY } ( <column-name> [ , … ] )  
     [ IN <dbspace-name> ]
     | <foreign-key-constraint>
     | CHECK ( <condition> )
   }

<foreign-key-constraint> ::=
   FOREIGN KEY [ <role-name> ] [ ( <column-name> [ , <column-name> ] … ) ] 
   …REFERENCES <table-name> [ ( <column-name> [ , <column-name> ] … ) ]
   …[ <actions> ] [ IN <dbspace-name> ]

<actions> ::=
   [ ON { UPDATE | DELETE } RESTRICT ]

<location-string> ::=
   { <remote-server-name>. [ <db-name> ].[ <owner> ].<object-name>
      | <remote-server-name>; [ <db-name> ]; [ <owner> ];<object-name> }

<range-partitioning-scheme> ::=
   RANGE ( <partition-key> ) ( <range-partition-decl> [,<range-partition-decl> … ] )

<partition-key> ::= <column-name>

<range-partition-declaration> ::=
    <range-partition-name> VALUES <= ( {<constant> |  MAX } ) [ IN <dbspace-name> ]

<hash-partitioning-scheme> ::=
   HASH ( <partition-key> [ , <partition-key>, … ] )

<composite-partitioning-scheme> ::=
   <hash-partitioning-scheme> SUBPARTITION BY <range-partitioning-scheme>
```

Copy

## TEMPORARY TABLES[¶](#temporary-tables "Link to this heading")

### Description[¶](#id1 "Link to this heading")

In Sybase IQ `GLOBAL | LOCAL TEMPORARY` is used to create temporary tables that exist only for the session. These tables are session-specific and automatically deleted when the session ends. They help store intermediate results or work data without affecting the permanent database schema. It also can be created only by adding an `#` at the beginning of the name.

Warning

This syntax is partially supported in Snowflake.

### Grammar Syntax[¶](#id2 "Link to this heading")

```
 CREATE [ { GLOBAL | LOCAL } TEMPORARY ] TABLE
```

Copy

### Sample Source Patterns[¶](#sample-source-patterns "Link to this heading")

#### Input Code:[¶](#input-code "Link to this heading")

##### Sybase[¶](#sybase "Link to this heading")

```
 CREATE LOCAL TEMPORARY TABLE TABLE01 (
    col1 INTEGER
);

CREATE GLOBAL TEMPORARY TABLE TABLE02 (
    col1 INTEGER
);

CREATE TABLE #TABLE03(
    col1 INTEGER
);
```

Copy

##### Output Code:[¶](#output-code "Link to this heading")

##### Sybase[¶](#id3 "Link to this heading")

```
 CREATE OR REPLACE TEMPORARY TABLE TABLE01 (
    col1 INTEGER
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "sybase",  "convertedOn": "03/19/2025",  "domain": "test" }}'
;

--** SSC-FDM-0009 - GLOBAL TEMPORARY TABLE FUNCTIONALITY NOT SUPPORTED. **
CREATE OR REPLACE TABLE TABLE02 (
    col1 INTEGER
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "sybase",  "convertedOn": "03/19/2025",  "domain": "test" }}'
;

CREATE OR REPLACE TEMPORARY TABLE T_TABLE03 (
    col1 INTEGER
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "sybase",  "convertedOn": "03/19/2025",  "domain": "test" }}'
;
```

Copy

### Related EWIs[¶](#related-ewis "Link to this heading")

[SSC-FDM-0009](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0009): GLOBAL TEMPORARY TABLE functionality not supported.

## IF NOT EXISTS[¶](#if-not-exists "Link to this heading")

### Description[¶](#id4 "Link to this heading")

> Ensures the table is created only if it does not already exist, preventing duplication and errors in your SQL script. ([Sybase SQL Language Reference](https://help.sap.com/docs/SAP_IQ/a898e08b84f21015969fa437e89860c8/a619764084f21015b8039a8346dc622c.html)).

SuccessPlaceholder

This syntax is fully supported in Snowflake.

### Grammar Syntax[¶](#id5 "Link to this heading")

```
 IF NOT EXISTS
```

Copy

### Sample Source Patterns[¶](#id6 "Link to this heading")

#### Input Code:[¶](#id7 "Link to this heading")

##### Sybase[¶](#id8 "Link to this heading")

```
 CREATE TABLE IF NOT EXISTS table1 (
    col1 INTEGER
);
```

Copy

##### Output Code:[¶](#id9 "Link to this heading")

##### Snowflake[¶](#snowflake "Link to this heading")

```
 CREATE TABLE IF NOT EXISTS table1 (
    col1 INTEGER
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "sybase",  "convertedOn": "03/19/2024" }}';
```

Copy

## (ENABLE | DISABLE) RLV STORE[¶](#enable-disable-rlv-store "Link to this heading")

### Description[¶](#id10 "Link to this heading")

> Controls Row-Level Versioning Store functionality. ([Sybase SQL Language Reference](https://help.sap.com/docs/SAP_IQ/a898e08b84f21015969fa437e89860c8/a619764084f21015b8039a8346dc622c.html)).

Note

This syntax is not needed in Snowflake.

### Grammar Syntax[¶](#id11 "Link to this heading")

```
 { ENABLE | DISABLE } RLV STORE
```

Copy

### Sample Source Patterns[¶](#id12 "Link to this heading")

#### Input Code:[¶](#id13 "Link to this heading")

##### Sybase[¶](#id14 "Link to this heading")

```
 CREATE TABLE rlv_table
(id INT)
ENABLE RLV STORE;
```

Copy

##### Output Code:[¶](#id15 "Link to this heading")

##### Snowflake[¶](#id16 "Link to this heading")

```
 CREATE OR REPLACE TABLE rlv_table
(
id INT
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "sybase",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
;
```

Copy

## IN DBSPACE[¶](#in-dbspace "Link to this heading")

### Description[¶](#id17 "Link to this heading")

> Specifies the DB space for data storage. ([Sybase SQL Language Reference](https://help.sap.com/docs/SAP_IQ/a898e08b84f21015969fa437e89860c8/a619764084f21015b8039a8346dc622c.html)).

Note

This syntax is not needed in Snowflake. Snowflake automatically handles storage.

### Grammar Syntax[¶](#id18 "Link to this heading")

```
 IN <dbspace-name>
```

Copy

### Sample Source Patterns[¶](#id19 "Link to this heading")

#### Input Code:[¶](#id20 "Link to this heading")

##### Sybase[¶](#id21 "Link to this heading")

```
 CREATE TABLE dbspace_table (
    id INT PRIMARY KEY
) 
IN my_dbspace;
```

Copy

##### Output Code:[¶](#id22 "Link to this heading")

##### Snowflake[¶](#id23 "Link to this heading")

```
 CREATE OR REPLACE TABLE dbspace_table (
    id INT PRIMARY KEY
);
```

Copy

## ON COMMIT[¶](#on-commit "Link to this heading")

### Description[¶](#id24 "Link to this heading")

> Specifies the behaviour of the temporary table when a commit is done. ([Sybase SQL Language Reference](https://help.sap.com/docs/SAP_IQ/a898e08b84f21015969fa437e89860c8/a619764084f21015b8039a8346dc622c.html))

Warning

This syntax is partially supported.

### Grammar Syntax[¶](#id25 "Link to this heading")

```
 [ ON COMMIT { DELETE | PRESERVE } ROWS ]
```

Copy

### Sample Source Patterns[¶](#id26 "Link to this heading")

#### Input Code:[¶](#id27 "Link to this heading")

##### Sybase[¶](#id28 "Link to this heading")

```
 CREATE LOCAL TEMPORARY TABLE temp_employees (
    DATA VARCHAR(255)
) ON COMMIT DELETE ROWS;  

CREATE LOCAL TEMPORARY TABLE temp_projects (
    DATA VARCHAR(255)
) ON COMMIT PRESERVE ROWS;
```

Copy

##### Output Code:[¶](#id29 "Link to this heading")

##### Snowflake[¶](#id30 "Link to this heading")

```
 CREATE OR REPLACE TEMPORARY TABLE temp_employees (
    DATA VARCHAR(255)
)
--    --** SSC-FDM-0008 - ON COMMIT NOT SUPPORTED **
--    ON COMMIT DELETE ROWS
    COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "sybase",  "convertedOn": "03/19/2025",  "domain": "test" }}'
;

CREATE OR REPLACE TEMPORARY TABLE temp_projects (
    DATA VARCHAR(255)
) ON COMMIT PRESERVE ROWS
    COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "sybase",  "convertedOn": "03/19/2025",  "domain": "test" }}'
;
```

Copy

### Related EWIs[¶](#id31 "Link to this heading")

[SSC-FDM-0008](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0008): On Commit not supported.

## AT LOCATION[¶](#at-location "Link to this heading")

### Description[¶](#id32 "Link to this heading")

> Creates a remote table (proxy). ([Sybase SQL Language Reference](https://help.sap.com/docs/SAP_IQ/a898e08b84f21015969fa437e89860c8/a619764084f21015b8039a8346dc622c.html))

Danger

This syntax is not supported in Snowflake.

### Grammar Syntax[¶](#id33 "Link to this heading")

```
 AT <location-string>
```

Copy

### Sample Source Patterns[¶](#id34 "Link to this heading")

#### Input Code:[¶](#id35 "Link to this heading")

##### Sybase[¶](#id36 "Link to this heading")

```
 CREATE TABLE t1
( 
    DATA VARCHAR(10)
)
AT 'SERVER_A.db1.joe.t1';
```

Copy

##### Output Code:[¶](#id37 "Link to this heading")

##### Snowflake[¶](#id38 "Link to this heading")

```
 CREATE OR REPLACE TABLE t1
(
    DATA VARCHAR(10)
)
    !!!RESOLVE EWI!!! /*** SSC-EWI-SY0002 - UNSUPPORTED REMOTE TABLE SYNTAX ***/!!!
AT 'SERVER_A.db1.joe.t1'
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "sybase",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
;
```

Copy

### Related EWIs[¶](#id39 "Link to this heading")

[SSC-EWI-SY0002](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/sybaseEWI.html#ssc-ewi-sy0002): UNSUPPORTED REMOTE TABLE SYNTAX.

## PARTITION BY[¶](#partition-by "Link to this heading")

### Description[¶](#id40 "Link to this heading")

> All rows of a table partition are physically colocated. ([Sybase SQL Language Reference](https://help.sap.com/docs/SAP_IQ/a898e08b84f21015969fa437e89860c8/a619764084f21015b8039a8346dc622c.html))

Note

This syntax is not needed in Snowflake.

### Grammar Syntax[¶](#id41 "Link to this heading")

```
 PARTITION BY 
     <range-partitioning-scheme>
     | <hash-partitioning-scheme> 
     | <composite-partitioning-scheme>
     
<range-partitioning-scheme> ::=
   RANGE ( <partition-key> ) ( <range-partition-decl> [,<range-partition-decl> … ] )

<partition-key> ::= <column-name>

<range-partition-declaration> ::=
    <range-partition-name> VALUES <= ( {<constant> |  MAX } ) [ IN <dbspace-name> ]

<hash-partitioning-scheme> ::=
   HASH ( <partition-key> [ , <partition-key>, … ] )

<composite-partitioning-scheme> ::=
   <hash-partitioning-scheme> SUBPARTITION BY <range-partitioning-scheme>
```

Copy

### Sample Source Patterns[¶](#id42 "Link to this heading")

#### Input Code:[¶](#id43 "Link to this heading")

##### Sybase[¶](#id44 "Link to this heading")

```
 -- Range Partitioning
CREATE TABLE sales (
    sale_id INT,
    sale_date DATE,
    amount DECIMAL(10, 2)
)
PARTITION BY RANGE (sale_date) (
    p1 VALUES <= ('2023-01-01'),
    p2 VALUES <= ('2024-01-01'),
    p3 VALUES <= (MAXVALUE)
);

-- Hash Partitioning
CREATE TABLE customers (
    customer_id INT,
    customer_name VARCHAR(255)
)
PARTITION BY HASH (customer_id);

-- Composite Partitioning (Hash-Range)
CREATE TABLE orders (
    order_id INT,
    customer_id INT,
    order_date DATE,
    amount DECIMAL(10,2)
)
PARTITION BY HASH (customer_id)
SUBPARTITION BY RANGE (order_date) (
    p1 VALUES <= ('2023-01-01'),
    p2 VALUES <= ('2024-01-01'),
    p3 VALUES <= (MAXVALUE)
);
```

Copy

##### Output Code:[¶](#id45 "Link to this heading")

##### Snowflake[¶](#id46 "Link to this heading")

```
 -- Range Partitioning
CREATE OR REPLACE TABLE sales (
    sale_id INT,
    sale_date DATE,
    amount DECIMAL(10, 2)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "sybase",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
;

-- Hash Partitioning
CREATE OR REPLACE TABLE customers (
    customer_id INT,
    customer_name VARCHAR(255)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "sybase",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
;

-- Composite Partitioning (Hash-Range)
CREATE OR REPLACE TABLE orders (
    order_id INT,
    customer_id INT,
    order_date DATE,
    amount DECIMAL(10,2)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "sybase",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
;
```

Copy

## CONSTRAINTS[¶](#constraints "Link to this heading")

### Description[¶](#id47 "Link to this heading")

> This ensures the accuracy and reliability of the data in the table. If there is any violation between the constraint and the data action, the action is aborted. ([Sybase SQL Language Reference](https://help.sap.com/docs/SAP_IQ/a898e08b84f21015969fa437e89860c8/a619764084f21015b8039a8346dc622c.html))

Warning

This syntax is partially supported.

### Grammar Syntax[¶](#id48 "Link to this heading")

```
 <table-constraint> ::=
    [ CONSTRAINT <constraint-name> ] 
   {  { UNIQUE | PRIMARY KEY } ( <column-name> [ , … ] )  
     [ IN <dbspace-name> ]
     | <foreign-key-constraint>
     | CHECK ( <condition> )
   }
   
<foreign-key-constraint> ::=
   FOREIGN KEY [ <role-name> ] [ ( <column-name> [ , <column-name> ] … ) ] 
   …REFERENCES <table-name> [ ( <column-name> [ , <column-name> ] … ) ]
   …[ <actions> ] [ IN <dbspace-name> ]

<actions> ::=
   [ ON { UPDATE | DELETE } RESTRICT ]
```

Copy

### Sample Source Patterns[¶](#id49 "Link to this heading")

#### Input Code:[¶](#id50 "Link to this heading")

##### Sybase[¶](#id51 "Link to this heading")

```
 CREATE TABLE t_constraint (
    id1 INT NOT NULL,
    id2 INT PRIMARY KEY,
    age INT CHECK (age >= 18),
    email VARCHAR(255) UNIQUE,
    product_id INT REFERENCES products(id) ON DELETE RESTRICT IN SOMEPLACE,
    cod_iq VARCHAR(20) IQ UNIQUE(5),
    CONSTRAINT unq_name_email UNIQUE (name, email),
    CONSTRAINT fk_ord_line FOREIGN KEY (ord_id, line_id) REFERENCES ord_lines(ord_id,line_id)
);
```

Copy

##### Output Code:[¶](#id52 "Link to this heading")

##### Snowflake[¶](#id53 "Link to this heading")

```
 CREATE OR REPLACE TABLE t_constraint (
    id1 INT NOT NULL,
    id2 INT PRIMARY KEY,
    age INT
            !!!RESOLVE EWI!!! /*** SSC-EWI-0035 - CHECK STATEMENT NOT SUPPORTED ***/!!!
            CHECK (age >= 18),
    email VARCHAR(255) UNIQUE,
    product_id INT REFERENCES products (id) ON DELETE RESTRICT ,
    cod_iq VARCHAR(20)
                       !!!RESOLVE EWI!!! /*** SSC-EWI-SY0003 - UNSUPPORTED IQ UNIQUE CONSTRAINT ***/!!!
 IQ UNIQUE(5),
       CONSTRAINT unq_name_email UNIQUE (name, email),
       CONSTRAINT fk_ord_line FOREIGN KEY (ord_id, line_id) REFERENCES ord_lines (ord_id, line_id)
   )
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "sybase",  "convertedOn": "03/19/2025",  "domain": "test" }}'
;
```

Copy

### Related EWIs[¶](#id54 "Link to this heading")

[SSC-EWI-0035](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0035): CHECK STATEMENT NOT SUPPORTED.

[SSC-EWI-SY0003](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/sybaseEWI.html#ssc-ewi-sy0003): UNSUPPORTED IQ UNIQUE CONSTRAINT.

## DEFAULT[¶](#default "Link to this heading")

### Description[¶](#id55 "Link to this heading")

Defines the default value of a column in a create table.

Warning

This syntax is partially supported in Snowflake.

### Grammar Syntax[¶](#id56 "Link to this heading")

```
 <default-value> ::=
   <special-value>
   | <string>
   | <global variable>
   | [ - ] <number>
   | ( <constant-expression> )
   | <built-in-function>( <constant-expression> )
   | AUTOINCREMENT
   | CURRENT DATABASE
   | CURRENT REMOTE USER
   | NULL
   | TIMESTAMP
   | LAST USER

<special-value> ::=
   CURRENT 
   { DATE | TIME | TIMESTAMP | USER | PUBLISHER }
   | USER
```

Copy

### Sample Source Patterns[¶](#id57 "Link to this heading")

#### Input Code:[¶](#id58 "Link to this heading")

##### Sybase[¶](#id59 "Link to this heading")

```
 create table t_defaults
(
col1 timestamp default current utc timestamp,
col2 timestamp default current timestamp,
col3 varchar default current user,
col4 varchar default current remote user,
col5 varchar default last user,
col6 varchar default current publisher,
col7 varchar default current date,
col8 varchar default current database,
col9 varchar default current time,
col10 varchar default user,
col11 int default autoincrement,
col12 int identity,
col13 int default -10, 
col14 int default 'literal', 
col15 int default null
)
;
```

Copy

##### Output Code:[¶](#id60 "Link to this heading")

##### Snowflake[¶](#id61 "Link to this heading")

```
 CREATE OR REPLACE TABLE t_defaults
(
    col1 timestamp default CURRENT_TIMESTAMP,
    col2 timestamp default CURRENT_TIMESTAMP,
    col3 VARCHAR default CURRENT_USER,
    col4 VARCHAR default
                         !!!RESOLVE EWI!!! /*** SSC-EWI-SY0001 - UNSUPPORTED DEFAULT VALUE CURRENT REMOTE USER IN SNOWFLAKE ***/!!! current remote user,
    col5 VARCHAR default
                         !!!RESOLVE EWI!!! /*** SSC-EWI-SY0001 - UNSUPPORTED DEFAULT VALUE LAST USER IN SNOWFLAKE ***/!!! last user,
    col6 VARCHAR default
                         !!!RESOLVE EWI!!! /*** SSC-EWI-SY0001 - UNSUPPORTED DEFAULT VALUE CURRENT PUBLISHER IN SNOWFLAKE ***/!!! current publisher,
    col7 VARCHAR default CURRENT_DATE,
    col8 VARCHAR default CURRENT_DATABASE,
    col9 VARCHAR default CURRENT_TIME,
    col10 VARCHAR DEFAULT CURRENT_USER,
    col11 INT IDENTITY ORDER,
    col12 INT IDENTITY ORDER,
    col13 INT default -10,
    col14 INT default 'literal',
    col15 INT default null
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "sybase",  "convertedOn": "03/19/2025",  "domain": "test" }}'
;
```

Copy

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
3. [TEMPORARY TABLES](#temporary-tables)
4. [IF NOT EXISTS](#if-not-exists)
5. [(ENABLE | DISABLE) RLV STORE](#enable-disable-rlv-store)
6. [IN DBSPACE](#in-dbspace)
7. [ON COMMIT](#on-commit)
8. [AT LOCATION](#at-location)
9. [PARTITION BY](#partition-by)
10. [CONSTRAINTS](#constraints)
11. [DEFAULT](#default)