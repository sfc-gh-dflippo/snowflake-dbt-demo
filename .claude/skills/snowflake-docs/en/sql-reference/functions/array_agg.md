---
auto_generated: true
description: Aggregate functions (Semi-structured Data) , Window functions (General)
  , Semi-structured and structured data functions (Array/Object)
last_scraped: '2026-01-14T16:56:15.346886+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/array_agg
title: ARRAY_AGG | Snowflake Documentation
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

     + JSON and XML parsing
     + [CHECK\_JSON](check_json.md)
     + [CHECK\_XML](check_xml.md)
     + [JSON\_EXTRACT\_PATH\_TEXT](json_extract_path_text.md)
     + [PARSE\_JSON](parse_json.md)
     + [TRY\_PARSE\_JSON](try_parse_json.md)
     + [PARSE\_XML](parse_xml.md)
     + [STRIP\_NULL\_VALUE](strip_null_value.md)
     + Array/object creation and manipulation
     + [ARRAY\_AGG](array_agg.md)
     + [ARRAY\_APPEND](array_append.md)
     + [ARRAY\_CAT](array_cat.md)
     + [ARRAY\_COMPACT](array_compact.md)
     + [ARRAY\_CONSTRUCT](array_construct.md)
     + [ARRAY\_CONSTRUCT\_COMPACT](array_construct_compact.md)
     + [ARRAY\_CONTAINS](array_contains.md)
     + [ARRAY\_DISTINCT](array_distinct.md)
     + [ARRAY\_EXCEPT](array_except.md)
     + [ARRAY\_FLATTEN](array_flatten.md)
     + [ARRAY\_GENERATE\_RANGE](array_generate_range.md)
     + [ARRAY\_INSERT](array_insert.md)
     + [ARRAY\_INTERSECTION](array_intersection.md)
     + [ARRAY\_MAX](array_max.md)
     + [ARRAY\_MIN](array_min.md)
     + [ARRAY\_POSITION](array_position.md)
     + [ARRAY\_PREPEND](array_prepend.md)
     + [ARRAY\_REMOVE](array_remove.md)
     + [ARRAY\_REMOVE\_AT](array_remove_at.md)
     + [ARRAY\_REVERSE](array_reverse.md)
     + [ARRAY\_SIZE](array_size.md)
     + [ARRAY\_SLICE](array_slice.md)
     + [ARRAY\_SORT](array_sort.md)
     + [ARRAY\_TO\_STRING](array_to_string.md)
     + [ARRAY\_UNION\_AGG](array_union_agg.md)
     + [ARRAY\_UNIQUE\_AGG](array_unique_agg.md)
     + [ARRAYS\_OVERLAP](arrays_overlap.md)
     + [ARRAYS\_TO\_OBJECT](arrays_to_object.md)
     + [ARRAYS\_ZIP](arrays_zip.md)
     + [OBJECT\_AGG](object_agg.md)
     + [OBJECT\_CONSTRUCT](object_construct.md)
     + [OBJECT\_CONSTRUCT\_KEEP\_NULL](object_construct_keep_null.md)
     + [OBJECT\_DELETE](object_delete.md)
     + [OBJECT\_INSERT](object_insert.md)
     + [OBJECT\_PICK](object_pick.md)
     + [PROMPT](prompt.md)
     + Higher-order
     + [FILTER](filter.md)
     + [REDUCE](reduce.md)
     + [TRANSFORM](transform.md)
     + Map creation and manipulation
     + [MAP\_CAT](map_cat.md)
     + [MAP\_CONTAINS\_KEY](map_contains_key.md)
     + [MAP\_DELETE](map_delete.md)
     + [MAP\_INSERT](map_insert.md)
     + [MAP\_KEYS](map_keys.md)
     + [MAP\_PICK](map_pick.md)
     + [MAP\_SIZE](map_size.md)
     + Extraction
     + [FLATTEN](flatten.md)
     + [GET](get.md)
     + [GET\_IGNORE\_CASE](get_ignore_case.md)
     + [GET\_PATH, :](get_path.md)
     + [OBJECT\_KEYS](object_keys.md)
     + [XMLGET](xmlget.md)
     + Conversion/casting
     + [AS\_<object\_type>](as.md)
     + [AS\_ARRAY](as_array.md)
     + [AS\_BINARY](as_binary.md)
     + [AS\_BOOLEAN](as_boolean.md)
     + [AS\_CHAR](as_char-varchar.md)
     + [AS\_VARCHAR](as_char-varchar.md)
     + [AS\_DATE](as_date.md)
     + [AS\_DECIMAL](as_decimal-number.md)
     + [AS\_NUMBER](as_decimal-number.md)
     + [AS\_DOUBLE](as_double-real.md)
     + [AS\_REAL](as_double-real.md)
     + [AS\_INTEGER](as_integer.md)
     + [AS\_OBJECT](as_object.md)
     + [AS\_TIME](as_time.md)
     + [AS\_TIMESTAMP\_LTZ](as_timestamp.md)
     + [AS\_TIMESTAMP\_NTZ](as_timestamp.md)
     + [AS\_TIMESTAMP\_TZ](as_timestamp.md)
     + [STRTOK\_TO\_ARRAY](strtok_to_array.md)
     + [TO\_ARRAY](to_array.md)
     + [TO\_JSON](to_json.md)
     + [TO\_OBJECT](to_object.md)
     + [TO\_VARIANT](to_variant.md)
     + [TO\_XML](to_xml.md)
     + Type predicates
     + [IS\_<object\_type>](is.md)
     + [IS\_ARRAY](is_array.md)
     + [IS\_BINARY](is_binary.md)
     + [IS\_BOOLEAN](is_boolean.md)
     + [IS\_CHAR](is_char-varchar.md)
     + [IS\_VARCHAR](is_char-varchar.md)
     + [IS\_DATE](is_date-value.md)
     + [IS\_DATE\_VALUE](is_date-value.md)
     + [IS\_DECIMAL](is_decimal.md)
     + [IS\_DOUBLE](is_double-real.md)
     + [IS\_REAL](is_double-real.md)
     + [IS\_INTEGER](is_integer.md)
     + [IS\_NULL\_VALUE](is_null_value.md)
     + [IS\_OBJECT](is_object.md)
     + [IS\_TIME](is_time.md)
     + [IS\_TIMESTAMP\_LTZ](is_timestamp.md)
     + [IS\_TIMESTAMP\_NTZ](is_timestamp.md)
     + [IS\_TIMESTAMP\_TZ](is_timestamp.md)
     + [TYPEOF](typeof.md)
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

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)[Semi-structured and structured data](../functions-semistructured.md)ARRAY\_AGG

