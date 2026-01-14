---
description:
  Each row in the database has an address. (Oracle SQL Language Reference Rowid Data Types)
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/oracle/basic-elements-of-oracle-sql/data-types/rowid-types
title: SnowConvert AI - Oracle - Rowid Data Type | Snowflake Documentation
---

## Description[¶](#description)

> Each row in the database has an address.
> ([Oracle SQL Language Reference Rowid Data Types](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/Data-Types.html#GUID-4231B94A-97E9-4B59-91EB-E7B2D0DA438C))

## ROWID DataType[¶](#rowid-datatype)

### Description[¶](#id1)

> The rows in heap-organized tables that are native to Oracle Database have row addresses called
> rowids. You can examine a rowid row address by querying the pseudocolumn ROWID. Values of this
> pseudocolumn are strings representing the address of each row. These strings have the data type
> ROWID. You can also create tables and clusters that contain actual columns having the ROWID data
> type.
> ([Oracle SQL Language Reference ROWID Data Types](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/Data-Types.html#GUID-AEF1FE4C-2DE5-4BE7-BB53-83AD8F1E34EF))

```
ROWID
```

### Sample Source Patterns[¶](#sample-source-patterns)

#### ROWID in Create Table[¶](#rowid-in-create-table)

##### Oracle[¶](#oracle)

```
CREATE TABLE rowid_table
(
    rowid_column ROWID
);
```

##### Snowflake[¶](#snowflake)

```
CREATE OR REPLACE TABLE rowid_table
    (
        rowid_column VARCHAR(18) !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - ROWID DATA TYPE CONVERTED TO VARCHAR ***/!!!
    )
    COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
    ;
```

#### Insert data in the ROWID column[¶](#insert-data-in-the-rowid-column)

It is possible to insert data in ROWID columns if the insert has a valid ROWID, as shown in the
example below. Unfortunately retrieving ROWID from a table is not allowed.

##### Oracle[¶](#id2)

```
INSERT INTO rowid_table VALUES ('AAATtCAAMAAAADLABD');

SELECT rowid_column FROM rowid_table;
```

##### Result[¶](#result)

<!-- prettier-ignore -->
|ROWID_COLUMN|
|---|
|AAATtCAAMAAAADLABD|

##### Snowflake[¶](#id3)

```
INSERT INTO rowid_table
VALUES ('AAATtCAAMAAAADLABD');

SELECT rowid_column FROM
rowid_table;
```

##### Result[¶](#id4)

<!-- prettier-ignore -->
|ROWID_COLUMN|
|---|
|AAATtCAAMAAAADLABD|

### Known Issues[¶](#known-issues)

**Note:**

Since the result set is too large, _Row Limiting Clause_ was added. You can remove this clause to
retrieve the entire result set.

**1. Retrieving ROWID from a table that does not have an explicit column with this data type**

As mentioned in the
[Snowflake forum](https://community.snowflake.com/s/question/0D50Z00007jUWEU/how-to-convert-oracle-rowids-to-snowflake-sql),
ROWID is not supported by Snowflake. The following query displays an error in Snowflake since
hr.employees do not contain a ROWID column.

#### Oracle[¶](#id5)

```
SELECT
    ROWID
FROM
    hr.employees
FETCH NEXT 10 ROWS ONLY;
```

##### Result[¶](#id6)

<!-- prettier-ignore -->
|ROWID|
|---|
|AAATtCAAMAAAADLABD|
|AAATtCAAMAAAADLABV|
|AAATtCAAMAAAADLABX|
|AAATtCAAMAAAADLAAv|
|AAATtCAAMAAAADLAAV|
|AAATtCAAMAAAADLAAD|
|AAATtCAAMAAAADLABL|
|AAATtCAAMAAAADLAAP|
|AAATtCAAMAAAADLAA6|
|AAATtCAAMAAAADLABg|

##### Snowflake[¶](#id7)

```
SELECT
    --** SSC-FDM-OR0030 - ROWID PSEUDOCOLUMN IS NOT SUPPORTED IN SNOWFLAKE, IT WAS CONVERTED TO NULL TO AVOID RUNTIME ERRORS **
    '' AS ROWID
FROM
    hr.employees
FETCH NEXT 10 ROWS ONLY;
```

##### Result[¶](#id8)

Danger

SQL compilation error: invalid identifier ‘ROWID’

### Related EWIs[¶](#related-ewis)

1. [SSC-EWI-0036](../../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0036):
   Data type converted to another data type.
2. [SSC-FDM-OR0030](../../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM.html#ssc-fdm-or0030):
   ROWID pseudocolumn is not supported in Snowflake.

## UROWID Data Type[¶](#urowid-data-type)

### Description[¶](#id9)

> Oracle uses universal rowids (urowids) to store the addresses of index-organized and foreign
> tables. Index-organized tables have logical urowids and foreign tables have foreign
> urowids.([Oracle SQL Language Reference UROWID Data Type](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/Data-Types.html#GUID-E9F3AE1C-AA6D-4262-A15F-778833251361))

```
UROWID [(size)]
```

### Sample Source Patterns[¶](#id10)

#### UROWID in Create Table[¶](#urowid-in-create-table)

##### Oracle[¶](#id11)

```
CREATE TABLE urowid_table
(
    urowid_column UROWID,
    urowid_sized_column UROWID(40)
);
```

##### Snowflake[¶](#id12)

```
CREATE OR REPLACE TABLE urowid_table
    (
        urowid_column VARCHAR(18) !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - UROWID DATA TYPE CONVERTED TO VARCHAR ***/!!!,
        urowid_sized_column VARCHAR(18) !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - UROWID DATA TYPE CONVERTED TO VARCHAR ***/!!!
    )
    COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
    ;
```

#### Insert data in the UROWID column[¶](#insert-data-in-the-urowid-column)

Just like [ROWID](#rowid-datatype), it is possible to insert data in UROWID columns if the insert
has a valid UROWID, but retrieving from a table is not allowed.

##### Oracle[¶](#id13)

```
INSERT INTO urowid_table VALUES ('*BAMAAJMCVUv+','*BAMAAJMCVUv+');

SELECT * FROM urowid_table;
```

##### Result[¶](#id14)

<!-- prettier-ignore -->
|UROWID_COLUMN|UROWID_SIZED_COLUMN|
|---|---|
|\*BAMAAJMCVUv+|\*BAMAAJMCVUv+|

##### Snowflake\*\* SSC-FDM-0007 - MISSING DEPENDENT OBJECT “urowid_table” \*\*[¶](#snowflake-ssc-fdm-0007-missing-dependent-object-urowid-table)

```
INSERT INTO urowid_table
VALUES ('*BAMAAJMCVUv+','*BAMAAJMCVUv+');

SELECT * FROM
urowid_table;
```

##### Result[¶](#id15)

<!-- prettier-ignore -->
|UROWID_COLUMN|UROWID_SIZED_COLUMN|
|---|---|
|\*BAMAAJMCVUv+|\*BAMAAJMCVUv+|

### Known Issues[¶](#id16)

**Note:**

Since the result set is too large, _Row Limiting Clause_ was added. You can remove this clause to
retrieve the entire result set.

**1. Retrieving UROWID from a table that does not have an explicit column with this data type**

The following query displays an error in Snowflake since hr.countries do not contain a ROWID (as
mentioned in
[Oracle’s documentation](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/Data-Types.html#GUID-E9F3AE1C-AA6D-4262-A15F-778833251361)
UROWID is accessed with `SELECT` … `ROWID` statement) column.

#### Oracle[¶](#id17)

```
SELECT
    rowid,
    country_name
FROM
    hr.countries FETCH NEXT 10 ROWS ONLY;
```

##### Result[¶](#id18)

<!-- prettier-ignore -->
|ROWID|COUNTRY_NAME|
|---|---|
|\*BAMAAJMCQVL+|Argentina|
|\*BAMAAJMCQVX+|Australia|
|\*BAMAAJMCQkX+|Belgium|
|\*BAMAAJMCQlL+|Brazil|
|\*BAMAAJMCQ0H+|Canada|
|\*BAMAAJMCQ0j+|Switzerland|
|\*BAMAAJMCQ07+|China|
|\*BAMAAJMCREX+|Germany|
|\*BAMAAJMCREv+|Denmark|
|\*BAMAAJMCRUf+|Egypt|

##### Snowflake[¶](#id19)

```
SELECT
        --** SSC-FDM-OR0030 - ROWID PSEUDOCOLUMN IS NOT SUPPORTED IN SNOWFLAKE, IT WAS CONVERTED TO NULL TO AVOID RUNTIME ERRORS **
        '' AS rowid,
        country_name
FROM
        hr.countries
FETCH NEXT 10 ROWS ONLY;
```

##### Result[¶](#id20)

Danger

SQL compilation error: invalid identifier ‘ROWID’

##### 2. EWI should be displayed by SnowConvert AI[¶](#ewi-should-be-displayed-by-snowconvert-ai)

EWI should be displayed when trying to select UROWID column. There is a work item to add the
corresponding EWI.

Danger

This issue has been marked as critical and will be fixed in the upcoming releases.

### Related EWIs[¶](#id21)

1. [SSC-EWI-0036](../../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0036):
   Data type converted to another data type.
2. [SSC-FDM-OR0030](../../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM.html#ssc-fdm-or0030):
   ROWID pseudocolumn is not supported in Snowflake.
