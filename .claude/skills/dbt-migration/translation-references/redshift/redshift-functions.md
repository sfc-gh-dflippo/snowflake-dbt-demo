---
description: Note
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/redshift/redshift-functions
title: SnowConvert AI - Redshift - Built-in functions | Snowflake Documentation
---

## Aggregate Functions[¶](#aggregate-functions)

> Aggregate functions compute a single result value from a set of input values.
> ([Redshift SQL Language Reference Aggregate Functions](https://docs.aws.amazon.com/redshift/latest/dg/c_Aggregate_Functions.html)).

<!-- prettier-ignore -->
|Redshift|Snowflake|
|---|---|---|
|[ANY_VALUE](https://docs.snowflake.com/en/sql-reference/functions/any_value) ( [ DISTINCT|ALL ] expression )|
|[AVG](https://docs.aws.amazon.com/redshift/latest/dg/r_AVG.html) ( [ DISTINCT|ALL ] _expression_ )|[AVG](https://docs.snowflake.com/en/sql-reference/functions/avg) ( [ DISTINCT ] expression) _Notes: Redshift and Snowflake may show different precision/decimals due to data type rounding/formatting._|
|[COUNT](https://docs.aws.amazon.com/redshift/latest/dg/r_COUNT.html)|[COUNT](https://docs.snowflake.com/en/sql-reference/functions/count)|
|[LISTAGG](https://docs.aws.amazon.com/redshift/latest/dg/r_LISTAGG.html)|[LISTAGG](https://docs.snowflake.com/en/sql-reference/functions/listagg) _Notes: Redshift’s DISTINCT ignores trailing spaces (‘a ‘ = ‘a’); Snowflake’s does not. (See_ [SSC-FDM-PG0013](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/postgresql/ssc-fdm-pg0013.md)_)._|
|[MAX](https://docs.aws.amazon.com/redshift/latest/dg/r_MAX.html)|[MAX](https://docs.snowflake.com/en/sql-reference/functions/max)|
|[MEDIAN](https://docs.aws.amazon.com/redshift/latest/dg/r_MEDIAN.html)|[MEDIAN](https://docs.snowflake.com/en/sql-reference/functions/median) _Notes**: Snowflake does not allow the use of date types**, while Redshift does. (See_ [SSC-FDM-PG0013](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/postgresql/ssc-fdm-pg0013.md)_)._|
|[MIN](https://docs.aws.amazon.com/redshift/latest/dg/r_MIN.html)|[MIN](https://docs.snowflake.com/en/sql-reference/functions/min)|
|[PERCENTILE_CONT](https://docs.aws.amazon.com/redshift/latest/dg/r_PERCENTILE_CONT.html)|[PERCENTILE_CONT](https://docs.snowflake.com/en/sql-reference/functions/percentile_cont)|
|[STDDEV/STDDEV_SAMP](https://docs.aws.amazon.com/redshift/latest/dg/r_STDDEV_functions.html) ( [ DISTINCT|ALL ] _expression_) [STDDEV_POP](https://docs.aws.amazon.com/redshift/latest/dg/r_STDDEV_functions.html) ( [ DISTINCT|
|[SUM](https://docs.aws.amazon.com/redshift/latest/dg/r_SUM.html)|[SUM](https://docs.snowflake.com/en/sql-reference/functions/sum)|
|[VARIANCE/VAR_SAMP](https://docs.aws.amazon.com/redshift/latest/dg/r_VARIANCE_functions.html) ( [ DISTINCT|ALL ] _expression_) [VAR_POP](https://docs.aws.amazon.com/redshift/latest/dg/r_VARIANCE_functions.html) ( [ DISTINCT|

## Array Functions[¶](#array-functions)

> Creates an array of the SUPER data type.
> ([Redshift SQL Language Reference Array Functions](https://docs.aws.amazon.com/redshift/latest/dg/c_Array_Functions.html)).

<!-- prettier-ignore -->
|Redshift|Snowflake|
|---|---|---|
|[ARRAY](https://docs.aws.amazon.com/redshift/latest/dg/r_array.html) ( [ expr1 ] [ , expr2 [ , … ] ] )|[ARRAY_CONSTRUCT](https://docs.snowflake.com/en/sql-reference/functions/array_construct) ( [ <expr1> ] [ , <expr2> [ , … ] ] )|
|[ARRAY_CONCAT](https://docs.aws.amazon.com/redshift/latest/dg/r_array_concat.html) ( super_expr1, super_expr2 )|[ARRAY_CAT](https://docs.snowflake.com/en/sql-reference/functions/array_cat) ( <array1> , <array2> )|
|[ARRAY_FLATTEN](https://docs.aws.amazon.com/redshift/latest/dg/array_flatten.html) ( _super_expr1_,_super_expr2_,.. )|[ARRAY_FLATTEN](https://docs.snowflake.com/en/sql-reference/functions/array_flatten) ( <array> ) _Notes: the results may vary between platforms (See_ [SSC-FDM-PG0013](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/postgresql/ssc-fdm-pg0013.md)_)._|
|[GET_ARRAY_LENGTH](https://docs.aws.amazon.com/redshift/latest/dg/get_array_length.html) ( _super_expr_ )|[ARRAY_SIZE](https://docs.snowflake.com/en/sql-reference/functions/array_size) ( <array>|<variant>)|
|[SPLIT_TO_ARRAY](https://docs.aws.amazon.com/redshift/latest/dg/split_to_array.html) ( _string_,_delimiter_ )|[SPLIT](https://docs.snowflake.com/en/sql-reference/functions/split) (<string>, <separator>) _Notes: Redshift allows missing delimiters; Snowflake requires them, defaulting to comma_|
|[SUBARRAY](https://docs.aws.amazon.com/redshift/latest/dg/r_subarray.html) ( _super_expr_, _start_position_, _length_ )|[ARRAY_SLICE](https://docs.snowflake.com/en/sql-reference/functions/array_slice) ( <array> , <from> , <to> ) _Notes: Function names and the second argument differ; adjust arguments for equivalence._|

## Conditional expressions[¶](#conditional-expressions)

<!-- prettier-ignore -->
|Redshift|Snowflake|
|---|---|
|[DECODE](https://docs.aws.amazon.com/redshift/latest/dg/r_DECODE_expression.html)|[DECODE](https://docs.snowflake.com/en/sql-reference/functions/decode) _Notes:_ _the results may vary between platforms (See_ [SSC-FDM-PG0013](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/postgresql/ssc-fdm-pg0013.md)_)._|
|[COALESCE](https://docs.aws.amazon.com/redshift/latest/dg/r_NVL_function.html) ( _expression_, _expression_, … )|[COALESCE](https://docs.snowflake.com/en/sql-reference/functions/coalesce) ( _expression_, _expression_, … )|
|[GREATEST](https://docs.aws.amazon.com/redshift/latest/dg/r_GREATEST_LEAST.html) ( value [, …] )|[GREATEST_IGNORE_NULLS](https://docs.snowflake.com/en/sql-reference/functions/greatest_ignore_nulls) ( <expr1> [, <expr2> … ] )|
|[LEAST](https://docs.aws.amazon.com/redshift/latest/dg/r_GREATEST_LEAST.html) ( value [, …] )|[LEAST_IGNORE_NULLS](https://docs.snowflake.com/en/sql-reference/functions/least_ignore_nulls) ( <expr1> [, <expr2> … ])|
|[NVL](https://docs.aws.amazon.com/redshift/latest/dg/r_NVL_function.html)( _expression_, _expression_, … )|[_NVL_](https://docs.snowflake.com/en/sql-reference/functions/nvl) _( expression, expression )_ _Notes: Redshift’s NVL accepts multiple arguments; Snowflake’s NVL accepts only two. To match Redshift behavior, NVL with more than two arguments is converted to COALESCE._|
|[NVL2](https://docs.aws.amazon.com/redshift/latest/dg/r_NVL2.html)|[NVL2](https://docs.snowflake.com/en/sql-reference/functions/nvl2)|
|[NULLIF](https://docs.aws.amazon.com/redshift/latest/dg/r_NULLIF_function.html)|[NULLIF](https://docs.snowflake.com/en/sql-reference/functions/nullif) _Notes: Redshift’s NULLIF ignores trailing spaces in some string comparisons, unlike Snowflake. Therefore, the transformation adds RTRIM for equivalence._|

## Data type formatting functions[¶](#data-type-formatting-functions)

> Data type formatting functions provide an easy way to convert values from one data type to
> another. For each of these functions, the first argument is always the value to be formatted and
> the second argument contains the template for the new format.
> ([Redshift SQL Language Reference Data type formatting functions](https://docs.aws.amazon.com/redshift/latest/dg/r_Data_type_formatting.html)).

<!-- prettier-ignore -->
|Redshift|Snowflake|
|---|---|
|[TO_CHAR](https://docs.aws.amazon.com/redshift/latest/dg/r_TO_CHAR.html)|[TO_CHAR](https://docs.snowflake.com/en/sql-reference/functions/to_char) _Notes: Snowflake’s support for this function is partial (see_ [_SSC-EWI-0006_](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.md#ssc-ewi-0006)_)._|
|[TO_DATE](https://docs.aws.amazon.com/redshift/latest/dg/r_TO_DATE_function.html)|[TO_DATE](https://docs.snowflake.com/en/sql-reference/functions/to_date) _Notes: Snowflake’s `TO_DATE` fails on invalid dates like ‘20010631’ (June has 30 days), unlike Redshift’s lenient `TO_DATE`. Use `TRY_TO_DATE` in Snowflake to handle these cases by returning NULL. (see_ [_SSC-FDM-RS0004_](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/redshift/ssc-fdm-rs0004.md)_,_ [_SSC-EWI-0006_](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.md#ssc-ewi-0006)_,_ [_SSC-FDM-0032_](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/general/ssc-fdm-0032.md)_)._|

## Date and time functions[¶](#date-and-time-functions)

<!-- prettier-ignore -->
|Redshift|Snowflake|
|---|---|---|---|---|
|[ADD_MONTHS](https://docs.aws.amazon.com/redshift/latest/dg/r_ADD_MONTHS.html)|[ADD_MONTHS](https://docs.snowflake.com/en/sql-reference/functions/add_months) _Notes:_ _the results may vary between platforms (See_ [SSC-FDM-PG0013](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/postgresql/ssc-fdm-pg0013.md)_)._|
|[AT TIME ZONE ‘timezone’](https://docs.aws.amazon.com/redshift/latest/dg/r_AT_TIME_ZONE.html)|[CONVERT_TIMEZONE](https://docs.snowflake.com/en/sql-reference/functions/convert_timezone) ( <source*tz> , <target_tz> , <source_timestamp_ntz> ) [CONVERT_TIMEZONE](https://docs.snowflake.com/en/sql-reference/functions/convert_timezone) ( <target_tz> , <source_timestamp> ) \_Notes: Redshift defaults to UTC; the Snowflake function requires explicit UTC specification. Therefore, it will be added as the target timezone.*|
|[CONVERT_TIMEZONE](https://docs.aws.amazon.com/redshift/latest/dg/CONVERT_TIMEZONE.html)|[CONVERT_TIMEZONE](https://docs.snowflake.com/en/sql-reference/functions/convert_timezone)|
|[CURRENT_DATE](https://docs.aws.amazon.com/redshift/latest/dg/r_CURRENT_DATE_function.html)|[CURRENT_DATE()](https://docs.snowflake.com/en/sql-reference/functions/current_date)|
|[DATE](https://docs.aws.amazon.com/redshift/latest/dg/r_TO_DATE_function.html)|[DATE](https://docs.snowflake.com/en/sql-reference/functions/to_date)|
|[DATEADD/DATE_ADD](https://docs.aws.amazon.com/redshift/latest/dg/r_DATEADD_function.html) ( _datepart_, _interval_, {_date_|_time_|_timetz_|_timestamp_} )|[DATE_ADD](https://docs.snowflake.com/en/sql-reference/functions/dateadd) ( <date*or_time_part>, <value>, <date_or_time_expr> ) \_Notes: Invalid date part formats are translated to Snowflake-compatible formats.*|
|[DATEDIFF/DATE_DIFF](https://docs.aws.amazon.com/redshift/latest/dg/r_DATEDIFF_function.html)|[DATEDIFF](https://docs.snowflake.com/en/sql-reference/functions/datediff) _Notes: Invalid date part formats are translated to Snowflake-compatible formats._|
|[DATE_PART/PGDATE_PART](https://docs.aws.amazon.com/redshift/latest/dg/r_DATE_PART_function.html)|[DATE_PART](https://docs.snowflake.com/en/sql-reference/functions/date_part) _Notes: this function is partially supported by Snowflake. (See_ [_SSC-EWI-OOO6_](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.md#ssc-ewi-0006)_)._|
|[DATE_PART_YEAR](https://docs.aws.amazon.com/redshift/latest/dg/r_DATE_PART_YEAR.html) (_date_)|[YEAR](https://docs.snowflake.com/en/sql-reference/functions/year) ( <date*or_timestamp_expr> ) \_Notes:* _the results may vary between platforms (See_ [SSC-FDM-PG0013](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/postgresql/ssc-fdm-pg0013.md)_)._|
|[DATE_TRUNC](https://docs.aws.amazon.com/redshift/latest/dg/r_DATE_TRUNC.html)|[DATE_TRUNC](https://docs.snowflake.com/en/sql-reference/functions/date_trunc) _Notes: Invalid date part formats are translated to Snowflake-compatible formats._|
|[GETDATE](https://docs.aws.amazon.com/redshift/latest/dg/r_GETDATE.html)()|[GETDATE](https://docs.snowflake.com/en/sql-reference/functions/getdate)()|
|[LAST_DAY](https://docs.aws.amazon.com/redshift/latest/dg/r_LAST_DAY.html)|[LAST_DAY](https://docs.snowflake.com/en/sql-reference/functions/last_day) _Notes:_ _the results may vary between platforms (See_ [SSC-FDM-PG0013](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/postgresql/ssc-fdm-pg0013.md)_)._|
|[NEXT_DAY](https://docs.aws.amazon.com/redshift/latest/dg/r_NEXT_DAY.html)|[NEXT_DAY](https://docs.snowflake.com/en/sql-reference/functions/next_day) _Notes:_ _the results may vary between platforms (See_ [SSC-FDM-PG0013](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/postgresql/ssc-fdm-pg0013.md)_)._|
|[SYSDATE](https://docs.aws.amazon.com/redshift/latest/dg/r_SYSDATE.html)|[SYSDATE](https://docs.snowflake.com/en/sql-reference/functions/sysdate)()|
|[TIMESTAMP](https://docs.aws.amazon.com/redshift/latest/dg/r_TO_TIMESTAMP.html)|[TO_TIMESTAMP](https://docs.snowflake.com/en/sql-reference/functions/to_timestamp)|
|[TRUNC](https://docs.aws.amazon.com/redshift/latest/dg/r_TRUNC_date.html)|[TRUNC](https://docs.snowflakhttps/docs.snowflake.com/en/sql-reference/functions/trunc2e.com/en/sql-reference/functions/trunc2)|
|[EXTRACT](https://docs.aws.amazon.com/redshift/latest/dg/r_EXTRACT_function.html)|[EXTRACT](https://docs.snowflake.com/en/sql-reference/functions/extract) _Notes:_ Part-time or Date time supported: DAY, DOW, DOY, EPOCH, HOUR, MINUTE, MONTH, QUARTER, SECOND, WEEK, YEAR.|

**Note:**

Redshift timestamps default to microsecond precision (6 digits); Snowflake defaults to nanosecond
precision (9 digits). Adjust precision as needed using ALTER SESSION (e.g.,
`ALTER SESSION SET TIMESTAMP_OUTPUT_FORMAT = 'YYYY-MM-DD HH24:MI:SS.FF2';`). Precision loss may
occur depending on the data type used.

Since some formats are incompatible with Snowflake, adjusting the account parameters
[DATE_INPUT_FORMAT or TIME_INPUT_FORMAT](https://docs.snowflake.com/en/sql-reference/date-time-input-output#data-loading)
might maintain functional equivalence between platforms.

## Hash Functions[¶](#hash-functions)

> A hash function is a mathematical function that converts a numerical input value into another
> value.
> ([Redshift SQL Language Reference Hash functions](https://docs.aws.amazon.com/redshift/latest/dg/hash-functions.html)).

<!-- prettier-ignore -->
|Redshift|Snowflake|
|---|---|
|[FNV_HASH](https://docs.aws.amazon.com/redshift/latest/dg/r_FNV_HASH.html) (value [, seed])|[_HASH_](https://docs.snowflake.com/en/sql-reference/functions/hash) _( <expr> [ , <expr> … ]_|

## JSON Functions[¶](#json-functions)

<!-- prettier-ignore -->
|Redshift|Snowflake|
|---|---|
|[JSON_EXTRACT_PATH_TEXT](https://docs.aws.amazon.com/redshift/latest/dg/JSON_EXTRACT_PATH_TEXT.html)|[JSON_EXTRACT_PATH_TEXT](https://docs.snowflake.com/en/sql-reference/functions/json_extract_path_text) _Notes:_ 1. _Redshift treats newline, tab, and carriage return characters literally; Snowflake interprets them._ 2. _A JSON literal and dot-separated path are required to access nested objects in the Snowflake function._ 3. _Paths with spaces in variables must be quoted._|

## Math functions[¶](#math-functions)

<!-- prettier-ignore -->
|Redshift|Snowflake|
|---|---|
|[ACOS](https://docs.aws.amazon.com/redshift/latest/dg/r_ACOS.html)|[ACOS](https://docs.snowflake.com/en/sql-reference/functions/acos)|
|[ASIN](https://docs.aws.amazon.com/redshift/latest/dg/r_ASIN.html)|[ASIN](https://docs.snowflake.com/en/sql-reference/functions/asin)|
|[ATAN](https://docs.aws.amazon.com/redshift/latest/dg/r_ATAN.html)|[ATAN](https://docs.snowflake.com/en/sql-reference/functions/atan)|
|[ATAN2](https://docs.aws.amazon.com/redshift/latest/dg/r_ATAN2.html)|[ATAN2](https://docs.snowflake.com/en/sql-reference/functions/atan2)|
|[CBRT](https://docs.aws.amazon.com/redshift/latest/dg/r_CBRT.html)|[CBRT](https://docs.snowflake.com/en/sql-reference/functions/cbrt)|
|[CEIL/CEILING](https://docs.aws.amazon.com/redshift/latest/dg/r_CEILING_FLOOR.html)|[CEIL](https://docs.snowflake.com/en/sql-reference/functions/ceil)|
|[COS](https://docs.aws.amazon.com/redshift/latest/dg/r_COS.html)|[COS](https://docs.snowflake.com/en/sql-reference/functions/cos)|
|[COT](https://docs.aws.amazon.com/redshift/latest/dg/r_COT.html)|[COT](https://docs.snowflake.com/en/sql-reference/functions/cot)|
|[DEGREES](https://docs.aws.amazon.com/redshift/latest/dg/r_DEGREES.html)|[DEGREES](https://docs.snowflake.com/en/sql-reference/functions/degrees)|
|[DEXP](https://docs.aws.amazon.com/redshift/latest/dg/r_DEXP.html)|[EXP](https://docs.snowflake.com/en/sql-reference/functions/exp)|
|[DLOG1/LN](https://docs.aws.amazon.com/redshift/latest/dg/r_DLOG1.html)|[LN](https://docs.snowflake.com/en/sql-reference/functions/ln)|
|[DLOG10](https://docs.aws.amazon.com/redshift/latest/dg/r_DLOG10.html) (_number_)|[LOG](https://docs.snowflake.com/en/sql-reference/functions/log) (10, _number_)|
|[EXP](https://docs.aws.amazon.com/redshift/latest/dg/r_EXP.html)|[EXP](https://docs.snowflake.com/en/sql-reference/functions/exp)|
|[FLOOR](https://docs.aws.amazon.com/redshift/latest/dg/r_FLOOR.html)|[FLOOR](https://docs.snowflake.com/en/sql-reference/functions/floor)|
|[LOG](https://docs.aws.amazon.com/redshift/latest/dg/r_LOG.html)|[LOG](https://docs.snowflake.com/en/sql-reference/functions/log)|
|[MOD](https://docs.aws.amazon.com/redshift/latest/dg/r_MOD.html)|[MOD](https://docs.snowflake.com/en/sql-reference/functions/mod)|
|[PI](https://docs.aws.amazon.com/redshift/latest/dg/r_PI.html)|[PI](https://docs.snowflake.com/en/sql-reference/functions/pi)|
|[POWER/POW](https://docs.aws.amazon.com/redshift/latest/dg/r_POWER.html)|[POWER/POW](https://docs.snowflake.com/en/sql-reference/functions/pow)|
|[RADIANS](https://docs.aws.amazon.com/redshift/latest/dg/r_RADIANS.html)|[RADIANS](https://docs.snowflake.com/en/sql-reference/functions/radians)|
|[RANDOM](https://docs.aws.amazon.com/redshift/latest/dg/r_RANDOM.html)|[RANDOM](https://docs.snowflake.com/en/sql-reference/functions/random)|
|[ROUND](https://docs.aws.amazon.com/redshift/latest/dg/r_ROUND.html)|[ROUND](https://docs.snowflake.com/en/sql-reference/functions/round)|
|[SIN](https://docs.aws.amazon.com/redshift/latest/dg/r_SIN.html)|[SIN](https://docs.snowflake.com/en/sql-reference/functions/sin)|
|[SIGN](https://docs.aws.amazon.com/redshift/latest/dg/r_SIGN.html)|[SIGN](https://docs.snowflake.com/en/sql-reference/functions/sign)|
|[SQRT](https://docs.aws.amazon.com/redshift/latest/dg/r_SQRT.html)|[SQRT](https://docs.snowflake.com/en/sql-reference/functions/sqrt)|
|[TAN](https://docs.aws.amazon.com/redshift/latest/dg/r_TAN.html)|[TAN](https://docs.snowflake.com/en/sql-reference/functions/tan)|
|[TRUNC](https://docs.aws.amazon.com/redshift/latest/dg/r_TRUNC.html)|[TRUNC](https://docs.snowflake.com/en/sql-reference/functions/trunc)|

**Note:**

Redshift and Snowflake results may differ in scale.

## String functions[¶](#string-functions)

> String functions process and manipulate character strings or expressions that evaluate to
> character strings.
> ([Redshift SQL Language Reference String functions](https://docs.aws.amazon.com/redshift/latest/dg/String_functions_header.html)).

<!-- prettier-ignore -->
|Redshift|Snowflake|
|---|---|
|[ASCII](https://docs.aws.amazon.com/redshift/latest/dg/r_ASCII.html)|[ASCII](https://docs.snowflake.com/en/sql-reference/functions/ascii)|
|[BTRIM](https://docs.aws.amazon.com/redshift/latest/dg/r_BTRIM.html)|[TRIM](https://docs.snowflake.com/en/sql-reference/functions/trim)|
|[CHAR_LENGTH](https://docs.aws.amazon.com/redshift/latest/dg/r_CHAR_LENGTH.html)|[LENGTH](https://docs.snowflake.com/en/sql-reference/functions/length)|
|[CHARACTER_LENGTH](https://docs.aws.amazon.com/redshift/latest/dg/r_CHARACTER_LENGTH.html)|[LENGTH](https://docs.snowflake.com/en/sql-reference/functions/length)|
|[CHARINDEX](https://docs.aws.amazon.com/redshift/latest/dg/r_CHARINDEX.html)|[CHARINDEX](https://docs.snowflake.com/en/sql-reference/functions/charindex)|
|[CHR](https://docs.aws.amazon.com/redshift/latest/dg/r_CHR.html)|[CHR](https://docs.snowflake.com/en/sql-reference/functions/chr)|
|[CONCAT](https://docs.aws.amazon.com/redshift/latest/dg/r_CONCAT.html)|[CONCAT](https://docs.snowflake.com/en/sql-reference/functions/concat)|
|[INITCAP](https://docs.aws.amazon.com/redshift/latest/dg/r_INITCAP.html)|[INITCAP](https://docs.snowflake.com/en/sql-reference/functions/initcap)|
|[LEFT/RIGHT](https://docs.snowflake.com/en/sql-reference/functions/initcap)|[LEFT](https://docs.snowflake.com/en/sql-reference/functions/left)/[RIGHT](https://docs.snowflake.com/en/sql-reference/functions/right) _Notes: For negative lengths in `LEFT`/`RIGHT`, Snowflake returns an empty string; Redshift raises an error._|
|[LEN](https://docs.aws.amazon.com/redshift/latest/dg/r_LEN.html)|[LEN](https://docs.snowflake.com/en/sql-reference/functions/length)|
|[LOWER](https://docs.aws.amazon.com/redshift/latest/dg/r_LOWER.html)|[LOWER](https://docs.snowflake.com/en/sql-reference/functions/lower)|
|[OCTET_LENGTH](https://docs.aws.amazon.com/redshift/latest/dg/r_OCTET_LENGTH.html)|[OCTET_LENGTH](https://docs.snowflake.com/en/sql-reference/functions/octet_length) _Notes:_ _the results may vary between platforms (See_ [SSC-FDM-PG0013](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/postgresql/ssc-fdm-pg0013.md)_)._|
|[QUOTE_IDENT](https://docs.aws.amazon.com/redshift/latest/dg/r_QUOTE_IDENT.html) (_string_)|[CONCAT](https://docs.snowflake.com/en/sql-reference/functions/concat) (‘”’, _string,_ ‘”’)|
|[REGEXP_REPLACE](https://docs.aws.amazon.com/redshift/latest/dg/REGEXP_REPLACE.html)|[REGEXP_REPLACE](https://docs.snowflake.com/en/sql-reference/functions/regexp_replace) _Notes: This function includes a `parameters` argument that enables the user to interpret the pattern using the Perl Compatible Regular Expression (PCRE) dialect, represented by the `p` value, this is removed to avoid any issues_. _(See_ [_SSC-EWI-0009_](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.md#ssc-ewi-0009)_,_ [_SC-FDM-0032_](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/general/ssc-fdm-0032.md)_,_ [_SSC-FDM- PG0011_](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/postgresql/ssc-fdm-pg0011.md)_)._|
|[REPEAT](https://docs.aws.amazon.com/redshift/latest/dg/r_REPEAT.html)|[REPEAT](https://docs.snowflake.com/en/sql-reference/functions/repeat)|
|[REPLACE](https://docs.aws.amazon.com/redshift/latest/dg/r_REPLACE.html)|[REPLACE](https://docs.snowflake.com/en/sql-reference/functions/replace)|
|[REPLICATE](https://docs.aws.amazon.com/redshift/latest/dg/r_REPLICATE.html)|[REPEAT](https://docs.snowflake.com/en/sql-reference/functions/repeat)|
|[REVERSE](https://docs.aws.amazon.com/redshift/latest/dg/r_REVERSE.html)|[REVERSE](https://docs.snowflake.com/en/sql-reference/functions/reverse)|
|[SOUNDEX](https://docs.aws.amazon.com/redshift/latest/dg/SOUNDEX.html)|[SOUNDEX](https://docs.snowflake.com/en/sql-reference/functions/soundex) _Notes: Certain special characters, the results may vary between platforms (See_ [SSC-FDM-PG0013](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/postgresql/ssc-fdm-pg0013.md)_)._|
|[SPLIT_PART](https://docs.aws.amazon.com/redshift/latest/dg/SPLIT_PART.html)|[SPLIT_PART](https://docs.snowflake.com/en/sql-reference/functions/split_part) _Notes: Snowflake and Redshift handle SPLIT_PART differently with case-insensitive collations._|
|[STRPOS](https://docs.aws.amazon.com/redshift/latest/dg/r_STRPOS.html) (_string_, _substring_ )|[POSITION](https://docs.snowflake.com/en/sql-reference/functions/position) ( <expr1> IN <expr> )|
|[SUBSTRING](https://docs.aws.amazon.com/redshift/latest/dg/r_SUBSTRING.html)|[_SUBSTRING_](https://docs.snowflake.com/en/sql-reference/functions/substr) _Notes:_ Snowflake partially supports this function. Redshift’s `SUBSTRING`, with a non-positive `start_position`, calculates `start_position + number_characters` (returning ‘’ if the result is non-positive). Snowflake’s behavior differs. (See [SSC-EWI-RS0006](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/redshift/ssc-ewi-rs0006.md)).|
|[TEXTLEN](https://docs.aws.amazon.com/redshift/latest/dg/r_TEXTLEN.html)|[LENGTH](https://docs.snowflake.com/en/sql-reference/functions/length)|
|[TRANSLATE](https://docs.aws.amazon.com/redshift/latest/dg/r_TRANSLATE.html)|[TRANSLATE](https://docs.snowflake.com/en/sql-reference/functions/translate)|
|[TRIM](https://docs.aws.amazon.com/redshift/latest/dg/r_TRIM.html)|[_TRIM_](https://docs.snowflake.com/en/sql-reference/functions/trim) _Notes: Redshift uses keywords (BOTH, LEADING, TRAILING) for trim; Snowflake uses TRIM, LTRIM, RTRIM._|
|[UPPER](https://docs.aws.amazon.com/redshift/latest/dg/r_UPPER.html)|[UPPER](https://docs.snowflake.com/en/sql-reference/functions/upper)|

## SUPER type information functions[¶](#super-type-information-functions)

<!-- prettier-ignore -->
|Redshift|Snowflake|
|---|---|
|[IS_ARRAY](https://docs.aws.amazon.com/redshift/latest/dg/r_is_array.html)|[IS_ARRAY](https://docs.snowflake.com/en/sql-reference/functions/is_array) _Notes:_ _the results may vary between platforms (See_ [SSC-FDM-PG0013](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/postgresql/ssc-fdm-pg0013.md)_)._|
|[IS_BOOLEAN](https://docs.aws.amazon.com/redshift/latest/dg/r_is_boolean.html)|[IS_BOOLEAN](https://docs.snowflake.com/en/sql-reference/functions/is_boolean) _Notes:_ _the results may vary between platforms (See_ [SSC-FDM-PG0013](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/postgresql/ssc-fdm-pg0013.md)_)._|

## Window functions[¶](#window-functions)

<!-- prettier-ignore -->
|Redshift|Snowflake|
|---|---|
|[AVG](https://docs.aws.amazon.com/redshift/latest/dg/r_WF_AVG.html)|[_AVG_](https://docs.snowflake.com/en/sql-reference/functions/avg) _Notes: AVG rounding/formatting can vary by data type between Redshift and Snowflake._|
|[COUNT](https://docs.aws.amazon.com/redshift/latest/dg/r_WF_COUNT.html)|[COUNT](https://docs.snowflake.com/en/sql-reference/functions/count)|
|[DENSE_RANK](https://docs.aws.amazon.com/redshift/latest/dg/r_WF_DENSE_RANK.html)|[DENSE_RANK](https://docs.snowflake.com/en/sql-reference/functions/dense_rank) _Notes: ORDER BY is mandatory in Snowflake; missing clauses are replaced with `ORDER BY 1`._|
|[FIRST_VALUE](https://docs.aws.amazon.com/redshift/latest/dg/r_WF_first_value.html)|[FIRST_VALUE](https://docs.snowflake.com/en/sql-reference/functions/first_value) _Notes: Snowflake needs ORDER BY; missing clauses get `ORDER BY <expr>.`_|
|[LAG](https://docs.aws.amazon.com/redshift/latest/dg/r_WF_LAG.html)|[LAG](https://docs.snowflake.com/en/sql-reference/functions/lag)|
|[LAST_VALUE](https://docs.aws.amazon.com/redshift/latest/dg/r_WF_last_value.html)|[LAST_VALUE](https://docs.snowflake.com/en/sql-reference/functions/last_value) _Notes: Snowflake needs ORDER BY; missing clauses get `ORDER BY <expr>`._|
|[LEAD](https://docs.aws.amazon.com/redshift/latest/dg/r_WF_LEAD.html)|[LEAD](https://docs.snowflake.com/en/sql-reference/functions/lead) *Notes: Redshift allows constant or expression offsets; Snowflake allows only constant offset*s.|
|[LISTAGG](https://docs.aws.amazon.com/redshift/latest/dg/r_WF_LISTAGG.html)|[LISTAGG](https://docs.snowflake.com/en/sql-reference/functions/listagg) _Notes: Redshift’s DISTINCT ignores trailing spaces (‘a ‘ = ‘a’); Snowflake’s does not. (See_ [SSC-FDM-PG0013](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/postgresql/ssc-fdm-pg0013.md)_)._|
|[MEDIAN](https://docs.aws.amazon.com/redshift/latest/dg/r_WF_MEDIAN.html)|[MEDIAN](https://docs.snowflake.com/en/sql-reference/functions/median) _Notes**: Snowflake does not allow the use of date types**, while Redshift does. (See_ [SSC-FDM-PG0013](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/postgresql/ssc-fdm-pg0013.md)_)._|
|[NTH_VALUE](https://docs.aws.amazon.com/redshift/latest/dg/r_WF_NTH.html)|[NTH_VALUE](https://docs.snowflake.com/en/sql-reference/functions/nth_value) _Notes: ORDER BY is mandatory in Snowflake; missing clauses are replaced with `ORDER BY 1`._|
|[NTILE](https://docs.aws.amazon.com/redshift/latest/dg/r_WF_NTILE.html)|[NTILE](https://docs.snowflake.com/en/sql-reference/functions/ntile) _Notes: ORDER BY is mandatory in Snowflake; missing clauses are replaced with `ORDER BY 1`. (See_ [SSC-FDM-PG0013](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/postgresql/ssc-fdm-pg0013.md)_)._|
|[PERCENT_RANK](https://docs.aws.amazon.com/redshift/latest/dg/r_WF_PERCENT_RANK.html)|[PERCENT_RANK](https://docs.snowflake.com/en/sql-reference/functions/percent_rank) _Notes: ORDER BY is mandatory in Snowflake; missing clauses are replaced with `ORDER BY 1`._|
|[PERCENTILE_CONT](https://docs.aws.amazon.com/redshift/latest/dg/r_WF_PERCENTILE_CONT.html)|[PERCENTILE_CONT](https://docs.snowflake.com/en/sql-reference/functions/percentile_cont) _Notes: Rounding varies between platforms._|
|[PERCENTILE_DISC](https://docs.aws.amazon.com/redshift/latest/dg/r_WF_PERCENTILE_DISC.html)|[PERCENTILE_DISC](https://docs.snowflake.com/en/sql-reference/functions/percentile_disc)|
|[RANK](https://docs.aws.amazon.com/redshift/latest/dg/r_WF_RANK.html)|[RANK](https://docs.snowflake.com/en/sql-reference/functions/rank)|
|[RATIO_TO_REPORT](https://docs.aws.amazon.com/redshift/latest/dg/r_WF_RATIO_TO_REPORT.html)|[RATIO_TO_REPORT](https://docs.snowflake.com/en/sql-reference/functions/ratio_to_report) _Notes:_ _the results may vary between platforms (See_ [SSC-FDM-PG0013](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/postgresql/ssc-fdm-pg0013.md)_)._|
|[ROW_NUMBER](https://docs.aws.amazon.com/redshift/latest/dg/r_WF_ROW_NUMBER.html)|[ROW_NUMBER](https://docs.snowflake.com/en/sql-reference/functions/row_number) N*otes: ORDER BY is mandatory in Snowflake; missing clauses are replaced with `ORDER BY 1`.*|
|[STDDEV_SAMP](https://docs.aws.amazon.com/redshift/latest/dg/r_WF_STDDEV.html)|STDDEV|
|[VAR_SAMP](https://docs.aws.amazon.com/redshift/latest/dg/r_WF_VARIANCE.html)|VARIANCE|

## Known Issues [¶](#known-issues)

1. For more information about quoted identifiers in functions, click
   [here](redshift-basic-elements.html#quoted-identifiers-in-functions).

## Related EWIs[¶](#related-ewis)

- [SSC-EWI-0006](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0006):
  Date or time format is not supported in Snowflake.
- [SSC-FDM-0032](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0032):
  Parameter is not a literal value, transformation could not be fully applied
- [SSC-FDM-RS0004](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/redshiftFDM.html#ssc-fdm-rs0004):
  Invalid dates will cause errors in Snowflake.
- [SSC-FDM-PG0013](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/postgresqlFDM.html#ssc-fdm-pg0013):
  Function syntactically supported by Snowflake but may have functional differences.

## IDENTITY[¶](#identity)

### Description [¶](#description)

The IDENTITY function is a system function that operates on a specified column of a table to
determine the initial value for the identity. If the initial value is not available, it defaults to
the value provided in the function. This will be translation to a Sequence in Snowflake.

### Grammar Syntax [¶](#grammar-syntax)

```
 "identity"(oid_id, oid_table_id, default)
```

**Note:**

This function is no longer supported in Redshift. It uses the default value to define the identity
and behaves like a standard identity column.

### Sample Source Patterns[¶](#sample-source-patterns)

#### Input Code:[¶](#input-code)

##### Redshift[¶](#redshift)

```
 CREATE TABLE IF NOT EXISTS table_test
(
    id integer,
    inventory_combo BIGINT  DEFAULT "identity"(850178, 0, '5,3'::text)
);

INSERT INTO table_test (id) VALUES
    (1),
    (2),
    (3),
    (4);

SELECT * FROM table_test;
```

##### Results[¶](#results)

<!-- prettier-ignore -->
|id|inventory_combo|
|---|---|
|1|5|
|2|8|
|3|11|
|3|14|

**Output Code:**

##### Snowflake[¶](#snowflake)

```
 CREATE TABLE IF NOT EXISTS table_test
(
    id integer,
    inventory_combo BIGINT IDENTITY(5,3) ORDER
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "11/13/2024",  "domain": "test" }}';

INSERT INTO table_test (id) VALUES
    (1),
    (2),
    (3),
    (4);

SELECT * FROM
    table_test;
```

##### Results[¶](#id1)

<!-- prettier-ignore -->
|id|inventory_combo|
|---|---|
|1|5|
|2|8|
|3|11|
|3|14|

### Related EWIs[¶](#id2)

There are no known issues.

## TO_CHAR[¶](#to-char)

Date function

## Description[¶](#id3)

> TO_CHAR converts a timestamp or numeric expression to a character-string data format.
> ([Redshift SQL Language Reference TO_CHAR function](https://docs.aws.amazon.com/redshift/latest/dg/r_TO_CHAR.html))

Warning

This function is partially supported in
[Snowflake](https://docs.snowflake.com/en/sql-reference/functions/to_char).

For more information about quoted identifiers in functions,
[click here](redshift-basic-elements.html#quoted-identifiers-in-functions).

## Grammar Syntax[¶](#id4)

```
 TO_CHAR(timestamp_expression | numeric_expression , 'format')
```

## Sample Source Patterns[¶](#id5)

### Input Code:[¶](#id6)

#### Redshift[¶](#id7)

```
 SELECT TO_CHAR(timestamp '2009-12-31 23:15:59', 'YYYY'),
       TO_CHAR(timestamp '2009-12-31 23:15:59', 'YYY'),
       TO_CHAR(timestamp '2009-12-31 23:15:59', 'TH'),
       "to_char"(timestamp '2009-12-31 23:15:59', 'MON-DY-DD-YYYY HH12:MIPM'),
       TO_CHAR(125.8, '999.99'),
       "to_char"(125.8, '999.99');
```

##### Results[¶](#id8)

<!-- prettier-ignore -->
|TO_CHAR|TO_CHAR|TO_CHAR|TO_CHAR|TO_CHAR|
|---|---|---|---|---|
|2009|009|DEC-THU-31-2009 11:15PM|125.80|125.80|

#### Output Code:[¶](#output-code)

##### Snowflake[¶](#id9)

```
 SELECT
       TO_CHAR(timestamp '2009-12-31 23:15:59', 'YYYY'),
       PUBLIC.YEAR_PART_UDF(timestamp '2009-12-31 23:15:59', 3),
       TO_CHAR(timestamp '2009-12-31 23:15:59', 'TH') !!!RESOLVE EWI!!! /*** SSC-EWI-0006 - TH FORMAT MAY FAIL OR MAY HAVE A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/!!!,
       PUBLIC.MONTH_SHORT_UDF(timestamp '2009-12-31 23:15:59', 'uppercase') || '-' || PUBLIC.DAYNAME_SHORT_UDF(timestamp '2009-12-31 23:15:59', 'uppercase') || TO_CHAR(timestamp '2009-12-31 23:15:59', '-DD-YYYY HH12:MI') || PUBLIC.MERIDIAN_INDICATORS_UDF(timestamp '2009-12-31 23:15:59', 'uppercase'),
       TO_CHAR(125.8, '999.99'),
       TO_CHAR(125.8, '999.99');
```

##### Results[¶](#id10)

<!-- prettier-ignore -->
|TO_CHAR|TO_CHAR|
|---|---|
|2009|Dec-Thu-31-2009 11:15PM|

## Known Issues [¶](#id11)

No issues were found.

## Related EWIs[¶](#id12)

- [SSC-EWI-0006](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0006):
  The current date/numeric format may have a different behavior in Snowflake.

## For datetime values[¶](#for-datetime-values)

Translation specification for the TO_CHAR function when transforming date or timestamp values to
string

### Description[¶](#id13)

> The following format strings apply to functions such as TO_CHAR. These strings can contain
> datetime separators (such as ‘`-`’, ‘`/`’, or ‘`:`’) and the following “dateparts” and
> “timeparts”.
> ([Redshift Datetime format strings reference page](https://docs.aws.amazon.com/redshift/latest/dg/r_FORMAT_strings.html))

### Grammar Syntax[¶](#id14)

```
TO_CHAR (timestamp_expression, 'format')
```

The following table specifies the mapping of each format element to Snowflake:

<!-- prettier-ignore -->
|Redshift|Snowflake|
|---|---|
|`BC, AD, bc, ad` (upper and lowercase era indicators)|`PUBLIC.ERA_INDICATORS_UDF`|
|`B.C,. A.D., b.c., a.d.` (upper and lowercase era indicators with points)|`PUBLIC.ERA_INDICATORS_WITH_POINTS_UDF`|
|`CC`|`PUBLIC.CENTURY_UDF`|
|`YYYY` and `YY`|Directly supported|
|`YYY` and `Y`|`PUBLIC.YEAR_PART_UDF`|
|`Y,YYY`|`PUBLIC.YEAR_WITH_COMMA_UDF`|
|`IYYY`|`YEAROFWEEKISO`|
|`I, IY, IYY`|`PUBLIC.ISO_YEAR_PART_UDF`|
|`Q`|`QUARTER`|
|`MONTH, Month, month`|`PUBLIC.FULL_MONTH_NAME_UDF`|
|`MON, Mon, mon`|`PUBLIC.MONTH_SHORT_UDF`|
|`RM, rm`|`PUBLIC.ROMAN_NUMERALS_MONTH_UDF`|
|`W`|`PUBLIC.WEEK_OF_MONTH_UDF`|
|`WW`|`PUBLIC.WEEK_NUMBER_UDF`|
|`IW`|`WEEKISO`|
|`DAY, Day, day`|`PUBLIC.DAYNAME_LONG_UDF`|
|`DY, Dy, dy`|`PUBLIC.DAYNAME_SHORT_UDF`|
|`DDD`|`DAYOFYEAR`|
|`IDDD`|`PUBLIC.DAY_OF_YEAR_ISO_UDF`|
|`D`|`PUBLIC.DAY_OF_WEEK_UDF` _Notes: For this UDF to work correctly the Snowflake session parameter `WEEK_START` should have its default value (`0`)._|
|`ID`|`DAYOFWEEKISO`|
|`J`|`PUBLIC.JULIAN_DAY_UDF`|
|`HH24`|Directly supported|
|`HH`|`HH12`|
|`HH12`|Directly supported|
|`MI`|Directly supported|
|`SS`|Directly supported|
|`MS`|`FF3`|
|`US`|`FF6`|
|`AM, PM, am, pm` (upper and lowercase meridian indicators)|`PUBLIC.MERIDIAN_INDICATORS_UDF`|
|`A.M., P.M., a.m., p.m.` (upper and lowercase meridian indicators with points)|`PUBLIC.MERIDIAN_INDICATORS_WITH_POINTS_UDF`|
|`TZ` and `tz`|`UTC` and `utc` _Notes: According to the_ [_redshift documentation_](https://docs.aws.amazon.com/redshift/latest/dg/r_Datetime_types.html#r_Datetime_types-timestamptz)_, all timestamp with time zone are stored in UTC, which causes this format element to return a fixed result._|
|`OF`|+00 _Notes: According to the_ [_redshift documentation_](https://docs.aws.amazon.com/redshift/latest/dg/r_Datetime_types.html#r_Datetime_types-timestamptz)_, all timestamp with time zone are stored in UTC, which causes this format element to return a fixed result._|
|`SSSS`|`PUBLIC.SECONDS_PAST_MIDNIGHT`|
|`SP`|_Notes: This is a PostgreSQL template pattern modifier for “spell mode”, however it does nothing on Redshift, so it is removed from the output._|
|`FX`|_Notes: This is another template pattern modifier for “fixed format”, however it has no use on the TO_CHAR function so it is removed._|

### Sample Source Patterns[¶](#id15)

#### Direct format elements transformation (no functions/UDFs)[¶](#direct-format-elements-transformation-no-functions-udfs)

The result is preserved as a single TO_CHAR function

##### _Redshift_[¶](#id16)

##### Query[¶](#query)

```
 SELECT TO_CHAR('2013-10-03 13:50:15.456871'::TIMESTAMP, 'DD/MM/YY HH:MI:SS.MS') AS col1;
```

##### Result[¶](#result)

```
+----------------------+
<!-- prettier-ignore -->
|col1|
+----------------------+
<!-- prettier-ignore -->
|03/10/13 01:50:15.456|
+----------------------+
```

##### _Snowflake_[¶](#id17)

##### Query[¶](#id18)

```
 SELECT TO_CHAR('2013-10-03 13:50:15.456871'::TIMESTAMP, 'DD/MM/YY HH12:MI:SS.FF3') AS col1;
```

##### Result[¶](#id19)

```
+----------------------+
<!-- prettier-ignore -->
|col1|
+----------------------+
<!-- prettier-ignore -->
|03/10/13 01:50:15.456|
+----------------------+
```

#### Format transformation using functions/UDFs[¶](#format-transformation-using-functions-udfs)

The result is a concatenation of multiple TO_CHAR, UDFs and Snowflake built-in functions that
generate the equivalent string representation of the datetime value

##### _Redshift_[¶](#id20)

##### Query[¶](#id21)

```
 SELECT TO_CHAR(DATE '2025-07-05', '"Today is " Month DAY DD, "it belongs to the week " IW') AS result;
```

##### Result[¶](#id22)

```
+-------------------------------------------------------------+
<!-- prettier-ignore -->
|result|
+-------------------------------------------------------------+
<!-- prettier-ignore -->
|Today is  July      SATURDAY  05, it belongs to the week  27|
+-------------------------------------------------------------+
```

##### _Snowflake_[¶](#id23)

##### Query[¶](#id24)

```
 SELECT
    'Today is ' ||
    TO_CHAR(DATE '2025-07-05', ' ') ||
    PUBLIC.FULL_MONTH_NAME_UDF(DATE '2025-07-05', 'firstOnly') ||
    ' ' ||
    PUBLIC.DAYNAME_LONG_UDF(DATE '2025-07-05', 'uppercase') ||
    TO_CHAR(DATE '2025-07-05', ' DD, ') ||
    'it belongs to the week ' ||
    TO_CHAR(DATE '2025-07-05', ' ') ||
    WEEKISO(DATE '2025-07-05') AS result;
```

##### Result[¶](#id25)

```
+-------------------------------------------------------------+
<!-- prettier-ignore -->
|result|
+-------------------------------------------------------------+
<!-- prettier-ignore -->
|Today is  July      SATURDAY  05, it belongs to the week  27|
+-------------------------------------------------------------+
```

#### Quoted text[¶](#quoted-text)

Format elements in double quoted text are added to the output directly without interpreting them,
escaped double quotes are transformed to their Snowflake escaped equivalent.

##### _Redshift_[¶](#id26)

##### Query[¶](#id27)

```
 SELECT
    TO_CHAR(DATE '2025-01-16', 'MM "TESTING DD" DD') AS result1,
    TO_CHAR(DATE '2025-01-16', 'MM TESTING \\"DD\\" DD') AS result2,
    TO_CHAR(DATE '2025-01-16', 'MM "TESTING \\"DD\\"" DD') AS result3;
```

##### Result[¶](#id28)

```
+-----------------+-------------------+-------------------+
<!-- prettier-ignore -->
|result1|result2|result3|
+-----------------+-------------------+-------------------+
<!-- prettier-ignore -->
|01 TESTING DD 16|01 TEST5NG "16" 16|01 TESTING "DD" 16|
+-----------------+-------------------+-------------------+
```

##### _Snowflake_[¶](#id29)

##### Query[¶](#id30)

```
 SELECT
    TO_CHAR(DATE '2025-01-16', 'MM ') || 'TESTING DD' || TO_CHAR(DATE '2025-01-16', ' DD') AS result1,
    TO_CHAR(DATE '2025-01-16', 'MM TEST') || PUBLIC.ISO_YEAR_PART_UDF(DATE '2025-01-16', 1) || TO_CHAR(DATE '2025-01-16', 'NG ""DD"" DD') AS result2,
    TO_CHAR(DATE '2025-01-16', 'MM ') || 'TESTING "DD"' || TO_CHAR(DATE '2025-01-16', ' DD') AS result3;
```

##### Result[¶](#id31)

```
+-----------------+-------------------+-------------------+
<!-- prettier-ignore -->
|result1|result2|result3|
+-----------------+-------------------+-------------------+
<!-- prettier-ignore -->
|01 TESTING DD 16|01 TEST5NG "16" 16|01 TESTING "DD" 16|
+-----------------+-------------------+-------------------+
```

### Known Issues[¶](#id32)

#### Template pattern modifiers not supported[¶](#template-pattern-modifiers-not-supported)

The following format template modifiers:

- FM (fill mode)
- TH and th (uppercase and lowercase ordinal number suffix)
- TM (translation mode)

Are not supported, including them in a format will generate
[SSC-EWI-0006](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0006)

Input code:

```
 SELECT TO_CHAR(CURRENT_DATE, 'FMMonth'),
TO_CHAR(CURRENT_DATE, 'DDTH'),
TO_CHAR(CURRENT_DATE, 'DDth'),
TO_CHAR(CURRENT_DATE, 'TMMonth');
```

Output code:

```
 SELECT
TO_CHAR(CURRENT_DATE(), 'FM') || PUBLIC.FULL_MONTH_NAME_UDF(CURRENT_DATE(), 'firstOnly') !!!RESOLVE EWI!!! /*** SSC-EWI-0006 - FMMonth FORMAT MAY FAIL OR MAY HAVE A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/!!!,
TO_CHAR(CURRENT_DATE(), 'DDTH') !!!RESOLVE EWI!!! /*** SSC-EWI-0006 - DDTH FORMAT MAY FAIL OR MAY HAVE A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/!!!,
TO_CHAR(CURRENT_DATE(), 'DDth') !!!RESOLVE EWI!!! /*** SSC-EWI-0006 - DDth FORMAT MAY FAIL OR MAY HAVE A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/!!!,
TO_CHAR(CURRENT_DATE(), 'TM') || PUBLIC.FULL_MONTH_NAME_UDF(CURRENT_DATE(), 'firstOnly') !!!RESOLVE EWI!!! /*** SSC-EWI-0006 - TMMonth FORMAT MAY FAIL OR MAY HAVE A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/!!!;
```

**Format parameter passed through variable**

When the format parameter is passed as a variable instead of a string literal, the transformation of
format elements can not be applied, an FDM will be added to the uses of the function warning about
it.

Input code:

```
 SELECT TO_CHAR(d, 'YYYY/MM/DD'),
TO_CHAR(d, f)
FROM (SELECT TO_DATE('2001-01-01','YYYY-MM-DD') as d, 'DD/MM/YYYY' as f);
```

Output code:

```
 SELECT TO_CHAR(d, 'YYYY/MM/DD'),
--** SSC-FDM-0032 - PARAMETER 'format_string' IS NOT A LITERAL VALUE, TRANSFORMATION COULD NOT BE FULLY APPLIED **
TO_CHAR(d, f)
FROM (SELECT TO_DATE('2001-01-01','YYYY-MM-DD') as d, 'DD/MM/YYYY' as f);
```

### Related EWIs[¶](#id33)

1. [SSC-EWI-0006](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0006):
   The current date/numeric format may have a different behavior in Snowflake.
2. [SSC-FDM-0032](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0032):
   Parameter is not a literal value, transformation could not be fully applied
