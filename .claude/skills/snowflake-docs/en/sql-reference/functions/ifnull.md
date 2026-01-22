---
auto_generated: true
description: Conditional expression functions
last_scraped: '2026-01-14T16:54:39.491258+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/ifnull
title: IFNULL | Snowflake Documentation
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

     + [[NOT] BETWEEN](/en/sql-reference/functions/between "[NOT] BETWEEN")
     + [BOOLAND](booland.md)
     + [BOOLNOT](boolnot.md)
     + [BOOLOR](boolor.md)
     + [BOOLXOR](boolxor.md)
     + [CASE](case.md)
     + [COALESCE](coalesce.md)
     + [DECODE](decode.md)
     + [EQUAL\_NULL](equal_null.md)
     + [GREATEST](greatest.md)
     + [GREATEST\_IGNORE\_NULLS](greatest_ignore_nulls.md)
     + [IFF](iff.md)
     + [IFNULL](ifnull.md)
     + [[NOT] IN](/en/sql-reference/functions/in "[NOT] IN")
     + [IS [NOT] DISTINCT FROM](/en/sql-reference/functions/is-distinct-from "IS [NOT] DISTINCT FROM")
     + [IS [NOT] NULL](/en/sql-reference/functions/is-null "IS [NOT] NULL")
     + [IS\_NULL\_VALUE](is_null_value.md)
     + [LEAST](least.md)
     + [LEAST\_IGNORE\_NULLS](least_ignore_nulls.md)
     + [NULLIF](nullif.md)
     + [NULLIFZERO](nullifzero.md)
     + [NVL](nvl.md)
     + [NVL2](nvl2.md)
     + [REGR\_VALX](regr_valx.md)
     + [REGR\_VALY](regr_valy.md)
     + [ZEROIFNULL](zeroifnull.md)
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

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)[Conditional expression](../expressions-conditional.md)IFNULL

Categories:
:   [Conditional expression functions](../expressions-conditional)

# IFNULL[¶](#ifnull "Link to this heading")

If `expr1` is NULL, returns `expr2`, otherwise returns `expr1`.

Aliases:
:   [NVL](nvl)

## Syntax[¶](#syntax "Link to this heading")

```
IFNULL( <expr1> , <expr2> )
```

Copy

## Arguments[¶](#arguments "Link to this heading")

`expr1`
:   A general expression.

`expr2`
:   A general expression.

## Usage notes[¶](#usage-notes "Link to this heading")

* Snowflake performs [implicit conversion](../data-type-conversion.html#label-when-coercion-occurs) of arguments to make
  them compatible. For example, if one of the input expressions is a numeric type, the return type
  is also a numeric type. That is, `SELECT IFNULL('17', 1);` first converts the VARCHAR value `'17'`
  to the NUMBER value `17`, and then returns the first non-NULL value.

  When conversion isn’t possible, implicit conversion fails. For example, `SELECT IFNULL('foo', 1);`
  returns an error because the VARCHAR value `'foo'` can’t be converted to a NUMBER value.

  We recommend passing in arguments of the same type or explicitly converting arguments if needed.

* When implicit conversion converts a non-numeric value to a numeric value, the result is a value
  of type NUMBER(18,5).

  For numeric string arguments that aren’t constants, if NUMBER(18,5) isn’t sufficient to represent
  the numeric value, then [cast](../data-type-conversion.html#label-data-type-explicit-casting) the argument to a type that
  can represent the value.

* Either expression can include a `SELECT` statement containing set
  operators, such as `UNION`, `INTERSECT`, `EXCEPT`, and `MINUS`.
  When using set operators, make sure that data types are compatible. For
  details, see the [General usage notes](../operators-query.html#label-operators-query-general-usage-notes) in the
  [Set operators](../operators-query) topic.

## Collation details[¶](#collation-details "Link to this heading")

* The [collation specifications](../collation.html#label-collation-specification) of all input arguments must be compatible.
* The collation of the result of the function is the highest-[precedence](../collation.html#label-determining-the-collation-used-in-an-operation) collation of the inputs.

## Returns[¶](#returns "Link to this heading")

Returns the data type of the returned expression.

If both expressions are NULL, returns NULL.

## Examples[¶](#examples "Link to this heading")

Create a table that contains contact information for suppliers:

```
CREATE TABLE IF NOT EXISTS suppliers (
  supplier_id INT PRIMARY KEY,
  supplier_name VARCHAR(30),
  phone_region_1 VARCHAR(15),
  phone_region_2 VARCHAR(15));
```

Copy

The table contains the phone number for each supplier in two different regions. The phone number can
be NULL for a region.

Insert values into the table:

```
INSERT INTO suppliers(supplier_id, supplier_name, phone_region_1, phone_region_2)
  VALUES(1, 'Company_ABC', NULL, '555-01111'),
        (2, 'Company_DEF', '555-01222', NULL),
        (3, 'Company_HIJ', '555-01333', '555-01444'),
        (4, 'Company_KLM', NULL, NULL);
```

Copy

The following SELECT statement uses the IFNULL function to
retrieve the `phone_region_1` and `phone_region_2` values.

This example shows the following results for the IFNULL function:

* The `IF_REGION_1_NULL` column contains the value in `phone_region_1` or, if that value is NULL, the
  value in `phone_region_2`.
* The `IF_REGION_2_NULL` column contains the value in `phone_region_2` or, if that value is NULL, the
  value in `phone_region_1`.
* If both `phone_region_1` and `phone_region_2` are NULL, the function returns NULL.

```
SELECT supplier_id,
       supplier_name,
       phone_region_1,
       phone_region_2,
       IFNULL(phone_region_1, phone_region_2) IF_REGION_1_NULL,
       IFNULL(phone_region_2, phone_region_1) IF_REGION_2_NULL
  FROM suppliers
  ORDER BY supplier_id;
```

Copy

```
+-------------+---------------+----------------+----------------+------------------+------------------+
| SUPPLIER_ID | SUPPLIER_NAME | PHONE_REGION_1 | PHONE_REGION_2 | IF_REGION_1_NULL | IF_REGION_2_NULL |
|-------------+---------------+----------------+----------------+------------------+------------------|
|           1 | Company_ABC   | NULL           | 555-01111      | 555-01111        | 555-01111        |
|           2 | Company_DEF   | 555-01222      | NULL           | 555-01222        | 555-01222        |
|           3 | Company_HIJ   | 555-01333      | 555-01444      | 555-01333        | 555-01444        |
|           4 | Company_KLM   | NULL           | NULL           | NULL             | NULL             |
+-------------+---------------+----------------+----------------+------------------+------------------+
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
4. [Collation details](#collation-details)
5. [Returns](#returns)
6. [Examples](#examples)