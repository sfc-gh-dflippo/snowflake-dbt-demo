---
auto_generated: true
description: Retrieves information from the database. (Sybase SQL Language Reference)
last_scraped: '2026-01-14T16:53:57.733983+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/sybase/sybase-select-statement
title: SnowConvert AI - Sybase IQ - SELECT | Snowflake Documentation
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)Translation References[Sybase IQ](README.md)StatementsSELECT

# SnowConvert AI - Sybase IQ - SELECT[¶](#snowconvert-ai-sybase-iq-select "Link to this heading")

## Description[¶](#description "Link to this heading")

> Retrieves information from the database. ([Sybase SQL Language Reference](https://help.sap.com/docs/SAP_IQ/a899599784f21015a466ed42e24d07f9/a624e72e84f210159276a39335acd358.html?version=16.0.11&amp;locale=en-US))

Warning

This syntax is partially supported in Snowflake.

## Grammar Syntax[¶](#grammar-syntax "Link to this heading")

```
 SELECT 
[ ALL | DISTINCT ] 
[ row-limitation-option1 ] 
   	select-list
   … 	[ INTO { host-variable-list | variable-list | table-name } ]
   … 	[ INTO LOCAL TEMPORARY TABLE { table-name } ]
   … 	[ FROM table-list ]
   … 	[ WHERE search-condition ]
   … 	[ GROUP BY [ expression [, ...]
         | ROLLUP ( expression [, ...] )
         | CUBE ( expression [, ...] ) ] ] 
   … 	[ HAVING search-condition ]
   … 	[ ORDER BY { expression | integer } [ ASC | DESC ] [, ...] ]
   | 	[ FOR JSON json-mode ] 
   … [ row-limitation-option ]

select-list:
   { column-name
   | expression [ [ AS ] alias-name ]
   | * 
   }

row-limitation-option1:
   FIRST 
   | TOP {ALL | limit-expression} [START AT startat-expression ]
  
limit-expression:
    simple-expression
  
startat-expression:
    simple-expression

row-limitation-option2:
   LIMIT { [ offset-expression, ] limit-expression 
   | limit-expression OFFSET offset-expression }

offset-expression:
   simple-expression

simple-expression:
   integer
   | variable
   | ( simple-expression )
   | ( simple-expression { + | - | * } simple-expression )


..FROM <table-expression> [,...]

<table-expression> ::=
   <table-name>
   | <view-name>
   | <procedure-name>
   | <common-table-expression>
   | ( <subquery> ) [ [ AS ] <derived-table-name> ( <column_name, ...>) ] ]
   | <derived-table>
   | <join-expression> 
   | ( <table-expression> , ... )
   | <openstring-expression>
   | <apply-expression>
   | <contains-expression>
   | <dml-derived-table>

<table-name> ::=
   [ <userid>.] <table-name> ]
   [ [ AS ] <correlation-name> ]
   [ FORCE INDEX ( <index-name> ) ]

<view-name> ::=
   [ <userid>.]<view-name> [ [ AS ] <correlation-name> ]

<procedure-name> ::=
   [  <owner>, ] <procedure-name> ([ <parameter>, ...])
   [  WITH(<column-name datatype>, )]
   [ [ AS ] <correlation-name> ]

<parameter> ::=
   <scalar-expression> | <table-parameter>

<table-parameter> ::= 
   TABLE (<select-statement)> [ OVER ( <table-parameter-over> )]

<table-parameter-over> ::=
   [ PARTITION BY {ANY
   | NONE|< table-expression> } ] 
   [ ORDER BY { <expression> | <integer> } 
   [ ASC | DESC ] [, ...] ]

<derived-table> ::=
   ( <select-statement> ) 
   	[ AS ] <correlation-name> [ ( <column-name>, ... ) ]

<join-expression> ::=
   <table-expression> <join-operator> <table-expression>
   	[ ON <join-condition> ]

<join-operator> ::=
   [ KEY | NATURAL ] [ <join-type> ] JOIN | CROSS JOIN

<join-type> ::=
   INNER
     | LEFT [ OUTER ]
     | RIGHT [ OUTER ]
     | FULL [ OUTER ]

<openstring-expression> ::=
   OPENSTRING ( { FILE | VALUE } <string-expression> )
     WITH ( <rowset-schema> ) 
   	[ OPTION ( <scan-option> ...  ) ]
   	[ AS ] <correlation-name>

<apply-expression> ::=
   <table-expression> { CROSS | OUTER } APPLY <table-expression>

<contains-expression> ::=
   { <table-name>  | <view-name> } CONTAINS 
   ( <column-name> [,...], <contains-query> ) 
   [ [ AS ] <score-correlation-name> ]

<rowset-schema> ::=
   <column-schema-list>
	   | TABLE [<owner>.]<table-name> [ ( <column-list> ) ]

<column-schema-list> ::=
   { <column-name user-or-base-type> |  filler( ) } [ , ... ]

<column-list> ::=
   { <column-name> | filler( ) } [ , ... ]

<scan-option> ::=
   BYTE ORDER MARK { ON | OFF }
   | COMMENTS INTRODUCED BY <comment-prefix>
   | DELIMITED BY <string>
   | ENCODING <encoding>
   | ESCAPE CHARACTER <character>
   | ESCAPES { ON | OFF }
   | FORMAT { TEXT  | BCP  }
   | HEXADECIMAL { ON | OFF }
   | QUOTE <string>
   | QUOTES { ON | OFF }
   | ROW DELIMITED BY string
   | SKIP <integer>
   | STRIP { ON | OFF | LTRIM | RTRIM | BOTH }

<contains-query> ::= <string>

<dml-derived-table> ::=
   ( <dml-statement>  ) REFERENCING ( [ <table-version-names>  | NONE ] )

<dml-statement> ::=
   <insert-statement> 
   <update-statement>
   <delete-statement>

<table-version-names> ::=
   OLD [ AS ] <correlation-name> [ FINAL [ AS ] <correlation-name> ]
     | FINAL [ AS ] <correlation-name>
```

Copy

## Sample Source Patterns[¶](#sample-source-patterns "Link to this heading")

### Row Limitation[¶](#row-limitation "Link to this heading")

Sybase allow row limitation in a query by using TOP clause with an optional START AT that Snowflake not supports but can transformed as down below to achieve the same functionality.

#### Input Code:[¶](#input-code "Link to this heading")

##### Sybase[¶](#sybase "Link to this heading")

```
 SELECT
TOP 10 START AT 2
COL1 
FROM TABLE1;

SELECT
FIRST
COL1 
FROM TABLE1;

SELECT
COL1 
FROM TABLE1
LIMIT 2, 1;

SELECT
COL1 
FROM TABLE1
LIMIT 1 OFFSET 2;
```

Copy

#### Output Code:[¶](#output-code "Link to this heading")

##### Snowflake[¶](#snowflake "Link to this heading")

```
 SELECT
COL1
FROM
TABLE1
LIMIT 10 OFFSET 2;

SELECT
TOP 1
COL1
FROM
TABLE1;

SELECT
COL1
FROM
TABLE1
LIMIT 1 OFFSET 2;

SELECT
COL1
FROM
TABLE1
LIMIT 1 OFFSET 2;
```

Copy

### Into Clause[¶](#into-clause "Link to this heading")

In Sybase a Table can be defined by selecting multiple rows and defining a name to stored the date retrieved. Snowflake does not support this behavior but can emulated by doing a CREATE TABLE AS.

#### Input Code:[¶](#id1 "Link to this heading")

##### Sybase[¶](#id2 "Link to this heading")

```
 SELECT
* INTO mynewtable
FROM TABLE1;

SELECT
* INTO LOCAL TEMPORARY TABLE mynewtable
FROM TABLE1;

SELECT
* INTO #mynewtable
FROM TABLE1;
```

Copy

#### Output Code:[¶](#id3 "Link to this heading")

##### Snowflake[¶](#id4 "Link to this heading")

```
 CREATE OR REPLACE TABLE mynewtable AS
SELECT
*
FROM
TABLE1;

CREATE OR REPLACE TEMPORARY TABLE mynewtable AS
SELECT
*
FROM
TABLE1;

CREATE OR REPLACE TEMPORARY TABLE T_mynewtable AS
SELECT
*
FROM
TABLE1;
```

Copy

### Force Index[¶](#force-index "Link to this heading")

Snowflake does not contain indexes for query optimization.

#### Input Code:[¶](#id5 "Link to this heading")

##### Sybase[¶](#id6 "Link to this heading")

```
 SELECT * FROM MyTable FORCE INDEX (MyIndex);
```

Copy

#### Output Code:[¶](#id7 "Link to this heading")

##### Snowflake[¶](#id8 "Link to this heading")

```
 SELECT
*
FROM
MyTable
--        --** SSC-FDM-SY0002 - FORCE INDEX IS NOT SUPPORTED IN SNOWFLAKE **
--        FORCE INDEX (MyIndex)
                             ;
```

Copy

### TABLE FUNCTIONS[¶](#table-functions "Link to this heading")

Snowflake allows calling a stored procedure(when the procedure meets certain [limitations](https://docs.snowflake.com/en/developer-guide/stored-procedure/stored-procedures-selecting-from#limitations-for-selecting-from-a-stored-procedure)) or a table value function in a FROM clause, but RESULTSETS and windowing cannot be used as parameters.

#### Input Code:[¶](#id9 "Link to this heading")

##### Sybase[¶](#id10 "Link to this heading")

```
 SELECT * FROM 
MyProcedure(TABLE (SELECT * FROM TABLE1));

SELECT * FROM MyProcedure(1, 'test');

SELECT * FROM 
MyProcedure(
TABLE (SELECT * FROM TABLE1) 
OVER (PARTITION BY Col1 ORDER BY Col2 DESC));

SELECT * FROM 
MyProcedure(
TABLE (SELECT * FROM AnotherTable) );
```

Copy

#### Output Code:[¶](#id11 "Link to this heading")

##### Snowflake[¶](#id12 "Link to this heading")

```
 SELECT
*
FROM
TABLE(MyProcedure(
                  !!!RESOLVE EWI!!! /*** SSC-EWI-SY0004 - UNSUPPORTED SYNTAX TABLE FUNCTION CAN'T RECEIVE A QUERY AS PARAMETER ***/!!!TABLE (SELECT * FROM TABLE1)));

SELECT
*
FROM
TABLE(MyProcedure(1, 'test'));


SELECT
*
FROM
TABLE(MyProcedure(
!!!RESOLVE EWI!!! /*** SSC-EWI-SY0004 - UNSUPPORTED SYNTAX TABLE FUNCTION CAN'T RECEIVE A QUERY AS PARAMETER ***/!!!
TABLE (SELECT * FROM TABLE1)
!!!RESOLVE EWI!!! /*** SSC-EWI-SY0005 - UNSUPPORTED SYNTAX TABLE FUNCTION CAN'T BE USED WITH OVER EXPRESSION ***/!!!
OVER (PARTITION BY Col1 ORDER BY Col2 DESC)));


SELECT
*
FROM
TABLE(MyProcedure(
!!!RESOLVE EWI!!! /*** SSC-EWI-SY0004 - UNSUPPORTED SYNTAX TABLE FUNCTION CAN'T RECEIVE A QUERY AS PARAMETER ***/!!!
TABLE (SELECT * FROM AnotherTable) ));
```

Copy

### OPEN STRING[¶](#open-string "Link to this heading")

Snowflake does not support [OPENSTRING](https://help.sap.com/docs/SAP_IQ/a898e08b84f21015969fa437e89860c8/a7749cf084f21015b73b899c1520fb06.html#parameters) functionality.

#### Input Code:[¶](#id13 "Link to this heading")

##### Sybase[¶](#id14 "Link to this heading")

```
 -- Openstring from file
SELECT * FROM 
OPENSTRING (FILE '/path/to/file.txt') 
WITH (Col1 INT, Col2 VARCHAR(20)) AS OS;

-- Openstring from value
SELECT * FROM 
OPENSTRING (VALUE '1,test') 
WITH (Col1 INT, Col2 VARCHAR(20)) AS OS;

-- Openstring with options
SELECT * FROM 
OPENSTRING (FILE '/path/to/file.csv') 
WITH (Col1 INT, Col2 VARCHAR(20)) 
OPTION (DELIMITED BY ',' QUOTE '"') AS OS;
```

Copy

#### Output Code:[¶](#id15 "Link to this heading")

##### Snowflake[¶](#id16 "Link to this heading")

```
 -- Openstring from file
SELECT
*
FROM
!!!RESOLVE EWI!!! /*** SSC-EWI-SY0006 - OPEN STRING IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
OPENSTRING (FILE '/path/to/file.txt')
WITH (Col1 INT, Col2 VARCHAR(20)) AS OS;

-- Openstring from value
SELECT
*
FROM
!!!RESOLVE EWI!!! /*** SSC-EWI-SY0006 - OPEN STRING IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
OPENSTRING (VALUE '1,test')
WITH (Col1 INT, Col2 VARCHAR(20)) AS OS;

-- Openstring with options
SELECT
*
FROM
!!!RESOLVE EWI!!! /*** SSC-EWI-SY0006 - OPEN STRING IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
OPENSTRING (FILE '/path/to/file.csv')
WITH (Col1 INT, Col2 VARCHAR(20))
OPTION (DELIMITED BY ',' QUOTE '"') AS OS;
```

Copy

### DML Derived Table[¶](#dml-derived-table "Link to this heading")

In Sybase, during execution, the DML statement specified in the dml-derived table is executed first, and the rows affected by that DML materialize into a temporary table whose columns are described by the REFERENCING clause. The temporary table represents the result set of dml-derived-table. Snowflake does not support this behavior.

#### Input Code:[¶](#id17 "Link to this heading")

##### Sybase[¶](#id18 "Link to this heading")

```
 -- DML derived table with insert
SELECT * FROM (INSERT INTO TargetTable (Col1, Col2) VALUES (1, 'test')) REFERENCING (FINAL AS F);

-- DML derived table with update
SELECT * FROM (UPDATE TargetTable SET Col2 = 'updated' WHERE Col1 = 1) REFERENCING (OLD AS O FINAL AS F);

-- DML derived table with delete
SELECT * FROM (DELETE FROM TargetTable WHERE Col1 = 1) REFERENCING (OLD AS O);
```

Copy

#### Output Code:[¶](#id19 "Link to this heading")

##### Snowflake[¶](#id20 "Link to this heading")

```
 -- DML derived table with insert
SELECT
*
FROM
!!!RESOLVE EWI!!! /*** SSC-EWI-SY0007 - DML DERIVED TABLE NOT SUPPORTED IN SNOWFLAKE ***/!!! (INSERT INTO TargetTable (Col1, Col2) VALUES (1, 'test')) REFERENCING (FINAL AS F);

-- DML derived table with update
SELECT
*
FROM
!!!RESOLVE EWI!!! /*** SSC-EWI-SY0007 - DML DERIVED TABLE NOT SUPPORTED IN SNOWFLAKE ***/!!! (UPDATE TargetTable SET Col2 = 'updated' WHERE Col1 = 1) REFERENCING (OLD AS O FINAL AS F);

-- DML derived table with delete
SELECT
*
FROM
!!!RESOLVE EWI!!! /*** SSC-EWI-SY0007 - DML DERIVED TABLE NOT SUPPORTED IN SNOWFLAKE ***/!!! (DELETE FROM TargetTable WHERE Col1 = 1) REFERENCING (OLD AS O);
```

Copy

### KEY JOIN[¶](#key-join "Link to this heading")

Snowflake does not support KEY join but when the ON CLAUSE is defined in the query the KEY keyword and removed otherwise an EWI is inserted.

#### Input Code:[¶](#id21 "Link to this heading")

##### Sybase[¶](#id22 "Link to this heading")

```
 SELECT * FROM Table1 KEY JOIN Table2;
SELECT * FROM Table1 KEY JOIN Table2 ON Table1.ID = Table2.ID;
```

Copy

#### Output Code:[¶](#id23 "Link to this heading")

##### Snowflake[¶](#id24 "Link to this heading")

```
 SELECT
*
FROM
Table1
!!!RESOLVE EWI!!! /*** SSC-EWI-SY0009 - KEY JOIN NOT SUPPORTED IN SNOWFLAKE ***/!!!
KEY JOIN
Table2;

SELECT
*
FROM
Table1
JOIN
Table2
ON Table1.ID = Table2.ID;
```

Copy

### OUTER-CROSS APPLY[¶](#outer-cross-apply "Link to this heading")

Snowflake transforms the clause the CROSS APPLY into LEFT OUTER JOIN and OUTER APPLY to INNER JOIN.

#### Input Code:[¶](#id25 "Link to this heading")

##### Sybase[¶](#id26 "Link to this heading")

```
 -- Apply cross apply
SELECT * FROM Table1 CROSS APPLY (SELECT Col2 FROM Table2 WHERE Table1.ID = Table2.ID) AS AP;

-- Apply outer apply
SELECT * FROM Table1 OUTER APPLY (SELECT Col2 FROM Table2 WHERE Table1.ID = Table2.ID) AS AP;
```

Copy

#### Output Code:[¶](#id27 "Link to this heading")

##### Snowflake[¶](#id28 "Link to this heading")

```
 -- Apply cross apply
SELECT
    *
FROM
    Table1
    LEFT OUTER JOIN (
        SELECT
            Col2
        FROM
            Table2
        WHERE
            Table1.ID = Table2.ID
    ) AS AP;

-- Apply outer apply
SELECT
    *
FROM
    Table1
    INNER JOIN LATERAL (
        SELECT
            Col2
        FROM
            Table2
        WHERE
            Table1.ID = Table2.ID
    ) AS AP;
```

Copy

### CONTAINS Clause[¶](#contains-clause "Link to this heading")

In Sybase the [CONTAINS](https://help.sap.com/docs/SAP_IQ/a898e08b84f21015969fa437e89860c8/a7749cf084f21015b73b899c1520fb06.html) clause following a table name to filter the table and return only those rows matching the full text query specified with contains-query. Every matching row of the table is returned together with a score column that can be referred to using score-correlation-name. Snowflake does not support this behavior.

#### Input Code:[¶](#id29 "Link to this heading")

##### Sybase[¶](#id30 "Link to this heading")

```
 -- Contains clause
SELECT * FROM MyTable CONTAINS (TextColumn, 'search term') AS Score;

-- Contains clause with multiple columns.
SELECT * FROM MyTable CONTAINS (TextColumn,TextColumn2, 'search term') AS Score;
```

Copy

#### Output Code:[¶](#id31 "Link to this heading")

##### Snowflake[¶](#id32 "Link to this heading")

```
 -- Contains clause
SELECT
*
FROM
MyTable
        !!!RESOLVE EWI!!! /*** SSC-EWI-SY0008 - CONTAINS CLAUSE NOT SUPPORTED IN SNOWFLAKE ***/!!!
        CONTAINS (TextColumn, 'search term') AS Score;

-- Contains clause with multiple columns.
SELECT
*
FROM
MyTable
        !!!RESOLVE EWI!!! /*** SSC-EWI-SY0008 - CONTAINS CLAUSE NOT SUPPORTED IN SNOWFLAKE ***/!!!
        CONTAINS (TextColumn,TextColumn2, 'search term') AS Score;
```

Copy

## Related EWIs[¶](#related-ewis "Link to this heading")

[SSC-FDM-0009](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0009): GLOBAL TEMPORARY TABLE FUNCTIONALITY NOT SUPPORTED.

[SSC-FDM-SY0001](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/sybaseFDM.html#ssc-fdm-sy0001): CALLING STORED PROCEDURE IN FROM CLAUSE MIGHT HAVE COMPILATION ERRORS

[SSC-FDM-SY0002](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/sybaseFDM.html#ssc-fdm-sy0002): FORCE INDEX IS NOT SUPPORTED IN SNOWFLAKE

[SSC-EWI-SY0004](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/sybaseEWI.html#ssc-ewi-sy0004) - UNSUPPORTED SYNTAX TABLE FUNCTION CAN’T RECEIVE A QUERY AS PARAMETER

[SSC-EWI-SY0005](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/sybaseEWI.html#ssc-ewi-sy0005) - UNSUPPORTED SYNTAX TABLE FUNCTION CAN’T BE USED WITH OVER EXPRESSION

[SSC-EWI-SY0006](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/sybaseEWI.html#ssc-ewi-sy0006) - OPEN STRING IS NOT SUPPORTED IN SNOWFLAKE

[SSC-EWI-SY0007](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/sybaseEWI.html#ssc-ewi-sy0007) - DML DERIVED TABLE NOT SUPPORTED IN SNOWFLAKE

[SSC-EWI-SY0008](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/sybaseEWI.html#ssc-ewi-sy0008) - CONTAINS CLAUSE NOT SUPPORTED IN SNOWFLAKE

[SSC-EWI-SY0009](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/sybaseEWI.html#ssc-ewi-sy0003) - KEY JOIN NOT SUPPORTED IN SNOWFLAKE

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
3. [Sample Source Patterns](#sample-source-patterns)
4. [Related EWIs](#related-ewis)