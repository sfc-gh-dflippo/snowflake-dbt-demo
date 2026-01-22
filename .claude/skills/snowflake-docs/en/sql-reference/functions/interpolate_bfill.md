---
auto_generated: true
description: Window functions (General)
last_scraped: '2026-01-14T16:57:58.199264+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/interpolate_bfill
title: INTERPOLATE_BFILL, INTERPOLATE_FFILL, INTERPOLATE_LINEAR | Snowflake Documentation
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
   * [Organization users and organization user groups](../functions-organization-users.md)
   * [Regular expressions](../functions-regexp.md)
   * [Semi-structured and structured data](../functions-semistructured.md)
   * [Snowpark Container Services](../functions-spcs.md)
   * [String & binary](../functions-string.md)
   * [System](../functions-system.md)
   * [Table](../functions-table.md)
   * [Vector](../functions-vector.md)
   * [Window](../functions-window.md)

     + [Syntax and usage](../functions-window-syntax.md)
     + General
     + [ANY\_VALUE](any_value.md)
     + [AVG](avg.md)
     + [CONDITIONAL\_CHANGE\_EVENT](conditional_change_event.md)
     + [CONDITIONAL\_TRUE\_EVENT](conditional_true_event.md)
     + [CORR](corr.md)
     + [COUNT](count.md)
     + [COUNT\_IF](count_if.md)
     + [COVAR\_POP](covar_pop.md)
     + [COVAR\_SAMP](covar_samp.md)
     + [INTERPOLATE\_BFILL](interpolate_bfill.md)
     + [INTERPOLATE\_FFILL](interpolate_bfill.md)
     + [INTERPOLATE\_LINEAR](interpolate_bfill.md)
     + [LISTAGG](listagg.md)
     + [MAX](max.md)
     + [MEDIAN](median.md)
     + [MIN](min.md)
     + [MODE](mode.md)
     + [PERCENTILE\_CONT](percentile_cont.md)
     + [PERCENTILE\_DISC](percentile_disc.md)
     + [RATIO\_TO\_REPORT](ratio_to_report.md)
     + [STDDEV, STDDEV\_SAMP](stddev.md)
     + [STDDEV\_POP](stddev_pop.md)
     + [SUM](sum.md)
     + [VAR\_POP](var_pop.md)
     + [VAR\_SAMP](var_samp.md)
     + [VARIANCE](variance.md)
     + [VARIANCE\_POP](variance_pop.md)
     + [VARIANCE\_SAMP](variance.md)
     + Ranking
     + [CUME\_DIST](cume_dist.md)
     + [DENSE\_RANK](dense_rank.md)
     + [FIRST\_VALUE](first_value.md)
     + [LAG](lag.md)
     + [LAST\_VALUE](last_value.md)
     + [LEAD](lead.md)
     + [NTH\_VALUE](nth_value.md)
     + [NTILE](ntile.md)
     + [PERCENT\_RANK](percent_rank.md)
     + [RANK](rank.md)
     + [ROW\_NUMBER](row_number.md)
     + Bitwise aggregation
     + [BITAND\_AGG](bitand_agg.md)
     + [BITOR\_AGG](bitor_agg.md)
     + [BITXOR\_AGG](bitxor_agg.md)
     + Boolean aggregation
     + [BOOLAND\_AGG](booland_agg.md)
     + [BOOLOR\_AGG](boolor_agg.md)
     + [BOOLXOR\_AGG](boolxor_agg.md)
     + Hash aggregation
     + [HASH\_AGG](hash_agg.md)
     + Semi-structured aggregation
     + [ARRAY\_AGG](array_agg.md)
     + [OBJECT\_AGG](object_agg.md)
     + Counting distinct values
     + [ARRAY\_UNION\_AGG](array_union_agg.md)
     + [ARRAY\_UNIQUE\_AGG](array_unique_agg.md)
     + Linear regression
     + [REGR\_AVGX](regr_avgx.md)
     + [REGR\_AVGY](regr_avgy.md)
     + [REGR\_COUNT](regr_count.md)
     + [REGR\_INTERCEPT](regr_intercept.md)
     + [REGR\_R2](regr_r2.md)
     + [REGR\_SLOPE](regr_slope.md)
     + [REGR\_SXX](regr_sxx.md)
     + [REGR\_SXY](regr_sxy.md)
     + [REGR\_SYY](regr_syy.md)
     + Statistics and probability
     + [KURTOSIS](kurtosis.md)
     + Cardinality estimation
     + [APPROX\_COUNT\_DISTINCT](approx_count_distinct.md)
     + [HLL](hll.md)
     + [HLL\_ACCUMULATE](hll_accumulate.md)
     + [HLL\_COMBINE](hll_combine.md)
     + [HLL\_ESTIMATE](hll_estimate.md)
     + [HLL\_EXPORT](hll_export.md)
     + [HLL\_IMPORT](hll_import.md)
     + Similarity estimation
     + [APPROXIMATE\_JACCARD\_INDEX](approximate_jaccard_index.md)
     + [APPROXIMATE\_SIMILARITY](approximate_similarity.md)
     + [MINHASH](minhash.md)
     + [MINHASH\_COMBINE](minhash_combine.md)
     + Frequency estimation
     + [APPROX\_TOP\_K](approx_top_k.md)
     + [APPROX\_TOP\_K\_ACCUMULATE](approx_top_k_accumulate.md)
     + [APPROX\_TOP\_K\_COMBINE](approx_top_k_combine.md)
     + [APPROX\_TOP\_K\_ESTIMATE](approx_top_k_estimate.md)
     + Percentile estimation
     + [APPROX\_PERCENTILE](approx_percentile.md)
     + [APPROX\_PERCENTILE\_ACCUMULATE](approx_percentile_accumulate.md)
     + [APPROX\_PERCENTILE\_COMBINE](approx_percentile_combine.md)
     + [APPROX\_PERCENTILE\_ESTIMATE](approx_percentile_estimate.md)
   * [Stored procedures](../../sql-reference-stored-procedures.md)
