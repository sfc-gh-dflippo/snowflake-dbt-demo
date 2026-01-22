---
auto_generated: true
description: Assigns an expression to a Snowflake Scripting variable, cursor, or RESULTSET.
last_scraped: '2026-01-14T16:56:36.626678+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/snowflake-scripting/let.html
title: LET (Snowflake Scripting) | Snowflake Documentation
---

1. [Overview](../../reference.md)
2. [SQL data types reference](../../sql-reference-data-types.md)
3. [SQL command reference](../../sql-reference-commands.md)
4. [Function and stored procedure reference](../../sql-reference-functions.md)
5. [Class reference](../../sql-reference-classes.md)
6. [Scripting reference](../../sql-reference-snowflake-scripting.md)

   * [AWAIT](await.md)
   * [BEGIN ... END](begin.md)
   * [BREAK](break.md)
   * [CANCEL](cancel.md)
   * [CASE](case.md)
   * [CLOSE](close.md)
   * [CONTINUE](continue.md)
   * [DECLARE](declare.md)
   * [EXCEPTION](exception.md)
   * [FETCH](fetch.md)
   * [FOR](for.md)
   * [IF](if.md)
   * [LET](let.md)
   * [LOOP](loop.md)
   * [NULL](null.md)
   * [OPEN](open.md)
   * [RAISE](raise.md)
   * [REPEAT](repeat.md)
   * [RETURN](return.md)
   * [WHILE](while.md)
7. [General reference](../../sql-reference.md)
8. [API reference](../../api-reference.md)

[Reference](../../reference.md)[Scripting reference](../../sql-reference-snowflake-scripting.md)LET

# LET (Snowflake Scripting)[¶](#let-snowflake-scripting "Link to this heading")

Assigns an expression to a Snowflake Scripting variable, cursor, or RESULTSET.

For more information on variables, cursors, and RESULTSETs, see:

* [Working with variables](../../developer-guide/snowflake-scripting/variables)
* [Working with cursors](../../developer-guide/snowflake-scripting/cursors)
* [Working with RESULTSETs](../../developer-guide/snowflake-scripting/resultsets)

Note

This [Snowflake Scripting](../../developer-guide/snowflake-scripting/index) construct is valid only within a
[Snowflake Scripting block](../../developer-guide/snowflake-scripting/blocks).

See also:
:   [DECLARE](declare)

## Syntax[¶](#syntax "Link to this heading")

```
LET { <variable_assignment> | <cursor_assignment> | <resultset_assignment> }
```

Copy

The syntax for each type of assignment is described below in more detail.

* [Variable assignment syntax](#label-snowscript-let-syntax-variable)
* [Cursor assignment syntax](#label-snowscript-let-syntax-cursor)
* [RESULTSET assignment syntax](#label-snowscript-let-syntax-resultset)

### Variable assignment syntax[¶](#variable-assignment-syntax "Link to this heading")

Use the following syntax to assign an expression to a [variable](../../developer-guide/snowflake-scripting/variables).

```
LET <variable_name> <type> { DEFAULT | := } <expression> ;

LET <variable_name> { DEFAULT | := } <expression> ;
```

Copy

Where:

> `variable_name`
> :   The name of the variable. The name must follow the naming rules for [object identifiers](../identifiers).
>
> `type`
> :   A [SQL data type](../../sql-reference-data-types).
>
> `DEFAULT expression` or . `:= expression`
> :   Assigns the value of `expression` to the variable.
>
>     If both `type` and `expression` are specified, the expression must evaluate to a data type that matches.

For example, the following `LET` statements declare three variables of type [NUMBER](../data-types-numeric.html#label-data-type-number),
with precision set to `38` and scale set to `2`. All three variables have a default value, using either `DEFAULT`
or `:=` to specify it.

```
BEGIN
  ...
  LET profit NUMBER(38, 2) DEFAULT 0.0;
  LET revenue NUMBER(38, 2) DEFAULT 110.0;
  LET cost NUMBER(38, 2) := 100.0;
  ...
```

Copy

For more examples, see:

* [Working with variables](../../developer-guide/snowflake-scripting/variables)
* [IF statements](../../developer-guide/snowflake-scripting/branch.html#label-snowscript-branch-if)
* [Working with loops](../../developer-guide/snowflake-scripting/loops)
* [Examples for common use cases of Snowflake Scripting](../../developer-guide/snowflake-scripting/use-cases)

### Cursor assignment syntax[¶](#cursor-assignment-syntax "Link to this heading")

Use one of the following syntaxes to assign an expression to a [cursor](../../developer-guide/snowflake-scripting/cursors).

```
LET <cursor_name> CURSOR FOR <query> ;
```

Copy

```
LET <cursor_name> CURSOR FOR <resultset_name> ;
```

Copy

Where:

> `cursor_name`
> :   The name to give the cursor. This can be any valid Snowflake [identifier](../identifiers)
>     that is not already in use in this block. The identifier is used by other cursor-related commands, such as [FETCH (Snowflake Scripting)](fetch).
>
> `query`
> :   The query that defines the result set that the cursor iterates over.
>
>     This can be almost any valid SELECT statement.
>
> `resultset_name`
> :   The name of the [RESULTSET](../../developer-guide/snowflake-scripting/resultsets) for the cursor to operate on.

For example, the following `LET` statement declares cursor `c1` for a query:

```
BEGIN
  ...
  LET c1 CURSOR FOR SELECT price FROM invoices;
  ...
```

Copy

For more examples, see [Working with cursors](../../developer-guide/snowflake-scripting/cursors).

### RESULTSET assignment syntax[¶](#resultset-assignment-syntax "Link to this heading")

Use the following syntax to assign an expression to a [RESULTSET](../../developer-guide/snowflake-scripting/resultsets).

```
<resultset_name> := ( <query> ) ;
```

Copy

Where:

> `resultset_name`
> :   The name to give the RESULTSET.
>
>     The name should be unique within the current scope.
>
>     The name must follow the naming rules for [Object identifiers](../identifiers).
>
> `DEFAULT query` or . `:= query`
> :   Assigns the value of `query` to the RESULTSET.

For example, the following `LET` statement declares RESULTSET `res` for a query:

```
BEGIN
  ...
  LET res RESULTSET := (SELECT price FROM invoices);
  ...
```

Copy

For more examples, see [Working with RESULTSETs](../../developer-guide/snowflake-scripting/resultsets).

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

1. [Syntax](#syntax)