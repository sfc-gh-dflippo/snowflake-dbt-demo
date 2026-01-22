---
auto_generated: true
description: Date & time functions
last_scraped: '2026-01-14T16:57:15.901875+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/year.html
title: YEAR* / DAY* / WEEK* / MONTH / QUARTER | Snowflake Documentation
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

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)[Date & time](../functions-date-time.md)YEAR

Categories:
:   [Date & time functions](../functions-date-time)

# YEAR\* / DAY\* / WEEK\* / MONTH / QUARTER[¶](#year-day-week-month-quarter "Link to this heading")

Extracts the corresponding date part from a date or timestamp.

These functions are alternatives to using the [DATE\_PART](date_part) (or [EXTRACT](extract)) function with the
equivalent date part (see [Supported date and time parts](../functions-date-time.html#label-supported-date-time-parts)).

See also:
:   [HOUR / MINUTE / SECOND](hour-minute-second)

## Syntax[¶](#syntax "Link to this heading")

```
YEAR( <date_or_timestamp_expr> )

YEAROFWEEK( <date_or_timestamp_expr> )
YEAROFWEEKISO( <date_or_timestamp_expr> )

DAY( <date_or_timestamp_expr> )

DAYOFMONTH( <date_or_timestamp_expr> )
DAYOFWEEK( <date_or_timestamp_expr> )
DAYOFWEEKISO( <date_or_timestamp_expr> )
DAYOFYEAR( <date_or_timestamp_expr> )

WEEK( <date_or_timestamp_expr> )

WEEKOFYEAR( <date_or_timestamp_expr> )
WEEKISO( <date_or_timestamp_expr> )

MONTH( <date_or_timestamp_expr> )

QUARTER( <date_or_timestamp_expr> )
```

Copy

## Arguments[¶](#arguments "Link to this heading")

`date_or_timestamp_expr`
:   A date or a timestamp, or an expression that can be evaluated to a date or a timestamp.

## Returns[¶](#returns "Link to this heading")

This function returns a value of type NUMBER.

## Usage notes[¶](#usage-notes "Link to this heading")

| Function name | Date part extracted from input date or timestamp | Possible values |
| --- | --- | --- |
| YEAR | Year | Any valid year (for example, 2025) |
| YEAROFWEEK [1] | Year that the extracted week belongs to | Any valid year (for example, 2025) |
| YEAROFWEEKISO | Year that the extracted week belongs to using [ISO semantics](../functions-date-time.html#label-calendar-weeks-weekdays) | Any valid year (for example, 2025) |
| DAY , DAYOFMONTH | Day (number) of the month | 1 to 31 |
| DAYOFWEEK [1] | Day (number) of the week | 0 to 7 |
| DAYOFWEEKISO | Day (number) of the week using [ISO semantics](../functions-date-time.html#label-calendar-weeks-weekdays) | 1 to 7 |
| DAYOFYEAR | Day (number) of the year | 1 to 366 |
| WEEK , WEEKOFYEAR [1] | Week (number) of the year | 1 to 54 |
| WEEKISO | Week (number) of the year using [ISO semantics](../functions-date-time.html#label-calendar-weeks-weekdays) | 1 to 53 |
| MONTH | Month (number) of the year | 1 to 12 |
| QUARTER | Quarter (number) of the year | 1 to 4 |

[1] Results dictated by the values set for the WEEK\_OF\_YEAR\_POLICY and/or WEEK\_START session parameters.

For details about ISO semantics and the parameter, see [Calendar weeks and weekdays](../functions-date-time.html#label-calendar-weeks-weekdays).

## Examples[¶](#examples "Link to this heading")

The following example demonstrates the use of the functions YEAR, QUARTER, MONTH, DAY, DAYOFWEEK,
and DAYOFYEAR:

```
SELECT '2025-04-11T23:39:20.123-07:00'::TIMESTAMP AS tstamp,
       YEAR(tstamp) AS "YEAR",
       QUARTER(tstamp) AS "QUARTER OF YEAR",
       MONTH(tstamp) AS "MONTH",
       DAY(tstamp) AS "DAY",
       DAYOFMONTH(tstamp) AS "DAY OF MONTH",
       DAYOFYEAR(tstamp) AS "DAY OF YEAR";
```

Copy

```
+-------------------------+------+-----------------+-------+-----+--------------+-------------+
| TSTAMP                  | YEAR | QUARTER OF YEAR | MONTH | DAY | DAY OF MONTH | DAY OF YEAR |
|-------------------------+------+-----------------+-------+-----+--------------+-------------|
| 2025-04-11 23:39:20.123 | 2025 |               2 |     4 |  11 |           11 |         101 |
+-------------------------+------+-----------------+-------+-----+--------------+-------------+
```

The following example demonstrates the use of the functions WEEK, WEEKISO, WEEKOFYEAR, YEAROFWEEK, and
YEAROFWEEKISO. The session parameter [WEEK\_OF\_YEAR\_POLICY](../parameters.html#label-week-of-year-policy) is set to `1`, so that the first week
of the year is the week that contains January 1st of that year.

```
ALTER SESSION SET WEEK_OF_YEAR_POLICY = 1;
```

Copy

```
SELECT '2016-01-02T23:39:20.123-07:00'::TIMESTAMP AS tstamp,
       WEEK(tstamp) AS "WEEK",
       WEEKISO(tstamp) AS "WEEK ISO",
       WEEKOFYEAR(tstamp) AS "WEEK OF YEAR",
       YEAROFWEEK(tstamp) AS "YEAR OF WEEK",
       YEAROFWEEKISO(tstamp) AS "YEAR OF WEEK ISO";
```

Copy

```
+-------------------------+------+----------+--------------+--------------+------------------+
| TSTAMP                  | WEEK | WEEK ISO | WEEK OF YEAR | YEAR OF WEEK | YEAR OF WEEK ISO |
|-------------------------+------+----------+--------------+--------------+------------------|
| 2016-01-02 23:39:20.123 |    1 |       53 |            1 |         2016 |             2015 |
+-------------------------+------+----------+--------------+--------------+------------------+
```

The following example also demonstrates the use of the functions WEEK, WEEKISO, WEEKOFYEAR, YEAROFWEEK, and
YEAROFWEEKISO. The session parameter WEEK\_OF\_YEAR\_POLICY is set to indicate that the first week
of the year is the first week of the year that contains at least four days from that year. In this example,
the week December 27, 2015 through January 2, 2016 is considered the last week of 2015, not the first week
of 2016. Even though the week contains Friday January 1, 2016, less than half of the week is in 2016.

```
ALTER SESSION SET WEEK_OF_YEAR_POLICY = 0;
```

Copy

```
SELECT '2016-01-02T23:39:20.123-07:00'::TIMESTAMP AS tstamp,
       WEEK(tstamp) AS "WEEK",
       WEEKISO(tstamp) AS "WEEK ISO",
       WEEKOFYEAR(tstamp) AS "WEEK OF YEAR",
       YEAROFWEEK(tstamp) AS "YEAR OF WEEK",
       YEAROFWEEKISO(tstamp) AS "YEAR OF WEEK ISO";
```

Copy

```
+-------------------------+------+----------+--------------+--------------+------------------+
| TSTAMP                  | WEEK | WEEK ISO | WEEK OF YEAR | YEAR OF WEEK | YEAR OF WEEK ISO |
|-------------------------+------+----------+--------------+--------------+------------------|
| 2016-01-02 23:39:20.123 |   53 |       53 |           53 |         2015 |             2015 |
+-------------------------+------+----------+--------------+--------------+------------------+
```

The following example demonstrates the use of the functions DAYOFWEEK and DAYOFWEEKISO.
The session parameter [WEEK\_START](../parameters.html#label-week-start) is set to indicate that the week starts on Sunday.

```
ALTER SESSION SET WEEK_START = 7;
```

Copy

The timestamp in the following query is for April 5, 2025, which was a Saturday. The DAYOFWEEK function
returns `7` for Saturday, because the first day of the week is set to Sunday. The DAYOFWEEKISO function
returns `6` because the first day of the week using ISO semantics is Monday. For more information about ISO
semantics and the WEEK\_START parameter, see [Calendar weeks and weekdays](../functions-date-time.html#label-calendar-weeks-weekdays).

```
SELECT '2025-04-05T23:39:20.123-07:00'::TIMESTAMP AS tstamp,
       DAYOFWEEK(tstamp) AS "DAY OF WEEK",
       DAYOFWEEKISO(tstamp) AS "DAY OF WEEK ISO";
```

Copy

```
+-------------------------+-------------+-----------------+
| TSTAMP                  | DAY OF WEEK | DAY OF WEEK ISO |
|-------------------------+-------------+-----------------|
| 2025-04-05 23:39:20.123 |           7 |               6 |
+-------------------------+-------------+-----------------+
```

The following example also demonstrates the use of the functions DAYOFWEEK and DAYOFWEEKISO.
The session parameter WEEK\_START is set to indicate that the week starts on Monday.

```
ALTER SESSION SET WEEK_START = 1;
```

Copy

```
SELECT '2025-04-05T23:39:20.123-07:00'::TIMESTAMP AS tstamp,
       DAYOFWEEK(tstamp) AS "DAY OF WEEK",
       DAYOFWEEKISO(tstamp) AS "DAY OF WEEK ISO";
```

Copy

```
+-------------------------+-------------+-----------------+
| TSTAMP                  | DAY OF WEEK | DAY OF WEEK ISO |
|-------------------------+-------------+-----------------|
| 2025-04-05 23:39:20.123 |           6 |               6 |
+-------------------------+-------------+-----------------+
```

For more examples, see [Working with date and time values](../date-time-examples).

For more detailed examples of the week-related functions (DAYOFWEEK, WEEK, WEEKOFYEAR, YEAROFWEEK, and so on),
see [Calendar weeks and weekdays](../functions-date-time.html#label-calendar-weeks-weekdays).

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