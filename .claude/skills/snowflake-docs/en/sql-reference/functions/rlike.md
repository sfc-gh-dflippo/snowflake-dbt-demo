---
auto_generated: true
description: String functions (regular expressions)
last_scraped: '2026-01-14T16:56:53.009072+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/rlike
title: '[ NOT ] RLIKE | Snowflake Documentation'
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

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)[Regular expressions](../functions-regexp.md)[ NOT ] RLIKE

Categories:
:   [String functions (regular expressions)](../functions-regexp)

# [ NOT ] RLIKE[¶](#not-rlike "Link to this heading")

Performs a comparison to determine whether a string matches or does not match a specified pattern. Both inputs must be text expressions.

RLIKE is similar to the [[ NOT ] LIKE](like) function, but with POSIX extended regular expressions instead of SQL LIKE pattern syntax.
It supports more complex matching conditions than LIKE.

Tip

You can use the search optimization service to improve the performance of queries that call this function.
For details, see [Search optimization service](../../user-guide/search-optimization-service).

Aliases:
:   [[ NOT ] REGEXP](regexp) (2nd syntax) , [REGEXP\_LIKE](regexp_like) (1st syntax)

See also: [String functions (regular expressions)](../functions-regexp)

> [REGEXP\_COUNT](regexp_count) , [REGEXP\_INSTR](regexp_instr) , [REGEXP\_REPLACE](regexp_replace) , [REGEXP\_SUBSTR](regexp_substr) , [REGEXP\_SUBSTR\_ALL](regexp_substr_all)
>
> [[ NOT ] ILIKE](ilike) , [[ NOT ] LIKE](like)

## Syntax[¶](#syntax "Link to this heading")

```
-- 1st syntax
RLIKE( <subject> , <pattern> [ , <parameters> ] )

-- 2nd syntax
<subject> [ NOT ] RLIKE <pattern>
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

Returns a BOOLEAN or NULL.

* When RLIKE is specified, the value is TRUE if there is a match. Otherwise, returns FALSE.
* When NOT RLIKE is specified, the value is TRUE if there is no match. Otherwise, returns FALSE.
* When either RLIKE or NOT RLIKE is specified, returns NULL if any argument is NULL.

## Usage Notes[¶](#usage-notes "Link to this heading")

* The function implicitly anchors a pattern at both ends (for example, `''` automatically becomes `'^$'`, and `'ABC'`
  automatically becomes `'^ABC$'`). For example, to match any string starting with `ABC`, the pattern is `'ABC.*'`.
* The backslash character (`\`) is the escape character. For more information, see [Specifying regular expressions in single-quoted string constants](../functions-regexp.html#label-regexp-escape-character-caveats).
* For more usage notes, see the [General usage notes](../functions-regexp.html#label-regexp-general-usage-notes) for regular expression functions.

## Collation Details[¶](#collation-details "Link to this heading")

Arguments with collation specifications currently aren’t supported.

## Examples[¶](#examples "Link to this heading")

Run the following commands to set up the data for the examples in this topic:

```
CREATE OR REPLACE TABLE rlike_ex(city VARCHAR(20));
INSERT INTO rlike_ex VALUES ('Sacramento'), ('San Francisco'), ('San Jose'), (null);
```

Copy

### Examples that use the first syntax[¶](#examples-that-use-the-first-syntax "Link to this heading")

The following examples perform case-insensitive pattern matching with wildcards:

```
SELECT * FROM rlike_ex WHERE RLIKE(city, 'san.*', 'i');
```

Copy

```
+---------------+
| CITY          |
|---------------|
| San Francisco |
| San Jose      |
+---------------+
```

```
SELECT * FROM rlike_ex WHERE NOT RLIKE(city, 'san.*', 'i');
```

Copy

```
+------------+
| CITY       |
|------------|
| Sacramento |
+------------+
```

The following examples determine if a string matches the format of a phone number and an email address.
In these examples, the regular expressions are specified in [dollar-quoted strings](../data-types-text.html#label-dollar-quoted-string-constants)
to avoid escaping the backslashes in the regular expression.

```
SELECT RLIKE('800-456-7891',
             $$[2-9]\d{2}-\d{3}-\d{4}$$) AS matches_phone_number;
```

Copy

```
+----------------------+
| MATCHES_PHONE_NUMBER |
|----------------------|
| True                 |
+----------------------+
```

```
SELECT RLIKE('jsmith@email.com',
             $$\w+@[a-zA-Z_]+\.[a-zA-Z]{2,3}$$) AS matches_email_address;
```

Copy

```
+-----------------------+
| MATCHES_EMAIL_ADDRESS |
|-----------------------|
| True                  |
+-----------------------+
```

The following examples perform the same matches but use
[single-quoted string constants](../data-types-text.html#label-single-quoted-string-constants) to specify the regular expressions.

Because the example uses single-quoted string constants,
[each backslash must be escaped with another backslash](../functions-regexp.html#label-regexp-escape-character-caveats).

```
SELECT RLIKE('800-456-7891',
             '[2-9]\\d{2}-\\d{3}-\\d{4}') AS matches_phone_number;
```

Copy

```
+----------------------+
| MATCHES_PHONE_NUMBER |
|----------------------|
| True                 |
+----------------------+
```

```
SELECT RLIKE('jsmith@email.com',
             '\\w+@[a-zA-Z_]+\\.[a-zA-Z]{2,3}') AS matches_email_address;
```

Copy

```
+-----------------------+
| MATCHES_EMAIL_ADDRESS |
|-----------------------|
| True                  |
+-----------------------+
```

Alternatively, rewrite the statements and avoid sequences that rely on the backslash character.

```
SELECT RLIKE('800-456-7891',
             '[2-9][0-9]{2}-[0-9]{3}-[0-9]{4}') AS matches_phone_number;
```

Copy

```
+----------------------+
| MATCHES_PHONE_NUMBER |
|----------------------|
| True                 |
+----------------------+
```

```
SELECT RLIKE('jsmith@email.com',
             '[a-zA-Z_]+@[a-zA-Z_]+\\.[a-zA-Z]{2,3}') AS matches_email_address;
```

Copy

```
+-----------------------+
| MATCHES_EMAIL_ADDRESS |
|-----------------------|
| True                  |
+-----------------------+
```

### Examples that use the second syntax[¶](#examples-that-use-the-second-syntax "Link to this heading")

The following example performs case-insensitive pattern matching with wildcards:

```
SELECT * FROM rlike_ex WHERE city RLIKE 'San.* [fF].*';
```

Copy

```
+---------------+
| CITY          |
|---------------|
| San Francisco |
+---------------+
```

### Additional examples[¶](#additional-examples "Link to this heading")

For additional examples of regular expressions, see [[ NOT ] REGEXP](regexp).

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
4. [Usage Notes](#usage-notes)
5. [Collation Details](#collation-details)
6. [Examples](#examples)