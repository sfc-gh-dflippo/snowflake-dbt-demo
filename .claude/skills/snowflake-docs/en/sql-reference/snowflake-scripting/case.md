---
auto_generated: true
description: A CASE statement provides a way to specify multiple conditions.
last_scraped: '2026-01-14T16:56:33.712267+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/snowflake-scripting/case
title: CASE (Snowflake Scripting) | Snowflake Documentation
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

[Reference](../../reference.md)[Scripting reference](../../sql-reference-snowflake-scripting.md)CASE

# CASE (Snowflake Scripting)[¶](#case-snowflake-scripting "Link to this heading")

A `CASE` statement provides a way to specify multiple conditions.

For more information on branching constructs, see [Working with conditional logic](../../developer-guide/snowflake-scripting/branch).

Note

This [Snowflake Scripting](../../developer-guide/snowflake-scripting/index) construct is valid only within a
[Snowflake Scripting block](../../developer-guide/snowflake-scripting/blocks).

## Syntax[¶](#syntax "Link to this heading")

**Simple CASE statement:**

> ```
> CASE ( <expression_to_match> )
>     WHEN <expression> THEN
>         <statement>;
>         [ <statement>; ... ]
>     [ WHEN ... ]
>     [ ELSE
>         <statement>;
>         [ <statement>; ... ]
>     ]
> END [ CASE ] ;
> ```
>
> Copy

Where:

> `expression_to_match`
> :   The expression to match.
>
> `expression`
> :   If the value of this expression matches the value of `expression_to_match`, then the statements in this clause
>     are executed.
>
> `statement`
> :   A statement can be any of the following:
>
>     * A single SQL statement (including CALL).
>     * A control-flow statement (for example, a [looping](../../developer-guide/snowflake-scripting/loops) or
>       [branching](../../developer-guide/snowflake-scripting/branch) statement).
>     * A nested [block](../../developer-guide/snowflake-scripting/blocks).

**Searched CASE statement:**

> ```
> CASE
>     WHEN <boolean_expression> THEN
>         <statement>;
>         [ <statement>; ... ]
>     [ WHEN ... ]
>     [ ELSE
>         <statement>;
>         [ <statement>; ... ]
>     ]
> END [ CASE ] ;
> ```
>
> Copy

Where:

> `boolean_expression`
> :   If this expression evaluates to TRUE, then the statements in this clause are executed.
>
> `statement`
> :   A statement can be any of the following:
>
>     * A single SQL statement (including CALL).
>     * A control-flow statement (for example, a [looping](../../developer-guide/snowflake-scripting/loops) or
>       [branching](../../developer-guide/snowflake-scripting/branch) statement).
>     * A nested [block](../../developer-guide/snowflake-scripting/blocks).

## Usage notes[¶](#usage-notes "Link to this heading")

* If more than one branch of the `CASE` would match the expression, only the first is used.
* When you compare expressions, NULL does not match NULL. If you wish to test explicitly for NULL values, use
  [IS [ NOT ] NULL](../functions/is-null).

## Examples[¶](#examples "Link to this heading")

This example demonstrates a simple `CASE` statement:

> ```
> CREATE PROCEDURE case_demo_01(v VARCHAR)
> RETURNS VARCHAR
> LANGUAGE SQL
> AS
>   BEGIN
>     CASE (v)
>       WHEN 'first choice' THEN
>         RETURN 'one';
>       WHEN 'second choice' THEN
>         RETURN 'two';
>       ELSE
>         RETURN 'unexpected choice';
>     END;
>   END;
> ```
>
> Copy
>
> Note: If you use [Snowflake CLI](../../developer-guide/snowflake-cli/index), [SnowSQL](../../user-guide/snowsql), the Classic Console, or the
> `execute_stream` or `execute_string` method in [Python Connector](../../developer-guide/python-connector/python-connector)
> code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](../../developer-guide/snowflake-scripting/running-examples)):
>
> ```
> CREATE PROCEDURE case_demo_01(v VARCHAR)
> RETURNS VARCHAR
> LANGUAGE SQL
> AS
> $$
>     BEGIN
>         CASE (v)
>             WHEN 'first choice' THEN
>                 RETURN 'one';
>             WHEN 'second choice' THEN
>                 RETURN 'two';
>             ELSE
>                 RETURN 'unexpected choice';
>        END CASE;
>     END;
> $$
> ;
> ```
>
> Copy

When you call this stored procedure, the procedure produces the following output:

> ```
> CALL case_demo_01('second choice');
> +--------------+
> | CASE_DEMO_01 |
> |--------------|
> | two          |
> +--------------+
> ```
>
> Copy

This example demonstrates a searched `CASE` statement:

> ```
> CREATE PROCEDURE case_demo_2(v VARCHAR)
> RETURNS VARCHAR
> LANGUAGE SQL
> AS
>   BEGIN
>     CASE
>       WHEN v = 'first choice' THEN
>         RETURN 'one';
>       WHEN v = 'second choice' THEN
>         RETURN 'two';
>       ELSE
>         RETURN 'unexpected choice';
>     END;
>   END;
> ```
>
> Copy
>
> Note: If you use [Snowflake CLI](../../developer-guide/snowflake-cli/index), [SnowSQL](../../user-guide/snowsql), the Classic Console, or the
> `execute_stream` or `execute_string` method in [Python Connector](../../developer-guide/python-connector/python-connector)
> code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](../../developer-guide/snowflake-scripting/running-examples)):
>
> ```
> CREATE PROCEDURE case_demo_2(v VARCHAR)
> RETURNS VARCHAR
> LANGUAGE SQL
> AS
> $$
>     BEGIN
>         CASE 
>             WHEN v = 'first choice' THEN
>                 RETURN 'one';
>             WHEN v = 'second choice' THEN
>                 RETURN 'two';
>             ELSE
>                 RETURN 'unexpected choice';
>        END CASE;
>     END;
> $$
> ;
> ```
>
> Copy

When you call this stored procedure, the procedure produces the following output:

> ```
> CALL case_demo_2('none of the above');
> +-------------------+
> | CASE_DEMO_2       |
> |-------------------|
> | unexpected choice |
> +-------------------+
> ```
>
> Copy

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