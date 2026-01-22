---
auto_generated: true
description: Conditional expression functions
last_scraped: '2026-01-14T16:57:33.277475+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/case.html
title: CASE | Snowflake Documentation
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

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)[Conditional expression](../expressions-conditional.md)CASE

Categories:
:   [Conditional expression functions](../expressions-conditional)

# CASE[¶](#case "Link to this heading")

Works like a cascading “if-then-else” statement. In the more general form,
a series of conditions are evaluated in sequence. When a condition evaluates
to TRUE, the evaluation stops and the associated result (after THEN) is
returned. If none of the conditions evaluate to TRUE, then the result after
the optional ELSE is returned, if present; otherwise NULL is returned.

In the second, “shorthand” form, the expression after CASE is compared to
each of the WHEN expressions in sequence, until one matches; then the
associated result (after THEN) is returned. If none of the expressions
match, the result after the optional ELSE is returned, if present;
otherwise NULL is returned.

Note that in the second form, a NULL CASE expression matches none of
the WHEN expressions, even if one of the WHEN expressions is also NULL.

See also:
:   [IFF](iff)

## Syntax[¶](#syntax "Link to this heading")

```
CASE
    WHEN <condition1> THEN <result1>
  [ WHEN <condition2> THEN <result2> ]
  [ ... ]
  [ ELSE <result3> ]
END

CASE <expr>
    WHEN <value1> THEN <result1>
  [ WHEN <value2> THEN <result2> ]
  [ ... ]
  [ ELSE <result3> ]
END
```

Copy

## Arguments[¶](#arguments "Link to this heading")

`condition#`
:   In the first form of `CASE`, each condition is an expression that
    should evaluate to a BOOLEAN value (True, False, or NULL).

`expr`
:   A general expression.

`value`
:   In the second form of `CASE`, each `value` is a potential match
    for `expr`. The `value` can be a literal or an expression.
    The `value` must be the same data type as the `expr`, or
    must be a data type that can be cast to the data type of the `expr`.

`result#`
:   In the first form of the `CASE` clause, if `condition#` is true,
    then the function returns the corresponding `result#`. If more than
    one condition is true, then the result associated with the first true
    condition is returned.

    In the second form of the `CASE` statement, if `value#` matches the
    `expr`, then the corresponding `result` is returned. If more
    than one `value` matches the `expr`, then the first matching
    value’s `result` is returned.

    The result should be an expression that evaluates to a single value.

    In both forms of `CASE`, if the optional `ELSE` clause is present, and
    if no matches are found, then the function returns the result in the
    `ELSE` clause. If no `ELSE` clause is present, and no matches are found,
    then the result is NULL.

## Usage notes[¶](#usage-notes "Link to this heading")

* Note that, contrary to [DECODE](decode), a NULL value in the condition
  does not match a NULL value elsewhere in the condition.
  For example `WHEN <null_expr> = NULL THEN 'Return me!'` does not
  return “Return me!”. If you want to compare to NULL values, use
  `IS NULL` rather than `= NULL`.
* The `condition#`, `expr`, `value`, and
  `result` can all be general expressions and thus can include
  subqueries that include set operators, such
  as `UNION`, `INTERSECT`, `EXCEPT`, and `MINUS`.
  When using set operators, make sure that data types are compatible. For
  details, see the [General usage notes](../operators-query.html#label-operators-query-general-usage-notes) in the
  [Set operators](../operators-query) topic.

## Collation details[¶](#collation-details "Link to this heading")

In the first form of `CASE`, each expression is independent, and the collation specifications in different
branches are independent. For example, in the following, the collation specifications in
`condition1` are independent of the collation specification(s) in `condition2`,
and those collation specifications do not need to be identical or even compatible.

```
CASE
    WHEN <condition1> THEN <result1>
  [ WHEN <condition2> THEN <result2> ]
```

Copy

In the second form of `CASE`, although all collation-related operations must use compatible collation specifications,
the collation specifications do not need to be identical. For example, in the following statement, the collation
specifications of both `value1` and `value2` must be compatible with the collation specification of
`expr`, but the collation specifications of `value1` and `value2` do not need to be identical
to each other or to the collation specification of `expr`.

> ```
> CASE <expr>
>     WHEN <value1> THEN <result1>
>   [ WHEN <value2> THEN <result2> ]
>   ...
> ```
>
> Copy

The value returned from the function has the
highest-[precedence](../collation.html#label-determining-the-collation-used-in-an-operation) collation of the `THEN`/`ELSE`
arguments.

## Examples[¶](#examples "Link to this heading")

This example shows a typical use of CASE:

```
SELECT
    column1,
    CASE
        WHEN column1=1 THEN 'one'
        WHEN column1=2 THEN 'two'
        ELSE 'other'
    END AS result
FROM (values(1),(2),(3)) v;
```

Copy

```
+---------+--------+
| COLUMN1 | RESULT |
|---------+--------|
|       1 | one    |
|       2 | two    |
|       3 | other  |
+---------+--------+
```

This example shows that if none of the values match, and there is no ELSE clause,
then the value returned is NULL:

```
SELECT
    column1,
    CASE
        WHEN column1=1 THEN 'one'
        WHEN column1=2 THEN 'two'
    END AS result
FROM (values(1),(2),(3)) v;
```

Copy

```
+---------+--------+
| COLUMN1 | RESULT |
|---------+--------|
|       1 | one    |
|       2 | two    |
|       3 | NULL   |
+---------+--------+
```

This example handles NULL explicitly.

```
SELECT
    column1,
    CASE 
        WHEN column1 = 1 THEN 'one'
        WHEN column1 = 2 THEN 'two'
        WHEN column1 IS NULL THEN 'NULL'
        ELSE 'other'
    END AS result
FROM VALUES (1), (2), (NULL);
```

Copy

```
+---------+--------+
| COLUMN1 | RESULT |
|---------+--------|
|       1 | one    |
|       2 | two    |
|    NULL | NULL   |
+---------+--------+
```

The following examples combine CASE with collation:

```
SELECT CASE COLLATE('m', 'upper')
    WHEN 'M' THEN TRUE
    ELSE FALSE
END;
```

Copy

```
+----------------------------+
| CASE COLLATE('M', 'UPPER') |
|     WHEN 'M' THEN TRUE     |
|     ELSE FALSE             |
| END                        |
|----------------------------|
| True                       |
+----------------------------+
```

```
SELECT CASE 'm'
    WHEN COLLATE('M', 'lower') THEN TRUE
    ELSE FALSE
END;
```

Copy

```
+------------------------------------------+
| CASE 'M'                                 |
|     WHEN COLLATE('M', 'LOWER') THEN TRUE |
|     ELSE FALSE                           |
| END                                      |
|------------------------------------------|
| True                                     |
+------------------------------------------+
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
5. [Examples](#examples)