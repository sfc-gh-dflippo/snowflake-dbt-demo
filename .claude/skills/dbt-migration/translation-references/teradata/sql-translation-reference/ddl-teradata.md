---
description:
  In this section, you will find the documentation for the translation reference of Data Definition
  Language Elements.
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/teradata/sql-translation-reference/ddl-teradata
title: SnowConvert AI - Teradata - DDL | Snowflake Documentation
---

## Index[¶](#index)

Translation reference to convert INDEX statement to Snowflake

Warning

Currently, **_Create Index_** statement is not being converted but it is being parsed. Also, if your
source code has Create `index` statements, these are going to be accounted for in the **_Assessment
Report._**

**Example of Create Index**

### Teradata input[¶](#teradata-input)

```
 CREATE INDEX (col1, col2, col3) ORDER BY VALUES (col2) ON table1;

CREATE INDEX my_index_name ON my_table (column1, column2);
```

**Note:**

Due to architectural reasons, Snowflake does not support indexes so, SnowConvert AI will remove all
the code related to the creation of indexes. Snowflake automatically creates micro-partitions for
every table that help speed up the performance of DML operations, the user does not have to worry
about creating or managing these micro-partitions.

Usually, this is enough to have a very good query performance however, there are ways to improve it
by creating data clustering keys.
[Snowflake’s official page](https://docs.snowflake.com/en/user-guide/tables-clustering-micropartitions.html)
provides more information about micro-partitions and data clustering.

## Join Index[¶](#join-index)

### Description [¶](#description)

In SnowConvert AI, Teradata Join Indexes are transformed into Snowflake Dynamic Tables. To properly
configure Dynamic Tables, two essential parameters must be defined: TARGET_LAG and WAREHOUSE. If
these parameters are left unspecified in the configuration options, SnowConvert AI will default to
preassigned values during the conversion, as demonstrated in the example below.

For more information on Join Indexes, click
[here](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/Database-Design/Join-and-Hash-Indexes/Join-Indexes).

For details on the necessary parameters for Dynamic Tables, click
[here](https://docs.snowflake.com/en/sql-reference/sql/create-dynamic-table).

### Sample Source Patterns[¶](#sample-source-patterns)

**Teradata**

**Join Index**

```
CREATE JOIN INDEX Employee
AS
SELECT
  Employee_Id,
  First_Name,
  Last_Name,
  BirthDate,
  DepartmentNo
FROM Employee
PRIMARY INDEX (First_Name);
```

**Snowflake**

**Dynamic Table**

```
CREATE OR REPLACE DYNAMIC TABLE Employee
--** SSC-FDM-0031 - DYNAMIC TABLE REQUIRED PARAMETERS SET BY DEFAULT **
TARGET_LAG='1 day'
WAREHOUSE=UPDATE_DUMMY_WAREHOUSE
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"teradata"}}'
AS
SELECT
  Employee_Id,
  First_Name,
  Last_Name,
  BirthDate,
  DepartmentNo
FROM
  Employee;
```

### Known Issues[¶](#known-issues)

No known errors detected at this time.

### Related EWIs[¶](#related-ewis)

1. [SSC-FDM-0031](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0031):
   Dynamic Table required parameters set by default

## Schema[¶](#schema)

### Description [¶](#id1)

The translation of the `CREATE SCHEMA` statement from Teradata to Snowflake is simple, as the basic
syntax remains the same.

### Sample Source Patterns[¶](#id2)

**Teradata**

**Join Index**

```
CREATE SCHEMA IF EXISTS schema_name;
```

**Snowflake**

**Dynamic Table**

```
CREATE SCHEMA IF EXISTS schema_name
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/23/2024" }}'
;
```

### Known Issues[¶](#id3)

#### WITH Properties of CREATE SCHEMA[¶](#with-properties-of-create-schema)

The `WITH` properties associated with the `CREATE SCHEMA` statement in Teradata are not supported in
Snowflake, as there is no equivalent functionality available.

**Teradata**

**Join Index**

```
CREATE SCHEMA IF EXISTS schema_name
WITH ( PROPERTY1 = PROPERTYNAME, PROPERTY2 = PROPERTTYNAME, PROPERTY3 = PROPERTTYNAME);
```

**Snowflake**

**Dynamic Table**

```
CREATE SCHEMA IF EXISTS schema_name
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/23/2024" }}'
!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'SCHEMA WITH' NODE ***/!!!
WITH ( PROPERTY1 = PROPERTYNAME, PROPERTY2 = PROPERTTYNAME, PROPERTY3 = PROPERTTYNAME);
```

### Related EWIs[¶](#id4)

1. [SSC-EWI-0073](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0073):
   Pending Functional Equivalence Review.

## Views[¶](#views)

Translation reference to convert Teradata VIEW statement to Snowflake

**Note:**

Some parts in the output code are omitted for clarity reasons.

### Description [¶](#id5)

Teradata’s VIEW statement is translated to Snowflake VIEW syntax.

For more information on Teradata VIEW, check
[here](https://docs.teradata.com/r/scPHvjfglIlB8F70YliLAw/EXhAa7frdTDJwg2OZukLgQ).

### Sample Source Patterns[¶](#id6)

#### Create View Transformation[¶](#create-view-transformation)

**Teradata**

##### View[¶](#view)

```
 CREATE VIEW view1 (someTable.col1, someTable.col2) AS locking row for access
    SELECT
    my_table.col1, my_table.col2
    FROM table1 AS my_table
    WHERE my_table.col1 = 'SpecificValue'
    UNION ALL
    SELECT other_table.col2
    FROM table2 AS other_table
    WHERE my_table.col2 = other_table.col2
```

**Snowflake**

##### View[¶](#id7)

```
 --** SSC-FDM-0007 - MISSING DEPENDENT OBJECTS "table1", "table2" **
CREATE OR REPLACE VIEW view1
(
    col1,
    col2)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/02/2025",  "domain": "no-domain-provided" }}'
AS
SELECT
    my_table.col1,
    my_table.col2
    FROM
    table1 AS my_table
    WHERE
    UPPER(RTRIM( my_table.col1)) = UPPER(RTRIM('SpecificValue'))
    UNION ALL
    SELECT
    other_table.col2
       FROM
    table2 AS other_table
       WHERE my_table.col2 = other_table.col2;
```

#### Custom Schema Tag[¶](#custom-schema-tag)

The custom schema is specified in the comment section before the specification of the view, with an
XML tag named “sc-view” that contains only the value of the schema and the view name separated with
a period ‘.’ as shown below: `<sc-view>SCHEMANAME.VIEWNAME</sc-view>`

The custom schema will be used as a view qualifier, and then the name of the view and all the
objects referred to in the FROM queries and inner queries will be using that custom schema.
Therefore could be several views with the same name, but with different custom tags. **Example**:
two views with the same name, will take the custom schema tag information to perform the
translation.

##### Teradata[¶](#teradata)

##### View[¶](#id8)

```
 /*<sc-view>RMSviews.EMPLOYEEB</sc-view>*/
REPLACE VIEW EMPLOYEEB AS
SELECT * FROM EMPLOYEE
WHERE AREA = "AREAB";

/*<sc-view>Views.EMPLOYEEB</sc-view>*/
REPLACE VIEW EMPLOYEEB AS
SELECT * FROM EMPLOYEE
WHERE AREA = "AREAB";
```

##### Snowflake[¶](#snowflake)

The transformation for Snowflake will vary depending on the customized schema name `MySchema`,
customized database name `MyDatabase` or not selecting a customized database or schema in the
conversion settings.

##### Custome Schema[¶](#custome-schema)

```
 /*<sc-view>RMSviews.EMPLOYEEB</sc-view>*/
--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "EMPLOYEE" **
CREATE OR REPLACE VIEW RMSviews.EMPLOYEEB
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
AS
SELECT
* FROM
RMSviews.EMPLOYEE
WHERE AREA = "AREAB";

/*<sc-view>Views.EMPLOYEEB</sc-view>*/
--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "EMPLOYEE" **
--** SSC-FDM-0019 - SEMANTIC INFORMATION COULD NOT BE LOADED FOR Views.EMPLOYEEB. CHECK IF THE NAME IS INVALID OR DUPLICATED. **
CREATE OR REPLACE VIEW Views.EMPLOYEEB
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
AS
SELECT
* FROM
Views.EMPLOYEE
 WHERE AREA = "AREAB";
```

##### Custome Database[¶](#custome-database)

```
 /*<sc-view>RMSviews.EMPLOYEEB</sc-view>*/
CREATE OR REPLACE VIEW MyDatabase.RMSviews.EMPLOYEEB
AS
   SELECT * FROM MyDatabase.RMSviews.EMPLOYEE
   WHERE AREA = "AREAB";

/*<sc-view>Views.EMPLOYEEB</sc-view>*/
CREATE OR REPLACE VIEW MyDatabase.Views.EMPLOYEEB
AS
   SELECT * FROM MyDatabase.Views.EMPLOYEE
   WHERE AREA = "AREAB";
```

##### Non selected[¶](#non-selected)

```
 /*<sc-view>RMSviews.EMPLOYEEB</sc-view>*/
CREATE OR REPLACE VIEW RMSviews.PUBLIC.EMPLOYEEB
AS
   SELECT * FROM RMSviews.PUBLIC.EMPLOYEE
   WHERE AREA = "AREAB";

/*<sc-view>Views.EMPLOYEEB</sc-view>*/
CREATE OR REPLACE VIEW Views.PUBLIC.EMPLOYEEB
AS
   SELECT * FROM Views.PUBLIC.EMPLOYEE
   WHERE AREA = "AREAB";
```

### Known Issues[¶](#id9)

#### 1. Locking row for access logic difference[¶](#locking-row-for-access-logic-difference)

In Snowflake, access to objects and elements is based on users and privileges.

### Related EWIs[¶](#id10)

1. [SSC-FDM-0007](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0007):
   Element with missing dependencies.
2. [SSC-FDM-0019](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0019):
   Sematic information could not be loaded.

## Tables[¶](#tables)

Translation reference to convert Teradata TABLE statement to Snowflake

**Note:**

Some parts in the output code are omitted for clarity reasons.

### Description [¶](#id11)

Teradata’s TABLE statement is translated to Snowflake TABLE syntax.

For more information on Teradata TABLEs, check
[here](https://docs.teradata.com/r/Teradata-VantageTM-SQL-Data-Definition-Language-Syntax-and-Examples/March-2019/Table-Statements/CREATE-TABLE).

### Sample Source Patterns[¶](#id12)

#### **Simple Create​ Table**[¶](#simple-create-table)

**Teradata**

##### Table[¶](#table)

```
 CREATE TABLE table1, no fallback,
no before journal,
no after journal (
  c1 INTEGER NOT NULL,
	f1 INTEGER NOT NULL,
	p1 INTEGER NOT NULL,
  DATE,
  TIME,
	FOREIGN KEY(f1) REFERENCES WITH CHECK OPTION table2 (d1)
)
UNIQUE PRIMARY INDEX(c1)
PARTITION BY COLUMN(p1);
```

**Snowflake**

##### Table[¶](#id13)

```
CREATE OR REPLACE TABLE table1 (
	c1 INTEGER NOT NULL,
	f1 INTEGER NOT NULL,
	p1 INTEGER NOT NULL,
	DATE,
	TIME,
	FOREIGN KEY(f1) REFERENCES table2 (d1) ,
	UNIQUE (c1)
)
----** SSC-FDM-0038 - MICRO-PARTITIONING IS AUTOMATICALLY HANDLED ON ALL SNOWFLAKE TABLES **
--PARTITION BY COLUMN(p1)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "09/19/2025",  "domain": "no-domain-provided" }}'
;
```

#### Table Kind Clause - SET and MULTISET[¶](#table-kind-clause-set-and-multiset)

Teradata’s kind clause determines whether duplicate rows are permitted (MULTISET) or not (SET).

##### Teradata[¶](#id14)

##### Table[¶](#id15)

```
 -- Set semantics
CREATE SET TABLE table1 (
    column1 INTEGER
);

--Multiset semantics
CREATE MULTISET TABLE table2(
    column1 INTEGER
);
```

##### Snowflake[¶](#id16)

##### Table[¶](#id17)

```
 -- Set semantics
--** SSC-FDM-TD0024 - SET TABLE FUNCTIONALITY NOT SUPPORTED. TABLE MIGHT HAVE DUPLICATE ROWS **
CREATE OR REPLACE TABLE table1 (
    column1 INTEGER
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;

--Multiset semantics
CREATE OR REPLACE TABLE table2 (
    column1 INTEGER
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;
```

#### Volatile and Global Temporary Tables[¶](#volatile-and-global-temporary-tables)

Teradata’s Volatile and Global Temporary tables are used for the temporary storage of data. Their
difference lies in that the table definition (DDL) of Global Temporary tables is persisted in the
Data Dictionary, while Volatile tables definition is not stored.

##### Teradata[¶](#id18)

##### Table[¶](#id19)

```
 --Global Temporary Table
CREATE MULTISET GLOBAL TEMPORARY TABLE table1 (
    column1 INTEGER
);

--Volatile Table
CREATE MULTISET VOLATILE TABLE table3 (
    column1 INTEGER
);
```

##### Snowflake[¶](#id20)

##### Table[¶](#id21)

```
 --Global Temporary Table
--** SSC-FDM-0009 - GLOBAL TEMPORARY TABLE FUNCTIONALITY NOT SUPPORTED. **
CREATE OR REPLACE TABLE table1 (
    column1 INTEGER
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;

--Volatile Table
CREATE OR REPLACE TEMPORARY TABLE table3 (
    column1 INTEGER
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;
```

#### With data and with no data option[¶](#with-data-and-with-no-data-option)

**Teradata**

##### Table[¶](#id22)

```
 -- With data
CREATE TABLE table1 AS table2 WITH DATA

-- With no data
CREATE TABLE table1 AS table2 WITH NO DATA
```

**Snowflake**

##### Table[¶](#id23)

```
 -- With data
CREATE OR REPLACE TABLE table1 CLONE table2
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;

-- With no data
--** SSC-FDM-0019 - SEMANTIC INFORMATION COULD NOT BE LOADED FOR table1. CHECK IF THE NAME IS INVALID OR DUPLICATED. **
CREATE OR REPLACE TABLE table1 LIKE table2
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;
```

#### Snowflake’s Reserved & Limited Keywords[¶](#snowflake-s-reserved-limited-keywords)

SnowConvert AI facilitates seamless SQL migrations to Snowflake by addressing challenges associated
with reserved keywords. As per Snowflake’s
[reserved and limited keyword documentation](https://docs.snowflake.com/en/sql-reference/reserved-keywords),
certain keywords cannot be used as column names, table names, or aliases without special handling.
SnowConvert AI includes functionality to ensure SQL code compatibility in such cases.

**Reserved ANSI Keywords as Column Names**

For column names that match **ANSI or Snowflake** **reserved keywords**, SnowConvert AI
automatically wraps the column name in double quotes (`"`) to comply with Snowflake’s syntax rules.
This adjustment ensures that queries with these column names compile correctly in Snowflake without
requiring manual intervention.

**Example:**

##### Table[¶](#id24)

```
 CREATE TABLE ReservedKeywords (
  "CREATE" VARCHAR(50),
  FOLLOWING VARCHAR(50),
  "ILIKE" VARCHAR(50),
  RLIKE VARCHAR(50)
);
```

**Snowflake**

##### Table[¶](#id25)

```
 CREATE OR REPLACE TABLE ReservedKeywords (
    "CREATE" VARCHAR(50),
    "FOLLOWING" VARCHAR(50),
    "ILIKE" VARCHAR(50),
    "RLIKE" VARCHAR(50)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "11/28/2024",  "domain": "test" }}'
;
```

**Snowflake-Specific Reserved Keywords**

Columns that match **Snowflake-specific reserved keywords** (e.g., `CONSTRAINT`, `CURRENT_DATE`,
`CURRENT_TIME`) may still cause compilation issues even when wrapped in quotes. SnowConvert AI
detects these instances and generates a warning with code
[`SSC-EWI-0045`](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0045),
prompting users to review and potentially rename these columns for compatibility.

**Example:**

##### Table[¶](#id26)

```
 CREATE TABLE ColumnReservedNames (
  "CONSTRAINT" VARCHAR(50),
  "CURRENT_DATE" VARCHAR(50),
  "CURRENT_TIME" VARCHAR(50)
);
```

**Snowflake**

##### Table[¶](#id27)

```
 CREATE OR REPLACE TABLE ColumnReservedNames (
    !!!RESOLVE EWI!!! /*** SSC-EWI-0045 - COLUMN NAME 'CONSTRAINT' IS A SNOWFLAKE RESERVED KEYWORD ***/!!!
    "CONSTRAINT" VARCHAR(50),
    !!!RESOLVE EWI!!! /*** SSC-EWI-0045 - COLUMN NAME 'CURRENT_DATE' IS A SNOWFLAKE RESERVED KEYWORD ***/!!!
    "CURRENT_DATE" VARCHAR(50),
    !!!RESOLVE EWI!!! /*** SSC-EWI-0045 - COLUMN NAME 'CURRENT_TIME' IS A SNOWFLAKE RESERVED KEYWORD ***/!!!
    "CURRENT_TIME" VARCHAR(50)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "11/28/2024",  "domain": "test" }}'
;
```

### Known Issues[¶](#id28)

#### 1. Create table options not supported[¶](#create-table-options-not-supported)

As shown in the example “Simple Create Table”, Snowflake does not support Teradata create table
options. They are removed.

##### 2. Partition by performance issues[¶](#partition-by-performance-issues)

In the example “Simple Create Table”, the `partition by` statement is removed due to performance
considerations.

##### 3. Primary Index moved[¶](#primary-index-moved)

In Teradata, the primary index constraint is declared outside of the `create table` statement, but
in Snowflake it is required to be inside, as shown in the example “Simple Create Table”.

##### 4. SET semantics not supported[¶](#set-semantics-not-supported)

As shown in the example “Table Kind Clause - SET and MULTISET”, Snowflake does not support
Teradata’s SET semantics. They are removed.

##### 5. Global Temporary table option not supported[¶](#global-temporary-table-option-not-supported)

As shown in the example “Volatile and Global Temporary Table”, Snowflake does not support Teradata’s
Global Temporary table option. It will be removed.

##### 6. Compress unsupported[¶](#compress-unsupported)

`COMPRESS (value1. value2, value3)` is removed due to being unsupported.

##### 7. On commit unsupported[¶](#on-commit-unsupported)

`On commit` is removed due to being unsupported.

##### 8. Block compression unsupported[¶](#block-compression-unsupported)

`Block compression` is removed due to being unsupported.

##### 9. Normalize unsupported[¶](#normalize-unsupported)

`Normalize` is removed due to being unsupported.

### Related EWIs[¶](#id29)

1. [SSC-FDM-0009](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0009):
   GLOBAL TEMPORARY TABLE functionality not supported.
2. [SSC-FDM-0019](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0019):
   Sematic information could not be loaded.
3. [SSC-FDM-TD0024](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/teradataFDM.html#ssc-fdm-td0024):
   Set table functionality not supported.
4. [SSC-PRF-0007](../../../general/technical-documentation/issues-and-troubleshooting/performance-review/generalPRF.html#ssc-prf-0007):
   CLUSTER BY performance review.
5. [SSC-EWI-0045](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0045):
   Column Name is Snowflake Reserved Keyword.

## WITH DEFAULT[¶](#with-default)

Translation reference to convert Teradata WITH DEFAULT clause in column definitions to Snowflake

**Note:**

Some parts in the output code are omitted for clarity reasons.

### Description [¶](#id30)

Teradata’s `WITH DEFAULT` clause sets a system-default value to columns that are inserted with no
values. This value is typically the equivalent of zero or empty.

#### Syntax:[¶](#syntax)

```
 WITH DEFAULT
```

The following table shows Teradata’s data types, their corresponding type in Snowflake, and the
default value to be set if supported.

<!-- prettier-ignore -->
|Teradata|Snowflake|Default Value|
|---|---|---|
|BLOB[(n)]|BYTE|NOT SUPPORTED|
|BYTE[(n)]|BYTE|NOT SUPPORTED|
|VARBYTE[(n)]|BYTE|NOT SUPPORTED|
|BIGINT|BIGINT|0|
|BYTEINT|BYTEINT|0|
|DECIMAL [(n[,m])]|DECIMAL|0|
|DOUBLE PRECISION|DOUBLE PRECISION|0|
|FLOAT|FLOAT|0|
|INTEGER|INTEGER|0|
|NUMBER(n[,m])|NUMBER|0|
|NUMBER[(\*[,m])]|NUMBER|0|
|NUMERIC [(n[,m])]|NUMERIC|0|
|REAL|REAL|0|
|SMALLINT|SMALLINT|0|
|DATE|DATE|CURRENT_DATE|
|TIME [(n)]|TIME|CURRENT_TIME|
|TIMESTAMP [(n)]|TIMESTAMP|CURRENT_TIMESTAMP|
|TIMESTAMP WITH TIME ZONE|TIMESTAMP_TZ|LOCALTIMESTAMP|
|INTERVAL DAY [(n)]|VARCHAR(21)|'0DAY'|
|INTERVAL DAY [(n)] TO HOUR|VARCHAR(21)|'0DAY'|
|INTERVAL DAY [(n)] TO MINUTE|VARCHAR(21)|'0DAY'|
|INTERVAL DAY [(n)] TO SECOND|VARCHAR(21)|'0DAY'|
|INTERVAL HOUR [(n)]|VARCHAR(21)|'0HOUR'|
|INTERVAL HOUR [(n)] TO MINUTE|VARCHAR(21)|'0HOUR'|
|INTERVAL HOUR [(n)] TO SECOND|VARCHAR(21)|'0HOUR'|
|INTERVAL MINUTE [(n)]|VARCHAR(21)|'0MINUTE'|
|INTERVAL MINUTE [(n)] TO SECOND [(m)]|VARCHAR(21)|'0MINUTE'|
|INTERVAL MONTH|VARCHAR(21)|'0MONTH'|
|INTERVAL SECOND [(n,[m])]|VARCHAR(21)|'0SECOND'|
|INTERVAL YEAR [(n)]|VARCHAR(21)|'0YEAR'|
|INTERVAL YEAR [(n)] TO MONTH|VARCHAR(21)|'0YEAR'|
|CHAR[(n)]|CHAR|''|
|CHARACTER(n) CHARACTER SET GRAPHIC|-|NOT SUPPORTED|
|CLOB|-|NOT SUPPORTED|
|CHAR VARYING(n)|VARCHAR|''|
|LONG VARCHAR|-|NOT SUPPORTED|
|LONG VARCHAR CHARACTER SET GRAPHIC|-|NOT SUPPORTED|
|VARCHAR(n)|VARCHAR|''|
|VARCHAR(n) CHARACTER SET GRAPHIC|-|NOT SUPPORTED|
|PERIOD(DATE)|VARCHAR(24)|NOT SUPPORTED|
|PERIOD(TIME [(n)])|VARCHAR(24)|NOT SUPPORTED|
|PERIOD(TIMESTAMP [(n)])|VARCHAR(24)|NOT SUPPORTED|

### Sample Source Patterns[¶](#id31)

#### Teradata[¶](#id32)

##### Query[¶](#query)

```
 CREATE TABLE SAMPLE_TABLE
(
    ID INT,

    -- Numeric Types
    big_integer_col BIGINT WITH DEFAULT,
    byteint_col BYTEINT WITH DEFAULT,
    decimal_col DECIMAL(10,2) WITH DEFAULT,
    double_precision_col DOUBLE PRECISION WITH DEFAULT,
    float_col FLOAT WITH DEFAULT,
    integer_col INTEGER WITH DEFAULT,
    number_col NUMBER WITH DEFAULT,
    numeric_col NUMERIC(10,2) WITH DEFAULT,
    real_col REAL WITH DEFAULT,
    smallint_col SMALLINT WITH DEFAULT,

    -- Character Types
    char_col CHAR(50) WITH DEFAULT,
    character_col CHARACTER(50) WITH DEFAULT,
    --clob_col CLOB,
    char_varying_col CHAR VARYING(100) WITH DEFAULT,
    --long_varchar_col LONG VARCHAR WITH DEFAULT,
    --long_varchar_graphic_col LONG VARCHAR CHARACTER SET GRAPHIC WITH DEFAULT,
    varchar_col VARCHAR(255) WITH DEFAULT,
    --varchar_graphic_col VARCHAR(255) CHARACTER SET GRAPHIC WITH DEFAULT,

    -- Date and Time Types
    date_col DATE WITH DEFAULT,
    time_col TIME WITH DEFAULT,
    time_precision_col TIME(6) WITH DEFAULT,
    timestamp_col TIMESTAMP WITH DEFAULT,
    timestamp_precision_col TIMESTAMP(6) WITH DEFAULT,
    tz_timestamp_col TIMESTAMP WITH TIME ZONE WITH DEFAULT,
    tz_timestamp_precision_col TIMESTAMP(6) WITH TIME ZONE WITH DEFAULT,
    interval_col INTERVAL DAY(4) WITH DEFAULT,
    interval_day_to_hour_col INTERVAL DAY(4) TO HOUR WITH DEFAULT,
    interval_hour_col INTERVAL HOUR(2) WITH DEFAULT,
    interval_minute_col INTERVAL MINUTE(2) WITH DEFAULT,
    interval_month_col INTERVAL MONTH WITH DEFAULT,
    interval_second_col INTERVAL SECOND(2) WITH DEFAULT,
    interval_year_col INTERVAL YEAR(4) WITH DEFAULT,

    -- Binary Types
    -- blob_col BLOB(1000),
    byte_col BYTE(1000) WITH DEFAULT,
    varbyte_col VARBYTE(1000) WITH DEFAULT
);
```

##### Snowflake [¶](#id33)

##### Query[¶](#id34)

```
 CREATE OR REPLACE TABLE SAMPLE_TABLE
(
    ID INT,
    -- Numeric Types
    big_integer_col BIGINT DEFAULT 0,
    byteint_col BYTEINT DEFAULT 0,
    decimal_col DECIMAL(10,2) DEFAULT 0,
    double_precision_col DOUBLE PRECISION DEFAULT 0,
    float_col FLOAT DEFAULT 0,
    integer_col INTEGER DEFAULT 0,
    number_col NUMBER(38, 18) DEFAULT 0,
    numeric_col NUMERIC(10,2) DEFAULT 0,
    real_col REAL DEFAULT 0,
    smallint_col SMALLINT DEFAULT 0,
    -- Character Types
    char_col CHAR(50) DEFAULT '',
    character_col CHARACTER(50) DEFAULT '',
    --clob_col CLOB,
    char_varying_col CHAR VARYING(100) DEFAULT '',
    --long_varchar_col LONG VARCHAR WITH DEFAULT,
    --long_varchar_graphic_col LONG VARCHAR CHARACTER SET GRAPHIC WITH DEFAULT,
    varchar_col VARCHAR(255) DEFAULT '',
    --varchar_graphic_col VARCHAR(255) CHARACTER SET GRAPHIC WITH DEFAULT,

    -- Date and Time Types
    date_col DATE DEFAULT CURRENT_DATE,
    time_col TIME DEFAULT CURRENT_TIME,
    time_precision_col TIME(6) DEFAULT CURRENT_TIME(6),
    timestamp_col TIMESTAMP
--                            !!!RESOLVE EWI!!! /*** SSC-EWI-0013 - EXCEPTION THROWN WHILE CONVERTING ITEM: Mobilize.T12Data.Sql.Ast.TdWithDefaultAttribute. LINE: 31 OF FILE: /Users/hbadillabonilla/Documents/Workspace/migrations-snowconvert/Tools/DocVerifier/out/temp/CUebOYutwG1Dca8jb0Fo/8921d487/SOURCE/Teradata_01.sql ***/!!!
--                            WITH DEFAULT
                                        ,
    timestamp_precision_col TIMESTAMP(6)
--                                         !!!RESOLVE EWI!!! /*** SSC-EWI-0013 - EXCEPTION THROWN WHILE CONVERTING ITEM: Mobilize.T12Data.Sql.Ast.TdWithDefaultAttribute. LINE: 32 OF FILE: /Users/hbadillabonilla/Documents/Workspace/migrations-snowconvert/Tools/DocVerifier/out/temp/CUebOYutwG1Dca8jb0Fo/8921d487/SOURCE/Teradata_01.sql ***/!!!
-- WITH DEFAULT
             ,
    tz_timestamp_col TIMESTAMP_TZ
--                                  WITH DEFAULT
--    !!!RESOLVE EWI!!! /*** SSC-EWI-0021 - WITH DEFAULT FOR 'TIMESTAMP WITH TIME ZONE' NOT SUPPORTED IN SNOWFLAKE ***/!!!
                                                                                                                        ,
    tz_timestamp_precision_col TIMESTAMP_TZ(6)
--                                               WITH DEFAULT
--    !!!RESOLVE EWI!!! /*** SSC-EWI-0021 - WITH DEFAULT FOR 'TIMESTAMP(6) WITH TIME ZONE' NOT SUPPORTED IN SNOWFLAKE ***/!!!
                                                                                                                           ,
    interval_col VARCHAR(21) !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - INTERVAL DAY(4) DATA TYPE CONVERTED TO VARCHAR ***/!!! DEFAULT '0DAY',
    interval_day_to_hour_col VARCHAR(21) !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - INTERVAL DAY(4) TO HOUR DATA TYPE CONVERTED TO VARCHAR ***/!!! DEFAULT '0DAY',
    interval_hour_col VARCHAR(21) !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - INTERVAL HOUR(2) DATA TYPE CONVERTED TO VARCHAR ***/!!! DEFAULT '0HOUR',
    interval_minute_col VARCHAR(21) !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - INTERVAL MINUTE(2) DATA TYPE CONVERTED TO VARCHAR ***/!!! DEFAULT '0MINUTE',
    interval_month_col VARCHAR(21) !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - INTERVAL MONTH DATA TYPE CONVERTED TO VARCHAR ***/!!! DEFAULT '0MONTH',
    interval_second_col VARCHAR(21) !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - INTERVAL SECOND(2) DATA TYPE CONVERTED TO VARCHAR ***/!!! DEFAULT '0SECOND',
    interval_year_col VARCHAR(21) !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - INTERVAL YEAR(4) DATA TYPE CONVERTED TO VARCHAR ***/!!! DEFAULT '0YEAR',
    -- Binary Types
    -- blob_col BLOB(1000),
    byte_col BINARY
--                    WITH DEFAULT
--    !!!RESOLVE EWI!!! /*** SSC-EWI-0021 - WITH DEFAULT FOR 'BYTE(1000)' NOT SUPPORTED IN SNOWFLAKE ***/!!!
                                                                                                          ,
    varbyte_col BINARY(1000)
--                             WITH DEFAULT
--    !!!RESOLVE EWI!!! /*** SSC-EWI-0021 - WITH DEFAULT FOR 'VARBYTE(1000)' NOT SUPPORTED IN SNOWFLAKE ***/!!!
)
```

### Known Issues[¶](#id35)

#### 1. Unsupported types[¶](#unsupported-types)

As shown in the table in the description table, some types are not supported and no default value
will be set when transforming the `WITH DEFAULT` clause.

### Related EWIs[¶](#id36)

1. [SSC-EWI-0021](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0021):
   Not Supported in Snowflake.
2. [SSC-EWI-0036](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0036):
   Data type converted to another data type.

## CREATE MACRO[¶](#create-macro)

Translation reference to convert Teradata CREATE MACRO to Snowflake Scripting

### Description [¶](#id37)

The Teradata `CREATE MACRO` defines one or more statements that are commonly used or that perform a
complex operation, thus avoiding writing the same sequence of statements multiple times. The macro
is executed when it is called by the EXECUTE statement.

For more information about `CREATE MACRO` click
[here](https://docs.teradata.com/r/Teradata-Database-SQL-Data-Definition-Language-Syntax-and-Examples/June-2017/Macro-Statements/CREATE-MACRO-and-REPLACE-MACRO).

```
 CREATE MACRO <macroname> [(parameter1, parameter2,...)] (
   <sql_statements>
);

[ EXECUTE | EXEC ] <macroname>;
```

### Sample Source Patterns [¶](#id38)

#### Setup data[¶](#setup-data)

The following code is necessary to execute the sample patterns present in this section.

##### Teradata[¶](#id39)

```
 CREATE TABLE DEPOSIT
(
    ACCOUNTNO NUMBER,
    ACCOUNTNAME VARCHAR(100)
);

INSERT INTO DEPOSIT VALUES (1, 'Account 1');
INSERT INTO DEPOSIT VALUES (2, 'Account 2');
INSERT INTO DEPOSIT VALUES (3, 'Account 3');
INSERT INTO DEPOSIT VALUES (4, 'Account 4');
```

##### Snowflake[¶](#id40)

```
 CREATE OR REPLACE TABLE DEPOSIT
(
    ACCOUNTNO NUMBER(38, 18),
    ACCOUNTNAME VARCHAR(100)
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;

INSERT INTO DEPOSIT
VALUES (1, 'Account 1');

INSERT INTO DEPOSIT
VALUES (2, 'Account 2');

INSERT INTO DEPOSIT
VALUES (3, 'Account 3');

INSERT INTO DEPOSIT
VALUES (4, 'Account 4');
```

#### Basic Macro [¶](#basic-macro)

Since there is no macro object in Snowflake, the conversion tool transforms Teradata macros into
Snowflake Scripting stored procedures. Besides, to replicate the functionality of the returned
result set, in Snowflake Scripting, the query that is supposed to return a data set from a macro is
assigned to a `RESULTSET` variable which will then be returned.

##### Teradata [¶](#id41)

##### Query[¶](#id42)

```
 REPLACE MACRO DEPOSITID (ID INT)
AS
(
  SELECT * FROM DEPOSIT WHERE ACCOUNTNO=:ID;
);

EXECUTE DEPOSITID(2);
```

##### Result[¶](#result)

```
+--------------+--------------+
<!-- prettier-ignore -->
|ACCOUNTNO|ACCOUNTNAME|
|--------------+--------------|
|2|Account 2|
+--------------+--------------+
```

##### Snowflake Scripting [¶](#snowflake-scripting)

##### Query[¶](#id43)

```
 CREATE OR REPLACE PROCEDURE DEPOSITID (ID FLOAT)
RETURNS TABLE ()
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        LET res RESULTSET := (SELECT * FROM DEPOSIT WHERE ACCOUNTNO=:ID);
        RETURN TABLE(res);
    END;
$$;

CALL DEPOSITID(2);
```

##### Result[¶](#id44)

```
+--------------+--------------+
<!-- prettier-ignore -->
|ACCOUNTNO|ACCOUNTNAME|
|--------------+--------------|
|2|Account 2|
+--------------+--------------+
```

#### Macro Calls Another Macro [¶](#macro-calls-another-macro)

SnowConvert AI supports the scenario where a macro calls another macro and, by transitivity, a
result set is returned by getting the results from Snowflake’s `RESULT_SCAN(LAST_QUERY_ID())`.

##### Teradata[¶](#id45)

##### Query[¶](#id46)

```
 REPLACE MACRO MacroCallOtherMacro (ID INT)
AS
(
    EXECUTE DEPOSITID(:ID);
);

EXECUTE MacroCallOtherMacro(2);
```

##### Result[¶](#id47)

```
+--------------+--------------+
<!-- prettier-ignore -->
|ACCOUNTNO|ACCOUNTNAME|
|--------------+--------------|
|2|Account 2|
+--------------+--------------+
```

##### Snowflake Scripting [¶](#id48)

##### Query[¶](#id49)

```
 CREATE OR REPLACE PROCEDURE MacroCallOtherMacro (ID FLOAT)
RETURNS TABLE (
)
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "09/09/2024" }}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        CALL DEPOSITID(:ID);
        LET res RESULTSET :=
        (
            SELECT
                *
            FROM
                TABLE(RESULT_SCAN(LAST_QUERY_ID()))
        );
        RETURN TABLE(res);
    END;
$$;

CALL MacroCallOtherMacro(2);
```

##### Result[¶](#id50)

```
+--------------+--------------+
<!-- prettier-ignore -->
|ACCOUNTNO|ACCOUNTNAME|
|--------------+--------------|
|2|Account 2|
+--------------+--------------+
```

#### Macro with no result set[¶](#macro-with-no-result-set)

Not all macros are intended to return a result set. The mentioned scenario is also supported.

##### Teradata[¶](#id51)

##### Query[¶](#id52)

```
 REPLACE MACRO MacroWithoutSelect (ACCOUNTNO NUMBER, ACCOUNTNAME VARCHAR(100))
AS
(
  INSERT INTO DEPOSIT VALUES (:ACCOUNTNO, :ACCOUNTNAME);
);

EXECUTE MacroWithoutSelect(5, 'Account 5');
SELECT * FROM DEPOSIT;
```

##### Result[¶](#id53)

```
+--------------+--------------+
<!-- prettier-ignore -->
|ACCOUNTNO|ACCOUNTNAME|
|--------------+--------------|
|1|Account 1|
+--------------+--------------+
<!-- prettier-ignore -->
|2|Account 2|
+--------------+--------------+
<!-- prettier-ignore -->
|3|Account 3|
+--------------+--------------+
<!-- prettier-ignore -->
|4|Account 4|
+--------------+--------------+
<!-- prettier-ignore -->
|5|Account 5|
+--------------+--------------+
```

##### Snowflake Scripting [¶](#id54)

##### Query[¶](#id55)

```
 CREATE OR REPLACE PROCEDURE MacroWithoutSelect (ACCOUNTNO FLOAT, ACCOUNTNAME VARCHAR(100))
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        INSERT INTO DEPOSIT
        VALUES (:ACCOUNTNO, :ACCOUNTNAME);
    END;
$$;

CALL MacroWithoutSelect(5, 'Account 5');
SELECT * FROM DEPOSIT;
```

##### Result[¶](#id56)

```
+--------------+--------------+
<!-- prettier-ignore -->
|ACCOUNTNO|ACCOUNTNAME|
|--------------+--------------|
|1|Account 1|
+--------------+--------------+
<!-- prettier-ignore -->
|2|Account 2|
+--------------+--------------+
<!-- prettier-ignore -->
|3|Account 3|
+--------------+--------------+
<!-- prettier-ignore -->
|4|Account 4|
+--------------+--------------+
<!-- prettier-ignore -->
|5|Account 5|
+--------------+--------------+
```

#### Macro returns multiple result sets[¶](#macro-returns-multiple-result-sets)

In Teradata, macros can return more than one result set from a single macro.

Snowflake Scripting procedures only allow one result set to be returned per procedure. To replicate
Teradata behavior, when there are two or more result sets to return, they are stored in temporary
tables. The Snowflake Scripting procedure will return an array containing the name of the temporary
tables.

##### Teradata[¶](#id57)

##### Query[¶](#id58)

```
 REPLACE MACRO DEPOSITID (ID INT)
AS
(
  SELECT * FROM DEPOSIT WHERE ACCOUNTNO=4;
  SELECT * FROM DEPOSIT WHERE ACCOUNTNO=:ID;
  EXECUTE DEPOSITID(:ID);
);

EXECUTE DEPOSITID(2);
```

##### Result Set 1[¶](#result-set-1)

```
+--------------+--------------+
<!-- prettier-ignore -->
|ACCOUNTNO|ACCOUNTNAME|
|--------------+--------------|
|4|Account 4|
+--------------+--------------+
```

##### Result Set 2[¶](#result-set-2)

```
+--------------+--------------+
<!-- prettier-ignore -->
|ACCOUNTNO|ACCOUNTNAME|
|--------------+--------------|
|2|Account 2|
+--------------+--------------+
```

##### Snowflake Scripting [¶](#id59)

##### Query[¶](#id60)

```
 CREATE OR REPLACE PROCEDURE DEPOSITID (ID FLOAT)
RETURNS ARRAY
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "09/09/2024" }}'
EXECUTE AS CALLER
AS
$$
  DECLARE
    return_arr ARRAY := array_construct();
    tbl_nm VARCHAR;
  BEGIN
    tbl_nm := 'RESULTSET_' || REPLACE(UPPER(UUID_STRING()), '-', '_');
    CREATE OR REPLACE TEMPORARY TABLE IDENTIFIER(:tbl_nm) AS
      SELECT
        * FROM
        DEPOSIT
      WHERE ACCOUNTNO=4;
    return_arr := array_append(return_arr, :tbl_nm);
    tbl_nm := 'RESULTSET_' || REPLACE(UPPER(UUID_STRING()), '-', '_');
    CREATE OR REPLACE TEMPORARY TABLE IDENTIFIER(:tbl_nm) AS
      SELECT
        * FROM
        DEPOSIT
      WHERE ACCOUNTNO=:ID;
    return_arr := array_append(return_arr, :tbl_nm);
    CALL DEPOSITID(:ID);
    tbl_nm := 'RESULTSET_' || REPLACE(UPPER(UUID_STRING()), '-', '_');
    CREATE OR REPLACE TEMPORARY TABLE IDENTIFIER(:tbl_nm) AS
      SELECT
        *
      FROM
        TABLE(RESULT_SCAN(LAST_QUERY_ID()));
    return_arr := array_append(return_arr, :tbl_nm);
    --** SSC-FDM-0020 - MULTIPLE RESULT SETS ARE RETURNED IN TEMPORARY TABLES **
    RETURN return_arr;
  END;
$$;

CALL DEPOSITID(2);
```

##### Result Set 1[¶](#id61)

```
+-----------------------------------------------------+
<!-- prettier-ignore -->
|DEPOSIDID|
|---|
|[|
|"RESULTSET_93D50CBB_F22C_418A_A88C_4E1DE101B500",|
|"RESULTSET_6BDE39D7_0554_406E_B52F_D9E863A3F15C"|
|]|
+-----------------------------------------------------+
```

##### Visualize Result Rets[¶](#visualize-result-rets)

Executing the above procedure on Snowflake, an array with temporary table names in it will be
returned:

```
[ "RESULTSET_93D50CBB_F22C_418A_A88C_4E1DE101B500",
  "RESULTSET_6BDE39D7_0554_406E_B52F_D9E863A3F15C"]
```

It is necessary to execute the following queries to display the result sets just like in Teradata.

##### Query[¶](#id62)

```
 SELECT * FROM table('RESULTSET_93D50CBB_F22C_418A_A88C_4E1DE101B500');
SELECT * FROM table('RESULTSET_6BDE39D7_0554_406E_B52F_D9E863A3F15C');
```

##### Result Set 1[¶](#id63)

```
+--------------+--------------+
<!-- prettier-ignore -->
|ACCOUNTNO|ACCOUNTNAME|
|--------------+--------------|
|4|Account 4|
+--------------+--------------+
```

##### Result Set 2[¶](#id64)

```
+--------------+--------------+
<!-- prettier-ignore -->
|ACCOUNTNO|ACCOUNTNAME|
|--------------+--------------|
|2|Account 2|
+--------------+--------------+
```

### Known Issues [¶](#id65)

No issues were found.

### Related EWIs[¶](#id66)

## CREATE PROCEDURE[¶](#create-procedure)

Translation reference to convert Teradata CREATE PROCEDURE to Snowflake Scripting

Description

The Teradata `CREATE PROCEDURE` and `REPLACE PROCEDURE` statement generates or replaces a stored
procedure implementation and compiles it.

For more information about `CREATE PROCEDURE` or `REPLACE PROCEDURE`
[click here](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/SQL-Data-Definition-Language-Syntax-and-Examples/Procedure-Statements/CREATE-PROCEDURE-and-REPLACE-PROCEDURE-SQL-Form).

```
 -- Create/replace procedure syntax
{CREATE | REPLACE} PROCEDURE [database_name. | user_name.] procedure_name
    ([<parameter_definition>[, ...n]])
[<SQL_data_access>]
[DYNAMIC RESULT SETS number_of_sets]
[SQL SECURITY <privilege_option>]
statement;


<parameter_definition> := [IN | OUT | INOUT] parameter_name data_type

<SQL_data_access> := {CONTAINS SQL | MODIFIES SQL DATA | READS SQL DATA}

<privilege_option> := {CREATOR | DEFINER | INVOKER | OWNER}
```

### Sample Source Patterns [¶](#id67)

#### Setup data[¶](#id68)

The following code is necessary to execute the sample patterns present in this section.

##### Teradata[¶](#id69)

```
 CREATE TABLE inventory (
    product_name VARCHAR(50),
    price INTEGER
);

INSERT INTO inventory VALUES ('Bread', 50);
INSERT INTO inventory VALUES ('Tuna', 150);
INSERT INTO inventory VALUES ('Gum', 20);
INSERT INTO inventory VALUES ('Milk', 80);
```

##### Snowflake[¶](#id70)

```
 CREATE OR REPLACE TABLE inventory (
    product_name VARCHAR(50),
    price INTEGER
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;

INSERT INTO inventory
VALUES ('Bread', 50);

INSERT INTO inventory
VALUES ('Tuna', 150);

INSERT INTO inventory
VALUES ('Gum', 20);

INSERT INTO inventory
VALUES ('Milk', 80);
```

#### Basic Procedure [¶](#basic-procedure)

##### Teradata [¶](#id71)

##### Query[¶](#id72)

```
 REPLACE PROCEDURE BasicProcedure(IN counterValue INTEGER)
BEGIN
    DECLARE productName VARCHAR(50);
    DECLARE productPrice INTEGER DEFAULT 0;
    DECLARE whileCounter INTEGER DEFAULT 0;
    SET productName = 'Salt';
    WHILE (whileCounter < counterValue) DO
        SET productPrice = 10 + productPrice;
        SET whileCounter = whileCounter + 1;
    END WHILE;
    INSERT INTO inventory VALUES (productName, productPrice);
END;

CALL BasicProcedure(5);
SELECT product_name, price FROM inventory WHERE product_name = 'Salt';
```

##### Result[¶](#id73)

```
+--------------+--------------+
<!-- prettier-ignore -->
|product_name|price|
|--------------+--------------|
|Salt|50|
+--------------+--------------+
```

##### Snowflake Scripting [¶](#id74)

##### Query[¶](#id75)

```
 CREATE OR REPLACE PROCEDURE BasicProcedure (COUNTERVALUE INTEGER)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/10/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        productName VARCHAR(50);
        productPrice INTEGER DEFAULT 0;
        whileCounter INTEGER DEFAULT 0;
    BEGIN



        productName := 'Salt';
            WHILE (:whileCounter < :counterValue) LOOP
            productPrice := 10 + productPrice;
            whileCounter := whileCounter + 1;
        END LOOP;
        INSERT INTO inventory
        VALUES (:productName, :productPrice);
    END;
$$;

CALL BasicProcedure(5);

SELECT
    product_name,
    price FROM
    inventory
WHERE
    UPPER(RTRIM( product_name)) = UPPER(RTRIM('Salt'));
```

##### Result[¶](#id76)

```
+--------------+--------------+
<!-- prettier-ignore -->
|product_name|price|
|--------------+--------------|
|Salt|50|
+--------------+--------------+
```

#### Single out parameter [¶](#single-out-parameter)

##### Teradata[¶](#id77)

##### Query[¶](#id78)

```
 REPLACE PROCEDURE procedureLabelSingle(OUT Message VARCHAR(100))
BEGIN
    set Message = 'Assignment value. Thanks';
END;

CALL procedureLabelSingle(?);
```

##### Result[¶](#id79)

```
Message                 |
------------------------+
Assignment value. Thanks|
```

##### Snowflake Scripting [¶](#id80)

##### Query[¶](#id81)

```
 CREATE OR REPLACE PROCEDURE procedureLabelSingle (MESSAGE OUT VARCHAR(100))
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/23/2024" }}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        Message := 'Assignment value. Thanks';
    END;
$$;

CALL procedureLabelSingle(?);
```

##### Result[¶](#id82)

```
+───────────────────────────────+
<!-- prettier-ignore -->
|PROCEDURELABELSINGLE|
+───────────────────────────────+
<!-- prettier-ignore -->
|""Assignment value. Thanks""|
+───────────────────────────────+
```

#### Multiple out parameter [¶](#multiple-out-parameter)

##### Teradata[¶](#id83)

##### Query[¶](#id84)

```
 REPLACE PROCEDURE procedureLabelMultiple(OUT Message VARCHAR(100), OUT Message2 VARCHAR(100))
BEGIN
    set Message = 'Assignment value. Thanks';
    set Message2 = 'Assignment value2. Thanks';
END;

CALL procedureLabelSingle(?, ?);
```

##### Result[¶](#id85)

```
1                       |2                        |
------------------------+-------------------------+
Assignment value. Thanks|Assignment value2. Thanks|
```

##### Snowflake Scripting [¶](#id86)

##### Query[¶](#id87)

```
 CREATE OR REPLACE PROCEDURE procedureLabelMultiple (MESSAGE OUT VARCHAR(100), MESSAGE2 OUT VARCHAR(100))
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        Message := 'Assignment value. Thanks';
        Message2 := 'Assignment value2. Thanks';
    END;
$$;

--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "procedureLabelSingle" **
CALL procedureLabelSingle(?, ?);
```

##### Result[¶](#id88)

```
+─────────────────────────+────────────────────────────────+
<!-- prettier-ignore -->
|PROCEDURELABELMULTIPLE||
+─────────────────────────+────────────────────────────────+
<!-- prettier-ignore -->
|"{||
|""Message""|""Assignment value. Thanks"",|
|""Message2""|""Assignment value2. Thanks""|
|}"||
+─────────────────────────+────────────────────────────────+
```

#### Multiple out parameter with dynamic result sets [¶](#multiple-out-parameter-with-dynamic-result-sets)

##### Teradata[¶](#id89)

##### Query[¶](#id90)

```
 REPLACE PROCEDURE Procedure1(out product_name VARCHAR(50), out price integer)
DYNAMIC RESULT SETS 2
BEGIN
	DECLARE result_set CURSOR WITH RETURN ONLY FOR
	SELECT * FROM inventory;
    DECLARE result_set2 CURSOR WITH RETURN ONLY FOR
	SELECT * FROM inventory;
    SET price = 100;
    SET product_name = 'another2';
	OPEN result_set2;
	OPEN result_set;
END;

REPLACE PROCEDURE Procedure2()
BEGIN
 DECLARE price INTEGER;
 DECLARE productName varchar(10);
 CALL Procedure1(productName, price);
 INSERT INTO inventory VALUES(:productName, :price);
END;

CALL Procedure2();
```

##### Result[¶](#id91)

![](../../../.gitbook/assets/image (223) (1).png)

##### Snowflake Scripting [¶](#id92)

##### Query[¶](#id93)

```
 --** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "inventory" **
CREATE OR REPLACE PROCEDURE Procedure1 (PRODUCT_NAME OUT VARCHAR(50), PRICE OUT integer)
RETURNS ARRAY
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
	DECLARE
		tbl_result_set VARCHAR;
		tbl_result_set2 VARCHAR;
		return_arr ARRAY := array_construct();
	BEGIN
		tbl_result_set := 'RESULTSET_' || REPLACE(UPPER(UUID_STRING()), '-', '_');
		CREATE OR REPLACE TEMPORARY TABLE IDENTIFIER(:tbl_result_set) AS
			SELECT
				* FROM
				inventory;
		LET result_set CURSOR
		FOR
			SELECT
				*
			FROM
				IDENTIFIER(?);
		tbl_result_set2 := 'RESULTSET_' || REPLACE(UPPER(UUID_STRING()), '-', '_');
		CREATE OR REPLACE TEMPORARY TABLE IDENTIFIER(:tbl_result_set2) AS
			SELECT
				* FROM
				inventory;
		LET result_set2 CURSOR
		FOR
			SELECT
				*
			FROM
				IDENTIFIER(?);
				price := 100;
				product_name := 'another2';
				OPEN result_set2 USING (tbl_result_set2);
				return_arr := array_append(return_arr, :tbl_result_set2);
				OPEN result_set USING (tbl_result_set);
				return_arr := array_append(return_arr, :tbl_result_set);
				--** SSC-FDM-0020 - MULTIPLE RESULT SETS ARE RETURNED IN TEMPORARY TABLES **
				RETURN return_arr;
	END;
$$;

--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "inventory" **
CREATE OR REPLACE PROCEDURE Procedure2 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
	DECLARE
				price INTEGER;
				productName varchar(10);
	BEGIN


				CALL Procedure1(:productName, :price);
				INSERT INTO inventory
				VALUES (:productName, :price);
	END;
$$;

CALL Procedure2();
```

### Known Issues [¶](#id94)

**1. SQL Data Access**

By default, Snowflake procedures support the execution of any kind of SQL statements, including data
reading or modification statements, making the SQL data access clause non-relevant. This clause will
be ignored when converting the procedure.

**2. Top Level Objects in Assessment Report**

Elements (Temporal tables or Views) inside Stored Procedures are being counted in the Assessment
report as Top Level Objects. The SnowConvert AI team is now working on a fix for this scenario.

### Related EWIs[¶](#id95)

1. [SSC-EWI-0073](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0073):
   Pending Functional Equivalence Review.
2. [SSC-FDM-0020](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0020):
   Multiple result sets are returned in temporary tables.
