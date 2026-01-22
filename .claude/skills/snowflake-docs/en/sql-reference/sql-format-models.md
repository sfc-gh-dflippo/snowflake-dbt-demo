---
auto_generated: true
description: In Snowflake, SQL format models (i.e. literals containing format strings)
  are used to specify how numeric values are converted to text strings and vice versa.
  As such, they can be specified as argumen
last_scraped: '2026-01-14T16:56:28.243070+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/sql-format-models
title: SQL format models | Snowflake Documentation
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

[Reference](../reference.md)[General reference](../sql-reference.md)SQL format models

# SQL format models[¶](#sql-format-models "Link to this heading")

In Snowflake, SQL format models (i.e. literals containing format strings) are used to specify how numeric values are converted to text strings and vice versa. As such, they can be specified as arguments in
the [TO\_CHAR , TO\_VARCHAR](functions/to_char) and [TO\_DECIMAL , TO\_NUMBER , TO\_NUMERIC](functions/to_decimal) conversion functions.

Note

Snowflake also provides some limited SQL format model support for dates, times, and timestamps (see [Date & time functions](functions-date-time) and [Conversion functions](functions-conversion)). Full
support for using SQL format models to format dates, times, and timestamps will be added in a future release.

## Components of a format model[¶](#components-of-a-format-model "Link to this heading")

A format model consists of a string of format elements and literals.

### Format elements[¶](#format-elements "Link to this heading")

Format elements are sequences of digits and/or letters (mostly case-insensitive), and, in some cases, symbols. Format elements can be directly concatenated to each other.

Some format elements are used commonly across all format models for controlling printing and matching input text. Other format elements have specific uses based on the type of values they are used to cast
to/from. For more information, see the following sections in this topic:

* [Format Modifiers and Generic Space Handling](#format-modifiers-and-generic-space-handling)
* [Fixed-position Format Elements](#fixed-position-format-elements)
* [Text-minimal Format Elements](#text-minimal-format-elements)

### Format literals[¶](#format-literals "Link to this heading")

Format literals are sequences that can consist of combinations of:

* Strings of arbitrary characters delimited by double quotes (a double quote is represented as two adjacent double quotes).
* One or more of the following symbols:

  | Symbol/Character | Notes |
  | --- | --- |
  | `.` (period) | In fixed numeric models, treated as a format element when following `0`, `9`, or `X`; otherwise preserved as-is. |
  | `,` (comma) | In numeric models, treated as a format element when following `0`, `9`, or `X`; otherwise preserved as-is. |
  | `;` (semi-colon) | Always preserved as-is. |
  | `:` (colon) | Always preserved as-is. |
  | `-` (minus sign) | Always preserved as-is. |
  | `=` (equal sign) | Always preserved as-is. |
  | `/` (forward slash) | Always preserved as-is. |
  | `(` (left parenthesis) | Always preserved as-is. |
  | `)` (right parenthesis) | Always preserved as-is. |

A literal is always printed as-is, exactly where it was located in the format model.

Here is a brief example of using a SQL format model to print the minus
sign after a number rather than before it. The `MI`
indicates where to put the minus sign if the number is a negative number.

> ```
> select to_varchar(-123.45, '999.99MI') as EXAMPLE;
> ```
>
> Copy

The output would look similar to `123.45-` rather than the default `-123.45`.

More examples are included at the end of this topic.

## Format modifiers and generic space handling[¶](#format-modifiers-and-generic-space-handling "Link to this heading")

The following table lists special format elements that control printing and matching input text, and are common to all format models:

| Element | Description |
| --- | --- |
| `_` (underscore) | Nothing printed; optional space on input. |
| `FM` | Fill mode modifier; toggles between *compact* and *fill* modes for any elements following the modifier in the model. |
| `FX` | Exact match modifier; toggles between *lax* and *exact* match modes for any elements following the modifier in the model. |

Note

The fill mode modifier has no effect on the text-minimal numeric format elements (`TM`, `TM9`, and `TME`).

### Printing output strings using the fill mode modifier[¶](#printing-output-strings-using-the-fill-mode-modifier "Link to this heading")

By default, the fill mode is set to *fill* and the `FM` fill mode modifier toggles it to *compact*; repeated use toggles it back to *fill*, etc.

In most cases, using *fill* mode on printing guarantees that format elements produce output of a fixed width by padding numbers on the left with leading zeros or spaces, and padding text with spaces on
the right. This guarantees that columnar output in fixed-width fonts will be aligned.

In *compact* mode, most format elements produce only minimum-width output (i.e. leading zeros and spaces and trailing spaces are suppressed).

The format elements that don’t adhere to these rules are explicitly noted below.

The exact match modifier, `FX` does not affect printing; the underscore format element prints nothing.

### Parsing input strings using the modifiers[¶](#parsing-input-strings-using-the-modifiers "Link to this heading")

Parsing of input strings is affected by both the fill mode modifier, `FM`, and the exact match modifier `FX`. Initially:

* Fill mode is set to *fill* and `FM` toggles it to *compact* and back.
* Exact match mode is set to *lax* and `FX` toggles it to *exact* and back.

All string matching against format elements and literals during parsing is case-insensitive.

In *lax* mode, the first step of input parsing is skipping leading white space (a sequence of spaces, tabs, LF, CR, FF, and VT characters); the mode at the beginning input is strict if the first format
element is `FX`, and *lax* otherwise.

Note

Only normal space characters are allowed within values to be parsed (i.e. components cannot be on different lines, separated by tabs, etc.).

In the *lax* match mode, spaces within literals are matched against any non-empty input sequence of spaces; non-space characters are matched one-to-one. In the *exact* mode, all characters in a literal
must match the input characters one-to-one.

The numeric format elements are matched against the corresponding digit sequences:

* If both *fill* and *exact* modes are in effect, the number of digits must exactly correspond to the width of the corresponding numeric format elements (leading zeros are expected).
* If *compact* or *lax* mode is in effect, a matching input number must have, at most, the number of digits equal to the maximal width of the format element, and at least one digit; leading zeros are
  ignored.

The textual format elements are matched case-insensitively:

* If both *fill* and *exact* modes are in effect, the number of trailing spaces, up to the max width of the element, is expected.
* Otherwise, spaces after the variable-length textual elements are ignored in *lax* mode, and exact match to the actual word (without padding spaces) is expected in *exact* mode.

Finally, the trailing white space until the end of the input string is ignored if the current mode is *lax*.

Normally, both *lax* and *exact* modes do not allow matching spaces where spaces are not present in the format model or could not be generated by printing the content of format elements in *fill* mode.

Note

This behavior differs from Oracle lax match semantics, where spaces can be inserted in between any two format elements — Snowflake uses stricter matching semantics to avoid excessive false matches
during automatic data type recognition.

Places where spaces should be ignored if present in both *lax* and *exact* modes can be explicitly marked using the `_` (underscore) format element.

As a rule of thumb, a format in *exact* mode recognizes only input strings printed by the same format, while a format in *lax* mode recognizes input strings which were printed by the similar format with
any fill mode modifiers added or removed.

## Numeric format models[¶](#numeric-format-models "Link to this heading")

Numeric format models supports two types:

* Fixed-position (with explicit placement of digits where the `0`, `9`, or `X` format elements are placed)
* Text-minimal (`TM`, `TME`, and `TM9` format elements)

Note

These two types cannot be intermingled within the same model.

### Fixed-position numeric formats[¶](#fixed-position-numeric-formats "Link to this heading")

Note

This section discusses non-negative fixed-position numbers; for more information about positioning of a number’s sign in the output for fixed-position numeric formats, see
[Sign Position for Fixed-Position Formats](#sign-position-for-fixed-position-formats).

Fixed-position numbers are represented using digit elements, `0` or `9`. For example, `999` holds numbers from 1 to 3 decimal digits. The fractional part of the numbers is delimited using separator
elements, `.` (period) or `D`:

* `.` is always rendered as a period.
* To use a different character for the `D` elements, modify the input string to replace all periods with commas and all commas with periods before applying the cast function.

Normally, the leading zeros in the integer part and trailing zeros in the fractional part are replaced with spaces (except when the value of the integer part is zero, in which case it is rendered as a
single `0` character). To suppress this behavior use the `0` format element in place of `9`; the corresponding positions have `0` characters preserved. The format element `B`, when used before
the number, suppresses preserving the last `0` in the integer value (i.e. if you use `B` and the value of the integer part of the number is zero, all digits are rendered as spaces).

The digit group separator `,` (comma) or `G` results in the corresponding group separator character being printed if the number is big enough so the digits are on the both sides of group separator.
An example of a format model useful for printing currency sums would be `999,999.00`.

When there are more digits in the integer part of the number than there are digit positions in the format, all digits are printed as `#` to indicate overflow.

The exponent element causes fixed-position numbers to be normalized so that the first digit in the integer part is 1 to 9 (unless the value of the number is zero, in which case the value of the exponent
is also zero). The `EE` element automatically picks the right number of digits in the exponent, and does not print the `+` sign, while `EEE`, `EEEE`, and `EEEEE` always print the `+` or `-`
sign for the exponent and the requested number of digits (leading zeros are not suppressed). Exponent overflow is indicated by `#` in place of digits.

The exponent indicators print either capital `E` or lowercase `e` depending on the case of the first letter in the format element.

The `X` format element works like `9`, except that hexadecimal digits `0-9A-F` are printed. Currently, hexadecimal fractions are not supported. Similar to `9`, `X` replaces leading zeros with
spaces. The `0` element, when used together with `X` prints hexadecimal digits without leading zero suppression (thus use `000X` to print hex numbers that always contain 4 digits).

Note that `X` prints hexadecimal digits with uppercase Latin letters, and lowercase `x` prints lowercase Latin letters. The hexadecimal `0` format element uses the case of the subsequent `X`
format element.

Normally, hexadecimal numbers are printed as unsigned, i.e. negative numbers have all `1`’s in the most significant bit(s), but using the `X` element together with an explicit sign (`S` or `MI`)
causes the `-` sign to be printed along with the absolute value of the number.

Fixed-position numeric format models report overflow on special values (infinity or not-a-number) of floating point numbers.

#### Fixed-position format elements[¶](#fixed-position-format-elements "Link to this heading")

The following table lists the supported elements for fixed-position formats. Note the following:

* The **Repeatable** column indicates whether an element can be repeated in a format model, otherwise the element can only be used once per format model.
* The **Case-sensitive** column indicates elements where the case of the element affects the format. For example:

  + `EE` processes exponents with an uppercase `E`.
  + `ee` processes exponents with a lowercase `e`.

  All the other elements are case-insensitive.

| Element | Repeatable | Case-sensitive | Description |
| --- | --- | --- | --- |
| `$` |  |  | Dollar sign printed before digits in the number (usually after the sign). |
| `.` (period) |  |  | Decimal fraction separator; always printed as a period. |
| `,` (comma) | ✔ |  | Digit group separator; printed as a comma or blank space. |
| `0` | ✔ |  | Position for a digit; leading/trailing zeros are explicitly printed. |
| `9` | ✔ |  | Position for a digit; leading/trailing zeros are replaced with blank spaces. |
| `B` |  |  | Forces representing a zero value as a space in the subsequent number. |
| `D` |  |  | Decimal fraction separator; alternative for `.` element (see description above). |
| `EE` |  | ✔ | Variable-width exponent, from 2 to 5 characters, with no `+` sign for integers (e.g. `E0`, `E21`, `E200`, `E-200`). |
| `EEE` |  | ✔ | Fixed-width exponent (3 characters); range covers from `E-9` to `E+9`. |
| `EEEE` |  | ✔ | Fixed-width exponent (4 characters); range covers from `E-99` to `E+99`. |
| `EEEEE` |  | ✔ | Fixed-width exponent (5 characters); range covers from `E-324` to `E+308`. |
| `G` | ✔ |  | Digit group separator; alternative for `,` (see description above). |
| `MI` |  |  | Explicit numeric sign place holder; prints a space for positive numbers or a `-` sign for negative numbers. |
| `S` |  |  | Explicit numeric sign place holder; prints a `+` sign for positive numbers or a `-` sign for negative numbers.. |
| `X` | ✔ | ✔ | Hexadecimal digit. |

#### Sign position for fixed-position formats[¶](#sign-position-for-fixed-position-formats "Link to this heading")

By default, fixed-position formats always reserve a space for the number’s sign:

* For non-negative numbers, the default blank space is printed before the first digit.
* For negative numbers, the default blank space and `-` sign are printed before the first digit (or decimal, when the `B` format element is used for fractional numbers).

However, the `S`, `MI`, and `$` format elements can be used to explicitly specify where the sign and/or blank space for the number are located.

For example (underscores, `_`, are used in these examples to indicate where blank spaces are inserted):

| Format Model | `12` prints as: | `-7` prints as: |
| --- | --- | --- |
| `99` | `_12` | `_-7` |
| `S99` | `+12` | `_-7` |
| `99S` | `12+` | `_7-` |
| `MI99` | `_12` | `-_7` |
| `99MI` | `12_` | `_7-` |
| `$99` | `_$12` | `_-$7` |

#### Printing numbers using fixed-position formats and the fill mode modifier[¶](#printing-numbers-using-fixed-position-formats-and-the-fill-mode-modifier "Link to this heading")

In *fill* mode, the variable-length format elements, such as `EE` and `MI`, are space-padded on the right.

In *compact* mode, all spaces resulting from numeric format elements, including the variable-length elements, are removed, so the resulting strings are shorter and no longer aligned. For
example (note the lack of blank spaces):

| Format Model | `12` prints as: | `-7` prints as: |
| --- | --- | --- |
| `FM99` | `12` | `-7` |

#### Parsing numbers using fixed-position formats and the modifiers[¶](#parsing-numbers-using-fixed-position-formats-and-the-modifiers "Link to this heading")

Parsing strings containing numbers is affected by both the `FX` and `FM` modifiers:

* In *lax* mode:

  + Digit group separators are optional (i.e. numbers with or without group separators match — though numbers of digits between respective group separators must match); it also permits `+` as a valid
    match for the `MI` format element.
  + The *lax* mode does not disable requirement that digits (even leading or trailing zeros) must be present to match `0` format elements.
  + Spaces between the leading sign and the first digit are allowed in *lax* mode.
  + Also, in *lax* mode, all the exponent format elements (`EE`, `EEE`, `EEEE`, and `EEEEE`) are treated as `EE`, and match an exponent specification with 1 to 3 digits and optional `+` or `-`
    sign.
  + Use `B` to allow matching numbers with no digits in the integer part. The decimal dot before an empty fractional part is optional in *lax* mode.
* In *exact* mode:

  + The number must have a proper number of spaces in place of omitted digits to match the format (i.e. in *fill* mode, it is spaces and, in *compact* mode, it is a lack of spaces).
  + Omitting group separators is not allowed under *exact* mode, and `MI` won’t match the `+` sign.
  + The exponent format elements other than `EE` must match the sign place and the exact number of digits required by the format element.
  + The decimal dot in the place specified by the format model is mandatory.

### Text-minimal numeric formats[¶](#text-minimal-numeric-formats "Link to this heading")

While fixed-position numeric format models always explicitly specify the number of digits, the text-minimal format elements use a minimal number of digits based on the value of the number. The `TM*` format
elements always produce variable-length output with no spaces, regardless of the fill mode modifier (*fill* or *compact*).

* `TM9` prints the number as an integer or decimal fraction, based on the value of the number. Any decimal fixed-point number value is printed precisely with the number of digits in the fractional part
  determined by the scale of the number (trailing zeros are preserved in *fill* mode).
* For floating-point numbers, `TM9` picks the number of fractional digits based on the number’s exponent (note that precise binary to decimal fraction conversion is not possible). If the floating-point
  number’s magnitude is too large, causing the positional notation to be too long, it switches to scientific notation (see `TME` below). If the floating-point number is too small, `TM9` prints zero.
* `TME` prints the number in scientific notation, i.e. with exponent (same as `EE`) and one digit in the integer position of the fractional part. The case of the exponent indicator (`E` or `e`)
  matches the case of the first letter (`T` or `t`) in the format element.
* `TM` chooses either `TM9` or `TME` depending on the magnitude of the number, to minimize the length of the text while preserving precision.

#### Text-minimal format elements[¶](#text-minimal-format-elements "Link to this heading")

The following table lists the supported elements for text-minimal formats. Note the following:

* No elements can be repeated within a text-minimal format string.
* The **Case-sensitive** column indicates elements where the case of the element affects the format. For example:

  + `TME` processes exponents with an uppercase `E`.
  + `tme` processes exponents with a lowercase `e`.

  All the other elements are case-insensitive.

| Element | Repeatable | Case-sensitive | Description |
| --- | --- | --- | --- |
| `$` |  |  | Dollar sign is inserted before digits in the number (usually after sign). |
| `TM` |  | ✔ | Text-minimal number, either `TM9` or `TME`, whichever is shorter. |
| `TM9` |  | ✔ | Text-minimal number in positional notation. |
| `TME` |  | ✔ | Text-minimal number in scientific notation (with exponent). |
| `B` |  |  | Forces representing a zero value as a space in the subsequent number. |
| `MI` |  |  | Explicit numeric sign place holder; becomes either `-` or a space. |
| `S` |  |  | Explicit numeric sign place holder; becomes either `-` or `+`. |

#### Sign position for text-minimal formats[¶](#sign-position-for-text-minimal-formats "Link to this heading")

By default, the sign for text-minimal formats is either:

* `-` for negative numbers, prepended to the number.
* Omitted for non-negative numbers.

The `$`, `S`, and `MI` elements have the same effect as with fixed-position format models. Note that floating-point numbers have two distinct zero values (`+0.` and `-0.`) which represent
infinitesimal positive and negative values, respectively.

#### Parsing numbers using text-minimal formats and the modifiers[¶](#parsing-numbers-using-text-minimal-formats-and-the-modifiers "Link to this heading")

Parsing with the text-minimal format models is not affected by the `FX` or `FM` modifiers; however, the explicit sign elements, `S` and `MI` are affected, as described above.

`TM9` matches any decimal number (integer or fractional) in positional notation; it does not match numbers in scientific notation (i.e. with exponent). Conversely:

* `TME` matches only scientific notation.
* `TM` matches both.

Numbers matched by text-minimal elements cannot have spaces or digit group separators within them.

Letters within exponent elements and hexadecimal digits are always matched without regard to case (lower or upper).

## Alternate, automatic, and default formats[¶](#alternate-automatic-and-default-formats "Link to this heading")

| Element | Description |
| --- | --- |
| `|` (pipe) | Separates alternative formats. |
| `AUTO` | Automatic format(s). |

When parsing strings, it is possible to specify multiple alternative formats by separating format strings with the `|` character. The string is successfully parsed if it matches any one format. If the
input string matches multiple formats, any format will be used for the conversion.

An entire format used for parsing can be replaced with the keyword `AUTO`; this inserts one or more alternative automatic formats depending on the type of the source or result value. Adding a custom format
to the automatic format(s) can be done using `AUTO` as one of the alternatives.

Default formats are used when formats are not explicitly specified in cast functions, for parsing input values (i.e. in CSV files), and for printing results.

### Default formats for printing[¶](#default-formats-for-printing "Link to this heading")

The following table lists the default formats for printing:

| SQL Data Type | Parameter | Default Format |
| --- | --- | --- |
| DECIMAL | *none* | `TM9` |
| DOUBLE | *none* | `TME` |

### Default formats for parsing[¶](#default-formats-for-parsing "Link to this heading")

The following table lists the default formats for parsing:

| SQL Data Type | Parameter | Default `AUTO` Format |
| --- | --- | --- |
| DECIMAL | *None* | `TM9` |
| DOUBLE | *None* | `TME` |

The list of formats used for automatic optimistic string conversion (i.e. for strings which are automatically recognized as numeric) is the union of all the formats in the above table of default input
formats.

## Examples[¶](#examples "Link to this heading")

### Output examples[¶](#output-examples "Link to this heading")

This example shows how to display numbers with leading zeros:

> ```
> create table sample_numbers (f float);
> insert into sample_numbers (f) values (1.2);
> insert into sample_numbers (f) values (123.456);
> insert into sample_numbers (f) values (1234.56);
> insert into sample_numbers (f) values (-123456.789);
> select to_varchar(f, '999,999.999'), to_varchar(f, 'S000,000.000') from sample_numbers;
> ```
>
> Copy

The output will look similar to:

> ```
> +------------------------------+-------------------------------+
> | TO_VARCHAR(F, '999,999.999') | TO_VARCHAR(F, 'S000,000.000') |
> +==============================+===============================+
> |        1.2                   | +000,001.200                  |
> +------------------------------+-------------------------------+
> |      123.456                 | +000,123.456                  |
> +------------------------------+-------------------------------+
> |    1,234.56                  | +001,234.560                  |
> +------------------------------+-------------------------------+
> | -123,456.789                 | -123,456.789                  |
> +------------------------------+-------------------------------+
> ```
>
> Copy

You don’t need leading zeros in order to align numbers. The default fill mode
is “fill”, which means that leading blanks are used to align numbers based
on the positions of the decimal points.

> ```
> select to_varchar(f, '999,999.999'), to_varchar(f, 'S999,999.999') from sample_numbers;
> ```
>
> Copy

The output will look similar to:

> ```
> +------------------------------+-------------------------------+
> | TO_VARCHAR(F, '999,999.999') | TO_VARCHAR(F, 'S999,999.999') |
> +==============================+===============================+
> |        1.2                   |       +1.2                    |
> +------------------------------+-------------------------------+
> |      123.456                 |     +123.456                  |
> +------------------------------+-------------------------------+
> |    1,234.56                  |   +1,234.56                   |
> +------------------------------+-------------------------------+
> | -123,456.789                 | -123,456.789                  |
> +------------------------------+-------------------------------+
> ```
>
> Copy

This example shows what happens if you use the FM (Fill Mode) modifier to
switch from “fill” mode to “compact” mode, i.e. to remove leading characters
that would align the numbers:

> ```
> select  to_varchar(f, '999,999.999'), to_varchar(f, 'FM999,999.999') from sample_numbers;
> ```
>
> Copy

The output will look similar to:

> ```
> +------------------------------+--------------------------------+
> | TO_VARCHAR(F, '999,999.999') | TO_VARCHAR(F, 'FM999,999.999') |
> +==============================+================================+
> |        1.2                   | 1.2                            |
> +------------------------------+--------------------------------+
> |      123.456                 | 123.456                        |
> +------------------------------+--------------------------------+
> |    1,234.56                  | 1,234.56                       |
> +------------------------------+--------------------------------+
> | -123,456.789                 | -123,456.789                   |
> +------------------------------+--------------------------------+
> ```
>
> Copy

This example shows how to display numbers in exponential notation:

> ```
> select to_char(1234, '9d999EE'), 'will look like', '1.234E3';
> ```
>
> Copy

The output will look similar to:

> ```
> +--------------------------+------------------+-----------+
> | TO_CHAR(1234, '9D999EE') | 'WILL LOOK LIKE' | '1.234E3' |
> +==========================+==================+===========+
> | 1.234E3                  |  will look like  |  1.234E3  |
> +--------------------------+------------------+-----------+
> ```
>
> Copy

This shows how to include literals in the output. The literal portions
are enclosed within double quotes (which, in turn, are inside the
single quotes that delimit the string).

> ```
> select to_char(12, '">"99"<"');
> ```
>
> Copy

The output will look similar to:

> ```
> +-------+
> | > 12< |
> +-------+
> ```
>
> Copy

### Input examples[¶](#input-examples "Link to this heading")

These examples demonstrate the use of format models for inputs.

> The following example shows some simple input operations, with an emphasis
> on showing the difference between using “0” and “9” to specify format of digits.
>
> The digit “9” as a formatter will accept blanks or “missing” leading digits.
> The digit “0” as a formatter will not accept blanks or missing leading zeros.
>
> ```
> -- All of the following convert the input to the number 12,345.67.
> SELECT TO_NUMBER('012,345.67', '999,999.99', 8, 2);
> SELECT TO_NUMBER('12,345.67', '999,999.99', 8, 2);
> SELECT TO_NUMBER(' 12,345.67', '999,999.99', 8, 2);
> -- The first of the following works, but the others will not convert.
> -- (They are not supposed to convert, so "failure" is correct.)
> SELECT TO_NUMBER('012,345.67', '000,000.00', 8, 2);
> SELECT TO_NUMBER('12,345.67', '000,000.00', 8, 2);
> SELECT TO_NUMBER(' 12,345.67', '000,000.00', 8, 2);
> ```
>
> Copy
>
> This shows how to accept either of two numeric formats
> (`-###` or `###-`).
>
> ```
> -- Create the table and insert data.
> create table format1 (v varchar, i integer);
> insert into format1 (v) values ('-101');
> insert into format1 (v) values ('102-');
> insert into format1 (v) values ('103');
>
> -- Try to convert varchar to integer without a
> -- format model.  This fails (as expected)
> -- with a message similar to:
> --    "Numeric value '102-' is not recognized"
> update format1 set i = TO_NUMBER(v);
>
> -- Now try again with a format specifier that allows the minus sign
> -- to be at either the beginning or the end of the number.
> -- Note the use of the vertical bar ("|") to indicate that
> -- either format is acceptable.
> update format1 set i = TO_NUMBER(v, 'MI999|999MI');
> select i from format1;
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

1. [Components of a format model](#components-of-a-format-model)
2. [Format modifiers and generic space handling](#format-modifiers-and-generic-space-handling)
3. [Numeric format models](#numeric-format-models)
4. [Alternate, automatic, and default formats](#alternate-automatic-and-default-formats)
5. [Examples](#examples)