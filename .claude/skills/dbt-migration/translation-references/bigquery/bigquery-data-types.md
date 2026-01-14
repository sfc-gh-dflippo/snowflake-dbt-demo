---
description:
  Snowflake provides support for the majority of fundamental SQL data types, with specific
  restrictions, across various SQL constructs including columns, local variables, expressions, and
  parameters.
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/bigquery/bigquery-data-types
title: SnowConvert AI - BigQuery - Data types | Snowflake Documentation
---

## Boolean Data Type[¶](#boolean-data-type)

<!-- prettier-ignore -->
|BigQuery|Snowflake|Notes|
|---|---|---|
|[BOOL/BOOLEAN](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#boolean_type)|[BOOLEAN](https://docs.snowflake.com/en/sql-reference/data-types-logical#boolean)||

## Bytes Data Type[¶](#bytes-data-type)

<!-- prettier-ignore -->
|BigQuery|Snowflake|Notes|
|---|---|---|
|[BYTES](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#bytes_type)|[BINARY](https://docs.snowflake.com/en/sql-reference/data-types-text#binary)|BYTES data type is **not supported** in Snowflake. BINARY is used instead. For more information, please refer to the [BYTES](#bytes) data type documentation.|

## Datetime Data Types[¶](#datetime-data-types)

<!-- prettier-ignore -->
|BigQuery|Snowflake|Notes|
|---|---|---|
|[DATE](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#date_type)|[DATE](https://docs.snowflake.com/en/sql-reference/data-types-datetime#date)||
|[DATETIME](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#date_type)|[DATETIME](https://docs.snowflake.com/en/sql-reference/data-types-datetime#datetime)|DATETIME is an alias for TIMESTAMP_NTZ in Snowflake.|
|[TIMESTAMP](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#timestamp_type)|[TIMESTAMP_TZ](https://docs.snowflake.com/en/sql-reference/data-types-datetime#timestamp-ltz-timestamp-ntz-timestamp-tz)|TIMESTAMP data type is converted to TIMESTAMP_TZ. For more information, please refer to the TIMESTAMP data type documentation.|
|[TIME](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#time_type)|[TIME](https://docs.snowflake.com/en/sql-reference/data-types-datetime#time)||

## Geography Data Type[¶](#geography-data-type)

<!-- prettier-ignore -->
|BigQuery|Snowflake|Notes|
|---|---|---|
|[GEOGRAPHY](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#geography_type)|[GEOGRAPHY](https://docs.snowflake.com/en/sql-reference/data-types-geospatial#geography-data-type)||

## Interval Data Type[¶](#interval-data-type)

<!-- prettier-ignore -->
|BigQuery|Snowflake|Notes|
|---|---|---|
|[INTERVAL](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#interval_type)|[VARCHAR(30)](https://docs.snowflake.com/en/sql-reference/data-types-text#varchar)|INTERVAL data type is **not supported** in Snowflake. VARCHAR is used instead. For more information, please refer to the [INTERVAL](#interval) data type documentation.|

## Json Data Type[¶](#json-data-type)

<!-- prettier-ignore -->
|BigQuery|Snowflake|Notes|
|---|---|---|
|[JSON](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#json_type)|[VARIANT](https://docs.snowflake.com/en/sql-reference/data-types-semistructured#variant)|JSON data type is **not supported** in Snowflake. VARIANT is used instead. For more information, please refer to the [JSON](#json) data type documentation.|

## Numeric Data Types[¶](#numeric-data-types)

<!-- prettier-ignore -->
|BigQuery|Snowflake|Notes|
|---|---|---|
|[INT64](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#numeric_types)|[INT](https://docs.snowflake.com/en/sql-reference/data-types-numeric#int-integer-bigint-smallint-tinyint-byteint)|INT is an alias for the NUMBER data type in Snowflake. The maximum precision and scale is NUMBER(38,37).|
|[INT](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#numeric_types)|[INT](https://docs.snowflake.com/en/sql-reference/data-types-numeric#int-integer-bigint-smallint-tinyint-byteint)|INT is an alias for the NUMBER data type in Snowflake. The maximum precision and scale is NUMBER(38,37).|
|[SMALLINT](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#numeric_types)|[SMALLINT](https://docs.snowflake.com/en/sql-reference/data-types-numeric#int-integer-bigint-smallint-tinyint-byteint)|SMALLINT is an alias for the NUMBER data type in Snowflake. The maximum precision and scale is NUMBER(38,37).|
|[INTEGER](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#numeric_types)|[INTEGER](https://docs.snowflake.com/en/sql-reference/data-types-numeric#int-integer-bigint-smallint-tinyint-byteint)|INTEGER is an alias for the NUMBER data type in Snowflake. The maximum precision and scale is NUMBER(38,37).|
|[BIGINT](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#numeric_types)|[BIGINT](https://docs.snowflake.com/en/sql-reference/data-types-numeric#int-integer-bigint-smallint-tinyint-byteint)|BIGINT is an alias for the NUMBER data type in Snowflake. The maximum precision and scale is NUMBER(38,37).|
|[TINYINT](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#numeric_types)|[TINYINT](https://docs.snowflake.com/en/sql-reference/data-types-numeric#int-integer-bigint-smallint-tinyint-byteint)|TINYINT is an alias for the NUMBER data type in Snowflake. The maximum precision and scale is NUMBER(38,37).|
|[BYTEINT](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#numeric_types)|[BYTEINT](https://docs.snowflake.com/en/sql-reference/data-types-numeric#int-integer-bigint-smallint-tinyint-byteint)|BYTEINT is an alias for the NUMBER data type in Snowflake. The maximum precision and scale is NUMBER(38,37).|
|[NUMERIC](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#numeric_types)|[NUMERIC](https://docs.snowflake.com/en/sql-reference/data-types-numeric#decimal-dec-numeric)|NUMERIC is an alias for the NUMBER data type in Snowflake. The maximum precision and scale is NUMBER(38,37).|
|[DECIMAL](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#numeric_types)|[DECIMAL](https://docs.snowflake.com/en/sql-reference/data-types-numeric#decimal-dec-numeric)|DECIMAL is an alias for the NUMBER data type in Snowflake. The maximum precision and scale is NUMBER(38,37).|
|[BIGNUMERIC](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#numeric_types)|[NUMERIC](https://docs.snowflake.com/en/sql-reference/data-types-numeric#decimal-dec-numeric)​|Snowflake does not support the BIGNUMERIC data type. Use NUMERIC instead. BIGNUMERIC’s precision 76,76 exceeds Snowflake’s limit (38), resulting in truncation or rounding, which can introduce significant inaccuracies.|
|[BIGDECIMAL](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#numeric_types)|[DECIMAL](https://docs.snowflake.com/en/sql-reference/data-types-numeric#decimal-dec-numeric)|Snowflake does not support the BIGDECIMAL data type. Use NUMERIC instead. BIGDECIMAL’s precision 76,76 exceeds Snowflake’s limit (38), resulting in truncation or rounding, which can introduce significant inaccuracies.|
|[FLOAT64](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#floating_point_types)|[FLOAT](https://docs.snowflake.com/en/sql-reference/data-types-numeric#data-types-for-floating-point-numbers)||

## String Data Types[¶](#string-data-types)

<!-- prettier-ignore -->
|BigQuery|Snowflake|Notes|
|---|---|---|
|[STRING](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#string_type)|[STRING](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#string_type)|STRING is an alias for the VARCHAR data type in Snowflake. VARCHAR holds Unicode UTF-8 characters.|

## ANY TYPE[¶](#any-type)

Translation specification for BigQuery’s ANY TYPE data type

### Description[¶](#description)

The following is an extract of information about the usage of `ANY TYPE` within `CREATE FUNCTION`
statements.

> A parameter with a type equal to `ANY TYPE` can match more than one argument type when the
> function is called.
>
> - If more than one parameter has type `ANY TYPE`, then BigQuery doesn’t enforce any type
>   relationship between these arguments.
> - The function return type cannot be `ANY TYPE`. It must be either omitted, which means to be
>   automatically determined based on `sql_expression`, or an explicit type.
> - Passing the function arguments of types that are incompatible with the function definition
>   results in an error at call time.

### Sample source patterns[¶](#sample-source-patterns)

#### Type definition for UDFs[¶](#type-definition-for-udfs)

`ANY TYPE` can only be found as the type for a function’s parameter. SnowConvert AI automatically
translates `ANY TYPE` to `VARIANT`.

##### BigQuery[¶](#bigquery)

```
CREATE FUNCTION addFourAndDivideAny(x ANY TYPE, y ANY TYPE)
AS (
  (x + 4) / y
);
```

##### Snowflake[¶](#snowflake)

```
CREATE FUNCTION addFourAndDivideAny (x VARIANT, y VARIANT)
RETURNS VARIANT
AS
$$
  ((x + 4) / y) :: VARIANT
$$;
```

## ARRAY<T>[¶](#array-t)

Translation specification for the ARRAY datatype from BigQuery to Snowflake

### Description[¶](#id1)

In BigQuery, an array is an ordered list of zero or more elements of non-array values. Elements in
an array must share the same type.
([Array Type. BigQuery](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#array_type))

### Sample Source Patterns[¶](#id2)

#### BigQuery[¶](#id3)

```
CREATE TABLE test.arrayTable
(
  col1 ARRAY<INT64>
);

CREATE TABLE test.anotherArrayTable
(
  col2 ARRAY<INT64>
);

INSERT INTO test.arrayTable VALUES ([4, 10, 55]);
INSERT INTO test.arrayTable VALUES ([6, 7, 33]);
INSERT INTO test.arrayTable VALUES ([50, 12, 22]);

INSERT INTO test.anotherArrayTable VALUES ([9, 11, 52]);
INSERT INTO test.anotherArrayTable VALUES ([3, 18, 11]);
INSERT INTO test.anotherArrayTable VALUES ([33, 27, 43]);
```

#### Snowflake[¶](#id4)

```
CREATE TABLE test.arrayTable
(
  col1 ARRAY DEFAULT []
);

CREATE TABLE test.anotherArrayTable
(
  col2 ARRAY DEFAULT []
);

INSERT INTO test.arrayTable SELECT [4, 10, 55];
INSERT INTO test.arrayTable SELECT [6, 7, 33];
INSERT INTO test.arrayTable SELECT [50, 12, 22];

INSERT INTO test.anotherArrayTable SELECT [9, 11, 52];
INSERT INTO test.anotherArrayTable SELECT [3, 18, 11];
INSERT INTO test.anotherArrayTable SELECT [33, 27, 43];
```

#### ARRAY access by index[¶](#array-access-by-index)

##### BigQuery[¶](#id5)

```
SELECT
col1[0] + 4 AS byIndex,
col1[OFFSET(0)] + 4 AS byOffset,
col1[ORDINAL(1)] + 4 AS byOrdinal
FROM test.arrayTable ORDER BY col1[0];
```

##### Snowflake[¶](#id6)

```
SELECT
--** SSC-FDM-BQ0001 - ACCESSING ARRAYS PRODUCES NULL INSTEAD OF AN ERROR FOR POSITIVE OUT OF BOUNDS INDEXES IN SNOWFLAKE **
col1[0] + 4 AS byIndex,
--** SSC-FDM-BQ0001 - ACCESSING ARRAYS PRODUCES NULL INSTEAD OF AN ERROR FOR POSITIVE OUT OF BOUNDS INDEXES IN SNOWFLAKE **
col1[0] + 4 AS byOffset,
--** SSC-FDM-BQ0001 - ACCESSING ARRAYS PRODUCES NULL INSTEAD OF AN ERROR FOR POSITIVE OUT OF BOUNDS INDEXES IN SNOWFLAKE **
col1[1 - 1] + 4 AS byOrdinal
FROM
test.arrayTable
ORDER BY
--** SSC-FDM-BQ0001 - ACCESSING ARRAYS PRODUCES NULL INSTEAD OF AN ERROR FOR POSITIVE OUT OF BOUNDS INDEXES IN SNOWFLAKE **
col1[0];
```

#### Safe ARRAY access by index[¶](#safe-array-access-by-index)

##### BigQuery[¶](#id7)

```
SELECT
col1[SAFE_OFFSET(0)] AS byOffsset,
col1[SAFE_OFFSET(-4)] AS byOffsetUnderflow,
col1[SAFE_OFFSET(500)] AS byOffsetOverflow,
col1[SAFE_ORDINAL(1)] AS byOrdinal,
col1[SAFE_ORDINAL(-4)] AS byOrdinalUnderflow,
col1[SAFE_ORDINAL(500)] AS byOrdinalOverflow
FROM test.arrayTable ORDER BY col1[0];
```

##### Snowflake[¶](#id8)

```
SELECT
PUBLIC.SAFE_OFFSET_UDF(col1, 0) AS byOffsset,
PUBLIC.SAFE_OFFSET_UDF(col1, -4) AS byOffsetUnderflow,
PUBLIC.SAFE_OFFSET_UDF(col1, 500) AS byOffsetOverflow,
PUBLIC.SAFE_OFFSET_UDF(col1, 1 - 1) AS byOrdinal,
PUBLIC.SAFE_OFFSET_UDF(col1, -4 - 1) AS byOrdinalUnderflow,
PUBLIC.SAFE_OFFSET_UDF(col1, 500 - 1) AS byOrdinalOverflow
FROM test.arrayTable ORDER BY
--** SSC-FDM-BQ0001 - ACCESSING ARRAYS PRODUCES NULL INSTEAD OF AN ERROR FOR POSITIVE OUT OF BOUNDS INDEXES IN SNOWFLAKE **
col1[0];
```

#### INSERT with ARRAY in the VALUES clause[¶](#insert-with-array-in-the-values-clause)

##### BigQuery[¶](#id9)

```
INSERT INTO test.arrayTable VALUES ([4, 10]);

INSERT INTO test.arrayTable (COL1)
VALUES ([1, 2, 3]), ([4, 5, 6]);

SELECT col1 FROM test.arrayTable ORDER BY col1[0], col1[1];
```

##### Snowflake[¶](#id10)

```
INSERT INTO test.arrayTable SELECT [4, 10];

INSERT INTO test.arrayTable (COL1)
SELECT [1, 2, 3]
UNION ALL
SELECT [4, 5, 6];

SELECT col1 FROM
  test.arrayTable
ORDER BY
  --** SSC-FDM-BQ0001 - ACCESSING ARRAYS PRODUCES NULL INSTEAD OF AN ERROR FOR POSITIVE OUT OF BOUNDS INDEXES IN SNOWFLAKE **
  col1[0],
  --** SSC-FDM-BQ0001 - ACCESSING ARRAYS PRODUCES NULL INSTEAD OF AN ERROR FOR POSITIVE OUT OF BOUNDS INDEXES IN SNOWFLAKE **
  col1[1];
```

#### MERGE statement[¶](#merge-statement)

##### BigQuery[¶](#id11)

```
MERGE INTO test.anotherArrayTable
USING test.arrayTable
ON col1[0] = col2[0]
WHEN MATCHED THEN UPDATE SET col2 = col1
WHEN NOT MATCHED THEN INSERT VALUES ([100, 100, 100]);

SELECT col2 FROM test.anotherArrayTable ORDER BY col2[0];
```

##### Snowflake[¶](#id12)

```
MERGE INTO test.anotherArrayTable
USING test.arrayTable
ON col1[0] = col2[0]
WHEN MATCHED THEN UPDATE SET col2 = col1
WHEN NOT MATCHED THEN INSERT VALUES ([100, 100, 100]) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'MergeStatement' NODE ***/!!!;

SELECT col2 FROM
  test.anotherArrayTable
ORDER BY
  --** SSC-FDM-BQ0001 - ACCESSING ARRAYS PRODUCES NULL INSTEAD OF AN ERROR FOR POSITIVE OUT OF BOUNDS INDEXES IN SNOWFLAKE **
  col2[0];
```

#### ARRAY DEFAULT column value insertion/update[¶](#array-default-column-value-insertion-update)

##### BigQuery[¶](#id13)

```
 INSERT INTO test.arrayTable VALUES (DEFAULT);

UPDATE test.arrayTable
SET col1 = DEFAULT
WHERE TRUE;

SELECT col1 FROM test.arrayTable;
```

##### Snowflake[¶](#id14)

```
 INSERT INTO test.arrayTable SELECT [];

UPDATE test.arrayTable
SET col1 = DEFAULT
WHERE TRUE;

SELECT col1 FROM test.arrayTable;
```

#### INSERT/UPDATE with NULL value[¶](#insert-update-with-null-value)

##### BigQuery[¶](#id15)

```
 INSERT INTO test.arrayTable
  SELECT
    numbers
  FROM
    (SELECT [6] AS numbers
    UNION ALL
    SELECT CAST(NULL AS ARRAY<INT64>));

UPDATE test.arrayTable
SET col1 = NULL
WHERE ARRAY_LENGTH(col1) > 1;

SELECT col1 FROM test.arrayTable ORDER BY ARRAY_LENGTH(col1);
```

##### Snowflake[¶](#id16)

```
INSERT INTO test.arrayTable
SELECT
  numbers
FROM
  (SELECT [6] AS numbers
  UNION ALL
  SELECT IFNULL(CAST(NULL AS ARRAY), []));

UPDATE test.arrayTable
SET col1 = IFNULL(NULL, [])
WHERE ARRAY_SIZE(col1) > 1;

SELECT col1 FROM test.arrayTable ORDER BY ARRAY_SIZE(col1);
```

#### ARRAY concatenation[¶](#array-concatenation)

##### BigQuery[¶](#id17)

```
SELECT [50, 30, 12] || [22, 33, 44] AS result;
```

##### Snowflake[¶](#id18)

```
SELECT ARRAY_CAT([50, 30, 12], [22, 33, 44]) AS result;
```

#### ARRAY used as parameter/return type[¶](#array-used-as-parameter-return-type)

##### BigQuery[¶](#id19)

```
CREATE FUNCTION test.myArrayFunction (valuesArray ARRAY<INT64>, otherValue INTEGER)
RETURNS ARRAY<INT64>
AS
(
  valuesArray || [otherValue]
);

SELECT test.myArrayFunction([5, 20, 10], 55) AS result;
```

##### Snowflake[¶](#id20)

```
CREATE FUNCTION test.myArrayFunction (valuesArray ARRAY, otherValue INTEGER)
RETURNS ARRAY
AS
$$
  ARRAY_CAT(valuesArray, [otherValue])
$$;

SELECT test.myArrayFunction([5, 20, 10], 55) AS result;
```

### Known Issues[¶](#known-issues)

**1. Non-safe ARRAY access will not fail for positive out of bounds indexes**

In BigQuery, accessing an array element by index will fail for any index value that is too low
(underflow) or too high (overflow) when not using SAFE_OFFSET or SAFE_ORDINAL. However, in Snowflake
errors are thrown only for underflow cases, any index that would case an overflow error will
generate a NULL value instead.

When non-safe access to elements in an array is detected SnowConvert AI will generate
[SSC-FDM-BQ0001](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/bigqueryFDM#ssc-fdm-bq0001)
to warn the user about this.

### Related EWIs[¶](#related-ewis)

1. [SSC-FDM-BQ0001](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/bigqueryFDM#ssc-fdm-bq0001):
   Accessing arrays produces NULL instead of an error for positive out of bounds indexes in
   Snowflake.

## BYTES[¶](#bytes)

Bytes data type and usages

### Description[¶](#id21)

> Sequence of bytes with a maximum of L bytes allowed in the binary string. The maximum length is 8
> MB (8,388,608 bytes). For more information please refer to
> [BigQuery BYTES data type](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#bytes_type).

**Note:**

BYTES data type is not supported in Snowflake, currently transformed to
[BINARY](https://docs.snowflake.com/en/sql-reference/data-types-text#binary).

### Sample Source Patterns[¶](#id22)

#### BYTES output format[¶](#bytes-output-format)

The default output format for binary data types in BigQuery is ‘BASE64’ and in Snowflake ‘HEX’. For
this reason, when a binary column is selected, the
[BASE64_ENCODE](https://docs.snowflake.com/en/sql-reference/functions/base64_encode) function is
automatically added. In order to maintain the default formatting of BigQuery.

##### BigQuery[¶](#id23)

```
 CREATE OR REPLACE TABLE bytesTable
(
  COL1 BYTES,
  COL2 BYTES(20)
);

INSERT INTO bytesTable VALUES (B"01020304", B"""AABBCCDD""");
INSERT INTO bytesTable VALUES (B'''\x01\x02\x03''', B"/+A=");

SELECT COL1 FROM bytesTable;
```

##### Snowflake:[¶](#id24)

```
CREATE OR REPLACE TABLE bytesTable
(
  COL1 BINARY,
  COL2 BINARY(20)
);

INSERT INTO bytesTable
SELECT
  TRY_TO_BINARY('01020304', 'utf-8'),
  TRY_TO_BINARY('AABBCCDD', 'utf-8');

INSERT INTO bytesTable
SELECT
  TRY_TO_BINARY('\x01\x02\x03', 'utf-8'),
  TRY_TO_BINARY('/+A=', 'utf-8');

SELECT BASE64_ENCODE( COL1) FROM bytesTable;
```

In case it is not added automatically and you want to see the data in BASE64 format, you can use the
[BASE64_ENCODE](https://docs.snowflake.com/en/sql-reference/functions/base64_encode) function or set
the
[BINARY_OUTPUT_FORMAT](https://docs.snowflake.com/en/sql-reference/parameters#binary-output-format)
format.

#### BYTES Literal[¶](#bytes-literal)

The following cases represent the forms that can be used to format byte literals in BigQuery.

```
 B"abc"
B'''abc'''
b"""abc"""
```

These literals are not supported in Snowflake, but instead the
[TRY_TO_BINARY](https://docs.snowflake.com/en/sql-reference/functions/try_to_binary) function can be
used to convert the input expression to a binary value. This function is a special version of
[TO_BINARY](https://docs.snowflake.com/en/sql-reference/functions/to_binary) that performs the same
operation, but with error handling support.

It is important to take into consideration that the binary format for the conversion can be: HEX,
BASE64, or UTF-8. The default is the value of the
[BINARY_INPUT_FORMAT](https://docs.snowflake.com/en/sql-reference/parameters#binary-input-format)
session parameter. If this parameter is not set, the default value is HEX.

#### Observations[¶](#observations)

- Please keep in mind that the default output format for binary data types in BigQuery is ‘BASE64’
  and in Snowflake ‘HEX’. You can use the
  [BASE64_ENCODE](https://docs.snowflake.com/en/sql-reference/functions/base64_encode) function or
  set the
  [BINARY_OUTPUT_FORMAT](https://docs.snowflake.com/en/sql-reference/parameters#binary-output-format)
  format if you want to view the data in BASE64 format.
- The only formats supported by Snowflake are: HEX, BASE64, or UTF-8. For more information, please
  refer to[Binary Input and Output](https://docs.snowflake.com/en/user-guide/binary-input-output) in
  Snowflake.
- Binary functions used to insert data into a values clause are not supported in Snowflake.

## GEOGRAPHY[¶](#geography)

GEOGRAPHY data type and usages

### Description[¶](#id25)

A collection of points, linestrings, and polygons, which is represented as a point set, or a subset
of the surface of the Earth. For more information please refer to
[BigQuery GEOGRAPHY data type](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#geography_type).

Success

Supported data type in Snowflake.

### Sample Source Patterns[¶](#id26)

#### GEOGRAPHY output format[¶](#geography-output-format)

The default output format for geography data types in BigQuery is **WKT** **(Well-Known Text)** and
in Snowflake **WKB (Well-Known Binary)**. For this reason, when geography columns are selected, the
[ST_ASWKT](https://docs.snowflake.com/en/sql-reference/functions/st_aswkt) function is automatically
added. In addition, when all the columns of a table are selected and it contains a Geography column,
the
[GEOGRAPHY_OUTPUT_FORMAT](https://docs.snowflake.com/en/sql-reference/parameters#geography-output-format)
is set to WKT. This is in order to keep the default BigQuery format.

##### BigQuery[¶](#id27)

```
CREATE OR REPLACE TABLE test.geographyType
(
  COL1 GEOGRAPHY
);

INSERT INTO test.geographyType VALUES
    (ST_GEOGFROMTEXT('POINT(-122.35 37.55)')), (ST_GEOGFROMTEXT('LINESTRING(-124.20 42.00, -120.01 41.99)'));

SELECT COL1 FROM test.geographyType;
SELECT * FROM test.geographyType;
```

##### Snowflake[¶](#id28)

```
CREATE OR REPLACE TABLE test.geographyType
(
  COL1 GEOGRAPHY
);

INSERT INTO test.geographyType
VALUES
    (
     --** SSC-FDM-BQ0010 - THE FUNCTION 'ST_GEOGFROMTEXT' IS NOT REQUIRED IN SNOWFLAKE. **
     'POINT(-122.35 37.55)'), (
     --** SSC-FDM-BQ0010 - THE FUNCTION 'ST_GEOGFROMTEXT' IS NOT REQUIRED IN SNOWFLAKE. **
     'LINESTRING(-124.20 42.00, -120.01 41.99)');

SELECT ST_ASWKT( COL1) FROM test.geographyType;

ALTER SESSION SET GEOGRAPHY_OUTPUT_FORMAT = 'WKT';
SELECT * FROM test.geographyType;
```

In case it is not added automatically and you want to see the data in WKT format, you can use the
[ST_ASWKT](https://docs.snowflake.com/en/sql-reference/functions/st_aswkt) function or set the
[GEOGRAPHY_OUTPUT_FORMAT](https://docs.snowflake.com/en/sql-reference/parameters#geography-output-format)
format.

#### Insert GEOGRAPHY data[¶](#insert-geography-data)

To insert data in geography type columns, no function is needed, because Snowflake automatically
detects that the data follows the [WGS 84 standard](https://spatialreference.org/ref/epsg/wgs-84/).

#### Observations[¶](#id29)

- Please keep in mind that the default output format for geography data types is **WKT**
  **(Well-Known Text)** and in Snowflake **WKB (Well-Known Binary)**. You can use the
  [ST_ASWKT](https://docs.snowflake.com/en/sql-reference/functions/st_aswkt) function or set the
  [GEOGRAPHY_OUTPUT_FORMAT](https://docs.snowflake.com/en/sql-reference/parameters#geography-output-format)
  format if you want to view the data in **WKT** format.
- Geography functions used to insert data into a values clause are not needed in Snowflake.

### Related EWI’s[¶](#related-ewi-s)

1. [SSC-FDM-BQ0010](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/bigqueryFDM#ssc-fdm-bq0010):
   Geography function is not required in Snowflake.

## INTERVAL[¶](#interval)

Interval data type and usages

### Description[¶](#id30)

An `INTERVAL` object represents duration or amount of time, without referring to any specific point
in time. There is no equivalent in Snowflake so it is transformed to Varchar
([BigQuery Language Reference INTERVAL Data Type](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#interval_type))

**Syntax**

```
INTERVAL int64_expression datetime_part

INTERVAL datetime_parts_string starting_datetime_part TO ending_datetime_part
```

### Sample Source Patterns[¶](#id31)

#### Interval with a single DateTime part[¶](#interval-with-a-single-datetime-part)

##### BigQuery[¶](#id32)

```
SELECT INTERVAL 1 YEAR;

SELECT CURRENT_DATE + INTERVAL 1 YEAR,
  CURRENT_DATE + INTERVAL 1 QUARTER,
  CURRENT_DATE + INTERVAL 1 MONTH,
  CURRENT_DATE + INTERVAL 1 WEEK,
  CURRENT_DATE + INTERVAL 1 DAY,
  CURRENT_DATE + INTERVAL 1 HOUR,
  CURRENT_DATE + INTERVAL 1 MINUTE,
  CURRENT_DATE + INTERVAL 1 SECOND;
```

##### Result[¶](#result)

```
1-0 0 0:0:0
```

```
2024-10-13T00:00:00
2024-01-13T00:00:00
2023-11-13T00:00:00
2023-10-20T00:00:00
2023-10-14T00:00:00
2023-10-13T01:00:00
2023-10-13T00:01:00
2023-10-13T00:00:01
```

##### Snowflake[¶](#id33)

```
SELECT
!!!RESOLVE EWI!!! /*** SSC-EWI-0107 - INTERVAL LITERAL IS NOT SUPPORTED BY SNOWFLAKE IN THIS SCENARIO  ***/!!! INTERVAL 1 YEAR;

SELECT
CURRENT_DATE() + INTERVAL '1 year',
CURRENT_DATE() + INTERVAL '1 quarter',
CURRENT_DATE() + INTERVAL '1 month',
CURRENT_DATE() + INTERVAL '1 week',
CURRENT_DATE() + INTERVAL '1 day',
CURRENT_DATE() + INTERVAL '1 hour',
CURRENT_DATE() + INTERVAL '1 minute',
CURRENT_DATE() + INTERVAL '1 second';
```

##### Result[¶](#id34)

```
2024-10-13
2024-01-13
2023-11-13
2023-10-20
2023-10-14
2023-10-13 01:00:00.000
2023-10-13 00:01:00.000
2023-10-13 00:00:01.000
```

Snowflake does not support the scenario where the **Interval** data type is queried directly, on the
contrary when it is used as an operator for a given date its translation is done using an
[Interval constant](https://docs.snowflake.com/en/sql-reference/data-types-datetime.html#interval-constants)
(if possible).

#### Interval with a DateTime part range[¶](#interval-with-a-datetime-part-range)

##### BigQuery[¶](#id35)

```
 SELECT INTERVAL '2-1 10' YEAR TO DAY;

SELECT CURRENT_DATE + INTERVAL '2-11' YEAR TO MONTH,
  CURRENT_DATE + INTERVAL '2-11 28' YEAR TO DAY,
  CURRENT_DATE + INTERVAL '2-11 28 16' YEAR TO HOUR,
  CURRENT_DATE + INTERVAL '2-11 28 16:15' YEAR TO MINUTE,
  CURRENT_DATE + INTERVAL '2-11 28 16:15:14' YEAR TO SECOND,
  CURRENT_DATE + INTERVAL '11 28' MONTH TO DAY,
  CURRENT_DATE + INTERVAL '11 28 16' MONTH TO HOUR,
  CURRENT_DATE + INTERVAL '11 28 16:15' MONTH TO MINUTE,
  CURRENT_DATE + INTERVAL '11 28 16:15:14' MONTH TO SECOND,
  CURRENT_DATE + INTERVAL '28 16' DAY TO HOUR,
  CURRENT_DATE + INTERVAL '28 16:15' DAY TO MINUTE,
  CURRENT_DATE + INTERVAL '28 16:15:14' DAY TO SECOND,
  CURRENT_DATE + INTERVAL '16:15' HOUR TO MINUTE,
  CURRENT_DATE + INTERVAL '16:15:14' HOUR TO SECOND,
  CURRENT_DATE + INTERVAL '15:14' MINUTE TO SECOND;
```

##### Result[¶](#id36)

```
2-1 10 0:0:0
```

```
2026-09-13T00:00:00
2026-10-11T00:00:00
2026-10-11T16:00:00
2026-10-11T16:15:00
2026-10-11T16:15:14
2024-10-11T00:00:00
2024-10-11T16:00:00
2024-10-11T16:15:00
2024-10-11T16:15:14
2023-11-10T16:00:00
2023-11-10T16:15:00
2023-11-10T16:15:14
2023-10-13T16:15:00
2023-10-13T16:15:14
2023-10-13T00:15:14
```

##### Snowflake[¶](#id37)

```
 SELECT
!!!RESOLVE EWI!!! /*** SSC-EWI-0107 - INTERVAL LITERAL IS NOT SUPPORTED BY SNOWFLAKE IN THIS SCENARIO  ***/!!! INTERVAL '2-1 10' YEAR TO DAY;

SELECT
CURRENT_DATE() + INTERVAL '2y, 11mm',
CURRENT_DATE() + INTERVAL '2y, 11mm, 28d',
CURRENT_DATE() + INTERVAL '2y, 11mm, 28d, 16h',
CURRENT_DATE() + INTERVAL '2y, 11mm, 28d, 16h, 15m',
CURRENT_DATE() + INTERVAL '2y, 11mm, 28d, 16h, 15m, 14s',
CURRENT_DATE() + INTERVAL '11mm, 28d',
CURRENT_DATE() + INTERVAL '11mm, 28d, 16h',
CURRENT_DATE() + INTERVAL '11mm, 28d, 16h, 15m',
CURRENT_DATE() + INTERVAL '11mm, 28d, 16h, 15m, 14s',
CURRENT_DATE() + INTERVAL '28d, 16h',
CURRENT_DATE() + INTERVAL '28d, 16h, 15m',
CURRENT_DATE() + INTERVAL '28d, 16h, 15m, 14s',
CURRENT_DATE() + INTERVAL '16h, 15m',
CURRENT_DATE() + INTERVAL '16h, 15m, 14s',
CURRENT_DATE() + INTERVAL '15m, 14s';
```

##### Result[¶](#id38)

```
2026-09-13
2026-10-11
2026-10-11 16:00:00.000
2026-10-11 16:15:00.000
2026-10-11 16:15:14.000
2024-10-11
2024-10-11 16:00:00.000
2024-10-11 16:15:00.000
2024-10-11 16:15:14.000
2023-11-10 16:00:00.000
2023-11-10 16:15:00.000
2023-11-10 16:15:14.000
2023-10-13 16:15:00.000
2023-10-13 16:15:14.000
2023-10-13 00:15:14.000
```

The Interval value is transformed to a supported Snowflake format and then inserted as text inside
the column. Since Snowflake does not support **Interval** as a data type, it is only supported in
arithmetic operations. In order to use the value, it needs to be extracted and used as an
[Interval constant](https://docs.snowflake.com/en/sql-reference/data-types-datetime.html#interval-constants)
(if possible).

#### Interval as a Column data type[¶](#interval-as-a-column-data-type)

##### BigQuery[¶](#id39)

```
 CREATE OR REPLACE TABLE test.my_table (
  id INT NOT NULL,
  interval_column INTERVAL
);

INSERT INTO test.my_table
VALUES (1, INTERVAL '2-11 28' YEAR TO DAY);

INSERT INTO test.my_table
VALUES (2, INTERVAL '2-11 28 16:15:14' YEAR TO SECOND);

INSERT INTO test.my_table
VALUES (3, INTERVAL '11 28 16:15:14' MONTH TO SECOND);

INSERT INTO test.my_table
VALUES (4, INTERVAL '15:14' MINUTE TO SECOND);

SELECT * FROM test.my_table;
```

##### Result[¶](#id40)

<!-- prettier-ignore -->
|ID|interval_column|
|---|---|
|1|2-11 28 0:0:0|
|2|2-11 28 16:15:14|
|3|0-11 28 16:15:14|
|4|0-0 0 0:15:14|

##### Snowflake[¶](#id41)

```
 CREATE OR REPLACE TABLE test.my_table (
  id INT NOT NULL,
interval_column VARCHAR(30) !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - INTERVAL DATA TYPE CONVERTED TO VARCHAR ***/!!!
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "bigquery",  "convertedOn": "04/01/2025",  "domain": "test" }}';

INSERT INTO test.my_table
VALUES (1, '2y, 11mm, 28d');

INSERT INTO test.my_table
VALUES (2, '2y, 11mm, 28d, 16h, 15m, 14s');

INSERT INTO test.my_table
VALUES (3, '11mm, 28d, 16h, 15m, 14s');

INSERT INTO test.my_table
VALUES (4, '15m, 14s');

SELECT * FROM
test.my_table;
```

##### Result[¶](#id42)

<!-- prettier-ignore -->
|ID|interval_column|
|---|---|
|1|2y, 11mm, 28d|
|2|2y, 11mm, 28d, 16h, 15m, 14s|
|3|11mm, 28d, 16h, 15m, 14s|
|4|15m, 14s|

In BigQuery the datetime_part follows the next canonical format:

```
[sign]Y-M [sign]D [sign]H:M:S[.F]
```

#### Interval comparison[¶](#interval-comparison)

##### BigQuery[¶](#id43)

```
SELECT INTERVAL 1 YEAR = INTERVAL 1 YEAR;

SELECT CURRENT_DATE + INTERVAL '-2 -16' DAY TO HOUR =  CURRENT_DATE + INTERVAL '-2 -16' DAY TO HOUR;

SELECT INTERVAL '-2 -16' DAY TO HOUR != INTERVAL '-2 16' DAY TO HOUR,
  INTERVAL '-2 -16' DAY TO HOUR <> INTERVAL '-2 16' DAY TO HOUR,
  INTERVAL '2 16:15' DAY TO MINUTE = INTERVAL '2 -16:15' DAY TO MINUTE,
  INTERVAL '2 16:15' DAY TO MINUTE > INTERVAL '2 -16:15' DAY TO MINUTE,
  INTERVAL '2 16:15' DAY TO MINUTE >= INTERVAL '2 -16:15' DAY TO MINUTE,
  INTERVAL '2 16:15' DAY TO MINUTE < INTERVAL '2 -16:15' DAY TO MINUTE,
  INTERVAL '2 16:15' DAY TO MINUTE <= INTERVAL '2 -16:15' DAY TO MINUTE,
  INTERVAL '1-5' YEAR TO MONTH = INTERVAL '1-5' YEAR TO MONTH,
  INTERVAL '1-5' YEAR TO MONTH > INTERVAL '2 16' DAY TO HOUR,
  INTERVAL '2-11 28 16:15:14.222' YEAR TO SECOND = INTERVAL '2-11 28 16:15:14.222' YEAR TO SECOND,
  INTERVAL '1-1 3' YEAR TO DAY = INTERVAL '13 3' MONTH TO DAY,
  INTERVAL '1-5' YEAR TO MONTH > INTERVAL '2 16' DAY TO HOUR;
```

##### Snowflake[¶](#id44)

```
SELECT
'1 year' = '1 year';

SELECT
CURRENT_DATE() + INTERVAL '-2d, -16h' = CURRENT_DATE() + INTERVAL '-2d, -16h';

SELECT
CURRENT_TIMESTAMP + INTERVAL '-2d, -16h' != CURRENT_TIMESTAMP + INTERVAL '-2d, 16h',
CURRENT_TIMESTAMP + INTERVAL '-2d, -16h' <> CURRENT_TIMESTAMP + INTERVAL '-2d, 16h',
CURRENT_TIMESTAMP + INTERVAL '2d, 16h, 15m' = CURRENT_TIMESTAMP + INTERVAL '2d, -16h, -15m',
CURRENT_TIMESTAMP + INTERVAL '2d, 16h, 15m' > CURRENT_TIMESTAMP + INTERVAL '2d, -16h, -15m',
CURRENT_TIMESTAMP + INTERVAL '2d, 16h, 15m' >= CURRENT_TIMESTAMP + INTERVAL '2d, -16h, -15m',
CURRENT_TIMESTAMP + INTERVAL '2d, 16h, 15m' < CURRENT_TIMESTAMP + INTERVAL '2d, -16h, -15m',
CURRENT_TIMESTAMP + INTERVAL '2d, 16h, 15m' <= CURRENT_TIMESTAMP + INTERVAL '2d, -16h, -15m',
CURRENT_TIMESTAMP + INTERVAL '1y, 5mm' = CURRENT_TIMESTAMP + INTERVAL '1y, 5mm',
CURRENT_TIMESTAMP + INTERVAL '1y, 5mm' > CURRENT_TIMESTAMP + INTERVAL '2d, 16h',
CURRENT_TIMESTAMP + INTERVAL '2y, 11mm, 28d, 16h, 15m, 14s, 222ms' = CURRENT_TIMESTAMP + INTERVAL '2y, 11mm, 28d, 16h, 15m, 14s, 222ms',
CURRENT_TIMESTAMP + INTERVAL '1y, 1mm, 3d' = CURRENT_TIMESTAMP + INTERVAL '13mm, 3d',
CURRENT_TIMESTAMP + INTERVAL '1y, 5mm' > CURRENT_TIMESTAMP + INTERVAL '2d, 16h';
```

As is known, Snowflake only supports Interval as a data type in arithmetic operations, which is why
the `CURRENT_TIMESTAMP` function is added to each operand to correctly support the comparison.

### Known Issues[¶](#id45)

#### 1. Only arithmetic operations are supported[¶](#only-arithmetic-operations-are-supported)

Snowflake Intervals have several limitations. Only arithmetic operations between `DATE` or
`TIMESTAMP` and
[Interval Constants](https://docs.snowflake.com/en/sql-reference/data-types-datetime.html#interval-constants)
are supported, every other scenario is not supported.

##### 2. Working with signs in the Interval data type[¶](#working-with-signs-in-the-interval-data-type)

In BigQuery, when the substring corresponding to the year-month is preceded by a sign (+ -), it
affects both the year and the month. In a similar way, it works for the substring corresponding to
the time, in this case, the following affects the hour, minute, and second. An example of this is
shown below.

##### BigQuery[¶](#id46)

```
SELECT CURRENT_DATE + INTERVAL '-2-11 -28 -16:15:14.222' YEAR TO SECOND;
```

##### Snowflake[¶](#id47)

```
 SELECT CURRENT_DATE + INTERVAL '-2y, -11mm, -28d, -16h, -15m, -14s, -222ms';
```

### Related EWIs[¶](#id48)

1. [SSC-EWI-0036](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0036):
   Data type converted to another data type.
2. [SSC-EWI-0107](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0107):
   Interval Literal Not Supported In Current Scenario.

## JSON[¶](#json)

Json data type and usages

### Description[¶](#id49)

Represents JSON, a lightweight data-interchange format. For more information please refer to
[BigQuery JSON data type](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#json_type).

Danger

JSON data type is not supported in Snowflake, currently transformed to
[VARIANT](https://docs.snowflake.com/en/sql-reference/data-types-semistructured#variant).

#### JSON Literals[¶](#json-literals)

```
 JSON 'json_formatted_data'
```

For more information please refer to
[JSON Literals in BigQuery](https://cloud.google.com/bigquery/docs/reference/standard-sql/lexical#json_literals).

These literals are not supported in Snowflake, but instead the
[PARSE_JSON](https://docs.snowflake.com/en/sql-reference/functions/parse_json) function can be used
to convert the input expression to a json type. The only point to take into consideration is that
this function cannot be used in the values clause in Snowflake, for this reason it is transformed to
a subquery.

### Sample Source Patterns[¶](#id50)

#### BigQuery[¶](#id51)

```
CREATE OR REPLACE TABLE test.jsonType
(
  COL1 JSON
);

INSERT INTO test.jsonType
VALUES
  (JSON'{"name": "John", "age": 30, "city": "New York"}'),
  (JSON'{"name": "Alice", "age": 28, "city": "San Francisco"}');

SELECT * FROM test.jsonType;

SELECT JSON'{"name": "John", "age": 30, "city": "New York"}';
```

#### Snowflake[¶](#id52)

```
CREATE OR REPLACE TABLE test.jsonType
(
  COL1 VARIANT
);

INSERT INTO test.jsonType
SELECT
  PARSE_JSON('{"name": "John", "age": 30, "city": "New York"}')
UNION ALL
SELECT
  PARSE_JSON('{"name": "Alice", "age": 28, "city": "San Francisco"}');

SELECT * FROM test.jsonType;

SELECT
  PARSE_JSON('{"name": "John", "age": 30, "city": "New York"}');
```

## STRUCT[¶](#struct)

Translation specification for the STRUCT datatype from BigQuery to Snowflake.

### Description[¶](#id53)

In BigQuery, a container of ordered fields each with a type (required) and field name (optional).
See
[Struct Type](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#struct_type).

In Snowflake,
[`OBJECT_CONSTRUCT`](https://docs.snowflake.com/en/sql-reference/functions/object_construct) can be
used to emulate the `STRUCT` behavior, and SnowConvert AI handles most implementation differences.

**Note:**

Arguments that represent keys within the OBJECT_CONSTRUCT must be the original names of the target
STRUCT. Any name specified within a STRUCT expression body will be replaced with the name found in
the target STRUCT. Most of the data pattern examples below contain an example of a name that is
replaced by the target name.

### Sample Source Patterns[¶](#id54)

#### BigQuery[¶](#id55)

```
CREATE OR REPLACE TABLE test.structTypes
(
    COL1 STRUCT<sc1 INT64>,
    COL2 STRUCT<sc2 STRING(10)>,
    COL3 STRUCT<sc3 STRUCT<sc31 INT64, sc32 INT64>>,
    COL4 STRUCT<sc4 ARRAY<INT64>>,
    COL5 STRUCT<sc5 INT64, sc51 INT64>,
    COL7 STRUCT<sc7 INT64 OPTIONS(description = "A repeated STRING field"), sc71 BOOL>,
    COL8 STRUCT<sc8 INT64 NOT NULL, sc81 BOOL NOT NULL OPTIONS(description = "A repeated STRING field")>
);

CREATE OR REPLACE TABLE test.tuple_sample (
  COL1 STRUCT<Key1 INT64, Key2 INT64>
);
```

#### Snowflake[¶](#id56)

```
CREATE OR REPLACE TABLE test.structTypes
(
    COL1 VARIANT /*** SSC-FDM-BQ0009 - STRUCT<INT> CONVERTED TO VARIANT. SOME OF ITS USAGES MIGHT HAVE FUNCTIONAL DIFFERENCES. ***/,
    COL2 VARIANT /*** SSC-FDM-BQ0009 - STRUCT<STRING(10)> CONVERTED TO VARIANT. SOME OF ITS USAGES MIGHT HAVE FUNCTIONAL DIFFERENCES. ***/,
    COL3 VARIANT /*** SSC-FDM-BQ0009 - STRUCT<STRUCT<INT64, INT64>> CONVERTED TO VARIANT. SOME OF ITS USAGES MIGHT HAVE FUNCTIONAL DIFFERENCES. ***/,
    COL4 VARIANT /*** SSC-FDM-BQ0009 - STRUCT<> CONVERTED TO VARIANT. SOME OF ITS USAGES MIGHT HAVE FUNCTIONAL DIFFERENCES. ***/,
    COL5 VARIANT /*** SSC-FDM-BQ0009 - STRUCT<INT, INT> CONVERTED TO VARIANT. SOME OF ITS USAGES MIGHT HAVE FUNCTIONAL DIFFERENCES. ***/,
    COL7 VARIANT /*** SSC-FDM-BQ0009 - STRUCT<INT, BOOLEAN> CONVERTED TO VARIANT. SOME OF ITS USAGES MIGHT HAVE FUNCTIONAL DIFFERENCES. ***/,
    COL8 VARIANT /*** SSC-FDM-BQ0009 - STRUCT<INT, BOOLEAN> CONVERTED TO VARIANT. SOME OF ITS USAGES MIGHT HAVE FUNCTIONAL DIFFERENCES. ***/
);

CREATE OR REPLACE TABLE test.tuple_sample (
  COL1 VARIANT /*** SSC-FDM-BQ0009 - STRUCT<INT, INT> CONVERTED TO VARIANT. SOME OF ITS USAGES MIGHT HAVE FUNCTIONAL DIFFERENCES. ***/
);
```

#### Insert INT Data Type to STRUCT column[¶](#insert-int-data-type-to-struct-column)

##### BigQuery[¶](#id57)

```
INSERT INTO test.structTypes (COL1) VALUES
(STRUCT(1)),
(STRUCT<INT64>(2)),
(STRUCT<a INT64>(3)),
(STRUCT<sc1 INT64>(4)),
(STRUCT<sc1 INT64>(5));
```

##### Snowflake[¶](#id58)

```
INSERT INTO test.structTypes (COL1)
SELECT
    OBJECT_CONSTRUCT('sc1', 1 :: INT)
UNION ALL
SELECT
    OBJECT_CONSTRUCT('sc1', 2 :: INT)
UNION ALL
SELECT
    OBJECT_CONSTRUCT('sc1', 3 :: INT)
UNION ALL
SELECT
    OBJECT_CONSTRUCT('sc1', 4 :: INT)
UNION ALL
SELECT
    OBJECT_CONSTRUCT('sc1', 5 :: INT);
```

#### Insert STRING Data Type to STRUCT column[¶](#insert-string-data-type-to-struct-column)

##### BigQuery[¶](#id59)

```
INSERT INTO test.structTypes (COL2) VALUES
(STRUCT('t1')),
(STRUCT<STRING>('t2')),
(STRUCT<sc2 STRING>('t3'));
```

##### Snowflake[¶](#id60)

```
INSERT INTO test.structTypes (COL2)
SELECT
    OBJECT_CONSTRUCT('sc2', 't1' :: STRING)
UNION ALL
SELECT
    OBJECT_CONSTRUCT('sc2', 't2' :: STRING)
UNION ALL
SELECT
    OBJECT_CONSTRUCT('sc2', 't3' :: STRING);
```

#### Insert STRUCT Data Type to STRUCT column[¶](#insert-struct-data-type-to-struct-column)

##### BigQuery[¶](#id61)

```
INSERT INTO test.structTypes (COL3) VALUES
(STRUCT(STRUCT(1,2))),
(STRUCT<sc3 STRUCT<sc31 INT64, sc32 INT64>>(STRUCT<INT64, INT64>(3, 4))),
(STRUCT<sc3 STRUCT<sc31 INT64, sc32 INT64>>(STRUCT<sc31 INT64, sc32 INT64>(5, 6))),
(STRUCT<STRUCT<INT64,INT64>>(STRUCT<INT64, INT64>(7, 8))),
(STRUCT<STRUCT<INT64,INT64>>(STRUCT(9, 10)));
```

##### Snowflake[¶](#id62)

```
INSERT INTO test.structTypes (COL3)
SELECT
  OBJECT_CONSTRUCT('sc3', OBJECT_CONSTRUCT('sc31', 1 :: INT, 'sc32', 2 :: INT))
UNION ALL
SELECT
  OBJECT_CONSTRUCT('sc3', OBJECT_CONSTRUCT('sc31', 3 :: INT, 'sc32', 4 :: INT))
UNION ALL
SELECT
  OBJECT_CONSTRUCT('sc3', OBJECT_CONSTRUCT('sc31', 5 :: INT, 'sc32', 6 :: INT))
UNION ALL
SELECT
  OBJECT_CONSTRUCT('sc3', OBJECT_CONSTRUCT('sc31', 7 :: INT, 'sc32', 8 :: INT))
UNION ALL
SELECT
  OBJECT_CONSTRUCT('sc3', OBJECT_CONSTRUCT('sc31', 9 :: INT, 'sc32', 10 :: INT));
```

#### Insert ARRAY Data Type to STRUCT column[¶](#insert-array-data-type-to-struct-column)

##### BigQuery[¶](#id63)

```
INSERT INTO test.structTypes (COL4) VALUES
(STRUCT([1,2,3,4])),
(STRUCT<sc4 ARRAY<INT64>>(ARRAY[5,6,7])),
(STRUCT<ARRAY<INT64>>([8,9,10,11]));
```

##### Snowflake[¶](#id64)

```
INSERT INTO test.structTypes (COL4)
SELECT
  OBJECT_CONSTRUCT('sc4', [1,2,3,4] :: ARRAY)
UNION ALL
SELECT
  OBJECT_CONSTRUCT('sc4', [5,6,7] :: ARRAY)
UNION ALL
SELECT
  OBJECT_CONSTRUCT('sc4', [8,9,10,11] :: ARRAY);
```

#### Insert to selected STRUCT columns[¶](#insert-to-selected-struct-columns)

##### BigQuery[¶](#id65)

```
INSERT INTO test.structTypes (COL7, COL8) VALUES
(STRUCT(1,true), STRUCT(2,false)),
(STRUCT<INT64, BOOL>(3, false), STRUCT<INT64, BOOL>(4, false)),
(STRUCT<a INT64, b BOOL>(5, true), STRUCT<a INT64, b BOOL>(6, true));
```

##### Snowflake[¶](#id66)

```
INSERT INTO test.structTypes (COL7, COL8)
SELECT
  OBJECT_CONSTRUCT('sc7', 1 :: INT, 'sc71', true),
  OBJECT_CONSTRUCT('sc8', 2 :: INT, 'sc81', false)
UNION ALL
SELECT
  OBJECT_CONSTRUCT('sc7', 3 :: INT, 'sc71', false),
  OBJECT_CONSTRUCT('sc8', 4 :: INT, 'sc81', false)
UNION ALL
SELECT
  OBJECT_CONSTRUCT('sc7', 5 :: INT, 'sc71', true),
  OBJECT_CONSTRUCT('sc8', 6 :: INT, 'sc81', true);
```

#### Insert to STRUCT column tuple syntax[¶](#insert-to-struct-column-tuple-syntax)

Warning

Translation of tuple syntax values is currently not supported.

##### BigQuery[¶](#id67)

```
INSERT INTO test.tuple_sample
VALUES
  ((12, 34)),
  ((56, 78)),
  ((9, 99)),
  ((12, 35));
```

##### Snowflake[¶](#id68)

```
INSERT INTO test.tuple_sample
!!!RESOLVE EWI!!! /*** SSC-EWI-BQ0012 - UNABLE TO GENERATE CORRECT OBJECT_CONSTRUCT PARAMETER. SYMBOL INFORMATION COULD NOT BE COLLECTED. ***/!!!
VALUES
  ((12, 34)),
  ((56, 78)),
  ((9, 99)),
  ((12, 35));
```

#### Update STRUCT column[¶](#update-struct-column)

##### BigQuery[¶](#id69)

```
UPDATE test.structTypes
SET col1 = STRUCT(100 AS number)
WHERE col1.sc1 = 4;
```

##### Snowflake[¶](#id70)

```
UPDATE test.structTypes
    SET col1 = OBJECT_CONSTRUCT('sc1', 100 :: INT)
WHERE col1:sc1 = 4;
```

#### Update STRUCT column field[¶](#update-struct-column-field)

##### BigQuery[¶](#id71)

```
UPDATE test.structTypes
SET col3 = STRUCT(STRUCT(80,90))
WHERE col3.sc3.sc31 = 20;
```

##### Snowflake[¶](#id72)

```
UPDATE test.structTypes
SET col3 = OBJECT_CONSTRUCT('sc3', OBJECT_CONSTRUCT('sc31', 80 :: INT, 'sc32', 90 :: INT))
WHERE col3:sc3:sc31 = 20;
```

#### Select from STRUCT column[¶](#select-from-struct-column)

##### BigQuery[¶](#id73)

```
SELECT COL3.sc3 FROM test.structTypes;
SELECT COL3.sc3.sc32 FROM test.structTypes;
SELECT COL4.sc4 FROM test.structTypes WHERE COL4.sc4 IS NOT NULL;
```

##### Snowflake[¶](#id74)

```
SELECT COL3:sc3
FROM
test.structTypes;
SELECT COL3:sc3:sc32
FROM
test.structTypes;
SELECT COL4:sc4
FROM
test.structTypes
WHERE COL4:sc4 IS NOT NULL;
```

#### Select from STRUCT column tuple syntax[¶](#select-from-struct-column-tuple-syntax)

##### BigQuery[¶](#id75)

```
SELECT *
FROM test.tuple_sample
WHERE (COL1.Key1, COL1.Key2) IN ((12, 34), (56, 78));

SELECT STRUCT<x ARRAY<INT64>, y INT64>(COL4.sc4, COL1.sc1)
FROM test.structTypes
WHERE COL1.sc1 IS NOT NULL;
```

##### Snowflake[¶](#id76)

```
SELECT *
FROM
test.tuple_sample
WHERE (COL1:Key1, COL1:Key2) IN ((12, 34), (56, 78));

SELECT
OBJECT_CONSTRUCT('x', COL4:sc4 :: ARRAY, 'y', COL1:sc1 :: INT)
FROM
test.structTypes
WHERE COL1:sc1 IS NOT  NULL;
```

#### Create a view using an anonymous STRUCT definition[¶](#create-a-view-using-an-anonymous-struct-definition)

##### BigQuery[¶](#id77)

```
CREATE OR REPLACE TABLE project-test.mydataset.sourcetable (
  id STRING,
  payload JSON
);

CREATE VIEW project-test.mydataset.myview AS
SELECT
  id,
  STRUCT(
    payload.user_id AS user_id,
    STRUCT(
      JSON_VALUE(payload, '$.details.ip_address') AS ip_address,
      JSON_VALUE(payload, '$.details.item_id') AS item_id,
      SAFE_CAST(JSON_VALUE(payload, '$.details.quantity') AS INT64) AS quantity,
      SAFE_CAST(JSON_VALUE(payload, '$.details.price') AS FLOAT64) AS price,
      JSON_VALUE(payload, '$.details.text') AS text
    ) AS details
  ) AS structured_payload
  FROM project-test.mydataset.sourcetable;
```

##### Snowflake[¶](#id78)

```
CREATE OR REPLACE TABLE "project-test".mydataset.sourcetable (
  id STRING,
  payload VARIANT
);

CREATE VIEW "project-test".mydataset.myview
AS
SELECT
  id,
  OBJECT_CONSTRUCT('user_id',
  payload:user_id, 'details', OBJECT_CONSTRUCT('ip_address', JSON_EXTRACT_PATH_TEXT(payload, 'details.ip_address'), 'item_id', JSON_EXTRACT_PATH_TEXT(payload, 'details.item_id'), 'quantity', TRY_CAST(JSON_EXTRACT_PATH_TEXT(payload, 'details.quantity') AS INT), 'price', TRY_CAST(JSON_EXTRACT_PATH_TEXT(payload, 'details.price') AS FLOAT), 'text', JSON_EXTRACT_PATH_TEXT(payload, 'details.text'))) AS structured_payload
  FROM
  "project-test".mydataset.sourcetable;
```

#### STRUCT column comparison expressions[¶](#struct-column-comparison-expressions)

BigQuery comparison operations for Structs compare value to value, ignoring the key if it exists,
while Snowflake comparison operations for Objects compare both, value and key. This may cause that
some comparisons return a different result.

##### BigQuery[¶](#id79)

```
SELECT * FROM test.structTypes WHERE COL1 NOT IN (COL2);
SELECT * FROM test.structTypes WHERE COL1 <> (COL2);
SELECT * FROM test.structTypes WHERE COL1 != (COL2);
```

##### Snowflake[¶](#id80)

```
SELECT * FROM
test.structTypes
--** SSC-FDM-BQ0008 - WHERE CLAUSE REFERENCES A COLUMN OF STRUCT TYPE. COMPARISON OPERATIONS MAY PRODUCE DIFFERENT RESULTS IN SNOWFLAKE. **
WHERE COL1 NOT IN (COL2);
SELECT * FROM
test.structTypes
--** SSC-FDM-BQ0008 - WHERE CLAUSE REFERENCES A COLUMN OF STRUCT TYPE. COMPARISON OPERATIONS MAY PRODUCE DIFFERENT RESULTS IN SNOWFLAKE. **
WHERE COL1 <> (COL2);
SELECT * FROM
test.structTypes
--** SSC-FDM-BQ0008 - WHERE CLAUSE REFERENCES A COLUMN OF STRUCT TYPE. COMPARISON OPERATIONS MAY PRODUCE DIFFERENT RESULTS IN SNOWFLAKE. **
WHERE COL1 != (COL2);
```

### Related EWIs[¶](#id81)

1. [SSC-FDM-BQ0010](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/bigqueryFDM#ssc-fdm-bq0010):
   Struct converted to VARIANT. Some of its usages might have functional differences.
2. [SSC-EWI-BQ0012](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/bigqueryEWI#ssc-ewi-bq0012):
   Unable to generate correct OBJECT_CONSTRUCT parameter.
3. [SSC-FDM-BQ0008](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/bigqueryFDM#ssc-fdm-bq0008):
   Where clause references a column of STRUCT type.

## TIMESTAMP[¶](#timestamp)

Timestamp data type and usages

### Description[¶](#id82)

> A timestamp value represents an absolute point in time, independent of any time zone or convention
> such as daylight saving time (DST), with microsecond precision. For more information please refer
> to
> [BigQuery Timestamp data type](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#timestamp_type).

### Grammar syntax[¶](#grammar-syntax)

<!-- prettier-ignore -->
|Name|Range|
|---|---|
|TIMESTAMP|0001-01-01 00:00:00 to 9999-12-31 23:59:59.999999 UTC|

Success

TIMESTAMP data type currently transformed to
[TIMESTAMP_TZ](https://docs.snowflake.com/en/sql-reference/data-types-datetime#timestamp-ltz-timestamp-ntz-timestamp-tz).

It is important to remark that BigQuery stores TIMESTAMP data in Coordinated Universal Time (UTC).

### Sample Source Patterns[¶](#id83)

#### TIMESTAMP without time[¶](#timestamp-without-time)

##### BigQuery[¶](#id84)

```
 CREATE OR REPLACE TABLE timestampTable
(
  COL1 TIMESTAMP
);

INSERT INTO timestampTable VALUES ('2008-12-26 15:30:00');
INSERT INTO timestampTable VALUES (TIMESTAMP'2008-12-27 18:30:00');
SELECT * FROM timestampTable;
```

##### Result[¶](#id85)

```
2008-12-26 15:30:00 UTC
2008-12-27 18:30:00 UTC
```

##### Snowflake[¶](#id86)

```
CREATE OR REPLACE TABLE timestampTable
(
  COL1 TIMESTAMP_TZ
);

INSERT INTO timestampTable VALUES ('2008-12-26 15:30:00');
INSERT INTO timestampTable VALUES (TIMESTAMP'2008-12-27 18:30:00');
SELECT * FROM timestampTable;
```

##### Result[¶](#id87)

```
2008-12-26 15:30:00.000 -0800
2008-12-27 18:30:00.000 -0800
```

#### TIMESTAMP with time zone[¶](#timestamp-with-time-zone)

When the time zone is defined you need to use the
[CONVERT_TIMEZONE](https://docs.snowflake.com/en/sql-reference/functions/convert_timezone) function
to store the data in Coordinated Universal Time (UTC). Also the timezone name inside the timestamp
literal is not supported by Snowflake, in that case it is necessary to use this function as well.

##### BigQuery[¶](#id88)

```
CREATE OR REPLACE TABLE test.timestampType
(
  COL1 TIMESTAMP
);

INSERT INTO test.timestampType VALUES ('2008-12-25 15:30:00 America/Chicago');
INSERT INTO test.timestampType VALUES ('2018-04-05 12:00:00+02:00');
INSERT INTO test.timestampType VALUES ('2008-12-26 15:30:00-08:00');
INSERT INTO test.timestampType VALUES (TIMESTAMP'2022-12-25 15:30:00 America/North_Dakota/New_Salem');
INSERT INTO test.timestampType VALUES (TIMESTAMP'2022-04-05 12:00:00+02:00');
INSERT INTO test.timestampType VALUES (TIMESTAMP'2022-12-26 15:30:00-08:00');
SELECT * FROM test.timestampType ORDER BY COL1;
```

##### Result[¶](#id89)

```
2008-12-25 21:30:00 UTC
2008-12-26 23:30:00 UTC
2018-04-05 10:00:00 UTC
2022-04-05 10:00:00 UTC
2022-12-25 21:30:00 UTC
2022-12-26 23:30:00 UTC
```

##### Snowflake[¶](#id90)

```
CREATE OR REPLACE TABLE test.timestampType
(
  COL1 TIMESTAMP_TZ
);

INSERT INTO test.timestampType
VALUES (CONVERT_TIMEZONE('America/Chicago', 'UTC', '2008-12-25 15:30:00'));
INSERT INTO test.timestampType
VALUES (CONVERT_TIMEZONE('UTC','2018-04-05 12:00:00+02:00'));
INSERT INTO test.timestampType
VALUES (CONVERT_TIMEZONE('UTC','2008-12-26 15:30:00-08:00'));

INSERT INTO test.timestampType
VALUES (CONVERT_TIMEZONE('America/North_Dakota/New_Salem', 'UTC', '2022-12-25 15:30:00'));
INSERT INTO test.timestampType
VALUES (CONVERT_TIMEZONE('UTC', '2022-04-05 12:00:00+02:00'));
INSERT INTO test.timestampType
VALUES (CONVERT_TIMEZONE('UTC', '2022-12-26 15:30:00-08:00'));
SELECT * FROM test.timestampType ORDER BY COL1;
```

##### Result[¶](#id91)

```
 2008-12-25 21:30:00.000 -0800
2008-12-26 23:30:00.000 +0000
2018-04-05 10:00:00.000 +0000
2022-04-05 10:00:00.000 +0000
2022-12-25 21:30:00.000 -0800
2022-12-26 23:30:00.000 +0000
```
