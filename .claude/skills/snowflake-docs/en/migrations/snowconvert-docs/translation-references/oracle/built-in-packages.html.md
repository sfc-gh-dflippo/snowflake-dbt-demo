---
auto_generated: true
description: Translation reference for Built-in packages.
last_scraped: '2026-01-14T16:55:33.511643+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/oracle/built-in-packages.html
title: SnowConvert AI - Oracle - Built-In packages | Snowflake Documentation
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
          + [Oracle](README.md)

            - [Sample Data](sample-data.md)
            - Basic Elements of Oracle SQL

              - [Literals](basic-elements-of-oracle-sql/literals.md)
              - [Data Types](basic-elements-of-oracle-sql/data-types/README.md)
            - [Pseudocolumns](pseudocolumns.md)
            - [Built-in Functions](functions/README.md)
            - [Built-in Packages](built-in-packages.md)
            - [SQL Queries and Subqueries](sql-queries-and-subqueries/selects.md)
            - [SQL Statements](sql-translation-reference/README.md)
            - [PL/SQL to Snowflake Scripting](pl-sql-to-snowflake-scripting/README.md)
            - [PL/SQL to Javascript](pl-sql-to-javascript/README.md)
            - [SQL Plus](sql-plus.md)
            - [Wrapped Objects](wrapped-objects.md)
            - ETL And BI Repointing

              - [Power BI Oracle Repointing](etl-bi-repointing/power-bi-oracle-repointing.md)
          + [SQL Server-Azure Synapse](../transact/README.md)
          + [Sybase IQ](../sybase/README.md)
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)Translation References[Oracle](README.md)Built-in Packages

# SnowConvert AI - Oracle - Built-In packages[¶](#snowconvert-ai-oracle-built-in-packages "Link to this heading")

Translation reference for Built-in packages.

## Description[¶](#description "Link to this heading")

