---
auto_generated: true
description: This is a translation reference to convert Oracle Create Type Statements
  (UDT’s) to snowflake
last_scraped: '2026-01-14T16:53:30.124928+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/oracle/sql-translation-reference/create_type
title: SnowConvert AI - Oracle - Create Type | Snowflake Documentation
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
          + [Teradata](../../teradata/README.md)
          + [Oracle](../README.md)

            - [Sample Data](../sample-data.md)
            - Basic Elements of Oracle SQL

              - [Literals](../basic-elements-of-oracle-sql/literals.md)
              - [Data Types](../basic-elements-of-oracle-sql/data-types/README.md)
            - [Pseudocolumns](../pseudocolumns.md)
            - [Built-in Functions](../functions/README.md)
            - [Built-in Packages](../built-in-packages.md)
            - [SQL Queries and Subqueries](../sql-queries-and-subqueries/selects.md)
            - [SQL Statements](README.md)

              * [CREATE TABLE](create-table.md)
              * [CREATE VIEW](create-view.md)
              * [CREATE MATERIALIZED VIEW](create-materialized-view.md)
              * [CREATE TYPE](create_type.md)
            - [PL/SQL to Snowflake Scripting](../pl-sql-to-snowflake-scripting/README.md)
            - [PL/SQL to Javascript](../pl-sql-to-javascript/README.md)
            - [SQL Plus](../sql-plus.md)
            - [Wrapped Objects](../wrapped-objects.md)
            - ETL And BI Repointing

              - [Power BI Oracle Repointing](../etl-bi-repointing/power-bi-oracle-repointing.md)
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

[Guides](../../../../../guides/README.md)[Migrations](../../../../README.md)Tools[SnowConvert AI](../../../overview.md)Translation References[Oracle](../README.md)[SQL Statements](README.md)CREATE TYPE

# SnowConvert AI - Oracle - Create Type[¶](#snowconvert-ai-oracle-create-type "Link to this heading")

This is a translation reference to convert Oracle Create Type Statements (UDT’s) to snowflake

## General Description[¶](#general-description "Link to this heading")

One of the most important features the Oracle database engine offers is an Object-Oriented approach. PL/SQL offers capabilities beyond other relational databases in the form of OOP by using Java-like statements in the form of packages, functions, tables and types. This document will cover the last one and how SnowConvert AI solves it, remaining compliant to functionality.

Oracle supports the following specifications:

* Abstract Data Type (*ADT*) (*including an SQLJ object type*).
* Standalone varying array (*varray*) type.
* Standalone nested table type.
* Incomplete object type.

