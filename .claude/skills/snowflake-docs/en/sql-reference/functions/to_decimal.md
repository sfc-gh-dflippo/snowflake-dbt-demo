---
auto_generated: true
description: Conversion functions
last_scraped: '2026-01-14T16:55:30.456616+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/to_decimal
title: TO_DECIMAL , TO_NUMBER , TO_NUMERIC | Snowflake Documentation
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

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)[Conversion](../functions-conversion.md)TO\_DECIMAL

Categories:
:   [Conversion functions](../functions-conversion)

# TO\_DECIMAL , TO\_NUMBER , TO\_NUMERIC[¶](#to-decimal-to-number-to-numeric "Link to this heading")

Converts an input expression to a fixed-point number.

These functions are synonymous.

See also:
:   [TRY\_TO\_DECIMAL, TRY\_TO\_NUMBER, TRY\_TO\_NUMERIC](try_to_decimal)

## Syntax[¶](#syntax "Link to this heading")

```
TO_DECIMAL( <expr> [, '<format>' ] [, <precision> [, <scale> ] ] )

TO_NUMBER( <expr> [, '<format>' ] [, <precision> [, <scale> ] ] )

TO_NUMERIC( <expr> [, '<format>' ] [, <precision> [, <scale> ] ] )
```

Copy

## Arguments[¶](#arguments "Link to this heading")

**Required:**

`expr`
:   An expression of a numeric, character, or variant type.

**Optional:**

`format`
:   The SQL format model used to parse the input `expr` and return. For more
    information, see [SQL format models](../sql-format-models).

`precision`
:   The maximum number of decimal digits in the resulting number, from 1
    to 38. In Snowflake, precision isn’t used to determine the
    number of bytes that are needed to store the number and doesn’t have any effect
    on efficiency, so the default is the maximum (38).

`scale`
:   The number of fractional decimal digits (from 0 to `precision` - 1).
    0 indicates no fractional digits; that is, an integer number. The default scale
    is 0.

## Returns[¶](#returns "Link to this heading")

The function returns a value of type NUMBER with the following defaults:

* If the `precision` isn’t specified, then it defaults to 38.
* If the `scale` isn’t specified, then it defaults to 0.

For NULL input, returns NULL.

## Usage notes[¶](#usage-notes "Link to this heading")

* For fixed-point numbers:

  + Numbers with different scales are converted by either adding zeros to the right (if the scale needs to be increased) or by
    reducing the number of fractional digits by rounding (if the scale needs to be decreased).
  + Note that casts of fixed-point numbers to fixed-point numbers that increase scale might fail.
* For floating-point numbers:

  + Numbers are converted if they are within the representable range, given the scale.
  + The conversion between binary and decimal fractional numbers is not precise. This might result in loss of precision or
    out-of-range errors.
  + Values of infinity and NaN (not-a-number) result in conversion errors.
* Strings are converted as decimal, integer, fractional, or floating-point numbers.

  + For fractional input, the precision is deduced as the number of digits after the point.
  + For floating-point input, omitting the mantissa or exponent is allowed and is interpreted as 0. Thus, `E` is parsed as 0.
* For VARIANT input:

  + If the variant contains a fixed-point or a floating-point numeric value, an appropriate numeric conversion is performed.
  + If the variant contains a string, a string conversion is performed.
  + If the variant contains a Boolean value, the result is 0 or 1 (for false and true, correspondingly).
  + If the variant contains JSON `null` value, the output is NULL.

## Examples[¶](#examples "Link to this heading")

Create a table with a VARCHAR column, then retrieve the string values from the table and pass those values
to the TO\_NUMBER function with different `precision` and `scale` values.

```
CREATE OR REPLACE TABLE number_conv(expr VARCHAR);
INSERT INTO number_conv VALUES ('12.3456'), ('98.76546');

SELECT expr,
       TO_NUMBER(expr),
       TO_NUMBER(expr, 10, 1),
       TO_NUMBER(expr, 10, 8)
  FROM number_conv;
```

Copy

The query returns the following output:

```
+----------+-----------------+------------------------+------------------------+
| EXPR     | TO_NUMBER(EXPR) | TO_NUMBER(EXPR, 10, 1) | TO_NUMBER(EXPR, 10, 8) |
|----------+-----------------+------------------------+------------------------|
| 12.3456  |              12 |                   12.3 |            12.34560000 |
| 98.76546 |              99 |                   98.8 |            98.76546000 |
+----------+-----------------+------------------------+------------------------+
```

Try a query on the same table using the TO\_NUMBER function to return a number with the `precision` of `10`
and the scale of `9`.

```
SELECT expr, TO_NUMBER(expr, 10, 9) FROM number_conv;
```

Copy

With the `precision` argument set to `10`, the maximal number of decimal digits in the results is 10.
Because both values in the table have two digits before the decimal point and `scale` is set to `9`,
the query returns an error because the results would return 11 digits.

```
100039 (22003): Numeric value '12.3456' is out of range
```

Use different [format elements](../sql-format-models) with the TO\_DECIMAL
function in a query:

```
SELECT column1,
       TO_DECIMAL(column1, '99.9') as D0,
       TO_DECIMAL(column1, '99.9', 9, 5) as D5,
       TO_DECIMAL(column1, 'TM9', 9, 5) as TD5
  FROM VALUES ('1.0'), ('-12.3'), ('0.0'), ('- 0.1');
```

Copy

The query returns the following output:

```
+---------+-----+-----------+-----------+
| COLUMN1 |  D0 |        D5 |       TD5 |
|---------+-----+-----------+-----------|
| 1.0     |   1 |   1.00000 |   1.00000 |
| -12.3   | -12 | -12.30000 | -12.30000 |
| 0.0     |   0 |   0.00000 |   0.00000 |
| - 0.1   |   0 |  -0.10000 |  -0.10000 |
+---------+-----+-----------+-----------+
```

The output shows that the `TM9` text-minimal format element prints precisely the number of
digits in the fractional part based on the specified scale. For more information, see
[Text-minimal numeric formats](../sql-format-models.html#label-text-minimal-numeric-formats).

Convert a number that uses a comma to separate groups of digits:

```
SELECT column1,
       TO_DECIMAL(column1, '9,999.99', 6, 2) as convert_number
  FROM VALUES ('3,741.72');
```

Copy

The query returns the following output:

```
+----------+----------------+
| COLUMN1  | CONVERT_NUMBER |
|----------+----------------|
| 3,741.72 |        3741.72 |
+----------+----------------+
```

Convert a currency value that uses a comma to separate groups of digits:

```
SELECT column1,
       TO_DECIMAL(column1, '$9,999.99', 6, 2) as convert_currency
  FROM VALUES ('$3,741.72');
```

Copy

The query returns the following output:

```
+-----------+------------------+
| COLUMN1   | CONVERT_CURRENCY |
|-----------+------------------|
| $3,741.72 |          3741.72 |
+-----------+------------------+
```

Use the [X format element](../sql-format-models.html#label-fixed-position-numeric-formats) with the TO\_DECIMAL function
to convert a hexadecimal value to a decimal value:

```
SELECT TO_DECIMAL('ae5', 'XXX');
```

Copy

The query returns the following output:

```
+--------------------------+
| TO_DECIMAL('AE5', 'XXX') |
|--------------------------|
|                     2789 |
+--------------------------+
```

The number of digits in the format element must be equal to or greater than the number of digits in the
expression. For example, try to run the following query:

```
SELECT TO_DECIMAL('ae5', 'XX');
```

Copy

The query returns an error:

```
100140 (22007): Can't parse 'ae5' as number with format 'XX'
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