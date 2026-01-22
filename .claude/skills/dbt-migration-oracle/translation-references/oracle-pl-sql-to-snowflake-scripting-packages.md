---
description:
  Use the CREATE PACKAGE statement to create the specification for a stored package, which is an
  encapsulated collection of related procedures, functions, and other program objects stored
  together in th
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/oracle/pl-sql-to-snowflake-scripting/packages
title: SnowConvert AI - Oracle - PACKAGES | Snowflake Documentation
---

## Description

> Use the `CREATE` `PACKAGE` statement to create the specification for a stored package, which is an
> encapsulated collection of related procedures, functions, and other program objects stored
> together in the database. The package specification declares these objects. The package body,
> specified subsequently, defines these
> objects.([Oracle PL/SQL Language Reference CREATE PACKAGE Statement](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/CREATE-PACKAGE.html#GUID-40636655-899F-47D0-95CA-D58A71C94A56))

Snowflake does not have an equivalent for Oracle packages, so in order to maintain the structure,
the packages are transformed into a schema, and all its elements are defined inside it. Also, the
package and its elements are renamed to preserve the original schema name.

## BODY

### Description 2

The header of the PACKAGE BODY is removed and each procedure or function definition is transformed
into a standalone function or procedure.

#### CREATE PACKAGE SYNTAX

```sql
CREATE [ OR REPLACE ]
[ EDITIONABLE | NONEDITIONABLE ]
PACKAGE BODY plsql_package_body_source
```

### Sample Source Patterns

#### Note

The following queries were transformed with the PackagesAsSchema option disabled.

#### Oracle

```sql
CREATE OR REPLACE PACKAGE BODY SCHEMA1.PKG1 AS
    PROCEDURE procedure1 AS
        BEGIN
            dbms_output.put_line('hello world');
        END;
END package1;
```

##### Snowflake

##### Snowflake 2

```sql
CREATE OR REPLACE PROCEDURE SCHEMA1_PKG1.procedure1 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        --** SSC-FDM-OR0035 - CHECK UDF IMPLEMENTATION FOR DBMS_OUTPUT.PUT_LINE_UDF. **
        CALL DBMS_OUTPUT.PUT_LINE_UDF('hello world');
    END;
$$;
```

### Known Issues

No issues were found.

### Related EWIs

1. [SSC-FDM-OR0035](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM#ssc-fdm-or0035):
   DBMS_OUTPUT.PUTLINE check UDF implementation.

## Constants

Translation spec for Package Constants

### Description 3

PACKAGE CONSTANTS can be declared either in the package declaration or in the PACKAGE BODY. When a
package constant is used in a procedure, a new variable is declared with the same name and value as
the constant, so the resulting code is pretty similar to the input.

#### Oracle Constant declaration Syntax

```sql
constant CONSTANT datatype [NOT NULL] { := | DEFAULT } expression ;
```

### Sample Source Patterns 2

#### Sample auxiliary code

##### Oracle 2

```sql
create table table1(id number);
```

##### Snowflake 3

```sql
CREATE OR REPLACE TABLE table1 (id NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;
```

##### Oracle 3

```sql
CREATE OR REPLACE PACKAGE PKG1 AS
    PROCEDURE procedure1;
    package_constant CONSTANT NUMBER:= 9999;
END PKG1;

CREATE OR REPLACE PACKAGE BODY PKG1 AS
    PROCEDURE procedure1 AS
    BEGIN
        INSERT INTO TABLE1(ID) VALUES(package_constant);
    END;
END PKG1;

CALL PKG1.procedure1();

SELECT * FROM TABLE1;
```

##### Result

<!-- prettier-ignore -->
|ID|
|---|
|9999|

##### Snowflake 4

```sql
CREATE SCHEMA IF NOT EXISTS PKG1
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

CREATE OR REPLACE PROCEDURE PKG1.procedure1 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        PACKAGE_CONSTANT NUMBER := 9999;
    BEGIN
        INSERT INTO TABLE1(ID) VALUES(:PACKAGE_CONSTANT);
    END;
$$;

CALL PKG1.procedure1();

SELECT * FROM
    TABLE1;
```

##### Result 2

<!-- prettier-ignore -->
|ID|
|---|
|9999|

###### Note 2

Note that the`PROCEDURE` definition is being removed since it is not required in Snowflake.

### Known Issues 2

No issues were found.

### Related EWIs 2

1. [SSC-FDM-0006](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0006):
   Number type column may not behave similarly in Snowflake.

## DECLARATION

### Description 4

The declaration is converted to a schema, so each inner element is declared inside this schema. All
the elements present in the package are commented except for the VARIABLES which have a proper
transformation.

#### CREATE PACKAGE SYNTAX 2

```sql
CREATE [ OR REPLACE ]
[ EDITIONABLE | NONEDITIONABLE ]
PACKAGE plsql_package_source
```

### Sample Source Patterns 3

#### Note 3

The following queries were transformed with the PackagesAsSchema option disabled.

#### Oracle 4

```sql
CREATE OR REPLACE PACKAGE SCHEMA1.PKG1 AS
   -- Function Declaration
   FUNCTION function_declaration(param1 VARCHAR) RETURN INTEGER;

   -- Procedure Declaration
   PROCEDURE procedure_declaration(param1 VARCHAR2, param2 VARCHAR2);

END PKG1;
```

##### Snowflake 5

```sql
CREATE SCHEMA IF NOT EXISTS SCHEMA1_PKG1
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;
```

###### Note 4

Note that both `FUNCTION` and `PROCEDURE` definitions are being removed since they are not required
in Snowflake.

### Known Issues 3

No issues were found.

### Related EWIs 3

No related EWIs.

## VARIABLES

Translation spec for Package Variables

### Description 5

PACKAGE VARIABLES can be declared either in the package declaration or in the PACKAGE BODY. Due to
its behavior, these variables are converted into
[Snowflake session variables](https://docs.snowflake.com/en/sql-reference/session-variables.html) so
each usage or assignment is translated to its equivalent in Snowflake.

#### Oracle Variable declaration syntax

```sql
variable datatype [ [ NOT NULL] {:= | DEFAULT} expression ] ;
```

### Sample Source Patterns 4

#### Sample auxiliary code 2

##### Oracle 5

```sql
create table table1(id number);
```

##### Snowflake 6

```sql
CREATE OR REPLACE TABLE table1 (id NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;
```

#### Variable declaration

##### Oracle 6

```sql
CREATE OR REPLACE PACKAGE PKG1 AS
    package_variable NUMBER:= 100;
END PKG1;
```

##### Snowflake Scripting

```sql
CREATE SCHEMA IF NOT EXISTS PKG1
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

SET "PKG1.PACKAGE_VARIABLE" = '' || (100);
```

#### Variable Usage

Package variable usages are transformed into the Snowflake
[GETVARIABLE](https://docs.snowflake.com/en/sql-reference/session-variables.html#session-variable-functions)
function which accesses the current value of a session variable. An explicit cast is added to the
original variable data type in order to maintain the functional equivalence in the operations where
these variables are used.

##### Oracle 7

```sql
CREATE OR REPLACE PACKAGE PKG1 AS
    PROCEDURE procedure1;
    package_variable NUMBER:= 100;
END PKG1;

CREATE OR REPLACE PACKAGE BODY PKG1 AS
    PROCEDURE procedure1 AS
    BEGIN
        INSERT INTO TABLE1(ID) VALUES(package_variable);
    END;
END PKG1;

CALL SCHEMA1.PKG1.procedure1();

SELECT * FROM TABLE1;
```

##### Result 3

<!-- prettier-ignore -->
|ID|
|---|
|100|

##### Snowflake 7

```sql
CREATE SCHEMA IF NOT EXISTS PKG1
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

SET "PKG1.PACKAGE_VARIABLE" = '' || (100);

CREATE OR REPLACE PROCEDURE PKG1.procedure1 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        INSERT INTO TABLE1(ID) VALUES(GETVARIABLE('PKG1.PACKAGE_VARIABLE') :: NUMBER);
    END;
$$;

CALL SCHEMA1.PKG1.procedure1();

SELECT * FROM
    TABLE1;
```

##### Result 4

<!-- prettier-ignore -->
|ID|
|---|
|100|

###### Note 5

Note that the `PROCEDURE` definition in the package is removed since it is not required by
Snowflake.

### Variable regular assignment

When a package variable is assigned using the `:=` operator, the assignation is replaced by a
SnowConvert AI UDF called UPDATE_PACKAGE_VARIABLE_STATE which is an abstraction of the Snowflake
[SETVARIABLE](https://docs.snowflake.com/en/sql-reference/session-variables.html#session-variable-functions)
function.

Oracle

#### Oracle 8

```sql
CREATE OR REPLACE PACKAGE PKG1 AS
    PROCEDURE procedure1;
    package_variable NUMBER:= 100;
END PKG1;

CREATE OR REPLACE PACKAGE BODY PKG1 AS
    PROCEDURE procedure1 AS
    BEGIN
        package_variable := package_variable + 100;
        INSERT INTO TABLE1(ID) VALUES(package_variable);
    END;
END PKG1;

CALL PKG1.procedure1();

SELECT * FROM TABLE1;
```

##### Result 5

<!-- prettier-ignore -->
|ID|
|---|
|200|

#### Snowflake 8

```sql
CREATE SCHEMA IF NOT EXISTS PKG1
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

SET "PKG1.PACKAGE_VARIABLE" = '' || (100);

CREATE OR REPLACE PROCEDURE PKG1.procedure1 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        CALL UPDATE_PACKAGE_VARIABLE_STATE_UDF('PKG1.PACKAGE_VARIABLE', TO_VARCHAR(GETVARIABLE('PKG1.PACKAGE_VARIABLE') :: NUMBER + 100));
        INSERT INTO TABLE1(ID) VALUES(GETVARIABLE('PKG1.PACKAGE_VARIABLE') :: NUMBER);
    END;
$$;

CALL PKG1.procedure1();

SELECT * FROM
    TABLE1;
```

##### Result 6

<!-- prettier-ignore -->
|ID|
|---|
|200|

###### Note 6

Note that the `PROCEDURE` definition in the package is removed since it is not required by
Snowflake.

#### Variable assignment as an output argument

When a package variable is used as an output argument a new variable is declared inside the
procedure, this variable will catch the output argument value of the procedure, and then the
variable will be used to update the session variable which refers to the package variable using the
UPDATE_PACKAGE_VARIABLE_STATE mentioned above.

##### Oracle 9

```sql
CREATE OR REPLACE PACKAGE PKG1 AS
    PROCEDURE procedure1;
    PROCEDURE procedure2(out_param OUT NUMBER);
    package_variable NUMBER:= 100;
END PKG1;

CREATE OR REPLACE PACKAGE BODY PKG1 AS
    PROCEDURE procedure1 AS
    BEGIN
        procedure2(package_variable);
        INSERT INTO TABLE1(ID) VALUES(package_variable);
    END;
    PROCEDURE procedure2 (out_param OUT NUMBER) AS
    BEGIN
        out_param := 1000;
    END;
END PKG1;

CALL PKG1.procedure1();
```

##### Result 7

<!-- prettier-ignore -->
|ID|
|---|
|1000|

##### Snowflake 9

```sql
CREATE SCHEMA IF NOT EXISTS PKG1
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
;

SET "PKG1.PACKAGE_VARIABLE" = '' || (100);

--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "TABLE1" **
CREATE OR REPLACE PROCEDURE PKG1.procedure1 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        PKG1_PACKAGE_VARIABLE VARIANT;
    BEGIN
        CALL PKG1.
        procedure2(:PKG1_PACKAGE_VARIABLE);
        CALL UPDATE_PACKAGE_VARIABLE_STATE_UDF('PKG1.PACKAGE_VARIABLE', TO_VARCHAR(:PKG1_PACKAGE_VARIABLE));
        INSERT INTO TABLE1(ID) VALUES(GETVARIABLE('PKG1.PACKAGE_VARIABLE') :: NUMBER);
    END;
$$;

CREATE OR REPLACE PROCEDURE PKG1.procedure2 (out_param OUT NUMBER(38, 18))
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        out_param := 1000;
    END;
$$;

CALL PKG1.procedure1();
```

##### Result 8

<!-- prettier-ignore -->
|ID|
|---|
|1000|

###### Note 7

Note that the `PROCEDURE` definition in the package is removed since it is not required by
Snowflake.

### Known Issues 4

No issues were found.

### Related EWIs 4

1. [SSC-FDM-0006](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0006):
   Number type column may not behave similarly in Snowflake.
