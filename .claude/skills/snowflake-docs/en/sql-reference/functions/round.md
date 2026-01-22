---
auto_generated: true
description: Numeric functions (Rounding and Truncation)
last_scraped: '2026-01-14T16:54:33.053347+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/round
title: ROUND | Snowflake Documentation
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

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)[Numeric](../functions-numeric.md)ROUND

Categories:
:   [Numeric functions](../functions-numeric) (Rounding and Truncation)

# ROUND[¶](#round "Link to this heading")

Returns rounded values for `input_expr`.

See also:
:   [CEIL](ceil) , [FLOOR](floor) , [TRUNCATE , TRUNC](trunc)

## Syntax[¶](#syntax "Link to this heading")

```
ROUND( <input_expr> [ , <scale_expr> [ , '<rounding_mode>' ] ] )
```

Copy

```
ROUND( EXPR => <input_expr> ,
       SCALE => <scale_expr>
       [ , ROUNDING_MODE => '<rounding_mode>'  ] )
```

Copy

## Arguments[¶](#arguments "Link to this heading")

**Required:**

`input_expr` . OR . `EXPR => input_expr`
:   The value or expression to operate on. The data type must be one of the numeric data types, such as DECFLOAT,
    FLOAT, or NUMBER.

    If you specify the `EXPR =>` named argument, you must also specify the `SCALE =>` named argument.

**Optional:**

