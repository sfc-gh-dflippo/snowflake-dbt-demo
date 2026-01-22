---
auto_generated: true
description: Snowflake provides support for all standard SELECT, DDL, and DML operations
  across the lifecycle of data in the system, from organizing and storing data to
  querying and working with data, as well as r
last_scraped: '2026-01-14T16:57:49.813646+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/data-lifecycle
title: Overview of the data lifecycle | Snowflake Documentation
---

1. [Overview](getting-started.md)
2. [Get started for users](../getting-started-for-users.md)

   * [Before you begin](setup.md)
   * [Sign in](connecting.md)
   * [Key concepts and architecture](intro-key-concepts.md)
   * [Snowsight tour](ui-snowsight-quick-tour.md)
   * [Data lifecycle](data-lifecycle.md)
3. [Tutorials](../learn-tutorials.md)
4. [Concepts for administrators](../concepts-for-administrators.md)
5. [Sample data](sample-data.md)
6. [Contacting support](contacting-support.md)

[Get started](getting-started.md)[Get started for users](../getting-started-for-users.md)Data lifecycle

# Overview of the data lifecycle[¶](#overview-of-the-data-lifecycle "Link to this heading")

Snowflake provides support for all standard SELECT, DDL, and DML operations across the lifecycle of data in the system, from organizing and
storing data to querying and working with data, as well as removing data from the system.

## Lifecycle diagram[¶](#lifecycle-diagram "Link to this heading")

All user data in Snowflake is logically represented as tables that you can query and modify through standard SQL interfaces. Each table
belongs to a schema which in turn belongs to a database.

![Snowflake Data Lifecycle](../_images/data-lifecycle.png)

## Organize data[¶](#organize-data "Link to this heading")

You can organize your data into databases, schemas, and tables. Snowflake doesn’t limit the number of databases you can create or the
number of schemas you can create within a database. Snowflake also doesn’t limit the number of tables you can create in a schema.

For more information, see the following topics:

* [CREATE DATABASE](../sql-reference/sql/create-database)
* [ALTER DATABASE](../sql-reference/sql/alter-database)
* [CREATE SCHEMA](../sql-reference/sql/create-schema)
* [ALTER SCHEMA](../sql-reference/sql/alter-schema)
* [CREATE TABLE](../sql-reference/sql/create-table)
* [ALTER TABLE](../sql-reference/sql/alter-table)

## Store data[¶](#store-data "Link to this heading")

You can insert data directly into tables. In addition, Snowflake provides DML for loading data into Snowflake tables from external,
formatted files.

For more information, see the following topics:

* [INSERT](../sql-reference/sql/insert)
* [COPY INTO <table>](../sql-reference/sql/copy-into-table)

## Query data[¶](#query-data "Link to this heading")

After data is stored in a table, you can issue SELECT statements to query the data.

For more information, see [SELECT](../sql-reference/sql/select).

## Work with data[¶](#work-with-data "Link to this heading")

After data is stored in a table, you can perform all standard DML operations on the data. In addition, Snowflake supports DDL actions,
such as cloning entire databases, schemas, and tables.

For more information, see the following topics:

* [UPDATE](../sql-reference/sql/update)
* [MERGE](../sql-reference/sql/merge)
* [DELETE](../sql-reference/sql/delete)
* [CREATE <object> … CLONE](../sql-reference/sql/create-clone)

## Remove data[¶](#remove-data "Link to this heading")

In addition to using the DML command, [DELETE](../sql-reference/sql/delete), to remove data from a table, you can truncate or drop an entire
table. You can also drop entire schemas and databases.

For more information, see the following topics:

* [TRUNCATE TABLE](../sql-reference/sql/truncate-table)
* [DROP TABLE](../sql-reference/sql/drop-table)
* [DROP SCHEMA](../sql-reference/sql/drop-schema)
* [DROP DATABASE](../sql-reference/sql/drop-database)

Was this page helpful?

YesNo

[Visit Snowflake](https://www.snowflake.com)

[Join the conversation](https://community.snowflake.com/s/)

[Develop with Snowflake](https://developers.snowflake.com)

[Share your feedback](/feedback)

[Read the latest on our blog](https://www.snowflake.com/blog/)

[Get your own certification](https://learn.snowflake.com)

[Privacy Notice](https://www.snowflake.com/privacy-policy/)[Site Terms](https://www.snowflake.com/legal/snowflake-site-terms/)Cookies Settings© 2026 Snowflake, Inc. All Rights Reserved.

On this page

1. [Lifecycle diagram](#lifecycle-diagram)
2. [Organize data](#organize-data)
3. [Store data](#store-data)
4. [Query data](#query-data)
5. [Work with data](#work-with-data)
6. [Remove data](#remove-data)

Related content

1. [Understanding & using Time Travel](/user-guide/data-time-travel)