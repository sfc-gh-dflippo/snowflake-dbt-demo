---
auto_generated: true
description: These string functions perform operations that match a regular expression
  (often referred to as a “regex”).
last_scraped: '2026-01-14T16:57:09.490995+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions-regexp.html
title: String functions (regular expressions) | Snowflake Documentation
---

1. [Overview](../reference.md)
2. [SQL data types reference](../sql-reference-data-types.md)
3. [SQL command reference](../sql-reference-commands.md)
4. [Function and stored procedure reference](../sql-reference-functions.md)

   * [Summary of functions](intro-summary-operators-functions.md)
   * [All functions (alphabetical)](functions-all.md)")
   * [Aggregate](functions-aggregation.md)
   * AI Functions

     * Scalar functions

       * [AI\_CLASSIFY](functions/ai_classify.md)
       * [AI\_COMPLETE](functions/ai_complete.md)
       * [AI\_COUNT\_TOKENS](functions/ai_count_tokens.md)
       * [AI\_EMBED](functions/ai_embed.md)
       * [AI\_EXTRACT](functions/ai_extract.md)
       * [AI\_FILTER](functions/ai_filter.md)
       * [AI\_PARSE\_DOCUMENT](functions/ai_parse_document.md)
       * [AI\_REDACT](functions/ai_redact.md)
       * [AI\_SENTIMENT](functions/ai_sentiment.md)
       * [AI\_SIMILARITY](functions/ai_similarity.md)
       * [AI\_TRANSCRIBE](functions/ai_transcribe.md)
       * [AI\_TRANSLATE](functions/ai_translate.md)
       * [CLASSIFY\_TEXT (SNOWFLAKE.CORTEX)](functions/classify_text-snowflake-cortex.md)")
       * [COMPLETE (SNOWFLAKE.CORTEX)](functions/complete-snowflake-cortex.md)")
       * [COMPLETE multimodal (images) (SNOWFLAKE.CORTEX)](functions/complete-snowflake-cortex-multimodal.md) (SNOWFLAKE.CORTEX)")
       * [EMBED\_TEXT\_768 (SNOWFLAKE.CORTEX)](functions/embed_text-snowflake-cortex.md)")
       * [EMBED\_TEXT\_1024 (SNOWFLAKE.CORTEX)](functions/embed_text_1024-snowflake-cortex.md)")
       * [ENTITY\_SENTIMENT (SNOWFLAKE.CORTEX)](functions/entity_sentiment-snowflake-cortex.md)")
       * [EXTRACT\_ANSWER (SNOWFLAKE.CORTEX)](functions/extract_answer-snowflake-cortex.md)")
       * [FINETUNE (SNOWFLAKE.CORTEX)](functions/finetune-snowflake-cortex.md)")
       * [PARSE\_DOCUMENT (SNOWFLAKE.CORTEX)](functions/parse_document-snowflake-cortex.md)")
       * [SENTIMENT (SNOWFLAKE.CORTEX)](functions/sentiment-snowflake-cortex.md)")
       * [SUMMARIZE (SNOWFLAKE.CORTEX)](functions/summarize-snowflake-cortex.md)")
       * [TRANSLATE (SNOWFLAKE.CORTEX)](functions/translate-snowflake-cortex.md)")
     * Aggregate functions

       * [AI\_AGG](functions/ai_agg.md)
       * [AI\_SUMMARIZE\_AGG](functions/ai_summarize_agg.md)
     * Helper functions

       * [COUNT\_TOKENS (SNOWFLAKE.CORTEX)](functions/count_tokens-snowflake-cortex.md)")
       * [SEARCH\_PREVIEW (SNOWFLAKE.CORTEX)](functions/search_preview-snowflake-cortex.md)")
       * [SPLIT\_TEXT\_MARKDOWN\_HEADER (SNOWFLAKE.CORTEX)](functions/split_text_markdown_header-snowflake-cortex.md)")
       * [SPLIT\_TEXT\_RECURSIVE\_CHARACTER (SNOWFLAKE.CORTEX)](functions/split_text_recursive_character-snowflake-cortex.md)")
       * [TRY\_COMPLETE (SNOWFLAKE.CORTEX)](functions/try_complete-snowflake-cortex.md)")
   * [Bitwise expression](expressions-byte-bit.md)
   * [Conditional expression](expressions-conditional.md)
   * [Context](functions-context.md)
   * [Conversion](functions-conversion.md)
   * [Data generation](functions-data-generation.md)
   * [Data metric](functions-data-metric.md)
   * [Date & time](functions-date-time.md)
   * [Differential privacy](functions-differential-privacy.md)
   * [Encryption](functions-encryption.md)
   * [File](functions-file.md)
   * [Geospatial](functions-geospatial.md)
   * [Hash](functions-hash-scalar.md)
   * [Metadata](functions-metadata.md)
   * [ML Model Monitors](functions-model-monitors.md)
   * [Notification](functions-notification.md)
   * [Numeric](functions-numeric.md)
   * [Organization users and organization user groups](functions-organization-users.md)
   * [Regular expressions](functions-regexp.md)

     + [[ NOT ] REGEXP](/en/sql-reference/functions/regexp "[ NOT ] REGEXP")
     + [REGEXP\_COUNT](functions/regexp_count.md)
     + [REGEXP\_EXTRACT\_ALL](functions/regexp_substr_all.md)
     + [REGEXP\_INSTR](functions/regexp_instr.md)
     + [REGEXP\_LIKE](functions/regexp_like.md)
     + [REGEXP\_REPLACE](functions/regexp_replace.md)
     + [REGEXP\_SUBSTR](functions/regexp_substr.md)
     + [REGEXP\_SUBSTR\_ALL](functions/regexp_substr_all.md)
     + [[ NOT ] RLIKE](/en/sql-reference/functions/rlike "[ NOT ] RLIKE")
   * [Semi-structured and structured data](functions-semistructured.md)
   * [Snowpark Container Services](functions-spcs.md)
   * [String & binary](functions-string.md)
   * [System](functions-system.md)
   * [Table](functions-table.md)
   * [Vector](functions-vector.md)
   * [Window](functions-window.md)
   * [Stored procedures](../sql-reference-stored-procedures.md)
