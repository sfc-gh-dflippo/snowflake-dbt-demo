---
description:
  The assignment statement sets the value of a data item to a valid value. (Oracle PL/SQL Language
  Reference ASSIGNMENT Statement)
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/oracle/pl-sql-to-snowflake-scripting/README
title: SnowConvert AI - Oracle - PL/SQL to Snowflake Scripting | Snowflake Documentation
---

## ASSIGNMENT STATEMENT

### Description

> The assignment statement sets the value of a data item to a valid value.
> ([Oracle PL/SQL Language Reference ASSIGNMENT Statement](https://docs.oracle.com/en/database/oracle/oracle-database/21/lnpls/assignment-statement.html#GUID-4C3BEFDF-3FFA-4E9D-96D0-4C5E13E08643))

#### Note

Some parts in the output code are omitted for clarity reasons.

#### Oracle Assignment Syntax

```sql
assignment_statement_target := expression ;

assignment_statement_target =
{ collection_variable [ ( index ) ]
<!-- prettier-ignore -->
|cursor_variable
|:host_cursor_variable
|object[.attribute]
|out_parameter
|placeholder
|record_variable[.field]
|scalar_variable
}
```

##### Snowflake Scripting Assignment Syntax

```sql
LET `<variable_name>` `<type>` { DEFAULT | := } `<expression>` ;

LET `<variable_name>` { DEFAULT | := } `<expression>` ;
```

###### Note 2

`LET` keyword is not needed for assignment statements when the variable has been declared before.
Check
[Snowflake Assignment documentation](https://docs.snowflake.com/en/sql-reference/snowflake-scripting/let.html#let)
for more information.

### Sample Source Patterns

#### 1. Scalar Variables

##### Oracle

```sql
CREATE TABLE TASSIGN (
    COL1 NUMBER,
    COL2 NUMBER,
    COL3 VARCHAR(20),
    COL4 VARCHAR(20)
);

CREATE OR REPLACE PROCEDURE PSCALAR
AS
   var1  NUMBER := 40;
   var2  NUMBER := 22.50;
   var3  VARCHAR(20);
   var4  BOOLEAN;
   var5  NUMBER;
BEGIN
   var1 := 1;
   var2 := 2.1;
   var2 := var2 + var2;
   var3 := 'Hello World';
   var4 := true;
   var4 := var1 > 500;
   IF var4 THEN
      var5 := 0;
   ELSE
      var5 := 1;
   END IF;
  INSERT INTO TASSIGN VALUES(var1, var2, var3, var5);
END;

CALL PSCALAR();

SELECT * FROM TASSIGN;
```

##### Result

<!-- prettier-ignore -->
|COL1|COL2|COL3|COL4|
|---|---|---|---|
|1|4.2|Hello World|1|

##### Snowflake Scripting

```sql
CREATE OR REPLACE TABLE TASSIGN (
     COL1 NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/,
     COL2 NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/,
     COL3 VARCHAR(20),
     COL4 VARCHAR(20)
 )
 COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
 ;

 CREATE OR REPLACE PROCEDURE PSCALAR ()
 RETURNS VARCHAR
 LANGUAGE SQL
 COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
 EXECUTE AS CALLER
 AS
 $$
     DECLARE
     var1 NUMBER(38, 18) := 40;
     var2 NUMBER(38, 18) := 22.50;
     var3  VARCHAR(20);
     var4  BOOLEAN;
     var5 NUMBER(38, 18);
     BEGIN
     var1 := 1;
     var2 := 2.1;
     var2 := :var2 + :var2;
     var3 := 'Hello World';
     var4 := true;
     var4 := :var1 > 500;
     IF (:var4) THEN
       var5 := 0;
       ELSE
       var5 := 1;
       END IF;
       INSERT INTO TASSIGN
       VALUES(:var1, :var2, :var3, :var5);
     END;
 $$;

 CALL PSCALAR();

SELECT * FROM
     TASSIGN;
```

##### Result 2

<!-- prettier-ignore -->
|COL1|COL2|COL3|COL4|
|---|---|---|---|
|1.000000000000000000|4.000000000000000000|Hello World|1|

Warning

Transformation for some data types needs to be updated, it may cause different results. For example,
NUMBER to NUMBER rounds the value and the decimal point is lost. There is already a work item for
this issue.

#### 2. Out Parameter Assignment

To get more information about how the output parameters are being converted, please go to the
following article [Output Parameters](#output-parameters).

#### 3. Not Supported Assignments

##### Oracle 2

```sql
CREATE OR REPLACE PROCEDURE pinvalid(out_parameter   IN OUT NUMBER)
AS
record_variable       employees%ROWTYPE;

TYPE cursor_type IS REF CURSOR;
cursor1   cursor_type;
cursor2   SYS_REFCURSOR;

TYPE collection_type IS TABLE OF NUMBER INDEX BY VARCHAR(64);
collection_variable     collection_type;

BEGIN
--Record Example
  record_variable.last_name := 'Ortiz';

--Cursor Example
  cursor1 := cursor2;

--Collection
  collection_variable('Test') := 5;

--Out Parameter
  out_parameter := 123;
END;
```

##### Snowflake Scripting 2

```sql
--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "employees" **
CREATE OR REPLACE PROCEDURE pinvalid (out_parameter OUT NUMBER(38, 18))
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
  DECLARE
    record_variable OBJECT !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - ROWTYPE DATA TYPE CONVERTED TO OBJECT ***/!!! := OBJECT_CONSTRUCT();
--    !!!RESOLVE EWI!!! /*** SSC-EWI-0058 - FUNCTIONALITY FOR 'PL REF CURSOR TYPE DEFINITION' IS NOT CURRENTLY SUPPORTED BY SNOWFLAKE SCRIPTING ***/!!!

--    TYPE cursor_type IS REF CURSOR;
    cursor1_res RESULTSET;
    cursor2_res RESULTSET;
--    !!!RESOLVE EWI!!! /*** SSC-EWI-0058 - FUNCTIONALITY FOR 'PL COLLECTION TYPE DEFINITION' IS NOT CURRENTLY SUPPORTED BY SNOWFLAKE SCRIPTING ***/!!!

--    TYPE collection_type IS TABLE OF NUMBER INDEX BY VARCHAR(64);
    collection_variable VARIANT !!!RESOLVE EWI!!! /*** SSC-EWI-0062 - CUSTOM TYPE 'collection_type' USAGE CHANGED TO VARIANT ***/!!!;
  BEGIN
    --Record Example
    record_variable := OBJECT_INSERT(record_variable, 'LAST_NAME', 'Ortiz', true);

    --Cursor Example
    !!!RESOLVE EWI!!! /*** SSC-EWI-OR0108 - THE FOLLOWING ASSIGNMENT STATEMENT IS NOT SUPPORTED BY SNOWFLAKE SCRIPTING ***/!!!
      cursor1 := :cursor2;

    --Collection
    !!!RESOLVE EWI!!! /*** SSC-EWI-OR0108 - THE FOLLOWING ASSIGNMENT STATEMENT IS NOT SUPPORTED BY SNOWFLAKE SCRIPTING ***/!!!
      collection_variable('Test') := 5;
    --Out Parameter
    out_parameter := 123;
  END;
$$;
```

### Known Issues

#### 1. Several Unsupported Assignment Statements

Currently, transformation for cursor, collection, record, and user-defined type variables are not
supported by Snow Scripting. Therefore assignment statements using these variables are commented and
marked as not supported. Changing these variables to Snowflake
[semi-structured data types](https://docs.snowflake.com/en/sql-reference/data-types-semistructured.html#semi-structured-data-types)
could help as a workaround in some scenarios.

### Related EWIs

1. [SSC-EWI-0036](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0036):
   Data type converted to another data type.
2. [SSC-EWI-0058](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0058):
   Functionality is not currently supported by Snowflake Scripting.
3. [SSC-EWI-0062](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0062):
   Custom type usage changed to variant.
4. [SSC-EWI-OR0108](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI#ssc-ewi-or0108):
   The Following Assignment Statement is Not Supported by Snowflake Scripting.
5. [SSC-FDM-0006](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0006):
   Number type column may not behave similarly in Snowflake.
6. [SSC-FDM-0007](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0007):
   Element with missing dependencies.

## CALL

### Description 2

There are two types of call statements in Oracle:

#### 1-CALL Statement

> Use the `CALL` statement to execute a routine (a standalone procedure or function, or a procedure
> or function defined within a type or package) from within SQL.
> ([Oracle SQL Language Reference CALL](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/CALL.html#GUID-6CD7B9C4-E5DC-4F3C-9B6A-876AD2C63545))

#### 2-Call Specification

> A call specification declares a Java method or a C language subprogram so that it can be invoked
> from PL/SQL.
> ([Oracle SQL Language Reference Call Specification](https://docs.oracle.com/en/database/oracle/oracle-database/21/lnpls/call-specification.html#GUID-C5F117AE-E9A2-499B-BA6A-35D072575BAD))

The CALL Specification is not supported in snowflake scripting since this is part of the development
libraries for C and JAVA, not a SQL statement, therefore this statement is not transformed.

### Known Issues 2

No issues were found.

### Related EWIs 2

No related EWIs.

## CASE

Translation reference for CASE statements

### Description 3

> The `CASE` statement chooses from a sequence of conditions and runs a corresponding statement. For
> more information regarding Oracle CASE, check
> [here](https://docs.oracle.com/en/database/oracle/oracle-database/21/lnpls/CASE-statement.html#GUID-F4251A23-0284-4990-A156-00A92F83BC35).

#### Note 3

Some parts in the output code are omitted for clarity reasons.

#### Simple case

##### Oracle CASE Syntax

```sql
[ <`<label>`> ] CASE case_operand
  WHEN boolean_expression THEN statement ;
  [ WHEN boolean_expression THEN statement ; ]...
  [ ELSE statement [ statement ]... ;
END CASE [ label ] ;
```

##### Snowflake Scripting CASE Syntax

```sql
CASE ( `<expression_to_match>` )
    WHEN `<expression>` THEN
        `<statement>`;
        [ `<statement>`; ... ]
    [ WHEN ... ]
    [ ELSE
        `<statement>`;
        [ `<statement>`; ... ]
    ]
END [ CASE ] ;
```

#### Searched case

##### Oracle CASE Syntax 2

```sql
[ <`<label>`> ] CASE
  WHEN boolean_expression THEN statement ;
  [ WHEN boolean_expression THEN statement ; ]...
  [ ELSE statement [ statement ]... ;
END CASE [ label ];
```

##### Snowflake Scripting CASE Syntax 2

```sql
CASE
    WHEN `<boolean_expression>` THEN
        `<statement>`;
        [ `<statement>`; ... ]
    [ WHEN ... ]
    [ ELSE
        `<statement>`;
        [ `<statement>`; ... ]
    ]
END [ CASE ] ;
```

### Sample Source Patterns 2

#### Sample auxiliar table

##### Oracle 3

```sql
CREATE TABLE case_table(col varchar(30));
```

##### Snowflake

```sql
CREATE OR REPLACE TABLE case_table (col varchar(30))
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;
```

#### Simple Case 2

##### Oracle 4

```sql
CREATE OR REPLACE PROCEDURE caseExample1 ( grade NUMBER )
IS
RESULT VARCHAR(20);
BEGIN
   <`<CASE1>`>
   CASE grade
    WHEN 10 THEN RESULT:='Excellent';
    WHEN 9 THEN RESULT:='Very Good';
    WHEN 8 THEN RESULT:='Good';
    WHEN 7 THEN RESULT:='Fair';
    WHEN 6 THEN RESULT:='Poor';
    ELSE RESULT:='No such grade';
  END CASE CASE1;
  INSERT INTO CASE_TABLE(COL) VALUES (RESULT);
END;

CALL caseExample1(6);

CALL caseExample1(4);

CALL caseExample1(10);

SELECT * FROM CASE_TABLE;
```

##### Result 3

<!-- prettier-ignore -->
|COL|
|---|
|Poor|
|No such grade|
|Excellent|

##### Snowflake Scripting 3

```sql
CREATE OR REPLACE PROCEDURE caseExample1 (grade NUMBER(38, 18))
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
  DECLARE
    RESULT VARCHAR(20);
  BEGIN
    !!!RESOLVE EWI!!! /*** SSC-EWI-0094 - LABEL DECLARATION FOR A STATEMENT IS NOT SUPPORTED BY SNOWFLAKE SCRIPTING <`<CASE1>`> ***/!!!
    CASE :grade
      WHEN 10 THEN
        RESULT := 'Excellent';
      WHEN 9 THEN
        RESULT := 'Very Good';
      WHEN 8 THEN
        RESULT := 'Good';
      WHEN 7 THEN
        RESULT := 'Fair';
      WHEN 6 THEN
        RESULT := 'Poor';
        ELSE
        RESULT := 'No such grade';
    END CASE;
    INSERT INTO CASE_TABLE(COL) VALUES (:RESULT);
  END;
$$;

CALL caseExample1(6);

CALL caseExample1(4);

CALL caseExample1(10);

--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "CASE_TABLE" **

SELECT * FROM
  CASE_TABLE;
```

##### Result 4

<!-- prettier-ignore -->
|COL|
|---|
|Poor|
|No such grade|
|Excellent|

#### Searched Case 2

##### Oracle 5

```sql
CREATE OR REPLACE PROCEDURE caseExample2 ( grade NUMBER )
IS
RESULT VARCHAR(20);
BEGIN
    <`<CASE1>`>
    CASE
     WHEN grade = 10 THEN RESULT:='Excellent';
     WHEN grade = 9 THEN RESULT:='Very Good';
     WHEN grade = 8 THEN RESULT:='Good';
     WHEN grade = 7 THEN RESULT:='Fair';
     WHEN grade = 6 THEN RESULT:='Poor';
     ELSE RESULT:='No such grade';
  END CASE CASE1;
  INSERT INTO CASE_TABLE(COL) VALUES (RESULT);
END;

CALL caseExample2(6);
CALL caseExample2(4);
CALL caseExample2(10);
SELECT * FROM CASE_TABLE;
```

##### Result 5

<!-- prettier-ignore -->
|COL|
|---|
|Poor|
|No such grade|
|Excellent|

##### Snowflake Scripting 4

```sql
CREATE OR REPLACE PROCEDURE caseExample2 (grade NUMBER(38, 18))
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
  DECLARE
    RESULT VARCHAR(20);
  BEGIN
    !!!RESOLVE EWI!!! /*** SSC-EWI-0094 - LABEL DECLARATION FOR A STATEMENT IS NOT SUPPORTED BY SNOWFLAKE SCRIPTING <`<CASE1>`> ***/!!!
    CASE
      WHEN :grade = 10 THEN
        RESULT := 'Excellent';
      WHEN :grade = 9 THEN
        RESULT := 'Very Good';
      WHEN :grade = 8 THEN
        RESULT := 'Good';
      WHEN :grade = 7 THEN
        RESULT := 'Fair';
      WHEN :grade = 6 THEN
        RESULT := 'Poor';
        ELSE
        RESULT := 'No such grade';
    END CASE;
    INSERT INTO CASE_TABLE(COL) VALUES (:RESULT);
  END;
$$;

CALL caseExample2(6);

CALL caseExample2(4);

CALL caseExample2(10);

--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "CASE_TABLE" **
SELECT * FROM
  CASE_TABLE;
```

##### Result 6

<!-- prettier-ignore -->
|COL|
|---|
|Poor|
|No such grade|
|Excellent|

### Known issues 3

#### 1. Labels are not supported in Snowflake Scripting CASE syntax

The labels are commented out or removed depending on their position.

### Related EWIS 3

1. [SSC-EWI-0094](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0094):
   Label declaration not supported.
2. [SSC-FDM-0007](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0007):
   Element with missing dependencies.

## COMPOUND STATEMENTS

This section is a translation specification for the compound statements

Warning

This section is a work in progress, information may change in the future.

### Note 4

Some parts in the output code are omitted for clarity reasons.

### General description

> The basic unit of a PL/SQL source program is the block, which groups related declarations and
> statements.
>
> A PL/SQL block is defined by the keywords DECLARE, BEGIN, EXCEPTION, and END. These keywords
> divide the block into a declarative part, an executable part, and an exception-handling part. Only
> the executable part is required.
> ([PL/SQL Anonymous Blocks](https://livesql.oracle.com/apex/livesql/file/tutorial_KS0KNKP218J86THKN85XU37.html))

The **`BEGIN...END`** block in Oracle can have the following characteristics:

1. Be nested.
2. Contain the DECLARE statement for variables.
3. Group multiple SQL or PL/SQL statements.

#### Oracle syntax

```sql
[DECLARE <Variable declaration>]
BEGIN
  <Executable statements>
[EXCEPTION <Exception handler>]
END
```

#### Snowflake syntax

```sql
BEGIN
    `<statement>`;
    [ `<statement>`; ... ]
[ EXCEPTION `<exception_handler>` ]
END;
```

##### Note 5

In Snowflake, a BEGIN/END block can be the top-level construct inside an anonymous block
([Snowflake documentation](https://docs.snowflake.com/en/sql-reference/snowflake-scripting/begin#usage-notes)).

### Sample Source Patterns 3

#### 1. IF-ELSE block

Review the following documentation about IF statements to learn more:
[SnowConvert AI IF statements translation](#if) and
[Snowflake IF statement documentation](https://docs.snowflake.com/en/sql-reference/snowflake-scripting/if)

##### Oracle 6

```sql
DECLARE
    age NUMBER := 18;
BEGIN
    IF age >= 18 THEN
        DBMS_OUTPUT.PUT_LINE('You are an adult.');
    ELSE
        DBMS_OUTPUT.PUT_LINE('You are a minor.');
    END IF;
END;
```

##### Result 7

```sql
Statement processed.
You are an adult.
```

##### Snowflake 2

Warning

When calling a procedure or user-defined function (UDF), generating code is needed to support the
equivalence as `call_results` variable. In this case, is used to print the information.

Review the user-defined function (UDF) used [here](../built-in-packages.html#put-line-procedure).

```sql
DECLARE
    age NUMBER(38, 18) := 18;
    call_results VARIANT;
BEGIN
    IF (:age >= 18) THEN
        --** SSC-FDM-OR0035 - CHECK UDF IMPLEMENTATION FOR DBMS_OUTPUT.PUT_LINE_UDF. **
        call_results := (
            CALL DBMS_OUTPUT.PUT_LINE_UDF('You are an adult.')
        );
    ELSE
        --** SSC-FDM-OR0035 - CHECK UDF IMPLEMENTATION FOR DBMS_OUTPUT.PUT_LINE_UDF. **
        call_results := (
            CALL DBMS_OUTPUT.PUT_LINE_UDF('You are a minor.')
        );
    END IF;
    RETURN call_results;
END;
```

##### Result 8

```sql
anonymous block
You are an adult.
```

#### 2. CASE statement

For more information, review the following documentation:
[SnowConvert AI CASE statement documentation](#case) and
[Snowflake CASE documentation](https://docs.snowflake.com/en/sql-reference/snowflake-scripting/case)

##### Oracle 7

```sql
BEGIN
   DECLARE
      day_of_week NUMBER := 3;
   BEGIN
      CASE day_of_week
         WHEN 1 THEN DBMS_OUTPUT.PUT_LINE('Sunday');
         WHEN 2 THEN DBMS_OUTPUT.PUT_LINE('Monday');
         WHEN 3 THEN DBMS_OUTPUT.PUT_LINE('Tuesday');
         WHEN 4 THEN DBMS_OUTPUT.PUT_LINE('Wednesday');
         WHEN 5 THEN DBMS_OUTPUT.PUT_LINE('Thursday');
         WHEN 6 THEN DBMS_OUTPUT.PUT_LINE('Friday');
         WHEN 7 THEN DBMS_OUTPUT.PUT_LINE('Saturday');
         ELSE DBMS_OUTPUT.PUT_LINE('Invalid day');
      END CASE;
   END;
END;
```

##### Result 9

```sql
Statement processed.
Tuesday
```

##### Snowflake 3

Warning

When calling a procedure or user-defined function (UDF), generating code is needed to support the
equivalence as `call_results` variable. In this case, is used to print the information.

Review the user-defined function (UDF) used [here](../built-in-packages.html#put-line-procedure).

```sql
DECLARE
   call_results VARIANT;
BEGIN
   DECLARE
      day_of_week NUMBER(38, 18) := 3;
   BEGIN
      CASE :day_of_week
         WHEN 1 THEN
            --** SSC-FDM-OR0035 - CHECK UDF IMPLEMENTATION FOR DBMS_OUTPUT.PUT_LINE_UDF. **
            call_results := (
               CALL DBMS_OUTPUT.PUT_LINE_UDF('Sunday')
            );
         WHEN 2 THEN
            --** SSC-FDM-OR0035 - CHECK UDF IMPLEMENTATION FOR DBMS_OUTPUT.PUT_LINE_UDF. **
            call_results := (
               CALL DBMS_OUTPUT.PUT_LINE_UDF('Monday')
            );
         WHEN 3 THEN
            --** SSC-FDM-OR0035 - CHECK UDF IMPLEMENTATION FOR DBMS_OUTPUT.PUT_LINE_UDF. **
            call_results := (
               CALL DBMS_OUTPUT.PUT_LINE_UDF('Tuesday')
            );
         WHEN 4 THEN
            --** SSC-FDM-OR0035 - CHECK UDF IMPLEMENTATION FOR DBMS_OUTPUT.PUT_LINE_UDF. **
            call_results := (
               CALL DBMS_OUTPUT.PUT_LINE_UDF('Wednesday')
            );
         WHEN 5 THEN
            --** SSC-FDM-OR0035 - CHECK UDF IMPLEMENTATION FOR DBMS_OUTPUT.PUT_LINE_UDF. **
            call_results := (
               CALL DBMS_OUTPUT.PUT_LINE_UDF('Thursday')
            );
         WHEN 6 THEN
            --** SSC-FDM-OR0035 - CHECK UDF IMPLEMENTATION FOR DBMS_OUTPUT.PUT_LINE_UDF. **
            call_results := (
               CALL DBMS_OUTPUT.PUT_LINE_UDF('Friday')
            );
         WHEN 7 THEN
            --** SSC-FDM-OR0035 - CHECK UDF IMPLEMENTATION FOR DBMS_OUTPUT.PUT_LINE_UDF. **
            call_results := (
               CALL DBMS_OUTPUT.PUT_LINE_UDF('Saturday')
            );
         ELSE
            --** SSC-FDM-OR0035 - CHECK UDF IMPLEMENTATION FOR DBMS_OUTPUT.PUT_LINE_UDF. **
            call_results := (
               CALL DBMS_OUTPUT.PUT_LINE_UDF('Invalid day')
            );
      END CASE;
   END;
   RETURN call_results;
END;
```

##### Result 10

```sql
anonymous block
Tuesday
```

#### 3. LOOP statements

For more information review the following documentation: [SnowConvert AI FOR LOOP](#for-loop) and
Snowflake [LOOP documentation](https://docs.snowflake.com/en/sql-reference/snowflake-scripting/loop)
and [FOR documentation](https://docs.snowflake.com/en/sql-reference/snowflake-scripting/for).

##### Oracle 8

```sql
BEGIN
    FOR i IN 1..10 LOOP
        NULL;
    END LOOP;
END;
```

##### Result 11

```sql
Statement processed.
```

##### Snowflake 4

##### First Tab

```sql
BEGIN
        --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
        FOR i IN 1 TO 10
                         --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
                         LOOP
                                    NULL;
                                END LOOP;
END;
```

##### Result 12

```sql
anonymous block
```

#### 4. Procedure call and OUTPUT parameters

Anonymous block in Oracle may have calls to procedures. Furthermore, the following documentation may
be useful: [SnowConvert AI Procedure documentation](create-procedure).

The following example uses the OUT parameters, the information about the current transformation can
be found here: [SnowConvert AI OUTPUT Parameters](#output-parameters)

##### Oracle 9

```sql
-- Procedure declaration
CREATE OR REPLACE PROCEDURE calculate_sum(
    p_num1 IN NUMBER,
    p_num2 IN NUMBER,
    p_result OUT NUMBER
)
IS
BEGIN
    -- Calculate the sum of the two numbers
    p_result := p_num1 + p_num2;
END;
/

-- Anonymous block with a procedure call
DECLARE
    -- Declare variables to hold the input and output values
    v_num1 NUMBER := 10;
    v_num2 NUMBER := 20;
    v_result NUMBER;
BEGIN
    -- Call the procedure with the input values and get the result
    calculate_sum(v_num1, v_num2, v_result);

    -- Display the result
    DBMS_OUTPUT.PUT_LINE('The sum of ' || v_num1 || ' and ' || v_num2 || ' is ' || v_result);
END;
/
```

##### Result 13

```sql
Statement processed.
The sum of 10 and 20 is 30
```

##### Snowflake 5

```sql
-- Procedure declaration
CREATE OR REPLACE PROCEDURE calculate_sum (p_num1 NUMBER(38, 18), p_num2 NUMBER(38, 18), p_result OUT NUMBER(38, 18)
)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
    BEGIN
    -- Calculate the sum of the two numbers
        p_result := :p_num1 + :p_num2;
    END;
$$;

-- Anonymous block with a procedure call
DECLARE
    -- Declare variables to hold the input and output values
    v_num1 NUMBER(38, 18) := 10;
    v_num2 NUMBER(38, 18) := 20;
    v_result NUMBER(38, 18);
    call_results VARIANT;
BEGIN
    CALL
    -- Call the procedure with the input values and get the result
    calculate_sum(:v_num1, :v_num2, :v_result);

    -- Display the result
    --** SSC-FDM-OR0035 - CHECK UDF IMPLEMENTATION FOR DBMS_OUTPUT.PUT_LINE_UDF. **
    call_results := (
        CALL DBMS_OUTPUT.PUT_LINE_UDF('The sum of ' || NVL(:v_num1 :: STRING, '') || ' and ' || NVL(:v_num2 :: STRING, '') || ' is ' || NVL(:v_result :: STRING, ''))
    );
    RETURN call_results;
END;
```

##### Result 14

```sql
anonymous block
The sum of 10 and 20 is 30
```

#### 5. Alter session

For more information, review the following documentation:
[Alter session documentation](../sql-translation-reference/README.html#alter-session).

Notice that in Oracle, the block `BEGIN...END` should use the `EXECUTE IMMEDIATE` statement to run
`alter session` statements.

##### Oracle 10

```sql
DECLARE
     lv_sql_txt VARCHAR2(200);
BEGIN
     lv_sql_txt := 'ALTER SESSION SET nls_date_format = ''DD-MM-YYYY''';
     EXECUTE IMMEDIATE lv_sql_txt;
END;
```

##### Result 15

```sql
Statement processed.
Done
```

##### Snowflake 6

```sql
DECLARE
     lv_sql_txt VARCHAR(200);
BEGIN
     lv_sql_txt := 'ALTER SESSION SET nls_date_format = ''DD-MM-YYYY''';
     !!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!!!!RESOLVE EWI!!! /*** SSC-EWI-0027 - THE FOLLOWING STATEMENT USES A VARIABLE/LITERAL WITH AN INVALID QUERY AND IT WILL NOT BE EXECUTED ***/!!!
     EXECUTE IMMEDIATE :lv_sql_txt;
END;
```

##### Result 16

```sql
anonymous block
Done
```

#### 6. Cursors

The following example displays the usage of a `cursor` inside a `BEGIN...END` block. Review the
following documentation to learn more: [Cursor documentation](cursor).

##### Oracle 11

```sql
CREATE TABLE employee (
    ID_Number NUMBER,
    emp_Name VARCHAR(200),
    emp_Phone NUMBER
);

INSERT INTO employee VALUES (1, 'NameA NameZ', 1234567890);
INSERT INTO employee VALUES (2, 'NameB NameY', 1234567890);

DECLARE
    var1 VARCHAR(20);
    CURSOR cursor1 IS SELECT emp_Name FROM employee ORDER BY ID_Number;
BEGIN
    OPEN cursor1;
    FETCH cursor1 INTO var1;
    CLOSE cursor1;
 DBMS_OUTPUT.PUT_LINE(var1);
END;
```

##### Result 17

```sql
Statement processed.
NameA NameZ
```

##### Snowflake 7

Warning

When calling a procedure or user-defined function (UDF), generating code is needed to support the
equivalence as `call_results` variable. In this case, is used to print the information.

Review the user-defined function (UDF) used [here](../built-in-packages.html#put-line-procedure).

```sql
CREATE OR REPLACE TABLE employee (
    ID_Number NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/,
    emp_Name VARCHAR(200),
    emp_Phone NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
;

INSERT INTO employee
VALUES (1, 'NameA NameZ', 1234567890);

INSERT INTO employee
VALUES (2, 'NameB NameY', 1234567890);

DECLARE
    var1 VARCHAR(20);
    --** SSC-PRF-0009 - PERFORMANCE REVIEW - CURSOR USAGE **
    cursor1 CURSOR
    FOR
  SELECT emp_Name FROM
   employee
  ORDER BY ID_Number;
    call_results VARIANT;
BEGIN
    OPEN cursor1;
    FETCH cursor1 INTO
  :var1;
    CLOSE cursor1;
    --** SSC-FDM-OR0035 - CHECK UDF IMPLEMENTATION FOR DBMS_OUTPUT.PUT_LINE_UDF. **
    call_results := (
  CALL DBMS_OUTPUT.PUT_LINE_UDF(:var1)
    );
    RETURN call_results;
END;
```

##### Result 18

```sql
anonymous block
NameA NameZ
```

#### 7. Select statements

For more information review the following documentation:
[Select documentation](../sql-queries-and-subqueries/selects).

##### Oracle 12

```sql
CREATE TABLE employee (
    ID_Number NUMBER,
    emp_Name VARCHAR(200),
    emp_Phone NUMBER
);

INSERT INTO employee VALUES (1, 'NameA NameZ', 1234567890);
INSERT INTO employee VALUES (2, 'NameB NameY', 1234567890);

DECLARE
    var_Result NUMBER;
BEGIN
    SELECT COUNT(*) INTO var_Result FROM employee;
    DBMS_OUTPUT.PUT_LINE(var_Result);
END;
```

##### Result 19

```sql
Statement processed.
2
```

##### Snowflake 8

Warning

When calling a procedure or user-defined function (UDF), generating code is needed to support the
equivalence as `call_results` variable. In this case, is used to print the information.

Review the user-defined function (UDF) used [here](../built-in-packages.html#put-line-procedure).

```sql
CREATE OR REPLACE TABLE employee (
       ID_Number NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/,
       emp_Name VARCHAR(200),
       emp_Phone NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/
   )
   COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
   ;

   INSERT INTO employee
   VALUES (1, 'NameA NameZ', 1234567890);

   INSERT INTO employee
   VALUES (2, 'NameB NameY', 1234567890);

   DECLARE
    var_Result NUMBER(38, 18);
       call_results VARIANT;
   BEGIN
       SELECT COUNT(*) INTO
           :var_Result
       FROM
           employee;
       --** SSC-FDM-OR0035 - CHECK UDF IMPLEMENTATION FOR DBMS_OUTPUT.PUT_LINE_UDF. **
       call_results := (
           CALL DBMS_OUTPUT.PUT_LINE_UDF(:var_Result)
       );
       RETURN call_results;
   END;
```

##### Result 20

```sql
anonymous block
2
```

#### 8. Join Statements

For more information review the following documentation:
[Joins documentation](../sql-queries-and-subqueries/joins).

##### Oracle 13

```sql
CREATE TABLE t1 (col1 INTEGER);
CREATE TABLE t2 (col1 INTEGER);

INSERT INTO t1 (col1) VALUES (2);
INSERT INTO t1 (col1) VALUES (3);
INSERT INTO t1 (col1) VALUES (4);

INSERT INTO t2 (col1) VALUES (1);
INSERT INTO t2 (col1) VALUES (2);
INSERT INTO t2 (col1) VALUES (2);
INSERT INTO t2 (col1) VALUES (3);

DECLARE
    total_price FLOAT;
    CURSOR cursor1 IS SELECT t1.col1 as FirstTable, t2.col1 as SecondTable
    FROM t1 INNER JOIN t2
        ON t2.col1 = t1.col1
    ORDER BY 1,2;
BEGIN
    total_price := 0.0;
    FOR rec IN cursor1 LOOP
      total_price := total_price + rec.FirstTable;
    END LOOP;
    DBMS_OUTPUT.PUT_LINE(total_price);
END;
```

##### Result 21

```sql
Statement processed.
7
```

##### Snowflake 9

Warning

When calling a procedure or user-defined function (UDF), generating code is needed to support the
equivalence as `call_results` variable. In this case, is used to print the information.

Review the user-defined function (UDF) used [here](../built-in-packages.html#put-line-procedure).

```sql
CREATE OR REPLACE TABLE t1 (col1 INTEGER)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
;

CREATE OR REPLACE TABLE t2 (col1 INTEGER)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
;

INSERT INTO t1(col1) VALUES (2);

INSERT INTO t1(col1) VALUES (3);

INSERT INTO t1(col1) VALUES (4);

INSERT INTO t2(col1) VALUES (1);

INSERT INTO t2(col1) VALUES (2);

INSERT INTO t2(col1) VALUES (2);

INSERT INTO t2(col1) VALUES (3);

DECLARE
    total_price FLOAT;
    --** SSC-PRF-0009 - PERFORMANCE REVIEW - CURSOR USAGE **
    cursor1 CURSOR
    FOR
        SELECT t1.col1 as FIRSTTABLE, t2.col1 as SECONDTABLE
           FROM
            t1
            INNER JOIN
                t2
               ON t2.col1 = t1.col1
           ORDER BY 1,2;
    call_results VARIANT;
BEGIN
    total_price := 0.0;
    OPEN cursor1;
    --** SSC-PRF-0004 - THIS STATEMENT HAS USAGES OF CURSOR FOR LOOP **
    FOR rec IN cursor1 DO
        total_price :=
        !!!RESOLVE EWI!!! /*** SSC-EWI-OR0036 - TYPES RESOLUTION ISSUES, ARITHMETIC OPERATION '+' MAY NOT BEHAVE CORRECTLY BETWEEN FLOAT AND unknown ***/!!!
        :total_price + rec.FIRSTTABLE;
    END FOR;
    CLOSE cursor1;
    --** SSC-FDM-OR0035 - CHECK UDF IMPLEMENTATION FOR DBMS_OUTPUT.PUT_LINE_UDF. **
    call_results := (
        CALL DBMS_OUTPUT.PUT_LINE_UDF(:total_price)
    );
    RETURN call_results;
END;
```

#### 9. Exception handling

##### Oracle 14

```sql
DECLARE
      v_result NUMBER;
BEGIN
   v_result := 1 / 0;
   EXCEPTION
      WHEN ZERO_DIVIDE THEN
         DBMS_OUTPUT.PUT_LINE( SQLERRM );
END;
```

##### Result 22

```sql
Statement processed.
ORA-01476: divisor is equal to zero
```

##### Snowflake 10

Warning

`ZERO_DIVIDE` exception in Snowflake is not supported.

```sql
DECLARE
      v_result NUMBER(38, 18);
      error_results VARIANT;
BEGIN
      v_result := 1 / 0;
   EXCEPTION
      WHEN ZERO_DIVIDE THEN
      --** SSC-FDM-OR0035 - CHECK UDF IMPLEMENTATION FOR DBMS_OUTPUT.PUT_LINE_UDF. **
      error_results := (
         CALL DBMS_OUTPUT.PUT_LINE_UDF( SQLERRM )
      );
      RETURN error_results;
END;
```

##### Result 23

```sql
anonymous block
Division by zero
```

### Known issues 4

1. Unsupported GOTO statements in Oracle.
2. Exceptions that use GOTO statements may be affected too.
3. Cursor functionality may be adapted under current restrictions on translations.

### Related EWIs 4

1. [SSC-EWI-0027](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0027):The
   following statement uses a variable/literal with an invalid query and it will not be executed.
2. [SSC-EWI-OR0036](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI#ssc-ewi-or0036):
   Types resolution issues, the arithmetic operation may not behave correctly between string and
   date.
3. [SSC-FDM-OR0035](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM#ssc-fdm-or0035):
   DBMS_OUTPUT.PUTLINE check UDF implementation.
4. [SSC-FDM-0006](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0006):
   Number type column may not behave similarly in Snowflake.
5. [SSC-PRF-0004](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/performance-review/generalPRF#ssc-prf-0004):
   This statement has usages of cursor for loop.
6. [SSC-EWI-0030](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0030):
   The statement below has usages of dynamic SQL

## CONTINUE

Translation reference to convert Oracle CONTINUE statement to Snowflake Scripting

### Description 4

> The `CONTINUE` statement exits the current iteration of a loop, either conditionally or
> unconditionally, and transfers control to the next iteration of either the current loop or an
> enclosing labeled loop.
> ([Oracle PL/SQL Language Reference CONTINUE Statement](https://docs.oracle.com/en/database/oracle/oracle-database/21/lnpls/CONTINUE-statement.html#GUID-3ED7E5D5-E2D0-42D1-8A7F-97FFC7372775))

#### Note 6

Some parts in the output code are omitted for clarity reasons.

#### Oracle CONTINUE Syntax

```sql
CONTINUE [ label ] [ WHEN boolean_expression ] ;
```

##### Snowflake Scripting CONTINUE Syntax

```sql
{ CONTINUE | ITERATE } [ `<label>` ] ;
```

### Sample Source Patterns 4

#### 1. Simple Continue

Code skips the `INSERT` statement by using `CONTINUE`.

##### Note 7

This case is functionally equivalent.

##### Oracle 15

```sql
CREATE TABLE continue_testing_table_1 (iterator VARCHAR2(5));

CREATE OR REPLACE PROCEDURE continue_procedure_1
IS
I NUMBER := 0;
J NUMBER := 20;
BEGIN
    WHILE I <= J LOOP
        I := I + 1;
        CONTINUE;
        INSERT INTO continue_testing_table_1
        VALUES (TO_CHAR(I));
    END LOOP;
END;

CALL continue_procedure_1();
SELECT * FROM continue_testing_table_1;
```

##### Result 24

<!-- prettier-ignore -->
|ITERATOR|
|---|

##### Snowflake Scripting 5

```sql
CREATE OR REPLACE TABLE continue_testing_table_1 (iterator VARCHAR(5))
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

CREATE OR REPLACE PROCEDURE continue_procedure_1 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        I NUMBER(38, 18) := 0;
        J NUMBER(38, 18) := 20;
    BEGIN
        WHILE (:I <= :J)
                         --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
                         LOOP
                             I := :I + 1;
                             CONTINUE;
                                    INSERT INTO continue_testing_table_1
                                    VALUES (TO_CHAR(:I));
                                END LOOP;
    END;
$$;

CALL continue_procedure_1();

SELECT * FROM
    continue_testing_table_1;
```

##### Result 25

<!-- prettier-ignore -->
|ITERATOR|
|---|

#### 2. Continue with condition

Code skips inserting even numbers by using `CONTINUE`.

##### Note 8

This case is not functionally equivalent, but, you can turn the condition into an `IF` statement.

##### Oracle 16

```sql
CREATE TABLE continue_testing_table_2 (iterator VARCHAR2(5));

CREATE OR REPLACE PROCEDURE continue_procedure_2
IS
I NUMBER := 0;
J NUMBER := 20;
BEGIN
    WHILE I <= J LOOP
        I := I + 1;
        CONTINUE WHEN MOD(I,2) = 0;
        INSERT INTO continue_testing_table_2 VALUES(TO_CHAR(I));
    END LOOP;
END;

CALL continue_procedure_2();
SELECT * FROM continue_testing_table_2;
```

##### Result 26

<!-- prettier-ignore -->
|ITERATOR|
|---|
|1|
|3|
|5|
|7|
|9|
|11|
|13|
|15|
|17|
|19|
|21|

##### Snowflake Scripting 6

```sql
CREATE OR REPLACE TABLE continue_testing_table_2 (iterator VARCHAR(5))
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

CREATE OR REPLACE PROCEDURE continue_procedure_2 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        I NUMBER(38, 18) := 0;
        J NUMBER(38, 18) := 20;
    BEGIN
        WHILE (:I <= :J)
                         --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
                         LOOP
                             I := :I + 1;
                             IF (MOD(:I,2) = 0) THEN
                                 CONTINUE;
                             END IF;
                                    INSERT INTO continue_testing_table_2
                             VALUES(TO_CHAR(:I));
                                END LOOP;
    END;
$$;

CALL continue_procedure_2();

SELECT * FROM
    continue_testing_table_2;
```

##### Result 27

<!-- prettier-ignore -->
|ITERATOR|
|---|
|1|
|3|
|5|
|7|
|9|
|11|
|13|
|15|
|17|
|19|
|21|

#### 3. Continue with label and condition

Code skips line 19, and the inner loop is only executed once because the `CONTINUE` is always
jumping to the outer loop using the label.

##### Note 9

This case is functionally equivalent applying the same process as the previous sample.

##### Note 10

Note that labels are going to be commented out.

##### Oracle 17

```sql
CREATE OR REPLACE PROCEDURE continue_procedure_3
IS
I NUMBER := 0;
J NUMBER := 10;
K NUMBER := 0;
BEGIN
    <`<out_loop>`>
    WHILE I <= J LOOP
        I := I + 1;
        INSERT INTO continue_testing_table_3 VALUES('I' || TO_CHAR(I));

        <`<in_loop>`>
        WHILE K <= J * 2 LOOP
            K := K + 1;
            CONTINUE out_loop WHEN K > J / 2;
            INSERT INTO continue_testing_table_3 VALUES('K' || TO_CHAR(K));
        END LOOP in_loop;

        K := 0;
    END LOOP out_loop;
END;

CALL continue_procedure_3();
SELECT * FROM continue_testing_table_3;
```

##### Result 28

<!-- prettier-ignore -->
|ITERATOR|
|---|
|I1|
|K1|
|K2|
|K3|
|K4|
|K5|
|I2|
|I3|
|I4|
|I5|
|I6|
|I7|
|I8|
|I9|
|I10|
|I11|

##### Snowflake Scripting 7

```sql
CREATE OR REPLACE PROCEDURE continue_procedure_3 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        I NUMBER(38, 18) := 0;
        J NUMBER(38, 18) := 10;
        K NUMBER(38, 18) := 0;
    BEGIN
        !!!RESOLVE EWI!!! /*** SSC-EWI-0094 - LABEL DECLARATION FOR A STATEMENT IS NOT SUPPORTED BY SNOWFLAKE SCRIPTING <`<out_loop>`> ***/!!!
        WHILE (:I <= :J)
                         --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
                         LOOP
                             I := :I + 1;
                                    INSERT INTO continue_testing_table_3
                             VALUES('I' || NVL(TO_CHAR(:I) :: STRING, ''));
                             !!!RESOLVE EWI!!! /*** SSC-EWI-0094 - LABEL DECLARATION FOR A STATEMENT IS NOT SUPPORTED BY SNOWFLAKE SCRIPTING <`<in_loop>`> ***/!!!
                             WHILE (:K <= :J * 2)
                                                  --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
                                                  LOOP
                                                      K := :K + 1;
                                                      IF (:K > :J / 2) THEN
                                                          CONTINUE out_loop;
                                                      END IF;
                                        INSERT INTO continue_testing_table_3
                                                      VALUES('K' || NVL(TO_CHAR(:K) :: STRING, ''));
                                    END LOOP in_loop;
                             K := 0;
                                END LOOP out_loop;
    END;
$$;

CALL continue_procedure_3();

SELECT * FROM
    continue_testing_table_3;
```

##### Result 29

<!-- prettier-ignore -->
|ITERATOR|
|---|
|I1|
|K1|
|K2|
|K3|
|K4|
|K5|
|I2|
|I3|
|I4|
|I5|
|I6|
|I7|
|I8|
|I9|
|I10|
|I11|

### Known Issues 5

No issues were found.

### Related EWIs 5

1. [SSC-EWI-0094](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0094):
   Label declaration not supported.

## DECLARE

Translation reference to convert Oracle DECLARE statement to Snowflake Scripting

### Note 11

Some parts in the output code are omitted for clarity reasons.

### Description 5

Oracle DECLARE statement is an optional part of the PL/SQL block statement. It allows the creation
of variables, constants, procedures declarations, and definitions, functions declarations, and
definitions, exceptions, cursors, types, and many other statements. For more information regarding
Oracle DECLARE, check
[here](https://docs.oracle.com/en/database/oracle/oracle-database/21/lnpls/block.html#GUID-9ACEB9ED-567E-4E1A-A16A-B8B35214FC9D).

#### Oracle DECLARE Syntax

```sql
declare_section body

declare_section::= { item_list_1 [ item_list_2 ] | item_list_2 }

item_list_1::=
{ type_definition
<!-- prettier-ignore -->
|cursor_declaration
|item_declaration
|function_declaration
|procedure_declaration
}
 ...

item_list_2::=
{ cursor_declaration
<!-- prettier-ignore -->
|cursor_definition
|function_declaration
|function_definition
|procedure_declaration
|procedure_definition
}
 ...

item_declaration::=
{ collection_variable_decl
<!-- prettier-ignore -->
|constant_declaration
|cursor_variable_declaration
|exception_declaration
|record_variable_declaration
|variable_declaration
}

body::= BEGIN statement ...
  [ EXCEPTION exception_handler [ exception_handler ]... ] END [ name ] ;
```

##### Snowflake Scripting DECLARE Syntax

```sql
[ DECLARE
  { `<variable_declaration>` | `<cursor_declaration>` | `<exception_declaration>` | `<resultset_declaration>` }
  [, { `<variable_declaration>` | `<cursor_declaration>` | `<exception_declaration>` | `<resultset_declaration>` } ... ]
]
BEGIN
    `<statement>`;
    [ `<statement>`; ... ]
[ EXCEPTION `<exception_handler>` ]
END [ `<label>` ] ;
```

### Sample Source Patterns 5

#### Variable declaration

##### Oracle Variable Declaration Syntax

```sql
variable_declaration::=
variable datatype [ [ NOT NULL] {:= | DEFAULT} expression ] ;
```

##### Snowflake Scripting Variable Declaration Syntax

```sql
`<variable_name>` `<type>`;

`<variable_name>` DEFAULT `<expression>` ;

`<variable_name>` `<type>` DEFAULT `<expression>` ;
```

##### Oracle 18

```sql
CREATE OR REPLACE PROCEDURE var_decl_proc
IS
var1 NUMBER;
var2 NUMBER := 1;
var3 NUMBER NOT NULL := 1;
var4 NUMBER DEFAULT 1;
var5 NUMBER NOT NULL DEFAULT 1;
BEGIN
    NULL;
END;
```

##### Snowflake Scripting 8

```sql
CREATE OR REPLACE PROCEDURE var_decl_proc ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        var1 NUMBER(38, 18);
        var2 NUMBER(38, 18) := 1;
        var3 NUMBER(38, 18) := 1 /*** SSC-FDM-OR0025 - NOT NULL CONSTRAINT IS NOT SUPPORTED BY SNOWFLAKE ***/;
        var4 NUMBER(38, 18) DEFAULT 1;
        var5 NUMBER(38, 18) DEFAULT 1 /*** SSC-FDM-OR0025 - NOT NULL CONSTRAINT IS NOT SUPPORTED BY SNOWFLAKE ***/;
    BEGIN
        NULL;
    END;
$$;
```

#### Constant declaration

Warning

Constants are not supported in Snowflake Scripting, however, they are being transformed to variables
to simulate the behavior.

##### Oracle Constant Declaration Syntax

```sql
constant_declaration::=
constant CONSTANT datatype [NOT NULL] { := | DEFAULT } expression ;
```

##### Snowflake Scripting Variable Declaration Syntax 2

```sql
`<variable_name>` `<type>`;

`<variable_name>` DEFAULT `<expression>` ;

`<variable_name>` `<type>` DEFAULT `<expression>` ;
```

##### Oracle 19

```sql
CREATE OR REPLACE PROCEDURE const_decl_proc
IS
my_const1 CONSTANT NUMBER := 40;
my_const2 CONSTANT NUMBER NOT NULL := 40;
my_const2 CONSTANT NUMBER DEFAULT 40;
my_const2 CONSTANT NUMBER NOT NULL DEFAULT 40;
BEGIN
    NULL;
END;
```

##### Snowflake Scripting 9

```sql
CREATE OR REPLACE PROCEDURE const_decl_proc ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        --** SSC-FDM-0016 - CONSTANTS ARE NOT SUPPORTED BY SNOWFLAKE SCRIPTING. IT WAS TRANSFORMED TO A VARIABLE **
        my_const1 NUMBER(38, 18) := 40;
        --** SSC-FDM-0016 - CONSTANTS ARE NOT SUPPORTED BY SNOWFLAKE SCRIPTING. IT WAS TRANSFORMED TO A VARIABLE **
        --** SSC-FDM-OR0025 - NOT NULL CONSTRAINT IS NOT SUPPORTED BY SNOWFLAKE **
        my_const2 NUMBER(38, 18) := 40;
        --** SSC-FDM-0016 - CONSTANTS ARE NOT SUPPORTED BY SNOWFLAKE SCRIPTING. IT WAS TRANSFORMED TO A VARIABLE **
        my_const2 NUMBER(38, 18) DEFAULT 40;
        --** SSC-FDM-0016 - CONSTANTS ARE NOT SUPPORTED BY SNOWFLAKE SCRIPTING. IT WAS TRANSFORMED TO A VARIABLE **
        --** SSC-FDM-OR0025 - NOT NULL CONSTRAINT IS NOT SUPPORTED BY SNOWFLAKE **
        my_const2 NUMBER(38, 18) DEFAULT 40;
    BEGIN
        NULL;
    END;
$$;
```

#### Cursor declaration

##### Oracle Cursor Declaration Syntax

```sql
cursor_declaration::= CURSOR cursor
  [( cursor_parameter_dec [, cursor_parameter_dec ]... )]
    RETURN rowtype;

cursor_parameter_dec::= parameter [IN] datatype [ { := | DEFAULT } expression ]

rowtype::=
{ {db_table_or_view | cursor | cursor_variable}%ROWTYPE
  | record%TYPE
  | record_type
  }
```

##### Snowflake Scripting Cursor Declaration Syntax

```sql
`<cursor_name>` CURSOR [ ( `<argument>` [, `<argument>` ... ] ) ]
        FOR `<query>` ;
```

Danger

The Oracle **_cursor declaration_** is not required so it might be commented out on the output code.
The **_cursor definition_** will be used instead of and it will be converted to the Snowflake
Scripting **_cursor declaration_**. Please go to the
[CURSOR](https://github.com/snowflake-mountain/SC.Docs/blob/main/translation-reference/translation-reference-1/pl-sql-to-snowflake-scripting/broken-reference/#README)
section to get more information about cursor definition.

#### Exception declaration

The exception declaration sometimes could be followed by the exception initialization, the current
transformation takes both and merge them into the Snowflake Scripting exception declaration. The
original `PRAGMA` `EXCEPTION_INIT` will be commented out.

##### Oracle Exception Declaration Syntax

```sql
exception_declaration::= exception EXCEPTION;

PRAGMA EXCEPTION_INIT ( exception, error_code ) ;
```

##### Snowflake Scripting Exception Declaration Syntax

```sql
`<exception_name>` EXCEPTION [ ( `<exception_number>` , '`<exception_message>`' ) ] ;
```

##### Oracle 20

```sql
CREATE OR REPLACE PROCEDURE procedure_exception
IS
my_exception EXCEPTION;
my_exception2 EXCEPTION;
PRAGMA EXCEPTION_INIT ( my_exception2, -20100 );
my_exception3 EXCEPTION;
PRAGMA EXCEPTION_INIT ( my_exception3, -19000 );
BEGIN
    NULL;
END;
```

##### Snowflake Scripting 10

```sql
CREATE OR REPLACE PROCEDURE procedure_exception ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        my_exception EXCEPTION;
        my_exception2 EXCEPTION (-20100, '');
        !!!RESOLVE EWI!!! /*** SSC-EWI-OR0051 - PRAGMA EXCEPTION_INIT IS NOT SUPPORTED ***/!!!
        PRAGMA EXCEPTION_INIT ( my_exception2, -20100 );
        !!!RESOLVE EWI!!! /*** SSC-EWI-OR0099 - EXCEPTION CODE NUMBER EXCEEDS SNOWFLAKE SCRIPTING LIMITS ***/!!!
        my_exception3 EXCEPTION;
        !!!RESOLVE EWI!!! /*** SSC-EWI-OR0051 - PRAGMA EXCEPTION_INIT IS NOT SUPPORTED ***/!!!
PRAGMA EXCEPTION_INIT ( my_exception3, -19000 );
    BEGIN
        NULL;
    END;
$$;
```

#### Not supported cases

The next Oracle declaration statements are not supported by the Snowflake Scripting declaration
block:

1. Cursor variable declaration.
2. Collection variable declaration.
3. Record variable declaration.
4. Type definition (all its variants).
5. Function declaration and definition.
6. Procedure declaration and definition.

### Known issues 6

#### 1. The variable declarations with NOT NULL constraints are not supported by Snow Scripting

The creation of variables with `NOT NULL` constraint throws an error in Snow Scripting.

##### 2. The cursor declaration has no equivalent to Snowflake Scripting

The Oracle cursor declaration is useless so it might be commented out in the output code. The cursor
definition will be used instead and it will be converted to the Snowflake Scripting cursor
declaration.

##### 3. The exception code exceeds Snowflake Scripting limits

Oracle exception code is being removed when it exceeds the Snowflake Scripting code limits. The
exception code must be an integer between -20000 and -20999.

##### 3. The not supported cases

There are some Oracle declaration statements that are not supported by the Snowflake Scripting
declaration block, so it might be commented out and a warning will be added.

### Related EWIS 6

1. [SSC-EWI-OR0051](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI#ssc-ewi-or0051):
   PRAGMA EXCEPTION_INIT is not supported.
2. [SSC-EWI-OR0099](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI#ssc-ewi-or0099):
   The exception code exceeds the Snowflake Scripting limit.
3. [SSC-FDM-0016](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0016):
   Constants are not supported by Snowflake Scripting. It was transformed into a variable.
4. [SSC-FDM-OR0025](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM#ssc-fdm-or0025):
   Not Null constraint is not supported in Snowflake Procedures.

## DEFAULT PARAMETERS

This article is about the current transformation of the default parameters and how their
functionality is being emulated.

### Note 12

Some parts in the output code are omitted for clarity reasons.

### Description 6

A **default parameter** is a parameter that has a value in case an argument is not passed in the
procedure or function call. Since Snowflake doesn’t support default parameters, SnowConvert AI
inserts the default value in the procedure or function call.

In the declaration, the DEFAULT VALUE clause of the parameter is removed. Both syntaxes, the `:=`
symbol and the `DEFAULT` clause, are supported.

### Sample Source Patterns 6

#### Sample auxiliary code

##### Oracle 21

```sql
CREATE TABLE TABLE1(COL1 NUMBER, COL2 NUMBER);
CREATE TABLE TABLE2(COL1 NUMBER, COL2 NUMBER, COL2 NUMBER);0016
```

##### Snowflake 11

```sql
CREATE OR REPLACE TABLE TABLE1 (COL1 NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/,
COL2 NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

CREATE OR REPLACE TABLE TABLE2 (COL1 NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/,
COL2 NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/,
COL2 NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;
```

#### Default parameter declaration

##### Oracle 22

```sql
CREATE OR REPLACE PROCEDURE PROC_WITH_DEFAULT_PARAMS1 (
    param1 NUMBER,
    param2 NUMBER default TO_NUMBER(1)
)
AS
BEGIN
 INSERT INTO TABLE1 (COL1, COL2)
    VALUES(param1, param2);
END;
CREATE OR REPLACE PROCEDURE PROC_WITH_DEFAULT_PARAMS2 (
    param1 NUMBER default 1,
    param2 NUMBER default 2
)
AS
BEGIN
 INSERT INTO TABLE1 (COL1, COL2)
    VALUES(param1, param2);
END;

CREATE OR REPLACE PROCEDURE PROCEDURE_WITH_DEAFAULT_PARAMS3 (
    param1 NUMBER DEFAULT 100,
    param2 NUMBER,
    param3 NUMBER DEFAULT 1000
)
IS
BEGIN
 INSERT INTO TABLE2(COL1, COL2, COL3)
    VALUES (param1, param2, param3);
END;
```

##### Snowflake Scripting 11

```sql
CREATE OR REPLACE PROCEDURE PROC_WITH_DEFAULT_PARAMS1 (param1 NUMBER(38, 18),
   param2 NUMBER(38, 18) DEFAULT TO_NUMBER(1)
)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
 BEGIN
  INSERT INTO TABLE1(COL1, COL2)
     VALUES(:param1, :param2);
 END;
$$;

CREATE OR REPLACE PROCEDURE PROC_WITH_DEFAULT_PARAMS2 (
   param1 NUMBER(38, 18) DEFAULT 1,
   param2 NUMBER(38, 18) DEFAULT 2
)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
 BEGIN
  INSERT INTO TABLE1(COL1, COL2)
     VALUES(:param1, :param2);
 END;
$$;

CREATE OR REPLACE PROCEDURE PROCEDURE_WITH_DEAFAULT_PARAMS3 (
   param1 NUMBER(38, 18) DEFAULT 100, param2 NUMBER(38, 18),
   param3 NUMBER(38, 18) DEFAULT 1000
)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
 BEGIN
  INSERT INTO TABLE2(COL1, COL2, COL3)
     VALUES (:param1, :param2, :param3);
 END;
$$;
```

#### Calling procedures with default parameters

##### Oracle 23

```sql
CREATE OR REPLACE PROCEDURE PROC_WITH_DEFAULT_CALLS
AS
BEGIN
    PROC_WITH_DEFAULT_PARAMS1(10, 15);
    PROC_WITH_DEFAULT_PARAMS1(10);
    PROC_WITH_DEFAULT_PARAMS2(10, 15);
    PROC_WITH_DEFAULT_PARAMS2(10);
    PROC_WITH_DEFAULT_PARAMS2();
END;
```

##### Snowflake Scripting 12

```sql
CREATE OR REPLACE PROCEDURE PROC_WITH_DEFAULT_CALLS ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        CALL
        PROC_WITH_DEFAULT_PARAMS1(10, 15);
        CALL
        PROC_WITH_DEFAULT_PARAMS1(10);
        CALL
        PROC_WITH_DEFAULT_PARAMS2(10, 15);
        CALL
        PROC_WITH_DEFAULT_PARAMS2(10);
        CALL
        PROC_WITH_DEFAULT_PARAMS2();
    END;
$$;
```

In order to check that the functionality is being emulated correctly the following query is going to
execute the procedure and a `SELECT` from the table mentioned before.

##### Oracle 24

```sql
CALL PROC_WITH_DEFAULT_CALLS();

SELECT * FROM TABLE1;
```

##### Result 30

<!-- prettier-ignore -->
|COL1|COL2|
|---|---|
|10|15|
|10|1|
|10|15|
|10|2|
|1|2|

##### Snowflake Scripting 13

```sql
CALL PROC_WITH_DEFAULT_CALLS();

SELECT * FROM TABLE1;
```

##### Result 31

<!-- prettier-ignore -->
|COL1|COL2|
|---|---|
|10|15|
|10|1|
|10|15|
|10|2|
|1|2|

#### Calling procedures with named arguments and default parameters

##### Oracle 25

```sql
CREATE OR REPLACE PROCEDURE PROC_WITH_DEFAULT_CALLS2
AS
BEGIN
    PROCEDURE_WITH_DEAFAULT_PARAMS3(10, 20, 30);
    PROCEDURE_WITH_DEAFAULT_PARAMS3(param1 => 10, param2 => 20, param3 => 30);
    PROCEDURE_WITH_DEAFAULT_PARAMS3(param3 => 10, param1 => 20, param2 => 30);
    PROCEDURE_WITH_DEAFAULT_PARAMS3(param3 => 10, param2 => 30);
    PROCEDURE_WITH_DEAFAULT_PARAMS3(param2 => 10, param3 => 30);
    PROCEDURE_WITH_DEAFAULT_PARAMS3(param2 => 10);
END;
```

##### Snowflake Scripting 14

```sql
CREATE OR REPLACE PROCEDURE PROC_WITH_DEFAULT_CALLS2 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        CALL
        PROCEDURE_WITH_DEAFAULT_PARAMS3(10, 20, 30);
        CALL
        PROCEDURE_WITH_DEAFAULT_PARAMS3(10, 20, 30);
        CALL
        PROCEDURE_WITH_DEAFAULT_PARAMS3(10, 20, 30);
        CALL
        PROCEDURE_WITH_DEAFAULT_PARAMS3(10, 30);
        CALL
        PROCEDURE_WITH_DEAFAULT_PARAMS3(10, 30);
        CALL
        PROCEDURE_WITH_DEAFAULT_PARAMS3(10);
    END;
$$;
```

In order to check that the functionality is being emulated correctly the following query is going to
execute the procedure and a `SELECT` from the table mentioned before.

##### Oracle 26

```sql
CALL PROC_WITH_DEFAULT_CALLS2();

SELECT * FROM TABLE2;
```

##### Result 32

<!-- prettier-ignore -->
|COL1|COL2|COL3|
|---|---|---|
|10|20|30|
|20|30|10|
|100|30|10|
|100|10|30|
|100|10|1000|

##### Snowflake Scripting 15

```sql
CALL PROC_WITH_DEFAULT_CALLS2();

SELECT * FROM TABLE2;
```

##### Result 33

<!-- prettier-ignore -->
|COL1|COL2|COL3|
|---|---|---|
|10|20|30|
|20|30|10|
|100|30|10|
|100|10|30|
|100|10|1000|

### Known Issues 7

1. No issues found

### Related EWIs 7

No related EWIs.

## EXECUTE IMMEDIATE

Translation reference to convert Oracle EXECUTE IMMEDIATE statement to Snowflake Scripting

### Description 7

> The `EXECUTE` `IMMEDIATE` statement builds and runs a dynamic SQL statement in a single operation.
>
> Native dynamic SQL uses the `EXECUTE` `IMMEDIATE` statement to process most dynamic SQL
> statements.
> ([Oracle PL/SQL Language Reference EXECUTE IMMEDIATE Statement](https://docs.oracle.com/en/database/oracle/oracle-database/21/lnpls/EXECUTE-IMMEDIATE-statement.html#GUID-C3245A95-B85B-4280-A01F-12307B108DC8))

#### Oracle EXECUTE IMMEDIATE Syntax

```sql
EXECUTE IMMEDIATE <dynamic statement> [<additional clause> , ...];

dynamic statement::= { '<string literal>' | `<variable>` }

additional clauses::=
{ <into clause> [<using clause>]
<!-- prettier-ignore -->
|<bulk collect into clause> [<using clause>]
|<using clause> [<dynamic return clause>]
|<dynamic return clasue> }
```

Snowflake Scripting has support for this statement, albeit with some functional differences. For
more information on the Snowflake counterpart, please visit
[Snowflake’s EXECUTE IMMEDIATE documentation](https://docs.snowflake.com/en/LIMITEDACCESS/snowscript-introduction.html#execute-immediate).

##### Snow Scripting EXECUTE IMMEDIATE Syntax

```sql
EXECUTE IMMEDIATE <dynamic statement> ;

dynamic statement::= {'<string literal>' | `<variable>` | $<session variable>}
```

### Sample Source Patterns 7

The next samples will create a table, and attempt to drop the table using Execute Immediate.

#### Using a hard-coded string

##### Oracle 27

```sql
CREATE TABLE immediate_dropped_table(
    col1 INTEGER
);

CREATE OR REPLACE PROCEDURE dropping_procedure
AS BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE immediate_dropped_table PURGE';
END;

CALL dropping_procedure();
SELECT * FROM immediate_dropped_table;
```

##### Snowflake Scripting 16

```sql
CREATE OR REPLACE TABLE immediate_dropped_table (
    col1 INTEGER
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

CREATE OR REPLACE PROCEDURE dropping_procedure ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        !!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!
        EXECUTE IMMEDIATE 'DROP TABLE immediate_dropped_table';
    END;
$$;

CALL dropping_procedure();

SELECT * FROM
    immediate_dropped_table;
```

#### Storing the string in a variable

##### Oracle 28

```sql
CREATE TABLE immediate_dropped_table(
    col1 INTEGER
);

CREATE OR REPLACE PROCEDURE dropping_procedure
AS
BEGIN
    DECLARE
        statement_variable VARCHAR2(500) := 'DROP TABLE immediate_dropped_table PURGE';
    BEGIN
        EXECUTE IMMEDIATE statement_variable;
    END;
END;

CALL dropping_procedure();
SELECT * FROM immediate_dropped_table;
```

##### Snowflake Scripting 17

```sql
CREATE OR REPLACE TABLE immediate_dropped_table (
    col1 INTEGER
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

CREATE OR REPLACE PROCEDURE dropping_procedure ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        DECLARE
            statement_variable VARCHAR(500) := 'DROP TABLE immediate_dropped_table';
        BEGIN
            !!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!
            EXECUTE IMMEDIATE :statement_variable;
        END;
    END;
$$;

CALL dropping_procedure();

SELECT * FROM
    immediate_dropped_table;
```

#### Concatenation for parameters in dynamic statement

##### Oracle 29

```sql
CREATE TABLE immediate_dropped_table(
    col1 INTEGER
);

CREATE OR REPLACE PROCEDURE dropping_procedure(param1 VARCHAR2)
AS
BEGIN
    DECLARE
        statement_variable VARCHAR2(500) := 'DROP TABLE ' || param1 || ' PURGE';
    BEGIN
        EXECUTE IMMEDIATE statement_variable;
    END;
END;

CALL dropping_procedure();
SELECT * FROM immediate_dropped_table;
```

##### Snowflake Scripting 18

```sql
CREATE OR REPLACE TABLE immediate_dropped_table (
    col1 INTEGER
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

CREATE OR REPLACE PROCEDURE dropping_procedure (param1 VARCHAR)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        DECLARE
            statement_variable VARCHAR(500) := 'DROP TABLE ' || NVL(:param1 :: STRING, '');
        BEGIN
            !!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!
            EXECUTE IMMEDIATE :statement_variable;
        END;
    END;
$$;

CALL dropping_procedure();

SELECT * FROM
    immediate_dropped_table;
```

#### USING Clause transformation

##### Oracle 30

```sql
CREATE TABLE immediate_inserted_table(COL1 INTEGER);

CREATE OR REPLACE PROCEDURE inserting_procedure_using(param1 INTEGER)
AS
BEGIN
    EXECUTE IMMEDIATE 'INSERT INTO immediate_inserted_table VALUES (:1)' USING param1;
END;

CALL inserting_procedure_using(1);

SELECT * FROM immediate_inserted_table;
```

##### Results

<!-- prettier-ignore -->
|COL1|
|---|
|1|

##### Snowflake Scripting 19

###### Note 13

Please note parenthesis are required for parameters in the USING Clause in Snowflake Scripting.

```sql
CREATE OR REPLACE TABLE immediate_inserted_table (COL1 INTEGER)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

CREATE OR REPLACE PROCEDURE inserting_procedure_using (param1 INTEGER)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        !!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!
        EXECUTE IMMEDIATE 'INSERT INTO immediate_inserted_table
VALUES (?)' USING ( param1);
    END;
$$;

CALL inserting_procedure_using(1);

SELECT * FROM
    immediate_inserted_table;
```

##### Results 2

<!-- prettier-ignore -->
|COL1|
|---|
|1|

### Known Issues 8

#### 1. Immediate Execution results cannot be stored in variables

SnowScripting does not support INTO nor BULK COLLECT INTO clauses. For this reason, results will
need to be passed through other means.

##### 2. Numeric Placeholders

Numeric Names for placeholders are currently not being recognized by SnowConvert AI, but there is a
work item to fix this issue.

##### 3. Argument Expressions are not supported by Snowflake Scripting

In Oracle it is possible to use Expressions as Arguments for the Using Clause; however, this is not
supported by Snowflake Scripting, and they are commented out.

##### 4. Dynamic SQL Execution queries may be marked incorrectly as non-runnable

In some scenarios there an execute statement may be commented regardless of being safe or non-safe
to run so please take this into account:

##### Oracle 31

```sql
CREATE OR REPLACE PROCEDURE inserting_procedure_variable_execute_concatenation_parameter(param1 INTEGER)
IS
    query VARCHAR2(500) := 'INSERT INTO immediate_inserted_table VALUES (';
BEGIN
    EXECUTE IMMEDIATE query || param1 || ')';
END;
```

##### Snowflake Scripting 20

###### Note 14

Please note parenthesis are required for parameters in the USING Clause in Snowflake Scripting.

```sql
CREATE OR REPLACE PROCEDURE inserting_procedure_variable_execute_concatenation_parameter (param1 INTEGER)
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
    DECLARE
        query VARCHAR(500) := 'INSERT INTO immediate_inserted_table VALUES (';
    BEGIN
        !!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!
        !!!RESOLVE EWI!!! /*** SSC-EWI-0027 - THE FOLLOWING STATEMENT USES A VARIABLE/LITERAL WITH AN INVALID QUERY AND IT WILL NOT BE EXECUTED ***/!!!
        EXECUTE IMMEDIATE NVL(:query :: STRING, '') || NVL(:param1 :: STRING, '') || ')';
    END;
$$;
```

### Related EWIs 8

1. [SSC-EWI-0027](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0027):
   Variable with invalid query.
2. [SSC-EWI-0030](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0030):
   The statement below has usages of dynamic SQL.

## EXIT

Translation reference to convert Oracle EXIT statement to Snowflake Scripting

### Note 15

Some parts in the output code are omitted for clarity reasons.

### Description 8

> The `EXIT` statement exits the current iteration of a loop, either conditionally or
> unconditionally, and transfers control to the end of either the current loop or an enclosing
> labeled loop.
> ([Oracle PL/SQL Language Reference EXIT Statement](https://docs.oracle.com/en/database/oracle/oracle-database/21/lnpls/EXIT-statement.html#GUID-66E20B6C-3606-42AD-A7DB-C8EC782B94D8))

#### Oracle EXIT Syntax

```sql
EXIT [ label ] [ WHEN boolean_expression ] ;
```

##### Snowflake Scripting EXIT Syntax

```sql
{ BREAK | EXIT } [ `<label>` ] ;
```

### Sample Source Patterns 8

#### Note 16

Note that you can change `EXIT`with `BREAK`and everything will work the same.

#### 1. Simple Exit

Code skips the `INSERT` statement by using `EXIT`.

##### Note 17

This case is functionally equivalent.

##### Oracle 32

```sql
CREATE TABLE exit_testing_table_1 (
    iterator VARCHAR2(5)
);

CREATE OR REPLACE PROCEDURE exit_procedure_1
IS
I NUMBER := 0;
J NUMBER := 20;
BEGIN
    WHILE I <= J LOOP
        I := I + 1;
        EXIT;
        INSERT INTO exit_testing_table_1 VALUES(TO_CHAR(I));
    END LOOP;
END;

CALL exit_procedure_1();
SELECT * FROM exit_testing_table_1;
```

##### Result 34

<!-- prettier-ignore -->
|ITERATOR|
|---|

##### Snowflake Scripting 21

```sql
CREATE OR REPLACE TABLE exit_testing_table_1 (
       iterator VARCHAR(5)
   )
   COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/14/2025",  "domain": "no-domain-provided" }}'
   ;

   CREATE OR REPLACE PROCEDURE exit_procedure_1 ()
   RETURNS VARCHAR
   LANGUAGE SQL
   COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/14/2025",  "domain": "no-domain-provided" }}'
   EXECUTE AS CALLER
   AS
   $$
       DECLARE
           I NUMBER(38, 18) := 0;
           J NUMBER(38, 18) := 20;
       BEGIN
           WHILE (:I <= :J)
                            --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
                            LOOP
                                I := :I + 1;
                                EXIT;
                                       INSERT INTO exit_testing_table_1
                                VALUES(TO_CHAR(:I));
                                   END LOOP;
       END;
   $$;

   CALL exit_procedure_1();

   SELECT * FROM
       exit_testing_table_1;
```

##### Result 35

<!-- prettier-ignore -->
|ITERATOR|
|---|

#### 2. Exit with condition

Code exits the loop when the iterator is greater than 5.

##### Note 18

This case is functionally equivalent by turning the condition into an `IF` statement.

##### Oracle 33

```sql
CREATE TABLE exit_testing_table_2 (
    iterator VARCHAR2(5)
);

CREATE OR REPLACE PROCEDURE exit_procedure_2
IS
I NUMBER := 0;
J NUMBER := 20;
BEGIN
    WHILE I <= J LOOP
        EXIT WHEN I > 5;
        I := I + 1;
        INSERT INTO exit_testing_table_2 VALUES(TO_CHAR(I));
    END LOOP;
END;

CALL exit_procedure_2();
SELECT * FROM exit_testing_table_2;
```

##### Result 36

<!-- prettier-ignore -->
|ITERATOR|
|---|
|1|
|2|
|3|
|4|
|5|
|6|

##### Snowflake Scripting 22

```sql
CREATE OR REPLACE TABLE exit_testing_table_2 (
       iterator VARCHAR(5)
   )
   COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/14/2025",  "domain": "no-domain-provided" }}'
   ;

   CREATE OR REPLACE PROCEDURE exit_procedure_2 ()
   RETURNS VARCHAR
   LANGUAGE SQL
   COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/14/2025",  "domain": "no-domain-provided" }}'
   EXECUTE AS CALLER
   AS
   $$
       DECLARE
           I NUMBER(38, 18) := 0;
           J NUMBER(38, 18) := 20;
       BEGIN
           WHILE (:I <= :J)
                            --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
                            LOOP
                                IF (:I > 5) THEN
                                    EXIT;
                                END IF;
                                I := :I + 1;
                                       INSERT INTO exit_testing_table_2
                                VALUES(TO_CHAR(:I));
                                   END LOOP;
       END;
   $$;

   CALL exit_procedure_2();

   SELECT * FROM
       exit_testing_table_2;
```

##### Result 37

<!-- prettier-ignore -->
|ITERATOR|
|---|
|1|
|2|
|3|
|4|
|5|
|6|

#### 3. Exit with label and condition

Code breaks both loops by using the `EXIT` statement pointing to the outer loop.

##### Note 19

This case is functionally equivalent applying the same process as the previous sample.

##### Note 20

Note that labels are going to be commented out.

##### Oracle 34

```sql
CREATE TABLE exit_testing_table_3 (
    iterator VARCHAR2(5)
);

CREATE OR REPLACE PROCEDURE exit_procedure_3
IS
I NUMBER := 0;
J NUMBER := 10;
K NUMBER := 0;
BEGIN
    <`<out_loop>`>
    WHILE I <= J LOOP
        I := I + 1;
        INSERT INTO exit_testing_table_3 VALUES('I' || TO_CHAR(I));

        <`<in_loop>`>
        WHILE K <= J * 2 LOOP
            K := K + 1;
                EXIT out_loop WHEN K > J / 2;
            INSERT INTO exit_testing_table_3 VALUES('K' || TO_CHAR(K));
        END LOOP in_loop;

        K := 0;
    END LOOP out_loop;
END;

CALL exit_procedure_3();
SELECT * FROM exit_testing_table_3;
```

##### Result 38

<!-- prettier-ignore -->
|ITERATOR|
|---|
|I1|
|K1|
|K2|
|K3|
|K4|
|K5|

##### Snowflake Scripting 23

```sql
CREATE OR REPLACE TABLE exit_testing_table_3 (
       iterator VARCHAR(5)
   )
   COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/14/2025",  "domain": "no-domain-provided" }}'
   ;

   CREATE OR REPLACE PROCEDURE exit_procedure_3 ()
   RETURNS VARCHAR
   LANGUAGE SQL
   COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/14/2025",  "domain": "no-domain-provided" }}'
   EXECUTE AS CALLER
   AS
   $$
       DECLARE
           I NUMBER(38, 18) := 0;
           J NUMBER(38, 18) := 10;
           K NUMBER(38, 18) := 0;
       BEGIN
           !!!RESOLVE EWI!!! /*** SSC-EWI-0094 - LABEL DECLARATION FOR A STATEMENT IS NOT SUPPORTED BY SNOWFLAKE SCRIPTING <`<out_loop>`> ***/!!!
           WHILE (:I <= :J)
                            --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
                            LOOP
                                I := :I + 1;
                                       INSERT INTO exit_testing_table_3
                                VALUES('I' || NVL(TO_CHAR(:I) :: STRING, ''));
                                !!!RESOLVE EWI!!! /*** SSC-EWI-0094 - LABEL DECLARATION FOR A STATEMENT IS NOT SUPPORTED BY SNOWFLAKE SCRIPTING <`<in_loop>`> ***/!!!
                                WHILE (:K <= :J * 2)
                                                     --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
                                                     LOOP
                                                         K := :K + 1;
                                                         IF (:K > :J / 2) THEN
                                                             EXIT out_loop;
                                                         END IF;
                                           INSERT INTO exit_testing_table_3
                                                         VALUES('K' || NVL(TO_CHAR(:K) :: STRING, ''));
                                       END LOOP in_loop;
                                K := 0;
                                   END LOOP out_loop;
       END;
   $$;

   CALL exit_procedure_3();

   SELECT * FROM
       exit_testing_table_3;
```

##### Result 39

<!-- prettier-ignore -->
|ITERATOR|
|---|
|I1|
|K1|
|K2|
|K3|
|K4|
|K5|

### Known Issues 9

No issues were found.

### Related EWIs 9

1. [SSC-EWI-0094](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0094):
   Label declaration not supported.

## EXPRESSIONS

Translation reference for Oracle expressions to Snow Scripting

### Note 21

Some parts in the output code are omitted for clarity reasons.

### Description 9

The following table has a summary of how to transform the different
[Oracle Expression kinds](https://docs.oracle.com/en/database/oracle/oracle-database/21/lnpls/expression.html#GUID-D4700B45-F2C8-443E-AEE7-2BD20FFD45B8)
into Snow Scripting.

<!-- prettier-ignore -->
|**Syntax**|**Conversion status**|**Notes**|
|---|---|---|
|[Character Expressions](https://docs.oracle.com/en/database/oracle/oracle-database/21/lnpls/expression.html#GUID-D4700B45-F2C8-443E-AEE7-2BD20FFD45B8__CHDGJCJE)|Partial|[Partially Supported Common scenarios](#partially-supported-common-scenarios)|
|[Numeric Expressions](https://docs.oracle.com/en/database/oracle/oracle-database/21/lnpls/expression.html#GUID-D4700B45-F2C8-443E-AEE7-2BD20FFD45B8__CHDIEJAI)|Partial|[Partially Supported Common scenarios](#not-supported-numeric-expressions)|
|[Date Expressions](https://docs.oracle.com/en/database/oracle/oracle-database/21/lnpls/expression.html#GUID-D4700B45-F2C8-443E-AEE7-2BD20FFD45B8__CHDIAFJD)|Partial|[Partially Supported Common scenarios](#not-supported-cases)|
|[Boolean Expressions](https://docs.oracle.com/en/database/oracle/oracle-database/21/lnpls/expression.html#GUID-D4700B45-F2C8-443E-AEE7-2BD20FFD45B8__CHDDGEFH)|Partial|[Not supported boolean expressions](#not-supported-boolean-expressions)|
|[Simple Case Expressions](https://docs.oracle.com/en/database/oracle/oracle-database/21/lnpls/expression.html#GUID-D4700B45-F2C8-443E-AEE7-2BD20FFD45B8__CHDIFFCB)|Full|N/A|
|[Searched Case Expressions](https://docs.oracle.com/en/database/oracle/oracle-database/21/lnpls/expression.html#GUID-D4700B45-F2C8-443E-AEE7-2BD20FFD45B8__CHDGJEJJ)|Full|N/A|
|[Collection Constructor](https://docs.oracle.com/en/database/oracle/oracle-database/21/lnpls/expression.html#GUID-D4700B45-F2C8-443E-AEE7-2BD20FFD45B8__CJACBCAB)|Not Translated|Snowflake does not have a native equivalent for Oracle collections. See [Collections and Records](collections-and-records).|
|[Qualified Expressions](https://docs.oracle.com/en/database/oracle/oracle-database/21/lnpls/qualified-expression.html#GUID-1C475462-11D2-4D0B-B2D1-497491F88746__SECTION_O3N_JWF_4JB)|Not Translated|Snowflake does not have a native equivalent for Oracle record types. See [Collections and Records](collections-and-records).|

#### Partially supported common scenarios

##### Oracle Constants

##### Oracle 35

```sql
CREATE TABLE EXPRESSIONS_TABLE(col VARCHAR(30));
CREATE OR REPLACE PROCEDURE EXPRESSIONS_SAMPLE
IS
RESULT VARCHAR(50);
CONST CONSTANT VARCHAR(20) := 'CONSTANT TEXT';
BEGIN
 -- CONSTANT EXPRESSIONS
 RESULT := CONST;
 INSERT INTO EXPRESSIONS_TABLE(COL) VALUES (RESULT);
END;

CALL EXPRESSIONS_SAMPLE();
SELECT * FROM EXPRESSIONS_TABLE;
```

##### Result 40

<!-- prettier-ignore -->
|COL|
|---|
|CONSTANT TEXT|

##### Snowflake 12

```sql
CREATE OR REPLACE TABLE EXPRESSIONS_TABLE (col VARCHAR(30))
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

CREATE OR REPLACE PROCEDURE EXPRESSIONS_SAMPLE ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
 DECLARE
  RESULT VARCHAR(50);
  --** SSC-FDM-0016 - CONSTANTS ARE NOT SUPPORTED BY SNOWFLAKE SCRIPTING. IT WAS TRANSFORMED TO A VARIABLE **
  CONST VARCHAR(20) := 'CONSTANT TEXT';
 BEGIN
  -- CONSTANT EXPRESSIONS
  RESULT := :CONST;
  INSERT INTO EXPRESSIONS_TABLE(COL) VALUES (:RESULT);
 END;
$$;

CALL EXPRESSIONS_SAMPLE();

SELECT * FROM
 EXPRESSIONS_TABLE;
```

##### Result 41

<!-- prettier-ignore -->
|COL|
|---|
|CONSTANT TEXT|

#### Not supported numeric expressions

##### Oracle 36

```sql
CREATE TABLE NUMERIC_EXPRESSIONS_TABLE(col number);

CREATE OR REPLACE PROCEDURE NUMERIC_EXPRESSIONS
IS
RESULT NUMBER;
CURSOR C1 IS SELECT * FROM NUMERIC_EXPRESSIONS_TABLE;
TYPE NUMERIC_TABLE IS TABLE OF NUMBER(10);
COLLECTION NUMERIC_TABLE;
BEGIN
 -- CURSOR EXPRESSIONS
 OPEN C1;
 RESULT := C1%ROWCOUNT;
 CLOSE C1;
 INSERT INTO NUMERIC_EXPRESSIONS_TABLE(COL) VALUES (RESULT);

 -- ** OPERATOR
 RESULT := 10 ** 2;
 INSERT INTO NUMERIC_EXPRESSIONS_TABLE(COL) VALUES (RESULT);

 -- COLLECTION EXPRESSIONS
 COLLECTION := NUMERIC_TABLE(1, 2, 3, 4, 5, 6);
 RESULT := COLLECTION.COUNT + COLLECTION.FIRST;
 INSERT INTO NUMERIC_EXPRESSIONS_TABLE(COL) VALUES (RESULT);

 -- IMPLICIT CURSOR EXPRESSIONS
 UPDATE NUMERIC_EXPRESSIONS_TABLE SET COL = COL + 4;
 RESULT := SQL%ROWCOUNT;
 INSERT INTO NUMERIC_EXPRESSIONS_TABLE(COL) VALUES (RESULT);
END;

CALL NUMERIC_EXPRESSIONS();
SELECT * FROM NUMERIC_EXPRESSIONS_TABLE;
```

##### Result 42

<!-- prettier-ignore -->
|COL|
|---|
|4|
|104|
|11|
|3|

#### Not supported boolean expressions

##### Oracle 37

```sql
--Aux function to convert BOOLEAN to VARCHAR
CREATE OR REPLACE FUNCTION convert_bool(p1 in BOOLEAN)
RETURN VARCHAR
AS
var1 VARCHAR(20) := 'FALSE';
BEGIN
IF p1 THEN
var1 := 'TRUE';
END IF;
RETURN var1;
END;

--Table
CREATE TABLE t_boolean_table
(
conditional_predicate VARCHAR(20),
collection_variable VARCHAR(20),
sql_variable VARCHAR(20)
)

--Main Procedure
CREATE OR REPLACE PROCEDURE p_boolean_limitations
AS

TYPE varray_example IS VARRAY(4) OF VARCHAR(15);
colection_example varray_example := varray_example('John', 'Mary', 'Alberto', 'Juanita');
collection_variable BOOLEAN;
conditional_predicate BOOLEAN;
sql_variable BOOLEAN;

--Result variables
col1 VARCHAR(20);
col2 VARCHAR(20);
col3 VARCHAR(20);
BEGIN

--Conditional predicate
conditional_predicate := INSERTING;

--Collection.EXISTS(index)
collection_variable := colection_example.EXISTS(2);

--Cursor FOUND / NOTFOUND / ISOPEN
sql_variable:= SQL%FOUND OR SQL%NOTFOUND OR SQL%ISOPEN;

--Convert BOOLEAN to VARCHAR to insert
col1 := convert_bool(conditional_predicate);
col2 := convert_bool(collection_variable);
col3 := convert_bool(sql_variable);

INSERT INTO t_boolean_table VALUES (col1, col2, col3);

END;

CALL p_boolean_limitations();

SELECT * FROM t_boolean_table;
```

### Related EWIs 2 2

1. [SSC-FDM-0016](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0016):
   Constants are not supported by Snowflake Scripting. It was transformed to a variable.

## FOR LOOP

### Description 10

> With each iteration of the `FOR` `LOOP` statement, its statements run, its index is either
> incremented or decremented, and control returns to the top of the loop.
> ([Oracle PL/SQL Language Reference FOR LOOP Statement](https://docs.oracle.com/en/database/oracle/oracle-database/21/lnpls/FOR-LOOP-statement.html#GUID-D00F8F0B-ECFC-48B6-B399-D8B5114E7E21)).

#### Oracle Syntax 2

```sql
FOR
pls_identifier [ MUTABLE | IMMUTABLE ] [ constrained_type ]
[ , iterand_decl ]

IN

[ REVERSE ] iteration_control pred_clause_seq
[, qual_iteration_ctl]...

LOOP
statement...
END LOOP [ label ] ;
```

##### Snowflake Scripting Syntax

```sql
FOR `<counter_variable>` IN [ REVERSE ] `<start>` TO `<end>` { DO | LOOP }
    statement;
    [ statement; ... ]
END { FOR | LOOP } [ `<label>` ] ;
```

Snowflake Scripting supports `FOR LOOP` that loops a specified number of times. The upper and lower
bounds must be `INTEGER`. Check more information in the
[Snowflake Scripting documentation](https://docs.snowflake.com/en/sql-reference/snowflake-scripting/for.html#for).

Oracle `FOR LOOP` behavior can also be modified by using the statements:

- [CONTINUE](#continue)
- [EXIT](#exit)
- GOTO
- [RAISE](#raise)

### Sample Source Patterns 9

#### 1. FOR LOOP

##### Note 22

This case is functionally equivalent.

##### Oracle FOR LOOP Example

```sql
CREATE OR REPLACE PROCEDURE P1
AS
BEGIN
    FOR i IN 1..10
    LOOP
        NULL;
    END LOOP;

    FOR i IN VAR1..VAR2
    LOOP
        NULL;
    END LOOP;

    FOR i IN REVERSE 1+2..10+5
    LOOP
        NULL;
    END LOOP;
END;
```

##### Snowflake Scripting FOR LOOP Example

```sql
CREATE OR REPLACE PROCEDURE P1 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/14/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
        FOR i IN 1 TO 10
        --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
        LOOP
            NULL;
        END LOOP;
        --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
        FOR i IN VAR1 TO VAR2
        --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
        LOOP
            NULL;
        END LOOP;
        --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
        FOR i IN REVERSE 1+2 TO 10+5
        --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
        LOOP
            NULL;
        END LOOP;
    END;
$$;
```

#### 2. FOR LOOP with additional clauses

##### Oracle FOR LOOP Example 2

```sql
CREATE OR REPLACE PROCEDURE P2
AS
BEGIN
    FOR i IN 1..10 WHILE i <= 5 LOOP
        NULL;
    END LOOP;

    FOR i IN 5..15 BY 5 LOOP
        NULL;
    END LOOP;
END;
```

##### Snowflake Scripting FOR LOOP Example 2

```sql
CREATE OR REPLACE PROCEDURE P2 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/14/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
        !!!RESOLVE EWI!!! /*** SSC-EWI-OR0101 - FOR LOOP WITH "WHILE" CLAUSE IS CURRENTLY NOT SUPPORTED BY SNOWFLAKE SCRIPTING ***/!!!
        FOR i IN 1 TO 10
                         --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
                         LOOP
                                    NULL;
                                END LOOP;
                         !!!RESOLVE EWI!!! /*** SSC-EWI-OR0101 - FOR LOOP WITH "BY" CLAUSE IS CURRENTLY NOT SUPPORTED BY SNOWFLAKE SCRIPTING ***/!!!
                         --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
                         FOR i IN 5 TO 15
                                          --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
                                          LOOP
                                           NULL;
                                       END LOOP;
    END;
$$;
```

#### 3. FOR LOOP with multiple conditions

##### Oracle FOR LOOP Example 3

```sql
CREATE OR REPLACE PROCEDURE P3
AS
BEGIN
    FOR i IN REVERSE 1..3,
    REVERSE i+5..i+7
    LOOP
        NULL;
    END LOOP;
END;
```

##### Snowflake Scripting FOR LOOP Example 3

```sql
CREATE OR REPLACE PROCEDURE P3 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/14/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
        !!!RESOLVE EWI!!! /*** SSC-EWI-OR0100 - FOR LOOP WITH MULTIPLE CONDITIONS IS CURRENTLY NOT SUPPORTED BY SNOWFLAKE SCRIPTING ***/!!!
        FOR i IN REVERSE 1 TO 3
        --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
        LOOP
            NULL;
        END LOOP;
    END;
$$;
```

#### 4. FOR LOOP with unsupported format

##### Oracle FOR LOOP Example 4

```sql
CREATE OR REPLACE PROCEDURE P3
AS
TYPE values_aat IS TABLE OF PLS_INTEGER INDEX BY PLS_INTEGER;
l_employee_values   values_aat;
BEGIN
    FOR power IN REPEAT power*2 WHILE power <= 64 LOOP
        NULL;
    END LOOP;

    FOR i IN VALUES OF l_employee_values LOOP
        NULL;
    END LOOP;
END;
```

##### Snowflake Scripting FOR LOOP Example 4

```sql
CREATE OR REPLACE PROCEDURE P3 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/14/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
    DECLARE
--        !!!RESOLVE EWI!!! /*** SSC-EWI-0058 - FUNCTIONALITY FOR 'PL COLLECTION TYPE DEFINITION' IS NOT CURRENTLY SUPPORTED BY SNOWFLAKE SCRIPTING ***/!!!
--        TYPE values_aat IS TABLE OF PLS_INTEGER INDEX BY PLS_INTEGER;
        l_employee_values VARIANT !!!RESOLVE EWI!!! /*** SSC-EWI-0062 - CUSTOM TYPE 'values_aat' USAGE CHANGED TO VARIANT ***/!!!;
    BEGIN
        !!!RESOLVE EWI!!! /*** SSC-EWI-OR0103 - FOR LOOP FORMAT IS CURRENTLY NOT SUPPORTED BY SNOWFLAKE SCRIPTING ***/!!!
        --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
        !!!RESOLVE EWI!!! /*** SSC-EWI-OR0101 - FOR LOOP WITH "WHILE" CLAUSE IS CURRENTLY NOT SUPPORTED BY SNOWFLAKE SCRIPTING ***/!!!
        FOR power IN REPEAT power*2 WHILE power <= 64
                                                      --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
                                                      LOOP
            NULL;
        END LOOP;
        !!!RESOLVE EWI!!! /*** SSC-EWI-OR0103 - FOR LOOP FORMAT IS CURRENTLY NOT SUPPORTED BY SNOWFLAKE SCRIPTING ***/!!!
        --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **

        FOR i IN VALUES OF :l_employee_values
                                              --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
                                              LOOP
            NULL;
        END LOOP;
    END;
$$;
```

Warning

Transformation for custom types is currently not supported for Snowflake Scripting.

### Known Issues 10

#### 1. For With Multiple Conditions

Oracle allows multiple conditions in a single `FOR LOOP` however, Snowflake Scripting only allows
one condition per `FOR LOOP`. Only the first condition is migrated and the others are ignored during
transformation. Check SSC-FDM-OR0022.

##### Oracle 38

```sql
FOR i IN REVERSE 1..3,
REVERSE i+5..i+7
LOOP
    NULL;
END LOOP;
```

##### Snowflake Scripting FOR LOOP Example 5

```sql
--** SSC-FDM-OR0022 - FOR LOOP WITH MULTIPLE CONDITIONS IS CURRENTLY NOT SUPPORTED BY SNOWFLAKE SCRIPTING **
FOR i IN REVERSE 1 TO 3 LOOP
    NULL;
END LOOP;
```

###### 2. Mutable vs Inmutable Counter Variable

Oracle allows modifying the value of the `FOR LOOP` variable inside the loop. The
[current documentation](https://docs.snowflake.com/en/sql-reference/snowflake-scripting/for.html#usage-notes)
includes this functionality but Snowflake recommends avoiding this. Modifying the value of this
variable may not behave correctly in Snowflake Scripting.

###### 3. Integer vs Float number for Upper or Lower Bound

Snowflake Scripting only allows an `INTEGER` or an expression that evaluates to an `INTEGER` as a
bound for the `FOR LOOP` condition. Floating numbers will be rounded up or down and alter the
original bound.

###### 4. Oracle Unsupported Clauses

Oracle allows additional clauses to the `FOR LOOP` condition. Like the **BY** clause for a stepped
increment in the condition. And the **WHILE** and **WHEN** clause for boolean expressions. These
additional clauses are not supported in Snowflake Scripting and are ignored during transformation.
Check
[SSC-EWI-OR0101](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI#ssc-ewi-or0101).

##### Oracle 39

```sql
FOR i IN 5..15 BY 5 LOOP
    NULL;
END LOOP;
```

##### Snowflake Scripting 24

```sql
!!!RESOLVE EWI!!! /*** SSC-EWI-OR0101 - FOR LOOP WITH "BY" CLAUSE IS CURRENTLY NOT SUPPORTED BY SNOWFLAKE SCRIPTING ***/!!!
FOR i IN 5 TO 15 LOOP
    NULL;
END LOOP;
```

###### 5. Unsupported Formats

Oracle allows different types of conditions for a `FOR LOOP`. It supports boolean expressions,
collections, records… However, Snowflake scripting only supports `FOR LOOP` with defined integers as
bounds. All other formats are marked as not supported and require additional manual effort to be
transformed. Check
[SSC-EWI-OR0103](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI#ssc-ewi-or0103).

### Related EWIs 10

1. [SSC-EWI-0058](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0058):
   Functionality is not currently supported by Snowflake Scripting.
2. [SSC-EWI-0062](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0062):
   Custom type usage changed to variant.
3. [SSC-EWI-OR0100](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI#ssc-ewi-or0100):
   For Loop With Multiple Conditions Is Currently Not Supported By Snowflake Scripting. Only First
   Condition Is Used.
4. [SSC-EWI-OR0101](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI#ssc-ewi-or0101):
   Specific For Loop Clause Is Currently Not Supported By Snowflake Scripting.
5. [SSC-EWI-OR0103](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI#ssc-ewi-or0103):
   For Loop Format Is Currently Not Supported By Snowflake Scripting.

## FORALL

### Description 11

> The `FORALL` statement runs one DML statement multiple times, with different values in the
> `VALUES` and `WHERE` clauses.
> ([Oracle PL/SQL Language Reference FORALL Statement](https://docs.oracle.com/database/121/LNPLS/forall_statement.htm#LNPLS01321)).

#### Oracle Syntax 3

```sql
FORALL index IN bounds_clause [ SAVE ] [ EXCEPTIONS ] dml_statement ;
```

Warning

Snowflake Scripting has no direct equivalence with the `FORALL` statement, however can be emulated
with different workarounds to get functional equivalence.

### Sample Source Patterns 10

#### Setup Data

##### Oracle 40

##### Tables 1

```sql
CREATE TABLE table1 (
    column1 NUMBER,
    column2 NUMBER
);

INSERT INTO table1 (column1, column2) VALUES (1, 2);
INSERT INTO table1 (column1, column2) VALUES (2, 3);
INSERT INTO table1 (column1, column2) VALUES (3, 4);
INSERT INTO table1 (column1, column2) VALUES (4, 5);
INSERT INTO table1 (column1, column2) VALUES (5, 6);

CREATE TABLE table2 (
    column1 NUMBER,
    column2 NUMBER
);

INSERT INTO table2 (column1, column2) VALUES (1, 2);
```

##### Tables 2

```sql
CREATE TABLE error_table (
    ORA_ERR_NUMBER$ NUMBER,
    ORA_ERR_MESG$ VARCHAR2(2000),
    ORA_ERR_ROWID$ ROWID,
    ORA_ERR_OPTYP$ VARCHAR2(2),
    ORA_ERR_TAG$ VARCHAR2(2000)
);

--departments
CREATE TABLE parent_table(
    Id   INT PRIMARY KEY,
    Name VARCHAR2(10)
);
INSERT INTO parent_table VALUES (10, 'IT');
INSERT INTO parent_table VALUES (20, 'HR');
INSERT INTO parent_table VALUES (30, 'INFRA');

--employees
CREATE TABLE source_table(
  Id INT PRIMARY KEY,
  Name VARCHAR2(20) NOT NULL,
  DepartmentID INT REFERENCES parent_table(Id)
);
INSERT INTO source_table VALUES (101, 'Anurag111111111', 10);
INSERT INTO source_table VALUES (102, 'Pranaya11111111', 20);
INSERT INTO source_table VALUES (103, 'Hina11111111111', 30);

--a copy of source
CREATE TABLE target_table(
  Id INT PRIMARY KEY,
  Name VARCHAR2(10) NOT NULL,
  DepartmentID INT REFERENCES parent_table(Id)
);

INSERT INTO target_table VALUES (101, 'Anurag', 10);
```

##### Snowflake 13

##### Tables 1 2

```sql
CREATE OR REPLACE TABLE table1 (
    column1 NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/,
    column2 NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

INSERT INTO table1(column1, column2) VALUES (1, 2);

INSERT INTO table1(column1, column2) VALUES (2, 3);

INSERT INTO table1(column1, column2) VALUES (3, 4);

INSERT INTO table1(column1, column2) VALUES (4, 5);

INSERT INTO table1(column1, column2) VALUES (5, 6);

CREATE OR REPLACE TABLE table2 (
    column1 NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/,
    column2 NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

INSERT INTO table2(column1, column2) VALUES (1, 2);
```

##### Tables 2 2

```sql
CREATE OR REPLACE TABLE error_table (
  "ORA_ERR_NUMBER$" NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/,
  "ORA_ERR_MESG$" VARCHAR(2000),
  "ORA_ERR_ROWID$" VARCHAR(18) !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - ROWID DATA TYPE CONVERTED TO VARCHAR ***/!!!,
  "ORA_ERR_OPTYP$" VARCHAR(2),
  "ORA_ERR_TAG$" VARCHAR(2000)
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

--departments
CREATE OR REPLACE TABLE parent_table (
      Id   INT PRIMARY KEY,
      Name VARCHAR(10)
  )
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

INSERT INTO parent_table
VALUES (10, 'IT');

INSERT INTO parent_table
VALUES (20, 'HR');

INSERT INTO parent_table
VALUES (30, 'INFRA');

--employees
CREATE OR REPLACE TABLE source_table (
  Id INT PRIMARY KEY,
  Name VARCHAR(20) NOT NULL,
  DepartmentID INT REFERENCES parent_table (Id)
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

INSERT INTO source_table
VALUES (101, 'Anurag111111111', 10);

INSERT INTO source_table
VALUES (102, 'Pranaya11111111', 20);

INSERT INTO source_table
VALUES (103, 'Hina11111111111', 30);

--a copy of source
CREATE OR REPLACE TABLE target_table (
  Id INT PRIMARY KEY,
  Name VARCHAR(10) NOT NULL,
  DepartmentID INT REFERENCES parent_table (Id)
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

INSERT INTO target_table
VALUES (101, 'Anurag', 10);
```

#### 1. FORALL With Collection of Records

##### Oracle 41

###### Note 23

The three cases below have the same transformation to Snowflake Scripting and are functionally
equivalent.

##### Source

```sql
CREATE OR REPLACE PROCEDURE myProcedure IS
    CURSOR cursorVariable IS SELECT * FROM table1;
    TYPE tableType IS TABLE OF cursorVariable%ROWTYPE;
    tableVariable tableType;
BEGIN
    OPEN cursorVariable;
    LOOP
        FETCH cursorVariable BULK COLLECT INTO tableVariable LIMIT 100;
        EXIT WHEN tableVariable.COUNT = 0;

        FORALL forIndex IN 1..tableVariable.COUNT
            INSERT INTO table2 (column1, column2)
            VALUES (tableVariable(forIndex).column1, tableVariable(forIndex).column2);
    END LOOP;
    CLOSE cursorVariable;
END;
```

##### Results 3

<!-- prettier-ignore -->
|COLUMN1|COLUMN2|
|---|---|

```sql
   1| 2|
   1|       2|
   2|       3|
   3|       4|
   4|       5|
   5|       6|
```

##### Snowflake 14

##### FORALL With Collection of Records

```sql
CREATE OR REPLACE PROCEDURE myProcedure ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$

    BEGIN
        --** SSC-PRF-0001 - THIS STATEMENT HAS USAGES OF CURSOR FETCH BULK OPERATIONS **
        --** SSC-PRF-0003 - FETCH INSIDE A LOOP IS CONSIDERED A COMPLEX PATTERN, THIS COULD DEGRADE SNOWFLAKE PERFORMANCE. **
        INSERT INTO table2(column1, column2)
        (
            SELECT
                column1,
                column2
            FROM
                table1
        );
    END;
$$;
```

##### Results 4

<!-- prettier-ignore -->
|COLUMN1|COLUMN2|
|---|---|
|1.000000000000000000|2.000000000000000000|
|1.000000000000000000|2.000000000000000000|
|2.000000000000000000|3.000000000000000000|
|3.000000000000000000|4.000000000000000000|
|4.000000000000000000|5.000000000000000000|
|5.000000000000000000|6.000000000000000000|

###### Note 24

The EWIs SSC-PRF-0001 and SSC-PRF-0003 are added in every FETCH BULK COLLECT occurrence into FORALL
statement.

#### 2. FORALL With INSERT INTO

##### Oracle 42

##### FORALL Example

```sql
CREATE OR REPLACE PROCEDURE myProcedure IS
    CURSOR cursorVariable IS
        SELECT * FROM table1;
    TYPE collectionTypeDefinition IS TABLE OF table1%ROWTYPE;
    collectionVariable collectionTypeDefinition;
BEGIN
    OPEN cursorVariable;
    LOOP
        FETCH cursorVariable BULK COLLECT INTO collectionVariable limit 2;
        EXIT WHEN collectionVariable.COUNT = 0;
        FORALL forIndex IN collectionVariable.FIRST..collectionVariable.LAST
            INSERT INTO table2 VALUES collectionVariable(forIndex);
        collectionVariable.DELETE;
    END LOOP;
    CLOSE cursorVariable;
END;
```

##### Results 5

<!-- prettier-ignore -->
|COLUMN1|COLUMN2|
|---|---|
|1|2|
|1|2|
|2|3|
|3|4|
|4|5|
|5|6|

##### Snowflake 15

##### FORALL Equivalent

```sql
CREATE OR REPLACE PROCEDURE myProcedure ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$

    BEGIN
        --** SSC-PRF-0001 - THIS STATEMENT HAS USAGES OF CURSOR FETCH BULK OPERATIONS **
        --** SSC-PRF-0003 - FETCH INSIDE A LOOP IS CONSIDERED A COMPLEX PATTERN, THIS COULD DEGRADE SNOWFLAKE PERFORMANCE. **
        INSERT INTO table2
        (
            SELECT
                * FROM
                table1
        );
    END;
$$;
```

##### Results 6

<!-- prettier-ignore -->
|COLUMN1|COLUMN2|
|---|---|
|1.000000000000000000|2.000000000000000000|
|1.000000000000000000|2.000000000000000000|
|2.000000000000000000|3.000000000000000000|
|3.000000000000000000|4.000000000000000000|
|4.000000000000000000|5.000000000000000000|
|5.000000000000000000|6.000000000000000000|

#### 3. FORALL With Multiple Fetched Collections

##### Oracle 43

##### With INSERT INTO

```sql
CREATE OR REPLACE PROCEDURE myProcedure IS
    CURSOR cursorVariable IS
        SELECT * FROM table1;
    column1Collection dbms_sql.NUMBER_table;
    column2Collection dbms_sql.NUMBER_table;
BEGIN
    OPEN cursorVariable;
    LOOP
        FETCH cursorVariable BULK COLLECT INTO column1Collection, column2Collection limit 20;
        EXIT WHEN column1Collection.COUNT = 0;
        FORALL forIndex IN 1..column1Collection.COUNT
            INSERT INTO table2 VALUES (
                column1Collection(forIndex),
                column2Collection(forIndex)
            );
    END LOOP;
    CLOSE cursorVariable;
END;
```

##### With UPDATE

```sql
CREATE OR REPLACE PROCEDURE myProcedure IS
    CURSOR cursorVariable IS
        SELECT * FROM table1;
    column1Collection dbms_sql.NUMBER_table;
    column2Collection dbms_sql.NUMBER_table;
BEGIN
    OPEN cursorVariable;
    LOOP
        FETCH cursorVariable BULK COLLECT INTO column1Collection, column2Collection limit 2;
        EXIT WHEN column1Collection.COUNT = 0;
        FORALL forIndex IN 1..column1Collection.COUNT
            UPDATE table2 SET column2 = column2Collection(forIndex)
            WHERE column1 = column1Collection(forIndex);
    END LOOP;
    CLOSE cursorVariable;
END;
```

##### Results INSERT INTO

<!-- prettier-ignore -->
|COLUMN1|COLUMN2|
|---|---|
|1|2|
|2|3|
|3|4|
|4|5|
|5|6|
|1|2|

##### Results UPDATE

<!-- prettier-ignore -->
|COLUMN1|COLUMN2|
|---|---|
|1|2.|

##### Snowflake 16

##### With INSERT INTO 2

```sql
CREATE OR REPLACE PROCEDURE myProcedure ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$

    BEGIN
        --** SSC-PRF-0001 - THIS STATEMENT HAS USAGES OF CURSOR FETCH BULK OPERATIONS **
        --** SSC-PRF-0003 - FETCH INSIDE A LOOP IS CONSIDERED A COMPLEX PATTERN, THIS COULD DEGRADE SNOWFLAKE PERFORMANCE. **
        INSERT INTO table2
        (
            SELECT
                $1,
                $2
            FROM
                table1
        );
    END;
$$;
```

##### With UPDATE 2

```sql
CREATE OR REPLACE PROCEDURE myProcedure ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$

    BEGIN
        --** SSC-PRF-0001 - THIS STATEMENT HAS USAGES OF CURSOR FETCH BULK OPERATIONS **
        --** SSC-PRF-0003 - FETCH INSIDE A LOOP IS CONSIDERED A COMPLEX PATTERN, THIS COULD DEGRADE SNOWFLAKE PERFORMANCE. **
        UPDATE table2
            SET column2 = column1Collection.$2
            FROM
                (
                    SELECT
                        * FROM
                        table1) AS column1Collection
            WHERE
                column1 = column1Collection.$1;
    END;
$$;
```

##### Results INSERT INTO 2

<!-- prettier-ignore -->
|COLUMN1|COLUMN2|
|---|---|
|1.000000000000000000|2.000000000000000000|
|1.000000000000000000|2.000000000000000000|
|2.000000000000000000|3.000000000000000000|
|3.000000000000000000|4.000000000000000000|
|4.000000000000000000|5.000000000000000000|
|5.000000000000000000|6.000000000000000000|

##### Results UPDATE 2

<!-- prettier-ignore -->
|COLUMN1|COLUMN2|
|---|---|
|1.000000000000000000|2.000000000000000000|

#### 4. FORALL With Record of Collections

##### Oracle 44

##### FORALL Example 2

```sql
CREATE OR REPLACE PROCEDURE myProcedure IS
    CURSOR cursorVariable IS
        SELECT * FROM table1;
    TYPE recordType IS RECORD(
        column1Collection dbms_sql.NUMBER_table,
        column2Collection dbms_sql.NUMBER_table
    );
    columnRecord recordType;
BEGIN
    OPEN cursorVariable;
    LOOP
        FETCH cursorVariable BULK COLLECT INTO columnRecord.column1Collection, columnRecord.column2Collection limit 20;
        FORALL forIndex IN 1..columnRecord.column1Collection.COUNT
            INSERT INTO table2 VALUES (
                columnRecord.column1Collection(forIndex),
                columnRecord.column2Collection(forIndex)
            );
        EXIT WHEN cursorVariable%NOTFOUND;
    END LOOP;
    CLOSE cursorVariable;
END;
```

##### Results 7

<!-- prettier-ignore -->
|COLUMN1|COLUMN2|
|---|---|
|1|2|
|1|2|
|2|3|
|3|4|
|4|5|
|5|6|

##### Snowflake 17

##### Scripting FORALL Equivalent

```sql
CREATE OR REPLACE PROCEDURE myProcedure ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$

    BEGIN
        --** SSC-PRF-0001 - THIS STATEMENT HAS USAGES OF CURSOR FETCH BULK OPERATIONS **
        --** SSC-PRF-0003 - FETCH INSIDE A LOOP IS CONSIDERED A COMPLEX PATTERN, THIS COULD DEGRADE SNOWFLAKE PERFORMANCE. **
        INSERT INTO table2
        (
            SELECT
                $1,
                $2
            FROM
                table1
        );
    END;
$$;
```

##### Results 8

<!-- prettier-ignore -->
|COLUMN1|COLUMN2|
|---|---|
|1.000000000000000000|2.000000000000000000|
|1.000000000000000000|2.000000000000000000|
|2.000000000000000000|3.000000000000000000|
|3.000000000000000000|4.000000000000000000|
|4.000000000000000000|5.000000000000000000|
|5.000000000000000000|6.000000000000000000|

#### 5. FORALL With Dynamic SQL

##### Oracle 45

##### FORALL Example 3

```sql
CREATE OR REPLACE PROCEDURE myProcedure IS
    cursorVariable SYS_REFCURSOR;
    TYPE collectionTypeDefinition IS
        TABLE OF table1%ROWTYPE;
    collectionVariable collectionTypeDefinition;
    query VARCHAR(200) := 'SELECT * FROM table1';
BEGIN
    OPEN cursorVariable FOR query;
    LOOP
        FETCH cursorVariable BULK COLLECT INTO collectionVariable;
        EXIT WHEN collectionVariable.COUNT = 0;
        FORALL forIndex IN collectionVariable.FIRST..collectionVariable.LAST
            INSERT INTO table2 VALUES collectionVariable(forIndex);
        collectionVariable.DELETE;
    END LOOP;
    CLOSE cursorVariable;
END;
```

##### Results 9

<!-- prettier-ignore -->
|COLUMN1|COLUMN2|
|---|---|
|1|2|
|1|2|
|2|3|
|3|4|
|4|5|
|5|6|

##### Snowflake 18

##### FORALL Equivalent 2

```sql
CREATE OR REPLACE PROCEDURE myProcedure ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        query VARCHAR(200) := 'SELECT * FROM
   table1';
    BEGIN
        --** SSC-PRF-0001 - THIS STATEMENT HAS USAGES OF CURSOR FETCH BULK OPERATIONS **
        --** SSC-PRF-0003 - FETCH INSIDE A LOOP IS CONSIDERED A COMPLEX PATTERN, THIS COULD DEGRADE SNOWFLAKE PERFORMANCE. **
        !!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!
        EXECUTE IMMEDIATE 'CREATE OR REPLACE TEMPORARY TABLE query AS ' || :query;
        INSERT INTO table2
        (
            SELECT
                *
            FROM
                query
        );
    END;
$$;
```

##### Results 10

<!-- prettier-ignore -->
|COLUMN1|COLUMN2|
|---|---|
|1.000000000000000000|2.000000000000000000|
|1.000000000000000000|2.000000000000000000|
|2.000000000000000000|3.000000000000000000|
|3.000000000000000000|4.000000000000000000|
|4.000000000000000000|5.000000000000000000|
|5.000000000000000000|6.000000000000000000|

#### 6. FORALL With Literal SQL

##### Oracle 46

##### FORALL Example 4

```sql
CREATE OR REPLACE PROCEDURE SampleProcedure
IS
TYPE TabRecType IS RECORD (
    column1 NUMBER,
    column2 NUMBER
);
TYPE tabType IS TABLE OF TabRecType;
cursorRef SYS_REFCURSOR;
tab tabType;
BEGIN
    OPEN cursorRef FOR 'SELECT src.column1, src.column2 FROM ' || 'table1' || ' src';

    LOOP
        BEGIN
            FETCH cursorRef BULK COLLECT INTO tab LIMIT 1000;
            FORALL i IN 1..tab.COUNT
                INSERT INTO table2 (column1, column2)
                VALUES (tab(i).column1, tab(i).column2);

            EXIT WHEN cursorRef%NOTFOUND;
        END;
    END LOOP;

    CLOSE cursorRef;
END;
```

##### Results 11

<!-- prettier-ignore -->
|COLUMN1|COLUMN2|
|---|---|
|1|2|
|1|2|
|2|3|
|3|4|
|4|5|
|5|6|

##### Snowflake 19

##### FORALL Equivalent 3

```sql
CREATE OR REPLACE PROCEDURE SampleProcedure ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$

    BEGIN
        EXECUTE IMMEDIATE 'CREATE OR REPLACE TEMPORARY TABLE cursorRef_TEMP_TABLE AS ' || 'SELECT src.column1, src.column2 FROM ' || 'table1' || ' src';
        --** SSC-PRF-0001 - THIS STATEMENT HAS USAGES OF CURSOR FETCH BULK OPERATIONS **
        --** SSC-PRF-0003 - FETCH INSIDE A LOOP IS CONSIDERED A COMPLEX PATTERN, THIS COULD DEGRADE SNOWFLAKE PERFORMANCE. **
        INSERT INTO table2(column1, column2)
        (
            SELECT
                *
            FROM
                cursorRef_TEMP_TABLE
        );
    END;
$$;
```

##### Results 12

<!-- prettier-ignore -->
|COLUMN1|COLUMN2|
|---|---|
|1|2|
|1|2|
|2|3|
|3|4|
|4|5|
|5|6|

#### 7. FORALL With Parametrized Cursors

##### Oracle 47

##### FORALL Example 5

```sql
CREATE OR REPLACE PROCEDURE myProcedure IS
    intVariable INTEGER := 7;
    CURSOR cursorVariable(param1 INTEGER, param2 INTEGER default 5) IS
        SELECT * FROM table1
        WHERE
            column2 = intVariable OR
            column1 BETWEEN param1 AND param2;
    TYPE collectionTypeDefinition IS
        TABLE OF table1%ROWTYPE;
    collectionVariable collectionTypeDefinition;
BEGIN
    OPEN cursorVariable(1);
    LOOP
        FETCH cursorVariable BULK COLLECT INTO collectionVariable limit 20;
        EXIT WHEN collectionVariable.COUNT = 0;
        FORALL forIndex IN collectionVariable.FIRST..collectionVariable.LAST
            INSERT INTO table2 VALUES collectionVariable(forIndex);
        collectionVariable.DELETE;
    END LOOP;
    CLOSE cursorVariable;
END;
```

##### Results 13

<!-- prettier-ignore -->
|COLUMN1|COLUMN2|
|---|---|
|1|2|
|1|2|
|2|3|
|3|4|
|4|5|
|5|6|

##### Snowflake 20

##### FORALL Equivalent 4

```sql
CREATE OR REPLACE PROCEDURE myProcedure ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        intVariable INTEGER := 7;
    BEGIN
        --** SSC-PRF-0001 - THIS STATEMENT HAS USAGES OF CURSOR FETCH BULK OPERATIONS **
        --** SSC-PRF-0003 - FETCH INSIDE A LOOP IS CONSIDERED A COMPLEX PATTERN, THIS COULD DEGRADE SNOWFLAKE PERFORMANCE. **
        INSERT INTO table2
        (
            SELECT
                * FROM
                table1
                   WHERE
                       column2 = :intVariable
                OR
                       column1 BETWEEN 1 AND 5
        );
    END;
$$;
```

##### Results 14

<!-- prettier-ignore -->
|COLUMN1|COLUMN2|
|---|---|
|1|2|
|1|2|
|2|3|
|3|4|
|4|5|
|5|6|

#### 8. FORALL Without LOOPS

##### Oracle 48

##### FORALL Example 6

```sql
CREATE OR REPLACE PROCEDURE  myProcedure IS
    TYPE collectionTypeDefinition IS TABLE OF table1%ROWTYPE;
    collectionVariable collectionTypeDefinition;
BEGIN
    SELECT * BULK COLLECT INTO collectionVariable FROM table1;
        FORALL forIndex IN 1..collectionVariable.COUNT
            INSERT INTO table2 VALUES (
                collectionVariable (forIndex).column1,
                collectionVariable (forIndex).column2
            );
        collectionVariable.DELETE;
END;
```

##### Results 15

<!-- prettier-ignore -->
|COLUMN1|COLUMN2|
|---|---|
|1|2|
|1|2|
|2|3|
|3|4|
|4|5|
|5|6|

##### Snowflake 21

##### FORALL Equivalent 5

```sql
CREATE OR REPLACE PROCEDURE myProcedure ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$

    BEGIN
        --** SSC-PRF-0003 - FETCH INSIDE A LOOP IS CONSIDERED A COMPLEX PATTERN, THIS COULD DEGRADE SNOWFLAKE PERFORMANCE. **
        INSERT INTO table2
        (
            SELECT
                column1,
                column2
            FROM
                table1
        );
    END;
$$;
```

##### Results 16

<!-- prettier-ignore -->
|COLUMN1|COLUMN2|
|---|---|
|1.000000000000000000|2.000000000000000000|
|1.000000000000000000|2.000000000000000000|
|2.000000000000000000|3.000000000000000000|
|3.000000000000000000|4.000000000000000000|
|4.000000000000000000|5.000000000000000000|
|5.000000000000000000|6.000000000000000000|

#### 9. FORALL With UPDATE Statements

##### Oracle 49

##### FORALL Example 7

```sql
CREATE OR REPLACE PROCEDURE myProcedure IS
    CURSOR cursorVariable IS
        SELECT * FROM table1;
    TYPE collectionTypeDefinition IS TABLE OF table1%ROWTYPE;
    collectionVariable collectionTypeDefinition;
BEGIN
    OPEN cursorVariable;
    LOOP
        FETCH cursorVariable BULK COLLECT INTO collectionVariable limit 2;
        EXIT WHEN collectionVariable.COUNT = 0;
        FORALL forIndex IN collectionVariable.FIRST..collectionVariable.LAST
            UPDATE table2 SET column1 = '54321' WHERE column2 = collectionVariable(forIndex).column2;
        collectionVariable.DELETE;
    END LOOP;
    CLOSE cursorVariable;
END;
```

##### Results 17

<!-- prettier-ignore -->
|COLUMN1|COLUMN2|
|---|---|
|54321|2|

##### Snowflake 22

##### FORALL Equivalent 6

```sql
CREATE OR REPLACE PROCEDURE myProcedure ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$

    BEGIN
        --** SSC-PRF-0001 - THIS STATEMENT HAS USAGES OF CURSOR FETCH BULK OPERATIONS **
        --** SSC-PRF-0003 - FETCH INSIDE A LOOP IS CONSIDERED A COMPLEX PATTERN, THIS COULD DEGRADE SNOWFLAKE PERFORMANCE. **
        UPDATE table2
            SET column1 = '54321'
            FROM
                (
                    SELECT
                        * FROM
                        table1) AS collectionVariable
            WHERE
                column2 = collectionVariable.column2;
    END;
$$;
```

##### Results 18

<!-- prettier-ignore -->
|COLUMN1|COLUMN2|
|---|---|
|54321|2|

#### 10. FORALL With DELETE Statements

##### Oracle 50

##### FORALL Example 8

```sql
CREATE OR REPLACE PROCEDURE myProcedure IS
    CURSOR cursorVariable IS
        SELECT * FROM table1;
    TYPE collectionTypeDefinition IS TABLE OF table1%ROWTYPE;
    collectionVariable collectionTypeDefinition;
BEGIN
    OPEN cursorVariable;
    LOOP
        FETCH cursorVariable BULK COLLECT INTO collectionVariable limit 2;
        EXIT WHEN collectionVariable.COUNT = 0;
        FORALL forIndex IN collectionVariable.FIRST..collectionVariable.LAST
            DELETE FROM table2 WHERE column2 = collectionVariable(forIndex).column2;
        collectionVariable.DELETE;
    END LOOP;
    CLOSE cursorVariable;
END;
```

##### Results 19

```sql
no data found
```

##### Snowflake 23

##### FORALL Equivalent 7

```sql
CREATE OR REPLACE PROCEDURE myProcedure ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$

    BEGIN
        --** SSC-PRF-0001 - THIS STATEMENT HAS USAGES OF CURSOR FETCH BULK OPERATIONS **
        --** SSC-PRF-0003 - FETCH INSIDE A LOOP IS CONSIDERED A COMPLEX PATTERN, THIS COULD DEGRADE SNOWFLAKE PERFORMANCE. **
        DELETE FROM
            table2
        USING (
            SELECT
                * FROM
                table1) collectionVariable
                WHERE
            table2.column2 = collectionVariable.column2;
    END;
$$;
```

##### Results 20

```sql
Query produced no results
```

#### 11. FORALL With PACKAGE References

##### Oracle 51

##### FORALL Example 9

```sql
CREATE OR REPLACE PACKAGE MyPackage AS
    TYPE collectionTypeDefinition IS
        TABLE OF table1%ROWTYPE;
    collectionVariable collectionTypeDefinition;
END;
/

CREATE OR REPLACE PROCEDURE InsertIntoPackage(param integer) IS
BEGIN
    SELECT
        param,
        param BULK COLLECT INTO MyPackage.collectionVariable
    FROM
        DUAL;
END;
/

CREATE OR REPLACE PROCEDURE InsertUsingPackage IS
BEGIN
        FORALL forIndex IN MyPackage.collectionVariable.FIRST..MyPackage.collectionVariable.LAST
            INSERT INTO table2 VALUES MyPackage.collectionVariable(forIndex);
        MyPackage.collectionVariable.DELETE;
END;
/

DECLARE
    param_value INTEGER := 10;
BEGIN
    InsertIntoPackage(param_value);
    InsertUsingPackage;
END;

select * from table2;
```

##### Results 21

<!-- prettier-ignore -->
|COLUMN1|COLUMN2|
|---|---|
|1|2|
|10|10|

##### Snowflake 24

##### FORALL Equivalent 8

```sql
CREATE SCHEMA IF NOT EXISTS MyPackage
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

!!!RESOLVE EWI!!! /*** SSC-EWI-OR0049 - PACKAGE TYPE DEFINITIONS in stateful package MyPackage are not supported yet ***/!!!
TYPE collectionTypeDefinition IS
    TABLE OF table1%ROWTYPE;

CREATE OR REPLACE TEMPORARY TABLE MYPACKAGE_COLLECTIONVARIABLE (
);

CREATE OR REPLACE PROCEDURE InsertIntoPackage (param integer)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        DELETE FROM
            MYPACKAGE_COLLECTIONVARIABLE;
        INSERT INTO MYPACKAGE_COLLECTIONVARIABLE
        (
            SELECT
                :param,
                :param
            FROM
        DUAL
        );
    END;
$$;

CREATE OR REPLACE PROCEDURE InsertUsingPackage ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$

    BEGIN
        --** SSC-PRF-0003 - FETCH INSIDE A LOOP IS CONSIDERED A COMPLEX PATTERN, THIS COULD DEGRADE SNOWFLAKE PERFORMANCE. **
        INSERT INTO table2
        (
            SELECT
                *
            FROM
                MYPACKAGE_COLLECTIONVARIABLE
        );
    END;
$$;

DECLARE
    param_value INTEGER := 10;
    call_results VARIANT;
BEGIN
    CALL
    InsertIntoPackage(:param_value);
    CALL
    InsertUsingPackage();
    RETURN call_results;
END;

select * from
    table2;
```

##### Results 22

<!-- prettier-ignore -->
|COLUMN1|COLUMN2|
|---|---|
|1.000000000000000000|2.000000000000000000|
|10.000000000000000000|10.000000000000000000|

Warning

The transformation above only works if the variable defined in the package is a record of
collections.

#### 12. FORALL With MERGE Statements

##### Oracle 52

##### FORALL Example 10

```sql
CREATE OR REPLACE PROCEDURE myProcedure IS
    CURSOR cursorVariable IS
        SELECT * FROM table1;
    TYPE collectionTypeDefinition IS
        TABLE OF table1%ROWTYPE;
    collectionVariable collectionTypeDefinition;
BEGIN
    OPEN cursorVariable;
    LOOP
        FETCH cursorVariable BULK COLLECT INTO collectionVariable limit 2;
        EXIT WHEN collectionVariable.COUNT = 0;
        FORALL forIndex IN collectionVariable.FIRST..collectionVariable.LAST
        MERGE INTO table2 tgt
            USING (
                SELECT
                    collectionVariable(forIndex).column1 column1,
                    collectionVariable(forIndex).column2 column2
                FROM DUAL
            ) src
           ON (tgt.column1 = src.column1)
        WHEN MATCHED THEN
            UPDATE SET
               tgt.column2 = src.column2 * 2
        WHEN NOT MATCHED THEN
            INSERT (column1, column2)
            VALUES (src.column1, src.column2);
    END LOOP;
    CLOSE cursorVariable;
END;
```

##### Results 23

<!-- prettier-ignore -->
|COLUMN1|COLUMN2|
|---|---|
|1|4|
|2|3|
|3|4|
|4|5|
|5|6|

##### Snowflake 25

##### FORALL Equivalent 9

```sql
CREATE OR REPLACE PROCEDURE myProcedure ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$

    BEGIN
        --** SSC-PRF-0001 - THIS STATEMENT HAS USAGES OF CURSOR FETCH BULK OPERATIONS **
        --** SSC-PRF-0003 - FETCH INSIDE A LOOP IS CONSIDERED A COMPLEX PATTERN, THIS COULD DEGRADE SNOWFLAKE PERFORMANCE. **
        MERGE INTO table2 tgt
            USING (
                SELECT
                    collectionVariable.column1 column1,
                    collectionVariable.column2 column2
                FROM
                    (
                        SELECT
                            * FROM
                            table1
                    ) collectionVariable
            ) src
           ON (tgt.column1 = src.column1)
        WHEN MATCHED THEN
            UPDATE SET
               tgt.column2 = src.column2 * 2
        WHEN NOT MATCHED THEN
            INSERT (column1, column2)
            VALUES (src.column1, src.column2);
    END;
$$;
```

##### Results 24

<!-- prettier-ignore -->
|COLUMN1|COLUMN2|
|---|---|
|2.000000000000000000|3.000000000000000000|
|3.000000000000000000|4.000000000000000000|
|4.000000000000000000|5.000000000000000000|
|5.000000000000000000|6.000000000000000000|
|1.000000000000000000|4.000000000000000000|

Warning

The transformation above only works if the `SELECT` statement inside the `MERGE` is selecting from
`DUAL` table.

#### 13. Default FORALL transformation

##### Note 25

You might also be interested in [Bulk Cursor Helpers](helpers.html#bulk-cursor-helpers).

##### Oracle 53

##### FORALL Example 11

```sql
CREATE OR REPLACE PROCEDURE myProcedure IS
    CURSOR cursorVariable IS SELECT * FROM table1;
    TYPE columnsRecordType IS RECORD (column1 dbms_sql.NUMBER_table, column2 dbms_sql.NUMBER_table);
    recordVariable columnsRecordType;
    TYPE collectionTypeDefinition IS TABLE OF table1%ROWTYPE;
    collectionVariable collectionTypeDefinition;
    col1 dbms_sql.NUMBER_table;
    col2 dbms_sql.NUMBER_table;
BEGIN
    OPEN cursorVariable;
    FETCH cursorVariable BULK COLLECT INTO collectionVariable limit 2;
    FORALL forIndex IN collectionVariable.FIRST..collectionVariable.LAST
        INSERT INTO table2 (column1, column2)
        VALUES (collectionVariable(forIndex).column1, collectionVariable(forIndex).column2);

    FETCH cursorVariable BULK COLLECT INTO col1, col2 limit 2;
    FORALL forIndex IN col1.FIRST..col1.LAST
        INSERT INTO table2 (column1, column2)
        VALUES (col1(forIndex), col2(forIndex));

    LOOP
        FETCH cursorVariable BULK COLLECT INTO recordVariable limit 2;
        EXIT WHEN recordVariable.column1.COUNT = 0;
        FORALL forIndex IN recordVariable.column1.FIRST..recordVariable.column1.LAST
            INSERT INTO table2 (column1, column2)
            VALUES (recordVariable.column1(forIndex), recordVariable.column2(forIndex));
    END LOOP;
    CLOSE cursorVariable;
END;
```

##### Results 25

<!-- prettier-ignore -->
|COLUMN1|COLUMN2|
|---|---|
|1|2|
|1|2|
|2|3|
|3|4|
|4|5|
|5|6|

##### Snowflake 26

##### FORALL Equivalent 10

```sql
--** SSC-FDM-0007 - MISSING DEPENDENT OBJECTS "table1", "table2" **
CREATE OR REPLACE PROCEDURE myProcedure ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        cursorVariable OBJECT := INIT_CURSOR_UDF('cursorVariable', '   SELECT * FROM
      table1');
        !!!RESOLVE EWI!!! /*** SSC-EWI-0056 - CUSTOM TYPES ARE NOT SUPPORTED IN SNOWFLAKE BUT REFERENCES TO THIS CUSTOM TYPE WERE CHANGED TO OBJECT ***/!!!
           TYPE columnsRecordType IS RECORD (column1 dbms_sql.NUMBER_table, column2 dbms_sql.NUMBER_table);
           recordVariable OBJECT !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - columnsRecordType DATA TYPE CONVERTED TO OBJECT ***/!!! := OBJECT_CONSTRUCT();
--        !!!RESOLVE EWI!!! /*** SSC-EWI-0058 - FUNCTIONALITY FOR 'PL COLLECTION TYPE DEFINITION' IS NOT CURRENTLY SUPPORTED BY SNOWFLAKE SCRIPTING ***/!!!
--           TYPE collectionTypeDefinition IS TABLE OF table1%ROWTYPE;
           collectionVariable VARIANT !!!RESOLVE EWI!!! /*** SSC-EWI-0062 - CUSTOM TYPE 'collectionTypeDefinition' USAGE CHANGED TO VARIANT ***/!!!;
           col1 VARIANT /*** SSC-FDM-0015 - REFERENCED CUSTOM TYPE 'dbms_sql.NUMBER_table' IN QUERY NOT FOUND, USAGES MAY BE AFFECTED ***/;
           col2 VARIANT /*** SSC-FDM-0015 - REFERENCED CUSTOM TYPE 'dbms_sql.NUMBER_table' IN QUERY NOT FOUND, USAGES MAY BE AFFECTED ***/;
        FORALL INTEGER;
    BEGIN
        cursorVariable := (
            CALL OPEN_BULK_CURSOR_UDF(:cursorVariable)
        );
        --** SSC-PRF-0001 - THIS STATEMENT HAS USAGES OF CURSOR FETCH BULK OPERATIONS **
        cursorVariable := (
            CALL FETCH_BULK_COLLECTION_RECORDS_UDF(:cursorVariable, 2)
        );
        collectionVariable := :cursorVariable:RESULT;
        FORALL := ARRAY_SIZE(:collectionVariable);
        INSERT INTO table2(column1, column2)
        (
            SELECT
                :collectionVariable[forIndex]:column1,
                : collectionVariable[forIndex]:column2
            FROM
                (
                    SELECT
                        seq4() AS forIndex
                    FROM
                        TABLE(GENERATOR(ROWCOUNT => :FORALL))
                )
        );
        --** SSC-PRF-0001 - THIS STATEMENT HAS USAGES OF CURSOR FETCH BULK OPERATIONS **
        cursorVariable := (
            CALL FETCH_BULK_COLLECTIONS_UDF(:cursorVariable, 2)
        );
        col1 := :cursorVariable:RESULT[0];
        col2 := :cursorVariable:RESULT[1];
        FORALL := ARRAY_SIZE(:col1);
        INSERT INTO table2(column1, column2)
        (
            SELECT
                :col1[forIndex],
                : col2[forIndex]
            FROM
                (
                    SELECT
                        seq4() AS forIndex
                    FROM
                        TABLE(GENERATOR(ROWCOUNT => :FORALL))
                )
        );
        --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **

        LOOP
            --** SSC-PRF-0003 - FETCH INSIDE A LOOP IS CONSIDERED A COMPLEX PATTERN, THIS COULD DEGRADE SNOWFLAKE PERFORMANCE. **
            --** SSC-PRF-0001 - THIS STATEMENT HAS USAGES OF CURSOR FETCH BULK OPERATIONS **
            cursorVariable := (
                CALL FETCH_BULK_RECORD_COLLECTIONS_UDF(:cursorVariable, 2)
            );
            recordVariable := :cursorVariable:RESULT;
            IF (ARRAY_SIZE(:recordVariable:column1) = 0) THEN
                EXIT;
            END IF;
            FORALL := ARRAY_SIZE(:recordVariable:column1);
            INSERT INTO table2(column1, column2)
            (
                SELECT
                    :recordVariable:column1[forIndex],
                    : recordVariable:column2[forIndex]
                FROM
                    (
                        SELECT
                            seq4() AS forIndex
                        FROM
                            TABLE(GENERATOR(ROWCOUNT => :FORALL))
                    )
            );
        END LOOP;
        cursorVariable := (
            CALL CLOSE_BULK_CURSOR_UDF(:cursorVariable)
        );
    END;
$$;
```

##### Results 26

<!-- prettier-ignore -->
|COLUMN1|COLUMN2|
|---|---|
|1.000000000000000000|2.000000000000000000|
|1.000000000000000000|2.000000000000000000|
|2.000000000000000000|3.000000000000000000|
|3.000000000000000000|4.000000000000000000|
|4.000000000000000000|5.000000000000000000|
|5.000000000000000000|6.000000000000000000|

###### Note 26

This transformation is done only when none of the previously mentioned transformations can be done.

#### 14. Multiple FORALL inside a LOOP clause

##### Note 27

This pattern applies when there is more than one FORALL in the same procedure and it meets the
following structure.

##### Oracle 54

##### FORALL Example 12

```sql
CREATE OR REPLACE PROCEDURE myProcedure IS
    CURSOR cursorVariable IS
        SELECT * FROM table1;

    TYPE collectionTypeDefinition IS TABLE OF table1%ROWTYPE;
    collectionVariable collectionTypeDefinition;
BEGIN
    OPEN cursorVariable;
    LOOP
        FETCH cursorVariable BULK COLLECT INTO collectionVariable limit 20;
        EXIT WHEN collectionVariable.COUNT = 0;

        FORALL forIndex IN collectionVariable.FIRST..collectionVariable.LAST
            INSERT INTO table2 VALUES collectionVariable(forIndex);

        FORALL forIndex IN collectionVariable.FIRST..collectionVariable.LAST
            UPDATE table2 SET column1 = '54321' WHERE column2 = collectionVariable(forIndex).column2;

    END LOOP;
    CLOSE cursorVariable;
END;
```

##### Results 27

<!-- prettier-ignore -->
|COLUMN1|COLUMN2|
|---|---|
|54321|2|
|54321|2|
|54321|3|
|54321|4|
|54321|5|
|54321|6|

##### Snowflake 27

##### FORALL Equivalent 11

```sql
CREATE OR REPLACE PROCEDURE myProcedure ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$

    BEGIN
        --** SSC-PRF-0001 - THIS STATEMENT HAS USAGES OF CURSOR FETCH BULK OPERATIONS **
        --** SSC-PRF-0003 - FETCH INSIDE A LOOP IS CONSIDERED A COMPLEX PATTERN, THIS COULD DEGRADE SNOWFLAKE PERFORMANCE. **
        INSERT INTO table2
        (
            SELECT
                * FROM
                table1
        );
        --** SSC-PRF-0003 - FETCH INSIDE A LOOP IS CONSIDERED A COMPLEX PATTERN, THIS COULD DEGRADE SNOWFLAKE PERFORMANCE. **
        UPDATE table2
            SET column1 = '54321'
            FROM
                (
                    SELECT
                        * FROM
                        table1) AS collectionVariable
            WHERE
                column2 = collectionVariable.column2;
    END;
$$;
```

##### Results 28

<!-- prettier-ignore -->
|COLUMN1|COLUMN2|
|---|---|
|54321|2|
|54321|2|
|54321|3|
|54321|4|
|54321|5|
|54321|6|

#### 15. Multiple FORALL inside different LOOP clauses

##### Note 28

This pattern applies when there is more than one FORALL in the same procedure and it meets the
following structure.

##### Oracle 55

##### FORALL Example 13

```sql
CREATE OR REPLACE PROCEDURE myProcedure IS
    CURSOR cursorVariable IS
        SELECT * FROM table1;

    CURSOR cursorVariable2 IS
        SELECT * FROM table1;

    TYPE collectionTypeDefinition IS
        TABLE OF table1%ROWTYPE;
    collectionVariable collectionTypeDefinition;

    TYPE collectionTypeDefinition2 IS
        TABLE OF table1%ROWTYPE;
    collectionVariable2 collectionTypeDefinition2;
BEGIN
    OPEN cursorVariable;
    LOOP
        FETCH cursorVariable BULK COLLECT INTO collectionVariable limit 2;
        EXIT WHEN collectionVariable.COUNT = 0;
        FORALL forIndex IN collectionVariable.FIRST..collectionVariable.LAST
            INSERT INTO table2 VALUES collectionVariable(forIndex);
    END LOOP;
    CLOSE cursorVariable;

    OPEN cursorVariable2;
    LOOP
        FETCH cursorVariable2 BULK COLLECT INTO collectionVariable2 limit 2;
        EXIT WHEN collectionVariable2.COUNT = 0;
        FORALL forIndex IN collectionVariable2.FIRST..collectionVariable2.LAST
            UPDATE table2 SET column1 = '54321' WHERE column2 = collectionVariable2(forIndex).column2;
    END LOOP;
    CLOSE cursorVariable2;
END;
```

##### Results 29

<!-- prettier-ignore -->
|COLUMN1|COLUMN2|
|---|---|
|54321|2|
|54321|2|
|54321|3|
|54321|4|
|54321|5|
|54321|6|

##### Snowflake 28

##### FORALL Equivalent 12

```sql
CREATE OR REPLACE PROCEDURE myProcedure ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$

    BEGIN
        --** SSC-PRF-0001 - THIS STATEMENT HAS USAGES OF CURSOR FETCH BULK OPERATIONS **
        --** SSC-PRF-0003 - FETCH INSIDE A LOOP IS CONSIDERED A COMPLEX PATTERN, THIS COULD DEGRADE SNOWFLAKE PERFORMANCE. **
        INSERT INTO table2
        (
            SELECT
                * FROM
                table1
        );
        --** SSC-PRF-0001 - THIS STATEMENT HAS USAGES OF CURSOR FETCH BULK OPERATIONS **
        --** SSC-PRF-0003 - FETCH INSIDE A LOOP IS CONSIDERED A COMPLEX PATTERN, THIS COULD DEGRADE SNOWFLAKE PERFORMANCE. **
        UPDATE table2
            SET column1 = '54321'
            FROM
                (
                    SELECT
                        * FROM
                        table1) AS collectionVariable2
            WHERE
                column2 = collectionVariable2.column2;
    END;
$$;
```

##### Results 30

<!-- prettier-ignore -->
|COLUMN1|COLUMN2|
|---|---|
|54321|2|
|54321|2|
|54321|3|
|54321|4|
|54321|5|
|54321|6|

#### 16. FORALL with MERGE INTO with LOG ERRORS

Warning

This pattern is not yet implemmented

##### Oracle 56

##### LOG ERRORS

```sql
CREATE OR REPLACE PROCEDURE procedure_example (
    department_id_in   IN source_table.DepartmentID%TYPE)
IS
    TYPE employee_ids_t IS TABLE OF source_table%ROWTYPE
    INDEX BY PLS_INTEGER;
    employee_list   employee_ids_t;
BEGIN
    SELECT *
        BULK COLLECT INTO employee_list
        FROM source_table
        WHERE DepartmentID = procedure_example.department_id_in;

    FORALL indx IN 1 .. employee_list.COUNT
      MERGE INTO target_table
      USING (SELECT * FROM DUAL) src
      ON (id = employee_list(indx).id)
      WHEN MATCHED THEN
        UPDATE SET
          name = employee_list(indx).Name
      WHEN NOT MATCHED THEN
        INSERT (Id, Name, DepartmentID)
        VALUES (employee_list(indx).Id, employee_list(indx).Name, employee_list(indx).DepartmentID)
      LOG ERRORS INTO error_table('MERGE INTO ERROR')
      REJECT LIMIT UNLIMITED;

END;

CALL procedure_example(10);

select * from target_table;
select * from error_table;
```

##### Snowflake 29

##### LOG ERRORS 2

```sql
--Generated by SnowConvert---------------
CREATE OR REPLACE TRANSIENT TABLE target_staging_table(
  Id INT PRIMARY KEY,
  Name VARCHAR2(10) NOT NULL,
  DepartmentID INT REFERENCES parent_table(Id)
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;
--Generated by SnowConvert---------------

CREATE OR REPLACE PROCEDURE procedure_example (DEPARTMENT_ID_IN INT !!!RESOLVE EWI!!! /*** SSC-EWI-OR0129 - TYPE ATTRIBUTE 'source_table.DepartmentID%TYPE' COULD NOT BE RESOLVED, SO IT WAS TRANSFORMED TO VARIANT ***/!!!)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        CREATE OR REPLACE TEMP TABLE SOURCE_TEMPORAL AS
        WITH source_data as (
            SELECT *
            FROM source_table
            WHERE DEPARTMENTID =: DEPARTMENT_ID_IN
        )
        SELECT source_data.*, parent_table.id as PARENT_KEY
        FROM source_data
        left join parent_table on source_data.DepartmentID = parent_table.id;

        --All records violating foreign key integrity
        INSERT INTO error_table (ERROR, COLUMN_NAME, REJECTED_RECORD)
        SELECT
            'Foreign Key Constraint Violated' ERROR,'KEY_COL' COLUMN_NAME, id
        FROM SOURCE_TEMPORAL
        WHERE PARENT_KEY IS NULL;

        DELETE FROM SOURCE_TEMPORAL
        WHERE PARENT_KEY IS NULL;

        BEGIN
            MERGE INTO target_table
            USING SOURCE_TEMPORAL SRC
            ON SRC.id = target_table.id
            WHEN MATCHED THEN
                UPDATE SET
                    name = SRC.name
            WHEN NOT MATCHED THEN
               INSERT (Id, Name, DepartmentID)
               VALUES (SRC.Id, SRC.Name, SRC.DepartmentID);
        EXCEPTION
            WHEN OTHER THEN
                CREATE OR REPLACE TEMPORARY STAGE my_int_stage
                  COPY_OPTIONS = (ON_ERROR='continue');

                --Create my file and populate with data
                COPY INTO @my_int_stage/my_file FROM (
                SELECT  * exclude(PARENT_KEY) FROM SOURCE_TEMPORAL
                ) OVERWRITE = TRUE ;

                COPY INTO target_staging_table(id, name, DepartmentID)
                FROM (
                  SELECT
                    -- distinct
                    t.$1, t.$2, t.$3
                  FROM @my_int_stage/my_file t
                  ) ON_ERROR = CONTINUE;

                INSERT INTO ERROR_TABLE (ERROR, FILE, LINE, CHARACTER, CATEGORY, CODE, SQL_STATE, COLUMN_NAME, ROW_NUMBER, REJECTED_RECORD)
                SELECT
                    ERROR, FILE,LINE, CHARACTER, CATEGORY, CODE, SQL_STATE, COLUMN_NAME, ROW_NUMBER, REJECTED_RECORD
                FROM TABLE(VALIDATE(target_staging_table, JOB_ID => '_last')) order by line; --The last charge on the current session

                MERGE INTO target_table
                USING target_staging_table staging
                ON staging.id = target_table.id
                WHEN MATCHED THEN
                    UPDATE SET
                        name = staging.name
                WHEN NOT MATCHED THEN
                INSERT (Id, Name, DepartmentID)
                VALUES (staging.Id, staging.Name, staging.DepartmentID);
        END;

        return 'Awesome!';
    END;
$$;

CALL procedure_example(10);

SELECT * FROM target_table;
SELECT * FROM error_table;
```

#### 17. FORALL with INSERT with LOG ERRORS

Warning

This pattern is not yet implemmented

##### Oracle 57

##### LOG ERRORS 3

```sql
CREATE OR REPLACE PROCEDURE procedure_example (
    department_id_in   IN source_table.DepartmentID%TYPE)
IS
    TYPE employee_ids_t IS TABLE OF source_table%ROWTYPE
    INDEX BY PLS_INTEGER;
    employee_list   employee_ids_t;
BEGIN
    SELECT *
        BULK COLLECT INTO employee_list
        FROM source_table
        WHERE DepartmentID = procedure_example.department_id_in;

    FORALL indx IN 1 .. employee_list.COUNT
        INSERT INTO target_table(Id, Name, DepartmentID)
        VALUES (employee_list(indx).Id, employee_list(indx).Name, employee_list(indx).DepartmentID)
        LOG ERRORS INTO error_table('MERGE INTO ERROR')
        REJECT LIMIT UNLIMITED;
END;
```

##### Snowflake 30

##### LOG ERRORS 4

```sql
--Generated by SnowConvert---------------
CREATE OR REPLACE TRANSIENT TABLE target_staging_table(
  Id INT PRIMARY KEY,
  Name VARCHAR2(10) NOT NULL,
  DepartmentID INT REFERENCES parent_table(Id)
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;
--Generated by SnowConvert---------------

CREATE OR REPLACE PROCEDURE procedure_example (DEPARTMENT_ID_IN INT !!!RESOLVE EWI!!! /*** SSC-EWI-OR0129 - TYPE ATTRIBUTE 'employees.DepartmentID%TYPE' COULD NOT BE RESOLVED, SO IT WAS TRANSFORMED TO VARIANT ***/!!!)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        CREATE OR REPLACE TEMP TABLE SOURCE_TEMPORAL AS
        WITH source_data as (
            SELECT *
            FROM source_table
            WHERE DEPARTMENTID =: DEPARTMENT_ID_IN
        )
        SELECT source_data.*, parent_table.id as PARENT_KEY
        FROM source_data
        left join parent_table on source_data.DepartmentID = parent_table.id;

        --All records violating foreign key integrity
        INSERT INTO error_table (ERROR, COLUMN_NAME, REJECTED_RECORD)
        SELECT
            'Foreign Key Constraint Violated' ERROR,'KEY_COL' COLUMN_NAME, id
        FROM SOURCE_TEMPORAL
        WHERE PARENT_KEY IS NULL;

        DELETE FROM SOURCE_TEMPORAL
        WHERE PARENT_KEY IS NULL;

        BEGIN
            INSERT INTO target_table (Id, Name, DepartmentID)
            SELECT SRC.Id, SRC.Name, SRC.DepartmentID FROM SOURCE_TEMPORAL SRC;
        EXCEPTION
            WHEN OTHER THEN
                CREATE OR REPLACE TEMPORARY STAGE my_int_stage
                  COPY_OPTIONS = (ON_ERROR='continue');

                --Create my file and populate with data
                COPY INTO @my_int_stage/my_file FROM (
                SELECT  * exclude(PARENT_KEY) FROM SOURCE_TEMPORAL
                ) OVERWRITE = TRUE ;

                COPY INTO target_staging_table(id, name, DepartmentID)
                FROM (
                  SELECT
                    -- distinct
                    t.$1, t.$2, t.$3
                  FROM @my_int_stage/my_file t
                  ) ON_ERROR = CONTINUE;

                INSERT INTO ERROR_TABLE (ERROR, FILE, LINE, CHARACTER, CATEGORY, CODE, SQL_STATE, COLUMN_NAME, ROW_NUMBER, REJECTED_RECORD)
                SELECT
                    ERROR, FILE,LINE, CHARACTER, CATEGORY, CODE, SQL_STATE, COLUMN_NAME, ROW_NUMBER, REJECTED_RECORD
                FROM TABLE(VALIDATE(target_staging_table, JOB_ID => '_last')) order by line; --The last charge on the current session

                INSERT INTO target_table (Id, Name, DepartmentID)
                SELECT staging.Id, staging.Name, staging.DepartmentID FROM target_staging_table staging;
        END;
    END;
$$;

CALL procedure_example(10);

SELECT * FROM target_table;
SELECT * FROM error_table;
```

### Known Issues 11

No issues were found.

### Related EWIs 11

1. [SSC-EWI-0030](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0030):
   The statement below has usages of dynamic SQL.
2. [SSC-EWI-0036](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0036):
   Data type converted to another data type.
3. [SSC-EWI-0056](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0056):
   Create Type Not Supported.
4. [SSC-EWI-0058](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0058):
   Functionality is not currently supported by Snowflake Scripting.
5. [SSC-EWI-0062](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0062):
   Custom type usage changed to variant.
6. [SSC-EWI-OR0049](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI#ssc-ewi-or0049):
   Package constants in stateful package are not supported yet.
7. [SSC-FDM-0006](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0006):
   Number type column may not behave similarly in Snowflake.
8. [SSC-FDM-0015:](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0015)
   ​Referenced custom type in query not found.
9. [SSC-PRF-0001](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/performance-review/generalPRF#ssc-prf-0001):
   This statement has usages of cursor fetch bulk operations.
10. [SSC-PRF-0003](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/performance-review/generalPRF#ssc-prf-0003):
    Fetch inside a loop is considered a complex pattern, this could degrade Snowflake performance.

## IF

### Description 12

The `IF` statement either runs or skips a sequence of one or more statements, depending on the value
of a `BOOLEAN` expression. For more information regarding Oracle IF, check
[here](https://docs.oracle.com/en/database/oracle/oracle-database/21/lnpls/IF-statement.html#GUID-B7D65A8E-B0C3-448F-B79C-6C330190A266).

```sql
IF boolean_expression THEN
    statement
    [ statement ]...
[
ELSIF boolean_expression THEN
    statement
    [ statement ]... ]...
   [
ELSE
statement [ statement ]... ] END IF ;
```

```sql
IF ( `<condition>` ) THEN
    `<statement>`;
    [ `<statement>`; ... ]
[
ELSEIF ( `<condition>` ) THEN
    `<statement>`;
    [ `<statement>`; ... ]
]
[
ELSE
    `<statement>`;
    [ `<statement>`; ... ]
]
END IF;
```

### Sample Source Patterns 11

#### Sample auxiliar table 2

```sql
CREATE TABLE if_table(col1 varchar(30));
```

```sql
CREATE OR REPLACE TABLE PUBLIC.if_table (col1 varchar(30));
```

#### Possible IF variations

##### Oracle 58

###### Code 1

```sql
CREATE OR REPLACE PROCEDURE ifExample1 ( flag NUMBER )
IS
BEGIN
    IF flag = 1 THEN
        INSERT INTO if_table(col1) VALUES ('one');
    END IF;
END;

CALL ifExample1(1);
SELECT * FROM if_table;
```

###### Code 2

```sql
CREATE OR REPLACE PROCEDURE ifExample2 ( flag NUMBER )
IS
BEGIN
    IF flag = 1 THEN
        INSERT INTO if_table(col1) VALUES ('one');
    ELSE
        INSERT INTO if_table(col1) VALUES ('Unexpected input.');
    END IF;
END;

CALL ifExample2(2);
SELECT * FROM if_table;
```

###### Code 3

```sql
CREATE OR REPLACE PROCEDURE ifExample3 ( flag NUMBER )
IS
BEGIN
    IF flag = 1 THEN
        INSERT INTO if_table(col1) VALUES ('one');
    ELSIF flag = 2 THEN
        INSERT INTO if_table(col1) VALUES ('two');
    ELSIF flag = 3 THEN
        INSERT INTO if_table(col1) VALUES ('three');
    END IF;
END;

CALL ifExample3(3);
SELECT * FROM if_table;
```

###### Code 4

```sql
CREATE OR REPLACE PROCEDURE ifExample4 ( flag NUMBER )
IS
BEGIN
    IF flag = 1 THEN
        INSERT INTO if_table(col1) VALUES ('one');
    ELSIF flag = 2 THEN
        INSERT INTO if_table(col1) VALUES ('two');
    ELSIF flag = 3 THEN
        INSERT INTO if_table(col1) VALUES ('three');
    ELSE
        INSERT INTO if_table(col1) VALUES ('Unexpected input.');
    END IF;
END;

CALL ifExample4(4);
SELECT * FROM if_table;
```

###### Result 1

<!-- prettier-ignore -->
|COL1|
|---|
|one|

###### Result 2 2

<!-- prettier-ignore -->
|COL1|
|---|
|Unexpected input.|

###### Result 3 2

<!-- prettier-ignore -->
|COL1|
|---|
|three|

###### Result 4 2

<!-- prettier-ignore -->
|COL1|
|---|
|Unexpected input.|

##### Snowflake Scripting 25

###### Code 1 2

```sql
CREATE OR REPLACE PROCEDURE ifExample1 (flag NUMBER(38, 18))
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        IF (:flag = 1) THEN
            INSERT INTO if_table(col1) VALUES ('one');
        END IF;
    END;
$$;

CALL ifExample1(1);

SELECT * FROM
    if_table;
```

###### Code 2 2

```sql
CREATE OR REPLACE PROCEDURE ifExample2 (flag NUMBER(38, 18))
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        IF (:flag = 1) THEN
            INSERT INTO if_table(col1) VALUES ('one');
        ELSE
            INSERT INTO if_table(col1) VALUES ('Unexpected input.');
        END IF;
    END;
$$;

CALL ifExample2(2);

SELECT * FROM
    if_table;
```

###### Code 3 2

```sql
CREATE OR REPLACE PROCEDURE ifExample3 (flag NUMBER(38, 18))
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        IF (:flag = 1) THEN
            INSERT INTO if_table(col1) VALUES ('one');
        ELSEIF (:flag = 2) THEN
            INSERT INTO if_table(col1) VALUES ('two');
        ELSEIF (:flag = 3) THEN
            INSERT INTO if_table(col1) VALUES ('three');
        END IF;
    END;
$$;

CALL ifExample3(3);

SELECT * FROM
    if_table;
```

###### Code 4 2

```sql
CREATE OR REPLACE PROCEDURE ifExample4 (flag NUMBER(38, 18))
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        IF (:flag = 1) THEN
            INSERT INTO if_table(col1) VALUES ('one');
        ELSEIF (:flag = 2) THEN
            INSERT INTO if_table(col1) VALUES ('two');
        ELSEIF (:flag = 3) THEN
            INSERT INTO if_table(col1) VALUES ('three');
        ELSE
            INSERT INTO if_table(col1) VALUES ('Unexpected input.');
        END IF;
    END;
$$;

CALL ifExample4(4);

SELECT * FROM if_table;
```

###### Result 1 2

<!-- prettier-ignore -->
|COL1|
|---|
|one|

###### Result 2 2 2

<!-- prettier-ignore -->
|COL1|
|---|
|Unexpected input.|

###### Result 3 2 2

<!-- prettier-ignore -->
|COL1|
|---|
|three|

###### Result 4 2 2

<!-- prettier-ignore -->
|COL1|
|---|
|Unexpected input.|

### Known issues 12

No issues were found.

### Related EWIS 12

No related EWIs.

## IS EMPTY

This is a translation reference to convert the Oracle IS EMPTY statement to Snowflake

Warning

This section is a work in progress; information may change in the future.

### Description 13

> Use the IS [NOT] EMPTY conditions to test whether a specified nested table is empty, regardless
> whether any elements of the collection are NULL.
> ([Documentation](https://docs.oracle.com/cd/B14117_01/server.101/b10759/conditions013.htm)).

#### Oracle syntax 4

```sql
nested_table IS [ NOT ] EMPTY
```

### Sample Source Patterns 12

#### Oracle 59

The following example shows the usage of the IS EMPTY statement. The statement is applied over a
nested table which uses a UDT as the definition type. The output shows the name of the employees who
do not have a phone number.

```sql
CREATE TYPE phone_number_type AS OBJECT (phone_number VARCHAR2(30));
/

CREATE TYPE phone_number_list AS TABLE OF phone_number_type;

CREATE TABLE employee (
    emp_id NUMBER,
    emp_name VARCHAR2(50),
    phone_numbers_col phone_number_list
) NESTED TABLE phone_numbers_col STORE AS nested_tab return as value;

INSERT INTO employee VALUES (
    1,
    'John Doe',
    phone_number_list(phone_number_type('1234567890'))
);
/

INSERT INTO employee VALUES (
    2,
    'Jane Smith',
    phone_number_list()
);

SELECT emp_name
FROM employee
WHERE phone_numbers_col IS EMPTY;
```

##### Output

<!-- prettier-ignore -->
|EMP_NAME|
|---|
|Jane Smith|

##### Snowflake 31

The Snowflake query shown below is the equivalence of the functionality of the IS EMPTY statement.
Particularly, the IS EMPTY statement has a difference between a NULL and an EMPTY object.

Notice that the User-Defined Types are transformed to a VARIANT. The VARIANT type in Snowflake is
able to store objects and arrays. Since a nested table is a sequence of information, the ARRAY type
is the most suitable type to redefine them and verify is the object ARRAY is empty.

The ARRAY_SIZE equivalent solution also allows to ask for nullability of the nested table
(transformed to VARIANT). In other words, the VARIANT type can also store NULLs and empty ARRAYs.

```sql
!!!RESOLVE EWI!!! /*** SSC-EWI-0056 - CUSTOM TYPES ARE NOT SUPPORTED IN SNOWFLAKE BUT REFERENCES TO THIS CUSTOM TYPE WERE CHANGED TO VARIANT ***/!!!
CREATE TYPE phone_number_type AS OBJECT (phone_number VARCHAR2(30))
;

!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'NESTED TABLE' NODE ***/!!!

CREATE TYPE phone_number_list AS TABLE OF phone_number_type;

CREATE OR REPLACE TABLE employee (
    emp_id NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/,
    emp_name VARCHAR(50),
    phone_numbers_col VARIANT !!!RESOLVE EWI!!! /*** SSC-EWI-0062 - CUSTOM TYPE 'phone_number_list' USAGE CHANGED TO VARIANT ***/!!!
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

CREATE OR REPLACE VIEW PUBLIC.employee_view
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "" }}'
AS
SELECT
    emp_id,
    emp_name,
    phone_numbers_col
FROM
    employee;

INSERT INTO employee
VALUES (
    1,
    'John Doe',
    phone_number_list(phone_number_type('1234567890') !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'phone_number_type' NODE ***/!!!) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'phone_number_list' NODE ***/!!!
);

INSERT INTO employee
VALUES (
    2,
    'Jane Smith',
    phone_number_list() !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'phone_number_list' NODE ***/!!!
);

SELECT emp_name
FROM
    employee
WHERE
    ARRAY_SIZE( phone_numbers_col) = 0;
```

##### Output 2

<!-- prettier-ignore -->
|EMP_NAME|
|---|
|Jane Smith|

#### Other possible combinations

<!-- prettier-ignore -->
|Description|Oracle|Snowflake|
|---|---|---|
|Ask for a IS NOT EMPTY|`(...) WHERE phone_numbers_col IS NOT EMPTY;`|`(...) WHERE ARRAY_SIZE(phone_numbers_col) != 0;`|
|Ask for NULL instead of EMPTY|`(...) WHERE phone_numbers_col IS NULL;`|`(...) WHERE ARRAY_SIZE(phone_numbers_col) IS NULL;`|

### Known Issues 13

#### **1. User-defined types are being transformed into Variant.**

User-defined types are not supported thus they are transformed into Variant types which could need
manual effort to ensure some functionalities.

Review the following page for more information:

[create-type-statement](../sql-translation-reference/create_type)

##### **2. Nested tables are not supported.**

Nested tables are not currently supported. The best approach based on this equivalence is to handle
nested tables as Variant but declare Arrays with JSON data inside and execute the PARSE_JSON
Snowflake function to populate the nested information.

Review the following pages for more information:

[nested-table-array-type-definition.md](collections-and-records.html#nested-table-array-type-definition)

[nested-table-type-definition.md](../sql-translation-reference/create_type.html#nested-table-type-definition)

##### **3. Insert statements are not supported for User-defined types.**

Since User-defined types are not supported in consequence the Insert statements to these types are
not supported. Specifically in nested tables, the `INSERT INTO ... VALUES` statement has to be
changed to a `INSERT INTO ...SELECT` because the ARRAY_CONSTRUCT function is expected to be used in
that pattern.

Review the following page for more information:

[object-type-definition.md](../sql-translation-reference/create_type.html#object-type-definition)

##### **4. Logic should be adapted to `ARRAY` types.**

Since the nested tables should be equivalently transformed to `VARIANT` and behave as `ARRAYs,`the
functionality and logic of implementing procedures and interaction with the data should be adapted.

Review the following examples:

##### 4.1 Procedures equivalence

##### Oracle 60

```sql
create or replace procedure proc1
as
    col1 phone_number_list:= phone_number_list();
begin
   IF col1 IS EMPTY
   THEN
    dbms_output.put_line('IS EMPTY');
   END IF;
end;
```

##### Snowflake 32

```sql
CREATE OR REPLACE PROCEDURE proc1 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
   DECLARE
      col1 VARIANT /*** SSC-FDM-0015 - REFERENCED CUSTOM TYPE 'phone_number_list' IN QUERY NOT FOUND, USAGES MAY BE AFFECTED ***/ := phone_number_list() !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'phone_number_list' NODE ***/!!!;
   BEGIN
      IF (ARRAY_SIZE(:col1) = 0) THEN
         --** SSC-FDM-OR0035 - CHECK UDF IMPLEMENTATION FOR DBMS_OUTPUT.PUT_LINE_UDF. **
         CALL DBMS_OUTPUT.PUT_LINE_UDF('IS EMPTY');
      END IF;
   END;
$$;
```

##### Output 3

<!-- prettier-ignore -->
|PROC1|
|---|
|IS EMPTY|

##### 4.2 Select statements

Outputs may differ from tables to `ARRAYs`.

##### Oracle 61

```sql
SELECT
    t.*
FROM
    employee e,
    table(e.phone_numbers_col) t
WHERE
    emp_id = 1;
```

##### Output 4

<!-- prettier-ignore -->
|PHONE_NUMBER|
|---|
|1234567890|

##### Snowflake 33

```sql
SELECT
    t.*
FROM
    employee e,
    !!!RESOLVE EWI!!! /*** SSC-EWI-OR0035 - TABLE FUNCTION IS NOT SUPPORTED WHEN IT IS USED AS A COLLECTION OF EXPRESSIONS ***/!!!
    table(e.phone_numbers_col) t
WHERE
    emp_id = 1;
```

##### Output 5

<!-- prettier-ignore -->
|PHONE_NUMBERS_COL|
|---|
|[ 1234567890 ]|

### Related EWIs 13

1. [SSC-EWI-0056](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0056):
   Create Type Not Supported.
2. [SSC-EWI-0062](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0062):
   Custom type usage changed to variant.
3. [SSC-EWI-0073](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0073):
   Pending Functional Equivalence Review.
4. [SSC-EWI-OR0035](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI#ssc-ewi-or0035):
   The table function is not supported when it is used as a collection of expressions.
5. [SSC-FDM-0006](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0006):
   Number type column may not behave similarly in Snowflake.
6. [SSC-FDM-0015:](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0015)
   ​Referenced custom type in query not found.
7. [SSC-FDM-OR0035](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM#ssc-fdm-or0035):
   DBMS_OUTPUT.PUTLINE check UDF implementation.

## LOCK TABLE

### Note 29

Non-relevant statement.

Warning

**Notice that this statement removed from the migration; because it is a non-relevant syntax. It
means that it is not required in Snowflake.**

### Description 14

In Oracle, the `LOCK TABLE` statement allows to explicitly acquire a shared or exclusive table lock
on the specified table. The table lock lasts until the end of the current transaction. Review more
information [here](https://docs.oracle.com/javadb/10.6.2.1/ref/rrefsqlj40506.html).

#### Syntax

```sql
LOCK TABLE tableName IN { SHARE | EXCLUSIVE } MODE
```

### Sample Source Patterns 13

#### Locking table

Notice that in this example the `LOCK TABLE` statement has been deleted. This is because Snowflake
handles locking in a different method through transactions.

##### Oracle 62

```sql
LOCK TABLE table1 IN EXCLUSIVE MODE;
```

##### Snowflake 34

```sql
[Empty output]
```

## LOG ERROR

### Note 30

Some parts in the output code are omitted for clarity reasons.

### Description 15

> The `FORALL` statement runs one DML statement multiple times, with different values in the
> `VALUES` and `WHERE` clauses.
> ([Oracle PL/SQL Language Reference FORALL Statement](https://docs.oracle.com/database/121/LNPLS/forall_statement.htm#LNPLS01321)).

#### Oracle Syntax 5

```sql
FORALL index IN bounds_clause [ SAVE ] [ EXCEPTIONS ] dml_statement ;
```

Warning

Snowflake Scripting has no direct equivalence with the `FORALL` statement, however can be emulated
with different workarounds to get functional equivalence.

### Sample Source Patterns 14

#### Setup Data 2

##### Oracle 63

##### Tables

```sql
CREATE TABLE error_table (
    ORA_ERR_NUMBER$ NUMBER,
    ORA_ERR_MESG$ VARCHAR2(2000),
    ORA_ERR_ROWID$ ROWID,
    ORA_ERR_OPTYP$ VARCHAR2(2),
    ORA_ERR_TAG$ VARCHAR2(2000)
);

--departments
CREATE TABLE parent_table(
    Id INT PRIMARY KEY,
    Name VARCHAR2(10)
);

INSERT INTO parent_table VALUES (10, 'IT');
INSERT INTO parent_table VALUES (20, 'HR');
INSERT INTO parent_table VALUES (30, 'INFRA');

--employees
CREATE TABLE source_table(
    Id INT PRIMARY KEY,
    Name VARCHAR2(20) NOT NULL,
    DepartmentID INT REFERENCES parent_table(Id)
);

INSERT INTO source_table VALUES (101, 'Anurag111111111', 10);
INSERT INTO source_table VALUES (102, 'Pranaya11111111', 20);
INSERT INTO source_table VALUES (103, 'Hina11111111111', 30);

--a copy of source
CREATE TABLE target_table(
    Id INT PRIMARY KEY,
    Name VARCHAR2(10) NOT NULL,
    DepartmentID INT REFERENCES parent_table(Id)
);

INSERT INTO target_table VALUES (101, 'Anurag', 10);
```

##### Snowflake 35

##### Tables 2 2 2

```sql
CREATE OR REPLACE TABLE error_table (
    "ORA_ERR_NUMBER$" NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/,
    "ORA_ERR_MESG$" VARCHAR(2000),
    "ORA_ERR_ROWID$" VARCHAR(18) !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - ROWID DATA TYPE CONVERTED TO VARCHAR ***/!!!,
    "ORA_ERR_OPTYP$" VARCHAR(2),
    "ORA_ERR_TAG$" VARCHAR(2000)
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

--departments
CREATE OR REPLACE TABLE parent_table (
        Id INT PRIMARY KEY,
        Name VARCHAR(10)
    )
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

INSERT INTO parent_table
VALUES (10, 'IT');

INSERT INTO parent_table
VALUES (20, 'HR');

INSERT INTO parent_table
VALUES (30, 'INFRA');

--employees
CREATE OR REPLACE TABLE source_table (
    Id INT PRIMARY KEY,
    Name VARCHAR(20) NOT NULL,
    DepartmentID INT REFERENCES parent_table (Id)
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

INSERT INTO source_table
VALUES (101, 'Anurag111111111', 10);

INSERT INTO source_table
VALUES (102, 'Pranaya11111111', 20);

INSERT INTO source_table
VALUES (103, 'Hina11111111111', 30);

--a copy of source
CREATE OR REPLACE TABLE target_table (
    Id INT PRIMARY KEY,
    Name VARCHAR(10) NOT NULL,
    DepartmentID INT REFERENCES parent_table (Id)
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

INSERT INTO target_table
VALUES (101, 'Anurag', 10);
```

#### 1. MERGE INTO Inside a FORALL

##### Oracle 64

###### Note 31

The three cases below have the same transformation to Snowflake Scripting and are functionally
equivalent.

##### Case 1

```sql
CREATE OR REPLACE PROCEDURE procedure_example (
    department_id_in   IN source_table.DepartmentID%TYPE)
IS
    TYPE employee_ids_t IS TABLE OF source_table%ROWTYPE
    INDEX BY PLS_INTEGER;
    employee_list   employee_ids_t;
BEGIN
    SELECT *
        BULK COLLECT INTO employee_list
        FROM source_table
        WHERE DepartmentID = procedure_example.department_id_in;

    FORALL indx IN 1 .. employee_list.COUNT
      MERGE INTO target_table
      USING (SELECT * FROM DUAL) src
      ON (id = employee_list(indx).id)
      WHEN MATCHED THEN
        UPDATE SET
          name = employee_list(indx).Name
      WHEN NOT MATCHED THEN
        INSERT (Id, Name, DepartmentID)
        VALUES (employee_list(indx).Id, employee_list(indx).Name, employee_list(indx).DepartmentID)
      LOG ERRORS INTO error_table('MERGE INTO ERROR')
      REJECT LIMIT UNLIMITED;

END;

CALL procedure_example(10);

select * from target_table;
select * from error_table;
```

##### Snowflake 36

##### FORALL With Collection of Records 2

```sql
CREATE OR REPLACE PROCEDURE procedure_example (department_id_in VARIANT !!!RESOLVE EWI!!! /*** SSC-EWI-OR0129 - TYPE ATTRIBUTE 'source_table.DepartmentID%TYPE' COULD NOT BE RESOLVED, SO IT WAS TRANSFORMED TO VARIANT ***/!!!)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
--        !!!RESOLVE EWI!!! /*** SSC-EWI-0058 - FUNCTIONALITY FOR 'PL COLLECTION TYPE DEFINITION' IS NOT CURRENTLY SUPPORTED BY SNOWFLAKE SCRIPTING ***/!!!
--        TYPE employee_ids_t IS TABLE OF source_table%ROWTYPE
--        INDEX BY PLS_INTEGER;
        employee_list VARIANT !!!RESOLVE EWI!!! /*** SSC-EWI-0062 - CUSTOM TYPE 'employee_ids_t' USAGE CHANGED TO VARIANT ***/!!!;
        FORALL INTEGER;
    BEGIN
        !!!RESOLVE EWI!!! /*** SSC-EWI-0058 - FUNCTIONALITY FOR 'RECORDS AND COLLECTIONS' IS NOT CURRENTLY SUPPORTED BY SNOWFLAKE SCRIPTING ***/!!!
        SELECT *
            BULK COLLECT INTO employee_list
            FROM source_table
            WHERE DepartmentID = procedure_example.department_id_in;
        FORALL := ARRAY_SIZE(:employee_list);
          MERGE INTO target_table
          USING (SELECT * FROM
                (
                    SELECT
                        seq4() AS indx
                    FROM
                        TABLE(GENERATOR(ROWCOUNT => :FORALL))
                )) src
          ON (id = : employee_list[indx]:id)
        WHEN MATCHED THEN
        UPDATE SET
          name = : employee_list[indx]:Name
        WHEN NOT MATCHED THEN
        INSERT (Id, Name, DepartmentID)
        VALUES (:employee_list[indx]:Id, : employee_list[indx]:Name, : employee_list[indx]:DepartmentID)
--        --** SSC-FDM-OR0031 - THE ERROR LOGGING CLAUSE IN DML STATEMENTS IS NOT SUPPORTED BY SNOWFLAKE **
--          LOG ERRORS INTO error_table('MERGE INTO ERROR')
--          REJECT LIMIT UNLIMITED
                                ;
    END;
$$;

CALL procedure_example(10);

select * from
    target_table;

select * from
    error_table;
```

#### 2. FORALL With INSERT INTO 2

##### Oracle 65

##### FORALL Example 14

```sql
CREATE OR REPLACE PROCEDURE myProcedure IS
    CURSOR cursorVariable IS
        SELECT * FROM table1;
    TYPE collectionTypeDefinition IS TABLE OF table1%ROWTYPE;
    collectionVariable collectionTypeDefinition;
BEGIN
    OPEN cursorVariable;
    LOOP
        FETCH cursorVariable BULK COLLECT INTO collectionVariable limit 2;
        EXIT WHEN collectionVariable.COUNT = 0;
        FORALL forIndex IN collectionVariable.FIRST..collectionVariable.LAST
            INSERT INTO table2 VALUES collectionVariable(forIndex);
        collectionVariable.DELETE;
    END LOOP;
    CLOSE cursorVariable;
END;
```

##### Results 31

<!-- prettier-ignore -->
|COLUMN1|COLUMN2|
|---|---|
|1|2|
|1|2|
|2|3|
|3|4|
|4|5|
|5|6|

##### Snowflake 37

##### FORALL Equivalent 13

```sql
CREATE OR REPLACE PROCEDURE myProcedure ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$

    BEGIN
        --** SSC-PRF-0001 - THIS STATEMENT HAS USAGES OF CURSOR FETCH BULK OPERATIONS **
        --** SSC-PRF-0003 - FETCH INSIDE A LOOP IS CONSIDERED A COMPLEX PATTERN, THIS COULD DEGRADE SNOWFLAKE PERFORMANCE. **
        INSERT INTO table2
        (
            SELECT
                * FROM
                table1
        );
    END;
$$;
```

##### Results 32

<!-- prettier-ignore -->
|COLUMN1|COLUMN2|
|---|---|
|1.000000000000000000|2.000000000000000000|
|1.000000000000000000|2.000000000000000000|
|2.000000000000000000|3.000000000000000000|
|3.000000000000000000|4.000000000000000000|
|4.000000000000000000|5.000000000000000000|
|5.000000000000000000|6.000000000000000000|

#### 3. FORALL With Multiple Fetched Collections 2

##### Oracle 66

##### With INSERT INTO 3

```sql
CREATE OR REPLACE PROCEDURE myProcedure IS
    CURSOR cursorVariable IS
        SELECT * FROM table1;
    column1Collection dbms_sql.NUMBER_table;
    column2Collection dbms_sql.NUMBER_table;
BEGIN
    OPEN cursorVariable;
    LOOP
        FETCH cursorVariable BULK COLLECT INTO column1Collection, column2Collection limit 20;
        EXIT WHEN column1Collection.COUNT = 0;
        FORALL forIndex IN 1..column1Collection.COUNT
            INSERT INTO table2 VALUES (
                column1Collection(forIndex),
                column2Collection(forIndex)
            );
    END LOOP;
    CLOSE cursorVariable;
END;
```

##### With UPDATE 3

```sql
CREATE OR REPLACE PROCEDURE myProcedure IS
    CURSOR cursorVariable IS
        SELECT * FROM table1;
    column1Collection dbms_sql.NUMBER_table;
    column2Collection dbms_sql.NUMBER_table;
BEGIN
    OPEN cursorVariable;
    LOOP
        FETCH cursorVariable BULK COLLECT INTO column1Collection, column2Collection limit 2;
        EXIT WHEN column1Collection.COUNT = 0;
        FORALL forIndex IN 1..column1Collection.COUNT
            UPDATE table2 SET column2 = column2Collection(forIndex)
            WHERE column1 = column1Collection(forIndex);
    END LOOP;
    CLOSE cursorVariable;
END;
```

##### Results INSERT INTO 3

<!-- prettier-ignore -->
|COLUMN1|COLUMN2|
|---|---|
|1|2|
|2|3|
|3|4|
|4|5|
|5|6|
|1|2|

##### Results UPDATE 3

<!-- prettier-ignore -->
|COLUMN1|COLUMN2|
|---|---|
|1|2|

##### Snowflake 38

##### With INSERT INTO 4

```sql
CREATE OR REPLACE PROCEDURE myProcedure ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$

    BEGIN
        --** SSC-PRF-0001 - THIS STATEMENT HAS USAGES OF CURSOR FETCH BULK OPERATIONS **
        --** SSC-PRF-0003 - FETCH INSIDE A LOOP IS CONSIDERED A COMPLEX PATTERN, THIS COULD DEGRADE SNOWFLAKE PERFORMANCE. **
        INSERT INTO table2
        (
            SELECT
                $1,
                $2
            FROM
                table1
        );
    END;
$$;
```

##### With UPDATE 4

```sql
CREATE OR REPLACE PROCEDURE myProcedure ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$

    BEGIN
        --** SSC-PRF-0001 - THIS STATEMENT HAS USAGES OF CURSOR FETCH BULK OPERATIONS **
        --** SSC-PRF-0003 - FETCH INSIDE A LOOP IS CONSIDERED A COMPLEX PATTERN, THIS COULD DEGRADE SNOWFLAKE PERFORMANCE. **
        UPDATE table2
            SET column2 = column1Collection.$2
            FROM
                (
                    SELECT
                        * FROM
                        table1) AS column1Collection
            WHERE
                column1 = column1Collection.$1;
    END;
$$;
```

##### Results INSERT INTO 4

<!-- prettier-ignore -->
|COLUMN1|COLUMN2|
|---|---|
|1.000000000000000000|2.000000000000000000|
|1.000000000000000000|2.000000000000000000|
|2.000000000000000000|3.000000000000000000|
|3.000000000000000000|4.000000000000000000|
|4.000000000000000000|5.000000000000000000|
|5.000000000000000000|6.000000000000000000|

##### Results UPDATE 4

<!-- prettier-ignore -->
|COLUMN1|COLUMN2|
|---|---|
|1.000000000000000000|2.000000000000000000|

#### 4. FORALL With Record of Collections 2

##### Oracle 67

##### FORALL Example 15

```sql
CREATE OR REPLACE PROCEDURE myProcedure IS
    CURSOR cursorVariable IS
        SELECT * FROM table1;
    TYPE recordType IS RECORD(
        column1Collection dbms_sql.NUMBER_table,
        column2Collection dbms_sql.NUMBER_table
    );
    columnRecord recordType;
BEGIN
    OPEN cursorVariable;
    LOOP
        FETCH cursorVariable BULK COLLECT INTO columnRecord.column1Collection, columnRecord.column2Collection limit 20;
        FORALL forIndex IN 1..columnRecord.column1Collection.COUNT
            INSERT INTO table2 VALUES (
                columnRecord.column1Collection(forIndex),
                columnRecord.column2Collection(forIndex)
            );
        EXIT WHEN cursorVariable%NOTFOUND;
    END LOOP;
    CLOSE cursorVariable;
END;
```

##### Results 33

<!-- prettier-ignore -->
|COLUMN1|COLUMN2|
|---|---|
|1|2|
|1|2|
|2|3|
|3|4|
|4|5|
|5|6|

##### Snowflake 39

##### Scripting FORALL Equivalent 2

```sql
CREATE OR REPLACE PROCEDURE myProcedure ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$

    BEGIN
        --** SSC-PRF-0001 - THIS STATEMENT HAS USAGES OF CURSOR FETCH BULK OPERATIONS **
        --** SSC-PRF-0003 - FETCH INSIDE A LOOP IS CONSIDERED A COMPLEX PATTERN, THIS COULD DEGRADE SNOWFLAKE PERFORMANCE. **
        INSERT INTO table2
        (
            SELECT
                $1,
                $2
            FROM
                table1
        );
    END;
$$;
```

##### Results 34

<!-- prettier-ignore -->
|COLUMN1|COLUMN2|
|---|---|
|1.000000000000000000|2.000000000000000000|
|1.000000000000000000|2.000000000000000000|
|2.000000000000000000|3.000000000000000000|
|3.000000000000000000|4.000000000000000000|
|4.000000000000000000|5.000000000000000000|
|5.000000000000000000|6.000000000000000000|

#### 5. FORALL With Dynamic SQL 2

##### Oracle 68

##### FORALL Example 16

```sql
CREATE OR REPLACE PROCEDURE myProcedure IS
    cursorVariable SYS_REFCURSOR;
    TYPE collectionTypeDefinition IS
        TABLE OF table1%ROWTYPE;
    collectionVariable collectionTypeDefinition;
    query VARCHAR(200) := 'SELECT * FROM table1';
BEGIN
    OPEN cursorVariable FOR query;
    LOOP
        FETCH cursorVariable BULK COLLECT INTO collectionVariable;
        EXIT WHEN collectionVariable.COUNT = 0;
        FORALL forIndex IN collectionVariable.FIRST..collectionVariable.LAST
            INSERT INTO table2 VALUES collectionVariable(forIndex);
        collectionVariable.DELETE;
    END LOOP;
    CLOSE cursorVariable;
END;
```

##### Results 35

<!-- prettier-ignore -->
|COLUMN1|COLUMN2|
|---|---|
|1|2|
|1|2|
|2|3|
|3|4|
|4|5|
|5|6|

##### Snowflake 40

##### FORALL Equivalent 14

```sql
CREATE OR REPLACE PROCEDURE myProcedure ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        query VARCHAR(200) := 'SELECT * FROM
   table1';
    BEGIN
        --** SSC-PRF-0001 - THIS STATEMENT HAS USAGES OF CURSOR FETCH BULK OPERATIONS **
        --** SSC-PRF-0003 - FETCH INSIDE A LOOP IS CONSIDERED A COMPLEX PATTERN, THIS COULD DEGRADE SNOWFLAKE PERFORMANCE. **
        !!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!
        EXECUTE IMMEDIATE 'CREATE OR REPLACE TEMPORARY TABLE query AS ' || :query;
        INSERT INTO table2
        (
            SELECT
                *
            FROM
                query
        );
    END;
$$;
```

##### Results 36

<!-- prettier-ignore -->
|COLUMN1|COLUMN2|
|---|---|
|1.000000000000000000|2.000000000000000000|
|1.000000000000000000|2.000000000000000000|
|2.000000000000000000|3.000000000000000000|
|3.000000000000000000|4.000000000000000000|
|4.000000000000000000|5.000000000000000000|
|5.000000000000000000|6.000|

#### 6. FORALL Without LOOPS

##### Oracle 69

##### FORALL Example 17

```sql
CREATE OR REPLACE PROCEDURE  myProcedure IS
    TYPE collectionTypeDefinition IS TABLE OF table1%ROWTYPE;
    collectionVariable collectionTypeDefinition;
BEGIN
    SELECT * BULK COLLECT INTO collectionVariable FROM table1;
        FORALL forIndex IN 1..collectionVariable.COUNT
            INSERT INTO table2 VALUES (
                collectionVariable (forIndex).column1,
                collectionVariable (forIndex).column2
            );
        collectionVariable.DELETE;
END;
```

##### Results 37

<!-- prettier-ignore -->
|COLUMN1|COLUMN2|
|---|---|
|1|2|
|1|2|
|2|3|
|3|4|
|4|5|
|5|6|

##### Snowflake 41

##### FORALL Equivalent 15

```sql
CREATE OR REPLACE PROCEDURE myProcedure ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$

    BEGIN
        --** SSC-PRF-0003 - FETCH INSIDE A LOOP IS CONSIDERED A COMPLEX PATTERN, THIS COULD DEGRADE SNOWFLAKE PERFORMANCE. **
        INSERT INTO table2
        (
            SELECT
                column1,
                column2
            FROM
                table1
        );
    END;
$$;
```

##### Results 38

<!-- prettier-ignore -->
|COLUMN1|COLUMN2|
|---|---|
|1.000000000000000000|2.000000000000000000|
|1.000000000000000000|2.000000000000000000|
|2.000000000000000000|3.000000000000000000|
|3.000000000000000000|4.000000000000000000|
|4.000000000000000000|5.000000000000000000|
|5.000000000000000000|6.000000000000000000|

#### 7. FORALL With UPDATE Statements

##### Oracle 70

##### FORALL Example 18

```sql
CREATE OR REPLACE PROCEDURE myProcedure IS
    CURSOR cursorVariable IS
        SELECT * FROM table1;
    TYPE collectionTypeDefinition IS TABLE OF table1%ROWTYPE;
    collectionVariable collectionTypeDefinition;
BEGIN
    OPEN cursorVariable;
    LOOP
        FETCH cursorVariable BULK COLLECT INTO collectionVariable limit 2;
        EXIT WHEN collectionVariable.COUNT = 0;
        FORALL forIndex IN collectionVariable.FIRST..collectionVariable.LAST
            UPDATE table2 SET column1 = '54321' WHERE column2 = collectionVariable(forIndex).column2;
        collectionVariable.DELETE;
    END LOOP;
    CLOSE cursorVariable;
END;
```

##### Results 39

<!-- prettier-ignore -->
|COLUMN1|COLUMN2|
|---|---|
|54321|2|

##### Snowflake 42

##### FORALL Equivalent 16

```sql
CREATE OR REPLACE PROCEDURE myProcedure ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$

    BEGIN
        --** SSC-PRF-0001 - THIS STATEMENT HAS USAGES OF CURSOR FETCH BULK OPERATIONS **
        --** SSC-PRF-0003 - FETCH INSIDE A LOOP IS CONSIDERED A COMPLEX PATTERN, THIS COULD DEGRADE SNOWFLAKE PERFORMANCE. **
        UPDATE table2
            SET column1 = '54321'
            FROM
                (
                    SELECT
                        * FROM
                        table1) AS collectionVariable
            WHERE
                column2 = collectionVariable.column2;
    END;
$$;
```

##### Results 40

```sql
ambiguous column name 'COLUMN2'
```

#### 8. FORALL With DELETE Statements

##### Oracle 71

##### FORALL Example 19

```sql
CREATE OR REPLACE PROCEDURE myProcedure IS
    CURSOR cursorVariable IS
        SELECT * FROM table1;
    TYPE collectionTypeDefinition IS TABLE OF table1%ROWTYPE;
    collectionVariable collectionTypeDefinition;
BEGIN
    OPEN cursorVariable;
    LOOP
        FETCH cursorVariable BULK COLLECT INTO collectionVariable limit 2;
        EXIT WHEN collectionVariable.COUNT = 0;
        FORALL forIndex IN collectionVariable.FIRST..collectionVariable.LAST
            DELETE FROM table2 WHERE column2 = collectionVariable(forIndex).column2;
        collectionVariable.DELETE;
    END LOOP;
    CLOSE cursorVariable;
END;
```

##### Results 41

```sql
no data found
```

##### Snowflake 43

##### FORALL Equivalent 17

```sql
CREATE OR REPLACE PROCEDURE myProcedure ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$

    BEGIN
        --** SSC-PRF-0001 - THIS STATEMENT HAS USAGES OF CURSOR FETCH BULK OPERATIONS **
        --** SSC-PRF-0003 - FETCH INSIDE A LOOP IS CONSIDERED A COMPLEX PATTERN, THIS COULD DEGRADE SNOWFLAKE PERFORMANCE. **
        DELETE FROM
            table2
        USING (
            SELECT
                * FROM
                table1) collectionVariable
                WHERE
            table2.column2 = collectionVariable.column2;
    END;
$$;
```

##### Results 42

```sql
Query produced no results
```

### Known Issues 14

No issues were found.

### Related EWIs 14

1. [SSC-EWI-0030](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0030):
   The statement below has usages of dynamic SQL.
2. [SSC-EWI-0036](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0036):
   Data type converted to another data type.
3. [SSC-EWI-0058](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0058):
   Functionality is not currently supported by Snowflake Scripting.
4. [SSC-EWI-0062](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0062):
   Custom type usage changed to variant.
5. [SSC-EWI-OR0129](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI#ssc-ewi-or0129):
   TYPE attribute could not be resolved.
6. [SSC-FDM-0006](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0006):
   Number type column may not behave similarly in Snowflake.
7. [SSC-FDM-OR0031:](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM#ssc-fdm-or0031)
   The error logging clause in DML statements is not supported by Snowflake.
8. [SSC-PRF-0001](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/performance-review/generalPRF#ssc-prf-0001):
   This statement has usages of cursor fetch bulk operations.
9. [SSC-PRF-0003](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/performance-review/generalPRF#ssc-prf-0003):
   Fetch inside a loop is considered a complex pattern, this could degrade Snowflake performance.

## LOOP

Translation reference to convert Oracle LOOP statement to Snowflake Scripting

### Description 16

> With each iteration of the basic `LOOP` statement, its statements run and control returns to the
> top of the loop. The `LOOP` statement ends when a statement inside the loop transfers control
> outside the loop or raises an exception.
> ([Oracle PL/SQL Language Reference BASIC LOOP Statement](https://docs.oracle.com/en/database/oracle/oracle-database/21/lnpls/basic-LOOP-statement.html#GUID-99AC48AC-D868-43C4-9E4D-6A7671942A39))

#### Oracle BASIC LOOP Syntax

```sql
LOOP statement... END LOOP [ label ] ;
```

##### Snowflake Scripting BASIC LOOP Syntax

```sql
LOOP
  `<statement>`;
  [ `<statement>`; ... ]
END LOOP [ `<label>` ] ;
```

Oracle `BASIC LOOP` behavior can also be modified by using the statements:

- [CONTINUE](#continue)
- [EXIT](#exit)
- GOTO
- [RAISE](#raise)

### Sample Source Patterns 15

#### Loop simple case

##### Note 32

This case is functionally equivalent.

##### Oracle 72

```sql
CREATE TABLE loop_testing_table
(
    iterator VARCHAR2(5)
);

CREATE OR REPLACE PROCEDURE loop_procedure
IS
I NUMBER := 1;
J NUMBER := 10;
BEGIN
  LOOP
    EXIT WHEN I = J;
    INSERT INTO loop_testing_table VALUES(TO_CHAR(I));
    I := I+1;
  END LOOP;
END;

CALL loop_procedure();
SELECT * FROM loop_testing_table;
```

##### Result 43

<!-- prettier-ignore -->
|ITERATOR|
|---|
|1|
|2|
|3|
|4|
|5|
|6|
|7|
|8|
|9|

##### Snowflake Scripting 26

```sql
CREATE OR REPLACE TABLE loop_testing_table
  (
      iterator VARCHAR(5)
  )
  COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/14/2025",  "domain": "no-domain-provided" }}'
  ;

  CREATE OR REPLACE PROCEDURE loop_procedure ()
  RETURNS VARCHAR
  LANGUAGE SQL
  COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/14/2025",  "domain": "no-domain-provided" }}'
  EXECUTE AS CALLER
  AS
  $$
  DECLARE
      I NUMBER(38, 18) := 1;
      J NUMBER(38, 18) := 10;
  BEGIN
      --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
      LOOP
        IF (:I = :J) THEN
          EXIT;
        END IF;
        INSERT INTO loop_testing_table
        VALUES(TO_CHAR(:I));
        I := :I +1;
      END LOOP;
  END;
  $$;

  CALL loop_procedure();

  SELECT * FROM
  loop_testing_table;
```

##### Result 44

<!-- prettier-ignore -->
|ITERATOR|
|---|
|1|
|2|
|3|
|4|
|5|
|6|
|7|
|8|
|9|

### Known Issues 15

No issues were found.

### Related EWIs 15

No related EWIs.

## OUTPUT PARAMETERS

### Description 17

An **output parameter** is a parameter whose value is passed out of the stored procedure/function
module, back to the calling PL/SQL block. Since the output parameters are not supported by Snowflake
Scripting, a solution has been implemented in order to emulate their functionality.

### Sample Source Patterns 16

#### Single out parameter

##### Oracle 73

```sql
-- Procedure with output parameter declaration
CREATE OR REPLACE PROCEDURE proc_with_single_output_parameters(param1 OUT NUMBER)
IS
BEGIN
    param1 := 123;
END;

-- Procedure with output parameter being called
CREATE OR REPLACE PROCEDURE proc_calling_proc_with_single_output_parameters
IS
    var1 NUMBER;
BEGIN
    proc_with_single_output_parameters(var1);
    INSERT INTO TABLE01 VALUES(var1, -1);
END;
```

##### Snowflake Scripting 27

```sql
-- Procedure with output parameter declaration
CREATE OR REPLACE PROCEDURE proc_with_single_output_parameters (param1 OUT NUMBER(38, 18))
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        param1 := 123;
    END;
$$;

-- Procedure with output parameter being called
--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "TABLE01" **
CREATE OR REPLACE PROCEDURE proc_calling_proc_with_single_output_parameters ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        var1 NUMBER(38, 18);
    BEGIN
        CALL
        proc_with_single_output_parameters(:var1);
        INSERT INTO TABLE01
        VALUES(:var1, -1);
    END;
$$;
```

#### Multiple out parameter

##### Oracle 74

```sql
-- Procedure with output parameters declaration
CREATE OR REPLACE PROCEDURE proc_with_multiple_output_parameters(
    param1 OUT NUMBER,
    param2 IN OUT NUMBER
)
IS
BEGIN
    param1 := 123;
    param2 := 456;
END;

-- Procedure with output parameters being called
CREATE OR REPLACE PROCEDURE proc_calling_proc_with_multiple_output_parameters
IS
    var1 NUMBER;
    var2 NUMBER;
BEGIN
    proc_with_multiple_output_parameters(var1, var2);
    INSERT INTO TABLE01 VALUES(var1, var2);
END;
```

##### Snowflake Scripting 28

```sql
-- Procedure with output parameters declaration
CREATE OR REPLACE PROCEDURE proc_with_multiple_output_parameters (param1 OUT NUMBER(38, 18), param2 OUT NUMBER(38, 18)
)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        param1 := 123;
        param2 := 456;
    END;
$$;

-- Procedure with output parameters being called
--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "TABLE01" **
CREATE OR REPLACE PROCEDURE proc_calling_proc_with_multiple_output_parameters ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        var1 NUMBER(38, 18);
        var2 NUMBER(38, 18);
    BEGIN
        CALL
        proc_with_multiple_output_parameters(:var1, :var2);
        INSERT INTO TABLE01
        VALUES(:var1, :var2);
    END;
$$;
```

In order to check that the functionality is being emulated correctly the following query is going to
execute the procedure and a `SELECT` from the table mentioned before.

##### Oracle 75

```sql
CALL proc_with_single_output_parameters();
CALL proc_with_multiple_output_parameters();

SELECT * FROM table01;
```

##### Result 45

<!-- prettier-ignore -->
|COL1|COL2|
|---|---|
|123|-1|
|123|456|

##### Snowflake Scripting 29

```sql
CALL proc_with_single_output_parameters();
CALL proc_with_multiple_output_parameters();

SELECT * FROM table01;
```

##### Result 46

<!-- prettier-ignore -->
|COL1|COL2|
|---|---|
|123.000000000000000000|-1|
|123.000000000000000000|456.000000000000000000|

#### Customer data type OUT parameters

When the output parameter is a customer type, the process is similar to a regular data type.

##### Oracle 76

```sql
CREATE OR REPLACE PROCEDURE procedure_udtype_out_params (
    p_employee_id NUMBER,
    p_address OUT address_type
)
AS
BEGIN
    -- Retrieve the employee's address based on the employee ID.
    SELECT home_address INTO p_address
    FROM employees
    WHERE employee_id = p_employee_id;
END;
```

##### Snowflake Scripting 30

```sql
--** SSC-FDM-0007 - MISSING DEPENDENT OBJECTS "address_type", "employees" **
CREATE OR REPLACE PROCEDURE procedure_udtype_out_params (p_employee_id NUMBER(38, 18), p_address OUT VARIANT /*** SSC-FDM-0015 - REFERENCED CUSTOM TYPE 'address_type' IN QUERY NOT FOUND, USAGES MAY BE AFFECTED ***/
)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        -- Retrieve the employee's address based on the employee ID.
        SELECT home_address INTO
            :p_address
        FROM
            employees
        WHERE employee_id = :p_employee_id;
    END;
$$;
```

#### Cursor OUT parameters

Cursor out parameters are not supported in Snowflake; despite that, a workaround that emulates
Oracle’s behavior is applied to the transformed code. The procedure with the out parameters
generates a temporary table with a dynamic name, and the procedure call will define the name of the
temp table as a string to create the table within the procedure call.

##### Oracle 77

```sql
CREATE OR REPLACE PROCEDURE get_employees_by_dept (
  p_department_id IN NUMBER,
  p_employee_cursor OUT SYS_REFCURSOR
)
AS
BEGIN
 OPEN p_employee_cursor FOR
     SELECT employee_id, first_name, last_name
     FROM   employees_sample
     WHERE  department_id = p_department_id
     ORDER BY last_name;
END get_employees_by_dept;
/

CREATE OR REPLACE PROCEDURE proc_calling_proc_with_cursor()
AS
DECLARE
   l_emp_id NUMBER;
   l_first_name VARCHAR;
   l_last_name VARCHAR;
   l_cursor  SYS_REFCURSOR;
BEGIN
   get_employees_by_dept(10, l_cursor);
   LOOP
       FETCH l_cursor INTO l_emp_id, l_first_name, l_last_name;
       EXIT WHEN l_cursor%NOTFOUND;
       INSERT INTO employee VALUES (l_emp_id, l_first_name, l_last_name);
    END LOOP;
    CLOSE l_cursor;
END;
/
```

##### Snowflake Scripting 31

```sql
--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "employees_sample" **
CREATE OR REPLACE PROCEDURE get_employees_by_dept (p_department_id NUMBER(38, 18), p_employee_cursor VARCHAR
)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
 BEGIN
  CREATE OR REPLACE TEMPORARY TABLE IDENTIFIER(:p_employee_cursor) AS
   SELECT employee_id, first_name, last_name
   FROM
    employees_sample
   WHERE  department_id = :p_department_id
   ORDER BY last_name;
 END;
$$;

--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "employee" **
CREATE OR REPLACE PROCEDURE proc_calling_proc_with_cursor ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
 DECLARE
    l_emp_id NUMBER(38, 18);
    l_first_name VARCHAR;
    l_last_name VARCHAR;
    l_cursor_res RESULTSET;
 BEGIN
    CALL
    get_employees_by_dept(10, 'proc_calling_proc_with_cursor_l_cursor');
    LET l_cursor CURSOR
    FOR
   SELECT
    *
   FROM
    IDENTIFIER('proc_calling_proc_with_cursor_l_cursor');
    OPEN l_cursor;
    --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
    LOOP
   --** SSC-PRF-0003 - FETCH INSIDE A LOOP IS CONSIDERED A COMPLEX PATTERN, THIS COULD DEGRADE SNOWFLAKE PERFORMANCE. **
        FETCH l_cursor INTO
    :l_emp_id,
    :l_first_name,
    :l_last_name;
   IF (l_emp_id IS NULL) THEN
    EXIT;
   END IF;
        INSERT INTO employee
   SELECT
    :l_emp_id,
    :l_first_name,
    :l_last_name;
     END LOOP;
        CLOSE l_cursor;
 END;
$$;
```

#### Record OUT parameters

Records are not natively supported in Snowflake; however, a workaround was used to emulate them as
output parameters. By defining an OBJECT variable instead of the record, we could emulate the
record’s field structure by assigning the out parameter result to each object property.
Additionally, for each record field assigned as an out parameter, a new variable with the field type
will be generated.

##### Oracle 78

```sql
CREATE OR REPLACE PROCEDURE procedure_with_out_params(
  param1 OUT INTEGER,
  param2 OUT INTEGER)
IS
BEGIN
  param1 := 123;
  param2 := 456;
END;

CREATE OR REPLACE PROCEDURE test_proc
IS
  TYPE custom_record1 IS RECORD(field3 INTEGER, field4 INTEGER);
  TYPE custom_record2 IS RECORD(field1 INTEGER, field2 custom_record1);
  var1 custom_record2;
BEGIN
  procedure_with_out_params(var1.field1, var1.field2.field4);
END;
```

##### Snowflake Scripting 32

```sql
CREATE OR REPLACE PROCEDURE procedure_with_out_params (param1 OUT INTEGER, param2 OUT INTEGER)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
  BEGIN
    param1 := 123;
    param2 := 456;
  END;
$$;

CREATE OR REPLACE PROCEDURE test_proc ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
  DECLARE
    !!!RESOLVE EWI!!! /*** SSC-EWI-0056 - CUSTOM TYPES ARE NOT SUPPORTED IN SNOWFLAKE BUT REFERENCES TO THIS CUSTOM TYPE WERE CHANGED TO OBJECT ***/!!!
    TYPE custom_record1 IS RECORD(field3 INTEGER, field4 INTEGER);
    !!!RESOLVE EWI!!! /*** SSC-EWI-0056 - CUSTOM TYPES ARE NOT SUPPORTED IN SNOWFLAKE BUT REFERENCES TO THIS CUSTOM TYPE WERE CHANGED TO OBJECT ***/!!!
    TYPE custom_record2 IS RECORD(field1 INTEGER, field2 custom_record1);
    var1 OBJECT !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - custom_record2 DATA TYPE CONVERTED TO OBJECT ***/!!! := OBJECT_CONSTRUCT();
    var1_field1 INTEGER;
    var1_field2_field4 INTEGER;
  BEGIN
    CALL
    procedure_with_out_params(:var1_field1, :var1_field2_field4);
    var1 := OBJECT_INSERT(COALESCE(var1, OBJECT_CONSTRUCT()), 'field1', :var1_field1, true);
    var1 := OBJECT_INSERT(COALESCE(var1, OBJECT_CONSTRUCT()), 'field2', OBJECT_INSERT(COALESCE(var1:field2, OBJECT_CONSTRUCT()), 'field4', :var1_field2_field4, true), true);
  END;
$$;
```

#### Package Variables as OUT parameters

Packages are not supported in Snowflake, so their local members, like variables or constants, should
also be preserved using a workaround. In this scenario, the package variable would be emulated using
a session variable that would be updated after setting a local variable with the output parameter
result.

##### Oracle 79

```sql
CREATE OR REPLACE PACKAGE scha1.pkg1 AS
    PKG_VAR1 NUMBER;
END my_package;
/

CREATE OR REPLACE PROCEDURE PROC_WITH_OUT_PARAM(param1 OUT NUMBER)
AS
BEGIN
   param1 := 0;
END;
CREATE OR REPLACE PROCEDURE PROC ()
AS
BEGIN
   PROC_WITH_OUT_PARAM(param1 => scha1.pkg1.PKG_VAR1);
END;
```

##### Snowflake Scripting 33

```sql
CREATE SCHEMA IF NOT EXISTS SCHA1_PKG1
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
;

SET "SCHA1_PKG1.PKG_VAR1" = '~';

CREATE OR REPLACE PROCEDURE PROC_WITH_OUT_PARAM (param1 OUT NUMBER(38, 18))
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
   BEGIN
      param1 := 0;
   END;
$$;

CREATE OR REPLACE PROCEDURE PROC ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
   DECLARE
      SCHA1_PKG1_PKG_VAR1 VARIANT;
   BEGIN
      CALL
      PROC_WITH_OUT_PARAM(param1 => :SCHA1_PKG1_PKG_VAR1);
      CALL UPDATE_PACKAGE_VARIABLE_STATE_UDF('SCHA1_PKG1.PKG_VAR1', TO_VARCHAR(:SCHA1_PKG1_PKG_VAR1));
   END;
$$;
```

### Known Issues 16

#### 1. Procedures with output parameters inside packages may not work correctly

Currently, there is an issue collecting the semantic information of procedures that reside inside
packages, which is why the transformation for output parameters may work partially or not work at
all. There is already a work in progress to resolve this issue.

#### 2. Some data types may not work properly

As seen in the transformation, when retrieving the value from the called procedures, an implicit
cast is performed from VARIANT to the type specified by the variable. Since there are a lot of
possible data types, some casts may fail or contain different data.

### Related EWIs 16

1. [SSC-FDM-0006](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0006):
   Number type column may not behave similarly in Snowflake.
2. [SSC-FDM-0007](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0007):
   Element with missing dependencies.
3. [SSC-FDM-0015](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0015):
   Data Type Not Recognized.

## NESTED PROCEDURES

### Description 18

In Oracle’s PL/SQL, `NESTED` `PROCEDURES` definition refers to a procedure that is declared and
defined within the declarative section of another PL/SQL block. This parent block can be an another
procedure, a function, or a package body. For more information please refer to
[Oracle procedure declarations and definitions](https://docs.oracle.com/en/database/oracle/oracle-database/21/lnpls/procedure-declaration-and-definition.html#GUID-9A48D7CE-3720-46A4-B5CA-C2250CA86AF2__CJACCJID).

#### Note 33

The transformations described below are specific to procedures embedded within other procedures or
packages.

### Sample Source Patterns 17

#### IN Parameter Mode for Nested Procedures

The IN keyword will be removed, as Snowflake nested procedures only support IN parameters
implicitly.

##### Oracle 80

```sql
CREATE OR REPLACE PROCEDURE calculate_basic_salary (
    p_base_salary IN NUMBER,
    p_bonus_amount IN NUMBER
)
AS
    v_total_salary NUMBER := p_base_salary;
    PROCEDURE add_bonus (
        p_bonus_to_add IN NUMBER
    )
    AS
    BEGIN
        v_total_salary := v_total_salary + p_bonus_to_add;
        INSERT INTO salary_logs (description, result_value)
        VALUES ('Bonus added', v_total_salary);
    END add_bonus;
BEGIN
    INSERT INTO salary_logs (description, result_value)
    VALUES ('Starting calculation', v_total_salary);
    add_bonus(p_bonus_to_add => p_bonus_amount);
    INSERT INTO salary_logs (description, result_value)
    VALUES ('Final salary', v_total_salary);
END calculate_basic_salary;
```

##### Snowflake Scripting 34

```sql
CREATE OR REPLACE PROCEDURE calculate_basic_salary (p_base_salary NUMBER(38, 18), p_bonus_amount NUMBER(38, 18)
    )
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/22/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
        DECLARE
        v_total_salary NUMBER(38, 18) := :p_base_salary;
        add_bonus PROCEDURE (p_bonus_to_add NUMBER(38, 18)
           )
        RETURNS VARCHAR
        AS
            BEGIN
                v_total_salary := :v_total_salary + :p_bonus_to_add;
            INSERT INTO salary_logs(description, result_value)
            VALUES ('Bonus added', :v_total_salary);
            END;
        BEGIN
        INSERT INTO salary_logs(description, result_value)
        VALUES ('Starting calculation', :v_total_salary);
        CALL
        add_bonus(:p_bonus_amount);
        INSERT INTO salary_logs(description, result_value)
        VALUES ('Final salary', :v_total_salary);
        END;
$$;
```

#### OUT Parameter Mode for Nested Procedures

SnowScript’s nested procedures do not support output parameters. To replicate this functionality in
Snowflake, a RETURN type must be created based on the output parameters.

If there’s only one output parameter, that parameter will be returned at the end. In cases with
multiple output parameters, an object construct will be generated containing their values. During
the call, these values will be assigned to a variable, and subsequently, these results will be
assigned to the corresponding variables or parameters.

##### Oracle 81

```sql
CREATE OR REPLACE PROCEDURE calculate_net_salary (
    p_base_salary IN NUMBER,
    p_bonus_amount IN NUMBER,
    p_net_salary OUT NUMBER
)
AS
    PROCEDURE calculate_tax (
        p_gross_amount IN NUMBER,
        p_net_result OUT NUMBER
    )
    AS
    BEGIN
        p_net_result := p_gross_amount * 0.8;
    END calculate_tax;
BEGIN
    calculate_tax(p_base_salary + p_bonus_amount, p_net_salary);
END calculate_net_salary;
```

##### Snowflake Scripting 35

```sql
CREATE OR REPLACE PROCEDURE calculate_net_salary (p_base_salary NUMBER(38, 18), p_bonus_amount NUMBER(38, 18), p_net_salary OUT NUMBER(38, 18)
    )
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/22/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
        DECLARE
        calculate_tax PROCEDURE (p_gross_amount NUMBER(38, 18), p_net_result NUMBER(38, 18)
           )
        RETURNS NUMBER
        AS
            BEGIN
                p_net_result := :p_gross_amount * 0.8;
                RETURN p_net_result;
            END;
        call_results NUMBER;
        BEGIN
        call_results := (
            CALL
            calculate_tax(:p_base_salary + :p_bonus_amount, :p_net_salary)
        );
        p_net_salary := :call_results;
        END;
$$;
```

#### Multiple OUT Parameters in Nested Procedures

##### Oracle 82

```sql
CREATE OR REPLACE PROCEDURE calculate_comprehensive_salary (
    p_base_salary IN NUMBER,
    p_bonus_amount IN NUMBER,
    p_final_salary OUT NUMBER,
    p_tax_calculated OUT NUMBER,
    p_total_gross OUT NUMBER
)
AS
    l_running_total NUMBER := p_base_salary;
    l_tax_amount NUMBER;
    l_net_amount NUMBER;
    PROCEDURE calculate_all_components (
        p_base_amount IN NUMBER,
        p_bonus_amt IN NUMBER,
        p_running_total_inout IN OUT NUMBER,
        p_tax_out OUT NUMBER,
        p_net_out OUT NUMBER
    )
    AS
    BEGIN
        p_running_total_inout := p_base_amount + p_bonus_amt;
        p_tax_out := p_running_total_inout * 0.25;
        p_net_out := p_running_total_inout - p_tax_out;
    END calculate_all_components;
BEGIN
    calculate_all_components(
        p_base_amount => p_base_salary,
        p_bonus_amt => p_bonus_amount,
        p_running_total_inout => l_running_total,
        p_tax_out => l_tax_amount,
        p_net_out => l_net_amount
    );

    p_final_salary := l_net_amount;
    p_tax_calculated := l_tax_amount;
    p_total_gross := l_running_total;
END calculate_comprehensive_salary;
```

##### Snowflake Scripting 36

```sql
CREATE OR REPLACE PROCEDURE calculate_comprehensive_salary (p_base_salary NUMBER(38, 18), p_bonus_amount NUMBER(38, 18), p_final_salary OUT NUMBER(38, 18), p_tax_calculated OUT NUMBER(38, 18), p_total_gross OUT NUMBER(38, 18)
    )
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/22/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
        DECLARE
        l_running_total NUMBER(38, 18) := :p_base_salary;
        l_tax_amount NUMBER(38, 18);
        l_net_amount NUMBER(38, 18);
        calculate_all_components PROCEDURE (p_base_amount NUMBER(38, 18), p_bonus_amt NUMBER(38, 18), p_running_total_inout NUMBER(38, 18), p_tax_out NUMBER(38, 18), p_net_out NUMBER(38, 18)
           )
        RETURNS VARIANT
        AS
            BEGIN
                p_running_total_inout := :p_base_amount + :p_bonus_amt;
                p_tax_out := :p_running_total_inout * 0.25;
                p_net_out := :p_running_total_inout - :p_tax_out;
                RETURN OBJECT_CONSTRUCT('p_running_total_inout', :p_running_total_inout, 'p_tax_out', :p_tax_out, 'p_net_out', :p_net_out);
            END;
        call_results VARIANT;
        BEGIN
        call_results := (
            CALL
            calculate_all_components(:p_base_salary, :p_bonus_amount, :l_running_total, :l_tax_amount, :l_net_amount)
        );
        l_running_total := :call_results:p_running_total_inout;
        l_tax_amount := :call_results:p_tax_out;
        l_net_amount := :call_results:p_net_out;
        p_final_salary := :l_net_amount;
        p_tax_calculated := :l_tax_amount;
        p_total_gross := :l_running_total;
        END;
$$;
```

#### Multi-level Nested Procedures

Snowflake only permits one level of nesting for nested procedures. Therefore, a nested procedure
within another nested procedure is not supported. If this occurs, the transformation will include
the error
`!!!RESOLVE EWI!!! /*** SSC-EWI-0111 - ONLY ONE LEVEL OF NESTING IS ALLOWED FOR NESTED PROCEDURES IN SNOWFLAKE. ***/!!!`

##### Oracle 83

```sql
CREATE OR REPLACE PROCEDURE calculate_executive_salary (
    p_result OUT NUMBER
)
AS
    PROCEDURE calculate_senior_level (
        senior_result OUT NUMBER
    )
    AS
        PROCEDURE calculate_base_level (
            base_result OUT NUMBER
        )
        AS
        BEGIN
            base_result := 75000;
        END calculate_base_level;
    BEGIN
        calculate_base_level(senior_result);
        senior_result := senior_result * 1.5;
    END calculate_senior_level;
BEGIN
    calculate_senior_level(p_result);
END calculate_executive_salary;
```

##### Snowflake Scripting 37

```sql
CREATE OR REPLACE PROCEDURE calculate_executive_salary (p_result OUT NUMBER(38, 18)
    )
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/22/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
        DECLARE
        calculate_senior_level PROCEDURE (senior_result NUMBER(38, 18)
           )
        RETURNS NUMBER
        AS
            DECLARE
                !!!RESOLVE EWI!!! /*** SSC-EWI-0111 - ONLY ONE LEVEL OF NESTING IS ALLOWED FOR NESTED PROCEDURES IN SNOWFLAKE. ***/!!!
                PROCEDURE calculate_base_level (
                    base_result OUT NUMBER
                )
                AS
                BEGIN
                    base_result := 75000;
                END calculate_base_level;
                call_results NUMBER;
            BEGIN
                call_results := (
                CALL
                calculate_base_level(:senior_result)
                );
                senior_result := :call_results;
                senior_result := :senior_result * 1.5;
                RETURN senior_result;
            END;
        call_results NUMBER;
        BEGIN
        call_results := (
            CALL
            calculate_senior_level(:p_result)
        );
        p_result := :call_results;
        END;
$$;
```

#### Default Values in Nested Procedures

Nested procedure arguments do not support default clauses. Therefore, if a nested procedure call
omits an optional parameter, the default value for that argument must be submitted within the
procedure call. SnowConvert AI automatically identifies these scenarios and fills the procedure
calls appropriately.

##### Oracle 84

```sql
CREATE OR REPLACE PROCEDURE calculate_total_compensation (
    p_base_salary IN NUMBER,
    p_final_compensation OUT NUMBER
)
AS
    v_total NUMBER := p_base_salary;
    l_bonus NUMBER;
    PROCEDURE add_bonus (
        p_salary_amount IN NUMBER,
        p_multiplier IN NUMBER DEFAULT 1.1,
        p_calculated_bonus OUT NUMBER
    )
    AS
    BEGIN
        p_calculated_bonus := p_salary_amount * (p_multiplier - 1);
    END add_bonus;
BEGIN
    add_bonus(p_base_salary, p_calculated_bonus => l_bonus);
    v_total := v_total + l_bonus;
    add_bonus(p_base_salary, 1.2, p_calculated_bonus => l_bonus);
    v_total := v_total + l_bonus;
    p_final_compensation := v_total;
END calculate_total_compensation;
```

##### Snowflake Scripting 38

```sql
CREATE OR REPLACE PROCEDURE calculate_total_compensation (p_base_salary NUMBER(38, 18), p_final_compensation OUT NUMBER(38, 18)
    )
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/22/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
        DECLARE
        v_total NUMBER(38, 18) := :p_base_salary;
        l_bonus NUMBER(38, 18);
        add_bonus PROCEDURE (p_salary_amount NUMBER(38, 18), p_multiplier NUMBER(38, 18), p_calculated_bonus NUMBER(38, 18)
           )
        RETURNS NUMBER
        AS
            BEGIN
                p_calculated_bonus := :p_salary_amount * (:p_multiplier - 1);
                RETURN p_calculated_bonus;
            END;
        call_results NUMBER;
        BEGIN
        call_results := (
            CALL
            add_bonus(:p_base_salary, 1.1, :l_bonus)
        );
        l_bonus := :call_results;
        v_total := :v_total + :l_bonus;
        call_results := (
            CALL
            add_bonus(:p_base_salary, 1.2, :l_bonus)
        );
        l_bonus := :call_results;
        v_total := :v_total + :l_bonus;
        p_final_compensation := :v_total;
        END;
$$;
```

#### Nested Procedure Overloading

Snowflake does not support the overloading of nested procedures. If this occurs, the EWI
`SSC-EWI-0112 - NESTED PROCEDURE OVERLOADING IS NOT SUPPORTED` will be added.

##### Oracle 85

```sql
CREATE OR REPLACE PROCEDURE demonstrate_salary_calculations(
    final_summary OUT VARCHAR2
)
AS
    result1 VARCHAR2(100);
    result2 VARCHAR2(100);
    result3 VARCHAR2(100);
    PROCEDURE calculate_salary(
        output OUT VARCHAR2
    )
    AS
    BEGIN
        output := 'Standard: 55000';
    END;
    PROCEDURE calculate_salary(
        base_amount IN NUMBER,
        output OUT VARCHAR2
    )
    AS
    BEGIN
        output := 'Calculated: ' || (base_amount * 1.15);
    END;
    PROCEDURE calculate_salary(
        employee_level IN VARCHAR2,
        output OUT VARCHAR2
    )
    AS
    BEGIN
        output := 'Level ' || UPPER(employee_level) || ': 60000';
    END;
BEGIN
    calculate_salary(result1);
    calculate_salary(50000, result2);
    calculate_salary('senior', result3);
    final_summary := result1 || ' | ' || result2 || ' | ' || result3;
END demonstrate_salary_calculations;
```

##### Snowflake Scripting 39

```sql
CREATE OR REPLACE PROCEDURE demonstrate_salary_calculations (final_summary OUT VARCHAR
    )
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/22/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
        DECLARE
        result1 VARCHAR(100);
        result2 VARCHAR(100);
        result3 VARCHAR(100);
        calculate_salary PROCEDURE(output VARCHAR
            )
        RETURNS VARCHAR
        AS
            BEGIN
                output := 'Standard: 55000';
                RETURN output;
            END;
        !!!RESOLVE EWI!!! /*** SSC-EWI-0112 - NESTED PROCEDURE OVERLOADING IS NOT SUPPORTED. ***/!!!
        calculate_salary PROCEDURE(base_amount NUMBER(38, 18), output VARCHAR
            )
        RETURNS VARCHAR
        AS
            BEGIN
                output := 'Calculated: ' || NVL((:base_amount * 1.15) :: STRING, '');
                RETURN output;
            END;
        !!!RESOLVE EWI!!! /*** SSC-EWI-0112 - NESTED PROCEDURE OVERLOADING IS NOT SUPPORTED. ***/!!!
        calculate_salary PROCEDURE(employee_level VARCHAR, output VARCHAR
            )
        RETURNS VARCHAR
        AS
            BEGIN
                output := 'Level ' || NVL(UPPER(:employee_level) :: STRING, '') || ': 60000';
                RETURN output;
            END;
        call_results VARCHAR;
        BEGIN
        call_results := (
            CALL
            calculate_salary(:result1)
        );
        result1 := :call_results;
        call_results := (
            CALL
            calculate_salary(50000, :result2)
        );
        result2 := :call_results;
        call_results := (
            CALL
            calculate_salary('senior', :result3)
        );
        result3 := :call_results;
        final_summary := NVL(:result1 :: STRING, '') || ' | ' || NVL(:result2 :: STRING, '') || ' | ' || NVL(:result3 :: STRING, '');
        END;
$$;
```

#### Nested procedure without a parameter list

In Snowflake, a nested procedure definition requires empty parentheses `()` to be syntactically
valid when it has no parameters; contrary to Oracle, where they are not needed. SnowConvert AI will
add these automatically during translation.

##### Oracle 86

```sql
CREATE OR REPLACE PROCEDURE reset_salary_system
AS
    PROCEDURE cleanup_salary_data
    AS
    BEGIN
        DELETE FROM salary_results;
        INSERT INTO salary_results VALUES (0);
    END cleanup_salary_data;
BEGIN
    cleanup_salary_data();
END reset_salary_system;
```

##### Snowflake Scripting 40

```sql
CREATE OR REPLACE PROCEDURE reset_salary_system ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/22/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
        DECLARE
        cleanup_salary_data PROCEDURE ()
        RETURNS VARCHAR
        AS
            BEGIN
                DELETE FROM
                salary_results;
            INSERT INTO salary_results
                VALUES (0);
            END;
        BEGIN
        CALL
        cleanup_salary_data();
        END;
$$;
```

#### Nested procedure with REFCURSOR output parameter

##### Oracle 87

```sql
CREATE OR REPLACE PROCEDURE process_department_salaries (
    p_department_id IN NUMBER
)
AS
    v_employee_cursor SYS_REFCURSOR;
    v_employee_id employees.employee_id%TYPE;
    v_first_name employees.first_name%TYPE;
    v_last_name employees.last_name%TYPE;
    PROCEDURE get_department_employees (
        p_dept_id IN NUMBER,
        p_cursor OUT SYS_REFCURSOR
    )
    AS
    BEGIN
        OPEN p_cursor FOR
            SELECT employee_id, first_name, last_name
            FROM employees
            WHERE department_id = p_dept_id;
    END get_department_employees;
BEGIN
    get_department_employees(p_department_id, v_employee_cursor);
    LOOP
        FETCH v_employee_cursor INTO v_employee_id, v_first_name, v_last_name;
        EXIT WHEN v_employee_cursor%NOTFOUND;
        INSERT INTO salary_audit VALUES (v_employee_id, v_first_name || ' ' || v_last_name);
    END LOOP;
    CLOSE v_employee_cursor;
END process_department_salaries;
```

##### Snowflake Scripting 41

```sql
CREATE OR REPLACE PROCEDURE process_department_salaries (p_department_id NUMBER(38, 18)
    )
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/22/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
        DECLARE
        v_employee_cursor_res RESULTSET;
        v_employee_id NUMBER(38, 18);
        v_first_name VARCHAR(50);
        v_last_name VARCHAR(50);
        get_department_employees PROCEDURE (p_dept_id NUMBER(38, 18), p_cursor VARCHAR
           )
        RETURNS VARCHAR
        AS
            BEGIN
                CREATE OR REPLACE TEMPORARY TABLE IDENTIFIER(:p_cursor) AS
                SELECT employee_id, first_name, last_name
                FROM
                    employees
                WHERE department_id = :p_dept_id;
                RETURN p_cursor;
            END;
        call_results VARCHAR;
        BEGIN
        call_results := (
            CALL
            get_department_employees(:p_department_id, 'process_department_salaries_v_employee_cursor')
        );
        LET v_employee_cursor CURSOR
        FOR
            SELECT
                *
            FROM
                IDENTIFIER('process_department_salaries_v_employee_cursor');
        OPEN v_employee_cursor;
        --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
        LOOP
            --** SSC-PRF-0003 - FETCH INSIDE A LOOP IS CONSIDERED A COMPLEX PATTERN, THIS COULD DEGRADE SNOWFLAKE PERFORMANCE. **
            FETCH v_employee_cursor INTO
                :v_employee_id,
                :v_first_name,
                :v_last_name;
            IF (v_employee_id IS NULL) THEN
                EXIT;
            END IF;
            INSERT INTO salary_audit
            SELECT
                :v_employee_id,
                NVL(:v_first_name :: STRING, '') || ' ' || NVL(:v_last_name :: STRING, '');
        END LOOP;
        CLOSE v_employee_cursor;
        END;
$$;
```

#### Nested procedure with NOCOPY parameter option

In Oracle PL/SQL, the NOCOPY keyword is an optimization hint for `OUT` and `IN OUT` procedure
parameters. By default, Oracle passes these parameters by value, creating an expensive copy of the
data during the call and copying it back upon completion. This can cause significant performance
overhead for large data structures.

NOCOPY instructs Oracle to pass by reference instead, allowing the procedure to directly modify the
original data. This eliminates copying overhead and improves performance. However, changes are
immediate and are not implicitly rolled back if an unhandled exception occurs within the procedure.

Therefore, we will remove the NOCOPY parameters option and add the FDM
`SSC-FDM-OR0050 - EXCEPTIONS WITH NOCOPY PARAMETERS MAY LEAD TO DATA INCONSISTENCY`. This is because
procedure execution terminates upon hitting an exception, preventing the `RETURN` statement from
being reached. As a result, the variable in the caller’s declare block retains its initial values,
as the procedure fails to successfully return a new value for assignment.

##### Oracle 88

```sql
CREATE OR REPLACE PROCEDURE calculate_bonus_with_nocopy (
    p_base_salary IN NUMBER,
    p_multiplier IN NUMBER,
    p_bonus_result OUT NOCOPY NUMBER
)
AS
    PROCEDURE compute_bonus(bonus_amount OUT NOCOPY NUMBER)
    AS
    BEGIN
        IF p_multiplier = 0 THEN
            bonus_amount := NULL;
        ELSE
            bonus_amount := p_base_salary * p_multiplier * 0.1;
        END IF;
    END compute_bonus;
BEGIN
    compute_bonus(p_bonus_result);
END calculate_bonus_with_nocopy;
```

##### Snowflake Scripting 42

```sql
CREATE OR REPLACE PROCEDURE calculate_bonus_with_nocopy (p_base_salary NUMBER(38, 18), p_multiplier NUMBER(38, 18), p_bonus_result OUT NUMBER(38, 18)
    )
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/22/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
        DECLARE
        compute_bonus PROCEDURE(bonus_amount
        --** SSC-FDM-OR0050 - EXCEPTIONS WITH NOCOPY PARAMETERS MAY LEAD TO DATA INCONSISTENCY. **
        NUMBER(38, 18))
        RETURNS NUMBER
        AS
            BEGIN
                IF (:p_multiplier = 0) THEN
                bonus_amount := NULL;
            ELSE
                bonus_amount := :p_base_salary * :p_multiplier * 0.1;
                END IF;
                RETURN bonus_amount;
            END;
        call_results NUMBER;
        BEGIN
        call_results := (
            CALL
            compute_bonus(:p_bonus_result)
        );
        p_bonus_result := :call_results;
        END;
$$;
```

### Known Issues 17

#### 1. Multi-level Nested Procedures

Our transformation efforts for nested procedures in Snowflake are limited to those nested directly
within other procedures, supporting only one level of nesting. If the nesting level exceeds one, or
if a procedure is nested within a standalone function, transformation is not supported, and the EWI
`!!!RESOLVE EWI!!! /*** SSC-EWI-0111 - ONLY ONE LEVEL OF NESTING IS ALLOWED FOR NESTED PROCEDURES IN SNOWFLAKE. ***/!!!`
will be added.

#### 2. Nested procedures overloading

Additionally, overloading of nested procedures is not supported in Snowflake. In such cases, the EWI
`!!!RESOLVE EWI!!! /*** SSC-EWI-0112 - NESTED PROCEDURE OVERLOADING IS NOT SUPPORTED. ***/!!!` will
be added.

#### 3. Nested procedures within anonymous blocks

Transformation for nested procedures within anonymous blocks is currently pending. The EWI
`!!!RESOLVE EWI!!! /*** SSC-EWI-OR0057 - TRANSFORMATION FOR NESTED PROCEDURE OR FUNCTION IS NOT SUPPORTED IN THIS SCENARIO ***/!!!`
will be added.

### Related EWIs 17

1. [SSC-FDM-OR0050](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM#ssc-fdm-or0050):
   Exceptions with `NOCOPY` parameters may lead to data inconsistency.
2. [SSC-EWI-OR0057](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI#ssc-ewi-or0057):
   Transformation for nested procedure or function is not supported.
3. [SSC-EWI-0111](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0111):
   Only one level of nesting is allowed for nested procedures in Snowflake.
4. [SSC-EWI-0112](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0112):
   Nested procedure overloading is not supported.

## PROCEDURE CALL

Translation reference for PROCEDURE CALL aka SUBPROGRAM INVOCATION

### Note 34

Some parts in the output code are omitted for clarity reasons.

### Description 19

This section describes the syntax for subprogram invocations within PL blocks, such as procedures or
anonymous blocks.

For more information on this subject, please refer to Oracle’s Subprogram documentation:
([Oracle PL/SQL Language Reference Subprogram Invocation Statement](https://docs.oracle.com/en/database/oracle/oracle-database/21/lnpls/plsql-subprograms.html#GUID-C04B6BF9-1B19-42F9-82D8-CA137E97A024))

Procedure calls can be migrated to Snowflake as long as there are no optional parameters and their
order matches the formal parameters. Please note that Procedure invocations get migrated to a Call
statement.

#### Oracle Subprogram Invocation Syntax

```sql
<subprogram invocation> := subprogram_name [ ( [ parameter [, parameter]... ] ) ]

`<parameter>` := {
  <actual parameter>
  | <formal parameter name> => <actual parameter>
  }
```

Snowflake Scripting has support for this statement, albeit with some functional differences.

##### Snow Scripting Subprogram Invocation Syntax

```sql
<subprogram invocation> := CALL subprogram_name [ ( [ parameter [, parameter]... ] ) ]

`<parameter>` := {
  <actual parameter>
  | <formal parameter name> => <actual parameter>
  }
```

### Sample Source Patterns 18

#### Note 35

**Consider the next table and procedure for the examples below.**

#### Oracle 89

```sql
CREATE TABLE procedure_call_test_table(
    col1 INTEGER
);

-- Simple Called procedure
CREATE OR REPLACE PROCEDURE called_procedure (param1 INTEGER)
AS
BEGIN
    INSERT INTO procedure_call_test_table VALUES (param1);
END;
```

##### Snowflake 44

```sql
CREATE OR REPLACE TABLE procedure_call_test_table (
        col1 INTEGER
    )
    COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
    ;

    -- Simple Called procedure
CREATE OR REPLACE PROCEDURE called_procedure (param1 INTEGER)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        INSERT INTO procedure_call_test_table
        VALUES (:param1);
    END;
$$;
```

#### Simple call

##### Oracle 90

```sql
CREATE OR REPLACE PROCEDURE simple_calling_procedure
AS
BEGIN
    called_procedure(1);
END;

CALL simple_calling_procedure();

SELECT * FROM procedure_call_test_table;
```

##### Result 47

<!-- prettier-ignore -->
|COL1|
|---|
|1|

##### Snowflake Scripting 43

```sql
CREATE OR REPLACE PROCEDURE simple_calling_procedure ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        CALL
        called_procedure(1);
    END;
$$;

CALL simple_calling_procedure();

--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "procedure_call_test_table" **

SELECT * FROM
    procedure_call_test_table;
```

##### Result 48

<!-- prettier-ignore -->
|COL1|
|---|
|1|

#### Calling a procedure with an optional parameter

Warning

This sample contains manual intervention for some functional differences and is used to explain
them. For more information on these differences, please check the
[Known Issues section](#procedure-call) below.

##### Oracle 91

```sql
-- Procedure with optional parameters
CREATE OR REPLACE PROCEDURE proc_optional_parameters (param1 INTEGER, param2 INTEGER := 8, param3 INTEGER)
AS
BEGIN
    INSERT INTO procedure_call_test_table VALUES (param1);
    INSERT INTO procedure_call_test_table VALUES (param2);
    INSERT INTO procedure_call_test_table VALUES (param3);
END;

CREATE OR REPLACE PROCEDURE calling_procedure
AS
BEGIN
    -- positional convention
    proc_optional_parameters(1, 2, 3);

    -- named convention
    proc_optional_parameters(param1 => 4, param2 => 5, param3 => 6);

    -- named convention, second gets ommited
    proc_optional_parameters(param1 => 7, param3 => 9);

    -- named convention, different order
    proc_optional_parameters(param3 => 12, param1 => 10, param2 => 11);
END;

CALL calling_procedure();

SELECT * FROM procedure_call_test_table;
```

##### Result 49

<!-- prettier-ignore -->
|COL1|
|---|
|1|
|2|
|3|
|4|
|5|
|6|
|7|
|8|
|9|
|10|
|11|
|12|

##### Snowflake Scripting 44

```sql
-- Procedure with optional parameters
CREATE OR REPLACE PROCEDURE proc_optional_parameters
                                                     !!!RESOLVE EWI!!! /*** SSC-EWI-0002 - DEFAULT PARAMETERS MAY NEED TO BE REORDERED. SNOWFLAKE ONLY SUPPORTS DEFAULT PARAMETERS AT THE END OF THE PARAMETERS DECLARATIONS ***/!!!
                                                     (param1 INTEGER, param2 INTEGER DEFAULT 8, param3 INTEGER)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        INSERT INTO procedure_call_test_table
        VALUES (:param1);
        INSERT INTO procedure_call_test_table
        VALUES (:param2);
        INSERT INTO procedure_call_test_table
        VALUES (:param3);
    END;
$$;

CREATE OR REPLACE PROCEDURE calling_procedure ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        CALL
        -- positional convention
        proc_optional_parameters(1, 2, 3);
        CALL

        -- named convention
        proc_optional_parameters(param1 => 4, param2 => 5, param3 => 6);
        CALL

        -- named convention, second gets ommited
        proc_optional_parameters(param1 => 7, param3 => 9);
        CALL

        -- named convention, different order
        proc_optional_parameters(param1 => 10, param2 => 11, param3 => 12);
    END;
$$;

CALL calling_procedure();

SELECT * FROM
    procedure_call_test_table;
```

##### Result 50

<!-- prettier-ignore -->
|COL1|
|---|
|1|
|2|
|3|
|4|
|5|
|6|
|7|
|8|
|9|
|10|
|11|
|12|

### Known Issues 18

#### 1. Calling Subprograms with default values is not supported

Snowflake does not support setting default values for parameters. So these will need to be filled
into every call.

##### 2. Named parameters are accepted, but not functionally equivalent

These parameters will not cause any compilation errors when ran in Snowflake; however, calls still
place them in a positional manner. For this reason, the order of these parameters needs to be
checked. SnowConvert AI does not support checking nor reordering these parameters.

##### 3. Calling Subprograms with Out Parameters is not supported

Snowflake does not have support for parameter modes, however, a solution is being implemented to
emulate their functionality. To get more information about the transformation for output parameters
please go to the following article [Output Parameters](#output-parameters).

### Related EWIs 18

1. [SSC-EWI-0002](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0002):
   Default Parameters May Need To Be Reordered.
2. [SSC-FDM-0007](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0007):
   Element with missing dependencies.

## RAISE

### Description 20

> The `RAISE` statement explicitly raises an exception.
>
> Outside an exception handler, you must specify the exception name. Inside an exception handler, if
> you omit the exception name, the `RAISE` statement reraises the current
> exception.([Oracle PL/SQL Language Reference Raise Statement](https://docs.oracle.com/en/database/oracle/oracle-database/21/lnpls/RAISE-statement.html#GUID-5F58843F-84C8-4768-A7B3-0E318948A88B))

The statement is fully supported by Snowflake Scripting, but please take into account that there
might be some differences when having some Commit and Rollback Statement.

```sql
RAISE `<exception_name>` ;
```

Snowflake Scripting has support for this statement.

```sql
RAISE `<exception_name>` ;
```

### Sample Source Patterns 19

#### Simple exception throw

##### Oracle 92

```sql
CREATE OR REPLACE PROCEDURE simple_exception_throw_handle(param1 INTEGER)
IS
    my_exception EXCEPTION;
    my_other_exception EXCEPTION;
BEGIN
    IF param1 > 0
        THEN RAISE my_exception;
    END IF;
EXCEPTION
    WHEN my_exception THEN
        IF param1 = 1
            THEN RAISE;
        END IF;
        RAISE my_other_exception;
END;

--Completes without issue
CALL simple_exception_throw_handle(0);
--Throws my_exception
CALL simple_exception_throw_handle(1);
--Throws my_exception, catches then raises second my_other_exception
CALL simple_exception_throw_handle(2);
```

###### Result 51

```sql
Call completed.
-----------------------------------------------------------------------
Error starting at line : 31 in command -
CALL simple_exception_throw_handle(1)
Error report -
ORA-06510: PL/SQL: unhandled user-defined exception
ORA-06512: at "SYSTEM.SIMPLE_EXCEPTION_THROW_HANDLE", line 12
ORA-06512: at "SYSTEM.SIMPLE_EXCEPTION_THROW_HANDLE", line 7
ORA-06512: at line 1
06510. 00000 -  "PL/SQL: unhandled user-defined exception"
*Cause:    A user-defined exception was raised by PL/SQL code, but
           not handled.
*Action:   Fix the problem causing the exception or write an exception
           handler for this condition. Or you may need to contact your
           application administrator or DBA.
-----------------------------------------------------------------------
Error starting at line : 33 in command -
CALL simple_exception_throw_handle(2)
Error report -
ORA-06510: PL/SQL: unhandled user-defined exception
ORA-06512: at "SYSTEM.SIMPLE_EXCEPTION_THROW_HANDLE", line 14
ORA-06510: PL/SQL: unhandled user-defined exception
ORA-06512: at "SYSTEM.SIMPLE_EXCEPTION_THROW_HANDLE", line 7
ORA-06512: at line 1
06510. 00000 -  "PL/SQL: unhandled user-defined exception"
*Cause:    A user-defined exception was raised by PL/SQL code, but
           not handled.
*Action:   Fix the problem causing the exception or write an exception
           handler for this condition. Or you may need to contact your
           application administrator or DBA.
```

##### Snowflake Scripting 45

```sql
CREATE OR REPLACE PROCEDURE simple_exception_throw_handle (param1 INTEGER)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        my_exception EXCEPTION;
        my_other_exception EXCEPTION;
    BEGIN
        IF (:param1 > 0) THEN
            RAISE my_exception;
        END IF;
        EXCEPTION
            WHEN my_exception THEN
            IF (:param1 = 1) THEN
                    RAISE;
            END IF;
                RAISE my_other_exception;
        END;
$$;

--Completes without issue
CALL simple_exception_throw_handle(0);

--Throws my_exception
CALL simple_exception_throw_handle(1);

--Throws my_exception, catches then raises second my_other_exception
CALL simple_exception_throw_handle(2);
```

###### Result 52

```sql
Call Completed
-----------------------------------------------------------------------
Uncaught exception of type 'MY_EXCEPTION' on line 7 at position 9
-----------------------------------------------------------------------
Uncaught exception of type 'MY_OTHER_EXCEPTION' on line 14 at position 9
```

### Known Issues 19

No issues were found.

### Related EWIs 19

No related EWIs.

## RAISE_APPICATION_ERROR

Translation reference for the raise_application_error statement.

### General description 2

The procedure `RAISE_APPLICATION_ERROR` lets you issue user-defined `ORA-` error messages from
stored subprograms. That way, you can report errors to your application and avoid returning
unhandled exceptions
([`Oracle documentation`](https://docs.oracle.com/cd/B19306_01/appdev.102/b14261/errors.htm)).

#### **Oracle syntax**

```sql
raise_application_error(
      error_number, message[, {TRUE | FALSE}]);
```

##### Note 36

The `error_number` is a negative integer in the range -20000 .. -20999 and `message` is a character
string up to 2048 bytes long.

If the optional third parameter is **TRUE**, the error is placed on the stack of previous errors. If
the parameter is **FALSE** (the default), the error replaces all previous errors.

The equivalent statement in Snowflake is the RAISE clause, nevertheless, it is required to declare
the user-defined exception as a variable before calling the RAISE statement for it.

#### **Snowflake Syntax**

```sql
`<exception_name>` EXCEPTION [ ( `<exception_number>` , '`<exception_message>`' ) ] ;
```

##### Note 37

For more information review the following
[Snowflake documentation](https://docs.snowflake.com/en/sql-reference/snowflake-scripting/exception#label-snowscript-introduction-exceptions-handling-an-exception-examples).

### Sample Source Patterns 20

#### 1. Exception in functions without declaring section

In this scenario, the function without a declaring section is translated to a procedure with the
exception declaration. Please note that:

- The exception variable name is declared in upper case.
- The exception variable name is based on the description and an ending is composed of an exception
  code name followed by a consecutive number.
- The declaring section is created even though the initial function or procedure does not contain
  it.

##### Oracle 93

```sql
CREATE OR REPLACE FUNCTION TEST(
    SAMPLE_A IN NUMBER DEFAULT NULL,
    SAMPLE_B IN NUMBER DEFAULT NULL
)
RETURN NUMBER
AS
BEGIN
    raise_application_error(-20001, 'First exception message', FALSE);
    raise_application_error(-20002, 'Second exception message');
  RETURN 1;
END TEST;
```

##### Output 6

```sql
ORA-20001: First exception message
```

##### Snowflake 45

```sql
!!!RESOLVE EWI!!! /*** SSC-EWI-0068 - USER DEFINED FUNCTION WAS TRANSFORMED TO SNOWFLAKE PROCEDURE ***/!!!
CREATE OR REPLACE PROCEDURE TEST (
    SAMPLE_A NUMBER(38, 18) DEFAULT NULL,
    SAMPLE_B NUMBER(38, 18) DEFAULT NULL
)
RETURNS NUMBER(38, 18)
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/14/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
  DECLARE
    FIRST_EXCEPTION_MESSAGE_EXCEPTION_CODE_0 EXCEPTION (-20001, 'FIRST EXCEPTION MESSAGE');
    SECOND_EXCEPTION_MESSAGE_EXCEPTION_CODE_1 EXCEPTION (-20002, 'SECOND EXCEPTION MESSAGE');
  BEGIN
    --** SSC-FDM-OR0011 - ADD TO STACK OF ERRORS IS NOT SUPPORTED, BOOLEAN ARGUMENT FALSE WAS REMOVED. **
    RAISE FIRST_EXCEPTION_MESSAGE_EXCEPTION_CODE_0;
    RAISE SECOND_EXCEPTION_MESSAGE_EXCEPTION_CODE_1;
    RETURN 1;
  END;
$$;
```

##### Output 7

```sql
FIRST EXCEPTION MESSAGE
```

#### 2. Exception code number outside limits

The following example shows the translation commented out in the procedure body. It is because the
code is outside the applicable code limits in Snowflake. The solution is to change the exception
code for an available code in the query section.

##### Oracle 94

```sql
CREATE OR REPLACE FUNCTION TEST(
    SAMPLE_A IN NUMBER DEFAULT NULL,
    SAMPLE_B IN NUMBER DEFAULT NULL
)
RETURN NUMBER
AS
BEGIN
    raise_application_error(-20000, 'My exception message');
    RETURN 1;
END TEST;
```

##### Output 8

```sql
ORA-20000: My exception message
```

##### Snowflake 46

```sql
!!!RESOLVE EWI!!! /*** SSC-EWI-0068 - USER DEFINED FUNCTION WAS TRANSFORMED TO SNOWFLAKE PROCEDURE ***/!!!
CREATE OR REPLACE PROCEDURE TEST (
    SAMPLE_A NUMBER(38, 18) DEFAULT NULL,
    SAMPLE_B NUMBER(38, 18) DEFAULT NULL
)
RETURNS NUMBER(38, 18)
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/14/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        MY_EXCEPTION_MESSAGE_EXCEPTION_CODE_0 EXCEPTION (-20000, 'MY EXCEPTION MESSAGE');
    BEGIN
        !!!RESOLVE EWI!!! /*** SSC-EWI-OR0099 - EXCEPTION CODE NUMBER EXCEEDS SNOWFLAKE SCRIPTING LIMITS ***/!!!
        RAISE MY_EXCEPTION_MESSAGE_EXCEPTION_CODE_0;
        RETURN 1;
    END;
$$;
```

##### Output 9

```sql
 Invalid error code '-20,000'. Must be between -20,999 and -20,000
```

#### 3. Exception stack functionality

The exception stack functionality is not supported in Snowflake and is removed from the exception
declaration.

##### Oracle 95

```sql
CREATE OR REPLACE FUNCTION TEST(
    SAMPLE_A IN NUMBER DEFAULT NULL,
    SAMPLE_B IN NUMBER DEFAULT NULL
)
RETURN NUMBER
AS
BEGIN
    raise_application_error(-20001, 'My exception message', TRUE);
    RETURN 1;
END TEST;
```

##### Output 10

```sql
ORA-20001: My exception message
```

##### Snowflake 47

```sql
!!!RESOLVE EWI!!! /*** SSC-EWI-0068 - USER DEFINED FUNCTION WAS TRANSFORMED TO SNOWFLAKE PROCEDURE ***/!!!
CREATE OR REPLACE PROCEDURE TEST (
    SAMPLE_A NUMBER(38, 18) DEFAULT NULL,
    SAMPLE_B NUMBER(38, 18) DEFAULT NULL
)
RETURNS NUMBER(38, 18)
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/14/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        MY_EXCEPTION_MESSAGE_EXCEPTION_CODE_0 EXCEPTION (-20001, 'MY EXCEPTION MESSAGE');
    BEGIN
        --** SSC-FDM-OR0011 - ADD TO STACK OF ERRORS IS NOT SUPPORTED, BOOLEAN ARGUMENT TRUE WAS REMOVED. **
        RAISE MY_EXCEPTION_MESSAGE_EXCEPTION_CODE_0;
        RETURN 1;
    END;
$$;
```

##### Output 11

```sql
MY EXCEPTION MESSAGE
```

#### 4. Multiple exceptions with the same exception code

Multiple exceptions with the same can coexist in the declaring section and raise statements.

##### Oracle 96

```sql
CREATE OR REPLACE FUNCTION TEST(
    SAMPLE_A IN NUMBER DEFAULT NULL,
    SAMPLE_B IN NUMBER DEFAULT NULL
)
RETURN NUMBER
AS
BEGIN
    IF TRUE THEN
        raise_application_error(-20001, 'The first exception');
    ELSE
        raise_application_error(-20001, 'Other exception inside');
    END IF;
    RETURN 1;
END TEST;
```

##### Output 12

```sql
ORA-20000: The first exception
```

##### Snowflake 48

```sql
!!!RESOLVE EWI!!! /*** SSC-EWI-0068 - USER DEFINED FUNCTION WAS TRANSFORMED TO SNOWFLAKE PROCEDURE ***/!!!
CREATE OR REPLACE PROCEDURE TEST (
    SAMPLE_A NUMBER(38, 18) DEFAULT NULL,
    SAMPLE_B NUMBER(38, 18) DEFAULT NULL
)
RETURNS NUMBER(38, 18)
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/14/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        THE_FIRST_EXCEPTION_EXCEPTION_CODE_0 EXCEPTION (-20001, 'THE FIRST EXCEPTION');
        OTHER_EXCEPTION_INSIDE_EXCEPTION_CODE_1 EXCEPTION (-20001, 'OTHER EXCEPTION INSIDE');
    BEGIN
        IF (TRUE) THEN
            RAISE THE_FIRST_EXCEPTION_EXCEPTION_CODE_0;
            ELSE
            RAISE OTHER_EXCEPTION_INSIDE_EXCEPTION_CODE_1;
            END IF;
            RETURN 1;
    END;
$$;
```

##### Output 13

```sql
THE FIRST EXCEPTION
```

### Known Issues 20

1. SQLREM function may be reviewed.
2. Exception code number outside the applicable limits in Snowflake has to be changed to an
   available code exception.
3. Add to a stack of errors is not supported.

### Related EWIs 20

1. [SSC-EWI-OR0099](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI#ssc-ewi-or0099):
   The exception code exceeds the Snowflake Scripting limit.
2. [SSC-FDM-0029](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0029):
   User defined function was transformed to a Snowflake procedure.
3. [SSC-FDM-OR0011](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM#ssc-fdm-or0011):
   The boolean argument was removed because the “add to stack” options is not supported.

## UDF CALL

Translation reference for User-defined function (UDF) Call

### Note 38

Some parts in the output code are omitted for clarity reasons.

### Description 21

As is widely acknowledged, non-scalar user-defined functions (UDFs) in Oracle are converted into
Snowflake stored procedures to accommodate more intricate functionalities.

This transformation also alters the way the function is invoked, transitioning from a traditional
function call to a stored procedure call.

For additional details regarding the invocation of stored procedures, refer to the documentation
accessible here: [PROCEDURE CALL](#procedure-call).

### Sample Source Patterns 21

#### Note 39

**Consider the next function and tables for the examples below.**

#### Oracle 97

```sql
CREATE OR REPLACE FUNCTION sum_to_varchar_function(p_number1 IN NUMBER, p_number2 IN NUMBER)
RETURN VARCHAR
IS
    result VARCHAR(100);
BEGIN
    result := TO_CHAR(p_number1 + p_number2);
    RETURN result;
END sum_to_varchar_function;

CREATE TABLE example_table (
    id NUMBER,
    column1 NUMBER
);
INSERT INTO example_table VALUES (1, 15);

CREATE TABLE result_table (
    id NUMBER,
    result_col VARCHAR(100)
);
```

##### Snowflake 49

```sql
CREATE OR REPLACE FUNCTION sum_to_varchar_function (p_number1 NUMBER(38, 18), p_number2 NUMBER(38, 18))
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "11/14/2024",  "domain": "test" }}'
AS
$$
    WITH declaration_variables_cte1 AS
    (
        SELECT
            TO_CHAR(p_number1 + p_number2) AS
            result
    )
    SELECT
        result
    FROM
        declaration_variables_cte1
$$;

CREATE OR REPLACE TABLE example_table (
       id NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/,
       column1 NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/
   )
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "11/14/2024",  "domain": "test" }}'
;

INSERT INTO example_table
VALUES (1, 15);

CREATE OR REPLACE TABLE result_table (
    id NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/,
       result_col VARCHAR(100)
   )
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "11/14/2024",  "domain": "test" }}'
;
```

#### UDF Call 2

##### Oracle 98

```sql
CREATE OR REPLACE PROCEDURE procedure_calling_function(param1 IN NUMBER)
IS
    result_value VARCHAR(200);
BEGIN
    result_value := sum_to_varchar_function(3, param1);
    INSERT INTO result_table VALUES (1, result_value);
END;

BEGIN
    procedure_calling_function(5);
END;
```

##### Result 53

```sql
ID RESULT_COL
1 8
```

##### Snowflake Scripting 46

```sql
CREATE OR REPLACE PROCEDURE procedure_calling_function (param1 NUMBER(38, 18))
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        result_value VARCHAR(200);
    BEGIN
        result_value := sum_to_varchar_function(3, :param1) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'sum_to_varchar_function' NODE ***/!!!;
        INSERT INTO result_table
        VALUES (1, :result_value);
    END;
$$;

DECLARE
    call_results VARIANT;

    BEGIN
    CALL
    procedure_calling_function(5);
    RETURN call_results;
    END;
```

##### Result 54

```sql
ID RESULT_COL
1 8
```

#### UDF Call within a query

When a function call is embedded within a query, the invocation process becomes more intricate due
to Snowflake’s limitation of not being able to call procedures directly within queries. To overcome
this limitation, the procedure invocation is moved outside the query, and the result is assigned to
a variable. This variable is then referenced within the query, thereby achieving functional
equivalence. This approach allows for the execution of more complex behaviors within Snowflake
queries while adhering to the procedural constraints.

##### Oracle 99

```sql
CREATE OR REPLACE PROCEDURE procedure_calling_function(param1 IN NUMBER)
IS
    result_value VARCHAR(200);
    result_value2 VARCHAR(200);
BEGIN
    SELECT
        sum_to_varchar_function(1, param1) AS result_column,
        sum_to_varchar_function(2, param1) AS result_column2
    INTO result_value, result_value2
    FROM example_table ext;

    INSERT INTO result_table VALUES (1, result_value);
    INSERT INTO result_table VALUES (2, result_value2);
END;

BEGIN
    procedure_calling_function(5);
END;
```

##### Result 55

```sql
ID RESULT_COL
1 6
2   7
```

##### Snowflake Scripting 47

```sql
CREATE OR REPLACE PROCEDURE procedure_calling_function (param1 NUMBER(38, 18))
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        result_value VARCHAR(200);
        result_value2 VARCHAR(200);
    BEGIN
        SELECT
            sum_to_varchar_function(1, :param1) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'sum_to_varchar_function' NODE ***/!!! AS result_column,
            sum_to_varchar_function(2, :param1) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'sum_to_varchar_function' NODE ***/!!! AS result_column2
        INTO
            :result_value,
            :result_value2
        FROM
            example_table ext;

        INSERT INTO result_table
        VALUES (1, :result_value);
        INSERT INTO result_table
        VALUES (2, :result_value2);
    END;
$$;

DECLARE
    call_results VARIANT;

    BEGIN
    CALL
    procedure_calling_function(5);
    RETURN call_results;
    END;
```

##### Result 56

```sql
ID RESULT_COL
1 6
2   7
```

### Known Issues 21

#### 1. Unsupported Usage of UDFs in Queries with Query Dependencies

When calling User-Defined Functions (UDFs) within queries with query dependencies, scenarios
involving embedded functions with columns as arguments are not supported. This limitation arises
because the column values cannot be accessed from outside the query. Examples of unsupported
scenarios include:

```sql
BEGIN
    SELECT
        sum_to_varchar_function(ext.col1, ext.col2) -- columns as arguments not supported
    INTO
        result_value
    FROM example_table ext;
END;
```

The supported scenarios include function calls with other types of arguments such as literal values,
external variables, or parameters. For instance:

```sql
BEGIN
    SELECT
        sum_to_varchar_function(100, param1)
    INTO
        result_value
    FROM example_table ext;
END;
```

In the supported scenarios, the function can effectively be migrated.

### Related EWIs 21

1. [SSC-EWI-0073](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0073):
   Pending Functional Equivalence Review.
2. [SSC-FDM-0006](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0006):
   Number type column may not behave similarly in Snowflake.
3. [SSC-FDM-0029](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0029):
   User defined function was transformed to a Snowflake procedure.

## WHILE

Translation reference to convert Oracle WHILE statement to Snowflake Scripting

### Description 22

> The `WHILE` `LOOP` statement runs one or more statements while a condition is `TRUE`.
> ([Oracle PL/SQL Language Reference WHILE Statement](https://docs.oracle.com/en/database/oracle/oracle-database/21/lnpls/WHILE-LOOP-statement.html#GUID-9339C3AD-7F41-4D3F-9B2D-6FC5DCE44C6B))

#### Oracle WHILE Syntax

```sql
WHILE boolean_expression
  LOOP statement... END LOOP [ label ] ;
```

##### Snowflake Scripting WHILE Syntax

```sql
WHILE ( `<condition>` ) { DO | LOOP }
  `<statement>`;
  [ `<statement>`; ... ]
END { WHILE | LOOP } [ `<label>` ] ;
```

Oracle `WHILE` behavior can also be modified by using the statements:

- [CONTINUE](#continue)
- [EXIT](#exit)
- GOTO
- [RAISE](#raise)

### Sample Source Patterns 22

#### While simple case

##### Note 40

This case is functionally equivalent.

##### Oracle 100

```sql
CREATE TABLE while_testing_table
(
    iterator VARCHAR2(5)
);

CREATE OR REPLACE PROCEDURE while_procedure
IS
I NUMBER := 1;
J NUMBER := 10;
BEGIN
  WHILE I <> J LOOP
    INSERT INTO while_testing_table VALUES(TO_CHAR(I));
    I := I+1;
  END LOOP;
END;

CALL while_procedure();
SELECT * FROM while_testing_table;
```

##### Result 57

<!-- prettier-ignore -->
|ITERATOR|
|---|
|1|
|2|
|3|
|4|
|5|
|6|
|7|
|8|
|9|

##### Snowflake Scripting 48

```sql
CREATE OR REPLACE TABLE while_testing_table
(
    iterator VARCHAR(5)
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

CREATE OR REPLACE PROCEDURE while_procedure ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
DECLARE
    I NUMBER(38, 18) := 1;
    J NUMBER(38, 18) := 10;
BEGIN
    WHILE (:I <> :J)
    --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
    LOOP
      INSERT INTO while_testing_table
      VALUES(TO_CHAR(:I));
      I := :I +1;
    END LOOP;
END;
$$;

CALL while_procedure();

SELECT * FROM
while_testing_table;
```

##### Result 58

<!-- prettier-ignore -->
|ITERATOR|
|---|
|1|
|2|
|3|
|4|
|5|
|6|
|7|
|8|
|9|

### Known Issues 22

No issues were found.

### Related EWIs 22

No related EWIs.
