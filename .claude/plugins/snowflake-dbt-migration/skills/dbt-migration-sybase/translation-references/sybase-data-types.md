---
description:
  Snowflake supports most basic SQL data types (with some restrictions) for columns, local
  variables, expressions, parameters, and other appropriate/suitable locations.
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/sybase/sybase-data-types
title: SnowConvert AI - Sybase IQ - Data Types | Snowflake Documentation
---

## Exact and approximate numerics

<!-- prettier-ignore -->
|Sybase|Snowflake|Notes|
|---|---|---|
|Sybase|Snowflake|Notes|
|BIGINT|BIGINT|​Note that BIGINT in Snowflake is an alias for NUMBER(38,0) [See note on this conversion below.]|
|BIT|BOOLEAN|Sybase only accepts ​1, 0, or NULL|
|DECIMAL|DECIMAL|​Snowflake's DECIMAL is synonymous with NUMBER|
|FLOAT|FLOAT|​This data type behaves equally on both systems. Precision 7-15 digits, float (1-24) Storage 4 - 8 bytes, float (25-53)|
|INT|INT|Note that INT in Snowflake is an alias for NUMBER(38,0) [See note on this conversion below.]|
|SMALLINT|SMALLINT​|​This data type behaves equally|
|TINYINT​|TINYINT|Note that TINYINT in Snowflake is an alias for NUMBER(38,0) [See note on this conversion below.]|
|NUMERIC|NUMERIC|​Snowflake's NUMERIC is synonymous with NUMBER|

### NOTE

- Each is converted to the alias in Snowflake with the same name for the conversion of integer data
  types (INT, SMALLINT, BIGINT, TINYINT). Each of those aliases is converted to NUMBER(38,0), a data
  type considerably larger than the integer datatype. Below is a comparison of the range of values
  that can be present in each data type:
  - Snowflake NUMBER(38,0): -99999999999999999999999999999999999999 to
    +99999999999999999999999999999999999999
  - Sybase TINYINT: 0 to 255
  - Sybase INT: -2^31 (-2,147,483,648) to 2^31-1 (2,147,483,647)
  - Sybase BIGINT: -2^63 (-9,223,372,036,854,775,808) to 2^63-1 (9,223,372,036,854,775,807)
  - Sybase SMALLINT: -2^15 (-32,768) to 2^15-1 (32,767)

## Date and time

<!-- prettier-ignore -->
|Sybase|Snowflake|Notes|
|---|---|---|
|DATE|DATE|Sybase accepts range from 0001-01-01 to 9999-12-31|
|DATETIME|TIMESTAMP_NTZ(3)|Snowflake’s DATETIME is an alias for TIMESTAMP_NTZ​|
|SMALLDATETIME|TIMESTAMP_NTZ|Snowflake’s DATETIME truncates the TIME information i.e. 1955-12-13 12:43:10 is saved as 1955-12-13|
|TIME|TIME|​This data type behaves equally on both systems. Range 00:00:00.0000000 through 23:59:59.9999999|
|TIMESTAMP|TIMESTAMP||

## Character strings

<!-- prettier-ignore -->
|Sybase|Snowflake|Notes|
|---|---|---|
|CHAR|CHAR|​Snowflake’s max string size in bytes is 167772161.|
|TEXT​|TEXT||
|VARCHAR​|VARCHAR|Snowflake’s max string size in bytes is 167772161.|

## Unicode character strings

<!-- prettier-ignore -->
|Sybase|Snowflake|Notes|
|---|---|---|
|NCHAR|NCHAR|Synonymous with VARCHAR except default length is VARCHAR(1).|
|NTEXT|TEXT|NTEXT is an Sybase domain type, implemented as a LONG NVARCHAR.|
|NVARCHAR|VARCHAR|Snowflake’s max string size in bytes is 167772161.|

## Binary strings

<!-- prettier-ignore -->
|Sybase|Snowflake|Notes|
|---|---|---|
|BINARY|​BINARY|In Snowflake the maximum length is 8 MB (8,388,608 bytes) and length is always measured in terms of bytes.|
|VARBINARY|VARBINARY|Snowflake use this data type as a synonymous with BINARY. Snowflake often represents each byte as 2 hexadecimal characters|
