---
auto_generated: true
description: String & binary functions (Matching/Comparison)
last_scraped: '2026-01-14T16:56:27.134001+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/substr.html
title: SUBSTR , SUBSTRING | Snowflake Documentation
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

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)[String & binary](../functions-string.md)SUBSTR

Categories:
:   [String & binary functions](../functions-string) (Matching/Comparison)

# SUBSTR , SUBSTRING[¶](#substr-substring "Link to this heading")

Returns the portion of the [string or binary](../data-types-text) value
from `base_expr`, starting from the character/byte specified by `start_expr`,
with optionally limited length.

These functions are synonymous.

See also:
:   [LEFT](left) , [RIGHT](right)

## Syntax[¶](#syntax "Link to this heading")

```
SUBSTR( <base_expr>, <start_expr> [ , <length_expr> ] )

SUBSTRING( <base_expr>, <start_expr> [ , <length_expr> ] )
```

Copy

## Arguments[¶](#arguments "Link to this heading")

`base_expr`
:   An expression that evaluates to a VARCHAR or BINARY value.

`start_expr`
:   An expression that evaluates to an integer. It specifies the offset from which the substring starts. The offset is measured in:

    * The number of UTF-8 characters if the input is a VARCHAR value.
    * The number of bytes if the input is a BINARY value.

    The start position is 1-based, not 0-based. For example, `SUBSTR('abc', 1, 1)` returns `a`, not `b`.

`length_expr`
:   An expression that evaluates to an integer. It specifies:

    * The number of UTF-8 characters to return if the input is VARCHAR.
    * The number of bytes to return if the input is BINARY.

    Specify a length that is greater than or equal to zero. If the length is a negative number, the function returns an
    empty string.

## Returns[¶](#returns "Link to this heading")

The data type of the returned value is the same as the data type of the `base_expr` (VARCHAR or BINARY).

If any of the inputs are NULL, NULL is returned.

## Usage notes[¶](#usage-notes "Link to this heading")

* If `length_expr` is specified, up to `length_expr` characters/bytes are
  returned. If `length_expr` isn’t specified, all the characters until the end of the string or
  binary value are returned.
* The values in `start_expr` start from 1:

  > + If 0 is specified, it is treated as 1.
  > + If a negative value is specified, the starting position is computed as
  >   the `start_expr` characters/bytes from the end of the string or binary
  >   value. If the position is outside of the range of a string or binary
  >   value, an empty value is returned.

## Collation details[¶](#collation-details "Link to this heading")

* Collation applies to VARCHAR inputs. Collation doesn’t apply if the input data type of the first parameter
  is BINARY.
* No impact. Although collation is accepted syntactically, collations don’t affect processing. For example,
  two-character and three-character letters in languages (for example, “dzs” in Hungarian or “ch” in Czech)
  are still counted as two or three characters (not one character) for the length argument.
* The collation of the result is the same as the collation of the input. This can be useful if the returned value is passed to another function as part of nested function calls.

## Examples[¶](#examples "Link to this heading")

The following examples use the SUBSTR function.

### Basic example[¶](#basic-example "Link to this heading")

The following example uses the SUBSTR function to return the portion of the string that starts at the
ninth character and limits the length of the returned value to three characters:

```
SELECT SUBSTR('testing 1 2 3', 9, 3);
```

Copy

```
+-------------------------------+
| SUBSTR('TESTING 1 2 3', 9, 3) |
|-------------------------------|
| 1 2                           |
+-------------------------------+
```

### Specifying different start and length values[¶](#specifying-different-start-and-length-values "Link to this heading")

The following example shows the substrings returned for the same `base_expr` when different
values are specified for `start_expr` and `length_expr`:

```
CREATE OR REPLACE TABLE test_substr (
    base_value VARCHAR,
    start_value INT,
    length_value INT)
  AS SELECT
    column1,
    column2,
    column3
  FROM
    VALUES
      ('mystring', -1, 3),
      ('mystring', -3, 3),
      ('mystring', -3, 7),
      ('mystring', -5, 3),
      ('mystring', -7, 3),
      ('mystring', 0, 3),
      ('mystring', 0, 7),
      ('mystring', 1, 3),
      ('mystring', 1, 7),
      ('mystring', 3, 3),
      ('mystring', 3, 7),
      ('mystring', 5, 3),
      ('mystring', 5, 7),
      ('mystring', 7, 3),
      ('mystring', NULL, 3),
      ('mystring', 3, NULL);

SELECT base_value,
       start_value,
       length_value,
       SUBSTR(base_value, start_value, length_value) AS substring
  FROM test_substr;
```

Copy

