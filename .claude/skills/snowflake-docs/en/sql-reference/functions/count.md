---
auto_generated: true
description: Aggregate functions (General) , Window functions
last_scraped: '2026-01-14T16:54:35.903872+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/count
title: COUNT | Snowflake Documentation
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

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)[Aggregate](../functions-aggregation.md)COUNT

Categories:
:   [Aggregate functions](../functions-aggregation) (General) , [Window functions](../functions-window)

# COUNT[¶](#count "Link to this heading")

Returns either the number of non-NULL records for the specified columns, or the total number of records.

See also:
:   [COUNT\_IF](count_if), [MAX](max), [MIN](min) , [SUM](sum)

## Syntax[¶](#syntax "Link to this heading")

**Aggregate function**

```
COUNT( [ DISTINCT ] <expr1> [ , <expr2> ... ] )

COUNT(*)

COUNT(<alias>.*)
```

Copy

**Window function**

```
COUNT( [ DISTINCT ] <expr1> [ , <expr2> ... ] ) OVER (
                                                     [ PARTITION BY <expr3> ]
                                                     [ ORDER BY <expr4> [ { ASC | DESC } ] [ NULLS { FIRST | LAST } ] [ <window_frame> ] ]
                                                     )
```

Copy

For detailed `window_frame` syntax, see [Window function syntax and usage](../functions-window-syntax).

## Arguments[¶](#arguments "Link to this heading")

`expr1`
:   A column name, which can be a qualified name (for example, database.schema.table.column\_name).

`expr2`
:   You can include additional column name(s) if you wish. For example, you
    could count the number of distinct combinations of last name and first name.

`expr3`
:   The column to partition on, if you want the result to be split into multiple
    windows.

`expr4`
:   The column to order each window on. Note that this is separate from any
    ORDER BY clause to order the final result set.

`*`
:   Returns the total number of records.

    When you pass a wildcard to the function, you can qualify the wildcard with the name or alias for the table.
    For example, to pass in all of the columns from the table named `mytable`, specify the following:

    ```
    (mytable.*)
    ```

    Copy

    You can also use the ILIKE and EXCLUDE keywords for filtering:

    * ILIKE filters for column names that match the specified pattern. Only one
      pattern is allowed. For example:

      ```
      (* ILIKE 'col1%')
      ```

      Copy
    * EXCLUDE filters out column names that don’t match the specified column or columns. For example:

      ```
      (* EXCLUDE col1)

      (* EXCLUDE (col1, col2))
      ```

      Copy

    Qualifiers are valid when you use these keywords. The following example uses the ILIKE keyword to
    filter for all of the columns that match the pattern `col1%` in the table `mytable`:

    ```
    (mytable.* ILIKE 'col1%')
    ```

    Copy

    The ILIKE and EXCLUDE keywords can’t be combined in a single function call.

    If you specify an unqualified and unfiltered wildcard (`*`), the function returns the total number of records, including
    records with NULL values.

    If you specify a wildcard with the ILIKE or EXCLUDE keyword for filtering, the function excludes records with NULL values.

    For this function, the ILIKE and EXCLUDE keywords are valid only in a SELECT list or GROUP BY clause.

    For more information about the ILIKE and EXCLUDE keywords, see the “Parameters” section in [SELECT](../sql/select).

