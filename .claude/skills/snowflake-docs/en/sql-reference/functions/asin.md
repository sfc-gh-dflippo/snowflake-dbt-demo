---
auto_generated: true
description: Numeric functions (Trigonometric)
last_scraped: '2026-01-14T16:54:31.474800+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/asin
title: ASIN | Snowflake Documentation
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

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)[Numeric](../functions-numeric.md)ASIN

Categories:
:   [Numeric functions](../functions-numeric) (Trigonometric)

# ASIN[¶](#asin "Link to this heading")

Computes the inverse sine (arc sine) of its argument; the result is a number in the interval `[-pi/2, pi/2]`.

## Syntax[¶](#syntax "Link to this heading")

```
ASIN( <input_expr> )
```

Copy

## Arguments[¶](#arguments "Link to this heading")

`input_expr`
:   The value or expression to operate on. Must be greater than or equal to -1.0 and
    less than or equal to +1.0. The data type must be FLOAT or DECFLOAT.

## Returns[¶](#returns "Link to this heading")

If the input expression is of type DECFLOAT, the returned type is DECFLOAT. Otherwise, the
returned type is FLOAT.

Returns the arc sine in radians (not degrees) in the range `[-pi/2, pi/2]`.

## Examples[¶](#examples "Link to this heading")

> ```
> SELECT ASIN(0), ASIN(0.5), ASIN(1);
>
> ---------+--------------+-------------+
>  ASIN(0) |  ASIN(0.5)   |   ASIN(1)   |
> ---------+--------------+-------------+
>  0       | 0.5235987756 | 1.570796327 |
> ---------+--------------+-------------+
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
3. [Returns](#returns)
4. [Examples](#examples)