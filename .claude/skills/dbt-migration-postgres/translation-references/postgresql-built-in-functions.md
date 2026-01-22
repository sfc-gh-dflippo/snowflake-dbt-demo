---
description: PostgreSQL
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/postgres/postgresql-built-in-functions
title: SnowConvert AI - PostgreSQL - Built-in functions | Snowflake Documentation
---

## Applies to

- PostgreSQL
- Greenplum
- Netezza

### Note

For more information about built-in functions and their Snowflake equivalents, also see
[Common built-in functions](../general/built-in-functions).

## Aggregate Functions

> Aggregate functions compute a single result value from a set of input values.
> ([PostgreSQL Language Reference Aggregate Functions](https://www.postgresql.org/docs/12/functions-aggregate.html)).

<!-- prettier-ignore -->
|PostgreSQL|Snowflake|
|---|---|
|[AVG](https://www.postgresql.org/docs/12/functions-aggregate.html)|[AVG](https://docs.snowflake.com/en/sql-reference/functions/avg) _Notes:_ PostgreSQL _and Snowflake may show different precision/decimals due to data type rounding/formatting._|
|[COUNT](https://www.postgresql.org/docs/12/functions-aggregate.html)|[COUNT](https://docs.snowflake.com/en/sql-reference/functions/count)|
|[MAX](https://www.postgresql.org/docs/12/functions-aggregate.html)|[MAX](https://docs.snowflake.com/en/sql-reference/functions/max)|
|[MEDIAN](https://techdocs.broadcom.com/us/en/vmware-tanzu/data-solutions/tanzu-greenplum/7/greenplum-database/ref_guide-function-summary.html#topic31)|[MEDIAN](https://docs.snowflake.com/en/sql-reference/functions/median) _Notes**: Snowflake does not allow the use of date types**, while_ PostgreSQL _does. (See_ [SSC-FDM-PG0013](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/postgresqlFDM.md#ssc-fdm-pg0013)_)._|
|[MIN](https://www.postgresql.org/docs/12/functions-aggregate.html)|[MIN](https://docs.snowflake.com/en/sql-reference/functions/min)|
|[PERCENTILE_CONT](https://www.postgresql.org/docs/9.4/functions-aggregate.html#FUNCTIONS-ORDEREDSET-TABLE)|[PERCENTILE_CONT](https://docs.snowflake.com/en/sql-reference/functions/percentile_cont)|
|[STDDEV/STDDEV_SAMP](https://www.postgresql.org/docs/12/functions-aggregate.html) (_expression_)|[STDDEV/STDDEV_SAMP](https://docs.snowflake.com/en/sql-reference/functions/stddev) (_expression_)|
|[STDDEV_POP](https://www.postgresql.org/docs/12/functions-aggregate.html) (_expression_)|[STDDEV_POP](https://docs.snowflake.com/en/sql-reference/functions/stddev_pop) (_expression_)|
|[SUM](https://www.postgresql.org/docs/12/functions-aggregate.html)|[SUM](https://docs.snowflake.com/en/sql-reference/functions/sum)|
|[VARIANCE/VAR_SAMP](https://www.postgresql.org/docs/12/functions-aggregate.html) (_expression_)|[VARIANCE/VAR_SAMP](https://docs.snowflake.com/en/sql-reference/functions/variance) (_expression_)|
|[VAR_POP](https://www.postgresql.org/docs/12/functions-aggregate.html) (_expression_)|[VAR_POP](https://docs.snowflake.com/en/sql-reference/functions/variance_pop) (_expression_)|

## Conditional expressions

<!-- prettier-ignore -->
|PostgreSQL|Snowflake|
|---|---|
|[COALESCE](https://www.postgresql.org/docs/12/functions-conditional.html) ( value _[, …]_ )|[COALESCE](https://docs.snowflake.com/en/sql-reference/functions/coalesce) ( _expression_, _expression_, … )|
|[GREATEST](https://www.postgresql.org/docs/12/functions-conditional.html) ( value [, …] )|[GREATEST_IGNORE_NULLS](https://docs.snowflake.com/en/sql-reference/functions/greatest_ignore_nulls) ( ```<expr1>``` [, ```<expr2>``` … ] )|
|[LEAST](https://www.postgresql.org/docs/12/functions-conditional.html) ( value [, …] )|[LEAST_IGNORE_NULLS](https://docs.snowflake.com/en/sql-reference/functions/least_ignore_nulls) ( ```<expr1>``` [, ```<expr2>``` … ])|
|[NULLIF](https://www.postgresql.org/docs/12/functions-conditional.html)|[NULLIF](https://docs.snowflake.com/en/sql-reference/functions/nullif) _Notes: PostgreSQL’s NULLIF ignores trailing spaces in some string comparisons, unlike Snowflake. Therefore, the transformation adds RTRIM for equivalence._|

## Data type formatting functions

> Data type formatting functions provide an easy way to convert values from one data type to
> another. For each of these functions, the first argument is always the value to be formatted and
> the second argument contains the template for the new format.
> ([PostgreSQL Language Reference Data type formatting functions](https://www.postgresql.org/docs/12/functions-formatting.html)).

<!-- prettier-ignore -->
|PostgreSQL|Snowflake|
|---|---|
|[TO_CHAR](https://www.postgresql.org/docs/12/functions-formatting.html)|[TO_CHAR](https://docs.snowflake.com/en/sql-reference/functions/to_char) _Notes: Snowflake’s support for this function is partial (see_ [_SSC-EWI-PG0005_](https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/postgres/broken-reference)_)._|
|[TO_DATE](https://www.postgresql.org/docs/12/functions-formatting.html)|[TO_DATE](https://docs.snowflake.com/en/sql-reference/functions/to_date) _Notes: Snowflake’s `TO_DATE` fails on invalid dates like ‘20010631’ (June has 30 days), unlike_ PostgreSQL’_s lenient `TO_DATE`. Use `TRY_TO_DATE` in Snowflake to handle these cases by returning NULL. (see_ [_SSC-EWI-PG0005_](https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/postgres/broken-reference)_,_ [_SSC-FDM-0032_](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.md#ssc-fdm-0032)_)._|

## Date and time functions

<!-- prettier-ignore -->
|PostgreSQL|Snowflake|
|---|---|
|[AT TIME ZONE ‘timezone’](https://www.postgresql.org/docs/12/functions-datetime.html#FUNCTIONS-DATETIME-ZONECONVERT)|[CONVERT_TIMEZONE](https://docs.snowflake.com/en/sql-reference/functions/convert_timezone) ( <source*tz> , ```<target_tz>``` , ```<source_timestamp_ntz>``` ) [CONVERT_TIMEZONE](https://docs.snowflake.com/en/sql-reference/functions/convert_timezone) ( ```<target_tz>``` , ```<source_timestamp>``` ) \_Notes:* PostgreSQL _defaults to UTC; the Snowflake function requires explicit UTC specification. Therefore, it will be added as the target timezone._|
|[CURRENT_DATE](https://www.postgresql.org/docs/8.2/functions-datetime.html)|[CURRENT_DATE()](https://docs.snowflake.com/en/sql-reference/functions/current_date)|
|[DATE_PART/PGDATE_PART](https://www.postgresql.org/docs/12/functions-datetime.html#FUNCTIONS-DATETIME-EXTRACT)|[DATE_PART](https://docs.snowflake.com/en/sql-reference/functions/date_part) _Notes: this function is partially supported by Snowflake. (See_ [_SSC-EWI-PGOOO5_](https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/postgres/broken-reference)_)._|
|[DATE_TRUNC](https://www.postgresql.org/docs/12/functions-datetime.html#FUNCTIONS-DATETIME-EXTRACT)|[DATE_TRUNC](https://docs.snowflake.com/en/sql-reference/functions/date_trunc) _Notes: Invalid date part formats are translated to Snowflake-compatible formats._|
|[TO_TIMESTAMP](https://www.postgresql.org/docs/12/functions-datetime.html#FUNCTIONS-DATETIME-EXTRACT)|[TO_TIMESTAMP](https://docs.snowflake.com/en/sql-reference/functions/to_timestamp)|
|[EXTRACT](https://www.postgresql.org/docs/current/functions-datetime.html#FUNCTIONS-DATETIME-EXTRACT)|[EXTRACT](https://docs.snowflake.com/en/sql-reference/functions/extract) _Notes:_ Part-time or Date time supported: DAY, DOW, DOY, EPOCH, HOUR, MINUTE, MONTH, QUARTER, SECOND, WEEK, YEAR.|
|[TIMEZONE](https://www.postgresql.org/docs/16/functions-datetime.html#FUNCTIONS-DATETIME-ZONECONVERT)|[CONVERT_TIMEZONE](https://docs.snowflake.com/en/sql-reference/functions/convert_timezone)|

### Note 2

PostgreSQL timestamps default to microsecond precision (6 digits); Snowflake defaults to nanosecond
precision (9 digits). Adjust precision as needed using ALTER SESSION (e.g.,
`ALTER SESSION SET TIMESTAMP_OUTPUT_FORMAT = 'YYYY-MM-DD HH24:MI:SS.FF2';`). Precision loss may
occur depending on the data type used.

Since some formats are incompatible with Snowflake, adjusting the account parameters
[DATE_INPUT_FORMAT or TIME_INPUT_FORMAT](https://docs.snowflake.com/en/sql-reference/date-time-input-output#data-loading)
might maintain functional equivalence between platforms.

## JSON Functions

<!-- prettier-ignore -->
|PostgreSQL|Snowflake|
|---|---|
|[JSON_EXTRACT_PATH_TEXT](https://www.postgresql.org/docs/9.3/functions-json.html)|[JSON_EXTRACT_PATH_TEXT](https://docs.snowflake.com/en/sql-reference/functions/json_extract_path_text) _Notes:_ 1. PostgreSQL _treats newline, tab, and carriage return characters literally; Snowflake interprets them._ 2. _A JSON literal and dot-separated path are required to access nested objects in the Snowflake function._ 3. _Paths with spaces in variables must be quoted._|

## Math functions

<!-- prettier-ignore -->
|PostgreSQL|Snowflake|
|---|---|
|[ACOS](https://www.postgresql.org/docs/12/functions-math.html)|[ACOS](https://docs.snowflake.com/en/sql-reference/functions/acos)|
|[ASIN](https://www.postgresql.org/docs/12/functions-math.html)|[ASIN](https://docs.snowflake.com/en/sql-reference/functions/asin)|
|[ATAN](https://www.postgresql.org/docs/12/functions-math.html)|[ATAN](https://docs.snowflake.com/en/sql-reference/functions/atan)|
|[ATAN2](https://www.postgresql.org/docs/12/functions-math.html)|[ATAN2](https://docs.snowflake.com/en/sql-reference/functions/atan2)|
|[CBRT](https://www.postgresql.org/docs/12/functions-math.html)|[CBRT](https://docs.snowflake.com/en/sql-reference/functions/cbrt)|
|[CEIL/CEILING](https://www.postgresql.org/docs/12/functions-math.html)|[CEIL](https://docs.snowflake.com/en/sql-reference/functions/ceil)|
|[COS](https://www.postgresql.org/docs/12/functions-math.html)|[COS](https://docs.snowflake.com/en/sql-reference/functions/cos)|
|[COT](https://www.postgresql.org/docs/12/functions-math.html)|[COT](https://docs.snowflake.com/en/sql-reference/functions/cot)|
|[DEGREES](https://www.postgresql.org/docs/12/functions-math.html)|[DEGREES](https://docs.snowflake.com/en/sql-reference/functions/degrees)|
|[LN](https://www.postgresql.org/docs/12/functions-math.html)|[LN](https://docs.snowflake.com/en/sql-reference/functions/ln)|
|[EXP](https://www.postgresql.org/docs/12/functions-math.html)|[EXP](https://docs.snowflake.com/en/sql-reference/functions/exp)|
|[FLOOR](https://www.postgresql.org/docs/12/functions-math.html)|[FLOOR](https://docs.snowflake.com/en/sql-reference/functions/floor)|
|[LOG](https://www.postgresql.org/docs/12/functions-math.html)|[LOG](https://docs.snowflake.com/en/sql-reference/functions/log)|
|[MOD](https://www.postgresql.org/docs/12/functions-math.html)|[MOD](https://docs.snowflake.com/en/sql-reference/functions/mod)|
|[PI](https://www.postgresql.org/docs/12/functions-math.html)|[PI](https://docs.snowflake.com/en/sql-reference/functions/pi)|
|[POWER/POW](https://www.postgresql.org/docs/12/functions-math.html)|[POWER/POW](https://docs.snowflake.com/en/sql-reference/functions/pow)|
|[RADIANS](https://www.postgresql.org/docs/12/functions-math.html)|[RADIANS](https://docs.snowflake.com/en/sql-reference/functions/radians)|
|[RANDOM](https://www.postgresql.org/docs/12/functions-math.html)|[RANDOM](https://docs.snowflake.com/en/sql-reference/functions/random)|
|[ROUND](https://www.postgresql.org/docs/12/functions-math.html)|[ROUND](https://docs.snowflake.com/en/sql-reference/functions/round)|
|[SIN](https://www.postgresql.org/docs/12/functions-math.html)|[SIN](https://docs.snowflake.com/en/sql-reference/functions/sin)|
|[SIGN](https://www.postgresql.org/docs/12/functions-math.html)|[SIGN](https://docs.snowflake.com/en/sql-reference/functions/sign)|
|[SQRT](https://www.postgresql.org/docs/12/functions-math.html)|[SQRT](https://docs.snowflake.com/en/sql-reference/functions/sqrt)|
|[TAN](https://www.postgresql.org/docs/12/functions-math.html)|[TAN](https://docs.snowflake.com/en/sql-reference/functions/tan)|
|[TRUNC](https://www.postgresql.org/docs/12/functions-math.html)|[TRUNC](https://docs.snowflake.com/en/sql-reference/functions/trunc)|

### Note 3

PostgreSQL and Snowflake results may differ in scale.

## String functions

> String functions process and manipulate character strings or expressions that evaluate to
> character strings.
> ([PostgreSQL Language Reference String functions](https://www.postgresql.org/docs/12/functions-string.html)).

<!-- prettier-ignore -->
|PostgreSQL|Snowflake|
|---|---|
|[ASCII](https://www.postgresql.org/docs/12/functions-string.html)|[ASCII](https://docs.snowflake.com/en/sql-reference/functions/ascii)|
|[BTRIM](https://www.postgresql.org/docs/12/functions-string.html)|[TRIM](https://docs.snowflake.com/en/sql-reference/functions/trim)|
|[CHAR_LENGTH](https://www.postgresql.org/docs/12/functions-string.html)|[LENGTH](https://docs.snowflake.com/en/sql-reference/functions/length)|
|[CHARACTER_LENGTH](https://www.postgresql.org/docs/12/functions-string.html)|[LENGTH](https://docs.snowflake.com/en/sql-reference/functions/length)|
|[CHR](https://www.postgresql.org/docs/9.1/functions-string.html)|[CHR](https://docs.snowflake.com/en/sql-reference/functions/chr)|
|[CONCAT](https://www.postgresql.org/docs/12/functions-string.html)|[CONCAT](https://docs.snowflake.com/en/sql-reference/functions/concat)|
|[INITCAP](https://www.postgresql.org/docs/12/functions-string.html)|[INITCAP](https://docs.snowflake.com/en/sql-reference/functions/initcap)|
|[LEFT/RIGHT](https://www.postgresql.org/docs/12/functions-string.html)|[LEFT](https://docs.snowflake.com/en/sql-reference/functions/left)/[RIGHT](https://docs.snowflake.com/en/sql-reference/functions/right)|
|[LOWER](https://www.postgresql.org/docs/12/functions-string.html)|[LOWER](https://docs.snowflake.com/en/sql-reference/functions/lower)|
|[OCTET_LENGTH](https://www.postgresql.org/docs/12/functions-string.html)|[OCTET_LENGTH](https://docs.snowflake.com/en/sql-reference/functions/octet_length) _Notes:_ _the results may vary between platforms (See_ [SSC-FDM-PG0013](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/postgresqlFDM.md#ssc-fdm-pg0013)_)._|
|[QUOTE_IDENT](https://www.postgresql.org/docs/12/functions-string.html) (_string_)|[CONCAT](https://docs.snowflake.com/en/sql-reference/functions/concat) (‘”’, _string,_ ‘”’)|
|[REGEXP_REPLACE](https://www.postgresql.org/docs/12/functions-string.html)|[REGEXP_REPLACE](https://docs.snowflake.com/en/sql-reference/functions/regexp_replace) _Notes: This function includes a `parameters` argument that enables the user to interpret the pattern using the Perl Compatible Regular Expression (PCRE) dialect, represented by the `p` value, this is removed to avoid any issues_. _(See_ [_SSC-EWI-0009_](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.md#ssc-ewi-0009)_,_ [_SC-FDM-0032_](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.md#ssc-fdm-0032)_,_ [_SSC-FDM- PG0011_](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/postgresqlFDM.md#ssc-fdm-pg0011)_)._|
|[REPEAT](https://www.postgresql.org/docs/12/functions-string.html)|[REPEAT](https://docs.snowflake.com/en/sql-reference/functions/repeat)|
|[REPLACE](https://www.postgresql.org/docs/12/functions-string.html)|[REPLACE](https://docs.snowflake.com/en/sql-reference/functions/replace)|
|[REVERSE](https://www.postgresql.org/docs/12/functions-string.html)|[REVERSE](https://docs.snowflake.com/en/sql-reference/functions/reverse)|
|[SPLIT_PART](https://www.postgresql.org/docs/12/functions-string.html)|[SPLIT_PART](https://docs.snowflake.com/en/sql-reference/functions/split_part) _Notes: Snowflake and_ PostgreSQL _handle SPLIT_PART differently with case-insensitive collations._|
|[STRPOS](https://www.postgresql.org/docs/12/functions-string.html) (_string_, _substring_ )|[POSITION](https://docs.snowflake.com/en/sql-reference/functions/position) ( ```<expr1>``` IN ```<expr>``` )|
|[SUBSTRING](https://www.postgresql.org/docs/12/functions-string.html)|[_SUBSTRING_](https://docs.snowflake.com/en/sql-reference/functions/substr) _Notes:_ Snowflake partially supports this function. PostgreSQL’s `SUBSTRING`, with a non-positive `start_position`, calculates `start_position + number_characters` (returning ‘’ if the result is non-positive). Snowflake’s behavior differs.|
|[TRANSLATE](https://www.postgresql.org/docs/12/functions-string.html)|[TRANSLATE](https://docs.snowflake.com/en/sql-reference/functions/translate)|
|[TRIM](https://www.postgresql.org/docs/12/functions-string.html)|[_TRIM_](https://docs.snowflake.com/en/sql-reference/functions/trim) _Notes:_ PostgreSQL _uses keywords (BOTH, LEADING, TRAILING) for trim; Snowflake uses TRIM, LTRIM, RTRIM._|
|[UPPER](https://www.postgresql.org/docs/12/functions-string.html)|[UPPER](https://docs.snowflake.com/en/sql-reference/functions/upper)|

## Window functions

<!-- prettier-ignore -->
|PostgreSQL|Snowflake|
|---|---|
|[AVG](https://www.postgresql.org/docs/9.4/functions-aggregate.html)|[_AVG_](https://docs.snowflake.com/en/sql-reference/functions/avg) _Notes: AVG rounding/formatting can vary by data type between_ PostgreSQL _and Snowflake._|
|[COUNT](https://www.postgresql.org/docs/9.4/functions-aggregate.html)|[COUNT](https://docs.snowflake.com/en/sql-reference/functions/count)|
|[DENSE_RANK](https://www.postgresql.org/docs/current/functions-window.html)|[DENSE_RANK](https://docs.snowflake.com/en/sql-reference/functions/dense_rank) _Notes: ORDER BY is mandatory in Snowflake; missing clauses are replaced with `ORDER BY 1`._|
|[FIRST_VALUE](https://www.postgresql.org/docs/current/functions-window.html)|[FIRST_VALUE](https://docs.snowflake.com/en/sql-reference/functions/first_value) _Notes: Snowflake needs ORDER BY; missing clauses get `ORDER BY ```<expr>```.`_|
|[LAG](https://www.postgresql.org/docs/current/functions-window.html)|[LAG](https://docs.snowflake.com/en/sql-reference/functions/lag)|
|[LAST_VALUE](https://www.postgresql.org/docs/current/functions-window.html)|[LAST_VALUE](https://docs.snowflake.com/en/sql-reference/functions/last_value) _Notes: Snowflake needs ORDER BY; missing clauses get `ORDER BY ```<expr>````._|
|[LEAD](https://www.postgresql.org/docs/current/functions-window.html)|[LEAD](https://docs.snowflake.com/en/sql-reference/functions/lead) _Notes:_ PostgreSQL *allows constant or expression offsets; Snowflake allows only constant offset*s.|
|[NTH_VALUE](https://www.postgresql.org/docs/current/functions-window.html)|[NTH_VALUE](https://docs.snowflake.com/en/sql-reference/functions/nth_value) _Notes: ORDER BY is mandatory in Snowflake; missing clauses are replaced with `ORDER BY 1`._|
|[NTILE](https://www.postgresql.org/docs/current/functions-window.html)|[NTILE](https://docs.snowflake.com/en/sql-reference/functions/ntile) _Notes: ORDER BY is mandatory in Snowflake; missing clauses are replaced with `ORDER BY 1`. (See_ [SSC-FDM-PG0013](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/postgresqlFDM.md#ssc-fdm-pg0013)_)._|
|[PERCENT_RANK](https://www.postgresql.org/docs/current/functions-window.html)|[PERCENT_RANK](https://docs.snowflake.com/en/sql-reference/functions/percent_rank) _Notes: ORDER BY is mandatory in Snowflake; missing clauses are replaced with `ORDER BY 1`._|
|[PERCENTILE_CONT](https://www.postgresql.org/docs/9.4/functions-aggregate.html)|[PERCENTILE_CONT](https://docs.snowflake.com/en/sql-reference/functions/percentile_cont) _Notes: Rounding varies between platforms._|
|[PERCENTILE_DISC](https://www.postgresql.org/docs/9.4/functions-aggregate.html)|[PERCENTILE_DISC](https://docs.snowflake.com/en/sql-reference/functions/percentile_disc)|
|[RANK](https://www.postgresql.org/docs/current/functions-window.html)|[RANK](https://docs.snowflake.com/en/sql-reference/functions/rank)|
|[ROW_NUMBER](https://www.postgresql.org/docs/current/functions-window.html)|[ROW_NUMBER](https://docs.snowflake.com/en/sql-reference/functions/row_number) N*otes: ORDER BY is mandatory in Snowflake; missing clauses are replaced with `ORDER BY 1`.*|

## Related EWIs

- [SSC-FDM-0032](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0032):
  Parameter is not a literal value, transformation could not be fully applied
- [SSC-FDM-PG0013](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/postgresqlFDM#ssc-fdm-pg0013):
  Function syntactically supported by Snowflake but may have functional differences.
- [SSC-EWI-0009](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0009):
  Regexp_Substr Function only supports POSIX regular expressions.
- [SSC-FDM- PG0011](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/postgresqlFDM#ssc-fdm-pg0011):
  The use of the COLLATE column constraint has been disabled for this pattern-matching condition.
