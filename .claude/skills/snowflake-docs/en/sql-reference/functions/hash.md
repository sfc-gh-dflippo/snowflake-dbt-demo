---
auto_generated: true
description: Hash functions
last_scraped: '2026-01-14T16:56:58.100833+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/hash
title: HASH | Snowflake Documentation
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

     + [HASH](hash.md)
     + [HASH\_AGG](hash_agg.md)
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

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)[Hash](../functions-hash-scalar.md)HASH

Categories:
:   [Hash functions](../functions-hash-scalar)

# HASH[¶](#hash "Link to this heading")

Returns a signed 64-bit hash value. Note that HASH never returns NULL, even for NULL inputs.

Possible uses for the HASH function include:

* Convert skewed data values to values that are likely to be more randomly or more evenly distributed.

  For example, you can hash a group of highly skewed values and generate a set of values that are more likely to be randomly distributed or evenly distributed.
* Put data in buckets. Because hashing can convert skewed data values to closer-to-evenly distributed values, you can use hashing to help take skewed values and
  create approximately evenly-sized buckets.

  If hashing alone is not sufficient to get the number of distinct buckets that you want, you can combine hashing with the [ROUND](round) or [WIDTH\_BUCKET](width_bucket)
  functions.

Note

HASH is a proprietary function that accepts a variable number of input expressions of arbitrary types and returns a signed value. It is not a
cryptographic hash function and should not be used as such.

Cryptographic hash functions have a few properties which this function does not, for example:

* The cryptographic hashing of a value cannot be inverted to find the original value.
* Given a value, it is infeasible to find another value with the same cryptographic hash.

For cryptographic purposes, use the SHA families of functions (in [String & binary functions](../functions-string)).

See also:
:   [HASH\_AGG](hash_agg)

## Syntax[¶](#syntax "Link to this heading")

```
HASH( <expr> [ , <expr> ... ] )

HASH(*)
```

Copy

## Arguments[¶](#arguments "Link to this heading")

`expr`
:   The expression can be a general expression of any Snowflake data type.

`*`
:   Returns a single hashed value based on all columns in each record,
    including records with NULL values.

    When you pass a wildcard to the function, you can qualify the wildcard with the name or alias for the table.
    For example, to pass in all of the columns from the table named `mytable`, specify the following:

    ```
    (mytable.*)
    ```

    Copy

    You can also use the ILIKE and EXCLUDE keywords for filtering:

    * ILIKE filters for column names that match the specified pattern. Only one
      pattern is allowed. For example:

      ```
      (* ILIKE 'col1%')
      ```

      Copy
    * EXCLUDE filters out column names that don’t match the specified column or columns. For example:

      ```
      (* EXCLUDE col1)

      (* EXCLUDE (col1, col2))
      ```

      Copy

    Qualifiers are valid when you use these keywords. The following example uses the ILIKE keyword to
    filter for all of the columns that match the pattern `col1%` in the table `mytable`:

    ```
    (mytable.* ILIKE 'col1%')
    ```

    Copy

    The ILIKE and EXCLUDE keywords can’t be combined in a single function call.

    For this function, the ILIKE and EXCLUDE keywords are valid only in a SELECT list or GROUP BY clause.

    For more information about the ILIKE and EXCLUDE keywords, see the “Parameters” section in [SELECT](../sql/select).

## Returns[¶](#returns "Link to this heading")

Returns a signed 64-bit value as NUMBER(19,0).

HASH never returns NULL, even for NULL inputs.

## Usage notes[¶](#usage-notes "Link to this heading")

