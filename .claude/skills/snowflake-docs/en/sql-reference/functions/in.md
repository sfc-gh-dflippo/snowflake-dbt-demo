---
auto_generated: true
description: Conditional expression functions
last_scraped: '2026-01-14T16:57:08.635471+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/in
title: '[ NOT ] IN | Snowflake Documentation'
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

     + [[NOT] BETWEEN](/en/sql-reference/functions/between "[NOT] BETWEEN")
     + [BOOLAND](booland.md)
     + [BOOLNOT](boolnot.md)
     + [BOOLOR](boolor.md)
     + [BOOLXOR](boolxor.md)
     + [CASE](case.md)
     + [COALESCE](coalesce.md)
     + [DECODE](decode.md)
     + [EQUAL\_NULL](equal_null.md)
     + [GREATEST](greatest.md)
     + [GREATEST\_IGNORE\_NULLS](greatest_ignore_nulls.md)
     + [IFF](iff.md)
     + [IFNULL](ifnull.md)
     + [[NOT] IN](/en/sql-reference/functions/in "[NOT] IN")
     + [IS [NOT] DISTINCT FROM](/en/sql-reference/functions/is-distinct-from "IS [NOT] DISTINCT FROM")
     + [IS [NOT] NULL](/en/sql-reference/functions/is-null "IS [NOT] NULL")
     + [IS\_NULL\_VALUE](is_null_value.md)
     + [LEAST](least.md)
     + [LEAST\_IGNORE\_NULLS](least_ignore_nulls.md)
     + [NULLIF](nullif.md)
     + [NULLIFZERO](nullifzero.md)
     + [NVL](nvl.md)
     + [NVL2](nvl2.md)
     + [REGR\_VALX](regr_valx.md)
     + [REGR\_VALY](regr_valy.md)
     + [ZEROIFNULL](zeroifnull.md)
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

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)[Conditional expression](../expressions-conditional.md)[NOT] IN

Categories:
:   [Conditional expression functions](../expressions-conditional)

# [ NOT ] IN[¶](#not-in "Link to this heading")

Tests whether its argument is or is not one of the members of an explicit list or the result of a subquery.

Note

In subquery form, IN is equivalent to `= ANY` and NOT IN is equivalent to `<> ALL`.

Tip

You can use the search optimization service to improve the performance of queries that call this function.
For details, see [Search optimization service](../../user-guide/search-optimization-service).

## Syntax[¶](#syntax "Link to this heading")

To compare individual values:

```
<value> [ NOT ] IN ( <value_1> [ , <value_2> ...  ] )
```

Copy

To compare *row constructors* (parenthesized lists of values):

```
( <value_A> [, <value_B> ... ] ) [ NOT ] IN (  ( <value_1> [ , <value_2> ... ] )  [ , ( <value_3> [ , <value_4> ... ] )  ...  ]  )
```

Copy

To compare a value to the values returned by a subquery:

```
<value> [ NOT ] IN ( <subquery> )
```

Copy

## Parameters[¶](#parameters "Link to this heading")

`value`
:   The value for which to search.

`value_A`, `value_B`
:   The elements of a row constructor for which to search.

    Ensure that each value on the right of IN (for example, `(value3, value4)`) has the same number of elements as the value on the
    left of IN (for example, `(value_A, value_B)`).

`value_#`
:   A value to which `value` should be compared.

    If the values to compare to are row constructors, then each `value_#` is an individual element of a row constructor.

`subquery`
:   A subquery that returns a list of values to which `value` can be compared.

## Usage notes[¶](#usage-notes "Link to this heading")

