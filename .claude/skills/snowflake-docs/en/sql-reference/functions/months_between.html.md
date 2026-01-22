---
auto_generated: true
description: Date & time functions
last_scraped: '2026-01-14T16:56:30.048993+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/months_between.html
title: MONTHS_BETWEEN | Snowflake Documentation
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

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)[Date & time](../functions-date-time.md)MONTHS\_BETWEEN

Categories:
:   [Date & time functions](../functions-date-time)

# MONTHS\_BETWEEN[¶](#months-between "Link to this heading")

Returns the number of months between two DATE or TIMESTAMP values.

For example, `MONTHS_BETWEEN('2020-02-01'::DATE, '2020-01-01'::DATE)` returns 1.0.

See also:
:   [DATEDIFF](datediff)

## Syntax[¶](#syntax "Link to this heading")

```
MONTHS_BETWEEN( <date_expr1> , <date_expr2> )
```

Copy

## Arguments[¶](#arguments "Link to this heading")

`date_expr1`
:   The date to subtract from.

`date_expr2`
:   The date to subtract.

## Returns[¶](#returns "Link to this heading")

A FLOAT representing the number of months between the two dates.

The number is calculated as described below:

* The integer portion of the FLOAT is calculated using the year and month parts of the input values.
* In most situations, the fractional portion is calculated using the day and time parts of the input values.
  (When calculating the fraction of a month, the function considers each month to be 31 days long.)

  However, there are two exceptions:

  > + If the days of the month are the same (e.g. February 28 and March 28), the fractional portion is zero,
  >   even if one or both input values are timestamps and the times differ.
  > + If the days of the month are both the last day of the month (e.g. February 28 and March 31), the fractional
  >   portion is zero, even if the days of the month are not the same.
  >
  > For example, the function considers each of the following pairs of dates/timestamps to be exactly 1.0 months apart:
  >
  > | Date/Timestamp 1 | Date/Timestamp 2 | Notes |
  > | --- | --- | --- |
  > | 2019-03-01 02:00:00 | 2019-02-01 13:00:00 | Same day of each month. |
  > | 2019-03-28 | 2019-02-28 | Same day of each month. |
  > | 2019-03-31 | 2019-02-28 | Last day of each month. |
  > | 2019-03-31 01:00:00 | 2019-02-28 13:00:00 | Last day of each month. |

## Usage notes[¶](#usage-notes "Link to this heading")

* If date (or timestamp) d1 represents an earlier point in time than d2, then `MONTHS_BETWEEN(d1, d2)`
  returns a negative value; otherwise it returns a positive value. More generally, swapping
  the inputs reverses the sign: `MONTHS_BETWEEN(d1, d2)` = `-MONTHS_BETWEEN(d2, d1)`.
* You can use a DATE value for one input parameter and a TIMESTAMP for the other.
* If you use one or more TIMESTAMP values but do not want fractional differences based on time of day, then cast your
  TIMESTAMP expressions to DATE.
* If you only want integer values, you can truncate, round, or cast the value. For example:

  ```
  SELECT
      ROUND(MONTHS_BETWEEN('2019-03-31 12:00:00'::TIMESTAMP,
                           '2019-02-28 00:00:00'::TIMESTAMP)) AS MonthsBetween1;
  +----------------+
  | MONTHSBETWEEN1 |
  |----------------|
  |              1 |
  +----------------+
  ```

  Copy
* If any input is NULL, the result is NULL.

## Examples[¶](#examples "Link to this heading")

This example shows differences in whole months. The first pair of dates have the same day of the month (the 15th).
The second pair of dates are both the last days in their respective months (February 28th and March 31st).

> ```
> SELECT
>     MONTHS_BETWEEN('2019-03-15'::DATE,
>                    '2019-02-15'::DATE) AS MonthsBetween1,
>     MONTHS_BETWEEN('2019-03-31'::DATE,
>                    '2019-02-28'::DATE) AS MonthsBetween2;
> +----------------+----------------+
> | MONTHSBETWEEN1 | MONTHSBETWEEN2 |
> |----------------+----------------|
> |       1.000000 |       1.000000 |
> +----------------+----------------+
> ```
>
> Copy

The next example shows differences in fractional months.

> * For the first column, the function is passed two dates.
> * For the second column, the function is passed two timestamps
>   that represent the same two dates as were used for the first column, but with different times.
>   The difference in the second column is larger than the first column due to the differences in time.
> * For the third column, the function is passed two timestamps that represent
>   the same day of their respective months. This causes the function to ignore
>   any time differences between the timestamps, so the fractional part is 0.
>
> ```
> SELECT
>     MONTHS_BETWEEN('2019-03-01'::DATE,
>                    '2019-02-15'::DATE) AS MonthsBetween1,
>     MONTHS_BETWEEN('2019-03-01 02:00:00'::TIMESTAMP,
>                    '2019-02-15 01:00:00'::TIMESTAMP) AS MonthsBetween2,
>     MONTHS_BETWEEN('2019-02-15 02:00:00'::TIMESTAMP,
>                    '2019-02-15 01:00:00'::TIMESTAMP) AS MonthsBetween3
>     ;
> +----------------+----------------+----------------+
> | MONTHSBETWEEN1 | MONTHSBETWEEN2 | MONTHSBETWEEN3 |
> |----------------+----------------+----------------|
> |       0.548387 |       0.549731 |       0.000000 |
> +----------------+----------------+----------------+
> ```
>
> Copy

The fact that the function returns an integer number of months both when the days of the
month are the same (e.g. February 28 and March 28) and when the days of the month are the last day of the month
(e.g. February 28 and March 31) can lead to unintuitive behavior; specifically, increasing the first date
in the pair does not always increase the output value.
In this example, as the first date increases from March 28th to March 30th and then to March 31st, the
difference increases from 1.0 to a larger number and then decreases back to 1.0.

> * For the first column, the input dates represent the same day in different months, so
>   the function returns `0` for the fractional part of the result.
> * For the second column, the input dates represent different days in different months (and are not both the last
>   day of the month), so the function calculates the fractional part of the result.
> * For the third column, the input dates represent the last days in each of two different months, so
>   the function again returns `0` for the fractional part of the result.
>
> ```
> SELECT
>     MONTHS_BETWEEN('2019-03-28'::DATE,
>                    '2019-02-28'::DATE) AS MonthsBetween1,
>     MONTHS_BETWEEN('2019-03-30'::DATE,
>                    '2019-02-28'::DATE) AS MonthsBetween2,
>     MONTHS_BETWEEN('2019-03-31'::DATE,
>                    '2019-02-28'::DATE) AS MonthsBetween3
>     ;
> +----------------+----------------+----------------+
> | MONTHSBETWEEN1 | MONTHSBETWEEN2 | MONTHSBETWEEN3 |
> |----------------+----------------+----------------|
> |       1.000000 |       1.064516 |       1.000000 |
> +----------------+----------------+----------------+
> ```
>
> Copy

This example shows that reversing the order of the parameters reverses the sign of the result:

> ```
> SELECT
>     MONTHS_BETWEEN('2019-03-01'::DATE,
>                    '2019-02-01'::DATE) AS MonthsBetween1,
>     MONTHS_BETWEEN('2019-02-01'::DATE,
>                    '2019-03-01'::DATE) AS MonthsBetween2
>     ;
> +----------------+----------------+
> | MONTHSBETWEEN1 | MONTHSBETWEEN2 |
> |----------------+----------------|
> |       1.000000 |      -1.000000 |
> +----------------+----------------+
> ```
>
> Copy

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