---
auto_generated: true
description: Conditional expression functions
last_scraped: '2026-01-14T16:57:18.753113+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/iff.html
title: IFF | Snowflake Documentation
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

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)[Conditional expression](../expressions-conditional.md)IFF

Categories:
:   [Conditional expression functions](../expressions-conditional)

# IFF[¶](#iff "Link to this heading")

Returns one of two values depending on whether a Boolean expression evaluates to true or false.
This function is similar to a single-level `if-then-else` expression. It is similar to [CASE](case),
but only allows a single condition. You can use it to add conditional logic to SQL statements.

## Syntax[¶](#syntax "Link to this heading")

```
IFF( <condition> , <expr1> , <expr2> )
```

Copy

## Arguments[¶](#arguments "Link to this heading")

`condition`
:   The condition is an expression that should evaluate to a BOOLEAN value
    (TRUE, FALSE, or NULL).

    If `condition` evaluates to TRUE, returns `expr1`, otherwise
    returns `expr2`.

`expr1`
:   A general expression. The function returns this value if the `condition`
    is true.

`expr2`
:   A general expression. The function returns this value if the `condition`
    is not true (that is, if it is false or NULL).

## Returns[¶](#returns "Link to this heading")

This function can return a value of any type. The function can return NULL if the value of the
expression that is returned is NULL.

## Usage notes[¶](#usage-notes "Link to this heading")

The `condition` can include a SELECT statement containing set
operators, such as UNION, INTERSECT, and EXCEPT (MINUS). When using set operators,
make sure that data types are compatible. For details, see the [General usage notes](../operators-query.html#label-operators-query-general-usage-notes)
in the [Set operators](../operators-query) topic.

## Collation details[¶](#collation-details "Link to this heading")

The value returned from the function retains the collation specification of the
highest-[precedence](../collation.html#label-determining-the-collation-used-in-an-operation) collation
of the `expr1` and `expr2` arguments.

## Examples[¶](#examples "Link to this heading")

The following examples use the `IFF` function.

Return `expr1` because the condition evaluates to true:

```
SELECT IFF(TRUE, 'true', 'false');
```

Copy

```
+----------------------------+
| IFF(TRUE, 'TRUE', 'FALSE') |
|----------------------------|
| true                       |
+----------------------------+
```

Return `expr2` because the condition evaluates to false:

```
SELECT IFF(FALSE, 'true', 'false');
```

Copy

```
+-----------------------------+
| IFF(FALSE, 'TRUE', 'FALSE') |
|-----------------------------|
| false                       |
+-----------------------------+
```

Return `expr2` because the condition evaluates to NULL:

```
SELECT IFF(NULL, 'true', 'false');
```

Copy

```
+----------------------------+
| IFF(NULL, 'TRUE', 'FALSE') |
|----------------------------|
| false                      |
+----------------------------+
```

Return NULL because the value of the expression returned is NULL:

```
SELECT IFF(TRUE, NULL, 'false');
```

Copy

```
+--------------------------+
| IFF(TRUE, NULL, 'FALSE') |
|--------------------------|
| NULL                     |
+--------------------------+
```

Return `expr1` (`integer`) if the value is an integer, or return
`expr2` (`non-integer`) if the value is not an integer:

```
SELECT value, IFF(value::INT = value, 'integer', 'non-integer')
  FROM ( SELECT column1 AS value
           FROM VALUES(1.0), (1.1), (-3.1415), (-5.000), (NULL) )
  ORDER BY value DESC;
```

Copy

```
+---------+---------------------------------------------------+
|   VALUE | IFF(VALUE::INT = VALUE, 'INTEGER', 'NON-INTEGER') |
|---------+---------------------------------------------------|
|    NULL | non-integer                                       |
|  1.1000 | non-integer                                       |
|  1.0000 | integer                                           |
| -3.1415 | non-integer                                       |
| -5.0000 | integer                                           |
+---------+---------------------------------------------------+
```

Return `expr1` (`High`) if the value is greater than 50, or return
`expr2` (`Low`) if the value is 50 or lower (or NULL):

```
SELECT value, IFF(value > 50, 'High', 'Low')
FROM ( SELECT column1 AS value
         FROM VALUES(22), (63), (5), (99), (NULL) );
```

Copy

```
+-------+--------------------------------+
| VALUE | IFF(VALUE > 50, 'HIGH', 'LOW') |
|-------+--------------------------------|
|    22 | Low                            |
|    63 | High                           |
|     5 | Low                            |
|    99 | High                           |
|  NULL | Low                            |
+-------+--------------------------------+
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