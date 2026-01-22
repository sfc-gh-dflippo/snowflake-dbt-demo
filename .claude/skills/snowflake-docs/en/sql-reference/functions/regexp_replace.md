---
auto_generated: true
description: String functions (regular expressions)
last_scraped: '2026-01-14T16:56:51.656908+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/regexp_replace
title: REGEXP_REPLACE | Snowflake Documentation
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

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)[Regular expressions](../functions-regexp.md)REGEXP\_REPLACE

Categories:
:   [String functions (regular expressions)](../functions-regexp)

# REGEXP\_REPLACE[¶](#regexp-replace "Link to this heading")

Returns the subject with the specified pattern — or all occurrences of the pattern — either removed
or replaced by a replacement string.

## Syntax[¶](#syntax "Link to this heading")

```
 REGEXP_REPLACE( <subject> ,
                 <pattern>
                   [ , <replacement>
                     [ , <position>
                       [ , <occurrence>
                         [ , <parameters> ]
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

`replacement`
:   String that replaces the substrings matched by the pattern. If an empty string is specified, the function removes all matched patterns and returns the resulting string.

    Default: `''` (empty string).

`position`
:   Number of characters from the beginning of the string where the function starts searching for matches.
    The value must be a positive integer.

    Default: `1` (the search for a match starts at the first character on the left)

`occurrence`
:   Specifies which occurrence of the pattern to replace. If `0` is specified, all occurrences are replaced.

    Default: `0` (all occurrences)

`parameters`
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

## Returns[¶](#returns "Link to this heading")

Returns a value of type VARCHAR.

If no matches are found, returns the original subject.

Returns NULL if any argument is NULL.

## Usage notes[¶](#usage-notes "Link to this heading")

* The replacement string can contain backreferences to capture groups; for example, sub-expressions of the pattern. A capture group is a regular expression that is enclosed within parentheses (`( )`). The maximum number of capture groups is nine.

  Backreferences match expressions inside a capture group. Backreferences have the form `n` where `n` is a value from 0 to 9, inclusive, which refers to the matching instance of the capture group. For more information, see [Examples](#examples) (in this topic).
* Parentheses (`( )`) and square brackets (`[ ]`) currently must be double-escaped to parse them as literal strings.

  The example below shows how to remove parentheses:

  ```
  SELECT REGEXP_REPLACE('Customers - (NY)','\\(|\\)','') AS customers;
  ```

  Copy

  ```
  +----------------+
  | CUSTOMERS      |
  |----------------|
  | Customers - NY |
  +----------------+
  ```
* For additional usage notes, see the [General usage notes](../functions-regexp.html#label-regexp-general-usage-notes) for regular expression functions.

## Collation details[¶](#collation-details "Link to this heading")

Arguments with collation specifications currently aren’t supported.

## Examples[¶](#examples "Link to this heading")

The following example replaces all spaces in the string with nothing (that is, all spaces are removed):

```
SELECT REGEXP_REPLACE('It was the best of times, it was the worst of times',
                      '( ){1,}',
                      '') AS result;
```

Copy

```
+------------------------------------------+
| RESULT                                   |
|------------------------------------------|
| Itwasthebestoftimes,itwastheworstoftimes |
+------------------------------------------+
```

The following example matches the string `times` and replaces it with the string `days`. Matching begins at the first
character in the string and replaces the second occurrence of the substring:

```
SELECT REGEXP_REPLACE('It was the best of times, it was the worst of times',
                      'times',
                      'days',
                      1,
                      2) AS result;
```

Copy

```
+----------------------------------------------------+
| RESULT                                             |
|----------------------------------------------------|
| It was the best of times, it was the worst of days |
+----------------------------------------------------+
```

The following example uses backreferences to rearrange the string `firstname middlename lastname` as
`lastname, firstname middlename` and insert a comma between `lastname` and `firstname`:

```
SELECT REGEXP_REPLACE('firstname middlename lastname',
                      '(.*) (.*) (.*)',
                      '\\3, \\1 \\2') AS name_sort;
```

Copy

```
+--------------------------------+
| NAME_SORT                      |
|--------------------------------|
| lastname, firstname middlename |
+--------------------------------+
```

The remaining examples use the data in the following table:

```
CREATE OR REPLACE TABLE regexp_replace_demo(body VARCHAR(255));

INSERT INTO regexp_replace_demo values
  ('Hellooo World'),
  ('How are you doing today?'),
  ('the quick brown fox jumps over the lazy dog'),
  ('PACK MY BOX WITH FIVE DOZEN LIQUOR JUGS');
```

Copy

The following example inserts the character `*` between every character of the subject, including the beginning and the end,
using an empty group (`()`), which finds a match between any two characters:

```
SELECT body,
       REGEXP_REPLACE(body, '()', '*') AS replaced
  FROM regexp_replace_demo;
```

Copy

```
+---------------------------------------------+-----------------------------------------------------------------------------------------+
| BODY                                        | REPLACED                                                                                |
|---------------------------------------------+-----------------------------------------------------------------------------------------|
| Hellooo World                               | *H*e*l*l*o*o*o* *W*o*r*l*d*                                                             |
| How are you doing today?                    | *H*o*w* *a*r*e* *y*o*u* *d*o*i*n*g* *t*o*d*a*y*?*                                       |
| the quick brown fox jumps over the lazy dog | *t*h*e* *q*u*i*c*k* *b*r*o*w*n* *f*o*x* *j*u*m*p*s* *o*v*e*r* *t*h*e* *l*a*z*y* *d*o*g* |
| PACK MY BOX WITH FIVE DOZEN LIQUOR JUGS     | *P*A*C*K* *M*Y* *B*O*X* *W*I*T*H* *F*I*V*E* *D*O*Z*E*N* *L*I*Q*U*O*R* *J*U*G*S*         |
+---------------------------------------------+-----------------------------------------------------------------------------------------+
```

The following example removes all of the vowels by replacing them with nothing, regardless of their order or case:

```
SELECT body,
       REGEXP_REPLACE(body, '[aeiou]', '', 1, 0, 'i') AS replaced
  FROM regexp_replace_demo;
