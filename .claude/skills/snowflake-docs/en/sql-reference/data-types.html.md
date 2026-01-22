---
auto_generated: true
description: Snowflake supports most basic SQL data types (with some restrictions)
  for use in columns, local variables, expressions, parameters, and any other appropriate
  locations.
last_scraped: '2026-01-14T16:55:37.187266+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/data-types.html
title: SQL data types reference | Snowflake Documentation
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

[Reference](../reference.md)SQL data types reference

# SQL data types reference[¶](#sql-data-types-reference "Link to this heading")

Snowflake supports most basic SQL data types (with some restrictions) for use in columns, local variables, expressions, parameters,
and any other appropriate locations.

Note

You can also load unstructured data into Snowflake. For more information, see [Introduction to unstructured data](user-guide/unstructured-intro).

In some cases, data of one type can be converted to another type. For example, INTEGER data can be converted to FLOAT data.

Some conversions are lossless, but others might lose information. The amount of loss depends upon the data types and the specific
values. For example, converting a FLOAT value to an INTEGER value removes the digits after the decimal place. (The value is
rounded to the nearest integer.)

In some cases, the user must specify the desired conversion, such as when passing a VARCHAR value to the
[TIME\_SLICE](sql-reference/functions/time_slice) function, which expects a TIMESTAMP or DATE argument. We
call this explicit casting.

In other cases, data types are converted automatically, such as when adding a float and an integer. We call this
implicit casting (or coercion). In Snowflake, data types are automatically coerced whenever necessary
and possible.

For more information about explicit and implicit casting, see [Data type conversion](sql-reference/data-type-conversion).

For more information about Snowflake data types, see the following topics:

* [Summary of data types](sql-reference/intro-summary-data-types)
* [Numeric data types](sql-reference/data-types-numeric)
* [String & binary data types](sql-reference/data-types-text)
* [Logical data types](sql-reference/data-types-logical)
* [Date & time data types](sql-reference/data-types-datetime)
* [Semi-structured data types](sql-reference/data-types-semistructured)
* [Structured data types](sql-reference/data-types-structured)
* [Unstructured data types](sql-reference/data-types-unstructured)
* [Geospatial data types](sql-reference/data-types-geospatial)
* [Vector data types](sql-reference/data-types-vector)
* [Unsupported data types](sql-reference/data-types-unsupported)
* [Data type conversion](sql-reference/data-type-conversion)

Was this page helpful?

YesNo

[Visit Snowflake](https://www.snowflake.com)

[Join the conversation](https://community.snowflake.com/s/)

[Develop with Snowflake](https://developers.snowflake.com)

[Share your feedback](/feedback)

[Read the latest on our blog](https://www.snowflake.com/blog/)

[Get your own certification](https://learn.snowflake.com)

[Privacy Notice](https://www.snowflake.com/privacy-policy/)[Site Terms](https://www.snowflake.com/legal/snowflake-site-terms/)Cookies Settings© 2026 Snowflake, Inc. All Rights Reserved.

Related content

1. [String & binary functions](/sql-reference/functions-string)
2. [Date & time functions](/sql-reference/functions-date-time)
3. [Semi-structured and structured data functions](/sql-reference/functions-semistructured)
4. [Geospatial functions](/sql-reference/functions-geospatial)
5. [Conversion functions](/sql-reference/functions-conversion)
6. [Data type conversion](/sql-reference/data-type-conversion)
7. [Unstructured Data](/user-guide/unstructured-intro)