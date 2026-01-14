---
description: This document details all the similarities, differences in SQL syntax
  and how SnowConvert AI would translate those SQL syntaxes into a functional Snowflake
  SQL Syntax.
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/oracle/sql-translation-reference/README
title: SnowConvert AI - Oracle - SQL Statements | Snowflake Documentation
---

## Alter Table[¶](#alter-table)

This section shows you the translations related to ALTER TABLE.

**Note:**

Some parts in the output code are omitted for clarity reasons.

### 1. Description[¶](#description)

Use the ALTER TABLE statement to alter the definition of a nonpartitioned table, a partitioned table, a table partition, or a table subpartition. For object tables or relational tables with object columns, use ALTER TABLE to convert the table to the latest definition of its referenced type after the type has been altered ([Oracle documentation](https://docs.oracle.com/cd/E11882_01/server.112/e41084/statements_3001.htm#SQLRF01001)).

**Oracle syntax**

```
ALTER TABLE [ schema. ] table
  [ alter_table_properties
  | column_clauses
  | constraint_clauses
  | alter_table_partitioning
  | alter_external_table
  | move_table_clause
  ]
  [ enable_disable_clause
  | { ENABLE | DISABLE } { TABLE LOCK | ALL TRIGGERS }
  ] ...
  ;
```

**Note:**

To review Snowflake syntax, review the following [documentation](https://docs.snowflake.com/en/sql-reference/sql/alter-table).

#### 2. Sample Source Patterns[¶](#sample-source-patterns)

#### 2.1. Alter table with clauses[¶](#alter-table-with-clauses)

Warning

**memoptimize_read_clause** and **memoptimize_read_clause** are not applicable in Snowflake so are being removed.

##### Oracle[¶](#oracle)

```
ALTER TABLE SOMESCHEMA.SOMENAME
MEMOPTIMIZE FOR READ
MEMOPTIMIZE FOR WRITE
 ADD (SOMECOLUMN NUMBER , SOMEOTHERCOLUMN VARCHAR(23))
 (PARTITION PT NESTED TABLE COLUMN_VALUE STORE AS SNAME
 ( SUBPARTITION SPART NESTED TABLE COLUMN_VALUE STORE AS SNAME))
ENABLE TABLE LOCK;
```

##### Snowflake[¶](#snowflake)

```
ALTER TABLE SOMESCHEMA.SOMENAME
ADD (SOMECOLUMN NUMBER(38, 18), SOMEOTHERCOLUMN VARCHAR(23));
```

**Note:**

Only some **column_clauses and constraint_clauses** are applicable in Snowflake. In Oracle alter table allows modifying properties from partitions created but in Snowflake, these actions are not required

#### 2.2. Alter table with not supported cases[¶](#alter-table-with-not-supported-cases)

##### Oracle[¶](#id1)

```
ALTER TABLE SOMENAME MODIFY COLUMN SCOLUMN NOT SUBSTITUTABLE AT ALL LEVELS FORCE;

ALTER TABLE SOMENAME MODIFY(SCOLUMN VISIBLE,SCOLUMN INVISIBLE);

ALTER TABLE SOMENAME MODIFY VARRAY VARRAYITEM (
STORAGE(PCTINCREASE 10));
```

##### Snowflake[¶](#id2)

```
!!!RESOLVE EWI!!! /*** SSC-EWI-0109 - ALTER TABLE SYNTAX NOT APPLICABLE IN SNOWFLAKE ***/!!!
ALTER TABLE SOMENAME
MODIFY COLUMN SCOLUMN NOT SUBSTITUTABLE AT ALL LEVELS FORCE;

!!!RESOLVE EWI!!! /*** SSC-EWI-0109 - ALTER TABLE SYNTAX NOT APPLICABLE IN SNOWFLAKE ***/!!!

ALTER TABLE SOMENAME
MODIFY(SCOLUMN VISIBLE,SCOLUMN INVISIBLE);

!!!RESOLVE EWI!!! /*** SSC-EWI-0109 - ALTER TABLE SYNTAX NOT APPLICABLE IN SNOWFLAKE ***/!!!

ALTER TABLE SOMENAME
MODIFY VARRAY VARRAYITEM (
STORAGE(PCTINCREASE 10));
```

#### 2.3. ADD CONSTRAINT action[¶](#add-constraint-action)

The ADD CONSTRAINT action has an equivalent in Snowflake, but it only one constraint can be added per ALTER TABLE statement, so it will be commented when the statement contains two or more constraints.

Warning

**enable_disable_clause** is removed since it is not relevant in Snowflake.

##### Oracle[¶](#id3)

```
-- MULTIPLE CONSTRAINT ADDITION SCENARIO
ALTER TABLE TABLE1 ADD (
CONSTRAINT TABLE1_PK
PRIMARY KEY
(ID)
ENABLE VALIDATE,
CONSTRAINT TABLE1_FK foreign key(ID2)
references TABLE2 (ID) ON DELETE CASCADE);

-- ONLY ONE CONSTRAINT ADDITION SCENARIO
ALTER TABLE TABLE1 ADD (
CONSTRAINT TABLE1_FK foreign key(ID2)
references TABLE2 (ID) ON DELETE CASCADE);
```

##### Snowflake[¶](#id4)

```
-- MULTIPLE CONSTRAINT ADDITION SCENARIO
!!!RESOLVE EWI!!! /*** SSC-EWI-OR0067 - MULTIPLE CONSTRAINT DEFINITION IN A SINGLE STATEMENT IS NOT SUPPORTED IN SNOWFLAKE. ***/!!!
ALTER TABLE TABLE1
ADD (
CONSTRAINT TABLE1_PK
PRIMARY KEY
(ID) ,
CONSTRAINT TABLE1_FK foreign key(ID2)
references TABLE2 (ID) ON DELETE CASCADE);

-- ONLY ONE CONSTRAINT ADDITION SCENARIO
ALTER TABLE TABLE1
ADD
CONSTRAINT TABLE1_FK foreign key(ID2)
references TABLE2 (ID) ON DELETE CASCADE;
```

### Known Issues[¶](#known-issues)

1. Some properties on the tables may be adapted to or not applicable.

### Related EWIs[¶](#related-ewis)

1. [SSC-EWI-0109](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0109): Alter Table syntax is not applicable in Snowflake.
2. [SSC-EWI-OR0067](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI.html#ssc-ewi-or0067): Multiple constraint definition in a single statement is not supported in Snowflake.

## Create Database Link[¶](#create-database-link)

Warning

Currently, **_Create Database Link_** statement is not being converted but it is being parsed. Also, if your source code has`create database link` statements, these are going to be accounted for in the **_Assessment Report._**

### **Example of a Source Code**[¶](#example-of-a-source-code)

```
CREATE PUBLIC DATABASE LINK db_link_name
CONNECT TO CURRENT_USER
USING 'connect string'

CREATE DATABASE LINK db_link_name2
CONNECT TO user_name IDENTIFIED BY user_password
USING 'connect string'

CREATE PUBLIC DATABASE LINK db_link_name3
```

### Snowflake output[¶](#snowflake-output)

```
----** SSC-OOS - OUT OF SCOPE CODE UNIT. CREATE DATABASE LINK IS OUT OF TRANSLATION SCOPE. **
--CREATE PUBLIC DATABASE LINK db_link_name
--CONNECT TO CURRENT_USER
--USING 'connect string'

----** SSC-OOS - OUT OF SCOPE CODE UNIT. CREATE DATABASE LINK IS OUT OF TRANSLATION SCOPE. **
--CREATE DATABASE LINK db_link_name2
--CONNECT TO user_name IDENTIFIED BY user_password
--USING 'connect string'

----** SSC-OOS - OUT OF SCOPE CODE UNIT. CREATE DATABASE LINK IS OUT OF TRANSLATION SCOPE. **

--CREATE PUBLIC DATABASE LINK db_link_name3
```

### Database Link References[¶](#database-link-references)

If in your input code you use objects from the database link the output code will keep the name of these objects but the name of the database link that they are using will be removed.

#### Example of a Source Code[¶](#id5)

```
-- CREATE DATABASE LINK STATEMENTS
CREATE DATABASE LINK mylink1
    CONNECT TO user1 IDENTIFIED BY password1
    USING 'my_connection_string1';

CREATE DATABASE LINK mylink2
    CONNECT TO user2 IDENTIFIED BY password2
    USING 'my_connection_string2';

-- SQL statements that use the database links
SELECT * FROM products@mylink1;

INSERT INTO employees@mylink2
    (employee_id, last_name, email, hire_date, job_id)
    VALUES (999, 'Claus', 'sclaus@oracle.com', SYSDATE, 'SH_CLERK');

UPDATE jobs@mylink2 SET min_salary = 3000
    WHERE job_id = 'SH_CLERK';

DELETE FROM employees@mylink2
    WHERE employee_id = 999;

-- SQL statement where it uses an object from
-- a database link that is not created
SELECT * FROM products@mylink;
```

#### Snowflake output[¶](#id6)

```
---- CREATE DATABASE LINK STATEMENTS
----** SSC-OOS - OUT OF SCOPE CODE UNIT. CREATE DATABASE LINK IS OUT OF TRANSLATION SCOPE. **
--CREATE DATABASE LINK mylink1
--    CONNECT TO user1 IDENTIFIED BY password1
--    USING 'my_connection_string1'

----** SSC-OOS - OUT OF SCOPE CODE UNIT. CREATE DATABASE LINK IS OUT OF TRANSLATION SCOPE. **

--CREATE DATABASE LINK mylink2
--    CONNECT TO user2 IDENTIFIED BY password2
--    USING 'my_connection_string2'

-- SQL statements that use the database links
SELECT * FROM
    !!!RESOLVE EWI!!! /*** SSC-EWI-OR0123 - DBLINK CONNECTIONS NOT SUPPORTED [ DBLINK : mylink1 | USER: user1/password1 | CONNECTION: 'my_connection_string1' ] ***/!!!
    products;

INSERT INTO
!!!RESOLVE EWI!!! /*** SSC-EWI-OR0123 - DBLINK CONNECTIONS NOT SUPPORTED [ DBLINK : mylink2 | USER: user2/password2 | CONNECTION: 'my_connection_string2' ] ***/!!!
employees
    (employee_id, last_name, email, hire_date, job_id)
    VALUES (999, 'Claus', 'sclaus@oracle.com', CURRENT_TIMESTAMP(), 'SH_CLERK');

UPDATE
!!!RESOLVE EWI!!! /*** SSC-EWI-OR0123 - DBLINK CONNECTIONS NOT SUPPORTED [ DBLINK : mylink2 | USER: user2/password2 | CONNECTION: 'my_connection_string2' ] ***/!!!
jobs
    SET min_salary = 3000
    WHERE job_id = 'SH_CLERK';

DELETE FROM
    !!!RESOLVE EWI!!! /*** SSC-EWI-OR0123 - DBLINK CONNECTIONS NOT SUPPORTED [ DBLINK : mylink2 | USER: user2/password2 | CONNECTION: 'my_connection_string2' ] ***/!!!
    employees
    WHERE employee_id = 999;

-- SQL statement where it uses an object from
-- a database link that is not created
--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "mylink" **
SELECT * FROM
    !!!RESOLVE EWI!!! /*** SSC-EWI-OR0123 - DBLINK CONNECTIONS NOT SUPPORTED [ DBLINK : mylink | USER: / | CONNECTION:  ] ***/!!!
    products;
```

### Related EWIs[¶](#id7)

1. [SSC-EWI-OR0123](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI.html#ssc-ewi-or0123): Db Link connections not supported.
2. [SSC-FDM-0007](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0007): Element with missing dependencies.

## Drop Table[¶](#drop-table)

**Note:**

Some parts in the output code are omitted for clarity reasons.

### Description[¶](#id8)

A Drop Table statement is used to remove a table. This statement varies a little between [Oracle](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/DROP-TABLE.html#GUID-39D89EDC-155D-4A24-837E-D45DDA757B45) and [Snowflake](https://docs.snowflake.com/en/sql-reference/sql/drop-table.html). Please double-check each documentation for more information regarding the differences.

In Oracle, the Drop Table syntax is:

```
DROP TABLE <table_name> [ CASCADE CONSTRAINTS ] [ PURGE ]
```

In Snowflake, the Drop table syntax is:

```
DROP TABLE [ IF EXISTS ] <table_name> [ CASCADE | RESTRICT ]
```

The main difference is that Snowflake does not have an equal for the PURGE clause, as the table will not be permanently removed from the system. Though, the CASCADE CONSTRAINTS and the CASCADE clauses _are_ the same. Both drop the table, even if foreign keys exist that reference this table.

#### Examples[¶](#examples)

Now, let’s see some code examples, and what it would look like after it has been transformed. Each example uses a different variation of the Drop Table statement.

##### Example 1:[¶](#example-1)

This example uses the **Drop Table** statement as simple as possible.

**Input Code:**

```
DROP TABLE TEST_TABLE1;
```

**Transformed Code:**

```
DROP TABLE TEST_TABLE1;
```

##### Example 2:[¶](#example-2)

This example uses the **Drop Table** statement with the PURGE clause. Remember there is no equivalent in Snowflake for the PURGE clause inside a Drop Table statement.

**Input Code:**

```
DROP TABLE TEST_TABLE1 PURGE;
```

**Transformed Code:**

```
DROP TABLE TEST_TABLE1;
```

##### Example 3:[¶](#example-3)

This example uses the **Drop Table** statement with the CASCADE CONSTRAINTS clause.

**Input Code:**

```
DROP TABLE TEST_TABLE1 CASCADE CONSTRAINTS;
```

**Transformed Code:**

```
DROP TABLE TEST_TABLE1 CASCADE;
```

In the transformed code, the CONSTRAINTS word is removed from the CASCADE CONSTRAINTS clause.

##### Example 4:[¶](#example-4)

This example uses the **Drop Table** statement with the CASCADE CONSTRAINTS and the PURGE clauses.

**Input Code:**

```
DROP TABLE TEST_TABLE1 CASCADE CONSTRAINTS PURGE;
```

**Transformed Code:**

```
DROP TABLE TEST_TABLE1 CASCADE;
```

As seen, the code changes. In the new Snowflake code, the PURGE clause is removed and the CONSTRAINTS word is also removed from the CASCADE clause.

#### Functional Equivalence[¶](#functional-equivalence)

Run the following code to check for functional equivalence, bear in mind the only part that is not equivalent is the PURGE clause, which in Oracle removes completely the table from the system and there is no equal for Snowflake. In both cases, the table is dropped even if it’s referenced in another table.

**Oracle:**

```
CREATE TABLE TEST_TABLE2 (
    col2 INTEGER,
    CONSTRAINT constraint_name PRIMARY KEY (col2)
);

CREATE TABLE OTHER_TABLE (
    other_col INTEGER REFERENCES TEST_TABLE2 (col2)
);

DROP TABLE TEST_TABLE2 CASCADE CONSTRAINTS PURGE;
```

**Snowflake:**

```
CREATE OR REPLACE TABLE TEST_TABLE2 (
       col2 INTEGER,
       CONSTRAINT constraint_name PRIMARY KEY (col2)
   )
   COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
   ;

   CREATE OR REPLACE TABLE OTHER_TABLE (
          other_col INTEGER REFERENCES TEST_TABLE2 (col2)
      )
   COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
   ;

   DROP TABLE TEST_TABLE2 CASCADE;
```

### Related EWIs[¶](#id9)

No related EWIs.

## Create Index[¶](#create-index)

Warning

Currently, **_Create Index_** statement is not being converted but it is being parsed. Also, if your source code has create `index` statements, these are going to be accounted for in the **_Assessment Report._**

### Example of a _create index_ parsed code:[¶](#example-of-a-create-index-parsed-code)

```
CREATE UNIQUE INDEX COL1_INDEX ILM (ADD POLICY OPTIMIZE AFTER 10 DAYS OF NO ACCESS) ON CLUSTER CLUSTER1
ONLINE USABLE DEFERRED INVALIDATION;

CREATE BITMAP INDEX COL1_INDEX ILM (ADD POLICY OPTIMIZE ( ON FUNC1 )) ON TABLE1 AS TAB1 (COL1 ASC) GLOBAL PARTITION BY RANGE (COL1, COL2) ( PARTITION VALUES LESS THAN (MAXVALUE) ) UNUSABLE IMMEDIATE INVALIDATION;

CREATE MULTIVALUE INDEX COL1_INDEX ILM (ADD POLICY SEGMENT TIER TO LOW_COST_TBS) ON TABLE1( TAB1 COL1 DESC, TAB1 COL2 ASC) FROM TABLE1 AS TAB1 WHERE COL1 > 0 LOCAL STORE IN (STORAGE1)
VISIBLE USABLE DEFERRED INVALIDATION;

CREATE INDEX COL1_INDEX ILM (DELETE POLICY POLICY1) ON CLUSTER CLUSTER1
PCTFREE 10
LOGGING
ONLINE
TABLESPACE DEFAULT
NOCOMPRESS
SORT
REVERSE
VISIBLE
INDEXING PARTIAL
NOPARALLEL;

CREATE INDEX COL1_INDEX ILM (DELETE_ALL) ON TABLE1 AS TAB1 (COL1 ASC) LOCAL (
PARTITION PARTITION1 TABLESPACE TABLESPACE1 NOCOMPRESS USABLE) DEFERRED INVALIDATION;

CREATE INDEX COL1_INDEX ON TABLE1 (COL1 ASC) GLOBAL
PARTITION BY HASH (COL1, COL2) (PARTITION PARTITION1 LOB(LOB1) STORE AS BASICFILE LOB_NAME (TABLESPACE TABLESPACE1)) USABLE IMMEDIATE INVALIDATION;

CREATE INDEX COL1_INDEX ON TABLE1 (COL1 DESC, COL2 ASC) INDEXTYPE IS INDEXTYPE1 LOCAL ( PARTITION PARTITION1 PARAMETERS('PARAMS')) NOPARALLEL PARAMETERS('PARAMS') USABLE DEFERRED INVALIDATION;

CREATE INDEX COL1_INDEX ON TABLE1 (COL1 ASC) INDEXTYPE IS XDB.XMLINDEX LOCAL ( PARTITION PARTITION1) PARALLEL 6 UNUSABLE IMMEDIATE INVALIDATION;
```

**Note:**

Due to architectural reasons, Snowflake does not support indexes so, SnowConvert AI will remove all the code related to the creation of indexes. Snowflake automatically creates micro-partitions for every table that help speed up the performance of DML operations, the user does not have to worry about creating or managing these micro-partitions.

Usually, this is enough to have an exceptionally good query performance. However, there are ways to improve it by creating data clustering keys. [Snowflake’s official page](https://docs.snowflake.com/en/user-guide/tables-clustering-micropartitions.html) provides more information about micro-partitions and data clustering.

## Create Sequence[¶](#create-sequence)

Let’s first see a code example, and what it would look like after it has been transformed.

### Oracle:[¶](#id10)

```
CREATE SEQUENCE SequenceSample
START WITH 1000
INCREMENT BY 1
NOCACHE
NOCYCLE;
```

### Snowflake:[¶](#id11)

```
CREATE OR REPLACE SEQUENCE SequenceSample
START WITH 1000
INCREMENT BY 1
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}';
```

The first change that it is done is to apply the schema or datawarehouse to the name of the sequence. The second transformation consists in removing some elements and add then as comments, since oracle has some elements in the create sequence that are not supported in snowflake.

In Oracle, after the name of the Sequence, the elements that are NOT commented are the following

- START WITH 1000
- INCREMENT BY 1

If the element is not one of those, it will be commented and added as a warning just before the create sequence, like in the example.

The following elements are the ones that are removed

- MAXVALUE
- NOMAXVALUE
- MINVALUE
- NOMINVALUE
- CYCLE
- NOCYCLE
- CACHE
- NOCACHE
- ORDER
- NOORDER
- KEEP
- NOKEEP
- SESSION
- GLOBAL
- SCALE
- EXTEND
- SCALE
- NOEXTEND
- NOSCALE
- SHARD
- EXTEND
- SHARD
- NOEXTEND
- NOSHARD

### SEQUENCE EXPRESSIONS[¶](#sequence-expressions)

- NEXTVAL: Snowflake grammar is the same as the Oracle one.
- CURRVAL: Snowflake does not has an equivalent so it is transformed to a stub function. Check this [link](https://docs.snowflake.com/en/user-guide/querying-sequences.html#currval-not-supported) to understand Snowflake’s approach.

#### Oracle:[¶](#id12)

```
select seq1.nextval from dual;
select seq1.currval from dual;
```

#### Snowflake:[¶](#id13)

```
select seq1.nextval from dual;

select
!!!RESOLVE EWI!!! /*** SSC-EWI-OR0069 - THE SEQUENCE CURRVAL PROPERTY IS NOT SUPPORTED IN SNOWFLAKE. ***/!!! seq1.currval from dual;
```

### Sequence START WITH[¶](#sequence-start-with)

`START WITH` statement value may exceed the maximum value allowed by Snowflake. What Snowflake said about the start value is: _Specifies the first value returned by the sequence. Supported values are any value that can be represented by a 64-bit two’s compliment integer (from `-2^63` to `2^63-1`)_. So according to the previously mentioned, the max value allowed is **9223372036854775807** for positive numbers and **9223372036854775808** for negative numbers.

#### Example Code[¶](#example-code)

##### Oracle:[¶](#id14)

```
CREATE SEQUENCE SEQUENCE1
START WITH 9223372036854775808;

CREATE SEQUENCE SEQUENCE2
START WITH -9223372036854775809;
```

##### Snowflake:[¶](#id15)

```
CREATE OR REPLACE SEQUENCE SEQUENCE1
!!!RESOLVE EWI!!! /*** SSC-EWI-OR0068 - SEQUENCE START VALUE EXCEEDS THE MAX VALUE ALLOWED BY SNOWFLAKE. ***/!!!
START WITH 9223372036854775808
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}';

CREATE OR REPLACE SEQUENCE SEQUENCE2
!!!RESOLVE EWI!!! /*** SSC-EWI-OR0068 - SEQUENCE START VALUE EXCEEDS THE MAX VALUE ALLOWED BY SNOWFLAKE. ***/!!!
START WITH -9223372036854775809
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}';
```

### Related EWIs[¶](#id16)

1. [SSC-EWI-OR0069](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI.html#ssc-ewi-or0069): The sequence CURRVAL property is not supported in Snowflake.
2. [SSC-EWI-OR0068](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI.html#ssc-ewi-or0068): The sequence start value exceeds the max value allowed by Snowflake.

## Alter Session[¶](#alter-session)

### Alter session[¶](#id17)

Alter session has an equivalent in Snowflake and some the variables are mapped to Snowflake variables. If a permutation of Alter Session is not supported the node will be commented and a warning will be added.

#### Oracle:[¶](#id18)

```
alter session set nls_date_format = 'DD-MM-YYYY';
```

#### Snowflake:[¶](#id19)

```
ALTER SESSION SET DATE_INPUT_FORMAT = 'DD-MM-YYYY' DATE_OUTPUT_FORMAT = 'DD-MM-YYYY';
```

### Session Parameters Reference[¶](#session-parameters-reference)

**Note:**

The session parameters that doesn’t appear in the table are not currently being transformed.

<!-- prettier-ignore -->
|Session Parameter|Snowflake transformation|
|---|---|
|NLS_DATE_FORMAT|DATE_INPUT_FORMAT and DATE_OUTPUT_FORMAT|
|NLS_NUMERIC_CHARACTERS|NOT SUPPORTED|

### Known Issues[¶](#id20)

No issues were found.

### Related EWIs[¶](#id21)

No related EWIs.

## Create Synonym[¶](#create-synonym)

**Note:**

Some parts in the output code are omitted for clarity reasons.

### Create Synonym[¶](#id22)

Synonyms are not supported in Snowflake. The references to the Synonyms will be changed for the original Object.

#### Oracle:[¶](#id23)

```
CREATE OR REPLACE SYNONYM B.TABLITA_SYNONYM FOR TABLITA;
```

#### Snowflake:[¶](#id24)

```
----** SSC-FDM-OR0005 - SYNONYMS NOT SUPPORTED IN SNOWFLAKE BUT REFERENCES TO THIS SYNONYM WERE CHANGED BY THE ORIGINAL OBJECT NAME. **
--CREATE OR REPLACE SYNONYM B.TABLITA_SYNONYM FOR TABLITA
                                                       ;
```

#### **Example 1**: Synonym that refers to a table.[¶](#example-1-synonym-that-refers-to-a-table)

Oracle source code:

```
CREATE TABLE TABLITA
(
    COLUMN1 NUMBER
);

CREATE OR REPLACE SYNONYM B.TABLITA_SYNONYM FOR TABLITA;

SELECT * FROM B.TABLITA_SYNONYM WHERE B.TABLITA_SYNONYM.COLUMN1 = 20;
```

Snowflake migrated code: you’ll notice that the `SELECT` originally refers to a synonym, but now it refers to the table that points the synonym.

```
CREATE OR REPLACE TABLE TABLITA
    (
        COLUMN1 NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/
    )
    COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
    ;

--    --** SSC-FDM-OR0005 - SYNONYMS NOT SUPPORTED IN SNOWFLAKE BUT REFERENCES TO THIS SYNONYM WERE CHANGED BY THE ORIGINAL OBJECT NAME. **

--    CREATE OR REPLACE SYNONYM B.TABLITA_SYNONYM FOR TABLITA
                                                           ;

SELECT * FROM
    TABLITA
    WHERE
    TABLITA.COLUMN1 = 20;
```

#### **Example 2**: Synonym that refers to another synonym.[¶](#example-2-synonym-that-refers-to-another-synonym)

Oracle source code:

```
CREATE TABLE TABLITA
(
    COLUMN1 NUMBER
);

CREATE OR REPLACE SYNONYM B.TABLITA_SYNONYM FOR TABLITA;
CREATE OR REPLACE SYNONYM C.TABLITA_SYNONYM2 FOR B.TABLITA_SYNONYM;

SELECT * FROM C.TABLITA_SYNONYM2 WHERE C.TABLITA_SYNONYM2.COLUMN1 = 20;

UPDATE C.TABLITA_SYNONYM2 SET COLUMN1 = 10;

INSERT INTO C.TABLITA_SYNONYM2 VALUES (1);
```

Snowflake migrated code: you’ll notice that originally the `SELECT` , `UPDATE`, `INSERT` refers to a synonym, and now it refers to the atomic object, which is a table.

```
CREATE OR REPLACE TABLE TABLITA
    (
        COLUMN1 NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/
    )
    COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
    ;

--    --** SSC-FDM-OR0005 - SYNONYMS NOT SUPPORTED IN SNOWFLAKE BUT REFERENCES TO THIS SYNONYM WERE CHANGED BY THE ORIGINAL OBJECT NAME. **

--    CREATE OR REPLACE SYNONYM B.TABLITA_SYNONYM FOR TABLITA
                                                           ;

--    --** SSC-FDM-OR0005 - SYNONYMS NOT SUPPORTED IN SNOWFLAKE BUT REFERENCES TO THIS SYNONYM WERE CHANGED BY THE ORIGINAL OBJECT NAME. **
--CREATE OR REPLACE SYNONYM C.TABLITA_SYNONYM2 FOR B.TABLITA_SYNONYM
                                                                  ;

SELECT * FROM
    TABLITA
    WHERE
    TABLITA.COLUMN1 = 20;

    UPDATE TABLITA
    SET COLUMN1 = 10;

    INSERT INTO TABLITA
    VALUES (1);
```

#### **Example 3**: Synonym that refers to a view[¶](#example-3-synonym-that-refers-to-a-view)

Oracle Source Code

```
CREATE OR REPLACE SYNONYM B.TABLITA_SYNONYM FOR TABLITA;

CREATE OR REPLACE SYNONYM C.TABLITA_SYNONYM2 FOR B.TABLITA_SYNONYM;

CREATE VIEW VIEW_ORGINAL AS SELECT * FROM C.TABLITA_SYNONYM2;

CREATE OR REPLACE SYNONYM VIEW_SYNONYM FOR VIEW_ORGINAL;

SELECT * FROM VIEW_SYNONYM;
```

Snowflake migrated code: you’ll notice that the `SELECT` originally refers to a synonym, and now it refers to the atomic objects, which is a view.

```
----** SSC-FDM-OR0005 - SYNONYMS NOT SUPPORTED IN SNOWFLAKE BUT REFERENCES TO THIS SYNONYM WERE CHANGED BY THE ORIGINAL OBJECT NAME. **
--CREATE OR REPLACE SYNONYM B.TABLITA_SYNONYM FOR TABLITA
                                                       ;

----** SSC-FDM-OR0005 - SYNONYMS NOT SUPPORTED IN SNOWFLAKE BUT REFERENCES TO THIS SYNONYM WERE CHANGED BY THE ORIGINAL OBJECT NAME. **
--CREATE OR REPLACE SYNONYM C.TABLITA_SYNONYM2 FOR B.TABLITA_SYNONYM
                                                                  ;

CREATE OR REPLACE VIEW VIEW_ORGINAL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
AS
--** SSC-FDM-0001 - VIEWS SELECTING ALL COLUMNS FROM A SINGLE TABLE ARE NOT REQUIRED IN SNOWFLAKE AND MAY IMPACT PERFORMANCE. **
SELECT * FROM
TABLITA;

----** SSC-FDM-OR0005 - SYNONYMS NOT SUPPORTED IN SNOWFLAKE BUT REFERENCES TO THIS SYNONYM WERE CHANGED BY THE ORIGINAL OBJECT NAME. **

--CREATE OR REPLACE SYNONYM VIEW_SYNONYM FOR VIEW_ORGINAL
                                                       ;

SELECT * FROM
VIEW_ORGINAL;
```

### Related EWIs[¶](#id25)

1. [SSC-FDM-0001](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0001): Views selecting all columns from a single table are not required in Snowflake.
2. [SSC-FDM-0006](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0006): Number type column may not behave similarly in Snowflake.
3. [SSC-FDM-OR0005](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM.html#ssc-fdm-or0005): Synonyms are not supported in Snowflake but references to this synonym were changed by the original object name.
