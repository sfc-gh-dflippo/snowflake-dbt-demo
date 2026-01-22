---
auto_generated: true
description: Data generation functions
last_scraped: '2026-01-14T16:56:44.494343+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/seq1.html
title: SEQ1 / SEQ2 / SEQ4 / SEQ8 | Snowflake Documentation
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

     + Random
     + [RANDOM](random.md)
     + [RANDSTR](randstr.md)
     + [UUID\_STRING](uuid_string.md)
     + Controlled distribution
     + [NORMAL](normal.md)
     + [UNIFORM](uniform.md)
     + [ZIPF](zipf.md)
     + [SEQ1](seq1.md)
     + [SEQ2](seq1.md)
     + [SEQ4](seq1.md)
     + [SEQ8](seq1.md)
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

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)[Data generation](../functions-data-generation.md)SEQ1

Categories:
:   [Data generation functions](../functions-data-generation)

# SEQ1 / SEQ2 / SEQ4 / SEQ8[¶](#seq1-seq2-seq4-seq8 "Link to this heading")

Returns a sequence of monotonically increasing integers, with wrap-around. Wrap-around occurs after the largest representable integer of the integer width (1, 2, 4, or 8 byte).

Important

This function uses sequences to produce a unique set of increasing integers, but does not necessarily produce a gap-free sequence. When operating on a large quantity of data, gaps can
appear in a sequence. If a fully ordered, gap-free sequence is required, consider using the [ROW\_NUMBER](row_number) window function.

For more details about sequences in Snowflake, see [Using Sequences](../../user-guide/querying-sequences).

## Syntax[¶](#syntax "Link to this heading")

```
SEQ1( [0|1] )

SEQ2( [0|1] )

SEQ4( [0|1] )

SEQ8( [0|1] )
```

Copy

## Usage notes[¶](#usage-notes "Link to this heading")

* If the optional sign argument is 0, the sequence continues at 0 after wrap-around. If the optional sign argument is 1, the sequence continues at the smallest representable number based
  on the given integer width.
* The default sign argument is 0.

## Examples[¶](#examples "Link to this heading")

These are basic examples of using sequences:

> ```
> SELECT seq8() FROM table(generator(rowCount => 5));
>
> +--------+
> | SEQ8() |
> |--------|
> |      0 |
> |      1 |
> |      2 |
> |      3 |
> |      4 |
> +--------+
> ```
>
> Copy
>
> ```
> SELECT * FROM (SELECT seq2(0), seq1(1) FROM table(generator(rowCount => 132))) ORDER BY seq2(0) LIMIT 7 OFFSET 125;
>
> +---------+---------+
> | SEQ2(0) | SEQ1(1) |
> |---------+---------|
> |     125 |     125 |
> |     126 |     126 |
> |     127 |     127 |
> |     128 |    -128 |
> |     129 |    -127 |
> |     130 |    -126 |
> |     131 |    -125 |
> +---------+---------+
> ```
>
> Copy

This example shows how to use ROW\_NUMBER to generate a sequence without gaps:

> ```
> SELECT ROW_NUMBER() OVER (ORDER BY seq4()) 
>     FROM TABLE(generator(rowcount => 10));
> +-------------------------------------+
> | ROW_NUMBER() OVER (ORDER BY SEQ4()) |
> |-------------------------------------|
> |                                   1 |
> |                                   2 |
> |                                   3 |
> |                                   4 |
> |                                   5 |
> |                                   6 |
> |                                   7 |
> |                                   8 |
> |                                   9 |
> |                                  10 |
> +-------------------------------------+
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
2. [Usage notes](#usage-notes)
3. [Examples](#examples)