---
auto_generated: true
description: Conversion functions
last_scraped: '2026-01-14T16:55:50.350316+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/cast.html
title: 'CAST , :: | Snowflake Documentation'
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

     + Any data type
     + [CAST, ::](cast.md)
     + [TRY\_CAST](try_cast.md)
     + Text, character, binary data types
     + [TO\_CHAR](to_char.md)
     + [TO\_VARCHAR](to_char.md)
     + [TO\_BINARY](to_binary.md)
     + [TRY\_TO\_BINARY](try_to_binary.md)
     + Numeric data types
     + [TO\_DECFLOAT](to_decfloat.md)
     + [TO\_DECIMAL](to_decimal.md)
     + [TO\_NUMBER](to_decimal.md)
     + [TO\_NUMERIC](to_decimal.md)
     + [TO\_DOUBLE](to_double.md)
     + [TRY\_TO\_DECFLOAT](try_to_decfloat.md)
     + [TRY\_TO\_DECIMAL](try_to_decimal.md)
     + [TRY\_TO\_NUMBER](try_to_decimal.md)
     + [TRY\_TO\_NUMERIC](try_to_decimal.md)
     + [TRY\_TO\_DOUBLE](try_to_double.md)
     + Boolean data types
     + [TO\_BOOLEAN](to_boolean.md)
     + [TRY\_TO\_BOOLEAN](try_to_boolean.md)
     + Date and time data types
     + [TO\_DATE](to_date.md)
     + [DATE](to_date.md)
     + [TO\_TIME](to_time.md)
     + [TIME](to_time.md)
     + [TO\_TIMESTAMP](to_timestamp.md)
     + [TO\_TIMESTAMP\_LTZ](to_timestamp.md)
     + [TO\_TIMESTAMP\_NTZ](to_timestamp.md)
     + [TO\_TIMESTAMP\_TZ](to_timestamp.md)
     + [TRY\_TO\_DATE](try_to_date.md)
     + [TRY\_TO\_TIME](try_to_time.md)
     + [TRY\_TO\_TIMESTAMP](try_to_timestamp.md)
     + [TRY\_TO\_TIMESTAMP\_LTZ](try_to_timestamp.md)
     + [TRY\_TO\_TIMESTAMP\_NTZ](try_to_timestamp.md)
     + [TRY\_TO\_TIMESTAMP\_TZ](try_to_timestamp.md)
     + Semi-structured data types
     + [TO\_ARRAY](to_array.md)
     + [TO\_OBJECT](to_object.md)
     + [TO\_VARIANT](to_variant.md)
     + Geospatial data types
     + [TO\_GEOGRAPHY](to_geography.md)
     + [TRY\_TO\_GEOGRAPHY](try_to_geography.md)
     + [ST\_GEOGRAPHYFROMWWKB](st_geographyfromwkb.md)
     + [ST\_GEOGRAPHYFROMWKT](st_geographyfromwkt.md)
     + [TO\_GEOMETRY](to_geometry.md)
     + [TRY\_TO\_GEOMETRY](try_to_geometry.md)
     + [ST\_GEOMETRYFROMWKB](st_geometryfromwkb.md)
     + [ST\_GEOMETRYFROMWKT](st_geometryfromwkt.md)
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

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)[Conversion](../functions-conversion.md)CAST, ::

Categories:
:   [Conversion functions](../functions-conversion)

# CAST , `::`[¶](#cast "Link to this heading")

Converts a value of one data type into another data type. The semantics of CAST
are the same as the semantics of the corresponding TO\_ `datatype` conversion
functions. If the cast is not possible, an error is raised. For more details,
see the individual TO\_ `datatype` conversion functions. For more information
about data type conversion and the TO\_ `datatype` conversion
functions, see [Data type conversion](../data-type-conversion).

The `::` operator provides alternative syntax for CAST.

See also:
:   [TRY\_CAST](try_cast)

## Syntax[¶](#syntax "Link to this heading")

```
CAST( <source_expr> AS <target_data_type> )
  [ RENAME FIELDS | ADD FIELDS ]

<source_expr> :: <target_data_type>
```

Copy

## Arguments[¶](#arguments "Link to this heading")

`source_expr`
:   Expression of any supported data type to be converted into a
    different data type.

