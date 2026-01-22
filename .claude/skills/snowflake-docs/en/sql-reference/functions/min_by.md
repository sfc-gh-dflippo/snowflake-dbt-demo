---
auto_generated: true
description: Aggregate functions (General)
last_scraped: '2026-01-14T16:56:10.421985+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/min_by
title: MIN_BY | Snowflake Documentation
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

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)[Aggregate](../functions-aggregation.md)MIN\_BY

Categories:
:   [Aggregate functions](../functions-aggregation) (General)

# MIN\_BY[¶](#min-by "Link to this heading")

Finds the row(s) containing the minimum value for a column and returns the value of another column in that row.

For example, if a table contains the columns `employee_id` and `salary`, `MIN_BY(employee_id, salary)` returns the value
of the `employee_id` column for the row that has the lowest value in the `salary` column.

If multiple rows contain the specified minimum value, the function is non-deterministic.

To return values for multiple rows, specify the optional `maximum_number_of_values_to_return` argument. With this
additional argument:

* The function returns an [ARRAY](../data-types-semistructured.html#label-data-type-array) containing the values of a column for the rows with the lowest
  values of a specified column.
* The values in the ARRAY are sorted by their corresponding values in the column containing the minimum values.
* If multiple rows contain these lowest values, the function is non-deterministic.

For example, `MIN_BY(employee_id, salary, 5)` returns an ARRAY of values of the `employee_id` column for the five rows
containing the lowest values in the `salary` column. The IDs in the ARRAY are sorted by the corresponding values in the
`salary` column.

See also:
:   [MIN](min)

## Syntax[¶](#syntax "Link to this heading")

```
MIN_BY( <col_to_return>, <col_containing_mininum> [ , <maximum_number_of_values_to_return> ] )
```

Copy

## Arguments[¶](#arguments "Link to this heading")

**Required:**

`col_to_return`
:   Column containing the value to return.

`col_containing_mininum`
:   Column containing the minimum value.

**Optional:**

`maximum_number_of_values_to_return`
:   Constant integer specifying the maximum number of values to return. You must specify a positive number. The maximum number that
    you can specify is `1000`.

## Returns[¶](#returns "Link to this heading")

* If `maximum_number_of_values_to_return` is not specified, the function returns a value of the same type as
  `col_to_return`.
* If `maximum_number_of_values_to_return` is specified, the function returns an ARRAY containing values of the same type
  as `col_to_return`. The values in the ARRAY are sorted by their corresponding `col_containing_mininum` values.

  For example, `MIN_BY(employee_id, salary, 5)` returns the IDs of the employees with the lowest five salaries, sorted by
  `salary` (in ascending order).

## Usage notes[¶](#usage-notes "Link to this heading")

* The function ignores NULL values in `col_containing_mininum`.
* If all values in `col_containing_mininum` are NULL, the function returns NULL (regardless of whether the optional
  `maximum_number_of_values_to_return` argument is specified).

## Examples[¶](#examples "Link to this heading")

The following examples demonstrate how to use the MIN\_BY function.

To run these examples, execute the following statements to set up the table and data for the examples:

```
CREATE OR REPLACE TABLE employees(employee_id NUMBER, department_id NUMBER, salary NUMBER);

INSERT INTO employees VALUES
  (1001, 10, 10000),
  (1020, 10, 9000),
  (1030, 10, 8000),
  (900, 20, 15000),
  (2000, 20, NULL),
  (2010, 20, 15000),
  (2020, 20, 8000);
```

Copy

Execute the following statement to view the contents of this table:

```
SELECT * FROM employees;
```

Copy

```
+-------------+---------------+--------+
| EMPLOYEE_ID | DEPARTMENT_ID | SALARY |
|-------------+---------------+--------|
|        1001 |            10 |  10000 |
|        1020 |            10 |   9000 |
|        1030 |            10 |   8000 |
|         900 |            20 |  15000 |
|        2000 |            20 |   NULL |
|        2010 |            20 |  15000 |
|        2020 |            20 |   8000 |
+-------------+---------------+--------+
```

The following example returns the ID of the employee with the lowest salary:

```
SELECT MIN_BY(employee_id, salary) FROM employees;
```

Copy

```
+-----------------------------+
| MIN_BY(EMPLOYEE_ID, SALARY) |
|-----------------------------|
|                        1030 |
+-----------------------------+
```

Note the following:

* Because more than one row contains the minimum value for the `salary` column, the function is non-deterministic and might
  return the employee ID for a different row in subsequent executions.
* The function ignores the NULL value in the `salary` column when determining the rows with the minimum values.

The following example returns an ARRAY containing the IDs of the employees with the three lowest salaries:

```
SELECT MIN_BY(employee_id, salary, 3) FROM employees;

+--------------------------------+
| MIN_BY(EMPLOYEE_ID, SALARY, 3) |
|--------------------------------|
| [                              |
|   1030,                        |
|   2020,                        |
|   1020                         |
| ]                              |
+--------------------------------+
```

Copy

As shown in the example, the values in the ARRAY are sorted by their corresponding values in the `salary` column. So,
MIN\_BY returns the IDs of employees sorted by their salary in ascending order.

If more than one of these rows contain the same value in the `salary` column, the order of the returned values for that salary
is non-deterministic.

See also [Using the MIN\_BY and MAX\_BY aggregate functions](../../user-guide/querying-time-series-data.html#label-using-min-by-and-max-by).

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