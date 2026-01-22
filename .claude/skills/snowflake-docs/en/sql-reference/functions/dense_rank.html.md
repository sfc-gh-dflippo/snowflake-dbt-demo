---
auto_generated: true
description: Window function syntax and usage (Ranking)
last_scraped: '2026-01-14T16:57:19.996789+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/dense_rank.html
title: DENSE_RANK | Snowflake Documentation
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

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)[Window](../functions-window.md)DENSE\_RANK

Categories:
:   [Window function syntax and usage](../functions-window-syntax) (Ranking)

# DENSE\_RANK[¶](#dense-rank "Link to this heading")

Returns the rank of a value within a group of values, without gaps in the ranks.

The rank value starts at 1 and continues up sequentially.

If two values are the same, they have the same rank.

## Syntax[¶](#syntax "Link to this heading")

```
DENSE_RANK() OVER ( [ PARTITION BY <expr1> ]
  ORDER BY <expr2> [ { ASC | DESC } ] [ NULLS { FIRST | LAST } ] [ <window_frame> ] )
```

Copy

For detailed `window_frame` syntax, see [Window function syntax and usage](../functions-window-syntax).

## Arguments[¶](#arguments "Link to this heading")

None.

The function itself takes no arguments because it returns the rank (relative position) of the current row
within the window, which is ordered by `<expr2>`. The ordering of the window determines the rank, so there
is no need to pass an additional parameter to the DENSE\_RANK function.

## Usage notes[¶](#usage-notes "Link to this heading")

* `expr1`
  The column or expression to partition the window by.

  For example, suppose that within each state or province, you want to rank
  farmers in order by the amount of corn they produced. In this case, you
  partition by state.

  If you want only a single group (e.g. you want to rank all farmers in the U.S.
  regardless of which state they live in), then omit the PARTITION BY clause.
* `expr2`
  The column or expression to order (rank) by.

  For example, if you’re ranking farmers to see who produced the most corn
  (within their state), then you would use the `bushels_produced` column. For details,
  see [Examples](#examples) (in this topic).
* Tie values result in the same rank value, but unlike [RANK](rank), they do not result in gaps in the sequence.

## Examples[¶](#examples "Link to this heading")

Create a table and data:

> ```
> -- Create table and load data.
> create or replace table corn_production (farmer_ID INTEGER, state varchar, bushels float);
> insert into corn_production (farmer_ID, state, bushels) values
>     (1, 'Iowa', 100),
>     (2, 'Iowa', 110),
>     (3, 'Kansas', 120),
>     (4, 'Kansas', 130);
> ```
>
> Copy

Show farmers’ corn production in descending order, along with the rank of each
individual farmer’s production (highest = `1`):

> ```
> SELECT state, bushels,
>         RANK() OVER (ORDER BY bushels DESC),
>         DENSE_RANK() OVER (ORDER BY bushels DESC)
>     FROM corn_production;
> +--------+---------+-------------------------------------+-------------------------------------------+
> | STATE  | BUSHELS | RANK() OVER (ORDER BY BUSHELS DESC) | DENSE_RANK() OVER (ORDER BY BUSHELS DESC) |
> |--------+---------+-------------------------------------+-------------------------------------------|
> | Kansas |     130 |                                   1 |                                         1 |
> | Kansas |     120 |                                   2 |                                         2 |
> | Iowa   |     110 |                                   3 |                                         3 |
> | Iowa   |     100 |                                   4 |                                         4 |
> +--------+---------+-------------------------------------+-------------------------------------------+
> ```
>
> Copy

Within each state, show farmers’ corn production in descending order, along with the rank of each
individual farmer’s production (highest = `1`):

> ```
> SELECT state, bushels,
>         RANK() OVER (PARTITION BY state ORDER BY bushels DESC),
>         DENSE_RANK() OVER (PARTITION BY state ORDER BY bushels DESC)
>     FROM corn_production;
> +--------+---------+--------------------------------------------------------+--------------------------------------------------------------+
> | STATE  | BUSHELS | RANK() OVER (PARTITION BY STATE ORDER BY BUSHELS DESC) | DENSE_RANK() OVER (PARTITION BY STATE ORDER BY BUSHELS DESC) |
> |--------+---------+--------------------------------------------------------+--------------------------------------------------------------|
> | Iowa   |     110 |                                                      1 |                                                            1 |
> | Iowa   |     100 |                                                      2 |                                                            2 |
> | Kansas |     130 |                                                      1 |                                                            1 |
> | Kansas |     120 |                                                      2 |                                                            2 |
> +--------+---------+--------------------------------------------------------+--------------------------------------------------------------+
> ```
>
> Copy

The query and output below show how tie values are handled by the RANK and DENSE\_RANK functions. Note that for DENSE\_RANK,
the ranks are `1`, `2`, `3`, `3`, `4`. Unlike with the output from the RANK function, the rank `4` is not skipped
because there was a tie for rank `3`.

> ```
> SELECT state, bushels,
>         RANK() OVER (ORDER BY bushels DESC),
>         DENSE_RANK() OVER (ORDER BY bushels DESC)
>     FROM corn_production;
> +--------+---------+-------------------------------------+-------------------------------------------+
> | STATE  | BUSHELS | RANK() OVER (ORDER BY BUSHELS DESC) | DENSE_RANK() OVER (ORDER BY BUSHELS DESC) |
> |--------+---------+-------------------------------------+-------------------------------------------|
> | Kansas |     130 |                                   1 |                                         1 |
> | Kansas |     120 |                                   2 |                                         2 |
> | Iowa   |     110 |                                   3 |                                         3 |
> | Iowa   |     110 |                                   3 |                                         3 |
> | Iowa   |     100 |                                   5 |                                         4 |
> +--------+---------+-------------------------------------+-------------------------------------------+
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
3. [Usage notes](#usage-notes)
4. [Examples](#examples)