---
description: Translation references to convert Teradata MLOAD files to Snowflake SQL
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/teradata/scripts-to-snowflake-sql-translation-reference/mload
title: SnowConvert AI - Teradata - MLOAD | Snowflake Documentation
---

## Import

### Description

> The IMPORT command specifies a source for data input.

For more information regarding Import MLoad, check
[here](https://docs.teradata.com/r/Teradata-MultiLoad-Reference/May-2017/Teradata-MultiLoad-Commands/IMPORT)

### Sample Source Patterns

As BTEQ content also MLoad is relocated in an `EXECUTE IMMEDIATE` block. Import transformation with
take each layout field an added to a select. Inserts in dml label will be transform to **COPY INTO**
and upserts (Update and insert) will be transform to **MERGE INTO.**

#### 1. DML label with insert

##### Teradata MLoad

```sql
-- Additional Params: -q SnowScript
.LOGTABLE my_table_log;
.LOGON my_teradata_system/username,password;

BEGIN IMPORT MLOAD TABLES my_table
WORKTABLES my_table_work
ERRORTABLES my_table_err;

.LAYOUT my_layout;
.FIELD col1 * VARCHAR(2);
.FIELD col2 * VARCHAR(5);

.dml label insert_into_my_table
  IGNORE DUPLICATE INSERT ROWS ;
INSERT INTO my_table(col1, col2) VALUES (:col1, :col2);

.IMPORT INFILE C:\USER\user\my_tr_file_1.tr
  FORMAT UNFORMAT
  LAYOUT my_layout APPLY insert_into_my_table;

.END MLOAD;
.LOGOFF;
```

##### Snowflake SQL

```sql
EXECUTE IMMEDIATE
$$
  DECLARE
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0);
  BEGIN
    -- Additional Params: -q SnowScript
    /*.LOGTABLE my_table_log;*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **

    /*.LOGON my_teradata_system/username,password;*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **

    /*BEGIN IMPORT MLOAD TABLES my_table
    WORKTABLES my_table_work*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **

    /*** SSC-EWI-0001 - UNRECOGNIZED TOKEN ON LINE '7' COLUMN '1' OF THE SOURCE CODE STARTING AT 'ERRORTABLES'. EXPECTED 'STATEMENT' GRAMMAR. LAST MATCHING TOKEN WAS 'my_table_err' ON LINE '7' COLUMN '13'. CODE '81'. ***/
    /*--ERRORTABLES my_table_err*/

    /*.LAYOUT my_layout;*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE. INFORMATION MAY BE USED IN A TRANSFORMED IMPORT CLAUSE **

    /*.dml label insert_into_my_table
      IGNORE DUPLICATE INSERT ROWS ;*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE. INFORMATION MAY BE USED IN A TRANSFORMED IMPORT CLAUSE **

    BEGIN
      CREATE OR REPLACE STAGE &{stagename};
      PUT file://C:\USER\user\my_tr_file_1.tr &{stagename};

      COPY INTO my_table (
        col1,
        col2
      )
      FROM
      (
        SELECT DISTINCT
          SUBSTRING($1, 1, 2) col1,
          SUBSTRING($1, 3, 5) col2
        FROM
          @&{stagename}/my_tr_file_1.tr
      );
    END;
    /*.END MLOAD;*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **

    /*.LOGOFF;*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **

  END
$$
```

##### 2. DML label with upsert

###### Teradata MLoad 2

```sql
-- Additional Params: -q SnowScript
.LOGTABLE my_table_log;
.LOGON my_teradata_system/username,password;

BEGIN IMPORT MLOAD TABLES my_table
WORKTABLES my_table_work
ERRORTABLES my_table_err;

.LAYOUT my_layout;
.FIELD col1 * VARCHAR(2);
.FIELD col2 * VARCHAR(5);

.dml label upsert_into_my_table;
UPDATE my_table
 SET
  col1 = :col1,
  col2 = :col2
 WHERE col2 = :col2
INSERT INTO my_table (
col1, col2)
VALUES (:col1, :col2);

.IMPORT INFILE C:\USER\user\my_tr_file_1.tr
  FORMAT UNFORMAT
  LAYOUT my_layout APPLY upsert_into_my_table;

.END MLOAD;
.LOGOFF;
```

###### Snowflake SQL 2

```sql
EXECUTE IMMEDIATE
$$
  DECLARE
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0);
  BEGIN
    -- Additional Params: -q SnowScript
    /*.LOGTABLE my_table_log;*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **

    /*.LOGON my_teradata_system/username,password;*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **

    /*BEGIN IMPORT MLOAD TABLES my_table
    WORKTABLES my_table_work*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **

    /*** SSC-EWI-0001 - UNRECOGNIZED TOKEN ON LINE '7' COLUMN '1' OF THE SOURCE CODE STARTING AT 'ERRORTABLES'. EXPECTED 'STATEMENT' GRAMMAR. LAST MATCHING TOKEN WAS 'my_table_err' ON LINE '7' COLUMN '13'. CODE '81'. ***/
    /*--ERRORTABLES my_table_err*/

    /*.LAYOUT my_layout;*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE. INFORMATION MAY BE USED IN A TRANSFORMED IMPORT CLAUSE **

    /*.dml label upsert_into_my_table;*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE. INFORMATION MAY BE USED IN A TRANSFORMED IMPORT CLAUSE **

    BEGIN
      CREATE OR REPLACE STAGE &{stagename};
      PUT file://C:\USER\user\my_tr_file_1.tr &{stagename};

      MERGE INTO my_table merge_table
      USING (
        SELECT
          SUBSTRING($1, 1, 2) col1,
          SUBSTRING($1, 3, 5) col2
        FROM
          @&{stagename}/my_tr_file_1.tr
      ) load_temp ON merge_table.col2 = load_temp.col2
      WHEN MATCHED THEN
        UPDATE SET
          merge_table.col1 = load_temp.col1,
          merge_table.col2 = load_temp.col2
      WHEN NOT MATCHED THEN
        INSERT (col1, col2)
        VALUES (load_temp.col1, load_temp.col2);
    END;
    /*.END MLOAD;*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **

    /*.LOGOFF;*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **

  END
$$
```

##### 3. Layout or DML label not found

###### Teradata MLoad 3

```sql
-- Additional Params: -q SnowScript
.LOGTABLE my_table_log;
.LOGON my_teradata_system/username,password;

BEGIN IMPORT MLOAD TABLES my_table
WORKTABLES my_table_work
ERRORTABLES my_table_err;

.LAYOUT my_layout;
.FIELD col1 * VARCHAR(2);
.FIELD col2 * VARCHAR(5);

.dml label insert_into_my_table
  IGNORE DUPLICATE INSERT ROWS ;
INSERT INTO my_table(col1, col2)VALUES (:col1, :col2);

.IMPORT INFILE C:\USER\user\my_tr_file_1.tr
  FORMAT UNFORMAT
  LAYOUT not_layout APPLY insert_into_my_table;

.IMPORT INFILE C:\USER\user\my_tr_file_1.tr
  FORMAT UNFORMAT
  LAYOUT my_layout APPLY insert_not_my_table;

.END MLOAD;
.LOGOFF;pl
```

###### Snowflake SQL 3

```sql
EXECUTE IMMEDIATE
$$
  DECLARE
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0);
  BEGIN
    -- Additional Params: -q SnowScript
    /*.LOGTABLE my_table_log;*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **

    /*.LOGON my_teradata_system/username,password;*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **

    /*BEGIN IMPORT MLOAD TABLES my_table
    WORKTABLES my_table_work*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **

    /*** SSC-EWI-0001 - UNRECOGNIZED TOKEN ON LINE '7' COLUMN '1' OF THE SOURCE CODE STARTING AT 'ERRORTABLES'. EXPECTED 'STATEMENT' GRAMMAR. LAST MATCHING TOKEN WAS 'my_table_err' ON LINE '7' COLUMN '13'. CODE '81'. ***/
    /*--ERRORTABLES my_table_err*/

    /*.LAYOUT my_layout;*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE. INFORMATION MAY BE USED IN A TRANSFORMED IMPORT CLAUSE **

    /*.dml label insert_into_my_table
      IGNORE DUPLICATE INSERT ROWS ;*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE. INFORMATION MAY BE USED IN A TRANSFORMED IMPORT CLAUSE **

--      .IMPORT INFILE C:\USER\user\my_tr_file_1.tr FORMAT UNFORMAT LAYOUT not_layout APPLY insert_into_my_table
                                                                                                              ;
    BEGIN
      CREATE OR REPLACE STAGE &{stagename};
      PUT file://C:\USER\user\my_tr_file_1.tr &{stagename};

    END;
    /*.END MLOAD;*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **

    /*.LOGOFF;*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **

    /*** SSC-EWI-0001 - UNRECOGNIZED TOKEN ON LINE '26' COLUMN '9' OF THE SOURCE CODE STARTING AT 'pl'. EXPECTED 'STATEMENT' GRAMMAR. LAST MATCHING TOKEN WAS 'pl' ON LINE '26' COLUMN '9'. CODE '81'. ***/
    /*--pl*/

  END
$$
```

##### 4. Conditions not found in update statement

###### Teradata MLoad 4

```sql
-- Additional Params: -q SnowScript
.LOGTABLE my_table_log;
.LOGON my_teradata_system/username,password;

BEGIN IMPORT MLOAD TABLES my_table
WORKTABLES my_table_work
ERRORTABLES my_table_err;

.LAYOUT my_layout;
.FIELD col1 * VARCHAR(2);
.FIELD col2 * VARCHAR(5);

.dml label upsert_into_my_table;
UPDATE my_table
 SET
  col1 = :col1,
  col2 = :col2
INSERT INTO my_table (
col1, col2)
VALUES (:col1, :col2);

.IMPORT INFILE C:\USER\user\my_tr_file_1.tr
  FORMAT UNFORMAT
  LAYOUT my_layout APPLY upsert_into_my_table;

.END MLOAD;
.LOGOFF;
```

###### Snowflake SQL 4

```sql
EXECUTE IMMEDIATE
$$
  DECLARE
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0);
  BEGIN
    -- Additional Params: -q SnowScript
    /*.LOGTABLE my_table_log;*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **

    /*.LOGON my_teradata_system/username,password;*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **

    /*BEGIN IMPORT MLOAD TABLES my_table
    WORKTABLES my_table_work*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **

    /*** SSC-EWI-0001 - UNRECOGNIZED TOKEN ON LINE '7' COLUMN '1' OF THE SOURCE CODE STARTING AT 'ERRORTABLES'. EXPECTED 'STATEMENT' GRAMMAR. LAST MATCHING TOKEN WAS 'my_table_err' ON LINE '7' COLUMN '13'. CODE '81'. ***/
    /*--ERRORTABLES my_table_err*/

    /*.LAYOUT my_layout;*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE. INFORMATION MAY BE USED IN A TRANSFORMED IMPORT CLAUSE **

    /*.dml label upsert_into_my_table;*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE. INFORMATION MAY BE USED IN A TRANSFORMED IMPORT CLAUSE **

--      .IMPORT INFILE C:\USER\user\my_tr_file_1.tr FORMAT UNFORMAT LAYOUT my_layout APPLY upsert_into_my_table
                                                                                                             ;
    /*.END MLOAD;*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **

    /*.LOGOFF;*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **

  END
$$
```

### Known Issues

Some statements from import clause where not supported yet:

- AXSMOD statement
- INMODE statement
- FORMAT (only FORMAT UNFORMAT is supported)
- WHERE condition of APPLY label

### Related EWIS

1. [SSC-EWI-0001](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0001):
   Unrecognized token on the line of the source code.
2. [SSC-FDM-0027](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0027):
   Removed next statement, not applicable in SnowFlake.
