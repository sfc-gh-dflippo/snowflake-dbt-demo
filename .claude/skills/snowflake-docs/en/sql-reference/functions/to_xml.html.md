---
auto_generated: true
description: Conversion functions , Semi-structured and structured data functions
  (Cast)
last_scraped: '2026-01-14T16:56:24.530622+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/to_xml.html
title: TO_XML | Snowflake Documentation
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

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)[Semi-structured and structured data](../functions-semistructured.md)TO\_XML

Categories:
:   [Conversion functions](../functions-conversion) , [Semi-structured and structured data functions](../functions-semistructured) (Cast)

# TO\_XML[¶](#to-xml "Link to this heading")

Converts a [VARIANT](../data-types-semistructured.html#label-data-type-variant) to a VARCHAR that contains an [XML](../../user-guide/semistructured-data-formats.html#label-xml-format) representation
of the value. If the input is NULL, the result is also NULL.

See also:
:   [CHECK\_XML](check_xml), [PARSE\_XML](parse_xml), [XMLGET](xmlget)

## Syntax[¶](#syntax "Link to this heading")

```
TO_XML( <expression> )
```

Copy

## Arguments[¶](#arguments "Link to this heading")

`expression`
:   An expression that evaluates to a VARIANT or that can be [cast](../data-type-conversion) to a VARIANT.

## Returns[¶](#returns "Link to this heading")

The data type of the returned value is VARCHAR.

## Usage notes[¶](#usage-notes "Link to this heading")

* Common uses for this function include:

  + Generating a string that contains an XML-formatted value that matches an originally inserted XML-formatted value.
  + Converting a semi-structured value (which doesn’t necessarily need to have been formatted as XML originally) into an
    XML-formatted value. For example, you can use TO\_XML to generate an XML-compatible representation of a value that was
    originally formatted as JSON.
* If the input `expression` doesn’t evaluate to a VARIANT, Snowflake implicitly
  [casts](../data-type-conversion) the result of the expression to a VARIANT. Because all other Snowflake data types
  can be cast to VARIANT, this means that a value of any data type can be passed to TO\_XML and converted to an XML-formatted string.
  (The [GEOGRAPHY](../data-types-geospatial) data type is a partial exception; to call TO\_XML with a value of
  type GEOGRAPHY, you must explicitly cast the GEOGRAPHY value to VARIANT.)
* If the value didn’t originate as XML, then Snowflake generates XML-compatible tags. These tags may use the `type` attribute to
  specify the Snowflake data type of the tag’s contents. Below are examples of tags generated by Snowflake.

  The outermost tag pair is similar to the following:

  ```
  <SnowflakeData type="OBJECT"> </SnowflakeData>
  ```

  Copy

  The data type specified in the `type` attribute of the tag can vary.

  For an OBJECT, each key-value pair’s tags are based on the key. For example:

  ```
  <key1 type="VARCHAR">value1</key1>
  ```

  Copy

  For an ARRAY, each element of the array is in a tag pair similar to:

  ```
  <e type="VARCHAR"> </e>
  ```

  Copy

  Here is a complete example of the XML for a simple OBJECT that contains two key-value pairs:

  ```
  <SnowflakeData type="OBJECT">
      <key1 type="VARCHAR">value1</key1>
      <key2 type="VARCHAR">value2</key2>
  </SnowflakeData>
  ```

  Copy

  Here is a complete example of the XML for a simple ARRAY that contains two VARCHAR values:

  ```
  <SnowflakeData type="ARRAY">
      <e type="VARCHAR">v1</e>
      <e type="VARCHAR">v2</e>
  </SnowflakeData>
  ```

  Copy

## Examples[¶](#examples "Link to this heading")

This example shows how to use the function if you’ve loaded XML-formatted data into an OBJECT by calling
[PARSE\_XML](parse_xml).

Create a table and insert data:

```
CREATE OR REPLACE TABLE xml_02 (x OBJECT);

INSERT INTO xml_02 (x)
  SELECT PARSE_XML('<note> <body>Sample XML</body> </note>');
```

Copy

Call the TO\_XML and TO\_VARCHAR functions:

```
SELECT x, TO_VARCHAR(x), TO_XML(x) FROM xml_02;
```

Copy

```
+---------------------------+--------------------------------------+--------------------------------------+
| X                         | TO_VARCHAR(X)                        | TO_XML(X)                            |
|---------------------------+--------------------------------------+--------------------------------------|
| <note>                    | <note><body>Sample XML</body></note> | <note><body>Sample XML</body></note> |
|   <body>Sample XML</body> |                                      |                                      |
| </note>                   |                                      |                                      |
+---------------------------+--------------------------------------+--------------------------------------+
```

You can also call the TO\_XML function with data that did not originate as XML-formatted data, as shown in the examples below.

The following example creates a simple OBJECT and then generates the corresponding XML. The XML output contains information about the
data types of the values in the key-value pairs, as well as the data type of the overall value (OBJECT).

```
CREATE OR REPLACE TABLE xml_03 (object_col_1 OBJECT);

INSERT INTO xml_03 (object_col_1)
  SELECT OBJECT_CONSTRUCT('key1', 'value1', 'key2', 'value2');
```

Copy

```
SELECT object_col_1, TO_XML(object_col_1)
  FROM xml_03;
```

Copy

```
+---------------------+-------------------------------------------------------------------------------------------------------------------+
| OBJECT_COL_1        | TO_XML(OBJECT_COL_1)                                                                                              |
|---------------------+-------------------------------------------------------------------------------------------------------------------|
| {                   | <SnowflakeData type="OBJECT"><key1 type="VARCHAR">value1</key1><key2 type="VARCHAR">value2</key2></SnowflakeData> |
|   "key1": "value1", |                                                                                                                   |
|   "key2": "value2"  |                                                                                                                   |
| }                   |                                                                                                                   |
+---------------------+-------------------------------------------------------------------------------------------------------------------+
```

The following example creates a simple ARRAY and then generates the corresponding XML. The XML output contains information about the
data types of the array elements, as well as the data type of the overall value (ARRAY).

```
CREATE OR REPLACE TABLE xml_04 (array_col_1 ARRAY);

INSERT INTO xml_04 (array_col_1)
  SELECT ARRAY_CONSTRUCT('v1', 'v2');
```

Copy

```
SELECT array_col_1, TO_XML(array_col_1)
  FROM xml_04;
```

Copy

```
+-------------+----------------------------------------------------------------------------------------------+
| ARRAY_COL_1 | TO_XML(ARRAY_COL_1)                                                                          |
|-------------+----------------------------------------------------------------------------------------------|
| [           | <SnowflakeData type="ARRAY"><e type="VARCHAR">v1</e><e type="VARCHAR">v2</e></SnowflakeData> |
|   "v1",     |                                                                                              |
|   "v2"      |                                                                                              |
| ]           |                                                                                              |
+-------------+----------------------------------------------------------------------------------------------+
```

The following example inserts data that is in JSON format and then generates the corresponding XML.

```
CREATE OR REPLACE TABLE xml_05 (json_col_1 VARIANT);

INSERT INTO xml_05 (json_col_1)
  SELECT PARSE_JSON(' { "key1": ["a1", "a2"] } ');
```

Copy

```
SELECT json_col_1,
       TO_JSON(json_col_1),
       TO_XML(json_col_1)
  FROM xml_05;
```

Copy

```
+-------------+----------------------+-------------------------------------------------------------------------------------------------------------------------+
| JSON_COL_1  | TO_JSON(JSON_COL_1)  | TO_XML(JSON_COL_1)                                                                                                      |
|-------------+----------------------+-------------------------------------------------------------------------------------------------------------------------|
| {           | {"key1":["a1","a2"]} | <SnowflakeData type="OBJECT"><key1 type="ARRAY"><e type="VARCHAR">a1</e><e type="VARCHAR">a2</e></key1></SnowflakeData> |
|   "key1": [ |                      |                                                                                                                         |
|     "a1",   |                      |                                                                                                                         |
|     "a2"    |                      |                                                                                                                         |
|   ]         |                      |                                                                                                                         |
| }           |                      |                                                                                                                         |
+-------------+----------------------+-------------------------------------------------------------------------------------------------------------------------+
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

Related content

1. [What is XML?](/sql-reference/functions/../../user-guide/semistructured-data-formats#label-what-is-xml)