Categories:
:   [Aggregate functions](../functions-aggregation) (Semi-structured Data) , [Window functions](../functions-window) (General) , [Semi-structured and structured data functions](../functions-semistructured) (Array/Object)

# ARRAY\_AGG[¶](#array-agg "Link to this heading")

Returns the input values, pivoted into an array. If the input is empty, the function returns an empty array.

Aliases:
:   ARRAYAGG

## Syntax[¶](#syntax "Link to this heading")

**Aggregate function**

```
ARRAY_AGG( [ DISTINCT ] <expr1> ) [ WITHIN GROUP ( <orderby_clause> ) ]
```

Copy

**Window function**

```
ARRAY_AGG( [ DISTINCT ] <expr1> )
  [ WITHIN GROUP ( <orderby_clause> ) ]
  OVER ( [ PARTITION BY <expr2> ] [ ORDER BY <expr3> [ { ASC | DESC } ] [ NULLS { FIRST | LAST } ] ] [ <window_frame> ] )
```

Copy

## Arguments[¶](#arguments "Link to this heading")

**Required:**

`expr1`
:   An expression (typically a column name) that determines the values to be put into the array.

`OVER()`
:   The OVER clause specifies that the function is being used as a window function.
    For details, see [Window function syntax and usage](../functions-window-syntax).

**Optional:**

`DISTINCT`
:   Removes duplicate values from the array.

`WITHIN GROUP orderby_clause`
:   Clause that contains one or more expressions (typically column names) that determine the order of the values in each array.

    The WITHIN GROUP(ORDER BY) syntax supports the same parameters as the main ORDER BY clause in a SELECT statement.
    See [ORDER BY](../constructs/order-by).

`PARTITION BY expr2`
:   Window function clause that specifies an expression (typically a column name).
    This expression defines partitions that group the input rows before the function is applied.
    For details, see [Window function syntax and usage](../functions-window-syntax).

`ORDER BY expr3` [ { ASC | DESC } ] [ NULLS { FIRST | LAST } ] [ `{window_frame}` ]
:   Optional expression to order by within each partition, followed by an optional window frame. For detailed
    `window_frame` syntax, see [Window function syntax and usage](../functions-window-syntax).

    When this function is used with a range-based frame, the ORDER BY clause supports only a single column.
    Row-based frames do not have this restriction.

