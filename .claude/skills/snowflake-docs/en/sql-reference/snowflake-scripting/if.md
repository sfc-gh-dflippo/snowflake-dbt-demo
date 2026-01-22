---
auto_generated: true
description: An IF statement provides a way to execute a set of statements if a condition
  is met.
last_scraped: '2026-01-14T16:56:38.262662+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/snowflake-scripting/if
title: IF (Snowflake Scripting) | Snowflake Documentation
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

[Reference](../../reference.md)[Scripting reference](../../sql-reference-snowflake-scripting.md)IF

# IF (Snowflake Scripting)[¶](#if-snowflake-scripting "Link to this heading")

An `IF` statement provides a way to execute a set of statements if a condition is met.

For more information on branching constructs, see [Working with conditional logic](../../developer-guide/snowflake-scripting/branch).

Note

This [Snowflake Scripting](../../developer-guide/snowflake-scripting/index) construct is valid only within a
[Snowflake Scripting block](../../developer-guide/snowflake-scripting/blocks).

## Syntax[¶](#syntax "Link to this heading")

```
IF ( <condition> ) THEN
    <statement>;
    [ <statement>; ... ]
[
ELSEIF ( <condition> ) THEN
    <statement>;
    [ <statement>; ... ]
]
[
ELSE
    <statement>;
    [ <statement>; ... ]
]
END IF;
```

Copy

Where:

> `condition`
> :   An expression that evaluates to a BOOLEAN.
>
> `statement`
> :   A statement can be any of the following:
>
>     * A single SQL statement (including CALL).
>     * A control-flow statement (for example, a [looping](../../developer-guide/snowflake-scripting/loops) or
>       [branching](../../developer-guide/snowflake-scripting/branch) statement).
>     * A nested [block](../../developer-guide/snowflake-scripting/blocks).

## Usage notes[¶](#usage-notes "Link to this heading")

* The keyword `THEN` is required.
* `ELSEIF` is one word (no spaces).
* `END IF` is two words.
* After each `THEN` or `ELSE` clause, the body allows the `BEGIN` and `END` keywords, but does not require
  them, even if the body contains more than one `statement`.
* If the `condition` is NULL, then it is treated as FALSE.

## Examples[¶](#examples "Link to this heading")

Here is an example of a Snowflake Scripting `IF` statement inside a stored procedure:

```
CREATE OR REPLACE PROCEDURE example_if(flag INTEGER)
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
BEGIN
  IF (FLAG = 1) THEN
    RETURN 'one';
  ELSEIF (FLAG = 2) THEN
    RETURN 'two';
  ELSE
    RETURN 'Unexpected input.';
  END IF;
END;
$$
;
```

Copy

Here is the command to call the stored procedure, along with the output:

```
CALL example_if(3);
```

Copy

```
+-------------------+
| EXAMPLE_IF        |
|-------------------|
| Unexpected input. |
+-------------------+
```

For more examples that use the `IF` statement, see:

* [Working with conditional logic](../../developer-guide/snowflake-scripting/branch) - Return different values based on IF conditions
  in a simple anonymous block.
* [Examples for common use cases of Snowflake Scripting](../../developer-guide/snowflake-scripting/use-cases) - Execute SQL statements based on IF conditions in loops.
* [BREAK](break), [LOOP](loop), and [Working with loops](../../developer-guide/snowflake-scripting/loops) -
  Execute BREAK statements to terminate a loop based on IF conditions.
* [EXCEPTION](exception) - Raise exceptions based on IF conditions.

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