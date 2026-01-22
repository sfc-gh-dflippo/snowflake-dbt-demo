---
auto_generated: true
description: String & binary functions (General)
last_scraped: '2026-01-14T16:54:30.991057+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/lpad
title: LPAD | Snowflake Documentation
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
   * [Snowpark Container Services](../functions-spcs.md)
   * [String & binary](../functions-string.md)

     + General manipulation
     + [ASCII](ascii.md)
     + [BIT\_LENGTH](bit_length.md)
     + [CHR](chr.md)
     + [CHAR](chr.md)
     + [CONCAT, ||](concat.md)
     + [CONCAT\_WS](concat_ws.md)
     + [INSERT](insert.md)
     + [LENGTH](length.md)
     + [LEN](length.md)
     + [LPAD](lpad.md)
     + [LTRIM](ltrim.md)
     + [OCTET\_LENGTH](octet_length.md)
     + [PARSE\_IP](parse_ip.md)
     + [PARSE\_URL](parse_url.md)
     + [REPEAT](repeat.md)
     + [REVERSE](reverse.md)
     + [RPAD](rpad.md)
     + [RTRIM](rtrim.md)
     + [RTRIMMED\_LENGTH](rtrimmed_length.md)
     + [SOUNDEX](soundex.md)
     + [SOUNDEX\_P123](soundex_p123.md)
     + [SPACE](space.md)
     + [SPLIT](split.md)
     + [SPLIT\_PART](split_part.md)
     + [SPLIT\_TO\_TABLE](split_to_table.md)
     + [STRTOK](strtok.md)
     + [STRTOK\_TO\_ARRAY](strtok_to_array.md)
     + [STRTOK\_SPLIT\_TO\_TABLE](strtok_split_to_table.md)
     + [TRANSLATE](translate.md)
     + [TRIM](trim.md)
     + [UNICODE](unicode.md)
     + [UUID\_STRING](uuid_string.md)
     + Full-text search
     + [SEARCH](search.md)
     + [SEARCH\_IP](search_ip.md)
     + Case conversion
     + [INITCAP](initcap.md)
     + [LOWER](lower.md)
     + [UPPER](upper.md)
     + Regular expression matching
     + [[ NOT ] REGEXP](/en/sql-reference/functions/regexp "[ NOT ] REGEXP")
     + [REGEXP\_COUNT](regexp_count.md)
     + [REGEXP\_EXTRACT\_ALL](regexp_substr_all.md)
     + [REGEXP\_INSTR](regexp_instr.md)
     + [REGEXP\_LIKE](regexp_like.md)
     + [REGEXP\_REPLACE](regexp_replace.md)
     + [REGEXP\_SUBSTR](regexp_substr.md)
     + [REGEXP\_SUBSTR\_ALL](regexp_substr_all.md)
     + [[ NOT ] RLIKE](/en/sql-reference/functions/rlike "[ NOT ] RLIKE")
     + Other matching/comparison
     + [CHARINDEX](charindex.md)
     + [CONTAINS](contains.md)
     + [EDITDISTANCE](editdistance.md)
     + [ENDSWITH](endswith.md)
     + [[ NOT ] ILIKE](/en/sql-reference/functions/ilike "[ NOT ] ILIKE")
     + [ILIKE ANY](ilike_any.md)
     + [JAROWINKLER\_SIMILARITY](jarowinkler_similarity.md)
     + [LEFT](left.md)
     + [[ NOT ] LIKE](/en/sql-reference/functions/like "[ NOT ] LIKE")
     + [LIKE ALL](like_all.md)
     + [LIKE ANY](like_any.md)
     + [POSITION](position.md)
     + [REPLACE](replace.md)
     + [RIGHT](right.md)
     + [STARTSWITH](startswith.md)
     + [SUBSTR](substr.md)
     + [SUBSTRING](substr.md)
     + Compression/decompression
     + [COMPRESS](compress.md)
     + [DECOMPRESS\_BINARY](decompress_binary.md)
     + [DECOMPRESS\_STRING](decompress_string.md)
     + Encoding/decoding
     + [BASE64\_DECODE\_BINARY](base64_decode_binary.md)
     + [BASE64\_DECODE\_STRING](base64_decode_string.md)
     + [BASE64\_ENCODE](base64_encode.md)
     + [HEX\_DECODE\_BINARY](hex_decode_binary.md)
     + [HEX\_DECODE\_STRING](hex_decode_string.md)
     + [HEX\_ENCODE](hex_encode.md)
     + [TRY\_BASE64\_DECODE\_BINARY](try_base64_decode_binary.md)
     + [TRY\_BASE64\_DECODE\_STRING](try_base64_decode_string.md)
     + [TRY\_HEX\_DECODE\_BINARY](try_hex_decode_binary.md)
     + [TRY\_HEX\_DECODE\_STRING](try_hex_decode_string.md)
     + Cryptographic/checksum
     + [MD5](md5.md)
     + [MD5\_HEX](md5.md)
     + [MD5\_BINARY](md5_binary.md)
     + [MD5\_NUMBER\_LOWER64](md5_number_lower64.md)
     + [MD5\_NUMBER\_UPPER64](md5_number_upper64.md)
     + [SHA1](sha1.md)
     + [SHA1\_HEX](sha1.md)
     + [SHA1\_BINARY](sha1_binary.md)
     + [SHA2](sha2.md)
     + [SHA2\_HEX](sha2.md)
     + [SHA2\_BINARY](sha2_binary.md)
     + Hash (non-cryptographic)
     + [HASH](hash.md)
     + [HASH\_AGG](hash_agg.md)
     + Collation
     + [COLLATE](collate.md)
     + [COLLATION](collation.md)
     + AI Functions
     + [AI\_AGG](ai_agg.md)
     + [AI\_CLASSIFY](ai_classify.md)
     + [AI\_COMPLETE](ai_complete.md)
     + [AI\_COUNT\_TOKENS](ai_count_tokens.md)
     + [AI\_EMBED](ai_embed.md)
     + [AI\_EXTRACT](ai_extract.md)
     + [AI\_FILTER](ai_filter.md)
     + [AI\_SENTIMENT](ai_sentiment.md)
     + [AI\_SIMILARITY](ai_similarity.md)
     + [AI\_SUMMARIZE\_AGG](ai_summarize_agg.md)
     + [AI\_TRANSLATE](ai_translate.md)
     + [CLASSIFY\_TEXT](classify_text-snowflake-cortex.md)
     + [COMPLETE](complete-snowflake-cortex.md)
     + [COMPLETE multimodal (images)](complete-snowflake-cortex-multimodal.md)")
     + [EMBED\_TEXT\_768](embed_text-snowflake-cortex.md)
     + [EMBED\_TEXT\_1024](embed_text_1024-snowflake-cortex.md)
     + [ENTITY\_SENTIMENT](entity_sentiment-snowflake-cortex.md)
     + [EXTRACT\_ANSWER](extract_answer-snowflake-cortex.md)
     + [FINETUNE](finetune-snowflake-cortex.md)
     + [PARSE\_DOCUMENT](parse_document-snowflake-cortex.md)
     + [SENTIMENT](sentiment-snowflake-cortex.md)
     + [SUMMARIZE](summarize-snowflake-cortex.md)
     + [TRANSLATE](translate-snowflake-cortex.md)
     + AI helper functions
     + [COUNT\_TOKENS](count_tokens-snowflake-cortex.md)
     + [SEARCH\_PREVIEW](search_preview-snowflake-cortex.md)
     + [SPLIT\_TEXT\_MARKDOWN\_HEADER](split_text_markdown_header-snowflake-cortex.md)
     + [SPLIT\_TEXT\_RECURSIVE\_CHARACTER](split_text_recursive_character-snowflake-cortex.md)
     + [TRY\_COMPLETE](try_complete-snowflake-cortex.md)
   * [System](../functions-system.md)
   * [Table](../functions-table.md)
   * [Vector](../functions-vector.md)
   * [Window](../functions-window.md)
   * [Stored procedures](../../sql-reference-stored-procedures.md)