LIMIT is not supported.

## Returns[¶](#returns "Link to this heading")

Returns a value of type ARRAY.

The maximum amount of data that ARRAY\_AGG can return for a single call is 128 MB.

## Usage notes[¶](#usage-notes "Link to this heading")

* If you do not specify WITHIN GROUP(ORDER BY), the order of
  elements within each array is unpredictable. (An ORDER BY clause outside
  the WITHIN GROUP clause applies to the order of the output rows, not to
  the order of the array elements within a row.)
* If you specify a number for an expression in WITHIN GROUP(ORDER BY), this number is parsed as a numeric
  constant, not as the ordinal position of a column in the SELECT list. Therefore, do not specify
  numbers as WITHIN GROUP(ORDER BY) expressions.
* If you specify DISTINCT and WITHIN GROUP, both must refer to the same column. For example:

  ```
  SELECT ARRAY_AGG(DISTINCT O_ORDERKEY) WITHIN GROUP (ORDER BY O_ORDERKEY) ...;
  ```

  Copy

  If you specify different columns for DISTINCT and WITHIN GROUP, an error occurs:

  ```
  SELECT ARRAY_AGG(DISTINCT O_ORDERKEY) WITHIN GROUP (ORDER BY O_ORDERSTATUS) ...;
  ```

  Copy

  ```
  SQL compilation error: [ORDERS.O_ORDERSTATUS] is not a valid order by expression
  ```

  You must either specify the same column for DISTINCT and WITHIN GROUP or omit DISTINCT.
* DISTINCT and WITHIN GROUP are supported for window function calls only when there is no ORDER BY clause
  within the OVER clause. When an ORDER BY clause is used in the OVER clause, values in the output array
  follow the same default order (that is, the order equivalent to `WITHIN GROUP (ORDER BY expr3)`).
* NULL values are omitted from the output.

## Examples[¶](#examples "Link to this heading")

The example queries below use the tables and data shown below:

> ```
> CREATE TABLE orders (
>     o_orderkey INTEGER,         -- unique ID for each order.
>     o_clerk VARCHAR,            -- identifies which clerk is responsible.
>     o_totalprice NUMBER(12, 2), -- total price.
>     o_orderstatus CHAR(1)       -- 'F' = Fulfilled (sent); 
>                                 -- 'O' = 'Ordered but not yet Fulfilled'.
>     );
>
> INSERT INTO orders (o_orderkey, o_orderstatus, o_clerk, o_totalprice) 
>   VALUES 
>     ( 32123, 'O', 'Clerk#000000321',     321.23),
>     ( 41445, 'F', 'Clerk#000000386', 1041445.00),
>     ( 55937, 'O', 'Clerk#000000114', 1055937.00),
>     ( 67781, 'F', 'Clerk#000000521', 1067781.00),
>     ( 80550, 'O', 'Clerk#000000411', 1080550.00),
>     ( 95808, 'F', 'Clerk#000000136', 1095808.00),
>     (101700, 'O', 'Clerk#000000220', 1101700.00),
>     (103136, 'F', 'Clerk#000000508', 1103136.00);
> ```
>
> Copy

This example shows non-pivoted output from a query that does not use ARRAY\_AGG().
The contrast in output between this example and the following example
shows that ARRAY\_AGG() pivots the data.

> ```
> SELECT O_ORDERKEY AS order_keys
>   FROM orders
>   WHERE O_TOTALPRICE > 450000
>   ORDER BY O_ORDERKEY;
> +------------+
> | ORDER_KEYS |
> |------------|
> |      41445 |
> |      55937 |
> |      67781 |
> |      80550 |
> |      95808 |
> |     101700 |
> |     103136 |
> +------------+
> ```
>
> Copy

This example shows how to use ARRAY\_AGG() to pivot a column of output
into an array in a single row:

> ```
> SELECT ARRAY_AGG(O_ORDERKEY) WITHIN GROUP (ORDER BY O_ORDERKEY ASC)
>   FROM orders 
>   WHERE O_TOTALPRICE > 450000;
> +--------------------------------------------------------------+
> | ARRAY_AGG(O_ORDERKEY) WITHIN GROUP (ORDER BY O_ORDERKEY ASC) |
> |--------------------------------------------------------------|
> | [                                                            |
> |   41445,                                                     |
> |   55937,                                                     |
> |   67781,                                                     |
> |   80550,                                                     |
> |   95808,                                                     |
> |   101700,                                                    |
> |   103136                                                     |
> | ]                                                            |
> +--------------------------------------------------------------+
> ```
>
> Copy