`target_data_type`
:   The data type to which to convert the expression. If the data
    type supports additional properties, such as
    [precision and scale](../data-types-numeric.html#label-data-types-numeric-precision-and-scale)
    (for numbers/decimals), the properties can be included.

`RENAME FIELDS`
:   For [structured OBJECTs](../data-types-structured), specifies that you want to change the OBJECT to use
    different key-value pairs. The values in the original object are copied to the new key-value pairs in the order in which
    they appear.

    For an example, see [Example: Changing the key names in an OBJECT value](../data-types-structured.html#label-structured-types-casting-struct-struct-object-key-names).

`ADD FIELDS`
:   For [structured OBJECTs](../data-types-structured), specifies that you want to add key-value pairs to the
    OBJECT.

    For an example, see [Example: Adding keys to an OBJECT value](../data-types-structured.html#label-structured-types-casting-struct-struct-object-key-add).

    The values for the newly added keys will be set to NULL. If you want to assign a value to these keys, call the
    [OBJECT\_INSERT](../data-types-structured.html#label-structured-types-transform-object-insert) function instead.

## Usage notes[¶](#usage-notes "Link to this heading")

* If the scale is not sufficient to hold the input value, the function
  rounds the value.
* If the precision is not sufficient to hold the input value, the function
  raises an error.
* When numeric columns are explicitly cast to forms of the integer data type during a data unload to Parquet files, the data type of these
  columns in the Parquet files is INT. For more information, see [Explicitly converting numeric columns to Parquet data types](../../user-guide/data-unload-considerations.html#label-converting-numeric-columns-to-parquet-data-types).
* Collation specifications aren’t retained when values to are cast to
  [text string data types](../data-types-text.html#label-character-datatypes) (for example, VARCHAR and STRING). You can include collation
  specifications when you cast values (for example, `CAST(myvalue AS VARCHAR) COLLATE 'en-ai'`).
* When you use the `::` alternative syntax, you cannot specify the `RENAME FIELDS` or `ADD FIELDS` arguments.

## Examples[¶](#examples "Link to this heading")

The CAST examples use the data in the following table:

```
CREATE OR REPLACE TABLE test_data_type_conversion (
  varchar_value VARCHAR,
  number_value NUMBER(5, 4),
  timestamp_value TIMESTAMP);

INSERT INTO test_data_type_conversion VALUES (
  '9.8765',
  1.2345,
  '2024-05-09 14:32:29.135 -0700');

SELECT * FROM test_data_type_conversion;
```

Copy

```
+---------------+--------------+-------------------------+
| VARCHAR_VALUE | NUMBER_VALUE | TIMESTAMP_VALUE         |
|---------------+--------------+-------------------------|
| 9.8765        |       1.2345 | 2024-05-09 14:32:29.135 |
+---------------+--------------+-------------------------+
```

The examples use the [SYSTEM$TYPEOF](system_typeof) function to show the data type of the converted value.

Convert a string to a number with specified scale (2):

```
SELECT CAST(varchar_value AS NUMBER(5,2)) AS varchar_to_number1,
       SYSTEM$TYPEOF(varchar_to_number1) AS data_type
  FROM test_data_type_conversion;
```

Copy

```
+--------------------+------------------+
| VARCHAR_TO_NUMBER1 | DATA_TYPE        |
|--------------------+------------------|
|               9.88 | NUMBER(5,2)[SB4] |
+--------------------+------------------+
```

Convert the same string to a number with scale 5, using
the `::` notation:

```
SELECT varchar_value::NUMBER(6,5) AS varchar_to_number2,
       SYSTEM$TYPEOF(varchar_to_number2) AS data_type
  FROM test_data_type_conversion;
```

Copy

```
+--------------------+------------------+
| VARCHAR_TO_NUMBER2 | DATA_TYPE        |
|--------------------+------------------|
|            9.87650 | NUMBER(6,5)[SB4] |
+--------------------+------------------+
```

Convert a number to an integer. For an integer, precision and scale cannot be specified, so
the default is always NUMBER(38, 0).

```
SELECT CAST(number_value AS INTEGER) AS number_to_integer,
       SYSTEM$TYPEOF(number_to_integer) AS data_type
  FROM test_data_type_conversion;
```

Copy

```
+-------------------+-------------------+
| NUMBER_TO_INTEGER | DATA_TYPE         |
|-------------------+-------------------|
|                 1 | NUMBER(38,0)[SB1] |
+-------------------+-------------------+
```

Convert a number to a string:

```
SELECT CAST(number_value AS VARCHAR) AS number_to_varchar,
       SYSTEM$TYPEOF(number_to_varchar) AS data_type
  FROM test_data_type_conversion;
```

Copy

```
+-------------------+--------------+
| NUMBER_TO_VARCHAR | DATA_TYPE    |
|-------------------+--------------|
| 1.2345            | VARCHAR[LOB] |
+-------------------+--------------+
```

Convert a timestamp to a date:

```
SELECT CAST(timestamp_value AS DATE) AS timestamp_to_date,
       SYSTEM$TYPEOF(timestamp_to_date) AS data_type
  FROM test_data_type_conversion;
```

Copy

```
+-------------------+-----------+
| TIMESTAMP_TO_DATE | DATA_TYPE |
|-------------------+-----------|
| 2024-05-09        | DATE[SB4] |
+-------------------+-----------+
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

Related content

1. [Data type conversion](/sql-reference/functions/../data-type-conversion)