```
+------------+-------------+--------------+-----------+
| BASE_VALUE | START_VALUE | LENGTH_VALUE | SUBSTRING |
|------------+-------------+--------------+-----------|
| mystring   |          -1 |            3 | g         |
| mystring   |          -3 |            3 | ing       |
| mystring   |          -3 |            7 | ing       |
| mystring   |          -5 |            3 | tri       |
| mystring   |          -7 |            3 | yst       |
| mystring   |           0 |            3 | mys       |
| mystring   |           0 |            7 | mystrin   |
| mystring   |           1 |            3 | mys       |
| mystring   |           1 |            7 | mystrin   |
| mystring   |           3 |            3 | str       |
| mystring   |           3 |            7 | string    |
| mystring   |           5 |            3 | rin       |
| mystring   |           5 |            7 | ring      |
| mystring   |           7 |            3 | ng        |
| mystring   |        NULL |            3 | NULL      |
| mystring   |           3 |         NULL | NULL      |
+------------+-------------+--------------+-----------+
```

### Returning substrings for email, phone, and date strings[¶](#returning-substrings-for-email-phone-and-date-strings "Link to this heading")

The following examples return substrings for customer information in a table.

Create the table and insert data:

```
CREATE OR REPLACE TABLE customer_contact_example (
    cust_id INT,
    cust_email VARCHAR,
    cust_phone VARCHAR,
    activation_date VARCHAR)
  AS SELECT
    column1,
    column2,
    column3,
    column4
  FROM
    VALUES
      (1, 'some_text@example.com', '800-555-0100', '20210320'),
      (2, 'some_other_text@example.org', '800-555-0101', '20240509'),
      (3, 'some_different_text@example.net', '800-555-0102', '20191017');

SELECT * from customer_contact_example;
```

Copy

```
+---------+---------------------------------+--------------+-----------------+
| CUST_ID | CUST_EMAIL                      | CUST_PHONE   | ACTIVATION_DATE |
|---------+---------------------------------+--------------+-----------------|
|       1 | some_text@example.com           | 800-555-0100 | 20210320        |
|       2 | some_other_text@example.org     | 800-555-0101 | 20240509        |
|       3 | some_different_text@example.net | 800-555-0102 | 20191017        |
+---------+---------------------------------+--------------+-----------------+
```

Use the [POSITION](position) function with the SUBSTR function to extract the domains from email addresses.
This example finds the position of `@` in each string and starts from the next character by adding
one:

```
SELECT cust_id,
       cust_email,
       SUBSTR(cust_email, POSITION('@' IN cust_email) + 1) AS domain
  FROM customer_contact_example;
```

Copy

```
+---------+---------------------------------+-------------+
| CUST_ID | CUST_EMAIL                      | DOMAIN      |
|---------+---------------------------------+-------------|
|       1 | some_text@example.com           | example.com |
|       2 | some_other_text@example.org     | example.org |
|       3 | some_different_text@example.net | example.net |
+---------+---------------------------------+-------------+
```

Tip

You can use the POSITION function to find the position of other characters, such as an empty
character (`' '`) or an underscore (`_`).

In the `cust_phone` column in the table, the area code is always the first three characters. Extract
the area code from phone numbers:

```
SELECT cust_id,
       cust_phone,
       SUBSTR(cust_phone, 1, 3) AS area_code
  FROM customer_contact_example;
```

Copy

```
+---------+--------------+-----------+
| CUST_ID | CUST_PHONE   | AREA_CODE |
|---------+--------------+-----------|
|       1 | 800-555-0100 | 800       |
|       2 | 800-555-0101 | 800       |
|       3 | 800-555-0102 | 800       |
+---------+--------------+-----------+
```

Remove the area code from phone numbers:

```
SELECT cust_id,
       cust_phone,
       SUBSTR(cust_phone, 5) AS phone_without_area_code
  FROM customer_contact_example;
```

Copy

```
+---------+--------------+-------------------------+
| CUST_ID | CUST_PHONE   | PHONE_WITHOUT_AREA_CODE |
|---------+--------------+-------------------------|
|       1 | 800-555-0100 | 555-0100                |
|       2 | 800-555-0101 | 555-0101                |
|       3 | 800-555-0102 | 555-0102                |
+---------+--------------+-------------------------+
```

In the `activation_date` column in the table, the date is always in the format `YYYYMMDD`. Extract the year,
month, and day from these strings:

```
SELECT cust_id,
       activation_date,
       SUBSTR(activation_date, 1, 4) AS year,
       SUBSTR(activation_date, 5, 2) AS month,
       SUBSTR(activation_date, 7, 2) AS day
  FROM customer_contact_example;
```

Copy

```
+---------+-----------------+------+-------+-----+
| CUST_ID | ACTIVATION_DATE | YEAR | MONTH | DAY |
|---------+-----------------+------+-------+-----|
|       1 | 20210320        | 2021 | 03    | 20  |
|       2 | 20240509        | 2024 | 05    | 09  |
|       3 | 20191017        | 2019 | 10    | 17  |
+---------+-----------------+------+-------+-----+
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
5. [Collation details](#collation-details)
6. [Examples](#examples)