---
description:
  Snowflake supports most basic SQL data types (with some restrictions) for columns, local
  variables, expressions, parameters, and other appropriate/suitable locations.
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/hive/data-types
title: SnowConvert AI - Hive - Data Types | Snowflake Documentation
---

## Exact and approximate numerics[¶](#exact-and-approximate-numerics)

<!-- prettier-ignore -->
|SparkSQL-DatabricksSQL|Snowflake|Notes|
|---|---|---|
|TINYINT, SHORT|SMALLINT|​Snowflake's SMALLINT has a larger range (-32768 to +32767) than Spark's TINYINT (-128 to +127). This should generally be a safe transformation.|
|SMALLINT|SMALLINT|Direct equivalent in terms of range.|
|INT, INTEGER|INT, INTEGER|​Direct equivalent in terms of range.|
|BIGINT|BIGINT​|Direct equivalent in terms of range.|
|DECIMAL(p, s)​|NUMBER(p, s)|Snowflake's NUMBER(p, s) is the direct equivalent for fixed-precision and scale numbers. p is the precision (total number of digits) and s is the scale (number of digits to the right of the decimal point).|
|NUMERIC(p, s)|NUMBER(p, s)|Synonym for DECIMAL(p, s), maps directly to Snowflake's NUMBER(p, s).|
|FLOAT|FLOAT|Direct equivalent in terms of range.|
|DOUBLE, DOUBLE PRECISION|DOUBLE|Generally a good equivalent for double-precision floating-point numbers.|
|REAL|REAL|If REAL in your Spark context is strictly single-precision, be mindful of potential precision differences.|

## Date and time [¶](#date-and-time)

<!-- prettier-ignore -->
|Hive-Spark-Databricks SQL|Snowflake|Notes|
|---|---|---|
|DATE|DATE|Direct equivalent for storing calendar dates (year, month, day).|
|TIMESTAMP|TIMESTAMP_NTZ|Snowflake offers several timestamp variations. TIMESTAMP_NTZ (no time zone) is often the best general equivalent if your Spark TIMESTAMP doesn’t have specific time zone information tied to the data itself.|

## Character strings [¶](#character-strings)

<!-- prettier-ignore -->
|Hive-Spark-Databricks SQL|Snowflake|Notes|
|---|---|---|
|STRING|VARCHAR|​Snowflake’s VARCHAR is the most common and flexible string type. It can store variable-length strings.|
|VARCHAR(n)​|VARCHAR(n)|Direct equivalent for variable-length strings with a maximum length.|
|CHAR(n)|CHAR(n)|Direct equivalent for fixed-length strings.|

## Binary strings [¶](#binary-strings)

<!-- prettier-ignore -->
|Hive-Spark-Databricks SQL|Snowflake|Notes|
|---|---|---|
|BINARY|​BINARY|Direct equivalent for storing raw byte sequences.|

## Boolean type [¶](#boolean-type)

<!-- prettier-ignore -->
|Hive-Spark-Databricks SQL|Snowflake|Notes|
|---|---|---|
|BOOLEAN, BOOL|​BOOLEAN|Direct equivalent for storing boolean (TRUE/FALSE) values.|

## Complex type [¶](#complex-type)

<!-- prettier-ignore -->
|Hive-Spark-Databricks SQL|Snowflake|Notes|
|---|---|---|
|ARRAY<DataType>|​ARRAY|Snowflake’s ARRAY type can store ordered lists of elements of a specified data type. The dataType within the array should also be mapped accordingly.|
|MAP<keyType, valueType>|VARIANT||
|STRUCT<name: dataType, …>|VARIANT||
|INTERVAL|VARCHAR(30)|INTERVAL data type is **not supported** in Snowflake. VARCHAR is used instead.|
