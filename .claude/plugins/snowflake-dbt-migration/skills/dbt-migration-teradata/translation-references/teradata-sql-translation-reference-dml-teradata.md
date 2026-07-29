---
description:
  In this section, you will find the documentation for the translation reference of Data
  Manipulation Language Elements.
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/teradata/sql-translation-reference/dml-teradata
title: SnowConvert AI - Teradata - DML | Snowflake Documentation
---

## Delete Statement

> See [Delete statement](https://docs.teradata.com/r/huc7AEHyHSROUkrYABqNIg/z8eO9bdxtjFRveHdDwwYPQ)

Teradata support calling more than one table in the`FROM`clause, Snowflake does not. Therefore, it
is necessary to use the`USING`clause to refer to the extra tables involved in the condition.

### Teradata

### Delete

```sql
DEL FROM MY_TABLE ALL;
DEL FROM MY_TABLE_2 WHERE COL1 > 50;
DELETE T1 FROM TABLE1 T1, TABLE2 T2 WHERE T1.ID = T2.ID;
DELETE FROM TABLE1 T1, TABLE2 T2 WHERE T1.ID = T2.ID;
DELETE T1 FROM TABLE2 T2, TABLE1 T1 WHERE T1.ID = T2.ID;
DELETE FROM TABLE1 WHERE TABLE1.COLUMN1 = TABLE2.COLUMN2
```

### Snowflake

### Delete 2

```sql
DELETE FROM
MY_TABLE;

DELETE FROM
MY_TABLE_2
WHERE
COL1 > 50;

DELETE FROM
TABLE1 T1
USING TABLE2 T2
WHERE
T1.ID = T2.ID;

DELETE FROM
TABLE1 T1
USING TABLE2 T2
WHERE
T1.ID = T2.ID;

DELETE FROM
TABLE1 T1
USING TABLE2 T2
WHERE
T1.ID = T2.ID;

DELETE FROM
TABLE1
WHERE
TABLE1.COLUMN1 = TABLE2.COLUMN2;
```

### Known Issues

#### 1. DEL abbreviation unsupported

The abbreviation is unsupported in Snowflake but it is translated correctly by changing it to
DELETE.

### Related EWIs

No related EWIs.

## Set Operators

The SQL set operators manipulate the result sets of several queries combining the results of each
query into a single result set.

### Note

Some parts in the output code are omitted for clarity reasons.

> See [Set operators](https://docs.teradata.com/r/b8dd8xEYJnxfsq4uFRrHQQ/Q8qU3AO1RXLNFCPOGTX73g)

Set Operators in both Teradata and Snowflake have the same syntax and supported scenarios `EXCEPT`,
`INTERSECT`, and `UNION` except for the clause `ALL` in the `INTERSECT ALL`, which is not supported
in Snowflake, resulting in the portion of the `ALL` as a commented code after the conversion.

### Teradata 2

### Intersect

```sql
 SELECT LastName, FirstName FROM employees
INTERSECT
SELECT FirstName, LastName FROM contractors;

SELECT LastName, FirstName FROM employees
INTERSECT ALL
SELECT FirstName, LastName FROM contractors;
```

#### Snowflake 2

#### Intersect 2

```sql
 SELECT
LastName,
FirstName FROM
employees
INTERSECT
SELECT
FirstName,
LastName FROM
contractors;

SELECT
LastName,
FirstName FROM
employees
INTERSECT
        !!!RESOLVE EWI!!! /*** SSC-EWI-0040 - THE 'INTERSECT ALL QUANTIFIER' CLAUSE IS NOT SUPPORTED IN SNOWFLAKE ***/!!! ALL
SELECT
FirstName,
LastName FROM
contractors;
```

### Known Issues 2

#### 1. INTERSECT ALL unsupported

The INTERSECT ALL is unsupported in Snowflake and then the part ALL will be commented.

### Related EWIs 2

1. [SSC-EWI-0040](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0040):
   Statement Not Supported.

## Update Statement

### Description

> Modifies column values in existing rows of a table.
> ([Teradata SQL Language Reference UPDATE](https://docs.teradata.com/r/huc7AEHyHSROUkrYABqNIg/k6fC7ozmhIZZXa315VjJAw))

### Sample Source Patterns

#### Basic case

##### Teradata 3

##### Update

```sql
 UPDATE CRASHDUMPS.TABLE1 i
 SET COLUMN4 = CRASHDUMPS.TABLE2.COLUMN3
 WHERE i.COLUMN1 = CRASHDUMPS.TABLE2.COLUMN1
 AND i.COLUMN3 = 'L';
```

##### Snowflake 3

##### Update 2

```sql
UPDATE CRASHDUMPS.TABLE1 AS i
 SET
  i.COLUMN4 = CRASHDUMPS.TABLE2.COLUMN3
 FROM
  CRASHDUMPS.TABLE2
  WHERE i.COLUMN1 = CRASHDUMPS.TABLE2.COLUMN1
  AND UPPER(RTRIM( i.COLUMN3)) = UPPER(RTRIM('L'));
```

#### UPDATE with forward alias

Teradata supports referencing an alias before it is declared, but Snowflake does not. The
transformation for this scenario is to take the referenced table and change the alias for the table
name it references.

##### Teradata 4

##### Update 3

```sql
 UPDATE i
 FROM CRASHDUMPS.TABLE2, CRASHDUMPS.TABLE1 i
 SET COLUMN4 = CRASHDUMPS.TABLE2.COLUMN3
 WHERE i.COLUMN1 = CRASHDUMPS.TABLE2.COLUMN1
 AND i.COLUMN3 = 'L';
```

##### Snowflake 4

##### Update 4

```sql
UPDATE CRASHDUMPS.TABLE1 AS i
  SET
  i.COLUMN4 = CRASHDUMPS.TABLE2.COLUMN3
  FROM
  CRASHDUMPS.TABLE2
  WHERE i.COLUMN1 = CRASHDUMPS.TABLE2.COLUMN1
  AND UPPER(RTRIM( i.COLUMN3)) = UPPER(RTRIM('L'));
```

#### UPDATE with target table in the the FROM clause

Teradata supports having the target table defined in the FROM clause, this is removed in Snowflake
to avoid duplicate alias and ambiguous column reference errors.

##### Teradata 5

##### Update 5

```sql
UPDATE some_table
FROM some_table
SET Code = Code + 100
WHERE Name = 'A';
```

##### Snowflake 5

##### Update 6

```sql
UPDATE some_table
  SET Code = Code + 100
  WHERE
  UPPER(RTRIM( Name)) = UPPER(RTRIM('A'));
```

### Related EWIs 3

No related EWIs.

## With Modifier

Select statement that uses the WITH modifier with a list of several named queries also known as
common table expressions (CTEs).

> See
> [With Modifier](https://docs.teradata.com/r/Teradata-VantageTM-SQL-Data-Manipulation-Language/July-2021/SELECT-Statements/WITH-Modifier)

Snowflake supports Teradata’s `WITH` modifier on a SELECT statement that has several `CTEs` (Common
Table Expressions). Teradata supports any order of CTE definition, regardless of whether it is
referenced before it is declared or not, but Snowflake requires that if a CTE calls another CTE, it
must be defined before it is called. Then the converted sequence of CTEs within the WITH will be
reordered into the unreferenced CTEs, then the CTE that calls the next CTE, and so on.

Where there is a cycle detected in the WITH calling sequence, it will be left as the original,
without any changes to the sequence as detailed in an example of the
[SSC-EWI-TD0077](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/teradataEWI#ssc-ewi-td0077).

In the example below, there are two CTEs named n1 and n2, the n1 referring to n2. Then the n2 must
be defined first in Snowflake as the corresponding converted code.

### Note 2

Some parts of the output code are omitted for clarity reasons.

### Teradata 6

### With Modifier 2

```sql
 WITH recursive n1(c1) as (select c1, c3 from t2, n1),
     n2(c2) as (select c2 from tablex)
     SELECT * FROM t1;
```

#### Snowflake 6

#### With Modifier 3

```sql
 WITH RECURSIVE n1(c1) AS
(
     SELECT
          c1,
          c3 from
          t2, n1
),
n2(c2) AS
(
     SELECT
          c2 from
          tablex
)
SELECT
     * FROM
     t1;
```

### Known Issues 3

#### 1. Impossible to reorder when cycles were found

When the CTEs references are analyzed and there is a cycle between the calls of the CTEs, the CTEs
will not be ordered.

### Related EWIs 4

No related EWIs.

## Insert Statement

SQL statement that adds new rows to a table.

### Note 3

Some parts in the output code are omitted for clarity reasons.

> See [Insert statement](https://docs.teradata.com/r/0I5vemahub4iSU2bk5WA1A/SQ4EQb1a8WMHn3tbrcvW9Q)

In Teradata, there is an alternate`INSERT`syntax that assigns the value for each table column
inline. This alternate structure requires a special transformation to be supported in Snowflake. The
inline assignment of the values is separated and placed inside the `VALUES(...)` part of the
Snowflake `INSERT INTO` statement.

### Teradata 7

### Insert

```sql
 INSERT INTO appDB.logTable (
    process_name = 'S2F_BOOKS_LOAD_NEW'
    , session_id = 105678989
    , message_txt = ''
    , message_ts = '2019-07-23 00:00:00'
    , Insert_dt = CAST((CURRENT_TIMESTAMP(0)) AS DATE FORMAT 'YYYY-MM-DD'));
```

#### Snowflake 7

#### Insert 2

```sql
 INSERT INTO appDB.logTable (
process_name, session_id, message_txt, message_ts, Insert_dt)
VALUES ('S2F_BOOKS_LOAD_NEW', 105678989, '', '2019-07-23 00:00:00', TO_DATE((CURRENT_TIMESTAMP(0))));
```

### Known Issues 4

No issues were found.

### Related EWIs 5

No related EWIs.

## LOGGING ERRORS

### Note 4

Some parts in the output code are omitted for clarity reasons.

### Note 5

Non-relevant statement.

Warning

**Notice that this statement is** **removed from the migration** **because it is a non-relevant
syntax. It means that it is not required in Snowflake.**

### Description 2

Statement to log errors when using statements as `INSERT...SELECT.` Please review the following
[documentation](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/SQL-Data-Manipulation-Language/Statement-Syntax/INSERT/INSERT-...-SELECT/INSERT/INSERT-...-SELECT-Examples/Example-Logging-Errors-with-INSERT-...-SELECT).

### Sample Source Patterns 2

#### LOGGING ERRORS 2

In this example, notice that `LOGGING ERRORS` has been removed because it is not a relevant syntax.
The syntax is not required in Snowflake.

##### Teradata 8

```sql
 INSERT INTO MY_TABLE
SELECT *
FROM MY_SAMPLE
LOGGING ERRORS;
```

##### Snowflake 8

```sql
INSERT INTO MY_TABLE SELECT
*
FROM
MY_SAMPLE;
```

#### LOGGING ALL ERRORS

In this example, notice that `LOGGING ALL ERRORS` has been removed because it is not a relevant
syntax. The syntax is not required in Snowflake.

##### Teradata 2 2

```sql
 INSERT INTO MY_TABLE
SELECT *
FROM MY_SAMPLE
LOGGING ALL ERRORS;
```

##### Snowflake 2 2

```sql
 INSERT INTO MY_TABLE SELECT
*
FROM
MY_SAMPLE;
```

#### LOGGING ERRORS WITH NO LIMIT

In this example, notice that `LOGGING ERRORS WITH NO LIMIT` has been removed because it is not a
relevant syntax. The syntax is not required in Snowflake.

##### Teradata 3 2

```sql
 INSERT INTO MY_TABLE
SELECT *
FROM MY_SAMPLE
LOGGING ERRORS WITH NO LIMIT;
```

##### Snowflake 3 2

```sql
 INSERT INTO MY_TABLE SELECT
*
FROM
MY_SAMPLE;
```

#### LOGGING ERRORS WITH LIMIT OF

In this example, notice that `LOGGING ERRORS WITH LIMIT OF` has been removed because it is not a
relevant syntax. The syntax is not required in Snowflake.

##### Teradata 4 2

```sql
 INSERT INTO MY_TABLE
SELECT *
FROM MY_SAMPLE
LOGGING ERRORS WITH LIMIT OF 100;
```

##### Snowflake 4 2

```sql
 INSERT INTO MY_TABLE SELECT
*
FROM
MY_SAMPLE;
```

### Known Issues 5

No issues were found.

### Related EWIs 6

No related EWIs.

## Select Statement

> See
> [Select statement](https://docs.teradata.com/reader/b8dd8xEYJnxfsq4uFRrHQQ/kH97CTRIXdd~i1yLemdvKw)

Snowflake supports Teradata’s `SELECT` syntax with a few exceptions. Primarily, it does not support
the `SEL` abbreviation.​

### Teradata 9

### Sel

```sql
SEL DISTINCT col1, col2 FROM table1
```

### Snowflake 9

### Select

```sql
SELECT DISTINCT col1,
col2 FROM
table1;
```

Teradata supports referencing an alias before it is declared, but Snowflake does not. The
transformation for this scenario is to take the referenced column and change the alias for the
column name it references.

### Teradata 10

### Alias

```sql
SELECT
my_val, sum(col1),
col2 AS my_val FROM table1
```

### Snowflake 10

### Alias 2

```sql
SELECT
my_val,
SUM(col1),
col2 AS my_val FROM
table1;
```

### Removed clause options

The following clause options are not relevant to Snowflake, therefore they are removed during the
migration.

<!-- prettier-ignore -->
|Teradata|Snowflake|
|---|---|
|Expand on|Unsupported|
|Normalize|Unsupported|
|With check option (Query)|Unsupported|

### Known Issues 6

#### 1. SEL abbreviation unsupported

The abbreviation is unsupported in Snowflake but it is translated correctly by changing it to
SELECT.

### Related EWIs 7

No related EWIs.

## ANY Predicate

Warning

This is a work in progress, changes may be applied in the future.

### Description 3

In Teradata enables quantification in a comparison operation or IN/NOT IN predicate. The comparison
of expression and at least one value in the set of values returned by subquery is true. Please
review the following
[Teradata documentation](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/SQL-Functions-Expressions-and-Predicates/Logical-Predicates/ANY/ALL/SOME)
for more information.

#### Teradata syntax

```sql
 { expression quantifier ( literal [ {, | OR} ... ] ) |
  { expression | ( expression [,...] ) } quantifier ( subquery )
}
```

Where quantifier:

```sql
 { comparison_operator [ NOT ] IN } { ALL |ANY | SOME }
```

#### Snowflake syntax

SuccessPlaceholder

In subquery form, IN is equivalent to `= ANY` and NOT IN is equivalent to `<> ALL`. Review the
following [Snowflake documentation](https://docs.snowflake.com/en/sql-reference/functions/in) for
more infromation.

To compare individual values:

```sql
 `<value>` [ NOT ] IN ( `<value_1>` [ , `<value_2>` ...  ] )
```

To compare _row constructors_ (parenthesized lists of values):

```sql
 ( `<value_A>` [, `<value_B>` ... ] ) [ NOT ] IN (  ( `<value_1>` [ , `<value_2>` ... ] )  [ , ( `<value_3>` [ , `<value_4>` ... ] )  ...  ]  )
```

To compare a value to the values returned by a subquery:

```sql
 `<value>` [ NOT ] IN ( `<subquery>` )
```

### Sample Source Patterns 3

#### Sample data

##### Teradata 5 2

##### Query

```sql
 CREATE TABLE Employee (
    EmpNo INT,
    Name VARCHAR(100),
    DeptNo INT
);

INSERT INTO Employee (EmpNo, Name, DeptNo)
VALUES (1, 'Alice', 100);

INSERT INTO Employee (EmpNo, Name, DeptNo)
VALUES (2, 'Bob', 300);

INSERT INTO Employee (EmpNo, Name, DeptNo)
VALUES (3, 'Charlie', 500);

INSERT INTO Employee (EmpNo, Name, DeptNo)
VALUES (4, 'David', 200);

INSERT INTO Employee (EmpNo, Name, DeptNo)
VALUES (5, 'Eve', 100);
```

##### Snowflake 5 2

##### Query 2

```sql
 CREATE OR REPLACE TABLE Employee (
    EmpNo INT,
    Name VARCHAR(100),
    DeptNo INT
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "01/14/2025",  "domain": "test" }}'
;

INSERT INTO Employee (EmpNo, Name, DeptNo)
VALUES (1, 'Alice', 100);

INSERT INTO Employee (EmpNo, Name, DeptNo)
VALUES (2, 'Bob', 300);

INSERT INTO Employee (EmpNo, Name, DeptNo)
VALUES (3, 'Charlie', 500);

INSERT INTO Employee (EmpNo, Name, DeptNo)
VALUES (4, 'David', 200);

INSERT INTO Employee (EmpNo, Name, DeptNo)
VALUES (5, 'Eve', 100);
```

#### Equal ANY pedicate in WHERE clause

##### Teradata 11

##### Input

```sql
 SELECT DeptNo
FROM Employee
WHERE DeptNo = ANY(100,300,500) ;
```

##### Output

<!-- prettier-ignore -->
|DeptNo|
|---|
|100|
|500|
|100|
|300|

###### Snowflake 11

##### Input 2

```sql
 SELECT DeptNo
FROM Employee
WHERE DeptNo IN(100,300,500) ;
```

##### Output 2

<!-- prettier-ignore -->
|DeptNo|
|---|
|100|
|500|
|100|
|300|

#### Other comparison operators in WHERE clause

When there are other comparison operators, there equivalent translation is to add a subquery with
the required logic.

##### Teradata 12

##### Input 3

```sql
 SELECT Name, DeptNo
FROM Employee
WHERE DeptNo < ANY(100,300,500) ;
```

##### Output 3

<!-- prettier-ignore -->
|Name|DeptNo|
|---|---|
|Eve|100|
|Alice|100|
|David|200|
|Bob|300|

###### Snowflake 12

##### Input 4

```sql
 SELECT Name, DeptNo
FROM Employee
WHERE DeptNo < ANY
(SELECT DeptNo
FROM Employee
WHERE DeptNo > 100
OR DeptNo > 300
OR DeptNo > 500);
```

##### Output 4

<!-- prettier-ignore -->
|NAME|DEPTNO|
|---|---|
|Alice|100|
|Eve|100|
|Bob|300|
|David|200|

#### IN ANY in WHERE clause

##### Teradata 13

##### Input 5

```sql
 SELECT DeptNo
FROM Employee
WHERE DeptNo IN ANY(100,300,500) ;
```

##### Output 5

<!-- prettier-ignore -->
|DeptNo|
|---|
|100|
|500|
|100|
|300|

###### Snowflake 13

##### Input 6

```sql
 SELECT DeptNo
FROM Employee
WHERE DeptNo IN(100,300,500) ;
```

##### Output 6

<!-- prettier-ignore -->
|DeptNo|
|---|
|100|
|500|
|100|
|300|

#### NOT IN ALL in WHERE clause

##### Teradata 14

##### Input 7

```sql
 SELECT Name, DeptNo
FROM Employee
WHERE DeptNo NOT IN ALL(100, 200);
```

##### Output 7

<!-- prettier-ignore -->
|Name|DeptNo|
|---|---|
|Charlie|500|
|Bob|300|

###### Snowflake 14

##### Input 8

```sql
 SELECT Name, DeptNo
FROM Employee
WHERE DeptNo NOT IN (100, 200);
```

##### Output 8

<!-- prettier-ignore -->
|Name|DeptNo|
|---|---|
|Charlie|500|
|Bob|300|

### Known Issues 7

#### NOT IN ANY in WHERE clause

##### Teradata 15

##### Input 9

```sql
 SELECT Name, DeptNo
FROM Employee
WHERE DeptNo NOT IN ANY(100, 200);
```

##### Output 9

<!-- prettier-ignore -->
|Name|DeptNo|
|---|---|
|Eve|100|
|Charlie|500|
|Alice|100|
|David|200|
|Bob|300|

###### Snowflake 15

##### Input 10

```sql
 SELECT Name, DeptNo
FROM Employee
WHERE DeptNo IN (100, 200)
   OR DeptNo NOT IN (100, 200);
```

##### Output 10

<!-- prettier-ignore -->
|Name|DeptNo|
|---|---|
|Eve|100|
|Charlie|500|
|Alice|100|
|David|200|
|Bob|300|

### Related EWIs 8

No related EWIs.

## Expand On Clause

Translation reference to convert Teradata Expand On functionality to Snowflake

### Description 4

> The Expand On clause expands a column having a **period** data type, creating a regular time
> series of rows based on the period value in the input row. For more information about Expand On
> clause, see the
> [Teradata documentation](https://docs.teradata.com/r/huc7AEHyHSROUkrYABqNIg/542VMPPqGwHBhF98pnTz9w).

### Sample Source Patterns 4

#### Note 6

Some parts in the output code are omitted for clarity reasons.

#### Sample data 2

##### Teradata 6 2

```sql
 CREATE TABLE table1 (id INTEGER, pd PERIOD (TIMESTAMP));

INSERT INTO
    table1
VALUES
    (
        1,
        PERIOD(
            TIMESTAMP '2022-05-23 10:15:20.00009',
            TIMESTAMP '2022-05-23 10:15:25.000012'
        )
    );
```

##### Snowflake 6 2

```sql
 CREATE OR REPLACE TABLE table1 (
    id INTEGER,
    pd VARCHAR(58) !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;

INSERT INTO table1
VALUES (
1, PUBLIC.PERIOD_UDF(
            TIMESTAMP '2022-05-23 10:15:20.00009',
            TIMESTAMP '2022-05-23 10:15:25.000012'
        ) !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!);
```

#### Expand On Clause 2

Suppose you want to expand the period column by seconds, for this Expand On clause has anchor period
expansion and interval literal expansion.

##### Anchor Period Expansion

##### Teradata 7 2

```sql
 SELECT
    id,
    BEGIN(bg)
FROM
    table1 EXPAND ON pd AS bg BY ANCHOR ANCHOR_SECOND;
```

##### Result

<!-- prettier-ignore -->
|id|BEGIN (bg)|
|---|---|
|1|2022-05-23 10:15:21.0000|
|1|2022-05-23 10:15:22.0000|
|1|2022-05-23 10:15:23.0000|
|1|2022-05-23 10:15:24.0000|
|1|2022-05-23 10:15:25.0000|

Snowflake doesn’t support Expand On clause. To reproduce the same results and functionality, the
Teradata SQL code will be contained in a CTE block, with an **EXPAND_ON_UDF** and **TABLE**
function, using **FLATTEN** function to return multiple rows, **ROW_COUNT_UDF** and
**DIFF_TTIME_PERIOD_UDF** to indicate how many rows are needed and returning **VALUE** to help the
EXPAND_ON_UDF to calculate the different regular time series. This CTE block returns the same expand
columns alias as in the Expand On clause, so the result can be used in any usage of period datatype.

##### Snowflake 7 2

```sql
 WITH ExpandOnCTE AS
(
    SELECT
        PUBLIC.EXPAND_ON_UDF('ANCHOR_SECOND', VALUE, pd) bg
    FROM
        table1,
        TABLE(FLATTEN(PUBLIC.ROW_COUNT_UDF(PUBLIC.DIFF_TIME_PERIOD_UDF('ANCHOR_SECOND', pd))))
)
SELECT
    id,
    PUBLIC.PERIOD_BEGIN_UDF(bg) !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!
FROM
    table1,
    ExpandOnCTE;
```

##### Result 2

<!-- prettier-ignore -->
|id|PERIOD_BEGIN_UDF(bg)|
|---|---|
|1|2022-05-23 10:15:21.0000|
|1|2022-05-23 10:15:22.0000|
|1|2022-05-23 10:15:23.0000|
|1|2022-05-23 10:15:24.0000|
|1|2022-05-23 10:15:25.0000|

### Known Issues 8

The Expand On clause can use interval literal expansion, for this case, SnowConvert AI will add an
error that this translation is planned.

#### Interval literal expansion

##### Teradata 8 2

```sql
 SELECT
    id,
    BEGIN(bg)
FROM
    table1 EXPAND ON pd AS bg BY INTERVAL '1' SECOND;
```

##### Result 3

<!-- prettier-ignore -->
|id|BEGIN(bg)|
|---|---|
|1|2022-05-23 10:15:20.0000|
|1|2022-05-23 10:15:21.0000|
|1|2022-05-23 10:15:22.0000|
|1|2022-05-23 10:15:23.0000|
|1|2022-05-23 10:15:24.0000|

##### Snowflake 8 2

```sql
 SELECT
    id,
    PUBLIC.PERIOD_BEGIN_UDF(bg) !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!
FROM
    table1
!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'EXPAND ON' NODE ***/!!!
EXPAND ON pd AS bg BY INTERVAL '1' SECOND;
```

### Related EWIs 9

1. [SSC-EWI-0073](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0073):
   Pending Functional Equivalence Review.
2. [SSC-EWI-TD0053](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/teradataEWI#ssc-ewi-td0053):
   Snowflake does not support the period datatype, all periods are handled as varchar instead.

## Normalize

Translation reference to convert Teradata Normalize functionality to Snowflake

### Description 5

> NORMALIZE specifies that period values in the first-period column that meet or overlap are
> combined to form a period that encompasses the individual period values. For more information
> about Normalize clause, see the
> [Teradata documentation](https://docs.teradata.com/r/2_MC9vCtAJRlKle2Rpb0mA/UuxiA0mklFgv~33X5nyKMA).

### Sample Source Patterns 5

#### Note 7

Some parts in the output code are omitteed for clarity reasons.

#### Sample data 3

##### Teradata 9 2

```sql
 CREATE TABLE project (
    emp_id INTEGER,
    project_name VARCHAR(20),
    dept_id INTEGER,
    duration PERIOD(DATE)
);

INSERT INTO project
VALUES
    (
        10,
        'First Phase',
        1000,
        PERIOD(DATE '2010-01-10', DATE '2010-03-20')
    );

INSERT INTO project
VALUES
    (
        10,
        'First Phase',
        2000,
        PERIOD(DATE '2010-03-20', DATE '2010-07-15')
    );

INSERT INTO project
VALUES
    (
        10,
        'Second Phase',
        2000,
        PERIOD(DATE '2010-06-15', DATE '2010-08-18')
    );

INSERT INTO project
VALUES
    (
        20,
        'First Phase',
        2000,
        PERIOD(DATE '2010-03-10', DATE '2010-07-20')
    );

INSERT INTO project
VALUES
    (
        20,
        'Second Phase',
        1000,
        PERIOD(DATE '2020-05-10', DATE '2020-09-20')
    );
```

##### Snowflake 9 2

```sql
 CREATE OR REPLACE TABLE project (
    emp_id INTEGER,
    project_name VARCHAR(20),
    dept_id INTEGER,
    duration VARCHAR(24) !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;

INSERT INTO project
VALUES (
10,
        'First Phase',
        1000, PUBLIC.PERIOD_UDF(DATE '2010-01-10', DATE '2010-03-20') !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!);

INSERT INTO project
VALUES (
10,
        'First Phase',
        2000, PUBLIC.PERIOD_UDF(DATE '2010-03-20', DATE '2010-07-15') !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!);

INSERT INTO project
VALUES (
10,
        'Second Phase',
        2000, PUBLIC.PERIOD_UDF(DATE '2010-06-15', DATE '2010-08-18') !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!);

INSERT INTO project
VALUES (
20,
        'First Phase',
        2000, PUBLIC.PERIOD_UDF(DATE '2010-03-10', DATE '2010-07-20') !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!);

INSERT INTO project
VALUES (
20,
        'Second Phase',
        1000, PUBLIC.PERIOD_UDF(DATE '2020-05-10', DATE '2020-09-20') !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!);
```

#### Normalize Clause

Suppose you want to use Normalize clause with the employee id.

##### Teradata 10 2

```sql
 SELECT
    NORMALIZE emp_id,
    duration
FROM
    project;
```

##### Result 4

<!-- prettier-ignore -->
|EMP_ID|DURATION|
|---|---|
|20|(2010-03-10, 2010-07-20)|
|10|(2010-01-10, 2010-08-18)|
|20|(2020-05-10, 2010-09-20)|

##### Snowflake 10 2

```sql
 !!!RESOLVE EWI!!! /*** SSC-EWI-TD0079 - THE REQUIRED PERIOD TYPE COLUMN WAS NOT FOUND ***/!!!
WITH NormalizeCTE AS
(
    SELECT
        T1.*,
        SUM(GroupStartFlag)
        OVER (
        PARTITION BY
            emp_id, duration
        ORDER BY
            PeriodColumn_begin
        ROWS UNBOUNDED PRECEDING) GroupID
    FROM
        (
            SELECT
                emp_id,
                duration,
                PUBLIC.PERIOD_BEGIN_UDF(PeriodColumn) PeriodColumn_begin,
                PUBLIC.PERIOD_END_UDF(PeriodColumn) PeriodColumn_end,
                (CASE
                    WHEN PeriodColumn_begin <= LAG(PeriodColumn_end)
                    OVER (
                    PARTITION BY
                        emp_id, duration
                    ORDER BY
                        PeriodColumn_begin,
                        PeriodColumn_end)
                        THEN 0
                    ELSE 1
                END) GroupStartFlag
            FROM
                project
        ) T1
)
SELECT
    emp_id,
    duration,
    PUBLIC.PERIOD_UDF(MIN(PeriodColumn_begin), MAX(PeriodColumn_end))
FROM
    NormalizeCTE
GROUP BY
    emp_id,
    duration,
    GroupID;
```

##### Result 5

<!-- prettier-ignore -->
|EMP_ID|PUBLIC.PERIOD_UDF(MIN(START_DATE), MAX(END_DATE))|
|---|---|
|20|2020-05-10\*2010-09-20|
|20|2010-03-10\*2010-07-20|
|10|2010-01-10\*2010-08-18|

### Known Issues 9

Normalize clause can use **ON MEETS OR OVERLAPS**, **ON OVERLAPS** or **ON OVERLAPS OR MEETS,** for
these cases SnowConvert AI will add an error that this translation is planned for the future.

#### Teradata 11 2

```sql
 SELECT NORMALIZE ON MEETS OR OVERLAPS emp_id, duration FROM table1;
```

##### Snowflake 11 2

```sql
 SELECT
       !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'NORMALIZE SET QUANTIFIER' NODE ***/!!!
       NORMALIZE ON MEETS OR OVERLAPS emp_id,
duration FROM
table1;
```

### Related EWIs 10

1. [SSC-EWI-0073](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0073):
   Pending Functional Equivalence Review.
2. [SSC-EWI-TD0079](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/teradataEWI#ssc-ewi-td0079):
   The required period type column was not found.
3. [SSC-EWI-TD0053](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/teradataEWI#ssc-ewi-td0053):
   Snowflake does not support the period datatype, all periods are handled as varchar instead.

## Reset When

### Description 6

> Reset When determines the partition on which an SQL window function operates based on some
> specific condition. If the condition evaluates to True, a new dynamic sub partition is created
> within the existing window partition. For more information about Reset When, see the
> [Teradata documentation](https://docs.teradata.com/reader/1DcoER_KpnGTfgPinRAFUw/b7wL86OoMTPno6hrSPNdDg).

### Sample Source Patterns 6

#### Sample data 4

##### Teradata 12 2

###### Query 2 2

```sql
CREATE TABLE account_balance
(
  account_id INTEGER NOT NULL,
  month_id INTEGER,
  balance INTEGER
)
UNIQUE PRIMARY INDEX (account_id, month_id);

INSERT INTO account_balance VALUES (1, 1, 60);
INSERT INTO account_balance VALUES (1, 2, 99);
INSERT INTO account_balance VALUES (1, 3, 94);
INSERT INTO account_balance VALUES (1, 4, 90);
INSERT INTO account_balance VALUES (1, 5, 80);
INSERT INTO account_balance VALUES (1, 6, 88);
INSERT INTO account_balance VALUES (1, 7, 90);
INSERT INTO account_balance VALUES (1, 8, 92);
INSERT INTO account_balance VALUES (1, 9, 10);
INSERT INTO account_balance VALUES (1, 10, 60);
INSERT INTO account_balance VALUES (1, 11, 80);
INSERT INTO account_balance VALUES (1, 12, 10);
```

###### Result 2 2

<!-- prettier-ignore -->
|account_id|month_id|balance|
|---|---|---|
|1|1|60|
|1|2|99|
|1|3|94|
|1|4|90|
|1|5|80|
|1|6|88|
|1|7|90|
|1|8|92|
|1|9|10|
|1|10|60|
|1|11|80|
|1|12|10|

##### Snowflake 12 2

###### Query 3

```sql
CREATE OR REPLACE TABLE account_balance (
  account_id INTEGER NOT NULL,
  month_id INTEGER,
  balance INTEGER,
  UNIQUE (account_id, month_id)
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;

INSERT INTO account_balance
VALUES (1, 1, 60);

INSERT INTO account_balance
VALUES (1, 2, 99);

INSERT INTO account_balance
VALUES (1, 3, 94);

INSERT INTO account_balance
VALUES (1, 4, 90);

INSERT INTO account_balance
VALUES (1, 5, 80);

INSERT INTO account_balance
VALUES (1, 6, 88);

INSERT INTO account_balance
VALUES (1, 7, 90);

INSERT INTO account_balance
VALUES (1, 8, 92);

INSERT INTO account_balance
VALUES (1, 9, 10);

INSERT INTO account_balance
VALUES (1, 10, 60);

INSERT INTO account_balance
VALUES (1, 11, 80);

INSERT INTO account_balance
VALUES (1, 12, 10);
```

###### Result 3 2

<!-- prettier-ignore -->
|account_id|month_id|balance|
|---|---|---|
|1|1|60|
|1|2|99|
|1|3|94|
|1|4|90|
|1|5|80|
|1|6|88|
|1|7|90|
|1|8|92|
|1|9|10|
|1|10|60|
|1|11|80|
|1|12|10|

#### Reset When 2

For each account, suppose you want to analyze the sequence of consecutive monthly balance increases.
When the balance of one month is less than or equal to the balance of the previous month, the
requirement is to reset the counter to zero and restart.

To analyze this data, Teradata SQL uses a window function with a nested aggregate and a Reset When
statement, as follows:

##### Teradata 13 2

###### Query 4

```sql
SELECT
   account_id,
   month_id,
   balance,
   (
     ROW_NUMBER() OVER (
       PARTITION BY account_id
       ORDER BY
         month_id RESET WHEN balance <= SUM(balance) OVER (
           PARTITION BY account_id
           ORDER BY month_id
           ROWS BETWEEN 1 PRECEDING AND 1 PRECEDING
         )
     ) -1
   ) AS balance_increase
FROM account_balance
ORDER BY 1, 2;
```

###### Result 4 2

<!-- prettier-ignore -->
|account_id|month_id|balance|balance_increase|
|---|---|---|---|
|1|1|60|0|
|1|2|99|1|
|1|3|94|0|
|1|4|90|0|
|1|5|80|0|
|1|6|88|1|
|1|7|90|2|
|1|8|92|3|
|1|9|10|0|
|1|10|60|1|
|1|11|80|2|
|1|12|10|0|

##### Snowflake 13 2

Snowflake does not support the Reset When clause in window functions. To reproduce the same result,
the Teradata SQL code must be translated using native SQL syntax and nested subqueries, as follows:

###### Query 5

```sql
SELECT
   account_id,
   month_id,
   balance,
   (
     ROW_NUMBER() OVER (
   PARTITION BY
      account_id, new_dynamic_part
   ORDER BY
         month_id
     ) -1
   ) AS balance_increase
FROM
   (
      SELECT
   account_id,
   month_id,
   balance,
   previous_value,
   SUM(dynamic_part) OVER (
           PARTITION BY account_id
           ORDER BY month_id
   ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
         ) AS new_dynamic_part
      FROM
   (
      SELECT
         account_id,
         month_id,
         balance,
         SUM(balance) OVER (
                 PARTITION BY account_id
                 ORDER BY month_id
                 ROWS BETWEEN 1 PRECEDING AND 1 PRECEDING
               ) AS previous_value,
         (CASE
            WHEN balance <= previous_value
               THEN 1
            ELSE 0
         END) AS dynamic_part
      FROM
         account_balance
   )
   )
ORDER BY 1, 2;
```

###### Result 5 2

<!-- prettier-ignore -->
|account_id|month_id|balance|balance_increase|
|---|---|---|---|
|1|1|60|0|
|1|2|99|1|
|1|3|94|0|
|1|4|90|0|
|1|5|80|0|
|1|6|88|1|
|1|7|90|2|
|1|8|92|3|
|1|9|10|0|
|1|10|60|1|
|1|11|80|2|
|1|12|10|0|

Two nested sub-queries are needed to support the Reset When functionality in Snowflake.

In the inner sub-query, a dynamic partition indicator (dynamic_part) is created and populated.
dynamic_part is set to 1 if one month’s balance is less than or equal to the preceding month’s
balance; otherwise, it’s set to 0.

In the next layer, a new_dynamic_part attribute is generated as the result of a SUM window function.

Finally, a new_dynamic_part is added as a new partition attribute (dynamic partition) to the
existing partition attribute (account_id) and applies the same ROW_NUMBER() window function as in
Teradata.

After these changes, Snowflake generates the same output as Teradata.

#### Reset When when conditional window function is a column

Same example as above, except that now the window function used in the RESET WHEN condition is
defined as a column called `previous`. This variation changes the transformation slightly since it
is no longer necessary to define the `previous_value` as in the previous example. It is the same
workaround.

##### Teradata 14 2

###### Query 6

```sql
SELECT
   account_id,
   month_id,
   balance,
   SUM(balance) OVER (
           PARTITION BY account_id
           ORDER BY month_id
           ROWS BETWEEN 1 PRECEDING AND 1 PRECEDING
         ) AS previous,
   (
     ROW_NUMBER() OVER (
       PARTITION BY account_id
       ORDER BY
         month_id RESET WHEN balance <= previous
     )
   ) AS balance_increase
FROM account_balance
ORDER BY 1, 2;
```

###### Result 6

<!-- prettier-ignore -->
|account_id|month_id|balance|previous|balance_increase|
|---|---|---|---|---|
|1|1|60||0|
|1|2|99|60|1|
|1|3|94|99|0|
|1|4|90|94|0|
|1|5|80|90|0|
|1|6|88|80|1|
|1|7|90|88|2|
|1|8|92|90|3|
|1|9|10|92|0|
|1|10|60|10|1|
|1|11|80|60|2|
|1|12|10|80|0|

##### Snowflake 14 2

###### Query 7

```sql
SELECT
   account_id,
   month_id,
   balance,
   SUM(balance) OVER (
           PARTITION BY account_id
           ORDER BY month_id
           ROWS BETWEEN 1 PRECEDING AND 1 PRECEDING
         ) AS previous,
   (
     ROW_NUMBER() OVER (
   PARTITION BY
      account_id, new_dynamic_part
   ORDER BY
         month_id
     )
   ) AS balance_increase
FROM
   (
      SELECT
   account_id,
   month_id,
   balance,
   SUM(balance) OVER (
           PARTITION BY account_id
           ORDER BY month_id
           ROWS BETWEEN 1 PRECEDING AND 1 PRECEDING
         ) AS previous,
   SUM(dynamic_part) OVER (
           PARTITION BY account_id
           ORDER BY month_id
   ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
         ) AS new_dynamic_part
      FROM
   (
      SELECT
         account_id,
         month_id,
         balance,
         SUM(balance) OVER (
                 PARTITION BY account_id
                 ORDER BY month_id
                 ROWS BETWEEN 1 PRECEDING AND 1 PRECEDING
               ) AS previous,
         (CASE
            WHEN balance <= previous
               THEN 1
            ELSE 0
         END) AS dynamic_part
      FROM
         account_balance
   )
   )
ORDER BY 1, 2;
```

###### Untitled

<!-- prettier-ignore -->
|account_id|month_id|balance|previous|balance_increase|
|---|---|---|---|---|
|1|1|60||0|
|1|2|99|60|1|
|1|3|94|99|0|
|1|4|90|94|0|
|1|5|80|90|0|
|1|6|88|80|1|
|1|7|90|88|2|
|1|8|92|90|3|
|1|9|10|92|0|
|1|10|60|10|1|
|1|11|80|60|2|
|1|12|10|80|0|

### Known Issues 10

The RESET WHEN clause could have some variations such as its condition. Currently, SnowConvert AI
only supports binary conditions (<=, >=, <> or =), in any other type, as `IS NOT NULL`, SnowConvert
AI will remove the RESET WHEN clause and add an error message since it is not supported in
Snowflake, as shown in the following example.

#### Teradata 15 2

##### Query 8

```sql
SELECT
    account_id,
    month_id,
    balance,
    ROW_NUMBER() OVER (
        PARTITION BY account_id
        ORDER BY month_id
        RESET WHEN balance IS NOT NULL
        ROWS UNBOUNDED PRECEDING
    ) as balance_increase
FROM account_balance
ORDER BY 1,2;
```

#### Snowflake 15 2

##### Query 9

```sql
SELECT
    account_id,
    month_id,
    balance,
    ROW_NUMBER() OVER (
        PARTITION BY account_id
    !!!RESOLVE EWI!!! /*** SSC-EWI-TD0077 - RESET WHEN CLAUSE IS NOT SUPPORTED IN THIS SCENARIO DUE TO ITS CONDITION ***/!!!
        ORDER BY month_id
        ROWS UNBOUNDED PRECEDING
    ) as balance_increase
FROM
    account_balance
ORDER BY 1,2;
```

### Related EWIs 11

- [SSC-EWI-TD0077](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/teradataEWI#ssc-ewi-td0077):
  RESET WHEN clause is not supported in this scenario due to its condition.

## SAMPLE clause

### Description 7

The SAMPLE clause in Teradata reduces the number of rows to be processed and it returns one or more
samples of rows as a list of fractions or as a list of numbers of rows. The clause is used in the
SELECT query. Please review the following
[Teradata documentation](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/SQL-Data-Manipulation-Language/SELECT-Statements/SAMPLE-Clause)
for more information.

#### Teradata syntax 2

```sql
SAMPLE
  [ WITH REPLACEMENT ]
  [ RANDOMIZED LOCALIZATION ]
  { { fraction_description | count_description } [,...] |
    when_clause ]
  }
```

#### Snowflake syntax 2

Review the following
[Snowflake documentation](https://docs.snowflake.com/en/sql-reference/constructs/sample) for more
information. `SAMPLE` and `TABLESAMPLE` are synonymous.

```sql
SELECT ...
FROM ...
  { SAMPLE | TABLESAMPLE } [ samplingMethod ]
[ ... ]
```

Where:

```sql
samplingMethod ::= {
{ BERNOULLI | ROW } ( { `<probability>` | `<num>` ROWS } ) |
{ SYSTEM | BLOCK } ( `<probability>` ) [ { REPEATABLE | SEED } ( `<seed>` ) ] }
```

- In Snowflake, the following keywords can be used interchangeably:

  > - `SAMPLE | TABLESAMPLE`
  > - `BERNOULLI | ROW`
  > - `SYSTEM | BLOCK`
  > - `REPEATABLE | SEED`

Review the following table to check on key differences.

<!-- prettier-ignore -->
|SAMPLE behavior|Teradata|Snowflake|
|---|---|---|
|Sample by probability|Also known as fraction description. It must be a fractional number between 0,1 and 1.|Decimal number between 0 and 100.|
|Fixed number of rows|Also known as count description. It is a positive integer that determines the number of rows to be sampled.|It specifies the number of rows (up to 1,000,000) to sample from the table. Can be any integer between `0` (no rows selected) and `1000000` inclusive.|
|Repeated rows|It is known as `WITH REPLACEMENT.` This is used to query more samples than there are rows in the table.|It is known as `REPEATABLE` or `SEED`. This is used to make the query deterministic. It means that the same set of rows will be the same for each query run.|
|Sampling methods|_Proportional_ and `RANDOMIZED ALLOCATION.`|`BERNOULLI` or `SYSTEM`.|

### Sample Source Patterns 7

#### Sample data 5

##### Teradata 16

###### Query 10

```sql
CREATE TABLE Employee (
    EmpNo INT,
    Name VARCHAR(100),
    DeptNo INT
);

INSERT INTO Employee (EmpNo, Name, DeptNo)
VALUES (1, 'Alice', 100);

INSERT INTO Employee (EmpNo, Name, DeptNo)
VALUES (2, 'Bob', 300);

INSERT INTO Employee (EmpNo, Name, DeptNo)
VALUES (3, 'Charlie', 500);

INSERT INTO Employee (EmpNo, Name, DeptNo)
VALUES (4, 'David', 200);

INSERT INTO Employee (EmpNo, Name, DeptNo)
VALUES (5, 'Eve', 100);
```

##### Snowflake 16

###### Query 11

```sql
CREATE OR REPLACE TABLE Employee (
    EmpNo INT,
    Name VARCHAR(100),
    DeptNo INT
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "01/14/2025",  "domain": "test" }}'
;

INSERT INTO Employee (EmpNo, Name, DeptNo)
VALUES (1, 'Alice', 100);

INSERT INTO Employee (EmpNo, Name, DeptNo)
VALUES (2, 'Bob', 300);

INSERT INTO Employee (EmpNo, Name, DeptNo)
VALUES (3, 'Charlie', 500);

INSERT INTO Employee (EmpNo, Name, DeptNo)
VALUES (4, 'David', 200);

INSERT INTO Employee (EmpNo, Name, DeptNo)
VALUES (5, 'Eve', 100);
```

#### SAMPLE clause 2

##### Fixed number of rows

Notice that for this example, the number of rows are a fixed number but not necessarily are the same
result for each run.

###### Teradata 16 2

###### Input 2 2

```sql
SELECT * FROM Employee SAMPLE 2;
```

**Output** 2 rows.

###### Snowflake 16 2

###### Input 3 2

```sql
SELECT * FROM Employee SAMPLE (2 ROWS);
```

**Output** 2 rows.

##### Rows number based on probability

This option will return a variety of rows depending on the probability set.

###### Teradata 17

###### Input 4 2

```sql
SELECT * FROM Employee SAMPLE 0.25;
```

**Output** 25% of probability for each row: 1 output row.

###### Snowflake 17

###### Input 5 2

```sql
SELECT * FROM Employee SAMPLE (25);
```

**Output** 25% of probability for each row: 1 output row.

### Known Issues 11

#### Fixed number of rows with replacement

This option will return a fixed number of rows and will allows the repetition of the rows. In
Snowflake, it is not possible to request more samples than rows in a table.

##### Teradata sample

##### Input 6 2

```sql
SELECT * FROM Employee SAMPLE WITH REPLACEMENT 8;
```

##### Output 2 2

<!-- prettier-ignore -->
|EmpNo|Name|DeptNo|
|---|---|---|
|5|Eve|100|
|5|Eve|100|
|4|David|200|
|3|Charlie|500|
|1|Alice|100|

#### SAMPLEID related functionality

In Teradata, it is possible to assign a unique ID to each sample that is specified. It helps to
identify which belongs to which sample. This is not ANSI grammar, instead it is an extension of
Teradata.

##### Teradata sample 2

##### Input 7 2

```sql
SELECT name, SAMPLEID FROM employee SAMPLE 0.5, 0.25, 0.25;
```

##### Output 3 2

<!-- prettier-ignore -->
|Name|SampleId|
|---|---|
|Eve|3|
|Charlie|1|
|Alice|1|
|David|2|
|Bob|1|

In Snowflake, there is not a SAMPLEID function. A possible workaround may be the following, but it
has to be adaptaed to each single case:

##### Snowflake possible workaround

##### Input 8 2

```sql
WITH sampled_data AS (
    -- Sample 100% of the rows from the Employee table
    SELECT *,
           ROW_NUMBER() OVER (ORDER BY EmpNo) AS row_num,
           COUNT(*) OVER () AS total_rows  -- Get the total row count to calculate sample size
    FROM Employee
)
SELECT Name,
       CASE
           -- First 50% of the rows
           WHEN row_num <= total_rows * 0.5 THEN 1
           -- Next 25% of the rows
           WHEN row_num <= total_rows * 0.75 THEN 2
           -- Remaining 25% of the rows
           ELSE 3
       END AS sample_id
FROM sampled_data
ORDER BY sample_id, row_num;  -- Order by sample_id and row_num for consistency
```

##### Output 4 2

<!-- prettier-ignore -->
|Name|SAMPLE_ID|
|---|---|
|Alice|1|
|Bob|1|
|Charlie|2|
|David|3|
|Eve|3|

#### Conditional sampling

In Snowflake there is not conditional sampling. This can be achieve by using CTE’s.

##### Teradata sample 3

##### Input 9 2

```sql
SELECT * FROM employee
SAMPLE WHEN DeptNo > 100 then 0.9
ELSE 0.1 END;
```

##### Output 5 2

<!-- prettier-ignore -->
|EmpNo|Name|DeptNo|
|---|---|---|
|3|Charlie|500|
|4|David|200|
|2|Bob|300|

### Related EWIs 12

[SSC-EWI-0021](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0021):
Syntax not supported in Snowflake.