5. [Class reference](../../sql-reference-classes.md)
6. [Scripting reference](../../sql-reference-snowflake-scripting.md)
7. [General reference](../../sql-reference.md)
8. [API reference](../../api-reference.md)

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)[Window](../functions-window.md)INTERPOLATE\_BFILL

Categories:
:   [Window functions](../functions-window) (General)

# INTERPOLATE\_BFILL, INTERPOLATE\_FFILL, INTERPOLATE\_LINEAR[¶](#interpolate-bfill-interpolate-ffill-interpolate-linear "Link to this heading")

[![Snowflake logo in black (no text)](../../_images/logo-snowflake-black.png)](../../_images/logo-snowflake-black.png) [Preview Feature](../../release-notes/preview-features) — Open

Available to all accounts.

Updates rows in a time-series data set to gap-fill missing values based on surrounding values.

You can call the following interpolation window functions:

* INTERPOLATE\_BFILL: Gap-fills rows based on the next observed row.
* INTERPOLATE\_FFILL: Gap-fills rows based on the previously observed row.
* INTERPOLATE\_LINEAR: Gap-fills rows based on the linear interpolation of previous and next values. This function
  only supports numeric values.

These functions have the same [window function syntax](../functions-window-syntax). They don’t
support explicit window frames.

## Syntax[¶](#syntax "Link to this heading")

```
INTERPOLATE_BFILL( <expr> )
  OVER ( [ PARTITION BY <expr1> ] ORDER BY <expr2> [ { ASC | DESC } ] [ NULLS { FIRST | LAST } ] )
```

Copy

```
INTERPOLATE_FFILL( <expr> )
  OVER ( [ PARTITION BY <expr1> ] ORDER BY <expr2> [ { ASC | DESC } ] [ NULLS { FIRST | LAST } ] )
```

Copy

```
INTERPOLATE_LINEAR( <expr> )
  OVER ( [ PARTITION BY <expr1> ] ORDER BY <expr2> [ { ASC | DESC } ] [ NULLS { FIRST | LAST } ] )
```

Copy

## Arguments[¶](#arguments "Link to this heading")

`expr`
:   An expression that defines the column that you want to gap-fill.

    The INTERPOLATE\_LINEAR input expression must be a numeric data type.

    The INTERPOLATE\_BFILL and INTERPOLATE\_FFILL input expressions do not support [geospatial data types](../data-types-geospatial).

## Parameters[¶](#parameters "Link to this heading")

