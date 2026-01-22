---
auto_generated: true
description: Constraints define integrity and consistency rules for data stored in
  tables. Snowflake provides support for constraints as defined in the ANSI SQL standard,
  as well as some extensions for compatibili
last_scraped: '2026-01-14T16:57:34.250902+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/constraints
title: Constraints | Snowflake Documentation
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

     + [Overview](constraints-overview.md)
     + [Creating](constraints-create.md)
     + [Modifying](constraints-alter.md)
     + [Dropping](constraints-drop.md)
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

[Reference](../reference.md)[General reference](../sql-reference.md)Constraints

# Constraints[¶](#constraints "Link to this heading")

Constraints define integrity and consistency rules for data stored in tables.
Snowflake provides support for constraints as defined in the ANSI SQL standard,
as well as some extensions for compatibility with other databases, such as Oracle.

Important

* For standard tables, Snowflake supports defining and maintaining constraints, but
  does not enforce them, except for NOT NULL constraints, which are always enforced.

  Violations of constraints may cause unexpected downstream effects. If you decide to create a
  constraint that must be relied upon, make sure your downstream processes can maintain data
  integrity. For more information, see [Constraint properties](sql/create-table-constraint.html#label-extended-constraint-properties).

  Constraints on standard tables are provided primarily for data modeling purposes and compatibility
  with other databases, as well as to support client tools that utilize constraints. For example,
  Tableau supports using constraints to perform join culling (join elimination), which can improve the
  performance of generated queries and cube refresh.
* For [hybrid tables](../user-guide/tables-hybrid), Snowflake both supports and enforces
  constraints. Primary key constraints are required and enforced on all hybrid tables, and other
  constraints are enforced when used.

**Next Topics:**

* [Overview of Constraints](constraints-overview)
* [Creating Constraints](constraints-create)
* [Modifying Constraints](constraints-alter)
* [Dropping Constraints](constraints-drop)

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