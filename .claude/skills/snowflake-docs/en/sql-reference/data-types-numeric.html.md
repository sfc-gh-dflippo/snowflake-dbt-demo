---
auto_generated: true
description: This topic describes the numeric data types supported in Snowflake, along
  with the supported formats for numeric constants and literals.
last_scraped: '2026-01-14T16:57:59.302262+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/data-types-numeric.html
title: Numeric data types | Snowflake Documentation
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

[Reference](../reference.md)[SQL data types reference](../sql-reference-data-types.md)Numeric

# Numeric data types[¶](#numeric-data-types "Link to this heading")

This topic describes the numeric data types supported in Snowflake, along with the supported formats for numeric constants
and literals.

## Data types for fixed-point numbers[¶](#data-types-for-fixed-point-numbers "Link to this heading")

Snowflake supports the following data types for fixed-point numbers.

### NUMBER[¶](#number "Link to this heading")

Numbers up to 38 digits, with an optional precision and scale:

Precision:
:   Total number of digits allowed.

Scale:
:   Number of digits allowed to the right of the decimal point.

By default, precision is 38, and scale is 0; that is, NUMBER(38, 0). Precision limits the range
of values that can be inserted into or cast to columns of a given type. For example, the value `999` fits into
NUMBER(38,0) but not into NUMBER(2,0).

Because precision is the total number of digits allowed, you can’t load a value into a NUMBER column if the number
of digits to the left of the decimal point exceeds the precision of the column minus its scale. For example,
NUMBER(20, 2) allows 18 digits on the left side of the decimal point and two digits on the right side of the decimal
point, for a total of 20 digits.

The *maximum scale*, which is the number of digits to the right of the decimal point, is 37. Numbers that have fewer than 38
significant digits, but whose least significant digit is past the 37th decimal place — for example,
0.0000000000000000000000000000000000000012 (1.2e-39) — can’t be represented without losing some digits of precision.

Note

If data is converted to another data type with lower precision, and then converted back to the higher-precision data
type, the data can lose precision. For example, precision is lost if you convert a NUMBER(38,37) value to a DOUBLE value
— which has a precision of approximately 15 decimal digits — and then back to NUMBER.