`OVER`
:   Standard window function OVER clause. See [Window function syntax and usage](../functions-window-syntax). For the interpolation functions, the
    PARTITION BY clause is optional, but the ORDER BY clause is required. You can’t specify an explicit window frame.

    The INTERPOLATE\_LINEAR function can have only one ORDER BY expression, and it must be a numeric, DATE, or TIMESTAMP expression (including all TIMESTAMP variants).

## Returns[¶](#returns "Link to this heading")

These functions return the same data type as the data type of the input expression.

## Examples[¶](#examples "Link to this heading")

The following examples show how to use the interpolation functions in simple queries.

### Example with two interpolation functions[¶](#example-with-two-interpolation-functions "Link to this heading")

The following example returns resampled `temperature` values and two different interpolated `temperature` values in the same query. (The table `march_temps_every_five_mins` was created earlier in this topic.)

```
SELECT observed,
    temperature,
    INTERPOLATE_BFILL(temperature) OVER (PARTITION BY city, county ORDER BY observed) bfill_temp,
    INTERPOLATE_FFILL(temperature) OVER (PARTITION BY city, county ORDER BY observed) ffill_temp,
    city,
    county
  FROM march_temps_every_five_mins
  ORDER BY observed;
```

Copy

```
+-------------------------+-------------+------------+------------+------------------+----------------+
| OBSERVED                | TEMPERATURE | BFILL_TEMP | FFILL_TEMP | CITY             | COUNTY         |
|-------------------------+-------------+------------+------------+------------------+----------------|
| 2025-03-15 09:45:00.000 |        NULL |         48 |       NULL | Big Bear City    | San Bernardino |
| 2025-03-15 09:49:00.000 |          48 |         48 |         48 | Big Bear City    | San Bernardino |
| 2025-03-15 09:50:00.000 |        NULL |         49 |         48 | Big Bear City    | San Bernardino |
| 2025-03-15 09:50:00.000 |          44 |         44 |         44 | South Lake Tahoe | El Dorado      |
| 2025-03-15 09:55:00.000 |          49 |         49 |         49 | Big Bear City    | San Bernardino |
| 2025-03-15 09:55:00.000 |          46 |         46 |         46 | South Lake Tahoe | El Dorado      |
| 2025-03-15 10:00:00.000 |        NULL |         51 |         49 | Big Bear City    | San Bernardino |
| 2025-03-15 10:00:00.000 |        NULL |         52 |         46 | South Lake Tahoe | El Dorado      |
| 2025-03-15 10:05:00.000 |        NULL |         51 |         49 | Big Bear City    | San Bernardino |
| 2025-03-15 10:05:00.000 |        NULL |         52 |         46 | South Lake Tahoe | El Dorado      |
| 2025-03-15 10:10:00.000 |          51 |         51 |         51 | Big Bear City    | San Bernardino |
| 2025-03-15 10:10:00.000 |          52 |         52 |         52 | South Lake Tahoe | El Dorado      |
| 2025-03-15 10:15:00.000 |        NULL |         54 |         51 | Big Bear City    | San Bernardino |
| 2025-03-15 10:15:00.000 |          54 |         54 |         54 | South Lake Tahoe | El Dorado      |
| 2025-03-15 10:18:00.000 |          54 |         54 |         54 | Big Bear City    | San Bernardino |
+-------------------------+-------------+------------+------------+------------------+----------------+
```

The `bfill_temp` column returns a meaningful value for every row, but `ffill_temp` returns NULL
for the first row. The INTERPOLATE\_FFILL function requires a previous value in order to return a non-NULL result.
The INTERPOLATE\_BFILL function only requires a next value.

### Example of an expected error for an explicit window frame[¶](#example-of-an-expected-error-for-an-explicit-window-frame "Link to this heading")

The following query returns an error because the interpolation functions do not support explicit window frames:

```
SELECT observed, temperature,
    INTERPOLATE_BFILL(temperature)
      OVER (PARTITION BY city, county ORDER BY observed ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) bfill_temp,
    city, county
  FROM march_temps_every_five_mins
  ORDER BY observed;
```

Copy

```
002303 (0A000): SQL compilation error: error line 1 at position 111
Sliding window frame unsupported for function INTERPOLATE_BFILL
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
3. [Parameters](#parameters)
4. [Returns](#returns)
5. [Examples](#examples)
6. [Example with two interpolation functions](#example-with-two-interpolation-functions)
7. [Example of an expected error for an explicit window frame](#example-of-an-expected-error-for-an-explicit-window-frame)