All this according to the information found in [Oracle Create Type Statement Documentation](https://docs.oracle.com/en/database/oracle/oracle-database/21/lnpls/CREATE-TYPE-statement.html#GUID-389D603D-FBD0-452A-8414-240BBBC57034)

```
CREATE [ OR REPLACE ] [ EDITIONABLE | NONEDITIONAL ] TYPE <type name>
[ <type source creation options> ]
[<type definition>]
[ <type properties> ]
```

Copy

## Limitations[¶](#limitations "Link to this heading")

Snowflake doesn’t support user-defined data types, according to its online documentation [Unsupported Data Types](https://docs.snowflake.com/en/sql-reference/data-types-unsupported.html), but it supports [Semi-structured Data Types](https://docs.snowflake.com/en/sql-reference/data-types-semistructured.html), which can be used to mimic the hierarchy-like structure of most User-defined types. For this reason, there are multiple type features that have no workaround.

Following are the User Defined Types features for which **NO** workaround is proposed:

### Subtypes: Type Hierarchy[¶](#subtypes-type-hierarchy "Link to this heading")

These statements aren’t supported in Snowflake. SnowConvert AI only recognizes them, but no translation is offered.

```
CREATE TYPE person_t AS OBJECT (name VARCHAR2(100), ssn NUMBER) 
   NOT FINAL;
/

CREATE TYPE employee_t UNDER person_t 
   (department_id NUMBER, salary NUMBER) 
   NOT FINAL;
/

CREATE TYPE part_time_emp_t UNDER employee_t (num_hrs NUMBER);
/
```

Copy

### Type properties[¶](#type-properties "Link to this heading")

These refer to the options that are normally used when using OOP in PL/SQL: Persistable, Instantiable and Final.

```
CREATE OR REPLACE TYPE type1 AS OBJECT () NOT FINAL NOT INSTANTIABLE NOT PERSISTABLE;
CREATE OR REPLACE TYPE type2 AS OBJECT () FINAL INSTANTIABLE PERSISTABLE;
```

Copy

### Nested Table Type[¶](#nested-table-type "Link to this heading")

These statements aren’t supported in Snowflake. SnowConvert AI only recognizes them, but no translation is offered.

```
CREATE TYPE textdoc_typ AS OBJECT
    ( document_typ      VARCHAR2(32)
    , formatted_doc     BLOB
    ) ;
/

CREATE TYPE textdoc_tab AS TABLE OF textdoc_typ;
/
```

Copy

### Type Source Creation Options[¶](#type-source-creation-options "Link to this heading")

These options stand for custom options regarding access and querying the type.

```
CREATE TYPE type1 FORCE OID 'abc' SHARING = METADATA DEFAULT COLLATION schema1.collation ACCESSIBLE BY (schema1.unitaccesor) AS OBJECT ();
CREATE TYPE type2 FORCE OID 'abc' SHARING = NONE DEFAULT COLLATION collation ACCESSIBLE BY (PROCEDURE unitaccesor) AS OBJECT ();
CREATE TYPE type3 AUTHID CURRENT_USER AS OBJECT ();
CREATE TYPE type4 AUTHID DEFINER AS OBJECT ();
```

Copy

## Proposed workarounds[¶](#proposed-workarounds "Link to this heading")

### About types definition[¶](#about-types-definition "Link to this heading")

For the definition, the proposed workaround is to create semi-structure data type to mimic Oracle’s data type.

### About types member function[¶](#about-types-member-function "Link to this heading")

For the member functions containing logic and DML, the proposed workaround relies on helpers to translate this into stored procedures.

## Current SnowConvert AI Support[¶](#current-snowconvert-ai-support "Link to this heading")

The next table shows a summary of the current support provided by the SnowConvert AI tool. Please keep into account that translations may still not be final, and more work may be needed.

| Type Statement Element | Current recognition status | Current translation status | Has Known Workarounds |
| --- | --- | --- | --- |
| [Object Type Definitions](#object-type-definition) | Recognized. | Partially Translated. | Yes. |
| [Subtype Definitions](#subtype-definition) | Recognized. | Not Translated. | No. |
| [Array Type Definitions](#array-type-definition) | Recognized. | Not Translated. | Yes. |
| [Nested Table Definitions](#nested-table-type) | Recognized. | Not Translated. | No. |
| [Member Function Definitions](#member-function-definitions) | Recognized. | Not Translated. | Yes. |

## Known Issues[¶](#known-issues "Link to this heading")

### 1. DML usages for Object Types are not being transformed[¶](#dml-usages-for-object-types-are-not-being-transformed "Link to this heading")

As of now, only DDL definitions that use User-Defined Types are being transformed into Variant. This means that any Inserts, Updates or Deletes using User-defined Types are not being transformed and need to be manually transformed. There is no EWI for this but there is a work item to add this corresponding EWI.

#### 2. Create Type creation options are not supported[¶](#create-type-creation-options-are-not-supported "Link to this heading")

Currently, there is no known workaround for any of the creation options, for these reasons they are not taken into account when defining the type.

## Related EWIs[¶](#related-ewis "Link to this heading")

No related EWIs.

## Array Type Definition[¶](#array-type-definition "Link to this heading")

This is a translation reference to convert the Array Variant of the Oracle Create Type Statements (UDT’s) to Snowflake

Danger

SnowConvert AI only recognizes these definitions and for the moment does not support any translation for them. This page is only used as a future reference for translations.

Note

Some parts in the output code are omitted for clarity reasons.

### Description[¶](#description "Link to this heading")

Array Types define an array structure of a previously existing datatype (including other Custom Types).

For the translation of array types, the type definition is replaced by a [Semi-structured Data Type](https://docs.snowflake.com/en/sql-reference/data-types-semistructured.html) and then it is expanded on any usages across the code. This means taking type’s definition and then expanding it on the original code.

```
CREATE TYPE <type name>
AS { VARRAY | [VARYING] ARRAY } ( <size limit> ) OF <data type>
```

Copy

### Sample Source Patterns[¶](#sample-source-patterns "Link to this heading")

#### Inserts for the array usage[¶](#inserts-for-the-array-usage "Link to this heading")

The next data will be inserted inside the table before querying the select. Please note these Inserts currently need to be manually migrated into Snowflake.

##### Oracle[¶](#oracle "Link to this heading")

```
INSERT INTO customer_table_demo(customer_table_id, customer_data) VALUES
(1, phone_list_typ_demo('2000-0000', '4000-0000', '0000-0000'));

INSERT INTO customer_table_demo(customer_table_id, customer_data) VALUES
(1, phone_list_typ_demo('8000-2000', '0000-0000', '5000-0000'));
```

Copy

##### Snowflake[¶](#snowflake "Link to this heading")

```
INSERT INTO customer_table_demo(customer_table_id, customer_data)
SELECT 1, ARRAY_CONSTRUCT('2000-0000', '4000-0000', '0000-0000');

INSERT INTO customer_table_demo(customer_table_id, customer_data)
SELECT 1, ARRAY_CONSTRUCT('8000-2000', '0000-0000', '5000-0000');
```

Copy

#### Array Type usage[¶](#array-type-usage "Link to this heading")

##### Oracle[¶](#id1 "Link to this heading")

```
CREATE TYPE phone_list_typ_demo AS VARRAY(3) OF VARCHAR2(25);
/

CREATE TABLE customer_table_demo (
    customer_table_id INTEGER,
    customer_data phone_list_typ_demo
);
/

SELECT * FROM customer_table_demo;
/
```

Copy

##### Results[¶](#results "Link to this heading")

| CUSTOMER\_TABLE\_ID | CUSTOMER\_DATA |
| --- | --- |
| 1 | [[‘2000-0000’,’4000-0000’,’0000-0000’]] |
| 1 | [[‘8000-2000’,’0000-0000’,’5000-0000’]] |

##### Snowflake[¶](#id2 "Link to this heading")

```
!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'VARYING ARRAY' NODE ***/!!!
CREATE TYPE phone_list_typ_demo AS VARRAY(3) OF VARCHAR2(25);

CREATE OR REPLACE TABLE customer_table_demo (
        customer_table_id INTEGER,
        customer_data VARIANT !!!RESOLVE EWI!!! /*** SSC-EWI-0062 - CUSTOM TYPE 'phone_list_typ_demo' USAGE CHANGED TO VARIANT ***/!!!
    )
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
;

CREATE OR REPLACE VIEW PUBLIC.customer_table_demo_view
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "" }}'
AS
SELECT
        customer_table_id,
        customer_data
FROM
        customer_table_demo;

    SELECT * FROM
        customer_table_demo_view;
```

Copy

##### Results[¶](#id3 "Link to this heading")

| CUSTOMER\_TABLE\_ID | CUSTOMER\_DATA |
| --- | --- |
| 1 | [[‘2000-0000’, ‘4000-0000’, ‘0000-0000’]] |
| 1 | [[‘8000-2000’, ‘0000-0000’, ‘5000-0000’]] |

### Known Issues[¶](#id4 "Link to this heading")

#### 1. Create Type creation options are not supported[¶](#id5 "Link to this heading")

Currently, there is no known workaround for any of the creation options, for these reasons they are not taken into account when defining the type.

##### 2. Migrated code output is not functional[¶](#migrated-code-output-is-not-functional "Link to this heading")

The statements are being changed unnecessarily, which makes them no longer be functional on the output code. This will be addressed when a proper transformation for them is in place.

### Related EWIs[¶](#id6 "Link to this heading")

1. [SSC-EWI-0062](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0062): Custom type usage changed to variant.
2. [SSC-EWI-0073](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0073): Pending Functional Equivalence Review.

## Member Function Definitions[¶](#member-function-definitions "Link to this heading")

This is a translation reference to convert the Member Functions of the Oracle Create Type Statements (UDT’s) to Snowflake

Danger

SnowConvert AI still does not recognize type member functions nor type body definitions. This page is only used as a future reference for translation.

Note

Some parts in the output code are omitted for clarity reasons.

### Description[¶](#id7 "Link to this heading")

Like other Class definitions, Oracle’s TYPE can implement methods to expose behaviors based on its attributes. MEMBER FUCTION will be transformed to Snowflake’s Stored Procedures, to maintain functional equivalence due to limitations.

Since functions are being transformed into procedures, the [transformation reference for PL/SQL](../pl-sql-to-snowflake-scripting/README) also applies here.

### Sample Source Patterns[¶](#id8 "Link to this heading")

#### Inserts for Simple square() member function[¶](#inserts-for-simple-square-member-function "Link to this heading")

The next data will be inserted inside the table before querying the select. Please note these Inserts currently need to be manually migrated into Snowflake.

##### Oracle[¶](#id9 "Link to this heading")

```
INSERT INTO table_member_function_demo(column1) VALUES
(type_member_function_demo(5));
```

Copy

##### Snowflake[¶](#id10 "Link to this heading")

```
INSERT INTO table_member_function_demo (column1)
SELECT OBJECT_CONSTRUCT('a1', 5);
```

Copy

#### Simple square() member function[¶](#simple-square-member-function "Link to this heading")

##### Oracle[¶](#id11 "Link to this heading")

```
-- TYPE DECLARATION
CREATE TYPE type_member_function_demo AS OBJECT (
    a1 NUMBER,
    MEMBER FUNCTION get_square RETURN NUMBER
);
/

-- TYPE BODY DECLARATION
CREATE TYPE BODY type_member_function_demo IS
   MEMBER FUNCTION get_square
   RETURN NUMBER
   IS x NUMBER;
   BEGIN
      SELECT c.column1.a1*c.column1.a1 INTO x
      FROM table_member_function_demo c;
      RETURN (x);
   END;
END;
/

-- TABLE
CREATE TABLE table_member_function_demo (column1 type_member_function_demo);
/

-- QUERYING DATA
SELECT
    t.column1.get_square()
FROM
    table_member_function_demo t;
/
```

Copy

##### Results[¶](#id12 "Link to this heading")

| T.COLUMN1.GET\_SQUARE() |
| --- |
| 25 |

##### Snowflake[¶](#id13 "Link to this heading")

```
-- TYPE DECLARATION
!!!RESOLVE EWI!!! /*** SSC-EWI-0056 - CUSTOM TYPES ARE NOT SUPPORTED IN SNOWFLAKE BUT REFERENCES TO THIS CUSTOM TYPE WERE CHANGED TO VARIANT ***/!!!
CREATE TYPE type_member_function_demo AS OBJECT (
    a1 NUMBER,
    MEMBER FUNCTION get_square RETURN NUMBER
)
;

---- TYPE BODY DECLARATION
--!!!RESOLVE EWI!!! /*** SSC-EWI-OR0007 - CREATE TYPE WITHOUT BODY IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
--CREATE TYPE BODY type_member_function_demo IS
--   MEMBER FUNCTION get_square
--   RETURN NUMBER
--   IS x NUMBER;
--   BEGIN
--      SELECT c.column1.a1*c.column1.a1 INTO x
--      FROM table_member_function_demo c;
--      RETURN (x);
--   END;
--END
   ;

-- TABLE
CREATE OR REPLACE TABLE table_member_function_demo (column1 VARIANT !!!RESOLVE EWI!!! /*** SSC-EWI-0062 - CUSTOM TYPE 'type_member_function_demo' USAGE CHANGED TO VARIANT ***/!!!
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
;

CREATE OR REPLACE VIEW PUBLIC.table_member_function_demo_view
<strong>COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "" }}'
</strong><strong>AS
</strong>SELECT
    column1:a1 :: NUMBER AS a1
FROM
    table_member_function_demo;

-- QUERYING DATA
SELECT
    t.column1.get_square() !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 't.column1.get_square' NODE ***/!!!
FROM
    table_member_function_demo t;
```

Copy

##### Results[¶](#id14 "Link to this heading")

| GET\_SQUARE() |
| --- |
| 25 |

### Known Issues[¶](#id15 "Link to this heading")

No Known issues.

### Related EWIs[¶](#id16 "Link to this heading")

1. [SSC-EWI-0056](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0056): Create Type Not Supported.
2. [SSC-EWI-0062](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0062): Custom type usage changed to variant.
3. [SSC-EWI-0073](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0073): Pending Functional Equivalence Review.
4. [SSC-EWI-OR0007](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI.html#ssc-ewi-or0007): Create Type Not Supported in Snowflake

## Nested Table Type Definition[¶](#nested-table-type-definition "Link to this heading")

This is a translation reference to convert the Nested Table Variant of the Oracle Create Type Statements (UDT’s) to Snowflake

Danger

SnowConvert AI only recognizes these definitions, does not support any translation and there is no known workaround for them.

### Description[¶](#id17 "Link to this heading")

Nested Table Types define an embedded table structure of a previously existing datatype (including other Custom Types). They can be used as a more powerful version of the [Array Type](#array-type-definition).

Unlike any of the other types, there is still no known workaround or any possible translation for them.

```
CREATE TYPE <type name> AS TABLE OF <data type>
```

Copy

### Sample Source Patterns[¶](#id18 "Link to this heading")

#### Nested Table Type usage[¶](#nested-table-type-usage "Link to this heading")

##### Oracle[¶](#id19 "Link to this heading")

```
CREATE TYPE textdoc_typ AS OBJECT (
    document_typ VARCHAR2(32),
    formatted_doc BLOB
);
/

CREATE TYPE textdoc_tab AS TABLE OF textdoc_typ;
/
```

Copy

##### Snowflake[¶](#id20 "Link to this heading")

```
!!!RESOLVE EWI!!! /*** SSC-EWI-0056 - CUSTOM TYPES ARE NOT SUPPORTED IN SNOWFLAKE BUT REFERENCES TO THIS CUSTOM TYPE WERE CHANGED TO VARIANT ***/!!!
CREATE TYPE textdoc_typ AS OBJECT (
    document_typ VARCHAR2(32),
    formatted_doc BLOB
)
;

!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'NESTED TABLE' NODE ***/!!!

CREATE TYPE textdoc_tab AS TABLE OF textdoc_typ;
```

Copy

### Known Issues[¶](#id21 "Link to this heading")

#### 1. Create Type creation options are not supported[¶](#id22 "Link to this heading")

Currently, there is no known workaround for any of the creation options; for these reasons, they are not taken into account when defining the type.

### Related EWIs[¶](#id23 "Link to this heading")

1. [SSC-EWI-0073](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0073): Pending Functional Equivalence Review
2. [SSC-EWI-0056](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0056): Create Type Not Supported.

## Object Type Definition[¶](#object-type-definition "Link to this heading")

This is a translation reference to convert the Object Variant of the Oracle Create Type Statements (UDT’s) to Snowflake

Note

SnowConvert AI supports a translation for Object Type Definitions itself. However, their usages are still a work in progress.

Note

Some parts in the output code are omitted for clarity reasons.

### Description[¶](#id24 "Link to this heading")

Object Types define a structure of data similar to a record, with the added advantages of the member function definitions. Meaning that their data may be used along some behavior within the type.

For the translation of object types, the type definition is replaced by a [Semi-structured Data Type](https://docs.snowflake.com/en/sql-reference/data-types-semistructured.html) and then it is expanded on any usages across the code. For tables this means replacing the column for a Variant, adding a View so that selects (and also Views) to the original table can still function.

```
CREATE TYPE <type name> AS OBJECT
( [{<type column definition> | type method definition } , ...]);
```

Copy

### Sample Source Patterns[¶](#id25 "Link to this heading")

#### Inserts for Simple Type usage[¶](#inserts-for-simple-type-usage "Link to this heading")

The next data will be inserted inside the table before querying the select. Please note these Inserts currently need to be manually migrated into Snowflake.

##### Oracle[¶](#id26 "Link to this heading")

```
INSERT INTO customer_table_demo(customer_table_id, customer_data)
VALUES ( 1, customer_typ_demo(1, 'First Name 1', 'Last Name 1'));

INSERT INTO customer_table_demo(customer_table_id, customer_data)
VALUES ( 2, customer_typ_demo(2, 'First Name 2', 'Last Name 2'));
```

Copy

##### Snowflake[¶](#id27 "Link to this heading")

```
INSERT INTO customer_table_demo(customer_table_id, customer_data)
VALUES ( 1, customer_typ_demo(1, 'First Name 1', 'Last Name 1') !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'customer_typ_demo' NODE ***/!!!);

INSERT INTO customer_table_demo(customer_table_id, customer_data)
VALUES ( 2, customer_typ_demo(2, 'First Name 2', 'Last Name 2') !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'customer_typ_demo' NODE ***/!!!);
```

Copy

#### Simple Type usage[¶](#simple-type-usage "Link to this heading")

##### Oracle[¶](#id28 "Link to this heading")

```
CREATE TYPE customer_typ_demo AS OBJECT (
    customer_id INTEGER,
    cust_first_name VARCHAR2(20),
    cust_last_name VARCHAR2(20)
);

CREATE TABLE customer_table_demo (
    customer_table_id INTEGER,
    customer_data customer_typ_demo
);

SELECT * FROM customer_table_demo;
```

Copy

##### Results[¶](#id29 "Link to this heading")

| CUSTOMER\_TABLE\_ID | CUSTOMER\_DATA |
| --- | --- |
| 1 | [1, First Name 1, Last Name 1] |
| 2 | [2, First Name 2, Last Name 2] |

##### Snowflake[¶](#id30 "Link to this heading")

```
!!!RESOLVE EWI!!! /*** SSC-EWI-0056 - CUSTOM TYPES ARE NOT SUPPORTED IN SNOWFLAKE BUT REFERENCES TO THIS CUSTOM TYPE WERE CHANGED TO VARIANT ***/!!!
CREATE TYPE customer_typ_demo AS OBJECT (
    customer_id INTEGER,
    cust_first_name VARCHAR2(20),
    cust_last_name VARCHAR2(20)
)
;

CREATE OR REPLACE TABLE customer_table_demo (
        customer_table_id INTEGER,
        customer_data VARIANT !!!RESOLVE EWI!!! /*** SSC-EWI-0062 - CUSTOM TYPE 'customer_typ_demo' USAGE CHANGED TO VARIANT ***/!!!
    )
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}}'
;

CREATE OR REPLACE VIEW PUBLIC.customer_table_demo_view
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "" }}'
AS
SELECT
        customer_table_id,
        customer_data:customer_id :: INTEGER AS customer_id,
        customer_data:cust_first_name :: VARCHAR AS cust_first_name,
        customer_data:cust_last_name :: VARCHAR AS cust_last_name
FROM
        customer_table_demo;

    SELECT * FROM
        customer_table_demo_view;
```

Copy

##### Results[¶](#id31 "Link to this heading")

| CUSTOMER\_TABLE\_ID | CUST\_ID | CUST\_FIRST\_NAME | CUST\_LAST\_NAME |
| --- | --- | --- | --- |
| 1 | 1 | First Name 1 | Last Name 1 |
| 2 | 2 | First Name 2 | Last Name 2 |

#### Inserts for Nested Type Usage[¶](#inserts-for-nested-type-usage "Link to this heading")

These statements need to be placed between the table creation and the select statement to test the output.

##### Oracle[¶](#id32 "Link to this heading")

```
INSERT INTO customer_table_demo(customer_id, customer_data) values
(1, customer_typ_demo('Customer 1', email_typ_demo('email@domain.com')));

INSERT INTO customer_table_demo(customer_id, customer_data) values
(2, customer_typ_demo('Customer 2', email_typ_demo('email2@domain.com')));
```

Copy

##### Snowflake[¶](#id33 "Link to this heading")

```
INSERT INTO customer_table_demo(customer_id, customer_data) values
(1, customer_typ_demo('Customer 1', email_typ_demo('email@domain.com') !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'email_typ_demo' NODE ***/!!!) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'customer_typ_demo' NODE ***/!!!);

INSERT INTO customer_table_demo(customer_id, customer_data) values
(2, customer_typ_demo('Customer 2', email_typ_demo('email2@domain.com') !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'email_typ_demo' NODE ***/!!!) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'customer_typ_demo' NODE ***/!!!);
```

Copy

#### Nested Type Usage[¶](#nested-type-usage "Link to this heading")

##### Oracle[¶](#id34 "Link to this heading")

```
CREATE TYPE email_typ_demo AS OBJECT (email VARCHAR2(20));

CREATE TYPE customer_typ_demo AS OBJECT (
    cust_name VARCHAR2(20),
    cust_email email_typ_demo
);

CREATE TABLE customer_table_demo (
    customer_id INTEGER,
    customer_data customer_typ_demo
);

SELECT * FROM customer_table_demo;
```

Copy

##### Results[¶](#id35 "Link to this heading")

| CUSTOMER\_ID | CUSTOMER\_DATA |
| --- | --- |
| 1 | [Customer 1, [email@domain.com]] |
| 2 | [Customer 2, [email2@domain.com]] |

##### Snowflake[¶](#id36 "Link to this heading")

```
!!!RESOLVE EWI!!! /*** SSC-EWI-0056 - CUSTOM TYPES ARE NOT SUPPORTED IN SNOWFLAKE BUT REFERENCES TO THIS CUSTOM TYPE WERE CHANGED TO VARIANT ***/!!!
CREATE TYPE email_typ_demo AS OBJECT (email VARCHAR2(20))
;

!!!RESOLVE EWI!!! /*** SSC-EWI-0056 - CUSTOM TYPES ARE NOT SUPPORTED IN SNOWFLAKE BUT REFERENCES TO THIS CUSTOM TYPE WERE CHANGED TO VARIANT ***/!!!

CREATE TYPE customer_typ_demo AS OBJECT (
    cust_name VARCHAR2(20),
    cust_email email_typ_demo
)
;

CREATE OR REPLACE TABLE customer_table_demo (
    customer_id INTEGER,
    customer_data VARIANT !!!RESOLVE EWI!!! /*** SSC-EWI-0062 - CUSTOM TYPE 'customer_typ_demo' USAGE CHANGED TO VARIANT ***/!!!
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}}'
;

CREATE OR REPLACE VIEW PUBLIC.customer_table_demo_view
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "" }}'
AS
SELECT
    customer_id,
    customer_data:cust_name :: VARCHAR AS cust_name,
    customer_data:cust_email:email :: VARCHAR AS email
FROM
    customer_table_demo;

SELECT * FROM
    customer_table_demo_view;
```

Copy

##### Results[¶](#id37 "Link to this heading")

| CUSTOMER\_ID | CUST\_NAME | CUST\_EMAIL |
| --- | --- | --- |
| 1 | Customer 1 | email@domain.com |
| 2 | Customer 2 | email2@domain.com |

### Known Issues[¶](#id38 "Link to this heading")

#### 1. Migrated code output is not the same[¶](#migrated-code-output-is-not-the-same "Link to this heading")

The view statement is being changed unnecessarily, which makes the table no longer have the same behavior in the output code. There is a work item to fix this issue.

##### 2. DML for User-defined Types is not being transformed[¶](#dml-for-user-defined-types-is-not-being-transformed "Link to this heading")

DML that interacts with elements that have User-defined types within them (like a table) are not being transformed. There is a work item to implement this in the future.

##### 3. Create Type creation options are not supported[¶](#id39 "Link to this heading")

Currently, there is no known workaround for any of the creation options, for these reasons they are not taken into account when defining the type.

### Related EWIs[¶](#id40 "Link to this heading")

1. [SSC-EWI-0056](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0056): Create Type Not Supported.
2. [SSC-EWI-0062](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0062): Custom type usage changed to variant.
3. [SSC-EWI-0073](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0073): Pending Functional Equivalence Review.

## Subtype Definition[¶](#subtype-definition "Link to this heading")

This is a translation reference to convert the Subtype Variant of the Oracle Create Type Statements (UDT’s) to Snowflake

Danger

Since there are no known workarounds, SnowConvert AI only recognizes these definitions and does not support any translation for them.

### Description[¶](#id41 "Link to this heading")

Subtypes define a structure of data similar to a record, with the added advantages of the member function definitions. Meaning that their data may be used along some behavior within the type. Unlike Object Types, Subtypes are built as an extension to another existing type.

Regarding subtype definitions, there is still no translation, but there might be a way to reimplement them using [Object Type Definitions](#object-type-definition) and then using their respective translation.

```
CREATE TYPE <type name> UNDER <super type name>
( [{<type column definition> | type method definition } , ...]);
```

Copy

### Sample Source Patterns[¶](#id42 "Link to this heading")

#### Subtypes under an Object Type[¶](#subtypes-under-an-object-type "Link to this heading")

##### Oracle[¶](#id43 "Link to this heading")

```
CREATE TYPE person_t AS OBJECT (name VARCHAR2(100), ssn INTEGER) 
   NOT FINAL;
/

CREATE TYPE employee_t UNDER person_t 
   (department_id INTEGER, salary INTEGER) 
   NOT FINAL;
/

CREATE TYPE part_time_emp_t UNDER employee_t (num_hrs INTEGER);
/
```

Copy

##### Snowflake[¶](#id44 "Link to this heading")

```
!!!RESOLVE EWI!!! /*** SSC-EWI-0056 - CUSTOM TYPES ARE NOT SUPPORTED IN SNOWFLAKE BUT REFERENCES TO THIS CUSTOM TYPE WERE CHANGED TO VARIANT ***/!!!
CREATE TYPE person_t AS OBJECT (name VARCHAR2(100), ssn INTEGER)
   NOT FINAL;

--!!!RESOLVE EWI!!! /*** SSC-EWI-OR0007 - CREATE TYPE SUBTYPE IS NOT SUPPORTED IN SNOWFLAKE ***/!!!

--CREATE TYPE employee_t UNDER person_t
--   (department_id INTEGER, salary INTEGER)
--   NOT FINAL
            ;

--!!!RESOLVE EWI!!! /*** SSC-EWI-OR0007 - CREATE TYPE SUBTYPE IS NOT SUPPORTED IN SNOWFLAKE ***/!!!

--CREATE TYPE part_time_emp_t UNDER employee_t (num_hrs INTEGER)
                                                              ;
```

Copy

### Known Issues[¶](#id45 "Link to this heading")

#### 1. Create Type creation options are not supported[¶](#id46 "Link to this heading")

Currently, there is no known workaround for any of the creation options, for these reasons they are not taken into account when defining the type.

### Related EWIs[¶](#id47 "Link to this heading")

1. [SSC-EWI-0056](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0056): Create Type Not Supported.
2. [SSC-EWI-OR0007](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI.html#ssc-ewi-or0007): Create Type Not Supported in Snowflake.

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

1. [General Description](#general-description)
2. [Limitations](#limitations)
3. [Proposed workarounds](#proposed-workarounds)
4. [Current SnowConvert AI Support](#current-snowconvert-ai-support)
5. [Known Issues](#known-issues)
6. [Related EWIs](#related-ewis)
7. [Array Type Definition](#array-type-definition)
8. [Member Function Definitions](#member-function-definitions)
9. [Nested Table Type Definition](#nested-table-type-definition)
10. [Object Type Definition](#object-type-definition)
11. [Subtype Definition](#subtype-definition)