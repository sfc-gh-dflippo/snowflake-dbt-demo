---
auto_generated: true
description: Snowflake SQL reserves all ANSI keywords (with the exception of type
  keywords such as CHAR, DATE, DECIMAL, etc.), as well as some additional keywords
  (ASC, DESC, MINUS, etc.) that are reserved by othe
last_scraped: '2026-01-14T16:55:24.795645+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/reserved-keywords
title: Reserved & limited keywords | Snowflake Documentation
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

[Reference](../reference.md)[General reference](../sql-reference.md)Reserved keywords

# Reserved & limited keywords[¶](#reserved-limited-keywords "Link to this heading")

Snowflake SQL reserves all ANSI keywords (with the exception of type keywords such as CHAR, DATE, DECIMAL, etc.), as well as some additional keywords (ASC, DESC, MINUS, etc.) that are reserved by
other popular databases. Additionally, Snowflake reserves keywords REGEXP and RLIKE (which function like the ANSI reserved keyword LIKE) and SOME (which is a synonym for the ANSI reserved keyword ANY).

To avoid parsing ambiguities, Snowflake SQL also prohibits the use of keywords such as LEFT, OUTER, JOIN, etc. as table names or aliases in the FROM list, and the use of keywords such as TRUE, FALSE, CASE,
etc. as column references in scalar expressions.

The following table provides the list of reserved keywords in Snowflake and keywords that are not strictly reserved, but have usage limitations:

| Keyword | Comment |
| --- | --- |
| **A** |  |
| ACCOUNT | Cannot be used as an identifier in a SHOW command (e.g. ‘SHOW … IN <identifier>’). |
| ALL | Reserved by ANSI. |
| ALTER | Reserved by ANSI. |
| AND | Reserved by ANSI. |
| ANY | Reserved by ANSI. |
| AS | Reserved by ANSI. |
| **B** |  |
| BETWEEN | Reserved by ANSI. |
| BY | Reserved by ANSI. |
| **C** |  |
| CASE | Cannot be used as column reference in a scalar expression. |
| CAST | Cannot be used as column reference in a scalar expression. |
| CHECK | Reserved by ANSI. |
| COLUMN | Reserved by ANSI. |
| CONNECT | Reserved by ANSI. |
| CONNECTION | Cannot be used as an identifier in a SHOW command (e.g. ‘SHOW … IN <identifier>’). |
| CONSTRAINT | Cannot be used as a column name in CREATE TABLE DDL. |
| CREATE | Reserved by ANSI. |
| CROSS | Cannot be used as table name or alias in a FROM clause. |
| CURRENT | Reserved by ANSI. |
| CURRENT\_DATE | Cannot be used as column name (reserved by ANSI). |
| CURRENT\_TIME | Cannot be used as column name (reserved by ANSI). |
| CURRENT\_TIMESTAMP | Cannot be used as column name (reserved by ANSI). |
| CURRENT\_USER | Cannot be used as column name (reserved by ANSI). |
| **D** |  |
| DATABASE | Cannot be used as an identifier in a SHOW command (e.g. ‘SHOW … IN <identifier>’). |
| DELETE | Reserved by ANSI. |
| DISTINCT | Reserved by ANSI. |
| DROP | Reserved by ANSI. |
| **E** |  |
| ELSE | Reserved by ANSI. |
| EXISTS | Reserved by ANSI. |
| **F** |  |
| FALSE | Cannot be used as column reference in a scalar expression. |
| FOLLOWING | Reserved by ANSI. |
| FOR | Reserved by ANSI. |
| FROM | Reserved by ANSI. |
| FULL | Cannot be used as table name or alias in a FROM clause. |
| **G** |  |
| GRANT | Reserved by ANSI. |
| GROUP | Reserved by ANSI. |
| GSCLUSTER | Cannot be used as an identifier in a SHOW command (e.g. ‘SHOW … IN <identifier>’). |
| **H** |  |
| HAVING | Reserved by ANSI. |
| **I** |  |
| ILIKE | Reserved by Snowflake. |
| IN | Reserved by ANSI. |
| INCREMENT | Reserved by Snowflake and others. |
| INNER | Cannot be used as table name or alias in a FROM clause. |
| INSERT | Reserved by ANSI. |
| INTERSECT | Reserved by ANSI. |
| INTO | Reserved by ANSI. |
| IS | Reserved by ANSI. |
| ISSUE | Cannot be used as an identifier in a SHOW command (e.g. ‘SHOW … IN <identifier>’). |
| **J** |  |
| JOIN | Cannot be used as table name or alias in a FROM clause. |
| **L** |  |
| LATERAL | Cannot be used as table name or alias in a FROM clause. |
| LEFT | Cannot be used as table name or alias in a FROM clause. |
| LIKE | Reserved by ANSI. |
| LOCALTIME | Cannot be used as column name (reserved by ANSI). |
| LOCALTIMESTAMP | Cannot be used as column name (reserved by ANSI). |
| **M** |  |
| MINUS | Reserved by Snowflake and others. |
| **N** |  |
| NATURAL | Cannot be used as table name or alias in a FROM clause. |
| NOT | Reserved by ANSI. |
| NULL | Reserved by ANSI. |
| **O** |  |
| OF | Reserved by ANSI. |
| ON | Reserved by ANSI. |
| OR | Reserved by ANSI. |
| ORDER | Reserved by ANSI. |
| ORGANIZATION | Cannot be used as an identifier in a SHOW command (e.g. ‘SHOW … IN <identifier>’). |
| **Q** |  |
| QUALIFY | Reserved by Snowflake. |
| **R** |  |
| REGEXP | Reserved by Snowflake. |
| REVOKE | Reserved by ANSI. |
| RIGHT | Cannot be used as table name or alias in a FROM clause. |
| RLIKE | Reserved by Snowflake. |
| ROW | Reserved by ANSI. |
| ROWS | Reserved by ANSI. |
| **S** |  |
| SAMPLE | Reserved by ANSI. |
| SCHEMA | Cannot be used as an identifier in a SHOW command (e.g. ‘SHOW … IN <identifier>’). |
| SELECT | Reserved by ANSI. |
| SET | Reserved by ANSI. |
| SOME | Reserved by Snowflake. |
| START | Reserved by ANSI. |
| **T** |  |
| TABLE | Reserved by ANSI. |
| TABLESAMPLE | Reserved by ANSI. |
| THEN | Reserved by ANSI. |
| TO | Reserved by ANSI. |
| TRIGGER | Reserved by ANSI. |
| TRUE | Cannot be used as column reference in a scalar expression. |
| TRY\_CAST | Cannot be used as column reference in a scalar expression. |
| **U** |  |
| UNION | Reserved by ANSI. |
| UNIQUE | Reserved by ANSI. |
| UPDATE | Reserved by ANSI. |
| USING | Cannot be used as table name or alias in a FROM clause. |
| **V** |  |
| VALUES | Reserved by ANSI. |
| VIEW | Cannot be used as an identifier in a SHOW command (e.g. ‘SHOW … IN <identifier>’). |
| **W** |  |
| WHEN | Cannot be used as column reference in a scalar expression. |
| WHENEVER | Reserved by ANSI. |
| WHERE | Reserved by ANSI. |
| WINDOW | Reserved by ANSI. |
| WITH | Reserved by ANSI. |

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