---
auto_generated: true
description: This family of functions can be used to construct, convert, extract,
  or modify date, time, and timestamp data.
last_scraped: '2026-01-14T16:54:50.100782+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions-date-time
title: Date & time functions | Snowflake Documentation
---

1. [Overview](../reference.md)
2. [SQL data types reference](../sql-reference-data-types.md)
3. [SQL command reference](../sql-reference-commands.md)
4. [Function and stored procedure reference](../sql-reference-functions.md)

   * [Summary of functions](intro-summary-operators-functions.md)
   * [All functions (alphabetical)](functions-all.md)")
   * [Aggregate](functions-aggregation.md)
   * AI Functions

     * Scalar functions

       * [AI\_CLASSIFY](functions/ai_classify.md)
       * [AI\_COMPLETE](functions/ai_complete.md)
       * [AI\_COUNT\_TOKENS](functions/ai_count_tokens.md)
       * [AI\_EMBED](functions/ai_embed.md)
       * [AI\_EXTRACT](functions/ai_extract.md)
       * [AI\_FILTER](functions/ai_filter.md)
       * [AI\_PARSE\_DOCUMENT](functions/ai_parse_document.md)
       * [AI\_REDACT](functions/ai_redact.md)
       * [AI\_SENTIMENT](functions/ai_sentiment.md)
       * [AI\_SIMILARITY](functions/ai_similarity.md)
       * [AI\_TRANSCRIBE](functions/ai_transcribe.md)
       * [AI\_TRANSLATE](functions/ai_translate.md)
       * [CLASSIFY\_TEXT (SNOWFLAKE.CORTEX)](functions/classify_text-snowflake-cortex.md)")
       * [COMPLETE (SNOWFLAKE.CORTEX)](functions/complete-snowflake-cortex.md)")
       * [COMPLETE multimodal (images) (SNOWFLAKE.CORTEX)](functions/complete-snowflake-cortex-multimodal.md) (SNOWFLAKE.CORTEX)")
       * [EMBED\_TEXT\_768 (SNOWFLAKE.CORTEX)](functions/embed_text-snowflake-cortex.md)")
       * [EMBED\_TEXT\_1024 (SNOWFLAKE.CORTEX)](functions/embed_text_1024-snowflake-cortex.md)")
       * [ENTITY\_SENTIMENT (SNOWFLAKE.CORTEX)](functions/entity_sentiment-snowflake-cortex.md)")
       * [EXTRACT\_ANSWER (SNOWFLAKE.CORTEX)](functions/extract_answer-snowflake-cortex.md)")
       * [FINETUNE (SNOWFLAKE.CORTEX)](functions/finetune-snowflake-cortex.md)")
       * [PARSE\_DOCUMENT (SNOWFLAKE.CORTEX)](functions/parse_document-snowflake-cortex.md)")
       * [SENTIMENT (SNOWFLAKE.CORTEX)](functions/sentiment-snowflake-cortex.md)")
       * [SUMMARIZE (SNOWFLAKE.CORTEX)](functions/summarize-snowflake-cortex.md)")
       * [TRANSLATE (SNOWFLAKE.CORTEX)](functions/translate-snowflake-cortex.md)")
     * Aggregate functions

       * [AI\_AGG](functions/ai_agg.md)
       * [AI\_SUMMARIZE\_AGG](functions/ai_summarize_agg.md)
     * Helper functions

       * [COUNT\_TOKENS (SNOWFLAKE.CORTEX)](functions/count_tokens-snowflake-cortex.md)")
       * [SEARCH\_PREVIEW (SNOWFLAKE.CORTEX)](functions/search_preview-snowflake-cortex.md)")
       * [SPLIT\_TEXT\_MARKDOWN\_HEADER (SNOWFLAKE.CORTEX)](functions/split_text_markdown_header-snowflake-cortex.md)")
       * [SPLIT\_TEXT\_RECURSIVE\_CHARACTER (SNOWFLAKE.CORTEX)](functions/split_text_recursive_character-snowflake-cortex.md)")
       * [TRY\_COMPLETE (SNOWFLAKE.CORTEX)](functions/try_complete-snowflake-cortex.md)")
   * [Bitwise expression](expressions-byte-bit.md)
   * [Conditional expression](expressions-conditional.md)
   * [Context](functions-context.md)
   * [Conversion](functions-conversion.md)
   * [Data generation](functions-data-generation.md)
   * [Data metric](functions-data-metric.md)
   * [Date & time](functions-date-time.md)

     + Construction
     + [DATE\_FROM\_PARTS](functions/date_from_parts.md)
     + [TIME\_FROM\_PARTS](functions/time_from_parts.md)
     + [TIMESTAMP\_FROM\_PARTS](functions/timestamp_from_parts.md)
     + Extraction
     + [DATE\_PART](functions/date_part.md)
     + [DAYNAME](functions/dayname.md)
     + [EXTRACT](functions/extract.md)
     + [HOUR](functions/hour-minute-second.md)
     + [MINUTE](functions/hour-minute-second.md)
     + [SECOND](functions/hour-minute-second.md)
     + [LAST\_DAY](functions/last_day.md)
     + [MONTHNAME](functions/monthname.md)
     + [NEXT\_DAY](functions/next_day.md)
     + [PREVIOUS\_DAY](functions/previous_day.md)
     + [YEAR](functions/year.md)
     + [YEAROFWEEK](functions/year.md)
     + [YEAROFWEEKISO](functions/year.md)
     + [DAY](functions/year.md)
     + [DAYOFMONTH](functions/year.md)
     + [DAYOFWEEK](functions/year.md)
     + [DAYOFWEEKISO](functions/year.md)
     + [DAYOFYEAR](functions/year.md)
     + [WEEK](functions/year.md)
     + [WEEKOFYEAR](functions/year.md)
     + [WEEKISO](functions/year.md)
     + [MONTH](functions/year.md)
     + [QUARTER](functions/year.md)
     + Addition & subtraction
     + [ADD\_MONTHS](functions/add_months.md)
     + [DATEADD](functions/dateadd.md)
     + [DATEDIFF](functions/datediff.md)
     + [MONTHS\_BETWEEN](functions/months_between.md)
     + [TIMEADD](functions/timeadd.md)
     + [TIMEDIFF](functions/timediff.md)
     + [TIMESTAMPADD](functions/timestampadd.md)
     + [TIMESTAMPDIFF](functions/timestampdiff.md)
     + Truncation
     + [DATE\_TRUNC](functions/date_trunc.md)
     + [TIME\_SLICE](functions/time_slice.md)
     + [TRUNCATE, TRUNC](functions/trunc2.md)
     + Conversion
     + [TO\_DATE](functions/to_date.md)
     + [DATE](functions/to_date.md)
     + [TO\_TIME](functions/to_time.md)
     + [TIME](functions/to_time.md)
     + [TO\_TIMESTAMP](functions/to_timestamp.md)
     + [TO\_TIMESTAMP\_LTZ](functions/to_timestamp.md)
     + [TO\_TIMESTAMP\_NTZ](functions/to_timestamp.md)
     + [TO\_TIMESTAMP\_TZ](functions/to_timestamp.md)
     + [TRY\_TO\_DATE](functions/try_to_date.md)
     + [TRY\_TO\_TIME](functions/try_to_time.md)
     + [TRY\_TO\_TIMESTAMP](functions/try_to_timestamp.md)
     + [TRY\_TO\_TIMESTAMP\_LTZ](functions/try_to_timestamp.md)
     + [TRY\_TO\_TIMESTAMP\_NTZ](functions/try_to_timestamp.md)
     + [TRY\_TO\_TIMESTAMP\_TZ](functions/try_to_timestamp.md)
     + Time zone
     + [CONVERT\_TIMEZONE](functions/convert_timezone.md)
     + Alerts
     + [LAST\_SUCCESSFUL\_SCHEDULED\_TIME](functions/last_successful_scheduled_time.md)
     + [SCHEDULED\_TIME](functions/scheduled_time.md)
   * [Differential privacy](functions-differential-privacy.md)
   * [Encryption](functions-encryption.md)
   * [File](functions-file.md)
   * [Geospatial](functions-geospatial.md)
   * [Hash](functions-hash-scalar.md)
   * [Metadata](functions-metadata.md)
   * [ML Model Monitors](functions-model-monitors.md)
   * [Notification](functions-notification.md)
   * [Numeric](functions-numeric.md)
   * [Organization users and organization user groups](functions-organization-users.md)
   * [Regular expressions](functions-regexp.md)
   * [Semi-structured and structured data](functions-semistructured.md)
   * [Snowpark Container Services](functions-spcs.md)
   * [String & binary](functions-string.md)
   * [System](functions-system.md)
   * [Table](functions-table.md)
   * [Vector](functions-vector.md)
   * [Window](functions-window.md)
   * [Stored procedures](../sql-reference-stored-procedures.md)
