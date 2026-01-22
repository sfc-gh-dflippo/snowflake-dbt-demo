---
auto_generated: true
description: Date & time functions
last_scraped: '2026-01-14T16:56:50.590175+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/date_trunc
title: DATE_TRUNC | Snowflake Documentation
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

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)[Date & time](../functions-date-time.md)DATE\_TRUNC

Categories:
:   [Date & time functions](../functions-date-time)

# DATE\_TRUNC[¶](#date-trunc "Link to this heading")

Truncates a DATE, TIME, or TIMESTAMP value to the specified precision. For example,
truncating a timestamp down to the quarter returns the timestamp corresponding
to midnight of the first day of the original timestamp’s quarter.

This function provides an alternative syntax for [TRUNCATE, TRUNC](trunc2) by reversing the
two arguments.

Truncation is not the same as extraction. For example:

* Truncating a timestamp down to the quarter using this function returns the timestamp corresponding
  to midnight of the first day of the quarter for the input timestamp.
* Extracting the quarter date part from a timestamp using the [EXTRACT](extract) function returns the
  quarter number of the year in the timestamp.

Alternatives:
:   [TRUNCATE, TRUNC](trunc2)

See also:
:   [DATE\_PART](date_part) , [EXTRACT](extract)

## Syntax[¶](#syntax "Link to this heading")

```
DATE_TRUNC( <date_or_time_part>, <date_or_time_expr> )
```

Copy

## Arguments[¶](#arguments "Link to this heading")

`date_or_time_part`
:   This argument must be one of the values listed in [Supported date and time parts](../functions-date-time.html#label-supported-date-time-parts).

`date_or_time_expr`
:   This argument must evaluate to a date, time, or timestamp.

## Returns[¶](#returns "Link to this heading")

The returned value is the same type as the input value.

For example, if the input value is a TIMESTAMP, then the returned value is a TIMESTAMP.

## Usage notes[¶](#usage-notes "Link to this heading")

* When `date_or_time_part` is `week` (or any of its variations), the output is controlled
  by the [WEEK\_START](../parameters.html#label-week-start) session parameter. For more details, including examples, see
  [Calendar weeks and weekdays](../functions-date-time.html#label-calendar-weeks-weekdays).
* For TIME values, you can’t specify a `date_or_time_part` that is outside the scope of the TIME type.
  For example, you can truncate a TIMESTAMP value to a `day`, `week`, `year`, and so on because the TIMESTAMP type
  encodes date/times with the required precision. However, trying to truncate a TIME value to a `day`, `week`, `year`,
  and so on causes an error.

## Examples[¶](#examples "Link to this heading")

The DATE\_TRUNC function examples use the data in the following table:

```
CREATE OR REPLACE TABLE test_date_trunc (
 mydate DATE,
 mytime TIME,
 mytimestamp TIMESTAMP);

INSERT INTO test_date_trunc VALUES (
  '2024-05-09',
  '08:50:48',
  '2024-05-09 08:50:57.891 -0700');

SELECT * FROM test_date_trunc;
```

Copy

```
+------------+----------+-------------------------+
| MYDATE     | MYTIME   | MYTIMESTAMP             |
|------------+----------+-------------------------|
| 2024-05-09 | 08:50:48 | 2024-05-09 08:50:57.891 |
+------------+----------+-------------------------+
```

The following examples show date truncation. In all cases, the returned value
is of the same data type as the input value, but with zeros for the portions,
such as fractional seconds, that were truncated.

Truncate a date down to the year, month, and day:

```
SELECT mydate AS "DATE",
       DATE_TRUNC('year', mydate) AS "TRUNCATED TO YEAR",
       DATE_TRUNC('month', mydate) AS "TRUNCATED TO MONTH",
       DATE_TRUNC('week', mydate) AS "TRUNCATED TO WEEK",
       DATE_TRUNC('day', mydate) AS "TRUNCATED TO DAY"
  FROM test_date_trunc;
```

Copy

```
+------------+-------------------+--------------------+-------------------+------------------+
| DATE       | TRUNCATED TO YEAR | TRUNCATED TO MONTH | TRUNCATED TO WEEK | TRUNCATED TO DAY |
|------------+-------------------+--------------------+-------------------+------------------|
| 2024-05-09 | 2024-01-01        | 2024-05-01         | 2024-05-06        | 2024-05-09       |
+------------+-------------------+--------------------+-------------------+------------------+
```

Truncate a time down to the minute:

```
SELECT mytime AS "TIME",
       DATE_TRUNC('minute', mytime) AS "TRUNCATED TO MINUTE"
  FROM test_date_trunc;
```

Copy

```
+----------+---------------------+
| TIME     | TRUNCATED TO MINUTE |
|----------+---------------------|
| 08:50:48 | 08:50:00            |
+----------+---------------------+
```

Truncate a TIMESTAMP down to the hour, minute, and second:

```
SELECT mytimestamp AS "TIMESTAMP",
       DATE_TRUNC('hour', mytimestamp) AS "TRUNCATED TO HOUR",
       DATE_TRUNC('minute', mytimestamp) AS "TRUNCATED TO MINUTE",
       DATE_TRUNC('second', mytimestamp) AS "TRUNCATED TO SECOND"
  FROM test_date_trunc;
```

Copy

```
+-------------------------+-------------------------+-------------------------+-------------------------+
| TIMESTAMP               | TRUNCATED TO HOUR       | TRUNCATED TO MINUTE     | TRUNCATED TO SECOND     |
|-------------------------+-------------------------+-------------------------+-------------------------|
| 2024-05-09 08:50:57.891 | 2024-05-09 08:00:00.000 | 2024-05-09 08:50:00.000 | 2024-05-09 08:50:57.000 |
+-------------------------+-------------------------+-------------------------+-------------------------+
```

Contrast the DATE\_TRUNC function with the [EXTRACT](extract) function:

```
SELECT DATE_TRUNC('quarter', mytimestamp) AS "TRUNCATED",
       EXTRACT('quarter', mytimestamp) AS "EXTRACTED"
  FROM test_date_trunc;
```

Copy

```
+-------------------------+-----------+
| TRUNCATED               | EXTRACTED |
|-------------------------+-----------|
| 2024-04-01 00:00:00.000 |         2 |
+-------------------------+-----------+
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