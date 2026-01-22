---
auto_generated: true
description: Date & time functions
last_scraped: '2026-01-14T16:55:17.381441+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/datediff.html
title: DATEDIFF | Snowflake Documentation
---

1. [Overview](../../reference.md)
2. [SQL data types reference](../../sql-reference-data-types.md)
3. [SQL command reference](../../sql-reference-commands.md)
4. [Function and stored procedure reference](../../sql-reference-functions.md)

   * [Summary of functions](../intro-summary-operators-functions.md)
   * [All functions (alphabetical)](../functions-all.md)")
   * [Aggregate](../functions-aggregation.md)
   * AI Functions

     * Scalar functions

       * [AI\_CLASSIFY](ai_classify.md)
       * [AI\_COMPLETE](ai_complete.md)
       * [AI\_COUNT\_TOKENS](ai_count_tokens.md)
       * [AI\_EMBED](ai_embed.md)
       * [AI\_EXTRACT](ai_extract.md)
       * [AI\_FILTER](ai_filter.md)
       * [AI\_PARSE\_DOCUMENT](ai_parse_document.md)
       * [AI\_REDACT](ai_redact.md)
       * [AI\_SENTIMENT](ai_sentiment.md)
       * [AI\_SIMILARITY](ai_similarity.md)
       * [AI\_TRANSCRIBE](ai_transcribe.md)
       * [AI\_TRANSLATE](ai_translate.md)
       * [CLASSIFY\_TEXT (SNOWFLAKE.CORTEX)](classify_text-snowflake-cortex.md)")
       * [COMPLETE (SNOWFLAKE.CORTEX)](complete-snowflake-cortex.md)")
       * [COMPLETE multimodal (images) (SNOWFLAKE.CORTEX)](complete-snowflake-cortex-multimodal.md) (SNOWFLAKE.CORTEX)")
       * [EMBED\_TEXT\_768 (SNOWFLAKE.CORTEX)](embed_text-snowflake-cortex.md)")
       * [EMBED\_TEXT\_1024 (SNOWFLAKE.CORTEX)](embed_text_1024-snowflake-cortex.md)")
       * [ENTITY\_SENTIMENT (SNOWFLAKE.CORTEX)](entity_sentiment-snowflake-cortex.md)")
       * [EXTRACT\_ANSWER (SNOWFLAKE.CORTEX)](extract_answer-snowflake-cortex.md)")
       * [FINETUNE (SNOWFLAKE.CORTEX)](finetune-snowflake-cortex.md)")
       * [PARSE\_DOCUMENT (SNOWFLAKE.CORTEX)](parse_document-snowflake-cortex.md)")
       * [SENTIMENT (SNOWFLAKE.CORTEX)](sentiment-snowflake-cortex.md)")
       * [SUMMARIZE (SNOWFLAKE.CORTEX)](summarize-snowflake-cortex.md)")
       * [TRANSLATE (SNOWFLAKE.CORTEX)](translate-snowflake-cortex.md)")
     * Aggregate functions

       * [AI\_AGG](ai_agg.md)
       * [AI\_SUMMARIZE\_AGG](ai_summarize_agg.md)
     * Helper functions

       * [COUNT\_TOKENS (SNOWFLAKE.CORTEX)](count_tokens-snowflake-cortex.md)")
       * [SEARCH\_PREVIEW (SNOWFLAKE.CORTEX)](search_preview-snowflake-cortex.md)")
       * [SPLIT\_TEXT\_MARKDOWN\_HEADER (SNOWFLAKE.CORTEX)](split_text_markdown_header-snowflake-cortex.md)")
       * [SPLIT\_TEXT\_RECURSIVE\_CHARACTER (SNOWFLAKE.CORTEX)](split_text_recursive_character-snowflake-cortex.md)")
       * [TRY\_COMPLETE (SNOWFLAKE.CORTEX)](try_complete-snowflake-cortex.md)")
   * [Bitwise expression](../expressions-byte-bit.md)
   * [Conditional expression](../expressions-conditional.md)
   * [Context](../functions-context.md)
   * [Conversion](../functions-conversion.md)
   * [Data generation](../functions-data-generation.md)
   * [Data metric](../functions-data-metric.md)
   * [Date & time](../functions-date-time.md)

     + Construction
     + [DATE\_FROM\_PARTS](date_from_parts.md)
     + [TIME\_FROM\_PARTS](time_from_parts.md)
     + [TIMESTAMP\_FROM\_PARTS](timestamp_from_parts.md)
     + Extraction
     + [DATE\_PART](date_part.md)
     + [DAYNAME](dayname.md)
     + [EXTRACT](extract.md)
     + [HOUR](hour-minute-second.md)
     + [MINUTE](hour-minute-second.md)
     + [SECOND](hour-minute-second.md)
     + [LAST\_DAY](last_day.md)
     + [MONTHNAME](monthname.md)
     + [NEXT\_DAY](next_day.md)
     + [PREVIOUS\_DAY](previous_day.md)
     + [YEAR](year.md)
     + [YEAROFWEEK](year.md)
     + [YEAROFWEEKISO](year.md)
     + [DAY](year.md)
     + [DAYOFMONTH](year.md)
     + [DAYOFWEEK](year.md)
     + [DAYOFWEEKISO](year.md)
     + [DAYOFYEAR](year.md)
     + [WEEK](year.md)
     + [WEEKOFYEAR](year.md)
     + [WEEKISO](year.md)
     + [MONTH](year.md)
     + [QUARTER](year.md)
     + Addition & subtraction
     + [ADD\_MONTHS](add_months.md)
     + [DATEADD](dateadd.md)
     + [DATEDIFF](datediff.md)
     + [MONTHS\_BETWEEN](months_between.md)
     + [TIMEADD](timeadd.md)
     + [TIMEDIFF](timediff.md)
     + [TIMESTAMPADD](timestampadd.md)
     + [TIMESTAMPDIFF](timestampdiff.md)
     + Truncation
     + [DATE\_TRUNC](date_trunc.md)
     + [TIME\_SLICE](time_slice.md)
     + [TRUNCATE, TRUNC](trunc2.md)
     + Conversion
     + [TO\_DATE](to_date.md)
     + [DATE](to_date.md)
     + [TO\_TIME](to_time.md)
     + [TIME](to_time.md)
     + [TO\_TIMESTAMP](to_timestamp.md)
     + [TO\_TIMESTAMP\_LTZ](to_timestamp.md)
     + [TO\_TIMESTAMP\_NTZ](to_timestamp.md)
     + [TO\_TIMESTAMP\_TZ](to_timestamp.md)
     + [TRY\_TO\_DATE](try_to_date.md)
     + [TRY\_TO\_TIME](try_to_time.md)
     + [TRY\_TO\_TIMESTAMP](try_to_timestamp.md)
     + [TRY\_TO\_TIMESTAMP\_LTZ](try_to_timestamp.md)
     + [TRY\_TO\_TIMESTAMP\_NTZ](try_to_timestamp.md)
     + [TRY\_TO\_TIMESTAMP\_TZ](try_to_timestamp.md)
     + Time zone
     + [CONVERT\_TIMEZONE](convert_timezone.md)
     + Alerts
     + [LAST\_SUCCESSFUL\_SCHEDULED\_TIME](last_successful_scheduled_time.md)
     + [SCHEDULED\_TIME](scheduled_time.md)
   * [Differential privacy](../functions-differential-privacy.md)
   * [Encryption](../functions-encryption.md)
   * [File](../functions-file.md)
   * [Geospatial](../functions-geospatial.md)
   * [Hash](../functions-hash-scalar.md)
   * [Metadata](../functions-metadata.md)
   * [ML Model Monitors](../functions-model-monitors.md)
   * [Notification](../functions-notification.md)
   * [Numeric](../functions-numeric.md)
   * [Organization users and organization user groups](../functions-organization-users.md)
   * [Regular expressions](../functions-regexp.md)
   * [Semi-structured and structured data](../functions-semistructured.md)
   * [Snowpark Container Services](../functions-spcs.md)
   * [String & binary](../functions-string.md)
   * [System](../functions-system.md)
   * [Table](../functions-table.md)
   * [Vector](../functions-vector.md)
   * [Window](../functions-window.md)
   * [Stored procedures](../../sql-reference-stored-procedures.md)
