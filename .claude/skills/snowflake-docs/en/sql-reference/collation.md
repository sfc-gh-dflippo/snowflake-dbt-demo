---
auto_generated: true
description: Collation allows you to specify alternative rules for comparing text
  strings, which can be used to compare and sort data according to a particular language
  or other user-specified rules.
last_scraped: '2026-01-14T16:55:22.191059+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/collation
title: Collation support | Snowflake Documentation
---

1. [Overview](../reference.md)
2. [SQL data types reference](../sql-reference-data-types.md)
3. [SQL command reference](../sql-reference-commands.md)
4. [Function and stored procedure reference](../sql-reference-functions.md)
5. [Class reference](../sql-reference-classes.md)
6. [Scripting reference](../sql-reference-snowflake-scripting.md)
7. [General reference](../sql-reference.md)

   * [Parameters](parameters.md)
   * [References](references.md)
   * [Ternary logic](ternary-logic.md)
   * [Collation support](collation.md)

     + [Supported collation locales](collation-locales.md)
   * [SQL format models](sql-format-models.md)
   * [Object identifiers](identifiers.md)
   * [Constraints](constraints.md)
   * [SQL variables](session-variables.md)
   * [Bind variables](bind-variables.md)
   * [Transactions](transactions.md)
   * [Table literals](literals-table.md)
   * [SNOWFLAKE database](snowflake-db.md)
   * [Snowflake Information Schema](info-schema.md)
   * [Metadata fields](metadata.md)
   * [Conventions](conventions.md)
   * [Reserved keywords](reserved-keywords.md)
8. [API reference](../api-reference.md)

[Reference](../reference.md)[General reference](../sql-reference.md)Collation support

# Collation support[¶](#collation-support "Link to this heading")

