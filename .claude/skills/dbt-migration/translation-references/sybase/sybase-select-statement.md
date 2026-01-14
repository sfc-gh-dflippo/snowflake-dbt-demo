---
description: Retrieves information from the database. (Sybase SQL Language Reference)
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/sybase/sybase-select-statement
title: SnowConvert AI - Sybase IQ - SELECT | Snowflake Documentation
---

## Description[¶](#description)

> Retrieves information from the database.
> ([Sybase SQL Language Reference](https://help.sap.com/docs/SAP_IQ/a899599784f21015a466ed42e24d07f9/a624e72e84f210159276a39335acd358.html?version=16.0.11&locale=en-US))

Warning

This syntax is partially supported in Snowflake.

## Grammar Syntax[¶](#grammar-syntax)

```
 SELECT
[ ALL | DISTINCT ]
[ row-limitation-option1 ]
   	select-list
   … 	[ INTO { host-variable-list | variable-list | table-name } ]
   … 	[ INTO LOCAL TEMPORARY TABLE { table-name } ]
   … 	[ FROM table-list ]
   … 	[ WHERE search-condition ]
   … 	[ GROUP BY [ expression [, ...]
         | ROLLUP ( expression [, ...] )
         | CUBE ( expression [, ...] ) ] ]
   … 	[ HAVING search-condition ]
   … 	[ ORDER BY { expression | integer } [ ASC | DESC ] [, ...] ]
   | 	[ FOR JSON json-mode ]
   … [ row-limitation-option ]

select-list:
   { column-name
   | expression [ [ AS ] alias-name ]
   | *
   }

row-limitation-option1:
   FIRST
   | TOP {ALL | limit-expression} [START AT startat-expression ]

limit-expression:
    simple-expression

startat-expression:
    simple-expression

row-limitation-option2:
   LIMIT { [ offset-expression, ] limit-expression
   | limit-expression OFFSET offset-expression }

offset-expression:
   simple-expression

simple-expression:
   integer
   | variable
   | ( simple-expression )
   | ( simple-expression { + | - | * } simple-expression )


..FROM <table-expression> [,...]

<table-expression> ::=
   <table-name>
   | <view-name>
   | <procedure-name>
   | <common-table-expression>
   | ( <subquery> ) [ [ AS ] <derived-table-name> ( <column_name, ...>) ] ]
   | <derived-table>
   | <join-expression>
   | ( <table-expression> , ... )
   | <openstring-expression>
   | <apply-expression>
   | <contains-expression>
   | <dml-derived-table>

<table-name> ::=
   [ <userid>.] <table-name> ]
   [ [ AS ] <correlation-name> ]
   [ FORCE INDEX ( <index-name> ) ]

<view-name> ::=
   [ <userid>.]<view-name> [ [ AS ] <correlation-name> ]

<procedure-name> ::=
   [  <owner>, ] <procedure-name> ([ <parameter>, ...])
   [  WITH(<column-name datatype>, )]
   [ [ AS ] <correlation-name> ]

<parameter> ::=
   <scalar-expression> | <table-parameter>

<table-parameter> ::=
   TABLE (<select-statement)> [ OVER ( <table-parameter-over> )]

<table-parameter-over> ::=
   [ PARTITION BY {ANY
   | NONE|< table-expression> } ]
   [ ORDER BY { <expression> | <integer> }
   [ ASC | DESC ] [, ...] ]

<derived-table> ::=
   ( <select-statement> )
   	[ AS ] <correlation-name> [ ( <column-name>, ... ) ]

<join-expression> ::=
   <table-expression> <join-operator> <table-expression>
   	[ ON <join-condition> ]

<join-operator> ::=
   [ KEY | NATURAL ] [ <join-type> ] JOIN | CROSS JOIN

<join-type> ::=
   INNER
     | LEFT [ OUTER ]
     | RIGHT [ OUTER ]
     | FULL [ OUTER ]

<openstring-expression> ::=
   OPENSTRING ( { FILE | VALUE } <string-expression> )
     WITH ( <rowset-schema> )
   	[ OPTION ( <scan-option> ...  ) ]
   	[ AS ] <correlation-name>

<apply-expression> ::=
   <table-expression> { CROSS | OUTER } APPLY <table-expression>

<contains-expression> ::=
   { <table-name>  | <view-name> } CONTAINS
   ( <column-name> [,...], <contains-query> )
   [ [ AS ] <score-correlation-name> ]

<rowset-schema> ::=
   <column-schema-list>
	   | TABLE [<owner>.]<table-name> [ ( <column-list> ) ]

<column-schema-list> ::=
   { <column-name user-or-base-type> |  filler( ) } [ , ... ]

<column-list> ::=
   { <column-name> | filler( ) } [ , ... ]

<scan-option> ::=
   BYTE ORDER MARK { ON | OFF }
   | COMMENTS INTRODUCED BY <comment-prefix>
   | DELIMITED BY <string>
   | ENCODING <encoding>
   | ESCAPE CHARACTER <character>
   | ESCAPES { ON | OFF }
   | FORMAT { TEXT  | BCP  }
   | HEXADECIMAL { ON | OFF }
   | QUOTE <string>
   | QUOTES { ON | OFF }
   | ROW DELIMITED BY string
   | SKIP <integer>
   | STRIP { ON | OFF | LTRIM | RTRIM | BOTH }

<contains-query> ::= <string>

<dml-derived-table> ::=
   ( <dml-statement>  ) REFERENCING ( [ <table-version-names>  | NONE ] )

<dml-statement> ::=
   <insert-statement>
   <update-statement>
   <delete-statement>

<table-version-names> ::=
   OLD [ AS ] <correlation-name> [ FINAL [ AS ] <correlation-name> ]
     | FINAL [ AS ] <correlation-name>
```

## Sample Source Patterns[¶](#sample-source-patterns)

### Row Limitation[¶](#row-limitation)

Sybase allow row limitation in a query by using TOP clause with an optional START AT that Snowflake
not supports but can transformed as down below to achieve the same functionality.

#### Input Code:[¶](#input-code)

##### Sybase[¶](#sybase)

```
 SELECT
TOP 10 START AT 2
COL1
FROM TABLE1;

SELECT
FIRST
COL1
FROM TABLE1;

SELECT
COL1
FROM TABLE1
LIMIT 2, 1;

SELECT
COL1
FROM TABLE1
LIMIT 1 OFFSET 2;
```

#### Output Code:[¶](#output-code)

##### Snowflake[¶](#snowflake)

```
 SELECT
COL1
FROM
TABLE1
LIMIT 10 OFFSET 2;

SELECT
TOP 1
COL1
FROM
TABLE1;

SELECT
COL1
FROM
TABLE1
LIMIT 1 OFFSET 2;

SELECT
COL1
FROM
TABLE1
LIMIT 1 OFFSET 2;
```

### Into Clause[¶](#into-clause)

In Sybase a Table can be defined by selecting multiple rows and defining a name to stored the date
retrieved. Snowflake does not support this behavior but can emulated by doing a CREATE TABLE AS.

#### Input Code:[¶](#id1)

##### Sybase[¶](#id2)

```
 SELECT
* INTO mynewtable
FROM TABLE1;

SELECT
* INTO LOCAL TEMPORARY TABLE mynewtable
FROM TABLE1;

SELECT
* INTO #mynewtable
FROM TABLE1;
```

#### Output Code:[¶](#id3)

##### Snowflake[¶](#id4)

```
 CREATE OR REPLACE TABLE mynewtable AS
SELECT
*
FROM
TABLE1;

CREATE OR REPLACE TEMPORARY TABLE mynewtable AS
SELECT
*
FROM
TABLE1;

CREATE OR REPLACE TEMPORARY TABLE T_mynewtable AS
SELECT
*
FROM
TABLE1;
```

### Force Index[¶](#force-index)

Snowflake does not contain indexes for query optimization.

#### Input Code:[¶](#id5)

##### Sybase[¶](#id6)

```
 SELECT * FROM MyTable FORCE INDEX (MyIndex);
```

#### Output Code:[¶](#id7)

##### Snowflake[¶](#id8)

```
 SELECT
*
FROM
MyTable
--        --** SSC-FDM-SY0002 - FORCE INDEX IS NOT SUPPORTED IN SNOWFLAKE **
--        FORCE INDEX (MyIndex)
                             ;
```

### TABLE FUNCTIONS[¶](#table-functions)

Snowflake allows calling a stored procedure(when the procedure meets certain
[limitations](https://docs.snowflake.com/en/developer-guide/stored-procedure/stored-procedures-selecting-from#limitations-for-selecting-from-a-stored-procedure))
or a table value function in a FROM clause, but RESULTSETS and windowing cannot be used as
parameters.

#### Input Code:[¶](#id9)

##### Sybase[¶](#id10)

```
 SELECT * FROM
MyProcedure(TABLE (SELECT * FROM TABLE1));

SELECT * FROM MyProcedure(1, 'test');

SELECT * FROM
MyProcedure(
TABLE (SELECT * FROM TABLE1)
OVER (PARTITION BY Col1 ORDER BY Col2 DESC));

SELECT * FROM
MyProcedure(
TABLE (SELECT * FROM AnotherTable) );
```

#### Output Code:[¶](#id11)

##### Snowflake[¶](#id12)

```
 SELECT
*
FROM
TABLE(MyProcedure(
                  !!!RESOLVE EWI!!! /*** SSC-EWI-SY0004 - UNSUPPORTED SYNTAX TABLE FUNCTION CAN'T RECEIVE A QUERY AS PARAMETER ***/!!!TABLE (SELECT * FROM TABLE1)));

SELECT
*
FROM
TABLE(MyProcedure(1, 'test'));


SELECT
*
FROM
TABLE(MyProcedure(
!!!RESOLVE EWI!!! /*** SSC-EWI-SY0004 - UNSUPPORTED SYNTAX TABLE FUNCTION CAN'T RECEIVE A QUERY AS PARAMETER ***/!!!
TABLE (SELECT * FROM TABLE1)
!!!RESOLVE EWI!!! /*** SSC-EWI-SY0005 - UNSUPPORTED SYNTAX TABLE FUNCTION CAN'T BE USED WITH OVER EXPRESSION ***/!!!
OVER (PARTITION BY Col1 ORDER BY Col2 DESC)));


SELECT
*
FROM
TABLE(MyProcedure(
!!!RESOLVE EWI!!! /*** SSC-EWI-SY0004 - UNSUPPORTED SYNTAX TABLE FUNCTION CAN'T RECEIVE A QUERY AS PARAMETER ***/!!!
TABLE (SELECT * FROM AnotherTable) ));
```

### OPEN STRING[¶](#open-string)

Snowflake does not support
[OPENSTRING](https://help.sap.com/docs/SAP_IQ/a898e08b84f21015969fa437e89860c8/a7749cf084f21015b73b899c1520fb06.html#parameters)
functionality.

#### Input Code:[¶](#id13)

##### Sybase[¶](#id14)

```
 -- Openstring from file
SELECT * FROM
OPENSTRING (FILE '/path/to/file.txt')
WITH (Col1 INT, Col2 VARCHAR(20)) AS OS;

-- Openstring from value
SELECT * FROM
OPENSTRING (VALUE '1,test')
WITH (Col1 INT, Col2 VARCHAR(20)) AS OS;

-- Openstring with options
SELECT * FROM
OPENSTRING (FILE '/path/to/file.csv')
WITH (Col1 INT, Col2 VARCHAR(20))
OPTION (DELIMITED BY ',' QUOTE '"') AS OS;
```

#### Output Code:[¶](#id15)

##### Snowflake[¶](#id16)

```
 -- Openstring from file
SELECT
*
FROM
!!!RESOLVE EWI!!! /*** SSC-EWI-SY0006 - OPEN STRING IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
OPENSTRING (FILE '/path/to/file.txt')
WITH (Col1 INT, Col2 VARCHAR(20)) AS OS;

-- Openstring from value
SELECT
*
FROM
!!!RESOLVE EWI!!! /*** SSC-EWI-SY0006 - OPEN STRING IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
OPENSTRING (VALUE '1,test')
WITH (Col1 INT, Col2 VARCHAR(20)) AS OS;

-- Openstring with options
SELECT
*
FROM
!!!RESOLVE EWI!!! /*** SSC-EWI-SY0006 - OPEN STRING IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
OPENSTRING (FILE '/path/to/file.csv')
WITH (Col1 INT, Col2 VARCHAR(20))
OPTION (DELIMITED BY ',' QUOTE '"') AS OS;
```

### DML Derived Table[¶](#dml-derived-table)

In Sybase, during execution, the DML statement specified in the dml-derived table is executed first,
and the rows affected by that DML materialize into a temporary table whose columns are described by
the REFERENCING clause. The temporary table represents the result set of dml-derived-table.
Snowflake does not support this behavior.

#### Input Code:[¶](#id17)

##### Sybase[¶](#id18)

```
 -- DML derived table with insert
SELECT * FROM (INSERT INTO TargetTable (Col1, Col2) VALUES (1, 'test')) REFERENCING (FINAL AS F);

-- DML derived table with update
SELECT * FROM (UPDATE TargetTable SET Col2 = 'updated' WHERE Col1 = 1) REFERENCING (OLD AS O FINAL AS F);

-- DML derived table with delete
SELECT * FROM (DELETE FROM TargetTable WHERE Col1 = 1) REFERENCING (OLD AS O);
```

#### Output Code:[¶](#id19)

##### Snowflake[¶](#id20)

```
 -- DML derived table with insert
SELECT
*
FROM
!!!RESOLVE EWI!!! /*** SSC-EWI-SY0007 - DML DERIVED TABLE NOT SUPPORTED IN SNOWFLAKE ***/!!! (INSERT INTO TargetTable (Col1, Col2) VALUES (1, 'test')) REFERENCING (FINAL AS F);

-- DML derived table with update
SELECT
*
FROM
!!!RESOLVE EWI!!! /*** SSC-EWI-SY0007 - DML DERIVED TABLE NOT SUPPORTED IN SNOWFLAKE ***/!!! (UPDATE TargetTable SET Col2 = 'updated' WHERE Col1 = 1) REFERENCING (OLD AS O FINAL AS F);

-- DML derived table with delete
SELECT
*
FROM
!!!RESOLVE EWI!!! /*** SSC-EWI-SY0007 - DML DERIVED TABLE NOT SUPPORTED IN SNOWFLAKE ***/!!! (DELETE FROM TargetTable WHERE Col1 = 1) REFERENCING (OLD AS O);
```

### KEY JOIN[¶](#key-join)

Snowflake does not support KEY join but when the ON CLAUSE is defined in the query the KEY keyword
and removed otherwise an EWI is inserted.

#### Input Code:[¶](#id21)

##### Sybase[¶](#id22)

```
 SELECT * FROM Table1 KEY JOIN Table2;
SELECT * FROM Table1 KEY JOIN Table2 ON Table1.ID = Table2.ID;
```

#### Output Code:[¶](#id23)

##### Snowflake[¶](#id24)

```
 SELECT
*
FROM
Table1
!!!RESOLVE EWI!!! /*** SSC-EWI-SY0009 - KEY JOIN NOT SUPPORTED IN SNOWFLAKE ***/!!!
KEY JOIN
Table2;

SELECT
*
FROM
Table1
JOIN
Table2
ON Table1.ID = Table2.ID;
```

### OUTER-CROSS APPLY[¶](#outer-cross-apply)

Snowflake transforms the clause the CROSS APPLY into LEFT OUTER JOIN and OUTER APPLY to INNER JOIN.

#### Input Code:[¶](#id25)

##### Sybase[¶](#id26)

```
 -- Apply cross apply
SELECT * FROM Table1 CROSS APPLY (SELECT Col2 FROM Table2 WHERE Table1.ID = Table2.ID) AS AP;

-- Apply outer apply
SELECT * FROM Table1 OUTER APPLY (SELECT Col2 FROM Table2 WHERE Table1.ID = Table2.ID) AS AP;
```

#### Output Code:[¶](#id27)

##### Snowflake[¶](#id28)

```
 -- Apply cross apply
SELECT
    *
FROM
    Table1
    LEFT OUTER JOIN (
        SELECT
            Col2
        FROM
            Table2
        WHERE
            Table1.ID = Table2.ID
    ) AS AP;

-- Apply outer apply
SELECT
    *
FROM
    Table1
    INNER JOIN LATERAL (
        SELECT
            Col2
        FROM
            Table2
        WHERE
            Table1.ID = Table2.ID
    ) AS AP;
```

### CONTAINS Clause[¶](#contains-clause)

In Sybase the
[CONTAINS](https://help.sap.com/docs/SAP_IQ/a898e08b84f21015969fa437e89860c8/a7749cf084f21015b73b899c1520fb06.html)
clause following a table name to filter the table and return only those rows matching the full text
query specified with contains-query. Every matching row of the table is returned together with a
score column that can be referred to using score-correlation-name. Snowflake does not support this
behavior.

#### Input Code:[¶](#id29)

##### Sybase[¶](#id30)

```
 -- Contains clause
SELECT * FROM MyTable CONTAINS (TextColumn, 'search term') AS Score;

-- Contains clause with multiple columns.
SELECT * FROM MyTable CONTAINS (TextColumn,TextColumn2, 'search term') AS Score;
```

#### Output Code:[¶](#id31)

##### Snowflake[¶](#id32)

```
 -- Contains clause
SELECT
*
FROM
MyTable
        !!!RESOLVE EWI!!! /*** SSC-EWI-SY0008 - CONTAINS CLAUSE NOT SUPPORTED IN SNOWFLAKE ***/!!!
        CONTAINS (TextColumn, 'search term') AS Score;

-- Contains clause with multiple columns.
SELECT
*
FROM
MyTable
        !!!RESOLVE EWI!!! /*** SSC-EWI-SY0008 - CONTAINS CLAUSE NOT SUPPORTED IN SNOWFLAKE ***/!!!
        CONTAINS (TextColumn,TextColumn2, 'search term') AS Score;
```

## Related EWIs[¶](#related-ewis)

[SSC-FDM-0009](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0009):
GLOBAL TEMPORARY TABLE FUNCTIONALITY NOT SUPPORTED.

[SSC-FDM-SY0001](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/sybaseFDM#ssc-fdm-sy0001):
CALLING STORED PROCEDURE IN FROM CLAUSE MIGHT HAVE COMPILATION ERRORS

[SSC-FDM-SY0002](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/sybaseFDM#ssc-fdm-sy0002):
FORCE INDEX IS NOT SUPPORTED IN SNOWFLAKE

[SSC-EWI-SY0004](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/sybaseEWI#ssc-ewi-sy0004) -
UNSUPPORTED SYNTAX TABLE FUNCTION CAN’T RECEIVE A QUERY AS PARAMETER

[SSC-EWI-SY0005](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/sybaseEWI#ssc-ewi-sy0005) -
UNSUPPORTED SYNTAX TABLE FUNCTION CAN’T BE USED WITH OVER EXPRESSION

[SSC-EWI-SY0006](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/sybaseEWI#ssc-ewi-sy0006) -
OPEN STRING IS NOT SUPPORTED IN SNOWFLAKE

[SSC-EWI-SY0007](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/sybaseEWI#ssc-ewi-sy0007) -
DML DERIVED TABLE NOT SUPPORTED IN SNOWFLAKE

[SSC-EWI-SY0008](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/sybaseEWI#ssc-ewi-sy0008) -
CONTAINS CLAUSE NOT SUPPORTED IN SNOWFLAKE

[SSC-EWI-SY0009](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/sybaseEWI#ssc-ewi-sy0003) -
KEY JOIN NOT SUPPORTED IN SNOWFLAKE
