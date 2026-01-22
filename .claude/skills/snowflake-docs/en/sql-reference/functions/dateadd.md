---
auto_generated: true
description: Date & time functions
last_scraped: '2026-01-14T16:57:01.126212+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/dateadd
title: DATEADD | Snowflake Documentation
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

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)[Date & time](../functions-date-time.md)DATEADD

Categories:
:   [Date & time functions](../functions-date-time)

# DATEADD[¶](#dateadd "Link to this heading")

Adds the specified value for the specified date or time part to a date, time, or timestamp.

Aliases:
:   [TIMEADD](timeadd) , [TIMESTAMPADD](timestampadd)

See also:
:   [ADD\_MONTHS](add_months)

## Syntax[¶](#syntax "Link to this heading")

```
DATEADD( <date_or_time_part>, <value>, <date_or_time_expr> )
```

Copy

## Arguments[¶](#arguments "Link to this heading")

`date_or_time_part`
:   This indicates the units of time that you want to add. For example if you
    want to add two days, then specify `day`. This unit of measure must
    be one of the values listed in [Supported date and time parts](../functions-date-time.html#label-supported-date-time-parts).

`value`
:   This is the number of units of time that you want to add. For example,
    if the units of time is `day`, and you want to add two days, specify `2`.
    If you want to subtract two days, specify `-2`.

`date_or_time_expr`
:   `date_or_time_expr` must evaluate to a date, time, or timestamp.
    This is the date, time, or timestamp to which you want to add.
    For example, if you want to add two days to August 1, 2024, then specify
    `'2024-08-01'::DATE`.

    If the data type is TIME, then the `date_or_time_part`
    must be in units of hours or smaller, not days or bigger.

    If the input data type is DATE, and the `date_or_time_part` is hours
    or smaller, the input value will not be rejected, but instead will be
    treated as a TIMESTAMP with hours, minutes, seconds, and fractions of
    a second all initially set to 0 (e.g. midnight on the specified date).

## Returns[¶](#returns "Link to this heading")

If `date_or_time_expr` is a time, then the return data type is a time.

If `date_or_time_expr` is a timestamp, then the return data type is a timestamp.

If `date_or_time_expr` is a date:

> * If `date_or_time_part` is `day` or larger (for example, `month`, `year`),
>   the function returns a DATE value.
> * If `date_or_time_part` is smaller than a day (for example, `hour`, `minute`,
>   `second`), the function returns a TIMESTAMP\_NTZ value, with `00:00:00.000` as the starting
>   time for the date.

## Usage notes[¶](#usage-notes "Link to this heading")

When `date_or_time_part` is `year`, `quarter`, or `month` (or any of their variations),
if the result month has fewer days than the original day of the month, the result day of the month might
be different from the original day.

## Examples[¶](#examples "Link to this heading")

The TIMEADD and TIMESTAMPADD functions are aliases for the DATEADD function. You can use any of these three
functions in the examples to return the same results.

Add years to a date:

```
SELECT TO_DATE('2022-05-08') AS original_date,
       DATEADD(year, 2, TO_DATE('2022-05-08')) AS date_plus_two_years;
```

Copy

```
+---------------+---------------------+
| ORIGINAL_DATE | DATE_PLUS_TWO_YEARS |
|---------------+---------------------|
| 2022-05-08    | 2024-05-08          |
+---------------+---------------------+
```

Subtract years from a date:

```
SELECT TO_DATE('2022-05-08') AS original_date,
       DATEADD(year, -2, TO_DATE('2022-05-08')) AS date_minus_two_years;
```

Copy

```
+---------------+----------------------+
| ORIGINAL_DATE | DATE_MINUS_TWO_YEARS |
|---------------+----------------------|
| 2022-05-08    | 2020-05-08           |
+---------------+----------------------+
```

Add two years and two hours to a date. First, set the timestamp output format, create a table,
and insert data:

```
ALTER SESSION SET TIMESTAMP_OUTPUT_FORMAT = 'YYYY-MM-DD HH24:MI:SS.FF9';
CREATE TABLE datetest (d date);
INSERT INTO datetest VALUES ('2022-04-05');
```

Copy

Run a query that adds two years and two hours to a date:

```
SELECT d AS original_date,
       DATEADD(year, 2, d) AS date_plus_two_years,
       TO_TIMESTAMP(d) AS original_timestamp,
       DATEADD(hour, 2, d) AS timestamp_plus_two_hours
  FROM datetest;
```

Copy

```
+---------------+---------------------+-------------------------+--------------------------+
| ORIGINAL_DATE | DATE_PLUS_TWO_YEARS | ORIGINAL_TIMESTAMP      | TIMESTAMP_PLUS_TWO_HOURS |
|---------------+---------------------+-------------------------+--------------------------|
| 2022-04-05    | 2024-04-05          | 2022-04-05 00:00:00.000 | 2022-04-05 02:00:00.000  |
+---------------+---------------------+-------------------------+--------------------------+
```

Add a month to a date in a month with the same or more days than the
resulting month. For example, if the date is January 31, adding a month should not
return February 31.

```
SELECT DATEADD(month, 1, '2023-01-31'::DATE) AS date_plus_one_month;
```

Copy

```
+---------------------+
| DATE_PLUS_ONE_MONTH |
|---------------------|
| 2023-02-28          |
+---------------------+
```

Add a month to a date in a month with fewer days than the resulting month.
Adding a month to February 28 returns March 28.

```
SELECT DATEADD(month, 1, '2023-02-28'::DATE) AS date_plus_one_month;
```

Copy

```
+---------------------+
| DATE_PLUS_ONE_MONTH |
|---------------------|
| 2023-03-28          |
+---------------------+
```

Add hours to a time:

```
SELECT TO_TIME('05:00:00') AS original_time,
       DATEADD(hour, 3, TO_TIME('05:00:00')) AS time_plus_three_hours;
```

Copy

```
+---------------+-----------------------+
| ORIGINAL_TIME | TIME_PLUS_THREE_HOURS |
|---------------+-----------------------|
| 05:00:00      | 08:00:00              |
+---------------+-----------------------+
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