5. [Class reference](../../sql-reference-classes.md)
6. [Scripting reference](../../sql-reference-snowflake-scripting.md)
7. [General reference](../../sql-reference.md)
8. [API reference](../../api-reference.md)

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)[String & binary](../functions-string.md)LPAD

Categories:
:   [String & binary functions](../functions-string) (General)

# LPAD[¶](#lpad "Link to this heading")

Left-pads a string with characters from another string, or left-pads a binary value with bytes from another binary value.

The argument (`base`) is left-padded to length `length_expr` with characters/bytes from the `pad` argument.

See also:
:   [RPAD](rpad)

## Syntax[¶](#syntax "Link to this heading")

```
LPAD( <base>, <length_expr> [, <pad>] )
```

Copy

## Arguments[¶](#arguments "Link to this heading")

`base`
:   A VARCHAR or BINARY value.

`length_expr`
:   An expression that evaluates to an integer. It specifies:

    * The number of UTF-8 characters to return if the input is VARCHAR.
    * The number of bytes to return if the input is BINARY.

`pad`
:   A VARCHAR or BINARY value. The type must match the data type of the `base` argument.
    Characters (or bytes) from this argument are used to pad the `base`.

## Returns[¶](#returns "Link to this heading")

The data type of the returned value is the same as the data type of the `base` input value (VARCHAR or BINARY).

## Usage notes[¶](#usage-notes "Link to this heading")

* If the `base` argument is longer than `length_expr`, it is truncated to length `length_expr`.
* The `pad` argument can be multiple characters/bytes long. The `pad`
  argument is repeated in the result until the desired length (`length_expr`) is
  reached, truncating any superfluous characters/bytes in the `pad` argument.
  If the `pad` argument is empty, no padding is inserted, but the result is
  still truncated to length `length_expr`.
