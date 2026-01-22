---
auto_generated: true
description: Date & time functions
last_scraped: '2026-01-14T16:58:01.647448+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/timestamp_from_parts
title: TIMESTAMP_FROM_PARTS | Snowflake Documentation
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

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)[Date & time](../functions-date-time.md)TIMESTAMP\_FROM\_PARTS

Categories:
:   [Date & time functions](../functions-date-time)

# TIMESTAMP\_FROM\_PARTS[¶](#timestamp-from-parts "Link to this heading")

Creates a timestamp from individual numeric components. If no time zone is in effect, the function can be used to create a timestamp from a date expression and a time expression.

Aliases:
:   TIMESTAMPFROMPARTS

Variations (and Aliases):
:   TIMESTAMP\_LTZ\_FROM\_PARTS , TIMESTAMPLTZFROMPARTS

    TIMESTAMP\_NTZ\_FROM\_PARTS , TIMESTAMPNTZFROMPARTS

    TIMESTAMP\_TZ\_FROM\_PARTS , TIMESTAMPTZFROMPARTS

## Syntax[¶](#syntax "Link to this heading")

```
TIMESTAMP_FROM_PARTS( <year>, <month>, <day>, <hour>, <minute>, <second> [, <nanosecond> ] [, <time_zone> ] )

TIMESTAMP_FROM_PARTS( <date_expr>, <time_expr> )
```

Copy

```
TIMESTAMP_LTZ_FROM_PARTS( <year>, <month>, <day>, <hour>, <minute>, <second> [, <nanosecond>] )
```

Copy

```
TIMESTAMP_NTZ_FROM_PARTS( <year>, <month>, <day>, <hour>, <minute>, <second> [, <nanosecond>] )

TIMESTAMP_NTZ_FROM_PARTS( <date_expr>, <time_expr> )
```

Copy

```
TIMESTAMP_TZ_FROM_PARTS( <year>, <month>, <day>, <hour>, <minute>, <second> [, <nanosecond>] [, <time_zone>] )
```

Copy

Note

