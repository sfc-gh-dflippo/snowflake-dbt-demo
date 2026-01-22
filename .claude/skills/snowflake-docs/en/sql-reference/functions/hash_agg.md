---
auto_generated: true
description: Aggregate functions , Window functions
last_scraped: '2026-01-14T16:57:54.740481+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/hash_agg
title: HASH_AGG | Snowflake Documentation
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

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)[Hash](../functions-hash-scalar.md)HASH\_AGG

Categories:
:   [Aggregate functions](../functions-aggregation) , [Window functions](../functions-window)

# HASH\_AGG[¶](#hash-agg "Link to this heading")

Returns an aggregate signed 64-bit hash value over the (unordered) set of input rows. HASH\_AGG never returns NULL, even if no input is provided. Empty input “hashes” to `0`.

One use for aggregate hash functions is to detect changes to a set of values without comparing the individual old and new values. HASH\_AGG can compute a single hash value
based on many inputs; almost any change to one of the inputs is likely to result in a change to the output of the HASH\_AGG function. Comparing two lists of values typically
requires sorting both lists, but HASH\_AGG produces the same value regardless of the order of the inputs. Because the values don’t need to be sorted for HASH\_AGG,
performance is typically much faster.

Note

HASH\_AGG is *not* a cryptographic hash function and should not be used as such.

For cryptographic purposes, use the SHA family of functions (in [String & binary functions](../functions-string)).

See also:
:   [HASH](hash)

## Syntax[¶](#syntax "Link to this heading")

**Aggregate function**

```
HASH_AGG( [ DISTINCT ] <expr> [ , <expr2> ... ] )

HASH_AGG(*)
```

Copy

**Window function**

```
HASH_AGG( [ DISTINCT ] <expr> [ , <expr2> ... ] ) OVER ( [ PARTITION BY <expr3> ] )

HASH_AGG(*) OVER ( [ PARTITION BY <expr3> ] )
```

Copy

## Arguments[¶](#arguments "Link to this heading")

