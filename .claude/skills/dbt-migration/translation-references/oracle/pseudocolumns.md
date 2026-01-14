---
description: Translation spec for ROWID pseudocolumn
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/oracle/pseudocolumns
title: SnowConvert AI - Oracle - Pseudocolumns | Snowflake Documentation
---

## ROWID[¶](#rowid)

Translation spec for ROWID pseudocolumn

### Description[¶](#description)

> For each row in the database, the `ROWID` pseudocolumn returns the address of the row.
> ([Oracle SQL Language Reference Rowid pseudocolumn](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/ROWID-Pseudocolumn.html#GUID-F6E0FBD2-983C-495D-9856-5E113A17FAF1))

Snowflake does not have an equivalent for ROWID. The pseudocolumn is transformed to _NULL_ in order
to avoid runtime errors.

```
ROWID
```

### Sample Source Patterns[¶](#sample-source-patterns)

#### Oracle[¶](#oracle)

```
CREATE TABLE sample_table
(
    sample_column varchar(10)
);

INSERT INTO sample_table(sample_column) VALUES ('text 1');
INSERT INTO sample_table(sample_column) VALUES ('text 2');

SELECT ROWID FROM sample_table;
SELECT MAX(ROWID) FROM sample_table;
```

##### Result Query 1[¶](#result-query-1)

```
<!-- prettier-ignore -->
|ROWID|
|---|
|AAASfCAABAAAIcpAAA|
|AAASfCAABAAAIcpAAB|
```

##### Result Query 2[¶](#result-query-2)

```
<!-- prettier-ignore -->
|MAX(ROWID)|
|---|
|AAASfCAABAAAIcpAAB|
```

##### Snowflake[¶](#snowflake)

```
CREATE OR REPLACE TABLE sample_table
    (
        sample_column varchar(10)
    )
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
;

INSERT INTO sample_table(sample_column) VALUES ('text 1');

INSERT INTO sample_table(sample_column) VALUES ('text 2');

SELECT
--** SSC-FDM-OR0030 - ROWID PSEUDOCOLUMN IS NOT SUPPORTED IN SNOWFLAKE, IT WAS CONVERTED TO NULL TO AVOID RUNTIME ERRORS **
'' AS ROWID
FROM
sample_table;

SELECT MAX(
--** SSC-FDM-OR0030 - ROWID PSEUDOCOLUMN IS NOT SUPPORTED IN SNOWFLAKE, IT WAS CONVERTED TO NULL TO AVOID RUNTIME ERRORS **
'' AS ROWID) FROM
sample_table;
```

##### Result Query 1[¶](#id1)

<!-- prettier-ignore -->
|NULL|
|---|
|      |
|      |

### Known Issues[¶](#known-issues)

No issues were found.

### Related EWIs[¶](#related-ewis)

- [SSC-FDM-OR0030](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM.html#ssc-fdm-or0030):
  ROWID pseudocolumn is not supported in Snowflake

## ROWNUM[¶](#rownum)

Translation spec for ROWNUM pseudocolumn

### Description[¶](#id2)

> For each row returned by a query, the `ROWNUM` pseudocolumn returns a number indicating the order
> in which Oracle selects the row from a table or set of joined rows.
> ([Oracle SQL Language Reference Rownum pseudocolumn](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/ROWNUM-Pseudocolumn.html#GUID-2E40EC12-3FCF-4A4F-B5F2-6BC669021726))

Snowflake does not have an equivalent for ROWNUM. The approach for the transformation is taking
advantage of the Snowflake [seq8](https://docs.snowflake.com/en/sql-reference/functions/seq1.html)
function to emulate the functionality.

```
ROWNUM
```

### Sample Source Patterns[¶](#id3)

#### Oracle[¶](#id4)

```
-- Table with sample data
CREATE TABLE TABLE1(COL1 VARCHAR(20), COL2 NUMBER);
INSERT INTO TABLE1 (COL1, COL2) VALUES('ROWNUM: ', null);
INSERT INTO TABLE1 (COL1, COL2) VALUES('ROWNUM: ', null);

-- Query 1: ROWNUM in a select

@@ -159,10 +171,10 @@ SELECT ROWNUM FROM TABLE1;
-- Query 2: ROWNUM in DML
UPDATE TABLE1 SET COL2 = ROWNUM;
SELECT * FROM TABLE1;
```

##### Result Query 1[¶](#id5)

```
<!-- prettier-ignore -->
|ROWNUM|
|---|
|1|
|2|
```

##### Result Query 2[¶](#id6)

```
<!-- prettier-ignore -->
|COL1|COL2|
|---|---|
|ROWNUM:|1|
|ROWNUM:|2|
```

##### Snowflake[¶](#id7)

```
-- Table with sample data
CREATE OR REPLACE TABLE TABLE1 (COL1 VARCHAR(20),
COL2 NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}}'
;

INSERT INTO TABLE1(COL1, COL2) VALUES('ROWNUM: ', null);

INSERT INTO TABLE1(COL1, COL2) VALUES('ROWNUM: ', null);

-- Query 1: ROWNUM in a select
SELECT
seq8() + 1
FROM
TABLE1;

-- Query 2: ROWNUM in DML
UPDATE TABLE1
SET COL2 = seq8() + 1;

SELECT * FROM
TABLE1;
```

##### Result Query 1[¶](#id8)

```
<!-- prettier-ignore -->
|SEQ8() + 1|
|---|
|1|
|2|
```

##### Result Query 2[¶](#id9)

```
<!-- prettier-ignore -->
|COL1|COL2|
|---|---|
|ROWNUM:|1|
|ROWNUM:|2|
```

### Known Issues[¶](#id10)

No issues were found.

### Related EWIs[¶](#id11)

1. [SSC-FDM-0006:](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0006)
   Number type column may not behave similarly in Snowflake
