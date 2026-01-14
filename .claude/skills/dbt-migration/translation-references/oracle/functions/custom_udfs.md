---
description:
  Some Oracle built-in functions and functionalities may not be available or may behave differently
  in Snowflake. To minimize these differences, some functions are replaced with SnowConvert AI
  Custom UD
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/oracle/functions/custom_udfs
title: SnowConvert AI - Oracle - SnowConvert AI Custom UDFs | Snowflake Documentation
---

## Description[¶](#description)

Some Oracle built-in functions and functionalities may not be available or may behave differently in
Snowflake. To minimize these differences, some functions are replaced with SnowConvert AI Custom
UDFs.

These UDFs are automatically created during migration, in the `UDF Helper` folder, inside the
`Output` folder. There is one file per custom UDF.

## BFILENAME UDF[¶](#bfilename-udf)

### Description[¶](#id1)

This function takes the directory name and the file name parameters of the Oracle `BFILENAME()` as
`STRING` and returns a concatenation of them using `\`. Since `BFILE` is translated to `VARCHAR`,
the `BFILENAME` result is handled as text.

Warning

The `\` must be changed to match the corresponding operating system file concatenation character.

### Custom UDF overloads[¶](#custom-udf-overloads)

#### BFILENAME_UDF(string, string)[¶](#bfilename-udf-string-string)

It concatenates the directory path and the file name.

**Parameters**

1. **DIRECTORYNAME**: A `STRING` that represents the directory path.
2. **FILENAME**: A `STRING` that represents the file name.

##### UDF[¶](#udf)

```
CREATE OR REPLACE FUNCTION PUBLIC.BFILENAME_UDF (DIRECTORYNAME STRING, FILENAME STRING)
RETURNS STRING
LANGUAGE SQL
IMMUTABLE
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}'
AS
$$
	DIRECTORYNAME || '\\' || FILENAME
$$;
```

Copy

##### Oracle[¶](#oracle)

```
--Create Table
CREATE TABLE bfile_table ( col1 BFILE );

--Insert Bfilename
INSERT INTO bfile_table VALUES ( BFILENAME('mydirectory', 'myfile.png') );

--Select
SELECT * FROM bfile_table;
```

Copy

##### Result[¶](#result)

<!-- prettier-ignore -->
|COL1|
|---|
|[BFILE:myfile.png]|

##### Snowflake[¶](#snowflake)

```
--Create Table
CREATE OR REPLACE TABLE bfile_table ( col1
!!!RESOLVE EWI!!! /*** SSC-EWI-OR0105 - ADDITIONAL WORK IS NEEDED FOR BFILE COLUMN USAGE. BUILD_STAGE_FILE_URL FUNCTION IS A RECOMMENDED WORKAROUND ***/!!!
VARCHAR
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

--Insert Bfilename
INSERT INTO bfile_table
VALUES (PUBLIC.BFILENAME_UDF('mydirectory', 'myfile.png') );

--Select
SELECT * FROM
bfile_table;
```

Copy

##### Result[¶](#id2)

<!-- prettier-ignore -->
|COL1|
|---|
|mydirectory\myfile.png|

### Known Issues[¶](#known-issues)

#### 1. No access to the DBMS_LOB built-in package[¶](#no-access-to-the-dbms-lob-built-in-package)

Since LOB data types are not supported in Snowflake there is not an equivalent for the `DBMS_LOB`
functions and there are no implemented workarounds yet.

### Related EWIs[¶](#related-ewis)

1. [SSC-EWI-OR0105](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI.html#ssc-ewi-or0105):
   Additional Work Is Needed For BFILE Column Usage.

## CAST_DATE UDF[¶](#cast-date-udf)

Note

Some parts in the output code are omitted for clarity reasons.

### Description[¶](#id3)

This custom UDF is added to avoid runtime exceptions caused by format differences when casting
strings to `DATE`, inside procedures and functions.

### Custom UDF overloads[¶](#id4)

#### CAST_DATE_UDF(datestr)[¶](#cast-date-udf-datestr)

It creates a `DATE` from a `STRING`.

**Parameters**

1. **DATESTR**: A `STRING` that represents a `DATE` with a specific format.

##### UDF[¶](#id5)

```
CREATE OR REPLACE FUNCTION PUBLIC.CAST_DATE_UDF(DATESTR STRING)
RETURNS DATE
LANGUAGE SQL
IMMUTABLE
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}'
AS
$$
	SELECT TO_DATE(DATESTR,'YYYY-MM-DD"T"HH24:MI:SS.FF')
$$;
```

Copy

##### Oracle[¶](#id6)

```
--Create Table
CREATE TABLE jsdateudf_table( col1 DATE );

--Create Procedure
CREATE OR REPLACE PROCEDURE jsdateudf_proc ( par1 DATE )
IS
BEGIN
    INSERT INTO jsdateudf_table VALUES(par1);
END;

--Insert Date
CALL jsdateudf_proc('20-03-1996');

--Select
SELECT * FROM jsdateudf_table;
```

Copy

##### Result[¶](#id7)

<!-- prettier-ignore -->
|COL1|
|---|
|1996-03-20 00:00:00.000|

##### Snowflake[¶](#id8)

```
--Create Table
CREATE OR REPLACE TABLE jsdateudf_table ( col1 TIMESTAMP /*** SSC-FDM-OR0042 - DATE TYPE COLUMN HAS A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
;

--Create Procedure
CREATE OR REPLACE PROCEDURE jsdateudf_proc (par1 TIMESTAMP /*** SSC-FDM-OR0042 - DATE TYPE COLUMN HAS A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        INSERT INTO jsdateudf_table
        VALUES(:par1);
    END;
$$;

--Insert Date
CALL jsdateudf_proc('20-03-1996');

--Select
SELECT * FROM
    jsdateudf_table;
```

Copy

##### Result[¶](#id9)

<!-- prettier-ignore -->
|COL1|
|---|
|1996-03-20|

### Known Issues[¶](#id10)

#### 1. Oracle DATE contains TIMESTAMP[¶](#oracle-date-contains-timestamp)

Take into consideration that Oracle `DATE` contains an empty `TIMESTAMP` (00:00:00.000), while
Snowflake `DATE` does not. SnowConvert AI allows transforming `DATE` to `TIMESTAMP` with the
SysdateAsCurrentTimestamp flag.

### Related EWIs[¶](#id11)

1. [SSC-FDM-OR0042](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM.html#ssc-fdm-or0042):
   Date Type Transformed To Timestamp Has A Different Behavior

## DATE_TO_JULIANDAYS_UDF[¶](#date-to-juliandays-udf)

### Description[¶](#id12)

The DATE_TO_JULIANDAYS_UDF() function takes a DATE and returns the number of days since January 1,
4712 BC. This function is equivalent to the Oracle TO_CHAR(DATE,’J’)

### Custom UDF overloads[¶](#id13)

#### DATE_TO_JULIANDAYS_UDF(date)[¶](#date-to-juliandays-udf-date)

**Parameters**

1. **INPUT_DATE**: The `DATE` of the operation.

##### UDF[¶](#id14)

```
CREATE OR REPLACE FUNCTION PUBLIC.DATE_TO_JULIAN_DAYS_UDF(input_date DATE)
RETURNS NUMBER
IMMUTABLE
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}'
AS
$$
    DATEDIFF(DAY,TO_DATE('00000101','YYYYMMDD'),TO_DATE('01/01/4712','DD/MM/YYYY')) +
    DATEDIFF(DAY,TO_DATE('00000101','YYYYMMDD'),input_date) + 38
    // Note: The 38 on the equation marks the differences in days between calendars and must be updated on the year 2099
$$
;
```

Copy

#### Usage Example[¶](#usage-example)

##### Oracle[¶](#id15)

```
--Create Table
CREATE TABLE datetojulian_table (col1 DATE);

INSERT INTO datetojulian_table VALUES (DATE '2020-01-01');
INSERT INTO datetojulian_table VALUES (DATE '1900-12-31');
INSERT INTO datetojulian_table VALUES (DATE '1904-02-29');
INSERT INTO datetojulian_table VALUES (DATE '1903-03-01');
INSERT INTO datetojulian_table VALUES (DATE '2000-12-31');

--Select
SELECT TO_CHAR(col1, 'J') FROM datetojulian_table;
```

Copy

##### Snowflake[¶](#id16)

```
--Create Table
CREATE OR REPLACE TABLE datetojulian_table (col1 TIMESTAMP /*** SSC-FDM-OR0042 - DATE TYPE COLUMN HAS A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
;

INSERT INTO datetojulian_table
VALUES (DATE '2020-01-01');

INSERT INTO datetojulian_table
VALUES (DATE '1900-12-31');

INSERT INTO datetojulian_table
VALUES (DATE '1904-02-29');

INSERT INTO datetojulian_table
VALUES (DATE '1903-03-01');

INSERT INTO datetojulian_table
VALUES (DATE '2000-12-31');

--Select
SELECT
PUBLIC.DATE_TO_JULIAN_DAYS_UDF(col1)
FROM
datetojulian_table;
```

Copy

### Known Issues[¶](#id17)

No issues were found.

### Related EWIs[¶](#id18)

- [SSC-FDM-OR0042](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM.html#ssc-fdm-or0042):
  Date Type Transformed To Timestamp Has A Different Behavior

## DATEADD UDF[¶](#dateadd-udf)

### Description[¶](#id19)

This UDF is used as a template for all cases when there is an addition between a `DATE` or
`TIMESTAMP` type and `FLOAT` type.

### Custom UDF overloads[¶](#id20)

#### DATEADD_UDF(date, float)[¶](#dateadd-udf-date-float)

**Parameters**

1. **FIRST_PARAM**: The first `DATE` of the operation.
2. **SECOND_PARAM**: The `FLOAT` to be added.

##### UDF[¶](#id21)

```
CREATE OR REPLACE FUNCTION PUBLIC.DATEADD_UDF(FIRST_PARAM DATE, SECOND_PARAM FLOAT)
RETURNS DATE
LANGUAGE SQL
IMMUTABLE
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}'
AS
$$
SELECT FIRST_PARAM + SECOND_PARAM::NUMBER
$$;
```

Copy

#### DATEADD_UDF(float, date)[¶](#dateadd-udf-float-date)

**Parameters**

1. **FIRST_PARAM**: The `FLOAT` to be added.
2. **SECOND_PARAM**: The `DATE` of the operation.

##### UDF[¶](#id22)

```
CREATE OR REPLACE FUNCTION PUBLIC.DATEADD_UDF(FIRST_PARAM FLOAT, SECOND_PARAM DATE)
RETURNS DATE
LANGUAGE SQL
IMMUTABLE
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}'
AS
$$
SELECT FIRST_PARAM::NUMBER + SECOND_PARAM
$$;
```

Copy

#### DATEADD_UDF(timestamp, float)[¶](#dateadd-udf-timestamp-float)

**Parameters**

1. **FIRST_PARAM**: The first `TIMESTAMP` of the operation.
2. **SECOND_PARAM**: The `FLOAT` to be added.

##### UDF[¶](#id23)

```
CREATE OR REPLACE FUNCTION PUBLIC.DATEADD_UDF(FIRST_PARAM TIMESTAMP, SECOND_PARAM FLOAT)
RETURNS TIMESTAMP
LANGUAGE SQL
IMMUTABLE
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}'
AS
$$
SELECT DATEADD(day, SECOND_PARAM,FIRST_PARAM)
$$;
```

Copy

#### DATEADD_UDF(float, timestamp)[¶](#dateadd-udf-float-timestamp)

**Parameters**

1. **FIRST_PARAM**: The`FLOAT` of the operation.
2. **SECOND_PARAM**: The`TIMESTAMP` of the operation.

##### UDF[¶](#id24)

```
CREATE OR REPLACE FUNCTION PUBLIC.DATEADD_UDF(FIRST_PARAM FLOAT, SECOND_PARAM TIMESTAMP)
RETURNS TIMESTAMP
LANGUAGE SQL
IMMUTABLE
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}'
AS
$$
SELECT DATEADD(day, FIRST_PARAM,SECOND_PARAM)
$$;
```

Copy

#### Usage example[¶](#id25)

##### Oracle[¶](#id26)

```
SELECT
    TO_TIMESTAMP('03/08/2009, 12:47 AM', 'dd/mm/yy, hh:mi AM')+62.40750856543442
FROM DUAL;
```

Copy

##### Result[¶](#id27)

<!-- prettier-ignore -->
|TO_TIMESTAMP(‘03/08/2009,12:47AM’,’DD/MM/YY,HH:MIAM’)+62.40750856543442|
|---|
|2009-10-04 10:33:49.000|

##### Snowflake[¶](#id28)

```
SELECT
    PUBLIC.DATEADD_UDF(TO_TIMESTAMP('03/08/2009, 12:47 AM', 'dd/mm/yy, hh:mi AM'), 62.40750856543442)
FROM DUAL;
```

Copy

##### Result[¶](#id29)

<!-- prettier-ignore -->
|PUBLIC.DATEADD_UDF(

<!-- prettier-ignore -->
|TO_TIMESTAMP(‘03/08/2009, 12:47 AM’, ‘DD/MM/YY, HH12:MI AM’), 62.40750856543442)|
|---|
|2009-10-04 00:47:00.000|

### Known Issues[¶](#id30)

#### 1. Differences in time precision[¶](#differences-in-time-precision)

When there are operations between Dates or Timestamps and Floats, the time may differ from Oracle’s.
There is an action item to fix this issue.

### Related EWIs[¶](#id31)

No EWIs related.

## DATEDIFF UDF[¶](#datediff-udf)

Note

Some parts in the output code are omitted for clarity reasons.

### Description[¶](#id32)

This UDF is used as a template for all cases when there is a subtraction between a `DATE,`
`TIMESTAMP,` and any other type (except Intervals).

### Custom UDF overloads[¶](#id33)

#### DATEDIFF_UDF(date, date)[¶](#datediff-udf-date-date)

**Parameters**

1. **FIRST_PARAM**: The first `DATE` of the operation.
2. **SECOND_PARAM**: The `DATE` to be subtracted.

##### UDF[¶](#id34)

```
CREATE OR REPLACE FUNCTION PUBLIC.DATEDIFF_UDF(FIRST_PARAM DATE, SECOND_PARAM DATE)
RETURNS INTEGER
LANGUAGE SQL
IMMUTABLE
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}'
AS
$$
	FIRST_PARAM - SECOND_PARAM
$$;
```

Copy

#### DATEDIFF_UDF(date, **timestamp**)[¶](#datediff-udf-date-timestamp)

**Parameters**

1. **FIRST_PARAM**: The first `DATE` of the operation.
2. **SECOND_PARAM**: The `TIMESTAMP` to be subtracted.

##### UDF[¶](#id35)

```
CREATE OR REPLACE FUNCTION PUBLIC.DATEDIFF_UDF(FIRST_PARAM DATE, SECOND_PARAM TIMESTAMP)
RETURNS INTEGER
LANGUAGE SQL
IMMUTABLE
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}'
AS
$$
	FIRST_PARAM - SECOND_PARAM::DATE
$$;
```

Copy

#### DATEDIFF_UDF(date, integer)[¶](#datediff-udf-date-integer)

**Parameters**

1. **FIRST_PARAM**: The first `DATE` of the operation.
2. **SECOND_PARAM**: The `INTEGER` to be subtracted.

##### UDF[¶](#id36)

```
CREATE OR REPLACE FUNCTION PUBLIC.DATEDIFF_UDF(FIRST_PARAM DATE, SECOND_PARAM INTEGER)
RETURNS DATE
LANGUAGE SQL
IMMUTABLE
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}'
AS
$$
	DATEADD(day,SECOND_PARAM*-1 ,FIRST_PARAM)
$$;
```

Copy

#### DATEDIFF_UDF(timestamp, timestamp)[¶](#datediff-udf-timestamp-timestamp)

**Parameters**

1. **FIRST_PARAM**: The first `TIMESTAMP` of the operation.
2. **SECOND_PARAM**: The `TIMESTAMP` to be subtracted.

##### UDF[¶](#id37)

```
CREATE OR REPLACE FUNCTION PUBLIC.DATEDIFF_UDF(FIRST_PARAM TIMESTAMP, SECOND_PARAM TIMESTAMP)
RETURNS INTEGER
LANGUAGE SQL
IMMUTABLE
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}'
AS
$$
	DATEDIFF(day,SECOND_PARAM ,FIRST_PARAM)
$$;
```

Copy

#### DATEDIFF_UDF(timestamp, date)[¶](#datediff-udf-timestamp-date)

**Parameters**

1. **FIRST_PARAM**: The first `TIMESTAMP` of the operation.
2. **SECOND_PARAM**: The `DATE` to be subtracted.

##### UDF[¶](#id38)

```
CREATE OR REPLACE FUNCTION PUBLIC.DATEDIFF_UDF(FIRST_PARAM TIMESTAMP, SECOND_PARAM DATE)
RETURNS INTEGER
LANGUAGE SQL
IMMUTABLE
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}'
AS
$$
	DATEDIFF(day,SECOND_PARAM ,FIRST_PARAM)
$$;
```

Copy

#### DATEDIFF_UDF(timestamp, number)[¶](#datediff-udf-timestamp-number)

**Parameters**

1. **FIRST_PARAM**: The first `TIMESTAMP` of the operation.
2. **SECOND_PARAM**: The `NUMBER` to be subtracted.

##### UDF[¶](#id39)

```
CREATE OR REPLACE FUNCTION PUBLIC.DATEDIFF_UDF(FIRST_PARAM TIMESTAMP, SECOND_PARAM NUMBER)
RETURNS TIMESTAMP
LANGUAGE SQL
IMMUTABLE
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}'
AS
$$
	DATEADD(day,SECOND_PARAM*-1,FIRST_PARAM)
$$;
```

Copy

#### Usage example[¶](#id40)

Note

The unknown is a column whose type could not be resolved, it could be a timestamp, date integer, or
number.

Note

**`--disableDateAsTimestamp`**

Flag to indicate whether `SYSDATE` should be transformed into `CURRENT_DATE` _or_
`CURRENT_TIMESTAMP`. This will also affect all `DATE` columns that will be transformed to
`TIMESTAMP`.

##### Oracle[¶](#id41)

```
--Create Table
CREATE TABLE times(AsTimeStamp TIMESTAMP, AsDate DATE);

--Subtraction operations
SELECT AsDate - unknown FROM times, unknown_table;
SELECT unknown - AsTimeStamp FROM times;
SELECT AsTimeStamp - unknown FROM times;
SELECT unknown - AsDate FROM times;
```

Copy

##### Snowflake[¶](#id42)

```
--Create Table
CREATE OR REPLACE TABLE times (AsTimeStamp TIMESTAMP(6),
AsDate TIMESTAMP /*** SSC-FDM-OR0042 - DATE TYPE COLUMN HAS A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
;

--Subtraction operations
SELECT
PUBLIC.DATEDIFF_UDF(
                     !!!RESOLVE EWI!!! /*** SSC-EWI-OR0036 - TYPES RESOLUTION ISSUES, ARITHMETIC OPERATION '-' MAY NOT BEHAVE CORRECTLY BETWEEN DATE AND unknown ***/!!!
 AsDate, unknown) FROM
