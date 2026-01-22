---
auto_generated: true
description: A LOOP loop does not specify a number of iterations or a terminating
  condition. The user must explicitly exit the loop by using BREAK or RETURN inside
  the loop.
last_scraped: '2026-01-14T16:56:34.682138+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/snowflake-scripting/loop
title: LOOP (Snowflake Scripting) | Snowflake Documentation
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

[Reference](../../reference.md)[Scripting reference](../../sql-reference-snowflake-scripting.md)LOOP

# LOOP (Snowflake Scripting)[¶](#loop-snowflake-scripting "Link to this heading")

A `LOOP` loop does not specify a number of iterations or a terminating condition. The user must explicitly
exit the loop by using [BREAK](break) or [RETURN](return) inside the loop.

For more information on loops, see [Working with loops](../../developer-guide/snowflake-scripting/loops).

Note

This [Snowflake Scripting](../../developer-guide/snowflake-scripting/index) construct is valid only within a
[Snowflake Scripting block](../../developer-guide/snowflake-scripting/blocks).

See also:
:   [BREAK](break), [CONTINUE](continue), [RETURN](return)

## Syntax[¶](#syntax "Link to this heading")

```
LOOP
    <statement>;
    [ <statement>; ... ]
END LOOP [ <label> ] ;
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
> `label`
> :   An optional label. Such a label can be a jump target for a [BREAK](break) or
>     [CONTINUE](continue) statement. A label must follow the naming rules for
>     [Object identifiers](../identifiers).

## Usage notes[¶](#usage-notes "Link to this heading")

* A `LOOP` repeats until a `BREAK` or `RETURN` is executed. The `BREAK` or `RETURN` command is almost always
  inside a conditional expression (e.g. `IF` or `CASE`).
* A loop can contain multiple statements. You can use, but are not required to use, a [BEGIN … END](begin)
  [block](../../developer-guide/snowflake-scripting/blocks) to contain those statements.

## Examples[¶](#examples "Link to this heading")

This loop inserts predictable test data into a table:

```
CREATE TABLE dummy_data (ID INTEGER);

CREATE PROCEDURE break_out_of_loop()
RETURNS INTEGER
LANGUAGE SQL
AS
$$
    DECLARE
        counter INTEGER;
    BEGIN
        counter := 0;
        LOOP
            counter := counter + 1;
            IF (counter > 5) THEN
                BREAK;
            END IF;
            INSERT INTO dummy_data (ID) VALUES (:counter);
        END LOOP;
        RETURN counter;
    END;
$$
;
```

Copy

Here is the output of executing the stored procedure:

```
CALL break_out_of_loop();
+-------------------+
| BREAK_OUT_OF_LOOP |
|-------------------|
|                 6 |
+-------------------+
```

Copy

Here is the content of the table after calling the stored procedure:

```
SELECT *
    FROM dummy_data
    ORDER BY ID;
+----+
| ID |
|----|
|  1 |
|  2 |
|  3 |
|  4 |
|  5 |
+----+
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