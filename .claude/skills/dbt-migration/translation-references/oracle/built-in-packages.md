---
description: Translation reference for Built-in packages.
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/oracle/built-in-packages
title: SnowConvert AI - Oracle - Built-In packages | Snowflake Documentation
---

## Description[¶](#description)

> Oracle supplies many PL/SQL packages with the Oracle server to extend database functionality and
> provide PL/SQL access to SQL features.
> ([Oracle PL/SQL Built-in Packages](https://docs.oracle.com/en/database/oracle/oracle-database/21/arpls/introduction-to-oracle-supplied-plsql-packages-and-types.html#GUID-4AA6AA30-CAEE-4DCD-B214-9AD51D0229B4))

## DBMS_OUTPUT[¶](#dbms-output)

### Description[¶](#id1)

> The `DBMS_OUTPUT` package is especially useful for displaying PL/SQL debugging information.
> ([Oracle PL/SQL DBMS_OUTPUT](https://docs.oracle.com/en/database/oracle/oracle-database/21/arpls/DBMS_OUTPUT.html#GUID-C1400094-18D5-4F36-A2C9-D28B0E12FD8C))

### PUT_LINE procedure[¶](#put-line-procedure)

Translation reference for DBMS_OUTPUT.PUT_LINE.

#### Description[¶](#id2)

> This procedure places a line in the buffer.
> ([Oracle PL/SQL DBMSOUTPUT.PUT_LINE](https://docs.oracle.com/en/database/oracle/oracle-database/21/arpls/DBMS_OUTPUT.html#GUID-19FA480D-591E-4584-9650-5D37C4AFA530))

This UDF is implemented using a temporary table to insert the data to be displayed to replicate the
functionality of Oracle `DBMS_OUTPUT.PUT_LINE` function.

#### Syntax[¶](#syntax)

```
 DBMS_OUTPUT.PUT_LINE(LOG VARCHAR);
```

#### Custom procedure[¶](#custom-procedure)

##### Setup data[¶](#setup-data)

The `DBMS_OUTPUT` schema must be created.

```
CREATE SCHEMA IF NOT EXISTS DBMS_OUTPUT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}';
```

##### DBMS_OUTPUT.PUT_LINE(VARCHAR)[¶](#dbms-output-put-line-varchar)

##### **Parameters**[¶](#parameters)

- **LOG**: Item in a buffer that you want to display.

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

**Note:**

- Note that this is using a temporary table, if you want the data to persist after a session ends,
  please remove TEMPORARY from the CREATE TABLE.
- The
  [temporary tables](https://docs.snowflake.com/en/user-guide/tables-temp-transient.html#temporary-tables)
  store non-permanent transitory data. They only exist within the session in which they were created
  and persist only for the rest of the session. After the session ends, the data stored in the table
  is completely removed from the system and is therefore not recoverable, either by the user who
  created the table or by Snowflake.

Warning

If you do not use the temporary table, keep in mind that you may need another column in the table
where the USER running DBMS_OUTPUT.PUT_LINE UDF is inserted to avoid confusion.

##### Usage example[¶](#usage-example)

###### Oracle[¶](#oracle)

```
CREATE OR REPLACE PROCEDURE PROC
IS
BEGIN
    DBMS_OUTPUT.PUT_LINE('Test');
END;

CALL PROC();
```

###### Result[¶](#result)

```
<!-- prettier-ignore -->
|DBMS_OUTPUT.PUT_LINE('test')|
|---|
|test|
```

###### Snowflake[¶](#snowflake)

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

###### Result[¶](#id3)

```
<!-- prettier-ignore -->
|ROW|WHEN|DATABASE|LOG|
|---|---|---|---|
|1|2022-04-25 11:16:23.844|CODETEST|test|
```

#### Known Issues[¶](#known-issues)

- The UDF code will remain commented out because it can affect performance, if the user decides to
  use it, they just need to uncomment the code.
- The user can modify the UDF so that the necessary information is inserted into the
  DBMS_OUTPUT.PUT_LINE table.

#### Related EWIs[¶](#related-ewis)

1. [SSC-FDM-OR0035](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM.html#ssc-fdm-or0035):
   Check UDF implementation for DBMS_OUTPUT.PUT_LINE_UDF.

## DBMS_LOB[¶](#dbms-lob)

### Description[¶](#id4)

> The `DBMS_LOB` package provides subprograms to operate on `BLOBs`, `CLOBs`, `NCLOBs`, `BFILEs`,
> and temporary `LOBs`. You can use `DBMS_LOB` to access and manipulate specific parts of a LOB or
> complete LOBs.
> ([Oracle PL/SQL DBMS_LOB](https://docs.oracle.com/en/database/oracle/oracle-database/21/arpls/DBMS_LOB.html#GUID-A35DE03B-41A6-4E55-8CDE-77737FED9306))

### SUBSTR Function[¶](#substr-function)

Translation reference for DBMS_RANDOM.SUBSTR.

#### Description[¶](#id5)

> This function returns `amount` bytes or characters of a LOB, starting from an absolute `offset`
> from the beginning of the LOB.
> ([Oracle PL/SQL DBMS_LOB.SUBSTR](https://docs.oracle.com/en/database/oracle/oracle-database/21/arpls/DBMS_LOB.html))

This built-in function is replaced with Snowflake
[SUBSTR function](https://docs.snowflake.com/en/sql-reference/functions/substr.html#substr-substring).
However, there are some differences.

**Note:**

The **amount** and **offset** parameters are inverted in Snowflake

#### Syntax[¶](#id6)

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

#### Function overloads[¶](#function-overloads)

**DBMS_LOB.SUBSTR(‘string’, amount, offset)**

##### Usage example[¶](#id7)

###### Oracle[¶](#id8)

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

###### Result[¶](#id9)

```
1              |2   |3            |4    |5   |6|
---------------+----+-------------+-----+----+-+
some magic here|some|me magic here|magic|here| |
```

###### Snowflake[¶](#id10)

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

###### Result[¶](#id11)

```
1              |2   |3            |4    |5   |6|
---------------+----+-------------+-----+----+-+
some magic here|some|me magic here|magic|here| |
```

##### DBMS_LOB.SUBSTR(**B**LOB, amount, offset)[¶](#dbms-lob-substr-blob-amount-offset)

###### Usage example[¶](#id12)

Warning

Result values in Oracle and Snowflake are being converted from bytes to strings for easier
understanding of the function.

For **Snowflake** consider using:

**hex_decode_string( to_varchar(SUBSTR(blob_column, 1, 6), ‘HEX’));**

and for **Oracle** consider using:

**utl_raw.cast_to_varchar2(DBMS_LOB.SUBSTR(blob_column, 1, 6));**

to obtain the result as a string.

###### Oracle[¶](#id13)

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

###### Result[¶](#id14)

```
1              |2   |3            |4    |5   |6|
---------------+----+-------------+-----+----+-+
some magic here|some|me magic here|magic|here| |
```

###### Snowflake[¶](#id15)

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

###### Result[¶](#id16)

```
1              |2   |3            |4    |5   |6|
---------------+----+-------------+-----+----+-+
some magic here|some|me magic here|magic|here| |
```

Warning

**Note:** `UTL_RAW.CAST_TO_RAW()` is currently not being transformed to `TO_BINARY()`. The function
is used to show the functional equivalence of the example.

##### DBMS_LOB.SUBSTR(CLOB, amount, offset)[¶](#dbms-lob-substr-clob-amount-offset)

###### Usage example[¶](#id17)

###### Oracle[¶](#id18)

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

###### Result[¶](#id19)

```
1              |2   |3            |4    |5   |6|
---------------+----+-------------+-----+----+-+
some magic here|some|me magic here|magic|here| |
```

###### Snowflake[¶](#id20)

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

###### Result[¶](#id21)

```
1              |2   |3            |4    |5   |6|
---------------+----+-------------+-----+----+-+
some magic here|some|me magic here|magic|here| |
```

Warning

**Note:** `UTL_RAW.CAST_TO_RAW()` is currently not being transformed to `TO_BINARY()`. The function
is used to show the functional equivalence of the example.

##### DBMS_LOB.SUBSTR(BFILE, amount, offset)[¶](#dbms-lob-substr-bfile-amount-offset)

###### Usage example[¶](#id22)

Using DBMS_LOB.SUBSTR() on a BFILE column returns a substring of the file content.

Warning

Next example is **not** a current migration, but a functional example to show the differences of the
SUBSTR function on BFILE types.

**File Content (file.txt):**

```
some magic here
```

###### Oracle[¶](#id23)

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

###### Console Log[¶](#console-log)

```
DBMS_OUTPUT.PUT_LINE(UTL_RAW.CAST_TO_VARCHAR2(DBMS_LOB.SUBSTR(fil,4,1))) |
-------------------------------------------------------------------------|
some magi                                                                |
```

###### Snowflake[¶](#id24)

**BFILE** columns are translated into **VARCHAR** columns, therefore applying a `SUBSTR` function on
the same column would return a substring of the file name, not the file content.

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

###### Result[¶](#id25)

<!-- prettier-ignore -->
|SUBSTR(bfile_column, 1, 9)|
|---|
|MY_DIR\fi|

#### Known Issues[¶](#id26)

##### 1. Using DBMS_LOB.SUBSTR with BFILE columns[¶](#using-dbms-lob-substr-with-bfile-columns)

The current transformation for BFILE datatypes in columns is VARCHAR, where the name of the file is
stored as a string. Therefore applying the SUBSTR function on a BFILE column after transformation
will return a substring of the file name, while Oracle would return a substring of the file content.

#### Related EWIs[¶](#id27)

1. [SSC-EWI-OR0076](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI.html#ssc-ewi-or0076):
   Built In Package Not Supported.
2. [SSC-FDM-OR0035](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM.html#ssc-fdm-or0035):
   DBMS_OUTPUT.PUTLINE check UDF implementation.

## UTL_FILE[¶](#utl-file)

### Description[¶](#id28)

> With `UTL_FILE` package, PL/SQL programs can read and write text files.
> ([Oracle PL/SQL UTL_FILE](https://docs.oracle.com/en/database/oracle/oracle-database/21/arpls/UTL_FILE.html#GUID-EBC42A36-EB72-4AA1-B75F-8CF4BC6E29B4))

### FCLOSE procedure[¶](#fclose-procedure)

Translation reference for UTL_FILE.FCLOSE.

#### Description[¶](#id29)

> This procedure closes an open file identified by a file handle.
> ([Oracle PL/SQL UTL_FILE.FCLOSE](https://docs.oracle.com/en/database/oracle/oracle-database/21/arpls/UTL_FILE.html#GUID-68874564-1A2C-4071-8D48-60539C805E0D))

This procedure is implemented using Snowflake
[STAGE](https://docs.snowflake.com/en/sql-reference/sql/create-stage.html) to store the written text
files.

**Note:**

This procedure requires to be used in conjunction with:

- [`UTL_FILE.FOPEN`](#fopen-procedure) procedure

#### Syntax[¶](#id30)

```
UTL_FILE.FCLOSE(
    FILE VARCHAR
    );
```

#### Setup data[¶](#id31)

- The `UTL_FILE` schema must be created.

```
CREATE SCHEMA IF NOT EXISTS UTL_FILE
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}';
```

- If you want to download the file, run the following command.

```
GET @UTL_FILE.utlfile_local_directory/<filename> file://<path_to_file>/<filename>;
```

Warning

- The [GET](https://docs.snowflake.com/en/sql-reference/sql/get.html) command runs in
  [Snowflake CLI](https://docs.snowflake.com/en/user-guide/snowsql-install-config.html).

#### Custom procedure overloads[¶](#custom-procedure-overloads)

##### UTL_FILE.FCLOSE(VARCHAR)[¶](#utl-file-fclose-varchar)

###### **Parameters**[¶](#id32)

- **FILE**: Active file handler returned from the call to [`UTL_FILE.FOPEN`](#fopen-procedure)

###### Functionality[¶](#functionality)

This procedure uses the `FOPEN_TABLES_LINES` table created in the
[`UTL_FILE.FOPEN`](#fopen-procedure) procedure.

This procedure writes to the utlfile_local_directory stage all lines with the same `FHANDLE` from
the file in `FOPEN_TABLES_LINES`.

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

**Note:**

- Note that this procedure uses the **stage** that was created previously. For now, if you want to
  write the file in another stage, you must modify the name.
- These procedures are implemented for the internal stages in the
  [`COPY INTO`](https://docs.snowflake.com/en/sql-reference/sql/copy-into-location.html)

##### Usage example[¶](#id33)

###### Oracle[¶](#id34)

```
DECLARE
    w_file UTL_FILE.FILE_TYPE;
BEGIN
    w_file:= UTL_FILE.FOPEN('MY_DIR','test.csv','w',1024);
    UTL_FILE.PUT_LINE(w_file,'New line');
    UTL_FILE.FCLOSE(w_file);
END;
```

Warning

To run this example, see
[`ORACLE UTL_FILE`](https://docs.oracle.com/en/database/oracle/oracle-database/21/arpls/UTL_FILE.html#GUID-FA16A38B-26AA-4002-9BE0-7D3950557F8C)

###### Snowflake[¶](#id35)

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

#### Known Issues[¶](#id36)

##### 1. **Modify the procedure for changing the name of the stage.**[¶](#modify-the-procedure-for-changing-the-name-of-the-stage)

The user can modify the procedure if it is necessary to change the name of the stage.

##### 2. Location **static.**[¶](#location-static)

The location used to write to this procedure is static. A new version of the procedure is expected
to increase its extensibility by using the location that has the `FILE` parameter.

##### 5. Files supported.[¶](#files-supported)

This procedure for now, only writes .CSV files.

#### Related EWIs[¶](#id37)

1. [SSC-FDM-0015](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0015):
   Data Type Not Recognized.
2. [SSC-FDM-OR0036](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM.html#ssc-fdm-or0036):
   Unnecessary built-in packages parameters.

### FOPEN procedure[¶](#fopen-procedure)

Translation reference for UTL_FILE.FOPEN.

#### Description[¶](#id38)

> This procedure opens a file.
> ([Oracle PL/SQL UTL_FILE.FOPEN](https://docs.oracle.com/en/database/oracle/oracle-database/21/arpls/UTL_FILE.html#GUID-DF14ADC3-983D-4E0F-BE2C-60733FF58539))

This procedure is implemented using Snowflake
[STAGE](https://docs.snowflake.com/en/sql-reference/sql/create-stage.html) to store the text files.

The user is in charge of uploading the local files to the
[STAGE](https://docs.snowflake.com/en/sql-reference/sql/create-stage.html) to be used by the
procedure.

**Note:**

This procedure requires to be used in conjunction with:

- [`UTL_FILE.FCLOSE`](#fclose-procedure) procedure

#### Syntax[¶](#id39)

```
UTL_FILE.FOPEN(
    LOCATION VARCHAR,
    FILENAME VARCHAR,
    OPEN_MODE VARCHAR,
    MAX_LINESIZE NUMBER,
    );
```

#### Setup data[¶](#id40)

- The `UTL_FILE` schema must be created.

```
CREATE SCHEMA IF NOT EXISTS UTL_FILE
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}';
```

- Create the stage `utlfile_local_directory`.

```
CREATE OR REPLACE FILE FORMAT  my_csv_format TYPE = csv;

CREATE OR REPLACE STAGE utlfile_local_directory
  file_format = my_csv_format;
```

- If the value in the `OPEN_MODE` parameter is **w** or **r** it is necessary to upload the file in
  the `utlfile_local_directory`.

```
PUT file://<path_to_file>/<filename> @UTL_FILE.utlfile_local_directory auto_compress=false;
```

Warning

- The [PUT](https://docs.snowflake.com/en/sql-reference/sql/put.html) command runs in
  [Snowflake CLI](https://docs.snowflake.com/en/user-guide/snowsql-install-config.html).

#### Custom procedure overloads[¶](#id41)

##### UTL_FILE.FOPEN( VARCHAR, VARCHAR)[¶](#utl-file-fopen-varchar-varchar)

###### **Parameters**[¶](#id42)

- **FILENAME:** The name of the file, including extension\*\*.\*\*
- **OPEN_MODE:** Specifies how the file is opened.

###### **Open modes**[¶](#open-modes)

The Oracle Built-in package
[`UTL_FILE.FOPEN`](https://docs.oracle.com/en/database/oracle/oracle-database/21/arpls/UTL_FILE.html#GUID-DF14ADC3-983D-4E0F-BE2C-60733FF58539)
procedure supports six modes of how to open the file, but only three of them are supported in the
Snowscripting procedure.

<!-- prettier-ignore -->
|OPEN_MODE|DESCRIPTION|STATUS|
|---|---|---|
|w|Write mode|Supported|
|a|Append mode|Supported|
|r|Read mode|Supported|
|rb|Read byte mode|Unsupported|
|wb|Write byte mode|Unsupported|
|ab|Append byte mode|Unsupported|

###### Functionality[¶](#id43)

This procedure uses two tables with which the operation of opening a file will be emulated. The
`FOPEN_TABLES` table will store the files that are open and the `FOPEN_TABLES_LINES` table stores
the lines that each file owns.

If the file is opened in write mode, a new file is created, if it is opened in read or append mode,
it loads the lines of the file in `FOPEN_TABLES_LINES` and inserts the file in `FOPEN_TABLES`.

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

**Note:**

- Note that this procedure uses the **stage** that was created previously. For now, if you want to
  use another name for the stage, you must modify the procedure.
- These procedures are implemented for the internal stages in the
  [`COPY INTO`](https://docs.snowflake.com/en/sql-reference/sql/copy-into-table.html)

##### Usage example[¶](#id44)

###### Oracle[¶](#id45)

```
DECLARE
    w_file UTL_FILE.FILE_TYPE;
BEGIN
    w_file:= UTL_FILE.FOPEN('MY_DIR','test.csv','w',1024);
END;
```

Warning

To run this example, see
[`ORACLE UTL_FILE`](https://docs.oracle.com/en/database/oracle/oracle-database/21/arpls/UTL_FILE.html#GUID-FA16A38B-26AA-4002-9BE0-7D3950557F8C)

###### Snowflake[¶](#id46)

```
DECLARE
    w_file OBJECT /*** SSC-FDM-0015 - REFERENCED CUSTOM TYPE 'UTL_FILE.FILE_TYPE' IN QUERY NOT FOUND, USAGES MAY BE AFFECTED ***/ := OBJECT_CONSTRUCT();
BEGIN
    w_file:=
    --** SSC-FDM-OR0036 - PARAMETERS: 'LOCATION, MAX_LINESIZE_UDF' UNNECESSARY IN THE IMPLEMENTATION. **
    UTL_FILE.FOPEN_UDF('MY_DIR','test.csv','w',1024);
END;
```

#### Known Issues[¶](#id47)

##### 1. **Modify the procedure for changing the name of the stage.**[¶](#id48)

The user can modify the procedure if it is necessary to change the name of the stage.

##### 2. **`LOCATION` parameter is not used.**[¶](#location-parameter-is-not-used)

The `LOCATION` parameter is not used now because the stage used in the procedure is static. It is
planned for an updated version of the procedure to increase its extensibility by using this
parameter to enter the name of the stage where the file you want to open is located.

##### 3. `MAX_LINESIZE` parameter is not used.[¶](#max-linesize-parameter-is-not-used)

The Oracle Built-in package
[`UTL_FILE.FOPEN`](https://docs.oracle.com/en/database/oracle/oracle-database/21/arpls/UTL_FILE.html#GUID-DF14ADC3-983D-4E0F-BE2C-60733FF58539)
procedure has the `MAX_LINESIZE` parameter, but in the Snowscripting procedure it is removed because
it is not used.

##### 4. `OPEN_MODE` values supported.[¶](#open-mode-values-supported)

This procedure supports _write_ (**w**), _read_ (**r**), and _append_ (**a**) modes to open files.

##### 5. Files supported.[¶](#id49)

This procedure for now, only supports .CSV files.

#### Related EWIs[¶](#id50)

1. [SSC-FDM-0015](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0015):
   Data Type Not Recognized.
2. [SSC-FDM-OR0036](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM.html#ssc-fdm-or0036):
   UnnecessaryBuiltInPackagesParameters

### PUT_LINE procedure[¶](#id51)

Translation reference for UTL_FILE.PUT_LINE.

#### Description[¶](#id52)

> This procedure writes the text string stored in the buffer parameter to the open file identified
> by the file handle.
> ([Oracle PL/SQL UTL_FILE.PUT_LINE](https://docs.oracle.com/en/database/oracle/oracle-database/21/arpls/UTL_FILE.html#GUID-BC046363-6F14-4128-B4D2-836DDBDB9B48))

#### Syntax[¶](#id53)

```
UTL_FILE.PUT_LINE(
    FILE VARCHAR,
    BUFFER VARCHAR,
    );
```

#### Setup data[¶](#id54)

- The `UTL_FILE` schema must be created.

```
CREATE SCHEMA IF NOT EXISTS UTL_FILE
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}';
```

#### Custom UDF[¶](#custom-udf)

##### UTL_FILE.PUT_LINE(VARCHAR, VARCHAR)[¶](#utl-file-put-line-varchar-varchar)

###### **Parameters**[¶](#id55)

- **FILE**: Active file handler returned from the call to [`UTL_FILE.FOPEN`](#fopen-procedure)
- **BUFFER:** Text buffer that contains the text to be written to the file\*\*.\*\*

###### Functionality[¶](#id56)

This procedure uses the `FOPEN_TABLES_LINES` table created in the
[`UTL_FILE.FOPEN`](#fopen-procedure) procedure.

If the `OPEN_MODE` of the file is _write_ (**w**) or _append_ (**a**), it inserts the buffer into
`FOPEN_TABLES_LINES`, but if the `OPEN_MODE` is read (**r**), it throws the `File_is_read_only`
exception.

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

Warning

**Note:**

- To use this procedure you must open the file with [UTL_FILE.FOPEN](#fopen-procedure)

##### Usage example[¶](#id57)

###### Oracle[¶](#id58)

```
DECLARE
    w_file UTL_FILE.FILE_TYPE;
BEGIN
    w_file:= UTL_FILE.FOPEN('MY_DIR','test.csv','w',1024);
    UTL_FILE.PUT_LINE(w_file,'New line');
END;
```

Warning

To run this example, see
[`ORACLE UTL_FILE`](https://docs.oracle.com/en/database/oracle/oracle-database/21/arpls/UTL_FILE.html#GUID-FA16A38B-26AA-4002-9BE0-7D3950557F8C)

###### Snowflake[¶](#id59)

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

#### Known Issues[¶](#id60)

##### 1. `AUTOFLUSH` parameter is not used.[¶](#autoflush-parameter-is-not-used)

The Oracle Built-in package
[`UTL_FILE.PUT_LINE`](https://docs.oracle.com/en/database/oracle/oracle-database/21/arpls/UTL_FILE.html#GUID-BC046363-6F14-4128-B4D2-836DDBDB9B48)
procedure has the `AUTOFLUSH` parameter, but in the Snowscripting procedure it is removed because it
is not used.

#### Related EWIs[¶](#id61)

1. [SSC-FDM-0015](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0015):
   Data Type Not Recognized.
2. [SSC-FDM-OR0036](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM.html#ssc-fdm-or0036):
   Unnecessary built-in packages parameters.

## DBMS_RANDOM[¶](#dbms-random)

### Description[¶](#id62)

> The `DBMS_RANDOM` package provides a built-in random number generator. `DBMS_RANDOM` is not
> intended for cryptography.
> ([Oracle PL/SQL DBMS_RANDOM](https://docs.oracle.com/en/database/oracle/oracle-database/21/arpls/DBMS_RANDOM.html#GUID-8DC48B0C-3707-4172-A306-C0308DD2EB0F))

### VALUE functions[¶](#value-functions)

Translation reference for DBMS_RANDOM.VALUE.

#### Description[¶](#id63)

> The basic function gets a random number, greater than or equal to 0 and less than 1.
> Alternatively, you can get a random Oracle number **`X`**, where **`X`** is greater than or equal
> to `low` and less than `high`.
> ([Oracle PL/SQL DBMS_RANDOM.VALUE](https://docs.oracle.com/en/database/oracle/oracle-database/21/arpls/DBMS_RANDOM.html#GUID-AAD9E936-D74F-440D-9E16-24F3F0DE8D31))

This UDF is implemented using the
[Math.random](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/random)
function of Javascript to replicate the functionality of Oracle DBMS_RANDOM.VALUE function.

#### Syntax[¶](#id64)

```
DBMS_RANDOM.VALUE()
    RETURN NUMBER;

DBMS_RANDOM.VALUE(
    low NUMBER,
    high NUMBER)
    RETURN NUMBER;
```

#### Custom UDF overloads[¶](#custom-udf-overloads)

##### Setup data[¶](#id65)

The `DBMS_RANDOM` schema must be created.

```
CREATE SCHEMA IF NOT EXISTS DBMS_RANDOM
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}';
```

##### DBMS_RANDOM.VALUE()[¶](#dbms-random-value)

###### **Parameters**[¶](#id66)

- No parameters.

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

**Note:**

**Note:** The UDF only supports approximately between 9 and 10 digits in the decimal part of the
number (9 or 10 digits of precision)

##### Usage example[¶](#id67)

###### Oracle[¶](#id68)

```
SELECT DBMS_RANDOM.VALUE() FROM DUAL;
```

###### Result[¶](#id69)

```
<!-- prettier-ignore -->
|DBMS_RANDOM.VALUE()|
|---|
|0.47337471168356406022193430290380483126|
```

**Note:**

The function can be called either\_`DBMS_RANDOM.VALUE()`\_ or _`DBMS_RANDOM.VALUE.`_

###### Snowflake[¶](#id70)

```
SELECT
--** SSC-FDM-OR0033 - DBMS_RANDOM.VALUE DIGITS OF PRECISION ARE LOWER IN SNOWFLAKE **
DBMS_RANDOM.VALUE_UDF() FROM DUAL;
```

###### Result[¶](#id71)

```
<!-- prettier-ignore -->
|DBMS_RANDOM.VALUE()|
|---|
|0.1014560867|
```

**Note:**

In Snowflake, you must put the parentheses.

**DBMS_RANDOM.VALUE(NUMBER, NUMBER)**

###### **Parameters**[¶](#id72)

- **low**: The lowest `NUMBER` from which a random number is generated. The number generated is
  greater than or equal to `low`.
- **high**: The highest `NUMBER` used as a limit when generating a random number. The number
  generated will be less than `high`.

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

**Note:**

- The Oracle DBMS_RANDOM.VALUE(low, high) function does not require parameters to have a specific
  order so the Snowflake UDF is implemented to support this feature by always taking out the highest
  and lowest number.
- The UDF only supports approximately between 9 and 10 digits in the decimal part of the number (9
  or 10 digits of precision).

##### Usage example[¶](#id73)

###### Oracle[¶](#id74)

```
SELECT DBMS_RANDOM.VALUE(-10,30) FROM DUAL;
```

###### Result[¶](#id75)

```
<!-- prettier-ignore -->
|DBMS_RANDOM.VALUE(-10,30)|
|---|
|16.0298681859960167648070354679783928085|
```

###### Snowflake[¶](#id76)

```
SELECT
--** SSC-FDM-OR0033 - DBMS_RANDOM.VALUE DIGITS OF PRECISION ARE LOWER IN SNOWFLAKE **
DBMS_RANDOM.VALUE_UDF(-10,30) FROM DUAL;
```

###### Result[¶](#id77)

```
<!-- prettier-ignore -->
|DBMS_RANDOM.VALUE(-10,30)|
|---|
|-6.346055187|
```

#### Known Issues[¶](#id78)

No issues were found.

#### Related EWIs[¶](#id79)

1. [SSC-FDM-OR0033](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM.html#ssc-fdm-or0033):
   DBMS_RANDOM.VALUE Built-In Package precision is lower in Snowflake.
