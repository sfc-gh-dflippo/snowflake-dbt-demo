---
description:
  Use the CREATE PACKAGE statement to create the specification for a stored package, which is an
  encapsulated collection of related procedures, functions, and other program objects stored
  together in th
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/oracle/pl-sql-to-snowflake-scripting/packages
title: SnowConvert AI - Oracle - PACKAGES | Snowflake Documentation
---

## Description[¶](#description)

> Use the `CREATE` `PACKAGE` statement to create the specification for a stored package, which is an
> encapsulated collection of related procedures, functions, and other program objects stored
> together in the database. The package specification declares these objects. The package body,
> specified subsequently, defines these
> objects.([Oracle PL/SQL Language Reference CREATE PACKAGE Statement](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/CREATE-PACKAGE.html#GUID-40636655-899F-47D0-95CA-D58A71C94A56))

Snowflake does not have an equivalent for Oracle packages, so in order to maintain the structure,
the packages are transformed into a schema, and all its elements are defined inside it. Also, the
package and its elements are renamed to preserve the original schema name.

## BODY[¶](#body)

### Description[¶](#id1)

The header of the PACKAGE BODY is removed and each procedure or function definition is transformed
into a standalone function or procedure.

#### CREATE PACKAGE SYNTAX[¶](#create-package-syntax)

```
CREATE [ OR REPLACE ]
[ EDITIONABLE | NONEDITIONABLE ]
PACKAGE BODY plsql_package_body_source
```

### Sample Source Patterns[¶](#sample-source-patterns)

**Note:**

The following queries were transformed with the PackagesAsSchema option disabled.

#### Oracle[¶](#oracle)

```
CREATE OR REPLACE PACKAGE BODY SCHEMA1.PKG1 AS
    PROCEDURE procedure1 AS
        BEGIN
            dbms_output.put_line('hello world');
        END;
END package1;
```

##### Snowflake[¶](#snowflake)

##### Snowflake[¶](#id2)

```
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

### Known Issues[¶](#known-issues)

No issues were found.

### Related EWIs[¶](#related-ewis)

1. [SSC-FDM-OR0035](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM.html#ssc-fdm-or0035):
   DBMS_OUTPUT.PUTLINE check UDF implementation.

## Constants[¶](#constants)

Translation spec for Package Constants

### Description[¶](#id3)

PACKAGE CONSTANTS can be declared either in the package declaration or in the PACKAGE BODY. When a
package constant is used in a procedure, a new variable is declared with the same name and value as
the constant, so the resulting code is pretty similar to the input.

#### Oracle Constant declaration Syntax[¶](#oracle-constant-declaration-syntax)

```
constant CONSTANT datatype [NOT NULL] { := | DEFAULT } expression ;
```

### Sample Source Patterns[¶](#id4)

#### Sample auxiliary code[¶](#sample-auxiliary-code)

##### Oracle[¶](#id5)

```
create table table1(id number);
```

##### Snowflake[¶](#id6)

```
CREATE OR REPLACE TABLE table1 (id NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;
```

##### Oracle[¶](#id7)

```
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

##### Result[¶](#result)

<!-- prettier-ignore -->
|ID|
|---|
|9999|

##### Snowflake[¶](#id8)

```
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

##### Result[¶](#id9)

<!-- prettier-ignore -->
|ID|
|---|
|9999|

**Note:**

Note that the`PROCEDURE` definition is being removed since it is not required in Snowflake.

### Known Issues[¶](#id10)

No issues were found.

### Related EWIs[¶](#id11)

1. [SSC-FDM-0006](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0006):
   Number type column may not behave similarly in Snowflake.

## DECLARATION[¶](#declaration)

### Description[¶](#id12)

The declaration is converted to a schema, so each inner element is declared inside this schema. All
the elements present in the package are commented except for the VARIABLES which have a proper
transformation.

#### CREATE PACKAGE SYNTAX[¶](#id13)

```
CREATE [ OR REPLACE ]
[ EDITIONABLE | NONEDITIONABLE ]
PACKAGE plsql_package_source
```

### Sample Source Patterns[¶](#id14)

**Note:**

The following queries were transformed with the PackagesAsSchema option disabled.

#### Oracle[¶](#id15)

```
CREATE OR REPLACE PACKAGE SCHEMA1.PKG1 AS
   -- Function Declaration
   FUNCTION function_declaration(param1 VARCHAR) RETURN INTEGER;

   -- Procedure Declaration
   PROCEDURE procedure_declaration(param1 VARCHAR2, param2 VARCHAR2);

END PKG1;
```

##### Snowflake[¶](#id16)

```
CREATE SCHEMA IF NOT EXISTS SCHEMA1_PKG1
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;
```

**Note:**

Note that both `FUNCTION` and `PROCEDURE` definitions are being removed since they are not required
in Snowflake.

### Known Issues[¶](#id17)

No issues were found.

### Related EWIs[¶](#id18)

No related EWIs.

## VARIABLES[¶](#variables)

Translation spec for Package Variables

### Description[¶](#id19)

PACKAGE VARIABLES can be declared either in the package declaration or in the PACKAGE BODY. Due to
its behavior, these variables are converted into
[Snowflake session variables](https://docs.snowflake.com/en/sql-reference/session-variables.html) so
each usage or assignment is translated to its equivalent in Snowflake.

#### Oracle Variable declaration syntax[¶](#oracle-variable-declaration-syntax)

```
variable datatype [ [ NOT NULL] {:= | DEFAULT} expression ] ;
```

### Sample Source Patterns[¶](#id20)

#### Sample auxiliary code[¶](#id21)

##### Oracle[¶](#id22)

```
create table table1(id number);
```

##### Snowflake[¶](#id23)

```
CREATE OR REPLACE TABLE table1 (id NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;
```

#### Variable declaration[¶](#variable-declaration)

##### Oracle[¶](#id24)

```
CREATE OR REPLACE PACKAGE PKG1 AS
    package_variable NUMBER:= 100;
END PKG1;
```

##### Snowflake Scripting[¶](#snowflake-scripting)

```
CREATE SCHEMA IF NOT EXISTS PKG1
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

SET "PKG1.PACKAGE_VARIABLE" = '' || (100);
```

#### Variable Usage[¶](#variable-usage)

Package variable usages are transformed into the Snowflake
[GETVARIABLE](https://docs.snowflake.com/en/sql-reference/session-variables.html#session-variable-functions)
function which accesses the current value of a session variable. An explicit cast is added to the
original variable data type in order to maintain the functional equivalence in the operations where
these variables are used.

##### Oracle[¶](#id25)

```
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

##### Result[¶](#id26)

<!-- prettier-ignore -->
|ID|
|---|
|100|

##### Snowflake[¶](#id27)

```
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

##### Result[¶](#id28)

<!-- prettier-ignore -->
|ID|
|---|
|100|

**Note:**

Note that the `PROCEDURE` definition in the package is removed since it is not required by
Snowflake.

### Variable regular assignment[¶](#variable-regular-assignment)

When a package variable is assigned using the `:=` operator, the assignation is replaced by a
SnowConvert AI UDF called UPDATE_PACKAGE_VARIABLE_STATE which is an abstraction of the Snowflake
[SETVARIABLE](https://docs.snowflake.com/en/sql-reference/session-variables.html#session-variable-functions)
function.

Oracle

#### Oracle[¶](#id29)

```
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

##### Result[¶](#id30)

<!-- prettier-ignore -->
|ID|
|---|
|200|

#### Snowflake[¶](#id31)

```
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

##### Result[¶](#id32)

<!-- prettier-ignore -->
|ID|
|---|
|200|

**Note:**

Note that the `PROCEDURE` definition in the package is removed since it is not required by
Snowflake.

#### Variable assignment as an output argument[¶](#variable-assignment-as-an-output-argument)

When a package variable is used as an output argument a new variable is declared inside the
procedure, this variable will catch the output argument value of the procedure, and then the
variable will be used to update the session variable which refers to the package variable using the
UPDATE_PACKAGE_VARIABLE_STATE mentioned above.

##### Oracle[¶](#id33)

```
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

##### Result[¶](#id34)

<!-- prettier-ignore -->
|ID|
|---|
|1000|

##### Snowflake[¶](#id35)

```
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

##### Result[¶](#id36)

<!-- prettier-ignore -->
|ID|
|---|
|1000|

**Note:**

Note that the `PROCEDURE` definition in the package is removed since it is not required by
Snowflake.

### Known Issues[¶](#id37)

No issues were found.

### Related EWIs[¶](#id38)

1. [SSC-FDM-0006](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0006):
   Number type column may not behave similarly in Snowflake.