* HASH is stable in the sense that it guarantees:

  + Any two values of type NUMBER that compare equally will hash to the same hash value, even if the
    respective types have different precision and/or scale.
  + Any two values of type FLOAT that can be converted to NUMBER(38, 0) without loss of precision will
    hash to the same value. For example, the following all return the same hash value:

    - `HASH(10::NUMBER(38,0))`
    - `HASH(10::NUMBER(5,3))`
    - `HASH(10::FLOAT)`
  + Any two values of type TIMESTAMP\_TZ that compare equally will hash to the same hash value, even if
    the timestamps are from different time zones.
  + This guarantee also applies to NUMBER, FLOAT, and TIMESTAMP\_TZ values within a VARIANT column.
  + Note that this guarantee does not apply to other combinations of types, even if implicit conversions exist
    between the types. For example, with overwhelming probability, the following will not return the same hash values
    even though `10 = '10'` after implicit conversion:

    - `HASH(10)`
    - `HASH('10')`
* `HASH(*)` means to create a single hashed value based on all columns in the row.
* Do not use HASH to create unique keys. HASH has a finite resolution of 64 bits, and is guaranteed to return
  non-unique values if more than 2^64 values are entered (e.g. for a table with more than 2^64 rows). In practice, if
  the input is on the order of 2^32 rows (approximately 4 billion rows) or more, the function is reasonably likely
  to return at least one duplicate value.

## Collation details[¶](#collation-details "Link to this heading")

No impact.

* Two strings that are identical but have different collation specifications have the same hash value. In other words,
  only the string, not the collation specification, affects the hash value.
* Two strings that are different, but compare equal according to a collation, might have a different hash value. For
  example, two strings that are identical using punctuation-insensitive collation will normally have different hash
  values because only the string, not the collation specification, affects the hash value.

## Examples[¶](#examples "Link to this heading")

```
SELECT HASH(SEQ8()) FROM TABLE(GENERATOR(rowCount=>10));
```

Copy

```
+----------------------+
|         HASH(SEQ8()) |
|----------------------|
| -6076851061503311999 |
| -4730168494964875235 |
| -3690131753453205264 |
| -7287585996956442977 |
| -1285360004004520191 |
|  4801857165282451853 |
| -2112898194861233169 |
|  1885958945512144850 |
| -3994946021335987898 |
| -3559031545629922466 |
+----------------------+
```

```
SELECT HASH(10), HASH(10::number(38,0)), HASH(10::number(5,3)), HASH(10::float);
```

Copy

```
+---------------------+------------------------+-----------------------+---------------------+
|            HASH(10) | HASH(10::NUMBER(38,0)) | HASH(10::NUMBER(5,3)) |     HASH(10::FLOAT) |
|---------------------+------------------------+-----------------------+---------------------|
| 1599627706822963068 |    1599627706822963068 |   1599627706822963068 | 1599627706822963068 |
+---------------------+------------------------+-----------------------+---------------------+
```

```
SELECT HASH(10), HASH('10');
```

Copy

```
+---------------------+---------------------+
|            HASH(10) |          HASH('10') |
|---------------------+---------------------|
| 1599627706822963068 | 3622494980440108984 |
+---------------------+---------------------+
```

```
SELECT HASH(null), HASH(null, null), HASH(null, null, null);
```

Copy

```
+---------------------+--------------------+------------------------+
|          HASH(NULL) |   HASH(NULL, NULL) | HASH(NULL, NULL, NULL) |
|---------------------+--------------------+------------------------|
| 8817975702393619368 | 953963258351104160 |    2941948363845684412 |
+---------------------+--------------------+------------------------+
```

The example below shows that even if the table contains multiple columns, `HASH(*)` returns a single value per row.

```
CREATE TABLE orders (order_ID INTEGER, customer_ID INTEGER, order_date ...);

...

SELECT HASH(*) FROM orders LIMIT 10;
```

Copy

```
+-----------------------+
|        HASH(*)        |
|-----------------------|
|  -3527903796973745449 |
|  6296330861892871310  |
|  6918165900200317484  |
|  -2762842444336053314 |
|  -2340602249668223387 |
|  5248970923485160358  |
|  -5807737826218607124 |
|  428973568495579456   |
|  2583438210124219420  |
|  4041917286051184231  |
+ ----------------------+
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