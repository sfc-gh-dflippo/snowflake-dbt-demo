---
auto_generated: true
description: BEGIN and END define a Snowflake Scripting block.
last_scraped: '2026-01-14T16:56:35.251588+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/snowflake-scripting/begin
title: BEGIN … END (Snowflake Scripting) | Snowflake Documentation
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

[Reference](../../reference.md)[Scripting reference](../../sql-reference-snowflake-scripting.md)BEGIN ... END

# BEGIN … END (Snowflake Scripting)[¶](#begin-end-snowflake-scripting "Link to this heading")

`BEGIN` and `END` define a Snowflake Scripting block.

For more information on blocks, see [Understanding blocks in Snowflake Scripting](../../developer-guide/snowflake-scripting/blocks).

## Syntax[¶](#syntax "Link to this heading")

```
BEGIN
    <statement>;
    [ <statement>; ... ]
[ EXCEPTION <exception_handler> ]
END;
```

Copy

Where:

> `statement`
> :   A statement can be any of the following:
>
>     * A single SQL statement (including CALL).
>     * A control-flow statement (for example, a [looping](../../developer-guide/snowflake-scripting/loops) or
>       [branching](../../developer-guide/snowflake-scripting/branch) statement).
>     * A nested [block](../../developer-guide/snowflake-scripting/blocks).
>
> `exception_handler`
> :   Specifies how exceptions should be handled. Refer to [Handling exceptions](../../developer-guide/snowflake-scripting/exceptions) and
>     [EXCEPTION (Snowflake Scripting)](exception).

## Usage notes[¶](#usage-notes "Link to this heading")

* The keyword `END` must be followed immediately by a semicolon, or followed immediately by a label that is
  immediately followed by a semicolon.
* The keyword `BEGIN` must not be followed immediately by a semicolon.
* `BEGIN` and `END` are usually used inside another language construct, such as a looping or branching construct,
  or inside a stored procedure. However, this is not required. A BEGIN/END block can be the top-level construct inside
  an anonymous block.
* Blocks can be nested.

## Examples[¶](#examples "Link to this heading")

This is a simple example of using `BEGIN` and `END` to group related statements. This example creates two
related tables.

```
EXECUTE IMMEDIATE $$
BEGIN
    CREATE TABLE parent (ID INTEGER);
    CREATE TABLE child (ID INTEGER, parent_ID INTEGER);
    RETURN 'Completed';
END;
$$
;
```

Copy

The next example is similar; the statements are grouped into a block and are also inside a transaction within
that block:

```
EXECUTE IMMEDIATE $$
BEGIN
    BEGIN TRANSACTION;
    TRUNCATE TABLE child;
    TRUNCATE TABLE parent;
    COMMIT;
    RETURN '';
END;
$$
;
```

Copy

In this example, the statements are inside a [branching](../../developer-guide/snowflake-scripting/branch) construct.

```
IF (both_rows_are_valid) THEN
    BEGIN
        BEGIN TRANSACTION;
        INSERT INTO parent ...;
        INSERT INTO child ...;
        COMMIT;
    END;
END IF;
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

1. [Syntax](#syntax)
2. [Usage notes](#usage-notes)
3. [Examples](#examples)