This example shows the use of the DISTINCT keyword with ARRAY\_AGG().

> ```
> SELECT ARRAY_AGG(DISTINCT O_ORDERSTATUS) WITHIN GROUP (ORDER BY O_ORDERSTATUS ASC)
>   FROM orders 
>   WHERE O_TOTALPRICE > 450000
>   ORDER BY O_ORDERSTATUS ASC;
> +-----------------------------------------------------------------------------+
> | ARRAY_AGG(DISTINCT O_ORDERSTATUS) WITHIN GROUP (ORDER BY O_ORDERSTATUS ASC) |
> |-----------------------------------------------------------------------------|
> | [                                                                           |
> |   "F",                                                                      |
> |   "O"                                                                       |
> | ]                                                                           |
> +-----------------------------------------------------------------------------+
> ```
>
> Copy

This example uses two separate ORDER BY clauses. One controls
the order within the output array inside each row, and the other controls
the order of the output rows:

> ```
> SELECT 
>     O_ORDERSTATUS, 
>     ARRAYAGG(O_CLERK) WITHIN GROUP (ORDER BY O_TOTALPRICE DESC)
>   FROM orders 
>   WHERE O_TOTALPRICE > 450000
>   GROUP BY O_ORDERSTATUS
>   ORDER BY O_ORDERSTATUS DESC;
> +---------------+-------------------------------------------------------------+
> | O_ORDERSTATUS | ARRAYAGG(O_CLERK) WITHIN GROUP (ORDER BY O_TOTALPRICE DESC) |
> |---------------+-------------------------------------------------------------|
> | O             | [                                                           |
> |               |   "Clerk#000000220",                                        |
> |               |   "Clerk#000000411",                                        |
> |               |   "Clerk#000000114"                                         |
> |               | ]                                                           |
> | F             | [                                                           |
> |               |   "Clerk#000000508",                                        |
> |               |   "Clerk#000000136",                                        |
> |               |   "Clerk#000000521",                                        |
> |               |   "Clerk#000000386"                                         |
> |               | ]                                                           |
> +---------------+-------------------------------------------------------------+
> ```
>
> Copy

The following example uses a different data set. The ARRAY\_AGG function is called as a window
function with a ROWS BETWEEN window frame. First, create the table and load it with 14 rows:

```
CREATE OR REPLACE TABLE array_data AS (
WITH data AS (
  SELECT 1 a, [1,3,2,4,7,8,10] b
  UNION ALL
  SELECT 2, [1,3,2,4,7,8,10]
  )
SELECT 'Ord'||a o_orderkey, 'c'||value o_clerk, index
  FROM data, TABLE(FLATTEN(b))
);
```

Copy

Now run the following query. Note that only a partial result set is shown here.

```
SELECT o_orderkey,
    ARRAY_AGG(o_clerk) OVER(PARTITION BY o_orderkey ORDER BY o_orderkey
      ROWS BETWEEN 3 PRECEDING AND CURRENT ROW) AS result
  FROM array_data;
```

Copy

```
+------------+---------+
| O_ORDERKEY | RESULT  |
|------------+---------|
| Ord1       | [       |
|            |   "c1"  |
|            | ]       |
| Ord1       | [       |
|            |   "c1", |
|            |   "c3"  |
|            | ]       |
| Ord1       | [       |
|            |   "c1", |
|            |   "c3", |
|            |   "c2"  |
|            | ]       |
| Ord1       | [       |
|            |   "c1", |
|            |   "c3", |
|            |   "c2", |
|            |   "c4"  |
|            | ]       |
| Ord1       | [       |
|            |   "c3", |
|            |   "c2", |
|            |   "c4", |
|            |   "c7"  |
|            | ]       |
| Ord1       | [       |
|            |   "c2", |
|            |   "c4", |
|            |   "c7", |
|            |   "c8"  |
|            | ]       |
| Ord1       | [       |
|            |   "c4", |
|            |   "c7", |
|            |   "c8", |
|            |   "c10" |
|            | ]       |
| Ord2       | [       |
|            |   "c1"  |
|            | ]       |
| Ord2       | [       |
|            |   "c1", |
|            |   "c3"  |
|            | ]       |
...
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