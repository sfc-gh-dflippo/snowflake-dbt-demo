---
auto_generated: true
description: 'A FOR loop repeats a sequence of steps a specific number of times. The
  number of times might be specified by the user, or might be specified by the number
  of rows in a cursor. The syntax of these two '
last_scraped: '2026-01-14T16:56:35.750375+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/snowflake-scripting/for.html
title: FOR (Snowflake Scripting) | Snowflake Documentation
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

[Reference](../../reference.md)[Scripting reference](../../sql-reference-snowflake-scripting.md)FOR

# FOR (Snowflake Scripting)[¶](#for-snowflake-scripting "Link to this heading")

A `FOR` loop repeats a sequence of steps a specific number of times. The number of times might be specified by the
user, or might be specified by the number of rows in a [cursor](../../developer-guide/snowflake-scripting/cursors). The syntax
of these two types of `FOR` loops is slightly different.

For more information on loops, see [Working with loops](../../developer-guide/snowflake-scripting/loops).

Note

This [Snowflake Scripting](../../developer-guide/snowflake-scripting/index) construct is valid only within a
[Snowflake Scripting block](../../developer-guide/snowflake-scripting/blocks).

See also:
:   [BREAK](break), [CONTINUE](continue)

## Syntax[¶](#syntax "Link to this heading")

To loop over all rows in a [cursor](../../developer-guide/snowflake-scripting/cursors), use:

> ```
> FOR <row_variable> IN <cursor_name> DO
>     <statement>;
>     [ <statement>; ... ]
> END FOR [ <label> ] ;
> ```
>
> Copy

To loop a specified number of times, use:

> ```
> FOR <counter_variable> IN [ REVERSE ] <start> TO <end> { DO | LOOP }
>     <statement>;
>     [ <statement>; ... ]
> END { FOR | LOOP } [ <label> ] ;
> ```
>
> Copy

Where:

> `row_variable`
> :   Specify a variable name that follows the rules for [Object identifiers](../identifiers).
>
>     Do not add a declaration for this variable in the DECLARE or BEGIN … END sections.
>     The name should not already be defined in the scope of the local block.
>
>     The name is valid inside the `FOR` loop, but not outside the `FOR` loop.
>
>     The `row_variable` holds one row from the cursor. Fields within that row are accessed using dot notation. For example:
>
>     > `my_row_variable.my_column_name`
>
>     A more complete example is included in the examples below.
>
> `counter_variable`
> :   Specify a variable name that follows the rules for [Object identifiers](../identifiers).
>
>     The name of the `counter_variable` is valid only inside the `FOR` loop.
>     If a variable with the same name is declared outside the loop, the outer variable and the loop variable are separate. Inside the
>     loop, references to that name are resolved to the loop variable.
>
>     The code inside the `FOR` loop is allowed to read the value of the counter variable, but should not change it. For
>     example, do not increment the counter variable manually to change the step size.
>
> `start`
> :   This is the initial value of `counter_variable`.
>
>     The starting value should be an INTEGER or an expression that evaluates to an INTEGER.
>
> `end`
> :   This is the final value of `counter_variable`, after the `counter_variable` has been incremented as you loop.
>
>     The ending value should be an INTEGER or an expression that evaluates to an INTEGER.
>
>     The `end` value should be greater than or equal to the `start` value. If `end` is less than
>     `start`, the loop executes 0 times (even if the `REVERSE` keyword is used).
>
> `statement`
> :   A statement can be any of the following:
>
>     * A single SQL statement (including CALL).
>     * A control-flow statement (for example, a [looping](../../developer-guide/snowflake-scripting/loops) or
>       [branching](../../developer-guide/snowflake-scripting/branch) statement).
>     * A nested [block](../../developer-guide/snowflake-scripting/blocks).
>
> `cursor_name`
> :   The name of the cursor to iterate through.
>
> `label`
> :   An optional label. Such a label can be a jump target for a [BREAK (Snowflake Scripting)](break) or
>     [CONTINUE (Snowflake Scripting)](continue) statement. A label must follow the naming rules for
>     [Object identifiers](../identifiers).

## Usage notes[¶](#usage-notes "Link to this heading")

* The loop iterates up to and including the `end` point.

  For example, `FOR i IN 1 TO 10` loops 10 times, and during the final iteration the value of `i` is 10.

  If you use the `REVERSE` keyword, then the loop iterates backwards down to and including the `start` value.
