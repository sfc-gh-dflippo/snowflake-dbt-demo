---
auto_generated: true
description: Semi-structured and structured data functions (Array/Object)
last_scraped: '2026-01-14T16:56:11.649347+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/array_cat
title: ARRAY_CAT | Snowflake Documentation
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

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)[Semi-structured and structured data](../functions-semistructured.md)ARRAY\_CAT

Categories:
:   [Semi-structured and structured data functions](../functions-semistructured) (Array/Object)

# ARRAY\_CAT[¶](#array-cat "Link to this heading")

Returns a concatenation of two arrays.

## Syntax[¶](#syntax "Link to this heading")

```
ARRAY_CAT( <array1> , <array2> )
```

Copy

## Arguments[¶](#arguments "Link to this heading")

`array1`
:   The source array.

`array2`
:   The array to be appended to `array1`.

## Returns[¶](#returns "Link to this heading")

An ARRAY containing the elements from `array2` appended after the elements of `array1`.

## Usage notes[¶](#usage-notes "Link to this heading")

* Both arguments must either be [structured ARRAYs](../data-types-structured) or
  [semi-structured ARRAYs](../data-types-semistructured.html#label-data-type-array).

* If you are passing in semi-structured ARRAYs, both arguments must be of ARRAY type or VARIANT containing an array.
* If you are passing in structured ARRAYs, the function returns an ARRAY of a type that can accommodate both input types.
* If either argument is NULL, the function returns NULL without reporting any error.

## Examples[¶](#examples "Link to this heading")

This example shows how to use `ARRAY_CAT()`:

> Create a simple table and data:
>
> > ```
> > CREATE TABLE array_demo (ID INTEGER, array1 ARRAY, array2 ARRAY);
> > ```
> >
> > Copy
> >
> > ```
> > INSERT INTO array_demo (ID, array1, array2) 
> >     SELECT 1, ARRAY_CONSTRUCT(1, 2), ARRAY_CONSTRUCT(3, 4);
> > ```
> >
> > Copy
>
> Execute the query:
>
> > ```
> > SELECT ARRAY_CAT(array1, array2) FROM array_demo;
> > +---------------------------+
> > | ARRAY_CAT(ARRAY1, ARRAY2) |
> > |---------------------------|
> > | [                         |
> > |   1,                      |
> > |   2,                      |
> > |   3,                      |
> > |   4                       |
> > | ]                         |
> > +---------------------------+
> > ```
> >
> > Copy

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