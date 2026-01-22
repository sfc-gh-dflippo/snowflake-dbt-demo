---
auto_generated: true
description: Date & time functions
last_scraped: '2026-01-14T16:56:50.307867+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/date_part
title: DATE_PART | Snowflake Documentation
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

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)[Date & time](../functions-date-time.md)DATE\_PART

Categories:
:   [Date & time functions](../functions-date-time)

# DATE\_PART[¶](#date-part "Link to this heading")

Extracts the specified date or time part from a date, time, or timestamp.

Alternatives:
:   [EXTRACT](extract) , [HOUR / MINUTE / SECOND](hour-minute-second) , [YEAR\* / DAY\* / WEEK\* / MONTH / QUARTER](year)

## Syntax[¶](#syntax "Link to this heading")

```
DATE_PART( <date_or_time_part> , <date_time_or_timestamp_expr> )
```

Copy

```
DATE_PART( <date_or_time_part> FROM <date_time_or_timestamp_expr> )
```

Copy

## Arguments[¶](#arguments "Link to this heading")

`date_or_time_part`
:   The unit of time. Must be one of the values listed in [Supported date and time parts](../functions-date-time.html#label-supported-date-time-parts) (e.g. `month`).
    The value can be a string literal or can be unquoted (for example, `'month'` or `month`).

    * When `date_or_time_part` is `week` (or any of its variations), the output is controlled by the [WEEK\_START](../parameters.html#label-week-start) session parameter.
    * When `date_or_time_part` is `dayofweek` or `yearofweek` (or any of their variations), the output is controlled by the [WEEK\_OF\_YEAR\_POLICY](../parameters.html#label-week-of-year-policy) and [WEEK\_START](../parameters.html#label-week-start) session parameters.

    For more information, including examples, see [Calendar weeks and weekdays](../functions-date-time.html#label-calendar-weeks-weekdays).

`date_time_or_timestamp_expr`
:   A date, a time, or a timestamp, or an expression that can be evaluated to a date, a time, or a timestamp.

## Returns[¶](#returns "Link to this heading")

Returns a value of NUMBER data type.

## Usage notes[¶](#usage-notes "Link to this heading")

Currently, when `date_or_timestamp_expr` is a DATE value, the following `date_or_time_part`
values are not supported:

* `epoch_millisecond`
* `epoch_microsecond`
* `epoch_nanosecond`

Other [date and time parts](../functions-date-time.html#label-supported-date-time-parts) (including `epoch_second`) are supported.

Tip

To extract a full DATE or TIME value instead of a single part from a TIMESTAMP value, you can cast the
TIMESTAMP value to a DATE or TIME value, respectively. For example:

```
SELECT '2025-04-08T23:39:20.123-07:00'::TIMESTAMP::DATE AS full_date_value;
```

Copy

```
+-----------------+
| FULL_DATE_VALUE |
|-----------------|
| 2025-04-08      |
+-----------------+
```

```
SELECT '2025-04-08T23:39:20.123-07:00'::TIMESTAMP::TIME AS full_time_value;
```

Copy

```
+-----------------+
| FULL_TIME_VALUE |
|-----------------|
| 23:39:20        |
+-----------------+
```

## Examples[¶](#examples "Link to this heading")

This shows a simple example of extracting part of a DATE:

```
SELECT DATE_PART(quarter, '2024-04-08'::DATE);
```

Copy

```
+----------------------------------------+
| DATE_PART(QUARTER, '2024-04-08'::DATE) |
|----------------------------------------|
|                                      2 |
+----------------------------------------+
```

This shows an example of extracting part of a TIMESTAMP:

```
SELECT TO_TIMESTAMP(
  '2024-04-08T23:39:20.123-07:00') AS "TIME_STAMP1",
  DATE_PART(year, "TIME_STAMP1") AS "EXTRACTED YEAR";
```

Copy

```
+-------------------------+----------------+
| TIME_STAMP1             | EXTRACTED YEAR |
|-------------------------+----------------|
| 2024-04-08 23:39:20.123 |           2024 |
+-------------------------+----------------+
```

This shows an example of converting a TIMESTAMP to the number of seconds since
the beginning of the [Unix epoch](https://en.wikipedia.org/wiki/Unix_time) (midnight January 1, 1970):

```
SELECT TO_TIMESTAMP(
  '2024-04-08T23:39:20.123-07:00') AS "TIME_STAMP1",
  DATE_PART(epoch_second, "TIME_STAMP1") AS "EXTRACTED EPOCH SECOND";
```

Copy

```
+-------------------------+------------------------+
| TIME_STAMP1             | EXTRACTED EPOCH SECOND |
|-------------------------+------------------------|
| 2024-04-08 23:39:20.123 |             1712619560 |
+-------------------------+------------------------+
```

This shows an example of converting a TIMESTAMP to the number of milliseconds since
the beginning of the [Unix epoch](https://en.wikipedia.org/wiki/Unix_time) (midnight January 1, 1970):

```
SELECT TO_TIMESTAMP(
  '2024-04-08T23:39:20.123-07:00') AS "TIME_STAMP1",
  DATE_PART(epoch_millisecond, "TIME_STAMP1") AS "EXTRACTED EPOCH MILLISECOND";
```

Copy

```
+-------------------------+-----------------------------+
| TIME_STAMP1             | EXTRACTED EPOCH MILLISECOND |
|-------------------------+-----------------------------|
| 2024-04-08 23:39:20.123 |               1712619560123 |
+-------------------------+-----------------------------+
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