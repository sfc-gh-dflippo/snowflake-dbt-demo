---
auto_generated: true
description: This family of functions can be used to convert an expression of any
  Snowflake data type to another data type.
last_scraped: '2026-01-14T16:55:24.507471+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions-conversion
title: Conversion functions | Snowflake Documentation
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

     + Any data type
     + [CAST, ::](functions/cast.md)
     + [TRY\_CAST](functions/try_cast.md)
     + Text, character, binary data types
     + [TO\_CHAR](functions/to_char.md)
     + [TO\_VARCHAR](functions/to_char.md)
     + [TO\_BINARY](functions/to_binary.md)
     + [TRY\_TO\_BINARY](functions/try_to_binary.md)
     + Numeric data types
     + [TO\_DECFLOAT](functions/to_decfloat.md)
     + [TO\_DECIMAL](functions/to_decimal.md)
     + [TO\_NUMBER](functions/to_decimal.md)
     + [TO\_NUMERIC](functions/to_decimal.md)
     + [TO\_DOUBLE](functions/to_double.md)
     + [TRY\_TO\_DECFLOAT](functions/try_to_decfloat.md)
     + [TRY\_TO\_DECIMAL](functions/try_to_decimal.md)
     + [TRY\_TO\_NUMBER](functions/try_to_decimal.md)
     + [TRY\_TO\_NUMERIC](functions/try_to_decimal.md)
     + [TRY\_TO\_DOUBLE](functions/try_to_double.md)
     + Boolean data types
     + [TO\_BOOLEAN](functions/to_boolean.md)
     + [TRY\_TO\_BOOLEAN](functions/try_to_boolean.md)
     + Date and time data types
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
     + Semi-structured data types
     + [TO\_ARRAY](functions/to_array.md)
     + [TO\_OBJECT](functions/to_object.md)
     + [TO\_VARIANT](functions/to_variant.md)
     + Geospatial data types
     + [TO\_GEOGRAPHY](functions/to_geography.md)
     + [TRY\_TO\_GEOGRAPHY](functions/try_to_geography.md)
     + [ST\_GEOGRAPHYFROMWWKB](functions/st_geographyfromwkb.md)
     + [ST\_GEOGRAPHYFROMWKT](functions/st_geographyfromwkt.md)
     + [TO\_GEOMETRY](functions/to_geometry.md)
     + [TRY\_TO\_GEOMETRY](functions/try_to_geometry.md)
     + [ST\_GEOMETRYFROMWKB](functions/st_geometryfromwkb.md)
     + [ST\_GEOMETRYFROMWKT](functions/st_geometryfromwkt.md)
   * [Data generation](functions-data-generation.md)
   * [Data metric](functions-data-metric.md)
   * [Date & time](functions-date-time.md)
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

[Reference](../reference.md)[Function and stored procedure reference](../sql-reference-functions.md)Conversion

# Conversion functions[¶](#conversion-functions "Link to this heading")

This family of functions can be used to convert an expression of any Snowflake data type to another data type.

## List of functions[¶](#list-of-functions "Link to this heading")

