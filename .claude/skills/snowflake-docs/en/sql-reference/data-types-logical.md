---
auto_generated: true
description: This topic describes the logical data types supported in Snowflake.
last_scraped: '2026-01-14T16:56:09.596875+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/data-types-logical
title: Logical data types | Snowflake Documentation
---

1. [Overview](../reference.md)
2. [SQL data types reference](../sql-reference-data-types.md)

   * [Summary](intro-summary-data-types.md)
   * [Numeric](data-types-numeric.md)
   * [String & binary](data-types-text.md)
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

[Reference](../reference.md)[SQL data types reference](../sql-reference-data-types.md)Logical

# Logical data types[¶](#logical-data-types "Link to this heading")

This topic describes the logical data types supported in Snowflake.

## Data types[¶](#data-types "Link to this heading")

Snowflake supports a single logical data type (BOOLEAN).

### BOOLEAN[¶](#boolean "Link to this heading")

BOOLEAN can have TRUE or FALSE values. BOOLEAN can also have an UNKNOWN value, which is represented by NULL.
BOOLEAN columns can be used in expressions (for example, a [SELECT](sql/select) list),
as well as predicates (for example, a [WHERE](constructs/where) clause).

The BOOLEAN data type enables support for [Ternary logic](ternary-logic).

## BOOLEAN conversion[¶](#boolean-conversion "Link to this heading")

Snowflake supports conversion to and from BOOLEAN.

### Conversion to BOOLEAN[¶](#conversion-to-boolean "Link to this heading")

Non-BOOLEAN values can be converted to BOOLEAN values explicitly or implicitly.

#### Explicit conversion[¶](#explicit-conversion "Link to this heading")

You can explicitly convert specific [text string](data-types-text.html#label-character-datatypes) and [numeric](data-types-numeric) values
to BOOLEAN values by using the [TO\_BOOLEAN](functions/to_boolean) or [CAST](functions/cast) functions:

String conversion:
:   * Strings converted to TRUE: `'true'`, `'t'`, `'yes'`, `'y'`, `'on'`, `'1'`.
    * Strings converted to FALSE: `'false'`, `'f'`, `'no'`, `'n'`, `'off'`, `'0'`.
    * Conversion is case-insensitive.
    * Other text strings can’t be converted to BOOLEAN values.

Numeric conversion:
:   * Zero (`0`) is converted to FALSE.
    * Any non-zero value is converted to TRUE.

#### Implicit conversion[¶](#implicit-conversion "Link to this heading")

Snowflake can implicitly convert specific text string and numeric values to BOOLEAN values:

String conversion:
:   * `'true'` is converted to TRUE.
    * `'false'` is converted to FALSE.
    * Conversion is case-insensitive.

Numeric conversion:
:   * Zero (`0`) is converted to FALSE.
    * Any non-zero value is converted to TRUE.

### Conversion from BOOLEAN[¶](#conversion-from-boolean "Link to this heading")

BOOLEAN values can be converted to non-BOOLEAN values explicitly or implicitly.

#### Explicit conversion[¶](#id1 "Link to this heading")

You can explicitly cast BOOLEAN values to text string or numeric values:

String conversion:
:   * TRUE is converted to `'true'`.
    * FALSE is converted to `'false'`.

Numeric conversion:
:   * TRUE is converted to `1`.
    * FALSE is converted to `0`.

#### Implicit conversion[¶](#id2 "Link to this heading")

Snowflake can implicitly convert BOOLEAN values to text string values:

String conversion:
:   * TRUE is converted to `'true'`.
    * FALSE is converted to `'false'`.

## Examples[¶](#examples "Link to this heading")

Create a table and insert values:

```
CREATE OR REPLACE TABLE test_boolean(
  b BOOLEAN,
  n NUMBER,
  s STRING);

INSERT INTO test_boolean VALUES
  (true, 1, 'yes'),
  (false, 0, 'no'),
  (NULL, NULL, NULL);

SELECT * FROM test_boolean;
```

Copy

```
+-------+------+------+
| B     |    N | S    |
|-------+------+------|
| True  |    1 | yes  |
| False |    0 | no   |
| NULL  | NULL | NULL |
+-------+------+------+
```

The following query includes a BOOLEAN-typed expression:

```
SELECT b, n, NOT b AND (n < 1) FROM test_boolean;
```

Copy

```
+-------+------+-------------------+
| B     |    N | NOT B AND (N < 1) |
|-------+------+-------------------|
| True  |    1 | False             |
| False |    0 | True              |
| NULL  | NULL | NULL              |
+-------+------+-------------------+
```

The following example uses a BOOLEAN column in predicates:

```
SELECT * FROM test_boolean WHERE NOT b AND (n < 1);
```

Copy

```
+-------+---+----+
| B     | N | S  |
|-------+---+----|
| False | 0 | no |
+-------+---+----+
```

The following example casts a text value to a BOOLEAN value. The example uses
the [SYSTEM$TYPEOF](functions/system_typeof) to show the type of the value
after the conversion.

```
SELECT s,
       TO_BOOLEAN(s),
       SYSTEM$TYPEOF(TO_BOOLEAN(s))
  FROM test_boolean;
```

Copy

```
+------+---------------+------------------------------+
| S    | TO_BOOLEAN(S) | SYSTEM$TYPEOF(TO_BOOLEAN(S)) |
|------+---------------+------------------------------|
| yes  | True          | BOOLEAN[SB1]                 |
| no   | False         | BOOLEAN[SB1]                 |
| NULL | NULL          | BOOLEAN[SB1]                 |
+------+---------------+------------------------------+
```

The following example casts a number value to a BOOLEAN value:

```
SELECT n,
       TO_BOOLEAN(n),
       SYSTEM$TYPEOF(TO_BOOLEAN(n))
  FROM test_boolean;
```

Copy

```
+------+---------------+------------------------------+
| N    | TO_BOOLEAN(N) | SYSTEM$TYPEOF(TO_BOOLEAN(N)) |
|------+---------------+------------------------------|
| 1    | True          | BOOLEAN[SB1]                 |
| 0    | False         | BOOLEAN[SB1]                 |
| NULL | NULL          | BOOLEAN[SB1]                 |
+------+---------------+------------------------------+
```

In this example, Snowflake implicitly converts a BOOLEAN value to a text value:

```
SELECT 'Text for ' || s || ' is ' || b AS result,
       SYSTEM$TYPEOF('Text for ' || s || ' is ' || b) AS type_of_result
  FROM test_boolean;
```

Copy

```
+----------------------+-------------------------+
| RESULT               | TYPE_OF_RESULT          |
|----------------------+-------------------------|
| Text for yes is true | VARCHAR(134217728)[LOB] |
| Text for no is false | VARCHAR(134217728)[LOB] |
| NULL                 | VARCHAR(134217728)[LOB] |
+----------------------+-------------------------+
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

1. [Data types](#data-types)
2. [BOOLEAN conversion](#boolean-conversion)
3. [Examples](#examples)

Related content

1. [Ternary logic](/sql-reference/ternary-logic)
2. [Conversion functions](/sql-reference/functions-conversion)
3. [Data type conversion](/sql-reference/data-type-conversion)