---
auto_generated: true
description: Returns TRUE when the input expression (numeric or string) is within
  the specified lower and upper boundary.
last_scraped: '2026-01-14T16:54:07.858481+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/transact/transact-dmls
title: SnowConvert AI - SQL Server-Azure Synapse - DMLs | Snowflake Documentation
---

1. [Overview](../../../../guides/README.md)
2. [Snowflake Horizon Catalog](../../../../user-guide/snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../../../../guides/overview-connecting.md)
6. [Virtual warehouses](../../../../user-guide/warehouses.md)
7. [Databases, Tables, & Views](../../../../guides/overview-db.md)
8. [Data types](../../../../data-types.md)
10. Data Integration

    - [Snowflake Openflow](../../../../user-guide/data-integration/openflow/about.md)
    - Apache Iceberg™

      - [Apache Iceberg™ Tables](../../../../user-guide/tables-iceberg.md)
      - [Snowflake Open Catalog](../../../../user-guide/opencatalog/overview.md)
11. Data engineering

    - [Data loading](../../../../guides/overview-loading-data.md)
    - [Dynamic Tables](../../../../user-guide/dynamic-tables-about.md)
    - [Streams and Tasks](../../../../user-guide/data-pipelines-intro.md)
    - [dbt Projects on Snowflake](../../../../user-guide/data-engineering/dbt-projects-on-snowflake.md)
    - [Data Unloading](../../../../guides/overview-unloading-data.md)
12. [Storage Lifecycle Policies](../../../../user-guide/storage-management/storage-lifecycle-policies.md)
13. [Migrations](../../../README.md)

    * Tools

      * [SnowConvert AI](../../overview.md)

        + General

          + [About](../../general/about.md)
          + [Getting Started](../../general/getting-started/README.md)
          + [Terms And Conditions](../../general/terms-and-conditions/README.md)
          + [Release Notes](../../general/release-notes/release-notes/README.md)
          + User Guide

            + [SnowConvert AI](../../general/user-guide/snowconvert/README.md)
            + [Project Creation](../../general/user-guide/project-creation.md)
            + [Extraction](../../general/user-guide/extraction.md)
            + [Deployment](../../general/user-guide/deployment.md)
            + [Data Migration](../../general/user-guide/data-migration.md)
            + [Data Validation](../../general/user-guide/data-validation.md)
            + [Power BI Repointing](../../general/user-guide/power-bi-repointing-general.md)
            + [ETL Migration](../../general/user-guide/etl-migration-replatform.md)
          + [Technical Documentation](../../general/technical-documentation/README.md)
          + [Contact Us](../../general/contact-us.md)
          + Others

            + [Using SnowConvert AI In A Ubuntu Docker Image](../../general/others/using-snowconvert-in-a-ubuntu-docker-image.md)
          + [Frequently Asked Questions (FAQ)](../../general/frequently-asked-questions-faq.md)")
        + Translation References

          + [General](../general/README.md)
          + [Teradata](../teradata/README.md)
          + [Oracle](../oracle/README.md)
          + [SQL Server-Azure Synapse](README.md)

            - [ANSI NULLS](transact-ansi-nulls.md)
            - [QUOTED\_IDENTIFIER](transact-quoted-identifier.md)
            - [Built-in Functions](transact-built-in-functions.md)
            - [Built-in Procedures](transact-built-in-procedures.md)
            - Data Definition Language

              - [ALTER TABLE](transact-alter-statement.md)
              - [CONTINUE HANDLER](transact-continue-handler.md)
              - [EXIT HANDLER](transact-exit-handler.md)
              - [CREATE FUNCTION](transact-create-function.md)
              - [CREATE INDEX](transact-create-index.md)
              - [CREATE MATERIALIZED VIEW](transact-create-materialized-view.md)
              - [CREATE PROCEDURE (JavaScript)](transact-create-procedure.md)")
              - [CREATE PROCEDURE (Snowflake Scripting)](transact-create-procedure-snow-script.md)")
              - [CREATE TABLE](transact-create-table.md)
              - [CREATE VIEW](transact-create-view.md)
            - [Data Types](transact-data-types.md)
            - [Data Manipulation Language](transact-dmls.md)
            - [General Statements](transact-general-statements.md)
            - [SELECT](transact-select.md)
            - [SYSTEM TABLES](transact-system-tables.md)
            - ETL And BI Repointing

              - [Power BI Transact and Synapse Repointing](etl-bi-repointing/power-bi-transact-repointing.md)
          + [Sybase IQ](../sybase/README.md)
          + [Hive-Spark-Databricks SQL](../hive/README.md)
          + [Redshift](../redshift/README.md)
          + [PostgreSQL-Greenplum-Netezza](../postgres/README.md)
          + [BigQuery](../bigquery/README.md)
          + [Vertica](../vertica/README.md)
          + [IBM DB2](../db2/README.md)
          + [SSIS](../ssis/README.md)
        + [Migration Assistant](../../migration-assistant/README.md)
        + [Data Validation CLI](../../data-validation-cli/index.md)
        + [AI Verification](../../snowconvert-ai-verification.md)
      * [Snowpark Migration Accelerator](../../../sma-docs/README.md)
    * Guides

      * [Teradata](../../../guides/teradata.md)
      * [Databricks](../../../guides/databricks.md)
      * [SQL Server](../../../guides/sqlserver.md)
      * [Amazon Redshift](../../../guides/redshift.md)
      * [Oracle](../../../guides/oracle.md)
      * [Azure Synapse](../../../guides/azuresynapse.md)
15. [Queries](../../../../guides/overview-queries.md)
16. [Listings](../../../../collaboration/collaboration-listings-about.md)
17. [Collaboration](../../../../guides/overview-sharing.md)
19. [Snowflake AI & ML](../../../../guides/overview-ai-features.md)
21. [Snowflake Postgres](../../../../user-guide/snowflake-postgres/about.md)
23. [Alerts & Notifications](../../../../guides/overview-alerts.md)
25. [Security](../../../../guides/overview-secure.md)
26. [Data Governance](../../../../guides/overview-govern.md)
27. [Privacy](../../../../guides/overview-privacy.md)
29. [Organizations & Accounts](../../../../guides/overview-manage.md)
30. [Business continuity & data recovery](../../../../user-guide/replication-intro.md)
32. [Performance optimization](../../../../guides/overview-performance.md)
33. [Cost & Billing](../../../../guides/overview-cost.md)

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)Translation References[SQL Server-Azure Synapse](README.md)Data Manipulation Language

# SnowConvert AI - SQL Server-Azure Synapse - DMLs[¶](#snowconvert-ai-sql-server-azure-synapse-dmls "Link to this heading")

## BETWEEN[¶](#between "Link to this heading")

Returns TRUE when the input expression (numeric or string) is within the
specified lower and upper boundary.

Applies to

* SQL Server
* Azure Synapse Analytics

Note

Some parts in the output code are omitted for clarity reasons.

**Source Code**

```
-- Additional Params: -t JavaScript
CREATE PROCEDURE ProcBetween
AS
BEGIN
declare @aValue int = 1;
IF(@aValue BETWEEN 1 AND 2)
   return 1
END;
GO
```

Copy

**Code Expected**

```
CREATE OR REPLACE PROCEDURE ProcBetween ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
   // SnowConvert AI Helpers Code section is omitted.

   let AVALUE = 1;
   if (SELECT(`   ? BETWEEN 1 AND 2`,[AVALUE])) {
      return 1;
   }
$$;
```

Copy

## BULK INSERT[¶](#bulk-insert "Link to this heading")

Translation reference for the Bulk Insert statement.

Applies to

* SQL Server
* Azure Synapse Analytics

Some parts in the output code are omitted for clarity reasons.

