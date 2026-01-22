---
description: SQL Server
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/transact/transact-create-view
title: SnowConvert AI - SQL Server-Azure Synapse - Views | Snowflake Documentation
---

## Sample Source Patterns

### SIMPLE CREATE VIEW

The following example shows a transformation for a simple `CREATE VIEW` statement.

#### Transact

```sql
CREATE VIEW VIEWNAME
AS
SELECT AValue from ATable;
```

##### Snowflake

```sql
CREATE OR REPLACE VIEW VIEWNAME
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
AS
SELECT
AValue
from
ATable;
```

## CREATE OR ALTER VIEW

The **CREATE OR ALTER** definition used in SqlServer is transformed to **CREATE OR REPLACE** in
Snowflake.

### Transact 2

```sql
CREATE OR ALTER VIEW VIEWNAME
AS
SELECT AValue from ATable;
```

#### Snowflake 2

```sql
CREATE OR REPLACE VIEW VIEWNAME
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
AS
SELECT
AValue
from
ATable;
```

## CREATE VIEW WITH

In this type of View, after the name of the View, the following clauses can come

- `WITH ENCRYPTION`
- `WITH SCHEMABINDING`
- `WITH VIEW_METADATA`

Warning

Notice that the above clauses are removed from the translation. because are not relevant in
Snowflake syntax.

### Transact 3

```sql
CREATE OR ALTER VIEW VIEWNAME
WITH ENCRYPTION
AS
SELECT AValue from ATable;
```

### Snowflake 3

```sql
CREATE OR REPLACE VIEW VIEWNAME
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
AS
SELECT
AValue
from
ATable;
```

## CREATE VIEW AS SELECT WITH CHECK OPTION

In this type of View, the clause **`WITH CHECK OPTION`** comes after the end of the Select statement
used in the Create View.

Warning

Notice that `WITH CHECK OPTION`is removed from the translation, because is not relevant in Snowflake
syntax.

### Transact 4

```sql
CREATE OR ALTER VIEW VIEWNAME
AS
SELECT AValue from ATable
WITH CHECK OPTION;
```

### Snowflake 4

```sql
CREATE OR REPLACE VIEW VIEWNAME
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
AS
SELECT
AValue
from
ATable;
```

## CREATE VIEW AS COMMON TABLE EXPRESSION

Common Table Expressions must be used to retrieve the data:

### Transact 5

```sql
CREATE VIEW EMPLOYEEIDVIEW
AS
WITH CTE AS ( SELECT NationalIDNumber from [HumanResources].[Employee]
UNION ALL
SELECT BusinessEntityID FROM [HumanResources].[EmployeeDepartmentHistory] )
SELECT * FROM MyCTE;
```

### Snowflake 5

```sql
CREATE OR REPLACE VIEW EMPLOYEEIDVIEW
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
AS
--** SSC-PRF-TS0001 - PERFORMANCE WARNING - RECURSION FOR CTE NOT CHECKED. MIGHT REQUIRE RECURSIVE KEYWORD **
WITH CTE AS ( SELECT
NationalIDNumber
from
HumanResources.Employee
UNION ALL
SELECT
BusinessEntityID
FROM
HumanResources.EmployeeDepartmentHistory
)
SELECT
*
FROM
MyCTE;
```

## UNSUPPORTED SCENARIOS

Common table expressions with Update, Insert or Delete statements will be commented out because they
are not supported in Snowflake and SQLServer.

In the case where an invalid CTE is added to the view, this will be completely commented out.

```sql
 --!!!RESOLVE EWI!!! /*** SSC-EWI-0021 - COMMON TABLE EXPRESSION IN VIEW NOT SUPPORTED ***/!!!
--CREATE OR REPLACE VIEW PUBLIC.EmployeeInsertVew
--AS
--WITH MyCTE AS ( SELECT
--NationalIDNumber
--from
--HumanResources.Employee
--UNION ALL
--SELECT
--BusinessEntityID
--FROM
--HumanResources.EmployeeDepartmentHistory
--)
--INSERT INTO PUBLIC.Dummy
```

### FINAL SAMPLE

Let’s see a final sample, let’s put together all the cases that we have seen so far and see how the
transformation would be

#### Transact 6

```sql
CREATE OR ALTER VIEW VIEWNAME
WITH ENCRYPTION
AS
Select AValue from ATable
WITH CHECK OPTION;
```

##### Snowflake 6

```sql
CREATE OR REPLACE VIEW VIEWNAME
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
AS
Select
AValue
from
ATable;
```

As you can see, we changed the **OR ALTER** with **OR REPLACE** and we removed the clause **WITH
ENCRYPTION** that comes after the view name and the **WITH CHECK OPTION** that comes after the
Select.

### Related EWIs

1. [SSC-PRF-TS0001](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/performance-review/sqlServerPRF#ssc-prf-ts0001):
   Performance warning - recursion for CTE not checked. Might require a recursive keyword.