5. [Class reference](../../sql-reference-classes.md)
6. [Scripting reference](../../sql-reference-snowflake-scripting.md)
7. [General reference](../../sql-reference.md)
8. [API reference](../../api-reference.md)

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)[Date & time](../functions-date-time.md)DATEDIFF

Categories:
:   [Date & time functions](../functions-date-time)

# DATEDIFF[¶](#datediff "Link to this heading")

Calculates the difference between two date, time, or timestamp expressions based on the date or time part requested.
The function returns the result of subtracting the second argument from the third argument.

Note

Difference calculations compare the specified date or time part, not the complete date or time. For example, the month
difference between November 28, 2024 and December 5, 2024 is 1, because the difference between the two months November
and December, both in 2024, is 1. To reflect the fact that the difference between the two dates is less than a full
month, calculate the difference in days instead.

You can also use the minus sign (`-`) to calculate the difference between two dates by subtracting one date from
another.

To add units of time to a date, time, or timestamp (for example, add two days to a date) or subtract units of time
from them, you can use the [DATEADD](dateadd), [TIMEADD](timeadd), or [TIMESTAMPADD](timestampadd) function.

See also:
:   [TIMEDIFF](timediff) , [TIMESTAMPDIFF](timestampdiff)

## Syntax[¶](#syntax "Link to this heading")

