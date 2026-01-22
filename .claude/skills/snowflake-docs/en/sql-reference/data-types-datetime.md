---
auto_generated: true
description: Snowflake supports data types for managing dates, times, and timestamps
  (combined date + time). Snowflake also supports formats for string constants used
  in manipulating dates, times, and timestamps.
last_scraped: '2026-01-14T16:55:46.743670+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/data-types-datetime
title: Date & time data types | Snowflake Documentation
---

1. [Overview](../reference.md)
2. [SQL data types reference](../sql-reference-data-types.md)

   * [Summary](intro-summary-data-types.md)
   * [Numeric](data-types-numeric.md)
   * [String & binary](data-types-text.md)
   * [Logical](data-types-logical.md)
   * [Date & time](data-types-datetime.md)

     + [Input and output formats](date-time-input-output.md)
     + [Working with date and time values](date-time-examples.md)
   * [Semi-structured](data-types-semistructured.md)
   * [Structured](data-types-structured.md)
   * [Unstructured](data-types-unstructured.md)
   * [Geospatial](data-types-geospatial.md)
   * [Vector](data-types-vector.md)
   * [Unsupported](data-types-unsupported.md)
   * [Conversion](data-type-conversion.md)
3. [SQL command reference](../sql-reference-commands.md)
4. [Function and stored procedure reference](../sql-reference-functions.md)
5. [Class reference](../sql-reference-classes.md)
6. [Scripting reference](../sql-reference-snowflake-scripting.md)
7. [General reference](../sql-reference.md)
8. [API reference](../api-reference.md)

[Reference](../reference.md)[SQL data types reference](../sql-reference-data-types.md)Date & time

# Date & time data types[¶](#date-time-data-types "Link to this heading")

Snowflake supports data types for managing dates, times, and timestamps (combined date + time). Snowflake also supports formats for
string constants used in manipulating dates, times, and timestamps.

## Data types[¶](#data-types "Link to this heading")

Snowflake supports the following date and time data types:

* [DATE](#label-datatypes-date)
* [DATETIME](#label-datatypes-datetime)
* [TIME](#label-datatypes-time)
* [TIMESTAMP\_LTZ , TIMESTAMP\_NTZ , TIMESTAMP\_TZ](#label-datatypes-timestamp-variations)

Note

For DATE and TIMESTAMP data, Snowflake recommends using years between 1582 and 9999. Snowflake accepts some
years outside this range, but years prior to 1582 should be avoided due to
[limitations on the Gregorian Calendar](#label-date-types-datetime-supported-calendar).

### DATE[¶](#date "Link to this heading")

Snowflake supports a single DATE data type for storing dates (with no time elements).

DATE accepts dates in the most common forms (`YYYY-MM-DD`, `DD-MON-YYYY`, and so on).

In addition, all accepted TIMESTAMP values are valid inputs for dates, but the TIME information is truncated.

### DATETIME[¶](#datetime "Link to this heading")

DATETIME is synonymous with TIMESTAMP\_NTZ.

### TIME[¶](#time "Link to this heading")

Snowflake supports a single TIME data type for storing times in the form of `HH:MI:SS`.

TIME supports an optional precision parameter for fractional seconds (for example, `TIME(3)`).
Time precision can range from 0 (seconds) to 9 (nanoseconds). The default precision is 9.

All TIME values must be between `00:00:00` and `23:59:59.999999999`. TIME internally stores “wallclock” time, and all operations on TIME values are performed
without taking any time zone into consideration.

### TIMESTAMP\_LTZ , TIMESTAMP\_NTZ , TIMESTAMP\_TZ[¶](#timestamp-ltz-timestamp-ntz-timestamp-tz "Link to this heading")

Snowflake supports three variations of timestamp.

TIMESTAMP\_LTZ:
:   TIMESTAMP\_LTZ internally stores UTC values with a specified precision. However, all operations are performed in the current session’s time zone, controlled by the
    [TIMEZONE](parameters.html#label-timezone) session parameter.

    Synonymous with TIMESTAMP\_LTZ:

    * TIMESTAMPLTZ
    * TIMESTAMP WITH LOCAL TIME ZONE

TIMESTAMP\_NTZ:
:   TIMESTAMP\_NTZ internally stores “wallclock” time with a specified precision. All operations are performed without taking any time zone into account.

    If the output format contains a time zone, the UTC indicator (`Z`) is displayed.

    TIMESTAMP\_NTZ is the default for TIMESTAMP.

    Synonymous with TIMESTAMP\_NTZ:

    * TIMESTAMPNTZ
    * TIMESTAMP WITHOUT TIME ZONE
    * DATETIME

TIMESTAMP\_TZ:
:   TIMESTAMP\_TZ internally stores UTC values together with an associated *time zone offset*. When a time zone isn’t provided, the session time zone offset is used. All
    operations are performed with the time zone offset specific to each record.

    Synonymous with TIMESTAMP\_TZ:

    * TIMESTAMPTZ
    * TIMESTAMP WITH TIME ZONE

    TIMESTAMP\_TZ values are compared based on their times in UTC. For example, the following comparison between
    different times in different timezones returns TRUE because the two values have equivalent times in UTC.

    ```
    SELECT '2024-01-01 00:00:00 +0000'::TIMESTAMP_TZ = '2024-01-01 01:00:00 +0100'::TIMESTAMP_TZ;
    ```

    Copy

Attention

TIMESTAMP\_TZ currently only stores the *offset* of a given time zone, not the actual *time zone*, at the moment of creation for a given value. This is especially
important for daylight saving time, which is not utilized by UTC.

For example, with the [TIMEZONE](parameters.html#label-timezone) parameter set to `"America/Los_Angeles"`, converting a value to TIMESTAMP\_TZ in January of a given year stores the
time zone offset of `-0800`. If six months are later added to the value, the `-0800` offset is retained, even though in July the offset for Los Angeles is
`-0700`. This is because, after the value is created, the actual time zone information (`"America/Los_Angeles"`) is no longer available. The following code
sample illustrates this behavior:

```
SELECT '2024-01-01 12:00:00'::TIMESTAMP_TZ;
```

Copy

```
+-------------------------------------+
| '2024-01-01 12:00:00'::TIMESTAMP_TZ |
|-------------------------------------|
| 2024-01-01 12:00:00.000 -0800       |
+-------------------------------------+
```

```
SELECT DATEADD(MONTH, 6, '2024-01-01 12:00:00'::TIMESTAMP_TZ);
```

Copy

```
+--------------------------------------------------------+
| DATEADD(MONTH, 6, '2024-01-01 12:00:00'::TIMESTAMP_TZ) |
|--------------------------------------------------------|
| 2024-07-01 12:00:00.000 -0800                          |
+--------------------------------------------------------+
```

#### TIMESTAMP[¶](#timestamp "Link to this heading")

TIMESTAMP in Snowflake is a user-specified alias associated with one of the TIMESTAMP\_\* variations. In all operations where TIMESTAMP is used, the associated TIMESTAMP\_\*
variation is automatically used. The TIMESTAMP data type is never stored in tables.

The TIMESTAMP\_\* variation associated with TIMESTAMP is specified by the [TIMESTAMP\_TYPE\_MAPPING](parameters.html#label-timestamp-type-mapping) session parameter. The default is TIMESTAMP\_NTZ.

All timestamp variations, as well as the TIMESTAMP alias, support an optional precision parameter for fractional
seconds (for example, `TIMESTAMP(3)`). Timestamp precision can range from 0 (seconds) to 9 (nanoseconds). The default precision is 9.

#### Timestamp examples[¶](#timestamp-examples "Link to this heading")

These examples create a table using different timestamps.

First, create a table with a TIMESTAMP column (mapped to TIMESTAMP\_NTZ):

```
ALTER SESSION SET TIMESTAMP_TYPE_MAPPING = TIMESTAMP_NTZ;

CREATE OR REPLACE TABLE ts_test(ts TIMESTAMP);

DESC TABLE ts_test;
```

Copy

```
+------+------------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+----------------+
| name | type             | kind   | null? | default | primary key | unique key | check | expression | comment | policy name | privacy domain |
|------+------------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+----------------|
| TS   | TIMESTAMP_NTZ(9) | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL           |
+------+------------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+----------------+
```

Next, explicitly use one of the TIMESTAMP variations (TIMESTAMP\_LTZ):

```
CREATE OR REPLACE TABLE ts_test(ts TIMESTAMP_LTZ);

DESC TABLE ts_test;
```

Copy

```
+------+------------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+----------------+
| name | type             | kind   | null? | default | primary key | unique key | check | expression | comment | policy name | privacy domain |
|------+------------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+----------------|
| TS   | TIMESTAMP_LTZ(9) | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL           |
+------+------------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+----------------+
```

Use TIMESTAMP\_LTZ with different time zones:

```
CREATE OR REPLACE TABLE ts_test(ts TIMESTAMP_LTZ);

ALTER SESSION SET TIMEZONE = 'America/Los_Angeles';

INSERT INTO ts_test VALUES('2024-01-01 16:00:00');
INSERT INTO ts_test VALUES('2024-01-02 16:00:00 +00:00');
```

Copy

This query shows that the time for January 2nd is 08:00 in Los Angeles (which is 16:00 in UTC):

```
SELECT ts, HOUR(ts) FROM ts_test;
```

Copy

```
+-------------------------------+----------+
| TS                            | HOUR(TS) |
|-------------------------------+----------|
| 2024-01-01 16:00:00.000 -0800 |       16 |
| 2024-01-02 08:00:00.000 -0800 |        8 |
+-------------------------------+----------+
```

Next, note that the times change with a different time zone:

```
ALTER SESSION SET TIMEZONE = 'America/New_York';

SELECT ts, HOUR(ts) FROM ts_test;
```

Copy

```
+-------------------------------+----------+
| TS                            | HOUR(TS) |
|-------------------------------+----------|
| 2024-01-01 19:00:00.000 -0500 |       19 |
| 2024-01-02 11:00:00.000 -0500 |       11 |
+-------------------------------+----------+
```

Create a table and use TIMESTAMP\_NTZ:

```
CREATE OR REPLACE TABLE ts_test(ts TIMESTAMP_NTZ);

ALTER SESSION SET TIMEZONE = 'America/Los_Angeles';

INSERT INTO ts_test VALUES('2024-01-01 16:00:00');
INSERT INTO ts_test VALUES('2024-01-02 16:00:00 +00:00');
```

Copy

Note that both times from different time zones are converted to the same “wallclock” time:

```
SELECT ts, HOUR(ts) FROM ts_test;
```

Copy

```
+-------------------------+----------+
| TS                      | HOUR(TS) |
|-------------------------+----------|
| 2024-01-01 16:00:00.000 |       16 |
| 2024-01-02 16:00:00.000 |       16 |
+-------------------------+----------+
```

Next, note that changing the session time zone doesn’t affect the results:

```
ALTER SESSION SET TIMEZONE = 'America/New_York';

SELECT ts, HOUR(ts) FROM ts_test;
```

Copy

```
+-------------------------+----------+
| TS                      | HOUR(TS) |
|-------------------------+----------|
| 2024-01-01 16:00:00.000 |       16 |
| 2024-01-02 16:00:00.000 |       16 |
+-------------------------+----------+
```

Create a table and use TIMESTAMP\_TZ:

```
CREATE OR REPLACE TABLE ts_test(ts TIMESTAMP_TZ);

ALTER SESSION SET TIMEZONE = 'America/Los_Angeles';

INSERT INTO ts_test VALUES('2024-01-01 16:00:00');
INSERT INTO ts_test VALUES('2024-01-02 16:00:00 +00:00');
```

Copy

Note that the January 1st record inherited the session time zone,
and `America/Los_Angeles` was converted to a numeric time zone offset:

```
SELECT ts, HOUR(ts) FROM ts_test;
```

Copy

```
+-------------------------------+----------+
| TS                            | HOUR(TS) |
|-------------------------------+----------|
| 2024-01-01 16:00:00.000 -0800 |       16 |
| 2024-01-02 16:00:00.000 +0000 |       16 |
+-------------------------------+----------+
```

Next, note that changing the session time zone doesn’t affect the results:

```
ALTER SESSION SET TIMEZONE = 'America/New_York';

SELECT ts, HOUR(ts) FROM ts_test;
```

Copy

```
+-------------------------------+----------+
| TS                            | HOUR(TS) |
|-------------------------------+----------|
| 2024-01-01 16:00:00.000 -0800 |       16 |
| 2024-01-02 16:00:00.000 +0000 |       16 |
+-------------------------------+----------+
```

## Supported calendar[¶](#supported-calendar "Link to this heading")

Snowflake uses the Gregorian Calendar for all dates and timestamps. The Gregorian Calendar starts in the year 1582, but recognizes prior years, which is important to note
because Snowflake does not adjust dates prior to 1582 (or calculations involving dates prior to 1582) to match the Julian Calendar. The `UUUU` format element
supports negative years.

## Date and time formats[¶](#date-and-time-formats "Link to this heading")

All of these data types accept most non-ambiguous date, time, or date + time formats. See
[Supported formats for AUTO detection](date-time-input-output.html#label-date-time-input-output-supported-formats-for-auto-detection) for the formats that Snowflake recognizes when
[configured to detect the format automatically](date-time-input-output.html#label-date-time-input-output-how-snowflake-determines).

You can also
[specify the date and time format manually](date-time-input-output.html#label-date-time-input-output-how-snowflake-determines). When specifying the
format, you can use the case-insensitive elements listed in the following table:

| Format element | Description |
| --- | --- |
| `YYYY` | Four-digit [1] year. |
| `YY` | Two-digit [1] year, controlled by the [TWO\_DIGIT\_CENTURY\_START](parameters.html#label-two-digit-century-start) session parameter. For example, when set to `1980`, values of `79` and `80` are parsed as `2079` and `1980`, respectively. |
| `MM` | Two-digit [1] month (`01` = January, and so on). |
| `MON` | Abbreviated month name [2]. |
| `MMMM` | Full month name [2]. |
| `DD` | Two-digit [1] day of month (`01` through `31`). |
| `DY` | Abbreviated day of week. |
| `HH24` | Two digits [1] for hour (`00` through `23`). You must not specify `AM` / `PM`. |
| `HH12` | Two digits [1] for hour (`01` through `12`). You can specify `AM` / `PM`. |
| `AM` , `PM` | Ante meridiem (`AM`) / post meridiem (`PM`). Use this only with `HH12` (not with `HH24`). |
| `MI` | Two digits [1] for minute (`00` through `59`). |
| `SS` | Two digits [1] for second (`00` through `59`). |
| `FF[0-9]` | Fractional seconds with precision `0` (seconds) to `9` (nanoseconds), e.g. `FF`, `FF0`, `FF3`, `FF9`. Specifying `FF` is equivalent to `FF9` (nanoseconds). |
| `TZH:TZM` , `TZHTZM` , `TZH` | Two-digit [1] time zone hour and minute, offset from UTC. Can be prefixed by `+`/`-` for sign. |
| `UUUU` | Four-digit year in [ISO format](https://en.wikipedia.org/wiki/ISO_8601), which are negative for BCE years. |

[1] The number of digits describes the output produced when serializing values to text. When parsing text, Snowflake accepts up to the specified number of digits. For example, a day number can be one or two digits.

[2] For the MON format element, the output produced when serializing values to text is the abbreviated month name. For the MMMM format element, the output produced when serializing values to text is the full month name. When parsing text, Snowflake accepts the three-digit abbreviation or the full month name for both MON and MMMM. For example, “January” or “Jan”, “February” or “Feb”, and so on are accepted when parsing text.

Note

* When a date-only format is used, the associated time is assumed to be midnight on that day.
* Anything in the format between double quotes or other than the above elements is parsed/formatted without being interpreted.
* For more details about valid ranges, number of digits, and best practices, see
  [Additional information about using date, time, and timestamp formats](date-time-input-output.html#label-date-time-input-output-additional-information).

### Examples of using date and time formats[¶](#examples-of-using-date-and-time-formats "Link to this heading")

The following example uses `FF` to indicate that the output has 9 digits in the fractional seconds field:

```
CREATE OR REPLACE TABLE timestamp_demo_table(
  tstmp TIMESTAMP,
  tstmp_tz TIMESTAMP_TZ,
  tstmp_ntz TIMESTAMP_NTZ,
  tstmp_ltz TIMESTAMP_LTZ);
INSERT INTO timestamp_demo_table (tstmp, tstmp_tz, tstmp_ntz, tstmp_ltz) VALUES (
  '2024-03-12 01:02:03.123456789',
  '2024-03-12 01:02:03.123456789',
  '2024-03-12 01:02:03.123456789',
  '2024-03-12 01:02:03.123456789');
```

Copy

```
ALTER SESSION SET TIMESTAMP_OUTPUT_FORMAT = 'YYYY-MM-DD HH24:MI:SS.FF';
ALTER SESSION SET TIMESTAMP_TZ_OUTPUT_FORMAT = 'YYYY-MM-DD HH24:MI:SS.FF';
ALTER SESSION SET TIMESTAMP_NTZ_OUTPUT_FORMAT = 'YYYY-MM-DD HH24:MI:SS.FF';
ALTER SESSION SET TIMESTAMP_LTZ_OUTPUT_FORMAT = 'YYYY-MM-DD HH24:MI:SS.FF';
```

Copy

```
SELECT tstmp, tstmp_tz, tstmp_ntz, tstmp_ltz
  FROM timestamp_demo_table;
```

Copy

```
+-------------------------------+-------------------------------+-------------------------------+-------------------------------+
| TSTMP                         | TSTMP_TZ                      | TSTMP_NTZ                     | TSTMP_LTZ                     |
|-------------------------------+-------------------------------+-------------------------------+-------------------------------|
| 2024-03-12 01:02:03.123456789 | 2024-03-12 01:02:03.123456789 | 2024-03-12 01:02:03.123456789 | 2024-03-12 01:02:03.123456789 |
+-------------------------------+-------------------------------+-------------------------------+-------------------------------+
```

## Date and time constants[¶](#date-and-time-constants "Link to this heading")

*Constants* (also known as *literals*) are fixed data values. Snowflake supports using string constants to specify fixed date, time, or timestamp values. String
constants must always be enclosed between delimiter characters. Snowflake supports using single quotes to delimit string constants.

For example:

```
DATE '2024-08-14'
TIME '10:03:56'
TIMESTAMP '2024-08-15 10:59:43'
```

Copy

The string is parsed as a DATE, TIME, or TIMESTAMP value based on the input format for the data type, as set through the following parameters:

DATE:
:   [DATE\_INPUT\_FORMAT](parameters.html#label-date-input-format)

TIME:
:   [TIME\_INPUT\_FORMAT](parameters.html#label-time-input-format)

TIMESTAMP:
:   [TIMESTAMP\_INPUT\_FORMAT](parameters.html#label-timestamp-input-format)

For example, to insert a specific date into a column in a table:

```
CREATE TABLE t1 (d1 DATE);

INSERT INTO t1 (d1) VALUES (DATE '2024-08-15');
```

Copy

## Interval constants[¶](#interval-constants "Link to this heading")

You can use interval constants to add or subtract a period of time to or from a date, time, or timestamp. Interval constants are implemented
using the INTERVAL keyword, which has the following syntax:

```
{ + | - } INTERVAL '<integer> [ <date_time_part> ] [ , <integer> [ <date_time_part> ] ... ]'
```

Copy

As with all string constants, Snowflake requires single quotes to delimit interval constants.

The INTERVAL keyword supports one more integers and, optionally, one or more date or time parts. For example:

* `INTERVAL '1 year'` represents one year.
* `INTERVAL '4 years, 5 months, 3 hours'` represents four years, five months, and three hours.

If a date or time part isn’t specified, the interval represents seconds (for example, `INTERVAL '2'` is the same
as `INTERVAL '2 seconds'`). Note that this is different from the default unit of time for performing date arithmetic.
For more details, see [Simple arithmetic for dates](#label-simple-date-arithmetic).

For the list of supported date and time parts, see [Supported Date and Time Parts for Intervals](#supported-date-and-time-parts-for-intervals).

Note

* The order of interval increments is important. The increments are added or subtracted in the order listed. For example:

  > + `INTERVAL '1 year, 1 day'` first adds or subtracts a year and then a day.
  > + `INTERVAL '1 day, 1 year'` first adds or subtracts a day and then a year.
  >
  > Ordering differences can affect calculations influenced by calendar events, such as leap years:
  >
  > ```
  > SELECT TO_DATE ('2019-02-28') + INTERVAL '1 day, 1 year';
  > ```
  >
  > Copy
  >
  > ```
  > +---------------------------------------------------+
  > | TO_DATE ('2019-02-28') + INTERVAL '1 DAY, 1 YEAR' |
  > |---------------------------------------------------|
  > | 2020-03-01                                        |
  > +---------------------------------------------------+
  > ```
  >
  > ```
  > SELECT TO_DATE ('2019-02-28') + INTERVAL '1 year, 1 day';
  > ```
  >
  > Copy
  >
  > ```
  > +---------------------------------------------------+
  > | TO_DATE ('2019-02-28') + INTERVAL '1 YEAR, 1 DAY' |
  > |---------------------------------------------------|
  > | 2020-02-29                                        |
  > +---------------------------------------------------+
  > ```
* INTERVAL is not a data type (that is, you can’t define a table column to be of data type INTERVAL). Intervals can only be used in date, time, and timestamp arithmetic.
* You can’t use an interval with a [SQL variable](session-variables). For example, the following query returns an error:

  ```
  SET v1 = '1 year';

  SELECT TO_DATE('2023-04-15') + INTERVAL $v1;
  ```

  Copy

### Supported date and time parts for intervals[¶](#supported-date-and-time-parts-for-intervals "Link to this heading")

The INTERVAL keyword supports the following date and time parts as arguments (case-insensitive):

| Date or Time Part | Abbreviations / Variations |
| --- | --- |
| `year` | `y` , `yy` , `yyy` , `yyyy` , `yr` , `years` , `yrs` |
| `quarter` | `q` , `qtr` , `qtrs` , `quarters` |
| `month` | `mm` , `mon` , `mons` , `months` |
| `week` | `w` , `wk` , `weekofyear` , `woy` , `wy` , `weeks` |
| `day` | `d` , `dd` , `days`, `dayofmonth` |
| `hour` | `h` , `hh` , `hr` , `hours` , `hrs` |
| `minute` | `m` , `mi` , `min` , `minutes` , `mins` |
| `second` | `s` , `sec` , `seconds` , `secs` |
| `millisecond` | `ms` , `msec` , `milliseconds` |
| `microsecond` | `us` , `usec` , `microseconds` |
| `nanosecond` | `ns` , `nsec` , `nanosec` , `nsecond` , `nanoseconds` , `nanosecs` , `nseconds` |

### Interval examples[¶](#interval-examples "Link to this heading")

Add a year interval to a specific date:

```
SELECT TO_DATE('2023-04-15') + INTERVAL '1 year';
```

Copy

```
+-------------------------------------------+
| TO_DATE('2023-04-15') + INTERVAL '1 YEAR' |
|-------------------------------------------|
| 2024-04-15                                |
+-------------------------------------------+
```

Add an interval of 3 hours and 18 minutes to a specific time:

```
SELECT TO_TIME('04:15:29') + INTERVAL '3 hours, 18 minutes';
```

Copy

```
+------------------------------------------------------+
| TO_TIME('04:15:29') + INTERVAL '3 HOURS, 18 MINUTES' |
|------------------------------------------------------|
| 07:33:29                                             |
+------------------------------------------------------+
```

Add a complex interval to the output of the CURRENT\_TIMESTAMP function:

```
SELECT CURRENT_TIMESTAMP + INTERVAL
    '1 year, 3 quarters, 4 months, 5 weeks, 6 days, 7 minutes, 8 seconds,
    1000 milliseconds, 4000000 microseconds, 5000000001 nanoseconds'
  AS complex_interval1;
```

Copy

The following is sample output. The output is different when the current timestamp is different.

```
+-------------------------------+
| COMPLEX_INTERVAL1             |
|-------------------------------|
| 2026-11-07 18:07:19.875000001 |
+-------------------------------+
```

Add a complex interval with abbreviated date/time part notation to a specific date:

```
SELECT TO_DATE('2025-01-17') + INTERVAL
    '1 y, 3 q, 4 mm, 5 w, 6 d, 7 h, 9 m, 8 s,
    1000 ms, 445343232 us, 898498273498 ns'
  AS complex_interval2;
```

Copy

```
+-------------------------------+
| COMPLEX_INTERVAL2             |
|-------------------------------|
| 2027-03-30 07:31:32.841505498 |
+-------------------------------+
```

Query a table of employee information and return the names of employees who were hired within the past two years and three months:

```
SELECT name, hire_date
  FROM employees
  WHERE hire_date > CURRENT_DATE - INTERVAL '2 y, 3 month';
```

Copy

Filter a TIMESTAMP column named `ts` from a table named `t1` and add four seconds to each returned value:

```
SELECT ts + INTERVAL '4 seconds'
  FROM t1
  WHERE ts > TO_TIMESTAMP('2024-04-05 01:02:03');
```

Copy

## Simple arithmetic for dates[¶](#simple-arithmetic-for-dates "Link to this heading")

In addition to using interval constants to add to and subtract from dates, times, and timestamps, you can also
add and subtract days to and from DATE values, in the form of `{ + | - }` `integer`, where `integer`
specifies the number of days to add or subtract.

Note

TIME and TIMESTAMP values don’t yet support simple arithmetic.

### Date arithmetic examples[¶](#date-arithmetic-examples "Link to this heading")

Add one day to a specific date:

```
SELECT TO_DATE('2024-04-15') + 1;
```

Copy

```
+---------------------------+
| TO_DATE('2024-04-15') + 1 |
|---------------------------|
| 2024-04-16                |
+---------------------------+
```

Subtract four days from a specific date:

```
SELECT TO_DATE('2024-04-15') - 4;
```

Copy

```
+---------------------------+
| TO_DATE('2024-04-15') - 4 |
|---------------------------|
| 2024-04-11                |
+---------------------------+
```

Query a table named `employees` and return the names of people who left the company, but were employed more than 365 days:

```
SELECT name
  FROM employees
  WHERE end_date > start_date + 365;
```

Copy

Was this page helpful?

YesNo

[Visit Snowflake](https://www.snowflake.com)

[Join the conversation](https://community.snowflake.com/s/)

[Develop with Snowflake](https://developers.snowflake.com)

[Share your feedback](/feedback)

[Read the latest on our blog](https://www.snowflake.com/blog/)

[Get your own certification](https://learn.snowflake.com)

[Privacy Notice](https://www.snowflake.com/privacy-policy/)[Site Terms](https://www.snowflake.com/legal/snowflake-site-terms/)Cookies Settings© 2026 Snowflake, Inc. All Rights Reserved.

### Alternative interfaces

[Snowflake Python APIs](/developer-guide/snowflake-python-api/snowflake-python-overview)[Snowflake REST APIs](/developer-guide/snowflake-rest-api/snowflake-rest-api)[Snowflake CLI](/developer-guide/snowflake-cli/index)

See all interfaces

On this page

1. [Data types](#data-types)
2. [Supported calendar](#supported-calendar)
3. [Date and time formats](#date-and-time-formats)
4. [Date and time constants](#date-and-time-constants)
5. [Interval constants](#interval-constants)
6. [Simple arithmetic for dates](#simple-arithmetic-for-dates)

Related content

1. [Date & time functions](/sql-reference/functions-date-time)
2. [Data type conversion](/sql-reference/data-type-conversion)