times,
unknown_table;

SELECT
PUBLIC.DATEDIFF_UDF(
                     !!!RESOLVE EWI!!! /*** SSC-EWI-OR0036 - TYPES RESOLUTION ISSUES, ARITHMETIC OPERATION '-' MAY NOT BEHAVE CORRECTLY BETWEEN unknown AND TIMESTAMP ***/!!!
 unknown, AsTimeStamp) FROM
times;

SELECT
PUBLIC.DATEDIFF_UDF(
                     !!!RESOLVE EWI!!! /*** SSC-EWI-OR0036 - TYPES RESOLUTION ISSUES, ARITHMETIC OPERATION '-' MAY NOT BEHAVE CORRECTLY BETWEEN TIMESTAMP AND unknown ***/!!!
 AsTimeStamp, unknown) FROM
times;

SELECT
PUBLIC.DATEDIFF_UDF(
                     !!!RESOLVE EWI!!! /*** SSC-EWI-OR0036 - TYPES RESOLUTION ISSUES, ARITHMETIC OPERATION '-' MAY NOT BEHAVE CORRECTLY BETWEEN unknown AND DATE ***/!!!
 unknown, AsDate) FROM
times;
```

Copy

### Known Issues[¶](#id43)

#### 1. Functional differences for timestamps[¶](#functional-differences-for-timestamps)

Sometimes the Snowflake value returned by the UDF may differ from the Oracle one due to the time.
Consider the following example

##### Oracle[¶](#id44)

```
-- CREATE TABLE UNKNOWN_TABLE(Unknown timestamp);
-- INSERT  INTO UNKNOWN_TABLE VALUES (TO_TIMESTAMP('01/10/09, 12:00 P.M.', 'dd/mm/yy, hh:mi P.M.'));

CREATE TABLE TIMES(AsTimeStamp TIMESTAMP);
INSERT INTO TIMES VALUES (TO_TIMESTAMP('05/11/21, 11:00 A.M.', 'dd/mm/yy, hh:mi A.M.'));

SELECT AsTimeStamp - unknown FROM times, unknown_table;
```

Copy

##### Result[¶](#id45)

<!-- prettier-ignore -->
|ASTIMESTAMP-UNKNOWN|
|---|
|4417 23:0:0.0|

##### Snowflake[¶](#id46)

```
-- CREATE TABLE UNKNOWN_TABLE(Unknown timestamp);
-- INSERT INTO UNKNOWN_TABLE VALUES (TO_TIMESTAMP('01/10/09, 12:00 P.M.', 'dd/mm/yy, hh:mi P.M.'));
CREATE OR REPLACE TABLE TIMES (AsTimeStamp TIMESTAMP(6)
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

INSERT INTO TIMES
VALUES (TO_TIMESTAMP('05/11/21, 11:00 A.M.', 'dd/mm/yy, hh:mi A.M.'));

SELECT
PUBLIC.DATEDIFF_UDF(
                     !!!RESOLVE EWI!!! /*** SSC-EWI-OR0036 - TYPES RESOLUTION ISSUES, ARITHMETIC OPERATION '-' MAY NOT BEHAVE CORRECTLY BETWEEN TIMESTAMP AND unknown ***/!!!
 AsTimeStamp, unknown) FROM
times,
unknown_table;
```

Copy

##### Result[¶](#id47)

<!-- prettier-ignore -->
|PUBLIC.DATEDIFF_UDF( ASTIMESTAMP, UNKNOWN)|
|---|
|4418|

### Related EWIs[¶](#id48)

1. [SSC-EWI-OR0036](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI.html#ssc-ewi-or0036):
   Types resolution issues, the arithmetic operation may not behave correctly between string and
   date.
2. [SSC-FDM-OR0042](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM.html#ssc-fdm-or0042):
   Date Type Transformed To Timestamp Has A Different Behavior.

## JSON_VALUE UDF[¶](#json-value-udf)

Translation reference to convert Oracle JSON_VALUE function to Snowflake

Note

Some parts in the output code are omitted for clarity reasons.

### Description[¶](#id49)

As per Oracle’s documentation, this function uses the
[SQL/JSON Path Expression](https://docs.oracle.com/en/database/oracle/oracle-database/19/adjsn/json-path-expressions.html#GUID-7B610884-39CD-4910-85E7-C251D342D879)
to request information about a portion of a JSON instance. The returning value is always a scalar
value, else the function returns `NULL` by default.

```
JSON_VALUE
  ( expr [ FORMAT JSON ], [ JSON_basic_path_expression ]
    [ JSON_value_returning_clause ] [ JSON_value_on_error_clause ]
    [ JSON_value_on_empty_clause ][ JSON_value_on_mismatch_clause ]
  )
```

Copy

The JSON_VALUE_UDF is a Snowflake implementation of the JSONPath specification that uses a modified
version of the original JavaScript implementation developed by
[Stefan Goessner](https://goessner.net/index.html).

### Sample Source Patterns[¶](#sample-source-patterns)

#### Setup Data[¶](#setup-data)

Run these queries to run queries in the JSON_VALUE Patterns section.

##### Oracle[¶](#id50)

```
CREATE TABLE MY_TAB (
    my_json VARCHAR(5000)
);

INSERT INTO MY_TAB VALUES ('{
    "store": {
      "book": [
        { "category": "reference",
          "author": "Nigel Rees",
          "title": "Sayings of the Century",
          "price": 8.95
        },
        { "category": "fiction",
          "author": "Evelyn Waugh",
          "title": "Sword of Honour",
          "price": 12.99
        },
        { "category": "fiction",
          "author": "Herman Melville",
          "title": "Moby Dick",
          "isbn": "0-553-21311-3",
          "price": 8.99
        },
        { "category": "fiction",
          "author": "J. R. R. Tolkien",
          "title": "The Lord of the Rings",
          "isbn": "0-395-19395-8",
          "price": 22.99
        }
      ],
      "bicycle": {
        "color": "red",
        "price": 19.95
      }
    }
  }');
```

Copy

##### Snowflake[¶](#id51)

```
CREATE OR REPLACE TABLE MY_TAB (
       my_json VARCHAR(5000)
   )
   COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
   ;

   INSERT INTO MY_TAB
   VALUES ('{
    "store": {
      "book": [
        { "category": "reference",
          "author": "Nigel Rees",
          "title": "Sayings of the Century",
          "price": 8.95
        },
        { "category": "fiction",
          "author": "Evelyn Waugh",
          "title": "Sword of Honour",
          "price": 12.99
        },
        { "category": "fiction",
          "author": "Herman Melville",
          "title": "Moby Dick",
          "isbn": "0-553-21311-3",
          "price": 8.99
        },
        { "category": "fiction",
          "author": "J. R. R. Tolkien",
          "title": "The Lord of the Rings",
          "isbn": "0-395-19395-8",
          "price": 22.99
        }
      ],
      "bicycle": {
        "color": "red",
        "price": 19.95
      }
    }
  }');
```

Copy

#### JSON_VALUE Patterns[¶](#json-value-patterns)

##### Oracle[¶](#id52)

```
-- 'Sayings of the Century'
SELECT JSON_VALUE(MY_JSON, '$..book[0].title') AS VALUE FROM MY_TAB;

-- NULL
-- gets books in positions 0, 1, 2 and 3 but returns null (default behavior) since a non scalar value was returned
SELECT JSON_VALUE(MY_JSON, '$..book[0,1 to 3,3]') AS VALUE FROM MY_TAB;

-- 'Sayings of the Century'
SELECT JSON_VALUE(MY_JSON, '$.store.book[*]?(@.category == "reference").title') AS VALUE FROM MY_TAB;

-- 'MY ERROR MESSAGE'
-- triggers error because the result is a non scalar value (is an object)
SELECT JSON_VALUE(MY_JSON, '$..book[0]' DEFAULT 'MY ERROR MESSAGE' ON ERROR DEFAULT 'MY EMPTY MESSAGE' ON EMPTY) AS VALUE FROM MY_TAB;

-- 'MY EMPTY MESSAGE'
-- triggers the on empty class because does not exists in the first book element
SELECT JSON_VALUE(MY_JSON, '$..book[0].isbn' DEFAULT 'MY ERROR MESSAGE' ON ERROR DEFAULT 'MY EMPTY MESSAGE' ON EMPTY) AS VALUE FROM MY_TAB;

-- Oracle error message: ORA-40462: JSON_VALUE evaluated to no value
-- this is a custom message from the UDF when no match is found and the ON ERROR clause is set to ERROR
SELECT JSON_VALUE(MY_JSON, '$..book[0].isbn' ERROR ON ERROR) AS VALUE FROM MY_TAB;

-- NULL
SELECT JSON_VALUE(MY_JSON, '$..book[0].isbn' NULL ON ERROR) AS VALUE FROM MY_TAB;

-- Oracle error message: ORA-40462: JSON_VALUE evaluated to no value
-- this is a custom message from the UDF when no match is found and the ON EMPTY clause is set to ERROR
SELECT JSON_VALUE(MY_JSON, '$..book[0].isbn' ERROR ON EMPTY) AS VALUE FROM MY_TAB;

-- NULL
SELECT JSON_VALUE(MY_JSON, '$..book[0].isbn' NULL ON EMPTY) AS VALUE FROM MY_TAB;

-- 'Sayings of the Century'
SELECT JSON_VALUE(MY_JSON, '$..book[0].title' RETURNING VARCHAR2) AS VALUE FROM MY_TAB;

-- 'Sayin'
SELECT JSON_VALUE(MY_JSON, '$..book[0].title' RETURNING VARCHAR2(5) TRUNCATE) AS VALUE FROM MY_TAB;

-- 'Sayings of the Century'
SELECT JSON_VALUE(MY_JSON, '$..book[0].title' RETURNING CLOB) AS VALUE FROM MY_TAB;

-- NULL
-- This is because the title field is a string and the function expects a number result type
SELECT JSON_VALUE(MY_JSON, '$..book[0].title' RETURNING NUMBER) AS VALUE FROM MY_TAB;

-- 420
-- This is because the title field is a string and the function expects a number result type
SELECT JSON_VALUE(MY_JSON, '$..book[0].title' RETURNING NUMBER DEFAULT 420 ON ERROR) AS VALUE FROM MY_TAB;

-- Oracle error message: ORA-01858: a non-numeric character was found where a numeric was expected
SELECT JSON_VALUE(MY_JSON, '$..book[0].title' RETURNING DATE ERROR ON ERROR) AS VALUE FROM MY_TAB;

-- ORA-40450: invalid ON ERROR clause
SELECT JSON_VALUE(MY_JSON, '$..book[0].title' ERROR ON MISMATCH) AS VALUE FROM MY_TAB;
```

Copy

##### Results[¶](#results)

<!-- prettier-ignore -->
|JSON Path|Query result|
|---|---|
|`'$..book[0].title'`|`'Sayings of the Century'`|
|`'$..book[0,1 to 3,3]'`|`NULL`|
|`'$.store.book[*]?(@.category == "reference").title'`|`'Sayings of the Century'`|
|`'$..book[0]'`|`'MY ERROR MESSAGE'`|
|`'$..book[0].isbn'`|`'MY EMPTY MESSAGE'`|
|`'$..book[0].isbn'`|`ORA-40462: JSON_VALUE evaluated to no value`|
|`'$..book[0].isbn'`|`NULL`|
|`'$..book[0].isbn'`|`ORA-40462: JSON_VALUE evaluated to no value`|
|`'$..book[0].isbn'`|`NULL`|
|`'$..book[0].title'`|`'Sayings of the Century'`|
|`'$..book[0].title'`|`'Sayin'`|
|`'$..book[0].title'`|`'Sayings of the Century'`|
|`'$..book[0].title'`|`NULL`|
|`'$..book[0].title'`|`420`|
|`'$..book[0].title'`|`ORA-01858: a non-numeric character was found where a numeric was expected`|
|`'$..book[0].title'`|`ORA-40450: invalid ON ERROR clause`|

##### Snowflake[¶](#id53)

```
-- 'Sayings of the Century'
SELECT
JSON_VALUE_UDF(MY_JSON, '$..book[0].title', NULL, NULL, NULL) AS VALUE FROM
MY_TAB;

-- NULL
-- gets books in positions 0, 1, 2 and 3 but returns null (default behavior) since a non scalar value was returned
SELECT
JSON_VALUE_UDF(MY_JSON, '$..book[0,1 to 3,3]', NULL, NULL, NULL) AS VALUE FROM
MY_TAB;

-- 'Sayings of the Century'
SELECT
JSON_VALUE_UDF(MY_JSON, '$.store.book[*]?(@.category == "reference").title', NULL, NULL, NULL) AS VALUE FROM
MY_TAB;

-- 'MY ERROR MESSAGE'
-- triggers error because the result is a non scalar value (is an object)
SELECT
JSON_VALUE_UDF(MY_JSON, '$..book[0]', NULL, 'MY ERROR MESSAGE' :: VARIANT, 'MY EMPTY MESSAGE' :: VARIANT) AS VALUE FROM
MY_TAB;

-- 'MY EMPTY MESSAGE'
-- triggers the on empty class because does not exists in the first book element
SELECT
JSON_VALUE_UDF(MY_JSON, '$..book[0].isbn', NULL, 'MY ERROR MESSAGE' :: VARIANT, 'MY EMPTY MESSAGE' :: VARIANT) AS VALUE FROM
MY_TAB;

-- Oracle error message: ORA-40462: JSON_VALUE evaluated to no value
-- this is a custom message from the UDF when no match is found and the ON ERROR clause is set to ERROR
SELECT
JSON_VALUE_UDF(MY_JSON, '$..book[0].isbn', NULL, 'SSC_ERROR_ON_ERROR' :: VARIANT, NULL) AS VALUE FROM
MY_TAB;

-- NULL
SELECT
JSON_VALUE_UDF(MY_JSON, '$..book[0].isbn', NULL, 'SSC_NULL_ON_ERROR' :: VARIANT, NULL) AS VALUE FROM
MY_TAB;

-- Oracle error message: ORA-40462: JSON_VALUE evaluated to no value
-- this is a custom message from the UDF when no match is found and the ON EMPTY clause is set to ERROR
SELECT
JSON_VALUE_UDF(MY_JSON, '$..book[0].isbn', NULL, NULL, 'SSC_ERROR_ON_EMPTY' :: VARIANT) AS VALUE FROM
MY_TAB;

-- NULL
SELECT
JSON_VALUE_UDF(MY_JSON, '$..book[0].isbn', NULL, NULL, 'SSC_NULL_ON_EMPTY' :: VARIANT) AS VALUE FROM
MY_TAB;

-- 'Sayings of the Century'
SELECT
JSON_VALUE_UDF(MY_JSON, '$..book[0].title', 'string', NULL, NULL) AS VALUE FROM
MY_TAB;

-- 'Sayin'
SELECT
LEFT(JSON_VALUE_UDF(MY_JSON, '$..book[0].title', 'string', NULL, NULL), 5) AS VALUE FROM
MY_TAB;

-- 'Sayings of the Century'
SELECT
JSON_VALUE_UDF(MY_JSON, '$..book[0].title', 'string', NULL, NULL) AS VALUE FROM
MY_TAB;

-- NULL
-- This is because the title field is a string and the function expects a number result type
SELECT
JSON_VALUE_UDF(MY_JSON, '$..book[0].title', 'number', NULL, NULL) AS VALUE FROM
MY_TAB;

-- 420
-- This is because the title field is a string and the function expects a number result type
SELECT
JSON_VALUE_UDF(MY_JSON, '$..book[0].title', 'number', 420 :: VARIANT, NULL) AS VALUE FROM
MY_TAB;

-- Oracle error message: ORA-01858: a non-numeric character was found where a numeric was expected
SELECT
!!!RESOLVE EWI!!! /*** SSC-EWI-0021 - RETURNING CLAUSE NOT SUPPORTED IN SNOWFLAKE ***/!!!
JSON_VALUE_UDF(MY_JSON, '$..book[0].title', NULL, 'SSC_ERROR_ON_ERROR' :: VARIANT, NULL) AS VALUE FROM
MY_TAB;

-- ORA-40450: invalid ON ERROR clause
SELECT
!!!RESOLVE EWI!!! /*** SSC-EWI-0021 - ON MISMATCH CLAUSE NOT SUPPORTED IN SNOWFLAKE ***/!!!
SON_VALUE_UDF(MY_JSON, '$..book[0].title', NULL, NULL, NULL) AS VALUE FROM
MY_TAB;
```

Copy

##### Results[¶](#id54)

<!-- prettier-ignore -->
|JSON Path|Query result|
|---|---|
|`'$..book[0].title'`|`'Sayings of the Century'`|
|`'$..book[0,1 to 3,3]'`|`NULL`|
|`'$.store.book[*]?(@.category == "reference").title'`|`'Sayings of the Century'`|
|`'$..book[0]'`|`'MY ERROR MESSAGE'`|
|`'$..book[0].isbn'`|`'MY EMPTY MESSAGE'`|
|`'$..book[0].isbn'`|`"SSC_CUSTOM_ERROR - NO MATCH FOUND"`|
|`'$..book[0].isbn'`|`NULL`|
|`'$..book[0].isbn'`|`"SSC_CUSTOM_ERROR - NO MATCH FOUND"`|
|`'$..book[0].isbn'`|`NULL`|
|`'$..book[0].title'`|`'Sayings of the Century'`|
|`'$..book[0].title'`|`'Sayin'`|
|`'$..book[0].title'`|`'Sayings of the Century'`|
|`'$..book[0].title'`|`NULL`|
|`'$..book[0].title'`|`420`|
|`'$..book[0].title'`|**NOT SUPPORTED**|
|`'$..book[0].title'`|**NOT SUPPORTED**|

### Known Issues[¶](#id55)

#### 1. Returning Type Clause is not fully supported[¶](#returning-type-clause-is-not-fully-supported)

Now, the only supported types when translating the functionality of the RETURNING TYPE clause are
`VARCHAR2`, `CLOB` and `NUMBER`.

For all the other types supported by the original JSON_VALUE function, the JSON_VALUE_UDF will
behave as if no RETURNING TYPE clause was specified.

Unsupported types:

- `DATE`
- `TIMESTAMP [WITH TIME ZONE]`
- `SDO_GEOMETRY`
- `CUSTOM TYPE`

#### 2. ON MISMATCH Clause is not supported[¶](#on-mismatch-clause-is-not-supported)

Now, the ON MISMATCH clause is not supported, and a warning EWI is placed instead. Thus, the
translated code will behave as if no ON MISMATCH clause was originally specified.

#### 3. Complex filters are not supported[¶](#complex-filters-are-not-supported)

Complex filters with more than one expression will return null as they are not supported.

For example, with the same data as before, this JSON path
`$.store.book[*]?(@.category == "reference").title` is supported and will return
`'Sayings of the Century'`.

However, `$.store.book[*]?(@.category == "reference" && @.price < 10).title` will return `null`
since more than one expression is used in the filter.

### Related EWIs[¶](#id56)

1. [SSC-EWI-0021](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0021):
   Not supported in Snowflake.

## JULIAN TO GREGORIAN DATE UDF[¶](#julian-to-gregorian-date-udf)

### Description[¶](#id57)

This User Defined Function (UDF) is used to transform or cast the Julian date format to a Gregorian
date format. Julian dates can be received in three different formats such as JD Edwards World,
astronomy or ordinary format.

### Custom UDF overloads[¶](#id58)

#### JULIAN_TO_GREGORIAN_DATE_UDF(julianDate, formatSelected)[¶](#julian-to-gregorian-date-udf-juliandate-formatselected)

It returns a string with the Gregorian date format YYYY-MM-DD.

##### Parameters:[¶](#parameters)

**JulianDate**: The Julian date to be cast. It can be either CYYDDD (where C is the century) or
YYYYDDD.

**formatSelected**: It represents the format in which the Julian date should be processed. Besides,
it is a CHAR and can accept the following formats:

<!-- prettier-ignore -->
|Format available|Letter representation in CHAR|Description|
|---|---|---|
|Astronomy standardized|‘J’|It is the default format. The cast is based in the expected conversion of the Astronomical Applications Department of the US. The Julian Date format for this is YYYYDDD.|
|JD Edwards World|‘E’|The expected Julian date to be received in this case should be CYYDDD (where C represents the century and is operationalized to be added 19 to the corresponding number).|
|Ordinal dates|‘R’|The ordinal dates are an arrangement of numbers which represent a concisely date. The format is YYYYDDD and can be easily read because the year part is not mutable.|

##### UDF[¶](#id59)

```
CREATE OR REPLACE FUNCTION PUBLIC.JULIAN_TO_GREGORIAN_DATE_UDF(JULIAN_DATE CHAR(7), FORMAT_SELECTED CHAR(1))
RETURNS variant
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}'
AS
$$
    const CONST_FOR_MODIFIED_JULIAN_DATE = 0.5;
    const BEGINNING_OF_GREG_CALENTAR = 2299161;
    const CONST_AFTER_GREG_VALUE = 1867216.25;
    const DIVIDENT_TO_GET_CENTURY = 36524.25;
    const LEAP_YEAR_CONSTANT = 4;
    const CONST_TO_GET_DAY_OF_MONTH = 30.6001;

    //Functions definitions

    function julianToGregorian(julianDate){
        const JD = julianDate + CONST_FOR_MODIFIED_JULIAN_DATE; //setting modified julian date
        const Z = Math.floor(JD); //setting fractional part of julian day
        const F = JD - Z; //fractional part of the julian date
        let A, alpha, B, C, D, E, year, month, day;

        //verification for the beginning of gregorian calendar
        if(Z < BEGINNING_OF_GREG_CALENTAR){
            A=Z;
        } else {
            //alpha is for dates after the beginning of gregorian calendar
            alpha = Math.floor((Z-CONST_AFTER_GREG_VALUE) / DIVIDENT_TO_GET_CENTURY);
            A=Z+1+alpha - Math.floor(alpha/LEAP_YEAR_CONSTANT);
        }

        B = A + 1524;
        C = Math.floor((B-122.1)/365.25);
        D = Math.floor(365.25*C);
        E = Math.floor((B-D)/CONST_TO_GET_DAY_OF_MONTH);

        day= Math.floor(B-D-Math.floor(CONST_TO_GET_DAY_OF_MONTH*E)+F);
        month=(E<14)? E -1: E-13;
        year=(month>2)? C-4716: C-4715;

        return new Date(year, month-1, day);
    }

