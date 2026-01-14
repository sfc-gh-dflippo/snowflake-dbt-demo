---
description: Oracle Create Procedure to Snowflake Snow Scripting
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/oracle/pl-sql-to-snowflake-scripting/create-procedure
title: SnowConvert AI - Oracle - CREATE PROCEDURE | Snowflake Documentation
---

## Description[¶](#description)

**Note:**

Some parts in the output code are omitted for clarity reasons.

> A procedure is a group of PL/SQL statements that you can call by name. A call specification
> (sometimes called call spec) declares a Java method or a third-generation language (3GL) routine
> so that it can be called from SQL and PL/SQL. The call spec tells Oracle Database which Java
> method to invoke when a call is made. It also tells the database what type conversions to make for
> the arguments and return value.
> [Oracle SQL Language Reference Create Procedure](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/CREATE-PROCEDURE.html#GUID-771879D8-BBFD-4D87-8A6C-290102142DA3).

For more information regarding Oracle Create Procedure, check
[here](https://docs.oracle.com/en/database/oracle/oracle-database/21/lnpls/CREATE-PROCEDURE-statement.html#GUID-5F84DB47-B5BE-4292-848F-756BF365EC54).

### Oracle Create Procedure Syntax[¶](#oracle-create-procedure-syntax)

```
CREATE [ OR REPLACE ] [ EDITIONABLE | NONEDITIONABLE ]
PROCEDURE
[ schema. ] procedure_name
[ ( parameter_declaration [, parameter_declaration ]... ) ] [ sharing_clause ]
[ ( default_collation_option | invoker_rights_clause | accessible_by_clause)... ]
{ IS | AS } { [ declare_section ]
    BEGIN statement ...
    [ EXCEPTION exception_handler [ exception_handler ]... ]
    END [ name ] ;
      |
    { java_declaration | c_declaration } } ;
```

For more information regarding Snowflake Create Procedure, check
[here](https://docs.snowflake.com/en/sql-reference/sql/create-procedure.html#create-procedure).

#### Snowflake Create Procedure Syntax[¶](#snowflake-create-procedure-syntax)

```
CREATE [ OR REPLACE ] PROCEDURE <name> ( [ <arg_name> <arg_data_type> ] [ , ... ] )
  RETURNS <result_data_type> [ NOT NULL ]
  LANGUAGE SQL
  [ { CALLED ON NULL INPUT | { RETURNS NULL ON NULL INPUT | STRICT } } ]
  [ VOLATILE | IMMUTABLE ]
  [ COMMENT = '<string_literal>' ]
  [ EXECUTE AS { CALLER | OWNER } ]
  AS '<procedure_definition>'
```

## Sample Source Patterns[¶](#sample-source-patterns)

### 1. Basic Procedure[¶](#basic-procedure)

#### Oracle[¶](#oracle)

```
CREATE OR REPLACE PROCEDURE PROC1
IS
BEGIN
null;
END;
```

##### Snow Scripting[¶](#snow-scripting)

```
CREATE OR REPLACE PROCEDURE PROC1 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
BEGIN
null;
END;
$$;
```

### 2. Procedure with Different Parameters[¶](#procedure-with-different-parameters)

#### Oracle[¶](#id1)

```
CREATE OR REPLACE PROCEDURE proc2
(
    p1 OUT INTEGER,
    p2 OUT INTEGER,
    p3 INTEGER := 1,
    p4 INTEGER DEFAULT 1
)
AS
BEGIN
	p1 := 17;
	p2 := 93;
END;
```

##### Snow Scripting[¶](#id2)

```
CREATE OR REPLACE PROCEDURE proc2
(p1 OUT INTEGER, p2 OUT INTEGER,
    p3 INTEGER DEFAULT 1,
    p4 INTEGER DEFAULT 1
)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
	BEGIN
		p1 := 17;
		p2 := 93;
	END;
$$;
```

#### Output parameters[¶](#output-parameters)

Snowflake does not allow output parameters in procedures, a way to simulate this behavior could be
to declare a variable and return its value at the end of the procedure.

#### Parameters with default values[¶](#parameters-with-default-values)

Snowflake does not allow setting default values for parameters in procedures, a way to simulate this
behavior could be to declare a variable with the default value or overload the procedure.

### 3. Procedure with Additional Settings[¶](#procedure-with-additional-settings)

#### Oracle[¶](#id3)

```
CREATE OR REPLACE PROCEDURE proc3
DEFAULT COLLATION USING_NLS_COMP
AUTHID CURRENT_USER
AS
BEGIN
NULL;
END;
```

##### Snow Scripting[¶](#id4)

```
CREATE OR REPLACE PROCEDURE proc3 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "11/14/2024",  "domain": "test" }}'
EXECUTE AS CALLER
AS
$$
BEGIN
NULL;
END;
$$;
```

### 4. Procedure with Basic Statements[¶](#procedure-with-basic-statements)

#### Oracle[¶](#id5)

```
CREATE OR REPLACE PROCEDURE proc4
(
  param1 NUMBER
)
IS
  localVar1 NUMBER;
  countRows NUMBER;
  tempSql VARCHAR(100);
  tempResult NUMBER;
  CURSOR MyCursor IS SELECT COL1 FROM Table1;

BEGIN
    localVar1 := param1;
    countRows := 0;
    tempSql := 'SELECT COUNT(*) FROM Table1 WHERE COL1 =' || localVar1;

    FOR myCursorItem IN MyCursor
        LOOP
            localVar1 := myCursorItem.Col1;
            countRows := countRows + 1;
        END LOOP;
    INSERT INTO Table2 VALUES(countRows, 'ForCursor: Total Row count is: ' || countRows);
    countRows := 0;

    OPEN MyCursor;
    LOOP
        FETCH MyCursor INTO tempResult;
        EXIT WHEN MyCursor%NOTFOUND;
        countRows := countRows + 1;
    END LOOP;
    CLOSE MyCursor;
    INSERT INTO Table2 VALUES(countRows, 'LOOP: Total Row count is: ' || countRows);

    EXECUTE IMMEDIATE tempSql INTO tempResult;
    IF tempResult > 0 THEN
        INSERT INTO Table2 (COL1, COL2) VALUES(tempResult, 'Hi, found value:' || localVar1 || ' in Table1 -- There are ' || tempResult || ' rows');
        COMMIT;
    END IF;
END proc3;
```

##### Snow Scripting[¶](#id6)

```
CREATE OR REPLACE PROCEDURE proc4
(param1 NUMBER(38, 18)
)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
  DECLARE
    localVar1 NUMBER(38, 18);
    countRows NUMBER(38, 18);
    tempSql VARCHAR(100);
    tempResult NUMBER(38, 18);
    --** SSC-PRF-0009 - PERFORMANCE REVIEW - CURSOR USAGE **
    MyCursor CURSOR
    FOR
      SELECT COL1 FROM
        Table1;
  BEGIN
    localVar1 := :param1;
    countRows := 0;
    tempSql := 'SELECT COUNT(*) FROM
   Table1
WHERE COL1 =' || NVL(:localVar1 :: STRING, '');
    OPEN MyCursor;
    --** SSC-PRF-0004 - THIS STATEMENT HAS USAGES OF CURSOR FOR LOOP **
    FOR myCursorItem IN MyCursor DO
      localVar1 := myCursorItem.Col1;
      countRows := :countRows + 1;
    END FOR;
    CLOSE MyCursor;
    INSERT INTO Table2
    VALUES(:countRows, 'ForCursor: Total Row count is: ' || NVL(:countRows :: STRING, ''));
    countRows := 0;
    OPEN MyCursor;
    --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
    LOOP
      --** SSC-PRF-0003 - FETCH INSIDE A LOOP IS CONSIDERED A COMPLEX PATTERN, THIS COULD DEGRADE SNOWFLAKE PERFORMANCE. **
        FETCH MyCursor INTO
        :tempResult;
      IF (tempResult IS NULL) THEN
        EXIT;
      END IF;
      countRows := :countRows + 1;
    END LOOP;
    CLOSE MyCursor;
    INSERT INTO Table2
    SELECT
      :countRows,
      'LOOP: Total Row count is: ' || NVL(:countRows :: STRING, '');
    !!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!

    EXECUTE IMMEDIATE :tempSql
                               !!!RESOLVE EWI!!! /*** SSC-EWI-0058 - FUNCTIONALITY FOR 'EXECUTE IMMEDIATE RETURNING CLAUSE' IS NOT CURRENTLY SUPPORTED BY SNOWFLAKE SCRIPTING ***/!!!
                               INTO tempResult;
    IF (:tempResult > 0) THEN
      INSERT INTO Table2(COL1, COL2)
      SELECT
        :tempResult,
        'Hi, found value:' || NVL(:localVar1 :: STRING, '') || ' in Table1 -- There are ' || NVL(:tempResult :: STRING, '') || ' rows';
      --** SSC-FDM-OR0012 - COMMIT REQUIRES THE APPROPRIATE SETUP TO WORK AS INTENDED **
      COMMIT;
    END IF;
  END;
$$;
```

### 5. Procedure with empty `RETURN` statements[¶](#procedure-with-empty-return-statements)

In Oracle procedures you can have empty `RETURN` statements to finish the execution of a procedure.
In Snowflake Scripting procedures can have `RETURN` statements but they must have a value. By
default all empty `RETURN` statements are converted with a `NULL` value.

#### Oracle[¶](#id7)

```
-- Procedure with empty return
CREATE OR REPLACE PROCEDURE MY_PROC
IS
BEGIN
   NULL;
   RETURN;
END;
```

##### Snowflake Scripting[¶](#snowflake-scripting)

```
-- Procedure with empty return
CREATE OR REPLACE PROCEDURE MY_PROC ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
   BEGIN
      NULL;
      RETURN NULL;
   END;
$$;
```

#### `RETURN` statements in procedures with output parameters[¶](#return-statements-in-procedures-with-output-parameters)

In procedures with output parameters, instead of a `NULL` value an `OBJECT_CONSTRUCT` will be used
in the empty `RETURN` statements to simulate the output parameters in Snowflake Scripting.

##### Oracle[¶](#id8)

```
CREATE OR REPLACE PROCEDURE PROC_WITH_OUTPUT_PARAMETERS (
    param1 OUT NUMBER,
    param2 OUT NUMBER,
    param3 NUMBER
)
IS
BEGIN
    IF param3 > 0 THEN
        param1 := 2;
        param2 := 1000;
        RETURN;
    END IF;
    param1 := 5;
    param2 := 3000;
END;
```

##### Snowflake Scripting[¶](#id9)

```
CREATE OR REPLACE PROCEDURE PROC_WITH_OUTPUT_PARAMETERS (param1 OUT NUMBER(38, 18), param2 OUT NUMBER(38, 18), param3 NUMBER(38, 18)
)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        IF (:param3 > 0) THEN
            param1 := 2;
            param2 := 1000;
            RETURN NULL;
        END IF;
        param1 := 5;
        param2 := 3000;
    END;
$$;
```

### 6. Procedure with DEFAULT parameters[¶](#procedure-with-default-parameters)

DEFAULT parameters allow named parameters to be initialized with default values if no value is
passed.

#### Oracle[¶](#id10)

```
CREATE OR REPLACE PROCEDURE TEST(
    X IN VARCHAR DEFAULT 'P',
    Y IN VARCHAR DEFAULT 'Q'
)
AS
    varX VARCHAR(32767) := NVL(X, 'P');
    varY NUMBER := NVL(Y, 1);
BEGIN
    NULL;
END TEST;

BEGIN
    TEST(Y => 'Y');
END;
```

##### Snowflake Scripting[¶](#id11)

```
CREATE OR REPLACE PROCEDURE TEST (
    X VARCHAR DEFAULT 'P',
    Y VARCHAR DEFAULT 'Q'
)
    RETURNS VARCHAR
    LANGUAGE SQL
    COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/02/2025",  "domain": "no-domain-provided" }}'
    EXECUTE AS CALLER
    AS
    $$
        DECLARE
            varX VARCHAR(32767) := NVL(:X, 'P');
            varY NUMBER(38, 18) := NVL(:Y, 1);
        BEGIN
            NULL;
        END;
    $$;

    DECLARE
        call_results VARIANT;

        BEGIN
        CALL
        TEST(Y => 'Y');
        RETURN call_results;
        END;
```

## Known Issues[¶](#known-issues)

### 1. Unsupported OUT parameters[¶](#unsupported-out-parameters)

Snowflake procedures do not have a native option for output parameters.

#### 2. Unsupported Oracle additional settings[¶](#unsupported-oracle-additional-settings)

The following Oracle settings and clauses are not supported by Snowflake procedures:

- `sharing_clause`
- `default_collation_option`
- `invoker_rights_clause`
- `accessible_by_clause`
- `java_declaration`
- `c_declaration`

## Related EWIS[¶](#related-ewis)

1. [SSC-EWI-0058](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0058):
   Functionality is not currently supported by Snowflake Scripting
2. [SSC-EWI-OR0097](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI.html#ssc-ewi-or0097):
   Procedures properties are not supported in Snowflake procedures.
3. [SSC-FDM-OR0012:](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM.html#ssc-fdm-or0012)
   COMMIT and ROLLBACK statements require adequate setup to perform as intended.
4. [SSC-PRF-0003](../../../general/technical-documentation/issues-and-troubleshooting/performance-review/generalPRF.html#ssc-prf-0003):
   Fetch inside a loop is considered a complex pattern, this could degrade Snowflake performance.
5. [SSC-PRF-0004](../../../general/technical-documentation/issues-and-troubleshooting/performance-review/generalPRF.html#ssc-prf-0004):
   This statement has usages of cursor for loop.
6. [SSC-EWI-0030](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0030):
   The statement below has usages of dynamic SQL
