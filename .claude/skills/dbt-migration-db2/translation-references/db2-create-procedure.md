---
description:
  Creates a new stored procedure or replaces an existing procedure for the current database. (IBM
  DB2 SQL Language Reference Create Procedure).
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/db2/db2-create-procedure
title: SnowConvert AI - IBM DB2 - CREATE PROCEDURE | Snowflake Documentation
---

## Description

> Creates a new stored procedure or replaces an existing procedure for the current database.
> ([IBM DB2 SQL Language Reference Create Procedure](https://www.ibm.com/docs/en/db2/12.1.0?topic=statements-create-procedure-sql)).

## Grammar Syntax

The following is a SQL syntax for creating a procedure in IBM Db2. See the full specification
[here](https://www.ibm.com/docs/en/db2/12.1.0?topic=statements-create-procedure-sql).

```sql
CREATE [ OR REPLACE ] PROCEDURE procedure_name
  ( [ parameter { , parameter }* ] )
LANGUAGE SQL
BEGIN
  statements
END;

parameter := [ IN | OUT | INOUT ] param_name data_type [ DEFAULT expression ]
```

## Sample Source Patterns

### Input Code

#### Db2

```sql
CREATE OR REPLACE PROCEDURE TEST_PROCEDURE ()
LANGUAGE SQL
BEGIN
    VALUES CURRENT_TIMESTAMP;
END;
```

#### Output Code

##### Snowflake

```sql
CREATE OR REPLACE PROCEDURE TEST_PROCEDURE ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "10/31/2025",  "domain": "no-domain-provided",  "migrationid": "tDqaAcdlYXqyx5yxM208hw==" }}'
AS
$$
   BEGIN
      SELECT
         CURRENT_TIMESTAMP      ;
   END
$$;
```

## Related EWIs

There are no issues for this transformation.

## DECLARE

### Description 2

Section to declare all the procedure variables except for loop variables. Db2 supports multiple
DECLARE sections per block statement, since Snowflake does not support this behavior they must be
merged into a single declaration statement per block.

### Grammar Syntax 2

```sql
 [ DECLARE declarations ]
```

### Sample Source Patterns 2

#### Input Code 2

##### Db2 2

```sql
CREATE OR REPLACE PROCEDURE first_procedure (first_parameter INTEGER)
LANGUAGE SQL
BEGIN
   DECLARE i INTEGER DEFAULT first_parameter;
   SELECT i;
END;

CREATE OR REPLACE PROCEDURE second_procedure (first_parameter INTEGER)
LANGUAGE SQL
BEGIN
   DECLARE i INTEGER DEFAULT first_parameter;
   DECLARE j INTEGER DEFAULT first_parameter;
   SELECT i;
END;
```

##### Output Code 2

##### Snowflake 2

```sql
CREATE OR REPLACE PROCEDURE first_procedure (first_parameter INTEGER)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "10/31/2025",  "domain": "no-domain-provided",  "migrationid": "tDqaAcdlYXqyx5yxM208hw==" }}'
AS
$$
   DECLARE
      i INTEGER DEFAULT first_parameter;
   BEGIN
      SELECT
         :i;
   END
$$;

CREATE OR REPLACE PROCEDURE second_procedure (first_parameter INTEGER)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "10/31/2025",  "domain": "no-domain-provided",  "migrationid": "tDqaAcdlYXqyx5yxM208hw==" }}'
AS
$$
   DECLARE
      i INTEGER DEFAULT first_parameter;
      j INTEGER DEFAULT first_parameter;
   BEGIN
      SELECT
         :i;
   END
$$;
```

### Known Issues

There are no known issues.

### Related EWIs 2

There are no related EWIs.

## EXCEPTION

### Description 3

Db2 handles exceptions with handlers declared in the block. A handler can be `CONTINUE` (execution
continues) or `EXIT` (leaves the block) and can catch general or specific conditions (for example,
`SQLEXCEPTION`, `SQLSTATE 'state'`, `SQLCODE code`).

### Grammar Syntax 3

```sql
DECLARE { CONTINUE | EXIT } HANDLER FOR condition
  statements;

condition := SQLEXCEPTION | SQLSTATE 'state' | SQLCODE code
```

### Sample Source Patterns 3

#### Input Code 3

##### Db2 3

```sql
CREATE OR REPLACE PROCEDURE update_employee_sp ()
LANGUAGE SQL
BEGIN
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
        INSERT INTO error_log(ts, msg) VALUES (CURRENT_TIMESTAMP, 'An exception occurred');

    SELECT var;
END;
```

##### Output Code 3

##### Snowflake 3

```sql
 CREATE OR REPLACE PROCEDURE update_employee_sp ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "10/31/2025",  "domain": "no-domain-provided",  "migrationid": "tDqaAcdlYXqyx5yxM208hw==" }}'
AS
$$
BEGIN

    SELECT var;
      EXCEPTION
         WHEN OTHER CONTINUE THEN
            INSERT INTO error_log (ts, msg) VALUES (CURRENT_TIMESTAMP, 'An exception occurred')
END
$$;
```

### Known Issues 2

There are no known issues.

### Related EWIs. 2

There are no related EWIs.

## LABEL

### Description 4

Labels are used in Db2 to qualify a block or to use the EXIT or END statement. Snowflake does not
support labels. However, a workaround is used for accessing outer-block-declared variables which can
be accessed by the fully quealified name, such as `outer_block.variable_name`

Warning

Since labels are not supported in Snowflake, an EWI will be printed.

### Grammar Syntax 4

```sql
 label : BEGIN
    statements
 END label;
```

### Sample Source Patterns 4

#### Input Code 4

##### Db2 4

```sql
CREATE OR REPLACE PROCEDURE P_DEMO_SCOPE()
BEGIN
outer_block:
BEGIN
    DECLARE v_scope_test VARCHAR(50) DEFAULT 'I am from the OUTER block';
    INSERT INTO TABLETEST(VALUE, TIME) VALUES(v_scope_test, CURRENT_TIMESTAMP);
    inner_block:
    BEGIN
    DECLARE v_scope_test VARCHAR(50) DEFAULT 'I am from the INNER block';
    SET outer_block.v_scope_test = 'The INNER block changed me!';
    INSERT INTO TABLETEST(VALUE, TIME) VALUES(v_scope_test, CURRENT_TIMESTAMP);

    END inner_block;

    INSERT INTO TABLETEST(VALUE, TIME) VALUES(v_scope_test, CURRENT_TIMESTAMP);

END outer_block;
END;
```

##### Output Code 4

##### Snowflake 4

```sql
CREATE OR REPLACE PROCEDURE P_DEMO_SCOPE ()
RETURNS VARCHAR
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "10/31/2025",  "domain": "no-domain-provided",  "migrationid": "vjqaAbThwXqZ0mSDaENBCw==" }}'
AS
$$
    BEGIN
        DECLARE
            outer_block_v_scope_test VARCHAR(50) DEFAULT 'I am from the OUTER block';
        BEGIN
            INSERT INTO TABLETEST (VALUE, TIME) VALUES(:outer_block_v_scope_test, CURRENT_TIMESTAMP);
            DECLARE
                v_scope_test VARCHAR(50) DEFAULT 'I am from the INNER block';
            BEGIN
                outer_block_v_scope_test := 'The INNER block changed me!';
            INSERT INTO TABLETEST (VALUE, TIME) VALUES(:v_scope_test, CURRENT_TIMESTAMP);
            END;

            INSERT INTO TABLETEST (VALUE, TIME) VALUES(:outer_block_v_scope_test, CURRENT_TIMESTAMP);
        END;
    END
$$;
```

### Known Issues 3

1. If a variable name is the same as a modified one, it will cause inconsistencies.

### Related EWIs 2 2

There are no related EWIs.

## VARIABLE DECLARATION

### Description 5

Declare variables inside the block’s `DECLARE` area. Variables can specify an initial value using
`DEFAULT`. Subsequent assignments use the `SET` statement.

#### Note

Variable declarations are fully supported by
[Snowflake](https://docs.snowflake.com/en/developer-guide/snowflake-scripting/variables#declaring-a-variable).

### Grammar Syntax 5

```sql
DECLARE
  name type [ DEFAULT expression ];
```

Notes:

- Use `SET name = expression;` to assign after declaration.

### Sample Source Patterns 5

#### Input Code 5

##### Db2 5

```sql
CREATE OR REPLACE PROCEDURE VARIABLE_DECLARATION ()
LANGUAGE SQL
BEGIN
    DECLARE v_simple_int INTEGER;
    DECLARE v_default_char CHAR(4) DEFAULT 'ABCD';
    DECLARE v_default_decimal DECIMAL(10,2) DEFAULT 10.00;
    DECLARE v_text VARCHAR(50) DEFAULT 'Test default';
    VALUES v_simple_int, v_default_char, v_default_decimal, v_text;
END;
```

##### Output Code 5

##### Snowflake 5

```sql
CREATE OR REPLACE PROCEDURE VARIABLE_DECLARATION ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "10/31/2025",  "domain": "no-domain-provided",  "migrationid": "tDqaAcdlYXqyx5yxM208hw==" }}'
AS
$$
   DECLARE
      v_simple_int INTEGER;
      v_default_char CHAR(4) DEFAULT 'ABCD';
      v_default_decimal DECIMAL(10,2) DEFAULT 10.00;
      v_text VARCHAR(50) DEFAULT 'Test default';
   BEGIN
      SELECT
         v_simple_int, v_default_char, v_default_decimal, v_text      ;
   END
$$;
```

### Known Issues 4

No issues were found.

### Related EWIs 3

There are no related EWIs.

## SET

### Description 6

Assign a value to a variable within a procedure block.

### Grammar Syntax 6

```sql
SET variable_name = expression;
```

### Sample Source Patterns 6

#### Input Code 6

##### Db2 6

```sql
CREATE OR REPLACE PROCEDURE PROC_SET ()
LANGUAGE SQL
BEGIN
    DECLARE v_total INTEGER DEFAULT 0;
    SET v_total = v_total + 10;
END;
```

##### Output Code 6

##### Snowflake 6

```sql
CREATE OR REPLACE PROCEDURE PROC_SET ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "10/31/2025",  "domain": "no-domain-provided",  "migrationid": "tDqaAcdlYXqyx5yxM208hw==" }}'
AS
$$
   DECLARE
      v_total INTEGER DEFAULT 0;
   BEGIN
      v_total := v_total + 10;
   END
$$;
```

## IF

### Description 7

Evaluate conditions and execute different branches. Db2 supports `ELSEIF` and an optional `ELSE`
branch.

### Grammar Syntax 7

```sql
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

### Sample Source Patterns 7

#### Input Code 7

##### Db2 7

```sql
CREATE OR REPLACE PROCEDURE PROC1 (paramNumber INTEGER)
LANGUAGE SQL
BEGIN
    DECLARE result VARCHAR(100);
    IF paramNumber = 0 THEN
      SET result = 'zero';
    ELSEIF paramNumber > 0 THEN
      SET result = 'positive';
    ELSEIF paramNumber < 0 THEN
      SET result = 'negative';
    ELSE
      SET result = 'NULL';
    END IF;
END;
```

##### Output Code 7

##### Db2 8

```sql
CREATE OR REPLACE PROCEDURE PROC1 (paramNumber INTEGER)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "10/31/2025",  "domain": "no-domain-provided",  "migrationid": "tDqaAcdlYXqyx5yxM208hw==" }}'
AS
$$
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
   END
$$;
```

### Known Issues 5

There are no known issues.

### Related EWIs. 3

There are no related EWIs.
