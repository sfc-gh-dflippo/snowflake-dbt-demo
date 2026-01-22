---
auto_generated: true
description: Window functions are analytic functions that you can use for various
  calculations such as running totals, moving averages, and rankings.
last_scraped: '2026-01-14T16:55:14.597064+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions-analytic.html
title: Window functions | Snowflake Documentation
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

     + [Syntax and usage](functions-window-syntax.md)
     + General
     + [ANY\_VALUE](functions/any_value.md)
     + [AVG](functions/avg.md)
     + [CONDITIONAL\_CHANGE\_EVENT](functions/conditional_change_event.md)
     + [CONDITIONAL\_TRUE\_EVENT](functions/conditional_true_event.md)
     + [CORR](functions/corr.md)
     + [COUNT](functions/count.md)
     + [COUNT\_IF](functions/count_if.md)
     + [COVAR\_POP](functions/covar_pop.md)
     + [COVAR\_SAMP](functions/covar_samp.md)
     + [INTERPOLATE\_BFILL](functions/interpolate_bfill.md)
     + [INTERPOLATE\_FFILL](functions/interpolate_bfill.md)
     + [INTERPOLATE\_LINEAR](functions/interpolate_bfill.md)
     + [LISTAGG](functions/listagg.md)
     + [MAX](functions/max.md)
     + [MEDIAN](functions/median.md)
     + [MIN](functions/min.md)
     + [MODE](functions/mode.md)
     + [PERCENTILE\_CONT](functions/percentile_cont.md)
     + [PERCENTILE\_DISC](functions/percentile_disc.md)
     + [RATIO\_TO\_REPORT](functions/ratio_to_report.md)
     + [STDDEV, STDDEV\_SAMP](functions/stddev.md)
     + [STDDEV\_POP](functions/stddev_pop.md)
     + [SUM](functions/sum.md)
     + [VAR\_POP](functions/var_pop.md)
     + [VAR\_SAMP](functions/var_samp.md)
     + [VARIANCE](functions/variance.md)
     + [VARIANCE\_POP](functions/variance_pop.md)
     + [VARIANCE\_SAMP](functions/variance.md)
     + Ranking
     + [CUME\_DIST](functions/cume_dist.md)
     + [DENSE\_RANK](functions/dense_rank.md)
     + [FIRST\_VALUE](functions/first_value.md)
     + [LAG](functions/lag.md)
     + [LAST\_VALUE](functions/last_value.md)
     + [LEAD](functions/lead.md)
     + [NTH\_VALUE](functions/nth_value.md)
     + [NTILE](functions/ntile.md)
     + [PERCENT\_RANK](functions/percent_rank.md)
     + [RANK](functions/rank.md)
     + [ROW\_NUMBER](functions/row_number.md)
     + Bitwise aggregation
     + [BITAND\_AGG](functions/bitand_agg.md)
     + [BITOR\_AGG](functions/bitor_agg.md)
     + [BITXOR\_AGG](functions/bitxor_agg.md)
     + Boolean aggregation
     + [BOOLAND\_AGG](functions/booland_agg.md)
     + [BOOLOR\_AGG](functions/boolor_agg.md)
     + [BOOLXOR\_AGG](functions/boolxor_agg.md)
     + Hash aggregation
     + [HASH\_AGG](functions/hash_agg.md)
     + Semi-structured aggregation
     + [ARRAY\_AGG](functions/array_agg.md)
     + [OBJECT\_AGG](functions/object_agg.md)
     + Counting distinct values
     + [ARRAY\_UNION\_AGG](functions/array_union_agg.md)
     + [ARRAY\_UNIQUE\_AGG](functions/array_unique_agg.md)
     + Linear regression
     + [REGR\_AVGX](functions/regr_avgx.md)
     + [REGR\_AVGY](functions/regr_avgy.md)
     + [REGR\_COUNT](functions/regr_count.md)
     + [REGR\_INTERCEPT](functions/regr_intercept.md)
     + [REGR\_R2](functions/regr_r2.md)
     + [REGR\_SLOPE](functions/regr_slope.md)
     + [REGR\_SXX](functions/regr_sxx.md)
     + [REGR\_SXY](functions/regr_sxy.md)
     + [REGR\_SYY](functions/regr_syy.md)
     + Statistics and probability
     + [KURTOSIS](functions/kurtosis.md)
     + Cardinality estimation
     + [APPROX\_COUNT\_DISTINCT](functions/approx_count_distinct.md)
     + [HLL](functions/hll.md)
     + [HLL\_ACCUMULATE](functions/hll_accumulate.md)
     + [HLL\_COMBINE](functions/hll_combine.md)
     + [HLL\_ESTIMATE](functions/hll_estimate.md)
     + [HLL\_EXPORT](functions/hll_export.md)
     + [HLL\_IMPORT](functions/hll_import.md)
     + Similarity estimation
     + [APPROXIMATE\_JACCARD\_INDEX](functions/approximate_jaccard_index.md)
     + [APPROXIMATE\_SIMILARITY](functions/approximate_similarity.md)
     + [MINHASH](functions/minhash.md)
     + [MINHASH\_COMBINE](functions/minhash_combine.md)
     + Frequency estimation
     + [APPROX\_TOP\_K](functions/approx_top_k.md)
     + [APPROX\_TOP\_K\_ACCUMULATE](functions/approx_top_k_accumulate.md)
     + [APPROX\_TOP\_K\_COMBINE](functions/approx_top_k_combine.md)
     + [APPROX\_TOP\_K\_ESTIMATE](functions/approx_top_k_estimate.md)
     + Percentile estimation
     + [APPROX\_PERCENTILE](functions/approx_percentile.md)
     + [APPROX\_PERCENTILE\_ACCUMULATE](functions/approx_percentile_accumulate.md)
     + [APPROX\_PERCENTILE\_COMBINE](functions/approx_percentile_combine.md)
     + [APPROX\_PERCENTILE\_ESTIMATE](functions/approx_percentile_estimate.md)
   * [Stored procedures](../sql-reference-stored-procedures.md)
