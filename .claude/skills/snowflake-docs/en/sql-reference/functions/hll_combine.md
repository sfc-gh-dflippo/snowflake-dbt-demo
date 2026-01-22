---
auto_generated: true
description: Aggregate functions (Cardinality Estimation) , Window function syntax
  and usage
last_scraped: '2026-01-14T16:57:57.228118+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/hll_combine
title: HLL_COMBINE | Snowflake Documentation
---

1. [Overview](../../reference.md)
2. [SQL data types reference](../../sql-reference-data-types.md)
3. [SQL command reference](../../sql-reference-commands.md)
4. [Function and stored procedure reference](../../sql-reference-functions.md)

   * [Summary of functions](../intro-summary-operators-functions.md)
   * [All functions (alphabetical)](../functions-all.md)")
   * [Aggregate](../functions-aggregation.md)

     + General
     + [ANY\_VALUE](any_value.md)
     + [AVG](avg.md)
     + [CORR](corr.md)
     + [COUNT](count.md)
     + [COUNT\_IF](count_if.md)
     + [COVAR\_POP](covar_pop.md)
     + [COVAR\_SAMP](covar_samp.md)
     + [LISTAGG](listagg.md)
     + [MAX](max.md)
     + [MAX\_BY](max_by.md)
     + [MEDIAN](median.md)
     + [MIN](min.md)
     + [MIN\_BY](min_by.md)
     + [MODE](mode.md)
     + [PERCENTILE\_CONT](percentile_cont.md)
     + [PERCENTILE\_DISC](percentile_disc.md)
     + [STDDEV, STDDEV\_SAMP](stddev.md)
     + [STDDEV\_POP](stddev_pop.md)
     + [SUM](sum.md)
     + [VAR\_POP](var_pop.md)
     + [VAR\_SAMP](var_samp.md)
     + [VARIANCE](variance.md)
     + [VARIANCE\_POP](variance_pop.md)
     + [VARIANCE\_SAMP](variance.md)
     + Bitwise
     + [BITAND\_AGG](bitand_agg.md)
     + [BITOR\_AGG](bitor_agg.md)
     + [BITXOR\_AGG](bitxor_agg.md)
     + Boolean
     + [BOOLAND\_AGG](booland_agg.md)
     + [BOOLOR\_AGG](boolor_agg.md)
     + [BOOLXOR\_AGG](boolxor_agg.md)
     + Hash
     + [HASH\_AGG](hash_agg.md)
     + Semi-structured
     + [ARRAY\_AGG](array_agg.md)
     + [OBJECT\_AGG](object_agg.md)
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
     + [SKEW](skew.md)
     + Count distinct values
     + [ARRAY\_UNION\_AGG](array_union_agg.md)
     + [ARRAY\_UNIQUE\_AGG](array_unique_agg.md)
     + [BITMAP\_BIT\_POSITION](bitmap_bit_position.md)
     + [BITMAP\_BUCKET\_NUMBER](bitmap_bucket_number.md)
     + [BITMAP\_COUNT](bitmap_count.md)
     + [BITMAP\_CONSTRUCT\_AGG](bitmap_construct_agg.md)
     + [BITMAP\_OR\_AGG](bitmap_or_agg.md)
     + Cardinality estimation
     + [APPROX\_COUNT\_DISTINCT](approx_count_distinct.md)
     + [DATASKETCHES\_HLL](datasketches_hll.md)
     + [DATASKETCHES\_HLL\_ACCUMULATE](datasketches_hll_accumulate.md)
     + [DATASKETCHES\_HLL\_COMBINE](datasketches_hll_combine.md)
     + [DATASKETCHES\_HLL\_ESTIMATE](datasketches_hll_estimate.md)
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
     + Utilities
     + [GROUPING](grouping.md)
     + [GROUPING\_ID](grouping_id.md)
     + AI Functions
     + [AI\_AGG](ai_agg.md)
     + [AI\_SUMMARIZE\_AGG](ai_summarize_agg.md)
     + Semantic views
     + [AGG](agg.md)
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
   * [Stored procedures](../../sql-reference-stored-procedures.md)
5. [Class reference](../../sql-reference-classes.md)
6. [Scripting reference](../../sql-reference-snowflake-scripting.md)
7. [General reference](../../sql-reference.md)
8. [API reference](../../api-reference.md)

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)[Aggregate](../functions-aggregation.md)HLL\_COMBINE

