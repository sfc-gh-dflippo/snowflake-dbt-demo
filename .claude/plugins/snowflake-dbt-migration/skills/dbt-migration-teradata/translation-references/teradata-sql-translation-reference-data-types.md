---
description: This section shows equivalents between data types in Teradata and in Snowflake.
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/teradata/sql-translation-reference/data-types
title: SnowConvert AI - Teradata - Data Types | Snowflake Documentation
---

## Conversion Table

<!-- prettier-ignore -->
|Teradata|Snowflake|Notes|
|---|---|---|---|---|
|`ARRAY`|`ARRAY`||
|`BIGINT`|`BIGINT`|`BIGINT`in Snowflake is an alias for `NUMBER(38,0).`[Check out [note](#integer-data-types)]|
|`BLOB`|`BINARY`|Limited to 8MB. `BLOB`is not supported, warning [SSC-FDM-TD0001](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/teradataFDM#ssc-fdm-td0001) is generated|
|`BYTE`|`BINARY`||
|`BYTEINT`|`BYTEINT`||
|`CHAR`|`CHAR`||
|`CLOB`|`VARCHAR`|​Limited to 16MB. `CLOB`is not supported, warning [SSC-FDM-TD0002](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/teradataFDM#ssc-fdm-td0002) is generated|
|`DATE`|`DATE`||
|`DECIMAL`|`DECIMAL`||
|`DOUBLE PRECISION`|`DOUBLE PRECISION`||
|`FLOAT`|`FLOAT`||
|`INTEGER`|`INTEGER`|`INTEGER`in Snowflake is an alias for `NUMBER(38,0)`. [Check out [note](#integer-data-types)]|
|`INTERVAL DAY [TO HOUR|MINUTE|SECOND]`|`VARCHAR(20)`|​Intervals are stored as`VARCHAR`in Snowflake except when used in addition/subtraction. [Check out [note](#integer-data-types)].|
|`INTERVAL HOUR [TO MINUTE|SECOND]`|`VARCHAR(20)`|​Intervals are stored as`VARCHAR`in Snowflake except when used in addition/subtraction. [Check out [note](#integer-data-types)].|
|`INTERVAL MINUTE [TO SECOND]`|`VARCHAR(20)`|​Intervals are stored as`VARCHAR`in Snowflake except when used in addition/subtraction. [Check out [note](#integer-data-types)].|
|`INTERVAL SECOND`|`VARCHAR(20)`|​Intervals are stored as`VARCHAR`in Snowflake except when used in addition/subtraction. [Check out [note](#integer-data-types)].|
|`INTERVAL YEAR [TO SECOND]`|`VARCHAR(20)`|​Intervals are stored as`VARCHAR`in Snowflake except when used in addition/subtraction. [Check out [note](#integer-data-types)].|
|`JSON`|`VARIANT`|Elements inside a JSON are ordered by their keys when inserted in a table. [Check out [note](data-types.md#json-data-type)].|
|`MBR`|`---`|Not supported|
|`NUMBER`|`NUMBER(38, 18)`||
|`PERIOD(DATE)`|`VARCHAR(24)`|Periods are stored as`VARCHAR`in Snowflake. [Check out [note](#integer-data-types)].|
|`PERIOD(TIME)`|`VARCHAR(34)`|Periods are stored as`VARCHAR`in Snowflake. [Check out [note](#integer-data-types)].|
|`PERIOD(TIME WITH TIME ZONE)`|`VARCHAR(46)`|Periods are stored as`VARCHAR`in Snowflake. [Check out [note](#integer-data-types)].|
|`PERIOD(TIMESTAMP)`|`VARCHAR(58)`|Periods are stored as`VARCHAR`in Snowflake. [Check out [note](#integer-data-types)].|
|`PERIOD(TIMESTAMP WITH TIME ZONE)`|`VARCHAR(58)`|Periods are stored as`VARCHAR`in Snowflake. [Check out [note](#integer-data-types)].|
|`REAL`|`REAL`||
|`SMALLINT`|`​SMALLINT`​|`SMALLINT` in Snowflake is an alias for `NUMBER(38,0).` [Check out [note](#integer-data-types)]|
|`ST_GEOMETRY`|`GEOGRAPHY`||
|`TIME`|`TIME`||
|`TIME WITH TIME ZONE`|`TIME`|Warning [SSC-FDM-0005](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0005) is generated.|
|`TIMESTAMP`|`TIMESTAMP`||
|`TIMESTAMP WITH TIME ZONE`|`TIMESTAMP_TZ`||
|`VARBYTE`|`BINARY`||
|`VARCHAR`|`VARCHAR`||
|`XML`|`VARIANT`|​|

## Notes

### Note

See the documentation on Teradata
[data types](https://docs.teradata.com/reader/~_sY_PYVxZzTnqKq45UXkQ/I_xWuywcishQ9U3Xal6zjA)

### Integer Data Types

For the conversion of integer data types (`INTEGER`, `SMALLINT`, and `BIGINT`), each one is
converted to the alias in Snowflake with the same name. Each of those aliases converts to
`NUMBER(38,0)`, a data type that is considerably larger than the integer datatype. Below is a
comparison of the range of values that can be present in each data type:

- Teradata `INTEGER`: -2,147,483,648 to 2,147,483,647
- Teradata `SMALLINT`: -32768 to 32767
- Teradata `BIGINT`: -9,223,372,036,854,775,808 to 9,223,372,036,854,775,807
- Snowflake `NUMBER(38,0)`: -99999999999999999999999999999999999999 to
  +99999999999999999999999999999999999999

Warning
[SSC-EWI-0036](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0036)
is generated.

### Interval/Period Data Types

Intervals and Periods are stored as a string (`VARCHAR`) in Snowflake. When converting, SnowConvert
AI creates a UDF that recreates the same expression as a string. Warning
[SSC-EWI-TD0053](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/teradataEWI#ssc-ewi-td0053)
is generated.

You can see more of the UDF’s in the public repository of UDF’s currently created by Snowflake
SnowConvert.

These UDF’s assume that periods are stored in a `VARCHAR` where the data/time parts are separated by
an `*`. For example for a Teradata period like `PERIOD('2018-01-01','2018-01-20')` it should be
stored in Snowflake as a `VARCHAR` like `'2018-01-01`\*`2018-01-20'`.

The only exception to the `VARCHAR` transformation for intervals are interval literals used to
add/subtract values from a Datetime expression, Snowflake does not have an `INTERVAL` datatype but
[interval constants](https://docs.snowflake.com/en/sql-reference/data-types-datetime.html#interval-constants)
exist for the specific purpose mentioned. Examples:

Input code:

```sql
 SELECT TIMESTAMP '2018-05-13 10:30:45' + INTERVAL '10 05:30' DAY TO MINUTE;
```

Output code:

```sql
 SELECT
TIMESTAMP '2018-05-13 10:30:45' + INTERVAL '10 DAY, 05 HOUR, 30 MINUTE';
```

Cases where the interval is being multiplied/divided by a numerical expression are transformed to
equivalent `DATEADD` function calls instead:

Input code:

```sql
 SELECT TIME '03:45:15' - INTERVAL '15:32:01' HOUR TO SECOND * 10;
```

Output code:

```sql
 SELECT
DATEADD('SECOND', 10 * -1, DATEADD('MINUTE', 10 * -32, DATEADD('HOUR', 10 * -15, TIME '03:45:15')));
```

### JSON Data Type

Elements inside a JSON are ordered by their keys when inserted in a table. Thus, the query results
might differ. However, this does not affect the order of arrays inside the JSON.

For example, if the original JSON is:

```sql
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

```sql
 {
   "age": 31,
   "cities": ["Los Angeles", "Lima", "Buenos Aires"],
   "firstName": "Peter",
   "lastName": "Andre"
}
```

Note how “age” is now the first element. However, the array of “cities” maintains its original
order.

## Known Issues

No issues were found.

## Related EWIs

No related EWIs.
