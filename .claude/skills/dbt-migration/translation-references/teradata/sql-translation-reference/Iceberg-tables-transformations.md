---
description:
  This section covers the transformation of tables into Snowflake-managed Iceberg tables, performed
  by SnowConvert AI when the conversion setting Table Translation is used.
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/teradata/sql-translation-reference/Iceberg-tables-transformations
title: SnowConvert AI - Teradata - Iceberg Tables Transformations | Snowflake Documentation
---

## Temporary tables[¶](#temporary-tables)

The temporary option is not supported in Iceberg tables, they will be preserved as temporary.

### Teradata[¶](#teradata)

```
CREATE VOLATILE TABLE myTable
(
  column1 NUMBER(15,0)
);
```

### Snowflake[¶](#snowflake)

```
CREATE OR REPLACE TEMPORARY TABLE myTable
(
 column1 NUMBER(15,0)
)
;
```

## Other tables[¶](#other-tables)

Other table types are going to be transformed into Iceberg tables.

### Teradata[¶](#id1)

```
CREATE TABLE myTable
(
  column1 NUMBER(15,0)
);
```

### Snowflake[¶](#id2)

```
CREATE OR REPLACE ICEBERG TABLE myTable (
  column1 NUMBER(15, 0)
)
CATALOG = 'SNOWFLAKE'
;
```

## Data types[¶](#data-types)

The following column data type conversions are applied to comply with the Iceberg tables type
requirements and restrictions.

**Note:**

Data types in the first column are the **Snowflake** data types that would normally be created if
the table target is not Iceberg, while second column shows the data type generated for Iceberg
tables.

<!-- prettier-ignore -->
|Original target type|New target type|
|---|---|
|TIME(X) TIMESTAMP(X) DATETIME(X) TIMESTAMP_LTZ(X) TIMESTAMP_NTZ(X) TIME TIMESTAMP DATETIME TIMESTAMP_LTZ TIMESTAMP_NTZ where X != 6|TIME(6) TIMESTAMP(6) DATETIME(6) TIMESTAMP_LTZ(6) TIMESTAMP_NTZ(6) TIME(6) TIMESTAMP(6) DATETIME(6) TIMESTAMP_LTZ(6) TIMESTAMP_NTZ(6)|
|VARCHAR(X) STRING(X) TEXT(X) NVARCHAR(X) NVARCHAR2(X) CHAR VARYING(X) NCHAR VARYING(X)|VARCHAR STRING TEXT NVARCHAR NVARCHAR2 CHAR VARYING NCHAR VARYING|
|CHAR[(n)] CHARACTER[(n)] NCHAR[(n)]|VARCHAR VARCHAR VARCHAR|
|NUMBER DECIMAL DEC NUMERIC INT INTEGER BIGINT SMALLINT TINYINT BYTEINT|NUMBER(38,0) DECIMAL(38,0) DEC(38,0) NUMERIC(38,0) NUMBER(38,0) NUMBER(38,0) NUMBER(38,0) NUMBER(38,0) NUMBER(38,0) NUMBER(38,0)|
|FLOAT FLOAT4 FLOAT8|DOUBLE DOUBLE DOUBLE|
|VARBINARY[(n)]|BINARY[(n)]|

## PARTITION BY[¶](#partition-by)

The following PARTITION BY cases are supported:

### PARTITION BY name[¶](#partition-by-name)

Left as is.

#### Teradata[¶](#id3)

```
CREATE TABLE myTable
(
  customerName VARCHAR(30),
  areaCode INTEGER
)
PARTITION BY areaCode;
```

#### Snowflake[¶](#id4)

```
CREATE OR REPLACE ICEBERG TABLE myTable (
  customerName VARCHAR,
  areaCode NUMBER(38, 0)
)
PARTITION BY (areaCode)
CATALOG = 'SNOWFLAKE'
;
```

### PARTITION BY CASE_N (equality over single column)[¶](#partition-by-case-n-equality-over-single-column)

When the CASE_N function follows this pattern:

```
PARTITION BY CASE_N(
  column_name = value1,
  column_name = value2,
  ...
  column_name = valueN)
```

It will be transformed to a PARTITION BY column_name.

#### Teradata[¶](#id5)

```
CREATE TABLE myTable
(
  customerName VARCHAR(30),
  weekDay VARCHAR(20)
)
PARTITION BY CASE_N(
weekDay =  'Sunday',
weekDay =  'Monday',
weekDay =  'Tuesday',
weekDay =  'Wednesday',
weekDay =  'Thursday',
weekDay =  'Friday',
weekDay =  'Saturday',
 NO CASE OR UNKNOWN);
```

#### Snowflake[¶](#id6)

```
CREATE OR REPLACE ICEBERG TABLE myTable (
  customerName VARCHAR,
  weekDay VARCHAR
)
PARTITION BY (weekDay)
CATALOG = 'SNOWFLAKE'
;
```

### PARTITION BY RANGE_N[¶](#partition-by-range-n)

PARTITION BY RANGE_N is transformed when it matches one of these patterns:

#### Numeric range[¶](#numeric-range)

Pattern:

```
RANGE_N(columnName BETWEEN x AND y EACH z) -- x, y and z must be numeric constants.
```

This case will be changed with a BUCKET partition transform.

##### Teradata[¶](#id7)

```
CREATE TABLE myTable
(
  customerName VARCHAR(30),
  totalPurchases INTEGER
)
PARTITION BY RANGE_N(totalPurchases BETWEEN 5 AND 200 EACH 10);
```

##### Snowflake[¶](#id8)

```
CREATE OR REPLACE ICEBERG TABLE myTable (
  customerName VARCHAR,
  totalPurchases NUMBER(38, 0)
)
PARTITION BY (BUCKET(20, totalPurchases))
CATALOG = 'SNOWFLAKE'
;
```

#### Datetime range[¶](#datetime-range)

Pattern:

```
RANGE_N(columnName BETWEEN date_constant AND date_constant EACH interval_constant) -- Interval qualifier must be YEAR, MONTH, DAY or HOUR
```

This case will be changed with the YEAR, MONTH, DAY or HOUR partition transforms.

##### Teradata[¶](#id9)

```
CREATE TABLE myTable
(
  customerName VARCHAR(30),
  purchaseDate DATE
)
PARTITION BY RANGE_N(purchaseDate BETWEEN DATE '2000-01-01' AND '2100-12-31' EACH INTERVAL '1' MONTH);
```

##### Snowflake[¶](#id10)

```
CREATE OR REPLACE ICEBERG TABLE myTable (
  customerName VARCHAR,
  purchaseDate DATE
)
PARTITION BY (MONTH(purchaseDate))
CATALOG = 'SNOWFLAKE'
;
```

## Known Issues[¶](#known-issues)

### 1. Unsupported data types[¶](#unsupported-data-types)

Current Snowflake support for Iceberg tables does not allow data types like VARIANT or GEOGRAPHY to
be used, tables with these types will be marked with an EWI.

### 2. Unsupported PARTITION BY cases[¶](#unsupported-partition-by-cases)

PARTITION BY cases different than the ones shown in this documentation will not be transformed,
instead, the PARTITION BY clause will be commented out with a PRF.

## Related EWIs[¶](#related-ewis)

1. [SSC-EWI-0115](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0115):
   Iceberg table contains unsupported datatypes
2. [SSC-PRF-0010](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/performance-review/generalPRF#ssc-prf-0010):
   Partition by removed, at least one of the specified expressions have no iceberg partition
   transform equivalent
