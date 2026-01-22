---
auto_generated: true
description: Conversion functions
last_scraped: '2026-01-14T16:56:08.062950+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/try_to_binary
title: TRY_TO_BINARY | Snowflake Documentation
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

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)[Conversion](../functions-conversion.md)TRY\_TO\_BINARY

Categories:
:   [Conversion functions](../functions-conversion)

# TRY\_TO\_BINARY[¶](#try-to-binary "Link to this heading")

A special version of [TO\_BINARY](to_binary) that performs the same operation (i.e. converts an input expression to a binary value),
but with error handling support (i.e. if the conversion cannot be performed, it returns a NULL value instead of raising an error).

For more information, see:

* [Error-handling conversion functions](../functions-conversion.html#label-try-conversion-functions).
* [TO\_BINARY](to_binary).
* [Binary input and output](../binary-input-output).

## Syntax[¶](#syntax "Link to this heading")

```
TRY_TO_BINARY( <string_expr> [, '<format>'] )
```

Copy

## Arguments[¶](#arguments "Link to this heading")

**Required:**

`string_expr`
:   A string expression.

**Optional:**

`format`
:   The binary format for conversion: HEX, BASE64, or UTF-8 (see [Binary input and output](../binary-input-output)). The default is the value of the
    BINARY\_INPUT\_FORMAT session parameter. If this parameter is not set, the
    default is HEX.

## Returns[¶](#returns "Link to this heading")

Returns a value of type BINARY.

## Usage notes[¶](#usage-notes "Link to this heading")

* Only works for string expressions.
* If `format` is specified but is not HEX, BASE64, or UTF-8, the result will be a NULL value.

## Examples[¶](#examples "Link to this heading")

This shows how to use the `TRY_TO_BINARY` function when loading
hex-encoded strings into a BINARY column:

> Create and fill a table:
>
> > ```
> > CREATE TABLE strings (v VARCHAR, hex_encoded_string VARCHAR, b BINARY);
> > INSERT INTO strings (v) VALUES
> >     ('01'),
> >     ('A B'),
> >     ('Hello'),
> >     (NULL);
> > UPDATE strings SET hex_encoded_string = HEX_ENCODE(v);
> > UPDATE strings SET b = TRY_TO_BINARY(hex_encoded_string, 'HEX');
> > ```
> >
> > Copy
>
> Query the table, calling TRY\_TO\_BINARY():
>
> > ```
> > SELECT v, hex_encoded_string, TO_VARCHAR(b, 'UTF-8')
> >   FROM strings
> >   ORDER BY v
> >   ;
> > +-------+--------------------+------------------------+
> > | V     | HEX_ENCODED_STRING | TO_VARCHAR(B, 'UTF-8') |
> > |-------+--------------------+------------------------|
> > | 01    | 3031               | 01                     |
> > | A B   | 412042             | A B                    |
> > | Hello | 48656C6C6F         | Hello                  |
> > | NULL  | NULL               | NULL                   |
> > +-------+--------------------+------------------------+
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