function cyydddToGregorian(julianDate){
        var c=Math.floor(julianDate/1000);
        var yy=(c<80)? c+2000: c+1900;
        var ddd=julianDate%1000;
        var date= new Date(yy, 0);
        date.setDate(ddd);
        return date;
    }

function ordinalDate(ordinalDate){
    const year = parseInt(ordinalDate.toString().substring(0,4));
    const dayOfYear = parseInt(ordinalDate.toString().substring(4));
    const date = new Date(year, 0); //Set date to the first day of year
    date.setDate(dayOfYear);
    return date;
}

function formatDate(toFormatDate){
    toFormatDate = toFormatDate.toDateString();
    let year = toFormatDate.split(" ")[3];
    let month = toFormatDate.split(" ")[1];
    let day = toFormatDate.split(" ")[2];
    return new Date(month + day + ", " + Math.abs(year)).toISOString().split('T')[0]
}

    switch(FORMAT_SELECTED){
        case 'E':
            //JD Edwards World formar, century added  - CYYDDD
            var result = formatDate(cyydddToGregorian(parseInt(JULIAN_DATE)));
            return result;
        break;
        case 'J':
            //astronomical format YYYYDDD
            return formatDate(julianToGregorian(parseInt(JULIAN_DATE)));
        break;
        case 'R':
            //ordinal date format YYYYDDD
            return formatDate(ordinalDate(parseInt(JULIAN_DATE)));
        break;
        default: return null;
    }

$$
;
```

Copy

### Usage Example[¶](#id60)

#### Oracle[¶](#id61)

```
select to_date('2020001', 'J') from dual;
```

Copy

##### Result[¶](#id62)

<!-- prettier-ignore -->
|TO_DATE(‘2020001’, ‘J’)|
|---|
|18-JUN-18|

##### Formatted result[¶](#formatted-result)

<!-- prettier-ignore -->
|TO_CHAR(TO_DATE(‘2020001’, ‘J’), ‘YYYY-MON-DD’)|
|---|
|0818-JUN-18|

- _Note: The date must be formatted in order to visualize all digits of the year._

#### Snowflake[¶](#id63)

```
select
PUBLIC.JULIAN_TO_GREGORIAN_DATE_UDF('2020001', 'J')
from dual;
```

Copy

##### Result[¶](#id64)

<!-- prettier-ignore -->
|JULIAN_TO_GREGORIAN_DATE_UDF(‘2020001’, ‘J’)|
|---|
|“0818-06-18”|

### Know Issues[¶](#know-issues)

1. Any other format: If the Julian Date is formatted in any other not supported format, there would
   be differences in the output.
2. Ranges of B.C. dates may represent inconsistencies due to unsupported Snowflake functions for
   dates.

#### Related EWIs[¶](#id65)

No EWIs related.

## MONTHS BETWEEN UDF [DEPRECATED][¶](#months-between-udf-deprecated)

Danger

This UDF has been deprecated. Current transformation for **Oracle**
[MONTHS_BETWEEN()](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/MONTHS_BETWEEN.html#GUID-E4A1AEC0-F5A0-4703-9CC8-4087EB889952)
is **Snowflake**
[MONTHS_BETWEEN()](https://docs.snowflake.com/en/sql-reference/functions/months_between.html#months-between).

### Description[¶](#id66)

> `MONTHS_BETWEEN` returns number of months between dates `date1` and `date2`.
> ([Oracle MONTHS_BETWEEN SQL Language Reference](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/MONTHS_BETWEEN.html#GUID-E4A1AEC0-F5A0-4703-9CC8-4087EB889952))

```
MONTHS_BETWEEN(date1, date2)
```

Copy

Oracle `MONTHS_BETWEEN` and Snowflake `MONTHS_BETWEEN` function, have some functional differences,
to minimize these differences and replicate Oracle `MONTHS_BETWEEN` function better, we added a
custom UDF.

### Custom UDF overloads[¶](#id67)

#### MONTHS_BETWEEN_UDF(timestamp_ltz, timestamp_ltz)[¶](#months-between-udf-timestamp-ltz-timestamp-ltz)

**Parameters**

1. **FIRST_DATE**: The first `TIMESTAMP_LTZ` of the operation.
2. **SECOND_DATE**: The second `TIMESTAMP_LTZ` of the operation.

##### UDF[¶](#id68)

```
CREATE OR REPLACE FUNCTION MONTHS_BETWEEN_UDF(FIRST_DATE TIMESTAMP_LTZ, SECOND_DATE TIMESTAMP_LTZ)
RETURNS NUMBER
IMMUTABLE
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}'
AS
$$
ROUND(MONTHS_BETWEEN(FIRST_DATE, SECOND_DATE))
$$
;
```

Copy

##### Oracle[¶](#id69)

```
SELECT
	MONTHS_BETWEEN('2000-03-20 22:01:11', '1996-03-20 10:01:11'),
	MONTHS_BETWEEN('1996-03-20 22:01:11', '2000-03-20 10:01:11'),
	MONTHS_BETWEEN('1982-05-11 22:31:19', '1900-01-25 15:21:15'),
	MONTHS_BETWEEN('1999-12-25 01:15:16', '1900-12-11 02:05:16')
FROM DUAL;
```

Copy

##### Result[¶](#id70)

<!-- prettier-ignore -->
|MONTHS_BETWEEN(‘2000-03-2022:01:11’,’1996-03-2010:01:11’)|MONTHS_BETWEEN(‘1996-03-2022:01:11’,’2000-03-2010:01:11’)|MONTHS_BETWEEN(‘1982-05-1122:31:19’,’1900-01-2515:21:15’)|MONTHS_BETWEEN(‘1999-12-2501:15:16’,’1900-12-1102:05:16’)|
|---|---|---|---|
|48|-48|987.558021206690561529271206690561529271|1188.450492831541218637992831541218637993|

##### Snowflake[¶](#id71)

```
SELECT
	MONTHS_BETWEEN('2000-03-20 22:01:11', '1996-03-20 10:01:11'),
	MONTHS_BETWEEN('1996-03-20 22:01:11', '2000-03-20 10:01:11'),
	MONTHS_BETWEEN('1982-05-11 22:31:19', '1900-01-25 15:21:15'),
	MONTHS_BETWEEN('1999-12-25 01:15:16', '1900-12-11 02:05:16')
