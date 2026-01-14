---
description:
  Translation reference for all the supported built-in functions by SnowConvert AI for BigQuery.
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/bigquery/bigquery-functions
title: SnowConvert AI - BigQuery - Built-in functions | Snowflake Documentation
---

## Aggregate Functions[¶](#aggregate-functions)

<!-- prettier-ignore -->
|BigQuery|Snowflake|
|---|---|
|[ANY_VALUE](https://cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions#any_value)|[ANY_VALUE](https://docs.snowflake.com/en/sql-reference/functions/any_value) _Note: Unlike BigQuery, Snowflake does not ignore NULLs . Additionally, Snowflake’s `OVER()` clause does not support the use of `ORDER BY` or explicit window frames._|
|[ANY_VALUE](https://cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions#any_value)( expr1, HAVING MAX expr2) [ANY_VALUE](https://cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions#any_value)( expr1, HAVING MIN expr2)|[MAX_BY](https://docs.snowflake.com/en/sql-reference/functions/max_by)(expr1, expr1) [MIN_BY](https://docs.snowflake.com/en/sql-reference/functions/min_by)(expr1, expr2)|
|[AVG](https://cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions#avg)|[AVG](https://docs.snowflake.com/en/sql-reference/functions/avg)|
|[COUNT](https://cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions#count)|[COUNT](https://docs.snowflake.com/en/sql-reference/functions/count)|
|[COUNTIF](https://cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions#countif)|[COUNT_IF](https://docs.snowflake.com/en/sql-reference/functions/count_if)|
|[LOGICAL_AND](https://cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions#logical_and)|[BOOLAND_AGG](https://docs.snowflake.com/en/sql-reference/functions/booland_agg)|
|[LOGICAL_OR](https://cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions#logical_or)|[BOOLOR_AGG](https://docs.snowflake.com/en/sql-reference/functions/boolor_agg)|
|[MAX](https://cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions#max)|[MAX](https://docs.snowflake.com/en/sql-reference/functions/max)|
|[MIN](https://cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions#min)|[MIN](https://docs.snowflake.com/en/sql-reference/functions/min)|
|[SUM](https://cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions#sum)|[SUM](https://docs.snowflake.com/en/sql-reference/functions/sum)|

## Array Functions[¶](#array-functions)

<!-- prettier-ignore -->
|BigQuery|Snowflake|
|---|---|
|[ARRAY_AGG](https://cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions#array_agg)|[ARRAY_AGG](https://docs.snowflake.com/en/sql-reference/functions/array_agg)|
|[ARRAY_CONCAT](https://cloud.google.com/bigquery/docs/reference/standard-sql/array_functions#array_concat)|[ARRAY_CAT](https://docs.snowflake.com/en/sql-reference/functions/array_cat)|
|[ARRAY_CONCAT_AGG](https://cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions#array_concat_agg)|[ARRAY_FLATTEN](https://docs.snowflake.com/en/sql-reference/functions/array_flatten)|
|[ARRAY_TO_STRING](https://cloud.google.com/bigquery/docs/reference/standard-sql/array_functions#array_to_string)(expr, delimiter)|[ARRAY_TO_STRING](https://docs.snowflake.com/en/sql-reference/functions/array_to_string)(ARRAY_COMPACT(expr), delimiter)|
|[ARRAY_TO_STRING](https://cloud.google.com/bigquery/docs/reference/standard-sql/array_functions#array_to_string)(expr, delimiter, null_text)|ARRAY*TO_STRING_UDF(expr, delimiter, null_text) \_Notes: SnowConvert AI generates a UDF to handle the NULL replacement parameter which is not natively supported in Snowflake’s ARRAY_TO_STRING function.*|
|[SELECT ARRAY](https://cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax#array_subquery) (SELECT query)|SELECT (SELECT ARRAY*AGG(\*) FROM (SELECT query)) \_Notes: BigQuery’s ARRAY subquery syntax is transformed to use ARRAY_AGG with a subquery in Snowflake.*|

## Conditional Expressions[¶](#conditional-expressions)

<!-- prettier-ignore -->
|BigQuery|Snowflake|
|---|---|
|[COALESCE](https://cloud.google.com/bigquery/docs/reference/standard-sql/conditional_expressions#coalesce)|[COALESCE](https://docs.snowflake.com/en/sql-reference/functions/coalesce)|
|[IF](https://cloud.google.com/bigquery/docs/reference/standard-sql/conditional_expressions#if)|[IFF](https://docs.snowflake.com/en/sql-reference/functions/iff)|
|[IFNULL](https://cloud.google.com/bigquery/docs/reference/standard-sql/conditional_expressions#ifnull)|[IFNULL](https://docs.snowflake.com/en/sql-reference/functions/ifnull)|
|[NULLIF](https://cloud.google.com/bigquery/docs/reference/standard-sql/conditional_expressions#nullif)|[NULLIF](https://docs.snowflake.com/en/sql-reference/functions/nullif)|

## Conversion Functions[¶](#conversion-functions)

<!-- prettier-ignore -->
|BigQuery|Snowflake|
|---|---|
|[SAFE_CAST](https://cloud.google.com/bigquery/docs/reference/standard-sql/conversion_functions#safe_casting)|[TRY_CAST](https://docs.snowflake.com/en/sql-reference/functions/try_cast)|

## Date Functions[¶](#date-functions)

<!-- prettier-ignore -->
|BigQuery|Snowflake|
|---|---|
|[CURRENT_DATE](https://cloud.google.com/bigquery/docs/reference/standard-sql/date_functions#current_date) [CURRENT_DATE](https://cloud.google.com/bigquery/docs/reference/standard-sql/date_functions#current_date)()|[CURRENT_DATE](https://docs.snowflake.com/en/sql-reference/functions/current_date) [CURRENT_DATE](https://docs.snowflake.com/en/sql-reference/functions/current_date)()|
|[FORMAT_DATE](https://cloud.google.com/bigquery/docs/reference/standard-sql/date_functions#format_date)|[TO_CHAR](https://docs.snowflake.com/en/sql-reference/functions/to_char) _Note: For further details on this translation, please consult this_ [_page_](format_date.md)_._|

## Datetime Functions[¶](#datetime-functions)

<!-- prettier-ignore -->
|BigQuery|Snowflake|
|---|---|
|[CURRENT_DATETIME](https://cloud.google.com/bigquery/docs/reference/standard-sql/datetime_functions#current_datetime) [CURRENT_DATETIME](https://cloud.google.com/bigquery/docs/reference/standard-sql/datetime_functions#current_datetime)()|[CURRENT_TIMESTAMP](https://docs.snowflake.com/en/sql-reference/functions/current_timestamp) :: TIMESTAMP_NTZ [CURRENT_TIMESTAMP](https://docs.snowflake.com/en/sql-reference/functions/current_timestamp)() :: TIMESTAMP_NTZ|

## Geography Functions[¶](#geography-functions)

<!-- prettier-ignore -->
|BigQuery|Snowflake|
|---|---|
|[ST_GEOGFROMTEXT](https://cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions#st_geogfromtext)|[ST_GEOGFROMTEXT](https://docs.snowflake.com/en/sql-reference/functions/st_geographyfromwkt) _Note: For further details on this translation, please consult this_ [_page_](st_geogfromtext.md)_._|
|[ST_GEOGPOINT](https://cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions#st_geogpoint)|[ST_POINT](https://docs.snowflake.com/en/sql-reference/functions/st_makepoint) _Note: For further details on this translation, please consult this_ [_page_](st_geogpoint.md)_._|

## JSON Functions[¶](#json-functions)

<!-- prettier-ignore -->
|BigQuery|Snowflake|
|---|---|
|[JSON_VALUE](https://cloud.google.com/bigquery/docs/reference/standard-sql/json_functions#json_value) / [JSON_EXTRACT_SCALAR](https://cloud.google.com/bigquery/docs/reference/standard-sql/json_functions#json_extract_scalar)|[JSON_EXTRACT_PATH_TEXT](https://docs.snowflake.com/en/sql-reference/functions/json_extract_path_text) _Notes: SnowConvert AI automatically translates BigQuery JSON paths to their Snowflake equivalents._|
|[JSON_VALUE_ARRAY](https://cloud.google.com/bigquery/docs/reference/standard-sql/json_functions#json_value_array)|JSON*VALUE_ARRAY_UDF \_Notes: SnowConvert AI generates a UDF to obtain an equivalent behavior for extracting arrays from JSON.*|
|[LAX_INT64](https://cloud.google.com/bigquery/docs/reference/standard-sql/json_functions#lax_int64)|PUBLIC.LAX*INT64_UDF \_Notes: SnowConvert AI generates a UDF to obtain an equivalent behavior.*|
|[LAX_BOOL](https://cloud.google.com/bigquery/docs/reference/standard-sql/json_functions#lax_bool)|PUBLIC.LAX*BOOL_UDF \_Notes: SnowConvert AI generates a UDF to obtain an equivalent behavior.*|

## Mathematical Functions[¶](#mathematical-functions)

<!-- prettier-ignore -->
|BigQuery|Snowflake|
|---|---|
|[ABS](https://cloud.google.com/bigquery/docs/reference/standard-sql/mathematical_functions#abs)|[ABS](https://docs.snowflake.com/en/sql-reference/functions/abs)|
|[LEAST](https://cloud.google.com/bigquery/docs/reference/standard-sql/mathematical_functions#least)|[LEAST](https://docs.snowflake.com/en/sql-reference/functions/least)|
|[MOD](https://cloud.google.com/bigquery/docs/reference/standard-sql/mathematical_functions#mod)|[MOD](https://docs.snowflake.com/en/sql-reference/functions/mod)|
|[ROUND](https://cloud.google.com/bigquery/docs/reference/standard-sql/mathematical_functions#round)(X) [ROUND](https://cloud.google.com/bigquery/docs/reference/standard-sql/mathematical_functions#round)(X, Y) [ROUND](https://cloud.google.com/bigquery/docs/reference/standard-sql/mathematical_functions#round)(X, Y, ‘ROUND_HALF_EVEN’) [ROUND](https://cloud.google.com/bigquery/docs/reference/standard-sql/mathematical_functions#round)(X, Y, ‘ROUND_HALF_AWAY_FROM_ZERO’)|[ROUND](https://docs.snowflake.com/en/sql-reference/functions/round)(X) [ROUND](https://docs.snowflake.com/en/sql-reference/functions/round)(X, Y) [ROUND](https://docs.snowflake.com/en/sql-reference/functions/round)(X, Y, ‘HALF_TO_EVEN’) [ROUND](https://docs.snowflake.com/en/sql-reference/functions/round)(X, Y, ‘HALF_AWAY_FROM_ZERO’)|

## Navigation Functions[¶](#navigation-functions)

<!-- prettier-ignore -->
|BigQuery|Snowflake|
|---|---|
|[FIRST_VALUE](https://cloud.google.com/bigquery/docs/reference/standard-sql/navigation_functions#first_value)|[FIRST_VALUE](https://docs.snowflake.com/en/sql-reference/functions/first_value)|
|[LAG](https://cloud.google.com/bigquery/docs/reference/standard-sql/navigation_functions#lag)|[LAG](https://docs.snowflake.com/en/sql-reference/functions/lag)|
|[LEAD](https://cloud.google.com/bigquery/docs/reference/standard-sql/navigation_functions#lead)|[LEAD](https://docs.snowflake.com/en/sql-reference/functions/lead)|
|[LAST_VALUE](https://cloud.google.com/bigquery/docs/reference/standard-sql/navigation_functions#last_value)|[LAST_VALUE](https://docs.snowflake.com/en/sql-reference/functions/last_value)|

## Numbering Functions[¶](#numbering-functions)

<!-- prettier-ignore -->
|BigQuery|Snowflake|
|---|---|
|[RANK](https://cloud.google.com/bigquery/docs/reference/standard-sql/numbering_functions#rank)|[RANK](https://docs.snowflake.com/en/sql-reference/functions/rank)|
|[ROW_NUMBER](https://cloud.google.com/bigquery/docs/reference/standard-sql/numbering_functions#row_number)|[ROW_NUMBER](https://docs.snowflake.com/en/sql-reference/functions/row_number)|

## String Functions[¶](#string-functions)

<!-- prettier-ignore -->
|BigQuery|Snowflake|
|---|---|
|[BYTE_LENGTH](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#byte_length)(expr)|LENGTH(TO*BINARY(HEX_ENCODE(expr))) \_Notes: BigQuery’s BYTE_LENGTH returns the number of bytes in a encoded string. Snowflake equivalent converts to binary after hex encoding to get byte length.*|
|[CHARACTER_LENGTH](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#character_length) [CHAR_LENGTH](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#char_length)|[LENGTH](https://docs.snowflake.com/en/sql-reference/functions/length)|
|[CONCAT](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#concat)|[CONCAT](https://docs.snowflake.com/en/sql-reference/functions/concat)|
|[ENDS_WITH](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#ends_with)|[ENDSWITH](https://docs.snowflake.com/en/sql-reference/functions/endswith)|
|[FROM_BASE64](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#from_base64)|[TRY_BASE64_DECODE_BINARY](https://docs.snowflake.com/en/sql-reference/functions/try_base64_decode_binary) _Notes: BigQuery defaults to BASE64 for binary data output, but Snowflake uses HEX. In Snowflake, you can use the_ [_`BASE64_ENCODE`_](https://docs.snowflake.com/en/sql-reference/functions/base64_encode) _function or set_ [_`BINARY_OUTPUT_FORMAT`_](https://docs.snowflake.com/en/sql-reference/parameters#binary-output-format) _to `’BASE64’` to view binary data in BASE64._|
|[FROM_HEX](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#from_hex)|[TRY_HEX_DECODE_BINARY](https://docs.snowflake.com/en/sql-reference/functions/try_hex_decode_binary) _Notes: BigQuery defaults to BASE64 for binary data output, but Snowflake uses HEX. In Snowflake, you can use the_ [_`BASE64_ENCODE`_](https://docs.snowflake.com/en/sql-reference/functions/base64_encode) _function or set_ [_`BINARY_OUTPUT_FORMAT`_](https://docs.snowflake.com/en/sql-reference/parameters#binary-output-format) _to `’BASE64’` to view binary data in BASE64._|
|[LEFT](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#left)|[LEFT](https://docs.snowflake.com/en/sql-reference/functions/left)|
|[LENGTH](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#length)|[LENGTH](https://docs.snowflake.com/en/sql-reference/functions/length)|
|[LOWER](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#lower)|[LOWER](https://docs.snowflake.com/en/sql-reference/functions/lower)|
|[LPAD](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#lpad)|[LPAD](https://docs.snowflake.com/en/sql-reference/functions/lpad)|
|[LTRIM](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#ltrim)|[LTRIM](https://docs.snowflake.com/en/sql-reference/functions/ltrim)|
|[REGEXP_CONTAINS](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#regexp_contains)(value, regexp)|[REGEXP_INSTR](../../../../sql-reference/functions/regexp_instr)(value, regexp) > 0|
|[REGEXP_EXTRACT_ALL](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#regexp_extract_all)|[REGEXP_SUBSTR_ALL](https://docs.snowflake.com/en/sql-reference/functions/regexp_substr_all)|
|[REPLACE](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#replace)|[REPLACE](https://docs.snowflake.com/en/sql-reference/functions/replace)|
|[RIGHT](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#right)|[RIGHT](https://docs.snowflake.com/en/sql-reference/functions/right)|
|[RPAD](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#rpad)|[RPAD](https://docs.snowflake.com/en/sql-reference/functions/rpad)|
|[RTRIM](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#rtrim)|[RTRIM](https://docs.snowflake.com/en/sql-reference/functions/rtrim)|
|[SPLIT](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#split)|[SPLIT](https://docs.snowflake.com/en/sql-reference/functions/split)|
|[STARTS_WITH](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#starts_with)|[STARTSWITH](https://docs.snowflake.com/en/sql-reference/functions/startswith)|
|[SUBSTR](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#substr)(string, position) [SUBSTRING](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#substring)(string, position) [SUBSTR](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#substr)(sttring, position, length) [SUBSTRING](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#substring)(sttring, position, length)|[SUBSTR](https://docs.snowflake.com/en/sql-reference/functions/substr)(string, IFF(position < -LENGTH(string), 1, position)) [SUBSTRING](https://docs.snowflake.com/en/sql-reference/functions/substr)(string, IFF(position < -LENGTH(string), 1, position)) [SUBSTR](https://docs.snowflake.com/en/sql-reference/functions/substr)(sttring, IFF(position < -LENGTH(string), 1, position), length) [SUBSTRING](https://docs.snowflake.com/en/sql-reference/functions/substr)(sttring, IFF(position < -LENGTH(string), 1, position), length)|
|[TO_HEX](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#to_hex)|[HEX_ENCODE](https://docs.snowflake.com/en/sql-reference/functions/hex_encode)|
|[UPPER](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#upper)|[UPPER](https://docs.snowflake.com/en/sql-reference/functions/upper)|

## Timestamp Functions[¶](#timestamp-functions)

<!-- prettier-ignore -->
|BigQuery|Snowflake|
|---|---|
|[CURRENT_TIMESTAMP](https://cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions#current_timestamp) [CURRENT_TIMESTAMP](https://cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions#current_timestamp)()|[CURRENT_TIMESTAMP](https://docs.snowflake.com/en/sql-reference/functions/current_timestamp) [CURRENT_TIMESTAMP](https://docs.snowflake.com/en/sql-reference/functions/current_timestamp)()|
|[SAFE.TIMESTAMP_MILLIS](https://cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions#timestamp_millis)|IFF(expr BETWEEN -62135596800000 AND 253402300799999, TO*TIMESTAMP(expr / 1000), null) \_Notes: Safe version with range validation to prevent overflow errors.*|
|[SAFE.TIMESTAMP_SECONDS](https://cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions#timestamp_seconds)|SAFE*TIMESTAMP_SECONDS_UDF(expr) \_Notes: SnowConvert AI generates a UDF to provide safe timestamp conversion with error handling.*|
|[TIMESTAMP_MILLIS](https://cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions#timestamp_millis)|TO*TIMESTAMP(expr / 1000) \_Notes: Converts milliseconds since epoch to timestamp by dividing by 1000.*|
|[TIMESTAMP_SECONDS](https://cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions#timestamp_seconds)(expr)|DATEADD(‘seconds’, expr, ‘1970-01-01’) _Notes: Adds seconds to Unix epoch start date._|
|[UNIX_MICROS](https://cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions#unix_micros)(timestamp)|DATE*PART(‘epoch_microsecond’, CONVERT_TIMEZONE(‘UTC’, timestamp)) \_Notes: Extracts microseconds since Unix epoch from timestamp converted to UTC.*|
|[UNIX_MILLIS](https://cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions#unix_millis)(timestamp)|DATE*PART(‘epoch_millisecond’, CONVERT_TIMEZONE(‘UTC’, timestamp)) \_Notes: Extracts milliseconds since Unix epoch from timestamp converted to UTC.*|
|[UNIX_SECONDS](https://cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions#unix_seconds)(timestamp)|DATE*PART(‘epoch_seconds’, CONVERT_TIMEZONE(‘UTC’, timestamp)) \_Notes: Extracts seconds since Unix epoch from timestamp converted to UTC.*|

## FORMAT_DATE[¶](#format-date)

Format_date function

### Description[¶](#description)

Formats a `DATE` value according to a specified format string.

For more information, please refer to
[FORMAT_DATE](https://cloud.google.com/bigquery/docs/reference/standard-sql/date_functions#format_date)
function.

### Grammar Syntax[¶](#grammar-syntax)

```
 FORMAT_DATE(format_string, date_expr)
```

#### Sample Source[¶](#sample-source)

##### BigQuery[¶](#bigquery)

```
CREATE TABLE TEST_DATE (col1 DATE);
SELECT FORMAT_DATE('%Y', col1);
```

##### Snowflake[¶](#snowflake)

```
CREATE TABLE TEST_DATE (col1 DATE);
SELECT
  TO_CHAR(col1, 'YYYY')
FROM
  TEST_DATE;
```

#### BigQuery Formats Equivalents[¶](#bigquery-formats-equivalents)

<!-- prettier-ignore -->
|BigQuery|Snowflake|
|---|---|
|%A|PUBLIC.DAYNAME*LONG_UDF(date_expr) \_Note: Generate UDF in conversion for support.*|
|%a|DY|
|%B|MMMM|
|%b|MON|
|%C|PUBLIC.CENTURY*UDF(date_expr) \_Note: Generate UDF in conversion for support.*|
|%c|DY MON DD HH24:MI:SS YYYY|
|%D|MM/DD/YY|
|%d|DD|
|%e|DD|
|%F|YYYY-MM-DD|
|%G|YEAROFWEEKISO(date_expr)|
|%g|PUBLIC.ISO*YEAR_PART_UDF(date_expr, 2) \_Note: Generate UDF in conversion for support.*|
|%H|HH24|
|%h|MON|
|%I|HH12|
|%J|PUBLIC.DAY*OF_YEAR_ISO_UDF(date_expr) \_Note: Generate UDF in conversion for support.*|
|%j|DAYOFYEAR(date_expr)|
|%k|HH24|
|%l|HH12|
|%M|MI|
|%m|MM|
|%n|_Not equivalent format_|
|%P|pm|
|%p|AM|
|%Q|QUARTER(date_expr)|
|%R|HH24:MI|
|%S|SS|
|%s|_Not equivalent format_|
|%T|HH24:MI:SS|
|%t|_Not equivalent format_|
|%U|WEEK(date_expr)|
|%u|DAYOFWEEKISO(date_expr)|
|%V|WEEKISO(date_expr)|
|%W|WEEK(date*expr) \_Note: Unlike BigQuery, Snowflake results are dictated by the values set for the WEEK_OF_YEAR_POLICY and/or WEEK_START session parameters. So, results could differ from BigQuery based on those parameters.*|
|%w|DAYOFWEEK(date*expr) \_Note: Unlike BigQuery, Snowflake results are dictated by the values set for the WEEK_OF_YEAR_POLICY and/or WEEK_START session parameters. So, results could differ from BigQuery based on those parameters.*|
|%X|HH24:MI:SS|
|%x|MM/DD/YY|
|%Y|YYYY|
|%y|YY|
|%Z|_Not equivalent format_|
|%z|_Not equivalent format_|
|%Ez|_Not equivalent format_|
|%E<number>S|_Not equivalent format_|
|%E\*S|_Not equivalent format_|
|%EY4|YYYY|

Warning

In BigQuery, the format related to time is not applied when the type is DATE, but Snowflake applies
the format with values in zero for HH:MI:SS usages.

**Note:**

For more information, please refer to
[BigQuery DateTime formats](https://cloud.google.com/bigquery/docs/reference/standard-sql/format-elements#format_elements_date_time).

## ST_GEOGFROMTEXT[¶](#st-geogfromtext)

Geography Function.

### Description[¶](#id1)

> Returns a `GEOGRAPHY` value that corresponds to the input
> [WKT](https://en.wikipedia.org/wiki/Well-known_text) representation.

For more information, please refer to
[ST_GEOGFROMTEXT](https://cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions#st_geogfromtext)
function.

SuccessPlaceholder

ST_GEOGFROMTEXT function is supported in Snowflake.

### Grammar Syntax[¶](#id2)

```
 ST_GEOGFROMTEXT(wkt_string[, oriented])
```

#### Sample Source[¶](#id3)

The oriented parameter in the ST_GEOGFROMTEXT function is not supported in Snowflake.

##### BigQuery[¶](#id4)

```
 SELECT ST_GEOGFROMTEXT('POINT(-122.35 37.55)');
SELECT ST_GEOGFROMTEXT('POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))', TRUE);
```

##### Snowflake[¶](#id5)

```
 SELECT ST_GEOGFROMTEXT('POINT(-122.35 37.55)');
SELECT
!!!RESOLVE EWI!!! /*** SSC-EWI-BQ0006 - ORIENTED PARAMETER IN THE ST_GEOGFROMTEXT FUNCTION IS NOT SUPPORTED IN SNOWFLAKE. ***/!!!
ST_GEOGFROMTEXT('POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))');
```

Please keep in mind that the default output format for geography data types is **WKT** **(Well-Known
Text)** and in Snowflake **WKB (Well-Known Binary)**. You can use the
[ST_ASWKT](https://docs.snowflake.com/en/sql-reference/functions/st_aswkt) function or set the
[GEOGRAPHY_OUTPUT_FORMAT](https://docs.snowflake.com/en/sql-reference/parameters#geography-output-format)
format if you want to view the data in **WKT** format.

#### Using ST_GEOGFROMTEXT function to insert geography data[¶](#using-st-geogfromtext-function-to-insert-geography-data)

This function is not allowed in the values clause and is not required in Snowflake.

##### BigQuery[¶](#id6)

```
 CREATE OR REPLACE TABLE test.geographyType
(
  COL1 GEOGRAPHY
);

INSERT INTO test.geographyType VALUES
    (ST_GEOGFROMTEXT('POINT(-122.35 37.55)')),
    (ST_GEOGFROMTEXT('LINESTRING(-124.20 42.00, -120.01 41.99)'));
```

##### Snowflake[¶](#id7)

```
 CREATE OR REPLACE TABLE test.geographyType
(
  COL1 GEOGRAPHY
);

INSERT INTO test.geographyType
VALUES
    (
     --** SSC-FDM-BQ0010 - THE FUNCTION 'ST_GEOGFROMTEXT' IS NOT REQUIRED IN SNOWFLAKE. **
     'POINT(-122.35 37.55)'),
    (
     --** SSC-FDM-BQ0010 - THE FUNCTION 'ST_GEOGFROMTEXT' IS NOT REQUIRED IN SNOWFLAKE. **
     'LINESTRING(-124.20 42.00, -120.01 41.99)');
```

### Related EWI’s[¶](#related-ewi-s)

1. [SSC-EWI-BQ0006](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/bigqueryEWI.html#ssc-ewi-bq0006):
   Oriented parameter in the ST_GEOGFROMTEXT function is not supported in Snowflake.
2. [SSC-FDM-BQ0010](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/bigqueryFDM.html#ssc-fdm-bq0010):
   Geography function is not required in Snowflake.

## ST_GEOGPOINT[¶](#st-geogpoint)

Geography Function.

### Description[¶](#id8)

> Creates a `GEOGRAPHY` with a single point. `ST_GEOGPOINT` creates a point from the specified
> `FLOAT64` longitude (in degrees, negative west of the Prime Meridian, positive east) and latitude
> (in degrees, positive north of the Equator, negative south) parameters and returns that point in a
> `GEOGRAPHY` value.

For more information, please refer to
[ST_GEOGPOINT](https://cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions#st_geogpoint)
function.

**Note:**

The function ST_GEOGPOINT is translated to ST_POINT in Snowflake.

### Grammar Syntax[¶](#id9)

```
 ST_GEOGPOINT(longitude, latitude)
```

#### Sample Source[¶](#id10)

##### BigQuery[¶](#id11)

```
 SELECT ST_GEOGPOINT(-122.0838, 37.3860);
```

##### Snowflake[¶](#id12)

```
 SELECT ST_POINT(-122.0838, 37.3860);
```

Please keep in mind that the default output format for geography data types is **WKT** **(Well-Known
Text)** and in Snowflake **WKB (Well-Known Binary)**. You can use the
[ST_ASWKT](https://docs.snowflake.com/en/sql-reference/functions/st_aswkt) function or set the
[GEOGRAPHY_OUTPUT_FORMAT](https://docs.snowflake.com/en/sql-reference/parameters#geography-output-format)
format if you want to view the data in **WKT** format.

#### Using ST_POINT function to insert geography data[¶](#using-st-point-function-to-insert-geography-data)

This function is not allowed in the values clause and is not required in Snowflake.

##### BigQuery[¶](#id13)

```
 CREATE OR REPLACE TABLE test.geographyType
(
  COL1 GEOGRAPHY
);

INSERT INTO test.geographyType
VALUES (ST_GEOGPOINT(-122.0838, 37.3860));
```

##### Snowflake[¶](#id14)

```
 CREATE OR REPLACE TABLE test.geographyType
(
  COL1 GEOGRAPHY
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "bigquery",  "convertedOn": "04/03/2025",  "domain": "test" }}';

INSERT INTO test.geographyType
VALUES (
--** SSC-FDM-BQ0010 - THE FUNCTION 'ST_GEOGFROMTEXT' IS NOT REQUIRED IN SNOWFLAKE. **
'POINT(122.0838 37.3860)');
```

### Related EWI’s[¶](#id15)

1. [SSC-FDM-BQ0010](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/bigqueryFDM.html#ssc-fdm-bq0010):
   Geography function is not required in Snowflake.
