---
auto_generated: true
description: Aggregate functions (General) , Window function syntax and usage (General)
last_scraped: '2026-01-14T16:56:56.997348+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/listagg
title: LISTAGG | Snowflake Documentation
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

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)[Aggregate](../functions-aggregation.md)LISTAGG

Categories:
:   [Aggregate functions](../functions-aggregation) (General) , [Window function syntax and usage](../functions-window-syntax) (General)

# LISTAGG[¶](#listagg "Link to this heading")

Returns the concatenated input values, separated by the `delimiter` string.

## Syntax[¶](#syntax "Link to this heading")

**Aggregate function**

```
LISTAGG( [ DISTINCT ] <expr1> [, <delimiter> ] )
    [ WITHIN GROUP ( <orderby_clause> ) ]
```

Copy

**Window function**

```
LISTAGG( [ DISTINCT ] <expr1> [, <delimiter> ] )
    [ WITHIN GROUP ( <orderby_clause> ) ]
    OVER ( [ PARTITION BY <expr2> ] )
```

Copy

## Required arguments[¶](#required-arguments "Link to this heading")

`expr1`
:   An expression (typically a column name) that determines the values to be put into the list.
    The expression must evaluate to a string, or to a data type that can be
    [cast](../data-type-conversion) to string.

`OVER()`
:   The OVER clause is required when the function is being used as a window function.
    For details, see [Window function syntax and usage](../functions-window-syntax).

## Optional arguments[¶](#optional-arguments "Link to this heading")

`DISTINCT`
:   Removes duplicate values from the list.

`delimiter`
:   A string, or an expression that evaluates to a string. Typically, this value is
    a single-character string. The string should be surrounded by single
    quotes, as shown in the examples below.

    If no `delimiter` is specified, an empty string is used as
    the `delimiter`.

    The `delimiter` must be a constant.

`WITHIN GROUP orderby_clause`
:   One or more expressions (typically column names) that determine the order of the values for
    each group in the list.

    The WITHIN GROUP (ORDER BY) syntax supports the same parameters as the
    [ORDER BY](../constructs/order-by) clause in a SELECT statement.

`PARTITION BY expr2`
:   Window function sub-clause that specifies an expression (typically a column name).
    This expression defines partitions that group the input rows before the function is applied.
    For details, see [Window function syntax and usage](../functions-window-syntax).

## Returns[¶](#returns "Link to this heading")

Returns a string that includes all of the non-NULL input values, separated by the `delimiter`.

This function does not return a list or an array. It returns a single string that contains all
of the non-NULL input values.

## Usage notes[¶](#usage-notes "Link to this heading")

* If you do not specify WITHIN GROUP (ORDER BY), the order of elements within each list is unpredictable.
  (An ORDER BY clause outside the WITHIN GROUP clause applies to the order of the output rows, not to the order
  of the list elements within a row.)
* If you specify a number for an expression in WITHIN GROUP (ORDER BY), this number is parsed as a numeric
  constant, not as the ordinal position of a column in the SELECT list. Therefore, do not specify numbers
  as WITHIN GROUP (ORDER BY) expressions.
* If you specify DISTINCT and WITHIN GROUP, both must refer to the same column. For example:

  ```
  SELECT LISTAGG(DISTINCT O_ORDERKEY) WITHIN GROUP (ORDER BY O_ORDERKEY) ...;
  ```

  Copy

  If you specify different columns for DISTINCT and WITHIN GROUP, an error occurs:

  ```
  SELECT LISTAGG(DISTINCT O_ORDERKEY) WITHIN GROUP (ORDER BY O_ORDERSTATUS) ...;
  ```

  Copy

  ```
  SQL compilation error: [ORDERS.O_ORDERSTATUS] is not a valid order by expression
  ```

  You must either specify the same column for DISTINCT and WITHIN GROUP or omit DISTINCT.
* Regarding NULL or empty input values:

  + If the input is empty, an empty string is returned.
  + If all input expressions evaluate to NULL, the output is an empty string.
  + If some but not all input expressions evaluate to NULL, the output contains
    all non-NULL values and excludes the NULL values.

* When this function is called as a window function, it does not support:

  + An ORDER BY clause within the OVER clause.
  + Explicit window frames.

## Collation details[¶](#collation-details "Link to this heading")

* The collation of the result is the same as the collation of the input.
* Elements inside the list are ordered according to collations, if the ORDER BY sub-clause specifies an expression
  with collation.
