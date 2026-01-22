---
auto_generated: true
description: Aggregate functions (Boolean) , Window functions , Conditional expression
  functions
last_scraped: '2026-01-14T16:56:16.091160+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/booland_agg
title: BOOLAND_AGG | Snowflake Documentation
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

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)[Aggregate](../functions-aggregation.md)BOOLAND\_AGG

Categories:
:   [Aggregate functions](../functions-aggregation) (Boolean) , [Window functions](../functions-window) , [Conditional expression functions](../expressions-conditional)

# BOOLAND\_AGG[¶](#booland-agg "Link to this heading")

Returns TRUE if all non-NULL Boolean records in a group evaluate to TRUE.

If all records in the group are NULL, or if the group is empty, the function returns NULL.

See also:
:   [BOOLAND](booland) , [BOOLOR\_AGG](boolor_agg) , [BOOLXOR\_AGG](boolxor_agg)

## Syntax[¶](#syntax "Link to this heading")

**Aggregate function**

```
BOOLAND_AGG( <expr> )
```

Copy

**Window function**

```
BOOLAND_AGG( <expr> )  OVER ( [ PARTITION BY <partition_expr> ] )
```

Copy

## Arguments[¶](#arguments "Link to this heading")

`expr`
:   The input expression must be an expression that can be evaluated to a boolean or converted to a boolean.

`partition_expr`
:   This column or expression specifies how to separate the input into partitions (sub-windows).

## Returns[¶](#returns "Link to this heading")

This function returns a value of type BOOLEAN.

## Usage notes[¶](#usage-notes "Link to this heading")

* [Numeric](../data-types-numeric) values are converted to `TRUE` if they are non-zero.
* [String and binary](../data-types-text) values aren’t supported because they can’t be converted to Boolean values.

* When this function is called as a window function, it does not support:

  + An ORDER BY clause within the OVER clause.
  + Explicit window frames.

## Examples[¶](#examples "Link to this heading")

**Aggregate function**

The following example shows that booland\_agg returns true when all of the input values are true.

> Create and load the table:
>
> ```
> create or replace table test_boolean_agg(
>     id integer,
>     c1 boolean, 
>     c2 boolean,
>     c3 boolean,
>     c4 boolean
>     );
>
> insert into test_boolean_agg (id, c1, c2, c3, c4) values 
>     (1, true, true,  true,  false),
>     (2, true, false, false, false),
>     (3, true, true,  false, false),
>     (4, true, false, false, false);
> ```
>
> Copy
>
> Display the data:
>
> ```
> select * from test_boolean_agg;
> +----+------+-------+-------+-------+
> | ID | C1   | C2    | C3    | C4    |
> |----+------+-------+-------+-------|
> |  1 | True | True  | True  | False |
> |  2 | True | False | False | False |
> |  3 | True | True  | False | False |
> |  4 | True | False | False | False |
> +----+------+-------+-------+-------+
> ```
>
> Copy
>
> Query the data:
>
> ```
> select booland_agg(c1), booland_agg(c2), booland_agg(c3), booland_agg(c4)
>     from test_boolean_agg;
> +-----------------+-----------------+-----------------+-----------------+
> | BOOLAND_AGG(C1) | BOOLAND_AGG(C2) | BOOLAND_AGG(C3) | BOOLAND_AGG(C4) |
> |-----------------+-----------------+-----------------+-----------------|
> | True            | False           | False           | False           |
> +-----------------+-----------------+-----------------+-----------------+
> ```
>
> Copy

**Window function**

This example is similar to the previous example, but it shows usage as a window function, with the input rows
split into two partitions (one for IDs greater than 0 and one for IDs less than or equal to 0). Additional data was
added to the table.

> Add rows to the table:
>
> ```
> insert into test_boolean_agg (id, c1, c2, c3, c4) values
>     (-4, false, false, false, true),
>     (-3, false, true,  true,  true),
>     (-2, false, false, true,  true),
>     (-1, false, true,  true,  true);
> ```
>
> Copy
>
> Display the data:
>
> ```
> select * 
>     from test_boolean_agg
>     order by id;
> +----+-------+-------+-------+-------+
> | ID | C1    | C2    | C3    | C4    |
> |----+-------+-------+-------+-------|
> | -4 | False | False | False | True  |
> | -3 | False | True  | True  | True  |
> | -2 | False | False | True  | True  |
> | -1 | False | True  | True  | True  |
> |  1 | True  | True  | True  | False |
> |  2 | True  | False | False | False |
> |  3 | True  | True  | False | False |
> |  4 | True  | False | False | False |
> +----+-------+-------+-------+-------+
> ```
>
> Copy
>
> Query the data:
>
> ```
> select 
>       id,
>       booland_agg(c1) OVER (PARTITION BY (id > 0)),
>       booland_agg(c2) OVER (PARTITION BY (id > 0)),
>       booland_agg(c3) OVER (PARTITION BY (id > 0)),
>       booland_agg(c4) OVER (PARTITION BY (id > 0))
>     from test_boolean_agg
>     order by id;
> +----+----------------------------------------------+----------------------------------------------+----------------------------------------------+----------------------------------------------+
> | ID | BOOLAND_AGG(C1) OVER (PARTITION BY (ID > 0)) | BOOLAND_AGG(C2) OVER (PARTITION BY (ID > 0)) | BOOLAND_AGG(C3) OVER (PARTITION BY (ID > 0)) | BOOLAND_AGG(C4) OVER (PARTITION BY (ID > 0)) |
> |----+----------------------------------------------+----------------------------------------------+----------------------------------------------+----------------------------------------------|
> | -4 | False                                        | False                                        | False                                        | True                                         |
> | -3 | False                                        | False                                        | False                                        | True                                         |
> | -2 | False                                        | False                                        | False                                        | True                                         |
> | -1 | False                                        | False                                        | False                                        | True                                         |
> |  1 | True                                         | False                                        | False                                        | False                                        |
> |  2 | True                                         | False                                        | False                                        | False                                        |
> |  3 | True                                         | False                                        | False                                        | False                                        |
> |  4 | True                                         | False                                        | False                                        | False                                        |
> +----+----------------------------------------------+----------------------------------------------+----------------------------------------------+----------------------------------------------+
> ```
>
> Copy

**Error example**

If this function is passed strings that can’t be converted to Boolean, the function returns an error:

```
select booland_agg('invalid type');

100037 (22018): Boolean value 'invalid_type' is not recognized
```

Copy

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