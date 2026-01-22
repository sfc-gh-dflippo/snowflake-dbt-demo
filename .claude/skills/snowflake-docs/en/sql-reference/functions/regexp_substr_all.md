---
auto_generated: true
description: String functions (regular expressions)
last_scraped: '2026-01-14T16:56:15.636462+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/regexp_substr_all
title: REGEXP_SUBSTR_ALL | Snowflake Documentation
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

     + [[ NOT ] REGEXP](/en/sql-reference/functions/regexp "[ NOT ] REGEXP")
     + [REGEXP\_COUNT](regexp_count.md)
     + [REGEXP\_EXTRACT\_ALL](regexp_substr_all.md)
     + [REGEXP\_INSTR](regexp_instr.md)
     + [REGEXP\_LIKE](regexp_like.md)
     + [REGEXP\_REPLACE](regexp_replace.md)
     + [REGEXP\_SUBSTR](regexp_substr.md)
     + [REGEXP\_SUBSTR\_ALL](regexp_substr_all.md)
     + [[ NOT ] RLIKE](/en/sql-reference/functions/rlike "[ NOT ] RLIKE")
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

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)[Regular expressions](../functions-regexp.md)REGEXP\_SUBSTR\_ALL

Categories:
:   [String functions (regular expressions)](../functions-regexp)

# REGEXP\_SUBSTR\_ALL[¶](#regexp-substr-all "Link to this heading")

