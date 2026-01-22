---
auto_generated: true
description: Aggregate functions (General) , Window function syntax and usage (General)
last_scraped: '2026-01-14T16:57:26.039895+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/sum.html
title: SUM | Snowflake Documentation
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

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)[Aggregate](../functions-aggregation.md)SUM

Categories:
:   [Aggregate functions](../functions-aggregation) (General) , [Window function syntax and usage](../functions-window-syntax) (General)

# SUM[¶](#sum "Link to this heading")

Returns the sum of non-NULL records for `expr`. You can use the DISTINCT keyword to compute the sum of unique
non-null values. If all records inside a group are NULL, the function returns NULL.

See also:
:   [COUNT](count) , [MAX](max) , [MIN](min)

## Syntax[¶](#syntax "Link to this heading")

**Aggregate function**

```
SUM( [ DISTINCT ] <expr1> )
```

Copy

**Window function**

```
SUM( [ DISTINCT ] <expr1> ) OVER (
                                 [ PARTITION BY <expr2> ]
                                 [ ORDER BY <expr3> [ { ASC | DESC } ] [ NULLS { FIRST | LAST } ] [ <window_frame> ] ]
                                 )
```

Copy

For detailed `window_frame` syntax, see [Window function syntax and usage](../functions-window-syntax).

## Arguments[¶](#arguments "Link to this heading")

`expr1`
:   This is an expression that evaluates to a numeric data type (INTEGER, FLOAT, DECIMAL, etc.).

`expr2`
:   This is the optional expression to partition by.

`expr3`
:   This is the optional expression to order by within each partition. (This does not control the order of the
    entire query output.)

## Usage notes[¶](#usage-notes "Link to this heading")

* Numeric values are summed into an equivalent or larger data type.
* When passed a VARCHAR expression, this function implicitly casts the input to floating point values. If the cast
  cannot be performed, an error is returned.

* When this function is called as a window function with an OVER clause that contains an ORDER BY clause:

  + A window frame is required. If no window frame is specified explicitly, the following implied window frame is used:

    `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`

    For more information about window frames, including syntax, usage notes, and examples, see [Window function syntax and usage](../functions-window-syntax).
  + Using the keyword DISTINCT inside the window function is prohibited and results in a compile-time error.

## Examples[¶](#examples "Link to this heading")

```
CREATE OR REPLACE TABLE sum_example(k INT, d DECIMAL(10,5),
                                    s1 VARCHAR(10), s2 VARCHAR(10));

INSERT INTO sum_example VALUES
  (1, 1.1, '1.1','one'),
  (1, 10, '10','ten'),
  (2, 2.2, '2.2','two'),
  (2, null, null,'null'),
  (3, null, null, 'null'),
  (null, 9, '9.9','nine');

SELECT * FROM sum_example;
```

Copy

```
+------+----------+------+------+
|    K |        D | S1   | S2   |
|------+----------+------+------|
|    1 |  1.10000 | 1.1  | one  |
|    1 | 10.00000 | 10.0 | ten  |
|    2 |  2.20000 | 2.2  | two  |
|    2 |     NULL | NULL | null |
|    3 |     NULL | NULL | null |
| NULL |  9.00000 | 9.9  | nine |
+------+----------+------+------+
```

```
SELECT SUM(d), SUM(s1) FROM sum_example;
```

Copy

```
+----------+---------+
|   SUM(D) | SUM(S1) |
|----------+---------|
| 22.30000 |    23.2 |
+----------+---------+
```

```
SELECT k, SUM(d), SUM(s1) FROM sum_example GROUP BY k;
```

Copy

```
+------+----------+---------+
|    K |   SUM(D) | SUM(S1) |
|------+----------+---------|
|    1 | 11.10000 |    11.1 |
|    2 |  2.20000 |     2.2 |
|    3 |     NULL |    NULL |
| NULL |  9.00000 |     9.9 |
+------+----------+---------+
```

```
SELECT SUM(s2) FROM sum_example;
```

Copy

```
100038 (22018): Numeric value 'one' is not recognized
```

The script below shows the use of this function (and some other aggregate window functions):

```
CREATE OR REPLACE TABLE example_cumulative (p INT, o INT, i INT);

INSERT INTO example_cumulative VALUES
    (  0, 1, 10), (0, 2, 20), (0, 3, 30),
    (100, 1, 10),(100, 2, 30),(100, 2, 5),(100, 3, 11),(100, 3, 120),
    (200, 1, 10000),(200, 1, 200),(200, 1, 808080),(200, 2, 33333),(200, 3, null), (200, 3, 4),
    (300, 1, null), (300, 1, null);
```

Copy

```
SELECT
    p, o, i,
    COUNT(i) OVER (PARTITION BY p ORDER BY o ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) count_i_Rows_Pre,
    SUM(i)   OVER (PARTITION BY p ORDER BY o ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) sum_i_Rows_Pre,
    AVG(i)   OVER (PARTITION BY p ORDER BY o ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) avg_i_Rows_Pre,
    MIN(i)   OVER (PARTITION BY p ORDER BY o ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) min_i_Rows_Pre,
    MAX(i)   OVER (PARTITION BY p ORDER BY o ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) max_i_Rows_Pre
  FROM example_cumulative
  ORDER BY p,o;
+-----+---+--------+------------------+----------------+----------------+----------------+----------------+
|   P | O |      I | COUNT_I_ROWS_PRE | SUM_I_ROWS_PRE | AVG_I_ROWS_PRE | MIN_I_ROWS_PRE | MAX_I_ROWS_PRE |
|-----+---+--------+------------------+----------------+----------------+----------------+----------------|
|   0 | 1 |     10 |                1 |             10 |         10.000 |             10 |             10 |
|   0 | 2 |     20 |                2 |             30 |         15.000 |             10 |             20 |
|   0 | 3 |     30 |                3 |             60 |         20.000 |             10 |             30 |
| 100 | 1 |     10 |                1 |             10 |         10.000 |             10 |             10 |
| 100 | 2 |     30 |                2 |             40 |         20.000 |             10 |             30 |
| 100 | 2 |      5 |                3 |             45 |         15.000 |              5 |             30 |
| 100 | 3 |     11 |                4 |             56 |         14.000 |              5 |             30 |
| 100 | 3 |    120 |                5 |            176 |         35.200 |              5 |            120 |
| 200 | 1 |  10000 |                1 |          10000 |      10000.000 |          10000 |          10000 |
| 200 | 1 |    200 |                2 |          10200 |       5100.000 |            200 |          10000 |
| 200 | 1 | 808080 |                3 |         818280 |     272760.000 |            200 |         808080 |
| 200 | 2 |  33333 |                4 |         851613 |     212903.250 |            200 |         808080 |
| 200 | 3 |   NULL |                4 |         851613 |     212903.250 |            200 |         808080 |
| 200 | 3 |      4 |                5 |         851617 |     170323.400 |              4 |         808080 |
| 300 | 1 |   NULL |                0 |           NULL |           NULL |           NULL |           NULL |
| 300 | 1 |   NULL |                0 |           NULL |           NULL |           NULL |           NULL |
+-----+---+--------+------------------+----------------+----------------+----------------+----------------+
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
3. [Usage notes](#usage-notes)
4. [Examples](#examples)