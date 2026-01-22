---
auto_generated: true
description: 'Snowflake supports most SQL data types. The following table provides
  a summary of the supported data types:'
last_scraped: '2026-01-14T16:56:47.967261+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/intro-summary-data-types
title: Summary of data types | Snowflake Documentation
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

[Reference](../reference.md)[SQL data types reference](../sql-reference-data-types.md)Summary

# Summary of data types[¶](#summary-of-data-types "Link to this heading")

Snowflake supports most SQL data types. The following table provides a summary of the supported data types:

| Category | Type | Notes |
| --- | --- | --- |
| [Numeric data types](data-types-numeric) | NUMBER | Default precision and scale are (38,0). |
|  | DECIMAL, NUMERIC | Synonymous with NUMBER. |
|  | INT, INTEGER, BIGINT, SMALLINT, TINYINT, BYTEINT | Synonymous with NUMBER, except precision and scale can’t be specified. |
|  | FLOAT, FLOAT4, FLOAT8 | [1] |
|  | DOUBLE, DOUBLE PRECISION, REAL | Synonymous with FLOAT. [1] |
|  | DECFLOAT | Stores numbers exactly, with up to 38 significant digits of precision, and uses a dynamic base-10 exponent. |
| [String & binary data types](data-types-text) | VARCHAR | Default length is 16777216 bytes. Maximum length is 134217728 bytes. |
|  | CHAR, CHARACTER | Synonymous with VARCHAR, except the default length is VARCHAR(1). |
|  | STRING, TEXT | Synonymous with VARCHAR. |
|  | BINARY |  |
|  | VARBINARY | Synonymous with BINARY. |
| [Logical data types](data-types-logical) | BOOLEAN | Currently only supported for accounts provisioned after January 25, 2016. |
| [Date & time data types](data-types-datetime) | DATE |  |
|  | DATETIME | Synonymous with TIMESTAMP\_NTZ. |
|  | TIME |  |
|  | TIMESTAMP | Alias for one of the TIMESTAMP variations (TIMESTAMP\_NTZ by default). |
|  | TIMESTAMP\_LTZ | TIMESTAMP with local time zone; time zone, if provided, isn’t stored. |
|  | TIMESTAMP\_NTZ | TIMESTAMP with no time zone; time zone, if provided, isn’t stored. |
|  | TIMESTAMP\_TZ | TIMESTAMP with time zone. |
| [Semi-structured data types](data-types-semistructured) | VARIANT |  |
|  | OBJECT |  |
|  | ARRAY |  |
| [Structured data types](data-types-structured) | ARRAY |  |
|  | OBJECT |  |
|  | MAP |  |
| [Unstructured data types](data-types-unstructured) | FILE | See [Introduction to unstructured data](../user-guide/unstructured-intro). |
| [Geospatial data types](data-types-geospatial) | GEOGRAPHY |  |
|  | GEOMETRY |  |
| [Vector data types](data-types-vector) | VECTOR |  |

[1] A known issue in Snowflake displays FLOAT, FLOAT4, FLOAT8, REAL, DOUBLE, and DOUBLE PRECISION as FLOAT, even though they are stored as DOUBLE.

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