> Oracle supplies many PL/SQL packages with the Oracle server to extend database functionality and provide PL/SQL access to SQL features. ([Oracle PL/SQL Built-in Packages](https://docs.oracle.com/en/database/oracle/oracle-database/21/arpls/introduction-to-oracle-supplied-plsql-packages-and-types.html#GUID-4AA6AA30-CAEE-4DCD-B214-9AD51D0229B4))

## DBMS\_OUTPUT[¶](#dbms-output "Link to this heading")

### Description[¶](#id1 "Link to this heading")

> The `DBMS_OUTPUT` package is especially useful for displaying PL/SQL debugging information. ([Oracle PL/SQL DBMS\_OUTPUT](https://docs.oracle.com/en/database/oracle/oracle-database/21/arpls/DBMS_OUTPUT.html#GUID-C1400094-18D5-4F36-A2C9-D28B0E12FD8C))

### PUT\_LINE procedure[¶](#put-line-procedure "Link to this heading")

Translation reference for DBMS\_OUTPUT.PUT\_LINE.

#### Description[¶](#id2 "Link to this heading")

> This procedure places a line in the buffer. ([Oracle PL/SQL DBMSOUTPUT.PUT\_LINE](https://docs.oracle.com/en/database/oracle/oracle-database/21/arpls/DBMS_OUTPUT.html#GUID-19FA480D-591E-4584-9650-5D37C4AFA530))

This UDF is implemented using a temporary table to insert the data to be displayed to replicate the functionality of Oracle `DBMS_OUTPUT.PUT_LINE` function.

#### Syntax[¶](#syntax "Link to this heading")

```
 DBMS_OUTPUT.PUT_LINE(LOG VARCHAR);
```

Copy

#### Custom procedure[¶](#custom-procedure "Link to this heading")

##### Setup data[¶](#setup-data "Link to this heading")

The `DBMS_OUTPUT` schema must be created.

```
CREATE SCHEMA IF NOT EXISTS DBMS_OUTPUT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}';
```

Copy

##### DBMS\_OUTPUT.PUT\_LINE(VARCHAR)[¶](#dbms-output-put-line-varchar "Link to this heading")

##### **Parameters**[¶](#parameters "Link to this heading")

* **LOG**: Item in a buffer that you want to display.

```
CREATE OR REPLACE procedure DBMS_OUTPUT.PUT_LINE_UDF(LOG VARCHAR)
RETURNS VARCHAR
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}'
AS $$
   
  //Performance may be affected by using this UDF.
  //If you want to start logging information, please uncomment the implementation.
  //Once the calls of DBMS_OUTPUT.PUT_LINE have been done, please use
  //the following query to read all the logs:
  //SELECT * FROM DBMS_OUTPUT.DBMS_OUTPUT_LOG.

  //snowflake.execute({sqlText:`
  //CREATE TEMPORARY TABLE IF NOT EXISTS DBMS_OUTPUT_LOG 
  //(
  //  WHEN TIMESTAMP,
  //  DATABASE VARCHAR,
  //  LOG VARCHAR
  //);`});

  //snowflake.execute({sqlText:`INSERT INTO DBMS_OUTPUT_LOG(WHEN, DATABASE, LOG) VALUES (CURRENT_TIMESTAMP,CURRENT_DATABASE(),?)`, binds:[LOG]});
  return LOG;
$$;
```

Copy

Note

* Note that this is using a temporary table, if you want the data to persist after a session ends, please remove TEMPORARY from the CREATE TABLE.
* The [temporary tables](https://docs.snowflake.com/en/user-guide/tables-temp-transient.html#temporary-tables) store non-permanent transitory data. They only exist within the session in which they were created and persist only for the rest of the session. After the session ends, the data stored in the table is completely removed from the system and is therefore not recoverable, either by the user who created the table or by Snowflake.

Warning

If you do not use the temporary table, keep in mind that you may need another column in the table where the USER running DBMS\_OUTPUT.PUT\_LINE UDF is inserted to avoid confusion.

##### Usage example[¶](#usage-example "Link to this heading")

###### Oracle[¶](#oracle "Link to this heading")

```
CREATE OR REPLACE PROCEDURE PROC 
IS
BEGIN
    DBMS_OUTPUT.PUT_LINE('Test');
END;

CALL PROC();
```

Copy

###### Result[¶](#result "Link to this heading")

```
|DBMS_OUTPUT.PUT_LINE('test') |
|-----------------------------|
|test                         |
```

Copy

###### Snowflake[¶](#snowflake "Link to this heading")

```
CREATE OR REPLACE PROCEDURE PROC ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        --** SSC-FDM-OR0035 - CHECK UDF IMPLEMENTATION FOR DBMS_OUTPUT.PUT_LINE_UDF. **
        CALL DBMS_OUTPUT.PUT_LINE_UDF('Test');
    END;
$$;

CALL PROC();
```

Copy

###### Result[¶](#id3 "Link to this heading")

```
|ROW |WHEN                    |DATABASE    |LOG      |
|----|------------------------|------------|---------|
| 1  |2022-04-25 11:16:23.844 |CODETEST    |test     |
```

Copy

#### Known Issues[¶](#known-issues "Link to this heading")

* The UDF code will remain commented out because it can affect performance, if the user decides to use it, they just need to uncomment the code.
* The user can modify the UDF so that the necessary information is inserted into the DBMS\_OUTPUT.PUT\_LINE table.

#### Related EWIs[¶](#related-ewis "Link to this heading")

1. [SSC-FDM-OR0035](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM.html#ssc-fdm-or0035): Check UDF implementation for DBMS\_OUTPUT.PUT\_LINE\_UDF.

## DBMS\_LOB[¶](#dbms-lob "Link to this heading")

### Description[¶](#id4 "Link to this heading")

> The `DBMS_LOB` package provides subprograms to operate on `BLOBs`, `CLOBs`, `NCLOBs`, `BFILEs`, and temporary `LOBs`. You can use `DBMS_LOB` to access and manipulate specific parts of a LOB or complete LOBs. ([Oracle PL/SQL DBMS\_LOB](https://docs.oracle.com/en/database/oracle/oracle-database/21/arpls/DBMS_LOB.html#GUID-A35DE03B-41A6-4E55-8CDE-77737FED9306))

### SUBSTR Function[¶](#substr-function "Link to this heading")

Translation reference for DBMS\_RANDOM.SUBSTR.

#### Description[¶](#id5 "Link to this heading")

> This function returns `amount` bytes or characters of a LOB, starting from an absolute `offset` from the beginning of the LOB. ([Oracle PL/SQL DBMS\_LOB.SUBSTR](https://docs.oracle.com/en/database/oracle/oracle-database/21/arpls/DBMS_LOB.html))

This built-in function is replaced with Snowflake [SUBSTR function](https://docs.snowflake.com/en/sql-reference/functions/substr.html#substr-substring). However, there are some differences.

Note

The **amount** and **offset** parameters are inverted in Snowflake

#### Syntax[¶](#id6 "Link to this heading")

```
DBMS_LOB.SUBSTR (
   lob_loc     IN    BLOB,
   amount      IN    INTEGER := 32767,
   offset      IN    INTEGER := 1)
  RETURN RAW;

DBMS_LOB.SUBSTR (
   lob_loc     IN    CLOB   CHARACTER SET ANY_CS,
   amount      IN    INTEGER := 32767,
   offset      IN    INTEGER := 1)
  RETURN VARCHAR2 CHARACTER SET lob_loc%CHARSET;

DBMS_LOB.SUBSTR (
   file_loc     IN    BFILE,
   amount      IN    INTEGER := 32767,
   offset      IN    INTEGER := 1)
  RETURN RAW;
```

Copy

#### Function overloads[¶](#function-overloads "Link to this heading")

**DBMS\_LOB.SUBSTR(‘string’, amount, offset)**

##### Usage example[¶](#id7 "Link to this heading")

###### Oracle[¶](#id8 "Link to this heading")

```
SELECT 
-- 1. "some magic here"
DBMS_LOB.SUBSTR('some magic here', 15, 1) "1",
-- 2. "some"
DBMS_LOB.SUBSTR('some magic here', 4, 1) "2",
-- 3. "me magic here"
DBMS_LOB.SUBSTR('some magic here', 15, 3) "3",
-- 4. "magic"
DBMS_LOB.SUBSTR('some magic here', 5, 6) "4",
-- 5. "here"
DBMS_LOB.SUBSTR('some magic here', 20, 12) "5",
-- 6. " "
DBMS_LOB.SUBSTR('some magic here', 250, 16) "6"
FROM DUAL;
```

Copy

###### Result[¶](#id9 "Link to this heading")

```
1              |2   |3            |4    |5   |6|
---------------+----+-------------+-----+----+-+
some magic here|some|me magic here|magic|here| |
```

Copy

###### Snowflake[¶](#id10 "Link to this heading")

```
SELECT
-- 1. "some magic here"
SUBSTR('some magic here', 1, 15) "1",
-- 2. "some"
SUBSTR('some magic here', 1, 4) "2",
-- 3. "me magic here"
SUBSTR('some magic here', 3, 15) "3",
-- 4. "magic"
SUBSTR('some magic here', 6, 5) "4",
-- 5. "here"
SUBSTR('some magic here', 12, 20) "5",
-- 6. " "
SUBSTR('some magic here', 16, 250) "6"
FROM DUAL;
```

Copy

###### Result[¶](#id11 "Link to this heading")

```
1              |2   |3            |4    |5   |6|
---------------+----+-------------+-----+----+-+
some magic here|some|me magic here|magic|here| |
```

Copy

##### DBMS\_LOB.SUBSTR(**B**LOB, amount, offset)[¶](#dbms-lob-substr-blob-amount-offset "Link to this heading")

###### Usage example[¶](#id12 "Link to this heading")

Warning

Result values in Oracle and Snowflake are being converted from bytes to strings for easier understanding of the function.

For **Snowflake** consider using:

**hex\_decode\_string( to\_varchar(SUBSTR(blob\_column, 1, 6), ‘HEX’));**

and for **Oracle** consider using:

**utl\_raw.cast\_to\_varchar2(DBMS\_LOB.SUBSTR(blob\_column, 1, 6));**

to obtain the result as a string.

###### Oracle[¶](#id13 "Link to this heading")

```
-- Create Table
CREATE TABLE blobtable( blob_column BLOB );

-- Insert sample value
INSERT INTO blobtable VALUES (utl_raw.cast_to_raw('some magic here'));

-- Select different examples
SELECT 
-- 1. "some magic here"
DBMS_LOB.SUBSTR(blob_column, 15, 1) "1",
-- 2. "some"
DBMS_LOB.SUBSTR(blob_column, 4, 1) "2",
-- 3. "me magic here"
DBMS_LOB.SUBSTR(blob_column, 15, 3) "3",
-- 4. "magic"
DBMS_LOB.SUBSTR(blob_column, 5, 6) "4",
-- 5. "here"
DBMS_LOB.SUBSTR(blob_column, 20, 12) "5",
-- 6. " "
DBMS_LOB.SUBSTR(blob_column, 250, 16) "6"
FROM BLOBTABLE;
```

Copy

###### Result[¶](#id14 "Link to this heading")

```
1              |2   |3            |4    |5   |6|
---------------+----+-------------+-----+----+-+
some magic here|some|me magic here|magic|here| |
```

Copy

###### Snowflake[¶](#id15 "Link to this heading")

```
-- Create Table
CREATE OR REPLACE TABLE blobtable ( blob_column BINARY
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
;

-- Insert sample value
INSERT INTO blobtable
VALUES (
!!!RESOLVE EWI!!! /*** SSC-EWI-OR0076 - TRANSLATION FOR BUILT-IN PACKAGE 'utl_raw.cast_to_raw' IS NOT CURRENTLY SUPPORTED. ***/!!!
'' AS cast_to_raw);

-- Select different examples
SELECT
-- 1. "some magic here"
SUBSTR(blob_column, 1, 15) "1",
-- 2. "some"
SUBSTR(blob_column, 1, 4) "2",
-- 3. "me magic here"
SUBSTR(blob_column, 3, 15) "3",
-- 4. "magic"
SUBSTR(blob_column, 6, 5) "4",
-- 5. "here"
SUBSTR(blob_column, 12, 20) "5",
-- 6. " "
SUBSTR(blob_column, 16, 250) "6"
FROM
BLOBTABLE;
```

Copy

###### Result[¶](#id16 "Link to this heading")

```
1              |2   |3            |4    |5   |6|
---------------+----+-------------+-----+----+-+
some magic here|some|me magic here|magic|here| |
```

Copy

Warning

**Note:** `UTL_RAW.CAST_TO_RAW()` is currently not being transformed to `TO_BINARY()`. The function is used to show the functional equivalence of the example.

##### DBMS\_LOB.SUBSTR(CLOB, amount, offset)[¶](#dbms-lob-substr-clob-amount-offset "Link to this heading")

###### Usage example[¶](#id17 "Link to this heading")

###### Oracle[¶](#id18 "Link to this heading")

```
-- Create Table
CREATE TABLE clobtable(clob_column CLOB);

-- Insert sample value
INSERT INTO clobtable VALUES ('some magic here');

-- Select
SELECT 
-- 1. "some magic here"
DBMS_LOB.SUBSTR(clob_column, 15, 1) "1",
-- 2. "some"
DBMS_LOB.SUBSTR(clob_column, 4, 1) "2",
-- 3. "me magic here"
DBMS_LOB.SUBSTR(clob_column, 15, 3) "3",
-- 4. "magic"
DBMS_LOB.SUBSTR(clob_column, 5, 6) "4",
-- 5. "here"
DBMS_LOB.SUBSTR(clob_column, 20, 12) "5",
-- 6. " "
DBMS_LOB.SUBSTR(clob_column, 250, 16) "6"
FROM clobtable;
```

Copy

###### Result[¶](#id19 "Link to this heading")

```
1              |2   |3            |4    |5   |6|
---------------+----+-------------+-----+----+-+
some magic here|some|me magic here|magic|here| |
```

Copy

###### Snowflake[¶](#id20 "Link to this heading")

```
-- Create Table
CREATE OR REPLACE TABLE clobtable (clob_column VARCHAR
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}}'
;

-- Insert sample value
INSERT INTO clobtable
VALUES ('some magic here');

-- Select
SELECT
-- 1. "some magic here"
SUBSTR(clob_column, 1, 15) "1",
-- 2. "some"
SUBSTR(clob_column, 1, 4) "2",
-- 3. "me magic here"
SUBSTR(clob_column, 3, 15) "3",
-- 4. "magic"
SUBSTR(clob_column, 6, 5) "4",
-- 5. "here"
SUBSTR(clob_column, 12, 20) "5",
-- 6. " "
SUBSTR(clob_column, 16, 250) "6"
FROM
clobtable;
```

Copy

###### Result[¶](#id21 "Link to this heading")

```
1              |2   |3            |4    |5   |6|
---------------+----+-------------+-----+----+-+
some magic here|some|me magic here|magic|here| |
```

Copy

Warning

**Note:** `UTL_RAW.CAST_TO_RAW()` is currently not being transformed to `TO_BINARY()`. The function is used to show the functional equivalence of the example.

##### DBMS\_LOB.SUBSTR(BFILE, amount, offset)[¶](#dbms-lob-substr-bfile-amount-offset "Link to this heading")

###### Usage example[¶](#id22 "Link to this heading")

Using DBMS\_LOB.SUBSTR() on a BFILE column returns a substring of the file content.

Warning

Next example is **not** a current migration, but a functional example to show the differences of the SUBSTR function on BFILE types.

**File Content (file.txt):**

```
some magic here
```

Copy

###### Oracle[¶](#id23 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE bfile_substr_procedure
IS
    fil BFILE := BFILENAME('MY_DIR', 'file.txt');
BEGIN
    DBMS_LOB.FILEOPEN(fil, DBMS_LOB.FILE_READONLY);
    DBMS_OUTPUT.PUT_LINE(UTL_RAW.CAST_TO_VARCHAR2(DBMS_LOB.SUBSTR(fil,9,1)));
    --Console Output:
    -- "some magi"
    DBMS_LOB.FILECLOSE(fil);
END;
```

Copy

###### Console Log[¶](#console-log "Link to this heading")

```
DBMS_OUTPUT.PUT_LINE(UTL_RAW.CAST_TO_VARCHAR2(DBMS_LOB.SUBSTR(fil,4,1))) |
-------------------------------------------------------------------------|
some magi                                                                |
```

Copy

###### Snowflake[¶](#id24 "Link to this heading")

**BFILE** columns are translated into **VARCHAR** columns, therefore applying a `SUBSTR` function on the same column would return a substring of the file name, not the file content.

```
CREATE OR REPLACE PROCEDURE bfile_substr_procedure ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        fil VARCHAR := PUBLIC.BFILENAME_UDF('MY_DIR', 'file.txt');
    BEGIN
        !!!RESOLVE EWI!!! /*** SSC-EWI-OR0076 - TRANSLATION FOR BUILT-IN PACKAGE 'DBMS_LOB.FILEOPEN' IS NOT CURRENTLY SUPPORTED. ***/!!!
        DBMS_LOB.FILEOPEN(:fil,
        !!!RESOLVE EWI!!! /*** SSC-EWI-OR0076 - TRANSLATION FOR BUILT-IN PACKAGE 'DBMS_LOB.FILE_READONLY' IS NOT CURRENTLY SUPPORTED. ***/!!!
        '' AS FILE_READONLY);
        --** SSC-FDM-OR0035 - CHECK UDF IMPLEMENTATION FOR DBMS_OUTPUT.PUT_LINE_UDF. **
        CALL DBMS_OUTPUT.PUT_LINE_UDF(
        !!!RESOLVE EWI!!! /*** SSC-EWI-OR0076 - TRANSLATION FOR BUILT-IN PACKAGE 'UTL_RAW.CAST_TO_VARCHAR2' IS NOT CURRENTLY SUPPORTED. ***/!!!
        '' AS CAST_TO_VARCHAR2);
        --Console Output:
        -- "some magi"
        !!!RESOLVE EWI!!! /*** SSC-EWI-OR0076 - TRANSLATION FOR BUILT-IN PACKAGE 'DBMS_LOB.FILECLOSE' IS NOT CURRENTLY SUPPORTED. ***/!!!
        DBMS_LOB.FILECLOSE(:fil);
    END;
$$;
```

Copy

###### Result[¶](#id25 "Link to this heading")

| SUBSTR(bfile\_column, 1, 9) |
| --- |
| MY\_DIR\fi |

#### Known Issues[¶](#id26 "Link to this heading")

##### 1. Using DBMS\_LOB.SUBSTR with BFILE columns[¶](#using-dbms-lob-substr-with-bfile-columns "Link to this heading")

The current transformation for BFILE datatypes in columns is VARCHAR, where the name of the file is stored as a string. Therefore applying the SUBSTR function on a BFILE column after transformation will return a substring of the file name, while Oracle would return a substring of the file content.

#### Related EWIs[¶](#id27 "Link to this heading")

1. [SSC-EWI-OR0076](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI.html#ssc-ewi-or0076): Built In Package Not Supported.
2. [SSC-FDM-OR0035](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM.html#ssc-fdm-or0035): DBMS\_OUTPUT.PUTLINE check UDF implementation.

## UTL\_FILE[¶](#utl-file "Link to this heading")

### Description[¶](#id28 "Link to this heading")

> With `UTL_FILE` package, PL/SQL programs can read and write text files. ([Oracle PL/SQL UTL\_FILE](https://docs.oracle.com/en/database/oracle/oracle-database/21/arpls/UTL_FILE.html#GUID-EBC42A36-EB72-4AA1-B75F-8CF4BC6E29B4))

### FCLOSE procedure[¶](#fclose-procedure "Link to this heading")

Translation reference for UTL\_FILE.FCLOSE.

#### Description[¶](#id29 "Link to this heading")

> This procedure closes an open file identified by a file handle. ([Oracle PL/SQL UTL\_FILE.FCLOSE](https://docs.oracle.com/en/database/oracle/oracle-database/21/arpls/UTL_FILE.html#GUID-68874564-1A2C-4071-8D48-60539C805E0D))

This procedure is implemented using Snowflake [STAGE](https://docs.snowflake.com/en/sql-reference/sql/create-stage.html) to store the written text files.

Note

This procedure requires to be used in conjunction with:

* [`UTL_FILE.FOPEN`](#fopen-procedure) procedure

#### Syntax[¶](#id30 "Link to this heading")

```
UTL_FILE.FCLOSE(
    FILE VARCHAR
    );
```

Copy

#### Setup data[¶](#id31 "Link to this heading")

* The `UTL_FILE` schema must be created.

```
CREATE SCHEMA IF NOT EXISTS UTL_FILE
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}';
```

Copy

* If you want to download the file, run the following command.

```
GET @UTL_FILE.utlfile_local_directory/<filename> file://<path_to_file>/<filename>;
```

Copy

Warning

* The [GET](https://docs.snowflake.com/en/sql-reference/sql/get.html) command runs in [Snowflake CLI](https://docs.snowflake.com/en/user-guide/snowsql-install-config.html).

#### Custom procedure overloads[¶](#custom-procedure-overloads "Link to this heading")

##### UTL\_FILE.FCLOSE(VARCHAR)[¶](#utl-file-fclose-varchar "Link to this heading")

###### **Parameters**[¶](#id32 "Link to this heading")

* **FILE**: Active file handler returned from the call to [`UTL_FILE.FOPEN`](#fopen-procedure)

###### Functionality[¶](#functionality "Link to this heading")

This procedure uses the `FOPEN_TABLES_LINES` table created in the [`UTL_FILE.FOPEN`](#fopen-procedure) procedure.

This procedure writes to the utlfile\_local\_directory stage all lines with the same `FHANDLE` from the file in `FOPEN_TABLES_LINES`.

```
CREATE OR REPLACE PROCEDURE UTL_FILE.FCLOSE_UDF(FILE VARCHAR)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}'
AS
$$
     DECLARE
        fhandle VARCHAR;
        fileParse VARIANT;
        File_is_read_only exception;
        fileNameConcat VARCHAR;
        copyIntoQuery VARCHAR ;
    BEGIN
        fileParse:= PARSE_JSON(FILE);
        fhandle:= :fileParse:handle;
        fileNameConcat:= '@UTL_FILE.utlfile_local_directory/'||:fileParse:name;
        copyIntoQuery:= 'COPY INTO '||:fileNameConcat||' FROM (SELECT LINE FROM UTL_FILE.FOPEN_TABLES_LINES WHERE FHANDLE = ? ORDER BY SEQ) FILE_FORMAT= (FORMAT_NAME = my_csv_format COMPRESSION=NONE)   OVERWRITE=TRUE';
        EXECUTE IMMEDIATE :copyIntoQuery USING (fhandle);
        DELETE FROM UTL_FILE.FOPEN_TABLES_LINES WHERE FHANDLE = :fhandle;
        DELETE FROM UTL_FILE.FOPEN_TABLES WHERE FHANDLE = :fhandle;
    END
$$;
```

Copy

Note

* Note that this procedure uses the **stage** that was created previously. For now, if you want to write the file in another stage, you must modify the name.
* These procedures are implemented for the internal stages in the [`COPY INTO`](https://docs.snowflake.com/en/sql-reference/sql/copy-into-location.html)

##### Usage example[¶](#id33 "Link to this heading")

###### Oracle[¶](#id34 "Link to this heading")

```
DECLARE 
    w_file UTL_FILE.FILE_TYPE;
BEGIN
    w_file:= UTL_FILE.FOPEN('MY_DIR','test.csv','w',1024);
    UTL_FILE.PUT_LINE(w_file,'New line');
    UTL_FILE.FCLOSE(w_file); 
END;
```

Copy

Warning

To run this example, see [`ORACLE UTL_FILE`](https://docs.oracle.com/en/database/oracle/oracle-database/21/arpls/UTL_FILE.html#GUID-FA16A38B-26AA-4002-9BE0-7D3950557F8C)

###### Snowflake[¶](#id35 "Link to this heading")

```
DECLARE
    w_file OBJECT /*** SSC-FDM-0015 - REFERENCED CUSTOM TYPE 'UTL_FILE.FILE_TYPE' IN QUERY NOT FOUND, USAGES MAY BE AFFECTED ***/ := OBJECT_CONSTRUCT();
    call_results VARIANT;
BEGIN
    w_file:=
    --** SSC-FDM-OR0036 - PARAMETERS: 'LOCATION, MAX_LINESIZE_UDF' UNNECESSARY IN THE IMPLEMENTATION. **
    UTL_FILE.FOPEN_UDF('MY_DIR','test.csv','w',1024);
    --** SSC-FDM-OR0036 - PARAMETERS: 'AUTOFLUSH_UDF' UNNECESSARY IN THE IMPLEMENTATION. **
    call_results := (
        CALL UTL_FILE.PUT_LINE_UDF(:w_file,'New line')
    );
    call_results := (
        CALL UTL_FILE.FCLOSE_UDF(:w_file)
    );
    RETURN call_results;
END;
```

Copy

#### Known Issues[¶](#id36 "Link to this heading")

##### 1. **Modify the procedure for changing the name of the stage.**[¶](#modify-the-procedure-for-changing-the-name-of-the-stage "Link to this heading")

The user can modify the procedure if it is necessary to change the name of the stage.

##### 2. Location **static.**[¶](#location-static "Link to this heading")

The location used to write to this procedure is static. A new version of the procedure is expected to increase its extensibility by using the location that has the `FILE` parameter.

##### 5. Files supported.[¶](#files-supported "Link to this heading")

This procedure for now, only writes .CSV files.

#### Related EWIs[¶](#id37 "Link to this heading")

1. [SSC-FDM-0015](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0015): Data Type Not Recognized.
2. [SSC-FDM-OR0036](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM.html#ssc-fdm-or0036): Unnecessary built-in packages parameters.

### FOPEN procedure[¶](#fopen-procedure "Link to this heading")

Translation reference for UTL\_FILE.FOPEN.

#### Description[¶](#id38 "Link to this heading")

> This procedure opens a file. ([Oracle PL/SQL UTL\_FILE.FOPEN](https://docs.oracle.com/en/database/oracle/oracle-database/21/arpls/UTL_FILE.html#GUID-DF14ADC3-983D-4E0F-BE2C-60733FF58539))

This procedure is implemented using Snowflake [STAGE](https://docs.snowflake.com/en/sql-reference/sql/create-stage.html) to store the text files.

The user is in charge of uploading the local files to the [STAGE](https://docs.snowflake.com/en/sql-reference/sql/create-stage.html) to be used by the procedure.

Note

This procedure requires to be used in conjunction with:

* [`UTL_FILE.FCLOSE`](#fclose-procedure) procedure

#### Syntax[¶](#id39 "Link to this heading")

```
UTL_FILE.FOPEN(
    LOCATION VARCHAR,
    FILENAME VARCHAR,
    OPEN_MODE VARCHAR,
    MAX_LINESIZE NUMBER,
    );
```

Copy

#### Setup data[¶](#id40 "Link to this heading")

* The `UTL_FILE` schema must be created.

```
CREATE SCHEMA IF NOT EXISTS UTL_FILE
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}';
```

Copy

* Create the stage `utlfile_local_directory`.

```
CREATE OR REPLACE FILE FORMAT  my_csv_format TYPE = csv;

CREATE OR REPLACE STAGE utlfile_local_directory
  file_format = my_csv_format;
```

Copy

* If the value in the `OPEN_MODE` parameter is **w** or **r** it is necessary to upload the file in the `utlfile_local_directory`.

```
PUT file://<path_to_file>/<filename> @UTL_FILE.utlfile_local_directory auto_compress=false;
```

Copy

Warning

* The [PUT](https://docs.snowflake.com/en/sql-reference/sql/put.html) command runs in [Snowflake CLI](https://docs.snowflake.com/en/user-guide/snowsql-install-config.html).

#### Custom procedure overloads[¶](#id41 "Link to this heading")

##### UTL\_FILE.FOPEN( VARCHAR, VARCHAR)[¶](#utl-file-fopen-varchar-varchar "Link to this heading")

###### **Parameters**[¶](#id42 "Link to this heading")

* **FILENAME:** The name of the file, including extension\*\*.\*\*
* **OPEN\_MODE:** Specifies how the file is opened.

###### **Open modes**[¶](#open-modes "Link to this heading")

The Oracle Built-in package [`UTL_FILE.FOPEN`](https://docs.oracle.com/en/database/oracle/oracle-database/21/arpls/UTL_FILE.html#GUID-DF14ADC3-983D-4E0F-BE2C-60733FF58539) procedure supports six modes of how to open the file, but only three of them are supported in the Snowscripting procedure.

| OPEN\_MODE | DESCRIPTION | STATUS |
| --- | --- | --- |
| w | Write mode | Supported |
| a | Append mode | Supported |
| r | Read mode | Supported |
| rb | Read byte mode | Unsupported |
| wb | Write byte mode | Unsupported |
| ab | Append byte mode | Unsupported |

###### Functionality[¶](#id43 "Link to this heading")

This procedure uses two tables with which the operation of opening a file will be emulated. The `FOPEN_TABLES` table will store the files that are open and the `FOPEN_TABLES_LINES` table stores the lines that each file owns.

If the file is opened in write mode, a new file is created, if it is opened in read or append mode, it loads the lines of the file in `FOPEN_TABLES_LINES` and inserts the file in `FOPEN_TABLES`.

```
CREATE OR REPLACE PROCEDURE UTL_FILE.FOPEN_UDF(FILENAME VARCHAR,OPEN_MODE VARCHAR)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}'
AS $$
    DECLARE
        fhandle VARCHAR;
        key VARCHAR;
        status VARCHAR;
        File_is_not_loaded_on_stage exception;
        fileNameConcat VARCHAR:= '@UTL_FILE.utlfile_local_directory/'||:FILENAME;
        copyIntoQuery VARCHAR DEFAULT 'COPY INTO UTL_FILE.FOPEN_TABLES_LINES (FHANDLE, LINE) FROM (SELECT ? , stageFile.$1 FROM '||:fileNameConcat||' stageFile)';
    BEGIN
        CREATE TABLE IF NOT EXISTS UTL_FILE.FOPEN_TABLES 
        (
          FHANDLE VARCHAR, 
          FILENAME VARCHAR,
          OPEN_MODE VARCHAR
        );

        CREATE TABLE IF NOT EXISTS UTL_FILE.FOPEN_TABLES_LINES 
        (
          SEQ    NUMBER AUTOINCREMENT,
          FHANDLE VARCHAR, 
          LINE    VARCHAR
        );   
        SELECT FHANDLE INTO fhandle FROM UTL_FILE.FOPEN_TABLES WHERE FILENAME = :FILENAME;
        SELECT UUID_STRING() INTO key;
        IF (OPEN_MODE = 'w') THEN
            INSERT INTO UTL_FILE.FOPEN_TABLES(FHANDLE, FILENAME, OPEN_MODE) VALUES(:key,:FILENAME,:OPEN_MODE);
            RETURN TO_JSON({ 'name': FILENAME, 'handle': key});
        ELSE
            IF (fhandle IS NULL) THEN
                EXECUTE IMMEDIATE :copyIntoQuery USING (key);
                SELECT OBJECT_CONSTRUCT(*):status INTO status FROM table(result_scan(last_query_id()));
                IF (status = 'LOADED') THEN
                    INSERT INTO UTL_FILE.FOPEN_TABLES(FHANDLE, FILENAME, OPEN_MODE) VALUES(:key,:FILENAME,:OPEN_MODE);
                    RETURN TO_JSON({'name': FILENAME, 'handle': key});
                ELSE
                    raise File_is_not_loaded_on_stage;
                END IF;
            ELSE
                UPDATE UTL_FILE.FOPEN_TABLES SET OPEN_MODE = :OPEN_MODE WHERE FHANDLE = :fhandle;
                RETURN TO_JSON({'name': FILENAME, 'handle': fhandle});
           END IF;
        END IF;     
    END
$$;
```

Copy

Note

* Note that this procedure uses the **stage** that was created previously. For now, if you want to use another name for the stage, you must modify the procedure.
* These procedures are implemented for the internal stages in the [`COPY INTO`](https://docs.snowflake.com/en/sql-reference/sql/copy-into-table.html)

##### Usage example[¶](#id44 "Link to this heading")

###### Oracle[¶](#id45 "Link to this heading")

```
DECLARE 
    w_file UTL_FILE.FILE_TYPE;
BEGIN
    w_file:= UTL_FILE.FOPEN('MY_DIR','test.csv','w',1024);
END;
```

Copy

Warning

To run this example, see [`ORACLE UTL_FILE`](https://docs.oracle.com/en/database/oracle/oracle-database/21/arpls/UTL_FILE.html#GUID-FA16A38B-26AA-4002-9BE0-7D3950557F8C)

###### Snowflake[¶](#id46 "Link to this heading")

```
DECLARE
    w_file OBJECT /*** SSC-FDM-0015 - REFERENCED CUSTOM TYPE 'UTL_FILE.FILE_TYPE' IN QUERY NOT FOUND, USAGES MAY BE AFFECTED ***/ := OBJECT_CONSTRUCT();
BEGIN
    w_file:=
    --** SSC-FDM-OR0036 - PARAMETERS: 'LOCATION, MAX_LINESIZE_UDF' UNNECESSARY IN THE IMPLEMENTATION. **
    UTL_FILE.FOPEN_UDF('MY_DIR','test.csv','w',1024);
END;
```

Copy

#### Known Issues[¶](#id47 "Link to this heading")

##### 1. **Modify the procedure for changing the name of the stage.**[¶](#id48 "Link to this heading")

The user can modify the procedure if it is necessary to change the name of the stage.

##### 2. **`LOCATION` parameter is not used.**[¶](#location-parameter-is-not-used "Link to this heading")

The `LOCATION` parameter is not used now because the stage used in the procedure is static. It is planned for an updated version of the procedure to increase its extensibility by using this parameter to enter the name of the stage where the file you want to open is located.

##### 3. `MAX_LINESIZE` parameter is not used.[¶](#max-linesize-parameter-is-not-used "Link to this heading")

The Oracle Built-in package [`UTL_FILE.FOPEN`](https://docs.oracle.com/en/database/oracle/oracle-database/21/arpls/UTL_FILE.html#GUID-DF14ADC3-983D-4E0F-BE2C-60733FF58539) procedure has the `MAX_LINESIZE` parameter, but in the Snowscripting procedure it is removed because it is not used.

##### 4. `OPEN_MODE` values supported.[¶](#open-mode-values-supported "Link to this heading")

This procedure supports *write* (**w**), *read* (**r**), and *append* (**a**) modes to open files.

##### 5. Files supported.[¶](#id49 "Link to this heading")

This procedure for now, only supports .CSV files.

#### Related EWIs[¶](#id50 "Link to this heading")

1. [SSC-FDM-0015](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0015): Data Type Not Recognized.
2. [SSC-FDM-OR0036](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM.html#ssc-fdm-or0036): UnnecessaryBuiltInPackagesParameters

### PUT\_LINE procedure[¶](#id51 "Link to this heading")

Translation reference for UTL\_FILE.PUT\_LINE.

#### Description[¶](#id52 "Link to this heading")

> This procedure writes the text string stored in the buffer parameter to the open file identified by the file handle. ([Oracle PL/SQL UTL\_FILE.PUT\_LINE](https://docs.oracle.com/en/database/oracle/oracle-database/21/arpls/UTL_FILE.html#GUID-BC046363-6F14-4128-B4D2-836DDBDB9B48))

#### Syntax[¶](#id53 "Link to this heading")

```
UTL_FILE.PUT_LINE(
    FILE VARCHAR,
    BUFFER VARCHAR,
    );
```

Copy

#### Setup data[¶](#id54 "Link to this heading")

* The `UTL_FILE` schema must be created.

```
CREATE SCHEMA IF NOT EXISTS UTL_FILE
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}';
```

Copy

#### Custom UDF[¶](#custom-udf "Link to this heading")

##### UTL\_FILE.PUT\_LINE(VARCHAR, VARCHAR)[¶](#utl-file-put-line-varchar-varchar "Link to this heading")

###### **Parameters**[¶](#id55 "Link to this heading")

* **FILE**: Active file handler returned from the call to [`UTL_FILE.FOPEN`](#fopen-procedure)
* **BUFFER:** Text buffer that contains the text to be written to the file\*\*.\*\*

###### Functionality[¶](#id56 "Link to this heading")

This procedure uses the `FOPEN_TABLES_LINES` table created in the [`UTL_FILE.FOPEN`](#fopen-procedure) procedure.

If the `OPEN_MODE` of the file is *write* (**w**) or *append* (**a**), it inserts the buffer into `FOPEN_TABLES_LINES`, but if the `OPEN_MODE` is read (**r**), it throws the `File_is_read_only` exception.

```
CREATE OR REPLACE PROCEDURE UTL_FILE.PUT_LINE_UDF(FILE VARCHAR,BUFFER VARCHAR)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}'
AS $$
    DECLARE 
        openMode VARCHAR;
        openModeTemp VARCHAR;
        fhandle VARCHAR;
        fileParse VARIANT;
        File_is_read_only exception;
    BEGIN
        fileParse:= PARSE_JSON(FILE);
        fhandle:= :fileParse:handle;
        SELECT OPEN_MODE INTO openModeTemp FROM UTL_FILE.FOPEN_TABLES WHERE FHANDLE = :fhandle; 
        IF (openModeTemp = 'a' or openModeTemp = 'w') THEN
            INSERT INTO UTL_FILE.FOPEN_TABLES_LINES(FHANDLE,LINE) VALUES(:fhandle,:BUFFER);
        ELSE  
            raise File_is_read_only;
        END IF;
    END
$$;  

-- This SELECT is manually added and not generated by SnowConvert AI
SELECT * FROM UTL_FILE.FOPEN_TABLES_LINES;
```

Copy

Warning

**Note:**

* To use this procedure you must open the file with [UTL\_FILE.FOPEN](#fopen-procedure)

##### Usage example[¶](#id57 "Link to this heading")

###### Oracle[¶](#id58 "Link to this heading")

```
DECLARE
    w_file UTL_FILE.FILE_TYPE;
BEGIN
    w_file:= UTL_FILE.FOPEN('MY_DIR','test.csv','w',1024);
    UTL_FILE.PUT_LINE(w_file,'New line');
END;
```

Copy

Warning

To run this example, see [`ORACLE UTL_FILE`](https://docs.oracle.com/en/database/oracle/oracle-database/21/arpls/UTL_FILE.html#GUID-FA16A38B-26AA-4002-9BE0-7D3950557F8C)

###### Snowflake[¶](#id59 "Link to this heading")

```
DECLARE
    w_file OBJECT /*** SSC-FDM-0015 - REFERENCED CUSTOM TYPE 'UTL_FILE.FILE_TYPE' IN QUERY NOT FOUND, USAGES MAY BE AFFECTED ***/ := OBJECT_CONSTRUCT();
    call_results VARIANT;
BEGIN
    w_file:=
    --** SSC-FDM-OR0036 - PARAMETERS: 'LOCATION, MAX_LINESIZE_UDF' UNNECESSARY IN THE IMPLEMENTATION. **
    UTL_FILE.FOPEN_UDF('MY_DIR','test.csv','w',1024);
    --** SSC-FDM-OR0036 - PARAMETERS: 'AUTOFLUSH_UDF' UNNECESSARY IN THE IMPLEMENTATION. **
    call_results := (
        CALL UTL_FILE.PUT_LINE_UDF(:w_file,'New line')
    );
    RETURN call_results;
END;
```

Copy

#### Known Issues[¶](#id60 "Link to this heading")

##### 1. `AUTOFLUSH` parameter is not used.[¶](#autoflush-parameter-is-not-used "Link to this heading")

The Oracle Built-in package [`UTL_FILE.PUT_LINE`](https://docs.oracle.com/en/database/oracle/oracle-database/21/arpls/UTL_FILE.html#GUID-BC046363-6F14-4128-B4D2-836DDBDB9B48) procedure has the `AUTOFLUSH` parameter, but in the Snowscripting procedure it is removed because it is not used.

#### Related EWIs[¶](#id61 "Link to this heading")

1. [SSC-FDM-0015](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0015): Data Type Not Recognized.
2. [SSC-FDM-OR0036](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM.html#ssc-fdm-or0036): Unnecessary built-in packages parameters.

## DBMS\_RANDOM[¶](#dbms-random "Link to this heading")

### Description[¶](#id62 "Link to this heading")

> The `DBMS_RANDOM` package provides a built-in random number generator. `DBMS_RANDOM` is not intended for cryptography. ([Oracle PL/SQL DBMS\_RANDOM](https://docs.oracle.com/en/database/oracle/oracle-database/21/arpls/DBMS_RANDOM.html#GUID-8DC48B0C-3707-4172-A306-C0308DD2EB0F))

### VALUE functions[¶](#value-functions "Link to this heading")

Translation reference for DBMS\_RANDOM.VALUE.

#### Description[¶](#id63 "Link to this heading")

> The basic function gets a random number, greater than or equal to 0 and less than 1. Alternatively, you can get a random Oracle number **`X`**, where **`X`** is greater than or equal to `low` and less than `high`. ([Oracle PL/SQL DBMS\_RANDOM.VALUE](https://docs.oracle.com/en/database/oracle/oracle-database/21/arpls/DBMS_RANDOM.html#GUID-AAD9E936-D74F-440D-9E16-24F3F0DE8D31))

This UDF is implemented using the [Math.random](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/random) function of Javascript to replicate the functionality of Oracle DBMS\_RANDOM.VALUE function.

#### Syntax[¶](#id64 "Link to this heading")

```
DBMS_RANDOM.VALUE()
    RETURN NUMBER;

DBMS_RANDOM.VALUE(
    low NUMBER,
    high NUMBER)
    RETURN NUMBER;
```

Copy

#### Custom UDF overloads[¶](#custom-udf-overloads "Link to this heading")

##### Setup data[¶](#id65 "Link to this heading")

The `DBMS_RANDOM` schema must be created.

```
CREATE SCHEMA IF NOT EXISTS DBMS_RANDOM
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}';
```

Copy

##### DBMS\_RANDOM.VALUE()[¶](#dbms-random-value "Link to this heading")

###### **Parameters**[¶](#id66 "Link to this heading")

* No parameters.

```
CREATE OR REPLACE FUNCTION DBMS_RANDOM.VALUE_UDF()
RETURNS DOUBLE
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}'
AS
$$  
  return Math.random();
$$;
```

Copy

Note

**Note:** The UDF only supports approximately between 9 and 10 digits in the decimal part of the number (9 or 10 digits of precision)

##### Usage example[¶](#id67 "Link to this heading")

###### Oracle[¶](#id68 "Link to this heading")

```
SELECT DBMS_RANDOM.VALUE() FROM DUAL;
```

Copy

###### Result[¶](#id69 "Link to this heading")

```
|DBMS_RANDOM.VALUE()                         |
|--------------------------------------------|
|0.47337471168356406022193430290380483126    |
```

Copy

Note

The function can be called either\_`DBMS_RANDOM.VALUE()`\_ or *`DBMS_RANDOM.VALUE.`*

###### Snowflake[¶](#id70 "Link to this heading")

```
SELECT
--** SSC-FDM-OR0033 - DBMS_RANDOM.VALUE DIGITS OF PRECISION ARE LOWER IN SNOWFLAKE **
DBMS_RANDOM.VALUE_UDF() FROM DUAL;
```

Copy

###### Result[¶](#id71 "Link to this heading")

```
|DBMS_RANDOM.VALUE() |
|--------------------|
|0.1014560867        |
```

Copy

Note

In Snowflake, you must put the parentheses.

**DBMS\_RANDOM.VALUE(NUMBER, NUMBER)**

###### **Parameters**[¶](#id72 "Link to this heading")

* **low**: The lowest `NUMBER` from which a random number is generated. The number generated is greater than or equal to `low`.
* **high**: The highest `NUMBER` used as a limit when generating a random number. The number generated will be less than `high`.

```
CREATE OR REPLACE FUNCTION DBMS_RANDOM.VALUE_UDF(low double, high double)
RETURNS DOUBLE
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}'
AS
$$
    if (LOW > HIGH) {
        [LOW, HIGH] = [HIGH, LOW];
    }
    
    const MAX_DECIMAL_DIGITS = 38;
    return (Math.random() * (HIGH - LOW) + LOW).toFixed(MAX_DECIMAL_DIGITS);
$$;
```

Copy

Note

* The Oracle DBMS\_RANDOM.VALUE(low, high) function does not require parameters to have a specific order so the Snowflake UDF is implemented to support this feature by always taking out the highest and lowest number.
* The UDF only supports approximately between 9 and 10 digits in the decimal part of the number (9 or 10 digits of precision).

##### Usage example[¶](#id73 "Link to this heading")

###### Oracle[¶](#id74 "Link to this heading")

```
SELECT DBMS_RANDOM.VALUE(-10,30) FROM DUAL;
```

Copy

###### Result[¶](#id75 "Link to this heading")

```
|DBMS_RANDOM.VALUE(-10,30)                   |
|--------------------------------------------|
|16.0298681859960167648070354679783928085    |
```

Copy

###### Snowflake[¶](#id76 "Link to this heading")

```
SELECT
--** SSC-FDM-OR0033 - DBMS_RANDOM.VALUE DIGITS OF PRECISION ARE LOWER IN SNOWFLAKE **
DBMS_RANDOM.VALUE_UDF(-10,30) FROM DUAL;
```

Copy

###### Result[¶](#id77 "Link to this heading")

```
|DBMS_RANDOM.VALUE(-10,30)   |
|----------------------------|
|-6.346055187                |
```

Copy

#### Known Issues[¶](#id78 "Link to this heading")

No issues were found.

#### Related EWIs[¶](#id79 "Link to this heading")

1. [SSC-FDM-OR0033](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM.html#ssc-fdm-or0033): DBMS\_RANDOM.VALUE Built-In Package precision is lower in Snowflake.

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
2. [DBMS\_OUTPUT](#dbms-output)
3. [DBMS\_LOB](#dbms-lob)
4. [UTL\_FILE](#utl-file)
5. [DBMS\_RANDOM](#dbms-random)