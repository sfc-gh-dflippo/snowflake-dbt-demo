---
auto_generated: true
description: 'Unquoted object identifiers:'
last_scraped: '2026-01-14T16:56:18.491276+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/identifiers-syntax
title: Identifier requirements | Snowflake Documentation
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

     + [Requirements](identifiers-syntax.md)
     + [Literals and variables as identifiers](identifier-literal.md)
     + [Object name resolution](name-resolution.md)
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

[Reference](../reference.md)[General reference](../sql-reference.md)[Object identifiers](identifiers.md)Requirements

# Identifier requirements[¶](#identifier-requirements "Link to this heading")

[Unquoted object identifiers](#label-unquoted-identifier):

* Start with a letter (A-Z, a-z) or an underscore (“\_”).
* Contain only letters, underscores, decimal digits (0-9), and dollar signs (“$”).
* Are stored and resolved as uppercase characters (e.g. `id` is stored and resolved as `ID`).

If you put [double quotes around an identifier](#label-delimited-identifier) (e.g.
“My identifier with blanks and punctuation.”), the following rules apply:

* The case of the identifier is preserved when storing and resolving the identifier (e.g. `"id"` is stored and resolved as
  `id`).
* The identifier can contain and start with ASCII, extended ASCII, and non-ASCII characters.

  To use the double quote character inside a quoted identifier, use two quotes. For example:

  ```
  CREATE TABLE "quote""andunquote""" ...
  ```

  Copy

  creates a table named:

  ```
  quote"andunquote"
  ```

  Copy

  where the quotation marks are part of the name.

Note

* Regardless of whether an identifier is unquoted or double-quoted, the maximum number of characters allowed is 255 (including blank spaces).
* Identifiers can also be specified using string literals, session variables or bind variables. For details, see [SQL variables](session-variables).

## Unquoted identifiers[¶](#unquoted-identifiers "Link to this heading")

If an identifier is not enclosed in double quotes, it must begin with a letter or underscore (`_`) and cannot contain extended characters or blank
spaces.

The following are all examples of valid identifiers; however, the case of the characters in these identifiers would not be preserved:

```
myidentifier
MyIdentifier1
My$identifier
_my_identifier
```

Copy

Unquoted identifiers are stored and [resolved](#label-identifier-casing) in uppercase. Therefore, an unquoted identifier is equivalent to a capitalized double-quoted
identifier with the same name. For example, the following two statements attempt to create the same table:

```
CREATE TABLE mytable(c1 INT, c2 INT);
```

Copy

```
+-------------------------------------+
| status                              |
|-------------------------------------|
| Table MYTABLE successfully created. |
+-------------------------------------+
```

```
CREATE TABLE "MYTABLE"(c1 INT, c2 INT);
```

Copy

```
002002 (42710): SQL compilation error:
Object 'MYTABLE' already exists.
```

## Double-quoted identifiers[¶](#double-quoted-identifiers "Link to this heading")

Delimited identifiers (i.e. identifiers enclosed in double quotes) are case-sensitive and can start with and contain any valid characters,
including:

* Numbers
* Special characters (`.`, `'`, `!`, `@`, `#`, `$`, `%`, `^`, `&`, `*`, etc.)
* Extended ASCII and non-ASCII characters
* Blank spaces

For example:

```
"MyIdentifier"
"my.identifier"
"my identifier"
"My 'Identifier'"
"3rd_identifier"
"$Identifier"
"идентификатор"
```

Copy

Important

If an object is created using a double-quoted identifier, when referenced in a query or any other SQL statement, the identifier must be specified
exactly as created, including the double quotes. Failure to include the quotes might result in an `Object does not exist` error (or
similar type of error).

Also, note that the entire identifier must be enclosed in quotes when referenced in a query/SQL statement. This is particularly important if periods
(`.`) are used in identifiers because periods are also used in fully-qualified object names to separate each object.

For example:

```
"My.DB"."My.Schema"."Table.1"
```

Copy

### Exceptions[¶](#exceptions "Link to this heading")

* Double-quoted identifiers are not supported for the
  [names of user-defined functions (UDFs) and procedures](../developer-guide/udf-stored-procedure-naming-conventions) in which the
  handler language is Java, JavaScript, Snowflake Scripting, or SQL.
* You can use only ASCII characters for the names of user-defined functions (UDFs) and procedures in which the handler language is Java.

## Identifier resolution[¶](#label-identifier-casing "Link to this heading")

By default, Snowflake applies the following rules for storing identifiers (at creation/definition time) and resolving them (in queries and other SQL
statements):

* When an identifier is unquoted, it is stored and resolved in uppercase.
* When an identifier is double-quoted, it is stored and resolved exactly as entered, including case.

For example, the following four names are equivalent and all resolve to `TABLENAME`:

```
TABLENAME
tablename
tableName
TableName
```

Copy

In contrast, the following four names are considered to be different, unique values:

```
"TABLENAME"
"tablename"
"tableName"
"TableName"
```

Copy

If these identifiers were used to create objects of the same type (e.g. tables), they would result in the creation of four distinct objects.

## Migrating from databases that treat double-quoted identifiers as case-insensitive[¶](#migrating-from-databases-that-treat-double-quoted-identifiers-as-case-insensitive "Link to this heading")

In the ANSI/ISO standard for SQL, identifiers in double quotes (delimited identifiers) are treated as case-sensitive. However,
some companies provide databases that treat double-quoted identifiers as case-insensitive.

If you are migrating your data and applications from one of these databases to Snowflake, those applications might use double
quotes around identifiers that are intended to be case-insensitive. This can prevent Snowflake from resolving the identifiers
correctly. For example, an application might use double quotes around an identifier in lowercase, and the Snowflake database
has the identifier in uppercase.

To work around this limitation, Snowflake provides the [QUOTED\_IDENTIFIERS\_IGNORE\_CASE](parameters.html#label-quoted-identifiers-ignore-case) session parameter, which
causes Snowflake to treat lowercase letters in double-quoted identifiers as uppercase when creating and finding objects.

See the next sections for details:

* [Controlling case using the QUOTED\_IDENTIFIERS\_IGNORE\_CASE parameter](#label-identifier-casing-parameter-howto)
* [Impact of changing the parameter](#label-changing-quoted-identifiers-ignore-case)

Note

Changing the value of the parameter can affect your ability to find existing objects. See
[Impact of changing the parameter](#label-changing-quoted-identifiers-ignore-case) for details.

### Controlling case using the QUOTED\_IDENTIFIERS\_IGNORE\_CASE parameter[¶](#controlling-case-using-the-quoted-identifiers-ignore-case-parameter "Link to this heading")

To configure Snowflake to treat alphabetic characters in double-quoted identifiers as uppercase for the session, set the
parameter to TRUE for the session. With this setting, all alphabetical characters in identifiers are stored and resolved as
uppercase characters.

In other words, the following eight names are equivalent and all resolve to `TABLENAME`:

```
TABLENAME
tablename
tableName
TableName
"TABLENAME"
"tablename"
"tableName"
"TableName"
```

Copy

Note that the parameter has no effect on any of the limitations for unquoted identifiers with regards to numbers, extended
characters, and blank spaces.

### Impact of changing the parameter[¶](#impact-of-changing-the-parameter "Link to this heading")

Changing the [QUOTED\_IDENTIFIERS\_IGNORE\_CASE](parameters.html#label-quoted-identifiers-ignore-case) session parameter only affects new objects and queries:

* With the default setting of FALSE, if an object is created using a double-quoted identifier with mixed case, Snowflake stores
  the identifier in mixed case.
* If the parameter is later changed to TRUE, Snowflake will not be able to resolve that double-quoted mixed case identifier and
  will not be able retrieve that object.

Tip

Due to the impact that changing the parameter can have on resolving identifiers, we highly recommend choosing the
identifier resolution method early in your implementation of Snowflake. Then, have your account administrator set the parameter
at the account level to enforce this resolution method by default.

Although you can override this parameter at the session level, we don’t encourage changing the parameter from the default,
unless you have an explicit need to do so.

The following examples illustrate the behavior after changing the parameter from FALSE to TRUE:

```
-- Set the default behavior
ALTER SESSION SET QUOTED_IDENTIFIERS_IGNORE_CASE = false;

-- Create a table with a double-quoted identifier
CREATE TABLE "One" (i int);  -- stored as "One"

-- Create a table with an unquoted identifier
CREATE TABLE TWO(j int);     -- stored as "TWO"

-- These queries work
SELECT * FROM "One";         -- searches for "One"
SELECT * FROM two;           -- searched for "TWO"
SELECT * FROM "TWO";         -- searches for "TWO"

-- These queries do not work
SELECT * FROM One;           -- searches for "ONE"
SELECT * FROM "Two";         -- searches for "Two"

-- Change to the all-uppercase behavior
ALTER SESSION SET QUOTED_IDENTIFIERS_IGNORE_CASE = true;

-- Create another table with a double-quoted identifier
CREATE TABLE "Three"(k int); -- stored as "THREE"

-- These queries work
SELECT * FROM "Two";         -- searches for "TWO"
SELECT * FROM two;           -- searched for "TWO"
SELECT * FROM "TWO";         -- searches for "TWO"
SELECT * FROM "Three";       -- searches for "THREE"
SELECT * FROM three;         -- searches for "THREE"

-- This query does not work now - "One" is not retrievable
SELECT * FROM "One";         -- searches for "ONE"
```

Copy

Additionally, if the identifiers for two tables differ only by case, one identifier might resolve to a different table after changing the parameter:

```
-- Set the default behavior
ALTER SESSION SET QUOTED_IDENTIFIERS_IGNORE_CASE = false;

-- Create a table with a double-quoted identifier
CREATE TABLE "Tab" (i int);  -- stored as "Tab"

-- Create a table with an unquoted identifier
CREATE TABLE TAB(j int);     -- stored as "TAB"

-- This query retrieves "Tab"
SELECT * FROM "Tab";         -- searches for "Tab"

-- Change to the all-uppercase behavior
ALTER SESSION SET QUOTED_IDENTIFIERS_IGNORE_CASE = true;

-- This query retrieves "TAB"
SELECT * FROM "Tab";         -- searches for "TAB"
```

Copy

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

1. [Unquoted identifiers](#unquoted-identifiers)
2. [Double-quoted identifiers](#double-quoted-identifiers)
3. [Identifier resolution](#label-identifier-casing)
4. [Migrating from databases that treat double-quoted identifiers as case-insensitive](#migrating-from-databases-that-treat-double-quoted-identifiers-as-case-insensitive)