The direct translation for [BULK INSERT](https://docs.microsoft.com/en-us/sql/t-sql/statements/bulk-insert-transact-sql?view=sql-server-ver15) is the Snowflake [COPY INTO](https://docs.snowflake.com/en/sql-reference/sql/copy-into-table.html) statement. The `COPY INTO` does not use directly the file path to retrieve the values. The file should exist before in a [STAGE](https://docs.snowflake.com/en/sql-reference/sql/create-stage.html). Also the options used in the `BULK INSERT` should be specified in a Snowflake [FILE FORMAT](https://docs.snowflake.com/en/sql-reference/sql/create-file-format.html) that will be consumed by the `STAGE` or directly by the `COPY INTO`.

To add a file to some `STAGE` you should use the [PUT](https://docs.snowflake.com/en/sql-reference/sql/put.html) command. Notice that the command can be executed only from the [SnowSQL CLI](https://docs.snowflake.com/en/user-guide/snowsql.html). Here is an example of the steps we should do before executing a `COPY INTO`:

### SQL Server[¶](#sql-server "Link to this heading")

```
-- Additional Params: -t JavaScript
CREATE PROCEDURE PROCEDURE_SAMPLE
AS

CREATE TABLE #temptable  
 ([col1] varchar(100),  
  [col2] int,  
  [col3] varchar(100))  

BULK INSERT #temptable FROM 'C:\test.txt'  
WITH   
(  
   FIELDTERMINATOR ='\t',  
   ROWTERMINATOR ='\n'
); 

GO
```

Copy

### Snowflake[¶](#snowflake "Link to this heading")

```
CREATE OR REPLACE FILE FORMAT FILE_FORMAT_638434968243607970
FIELD_DELIMITER = '\t'
RECORD_DELIMITER = '\n';

CREATE OR REPLACE STAGE STAGE_638434968243607970
FILE_FORMAT = FILE_FORMAT_638434968243607970;

--** SSC-FDM-TS0004 - PUT STATEMENT IS NOT SUPPORTED ON WEB UI. YOU SHOULD EXECUTE THE CODE THROUGH THE SNOWFLAKE CLI **
PUT file://C:\test.txt @STAGE_638434968243607970 AUTO_COMPRESS = FALSE;

CREATE OR REPLACE PROCEDURE PROCEDURE_SAMPLE ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
 // SnowConvert AI Helpers Code section is omitted.

 EXEC(`CREATE OR REPLACE TEMPORARY TABLE T_temptable
(
   col1 VARCHAR(100),
   col2 INT,
   col3 VARCHAR(100))`);
 EXEC(`COPY INTO T_temptable FROM @STAGE_638434968243607970/test.txt`);
$$
```

Copy

As you see in the code above, SnowConvert AI identifies all the `BULK INSERTS` in the code, and for each instance, a new `STAGE` and `FILE FORMAT` will be created before the copy into execution. In addition, after the creation of the `STAGE`, a `PUT` command will be created as well in order to add the file to the stage.

The names of the generated statements are auto-generated using the current timestamp in seconds, in order to avoid collisions between their usages.

Finally, all the options for the bulk insert are being mapped to file format options if apply. If the option is not supported in Snowflake, it will be commented and a warning will be added. See also [SSC-FDM-TS0004](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/sqlServerFDM.html#ssc-fdm-ts0004).

#### Supported bulk options[¶](#supported-bulk-options "Link to this heading")

| SQL Server | Snowflake |
| --- | --- |
| FORMAT | TYPE |
| FIELDTERMINATOR | FIELD\_DELIMITER |
| FIRSTROW | SKIP\_HEADER |
| ROWTERMINATOR | RECORD\_DELIMITER |
| FIELDQUOTE | FIELD\_OPTIONALLY\_ENCLOSED\_BY |

### Related EWIs[¶](#related-ewis "Link to this heading")

1. [SSC-FDM-TS0004](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/sqlServerFDM.html#ssc-fdm-ts0004): PUT STATEMENT IS NOT SUPPORTED ON WEB UI.

## Common Table Expression (CTE)[¶](#common-table-expression-cte "Link to this heading")

Applies to

* SQL Server
* Azure Synapse Analytics

Some parts in the output code are omitted for clarity reasons.

Common table expressions are supported in Snowflake SQL by default.

### Syntax[¶](#syntax "Link to this heading")

#### Snowflake SQL[¶](#snowflake-sql "Link to this heading")

Subquery:

```
[ WITH
       <cte_name1> [ ( <cte_column_list> ) ] AS ( SELECT ...  )
   [ , <cte_name2> [ ( <cte_column_list> ) ] AS ( SELECT ...  ) ]
   [ , <cte_nameN> [ ( <cte_column_list> ) ] AS ( SELECT ...  ) ]
]
SELECT ...
```

Copy

Recursive CTE:

```
[ WITH [ RECURSIVE ]
       <cte_name1> ( <cte_column_list> ) AS ( anchorClause UNION ALL recursiveClause )
   [ , <cte_name2> ( <cte_column_list> ) AS ( anchorClause UNION ALL recursiveClause ) ]
   [ , <cte_nameN> ( <cte_column_list> ) AS ( anchorClause UNION ALL recursiveClause ) ]
]
SELECT ...
```

Copy

Where:

```
anchorClause ::=
    SELECT <anchor_column_list> FROM ...

 recursiveClause ::=
     SELECT <recursive_column_list> FROM ... [ JOIN ... ]
```

Copy

#### Noteworthy details[¶](#noteworthy-details "Link to this heading")

The RECURSIVE keyword does not exist in T-SQL, and the transformation does not actively add the keyword to the result. A warning is added to the output code in order to state this behavior.

#### Common Table Expression with SELECT INTO[¶](#common-table-expression-with-select-into "Link to this heading")

The following transformation occurs when the WITH expression is followed by an SELECT INTO statement and it will be transformed into a [TEMPORARY TABLE](https://docs.snowflake.com/en/user-guide/tables-temp-transient.html).

#### SQL Server:[¶](#id1 "Link to this heading")

```
WITH ctetable(col1, col2) AS
    (
        SELECT	col1, col2 FROM	t1 poh WHERE poh.col1 = 16 and poh.col2 = 4
    ),
    employeeCte AS
    (
	SELECT BUSINESSENTITYID, VACATIONHOURS FROM employee WHERE BUSINESSENTITYID = (SELECT col1 FROM ctetable)
    ),
    finalCte AS
    (
        SELECT BUSINESSENTITYID, VACATIONHOURS FROM employeeCte  
    ) SELECT * INTO #table2 FROM finalCte;

SELECT * FROM #table2;
```

Copy

#### Snowflake:[¶](#id2 "Link to this heading")

```
CREATE OR REPLACE TEMPORARY TABLE T_table2 AS
	WITH ctetable (
		col1,
		col2
	) AS
		   (
		       SELECT
		   		col1,
		   		col2
		       FROM
		   		t1 poh
		       WHERE
		   		poh.col1 = 16 and poh.col2 = 4
		   ),
		   		employeeCte AS
		   		    (
		   			SELECT
		   		BUSINESSENTITYID,
		   		VACATIONHOURS
		       FROM
		   		employee
		       WHERE
		   		BUSINESSENTITYID = (SELECT
		   						col1
		   					FROM
		   						ctetable
		   		)
		   		    ),
		   		finalCte AS
		   		    (
		   		        SELECT
		   		BUSINESSENTITYID,
		   		VACATIONHOURS
		       FROM
		   		employeeCte
		   		    )
		   		SELECT
		       *
		       FROM
		       finalCte;

		       SELECT
		       *
		       FROM
		       T_table2;
```

Copy

#### Common Table Expression with other expressions[¶](#common-table-expression-with-other-expressions "Link to this heading")

The following transformation occurs when the WITH expression is followed by INSERT or DELETE statements.

#### SQL Server:[¶](#id3 "Link to this heading")

```
WITH CTE AS( SELECT * from table1)
INSERT INTO Table2 (a,b,c,d)
SELECT a,b,c,d
FROM CTE
WHERE e IS NOT NULL;
```

Copy

#### Snowflake:[¶](#id4 "Link to this heading")

```
INSERT INTO Table2 (a, b, c, d)
WITH CTE AS( SELECT
*
from
table1
)
SELECT
a,
b,
c,
d
FROM
CTE AS CTE
WHERE
e IS NOT NULL;
```

Copy

#### Common Table Expression with Delete From[¶](#common-table-expression-with-delete-from "Link to this heading")

For this transformation, it will only apply for a CTE (Common Table Expression) with a Delete From, however, only for some specifics CTE. It must have only one CTE, and it must have inside a function of ROW\_NUMBER or RANK.

The purpose of the CTE with the Delete must be to remove duplicates from a table. In case that the CTE with Delete intents to remove another kind of data, this transformation will not apply.

Let’s see an example. For a working example, we must first create a table with some data.

```
CREATE TABLE WithQueryTest
(
    ID BIGINT,
    Value BIGINT,
    StringValue NVARCHAR(258)
);

Insert into WithQueryTest values(100, 100, 'First');
Insert into WithQueryTest values(200, 200, 'Second');
Insert into WithQueryTest values(300, 300, 'Third');
Insert into WithQueryTest values(400, 400, 'Fourth');
Insert into WithQueryTest values(100, 100, 'First');
```

Copy

Note that there is a duplicated value. The lines 8 and 12 insert the same value. Now we are going to eliminate the duplicates rows in a table.

```
WITH Duplicated AS (
SELECT *, ROW_NUMBER() OVER (PARTITION BY ID ORDER BY ID) AS RN
FROM WithQueryTest
)
DELETE FROM Duplicated
WHERE Duplicated.RN > 1
```

Copy

If we execute a Select from the table, it will show the following result

| ID | Value | StringValue |
| --- | --- | --- |
| 100 | 100 | First |
| 200 | 200 | Second |
| 300 | 300 | Third |
| 400 | 400 | Fourth |

Note that there are no duplicateds rows. In order to conserve the functionality of these CTE with Delete in Snowflake, it will be transformed to

```
CREATE OR REPLACE TABLE PUBLIC.WithQueryTest AS SELECT
*
FROM PUBLIC.WithQueryTest
QUALIFY ROW_NUMBER()
OVER (PARTITION BY ID ORDER BY ID) = 1 ;
```

Copy

As you can see, the query is transformed to a Create Or Replace Table.

Let’s try it in Snowflake, in order to test it, we need the table too.

```
CREATE OR REPLACE TABLE PUBLIC.WithQueryTest
(
ID BIGINT,
Value BIGINT,
StringValue VARCHAR(258)
);

Insert into PUBLIC.WithQueryTest values(100, 100, 'First');
Insert into PUBLIC.WithQueryTest values(200, 200, 'Second');
Insert into PUBLIC.WithQueryTest values(300, 300, 'Third');
Insert into PUBLIC.WithQueryTest values(400, 400, 'Fourth');
Insert into PUBLIC.WithQueryTest values(100, 100, 'First');
```

Copy

Now, if we execute the result of the transformation, and then a Select to check if the duplicated rows were deleted, this would be the result.

| ID | Value | StringValue |
| --- | --- | --- |
| 100 | 100 | First |
| 200 | 200 | Second |
| 300 | 300 | Third |
| 400 | 400 | Fourth |

#### Common Table Expression with MERGE statement[¶](#common-table-expression-with-merge-statement "Link to this heading")

The following transformation occurs when the WITH expression is followed by MERGE statement and it will be transformed into a [MERGE INTO](https://docs.snowflake.com/en/sql-reference/sql/merge.html).

##### SQL Server:[¶](#id5 "Link to this heading")

```
WITH ctetable(col1, col2) as 
    (
        SELECT col1, col2
        FROM t1 poh
        where poh.col1 = 16 and poh.col2 = 88
    ),
    finalCte As
    (
        SELECT col1 FROM ctetable  
    )  
    MERGE  
  table1 AS target
  USING finalCte AS source  
  ON (target.ID = source.COL1)
  WHEN MATCHED THEN UPDATE SET target.ID = source.Col1
  WHEN NOT MATCHED THEN INSERT (ID, col1) VALUES (source.COL1, source.COL1 );
```

Copy

##### Snowflake:[¶](#id6 "Link to this heading")

```
MERGE INTO table1 AS target
USING (
  --** SSC-PRF-TS0001 - PERFORMANCE WARNING - RECURSION FOR CTE NOT CHECKED. MIGHT REQUIRE RECURSIVE KEYWORD **
  WITH ctetable (
    col1,
    col2
  ) as
       (
           SELECT
           col1,
           col2
           FROM
           t1 poh
           where
           poh.col1 = 16 and poh.col2 = 88
       ),
           finalCte As
               (
                   SELECT
           col1
           FROM
           ctetable
               )
           SELECT
           *
           FROM
           finalCte
) AS source
ON (target.ID = source.COL1)
WHEN MATCHED THEN
           UPDATE SET
           target.ID = source.Col1
WHEN NOT MATCHED THEN
           INSERT (ID, col1) VALUES (source.COL1, source.COL1);
```

Copy

#### Common Table Expression with UPDATE statement[¶](#common-table-expression-with-update-statement "Link to this heading")

The following transformation occurs when the WITH expression is followed by an UPDATE statement and it will be transformed into an [UPDATE](https://docs.snowflake.com/en/sql-reference/sql/update.html) statement.

##### SQL Server:[¶](#id7 "Link to this heading")

```
WITH ctetable(col1, col2) AS 
    (
        SELECT col1, col2
        FROM table2 poh
        WHERE poh.col1 = 5 and poh.col2 = 4
    )
UPDATE tab1
SET ID = 8, COL1 = 8
FROM table1 tab1
INNER JOIN ctetable CTE ON tab1.ID = CTE.col1;
```

Copy

##### Snowflake:[¶](#id8 "Link to this heading")

```
UPDATE dbo.table1 tab1
    SET
        ID = 8,
        COL1 = 8
    FROM
        (
            WITH ctetable (
                col1,
                col2
            ) AS
                   (
                       SELECT
                           col1,
                           col2
                       FROM
                           table2 poh
                       WHERE
                           poh.col1 = 5 and poh.col2 = 4
                   )
                   SELECT
                       *
                   FROM
                       ctetable
        ) AS CTE
    WHERE
        tab1.ID = CTE.col1;
```

Copy

### Known Issues[¶](#known-issues "Link to this heading")

No issues were found.

### Related EWIs[¶](#id9 "Link to this heading")

1. [SSC-EWI-0108](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0108): The following subquery matches at least one of the patterns considered invalid and may produce compilation errors.
2. [SSC-PRF-TS0001](../../general/technical-documentation/issues-and-troubleshooting/performance-review/sqlServerPRF.html#ssc-prf-ts0001): Performance warning - recursion for CTE not checked. Might require a recursive keyword.

## DELETE[¶](#delete "Link to this heading")

Translation reference for Transact-SQL Delete statement to Snowflake

Applies to

* SQL Server
* Azure Synapse Analytics

Note

Some parts in the output code are omitted for clarity reasons.

### Description[¶](#description "Link to this heading")

Removes one or more rows from a table or view in SQL Server. For more information regarding SQL Server Delete, check [here](https://docs.microsoft.com/en-us/sql/t-sql/statements/delete-transact-sql?view=sql-server-ver15).

```
 [ WITH <common_table_expression> [ ,...n ] ]  
DELETE   
    [ TOP ( expression ) [ PERCENT ] ]   
    [ FROM ]   
    { { table_alias  
      | <object>   
      | rowset_function_limited   
      [ WITH ( table_hint_limited [ ...n ] ) ] }   
      | @table_variable  
    }  
    [ <OUTPUT Clause> ]  
    [ FROM table_source [ ,...n ] ]   
    [ WHERE { <search_condition>   
            | { [ CURRENT OF   
                   { { [ GLOBAL ] cursor_name }   
                       | cursor_variable_name   
                   }   
                ]  
              }  
            }   
    ]   
    [ OPTION ( <Query Hint> [ ,...n ] ) ]   
[; ]  
  
<object> ::=  
{   
    [ server_name.database_name.schema_name.   
      | database_name. [ schema_name ] .   
      | schema_name.  
    ]  
    table_or_view_name   
}
```

Copy

### Sample Source Patterns[¶](#sample-source-patterns "Link to this heading")

#### Sample Data[¶](#sample-data "Link to this heading")

##### SQL Server[¶](#id10 "Link to this heading")

```
CREATE TABLE Employees (
    EmployeeID INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    DepartmentID INT
);

CREATE TABLE Departments (
    DepartmentID INT PRIMARY KEY,
    DepartmentName VARCHAR(50)
);

INSERT INTO Employees (EmployeeID, FirstName, LastName, DepartmentID) VALUES
(1, 'John', 'Doe', 1),
(2, 'Jane', 'Smith', 2),
(3, 'Bob', 'Johnson', 1),
(4, 'Alice', 'Brown', 3),
(5, 'Michael', 'Davis', NULL);

INSERT INTO Departments (DepartmentID, DepartmentName) VALUES
(1, 'Sales'),
(2, 'Marketing'),
(3, 'Engineering'),
(4, 'Finance');
```

Copy

##### Snowflake[¶](#id11 "Link to this heading")

```
CREATE OR REPLACE TABLE Employees (
    EmployeeID INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    DepartmentID INT
);

CREATE OR REPLACE TABLE Departments (
    DepartmentID INT PRIMARY KEY,
    DepartmentName VARCHAR(50)
);

INSERT INTO Employees (EmployeeID, FirstName, LastName, DepartmentID) VALUES
(1, 'John', 'Doe', 1),
(2, 'Jane', 'Smith', 2),
(3, 'Bob', 'Johnson', 1),
(4, 'Alice', 'Brown', 3),
(5, 'Michael', 'Davis', NULL);

INSERT INTO Departments (DepartmentID, DepartmentName) VALUES
(1, 'Sales'),
(2, 'Marketing'),
(3, 'Engineering'),
(4, 'Finance');
```

Copy

#### Basic Case[¶](#basic-case "Link to this heading")

The transformation for the DELETE statement is fairly straightforward, with some caveats. One of these caveats is the way Snowflake supports multiple sources in the FROM clause, however, there is an equivalent in Snowflake as shown below.

##### SQL Server[¶](#id12 "Link to this heading")

```
 DELETE T1 FROM Departments T2, Employees T1 WHERE T1.DepartmentID = T2.DepartmentID
```

Copy

##### Snowflake[¶](#id13 "Link to this heading")

```
DELETE FROM
Employees T1
USING Departments T2
WHERE
T1.DepartmentID = T2.DepartmentID;
```

Copy

Note

Note that, since the original DELETE was for T1, the presence of TABLE2 T2 in the FROM clause requires the creation of the USING clause.

#### Delete duplicates from a table[¶](#delete-duplicates-from-a-table "Link to this heading")

The following documentation explains a [common pattern used to remove duplicated rows from a table in SQL Server](https://learn.microsoft.com/en-us/troubleshoot/sql/database-engine/development/remove-duplicate-rows-sql-server-tab#method-2). This approach uses the `ROW_NUMBER` function to partition the data based on the `key_value` which may be one or more columns separated by commas. Then, delete all records that received a row number value that is greater than 1. This value indicates that the records are duplicates. You can read the referenced documentation to understand the behavior of this method and recreate it.

```
DELETE T
FROM
(
SELECT *
, DupRank = ROW_NUMBER() OVER (
              PARTITION BY key_value
              ORDER BY ( {expression} )
            )
FROM original_table
) AS T
WHERE DupRank > 1
```

Copy

The following example uses this approach to remove duplicates from a table and its equivalent in Snowflake. The transformation consists of performing an [INSERT OVERWRITE](https://docs.snowflake.com/en/sql-reference/sql/insert#optional-parameters) statement which truncates the table (removes all data) and then inserts again the rows in the same table ignoring the duplicated ones. The output code is generated considering the same `PARTITION BY` and `ORDER BY` clauses used in the original code.

##### SQL Server[¶](#id14 "Link to this heading")

Create a table with duplicated rows

##### Insert duplicates[¶](#insert-duplicates "Link to this heading")

```
 create table duplicatedRows(
    someID int,
    col2 bit,
    col3 bit,
    col4 bit,
    col5 bit
);

insert into duplicatedRows VALUES(10, 1, 0, 0, 1);
insert into duplicatedRows VALUES(10, 1, 0, 0, 1);
insert into duplicatedRows VALUES(11, 1, 1, 0, 1);
insert into duplicatedRows VALUES(12, 0, 0, 1, 1);
insert into duplicatedRows VALUES(12, 0, 0, 1, 1);
insert into duplicatedRows VALUES(13, 1, 0, 1, 0);
insert into duplicatedRows VALUES(14, 1, 0, 1, 0);
insert into duplicatedRows VALUES(14, 1, 0, 1, 0);

select * from duplicatedRows;
```

Copy

##### Output[¶](#output "Link to this heading")

| someID | col2 | col3 | col4 | col5 |
| --- | --- | --- | --- | --- |
| 10 | true | false | false | true |
| 10 | true | false | false | true |
| 11 | true | true | false | true |
| 12 | false | false | true | true |
| 12 | false | false | true | true |
| 13 | true | false | true | false |
| 14 | true | false | true | false |
| 14 | true | false | true | false |

##### Remove duplicates[¶](#remove-duplicates "Link to this heading")

```
 DELETE f FROM (
	select  someID, row_number() over (
		partition by someID, col2
		order by
			case when COL3 = 1 then 1 else 0 end
			+ case when col4 = 1 then 1 else 0 end
			+ case when col5 = 1 then 1 else 0 end
			asc
		) as rownum
	from
		duplicatedRows
	) f where f.rownum > 1;
	
select * from duplicatedRows;
```

Copy

##### Output[¶](#id15 "Link to this heading")

| someID | col2 | col3 | col4 | col5 |
| --- | --- | --- | --- | --- |
| 10 | true | false | false | true |
| 11 | true | true | false | true |
| 12 | false | false | true | true |
| 13 | true | false | true | false |
| 14 | true | false | true | false |

##### Snowflake[¶](#id16 "Link to this heading")

Create a table with duplicated rows

##### Insert duplicates[¶](#id17 "Link to this heading")

```
 create table duplicatedRows(
    someID int,
    col2 BOOLEAN,
    col3 BOOLEAN,
    col4 BOOLEAN,
    col5 BOOLEAN
);

insert into duplicatedRows VALUES(10, 1, 0, 0, 1);
insert into duplicatedRows VALUES(10, 1, 0, 0, 1);
insert into duplicatedRows VALUES(11, 1, 1, 0, 1);
insert into duplicatedRows VALUES(12, 0, 0, 1, 1);
insert into duplicatedRows VALUES(12, 0, 0, 1, 1);
insert into duplicatedRows VALUES(13, 1, 0, 1, 0);
insert into duplicatedRows VALUES(14, 1, 0, 1, 0);
insert into duplicatedRows VALUES(14, 1, 0, 1, 0);

select * from duplicatedRows;
```

Copy

##### Output[¶](#id18 "Link to this heading")

| someID | col2 | col3 | col4 | col5 |
| --- | --- | --- | --- | --- |
| 10 | true | false | false | true |
| 10 | true | false | false | true |
| 11 | true | true | false | true |
| 12 | false | false | true | true |
| 12 | false | false | true | true |
| 13 | true | false | true | false |
| 14 | true | false | true | false |
| 14 | true | false | true | false |

##### Remove duplicates[¶](#id19 "Link to this heading")

```
   insert overwrite into duplicatedRows
            SELECT
                *
            FROM
                duplicatedRows
            QUALIFY
                ROW_NUMBER()
                over
                (partition by someID, col2
		    order by
			case when COL3 = 1 then 1 else 0 end
			+ case when col4 = 1 then 1 else 0 end
			+ case when col5 = 1 then 1 else 0 end
			asc) = 1;
	
select * from duplicatedRows;
```

Copy

##### Output[¶](#id20 "Link to this heading")

| someID | col2 | col3 | col4 | col5 |
| --- | --- | --- | --- | --- |
| 10 | true | false | false | true |
| 11 | true | true | false | true |
| 12 | false | false | true | true |
| 13 | true | false | true | false |
| 14 | true | false | true | false |

Warning

Consider that there may be several variations of this pattern, but all of them are based on the same principle and have the same structure.

#### DELETE WITH INNER JOIN[¶](#delete-with-inner-join "Link to this heading")

##### SQL SERVER[¶](#id21 "Link to this heading")

```
DELETE ee
FROM Employees ee INNER JOIN Departments dept
ON ee.DepartmentID = dept.DepartmentID;

SELECT * FROM Employees;
```

Copy

#### Output[¶](#id22 "Link to this heading")

| EmployeeID | FirstName | LastName | DepartmentID |
| --- | --- | --- | --- |
| 5 | Michael | Davis | null |
| 6 | Lucas | Parker | 8 |

##### Snowflake[¶](#id23 "Link to this heading")

```
DELETE FROM
    Employees ee
USING Departments dept
WHERE
    ee.DepartmentID = dept.DepartmentID;

SELECT
    *
FROM
    Employees;
```

Copy

##### Output[¶](#id24 "Link to this heading")

| EmployeeID | FirstName | LastName | DepartmentID |
| --- | --- | --- | --- |
| 5 | Michael | Davis | null |
| 6 | Lucas | Parker | 8 |

#### DELETE WITH LEFT JOIN[¶](#delete-with-left-join "Link to this heading")

##### SQL Server[¶](#id25 "Link to this heading")

```
DELETE Employees
FROM Employees LEFT JOIN Departments
ON Employees.DepartmentID = Departments.DepartmentID
WHERE Departments.DepartmentID IS NULL;

SELECT * FROM Employees;
```

Copy

##### Output[¶](#id26 "Link to this heading")

| EmployeeID | FirstName | LastName | DepartmentID |
| --- | --- | --- | --- |
| 1 | John | Doe | 1 |
| 2 | Jane | Smith | 2 |
| 3 | Bob | Johnson | 1 |
| 4 | Alice | Brown | 3 |

##### Snowflake[¶](#id27 "Link to this heading")

```
DELETE FROM
    Employees
USING Departments
WHERE
    Departments.DepartmentID IS NULL
    AND Employees.DepartmentID = Departments.DepartmentID(+);

SELECT
    *
FROM
    Employees;
```

Copy

##### Output[¶](#id28 "Link to this heading")

| EmployeeID | FirstName | LastName | DepartmentID |
| --- | --- | --- | --- |
| 1 | John | Doe | 1 |
| 2 | Jane | Smith | 2 |
| 3 | Bob | Johnson | 1 |
| 4 | Alice | Brown | 3 |

#### DELETE WITH RIGHT JOIN[¶](#delete-with-right-join "Link to this heading")

##### SQL SERVER[¶](#id29 "Link to this heading")

```
DELETE Employees
FROM Employees RIGHT JOIN Departments
ON Employees.DepartmentID = Departments.DepartmentID
WHERE Employees.DepartmentID IS NOT NULL;

SELECT * FROM Employees;
```

Copy

##### Output[¶](#id30 "Link to this heading")

| EmployeeID | FirstName | LastName | DepartmentID |
| --- | --- | --- | --- |
| 5 | Michael | Davis | null |
| 6 | Lucas | Parker | 8 |

##### Snowflake[¶](#id31 "Link to this heading")

```
DELETE FROM
    Employees
USING Departments
WHERE
    Employees.DepartmentID IS NOT NULL
    AND Employees.DepartmentID(+) = Departments.DepartmentID;

SELECT
    *
FROM
    Employees;
```

Copy

##### Output[¶](#id32 "Link to this heading")

| EmployeeID | FirstName | LastName | DepartmentID |
| --- | --- | --- | --- |
| 5 | Michael | Davis | null |
| 6 | Lucas | Parker | 8 |

### Known Issues[¶](#id33 "Link to this heading")

1. **FULL JOIN not supported**  
   The FULL JOIN can not be represented using the (+) syntax. When found, SnowConvert AI will warn the user about this with an FDM.

#### SQL Server[¶](#id34 "Link to this heading")

```
DELETE Employees
FROM Employees FULL OUTER JOIN Departments
ON Employees.DepartmentID = Departments.DepartmentID
WHERE Departments.DepartmentID IS NULL;
```

Copy

##### Snowflake[¶](#id35 "Link to this heading")

```
 !!!RESOLVE EWI!!! /*** SSC-EWI-TS0081 - USING A FULL JOIN IN A DELETE STATEMENT IS NOT SUPPORTED ***/!!!
DELETE FROM
    Employees
USING Departments
WHERE
    Departments.DepartmentID IS NULL
    AND Employees.DepartmentID = Departments.DepartmentID;
```

Copy

### Related EWIs[¶](#id36 "Link to this heading")

1. [SSC-EWI-TS0081](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/sqlServerEWI.html#ssc-ewi-ts0081): Using a full join in a delete statement is not supported

## DROP STATEMENT[¶](#drop-statement "Link to this heading")

DROP statements

Applies to

* SQL Server
* Azure Synapse Analytics

Some parts in the output code are omitted for clarity reasons.

### DROP TABLE[¶](#drop-table "Link to this heading")

#### Transact-SQL[¶](#transact-sql "Link to this heading")

```
DROP TABLE [ IF EXISTS ] <table_name> [ ,...n ]  
[ ; ]
```

Copy

#### Snowflake[¶](#id37 "Link to this heading")

```
DROP TABLE [ IF EXISTS ] <name> [ CASCADE | RESTRICT ]
```

Copy

#### Translation[¶](#translation "Link to this heading")

Translation for single `DROP TABLE` statements is very straightforward. As long as there is only one table being dropped within the statement, it’s left as-is.

For example:

```
DROP TABLE IF EXISTS [table_name]
```

Copy

```
DROP TABLE IF EXISTS table_name;
```

Copy

The only noteworthy difference between SQL Server and Snowflake appears when the input statement drops more than one table. In these scenarios, a different `DROP TABLE` statement is created for each table being dropped.

For example:

##### SQL Server[¶](#id38 "Link to this heading")

```
DROP TABLE IF EXISTS [table_name], [table_name2], [table_name3]
```

Copy

##### Snowflake[¶](#id39 "Link to this heading")

```
DROP TABLE IF EXISTS table_name;

DROP TABLE IF EXISTS table_name2;

DROP TABLE IF EXISTS table_name3;
```

Copy

## EXISTS[¶](#exists "Link to this heading")

Transact-SQL subqueries using EXISTS statement transformation details

Applies to

* SQL Server
* Azure Synapse Analytics

Some parts in the output code are omitted for clarity reasons.

### Types of Subqueries[¶](#types-of-subqueries "Link to this heading")

Subqueries can be categorized as correlated or uncorrelated:

A correlated subquery, refers to one or more columns from outside of the subquery. (The columns are typically referenced inside the WHERE clause of the subquery.) A correlated subquery can be thought of as a filter on the table that it refers to, as if the subquery were evaluated on each row of the table in the outer query.

An uncorrelated subquery, has no such external column references. It is an independent query, the results of which are returned to and used by the outer query once (not per row).

The EXISTS statement is considered a correlated subquery.

#### SQL SERVER[¶](#id40 "Link to this heading")

```
-- Additional Params: -t JavaScript
CREATE PROCEDURE ProcExists
AS
BEGIN
IF(EXISTS(Select AValue from ATable))
  return 1;
END;
```

Copy

#### Snowflake[¶](#id41 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE ProcExists ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
  // SnowConvert AI Helpers Code section is omitted.

  if (SELECT(`   EXISTS(Select
         AValue
      from
         ATable
   )`)) {
    return 1;
  }
$$;
```

Copy

## IN[¶](#in "Link to this heading")

Transact-SQL subqueries using IN statement transformation details

Applies to

* SQL Server
* Azure Synapse Analytics

Some parts in the output code are omitted for clarity reasons.

The IN operator checks if an expression is included in the values returned by a subquery.

### SQL SERVER[¶](#id42 "Link to this heading")

```
-- Additional Params: -t JavaScript
CREATE PROCEDURE dbo.SP_IN_EXAMPLE
AS
	DECLARE @results as VARCHAR(50);

	SELECT @results = COUNT(*) FROM TABLE1

	IF @results IN (1,2,3)
		SELECT 'is IN';
	ELSE
		SELECT 'is NOT IN';
	
	return
GO

-- =============================================
-- Example to execute the stored procedure
-- =============================================
EXECUTE dbo.SP_IN_EXAMPLE
GO
```

Copy

### Snowflake[¶](#id43 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE dbo.SP_IN_EXAMPLE ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
	// SnowConvert AI Helpers Code section is omitted.

	let RESULTS;
	SELECT(`   COUNT(*) FROM
   TABLE1`,[],(value) => RESULTS = value);
	if ([1,2,3].includes(RESULTS)) {
	} else {
	}
	return;
$$;

-- =============================================
-- Example to execute the stored procedure
-- =============================================
CALL dbo.SP_IN_EXAMPLE();
```

Copy

## INSERT[¶](#insert "Link to this heading")

Translation reference for SQL Server Insert statement to Snowflake

Applies to

* SQL Server
* Azure Synapse Analytics

Some parts in the output code are omitted for clarity reasons.

### Description[¶](#id44 "Link to this heading")

Adds one or more rows to a table or a view in SQL Server. For more information regarding SQL Server Insert, check [here](https://docs.microsoft.com/en-us/sql/t-sql/statements/insert-transact-sql?view=sql-server-ver15).

#### Syntax comparison[¶](#syntax-comparison "Link to this heading")

The basic insert grammar is equivalent between both SQL languages. However there are still some other syntax elements in SQL Server that show differences, for example, one allows the developer to add a value to a column by using the assign operator. The syntax mentioned will be transformed to the basic insert syntax too.

##### Snowflake[¶](#id45 "Link to this heading")

```
INSERT [ OVERWRITE ] INTO <target_table> [ ( <target_col_name> [ , ... ] ) ]
       {
         VALUES ( { <value> | DEFAULT | NULL } [ , ... ] ) [ , ( ... ) ]  |
         <query>
       }
```

Copy

##### SQL Server[¶](#id46 "Link to this heading")

```
[ WITH <common_table_expression> [ ,...n ] ]  
INSERT   
{  
        [ TOP ( expression ) [ PERCENT ] ]   
        [ INTO ]   
        { <object> | rowset_function_limited   
          [ WITH ( <Table_Hint_Limited> [ ...n ] ) ]  
        }  
    {  
        [ ( column_list ) ]   
        [ <OUTPUT Clause> ]  
        { VALUES ( { DEFAULT | NULL | expression } [ ,...n ] ) [ ,...n     ]   
        | derived_table   
        | execute_statement  
        | <dml_table_source>  
        | DEFAULT VALUES   
        }  
    }  
}  
[;]  
  
<object> ::=  
{   
    [ server_name . database_name . schema_name .   
      | database_name .[ schema_name ] .   
      | schema_name .   
    ]  
  table_or_view_name  
}  
  
<dml_table_source> ::=  
    SELECT <select_list>  
    FROM ( <dml_statement_with_output_clause> )   
      [AS] table_alias [ ( column_alias [ ,...n ] ) ]  
    [ WHERE <search_condition> ]  
        [ OPTION ( <query_hint> [ ,...n ] ) ]
```

Copy

### Sample Source Patterns[¶](#id47 "Link to this heading")

#### Basic INSERT[¶](#basic-insert "Link to this heading")

##### SQL Server[¶](#id48 "Link to this heading")

```
INSERT INTO TABLE1 VALUES (1, 2, 123, 'LiteralValue');
```

Copy

##### Snowflake[¶](#id49 "Link to this heading")

```
INSERT INTO TABLE1 VALUES (1, 2, 123, 'LiteralValue');
```

Copy

#### INSERT with assing operator[¶](#insert-with-assing-operator "Link to this heading")

##### SQL Server[¶](#id50 "Link to this heading")

```
INSERT INTO aTable (columnA = 'varcharValue', columnB = 1);
```

Copy

##### Snowflake[¶](#id51 "Link to this heading")

```
INSERT INTO aTable (columnA = 'varcharValue', columnB = 1);
```

Copy

#### INSERT with no INTO[¶](#insert-with-no-into "Link to this heading")

##### SQL Server[¶](#id52 "Link to this heading")

```
INSERT exampleTable VALUES ('Hello', 23);
```

Copy

##### Snowflake[¶](#id53 "Link to this heading")

```
INSERT INTO exampleTable VALUES ('Hello', 23);
```

Copy

#### INSERT with common table expression[¶](#insert-with-common-table-expression "Link to this heading")

##### SQL Server[¶](#id54 "Link to this heading")

```
WITH ctevalues (textCol, numCol) AS (SELECT 'cte string', 155)
INSERT INTO exampleTable SELECT * FROM ctevalues;
```

Copy

##### Snowflake[¶](#id55 "Link to this heading")

```
INSERT INTO exampleTable
WITH ctevalues (
textCol,
numCol
) AS (SELECT 'cte string', 155)
SELECT
*
FROM
ctevalues AS ctevalues;
```

Copy

#### INSERT with Table DML Factor with MERGE as DML[¶](#insert-with-table-dml-factor-with-merge-as-dml "Link to this heading")

This case is so specific where the `INSERT` statement has a `SELECT` query, and the `FROM` clause of the `SELECT` mentioned contains a `MERGE` DML statement.
Looking for an equivalent in Snowflake, the next statements are created: a temporary table, [the merge statement converted](#merge), and finally, the insert statement.

##### SQL Server[¶](#id56 "Link to this heading")

```
INSERT INTO T3
SELECT
  col1,
  col2
FROM (
  MERGE T1 USING T2
  	ON T1.col1 = T2.col1
  WHEN NOT MATCHED THEN
    INSERT VALUES ( T2.col1, T2.col2 )
  WHEN MATCHED THEN
    UPDATE SET T1.col2 = t2.col2
  OUTPUT
  	$action ACTION_OUT,
    T2.col1,
    T2.col2
) AS MERGE_OUT
 WHERE ACTION_OUT='UPDATE';
```

Copy

##### Snowflake[¶](#id57 "Link to this heading")

```
--** SSC-FDM-TS0026 - DELETE CASE IS NOT BEING CONSIDERED, PLEASE CHECK IF THE ORIGINAL MERGE PERFORMS IT **
CREATE OR REPLACE TEMPORARY TABLE MERGE_OUT AS
SELECT
	CASE WHEN T1.$1 IS NULL THEN 'INSERT' ELSE 'UPDATE' END ACTION_OUT,
	T2.col1,
	T2.col2
FROM T2 LEFT JOIN T1 ON T1.col1 = T2.col1;

MERGE INTO T1
USING T2
ON T1.col1 = T2.col1
WHEN NOT MATCHED THEN INSERT VALUES (T2.col1, T2.col2)
WHEN MATCHED THEN UPDATE SET T1.col2 = t2.col2
!!!RESOLVE EWI!!! /*** SSC-EWI-0021 - OUTPUT CLAUSE NOT SUPPORTED IN SNOWFLAKE ***/!!!
OUTPUT
	$action ACTION_OUT,
	T2.col1,
	T2.col2 ;

INSERT INTO T3
SELECT col1, col2
FROM MERGE_OUT
WHERE ACTION_OUT ='UPDATE';
```

Copy

**NOTE:** As the pattern’s name suggests, it is ONLY for cases where the insert comes with a select…from which the body contains a MERGE statement.

### Known Issues[¶](#id58 "Link to this heading")

**1. Syntax elements that require special mappings:**

* [INTO]: This keyword is obligatory in Snowflake and should be added if not present.
* [DEFAULT VALUES]: Inserts the default value in all columns specified in the insert. Should be transformed to VALUES (DEFAULT, DEFAULT, …), the amount of DEFAULTs added equals the number of columns the insert will modify. For now, there is a warning being added.

#### SQL Server[¶](#id59 "Link to this heading")

```
INSERT INTO exampleTable DEFAULT VALUES;
```

Copy

#### Snowflake[¶](#id60 "Link to this heading")

```
!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'INSERT WITH DEFAULT VALUES' NODE ***/!!!
INSERT INTO exampleTable DEFAULT VALUES;
```

Copy

**2. Syntax elements not supported or irrelevant:**

* [TOP (expression) [PERCENT]]: Indicates the amount or percent of rows that will be inserted. Not supported.
* [rowset\_function\_limited]: It is either OPENQUERY() or OPENROWSET(), used to read data from remote servers. Not supported.
* [WITH table\_hint\_limited]: These are used to get reading/writing locks on tables. Not relevant in Snowflake.
* [<OUTPUT Clause>]: Specifies a table or result set in which the inserted rows will also be inserted. Not supported.
* [execute\_statement]: Can be used to run a query to get data from. Not supported.
* [dml\_table\_source]: A temporary result set generated by the OUTPUT clause of another DML statement. Not supported.

**3. The DELETE case is not being considered.**

* For the *INSERT with Table DML Factor with MERGE as DML* pattern, the DELETE case is not being considered in the solution, so if the source code merge statement has a DELETE case please consider that it might not work as expected.

### Related EWIs[¶](#id61 "Link to this heading")

1. [SSC-EWI-0073](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0073): Pending Functional Equivalence Review.
2. [SSC-FDM-TS0026](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/sqlServerFDM.html#ssc-fdm-ts0026): DELETE case is not being considered.

## MERGE[¶](#merge "Link to this heading")

Transact-SQL MERGE statement transformation details

Applies to

* SQL Server
* Azure Synapse Analytics

### Syntax comparison[¶](#id62 "Link to this heading")

#### Snowflake[¶](#id63 "Link to this heading")

```
MERGE
    INTO <target_table>
    USING <source>
    ON <join_expr>
    { matchedClause | notMatchedClause } [ ... ]
```

Copy

#### Transact-SQL[¶](#id64 "Link to this heading")

```
-- SQL Server and Azure SQL Database
[ WITH <common_table_expression> [,...n] ]  
MERGE
    [ TOP ( expression ) [ PERCENT ] ]
    [ INTO ] <target_table> [ WITH ( <merge_hint> ) ] [ [ AS ] table_alias ]  
    USING <table_source> [ [ AS ] table_alias ]
    ON <merge_search_condition>  
    [ WHEN MATCHED [ AND <clause_search_condition> ]  
        THEN <merge_matched> ] [ ...n ]  
    [ WHEN NOT MATCHED [ BY TARGET ] [ AND <clause_search_condition> ]  
        THEN <merge_not_matched> ]  
    [ WHEN NOT MATCHED BY SOURCE [ AND <clause_search_condition> ]  
        THEN <merge_matched> ] [ ...n ]  
    [ <output_clause> ]  
    [ OPTION ( <query_hint> [ ,...n ] ) ]
;
```

Copy

#### Example[¶](#example "Link to this heading")

Given the following source code:

##### SQL Server[¶](#id65 "Link to this heading")

```
MERGE
INTO
  targetTable WITH(KEEPIDENTITY, KEEPDEFAULTS, HOLDLOCK, IGNORE_CONSTRAINTS, IGNORE_TRIGGERS, NOLOCK, INDEX(value1, value2, value3)) as tableAlias
USING
  tableSource AS tableAlias2
ON
  mergeSetCondition > mergeSetCondition
WHEN MATCHED BY TARGET AND pi.Quantity - src.OrderQty >= 0
  THEN UPDATE SET pi.Quantity = pi.Quantity - src.OrderQty
OUTPUT $action, DELETED.v AS DELETED, INSERTED.v INSERTED INTO @localVar(col, list)
OPTION(RECOMPILE);
```

Copy

You can expect to get something like this:

##### Snowflake[¶](#id66 "Link to this heading")

```
MERGE INTO targetTable as tableAlias
USING tableSource AS tableAlias2
ON mergeSetCondition > mergeSetCondition
WHEN MATCHED AND pi.Quantity - src.OrderQty >= 0 THEN
  UPDATE SET
    pi.Quantity = pi.Quantity - src.OrderQty
    !!!RESOLVE EWI!!! /*** SSC-EWI-0021 - OUTPUT CLAUSE NOT SUPPORTED IN SNOWFLAKE ***/!!!
   OUTPUT $action, DELETED.v AS DELETED, INSERTED.v INSERTED INTO @localVar(col, list);
```

Copy

### Related EWIs[¶](#id67 "Link to this heading")

1. [SSC-EWI-0021](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0021): Syntax not supported in Snowflake.

## SELECT[¶](#select "Link to this heading")

Translation reference to convert SQL Server Select statement to Snowflake

Applies to

* SQL Server
* Azure Synapse Analytics

Some parts in the output code are omitted for clarity reasons.

### Description[¶](#id68 "Link to this heading")

Allows the selection of one or more rows or columns of one or more tables in SQL Server.
For more information regarding SQL Server Select, check [here](https://docs.microsoft.com/en-us/sql/t-sql/queries/select-transact-sql?view=sql-server-ver15).

```
<SELECT statement> ::=    
    [ WITH { [ XMLNAMESPACES ,] [ <common_table_expression> [,...n] ] } ]  
    <query_expression>   
    [ ORDER BY <order_by_expression> ] 
    [ <FOR Clause>]   
    [ OPTION ( <query_hint> [ ,...n ] ) ]   
<query_expression> ::=   
    { <query_specification> | ( <query_expression> ) }   
    [  { UNION [ ALL ] | EXCEPT | INTERSECT }  
        <query_specification> | ( <query_expression> ) [...n ] ]   
<query_specification> ::=   
SELECT [ ALL | DISTINCT ]   
    [TOP ( expression ) [PERCENT] [ WITH TIES ] ]   
    < select_list >   
    [ INTO new_table ]   
    [ FROM { <table_source> } [ ,...n ] ]   
    [ WHERE <search_condition> ]   
    [ <GROUP BY> ]   
    [ HAVING < search_condition > ]
```

Copy

### Sample Source Patterns[¶](#id69 "Link to this heading")

#### SELECT WITH COLUMN ALIASES[¶](#select-with-column-aliases "Link to this heading")

The following example demonstrates how to use column aliases in Snowflake. The first two columns, from the SQL Server code, are expected to be transformed from an assignment form into a normalized form using the `AS` keyword. The third and fourth columns are using valid Snowflake formats.

##### SQL Server[¶](#id70 "Link to this heading")

```
SELECT
    MyCol1Alias = COL1,
    MyCol2Alias = COL2,
    COL3 AS MyCol3Alias,
    COL4 MyCol4Alias
FROM TABLE1;
```

Copy

##### Snowflake[¶](#id71 "Link to this heading")

```
SELECT
    COL1 AS MyCol1Alias,
    COL2 AS MyCol2Alias,
    COL3 AS MyCol3Alias,
    COL4 MyCol4Alias
FROM
    TABLE1;
```

Copy

#### SELECT TOP[¶](#select-top "Link to this heading")

##### SQL Server[¶](#id72 "Link to this heading")

```
SELECT TOP 1 * from ATable;
```

Copy

##### Snowflake[¶](#id73 "Link to this heading")

```
SELECT TOP 1
*
from
ATable;
```

Copy

#### SELECT INTO[¶](#select-into "Link to this heading")

The following example shows the `SELECT INTO` is transformed into a `CREATE TABLE AS`, this is because in Snowflake there is no equivalent for
`SELECT INTO` and to create a table based on a query has to be with the `CREATE TABLE AS`.

##### SQL Server[¶](#id74 "Link to this heading")

```
SELECT * INTO NEWTABLE FROM TABLE1;
```

Copy

##### Snowflake[¶](#id75 "Link to this heading")

```
CREATE OR REPLACE TABLE NEWTABLE AS
SELECT
*
FROM
TABLE1;
```

Copy

Another case is when including set operators such as `EXCEPT` and `INTERSECT`. The transformation is basically the same as the previous one.

##### SQL Server[¶](#id76 "Link to this heading")

```
SELECT * INTO NEWTABLE FROM TABLE1
EXCEPT
SELECT * FROM TABLE2
INTERSECT
SELECT * FROM TABLE3;
```

Copy

##### Snowflake[¶](#id77 "Link to this heading")

```
CREATE OR REPLACE TABLE NEWTABLE AS
SELECT
*
FROM
TABLE1
EXCEPT
SELECT
*
FROM
TABLE2
INTERSECT
SELECT
*
FROM
TABLE3;
```

Copy

#### SELECT TOP Aditional Arguments[¶](#select-top-aditional-arguments "Link to this heading")

Since `PERCENT` and `WITH TIES` keywords affect the result, and they are not supported by Snowflake, they will be commented out and added as an error.

##### SQL Server[¶](#id78 "Link to this heading")

```
SELECT TOP 1 PERCENT * from ATable;
SELECT TOP 1 WITH TIES * from ATable;
SELECT TOP 1 PERCENT WITH TIES * from ATable;
```

Copy

##### Snowflake[¶](#id79 "Link to this heading")

```
SELECT
TOP 1 !!!RESOLVE EWI!!! /*** SSC-EWI-0040 - THE 'TOP PERCENT' CLAUSE IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
*
from
ATable;

SELECT
TOP 1 !!!RESOLVE EWI!!! /*** SSC-EWI-0040 - THE 'TOP WITH TIES' CLAUSE IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
*
from
ATable;

SELECT
TOP 1 !!!RESOLVE EWI!!! /*** SSC-EWI-0040 - THE 'TOP PERCENT AND WITH TIES' CLAUSE IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
*
from
ATable;
```

Copy

#### SELECT FOR[¶](#select-for "Link to this heading")

Since the `FOR` clause is not supported in Snowflake, it is commented out and added as an error during the transformation.

##### SQL Server[¶](#id80 "Link to this heading")

```
SELECT column1, column2 FROM my_table FOR XML PATH('');
```

Copy

##### Snowflake[¶](#id81 "Link to this heading")

```
SELECT
--** SSC-FDM-TS0016 - XML COLUMNS IN SNOWFLAKE MIGHT HAVE A DIFFERENT FORMAT **
FOR_XML_UDF(OBJECT_CONSTRUCT('column1', column1, 'column2', column2), '')
FROM
my_table;
```

Copy

#### SELECT OPTION[¶](#select-option "Link to this heading")

The `OPTION` clause is not supported by Snowflake. It will be commented out and added as a warning during the transformation.

Notice that the `OPTION` statement has been removed from transformation because it is not relevant or not needed in Snowflake.

##### SQL Server[¶](#id82 "Link to this heading")

```
SELECT column1, column2 FROM my_table OPTION (HASH GROUP, FAST 10);
```

Copy

##### Snowflake[¶](#id83 "Link to this heading")

```
SELECT
column1,
column2
FROM
my_table;
```

Copy

#### SELECT WITH[¶](#select-with "Link to this heading")

The `WITH` clause is not supported by Snowflake. It will be commented out and added as a warning during the transformation.

Notice that the `WITH(NOLOCK, NOWAIT)` statement has been removed from transformation because it is not relevant or not needed in Snowflake.

##### SQL Server[¶](#id84 "Link to this heading")

```
SELECT AValue from ATable WITH(NOLOCK, NOWAIT);
```

Copy

##### Snowflake[¶](#id85 "Link to this heading")

```
SELECT
AValue
from
ATable;
```

Copy

### Related EWIs[¶](#id86 "Link to this heading")

1. [SSC-EWI-0040](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0040): Statement Not Supported.
2. [SSC-FDM-TS0016](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/sqlServerFDM.html#ssc-fdm-ts0016): XML columns in Snowflake might have a different format

## SET OPERATORS[¶](#set-operators "Link to this heading")

Applies to

* SQL Server
* Azure Synapse Analytics

Set Operators in both TSQL and Snowflake present the same syntax and supported scenarios(EXCEPT, INTERSECT, UNION and UNION ALL), with the exception of the MINUS which is not supported in TSQL, resulting in the same code during conversion.

```
SELECT LastName, FirstName FROM employees
UNION ALL
SELECT FirstName, LastName FROM contractors;

SELECT ...
INTERSECT
SELECT ...

SELECT ...
EXCEPT
SELECT ...
```

Copy

## TRUNCATE[¶](#truncate "Link to this heading")

Transact-SQL TRUNCATE statement transformation details

Applies to

* SQL Server
* Azure Synapse Analytics

Some parts in the output code are omitted for clarity reasons.

### SQL Server[¶](#id87 "Link to this heading")

```
TRUNCATE TABLE TABLE1;
```

Copy

### Snowflake[¶](#id88 "Link to this heading")

```
TRUNCATE TABLE TABLE1;
```

Copy

## UPDATE[¶](#update "Link to this heading")

Translation reference to convert SQL Server Update statement to Snowflake

Applies to

* SQL Server
* Azure Synapse Analytics

Note

Some parts in the output code are omitted for clarity reasons.

### Description[¶](#id89 "Link to this heading")

Changes existing data in a table or view in SQL Server. For more information regarding SQL Server Update, check [here](https://docs.microsoft.com/en-us/sql/t-sql/queries/update-transact-sql?view=sql-server-ver15).

```
[ WITH <common_table_expression> [...n] ]  
UPDATE   
    [ TOP ( expression ) [ PERCENT ] ]   
    { { table_alias | <object> | rowset_function_limited   
         [ WITH ( <Table_Hint_Limited> [ ...n ] ) ]  
      }  
      | @table_variable      
    }  
    SET  
        { column_name = { expression | DEFAULT | NULL }  
          | { udt_column_name.{ { property_name = expression  
                                | field_name = expression }  
                                | method_name ( argument [ ,...n ] )  
                              }  
          }  
          | column_name { .WRITE ( expression , @Offset , @Length ) }  
          | @variable = expression  
          | @variable = column = expression  
          | column_name { += | -= | *= | /= | %= | &= | ^= | |= } expression  
          | @variable { += | -= | *= | /= | %= | &= | ^= | |= } expression  
          | @variable = column { += | -= | *= | /= | %= | &= | ^= | |= } expression  
        } [ ,...n ]   
  
    [ <OUTPUT Clause> ]  
    [ FROM{ <table_source> } [ ,...n ] ]   
    [ WHERE { <search_condition>   
            | { [ CURRENT OF   
                  { { [ GLOBAL ] cursor_name }   
                      | cursor_variable_name   
                  }   
                ]  
              }  
            }   
    ]   
    [ OPTION ( <query_hint> [ ,...n ] ) ]  
[ ; ]  
  
<object> ::=  
{   
    [ server_name . database_name . schema_name .   
    | database_name .[ schema_name ] .   
    | schema_name .  
    ]  
    table_or_view_name}
```

Copy

### Sample Source Patterns[¶](#id90 "Link to this heading")

### Basic UPDATE[¶](#basic-update "Link to this heading")

The conversion for a regular UPDATE statement is very straightforward. Since the basic UPDATE structure is supported by default in Snowflake,
the outliers are the parts where you are going to see some differences.

#### SQL Server[¶](#id91 "Link to this heading")

```
Update UpdateTest1
Set Col1 = 5;
```

Copy

#### Snowflake[¶](#id92 "Link to this heading")

```
Update UpdateTest1
Set
Col1 = 5;
```

Copy

### Cartesian Products[¶](#cartesian-products "Link to this heading")

SQL Server allows add circular references between the target table of the Update Statement and the FROM Clause/ In execution time, the database optimizer removes any cartesian product generated. Otherwise, Snowflake currently does not optimize this scenario, producing a cartesian product that can be checked in the Execution Plan.\

To resolve this, if there is a JOIN where one of their tables is the same as the update target, this reference is removed and added to the WHERE clause, and it is used to just filter the data and avoid making a set operation.

#### SQL Server[¶](#id93 "Link to this heading")

```
UPDATE [HumanResources].[EMPLOYEEDEPARTMENTHISTORY_COPY]
SET
	BusinessEntityID = b.BusinessEntityID ,
	DepartmentID = b.DepartmentID,
	ShiftID = b.ShiftID,
	StartDate = b.StartDate,
	EndDate = b.EndDate,
	ModifiedDate = b.ModifiedDate
	FROM [HumanResources].[EMPLOYEEDEPARTMENTHISTORY_COPY] AS a
	RIGHT OUTER JOIN [HumanResources].[EmployeeDepartmentHistory] AS b
	ON a.BusinessEntityID = b.BusinessEntityID and a.ShiftID = b.ShiftID;
```

Copy

#### Snowflake[¶](#id94 "Link to this heading")

```
UPDATE HumanResources.EMPLOYEEDEPARTMENTHISTORY_COPY a
	SET
		BusinessEntityID = b.BusinessEntityID,
		DepartmentID = b.DepartmentID,
		ShiftID = b.ShiftID,
		StartDate = b.StartDate,
		EndDate = b.EndDate,
		ModifiedDate = b.ModifiedDate
	FROM
		HumanResources.EmployeeDepartmentHistory AS b
	WHERE
		a.BusinessEntityID(+) = b.BusinessEntityID
		AND a.ShiftID(+) = b.ShiftID;
```

Copy

### OUTPUT clause[¶](#output-clause "Link to this heading")

The OUTPUT clause is not supported by Snowflake.

#### SQL Server[¶](#id95 "Link to this heading")

```
Update UpdateTest2
Set Col1 = 5
OUTPUT
	deleted.Col1,
	inserted.Col1
	into ValuesTest;
```

Copy

#### Snowflake[¶](#id96 "Link to this heading")

```
Update UpdateTest2
	Set
		Col1 = 5
!!!RESOLVE EWI!!! /*** SSC-EWI-0021 - OUTPUT CLAUSE NOT SUPPORTED IN SNOWFLAKE ***/!!!
OUTPUT
	deleted.Col1,
	inserted.Col1
	into ValuesTest;
```

Copy

### CTE[¶](#cte "Link to this heading")

The WITH CTE clause is moved to the internal query in the update statement to be supported by Snowflake.

#### SQL Server[¶](#id97 "Link to this heading")

```
With ut as (select * from UpdateTest3)
Update x
Set Col1 = 5 
from ut as x;
```

Copy

#### Snowflake[¶](#id98 "Link to this heading")

```
UPDATE UpdateTest3
Set
Col1 = 5
FROM
(
WITH ut as (select
*
from
UpdateTest3
)
SELECT
*
FROM
ut
) AS x;
```

Copy

### TOP clause[¶](#top-clause "Link to this heading")

The TOP clause is not supported by Snowflake.

#### SQL Server[¶](#id99 "Link to this heading")

```
Update TOP(10) UpdateTest4
Set Col1 = 5;
```

Copy

#### Snowflake[¶](#id100 "Link to this heading")

```
Update
--       !!!RESOLVE EWI!!! /*** SSC-EWI-0021 - TOP CLAUSE NOT SUPPORTED IN SNOWFLAKE ***/!!!
-- TOP(10)
         UpdateTest4
Set
Col1 = 5;
```

Copy

### WITH TABLE HINT LIMITED[¶](#with-table-hint-limited "Link to this heading")

The Update WITH clause in not supported by Snowflake.

#### SQL Server[¶](#id101 "Link to this heading")

```
Update UpdateTest5 WITH(TABLOCK)
Set Col1 = 5;
```

Copy

#### Snowflake[¶](#id102 "Link to this heading")

```
Update UpdateTest5
Set
Col1 = 5;
```

Copy

### Related EWIs[¶](#id103 "Link to this heading")

1. [SSC-EWI-0021](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0021): Syntax not supported in Snowflake.

## UPDATE WITH JOIN[¶](#update-with-join "Link to this heading")

Translation specification for UPDATE statement with WHERE and JOIN clauses

Warning

*This is a work in progress and may change in the future.*

### Description[¶](#id104 "Link to this heading")

The pattern UPDATE FROM is used to update data based on data from other tables. This [SQLServer documentation](https://learn.microsoft.com/en-us/sql/t-sql/queries/update-transact-sql?view=sql-server-ver16#OtherTables) provides a simple sample.

Review the following SQL Server syntax from the [documentation](https://learn.microsoft.com/en-us/sql/t-sql/queries/update-transact-sql?view=sql-server-ver16#UpdateExamples).

#### SQL Server Syntax[¶](#sql-server-syntax "Link to this heading")

```
UPDATE [table_name] 
SET column_name = expression [, ...]
[FROM <table_source> [, ...]]
[WHERE <search_condition>]
[OPTION (query_hint)]
```

Copy

* **`table_name`**: The table or view you are updating.
* **`SET`**: Specifies the columns and their new values. The `SET` clause assigns a new value (or expression) to one or more columns.
* **`FROM`**: Used to specify one or more source tables (*like a **join**)*. It helps define where the data comes from to perform the update.
* **`WHERE`**: Specifies which rows should be updated based on the condition(s). Without this clause, all rows in the table would be updated.
* **`OPTION (query_hint)`**: Specifies hints for query optimization.

##### Snowflake syntax[¶](#snowflake-syntax "Link to this heading")

The Snowflake syntax can also be reviewed in the [Snowflake documentation](https://docs.snowflake.com/en/sql-reference/sql/update).

Note

Snowflake does not support `JOINs` in `UPDATE` clause.

```
 UPDATE <target_table>
       SET <col_name> = <value> [ , <col_name> = <value> , ... ]
        [ FROM <additional_tables> ]
        [ WHERE <condition> ]
```

Copy

**Required parameters**

* ***`target_table:`***Specifies the table to update.
* ***`col_name:`***Specifies the name of a column in *`target_table`*. Do not include the table name. E.g., `UPDATE t1 SET t1.col = 1` is invalid.
* ***`value`**`:`*Specifies the new value to set in *`col_name`*.

**Optional parameters**

* **``` FROM`` ```** ***`additional_tables:`*** Specifies one or more tables to use for selecting rows to update or for setting new values. *Note that repeating the target table results in a self-join.*
* **``` WHERE`` ```** ***`condition:`***The expression that specifies the rows in the target table to update. Default: No value (all rows of the target table are updated)

#### Translation Summary[¶](#translation-summary "Link to this heading")

| SQL Server JOIN type | Snowflake Best Alternative |
| --- | --- |
| Single `INNER JOIN` | Use the target table in the `FROM` clause to emulate an `INNER JOIN`. |
| Multiple `INNER JOIN` | Use the target table in the `FROM` clause to emulate an `INNER JOIN`. |
| Multiple `INNER JOIN` + Agregate condition | Use subquery + IN Operation |
| Single `LEFT JOIN` | Use subquery + IN Operation |
| Multiple `LEFT JOIN` | Use Snowflake `UPDATE` reordering the statements as needed.  **`UPDATE`** `[target_table_name]`  **`SET`** `[all_set_statements]`  **`FROM`** `[all_left_join_tables_separated_by_comma]`  **`WHERE`** `[all_clauses_into_the_ON_part]` |
| Multiple `RIGHT JOIN` | Use Snowflake `UPDATE` reordering the statements as needed.  **`UPDATE`** `[target_table_name]`  **`SET`** `[all_set_statements]`  **`FROM`** `[all_right_join_tables_separated_by_comma]`  **`WHERE`** `[all_clauses_into_the_ON_part]` |
| Single RIGHT JOIN | Use the table in the `FROM` clause and add filters in the `WHERE` clause as needed. |

*Note-1: Simple JOIN may use the table in the `FROM` clause and add filters in the `WHERE` clause as needed.*

*Note-2: Other approaches may include (+) operand to define the JOINs.*

### Sample Source Patterns[¶](#id105 "Link to this heading")

#### Setup data[¶](#setup-data "Link to this heading")

##### SQLServer[¶](#sqlserver "Link to this heading")

```
CREATE TABLE Orders (
    OrderID INT PRIMARY KEY,
    CustomerID INT,
    ProductID INT,
    Quantity INT,
    OrderDate DATE
);

CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY,
    CustomerName VARCHAR(100)
);

CREATE TABLE Products (
    ProductID INT PRIMARY KEY,
    ProductName VARCHAR(100),
    Price DECIMAL(10, 2)
);
```

Copy

##### Snowflake[¶](#id106 "Link to this heading")

```
CREATE OR REPLACE TABLE Orders (
    OrderID INT PRIMARY KEY,
    CustomerID INT,
    ProductID INT,
    Quantity INT,
    OrderDate DATE
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "11/12/2024",  "domain": "test" }}'
;

CREATE OR REPLACE TABLE Customers (
    CustomerID INT PRIMARY KEY,
    CustomerName VARCHAR(100)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "11/12/2024",  "domain": "test" }}'
;

CREATE OR REPLACE TABLE Products (
    ProductID INT PRIMARY KEY,
    ProductName VARCHAR(100),
    Price DECIMAL(10, 2)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "11/12/2024",  "domain": "test" }}'
;
```

Copy

Data Insertion for samples

```
-- Insert Customer Data
INSERT INTO Customers (CustomerID, CustomerName) VALUES (1, 'John Doe');
INSERT INTO Customers (CustomerID, CustomerName) VALUES (2, 'Jane Smith');
INSERT INTO Customers (CustomerID, CustomerName) VALUES (3, 'Alice Johnson');
INSERT INTO Customers (CustomerID, CustomerName) VALUES (4, 'Bob Lee');
INSERT INTO Customers (CustomerID, CustomerName) VALUES (5, 'Charlie Brown');
INSERT INTO Customers (CustomerID, CustomerName) VALUES (6, 'David White');
INSERT INTO Customers (CustomerID, CustomerName) VALUES (7, 'Eve Black');
INSERT INTO Customers (CustomerID, CustomerName) VALUES (8, 'Grace Green');
INSERT INTO Customers (CustomerID, CustomerName) VALUES (9, 'Hank Blue');
INSERT INTO Customers (CustomerID, CustomerName) VALUES (10, 'Ivy Red');
INSERT INTO Customers (CustomerID, CustomerName) VALUES (11, 'Jack Grey');
INSERT INTO Customers (CustomerID, CustomerName) VALUES (12, 'Kim Yellow');
INSERT INTO Customers (CustomerID, CustomerName) VALUES (13, 'Leo Purple');
INSERT INTO Customers (CustomerID, CustomerName) VALUES (14, 'Mona Pink');
INSERT INTO Customers (CustomerID, CustomerName) VALUES (15, 'Nathan Orange');
INSERT INTO Customers (CustomerID, CustomerName) VALUES (16, 'Olivia Cyan');
INSERT INTO Customers (CustomerID, CustomerName) VALUES (17, 'Paul Violet');
INSERT INTO Customers (CustomerID, CustomerName) VALUES (18, 'Quincy Brown');
INSERT INTO Customers (CustomerID, CustomerName) VALUES (19, 'Rita Silver');
INSERT INTO Customers (CustomerID, CustomerName) VALUES (20, 'Sam Green');
INSERT INTO Customers (CustomerID, CustomerName) VALUES (21, 'Tina Blue');
INSERT INTO Customers (CustomerID, CustomerName) VALUES (22, 'Ursula Red');
INSERT INTO Customers (CustomerID, CustomerName) VALUES (23, 'Vince Yellow');
INSERT INTO Customers (CustomerID, CustomerName) VALUES (24, 'Wendy Black');
INSERT INTO Customers (CustomerID, CustomerName) VALUES (25, 'Xander White');

-- Insert Product Data
INSERT INTO Products (ProductID, ProductName, Price) VALUES (1, 'Laptop', 999.99);
INSERT INTO Products (ProductID, ProductName, Price) VALUES (2, 'Smartphone', 499.99);
INSERT INTO Products (ProductID, ProductName, Price) VALUES (3, 'Tablet', 299.99);
INSERT INTO Products (ProductID, ProductName, Price) VALUES (4, 'Headphones', 149.99);
INSERT INTO Products (ProductID, ProductName, Price) VALUES (5, 'Monitor', 199.99);
INSERT INTO Products (ProductID, ProductName, Price) VALUES (6, 'Keyboard', 49.99);
INSERT INTO Products (ProductID, ProductName, Price) VALUES (7, 'Mouse', 29.99);
INSERT INTO Products (ProductID, ProductName, Price) VALUES (8, 'Camera', 599.99);
INSERT INTO Products (ProductID, ProductName, Price) VALUES (9, 'Printer', 99.99);
INSERT INTO Products (ProductID, ProductName, Price) VALUES (10, 'Speaker', 129.99);
INSERT INTO Products (ProductID, ProductName, Price) VALUES (11, 'Charger', 29.99);
INSERT INTO Products (ProductID, ProductName, Price) VALUES (12, 'TV', 699.99);
INSERT INTO Products (ProductID, ProductName, Price) VALUES (13, 'Smartwatch', 199.99);
INSERT INTO Products (ProductID, ProductName, Price) VALUES (14, 'Projector', 499.99);
INSERT INTO Products (ProductID, ProductName, Price) VALUES (15, 'Game Console', 399.99);
INSERT INTO Products (ProductID, ProductName, Price) VALUES (16, 'Speaker System', 299.99);
INSERT INTO Products (ProductID, ProductName, Price) VALUES (17, 'Earphones', 89.99);
INSERT INTO Products (ProductID, ProductName, Price) VALUES (18, 'USB Drive', 15.99);
INSERT INTO Products (ProductID, ProductName, Price) VALUES (19, 'External Hard Drive', 79.99);
INSERT INTO Products (ProductID, ProductName, Price) VALUES (20, 'Router', 89.99);
INSERT INTO Products (ProductID, ProductName, Price) VALUES (21, 'Printer Ink', 49.99);
INSERT INTO Products (ProductID, ProductName, Price) VALUES (22, 'Flash Drive', 9.99);
INSERT INTO Products (ProductID, ProductName, Price) VALUES (23, 'Gamepad', 34.99);
INSERT INTO Products (ProductID, ProductName, Price) VALUES (24, 'Webcam', 49.99);
INSERT INTO Products (ProductID, ProductName, Price) VALUES (25, 'Docking Station', 129.99);

-- Insert Orders Data
INSERT INTO Orders (OrderID, CustomerID, ProductID, Quantity, OrderDate) VALUES (1, 1, 1, 2, '2024-11-01');
INSERT INTO Orders (OrderID, CustomerID, ProductID, Quantity, OrderDate) VALUES (2, 2, 2, 1, '2024-11-02');
INSERT INTO Orders (OrderID, CustomerID, ProductID, Quantity, OrderDate) VALUES (3, 3, 3, 5, '2024-11-03');
INSERT INTO Orders (OrderID, CustomerID, ProductID, Quantity, OrderDate) VALUES (4, 4, 4, 3, '2024-11-04');
INSERT INTO Orders (OrderID, CustomerID, ProductID, Quantity, OrderDate) VALUES (5, NULL, 5, 7, '2024-11-05');  -- NULL Customer
INSERT INTO Orders (OrderID, CustomerID, ProductID, Quantity, OrderDate) VALUES (6, 6, 6, 2, '2024-11-06');
INSERT INTO Orders (OrderID, CustomerID, ProductID, Quantity, OrderDate) VALUES (7, 7, NULL, 4, '2024-11-07');  -- NULL Product
INSERT INTO Orders (OrderID, CustomerID, ProductID, Quantity, OrderDate) VALUES (8, 8, 8, 1, '2024-11-08');
INSERT INTO Orders (OrderID, CustomerID, ProductID, Quantity, OrderDate) VALUES (9, 9, 9, 3, '2024-11-09');
INSERT INTO Orders (OrderID, CustomerID, ProductID, Quantity, OrderDate) VALUES (10, 10, 10, 2, '2024-11-10');
INSERT INTO Orders (OrderID, CustomerID, ProductID, Quantity, OrderDate) VALUES (11, 11, 11, 5, '2024-11-11');
INSERT INTO Orders (OrderID, CustomerID, ProductID, Quantity, OrderDate) VALUES (12, 12, 12, 2, '2024-11-12');
INSERT INTO Orders (OrderID, CustomerID, ProductID, Quantity, OrderDate) VALUES (13, NULL, 13, 8, '2024-11-13');  -- NULL Customer
INSERT INTO Orders (OrderID, CustomerID, ProductID, Quantity, OrderDate) VALUES (14, 14, NULL, 4, '2024-11-14');  -- NULL Product
INSERT INTO Orders (OrderID, CustomerID, ProductID, Quantity, OrderDate) VALUES (15, 15, 15, 3, '2024-11-15');
INSERT INTO Orders (OrderID, CustomerID, ProductID, Quantity, OrderDate) VALUES (16, 16, 16, 2, '2024-11-16');
INSERT INTO Orders (OrderID, CustomerID, ProductID, Quantity, OrderDate) VALUES (17, 17, 17, 1, '2024-11-17');
INSERT INTO Orders (OrderID, CustomerID, ProductID, Quantity, OrderDate) VALUES (18, 18, 18, 4, '2024-11-18');
INSERT INTO Orders (OrderID, CustomerID, ProductID, Quantity, OrderDate) VALUES (19, 19, 19, 3, '2024-11-19');
INSERT INTO Orders (OrderID, CustomerID, ProductID, Quantity, OrderDate) VALUES (20, 20, 20, 6, '2024-11-20');
INSERT INTO Orders (OrderID, CustomerID, ProductID, Quantity, OrderDate) VALUES (21, 21, 21, 3, '2024-11-21');
INSERT INTO Orders (OrderID, CustomerID, ProductID, Quantity, OrderDate) VALUES (22, 22, 22, 5, '2024-11-22');
INSERT INTO Orders (OrderID, CustomerID, ProductID, Quantity, OrderDate) VALUES (23, 23, 23, 2, '2024-11-23');
INSERT INTO Orders (OrderID, CustomerID, ProductID, Quantity, OrderDate) VALUES (24, 24, 24, 4, '2024-11-24');
INSERT INTO Orders (OrderID, CustomerID, ProductID, Quantity, OrderDate) VALUES (25, 25, 25, 3, '2024-11-25');
```

Copy

#### Case 1: Single `INNER JOIN` Update[¶](#case-1-single-inner-join-update "Link to this heading")

For INNER JOIN, if the table is used inside the FROM statements, it automatically turns into INNER JOIN. Notice that there are several approaches to support JOINs in UPDATE statements in Snowflake. This is one of the simplest patterns to ensure readability.

##### SQL Server[¶](#id107 "Link to this heading")

```
UPDATE Orders
SET Quantity = 10
FROM Orders O
INNER JOIN Customers C ON O.CustomerID = C.CustomerID
WHERE C.CustomerName = 'John Doe';

-- Select the changes
SELECT Orders.CustomerID, Orders.Quantity, Customers.CustomerName
FROM Orders, Customers
WHERE Orders.CustomerID = Customers.CustomerID
AND Customers.CustomerName = 'John Doe';
```

Copy

##### Output[¶](#id108 "Link to this heading")

| CustomerID | Quantity | CustomerName |
| --- | --- | --- |
| 1 | 10 | John Doe |

##### Snowflake[¶](#id109 "Link to this heading")

```
UPDATE Orders O
SET O.Quantity = 10
FROM 
  Customers C
WHERE 
  C.CustomerName = 'John Doe'
  AND O.CustomerID = C.CustomerID;


-- Select the changes
SELECT Orders.CustomerID, Orders.Quantity, Customers.CustomerName
FROM Orders, Customers
WHERE Orders.CustomerID = Customers.CustomerID
AND Customers.CustomerName = 'John Doe';
```

Copy

##### Output[¶](#id110 "Link to this heading")

| CustomerID | Quantity | CustomerName |
| --- | --- | --- |
| 1 | 10 | John Doe |

**Other approaches:**

MERGE INTO

```
MERGE INTO Orders O
USING Customers C
ON O.CustomerID = C.CustomerID
WHEN MATCHED AND C.CustomerName = 'John Doe' THEN
  UPDATE SET O.Quantity = 10;
```

Copy


IN Operation

```
UPDATE Orders O
SET O.Quantity = 10
WHERE O.CustomerID IN 
  (SELECT CustomerID FROM Customers WHERE CustomerName = 'John Doe');
```

Copy

#### Case 2: Multiple `INNER JOIN` Update[¶](#case-2-multiple-inner-join-update "Link to this heading")

##### SQL Server[¶](#id111 "Link to this heading")

```
 UPDATE Orders
SET Quantity = 5
FROM Orders O
INNER JOIN Customers C ON O.CustomerID = C.CustomerID
INNER JOIN Products P ON O.ProductID = P.ProductID
WHERE C.CustomerName = 'Alice Johnson' AND P.ProductName = 'Tablet';

-- Select the changes
SELECT Orders.CustomerID, Orders.Quantity, Customers.CustomerName FROM Orders, Customers
WHERE Orders.CustomerID = Customers.CustomerID
AND Customers.CustomerName = 'Alice Johnson';
```

Copy

##### Output[¶](#id112 "Link to this heading")

| CustomerID | Quantity | CustomerName |
| --- | --- | --- |
| 3 | 5 | Alice Johnson |

##### Snowflake[¶](#id113 "Link to this heading")

```
UPDATE Orders O
SET O.Quantity = 5
FROM Customers C, Products P
WHERE O.CustomerID = C.CustomerID
  AND C.CustomerName = 'Alice Johnson'
  AND P.ProductName = 'Tablet'
  AND O.ProductID = P.ProductID;

-- Select the changes
SELECT Orders.CustomerID, Orders.Quantity, Customers.CustomerName FROM Orders, Customers
WHERE Orders.CustomerID = Customers.CustomerID
AND Customers.CustomerName = 'Alice Johnson';
```

Copy

##### Output[¶](#id114 "Link to this heading")

| CustomerID | Quantity | CustomerName |
| --- | --- | --- |
| 3 | 5 | Alice Johnson |

#### Case 3: Multiple `INNER JOIN` Update with Aggregate Condition[¶](#case-3-multiple-inner-join-update-with-aggregate-condition "Link to this heading")

##### SQL Server[¶](#id115 "Link to this heading")

```
UPDATE Orders
SET Quantity = 6
FROM Orders O
INNER JOIN Customers C ON O.CustomerID = C.CustomerID
INNER JOIN Products P ON O.ProductID = P.ProductID
WHERE C.CustomerID IN (SELECT CustomerID FROM Orders WHERE Quantity > 3)
AND P.Price < 200;

SELECT C.CustomerID, C.CustomerName, O.Quantity, P.Price FROM Orders O
INNER JOIN Customers C ON O.CustomerID = C.CustomerID
INNER JOIN Products P ON O.ProductID = P.ProductID
WHERE C.CustomerID IN (SELECT CustomerID FROM Orders WHERE Quantity > 3)
AND P.Price < 200;
```

Copy

##### Output[¶](#id116 "Link to this heading")

| CustomerID | CustomerName | Quantity | Price |
| --- | --- | --- | --- |
| 11 | Jack Grey | 6 | 29.99 |
| 18 | Quincy Brown | 6 | 15.99 |
| 20 | Sam Green | 6 | 89.99 |
| 22 | Ursula Red | 6 | 9.99 |
| 24 | Wendy Black | 6 | 49.99 |

##### Snowflake[¶](#id117 "Link to this heading")

```
UPDATE Orders O
SET Quantity = 6
WHERE O.CustomerID IN (SELECT CustomerID FROM Orders WHERE Quantity > 3)
AND O.ProductID IN (SELECT ProductID FROM Products WHERE Price < 200);

-- Select changes
SELECT C.CustomerID, C.CustomerName, O.Quantity, P.Price FROM Orders O
INNER JOIN Customers C ON O.CustomerID = C.CustomerID
INNER JOIN Products P ON O.ProductID = P.ProductID
WHERE C.CustomerID IN (SELECT CustomerID FROM Orders WHERE Quantity > 3)
AND P.Price < 200;
```

Copy

##### Output[¶](#id118 "Link to this heading")

| CustomerID | CustomerName | Quantity | Price |
| --- | --- | --- | --- |
| 11 | Jack Grey | 6 | 29.99 |
| 18 | Quincy Brown | 6 | 15.99 |
| 20 | Sam Green | 6 | 89.99 |
| 22 | Ursula Red | 6 | 9.99 |
| 24 | Wendy Black | 6 | 49.99 |

#### Case 4: Single `LEFT JOIN` Update[¶](#case-4-single-left-join-update "Link to this heading")

##### SQL Server[¶](#id119 "Link to this heading")

```
UPDATE Orders
SET Quantity = 13
FROM Orders O
LEFT JOIN Customers C ON O.CustomerID = C.CustomerID
WHERE C.CustomerID IS NULL AND O.ProductID = 13;

-- Select the changes
SELECT * FROM orders
WHERE CustomerID IS NULL;
```

Copy

##### Output[¶](#id120 "Link to this heading")

| OrderID | CustomerID | ProductID | Quantity | OrderDate |
| --- | --- | --- | --- | --- |
| 5 | null | 5 | 7 | 2024-11-05 |
| 13 | null | 13 | 13 | 2024-11-13 |

##### Snowflake[¶](#id121 "Link to this heading")

```
UPDATE Orders
SET Quantity = 13
WHERE OrderID IN (
  SELECT O.OrderID
  FROM Orders O
  LEFT JOIN Customers C ON O.CustomerID = C.CustomerID
  WHERE C.CustomerID IS NULL AND O.ProductID = 13
);


-- Select the changes
SELECT * FROM orders
WHERE CustomerID IS NULL;
```

Copy

##### Output[¶](#id122 "Link to this heading")

| OrderID | CustomerID | ProductID | Quantity | OrderDate |
| --- | --- | --- | --- | --- |
| 5 | null | 5 | 7 | 2024-11-05 |
| 13 | null | 13 | 13 | 2024-11-13 |

Note

This approach in Snowflake will not work because it does not update the necessary rows:

`UPDATE Orders O SET O.Quantity = 13 FROM Customers C WHERE O.CustomerID = C.CustomerID AND C.CustomerID IS NULL AND O.ProductID = 13;`

#### Case 5: Multiple `LEFT JOIN` and `RIGHT JOIN` Update[¶](#case-5-multiple-left-join-and-right-join-update "Link to this heading")

This is a more complex pattern. To translate multiple LEFT JOINs, please review the following pattern:

Note

`LEFT JOIN` and `RIGHT JOIN` will depend on the order in the `FROM` clause.

```
UPDATE [target_table_name]
SET [all_set_statements]
FROM [all_left_join_tables_separated_by_comma]
WHERE [all_clauses_into_the_ON_part]
```

Copy

##### SQL Server[¶](#id123 "Link to this heading")

```
UPDATE Orders
SET
    Quantity = C.CustomerID
FROM Orders O
LEFT JOIN Customers C ON C.CustomerID = O.CustomerID
LEFT JOIN Products P ON P.ProductID = O.ProductID
WHERE C.CustomerName = 'Alice Johnson'
  AND P.ProductName = 'Tablet';

SELECT O.OrderID, O.CustomerID, O.ProductID, O.Quantity, O.OrderDate
FROM Orders O
LEFT JOIN Customers C ON C.CustomerID = O.CustomerID
LEFT JOIN Products P ON P.ProductID = O.ProductID
WHERE C.CustomerName = 'Alice Johnson'
  AND P.ProductName = 'Tablet';
```

Copy

##### Output[¶](#id124 "Link to this heading")

| OrderID | CustomerID | ProductID | Quantity | OrderDate |
| --- | --- | --- | --- | --- |
| 3 | 3 | 3 | 3 | 2024-11-12 |

##### Snowflake[¶](#id125 "Link to this heading")

```
UPDATE Orders O
SET O.Quantity = C.CustomerID
FROM Customers C, Products P
WHERE O.CustomerID = C.CustomerID
  AND C.CustomerName = 'Alice Johnson'
  AND P.ProductName = 'Tablet'
  AND O.ProductID = P.ProductID;

  SELECT O.OrderID, O.CustomerID, O.ProductID, O.Quantity, O.OrderDate
FROM Orders O
LEFT JOIN Customers C ON C.CustomerID = O.CustomerID
LEFT JOIN Products P ON P.ProductID = O.ProductID
WHERE C.CustomerName = 'Alice Johnson'
  AND P.ProductName = 'Tablet';
```

Copy

##### Output[¶](#id126 "Link to this heading")

| OrderID | CustomerID | ProductID | Quantity | OrderDate |
| --- | --- | --- | --- | --- |
| 3 | 3 | 3 | 3 | 2024-11-12 |

#### Case 6: Mixed `INNER JOIN` and `LEFT JOIN` Update[¶](#case-6-mixed-inner-join-and-left-join-update "Link to this heading")

##### SQL Server[¶](#id127 "Link to this heading")

```
UPDATE Orders
SET Quantity = 4
FROM Orders O
INNER JOIN Products P ON O.ProductID = P.ProductID
LEFT JOIN Customers C ON O.CustomerID = C.CustomerID
WHERE C.CustomerID IS NULL AND P.ProductName = 'Monitor';

-- Select changes
SELECT O.CustomerID, C.CustomerName, O.Quantity FROM Orders O
INNER JOIN Products P ON O.ProductID = P.ProductID
LEFT JOIN Customers C ON O.CustomerID = C.CustomerID
WHERE C.CustomerID IS NULL AND P.ProductName = 'Monitor';
```

Copy

##### Output[¶](#id128 "Link to this heading")

| CustomerID | CustomerName | Quantity |
| --- | --- | --- |
| null | null | 4 |

##### Snowflake[¶](#id129 "Link to this heading")

```
UPDATE Orders O
SET Quantity = 4
WHERE O.ProductID IN (SELECT ProductID FROM Products WHERE ProductName = 'Monitor')
AND O.CustomerID IS NULL;

-- Select changes
SELECT O.CustomerID, C.CustomerName, O.Quantity FROM Orders O
INNER JOIN Products P ON O.ProductID = P.ProductID
LEFT JOIN Customers C ON O.CustomerID = C.CustomerID
WHERE C.CustomerID IS NULL AND P.ProductName = 'Monitor';
```

Copy

##### Output[¶](#id130 "Link to this heading")

| CustomerID | CustomerName | Quantity |
| --- | --- | --- |
| null | null | 4 |

#### Case 7: Single `RIGHT JOIN` Update[¶](#case-7-single-right-join-update "Link to this heading")

##### SQL Server[¶](#id131 "Link to this heading")

```
UPDATE O
SET O.Quantity = 1000
FROM Orders O
RIGHT JOIN Customers C ON O.CustomerID = C.CustomerID
WHERE C.CustomerName = 'Alice Johnson';

-- Select changes 
SELECT
    O.OrderID,
    O.CustomerID,
    O.ProductID,
    O.Quantity,
    O.OrderDate,
    C.CustomerName
FROM
    Orders O
RIGHT JOIN Customers C ON O.CustomerID = C.CustomerID
WHERE
    C.CustomerName = 'Alice Johnson';
```

Copy

##### Output[¶](#id132 "Link to this heading")

| OrderID | CustomerID | ProductID | Quantity | CustomerName |
| --- | --- | --- | --- | --- |
| 3 | 3 | 3 | 1000 | Alice Johnson |

##### Snowflake[¶](#id133 "Link to this heading")

```
UPDATE Orders O
SET O.Quantity = 1000
FROM Customers C
WHERE O.CustomerID = C.CustomerID
  AND C.CustomerName = 'Alice Johnson';


  -- Select changes 
SELECT
    O.OrderID,
    O.CustomerID,
    O.ProductID,
    O.Quantity,
    O.OrderDate,
    C.CustomerName
FROM
    Orders O
RIGHT JOIN Customers C ON O.CustomerID = C.CustomerID
WHERE
    C.CustomerName = 'Alice Johnson';
```

Copy

##### Output[¶](#id134 "Link to this heading")

| OrderID | CustomerID | ProductID | Quantity | CustomerName |
| --- | --- | --- | --- | --- |
| 3 | 3 | 3 | 1000 | Alice Johnson |

#### Know Issues[¶](#know-issues "Link to this heading")

* Since `UPDATE` in Snowflake does not allow the usage of `JOINs` directly, there may be cases that do not match the patterns described.

## UPDATE with LEFT and RIGHT JOIN[¶](#update-with-left-and-right-join "Link to this heading")

Translation specification for the UPDATE statement with JOINs.

Applies to

* SQL Server
* Azure Synapse Analytics

Warning

Partially supported in Snowflake

### Description[¶](#id135 "Link to this heading")

The pattern UPDATE FROM is used to update data based on data from other tables. This [SQLServer documentation](https://learn.microsoft.com/en-us/sql/t-sql/queries/update-transact-sql?view=sql-server-ver16#OtherTables) provides a simple sample.

Review the following SQL Server syntax from the [documentation](https://learn.microsoft.com/en-us/sql/t-sql/queries/update-transact-sql?view=sql-server-ver16#UpdateExamples).

#### SQL Server Syntax[¶](#id136 "Link to this heading")

```
UPDATE [table_name] 
SET column_name = expression [, ...]
[FROM <table_source> [, ...]]
[WHERE <search_condition>]
[OPTION (query_hint)]
```

Copy

* **`table_name`**: The table or view you are updating.
* **`SET`**: Specifies the columns and their new values. The `SET` clause assigns a new value (or expression) to one or more columns.
* **`FROM`**: Used to specify one or more source tables (*like a **join**)*. It helps define where the data comes from to perform the update.
* **`WHERE`**: Specifies which rows should be updated based on the condition(s). Without this clause, all rows in the table would be updated.
* **`OPTION (query_hint)`**: Specifies hints for query optimization.

##### Snowflake syntax[¶](#id137 "Link to this heading")

The Snowflake syntax can also be reviewed in the [Snowflake documentation](https://docs.snowflake.com/en/sql-reference/sql/update).

Note

Snowflake does not support `JOINs` in `UPDATE` clause.

```
 UPDATE <target_table>
       SET <col_name> = <value> [ , <col_name> = <value> , ... ]
        [ FROM <additional_tables> ]
```

Copy

**Required parameters**

* ***`target_table:`***Specifies the table to update.
* ***`col_name:`***Specifies the name of a column in *`target_table`*. Do not include the table name. E.g., `UPDATE t1 SET t1.col = 1` is invalid.
* ***`value`**`:`*Specifies the new value to set in *`col_name`*.

**Optional parameters**

* **``` FROM`` ```** ***`additional_tables:`*** Specifies one or more tables to use for selecting rows to update or for setting new values. *Note that repeating the target table results in a self-join.*
* **``` WHERE`` ```** ***`condition:`***The expression that specifies the rows in the target table to update. Default: No value (all rows of the target table are updated)

#### Translation Summary[¶](#id138 "Link to this heading")

As it is explained in the grammar description, there is not straight forward equivalent solution for JOINs inside the UPDATE cluase. For this reason, the approach to transform this statements is to add the operator (+) on the column that logically will add the required data into the table. This operator (+) is added to the cases on which the tables are referenced in the `LEFT`/`RIGHT` `JOIN` section.

Notice that there are other languages that use this operator (+) and the position of the operator may determine the type of join. In this specific case in Snowflake, the position will not determine the join type but the asociation with the logically needed tables and columns will.

Even when there are other alternative as MERGE c;ause or the usages of a CTE; these alternatives tend to turn difficult to read when there are complex queries, and get extensive.

### Sample Source Patterns[¶](#id139 "Link to this heading")

#### Setup data[¶](#id140 "Link to this heading")

##### SQL Server[¶](#id141 "Link to this heading")

```
 CREATE TABLE GenericTable1 (
    Col1 INT,
    Col2 VARCHAR(10),
    Col3 VARCHAR(10),
    Col4 VARCHAR(10),
    Col5 VARCHAR(10),
    Col6 VARCHAR(100)
);

CREATE TABLE GenericTable2 (
    Col1 VARCHAR(10),
    Col2 VARCHAR(10),
    Col3 VARCHAR(10),
    Col4 VARCHAR(10),
    Col5 VARCHAR(10)
);

CREATE TABLE GenericTable3 (
    Col1 VARCHAR(10),
    Col2 VARCHAR(100),
    Col3 CHAR(1)
);

INSERT INTO GenericTable1 (Col1, Col2, Col3, Col4, Col5, Col6)
VALUES
(1, 'A1', 'B1', 'C1', NULL, NULL),
(2, 'A2', 'B2', 'C2', NULL, NULL),
(3, 'A3', 'B3', 'C3', NULL, NULL);

INSERT INTO GenericTable2 (Col1, Col2, Col3, Col4, Col5)
VALUES
('1', 'A1', 'B1', 'C1', 'X1'),
('2', 'A2', 'B2', 'C2', 'X2'),
('3', 'A3', 'B3', 'C3', 'X3');

INSERT INTO GenericTable3 (Col1, Col2, Col3)
VALUES
('X1', 'Description1', 'A'),
('X2', 'Description2', 'A'),
('X3', 'Description3', 'A');
```

Copy

##### Snowflake[¶](#id142 "Link to this heading")

```
 CREATE OR REPLACE TABLE GenericTable1 (
    Col1 INT,
    Col2 VARCHAR(10),
    Col3 VARCHAR(10),
    Col4 VARCHAR(10),
    Col5 VARCHAR(10),
    Col6 VARCHAR(100)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "12/18/2024",  "domain": "test" }}'
;

CREATE OR REPLACE TABLE GenericTable2 (
    Col1 VARCHAR(10),
    Col2 VARCHAR(10),
    Col3 VARCHAR(10),
    Col4 VARCHAR(10),
    Col5 VARCHAR(10)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "12/18/2024",  "domain": "test" }}'
;

CREATE OR REPLACE TABLE GenericTable3 (
    Col1 VARCHAR(10),
    Col2 VARCHAR(100),
    Col3 CHAR(1)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "12/18/2024",  "domain": "test" }}'
;

INSERT INTO GenericTable1 (Col1, Col2, Col3, Col4, Col5, Col6)
VALUES
(1, 'A1', 'B1', 'C1', NULL, NULL),
(2, 'A2', 'B2', 'C2', NULL, NULL),
(3, 'A3', 'B3', 'C3', NULL, NULL);

INSERT INTO GenericTable2 (Col1, Col2, Col3, Col4, Col5)
VALUES
('1', 'A1', 'B1', 'C1', 'X1'),
('2', 'A2', 'B2', 'C2', 'X2'),
('3', 'A3', 'B3', 'C3', 'X3');

INSERT INTO GenericTable3 (Col1, Col2, Col3)
VALUES
('X1', 'Description1', 'A'),
('X2', 'Description2', 'A'),
('X3', 'Description3', 'A');
```

Copy

#### LEFT JOIN[¶](#left-join "Link to this heading")

##### SQL Server[¶](#id143 "Link to this heading")

```
 UPDATE T1
SET
    T1.Col5 = T2.Col5,
    T1.Col6 = T3.Col2
FROM GenericTable1 T1
LEFT JOIN GenericTable2 T2 ON
    T2.Col1 COLLATE SQL_Latin1_General_CP1_CI_AS = T1.Col1
    AND T2.Col2 = T1.Col2
    AND T2.Col3 = T1.Col3
    AND T2.Col4 = T1.Col4
LEFT JOIN GenericTable3 T3 ON
    T3.Col1 = T2.Col5 AND T3.Col3 = 'A';
```

Copy

##### Output Before Query[¶](#output-before-query "Link to this heading")

| Col1 | Col2 | Col3 | Col4 | Col5 | Col6 |
| --- | --- | --- | --- | --- | --- |
| 1 | A1 | B1 | C1 | *null* | *null* |
| 2 | A2 | B2 | C2 | *null* | *null* |
| 3 | A3 | B3 | C3 | *null* | *null* |

##### Output After Query[¶](#output-after-query "Link to this heading")

| Col1 | Col2 | Col3 | Col4 | Col5 | Col6 |
| --- | --- | --- | --- | --- | --- |
| 1 | A1 | B1 | C1 | *X1* | *Description1* |
| 2 | A2 | B2 | C2 | *X2* | *Description2* |
| 3 | A3 | B3 | C3 | *X3* | *Description3* |

##### Snowflake[¶](#id144 "Link to this heading")

```
 UPDATE dbo.GenericTable1 T1
    SET
        T1.Col5 = T2.Col5,
        T1.Col6 = T3.Col2
    FROM
        GenericTable2 T2,
        GenericTable3 T3
    WHERE
        T2.Col1(+) COLLATE 'EN-CI-AS' /*** SSC-FDM-TS0002 - COLLATION FOR VALUE CP1 NOT SUPPORTED ***/ = T1.Col1
        AND T2.Col2(+) = T1.Col2
        AND T2.Col3(+) = T1.Col3
        AND T2.Col4(+) = T1.Col4
        AND T3.Col1(+) = T2.Col5
        AND T3.Col3 = 'A';
```

Copy

##### Output Before Query[¶](#id145 "Link to this heading")

| Col1 | Col2 | Col3 | Col4 | Col5 | Col6 |
| --- | --- | --- | --- | --- | --- |
| 1 | A1 | B1 | C1 | *null* | *null* |
| 2 | A2 | B2 | C2 | *null* | *null* |
| 3 | A3 | B3 | C3 | *null* | *null* |

##### Output After Query[¶](#id146 "Link to this heading")

| Col1 | Col2 | Col3 | Col4 | Col5 | Col6 |
| --- | --- | --- | --- | --- | --- |
| 1 | A1 | B1 | C1 | *X1* | *Description1* |
| 2 | A2 | B2 | C2 | *X2* | *Description2* |
| 3 | A3 | B3 | C3 | *X3* | *Description3* |

#### RIGHT JOIN[¶](#right-join "Link to this heading")

##### SQL Server[¶](#id147 "Link to this heading")

```
UPDATE T1
SET
    T1.Col5 = T2.Col5
FROM GenericTable2 T2
RIGHT JOIN GenericTable1 T1 ON
    T2.Col1 COLLATE SQL_Latin1_General_CP1_CI_AS = T1.Col1
    AND T2.Col2 = T1.Col2
    AND T2.Col3 = T1.Col3
    AND T2.Col4 = T1.Col4;
```

Copy

##### Output Before Query[¶](#id148 "Link to this heading")

| Col1 | Col2 | Col3 | Col4 | Col5 | Col6 |
| --- | --- | --- | --- | --- | --- |
| 1 | A1 | B1 | C1 | *null* | *null* |
| 2 | A2 | B2 | C2 | *null* | *null* |
| 3 | A3 | B3 | C3 | *null* | *null* |

##### Output After Query[¶](#id149 "Link to this heading")

| Col1 | Col2 | Col3 | Col4 | Col5 | Col6 |
| --- | --- | --- | --- | --- | --- |
| 1 | A1 | B1 | C1 | *\*\*X1* | *null* |
| 2 | A2 | B2 | C2 | *\*\*X2* | *null* |
| 3 | A3 | B3 | C3 | *\*\*X3* | *null* |

##### Snowflake[¶](#id150 "Link to this heading")

```
 UPDATE dbo.GenericTable1 T1
    SET
        T1.Col5 = T2.Col5
    FROM
        GenericTable2 T2,
        GenericTable1 T1
    WHERE
        T2.Col1 COLLATE 'EN-CI-AS' /*** SSC-FDM-TS0002 - COLLATION FOR VALUE CP1 NOT SUPPORTED ***/ = T1.Col1
        AND T2.Col2 = T1.Col2(+)
        AND T2.Col3 = T1.Col3(+)
        AND T2.Col4 = T1.Col4(+);
```

Copy

##### Output Before Query[¶](#id151 "Link to this heading")

| Col1 | Col2 | Col3 | Col4 | Col5 | Col6 |
| --- | --- | --- | --- | --- | --- |
| 1 | A1 | B1 | C1 | *null* | *null* |
| 2 | A2 | B2 | C2 | *null* | *null* |
| 3 | A3 | B3 | C3 | *null* | *null* |

##### Output After Query[¶](#id152 "Link to this heading")

| Col1 | Col2 | Col3 | Col4 | Col5 | Col6 |
| --- | --- | --- | --- | --- | --- |
| 1 | A1 | B1 | C1 | *\*\*X1* | *null* |
| 2 | A2 | B2 | C2 | *\*\*X2* | *null* |
| 3 | A3 | B3 | C3 | *\*\*X3* | *null* |

### Known Issues[¶](#id153 "Link to this heading")

* There may be patterns that cannot be translated due to differences in logic.
* If your query pattern applies, review non-deterministic rows: “When a [FROM](https://docs.snowflake.com/en/sql-reference/constructs/from) clause contains a [JOIN](https://docs.snowflake.com/en/sql-reference/constructs/join) between tables (e.g. `t1` and `t2`), a target row in `t1` may join against (i.e. match) more than one row in table `t2`. When this occurs, the target row is called a *multi-joined row*. When updating a multi-joined row, the [ERROR\_ON\_NONDETERMINISTIC\_UPDATE](https://docs.snowflake.com/en/sql-reference/parameters.html#label-error-on-nondeterministic-update) session parameter controls the outcome of the update” ([Snowflake documentation](https://docs.snowflake.com/en/sql-reference/sql/update)).

Was this page helpful?

YesNo

[Visit Snowflake](https://www.snowflake.com)

[Join the conversation](https://community.snowflake.com/s/)

[Develop with Snowflake](https://developers.snowflake.com)

[Share your feedback](/feedback)

[Read the latest on our blog](https://www.snowflake.com/blog/)

[Get your own certification](https://learn.snowflake.com)

[Privacy Notice](https://www.snowflake.com/privacy-policy/)[Site Terms](https://www.snowflake.com/legal/snowflake-site-terms/)Cookies Settings© 2026 Snowflake, Inc. All Rights Reserved.

Terms of Use

The SnowConvert AI tool is subject to the [Conversion Software Terms of Use](https://www.snowflake.com/en/legal/technical-services-and-education/conversion-software-terms/).

On this page

1. [BETWEEN](#between)
2. [BULK INSERT](#bulk-insert)
3. [Common Table Expression (CTE)](#common-table-expression-cte)
4. [DELETE](#delete)
5. [DROP STATEMENT](#drop-statement)
6. [EXISTS](#exists)
7. [IN](#in)
8. [INSERT](#insert)
9. [MERGE](#merge)
10. [SELECT](#select)
11. [SET OPERATORS](#set-operators)
12. [TRUNCATE](#truncate)
13. [UPDATE](#update)
14. [UPDATE WITH JOIN](#update-with-join)
15. [UPDATE with LEFT and RIGHT JOIN](#update-with-left-and-right-join)