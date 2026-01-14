---
description: Note
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/redshift/redshift-system-catalog
title: SnowConvert AI - Redshift - System catalog tables | Snowflake Documentation
---

## Description [¶](#description)

> The system catalogs store schema metadata, such as information about tables and columns. System
> catalog tables have a PG prefix.
>
> The standard PostgreSQL catalog tables are accessible to Amazon Redshift users.
> ([Redshift SQL Language reference System catalog tables](https://docs.aws.amazon.com/redshift/latest/dg/c_intro_catalog_views.html)).

The following table outlines how SnowConvert AI transforms references to SQL functions defined in
the `pg_catalog` in Redshift.

## Mapping of SQL functions from the `pg_catalog`[¶](#mapping-of-sql-functions-from-the-pg-catalog)

<!-- prettier-ignore -->
|Redshift|Snowflake|
|---|---|
|pg_catalog.row_number()|[row_number()](https://docs.snowflake.com/en/sql-reference/functions/row_number)|
|pg_catalog.replace()|[replace()](https://docs.snowflake.com/en/sql-reference/functions/replace)|
|pg_catalog.lead()|[lead()](https://docs.snowflake.com/en/sql-reference/functions/lead)|
