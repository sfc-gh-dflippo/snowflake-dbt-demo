---
auto_generated: true
description: Uses the specified cursor to fetch one or more rows.
last_scraped: '2026-01-14T16:55:35.059632+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/snowflake-scripting/fetch
title: FETCH (Snowflake Scripting) | Snowflake Documentation
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

[Reference](../../reference.md)[Scripting reference](../../sql-reference-snowflake-scripting.md)FETCH

# FETCH (Snowflake Scripting)[¶](#fetch-snowflake-scripting "Link to this heading")

Uses the specified cursor to fetch one or more rows.

For more information on cursors, see [Working with cursors](../../developer-guide/snowflake-scripting/cursors).

Note

This [Snowflake Scripting](../../developer-guide/snowflake-scripting/index) construct is valid only within a
[Snowflake Scripting block](../../developer-guide/snowflake-scripting/blocks).

See also:
:   [DECLARE](declare), [OPEN](open), [CLOSE](close)

## Syntax[¶](#syntax "Link to this heading")

```
FETCH <cursor_name> INTO <variable> [, <variable> ... ] ;
```

Copy

Where:

> `cursor_name`
> :   The name of the cursor.
>
> `variable`
> :   The name of the variable into which to retrieve the value of one column of the current row.
>
>     You should have one variable for each column defined in the cursor declaration.
>
>     The variable must already have been [declared](../../developer-guide/snowflake-scripting/variables.html#label-snowscript-declare-variable).
>
>     The variable’s data type must be compatible with the value to be fetched.

## Usage notes[¶](#usage-notes "Link to this heading")

* The number of `variable`s should match the number of expressions selected in the `SELECT` clause of
  the cursor declaration.
* If you try to `FETCH` a row after the last row, you get NULL values.
* A RESULTSET or CURSOR does not necessarily cache all the rows of the result set at the time that the query is executed.
  FETCH operations can experience latency.

## Examples[¶](#examples "Link to this heading")

```
FETCH my_cursor_name INTO my_variable_name ;
```

Copy

For a more complete example of using a cursor, see
[the introductory cursor example](../../developer-guide/snowflake-scripting/cursors.html#label-snowscript-cursors-example).

An example using a loop is included in the documentation for [FOR loops](../../developer-guide/snowflake-scripting/loops.html#label-snowscript-loop-for).

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
2. [Usage notes](#usage-notes)
3. [Examples](#examples)