---
description: A subdivision of the SELECT statement done in IBM DB2.
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/db2/db2-select-statement
title: SnowConvert AI - IBM DB2 - SELECT STATEMENT | Snowflake Documentation
---

## Description[¶](#description)

> A subdivision of the SELECT statement done in IBM DB2.

Click [here](https://www.ibm.com/docs/en/db2/11.5?topic=queries-fullselect) to navigate to the IBM
DB2 documentation page for this syntax.

## Grammar Syntax[¶](#grammar-syntax)

![image](../../../../_images/select_statement_overview.png)

## From Clause[¶](#from-clause)

All information about this part of the syntax is specified on the
[from-clause page](db2-from-clause).

## Where Clause[¶](#where-clause)

> The WHERE clause specifies an intermediate result table that consists of those rows of R for which
> the search-condition is true. R is the result of the FROM clause of the subselect.

Click [here](https://www.ibm.com/docs/en/db2/11.5?topic=subselect-where-clause) to navigate to the
IBM DB2 documentation page for this syntax.

### Grammar Syntax[¶](#id1)

![image](../../../../_images/where_clause_syntax.png)

SuccessPlaceholder

All the grammar specified in this where clause of DB2 is ANSI compliant, equivalent to Snowflake,
and is therefore translated as is by SnowConvert AI.

## Group By Clause[¶](#group-by-clause)

> The GROUP BY clause specifies an intermediate result table that consists of a grouping of the rows
> of R. R is the result of the previous clause of the subselect.

Click [here](https://www.ibm.com/docs/en/db2/11.5?topic=subselect-group-by-clause) to navigate to
the IBM DB2 documentation page for this syntax.

### Grammar Syntax[¶](#id2)

![image](../../../../_images/group_by_clause_syntax.png)

### No explicit column reference[¶](#no-explicit-column-reference)

> The following expressions, which do not contain an explicit column reference, can be used in a
> grouping-expression to identify a column of R:
>
> - ROW CHANGE TIMESTAMP FOR table-designator
> - ROW CHANGE TOKEN FOR table-designator
> - RID_BIT or RID scalar function

ROW CHANGE Expressions and RID/RID_BIT scalar functions are not supported in Snowflake.

#### Sample Source Patterns

##### IBM DB2

```
select * from product group by ROW CHANGE TIMESTAMP FOR product;
```

Copy

##### Snowflake

```
select * from
 product
--!!!RESOLVE EWI!!! /*** SSC-EWI-0021 - GROUP BY ROW CHANGE TIMESTAMP FOR NOT SUPPORTED IN SNOWFLAKE ***/!!!
--group by ROW CHANGE TIMESTAMP FOR product
                                         ;
```

Copy

##### IBM DB2

```
    select * from product group by RID();
```

Copy

##### Snowflake

```
select * from
 product
--!!!RESOLVE EWI!!! /*** SSC-EWI-0021 - GROUP BY scalar function RID NOT SUPPORTED IN SNOWFLAKE ***/!!!
--group by RID()
              ;
```

Copy

#### Related EWIs

1. [SSC-EWI-0021](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0021)

## Fetch Clause

### Description

> Sets a maximum number of rows to be retrieved.

Click [here](https://www.ibm.com/docs/en/db2/11.5?topic=subselect-fetch-clause) to navigate to the
IBM DB2 documentation page for this syntax.

### Grammar Syntax

![image](../../../../_images/fetch_clause_syntax.png)

### Sample Source Patterns

#### Fetch without row count

##### IBM DB2

```
 SELECT * FROM Product FETCH First Row ONLY;
/* or */
SELECT * FROM Product FETCH First Rows ONLY;
/* or */
SELECT * FROM Product FETCH Next Row ONLY;
/* or */
SELECT * FROM Product FETCH Next Rows ONLY;
```

Copy

###### Snowflake

```
SELECT * FROM
   Product
FETCH NEXT 1 ROW ONLY;
```

Copy

## Offset Clause

### Description

> Sets the number of rows to skip.

Click [here](https://www.ibm.com/docs/en/db2/11.5?topic=subselect-offset-clause) to navigate to the
IBM DB2 documentation page for this syntax.

### Grammar Syntax

![image](../../../../_images/offset_clause_syntax_1.png)

![image](../../../../_images/offset_clause_syntax_2.png)

### Sample Source Patterns

#### Offset row-count

##### IBM DB2

```
 SELECT * FROM Product OFFSET 3 ROW;
/* or */
SELECT * FROM Product OFFSET 3 ROWS;
```

Copy

##### Snowflake

```
SELECT * FROM
   Product
LIMIT NULL
OFFSET 3;
```

Copy

#### Limit X,Y

##### IBM DB2

```
SELECT * FROM Product LIMIT 3,2;
```

Copy

##### Snowflake

```
SELECT * FROM
   Product
OFFSET 3 ROWS
FETCH NEXT 2 ROWS ONLY;
```

Copy

## Order by Clause

### Description

> The ORDER BY clause specifies an ordering of the rows of the result table.

Click [here](https://www.ibm.com/docs/en/db2/11.5?topic=subselect-order-by-clause) to navigate to
the IBM DB2 documentation page for this syntax.

### Grammar Syntax

![image](../../../../_images/order_by_clause_syntax_1.png)

![image](../../../../_images/order_by_clause_syntax_2.png)

### Sample Source Patterns

The only paths of ORDER BY in Db2 that are not supported in Snowflake are those when it is used with
ORDER OF and INPUT SEQUENCE; hence, if these are present, the clause will be marked with an EWI.

#### IBM DB2 Not Supported Examples

```
Select * from ORDERBYTest ORDER BY ORDER OF TableDesignator;
Select * from ORDERBYTest ORDER BY INPUT SEQUENCE;
```

Copy

##### Snowflake

```
Select * from
   ORDERBYTest
!!!RESOLVE EWI!!! /*** SSC-EWI-0021 - ORDER BY ORDER OF NOT SUPPORTED IN SNOWFLAKE ***/!!!
ORDER BY ORDER OF TableDesignator;


Select * from
   ORDERBYTest
!!!RESOLVE EWI!!! /*** SSC-EWI-0021 - ORDER BY INPUT SEQUENCE NOT SUPPORTED IN SNOWFLAKE ***/!!!
ORDER BY INPUT SEQUENCE;
```

Copy

### Related EWIs

1. [SSC-EWI-0021](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0021):
   NODE NOT SUPPORTED

## Values Clause

### Description

> Derives a result table by specifying the actual values, using expressions or row expressions, for
> each column of a row in the result table. hin

Note

The VALUES clause is not supported in Snowflake. For this reason, it is translated to a SELECT
statement, as shown in the examples below.

### Grammar Syntax[¶](#id23)

![image](../../../../_images/values_clause_syntax.png)

### Sample Source Patterns[¶](#id24)

The Values clause is not supported in Snowflake. For this reason, the values clause is translated to
a select query.

#### IBM DB2[¶](#id25)

```
VALUES 1, 2, 3
```

Copy

<!-- prettier-ignore -->
|     |
|---|
|1|
|2|
|3|

##### Snowflake[¶](#id26)

```
SELECT 1, 2, 3
```

Copy

<!-- prettier-ignore -->
|     |     |     |
|---|---|---|
|1|2|3|

For the values with multiple rows, a Union is used:

##### IBM DB2[¶](#id27)

```
VALUES (1, 1, 1),
    (2, 2, 2),
    (3, 3, 3)
```

Copy

<!-- prettier-ignore -->
|     |     |     |
|---|---|---|
|1|1|1|
|2|2|2|
|3|3|3|

##### Snowflake[¶](#id28)

```
SELECT
   1, 1, 1
UNION
SELECT
   2, 2, 2
UNION
SELECT
   3, 3, 3
```

Copy

<!-- prettier-ignore -->
|     |     |     |
|---|---|---|
|1|1|1|
|2|2|2|
|3|3|3|

## Removed Clauses[¶](#removed-clauses)

### Description[¶](#id29)

The following clauses are removed since they are not applicable in Snowflake:

- FOR READ ONLY
- Update Clause
- Optimize for Clause
- Concurrent access resolution Clause
- Isolation Clause

### Sample Source Patterns[¶](#id30)

#### IBM DB2[¶](#id31)

```
-- For Read Only
SELECT
   *
FROM
   Table1
FOR READ ONLY;


-- Update Clause
SELECT
   *
FROM
   Table1
FOR UPDATE OF
   COL1,
   COL2;


--Optimize For Clause
SELECT
   *
FROM
   Table1
OPTIMIZE FOR 2 ROWS;


-- Concurrent access resolution Clause
SELECT
   *
FROM
   Table1
WAIT FOR OUTCOME;


-- Isolation Clause
SELECT
   *
FROM
   Table1
WITH RR USE AND KEEP EXCLUSIVE LOCKS;
```

Copy

##### Snowflake[¶](#id32)

```
-- For Read Only
SELECT
   *
FROM
   Table1;


-- Update Clause
SELECT
   *
FROM
   Table1;


--Optimize For Clause
SELECT
   *
FROM
   Table1;


-- Concurrent access resolution Clause
SELECT
   *
FROM
   Table1;


-- Isolation Clause
SELECT
   *
FROM
   Table1;
```

Copy