* A loop can contain multiple statements. You can use, but are not required to use, a [BEGIN … END (Snowflake Scripting)](begin)
  [block](../../developer-guide/snowflake-scripting/blocks) to contain those statements.
* The optional keyword `REVERSE` causes Snowflake to start with the `end` value and decrement down to the `start` value.
* Although you can change the value of the `counter_variable` inside the loop, Snowflake recommends that you avoid doing this.
  Changing the value makes the code more difficult to understand.
* If you use the keyword `DO`, then use `END FOR` at the end of the `FOR` loop. If you use the keyword `LOOP`, then use
  `END LOOP` at the end of the `FOR` loop.

## Examples[¶](#examples "Link to this heading")

Cursor-Based FOR Loops:

This example shows how to use a [cursor](../../developer-guide/snowflake-scripting/cursors) to sum the values in the `price`
column of all the rows returned by a query. This stored procedure behaves somewhat like an aggregate function.

> ```
> CREATE or replace TABLE invoices (price NUMBER(12, 2));
> INSERT INTO invoices (price) VALUES
>     (11.11),
>     (22.22);
> ```
>
> Copy
>
> ```
> CREATE OR REPLACE PROCEDURE for_loop_over_cursor()
> RETURNS FLOAT
> LANGUAGE SQL
> AS
> $$
> DECLARE
>     total_price FLOAT;
>     c1 CURSOR FOR SELECT price FROM invoices;
> BEGIN
>     total_price := 0.0;
>     OPEN c1;
>     FOR rec IN c1 DO
>         total_price := total_price + rec.price;
>     END FOR;
>     CLOSE c1;
>     RETURN total_price;
> END;
> $$
> ;
> ```
>
> Copy
>
> Here is the output of the stored procedure:
>
> ```
> CALL for_loop_over_cursor();
> +----------------------+
> | FOR_LOOP_OVER_CURSOR |
> |----------------------|
> |                33.33 |
> +----------------------+
> ```
>
> Copy

Counter-Based FOR Loops:

This example shows how to use a `FOR` loop to iterate a specified number of times:

> ```
> CREATE PROCEDURE simple_for(iteration_limit INTEGER)
> RETURNS INTEGER
> LANGUAGE SQL
> AS
> $$
>     DECLARE
>         counter INTEGER DEFAULT 0;
>     BEGIN
>         FOR i IN 1 TO iteration_limit DO
>             counter := counter + 1;
>         END FOR;
>         RETURN counter;
>     END;
> $$;
> ```
>
> Copy
>
> Here is the output of the stored procedure:
>
> ```
> CALL simple_for(3);
> +------------+
> | SIMPLE_FOR |
> |------------|
> |          3 |
> +------------+
> ```
>
> Copy

The following example shows how to use the `REVERSE` keyword to count backwards.

> ```
> CREATE PROCEDURE reverse_loop(iteration_limit INTEGER)
> RETURNS VARCHAR
> LANGUAGE SQL
> AS
> $$
>     DECLARE
>         values_of_i VARCHAR DEFAULT '';
>     BEGIN
>         FOR i IN REVERSE 1 TO iteration_limit DO
>             values_of_i := values_of_i || ' ' || i::varchar;
>         END FOR;
>         RETURN values_of_i;
>     END;
> $$;
> ```
>
> Copy
>
> Here is the output of the stored procedure:
>
> ```
> CALL reverse_loop(3);
> +--------------+
> | REVERSE_LOOP |
> |--------------|
> |  3 2 1       |
> +--------------+
> ```
>
> Copy

The following example shows the behavior when the loop counter variable has the same name (`i`) as a variable that was already
declared. Within the `FOR` loop, references to `i` resolve to the loop counter variable (not to the variable declared outside of
the loop).

> ```
> CREATE PROCEDURE p(iteration_limit INTEGER)
> RETURNS VARCHAR
> LANGUAGE SQL
> AS
> $$
>     DECLARE
>         counter INTEGER DEFAULT 0;
>         i INTEGER DEFAULT -999;
>         return_value VARCHAR DEFAULT '';
>     BEGIN
>         FOR i IN 1 TO iteration_limit DO
>             counter := counter + 1;
>         END FOR;
>         return_value := 'counter: ' || counter::varchar || '\n';
>         return_value := return_value || 'i: ' || i::VARCHAR;
>         RETURN return_value;
>     END;
> $$;
> ```
>
> Copy
>
> Here is the output of the stored procedure:
>
> ```
> CALL p(3);
> +------------+
> | P          |
> |------------|
> | counter: 3 |
> | i: -999    |
> +------------+
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