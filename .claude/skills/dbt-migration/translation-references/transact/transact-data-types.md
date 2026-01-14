---
description:
  Snowflake supports most basic SQL data types (with some restrictions) for use in columns, local
  variables, expressions, parameters, and any other appropriate/suitable locations.
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/transact/transact-data-types
title: SnowConvert AI - SQL Server-Azure Synapse - Data Types | Snowflake Documentation
---

## Exact and approximate numerics[¶](#exact-and-approximate-numerics)

<!-- prettier-ignore -->
|T-SQL|Snowflake|Notes|
|---|---|---|
|BIGINT|BIGINT|​Note that BIGINT in Snowflake is an alias for NUMBER(38,0) [See note on this conversion below.]|
|BIT|BOOLEAN|SQLServer only accepts ​1, 0, or NULL|
|DECIMAL|DECIMAL|​Snowflake’s DECIMAL is synonymous with NUMBER|
|FLOAT|FLOAT|​This data type behaves equally on both systems. Precision 7-15 digits, float (1-24) Storage 4 - 8 bytes, float (25-53)|
|INT|INT|Note that INT in Snowflake is an alias for NUMBER(38,0) [See note on this conversion below.]|
|MONEY|NUMBER(38, 4)|[See note on this conversion below.]|
|REAL​|REAL|Snowflake’s REAL is synonymous with FLOAT|
|SMALLINT|SMALLINT​|​This data type behaves equally|
|SMALLMONEY|NUMBER(38, 4)|[See note on this conversion below.]|
|TINYINT​|TINYINT|Note that TINYINT in Snowflake is an alias for NUMBER(38,0) [See note on this conversion below.]|
|NUMERIC|NUMERIC|​Snowflake’s NUMERIC is synonymous with NUMBER|

**NOTE:**

- For the conversion of integer data types (INT, SMALLINT, BIGINT, TINYINT), each is converted to
  the alias in Snowflake with the same name. Each of those aliases is actually converted to
  NUMBER(38,0), a data type that is considerably larger than the integer datatype. Below is a
  comparison of the range of values that can be present in each data type:

  - Snowflake NUMBER(38,0): -99999999999999999999999999999999999999 to
    +99999999999999999999999999999999999999
  - SQLServer TINYINT: 0 to 255
  - SQLServer INT: -2^31 (-2,147,483,648) to 2^31-1 (2,147,483,647)
  - SQLServer BIGINT: -2^63 (-9,223,372,036,854,775,808) to 2^63-1 (9,223,372,036,854,775,807)
  - SQLServer SMALLINT: -2^15 (-32,768) to 2^15-1 (32,767)

- For Money and Smallmoney: ​

  - Currency or monetary data does not need to be enclosed in single quotation marks ( ‘ ). It is
    important to remember that while you can specify monetary values preceded by a currency symbol,
    SQL Server does not store any currency information associated with the symbol, it only stores
    the numeric value.
  - Please take care on the translations for the DMLs

## Date and time[¶](#date-and-time)

<!-- prettier-ignore -->
|T-SQL|Snowflake|Notes|
|---|---|---|
|DATE|DATE|​SQLServer accepts range from 0001-01-01 to 9999-12-31|
|DATETIME2|TIMESTAMP_NTZ(7)​|Snowflake’s DATETIME is an alias for TIMESTAMP_NTZ|
|DATETIME|TIMESTAMP_NTZ(3)|Snowflake’s DATETIME is an alias for TIMESTAMP_NTZ​|
|DATETIMEOFFSET|TIMESTAMP_TZ(7)|Snowflake’s timestamp precision ranges from 0 to 9 (_this value’s the default_) Snowflake’s operations are performed in the current session’s time zone, controlled by the TIMEZONE session parameter|
|SMALLDATETIME|TIMESTAMP_NTZ|Snowflake’s DATETIME truncates the TIME information i.e. 1955-12-13 12:43:10 is saved as 1955-12-13|
|TIME|TIME|​This data type behaves equally on both systems. Range 00:00:00.0000000 through 23:59:59.9999999|
|TIMESTAMP|TIMESTAMP|This is an user defined data type in TSQL so it’s converted to it’s equivalent in snowflake Timestamp.|

## Character strings[¶](#character-strings)

<!-- prettier-ignore -->
|T-SQL|Snowflake|Notes|
|---|---|---|
|CHAR|CHAR|​SQLServer’s max string size in bytes is 8000 whereas Snowflake is 167772161.|
|TEXT​|TEXT||
|VARCHAR​|VARCHAR|SQLServer’s max string size in bytes is 8000 whereas Snowflake is 167772161. SQLServer’s VARCHAR(MAX) has no equivalent in SnowFlake, it is converted to VARCHAR to take the largest possible size by default.|

## Unicode character strings[¶](#unicode-character-strings)

<!-- prettier-ignore -->
|T-SQL|Snowflake|Notes|
|---|---|---|
|NCHAR|NCHAR|Synonymous with VARCHAR except default length is VARCHAR(1).|
|NTEXT|TEXT|Snowflake use TEXT data type as a synonymous with VARCHAR ​SQLServer’s NTEXT(MAX) has no equivalent in SnowFlake, it is converted to VARCHAR to take the largest possible size by default.|
|NVARCHAR|VARCHAR|Snowflake use this data type as a synonymous with VARCHAR ​SQLServer’s NVARCHAR(MAX) has no equivalent in SnowFlake, it is converted to VARCHAR to take the largest possible size by default.|

## Binary strings[¶](#binary-strings)

<!-- prettier-ignore -->
|T-SQL|Snowflake|Notes|
|---|---|---|
|BINARY|​BINARY|In Snowflake the maximum length is 8 MB (8,388,608 bytes) and length is always measured in terms of bytes.|
|VARBINARY|VARBINARY|Snowflake use this data type as a synonymous with BINARY. Snowflake often represents each byte as 2 hexadecimal characters|
|IMAGE|VARBINARY|​Snowflake use this data type as a synonymous with BINARY. Snowflake often represents each byte as 2 hexadecimal characters|

## Other data types[¶](#other-data-types)

<!-- prettier-ignore -->
|T-SQL|Snowflake|Notes|
|---|---|---|
|CURSOR|_\*to be defined_|Not supported by Snowflake. Translate into Cursor helpers|
|HIERARCHYID|_\*to be defined_|Not supported by Snowflake|
|SQL_VARIANT|VARIANT|Maximum size of 16 MB compressed. A value of any data type can be implicitly cast to a VARIANT value|
|GEOMETRY|_\*to be defined_|Not supported by Snowflake|
|GEOGRAPHY|GEOGRAPHY|The objects store in Snowflake’s GEOGRAPHY data type must be WKT / WKB / EWKT / EWKB / GeoJSON geospatial objects to support LineString and Polygon objects|
|TABLE|_\*to be defined_|Not supported by Snowflake|
|ROWVERSION|_\*to be defined_|Not supported by Snowflake|
|UNIQUEIDENTIFIER|VARCHAR|​​Snowflake use STRING type as a synonymous with VARCHAR. Because of conversion Snowflake often represents each byte as 2 hexadecimal characters|
|XML|VARIANT|​Snowflake use VARIANT data type as a synonymous with XML|
|SYSNAME|VARCHAR(128)|NOT NULL constraint added to the column definition|