```

Copy

```
+---------------------------------------------+----------------------------------+
| BODY                                        | REPLACED                         |
|---------------------------------------------+----------------------------------|
| Hellooo World                               | Hll Wrld                         |
| How are you doing today?                    | Hw r y dng tdy?                  |
| the quick brown fox jumps over the lazy dog | th qck brwn fx jmps vr th lzy dg |
| PACK MY BOX WITH FIVE DOZEN LIQUOR JUGS     | PCK MY BX WTH FV DZN LQR JGS     |
+---------------------------------------------+----------------------------------+
```

The following example removes all words that contain the lowercase letter `o` from the subject by matching
a word boundary (`\b`), followed by zero or more word characters (`\S`), the letter `o`, and then zero or more
word characters until the next word boundary:

```
SELECT body,
       REGEXP_REPLACE(body, '\\b(\\S*)o(\\S*)\\b') AS replaced
  FROM regexp_replace_demo;
```

Copy

```
+---------------------------------------------+-----------------------------------------+
| BODY                                        | REPLACED                                |
|---------------------------------------------+-----------------------------------------|
| Hellooo World                               |                                         |
| How are you doing today?                    |  are   ?                                |
| the quick brown fox jumps over the lazy dog | the quick   jumps  the lazy             |
| PACK MY BOX WITH FIVE DOZEN LIQUOR JUGS     | PACK MY BOX WITH FIVE DOZEN LIQUOR JUGS |
+---------------------------------------------+-----------------------------------------+
```

The following example replaces all words that contain the lowercase letter `o`, swapping
the letters in front of and behind the first instance of `o`, and replacing the `o` with the character
sequence `@@`:

```
SELECT body,
       REGEXP_REPLACE(body, '\\b(\\S*)o(\\S*)\\b', '\\2@@\\1') AS replaced
  FROM regexp_replace_demo;
```

Copy

```
+---------------------------------------------+-------------------------------------------------+
| BODY                                        | REPLACED                                        |
|---------------------------------------------+-------------------------------------------------|
| Hellooo World                               | @@Helloo rld@@W                                 |
| How are you doing today?                    | w@@H are u@@y ing@@d day@@t?                    |
| the quick brown fox jumps over the lazy dog | the quick wn@@br x@@f jumps ver@@ the lazy g@@d |
| PACK MY BOX WITH FIVE DOZEN LIQUOR JUGS     | PACK MY BOX WITH FIVE DOZEN LIQUOR JUGS         |
+---------------------------------------------+-------------------------------------------------+
```

The following example is the same as the previous example, but the replacement starts at position `3` in the subject:

```
SELECT body,
       REGEXP_REPLACE(body, '\\b(\\S*)o(\\S*)\\b', '\\2@@\\1', 3) AS replaced
  FROM regexp_replace_demo;
```

Copy

```
+---------------------------------------------+-------------------------------------------------+
| BODY                                        | REPLACED                                        |
|---------------------------------------------+-------------------------------------------------|
| Hellooo World                               | He@@lloo rld@@W                                 |
| How are you doing today?                    | How are u@@y ing@@d day@@t?                     |
| the quick brown fox jumps over the lazy dog | the quick wn@@br x@@f jumps ver@@ the lazy g@@d |
| PACK MY BOX WITH FIVE DOZEN LIQUOR JUGS     | PACK MY BOX WITH FIVE DOZEN LIQUOR JUGS         |
+---------------------------------------------+-------------------------------------------------+
```

The following example is the same as the previous example, but only the third occurrence is replaced, starting at position
`3` in the subject:

```
SELECT body,
       REGEXP_REPLACE(body, '\\b(\\S*)o(\\S*)\\b', '\\2@@\\1', 3, 3) AS replaced
  FROM regexp_replace_demo;
```

Copy

```
+---------------------------------------------+----------------------------------------------+
| BODY                                        | REPLACED                                     |
|---------------------------------------------+----------------------------------------------|
| Hellooo World                               | Hellooo World                                |
| How are you doing today?                    | How are you doing day@@t?                    |
| the quick brown fox jumps over the lazy dog | the quick brown fox jumps ver@@ the lazy dog |
| PACK MY BOX WITH FIVE DOZEN LIQUOR JUGS     | PACK MY BOX WITH FIVE DOZEN LIQUOR JUGS      |
+---------------------------------------------+----------------------------------------------+
```

The following example is the same as the previous example, but it uses case-insensitive matching:

```
SELECT body,
       REGEXP_REPLACE(body, '\\b(\\S*)o(\\S*)\\b', '\\2@@\\1', 3, 3, 'i') AS replaced
  FROM regexp_replace_demo;
```

Copy

```
+---------------------------------------------+----------------------------------------------+
| BODY                                        | REPLACED                                     |
|---------------------------------------------+----------------------------------------------|
| Hellooo World                               | Hellooo World                                |
| How are you doing today?                    | How are you doing day@@t?                    |
| the quick brown fox jumps over the lazy dog | the quick brown fox jumps ver@@ the lazy dog |
| PACK MY BOX WITH FIVE DOZEN LIQUOR JUGS     | PACK MY BOX WITH FIVE DOZEN R@@LIQU JUGS     |
+---------------------------------------------+----------------------------------------------+
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