---
auto_generated: true
description: 'Snowflake doesn’t support the following data types:'
last_scraped: '2026-01-14T16:56:22.149609+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/data-types-unsupported.html
title: Unsupported data types | Snowflake Documentation
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

[Reference](../reference.md)[SQL data types reference](../sql-reference-data-types.md)Unsupported

# Unsupported data types[¶](#unsupported-data-types "Link to this heading")

Snowflake doesn’t support the following data types:

| Category | Type | Notes |
| --- | --- | --- |
| LOB (Large Object) | BLOB | BINARY can be used instead; maximum of 67108864 bytes. For more information, see [String & binary data types](data-types-text). |
| CLOB | VARCHAR can be used instead; maximum of 134217728 bytes (for singlebyte). For more information, see [String & binary data types](data-types-text). |
| Other | ENUM |  |
| User-defined data types |  |

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