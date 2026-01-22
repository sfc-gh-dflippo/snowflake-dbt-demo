---
auto_generated: true
description: Date & time functions
last_scraped: '2026-01-14T16:56:30.592433+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/date_from_parts.html
title: DATE_FROM_PARTS | Snowflake Documentation
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

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)[Date & time](../functions-date-time.md)DATE\_FROM\_PARTS

Categories:
:   [Date & time functions](../functions-date-time)

# DATE\_FROM\_PARTS[¶](#date-from-parts "Link to this heading")

Creates a date from individual numeric components that represent the year,
month, and day of the month.

Aliases:
:   DATEFROMPARTS

## Syntax[¶](#syntax "Link to this heading")

```
DATE_FROM_PARTS( <year>, <month>, <day> )
```

Copy

## Arguments[¶](#arguments "Link to this heading")

`year`
:   The integer expression to use as a year for building a date.

`month`
:   The integer expression to use as a month for building a date, with
    January represented as 1, and December as 12.

`day`
:   The integer expression to use as a day for building a date, usually in
    the 1-31 range.

## Usage notes[¶](#usage-notes "Link to this heading")

DATE\_FROM\_PARTS is typically used to handle values in “normal” ranges
(e.g. months 1-12, days 1-31), but it also handles values from outside these
ranges. This allows, for example, choosing the N-th day in a year, which can
be used to simplify some computations.

Year, month, and day values can be negative (e.g. to calculate a date N months
prior to a specific date). The behavior of negative numbers is not entirely
intuitive; see the Examples section for details.

## Examples[¶](#examples "Link to this heading")

Components in normal ranges:

> ```
> SELECT DATE_FROM_PARTS(1977, 8, 7);
> +-----------------------------+
> | DATE_FROM_PARTS(1977, 8, 7) |
> |-----------------------------|
> | 1977-08-07                  |
> +-----------------------------+
> ```
>
> Copy

Components outside normal ranges:

> * 100th day (from January 1, 2010)
> * 24 months (from January 1, 2010)
>
> ```
> SELECT DATE_FROM_PARTS(2010, 1, 100), DATE_FROM_PARTS(2010, 1 + 24, 1);
> +-------------------------------+----------------------------------+
> | DATE_FROM_PARTS(2010, 1, 100) | DATE_FROM_PARTS(2010, 1 + 24, 1) |
> |-------------------------------+----------------------------------|
> | 2010-04-10                    | 2012-01-01                       |
> +-------------------------------+----------------------------------+
> ```
>
> Copy

Components with zero or negative numbers:

> ```
> SELECT DATE_FROM_PARTS(2004, 1, 1),   -- January 1, 2004, as expected.
>        DATE_FROM_PARTS(2004, 0, 1),   -- This is one month prior to DATE_FROM_PARTS(2004, 1, 1), so it's December 1, 2003.
>                                       -- This is NOT a synonym for January 1, 2004.
>        DATE_FROM_PARTS(2004, -1, 1)   -- This is two months (not one month) before DATE_FROM_PARTS(2004, 1, 1), so it's November 1, 2003.
>        ;
> +-----------------------------+-----------------------------+------------------------------+
> | DATE_FROM_PARTS(2004, 1, 1) | DATE_FROM_PARTS(2004, 0, 1) | DATE_FROM_PARTS(2004, -1, 1) |
> |-----------------------------+-----------------------------+------------------------------|
> | 2004-01-01                  | 2003-12-01                  | 2003-11-01                   |
> +-----------------------------+-----------------------------+------------------------------+
> ```
>
> Copy
>
> ```
> SELECT DATE_FROM_PARTS(2004, 2, 1),   -- February 1, 2004, as expected.
>        DATE_FROM_PARTS(2004, 2, 0),   -- This is one day prior to DATE_FROM_PARTS(2004, 2, 1), so it's January 31, 2004.
>        DATE_FROM_PARTS(2004, 2, -1);  -- Two days prior to DATE_FROM_PARTS(2004, 2, 1) so it's January 30, 2004.
> +-----------------------------+-----------------------------+------------------------------+
> | DATE_FROM_PARTS(2004, 2, 1) | DATE_FROM_PARTS(2004, 2, 0) | DATE_FROM_PARTS(2004, 2, -1) |
> |-----------------------------+-----------------------------+------------------------------|
> | 2004-02-01                  | 2004-01-31                  | 2004-01-30                   |
> +-----------------------------+-----------------------------+------------------------------+
> ```
>
> Copy
>
> ```
> SELECT DATE_FROM_PARTS(2004, -1, -1);  -- Two months and two days prior to DATE_FROM_PARTS(2004, 1, 1), so it's October 30, 2003.
> +-------------------------------+
> | DATE_FROM_PARTS(2004, -1, -1) |
> |-------------------------------|
> | 2003-10-30                    |
> +-------------------------------+
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
3. [Usage notes](#usage-notes)
4. [Examples](#examples)