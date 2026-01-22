---
auto_generated: true
description: Semi-structured and structured data functions (Array/Object)
last_scraped: '2026-01-14T16:56:57.627251+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/array_slice
title: ARRAY_SLICE | Snowflake Documentation
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

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)[Semi-structured and structured data](../functions-semistructured.md)ARRAY\_SLICE

Categories:
:   [Semi-structured and structured data functions](../functions-semistructured) (Array/Object)

# ARRAY\_SLICE[¶](#array-slice "Link to this heading")

Returns an array constructed from a specified subset of elements of the input array.

## Syntax[¶](#syntax "Link to this heading")

```
ARRAY_SLICE( <array> , <from> , <to> )
```

Copy

## Arguments[¶](#arguments "Link to this heading")

`array`
:   The source array of which a subset of the elements are used to construct the resulting array.

`from`
:   A position in the source array. The position of the first element is `0`. Elements from positions less than `from`
    aren’t included in the resulting array.

`to`
:   A position in the source array. Elements from positions equal to or greater than `to` are not included in
    the resulting array.

## Returns[¶](#returns "Link to this heading")

This function returns a value of type ARRAY.

Returns NULL if the any argument is NULL, including the input `array`, `from`, or `to`.

## Usage notes[¶](#usage-notes "Link to this heading")

* The output includes elements up to, but not including the element
  specified by the parameter `to`.
* If either `from` or `to` is negative, it is relative to
  the end of the array, not the beginning of the array. For example, `-2` refers
  to the second-from-the-last position in the array.
* If `from` and `to` are both beyond the upper end of the
  array, or are both beyond the lower end of the array, then the result is
  the empty set.
* When you pass a [structured array](../data-types-structured) to the function, the function returns a structured
  array of the same type.

Note that many of these rules (for example, interpretation of negative numbers as
indexes from the end of the array, and the rule that the slice is up to, but
not including, the `to` index), are similar to the rules for array
slices in programming languages such as Python.

Each of these rules is illustrated in at least one example below.

## Examples[¶](#examples "Link to this heading")

These examples use [ARRAY constants](../data-types-semistructured.html#label-array-constant) to construct arrays. Alternatively, you can
use the [ARRAY\_CONSTRUCT](array_construct) function to construct arrays.

This example shows a simple array slice:

```
SELECT ARRAY_SLICE([0,1,2,3,4,5,6], 0, 2);
```

Copy

```
+------------------------------------+
| ARRAY_SLICE([0,1,2,3,4,5,6], 0, 2) |
|------------------------------------|
| [                                  |
|   0,                               |
|   1                                |
| ]                                  |
+------------------------------------+
```

This example slices an array to the last index by using the [ARRAY\_SIZE](array_size) function with the
ARRAY\_SLICE function:

```
SELECT ARRAY_SLICE([0,1,2,3,4,5,6], 3, ARRAY_SIZE([0,1,2,3,4,5,6])) AS slice_to_last_index;
```

Copy

```
+---------------------+
| SLICE_TO_LAST_INDEX |
|---------------------|
| [                   |
|   3,                |
|   4,                |
|   5,                |
|   6                 |
| ]                   |
+---------------------+
```

Although the indexes must be numeric, the elements of the array don’t need
to be numeric:

```
SELECT ARRAY_SLICE(['foo','snow','flake','bar'], 1, 3);
```

Copy

```
+-------------------------------------------------+
| ARRAY_SLICE(['FOO','SNOW','FLAKE','BAR'], 1, 3) |
|-------------------------------------------------|
| [                                               |
|   "snow",                                       |
|   "flake"                                       |
| ]                                               |
+-------------------------------------------------+
```

This example shows the effect of using NULL as the input array:

```
SELECT ARRAY_SLICE(NULL, 2, 3);
```

Copy

```
+-------------------------+
| ARRAY_SLICE(NULL, 2, 3) |
|-------------------------|
| NULL                    |
+-------------------------+
```

This example shows the effect of using NULL as one of the slice indexes:

```
SELECT ARRAY_SLICE([0,1,2,3,4,5,6], NULL, 2);
```

Copy

```
+---------------------------------------+
| ARRAY_SLICE([0,1,2,3,4,5,6], NULL, 2) |
|---------------------------------------|
| NULL                                  |
+---------------------------------------+
```

This example shows the effect of using a negative number as an index. The number
is interpreted as the offset from the end of the array:

```
SELECT ARRAY_SLICE([0,1,2,3,4,5,6], 0, -2);
```

Copy

```
+-------------------------------------+
| ARRAY_SLICE([0,1,2,3,4,5,6], 0, -2) |
|-------------------------------------|
| [                                   |
|   0,                                |
|   1,                                |
|   2,                                |
|   3,                                |
|   4                                 |
| ]                                   |
+-------------------------------------+
```

This example shows that both indexes can be negative (that is, both can be relative to the end of
the array):

```
SELECT ARRAY_SLICE([0,1,2,3,4,5,6], -5, -3);
```

Copy

```
+--------------------------------------+
| ARRAY_SLICE([0,1,2,3,4,5,6], -5, -3) |
|--------------------------------------|
| [                                    |
|   2,                                 |
|   3                                  |
| ]                                    |
+--------------------------------------+
```

In this example, both indexes are beyond the end of the array:

```
SELECT ARRAY_SLICE([0,1,2,3,4,5,6], 10, 12);
```

Copy

```
+--------------------------------------+
| ARRAY_SLICE([0,1,2,3,4,5,6], 10, 12) |
|--------------------------------------|
| []                                   |
+--------------------------------------+
```

In this example, both indexes are before the start of the array:

```
SELECT ARRAY_SLICE([0,1,2,3,4,5,6], -10, -12);
```

Copy

```
+----------------------------------------+
| ARRAY_SLICE([0,1,2,3,4,5,6], -10, -12) |
|----------------------------------------|
| []                                     |
+----------------------------------------+
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