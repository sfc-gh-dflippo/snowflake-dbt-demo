---
description: Current Data types conversion for PostgreSQL to Snowflake.
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/postgres/data-types/postgresql-data-types
title: SnowConvert AI - PostgreSQL - Data types | Snowflake Documentation
---

## Applies to

- PostgreSQL
- Greenplum
- Netezza

Snowflake supports most basic
[SQL data types](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types) (with some
restrictions) for use in columns, local variables, expressions, parameters, and any other
appropriate/suitable locations.

## Numeric Data Types

<!-- prettier-ignore -->
|PostgreSQL|Snowflake|
|---|---|
|INT|INT|
|INT2|SMALLINT|
|INT4|INTEGER|
|INT8|INTEGER|
|INTEGER|INTEGER|
|BIGINT|BIGINT|
|DECIMAL|DECIMAL|
|DOUBLE PRECISION|DOUBLE PRECISION|
|NUMERIC​|NUMERIC|
|SMALLINT|SMALLINT|
|FLOAT|FLOAT|
|FLOAT4|FLOAT4|
|FLOAT8|FLOAT8|
|REAL|REAL​|
|BIGSERIAL/SERIAL8|INTEGER _Note: Snowflake supports defining columns as IDENTITY, which automatically generates sequential values. This is the more concise and often preferred approach in Snowflake._|

## Character Types

<!-- prettier-ignore -->
|PostgreSQL|Snowflake|
|---|---|
|VARCHAR|VARCHAR _Note: VARCHAR holds Unicode UTF-8 characters. If no length is specified, the default is the maximum allowed length (16,777,216)._|
|CHAR|CHAR|
|CHARACTER|CHARACTER _Note:_ Snowflake’s CHARACTER is an alias for VARCHAR.|
|NCHAR|NCHAR|
|BPCHAR|VARCHAR _Note: BPCHAR data type is **not supported** in Snowflake. VARCHAR is used instead. For more information please refer to_ [_SSC-FDM-PG0002_](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/postgresqlFDM.md#ssc-fdm-pg0002)_._|
|CHARACTER VARYING|CHARACTER VARYING|
|NATIONAL CHARACTER|NCHAR|
|NATIONAL CHARACTER VARYING|NCHAR VARYING|
|TEXT|TEXT|
|[NAME](https://www.postgresql.org/docs/current/datatype-character.html) (Special character type)|VARCHAR|

## Boolean Types

<!-- prettier-ignore -->
|PostgreSQL|Snowflake|
|---|---|
|BOOL/BOOLEAN|BOOLEAN|

## Binary Types

<!-- prettier-ignore -->
|PostgreSQL|Snowflake|
|---|---|
|BYTEA|BINARY|

## Bit String Types

<!-- prettier-ignore -->
|PostgreSQL|Snowflake|
|---|---|
|BIT|CHARACTER|
|BIT VARYING|CHARACTER VARYING|
|VARBIT|CHARACTER VARYING|

## Date & Time Data

<!-- prettier-ignore -->
|PostgreSQL|Snowflake|
|---|---|
|DATE|DATE|
|TIME|TIME|
|TIME WITH TIME ZONE|TIME _Note: Time zone not supported for time data type. For more information, please refer to_ [_SSC-FDM-0005_](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.md#ssc-fdm-0005)_._|
|TIME WITHOUT TIME ZONE|TIME|
|TIMESTAMP|TIMESTAMP|
|TIMESTAMPTZ|TIMESTAMP_TZ|
|TIMESTAMP WITH TIME ZONE|TIMESTAMP_TZ|
|TIMESTAMP WITHOUT TIME ZONE|TIMESTAMP_NTZ|
|INTERVAL YEAR TO MONTH|VARCHAR _Note: Data type is **not supported** in Snowflake. VARCHAR is used instead. For more information please refer to_ [_SSC-EWI-0036_](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.md#ssc-ewi-0036)_._|
|INTERVAL DAY TO SECOND|VARCHAR _Note: Data type is **not supported** in Snowflake. VARCHAR is used instead. For more information please refer to_ [_SSC-EWI-0036_](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.md#ssc-ewi-0036)_._|

## Pseudo Types

<!-- prettier-ignore -->
|PostgreSQL|Snowflake|
|---|---|
|UNKNOWN|TEXT _Note: Data type is **not supported** in Snowflake. TEXT is used instead. For more information please refer to_ [_SSC-EWI-0036_](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.md#ssc-ewi-0036)_._|

## Array Types

<!-- prettier-ignore -->
|PostgreSQL|Snowflake|
|---|---|
|type []|ARRAY _Note: Strongly typed array transformed to ARRAY without type checking. For more information please refer to_ [_SSC-FDM-PG0016_](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/postgresqlFDM.md#ssc-fdm-pg0016)_._|

## Related EWIs

1. [SSC-FDM-PG0002](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/postgresqlFDM#ssc-fdm-pg0002):
   Bpchar converted to varchar.
2. [SSC-FDM-PG0003](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/postgresqlFDM#ssc-fdm-pg0003):
   Bytea Converted To Binary
3. [SSC-FDM-PG0014](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/postgresqlFDM#ssc-fdm-pg0014):
   Unknown Pseudotype transformed to Text Type
4. [SSC-FDM-0005](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0005):
   TIME ZONE not supported for time data type.
5. [SSC-EWI-0036](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0036):
   Data type converted to another data type.
6. [SSC-EWI-PG0016](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/postgresqlEWI#ssc-ewi-pg0016):
   Bit String Type converted to Varchar Type.
7. [SSC-FDM-PG0016](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/postgresqlFDM#ssc-fdm-pg0016):
   _Strongly typed array transformed to ARRAY without type checking_.
