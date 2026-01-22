---
description:
  Creates a new table in the current database. You define a list of columns, which each hold data of
  a distinct type. The owner of the table is the issuer of the CREATE TABLE command.
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/sybase/sybase-create-table
title: SnowConvert AI - Sybase IQ - CREATE TABLE | Snowflake Documentation
---

## Description

Creates a new table in the current database. You define a list of columns, which each hold data of a
distinct type. The owner of the table is the issuer of the CREATE TABLE command.

For more information, please refer to
[`CREATE TABLE`](https://help.sap.com/docs/SAP_IQ/a898e08b84f21015969fa437e89860c8/a619764084f21015b8039a8346dc622c.html)
documentation.

## Grammar Syntax

```sql
 CREATE [ { GLOBAL | LOCAL } TEMPORARY ] TABLE
   [ IF NOT EXISTS ] [ `<owner>`. ]<table-name>
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
   | `<string>`
   | <global variable>
   | [ - ] `<number>`
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
   IQ UNIQUE ( `<integer>` )
   | { [ CONSTRAINT <constraint-name> ]
     { UNIQUE
        | PRIMARY KEY
        | REFERENCES <table-name> [ ( <column-name> ) ] [ ON { UPDATE | DELETE } RESTRICT ] }
      [ IN <dbspace-name> ]
      | CHECK ( `<condition>` )
   }

<table-constraint> ::=
    [ CONSTRAINT <constraint-name> ]
   {  { UNIQUE | PRIMARY KEY } ( <column-name> [ , … ] )
     [ IN <dbspace-name> ]
     | <foreign-key-constraint>
     | CHECK ( `<condition>` )
   }

<foreign-key-constraint> ::=
   FOREIGN KEY [ <role-name> ] [ ( <column-name> [ , <column-name> ] … ) ]
   …REFERENCES <table-name> [ ( <column-name> [ , <column-name> ] … ) ]
   …[ `<actions>` ] [ IN <dbspace-name> ]

`<actions>` ::=
   [ ON { UPDATE | DELETE } RESTRICT ]

<location-string> ::=
   { <remote-server-name>. [ <db-name> ].[ `<owner>` ].<object-name>
      | <remote-server-name>; [ <db-name> ]; [ `<owner>` ];<object-name> }

<range-partitioning-scheme> ::=
   RANGE ( <partition-key> ) ( <range-partition-decl> [,<range-partition-decl> … ] )

<partition-key> ::= <column-name>

<range-partition-declaration> ::=
    <range-partition-name> VALUES <= ( {`<constant>` |  MAX } ) [ IN <dbspace-name> ]

<hash-partitioning-scheme> ::=
   HASH ( <partition-key> [ , <partition-key>, … ] )

<composite-partitioning-scheme> ::=
   <hash-partitioning-scheme> SUBPARTITION BY <range-partitioning-scheme>
```

## TEMPORARY TABLES

### Description 2

In Sybase IQ `GLOBAL | LOCAL TEMPORARY` is used to create temporary tables that exist only for the
session. These tables are session-specific and automatically deleted when the session ends. They
help store intermediate results or work data without affecting the permanent database schema. It
also can be created only by adding an `#` at the beginning of the name.

Warning

This syntax is partially supported in Snowflake.

### Grammar Syntax 2

```sql
 CREATE [ { GLOBAL | LOCAL } TEMPORARY ] TABLE
```

### Sample Source Patterns

#### Input Code

##### Sybase

```sql
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

##### Output Code

##### Sybase 2

```sql
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

### Related EWIs

[SSC-FDM-0009](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0009):
GLOBAL TEMPORARY TABLE functionality not supported.

## IF NOT EXISTS

### Description 3

> Ensures the table is created only if it does not already exist, preventing duplication and errors
> in your SQL script.
> ([Sybase SQL Language Reference](https://help.sap.com/docs/SAP_IQ/a898e08b84f21015969fa437e89860c8/a619764084f21015b8039a8346dc622c.html)).

SuccessPlaceholder

This syntax is fully supported in Snowflake.

### Grammar Syntax 3

```sql
 IF NOT EXISTS
```

### Sample Source Patterns 2

#### Input Code: 2

##### Sybase 3

```sql
 CREATE TABLE IF NOT EXISTS table1 (
    col1 INTEGER
);
```

##### Output Code: 2

##### Snowflake

```sql
 CREATE TABLE IF NOT EXISTS table1 (
    col1 INTEGER
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "sybase",  "convertedOn": "03/19/2024" }}';
```

## (ENABLE | DISABLE) RLV STORE

### Description 4

> Controls Row-Level Versioning Store functionality.
> ([Sybase SQL Language Reference](https://help.sap.com/docs/SAP_IQ/a898e08b84f21015969fa437e89860c8/a619764084f21015b8039a8346dc622c.html)).

#### Note

This syntax is not needed in Snowflake.

### Grammar Syntax 4

```sql
 { ENABLE | DISABLE } RLV STORE
```

### Sample Source Patterns 3

#### Input Code: 3

##### Sybase 4

```sql
 CREATE TABLE rlv_table
(id INT)
ENABLE RLV STORE;
```

##### Output Code: 3

##### Snowflake 2

```sql
 CREATE OR REPLACE TABLE rlv_table
(
id INT
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "sybase",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
;
```

## IN DBSPACE

### Description 5

> Specifies the DB space for data storage.
> ([Sybase SQL Language Reference](https://help.sap.com/docs/SAP_IQ/a898e08b84f21015969fa437e89860c8/a619764084f21015b8039a8346dc622c.html)).

#### Note 2

This syntax is not needed in Snowflake. Snowflake automatically handles storage.

### Grammar Syntax 5

```sql
 IN <dbspace-name>
```

### Sample Source Patterns 4

#### Input Code: 4

##### Sybase 5

```sql
 CREATE TABLE dbspace_table (
    id INT PRIMARY KEY
)
IN my_dbspace;
```

##### Output Code: 4

##### Snowflake 3

```sql
 CREATE OR REPLACE TABLE dbspace_table (
    id INT PRIMARY KEY
);
```

## ON COMMIT

### Description 6

> Specifies the behaviour of the temporary table when a commit is done.
> ([Sybase SQL Language Reference](https://help.sap.com/docs/SAP_IQ/a898e08b84f21015969fa437e89860c8/a619764084f21015b8039a8346dc622c.html))

Warning

This syntax is partially supported.

### Grammar Syntax 6

```sql
 [ ON COMMIT { DELETE | PRESERVE } ROWS ]
```

### Sample Source Patterns 5

#### Input Code: 5

##### Sybase 6

```sql
 CREATE LOCAL TEMPORARY TABLE temp_employees (
    DATA VARCHAR(255)
) ON COMMIT DELETE ROWS;

CREATE LOCAL TEMPORARY TABLE temp_projects (
    DATA VARCHAR(255)
) ON COMMIT PRESERVE ROWS;
```

##### Output Code: 5

##### Snowflake 4

```sql
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

### Related EWIs 2

[SSC-FDM-0008](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0008):
On Commit not supported.

## AT LOCATION

### Description 7

> Creates a remote table (proxy).
> ([Sybase SQL Language Reference](https://help.sap.com/docs/SAP_IQ/a898e08b84f21015969fa437e89860c8/a619764084f21015b8039a8346dc622c.html))

Danger

This syntax is not supported in Snowflake.

### Grammar Syntax 7

```sql
 AT <location-string>
```

### Sample Source Patterns 6

#### Input Code: 6

##### Sybase 7

```sql
 CREATE TABLE t1
(
    DATA VARCHAR(10)
)
AT 'SERVER_A.db1.joe.t1';
```

##### Output Code: 6

##### Snowflake 5

```sql
 CREATE OR REPLACE TABLE t1
(
    DATA VARCHAR(10)
)
    !!!RESOLVE EWI!!! /*** SSC-EWI-SY0002 - UNSUPPORTED REMOTE TABLE SYNTAX ***/!!!
AT 'SERVER_A.db1.joe.t1'
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "sybase",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
;
```

### Related EWIs 3

[SSC-EWI-SY0002](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/sybaseEWI#ssc-ewi-sy0002):
UNSUPPORTED REMOTE TABLE SYNTAX.

## PARTITION BY

### Description 8

> All rows of a table partition are physically colocated.
> ([Sybase SQL Language Reference](https://help.sap.com/docs/SAP_IQ/a898e08b84f21015969fa437e89860c8/a619764084f21015b8039a8346dc622c.html))

#### Note 3

This syntax is not needed in Snowflake.

### Grammar Syntax 8

```sql
 PARTITION BY
     <range-partitioning-scheme>
     | <hash-partitioning-scheme>
     | <composite-partitioning-scheme>

<range-partitioning-scheme> ::=
   RANGE ( <partition-key> ) ( <range-partition-decl> [,<range-partition-decl> … ] )

<partition-key> ::= <column-name>

<range-partition-declaration> ::=
    <range-partition-name> VALUES <= ( {`<constant>` |  MAX } ) [ IN <dbspace-name> ]

<hash-partitioning-scheme> ::=
   HASH ( <partition-key> [ , <partition-key>, … ] )

<composite-partitioning-scheme> ::=
   <hash-partitioning-scheme> SUBPARTITION BY <range-partitioning-scheme>
```

### Sample Source Patterns 7

#### Input Code: 7

##### Sybase 8

```sql
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

##### Output Code: 7

##### Snowflake 6

```sql
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

## CONSTRAINTS

### Description 9

> This ensures the accuracy and reliability of the data in the table. If there is any violation
> between the constraint and the data action, the action is aborted.
> ([Sybase SQL Language Reference](https://help.sap.com/docs/SAP_IQ/a898e08b84f21015969fa437e89860c8/a619764084f21015b8039a8346dc622c.html))

Warning

This syntax is partially supported.

### Grammar Syntax 9

```sql
 <table-constraint> ::=
    [ CONSTRAINT <constraint-name> ]
   {  { UNIQUE | PRIMARY KEY } ( <column-name> [ , … ] )
     [ IN <dbspace-name> ]
     | <foreign-key-constraint>
     | CHECK ( `<condition>` )
   }

<foreign-key-constraint> ::=
   FOREIGN KEY [ <role-name> ] [ ( <column-name> [ , <column-name> ] … ) ]
   …REFERENCES <table-name> [ ( <column-name> [ , <column-name> ] … ) ]
   …[ `<actions>` ] [ IN <dbspace-name> ]

`<actions>` ::=
   [ ON { UPDATE | DELETE } RESTRICT ]
```

### Sample Source Patterns 8

#### Input Code: 8

##### Sybase 9

```sql
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

##### Output Code: 8

##### Snowflake 7

```sql
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

### Related EWIs 4

[SSC-EWI-0035](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0035):
CHECK STATEMENT NOT SUPPORTED.

[SSC-EWI-SY0003](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/sybaseEWI#ssc-ewi-sy0003):
UNSUPPORTED IQ UNIQUE CONSTRAINT.

## DEFAULT

### Description 10

Defines the default value of a column in a create table.

Warning

This syntax is partially supported in Snowflake.

### Grammar Syntax 10

```sql
 <default-value> ::=
   <special-value>
   | `<string>`
   | <global variable>
   | [ - ] `<number>`
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

### Sample Source Patterns 9

#### Input Code: 9

##### Sybase 10

```sql
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

##### Output Code: 9

##### Snowflake 8

```sql
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