5. [Class reference](../sql-reference-classes.md)
6. [Scripting reference](../sql-reference-snowflake-scripting.md)
7. [General reference](../sql-reference.md)
8. [API reference](../api-reference.md)

[Reference](../reference.md)[Function and stored procedure reference](../sql-reference-functions.md)Window

# Window functions[¶](#window-functions "Link to this heading")

Window functions are analytic functions that you can use for various calculations such as running totals,
moving averages, and rankings.

For general syntax rules, see [Window function syntax and usage](functions-window-syntax). For syntax specific to
individual functions, go to the links in the following table.

| Sub-category | Notes |
| --- | --- |
| **General window** |  |
| [ANY\_VALUE](functions/any_value) |  |
| [AVG](functions/avg) |  |
| [CONDITIONAL\_CHANGE\_EVENT](functions/conditional_change_event) |  |
| [CONDITIONAL\_TRUE\_EVENT](functions/conditional_true_event) |  |
| [CORR](functions/corr) |  |
| [COUNT](functions/count) |  |
| [COUNT\_IF](functions/count_if) |  |
| [COVAR\_POP](functions/covar_pop) |  |
| [COVAR\_SAMP](functions/covar_samp) |  |
| [INTERPOLATE\_BFILL, INTERPOLATE\_FFILL, INTERPOLATE\_LINEAR](functions/interpolate_bfill) |  |
| [LISTAGG](functions/listagg) | Uses WITHIN GROUP syntax. |
| [MAX](functions/max) |  |
| [MEDIAN](functions/median) |  |
| [MIN](functions/min) |  |
| [MODE](functions/mode) |  |
| [PERCENTILE\_CONT](functions/percentile_cont) | Uses WITHIN GROUP syntax. |
| [PERCENTILE\_DISC](functions/percentile_disc) | Uses WITHIN GROUP syntax. |
| [RATIO\_TO\_REPORT](functions/ratio_to_report) |  |
| [STDDEV, STDDEV\_SAMP](functions/stddev) | STDDEV and STDDEV\_SAMP are aliases. |
| [STDDEV\_POP](functions/stddev_pop) |  |
| [SUM](functions/sum) |  |
| [VAR\_POP](functions/var_pop) |  |
| [VAR\_SAMP](functions/var_samp) |  |
| [VARIANCE\_POP](functions/variance_pop) | Alias for [VAR\_POP](functions/var_pop). |
| [VARIANCE , VARIANCE\_SAMP](functions/variance) | Alias for [VAR\_SAMP](functions/var_samp). |
| **Ranking** |  |
| [CUME\_DIST](functions/cume_dist) |  |
| [DENSE\_RANK](functions/dense_rank) |  |
| [FIRST\_VALUE](functions/first_value) |  |
| [LAG](functions/lag) |  |
| [LAST\_VALUE](functions/last_value) |  |
| [LEAD](functions/lead) |  |
| [NTH\_VALUE](functions/nth_value) |  |
| [NTILE](functions/ntile) |  |
| [PERCENT\_RANK](functions/percent_rank) | Supports only RANGE BETWEEN window frames without explicit offsets. |
| [RANK](functions/rank) |  |
| [ROW\_NUMBER](functions/row_number) |  |
| **Bitwise aggregation** |  |
| [BITAND\_AGG](functions/bitand_agg) |  |
| [BITOR\_AGG](functions/bitor_agg) |  |
| [BITXOR\_AGG](functions/bitxor_agg) |  |
| **Boolean aggregation** |  |
| [BOOLAND\_AGG](functions/booland_agg) |  |
| [BOOLOR\_AGG](functions/boolor_agg) |  |
| [BOOLXOR\_AGG](functions/boolxor_agg) |  |
| **Hash** |  |
| [HASH\_AGG](functions/hash_agg) |  |
| **Semi-structured data aggregation** |  |
| [ARRAY\_AGG](functions/array_agg) |  |
| [OBJECT\_AGG](functions/object_agg) |  |
| **Counting distinct values** |  |
| [ARRAY\_UNION\_AGG](functions/array_union_agg) |  |
| [ARRAY\_UNIQUE\_AGG](functions/array_unique_agg) |  |
| **Linear regression** |  |
| [REGR\_AVGX](functions/regr_avgx) |  |
| [REGR\_AVGY](functions/regr_avgy) |  |
| [REGR\_COUNT](functions/regr_count) |  |
| [REGR\_INTERCEPT](functions/regr_intercept) |  |
| [REGR\_R2](functions/regr_r2) |  |
| [REGR\_SLOPE](functions/regr_slope) |  |
| [REGR\_SXX](functions/regr_sxx) |  |
| [REGR\_SXY](functions/regr_sxy) |  |
| [REGR\_SYY](functions/regr_syy) |  |
| **Statistics and probability** |  |
| [KURTOSIS](functions/kurtosis) |  |
| **Cardinality estimation** . (**using** [HyperLogLog](../user-guide/querying-approximate-cardinality)) |  |
| [APPROX\_COUNT\_DISTINCT](functions/approx_count_distinct) | Alias for [HLL](functions/hll). |
| [HLL](functions/hll) |  |
| [HLL\_ACCUMULATE](functions/hll_accumulate) |  |
| [HLL\_COMBINE](functions/hll_combine) |  |
| [HLL\_ESTIMATE](functions/hll_estimate) | Not an aggregate function; uses scalar input from [HLL\_ACCUMULATE](functions/hll_accumulate) or [HLL\_COMBINE](functions/hll_combine). |
| [HLL\_EXPORT](functions/hll_export) |  |
| [HLL\_IMPORT](functions/hll_import) |  |
| **Similarity estimation** . (**using** [MinHash](../user-guide/querying-approximate-similarity)) |  |
| [APPROXIMATE\_JACCARD\_INDEX](functions/approximate_jaccard_index) | Alias for [APPROXIMATE\_SIMILARITY](functions/approximate_similarity). |
| [APPROXIMATE\_SIMILARITY](functions/approximate_similarity) |  |
| [MINHASH](functions/minhash) |  |
| [MINHASH\_COMBINE](functions/minhash_combine) |  |
| **Frequency estimation** . (**using** [Space-Saving](../user-guide/querying-approximate-frequent-values)) |  |
| [APPROX\_TOP\_K](functions/approx_top_k) |  |
| [APPROX\_TOP\_K\_ACCUMULATE](functions/approx_top_k_accumulate) |  |
| [APPROX\_TOP\_K\_COMBINE](functions/approx_top_k_combine) |  |
| [APPROX\_TOP\_K\_ESTIMATE](functions/approx_top_k_estimate) | Not an aggregate function; uses scalar input from [APPROX\_TOP\_K\_ACCUMULATE](functions/approx_top_k_accumulate) or [APPROX\_TOP\_K\_COMBINE](functions/approx_top_k_combine). |
| **Percentile estimation** . (**using** [t-Digest](../user-guide/querying-approximate-percentile-values)) |  |
| [APPROX\_PERCENTILE](functions/approx_percentile) |  |
| [APPROX\_PERCENTILE\_ACCUMULATE](functions/approx_percentile_accumulate) |  |
| [APPROX\_PERCENTILE\_COMBINE](functions/approx_percentile_combine) |  |
| [APPROX\_PERCENTILE\_ESTIMATE](functions/approx_percentile_estimate) | Not an aggregate function; uses scalar input from [APPROX\_PERCENTILE\_ACCUMULATE](functions/approx_percentile_accumulate) or [APPROX\_PERCENTILE\_COMBINE](functions/approx_percentile_combine). |

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

Related content

1. [Analyzing data with window functions](/sql-reference/../user-guide/functions-window-using)
2. [Window function syntax and usage](/sql-reference/functions-window-syntax)