FROM DUAL;
```

Copy

##### Result[¶](#id72)

<!-- prettier-ignore -->
|MONTHS_BETWEEN_UDF(‘2000-03-20 22:01:11’, ‘1996-03-20 10:01:11’)|MONTHS_BETWEEN_UDF(‘1996-03-20 22:01:11’, ‘2000-03-20 10:01:11’)|MONTHS_BETWEEN_UDF(‘1982-05-11 22:31:19’, ‘1900-01-25 15:21:15’)|MONTHS_BETWEEN_UDF(‘1999-12-25 01:15:16’, ‘1900-12-11 02:05:16’)|
|---|---|---|---|
|48.000000|-48.000000|987.558024|1188.450497|

### Known Issues[¶](#id73)

#### 1. Precision may differ from Oracle[¶](#precision-may-differ-from-oracle)

Some results may differ in the number of decimal digits.

### Related EWIs[¶](#id74)

No related EWIs.

## REGEXP LIKE UDF[¶](#regexp-like-udf)

Note

Some parts in the output code are omitted for clarity reasons.

### Description[¶](#id75)

> `REGEXP_LIKE` performs regular expression matching. This condition evaluates strings using
> characters as defined by the input character set.
> ([Oracle Language Regerence REGEXP_LIKE Condition](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/Pattern-matching-Conditions.html#GUID-D2124F3A-C6E4-4CCA-A40E-2FFCABFD8E19))

```
REGEXP_LIKE(source_char, pattern [, match_param ])
```

Copy

Oracle `REGEXP_LIKE` and Snowflake `REGEXP_LIKE` condition, have some functional differences, to
minimize these differences and replicate Oracle `REGEXP_LIKE` function better, we added a custom
UDF. The main idea is to escape the backslash symbol from the regular expression where it is
required. These are the special characters that need to be escaped when they come with a backslash:
`'d', 'D', 'w', 'W', 's', 'S', 'A', 'Z', 'n'`. Also, the **backreference expression** (matches the
same text as most recently matched by the “number specified” capturing group) needs to be escaped.

### Custom UDF overloads[¶](#id76)

#### REGEXP_LIKE_UDF(string, string)[¶](#regexp-like-udf-string-string)

##### Parameters[¶](#id77)

1. **COL:** is the character expression that serves as the search value.
2. **PATTERN:** is the regular expression.

##### UDF[¶](#id78)

```
CREATE OR REPLACE FUNCTION REGEXP_LIKE_UDF(COL STRING, PATTERN STRING)
RETURNS BOOLEAN
LANGUAGE JAVASCRIPT
IMMUTABLE
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}'
AS
$$
return COL.match(new RegExp(PATTERN));
$$;
```

Copy

##### Oracle[¶](#id79)

##### Snowflake[¶](#id80)

#### REGEXP_LIKE_UDF(string, string, string)[¶](#regexp-like-udf-string-string-string)

##### Parameters[¶](#id81)

1. **COL:** is the character expression that serves as the search value.
2. **PATTERN:** is the regular expression.
3. **MATCHPARAM**: is a character expression that let’s change the default matching behavior of the
   condition. In the following table, there are the Oracle characters with their description and
   their equivalent in the UDF.

<!-- prettier-ignore -->
|Match Parameter|Description|UDF Equivalent|
|---|---|---|
|‘i’|Specifies case-insensitive matching, even if the determined collation of the condition is case-sensitive.|‘i’|
|‘c’|Specifies case-sensitive and accent-sensitive matching, even if the determined collation of the condition is case-insensitive or accent-insensitive.|Does not have an equivalent. It is being removed from the parameter..|
|‘n’|Allows the period (.), which is the match-any-character wildcard character, to match the newline character. If you omit this parameter, then the period does not match the newline character.|‘s’|
|‘m’|Treats the source string as multiple lines. Oracle interprets `^` and `$` as the start and end, respectively, of any line anywhere in the source string, rather than only at the start or end of the entire source string. If you omit this parameter, then Oracle treats the source string as a single line.|‘m’|
|‘x’|Ignores whitespace characters. By default, whitespace characters match themselves.|Does not have an equivalent. It is being removed from the parameter.|

##### UDF[¶](#id82)

```
CREATE OR REPLACE FUNCTION REGEXP_LIKE_UDF(COL STRING, PATTERN STRING, MATCHPARAM STRING)
RETURNS BOOLEAN
LANGUAGE JAVASCRIPT
IMMUTABLE
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}'
AS
$$
return COL.match(new RegExp(PATTERN, MATCHPARAM));
$$;
```

Copy

##### Oracle[¶](#id83)

##### Snowflake[¶](#id84)

### Known Issues[¶](#id85)

#### **1. UDF match parameter may not behave as expected**[¶](#udf-match-parameter-may-not-behave-as-expected)

Due to all the characters available in the Oracle match parameter does not have their equivalent in
the user-defined function, the query result may have some functional differences compared to Oracle.

##### 2. UDF pattern parameter does not allow only ‘\’ as a regular expression[¶](#udf-pattern-parameter-does-not-allow-only-as-a-regular-expression)

If as a pattern parameter the regular expression used is only ‘\’ an exception will be thrown like
this: JavaScript execution error: Uncaught SyntaxError: Invalid regular expression: //: \ at end of
pattern in REGEXP_LIKE_UDF at ‘return COL.match(new RegExp(PATTERN));’ position 17 stackstrace:
REGEXP_LIKE_UDF

## TIMESTAMP DIFF UDF[¶](#timestamp-diff-udf)

### Description[¶](#id86)

Snowflake does not support the addition operation between `TIMESTAMP` data types with the `-`
operand. In order to replicate this functionality, we have added a custom UDF.

### Custom UDF overloads[¶](#id87)

#### TIMESTAMP_DIFF_UDF(timestamp, timestamp)[¶](#timestamp-diff-udf-timestamp-timestamp)

**Parameters**

1. **LEFT_TS**: The first `TIMESTAMP` of the operation.
2. **RIGHT_TS**: The `TIMESTAMP` to be added.

##### UDF[¶](#id88)

```
CREATE OR REPLACE FUNCTION TIMESTAMP_DIFF_UDF(LEFT_TS TIMESTAMP, RIGHT_TS TIMESTAMP )
RETURNS VARCHAR
LANGUAGE SQL
IMMUTABLE
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}'
AS
$$
WITH RESULTS(days,hours,min,sec,millisecond,sign) AS
(
  SELECT
  abs(TRUNC(x/1000/3600/24)) days,
  abs(TRUNC(x/1000/60 / 60)-trunc(x/1000/3600/24)*24) hours,
  abs(TRUNC(MOD(x/1000,3600)/60)) min,
  abs(TRUNC(MOD(x/1000,60))) sec,
  abs(TRUNC(MOD(x,1000))) millisecond,
  SIGN(x)
  FROM (SELECT TIMESTAMPDIFF(millisecond, RIGHT_TS, LEFT_TS) x ,SIGN(TIMESTAMPDIFF(millisecond, RIGHT_TS, LEFT_TS)) sign))
  SELECT
  IFF(SIGN>0,'+','-') || TRIM(TO_CHAR(days,'000000000')) || ' ' || TO_CHAR(hours,'00') || ':' || TRIM(TO_CHAR(min,'00')) || ':' || TRIM(TO_CHAR(sec,'00')) || '.' || TRIM(TO_CHAR(millisecond,'00000000'))
  from RESULTS
$$;
```

Copy

##### Oracle[¶](#id89)

```
--Create Table
CREATE TABLE timestampdiff_table (col1 TIMESTAMP, col2 TIMESTAMP);

--Insert data
INSERT INTO timestampdiff_table VALUES ('2000-03-20 22:01:11', '1996-03-20 10:01:11');
INSERT INTO timestampdiff_table VALUES ('1996-03-20 22:01:11', '2000-03-20 10:01:11');
INSERT INTO timestampdiff_table VALUES ('1982-05-11 22:31:19', '1900-01-25 15:21:15');
INSERT INTO timestampdiff_table VALUES ('1999-12-25 01:15:16', '1900-12-11 02:05:16');

--Select
SELECT col1 - col2 FROM timestampdiff_table;
```

Copy

##### Result[¶](#id90)

<!-- prettier-ignore -->
|COL1-COL2|
|---|
|1461 12:0:0.0|
|-1460 12:0:0.0|
|30056 7:10:4.0|
|36172 23:10:0.0|

##### Snowflake[¶](#id91)

```
--Create Table
CREATE OR REPLACE TABLE timestampdiff_table (col1 TIMESTAMP(6),
col2 TIMESTAMP(6)
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

--Insert data
INSERT INTO timestampdiff_table
VALUES ('2000-03-20 22:01:11', '1996-03-20 10:01:11');

INSERT INTO timestampdiff_table
VALUES ('1996-03-20 22:01:11', '2000-03-20 10:01:11');

INSERT INTO timestampdiff_table
VALUES ('1982-05-11 22:31:19', '1900-01-25 15:21:15');

INSERT INTO timestampdiff_table
VALUES ('1999-12-25 01:15:16', '1900-12-11 02:05:16');

--Select
SELECT
PUBLIC.TIMESTAMP_DIFF_UDF( col1, col2) FROM
timestampdiff_table;
```

Copy

##### Result[¶](#id92)

<!-- prettier-ignore -->
|TIMESTAMP_DIFF_UDF( COL1, COL2)|
|---|
|+000001461 12:00:00.00000000|
|-000001460 12:00:00.00000000|
|+000030056 07:10:04.00000000|
|+000036172 23:10:00.00000000|

### Known Issues[¶](#id93)

#### 1. TIMESTAMP format may differ from Oracle[¶](#timestamp-format-may-differ-from-oracle)

The `TIMESTAMP` format may differ from Oracle, please consider the `TIMESTAMP_OUTPUT_FORMAT`
[setting](https://docs.snowflake.com/en/user-guide/date-time-input-output.html#output-formats) when
working with `TIMESTAMP` data types.

### Related EWIs[¶](#id94)

No related EWIs.

## TRUNC (date) UDF[¶](#trunc-date-udf)

### Description[¶](#id95)

> The `TRUNC` (date) function returns `date` with the time portion of the day truncated to the unit
> specified by the format model `fmt`.
> ([Oracle TRUNC(date) SQL Language Reference](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/TRUNC-date.html#GUID-BC82227A-2698-4EC8-8C1A-ABECC64B0E79))

```
TRUNC(date [, fmt ])
```

Copy

Oracle `TRUNC` and Snowflake `TRUNC` function with date arguments have some functional differences.

`TRUNC_UDF` helper will be added to handle the following cases:

1. The format is not supported by Snowflake.

2. The format exists in Snowflake but works differently.

3. The tool cannot determine the datatype of the first argument.

4. The format is provided as a column or expression and not as a literal.

### Custom UDF overloads[¶](#id96)

#### TRUNC_UDF(date)[¶](#trunc-udf-date)

It applies an explicit `DATE`
[cast](https://docs.snowflake.com/en/sql-reference/functions/cast.html) to the input Timestamp.

**Parameters**

1. **INPUT**: The Timestamp with Time Zone
   ([TIMESTAMP_LTZ](https://docs.snowflake.com/en/sql-reference/data-types-datetime.html#timestamp-ltz-timestamp-ntz-timestamp-tz))
   that needs to be truncated.

Warning

The default parameter for the UDF is `TIMESTAMP_LTZ`. It may need to be changed to `TIMESTAMP_TZ` or
`TIMESTAMP_NTZ` to match the default `TIMESTAMP` used by the user.

##### UDF[¶](#id97)

```
CREATE OR REPLACE FUNCTION PUBLIC.TRUNC_UDF(INPUT TIMESTAMP_LTZ)
RETURNS DATE
IMMUTABLE
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}'
AS
$$
    INPUT::DATE
$$;
```

Copy

##### Oracle[¶](#id98)

```
SELECT
TRUNC(
	TO_TIMESTAMP ( '20-Mar-1996 21:01:11 ', 'DD-Mon-YYYY HH24:MI:SS' )
	)
"Date" FROM DUAL;
```

Copy

##### Result[¶](#id99)

<!-- prettier-ignore -->
|Date|
|---|
|1996-03-20 00:00:00.000|

##### Snowflake[¶](#id100)

```
SELECT
TRUNC(
	TO_TIMESTAMP ( '20-Mar-1996 21:01:11 ', 'DD-Mon-YYYY HH24:MI:SS' ), 'DD'
	)
