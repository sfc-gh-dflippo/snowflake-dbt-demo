---
auto_generated: true
description: Window function syntax and usage (Ranking)
last_scraped: '2026-01-14T16:54:38.781483+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/lag
title: LAG | Snowflake Documentation
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

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)[Window](../functions-window.md)LAG

Categories:
:   [Window function syntax and usage](../functions-window-syntax) (Ranking)

# LAG[¶](#lag "Link to this heading")

Accesses data in a previous row in the same result set without having to join the table to itself.

See also:
:   [LEAD](lead)

## Syntax[¶](#syntax "Link to this heading")

```
LAG ( <expr> [ , <offset> , <default> ] ) [ { IGNORE | RESPECT } NULLS ]
    OVER ( [ PARTITION BY <expr1> ] ORDER BY <expr2> [ { ASC | DESC } ] [ NULLS { FIRST | LAST } ] )
```

Copy

## Arguments[¶](#arguments "Link to this heading")

`expr`
:   The expression to be returned based on the specified offset.

`offset`
:   The number of rows backward from the current row from which to obtain a value. For example, an `offset` of 2 returns
    the `expr` value with an interval of 2 rows.

    Note that setting a negative offset has the same effect as using the [LEAD](lead) function.

    Default is 1.

`default`
:   The expression to return when the offset goes out of the bounds of the window. Supports any expression whose type is compatible with `expr`.

    Default is NULL.

`{ IGNORE | RESPECT } NULLS`
:   Whether to ignore or respect NULL values when an `expr` contains NULL values:

    * `IGNORE NULLS` excludes any row whose expression evaluates to NULL when offset rows are counted.
    * `RESPECT NULLS` includes any row whose expression evaluates to NULL when offset rows are counted.

    Default: `RESPECT NULLS`

## Usage notes[¶](#usage-notes "Link to this heading")

* The PARTITION BY clause partitions the result set produced by the FROM clause into partitions to which the function is applied.
  For more information, see [Window function syntax and usage](../functions-window-syntax).
* The ORDER BY clause orders the data within each partition.

## Examples[¶](#examples "Link to this heading")

Create the table and load the data:

```
CREATE OR REPLACE TABLE sales(
  emp_id INTEGER,
  year INTEGER,
  revenue DECIMAL(10,2));
```

Copy

```
INSERT INTO sales VALUES
  (0, 2010, 1000),
  (0, 2011, 1500),
  (0, 2012, 500),
  (0, 2013, 750);
INSERT INTO sales VALUES
  (1, 2010, 10000),
  (1, 2011, 12500),
  (1, 2012, 15000),
  (1, 2013, 20000);
INSERT INTO sales VALUES
  (2, 2012, 500),
  (2, 2013, 800);
```

Copy

This query shows the difference between this year’s revenue and the previous year’s revenue:

```
SELECT emp_id, year, revenue,
       revenue - LAG(revenue, 1, 0) OVER (PARTITION BY emp_id ORDER BY year) AS diff_to_prev
  FROM sales
  ORDER BY emp_id, year;
```

Copy

```
+--------+------+----------+--------------+
| EMP_ID | YEAR |  REVENUE | DIFF_TO_PREV |
|--------+------+----------+--------------|
|      0 | 2010 |  1000.00 |      1000.00 |
|      0 | 2011 |  1500.00 |       500.00 |
|      0 | 2012 |   500.00 |     -1000.00 |
|      0 | 2013 |   750.00 |       250.00 |
|      1 | 2010 | 10000.00 |     10000.00 |
|      1 | 2011 | 12500.00 |      2500.00 |
|      1 | 2012 | 15000.00 |      2500.00 |
|      1 | 2013 | 20000.00 |      5000.00 |
|      2 | 2012 |   500.00 |       500.00 |
|      2 | 2013 |   800.00 |       300.00 |
+--------+------+----------+--------------+
```

Create another table and load the data:

```
CREATE OR REPLACE TABLE t1 (
  col_1 NUMBER,
  col_2 NUMBER);
```

Copy

```
INSERT INTO t1 VALUES
  (1, 5),
  (2, 4),
  (3, NULL),
  (4, 2),
  (5, NULL),
  (6, NULL),
  (7, 6);
```

Copy

This query shows how the IGNORE NULLS clause affects the output.
All rows (except the first) contain non-NULL values even if the preceding row contained NULL.
If the preceding row contained NULL, then the current row uses the most recent non-NULL value.

```
SELECT col_1,
       col_2,
       LAG(col_2) IGNORE NULLS OVER (ORDER BY col_1)
  FROM t1
  ORDER BY col_1;
```

Copy

```
+-------+-------+-----------------------------------------------+
| COL_1 | COL_2 | LAG(COL_2) IGNORE NULLS OVER (ORDER BY COL_1) |
|-------+-------+-----------------------------------------------|
|     1 |     5 |                                          NULL |
|     2 |     4 |                                             5 |
|     3 |  NULL |                                             4 |
|     4 |     2 |                                             4 |
|     5 |  NULL |                                             2 |
|     6 |  NULL |                                             2 |
|     7 |     6 |                                             2 |
+-------+-------+-----------------------------------------------+
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
3. [Usage notes](#usage-notes)
4. [Examples](#examples)