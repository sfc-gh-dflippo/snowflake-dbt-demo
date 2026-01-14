---
description:
  This page provides a description of the translation for the built-in functions in Teradata to
  Snowflake
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/teradata/sql-translation-reference/teradata-built-in-functions
title: SnowConvert AI - Teradata - Built-in Functions | Snowflake Documentation
---

## Aggregate Functions[¶](#aggregate-functions)

<!-- prettier-ignore -->
|Teradata|Snowflake|Note|
|---|---|---|
|AVG|AVG||
|CORR|CORR||
|COUNT|COUNT||
|COVAR_POP|COVAR_POP||
|COVAR_SAMP|COVAR_SAMP||
|GROUPING|GROUPING||
|KURTOSIS|KURTOSIS||
|MAXIMUM MAX|MAX||
|MINIMUM MIN|MIN||
|PIVOT|PIVOT|Check [PIVOT.](#pivot)|
|REGR_AVGX|REGR_AVGX||
|REGR_AVGY|REGR_AVGY||
|REGR_COUNT|REGR_COUNT||
|REGR_INTERCEPT|REGR_INTERCEPT||
|REGR_R2|REGR_R2||
|REGR_SLOPE|REGR_SLOPE||
|REGR_SXX|REGR_SXX||
|REGR_SXY|REGR_SXY||
|REGR_SYY|REGR_SYY||
|SKEW|SKEW||
|STDDEV_POP|STDDEV_POP||
|STDDEV_SAMP|STDDEV_SAMP||
|SUM|SUM||
|UNPIVOT|UNPIVOT|Unpivot with multiple functions not supported in Snowflake|
|VAR_POP|VAR_POP||
|VAR_SAMP|VAR_SAMP||

> See
> [Aggregate functions​](https://docs.teradata.com/r/Teradata-VantageTM-SQL-Functions-Expressions-and-Predicates-17.20/Aggregate-Functions)

## Arithmetic, Trigonometric, Hyperbolic Operators/Functions[¶](#arithmetic-trigonometric-hyperbolic-operators-functions)

<!-- prettier-ignore -->
|Teradata|Snowflake|Note|
|---|---|---|
|ABS|ABS||
|CEILING|CEIL||
|DEGREES|DEGREES||
|EXP|EXP||
|FLOOR|FLOOR||
|**_HYPERBOLIC_** ACOSH ASINH ATANH COSH SINH TANH|**_HYPERBOLIC_** ACOSH ASINH ATANH COSH SINH TANH||
|LOG|LOG||
|LN|LN||
|MOD|MOD||
|NULLIFZERO(param)|CASE WHEN param=0 THEN null ELSE param END||
|POWER|POWER||
|RANDOM|RANDOM||
|RADIANS|RADIANS||
|ROUND|ROUND||
|SIGN|SIGN||
|SQRT|SQRT||
|TRUNC|TRUNC_UDF||
|**_TRIGONOMETRIC_** ACOS ASIN ATAN ATAN2 COS SIN TAN|**_TRIGONOMETRIC_** ACOS ASIN ATAN ATAN2 COS SIN TAN||
|ZEROIFNULL|ZEROIFNULL||

> See
> [Arithmetic, Trigonometric, Hyperbolic Operators/Functions](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/Teradata-VantageTM-SQL-Functions-Expressions-and-Predicates-17.20/Arithmetic-Trigonometric-Hyperbolic-Operators/Functions)​

## Attribute Functions[¶](#attribute-functions)

<!-- prettier-ignore -->
|Teradata|Snowflake|Note|
|---|---|---|
|BIT_LENGTH|BIT_LENGTH||
|BYTE BYTES|LENGTH||
|CHAR CHARS CHARACTERS|LEN||
|CHAR_LENGTH CHARACTER_LENGTH|LEN||
|MCHARACTERS|LENGTH||
|OCTECT_LENGTH|OCTECT_LENGTH||

> See
> [Attribute functions](https://docs.teradata.com/r/Teradata-VantageTM-SQL-Functions-Expressions-and-Predicates-17.20/Attribute-Functions)

## Bit/Byte Manipulation Functions[¶](#bit-byte-manipulation-functions)

<!-- prettier-ignore -->
|Teradata|Snowflake|Note|
|---|---|---|
|BITAND|BITAND||
|BITNOT|BITNOT||
|BITOR|BITOR||
|BITXOR|BITXOR||
|GETBIT|GETBIT||

> See
> [Bit/Byte functions](https://docs.teradata.com/r/Teradata-VantageTM-SQL-Functions-Expressions-and-Predicates-17.20/Bit/Byte-Manipulation-Functions)

## Built-In (System Functions)[¶](#built-in-system-functions)

<!-- prettier-ignore -->
|Teradata|Snowflake|Note|
|---|---|---|
|ACCOUNT|CURRENT_ACCOUNT||
|CURRENT_DATE CURDATE|CURRENT_DATE||
|CURRENT_ROLE|CURRENT_ROLE||
|CURRENT_TIME CURTIME|CURRENT_TIME||
|CURRENT_TIMESTAMP|CURRENT_TIMESTAMP||
|DATABASE|CURRENT_DATABASE||
|DATE|CURRENT_DATE||
|NOW|CURRENT_TIMESTAMP||
|PROFILE|CURRENT_ROLE|Check [SSC-EWI-TD0068](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/teradataEWI#ssc-ewi-td0068) for more details on this transformation|
|SESSION|CURRENT_SESSION||
|TIME|CURRENT_TIME||
|USER|CURRENT_USER||

> See
> [Built-In Functions](https://docs.teradata.com/r/Teradata-VantageTM-SQL-Functions-Expressions-and-Predicates-17.20/Built-In-Functions)

## Business Calendars[¶](#business-calendars)

<!-- prettier-ignore -->
|Teradata|Snowflake|Note|
|---|---|---|
|DAYNUMBER_OF_MONTH(DatetimeValue, ‘COMPATIBLE’)|DAYOFMONTH||
|DAYNUMBER_OF_MONTH(DatetimeValue, ‘ISO’)|DAYNUMBER_OF_MONTH_ISO_UDF||
|DAYNUMBER_OF_MONTH(DatetimeValue, ‘TERADATA’)|DAYOFMONTH||
|DAYNUMBER_OF_WEEK(DatetimeValue, ‘ISO’)|DAYOFWEEKISO||
|DAYNUMBER_OF_WEEK(DatetimeValue, ‘COMPATIBLE’)|DAY_OF_WEEK_COMPATIBLE_UDF||
|DAYNUMBER_OF_WEEK(DatetimeValue, ‘TERADATA’) DAYNUMBER_OF_WEEK(DatetimeValue)|TD_DAY_OF_WEEK_UDF||
|DAYNUMBER_OF_YEAR(DatetimeValue, ‘ISO’)|PUBLIC.DAY_OF_YEAR_ISO_UDF||
|DAYNUMBER_OF_YEAR(DatetimeValue)|DAYOFYEAR||
|QUARTERNUMBER_OF_YEAR|QUARTER||
|TD_SUNDAY(DateTimeValue)|PREVIOUS_DAY(DateTimeValue, ‘Sunday’)||
|WEEKNUMBER_OF_MONTH|WEEKNUMBER_OF_MONTH_UDF||
|WEEKNUMBER_OF_QUARTER(dateTimeValue)|WEEKNUMBER_OF_QUARTER_UDF||
|WEEKNUMBER_OF_QUARTER(dateTimeValue, ‘ISO’)|WEEKNUMBER_OF_QUARTER_ISO_UDF||
|WEEKNUMBER_OF_QUARTER(dateTimeValue, ‘COMPATIBLE’)|WEEKNUMBER_OF_QUARTER_COMPATIBLE_UDF||
|WEEKNUMBER_OF_YEAR(DateTimeValue, ‘ISO’)|WEEKISO||
|YEARNUMBER_OF_CALENDAR(DATETIMEVALUE, ‘COMPATIBLE’)|YEAR||
|YEARNUMBER_OF_CALENDAR(DATETIMEVALUE, ‘ISO’)|YEAROFWEEKISO||

> See
> [Business Calendars](https://docs.teradata.com/r/Teradata-VantageTM-SQL-Date-and-Time-Functions-and-Expressions-17.20/Business-Calendars)

## Calendar Functions[¶](#calendar-functions)

<!-- prettier-ignore -->
|Teradata|Snowflake|Note|
|---|---|---|
|DAYNUMBER_OF_WEEK(DatetimeValue)|TD_DAY_OF_WEEK_UDF||
|DAYNUMBER_OF_WEEK(DatetimeValue, ‘COMPATIBLE’)|DAY_OF_WEEK_COMPATIBLE_UDF||
|QuarterNumber_Of_Year(DatetimeValue, ‘ISO’)|QUARTER_OF_YEAR_ISO_UDF(DatetimeValue)||
|TD_DAY_OF_CALENDAR|TD_DAY_OF_CALENDAR_UDF||
|TD_DAY_OF_MONTH DAYOFMONTH|DAYOFMONTH||
|TD_DAY_OF_WEEK DAYOFWEEK|TD_DAY_OF_WEEK_UDF||
|TD_DAY_OF_YEAR|DAYOFYEAR||
|TD_MONTH_OF_CALENDAR(DateTimeValue) MONTH_CALENDAR(DateTimeValue)|TD_MONTH_OF_CALENDAR_UDF(DateTimeValue)||
|TD_WEEK_OF_CALENDAR(DateTimeValue) WEEK_OF_CALENDAR(DateTimeValue)|TD_WEEK_OF_CALENDAR_UDF(DateTimeValue)||
|TD_WEEK_OF_YEAR|WEEK_OF_YEAR_UDF||
|TD_YEAR_BEGIN(DateTimeValue)|YEAR_BEGIN_UDF(DateTimeValue)||
|TD_YEAR_BEGIN(DateTimeValue, ‘ISO’)|YEAR_BEGIN_ISO_UDF(DateTimeValue)||
|TD_YEAR_END(DateTimeValue)|YEAR_END_UDF(DateTimeValue)||
|TD_YEAR_END(DateTimeValue, ‘ISO’)|YEAR_END_ISO_UDF(DateTimeValue)||
|WEEKNUMBER_OF_MONTH(DateTimeValue)|WEEKNUMBER_OF_MONTH_UDF(DateTimeValue)||
|WEEKNUMBER_OF_QUARTER(DateTimeValue)|WEEKNUMBER_OF_QUARTER_UDF(DateTimeValue)||
|WEEKNUMBER_OF_QUARTER(DateTimeValue, ‘ISO’)|WEEKNUMBER_OF_QUARTER_ISO_UDF(DateTimeValue)||
|WEEKNUMBER_OF_QUARTER(DateTimeValue, ‘COMPATIBLE’)|WEEKNUMBER_OF_QUARTER_COMPATIBLE_UDF(DateTimeValue)||
|WEEKNUMBER_OF_YEAR(DateTimeValue)|WEEK_OF_YEAR_UDF(DateTimeValue)||
|WEEKNUMBER_OF_YEAR(DateTimeValue, ‘COMPATIBLE’)|WEEK_OF_YEAR_COMPATIBLE_UDF(DateTimeValue)||

> See
> [Calendar Functions](https://docs.teradata.com/r/WX0vkeB8F3JQXZ0HTR~d0Q/~8TzAjUr3AFwohWtu8ndxQ)

## Case Functions[¶](#case-functions)

<!-- prettier-ignore -->
|Teradata|Snowflake|Note|
|---|---|---|
|COALESCE|COALESCE|Check [Coalesce](#coalesce).|
|NULLIF|NULLIF||

> See
> [case functions](https://docs.teradata.com/r/Teradata-VantageTM-SQL-Functions-Expressions-and-Predicates-17.20/CASE-Expressions)

## Comparison Functions[¶](#comparison-functions)

<!-- prettier-ignore -->
|Teradata|Snowflake|Note|
|---|---|---|
|DECODE|DECODE||
|GREATEST|GREATEST||
|LEAST|LEAST||

> See
> [comparison functions](https://docs.teradata.com/r/Teradata-VantageTM-SQL-Functions-Expressions-and-Predicates-17.20/Comparison-Operators-and-Functions)

## Data type conversions[¶](#data-type-conversions)

<!-- prettier-ignore -->
|Teradata|Snowflake|Note|
|---|---|---|
|CAST|CAST||
|CAST(DatetimeValue AS INT)|DATE_TO_INT_UDF||
|CAST (VarcharValue AS INTERVAL)|INTERVAL_UDF|Check [Cast to INTERVAL datatype](#cast-to-interval-datatype)|
|TRYCAST|TRY_CAST||
|FROM_BYTES|TO_NUMBER TO_BINARY|[FROM_BYTES](#from-bytes) with ASCII parameter not supported in Snowflake.|

> See
> [Data Type Conversions](https://docs.teradata.com/reader/~_sY_PYVxZzTnqKq45UXkQ/iZ57TG_CtznEu1JdSbFNsQ)

## Data Type Conversion Functions[¶](#data-type-conversion-functions)

<!-- prettier-ignore -->
|Teradata|Snowflake|Note|
|---|---|---|
|TO_BYTES(Input, ‘Base10’)|INT2HEX_UDF(Input)||
|TO_NUMBER|TO_NUMBER||
|TO_CHAR|TO_CHAR or equivalent expression|Check [TO_CHAR](#to-char).|
|TO_DATE|TO_DATE||
|TO_DATE(input, ‘YYYYDDD’)|JULIAN_TO_DATE_UDF||

> See
> [Data Type Conversion Functions](https://docs.teradata.com/r/Teradata-VantageTM-Data-Types-and-Literals/March-2019/Data-Type-Conversion-Functions)

## DateTime and Interval functions[¶](#datetime-and-interval-functions)

<!-- prettier-ignore -->
|Teradata|Snowflake|Note|
|---|---|---|
|ADD_MONTHS|ADD_MONTHS||
|EXTRACT|EXTRACT||
|LAST_DAY|LAST_DAY||
|MONTH|MONTH||
|MONTHS_BETWEEN|MONTHS_BETWEEN_UDF||
|NEXT_DAY|NEXT_DAY||
|OADD_MONTHS|ADD_MONTHS||
|ROUND(Numeric)|ROUND||
|ROUND(Date)|ROUND_DATE_UDF||
|TRUNC(Date)|TRUNC_UDF||
|YEAR|YEAR||

> See
> [DateTime and Interval Functions and Expressions](https://docs.teradata.com/r/kmuOwjp1zEYg98JsB8fu_A/JhmMJqd9vWURvHYeTRgQLQ)

## Hash functions[¶](#hash-functions)

<!-- prettier-ignore -->
|Teradata|Snowflake|Note|
|---|---|---|
|HASH_MD5|MD5||
|HASHAMP HASHBACKAM HASHBUCKET HASHROW|Not supported|Check notes on [the architecture differences between Teradata and Snowflake](#architecture-differences-between-teradata-and-snowflake)|

> See [Hash functions](https://docs.teradata.com/r/756LNiPSFdY~4JcCCcR5Cw/jslafnqlE8bGpg~wXQiEFw)

## JSON functions[¶](#json-functions)

<!-- prettier-ignore -->
|Teradata|Snowflake|Note|
|---|---|---|
|NEW JSON|TO_JSON(PARSE_JSON()**)**|Check [NEW JSON](#new-json)|
|JSON_CHECK|CHECK_JSON|Check JSON_CHECK|
|JSON_TABLE|Equivalent query|Check [JSON_TABLE](#json-table)|
|JSONExtract JSONExtractValue JSONExtractLargeValue|JSON_EXTRACT_UDF|Check [JSON_EXTRACT](#json-extract)|

> See
> [JSON documentation](https://docs.teradata.com/r/C8cVEJ54PO4~YXWXeXGvsA/_aeoMCG0XgMNegNj0oy5cg)

## Null-Handling functions[¶](#null-handling-functions)

<!-- prettier-ignore -->
|Teradata|Snowflake|Note|
|---|---|---|
|NVL|NVL||
|NVL2|NVL2||

> See
> [Null-Handling functions](https://docs.teradata.com/r/756LNiPSFdY~4JcCCcR5Cw/4di35TY_6SqRNEGk4vv0ww)

## Ordered Analytical/Window Aggregate functions[¶](#ordered-analytical-window-aggregate-functions)

<!-- prettier-ignore -->
|Teradata|Snowflake|Note|
|---|---|---|
|CSUM(col1, col2)|SUM(col_1) OVER (PARTITION BY null ORDER BY col_2 ROWS UNBOUNDED PRECEDING)||
|CUME_DIST|CUME_DIST||
|DENSE_RANK|DENSE_RANK||
|FIRST_VALUE|FIRST_VALUE||
|LAG|LAG||
|LAST_VALUE|LAST_VALUE||
|LEAD|LEAD||
|MAVG(csales, 2, cdate, csales)|AVG(csales) OVER ( ORDER BY cdate, csales ROWS 1 PRECEDING)||
|MEDIAN|MEDIAN||
|MSUM(csales, 2, cdate, csales)|SUM(csales) OVER(ORDER BY cdate, csales ROWS 1 PRECEDING)||
|PERCENT_RANK|PERCENT_RANK||
|PERCENTILE_CONT|PERCENTILE_CONT||
|PERCENTILE_DISC|PERCENTILE_DISC||
|QUANTILE|QUANTILE||
|RANK|RANK||
|ROW_NUMBER|ROW_NUMBER||

> See [Window functions](https://docs.teradata.com/r/756LNiPSFdY~4JcCCcR5Cw/qbFqalW6IF5Fryz47~iqJQ)

## Period functions and operators[¶](#period-functions-and-operators)

<!-- prettier-ignore -->
|Teradata|Snowflake|Note|
|---|---|---|
|BEGIN|PERIOD_BEGIN_UDF||
|END|PERIOD_END_UDF||
|INTERVAL|TIMESTAMPDIFF||
|LAST|PERIOD_LAST_UDF||
|LDIFF|PERIOD_LDIFF_UDF||
|OVERLAPS|PUBLIC.PERIOD_OVERLAPS_UDF||
|PERIOD|PERIOD_UDF||
|PERIOD(datetimeValue, UNTIL_CHANGED) PERIOD(datetimeValue, UNTIL_CLOSED)|PERIOD_UDF(datetimeValue, ‘9999-12-31 23:59:59.999999’)|See notes about [ending bound constants](#ending-bound-constants-until-changed-and-until-closed)|
|RDIFF|PERIOD_RDIFF_UDF||

> See
> [Period Functions and Operators](https://docs.teradata.com/r/Teradata-Database-SQL-Functions-Operators-Expressions-and-Predicates/June-2017/Period-Functions-and-Operators)

## Query band functions[¶](#query-band-functions)

<!-- prettier-ignore -->
|Teradata|Snowflake|Note|
|---|---|---|
|GETQUERYBANDVALUE|GETQUERYBANDVALUE_UDF|Check G[ETQUERYBANDVALUE](#getquerybandvalue)|

> See
> [Query band functions](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/Teradata-VantageTM-Application-Programming-Reference-17.20/Workload-Management-Query-Band-APIs/Open-APIs-SQL-Interfaces)

## Regex functions[¶](#regex-functions)

<!-- prettier-ignore -->
|Teradata|Snowflake|Note|
|---|---|---|
|REGEXP_INSTR|REGEXP_INSTR|Check [Regex functions](#regex-functions)|
|REGEXP_REPLACE|REGEXP_REPLACE|Check [Regex functions](#regex-functions)|
|REGEXP_SIMILAR|REGEXP_LIKE|Check [Regex functions](#regex-functions)|
|REGEXP_SUBSTR|REGEXP_SUBSTR|Check [Regex functions](#regex-functions)|

> See [Regex functions](https://docs.teradata.com/r/756LNiPSFdY~4JcCCcR5Cw/yL2xT~elOTehmwVmwVBRHA)

## String operators and functions[¶](#string-operators-and-functions)

<!-- prettier-ignore -->
|Teradata|Snowflake|Note|
|---|---|---|
|ASCII|ASCII||
|CHAR2HEXINT|CHAR2HEXINT_UDF||
|CHR|CHR/CHAR||
|CHAR_LENGTH|LEN||
|CONCAT|CONCAT||
|EDITDISTANCE|EDITDISTANCE||
|INDEX|CHARINDEX|Check notes about [implicit conversion](#implicit-conversion)|
|INITCAP|INITCAP||
|INSTR|REGEXP_INSTR||
|INSTR(StringValue, StringValue ,NumericNegativeValue, NumericValue)|INSTR_UDF(StringValue, StringValue ,NumericNegativeValue, NumericValue)||
|LEFT|LEFT||
|LENGTH|LENGTH||
|LOWER|LOWER||
|LPAD|LPAD||
|LTRIM|LTRIM||
|OREPLACE|REPLACE||
|OTRANSLATE|TRANSLATE||
|POSITION|POSITION|Check notes about [implicit conversion](#implicit-conversion)|
|REVERSE|REVERSE||
|RIGHT|RIGHT||
|RPAD|RPAD||
|RTRIM|RTRIM||
|SOUNDEX|SOUNDEX_P123||
|STRTOK|STRTOK||
|STRTOK_SPLIT_TO_TABLE|STRTOK_SPLIT_TO_TABLE|Check [Strtok_split_to_table](#strtok-split-to-table)|
|SUBSTRING|SUBSTR/SUBSTR_UDF|Check [Substring](#substring)|
|TRANSLATE_CHK|TRANSLATE_CHK_UDF||
|TRIM(LEADING ‘0’ FROM aTABLE)|LTRIM(aTABLE, ‘0’)||
|TRIM(TRAILING ‘0’ FROM aTABLE)|RTRIM(aTABLE, ‘0’)||
|TRIM(BOTH ‘0’ FROM aTABLE)|TRIM(aTABLE, ‘0’)||
|TRIM(CAST(numericValue AS FORMAT ‘999’))|LPAD(numericValue, 3, 0)||
|UPPER|UPPER||

> See
> [String operators and functions](https://docs.teradata.com/reader/756LNiPSFdY~4JcCCcR5Cw/5nyfztBE7gDQVCVU2MFTnA)​​​

## St_Point functions[¶](#st-point-functions)

<!-- prettier-ignore -->
|Teradata|Snowflake|Note|
|---|---|---|
|ST_SPHERICALDISTANCE|HAVERSINE ST_DISTANCE||

See [St_Point functions](https://docs.teradata.com/r/W1AEeHO2cxTi3Sn7dtj8hg/JDVMx04qe~mo1mIm2h7NWQ)

## Table operators[¶](#table-operators)

<!-- prettier-ignore -->
|Teradata|Snowflake|Note|
|---|---|---|
|TD_UNPIVOT|Equivalent query|Check [Td_unpivot](#td-unpivot)|

> See
> [Table Operators](https://docs.teradata.com/r/Teradata-Database-SQL-Functions-Operators-Expressions-and-Predicates/June-2017/Table-Operators)

## XML functions[¶](#xml-functions)

<!-- prettier-ignore -->
|Teradata|Snowflake|Note|
|---|---|---|
|XMLAGG|LISTAGG|Check [Xmlagg](#xmlagg)|
|XMLQUERY|Not Supported||

> See [XML functions](https://docs.teradata.com/r/JTydkOYDksSy26sxlEtMvg/GhlIYri~mxyncdX5BV3jWA)

## Extensibility UDFs[¶](#extensibility-udfs)

This section contains UDFs and other extensibility functions that are not offered as system built-in
functions by Teradata but are transformed by SnowConvert AI

<!-- prettier-ignore -->
|Teradata|Snowflake|Note|
|---|---|---|
|CHKNUM|CHKNUM_UDF|Check [this UDF download page](https://downloads.teradata.com/download/extensibility/isnumeric-udf)|

## Notes[¶](#notes)

### Architecture differences between Teradata and Snowflake[¶](#architecture-differences-between-teradata-and-snowflake)

Teradata has a shared-nothing architecture with Access Module Processors (AMP) where each AMP
manages their own share of disk storage and is accessed through hashing when doing queries. To take
advantage of parallelism the stored information should be evenly distributed among AMPs and to do
this Teradata offers a group of hash-related functions that can be used to determine how good the
actual primary indexes are.

On the other hand, Snowflake architecture is different, and it manages how the data is stored on its
own, meaning users do not need to worry about optimizing their data distribution.

### Ending bound constants (UNTIL_CHANGED and UNTIL_CLOSED)[¶](#ending-bound-constants-until-changed-and-until-closed)

Both UNTIL_CHANGED and UNTIL_CLOSED are Teradata constants that represent an undefined ending bound
for periods. Internally, these constants are represented as the maximum value a timestamp can have
i.e ‘9999-12-31 23:59:59.999999’. During the migration of the PERIOD function, the ending bound is
checked if present to determine if it is one of these constants and to replace it with varchar of
value ‘9999-12-31 23:59:59.999999’ in case it is, Snowflake then casts the varchar to date or
timestamp depending on the type of the beginning bound when calling PERIOD\_\_\_UDF.

### Implicit conversion[¶](#implicit-conversion)

Some Teradata string functions like INDEX or POSITION accept non-string data types and implicitly
convert them to string, this can cause inconsistencies in the results of those functions between
Teradata and Snowflake. For example, the following Teradata code:

```
 SELECT INDEX(35, '5');
```

Returns 4, while the CHARINDEX equivalent in Snowflake:

```
 SELECT CHARINDEX('5', 35);
```

Returns 2, this happens because Teradata has its own
[default formats](https://docs.teradata.com/r/S0Fw2AVH8ff3MDA0wDOHlQ/Xh8u4~A7KI46wOdMG9DSHQ) which
are used during implicit conversion. In the above example, Teradata
[interprets the numeric constant](https://docs.teradata.com/r/T5QsmcznbJo1bHmZT2KnFw/TEOJhlyP6az05SdTK9JHMg)
35 as BYTEINT and uses BYTEINT default format`'-999'` for the implicit conversion to string, causing
the converted value to be `' 35'`. On the other hand, Snowflake uses its own
[default formats](https://docs.snowflake.com/en/sql-reference/sql-format-models.html#default-formats-for-parsing),
creating inconsistencies in the result.

To solve this, the following changes are done to those function parameters:

- If the parameter does **not** have a cast with format, then a snowflake`TO_VARCHAR`function with
  the default Teradata format equivalent in Snowflake is added instead.
- If the parameter does have a cast with format, then the format is converted to its Snowflake
  equivalent and the`TO_VARCHAR`function is added.

  - As a side note, Teradata ignores the sign of a number if it is not explicitly put inside a
    format, while Snowflake always adds spaces to insert the sign even when not specified, for those
    cases a check is done to see if the sign was specified and to remove it from the Snowflake
    string in case it was not.

After these changes, the resulting code would be:

```
 SELECT CHARINDEX( '5', TO_VARCHAR(35, 'MI999'));
```

Which returns 4, the same as the Teradata code.

## Known Issues [¶](#known-issues)

No issues were found.

## Related EWIs [¶](#related-ewis)

No related EWIs.

## COALESCE[¶](#coalesce)

### Description[¶](#description)

The coalesce function is used to return the first non-null element in a list. For more information
check [COALESCE](https://docs.teradata.com/r/kmuOwjp1zEYg98JsB8fu_A/Wo3afkb7dFsUUAO5AwQOkQ).

```
COALESCE(element_1, element_2 [, element_3, ..., element_n])
```

Both Teradata and Snowflake COALESCE functions allow mixing numeric with string and date with
timestamp parameters. However, they handle these two cases differently:

- Numeric along with string parameters: Teradata converts all numeric parameters to varchar while
  Snowflake does the opposite
- Timestamp along with date parameters: Teradata converts all timestamps to date while Snowflake
  does the opposite

To ensure functional equivalence in the first case, all numeric parameters are cast
to`string`using`to_varchar`function, this takes the format of the numbers into account. In the
second case, all timestamps are casted to date using `to_date`, Teradata ignores the format of
timestamps when casting them so it is removed during transformation.

### Sample Source Patterns[¶](#sample-source-patterns)

#### Numeric mixed with string parameters[¶](#numeric-mixed-with-string-parameters)

##### _Teradata_[¶](#teradata)

**Query**

```
 SELECT COALESCE(125, 'hello', cast(850 as format '-999'));
```

**Result**

```
COLUMN1|
-------+
125    |
```

##### _Snowflake_[¶](#snowflake)

**Query**

```
SELECT
 COALESCE(TO_VARCHAR(125), 'hello', TO_VARCHAR(850, '9000'));
```

**Result**

```
COLUMN1|
-------+
125    |
```

#### Timestamp mixed with date parameters[¶](#timestamp-mixed-with-date-parameters)

##### _Teradata_[¶](#id1)

**Query**

```
 SELECT COALESCE(cast(TIMESTAMP '2021-09-14 10:14:59' as format 'HH:MI:SSBDD-MM-YYYY'), current_date);
```

**Result**

```
COLUMN1    |
-----------+
2021-09-14 |
```

##### _Snowflake_[¶](#id2)

**Query**

```
SELECT
 COALESCE(TO_DATE(TIMESTAMP '2021-09-14 10:14:59' !!!RESOLVE EWI!!! /*** SSC-EWI-TD0025 - OUTPUT FORMAT 'HH:MI:SSBDD-MM-YYYY' NOT SUPPORTED. ***/!!!), CURRENT_DATE());
```

**Result**

```
COLUMN1    |
-----------+
2021-09-14 |
```

### Known Issues[¶](#id3)

No known issues\_.\_

### Related EWIs[¶](#id4)

- [SSC-EWI-TD0025](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/teradataEWI#ssc-ewi-td0025):
  Output format not supported.

## CURRENT_TIMESTAMP[¶](#current-timestamp)

### Severity[¶](#severity)

Low

### Description[¶](#id5)

Fractional seconds are only displayed if it is explicitly set in the TIME_OUTPUT_FORMAT session
parameter.

#### Input code:[¶](#input-code)

```
SELECT current_timestamp(4) at local;
```

#### Output code:[¶](#output-code)

```
SELECT
CURRENT_TIMESTAMP(4);
```

### Recommendations[¶](#recommendations)

- Check if the TIME_OUTPUT\_\_\_FORMAT session parameter is set to get the behavior that you want.
- If you need more support, you can email us at
  [snowconvert-support@snowflake.com](https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/teradata/sql-translation-reference/mailto:snowconvert-support%40snowflake.com)

### Known Issues [¶](#id6)

No issues were found.

### Related EWIs [¶](#id7)

No related EWIs.

## DAYNUMBER_OF_MONTH[¶](#daynumber-of-month)

### Description[¶](#id8)

Returns the number of days elapsed from the beginning of the month to the given date. For more
information check
[DAYNUMBER_OF_MONTH](https://docs.teradata.com/r/kmuOwjp1zEYg98JsB8fu_A/msvzanlVHZUHwFv5LYpqzg).

```
DAYNUMBER_OF_MONTH(expression [, calendar_name])
```

Both Teradata and Snowflake handle the DAYNUMBER_OF_MONTH function in the same way, except in one
case:

- The ISO calendar: An ISO month has 4 or 5 complete weeks. For more information check
  [About ISO Computation](https://docs.teradata.com/r/kmuOwjp1zEYg98JsB8fu_A/RdZQp3YPJ1WrBpj8b3uljA).

To ensure functional equivalence, a user-defined function (UDF) is added for the ISO calendar case.

### Sample Source Patterns[¶](#id9)

#### _Teradata_[¶](#id10)

**Query**

```
SELECT
    DAYNUMBER_OF_MONTH (DATE'2022-12-22'),
    DAYNUMBER_OF_MONTH (DATE'2022-12-22', NULL),
    DAYNUMBER_OF_MONTH (DATE'2022-12-22', 'Teradata'),
    DAYNUMBER_OF_MONTH (DATE'2022-12-22', 'COMPATIBLE');
```

**Result**

```
COLUMN1|COLUMN2|COLUMN3|COLUMN4|
-------+-------+-------+-------+
22     |22     |22     |22     |
```

#### _Snowflake_[¶](#id11)

**Query**

```
SELECT
    DAYOFMONTH(DATE'2022-12-22'),
    DAYOFMONTH(DATE'2022-12-22'),
    DAYOFMONTH(DATE'2022-12-22'),
    DAYOFMONTH(DATE'2022-12-22');
```

**Result**

```
COLUMN1|COLUMN2|COLUMN3|COLUMN4|
-------+-------+-------+-------+
22     |22     |22     |22     |
```

#### ISO calendar[¶](#iso-calendar)

##### _Teradata_[¶](#id12)

**Query**

```
SELECT DAYNUMBER_OF_MONTH (DATE'2022-12-22', 'ISO');
```

**Result**

```
COLUMN1|
-------+
25     |
```

##### _Snowflake_[¶](#id13)

**Query**

```
SELECT
PUBLIC.DAYNUMBER_OF_MONTH_UDF(DATE'2022-12-22');
```

**Result**

```
COLUMN1|
-------+
25     |
```

### Known Issues [¶](#id14)

No issues were found.

### Related EWIs [¶](#id15)

No related EWIs.

## FROM_BYTES[¶](#from-bytes)

Translation specification for transforming the TO_CHAR function into an equivalent function
concatenation in Snowflake

### Description[¶](#id16)

The FROM_BYTES function encodes a sequence of bits into a sequence of characters representing its
encoding. For more information check
[FROM_BYTES(Encoding)](https://www.docs.teradata.com/r/Teradata-VantageTM-Data-Types-and-Literals/March-2019/Data-Type-Conversion-Functions/FROM_BYTES).

Snowflake does not have support for FROM_BYTES function, however, some workarounds can be done for
the most common occurrences of this function.

### Sample Source Patterns[¶](#id17)

#### Teradata[¶](#id18)

##### Query[¶](#query)

```
 SELECT
FROM_BYTES('5A1B'XB, 'base10'), --returns '23067'
FROM_BYTES('5A3F'XB, 'ASCII'), --returns 'Z\ESC '
FROM_BYTES('5A1B'XB, 'base16'); -- returns '5A1B'
```

##### Result[¶](#result)

```
COLUMN1    | COLUMN2    | COLUMN3 |
-----------+------------+---------+
23067      |  Z\ESC     | 5A1B    |
```

##### Snowflake[¶](#id19)

##### Query[¶](#id20)

```
 SELECT
--returns '23067'
TO_NUMBER('5A1B', 'XXXX'),
--returns 'Z\ESC '
!!!RESOLVE EWI!!! /*** SSC-EWI-0031 - FROM_BYTES FUNCTION NOT SUPPORTED ***/!!!
FROM_BYTES(TO_BINARY('5A3F'), 'ASCII'),
TO_BINARY('5A1B', 'HEX'); -- returns '5A1B'
```

##### Result[¶](#id21)

```
COLUMN1    | COLUMN2    | COLUMN3 |
-----------+------------+---------+
23067      |  Z\ESC     | 5A1B    |
```

**Note:**

Some parts in the output code are omitted for clarity reasons.

### Known Issues[¶](#id22)

1. TO_NUMBER format parameter must match with the digits on the input string.
2. There is no functional equivalent built-in function for FROM_BYTES when encoding to ANSI

### Related EWIs[¶](#id23)

1. [SSC-EWI-0031](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0031):
   FUNCTION NOT SUPPORTED

## GETQUERYBANDVALUE[¶](#getquerybandvalue)

Translation specification for the transformation of GetQueryBandValue to Snowflake

### Description[¶](#id24)

The GetQueryBandValue function searches a name key inside of the query band and returns its
associated value if present. It can be used to search inside the transaction, session, profile, or
any of the key-value pairs of the query band.

For more information on this function check
[GetQueryBandValue](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/Teradata-VantageTM-Application-Programming-Reference-17.20/Workload-Management-Query-Band-APIs/Open-APIs-SQL-Interfaces/GetQueryBandValue)
in the Teradata documentation.

```
[SYSLIB.]GetQueryBandValue([QueryBandIn,] SearchType, Name);
```

### Sample Source Patterns[¶](#id25)

#### Setup data[¶](#setup-data)

##### Teradata[¶](#id26)

##### Query[¶](#id27)

```
 SET QUERY_BAND = 'hola=hello;adios=bye;' FOR SESSION;
```

##### _Snowflake_[¶](#id28)

##### Query[¶](#id29)

```
 ALTER SESSION SET QUERY_TAG = 'hola=hello;adios=bye;';
```

#### GetQueryBandValue with QueryBandIn parameter[¶](#getquerybandvalue-with-querybandin-parameter)

##### _Teradata_[¶](#id30)

##### Query[¶](#id31)

```
 SELECT
GETQUERYBANDVALUE('=T> user=Mark;account=Mark200; =S> user=Sara;account=SaraDB;role=DbAdmin =P> user=Peter;account=Peter3;', 0, 'account') as Example1,
GETQUERYBANDVALUE('=T> user=Mark;account=Mark200; =S> user=Sara;account=SaraDB;role=DbAdmin =P> user=Peter;account=Peter3;', 1, 'account') as Example2,
GETQUERYBANDVALUE('=T> user=Mark;account=Mark200; =S> user=Sara;account=SaraDB;role=DbAdmin =P> user=Peter;account=Peter3;', 2, 'account') as Example3,
GETQUERYBANDVALUE('=T> user=Mark;account=Mark200; =S> user=Sara;account=SaraDB;role=DbAdmin =P> user=Peter;account=Peter3;', 3, 'account') as Example4,
GETQUERYBANDVALUE('=T> user=Mark;account=Mark200; =S> user=Sara;account=SaraDB;role=DbAdmin =P> user=Peter;account=Peter3;', 0, 'role') as Example5,
GETQUERYBANDVALUE('=T> user=Mark;account=Mark200; =S> user=Sara;account=SaraDB;role=DbAdmin =P> user=Peter;account=Peter3;', 1, 'role') as Example6;
```

##### Result[¶](#id32)

```
+----------+----------+----------+----------+----------+----------+
<!-- prettier-ignore -->
|EXAMPLE1|EXAMPLE2|EXAMPLE3|EXAMPLE4|EXAMPLE5|EXAMPLE6|
+----------+----------+----------+----------+----------+----------+
<!-- prettier-ignore -->
|Mark200|Mark200|SaraDB|Peter3|DbAdmin||
+----------+----------+----------+----------+----------+----------+
```

##### _Snowflake_[¶](#id33)

##### Query[¶](#id34)

```
 SELECT
GETQUERYBANDVALUE_UDF('=T> user=Mark;account=Mark200; =S> user=Sara;account=SaraDB;role=DbAdmin =P> user=Peter;account=Peter3;', 0, 'account') as Example1,
GETQUERYBANDVALUE_UDF('=T> user=Mark;account=Mark200; =S> user=Sara;account=SaraDB;role=DbAdmin =P> user=Peter;account=Peter3;', 1, 'account') as Example2,
GETQUERYBANDVALUE_UDF('=T> user=Mark;account=Mark200; =S> user=Sara;account=SaraDB;role=DbAdmin =P> user=Peter;account=Peter3;', 2, 'account') as Example3,
GETQUERYBANDVALUE_UDF('=T> user=Mark;account=Mark200; =S> user=Sara;account=SaraDB;role=DbAdmin =P> user=Peter;account=Peter3;', 3, 'account') as Example4,
GETQUERYBANDVALUE_UDF('=T> user=Mark;account=Mark200; =S> user=Sara;account=SaraDB;role=DbAdmin =P> user=Peter;account=Peter3;', 0, 'role') as Example5,
GETQUERYBANDVALUE_UDF('=T> user=Mark;account=Mark200; =S> user=Sara;account=SaraDB;role=DbAdmin =P> user=Peter;account=Peter3;', 1, 'role') as Example6;
```

##### Result[¶](#id35)

```
+----------+----------+----------+----------+----------+----------+
<!-- prettier-ignore -->
|EXAMPLE1|EXAMPLE2|EXAMPLE3|EXAMPLE4|EXAMPLE5|EXAMPLE6|
+----------+----------+----------+----------+----------+----------+
<!-- prettier-ignore -->
|Mark200|Mark200|SaraDB|Peter3|DbAdmin||
+----------+----------+----------+----------+----------+----------+
```

#### GetQueryBandValue without QueryBandIn parameter[¶](#getquerybandvalue-without-querybandin-parameter)

##### _Teradata_[¶](#id36)

##### Query[¶](#id37)

```
 SELECT
GETQUERYBANDVALUE(2, 'hola') as Example1,
GETQUERYBANDVALUE(2, 'adios') as Example2;
```

##### Result[¶](#id38)

```
+----------+----------+
<!-- prettier-ignore -->
|EXAMPLE1|EXAMPLE2|
+----------+----------+
<!-- prettier-ignore -->
|hello|bye|
+----------+----------+
```

##### _Snowflake_[¶](#id39)

##### Query[¶](#id40)

```
 SELECT
GETQUERYBANDVALUE_UDF('hola') as Example1,
GETQUERYBANDVALUE_UDF('adios') as Example2;
```

##### Result[¶](#id41)

```
+----------+----------+
<!-- prettier-ignore -->
|EXAMPLE1|EXAMPLE2|
+----------+----------+
<!-- prettier-ignore -->
|hello|bye|
+----------+----------+
```

**Note:**

Some parts in the output code are omitted for clarity reasons.

### Known Issues[¶](#id42)

**1. GetQueryBandValue without QueryBandIn parameter only supported for session**

Teradata allows defining query bands at transaction, session or profile levels. If GetQueryBandValue
is called without specifying an input query band Teradata will automatically check the transaction,
session or profile query bands depending on the value of the SearchType parameter.

In Snowflake the closest equivalent to query bands are query tags, which can be specified for
session, user and account.

Due to these differences, the implementation of GetQueryBandValue without QueryBandIn parameter only
considers the session query tag and may not work as expected for other search types.

### Related EWIs[¶](#id43)

No related EWIs.

## JSON_CHECK[¶](#json-check)

### Description[¶](#id44)

The JSON_CHECK function checks a string for valid JSON.

For more information regarding Teradata JSON_CHECK, check
[here](https://docs.teradata.com/r/Teradata-Database-JSON-Data-Type/June-2017/JSON-Functions-and-Operators/JSON_CHECK).

```
[TD_SYSFNLIB.]JSON_CHECK(string_expr);
```

### Sample Source Pattern[¶](#sample-source-pattern)

#### Basic Source Pattern[¶](#basic-source-pattern)

##### Teradata[¶](#id45)

**Query**

```
SELECT JSON_CHECK('{"key": "value"}');
```

##### Snowflake Scripting[¶](#snowflake-scripting)

**Query**

```
SELECT
IFNULL(CHECK_JSON('{"key": "value"}'), 'OK');
```

#### JSON_CHECK inside CASE transformation[¶](#json-check-inside-case-transformation)

##### Teradata[¶](#id46)

**Query**

```
SELECT CASE WHEN JSON_CHECK('{}') = 'OK' then 'OKK' ELSE 'NOT OK' END;
```

##### Snowflake Scripting[¶](#id47)

**Query**

```
SELECT
CASE
WHEN UPPER(RTRIM(IFNULL(CHECK_JSON('{}'), 'OK'))) = UPPER(RTRIM('OK'))
THEN 'OKK' ELSE 'NOT OK'
END;
```

### Known Issues [¶](#id48)

No issues were found.

### Related EWIs [¶](#id49)

No related EWIs.

## JSON_EXTRACT[¶](#json-extract)

Translation reference to convert the Teradata functions JSONExtractValue, JSONExtractLargeValue and
JSONExtract to Snowflake Scripting.

### Description[¶](#id50)

As per Teradata’s documentation, these functions use the
[JSONPath Query Syntax](https://docs.teradata.com/r/Teradata-VantageTM-JSON-Data-Type/March-2019/Operations-on-the-JSON-Type/JSONPath-Request-Syntax)
to request information about a portion of a JSON instance. The entity desired can be any portion of
a JSON instance, such as a name/value pair, an object, an array, an array element, or a value.

For more information regarding Teradata JSONExtractValue, JSONExtractLargeValue and JSONExtract,
check
[here](https://docs.teradata.com/r/Teradata-VantageTM-JSON-Data-Type/March-2019/JSON-Methods/Comparison-of-JSONExtract-and-JSONExtractValue).

```
 JSON_expr.JSONExtractValue(JSONPath_expr)

JSON_expr.JSONExtractLargeValue(JSONPath_expr)

JSON_expr.JSONExtract(JSONPath_expr)
```

The JSON_EXTRACT_UDF is a Snowflake implementation of the JSONPath specification that uses a
modified version of the original JavaScript implementation developed by
[Stefan Goessner](https://goessner.net/index.html).

#### Sample Source Pattern[¶](#id51)

##### Teradata[¶](#id52)

##### Query[¶](#id53)

```
 SELECT
    Store.JSONExtract('$..author') as AllAuthors,
    Store.JSONExtractValue('$..book[2].title') as ThirdBookTitle,
    Store.JSONExtractLargeValue('$..book[2].price') as ThirdBookPrice
FROM BookStores;
```

##### Snowflake Scripting[¶](#id54)

##### Query[¶](#id55)

```
 SELECT
    JSON_EXTRACT_UDF(Store, '$..author', FALSE) as AllAuthors,
    JSON_EXTRACT_UDF(Store, '$..book[2].title', TRUE) as ThirdBookTitle,
    JSON_EXTRACT_UDF(Store, '$..book[2].price', TRUE) as ThirdBookPrice
    FROM
    BookStores;
```

**Note:**

Some parts in the output code are omitted for clarity reasons.

### Known Issues[¶](#id56)

#### 1. Elements inside JSONs may not retain their original order.[¶](#elements-inside-jsons-may-not-retain-their-original-order)

Elements inside a JSON are ordered by their keys when inserted in a table. Thus, the query results
might differ. However, this does not affect the order of arrays inside the JSON.

For example, if the original JSON is:

```
 {
   "firstName":"Peter",
   "lastName":"Andre",
   "age":31,
   "cities": ["Los Angeles", "Lima", "Buenos Aires"]
}
```

Using the Snowflake
[PARSE_JSON()](https://docs.snowflake.com/en/sql-reference/functions/parse_json.html) that
interprets an input string as a JSON document, producing a VARIANT value. The inserted JSON will be:

```
 {
   "age": 31,
   "cities": ["Los Angeles", "Lima", "Buenos Aires"],
   "firstName": "Peter",
   "lastName": "Andre"
}
```

Note how “age” is now the first element. However, the array of “cities” maintains its original
order.

### Related EWIs[¶](#id57)

No related EWIs.

## JSON_TABLE[¶](#json-table)

Translation specification for the transformation of JSON_TABLE into a equivalent query in Snowflake

**Note:**

Some parts in the output code are omitted for clarity reasons.

### Description[¶](#id58)

Creates a table based on the contents of a JSON document. See
[JSON_TABLE documentation](https://docs.teradata.com/r/Teradata-VantageTM-JSON-Data-Type-17.20/JSON-Shredding/JSON_TABLE).

```
[TD_SYSFNLIB.]JSON_TABLE(
  ON (json_documents_retrieving_expr)
  USING
      ROWEXPR (row_expr_literal)
      COLEXPR (column_expr_literal)
  [AS] correlation_name [(column_name [,...])]
)
```

The conversion of JSON_TABLE has the considerations shown below:

- ROW_NUMBER() is an equivalent of ordinal columns in Snowflake.
- In Teradata, the second column of JSON_TABLE must be JSON type because the generated columns
  replace the second column, for that reason, SnowConvert AI assumes that the column has the right
  type, and uses it for the transformation.

### Sample Source Patterns[¶](#id59)

#### Setup data[¶](#id60)

##### Teradata[¶](#id61)

##### Query[¶](#id62)

```
 create table myJsonTable(
 col1 integer,
 col2 JSON(1000)
 );


insert into myJsonTable values(1,
new json('{
"name": "Matt",
"age" : 30,
"songs" : [
	{"name" : "Late night", "genre" : "Jazz"},
	{"name" : "Wake up", "genre" : "Rock"},
	{"name" : "Who am I", "genre" : "Rock"},
	{"name" : "Raining", "genre" : "Blues"}
]
}'));
```

##### _Snowflake_[¶](#id63)

##### Query[¶](#id64)

```
 CREATE OR REPLACE TABLE myJsonTable (
 col1 integer,
 col2 VARIANT
 )
 COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;

INSERT INTO myJsonTable
VALUES (1, TO_JSON(PARSE_JSON('{
"name": "Matt",
"age" : 30,
"songs" : [
	{"name" : "Late night", "genre" : "Jazz"},
	{"name" : "Wake up", "genre" : "Rock"},
	{"name" : "Who am I", "genre" : "Rock"},
	{"name" : "Raining", "genre" : "Blues"}
]
}')));
```

#### Pattern code 1[¶](#pattern-code-1)

##### _Teradata_[¶](#id65)

##### Query[¶](#id66)

```
 SELECT * FROM
JSON_TABLE(ON (SELECT COL1, COL2 FROM myJsonTable WHERE col1 = 1)
USING rowexpr('$.songs[*]')
colexpr('[ {"jsonpath" : "$.name",
            "type" : "CHAR(20)"},
            {"jsonpath" : "$.genre",
             "type" : "VARCHAR(20)"}]')) AS JT(ID, "Song name", Genre);
```

##### Result[¶](#id67)

```
ID | Song name  | Genre |
---+------------+-------+
1  | Late night | Jazz  |
---+------------+-------+
1  | Wake up    | Rock  |
---+------------+-------+
1  | Who am I   | Rock  |
---+------------+-------+
1  | Raining    | Blues |
```

##### _Snowflake_[¶](#id68)

##### Query[¶](#id69)

```
 SELECT
* FROM
(
SELECT
COL1 AS ID,
rowexpr.value:name :: CHAR(20) AS "Song name",
rowexpr.value:genre :: VARCHAR(20) AS Genre
FROM
myJsonTable,
TABLE(FLATTEN(INPUT => COL2:songs)) rowexpr
WHERE col1 = 1
) JT;
```

##### Result[¶](#id70)

```
ID | Song name  | Genre |
---+------------+-------+
1  | Late night | Jazz  |
---+------------+-------+
1  | Wake up    | Rock  |
---+------------+-------+
1  | Who am I   | Rock  |
---+------------+-------+
1  | Raining    | Blues |
```

### Known Issues[¶](#id71)

**1. The JSON path in COLEXPR can not have multiple asterisk accesses**

The columns JSON path cannot have multiple lists with asterisk access, for example:
`$.Names[*].FullNames[*]`. On the other hand, the JSON path of ROWEXP can have it.

**2. JSON structure defined in the COLEXPR literal must be a valid JSON**

When it is not the case the user will be warned about the JSON being badly formed.

### Related EWIs[¶](#id72)

No related EWIs.

## NEW JSON[¶](#new-json)

### Description[¶](#id73)

Allocates a new instance of a JSON datatype. For more information check
[NEW JSON Constructor Expression.](https://docs.teradata.com/r/Teradata-Database-JSON-Data-Type/June-2017/The-JSON-Data-Type/About-JSON-Type-Constructor/NEW-JSON-Constructor-Expression)

```
NEW JSON ( [ JSON_string_spec | JSON_binary_data_spec ] )

JSON_string_spec := JSON_String_literal [, { LATIN | UNICODE | BSON | UBJSON } ]

JSON_binary_data_spec := JSON_binary_literal [, { BSON | UBJSON } ]
```

The second parameter of the NEW JSON function is always omitted by SnowConvert AI since Snowflake
works only with UTF-8.

### Sample Source Patterns[¶](#id74)

#### NEW JSON with string data[¶](#new-json-with-string-data)

##### _Teradata_[¶](#id75)

**Query**

```
SELECT NEW JSON ('{"name" : "cameron", "age" : 24}'),
NEW JSON ('{"name" : "cameron", "age" : 24}', LATIN);
```

**Result**

<!-- prettier-ignore -->
|COLUMN1|COLUMN2|
|---|---|
|{“age”:24,”name”:”cameron”}|{“age”:24,”name”:”cameron”}|

##### _Snowflake_[¶](#id76)

**Query**

```
SELECT
TO_JSON(PARSE_JSON('{"name" : "cameron", "age" : 24}')),
!!!RESOLVE EWI!!! /*** SSC-EWI-TD0039 - INPUT FORMAT 'LATIN' NOT SUPPORTED ***/!!!
TO_JSON(PARSE_JSON('{"name" : "cameron", "age" : 24}'));
```

**Result**

<!-- prettier-ignore -->
|COLUMN1|COLUMN2|
|---|---|
|{“age”:24,”name”:”cameron”}|{“age”:24,”name”:”cameron”}|

### Known Issues[¶](#id77)

**1. The second parameter is not supported**

The second parameter of the function used to specify the format of the resulting JSON is not
supported because Snowflake only supports UTF-8, this may result in functional differences for some
uses of the function.

**2. JSON with BINARY data is not supported**

Snowflake does not support parsing binary data to create a JSON value, the user will be warned when
SnowConvert AI finds a NEW JSON with binary data.

### Related EWIs[¶](#id78)

1. [SSC-EWI-TD0039](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/teradataEWI#ssc-ewi-td0039):
   Input format not supported.

## NVP[¶](#nvp)

### Description[¶](#id79)

Extracts the value of the key-value pair where the key matches the nth occurrence of the specified
name to search. See
[NVP](https://docs.teradata.com/r/Teradata-VantageTM-SQL-Functions-Expressions-and-Predicates-17.20/String-Operators-and-Functions/NVP).

```
[TD_SYSFNLIB.] NVP (
in_string,
name_to_search
[, name_delimiters ]
[, value_delimiters ]
[, occurrence ]
)
```

### Sample Source Patterns[¶](#id80)

#### NVP basic case[¶](#nvp-basic-case)

##### _Teradata_[¶](#id81)

**Query**

```
SELECT
NVP('entree=-orange chicken&entree+.honey salmon', 'entree', '&', '=- +.', 1),
NVP('Hello=bye|name=Lucas|Hello=world!', 'Hello', '|', '=', 2),
NVP('Player=Mario$Game&Tenis%Player/Susana$Game=Chess', 'Player', '% $', '= & /', 2);
```

**Result**

```
COLUMN1        | COLUMN2 | COLUMN3 |
---------------+---------+---------+
orange chicken | world!  | Susana  |
```

##### _Snowflake_[¶](#id82)

**Query**

```
SELECT
PUBLIC.NVP_UDF('entree=-orange chicken&entree+.honey salmon', 'entree', '&', '=- +.', 1),
PUBLIC.NVP_UDF('Hello=bye|name=Lucas|Hello=world!', 'Hello', '|', '=', 2),
PUBLIC.NVP_UDF('Player=Mario$Game&Tenis%Player/Susana$Game=Chess', 'Player', '% $', '= & /', 2);
```

**Result**

```
COLUMN1        | COLUMN2 | COLUMN3 |
---------------+---------+---------+
orange chicken | world!  | Susana  |
```

#### NVP with optional parameters ignored[¶](#nvp-with-optional-parameters-ignored)

##### _Teradata_[¶](#id83)

**Query**

```
SELECT
NVP('City=Los Angeles&Color=Green&Color=Blue&City=San Jose', 'Color'),
NVP('City=Los Angeles&Color=Green&Color=Blue&City=San Jose', 'Color', 2),
NVP('City=Los Angeles#Color=Green#Color=Blue#City=San Jose', 'City', '#', '=');
```

**Result**

```
COLUMN1 | COLUMN2 | COLUMN3     |
--------+---------+-------------+
Green   | Blue    | Los Angeles |
```

##### _Snowflake_[¶](#id84)

**Query**

```
SELECT
    PUBLIC.NVP_UDF('City=Los Angeles&Color=Green&Color=Blue&City=San Jose', 'Color', '&', '=', 1),
    PUBLIC.NVP_UDF('City=Los Angeles&Color=Green&Color=Blue&City=San Jose', 'Color', '&', '=', 2),
    PUBLIC.NVP_UDF('City=Los Angeles#Color=Green#Color=Blue#City=San Jose', 'City', '#', '=', 1);
```

**Result**

```
COLUMN1 | COLUMN2 | COLUMN3     |
--------+---------+-------------+
Green   | Blue    | Los Angeles |
```

#### NVP with spaces in delimiters[¶](#nvp-with-spaces-in-delimiters)

##### _Teradata_[¶](#id85)

**Query**

```
SELECT
NVP('store = whole foods&&store: ?Bristol farms','store', '&&', '\ =\  :\ ?', 2),
NVP('Hello = bye|name = Lucas|Hello = world!', 'Hello', '|', '\ =\ ', 2);
```

**Result**

```
COLUMN1       | COLUMN2 |
--------------+---------+
Bristol farms | world!  |
```

##### _Snowflake_[¶](#id86)

**Query**

```
SELECT
PUBLIC.NVP_UDF('store = whole foods&&store: ?Bristol farms', 'store', '&&', '\\ =\\  :\\ ?', 2),
PUBLIC.NVP_UDF('Hello = bye|name = Lucas|Hello = world!', 'Hello', '|', '\\ =\\ ', 2);
```

**Result**

```
COLUMN1       | COLUMN2 |
--------------+---------+
Bristol farms | world!  |
```

#### NVP with non-literal delimiters[¶](#nvp-with-non-literal-delimiters)

##### _Teradata_[¶](#id87)

**Query**

```
SELECT NVP('store = whole foods&&store: ?Bristol farms','store', '&&', valueDelimiter, 2);
```

##### _Snowflake_[¶](#id88)

**Query**

```
SELECT
PUBLIC.NVP_UDF('store = whole foods&&store: ?Bristol farms', 'store', '&&', valueDelimiter, 2) /*** SSC-FDM-TD0008 - WHEN NVP_UDF FOURTH PARAMETER IS NON-LITERAL AND IT CONTAINS A BACKSLASH, THAT BACKSLASH NEEDS TO BE ESCAPED ***/;
```

### Known Issues[¶](#id89)

**1. Delimiters with spaces (\ ) need to have the backslash scaped in Snowflake**

In Teradata, delimiters including space specify them using “\ “ (see
[NVP with spaces in delimiters](#nvp-with-spaces-in-delimiters)), as shown in the examples, in
Teradata it is not necessary to escape the backslash, however, it is necessary in Snowflake.
Escaping the backslashes in the delimiter can be done automatically by SnowConvert AI but only if
the delimiter values are literal strings, otherwise the user will be warned that the backlashes
could not be escaped and that it may cause different results in Snowflake.

### Related EWIs[¶](#id90)

1. [SSC-FDM-TD0008](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/teradataFDM#ssc-fdm-td0008):
   Non-literal delimiters with spaces need their backslash scaped in snowflake.

## OVERLAPS[¶](#overlaps)

### Description[¶](#id91)

According to Teradata’s documentation, the OVERLAPS operator compares two or more period
expressions. If they overlap, it returns true.

For more information regarding Teradata’s OVERLAPS, check
[here](https://docs.teradata.com/r/kmuOwjp1zEYg98JsB8fu_A/3VIgdwHNVU~tsnNiIR1aEw).

```
period_expression
OVERLAPS
period_expression
```

The PERIOD_OVERLAPS_UDF is a Snowflake implementation of the OVERLAPS operator in Teradata.

### Sample Source Pattern[¶](#id92)

#### Teradata[¶](#id93)

**Query**

```
SELECT
    PERIOD(DATE '2009-01-01', DATE '2010-09-24')
    OVERLAPS
    PERIOD(DATE '2009-02-01', DATE '2009-06-24');
```

#### Snowflake Scripting[¶](#id94)

**Query**

```
SELECT
    PUBLIC.PERIOD_OVERLAPS_UDF(ARRAY_CONSTRUCT(PUBLIC.PERIOD_UDF(DATE '2009-01-01', DATE '2010-09-24') !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!, PUBLIC.PERIOD_UDF(DATE '2009-02-01', DATE '2009-06-24') !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!)) !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!;
```

### Known Issues[¶](#id95)

#### 1. Unsupported Period Expressions[¶](#unsupported-period-expressions)

The _PERIOD(TIME WITH TIME ZONE)_ and _PERIOD(TIMESTAMP WITH TIME ZONE)_ expressions are not
supported yet.

### Related EWIs[¶](#id96)

1. [SSC-EWI-TD0053](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/teradataEWI#ssc-ewi-td0053):
   Snowflake does not support the period datatype, all periods are handled as varchar instead

## P_INTERSECT[¶](#p-intersect)

### Description[¶](#id97)

According to Teradata’s documentation, the P_INTERSECT operator compares two or more period
expressions. If they overlap, it returns the common portion of the period expressions.

For more information regarding Teradata’s P_INTERSECT, check
[here](https://docs.teradata.com/r/kmuOwjp1zEYg98JsB8fu_A/iW6iefgeyOypFOMY2qGG_A).

```
period_expression
P_INTERSECT
period_expression
```

The PERIOD_INTERSECT_UDF is a Snowflake implementation of the P_INTERSECT operator in Teradata.

### Sample Source Pattern[¶](#id98)

#### Teradata[¶](#id99)

**Query**

```
SELECT
    PERIOD(DATE '2009-01-01', DATE '2010-09-24')
    P_INTERSECT
    PERIOD(DATE '2009-02-01', DATE '2009-06-24');
```

#### Snowflake Scripting[¶](#id100)

**Query**

```
SELECT
    PUBLIC.PERIOD_INTERSECT_UDF(ARRAY_CONSTRUCT(PUBLIC.PERIOD_UDF(DATE '2009-01-01', DATE '2010-09-24') !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!, PUBLIC.PERIOD_UDF(DATE '2009-02-01', DATE '2009-06-24') !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!)) !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!;
```

### Known Issues[¶](#id101)

#### 1. Unsupported Period Expressions[¶](#id102)

The _PERIOD(TIME WITH TIME ZONE)_ and _PERIOD(TIMESTAMP WITH TIME ZONE)_ expressions are not
supported yet.

### Related EWIs[¶](#id103)

1. [SSC-EWI-TD0053](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/teradataEWI#ssc-ewi-td0053):
   Snowflake does not support the period datatype, all periods are handled as varchar instead

## PIVOT[¶](#pivot)

Translation specification for the PIVOT function form Teradata to Snowflake

**Note:**

Some parts in the output code are omitted for clarity reasons.

### Description[¶](#id104)

The pivot function is used to transform rows of a table into columns. For more information check the
[PIVOT Teradata documentation.](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/Teradata-VantageTM-SQL-Functions-Expressions-and-Predicates-17.20/Aggregate-Functions/PIVOT)

```
PIVOT ( pivot_spec )
  [ WITH with_spec [,...] ]
  [AS] derived_table_name [ ( cname [,...] ) ]

pivot_spec := aggr_fn_spec [,...] FOR for_spec

aggr_fn_spec := aggr_fn ( cname ) [ [AS] pvt_aggr_alias ]

for_spec := { cname IN ( expr_spec_1 [,...] ) |
( cname [,...] ) IN ( expr_spec_2 [,...] ) |
cname IN ( subquery )
}

expr_spec_1 := expr [ [AS] expr_alias_name ]

expr_spec_2 := ( expr [,...] ) [ [AS] expr_alias_name ]

with_spec := aggr_fn ( { cname [,...] | * } ) [AS] aggr_alias
```

### Sample Source Patterns[¶](#id105)

#### Setup data[¶](#id106)

##### Teradata[¶](#id107)

##### Query[¶](#id108)

```
 CREATE TABLE star1(
	country VARCHAR(20),
	state VARCHAR(10),
	yr INTEGER,
	qtr VARCHAR(3),
	sales INTEGER,
	cogs INTEGER
);

insert into star1 values ('USA', 'CA', 2001, 'Q1', 30, 15);
insert into star1 values ('Canada', 'ON', 2001, 'Q2', 10, 0);
insert into star1 values ('Canada', 'BC', 2001, 'Q3', 10, 0);
insert into star1 values ('USA', 'NY', 2001, 'Q1', 45, 25);
insert into star1 values ('USA', 'CA', 2001, 'Q2', 50, 20);
```

##### _Snowflake_[¶](#id109)

##### Query[¶](#id110)

```
 CREATE OR REPLACE TABLE star1 (
	country VARCHAR(20),
	state VARCHAR(10),
	yr INTEGER,
	qtr VARCHAR(3),
	sales INTEGER,
	cogs INTEGER
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;

INSERT INTO star1
VALUES ('USA', 'CA', 2001, 'Q1', 30, 15);

INSERT INTO star1
VALUES ('Canada', 'ON', 2001, 'Q2', 10, 0);

INSERT INTO star1
VALUES ('Canada', 'BC', 2001, 'Q3', 10, 0);

INSERT INTO star1
VALUES ('USA', 'NY', 2001, 'Q1', 45, 25);

INSERT INTO star1
VALUES ('USA', 'CA', 2001, 'Q2', 50, 20);
```

#### Basic PIVOT transformation[¶](#basic-pivot-transformation)

##### _Teradata_[¶](#id111)

##### Query[¶](#id112)

```
 SELECT *
FROM star1 PIVOT (
	SUM(sales) FOR qtr
    IN ('Q1',
    	'Q2',
        'Q3')
)Tmp;
```

##### Result[¶](#id113)

```
Country | State | yr   | cogs | 'Q1' | 'Q2' | 'Q3' |
--------+-------+------+------+------+------+------+
Canada	| BC	| 2001 | 0    | null | null | 10   |
--------+-------+------+------+------+------+------+
USA 	| NY	| 2001 | 25   | 45   | null | null |
--------+-------+------+------+------+------+------+
Canada 	| ON 	| 2001 | 0    | null | 10   | null |
--------+-------+------+------+------+------+------+
USA 	| CA 	| 2001 | 20   | null | 50   | null |
--------+-------+------+------+------+------+------+
USA 	| CA 	| 2001 | 15   | 30   | null | null |
--------+-------+------+------+------+------+------+
```

##### _Snowflake_[¶](#id114)

##### Query[¶](#id115)

```
 SELECT
	*
FROM
	star1 PIVOT(
	SUM(sales) FOR qtr IN ('Q1',
	   	'Q2',
	       'Q3'))Tmp;
```

##### Result[¶](#id116)

```
Country | State | yr   | cogs | 'Q1' | 'Q2' | 'Q3' |
--------+-------+------+------+------+------+------+
Canada	| BC	| 2001 | 0    | null | null | 10   |
--------+-------+------+------+------+------+------+
USA 	| NY	| 2001 | 25   | 45   | null | null |
--------+-------+------+------+------+------+------+
Canada 	| ON 	| 2001 | 0    | null | 10   | null |
--------+-------+------+------+------+------+------+
USA 	| CA 	| 2001 | 20   | null | 50   | null |
--------+-------+------+------+------+------+------+
USA 	| CA 	| 2001 | 15   | 30   | null | null |
--------+-------+------+------+------+------+------+
```

#### PIVOT with aliases transformation[¶](#pivot-with-aliases-transformation)

##### _Teradata_[¶](#id117)

##### Query[¶](#id118)

```
 SELECT *
FROM star1 PIVOT (
	SUM(sales) as ss1 FOR qtr
    IN ('Q1' AS Quarter1,
    	'Q2' AS Quarter2,
        'Q3' AS Quarter3)
)Tmp;
```

##### Result[¶](#id119)

```
Country | State | yr   | cogs | Quarter1_ss1 | Quarter2_ss1 | Quarter3_ss1 |
--------+-------+------+------+--------------+--------------+--------------+
Canada	| BC	| 2001 | 0    | null 	     | null         | 10           |
--------+-------+------+------+--------------+--------------+--------------+
USA 	| NY	| 2001 | 25   | 45 	     | null 	    | null         |
--------+-------+------+------+--------------+--------------+--------------+
Canada 	| ON 	| 2001 | 0    | null 	     | 10 	    | null 	   |
--------+-------+------+------+--------------+--------------+--------------+
USA 	| CA 	| 2001 | 20   | null         | 50           | null         |
--------+-------+------+------+--------------+--------------+--------------+
USA 	| CA 	| 2001 | 15   | 30           | null         | null         |
--------+-------+------+------+--------------+--------------+--------------+
```

##### _Snowflake_[¶](#id120)

##### Query[¶](#id121)

```
 SELECT
	*
FROM
	!!!RESOLVE EWI!!! /*** SSC-EWI-0015 - PIVOT/UNPIVOT RENAME COLUMN NOT SUPPORTED ***/!!!
	star1 PIVOT(
	SUM(sales) FOR qtr IN (
	                       !!!RESOLVE EWI!!! /*** SSC-EWI-0015 - PIVOT/UNPIVOT RENAME COLUMN NOT SUPPORTED ***/!!!
	                       'Q1',
	!!!RESOLVE EWI!!! /*** SSC-EWI-0015 - PIVOT/UNPIVOT RENAME COLUMN NOT SUPPORTED ***/!!!
	   	'Q2',
	!!!RESOLVE EWI!!! /*** SSC-EWI-0015 - PIVOT/UNPIVOT RENAME COLUMN NOT SUPPORTED ***/!!!
	       'Q3'))Tmp;
```

##### Result[¶](#id122)

```
 Country | State | yr   | cogs | Quarter1_ss1 | Quarter2_ss1 | Quarter3_ss1 |
--------+-------+------+------+--------------+--------------+--------------+
Canada	| BC	| 2001 | 0    | null 	     | null         | 10           |
--------+-------+------+------+--------------+--------------+--------------+
USA 	| NY	| 2001 | 25   | 45 	     | null 	    | null         |
--------+-------+------+------+--------------+--------------+--------------+
Canada 	| ON 	| 2001 | 0    | null 	     | 10 	    | null 	   |
--------+-------+------+------+--------------+--------------+--------------+
USA 	| CA 	| 2001 | 20   | null         | 50           | null         |
--------+-------+------+------+--------------+--------------+--------------+
USA 	| CA 	| 2001 | 15   | 30           | null         | null         |
--------+-------+------+------+--------------+--------------+--------------+
```

### Known Issues[¶](#id123)

**1. WITH clause not supported**

Using the WITH clause is not currently supported.

**2. Pivot over multiple pivot columns not supported**

SnowConvert AI is transforming the PIVOT function into the PIVOT function in Snowflake, which only
supports applying the function over a single column.

**3. Pivot with multiple aggregate functions not supported**

The PIVOT function in Snowflake only supports applying one aggregate function over the data.

**4. Subquery in the IN clause not supported**

The IN clause of the Snowflake PIVOT function does not accept subqueries.

**5. Aliases only supported if all IN clause elements have it and table specification is present**

For the column names with aliases to be equivalent, SnowConvert AI requires that all the values
specified in the IN clause have one alias specified and the table specification is present in the
input code, this is necessary so SnowConvert AI can successfully create the alias list for the
resulting table.

### Related EWIs[¶](#id124)

1. [SSC-EWI-0015](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0015):
   The input pivot/unpivot statement form is not supported

## RANK[¶](#rank)

Translation specification for the transformation of the RANK() function

### Description[¶](#id125)

RANK sorts a result set and identifies the numeric rank of each row in the result. The only argument
for RANK is the sort column or columns, and the function returns an integer that represents the rank
of each row in the result.
([RANK in Teradata](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/SQL-Functions-Expressions-and-Predicates/Ordered-Analytical/Window-Aggregate-Functions/RANK-Teradata))

#### Teradata syntax[¶](#teradata-syntax)

```
 RANK ( sort_expression [ ASC | DESC ] [,...] )
```

#### Snowflake syntax[¶](#snowflake-syntax)

```
 RANK() OVER
(
    [ PARTITION BY <expr1> ]
    ORDER BY <expr2> [ { ASC | DESC } ]
    [ <window_frame> ]
)
```

### Sample Source Pattern[¶](#id126)

#### Setup data[¶](#id127)

##### Teradata[¶](#id128)

##### Query[¶](#id129)

```
 CREATE TABLE Sales (
  Product VARCHAR(255),
  Sales INT
);

INSERT INTO Sales (Product, Sales) VALUES ('A', 100);
INSERT INTO Sales (Product, Sales) VALUES ('B', 150);
INSERT INTO Sales (Product, Sales) VALUES ('C', 200);
INSERT INTO Sales (Product, Sales) VALUES ('D', 150);
INSERT INTO Sales (Product, Sales) VALUES ('E', 120);
INSERT INTO Sales (Product, Sales) VALUES ('F', NULL);
```

##### Snowflake[¶](#id130)

##### Query[¶](#id131)

```
 CREATE OR REPLACE TABLE Sales (
  Product VARCHAR(255),
  Sales INT
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;

INSERT INTO Sales (Product, Sales)
VALUES ('A', 100);

INSERT INTO Sales (Product, Sales)
VALUES ('B', 150);

INSERT INTO Sales (Product, Sales)
VALUES ('C', 200);

INSERT INTO Sales (Product, Sales)
VALUES ('D', 150);

INSERT INTO Sales (Product, Sales)
VALUES ('E', 120);

INSERT INTO Sales (Product, Sales)
VALUES ('F', NULL);
```

#### RANK() using ASC, DESC, and DEFAULT order[¶](#rank-using-asc-desc-and-default-order)

##### Teradata[¶](#id132)

Warning

Notice that Teradata’s ordering default value when calling RANK() is DESC. However, the default in
Snowflake is ASC. Thus, DESC is added in the conversion of RANK() when no order is specified.

##### Query[¶](#id133)

```
 SELECT
  Sales,
  RANK(Sales ASC) AS SalesAsc,
  RANK(Sales DESC) AS SalesDesc,
  RANK(Sales) AS SalesDefault
FROM
  Sales;
```

##### Result[¶](#id134)

<!-- prettier-ignore -->
|SALES|SALESASC|SALESDESC|SALESDEFAULT|
|---|---|---|---|
|NULL|6|6|6|
|200|5|1|1|
|150|3|2|2|
|120|2|4|4|
|100|1|5|5|

##### Snowflake[¶](#id135)

##### Query[¶](#id136)

```
 SELECT
  Sales,
  RANK() OVER (
  ORDER BY
    Sales ASC) AS SalesAsc,
    RANK() OVER (
    ORDER BY
    Sales DESC NULLS LAST) AS SalesDesc,
    RANK() OVER (
    ORDER BY
    Sales DESC NULLS LAST) AS SalesDefault
    FROM
    Sales;
```

##### Result[¶](#id137)

<!-- prettier-ignore -->
|SALES|SALESASC|SALESDESC|SALESDEFAULT|
|---|---|---|---|
|NULL|6|6|6|
|200|5|1|1|
|150|3|2|2|
|120|2|4|4|
|100|1|5|5|

### Known Issues [¶](#id138)

No issues were found.

### Related EWIs [¶](#id139)

No related EWIs.

## Regex functions[¶](#id140)

### Description[¶](#id141)

Both Teradata and Snowflake offer support for functions that apply regular expressions over varchar
inputs. See the
[Teradata documentation](https://docs.teradata.com/r/Teradata-VantageTM-SQL-Functions-Expressions-and-Predicates/March-2019/Regular-Expression-Functions)
and [Snowflake documentation](https://docs.snowflake.com/en/sql-reference/functions-regexp.html) for
more details.

```
REGEXP_SUBSTR(source. regexp [, position, occurrence, match])
REGEXP_REPLACE(source. regexp [, replace_string, position, occurrence, match])
REGEXP_INSTR(source. regexp [, position, occurrence, return_option, match])
REGEXP_SIMILAR(source. regexp [, match])
REGEXP_SPLIT_TO_TABLE(inKey. source. regexp, match)
```

### Sample Source Patterns[¶](#id142)

#### Setup data[¶](#id143)

##### Teradata[¶](#id144)

**Query**

```
CREATE TABLE regexpTable
(
    col1 CHAR(35)
);

INSERT INTO regexpTable VALUES('hola');
```

##### _Snowflake_[¶](#id145)

**Query**

```
CREATE OR REPLACE TABLE regexpTable
(
    col1 CHAR(35)
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;

INSERT INTO regexpTable
VALUES ('hola');
```

#### Regex transformation example[¶](#regex-transformation-example)

##### _Teradata_[¶](#id146)

**Query**

```
SELECT
REGEXP_REPLACE(col1,'.*(h(i|o))','ha', 1, 0, 'x'),
REGEXP_SUBSTR(COL1,'.*(h(i|o))', 2, 1, 'x'),
REGEXP_INSTR(COL1,'.*(h(i|o))',1, 1, 0, 'x'),
REGEXP_SIMILAR(COL1,'.*(h(i|o))', 'xl')
FROM regexpTable;
```

**Result**

```
COLUMN1|COLUMN2|COLUMN3|COLUMN4|
-------+-------+-------+-------+
hala   |null   |1      |0      |
```

##### _Snowflake_[¶](#id147)

**Query**

```
--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "regexpTable" **
SELECT
REGEXP_REPLACE(col1, '.*(h(i|o))', 'ha', 1, 0),
REGEXP_SUBSTR(COL1, '.*(h(i|o))', 2, 1),
REGEXP_INSTR(COL1, '.*(h(i|o))', 1, 1, 0),
--** SSC-FDM-TD0016 - VALUE 'l' FOR PARAMETER 'match_arg' IS NOT SUPPORTED IN SNOWFLAKE **
REGEXP_LIKE(COL1, '.*(h(i|o))')
FROM
regexpTable;
```

**Result**

```
COLUMN1|COLUMN2|COLUMN3|COLUMN4|
-------+-------+-------+-------+
hala   |null   |1      |FALSE  |
```

### Known Issues[¶](#id148)

**1. Snowflake only supports POSIX regular expressions**

The user will be warned when SnowConvert AI finds a non-POSIX regular expression.

**2. Teradata “match_arg” option ‘l’ is unsupported in Snowflake**

The option ‘l’ has no counterpart in Snowflake and the user will be warned if SnowConvert AI finds
them.

**3. Fixed size of the CHAR datatype may cause different behavior**

Some regex functions in Teradata will try to match the whole column of CHAR datatype in a table even
if some of the characters in the column were left empty due to a smaller string being inserted. In
Snowflake this does not happen because the CHAR datatype is of variable size.

**4. REGEXP_SPLIT_TO_TABLE not supported**

The function is currently not supported by Snowflake.

### Related EWIs[¶](#id149)

1. [SSC-FDM-0007](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0007):
   Element with missing dependencies.
2. [SSC-FDM-TD0016](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/teradataFDM#ssc-fdm-td0016):
   Value ‘l’ for parameter ‘match_arg’ is not supported in Snowflake.

## STRTOK_SPLIT_TO_TABLE[¶](#strtok-split-to-table)

### Description[¶](#id150)

Split a string into a table using the provided delimiters. For more information check
[STRTOK_SPLIT_TO_TABLE](https://docs.teradata.com/r/Teradata-VantageTM-SQL-Functions-Expressions-and-Predicates-17.20/String-Operators-and-Functions/STRTOK_SPLIT_TO_TABLE).

```
[TD_SYSFNLIB.] STRTOK_SPLIT_TO_TABLE ( inkey, instring, delimiters )
  RETURNS ( outkey, tokennum, token )
```

### Sample Source Patterns[¶](#id151)

#### Setup data[¶](#id152)

##### Teradata[¶](#id153)

**Query**

```
CREATE TABLE strtokTable
(
	col1 INTEGER,
	col2 VARCHAR(100)
);

INSERT INTO strtokTable VALUES(4, 'hello-world-split-me');
INSERT INTO strtokTable VALUES(1, 'string$split$by$dollars');
```

##### _Snowflake_[¶](#id154)

**Query**

```
CREATE OR REPLACE TABLE strtokTable
(
	col1 INTEGER,
	col2 VARCHAR(100)
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;

INSERT INTO strtokTable
VALUES (4, 'hello-world-split-me');

INSERT INTO strtokTable
VALUES (1, 'string$split$by$dollars');
```

#### STRTOK_SPLIT_TO_TABLE transformation[¶](#strtok-split-to-table-transformation)

##### _Teradata_[¶](#id155)

**Query**

```
SELECT outkey, tokennum, token FROM table(STRTOK_SPLIT_TO_TABLE(strtokTable.col1, strtokTable.col2, '-$')
RETURNS (outkey INTEGER, tokennum INTEGER, token VARCHAR(100))) AS testTable
ORDER BY outkey, tokennum;
```

**Result**

```
outkey |tokennum | token  |
-------+---------+--------+
1      |1        |string  |
-------+---------+--------+
1      |2        |split   |
-------+---------+--------+
1      |3        |by      |
-------+---------+--------+
1      |4        |dollars |
-------+---------+--------+
4      |1        |hello   |
-------+---------+--------+
4      |2        |world   |
-------+---------+--------+
4      |3        |split   |
-------+---------+--------+
4      |4        |me      |
```

##### _Snowflake_[¶](#id156)

**Query**

```
SELECT
CAST(strtokTable.col1 AS INTEGER) AS outkey,
CAST(INDEX AS INTEGER) AS tokennum,
CAST(VALUE AS VARCHAR) AS token
FROM
strtokTable,
table(STRTOK_SPLIT_TO_TABLE(strtokTable.col2, '-$')) AS testTable
ORDER BY outkey, tokennum;
```

**Result**

```
outkey |tokennum | token  |
-------+---------+--------+
1      |1        |string  |
-------+---------+--------+
1      |2        |split   |
-------+---------+--------+
1      |3        |by      |
-------+---------+--------+
1      |4        |dollars |
-------+---------+--------+
4      |1        |hello   |
-------+---------+--------+
4      |2        |world   |
-------+---------+--------+
4      |3        |split   |
-------+---------+--------+
4      |4        |me      |
```

### Known Issues[¶](#id157)

No known issues.

### Related EWIs [¶](#id158)

No related EWIs.

## SUBSTRING[¶](#substring)

### Description[¶](#id159)

Extracts a substring from a given input string. For more information check
[SUBSTRING/SUBSTR.](https://docs.teradata.com/r/kmuOwjp1zEYg98JsB8fu_A/lxOd~YrdVkJGt0_anAEXFQ)

```
SUBSTRING(string_expr FROM n1 [FOR n2])

SUBSTR(string_expr, n1, [, n2])
```

When the value to start getting the substring (n1) is less than one SUBSTR_UDF is inserted instead.

### Sample Source Patterns[¶](#id160)

#### SUBSTRING transformation[¶](#substring-transformation)

##### _Teradata_[¶](#id161)

**Query**

```
SELECT SUBSTR('Hello World!', 2, 6),
SUBSTR('Hello World!', -2, 6),
SUBSTRING('Hello World!' FROM 2 FOR 6),
SUBSTRING('Hello World!' FROM -2 FOR 6);
```

**Result**

```
COLUMN1 |COLUMN2 |COLUMN3 | COLUMN4 |
--------+--------+--------+---------+
ello W  |Hel     |ello W  |Hel      |
```

##### _Snowflake_[¶](#id162)

**Query**

```
SELECT
SUBSTR('Hello World!', 2, 6),
PUBLIC.SUBSTR_UDF('Hello World!', -2, 6),
SUBSTRING('Hello World!', 2, 6),
PUBLIC.SUBSTR_UDF('Hello World!', -2, 6);
```

**Result**

```
COLUMN1 |COLUMN2 |COLUMN3 | COLUMN4 |
--------+--------+--------+---------+
ello W  |Hel     |ello W  |Hel      |
```

### Related EWIs[¶](#id163)

No related EWIs.

## TD_UNPIVOT[¶](#td-unpivot)

Translation specification for the transformation of TD_UNPIVOT into an equivalent query in Snowflake

**Note:**

Some parts in the output code are omitted for clarity reasons.

### Description[¶](#id164)

`TD_UNPIVOT` in Teradata can unpivot multiple columns at once, while Snowflake `UNPIVOT` can only
unpivot a single column\*\*.\*\* The _unpivot_ functionality is used to transform columns of the
specified table into rows. For more information see
[TD_UNPIVOT](https://docs.teradata.com/r/Teradata-VantageTM-SQL-Operators-and-User-Defined-Functions-17.20/Table-Operators/TD_UNPIVOT).

```
[TD_SYSFNLIB.] TD_UNPIVOT (
  ON { tableName | ( query_expression ) }
  USING VALUE_COLUMNS ( 'value_columns_value' [,...] )
  UNPIVOT_COLUMN ( 'unpivot_column_value' )
  COLUMN_LIST ( 'column_list_value' [,...] )
  [ COLUMN_ALIAS_LIST ( 'column_alias_list_value' [,...] )
      INCLUDE_NULLS ( { 'No' | 'Yes' } )
  ]
)
```

The following transformation is able to generate a SQL query in Snowflake that unpivots multiple
columns at the same time, the same way it works in Teradata.

### Sample Source Patterns[¶](#id165)

#### Setup data title[¶](#setup-data-title)

##### Teradata[¶](#id166)

##### Query[¶](#id167)

```
 CREATE TABLE superunpivottest (
	myKey INTEGER NOT NULL PRIMARY KEY,
	firstSemesterIncome DECIMAL(10,2),
	secondSemesterIncome DECIMAL(10,2),
	firstSemesterExpenses DECIMAL(10,2),
	secondSemesterExpenses DECIMAL(10,2)
);

INSERT INTO superUnpivottest VALUES (2020, 15440, 25430.57, 10322.15, 12355.36);
INSERT INTO superUnpivottest VALUES (2018, 18325.25, 25220.65, 15560.45, 15680.33);
INSERT INTO superUnpivottest VALUES (2019, 23855.75, 34220.22, 14582.55, 24122);
```

##### _Snowflake_[¶](#id168)

##### Query[¶](#id169)

```
 CREATE OR REPLACE TABLE superunpivottest (
	myKey INTEGER NOT NULL PRIMARY KEY,
	firstSemesterIncome DECIMAL(10,2),
	secondSemesterIncome DECIMAL(10,2),
	firstSemesterExpenses DECIMAL(10,2),
	secondSemesterExpenses DECIMAL(10,2)
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;

INSERT INTO superUnpivottest
VALUES (2020, 15440, 25430.57, 10322.15, 12355.36);

INSERT INTO superUnpivottest
VALUES (2018, 18325.25, 25220.65, 15560.45, 15680.33);

INSERT INTO superUnpivottest
VALUES (2019, 23855.75, 34220.22, 14582.55, 24122);
```

#### TD_UNPIVOT transformation[¶](#td-unpivot-transformation)

##### _Teradata_[¶](#id170)

##### Query[¶](#id171)

```
 SELECT * FROM
 TD_UNPIVOT(
 	ON superunpivottest
 	USING
 	VALUE_COLUMNS('Income', 'Expenses')
 	UNPIVOT_COLUMN('Semester')
 	COLUMN_LIST('firstSemesterIncome, firstSemesterExpenses', 'secondSemesterIncome, secondSemesterExpenses')
    COLUMN_ALIAS_LIST('First', 'Second')
 )X ORDER BY mykey, Semester;
```

##### Result[¶](#id172)

```
myKey |Semester |Income   | Expenses |
------+---------+---------+----------+
2018  |First    |18325.25 |15560.45  |
------+---------+---------+----------+
2018  |Second   |25220.65 |15680.33  |
------+---------+---------+----------+
2019  |First    |23855.75 |14582.55  |
------+---------+---------+----------+
2019  |Second   |34220.22 |24122.00  |
------+---------+---------+----------+
2020  |First    |15440.00 |10322.15  |
------+---------+---------+----------+
2020  |Second   |25430.57 |12355.36  |
```

##### _Snowflake_[¶](#id173)

##### Query[¶](#id174)

```
 SELECT
 * FROM
 !!!RESOLVE EWI!!! /*** SSC-EWI-TD0061 - TD_UNPIVOT TRANSFORMATION REQUIRES COLUMN INFORMATION THAT COULD NOT BE FOUND, COLUMNS MISSING IN RESULT ***/!!!
 (
  SELECT
   TRIM(GET_IGNORE_CASE(OBJECT_CONSTRUCT('FIRSTSEMESTERINCOME', 'First', 'FIRSTSEMESTEREXPENSES', 'First', 'SECONDSEMESTERINCOME', 'Second', 'SECONDSEMESTEREXPENSES', 'Second'), Semester), '"') AS Semester,
   Income,
   Expenses
  FROM
   superunpivottest UNPIVOT(Income FOR Semester IN (
    firstSemesterIncome,
    secondSemesterIncome
   )) UNPIVOT(Expenses FOR Semester1 IN (
    firstSemesterExpenses,
    secondSemesterExpenses
   ))
  WHERE
   Semester = 'FIRSTSEMESTERINCOME'
   AND Semester1 = 'FIRSTSEMESTEREXPENSES'
   OR Semester = 'SECONDSEMESTERINCOME'
   AND Semester1 = 'SECONDSEMESTEREXPENSES'
 ) X ORDER BY mykey, Semester;
```

##### Result[¶](#id175)

```
myKey |Semester |Income   | Expenses |
------+---------+---------+----------+
2018  |First    |18325.25 |15560.45  |
------+---------+---------+----------+
2018  |Second   |25220.65 |15680.33  |
------+---------+---------+----------+
2019  |First    |23855.75 |14582.55  |
------+---------+---------+----------+
2019  |Second   |34220.22 |24122.00  |
------+---------+---------+----------+
2020  |First    |15440.00 |10322.15  |
------+---------+---------+----------+
2020  |Second   |25430.57 |12355.36  |
```

### Known Issues[¶](#id176)

1. **TD_UNPIVOT with INCLUDE_NULLS clause set to YES is not supported**

Snowflake UNPIVOT function used in the transformation will ignore null values always, and the user
will be warned that the INCLUDE_NULLS clause is not supported when it is set to YES.

2. **Table information is required to correctly transform the function**

SnowConvert AI needs the name of the columns that are being used in the TD_UNPIVOT function; if the
user does not include the columns list in the query_expression of the function but provides the name
of the table being unpivoted, then it will try to retrieve the column names from the table
definition. If the names can not be found then the user will be warned that the resulting query
might be losing columns in the result.

### Related EWIs[¶](#id177)

1. [SSC-EWI-TD0061](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/teradataEWI#ssc-ewi-td0061):
   TD_UNPIVOT transformation requires column information that could not be found, columns missing in
   result.

## TO_CHAR[¶](#to-char)

### Description[¶](#id178)

The TO_CHAR function casts a DateTime or numeric value to a string. For more information check
[TO_CHAR(Numeric)](https://docs.teradata.com/r/kmuOwjp1zEYg98JsB8fu_A/4xbLyOA_385QLYctkj~hjw) and
[TO_CHAR(DateTime)](https://docs.teradata.com/r/kmuOwjp1zEYg98JsB8fu_A/he2a_fFPveMN9cjMlF3Tqg).

```
-- Numeric version
[TD_SYSFNLIB.]TO_CHAR(numeric_expr [, format_arg [, nls_param]])

-- DateTime version
[TD_SYSFNLIB.]TO_CHAR(dateTime_expr [, format_arg])
```

Both Snowflake and Teradata have their own version of the TO_CHAR function, however, Teradata
supports plenty of formats that are not natively supported by Snowflake. To support these format
elements SnowConvert AI uses Snowflake built-in functions and custom UDFs to generate a
concatenation expression that produces the same string as the original TO_CHAR function in Teradata.

### Sample Source Patterns[¶](#id179)

#### TO_CHAR(DateTime) transformation[¶](#to-char-datetime-transformation)

##### _Teradata_[¶](#id180)

**Query**

```
SELECT
TO_CHAR(date '2012-12-23'),
TO_CHAR(date '2012-12-23', 'DS'),
TO_CHAR(date '2012-12-23', 'DAY DD, MON YY');
```

**Result**

```
COLUMN1    | COLUMN2    | COLUMN3           |
-----------+------------+-------------------+
2012/12/23 | 12/23/2012 | SUNDAY 23, DEC 12 |
```

##### _Snowflake_[¶](#id181)

**Query**

```
SELECT
TO_CHAR(date '2012-12-23') /*** SSC-FDM-TD0029 - SNOWFLAKE SUPPORTED FORMATS FOR TO_CHAR DIFFER FROM TERADATA AND MAY FAIL OR HAVE DIFFERENT BEHAVIOR ***/,
TO_CHAR(date '2012-12-23', 'MM/DD/YYYY') /*** SSC-FDM-TD0029 - SNOWFLAKE SUPPORTED FORMATS FOR TO_CHAR DIFFER FROM TERADATA AND MAY FAIL OR HAVE DIFFERENT BEHAVIOR ***/,
PUBLIC.DAYNAME_LONG_UDF(date '2012-12-23', 'uppercase') || TO_CHAR(date '2012-12-23', ' DD, ') || PUBLIC.MONTH_SHORT_UDF(date '2012-12-23', 'uppercase') || TO_CHAR(date '2012-12-23', ' YY') /*** SSC-FDM-TD0029 - SNOWFLAKE SUPPORTED FORMATS FOR TO_CHAR DIFFER FROM TERADATA AND MAY FAIL OR HAVE DIFFERENT BEHAVIOR ***/;
```

**Result**

```
COLUMN1    | COLUMN2    | COLUMN3           |
-----------+------------+-------------------+
2012/12/23 | 12/23/2012 | SUNDAY 23, DEC 12 |
```

#### TO_CHAR(Numeric) transformation[¶](#to-char-numeric-transformation)

##### _Teradata_[¶](#id182)

**Query**

```
SELECT
TO_CHAR(1255.495),
TO_CHAR(1255.495, '9.9EEEE'),
TO_CHAR(1255.495, 'SC9999.9999', 'nls_iso_currency = ''EUR''');
```

**Result**

```
COLUMN1  | COLUMN2 | COLUMN3       |
---------+---------+---------------+
1255.495 | 1.3E+03 | +EUR1255.4950 |
```

##### _Snowflake_[¶](#id183)

**Query**

```
SELECT
TO_CHAR(1255.495) /*** SSC-FDM-TD0029 - SNOWFLAKE SUPPORTED FORMATS FOR TO_CHAR DIFFER FROM TERADATA AND MAY FAIL OR HAVE DIFFERENT BEHAVIOR ***/,
TO_CHAR(1255.495, '9.0EEEE') /*** SSC-FDM-TD0029 - SNOWFLAKE SUPPORTED FORMATS FOR TO_CHAR DIFFER FROM TERADATA AND MAY FAIL OR HAVE DIFFERENT BEHAVIOR ***/,
PUBLIC.INSERT_CURRENCY_UDF(TO_CHAR(1255.495, 'S9999.0000'), 2, 'EUR') /*** SSC-FDM-TD0029 - SNOWFLAKE SUPPORTED FORMATS FOR TO_CHAR DIFFER FROM TERADATA AND MAY FAIL OR HAVE DIFFERENT BEHAVIOR ***/;
```

**Result**

```
COLUMN1  | COLUMN2 | COLUMN3       |
---------+---------+---------------+
1255.495 | 1.3E+03 | +EUR1255.4950 |
```

### Known Issues[¶](#id184)

**1. Formats with different or unsupported behaviors**

Teradata offers an extensive list of format elements that may show different behavior in Snowflake
after the transformation of the TO_CHAR function. For the list of elements with different or
unsupported behaviors check
[SSC-EWI-TD0029](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/teradataEWI#ssc-ewi-td0029).

### Related EWIs[¶](#id185)

1. [SSC-FDM-TD0029](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/teradataFDM#ssc-fdm-td0029):
   Snowflake supported formats for TO_CHAR differ from Teradata and may fail or have different
   behavior.

## XMLAGG[¶](#xmlagg)

### Description[¶](#id186)

Construct an XML value by performing an aggregation of multiple rows. For more information check
[XMLAGG](https://docs.teradata.com/r/Teradata-VantageTM-XML-Data-Type/June-2020/Functions-for-XML-Type-and-XQuery/XMLAGG).

```
XMLAGG (
  XML_value_expr
  [ ORDER BY order_by_spec [,...] ]
  [ RETURNING { CONTENT | SEQUENCE } ]
)

order_by_spec := sort_key [ ASC | DESC ] [ NULLS { FIRST | LAST } ]
```

### Sample Source Patterns[¶](#id187)

#### Setup data[¶](#id188)

##### Teradata[¶](#id189)

**Query**

```
create table orders (
	o_orderkey int,
	o_totalprice float);

insert into orders values (1,500000);
insert into orders values (2,100000);
insert into orders values (3,600000);
insert into orders values (4,700000);
```

##### _Snowflake_[¶](#id190)

**Query**

```
CREATE OR REPLACE TABLE orders (
	o_orderkey int,
	o_totalprice float)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;

INSERT INTO orders
VALUES (1,500000);

INSERT INTO orders
VALUES (2,100000);

INSERT INTO orders
VALUES (3,600000);

INSERT INTO orders
VALUES (4,700000);
```

#### XMLAGG transformation[¶](#xmlagg-transformation)

##### _Teradata_[¶](#id191)

**Query**

```
select
    xmlagg(o_orderkey order by o_totalprice desc) (varchar(10000))
from orders
where o_totalprice > 5;
```

**Result**

```
COLUMN1 |
--------+
4 3 1 2 |
```

##### _Snowflake_[¶](#id192)

**Query**

```
SELECT
    LEFT(TO_VARCHAR(LISTAGG ( o_orderkey, ' ')
    WITHIN GROUP(
 order by o_totalprice DESC NULLS LAST)), 10000)
    from
    orders
    where o_totalprice > 5;
```

**Result**

```
COLUMN1 |
--------+
4 3 1 2 |
```

### Known Issues[¶](#id193)

**1. The RETURNING clause is currently not supported.**

The user will be warned that the translation of the returning clause will be added in the future.

### Related EWIs [¶](#id194)

No related EWIs.

## CAST[¶](#cast)

## Cast from Number Datatypes to Varchar Datatype[¶](#cast-from-number-datatypes-to-varchar-datatype)

Teradata when casts to varchar uses default formats for each number datatype, so SnowConvert AI adds
formats to keep the equivalence among platforms.

### Sample Source Patterns[¶](#id195)

#### BYTEINT[¶](#byteint)

##### _Teradata_[¶](#id196)

**Query**

```
SELECT '"'||cast(cast(12 as BYTEINT) as varchar(10))||'"';
```

**Result**

```
(('"'||12)||'"')|
----------------+
"12"            |
```

##### _Snowflake_[¶](#id197)

**Query**

```
SELECT
'"'|| LEFT(TO_VARCHAR(cast(12 as BYTEINT), 'TM'), 10) ||'"';
```

**Result**

```
"'""'|| LEFT(TO_VARCHAR(CAST(12 AS BYTEINT), 'TM'), 10) ||'""'"
---------------------------------------------------------------
"12"
```

#### SMALLINT[¶](#smallint)

##### _Teradata_[¶](#id198)

**Query**

```
SELECT '"'||cast(cast(123 as SMALLINT) as varchar(10))||'"';
```

**Result**

```
(('"'||123)||'"')|
-----------------+
"123"            |
```

##### _Snowflake_[¶](#id199)

**Query**

```
SELECT
'"'|| LEFT(TO_VARCHAR(CAST(123 AS SMALLINT), 'TM'), 10) ||'"';
```

**Result**

```
"'""'|| LEFT(TO_VARCHAR(CAST(123 AS SMALLINT), 'TM'), 10) ||'""'"
-----------------------------------------------------------------
"123"
```

#### INTEGER[¶](#integer)

##### _Teradata_[¶](#id200)

**Query**

```
SELECT '"'||cast(cast(12345 as INTEGER) as varchar(10))||'"';
```

**Result**

```
(('"'||12345)||'"')|
-------------------+
"12345"            |
```

##### _Snowflake_[¶](#id201)

**Query**

```
SELECT
'"'|| LEFT(TO_VARCHAR(CAST(12345 AS INTEGER), 'TM'), 10) ||'"';
```

**Result**

```
"'""'|| LEFT(TO_VARCHAR(CAST(12345 AS INTEGER), 'TM'), 10) ||'""'"
------------------------------------------------------------------
"12345"
```

#### BIGINT[¶](#bigint)

##### _Teradata_[¶](#id202)

**Query**

```
SELECT '"'||cast(cast(12345 as BIGINT) as varchar(10))||'"';
```

**Result**

```
(('"'||12345)||'"')|
-------------------+
"12345"            |
```

##### _Snowflake_[¶](#id203)

**Query**

```
SELECT
       '"'|| LEFT(TO_VARCHAR(CAST(12345 AS BIGINT), 'TM'), 10) ||'"';
```

**Result**

```
"'""'|| LEFT(TO_VARCHAR(CAST(12345 AS BIGINT), 'TM'), 10) ||'""'"
-----------------------------------------------------------------
"12345"
```

#### DECIMAL[(n[,m])] or NUMERIC[(n[,m])][¶](#decimal-n-m-or-numeric-n-m)

##### _Teradata_[¶](#id204)

**Query**

```
SELECT '"'||cast(cast(12345 as DECIMAL) as varchar(10))||'"',
       '"'||cast(cast(12345 as DECIMAL(12, 2)) as varchar(10))||'"';
```

**Result**

```
(('"'||12345)||'"')|(('"'||12345)||'"')|
-------------------+-------------------+
"12345."           |"12345.00"         |
```

##### _Snowflake_[¶](#id205)

**Query**

```
SELECT
'"'|| LEFT(TO_VARCHAR(CAST(12345 AS DECIMAL), 'TM.'), 10) ||'"',
'"'|| LEFT(TO_VARCHAR(CAST(12345 AS DECIMAL(12, 2)), 'TM'), 10) ||'"';
```

**Result**

```
'"'|| LEFT(TO_VARCHAR(CAST(12345 AS DECIMAL), 'TM.'), 10) ||'"'	'"'|| LEFT(TO_VARCHAR(CAST(12345 AS DECIMAL(12, 2)), 'TM'), 10) ||'"'
"12345."	"12345.00"
```

### Known Issues [¶](#id206)

- Teradata treats the numbers between 0 and 1 differently than Snowflake. For those values, Teradata
  does not add the zero before the dot; meanwhile, Snowflake does.

#### _Teradata_[¶](#id207)

**Query**

```
SELECT '"'||cast(cast(-0.1 as DECIMAL(12, 2)) as varchar(10))||'"' AS column1,
       '"'||cast(cast(0.1 as DECIMAL(12, 2)) as varchar(10))||'"' AS column2;
```

**Result**

```
COLUMN1          |COLUMN2
-----------------+--------------+
"-.10"           |".10"         |
```

#### _Snowflake_[¶](#id208)

**Query**

```
SELECT
'"'|| LEFT(TO_VARCHAR(CAST(-0.1 AS DECIMAL(12, 2)), 'TM'), 10) ||'"' AS column1,
'"'|| LEFT(TO_VARCHAR(CAST(0.1 AS DECIMAL(12, 2)), 'TM'), 10) ||'"' AS column2;
```

**Result**

```
COLUMN1           |COLUMN2
------------------+---------------+
"-0.10"           |"0.10"         |
```

### Related EWIs [¶](#id209)

No related EWIs.

## Cast to DATE using { }[¶](#cast-to-date-using)

### Description[¶](#id210)

The following syntax casts a date-formatted string to DATE datatype by putting a d before the string
definition inside curly braces.

```
SELECT {d '1233-10-10'}
```

### Sample Source Patterns[¶](#id211)

#### Cast to DATE using curly braces[¶](#cast-to-date-using-curly-braces)

**Teradata**

**Cast to Date**

```
SELECT * FROM RESOURCE_DETAILS where change_ts >= {d '2022-09-10'};
```

**Snowflake**

**Cast to Date**

```
SELECT
* FROM
PUBLIC.RESOURCE_DETAILS
where change_ts >= DATE('2022-09-10');
```

## Cast to INTERVAL datatype[¶](#cast-to-interval-datatype)

### Description[¶](#id212)

Snowflake does not support the Interval data type, but it has INTERVAL constants that can be used in
DateTime operations and other uses can be emulated using VARCHAR, SnowConvert AI will transform CAST
functions to the INTERVAL datatype into an equivalent depending on the case:

- When the value being casted is of type interval an UDF will be generated to produce the new
  interval equivalent as a string
- When the value is a literal, an Snowflake interval constant will be generated if the cast is used
  in a datetime operation, otherwise a literal string will be generated
- When the value is non-literal then a cast to string will be generated

### Sample Source Patterns[¶](#id213)

#### Non-interval literals[¶](#non-interval-literals)

##### _Teradata_[¶](#id214)

**Query**

```
SELECT TIMESTAMP '2022-10-15 10:30:00' + CAST ('12:34:56.78' AS INTERVAL HOUR(2) TO SECOND(2)) AS VARCHAR_TO_INTERVAL,
TIMESTAMP '2022-10-15 10:30:00' + CAST(-5 AS INTERVAL YEAR(4)) AS NUMBER_TO_INTERVAL,
CAST('07:00' AS INTERVAL HOUR(2) TO MINUTE) AS OUTSIDE_DATETIME_OPERATION;
```

**Result**

```
VARCHAR_TO_INTERVAL | NUMBER_TO_INTERVAL | OUTSIDE_DATETIME_OPERATION |
--------------------+--------------------+----------------------------+
2022-10-15 23:04:56 |2017-10-15 10:30:00 | 7:00                       |
```

##### _Snowflake_[¶](#id215)

**Query**

```
SELECT
TIMESTAMP '2022-10-15 10:30:00' + INTERVAL '12 HOUR, 34 MINUTE, 56 SECOND, 780000 MICROSECOND' AS VARCHAR_TO_INTERVAL,
TIMESTAMP '2022-10-15 10:30:00' + INTERVAL '-5 YEAR' AS NUMBER_TO_INTERVAL,
'07:00' AS OUTSIDE_DATETIME_OPERATION;
```

**Result**

```
VARCHAR_TO_INTERVAL     | NUMBER_TO_INTERVAL     | OUTSIDE_DATETIME_OPERATION |
------------------------+------------------------+----------------------------+
2022-10-15 23:04:56.780 |2017-10-15 10:30:00.000 | 07:00                      |
```

#### Non-literal and non-interval values[¶](#non-literal-and-non-interval-values)

##### _Teradata_[¶](#id216)

**Query**

```
SELECT TIMESTAMP '2022-10-15 10:30:00' + CAST('20 ' || '10' AS INTERVAL DAY TO HOUR) AS DATETIME_OPERATION,
CAST('20 ' || '10' AS INTERVAL DAY TO HOUR) AS OUTSIDE_DATETIME_OPERATION;
```

**Result**

```
DATETIME_OPERATION  | OUTSIDE_DATETIME_OPERATION |
--------------------+----------------------------+
2022-11-04 20:30:00 | 20 10                      |
```

##### _Snowflake_[¶](#id217)

**Query**

```
SELECT
PUBLIC.DATETIMEINTERVALADD_UDF(TIMESTAMP '2022-10-15 10:30:00', CAST('20 ' || '10' AS VARCHAR(21)), 'DAY', '+') AS DATETIME_OPERATION,
CAST('20 ' || '10' AS VARCHAR(21)) AS OUTSIDE_DATETIME_OPERATION;
```

**Result**

```
DATETIME_OPERATION      | OUTSIDE_DATETIME_OPERATION |
------------------------+----------------------------+
2022-11-04 20:30:00.000 | 20 10                      |
```

#### Cast of interval to another interval[¶](#cast-of-interval-to-another-interval)

##### _Teradata_[¶](#id218)

**Query**

```
SELECT
TIMESTAMP '2022-10-15 10:30:00' + CAST(INTERVAL '5999' MINUTE AS INTERVAL DAY TO HOUR) AS DATETIME_OPERATION,
CAST(INTERVAL '5999' MINUTE AS INTERVAL DAY TO HOUR) AS OUTSIDE_DATETIME_OPERATION;
```

**Result**

```
DATETIME_OPERATION  | OUTSIDE_DATETIME_OPERATION |
--------------------+----------------------------+
2022-10-19 13:30:00 | 4 03                       |
```

##### _Snowflake_[¶](#id219)

**Query**

```
SELECT
PUBLIC.DATETIMEINTERVALADD_UDF(
TIMESTAMP '2022-10-15 10:30:00', PUBLIC.INTERVALTOINTERVAL_UDF('5999', 'MINUTE', 'MINUTE', 'DAY', 'HOUR'), 'DAY', '+') AS DATETIME_OPERATION,
PUBLIC.INTERVALTOINTERVAL_UDF('5999', 'MINUTE', 'MINUTE', 'DAY', 'HOUR') AS OUTSIDE_DATETIME_OPERATION;
```

**Result**

```
DATETIME_OPERATION      | OUTSIDE_DATETIME_OPERATION |
------------------------+----------------------------+
2022-10-19 13:30:00.000 | 4 03                       |
```

### Known Issues[¶](#id220)

**No known issues.**

### Related EWIs[¶](#id221)

No related EWIs.
