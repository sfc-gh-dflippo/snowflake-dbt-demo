---
auto_generated: true
description: Window function syntax and usage (Ranking)
last_scraped: '2026-01-14T16:54:31.631291+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/nth_value
title: NTH_VALUE | Snowflake Documentation
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

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)[Window](../functions-window.md)NTH\_VALUE

Categories:
:   [Window function syntax and usage](../functions-window-syntax) (Ranking)

# NTH\_VALUE[¶](#nth-value "Link to this heading")

Returns the nth value (up to 1000) within an ordered group of values.

See also:
:   [FIRST\_VALUE](first_value) , [LAST\_VALUE](last_value)

## Syntax[¶](#syntax "Link to this heading")

```
NTH_VALUE( <expr> , <n> ) [ FROM { FIRST | LAST } ] [ { IGNORE | RESPECT } NULLS ]
  OVER ( [ PARTITION BY <expr1> ] ORDER BY <expr2> [ { ASC | DESC } ] [ NULLS { FIRST | LAST } ] [ <window_frame> ] )
```

Copy

For detailed `window_frame` syntax, see [Window function syntax and usage](../functions-window-syntax).

## Arguments[¶](#arguments "Link to this heading")

`n`
:   This specifies which value of N to use when looking for the Nth value.

`expr`
:   The expression that determines the return value.

`expr1`
:   The expression by which to partition the rows. You can specify a single expression or a comma-separated list of expressions.
    For example:

    ```
    PARTITION BY column_1, column_2
    ```

    Copy

`expr2`
:   The expression by which to order the rows. You can specify a single expression or a comma-separated list of expressions.
    For example:

    ```
    ORDER BY column_3, column_4
    ```

    Copy

`FROM { FIRST | LAST }`
:   Whether to ignore or respect NULL values when an `expr` contains NULL values:

    * `FROM FIRST` starts from the beginning of the ordered list and moves forward.
    * `FROM LAST` starts from the end of the ordered list and moves backward.

    Default: `FROM FIRST`

`{ IGNORE | RESPECT } NULLS`
:   Whether to ignore or respect NULL values when an `expr` contains NULL values:

    * `IGNORE NULLS` skips NULL values in the expression.
    * `RESPECT NULLS` returns a NULL value if it is the nth value in the expression.

    Default: `RESPECT NULLS`

## Usage notes[¶](#usage-notes "Link to this heading")

* Input value `n` can’t be greater than 1000.

* This function is a rank-related function, so it must specify a window. A window clause consists of the following subclauses:

  > + `PARTITION BY expr1` subclause (optional).
  > + `ORDER BY expr2` subclause (required). For details about additional supported ordering options (sort order, ordering
  >   of NULL values, and so on), see the documentation for the [ORDER BY](../constructs/order-by) clause, which follows
  >   the same rules.
  > + `window_frame` subclause (optional).
* The order of rows in a window (and thus the result of the query) is fully deterministic only if the keys in the ORDER BY clause
  make each row unique. Consider the following example:

  ```
  ... OVER (PARTITION BY p ORDER BY o COLLATE 'lower') ...
  ```

  Copy

  The query result can vary if any partition contains values of column `o` that are identical, or would be identical
  in a case-insensitive comparison.
* The ORDER BY clause inside the OVER clause controls the order of rows only within the window, not the order of rows in the output
  of the entire query. To control output order, use a separate ORDER BY clause at the outermost level of the query.

* The optional `window_frame` (cumulative or sliding) specifies the subset of rows within the window for which the function
  is calculated. If no `window_frame` is specified, the default is the entire window:

  > `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`

  Note that this deviates from the ANSI standard, which specifies the following default for window frames:

  > `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`

For more information about window frames, including syntax, usage notes, and examples, see [Window function syntax and usage](../functions-window-syntax).

## Examples[¶](#examples "Link to this heading")

```
SELECT column1,
       column2,
       NTH_VALUE(column2, 2) OVER (PARTITION BY column1 ORDER BY column2) AS column2_2nd
  FROM VALUES
    (1, 10), (1, 11), (1, 12),
    (2, 20), (2, 21), (2, 22);
```

Copy

```
+---------+---------+-------------+
| COLUMN1 | COLUMN2 | COLUMN2_2ND |
|---------+---------+-------------|
|       1 |      10 |          11 |
|       1 |      11 |          11 |
|       1 |      12 |          11 |
|       2 |      20 |          21 |
|       2 |      21 |          21 |
|       2 |      22 |          21 |
+---------+---------+-------------+
```

The following example returns the results of three related functions: [FIRST\_VALUE](first_value),
NTH\_VALUE, and [LAST\_VALUE](last_value).

* The query creates a sliding window frame that is three rows wide, which contains:

  + The row that precedes the current row.
  + The current row.
  + The row that follows the current row.
* The `2` in the call `NTH_VALUE(i, 2)` specifies the second row in the window frame (which, in this case, is
  also the current row).
* When the current row is the very first row in the window frame, there is no preceding row to reference, so
  FIRST\_VALUE returns a NULL for that row.
* Frame boundaries sometimes extend beyond the rows in a partition, but non-existent rows are not included in window function
  calculations. For example, when the current row is the very first row in the partition and the window frame is
  `ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING`, there is no preceding row to reference, so the FIRST\_VALUE function returns the
  value of the first row in the partition.
* The results never match for all three functions, given the data in the table. These functions select the *first*,
  *last*, or *nth* value for each row in the frame, and the selection of values applies separately to each partition.

To run this example, first create and load the table:

```
CREATE TABLE demo1 (i INTEGER, partition_col INTEGER, order_col INTEGER);

INSERT INTO demo1 (i, partition_col, order_col) VALUES
  (1, 1, 1),
  (2, 1, 2),
  (3, 1, 3),
  (4, 1, 4),
  (5, 1, 5),
  (1, 2, 1),
  (2, 2, 2),
  (3, 2, 3),
  (4, 2, 4);
```

Copy

Now run the following query:

```
SELECT partition_col, order_col, i,
       FIRST_VALUE(i)  OVER (PARTITION BY partition_col ORDER BY order_col
         ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) AS FIRST_VAL,
       NTH_VALUE(i, 2) OVER (PARTITION BY partition_col ORDER BY order_col
         ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) AS NTH_VAL,
       LAST_VALUE(i)   OVER (PARTITION BY partition_col ORDER BY order_col
         ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) AS LAST_VAL
  FROM demo1
  ORDER BY partition_col, i, order_col;
```

Copy

```
+---------------+-----------+---+-----------+---------+----------+
| PARTITION_COL | ORDER_COL | I | FIRST_VAL | NTH_VAL | LAST_VAL |
|---------------+-----------+---+-----------+---------+----------|
|             1 |         1 | 1 |         1 |       2 |        2 |
|             1 |         2 | 2 |         1 |       2 |        3 |
|             1 |         3 | 3 |         2 |       3 |        4 |
|             1 |         4 | 4 |         3 |       4 |        5 |
|             1 |         5 | 5 |         4 |       5 |        5 |
|             2 |         1 | 1 |         1 |       2 |        2 |
|             2 |         2 | 2 |         1 |       2 |        3 |
|             2 |         3 | 3 |         2 |       3 |        4 |
|             2 |         4 | 4 |         3 |       4 |        4 |
+---------------+-----------+---+-----------+---------+----------+
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