5. [Class reference](../sql-reference-classes.md)
6. [Scripting reference](../sql-reference-snowflake-scripting.md)
7. [General reference](../sql-reference.md)
8. [API reference](../api-reference.md)

[Reference](../reference.md)[Function and stored procedure reference](../sql-reference-functions.md)Regular expressions

# String functions (regular expressions)[¶](#string-functions-regular-expressions "Link to this heading")

These string functions perform operations that match a regular expression (often referred to as a “regex”).

## List of regex functions[¶](#list-of-regex-functions "Link to this heading")

| Function | Notes |
| --- | --- |
| [[ NOT ] REGEXP](functions/regexp) | Alias for RLIKE. |
| [REGEXP\_COUNT](functions/regexp_count) |  |
| [REGEXP\_EXTRACT\_ALL](functions/regexp_substr_all) | Alias for REGEXP\_SUBSTR\_ALL. |
| [REGEXP\_INSTR](functions/regexp_instr) |  |
| [REGEXP\_LIKE](functions/regexp_like) | Alias for RLIKE. |
| [REGEXP\_REPLACE](functions/regexp_replace) |  |
| [REGEXP\_SUBSTR](functions/regexp_substr) |  |
| [REGEXP\_SUBSTR\_ALL](functions/regexp_substr_all) |  |
| [[ NOT ] RLIKE](functions/rlike) |  |

## General usage notes[¶](#general-usage-notes "Link to this heading")

In these notes, “subject” refers to the string to operate on and “pattern” refers to the regular expression:

* The subject is typically a variable column, while the pattern is typically a constant, but this is not required; every argument
  to a regular expression function can be either a constant or variable.
