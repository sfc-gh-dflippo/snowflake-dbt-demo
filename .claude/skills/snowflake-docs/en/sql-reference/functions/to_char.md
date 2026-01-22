---
auto_generated: true
description: Conversion functions
last_scraped: '2026-01-14T16:55:34.665306+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/to_char
title: TO_CHAR , TO_VARCHAR | Snowflake Documentation
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

     + Any data type
     + [CAST, ::](cast.md)
     + [TRY\_CAST](try_cast.md)
     + Text, character, binary data types
     + [TO\_CHAR](to_char.md)
     + [TO\_VARCHAR](to_char.md)
     + [TO\_BINARY](to_binary.md)
     + [TRY\_TO\_BINARY](try_to_binary.md)
     + Numeric data types
     + [TO\_DECFLOAT](to_decfloat.md)
     + [TO\_DECIMAL](to_decimal.md)
     + [TO\_NUMBER](to_decimal.md)
     + [TO\_NUMERIC](to_decimal.md)
     + [TO\_DOUBLE](to_double.md)
     + [TRY\_TO\_DECFLOAT](try_to_decfloat.md)
     + [TRY\_TO\_DECIMAL](try_to_decimal.md)
     + [TRY\_TO\_NUMBER](try_to_decimal.md)
     + [TRY\_TO\_NUMERIC](try_to_decimal.md)
     + [TRY\_TO\_DOUBLE](try_to_double.md)
     + Boolean data types
     + [TO\_BOOLEAN](to_boolean.md)
     + [TRY\_TO\_BOOLEAN](try_to_boolean.md)
     + Date and time data types
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
     + Semi-structured data types
     + [TO\_ARRAY](to_array.md)
     + [TO\_OBJECT](to_object.md)
     + [TO\_VARIANT](to_variant.md)
     + Geospatial data types
     + [TO\_GEOGRAPHY](to_geography.md)
     + [TRY\_TO\_GEOGRAPHY](try_to_geography.md)
     + [ST\_GEOGRAPHYFROMWWKB](st_geographyfromwkb.md)
     + [ST\_GEOGRAPHYFROMWKT](st_geographyfromwkt.md)
     + [TO\_GEOMETRY](to_geometry.md)
     + [TRY\_TO\_GEOMETRY](try_to_geometry.md)
     + [ST\_GEOMETRYFROMWKB](st_geometryfromwkb.md)
     + [ST\_GEOMETRYFROMWKT](st_geometryfromwkt.md)
   * [Data generation](../functions-data-generation.md)
   * [Data metric](../functions-data-metric.md)
   * [Date & time](../functions-date-time.md)
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

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)[Conversion](../functions-conversion.md)TO\_CHAR

Categories:
:   [Conversion functions](../functions-conversion)

# TO\_CHAR , TO\_VARCHAR[¶](#to-char-to-varchar "Link to this heading")

Converts the input expression to a string. For NULL input, the output is NULL.

These functions are synonymous.

## Syntax[¶](#syntax "Link to this heading")

```
TO_CHAR( <expr> )
TO_CHAR( <numeric_expr> [, '<format>' ] )
TO_CHAR( <date_or_time_expr> [, '<format>' ] )
TO_CHAR( <binary_expr> [, '<format>' ] )

TO_VARCHAR( <expr> )
TO_VARCHAR( <numeric_expr> [, '<format>' ] )
TO_VARCHAR( <date_or_time_expr> [, '<format>' ] )
TO_VARCHAR( <binary_expr> [, '<format>' ] )
```

Copy

## Arguments[¶](#arguments "Link to this heading")

**Required:**

`expr`
:   An expression of any data type.

`numeric_expr`
:   A numeric expression.

`date_or_time_expr`
:   An expression of type DATE, TIME, or TIMESTAMP.

`binary_expr`
:   An expression of type BINARY or VARBINARY.

**Optional:**