Snowflake also supports the [FLOAT](#label-data-type-float) data type, which allows a wider range of values,
although with less precision.

### DECIMAL , DEC , NUMERIC[¶](#decimal-dec-numeric "Link to this heading")

Synonymous with NUMBER.

### INT , INTEGER , BIGINT , SMALLINT , TINYINT , BYTEINT[¶](#int-integer-bigint-smallint-tinyint-byteint "Link to this heading")

Synonymous with NUMBER, except that precision and scale can’t be specified (that is, it always defaults to NUMBER(38, 0)).
Therefore, for all INTEGER data types, the range of values is all integer values from
-99999999999999999999999999999999999999 to +99999999999999999999999999999999999999 (inclusive).

The various names — for example, TINYINT, BYTEINT, and so on —are to simplify porting from other systems and to suggest
the expected range of values for a column of the specified type.

### Impact of precision and scale on storage size[¶](#impact-of-precision-and-scale-on-storage-size "Link to this heading")

Precision — the total number of digits — doesn’t affect storage. The storage requirements for the same number in columns with
different precisions, such as NUMBER(2,0) and NUMBER(38,0), are the same. For each micro-partition, Snowflake determines
the minimum and maximum values for a given column and uses that information to determine the storage size for all values
for that column in the partition. For example:

* If a column contains only values between `-128` and `+127`, each of the values consumes 1 byte (uncompressed).
* If the largest value in the column is `10000000`, each of the values consumes 4 bytes (uncompressed).

However, scale — the number of digits following the decimal point — affects storage. For example, the same value stored in
a column of type NUMBER(10,5) consumes more space than NUMBER(5,0). Also, processing values with a larger scale might be
slightly slower and consume more memory.

To save space, Snowflake compresses values before writing them to storage. The amount of compression depends on the data
values and other factors.

### Examples of fixed-point data types in a table[¶](#examples-of-fixed-point-data-types-in-a-table "Link to this heading")

The following statement creates a table with columns of various fixed-point data types:

```
CREATE OR REPLACE TABLE test_fixed(
  num0 NUMBER,
  num10 NUMBER(10,1),
  dec20 DECIMAL(20,2),
  numeric30 NUMERIC(30,3),
  int1 INT,
  int2 INTEGER);

DESC TABLE test_fixed;
```

Copy

```
+-----------+--------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+----------------+
| name      | type         | kind   | null? | default | primary key | unique key | check | expression | comment | policy name | privacy domain |
|-----------+--------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+----------------|
| NUM0      | NUMBER(38,0) | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL           |
| NUM10     | NUMBER(10,1) | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL           |
| DEC20     | NUMBER(20,2) | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL           |
| NUMERIC30 | NUMBER(30,3) | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL           |
| INT1      | NUMBER(38,0) | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL           |
| INT2      | NUMBER(38,0) | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL           |
+-----------+--------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+----------------+
```

## Data types for floating-point numbers[¶](#data-types-for-floating-point-numbers "Link to this heading")

Snowflake supports the following data types for floating-point numbers.

### FLOAT , FLOAT4 , FLOAT8[¶](#float-float4-float8 "Link to this heading")

The names FLOAT, FLOAT4, and FLOAT8 are for compatibility with other systems. Snowflake treats all three as 64-bit
floating-point numbers.

#### Precision[¶](#precision "Link to this heading")

Snowflake uses double-precision (64 bit) IEEE 754 floating-point numbers.

Precision is approximately 15 digits. For example, for integers, the range is from -9007199254740991 to +9007199254740991
(-253 + 1 to +253 - 1). Floating-point values can range from approximately
10-308 to 10+308. Snowflake can represent more extreme values between approximately 10-324
and 10-308 with less precision. For more details, see the
[Wikipedia article on double-precision numbers](https://en.wikipedia.org/wiki/Double-precision_floating-point_format).

Snowflake supports the fixed-point data type [NUMBER](#label-data-type-number), which allows greater precision,
although a smaller range of exponents.

#### Special values[¶](#special-values "Link to this heading")

Snowflake supports the following special values for FLOAT:

* `'NaN'` (not a number)
* `'inf'` (infinity)
* `'-inf'` (negative infinity)

The symbols `'NaN'`, `'inf'`, and `'-inf'` must be in single quotes, and are case-insensitive.

Comparison semantics for `'NaN'` differ from the IEEE 754 standard in the following ways:

| Condition | Snowflake | IEEE 754 | Comment |
| --- | --- | --- | --- |
| `'NaN' = 'NaN'` | `TRUE` | `FALSE` | In Snowflake, `'NaN'` values are all equal. |
| `'NaN' > X` . where `X` is any FLOAT value, including . infinity, other than `NaN` itself. | `TRUE` | `FALSE` | In Snowflake, `'NaN'` is greater . than any other FLOAT value, . including infinity. |

#### Rounding errors[¶](#rounding-errors "Link to this heading")

Floating point operations can have small rounding errors in the least significant digits. Rounding errors can occur in any type
of floating-point processing, including trigonometric, statistical, and geospatial functions.

The following list shows considerations for rounding errors:

* Errors can vary each time the query is executed.
* Errors can be larger when operands have different precision or scale.
* Errors can accumulate, especially when aggregate functions —for example, [SUM](functions/sum)
  or [AVG](functions/avg) — process large numbers of rows. Casting to a fixed-point data type before
  aggregating can reduce or eliminate these errors.
* Rounding errors can occur not only when working with SQL, but also when working with other code — for example, Java,
  JavaScript, or Python — that runs inside Snowflake — for example, in
  [UDFs](../developer-guide/udf/udf-overview) and
  [stored procedures](../developer-guide/stored-procedure/stored-procedures-overview).
* When comparing two floating-point numbers, Snowflake recommends comparing for approximate equality rather than exact equality.

It might be possible to avoid these types of approximation errors by using the exact [DECFLOAT](#label-data-type-decfloat) data type.

### DOUBLE , DOUBLE PRECISION , REAL[¶](#double-double-precision-real "Link to this heading")

Synonymous with FLOAT.

### Examples of floating-point data types in a table[¶](#examples-of-floating-point-data-types-in-a-table "Link to this heading")

The following statement creates a table with columns of various floating-point data types:

```
CREATE OR REPLACE TABLE test_float(
  double1 DOUBLE,
  float1 FLOAT,
  dp1 DOUBLE PRECISION,
  real1 REAL);

DESC TABLE test_float;
```

Copy

```
+---------+-------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+----------------+
| name    | type  | kind   | null? | default | primary key | unique key | check | expression | comment | policy name | privacy domain |
|---------+-------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+----------------|
| DOUBLE1 | FLOAT | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL           |
| FLOAT1  | FLOAT | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL           |
| DP1     | FLOAT | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL           |
| REAL1   | FLOAT | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL           |
+---------+-------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+----------------+
```

Note

The DESC TABLE command’s `type` column displays the data type FLOAT not only for FLOAT, but also for synonyms
of FLOAT; for example, DOUBLE, DOUBLE PRECISION, and REAL.

### DECFLOAT[¶](#decfloat "Link to this heading")

The decimal float (DECFLOAT) data type stores numbers exactly, with up to 38 significant digits of precision,
and uses a dynamic base-10 exponent to represent very large or small values. The exponent range is from -16383
to 16384, allowing values approximately between -10^(16384) and 10^(16384). The DECFLOAT data type supports a variable
scale so that the scale varies depending on the specific value being stored. In contrast to the FLOAT data type,
which represents values as approximations, the DECFLOAT data type represents exact values in the specified precision.

The DECFLOAT data type doesn’t support the following [special values](#label-data-type-float-special-values)
that are supported by the FLOAT data type: `'NaN'` (not a number), `'inf'` (infinity),
and `'-inf'` (negative infinity).

#### Use cases for the DECFLOAT data type[¶](#use-cases-for-the-decfloat-data-type "Link to this heading")

Use the DECFLOAT data type when you need exact decimal results and a wide, variable scale in the same column.

The DECFLOAT data type is appropriate for the following general use cases:

* You are ingesting data, and the scale of incoming numeric values is unknown or highly variable.
* You require exact numeric values; for example, ledgers, taxes, or compliance.
* You are migrating from systems that rely on the IEEE 754-decimal representation or 128-bit decimals. These
  migrations might be blocked by the precision or range limitations of other Snowflake data types.
* You want to avoid `Number out of representable range` errors when you sum, multiply, or divide high-precision
  numeric values.

For example, you can use the DECFLOAT data type for the following specific use cases:

* You are ingesting heterogeneously scaled data from Oracle DECIMAL or DB2 DECFLOAT columns.
* You are performing financial modeling that involves computations with scales of results that are hard to predict.
* You are running scientific measurements that swing from nano units to astronomical units.

You can continue to use the NUMBER data type for fixed-scale numeric columns or the FLOAT data type for high-throughput
analytics where imprecise results are acceptable.

#### Usage notes for the DECFLOAT data type[¶](#usage-notes-for-the-decfloat-data-type "Link to this heading")

* If an operation produces a result with more than 38 digits, the DECFLOAT value is rounded to 38-digit precision,
  with the least-significant digits rounded off according to the current rounding mode. Snowflake uses
  the [half up rounding mode](https://en.wikipedia.org/wiki/Rounding#Rounding_half_up) for DECFLOAT
  values.
* When you specify a DECFLOAT value or you cast to a DECFLOAT value, avoid using numeric literals in SQL. If you
  use numeric literals in SQL, the values are interpreted as NUMBER or FLOAT values before being cast to a DECFLOAT value,
  which can result in range errors or loss of exactness. Instead, use either string literals — such as `SELECT '<value>'::DECFLOAT`
  — or the DECFLOAT literal — such as `SELECT DECFLOAT '<value>'`.
* When operations mix DECFLOAT values and values of other numeric types, coercion prefers the DECFLOAT values.
  For example, when you add a value of NUMBER type and DECFLOAT type, the result is a DECFLOAT value.
* Use of the DECFLOAT type might cause storage consumption to increase.

#### Drivers and driver versions that support the DECFLOAT data type[¶](#drivers-and-driver-versions-that-support-the-decfloat-data-type "Link to this heading")

The following Snowflake drivers and driver versions support the DECFLOAT data type. You might need to update your drivers
to the versions that support DECFLOAT:

| Driver | Minimum supported version | Notes |
| --- | --- | --- |
| Snowflake Connector for Python | 3.14.1 | pandas DataFrames don’t support the DECFLOAT type. |
| ODBC | 3.12.0 | None. |
| JDBC | 3.27.0 | None. |
| Go Snowflake Driver | 1.17.0 | None. |
| SQL API | 2.0.0 | None. |

Unsupported drivers treat DECFLOAT values as TEXT values. For some drivers, a driver parameter must be set to map
the DECFLOAT type to a language-native type. For more information, see [Drivers](../developer-guide/drivers).

#### Limitations for the DECFLOAT data type[¶](#limitations-for-the-decfloat-data-type "Link to this heading")

The following limitations apply to the DECFLOAT type:

* DECFLOAT values can’t be stored in VARIANT, OBJECT, or ARRAY values. To cast a DECFLOAT value to a VARIANT value,
  you can first cast it to a VARCHAR value, and then cast it to a VARIANT value.
* DECFLOAT values aren’t supported in the following types of tables:

  + Tables in external formats, such as Iceberg
  + Hybrid tables
* The DECFLOAT data type isn’t supported in Snowflake Scripting stored procedures. However, it is supported in
  Snowflake Scripting user-defined functions (UDFs).
* The DECFLOAT data type isn’t supported in stored procedures or UDFs written in a language other than SQL,
  such as Python or Java.
* The DECFLOAT data type isn’t supported in Snowpark.
* Snowsight has limited support for the DECFLOAT data type.
* The following features don’t support the DECFLOAT data type:

  + [Clustering keys](../user-guide/tables-clustering-keys)
  + [Differential privacy](../user-guide/diff-privacy/differential-privacy-sql-reference)
  + [Sensitive data classification](../user-guide/classify-intro)
  + [Search optimization service](../user-guide/search-optimization-service)
* The NUMBER and FLOAT types might provide better performance than the DECFLOAT type.

#### Examples for the DECFLOAT data type[¶](#examples-for-the-decfloat-data-type "Link to this heading")

The following examples use the DECFLOAT data type:

* [Show the differences between DECFLOAT and FLOAT](#label-decfloat-example-differences-with-float)
* [Use DECFLOAT values with aggregate functions](#label-decfloat-example-aggregate-functions)

##### Show the differences between DECFLOAT and FLOAT[¶](#show-the-differences-between-decfloat-and-float "Link to this heading")

The following example shows the differences between the DECFLOAT and FLOAT data types:

1. Create a table with a DECFLOAT column and a FLOAT column, and then insert the same values for both types into the table:

   ```
   CREATE OR REPLACE TABLE decfloat_sample (
     id INT,
     decfloat_val DECFLOAT,
     float_val FLOAT);

   INSERT INTO decfloat_sample VALUES
     (
       1,
       DECFLOAT '123e7000',
       FLOAT '123e7000'
     ),
     (
       2,
       12345678901234567890123456789::DECFLOAT,
       12345678901234567890123456789::FLOAT
     ),
     (
       3,
       '-4.2e-5432'::DECFLOAT,
       '-4.2e-5432'::FLOAT
     ),
     (
       4,
       '1.00000000000000000000000000000000000014'::DECFLOAT,
       '1.00000000000000000000000000000000000014'::FLOAT
     ),
     (
       5,
       '1.00000000000000000000000000000000000015'::DECFLOAT,
       '1.00000000000000000000000000000000000015'::FLOAT
     );
   ```

   Copy

   The statement inserts DECFLOAT values in the following ways:

   * The first value is inserted by using the DECFLOAT literal.
   * The second value is inserted by casting an INTEGER value to a DECFLOAT value.
   * The third, fourth, and fifth values are inserted by casting a VARCHAR value to a DECFLOAT value.
2. To show the types, describe the table by using the DESC TABLE command.

   The precision wasn’t specified in the table definition for either column, but the output shows that the DECFLOAT data type supports up to 38 significant digits of precision:

   ```
   DESC TABLE decfloat_sample;
   ```

   Copy

   ```
   +--------------+--------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+----------------+
   | name         | type         | kind   | null? | default | primary key | unique key | check | expression | comment | policy name | privacy domain |
   |--------------+--------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+----------------|
   | ID           | NUMBER(38,0) | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL           |
   | DECFLOAT_VAL | DECFLOAT(38) | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL           |
   | FLOAT_VAL    | FLOAT        | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL           |
   +--------------+--------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+----------------+
   ```
3. To show the differences in the values, query the table by using the SELECT statement:

   ```
   SELECT * FROM decfloat_sample;
   ```

   Copy

   ```
   +----+-----------------------------------------+------------------------+
   | ID | DECFLOAT_VAL                            |              FLOAT_VAL |
   |----+-----------------------------------------+------------------------|
   |  1 | 1.23e7002                               | inf                    |
   |  2 | 12345678901234567890123456789           |   1.23456789012346e+28 |
   |  3 | -4.2e-5432                              |  -0                    |
   |  4 | 1.0000000000000000000000000000000000001 |   1                    |
   |  5 | 1.0000000000000000000000000000000000002 |   1                    |
   +----+-----------------------------------------+------------------------+
   ```

   The output shows the following differences:

   * The first row shows that the DECFLOAT type supports a wider range of values than the FLOAT type.
     The DECFLOAT value is very large (`1.23e7002`). The FLOAT value is `inf`, which means that the
     value is larger than any value that the FLOAT type can represent.
   * The second row shows that the DECFLOAT type retains the specified value exactly. The FLOAT
     value is an approximation that is stored in scientific notation.
   * The third row shows that the DECFLOAT type supports very small values (`-4.2e-5432`). The FLOAT
     value is approximated to `-0`.
   * The fourth and fifth rows show that the DECFLOAT type supports up to 38 digits of precision and uses
     rounding rules for values beyond the limit. The FLOAT value is approximated to `1` in both rows.

##### Use DECFLOAT values with aggregate functions[¶](#use-decfloat-values-with-aggregate-functions "Link to this heading")

The following example uses DECFLOAT values with aggregate functions:

1. Create a table, and then insert DECFLOAT values into the table:

   ```
   CREATE OR REPLACE TABLE decfloat_agg_sample (decfloat_val DECFLOAT);

   INSERT INTO decfloat_agg_sample VALUES
     (DECFLOAT '1e1000'),
     (DECFLOAT '-2.47e999'),
     (DECFLOAT '22e-75');
   ```

   Copy
2. Query the table by using some aggregate functions:

   ```
   SELECT SUM(decfloat_val),
          AVG(decfloat_val),
          MAX(decfloat_val),
          MIN(decfloat_val)
     FROM decfloat_agg_sample;
   ```

   Copy

   ```
   +-------------------+-------------------+-------------------+-------------------+
   | SUM(DECFLOAT_VAL) | AVG(DECFLOAT_VAL) | MAX(DECFLOAT_VAL) | MIN(DECFLOAT_VAL) |
   |-------------------+-------------------+-------------------+-------------------|
   | 7.53e999          | 2.51e999          | 1e1000            | -2.47e999         |
   +-------------------+-------------------+-------------------+-------------------+
   ```

## Numeric constants[¶](#numeric-constants "Link to this heading")

The term *constants* — also known as *literals* — refers to fixed data values. The following formats are
supported for numeric constants:

> `[+-][digits][.digits][e[+-]digits]`

Where:

* `+` or `-` indicates a positive or negative value. The default is positive.
* `digits` is one or more digits from 0 to 9.
* `e` (or `E`) indicates an exponent in scientific notation. At least one digit must follow the exponent marker if present.

The following numbers are all examples of supported numeric constants:

```
15
+1.34
0.2
15e-03
1.234E2
1.234E+2
-1
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

1. [Data types for fixed-point numbers](#data-types-for-fixed-point-numbers)
2. [NUMBER](#number)
3. [DECIMAL , DEC , NUMERIC](#decimal-dec-numeric)
4. [INT , INTEGER , BIGINT , SMALLINT , TINYINT , BYTEINT](#int-integer-bigint-smallint-tinyint-byteint)
5. [Impact of precision and scale on storage size](#impact-of-precision-and-scale-on-storage-size)
6. [Examples of fixed-point data types in a table](#examples-of-fixed-point-data-types-in-a-table)
7. [Data types for floating-point numbers](#data-types-for-floating-point-numbers)
8. [FLOAT , FLOAT4 , FLOAT8](#float-float4-float8)
9. [DOUBLE , DOUBLE PRECISION , REAL](#double-double-precision-real)
10. [Examples of floating-point data types in a table](#examples-of-floating-point-data-types-in-a-table)
11. [DECFLOAT](#decfloat)
12. [Numeric constants](#numeric-constants)

Related content

1. [Arithmetic operators](/sql-reference/operators-arithmetic)
2. [Comparison operators](/sql-reference/operators-comparison)
3. [Logical operators](/sql-reference/operators-logical)
4. [Numeric functions](/sql-reference/functions-numeric)
5. [Conversion functions](/sql-reference/functions-conversion)
6. [Data type conversion](/sql-reference/data-type-conversion)