`alias.*`
:   Returns the number of records that don’t contain any NULL values. For an example, see [Examples](#examples).

## Returns[¶](#returns "Link to this heading")

Returns a value of type NUMBER.

## Usage notes[¶](#usage-notes "Link to this heading")

* This function treats [JSON null](../../user-guide/semistructured-considerations.html#label-variant-null) (VARIANT NULL) as SQL NULL.
* For more information about NULL values and aggregate functions, see
  [Aggregate functions and NULL values](../functions-aggregation.html#label-aggregate-functions-and-null-values).
* When this function is called as an aggregate function:

  + If the `DISTINCT` keyword is used, it applies to all columns. For example,
    `DISTINCT col1, col2, col3` means to return the number of different
    combinations of columns `col1`, `col2`, and `col3`. For example, assume the data is:

    ```
    1, 1, 1
    1, 1, 1
    1, 1, 1
    1, 1, 2
    ```

    Copy

    In this case, the function returns `2`, because that’s the number of distinct combinations of values in the three columns.

* When this function is called as a window function with an OVER clause that contains an ORDER BY clause:

  + A window frame is required. If no window frame is specified explicitly, the following implied window frame is used:

    `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`

    For more information about window frames, including syntax, usage notes, and examples, see [Window function syntax and usage](../functions-window-syntax).
  + Using the keyword DISTINCT inside the window function is prohibited and results in a compile-time error.

* To return the number of rows that match a condition, use [COUNT\_IF](count_if).
* When possible, use the COUNT function on tables and views without a [row access policy](../../user-guide/security-row-intro.html#label-security-row-intro-considerations).
  The query with this function is faster and more accurate on tables or views without a row access policy. The reasons for the performance
  difference include:

  + Snowflake maintains statistics on tables and views, and this optimization allows simple queries to run faster.
  + When a row access policy is set on a table or view and the COUNT function is used in a query, Snowflake must scan each row and
    determine whether the user is allowed to view the row.

## Examples[¶](#examples "Link to this heading")

The following examples use the COUNT function on data with NULL values.

Create a table and insert values:

```
CREATE TABLE basic_example (i_col INTEGER, j_col INTEGER);
INSERT INTO basic_example VALUES
    (11,101), (11,102), (11,NULL), (12,101), (NULL,101), (NULL,102);
```

Copy

Query the table:

```
SELECT *
    FROM basic_example
    ORDER BY i_col;
```

Copy

```
+-------+-------+
| I_COL | J_COL |
|-------+-------|
|    11 |   101 |
|    11 |   102 |
|    11 |  NULL |
|    12 |   101 |
|  NULL |   101 |
|  NULL |   102 |
+-------+-------+
```

```
SELECT COUNT(*) AS "All",
       COUNT(* ILIKE 'i_c%') AS "ILIKE",
       COUNT(* EXCLUDE i_col) AS "EXCLUDE",
       COUNT(i_col) AS "i_col", 
       COUNT(DISTINCT i_col) AS "DISTINCT i_col", 
       COUNT(j_col) AS "j_col", 
       COUNT(DISTINCT j_col) AS "DISTINCT j_col"
  FROM basic_example;
```

Copy

```
+-----+-------+---------+-------+----------------+-------+----------------+
| All | ILIKE | EXCLUDE | i_col | DISTINCT i_col | j_col | DISTINCT j_col |
|-----+-------+---------+-------+----------------+-------+----------------|
|   6 |     4 |       5 |     4 |              2 |     5 |              2 |
+-----+-------+---------+-------+----------------+-------+----------------+
```

The `All` column in this output shows that when an unqualified and unfiltered wildcard is specified
for COUNT, the function returns the total number of rows in the table, including rows with NULL values. The other
columns in the output show that when a column or a wildcard with filtering is specified, the function excludes
rows with NULL values.

The next query uses the COUNT function with the GROUP BY clause:

```
SELECT i_col, COUNT(*), COUNT(j_col)
    FROM basic_example
    GROUP BY i_col
    ORDER BY i_col;
```

Copy

```
+-------+----------+--------------+
| I_COL | COUNT(*) | COUNT(J_COL) |
|-------+----------+--------------|
|    11 |        3 |            2 |
|    12 |        1 |            1 |
|  NULL |        2 |            2 |
+-------+----------+--------------+
```

The following example shows that `COUNT(alias.*)` returns the number of rows that don’t contain any NULL values.
The `basic_example` table has a total of six rows, but three rows have at least one NULL value, and the other three rows
have no NULL values.

```
SELECT COUNT(n.*) FROM basic_example AS n;
```

Copy

```
+------------+
| COUNT(N.*) |
|------------|
|          3 |
+------------+
```

The following example shows that [JSON null](../../user-guide/semistructured-considerations.html#label-variant-null) (VARIANT NULL) is treated as SQL NULL by
the COUNT function.

Create the table and insert data that contains both SQL NULL and JSON null values:

```
CREATE OR REPLACE TABLE count_example_with_variant_column (
  i_col INTEGER, 
  j_col INTEGER, 
  v VARIANT);
```

Copy

```
BEGIN WORK;

INSERT INTO count_example_with_variant_column (i_col, j_col, v) 
  VALUES (NULL, 10, NULL);
INSERT INTO count_example_with_variant_column (i_col, j_col, v) 
  SELECT 1, 11, PARSE_JSON('{"Title": null}');
INSERT INTO count_example_with_variant_column (i_col, j_col, v) 
  SELECT 2, 12, PARSE_JSON('{"Title": "O"}');
INSERT INTO count_example_with_variant_column (i_col, j_col, v) 
  SELECT 3, 12, PARSE_JSON('{"Title": "I"}');

COMMIT WORK;
```

Copy

In this SQL code, note the following:

* The first INSERT INTO statement inserts a SQL NULL for both a VARIANT column and a non-VARIANT column.
* The second INSERT INTO statement inserts a JSON null (VARIANT NULL).
* The last two INSERT INTO statements insert non-NULL VARIANT values.

Show the data:

```
SELECT i_col, j_col, v, v:Title
    FROM count_example_with_variant_column
    ORDER BY i_col;
```

Copy

```
+-------+-------+-----------------+---------+
| I_COL | J_COL | V               | V:TITLE |
|-------+-------+-----------------+---------|
|     1 |    11 | {               | null    |
|       |       |   "Title": null |         |
|       |       | }               |         |
|     2 |    12 | {               | "O"     |
|       |       |   "Title": "O"  |         |
|       |       | }               |         |
|     3 |    12 | {               | "I"     |
|       |       |   "Title": "I"  |         |
|       |       | }               |         |
|  NULL |    10 | NULL            | NULL    |
+-------+-------+-----------------+---------+
```

Show that the COUNT function treats both the NULL and the JSON null (VARIANT NULL) values
as NULLs. There are four rows in the table. One has a SQL NULL and the other has a
JSON null. Both those rows are excluded from the count, so the count is `2`.

```
SELECT COUNT(v:Title)
    FROM count_example_with_variant_column;
```

Copy

```
+----------------+
| COUNT(V:TITLE) |
|----------------|
|              2 |
+----------------+
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