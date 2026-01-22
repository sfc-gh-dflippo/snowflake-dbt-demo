---
auto_generated: true
description: 'Snowflake supports three binary formats or encoding schemes: hex, base64,
  and UTF-8.'
last_scraped: '2026-01-14T16:56:07.074232+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/binary-input-output
title: Binary input and output | Snowflake Documentation
---

1. [Overview](../reference.md)
2. [SQL data types reference](../sql-reference-data-types.md)

   * [Summary](../sql-reference/intro-summary-data-types.md)
   * [Numeric](../sql-reference/data-types-numeric.md)
   * [String & binary](../sql-reference/data-types-text.md)

     + [Binary input and output formats](../sql-reference/binary-input-output.md)
     + [Working with binary values](../sql-reference/binary-examples.md)
   * [Logical](../sql-reference/data-types-logical.md)
   * [Date & time](../sql-reference/data-types-datetime.md)
   * [Semi-structured](../sql-reference/data-types-semistructured.md)
   * [Structured](../sql-reference/data-types-structured.md)
   * [Unstructured](../sql-reference/data-types-unstructured.md)
   * [Geospatial](../sql-reference/data-types-geospatial.md)
   * [Vector](../sql-reference/data-types-vector.md)
   * [Unsupported](../sql-reference/data-types-unsupported.md)
   * [Conversion](../sql-reference/data-type-conversion.md)
3. [SQL command reference](../sql-reference-commands.md)
4. [Function and stored procedure reference](../sql-reference-functions.md)
5. [Class reference](../sql-reference-classes.md)
6. [Scripting reference](../sql-reference-snowflake-scripting.md)
7. [General reference](../sql-reference.md)
8. [API reference](../api-reference.md)

[Reference](../reference.md)[SQL data types reference](../sql-reference-data-types.md)[String & binary](../sql-reference/data-types-text.md)Binary input and output formats

# Binary input and output[¶](#binary-input-and-output "Link to this heading")

Snowflake supports three binary formats or encoding schemes: hex, base64, and UTF-8.

## Overview of supported binary formats[¶](#overview-of-supported-binary-formats "Link to this heading")

This section describes the supported binary formats.

### hex (default)[¶](#hex-default "Link to this heading")

The “hex” format refers to the hexadecimal, or base 16, system. In this format, each byte is represented by two characters
(digits from `0` to `9` and letters from `A` to `F`). When using hex to perform conversion:

| From | To | Notes |
| --- | --- | --- |
| Binary | String | hex uses uppercase letters. |
| String | Binary | hex is case-insensitive. |

Hex is the default binary format.

### base64[¶](#base64 "Link to this heading")

