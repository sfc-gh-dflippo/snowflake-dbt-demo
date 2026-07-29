---
description: Danger
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/oracle/pl-sql-to-snowflake-scripting/cursor
title: SnowConvert AI - Oracle - CURSOR | Snowflake Documentation
---

## Description

Danger

This section covers the Translation Reference for Oracle
[Explicit Cursor](https://docs.oracle.com/en/database/oracle/oracle-database/21/lnpls/static-sql.html#GUID-89E0242F-42AC-4B21-9DF1-ACD6F4FC03B9).
For Oracle
[Cursor Variables](https://docs.oracle.com/en/database/oracle/oracle-database/21/lnpls/static-sql.html#GUID-4A6E054A-4002-418D-A1CA-DE849CD7E6D5)
there is no equivalent in Snowflake Scripting.

### Note

Some parts in the output code are omitted for clarity reasons.

Cursors are pointers that allow users to iterate through query results. For more information on
Oracle Cursors check
[here](https://docs.oracle.com/en/database/oracle/oracle-database/21/lnpls/static-sql.html#GUID-F1FE15F9-5C96-4C4E-B240-B7363D25A8F1).

### Oracle Cursor Syntax

#### Cursor Definition

```sql
CURSOR cursor
 [ ( cursor_parameter_dec [, cursor_parameter_dec ]... )]
   [ RETURN rowtype] IS select_statement ;
```

#### Cursor Open

```sql
OPEN cursor [ ( cursor_parameter [ [,] actual_cursor_parameter ]... ) ] ;
```

#### Cursor Fetch

```sql
FETCH { cursor | cursor_variable | :host_cursor_variable }
  { into_clause | bulk_collect_into_clause [ LIMIT numeric_expression ] } ;
```

#### Cursor Close

```sql
CLOSE { cursor | cursor_variable | :host_cursor_variable } ;
```

#### Cursor Attributes

```sql
named_cursor%{ ISOPEN | FOUND | NOTFOUND | ROWCOUNT }
```

#### Cursor FOR Loop

```sql
[ FOR record IN
  { cursor [ ( cursor_parameter_dec
               [ [,] cursor_parameter_dec ]... )]
  | ( select_statement )
  }
    LOOP statement... END LOOP [label] ;
```

Snowflake Scripting has support for cursors, however, they have fewer functionalities compared to
Oracle. To check more information regarding these cursors, check
[here](https://docs.snowflake.com/en/developer-guide/snowflake-scripting/cursors.html).

#### Snowflake Scripting Cursor Syntax

##### Cursor Declaration

```sql
`<cursor_name>` CURSOR FOR `<query>`
```

##### Cursor Open 2

```sql
OPEN `<cursor_name>` [ USING (bind_variable_1 [, bind_variable_2 ...] ) ] ;
```

##### Cursor Fetch 2

```sql
FETCH `<cursor_name>` INTO `<variable>` [, `<variable>` ... ] ;
```

##### Cursor Close 2

```sql
CLOSE `<cursor_name>` ;
```

##### Cursor FOR Loop 2

```sql
FOR `<row_variable>` IN `<cursor_name>` DO
    statement;
    [ statement; ... ]
END FOR [ `<label>` ] ;
```

## Sample Source Patterns

### 1. Basic cursor example

#### Oracle Cursor Example

```sql
CREATE OR REPLACE PROCEDURE basic_cursor_sample AS
    var1 VARCHAR(20);
    CURSOR cursor1 IS SELECT region_name FROM hr.regions ORDER BY region_name;
BEGIN
    OPEN cursor1;
    FETCH cursor1 INTO var1;
    CLOSE cursor1;
END;
```

##### Snowflake Scripting Cursor Example

```sql
CREATE OR REPLACE PROCEDURE basic_cursor_sample ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        var1 VARCHAR(20);
        --** SSC-PRF-0009 - PERFORMANCE REVIEW - CURSOR USAGE **
        cursor1 CURSOR
        FOR
            SELECT region_name FROM
                hr.regions
            ORDER BY region_name;
    BEGIN
        OPEN cursor1;
        FETCH cursor1 INTO
            :var1;
    CLOSE cursor1;
    END;
$$;
```

### 2. Explicit Cursor For Loop

#### Oracle Explicit Cursor For Loop Example

```sql
CREATE OR REPLACE PROCEDURE explicit_cursor_for_sample AS
    CURSOR cursor1 IS SELECT region_name FROM hr.regions ORDER BY region_name;
BEGIN
    FOR r1 IN cursor1 LOOP
        NULL;
    END LOOP;
END;
```

##### Snowflake Scripting Explicit Cursor For Loop Example

```sql
CREATE OR REPLACE PROCEDURE explicit_cursor_for_sample ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        --** SSC-PRF-0009 - PERFORMANCE REVIEW - CURSOR USAGE **
        cursor1 CURSOR
        FOR
            SELECT region_name FROM
                hr.regions
            ORDER BY region_name;
    BEGIN
                OPEN cursor1;
                --** SSC-PRF-0004 - THIS STATEMENT HAS USAGES OF CURSOR FOR LOOP **
                FOR r1 IN cursor1 DO
            NULL;
                END FOR;
                CLOSE cursor1;
    END;
$$;
```

### 3. Implicit Cursor For Loop

#### Oracle Implicit Cursor For Loop Example

```sql
CREATE OR REPLACE PROCEDURE implicit_cursor_for_sample AS
BEGIN
    FOR r1 IN (SELECT region_name FROM hr.regions ORDER BY region_name) LOOP
        NULL;
    END LOOP;
END;
```

##### Snowflake Scripting Implicit Cursor For Loop Example

```sql
CREATE OR REPLACE PROCEDURE implicit_cursor_for_sample ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        LET temporary_for_cursor_0 CURSOR
        FOR
            (SELECT region_name FROM
                    hr.regions
                ORDER BY region_name);
        --** SSC-PRF-0004 - THIS STATEMENT HAS USAGES OF CURSOR FOR LOOP **
        FOR r1 IN temporary_for_cursor_0 DO
            NULL;
        END FOR;
    END;
$$;
```

### 4. Parameterized Cursor

You can use “?” In the filter condition of the cursor at the declaration section define the bind
variable. While opening the cursor we can add the additional syntax “USING <bind_variable_1 >” to
pass the bind variable.

Below are some examples of scenarios that can occur in the use of parameters in cursors:

#### 4.1 Basic Cursor Parameterized Example

##### Oracle Parameterized Cursor Example

```sql
CREATE OR REPLACE PROCEDURE parameterized_cursor_for_sample AS
    CURSOR cursor1 (low number, high IN number) IS
        SELECT region_name FROM hr.regions WHERE region_id BETWEEN low AND high;
BEGIN
    OPEN cursor1(3,5);
    CLOSE cursor1;
END;
```

##### Snowflake Parameterized Cursor Example

```sql
CREATE OR REPLACE PROCEDURE parameterized_cursor_for_sample ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        --** SSC-PRF-0009 - PERFORMANCE REVIEW - CURSOR USAGE **
        cursor1 CURSOR
        FOR
            SELECT region_name FROM
                hr.regions
            WHERE region_id BETWEEN ? AND ?;
    BEGIN
                OPEN cursor1 USING (3, 5);
                CLOSE cursor1;
    END;
$$;
```

#### 4.2 Parameterized Cursors With Multiple Sending Parameters

##### Oracle Parameterized Cursor Example 2

```sql
CREATE OR REPLACE PROCEDURE parameterized_cursor_for_sample AS
    CURSOR cursor1 (low number DEFAULT 2, high IN number DEFAULT 7) IS
        SELECT region_name FROM hr.regions
        WHERE region_id BETWEEN low AND high OR low < 0;
BEGIN
    OPEN cursor1(3,5);
    OPEN cursor1(3);
    OPEN cursor1;
    OPEN cursor1(high => 15, low => 5);
    OPEN cursor1(high => 15);
    CLOSE cursor1;
END;
```

##### Snowflake Parameterized Cursor Example 2

```sql
CREATE OR REPLACE PROCEDURE parameterized_cursor_for_sample ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        --** SSC-PRF-0009 - PERFORMANCE REVIEW - CURSOR USAGE **
        cursor1 CURSOR
        FOR
            SELECT region_name FROM
                hr.regions
            WHERE region_id BETWEEN ? AND ?
                OR ? < 0;
    BEGIN
                OPEN cursor1 USING (3, 5, 3);
                OPEN cursor1 USING (3, 7, 3);
                OPEN cursor1 USING (2, 7, 2);
                OPEN cursor1 USING (5, 15, 5);
                OPEN cursor1 USING (2, 15, 2);
                CLOSE cursor1;
    END;
$$;
```

#### 4.3 Parameterized Cursors With Use Of Procedure Parameters In Query

##### Oracle Parameterized Cursor Example 3

```sql
CREATE OR REPLACE PROCEDURE parameterized_cursor_for_sample (high_param number) AS
    CURSOR cursor1 (low number DEFAULT 2) IS
        SELECT region_name FROM hr.regions
        WHERE region_id BETWEEN low AND high_param;
BEGIN
    OPEN cursor1(3);
    CLOSE cursor1;
END;
CALL parameterized_cursor_for_sample(5);
```

##### Snowflake Parameterized Cursor Example 3

```sql
CREATE OR REPLACE PROCEDURE parameterized_cursor_for_sample (high_param NUMBER(38, 18))
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        --** SSC-PRF-0009 - PERFORMANCE REVIEW - CURSOR USAGE **
        cursor1 CURSOR
        FOR
            SELECT region_name FROM
                hr.regions
            WHERE region_id BETWEEN ? AND ?;
    BEGIN
                OPEN cursor1 USING (3, high_param);
                CLOSE cursor1;
    END;
$$;

CALL parameterized_cursor_for_sample(5);
```

### 5. Using Cursors In Fetch And For Loop

Cursors can be controlled through the use of the FOR statement, allowing each and every record of a
cursor to be processed while the FETCH statement puts, record by record, the values returned by the
cursor into a set of variables, which may be PLSQL records

#### 5.1 Cursors For Loop

##### Oracle Cursor For Loop Example

```sql
CREATE OR REPLACE PROCEDURE p_cursors_for_loop AS
 datePlusOne TIMESTAMP;
 CURSOR c_product(low number, high number) IS
    SELECT name, price, create_on FROM products WHERE price BETWEEN low AND high;
BEGIN
    FOR record_product IN c_product(3,5)
    LOOP
      datePlusOne := record_product.create_on + 1;
      INSERT INTO sold_items values(record_product.name, record_product.price, datePlusOne);
    END LOOP;
END;
```

##### Snowflake Cursor For Loop Example

```sql
CREATE OR REPLACE PROCEDURE p_cursors_for_loop ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
 DECLARE
  datePlusOne TIMESTAMP(6);
  --** SSC-PRF-0009 - PERFORMANCE REVIEW - CURSOR USAGE **
  c_product CURSOR
  FOR
     SELECT
      OBJECT_CONSTRUCT('NAME', name, 'PRICE', price, 'CREATE_ON', create_on) sc_cursor_record FROM
      products
     WHERE price BETWEEN ? AND ?;
 BEGIN
  OPEN c_product USING (3, 5);
  --** SSC-PRF-0004 - THIS STATEMENT HAS USAGES OF CURSOR FOR LOOP **
  FOR record_product IN c_product DO
     LET record_product OBJECT := record_product.sc_cursor_record;
     datePlusOne :=
                    !!!RESOLVE EWI!!! /*** SSC-EWI-OR0036 - TYPES RESOLUTION ISSUES, ARITHMETIC OPERATION '+' MAY NOT BEHAVE CORRECTLY BETWEEN unknown AND Number ***/!!!
                    record_product.CREATE_ON + 1;
                    INSERT INTO sold_items
                    SELECT
      :record_product:NAME,
      :record_product:PRICE,
      :datePlusOne;
  END FOR;
  CLOSE c_product;
 END;
$$;
```

#### 5.2 Cursors Fetch

##### Oracle Cursor Fetch Example

```sql
CREATE OR REPLACE PROCEDURE p_cursors_fetch AS
record_product products%rowtype;
 CURSOR c_product(low number, high number) IS
    SELECT * FROM products WHERE price BETWEEN low AND high;
BEGIN
    OPEN c_product(3,5);
    LOOP
        FETCH c_product INTO record_product;
        EXIT WHEN c_product%notfound;
        INSERT INTO sold_items VALUES (record_product.name, record_product.price);
        INSERT INTO sold_items VALUES record_product;
    END LOOP;
    CLOSE c_product;
END;
```

##### Snowflake Cursor Fetch Example

```sql
CREATE OR REPLACE PROCEDURE p_cursors_fetch ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/14/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
 DECLARE
  record_product OBJECT !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - ROWTYPE DATA TYPE CONVERTED TO OBJECT ***/!!! := OBJECT_CONSTRUCT();
  --** SSC-PRF-0009 - PERFORMANCE REVIEW - CURSOR USAGE **
  c_product CURSOR
  FOR
     SELECT
      OBJECT_CONSTRUCT( *) sc_cursor_record FROM
      products
     WHERE price BETWEEN ? AND ?;
 BEGIN
  OPEN c_product USING (3, 5);
  --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
  LOOP
     --** SSC-PRF-0003 - FETCH INSIDE A LOOP IS CONSIDERED A COMPLEX PATTERN, THIS COULD DEGRADE SNOWFLAKE PERFORMANCE. **
      FETCH c_product INTO
      :record_product;
      IF (record_product IS NULL) THEN
      EXIT;
      END IF;
      INSERT INTO sold_items
      SELECT
      :record_product:NAME,
      :record_product:PRICE;
      INSERT INTO sold_items
      SELECT
      null !!!RESOLVE EWI!!! /*** SSC-EWI-OR0002 - COLUMNS FROM EXPRESSION products%rowtype NOT FOUND ***/!!!;
  END LOOP;
    CLOSE c_product;
 END;
$$;
```

## Known Issues

### 1. RETURN clause is not supported in Snowflake Scripting Cursor Declaration

The Cursor Declaration for Snowflake Scripting does not include this clause. It can be removed from
the Oracle Cursor definition to get functional equivalence.

#### 2. OPEN statement cannot pass values for declared arguments

Even though arguments can be declared for a cursor, their values cannot be assigned in Snowflake
Scripting. The best alternative is to use the `USING` clause with bind variables.

#### 3. FETCH statement cannot use records

Snowflake Scripting does not support records. However, it is possible to migrate them using the
OBJECT data type and the OBJECT_CONSTRUCT() method. For more information please see the
[Record Type Definition Section](collections-and-records.html#record-type-definition).

#### 4. FETCH BULK COLLECT INTO clause is not supported in Snowflake Scripting

Snowflake Scripting does not support the BULK COLLECT INTO clause. However, it is possible to use
ARRAY_AGG along with a temporal table to construct a new variable with the data corresponding to the
Cursor information. For more information please see the
[Collection Bulk Operations Section](collections-and-records.html#collection-bulk-operations).

#### 5. Cursor attributes do not exist in Snowflake Scripting

Oracle cursors have different attributes that allow the user to check their status like if it is
opened or the amount of fetched rows, however, these attributes regarding the cursor status do not
exist in Snowflake Scripting.

#### 6. The cursor’s query does not have access to the procedure’s variables and parameters

In Oracle, the query in the cursor declaration has access to procedure variables and parameters but
in Snowflake Scripting, it does not. The alternative to this is to use the `USING` clause with bind
variables.

#### 7. %NOTFOUND attribute is not supported in Snowflake Scripting Cursor

In Oracle can be used, before the first fetch from an open cursor, cursor_name%NOTFOUND returns TRUE
if the last fetch failed to return a row, or FALSE if the last fetch returned a row. Snowflake
Scripting does not support the use of this attribute instead it can be validated if the variable
assigned to the cursor result contains values

## Related EWIs

1. [SSC-EWI-0036](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0036):
   Data type converted to another data type.
2. [SSC-EWI-OR0002](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI#ssc-ewi-or0002):
   Columns from expression not found.
3. [SSC-EWI-OR0036](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI#ssc-ewi-or0036):
   Types resolution issues, the arithmetic operation may not behave correctly between string and
   date.
4. [SSC-PRF-0003](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/performance-review/generalPRF#ssc-prf-0003):
   Fetch inside a loop is considered a complex pattern, this could degrade Snowflake performance.
5. [SSC-PRF-0004](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/performance-review/generalPRF#ssc-prf-0004):
   This statement has usages of cursor for loop.

## CURSOR DECLARATION 2

### Note 2

Non-relevant statement.

Warning

**Notice that this statement removed from the migration; because it is a non-relevant syntax. It
means that it is not required in Snowflake.**

### Note 3

Some parts in the output code are omitted for clarity reasons.

### Description 2

This section explains the translation of the declaration of cursors in Oracle. For more information
review the following documentation about
[procedures](https://docs.oracle.com/en/database/oracle/oracle-database/19/lnpls/CREATE-PROCEDURE-statement.html#GUID-5F84DB47-B5BE-4292-848F-756BF365EC54)
and
[cursors](https://docs.oracle.com/en/database/oracle/oracle-database/19/lnpls/cursor-variable-declaration.html#GUID-CE884B31-07F0-46AA-8067-EBAF73821F3D)
in Oracle.

### Sample Source Patterns 2

#### CURSOR DECLARATION 2 2

Notice that in this example the `CURSOR` statement has been deleted. This is a non-relevant syntax
in the transformation targeted to Snowflake.

##### Oracle

```sql
CREATE PROCEDURE PROC_COLLECTIONS
AS
CURSOR C2 RETURN T1%TYPE;
BEGIN
    NULL;
END
```

##### Snowflake

```sql
CREATE OR REPLACE PROCEDURE PROC_COLLECTIONS ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        NULL;
    END;
$$;
```

### Known Issues 2

No issues were found.

### Related EWIs 2

No related EWIs.

## Cursor Variables

Translation reference for cursor variables and the OPEN FOR statement

### Note 4

Some parts in the output code are omitted for clarity reasons.

### Description 3

> A cursor variable is like an explicit cursor that is not limited to one query.
>
> ([Oracle PL/SQL Language Reference Cursor Variable Declaration](https://docs.oracle.com/en/database/oracle/oracle-database/21/lnpls/cursor-variable-declaration.html#GUID-CE884B31-07F0-46AA-8067-EBAF73821F3D))

#### Oracle Syntax

##### Ref cursor type definition

```sql
TYPE type IS REF CURSOR
  [ RETURN
    { {db_table_or_view | cursor | cursor_variable}%ROWTYPE
    | record%TYPE
    | record_type
    | ref_cursor_type
    }
  ] ;
```

##### Cursor variable declaration

```sql
cursor_variable type;
```

##### OPEN FOR statement

```sql
OPEN { cursor_variable | :host_cursor_variable}
  FOR select_statement [ using_clause ] ;
```

Warning

Snowflake Scripting has no direct equivalence with cursor variables and the `OPEN FOR` statement,
however, they can be emulated with different workarounds to get functional equivalence.

### Sample Source Patterns 3

#### 1. OPEN FOR statement with dynamic SQL inside a VARCHAR variable

##### Oracle Example

```sql
CREATE OR REPLACE PROCEDURE procedure1
AS
 query1 VARCHAR(200) := 'SELECT 123 FROM dual';
 cursor_var SYS_REFCURSOR;
BEGIN
 OPEN cursor_var FOR query1;
 CLOSE cursor_var;
END;
```

##### Snowflake Scripting Exaple

```sql
CREATE OR REPLACE PROCEDURE procedure1 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
 DECLARE
  query1 VARCHAR(200) := 'SELECT 123 FROM dual';
  cursor_var_res RESULTSET;
 BEGIN
  !!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!
  cursor_var_res := (
   EXECUTE IMMEDIATE :query1
  );
  LET cursor_var CURSOR
  FOR
   cursor_var_res;
  OPEN cursor_var;
  CLOSE cursor_var;
 END;
$$;
```

#### 2. OPEN FOR statement with dynamic SQL inside a string literal

##### Oracle Example 2

```sql
CREATE OR REPLACE PROCEDURE procedure2
AS
    cursor_var SYS_REFCURSOR;
BEGIN
    OPEN cursor_var FOR 'SELECT 123 FROM dual';
    CLOSE cursor_var;
END;
```

##### Snowflake Scripting Example

```sql
CREATE OR REPLACE PROCEDURE procedure2 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        cursor_var_res RESULTSET;
    BEGIN
        !!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!
        cursor_var_res := (
            EXECUTE IMMEDIATE 'SELECT 123 FROM dual'
        );
        LET cursor_var CURSOR
        FOR
            cursor_var_res;
        OPEN cursor_var;
        CLOSE cursor_var;
    END;
$$;
```

#### 3. OPEN FOR statement with SELECT statement

##### Oracle Example 3

```sql
CREATE OR REPLACE PROCEDURE procedure3
AS
 cursor_var SYS_REFCURSOR;
BEGIN
 OPEN cursor_var FOR SELECT 123 FROM dual;
 CLOSE cursor_var;
END;
```

##### Snowflake Scripting Example 2

```sql
CREATE OR REPLACE PROCEDURE procedure3 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
 DECLARE
  cursor_var_res RESULTSET;
 BEGIN
  LET cursor_var CURSOR
  FOR
   SELECT 123 FROM dual;
  OPEN cursor_var;
  CLOSE cursor_var;
 END;
$$;
```

#### 4. Cursor Variable declared with REF CURSOR type

##### Oracle Example 4

```sql
CREATE OR REPLACE PROCEDURE procedure4
AS
    TYPE cursor_ref_type1 IS REF CURSOR;
    query1 VARCHAR(200) := 'SELECT 123 FROM dual';
    cursor_var cursor_ref_type1;
BEGIN
    OPEN cursor_var FOR query1;
    CLOSE cursor_var;
END;
```

##### Snowflake Scripting Example 3

```sql
CREATE OR REPLACE PROCEDURE procedure4 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
--        !!!RESOLVE EWI!!! /*** SSC-EWI-0058 - FUNCTIONALITY FOR 'PL REF CURSOR TYPE DEFINITION' IS NOT CURRENTLY SUPPORTED BY SNOWFLAKE SCRIPTING ***/!!!
--        TYPE cursor_ref_type1 IS REF CURSOR;
        query1 VARCHAR(200) := 'SELECT 123 FROM dual';
        cursor_var_res RESULTSET;
    BEGIN
        !!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!
        cursor_var_res := (
            EXECUTE IMMEDIATE :query1
        );
        LET cursor_var CURSOR
        FOR
            cursor_var_res;
        OPEN cursor_var;
        CLOSE cursor_var;
    END;
$$;
```

#### 5. OPEN FOR statement with USING clause

##### Oracle Example 5

```sql
CREATE OR REPLACE PROCEDURE procedure5
AS
    query1 VARCHAR(200) := 'SELECT col1 FROM cursortable1 WHERE col1 = :a';
    column_filter INTEGER := 1;
    cursor_var SYS_REFCURSOR;
BEGIN
    OPEN cursor_var FOR query1 USING column_filter;
    CLOSE cursor_var;
END;
```

##### Snowflake Scripting Example 4

```sql
CREATE OR REPLACE PROCEDURE procedure5 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        query1 VARCHAR(200) := 'SELECT col1 FROM
   cursortable1
WHERE col1 = ?';
        column_filter INTEGER := 1;
        cursor_var_res RESULTSET;
    BEGIN
        !!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!
        cursor_var_res := (
            EXECUTE IMMEDIATE :query1 USING ( column_filter)
        );
        LET cursor_var CURSOR
        FOR
            cursor_var_res;
        OPEN cursor_var;
        CLOSE cursor_var;
    END;
$$;
```

### Known Issues 3

No issues were found.

### Related EWIs 3

1. [SSC-EWI-0030](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0030):
   The statement below has usages of dynamic SQL.
2. [SSC-EWI-0058](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0058):
   Functionality is not currently supported by Snowflake Scripting.

## PARAMETRIZED CURSOR

Parametrized Cursor is not supported by Snowflake Scripting

### Note 5

Some parts in the output code are omitted for clarity reasons.

### Description 4

Oracle supports parameters for cursors that are declared. However, Snowflake Scripting does not
support this feature, so the declaration and the usage of the cursor are not possible.

#### Example Code

##### Oracle 2

```sql
CREATE OR REPLACE PROCEDURE parametrized_cursor_sample AS
    CURSOR cursor1(param1 number) IS SELECT region_name FROM hr.regions where region_id = param1 ORDER BY region_name;
    var1 integer;
BEGIN
    OPEN cursor1(123);
    FETCH cursor1 INTO var1;
    CLOSE cursor1;
    FOR r1 IN cursor1(456) LOOP
        NULL;
    END LOOP;
END;
```

##### Snowflake 2

```sql
CREATE OR REPLACE PROCEDURE parametrized_cursor_sample ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/14/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        --** SSC-PRF-0009 - PERFORMANCE REVIEW - CURSOR USAGE **
        cursor1 CURSOR
        FOR
            SELECT
                OBJECT_CONSTRUCT('REGION_NAME', region_name) sc_cursor_record FROM
                hr.regions
            where region_id = ?
            ORDER BY region_name;
                var1 integer;
    BEGIN
                OPEN cursor1 USING (123);
                FETCH cursor1 INTO
            :var1;
    CLOSE cursor1;
                OPEN cursor1 USING (456);
                --** SSC-PRF-0004 - THIS STATEMENT HAS USAGES OF CURSOR FOR LOOP **
                FOR r1 IN cursor1 DO
            LET r1 OBJECT := r1.sc_cursor_record;
                   NULL;
                END FOR;
                CLOSE cursor1;
    END;
$$;
```

#### Recommendations

- Try using bindings for the query in the cursor and open the cursor with the `USING` clause. Keep
  in mind that a parameter that is used multiple times on a single cursor may require passing the
  variable multiple times in the `USING` clause.

##### Snowflake Query

```sql
CREATE OR REPLACE PROCEDURE PUBLIC.parametrized_cursor_sample_fixed ()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
   DECLARE
      var1 STRING;
      cursor1 CURSOR FOR SELECT region_name FROM hr.regions where region_id = ? ORDER BY region_name;
   BEGIN
      NULL;
      OPEN cursor1 USING (1);
      FETCH cursor1 INTO var1;
      CLOSE cursor1;
      OPEN cursor1 USING (2);
      FOR r1 IN cursor1 DO
         NULL;
      END FOR;
      CLOSE cursor1;
   END;
$$;
```

- Manually change the cursor to use bindings.
- If you need more support, you can email us at
  [snowconvert-support@snowflake.com](https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/oracle/pl-sql-to-snowflake-scripting/mailto:snowconvert-support%40snowflake.com)

### Related EWIs 4

1. [SSC-PRF-0004](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/performance-review/generalPRF#ssc-prf-0004):
   This statement has usages of cursor for loop.

## Workaround for cursors using parameters or procedure variables

### Description 5

This section describes how to simulate the usage of cursor parameters and procedure variables inside
the query of a cursor. The name of the variables or parameters is replaced with bindings using the
`?` sign. Then, when the cursor is opened, the values should be passed with the `USING` clause.

#### Note 6

```sql
Some parts in the output code are omitted for clarity reasons.
```

#### Cursor with local variables

Use bindings for the query in the cursor for variable or procedure parameter used and open the
cursor with the `USING` clause.

##### Oracle Cursor

```sql
CREATE OR REPLACE PROCEDURE oracle_cursor_sample
AS
    like_value VARCHAR(255);
    CURSOR c1 IS SELECT region_name FROM hr.regions WHERE region_name LIKE like_value ORDER BY region_name;
    r_name VARCHAR(255);
BEGIN
    like_value := 'E%';
    OPEN c1;
    FETCH c1 INTO r_name;
    CLOSE c1;
    like_value := 'A%';
    FOR r1 IN c1 LOOP
        NULL;
    END LOOP;
END;
```

##### Snowflake Scripting Cursor

```sql
CREATE OR REPLACE PROCEDURE oracle_cursor_sample ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/14/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        like_value VARCHAR(255);
        --** SSC-PRF-0009 - PERFORMANCE REVIEW - CURSOR USAGE **
        c1 CURSOR
        FOR
            SELECT region_name FROM
                hr.regions
            WHERE region_name LIKE ?
            ORDER BY region_name;
        r_name VARCHAR(255);
    BEGIN
        like_value := 'E%';
        OPEN c1 USING (like_value);
        FETCH c1 INTO
            :r_name;
    CLOSE c1;
        like_value := 'A%';
        OPEN c1;
        --** SSC-PRF-0004 - THIS STATEMENT HAS USAGES OF CURSOR FOR LOOP **
        FOR r1 IN c1 DO
            NULL;
        END FOR;
        CLOSE c1;
    END;
$$;
```

#### Cursor with parameters

Use bindings for the query in the cursor for each parameter used and open the cursor with the
`USING` clause. Keep in mind that a parameter that is used multiple times on a single cursor may
require passing the variable multiple times in the `USING` clause.

##### Oracle Cursor 2

```sql
CREATE OR REPLACE PROCEDURE parametrized_cursor_sample AS
    CURSOR cursor1(param1 number) IS SELECT region_name FROM hr.regions where region_id = param1 ORDER BY region_name;
    var1 integer;
BEGIN
    OPEN cursor1(123);
    FETCH cursor1 INTO var1;
    CLOSE cursor1;
    FOR r1 IN cursor1(456) LOOP
        NULL;
    END LOOP;
END;
```

##### Snowflake Scripting Cursor 2

```sql
CREATE OR REPLACE PROCEDURE parametrized_cursor_sample ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        --** SSC-PRF-0009 - PERFORMANCE REVIEW - CURSOR USAGE **
        cursor1 CURSOR
        FOR
            SELECT
                OBJECT_CONSTRUCT('REGION_NAME', region_name) sc_cursor_record FROM
                hr.regions
            where region_id = ?
            ORDER BY region_name;
                var1 integer;
    BEGIN
                OPEN cursor1 USING (123);
                FETCH cursor1 INTO
            :var1;
    CLOSE cursor1;
                OPEN cursor1 USING (456);
                --** SSC-PRF-0004 - THIS STATEMENT HAS USAGES OF CURSOR FOR LOOP **
                FOR r1 IN cursor1 DO
            LET r1 OBJECT := r1.sc_cursor_record;
                   NULL;
                END FOR;
                CLOSE cursor1;
    END;
$$;
```

### Related EWIs 5

1. [SSC-PRF-0004](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/performance-review/generalPRF#ssc-prf-0004):
   This statement has usages of cursor for loop