* When `base` is a string, the default `pad` string is `' '` (a single blank space). When
  `base` is a binary value, the `pad` argument must be provided explicitly.

## Collation details[¶](#collation-details "Link to this heading")

* Collation applies to VARCHAR inputs. Collation doesn’t apply if the input data type of the first argument
  is BINARY.
* No impact.
  Although collation is accepted syntactically, collations have no impact on processing. For example, languages with
  two-character and three-character letters (for example, “dzs” in Hungarian, “ch” in Czech) still count
  those as two or three characters (not one character) for the length argument.
* The collation of the result is the same as the collation of the input. This can be useful if the returned value is passed to another function as part of nested function calls.
* Currently, Snowflake allows the `base` and `pad` arguments to have different collation specifiers.
  However, the individual collation specifiers can’t both be retained because the returned value has only one
  collation specifier. Snowflake recommends that you avoid using `pad` strings that have a different
  collation from the `base` string.

## Examples[¶](#examples "Link to this heading")

The LPAD function can pad a string with characters on the left so that the values conform to a
specific format. The following example assumes that the `id` values in a column should be eight
characters long and padded with zeros on the left to meet this standard.

Create a table with an `id` column and insert values:

```
CREATE OR REPLACE TABLE demo_lpad_ids (id VARCHAR);

INSERT INTO demo_lpad_ids VALUES
  ('5'),
  ('50'),
  ('500');
```

Copy

Run a query using the LPAD function so that values in the output meet the standard:

```
SELECT id, LPAD(id, 8, '0') AS padded_ids
  FROM demo_lpad_ids;
```

Copy

```
+-----+------------+
| ID  | PADDED_IDS |
|-----+------------|
| 5   | 00000005   |
| 50  | 00000050   |
| 500 | 00000500   |
+-----+------------+
```

The following additional examples use the LPAD function to pad VARCHAR and BINARY data on the left.

Create and fill a table:

```
CREATE OR REPLACE TABLE padding_example (v VARCHAR, b BINARY);

INSERT INTO padding_example (v, b)
  SELECT
    'Hi',
    HEX_ENCODE('Hi');

INSERT INTO padding_example (v, b)
  SELECT
    '-123.00',
    HEX_ENCODE('-123.00');

INSERT INTO padding_example (v, b)
  SELECT
    'Twelve Dollars',
    TO_BINARY(HEX_ENCODE('Twelve Dollars'), 'HEX');
```

Copy

Query the table to show the data:

```
SELECT * FROM padding_example;
```

Copy

```
+----------------+------------------------------+
| V              | B                            |
|----------------+------------------------------|
| Hi             | 4869                         |
| -123.00        | 2D3132332E3030               |
| Twelve Dollars | 5477656C766520446F6C6C617273 |
+----------------+------------------------------+
```

This example demonstrates left-padding of VARCHAR values using the LPAD function, with the
results limited to 10 characters:

```
SELECT v,
       LPAD(v, 10, ' ') AS pad_with_blank,
       LPAD(v, 10, '$') AS pad_with_dollar_sign
  FROM padding_example
  ORDER BY v;
```

Copy

```
+----------------+----------------+----------------------+
| V              | PAD_WITH_BLANK | PAD_WITH_DOLLAR_SIGN |
|----------------+----------------+----------------------|
| -123.00        |    -123.00     | $$$-123.00           |
| Hi             |         Hi     | $$$$$$$$Hi           |
| Twelve Dollars | Twelve Dol     | Twelve Dol           |
+----------------+----------------+----------------------+
```

This example demonstrates left-padding of BINARY values using the LPAD function, with the
results limited to 10 bytes:

```
SELECT b,
       LPAD(b, 10, TO_BINARY(HEX_ENCODE(' '))) AS pad_with_blank,
       LPAD(b, 10, TO_BINARY(HEX_ENCODE('$'))) AS pad_with_dollar_sign
  FROM padding_example
  ORDER BY b;
```

Copy

```
+------------------------------+----------------------+----------------------+
| B                            | PAD_WITH_BLANK       | PAD_WITH_DOLLAR_SIGN |
|------------------------------+----------------------+----------------------|
| 2D3132332E3030               | 2020202D3132332E3030 | 2424242D3132332E3030 |
| 4869                         | 20202020202020204869 | 24242424242424244869 |
| 5477656C766520446F6C6C617273 | 5477656C766520446F6C | 5477656C766520446F6C |
+------------------------------+----------------------+----------------------+
```

This example shows left-padding when multiple characters are used and when
the padding isn’t an even multiple of the length of the multi-character
string used for padding:

```
SELECT LPAD('123.50', 19, '*_');
```

Copy

```
+--------------------------+
| LPAD('123.50', 19, '*_') |
|--------------------------|
| *_*_*_*_*_*_*123.50      |
+--------------------------+
```

The output shows that 19 characters were returned, and the last `*` character doesn’t have
an accompanying `_` character.

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
5. [Collation details](#collation-details)
6. [Examples](#examples)