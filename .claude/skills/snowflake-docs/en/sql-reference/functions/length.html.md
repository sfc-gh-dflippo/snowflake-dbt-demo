---
auto_generated: true
description: String & binary functions (General)
last_scraped: '2026-01-14T16:57:29.554849+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/length.html
title: LENGTH, LEN | Snowflake Documentation
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

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)[String & binary](../functions-string.md)LENGTH

Categories:
:   [String & binary functions](../functions-string) (General)

# LENGTH, LEN[¶](#length-len "Link to this heading")

Returns the length of an input [string or binary](../data-types-text) value. For strings,
the length is the number of characters, and UTF-8 characters are counted as a single character. For binary,
the length is the number of bytes.

## Syntax[¶](#syntax "Link to this heading")

```
LENGTH( <expression> )

LEN( <expression> )
```

Copy

## Arguments[¶](#arguments "Link to this heading")

`expression`
:   The input expression must be a string or binary value.

## Returns[¶](#returns "Link to this heading")

The returned data type is INTEGER (more precisely, NUMBER(18, 0)).

## Collation details[¶](#collation-details "Link to this heading")

* No impact.
  In languages in which one character is one letter and vice versa, the LENGTH function behaves the same with and without
  collation.
* In languages where the alphabet contains digraphs or trigraphs (such as “Dz” and “Dzs” in Hungarian), each character in each digraph and trigraph is treated as an independent character, not as part of a single multi-character letter.
  For example, although Hungarian treats “dz” as a single letter, Snowflake returns `2` for `LENGTH(COLLATE('dz', 'hu'))`.

## Examples[¶](#examples "Link to this heading")

Create a table and insert VARCHAR values:

```
CREATE OR REPLACE TABLE length_function_demo (s VARCHAR);

INSERT INTO length_function_demo VALUES
  (''),
  ('Joyeux Noël'),
  ('Merry Christmas'),
  ('Veselé Vianoce'),
  ('Wesołych Świąt'),
  ('圣诞节快乐'),
  (NULL);
```

Copy

Query the table using the LENGTH function:

```
SELECT s, LENGTH(s) FROM length_function_demo;
```

Copy

```
+-----------------+-----------+
| S               | LENGTH(S) |
|-----------------+-----------|
|                 |         0 |
| Joyeux Noël     |        11 |
| Merry Christmas |        15 |
| Veselé Vianoce  |        14 |
| Wesołych Świąt  |        14 |
| 圣诞节快乐        |         5 |
| NULL            |      NULL |
+-----------------+-----------+
```

For the next example, create a table and insert BINARY data:

```
CREATE OR REPLACE TABLE binary_demo_table (
  v VARCHAR,
  b_hex BINARY,
  b_base64 BINARY,
  b_utf8 BINARY);

INSERT INTO binary_demo_table (v) VALUES ('hello');

UPDATE binary_demo_table SET
  b_hex    = TO_BINARY(HEX_ENCODE(v), 'HEX'),
  b_base64 = TO_BINARY(BASE64_ENCODE(v), 'BASE64'),
  b_utf8   = TO_BINARY(v, 'UTF-8');

SELECT * FROM binary_demo_table;
```

Copy

```
+-------+------------+------------+------------+
| V     | B_HEX      | B_BASE64   | B_UTF8     |
|-------+------------+------------+------------|
| hello | 68656C6C6F | 68656C6C6F | 68656C6C6F |
+-------+------------+------------+------------+
```

Query the table using the LENGTH function:

```
SELECT v, LENGTH(v),
       TO_VARCHAR(b_hex, 'HEX') AS b_hex, LENGTH(b_hex),
       TO_VARCHAR(b_base64, 'BASE64') AS b_base64, LENGTH(b_base64),
       TO_VARCHAR(b_utf8, 'UTF-8') AS b_utf8, LENGTH(b_utf8)
  FROM binary_demo_table;
```

Copy

```
+-------+-----------+------------+---------------+----------+------------------+--------+----------------+
| V     | LENGTH(V) | B_HEX      | LENGTH(B_HEX) | B_BASE64 | LENGTH(B_BASE64) | B_UTF8 | LENGTH(B_UTF8) |
|-------+-----------+------------+---------------+----------+------------------+--------+----------------|
| hello |         5 | 68656C6C6F |             5 | aGVsbG8= |                5 | hello  |              5 |
+-------+-----------+------------+---------------+----------+------------------+--------+----------------+
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
4. [Collation details](#collation-details)
5. [Examples](#examples)