5. [Class reference](../sql-reference-classes.md)
6. [Scripting reference](../sql-reference-snowflake-scripting.md)
7. [General reference](../sql-reference.md)
8. [API reference](../api-reference.md)

[Reference](../reference.md)[Function and stored procedure reference](../sql-reference-functions.md)Date & time

# Date & time functions[¶](#date-time-functions "Link to this heading")

This family of functions can be used to construct, convert, extract, or modify date, time, and timestamp data.

## List of functions[¶](#list-of-functions "Link to this heading")

| Sub-category | Function | Notes |
| --- | --- | --- |
| **Construction** | [DATE\_FROM\_PARTS](functions/date_from_parts) |  |
| [TIME\_FROM\_PARTS](functions/time_from_parts) |  |
| [TIMESTAMP\_FROM\_PARTS](functions/timestamp_from_parts) |  |
| **Extraction** | [DATE\_PART](functions/date_part) | Accepts all date and time parts (see [Supported date and time parts](#label-supported-date-time-parts)). |
| [DAYNAME](functions/dayname) |  |
| [EXTRACT](functions/extract) | Alternative for [DATE\_PART](functions/date_part). |
| [HOUR / MINUTE / SECOND](functions/hour-minute-second) | Alternative for [DATE\_PART](functions/date_part). |
| [LAST\_DAY](functions/last_day) | Accepts relevant date parts (see [Supported date and time parts](#label-supported-date-time-parts)). |
| [MONTHNAME](functions/monthname) |  |
| [NEXT\_DAY](functions/next_day) |  |
| [PREVIOUS\_DAY](functions/previous_day) |  |
| [YEAR\* / DAY\* / WEEK\* / MONTH / QUARTER](functions/year) | Alternative for [DATE\_PART](functions/date_part). |
| **Addition/subtraction** | [ADD\_MONTHS](functions/add_months) |  |
| [DATEADD](functions/dateadd) | Accepts relevant date and time parts (see [Supported date and time parts](#label-supported-date-time-parts)). |
| [DATEDIFF](functions/datediff) | Accepts relevant date and time parts (see [Supported date and time parts](#label-supported-date-time-parts)). |
| [MONTHS\_BETWEEN](functions/months_between) |  |
| [TIMEADD](functions/timeadd) | Alias for [DATEADD](functions/dateadd). |
| [TIMEDIFF](functions/timediff) | Alias for [DATEDIFF](functions/datediff). |
| [TIMESTAMPADD](functions/timestampadd) | Alias for [DATEADD](functions/dateadd). |
| [TIMESTAMPDIFF](functions/timestampdiff) | Alias for [DATEDIFF](functions/datediff). |
| **Truncation** | [DATE\_TRUNC](functions/date_trunc) | Accepts relevant date and time parts (see [Supported date and time parts](#label-supported-date-time-parts)). |
| [TIME\_SLICE](functions/time_slice) | Allows a time to be “rounded” to the start of an evenly-spaced interval. |
| [TRUNCATE, TRUNC](functions/trunc2) | Alternative for [DATE\_TRUNC](functions/date_trunc). |
| **Conversion** | [TO\_DATE , DATE](functions/to_date) | Supports conversions based on string, timestamp, and VARIANT expressions. Supports integers for conversions based on the beginning of the Unix epoch. |
| [TO\_TIME , TIME](functions/to_time) | Supports conversions based on string, timestamp, and VARIANT expressions. Supports integers for conversions based on the beginning of the Unix epoch. |
| [TO\_TIMESTAMP / TO\_TIMESTAMP\_\*](functions/to_timestamp) | Supports conversions based on string, date, timestamp, and VARIANT expressions. Supports numeric expressions and integers for conversions based on the beginning of the Unix epoch. |
| **Time zone** | [CONVERT\_TIMEZONE](functions/convert_timezone) |  |
| **Alerts** | [LAST\_SUCCESSFUL\_SCHEDULED\_TIME](functions/last_successful_scheduled_time) |  |
| [SCHEDULED\_TIME](functions/scheduled_time) |  |

## Output formats[¶](#output-formats "Link to this heading")

Several date and time functions return date, time, and timestamp values. The following session parameters
determine the format of the output returned by these functions:

* The display format for times is determined by the [TIME\_OUTPUT\_FORMAT](parameters.html#label-time-output-format)
  session parameter (default `HH24:MI:SS`).
* The display format for dates is determined by the [DATE\_OUTPUT\_FORMAT](parameters.html#label-date-output-format)
  session parameter (default `YYYY-MM-DD`).
* The display format for timestamps is determined by the timestamp data type returned by the function.
  The following session parameters set the output format for different timestamp data types:

  + [TIMESTAMP\_LTZ\_OUTPUT\_FORMAT](parameters.html#label-timestamp-ltz-output-format)
  + [TIMESTAMP\_NTZ\_OUTPUT\_FORMAT](parameters.html#label-timestamp-ntz-output-format)
  + [TIMESTAMP\_TZ\_OUTPUT\_FORMAT](parameters.html#label-timestamp-tz-output-format)
  + [TIMESTAMP\_OUTPUT\_FORMAT](parameters.html#label-timestamp-output-format)

For more information, see [Date and time input and output formats](date-time-input-output).

## Supported date and time parts[¶](#supported-date-and-time-parts "Link to this heading")

Certain functions (as well as their appropriate aliases and alternatives) accept a date or time part as an argument. The following two
tables list the parts (case-insensitive) that you can use with these functions.

| Date parts | Abbreviations / variations | DATEADD | DATEDIFF | DATE\_PART | DATE\_TRUNC | LAST\_DAY |
| --- | --- | --- | --- | --- | --- | --- |
| `year` | `y` , `yy` , `yyy` , `yyyy` , `yr` , `years` , `yrs` | ✔ | ✔ | ✔ | ✔ | ✔ |
| `month` | `mm` , `mon` , `mons` , `months` | ✔ | ✔ | ✔ | ✔ | ✔ |
| `day` | `d` , `dd` , `days`, `dayofmonth` | ✔ | ✔ | ✔ | ✔ |  |
| `dayofweek` [1] | `weekday` , `dow` , `dw` |  |  | ✔ |  |  |
| `dayofweek_iso` [2] | `dayofweekiso` , `weekday_iso` , `dow_iso` , `dw_iso` |  |  | ✔ |  |  |
| `dayofyear` | `yearday` , `doy` , `dy` |  |  | ✔ |  |  |
| `week` [1] | `w` , `wk` , `weekofyear` , `woy` , `wy` | ✔ | ✔ | ✔ | ✔ | ✔ |
| `week_iso` [2] | `weekiso` , `weekofyeariso` , `weekofyear_iso` |  |  | ✔ |  |  |
| `quarter` | `q` , `qtr` , `qtrs` , `quarters` | ✔ | ✔ | ✔ | ✔ | ✔ |
| `yearofweek` [1] |  |  |  | ✔ |  |  |
| `yearofweekiso` [2] |  |  |  | ✔ |  |  |

[1] For usage details, see the next section, which describes how Snowflake handles calendar weeks and weekdays.

[2] Not controlled by the WEEK\_START and WEEK\_OF\_YEAR\_POLICY session parameters, as described in the next section.

| Time Parts | Abbreviations / Variations | DATEADD | DATEDIFF | DATE\_PART | DATE\_TRUNC | LAST\_DAY |
| --- | --- | --- | --- | --- | --- | --- |
| `hour` | `h` , `hh` , `hr` , `hours` , `hrs` | ✔ | ✔ | ✔ | ✔ |  |
| `minute` | `m` , `mi` , `min` , `minutes` , `mins` | ✔ | ✔ | ✔ | ✔ |  |
| `second` | `s` , `sec` , `seconds` , `secs` | ✔ | ✔ | ✔ | ✔ |  |
| `millisecond` | `ms` , `msec` , `milliseconds` | ✔ | ✔ |  | ✔ |  |
| `microsecond` | `us` , `usec` , `microseconds` | ✔ | ✔ |  | ✔ |  |
| `nanosecond` | `ns` , `nsec` , `nanosec` , `nsecond` , `nanoseconds` , `nanosecs` , `nseconds` | ✔ | ✔ | ✔ | ✔ |  |
| `epoch_second` | `epoch` , `epoch_seconds` |  |  | ✔ |  |  |
| `epoch_millisecond` | `epoch_milliseconds` |  |  | ✔ |  |  |
| `epoch_microsecond` | `epoch_microseconds` |  |  | ✔ |  |  |
| `epoch_nanosecond` | `epoch_nanoseconds` |  |  | ✔ |  |  |
| `timezone_hour` | `tzh` |  |  | ✔ |  |  |
| `timezone_minute` | `tzm` |  |  | ✔ |  |  |

## Calendar weeks and weekdays[¶](#calendar-weeks-and-weekdays "Link to this heading")

The behavior of week-related functions in Snowflake is controlled by the [WEEK\_START](parameters.html#label-week-start) and [WEEK\_OF\_YEAR\_POLICY](parameters.html#label-week-of-year-policy) session parameters. An important aspect of understanding how these
parameters interact is the concept of ISO weeks.

### ISO weeks[¶](#iso-weeks "Link to this heading")

As defined in the [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) standard (for dates and time formats), ISO weeks always start on Monday and “belong” to the year that contains the Thursday of
that week. This means that a day in one year might belong to a week in a different year:

* For days in early January, the WOY (week of the year) value can be 52 or 53 (i.e. the day belongs to the last week in the previous year).
* For days in late December, the WOY value can be 1 (i.e. the day belongs to the first week in the next year).

Snowflake provides a special set of week-related date functions (and equivalent data parts) whose behavior is consistent with the ISO week semantics:
[DAYOFWEEKISO, WEEKISO, and YEAROFWEEKISO](functions/year).

These functions (and date parts) disregard the session parameters (i.e. they always follow the ISO semantics).

For details about how the other week-related date functions are handled, see the following sections:

* [First day of the week](#label-calendar-iso-weeks-first-day)
* [First and last weeks of the year](#label-calendar-iso-weeks-first-and-last)
* [Examples](#label-calendar-iso-weeks-examples)

### First day of the week[¶](#first-day-of-the-week "Link to this heading")

Most week-related functions are controlled only by the [WEEK\_START](parameters.html#label-week-start) session parameter. The function results differ depending on how this parameter is set:

| Function | Parameter set to `0` (default / legacy behavior) | Parameter set to `1` - `7` (Monday - Sunday) |
| --- | --- | --- |
| [DAYOFWEEK](functions/year) | Returns `0` (Sunday) to `6` (Saturday). | Returns `1` (defined first day of the week) to `7` (last day of the week relative to the defined first day). |
| [DATE\_TRUNC](functions/date_trunc) (with a `WEEK` part) | Truncates the input week to start on Monday. | Truncates the input week to start on the defined first day of the week. |
| [LAST\_DAY](functions/last_day) (with a `WEEK` part) | Returns the Sunday of the input week. | Returns the last day of the input week relative to the defined first day of the week. |
| [DATEDIFF](functions/datediff) (with a `WEEK` part) | Calculated using weeks starting on Monday. | Calculated using weeks starting on the defined first day of the week. |

Tip

The default value for the parameter is `0`, which preserves the legacy Snowflake behavior (ISO-like semantics).
However, we recommend changing this value to explicitly control the resulting behavior of the functions. The most common
scenario is to set the parameter to `1`.

### First and last weeks of the year[¶](#first-and-last-weeks-of-the-year "Link to this heading")

The [WEEK\_OF\_YEAR\_POLICY](parameters.html#label-week-of-year-policy) session parameter controls how the [WEEK and YEAROFWEEK](functions/year) functions behave.
The parameter can have two values:

* `0`: The affected week-related functions use semantics similar to the ISO semantics, in which a week belongs to a given year
  if at least 4 days of that week are in that year. This means that all the weeks have 7 days, but the first days of January and the
  last days of December might belong to a week in a different year. For this reason, both the [YEAROFWEEK and YEAROFWEEKISO](functions/year)
  functions can provide the year that the week belongs to.
* `1`: January 1 always starts the first week of the year, and December 31 is always in the last week of the year. This means
  that the first week and last week in the year might have fewer than 7 days.

This behavior is also influenced by the start day of the week, as controlled by the value set for the [WEEK\_START](parameters.html#label-week-start) session parameter:

* `0` or `1`: The behavior is equivalent to the ISO week semantics, with the week starting on Monday.
* `2` to `7`: The “4 days” logic is preserved, but the first day of the week is different.

Tip

The default value for both parameters is `0`, which preserves the legacy Snowflake behavior (ISO-like semantics). However,
we recommend changing these values to explicitly control the resulting behavior of the functions. The most common scenario is
to set both parameters to `1`.

### Examples[¶](#examples "Link to this heading")

These examples query the same set of date functions, but with different values set for the [WEEK\_OF\_YEAR\_POLICY](parameters.html#label-week-of-year-policy)
and [WEEK\_START](parameters.html#label-week-start) session parameters to illustrate how they influence the results of the functions.

The examples use the following data:

```
CREATE OR REPLACE TABLE week_examples (d DATE);

INSERT INTO week_examples VALUES
  ('2016-12-30'),
  ('2016-12-31'),
  ('2017-01-01'),
  ('2017-01-02'),
  ('2017-01-03'),
  ('2017-01-04'),
  ('2017-01-05'),
  ('2017-12-30'),
  ('2017-12-31');
```

Copy

#### Controlling the first day of the week[¶](#controlling-the-first-day-of-the-week "Link to this heading")

Setting WEEK\_START to `0` (legacy behavior) or `1` (Monday) does not have a significant effect, as illustrated in the following two examples:

```
ALTER SESSION SET WEEK_START = 0;

SELECT d "Date",
       DAYNAME(d) "Day",
       DAYOFWEEK(d) "DOW",
       DATE_TRUNC('week', d) "Trunc Date",
       DAYNAME("Trunc Date") "Trunc Day",
       LAST_DAY(d, 'week') "Last DOW Date",
       DAYNAME("Last DOW Date") "Last DOW Day",
       DATEDIFF('week', '2017-01-01', d) "Weeks Diff from 2017-01-01 to Date"
  FROM week_examples;
```

Copy

```
+------------+-----+-----+------------+-----------+---------------+--------------+------------------------------------+
| Date       | Day | DOW | Trunc Date | Trunc Day | Last DOW Date | Last DOW Day | Weeks Diff from 2017-01-01 to Date |
|------------+-----+-----+------------+-----------+---------------+--------------+------------------------------------|
| 2016-12-30 | Fri |   5 | 2016-12-26 | Mon       | 2017-01-01    | Sun          |                                  0 |
| 2016-12-31 | Sat |   6 | 2016-12-26 | Mon       | 2017-01-01    | Sun          |                                  0 |
| 2017-01-01 | Sun |   0 | 2016-12-26 | Mon       | 2017-01-01    | Sun          |                                  0 |
| 2017-01-02 | Mon |   1 | 2017-01-02 | Mon       | 2017-01-08    | Sun          |                                  1 |
| 2017-01-03 | Tue |   2 | 2017-01-02 | Mon       | 2017-01-08    | Sun          |                                  1 |
| 2017-01-04 | Wed |   3 | 2017-01-02 | Mon       | 2017-01-08    | Sun          |                                  1 |
| 2017-01-05 | Thu |   4 | 2017-01-02 | Mon       | 2017-01-08    | Sun          |                                  1 |
| 2017-12-30 | Sat |   6 | 2017-12-25 | Mon       | 2017-12-31    | Sun          |                                 52 |
| 2017-12-31 | Sun |   0 | 2017-12-25 | Mon       | 2017-12-31    | Sun          |                                 52 |
+------------+-----+-----+------------+-----------+---------------+--------------+------------------------------------+
```

```
ALTER SESSION SET WEEK_START = 1;

SELECT d "Date",
       DAYNAME(d) "Day",
       DAYOFWEEK(d) "DOW",
       DATE_TRUNC('week', d) "Trunc Date",
       DAYNAME("Trunc Date") "Trunc Day",
       LAST_DAY(d, 'week') "Last DOW Date",
       DAYNAME("Last DOW Date") "Last DOW Day",
       DATEDIFF('week', '2017-01-01', d) "Weeks Diff from 2017-01-01 to Date"
  FROM week_examples;
```

Copy

```
+------------+-----+-----+------------+-----------+---------------+--------------+------------------------------------+
| Date       | Day | DOW | Trunc Date | Trunc Day | Last DOW Date | Last DOW Day | Weeks Diff from 2017-01-01 to Date |
|------------+-----+-----+------------+-----------+---------------+--------------+------------------------------------|
| 2016-12-30 | Fri |   5 | 2016-12-26 | Mon       | 2017-01-01    | Sun          |                                  0 |
| 2016-12-31 | Sat |   6 | 2016-12-26 | Mon       | 2017-01-01    | Sun          |                                  0 |
| 2017-01-01 | Sun |   7 | 2016-12-26 | Mon       | 2017-01-01    | Sun          |                                  0 |
| 2017-01-02 | Mon |   1 | 2017-01-02 | Mon       | 2017-01-08    | Sun          |                                  1 |
| 2017-01-03 | Tue |   2 | 2017-01-02 | Mon       | 2017-01-08    | Sun          |                                  1 |
| 2017-01-04 | Wed |   3 | 2017-01-02 | Mon       | 2017-01-08    | Sun          |                                  1 |
| 2017-01-05 | Thu |   4 | 2017-01-02 | Mon       | 2017-01-08    | Sun          |                                  1 |
| 2017-12-30 | Sat |   6 | 2017-12-25 | Mon       | 2017-12-31    | Sun          |                                 52 |
| 2017-12-31 | Sun |   7 | 2017-12-25 | Mon       | 2017-12-31    | Sun          |                                 52 |
+------------+-----+-----+------------+-----------+---------------+--------------+------------------------------------+
```

* With WEEK\_START set to `0`, the DOW for Sunday is `0`.
* With WEEK\_START set to `1`, the DOW for Sunday is `7`.

The results differ more significantly if WEEK\_START is set to any day other than Monday. For example, setting the parameter to `3` (Wednesday) changes the results of all the week-related functions (columns 3 through 8):

```
ALTER SESSION SET WEEK_START = 3;

SELECT d "Date",
       DAYNAME(d) "Day",
       DAYOFWEEK(d) "DOW",
       DATE_TRUNC('week', d) "Trunc Date",
       DAYNAME("Trunc Date") "Trunc Day",
       LAST_DAY(d, 'week') "Last DOW Date",
       DAYNAME("Last DOW Date") "Last DOW Day",
       DATEDIFF('week', '2017-01-01', d) "Weeks Diff from 2017-01-01 to Date"
  FROM week_examples;
```

Copy

```
+------------+-----+-----+------------+-----------+---------------+--------------+------------------------------------+
| Date       | Day | DOW | Trunc Date | Trunc Day | Last DOW Date | Last DOW Day | Weeks Diff from 2017-01-01 to Date |
|------------+-----+-----+------------+-----------+---------------+--------------+------------------------------------|
| 2016-12-30 | Fri |   3 | 2016-12-28 | Wed       | 2017-01-03    | Tue          |                                  0 |
| 2016-12-31 | Sat |   4 | 2016-12-28 | Wed       | 2017-01-03    | Tue          |                                  0 |
| 2017-01-01 | Sun |   5 | 2016-12-28 | Wed       | 2017-01-03    | Tue          |                                  0 |
| 2017-01-02 | Mon |   6 | 2016-12-28 | Wed       | 2017-01-03    | Tue          |                                  0 |
| 2017-01-03 | Tue |   7 | 2016-12-28 | Wed       | 2017-01-03    | Tue          |                                  0 |
| 2017-01-04 | Wed |   1 | 2017-01-04 | Wed       | 2017-01-10    | Tue          |                                  1 |
| 2017-01-05 | Thu |   2 | 2017-01-04 | Wed       | 2017-01-10    | Tue          |                                  1 |
| 2017-12-30 | Sat |   4 | 2017-12-27 | Wed       | 2018-01-02    | Tue          |                                 52 |
| 2017-12-31 | Sun |   5 | 2017-12-27 | Wed       | 2018-01-02    | Tue          |                                 52 |
+------------+-----+-----+------------+-----------+---------------+--------------+------------------------------------+
```

#### Controlling the year and days for the first/last weeks of the year[¶](#controlling-the-year-and-days-for-the-first-last-weeks-of-the-year "Link to this heading")

The following example sets both parameters to `0` to follow ISO-like semantics (i.e. week starts on Monday and all weeks have 7 days):

```
ALTER SESSION SET WEEK_OF_YEAR_POLICY=0, WEEK_START=0;

SELECT d "Date",
       DAYNAME(d) "Day",
       WEEK(d) "WOY",
       WEEKISO(d) "WOY (ISO)",
       YEAROFWEEK(d) "YOW",
       YEAROFWEEKISO(d) "YOW (ISO)"
  FROM week_examples;
```

Copy

```
+------------+-----+-----+-----------+------+-----------+
| Date       | Day | WOY | WOY (ISO) |  YOW | YOW (ISO) |
|------------+-----+-----+-----------+------+-----------|
| 2016-12-30 | Fri |  52 |        52 | 2016 |      2016 |
| 2016-12-31 | Sat |  52 |        52 | 2016 |      2016 |
| 2017-01-01 | Sun |  52 |        52 | 2016 |      2016 |
| 2017-01-02 | Mon |   1 |         1 | 2017 |      2017 |
| 2017-01-03 | Tue |   1 |         1 | 2017 |      2017 |
| 2017-01-04 | Wed |   1 |         1 | 2017 |      2017 |
| 2017-01-05 | Thu |   1 |         1 | 2017 |      2017 |
| 2017-12-30 | Sat |  52 |        52 | 2017 |      2017 |
| 2017-12-31 | Sun |  52 |        52 | 2017 |      2017 |
+------------+-----+-----+-----------+------+-----------+
```

The next example illustrates the effect of keeping WEEK\_OF\_YEAR\_POLICY set to `0`, but changing WEEK\_START to `3` (Wednesday):

```
ALTER SESSION SET WEEK_OF_YEAR_POLICY=0, WEEK_START=3;

SELECT d "Date",
       DAYNAME(d) "Day",
       WEEK(d) "WOY",
       WEEKISO(d) "WOY (ISO)",
       YEAROFWEEK(d) "YOW",
       YEAROFWEEKISO(d) "YOW (ISO)"
  FROM week_examples;
```

Copy

```
+------------+-----+-----+-----------+------+-----------+
| Date       | Day | WOY | WOY (ISO) |  YOW | YOW (ISO) |
|------------+-----+-----+-----------+------+-----------|
| 2016-12-30 | Fri |  53 |        52 | 2016 |      2016 |
| 2016-12-31 | Sat |  53 |        52 | 2016 |      2016 |
| 2017-01-01 | Sun |  53 |        52 | 2016 |      2016 |
| 2017-01-02 | Mon |  53 |         1 | 2016 |      2017 |
| 2017-01-03 | Tue |  53 |         1 | 2016 |      2017 |
| 2017-01-04 | Wed |   1 |         1 | 2017 |      2017 |
| 2017-01-05 | Thu |   1 |         1 | 2017 |      2017 |
| 2017-12-30 | Sat |  52 |        52 | 2017 |      2017 |
| 2017-12-31 | Sun |  52 |        52 | 2017 |      2017 |
+------------+-----+-----+-----------+------+-----------+
```

* 2016 now has 53 weeks (instead of 52).
* WOY for Jan 1st, 2017 moves to week 53 (from 52).
* WOY for Jan 2nd and 3rd, 2017 moves to week 53 (from 1).
* YOW for Jan 2nd and 3rd, 2017 moves to 2016 (from 2017).
* WOY (ISO) and YOW (ISO) are not affected by the parameter change.

The last two examples set WEEK\_OF\_YEAR\_POLICY to `1` and set WEEK\_START first to `1` (Monday) and then `3` (Wednesday):

```
ALTER SESSION SET WEEK_OF_YEAR_POLICY=1, WEEK_START=1;

SELECT d "Date",
       DAYNAME(d) "Day",
       WEEK(d) "WOY",
       WEEKISO(d) "WOY (ISO)",
       YEAROFWEEK(d) "YOW",
       YEAROFWEEKISO(d) "YOW (ISO)"
  FROM week_examples;
```

Copy

```
+------------+-----+-----+-----------+------+-----------+
| Date       | Day | WOY | WOY (ISO) |  YOW | YOW (ISO) |
|------------+-----+-----+-----------+------+-----------|
| 2016-12-30 | Fri |  53 |        52 | 2016 |      2016 |
| 2016-12-31 | Sat |  53 |        52 | 2016 |      2016 |
| 2017-01-01 | Sun |   1 |        52 | 2017 |      2016 |
| 2017-01-02 | Mon |   2 |         1 | 2017 |      2017 |
| 2017-01-03 | Tue |   2 |         1 | 2017 |      2017 |
| 2017-01-04 | Wed |   2 |         1 | 2017 |      2017 |
| 2017-01-05 | Thu |   2 |         1 | 2017 |      2017 |
| 2017-12-30 | Sat |  53 |        52 | 2017 |      2017 |
| 2017-12-31 | Sun |  53 |        52 | 2017 |      2017 |
+------------+-----+-----+-----------+------+-----------+
```

```
ALTER SESSION SET week_of_year_policy=1, week_start=3;

SELECT d "Date",
       DAYNAME(d) "Day",
       WEEK(d) "WOY",
       WEEKISO(d) "WOY (ISO)",
       YEAROFWEEK(d) "YOW",
       YEAROFWEEKISO(d) "YOW (ISO)"
  FROM week_examples;
```

Copy

```
+------------+-----+-----+-----------+------+-----------+
| Date       | Day | WOY | WOY (ISO) |  YOW | YOW (ISO) |
|------------+-----+-----+-----------+------+-----------|
| 2016-12-30 | Fri |  53 |        52 | 2016 |      2016 |
| 2016-12-31 | Sat |  53 |        52 | 2016 |      2016 |
| 2017-01-01 | Sun |   1 |        52 | 2017 |      2016 |
| 2017-01-02 | Mon |   1 |         1 | 2017 |      2017 |
| 2017-01-03 | Tue |   1 |         1 | 2017 |      2017 |
| 2017-01-04 | Wed |   2 |         1 | 2017 |      2017 |
| 2017-01-05 | Thu |   2 |         1 | 2017 |      2017 |
| 2017-12-30 | Sat |  53 |        52 | 2017 |      2017 |
| 2017-12-31 | Sun |  53 |        52 | 2017 |      2017 |
+------------+-----+-----+-----------+------+-----------+
```

* With WEEK\_OF\_YEAR\_POLICY set to `1` and WEEK\_START set to `1` (Monday):

  + WOY for `2017-01-01` is `1`.
  + Week 1 consists of 1 day.
  + Week 2 starts on `Mon`.

  This usage scenario is generally the most common.
* With WEEK\_OF\_YEAR\_POLICY set to `1` and WEEK\_START set to `3` (Wednesday):

  + WOY for 2017-01-01 is still `1`.
  + Week 1 consists of 3 days.
  + Week 2 starts on `Wed`.

In both examples, WOY (ISO) and YOW (ISO) are not affected by the parameter change.

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

1. [List of functions](#list-of-functions)
2. [Output formats](#output-formats)
3. [Supported date and time parts](#supported-date-and-time-parts)
4. [Calendar weeks and weekdays](#calendar-weeks-and-weekdays)

Related content

1. [Date & time data types](/sql-reference/data-types-datetime)
2. [Conversion functions](/sql-reference/functions-conversion)