`format`
:   The format of the output string:

    * For `numeric_expr`, specifies the SQL format model used to
      interpret the numeric expression. For more information, see
      [SQL format models](../sql-format-models).
    * For `date_or_time_expr`, specifies the expected format to parse
      or produce a string. For more information, see [Date and time formats in conversion functions](../functions-conversion.html#label-date-time-format-conversion).

      The default is the current value of the following session
      parameters:

      > + [DATE\_OUTPUT\_FORMAT](../parameters.html#label-date-output-format) (for DATE inputs)
      > + [TIME\_OUTPUT\_FORMAT](../parameters.html#label-time-output-format) (for TIME inputs)
      > + [TIMESTAMP\_OUTPUT\_FORMAT](../parameters.html#label-timestamp-output-format) (for TIMESTAMP inputs)
    * For `binary_expr`, specifies the format in which to produce
      the string (e.g. ‘HEX’, ‘BASE64’ or ‘UTF-8’).

      For more information, see
      [Overview of supported binary formats](../binary-input-output.html#label-overview-of-supported-binary-formats).

## Returns[¶](#returns "Link to this heading")

This function returns a value of VARCHAR data type or NULL.

## Usage notes[¶](#usage-notes "Link to this heading")

* For VARIANT, ARRAY, or OBJECT inputs, the output is the string containing
  a JSON document or JSON elementary value (unless VARIANT or OBJECT
  contains an XML tag, in which case the output is a string containing
  an XML document):

  + A string stored in VARIANT is preserved as is (i.e. it is not converted to
    a JSON string).
  + A JSON **null** value is converted to a string containing the word “null”.

## Examples[¶](#examples "Link to this heading")

The following examples convert numbers, timestamps, and dates to strings.

### Examples that convert numbers[¶](#examples-that-convert-numbers "Link to this heading")

Convert numeric values to strings in the specified [formats](../sql-format-models):

```
CREATE OR REPLACE TABLE convert_numbers_to_strings(column1 NUMBER);

INSERT INTO convert_numbers_to_strings VALUES
  (-12.391),
  (0),
  (-1),
  (0.10),
  (0.01),
  (3987),
  (1.111);

SELECT column1 AS orig_value,
       TO_CHAR(column1, '">"$99.0"<"') AS D2_1,
       TO_CHAR(column1, '">"B9,999.0"<"') AS D4_1,
       TO_CHAR(column1, '">"TME"<"') AS TME,
       TO_CHAR(column1, '">"TM9"<"') AS TM9,
       TO_CHAR(column1, '">"0XXX"<"') AS X4,
       TO_CHAR(column1, '">"S0XXX"<"') AS SX4
  FROM convert_numbers_to_strings;
```

Copy

```
+------------+----------+------------+-------------+------------+--------+---------+
| ORIG_VALUE | D2_1     | D4_1       | TME         | TM9        | X4     | SX4     |
|------------+----------+------------+-------------+------------+--------+---------|
|    -12.391 | >-$12.4< | >   -12.4< | >-1.2391E1< | >-12.391<  | >FFF4< | >-000C< |
|      0.000 | >  $0.0< | >      .0< | >0E0<       | >0.000<    | >0000< | >+0000< |
|     -1.000 | > -$1.0< | >    -1.0< | >-1E0<      | >-1.000<   | >FFFF< | >-0001< |
|      0.100 | >  $0.1< | >      .1< | >1E-1<      | >0.100<    | >0000< | >+0000< |
|      0.010 | >  $0.0< | >      .0< | >1E-2<      | >0.010<    | >0000< | >+0000< |
|   3987.000 | > $##.#< | > 3,987.0< | >3.987E3<   | >3987.000< | >0F93< | >+0F93< |
|      1.111 | >  $1.1< | >     1.1< | >1.111E0<   | >1.111<    | >0001< | >+0001< |
+------------+----------+------------+-------------+------------+--------+---------+
```

The output illustrates how the values are converted to strings based on the specified formats:

* The `>` and `<` symbols are string literals that are included in the output. They make it easier
  to see where spaces are inserted.
* The `D2_1` column shows the values with a `$` printed before the digits.

  + For the `3987` value, there are more digits in the integer part of the number than there are digit positions
    in the format, so all digits are printed as `#` to indicate overflow.
  + For the `0.10`, `0.01`, and `1.111` values, there are more digits in the fractional part of the number
    than there are digit positions in the format, so the fractional values are truncated.
* The `D4_1` column shows that zero values are represented as spaces in the integer parts of the
  numbers.

  + For the `0`, `0.10`, and `0.01` values, a space replaces the zero before the separator.
  + For the `0.10`, `0.01`, and `1.111` values, there are more digits in the fractional part of
    the number than there are digit positions in the format, so the fractional values are truncated.
* The `TME` column shows the values in scientific notation.
* The `TM9` column shows the values as integers or decimal fractions, based on the value of the number.
* The `X4` column shows the values as hexadecimal digits without the fractional parts.
* The `SX4` column shows the values as hexadecimal digits of the absolute value of the numbers and
  includes the numeric sign (`+` or `-`).

This example converts a logarithmic value to a string:

```
SELECT TO_VARCHAR(LOG(3,4));
```

Copy

```
+----------------------+
| TO_VARCHAR(LOG(3,4)) |
|----------------------|
| 1.261859507          |
+----------------------+
```

### Examples that convert timestamps and dates[¶](#examples-that-convert-timestamps-and-dates "Link to this heading")

Convert a TIMESTAMP value to a string in the specified format:

```
SELECT TO_VARCHAR('2024-04-05 01:02:03'::TIMESTAMP, 'mm/dd/yyyy, hh24:mi hours');
```

Copy

```
+---------------------------------------------------------------------------+
| TO_VARCHAR('2024-04-05 01:02:03'::TIMESTAMP, 'MM/DD/YYYY, HH24:MI HOURS') |
|---------------------------------------------------------------------------|
| 04/05/2024, 01:02 hours                                                   |
+---------------------------------------------------------------------------+
```

Convert a DATE value to a string in the default format:

```
SELECT TO_VARCHAR('03-April-2024'::DATE);
```

Copy

```
+-----------------------------------+
| TO_VARCHAR('03-APRIL-2024'::DATE) |
|-----------------------------------|
| 2024-04-03                        |
+-----------------------------------+
```

Convert a DATE value to a string in the specified format:

```
SELECT TO_VARCHAR('03-April-2024'::DATE, 'yyyy.mm.dd');
```

Copy

```
+-------------------------------------------------+
| TO_VARCHAR('03-APRIL-2024'::DATE, 'YYYY.MM.DD') |
|-------------------------------------------------|
| 2024.04.03                                      |
+-------------------------------------------------+
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