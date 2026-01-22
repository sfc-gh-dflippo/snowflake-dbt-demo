---
auto_generated: true
description: Semi-structured and structured data functions (Parsing)
last_scraped: '2026-01-14T16:57:08.044228+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/parse_json.html
title: PARSE_JSON | Snowflake Documentation
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

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)[Semi-structured and structured data](../functions-semistructured.md)PARSE\_JSON

Categories:
:   [Semi-structured and structured data functions](../functions-semistructured) (Parsing)

# PARSE\_JSON[¶](#parse-json "Link to this heading")

Interprets an input string as a JSON document, producing a [VARIANT](../data-types-semistructured.html#label-data-type-variant) value.

You can use the PARSE\_JSON function when you have input data in JSON format. This function can convert
data from JSON format to [ARRAY](../data-types-semistructured.html#label-data-type-array) or [OBJECT](../data-types-semistructured.html#label-data-type-object) data and store that
data directly in a VARIANT value. You can then analyze or manipulate the data.

By default, the function doesn’t allow duplicate keys in the JSON object, but you can set the
`'parameter'` argument to allow duplicate keys.

See also:
:   [TRY\_PARSE\_JSON](try_parse_json)

## Syntax[¶](#syntax "Link to this heading")

```
PARSE_JSON( <expr> [ , '<parameter>' ] )
```

Copy

## Arguments[¶](#arguments "Link to this heading")

**Required:**

`expr`
:   An expression of string type (for example, VARCHAR) that holds valid JSON information.

**Optional:**

`'parameter'`
:   String constant that specifies the parameter used to search for matches. Supported values:

    | Parameter | Description |
    | --- | --- |
    | `d` | Allow duplicate keys in JSON objects. If a JSON object contains a duplicate key, the returned object has a single instance of that key with the last value specified for that key. |
    | `s` | Don’t allow duplicate keys in JSON objects (strict). This value is the default. |

## Returns[¶](#returns "Link to this heading")

Returns a value of type VARIANT that contains a JSON document.

If the input is NULL, the function returns NULL.

This function doesn’t return a [structured type](../data-types-structured).

## Usage notes[¶](#usage-notes "Link to this heading")

* This function supports an input expression with a maximum size of 64 MB compressed.
* If the PARSE\_JSON function is called with an empty string, or with a string containing only whitespace characters, then
  the function returns NULL (rather than raising an error), even though an empty string isn’t valid JSON. This behavior allows
  processing to continue rather than aborting if some inputs are empty strings.
* If the input is NULL, the output is also NULL. However, if the input string is `'null'`, then it is interpreted as a
  [JSON null](../../user-guide/semistructured-considerations.html#label-variant-null) value so that the result isn’t SQL NULL, but instead a valid VARIANT value containing `null`.
  See the example below.
* When parsing decimal numbers, PARSE\_JSON attempts to preserve the exactness of the representation by treating 123.45 as NUMBER(5,2),
  not as a DOUBLE value. However, numbers that use scientific notation (for example, 1.2345e+02), or numbers that cannot be stored as fixed-point
  decimals due to range or scale limitations, are stored as DOUBLE values. Because JSON does not represent values such as TIMESTAMP, DATE,
  TIME, or BINARY natively, these values must be represented as strings.
* In JSON, an object (also called a “dictionary” or a “hash”) is an unordered set of
  key-value pairs.

* TO\_JSON and PARSE\_JSON are (almost) converse or reciprocal functions.

  + The PARSE\_JSON function takes a string as input and returns a JSON-compatible [VARIANT](../data-types-semistructured.html#label-data-type-variant).
  + The TO\_JSON function takes a JSON-compatible VARIANT and returns a string.

  The following is (conceptually) true if X is a string containing valid JSON:

  > `X = TO_JSON(PARSE_JSON(X));`

  For example, the following is (conceptually) true:

  > `'{"pi":3.14,"e":2.71}' = TO_JSON(PARSE_JSON('{"pi":3.14,"e":2.71}'))`

  However, the functions are not perfectly reciprocal because:

  + Empty strings, and strings with only whitespace, are not handled reciprocally. For example, the return value of
    `PARSE_JSON('')` is NULL, but the return value of `TO_JSON(NULL)` is NULL, not the reciprocal `''`.
  + The order of the key-value pairs in the string produced by TO\_JSON is not predictable.
  + The string produced by TO\_JSON can have less whitespace than the string passed to PARSE\_JSON.

  For example, the following are equivalent JSON, but not equivalent strings:

  + `{"pi": 3.14, "e": 2.71}`
  + `{"e":2.71,"pi":3.14}`

## Examples[¶](#examples "Link to this heading")

The following examples use the PARSE\_JSON function.

### Storing values of different data types in a VARIANT column[¶](#storing-values-of-different-data-types-in-a-variant-column "Link to this heading")

This example stores different types of data in a VARIANT column by calling PARSE\_JSON to parse strings.

Create and fill a table. The INSERT statement uses PARSE\_JSON to insert VARIANT values in the `v` column
of the table.

```
CREATE OR REPLACE TABLE vartab (n NUMBER(2), v VARIANT);

INSERT INTO vartab
  SELECT column1 AS n, PARSE_JSON(column2) AS v
    FROM VALUES (1, 'null'), 
                (2, null), 
                (3, 'true'),
                (4, '-17'), 
                (5, '123.12'), 
                (6, '1.912e2'),
                (7, '"Om ara pa ca na dhih"  '), 
                (8, '[-1, 12, 289, 2188, false,]'), 
                (9, '{ "x" : "abc", "y" : false, "z": 10} ') 
       AS vals;
```

Copy

Query the data. The query uses the [TYPEOF](typeof) function to show the data types of
the values stored in the VARIANT values.

```
SELECT n, v, TYPEOF(v)
  FROM vartab
  ORDER BY n;
```

Copy

```
+---+------------------------+------------+
| N | V                      | TYPEOF(V)  |
|---+------------------------+------------|
| 1 | null                   | NULL_VALUE |
| 2 | NULL                   | NULL       |
| 3 | true                   | BOOLEAN    |
| 4 | -17                    | INTEGER    |
| 5 | 123.12                 | DECIMAL    |
| 6 | 1.912000000000000e+02  | DOUBLE     |
| 7 | "Om ara pa ca na dhih" | VARCHAR    |
| 8 | [                      | ARRAY      |
|   |   -1,                  |            |
|   |   12,                  |            |
|   |   289,                 |            |
|   |   2188,                |            |
|   |   false,               |            |
|   |   undefined            |            |
|   | ]                      |            |
| 9 | {                      | OBJECT     |
|   |   "x": "abc",          |            |
|   |   "y": false,          |            |
|   |   "z": 10              |            |
|   | }                      |            |
+---+------------------------+------------+
```

### Insert a JSON object with duplicate keys in a VARIANT value[¶](#insert-a-json-object-with-duplicate-keys-in-a-variant-value "Link to this heading")

Try to insert a JSON object with duplicate keys in a VARIANT value:

```
INSERT INTO vartab
SELECT column1 AS n, PARSE_JSON(column2) AS v
  FROM VALUES (10, '{ "a" : "123", "b" : "456", "a": "789"} ')
     AS vals;
```

Copy

An error is returned because duplicate keys aren’t allowed by default:

```
100069 (22P02): Error parsing JSON: duplicate object attribute "a", pos 31
```

Insert a JSON object with duplicate keys in a VARIANT value, and specify the `d` parameter to allow
duplicates:

```
INSERT INTO vartab
SELECT column1 AS n, PARSE_JSON(column2, 'd') AS v
  FROM VALUES (10, '{ "a" : "123", "b" : "456", "a": "789"} ')
     AS vals;
```

Copy

```
+-------------------------+
| number of rows inserted |
|-------------------------|
|                       1 |
+-------------------------+
```

A query on the table shows that only the value of the last duplicate key was inserted:

```
SELECT v
  FROM vartab
  WHERE n = 10;
```

Copy

```
+---------------+
| V             |
|---------------|
| {             |
|   "a": "789", |
|   "b": "456"  |
| }             |
+---------------+
```

### Handling NULL values with the PARSE\_JSON and TO\_JSON functions[¶](#handling-null-values-with-the-parse-json-and-to-json-functions "Link to this heading")

The following example shows how PARSE\_JSON and TO\_JSON handle NULL values:

```
SELECT TO_JSON(NULL), TO_JSON('null'::VARIANT),
       PARSE_JSON(NULL), PARSE_JSON('null');
```

Copy

```
+---------------+--------------------------+------------------+--------------------+
| TO_JSON(NULL) | TO_JSON('NULL'::VARIANT) | PARSE_JSON(NULL) | PARSE_JSON('NULL') |
|---------------+--------------------------+------------------+--------------------|
| NULL          | "null"                   | NULL             | null               |
+---------------+--------------------------+------------------+--------------------+
```

### Comparing PARSE\_JSON and TO\_JSON[¶](#comparing-parse-json-and-to-json "Link to this heading")

The following examples demonstrate the relationship between the PARSE\_JSON and TO\_JSON functions.

This example creates a table with a VARCHAR column and a VARIANT column. The INSERT statement inserts
a VARCHAR value, and the UPDATE statement generates a JSON value that corresponds with that VARCHAR value.

```
CREATE OR REPLACE TABLE jdemo2 (
  varchar1 VARCHAR, 
  variant1 VARIANT);

INSERT INTO jdemo2 (varchar1) VALUES ('{"PI":3.14}');

UPDATE jdemo2 SET variant1 = PARSE_JSON(varchar1);
```

Copy

This query shows that TO\_JSON and PARSE\_JSON are conceptually reciprocal functions:

```
SELECT varchar1, 
       PARSE_JSON(varchar1), 
       variant1, 
       TO_JSON(variant1),
       PARSE_JSON(varchar1) = variant1, 
       TO_JSON(variant1) = varchar1
  FROM jdemo2;
```

Copy

```
+-------------+----------------------+--------------+-------------------+---------------------------------+------------------------------+
| VARCHAR1    | PARSE_JSON(VARCHAR1) | VARIANT1     | TO_JSON(VARIANT1) | PARSE_JSON(VARCHAR1) = VARIANT1 | TO_JSON(VARIANT1) = VARCHAR1 |
|-------------+----------------------+--------------+-------------------+---------------------------------+------------------------------|
| {"PI":3.14} | {                    | {            | {"PI":3.14}       | True                            | True                         |
|             |   "PI": 3.14         |   "PI": 3.14 |                   |                                 |                              |
|             | }                    | }            |                   |                                 |                              |
+-------------+----------------------+--------------+-------------------+---------------------------------+------------------------------+
```

However, the functions are not exactly reciprocal. Differences in whitespace or in the order of key-value
pairs can prevent the output from matching the input. For example:

```
SELECT TO_JSON(PARSE_JSON('{"b":1,"a":2}')),
       TO_JSON(PARSE_JSON('{"b":1,"a":2}')) = '{"b":1,"a":2}',
       TO_JSON(PARSE_JSON('{"b":1,"a":2}')) = '{"a":2,"b":1}';
```

Copy

```
+--------------------------------------+--------------------------------------------------------+--------------------------------------------------------+
| TO_JSON(PARSE_JSON('{"B":1,"A":2}')) | TO_JSON(PARSE_JSON('{"B":1,"A":2}')) = '{"B":1,"A":2}' | TO_JSON(PARSE_JSON('{"B":1,"A":2}')) = '{"A":2,"B":1}' |
|--------------------------------------+--------------------------------------------------------+--------------------------------------------------------|
| {"a":2,"b":1}                        | False                                                  | True                                                   |
+--------------------------------------+--------------------------------------------------------+--------------------------------------------------------+
```

### Comparing PARSE\_JSON and TO\_VARIANT[¶](#comparing-parse-json-and-to-variant "Link to this heading")

Although both the PARSE\_JSON function and the [TO\_VARIANT](to_variant) function can take a string and return
a VARIANT value, they are not equivalent. The following example creates a table with two VARIANT
columns. Then, it uses PARSE\_JSON to insert a value into one column and TO\_VARIANT to
insert a value into the other column.

```
CREATE OR REPLACE TABLE jdemo3 (
  variant1 VARIANT,
  variant2 VARIANT);

INSERT INTO jdemo3 (variant1, variant2)
  SELECT
    PARSE_JSON('{"PI":3.14}'),
    TO_VARIANT('{"PI":3.14}');
```

Copy

The query below shows that the functions returned VARIANT values that
store values of different data types.

```
SELECT variant1,
       TYPEOF(variant1),
       variant2,
       TYPEOF(variant2),
       variant1 = variant2
  FROM jdemo3;
```

Copy

```
+--------------+------------------+-----------------+------------------+---------------------+
| VARIANT1     | TYPEOF(VARIANT1) | VARIANT2        | TYPEOF(VARIANT2) | VARIANT1 = VARIANT2 |
|--------------+------------------+-----------------+------------------+---------------------|
| {            | OBJECT           | "{\"PI\":3.14}" | VARCHAR          | False               |
|   "PI": 3.14 |                  |                 |                  |                     |
| }            |                  |                 |                  |                     |
+--------------+------------------+-----------------+------------------+---------------------+
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