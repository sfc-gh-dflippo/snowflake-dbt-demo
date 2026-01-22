---
auto_generated: true
description: Conversion functions , Date & time functions
last_scraped: '2026-01-14T16:54:34.632652+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/to_timestamp
title: TO_TIMESTAMP / TO_TIMESTAMP_* | Snowflake Documentation
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

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)[Date & time](../functions-date-time.md)TO\_TIMESTAMP\_TZ

Categories:
:   [Conversion functions](../functions-conversion) , [Date & time functions](../functions-date-time)

# TO\_TIMESTAMP / TO\_TIMESTAMP\_\*[¶](#to-timestamp-to-timestamp "Link to this heading")

Converts an input expression into the corresponding timestamp:

* TO\_TIMESTAMP\_LTZ (timestamp with local time zone)
* TO\_TIMESTAMP\_NTZ (timestamp with no time zone)
* TO\_TIMESTAMP\_TZ (timestamp with time zone)

Note

TO\_TIMESTAMP maps to one of the other timestamp functions, based on the
[TIMESTAMP\_TYPE\_MAPPING](../parameters.html#label-timestamp-type-mapping) session parameter. The parameter default is
TIMESTAMP\_NTZ, so TO\_TIMESTAMP maps to TO\_TIMESTAMP\_NTZ by default.

See also:
:   [TRY\_TO\_TIMESTAMP / TRY\_TO\_TIMESTAMP\_\*](try_to_timestamp) ,

    [AS\_TIMESTAMP\_\*](as_timestamp) , [IS\_TIMESTAMP\_\*](is_timestamp) ,

    [TO\_DATE , DATE](to_date) , [TO\_TIME , TIME](to_time)

## Syntax[¶](#syntax "Link to this heading")

```
timestampFunction ( <numeric_expr> [ , <scale> ] )

timestampFunction ( <date_expr> )

timestampFunction ( <timestamp_expr> )

timestampFunction ( <string_expr> [ , <format> ] )

timestampFunction ( '<integer>' )

timestampFunction ( <variant_expr> )
```

Copy

Where:

> ```
> timestampFunction ::=
>     TO_TIMESTAMP | TO_TIMESTAMP_LTZ | TO_TIMESTAMP_NTZ | TO_TIMESTAMP_TZ
> ```
>
> Copy

## Arguments[¶](#arguments "Link to this heading")

**Required:**

One of:

> `numeric_expr`
> :   A number of seconds (if scale = 0 or is absent) or fractions of a second (e.g. milliseconds or nanoseconds)
>     since the start of the Unix epoch (1970-01-01 00:00:00 UTC). If a non-integer decimal expression is input, the
>     scale of the result is inherited.
>
> `date_expr`
> :   A date to be converted into a timestamp.
>
> `timestamp_expr`
> :   A timestamp to be converted into another timestamp (e.g. convert TIMESTAMP\_LTZ to TIMESTAMP\_NTZ).
>
> `string_expr`
> :   A string from which to extract a timestamp, for example `'2019-01-31 01:02:03.004'`.
>
> `'integer'`
> :   An expression that evaluates to a string containing an integer, for example `'15000000'`. Depending
>     on the magnitude of the string, it can be interpreted as seconds, milliseconds, microseconds, or
>     nanoseconds. For details, see the [Usage Notes](#usage-notes).
>
> `variant_expr`
> :   An expression of type VARIANT. The VARIANT must contain one of the following:
>
>     * A string from which to extract a timestamp.
>     * A timestamp.
>     * An integer that represents the number of seconds, milliseconds, microseconds, or nanoseconds.
>     * A string containing an integer that represents the number of seconds, milliseconds, microseconds, or nanoseconds.
>
>     Although TO\_TIMESTAMP accepts a DATE value, it does not accept a DATE inside a VARIANT.

**Optional:**

`format`
:   Format specifier (only for `string_expr`). For more information, see [Date and time formats in conversion functions](../functions-conversion.html#label-date-time-format-conversion).

    The default value is the current value of the [TIMESTAMP\_INPUT\_FORMAT](../parameters.html#label-timestamp-input-format) parameter (default
    [AUTO](../date-time-input-output.html#label-date-time-input-output-supported-formats-for-auto-detection)).

`scale`
:   Scale specifier (only for `numeric_expr`). If specified, defines the scale of the numbers provided. For example:

    * For seconds, scale = `0`.
    * For milliseconds, scale = `3`.
    * For microseconds, scale = `6`.
    * For nanoseconds, scale = `9`.

    Default: `0`

## Returns[¶](#returns "Link to this heading")

The data type of the returned value is one of the TIMESTAMP data
types. By default, the data type is TIMESTAMP\_NTZ. You can change
this by setting the session parameter [TIMESTAMP\_TYPE\_MAPPING](../parameters.html#label-timestamp-type-mapping).

If the input is NULL, then the result is NULL.

## Usage notes[¶](#usage-notes "Link to this heading")

* This family of functions returns timestamp values, specifically:

  + For `string_expr`: A timestamp represented by a given string. If the string does not have a time component, midnight is used.
  + For `date_expr`: A timestamp representing midnight of a given day is used, according to the specific timestamp mapping (NTZ/LTZ/TZ) semantics.
  + For `timestamp_expr`: A timestamp with possibly different mapping than the source timestamp.
  + For `numeric_expr`: A timestamp representing the number of seconds (or fractions of a second) provided by the user. UTC time is always used to build the result.
  + For `variant_expr`:

    - If the VARIANT contains a JSON null value, the result is NULL.
    - If the VARIANT contains a timestamp value of the same kind as the result, this value is preserved as is.
    - If the VARIANT contains a timestamp value of a different kind, the conversion is done in the same way as from `timestamp_expr`.
    - If the VARIANT contains a string, conversion from a string value is performed (using automatic format).
    - If the VARIANT contains a number, conversion from `numeric_expr` is performed.

      Note

      When an INTEGER value is cast directly to TIMESTAMP\_NTZ, the integer is treated as the number of seconds
      since the beginning of the Linux epoch, and the local time zone is not taken into account. However, if the
      INTEGER value is stored inside a VARIANT value, for example as shown below, then the conversion is indirect,
      and is affected by the local time zone, even though the final result is TIMESTAMP\_NTZ:

      ```
      SELECT TO_TIMESTAMP(31000000);
      SELECT TO_TIMESTAMP(PARSE_JSON(31000000));
      SELECT PARSE_JSON(31000000)::TIMESTAMP_NTZ;
      ```

      Copy

      The timestamp returned by the first query is different from the time returned by the second and
      third queries.

      To convert independently of the local time zone, add an explicit cast to integer in the expression, as shown
      below:

      ```
      SELECT TO_TIMESTAMP(31000000);
      SELECT TO_TIMESTAMP(PARSE_JSON(31000000)::INT);
      SELECT PARSE_JSON(31000000)::INT::TIMESTAMP_NTZ;
      ```

      Copy

      The timestamp returned by all three queries is the same. This applies whether casting to TIMESTAMP\_NTZ or calling the
      function TO\_TIMESTAMP\_NTZ. It also applies when calling TO\_TIMESTAMP when the TIMESTAMP\_TYPE\_MAPPING parameter
      is set to TIMESTAMP\_NTZ.

      For an example with output, see the examples at the end of this topic.
  + If conversion is not possible, an error is returned.
* For timestamps with time zones, the setting of the [TIMEZONE](../parameters.html#label-timezone) parameter affects the return value. The returned
  timestamp is in the time zone for the session.
* The display format for timestamps in the output is determined by the timestamp output format that corresponds with the
  function ([TIMESTAMP\_OUTPUT\_FORMAT](../parameters.html#label-timestamp-output-format), [TIMESTAMP\_LTZ\_OUTPUT\_FORMAT](../parameters.html#label-timestamp-ltz-output-format), [TIMESTAMP\_NTZ\_OUTPUT\_FORMAT](../parameters.html#label-timestamp-ntz-output-format),
  or [TIMESTAMP\_TZ\_OUTPUT\_FORMAT](../parameters.html#label-timestamp-tz-output-format)).
* If the format of the input parameter is a string that contains an integer:

  + After the string is converted to an integer, the integer is treated as a number of seconds, milliseconds,
    microseconds, or nanoseconds after the start of the Unix epoch (1970-01-01 00:00:00.000000000 UTC).

    - If the integer is less than 31536000000 (the number of milliseconds in a year), then the value is treated as
      a number of seconds.
    - If the value is greater than or equal to 31536000000 and less than 31536000000000, then the value is treated
      as milliseconds.
    - If the value is greater than or equal to 31536000000000 and less than 31536000000000000, then the value is
      treated as microseconds.
    - If the value is greater than or equal to 31536000000000000, then the value is
      treated as nanoseconds.
  + If more than one row is evaluated (for example, if the input is the column name of a table that contains more than
    one row), each value is examined independently to determine if the value represents seconds, milliseconds, microseconds, or
    nanoseconds.

* When you use the TO\_TIMESTAMP\_NTZ or TRY\_TO\_TIMESTAMP\_NTZ function to convert a timestamp with time zone information, the time zone
  information is lost. If the timestamp is then converted back to a timestamp with time zone information (by using
  the TO\_TIMESTAMP\_TZ function for example), the time zone information is not recoverable.

## Examples[¶](#examples "Link to this heading")

This example shows that TO\_TIMESTAMP\_TZ creates a timestamp that contains a time
zone from the session, but the value from TO\_TIMESTAMP\_NTZ does not have a
time zone:

```
ALTER SESSION SET TIMEZONE = 'America/Los_Angeles';
```

Copy

```
SELECT TO_TIMESTAMP_TZ('2024-04-05 01:02:03');
```

Copy

```
+----------------------------------------+
| TO_TIMESTAMP_TZ('2024-04-05 01:02:03') |
|----------------------------------------|
| 2024-04-05 01:02:03.000 -0700          |
+----------------------------------------+
```

```
SELECT TO_TIMESTAMP_NTZ('2024-04-05 01:02:03');
```

Copy

```
+-----------------------------------------+
| TO_TIMESTAMP_NTZ('2024-04-05 01:02:03') |
|-----------------------------------------|
| 2024-04-05 01:02:03.000                 |
+-----------------------------------------+
```

The following examples show how different formats can influence the parsing of an ambiguous date.
Assume that the [TIMESTAMP\_TZ\_OUTPUT\_FORMAT](../parameters.html#label-timestamp-tz-output-format) is not set, so the
[TIMESTAMP\_OUTPUT\_FORMAT](../parameters.html#label-timestamp-output-format) is used and is set to the default
(`YYYY-MM-DD HH24:MI:SS.FF3 TZHTZM`).

This example shows the results when the input format is `mm/dd/yyyy hh24:mi:ss` (month/day/year):

```
SELECT TO_TIMESTAMP_TZ('04/05/2024 01:02:03', 'mm/dd/yyyy hh24:mi:ss');
```

Copy

```
+-----------------------------------------------------------------+
| TO_TIMESTAMP_TZ('04/05/2024 01:02:03', 'MM/DD/YYYY HH24:MI:SS') |
|-----------------------------------------------------------------|
| 2024-04-05 01:02:03.000 -0700                                   |
+-----------------------------------------------------------------+
```

This example shows the results when the input format is `dd/mm/yyyy hh24:mi:ss` (day/month/year):

```
SELECT TO_TIMESTAMP_TZ('04/05/2024 01:02:03', 'dd/mm/yyyy hh24:mi:ss');
```

Copy

```
+-----------------------------------------------------------------+
| TO_TIMESTAMP_TZ('04/05/2024 01:02:03', 'DD/MM/YYYY HH24:MI:SS') |
|-----------------------------------------------------------------|
| 2024-05-04 01:02:03.000 -0700                                   |
+-----------------------------------------------------------------+
```

This example shows how to use a numeric input that represents approximately 40
years from midnight January 1, 1970 (the start of the Unix epoch). The scale
is not specified, so the default scale of `0` (seconds) is used.

```
ALTER SESSION SET TIMESTAMP_OUTPUT_FORMAT = 'YYYY-MM-DD HH24:MI:SS.FF9 TZH:TZM';
```

Copy

```
SELECT TO_TIMESTAMP_NTZ(40 * 365.25 * 86400);
```

Copy

```
+---------------------------------------+
| TO_TIMESTAMP_NTZ(40 * 365.25 * 86400) |
|---------------------------------------|
| 2010-01-01 00:00:00.000               |
+---------------------------------------+
```

This example is similar to the preceding example, but provides the value as milliseconds
by specifying a scale value of `3`:

```
SELECT TO_TIMESTAMP_NTZ(40 * 365.25 * 86400 * 1000 + 456, 3);
```

Copy

```
+-------------------------------------------------------+
| TO_TIMESTAMP_NTZ(40 * 365.25 * 86400 * 1000 + 456, 3) |
|-------------------------------------------------------|
| 2010-01-01 00:00:00.456                               |
+-------------------------------------------------------+
```

This example shows how the results change when different scale values are specified for the same
numeric value:

```
SELECT TO_TIMESTAMP(1000000000, 0) AS "Scale in seconds",
       TO_TIMESTAMP(1000000000, 3) AS "Scale in milliseconds",
       TO_TIMESTAMP(1000000000, 6) AS "Scale in microseconds",
       TO_TIMESTAMP(1000000000, 9) AS "Scale in nanoseconds";
```

Copy

```
+-------------------------+-------------------------+-------------------------+-------------------------+
| Scale in seconds        | Scale in milliseconds   | Scale in microseconds   | Scale in nanoseconds    |
|-------------------------+-------------------------+-------------------------+-------------------------|
| 2001-09-09 01:46:40.000 | 1970-01-12 13:46:40.000 | 1970-01-01 00:16:40.000 | 1970-01-01 00:00:01.000 |
+-------------------------+-------------------------+-------------------------+-------------------------+
```

This example shows how the function determines the units to use (seconds, milliseconds, microseconds, or nanoseconds)
when the input is a string that contains an integer, based on the magnitude of the value.

Create and load the table with strings containing integers within different ranges:

```
CREATE OR REPLACE TABLE demo1 (
  description VARCHAR,
  value VARCHAR -- string rather than bigint
);

INSERT INTO demo1 (description, value) VALUES
  ('Seconds',      '31536000'),
  ('Milliseconds', '31536000000'),
  ('Microseconds', '31536000000000'),
  ('Nanoseconds',  '31536000000000000');
```

Copy

Pass the strings to the function:

```
SELECT description,
       value,
       TO_TIMESTAMP(value),
       TO_DATE(value)
  FROM demo1
  ORDER BY value;
```

Copy

```
+--------------+-------------------+-------------------------+----------------+
| DESCRIPTION  | VALUE             | TO_TIMESTAMP(VALUE)     | TO_DATE(VALUE) |
|--------------+-------------------+-------------------------+----------------|
| Seconds      | 31536000          | 1971-01-01 00:00:00.000 | 1971-01-01     |
| Milliseconds | 31536000000       | 1971-01-01 00:00:00.000 | 1971-01-01     |
| Microseconds | 31536000000000    | 1971-01-01 00:00:00.000 | 1971-01-01     |
| Nanoseconds  | 31536000000000000 | 1971-01-01 00:00:00.000 | 1971-01-01     |
+--------------+-------------------+-------------------------+----------------+
```

The following example casts values to TIMESTAMP\_NTZ. The example shows the difference in
behavior between using an integer and using a variant that contains an integer:

```
SELECT 0::TIMESTAMP_NTZ, PARSE_JSON(0)::TIMESTAMP_NTZ, PARSE_JSON(0)::INT::TIMESTAMP_NTZ;
```

Copy

```
+-------------------------+------------------------------+-----------------------------------+
| 0::TIMESTAMP_NTZ        | PARSE_JSON(0)::TIMESTAMP_NTZ | PARSE_JSON(0)::INT::TIMESTAMP_NTZ |
|-------------------------+------------------------------+-----------------------------------|
| 1970-01-01 00:00:00.000 | 1969-12-31 16:00:00.000      | 1970-01-01 00:00:00.000           |
+-------------------------+------------------------------+-----------------------------------+
```

The returned timestamps match for an integer and for a variant cast to an integer in the
first and third columns, but the returned timestamp is different for the variant that is not
cast to an integer in the second column. For more information, see
[Usage notes](#label-to-timestamp-usage-notes).

This same behavior applies when calling the TO\_TIMESTAMP\_NTZ function:

```
SELECT TO_TIMESTAMP_NTZ(0), TO_TIMESTAMP_NTZ(PARSE_JSON(0)), TO_TIMESTAMP_NTZ(PARSE_JSON(0)::INT);
```

Copy

```
+-------------------------+---------------------------------+--------------------------------------+
| TO_TIMESTAMP_NTZ(0)     | TO_TIMESTAMP_NTZ(PARSE_JSON(0)) | TO_TIMESTAMP_NTZ(PARSE_JSON(0)::INT) |
|-------------------------+---------------------------------+--------------------------------------|
| 1970-01-01 00:00:00.000 | 1969-12-31 16:00:00.000         | 1970-01-01 00:00:00.000              |
+-------------------------+---------------------------------+--------------------------------------+
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