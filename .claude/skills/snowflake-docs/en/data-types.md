---
auto_generated: true
description: Snowflake supports most basic SQL data types (with some restrictions)
  for use in columns, local variables, expressions, parameters, and any other appropriate
  locations.
last_scraped: '2026-01-14T16:54:23.467879+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/data-types
title: Snowflake data types | Snowflake Documentation
---

1. [Overview](guides/README.md)
2. [Snowflake Horizon Catalog](user-guide/snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](guides/overview-connecting.md)
6. [Virtual warehouses](user-guide/warehouses.md)
7. [Databases, Tables, & Views](guides/overview-db.md)
8. [Data types](data-types.md)
10. Data Integration

    - [Snowflake Openflow](user-guide/data-integration/openflow/about.md)
    - Apache Iceberg™

      - [Apache Iceberg™ Tables](user-guide/tables-iceberg.md)
      - [Snowflake Open Catalog](user-guide/opencatalog/overview.md)
11. Data engineering

    - [Data loading](guides/overview-loading-data.md)
    - [Dynamic Tables](user-guide/dynamic-tables-about.md)
    - [Streams and Tasks](user-guide/data-pipelines-intro.md)
    - [dbt Projects on Snowflake](user-guide/data-engineering/dbt-projects-on-snowflake.md)
    - [Data Unloading](guides/overview-unloading-data.md)
12. [Storage Lifecycle Policies](user-guide/storage-management/storage-lifecycle-policies.md)
13. [Migrations](migrations/README.md)
15. [Queries](guides/overview-queries.md)
16. [Listings](collaboration/collaboration-listings-about.md)
17. [Collaboration](guides/overview-sharing.md)
19. [Snowflake AI & ML](guides/overview-ai-features.md)
21. [Snowflake Postgres](user-guide/snowflake-postgres/about.md)
23. [Alerts & Notifications](guides/overview-alerts.md)
25. [Security](guides/overview-secure.md)
26. [Data Governance](guides/overview-govern.md)
27. [Privacy](guides/overview-privacy.md)
29. [Organizations & Accounts](guides/overview-manage.md)
30. [Business continuity & data recovery](user-guide/replication-intro.md)
32. [Performance optimization](guides/overview-performance.md)
33. [Cost & Billing](guides/overview-cost.md)

[Guides](guides/README.md)Data types

# Snowflake data types[¶](#snowflake-data-types "Link to this heading")

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
5. [Vector functions](/sql-reference/functions-vector)
6. [Conversion functions](/sql-reference/functions-conversion)
7. [Data type conversion](/sql-reference/data-type-conversion)