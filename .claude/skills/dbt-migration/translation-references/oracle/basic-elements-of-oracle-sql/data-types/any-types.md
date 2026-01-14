---
description:
  The Any types provide highly flexible modeling of procedure parameters and table columns where the
  actual type is not known. These data types let you dynamically encapsulate and access type
  descriptio
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/oracle/basic-elements-of-oracle-sql/data-types/any-types
title: SnowConvert AI - Oracle - Any Types | Snowflake Documentation
---

## Description[¶](#description)

> The `Any` types provide highly flexible modeling of procedure parameters and table columns where
> the actual type is not known. These data types let you dynamically encapsulate and access type
> descriptions, data instances, and sets of data instances of any other SQL type.
> ([Oracle SQL Language Reference ANYTYPES Data Types](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/Data-Types.html#GUID-5A8C5AC6-BC32-4D78-B0DE-037162106C72))

## ANYDATA[¶](#anydata)

### Description[¶](#id1)

> This type contains an instance of a given type, with data, plus a description of the type.
> `ANYDATA` can be used as a table column data type and lets you store heterogeneous values in a
> single column. The values can be of SQL built-in types as well as user-defined types.
> ([Oracle SQL Language Reference ANYDATA Data Type](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/Data-Types.html#GUID-2FCFAF23-DFE9-4D05-8518-88AB134E0692)).

The `ANYDATA` data type is **not supported** in Snowflake.

```
{ SYS.ANYDATA | ANYDATA }
```

Copy

### Sample Source Patterns[¶](#sample-source-patterns)

#### Create Table with ANYDATA[¶](#create-table-with-anydata)

##### Oracle[¶](#oracle)

```
CREATE TABLE anydatatable
(
    col1 NUMBER,
    col2 ANYDATA,
    col3 SYS.ANYDATA
);
```

Copy

##### Snowflake[¶](#snowflake)

```
CREATE OR REPLACE TABLE anydatatable
    (
        col1 NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/,
        col2 VARIANT,
        col3 VARIANT
    )
    COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
    ;
```

Copy

#### Inserting data into ANYDATA column[¶](#inserting-data-into-anydata-column)

##### Oracle[¶](#id2)

```
INSERT INTO anydatatable VALUES(
	555,
	ANYDATA.ConvertVarchar('Another Test Text')
);
```

Copy

##### Snowflake[¶](#id3)

```
INSERT INTO anydatatable
VALUES(
	555,
	ANYDATA.ConvertVarchar('Another Test Text') !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'ANYDATA.ConvertVarchar' NODE ***/!!!
);
```

Copy

#### Functional Example[¶](#functional-example)

Warning

This example **is not a translation** of SnowConvert AI, it is only used to show the functional
equivalence between Oracle `ANYDATA` and Snowflake `VARIANT`

Warning

We are using the `ANYDATA` built-in package. The conversion for this package is currently **not
supported** by SnowConvert.

##### Oracle[¶](#id4)

```
--Create Table
CREATE TABLE anydatatable_example
(
	col1 ANYDATA,
	col2 ANYDATA,
	col3 ANYDATA,
	col4 ANYDATA,
	col5 ANYDATA
);

--Insert data
INSERT INTO anydatatable_example VALUES(
	ANYDATA.ConvertNumber(123),
	ANYDATA.ConvertVarchar('Test Text'),
	ANYDATA.ConvertBFloat(3.14f),
	ANYDATA.ConvertDate(CURRENT_DATE),
	ANYDATA.ConvertTimestamp(CURRENT_TIMESTAMP)
);

--Retrieve information
SELECT
	ANYDATA.AccessNumber(col1) AS col1,
	ANYDATA.AccessVarchar(col2) AS col2,
	ANYDATA.AccessBFloat(col3) AS col3,
	ANYDATA.AccessDate(col4) AS col4,
	ANYDATA.AccessTimestamp(col5) AS col5
FROM anydatatable_example;
```

Copy

##### Result[¶](#result)

<!-- prettier-ignore -->
|COL1|COL2|COL3|COL4|COL5|
|---|---|---|---|---|
|123|Test Text|3.14|2021-12-05 18:24:59.000|2021-12-05 18:24:59.100|

##### Snowflake[¶](#id5)

```
--Create Table
CREATE OR REPLACE TABLE anydatatable_example
	(
		col1 VARIANT,
		col2 VARIANT,
		col3 VARIANT,
		col4 VARIANT,
		col5 VARIANT
	)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

--Insert data
INSERT INTO anydatatable_example
VALUES(
	ANYDATA.ConvertNumber(123) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'ANYDATA.ConvertNumber' NODE ***/!!!,
	ANYDATA.ConvertVarchar('Test Text') !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'ANYDATA.ConvertVarchar' NODE ***/!!!,
	ANYDATA.ConvertBFloat(3.14) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'ANYDATA.ConvertBFloat' NODE ***/!!!,
	ANYDATA.ConvertDate(CURRENT_DATE()) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'ANYDATA.ConvertDate' NODE ***/!!!,
	ANYDATA.ConvertTimestamp(CURRENT_TIMESTAMP()) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'ANYDATA.ConvertTimestamp' NODE ***/!!!
);

--Retrieve information
SELECT
	ANYDATA.AccessNumber(col1) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'ANYDATA.AccessNumber' NODE ***/!!! AS col1,
	ANYDATA.AccessVarchar(col2) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'ANYDATA.AccessVarchar' NODE ***/!!! AS col2,
	ANYDATA.AccessBFloat(col3) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'ANYDATA.AccessBFloat' NODE ***/!!! AS col3,
	ANYDATA.AccessDate(col4) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'ANYDATA.AccessDate' NODE ***/!!! AS col4,
	ANYDATA.AccessTimestamp(col5) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'ANYDATA.AccessTimestamp' NODE ***/!!! AS col5
FROM
	anydatatable_example;
```

Copy

##### Result[¶](#id6)

<!-- prettier-ignore -->
|COL1|COL2|COL3|COL4|COL5|
|---|---|---|---|---|
|123|“Test Text”|3.14|“2021-12-05”|“2021-12-05 18:24:43.326 -0800”|

### Known Issues[¶](#known-issues)

#### 1. No access to the ANYDATA built-in package[¶](#no-access-to-the-anydata-built-in-package)

Most operations with `ANYDATA` columns require to use the `ANYDATA` built-in package, transformation
for Oracle built-in packages is not supported by SnowConvert AI yet.

### Related EWIs[¶](#related-ewis)

1. [SSC-FDM-0006](../../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0006):
   Number type column may not behave similarly in Snowflake.
2. [SSC-EWI-0073](../../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0073):
   Pending Functional Equivalence Review.

## ANYDATASET[¶](#anydataset)

Note

Some parts in the output code are omitted for clarity reasons.

### Description[¶](#id7)

> This type contains a description of a given type plus a set of data instances of that type.
> `ANYDATASET` can be used as a procedure parameter data type where such flexibility is needed. The
> values of the data instances can be of SQL built-in types as well as user-defined types.
> ([Oracle SQL Language Reference ANYDATASET Data Type](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/Data-Types.html#GUID-CBC6D668-4FDB-40C9-B240-DFDA6420C13B)).

The `ANYDATASET` data type is **not supported** in Snowflake. A possible workaround for this data
type could be
[Snowflake ARRAY](https://docs.snowflake.com/en/sql-reference/data-types-semistructured.html#array),
however that transformation is currently not supported by SnowConvert.

```
{ SYS.ANYDATASET | ANYDATASET }
```

Copy

### Sample Source Patterns[¶](#id8)

#### Create Table with ANYDATASET[¶](#create-table-with-anydataset)

##### Oracle[¶](#id9)

```
CREATE TABLE anydatasettable
(
	col1 NUMBER,
	col2 ANYDATASET,
	col3 SYS.ANYDATASET
);
```

Copy

##### Snowflake[¶](#id10)

```
CREATE OR REPLACE TABLE anydatasettable
	(
		col1 NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/,
	!!!RESOLVE EWI!!! /*** SSC-EWI-0028 - TYPE NOT SUPPORTED BY SNOWFLAKE ***/!!!
		col2 ANYDATASET,
	!!!RESOLVE EWI!!! /*** SSC-EWI-0028 - TYPE NOT SUPPORTED BY SNOWFLAKE ***/!!!
		col3 SYS.ANYDATASET
	)
	COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
	;
```

Copy

#### Inserting data into ANYDATASET column[¶](#inserting-data-into-anydataset-column)

##### Oracle[¶](#id11)

```
DECLARE
    anytype_example    ANYTYPE;
    anydataset_example ANYDATASET;
BEGIN
    ANYDATASET.BEGINCREATE(DBMS_TYPES.TYPECODE_VARCHAR2, anytype_example, anydataset_example);

    anydataset_example.ADDINSTANCE;
    anydataset_example.SETVARCHAR2('First element');

    anydataset_example.ADDINSTANCE;
    anydataset_example.SETVARCHAR2('Second element');

    ANYDATASET.ENDCREATE(anydataset_example);

    INSERT INTO anydatasettable VALUES (123, anydataset_example);
END;
```

Copy

##### Snowflake[¶](#id12)

```
DECLARE
    !!!RESOLVE EWI!!! /*** SSC-EWI-0028 - TYPE NOT SUPPORTED BY SNOWFLAKE ***/!!!
    anytype_example    ANYTYPE;
    !!!RESOLVE EWI!!! /*** SSC-EWI-0028 - TYPE NOT SUPPORTED BY SNOWFLAKE ***/!!!
    anydataset_example ANYDATASET;
BEGIN
    CALL
    ANYDATASET.BEGINCREATE(
    !!!RESOLVE EWI!!! /*** SSC-EWI-OR0076 - TRANSLATION FOR BUILT-IN PACKAGE 'DBMS_TYPES.TYPECODE_VARCHAR2' IS NOT CURRENTLY SUPPORTED. ***/!!!
    '' AS TYPECODE_VARCHAR2, :anytype_example, :anydataset_example);
    CALL

    anydataset_example.ADDINSTANCE();
    CALL
    anydataset_example.SETVARCHAR2('First element');
    CALL

    anydataset_example.ADDINSTANCE();
    CALL
    anydataset_example.SETVARCHAR2('Second element');
    CALL

    ANYDATASET.ENDCREATE(:anydataset_example);

    INSERT INTO anydatasettable
    VALUES (123, :anydataset_example);
END;
```

Copy

### Known Issues[¶](#id13)

#### 1. Inserts are being parsed incorrectly[¶](#inserts-are-being-parsed-incorrectly)

Some of the functions needed to create and insert a new `ANYDATASET` object are not being parsed
correctly by SnowConvert.

##### 1. No access to the ANYDATASET built-in package[¶](#no-access-to-the-anydataset-built-in-package)

Most operations with `ANYDATASET` columns require to use the `ANYDATASET` built-in package,
transformation for Oracle built-in packages is not supported by SnowConvert AI yet.

### Related EWIs[¶](#id14)

1. [SSC-EWI-OR0076](../../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI.html#ssc-ewi-or0076):
   Built In Package Not Supported.
2. [SSC-FDM-0006:](../../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0006)
   Number type column may not behave similarly in Snowflake
3. [SSC-EWI-0028](../../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0028):
   Type not supported by Snowflake.

## ANYTYPE[¶](#anytype)

### Description[¶](#id15)

> This type can contain a type description of any named SQL type or unnamed transient type.
> ([Oracle SQL Language Reference ANYTYPE Data Type](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/Data-Types.html#GUID-CBC6D668-4FDB-40C9-B240-DFDA6420C13B)).

The `ANYTYPE` data type is **not supported** in Snowflake.

```
{ SYS.ANYTYPE | ANYTYPE }
```

Copy

### Sample Source Patterns[¶](#id16)

#### Create Table with ANYTYPE[¶](#create-table-with-anytype)

##### Oracle[¶](#id17)

```
CREATE TABLE anytypetable
(
	col1 NUMBER,
	col2 ANYTYPE,
	col3 SYS.ANYTYPE
);
```

Copy

##### Snowflake[¶](#id18)

```
CREATE OR REPLACE TABLE anytypetable
	(
		col1 NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/,
	!!!RESOLVE EWI!!! /*** SSC-EWI-0028 - TYPE NOT SUPPORTED BY SNOWFLAKE ***/!!!
		col2 ANYTYPE,
	!!!RESOLVE EWI!!! /*** SSC-EWI-0028 - TYPE NOT SUPPORTED BY SNOWFLAKE ***/!!!
		col3 SYS.ANYTYPE
	)
	COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
	;
```

Copy

#### Inserting data into ANYTYPE column[¶](#inserting-data-into-anytype-column)

##### Oracle[¶](#id19)

```
--Create Custom Type
CREATE OR REPLACE TYPE example_type AS OBJECT (id NUMBER, name VARCHAR(20));

--Insert
INSERT INTO anytypetable VALUES(
    123,
    GETANYTYPEFROMPERSISTENT ('HR', 'EXAMPLE_TYPE')
);
```

Copy

##### Snowflake[¶](#id20)

```
--Create Custom Type
!!!RESOLVE EWI!!! /*** SSC-EWI-0056 - CUSTOM TYPES ARE NOT SUPPORTED IN SNOWFLAKE BUT REFERENCES TO THIS CUSTOM TYPE WERE CHANGED TO VARIANT ***/!!!
CREATE OR REPLACE TYPE example_type AS OBJECT (id NUMBER, name VARCHAR(20))
;

--Insert
INSERT INTO anytypetable
VALUES(
    123,
    GETANYTYPEFROMPERSISTENT ('HR', 'EXAMPLE_TYPE') !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'GETANYTYPEFROMPERSISTENT' NODE ***/!!!
);
```

Copy

### Known Issues[¶](#id21)

#### 1. No access to the ANYTYPE built-in package[¶](#no-access-to-the-anytype-built-in-package)

Most operations with `ANYDATA` columns require to use the `ANYTYPE` built-in package, transformation
for Oracle built-in packages is not supported by SnowConvert AI yet.

### Related EWIs[¶](#id22)

1. [SSC-EWI-0056](../../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0056):
   Create Type Not Supported.
2. [SSC-EWI-0073](../../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0073):
   Pending Functional Equivalence Review.
3. [SSC-EWI-0028](../../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0028):
   Type not supported in Snowflake.
4. [SSC-FDM-0006](../../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0006):
   Number type column may not behave similarly in Snowflake.
