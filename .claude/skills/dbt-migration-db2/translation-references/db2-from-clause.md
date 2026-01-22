---
description: The FROM clause specifies an intermediate result table
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/db2/db2-from-clause
title: SnowConvert AI - IBM DB2 - From Clause | Snowflake Documentation
---

## Description

> The FROM clause specifies an intermediate result table

Click [here](https://www.ibm.com/docs/en/db2/11.5?topic=subselect-from-clause) to navigate to the
IBM DB2 documentation page for this syntax.

## Grammar Syntax

![image](https://docs.snowflake.com/en/migrations/snowconvert-docs/_images/from_clause_overview.png)

## Table Reference

### Description 2

> A _table-reference_ specifies an intermediate result table.

Click [here](https://www.ibm.com/docs/en/db2/11.5?topic=clause-table-reference) to navigate to the
IBM DB2 documentation page for this syntax.

### Grammar Syntax 2

![image](https://docs.snowflake.com/en/migrations/snowconvert-docs/_images/table_reference_syntax.png)

Navigate to the following pages to get more details about the translation spec for the subsections
of the Table Reference grammar.

## Analyze Table Expression

### Description 3

> Returns the result of executing a specific data mining model by using an in-database analytics
> provider, a named model implementation, and input data.

Click
[here](https://www.ibm.com/docs/en/db2/11.5?topic=clause-table-reference#sdx-synid_analyze_table-expression)
to navigate to the IBM DB2 documentation page for this syntax.

Analyze Table Expressions are not supported in Snowflake. The output query can be malformed

### Grammar Syntax 3

![image](https://docs.snowflake.com/en/migrations/snowconvert-docs/_images/analyze_table_syntax.png)

### Sample Source Patterns

#### IBM DB2

```sql
 SELECT
   *
FROM v1 ANALYZE_TABLE(
   IMPLEMENTATION 'PROVIDER=SAS; ROUTINE_SOURCE_TABLE=ETLIN.SOURCE_TABLE; ROUTINE_SOURCE_NAME=SCORING_FUN3;')
ORDER BY 1;
```

##### Snowflake

```sql
SELECT
   *
FROM
   !!!RESOLVE EWI!!! /*** SSC-EWI-DB0019 - ANALYZE TABLE FACTOR IS NOT SUPPORTED ***/!!!
 v1 ANALYZE_TABLE(
   IMPLEMENTATION 'PROVIDER=SAS; ROUTINE_SOURCE_TABLE=ETLIN.SOURCE_TABLE; ROUTINE_SOURCE_NAME=SCORING_FUN3;')
ORDER BY 1;
```

### Related EWIs

1. [SSC-EWI-DB0019](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/db2EWI):
   ANALYZE TABLE FACTOR IS NOT SUPPORTED

## Collection Derived Table

### Description 4

> A collection-derived-table can be used to convert the elements of an array into values of a column
> in separate rows. If WITH ORDINALITY is specified, an extra column of data type INTEGER is
> appended. This column contains the position of the element in the array.

Click
[here](https://www.ibm.com/docs/en/db2/11.5?topic=clause-table-reference#sdx-synid_frag-collection-derived-table)
to navigate to the IBM DB2 documentation page for this syntax.

Collection Derived Tables are not supported in Snowflake.

### Grammar Syntax 4

![image](https://docs.snowflake.com/en/migrations/snowconvert-docs/_images/collection_derived_table_syntax_1.png)

![image](https://docs.snowflake.com/en/migrations/snowconvert-docs/_images/collection_derived_table_syntax_2.png)

### Sample Source Patterns 2

#### IBM DB2 2

```sql
SELECT
   *
FROM
   UNNEST(testArray) WITH ORDINALITY;
```

##### Snowflake 2

```sql
SELECT
   *
FROM
   !!!RESOLVE EWI!!! /*** SSC-EWI-DB0016 - UNNEST FUNCTION IS NOT SUPPORTED ***/!!!
   UNNEST(test) WITH ORDINALITY;
```

### Related EWIs 2

1. [SSC-EWI-DB0016](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/db2EWI):
   UNNEST FUNCTION IS NOT SUPPORTED

## Data Change Table Reference

### Description 5

> A _data-change-table-reference_ clause specifies an intermediate result table. This table is based
> on the rows that are directly changed by the searched UPDATE, searched DELETE, or INSERT statement
> that is included in the clause.

Click
[here](https://www.ibm.com/docs/en/db2/11.5?topic=clause-table-reference#sdx-synid_data-change-table-reference)
to navigate to the IBM DB2 documentation page for this syntax.

Data Change Table Reference is not supported in Snowflake. The output query can be malformed.

### Grammar Syntax 5

![image](https://docs.snowflake.com/en/migrations/snowconvert-docs/_images/data_change_table_syntax.png)

### Sample Source Patterns 3

#### IBM DB2 3

```sql
 SELECT
   *
FROM
   OLD Table(UPDATE T1 SET NAME = 'Tony' where ID = 4)
```

#### Snowflake 3

```sql
SELECT
   *
FROM
   !!!RESOLVE EWI!!! /*** SSC-EWI-DB0006 - INTERMEDIATE RESULT TABLE IS NOT SUPPORTED. ***/!!!
   OLD Table(UPDATE T1 SET NAME = 'Tony' where ID = 4);
```

### Related EWIs 3

1. [SSC-EWI-DB0006](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/db2EWI#ssc-ewi-db0006):
   INTERMEDIATE RESULT TABLE IS NOT SUPPORTED.

## External Table Reference

### Description 6

> An external table resides in a text-based, delimited or non-delimited file outside of a database.
> An external-table-reference specifies the name of the file that contains an external table.

Click
[here](https://www.ibm.com/docs/en/db2/11.5?topic=clause-table-reference#sdx-synid_external-table-reference)
to navigate to the IBM DB2 documentation page for this syntax.

External Table Reference is not supported in Snowflake. The output query can be malformed.

### Grammar Syntax 6

![image](https://docs.snowflake.com/en/migrations/snowconvert-docs/_images/external_table_syntax.png)

### Sample Source Patterns 4

#### IBM DB2 4

```sql
 SELECT
   *
FROM
   EXTERNAL SOMENAME AS T1 LIKE TABLE2 USING(COMPRESS NO)
```

##### Snowflake 4

```sql
SELECT
   *
FROM
   !!!RESOLVE EWI!!! /*** SSC-EWI-DB0014 - THE USE OF EXTERNAL TABLE REFERENCES IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
   EXTERNAL SOMENAME AS T1 LIKE TABLE2 USING(COMPRESS NO);
```

### Related EWIs 4

1. [SSC-EWI-DB0014](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/db2EWI#ssc-ewi-db0014):
   THE USE OF EXTERNAL TABLE REFERENCES IS NOT SUPPORTED IN SNOWFLAKE

## Nested Table Expression

### Description 7

> A fullselect in parentheses is called a _nested table expression_. The intermediate result table
> is the result of that fullselect.

Click
[here](https://www.ibm.com/docs/en/db2/11.5?topic=clause-table-reference#sdx-synid_frag-nested-table-expression)
to navigate to the IBM DB2 documentation page for this syntax.

Warning

Nested Table Expression is partially applicable in Snowflake.

### Grammar Syntax 7

![image](https://docs.snowflake.com/en/migrations/snowconvert-docs/_images/nested_table_syntax.png)

### Sample Source Patterns 5

#### Unsupported cases

##### IBM DB2 5

```sql
 Select
   AValue
from
   LATERAL RETURN DATA UNTIL FEDERATED SQLSTATE VALUE 'stringConstant' WITHIN(
      Select
         AValue
      from
         ATable
   );
```

##### Snowflake 5

```sql
Select
   AValue
from
   LATERAL
--           --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE. CONTINUE HANDLER **
--           RETURN DATA UNTIL FEDERATED SQLSTATE VALUE 'stringConstant' WITHIN
                                                                             (
      Select
         AValue
      from
         ATable
   );
```

### Related EWIs 5

1. [SSC-FDM-0027](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0027):
   REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.

## ONLY TABLE REFERENCE

### Description 8

> The use of ONLY(table-name) or ONLY(view-name) means that the rows of the applicable subtables or
> subviews are not included in the intermediate result table.

Click
[here](https://www.ibm.com/docs/en/db2/11.5?topic=clause-table-reference#sdx-synid_only-table-reference)
to navigate to the IBM DB2 documentation page for this syntax.

### Grammar Syntax 8

![image](https://docs.snowflake.com/en/migrations/snowconvert-docs/_images/only_table_syntax.png)

### Sample Source Patterns 6

#### IBM DB2 6

```sql
 Select * from ONLY(ATable) AS CorrelationName;
```

##### Snowflake 6

```sql
 Select * from
   ATable AS CorrelationName;
```

## OUTER TABLE REFERENCE

### Description 9

> The use of OUTER(table-name) or OUTER(view-name) represents a virtual table.

Click
[here](https://www.ibm.com/docs/en/db2/11.5?topic=clause-table-reference#sdx-synid_outer-table-reference)
to navigate to the IBM DB2 documentation page for this syntax.

Warning

OUTER TABLE REFERENCE is not applicable in Snowflake.

### Grammar Syntax 9

![image](https://docs.snowflake.com/en/migrations/snowconvert-docs/_images/outer_table_syntax.png)

### Sample Source Patterns 7

#### IBM DB2 7

```sql
 Select * from OUTER(ATable) AS CorrelationName;
```

##### Snowflake 7

```sql
 Select * from
   !!!RESOLVE EWI!!! /*** SSC-EWI-DB0004 - OUTER TABLE REFERENCE IS NOT SUPPORTED IN SNOWFLAKE. ***/!!! OUTER(ATable) AS CorrelationName;
```

### Related EWIs 6

1. [SSC-EWI-DB0004](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/db2EWI#ssc-ewi-db0004):
   OUTER TABLE REFERENCE IS NOT SUPPORTED IN SNOWFLAKE.

## Period Specification

> A period-specification identifies an intermediate result table consisting of the rows of the
> referenced table where the period matches the specification. A period-specification can be
> specified following the name of a temporal table or the name of a view

Click
[here](https://www.ibm.com/docs/en/db2/11.5?topic=clause-table-reference#sdx-synid_period-specification)
to navigate to the IBM DB2 documentation page for this syntax.

Period Specification is currently not supported by Snowflake.

### Grammar Syntax 10

![image](https://docs.snowflake.com/en/migrations/snowconvert-docs/_images/period_specification_syntax.png)

### Sample Source Patterns 8

#### IBM DB2 8

```sql
 SELECT
   *
FROM
   Table1
FOR BUSINESS_TIME AS OF "12-12-12"
```

#### Snowflake 8

```sql
SELECT
   *
FROM
   Table1
   !!!RESOLVE EWI!!! /*** SSC-EWI-DB0003 - PERIOD SPECIFICATION IS NOT SUPPORTED IN SNOWFLAKE. ***/!!!
FOR BUSINESS_TIME AS OF "12-12-12";
```

### Related EWIs 7

1. [SSC-EWI-DB0003](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/db2EWI#ssc-ewi-db0003):
   PERIOD SPECIFICATION IS NOT SUPPORTED IN SNOWFLAKE.

## Table Function Reference

### Description 10

> Table functions return columns of a table, resembling a table created through a simple CREATE
> TABLE statement. A table function can be used only in the FROM clause of a statement.

Click
[here](https://www.ibm.com/docs/en/db2/11.5?topic=clause-table-reference#sdx-synid_table-function-reference)
to navigate to the IBM DB2 documentation page for this syntax.

Warning

Table Function Reference is not applicable in Snowflake.

### Grammar Syntax 11

![image](https://docs.snowflake.com/en/migrations/snowconvert-docs/_images/table_function_syntax_1.png)

![image](https://docs.snowflake.com/en/migrations/snowconvert-docs/_images/table_function_syntax_2.png)

### Sample Source Patterns 9

For the transformation of Table Function Reference, we must comment out the
table-UDF-cardinality-clause. This clause is used for performance reasons, and is not relevant in
Snowflake.

#### IBM DB2 9

```sql
 SELECT * FROM TABLE(TUDF1(3) CARDINALITY 30) AS X;
```

##### Snowflake 9

```sql
SELECT * FROM TABLE(TUDF1(3)) AS X;
```

Note that each function along with the type of it’s arguments specified in the table reference must
exist, otherwise it will cause errors.
