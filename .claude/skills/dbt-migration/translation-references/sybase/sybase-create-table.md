---
description:
  Creates a new table in the current database. You define a list of columns, which each hold data of
  a distinct type. The owner of the table is the issuer of the CREATE TABLE command.
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/sybase/sybase-create-table
title: SnowConvert AI - Sybase IQ - CREATE TABLE | Snowflake Documentation
---

## Description[¶](#description)

Creates a new table in the current database. You define a list of columns, which each hold data of a
distinct type. The owner of the table is the issuer of the CREATE TABLE command.

For more information, please refer to
[`CREATE TABLE`](https://help.sap.com/docs/SAP_IQ/a898e08b84f21015969fa437e89860c8/a619764084f21015b8039a8346dc622c.html)
documentation.

## Grammar Syntax [¶](#grammar-syntax)

```
 CREATE [ { GLOBAL | LOCAL } TEMPORARY ] TABLE
   [ IF NOT EXISTS ] [ <owner>. ]<table-name>
   … ( <column-definition> [ <column-constraint> ] …
   [ , <column-definition> [ <column-constraint> ] …]
   [ , <table-constraint> ] … )
   |{ ENABLE | DISABLE } RLV STORE

   …[ IN <dbspace-name> ]
   …[ ON COMMIT { DELETE | PRESERVE } ROWS ]
   [ AT <location-string> ]
   [PARTITION BY
     <range-partitioning-scheme>
     | <hash-partitioning-scheme>
     | <composite-partitioning-scheme> ]

<column-definition> ::=
   <column-name> <data-type>
    [ [ NOT ] NULL ]
    [ DEFAULT <default-value> | IDENTITY ]
    [ PARTITION | SUBPARTITION ( <partition-name> IN  <dbspace-name> [ , ... ] ) ]

<default-value> ::=
   <special-value>
   | <string>
   | <global variable>
   | [ - ] <number>
   | ( <constant-expression> )
   | <built-in-function>( <constant-expression> )
   | AUTOINCREMENT
   | CURRENT DATABASE
   | CURRENT REMOTE USER
   | NULL
   | TIMESTAMP
   | LAST USER

<special-value> ::=
   CURRENT
   { DATE | TIME | TIMESTAMP | USER | PUBLISHER }
   | USER

<column-constraint> ::=
   IQ UNIQUE ( <integer> )
   | { [ CONSTRAINT <constraint-name> ]
     { UNIQUE
        | PRIMARY KEY
        | REFERENCES <table-name> [ ( <column-name> ) ] [ ON { UPDATE | DELETE } RESTRICT ] }
      [ IN <dbspace-name> ]
      | CHECK ( <condition> )
   }

<table-constraint> ::=
    [ CONSTRAINT <constraint-name> ]
   {  { UNIQUE | PRIMARY KEY } ( <column-name> [ , … ] )
     [ IN <dbspace-name> ]
     | <foreign-key-constraint>
     | CHECK ( <condition> )
   }

<foreign-key-constraint> ::=
   FOREIGN KEY [ <role-name> ] [ ( <column-name> [ , <column-name> ] … ) ]
   …REFERENCES <table-name> [ ( <column-name> [ , <column-name> ] … ) ]
   …[ <actions> ] [ IN <dbspace-name> ]

<actions> ::=
   [ ON { UPDATE | DELETE } RESTRICT ]

<location-string> ::=
   { <remote-server-name>. [ <db-name> ].[ <owner> ].<object-name>
      | <remote-server-name>; [ <db-name> ]; [ <owner> ];<object-name> }

<range-partitioning-scheme> ::=
   RANGE ( <partition-key> ) ( <range-partition-decl> [,<range-partition-decl> … ] )

<partition-key> ::= <column-name>

<range-partition-declaration> ::=
    <range-partition-name> VALUES <= ( {<constant> |  MAX } ) [ IN <dbspace-name> ]

<hash-partitioning-scheme> ::=
   HASH ( <partition-key> [ , <partition-key>, … ] )

<composite-partitioning-scheme> ::=
   <hash-partitioning-scheme> SUBPARTITION BY <range-partitioning-scheme>
```

Copy

## TEMPORARY TABLES[¶](#temporary-tables)

### Description[¶](#id1)

In Sybase IQ `GLOBAL | LOCAL TEMPORARY` is used to create temporary tables that exist only for the
session. These tables are session-specific and automatically deleted when the session ends. They
help store intermediate results or work data without affecting the permanent database schema. It
also can be created only by adding an `#` at the beginning of the name.

Warning

This syntax is partially supported in Snowflake.

### Grammar Syntax[¶](#id2)

```
 CREATE [ { GLOBAL | LOCAL } TEMPORARY ] TABLE
```

Copy

### Sample Source Patterns[¶](#sample-source-patterns)

#### Input Code:[¶](#input-code)

##### Sybase[¶](#sybase)

```
 CREATE LOCAL TEMPORARY TABLE TABLE01 (
    col1 INTEGER
);

CREATE GLOBAL TEMPORARY TABLE TABLE02 (
    col1 INTEGER
);

CREATE TABLE #TABLE03(
    col1 INTEGER
);
```

Copy

##### Output Code:[¶](#output-code)

##### Sybase[¶](#id3)

```
 CREATE OR REPLACE TEMPORARY TABLE TABLE01 (
    col1 INTEGER
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "sybase",  "convertedOn": "03/19/2025",  "domain": "test" }}'
;

--** SSC-FDM-0009 - GLOBAL TEMPORARY TABLE FUNCTIONALITY NOT SUPPORTED. **
CREATE OR REPLACE TABLE TABLE02 (
    col1 INTEGER
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "sybase",  "convertedOn": "03/19/2025",  "domain": "test" }}'
;

CREATE OR REPLACE TEMPORARY TABLE T_TABLE03 (
    col1 INTEGER
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "sybase",  "convertedOn": "03/19/2025",  "domain": "test" }}'
;
```

Copy

### Related EWIs[¶](#related-ewis)

[SSC-FDM-0009](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0009):
GLOBAL TEMPORARY TABLE functionality not supported.

## IF NOT EXISTS[¶](#if-not-exists)

### Description[¶](#id4)

> Ensures the table is created only if it does not already exist, preventing duplication and errors
> in your SQL script.
> ([Sybase SQL Language Reference](https://help.sap.com/docs/SAP_IQ/a898e08b84f21015969fa437e89860c8/a619764084f21015b8039a8346dc622c.html)).

SuccessPlaceholder

This syntax is fully supported in Snowflake.

### Grammar Syntax[¶](#id5)

```
 IF NOT EXISTS
```

Copy

### Sample Source Patterns[¶](#id6)

#### Input Code:[¶](#id7)

##### Sybase[¶](#id8)

```
 CREATE TABLE IF NOT EXISTS table1 (
    col1 INTEGER
);
```

Copy

##### Output Code:[¶](#id9)

##### Snowflake[¶](#snowflake)

```
 CREATE TABLE IF NOT EXISTS table1 (
    col1 INTEGER
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "sybase",  "convertedOn": "03/19/2024" }}';
```

Copy

## (ENABLE | DISABLE) RLV STORE[¶](#enable-disable-rlv-store)

### Description[¶](#id10)

> Controls Row-Level Versioning Store functionality.
> ([Sybase SQL Language Reference](https://help.sap.com/docs/SAP_IQ/a898e08b84f21015969fa437e89860c8/a619764084f21015b8039a8346dc622c.html)).

Note

This syntax is not needed in Snowflake.

### Grammar Syntax[¶](#id11)

```
 { ENABLE | DISABLE } RLV STORE
```

Copy

### Sample Source Patterns[¶](#id12)

#### Input Code:[¶](#id13)

##### Sybase[¶](#id14)

```
 CREATE TABLE rlv_table
(id INT)
ENABLE RLV STORE;
```

Copy

##### Output Code:[¶](#id15)

##### Snowflake[¶](#id16)

```
 CREATE OR REPLACE TABLE rlv_table
(
id INT
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "sybase",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
;
```

Copy

## IN DBSPACE[¶](#in-dbspace)

### Description[¶](#id17)

> Specifies the DB space for data storage.
> ([Sybase SQL Language Reference](https://help.sap.com/docs/SAP_IQ/a898e08b84f21015969fa437e89860c8/a619764084f21015b8039a8346dc622c.html)).

Note

This syntax is not needed in Snowflake. Snowflake automatically handles storage.

### Grammar Syntax[¶](#id18)

```
 IN <dbspace-name>
```

Copy

### Sample Source Patterns[¶](#id19)

#### Input Code:[¶](#id20)

##### Sybase[¶](#id21)

```
 CREATE TABLE dbspace_table (
    id INT PRIMARY KEY
)
IN my_dbspace;
```

Copy

##### Output Code:[¶](#id22)

##### Snowflake[¶](#id23)

```
 CREATE OR REPLACE TABLE dbspace_table (
    id INT PRIMARY KEY
);
```

Copy

## ON COMMIT[¶](#on-commit)

### Description[¶](#id24)

> Specifies the behaviour of the temporary table when a commit is done.
> ([Sybase SQL Language Reference](https://help.sap.com/docs/SAP_IQ/a898e08b84f21015969fa437e89860c8/a619764084f21015b8039a8346dc622c.html))

Warning

This syntax is partially supported.

### Grammar Syntax[¶](#id25)

```
 [ ON COMMIT { DELETE | PRESERVE } ROWS ]
```

Copy

### Sample Source Patterns[¶](#id26)

#### Input Code:[¶](#id27)

##### Sybase[¶](#id28)

```
 CREATE LOCAL TEMPORARY TABLE temp_employees (
    DATA VARCHAR(255)
) ON COMMIT DELETE ROWS;

CREATE LOCAL TEMPORARY TABLE temp_projects (
    DATA VARCHAR(255)
) ON COMMIT PRESERVE ROWS;
```

Copy

##### Output Code:[¶](#id29)

##### Snowflake[¶](#id30)

```
 CREATE OR REPLACE TEMPORARY TABLE temp_employees (
    DATA VARCHAR(255)
)
--    --** SSC-FDM-0008 - ON COMMIT NOT SUPPORTED **
--    ON COMMIT DELETE ROWS
    COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "sybase",  "convertedOn": "03/19/2025",  "domain": "test" }}'
;

CREATE OR REPLACE TEMPORARY TABLE temp_projects (
    DATA VARCHAR(255)
) ON COMMIT PRESERVE ROWS
    COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "sybase",  "convertedOn": "03/19/2025",  "domain": "test" }}'
;
```

Copy

### Related EWIs[¶](#id31)

[SSC-FDM-0008](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0008):
On Commit not supported.

## AT LOCATION[¶](#at-location)

### Description[¶](#id32)

> Creates a remote table (proxy).
> ([Sybase SQL Language Reference](https://help.sap.com/docs/SAP_IQ/a898e08b84f21015969fa437e89860c8/a619764084f21015b8039a8346dc622c.html))

Danger

This syntax is not supported in Snowflake.

### Grammar Syntax[¶](#id33)

```
 AT <location-string>
```

Copy

### Sample Source Patterns[¶](#id34)

#### Input Code:[¶](#id35)

##### Sybase[¶](#id36)

```
 CREATE TABLE t1
(
    DATA VARCHAR(10)
)
AT 'SERVER_A.db1.joe.t1';
```

Copy

##### Output Code:[¶](#id37)

##### Snowflake[¶](#id38)

```
 CREATE OR REPLACE TABLE t1
(
    DATA VARCHAR(10)
)
    !!!RESOLVE EWI!!! /*** SSC-EWI-SY0002 - UNSUPPORTED REMOTE TABLE SYNTAX ***/!!!
AT 'SERVER_A.db1.joe.t1'
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "sybase",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
;
```

Copy

### Related EWIs[¶](#id39)

[SSC-EWI-SY0002](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/sybaseEWI.html#ssc-ewi-sy0002):
UNSUPPORTED REMOTE TABLE SYNTAX.

## PARTITION BY[¶](#partition-by)

### Description[¶](#id40)

> All rows of a table partition are physically colocated.
> ([Sybase SQL Language Reference](https://help.sap.com/docs/SAP_IQ/a898e08b84f21015969fa437e89860c8/a619764084f21015b8039a8346dc622c.html))

Note

This syntax is not needed in Snowflake.

### Grammar Syntax[¶](#id41)

```
 PARTITION BY
     <range-partitioning-scheme>
     | <hash-partitioning-scheme>
     | <composite-partitioning-scheme>

<range-partitioning-scheme> ::=
   RANGE ( <partition-key> ) ( <range-partition-decl> [,<range-partition-decl> … ] )

<partition-key> ::= <column-name>

<range-partition-declaration> ::=
    <range-partition-name> VALUES <= ( {<constant> |  MAX } ) [ IN <dbspace-name> ]

<hash-partitioning-scheme> ::=
   HASH ( <partition-key> [ , <partition-key>, … ] )

<composite-partitioning-scheme> ::=
   <hash-partitioning-scheme> SUBPARTITION BY <range-partitioning-scheme>
```

Copy

### Sample Source Patterns[¶](#id42)

#### Input Code:[¶](#id43)

##### Sybase[¶](#id44)

```
 -- Range Partitioning
CREATE TABLE sales (
    sale_id INT,
    sale_date DATE,
    amount DECIMAL(10, 2)
)
PARTITION BY RANGE (sale_date) (
    p1 VALUES <= ('2023-01-01'),
    p2 VALUES <= ('2024-01-01'),
    p3 VALUES <= (MAXVALUE)
);

-- Hash Partitioning
CREATE TABLE customers (
    customer_id INT,
    customer_name VARCHAR(255)
)
PARTITION BY HASH (customer_id);

-- Composite Partitioning (Hash-Range)
CREATE TABLE orders (
    order_id INT,
    customer_id INT,
    order_date DATE,
    amount DECIMAL(10,2)
)
PARTITION BY HASH (customer_id)
SUBPARTITION BY RANGE (order_date) (
    p1 VALUES <= ('2023-01-01'),
    p2 VALUES <= ('2024-01-01'),
    p3 VALUES <= (MAXVALUE)
);
```

Copy

##### Output Code:[¶](#id45)

##### Snowflake[¶](#id46)

```
 -- Range Partitioning
CREATE OR REPLACE TABLE sales (
    sale_id INT,
    sale_date DATE,
    amount DECIMAL(10, 2)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "sybase",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
;

-- Hash Partitioning
CREATE OR REPLACE TABLE customers (
    customer_id INT,
    customer_name VARCHAR(255)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "sybase",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
;

-- Composite Partitioning (Hash-Range)
CREATE OR REPLACE TABLE orders (
    order_id INT,
    customer_id INT,
    order_date DATE,
    amount DECIMAL(10,2)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "sybase",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
;
```

Copy

## CONSTRAINTS[¶](#constraints)

### Description[¶](#id47)

> This ensures the accuracy and reliability of the data in the table. If there is any violation
> between the constraint and the data action, the action is aborted.
> ([Sybase SQL Language Reference](https://help.sap.com/docs/SAP_IQ/a898e08b84f21015969fa437e89860c8/a619764084f21015b8039a8346dc622c.html))

Warning

This syntax is partially supported.

### Grammar Syntax[¶](#id48)

```
 <table-constraint> ::=
    [ CONSTRAINT <constraint-name> ]
   {  { UNIQUE | PRIMARY KEY } ( <column-name> [ , … ] )
     [ IN <dbspace-name> ]
     | <foreign-key-constraint>
     | CHECK ( <condition> )
   }

<foreign-key-constraint> ::=
   FOREIGN KEY [ <role-name> ] [ ( <column-name> [ , <column-name> ] … ) ]
   …REFERENCES <table-name> [ ( <column-name> [ , <column-name> ] … ) ]
   …[ <actions> ] [ IN <dbspace-name> ]

<actions> ::=
   [ ON { UPDATE | DELETE } RESTRICT ]
```

Copy

### Sample Source Patterns[¶](#id49)

#### Input Code:[¶](#id50)

##### Sybase[¶](#id51)

```
 CREATE TABLE t_constraint (
    id1 INT NOT NULL,
    id2 INT PRIMARY KEY,
    age INT CHECK (age >= 18),
    email VARCHAR(255) UNIQUE,
    product_id INT REFERENCES products(id) ON DELETE RESTRICT IN SOMEPLACE,
    cod_iq VARCHAR(20) IQ UNIQUE(5),
    CONSTRAINT unq_name_email UNIQUE (name, email),
    CONSTRAINT fk_ord_line FOREIGN KEY (ord_id, line_id) REFERENCES ord_lines(ord_id,line_id)
);
```

Copy

##### Output Code:[¶](#id52)

##### Snowflake[¶](#id53)

```
 CREATE OR REPLACE TABLE t_constraint (
    id1 INT NOT NULL,
    id2 INT PRIMARY KEY,
    age INT
            !!!RESOLVE EWI!!! /*** SSC-EWI-0035 - CHECK STATEMENT NOT SUPPORTED ***/!!!
            CHECK (age >= 18),
    email VARCHAR(255) UNIQUE,
    product_id INT REFERENCES products (id) ON DELETE RESTRICT ,
    cod_iq VARCHAR(20)
                       !!!RESOLVE EWI!!! /*** SSC-EWI-SY0003 - UNSUPPORTED IQ UNIQUE CONSTRAINT ***/!!!
 IQ UNIQUE(5),
       CONSTRAINT unq_name_email UNIQUE (name, email),
       CONSTRAINT fk_ord_line FOREIGN KEY (ord_id, line_id) REFERENCES ord_lines (ord_id, line_id)
   )
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "sybase",  "convertedOn": "03/19/2025",  "domain": "test" }}'
;
```

Copy

### Related EWIs[¶](#id54)

[SSC-EWI-0035](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0035):
CHECK STATEMENT NOT SUPPORTED.

[SSC-EWI-SY0003](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/sybaseEWI.html#ssc-ewi-sy0003):
UNSUPPORTED IQ UNIQUE CONSTRAINT.

## DEFAULT[¶](#default)

### Description[¶](#id55)

Defines the default value of a column in a create table.

Warning

This syntax is partially supported in Snowflake.

### Grammar Syntax[¶](#id56)

```
 <default-value> ::=
   <special-value>
   | <string>
   | <global variable>
   | [ - ] <number>
   | ( <constant-expression> )
   | <built-in-function>( <constant-expression> )
   | AUTOINCREMENT
   | CURRENT DATABASE
   | CURRENT REMOTE USER
   | NULL
   | TIMESTAMP
   | LAST USER

<special-value> ::=
   CURRENT
   { DATE | TIME | TIMESTAMP | USER | PUBLISHER }
   | USER
```

Copy

### Sample Source Patterns[¶](#id57)

#### Input Code:[¶](#id58)

##### Sybase[¶](#id59)

```
 create table t_defaults
(
col1 timestamp default current utc timestamp,
col2 timestamp default current timestamp,
col3 varchar default current user,
col4 varchar default current remote user,
col5 varchar default last user,
col6 varchar default current publisher,
col7 varchar default current date,
col8 varchar default current database,
col9 varchar default current time,
col10 varchar default user,
col11 int default autoincrement,
col12 int identity,
col13 int default -10,
col14 int default 'literal',
col15 int default null
)
;
```

Copy

##### Output Code:[¶](#id60)

##### Snowflake[¶](#id61)

```
 CREATE OR REPLACE TABLE t_defaults
(
    col1 timestamp default CURRENT_TIMESTAMP,
    col2 timestamp default CURRENT_TIMESTAMP,
    col3 VARCHAR default CURRENT_USER,
    col4 VARCHAR default
                         !!!RESOLVE EWI!!! /*** SSC-EWI-SY0001 - UNSUPPORTED DEFAULT VALUE CURRENT REMOTE USER IN SNOWFLAKE ***/!!! current remote user,
    col5 VARCHAR default
                         !!!RESOLVE EWI!!! /*** SSC-EWI-SY0001 - UNSUPPORTED DEFAULT VALUE LAST USER IN SNOWFLAKE ***/!!! last user,
    col6 VARCHAR default
                         !!!RESOLVE EWI!!! /*** SSC-EWI-SY0001 - UNSUPPORTED DEFAULT VALUE CURRENT PUBLISHER IN SNOWFLAKE ***/!!! current publisher,
    col7 VARCHAR default CURRENT_DATE,
    col8 VARCHAR default CURRENT_DATABASE,
    col9 VARCHAR default CURRENT_TIME,
    col10 VARCHAR DEFAULT CURRENT_USER,
    col11 INT IDENTITY ORDER,
    col12 INT IDENTITY ORDER,
    col13 INT default -10,
    col14 INT default 'literal',
    col15 INT default null
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "sybase",  "convertedOn": "03/19/2025",  "domain": "test" }}'
;
```

Copy