Collation allows you to specify alternative rules for comparing [text strings](data-types-text.html#label-character-datatypes),
which can be used to compare and sort data according to a particular language or other user-specified rules.

## Overview of collation support[¶](#overview-of-collation-support "Link to this heading")

The following sections explain what collation is and how you use collation when comparing strings:

* [Understanding collation](#label-collation-definition)
* [Uses for collation](#label-collation-uses)
* [Collation control](#label-collation-control)

### Understanding collation[¶](#understanding-collation "Link to this heading")

Text strings in Snowflake are stored using the UTF-8 character set and, by default, strings are compared according to
the Unicode codes that represent the characters in the string.

However, comparing strings based on their UTF-8 character representations might not provide the desired or expected behavior. For example:

* If special characters in a given language do not sort according to that language’s ordering standards, then sorting might return unexpected results.
* You might want the strings to be ordered by other rules, such as ignoring whether the characters are uppercase or lowercase.

Collation allows you to explicitly specify the rules to use for comparing strings, based on:

* Different locales (that is, different character sets for different languages).
* Case-sensitivity (that is, whether to use case-sensitive or case-insensitive string comparisons without explicitly calling the [UPPER](functions/upper) or
  [LOWER](functions/lower) functions to convert the strings).
* Accent-sensitivity (for example, whether `Z`, `Ź`, and `Ż` are considered the same letter or different letters).
* Punctuation-sensitivity (that is, whether comparisons use only letters or include all characters). For example, if a comparison is punctuation-insensitive, then `A-B-C` and `ABC` are treated as
  equivalent.
* Additional options, such as preferences for sorting based on the first letter in a string and trimming of leading and/or trailing blank spaces.

### Uses for collation[¶](#uses-for-collation "Link to this heading")

Collation can be used in a wide variety of operations, including (but not limited to):

| Usage | Example | Link |
| --- | --- | --- |
| Simple comparison | `... WHERE column1 = column2 ...` | [WHERE](constructs/where) |
| Joins | `... ON table1.column1 = table2.column2 ...` | [JOIN](constructs/join) |
| Sorting | `... ORDER BY column1 ...` | [ORDER BY](constructs/order-by) |
| Top-K sorting | `... ORDER BY column1 LIMIT N ...` | [LIMIT / FETCH](constructs/limit) |
| Aggregation | `... GROUP BY ...` | [GROUP BY](constructs/group-by) |
| Window functions | `... PARTITION BY ... ORDER BY ...` | [Window functions](functions-window) |
| Scalar functions | `... LEAST(column1, column2, column3) ...` | [Scalar functions](functions) |
| Aggregate functions | `... MIN(column1), MAX(column1) ...` | [Aggregate functions](functions-aggregation) |
| Data clustering | `... CLUSTER BY (column1) ...` | [Clustering Keys & Clustered Tables](../user-guide/tables-clustering-keys) |

### Collation control[¶](#collation-control "Link to this heading")

Collation control is granular. You can explicitly specify the collation to use for:

* An account, using the account-level parameter [DEFAULT\_DDL\_COLLATION](parameters.html#label-default-ddl-collation).
* All columns in all tables added to a database, using the [ALTER DATABASE](sql/alter-database) command.
* All columns in all tables added to a schema, using the [ALTER SCHEMA](sql/alter-schema) command.
* All columns added to a table, using the [ALTER TABLE](sql/alter-table) command.
* Individual columns in a table, using the [CREATE TABLE](sql/create-table) command.
* A specific comparison within a SQL statement (for example, `WHERE col1 = col2`). If multiple collations are applied to a
  statement, Snowflake determines the collation to use based on precedence. For more details about precedence, see
  [Collation precedence in multi-string operations](#label-determining-the-collation-used-in-an-operation).

## Collation SQL constructs[¶](#collation-sql-constructs "Link to this heading")

You can use the following SQL constructs for collation:

* [COLLATE clause for table column definitions](#label-collate-clause)
* [COLLATE function](#label-collate-function)
* [COLLATION function](#label-collation-function)

### COLLATE clause for table column definitions[¶](#collate-clause-for-table-column-definitions "Link to this heading")

Adding the optional COLLATE clause to the definition of a table column indicates that the specified collation is used for comparisons and other related operations performed on the data in
the column:

```
CREATE TABLE <table_name> ( <col_name> <col_type> COLLATE '<collation_specification>'
                            [ , <col_name> <col_type> COLLATE '<collation_specification>' ... ]
                            [ , ... ]
                          )
```

Copy

If no COLLATE clause is specified for a column, Snowflake uses the default, which compares strings based on their UTF-8 character representations.

Also, Snowflake supports specifying an empty string for the collation specification (for example, `COLLATE ''`), which is equivalent to specifying no collation for the column.

However, due to precedence, specifying `COLLATE ''` for a column does not have the same effect as explicitly specifying `COLLATE 'utf8'`. For more details, see
[Collation precedence in multi-string operations](#label-determining-the-collation-used-in-an-operation).

You can’t specify the COLLATE clause for indexed columns in [hybrid tables](../user-guide/tables-hybrid). For more information, see [Collations on hybrid table columns](sql/create-hybrid-table.html#label-hybrid-table-collations-disable).

To see whether collation has been specified for the columns in a table, use [DESCRIBE TABLE](sql/desc-table). When you execute the DESCRIBE TABLE command, collation specifications are in the `type` column in the output. Alternatively, use the [COLLATION](#label-collation-function) function to view the collation, if any, for a specific column.

### COLLATE function[¶](#collate-function "Link to this heading")

The [COLLATE](functions/collate) function uses the specified collation on the input string expression:

```
COLLATE( <expression> , '<collation_specification>' )
```

Copy

This function can also be called using infix notation:

```
<expression> COLLATE '<collation_specification>'
```

Copy

This function is particularly useful for explicitly specifying a particular collation for a particular operation (for example,
sorting), but it can also be used to:

* Allow collation in the [SELECT](sql/select) clause of a subquery, making all operations on the specified column in the outer query use the collation.
* Create a table using CTAS with a specified collation.

This example valuates using English case-insensitive collation:

```
SELECT * FROM t1 WHERE COLLATE(col1 , 'en-ci') = 'Tango';
```

Copy

This example sorts the results using German (Deutsch) collation:

```
SELECT * FROM t1 ORDER BY COLLATE(col1 , 'de');
```

Copy

This example creates a table with a column using French collation:

```
CREATE TABLE t2 AS SELECT COLLATE(col1, 'fr') AS col1 FROM t1;
```

Copy

This example uses infix notation to create a table with a column using French collation:

```
CREATE TABLE t2 AS SELECT col1 COLLATE 'fr' AS col1 FROM t1;
```

Copy

### COLLATION function[¶](#collation-function "Link to this heading")

The [COLLATION](functions/collation) function returns the collation specification used by an expression, including a table column:

```
COLLATION( <expression> )
```

Copy

If no collation has been specified for the expression, the function returns NULL.

Typically, if you use this function on a column name, it is best to use DISTINCT to avoid getting one row of output for each row in the table. For example:

```
SELECT DISTINCT COLLATION(column1) FROM table1;
```

Copy

Note

This function only returns the collation specification, not its precedence level. For more details about precedence, see [Collation precedence in multi-string operations](#label-determining-the-collation-used-in-an-operation) (in this
topic).

## Collation specifications[¶](#collation-specifications "Link to this heading")

When using a [COLLATE](#label-collate-clause) clause (for a table column) or the [COLLATE](#label-collate-function) function (for an expression), you must include a collation specification,
which determines the comparison logic used for the column/expression.

A collation specification consists of a string of one or more specifiers separated by a hyphen (`-`), in the form of:

> `'<specifier>[-<specifier> ...]'`

The following specifiers are supported (for more information, see [Supported specifiers](#label-supported-specifiers) in this topic):

* Locale
* Case-sensitivity
* Accent-sensitivity
* Punctuation-sensitivity
* First-letter preference
* Case-conversion
* Space-trimming

Specifiers are case-insensitive and can be in any order, except for locale, which must always be first, if used.

The following sections provide more details about collation specifications:

* [Specification examples](#label-collation-specification-examples)
* [Supported specifiers](#label-supported-specifiers)

### Specification examples[¶](#specification-examples "Link to this heading")

Some examples of collation specification strings include:

* `'de'`: German (Deutsch) locale.
* `'de-ci-pi'`: German locale, with case-insensitive and punctuation-insensitive comparisons.
* `'fr_CA-ai'`: Canadian French locale, with accent-insensitive comparisons.
* `'en_US-trim'`: US English locale, with leading spaces and trailing spaces trimmed before the comparison.

You can also specify an empty string for a collation specification (for example, `COLLATE ''` or `COLLATE(col1, '')`), which indicates to use no collation.

### Supported specifiers[¶](#supported-specifiers "Link to this heading")

Locale:
:   Specifies the language-specific and country-specific rules to apply.

    Supports valid locale strings, consisting of a language code (required) and country code (optional) in the form of `language_country`. Some locale examples include:

    * `en` - English
    * `en_US` - American English
    * `fr` - French
    * `fr_CA` - Canadian French

    In addition, the `utf8` pseudo-locale specifies Unicode ordering, which is the default. For more details, see [Differences in sorting when using UTF-8 or locale collation](#label-collation-utf8-vs-locale) (in this topic).

    The locale specifier is optional, but, if used, must be the first specifier in the string.

    For the full list of locales supported by Snowflake, see [Collation locales supported by Snowflake](collation-locales).

Case-sensitivity:
:   Determines whether case is considered when comparing values. Possible values:

    * `cs` - Case-sensitive (default)
    * `ci` - Case-insensitive

    For example:

    | Collation Specification | Value | Result |
    | --- | --- | --- |
    | `'en-ci'` | `Abc = abc` | True |
    | `'en-cs'` / `en` | `Abc = abc` | False |

Accent-sensitivity:
:   Determines whether accented characters are considered equal to, or different from, their base characters. Possible values:

    * `as` - Accent-sensitive (default)
    * `ai` - Accent-insensitive

    For example:

    | Collation Specification | Value | Result | Notes |
    | --- | --- | --- | --- |
    | `'fr-ai'` | `E = É` | True |  |
    | `'fr-as'` / `'fr'` | `E = É` | False |  |
    | `'en-ai'` | `a = ą` | True | In English, these letters are treated as having only accent differences, so specifying accent-insensitivity results in the values comparing as equal. |
    | `'pl-ai'` | `a = ą` | False | In Polish, these letters are treated as separate base letters, so they always compare as unequal regardless of whether accent-insensitivity is specified. |
    | `'pl-as'` / `'pl'` | `a = ą` | False |  |

    The rules for accent-sensitivity and collation vary between languages. For example, in some languages, collation is always accent-sensitive, and you cannot turn it off even by specifying
    accent-insensitive collation.

Punctuation-sensitivity:
:   Determines whether non-letter characters matter. Possible values:

    * `ps` - Punctuation-sensitive.
    * `pi` - Punctuation-insensitive.

    Note that the default is locale-specific (that is, if punctuation-sensitivity is not specified, locale-specific rules are used). In most cases, the rules are equivalent to `ps`.

    For example:

    | Collation Specification | Value | Result | Notes |
    | --- | --- | --- | --- |
    | `'en-pi'` | `A-B-C = ABC` | True |  |
    | `'en-ps'` | `A-B-C = ABC` | False |  |

First-letter preference:
:   Determines whether, when sorting, uppercase or lowercase letters are first. Possible values:

    * `fl` - Lowercase letters sorted first.
    * `fu` - Uppercase letters sorted first.

    The default is locale-specific (that is, if no value is specified, locale-specific ordering is used). In most cases, the ordering is equivalent to `fl`.

    Also, this specifier has no impact on equality comparisons.

Case-conversion:
:   Results in strings being converted to lowercase or uppercase before comparisons. In some situations, this is faster than full locale-specific collation. Possible values:

    * `upper` - Convert the string to uppercase before comparisons.
    * `lower` - Convert the string to lowercase before comparisons.

    This specifier does not have a default (that is, if no value is specified, neither of the conversions occurs).

Space-trimming:
:   Removes leading/trailing spaces from strings before comparisons. This functionality can be useful for performing comparisons equivalent (except in extremely rare corner cases) in semantics to the SQL CHAR data type.

    Possible values:

    * `trim` - Remove both leading and trailing spaces before comparisons.
    * `ltrim` - Remove only leading spaces before comparisons.
    * `rtrim` - Remove only trailing spaces before comparisons.

    This specifier does not have a default (that is, if no value is specified, trimming is not performed).

    For example:

    | Collation Specification | Value | Result | Notes |
    | --- | --- | --- | --- |
    | `'en-trim'` | `__ABC_ = ABC` | True | For the purposes of these examples, underscore characters represent blank spaces. |
    | `'en-ltrim'` | `__ABC_ = ABC` | False |  |
    | `'en-rtrim'` | `__ABC_ = ABC` | False |  |
    | `'en'` | `__ABC_ = ABC` | False |  |

## Collation implementation details[¶](#collation-implementation-details "Link to this heading")

The following sections provide more detail about support for collation:

* [Case-insensitive comparisons](#label-collation-upper-lower)
* [Differences in sorting when using UTF-8 or locale collation](#label-collation-utf8-vs-locale)
* [Collation precedence in multi-string operations](#label-determining-the-collation-used-in-an-operation)
* [Limited support for collation in built-in functions](#label-limited-support-for-collation-in-built-in-functions)
* [Performance implications of using collation](#label-collation-performance)
* [Additional considerations for using collation](#label-collation-considerations)

### Case-insensitive comparisons[¶](#case-insensitive-comparisons "Link to this heading")

The following sections describe case-insensitive comparisons:

* [Differences when comparing uppercase strings and original strings](#label-collation-upper-lower-case-insensitive-comparison-uppercase-original)
* [Character weights](#label-collation-character-weights)

#### Differences when comparing uppercase strings and original strings[¶](#differences-when-comparing-uppercase-strings-and-original-strings "Link to this heading")

In some languages, two lowercase characters have the same corresponding uppercase character. For example, some languages support both
dotted and undotted forms of lowercase `I` (for example, `i` and `ı`). Forcing the strings to uppercase affects comparisons.

The following example illustrates the difference:

Create the table:

```
CREATE OR REPLACE TABLE test_table (col1 VARCHAR, col2 VARCHAR);
INSERT INTO test_table VALUES ('ı', 'i');
```

Copy

Query the data:

```
SELECT col1 = col2,
       COLLATE(col1, 'lower') = COLLATE(col2, 'lower'),
       COLLATE(col1, 'upper') = COLLATE(col2, 'upper')
  FROM test_table;
```

Copy

```
+-------------+-------------------------------------------------+-------------------------------------------------+
| COL1 = COL2 | COLLATE(COL1, 'LOWER') = COLLATE(COL2, 'LOWER') | COLLATE(COL1, 'UPPER') = COLLATE(COL2, 'UPPER') |
|-------------+-------------------------------------------------+-------------------------------------------------|
| False       | False                                           | True                                            |
+-------------+-------------------------------------------------+-------------------------------------------------+
```

#### Character weights[¶](#character-weights "Link to this heading")

Snowflake supports the following [collation specifications](#label-collation-specification).

* [ICU](https://en.wikipedia.org/wiki/International_Components_for_Unicode) (International Components for Unicode).
* Snowflake-specific collation specifications (for example, `upper` and `lower`).

For case-insensitive comparison operations defined by the ICU, Snowflake follows the
[Unicode Collation Algorithm (UCA)](http://www.unicode.org/reports/tr10) and considers only the
primary and secondary weights, not the tertiary weights, of Unicode characters. Characters that differ only in their tertiary
weights are treated as identical. For example, using the `en-ci` collation specification, a space and a non-breaking space
are considered identical.

### Differences in sorting when using UTF-8 or locale collation[¶](#differences-in-sorting-when-using-utf-8-or-locale-collation "Link to this heading")

Strings are always stored internally in Snowflake in UTF-8, and can represent any character in any language supported by UTF-8. Therefore, when no collation is specified, the
behavior is the same as the UTF-8 collation (that is, `'utf8'`).

In Snowflake, `'utf8'` and `'bin'` are equivalent collation specifications. However, these specifications can’t be mixed in a single expression. For example, the following
query returns an error:

```
SELECT 'abc' COLLATE 'bin' = 'abc' COLLATE 'utf8';
```

Copy

UTF-8 collation is based on the numeric representation of the character as opposed to the alphabetic order of the character.

This is analogous to sorting by the ordinal value of each ASCII character, which is important to note because uppercase letters have ordinal values lower than lowercase letters:

`A = 65`

`B = 66`

`...`

`a = 97`

`b = 98`

`...`

As a result:

* If you sort in UTF-8 order, all uppercase letters are returned before all lowercase letters:

  > `A` , `B` , … , `Y` , `Z` , … , `a` , `b` , … , `y` , `z`
* In contrast, the `'en'` collation specification sorts alphabetically (instead of using the UTF-8 internal representation), resulting in both `A` and `a` returned before both `B` and `b`:

  > `a` , `A` , `b` , `B` , …

Additionally, the differences between the `cs` and `ci` case-sensitivity specifiers affect sorting:

* `cs` (case-sensitive) always returns the lowercase version of a letter before the uppercase version of the same letter. For example, using `'en-cs'`:

  > `a` , `A` , `b` , `B` , …

  Case-sensitive is the default and, therefore, `'en-cs'` and `'en'` are equivalent.
* `ci` (case-insensitive) returns uppercase and lowercase versions of letters randomly with respect to each other, but still before both uppercase and lowercase version of later letters. For
  example, using `'en-ci'`:

  > `A` , `a` , `b` , `B` , …

Some non-alphabetic characters can also be sorted differently depending upon the collation setting. The following example shows that
the plus character (`+`) and minus character (`-`) are sorted differently for different collation settings:

Create the table:

```
CREATE OR REPLACE TABLE demo (
    no_explicit_collation VARCHAR,
    en_ci VARCHAR COLLATE 'en-ci',
    en VARCHAR COLLATE 'en',
    utf_8 VARCHAR collate 'utf8');
INSERT INTO demo (no_explicit_collation) VALUES
    ('-'),
    ('+');
UPDATE demo SET
    en_ci = no_explicit_collation,
    en = no_explicit_collation,
    utf_8 = no_explicit_collation;
```

Copy

Query the data:

```
SELECT MAX(no_explicit_collation), MAX(en_ci), MAX(en), MAX(utf_8)
  FROM demo;
```

Copy

```
+----------------------------+------------+---------+------------+
| MAX(NO_EXPLICIT_COLLATION) | MAX(EN_CI) | MAX(EN) | MAX(UTF_8) |
|----------------------------+------------+---------+------------|
| -                          | +          | +       | -          |
+----------------------------+------------+---------+------------+
```

### Collation precedence in multi-string operations[¶](#collation-precedence-in-multi-string-operations "Link to this heading")

When performing an operation on two (or more) strings, different collations might be specified for different strings.
Determining the collation to apply depends on how collation was specified for each input and the precedence of each
specifier.

There are three precedence levels (from highest to lowest):

Function:
:   Collation is specified using the [COLLATE function](#label-collate-function) in a SQL statement.

Column:
:   Collation was specified in the column definition.

None:
:   No collation is/was specified for a given expression/column, or collation with an empty specification is/was used (for example, `COLLATE(col1, '')` or `col1 STRING COLLATE ''`).

When determining the collation to use, the collation specification with the highest precedence is used. If multiple collations are specified with the same precedence level, their
values are compared, and if they are not equal, an error is returned.

For example, consider a table with the following column-level collation specifications:

```
CREATE OR REPLACE TABLE collation_precedence_example(
  col1    VARCHAR,               -- equivalent to COLLATE ''
  col2_fr VARCHAR COLLATE 'fr',  -- French locale
  col3_de VARCHAR COLLATE 'de'   -- German locale
);
```

Copy

If the table is used in a statement comparing two strings, collation is applied as follows:

* This comparison uses the `'fr'` collation because the precedence for `col2_fr` is higher than the
  precedence for `col1`:

  ```
  ... WHERE col1 = col2_fr ...
  ```

  Copy
* This comparison uses the `'en'` collation, because it is explicitly specified in the statement,
  which takes precedence over the collation for `col2_fr`:

  ```
  ... WHERE col1 COLLATE 'en' = col2_fr ...
  ```

  Copy
* This comparison returns an error because the expressions have different collations at the same precedence level:

  ```
  ... WHERE col2_fr = col3_de ...
  ```

  Copy
* This comparison uses the `'de'` collation because collation for `col2_fr` has been removed:

  ```
  ... WHERE col2_fr COLLATE '' = col3_de ...
  ```

  Copy
* This comparison returns an error because the expressions have different collations at the same precedence level:

  ```
  ... WHERE col2_fr COLLATE 'en' = col3_de COLLATE 'de' ...
  ```

  Copy

Because explicit collation has higher precedence than no collation, specifying an empty string (or specifying no collation) is
different from explicitly specifying `'utf8'` collation. The last two statements in the following code examples show the difference:

For example, consider a table with the following column-level collation specifications:

```
CREATE OR REPLACE TABLE collation_precedence_example2(
  s1 STRING COLLATE '',
  s2 STRING COLLATE 'utf8',
  s3 STRING COLLATE 'fr'
);
```

Copy

If the table is used in a statement comparing two strings, collation is applied as follows:

* This comparison uses `'utf8'` because `s1` has no collation and `'utf8'` is the default:

  ```
  ... WHERE s1 = 'a' ...
  ```

  Copy
* This comparison uses `'utf8'` because `s1` has no collation and `s2` has explicit `'utf8'` collation

  ```
  ... WHERE s1 = s2 ...
  ```

  Copy
* This comparison executes without error because `s1` has no collation and `s3` has explicit `fr` collation, so the
  explicit collation takes precedence:

  ```
  ... WHERE s1 = s3 ...
  ```

  Copy
* This comparison causes an error because `s2` and `s3` have different collations specified at the same precedence level:

  ```
  ... WHERE s2 = s3 ...
  ```

  Copy

  ```
  002322 (42846): SQL compilation error: Incompatible collations: 'fr' and 'utf8'
  ```

### Limited support for collation in built-in functions[¶](#limited-support-for-collation-in-built-in-functions "Link to this heading")

Collation is supported in only a subset of string functions. Functions that could reasonably be expected to implement
collation, but do not yet support collation, return an error when used with collation. These error messages are
displayed not only when calling the COLLATE function, but also when calling a string function on a column that was
defined as collated in the CREATE TABLE or ALTER TABLE statement that created that column.

Currently, collation influences only simple comparison operations. For example, `POSITION('abc' in COLLATE('ABC', 'en-ci'))`
does not find `abc` in `ABC`, even though case-insensitive collation is specified.

#### Functions that support collation[¶](#functions-that-support-collation "Link to this heading")

These functions support collation:

* [[ NOT ] BETWEEN](functions/between)
* [CASE](functions/case)
* [CHARINDEX](functions/charindex)
* [COALESCE](functions/coalesce)
* [CONCAT , ||](functions/concat)
* [CONTAINS](functions/contains)
* [DECODE](functions/decode)
* [ENDSWITH](functions/endswith)
* [EQUAL\_NULL](functions/equal_null)
* [GET\_DDL](functions/get_ddl)
* [GREATEST](functions/greatest)
* [IFF](functions/iff)
* [IFNULL](functions/ifnull)
* [[ NOT ] ILIKE](functions/ilike)
* [ILIKE ANY](functions/ilike_any) (partial support)
* [LEAST](functions/least)
* [LEFT](functions/left)
* [LENGTH, LEN](functions/length) (supported without impact)
* [[ NOT ] LIKE](functions/like)
* [LIKE ALL](functions/like_all) (partial support)
* [LIKE ANY](functions/like_any) (partial support)
* [LISTAGG](functions/listagg)
* [LPAD](functions/lpad)
* [MAX](functions/max)
* [MIN](functions/min)
* [NULLIF](functions/nullif)
* [NVL](functions/nvl)
* [NVL2](functions/nvl2)
* [POSITION](functions/position)
* [REPLACE](functions/replace)
* [RIGHT](functions/right)
* [RPAD](functions/rpad)
* [SPLIT](functions/split)
* [SPLIT\_PART](functions/split_part)
* [STARTSWITH](functions/startswith)
* [SUBSTR , SUBSTRING](functions/substr) (supported without impact)

Some of these functions have limitations on their use with collation. For information, see the documentation of each
specific function.

This list might expand over time.

Caution

Some SQL operators and predicates, such as `||` (concatenation) and `LIKE`, are implemented as functions
(and are available as functions, for example `LIKE()` and `CONCAT()`). If a predicate or operator is implemented as
a function, and the function does not support collation, then the predicate or operator does not support collation.

See also [Collation limitations](#label-collation-limitations).

### Performance implications of using collation[¶](#performance-implications-of-using-collation "Link to this heading")

Using collation can affect the performance of various database operations:

* Operations involving comparisons might be slower.

  This can impact simple [WHERE](constructs/where) clauses, as well as joins, sorts, GROUP BY operations, etc.
* When used with some functions in [WHERE](constructs/where) predicates, micro-partition pruning might be less
  efficient.
* Using collation in a [WHERE](constructs/where) predicate that is different from the collation specified for the
  column might result in reduced pruning efficiency or the complete elimination of pruning.

### Additional considerations for using collation[¶](#additional-considerations-for-using-collation "Link to this heading")

* Remember that, despite the similarity in their names, the following collation functions return different results:

  + [COLLATE](#label-collate-function) explicitly specifies which collation to use.
  + [COLLATION](#label-collation-function) shows which collation is used if none is specified explicitly.
* A column with a collation specification can use characters that are not from the locale for the collation, which might impact sorting.

  For example, if a column is created with a `COLLATE 'en'` clause, the data in the column can contain the non-English character `É`. In this situation, the character `É` is sorted close to
  `E`.
* You can specify collation operations that are not necessarily meaningful.

  For example, you could specify that Polish data is compared to French data using German collation:

  ```
  SELECT ... WHERE COLLATE(French_column, 'de') = Polish_column;
  ```

  Copy

  However, Snowflake does not recommend using the feature this way because it might return unexpected or unintended results.
* After a table column is defined, you cannot change the collation for the column. In other words, after a column has been created with a particular collation using a
  [CREATE TABLE](sql/create-table) statement, you cannot use [ALTER TABLE](sql/alter-table) to change the
  collation.

  However, you can specify a different collation in a DML statement, such as a [SELECT](sql/select) statement, that references the column.

## Differences between `ci` and `upper` / `lower`[¶](#differences-between-ci-and-upper-lower "Link to this heading")

The `upper` and `lower` collation specifications can provide better performance than the `ci` collation specification during
string comparison and sorting. However, `upper` and `lower` have slightly different effects from `ci`, as explained in the
next sections:

* [Differences in comparisons of widths, spaces, and scripts](#label-collation-upper-lower-differences-comparisons)
* [Differences in handling ignorable code points](#label-collation-upper-lower-differences-ignorable)
* [Differences when characters are represented by different code points](#label-collation-upper-lower-differences-sequences)
* [Differences with sequences of code points representing a single character](#label-collation-upper-lower-differences-character)
* [Differences when changes to case result in multiple code points](#label-collation-upper-lower-differences-case)
* [Differences in sort order](#label-collation-upper-lower-differences-sort)

### Differences in comparisons of widths, spaces, and scripts[¶](#differences-in-comparisons-of-widths-spaces-and-scripts "Link to this heading")

During string comparisons, the `ci` collation specification recognizes that different visual representations
of a character might still refer to the same character, and treats them accordingly. To allow for more performant
comparisons, the `upper` and `lower` collation specifications do not recognize these different visual
representations of a character as the same character.

Specifically, the `ci` collation specification ignores some differences in the following categories,
while the `upper` and `lower` collation specifications do not ignore them:

* [Character widths](#label-collation-upper-lower-differences-comparisons-widths)
* [Types of spaces](#label-collation-upper-lower-differences-comparisons-spaces)
* [Character scripts](#label-collation-upper-lower-differences-comparisons-scripts)

The following sections include examples that illustrate these differences.

Note

The comparison behavior of full-width and half-width characters might depend on the locale.

#### Example of comparisons of characters with different widths[¶](#example-of-comparisons-of-characters-with-different-widths "Link to this heading")

Create a table named `different_widths` and insert rows containing characters of different widths:

```
CREATE OR REPLACE TABLE different_widths(codepoint STRING, description STRING);

INSERT INTO different_widths VALUES
  ('a', 'ASCII a'),
  ('A', 'ASCII A'),
  ('ａ', 'Full-width a'),
  ('Ａ', 'Full-width A');

SELECT codepoint VISUAL_CHAR,
       'U+'  || TO_CHAR(UNICODE(codepoint), '0XXX') codepoint_representation,
       description
  FROM different_widths;
```

Copy

```
+-------------+--------------------------+--------------+
| VISUAL_CHAR | CODEPOINT_REPRESENTATION | DESCRIPTION  |
|-------------+--------------------------+--------------|
| a           | U+0061                   | ASCII a      |
| A           | U+0041                   | ASCII A      |
| ａ          | U+FF41                   | Full-width a |
| Ａ          | U+FF21                   | Full-width A |
+-------------+--------------------------+--------------+
```

The following query shows that the `ci` collation specification finds one distinct value when comparing the characters.
The `upper` and `lower` collation specifications find two distinct values when comparing the characters.

```
SELECT COUNT(*) NumRows,
       COUNT(DISTINCT UNICODE(codepoint)) DistinctCodepoints,
       COUNT(DISTINCT codepoint COLLATE 'en-ci') DistinctCodepoints_EnCi,
       COUNT(DISTINCT codepoint COLLATE 'upper') DistinctCodepoints_Upper,
       COUNT(DISTINCT codepoint COLLATE 'lower') DistinctCodepoints_Lower
  FROM different_widths;
```

Copy

```
+---------+--------------------+-------------------------+--------------------------+--------------------------+
| NUMROWS | DISTINCTCODEPOINTS | DISTINCTCODEPOINTS_ENCI | DISTINCTCODEPOINTS_UPPER | DISTINCTCODEPOINTS_LOWER |
|---------+--------------------+-------------------------+--------------------------+--------------------------|
|       4 |                  4 |                       1 |                        2 |                        2 |
+---------+--------------------+-------------------------+--------------------------+--------------------------+
```

The `ci` collation specification ignores differences in both width and case, which means that it finds no differences
between the characters. The `upper` and `lower` collation specifications only ignore differences in case, so
the half-width characters are considered to be different characters than the full-width characters.

The half-width lowercase `a` is considered to be the same as the half-width uppercase `A`, and the full-width
lowercase `a` is considered to be the same as the full-width uppercase `A`. Therefore, the `upper` and
`lower` collation specifications find two distinct values.

#### Example of comparisons of different types of spaces[¶](#example-of-comparisons-of-different-types-of-spaces "Link to this heading")

Create a table named `different_whitespaces` and insert rows with different types of spaces:

```
CREATE OR REPLACE TABLE different_whitespaces(codepoint STRING, description STRING);

INSERT INTO different_whitespaces VALUES
  (' ', 'ASCII space'),
  ('\u00A0', 'Non-breaking space'),
  (' ', 'Ogham space mark'),
  (' ', 'en space'),
  (' ', 'em space');

SELECT codepoint visual_char,
       'U+'  || TO_CHAR(unicode(codepoint), '0XXX')
       codepoint_representation, description
  FROM different_whitespaces;
```

Copy

```
+-------------+--------------------------+--------------------+
| VISUAL_CHAR | CODEPOINT_REPRESENTATION | DESCRIPTION        |
|-------------+--------------------------+--------------------|
|             | U+0020                   | ASCII space        |
|             | U+00A0                   | Non-breaking space |
|             | U+1680                   | Ogham space mark   |
|             | U+2002                   | en space           |
|             | U+2003                   | em space           |
+-------------+--------------------------+--------------------+
```

The following query shows that the `ci` collation specification finds one distinct value when comparing the spaces, which
means that there are no differences between them. The `upper` and `lower` collation specifications find five distinct
values when comparing the spaces, which means that they are all different.

```
SELECT COUNT(*) NumRows,
       COUNT(DISTINCT UNICODE(codepoint)) NumDistinctCodepoints,
       COUNT(DISTINCT codepoint COLLATE 'en-ci') DistinctCodepoints_EnCi,
       COUNT(DISTINCT codepoint COLLATE 'upper') DistinctCodepoints_Upper,
       COUNT(DISTINCT codepoint COLLATE 'lower') DistinctCodepoints_Lower
  FROM different_whitespaces;
```

Copy

```
+---------+-----------------------+-------------------------+--------------------------+--------------------------+
| NUMROWS | NUMDISTINCTCODEPOINTS | DISTINCTCODEPOINTS_ENCI | DISTINCTCODEPOINTS_UPPER | DISTINCTCODEPOINTS_LOWER |
|---------+-----------------------+-------------------------+--------------------------+--------------------------|
|       5 |                     5 |                       1 |                        5 |                        5 |
+---------+-----------------------+-------------------------+--------------------------+--------------------------+
```

#### Example of comparisons of characters with different scripts[¶](#example-of-comparisons-of-characters-with-different-scripts "Link to this heading")

Create a table named `different_scripts` and insert rows containing characters that use different scripts:

```
CREATE OR REPLACE TABLE different_scripts(codepoint STRING, description STRING);

INSERT INTO different_scripts VALUES
  ('1', 'ASCII digit 1'),
  ('¹', 'Superscript 1'),
  ('₁', 'Subscript 1'),
  ('①', 'Circled digit 1'),
  ('੧', 'Gurmukhi digit 1'),
  ('௧', 'Tamil digit 1');

SELECT codepoint VISUAL_CHAR,
       'U+'  || TO_CHAR(UNICODE(codepoint), '0XXX') codepoint_representation,
       description
  FROM different_scripts;
```

Copy

```
+-------------+--------------------------+------------------+
| VISUAL_CHAR | CODEPOINT_REPRESENTATION | DESCRIPTION      |
|-------------+--------------------------+------------------|
| 1           | U+0031                   | ASCII digit 1    |
| ¹           | U+00B9                   | Superscript 1    |
| ₁           | U+2081                   | Subscript 1      |
| ①           | U+2460                   | Circled digit 1  |
| ੧           | U+0A67                   | Gurmukhi digit 1 |
| ௧           | U+0BE7                   | Tamil digit 1    |
+-------------+--------------------------+------------------+
```

The following query shows that the `ci` collation specification finds one distinct value when comparing the characters, which
means that there are no differences between them. The `upper` and `lower` collation specifications find six distinct
values when comparing the characters, which means that they are all different.

```
SELECT COUNT(*) NumRows,
       COUNT(DISTINCT UNICODE(codepoint)) DistinctCodepoints,
       COUNT(DISTINCT codepoint COLLATE 'en-ci') DistinctCodepoints_EnCi,
       COUNT(DISTINCT codepoint COLLATE 'upper') DistinctCodepoints_Upper,
       COUNT(DISTINCT codepoint COLLATE 'lower') DistinctCodepoints_Lower
  FROM different_scripts;
```

Copy

```
+---------+--------------------+-------------------------+--------------------------+--------------------------+
| NUMROWS | DISTINCTCODEPOINTS | DISTINCTCODEPOINTS_ENCI | DISTINCTCODEPOINTS_UPPER | DISTINCTCODEPOINTS_LOWER |
|---------+--------------------+-------------------------+--------------------------+--------------------------|
|       6 |                  6 |                       1 |                        6 |                        6 |
+---------+--------------------+-------------------------+--------------------------+--------------------------+
```

### Differences in handling ignorable code points[¶](#differences-in-handling-ignorable-code-points "Link to this heading")

The Unicode Collation Algorithm specifies that collation elements (code points) can be
[ignorable](https://www.unicode.org/reports/tr10/tr10-36.html#Ignorables_Defn), which means that a code point is not considered
during string comparison and sorting.

* With the `ci` collation specification, these code points are ignored. This can make it difficult to search for or replace
  ignorable code points.
* With the `upper` and `lower` collation specifications, these code points are not ignored.

For example, the code point `U+0001` is ignorable. If you compare this code point to an empty string with the `en-ci`
collation specification, the result is TRUE because `U+0001` is ignored:

```
SELECT '\u0001' = '' COLLATE 'en-ci';
```

Copy

```
+-------------------------------+
| '\U0001' = '' COLLATE 'EN-CI' |
|-------------------------------|
| True                          |
+-------------------------------+
```

On the other hand, if you use the `upper` or `lower` collation specification, the result is FALSE because `U+0001` is not
ignored:

```
SELECT '\u0001' = '' COLLATE 'upper';
```

Copy

```
+-------------------------------+
| '\U0001' = '' COLLATE 'UPPER' |
|-------------------------------|
| False                         |
+-------------------------------+
```

Similarly, suppose that you call the [REPLACE](functions/replace) function to remove this code point from a string.
If you use the `en-ci` collation specification, the function does not remove the code point because `U+0001` is ignored.

As shown in the following example, the string returned by the REPLACE function has the same length as the string passed into the
function because the function does not remove the `U+0001` character.

```
SELECT
  LEN('abc\u0001') AS original_length,
  LEN(REPLACE('abc\u0001' COLLATE 'en-ci', '\u0001')) AS length_after_replacement;
```

Copy

```
+-----------------+--------------------------+
| ORIGINAL_LENGTH | LENGTH_AFTER_REPLACEMENT |
|-----------------+--------------------------|
|               4 |                        4 |
+-----------------+--------------------------+
```

On the other hand, if you use the `upper` or `lower` collation specification, the function removes the code point from the
string, returning a shorter string.

```
SELECT
  LEN('abc\u0001') AS original_length,
  LEN(REPLACE('abc\u0001' COLLATE 'upper', '\u0001')) AS length_after_replacement;
```

Copy

```
+-----------------+--------------------------+
| ORIGINAL_LENGTH | LENGTH_AFTER_REPLACEMENT |
|-----------------+--------------------------|
|               4 |                        3 |
+-----------------+--------------------------+
```

### Differences when characters are represented by different code points[¶](#differences-when-characters-are-represented-by-different-code-points "Link to this heading")

In Unicode,
[different sequences of code points can represent the same character](https://en.wikipedia.org/wiki/Unicode_equivalence).
For example, the Greek Small Letter Iota with Dialytika and Tonos can be represented by the
[precomposed character](https://en.wikipedia.org/wiki/Precomposed_character) with the code point `U+0390` or by the
sequence of code points `U+03b9` `U+0308` `U+0301` for the decomposed characters.

If you use the `ci` collation specification, the different sequences of code points for a character are treated as the same
character. For example, the code point `U+0390` and the sequence of code points `U+03b9` `U+0308` `U+0301` are treated
as equivalent:

```
SELECT '\u03b9\u0308\u0301' = '\u0390' COLLATE 'en-ci';
```

Copy

```
+-------------------------------------------------+
| '\U03B9\U0308\U0301' = '\U0390' COLLATE 'EN-CI' |
|-------------------------------------------------|
| True                                            |
+-------------------------------------------------+
```

In order to improve performance for the `upper` and `lower` collation specifications, the sequences are not handled in the
same way. Two sequences of code points are considered to be equivalent only if they result in the same binary representation
after they are converted to uppercase or lowercase.

For example, using the `upper` specification with the code point `U+0390` and the sequence of code points `U+03b9`
`U+0308` `U+0301` results in characters that are treated as equal:

```
SELECT '\u03b9\u0308\u0301' = '\u0390' COLLATE 'upper';
```

Copy

```
+-------------------------------------------------+
| '\U03B9\U0308\U0301' = '\U0390' COLLATE 'UPPER' |
|-------------------------------------------------|
| True                                            |
+-------------------------------------------------+
```

Using the `lower` specification results in characters that are not equal:

```
SELECT '\u03b9\u0308\u0301' = '\u0390' COLLATE 'lower';
```

Copy

```
+-------------------------------------------------+
| '\U03B9\U0308\U0301' = '\U0390' COLLATE 'LOWER' |
|-------------------------------------------------|
| False                                           |
+-------------------------------------------------+
```

These differences are less likely to occur when using `upper` (rather than `lower`) because there is only one composite
uppercase code point (`U+0130`), compared to over 100 composite lowercase code points.

### Differences with sequences of code points representing a single character[¶](#differences-with-sequences-of-code-points-representing-a-single-character "Link to this heading")

In cases where a sequence of code points represents a single character, the `ci` collation specification recognizes that the
sequence represents a single character and does not match individual code points in the sequence.

For example, the sequence of code points `U+03b9` `U+0308` `U+0301` represents a single character (the Greek Small Letter
Iota with Dialytika and Tonos). `U+0308` and `U+0301` represent accents applied to `U+03b9`.

For the `ci` collation specification, if you use the [CONTAINS](functions/contains) function to determine if the
sequence `U+03b9` `U+0308` contains `U+03b9` or `U+0308`, the function returns FALSE because the sequence `U+03b9`
`U+0308` is treated as a single character:

```
SELECT CONTAINS('\u03b9\u0308', '\u03b9' COLLATE 'en-ci');
```

Copy

```
+----------------------------------------------------+
| CONTAINS('\U03B9\U0308', '\U03B9' COLLATE 'EN-CI') |
|----------------------------------------------------|
| False                                              |
+----------------------------------------------------+
```

```
SELECT CONTAINS('\u03b9\u0308', '\u0308' COLLATE 'en-ci');
```

Copy

```
+----------------------------------------------------+
| CONTAINS('\U03B9\U0308', '\U0308' COLLATE 'EN-CI') |
|----------------------------------------------------|
| False                                              |
+----------------------------------------------------+
```

To improve performance, the `upper` and `lower` specifications do not treat these sequences as a single character. In the
example above, the CONTAINS function returns TRUE because these specifications treat the sequence of code points as separate
characters:

```
SELECT CONTAINS('\u03b9\u0308', '\u03b9' COLLATE 'upper');
```

Copy

```
+----------------------------------------------------+
| CONTAINS('\U03B9\U0308', '\U03B9' COLLATE 'UPPER') |
|----------------------------------------------------|
| True                                               |
+----------------------------------------------------+
```

```
SELECT CONTAINS('\u03b9\u0308', '\u0308' COLLATE 'upper');
```

Copy

```
+----------------------------------------------------+
| CONTAINS('\U03B9\U0308', '\U0308' COLLATE 'UPPER') |
|----------------------------------------------------|
| True                                               |
+----------------------------------------------------+
```

### Differences when changes to case result in multiple code points[¶](#differences-when-changes-to-case-result-in-multiple-code-points "Link to this heading")

For some composite characters, the uppercase or lowercase version of the character is represented by a sequence of code points.
For example, the uppercase character for the German character ß is a sequence of two S characters (SS).

Even though ß and SS are equivalent, when you use the `upper` collation specification, searches of ß and SS return different
results. Sequences produced by case conversion either match in their entirety or not at all.

```
SELECT CONTAINS('ß' , 's' COLLATE 'upper');
```

Copy

```
+--------------------------------------+
| CONTAINS('SS' , 'S' COLLATE 'UPPER') |
|--------------------------------------|
| False                                |
+--------------------------------------+
```

```
SELECT CONTAINS('ss', 's' COLLATE 'upper');
```

Copy

```
+-------------------------------------+
| CONTAINS('SS', 'S' COLLATE 'UPPER') |
|-------------------------------------|
| True                                |
+-------------------------------------+
```

### Differences in sort order[¶](#differences-in-sort-order "Link to this heading")

Sorting for the `upper` and `lower` collation specifications works differently from sorting for the `ci` specification:

* With the `ci` specification, strings are sorted by collation key. In general, the collation key can account for case
  sensitivity, accent sensitivity, locale, etc.
* With the `upper` and `lower` specifications, strings are sorted by code point to improve performance.

For example, some characters within the ASCII range (such as `+` and `-`) sort differently:

```
SELECT '+' < '-' COLLATE 'en-ci';
```

Copy

```
+---------------------------+
| '+' < '-' COLLATE 'EN-CI '|
|---------------------------|
| False                     |
+---------------------------+
```

```
SELECT '+' < '-' COLLATE 'upper';
```

Copy

```
+---------------------------+
| '+' < '-' COLLATE 'UPPER' |
|---------------------------|
| True                      |
+---------------------------+
```

As another example, strings with ignored code points sort in a different order:

```
SELECT 'a\u0001b' < 'ab' COLLATE 'en-ci';
```

Copy

```
+-----------------------------------+
| 'A\U0001B' < 'AB' COLLATE 'EN-CI' |
|-----------------------------------|
| False                             |
+-----------------------------------+
```

```
SELECT 'a\u0001b' < 'ab' COLLATE 'upper';
```

Copy

```
+-----------------------------------+
| 'A\U0001B' < 'AB' COLLATE 'UPPER' |
|-----------------------------------|
| True                              |
+-----------------------------------+
```

In addition, emojis sort differently:

```
SELECT 'abc' < '❄' COLLATE 'en-ci';
```

Copy

```
+-----------------------------+
| 'ABC' < '❄' COLLATE 'EN-CI' |
|-----------------------------|
| False                       |
+-----------------------------+
```

```
SELECT 'abc' < '❄' COLLATE 'upper';
```

Copy

```
+-----------------------------+
| 'ABC' < '❄' COLLATE 'UPPER' |
|-----------------------------|
| True                        |
+-----------------------------+
```

## Collation limitations[¶](#collation-limitations "Link to this heading")

The following limitations apply to collation:

* [Collation is supported only for strings up to 64 MB](#label-collation-limitations-strings-up-to-8mb)
* [Collation not supported with UDFs](#label-collation-limitations-udfs)
* [Collation not supported for strings in VARIANT, ARRAY, or OBJECT values](#label-collation-limitations-variant-array-object)
* [Clean rooms support only default collation](#label-collation-limitations-clean-rooms)

### Collation is supported only for strings up to 64 MB[¶](#collation-is-supported-only-for-strings-up-to-64-mb "Link to this heading")

Although the Snowflake VARCHAR data type supports strings up to 128 MB, Snowflake supports collation only when the
resulting string is 64 MB or less. (Some collation operations can lengthen a string.)

### Collation not supported with UDFs[¶](#collation-not-supported-with-udfs "Link to this heading")

Snowflake does not support collation with UDFs (user-defined functions):

* You cannot return a collated string value from a UDF; the server reports that the actual return type is incompatible with
  the declared return type.
* If you pass a collated string value to a UDF, the collation information is not passed; the UDF sees the string as an uncollated
  string.

### Collation not supported for strings in VARIANT, ARRAY, or OBJECT values[¶](#collation-not-supported-for-strings-in-variant-array-or-object-values "Link to this heading")

Strings stored inside a VARIANT, OBJECT, or ARRAY value do not include a collation specification. Therefore:

* Comparison of these values always uses the `'utf8'` collation.
* When a VARCHAR value with a collation specification is used to construct an ARRAY, OBJECT, or VARIANT value, the
  collation specification is not preserved.
* You can still compare a value stored inside an ARRAY, OBJECT, or VARIANT by extracting the value, casting to
  VARCHAR, and adding a collation specification. For example:

  ```
  COLLATE(VARIANT_COL:fld1::VARCHAR, 'en-ci') = VARIANT_COL:fld2::VARCHAR
  ```

  Copy

### Clean rooms support only default collation[¶](#clean-rooms-support-only-default-collation "Link to this heading")

Clean rooms support only default collation at the account level. You can check this by running SHOW PARAMETERS LIKE
‘DEFAULT\_DDL\_COLLATION’ IN ACCOUNT;

## Collation examples[¶](#collation-examples "Link to this heading")

The following statement creates a table that uses different collation for each column:

```
CREATE OR REPLACE TABLE collation_demo (
  uncollated_phrase VARCHAR, 
  utf8_phrase VARCHAR COLLATE 'utf8',
  english_phrase VARCHAR COLLATE 'en',
  spanish_phrase VARCHAR COLLATE 'es');

INSERT INTO collation_demo (
      uncollated_phrase, 
      utf8_phrase, 
      english_phrase, 
      spanish_phrase) 
   VALUES (
     'pinata', 
     'pinata', 
     'pinata', 
     'piñata');
```

Copy

Note

Collations don’t affect the set of characters that can be stored. Snowflake supports all UTF-8 characters.

The following query on the table shows the expected values:

```
SELECT * FROM collation_demo;
```

Copy

```
+-------------------+-------------+----------------+----------------+
| UNCOLLATED_PHRASE | UTF8_PHRASE | ENGLISH_PHRASE | SPANISH_PHRASE |
|-------------------+-------------+----------------+----------------|
| pinata            | pinata      | pinata         | piñata         |
+-------------------+-------------+----------------+----------------+
```

The following query does not find a match because the character `ñ` does not match `n`:

```
SELECT * FROM collation_demo WHERE spanish_phrase = uncollated_phrase;
```

Copy

```
+-------------------+-------------+----------------+----------------+
| UNCOLLATED_PHRASE | UTF8_PHRASE | ENGLISH_PHRASE | SPANISH_PHRASE |
|-------------------+-------------+----------------+----------------|
+-------------------+-------------+----------------+----------------+
```

Changing collation doesn’t force related, but unequal, characters (for example, `ñ` and `n`) to be treated as equal:

```
CREATE OR REPLACE TABLE collation_demo1 (
  uncollated_phrase VARCHAR, 
  utf8_phrase VARCHAR COLLATE 'utf8',
  english_phrase VARCHAR COLLATE 'en-ai',
  spanish_phrase VARCHAR COLLATE 'es-ai');

INSERT INTO collation_demo1 (
    uncollated_phrase, 
    utf8_phrase, 
    english_phrase, 
    spanish_phrase) 
  VALUES (
    'piñata', 
    'piñata', 
    'piñata', 
    'piñata');

SELECT uncollated_phrase = 'pinata', 
       utf8_phrase = 'pinata', 
       english_phrase = 'pinata', 
       spanish_phrase = 'pinata'
  FROM collation_demo1;
```

Copy

```
+------------------------------+------------------------+---------------------------+---------------------------+
| UNCOLLATED_PHRASE = 'PINATA' | UTF8_PHRASE = 'PINATA' | ENGLISH_PHRASE = 'PINATA' | SPANISH_PHRASE = 'PINATA' |
|------------------------------+------------------------+---------------------------+---------------------------|
| False                        | False                  | True                      | False                     |
+------------------------------+------------------------+---------------------------+---------------------------+
```

Only the English phrase returns `True` for the following reasons:

* Uncollated comparisons don’t ignore accents.
* `utf8` collation comparisons don’t ignore accents.
* The `en-ai` and `es-ai` collation comparisons ignore accents, but in Spanish, `ñ` is treated as an
  individual character rather than an accented `n`.

The following examples demonstrate the effect of collation on sort order:

```
INSERT INTO collation_demo (spanish_phrase) VALUES
  ('piña colada'),
  ('Pinatubo (Mount)'),
  ('pint'),
  ('Pinta');
```

Copy

```
SELECT spanish_phrase FROM collation_demo 
  ORDER BY spanish_phrase;
```

Copy

```
+------------------+
| SPANISH_PHRASE   |
|------------------|
| Pinatubo (Mount) |
| pint             |
| Pinta            |
| piña colada      |
| piñata           |
+------------------+
```

The following query returns the values in a different order by changing the
collation to from `'es'` (Spanish) to `'utf8'`:

```
SELECT spanish_phrase FROM collation_demo 
  ORDER BY COLLATE(spanish_phrase, 'utf8');
```

Copy

```
+------------------+
| SPANISH_PHRASE   |
|------------------|
| Pinatubo (Mount) |
| Pinta            |
| pint             |
| piña colada      |
| piñata           |
+------------------+
```

This example shows how to use the [COLLATION](#label-collation-function) function to view the collation for an expression, such as a column:

```
CREATE OR REPLACE TABLE collation_demo2 (
  c1 VARCHAR COLLATE 'fr', 
  c2 VARCHAR COLLATE '');

INSERT INTO collation_demo2 (c1, c2) VALUES
  ('a', 'a'),
  ('b', 'b');
```

Copy

```
SELECT DISTINCT COLLATION(c1), COLLATION(c2) FROM collation_demo2;
```

Copy

```
+---------------+---------------+
| COLLATION(C1) | COLLATION(C2) |
|---------------+---------------|
| fr            | NULL          |
+---------------+---------------+
```

You can also use [DESCRIBE TABLE](sql/desc-table) to view collation information about the columns in a table:

```
DESC TABLE collation_demo2;
```

Copy

```
+------+--------------------------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+----------------+
| name | type                           | kind   | null? | default | primary key | unique key | check | expression | comment | policy name | privacy domain |
|------+--------------------------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+----------------|
| C1   | VARCHAR(16777216) COLLATE 'fr' | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL           |
| C2   | VARCHAR(16777216)              | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL           |
+------+--------------------------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+----------------+
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

1. [Overview of collation support](#overview-of-collation-support)
2. [Understanding collation](#understanding-collation)
3. [Uses for collation](#uses-for-collation)
4. [Collation control](#collation-control)
5. [Collation SQL constructs](#collation-sql-constructs)
6. [COLLATE clause for table column definitions](#collate-clause-for-table-column-definitions)
7. [COLLATE function](#collate-function)
8. [COLLATION function](#collation-function)
9. [Collation specifications](#collation-specifications)
10. [Specification examples](#specification-examples)
11. [Supported specifiers](#supported-specifiers)
12. [Collation implementation details](#collation-implementation-details)
13. [Case-insensitive comparisons](#case-insensitive-comparisons)
14. [Differences in sorting when using UTF-8 or locale collation](#differences-in-sorting-when-using-utf-8-or-locale-collation)
15. [Collation precedence in multi-string operations](#collation-precedence-in-multi-string-operations)
16. [Limited support for collation in built-in functions](#limited-support-for-collation-in-built-in-functions)
17. [Performance implications of using collation](#performance-implications-of-using-collation)
18. [Additional considerations for using collation](#additional-considerations-for-using-collation)
19. [Differences between ci and upper / lower](#differences-between-ci-and-upper-lower)
20. [Differences in comparisons of widths, spaces, and scripts](#differences-in-comparisons-of-widths-spaces-and-scripts)
21. [Differences in handling ignorable code points](#differences-in-handling-ignorable-code-points)
22. [Differences when characters are represented by different code points](#differences-when-characters-are-represented-by-different-code-points)
23. [Differences with sequences of code points representing a single character](#differences-with-sequences-of-code-points-representing-a-single-character)
24. [Differences when changes to case result in multiple code points](#differences-when-changes-to-case-result-in-multiple-code-points)
25. [Differences in sort order](#differences-in-sort-order)
26. [Collation limitations](#collation-limitations)
27. [Collation is supported only for strings up to 64 MB](#collation-is-supported-only-for-strings-up-to-64-mb)
28. [Collation not supported with UDFs](#collation-not-supported-with-udfs)
29. [Collation not supported for strings in VARIANT, ARRAY, or OBJECT values](#collation-not-supported-for-strings-in-variant-array-or-object-values)
30. [Clean rooms support only default collation](#clean-rooms-support-only-default-collation)
31. [Collation examples](#collation-examples)