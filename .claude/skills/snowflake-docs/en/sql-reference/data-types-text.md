---
auto_generated: true
description: This topic describes the string/text data types, including binary strings,
  supported in Snowflake, along with the supported formats for string constants/literals.
last_scraped: '2026-01-14T16:56:09.283678+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/data-types-text
title: String & binary data types | Snowflake Documentation
---

1. [Overview](../reference.md)
2. [SQL data types reference](../sql-reference-data-types.md)

   * [Summary](intro-summary-data-types.md)
   * [Numeric](data-types-numeric.md)
   * [String & binary](data-types-text.md)

     + [Binary input and output formats](binary-input-output.md)
     + [Working with binary values](binary-examples.md)
   * [Logical](data-types-logical.md)
   * [Date & time](data-types-datetime.md)
   * [Semi-structured](data-types-semistructured.md)
   * [Structured](data-types-structured.md)
   * [Unstructured](data-types-unstructured.md)
   * [Geospatial](data-types-geospatial.md)
   * [Vector](data-types-vector.md)
   * [Unsupported](data-types-unsupported.md)
   * [Conversion](data-type-conversion.md)
3. [SQL command reference](../sql-reference-commands.md)
4. [Function and stored procedure reference](../sql-reference-functions.md)
5. [Class reference](../sql-reference-classes.md)
6. [Scripting reference](../sql-reference-snowflake-scripting.md)
7. [General reference](../sql-reference.md)
8. [API reference](../api-reference.md)

[Reference](../reference.md)[SQL data types reference](../sql-reference-data-types.md)String & binary

# String & binary data types[¶](#string-binary-data-types "Link to this heading")

This topic describes the string/text data types, including binary strings, supported in Snowflake, along with the supported formats for string constants/literals.

## Data types for text strings[¶](#data-types-for-text-strings "Link to this heading")

Snowflake supports the following data types for text (that is, character) strings.

### VARCHAR[¶](#varchar "Link to this heading")

VARCHAR values hold Unicode UTF-8 characters.

Note

In some systems outside of Snowflake, data types such as CHAR and VARCHAR store ASCII, while data types such as NCHAR and
NVARCHAR store Unicode.

In Snowflake, VARCHAR and all other string data types store Unicode UTF-8 characters. There is no difference with respect to
Unicode handling between CHAR and NCHAR data types. Synonyms such as NCHAR are primarily for syntax compatibility when porting
DDL commands to Snowflake.

When you declare a column of type VARCHAR, you can specify an optional parameter `(N)`, which is the maximum number of
characters to store. For example:

```
CREATE TABLE t1 (v VARCHAR(134217728));
```

Copy

If no length is specified, the default is 16777216.

Although a VARCHAR value’s maximum length is specified in characters, a VARCHAR value is also limited to a maximum of
134217728 bytes (128 MB). The maximum number of Unicode characters that can be stored in a VARCHAR column is as follows:

Single-byte:
:   134217728

Multi-byte:
:   Between 67108864 (2 bytes per character) and 33554432 (4 bytes per character)

For example, if you declare a column as `VARCHAR(134217728)`, the column can hold a maximum of 67,108,864 2-byte Unicode characters,
even though you specified a maximum length of `134217728`.

When choosing the maximum length for a VARCHAR column, consider the following:

* **Storage:** A column consumes storage for only the amount of actual data stored. For example, a 1-character string in a
  `VARCHAR(134217728)` column only consumes a single character.
* **Performance:** There is no performance difference between using the full-length VARCHAR declaration `VARCHAR(134217728)` and a
  smaller length.

  In any relational database, SELECT statements in which a WHERE clause references VARCHAR columns or string columns aren’t
  as fast as SELECT statements filtered using a date or numeric column condition.
* **Tools for working with data:** Some BI/ETL tools define the maximum size of the VARCHAR data in storage or in memory. If you
  know the maximum size for a column, you can limit the size when you add the column.