The date and time expression version of TIMESTAMP\_FROM\_PARTS is only valid when the [TIMESTAMP\_TYPE\_MAPPING](../parameters.html#label-timestamp-type-mapping) session parameter is set to TIMESTAMP\_NTZ.

## Arguments[¶](#arguments "Link to this heading")

**Required:**

`year`
:   An integer expression to use as a year for building a timestamp.

`month`
:   An integer expression to use as a month for building a timestamp, with January represented as `1`, and December as `12`.

`day`
:   An integer expression to use as a day for building a timestamp, usually in the `1`-`31` range.

`hour`
:   An integer expression to use as an hour for building a timestamp, usually in the `0`-`23` range.

`minute`
:   An integer expression to use as a minute for building a timestamp, usually in the `0`-`59` range.

`second`
:   An integer expression to use as a second for building a timestamp, usually in the `0`-`59` range.

`date_expr` , `time_expr`
:   Specifies the date and time expressions to use for building a timestamp where `date_expr` provides the year, month, and day for the timestamp and `time_expr` provides the hour,
    minute, second, and nanoseconds within the day. Only valid for:

    * TIMESTAMP\_FROM\_PARTS (when the [TIMESTAMP\_TYPE\_MAPPING](../parameters.html#label-timestamp-type-mapping) session parameter is set to TIMESTAMP\_NTZ)
    * TIMESTAMP\_NTZ\_FROM\_PARTS

**Optional:**

`nanoseconds`
:   An integer expression to use as a nanosecond for building a timestamp, usually in the `0`-`999999999` range.

`time_zone`
:   A string expression to use as a time zone for building a timestamp (e.g. `America/Los_Angeles`). Only valid for:

    * TIMESTAMP\_FROM\_PARTS (when the [TIMESTAMP\_TYPE\_MAPPING](../parameters.html#label-timestamp-type-mapping) session parameter is set to TIMESTAMP\_TZ)
    * TIMESTAMP\_TZ\_FROM\_PARTS

## Usage notes[¶](#usage-notes "Link to this heading")

* TIMESTAMP\_FROM\_PARTS variations are typically used to handle values in the “normal” value ranges (e.g. months `1`-`12`, days `1`-`31`, hours `0`-`23`, etc.); however, they can also
  handle values from outside these ranges. This allows choosing the Nth day in a year or Nth second in a day, which can be useful for simplifying some computations.
* TIMESTAMP\_FROM\_PARTS is equivalent to the variation specified by the [TIMESTAMP\_TYPE\_MAPPING](../parameters.html#label-timestamp-type-mapping) session parameter (default is TIMESTAMP\_NTZ).

## Examples[¶](#examples "Link to this heading")

Set the session variables that control output format and time zone:

> ```
> ALTER SESSION SET TIMESTAMP_OUTPUT_FORMAT='YYYY-MM-DD HH24:MI:SS.FF9 TZH:TZM';
> ALTER SESSION SET TIMESTAMP_NTZ_OUTPUT_FORMAT='YYYY-MM-DD HH24:MI:SS.FF9 TZH:TZM';
> ALTER SESSION SET TIMEZONE='America/New_York';
> ```
>
> Copy

Using `TIMESTAMP_LTZ_FROM_PARTS`:

> ```
> SELECT TIMESTAMP_LTZ_FROM_PARTS(2013, 4, 5, 12, 00, 00);
> +--------------------------------------------------+
> | TIMESTAMP_LTZ_FROM_PARTS(2013, 4, 5, 12, 00, 00) |
> |--------------------------------------------------|
> | 2013-04-05 12:00:00.000000000 -0400              |
> +--------------------------------------------------+
> ```
>
> Copy

Using `TIMESTAMP_NTZ_FROM_PARTS`:

> ```
> select timestamp_ntz_from_parts(2013, 4, 5, 12, 00, 00, 987654321);
> +-------------------------------------------------------------+
> | TIMESTAMP_NTZ_FROM_PARTS(2013, 4, 5, 12, 00, 00, 987654321) |
> |-------------------------------------------------------------|
> | 2013-04-05 12:00:00.987654321                               |
> +-------------------------------------------------------------+
> ```
>
> Copy

Using `TIMESTAMP_NTZ_FROM_PARTS` with a date and time rather than with
year, month, day, hour, etc.:

> ```
> select timestamp_ntz_from_parts(to_date('2013-04-05'), to_time('12:00:00'));
> +----------------------------------------------------------------------+
> | TIMESTAMP_NTZ_FROM_PARTS(TO_DATE('2013-04-05'), TO_TIME('12:00:00')) |
> |----------------------------------------------------------------------|
> | 2013-04-05 12:00:00.000000000                                        |
> +----------------------------------------------------------------------+
> ```
>
> Copy

Using `TIMESTAMP_TZ_FROM_PARTS` with a session-default time zone (‘America/New\_York’/-0400):

> ```
> select timestamp_tz_from_parts(2013, 4, 5, 12, 00, 00);
> +-------------------------------------------------+
> | TIMESTAMP_TZ_FROM_PARTS(2013, 4, 5, 12, 00, 00) |
> |-------------------------------------------------|
> | 2013-04-05 12:00:00.000000000 -0400             |
> +-------------------------------------------------+
> ```
>
> Copy

Using `TIMESTAMP_TZ_FROM_PARTS` with a specified time zone (‘America/Los\_Angeles’/-0700); note also the use of 0 as the nanoseconds argument:

> ```
> select timestamp_tz_from_parts(2013, 4, 5, 12, 00, 00, 0, 'America/Los_Angeles');
> +---------------------------------------------------------------------------+
> | TIMESTAMP_TZ_FROM_PARTS(2013, 4, 5, 12, 00, 00, 0, 'AMERICA/LOS_ANGELES') |
> |---------------------------------------------------------------------------|
> | 2013-04-05 12:00:00.000000000 -0700                                       |
> +---------------------------------------------------------------------------+
> ```
>
> Copy

Handling values outside normal ranges (subtracting 1 hour by specifying -3600 seconds):

> ```
> select timestamp_from_parts(2013, 4, 5, 12, 0, -3600);
> +------------------------------------------------+
> | TIMESTAMP_FROM_PARTS(2013, 4, 5, 12, 0, -3600) |
> |------------------------------------------------|
> | 2013-04-05 11:00:00.000000000                  |
> +------------------------------------------------+
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