**For DATEDIFF:**

```
DATEDIFF( <date_or_time_part>, <date_or_time_expr1>, <date_or_time_expr2> )
```

Copy

**For minus sign:**

```
<date_expr2> - <date_expr1>
```

Copy

## Arguments[¶](#arguments "Link to this heading")

**For DATEDIFF:**

`date_or_time_part`
:   The unit of time. Must be one of the values listed in [Supported date and time parts](../functions-date-time.html#label-supported-date-time-parts) (for example, `month`).
    The value can be a string literal or can be unquoted (for example, `'month'` or `month`).

`date_or_time_expr1`, `date_or_time_expr2`
:   The values to compare. Must be a date, a time, a timestamp, or an expression that can be evaluated to
    a date, a time, or a timestamp. The value `date_or_time_expr1` is subtracted from
    `date_or_time_expr2`.

**For minus sign:**

`date_expr1`, `date_expr2`
:   The values to compare. Must be a date, or an expression that can be evaluated to a date. The value `date_expr1` is
    subtracted from `date_expr2`.

## Returns[¶](#returns "Link to this heading")

**For DATEDIFF:**

Returns an integer representing the difference in the number of units (seconds, days, and so on) between `date_or_time_expr2` and
`date_or_time_expr1`.

Returns NULL if any argument is NULL.

**For minus sign:**

Returns an integer representing the number of days difference between `date_expr2` and
`date_expr1`. (The units are always days.)

Returns an error if `date_expr2` or `date_expr1` is NULL.

## Usage notes[¶](#usage-notes "Link to this heading")

**For both DATEDIFF and minus sign:**

* Output values can be negative, for example, -12 days.

**For DATEDIFF:**

* The function supports units of years, quarters, months, weeks, days, hours, minutes, seconds, milliseconds, microseconds, and nanoseconds.
* If `date_or_time_part` is `week` (or any of its variations), the output is controlled by the [WEEK\_START](../parameters.html#label-week-start) session parameter. For more details, including examples, see
  [Calendar weeks and weekdays](../functions-date-time.html#label-calendar-weeks-weekdays).
* The unit (for example, `month`) used to calculate the difference determines which parts of the DATE, TIME, or TIMESTAMP field are
  evaluated. So, the unit determines the precision of the result.

  Smaller units are not used, so values are not rounded. For example, even though the difference between January 1, 2021 and
  February 28, 2021 is closer to two months than to one month, the following returns one month:

  ```
  DATEDIFF(month, '2021-01-01'::DATE, '2021-02-28'::DATE)
  ```

  Copy

  For a DATE value:

  > + `year` uses only the year and disregards all the other parts.
  > + `month` uses the month and year.
  > + `day` uses the entire date.

  For a TIME value:

  > + `hour` uses only the hour and disregards all the other parts.
  > + `minute` uses the hour and minute.
  > + `second` uses the hour, minute, and second, but not the fractional seconds.
  > + `millisecond` uses the hour, minute, second, and first three digits of the fractional seconds. Fractional
  >   seconds are not rounded. For example, `DATEDIFF(milliseconds, '2024-02-20 21:18:41.0000', '2024-02-20 21:18:42.1239')` returns 1.123 seconds,
  >   not 1.124 seconds.
  > + `microsecond` uses the hour, minute, second, and first six digits of the fractional seconds. Fractional
  >   seconds are not rounded.
  > + `nanosecond` uses the hour, minute, second, and all nine digits of the fractional seconds.

  For a TIMESTAMP value:

  > The rules match the rules for DATE and TIME data types above. Only the specified unit and larger units are used.

**For minus sign:**

* `date_expr1` and `date_expr2` must both be dates. Times and timestamps are not allowed.

## Examples[¶](#examples "Link to this heading")

Calculate the difference in years between two timestamps:

```
SELECT DATEDIFF(year, 
                '2020-04-09 14:39:20'::TIMESTAMP, 
                '2023-05-08 23:39:20'::TIMESTAMP) 
  AS diff_years;
```

Copy

```
+------------+
| DIFF_YEARS |
|------------|
|          3 |
+------------+
```

Calculate the difference in hours between two timestamps:

```
SELECT DATEDIFF(hour, 
               '2023-05-08T23:39:20.123-07:00'::TIMESTAMP, 
               DATEADD(year, 2, ('2023-05-08T23:39:20.123-07:00')::TIMESTAMP)) 
  AS diff_hours;
```

Copy

```
+------------+
| DIFF_HOURS |
|------------|
|      17544 |
+------------+
```

Demonstrate how date parts affect DATEDIFF calculations; also, demonstrate use of the minus sign for date
subtraction:

```
SELECT column1 date_1, column2 date_2,
       DATEDIFF(year, column1, column2) diff_years,
       DATEDIFF(month, column1, column2) diff_months,
       DATEDIFF(day, column1, column2) diff_days,
       column2::DATE - column1::DATE AS diff_days_via_minus
  FROM VALUES
       ('2015-12-30', '2015-12-31'),
       ('2015-12-31', '2016-01-01'),
       ('2016-01-01', '2017-12-31'),
       ('2016-08-23', '2016-09-07');
```

Copy

```
+------------+------------+------------+-------------+-----------+---------------------+
| DATE_1     | DATE_2     | DIFF_YEARS | DIFF_MONTHS | DIFF_DAYS | DIFF_DAYS_VIA_MINUS |
|------------+------------+------------+-------------+-----------+---------------------|
| 2015-12-30 | 2015-12-31 |          0 |           0 |         1 |                   1 |
| 2015-12-31 | 2016-01-01 |          1 |           1 |         1 |                   1 |
| 2016-01-01 | 2017-12-31 |          1 |          23 |       730 |                 730 |
| 2016-08-23 | 2016-09-07 |          0 |           1 |        15 |                  15 |
+------------+------------+------------+-------------+-----------+---------------------+
```

Demonstrate how time parts affect DATEDIFF calculations:

```
ALTER SESSION SET TIMESTAMP_NTZ_OUTPUT_FORMAT = 'DY, DD MON YYYY HH24:MI:SS';
```

Copy

```
SELECT column1 timestamp_1, column2 timestamp_2,
       DATEDIFF(hour, column1, column2) diff_hours,
       DATEDIFF(minute, column1, column2) diff_minutes,
       DATEDIFF(second, column1, column2) diff_seconds
  FROM VALUES
       ('2016-01-01 01:59:59'::TIMESTAMP, '2016-01-01 02:00:00'::TIMESTAMP),
       ('2016-01-01 01:00:00'::TIMESTAMP, '2016-01-01 01:59:00'::TIMESTAMP),
       ('2016-01-01 01:00:59'::TIMESTAMP, '2016-01-01 02:00:00'::TIMESTAMP);
```

Copy

```
+---------------------------+---------------------------+------------+--------------+--------------+
| TIMESTAMP_1               | TIMESTAMP_2               | DIFF_HOURS | DIFF_MINUTES | DIFF_SECONDS |
|---------------------------+---------------------------+------------+--------------+--------------|
| Fri, 01 Jan 2016 01:59:59 | Fri, 01 Jan 2016 02:00:00 |          1 |            1 |            1 |
| Fri, 01 Jan 2016 01:00:00 | Fri, 01 Jan 2016 01:59:00 |          0 |           59 |         3540 |
| Fri, 01 Jan 2016 01:00:59 | Fri, 01 Jan 2016 02:00:00 |          1 |           60 |         3541 |
+---------------------------+---------------------------+------------+--------------+--------------+
```

Use the [CURRENT\_TIMESTAMP](current_timestamp) function with the DATEDIFF function to
calculate the difference in years, months, and days between a specified timestamp and the
current timestamp:

```
SELECT column1 specified_timestamp,
       column2 timestamp_now,
       DATEDIFF(year, column1, column2) diff_years,
       DATEDIFF(month, column1, column2) diff_months,
       DATEDIFF(day, column1, column2) diff_days,
       column2::DATE - column1::DATE AS diff_days_via_minus
  FROM VALUES
    ('2012-08-23 09:00:00.000 -0700', CURRENT_TIMESTAMP);
```

Copy

```
+-------------------------------+-------------------------------+------------+-------------+-----------+---------------------+
| SPECIFIED_TIMESTAMP           | TIMESTAMP_NOW                 | DIFF_YEARS | DIFF_MONTHS | DIFF_DAYS | DIFF_DAYS_VIA_MINUS |
|-------------------------------+-------------------------------+------------+-------------+-----------+---------------------|
| 2012-08-23 09:00:00.000 -0700 | 2024-09-04 17:21:12.189 -0700 |         12 |         145 |      4395 |                4395 |
+-------------------------------+-------------------------------+------------+-------------+-----------+---------------------+
```

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

1. [Syntax](#syntax)
2. [Arguments](#arguments)
3. [Returns](#returns)
4. [Usage notes](#usage-notes)
5. [Examples](#examples)