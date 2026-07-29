---
description: Translation reference for the Transact-SQL User Defined Functions
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/transact/transact-create-function
title: SnowConvert AI - SQL Server - CREATE FUNCTION | Snowflake Documentation
---

## Description

SQL Server only supports two types of
[User Defined Functions](https://docs.microsoft.com/en-us/sql/t-sql/statements/create-function-transact-sql?view=sql-server-ver15):

- [Scalar](https://docs.microsoft.com/en-us/sql/t-sql/statements/create-function-transact-sql?view=sql-server-ver15#a-using-a-scalar-valued-user-defined-function-that-calculates-the-iso-week)
- [Table-Valued](https://docs.microsoft.com/en-us/sql/t-sql/statements/create-function-transact-sql?view=sql-server-ver15#b-creating-an-inline-table-valued-function)

Using these UDFs types, is possible to subcategorized them into **simple and complex,** according to
the inner logic.

Simple UDFs, matches the SQL Server syntax with Snowflake syntax. This type doesn’t add any logic
and goes straightforward to the result. These are usually match to Snowflake’s SQL UDFs. SnowConvert
supports translating SQL Server Scalar User Defined Functions directly to
[Snowflake Scripting UDFs](https://docs.snowflake.com/en/migrations/snowconvert-docs/developer-guide/udf/sql/udf-sql-procedural-functions)
when they meet specific criteria.

Complex UDFs, makes extensive use of a particular statements
([INSERT](https://docs.microsoft.com/en-us/sql/t-sql/statements/insert-transact-sql?view=sql-server-ver15),
[DELETE](https://docs.microsoft.com/en-us/sql/t-sql/statements/delete-transact-sql?view=sql-server-ver15),
[UPDATE](https://docs.microsoft.com/en-us/sql/t-sql/queries/update-transact-sql?view=sql-server-ver15),
[SET](https://docs.microsoft.com/en-us/sql/t-sql/language-elements/set-local-variable-transact-sql?view=sql-server-ver15),
[DECLARE](https://docs.microsoft.com/en-us/sql/t-sql/language-elements/declare-local-variable-transact-sql?view=sql-server-ver15),
etc) or
[control-of-flow](https://docs.microsoft.com/en-us/sql/t-sql/language-elements/control-of-flow?view=sql-server-ver15)
blocks
([IF…ELSE](https://docs.microsoft.com/en-us/sql/t-sql/language-elements/if-else-transact-sql?view=sql-server-ver15),
[WHILE](https://docs.microsoft.com/en-us/sql/t-sql/language-elements/while-transact-sql?view=sql-server-ver15),
etc) and usually represents a mismatch or violation to Snowflake’s SQL UDFs definition.

## Limitations

Transact UDFs have some limitations not present in other database engines (_such as Oracle and
Teradata_). These limitations helps the translations by narrowing the failure scope. This means,
there are specific scenarios we can expect to avoid.

Here are some of the limitations SQL Server has on UDFs

- UDFs cannot be used to perform actions that modify the database state
- User-defined functions cannot contain an OUTPUT INTO clause that has a table as its target
- User-defined functions cannot return multiple result sets. Use a stored procedure if you need to
  return multiple result sets.

For the full list, please check this link
[Create User-defined Functions (Database engine)](https://docs.microsoft.com/en-us/sql/relational-databases/user-defined-functions/create-user-defined-functions-database-engine)

[scalar.md](#scalar)

[inline-table-valued.md](#inline-table-valued)

## INLINE TABLE-VALUED

Translation reference to convert Transact-SQL UDF (User Defined Functions) with TABLE return type to
Snowflake.

Applies to

- SQL Server
- Azure Synapse Analytics

### Description 2

#### Note

Some parts in the output code are omitted for clarity reasons.

> Inline Table-Valued functions are table expression that can accept parameters, perform a SELECT
> statement and return a TABLE
> ([SQL Server Language Reference Creating an inline table-valued function](https://docs.microsoft.com/en-us/sql/t-sql/statements/create-function-transact-sql?view=sql-server-ver15#b-creating-an-inline-table-valued-function)).

#### Transact Syntax

```sql
 -- Transact-SQL Inline Table-Valued Function Syntax
CREATE [ OR ALTER ] FUNCTION [ schema_name. ] function_name
( [ { @parameter_name [ AS ] [ type_schema_name. ] parameter_data_type
    [ = default ] [ READONLY ] }
    [ ,...n ]
  ]
)
RETURNS TABLE
    [ WITH `<function_option>` [ ,...n ] ]
    [ AS ]
    RETURN [ ( ] select_stmt [ ) ]
[ ; ]
```

#### Snowflake SQL Syntax

```sql
CREATE OR REPLACE FUNCTION `<name>` ( [ `<arguments>` ] )
  RETURNS TABLE ( `<output_col_name>` `<output_col_type>` [, `<output_col_name>` `<output_col_type>` ... ] )
  AS '`<sql_expression>`'sql
```

### Sample Source Patterns

The following section describes all the possible source code patterns that can appear in this kind
of `CREATE FUNCTION` syntax.

For Inline Table-Valued functions, there can only exist one statement per body that could be:

- `SELECT` Statement
- `WITH` Common Table Expression

#### Select and return values directly from one table

This is the simplest scenario, performing a simple select from a table and returning those values

##### Transact-SQL

##### Inline Table-Valued 2

```sql
CREATE FUNCTION GetDepartmentInfo()
RETURNS TABLE
AS
RETURN
(
  SELECT DepartmentID, Name, GroupName
  FROM HumanResources.Department
);

GO

SELECT * from GetDepartmentInfo()
```

##### Result

<!-- prettier-ignore -->
|DepartmentID|Name|GroupName|
|---|---|---|
|1|Engineering|Research and Development|
|2|Tool Design|Research and Development|
|3|Sales|Sales and Marketing|
|4|Marketing|Sales and Marketing|
|5|Purchasing|Inventory Management|
|6|Research and Development|Research and Development|
|7|Production|Manufacturing|
|8|Production Control|Manufacturing|
|9|Human Resources|Executive General and Administration|
|10|Finance|Executive General and Administration|
|11|Information Services|Executive General and Administration|
|12|Document Control|Quality Assurance|
|13|Quality Assurance|Quality Assurance|
|14|Facilities and Maintenance|Executive General and Administration|
|15|Shipping and Receiving|Inventory Management|
|16|Executive|Executive General and Administration|

##### Snowflake SQL

##### Inline Table-Valued 3

```sql
CREATE OR REPLACE FUNCTION GetDepartmentInfo ()
RETURNS TABLE(
  DepartmentID STRING /*** SSC-FDM-TS0012 - INFORMATION FOR THE COLUMN DepartmentID WAS NOT FOUND. STRING DATATYPE USED TO MATCH CAST AS STRING OPERATION ***/,
  Name STRING /*** SSC-FDM-TS0012 - INFORMATION FOR THE COLUMN Name WAS NOT FOUND. STRING DATATYPE USED TO MATCH CAST AS STRING OPERATION ***/,
  GroupName STRING /*** SSC-FDM-TS0012 - INFORMATION FOR THE COLUMN GroupName WAS NOT FOUND. STRING DATATYPE USED TO MATCH CAST AS STRING OPERATION ***/
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
AS
$$
    SELECT
    CAST(DepartmentID AS STRING),
    CAST(Name AS STRING),
    CAST(GroupName AS STRING)
    FROM
    HumanResources.Department
$$;

SELECT
    *
from
    TABLE(GetDepartmentInfo());
```

##### Result 2

<!-- prettier-ignore -->
|DepartmentID|Name|GroupName|
|---|---|---|
|1|Engineering|Research and Development|
|2|Tool Design|Research and Development|
|3|Sales|Sales and Marketing|
|4|Marketing|Sales and Marketing|
|5|Purchasing|Inventory Management|
|6|Research and Development|Research and Development|
|7|Production|Manufacturing|
|8|Production Control|Manufacturing|
|9|Human Resources|Executive General and Administration|
|10|Finance|Executive General and Administration|
|11|Information Services|Executive General and Administration|
|12|Document Control|Quality Assurance|
|13|Quality Assurance|Quality Assurance|
|14|Facilities and Maintenance|Executive General and Administration|
|15|Shipping and Receiving|Inventory Management|
|16|Executive|Executive General and Administration|

#### Select and return values from multiple tables renaming columns and using built in functions

This is an example of a query using built-in functions in a select statement getting data from
different tables, renaming columns and returning a table.

##### Transact-SQL 2

##### Inline Table-Valued 4

```sql
CREATE FUNCTION GetPersonBasicInfo()
RETURNS TABLE
AS
RETURN
(
 SELECT TOP (20)
      P.PersonType,
      P.FirstName,
      E.JobTitle,
   E.Gender,
      YEAR(E.HireDate) as HIREYEAR
  FROM
      Person.Person P
  INNER JOIN
      HumanResources.Employee E
  ON
      P.BusinessEntityID = E.BusinessEntityID
);

GO

SELECT * FROM GetPersonBasicInfo();
```

##### Result 3

<!-- prettier-ignore -->
|PersonType|FirstName|JobTitle|Gender|HIREYEAR|
|---|---|---|---|---|
|EM|Ken|Chief Executive Officer|M|2009|
|EM|Terri|Vice President of Engineering|F|2008|
|EM|Roberto|Engineering Manager|M|2007|
|EM|Rob|Senior Tool Designer|M|2007|
|EM|Gail|Design Engineer|F|2008|
|EM|Jossef|Design Engineer|M|2008|
|EM|Dylan|Research and Development Manager|M|2009|
|EM|Diane|Research and Development Engineer|F|2008|
|EM|Gigi|Research and Development Engineer|F|2009|
|EM|Michael|Research and Development Manager|M|2009|
|EM|Ovidiu|Senior Tool Designer|M|2010|
|EM|Thierry|Tool Designer|M|2007|
|EM|Janice|Tool Designer|F|2010|
|EM|Michael|Senior Design Engineer|M|2010|
|EM|Sharon|Design Engineer|F|2011|
|EM|David|Marketing Manager|M|2007|
|EM|Kevin|Marketing Assistant|M|2007|
|EM|John|Marketing Specialist|M|2011|
|EM|Mary|Marketing Assistant|F|2011|
|EM|Wanida|Marketing Assistant|F|2011|

##### Snowflake SQL 2

##### Inline Table-Valued 5

```sql
CREATE OR REPLACE FUNCTION GetPersonBasicInfo ()
RETURNS TABLE(
 PersonType STRING /*** SSC-FDM-TS0012 - INFORMATION FOR THE COLUMN PersonType WAS NOT FOUND. STRING DATATYPE USED TO MATCH CAST AS STRING OPERATION ***/,
 FirstName STRING /*** SSC-FDM-TS0012 - INFORMATION FOR THE COLUMN FirstName WAS NOT FOUND. STRING DATATYPE USED TO MATCH CAST AS STRING OPERATION ***/,
 JobTitle STRING /*** SSC-FDM-TS0012 - INFORMATION FOR THE COLUMN JobTitle WAS NOT FOUND. STRING DATATYPE USED TO MATCH CAST AS STRING OPERATION ***/,
 Gender STRING /*** SSC-FDM-TS0012 - INFORMATION FOR THE COLUMN Gender WAS NOT FOUND. STRING DATATYPE USED TO MATCH CAST AS STRING OPERATION ***/,
 HIREYEAR INTEGER
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
AS
$$
  SELECT
  TOP 20
  CAST(P.PersonType AS STRING),
  CAST(P.FirstName AS STRING),
  CAST(E.JobTitle AS STRING),
  CAST(E.Gender AS STRING),
  YEAR(E.HireDate :: TIMESTAMP) as HIREYEAR
   FROM
  Person.Person P
   INNER JOIN
   HumanResources.Employee E
   ON P.BusinessEntityID = E.BusinessEntityID
$$;

SELECT
  *
FROM
  TABLE(GetPersonBasicInfo());
```

##### Result 4

<!-- prettier-ignore -->
|PersonType|FirstName|JobTitle|Gender|HIREYEAR|
|---|---|---|---|---|
|EM|Ken|Chief Executive Officer|M|2009|
|EM|Terri|Vice President of Engineering|F|2008|
|EM|Roberto|Engineering Manager|M|2007|
|EM|Rob|Senior Tool Designer|M|2007|
|EM|Gail|Design Engineer|F|2008|
|EM|Jossef|Design Engineer|M|2008|
|EM|Dylan|Research and Development Manager|M|2009|
|EM|Diane|Research and Development Engineer|F|2008|
|EM|Gigi|Research and Development Engineer|F|2009|
|EM|Michael|Research and Development Manager|M|2009|
|EM|Ovidiu|Senior Tool Designer|M|2010|
|EM|Thierry|Tool Designer|M|2007|
|EM|Janice|Tool Designer|F|2010|
|EM|Michael|Senior Design Engineer|M|2010|
|EM|Sharon|Design Engineer|F|2011|
|EM|David|Marketing Manager|M|2007|
|EM|Kevin|Marketing Assistant|M|2007|
|EM|John|Marketing Specialist|M|2011|
|EM|Mary|Marketing Assistant|F|2011|
|EM|Wanida|Marketing Assistant|F|2011|

#### Select columns using WITH statement

The body of an inline table-valued function can also be specified using a WITH statement as shown
below.

##### Transact-SQL 3

##### Inline Table-Valued 6

```sql
CREATE FUNCTION GetMaritalStatusByGender
(
 @P_Gender nchar(1)
)

RETURNS TABLE
AS
RETURN
(
  WITH CTE AS
 (
  SELECT BusinessEntityID, MaritalStatus, Gender
  FROM HumanResources.Employee
  where Gender = @P_Gender
 )
  SELECT
 MaritalStatus, Gender, CONCAT(P.FirstName,' ', P.LastName) as Name
  FROM
 CTE INNER JOIN Person.Person P
  ON
 CTE.BusinessEntityID = P.BusinessEntityID
);

GO

select * from GetMaritalStatusByGender('F');
```

##### Result 5

<!-- prettier-ignore -->
|MaritalStatus|Gender|Name|
|---|---|---|
|S|F|Terri Duffy|
|M|F|Gail Erickson|
|S|F|Diane Margheim|
|M|F|Gigi Matthew|
|M|F|Janice Galvin|
|M|F|Sharon Salavaria|
|S|F|Mary Dempsey|
|M|F|Wanida Benshoof|
|M|F|Mary Gibson|
|M|F|Jill Williams|
|S|F|Jo Brown|
|M|F|Britta Simon|
|M|F|Margie Shoop|
|M|F|Rebecca Laszlo|
|M|F|Suchitra Mohan|
|M|F|Kim Abercrombie|
|S|F|JoLynn Dobney|
|M|F|Nancy Anderson|
|M|F|Ruth Ellerbrock|
|M|F|Doris Hartwig|
|M|F|Diane Glimp|
|M|F|Bonnie Kearney|
|M|F|Denise Smith|
|S|F|Diane Tibbott|
|M|F|Carole Poland|
|M|F|Carol Philips|
|M|F|Merav Netz|
|S|F|Betsy Stadick|
|S|F|Danielle Tiedt|
|S|F|Kimberly Zimmerman|
|M|F|Elizabeth Keyser|
|M|F|Mary Baker|
|M|F|Alice Ciccu|
|M|F|Linda Moschell|
|S|F|Angela Barbariol|
|S|F|Kitti Lertpiriyasuwat|
|S|F|Susan Eaton|
|S|F|Kim Ralls|
|M|F|Nicole Holliday|
|S|F|Anibal Sousa|
|M|F|Samantha Smith|
|S|F|Olinda Turner|
|S|F|Cynthia Randall|
|M|F|Sandra Reátegui Alayo|
|S|F|Linda Randall|
|S|F|Shelley Dyck|
|S|F|Laura Steele|
|S|F|Susan Metters|
|S|F|Katie McAskill-White|
|M|F|Barbara Decker|
|M|F|Yvonne McKay|
|S|F|Janeth Esteves|
|M|F|Brenda Diaz|
|M|F|Lorraine Nay|
|M|F|Paula Nartker|
|S|F|Lori Kane|
|M|F|Kathie Flood|
|S|F|Belinda Newman|
|M|F|Karen Berge|
|M|F|Lori Penor|
|M|F|Jo Berry|
|M|F|Laura Norman|
|M|F|Paula Barreto de Mattos|
|M|F|Mindy Martin|
|M|F|Deborah Poe|
|S|F|Candy Spoon|
|M|F|Barbara Moreland|
|M|F|Janet Sheperdigian|
|S|F|Wendy Kahn|
|S|F|Sheela Word|
|M|F|Linda Meisner|
|S|F|Erin Hagens|
|M|F|Annette Hill|
|S|F|Jean Trenary|
|S|F|Stephanie Conroy|
|S|F|Karen Berg|
|M|F|Janaina Bueno|
|M|F|Linda Mitchell|
|S|F|Jillian Carson|
|S|F|Pamela Ansman-Wolfe|
|S|F|Lynn Tsoflias|
|M|F|Amy Alberts|
|S|F|Rachel Valdez|
|M|F|Jae Pak|

##### Snowflake SQL 3

##### Inline Table-Valued 7

```sql
 --** SSC-FDM-0007 - MISSING DEPENDENT OBJECTS "HumanResources.Employee", "Person.Person" **
CREATE OR REPLACE FUNCTION GetMaritalStatusByGender
(P_GENDER STRING
)
RETURNS TABLE(
 MaritalStatus STRING /*** SSC-FDM-TS0012 - INFORMATION FOR THE COLUMN MaritalStatus WAS NOT FOUND. STRING DATATYPE USED TO MATCH CAST AS STRING OPERATION ***/,
 Gender STRING /*** SSC-FDM-TS0012 - INFORMATION FOR THE COLUMN Gender WAS NOT FOUND. STRING DATATYPE USED TO MATCH CAST AS STRING OPERATION ***/,
 Name VARCHAR
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
AS
$$
 --** SSC-PRF-TS0001 - PERFORMANCE WARNING - RECURSION FOR CTE NOT CHECKED. MIGHT REQUIRE RECURSIVE KEYWORD **
  WITH CTE AS
 (
  SELECT
   BusinessEntityID,
   MaritalStatus,
   Gender
  FROM
   HumanResources.Employee
  where
   Gender = :P_GENDER
 )
  SELECT
  CAST(MaritalStatus AS STRING),
  CAST(Gender AS STRING),
  CONCAT(P.FirstName,' ', P.LastName) as Name
  FROM
  CTE
  INNER JOIN
   Person.Person P
  ON CTE.BusinessEntityID = P.BusinessEntityID
$$;

select
  *
from
  TABLE(GetMaritalStatusByGender('F'));
```

##### Result 6

<!-- prettier-ignore -->
|MaritalStatus|Gender|Name|
|---|---|---|
|S|F|Terri Duffy|
|M|F|Gail Erickson|
|S|F|Diane Margheim|
|M|F|Gigi Matthew|
|M|F|Janice Galvin|
|M|F|Sharon Salavaria|
|S|F|Mary Dempsey|
|M|F|Wanida Benshoof|
|M|F|Mary Gibson|
|M|F|Jill Williams|
|S|F|Jo Brown|
|M|F|Britta Simon|
|M|F|Margie Shoop|
|M|F|Rebecca Laszlo|
|M|F|Suchitra Mohan|
|M|F|Kim Abercrombie|
|S|F|JoLynn Dobney|
|M|F|Nancy Anderson|
|M|F|Ruth Ellerbrock|
|M|F|Doris Hartwig|
|M|F|Diane Glimp|
|M|F|Bonnie Kearney|
|M|F|Denise Smith|
|S|F|Diane Tibbott|
|M|F|Carole Poland|
|M|F|Carol Philips|
|M|F|Merav Netz|
|S|F|Betsy Stadick|
|S|F|Danielle Tiedt|
|S|F|Kimberly Zimmerman|
|M|F|Elizabeth Keyser|
|M|F|Mary Baker|
|M|F|Alice Ciccu|
|M|F|Linda Moschell|
|S|F|Angela Barbariol|
|S|F|Kitti Lertpiriyasuwat|
|S|F|Susan Eaton|
|S|F|Kim Ralls|
|M|F|Nicole Holliday|
|S|F|Anibal Sousa|
|M|F|Samantha Smith|
|S|F|Olinda Turner|
|S|F|Cynthia Randall|
|M|F|Sandra Reátegui Alayo|
|S|F|Linda Randall|
|S|F|Shelley Dyck|
|S|F|Laura Steele|
|S|F|Susan Metters|
|S|F|Katie McAskill-White|
|M|F|Barbara Decker|
|M|F|Yvonne McKay|
|S|F|Janeth Esteves|
|M|F|Brenda Diaz|
|M|F|Lorraine Nay|
|M|F|Paula Nartker|
|S|F|Lori Kane|
|M|F|Kathie Flood|
|S|F|Belinda Newman|
|M|F|Karen Berge|
|M|F|Lori Penor|
|M|F|Jo Berry|
|M|F|Laura Norman|
|M|F|Paula Barreto de Mattos|
|M|F|Mindy Martin|
|M|F|Deborah Poe|
|S|F|Candy Spoon|
|M|F|Barbara Moreland|
|M|F|Janet Sheperdigian|
|S|F|Wendy Kahn|
|S|F|Sheela Word|
|M|F|Linda Meisner|
|S|F|Erin Hagens|
|M|F|Annette Hill|
|S|F|Jean Trenary|
|S|F|Stephanie Conroy|
|S|F|Karen Berg|
|M|F|Janaina Bueno|
|M|F|Linda Mitchell|
|S|F|Jillian Carson|
|S|F|Pamela Ansman-Wolfe|
|S|F|Lynn Tsoflias|
|M|F|Amy Alberts|
|S|F|Rachel Valdez|
|M|F|Jae Pak|

### Known issues

No issues were found

### Related EWIs

1. [SSC-FDM-TS0012](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/sqlServerFDM#ssc-fdm-ts0012):
   Information for the expression was not found. CAST to STRING used
2. [SSC-PRF-TS0001](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/performance-review/sqlServerPRF#ssc-prf-ts0001):
   Performance warning - recursion for CTE not checked. Might require a recursive keyword.
3. [SSC-EWI-0073](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0073):
   Pending Functional Equivalence Review

## MULTI-STATEMENT TABLE-VALUED

Translation reference to convert Transact-SQL UDF (User Defined Functions) with TABLE return type to
Snowflake.

Applies to

- SQL Server
- Azure Synapse Analytics

### Note 2

Some parts in the output code are omitted for clarity reasons.

### Note 3

All the code samples on this page have not been implemented yet in SnowConvert AI. They should be
interpreted as a reference for how each scenario should be translated to Snowflake. These
translations may change in the future.Some parts in the output code are omitted for clarity reasons.

### Description 3

Multi-statement table-valued is similar to Inline-statement table-valued
([INLINE TABLE-VALUED](#inline-table-valued)). However Multi-statement table-valued may have more
than one statement in its function body, the table columns are specified in the return type and it
has a BEGIN/END block
([SQL Server Language Reference Creating a multi-statement table-valued function](https://docs.microsoft.com/en-us/sql/t-sql/statements/create-function-transact-sql?view=sql-server-ver15#c-creating-a-multi-statement-table-valued-function)

#### Transact-SQL Syntax

```sql
CREATE [ OR ALTER ] FUNCTION [ schema_name. ] function_name
( [ { @parameter_name [ AS ] [ type_schema_name. ] parameter_data_type
    [ = default ] [READONLY] }
    [ ,...n ]
  ]
)
RETURNS @return_variable TABLE `<table_type_definition>`
    [ WITH `<function_option>` [ ,...n ] ]
    [ AS ]
    BEGIN
        function_body
        RETURN
    END
[ ; ]
```

#### Snowflake SQL 4

```sql
CREATE OR REPLACE FUNCTION `<name>` ( [ `<arguments>` ] )
  RETURNS TABLE ( `<output_col_name>` `<output_col_type>` [, `<output_col_name>` `<output_col_type>` ... ] )
  AS '`<sql_expression>`'
```

### Sample Source Patterns 2

The following section describes all the possible source code patterns that can appear in this kind
ofCREATE FUNCTION syntax.

The function body of Multi-Statement Table-Valued function must be a SELECT statement. For this
reason the others statements must be called separately.

#### **Insert values in a table**

Inserts one or more rows into the table and returns the table with the new values

##### Transact-SQL 4

##### MULTI-STATEMENT TABLE-VALUED 2

```sql
CREATE OR ALTER FUNCTION calc_behavioral_segment()
RETURNS @behavioral_segments TABLE (behavioral_segment VARCHAR(50))
AS
BEGIN
 DECLARE @col varchar(15)
 SET @col = 'Unknown'
 INSERT INTO @behavioral_segments
 SELECT @col

 RETURN
END

SELECT * FROM calc_behavioral_segment();
```

##### Result 7

<!-- prettier-ignore -->
|BEHAVIORAL_SEGMENT|
|---|
|Unknown|

##### Snowflake SQL 5

##### MULTI-STATEMENT TABLE-VALUED 3

```sql
!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'TABLE VALUED FUNCTIONS' NODE ***/!!!
CREATE OR ALTER FUNCTION calc_behavioral_segment ()
RETURNS BEHAVIORAL_SEGMENTS TABLE (
 behavioral_segment VARCHAR(50))
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
AS
BEGIN
 DECLARE @col varchar(15)
 SET @col = 'Unknown'
 INSERT INTO @behavioral_segments
 SELECT @col

 RETURN
END

SELECT * FROM calc_behavioral_segment();;
```

##### Results

<!-- prettier-ignore -->
|BEHAVIORAL_SEGMENT|
|---|
|Unknown|

#### Insert value according to if/else statement

Inserts a row into the table according to the condition and returns the table with the new value

##### Transact-SQL 5

##### MULTI-STATEMENT TABLE-VALUED 4

```sql
CREATE OR ALTER FUNCTION odd_or_even_number(@number INT)
RETURNS @numbers TABLE (number_type VARCHAR(15))
AS
BEGIN
 IF ((@number % 2) = 0)
 BEGIN
  INSERT @numbers SELECT 'Even'
 END

 ELSE
 BEGIN
  INSERT @numbers SELECT 'Odd'
 END

 RETURN
END

SELECT * FROM odd_or_even_number(9);
```

##### Result 8

<!-- prettier-ignore -->
|NUMBER_TYPE|
|---|
|Odd|

##### Snowflake SQL 6

##### MULTI-STATEMENT TABLE-VALUED 5

```sql
!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'TABLE VALUED FUNCTIONS' NODE ***/!!!
CREATE OR ALTER FUNCTION odd_or_even_number (NUMBER INT)
RETURNS NUMBERS TABLE (
 number_type VARCHAR(15))
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
AS
BEGIN
 IF ((@number % 2) = 0)
 BEGIN
  INSERT @numbers SELECT 'Even'
 END

 ELSE
 BEGIN
  INSERT @numbers SELECT 'Odd'
 END

 RETURN
END

SELECT * FROM odd_or_even_number(9);;
```

##### Result 9

<!-- prettier-ignore -->
|NUMBER_TYPE|
|---|
|Odd|

#### Inserts multiple according to if/else statement

The example below inserts more than one value into the table and more than one variable is modified
according to the condition. Returns the table with the new values

##### Transact-SQL 6

##### MULTI-STATEMENT TABLE-VALUED 6

```sql
CREATE OR ALTER FUNCTION new_employee_hired(@id VARCHAR (50), @position VARCHAR(50), @experience VARCHAR(15))
RETURNS @new_employee TABLE (id_employee VARCHAR (50), working_from_home BIT, team VARCHAR(15), computer VARCHAR(15))
AS
BEGIN
 DECLARE @wfh BIT
 DECLARE @team VARCHAR(15)
 DECLARE @computer VARCHAR(15)

 IF @position = 'DEVELOPER'
 BEGIN
  SET @team = 'TEAM_1'
  SET @computer = 'LAPTOP'
 END

 IF @position = 'IT'
 BEGIN
  SET @team = 'TEAM_2'
  SET @computer = 'DESKTOP'
 END

 IF @experience = 'JUNIOR'
 BEGIN
  SET @wfh = '0'
 END
 IF @experience = 'SENIOR'
 BEGIN
  SET @wfh = '1'
 END

 INSERT INTO @new_employee VALUES (@id, @wfh, @team, @computer)
 RETURN
END

SELECT * FROM new_employee_hired('123456789', 'DEVELOPER', 'SENIOR');
```

##### Result 10

<!-- prettier-ignore -->
|ID_EMPLOYEE|WORKING_FROM_HOME|TEAM|COMPUTER|
|---|---|---|---|
|123456789|1|TEAM_1|LAPTOP|

##### Snowflake

##### MULTI-STATEMENT TABLE-VALUED 7

```sql
 !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'TABLE VALUED FUNCTIONS' NODE ***/!!!
CREATE OR ALTER FUNCTION new_employee_hired (ID STRING, POSITION STRING, EXPERIENCE STRING)
RETURNS NEW_EMPLOYEE TABLE (
 id_employee VARCHAR(50),
 working_from_home BOOLEAN,
 team VARCHAR(15),
 computer VARCHAR(15))
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
AS
BEGIN
 DECLARE @wfh BIT
 DECLARE @team VARCHAR(15)
 DECLARE @computer VARCHAR(15)

 IF @position = 'DEVELOPER'
 BEGIN
  SET @team = 'TEAM_1'
  SET @computer = 'LAPTOP'
 END

 IF @position = 'IT'
 BEGIN
  SET @team = 'TEAM_2'
  SET @computer = 'DESKTOP'
 END

 IF @experience = 'JUNIOR'
 BEGIN
  SET @wfh = '0'
 END
 IF @experience = 'SENIOR'
 BEGIN
  SET @wfh = '1'
 END

 INSERT INTO @new_employee VALUES (@id, @wfh, @team, @computer)
 RETURN
END

SELECT * FROM new_employee_hired('123456789', 'DEVELOPER', 'SENIOR');;
```

##### Result 11

<!-- prettier-ignore -->
|ID_EMPLOYEE|WORKING_FROM_HOME|TEAM|COMPUTER|
|---|---|---|---|
|123456789|1|TEAM_1|LAPTOP|

Warning

In case there are nested if statements and more than one variables are modified in the statements it
is necessary to use a stored procedure.

#### Update values previously inserted

Updates columns values of the table into the function body and returns it with the new values.

##### Transact-SQL 7

##### MULTI-STATEMENT TABLE-VALUED 8

```sql
CREATE OR ALTER FUNCTION get_employees_history()
RETURNS @employee_history TABLE (
 department_name NVARCHAR(50),
 first_name NVARCHAR(50),
 last_name NVARCHAR(50),
 start_date DATE,
 end_date DATE,
 job_title NVARCHAR(50),
 months_working INT
)
BEGIN
 INSERT INTO @employee_history
 SELECT D.name AS department_name, P.first_name, P.last_name, EH.start_date, EH.end_date, E.job_title, 0 FROM Department D
 LEFT OUTER JOIN employee_department_history EH
  ON D.department_ID = EH.department_ID
 INNER JOIN  Employee E
  ON E.business_entity_ID = EH.business_entity_ID
 INNER JOIN Person P
  ON P.business_entity_ID = E.business_entity_ID

 UPDATE @employee_history
 SET
  months_working =
  CASE WHEN end_date IS NULL THEN DATEDIFF(MONTH, start_date, GETDATE())
  ELSE DATEDIFF(MONTH, start_date, end_date)
 END
 RETURN;
END;

SELECT TOP(10) * FROM get_employees_history();
```

##### Result 12

<!-- prettier-ignore -->
|DEPARTMENT_NAME|FIRST_NAME|LAST_NAME|START_DATE|END_DATE|JOB_TITLE|MONTHS_WORKING|
|---|---|---|---|---|---|---|
|Sales|Syed|Abbas|2013-03-14|NULL|Pacific Sales Manager|106|
|Production|Kim|Abercrombie|2010-01-16|NULL|Production Technician - WC60|144|
|Quality Assurance|Hazem|Abolrous|2009-02-28|NULL|Quality Assurance Manager|155|
|Shipping and Receiving|Pilar|Ackerman|2009-01-02|NULL|Shipping and Receiving Supervisor|156|
|Production|Jay|Adams|2009-03-05|NULL|Production Technician - WC60|154|
|Information Services|François|Ajenstat|2009-01-17|NULL|Database Administrator|156|
|Sales|Amy|Alberts|2012-04-16|NULL|European Sales Manager|117|
|Production|Greg|Alderson|2008-12-02|NULL|Production Technician - WC45|157|
|Quality Assurance|Sean|Alexander|2008-12-28|NULL|Quality Assurance Technician|157|
|Facilities and Maintenance|Gary|Altman|2009-12-02|NULL|Facilities Manager|145|

##### Snowflake SQL 7

##### MULTI-STATEMENT TABLE-VALUED 9

```sql
!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'TABLE VALUED FUNCTIONS' NODE ***/!!!
CREATE OR ALTER FUNCTION get_employees_history ()
RETURNS EMPLOYEE_HISTORY TABLE (
 department_name VARCHAR(50),
 first_name VARCHAR(50),
 last_name VARCHAR(50),
 start_date DATE,
 end_date DATE,
 job_title VARCHAR(50),
 months_working INT
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
BEGIN
 INSERT INTO @employee_history
 SELECT D.name AS department_name, P.first_name, P.last_name, EH.start_date, EH.end_date, E.job_title, 0 FROM Department D
 LEFT OUTER JOIN employee_department_history EH
  ON D.department_ID = EH.department_ID
 INNER JOIN  Employee E
  ON E.business_entity_ID = EH.business_entity_ID
 INNER JOIN Person P
  ON P.business_entity_ID = E.business_entity_ID

 UPDATE @employee_history
 SET
  months_working =
  CASE WHEN end_date IS NULL THEN DATEDIFF(MONTH, start_date, GETDATE())
  ELSE DATEDIFF(MONTH, start_date, end_date)
 END
 RETURN;
END;

SELECT TOP(10) * FROM get_employees_history();;
```

##### Result 13

<!-- prettier-ignore -->
|DEPARTMENT_NAME|FIRST_NAME|LAST_NAME|START_DATE|END_DATE|JOB_TITLE|MONTHS_WORKING|
|---|---|---|---|---|---|---|
|Sales|Syed|Abbas|2013-03-14|NULL|Pacific Sales Manager|106|
|Production|Kim|Abercrombie|2010-01-16|NULL|Production Technician - WC60|144|
|Quality Assurance|Hazem|Abolrous|2009-02-28|NULL|Quality Assurance Manager|155|
|Shipping and Receiving|Pilar|Ackerman|2009-01-02|NULL|Shipping and Receiving Supervisor|156|
|Production|Jay|Adams|2009-03-05|NULL|Production Technician - WC60|154|
|Information Services|François|Ajenstat|2009-01-17|NULL|Database Administrator|156|
|Sales|Amy|Alberts|2012-04-16|NULL|European Sales Manager|117|
|Production|Greg|Alderson|2008-12-02|NULL|Production Technician - WC45|157|
|Quality Assurance|Sean|Alexander|2008-12-28|NULL|Quality Assurance Technician|157|
|Facilities and Maintenance|Gary|Altman|2009-12-02|NULL|Facilities Manager|145|

#### Multiple return clauses

In the following sample there is more than one return clause, this is because depending on the
situation it is not necessary to keep executing the whole function.

##### Transact-SQL 8

##### MULTI-STATEMENT TABLE-VALUED 10

```sql
CREATE OR ALTER FUNCTIONcreate_new_team(@team_name VARCHAR(50))
</strong>RETURNS @new_team TABLE (type VARCHAR(50), name VARCHAR(50))
AS
BEGIN
 DECLARE @employees INT
 SET @employees = (SELECT count(*) FROM employee)
 DECLARE @type VARCHAR(15)
 SET @type = 'small_team'
 IF (@employees &#x3C; 8)
 BEGIN
  INSERT @new_team VALUES (@type, @team_name)
  RETURN
 END

 SET @type = 'big_team'
 INSERT @new_team VALUES (@type, @team_name)

 RETURN
END

SELECT * FROMcreate_new_team('Team1');
```

##### Result 14

<!-- prettier-ignore -->
|TYPE|NAME|
|---|---|
|SMALL_TEAM|TEAM1|

##### Snowflake SQL 8

##### MULTI-STATEMENT TABLE-VALUED 11

```sql
!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'TABLE VALUED FUNCTIONS' NODE ***/!!!
CREATE OR ALTER FUNCTIONcreate_new_team (TEAM_NAME STRING)
RETURNS NEW_TEAM TABLE (
 type VARCHAR(50),
 name VARCHAR(50))
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
AS
BEGIN
 DECLARE @employees INT
 SET @employees = (SELECT count(*) FROM employee)
 DECLARE @type VARCHAR(15)
 SET @type = 'small_team'
 IF (@employees < 8)
 BEGIN
  INSERT @new_team VALUES (@type, @team_name)
  RETURN
 END

 SET @type = 'big_team'
 INSERT @new_team VALUES (@type, @team_name)

 RETURN
END

SELECT * FROMcreate_new_team('Team1');;
```

##### Result 15

<!-- prettier-ignore -->
|TYPE|NAME|
|---|---|
|SMALL_TEAM|TEAM1|

Warning

This transformation is applied when there is only one value to insert, if there is more than one
value it is necessary to use a stored procedure.

#### Complex cases

The example is a complex case that uses nested `if` statements and inserts a value depending on the
true condition.

##### Transact-SQL 9

##### MULTI-STATEMENT TABLE-VALUED 12

```sql
CREATE OR ALTER FUNCTION vacation_status(@id VARCHAR (50))
RETURNS @status TABLE (vacation_status VARCHAR(30))
AS
BEGIN
 DECLARE @hire_date DATETIME
 SET @hire_date = (SELECT @hire_date FROM employee WHERE employeeId = @id)
 DECLARE @vacation_hours INT
 SET @vacation_hours = (SELECT count(vacation_hours) FROM employee WHERE employeeId = @id)
 DECLARE @time_working INT
 SET @time_working = (SELECT DATEDIFF(MONTH, @hire_date,GETDATE()))

 IF (@vacation_hours > 0)
 BEGIN
  IF (@time_working > 3)
  BEGIN
   IF (@vacation_hours < 120)
   BEGIN
    INSERT INTO @status VALUES ('Ok')
   END

   IF (@vacation_hours = 120)
   BEGIN
    INSERT INTO @status values ('In the limit')
   END

   IF (@vacation_hours > 120)
   BEGIN
    INSERT INTO @status VALUES ('With excess')
   END
  END
  ELSE
  BEGIN
   INSERT INTO @status values ('Hired recently')
  END
 END
 ELSE
 BEGIN
  INSERT INTO @status values ('No hours')
 END
 RETURN
END

SELECT * FROM vacation_status('adventure-worksken0')
```

##### Result 16

<!-- prettier-ignore -->
|VACATION_STATUS|
|---|
|OK|

##### Snowflake SQL 9

##### MULTI-STATEMENT TABLE-VALUED 13

```sql
 !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'TABLE VALUED FUNCTIONS' NODE ***/!!!
CREATE OR ALTER FUNCTION vacation_status (ID STRING)
RETURNS STATUS TABLE (
 vacation_status VARCHAR(30))
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
AS
BEGIN
 DECLARE @hire_date DATETIME
 SET @hire_date = (SELECT @hire_date FROM employee WHERE employeeId = @id)
 DECLARE @vacation_hours INT
 SET @vacation_hours = (SELECT count(vacation_hours) FROM employee WHERE employeeId = @id)
 DECLARE @time_working INT
 SET @time_working = (SELECT DATEDIFF(MONTH, @hire_date,GETDATE()))

 IF (@vacation_hours > 0)
 BEGIN
  IF (@time_working > 3)
  BEGIN
   IF (@vacation_hours < 120)
   BEGIN
    INSERT INTO @status VALUES ('Ok')
   END

   IF (@vacation_hours = 120)
   BEGIN
    INSERT INTO @status values ('In the limit')
   END

   IF (@vacation_hours > 120)
   BEGIN
    INSERT INTO @status VALUES ('With excess')
   END
  END
  ELSE
  BEGIN
   INSERT INTO @status values ('Hired recently')
  END
 END
 ELSE
 BEGIN
  INSERT INTO @status values ('No hours')
 END
 RETURN
END

SELECT * FROM vacation_status('adventure-worksken0');
```

##### Second Tab

<!-- prettier-ignore -->
|VACATION_STATUS|
|---|
|OK|

### Known Issues 2

#### While statements along side queries

The problem with this example is that there’s no way of transforming the while statement to a CTE
inside the `WITH` clause of the main select, this forces us to transform this statement to store
procedure to maintain the same logic.

##### Transact-SQL 10

##### MULTI-STATEMENT TABLE-VALUED 14

```sql
--Additional Params: -t JavaScript
CREATE OR ALTER FUNCTION get_group_name
(@department_id INT)
RETURNS @group_names TABLE (group_name VARCHAR(15))
AS
BEGIN
DECLARE @name VARCHAR(30) = 'Another Department'
WHILE @name = 'Another Department'
BEGIN
 IF (@department_id &#x3C; 3)
 BEGIN
  SET @name = 'engineering'
 END

 IF @department_id = 3
 BEGIN
  SET @name = 'Tool Design'
 END

 SELECT @department_id = @department_id / 3
END
INSERT @group_names SELECT @name
RETURN
END

SELECT * FROM get_group_name(9);
```

##### Result 17

<!-- prettier-ignore -->
|GROUP_NAME|
|---|
|Tool Design|

##### Snowflake SQL 10

##### MULTI-STATEMENT TABLE-VALUED 15

```sql
 !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'TABLE VALUED FUNCTIONS' NODE ***/!!!
CREATE OR ALTER FUNCTION get_group_name
(DEPARTMENT_ID INT)
RETURNS @group_names TABLE (
 group_name VARCHAR(15))
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
AS
BEGIN
DECLARE @name VARCHAR(30) = 'Another Department'
WHILE @name = 'Another Department'
BEGIN
 IF (@department_id < 3)
 BEGIN
  SET @name = 'engineering'
 END

 IF @department_id = 3
 BEGIN
  SET @name = 'Tool Design'
 END

 SELECT @department_id = @department_id / 3
END
INSERT @group_names SELECT @name
RETURN
END

SELECT * FROM get_group_name(9);;
```

##### Result 18

<!-- prettier-ignore -->
|GROUP_NAME|
|---|
|Tool Design|

#### Declare Cursor

User-defined functions cannot DECLARE, OPEN, FETCH, CLOSE or DEALLOCATE a `CURSOR`. Use a Stored
Procedure to work with cursors.

##### Transact-SQL 11

##### MULTI-STATEMENT TABLE-VALUED 16

```sql
 --Additional Params: -t JavaScript

CREATE OR ALTER FUNCTION amount_new_specimens(@id int)
RETURNS @new_specimens TABLE (amount int)
AS
BEGIN
 DECLARE @first_specimen VARCHAR(30) ;
 set @first_specimen = (select name_specimen from specimen where specimen_id = @id);
 DECLARE @second_specimen VARCHAR(30);

 DECLARE @specimens TABLE (name_specimen VARCHAR(30))

 DECLARE Cursor1 CURSOR
 FOR SELECT name_specimen
 FROM specimen

 OPEN cursor1
 FETCH NEXT FROM cursor1
 INTO @second_specimen;

 WHILE @@FETCH_STATUS = 0
 BEGIN
  IF @first_specimen <> @second_specimen
  BEGIN
   INSERT INTO @specimens values (CONCAT_WS('-', @first_specimen, @second_specimen))
  END
  FETCH NEXT FROM cursor1
  INTO @second_specimen;
 END

 CLOSE cursor1;
 DEALLOCATE cursor1;

 INSERT INTO @new_specimens SELECT COUNT(*) FROM @specimens
 RETURN
END

SELECT * FROM amount_new_specimens(1);
```

##### Result 19

<!-- prettier-ignore -->
|AMOUNT|
|---|
|3|

##### Snowflake SQL 11

##### MULTI-STATEMENT TABLE-VALUED 17

```sql
 --Additional Params: -t JavaScript
!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'TABLE VALUED FUNCTIONS' NODE ***/!!!

CREATE OR ALTER FUNCTION amount_new_specimens (ID INT)
RETURNS @new_specimens TABLE (
 amount INT
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
AS
BEGIN
 DECLARE @first_specimen VARCHAR(30) ;
 set @first_specimen = (select name_specimen from specimen where specimen_id = @id);
 DECLARE @second_specimen VARCHAR(30);

 DECLARE @specimens TABLE (name_specimen VARCHAR(30))

 DECLARE Cursor1 CURSOR
 FOR SELECT name_specimen
 FROM specimen

 OPEN cursor1
 FETCH NEXT FROM cursor1
 INTO @second_specimen;

 WHILE @@FETCH_STATUS = 0
 BEGIN
  IF @first_specimen <> @second_specimen
  BEGIN
   INSERT INTO @specimens values (CONCAT_WS('-', @first_specimen, @second_specimen))
  END
  FETCH NEXT FROM cursor1
  INTO @second_specimen;
 END

 CLOSE cursor1;
 DEALLOCATE cursor1;

 INSERT INTO @new_specimens SELECT COUNT(*) FROM @specimens
 RETURN
END

SELECT * FROM amount_new_specimens(1);;
```

##### Result 20

<!-- prettier-ignore -->
|AMOUNT|
|---|
|3|

#### Different statements are not supported in Common Tables Expressions

The clauses `UPDATE`, `INSERT`, `DELETE`, `ALTER` or `DROP` are not supported on the body of common
tables expressions, even after their declaration using a delimitator. For this reason, the function
can be modified to work as a stored procedure.

##### Transact-SQL 12

##### MULTI-STATEMENT TABLE-VALUED 18

```sql
 --Additional Params: -t JavaScript

CREATE OR ALTER PROCEDURE product_history
AS
BEGIN
 DECLARE @product_history TABLE (
  product_name NVARCHAR(50),
  rating INT
 )
 INSERT INTO @product_history
 SELECT P.Name AS product_name, AVG(ALL R.rating) FROM Production.product P
 INNER JOIN  Production.product_review R
  ON R.product_ID = P.product_ID
 GROUP BY P.Name;

 DELETE FROM @product_history
 WHERE rating < 2;

 SELECT * FROM @product_history;

END
GO;

EXEC product_history
```

##### Result 21

<!-- prettier-ignore -->
|PRODUCT_NAME|Rating|
|---|---|
|HL Mountain Pedal|3|
|Mountain Bike Socks, M|5|
|Road-550-W Yellow, 40|5|

##### Snowflake SQL 12

##### MULTI-STATEMENT TABLE-VALUED 19

```sql
CREATE OR REPLACE PROCEDURE product_history ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
 // REGION SnowConvert AI Helpers Code
 var _RS, ROW_COUNT, _ROWS, MESSAGE_TEXT, SQLCODE = 0, SQLSTATE = '00000', OBJECT_SCHEMA_NAME  = 'UNKNOWN', ERROR_HANDLERS, NUM_ROWS_AFFECTED, PROC_NAME = arguments.callee.name, DOLLAR_DOLLAR = '$' + '$';
 function* sqlsplit(sql) {
  var part = '';
  var ismark = () => sql[i] == '$' && sql[i + 1] == '$';
  for(var i = 0;i < sql.length;i++) {
   if (sql[i] == ';') {
    yield part + sql[i];
    part = '';
   } else if (ismark()) {
    part += sql[i++] + sql[i++];
    while ( i < sql.length && !ismark() ) {
     part += sql[i++];
    }
    part += sql[i] + sql[i++];
   } else part += sql[i];
  }
  if (part.trim().length) yield part;
 };
 var formatDate = (arg) => (new Date(arg - (arg.getTimezoneOffset() * 60000))).toISOString().slice(0,-1);
 var fixBind = function (arg) {
  arg = arg == undefined ? null : arg instanceof Date ? formatDate(arg) : arg;
  return arg;
 };
 var EXEC = (stmt,binds = [],severity = "16",noCatch = false) => {
  binds = binds ? binds.map(fixBind) : binds;
  for(var stmt of sqlsplit(stmt)) {
   try {
    _RS = snowflake.createStatement({
      sqlText : stmt,
      binds : binds
     });
    _ROWS = _RS.execute();
    ROW_COUNT = _RS.getRowCount();
    NUM_ROWS_AFFECTED = _RS.getNumRowsAffected();
    return {
     THEN : (action) => !SQLCODE && action(fetch(_ROWS))
    };
   } catch(error) {
    let rStack = new RegExp('At .*, line (\\d+) position (\\d+)');
    let stackLine = error.stackTraceTxt.match(rStack) || [0,-1];
    MESSAGE_TEXT = error.message.toString();
    SQLCODE = error.code.toString();
    SQLSTATE = error.state.toString();
    snowflake.execute({
     sqlText : `SELECT UPDATE_ERROR_VARS_UDF(?,?,?,?,?,?)`,
     binds : [stackLine[1],SQLCODE,SQLSTATE,MESSAGE_TEXT,PROC_NAME,severity]
    });
    throw error;
   }
  }
 };
 // END REGION

  EXEC(`CREATE OR REPLACE TEMPORARY TABLE T_product_history (
   product_name VARCHAR(50),
   rating INT
)`);
 EXEC(` INSERT INTO T_product_history
 SELECT
    P.Name AS product_name,
    AVG(ALL R.rating) FROM
    Production.product P
    INNER JOIN
       Production.product_review R
       ON R.product_ID = P.product_ID
 GROUP BY
    P.Name`);
 EXEC(`DELETE FROM
   T_product_history
WHERE
   rating < 2`);
 EXEC(`
 SELECT
    *
 FROM
    T_product_history`);
$$;
;

CALL product_history();
```

##### Result 22

<!-- prettier-ignore -->
|PRODUCT_NAME|Rating|
|---|---|
|HL Mountain Pedal|3|
|Mountain Bike Socks, M|5|
|Road-550-W Yellow, 40|5|

### Related EWIs 2

1. [SSC-EWI-0040](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0040):
   Statement Not Supported.
2. [SSC-EWI-0073](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0073):
   Pending Functional Equivalence Review

## SCALAR

Translation reference to convert Transact-SQL UDF (User Defined Functions) with scalar return type
to Snowflake.

Applies to

- SQL Server
- Azure Synapse Analytics

### Description 4

#### Note 4

Some parts in the output code are omitted for clarity reasons.

> A scalar user-defined function is a Transact-SQL or common language runtime (CLR) routine that
> accepts parameters, performs an action, such as a complex calculation, and returns the result of
> that action as a scalar value.
> ([SQL Server Language ReferenceCREATE FUNCTION subsection](https://docs.microsoft.com/en-us/sql/t-sql/statements/create-function-transact-sql?view=sql-server-ver15)).

#### Note 5

These functions are usually used inside the `SELECT`statement, or single variable setup (most likely
inside a stored procedure).

#### Transact-SQL Syntax 2

```sql
 -- Transact-SQL Scalar Function Syntax
CREATE [ OR ALTER ] FUNCTION [ schema_name. ] function_name
( [ { @parameter_name [ AS ][ type_schema_name. ] parameter_data_type
 [ = default ] [ READONLY ] }
    [ ,...n ]
  ]
)
RETURNS return_data_type
    [ WITH `<function_option>` [ ,...n ] ]
    [ AS ]
    BEGIN
        function_body
        RETURN scalar_expression
    END
[ ; ]
```

#### Snowflake Syntax

Snowflake allows 3 different languages in their user defined functions:

- SQL
- JavaScript
- Java

For now, SnowConvert AI will support only `SQL` and `JavaScript` as target languages.

##### SQL

###### Note 6

SQL user defined functions only supports one query as their body. They can read from the database,
but is not allowed to write or modify it.
([Scalar SQL UDFs Reference](https://docs.snowflake.com/en/developer-guide/udf/sql/udf-sql-scalar-functions.html)).

```sql
CREATE [ OR REPLACE ] [ SECURE ] FUNCTION `<name>` ( [ `<arg_name>` `<arg_data_type>` ] [ , ... ] )
  RETURNS { `<result_data_type>` | TABLE ( `<col_name>` `<col_data_type>` [ , ... ] ) }
  [ [ NOT ] NULL ]
  [ { CALLED ON NULL INPUT | { RETURNS NULL ON NULL INPUT | STRICT } } ]
  [ VOLATILE | IMMUTABLE ]
  [ COMMENT = '`<string_literal>`' ]
  AS '`<function_definition>`'
```

##### JavaScript

###### Note 7

JavaScript user defined functions allows multiple statements in their bodies, but cannot perform
queries to the database. (Scalar JavaScript UDFs Reference)

```sql
CREATE [ OR REPLACE ] [ SECURE ] FUNCTION `<name>` ( [ `<arg_name>` `<arg_data_type>` ] [ , ... ] )
  RETURNS { `<result_data_type>` | TABLE ( `<col_name>` `<col_data_type>` [ , ... ] ) }
  [ [ NOT ] NULL ]
  LANGUAGE JAVASCRIPT
  [ { CALLED ON NULL INPUT | { RETURNS NULL ON NULL INPUT | STRICT } } ]
  [ VOLATILE | IMMUTABLE ]
  [ COMMENT = '`<string_literal>`' ]
  AS '`<function_definition>`'
```

### Sample Source Patterns 3

#### Set and Declare Statements

The most common statements in function bodies are the `DECLARE` and `SET` statements. For `DECLARE`
statements without default value, the transformation will be ignored. `SET` statements and `DECLARE`
statements with a default value, will be transformed to a `COMMON TABLE EXPRESSION.` Each common
table expression will contain a column that represents the local variable value.

##### Transact-SQL 13

##### Query

```sql
CREATE OR ALTER FUNCTION PURCHASING.GetVendorName()
RETURNS NVARCHAR(50) AS
BEGIN
 DECLARE @result NVARCHAR(50)
 DECLARE @BUSINESSENTITYID INT

 SET @BUSINESSENTITYID = 1492

 SELECT @result = Name FROM PURCHASING.VENDOR WHERE BUSINESSENTITYID = @BUSINESSENTITYID

 RETURN @result
END

GO

SELECT PURCHASING.GetVendorName() as vendor_name;
```

##### Result 23

<!-- prettier-ignore -->
|vendor_name|
|---|
|Australia Bike Retailer|

##### Snowflake 2

##### Query 2

```sql
CREATE OR REPLACE FUNCTION PURCHASING.GetVendorName ()
RETURNS VARCHAR(50)
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
AS
$$
 WITH CTE1 AS
 (
  SELECT
   1492 AS BUSINESSENTITYID
 ),
 CTE2 AS
 (
  SELECT
   Name AS RESULT
  FROM
   PURCHASING.VENDOR
  WHERE
   BUSINESSENTITYID = (
    SELECT
     BUSINESSENTITYID
    FROM
     CTE1
   )
 )
 SELECT
  RESULT
 FROM
  CTE2
$$;

SELECT
 PURCHASING.GetVendorName() as vendor_name;
```

##### Result 24

<!-- prettier-ignore -->
|VENDOR_NAME|
|---|
|Australia Bike Retailer|

#### If/Else Statement Transformation

If/Else statement can be handled in different ways, they can be either transformed to javascript or
to SQL using the [CASE EXPRESSION](https://docs.snowflake.com/en/sql-reference/functions/case.html)
inside the select allowing conditionals inside the queries, while the javascript transformation is
pretty straightforward, the Case statement might not be so obvious at first glance.

##### Transact-SQL 14

##### Query 3

```sql
CREATE OR ALTER FUNCTION PURCHASING.HasActiveFlag(@BusinessEntityID int)
RETURNS VARCHAR(10) AS
BEGIN
 DECLARE @result VARCHAR(10)
 DECLARE @ActiveFlag BIT

 SELECT @ActiveFlag = ActiveFlag from PURCHASING.VENDOR v where v.BUSINESSENTITYID = @BusinessEntityID

 IF @ActiveFlag = 1
  SET @result = 'YES'
 ELSE IF @ActiveFlag = 0
  SET @result = 'NO'

 RETURN @result
END

GO

SELECT PURCHASING.HasActiveFlag(1516) as has_active_flag;
```

##### Result 25

<!-- prettier-ignore -->
|has_active_flag|
|---|
|NO|

##### Snowflake 3

##### Query 4

```sql
CREATE OR REPLACE FUNCTION PURCHASING.HasActiveFlag (P_BUSINESSENTITYID INT)
RETURNS VARCHAR(10)
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
AS
$$
 WITH CTE1 AS
 (

  SELECT
   ActiveFlag AS ACTIVEFLAG
  from
   PURCHASING.VENDOR v
  where
   v.BUSINESSENTITYID = P_BUSINESSENTITYID
 ),
 CTE2 AS
 (
  SELECT
   CASE
    WHEN (
     SELECT
      ACTIVEFLAG
     FROM
      CTE1
    ) = 1
     THEN 'YES'
    WHEN (
     SELECT
      ACTIVEFLAG
     FROM
      CTE1
    ) = 0
     THEN 'NO'
   END AS RESULT
 )
 SELECT
  RESULT
 FROM
  CTE2
$$;

SELECT
 PURCHASING.HasActiveFlag(1516) as has_active_flag;
```

##### Result 26

<!-- prettier-ignore -->
|HAS_ACTIVE_FLAG|
|---|
|NO|

#### Nested Statements

For nested statements, the structured programming is being transformed to a single query. The
statements in the control-of-flow are going to be nested in table structures in order to preserve
the execution order.

##### Note 8

`CASE EXPRESSIONS` only can return one value per statement

##### Example

###### Note 9

The following code in both programming paradigms is functionally equivalent.

##### Structured Programming

```sql
 DECLARE @VendorId AS int;
DECLARE @AccountNumber AS VARCHAR(50);
SELECT @VendorId = poh.VendorID
    FROM Purchasing.PurchaseOrderHeader poh
    WHERE PurchaseOrderID = 1
SELECT @AccountNumber = v.AccountNumber
    FROM Purchasing.Vendor v
    WHERE v.BusinessEntityID = @VendorId
```

##### SQL 2

```sql
 SELECT V.AccountNumber AccountNumber
FROM (SELECT poh.VendorID VendorId
         FROM Purchasing.PurchaseOrderHeader poh
         WHERE PurchaseOrderID = 1
) T1, Purchasing.Vendor v
WHERE v.BusinessEntityID = T1.VendorId
```

##### Result 27

<!-- prettier-ignore -->
|AccountNumber|
|---|
|LITWARE0001|

#### Conditional variables through SELECTs

Variable definition and assignment within conditional statements tends to be somewhat problematic,
because references to the variable further down the code would have to know where the variable was
last modified. Not only that, but if the reference is within another conditional statement, then
there would have to be some kind of redirect that references the previous known assignment to the
variable.

This is all aggravated by nesting and complex querying that can be found on input code. That’s why a
specific
[EWI](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0068)
is added when these patterns are found.

In the following scenario, the first `IF` statement can be transformed without problems, because the
contents are straightforward enough. The second and third `IF` statements are commented out because
they’re not supported at the moment, since there are statements other than variable assignments
through `SELECT`.

##### SQL Server

##### Query 5

```sql
CREATE or ALTER FUNCTION PURCHASING.SELECTINUDF (
    @param1 varchar(12)
)
RETURNS int
AS
BEGIN
    declare @var1 int;
    declare @var2 int;
    declare @var3 int;

    IF @param1 = 'first'
    BEGIN
        select @var1 = col1 + 10 from table1 WHERE id = 0;
        select @var2 = col1 + 20 from table1 WHERE id = 0;
        select @var3 = col1 + 30 from table1 WHERE id = 0;
    END

    IF @param1 = 'second'
    BEGIN
        declare @var4 int = 10;
        select @var1 = col1 + 40 from table1 WHERE id = 0;
        select @var2 = col1 + 40 from table1 WHERE id = 0;
    END

    IF @param1 = 'third'
    BEGIN
        select col1 from table1 where id = 0;
        select @var1 = col1 + 50 from table1 WHERE id = 0;
        select @var2 = col1 + 50 from table1 WHERE id = 0;
    END

    RETURN @var1
END

SELECT PURCHASING.SELECTINUDF('first') as result; -- Assuming table1.col1 is 0 when ID = 0
```

##### Result 28

<!-- prettier-ignore -->
|RESULT|
|---|
|10|

##### Snowflake 4

##### Query 6

```sql
CREATE OR REPLACE FUNCTION PURCHASING.SELECTINUDF (PARAM1 STRING)
RETURNS INT
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
AS
$$
    WITH CTE1 AS
    (
        SELECT
            CASE
                WHEN PARAM1 = 'first'
                    THEN (SELECT
                        col1 + 10 AS VAR1 from
                        table1
                        WHERE
                        id = 0)
            END AS VAR1,
            CASE
                WHEN PARAM1 = 'first'
                        THEN (SELECT
                        col1 + 20 AS VAR2 from
                        table1
                        WHERE
                        id = 0)
            END AS VAR2,
            CASE
                WHEN PARAM1 = 'first'
                        THEN (SELECT
                        col1 + 30 AS VAR3 from
                        table1
                        WHERE
                        id = 0)
            END AS VAR3
    ),
    !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'IF STATEMENT' NODE ***/!!!
    CTE2 AS
    (
        /*    IF @param1 = 'second'
            BEGIN
                declare @var4 int = 10;
                select @var1 = col1 + 40 from table1 WHERE id = 0;
                select @var2 = col1 + 40 from table1 WHERE id = 0;
            END*/
        SELECT
            null
    ),
    !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'IF STATEMENT' NODE ***/!!!
    CTE3 AS
    (
        /*    IF @param1 = 'third'
            BEGIN
                select col1 from table1 where id = 0;
                select @var1 = col1 + 50 from table1 WHERE id = 0;
                select @var2 = col1 + 50 from table1 WHERE id = 0;
            END*/
        SELECT
            null
    ),
    CTE4 AS
    (

        SELECT
            PURCHASING.SELECTINUDF('first') as result
    )
    SELECT
        VAR1
    FROM
        CTE4
$$ -- Assuming table1.col1 is 0 when ID = 0
;
```

##### Result 29

<!-- prettier-ignore -->
|RESULT|
|---|
|10|

#### Assign and return a variable

In this simple pattern, there is a variable declaration, then, that variable is set using a `SELECT`
statement and finally returned. This is going to be migrated to a
[Common Table Expression](https://docs.snowflake.com/en/sql-reference/constructs/with.html) in order
to keep the original behavior.

##### SQL Server 2

##### Query 7

```sql
CREATE OR ALTER FUNCTION Purchasing.GetTotalFreight()
RETURNS MONEY AS
BEGIN
 DECLARE @Result MONEY
 SELECT @Result = ISNULL(SUM(t.Freight), 0) from Purchasing.PurchaseOrderHeader t
 return @Result
END

GO

select Purchasing.GetTotalFreight() as Result;
```

##### Result 30

<!-- prettier-ignore -->
|Result|
|---|
|1583978.2263|

##### Snowflake 5

##### Query 8

```sql
CREATE OR REPLACE FUNCTION Purchasing.GetTotalFreight ()
RETURNS NUMBER(38, 4)
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
AS
$$
 WITH CTE1 AS
 (
  SELECT
   NVL(SUM(t.Freight), 0) AS RESULT from
   Purchasing.PurchaseOrderHeader t
 )
 SELECT
  RESULT
 FROM
  CTE1
$$;

select
 Purchasing.GetTotalFreight() as Result;
```

##### Result 31

<!-- prettier-ignore -->
|RESULT|
|---|
|1583978.2263|

#### Multiple Function Calls

For this specific pattern there are no obvious queries, but there are multiple calls to multiple
functions working on the same variable and returning it at the end. Since Snowflake only supports
queries inside its functions, the solution for this block is going to be adding it to a Select and
nesting the calls inside, making sure the return value is the same as the one on the source.

##### SQL Server 3

##### Query 9

```sql
CREATE OR ALTER FUNCTION PURCHASING.Foo
(
 @PARAM1 INT
)
RETURNS varchar(25)
AS
BEGIN
 DECLARE @filter INT = @PARAM1
 DECLARE @NAME VARCHAR(25) = (SELECT Name from Purchasing.Vendor v where BusinessEntityID = @filter)
 SET @NAME = REPLACE(@NAME, 'Australia', 'USA')
 SET @NAME = REPLACE(@NAME, 'Bike', 'Car')
 RETURN @NAME
END

GO

SELECT PURCHASING.Foo(1492) AS Name;
```

##### Result 32

<!-- prettier-ignore -->
|Name|
|---|
|USA Car Retailer|

##### Snowflake 6

##### Query 10

```sql
CREATE OR REPLACE FUNCTION PURCHASING.Foo (PARAM1 INT)
RETURNS VARCHAR(25)
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
AS
$$
 WITH CTE1 AS
 (
  SELECT
   PARAM1 AS FILTER
 ),
 CTE2 AS
 (
  SELECT
   (SELECT
     Name
    from
     Purchasing.Vendor v
    where
     BusinessEntityID = (
      SELECT
       FILTER
      FROM
       CTE1
     )
   ) AS NAME
 ),
 CTE3 AS
 (
  SELECT
   REPLACE((
    SELECT
     NAME
    FROM
     CTE3
   ), 'Australia', 'USA') AS NAME
 ),
 CTE4 AS
 (
  SELECT
   REPLACE((
    SELECT
     NAME
    FROM
     CTE4
   ), 'Bike', 'Car') AS NAME
 )
 SELECT
  NAME
 FROM
  CTE4
$$;

SELECT
 PURCHASING.Foo(1492) AS Name;
```

##### Result 33

<!-- prettier-ignore -->
|NAME|
|---|
|USA Car Retailer|

#### Increase a variable based on multiple IF conditions and return its value

For this pattern, a variable is modified (increased in this case) using multiple IF conditions. In
the beginning, a set of variables is initialized and used to determine whether the result variable
should be increased or not. Finally, the result variable is returned.

##### SQL Server 4

##### Query 11

```sql
CREATE OR ALTER FUNCTION PURCHASING.FOO()
RETURNS MONEY
AS
BEGIN
 declare @firstValue MONEY
 declare @secondValue MONEY
 declare @Result MONEY
 select  @Result = 0
 select  @firstValue = SubTotal from Purchasing.PurchaseOrderHeader where PurchaseOrderID = 1
 select  @secondValue = SubTotal from Purchasing.PurchaseOrderHeader where PurchaseOrderID = 2
 if @firstValue is not null
  select @Result = @Result + @firstValue
 if @secondValue is not null
  select @Result = @Result + @secondValue
 return @Result
END

GO

SELECT PURCHASING.Foo() AS Result;
```

##### Result 34

<!-- prettier-ignore -->
|Result|
|---|
|473.1415|

##### Snowflake 7

##### Query 12

```sql
CREATE OR REPLACE FUNCTION PURCHASING.FOO ()
RETURNS NUMBER(38, 4)
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
AS
$$
 WITH CTE1 AS
 (
  select
   0 AS RESULT
 ),
 CTE2 AS
 (
  select
   SubTotal AS FIRSTVALUE
  from
   Purchasing.PurchaseOrderHeader
  where
   PurchaseOrderID = 1
 ),
 CTE3 AS
 (
  select
   SubTotal AS SECONDVALUE
  from
   Purchasing.PurchaseOrderHeader
  where
   PurchaseOrderID = 2
 ),
 CTE4 AS
 (
  SELECT
   CASE
    WHEN (
     SELECT
      FIRSTVALUE
     FROM
      CTE2
    ) is not null
     THEN (
     select
      (
       SELECT
        RESULT
       FROM
        CTE1
      ) + (
       SELECT
        FIRSTVALUE
       FROM
        CTE2
      ) AS RESULT)
   END AS RESULT
 ),
 CTE5 AS
 (
  SELECT
   CASE
    WHEN (
     SELECT
      SECONDVALUE
     FROM
      CTE3
    ) is not null
     THEN (
     select
      (
       SELECT
        RESULT
       FROM
        CTE1
      ) + (
       SELECT
        SECONDVALUE
       FROM
        CTE3
      ) AS RESULT)
    ELSE (SELECT
     RESULT
    FROM
     CTE4)
   END AS RESULT
 )
 SELECT
  RESULT
 FROM
  CTE5
$$;

SELECT
 PURCHASING.Foo() AS Result;
```

##### Result 35

<!-- prettier-ignore -->
|RESULT|
|---|
|473.1415|

#### Two or more RETURN statements

For this pattern, the `IF` block containing the return clause that breaks the code flow is added at
the end of the body, like the final statement to be executed in a `CASE` expression.

##### Basic Case

For this particular scenario, there is no logic between the conditional `RETURN` statement and the
final `RETURN` statement, so all body will be mapped to a single `CASE EXPRESSION`.

##### SQL Server 5

##### Query 13

```sql
CREATE OR ALTER FUNCTION [PURCHASING].[FOO] ()
RETURNS INT
AS
BEGIN
 IF exists (SELECT PreferredVendorStatus FROM Purchasing.Vendor v )
  RETURN 1

 RETURN 0
END

GO

SELECT PURCHASING.FOO() as result;
```

##### Result 36

<!-- prettier-ignore -->
|result|
|---|
|1|

##### Snowflake 8

##### Query 14

```sql
CREATE OR REPLACE FUNCTION PURCHASING.FOO ()
RETURNS INT
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
AS
$$
 SELECT
  CASE
   WHEN exists (SELECT
     PreferredVendorStatus
    FROM
     Purchasing.Vendor v
   )
    THEN 1
   ELSE 0
  END
$$;

SELECT
 PURCHASING.FOO() as result;
```

##### Result 37

<!-- prettier-ignore -->
|RESULT|
|---|
|1|

#### Common Table Expressions

Common table expressions will be kept as in the original code, and they are going to be concatenated
with the generated ones. SnowConvert AI is able to identify first all the original
`COMMON TABLE EXPRESSION` names in order to avoid generating duplicated names.

##### SQL Server 6

##### Query 15

```sql
CREATE OR ALTER FUNCTION [PURCHASING].[FOO]
(
 @status INT
)
Returns INT
As
Begin
 Declare @result as int = 0

 ;WITH ctetable(RevisionNumber) as
 (
  SELECT RevisionNumber
  FROM Purchasing.PurchaseOrderHeader poh
  where poh.Status = @status
 ),
 finalCte As
 (
  SELECT RevisionNumber FROM ctetable
 )

 Select @result = count(RevisionNumber) from finalCte
 return @result;
End

GO

SELECT PURCHASING.FOO(4) as result;
```

##### Result 38

<!-- prettier-ignore -->
|result|
|---|
|3689|

##### Snowflake 9

##### Query 16

```sql
CREATE OR REPLACE FUNCTION PURCHASING.FOO (STATUS INT)
Returns INT
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
AS
$$
 WITH CTE1 AS
 (
  SELECT
   0 AS RESULT
 ),
 ctetable (
  RevisionNumber
 ) as
  (
   SELECT
   RevisionNumber
   FROM
   Purchasing.PurchaseOrderHeader poh
   where
   poh.Status = STATUS
  ),
  finalCte As
  (
   SELECT
   RevisionNumber
  FROM
   ctetable
  ),
  CTE2 AS
  (
  Select
   COUNT(RevisionNumber) AS RESULT from
   finalCte
  )
  SELECT
  RESULT
  FROM
  CTE2
$$;

SELECT
  PURCHASING.FOO(4) as result;
```

##### Result 39

<!-- prettier-ignore -->
|RESULT|
|---|
|3689|

#### Transform to JavaScript UDFs

If there are multiple statements and the function does not access the database in any way, it can be
transformed into a JavaScript function keeping the functional equivalence

##### SQL Server 7

##### Query 1

```sql
CREATE OR ALTER FUNCTION PURCHASING.GetFiscalYear
(
 @DATE AS DATETIME
)
RETURNS INT
AS
BEGIN
 DECLARE @FiscalYear AS INT
 DECLARE @CurMonth AS INT
 SET @CurMonth = DATEPART(M,@DATE)
 SET @FiscalYear = DATEPART(YYYY, @DATE)
 IF (@CurMonth >= 7)
 BEGIN
  SET @FiscalYear = @FiscalYear + 1
 END
 RETURN @FiscalYear
END

GO

SELECT PURCHASING.GetFiscalYear('2020-10-10') as DATE;
```

##### Query 2 2

```sql
CREATE OR ALTER FUNCTION PURCHASING.[getCleanChargeCode]
(
 @ChargeCode varchar(50)
)
returns varchar(50) as
begin
 declare @CleanChargeCode varchar(50),@Len int,@Pos int=2
 set @Pos=LEN(@ChargeCode)-1
 while @Pos > 1
 begin
  set @CleanChargeCode=RIGHT(@ChargeCode,@Pos)
  if TRY_CAST(@CleanChargeCode as bigint) is not null
   return @CleanChargeCode
  set @Pos=@Pos-1
 end
 set @Pos=LEN(@ChargeCode)-1
 while @Pos > 1
 begin
  set @CleanChargeCode=LEFT(@ChargeCode,@Pos)
  if TRY_CAST(@CleanChargeCode as bigint) is not null
   return @CleanChargeCode
  set @Pos=@Pos-1
 end
 return null
end

GO

SELECT PURCHASING.[getCleanChargeCode](https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/transact/'16test') AS CleanChargeCode;
```

##### Result 1

<!-- prettier-ignore -->
|DATE|
|---|
|2021|

##### Result 2 2

<!-- prettier-ignore -->
|CleanChargeCode|
|---|
|16|

##### Snowflake 10

##### Query 1 2

```sql
!!!RESOLVE EWI!!! /*** SSC-EWI-0068 - USER DEFINED FUNCTION WAS TRANSFORMED TO SNOWFLAKE PROCEDURE ***/!!!
CREATE OR REPLACE PROCEDURE PURCHASING.GetFiscalYear (DATE TIMESTAMP_NTZ(3))
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
 DECLARE
  FISCALYEAR INT;
  CURMONTH INT;
 BEGIN

  CURMONTH := DATE_PART(month, :DATE :: TIMESTAMP);
  FISCALYEAR := DATE_PART(year, :DATE :: TIMESTAMP);
  IF ((:CURMONTH >= 7)) THEN
   BEGIN
    FISCALYEAR := :FISCALYEAR + 1;
   END;
  END IF;
  RETURN :FISCALYEAR;
 END;
$$;

SELECT
 PURCHASING.GetFiscalYear('2020-10-10') !!!RESOLVE EWI!!! /*** SSC-EWI-0067 - UDF WAS TRANSFORMED TO SNOWFLAKE PROCEDURE, CALLING PROCEDURES INSIDE QUERIES IS NOT SUPPORTED ***/!!! as DATE;
```

##### Query 2 2 2

```sql
!!!RESOLVE EWI!!! /*** SSC-EWI-0068 - USER DEFINED FUNCTION WAS TRANSFORMED TO SNOWFLAKE PROCEDURE ***/!!!
CREATE OR REPLACE PROCEDURE PURCHASING.getCleanChargeCode (CHARGECODE STRING)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
 DECLARE
  CLEANCHARGECODE VARCHAR(50);
  LEN INT;
  POS INT := 2;
 BEGIN

  POS := LEN(:CHARGECODE)-1;
  WHILE (:POS > 1) LOOP
   CLEANCHARGECODE := RIGHT(:CHARGECODE, :POS);
   IF (CAST(:CLEANCHARGECODE AS BIGINT) /*** SSC-FDM-TS0005 - TRY_CONVERT/TRY_CAST COULD NOT BE CONVERTED TO TRY_CAST ***/!!!RESOLVE EWI!!! /*** SSC-EWI-TS0074 - CAST RESULT MAY BE DIFFERENT FROM TRY_CAST FUNCTION DUE TO MISSING DEPENDENCIES ***/!!! is not null) THEN
    RETURN :CLEANCHARGECODE;
   END IF;
   POS := :POS -1;
  END LOOP;
  POS := LEN(:CHARGECODE)-1;
  WHILE (:POS > 1) LOOP
   CLEANCHARGECODE := LEFT(:CHARGECODE, :POS);
   IF (CAST(:CLEANCHARGECODE AS BIGINT) /*** SSC-FDM-TS0005 - TRY_CONVERT/TRY_CAST COULD NOT BE CONVERTED TO TRY_CAST ***/!!!RESOLVE EWI!!! /*** SSC-EWI-TS0074 - CAST RESULT MAY BE DIFFERENT FROM TRY_CAST FUNCTION DUE TO MISSING DEPENDENCIES ***/!!! is not null) THEN
    RETURN :CLEANCHARGECODE;
   END IF;
   POS := :POS -1;
  END LOOP;
  RETURN null;
 END;
$$;

SELECT
 PURCHASING.getCleanChargeCode('16test') !!!RESOLVE EWI!!! /*** SSC-EWI-0067 - UDF WAS TRANSFORMED TO SNOWFLAKE PROCEDURE, CALLING PROCEDURES INSIDE QUERIES IS NOT SUPPORTED ***/!!! AS CleanChargeCode;
```

##### Result 1 2

<!-- prettier-ignore -->
|DATE|
|---|
|2021.0|

##### Result 2 2 2

<!-- prettier-ignore -->
|CLEANCHARGECODE|
|---|
|16|

### Known Issues 3

Warning

User-defined functions cannot be used to perform actions that modify the database state

Warning

User-defined functions cannot contain an `OUTPUT INTO` clause that has a table as its target

Warning

User-defined functions cannot DECLARE, OPEN, FETCH, CLOSE or DEALLOCATE a `CURSOR`. Use a Stored
Procedure if you need to use cursors.

Warning

User-defined functions cannot perform control-of-flow statements such as WHILE if there is at least
one call to the database

Warning

User-defined functions with references to other user-defined functions that were transformed to
Stored Procedures, will be transformed to Stored Procedures too.

Warning

User-defined functions that use
[@@ROWCOUNT](https://docs.microsoft.com/en-us/sql/t-sql/functions/rowcount-transact-sql?view=sql-server-ver15)
are not supported in SQL and should be transformed to stored procedures in order to keep the
functional equivalence.

Warning

User-defined functions that have `SELECT` statements assigning a variable to itself is not supported
in Snowflake. See also
[SELECT @local_variable](https://docs.microsoft.com/en-us/sql/t-sql/language-elements/select-local-variable-transact-sql?view=sql-server-ver15)

For all the unsupported cases, please check the related EWIs and the patterns below to obtain
recommendations and possible workarounds.

#### Conditionals other than if/else statements along side queries

The next scenario involves the use of the “while statement” along side other queries. The problem
with this example is that there’s no way of transforming the while statement to a CTE inside the
`WITH` clause of the main select, this forces us to transform this statement to JavaScript procedure
to maintain the same logic.

##### SQL Server 8

##### Query 17

```sql
CREATE OR ALTER FUNCTION PURCHASING.FOO()
RETURNS INT
AS
BEGIN
    DECLARE @i int = 0, @p int;
    Select @p = COUNT(*) FROM PURCHASING.VENDOR

    WHILE (@p < 1000)
    BEGIN
        SET @i = @i + 1
        SET @p = @p + @i
    END

    IF (@i = 6)
        RETURN 1

    RETURN @p
END

GO

SELECT PURCHASING.FOO() as result;
```

##### Result 40

<!-- prettier-ignore -->
|result|
|---|
|1007|

###### Snowflake 2 2

##### Query 18

```sql
 !!!RESOLVE EWI!!! /*** SSC-EWI-0068 - USER DEFINED FUNCTION WAS TRANSFORMED TO SNOWFLAKE PROCEDURE ***/!!!
CREATE OR REPLACE PROCEDURE PURCHASING.FOO ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        I INT := 0;
        P INT;
    BEGIN

        Select
            COUNT(*)
        INTO
            :P
 FROM
            PURCHASING.VENDOR;
        WHILE (:P < 1000) LOOP
            I := :I + 1;
            P := :P + :I;
        END LOOP;
        IF ((:I = 6)) THEN
            RETURN 1;
        END IF;
        RETURN :P;
    END;
$$;

SELECT
    PURCHASING.FOO() !!!RESOLVE EWI!!! /*** SSC-EWI-0067 - UDF WAS TRANSFORMED TO SNOWFLAKE PROCEDURE, CALLING PROCEDURES INSIDE QUERIES IS NOT SUPPORTED ***/!!! as result;
```

##### Result 41

<!-- prettier-ignore -->
|FOO|
|---|
|1007|

#### Assign a variable using its own value iterating through a rowset

In the following example, the variable `@names` is used to concatenate multiple values from a column
into one single string. The variable is updated on each iteration as shown, which is not supported
by SnowFlake UDFs. For this scenario, the function should be transformed into a _procedure_.

##### SQL Server 2 2

##### Query 19

```sql
CREATE OR ALTER FUNCTION PURCHASING.FOO()
RETURNS VARCHAR(8000)
AS
BEGIN
    DECLARE @names varchar(8000)
    SET @names = ''
    SELECT @names = ISNULL(@names + ' ', '') + Name from Purchasing.Vendor v
    return @names
END

GO

select PURCHASING.FOO() as names;
```

##### Result 42

<!-- prettier-ignore -->
|names|
|---|
|Australia Bike Retailer Allenson Cycles Advanced Bicycles Trikes, Inc. Morgan Bike Accessories Cycling Master Chicago Rent-All Greenwood Athletic Company Compete Enterprises, Inc International Light Speed Training Systems Gardner Touring Cycles Internati|

###### Snowflake query

```sql
!!!RESOLVE EWI!!! /*** SSC-EWI-0068 - USER DEFINED FUNCTION WAS TRANSFORMED TO SNOWFLAKE PROCEDURE ***/!!!
CREATE OR REPLACE PROCEDURE PURCHASING.FOO ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        NAMES VARCHAR(8000);
    BEGIN

        NAMES := '';
        SELECT
            NVL(:NAMES || ' ', '') + Name
        INTO
            :NAMES
        from
            Purchasing.Vendor v;
        RETURN :NAMES;
    END;
$$;

select
    PURCHASING.FOO() !!!RESOLVE EWI!!! /*** SSC-EWI-0067 - UDF WAS TRANSFORMED TO SNOWFLAKE PROCEDURE, CALLING PROCEDURES INSIDE QUERIES IS NOT SUPPORTED ***/!!! as names;
```

Warning

For the described scenarios above, consider the following limitations:

1. All the calls to user-defined functions in DML queries such as `SELECT`, `INSERT`, `DELETE`,
   `UPDATE` or `MERGE` will fail because calls to Stored Procedures within these queries are not
   allowed.
2. Calls to user-defined functions inside procedures, should be preceeded by the `CALL` keyword.
3. Use- defined functions used in
   [COMPUTED COLUMNS](https://docs.microsoft.com/en-us/sql/relational-databases/tables/specify-computed-columns-in-a-table?view=sql-server-ver15)
   will fail during the execution.

### Related EWIs 3

1. [SSC-EWI-0067](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0067):
   UDF was transformed to Snowflake procedure, calling procedures inside a query is not supported.
2. [SSC-EWI-0068](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0068):
   User defined function was transformed to a Snowflake procedure.
3. [SSC-EWI-0073](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0073):
   Pending Functional Equivalence Review.

## Snowflake Script UDF (SCALAR)

Translation reference for SQL Server Scalar User Defined Functions to
[Snowflake Scripting UDFs](https://docs.snowflake.com/en/migrations/snowconvert-docs/developer-guide/udf/sql/udf-sql-procedural-functions)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description 5

SnowConvert supports translating SQL Server Scalar User Defined Functions directly to **Snowflake
Scripting UDFs** (SnowScript UDFs) when they meet specific criteria, instead of converting all
functions to Stored Procedures.

**Snowflake Scripting UDFs** are user-defined functions written using Snowflake’s procedural
language syntax (Snowscript) within a SQL UDF body. They support variables, loops, conditional
logic, and exception handling.

#### When Functions Become SnowScript UDFs

SnowConvert analyzes each SQL Server function and automatically determines the appropriate Snowflake
target. A function becomes a SnowScript UDF when it contains **only** procedural logic without data
access operations.

### Sample Source Patterns 4

#### Simple Calculation Function

A basic scalar function that performs calculations without querying data.

##### SQL Server 9

```sql
CREATE FUNCTION dbo.CalculateProfit
(
    @Cost DECIMAL(10,2),
    @Revenue DECIMAL(10,2)
)
RETURNS DECIMAL(10,2)
AS
BEGIN
    DECLARE @Profit DECIMAL(10,2)
    SET @Profit = @Revenue - @Cost
    RETURN @Profit
END
GO

SELECT dbo.CalculateProfit(100.00, 150.00) as Profit;
```

##### Result 43

<!-- prettier-ignore -->
|Profit|
|---|
|50.00|

##### Snowflake (SnowScript UDF)

```sql
CREATE OR REPLACE FUNCTION dbo.CalculateProfit (COST DECIMAL(10,2), REVENUE DECIMAL(10,2))
RETURNS DECIMAL(10, 2)
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "10/09/2025",  "domain": "no-domain-provided",  "migrationid": "QsqZARsvG3aeleeXZB43fg==" }}'
AS
$$
   DECLARE
 PROFIT DECIMAL(10, 2);
   BEGIN

 PROFIT := :REVENUE - :COST;
 RETURN :PROFIT;
   END;
$$;

SELECT
   dbo.CalculateProfit(100.00, 150.00) as Profit;
```

##### Result 44

<!-- prettier-ignore -->
|PROFIT|
|---|
|50.00|

#### Function with Conditional Logic (IF/ELSE)

Functions using IF/ELSE statements for business logic.

##### SQL Server 10

```sql
CREATE FUNCTION dbo.GetDiscountRate
(
    @CustomerType VARCHAR(20),
    @OrderAmount DECIMAL(10,2)
)
RETURNS DECIMAL(5,2)
AS
BEGIN
    DECLARE @Discount DECIMAL(5,2)

    IF @CustomerType = 'Premium'
        SET @Discount = 0.15
    ELSE IF @CustomerType = 'Standard'
        SET @Discount = 0.10
    ELSE
        SET @Discount = 0.05

    IF @OrderAmount > 1000
        SET @Discount = @Discount + 0.05

    RETURN @Discount
END
GO

SELECT dbo.GetDiscountRate('Premium', 1200.00) as DiscountRate;
```

##### Result 45

<!-- prettier-ignore -->
|DiscountRate|
|---|
|0.20|

##### Snowflake (SnowScript UDF) 2

```sql
CREATE OR REPLACE FUNCTION dbo.GetDiscountRate (CUSTOMERTYPE STRING, ORDERAMOUNT DECIMAL(10,2))
RETURNS DECIMAL(5, 2)
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "10/09/2025",  "domain": "no-domain-provided",  "migrationid": "QsqZARsvG3aeleeXZB43fg==" }}'
AS
$$
   DECLARE
 DISCOUNT DECIMAL(5, 2);
   BEGIN

 IF (:CUSTOMERTYPE = 'Premium') THEN
 DISCOUNT := 0.15;
 ELSEIF (:CUSTOMERTYPE = 'Standard') THEN
 DISCOUNT := 0.10;
 ELSE
 DISCOUNT := 0.05;
 END IF;
 IF (:ORDERAMOUNT > 1000) THEN
 DISCOUNT := :DISCOUNT + 0.05;
 END IF;
 RETURN :DISCOUNT;
   END;
$$;

SELECT
   dbo.GetDiscountRate('Premium', 1200.00) as DiscountRate;
```

##### Result 46

<!-- prettier-ignore -->
|DISCOUNTRATE|
|---|
|0.20|

#### Function with WHILE Loop

Functions using WHILE loops for iterative calculations.

##### SQL Server 11

```sql
CREATE FUNCTION dbo.Factorial
(
    @Number INT
)
RETURNS BIGINT
AS
BEGIN
    DECLARE @Result BIGINT = 1
    DECLARE @Counter INT = 1

    WHILE @Counter <= @Number
    BEGIN
        SET @Result = @Result * @Counter
        SET @Counter = @Counter + 1
    END

    RETURN @Result
END
GO

SELECT dbo.Factorial(5) as FactorialResult;
```

##### Result 47

<!-- prettier-ignore -->
|FactorialResult|
|---|
|120|

##### Snowflake (SnowScript UDF) 3

```sql
CREATE OR REPLACE FUNCTION dbo.Factorial (NUMBER INT)
RETURNS BIGINT
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "10/09/2025",  "domain": "no-domain-provided",  "migrationid": "QsqZARsvG3aeleeXZB43fg==" }}'
AS
$$
  DECLARE
  RESULT BIGINT := 1;
  COUNTER INT := 1;
  BEGIN

    WHILE (:COUNTER <= :NUMBER) LOOP
      RESULT := :RESULT * :COUNTER;
      COUNTER := :COUNTER + 1;
    END LOOP;
    RETURN :RESULT;
  END;
$$;

SELECT
   dbo.Factorial(5) as FactorialResult;
```

##### Result 48

<!-- prettier-ignore -->
|FACTORIALRESULT|
|---|
|120|

#### String Manipulation Function

Complex string operations using loops and conditional logic.

##### SQL Server 12

```sql
CREATE FUNCTION dbo.CleanPhoneNumber
(
    @Phone VARCHAR(20)
)
RETURNS VARCHAR(10)
AS
BEGIN
    DECLARE @Clean VARCHAR(10) = ''
    DECLARE @i INT = 1
    DECLARE @Char CHAR(1)

    WHILE @i <= LEN(@Phone)
    BEGIN
        SET @Char = SUBSTRING(@Phone, @i, 1)
        IF @Char BETWEEN '0' AND '9'
            SET @Clean = @Clean + @Char
        SET @i = @i + 1
    END

    RETURN @Clean
END
GO

SELECT dbo.CleanPhoneNumber('(555) 123-4567') as CleanPhone;
```

##### Result 49

<!-- prettier-ignore -->
|CleanPhone|
|---|
|5551234567|

##### Snowflake (SnowScript UDF) 4

```sql
CREATE OR REPLACE FUNCTION dbo.CleanPhoneNumber (PHONE STRING)
RETURNS VARCHAR(10)
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "10/09/2025",  "domain": "no-domain-provided",  "migrationid": "QsqZARsvG3aeleeXZB43fg==" }}'
AS
$$
   DECLARE
 CLEAN VARCHAR(10) := '';
 I INT := 1;
 CHAR CHAR(1);
   BEGIN

 WHILE (:I <= LEN(:PHONE)) LOOP
 CHAR := SUBSTRING(:PHONE, :I, 1);
 IF (:CHAR BETWEEN '0' AND '9') THEN
  CLEAN := :CLEAN + :CHAR;
 END IF;
 I := :I + 1;
 END LOOP;
 RETURN :CLEAN;
   END;
$$;

SELECT
   dbo.CleanPhoneNumber('(555) 123-4567') as CleanPhone;
```

##### Result 50

<!-- prettier-ignore -->
|CLEANPHONE|
|---|
|5551234567|

#### CASE Statement Logic

Functions using CASE expressions for categorization.

##### SQL Server 13

```sql
CREATE FUNCTION dbo.GetGrade
(
    @Score INT
)
RETURNS CHAR(1)
AS
BEGIN
    DECLARE @Grade CHAR(1)

    SET @Grade = CASE
        WHEN @Score >= 90 THEN 'A'
        WHEN @Score >= 80 THEN 'B'
        WHEN @Score >= 70 THEN 'C'
        WHEN @Score >= 60 THEN 'D'
        ELSE 'F'
    END

    RETURN @Grade
END
GO

SELECT dbo.GetGrade(85) as Grade;
```

##### Result 51

<!-- prettier-ignore -->
|Grade|
|---|
|B|

##### Snowflake (SnowScript UDF) 5

```sql
CREATE OR REPLACE FUNCTION dbo.GetGrade (SCORE INT)
RETURNS CHAR(1)
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "10/09/2025",  "domain": "no-domain-provided",  "migrationid": "QsqZARsvG3aeleeXZB43fg==" }}'
AS
$$
   DECLARE
 GRADE CHAR(1);
   BEGIN

 CASE
 WHEN :SCORE >= 90 THEN
  GRADE := 'A';
 WHEN :SCORE >= 80 THEN
  GRADE := 'B';
 WHEN :SCORE >= 70 THEN
  GRADE := 'C';
 WHEN :SCORE >= 60 THEN
  GRADE := 'D';
 ELSE
  GRADE := 'F';
 END;
 RETURN :GRADE;
   END;
$$;

SELECT
   dbo.GetGrade(85) as Grade;
```

##### Result 52

<!-- prettier-ignore -->
|GRADE|
|---|
|B|

#### Select Into variable assingment

Functions using simple select into for variable assignment.

##### SQL Server 14

```sql
CREATE FUNCTION dbo.CalculatePrice
(
    @BasePrice DECIMAL(10, 2),
    @Quantity INT
)
RETURNS DECIMAL(10, 2)
AS
BEGIN
    DECLARE @Discount DECIMAL(5, 2);
    DECLARE @Subtotal DECIMAL(10, 2);
    DECLARE @FinalPrice DECIMAL(10, 2);

    SELECT @Discount = CASE
                           WHEN @Quantity >= 10 THEN 0.15
                           WHEN @Quantity >= 5 THEN 0.10
                           ELSE 0.05
                       END,
           @Subtotal = @BasePrice * @Quantity;

    SET @FinalPrice = @Subtotal * (1 - @Discount);

    RETURN @FinalPrice;
END;
```

##### Result 53

<!-- prettier-ignore -->
|CALCULATEPRICE(100, 3)|
|---|
|285|

##### Snowflake (SnowScript UDF) 6

```sql
CREATE OR REPLACE FUNCTION dbo.CalculatePrice (BASEPRICE DECIMAL(10, 2), QUANTITY INT)
RETURNS DECIMAL(10, 2)
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "11/26/2025",  "domain": "no-domain-provided",  "migrationid": "T8GaASfFsHeOffK4v3SnIQ==" }}'
AS
$$
    DECLARE
        DISCOUNT DECIMAL(5, 2);
        SUBTOTAL DECIMAL(10, 2);
        FINALPRICE DECIMAL(10, 2);
    BEGIN

        DISCOUNT := CASE
                                      WHEN :QUANTITY >= 10 THEN 0.15
                                      WHEN :QUANTITY >= 5 THEN 0.10
                                      ELSE 0.05
                                  END;
        SUBTOTAL := :BASEPRICE * :QUANTITY;
        FINALPRICE := :SUBTOTAL * (1 - :DISCOUNT);
        RETURN :FINALPRICE;
    END;
$$;
```

##### Result 54

<!-- prettier-ignore -->
|CALCULATEPRICE(100, 3)|
|---|
|285|

### Known Issues 4

Warning

**SnowConvert AI will not translate UDFs containing the following elements into SnowScripting UDFs,
as these features are unsupported in SnowScripting UDFs:**

- Access database tables
- Use cursors
- Call other UDFs
- Contain aggregate or window functions
- Perform DML operations (INSERT/UPDATE/DELETE)
- Return result sets

### Related EWIs 4

1. [SSC-EWI-0067](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0067):
   UDF was transformed to Snowflake procedure, calling procedures inside a query is not supported.
2. [SSC-EWI-0068](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0068):
   User defined function was transformed to a Snowflake procedure.
3. [SSC-EWI-0073](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0073):
   Pending Functional Equivalence Review.