Returns an [ARRAY](../data-types-semistructured.html#label-data-type-array) that contains all substrings that match a
[regular expression](../functions-regexp) within a string.

Aliases:
:   REGEXP\_EXTRACT\_ALL

## Syntax[¶](#syntax "Link to this heading")

```
REGEXP_SUBSTR_ALL( <subject> ,
                   <pattern>
                     [ , <position>
                       [ , <occurrence>
                         [ , <regex_parameters>
                           [ , <group_num> ]
                         ]
                       ]
                     ]
)
```

Copy

## Arguments[¶](#arguments "Link to this heading")

**Required:**

`subject`
:   The string to search for matches.

`pattern`
:   Pattern to match.

    For guidelines on specifying patterns, see [String functions (regular expressions)](../functions-regexp).

**Optional:**

`position`
:   Number of characters from the beginning of the string where the function starts searching for matches.
    The value must be a positive integer.

    Default: `1` (the search for a match starts at the first character on the left)

`occurrence`
:   Specifies the first occurrence of the pattern from which to start returning matches.

    The function skips the first `occurrence - 1` matches. For example, if there are 5 matches and
    you specify `3` for the `occurrence` argument, the function ignores the first two matches and
    returns the third, fourth, and fifth matches.

    Default: `1`

`regex_parameters`
:   String of one or more characters that specifies the parameters used for searching for matches. Supported values:

    | Parameter | Description |
    | --- | --- |
    | `c` | Case-sensitive matching |
    | `i` | Case-insensitive matching |
    | `m` | Multi-line mode |
    | `e` | Extract submatches |
    | `s` | Single-line mode POSIX wildcard character `.` matches `\n` |

    Default: `c`

    For more information, see [Specifying the parameters for the regular expression](../functions-regexp.html#label-regexp-parameters-argument).

    Note

    By default, REGEXP\_SUBSTR\_ALL returns the entire matching part of the subject.
    However, if the `e` parameter is specified, REGEXP\_SUBSTR\_ALL returns the
    part of the subject that matches the first group in the pattern.
    If `e` is specified but a `group_num` is not also specified, then the `group_num`
    defaults to 1 (the first group). If there is no sub-expression in the pattern, REGEXP\_SUBSTR\_ALL behaves as
    if `e` was not set. For examples that use `e`, see [Examples](#examples) in this topic.

`group_num`
:   Specifies which group to extract. Groups are specified by using parentheses in
    the regular expression.

    If a `group_num` is specified, Snowflake allows extraction even if the `'e'` option was not
    also specified. The `'e'` is implied.

    Snowflake supports up to 1024 groups.

    For examples that use `group_num`, see the [Examples](#examples) in this topic.

## Returns[¶](#returns "Link to this heading")

The function returns a value of type ARRAY. The array contains an element for each matching substring.

The function returns an empty array if no match is found.

The function returns NULL in the following cases:

* Any argument is NULL.
* You specify `group_num` and the pattern doesn’t specify a grouping with that number. For example, if the
  pattern specifies only one group (for example, `a(b)c`), and you use `2` as `group_num`, the function returns
  NULL.

## Usage notes[¶](#usage-notes "Link to this heading")

For additional information on using regular expressions, see [String functions (regular expressions)](../functions-regexp).

## Collation details[¶](#collation-details "Link to this heading")

Arguments with collation specifications currently aren’t supported.

## Examples[¶](#examples "Link to this heading")

The pattern in the following example matches a lowercase “a” followed by a digit. The example returns an ARRAY that contains all
of the matches:

```
SELECT REGEXP_SUBSTR_ALL('a1_a2a3_a4A5a6', 'a[[:digit:]]') AS matches;
```

Copy

```
+---------+
| MATCHES |
|---------|
| [       |
|   "a1", |
|   "a2", |
|   "a3", |
|   "a4", |
|   "a6"  |
| ]       |
+---------+
```

The following example starts finding matches from the second character in the string (`2`):

```
SELECT REGEXP_SUBSTR_ALL('a1_a2a3_a4A5a6', 'a[[:digit:]]', 2) AS matches;
```

Copy

```
+---------+
| MATCHES |
|---------|
| [       |
|   "a2", |
|   "a3", |
|   "a4", |
|   "a6"  |
| ]       |
+---------+
```

The following example starts returning matches from the third occurrence of the pattern in the string (`3`):

```
SELECT REGEXP_SUBSTR_ALL('a1_a2a3_a4A5a6', 'a[[:digit:]]', 1, 3) AS matches;
```

Copy

```
+---------+
| MATCHES |
|---------|
| [       |
|   "a3", |
|   "a4", |
|   "a6"  |
| ]       |
+---------+
```

The following example performs a case-insensitive match (`i`):

```
SELECT REGEXP_SUBSTR_ALL('a1_a2a3_a4A5a6', 'a[[:digit:]]', 1, 1, 'i') AS matches;
```

Copy

```
+---------+
| MATCHES |
|---------|
| [       |
|   "a1", |
|   "a2", |
|   "a3", |
|   "a4", |
|   "A5", |
|   "a6"  |
| ]       |
+---------+
```

The following example performs a case-insensitive match and returns the part of the string that matches the first group (`ie`):

```
SELECT REGEXP_SUBSTR_ALL('a1_a2a3_a4A5a6', '(a)([[:digit:]])', 1, 1, 'ie') AS matches;
```

Copy

```
+---------+
| MATCHES |
|---------|
| [       |
|   "a",  |
|   "a",  |
|   "a",  |
|   "a",  |
|   "A",  |
|   "a"   |
| ]       |
+---------+
```

The following example demonstrates that the function returns an empty array when no matches are found:

```
SELECT REGEXP_SUBSTR_ALL('a1_a2a3_a4A5a6', 'b') AS matches;
```

Copy

```
+---------+
| MATCHES |
|---------|
| []      |
+---------+
```

This example shows how to retrieve each second word in a string from the first, second, and third
matches of a two-word pattern in which the first word is `A`.

First, create a table and insert data:

```
CREATE OR REPLACE TABLE test_regexp_substr_all (string1 VARCHAR);;
INSERT INTO test_regexp_substr_all (string1) VALUES ('A MAN A PLAN A CANAL');
```

Copy

Run the query:

```
SELECT REGEXP_SUBSTR_ALL(string1, 'A\\W+(\\w+)', 1, 1, 'e', 1) AS result1,
       REGEXP_SUBSTR_ALL(string1, 'A\\W+(\\w+)', 1, 2, 'e', 1) AS result2,
       REGEXP_SUBSTR_ALL(string1, 'A\\W+(\\w+)', 1, 3, 'e', 1) AS result3
  FROM test_regexp_substr_all;
```

Copy

```
+-----------+-----------+-----------+
| RESULT1   | RESULT2   | RESULT3   |
|-----------+-----------+-----------|
| [         | [         | [         |
|   "MAN",  |   "PLAN", |   "CANAL" |
|   "PLAN", |   "CANAL" | ]         |
|   "CANAL" | ]         |           |
| ]         |           |           |
+-----------+-----------+-----------+
```

This example shows how to retrieve the first, second, and third groups within each occurrence of the pattern
in a string. In this case, the returned values are each individual letter of each matched word in each group.

```
SELECT REGEXP_SUBSTR_ALL(string1, 'A\\W+(\\w)(\\w)(\\w)', 1, 1, 'e', 1) AS result1,
       REGEXP_SUBSTR_ALL(string1, 'A\\W+(\\w)(\\w)(\\w)', 1, 1, 'e', 2) AS result2,
       REGEXP_SUBSTR_ALL(string1, 'A\\W+(\\w)(\\w)(\\w)', 1, 1, 'e', 3) AS result3
  FROM test_regexp_substr_all;
```

Copy

```
+---------+---------+---------+
| RESULT1 | RESULT2 | RESULT3 |
|---------+---------+---------|
| [       | [       | [       |
|   "M",  |   "A",  |   "N",  |
|   "P",  |   "L",  |   "A",  |
|   "C"   |   "A"   |   "N"   |
| ]       | ]       | ]       |
+---------+---------+---------+
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

Related content

1. [String functions (regular expressions)](/sql-reference/functions/../functions-regexp)
2. [REGEXP\_SUBSTR](/sql-reference/functions/regexp_substr)