* The `delimiter` cannot use a collation specification.
* Specifying collation inside ORDER BY does not impact the collation of the result. For example, the statement below
  contains two ORDER BY clauses, one for LISTAGG and one for the query results. Specifying collation inside
  the first one does not affect the collation of the second one. If you need to collate the output in both ORDER BY
  clauses, you must specify collation explicitly in both clauses.

  ```
  SELECT LISTAGG(x, ', ') WITHIN GROUP (ORDER BY last_name COLLATE 'es')
    FROM table1
    ORDER BY last_name;
  ```

  Copy

## Examples[¶](#examples "Link to this heading")

These examples use the LISTAGG function.

### Using the LISTAGG function to concatenate values in query results[¶](#using-the-listagg-function-to-concatenate-values-in-query-results "Link to this heading")

The following examples use the LISTAGG function to concatenate values in the results of
queries on orders data.

Note

These examples query the [TPC-H sample data](../../user-guide/sample-data-tpch). Before
running the queries, execute the following SQL statement:

```
USE SCHEMA snowflake_sample_data.tpch_sf1;
```

Copy

This example lists the distinct `o_orderkey` values for orders with a `o_totalprice` greater than
`520000` and uses and empty string for the `delimiter`:

```
SELECT LISTAGG(DISTINCT o_orderkey, ' ')
  FROM orders
  WHERE o_totalprice > 520000;
```

Copy

```
+-------------------------------------------------+
| LISTAGG(DISTINCT O_ORDERKEY, ' ')               |
|-------------------------------------------------|
| 2232932 1750466 3043270 4576548 4722021 3586919 |
+-------------------------------------------------+
```

This example lists the distinct `o_orderstatus` values for orders with a `o_totalprice` greater than
`520000` and uses a vertical bar for the `delimiter`:

```
SELECT LISTAGG(DISTINCT o_orderstatus, '|')
  FROM orders
  WHERE o_totalprice > 520000;
```

Copy

```
+--------------------------------------+
| LISTAGG(DISTINCT O_ORDERSTATUS, '|') |
|--------------------------------------|
| O|F                                  |
+--------------------------------------+
```

This example lists the `o_orderstatus` and `o_clerk` values of each order with a `o_totalprice` greater than
`520000` grouped by `o_orderstatus`. The query uses a comma for the `delimiter`:

```
SELECT o_orderstatus,
   LISTAGG(o_clerk, ', ')
     WITHIN GROUP (ORDER BY o_totalprice DESC)
  FROM orders
  WHERE o_totalprice > 520000
  GROUP BY o_orderstatus;
```

Copy

```
+---------------+---------------------------------------------------+
| O_ORDERSTATUS | LISTAGG(O_CLERK, ', ')                            |
|               |      WITHIN GROUP (ORDER BY O_TOTALPRICE DESC)    |
|---------------+---------------------------------------------------|
| O             | Clerk#000000699, Clerk#000000336, Clerk#000000245 |
| F             | Clerk#000000040, Clerk#000000230, Clerk#000000924 |
+---------------+---------------------------------------------------+
```

### Using collation with the LISTAGG function[¶](#using-collation-with-the-listagg-function "Link to this heading")

The following examples show [collation](../collation) with the LISTAGG function.
The examples use the following data:

```
CREATE OR REPLACE TABLE collation_demo (
  spanish_phrase VARCHAR COLLATE 'es');
```

Copy

```
INSERT INTO collation_demo (spanish_phrase) VALUES
  ('piña colada'),
  ('Pinatubo (Mount)'),
  ('pint'),
  ('Pinta');
```

Copy

Note the difference in output order with the different
collation specifications. This query uses the `es` collation specification:

```
SELECT LISTAGG(spanish_phrase, '|')
    WITHIN GROUP (ORDER BY COLLATE(spanish_phrase, 'es')) AS es_collation
  FROM collation_demo;
```

Copy

```
+-----------------------------------------+
| ES_COLLATION                            |
|-----------------------------------------|
| Pinatubo (Mount)|pint|Pinta|piña colada |
+-----------------------------------------+
```

This query uses the `utf8` collation specification:

```
SELECT LISTAGG(spanish_phrase, '|')
    WITHIN GROUP (ORDER BY COLLATE(spanish_phrase, 'utf8')) AS utf8_collation
  FROM collation_demo;
```

Copy

```
+-----------------------------------------+
| UTF8_COLLATION                          |
|-----------------------------------------|
| Pinatubo (Mount)|Pinta|pint|piña colada |
+-----------------------------------------+
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
2. [Required arguments](#required-arguments)
3. [Optional arguments](#optional-arguments)
4. [Returns](#returns)
5. [Usage notes](#usage-notes)
6. [Collation details](#collation-details)
7. [Examples](#examples)