---
auto_generated: true
description: Date & time functions
last_scraped: '2026-01-14T16:57:22.490271+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/convert_timezone.html
title: CONVERT_TIMEZONE | Snowflake Documentation
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

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)[Date & time](../functions-date-time.md)CONVERT\_TIMEZONE

Categories:
:   [Date & time functions](../functions-date-time)

# CONVERT\_TIMEZONE[¶](#convert-timezone "Link to this heading")

Converts a timestamp to another time zone.

## Syntax[¶](#syntax "Link to this heading")

```
CONVERT_TIMEZONE( <source_tz> , <target_tz> , <source_timestamp_ntz> )

CONVERT_TIMEZONE( <target_tz> , <source_timestamp> )
```

Copy

## Arguments[¶](#arguments "Link to this heading")

`source_tz`
:   String specifying the time zone for the input timestamp. Required for timestamps with no time zone (i.e. TIMESTAMP\_NTZ).

`target_tz`
:   String specifying the time zone to which the input timestamp is converted.

`source_timestamp_ntz`
:   For the 3-argument version, string specifying the timestamp to convert (must be TIMESTAMP\_NTZ).

`source_timestamp`
:   For the 2-argument version, string specifying the timestamp to convert (can be any timestamp variant, including TIMESTAMP\_NTZ).

## Returns[¶](#returns "Link to this heading")

Returns a value of type TIMESTAMP\_NTZ, TIMESTAMP\_TZ, or NULL:

* For the 3-argument version, returns a value of type TIMESTAMP\_NTZ.
* For the 2-argument version, returns a value of type TIMESTAMP\_TZ.
* If any argument is NULL, returns NULL.

## Usage notes[¶](#usage-notes "Link to this heading")

* The display format for timestamps in the output is determined by the
  [timestamp output format](../date-time-input-output.html#label-session-parameters-for-dates-times-timestamps) for the current
  session and the data type of the returned timestamp value.
* For the 3-argument version, the “wallclock” time in the result represents the same moment in time as the input “wallclock”
  in the input time zone, but in the target time zone.
* For the 2-argument version, the `source_timestamp` argument typically includes the time zone. If the value
  is of type TIMESTAMP\_TZ, the time zone is taken from its value. Otherwise, the current session time zone is used.
* For `source_tz` and `target_tz`, you can specify a [time zone name](https://data.iana.org/time-zones/tzdb-2025b/zone1970.tab) or a [link name](https://data.iana.org/time-zones/tzdb-2025b/backward) from release
  2025b of the [IANA Time Zone Database](https://www.iana.org/time-zones) (for example, `America/Los_Angeles`, `Europe/London`, `UTC`,
  `Etc/GMT`, and so on).

  Note

  + Time zone names are case-sensitive and must be enclosed in single quotes (e.g. `'UTC'`).
  + Snowflake does not support the majority of timezone [abbreviations](https://en.wikipedia.org/wiki/List_of_time_zone_abbreviations) (e.g. `PDT`, `EST`, etc.) because a
    given abbreviation might refer to one of several different time zones. For example, `CST` might refer to Central
    Standard Time in North America (UTC-6), Cuba Standard Time (UTC-5), and China Standard Time (UTC+8).

## Examples[¶](#examples "Link to this heading")

To use the default [timestamp output format](../date-time-input-output.html#label-session-parameters-for-dates-times-timestamps)
for the timestamps returned in the examples, unset the TIMESTAMP\_OUTPUT\_FORMAT parameter in the current session:

```
ALTER SESSION UNSET TIMESTAMP_OUTPUT_FORMAT;
```

Copy

### Examples that specify a source time zone[¶](#examples-that-specify-a-source-time-zone "Link to this heading")

The following examples use the 3-argument version of the CONVERT\_TIMEZONE function and specify a `source_tz`
value. These examples return TIMESTAMP\_NTZ values.

Convert a “wallclock” time in Los Angeles to the matching “wallclock” time in New York:

```
SELECT CONVERT_TIMEZONE(
  'America/Los_Angeles',
  'America/New_York',
  '2024-01-01 14:00:00'::TIMESTAMP_NTZ
) AS conv;
```

Copy

```
+-------------------------+
| CONV                    |
|-------------------------|
| 2024-01-01 17:00:00.000 |
+-------------------------+
```

Convert a “wallclock” time in Warsaw to the matching “wallclock” time in UTC:

```
SELECT CONVERT_TIMEZONE(
  'Europe/Warsaw',
  'UTC',
  '2024-01-01 00:00:00'::TIMESTAMP_NTZ
) AS conv;
```

Copy

```
+-------------------------+
| CONV                    |
|-------------------------|
| 2023-12-31 23:00:00.000 |
+-------------------------+
```

### Examples that do not specify a source time zone[¶](#examples-that-do-not-specify-a-source-time-zone "Link to this heading")

The following examples use the 2-argument version of the CONVERT\_TIMEZONE function. These examples return
TIMESTAMP\_TZ values. Therefore, the returned values include an offset that shows the difference between
the timestamp’s time zone and Coordinated Universal Time (UTC). For example, the `America/Los_Angeles`
time zone has an offset of `-0700` to show that it is seven hours behind UTC.

Convert a string specifying a TIMESTAMP\_TZ value to a different time zone:

```
SELECT CONVERT_TIMEZONE(
  'America/Los_Angeles',
  '2024-04-05 12:00:00 +02:00'
) AS time_in_la;
```

Copy

```
+-------------------------------+
| TIME_IN_LA                    |
|-------------------------------|
| 2024-04-05 03:00:00.000 -0700 |
+-------------------------------+
```

Show the current “wallclock” time in different time zones:

```
SELECT
  CURRENT_TIMESTAMP() AS now_in_la,
  CONVERT_TIMEZONE('America/New_York', CURRENT_TIMESTAMP()) AS now_in_nyc,
  CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP()) AS now_in_paris,
  CONVERT_TIMEZONE('Asia/Tokyo', CURRENT_TIMESTAMP()) AS now_in_tokyo;
```

Copy

```
+-------------------------------+-------------------------------+-------------------------------+-------------------------------+
| NOW_IN_LA                     | NOW_IN_NYC                    | NOW_IN_PARIS                  | NOW_IN_TOKYO                  |
|-------------------------------+-------------------------------+-------------------------------+-------------------------------|
| 2024-06-12 08:52:53.114 -0700 | 2024-06-12 11:52:53.114 -0400 | 2024-06-12 17:52:53.114 +0200 | 2024-06-13 00:52:53.114 +0900 |
+-------------------------------+-------------------------------+-------------------------------+-------------------------------+
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