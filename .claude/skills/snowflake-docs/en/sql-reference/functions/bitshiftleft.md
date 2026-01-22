---
auto_generated: true
description: Bitwise expression functions
last_scraped: '2026-01-14T16:55:51.252122+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/bitshiftleft
title: BITSHIFTLEFT | Snowflake Documentation
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

     + [BITAND](bitand.md)
     + [BITAND\_AGG](bitand_agg.md)
     + [BITNOT](bitnot.md)
     + [BITOR](bitor.md)
     + [BITOR\_AGG](bitor_agg.md)
     + [BITSHIFTLEFT](bitshiftleft.md)
     + [BITSHIFTRIGHT](bitshiftright.md)
     + [BITXOR](bitxor.md)
     + [BITXOR\_AGG](bitxor_agg.md)
     + [GETBIT](getbit.md)
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

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)[Bitwise expression](../expressions-byte-bit.md)BITSHIFTLEFT

Categories:
:   [Bitwise expression functions](../expressions-byte-bit)

# BITSHIFTLEFT[¶](#bitshiftleft "Link to this heading")

Shifts the bits for a numeric or binary expression `n` positions to the left.

Aliases:
:   BIT\_SHIFTLEFT

See also:
:   [BITSHIFTRIGHT](bitshiftright)

## Syntax[¶](#syntax "Link to this heading")

```
BITSHIFTLEFT( <expr1> , <n> )
```

Copy

## Arguments[¶](#arguments "Link to this heading")

`expr1`
:   This expression must evaluate to an INTEGER value, a BINARY value, or a value of a data type
    that can be cast to an INTEGER value.

`n`
:   The number of bits to shift by.

## Returns[¶](#returns "Link to this heading")

Returns an INTEGER value, a BINARY value, or NULL:

* When the input expression contains an INTEGER value, returns a signed 128-bit (16-byte) integer,
  regardless of the size or data type of the input data value.
* When the input expression contains a BINARY value, returns a BINARY value.
* If any argument is NULL, returns NULL.

## Usage notes[¶](#usage-notes "Link to this heading")

* If the data type of any argument is [numeric](../data-types-numeric)
  but not INTEGER (e.g. FLOAT, DECIMAL, etc.), then that argument is cast to an INTEGER value.
* If the data type of any argument is a string (e.g. VARCHAR), then the
  argument is cast to an INTEGER value if possible. For example, the string `12.3`
  is cast to `12`. If the value cannot be cast to an INTEGER value, then the
  value is treated as NULL.
* If a signed INTEGER value is returned, and the value of the high bit changes (from 0 to 1, or from 1 to 0),
  the sign of the result is reversed. For example, `BITSHIFTLEFT(1, 127)` returns a negative number.
* If a signed INTEGER value is returned, bits that are shifted past the end of the 128-bit output value
  are dropped.
* The function does not implicitly cast arguments to BINARY values.

## Examples[¶](#examples "Link to this heading")

The following sections contain examples for INTEGER argument values and BINARY argument values.

### Using BITSHIFTLEFT and BITSHIFTRIGHT with INTEGER argument values[¶](#using-bitshiftleft-and-bitshiftright-with-integer-argument-values "Link to this heading")

Create a simple table and data:

```
CREATE OR REPLACE TABLE bits (ID INTEGER, bit1 INTEGER, bit2 INTEGER);
```

Copy

```
INSERT INTO bits (ID, bit1, bit2) VALUES 
  (   11,    1,     1),    -- Bits are all the same.
  (   24,    2,     4),    -- Bits are all different.
  (   42,    4,     2),    -- Bits are all different.
  ( 1624,   16,    24),    -- Bits overlap.
  (65504,    0, 65504),    -- Lots of bits (all but the low 6 bits).
  (    0, NULL,  NULL)     -- No bits.
  ;
```

Copy

Run the query:

```
SELECT bit1, 
       bit2, 
       BITSHIFTLEFT(bit1, 1), 
       BITSHIFTRIGHT(bit2, 1)
  FROM bits
  ORDER BY bit1;
```

Copy

```
+------+-------+-----------------------+------------------------+
| BIT1 |  BIT2 | BITSHIFTLEFT(BIT1, 1) | BITSHIFTRIGHT(BIT2, 1) |
|------+-------+-----------------------+------------------------|
|    0 | 65504 |                     0 |                  32752 |
|    1 |     1 |                     2 |                      0 |
|    2 |     4 |                     4 |                      2 |
|    4 |     2 |                     8 |                      1 |
|   16 |    24 |                    32 |                     12 |
| NULL |  NULL |                  NULL |                   NULL |
+------+-------+-----------------------+------------------------+
```

### Using BITSHIFTLEFT with BINARY argument values[¶](#using-bitshiftleft-with-binary-argument-values "Link to this heading")

Create a simple table and insert the data:

```
CREATE OR REPLACE TABLE bits (ID INTEGER, bit1 BINARY(2), bit2 BINARY(2), bit3 BINARY(4));

INSERT INTO bits VALUES
  (1, x'1010', x'0101', x'11001010'),
  (2, x'1100', x'0011', x'01011010'),
  (3, x'BCBC', x'EEFF', x'ABCDABCD'),
  (4, NULL, NULL, NULL);
```

Copy

Note

The BINARY values are inserted using the `x'value'` notation, where `value` contains
hexadecimal digits. For more information, see [Binary input and output](../binary-input-output).

Run the query:

```
SELECT bit1,
       bit3,
       BITSHIFTLEFT(bit1, 1),
       BITSHIFTLEFT(bit3, 1),
       BITSHIFTLEFT(bit1, 8),
       BITSHIFTLEFT(bit3, 16)
  FROM bits;
```

Copy

```
+------+----------+-----------------------+-----------------------+-----------------------+------------------------+
| BIT1 | BIT3     | BITSHIFTLEFT(BIT1, 1) | BITSHIFTLEFT(BIT3, 1) | BITSHIFTLEFT(BIT1, 8) | BITSHIFTLEFT(BIT3, 16) |
|------+----------+-----------------------+-----------------------+-----------------------+------------------------|
| 1010 | 11001010 | 2020                  | 22002020              | 1000                  | 10100000               |
| 1100 | 01011010 | 2200                  | 02022020              | 0000                  | 10100000               |
| BCBC | ABCDABCD | 7978                  | 579B579A              | BC00                  | ABCD0000               |
| NULL | NULL     | NULL                  | NULL                  | NULL                  | NULL                   |
+------+----------+-----------------------+-----------------------+-----------------------+------------------------+
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