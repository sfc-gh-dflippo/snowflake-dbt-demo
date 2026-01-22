---
auto_generated: true
description: Numeric functions (Rounding and Truncation)
last_scraped: '2026-01-14T16:56:31.113445+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/trunc.html
title: TRUNCATE , TRUNC | Snowflake Documentation
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
   * [Differential privacy](../functions-differential-privacy.md)
   * [Encryption](../functions-encryption.md)
   * [File](../functions-file.md)
   * [Geospatial](../functions-geospatial.md)
   * [Hash](../functions-hash-scalar.md)
   * [Metadata](../functions-metadata.md)
   * [ML Model Monitors](../functions-model-monitors.md)
   * [Notification](../functions-notification.md)
   * [Numeric](../functions-numeric.md)

     + Arithmetic
     + [DIV0](div0.md)
     + [DIV0NULL](div0null.md)
     + Rounding and truncation
     + [ABS](abs.md)
     + [CEIL](ceil.md)
     + [FLOOR](floor.md)
     + [MOD](mod.md)
     + [ROUND](round.md)
     + [SIGN](sign.md)
     + [TRUNCATE, TRUNC](trunc.md)
     + Exponent and root
     + [CBRT](cbrt.md)
     + [EXP](exp.md)
     + [FACTORIAL](factorial.md)
     + [POW](pow.md)
     + [POWER](pow.md)
     + [SQRT](sqrt.md)
     + [SQUARE](square.md)
     + Logarithmic
     + [LN](ln.md)
     + [LOG](log.md)
     + Trigonometric
     + [ACOS](acos.md)
     + [ACOSH](acosh.md)
     + [ASIN](asin.md)
     + [ASINH](asinh.md)
     + [ATAN](atan.md)
     + [ATAN2](atan2.md)
     + [ATANH](atanh.md)
     + [COS](cos.md)
     + [COSH](cosh.md)
     + [COT](cot.md)
     + [DEGREES](degrees.md)
     + [PI](pi.md)
     + [RADIANS](radians.md)
     + [SIN](sin.md)
     + [SINH](sinh.md)
     + [TAN](tan.md)
     + [TANH](tanh.md)
     + Other
     + [WIDTH\_BUCKET](width_bucket.md)
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

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)[Numeric](../functions-numeric.md)TRUNCATE, TRUNC

Categories:
:   [Numeric functions](../functions-numeric) (Rounding and Truncation)

# TRUNCATE , TRUNC[¶](#truncate-trunc "Link to this heading")

Rounds the input expression down to the nearest (or equal) value closer to zero.
Depending on the value you specify as the scale parameter, the transformation can remove:

* All the digits after the decimal point, producing an integer value. This is the default
  and most common use of TRUNC for numbers.
* Some of the significant digits after the decimal point, producing a less precise value.
* All the significant digits after the decimal point and some significant digits
  to the left of the decimal point, producing a value that is a multiple of 10, 100, or other power of 10.

The TRUNCATE and TRUNC functions are synonymous.

Note

TRUNC is overloaded. It can also be used with date/time values to [truncate dates, times, and timestamps](trunc2)
to a specified part. The numeric TRUNC has one required and one optional parameter. The date/time TRUNC has two required parameters.

See also:
:   [CEIL](ceil) , [FLOOR](floor) , [ROUND](round)

## Syntax[¶](#syntax "Link to this heading")

```
TRUNCATE( <input_expr> [ , <scale_expr> ] )

TRUNC( <input_expr> [ , <scale_expr> ] )
```

Copy

## Arguments[¶](#arguments "Link to this heading")

`input_expr`
:   The value or expression to operate on. The data type must be one of the numeric data types, such as DECFLOAT,
    FLOAT, or NUMBER.

`scale_expr`
:   The number of digits to include after the decimal point.

    The default `scale_expr` is zero, meaning that the function removes all digits after the decimal point.

    For information about negative scales, see the [Usage notes](#label-trunc-usage-notes) below.

## Returns[¶](#returns "Link to this heading")

* If the input is a NUMBER value, the data type of the returned value is NUMBER(precision, scale).

  If the input scale was greater than or equal to zero, then the output scale generally matches the input scale.

  If the input scale was negative, then the output scale is 0.

  For example:

  + The data type returned by `TRUNCATE(3.14, 1)` is `NUMBER(4, 1)`.
  + The data type returned by `TRUNCATE(3.14, 0)` is `NUMBER(4, 0)`.
  + The data type returned by `TRUNCATE(33.33, -1)` is `NUMBER(5, 0)`.

  If the scale is zero, then the value is effectively an integer.
* If the input is a FLOAT value, the data type of the returned value is FLOAT.
* If the input is a DECFLOAT value, the data type of the returned value is DECFLOAT.

## Usage notes[¶](#usage-notes "Link to this heading")

* If `scale_expr` is negative, then it specifies the number of places before the decimal point to
  which to adjust the number. For example, if the scale is -2, then the result is a multiple of 100.
* If `scale_expr` is larger than the input expression scale, the function does not have any effect.
* If either the `input_expr` or the `scale_expr` is NULL, then the result is NULL.
* Truncation is performed towards 0, not towards the smaller number. For example, `TRUNCATE(-9.6)` results in `-9`, not `-10`.

## Examples[¶](#examples "Link to this heading")

The following examples demonstrate the TRUNC function for numeric values.
For examples of truncating dates, times, and timestamps, see [the date/time form of TRUNC](trunc2).

The examples use data from this sample table. The table contains two different decimal numbers,
-975.975 and 135.135, along with different values to use for the scale parameter with the TRUNC function.

```
CREATE TABLE numeric_trunc_demo (n FLOAT, scale INTEGER);
INSERT INTO numeric_trunc_demo (n, scale) VALUES
   (-975.975, -1), (-975.975,  0), (-975.975,  2),
   ( 135.135, -2), ( 135.135,  0), ( 135.135,  1),
   ( 135.135,  3), ( 135.135, 50), ( 135.135, NULL);
```

Copy

When you don’t specify a scale parameter, the default behavior for TRUNC
with a numeric parameter is to return the integer value that’s equal to
the parameter or closer to zero. Specifying a scale parameter of 0
does the same thing.

```
SELECT DISTINCT n, TRUNCATE(n)
  FROM numeric_trunc_demo ORDER BY n;
```

Copy

```
+----------+-------------+
|        N | TRUNCATE(N) |
|----------+-------------|
| -975.975 |        -975 |
|  135.135 |         135 |
+----------+-------------+
```

The following example shows the results of calling the TRUNC function with
zero, positive, or negative scale parameters applied to a positive and a negative
number.

* Specifying a zero scale parameter removes all the digits after the decimal point, producing an integer value.
* Specifying a positive scale parameter leaves the specified number of significant digits after the decimal point.
* Specifying a negative scale parameter turns that many digits into zeroes to the left of the decimal point.
* Specifying a scale that is greater than +38 or less than -38 is the same as specifying +38 or -38.

```
SELECT n, scale, TRUNC(n, scale)
  FROM numeric_trunc_demo ORDER BY n, scale;
```

Copy

```
+----------+-------+-----------------+
|        N | SCALE | TRUNC(N, SCALE) |
|----------+-------+-----------------|
| -975.975 |    -1 |        -970     |
| -975.975 |     0 |        -975     |
| -975.975 |     2 |        -975.97  |
|  135.135 |    -2 |         100     |
|  135.135 |     0 |         135     |
|  135.135 |     1 |         135.1   |
|  135.135 |     3 |         135.135 |
|  135.135 |    50 |         135.135 |
|  135.135 |  NULL |            NULL |
+----------+-------+-----------------+
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