The “base64” format encodes binary data (or string data) as printable ASCII characters (letters,
digits, and punctuation marks or mathematical operators).
(The base64 encoding scheme is defined in [RFC 4648](https://tools.ietf.org/html/rfc4648).)

Base64-encoded data has the following advantages:

* Because base64-encoded data is pure ASCII text, it can be stored in systems that support ASCII character data but
  not BINARY data. For example, binary data that represents music (digital samples), or UTF data that represents
  Mandarin language characters, can be encoded as ASCII text and stored in systems that support only ASCII characters.
* Because base64-encoded data doesn’t contain control characters (for example, end-of-transmission characters, tab characters),
  base64-encoded data can be transmitted and received without risk that control characters could
  be interpreted as commands rather than as data. Base64-encoded data is compatible with older modems and
  other telecommunications equipment that transmit and receive data one character at a time (without packet headers
  or protocols that indicate which parts of a packet are data and which are header or control information).

Base64-encoded data has the following disadvantages:

* Converting data back and forth between binary and printable ASCII representations consumes computation resources.
* Base64-encoded data requires approximately 1/3 more storage space than the original data.

The following sections provide technical details on base64 encoding.

#### Details of base64 encoding[¶](#details-of-base64-encoding "Link to this heading")

Each group of three 8-bit bytes (a total of 24 bits) of binary data is re-arranged into four groups of 6 bits each
(still 24 bits). Each of the 64 possible combinations of 6 bits is represented by one of the following 64 printable
ASCII characters:

* Uppercase letters (A - Z)
* Lowercase letters (a - z)
* Decimal digits (0 - 9)
* `+`
* `/`

In addition, the character `=` is used for padding if the length of the input that isn’t an exact multiple of 3.

Because base64-encoded data doesn’t contain whitespace characters (for example, blanks and line breaks), base64-encoded
data can be mixed with whitespace if desired. For example, if the transmitter or receiver has a maximum limit
on line length, the base64-encoded data can be split into individual lines by adding newline characters without
corrupting the data. When using base64 to perform conversion:

| From | To | Notes |
| --- | --- | --- |
| Binary | String | Base64 does not insert any whitespace or line breaks. |
| String | Binary | Base64 ignores all whitespace and line breaks. |

### UTF-8[¶](#utf-8 "Link to this heading")

The UTF-8 format refers to the UTF-8 character encoding for Unicode.

UTF-8 is used for text-to-binary encoding. UTF-8 can’t be used for binary-to-text encoding because not all possible BINARY values
can be converted to valid UTF-8 strings.

This format is convenient for performing one-to-one conversion between binary and string, for reinterpreting the underlying data
as one type or the other rather than actually encoding and decoding.

## Session parameters for binary values[¶](#session-parameters-for-binary-values "Link to this heading")

There are two session parameters that determine how binary values are passed into and out of Snowflake:

* [BINARY\_INPUT\_FORMAT](parameters.html#label-binary-input-format): Specifies the format of VARCHAR input to functions that convert from VARCHAR to BINARY.
  It is used for:

  + Performing conversion to BINARY in the one-argument version of [TO\_BINARY](functions/to_binary).
  + Loading data into Snowflake (if no file format option is specified; see below for details).

  The parameter can be set to `HEX`, `BASE64`, or `UTF-8` (or `UTF8`).
  The parameter values are case-insensitive. The default is `HEX`.
* [BINARY\_OUTPUT\_FORMAT](parameters.html#label-binary-output-format): Specifies the format of VARCHAR output from functions that convert from BINARY to VARCHAR.
  It is used for:

  + Performing conversion to VARCHAR in the one-argument version of [TO\_CHAR , TO\_VARCHAR](functions/to_char).
  + Unloading data from Snowflake (if no file format option is specified; see below for details).
  + Displaying binary data in human-readable format (for example, in the Snowflake web interface) when no binary-to-varchar conversion
    was called explicitly.

  The parameter can be set to `HEX` or `BASE64`. The parameter values are case-insensitive. The default is `HEX`.

  Note

  Because conversion from binary to string can fail with the UTF-8 format, BINARY\_OUTPUT\_FORMAT can’t be set to `UTF-8`. To use
  UTF-8 for conversion in this situation, use the two-argument version of [TO\_CHAR , TO\_VARCHAR](functions/to_char).

The parameters can be set at the account, user, and session levels. Execute the [SHOW PARAMETERS](sql/show-parameters) command to
view the current parameter settings that apply to all operations in the current session.

## File format option for loading/unloading binary values[¶](#file-format-option-for-loading-unloading-binary-values "Link to this heading")

Separate from the binary input and output session parameters, Snowflake provides the BINARY\_FORMAT file format option, which can be
used to explicitly control binary formatting when loading data into or unloading data from Snowflake tables.

This option can be set to `HEX`, `BASE64`, or `UTF-8` (values are case-insensitive). The option affects both data
loading and unloading and, similar to other file format options, can be specified in the following ways:

* In a named file format, which can then be referenced in a named stage or directly in a COPY command.
* In a named stage, which can then be referenced directly in a COPY command.
* Directly in a COPY command.

### Data loading[¶](#data-loading "Link to this heading")

When used for data loading, BINARY\_FORMAT specifies the format of binary values in your staged data files. This option
overrides any value set for the BINARY\_INPUT\_FORMAT parameter in the session (see [Session parameters for binary values](#label-session-parameters-for-binary-values)).

If the option is set to `HEX` or `BASE64`, data loading can fail if the strings in the staged data file aren’t valid hex or
base64. In this case, Snowflake returns an error and then performs the action specified for the ON\_ERROR copy option.

### Data unloading[¶](#data-unloading "Link to this heading")

When used in data unloading, the BINARY\_FORMAT option specifies the format applied to binary values unloaded to the files in the
specified stage. This option overrides any value set for the BINARY\_OUTPUT\_FORMAT parameter in the session
(see [Session parameters for binary values](#label-session-parameters-for-binary-values)).

If the option is set to `UTF-8`, data unloading fails if any binary values in the table contain invalid UTF-8. In this case, Snowflake
returns an error.

## Example input/output[¶](#example-input-output "Link to this heading")

BINARY input/output can be confusing because “what you see isn’t necessarily what you get.”

Consider the following example:

```
CREATE OR REPLACE TABLE binary_table (v VARCHAR, b BINARY);

INSERT INTO binary_table (v, b)
  SELECT 'AB', TO_BINARY('AB');

SELECT v, b FROM binary_table;
```

Copy

```
+----+----+
| V  | B  |
|----+----|
| AB | AB |
+----+----+
```

The outputs for column `v` (VARCHAR) and column `b` appear to be identical. Yet
the value for column `b` was converted to binary. Why does the value in column
`b` look unchanged?

The answer is that the argument to TO\_BINARY is treated as a sequence of
hexadecimal digits (even though it is inside quotes and therefore looks
like a string). The two characters you see are actually interpreted as a pair of
hexadecimal digits that represent one byte of binary data, not two bytes of
string data. (This wouldn’t have worked if the input “string” had
contained characters other than hexadecimal digits; the result would have been an
error message similar to `"String '...' isn't a legal hex-encoded string"`.)

Also, when BINARY data is displayed, by default it is displayed as a
sequence of hexadecimal digits. Thus the data went in as hexadecimal digits
(not a string) and is displayed as hexadecimal digits, so it appears unchanged.

In fact, if the goal was to store the two-character string `AB`, then the code
was wrong. The proper code would use the function [HEX\_ENCODE](functions/hex_encode)
to convert the string to a sequence of hexadecimal digits (or use another “encode” function to
convert to another format, such as base64) before storing the data.
Examples of that are below.

### Hexadecimal (“HEX”) format example[¶](#hexadecimal-hex-format-example "Link to this heading")

One way to enter BINARY data is to encode it as a string of hexadecimal
characters, as shown in the following example.

Start by creating a table with a BINARY column:

```
CREATE OR REPLACE TABLE demo_binary_hex (b BINARY);
```

Copy

If you try to insert an “ordinary” string by using the TO\_BINARY function
to try to convert it to a valid BINARY value, it fails:

```
INSERT INTO demo_binary_hex (b) SELECT TO_BINARY('HELP', 'HEX');
```

Copy

Here’s the error message:

```
100115 (22000): The following string is not a legal hex-encoded value: 'HELP'
```

This time, explicitly convert the input to a string of hexadecimal digits
before inserting it (this will succeed):

```
INSERT INTO demo_binary_hex (b) SELECT TO_BINARY(HEX_ENCODE('HELP'), 'HEX');
```

Copy

Now, retrieve the data:

```
SELECT TO_VARCHAR(b), HEX_DECODE_STRING(TO_VARCHAR(b)) FROM demo_binary_hex;
```

Copy

```
+---------------+----------------------------------+
| TO_VARCHAR(B) | HEX_DECODE_STRING(TO_VARCHAR(B)) |
|---------------+----------------------------------|
| 48454C50      | HELP                             |
+---------------+----------------------------------+
```

As you can see, by default the output is shown as hexadecimal. To get back
the original string, use the function [HEX\_DECODE\_STRING](functions/hex_decode_string)
(the complement of the function HEX\_ENCODE that was used previously to encode the string).

The following query shows in more detail what’s going on internally:

```
SELECT 'HELP',
       HEX_ENCODE('HELP'),
       b,
       HEX_DECODE_STRING(HEX_ENCODE('HELP')),
       TO_VARCHAR(b),
       HEX_DECODE_STRING(TO_VARCHAR(b))
  FROM demo_binary_hex;
```

Copy

```
+--------+--------------------+----------+---------------------------------------+---------------+----------------------------------+
| 'HELP' | HEX_ENCODE('HELP') | B        | HEX_DECODE_STRING(HEX_ENCODE('HELP')) | TO_VARCHAR(B) | HEX_DECODE_STRING(TO_VARCHAR(B)) |
|--------+--------------------+----------+---------------------------------------+---------------+----------------------------------|
| HELP   | 48454C50           | 48454C50 | HELP                                  | 48454C50      | HELP                             |
+--------+--------------------+----------+---------------------------------------+---------------+----------------------------------+
```

### BASE64 format example[¶](#base64-format-example "Link to this heading")

Before reading this section, consider reading [Hexadecimal (“HEX”) format example](#label-hexadecimal-format-example).
The basic concepts are similar, and [Hexadecimal (“HEX”) format example](#label-hexadecimal-format-example) explains them in
more detail.

Start by creating a table with a BINARY column:

```
CREATE OR REPLACE TABLE demo_binary_base64 (b BINARY);
```

Copy

Insert a row:

```
INSERT INTO demo_binary_base64 (b) SELECT TO_BINARY(BASE64_ENCODE('HELP'), 'BASE64');
```

Copy

Retrieve that row:

```
SELECT 'HELP',
       BASE64_ENCODE('HELP'),
       BASE64_DECODE_STRING(BASE64_ENCODE('HELP')),
       TO_VARCHAR(b, 'BASE64'),
       BASE64_DECODE_STRING(TO_VARCHAR(b, 'BASE64'))
 FROM demo_binary_base64;
```

Copy

```
+--------+-----------------------+---------------------------------------------+-------------------------+-----------------------------------------------+
| 'HELP' | BASE64_ENCODE('HELP') | BASE64_DECODE_STRING(BASE64_ENCODE('HELP')) | TO_VARCHAR(B, 'BASE64') | BASE64_DECODE_STRING(TO_VARCHAR(B, 'BASE64')) |
|--------+-----------------------+---------------------------------------------+-------------------------+-----------------------------------------------|
| HELP   | SEVMUA==              | HELP                                        | SEVMUA==                | HELP                                          |
+--------+-----------------------+---------------------------------------------+-------------------------+-----------------------------------------------+
```

### UTF-8 format example[¶](#utf-8-format-example "Link to this heading")

Start by creating a table with a BINARY column:

```
CREATE OR REPLACE TABLE demo_binary_utf8 (b BINARY);
```

Copy

Insert a row:

```
INSERT INTO demo_binary_utf8 (b) SELECT TO_BINARY('HELP', 'UTF-8');
```

Copy

Retrieve that row:

```
SELECT 'HELP',
       TO_VARCHAR(b, 'UTF-8')
  FROM demo_binary_utf8;
```

Copy

```
+--------+------------------------+
| 'HELP' | TO_VARCHAR(B, 'UTF-8') |
|--------+------------------------|
| HELP   | HELP                   |
+--------+------------------------+
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

1. [Overview of supported binary formats](#overview-of-supported-binary-formats)
2. [Session parameters for binary values](#session-parameters-for-binary-values)
3. [File format option for loading/unloading binary values](#file-format-option-for-loading-unloading-binary-values)
4. [Example input/output](#example-input-output)

Related content

1. [String & binary data types](/sql-reference/data-types-text)