`exprN`
:   The expression can be a general expression of any Snowflake data type, except
    [GEOGRAPHY](../data-types-geospatial.html#label-data-types-geography) and [GEOMETRY](../data-types-geospatial.html#label-data-types-geometry).

`expr2`
:   You can include additional expressions.

`expr3`
:   The column to partition on, if you want the result to be split into multiple
    windows.

`*`
:   Returns an aggregated hash value over all columns for all records, including records with
    NULL values. You can specify the wildcard for both the aggregate function and the window
    function.

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

HASH\_AGG never returns NULL, even for NULL inputs.

## Usage notes[¶](#usage-notes "Link to this heading")

* HASH\_AGG computes a “fingerprint” over an entire table, query result, or window. Any change to the input will
  influence the result of HASH\_AGG with overwhelming probability. This can be used to quickly detect changes to table
  contents or query results.

  Note that it is possible, though very unlikely, that two different input tables will produce the same result for HASH\_AGG. If you need to make sure that two tables or query results that
  produce the same HASH\_AGG result really contain the same data, you must still compare the data for equality (for example, by using the MINUS operator). For more details, see
  [Set operators](../operators-query).
* HASH\_AGG is *not* order-sensitive (that is, the order of rows in an input table or query result does not influence the result of HASH\_AGG). However, changing the order of input columns
  *does* change the result.
* HASH\_AGG hashes individual input rows using the [HASH](hash) function. The salient features of this function carry over to HASH\_AGG. In particular, HASH\_AGG is “stable” in the sense
  that any two rows that compare as equal and have compatible types are guaranteed to hash to the same value (that is, they influence the result of HASH\_AGG in the same way).

  For example, changing the scale and precision of a column that is part of some table doesn’t change the result of HASH\_AGG over that table. See [HASH](hash) for details.
* In contrast to most other aggregate functions, HASH\_AGG doesn’t ignore NULL inputs (that is, NULL inputs influence the result of HASH\_AGG).
* For both the aggregate function and the window function, duplicate rows, including duplicate all-NULL rows,
  influence the result. The DISTINCT keyword can be used to suppress the effect of duplicate rows.

* When this function is called as a window function, it does not support:

  + An ORDER BY clause within the OVER clause.
  + Explicit window frames.

## Collation details[¶](#collation-details "Link to this heading")

* Two strings that are identical but have different collation specifications have the same hash value. In other words,
  only the string, not the collation specification, affects the hash value.
* Two strings that are different, but compare as equal according to a collation, might have a different hash value. For
  example, two strings that are identical using punctuation-insensitive collation normally have different hash
  values because only the string, not the collation specification, affects the hash value.

## Examples[¶](#examples "Link to this heading")

This example shows that NULLs are not ignored:

```
SELECT HASH_AGG(NULL), HASH_AGG(NULL, NULL), HASH_AGG(NULL, NULL, NULL);
```

Copy

```
+----------------------+----------------------+----------------------------+
|       HASH_AGG(NULL) | HASH_AGG(NULL, NULL) | HASH_AGG(NULL, NULL, NULL) |
|----------------------+----------------------+----------------------------|
| -5089618745711334219 |  2405106413361157177 |       -5970411136727777524 |
+----------------------+----------------------+----------------------------+
```

This example shows that empty input hashes to `0`:

```
SELECT HASH_AGG(NULL) WHERE 0 = 1;
```

Copy

```
+----------------+
| HASH_AGG(NULL) |
|----------------|
|              0 |
+----------------+
```

Use HASH\_AGG(\*) to conveniently aggregate over all input columns:

```
SELECT HASH_AGG(*) FROM orders;
```

Copy

```
+---------------------+
|     HASH_AGG(*)     |
|---------------------|
| 1830986524994392080 |
+---------------------+
```

This example shows that grouped aggregation is supported:

```
SELECT YEAR(o_orderdate), HASH_AGG(*)
  FROM ORDERS GROUP BY 1 ORDER BY 1;
```

Copy

```
+-------------------+----------------------+
| YEAR(O_ORDERDATE) |     HASH_AGG(*)      |
|-------------------+----------------------|
| 1992              | 4367993187952496263  |
| 1993              | 7016955727568565995  |
| 1994              | -2863786208045652463 |
| 1995              | 1815619282444629659  |
| 1996              | -4747088155740927035 |
| 1997              | 7576942849071284554  |
| 1998              | 4299551551435117762  |
+-------------------+----------------------+
```

This example suppresses duplicate rows using DISTINCT (duplicate rows influence results of HASH\_AGG):

```
SELECT YEAR(o_orderdate), HASH_AGG(o_custkey, o_orderdate)
  FROM orders GROUP BY 1 ORDER BY 1;
```

Copy

```
+-------------------+----------------------------------+
| YEAR(O_ORDERDATE) | HASH_AGG(O_CUSTKEY, O_ORDERDATE) |
|-------------------+----------------------------------|
| 1992              | 5686635209456450692              |
| 1993              | -6250299655507324093             |
| 1994              | 6630860688638434134              |
| 1995              | 6010861038251393829              |
| 1996              | -767358262659738284              |
| 1997              | 6531729365592695532              |
| 1998              | 2105989674377706522              |
+-------------------+----------------------------------+
```

```
SELECT YEAR(o_orderdate), HASH_AGG(DISTINCT o_custkey, o_orderdate)
  FROM orders GROUP BY 1 ORDER BY 1;
```

Copy

```
+-------------------+-------------------------------------------+
| YEAR(O_ORDERDATE) | HASH_AGG(DISTINCT O_CUSTKEY, O_ORDERDATE) |
|-------------------+-------------------------------------------|
| 1992              | -8416988862307613925                      |
| 1993              | 3646533426281691479                       |
| 1994              | -7562910554240209297                      |
| 1995              | 6413920023502140932                       |
| 1996              | -3176203653000722750                      |
| 1997              | 4811642075915950332                       |
| 1998              | 1919999828838507836                       |
+-------------------+-------------------------------------------+
```

This example computes the number of days on which the corresponding sets of customers with orders with status not equal `'F'` and status not equal `'P'`, respectively, are identical:

```
SELECT COUNT(DISTINCT o_orderdate) FROM orders;
```

Copy

```
+-----------------------------+
| COUNT(DISTINCT O_ORDERDATE) |
|-----------------------------|
| 2406                        |
+-----------------------------+
```

```
SELECT COUNT(o_orderdate)
  FROM (SELECT o_orderdate, HASH_AGG(DISTINCT o_custkey)
    FROM orders
    WHERE o_orderstatus <> 'F'
    GROUP BY 1
    INTERSECT
      SELECT o_orderdate, HASH_AGG(DISTINCT o_custkey)
        FROM orders
        WHERE o_orderstatus <> 'P'
        GROUP BY 1);
```

Copy

```
+--------------------+
| COUNT(O_ORDERDATE) |
|--------------------|
| 1143               |
+--------------------+
```

The query doesn’t account for the possibility of hash collisions, so the actual number of days might be slightly lower.

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