* **Collation:** When you specify a <collation> for a VARCHAR column, the number of characters
  that are allowed varies, depending on the number of bytes each character takes and the collation specification of the column.

  When comparing values in a collated column,
  [Snowflake follows the Unicode Collation Algorithm (UCA)](collation.html#label-collation-character-weights). This algorithm affects the
  maximum number of characters allowed. Currently, around 1.5 million to 8 million characters are allowed in a VARCHAR column
  that is defined with a maximum size and a collation specification.

  As an example, the following table shows how the maximum number of characters can vary for a `VARCHAR(134217728)` column, depending
  on the number of bytes per character and the collation specification used:

  | Number of bytes per character | Collation specification | Maximum number of characters allowed (approximate) |
  | --- | --- | --- |
  | 1 byte | `en-ci` or `en-ci-pi-ai` | Around 56 million characters |
  | 1 byte | `en` | Around 32 million characters |
  | 2 byte | `en-ci-pi-ai` | Around 64 million characters |
  | 2 byte | `en-ci` or `en-ci-pi` | Around 21.6 million characters |
  | 2 byte | `en` | Around 12 million characters |

### CHAR, CHARACTER, NCHAR[¶](#char-character-nchar "Link to this heading")

Synonymous with VARCHAR, except that if the length is not specified, `CHAR(1)` is the default.

Note

Snowflake currently deviates from common CHAR semantics in that strings shorter than the maximum length are not space-padded at the end.

### STRING, TEXT, VARCHAR2, NVARCHAR, NVARCHAR2, CHAR VARYING, NCHAR VARYING[¶](#string-text-varchar2-nvarchar-nvarchar2-char-varying-nchar-varying "Link to this heading")

Synonymous with VARCHAR.

### String examples in table columns[¶](#string-examples-in-table-columns "Link to this heading")

```
CREATE OR REPLACE TABLE test_text(
  vm VARCHAR(134217728),
  vd VARCHAR,
  v50 VARCHAR(50),
  cm CHAR(134217728),
  cd CHAR,
  c10 CHAR(10),
  sm STRING(134217728),
  sd STRING,
  s20 STRING(20),
  tm TEXT(134217728),
  td TEXT,
  t30 TEXT(30));

DESC TABLE test_text;
```

Copy

```
+------+--------------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+----------------+
| name | type               | kind   | null? | default | primary key | unique key | check | expression | comment | policy name | privacy domain |
|------+--------------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+----------------|
| VM   | VARCHAR(134217728) | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL           |
| VD   | VARCHAR(16777216)  | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL           |
| V50  | VARCHAR(50)        | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL           |
| CM   | VARCHAR(134217728) | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL           |
| CD   | VARCHAR(1)         | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL           |
| C10  | VARCHAR(10)        | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL           |
| SM   | VARCHAR(134217728) | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL           |
| SD   | VARCHAR(16777216)  | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL           |
| S20  | VARCHAR(20)        | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL           |
| TM   | VARCHAR(134217728) | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL           |
| TD   | VARCHAR(16777216)  | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL           |
| T30  | VARCHAR(30)        | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL           |
+------+--------------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+----------------+
```

## Data types for binary strings[¶](#data-types-for-binary-strings "Link to this heading")

Snowflake supports the following data types for binary strings.

### BINARY[¶](#binary "Link to this heading")

The maximum length is 64 MB (67,108,864 bytes). Unlike VARCHAR, the BINARY data type has no notion of Unicode characters,
so the length is always measured in terms of bytes.

BINARY values are limited to 64 MB so that they fit within 128 MB when converted to hexadecimal strings, for example using
`TO_CHAR(<binary_expression>, 'HEX')`.

When you declare a column of type BINARY, you can specify an optional parameter `(N)`, which is the maximum number of
bytes to store. For example:

```
CREATE TABLE b1 (b BINARY(33554432));
```

Copy

If no length is specified, the default is 8388608.

### VARBINARY[¶](#varbinary "Link to this heading")

VARBINARY is synonymous with BINARY.

### Internal representation[¶](#internal-representation "Link to this heading")

The BINARY data type holds a sequence of 8-bit bytes.

When Snowflake displays BINARY data values, Snowflake often represents each
byte as two hexadecimal characters. For example, the word `HELP` might be
displayed as `48454C50`, where `48` is the hexadecimal equivalent of
the ASCII (Unicode) letter `H`, `45` is the hexadecimal representation of
the letter `E`, and so on.

For more information about entering and displaying BINARY data, see
[Binary input and output](binary-input-output).

### Binary examples in table columns[¶](#binary-examples-in-table-columns "Link to this heading")

```
CREATE OR REPLACE TABLE test_binary(
  bd BINARY,
  b100 BINARY(100),
  vbd VARBINARY);

DESC TABLE test_binary;
```

Copy

```
+------+-----------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+----------------+
| name | type            | kind   | null? | default | primary key | unique key | check | expression | comment | policy name | privacy domain |
|------+-----------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+----------------|
| BD   | BINARY(8388608) | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL           |
| B100 | BINARY(100)     | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL           |
| VBD  | BINARY(8388608) | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL           |
+------+-----------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+----------------+
```

## String constants[¶](#string-constants "Link to this heading")

*Constants* (also known as *literals*) refer to fixed data values. String constants in Snowflake must always be enclosed between
delimiter characters. Snowflake supports using either of the following to delimit string constants:

* [Single quotes](#label-single-quoted-string-constants)
* [Pairs of dollar signs](#label-dollar-quoted-string-constants)

### Single-quoted string constants[¶](#single-quoted-string-constants "Link to this heading")

A string constant can be enclosed between single quote delimiters (for example, `'This is a string'`). To include
a single quote character within a string constant, type two adjacent single quotes (for example, `''`).

For example:

```
SELECT 'Today''s sales projections', '-''''-';
```

Copy

```
+------------------------------+----------+
| 'TODAY''S SALES PROJECTIONS' | '-''''-' |
|------------------------------+----------|
| Today's sales projections    | -''-     |
+------------------------------+----------+
```

Note

Two single quotes is not the same as the double quote character (`"`), which is used (as needed) for delimiting object identifiers. For more information, see
[Identifier requirements](identifiers-syntax).

#### Escape sequences in single-quoted string constants[¶](#escape-sequences-in-single-quoted-string-constants "Link to this heading")

To include a single quote or other special characters (for example, newlines) in a single-quoted string constant, you must escape these
characters by using *backslash escape sequences*. A backslash escape sequence is a sequence of characters that begins with a
backslash (`\`).

Note

If the string contains many single quotes, backslashes, or other special characters, you can use a
[dollar-quoted string constant](#label-dollar-quoted-string-constants) instead to avoid escaping these characters.

You can also use escape sequences to insert ASCII characters by specifying their
[code points](https://en.wikipedia.org/wiki/Code_point) (the numeric values that correspond to those characters) in octal or
hexadecimal. For example, in ASCII, the code point for the space character is 32, which is 20 in hexadecimal. To specify a space,
you can use the hexadecimal escape sequence `\x20`.

You can also use escape sequences to insert Unicode characters, for example `\u26c4`.

The following table lists the supported escape sequences in four categories: simple, octal, hexadecimal, and Unicode:

> | Escape sequence | Character represented |
> | --- | --- |
> | **Simple escape sequences** |  |
> | `\'` | A single quote (`'`) character. |
> | `\"` | A double quote (`"`) character. |
> | `\\` | A backslash (`\`) character. |
> | `\b` | A backspace character. |
> | `\f` | A formfeed character. |
> | `\n` | A newline (linefeed) character. |
> | `\r` | A carriage return character. |
> | `\t` | A tab character. |
> | `\0` | An ASCII NUL character. |
> | **Octal escape sequences** |  |
> | `\ooo` | ASCII character in octal notation (that is, where each `o` represents an octal digit). |
> | **Hexadecimal escape sequences** |  |
> | `\xhh` | ASCII character in hexadecimal notation (that is, where each `h` represents a hexadecimal digit). |
> | **Unicode escape sequences** |  |
> | `\uhhhh` | Unicode character in hexadecimal notation (that is, where each `h` represents a hexadecimal digit). The number of hexadecimal digits must be exactly four. |

As shown in the table above, if a string constant must include a backslash character (for example, `C:\` in a Windows path or `\d` in
a [regular expression](functions-regexp.html#label-regexp-general-usage-notes)), you must escape the backslash with a second backslash. For
example, to include `\d` in a regular expression in a string constant, use `\\d`.

If a backslash is used in sequences other than the ones listed above, the backslash is ignored. For example, the
sequence of characters `'\z'` is interpreted as `'z'`.

The following example demonstrates how to use backslash escape sequences. This includes examples of specifying:

* A tab character.
* A newline.
* A backslash.
* The octal and hexadecimal escape sequences for an exclamation mark (code point 33, which is `\041` in octal and `\x21` in
  hexadecimal).
* The Unicode escape sequence for a small image of a snowman.
* Something that is not a valid escape sequence.

```
SELECT $1, $2 FROM
  VALUES
    ('Tab','Hello\tWorld'),
    ('Newline','Hello\nWorld'),
    ('Backslash','C:\\user'),
    ('Octal','-\041-'),
    ('Hexadecimal','-\x21-'),
    ('Unicode','-\u26c4-'),
    ('Not an escape sequence', '\z');
```

Copy

```
+------------------------+---------------+
| $1                     | $2            |
|------------------------+---------------|
| Tab                    | Hello   World |
| Newline                | Hello         |
|                        | World         |
| Backslash              | C:\user       |
| Octal                  | -!-           |
| Hexadecimal            | -!-           |
| Unicode                | -⛄-          |
| Not an escape sequence | z             |
+------------------------+---------------+
```

### Dollar-quoted string constants[¶](#dollar-quoted-string-constants "Link to this heading")

In some cases, you might need to specify a string constant that contains:

* Single quote characters.
* Backslash characters (for example, in a [regular expression](functions-regexp)).
* Newline characters (for example, in the body of a stored procedure or function that you specify in
  [CREATE PROCEDURE](sql/create-procedure) or [CREATE FUNCTION](sql/create-function)).

In these cases, you can avoid [escaping these characters](#label-single-quoted-string-constants-escape-sequences) by using
a pair of dollar signs (`$$`) rather than a single quote (`'`) to delimit the beginning and ending of the string.

In a dollar-quoted string constant, you can include quotes, backslashes, newlines and any other special character (except for
double-dollar signs) without escaping those characters. The content of a dollar-quoted string constant is always interpreted
literally.

The following examples are equivalent ways of specifying string constants:

| Example using single quote delimiters | Example using double dollar sign delimiters |
| --- | --- |
| ``` 'string with a \' character' ```  Copy | ``` $$string with a ' character$$ ```  Copy |
| ``` 'regular expression with \\ characters: \\d{2}-\\d{3}-\\d{4}' ```  Copy | ``` $$regular expression with \ characters: \d{2}-\d{3}-\d{4}$$ ```  Copy |
| ``` 'string with a newline\ncharacter' ```  Copy | ``` $$string with a newline character$$ ```  Copy |

The following example uses a dollar-quoted string constant that contains newlines and several
[escape sequences](#label-single-quoted-string-constants-escape-sequences):

```
SELECT $1, $2 FROM VALUES (
  'row1',
  $$a
                                  ' \ \t
                                  \x21 z $ $$);
```

Copy

```
+------+---------------------------------------------+
| $1   | $2                                          |
|------+---------------------------------------------|
| row1 | a                                           |
|      |                                   ' \ \t    |
|      |                                   \x21 z $  |
+------+---------------------------------------------+
```

In this example, the escape sequences are interpreted as their individual characters
(for example, a backslash followed by a `t`), rather than as escape sequences.

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

1. [Data types for text strings](#data-types-for-text-strings)
2. [Data types for binary strings](#data-types-for-binary-strings)
3. [String constants](#string-constants)

Related content

1. [String & binary functions](/sql-reference/functions-string)
2. [Collation support](/sql-reference/collation)
3. [Semi-structured and structured data functions](/sql-reference/functions-semistructured)
4. [Conversion functions](/sql-reference/functions-conversion)
5. [Binary input and output](/sql-reference/binary-input-output)
6. [Data type conversion](/sql-reference/data-type-conversion)