`scale_expr` . OR . `SCALE => scale_expr`
:   The number of digits the output includes after the decimal point.

    The default `scale_expr` is zero, meaning that the function removes all digits after the decimal point.

    For information about negative numbers, see [Usage notes](#label-round-function-usage-notes).

    If you specify the `SCALE =>` named argument, you must specify `EXPR =>` as the preceding named argument.

`'rounding_mode'` . OR . `ROUNDING_MODE => 'rounding_mode'`
:   The rounding mode to use. You can specify one of the following values:

    * `HALF_AWAY_FROM_ZERO`. This mode rounds the value [half away from zero](https://en.wikipedia.org/wiki/Rounding#Rounding_half_away_from_zero).
    * `HALF_TO_EVEN`. This mode rounds the value [half to even](https://en.wikipedia.org/wiki/Rounding#Rounding_half_to_even).

    Default: `HALF_AWAY_FROM_ZERO`

    If you specify the `ROUNDING_MODE =>` named argument, you must specify both `EXPR =>` and `SCALE =>` as preceding named arguments.

    Note

    If you specify either value for the `rounding_mode` argument, the data type of `input_expr` must be
    [one of the data types for a fixed-point number](../data-types-numeric.html#label-data-types-for-fixed-point-numbers).

    [Data types for floating point numbers](../data-types-numeric.html#label-data-types-for-floating-point-numbers) (for example, FLOAT) aren’t supported
    with this argument.

## Returns[¶](#returns "Link to this heading")

The return type is based on the input type:

* If the input expression is a FLOAT, the returned type is a FLOAT.
* If the input expression is DECFLOAT, the returned type is DECFLOAT.
* If the input expression is a NUMBER, the returned type is a NUMBER.

  + If the input scale is constant:

    - If the input scale is positive, the returned type has a scale equal to the input scale and has a precision large enough to
      encompass any possible result.
    - If the input scale is negative, the returned type has a scale of 0.
  + If the input scale isn’t constant, the returned type’s scale is the same as the input expression’s.

If the scale is zero, then the value is effectively an INTEGER.

For example:

* The data type returned by `ROUND(3.14::FLOAT, 1)` is FLOAT.
* The NUMBER returned by `ROUND(3.14, 1)` has scale 1 and precision at least 3.
* The NUMBER returned by `ROUND(-9.99, 0)` has scale 0 and precision at least 2.
* The NUMBER returned by `ROUND(33.33, -1)` has scale 0 and precision at least 3.

If either the `input_expr` or the `scale_expr` is NULL, the function returns NULL.

## Usage notes[¶](#usage-notes "Link to this heading")

* You must either specify all arguments by name or by position. You can’t specify some of the arguments by name and other
  arguments by position.

  When specifying an argument by name, you can’t use double quotes around the argument name.
* If `scale_expr` is negative, it specifies the number of places before the decimal point to
  which to adjust the number. For example, if the scale is -2, the result is a multiple of 100.
* If `scale_expr` is larger than the input expression scale, the function doesn’t have any effect.
* By default, half-points are rounded away from zero for decimals. For example, -0.5 is rounded to -1.0.

  To change the rounding mode to round the value [half to even](https://en.wikipedia.org/wiki/Rounding#Rounding_half_to_even) (for example, to round -0.5 to 0), specify
  `'HALF_TO_EVEN'` for the `rounding_mode` argument.

  Note

  If you specify the `rounding_mode` argument, the data type of the `input_expr` argument must be
  [one of the data types for a fixed-point number](../data-types-numeric.html#label-data-types-for-fixed-point-numbers).
* Floating point numbers are approximate values. A floating point number might not round as expected.
* If rounding brings the number outside of the range of values of the data type, the function returns an error.

## Examples[¶](#examples "Link to this heading")

This following example shows a simple use of ROUND, with the default number of decimal places (0):

```
SELECT ROUND(135.135), ROUND(-975.975);
```

Copy

```
+----------------+-----------------+
| ROUND(135.135) | ROUND(-975.975) |
|----------------+-----------------|
|            135 |            -976 |
+----------------+-----------------+
```

The next example queries the data in the following table:

```
CREATE TABLE test_ceiling (n FLOAT, scale INTEGER);

INSERT INTO test_ceiling (n, scale) VALUES
  (-975.975, -1),
  (-975.975,  0),
  (-975.975,  2),
  ( 135.135, -2),
  ( 135.135,  0),
  ( 135.135,  1),
  ( 135.135,  3),
  ( 135.135, 50),
  ( 135.135, NULL);
```

Copy

Query the table and use a range of values for the `scale_expr` argument:

```
SELECT n, scale, ROUND(n, scale)
  FROM test_ceiling
  ORDER BY n, scale;
```

Copy

```
+----------+-------+-----------------+
|        N | SCALE | ROUND(N, SCALE) |
|----------+-------+-----------------|
| -975.975 |    -1 |        -980     |
| -975.975 |     0 |        -976     |
| -975.975 |     2 |        -975.98  |
|  135.135 |    -2 |         100     |
|  135.135 |     0 |         135     |
|  135.135 |     1 |         135.1   |
|  135.135 |     3 |         135.135 |
|  135.135 |    50 |         135.135 |
|  135.135 |  NULL |            NULL |
+----------+-------+-----------------+
```

The next two examples show the difference between using the default rounding mode (`'HALF_AWAY_FROM_ZERO'`) and the rounding
mode `'HALF_TO_EVEN'`. Both examples call the ROUND function twice, first with the default rounding behavior, then with `'HALF_TO_EVEN'`.

The first example uses a positive input value of 2.5:

```
SELECT ROUND(2.5, 0), ROUND(2.5, 0, 'HALF_TO_EVEN');
```

Copy

```
+---------------+-------------------------------+
| ROUND(2.5, 0) | ROUND(2.5, 0, 'HALF_TO_EVEN') |
|---------------+-------------------------------|
|             3 |                             2 |
+---------------+-------------------------------+
```

The second example uses a negative input value of -2.5:

```
SELECT ROUND(-2.5, 0), ROUND(-2.5, 0, 'HALF_TO_EVEN');
```

Copy

```
+----------------+--------------------------------+
| ROUND(-2.5, 0) | ROUND(-2.5, 0, 'HALF_TO_EVEN') |
|----------------+--------------------------------|
|             -3 |                             -2 |
+----------------+--------------------------------+
```

The next two examples demonstrate how to specify the arguments to the function by name, rather than by position:

```
SELECT ROUND(
  EXPR => -2.5,
  SCALE => 0) AS named_arguments;
```

Copy

```
+-----------------+
| NAMED_ARGUMENTS |
|-----------------|
|              -3 |
+-----------------+
```

```
SELECT ROUND(
  EXPR => -2.5,
  SCALE => 0,
  ROUNDING_MODE => 'HALF_TO_EVEN') AS named_with_rounding_mode;
```

Copy

```
+--------------------------+
| NAMED_WITH_ROUNDING_MODE |
|--------------------------|
|                       -2 |
+--------------------------+
```

The next example shows that FLOAT values aren’t always stored exactly. As you can see below, in some cases .005 is
rounded to .01, while in other cases it is rounded to 0. The difference isn’t in the rounding; the difference is
actually in the underlying representation of the floating point number, because 1.005 is stored as a number very slightly
smaller than 1.005 (approximately 1.004999). The DECIMAL value, however is stored as an exact number, and is rounded
to .01 as expected in all cases.

Create and load a table:

```
CREATE OR REPLACE TEMP TABLE rnd1(f float, d DECIMAL(10, 3));

INSERT INTO rnd1 (f, d) VALUES
  ( -10.005,  -10.005),
  (  -1.005,   -1.005),
  (   1.005,    1.005),
  (  10.005,   10.005);
```

Copy

Show examples of the difference between rounded FLOAT values and rounded DECIMAL values:

```
SELECT f,
       ROUND(f, 2),
       d,
       ROUND(d, 2)
  FROM rnd1
  ORDER BY 1;
```

Copy

```
+---------+-------------+---------+-------------+
|       F | ROUND(F, 2) |       D | ROUND(D, 2) |
|---------+-------------+---------+-------------|
| -10.005 |      -10.01 | -10.005 |      -10.01 |
|  -1.005 |       -1    |  -1.005 |       -1.01 |
|   1.005 |        1    |   1.005 |        1.01 |
|  10.005 |       10.01 |  10.005 |       10.01 |
+---------+-------------+---------+-------------+
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