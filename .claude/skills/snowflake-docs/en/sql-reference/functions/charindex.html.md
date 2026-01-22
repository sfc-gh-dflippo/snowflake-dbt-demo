---
auto_generated: true
description: String & binary functions (Matching/Comparison)
last_scraped: '2026-01-14T16:57:16.963671+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/charindex.html
title: CHARINDEX | Snowflake Documentation
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

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)[String & binary](../functions-string.md)CHARINDEX

Categories:
:   [String & binary functions](../functions-string) (Matching/Comparison)

# CHARINDEX[¶](#charindex "Link to this heading")

Searches for the first occurrence of the first argument in the second argument and, if successful, returns the position (1-based) of the first argument in the second argument.

Aliases:
:   [POSITION](position)

    Note that the CHARINDEX function does not support one of the syntax variations that POSITION supports.

## Syntax[¶](#syntax "Link to this heading")

```
CHARINDEX( <expr1>, <expr2> [ , <start_pos> ] )
```

Copy

## Arguments[¶](#arguments "Link to this heading")

**Required:**

`expr1`
:   A string or binary expression representing the value to look for.

`expr2`
:   A string or binary expression representing the value to search.

**Optional:**

`start_pos`
:   A number indicating the position from where to start the search (with `1` representing the start of `expr2`).

    Default: `1`

## Usage notes[¶](#usage-notes "Link to this heading")

* If any arguments are NULL, the function returns NULL.
* If the string or binary value is not found, the function returns `0`.
* If the specified optional `start_pos` is beyond the end of the second argument (the string to
  search), the function returns `0`.
* If the first argument is empty (e.g. an empty string), the function returns `1`.
* The data types of the first two arguments should be the same; either both
  should be strings or both should be binary values.

## Collation details[¶](#collation-details "Link to this heading")

This function does not support the following collation specifications:

* `pi` (punctuation-insensitive).
* `cs-ai` (case-sensitive, accent-insensitive).

## Examples[¶](#examples "Link to this heading")

### VARCHAR expressions[¶](#varchar-expressions "Link to this heading")

Find the first occurrence of ‘an’ in ‘banana’:

> ```
> select charindex('an', 'banana', 1);
> +------------------------------+
> | CHARINDEX('AN', 'BANANA', 1) |
> |------------------------------|
> |                            2 |
> +------------------------------+
> ```
>
> Copy

Find the first occurrence of ‘an’ in ‘banana’ at or after position 3. This search finds the second occurrence of ‘an’.

> ```
> select charindex('an', 'banana', 3);
> +------------------------------+
> | CHARINDEX('AN', 'BANANA', 3) |
> |------------------------------|
> |                            4 |
> +------------------------------+
> ```
>
> Copy

Search for various characters, including unicode characters, in strings:

> ```
> SELECT n, h, CHARINDEX(n, h) FROM pos;
>
> +--------+---------------------+-----------------+
> | N      | H                   | CHARINDEX(N, H) |
> |--------+---------------------+-----------------|
> |        |                     |               1 |
> |        | sth                 |               1 |
> | 43     | 41424344            |               5 |
> | a      | NULL                |            NULL |
> | dog    | catalog             |               0 |
> | log    | catalog             |               5 |
> | lésine | le péché, la lésine |              14 |
> | nicht  | Ich weiß nicht      |              10 |
> | sth    |                     |               0 |
> | ☃c     | ☃a☃b☃c☃d            |               5 |
> | ☃☃     | bunch of ☃☃☃☃       |              10 |
> | ❄c     | ❄a☃c❄c☃             |               5 |
> | NULL   | a                   |            NULL |
> | NULL   | NULL                |            NULL |
> +--------+---------------------+-----------------+
> ```
>
> Copy

### BINARY expressions[¶](#binary-expressions "Link to this heading")

Note that because the values below are hexadecimal representations, a single BINARY byte is represented as two hex
digits.

In this example, the returned value is 3 because ‘EF’ matches the 3rd
byte (the first byte is ‘AB’; the second byte is ‘CD’, and the third byte
is ‘EF’):

> ```
> SELECT CHARINDEX(X'EF', X'ABCDEF');
> +-----------------------------+
> | CHARINDEX(X'EF', X'ABCDEF') |
> |-----------------------------|
> |                           3 |
> +-----------------------------+
> ```
>
> Copy

In this example, there is no match. Although the sequence ‘BC’ appears to be
in the value being searched, the ‘B’ is the second nybble of the first
byte, and the ‘C’ is the first nybble of the second byte; no byte actually
contains ‘BC’, so the returned value is 0 (not found).

> ```
> SELECT CHARINDEX(X'BC', X'ABCD');
> +---------------------------+
> | CHARINDEX(X'BC', X'ABCD') |
> |---------------------------|
> |                         0 |
> +---------------------------+
> ```
>
> Copy

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
4. [Collation details](#collation-details)
5. [Examples](#examples)