* As in most contexts, NULL is not equal to NULL. If `value` is NULL, then the
  return value of the function is NULL, whether or not the list or subquery
  contains NULL. See [Using NULL](#label-in-list-null-examples).
* Syntactically, IN is treated as an operator rather than a function. This example shows the difference between
  using IN as an operator and calling `f()` as a function:

  ```
  SELECT
      f(a, b),
      x IN (y, z) ...
  ```

  Copy

  You *can’t* use function syntax with IN. For example, you can’t rewrite the preceding example as:

  ```
  SELECT
      f(a, b),
      IN(x, (y, z)) ...
  ```

  Copy
* IN is also considered a [subquery operator](../operators-subquery).
* In a query that uses IN, you can expand an [array](../data-types-semistructured.html#label-data-type-array) into
  a list of individual values by using the spread operator (`**`). For more information and
  examples, see [Expansion operators](../operators-expansion).

## Collation details[¶](#collation-details "Link to this heading")

Arguments with collation specifications currently aren’t supported.

## Examples[¶](#examples "Link to this heading")

The following examples use the IN function.

### Using IN with simple literals[¶](#using-in-with-simple-literals "Link to this heading")

The following examples show how to use IN and NOT IN with simple literals:

```
SELECT 1 IN (1, 2, 3) AS RESULT;
```

Copy

```
+--------+
| RESULT |
|--------|
| True   |
+--------+
```

```
SELECT 4 NOT IN (1, 2, 3) AS RESULT;
```

Copy

```
+--------+
| RESULT |
|--------|
| True   |
+--------+
```

### Using IN with a subquery[¶](#using-in-with-a-subquery "Link to this heading")

These example shows how to use IN in a subquery.

```
SELECT 'a' IN (
  SELECT column1 FROM VALUES ('b'), ('c'), ('d')
  ) AS RESULT;
```

Copy

```
+--------+
| RESULT |
|--------|
| False  |
+--------+
```

### Using IN with a table[¶](#using-in-with-a-table "Link to this heading")

These examples show how to use IN with a table. The statement below creates the table used in the examples.

```
CREATE OR REPLACE TABLE in_function_demo (
  col_1 INTEGER,
  col_2 INTEGER,
  col_3 INTEGER);

INSERT INTO in_function_demo (col_1, col_2, col_3) VALUES
  (1, 1, 1),
  (1, 2, 3),
  (4, 5, NULL);
```

Copy

This example shows how to use IN with a single column of a table:

```
SELECT col_1, col_2, col_3
  FROM in_function_demo
  WHERE (col_1) IN (1, 10, 100, 1000)
  ORDER BY col_1, col_2, col_3;
```

Copy

```
+-------+-------+-------+
| COL_1 | COL_2 | COL_3 |
|-------+-------+-------|
|     1 |     1 |     1 |
|     1 |     2 |     3 |
+-------+-------+-------+
```

This example shows how to use IN with multiple columns of a table:

```
SELECT col_1, col_2, col_3
  FROM in_function_demo
  WHERE (col_1, col_2, col_3) IN (
    (1,2,3),
    (4,5,6));
```

Copy

```
+-------+-------+-------+
| COL_1 | COL_2 | COL_3 |
|-------+-------+-------|
|     1 |     2 |     3 |
+-------+-------+-------+
```

This example shows how to use IN with a subquery that reads multiple columns of a table:

```
SELECT (1, 2, 3) IN (
  SELECT col_1, col_2, col_3 FROM in_function_demo
  ) AS RESULT;
```

Copy

```
+--------+
| RESULT |
|--------|
| True   |
+--------+
```

### Using NULL[¶](#using-null "Link to this heading")

Remember that NULL != NULL. IN and NOT IN lists that contain comparisons with NULL (including equality conditions) might produce unexpected
results because NULL represents an unknown value. Comparisons with NULL do not return TRUE or FALSE; they return NULL. See also
[Ternary logic](../ternary-logic).

For example, the following query returns NULL, not TRUE, because SQL cannot determine whether NULL equals any value, including another NULL.

```
SELECT NULL IN (1, 2, NULL) AS RESULT;
```

Copy

```
+--------+
| RESULT |
|--------|
| NULL   |
+--------+
```

Note that if you change the query to select `1`, not NULL, it returns TRUE:

```
SELECT 1 IN (1, 2, NULL) AS RESULT;
```

Copy

```
+--------+
| RESULT |
|--------|
| True   |
+--------+
```

In this case, the result is TRUE because `1` does have a match in the IN list. The fact that NULL also exists
in the IN list doesn’t affect the result.

Similarly, NOT IN comparisons with NULL also return NULL if any value in the list is NULL.

```
SELECT 1 NOT IN (1, 2, NULL) AS RESULT;
```

Copy

```
+--------+
| RESULT |
|--------|
| NULL  |
+--------+
```

The same behavior is true for the following query, where the set of values `4, 5, NULL` *does not match* either `4, 5, NULL` or `7, 8, 9`:

```
SELECT (4, 5, NULL) IN ( (4, 5, NULL), (7, 8, 9) ) AS RESULT;
```

Copy

The following example shows the same behavior with NULL comparisions but uses a subquery to define the IN list values that are compared:

```
CREATE OR REPLACE TABLE in_list_table (
  val1 INTEGER,
  val2 INTEGER,
  val3 INTEGER
);

INSERT INTO in_list_table VALUES (1, 10, NULL), (2, 20, NULL), (NULL, NULL, NULL);

SELECT 1 IN (SELECT val1 FROM in_list_table) AS RESULT;
```

Copy

```
+--------+
| RESULT |
|--------|
| True   |
+--------+
```

```
SELECT NULL IN (SELECT val1 FROM in_list_table) AS RESULT;
```

Copy

```
+--------+
| RESULT |
|--------|
| NULL   |
+--------+
```

```
SELECT 3 IN (SELECT val1 FROM in_list_table) AS RESULT;
```

Copy

```
+--------+
| RESULT |
|--------|
| NULL   |
+--------+
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
2. [Parameters](#parameters)
3. [Usage notes](#usage-notes)
4. [Collation details](#collation-details)
5. [Examples](#examples)