"Date" FROM DUAL;
```

Copy

##### Result[¶](#id101)

<!-- prettier-ignore -->
|DATE|
|---|
|1996-03-20|

#### TRUNC_UDF(date, fmt)[¶](#trunc-udf-date-fmt)

Manually creates a new date using `DATE_FROM_PARTS()`
[function](https://docs.snowflake.com/en/sql-reference/functions/date_from_parts.html#date-from-parts),
depending on the format category used.

**Parameters**

1. **DATE_TO_TRUNC**: The Timestamp with Time Zone
   ([TIMESTAMP_LTZ](https://docs.snowflake.com/en/sql-reference/data-types-datetime.html#timestamp-ltz-timestamp-ntz-timestamp-tz))
   that needs to be truncated.
2. **DATE_FMT**: The date format as a VARCHAR. Same
   [formats that are supported](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/ROUND-and-TRUNC-Date-Functions.html#GUID-8E10AB76-21DA-490F-A389-023B648DDEF8)
   in Oracle.

Warning

The default parameter for the UDF is `TIMESTAMP_LTZ`. It may need to be changed to `TIMESTAMP_TZ` or
`TIMESTAMP_NTZ` to match the default `TIMESTAMP` used by the user.

##### UDF[¶](#id102)

```
CREATE OR REPLACE FUNCTION PUBLIC.TRUNC_UDF(DATE_TO_TRUNC TIMESTAMP_LTZ, DATE_FMT VARCHAR(5))
RETURNS DATE
IMMUTABLE
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}'
AS
$$
CAST(CASE
WHEN UPPER(DATE_FMT) IN ('CC','SCC') THEN DATE_FROM_PARTS(CAST(LEFT(CAST(YEAR(DATE_TO_TRUNC) as CHAR(4)),2) || '01' as INTEGER),1,1)
WHEN UPPER(DATE_FMT) IN ('SYYYY','YYYY','YEAR','SYEAR','YYY','YY','Y') THEN DATE_FROM_PARTS(YEAR(DATE_TO_TRUNC),1,1)
WHEN UPPER(DATE_FMT) IN ('IYYY','IYY','IY','I') THEN
    CASE DAYOFWEEK(DATE_FROM_PARTS(YEAR(DATE_TO_TRUNC),1,1))
         WHEN 0 THEN DATEADD(DAY, 1, DATE_FROM_PARTS(YEAR(DATE_TO_TRUNC),1,1))
         WHEN 1 THEN DATEADD(DAY, 0, DATE_FROM_PARTS(YEAR(DATE_TO_TRUNC),1,1))
         WHEN 2 THEN DATEADD(DAY, -1, DATE_FROM_PARTS(YEAR(DATE_TO_TRUNC),1,1))
         WHEN 3 THEN DATEADD(DAY, -2, DATE_FROM_PARTS(YEAR(DATE_TO_TRUNC),1,1))
         WHEN 4 THEN DATEADD(DAY, -3, DATE_FROM_PARTS(YEAR(DATE_TO_TRUNC),1,1))
         WHEN 5 THEN DATEADD(DAY, 3, DATE_FROM_PARTS(YEAR(DATE_TO_TRUNC),1,1))
         WHEN 6 THEN DATEADD(DAY, 2, DATE_FROM_PARTS(YEAR(DATE_TO_TRUNC),1,1))
    END
WHEN UPPER(DATE_FMT) IN ('MONTH','MON','MM','RM') THEN DATE_FROM_PARTS(YEAR(DATE_TO_TRUNC),MONTH(DATE_TO_TRUNC),1)
WHEN UPPER(DATE_FMT)IN ('Q') THEN DATE_FROM_PARTS(YEAR(DATE_TO_TRUNC),(QUARTER(DATE_TO_TRUNC)-1)*3+1,1)
WHEN UPPER(DATE_FMT) IN ('WW') THEN DATEADD(DAY, 0-MOD(TIMESTAMPDIFF(DAY,DATE_FROM_PARTS(YEAR(DATE_TO_TRUNC),1,1),DATE_TO_TRUNC),7), DATE_TO_TRUNC)
WHEN UPPER(DATE_FMT) IN ('IW') THEN DATEADD(DAY, 0-MOD(TIMESTAMPDIFF(DAY,(CASE DAYOFWEEK(DATE_FROM_PARTS(YEAR(DATE_TO_TRUNC),1,1))
                                                                 WHEN 0 THEN DATEADD(DAY, 1, DATE_FROM_PARTS(YEAR(DATE_TO_TRUNC),1,1))
                                                                 WHEN 1 THEN DATEADD(DAY, 0, DATE_FROM_PARTS(YEAR(DATE_TO_TRUNC),1,1))
                                                                 WHEN 2 THEN DATEADD(DAY, -1, DATE_FROM_PARTS(YEAR(DATE_TO_TRUNC),1,1))
                                                                 WHEN 3 THEN DATEADD(DAY, -2, DATE_FROM_PARTS(YEAR(DATE_TO_TRUNC),1,1))
                                                                 WHEN 4 THEN DATEADD(DAY, -3, DATE_FROM_PARTS(YEAR(DATE_TO_TRUNC),1,1))
                                                                 WHEN 5 THEN DATEADD(DAY, 3, DATE_FROM_PARTS(YEAR(DATE_TO_TRUNC),1,1))
                                                                 WHEN 6 THEN DATEADD(DAY, 2, DATE_FROM_PARTS(YEAR(DATE_TO_TRUNC),1,1))
                                                               END),      DATE_TO_TRUNC),7), DATE_TO_TRUNC)
WHEN UPPER(DATE_FMT) IN ('W') THEN DATEADD(DAY, 0-MOD(TIMESTAMPDIFF(DAY,DATE_FROM_PARTS(YEAR(DATE_TO_TRUNC),MONTH(DATE_TO_TRUNC),1),DATE_TO_TRUNC),7), DATE_TO_TRUNC)
WHEN UPPER(DATE_FMT) IN ('DDD', 'DD','J') THEN DATE_TO_TRUNC
WHEN UPPER(DATE_FMT) IN ('DAY', 'DY','D') THEN DATEADD(DAY, 0-DAYOFWEEK(DATE_TO_TRUNC), DATE_TO_TRUNC)
WHEN UPPER(DATE_FMT) IN ('HH', 'HH12','HH24') THEN DATE_TO_TRUNC
WHEN UPPER(DATE_FMT) IN ('MI') THEN DATE_TO_TRUNC
END AS DATE)
$$
;
```

Copy

### TRUNC format scenarios[¶](#trunc-format-scenarios)

Warning

The results format depends on the DateTime output formats configurated for the database.

#### 1. Natively supported formats[¶](#natively-supported-formats)

##### Oracle[¶](#id103)

```
SELECT TRUNC(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'),'YYYY') FROM DUAL UNION ALL
SELECT TRUNC(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'),'YEAR') FROM DUAL UNION ALL
SELECT TRUNC(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'),'YYY') FROM DUAL UNION ALL
SELECT TRUNC(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'),'YY') FROM DUAL UNION ALL
SELECT TRUNC(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'),'Y') FROM DUAL UNION ALL
SELECT TRUNC(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'),'Q') FROM DUAL UNION ALL
SELECT TRUNC(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'),'MONTH') FROM DUAL UNION ALL
SELECT TRUNC(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'),'MON') FROM DUAL UNION ALL
SELECT TRUNC(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'),'MM') FROM DUAL UNION ALL
SELECT TRUNC(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'),'DD') FROM DUAL UNION ALL
SELECT TRUNC(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'),'HH') FROM DUAL UNION ALL
SELECT TRUNC(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'),'MI') FROM DUAL;
```

Copy

##### Result[¶](#id104)

<!-- prettier-ignore -->
|TRUNC(TO_DATE(‘20/04/2022 13:21:10’,’DD/MM/YYYY HH24:MI:SS’),’YYYY’)|
|---|
|01-JAN-22|
|01-JAN-22|
|01-JAN-22|
|01-JAN-22|
|01-JAN-22|
|01-APR-22|
|01-APR-22|
|01-APR-22|
|01-APR-22|
|20-APR-22|
|20-APR-22|
|20-APR-22|

##### Snowflake[¶](#id105)

```
SELECT TRUNC(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'),'YYYY') FROM DUAL UNION ALL
SELECT TRUNC(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'),'YEAR') FROM DUAL UNION ALL
SELECT TRUNC(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'),'YYY') FROM DUAL UNION ALL
SELECT TRUNC(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'),'YY') FROM DUAL UNION ALL
SELECT TRUNC(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'),'Y') FROM DUAL UNION ALL
SELECT TRUNC(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'),'Q') FROM DUAL UNION ALL
SELECT TRUNC(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'),'MONTH') FROM DUAL UNION ALL
SELECT TRUNC(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'),'MON') FROM DUAL UNION ALL
SELECT TRUNC(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'),'MM') FROM DUAL UNION ALL
SELECT TRUNC(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'),'DD') FROM DUAL UNION ALL
SELECT TRUNC(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'),'HH') FROM DUAL UNION ALL
SELECT TRUNC(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'),'MI') FROM DUAL;
```

Copy

##### Result[¶](#id106)

<!-- prettier-ignore -->
|TRUNC(TO_DATE(‘20/04/2022 13:21:10’,’DD/MM/YYYY HH24:MI:SS’),’YYYY’)|
|---|
|2022-01-01|
|2022-01-01|
|2022-01-01|
|2022-01-01|
|2022-01-01|
|2022-04-01|
|2022-04-01|
|2022-04-01|
|2022-04-01|
|2022-04-20|
|2022-04-20|
|2022-04-20|

#### 2. Formats mapped to another format[¶](#formats-mapped-to-another-format)

##### Oracle[¶](#id107)

```
SELECT TRUNC(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS')) FROM DUAL UNION ALL
SELECT TRUNC(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'),'SYYYY') FROM DUAL UNION ALL
SELECT TRUNC(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'),'SYEAR') FROM DUAL UNION ALL
SELECT TRUNC(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'),'RM') FROM DUAL UNION ALL
SELECT TRUNC(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'),'IW') FROM DUAL UNION ALL
SELECT TRUNC(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'),'DDD') FROM DUAL UNION ALL
SELECT TRUNC(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'),'J') FROM DUAL UNION ALL
SELECT TRUNC(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'),'HH12') FROM DUAL UNION ALL
SELECT TRUNC(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'),'HH24') FROM DUAL;
```

Copy

##### Result[¶](#id108)

<!-- prettier-ignore -->
|TRUNC(TO_DATE(‘20/04/2022 13:21:10’,’DD/MM/YYYY HH24:MI:SS’))|
|---|
|20-APR-22|
|01-JAN-22|
|01-JAN-22|
|01-APR-22|
|18-APR-22|
|20-APR-22|
|20-APR-22|
|20-APR-22|
|20-APR-22|

##### Snowflake[¶](#id109)

```
SELECT TRUNC(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'), 'DD') FROM DUAL UNION ALL
SELECT TRUNC(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'), 'YYYY') FROM DUAL UNION ALL
SELECT TRUNC(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'), 'YEAR') FROM DUAL UNION ALL
SELECT TRUNC(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'), 'MM') FROM DUAL UNION ALL
SELECT TRUNC(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'), 'WK') FROM DUAL UNION ALL
SELECT TRUNC(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'), 'DD') FROM DUAL UNION ALL
SELECT TRUNC(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'), 'D') FROM DUAL UNION ALL
SELECT TRUNC(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'), 'HH') FROM DUAL UNION ALL
SELECT TRUNC(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'), 'HH') FROM DUAL;
```

Copy

##### Result[¶](#id110)

<!-- prettier-ignore -->
|TRUNC(TO_DATE(‘20/04/2022 13:21:10’,’DD/MM/YYYY HH24:MI:SS’), ‘DD’)|
|---|
|2022-04-20|
|2022-01-01|
|2022-01-01|
|2022-04-01|
|2022-04-18|
|2022-04-20|
|2022-04-20|
|2022-04-20|
|2022-04-20|

#### 3. Day formats[¶](#day-formats)

##### Oracle[¶](#id111)

```
SELECT TRUNC(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'),'DAY') FROM DUAL UNION ALL
SELECT TRUNC(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'),'DY') FROM DUAL UNION ALL
SELECT TRUNC(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'),'D') FROM DUAL;
```

Copy

##### Result[¶](#id112)

<!-- prettier-ignore -->
|TRUNC(TO_DATE(‘20/04/2022 13:21:10’,’DD/MM/YYYY HH24:MI:SS’),’DAY’)|
|---|
|17-APR-22|
|17-APR-22|
|17-APR-22|

##### Snowflake[¶](#id113)

```
SELECT
TRUNC_UDF(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'),'DAY') FROM DUAL UNION ALL
SELECT
TRUNC_UDF(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'),'DY') FROM DUAL UNION ALL
SELECT
TRUNC_UDF(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'),'D') FROM DUAL;
```

Copy

##### Result[¶](#id114)

<!-- prettier-ignore -->
|TRUNC_UDF(TO_DATE(‘20/04/2022 13:21:10’,’DD/MM/YYYY HH24:MI:SS’),’DAY’)|
|---|
|2022-04-17|
|2022-04-17|
|2022-04-17|

#### 4. Unsupported formats[¶](#unsupported-formats)

##### Oracle[¶](#id115)

```
SELECT TRUNC(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'),'CC') FROM DUAL UNION ALL
SELECT TRUNC(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'),'SCC') FROM DUAL UNION ALL
SELECT TRUNC(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'),'IYYY') FROM DUAL UNION ALL
SELECT TRUNC(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'),'IY') FROM DUAL UNION ALL
SELECT TRUNC(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'),'I') FROM DUAL UNION ALL
SELECT TRUNC(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'),'WW') FROM DUAL UNION ALL
SELECT TRUNC(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'),'W') FROM DUAL;
```

Copy

##### Result[¶](#id116)

<!-- prettier-ignore -->
|TRUNC(TO_DATE(‘20/04/2022 13:21:10’,’DD/MM/YYYY HH24:MI:SS’),’CC’)|
|---|
|01-JAN-01|
|01-JAN-01|
|03-JAN-22|
|03-JAN-22|
|03-JAN-22|
|16-APR-22|
|15-APR-22|

##### Snowflake[¶](#id117)

```
SELECT
TRUNC_UDF(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'),'CC') FROM DUAL UNION ALL
SELECT
TRUNC_UDF(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'),'SCC') FROM DUAL UNION ALL
SELECT
TRUNC_UDF(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'),'IYYY') FROM DUAL UNION ALL
SELECT
TRUNC_UDF(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'),'IY') FROM DUAL UNION ALL
SELECT
TRUNC_UDF(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'),'I') FROM DUAL UNION ALL
SELECT
TRUNC_UDF(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'),'WW') FROM DUAL UNION ALL
SELECT
TRUNC_UDF(TO_DATE('20/04/2022 13:21:10','DD/MM/YYYY HH24:MI:SS'),'W') FROM DUAL;
```

Copy

##### Result[¶](#id118)

<!-- prettier-ignore -->
|TRUNC_UDF(TO_DATE(‘20/04/2022 13:21:10’,’DD/MM/YYYY HH24:MI:SS’),’CC’)|
|---|
|2001-01-01|
|2001-01-01|
|2022-01-03|
|2022-01-03|
|2022-01-03|
|2022-04-16|
|2022-04-15|

Note

When the `TRUNC` function is used with an unsupported format or a parameter that cannot be handled
by SnowConvert AI. To avoid any issues, the format is replaced with a valid format, or `TRUNC_UDF`
is added.

### Known Issues[¶](#id119)

#### 1. Oracle DATE contains TIMESTAMP[¶](#id120)

Take into consideration that Oracle `DATE` contains an empty `TIMESTAMP` (00:00:00.000), while
Snowflake `DATE` does not.

### Related EWIs[¶](#id121)

No related EWIs.

## TRUNC (number) UDF[¶](#trunc-number-udf)

### Description[¶](#id122)

> The `TRUNC` (number) function returns `n1` truncated to `n2` decimal places. If `n2` is omitted,
> then `n1` is truncated to 0 places. `n2` can be negative to truncate (make zero) `n2` digits left
> of the decimal point.
> ([Oracle TRUNC(number) SQL Language Reference](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/TRUNC-number.html#GUID-911AE7FE-E04A-471D-8B0E-9C50EBEFE07D))

```
TRUNC(n1 [, n2 ])
```

Copy

TRUNC_UDF for numeric values will be added to handle cases **where the first column has an
unrecognized data type.**

Example:

```
SELECT TRUNC(column1) FROM DUAL;
```

Copy

If the definition of `column1` was not provided to the tool. Then the `TRUNC_UDF` will be added and
in execution time, the overload of `TRUNC_UDF` will handle the case if it is a numeric or a date
type.

Please refer to [TRUNC (DATE)](README) section.

The following sections provide the proof that `TRUNC_UDF` will handle perfectly numeric values.

### Custom UDF overloads[¶](#id123)

#### TRUNC_UDF(n1)[¶](#trunc-udf-n1)

It calls Snowflake `TRUNC`
[function](https://docs.snowflake.com/en/sql-reference/functions/trunc.html#truncate-trunc) with the
input number. This overload exists in order to handle the different types of parameter scenarios, in
case that information is not available during the migration.

**Parameters**

1. **INPUT**: The `NUMBER` that needs to be truncated.

##### UDF[¶](#id124)

```
CREATE OR REPLACE FUNCTION PUBLIC.TRUNC_UDF(INPUT NUMBER)
RETURNS INT
IMMUTABLE
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}'
AS
$$
    TRUNC(INPUT)
$$;
```

Copy

##### Oracle[¶](#id125)

```
--TRUNC(NUMBER)
SELECT
	TRUNC ( 1.000001 ),
	TRUNC ( 15.79 ),
	TRUNC ( -975.975 ),
	TRUNC ( 135.135 )
FROM DUAL;
```

Copy

##### Result[¶](#id126)

<!-- prettier-ignore -->
|TRUNC(1.000001)|TRUNC(15.79)|TRUNC(-975.975)|TRUNC(135.135)|
|---|---|---|---|
|1|15|-975|135|

##### Snowflake[¶](#id127)

```
--TRUNC(NUMBER)
SELECT
	TRUNC ( 1.000001 ),
	TRUNC ( 15.79 ),
	TRUNC ( -975.975 ),
	TRUNC ( 135.135 )
FROM DUAL;
```

Copy

##### Result[¶](#id128)

<!-- prettier-ignore -->
|TRUNC_UDF(1.000001)|TRUNC_UDF(15.79)|TRUNC_UDF(-975.975)|TRUNC_UDF(135.135)|
|---|---|---|---|
|1|15|-975|135|

#### TRUNC_UDF(n1, n2)[¶](#trunc-udf-n1-n2)

It calls Snowflake `TRUNC`
[function](https://docs.snowflake.com/en/sql-reference/functions/trunc.html#truncate-trunc) with the
input number and the scale. This overload exists in order to handle the different types of parameter
scenarios, in case that information is not available during the migration.

**Parameters**

1. **INPUT**: The `NUMBER` that needs to be truncated.
2. **SCALE**: Represents the number of digits the output will include after the decimal point.

##### UDF[¶](#id129)

```
CREATE OR REPLACE FUNCTION PUBLIC.TRUNC_UDF(INPUT NUMBER, SCALE NUMBER)
RETURNS INT
IMMUTABLE
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}'
AS
$$
    TRUNC(INPUT, SCALE)
$$;
```

Copy

##### Oracle[¶](#id130)

```
--TRUNC(NUMBER, SCALE)
SELECT
	TRUNC ( 1.000001, -2 ),
	TRUNC ( 1.000001, -1 ),
	TRUNC ( 1.000001, 0 ),
	TRUNC ( 1.000001, 1 ),
	TRUNC ( 1.000001, 2 ),
	TRUNC ( 15.79, -2),
	TRUNC ( 15.79, -1),
	TRUNC ( 15.79, 0),
	TRUNC ( 15.79, 1 ),
	TRUNC ( 15.79, 50 ),
	TRUNC ( -9.6, -2 ),
	TRUNC ( -9.6, -1 ),
	TRUNC ( -9.6, 0 ),
	TRUNC ( -9.6, 1 ),
	TRUNC ( -9.6, 2 ),
	TRUNC ( -975.975, -3 ),
	TRUNC ( -975.975, -2 ),
	TRUNC ( -975.975, -1 ),
	TRUNC ( -975.975, 0 ),
	TRUNC ( -975.975, 1 ),
	TRUNC ( -975.975, 2 ),
	TRUNC ( -975.975, 3 ),
	TRUNC ( -975.975, 5 ),
	TRUNC ( 135.135, -10 ),
	TRUNC ( 135.135, -2 ),
	TRUNC ( 135.135, 0 ),
	TRUNC ( 135.135, 1 ),
	TRUNC ( 135.135, 2 ),
	TRUNC ( 135.135, 3 ),
	TRUNC ( 135.135, 5 )
FROM DUAL;
```

Copy

##### Result[¶](#id131)

<!-- prettier-ignore -->
|TRUNC(1.000001,-2)|TRUNC(1.000001,-1)|TRUNC(1.000001,0)|TRUNC(1.000001,1)|TRUNC(1.000001,2)|TRUNC(15.79,-2)|TRUNC(15.79,-1)|TRUNC(15.79,0)|TRUNC(15.79,1)|TRUNC(15.79,50)|TRUNC(-9.6,-2)|TRUNC(-9.6,-1)|TRUNC(-9.6,0)|TRUNC(-9.6,1)|TRUNC(-9.6,2)|TRUNC(-975.975,-3)|TRUNC(-975.975,-2)|TRUNC(-975.975,-1)|TRUNC(-975.975,0)|TRUNC(-975.975,1)|TRUNC(-975.975,2)|TRUNC(-975.975,3)|TRUNC(-975.975,5)|TRUNC(135.135,-10)|TRUNC(135.135,-2)|TRUNC(135.135,0)|TRUNC(135.135,1)|TRUNC(135.135,2)|TRUNC(135.135,3)|TRUNC(135.135,5)|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|0|0|1|1|1|0|10|15|15.7|15.79|0|0|-9|-9.6|-9.6|0|-900|-970|-975|-975.9|-975.97|-975.975|-975.975|0|100|135|135.1|135.13|135.135|135.135|

##### Snowflake[¶](#id132)

```
--TRUNC(NUMBER, SCALE)
SELECT
	TRUNC ( 1.000001, -2 ),
	TRUNC ( 1.000001, -1 ),
	TRUNC ( 1.000001, 0 ),
	TRUNC ( 1.000001, 1 ),
	TRUNC ( 1.000001, 2 ),
	TRUNC ( 15.79, -2),
	TRUNC ( 15.79, -1),
	TRUNC ( 15.79, 0),
	TRUNC ( 15.79, 1 ),
	TRUNC ( 15.79, 50 ),
	TRUNC ( -9.6, -2 ),
	TRUNC ( -9.6, -1 ),
	TRUNC ( -9.6, 0 ),
	TRUNC ( -9.6, 1 ),
	TRUNC ( -9.6, 2 ),
	TRUNC ( -975.975, -3 ),
	TRUNC ( -975.975, -2 ),
	TRUNC ( -975.975, -1 ),
	TRUNC ( -975.975, 0 ),
	TRUNC ( -975.975, 1 ),
	TRUNC ( -975.975, 2 ),
	TRUNC ( -975.975, 3 ),
	TRUNC ( -975.975, 5 ),
	TRUNC ( 135.135, -10 ),
	TRUNC ( 135.135, -2 ),
	TRUNC ( 135.135, 0 ),
	TRUNC ( 135.135, 1 ),
	TRUNC ( 135.135, 2 ),
	TRUNC ( 135.135, 3 ),
	TRUNC ( 135.135, 5 )
FROM DUAL;
```

Copy

##### Result[¶](#id133)

<!-- prettier-ignore -->
|TRUNC_UDF ( 1.000001, -2 )|TRUNC_UDF ( 1.000001, -1 )|TRUNC_UDF ( 1.000001, 0 )|TRUNC_UDF ( 1.000001, 1 )|TRUNC_UDF ( 1.000001, 2 )|TRUNC_UDF ( 15.79, -2)|TRUNC_UDF ( 15.79, -1)|TRUNC_UDF ( 15.79, 0)|TRUNC_UDF ( 15.79, 1 )|TRUNC_UDF ( 15.79, 50 )|TRUNC_UDF ( -9.6, -2 )|TRUNC_UDF ( -9.6, -1 )|TRUNC_UDF ( -9.6, 0 )|TRUNC_UDF ( -9.6, 1 )|TRUNC_UDF ( -9.6, 2 )|TRUNC_UDF ( -975.975, -3 )|TRUNC_UDF ( -975.975, -2 )|TRUNC_UDF ( -975.975, -1 )|TRUNC_UDF ( -975.975, 0 )|TRUNC_UDF ( -975.975, 1 )|TRUNC_UDF ( -975.975, 2 )|TRUNC_UDF ( -975.975, 3 )|TRUNC_UDF ( -975.975, 5 )|TRUNC_UDF ( 135.135, -10 )|TRUNC_UDF ( 135.135, -2 )|TRUNC_UDF ( 135.135, 0 )|TRUNC_UDF ( 135.135, 1 )|TRUNC_UDF ( 135.135, 2 )|TRUNC_UDF ( 135.135, 3 )|TRUNC_UDF ( 135.135, 5 )|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|0|0|1|1.0|1.00|0|10|15|15.7|15.79|0|0|-9|-9.6|-9.6|0|-900|-970|-975|-975.9|-975.97|-975.975|-975.975|0|100|135|135.1|135.13|135.135|135.135|

### Known Issues[¶](#id134)

No issues were found.

### Related EWIs[¶](#id135)

No related EWIs.

# SnowConvert AI - Oracle - INTERVAL UDFs[¶](#snowconvert-ai-oracle-interval-udfs)

## Necessary code to run INTERVAL UDFs[¶](#necessary-code-to-run-interval-udfs)

In order to run any of the interval UDFs, it is necessary to run the following code before:

```
CREATE OR REPLACE FUNCTION PUBLIC.INTERVAL2MONTHS_UDF
(INPUT_VALUE VARCHAR())
RETURNS INTEGER
IMMUTABLE
AS
$$
CASE WHEN SUBSTR(INPUT_VALUE,1,1) = '-' THEN
   12 * CAST(SUBSTR(INPUT_VALUE,1 , POSITION('-', INPUT_VALUE,2)-1) AS INTEGER)
   - CAST(SUBSTR(INPUT_VALUE,POSITION('-', INPUT_VALUE)+1) AS INTEGER)
ELSE
   12 * CAST(SUBSTR(INPUT_VALUE,1 , POSITION('-', INPUT_VALUE,2)-1) AS INTEGER)
   + CAST(SUBSTR(INPUT_VALUE,POSITION('-', INPUT_VALUE)+1) AS INTEGER)
END
$$;

CREATE OR REPLACE FUNCTION PUBLIC.INTERVAL2SECONDS_UDF
(INPUT_PART VARCHAR(30), INPUT_VALUE VARCHAR())
RETURNS DECIMAL(20,6)
IMMUTABLE
AS
$$
CASE WHEN SUBSTR(INPUT_VALUE,1,1) = '-' THEN
   DECODE(INPUT_PART,
           'DAY',              86400 * INPUT_VALUE,
           'DAY TO HOUR',      86400 * CAST(SUBSTR(INPUT_VALUE, 1, POSITION(' ', INPUT_VALUE)-1) AS DECIMAL(10,0))
                               - 3600 * CAST(SUBSTR(INPUT_VALUE, POSITION(' ', INPUT_VALUE)+1) AS DECIMAL(10,0)),
           'DAY TO MINUTE',    86400 * CAST(SUBSTR(INPUT_VALUE, 1, POSITION(' ', INPUT_VALUE)-1) AS INTEGER)
                               - 3600 * CAST(SUBSTR(INPUT_VALUE, POSITION(' ', INPUT_VALUE)+1, POSITION(':', INPUT_VALUE)-POSITION(' ', INPUT_VALUE)-1) AS INTEGER)
                               - 60 * CAST(SUBSTR(INPUT_VALUE, POSITION(':', INPUT_VALUE)+1) AS INTEGER),
           'DAY TO SECOND',    86400 * CAST(SUBSTR(INPUT_VALUE, 1, POSITION(' ', INPUT_VALUE)-1) AS INTEGER)
                               - 3600 * CAST(SUBSTR(INPUT_VALUE, POSITION(' ', INPUT_VALUE)+1, POSITION(':', INPUT_VALUE)-POSITION(' ', INPUT_VALUE)-1) AS INTEGER)
                               - 60 * CAST(SUBSTR(INPUT_VALUE, POSITION(':', INPUT_VALUE)+1, POSITION(':', INPUT_VALUE, POSITION(':', INPUT_VALUE)+1) - POSITION(':', INPUT_VALUE) - 1) AS INTEGER)
                               - CAST(SUBSTR(INPUT_VALUE,POSITION(':', INPUT_VALUE, POSITION(':', INPUT_VALUE)+1)+1) AS DECIMAL(10,6)),
           'DAY TO SECOND(3)',  86400 * CAST(SUBSTR(INPUT_VALUE, 1, POSITION(' ', INPUT_VALUE)-1) AS INTEGER)
                               - 3600 * CAST(SUBSTR(INPUT_VALUE, POSITION(' ', INPUT_VALUE)+1, POSITION(':', INPUT_VALUE)-POSITION(' ', INPUT_VALUE)-1) AS INTEGER)
                               - 60 * CAST(SUBSTR(INPUT_VALUE, POSITION(':', INPUT_VALUE)+1, POSITION(':', INPUT_VALUE, POSITION(':', INPUT_VALUE)+1) - POSITION(':', INPUT_VALUE) - 1) AS INTEGER)
                               - CAST(SUBSTR(INPUT_VALUE,POSITION(':', INPUT_VALUE, POSITION(':', INPUT_VALUE)+1)+1) AS DECIMAL(10,6)),
           'HOUR(3)',          3600 * INPUT_VALUE,
           'HOUR',             3600 * INPUT_VALUE,
           'HOUR TO MINUTE',   3600 * CAST(SUBSTR(INPUT_VALUE,1 , POSITION(':', INPUT_VALUE)-1) AS INTEGER)
                               - 60 * CAST(SUBSTR(INPUT_VALUE,POSITION(':', INPUT_VALUE)+1) AS INTEGER),
           'HOUR TO SECOND',   3600 * CAST(SUBSTR(INPUT_VALUE, 1, POSITION(':', INPUT_VALUE)-POSITION(' ', INPUT_VALUE)-1) AS INTEGER)
                               - 60 * CAST(SUBSTR(INPUT_VALUE, POSITION(':', INPUT_VALUE)+1, POSITION(':', INPUT_VALUE, POSITION(':', INPUT_VALUE)+1) - POSITION(':', INPUT_VALUE) - 1) AS INTEGER)
                               - CAST(SUBSTR(INPUT_VALUE,POSITION(':', INPUT_VALUE, POSITION(':', INPUT_VALUE)+1)+1) AS DECIMAL(10,6)),
           'MINUTE',           60 * INPUT_VALUE,
           'MINUTE TO SECOND', 60 * CAST(SUBSTR(INPUT_VALUE, 1, POSITION(':', INPUT_VALUE)-POSITION(' ', INPUT_VALUE)-1) AS INTEGER)
                               - CAST(SUBSTR(INPUT_VALUE, POSITION(':', INPUT_VALUE)+1) AS DECIMAL(10,6)),
           'SECOND(2,3)',      INPUT_VALUE,
           'SECOND',           INPUT_VALUE
            )
ELSE
   DECODE(INPUT_PART,
           'DAY',              86400 * INPUT_VALUE,
           'DAY TO HOUR',      86400 * CAST(SUBSTR(INPUT_VALUE, 1, POSITION(' ', INPUT_VALUE)-1) AS INTEGER)
                               + 3600 * CAST(SUBSTR(INPUT_VALUE, POSITION(' ', INPUT_VALUE)+1) AS INTEGER),
           'DAY TO MINUTE',    86400 * CAST(SUBSTR(INPUT_VALUE, 1, POSITION(' ', INPUT_VALUE)-1) AS INTEGER)
                               + 3600 * CAST(SUBSTR(INPUT_VALUE, POSITION(' ', INPUT_VALUE)+1, POSITION(':', INPUT_VALUE)-POSITION(' ', INPUT_VALUE)-1) AS INTEGER)
                               + 60 * CAST(SUBSTR(INPUT_VALUE, POSITION(':', INPUT_VALUE)+1) AS INTEGER),
           'DAY TO SECOND',    86400 * CAST(SUBSTR(INPUT_VALUE, 1, POSITION(' ', INPUT_VALUE)-1) AS INTEGER)
                               + 3600 * CAST(SUBSTR(INPUT_VALUE, POSITION(' ', INPUT_VALUE)+1, POSITION(':', INPUT_VALUE)-POSITION(' ', INPUT_VALUE)-1) AS INTEGER)
                               + 60 * CAST(SUBSTR(INPUT_VALUE, POSITION(':', INPUT_VALUE)+1, POSITION(':', INPUT_VALUE, POSITION(':', INPUT_VALUE)+1) - POSITION(':', INPUT_VALUE) - 1) AS INTEGER)
                               + CAST(SUBSTR(INPUT_VALUE,POSITION(':', INPUT_VALUE, POSITION(':', INPUT_VALUE)+1)+1) AS DECIMAL(10,6)),
           'DAY TO SECOND(3)',    86400 * CAST(SUBSTR(INPUT_VALUE, 1, POSITION(' ', INPUT_VALUE)-1) AS INTEGER)
                               + 3600 * CAST(SUBSTR(INPUT_VALUE, POSITION(' ', INPUT_VALUE)+1, POSITION(':', INPUT_VALUE)-POSITION(' ', INPUT_VALUE)-1) AS INTEGER)
                               + 60 * CAST(SUBSTR(INPUT_VALUE, POSITION(':', INPUT_VALUE)+1, POSITION(':', INPUT_VALUE, POSITION(':', INPUT_VALUE)+1) - POSITION(':', INPUT_VALUE) - 1) AS INTEGER)
                               + CAST(SUBSTR(INPUT_VALUE,POSITION(':', INPUT_VALUE, POSITION(':', INPUT_VALUE)+1)+1) AS DECIMAL(10,6)),
           'HOUR(3)',          3600 * INPUT_VALUE,
           'HOUR',             3600 * INPUT_VALUE,
           'HOUR TO MINUTE',   3600 * CAST(SUBSTR(INPUT_VALUE,1 , POSITION(':', INPUT_VALUE)-1) AS INTEGER)
                               + 60 * CAST(SUBSTR(INPUT_VALUE,POSITION(':', INPUT_VALUE)+1) AS INTEGER),
           'HOUR TO SECOND',   3600 * CAST(SUBSTR(INPUT_VALUE, 1, POSITION(':', INPUT_VALUE)-POSITION(' ', INPUT_VALUE)-1) AS INTEGER)
                               + 60 * CAST(SUBSTR(INPUT_VALUE, POSITION(':', INPUT_VALUE)+1, POSITION(':', INPUT_VALUE, POSITION(':', INPUT_VALUE)+1) - POSITION(':', INPUT_VALUE) - 1) AS INTEGER)
                               + CAST(SUBSTR(INPUT_VALUE,POSITION(':', INPUT_VALUE, POSITION(':', INPUT_VALUE)+1)+1) AS DECIMAL(10,6)),
           'MINUTE',           60 * INPUT_VALUE,
           'MINUTE TO SECOND', 60 * CAST(SUBSTR(INPUT_VALUE, 1, POSITION(':', INPUT_VALUE)-POSITION(' ', INPUT_VALUE)-1) AS INTEGER)
                               + CAST(SUBSTR(INPUT_VALUE, POSITION(':', INPUT_VALUE)+1) AS DECIMAL(10,6)),
           'SECOND(2,3)',      INPUT_VALUE,
           'SECOND',           INPUT_VALUE
        )
END
$$;
```

Copy

## DATEADD UDF INTERVAL[¶](#dateadd-udf-interval)

Note

Some parts in the output code are omitted for clarity reasons.

### Description[¶](#id136)

This UDF is used to resolve operations with intervals like:

- INTERVAL + DATE
- INTERVAL + TIMESTAMP
- DATE + INTERVAL
- DATE + TIMESTAMP
- INTERVAL + UNKNOWN
- UNKNOWN + INTERVAL

Note

An UNKNOWN type is a column or expression whose type could not be resolved by Snow Convert, it use
to happen when the DDLs for tables are not included in the migration or when there is an expression
or subquery that can return different data types.

### Custom UDF overloads[¶](#id137)

#### DATEADD_UDF(string, date)[¶](#dateadd-udf-string-date)

**Parameters**

1. **INTERVAL_VALUE**: The interval `String` of the operation.
2. **D**: The `DATE` where the interval will be added.

##### UDF[¶](#id138)

```
CREATE OR REPLACE FUNCTION PUBLIC.DATEADD_UDF(INTERVAL_VALUE STRING,D DATE)
RETURNS DATE
LANGUAGE SQL
IMMUTABLE
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}'
AS
$$
WITH VARS(INPUT_VALUE, INPUT_PART) AS (
SELECT SUBSTR(INTERVAL_VALUE,11,POSITION('''',INTERVAL_VALUE,11)-11),
       TRIM(SUBSTR(INTERVAL_VALUE,POSITION('''',INTERVAL_VALUE,11)+1)))
SELECT

    CASE WHEN INPUT_PART='YEAR(2) TO MONTH' OR INPUT_PART='YEAR(4) TO MONTH' THEN
        DATEADD(MONTHS,PUBLIC.INTERVAL_TO_MONTHS_UDF(INPUT_VALUE),D)
    WHEN INPUT_PART='MONTH' THEN
        DATEADD(MONTHS,TO_NUMBER(INPUT_VALUE),D)
    ELSE
        DATEADD(MICROSECONDS,1000000*PUBLIC.INTERVAL_TO_SECONDS_UDF(INPUT_PART, INPUT_VALUE),D)::DATE
    END CASE
FROM VARS
$$;
```

Copy

#### DATEADD_UDF(date, string)[¶](#dateadd-udf-date-string)

**Parameters**

1. **D**: The `DATE` where the interval will be added.
2. **INTERVAL_VALUE**: The interval `String` of the operation.

##### UDF[¶](#id139)

```
CREATE OR REPLACE FUNCTION PUBLIC.DATEADD_UDF(D DATE, INTERVAL_VALUE STRING)
RETURNS DATE
LANGUAGE SQL
IMMUTABLE
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}'
AS
$$
WITH VARS(INPUT_VALUE, INPUT_PART) AS (
SELECT SUBSTR(INTERVAL_VALUE,11,POSITION('''',INTERVAL_VALUE,11)-11),
       TRIM(SUBSTR(INTERVAL_VALUE,POSITION('''',INTERVAL_VALUE,11)+1)))
SELECT

    CASE WHEN INPUT_PART='YEAR(2) TO MONTH' OR INPUT_PART='YEAR(4) TO MONTH' THEN
        DATEADD(MONTHS,PUBLIC.INTERVAL_TO_MONTHS_UDF(INPUT_VALUE),D)
    WHEN INPUT_PART='MONTH' THEN
        DATEADD(MONTHS,TO_NUMBER(INPUT_VALUE),D)
    ELSE
        DATEADD(MICROSECONDS,1000000*PUBLIC.INTERVAL_TO_SECONDS_UDF(INPUT_PART, INPUT_VALUE),D)::DATE
    END CASE
FROM VARS
$$;
```

Copy

#### DATEADD_UDF(string, timestamp)[¶](#dateadd-udf-string-timestamp)

**Parameters**

1. **INTERVAL_VALUE**: The interval `String` of the operation.
2. **D**: The `TIMESTAMP` where the interval will be added.

##### UDF[¶](#id140)

```
CREATE OR REPLACE FUNCTION PUBLIC.DATEADD_UDF(INTERVAL_VALUE STRING,D TIMESTAMP)
RETURNS TIMESTAMP
LANGUAGE SQL
IMMUTABLE
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}'
AS
$$
WITH VARS(INPUT_VALUE, INPUT_PART) AS (
SELECT SUBSTR(INTERVAL_VALUE,11,POSITION('''',INTERVAL_VALUE,11)-11),
       TRIM(SUBSTR(INTERVAL_VALUE,POSITION('''',INTERVAL_VALUE,11)+1)))
SELECT

    CASE WHEN INPUT_PART='YEAR(2) TO MONTH' OR INPUT_PART='YEAR(4) TO MONTH' THEN
        DATEADD(MONTHS,PUBLIC.INTERVAL_TO_MONTHS_UDF(INPUT_VALUE),D)
    WHEN INPUT_PART='MONTH' THEN
        DATEADD(MONTHS,TO_NUMBER(INPUT_VALUE),D)
    ELSE
        DATEADD(MICROSECONDS,1000000*PUBLIC.INTERVAL_TO_SECONDS_UDF(INPUT_PART, INPUT_VALUE),D)
    END CASE
FROM VARS
$$;
```

Copy

#### DATEADD_UDF(timestamp, string)[¶](#dateadd-udf-timestamp-string)

**Parameters**

1. **D**: The `TIMESTAMP` where the interval will be added.
2. **INTERVAL_VALUE**: The interval `String` of the operation.

##### UDF[¶](#id141)

```
CREATE OR REPLACE FUNCTION PUBLIC.DATEADD_UDF(D TIMESTAMP, INTERVAL_VALUE STRING)
RETURNS TIMESTAMP
LANGUAGE SQL
IMMUTABLE
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}'
AS
$$
WITH VARS(INPUT_VALUE, INPUT_PART) AS (
SELECT SUBSTR(INTERVAL_VALUE,11,POSITION('''',INTERVAL_VALUE,11)-11),
       TRIM(SUBSTR(INTERVAL_VALUE,POSITION('''',INTERVAL_VALUE,11)+1)))
SELECT

    CASE WHEN INPUT_PART='YEAR(2) TO MONTH' OR INPUT_PART='YEAR(4) TO MONTH' THEN
        DATEADD(MONTHS,PUBLIC.INTERVAL_TO_MONTHS_UDF(INPUT_VALUE),D)
    WHEN INPUT_PART='MONTH' THEN
        DATEADD(MONTHS,TO_NUMBER(INPUT_VALUE),D)
    ELSE
        DATEADD(MICROSECONDS,1000000*PUBLIC.INTERVAL_TO_SECONDS_UDF(INPUT_PART, INPUT_VALUE),D)
    END CASE
FROM VARS
$$;
```

Copy

#### Usage example[¶](#id142)

Note

**`--disableDateAsTimestamp`**

Flag to indicate whether `SYSDATE` should be transformed into `CURRENT_DATE` _or_
`CURRENT_TIMESTAMP`. This will also affect all `DATE` columns that will be transformed to
`TIMESTAMP`.

##### Oracle[¶](#id143)

```
-- DROP TABLE UNKNOWN_TABLE;
-- CREATE TABLE UNKNOWN_TABLE(Unknown timestamp);
-- INSERT  INTO UNKNOWN_TABLE VALUES (TO_TIMESTAMP('01/10/09, 12:00 P.M.', 'dd/mm/yy, hh:mi P.M.'));

CREATE TABLE TIMES(
AsTimeStamp TIMESTAMP,
AsTimestampTwo TIMESTAMP,
AsDate DATE,
AsDateTwo DATE
);

INSERT INTO TIMES VALUES (
TO_TIMESTAMP('05/11/21, 11:00 A.M.', 'dd/mm/yy, hh:mi A.M.'),
TO_TIMESTAMP('05/11/21, 10:00 A.M.', 'dd/mm/yy, hh:mi A.M.'),
TO_DATE('06/11/21', 'dd/mm/yy'),
TO_DATE('05/11/21', 'dd/mm/yy'));

SELECT
 AsTimeStamp+INTERVAL '1-1' YEAR(2) TO MONTH,
 AsTimeStamp+INTERVAL '2-1' YEAR(4) TO MONTH,
 AsTimeStamp+INTERVAL '1' MONTH,
 AsTimeStamp+INTERVAL '2' MONTH,
 AsDate+INTERVAL '1-1' YEAR(2) TO MONTH,
 AsDate+INTERVAL '2-1' YEAR(4) TO MONTH,
 AsDate+INTERVAL '1' MONTH,
 AsDate+INTERVAL '2' MONTH,
 Unknown+INTERVAL '1 01:00:00.222' DAY TO SECOND(3),
 Unknown+INTERVAL '1 01:10' DAY TO MINUTE,
 Unknown+INTERVAL '1 1' DAY TO HOUR,
 INTERVAL '1' MONTH+AsTimeStamp,
 INTERVAL '1' MONTH+AsDate,
 INTERVAL '1' MONTH+Unknown,
 INTERVAL '2' MONTH+AsTimeStamp,
 INTERVAL '2' MONTH+AsDate,
 INTERVAL '2' MONTH+Unknown
FROM TIMES, UNKNOWN_TABLE;
```

Copy

##### Results[¶](#id144)

```
<!-- prettier-ignore -->
|ASTIMESTAMP+INTERVAL'1-1'YEAR(2)TOMONTH|ASTIMESTAMP+INTERVAL'2-1'YEAR(4)TOMONTH|ASTIMESTAMP+INTERVAL'1'MONTH|ASTIMESTAMP+INTERVAL'2'MONTH|ASDATE+INTERVAL'1-1'YEAR(2)TOMONTH|ASDATE+INTERVAL'2-1'YEAR(4)TOMONTH|ASDATE+INTERVAL'1'MONTH|ASDATE+INTERVAL'2'MONTH|UNKNOWN+INTERVAL'101:00:00.222'DAYTOSECOND(3)|UNKNOWN+INTERVAL'101:10'DAYTOMINUTE|UNKNOWN+INTERVAL'11'DAYTOHOUR|INTERVAL'1'MONTH+ASTIMESTAMP|INTERVAL'1'MONTH+ASDATE|INTERVAL'1'MONTH+UNKNOWN|INTERVAL'2'MONTH+ASTIMESTAMP|INTERVAL'2'MONTH+ASDATE|INTERVAL'2'MONTH+UNKNOWN|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|2022-12-05 11:00:00.000|2023-12-05 11:00:00.000|2021-12-05 11:00:00.000|2022-01-05 11:00:00.000|2022-12-06 00:00:00.000|2023-12-06 00:00:00.000|2021-12-06 00:00:00.000|2022-01-06 00:00:00.000|2009-10-02 13:00:00.222|2009-10-02 13:10:00.000|2009-10-02 13:00:00.000|2021-12-05 11:00:00.000|2021-12-06 00:00:00.000|2009-11-01 12:00:00.000|2022-01-05 11:00:00.000|2022-01-06 00:00:00.000|2009-12-01 12:00:00.000|
```

Copy

##### Snowflake[¶](#id145)

Note

This configuration was used in Snowflake

```
ALTER SESSION SET TIMESTAMP_NTZ_OUTPUT_FORMAT= 'DD-MON-YY HH.MI.SS.FF6 AM';
ALTER SESSION SET DATE_OUTPUT_FORMAT= 'DD-MON-YY';
```

Copy

```
-- DROP TABLE UNKNOWN_TABLE;
-- CREATE TABLE UNKNOWN_TABLE(Unknown timestamp);
-- INSERT  INTO UNKNOWN_TABLE VALUES (TO_TIMESTAMP('01/10/09, 12:00 P.M.', 'dd/mm/yy, hh:mi P.M.'));
CREATE OR REPLACE TABLE TIMES (
 AsTimeStamp TIMESTAMP(6),
 AsTimestampTwo TIMESTAMP(6),
 AsDate TIMESTAMP /*** SSC-FDM-OR0042 - DATE TYPE COLUMN HAS A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/,
 AsDateTwo TIMESTAMP /*** SSC-FDM-OR0042 - DATE TYPE COLUMN HAS A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/
 )
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
;

INSERT INTO TIMES
VALUES (
TO_TIMESTAMP('05/11/21, 11:00 A.M.', 'dd/mm/yy, hh:mi A.M.'),
TO_TIMESTAMP('05/11/21, 10:00 A.M.', 'dd/mm/yy, hh:mi A.M.'),
TO_DATE('06/11/21', 'dd/mm/yy'),
TO_DATE('05/11/21', 'dd/mm/yy'));

--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "UNKNOWN_TABLE" **

SELECT
 !!!RESOLVE EWI!!! /*** SSC-EWI-OR0095 - OPERATION BETWEEN INTERVAL TYPE AND DATE TYPE NOT SUPPORTED ***/!!!
 AsTimeStamp + INTERVAL '1y, 1mm',
 !!!RESOLVE EWI!!! /*** SSC-EWI-OR0095 - OPERATION BETWEEN INTERVAL TYPE AND DATE TYPE NOT SUPPORTED ***/!!!
 AsTimeStamp + INTERVAL '2y, 1mm',
 !!!RESOLVE EWI!!! /*** SSC-EWI-OR0095 - OPERATION BETWEEN INTERVAL TYPE AND DATE TYPE NOT SUPPORTED ***/!!!
 AsTimeStamp + INTERVAL '1 month',
 !!!RESOLVE EWI!!! /*** SSC-EWI-OR0095 - OPERATION BETWEEN INTERVAL TYPE AND DATE TYPE NOT SUPPORTED ***/!!!
 AsTimeStamp + INTERVAL '2 month',
 AsDate+ INTERVAL '1y, 1mm',
 AsDate+ INTERVAL '2y, 1mm',
 AsDate+ INTERVAL '1 month',
 AsDate+ INTERVAL '2 month',
 !!!RESOLVE EWI!!! /*** SSC-EWI-OR0036 - TYPES RESOLUTION ISSUES, ARITHMETIC OPERATION '+' MAY NOT BEHAVE CORRECTLY BETWEEN Unknown AND Interval ***/!!!
 Unknown + INTERVAL '1d, 01h, 00m, 00s, 222ms',
 !!!RESOLVE EWI!!! /*** SSC-EWI-OR0036 - TYPES RESOLUTION ISSUES, ARITHMETIC OPERATION '+' MAY NOT BEHAVE CORRECTLY BETWEEN Unknown AND Interval ***/!!!
 Unknown + INTERVAL '1d, 01h, 10m',
 !!!RESOLVE EWI!!! /*** SSC-EWI-OR0036 - TYPES RESOLUTION ISSUES, ARITHMETIC OPERATION '+' MAY NOT BEHAVE CORRECTLY BETWEEN Unknown AND Interval ***/!!!
 Unknown + INTERVAL '1d, 1h',
 !!!RESOLVE EWI!!! /*** SSC-EWI-OR0095 - OPERATION BETWEEN INTERVAL TYPE AND DATE TYPE NOT SUPPORTED ***/!!!
 AsTimeStamp + INTERVAL '1 month',
 !!!RESOLVE EWI!!! /*** SSC-EWI-OR0095 - OPERATION BETWEEN INTERVAL TYPE AND DATE TYPE NOT SUPPORTED ***/!!!
 AsDate + INTERVAL '1 month',
 !!!RESOLVE EWI!!! /*** SSC-EWI-OR0036 - TYPES RESOLUTION ISSUES, ARITHMETIC OPERATION '+' MAY NOT BEHAVE CORRECTLY BETWEEN Unknown AND Interval ***/!!!
 Unknown + INTERVAL '1 month',
 !!!RESOLVE EWI!!! /*** SSC-EWI-OR0095 - OPERATION BETWEEN INTERVAL TYPE AND DATE TYPE NOT SUPPORTED ***/!!!
 AsTimeStamp + INTERVAL '2 month',
 !!!RESOLVE EWI!!! /*** SSC-EWI-OR0095 - OPERATION BETWEEN INTERVAL TYPE AND DATE TYPE NOT SUPPORTED ***/!!!
 AsDate + INTERVAL '2 month',
 !!!RESOLVE EWI!!! /*** SSC-EWI-OR0036 - TYPES RESOLUTION ISSUES, ARITHMETIC OPERATION '+' MAY NOT BEHAVE CORRECTLY BETWEEN Unknown AND Interval ***/!!!
 Unknown + INTERVAL '2 month'
FROM
 TIMES,
 UNKNOWN_TABLE;
```

Copy

##### Results[¶](#id146)

```
<!-- prettier-ignore -->
|DATEADD_UDF(ASTIMESTAMP,'INTERVAL ''1-1'' YEAR(2) TO MONTH')|DATEADD_UDF(ASTIMESTAMP,'INTERVAL ''2-1'' YEAR(4) TO MONTH')|DATEADD_UDF(ASTIMESTAMP,'INTERVAL ''1'' MONTH')|DATEADD_UDF(ASTIMESTAMP,'INTERVAL ''2'' MONTH')|DATEADD_UDF(ASDATE,'INTERVAL ''1-1'' YEAR(2) TO MONTH')|DATEADD_UDF(ASDATE,'INTERVAL ''2-1'' YEAR(4) TO MONTH')|DATEADD_UDF(ASDATE,'INTERVAL ''1'' MONTH')|DATEADD_UDF(ASDATE,'INTERVAL ''2'' MONTH')|DATEADD_UDF(UNKNOWN,'INTERVAL ''1 01:00:00.222'' DAY TO SECOND(3)')|DATEADD_UDF(UNKNOWN,'INTERVAL ''1 01:10'' DAY TO MINUTE')|DATEADD_UDF(UNKNOWN,'INTERVAL ''1 1'' DAY TO HOUR')|DATEADD_UDF('INTERVAL ''1'' MONTH',ASTIMESTAMP)|DATEADD_UDF('INTERVAL ''1'' MONTH',ASDATE)|DATEADD_UDF('INTERVAL ''1'' MONTH',UNKNOWN)|DATEADD_UDF('INTERVAL ''2'' MONTH',ASTIMESTAMP)|DATEADD_UDF('INTERVAL ''2'' MONTH',ASDATE)|DATEADD_UDF('INTERVAL ''2'' MONTH',UNKNOWN)|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|2022-12-05 11:00:00.000|2023-12-05 11:00:00.000|2021-12-05 11:00:00.000|2022-01-05 11:00:00.000|2022-12-06|2023-12-06|2021-12-06|2022-01-06|2009-10-02 13:00:00.222|2009-10-02 13:10:00.000|2009-10-02 13:00:00.000|2021-12-05 11:00:00.000|2021-12-06|2009-11-01 12:00:00.000|2022-01-05 11:00:00.000|2022-01-06|2009-12-01 12:00:00.000|
```

Copy

### Known Issues[¶](#id147)

#### 1. INTERVAL + INTERVAL Operation is not supported[¶](#interval-interval-operation-is-not-supported)

Snowflake does not support INTERVAL + INTERVAL operations.

### Related EWIs[¶](#id148)

1. [SSC-EWI-OR0036](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI.html#ssc-ewi-or0036):
   Types resolution issues, the arithmetic operation may not behave correctly between string and
   date.
2. [SSC-EWI-OR0095](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI.html#ssc-ewi-or0095):
   Operation Between Interval Type and Date Type not Supported.
3. [SSC-FDM-0007](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0007):
   Element with missing dependencies.
4. [SSC-FDM-OR0042](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM.html#ssc-fdm-or0042):
   Date Type Transformed To Timestamp Has A Different Behavior.

## DATEDIFF UDF INTERVAL[¶](#datediff-udf-interval)

Note

Some parts in the output code are omitted for clarity reasons.

### Description[¶](#id149)

This UDF is used to resolve operations with intervals like:

- INTERVAL - UNKNOWN
- UNKNOWN - INTERVAL
- DATE - INTERVAL
- TIMESTAMP - INTERVAL

Note

An UNKNOWN type is a column or expression whose type could not be resolved by Snow Convert, it use
to happen when the DDLs for tables are not included in the migration or when there is an expression
or subquery that can return different data types.

### Custom UDF overloads[¶](#id150)

#### DATEADD_DDIF(string, date)[¶](#dateadd-ddif-string-date)

**Parameters**

1. **INTERVAL_VALUE**: The interval `String` of the operation.
2. **D**: The `DATE` where the interval will be subtracted.

##### UDF[¶](#id151)

```
CREATE OR REPLACE FUNCTION PUBLIC.DATEDIFF_UDF(INTERVAL_VALUE STRING,D DATE)
RETURNS DATE
LANGUAGE SQL
IMMUTABLE
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}'
AS
$$
WITH VARS(INPUT_VALUE, INPUT_PART) AS (
SELECT SUBSTR(INTERVAL_VALUE,11,POSITION('''',INTERVAL_VALUE,11)-11),
       TRIM(SUBSTR(INTERVAL_VALUE,POSITION('''',INTERVAL_VALUE,11)+1)))
SELECT
    CASE WHEN INPUT_PART='YEAR(2) TO MONTH' OR INPUT_PART='YEAR(4) TO MONTH' THEN
        DATEADD(MONTHS,-1*PUBLIC.INTERVAL_TO_MONTHS_UDF(INPUT_VALUE),D)
    WHEN INPUT_PART='MONTH' THEN
        DATEADD(MONTHS,-1*TO_NUMBER(INPUT_VALUE),D)
    ELSE
        DATEADD(MICROSECONDS,-1*1000000*PUBLIC.INTERVAL_TO_SECONDS_UDF(INPUT_PART, INPUT_VALUE),D)::DATE
    END CASE
FROM VARS
$$;
```

Copy

#### DATEADD_DIFF(date, string)[¶](#dateadd-diff-date-string)

**Parameters**

1. **D**: The `DATE` where the interval will be subtracted.
2. **INTERVAL_VALUE**: The interval `String` of the operation.

##### UDF[¶](#id152)

```
CREATE OR REPLACE FUNCTION PUBLIC.DATEDIFF_UDF(D DATE, INTERVAL_VALUE STRING)
RETURNS DATE
LANGUAGE SQL
IMMUTABLE
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}'
AS
$$
WITH VARS(INPUT_VALUE, INPUT_PART) AS (
SELECT SUBSTR(INTERVAL_VALUE,11,POSITION('''',INTERVAL_VALUE,11)-11),
       TRIM(SUBSTR(INTERVAL_VALUE,POSITION('''',INTERVAL_VALUE,11)+1)))
SELECT
    CASE WHEN INPUT_PART='YEAR(2) TO MONTH' OR INPUT_PART='YEAR(4) TO MONTH' THEN
        DATEADD(MONTHS,-1*PUBLIC.INTERVAL_TO_MONTHS_UDF(INPUT_VALUE),D)
    WHEN INPUT_PART='MONTH' THEN
        DATEADD(MONTHS,-1*TO_NUMBER(INPUT_VALUE),D)
    ELSE
        DATEADD(MICROSECONDS,-1*1000000*PUBLIC.INTERVAL_TO_SECONDS_UDF(INPUT_PART, INPUT_VALUE),D)::DATE
    END CASE
FROM VARS
$$;
```

Copy

#### DATEADD_DIFF(string, timestamp)[¶](#dateadd-diff-string-timestamp)

**Parameters**

1. **INTERVAL_VALUE**: The interval `String` of the operation.
2. **D**: The `TIMESTAMP` where the interval will be subtracted.

##### UDF[¶](#id153)

```
CREATE OR REPLACE FUNCTION PUBLIC.DATEDIFF_UDF(INTERVAL_VALUE STRING,D TIMESTAMP)
RETURNS TIMESTAMP
LANGUAGE SQL
IMMUTABLE
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}'
AS
$$
WITH VARS(INPUT_VALUE, INPUT_PART) AS (
SELECT SUBSTR(INTERVAL_VALUE,11,POSITION('''',INTERVAL_VALUE,11)-11),
       TRIM(SUBSTR(INTERVAL_VALUE,POSITION('''',INTERVAL_VALUE,11)+1)))
SELECT
    CASE WHEN INPUT_PART='YEAR(2) TO MONTH' OR INPUT_PART='YEAR(4) TO MONTH' THEN
        DATEADD(MONTHS,-1*PUBLIC.INTERVAL_TO_MONTHS_UDF(INPUT_VALUE),D)
    WHEN INPUT_PART='MONTH' THEN
        DATEADD(MONTHS,-1*TO_NUMBER(INPUT_VALUE),D)
    ELSE
        DATEADD(MICROSECONDS,-1*1000000*PUBLIC.INTERVAL_TO_SECONDS_UDF(INPUT_PART, INPUT_VALUE),D)
    END CASE
FROM VARS
$$;
```

Copy

#### DATEADD_DIFF(timestamp, string)[¶](#dateadd-diff-timestamp-string)

**Parameters**

1. **D**: The `TIMESTAMP` where the interval will be subtracted.
2. **INTERVAL_VALUE**: The interval `String` of the operation.

##### UDF[¶](#id154)

```
CREATE OR REPLACE FUNCTION PUBLIC.DATEDIFF_UDF(D TIMESTAMP, INTERVAL_VALUE STRING)
RETURNS TIMESTAMP
LANGUAGE SQL
IMMUTABLE
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}'
AS
$$
WITH VARS(INPUT_VALUE, INPUT_PART) AS (
SELECT SUBSTR(INTERVAL_VALUE,11,POSITION('''',INTERVAL_VALUE,11)-11),
       TRIM(SUBSTR(INTERVAL_VALUE,POSITION('''',INTERVAL_VALUE,11)+1)))
SELECT
    CASE WHEN INPUT_PART='YEAR(2) TO MONTH' OR INPUT_PART='YEAR(4) TO MONTH' THEN
        DATEADD(MONTHS,-1*PUBLIC.INTERVAL_TO_MONTHS_UDF(INPUT_VALUE),D)
    WHEN INPUT_PART='MONTH' THEN
        DATEADD(MONTHS,-1*TO_NUMBER(INPUT_VALUE),D)
    ELSE
        DATEADD(MICROSECONDS,-1*1000000*PUBLIC.INTERVAL_TO_SECONDS_UDF(INPUT_PART, INPUT_VALUE),D)
    END CASE
FROM VARS
$$;
```

Copy

#### Usage example[¶](#id155)

Note

**`--disableDateAsTimestamp`**

Flag to indicate whether `SYSDATE` should be transformed into `CURRENT_DATE` _or_
`CURRENT_TIMESTAMP`. This will also affect all `DATE` columns that will be transformed to
`TIMESTAMP`.

##### Oracle[¶](#id156)

```
-- DROP TABLE UNKNOWN_TABLE;
-- CREATE TABLE UNKNOWN_TABLE(Unknown timestamp);
-- INSERT  INTO UNKNOWN_TABLE VALUES (TO_TIMESTAMP('01/10/09, 12:00 P.M.', 'dd/mm/yy, hh:mi P.M.'));

CREATE TABLE TIMES(
AsTimeStamp TIMESTAMP,
AsTimestampTwo TIMESTAMP,
AsDate DATE,
AsDateTwo DATE
);

INSERT INTO TIMES VALUES (
TO_TIMESTAMP('05/11/21, 11:00 A.M.', 'dd/mm/yy, hh:mi A.M.'),
TO_TIMESTAMP('05/11/21, 10:00 A.M.', 'dd/mm/yy, hh:mi A.M.'),
TO_DATE('06/11/21', 'dd/mm/yy'),
TO_DATE('05/11/21', 'dd/mm/yy'));

SELECT
 AsTimeStamp-INTERVAL '1-1' YEAR(2) TO MONTH,
 AsTimeStamp-INTERVAL '2-1' YEAR(4) TO MONTH,
 AsTimeStamp-INTERVAL '1' MONTH,
 AsTimeStamp-INTERVAL '2' MONTH,
 AsDate-INTERVAL '1-1' YEAR(2) TO MONTH,
 AsDate-INTERVAL '2-1' YEAR(4) TO MONTH,
 AsDate-INTERVAL '1' MONTH,
 AsDate-INTERVAL '2' MONTH,
 Unknown-INTERVAL '1 01:00:00.222' DAY TO SECOND(3),
 Unknown-INTERVAL '1 01:10' DAY TO MINUTE,
 Unknown-INTERVAL '1 1' DAY TO HOUR
FROM TIMES, UNKNOWN_TABLE;
```

Copy

##### Result[¶](#id157)

```
<!-- prettier-ignore -->
|ASTIMESTAMP-INTERVAL'1-1'YEAR(2)TOMONTH|ASTIMESTAMP-INTERVAL'2-1'YEAR(4)TOMONTH|ASTIMESTAMP-INTERVAL'1'MONTH|ASTIMESTAMP-INTERVAL'2'MONTH|ASDATE-INTERVAL'1-1'YEAR(2)TOMONTH|ASDATE-INTERVAL'2-1'YEAR(4)TOMONTH|ASDATE-INTERVAL'1'MONTH|ASDATE-INTERVAL'2'MONTH|UNKNOWN-INTERVAL'101:00:00.222'DAYTOSECOND(3)|UNKNOWN-INTERVAL'101:10'DAYTOMINUTE|UNKNOWN-INTERVAL'11'DAYTOHOUR|
|---|---|---|---|---|---|---|---|---|---|---|
|2020-10-05 11:00:00.000|2019-10-05 11:00:00.000|2021-10-05 11:00:00.000|2021-09-05 11:00:00.000|2020-10-06 00:00:00.000|2019-10-06 00:00:00.000|2021-10-06 00:00:00.000|2021-09-06 00:00:00.000|2009-09-30 10:59:59.778|2009-09-30 10:50:00.000|2009-09-30 11:00:00.000|
```

Copy

##### Snowflake[¶](#id158)

Note

This configuration was used in Snowflake

```
ALTER SESSION SET TIMESTAMP_NTZ_OUTPUT_FORMAT= 'DD-MON-YY HH.MI.SS.FF6 AM';
ALTER SESSION SET DATE_OUTPUT_FORMAT= 'DD-MON-YY';
```

Copy

```
-- DROP TABLE UNKNOWN_TABLE;
-- CREATE TABLE UNKNOWN_TABLE(Unknown timestamp);
-- INSERT  INTO UNKNOWN_TABLE VALUES (TO_TIMESTAMP('01/10/09, 12:00 P.M.', 'dd/mm/yy, hh:mi P.M.'));
CREATE OR REPLACE TABLE TIMES (
 AsTimeStamp TIMESTAMP(6),
 AsTimestampTwo TIMESTAMP(6),
 AsDate TIMESTAMP /*** SSC-FDM-OR0042 - DATE TYPE COLUMN HAS A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/,
 AsDateTwo TIMESTAMP /*** SSC-FDM-OR0042 - DATE TYPE COLUMN HAS A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/
 )
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
;

INSERT INTO TIMES
VALUES (
TO_TIMESTAMP('05/11/21, 11:00 A.M.', 'dd/mm/yy, hh:mi A.M.'),
TO_TIMESTAMP('05/11/21, 10:00 A.M.', 'dd/mm/yy, hh:mi A.M.'),
TO_DATE('06/11/21', 'dd/mm/yy'),
TO_DATE('05/11/21', 'dd/mm/yy'));

--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "UNKNOWN_TABLE" **

SELECT
 !!!RESOLVE EWI!!! /*** SSC-EWI-OR0095 - OPERATION BETWEEN INTERVAL TYPE AND DATE TYPE NOT SUPPORTED ***/!!!
 AsTimeStamp - INTERVAL '1y, 1mm',
 !!!RESOLVE EWI!!! /*** SSC-EWI-OR0095 - OPERATION BETWEEN INTERVAL TYPE AND DATE TYPE NOT SUPPORTED ***/!!!
 AsTimeStamp - INTERVAL '2y, 1mm',
 !!!RESOLVE EWI!!! /*** SSC-EWI-OR0095 - OPERATION BETWEEN INTERVAL TYPE AND DATE TYPE NOT SUPPORTED ***/!!!
 AsTimeStamp - INTERVAL '1 month',
 !!!RESOLVE EWI!!! /*** SSC-EWI-OR0095 - OPERATION BETWEEN INTERVAL TYPE AND DATE TYPE NOT SUPPORTED ***/!!!
 AsTimeStamp - INTERVAL '2 month',
 AsDate- INTERVAL '1y, 1mm',
 AsDate- INTERVAL '2y, 1mm',
 AsDate- INTERVAL '1 month',
 AsDate- INTERVAL '2 month',
 !!!RESOLVE EWI!!! /*** SSC-EWI-OR0036 - TYPES RESOLUTION ISSUES, ARITHMETIC OPERATION '-' MAY NOT BEHAVE CORRECTLY BETWEEN Unknown AND Interval ***/!!!
 Unknown - INTERVAL '1d, 01h, 00m, 00s, 222ms',
 !!!RESOLVE EWI!!! /*** SSC-EWI-OR0036 - TYPES RESOLUTION ISSUES, ARITHMETIC OPERATION '-' MAY NOT BEHAVE CORRECTLY BETWEEN Unknown AND Interval ***/!!!
 Unknown - INTERVAL '1d, 01h, 10m',
 !!!RESOLVE EWI!!! /*** SSC-EWI-OR0036 - TYPES RESOLUTION ISSUES, ARITHMETIC OPERATION '-' MAY NOT BEHAVE CORRECTLY BETWEEN Unknown AND Interval ***/!!!
 Unknown - INTERVAL '1d, 1h'
FROM
 TIMES,
 UNKNOWN_TABLE;
```

Copy

##### Result[¶](#id159)

```
<!-- prettier-ignore -->
|DATEDIFF_UDF(ASTIMESTAMP,'INTERVAL ''1-1'' YEAR(2) TO MONTH')|DATEDIFF_UDF(ASTIMESTAMP,'INTERVAL ''2-1'' YEAR(4) TO MONTH')|DATEDIFF_UDF(ASTIMESTAMP,'INTERVAL ''1'' MONTH')|DATEDIFF_UDF(ASTIMESTAMP,'INTERVAL ''2'' MONTH')|DATEDIFF_UDF(ASDATE,'INTERVAL ''1-1'' YEAR(2) TO MONTH')|DATEDIFF_UDF(ASDATE,'INTERVAL ''2-1'' YEAR(4) TO MONTH')|DATEDIFF_UDF(ASDATE,'INTERVAL ''1'' MONTH')|DATEDIFF_UDF(ASDATE,'INTERVAL ''2'' MONTH')|DATEDIFF_UDF(UNKNOWN,'INTERVAL ''1 01:00:00.222'' DAY TO SECOND(3)')|DATEDIFF_UDF(UNKNOWN,'INTERVAL ''1 01:10'' DAY TO MINUTE')|DATEDIFF_UDF(UNKNOWN,'INTERVAL ''1 1'' DAY TO HOUR')|
|---|---|---|---|---|---|---|---|---|---|---|
|2020-10-05 11:00:00.000|2019-10-05 11:00:00.000|2021-10-05 11:00:00.000|2021-09-05 11:00:00.000|2020-10-06|2019-10-06|2021-10-06|2021-09-06|2009-09-30 10:59:59.778|2009-09-30 10:50:00.000|2009-09-30 11:00:00.000|
```

Copy

### Known Issues[¶](#id160)

#### 1. INTERVAL - INTERVAL Operation is not supported[¶](#id161)

Snowflake does not support INTERVAL - INTERVAL operations.

### Related EWIs[¶](#id162)

1. [SSC-EWI-OR0036](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI.html#ssc-ewi-or0036):
   Types resolution issues, the arithmetic operation may not behave correctly between string and
   date.
2. [SSC-EWI-OR0095](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI.html#ssc-ewi-or0095):
   Operation Between Interval Type and Date Type not Supported.
3. [SSC-FDM-0007](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0007):
   Element with missing dependencies.
4. [SSC-FDM-OR0042](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM.html#ssc-fdm-or0042):
   Date Type Transformed To Timestamp Has A Different Behavior.