Categories:
:   [Aggregate functions](../functions-aggregation) (Cardinality Estimation) , [Window function syntax and usage](../functions-window-syntax)

# HLL\_COMBINE[¶](#hll-combine "Link to this heading")

Combines (merges) input states into a single output state.

This allows scenarios where [HLL\_ACCUMULATE](hll_accumulate) is run over horizontal
partitions of the same table, producing an algorithm state for each table
partition. These states can later be combined using [HLL\_COMBINE](#),
producing the same output state as a single run of [HLL\_ACCUMULATE](hll_accumulate)
over the entire table.

See also:
:   [HLL](hll) , [HLL\_ACCUMULATE](hll_accumulate) , [HLL\_ESTIMATE](hll_estimate)

## Syntax[¶](#syntax "Link to this heading")

```
HLL_COMBINE( [ DISTINCT ] <state> )
```

Copy

## Arguments[¶](#arguments "Link to this heading")

`state`
:   An expression that contains state information generated
    by a call to [HLL\_ACCUMULATE](hll_accumulate).

## Usage notes[¶](#usage-notes "Link to this heading")

* DISTINCT is supported syntactically, but has no effect.
* The output of this function is not fully deterministic. Running this
  function on the same inputs might return different results at different
  times. The differences are typically small and are consistent with the fact
  that the HLL\_\* functions are approximation functions.

## Examples[¶](#examples "Link to this heading")

This example shows how to use the three related functions
`HLL_ACCUMULATE`, `HLL_ESTIMATE`, and `HLL_COMBINE`.

> Create a simple table and data:
>
> > ```
> > -- Create a sequence to use to generate values for the table.
> > CREATE OR REPLACE SEQUENCE seq92;
> > CREATE OR REPLACE TABLE sequence_demo (c1 INTEGER DEFAULT seq92.nextval, dummy SMALLINT);
> > INSERT INTO sequence_demo (dummy) VALUES (0);
> >
> > -- Double the number of rows a few times, until there are 8 rows:
> > INSERT INTO sequence_demo (dummy) SELECT dummy FROM sequence_demo;
> > INSERT INTO sequence_demo (dummy) SELECT dummy FROM sequence_demo;
> > INSERT INTO sequence_demo (dummy) SELECT dummy FROM sequence_demo;
> > ```
> >
> > Copy
>
> Create a table that contains the “state” that represents the current
> approximate cardinality information for the table named sequence\_demo:
>
> > ```
> > CREATE OR REPLACE TABLE resultstate1 AS (
> >      SELECT hll_accumulate(c1) AS rs1
> >         FROM sequence_demo);
> > ```
> >
> > Copy
>
> Now create a second table and add data. (In a more realistic situation,
> the user could have loaded more data into the first table and divided the
> data into non-overlapping sets based on the time that the data was loaded.)
>
> > ```
> > CREATE OR REPLACE TABLE test_table2 (c1 INTEGER);
> > -- Insert data.
> > INSERT INTO test_table2 (c1) SELECT c1 + 4 FROM sequence_demo;
> > ```
> >
> > Copy
>
> Get the “state” information for just the new data.
>
> > ```
> > CREATE OR REPLACE TABLE resultstate2 AS 
> >   (SELECT hll_accumulate(c1) AS rs1 
> >      FROM test_table2);
> > ```
> >
> > Copy
>
> Combine the “state” information for the two batches of rows:
>
> > ```
> > CREATE OR REPLACE TABLE combined_resultstate (c1) AS 
> >   SELECT hll_combine(rs1) AS apc1
> >     FROM (
> >         SELECT rs1 FROM resultstate1
> >         UNION ALL
> >         SELECT rs1 FROM resultstate2
> >       )
> >       ;
> > ```
> >
> > Copy
>
> Get the approximate cardinality of the combined set of rows:
>
> > ```
> > SELECT hll_estimate(c1) FROM combined_resultstate;
> > ```
> >
> > Copy
>
> Output:
>
> > ```
> > +------------------+
> > | HLL_ESTIMATE(C1) |
> > |------------------|
> > |               12 |
> > +------------------+
> > ```
> >
> > Copy

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