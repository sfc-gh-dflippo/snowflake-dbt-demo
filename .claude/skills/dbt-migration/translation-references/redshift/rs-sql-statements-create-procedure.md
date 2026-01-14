---
description:
  Creates a new stored procedure or replaces an existing procedure for the current database.
  (Redshift SQL Language Reference Create Procedure).
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/redshift/rs-sql-statements-create-procedure
title: SnowConvert AI - Redshift - CREATE PROCEDURE | Snowflake Documentation
---

## Description[¶](#description)

> Creates a new stored procedure or replaces an existing procedure for the current database.
> ([Redshift SQL Language Reference Create Procedure](https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_PROCEDURE.html)).

See the following definitions for more information about procedure clauses:

- [ARGUMENTS MODE](#arguments-mode)
- [POSITIONAL ARGUMENTS](#positional-arguments)
- [NONATOMIC](#nonatomic)
- [PROCEDURE BODY](#procedure-body)
- [SECURITY (DEFINER | INVOKER)](#security-definer-invoker)

## Grammar Syntax[¶](#grammar-syntax)

The following is the SQL syntax to create a Procedure in Amazon Redshift. Click
[here](https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_PROCEDURE.html) to here to go to
Redshifts specification for this syntax.

```
 CREATE [ OR REPLACE ] PROCEDURE sp_procedure_name
  ( [ [ argname ] [ argmode ] argtype [, ...] ] )
[ NONATOMIC ]
AS $$
  procedure_body
$$ LANGUAGE plpgsql
[ { SECURITY INVOKER | SECURITY DEFINER } ]
[ SET configuration_parameter { TO value | = value } ]
```

## Sample Source Patterns[¶](#sample-source-patterns)

### Input Code:[¶](#input-code)

#### Redshift[¶](#redshift)

```
 CREATE PROCEDURE TEST_PROCEDURE()
LANGUAGE PLPGSQL
AS
$$
BEGIN
    NULL;
END;
$$;
```

#### Output Code:[¶](#output-code)

##### Snowflake[¶](#snowflake)

```
 CREATE PROCEDURE TEST_PROCEDURE ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/07/2025",  "domain": "test" }}'
AS
$$
    BEGIN
        NULL;
    END;
$$;
```

## Related EWIs[¶](#related-ewis)

There are no issues for this transformation.

## ALIAS DECLARATION[¶](#alias-declaration)

### Description[¶](#id1)

If the stored procedure’s signature omits the argument name, you can declare an alias for the
argument.

There is no support for this in Snowflake.

To achieve functional equivalence, aliases will be removed, and all usages will be renamed.

When an alias is declared for a parameter nameless, a generated name will be created for the
parameter and the usages. When the alias is for a parameter with name the alias will be replaced by
the real parameter name.

### Grammar Syntax[¶](#id2)

```
 name ALIAS FOR $n;
```

### Sample Source Patterns[¶](#id3)

#### Input Code:[¶](#id4)

##### Redshift[¶](#id5)

```
 CREATE OR REPLACE PROCEDURE test_procedure (integer)
LANGUAGE plpgsql
AS
$$
DECLARE
    first_alias ALIAS  FOR $1;
    second_alias ALIAS  FOR $1;
BEGIN
   INSERT INTO t1
   VALUES (first_alias + 1);
   INSERT INTO t1
   VALUES (second_alias + 2);
END;
$$;

--Notice the parameter already has a name
--and we are defining two alias to the same parameter
CREATE OR REPLACE PROCEDURE test_procedure (PARAMETER1 integer)
LANGUAGE plpgsql
AS
$$
DECLARE
    first_alias ALIAS  FOR $1;
    second_alias ALIAS  FOR $1;
BEGIN
   INSERT INTO t1
   VALUES (first_alias + 1);
   INSERT INTO t1
   VALUES (second_alias + 2);
END;
$$;
```

##### Output Code:[¶](#id6)

##### Snowflake[¶](#id7)

```
 CREATE OR REPLACE PROCEDURE test_procedure (SC_ARG1 integer)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
AS
$$
BEGIN
   INSERT INTO t1
   VALUES (:SC_ARG1 + 1);
   INSERT INTO t1
   VALUES (:SC_ARG1 + 2);
END;
$$;

--Notice the parameter already has a name
--and we are defining two alias to the same parameter
--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "t1" **
CREATE OR REPLACE PROCEDURE test_procedure (PARAMETER1 integer)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
AS
$$
BEGIN
   INSERT INTO t1
   VALUES (:PARAMETER1 + 1);
   INSERT INTO t1
   VALUES (:PARAMETER1 + 2);
END;
$$;
```

### Known Issues[¶](#known-issues)

There are no known issues.

### Related EWIs.[¶](#id8)

There are no related EWIs.

## ARGUMENTS MODE[¶](#arguments-mode)

### Description[¶](#id9)

Amazon Redshift stored procedures support parameters that can be passed during procedure invocation.
These parameters allow you to provide input values, retrieve output values, or use them for input
and output operations. Below is a detailed explanation of the types of parameters, their modes, and
examples of their usage. Snowflake only supports input values.

#### IN (Input Parameters)[¶](#in-input-parameters)

Purpose: Used to pass values into the procedure.

Default Mode: If no mode is specified, parameters are considered IN.

Behavior: Values passed to the procedure cannot be modified inside the procedure.

##### OUT (Output Parameters)[¶](#out-output-parameters)

Purpose: Used to return values from the procedure.

Behavior: Parameters can be modified inside the procedure and are returned to the caller. You cannot
send an initial value.

##### INOUT (Input/Output Parameters)[¶](#inout-input-output-parameters)

Purpose: Used to pass values into the procedure and modify them to return updated values.

Behavior: Combines the behavior of IN and OUT. You must send an initial value regardless of the
output.

### Grammar Syntax[¶](#id10)

```
 [ argname ] [ argmode ] argtype
```

### Sample Source Patterns[¶](#id11)

#### Input Code:[¶](#id12)

##### Redshift[¶](#id13)

```
CREATE OR REPLACE PROCEDURE SP_PARAMS(
IN PARAM1 INTEGER,
OUT PARAM2 INTEGER,
INOUT PARAM3 INTEGER)
AS
$$
    BEGIN
        NULL;
    END;
$$
LANGUAGE plpgsql;
```

##### Output Code:[¶](#id14)

##### Snowflake[¶](#id15)

```
 CREATE OR REPLACE PROCEDURE SP_PARAMS (PARAM1 INTEGER, PARAM2 OUT INTEGER, PARAM3 OUT INTEGER)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/10/2025",  "domain": "no-domain-provided" }}'
AS
$$
    BEGIN
        NULL;
    END;
$$;
```

### Known Issues[¶](#id16)

There are no known issues.

### Related EWIs[¶](#id17)

1. [SCC-EWI-0028](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0028)
   : Type not supported by Snowflake.
2. [SSC-EWI-RS0010](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/redshiftEWI.html#ssc-ewi-rs0010):
   Top-level procedure call with out parameters is not supported.

## PROCEDURE BODY[¶](#procedure-body)

### Description[¶](#id18)

Like Redshift, Snowflake supports CREATE PROCEDURE using $$ procedure_logic $$ as the body. There is
a difference in the Redshift syntax where a word can be inside the $$ like $word$ and used as a
delimiter body like $word$ procedure_logic $word$. SnowConvert AI will transform it by removing the
word, leaving the $$.

### Grammar Syntax[¶](#id19)

```
 AS
$Alias$
  procedure_body
$Alias$
```

### Sample Source Patterns[¶](#id20)

#### Input Code:[¶](#id21)

##### Redshift[¶](#id22)

```
 CREATE OR REPLACE PROCEDURE SP()
AS
$somename$
BEGIN
   NULL;
END;
$somename$
LANGUAGE plpgsql;
```

##### Output Code:[¶](#id23)

##### Snowflake[¶](#id24)

```
 CREATE OR REPLACE PROCEDURE SP ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/07/2025",  "domain": "test" }}'
AS
$$
   BEGIN
      NULL;
   END;
$$;
```

### Known Issues[¶](#id25)

There are no known issues.

### Related EWIs.[¶](#id26)

There are no related EWIs.

## BLOCK STATEMENT[¶](#block-statement)

### Description[¶](#id27)

PL/pgSQL is a block-structured language. The complete body of a procedure is defined in a block,
which contains variable declarations and PL/pgSQL statements. A statement can also be a nested
block, or subblock.

### Grammar Syntax[¶](#id28)

```
 [ <<label>> ]
[ DECLARE
  declarations ]
BEGIN
  statements
EXCEPTION
  WHEN OTHERS THEN
    statements
END [ label ];
```

### Sample Source Patterns[¶](#id29)

#### Input Code:[¶](#id30)

##### Redshift[¶](#id31)

```
 CREATE OR REPLACE PROCEDURE MY_PROCEDURE()
AS
$$
    BEGIN
        NULL;
    END;
$$
LANGUAGE plpgsql;
```

##### Output Code:[¶](#id32)

##### Snowflake[¶](#id33)

```
 CREATE OR REPLACE PROCEDURE MY_PROCEDURE ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/10/2025",  "domain": "test" }}'
AS
$$
    BEGIN
        NULL;
    END;
$$;
```

### Known Issues[¶](#id34)

There are no known issues.

### Related EWIs.[¶](#id35)

There are no related EWIs.

## DECLARE[¶](#declare)

### Description[¶](#id36)

Section to declare all the procedure variables except for loop variables. Redshift supports multiple
DECLARE sections per block statement, since Snowflake does not support this behavior they must be
merged into a single declaration statement per block.

### Grammar Syntax[¶](#id37)

```
 [ DECLARE declarations ]
```

### Sample Source Patterns[¶](#id38)

#### Input Code:[¶](#id39)

##### Redshift[¶](#id40)

```
 CREATE OR REPLACE PROCEDURE first_procedure (first_parameter integer)
LANGUAGE plpgsql
    AS
$$
DECLARE
    i int := first_parameter;
BEGIN
   select i;
END;
$$;

CREATE OR REPLACE PROCEDURE second_procedure (first_parameter integer)
LANGUAGE plpgsql
    AS
$$
DECLARE
    i int := first_parameter;
DECLARE
    j int := first_parameter;
BEGIN
   select i;
END;
$$;
```

##### Output Code:[¶](#id41)

##### Snowflake[¶](#id42)

```
 CREATE OR REPLACE PROCEDURE first_procedure (first_parameter integer)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/11/2025",  "domain": "test" }}'
    AS
$$
   DECLARE
      i int := first_parameter;
BEGIN
   select i;
END;
$$;

CREATE OR REPLACE PROCEDURE second_procedure (first_parameter integer)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/11/2025",  "domain": "test" }}'
    AS
$$
   DECLARE
      i int := first_parameter;
      j int := first_parameter;
BEGIN
   select i;
END;
$$;
```

### Known Issues[¶](#id43)

There are no known issues.

### Related EWIs.[¶](#id44)

There are no related EWIs.

## EXCEPTION[¶](#exception)

### Description[¶](#id45)

When an exception occurs, and you add an exception-handling block, you can write RAISE statements
and most other PL/pgSQL statements. For example, you can raise an exception with a custom message or
insert a record into a logging table.

### Grammar Syntax[¶](#id46)

```
 EXCEPTION
  WHEN OTHERS THEN
    statements
```

### Sample Source Patterns[¶](#id47)

#### Input Code:[¶](#id48)

##### Redshift[¶](#id49)

```
 CREATE OR REPLACE PROCEDURE update_employee_sp() AS
$$
BEGIN
    select var;
EXCEPTION WHEN OTHERS THEN
    RAISE INFO 'An exception occurred.';
END;
$$
LANGUAGE plpgsql;
```

##### Output Code:[¶](#id50)

##### Snowflake[¶](#id51)

```
 CREATE OR REPLACE PROCEDURE update_employee_sp ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
AS
$$
BEGIN
    select var;
EXCEPTION WHEN OTHER THEN
        CALL RAISE_MESSAGE_UDF('INFO', 'An exception occurred.');
        RAISE;
END;
$$;
```

### Known Issues[¶](#id52)

There are no known issues.

### Related EWIs.[¶](#id53)

There are no related EWIs.

## LABEL[¶](#label)

### Description[¶](#id54)

Labels are used in Redshift to qualify a block or to use the EXIT or END statement. Snowflake does
not support labels.

Warning

Since labels are not supported in Snowflake, an EWI will be printed.

### Grammar Syntax[¶](#id55)

```
 [<<label>>]
BEGIN
    ...
END [label]
```

### Sample Source Patterns[¶](#id56)

#### Input Code:[¶](#id57)

##### Redshift[¶](#id58)

```
 CREATE OR REPLACE PROCEDURE test_procedure (first_parameter integer)
LANGUAGE plpgsql
AS
$$
    <<Begin_block_label>>
BEGIN
   INSERT INTO my_test_table
   VALUES (first_parameter);
END;
$$;
```

##### Output Code:[¶](#id59)

##### Snowflake[¶](#id60)

```
 CREATE OR REPLACE PROCEDURE test_procedure (first_parameter integer)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
AS
$$
   !!!RESOLVE EWI!!! /*** SSC-EWI-0094 - LABEL DECLARATION FOR A STATEMENT IS NOT SUPPORTED BY SNOWFLAKE SCRIPTING <<Begin_block_label>> ***/!!!
BEGIN
   INSERT INTO my_test_table
   VALUES (:first_parameter);
END;
$$;
```

### Known Issues[¶](#id61)

There are no known issues.

### Related EWIs[¶](#id62)

1. [SSC-EWI-0094](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0094):
   Label declaration not supported

## NONATOMIC[¶](#nonatomic)

### Description[¶](#id63)

The NONATOMIC commits after each statement in the stored procedure. Snowflake supports an AUTOCOMMIT
parameter. The default setting for AUTOCOMMIT is TRUE (enabled).

While AUTOCOMMIT is enabled, Each statement outside an explicit transaction is treated as inside its
implicit single-statement transaction. In other words, that statement is automatically committed if
it succeeds and automatically rolled back if it fails. In other words, Snowflake works as NONATOMIC
“by default”.

### Grammar Syntax[¶](#id64)

```
 NONATOMIC
```

### Sample Source Patterns[¶](#id65)

#### Input Code:[¶](#id66)

##### Redshift[¶](#id67)

```
 CREATE OR REPLACE PROCEDURE SP_NONATOMIC()
NONATOMIC
AS
$$
    BEGIN
        NULL;
    END;
$$
LANGUAGE plpgsql;
```

##### Output Code:[¶](#id68)

##### Snowflake[¶](#id69)

```
 CREATE OR REPLACE PROCEDURE SP_NONATOMIC ()
RETURNS VARCHAR
----** SSC-FDM-RS0008 - SNOWFLAKE USES AUTOCOMMIT BY DEFAULT. **
--NONATOMIC
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/10/2025",  "domain": "test" }}'
AS
$$
    BEGIN
        NULL;
    END;
$$;
```

### Known Issues[¶](#id70)

There are no known issues.

### Related EWIs.[¶](#id71)

There are no related EWIs.

## POSITIONAL ARGUMENTS[¶](#positional-arguments)

### Description[¶](#id72)

Redshift supports nameless parameters by referencing the parameters by their position using $.
Snowflake does not support this behavior. To ensure functional equivalence, SnowConvert AI can
convert those references by the parameter’s name if the name is present in the definition. If not,
SnowConvert AI will generate a name for the parameter, and the uses will be replaced with the new
name.

### Grammar Syntax[¶](#id73)

```
 $n
```

### Sample Source Patterns[¶](#id74)

#### Input Code:[¶](#id75)

##### Redshift[¶](#id76)

```
 CREATE OR REPLACE PROCEDURE SP_POSITIONAL_REFERENCES(
INTEGER,
param2 INTEGER,
INTEGER)
AS
$$
    DECLARE
        localVariable INTEGER := 0;
    BEGIN
        localVariable := $2 + $3 + $1;
    END;
$$
LANGUAGE plpgsql;
```

##### Output Code:[¶](#id77)

##### Snowflake[¶](#id78)

```
 CREATE OR REPLACE PROCEDURE SP_POSITIONAL_REFERENCES (SC_ARG1
INTEGER,
param2 INTEGER, SC_ARG3 INTEGER)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
AS
$$
    DECLARE
        localVariable INTEGER := 0;
    BEGIN
        localVariable := param2 + SC_ARG3 + SC_ARG1;
    END;
$$;
```

### Known Issues[¶](#id79)

There are no known issues.

### Related EWIs.[¶](#id80)

There are no related EWIs.

## RAISE[¶](#raise)

### Description[¶](#id81)

> Use the `RAISE level` statement to report messages and raise errors.
>
> ([Redshift SQL Language Reference RAISE](https://docs.aws.amazon.com/es_es/redshift/latest/dg/c_PLpgSQL-statements.html#r_PLpgSQL-messages-errors))

**Note:**

RAISE are fully supported by
[Snowflake](https://docs.snowflake.com/en/developer-guide/snowflake-scripting/variables#declaring-a-variable).

### Grammar Syntax[¶](#id82)

```
 RAISE level 'format' [, variable [, ...]];
```

In Amazon Redshift, the `RAISE` statement is used to generate messages in the console or throw
custom exceptions. Redshift allows you to specify different _levels_ to indicate the severity of the
message. In Snowflake, this functionality can be emulated using a user-defined function (UDF) that
makes a call to the console depending on the specified level.

1. **Exception**: When the level is “EXCEPTION”, a custom exception is raised with a general
   message: _“To view the EXCEPTION MESSAGE, you need to check the log.”_ The exception code is
   `-20002`, which informs the user that the custom message can be found in the logs. This is due to
   limitations when sending custom exceptions in Snowflake.
2. **Warning**: If the level is “WARNING”, `SYSTEM$LOG_WARN` is used to print the warning message to
   Snowflake’s log, which helps highlight potential issues without interrupting the flow of
   execution.
3. **Info**: For any other level (such as “INFO”), `SYSTEM$LOG_INFO` is used to print the message to
   the console log, providing more detailed feedback about the system’s state without causing
   critical disruptions.

This approach allows emulating Redshift’s severity levels functionality, adapting them to
Snowflake’s syntax and features, while maintaining flexibility and control over the messages and
exceptions generated during execution.

**Limitations**

- To view logs in Snowflake, it is necessary to have specific privileges, such as the `ACCOUNTADMIN`
  or `SECURITYADMIN` roles.
- Logs in Snowflake are not available immediately and may have a slight delay before the information
  is visible.
- Personalized error messages in exceptions are not displayed like in Redshift. To view custom
  messages, you must access the logs directly.

For further information, please refer to the following
[page](https://docs.snowflake.com/developer-guide/logging-tracing/logging-snowflake-scripting).

### Sample Source Patterns[¶](#id83)

#### Input Code:[¶](#id84)

##### Redshift[¶](#id85)

```
 CREATE OR REPLACE PROCEDURE raise_example(IN user_id INT)
LANGUAGE plpgsql
AS $$
BEGIN
	RAISE EXCEPTION 'User % not exists.', user_id;
END;
$$;
```

##### Output Code:[¶](#id86)

##### Snowflake[¶](#id87)

```
 CREATE OR REPLACE PROCEDURE raise_example (user_id INT)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/11/2025",  "domain": "test" }}'
AS $$
BEGIN
	CALL RAISE_MESSAGE_UDF('EXCEPTION', 'User % not exists.', array_construct(:user_id));
END;
$$;
```

#### UDFs [¶](#udfs)

##### RAISE_MESSAGE_UDF[¶](#raise-message-udf)

```
 CREATE OR REPLACE PROCEDURE RAISE_MESSAGE_UDF(LEVEL VARCHAR, MESSAGE VARCHAR, ARGS VARIANT)
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
    DECLARE
        MY_EXCEPTION EXCEPTION (-20002, 'To view the EXCEPTION MESSAGE, you need to check the log.');
        SC_RAISE_MESSAGE VARCHAR;
    BEGIN
        SC_RAISE_MESSAGE := STRING_FORMAT_UDF(MESSAGE, ARGS);
        IF (LEVEL = 'EXCEPTION') THEN
            SYSTEM$LOG_ERROR(SC_RAISE_MESSAGE);
            RAISE MY_EXCEPTION;
        ELSEIF (LEVEL = 'WARNING') THEN
            SYSTEM$LOG_WARN(SC_RAISE_MESSAGE);
            RETURN 'Warning printed successfully';
        ELSE
            SYSTEM$LOG_INFO(SC_RAISE_MESSAGE);
            RETURN 'Message printed successfully';
        END IF;
    END;
$$;
```

##### STRING_FORMAT_UDF[¶](#string-format-udf)

```
 CREATE OR REPLACE FUNCTION PUBLIC.STRING_FORMAT_UDF(PATTERN VARCHAR, ARGS VARIANT)
RETURNS VARCHAR
LANGUAGE JAVASCRIPT
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "udf",  "convertedOn": "02/11/2025",  "domain": "test" }}'
AS
$$
	var placeholder_str = "{%}";
	var result = PATTERN.replace(/(?<!%)%(?!%)/g, placeholder_str).replace("%%","%");
	for (var i = 0; i < ARGS.length; i++)
	{
		result = result.replace(placeholder_str, ARGS[i]);
	}
	return result;
$$;
```

### Known Issues[¶](#id88)

There are no known issues.

### Related EWIs.[¶](#id89)

There are no related EWIs.

## RETURN[¶](#return)

### Description[¶](#id90)

> The RETURN statement returns back to the caller from a stored procedure.
> ([Redshift SQL Language Reference Return](https://docs.aws.amazon.com/redshift/latest/dg/c_PLpgSQL-statements.html#r_PLpgSQL-return)).

The conversion of the return statement from Amazon Redshift to Snowflake is straightforward, only
considering adding a `NULL` to the return statement on Snowflake.

### Grammar Syntax[¶](#id91)

```
 RETURN;
```

### Sample Source Patterns[¶](#id92)

#### Simple Case[¶](#simple-case)

##### Input Code:[¶](#id93)

##### Redshift[¶](#id94)

```
 CREATE OR REPLACE PROCEDURE procedure1 ()
AS
$$
BEGIN
   RETURN;
END
$$ LANGUAGE plpgsql;
```

##### Output Code:[¶](#id95)

##### Redshift[¶](#id96)

```
 CREATE OR REPLACE PROCEDURE procedure1 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/12/2025",  "domain": "test" }}'
AS
$$
BEGIN
  RETURN NULL;
END
$$;
```

#### When the procedure has out parameters[¶](#when-the-procedure-has-out-parameters)

SnowConvert AI returns a variant with parameters set up as output parameters. So, for each return,
SnowConvert AI will add a variant as a return value.

##### Input Code:[¶](#id97)

##### Redshift[¶](#id98)

```
 CREATE OR REPLACE PROCEDURE procedure1 (OUT output_value VARCHAR)
AS
$$
BEGIN
   RETURN;
END
$$ LANGUAGE plpgsql;
```

##### Output Code:[¶](#id99)

##### Redshift[¶](#id100)

```
 CREATE OR REPLACE PROCEDURE procedure1 (output_value OUT VARCHAR)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
AS
$$
BEGIN
   RETURN NULL;
END
$$;
```

### Known Issues[¶](#id101)

There are no known issues.

### Related EWIs.[¶](#id102)

There are no related EWIs.

## SECURITY (DEFINER | INVOKER)[¶](#security-definer-invoker)

### Description[¶](#id103)

The SECURITY clause in Amazon Redshift stored procedures defines the access control and permissions
context under which the procedure executes. This determines whether the procedure uses the
privileges of the owner (creator) or the caller (user invoking the procedure).

### Grammar Syntax[¶](#id104)

```
 [ { SECURITY INVOKER | SECURITY DEFINER } ]
```

### Sample Source Patterns[¶](#id105)

#### Input Code:[¶](#id106)

##### Redshift[¶](#id107)

```
 CREATE OR REPLACE PROCEDURE SP_SECURITY_INVOKER( )
AS
$$
    BEGIN
        NULL;
    END;
$$
LANGUAGE plpgsql
SECURITY INVOKER
;

CREATE OR REPLACE PROCEDURE SP_SECURITY_DEFINER( )
AS
$$
     BEGIN
        NULL;
    END;
$$
LANGUAGE plpgsql
SECURITY DEFINER;
```

##### Output Code:[¶](#id108)

##### Snowflake[¶](#id109)

```
 CREATE OR REPLACE PROCEDURE SP_SECURITY_INVOKER ( )
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/07/2025",  "domain": "test" }}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        NULL;
    END;
$$
;

CREATE OR REPLACE PROCEDURE SP_SECURITY_DEFINER ( )
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/07/2025",  "domain": "test" }}'
EXECUTE AS OWNER
AS
$$
    BEGIN
        NULL;
    END;
$$;
```

### Known Issues[¶](#id110)

There are no known issues.

### Related EWIs.[¶](#id111)

There are no related EWIs.

## VARIABLE DECLARATION[¶](#variable-declaration)

### Description[¶](#id112)

> Declare all variables in a block, except for loop variables, in the block’s DECLARE section.
>
> ([Redshift SQL Language Reference Variable Declaration](https://docs.aws.amazon.com/redshift/latest/dg/c_PLpgSQL-structure.html#r_PLpgSQL-variable-declaration))

**Note:**

Variable declarations are fully supported by
[Snowflake](https://docs.snowflake.com/en/developer-guide/snowflake-scripting/variables#declaring-a-variable).

### Grammar Syntax[¶](#id113)

```
 DECLARE
name [ CONSTANT ] type [ NOT NULL ] [ { DEFAULT | := } expression ];
```

In Redshift, the `CONSTANT` keyword prevents variable reassignment during execution. Since Snowflake
does not support this keyword, it is removed during transformation. This does not impact
functionality, as the logic should not attempt to reassign a constant variable.

The `NOT NULL` constraint in Redshift ensures a variable cannot be assigned a null value and
requires a non-null default value. As Snowflake does not support this constraint, it is removed
during transformation. However, the default value is retained to maintain functionality.

A variable declare with a Refcursor is transformed to Resultset type, for more
[information](#declare-refcursor).

### Sample Source Patterns[¶](#id114)

#### Input Code:[¶](#id115)

##### Redshift[¶](#id116)

```
 CREATE OR REPLACE PROCEDURE VARIABLE_DECLARATION()
LANGUAGE plpgsql
AS $$
DECLARE
    v_simple_int INT;
    v_default_char CHAR(4) DEFAULT 'ABCD';
    v_default_float FLOAT := 10.00;
    v_constant_char CONSTANT CHAR(4) := 'ABCD';
    v_notnull VARCHAR NOT NULL DEFAULT 'Test default';
    v_refcursor REFCURSOR;
BEGIN
-- Procedure logic
END;
$$;
```

##### Output Code:[¶](#id117)

##### Snowflake[¶](#id118)

```
 CREATE OR REPLACE PROCEDURE VARIABLE_DECLARATION ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
AS $$
        DECLARE
            v_simple_int INT;
            v_default_char CHAR(4) DEFAULT 'ABCD';
            v_default_float FLOAT := 10.00;
            v_constant_char CHAR(4) := 'ABCD';
            --** SSC-FDM-PG0012 - NOT NULL CONSTRAINT HAS BEEN REMOVED. ASSIGNING NULL TO THIS VARIABLE WILL NO LONGER CAUSE A FAILURE. **
            v_notnull VARCHAR DEFAULT 'Test default';
            v_refcursor RESULTSET;
BEGIN
            NULL;
-- Procedure logic
END;
$$;
```

### Known Issues [¶](#id119)

No issues were found.

### Related EWIs[¶](#id120)

1. [SSC-FDM-PG0012](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/postgresqlFDM.html#ssc-fdm-pg0012):
   NOT NULL constraint has been removed. Assigning NULL to this variable will no longer cause a
   failure.

## TRANSACTIONS[¶](#transactions)

## COMMIT[¶](#commit)

### Description[¶](#id121)

> Commits the current transaction to the database. This command makes the database updates from the
> transaction permanent.
> ([Redshift SQL Language Reference COMMIT](https://docs.aws.amazon.com/redshift/latest/dg/r_COMMIT.html))

Grammar Syntax

```
COMMIT [WORK | TRANSACTION]
```

### Sample Source Patterns[¶](#id122)

#### Setup data[¶](#setup-data)

##### Redshift[¶](#id123)

##### Query[¶](#query)

```
 CREATE TABLE transaction_values_test
(
    col1 INTEGER
);
```

##### Snowflake[¶](#id124)

##### Query[¶](#id125)

```
 CREATE TABLE transaction_values_test
(
    col1 INTEGER
);
```

#### COMMIT with TRANSACTION keyword[¶](#commit-with-transaction-keyword)

The TRANSACTION keyword is not supported in Snowflake. However, since it does not have an impact on
functionality it will just be removed.

##### Redshift[¶](#id126)

##### Query[¶](#id127)

```
 COMMIT TRANSACTION;
```

##### Snowflake[¶](#id128)

##### Query[¶](#id129)

```
 COMMIT;
```

#### COMMIT in a default transaction behavior procedure (without NONATOMIC clause)[¶](#commit-in-a-default-transaction-behavior-procedure-without-nonatomic-clause)

In order to avoid out of scope transaction exceptions in Snowflake, the usages of COMMIT will be
matched with BEGIN TRANSACTION.

When multiple COMMIT statements are present in the procedure, multiple BEGIN TRANSACTION statements
will be generated after every COMMIT to emulate the Redshift transaction behavior.

##### Redshift[¶](#id130)

##### Query[¶](#id131)

```
 CREATE OR REPLACE PROCEDURE transaction_test(a INT)
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO transaction_values_test VALUES (a);
    COMMIT;
    INSERT INTO transaction_values_test VALUES (a + 1);
    COMMIT;
END
$$;

CALL transaction_test(120);

SELECT * FROM transaction_values_test;
```

##### Result[¶](#result)

```
+------+
<!-- prettier-ignore -->
|col1|
+------+
<!-- prettier-ignore -->
|120|
|121|
+------+
```

##### Snowflake[¶](#id132)

##### Query[¶](#id133)

```
 CREATE OR REPLACE PROCEDURE transaction_test (a INT)
RETURNS VARCHAR
    LANGUAGE SQL
    AS $$
BEGIN
    BEGIN TRANSACTION;
    INSERT INTO transaction_values_test
    VALUES (:a);
    COMMIT;
    BEGIN TRANSACTION;
    INSERT INTO transaction_values_test
    VALUES (:a + 1);
    COMMIT;
END
$$;

CALL transaction_test(120);

SELECT * FROM
    transaction_values_test;
```

##### Result[¶](#id134)

```
+------+
<!-- prettier-ignore -->
|col1|
+------+
<!-- prettier-ignore -->
|120|
|121|
+------+
```

#### COMMIT in a procedure with NONATOMIC behavior[¶](#commit-in-a-procedure-with-nonatomic-behavior)

The NONATOMIC behavior from Redshift is emulated in Snowflake by using the session parameter
AUTOCOMMIT set to true.

Since the AUTOCOMMIT session parameter is assumed to be true by SnowConvert AI, the COMMIT statement
inside NONATOMIC procedures is left as is.

##### Redshift[¶](#id135)

##### Query[¶](#id136)

```
 CREATE OR REPLACE PROCEDURE nonatomic_procedure(a int)
    NONATOMIC
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO transaction_values_test values (a + 2);
    INSERT INTO transaction_values_test values (a + 3);
    COMMIT;
END
$$;

CALL nonatomic_procedure(10);

SELECT * FROM transaction_values_test;
```

##### Result[¶](#id137)

```
+------+
<!-- prettier-ignore -->
|col1|
+------+
<!-- prettier-ignore -->
|12|
|13|
+------+
```

##### Snowflake[¶](#id138)

##### Query[¶](#id139)

```
 CREATE OR REPLACE PROCEDURE nonatomic_procedure (a int)
RETURNS VARCHAR
--    --** SSC-FDM-RS0008 - SNOWFLAKE USES AUTOCOMMIT BY DEFAULT. **
--    NONATOMIC
    LANGUAGE SQL
    COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
    AS $$
BEGIN
    INSERT INTO transaction_values_test
    values (:a + 2);
    INSERT INTO transaction_values_test
    values (:a + 3);
    COMMIT;
END
$$;

CALL nonatomic_procedure(10);

SELECT * FROM
transaction_values_test;
```

##### Result[¶](#id140)

```
+------+
<!-- prettier-ignore -->
|col1|
+------+
<!-- prettier-ignore -->
|12|
|13|
+------+
```

### Known Issues[¶](#id141)

**1. COMMIT inside a nested procedure call**

In Redshift, when a COMMIT statement is specified in a nested procedure call, the command will
commit all pending work from previous statements in the current and parent scopes. Committing the
parent scope actions is not supported in Snowflake, when this case is detected an FDM will be
generated.

#### Redshift[¶](#id142)

##### Query[¶](#id143)

```
 CREATE OR REPLACE PROCEDURE transaction_test(a INT)
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO transaction_values_test VALUES (a);
    COMMIT;
END
$$;

CREATE OR REPLACE PROCEDURE nested_transaction_test(a INT)
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO transaction_values_test values (a);
    INSERT INTO transaction_values_test values (a + 1);
    INSERT INTO transaction_values_test values (a + 2);
    CALL transaction_test(a + 3);
END
$$;
```

##### Snowflake[¶](#id144)

##### Query[¶](#id145)

```
 CREATE OR REPLACE PROCEDURE transaction_test (a INT)
RETURNS VARCHAR
    LANGUAGE SQL
    COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
    AS $$
BEGIN
    BEGIN TRANSACTION;
    INSERT INTO transaction_values_test
    VALUES (:a);
    COMMIT;
END
$$;

CREATE OR REPLACE PROCEDURE nested_transaction_test (a INT)
RETURNS VARCHAR
    LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
    AS $$
BEGIN
    INSERT INTO transaction_values_test
    values (:a);
    INSERT INTO transaction_values_test
    values (:a + 1);
    INSERT INTO transaction_values_test
    values (:a + 2);
    --** SSC-FDM-RS0006 - CALLED PROCEDURE CONTAINS USAGES OF COMMIT/ROLLBACK, MODIFYING THE CURRENT TRANSACTION IN CHILD SCOPES IS NOT SUPPORTED IN SNOWFLAKE **
    CALL transaction_test(:a + 3);
END
$$;
```

### Known Issues[¶](#id146)

There are no known issues.

### Related EWIs[¶](#id147)

1. [SSC-FDM-RS0006](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/redshiftFDM.html#ssc-fdm-rs0006):
   Called procedure contains usages of COMMIT/ROLLBACK, modifying the current transaction in child
   scopes is not supported in Snowflake.

## ROLLBACK[¶](#rollback)

### Description[¶](#id148)

> Stops the current transaction and discards all updates made by that transaction.
> ([Redshift SQL Language Reference ROLLBACK](https://docs.aws.amazon.com/redshift/latest/dg/r_ROLLBACK.html))

Grammar Syntax

```
ROLLBACK [WORK | TRANSACTION]
```

### Sample Source Patterns[¶](#id149)

#### Setup data[¶](#id150)

##### Redshift[¶](#id151)

##### Query[¶](#id152)

```
 CREATE TABLE transaction_values_test
(
    col1 INTEGER
);
```

##### Snowflake[¶](#id153)

##### Query[¶](#id154)

```
 CREATE TABLE transaction_values_test
(
    col1 INTEGER
);
```

#### ROLLBACK with TRANSACTION keyword[¶](#rollback-with-transaction-keyword)

The TRANSACTION keyword is not supported in Snowflake. However, since it does not have an impact on
functionality it will just be removed.

##### Redshift[¶](#id155)

##### Query[¶](#id156)

```
 ROLLBACK TRANSACTION;
```

##### Snowflake[¶](#id157)

##### Query[¶](#id158)

```
 ROLLBACK;
```

#### ROLLBACK in a default transaction behavior procedure (without NONATOMIC clause)[¶](#rollback-in-a-default-transaction-behavior-procedure-without-nonatomic-clause)

In order to avoid out of scope transaction exceptions in Snowflake, the usages of ROLLBACK will be
matched with BEGIN TRANSACTION.

When multiple transaction control statements are present in the procedure, multiple BEGIN
TRANSACTION statements will be generated after every each one of them to emulate the Redshift
transaction behavior.

##### Redshift[¶](#id159)

##### Query[¶](#id160)

```
 CREATE OR REPLACE PROCEDURE transaction_test(a INT)
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO transaction_values_test values (a);
    COMMIT;
    insert into transaction_values_test values (80);
    insert into transaction_values_test values (55);
    ROLLBACK;
END
$$;

CALL transaction_test(120);

SELECT * FROM transaction_values_test;
```

##### Result[¶](#id161)

```
+------+
<!-- prettier-ignore -->
|col1|
+------+
<!-- prettier-ignore -->
|120|
+------+
```

##### Snowflake[¶](#id162)

##### Query[¶](#id163)

```
 CREATE OR REPLACE PROCEDURE transaction_test (a INT)
RETURNS VARCHAR
    LANGUAGE SQL
    AS $$
BEGIN
    BEGIN TRANSACTION;
    INSERT INTO transaction_values_test values (:a);
    COMMIT;
    BEGIN TRANSACTION;
    insert into transaction_values_test values (80);
    insert into transaction_values_test values (55);
    ROLLBACK;
END
$$;

CALL transaction_test(120);

SELECT * FROM
    transaction_values_test;
```

##### Result[¶](#id164)

```
+------+
<!-- prettier-ignore -->
|col1|
+------+
<!-- prettier-ignore -->
|120|
+------+
```

#### ROLLBACK in a procedure with NONATOMIC behavior[¶](#rollback-in-a-procedure-with-nonatomic-behavior)

The NONATOMIC behavior from Redshift is emulated in Snowflake by using the session parameter
AUTOCOMMIT set to true.

Since the AUTOCOMMIT session parameter is assumed to be true by SnowConvert AI, the ROLLBACK
statement inside NONATOMIC procedures is left as is.

##### Redshift[¶](#id165)

##### Query[¶](#id166)

```
 CREATE OR REPLACE PROCEDURE nonatomic_procedure(a int)
    NONATOMIC
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO transaction_values_test values (a);
    INSERT INTO transaction_values_test values (a + 1);
    ROLLBACK;
    INSERT INTO transaction_values_test values (a + 2);
    INSERT INTO transaction_values_test values (a + 3);
    COMMIT;
END
$$;

CALL nonatomic_procedure(10);

SELECT * FROM transaction_values_test;
```

##### Result[¶](#id167)

```
+------+
<!-- prettier-ignore -->
|col1|
+------+
<!-- prettier-ignore -->
|10|
|11|
|12|
|13|
+------+
```

##### Snowflake[¶](#id168)

##### Query[¶](#id169)

```
 CREATE OR REPLACE PROCEDURE nonatomic_procedure (a int)
RETURNS VARCHAR
--    --** SSC-FDM-RS0008 - SNOWFLAKE USES AUTOCOMMIT BY DEFAULT. **
--    NONATOMIC
    LANGUAGE SQL
    COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
    AS $$
BEGIN
    INSERT INTO transaction_values_test
    values (:a);
    INSERT INTO transaction_values_test
    values (:a + 1);
    ROLLBACK;
    INSERT INTO transaction_values_test
    values (:a + 2);
    INSERT INTO transaction_values_test
    values (:a + 3);
    COMMIT;
END
$$;

CALL nonatomic_procedure(10);

SELECT * FROM
transaction_values_test;
```

##### Result[¶](#id170)

```
+------+
<!-- prettier-ignore -->
|col1|
+------+
<!-- prettier-ignore -->
|10|
|11|
|12|
|13|
+------+
```

### Known Issues[¶](#id171)

**1. ROLLBACK inside a nested procedure call**

In Redshift, when a ROLLBACK statement is specified in a nested procedure call, the command will
commit all pending work from previous statements in the current and parent scopes. Committing the
parent scope actions is not supported in Snowflake, when this case is detected an FDM will be
generated.

#### Redshift[¶](#id172)

##### Query[¶](#id173)

```
 CREATE OR REPLACE PROCEDURE transaction_test(a int)
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO transaction_values_test values (a);
    ROLLBACK;
    INSERT INTO transaction_values_test values (a + 1);
END
$$;

CREATE OR REPLACE PROCEDURE nested_transaction_test(a int)
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO transaction_values_test values (a);
    CALL transaction_test(a + 3);
    COMMIT;
END
$$;
```

##### Snowflake[¶](#id174)

##### Query[¶](#id175)

```
 CREATE OR REPLACE PROCEDURE transaction_test (a int)
RETURNS VARCHAR
    LANGUAGE SQL
    COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
    AS $$
BEGIN
    BEGIN TRANSACTION;
    INSERT INTO transaction_values_test
    values (:a);
    ROLLBACK;
    BEGIN TRANSACTION;
    INSERT INTO transaction_values_test
    values (:a + 1);
    COMMIT;
END
$$;

CREATE OR REPLACE PROCEDURE nested_transaction_test (a int)
RETURNS VARCHAR
    LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
    AS $$
BEGIN
    BEGIN TRANSACTION;
    INSERT INTO transaction_values_test
    values (:a);
    --** SSC-FDM-RS0006 - CALLED PROCEDURE CONTAINS USAGES OF COMMIT/ROLLBACK, MODIFYING THE CURRENT TRANSACTION IN CHILD SCOPES IS NOT SUPPORTED IN SNOWFLAKE **
    CALL transaction_test(:a + 3);
    COMMIT;
END
$$;
```

**2. ROLLBACK of DDL statements**

In Snowflake, DDL statements perform an implicit commit whenever they are executed inside a
procedure, making effective all the work prior to executing the DDL as well as the DDL itself. This
causes the ROLLBACK statement to not be able to discard any changes before that point, this issue
will be informed using an FDM.

##### Redshift[¶](#id176)

##### Query[¶](#id177)

```
 CREATE OR REPLACE PROCEDURE rollback_ddl(a int)
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO transaction_values_test values (a);
    CREATE TABLE someRollbackTable
    (
        col1 INTEGER
    );

    INSERT INTO someRollbackTable values (a);
    ROLLBACK;
END
$$;
```

##### Snowflake[¶](#id178)

##### Query[¶](#id179)

```
 CREATE OR REPLACE PROCEDURE rollback_ddl (a int)
RETURNS VARCHAR
    LANGUAGE SQL
    COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
    AS $$
BEGIN
    BEGIN TRANSACTION;
    INSERT INTO transaction_values_test
    values (:a);
    CREATE TABLE someRollbackTable
    (
        col1 INTEGER
    );
    BEGIN TRANSACTION;
    INSERT INTO someRollbackTable
    values (:a);
    --** SSC-FDM-RS0007 - DDL STATEMENTS PERFORM AN AUTOMATIC COMMIT, ROLLBACK WILL NOT WORK AS EXPECTED **
    ROLLBACK;
END
$$;
```

### Known Issues[¶](#id180)

There are no known issues.

### Related EWIs[¶](#id181)

1. [SSC-FDM-RS0006](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/redshiftFDM.html#ssc-fdm-rs0006):
   Called procedure contains usages of COMMIT/ROLLBACK, modifying the current transaction in child
   scopes is not supported in Snowflake.
2. [SSC-FDM-RS0007](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/redshiftFDM.html#ssc-fdm-rs0007):
   DDL statements perform an automatic COMMIT, ROLLBACK will not work as expected.

## TRUNCATE[¶](#truncate)

### Description[¶](#id182)

> Deletes all of the rows from a table without doing a table scan
> ([Redshift SQL Language Reference TRUNCATE](https://docs.aws.amazon.com/redshift/latest/dg/r_TRUNCATE.html))

Grammar Syntax

```
TRUNCATE [TABLE] table_name
```

### Sample Source Patterns[¶](#id183)

#### Setup data[¶](#id184)

##### Redshift[¶](#id185)

##### Query[¶](#id186)

```
 CREATE TABLE transaction_values_test
(
    col1 INTEGER
);
```

##### Snowflake[¶](#id187)

##### Query[¶](#id188)

```
 CREATE TABLE transaction_values_test
(
    col1 INTEGER
);
```

#### TRUNCATE in a default transaction behavior procedure (without NONATOMIC clause)[¶](#truncate-in-a-default-transaction-behavior-procedure-without-nonatomic-clause)

Since the TRUNCATE statement automatically commits the transaction it is executed in, any of its
usages will generate a COMMIT statement in Snowflake to emulate this behavior.

Since a COMMIT statement is generated the same BEGIN TRANSACTION statement generation will be
applied to TRUNCATE. For more information check the
[COMMIT translation specification](#commit-in-a-default-transaction-behavior-procedure-without-nonatomic-clause).

##### Redshift[¶](#id189)

##### Query[¶](#id190)

```
 CREATE OR REPLACE PROCEDURE truncate_in_procedure(a int)
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO transaction_values_test VALUES (a);
    TRUNCATE TABLE transaction_values_test;
    INSERT INTO transaction_values_test VALUES (a + 12);
    COMMIT;
END
$$;

CALL truncate_in_procedure(10);

SELECT * FROM transaction_values_test;
```

##### Result[¶](#id191)

```
+------+
<!-- prettier-ignore -->
|col1|
+------+
<!-- prettier-ignore -->
|22|
+------+
```

##### Snowflake[¶](#id192)

##### Query[¶](#id193)

```
 CREATE OR REPLACE PROCEDURE truncate_in_procedure (a int)
RETURNS VARCHAR
    LANGUAGE SQL
    AS $$
BEGIN
    BEGIN TRANSACTION;
    INSERT INTO transaction_values_test
    VALUES (:a);
    TRUNCATE TABLE transaction_values_test;
    COMMIT;
    BEGIN TRANSACTION;
    INSERT INTO transaction_values_test
    VALUES (:a + 12);
    COMMIT;
END
$$;

CALL truncate_in_procedure(10);

SELECT * FROM
    transaction_values_test;
```

##### Result[¶](#id194)

```
+------+
<!-- prettier-ignore -->
|col1|
+------+
<!-- prettier-ignore -->
|22|
+------+
```

#### TRUNCATE in a procedure with NONATOMIC behavior[¶](#truncate-in-a-procedure-with-nonatomic-behavior)

The NONATOMIC behavior from Redshift is emulated in Snowflake by using the session parameter
AUTOCOMMIT set to true.

Since the AUTOCOMMIT session parameter is assumed to be true by SnowConvert AI, the TRUNCATE
statement inside NONATOMIC procedures is left as is, there is no need to generate a COMMIT statement
because every statement is automatically commited when executed.

##### Redshift[¶](#id195)

##### Query[¶](#id196)

```
 CREATE OR REPLACE PROCEDURE nonatomic_procedure(a int)
    NONATOMIC
    LANGUAGE plpgsql
    AS $$
BEGIN
    TRUNCATE TABLE transaction_values_test;
    INSERT INTO transaction_values_test values (a);
    INSERT INTO transaction_values_test values (a + 1);
    ROLLBACK;
    INSERT INTO transaction_values_test values (a + 2);
    INSERT INTO transaction_values_test values (a + 3);
    COMMIT;
END
$$;

CALL nonatomic_procedure(10);

SELECT * FROM transaction_values_test;
```

##### Result[¶](#id197)

```
+------+
<!-- prettier-ignore -->
|col1|
+------+
<!-- prettier-ignore -->
|10|
|11|
|12|
|13|
+------+
```

##### Snowflake[¶](#id198)

##### Query[¶](#id199)

```
 CREATE OR REPLACE PROCEDURE nonatomic_procedure (a int)
RETURNS VARCHAR
--    --** SSC-FDM-RS0008 - SNOWFLAKE USES AUTOCOMMIT BY DEFAULT. **
--    NONATOMIC
    LANGUAGE SQL
    COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
    AS $$
BEGIN
    TRUNCATE TABLE transaction_values_test;
    INSERT INTO transaction_values_test
    values (:a);
    INSERT INTO transaction_values_test
    values (:a + 1);
    ROLLBACK;
    INSERT INTO transaction_values_test
    values (:a + 2);
    INSERT INTO transaction_values_test
    values (:a + 3);
    COMMIT;
END
$$;

CALL nonatomic_procedure(10);

SELECT * FROM
transaction_values_test;
```

##### Result[¶](#id200)

```
+------+
<!-- prettier-ignore -->
|col1|
+------+
<!-- prettier-ignore -->
|10|
|11|
|12|
|13|
+------+
```

### Known Issues[¶](#id201)

**1. TRUNCATE inside a nested procedure call**

In Redshift, when a COMMIT statement is specified in a nested procedure call, the command will
commit all pending work from previous statements in the current and parent scopes. Committing the
parent scope actions is not supported in Snowflake, when this case is detected an FDM will be
generated.

#### Redshift[¶](#id202)

##### Query[¶](#id203)

```
 CREATE OR REPLACE PROCEDURE transaction_test(a INT)
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO transaction_values_test VALUES (a);
    TRUNCATE TABLE transaction_values_test;
END
$$;

CREATE OR REPLACE PROCEDURE nested_transaction_test(a INT)
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO transaction_values_test values (a);
    INSERT INTO transaction_values_test values (a + 1);
    INSERT INTO transaction_values_test values (a + 2);
    CALL transaction_test(a + 3);
END
$$;
```

##### Snowflake[¶](#id204)

##### Query[¶](#id205)

```
 CREATE OR REPLACE PROCEDURE transaction_test (a INT)
RETURNS VARCHAR
    LANGUAGE SQL
    COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
    AS $$
BEGIN
    BEGIN TRANSACTION;
    INSERT INTO transaction_values_test
    VALUES (:a);
    TRUNCATE TABLE transaction_values_test;
    COMMIT;
END
$$;

CREATE OR REPLACE PROCEDURE nested_transaction_test (a INT)
RETURNS VARCHAR
    LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
    AS $$
BEGIN
    INSERT INTO transaction_values_test
    values (:a);
    INSERT INTO transaction_values_test
    values (:a + 1);
    INSERT INTO transaction_values_test
    values (:a + 2);
    --** SSC-FDM-RS0006 - CALLED PROCEDURE CONTAINS USAGES OF COMMIT/ROLLBACK, MODIFYING THE CURRENT TRANSACTION IN CHILD SCOPES IS NOT SUPPORTED IN SNOWFLAKE **
    CALL transaction_test(:a + 3);
END
$$;
```

### Known Issues[¶](#id206)

There are no known issues.

### Related EWIs[¶](#id207)

1. [SSC-FDM-RS0006](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/redshiftFDM.html#ssc-fdm-rs0006):
   Called procedure contains usages of COMMIT/ROLLBACK, modifying the current transaction in child
   scopes is not supported in Snowflake.

## CONDITIONS[¶](#conditions)

## CASE[¶](#case)

### Description[¶](#id208)

> The `CASE` statement in Redshift lets you return values based on conditions, enabling conditional
> logic in queries. It has two forms: simple and searched.
> ([Redshift SQL Language Reference Conditionals: Case](https://docs.aws.amazon.com/redshift/latest/dg/c_PLpgSQL-statements.html#r_PLpgSQL-conditionals-case)).

### Simple Case[¶](#id209)

A simple CASE statement provides conditional execution based on equality of operands.

**Note:**

Simple Case are fully supported by
[Snowflake](https://docs.snowflake.com/en/developer-guide/snowflake-scripting/variables#declaring-a-variable).

### Grammar Syntax[¶](#id210)

```
 CASE search-expression
WHEN expression [, expression [ ... ]] THEN
  statements
[ WHEN expression [, expression [ ... ]] THEN
  statements
  ... ]
[ ELSE
  statements ]
END CASE;
```

### Sample Source Patterns[¶](#id211)

#### Input Code:[¶](#id212)

##### Redshift[¶](#id213)

```
 CREATE OR REPLACE PROCEDURE proc1(x INT)
LANGUAGE plpgsql
AS $$
BEGIN
  CASE x
WHEN 1, 2 THEN
  NULL;
ELSE
  NULL;
END CASE;
END;
$$;
```

##### Output Code:[¶](#id214)

##### Redshift[¶](#id215)

```
 CREATE OR REPLACE PROCEDURE proc1 (x INT)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/14/2025",  "domain": "test" }}'
AS $$
BEGIN
  CASE x
    WHEN 1 THEN
      NULL;
    WHEN 2 THEN
      NULL;
   ELSE
     NULL;
  END CASE;
END;
$$;
```

### Searched Case[¶](#searched-case)

**Note:**

Searched Case are fully supported by
[Snowflake](https://docs.snowflake.com/en/developer-guide/snowflake-scripting/variables#declaring-a-variable).

### Grammar Syntax[¶](#id216)

```
 CASE
WHEN boolean-expression THEN
  statements
[ WHEN boolean-expression THEN
  statements
  ... ]
[ ELSE
  statements ]
END CASE;
```

### Sample Source Patterns[¶](#id217)

#### Input Code:[¶](#id218)

##### Redshift[¶](#id219)

```
 CREATE PROCEDURE PROC1 (paramNumber int)
LANGUAGE plpgsql
AS $$
DECLARE
    result VARCHAR(100);
BEGIN
CASE
  WHEN paramNumber BETWEEN 0 AND 10 THEN
    result := 'value is between zero and ten';
  WHEN paramNumber BETWEEN 11 AND 20 THEN
    result := 'value is between eleven and twenty';
  END CASE;
END;
$$;
```

##### Output Code:[¶](#id220)

##### Redshift[¶](#id221)

```
 CREATE PROCEDURE PROC1 (paramNumber int)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
AS $$
    DECLARE
      result VARCHAR(100);
      case_not_found EXCEPTION (-20002, 'Case not found.');
BEGIN
CASE
  WHEN paramNumber BETWEEN 0 AND 10 THEN
    result := 'value is between zero and ten';
  WHEN paramNumber BETWEEN 11 AND 20 THEN
    result := 'value is between eleven and twenty';
  ELSE
    RAISE case_not_found;
  END CASE;
END;
$$;
```

#### CASE Without ELSE[¶](#case-without-else)

In Redshift, when a `CASE` expression is executed and none of the validated conditions are met, and
there is no `ELSE` defined, the exception ‘CASE NOT FOUND’ is triggered. In Snowflake, the code
executes but returns no result. To maintain the same functionality in Snowflake in this scenario, an
exception with the same name will be declared and executed if none of the `CASE` conditions are met.

**Note:**

Case Without Else are fully supported by
[Snowflake](https://docs.snowflake.com/en/developer-guide/snowflake-scripting/variables#declaring-a-variable).

##### Input Code:[¶](#id222)

##### Redshift[¶](#id223)

```
 CREATE OR REPLACE PROCEDURE procedure1 (input_value INT)
AS $$
BEGIN
  CASE input_value
  WHEN 1 THEN
   NULL;
  END CASE;
END;
$$ LANGUAGE plpgsql;
```

##### Output Code:[¶](#id224)

##### Redshift[¶](#id225)

```
 CREATE OR REPLACE PROCEDURE procedure1 (input_value INT)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
AS $$
    DECLARE
      case_not_found EXCEPTION (-20002, 'Case not found.');
BEGIN
  CASE input_value
  WHEN 1 THEN
   NULL;
  ELSE
   RAISE case_not_found;
  END CASE;
END;
$$;
```

### Known Issues[¶](#id226)

There are no known issues.

### Related EWIs.[¶](#id227)

There are no related EWIs.

## IF[¶](#if)

### Description[¶](#id228)

> This statement allows you to make decisions based on certain conditions.
> ([Redshift SQL Language Reference Conditionals: IF](https://docs.aws.amazon.com/redshift/latest/dg/c_PLpgSQL-statements.html#r_PLpgSQL-conditionals-if)).

SnowConvert AI will add the parenthesis in the conditions and change the keyword ELSIF by ELSEIF
since Redshift does not require the parenthesis in the conditions and ELSIF is the keyword.

### Grammar Syntax[¶](#id229)

```
 IF boolean-expression THEN
  statements
[ ELSIF boolean-expression THEN
  statements
[ ELSIF boolean-expression THEN
  statements
    ...] ]
[ ELSE
  statements ]
END IF;
```

### Sample Source Patterns[¶](#id230)

#### Input Code:[¶](#id231)

##### Redshift[¶](#id232)

```
 CREATE PROCEDURE PROC1 (paramNumber int)
LANGUAGE plpgsql
AS $$
DECLARE
    result VARCHAR(100);
BEGIN
    IF paramNumber = 0 THEN
      result := 'zero';
    ELSIF paramNumber > 0 THEN
      result := 'positive';
    ELSIF paramNumber < 0 THEN
      result := 'negative';
    ELSE
      result := 'NULL';
    END IF;
END;
$$;
```

##### Output Code:[¶](#id233)

##### Redshift[¶](#id234)

```
 CREATE PROCEDURE PROC1 (paramNumber int)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
AS $$
        DECLARE
            result VARCHAR(100);
BEGIN
            IF (:paramNumber = 0) THEN
                result := 'zero';
            ELSEIF (:paramNumber > 0) THEN
                result := 'positive';
            ELSEIF (:paramNumber < 0) THEN
                result := 'negative';
              ELSE
                result := 'NULL';
            END IF;
END;
$$;
```

### Known Issues[¶](#id235)

There are no known issues.

### Related EWIs.[¶](#id236)

There are no related EWIs.

## LOOPS[¶](#loops)

### Description[¶](#id237)

These statements are used to repeat a block of code until the specified condition.
([Redshift SQL Language Reference Loops](https://docs.aws.amazon.com/redshift/latest/dg/c_PLpgSQL-statements.html#r_PLpgSQL-loops)).

[CONTINUE](#continue) [FOR](#for) [LOOP](#loop) [WHILE](#while) [EXIT](#exit)

## CONTINUE[¶](#continue)

### Description[¶](#id238)

> When the CONTINUE conditions are true, the loop can continue the execution, when is false stop the
> loop.
> ([Redshift SQL Language Reference Conditionals: CONTINUE](https://docs.aws.amazon.com/redshift/latest/dg/c_PLpgSQL-statements.html#r_PLpgSQL-loops)).

Warning

CONTINUE are partial supported by
[Snowflake](https://docs.snowflake.com/en/developer-guide/snowflake-scripting/variables#declaring-a-variable).

### Grammar Syntax[¶](#id239)

```
 CONTINUE [ label ] [ WHEN expression ];
```

### Sample Source Patterns[¶](#id240)

#### Input Code:[¶](#id241)

##### Redshift[¶](#id242)

```
 CREATE OR REPLACE PROCEDURE procedure1 (x INT)
    LANGUAGE plpgsql
AS $$
DECLARE
    i INTEGER := 0;
BEGIN
    <<simple_loop_when>>
    LOOP
        i := i + 1;
        CONTINUE WHEN i = 5;
        RAISE INFO 'i %', i;
        EXIT simple_loop_when WHEN (i >= x);
    END LOOP;
END;
$$;

CREATE OR REPLACE PROCEDURE procedure11 (x INT)
    LANGUAGE plpgsql
AS $$
DECLARE
    i INTEGER := 0;
BEGIN
    LOOP
        i := i + 1;
		IF (I = 5) THEN
        	CONTINUE;
		END IF;
        RAISE INFO 'i %', i;
        EXIT WHEN (i >= x);
    END LOOP;
END;
$$;
```

##### Results[¶](#results)

<!-- prettier-ignore -->
|Console Output|
|---|
|1|
|2|
|3|
|4|
|6|
|7|

##### Output Code:[¶](#id243)

##### Snowflake[¶](#id244)

```
 CREATE OR REPLACE PROCEDURE procedure1 (x INT)
RETURNS VARCHAR
    LANGUAGE SQL
    COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
AS $$
    		DECLARE
    			i INTEGER := 0;
BEGIN
    			--** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
    LOOP
        i := i + 1;
        IF (:i = 5) THEN
        	CONTINUE;
        END IF;
        CALL RAISE_MESSAGE_UDF('INFO', 'i %', array_construct(:i));
        IF ((:i >= : x)) THEN
        	EXIT simple_loop_when;
        END IF;
    END LOOP simple_loop_when;
END;
$$;

CREATE OR REPLACE PROCEDURE procedure11 (x INT)
RETURNS VARCHAR
    LANGUAGE SQL
    COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
AS $$
    		DECLARE
    			i INTEGER := 0;
BEGIN
    			--** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
    LOOP
        i := i + 1;
		IF (:I = 5) THEN
        	CONTINUE;
		END IF;
        CALL RAISE_MESSAGE_UDF('INFO', 'i %', array_construct(:i));
        IF ((:i >= : x)) THEN
        	EXIT;
        END IF;
    END LOOP;
END;
$$;
```

##### Results[¶](#id245)

<!-- prettier-ignore -->
|Console Output|
|---|
|1|
|2|
|3|
|4|
|6|
|7|

### Known Issues[¶](#id246)

There are no known issues.

### Related EWIs.[¶](#id247)

There are no related EWIs.

## EXIT[¶](#exit)

### Description[¶](#id248)

> Stop the loop execution when the conditions defined in the WHEN statement are true
> ([Redshift SQL Language Reference Conditionals: EXIT](https://docs.aws.amazon.com/redshift/latest/dg/c_PLpgSQL-statements.html#r_PLpgSQL-loops)).

Warning

EXIT are partial supported by
[Snowflake](https://docs.snowflake.com/en/developer-guide/snowflake-scripting/variables#declaring-a-variable).

### Grammar Syntax[¶](#id249)

```
 EXIT [ label ] [ WHEN expression ];
```

### Sample Source Patterns[¶](#id250)

#### Input Code:[¶](#id251)

##### Redshift[¶](#id252)

```
 CREATE OR REPLACE PROCEDURE simple_loop_when(x int)
LANGUAGE plpgsql
AS $$
DECLARE i INTEGER := 0;
BEGIN
  <<simple_loop_when>>
  LOOP
    RAISE INFO 'i %', i;
    i := i + 1;
    EXIT simple_loop_when WHEN (i >= x);
  END LOOP;
END;
$$;
```

##### Output Code:[¶](#id253)

##### Redshift[¶](#id254)

```
 CREATE OR REPLACE PROCEDURE simple_loop_when (x int)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
AS $$
    DECLARE
      i INTEGER := 0;
BEGIN
      --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
  LOOP
        CALL RAISE_MESSAGE_UDF('INFO', 'i %', array_construct(:i));
    i := i + 1;
        IF ((:i >= : x)) THEN
          EXIT simple_loop_when;
        END IF;
  END LOOP simple_loop_when;
END;
$$;
```

### Known Issues[¶](#id255)

There are no known issues.

### Related EWIs.[¶](#id256)

There are no related EWIs.

## FOR[¶](#for)

### Grammar Syntax[¶](#id257)

Integer variant

```
 [<<label>>]
FOR name IN [ REVERSE ] expression .. expression LOOP
  statements
END LOOP [ label ];
```

### Sample Source Patterns[¶](#id258)

#### Input Code:[¶](#id259)

##### Redshift[¶](#id260)

```
 CREATE OR REPLACE PROCEDURE procedure1 ()
AS $$
BEGIN
  FOR i IN 1..10 LOOP
    NULL;
  END LOOP;

  FOR i IN REVERSE 10..1 LOOP
    NULL;
  END LOOP;
END;
$$ LANGUAGE plpgsql;
```

##### Output Code:[¶](#id261)

##### Redshift[¶](#id262)

```
 CREATE OR REPLACE PROCEDURE procedure1 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
AS $$
BEGIN
  FOR i IN 1 TO 10
                   --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
                   LOOP
    NULL;
  END LOOP;

  FOR i IN REVERSE 10 TO 1
                           --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
                           LOOP
    NULL;
  END LOOP;
END;
$$;
```

### Known Issues[¶](#id263)

There are no known issues.

### Related EWIs.[¶](#id264)

1. [SSC-EWI-PG0006](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/postgresqlEWI.html#ssc-ewi-pg0006):
   Reference a variable using the Label is not supported by Snowflake.

## LOOP[¶](#loop)

### Description[¶](#id265)

> A simple loop defines an unconditional loop that is repeated indefinitely until terminated by an
> EXIT or RETURN statement.
> ([Redshift SQL Language Reference Conditionals: Simple Loop](https://docs.aws.amazon.com/redshift/latest/dg/c_PLpgSQL-statements.html#r_PLpgSQL-loops)).

Warning

Simple Loop are partial supported by
[Snowflake](https://docs.snowflake.com/en/developer-guide/snowflake-scripting/variables#declaring-a-variable).

### Grammar Syntax[¶](#id266)

```
 [<<label>>]
LOOP
  statements
END LOOP [ label ];
```

### Sample Source Patterns[¶](#id267)

#### Input Code:[¶](#id268)

##### Redshift[¶](#id269)

```
 CREATE OR REPLACE PROCEDURE simple_loop()
LANGUAGE plpgsql
AS $$
BEGIN
  <<simple_while>>
  LOOP
    RAISE INFO 'I am raised once';
    EXIT simple_while;
    RAISE INFO 'I am not raised';
  END LOOP;
  RAISE INFO 'I am raised once as well';
END;
$$;
```

##### Output Code:[¶](#id270)

##### Redshift[¶](#id271)

```
 CREATE OR REPLACE PROCEDURE simple_loop ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
AS $$
BEGIN
  --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
  LOOP
    CALL RAISE_MESSAGE_UDF('INFO', 'I am raised once');
    EXIT simple_while;
    CALL RAISE_MESSAGE_UDF('INFO', 'I am not raised');
  END LOOP simple_while;
  CALL RAISE_MESSAGE_UDF('INFO', 'I am raised once as well');
END;
$$;
```

### Known Issues[¶](#id272)

There are no known issues.

### Related EWIs.[¶](#id273)

There are no related EWIs.

## WHILE[¶](#while)

### Grammar Syntax[¶](#id274)

```
 [<<label>>]
WHILE expression LOOP
  statements
END LOOP [ label ];
```

### Sample Source Patterns[¶](#id275)

#### Input Code:[¶](#id276)

##### Redshift[¶](#id277)

```
 CREATE OR REPLACE PROCEDURE simple_loop_when()
    LANGUAGE plpgsql
AS $$
DECLARE
    i INTEGER := 0;
BEGIN
    WHILE I > 5 AND I > 10 LOOP
        NULL;
    END LOOP;
END;
$$;
```

##### Output Code:[¶](#id278)

##### Redshift[¶](#id279)

```
 CREATE OR REPLACE PROCEDURE simple_loop_when ()
RETURNS VARCHAR
    LANGUAGE SQL
    COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
AS $$
            DECLARE
                i INTEGER := 0;
BEGIN
                WHILE (:I > 5 AND : I > 10)
                                            --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
                                            LOOP
        NULL;
    END LOOP;
END;
$$;
```

### Known Issues[¶](#id280)

There are no known issues.

### Related EWIs.[¶](#id281)

There are no related EWIs.

## CURSORS[¶](#cursors)

## CLOSE CURSOR[¶](#close-cursor)

### Description[¶](#id282)

> Closes all of the free resources that are associated with an open cursor..
> ([Redshift SQL Language Reference Close Cursor](https://docs.aws.amazon.com/redshift/latest/dg/close.html)).

**Note:**

This syntax is fully supported in Snowflake.

### Grammar Syntax[¶](#id283)

```
 CLOSE cursor
```

### Sample Source Patterns[¶](#id284)

#### Input Code:[¶](#id285)

##### Redshift[¶](#id286)

```
 CREATE OR REPLACE PROCEDURE cursor_test()
AS $$
BEGIN
   CLOSE cursor1;
END;
$$;
```

##### Output Code:[¶](#id287)

##### Redshift[¶](#id288)

```
 CREATE OR REPLACE PROCEDURE cursor_test ()
RETURNS VARCHAR
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/05/2025",  "domain": "test" }}'
AS $$
BEGIN
   CLOSE cursor1;
END;
$$;
```

### Known Issues[¶](#id289)

There are no known issues.

### Related EWIs.[¶](#id290)

There are no related EWIs.

## FETCH CURSOR[¶](#fetch-cursor)

### Description[¶](#id291)

> Retrieves rows using a cursor.
> ([Redshift SQL Language reference Fetch](https://docs.aws.amazon.com/redshift/latest/dg/fetch.html))

Transformation information

```
 FETCH [ NEXT | ALL | {FORWARD [ count | ALL ] } ] FROM cursor

FETCH cursor INTO target [, target ...];
```

### Sample Source Patterns[¶](#id292)

#### Setup data[¶](#id293)

##### Redshift[¶](#id294)

##### Query[¶](#id295)

```
 CREATE TABLE cursor_example
(
	col1 INTEGER,
	col2 VARCHAR(20)
);

INSERT INTO cursor_example VALUES (10, 'hello');
```

##### Snowflake[¶](#id296)

##### Query[¶](#id297)

```
 CREATE TABLE cursor_example
(
	col1 INTEGER,
	col2 VARCHAR(20)
);

INSERT INTO cursor_example VALUES (10, 'hello');
```

#### Fetch into[¶](#fetch-into)

The FETCH into statement from Redshift is fully equivalent in Snowflake

##### Redshift[¶](#id298)

##### Query[¶](#id299)

```
 CREATE OR REPLACE PROCEDURE fetch_into_example()
LANGUAGE plpgsql
AS $$
DECLARE my_cursor CURSOR FOR
        SELECT col1, col2
        FROM cursor_example;
        some_id INT;
        message VARCHAR(20);
BEGIN
    OPEN my_cursor;
    FETCH my_cursor INTO some_id, message;
    CLOSE my_cursor;
    INSERT INTO cursor_example VALUES (some_id * 10, message || ' world!');
END;
$$;

CALL fetch_into_example();

SELECT * FROM cursor_example;
```

##### Result[¶](#id300)

```
+------+-------------+
<!-- prettier-ignore -->
|col1|col2|
+------+-------------+
<!-- prettier-ignore -->
|10|hello|
|100|hello world!|
+------+-------------+
```

##### Snowflake[¶](#id301)

##### Query[¶](#id302)

```
 CREATE OR REPLACE PROCEDURE fetch_into_example ()
RETURNS VARCHAR
LANGUAGE SQL
AS $$
DECLARE
    my_cursor CURSOR FOR
    SELECT col1, col2
    FROM
    cursor_example;
    some_id INT;
    message VARCHAR(20);
BEGIN
    OPEN my_cursor;
    FETCH my_cursor INTO some_id, message;
    CLOSE my_cursor;
    INSERT INTO cursor_example
			VALUES (:some_id * 10, :message || ' world!');
END;
$$;

CALL fetch_into_example();

SELECT * FROM
	cursor_example;
```

##### Result[¶](#id303)

```
+------+-------------+
<!-- prettier-ignore -->
|col1|col2|
+------+-------------+
<!-- prettier-ignore -->
|10|hello|
|100|hello world!|
+------+-------------+
```

### Known Issues[¶](#id304)

**1. Fetch without target variables is not supported**

Snowflake requires the FETCH statement to specify the INTO clause with the variables where the
fetched row values are going to be stored. When a FETCH statement is found in the code with no INTO
clause an EWI will be generated.

Input Code:

```
 FETCH FORWARD FROM cursor1;
```

Output Code:

```
 !!!RESOLVE EWI!!! /*** SSC-EWI-PG0015 - FETCH CURSOR WITHOUT TARGET VARIABLES IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
FETCH FORWARD FROM cursor1;
```

### Known Issues[¶](#id305)

There are no known issues.

### Related EWIs[¶](#id306)

1. [SSC-EWI-PG0015](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/postgresqlEWI.html#ssc-ewi-pg0015):
   Fetch cursor without target variables is not supported in Snowflake

## OPEN CURSOR[¶](#open-cursor)

### Description[¶](#id307)

> Before you can use a cursor to retrieve rows, it must be opened.
> ([Redshift SQL Language Reference Open Cursor](https://docs.aws.amazon.com/redshift/latest/dg/c_PLpgSQL-statements.html#r_PLpgSQL-cursors)).

**Note:**

This syntax is fully supported in Snowflake.

### Grammar Syntax[¶](#id308)

```
 OPEN bound_cursor_name [ ( argument_values ) ];
```

### Sample Source Patterns[¶](#id309)

#### Setup data[¶](#id310)

##### Redshift[¶](#id311)

##### Query[¶](#id312)

```
 CREATE TABLE cursor_example
(
	col1 INTEGER,
	col2 VARCHAR(20)
);

CREATE TABLE cursor_example_results
(
	col1 INTEGER,
	col2 VARCHAR(20)
);

INSERT INTO cursor_example VALUES (10, 'hello');
```

##### Snowflake[¶](#id313)

##### Query[¶](#id314)

```
 CREATE TABLE cursor_example
(
	col1 INTEGER,
	col2 VARCHAR(20)
);

CREATE TABLE cursor_example_results
(
	col1 INTEGER,
	col2 VARCHAR(20)
);

INSERT INTO cursor_example VALUES (10, 'hello');
```

#### Open cursor without arguments[¶](#open-cursor-without-arguments)

##### Input Code:[¶](#id315)

##### Redshift[¶](#id316)

```
 CREATE OR REPLACE PROCEDURE cursor_test()
AS $$
BEGIN
   OPEN cursor1;
END;
$$;
```

##### Output Code:[¶](#id317)

##### Redshift[¶](#id318)

```
 CREATE OR REPLACE PROCEDURE cursor_test ()
RETURNS VARCHAR
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/05/2025",  "domain": "test" }}'
AS $$
BEGIN
   OPEN cursor1;
END;
$$;
```

#### Open cursor with arguments[¶](#open-cursor-with-arguments)

Cursor arguments have to be binded per each one of its uses, SnowConvert AI will generate the
bindings, was well as reorder and repeat the passed values to the OPEN statement as needed to
satisfy the bindings.

##### Redshift[¶](#id319)

##### Query[¶](#id320)

```
 CREATE OR REPLACE PROCEDURE cursor_open_test()
LANGUAGE plpgsql
AS $$
DECLARE
    cursor2 CURSOR (val1 VARCHAR(20), val2 INTEGER) FOR SELECT col1 + val2, col2 FROM cursor_example where val1 = col2 and val2 > col1;
    res1 INTEGER;
    res2 VARCHAR(20);
BEGIN
    OPEN cursor2('hello', 50);
    FETCH cursor2 INTO res1, res2;
    CLOSE cursor2;
    INSERT INTO cursor_example_results VALUES (res1, res2);
END;
$$;

call cursor_open_test();

SELECT * FROM cursor_example_results;
```

##### Result[¶](#id321)

```
+------+-------+
<!-- prettier-ignore -->
|col1|col2|
+------+-------+
<!-- prettier-ignore -->
|60|hello|
+------+-------+
```

##### Snowflake[¶](#id322)

##### Query[¶](#id323)

```
 CREATE OR REPLACE PROCEDURE cursor_open_test ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
AS $$
        DECLARE
            cursor2 CURSOR FOR SELECT col1 + ?, col2 FROM
                cursor_example
            where
                ? = col2 and ? > col1;
            res1 INTEGER;
            res2 VARCHAR(20);
BEGIN
    OPEN cursor2 USING (50, 'hello', 50);
    FETCH cursor2 INTO res1, res2;
    CLOSE cursor2;
    INSERT INTO cursor_example_results
            VALUES (:res1, : res2);
END;
$$;

call cursor_open_test();
SELECT * FROM
cursor_example_results;
```

##### Result[¶](#id324)

```
+------+-------+
<!-- prettier-ignore -->
|col1|col2|
+------+-------+
<!-- prettier-ignore -->
|60|hello|
+------+-------+
```

#### Open cursor with procedure parameters or local variables[¶](#open-cursor-with-procedure-parameters-or-local-variables)

The procedure parameters or local variables have to be binded per each one of its uses in the cursor
query, SnowConvert AI will generate the bindings and add the parameter or variable names to the OPEN
statement, even if the cursor originally had no parameters.

##### Redshift[¶](#id325)

##### Query[¶](#id326)

```
 CREATE OR REPLACE PROCEDURE cursor_open_test(someValue iNTEGER)
LANGUAGE plpgsql
AS $$
DECLARE
    charVariable VARCHAR(20) DEFAULT 'hello';
    cursor2 CURSOR FOR SELECT col1 + someValue, col2 FROM cursor_example where charVariable = col2 and someValue > col1;
    res1 INTEGER;
    res2 VARCHAR(20);
BEGIN
    OPEN cursor2;
    FETCH cursor2 INTO res1, res2;
    CLOSE cursor2;
    INSERT INTO cursor_example_results VALUES (res1, res2);
END;
$$;

call cursor_open_test(30);
```

##### Result[¶](#id327)

```
+------+-------+
<!-- prettier-ignore -->
|col1|col2|
+------+-------+
<!-- prettier-ignore -->
|40|hello|
+------+-------+
```

##### Snowflake[¶](#id328)

##### Query[¶](#id329)

```
 CREATE OR REPLACE PROCEDURE cursor_open_test (someValue iNTEGER)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
AS $$
        DECLARE
            charVariable VARCHAR(20) DEFAULT 'hello';
            cursor2 CURSOR FOR SELECT col1 + ?, col2 FROM
                cursor_example
            where
                ? = col2 and ? > col1;
            res1 INTEGER;
            res2 VARCHAR(20);
BEGIN
    OPEN cursor2 USING (someValue, charVariable, someValue);
    FETCH cursor2 INTO res1, res2;
    CLOSE cursor2;
    INSERT INTO cursor_example_results
            VALUES (:res1, : res2);
END;
$$;

call cursor_open_test(30);
```

##### Result[¶](#id330)

```
+------+-------+
<!-- prettier-ignore -->
|col1|col2|
+------+-------+
<!-- prettier-ignore -->
|40|hello|
+------+-------+
```

### Known Issues[¶](#id331)

There are no known issues.

### Related EWIs.[¶](#id332)

There are no related EWIs.

## DECLARE CURSOR[¶](#declare-cursor)

### Description[¶](#id333)

> Defines a new cursor. Use a cursor to retrieve a few rows at a time from the result set of a
> larger query.
> ([Redshift SQL Language Reference Declare Cursor](https://docs.aws.amazon.com/redshift/latest/dg/declare.html)).

**Note:**

This syntax is fully supported in Snowflake.

### Grammar Syntax[¶](#id334)

```
 name CURSOR [ ( arguments ) ] FOR query
```

### Sample Source Patterns[¶](#id335)

#### Input Code:[¶](#id336)

### Input Code:[¶](#id337)

#### Redshift[¶](#id338)

```
 CREATE OR REPLACE PROCEDURE cursor_test()
AS $$
DECLARE
   -- Declare the cursor
   cursor1 CURSOR FOR SELECT 1;
   cursor2 CURSOR (key integer) FOR SELECT 2 where 1 = key;

BEGIN
END;
$$;
```

##### Output Code:[¶](#id339)

##### Redshift[¶](#id340)

```
 CREATE OR REPLACE PROCEDURE cursor_test ()
RETURNS VARCHAR
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
AS $$
      DECLARE
         -- Declare the cursor
         cursor1 CURSOR FOR SELECT 1;
         cursor2 CURSOR FOR SELECT 2 where 1 = ?;
BEGIN
         NULL;
END;
$$;
```

### Known Issues[¶](#id341)

There are no known issues.

### Related EWIs.[¶](#id342)

There are no related EWIs.

## DECLARE REFCURSOR[¶](#declare-refcursor)

### Description[¶](#id343)

> A `refcursor` data type simply holds a reference to a cursor. You can create a cursor variable by
> declaring it as a variable of type `refcursor`
>
> ([Redshift SQL Language Reference Refcursor Declaration](https://docs.aws.amazon.com/redshift/latest/dg/c_PLpgSQL-statements.html#r_PLpgSQL-cursors))

**Note:**

Refcursor declarations are fully supported by
[Snowflake](https://docs.snowflake.com/en/developer-guide/snowflake-scripting/variables#declaring-a-variable).

### Grammar Syntax[¶](#id344)

```
 DECLARE
name refcursor;
```

Since Snowflake does not support the `REFCURSOR` data type, its functionality is replicated by
converting the `REFCURSOR` variable into a `RESULTSET` type. The query used to open the `REFCURSOR`
is assigned to the `RESULTSET` variable, after which a new cursor is created and linked to the
`RESULTSET` variable. Additionally, all references to the original `REFCURSOR` within the cursor
logic are updated to use the new cursor, thereby replicating the original functionality.

### Sample Source Patterns[¶](#id345)

#### Case: Single use[¶](#case-single-use)

##### Input Code:[¶](#id346)

##### Redshift[¶](#id347)

```
 CREATE OR REPLACE PROCEDURE VARIABLE_REFCURSOR()
LANGUAGE plpgsql
AS $$
DECLARE
  v_curs1 refcursor;
BEGIN
  OPEN v_curs1 FOR SELECT column1_name, column2_name FROM your_table;
-- Cursor logic
  CLOSE v_curs1;
 END;
$$;
```

##### Output Code:[¶](#id348)

##### Snowflake[¶](#id349)

```
 CREATE OR REPLACE PROCEDURE VARIABLE_REFCURSOR ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
AS $$
  DECLARE
   v_curs1 RESULTSET;
BEGIN
   v_curs1 := (
    SELECT column1_name, column2_name FROM your_table
   );
   LET v_curs1_Resultset_1 CURSOR
   FOR
    v_curs1;
   OPEN v_curs1_Resultset_1;
-- Cursor logic
  CLOSE v_curs1_Resultset_1;
 END;
$$;
```

##### Case: Cursor with Dynamic Sql [¶](#case-cursor-with-dynamic-sql)

##### Input Code:[¶](#id350)

##### Redshift[¶](#id351)

```
 CREATE OR REPLACE PROCEDURE VARIABLE_REFCURSOR_DYNAMIC(min_salary NUMERIC)
LANGUAGE plpgsql
AS $$
DECLARE
    cur refcursor;
    qry TEXT;
BEGIN
    qry := 'SELECT id, name FROM employees WHERE salary > ' || min_salary;

    OPEN cur FOR EXECUTE qry;
-- Cursor logic
    CLOSE cur;
END;
$$;


CREATE OR REPLACE PROCEDURE VARIABLE_REFCURSOR_DYNAMIC2(min_salary NUMERIC)
LANGUAGE plpgsql
AS $$
DECLARE
    cur refcursor;
BEGIN
    OPEN cur FOR EXECUTE 'SELECT id, name FROM employees WHERE salary > ' || min_salary;
-- Cursor logic
    CLOSE cur;
END;
$$;
```

##### Output Code:[¶](#id352)

##### Redshift[¶](#id353)

```
 CREATE OR REPLACE PROCEDURE VARIABLE_REFCURSOR_DYNAMIC (min_salary NUMERIC)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
AS $$
        DECLARE
            cur RESULTSET;
    qry TEXT;
BEGIN
    qry := 'SELECT id, name FROM employees WHERE salary > ' || min_salary;
            cur := (
                EXECUTE IMMEDIATE qry
            );
            LET cur_Resultset_1 CURSOR
            FOR
                cur;
            OPEN cur_Resultset_1;
-- Cursor logic
    CLOSE cur_Resultset_1;
END;
$$;


CREATE OR REPLACE PROCEDURE VARIABLE_REFCURSOR_DYNAMIC2 (min_salary NUMERIC)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
AS $$
        DECLARE
            cur RESULTSET;
BEGIN
            cur := (
                EXECUTE IMMEDIATE 'SELECT id, name FROM employees WHERE salary > ' || min_salary
            );
            LET cur_Resultset_2 CURSOR
            FOR
                cur;
            OPEN cur_Resultset_2;
-- Cursor logic
    CLOSE cur_Resultset_2;
END;
$$;
```

##### Case: Multiple uses: [¶](#case-multiple-uses)

##### Input Code:[¶](#id354)

##### Redshift[¶](#id355)

```
 CREATE OR REPLACE PROCEDURE VARIABLE_REFCURSOR()
LANGUAGE plpgsql
AS $$
DECLARE
  v_curs1 refcursor;
BEGIN
  OPEN v_curs1 FOR SELECT column1_name, column2_name FROM your_table;
-- Cursor logic
  CLOSE v_curs1;
  OPEN v_curs1 FOR SELECT column3_name, column4_name FROM your_table2;
-- Cursor logic
  CLOSE v_curs1;
 END;
$$;
```

##### Output Code:[¶](#id356)

##### Snowflake[¶](#id357)

```
 CREATE OR REPLACE PROCEDURE VARIABLE_REFCURSOR ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
AS $$
  DECLARE
   v_curs1 RESULTSET;
BEGIN
   v_curs1 := (
    SELECT column1_name, column2_name FROM your_table
   );
   LET v_curs1_Resultset_1 CURSOR
   FOR
    v_curs1;
   OPEN v_curs1_Resultset_1;
-- Cursor logic
  CLOSE v_curs1_Resultset_1;
   v_curs1 := (
    SELECT column3_name, column4_name FROM your_table2
   );
   LET v_curs1_Resultset_2 CURSOR
   FOR
    v_curs1;
   OPEN v_curs1_Resultset_2;
-- Cursor logic
  CLOSE v_curs1_Resultset_2;
 END;
$$;
```

### Known Issues[¶](#id358)

There are no known issues.

### Related EWIs.[¶](#id359)

There are no related EWIs.
