---
auto_generated: true
description: Date & time functions
last_scraped: '2026-01-14T16:56:59.802639+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/add_months
title: ADD_MONTHS | Snowflake Documentation
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

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)[Date & time](../functions-date-time.md)ADD\_MONTHS

Categories:
:   [Date & time functions](../functions-date-time)

# ADD\_MONTHS[¶](#add-months "Link to this heading")

Adds or subtracts a specified number of months to a date or timestamp, preserving the end-of-month information.

## Syntax[¶](#syntax "Link to this heading")

```
ADD_MONTHS( <date_or_timestamp_expr> , <num_months_expr> )
```

Copy

## Arguments[¶](#arguments "Link to this heading")

**Required:**

`date_or_timestamp_expr`
:   This is the date or timestamp expression to which you want to add
    a specified number of months.

`num_months_expr`
:   This is the number of months you want to add. This should be an
    integer. It may be positive or negative. If the value is a
    non-integer numeric value (for example, FLOAT) the value will be
    rounded to the nearest integer.

## Returns[¶](#returns "Link to this heading")

The data type of the returned value is the same as the data type of the
first parameter. For example, if the input is a `DATE`, then the
output is a `DATE`. If the input is a `TIMESTAMP_NTZ`, then the
output is a `TIMESTAMP_NTZ`.

## Usage notes[¶](#usage-notes "Link to this heading")

* ADD\_MONTHS returns slightly different results than [DATEADD](dateadd) used with a `MONTH` component:

  + For both ADD\_MONTHS and [DATEADD](dateadd), if the result month has fewer days than the original day, the result day of the month is the last day of the result month.
  + For ADD\_MONTHS only, if the original day is the last day of the month, the result day of month will be the last day of the result month.
* `num_months_expr` can be a positive or negative integer to either add or subtract months, respectively.

## Examples[¶](#examples "Link to this heading")

Add 2 months to a date and cast the date to a timestamp with no time zone:

> ```
> SELECT ADD_MONTHS('2016-05-15'::timestamp_ntz, 2) AS RESULT;
> +-------------------------+
> | RESULT                  |
> |-------------------------|
> | 2016-07-15 00:00:00.000 |
> +-------------------------+
> ```
>
> Copy

Demonstrate preservation of end-of-month information:

> * Add one month to the last day of February 2016 (a leap year).
> * Subtract one month from the last day of May 2016.
>
>   > ```
>   > SELECT ADD_MONTHS('2016-02-29'::date, 1) AS RESULT;
>   > +------------+
>   > | RESULT     |
>   > |------------|
>   > | 2016-03-31 |
>   > +------------+
>   > ```
>   >
>   > Copy
>   >
>   > ```
>   > SELECT ADD_MONTHS('2016-05-31'::date, -1) AS RESULT;
>   > +------------+
>   > | RESULT     |
>   > |------------|
>   > | 2016-04-30 |
>   > +------------+
>   > ```
>   >
>   > Copy

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