| Sub-category | Function | Notes |
| --- | --- | --- |
| **Any data type** | [CAST , ::](functions/cast) |  |
| [TRY\_CAST](functions/try_cast) | Error-handling version of CAST. |
| **Text/character/binary data types** | [TO\_CHAR , TO\_VARCHAR](functions/to_char) |  |
| [TO\_BINARY](functions/to_binary) |  |
| [TRY\_TO\_BINARY](functions/try_to_binary) | Error-handling version to TO\_BINARY. |
| **Numeric data types** | [TO\_DECFLOAT](functions/to_decfloat) |  |
| [TO\_DECIMAL , TO\_NUMBER , TO\_NUMERIC](functions/to_decimal) |  |
| [TO\_DOUBLE](functions/to_double) |  |
| [TRY\_TO\_DECFLOAT](functions/try_to_decfloat) | Error-handling version of TO\_DECFLOAT. |
| [TRY\_TO\_DECIMAL, TRY\_TO\_NUMBER, TRY\_TO\_NUMERIC](functions/try_to_decimal) | Error-handling versions of TO\_DECIMAL, TO\_NUMBER, and so on. |
| [TRY\_TO\_DOUBLE](functions/try_to_double) | Error-handling version of TO\_DOUBLE. |
| **Boolean data type** | [TO\_BOOLEAN](functions/to_boolean) |  |
| [TRY\_TO\_BOOLEAN](functions/try_to_boolean) | Error-handling version of TO\_BOOLEAN. |
| **Date and time data types** | [TO\_DATE , DATE](functions/to_date) |  |
| [TO\_TIME , TIME](functions/to_time) |  |
| [TO\_TIMESTAMP / TO\_TIMESTAMP\_\*](functions/to_timestamp) |  |
| [TRY\_TO\_DATE](functions/try_to_date) | Error-handling version of TO\_DATE. |
| [TRY\_TO\_TIME](functions/try_to_time) | Error-handling version of TO\_TIME. |
| [TRY\_TO\_TIMESTAMP / TRY\_TO\_TIMESTAMP\_\*](functions/try_to_timestamp) | Error-handling versions of TO\_TIMESTAMP, and so on. |
| **Semi-structured data types** | [TO\_ARRAY](functions/to_array) |  |
| [TO\_OBJECT](functions/to_object) |  |
| [TO\_VARIANT](functions/to_variant) |  |
| **Geospatial data types** | [TO\_GEOGRAPHY](functions/to_geography) |  |
| [TRY\_TO\_GEOGRAPHY](functions/try_to_geography) | Error-handling version of TO\_GEOGRAPHY |
| [ST\_GEOGFROMGEOHASH](functions/st_geogfromgeohash) |  |
| [ST\_GEOGPOINTFROMGEOHASH](functions/st_geogpointfromgeohash) |  |
| [ST\_GEOGRAPHYFROMWKB](functions/st_geographyfromwkb) |  |
| [ST\_GEOGRAPHYFROMWKT](functions/st_geographyfromwkt) |  |
| [TO\_GEOMETRY](functions/to_geometry) |  |
| [TRY\_TO\_GEOMETRY](functions/try_to_geometry) | Error-handling version of TO\_GEOMETRY |
| [ST\_GEOMETRYFROMWKB](functions/st_geometryfromwkb) |  |
| [ST\_GEOMETRYFROMWKT](functions/st_geometryfromwkt) |  |

## Error-handling conversion functions[¶](#error-handling-conversion-functions "Link to this heading")

Conversion functions with a TRY\_ prefix are special versions of their respective conversion functions. These functions return a NULL value instead of raising an error when the conversion cannot be performed:

* [TRY\_CAST](functions/try_cast)
* [TRY\_TO\_BINARY](functions/try_to_binary)
* [TRY\_TO\_BOOLEAN](functions/try_to_boolean)
* [TRY\_TO\_DATE](functions/try_to_date)
* [TRY\_TO\_DECIMAL, TRY\_TO\_NUMBER, TRY\_TO\_NUMERIC](functions/try_to_decimal)
* [TRY\_TO\_DOUBLE](functions/try_to_double)
* [TRY\_TO\_GEOGRAPHY](functions/try_to_geography)
* [TRY\_TO\_GEOMETRY](functions/try_to_geometry)
* [TRY\_TO\_TIME](functions/try_to_time)
* [TRY\_TO\_TIMESTAMP / TRY\_TO\_TIMESTAMP\_\*](functions/try_to_timestamp)

These functions only support string expressions (i.e. VARCHAR or CHAR data type) as input.

Important

These error-handling conversion functions are optimized for situations where conversion errors are relatively infrequent:

* If there are no (or very few) errors, they should result in no visible performance impact.
* If there are a large number of conversion failures, using these functions can result in significantly slower performance. Also, when using them with the VARIANT type, some operations might result in reduced performance.

## Numeric formats in conversion functions[¶](#numeric-formats-in-conversion-functions "Link to this heading")

The functions
[TO\_DECIMAL , TO\_NUMBER , TO\_NUMERIC](functions/to_decimal), and
[TO\_DOUBLE](functions/to_double)
accept an optional parameter that specifies the format of the input string,
if the input expression evaluates to a string. For more information
about the values this parameter can have, see
[SQL format models](sql-format-models).

## Date and time formats in conversion functions[¶](#date-and-time-formats-in-conversion-functions "Link to this heading")

The following functions allow you to specify the expected date, time, or timestamp format to parse or produce a string:

* [TO\_CHAR , TO\_VARCHAR](functions/to_char)
* [TO\_DATE , DATE](functions/to_date)
* [TRY\_TO\_DATE](functions/try_to_date)
* [TO\_TIME , TIME](functions/to_time)
* [TRY\_TO\_TIME](functions/try_to_time)
* [TO\_TIMESTAMP / TO\_TIMESTAMP\_\*](functions/to_timestamp)
* [TRY\_TO\_TIMESTAMP / TRY\_TO\_TIMESTAMP\_\*](functions/try_to_timestamp)

You specify the format in an optional argument, using the following case-insensitive elements to describe the format:

| Format element | Description |
| --- | --- |
| `YYYY` | Four-digit [1] year. |
| `YY` | Two-digit [1] year, controlled by the [TWO\_DIGIT\_CENTURY\_START](parameters.html#label-two-digit-century-start) session parameter. For example, when set to `1980`, values of `79` and `80` are parsed as `2079` and `1980`, respectively. |
| `MM` | Two-digit [1] month (`01` = January, and so on). |
| `MON` | Abbreviated month name [2]. |
| `MMMM` | Full month name [2]. |
| `DD` | Two-digit [1] day of month (`01` through `31`). |
| `DY` | Abbreviated day of week. |
| `HH24` | Two digits [1] for hour (`00` through `23`). You must not specify `AM` / `PM`. |
| `HH12` | Two digits [1] for hour (`01` through `12`). You can specify `AM` / `PM`. |
| `AM` , `PM` | Ante meridiem (`AM`) / post meridiem (`PM`). Use this only with `HH12` (not with `HH24`). |
| `MI` | Two digits [1] for minute (`00` through `59`). |
| `SS` | Two digits [1] for second (`00` through `59`). |
| `FF[0-9]` | Fractional seconds with precision `0` (seconds) to `9` (nanoseconds), e.g. `FF`, `FF0`, `FF3`, `FF9`. Specifying `FF` is equivalent to `FF9` (nanoseconds). |
| `TZH:TZM` , `TZHTZM` , `TZH` | Two-digit [1] time zone hour and minute, offset from UTC. Can be prefixed by `+`/`-` for sign. |
| `UUUU` | Four-digit year in [ISO format](https://en.wikipedia.org/wiki/ISO_8601), which are negative for BCE years. |

[1] The number of digits describes the output produced when serializing values to text. When parsing text, Snowflake accepts up to the specified number of digits. For example, a day number can be one or two digits.

[2] For the MON format element, the output produced when serializing values to text is the abbreviated month name. For the MMMM format element, the output produced when serializing values to text is the full month name. When parsing text, Snowflake accepts the three-digit abbreviation or the full month name for both MON and MMMM. For example, “January” or “Jan”, “February” or “Feb”, and so on are accepted when parsing text.

Note

* When a date-only format is used, the associated time is assumed to be midnight on that day.
* Anything in the format between double quotes or other than the above elements is parsed/formatted without being interpreted.
* For more details about valid ranges, number of digits, and best practices, see
  [Additional information about using date, time, and timestamp formats](date-time-input-output.html#label-date-time-input-output-additional-information).

### Usage notes[¶](#usage-notes "Link to this heading")

Anything in the format between double quotes or other than the above elements is parsed/formatted without being interpreted.

### Examples[¶](#examples "Link to this heading")

Convert a string to a date using a specified input format of `dd/mm/yyyy`. The display format for dates in the output
is determined by the [DATE\_OUTPUT\_FORMAT](parameters.html#label-date-output-format) session parameter (default `YYYY-MM-DD`).

```
SELECT TO_DATE('3/4/2024', 'dd/mm/yyyy');
```

Copy

```
+-----------------------------------+
| TO_DATE('3/4/2024', 'DD/MM/YYYY') |
|-----------------------------------|
| 2024-04-03                        |
+-----------------------------------+
```

Convert a date to a string, and specify a [date output format](parameters.html#label-date-output-format)
of `mon dd, yyyy`.

```
SELECT TO_VARCHAR('2024-04-05'::DATE, 'mon dd, yyyy');
```

Copy

```
+------------------------------------------------+
| TO_VARCHAR('2024-04-05'::DATE, 'MON DD, YYYY') |
|------------------------------------------------|
| Apr 05, 2024                                   |
+------------------------------------------------+
```

## Binary formats in conversion functions[¶](#binary-formats-in-conversion-functions "Link to this heading")

[TO\_CHAR , TO\_VARCHAR](functions/to_char), and [TO\_BINARY](functions/to_binary) accept an optional
argument specifying the expected format to parse or produce a string.

The format can be one of the following strings (case-insensitive):

> * HEX
> * BASE64
> * UTF-8

For more information about these formats, see [Overview of supported binary formats](binary-input-output.html#label-overview-of-supported-binary-formats).

For examples of using these formats, see the Examples section of
[Binary input and output](binary-input-output).

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
2. [Error-handling conversion functions](#error-handling-conversion-functions)
3. [Numeric formats in conversion functions](#numeric-formats-in-conversion-functions)
4. [Date and time formats in conversion functions](#date-and-time-formats-in-conversion-functions)
5. [Binary formats in conversion functions](#binary-formats-in-conversion-functions)

Related content

1. [SQL data types reference](/sql-reference/../sql-reference-data-types)
2. [Date & time functions](/sql-reference/functions-date-time)
3. [Semi-structured and structured data functions](/sql-reference/functions-semistructured)
4. [Geospatial functions](/sql-reference/functions-geospatial)