* Patterns support the most of the POSIX ERE (Extended Regular Expression) syntax. For details, see the
  [POSIX basic and extended](http://en.wikipedia.org/wiki/Regular_expression#POSIX_basic_and_extended) section (in Wikipedia).

  One exception is that the regular expression functions don’t support non-greedy quantifiers, for example `*?`, `??`,
  and `+?`.
* Patterns also support the following Perl backslash-sequences:

  + `\d`: decimal digit (0-9).
  + `\D`: not a decimal digit.
  + `\s`: whitespace character.
  + `\S`: not a whitespace character.
  + `\w`: “word” character (a-z, A-Z, underscore (“\_”), or decimal digit).
  + `\W`: not a word character.
  + `\b`: word boundary.
  + `\B`: not a word boundary.

  For details, see the [Character classes](http://en.wikipedia.org/wiki/Regular_expression#Character_classes) section (in Wikipedia) or the
  [Backslash sequences](http://perldoc.perl.org/perlrecharclass.html#Backslash-sequences) section (in the Perl documentation).

  Note

  In [single-quoted string constants](data-types-text.html#label-single-quoted-string-constants), you must escape the backslash character in
  the backslash-sequence. For example, to specify `\d`, use `\\d`. For details, see
  [Specifying regular expressions in single-quoted string constants](#label-regexp-escape-character-caveats) (in this topic).

  You do not need to escape backslashes if you are delimiting the string with
  [pairs of dollar signs ($$)](data-types-text.html#label-dollar-quoted-string-constants) (rather than single quotes).
* By default, the POSIX wildcard character `.` (in the pattern) does not include newline characters `\n` (in the subject) as matches.

  To also match newline characters, either replace `.` with `(.|\n)` in the `pattern` argument, or use the `s` parameter in the `parameters` argument (described
  below).
* All the regular expression functions support Unicode. A single Unicode character always counts as one character (that is, the POSIX meta-character `.` matches exactly one Unicode character),
  regardless of the byte-length of the corresponding binary representation of that character. Also, for functions that take or return subject offsets, a single Unicode character counts as 1.

## Specifying the parameters for the regular expression[¶](#specifying-the-parameters-for-the-regular-expression "Link to this heading")

Most regular expression functions support an optional `parameters` argument. The `parameters` argument is a VARCHAR string that specifies the matching
behavior of the regular expression function. The following parameters are supported:

| Parameter | Description |
| --- | --- |
| `c` | Enables case-sensitive matching. |
| `i` | Enables case-insensitive matching. |
| `m` | Enables multi-line mode (that is, meta-characters `^` and `$` mark the beginning and end of any line of the subject). By default, multi-line mode is disabled (that is, `^` and `$` mark the beginning and end of the entire subject). |
| `e` | Extracts submatches; applies only to [REGEXP\_INSTR](functions/regexp_instr), [REGEXP\_SUBSTR](functions/regexp_substr), [REGEXP\_SUBSTR\_ALL](functions/regexp_substr_all), and the aliases for these functions. |
| `s` | Enables the POSIX wildcard character `.` to match `\n`. By default, wildcard character matching is disabled. |

The default string is `c`, which specifies:

* Case-sensitive matching.
* Single-line mode.
* No submatch extraction, except for [REGEXP\_REPLACE](functions/regexp_replace), which always uses submatch extraction.
* POSIX wildcard character `.` does not match `\n` newline characters.

When specifying multiple parameters, enter the string with no spaces or delimiters.
For example, `ims` specifies case-insensitive matching in multi-line mode with POSIX wildcard matching.

If both `c` and `i` are included in the `parameters` string, the one that occurs last in the string dictates whether the function performs case-sensitive or case-insensitive
matching. For example, `ci` specifies case-insensitive matching because the `i` occurs last in the string.

The following example shows how the results can be different for case-sensitive and case-insensitive matching.
The [REGEXP\_COUNT](functions/regexp_count) function returns no matches for `snow` and `SNOW` for case-sensitive matching (`c` parameter,
the default) and one match for case-insensitive matching (`i` parameter):

```
SELECT REGEXP_COUNT('snow', 'SNOW', 1, 'c') AS case_sensitive_matching,
       REGEXP_COUNT('snow', 'SNOW', 1, 'i') AS case_insensitive_matching;
```

Copy

```
+-------------------------+---------------------------+
| CASE_SENSITIVE_MATCHING | CASE_INSENSITIVE_MATCHING |
|-------------------------+---------------------------|
|                       0 |                         1 |
+-------------------------+---------------------------+
```

Use the [REGEXP\_SUBSTR](functions/regexp_substr) function with the `e` parameter to look for the word
`Release`, followed by one or more non-word characters, followed by one or more digits, and then return
the substring that matches the digits:

```
SELECT REGEXP_SUBSTR('Release 24', 'Release\\W+(\\d+)', 1, 1, 'e') AS release_number;
```

Copy

```
+----------------+
| RELEASE_NUMBER |
|----------------|
| 24             |
+----------------+
```

For more examples that use parameters, see [REGEXP\_INSTR](functions/regexp_instr), [REGEXP\_LIKE](functions/regexp_like),
[REGEXP\_SUBSTR](functions/regexp_substr), [REGEXP\_SUBSTR\_ALL](functions/regexp_substr_all), and [[ NOT ] RLIKE](functions/rlike).

## Matching characters that are metacharacters[¶](#matching-characters-that-are-metacharacters "Link to this heading")

In regular expressions, some characters are treated as metacharacters that have a specific meaning. For example:

* `.` is a
  [metacharacter that matches any single character](https://en.wikipedia.org/wiki/Regular_expression#POSIX_basic_and_extended).
* `*` is a [quantifier](https://en.wikipedia.org/wiki/Regular_expression#Basic_concepts) that matches zero or more instances
  of the preceding element. For example, `BA*` matches `B`, `BA`, `BAA`, and so on.
* `?` is a quantifier that matches zero or one instance of the preceding element.

To match the actual character (for example, an actual period, asterisk, or question mark), you must escape the metacharacter with a
backslash (for example, `\.`, `\*`, `\?`, and so on).

Note

If you are using the regular expression in a [single-quoted string constant](data-types-text.html#label-single-quoted-string-constants),
you must escape the backslash with a second backslash (for example, `\\.`, `\\*`, `\\?`, and so on). For details, see
[Specifying regular expressions in single-quoted string constants](#label-regexp-escape-character-caveats)

For example, suppose that you need to find an open parenthesis (`(`) in a string. One way to specify this is to use a backslash
to escape the character in the pattern (for example, `\(`).

If you are specifying the pattern as a [single-quoted string constant](data-types-text.html#label-single-quoted-string-constants), you must also
[escape that backslash with a second backslash](data-types-text.html#label-single-quoted-string-constants-escape-sequences).

The following pattern matches a sequence of alphanumeric characters that appear inside parentheses (for example, `(NY)`):

```
SELECT REGEXP_SUBSTR('Customers - (NY)','\\([[:alnum:]]+\\)') AS location;
```

Copy

```
+----------+
| LOCATION |
|----------|
| (NY)     |
+----------+
```

For additional examples, see [Example of using metacharacters in a single-quoted string constant](#label-regexp-escape-character-caveats-metacharacter).

Note that you do not need to escape the backslash character if you are using a
[dollar-quoted string constant](data-types-text.html#label-dollar-quoted-string-constants):

```
SELECT REGEXP_SUBSTR('Customers - (NY)',$$\([[:alnum:]]+\)$$) AS location;
```

Copy

```
+----------+
| LOCATION |
|----------|
| (NY)     |
+----------+
```

## Using backreferences[¶](#using-backreferences "Link to this heading")

Snowflake does not support backreferences in regular expression patterns (known as “squares” in formal language theory); however, backreferences are supported in the replacement string of the
[REGEXP\_REPLACE](functions/regexp_replace) function.

## Specifying an empty pattern[¶](#specifying-an-empty-pattern "Link to this heading")

In most regexp functions, an empty pattern (that is, `''`) matches nothing, not even an empty subject.

The exceptions are [REGEXP\_LIKE](functions/regexp_like) and its aliases [[ NOT ] REGEXP](functions/regexp) and [[ NOT ] RLIKE](functions/rlike),
in which the empty pattern matches the empty subject because the pattern is implicitly anchored at both ends
(that is, `''` automatically becomes `'^$'`).

An empty group (that is, subexpression `()`), matches the space in between characters, including the beginning and end of the subject.

## Specifying regular expressions in dollar-quoted string constants[¶](#specifying-regular-expressions-in-dollar-quoted-string-constants "Link to this heading")

If you are using a string constant to specify the regular expression for a function, you can use a
[dollar-quoted string constant](data-types-text.html#label-dollar-quoted-string-constants) to avoid
[escaping the backslash characters in the regular expression](#label-regexp-escape-character-caveats). (If you are using
[single-quoted string constants](data-types-text.html#label-single-quoted-string-constants), you need to escape the backslashes.)

The content of a dollar-quoted string constant is always interpreted literally.

For example, when escaping a [metacharacter](#label-regex-metacharacter), you only need to use a single backslash:

```
SELECT w2
  FROM wildcards
  WHERE REGEXP_LIKE(w2, $$\?$$);
```

Copy

When using a [backreference](#label-regex-backreferences), you only need to use a single backslash:

```
SELECT w2, REGEXP_REPLACE(w2, '(.old)', $$very \1$$)
  FROM wildcards
  ORDER BY w2;
```

Copy

## Specifying regular expressions in single-quoted string constants[¶](#specifying-regular-expressions-in-single-quoted-string-constants "Link to this heading")

If you are using a regular expression in a [single-quoted string constant](data-types-text.html#label-single-quoted-string-constants), you must
escape any backslashes in [backslash-sequences](#label-regexp-general-usage-notes) with a second backslash.

Note

To avoid escaping backslashes in a regular expression, you can use a
[dollar-quoted string constant](#label-regexp-double-dollar-sign-strings), rather than a single-quoted string constant.

For example:

* If you are [escaping a metacharacter](#label-regex-metacharacter) with a backslash, you must escape the backslash with
  a second backslash. See [Example of using metacharacters in a single-quoted string constant](#label-regexp-escape-character-caveats-metacharacter).
* If you are using a [backslash-sequence](#label-regexp-general-usage-notes), you must escape the backslash in the sequence.
* If you are using a [backreference](#label-regex-backreferences), you must escape the backslash in the backreference.
  See [Example of using backreferences in a single-quoted string constant](#label-regexp-escape-character-caveats-backreference).

### Example of using metacharacters in a single-quoted string constant[¶](#example-of-using-metacharacters-in-a-single-quoted-string-constant "Link to this heading")

This example uses the backslash as part of an escape sequence in a regular expression that searches for a question mark (`?`).

Create a table and insert a row that contains a single backslash in one column and a question mark in another column:

```
CREATE OR REPLACE TABLE wildcards (w VARCHAR, w2 VARCHAR);
INSERT INTO wildcards (w, w2) VALUES ('\\', '?');
```

Copy

The following query searches for the question mark literal. The search uses a regular expression, and the question mark is a
meta-character in regular expressions, so the search must escape the question mark to treat it as a literal. Because the
backslash appears in a string literal, the backslash itself must also be escaped:

```
SELECT w2
  FROM wildcards
  WHERE REGEXP_LIKE(w2, '\\?');
```

Copy

```
+----+
| W2 |
|----|
| ?  |
+----+
```

The following query makes it easier to see that the regular expression is composed of two characters (the backslash escape
character and the question mark):

```
SELECT w2
  FROM wildcards
  WHERE REGEXP_LIKE(w2, '\\' || '?');
```

Copy

```
+----+
| W2 |
|----|
| ?  |
+----+
```

In the previous example, the extra backslash was needed only because the escape character was part of a string literal.
It was not needed for the regular expression itself. The following SELECT statement does not need to parse a string literal as
part of the SQL command string, and therefore does not need the extra escape character that the string literal needed:

```
SELECT w, w2, w || w2 AS escape_sequence, w2
  FROM wildcards
  WHERE REGEXP_LIKE(w2, w || w2);
```

Copy

```
+---+----+-----------------+----+
| W | W2 | ESCAPE_SEQUENCE | W2 |
|---+----+-----------------+----|
| \ | ?  | \?              | ?  |
+---+----+-----------------+----+
```

### Example of using backreferences in a single-quoted string constant[¶](#example-of-using-backreferences-in-a-single-quoted-string-constant "Link to this heading")

If you use a [backreference](#label-regex-backreferences) (for example, `\1`) in a string literal, you must escape the backslash
that is a part of that backreference. For example, to specify the backreference `\1` in a replacement string literal of
[REGEXP\_REPLACE](functions/regexp_replace), use `\\1`.

The following example uses the table created earlier. The SELECT uses a backreference to replace each occurrence of the regular
expression `.old` with a copy of the matched string preceded by the word “very”:

```
INSERT INTO wildcards (w, w2) VALUES (NULL, 'When I am cold, I am bold.');
```

Copy

```
SELECT w2, REGEXP_REPLACE(w2, '(.old)', 'very \\1')
  FROM wildcards
  ORDER BY w2;
```

Copy

```
+----------------------------+------------------------------------------+
| W2                         | REGEXP_REPLACE(W2, '(.OLD)', 'VERY \\1') |
|----------------------------+------------------------------------------|
| ?                          | ?                                        |
| When I am cold, I am bold. | When I am very cold, I am very bold.     |
+----------------------------+------------------------------------------+
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

1. [List of regex functions](#list-of-regex-functions)
2. [General usage notes](#general-usage-notes)
3. [Specifying the parameters for the regular expression](#specifying-the-parameters-for-the-regular-expression)
4. [Matching characters that are metacharacters](#matching-characters-that-are-metacharacters)
5. [Using backreferences](#using-backreferences)
6. [Specifying an empty pattern](#specifying-an-empty-pattern)
7. [Specifying regular expressions in dollar-quoted string constants](#specifying-regular-expressions-in-dollar-quoted-string-constants)
8. [Specifying regular expressions in single-quoted string constants](#specifying-regular-expressions-in-single-quoted-string-constants)

Related content

1. [String & binary functions](/sql-reference/functions-string)