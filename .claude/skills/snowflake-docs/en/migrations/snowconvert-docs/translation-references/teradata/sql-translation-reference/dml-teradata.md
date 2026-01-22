---
auto_generated: true
description: In this section, you will find the documentation for the translation
  reference of Data Manipulation Language Elements.
last_scraped: '2026-01-14T16:53:52.880356+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/teradata/sql-translation-reference/dml-teradata
title: SnowConvert AI - Teradata - DML | Snowflake Documentation
---

1. [Overview](../../../../../guides/README.md)
2. [Snowflake Horizon Catalog](../../../../../user-guide/snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../../../../../guides/overview-connecting.md)
6. [Virtual warehouses](../../../../../user-guide/warehouses.md)
7. [Databases, Tables, & Views](../../../../../guides/overview-db.md)
8. [Data types](../../../../../data-types.md)
10. Data Integration

    - [Snowflake Openflow](../../../../../user-guide/data-integration/openflow/about.md)
    - Apache Iceberg™

      - [Apache Iceberg™ Tables](../../../../../user-guide/tables-iceberg.md)
      - [Snowflake Open Catalog](../../../../../user-guide/opencatalog/overview.md)
11. Data engineering

    - [Data loading](../../../../../guides/overview-loading-data.md)
    - [Dynamic Tables](../../../../../user-guide/dynamic-tables-about.md)
    - [Streams and Tasks](../../../../../user-guide/data-pipelines-intro.md)
    - [dbt Projects on Snowflake](../../../../../user-guide/data-engineering/dbt-projects-on-snowflake.md)
    - [Data Unloading](../../../../../guides/overview-unloading-data.md)
12. [Storage Lifecycle Policies](../../../../../user-guide/storage-management/storage-lifecycle-policies.md)
13. [Migrations](../../../../README.md)

    * Tools

      * [SnowConvert AI](../../../overview.md)

        + General

          + [About](../../../general/about.md)
          + [Getting Started](../../../general/getting-started/README.md)
          + [Terms And Conditions](../../../general/terms-and-conditions/README.md)
          + [Release Notes](../../../general/release-notes/release-notes/README.md)
          + User Guide

            + [SnowConvert AI](../../../general/user-guide/snowconvert/README.md)
            + [Project Creation](../../../general/user-guide/project-creation.md)
            + [Extraction](../../../general/user-guide/extraction.md)
            + [Deployment](../../../general/user-guide/deployment.md)
            + [Data Migration](../../../general/user-guide/data-migration.md)
            + [Data Validation](../../../general/user-guide/data-validation.md)
            + [Power BI Repointing](../../../general/user-guide/power-bi-repointing-general.md)
            + [ETL Migration](../../../general/user-guide/etl-migration-replatform.md)
          + [Technical Documentation](../../../general/technical-documentation/README.md)
          + [Contact Us](../../../general/contact-us.md)
          + Others

            + [Using SnowConvert AI In A Ubuntu Docker Image](../../../general/others/using-snowconvert-in-a-ubuntu-docker-image.md)
          + [Frequently Asked Questions (FAQ)](../../../general/frequently-asked-questions-faq.md)")
        + Translation References

          + [General](../../general/README.md)
          + [Teradata](../README.md)

            - [Data Migration Considerations](../data-migration-considerations.md)
            - [Session Modes in Teradata](../session-modes.md)
            - [Sql Translation Reference](README.md)

              * [Built-in Functions](teradata-built-in-functions.md)
              * [Data Types](data-types.md)
              * [Database DBC](database-dbc.md)
              * [DDL Statements](ddl-teradata.md)
              * [DML Statements](dml-teradata.md)
              * [Analytic](analytic.md)
              * [Iceberg Table Transformations](Iceberg-tables-transformations.md)
            - [SQL to JavaScript (Procedures)](../teradata-to-javascript-translation-reference.md)")
            - [SQL to Snowflake Scripting (Procedures)](../teradata-to-snowflake-scripting-translation-reference.md)")
            - [Scripts To Python](../scripts-to-python/README.md)
            - [Scripts to Snowflake SQL](../scripts-to-snowflake-sql-translation-reference/README.md)
            - ETL And BI Repointing

              - [Power BI Teradata Repointing](../etl-bi-repointing/power-bi-teradata-repointing.md)
          + [Oracle](../../oracle/README.md)
          + [SQL Server-Azure Synapse](../../transact/README.md)
          + [Sybase IQ](../../sybase/README.md)
          + [Hive-Spark-Databricks SQL](../../hive/README.md)
          + [Redshift](../../redshift/README.md)
          + [PostgreSQL-Greenplum-Netezza](../../postgres/README.md)
          + [BigQuery](../../bigquery/README.md)
          + [Vertica](../../vertica/README.md)
          + [IBM DB2](../../db2/README.md)
          + [SSIS](../../ssis/README.md)
        + [Migration Assistant](../../../migration-assistant/README.md)
        + [Data Validation CLI](../../../data-validation-cli/index.md)
        + [AI Verification](../../../snowconvert-ai-verification.md)
      * [Snowpark Migration Accelerator](../../../../sma-docs/README.md)
    * Guides

      * [Teradata](../../../../guides/teradata.md)
      * [Databricks](../../../../guides/databricks.md)
      * [SQL Server](../../../../guides/sqlserver.md)
      * [Amazon Redshift](../../../../guides/redshift.md)
      * [Oracle](../../../../guides/oracle.md)
      * [Azure Synapse](../../../../guides/azuresynapse.md)
15. [Queries](../../../../../guides/overview-queries.md)
16. [Listings](../../../../../collaboration/collaboration-listings-about.md)
17. [Collaboration](../../../../../guides/overview-sharing.md)
19. [Snowflake AI & ML](../../../../../guides/overview-ai-features.md)
21. [Snowflake Postgres](../../../../../user-guide/snowflake-postgres/about.md)
23. [Alerts & Notifications](../../../../../guides/overview-alerts.md)
25. [Security](../../../../../guides/overview-secure.md)
26. [Data Governance](../../../../../guides/overview-govern.md)
27. [Privacy](../../../../../guides/overview-privacy.md)
29. [Organizations & Accounts](../../../../../guides/overview-manage.md)
30. [Business continuity & data recovery](../../../../../user-guide/replication-intro.md)
32. [Performance optimization](../../../../../guides/overview-performance.md)
33. [Cost & Billing](../../../../../guides/overview-cost.md)

[Guides](../../../../../guides/README.md)[Migrations](../../../../README.md)Tools[SnowConvert AI](../../../overview.md)Translation References[Teradata](../README.md)[Sql Translation Reference](README.md)DML Statements

# SnowConvert AI - Teradata - DML[¶](#snowconvert-ai-teradata-dml "Link to this heading")

In this section, you will find the documentation for the translation reference of Data Manipulation Language Elements.

## Delete Statement[¶](#delete-statement "Link to this heading")

> See [Delete statement](https://docs.teradata.com/r/huc7AEHyHSROUkrYABqNIg/z8eO9bdxtjFRveHdDwwYPQ)

Teradata support calling more than one table in the`FROM`clause, Snowflake does not. Therefore, it is necessary to use the`USING`clause to refer to the extra tables involved in the condition.

**Teradata**

**Delete**

```
DEL FROM MY_TABLE ALL;
DEL FROM MY_TABLE_2 WHERE COL1 > 50;
DELETE T1 FROM TABLE1 T1, TABLE2 T2 WHERE T1.ID = T2.ID;
DELETE FROM TABLE1 T1, TABLE2 T2 WHERE T1.ID = T2.ID;
DELETE T1 FROM TABLE2 T2, TABLE1 T1 WHERE T1.ID = T2.ID;
DELETE FROM TABLE1 WHERE TABLE1.COLUMN1 = TABLE2.COLUMN2
```

Copy




**Snowflake**

**Delete**

```
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

Copy




### Known Issues[¶](#known-issues "Link to this heading")

#### 1. DEL abbreviation unsupported[¶](#del-abbreviation-unsupported "Link to this heading")

The abbreviation is unsupported in Snowflake but it is translated correctly by changing it to DELETE.

### Related EWIs[¶](#related-ewis "Link to this heading")

No related EWIs.

## Set Operators[¶](#set-operators "Link to this heading")

The SQL set operators manipulate the result sets of several queries combining the results of each query into a single result set.

Note

Some parts in the output code are omitted for clarity reasons.

> See [Set operators](https://docs.teradata.com/r/b8dd8xEYJnxfsq4uFRrHQQ/Q8qU3AO1RXLNFCPOGTX73g)

Set Operators in both Teradata and Snowflake have the same syntax and supported scenarios `EXCEPT`, `INTERSECT`, and `UNION` except for the clause `ALL` in the `INTERSECT ALL`, which is not supported in Snowflake, resulting in the portion of the `ALL` as a commented code after the conversion.

**Teradata**

### Intersect[¶](#intersect "Link to this heading")

```
 SELECT LastName, FirstName FROM employees
INTERSECT
SELECT FirstName, LastName FROM contractors;

SELECT LastName, FirstName FROM employees
INTERSECT ALL
SELECT FirstName, LastName FROM contractors;
```

Copy

**Snowflake**

#### Intersect[¶](#id1 "Link to this heading")

```
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

Copy

### Known Issues[¶](#id2 "Link to this heading")

#### 1. INTERSECT ALL unsupported[¶](#intersect-all-unsupported "Link to this heading")

The INTERSECT ALL is unsupported in Snowflake and then the part ALL will be commented.

### Related EWIs[¶](#id3 "Link to this heading")

1. [SSC-EWI-0040](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0040): Statement Not Supported.

## Update Statement[¶](#update-statement "Link to this heading")

### Description[¶](#description "Link to this heading")

> Modifies column values in existing rows of a table. ([Teradata SQL Language Reference UPDATE](https://docs.teradata.com/r/huc7AEHyHSROUkrYABqNIg/k6fC7ozmhIZZXa315VjJAw))

### Sample Source Patterns[¶](#sample-source-patterns "Link to this heading")

#### Basic case[¶](#basic-case "Link to this heading")

**Teradata**

**Update**

```
 UPDATE CRASHDUMPS.TABLE1 i
 SET COLUMN4 = CRASHDUMPS.TABLE2.COLUMN3
 WHERE i.COLUMN1 = CRASHDUMPS.TABLE2.COLUMN1
 AND i.COLUMN3 = 'L';
```

Copy




**Snowflake**

**Update**

```
UPDATE CRASHDUMPS.TABLE1 AS i
 SET
  i.COLUMN4 = CRASHDUMPS.TABLE2.COLUMN3
 FROM
  CRASHDUMPS.TABLE2
  WHERE i.COLUMN1 = CRASHDUMPS.TABLE2.COLUMN1
  AND UPPER(RTRIM( i.COLUMN3)) = UPPER(RTRIM('L'));
```

Copy

#### UPDATE with forward alias[¶](#update-with-forward-alias "Link to this heading")

Teradata supports referencing an alias before it is declared, but Snowflake does not. The transformation for this scenario is to take the referenced table and change the alias for the table name it references.

**Teradata**

**Update**

```
 UPDATE i
 FROM CRASHDUMPS.TABLE2, CRASHDUMPS.TABLE1 i
 SET COLUMN4 = CRASHDUMPS.TABLE2.COLUMN3
 WHERE i.COLUMN1 = CRASHDUMPS.TABLE2.COLUMN1
 AND i.COLUMN3 = 'L';
```

Copy




**Snowflake**

**Update**

```
UPDATE CRASHDUMPS.TABLE1 AS i
  SET
  i.COLUMN4 = CRASHDUMPS.TABLE2.COLUMN3
  FROM
  CRASHDUMPS.TABLE2
  WHERE i.COLUMN1 = CRASHDUMPS.TABLE2.COLUMN1
  AND UPPER(RTRIM( i.COLUMN3)) = UPPER(RTRIM('L'));
```

Copy

#### UPDATE with target table in the the FROM clause[¶](#update-with-target-table-in-the-the-from-clause "Link to this heading")

Teradata supports having the target table defined in the FROM clause, this is removed in Snowflake to avoid duplicate alias and ambiguous column reference errors.

**Teradata**

**Update**

```
UPDATE some_table
FROM some_table
SET Code = Code + 100
WHERE Name = 'A';
```

Copy




**Snowflake**

**Update**

```
UPDATE some_table
  SET Code = Code + 100
  WHERE
  UPPER(RTRIM( Name)) = UPPER(RTRIM('A'));
```

Copy

### Related EWIs[¶](#id4 "Link to this heading")

No related EWIs.

## With Modifier[¶](#with-modifier "Link to this heading")

Select statement that uses the WITH modifier with a list of several named queries also known as common table expressions (CTEs).

> See [With Modifier](https://docs.teradata.com/r/Teradata-VantageTM-SQL-Data-Manipulation-Language/July-2021/SELECT-Statements/WITH-Modifier)

Snowflake supports Teradata’s `WITH` modifier on a SELECT statement that has several `CTEs` (Common Table Expressions). Teradata supports any order of CTE definition, regardless of whether it is referenced before it is declared or not, but Snowflake requires that if a CTE calls another CTE, it must be defined before it is called. Then the converted sequence of CTEs within the WITH will be reordered into the unreferenced CTEs, then the CTE that calls the next CTE, and so on.

Where there is a cycle detected in the WITH calling sequence, it will be left as the original, without any changes to the sequence as detailed in an example of the [SSC-EWI-TD0077](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/teradataEWI.html#ssc-ewi-td0077).

In the example below, there are two CTEs named n1 and n2, the n1 referring to n2. Then the n2 must be defined first in Snowflake as the corresponding converted code.

Note

Some parts of the output code are omitted for clarity reasons.

**Teradata**

### With Modifier[¶](#id5 "Link to this heading")

```
 WITH recursive n1(c1) as (select c1, c3 from t2, n1),
     n2(c2) as (select c2 from tablex)
     SELECT * FROM t1;
```

Copy

**Snowflake**

#### With Modifier[¶](#id6 "Link to this heading")

```
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

Copy

### Known Issues[¶](#id7 "Link to this heading")

#### 1. Impossible to reorder when cycles were found[¶](#impossible-to-reorder-when-cycles-were-found "Link to this heading")

When the CTEs references are analyzed and there is a cycle between the calls of the CTEs, the CTEs will not be ordered.

### Related EWIs[¶](#id8 "Link to this heading")

No related EWIs.

## Insert Statement[¶](#insert-statement "Link to this heading")

SQL statement that adds new rows to a table.

Note

Some parts in the output code are omitted for clarity reasons.

> See [Insert statement](https://docs.teradata.com/r/0I5vemahub4iSU2bk5WA1A/SQ4EQb1a8WMHn3tbrcvW9Q)

In Teradata, there is an alternate`INSERT`syntax that assigns the value for each table column inline. This alternate structure requires a special transformation to be supported in Snowflake. The inline assignment of the values is separated and placed inside the `VALUES(...)` part of the Snowflake `INSERT INTO` statement.

**Teradata**

### Insert[¶](#insert "Link to this heading")

```
 INSERT INTO appDB.logTable (
    process_name = 'S2F_BOOKS_LOAD_NEW'
    , session_id = 105678989 
    , message_txt = '' 
    , message_ts = '2019-07-23 00:00:00'
    , Insert_dt = CAST((CURRENT_TIMESTAMP(0)) AS DATE FORMAT 'YYYY-MM-DD'));
```

Copy

**Snowflake**

#### Insert[¶](#id9 "Link to this heading")

```
 INSERT INTO appDB.logTable (
process_name, session_id, message_txt, message_ts, Insert_dt)
VALUES ('S2F_BOOKS_LOAD_NEW', 105678989, '', '2019-07-23 00:00:00', TO_DATE((CURRENT_TIMESTAMP(0))));
```

Copy

### Known Issues [¶](#id10 "Link to this heading")

No issues were found.

### Related EWIs [¶](#id11 "Link to this heading")

No related EWIs.

## LOGGING ERRORS[¶](#logging-errors "Link to this heading")

Note

Some parts in the output code are omitted for clarity reasons.

Note

Non-relevant statement.

Warning

**Notice that this statement is** **removed from the migration** **because it is a non-relevant syntax. It means that it is not required in Snowflake.**

### Description[¶](#id12 "Link to this heading")

Statement to log errors when using statements as `INSERT...SELECT.` Please review the following [documentation](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/SQL-Data-Manipulation-Language/Statement-Syntax/INSERT/INSERT-...-SELECT/INSERT/INSERT-...-SELECT-Examples/Example-Logging-Errors-with-INSERT-...-SELECT).

### Sample Source Patterns[¶](#id13 "Link to this heading")

#### LOGGING ERRORS[¶](#id14 "Link to this heading")

In this example, notice that `LOGGING ERRORS` has been removed because it is not a relevant syntax. The syntax is not required in Snowflake.

##### Teradata[¶](#teradata "Link to this heading")

```
 INSERT INTO MY_TABLE
SELECT *
FROM MY_SAMPLE
LOGGING ERRORS;
```

Copy

##### Snowflake[¶](#snowflake "Link to this heading")

```
INSERT INTO MY_TABLE SELECT
*
FROM
MY_SAMPLE;
```

#### LOGGING ALL ERRORS[¶](#logging-all-errors "Link to this heading")

In this example, notice that `LOGGING ALL ERRORS` has been removed because it is not a relevant syntax. The syntax is not required in Snowflake.

##### Teradata[¶](#id15 "Link to this heading")

```
 INSERT INTO MY_TABLE
SELECT *
FROM MY_SAMPLE
LOGGING ALL ERRORS;
```

Copy

##### Snowflake[¶](#id16 "Link to this heading")

```
 INSERT INTO MY_TABLE SELECT
*
FROM
MY_SAMPLE;
```

Copy

#### LOGGING ERRORS WITH NO LIMIT[¶](#logging-errors-with-no-limit "Link to this heading")

In this example, notice that `LOGGING ERRORS WITH NO LIMIT` has been removed because it is not a relevant syntax. The syntax is not required in Snowflake.

##### Teradata[¶](#id17 "Link to this heading")

```
 INSERT INTO MY_TABLE
SELECT *
FROM MY_SAMPLE
LOGGING ERRORS WITH NO LIMIT;
```

Copy

##### Snowflake[¶](#id18 "Link to this heading")

```
 INSERT INTO MY_TABLE SELECT
*
FROM
MY_SAMPLE;
```

Copy

#### LOGGING ERRORS WITH LIMIT OF[¶](#logging-errors-with-limit-of "Link to this heading")

In this example, notice that `LOGGING ERRORS WITH LIMIT OF` has been removed because it is not a relevant syntax. The syntax is not required in Snowflake.

##### Teradata[¶](#id19 "Link to this heading")

```
 INSERT INTO MY_TABLE
SELECT *
FROM MY_SAMPLE
LOGGING ERRORS WITH LIMIT OF 100;
```

Copy

##### Snowflake[¶](#id20 "Link to this heading")

```
 INSERT INTO MY_TABLE SELECT
*
FROM
MY_SAMPLE;
```

Copy

### Known Issues [¶](#id21 "Link to this heading")

No issues were found.

### Related EWIs [¶](#id22 "Link to this heading")

No related EWIs.

## Select Statement[¶](#select-statement "Link to this heading")

> See [Select statement](https://docs.teradata.com/reader/b8dd8xEYJnxfsq4uFRrHQQ/kH97CTRIXdd~i1yLemdvKw)

Snowflake supports Teradata’s `SELECT` syntax with a few exceptions. Primarily, it does not support the `SEL` abbreviation.​

**Teradata**

**Sel**

```
SEL DISTINCT col1, col2 FROM table1
```

Copy




**Snowflake**

**Select**

```
SELECT DISTINCT col1,
col2 FROM
table1;
```

Copy




Teradata supports referencing an alias before it is declared, but Snowflake does not. The transformation for this scenario is to take the referenced column and change the alias for the column name it references.

**Teradata**

**Alias**

```
SELECT
my_val, sum(col1),
col2 AS my_val FROM table1
```

Copy




**Snowflake**

**Alias**

```
SELECT
my_val,
SUM(col1),
col2 AS my_val FROM
table1;
```

Copy




### Removed clause options[¶](#removed-clause-options "Link to this heading")

The following clause options are not relevant to Snowflake, therefore they are removed during the migration.

| Teradata | Snowflake |
| --- | --- |
| Expand on | Unsupported |
| Normalize | Unsupported |
| With check option (Query) | Unsupported |

### Known Issues[¶](#id23 "Link to this heading")

#### 1. SEL abbreviation unsupported[¶](#sel-abbreviation-unsupported "Link to this heading")

The abbreviation is unsupported in Snowflake but it is translated correctly by changing it to SELECT.

### Related EWIs[¶](#id24 "Link to this heading")

No related EWIs.

## ANY Predicate[¶](#any-predicate "Link to this heading")

Warning

This is a work in progress, changes may be applied in the future.

### Description[¶](#id25 "Link to this heading")

In Teradata enables quantification in a comparison operation or IN/NOT IN predicate. The comparison of expression and at least one value in the set of values returned by subquery is true. Please review the following [Teradata documentation](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/SQL-Functions-Expressions-and-Predicates/Logical-Predicates/ANY/ALL/SOME) for more information.

**Teradata syntax**

```
 { expression quantifier ( literal [ {, | OR} ... ] ) |
  { expression | ( expression [,...] ) } quantifier ( subquery )
}
```

Copy

Where quantifier:

```
 { comparison_operator [ NOT ] IN } { ALL |ANY | SOME }
```

Copy

**Snowflake syntax**

SuccessPlaceholder

In subquery form, IN is equivalent to `= ANY` and NOT IN is equivalent to `<> ALL`. Review the following [Snowflake documentation](https://docs.snowflake.com/en/sql-reference/functions/in) for more infromation.

To compare individual values:

```
 <value> [ NOT ] IN ( <value_1> [ , <value_2> ...  ] )
```

Copy

To compare *row constructors* (parenthesized lists of values):

```
 ( <value_A> [, <value_B> ... ] ) [ NOT ] IN (  ( <value_1> [ , <value_2> ... ] )  [ , ( <value_3> [ , <value_4> ... ] )  ...  ]  )
```

Copy

To compare a value to the values returned by a subquery:

```
 <value> [ NOT ] IN ( <subquery> )
```

Copy

### Sample Source Patterns[¶](#id26 "Link to this heading")

#### Sample data[¶](#sample-data "Link to this heading")

##### Teradata[¶](#id27 "Link to this heading")

##### Query[¶](#query "Link to this heading")

```
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

Copy

##### Snowflake[¶](#id28 "Link to this heading")

##### Query[¶](#id29 "Link to this heading")

```
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

Copy

#### Equal ANY pedicate in WHERE clause [¶](#equal-any-pedicate-in-where-clause "Link to this heading")

**Teradata**

##### Input[¶](#input "Link to this heading")

```
 SELECT DeptNo
FROM Employee
WHERE DeptNo = ANY(100,300,500) ;
```

Copy

##### Output[¶](#output "Link to this heading")

| DeptNo |
| --- |
| 100 |
| 500 |
| 100 |
| 300 |

**Snowflake**

##### Input[¶](#id30 "Link to this heading")

```
 SELECT DeptNo
FROM Employee
WHERE DeptNo IN(100,300,500) ;
```

Copy

##### Output[¶](#id31 "Link to this heading")

| DeptNo |
| --- |
| 100 |
| 500 |
| 100 |
| 300 |

#### Other comparison operators in WHERE clause[¶](#other-comparison-operators-in-where-clause "Link to this heading")

When there are other comparison operators, there equivalent translation is to add a subquery with the required logic.

**Teradata**

##### Input[¶](#id32 "Link to this heading")

```
 SELECT Name, DeptNo
FROM Employee
WHERE DeptNo < ANY(100,300,500) ;
```

Copy

##### Output[¶](#id33 "Link to this heading")

| Name | DeptNo |
| --- | --- |
| Eve | 100 |
| Alice | 100 |
| David | 200 |
| Bob | 300 |

**Snowflake**

##### Input[¶](#id34 "Link to this heading")

```
 SELECT Name, DeptNo
FROM Employee
WHERE DeptNo < ANY 
(SELECT DeptNo
FROM Employee
WHERE DeptNo > 100
OR DeptNo > 300
OR DeptNo > 500);
```

Copy

##### Output[¶](#id35 "Link to this heading")

| NAME | DEPTNO |
| --- | --- |
| Alice | 100 |
| Eve | 100 |
| Bob | 300 |
| David | 200 |

#### IN ANY in WHERE clause[¶](#in-any-in-where-clause "Link to this heading")

**Teradata**

##### Input[¶](#id36 "Link to this heading")

```
 SELECT DeptNo
FROM Employee
WHERE DeptNo IN ANY(100,300,500) ;
```

Copy

##### Output[¶](#id37 "Link to this heading")

| DeptNo |
| --- |
| 100 |
| 500 |
| 100 |
| 300 |

**Snowflake**

##### Input[¶](#id38 "Link to this heading")

```
 SELECT DeptNo
FROM Employee
WHERE DeptNo IN(100,300,500) ;
```

Copy

##### Output[¶](#id39 "Link to this heading")

| DeptNo |
| --- |
| 100 |
| 500 |
| 100 |
| 300 |

#### NOT IN ALL in WHERE clause[¶](#not-in-all-in-where-clause "Link to this heading")

**Teradata**

##### Input[¶](#id40 "Link to this heading")

```
 SELECT Name, DeptNo
FROM Employee
WHERE DeptNo NOT IN ALL(100, 200);
```

Copy

##### Output[¶](#id41 "Link to this heading")

| Name | DeptNo |
| --- | --- |
| Charlie | 500 |
| Bob | 300 |

**Snowflake**

##### Input[¶](#id42 "Link to this heading")

```
 SELECT Name, DeptNo
FROM Employee
WHERE DeptNo NOT IN (100, 200);
```

Copy

##### Output[¶](#id43 "Link to this heading")

| Name | DeptNo |
| --- | --- |
| Charlie | 500 |
| Bob | 300 |

### Known Issues[¶](#id44 "Link to this heading")

#### NOT IN ANY in WHERE clause[¶](#not-in-any-in-where-clause "Link to this heading")

**Teradata**

##### Input[¶](#id45 "Link to this heading")

```
 SELECT Name, DeptNo
FROM Employee
WHERE DeptNo NOT IN ANY(100, 200);
```

Copy

##### Output[¶](#id46 "Link to this heading")

| Name | DeptNo |
| --- | --- |
| Eve | 100 |
| Charlie | 500 |
| Alice | 100 |
| David | 200 |
| Bob | 300 |

**Snowflake**

##### Input[¶](#id47 "Link to this heading")

```
 SELECT Name, DeptNo
FROM Employee
WHERE DeptNo IN (100, 200)
   OR DeptNo NOT IN (100, 200);
```

Copy

##### Output[¶](#id48 "Link to this heading")

| Name | DeptNo |
| --- | --- |
| Eve | 100 |
| Charlie | 500 |
| Alice | 100 |
| David | 200 |
| Bob | 300 |

### Related EWIs[¶](#id49 "Link to this heading")

No related EWIs.

## Expand On Clause[¶](#expand-on-clause "Link to this heading")

Translation reference to convert Teradata Expand On functionality to Snowflake

### Description[¶](#id50 "Link to this heading")

> The Expand On clause expands a column having a **period** data type, creating a regular time series of rows based on the period value in the input row. For more information about Expand On clause, see the [Teradata documentation](https://docs.teradata.com/r/huc7AEHyHSROUkrYABqNIg/542VMPPqGwHBhF98pnTz9w).

### Sample Source Patterns[¶](#id51 "Link to this heading")

Note

Some parts in the output code are omitted for clarity reasons.

#### Sample data[¶](#id52 "Link to this heading")

##### Teradata[¶](#id53 "Link to this heading")

```
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

Copy

##### Snowflake[¶](#id54 "Link to this heading")

```
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

Copy

#### Expand On Clause[¶](#id55 "Link to this heading")

Suppose you want to expand the period column by seconds, for this Expand On clause has anchor period expansion and interval literal expansion.

##### Anchor Period Expansion[¶](#anchor-period-expansion "Link to this heading")

##### Teradata[¶](#id56 "Link to this heading")

```
 SELECT
    id,
    BEGIN(bg)
FROM
    table1 EXPAND ON pd AS bg BY ANCHOR ANCHOR_SECOND;
```

Copy

##### Result[¶](#result "Link to this heading")

| id | BEGIN (bg) |
| --- | --- |
| 1 | 2022-05-23 10:15:21.0000 |
| 1 | 2022-05-23 10:15:22.0000 |
| 1 | 2022-05-23 10:15:23.0000 |
| 1 | 2022-05-23 10:15:24.0000 |
| 1 | 2022-05-23 10:15:25.0000 |

Snowflake doesn’t support Expand On clause. To reproduce the same results and functionality, the Teradata SQL code will be contained in a CTE block, with an **EXPAND\_ON\_UDF** and **TABLE** function, using **FLATTEN** function to return multiple rows, **ROW\_COUNT\_UDF** and **DIFF\_TTIME\_PERIOD\_UDF** to indicate how many rows are needed and returning **VALUE** to help the EXPAND\_ON\_UDF to calculate the different regular time series. This CTE block returns the same expand columns alias as in the Expand On clause, so the result can be used in any usage of period datatype.

##### Snowflake[¶](#id57 "Link to this heading")

```
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

Copy

##### Result[¶](#id58 "Link to this heading")

| id | PERIOD\_BEGIN\_UDF(bg) |
| --- | --- |
| 1 | 2022-05-23 10:15:21.0000 |
| 1 | 2022-05-23 10:15:22.0000 |
| 1 | 2022-05-23 10:15:23.0000 |
| 1 | 2022-05-23 10:15:24.0000 |
| 1 | 2022-05-23 10:15:25.0000 |

### Known Issues[¶](#id59 "Link to this heading")

The Expand On clause can use interval literal expansion, for this case, SnowConvert AI will add an error that this translation is planned.

#### Interval literal expansion[¶](#interval-literal-expansion "Link to this heading")

##### Teradata[¶](#id60 "Link to this heading")

```
 SELECT
    id,
    BEGIN(bg)
FROM
    table1 EXPAND ON pd AS bg BY INTERVAL '1' SECOND;
```

Copy

##### Result[¶](#id61 "Link to this heading")

| id | BEGIN(bg) |
| --- | --- |
| 1 | 2022-05-23 10:15:20.0000 |
| 1 | 2022-05-23 10:15:21.0000 |
| 1 | 2022-05-23 10:15:22.0000 |
| 1 | 2022-05-23 10:15:23.0000 |
| 1 | 2022-05-23 10:15:24.0000 |

##### Snowflake[¶](#id62 "Link to this heading")

```
 SELECT
    id,
    PUBLIC.PERIOD_BEGIN_UDF(bg) !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!
FROM
    table1
!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'EXPAND ON' NODE ***/!!!
EXPAND ON pd AS bg BY INTERVAL '1' SECOND;
```

Copy

### Related EWIs[¶](#id63 "Link to this heading")

1. [SSC-EWI-0073](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0073): Pending Functional Equivalence Review.
2. [SSC-EWI-TD0053](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/teradataEWI.html#ssc-ewi-td0053): Snowflake does not support the period datatype, all periods are handled as varchar instead.

## Normalize[¶](#normalize "Link to this heading")

Translation reference to convert Teradata Normalize functionality to Snowflake

### Description[¶](#id64 "Link to this heading")

> NORMALIZE specifies that period values in the first-period column that meet or overlap are combined to form a period that encompasses the individual period values. For more information about Normalize clause, see the [Teradata documentation](https://docs.teradata.com/r/2_MC9vCtAJRlKle2Rpb0mA/UuxiA0mklFgv~33X5nyKMA).

### Sample Source Patterns[¶](#id65 "Link to this heading")

Note

Some parts in the output code are omitteed for clarity reasons.

#### Sample data[¶](#id66 "Link to this heading")

##### Teradata[¶](#id67 "Link to this heading")

```
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

Copy

##### Snowflake[¶](#id68 "Link to this heading")

```
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

Copy

#### Normalize Clause[¶](#normalize-clause "Link to this heading")

Suppose you want to use Normalize clause with the employee id.

##### Teradata[¶](#id69 "Link to this heading")

```
 SELECT
    NORMALIZE emp_id,
    duration
FROM
    project;
```

Copy

##### Result[¶](#id70 "Link to this heading")

| EMP\_ID | DURATION |
| --- | --- |
| 20 | (2010-03-10, 2010-07-20) |
| 10 | (2010-01-10, 2010-08-18) |
| 20 | (2020-05-10, 2010-09-20) |

##### Snowflake[¶](#id71 "Link to this heading")

```
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

Copy

##### Result[¶](#id72 "Link to this heading")

| EMP\_ID | PUBLIC.PERIOD\_UDF(MIN(START\_DATE), MAX(END\_DATE)) |
| --- | --- |
| 20 | 2020-05-10\*2010-09-20 |
| 20 | 2010-03-10\*2010-07-20 |
| 10 | 2010-01-10\*2010-08-18 |

### Known Issues[¶](#id73 "Link to this heading")

Normalize clause can use **ON MEETS OR OVERLAPS**, **ON OVERLAPS** or **ON OVERLAPS OR MEETS,** for these cases SnowConvert AI will add an error that this translation is planned for the future.

#### Teradata[¶](#id74 "Link to this heading")

```
 SELECT NORMALIZE ON MEETS OR OVERLAPS emp_id, duration FROM table1;
```

Copy

##### Snowflake[¶](#id75 "Link to this heading")

```
 SELECT
       !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'NORMALIZE SET QUANTIFIER' NODE ***/!!!
       NORMALIZE ON MEETS OR OVERLAPS emp_id,
duration FROM
table1;
```

Copy

### Related EWIs[¶](#id76 "Link to this heading")

1. [SSC-EWI-0073](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0073): Pending Functional Equivalence Review.
2. [SSC-EWI-TD0079](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/teradataEWI.html#ssc-ewi-td0079): The required period type column was not found.
3. [SSC-EWI-TD0053](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/teradataEWI.html#ssc-ewi-td0053): Snowflake does not support the period datatype, all periods are handled as varchar instead.

## Reset When[¶](#reset-when "Link to this heading")

### Description[¶](#id77 "Link to this heading")

> Reset When determines the partition on which an SQL window function operates based on some specific condition. If the condition evaluates to True, a new dynamic sub partition is created within the existing window partition. For more information about Reset When, see the [Teradata documentation](https://docs.teradata.com/reader/1DcoER_KpnGTfgPinRAFUw/b7wL86OoMTPno6hrSPNdDg).

### Sample Source Patterns[¶](#id78 "Link to this heading")

#### Sample data[¶](#id79 "Link to this heading")

##### Teradata[¶](#id80 "Link to this heading")

**Query**

```
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

Copy



**Result**

| account\_id | month\_id | balance |
| --- | --- | --- |
| 1 | 1 | 60 |
| 1 | 2 | 99 |
| 1 | 3 | 94 |
| 1 | 4 | 90 |
| 1 | 5 | 80 |
| 1 | 6 | 88 |
| 1 | 7 | 90 |
| 1 | 8 | 92 |
| 1 | 9 | 10 |
| 1 | 10 | 60 |
| 1 | 11 | 80 |
| 1 | 12 | 10 |

##### Snowflake[¶](#id81 "Link to this heading")

**Query**

```
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

Copy



**Result**

| account\_id | month\_id | balance |
| --- | --- | --- |
| 1 | 1 | 60 |
| 1 | 2 | 99 |
| 1 | 3 | 94 |
| 1 | 4 | 90 |
| 1 | 5 | 80 |
| 1 | 6 | 88 |
| 1 | 7 | 90 |
| 1 | 8 | 92 |
| 1 | 9 | 10 |
| 1 | 10 | 60 |
| 1 | 11 | 80 |
| 1 | 12 | 10 |

#### Reset When[¶](#id82 "Link to this heading")

For each account, suppose you want to analyze the sequence of consecutive monthly balance increases. When the balance of one month is less than or equal to the balance of the previous month, the requirement is to reset the counter to zero and restart.

To analyze this data, Teradata SQL uses a window function with a nested aggregate and a Reset When statement, as follows:

##### Teradata[¶](#id83 "Link to this heading")

**Query**

```
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

Copy



**Result**

| account\_id | month\_id | balance | balance\_increase |
| --- | --- | --- | --- |
| 1 | 1 | 60 | 0 |
| 1 | 2 | 99 | 1 |
| 1 | 3 | 94 | 0 |
| 1 | 4 | 90 | 0 |
| 1 | 5 | 80 | 0 |
| 1 | 6 | 88 | 1 |
| 1 | 7 | 90 | 2 |
| 1 | 8 | 92 | 3 |
| 1 | 9 | 10 | 0 |
| 1 | 10 | 60 | 1 |
| 1 | 11 | 80 | 2 |
| 1 | 12 | 10 | 0 |

##### Snowflake[¶](#id84 "Link to this heading")

Snowflake does not support the Reset When clause in window functions. To reproduce the same result, the Teradata SQL code must be translated using native SQL syntax and nested subqueries, as follows:

**Query**

```
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

Copy



**Result**

| account\_id | month\_id | balance | balance\_increase |
| --- | --- | --- | --- |
| 1 | 1 | 60 | 0 |
| 1 | 2 | 99 | 1 |
| 1 | 3 | 94 | 0 |
| 1 | 4 | 90 | 0 |
| 1 | 5 | 80 | 0 |
| 1 | 6 | 88 | 1 |
| 1 | 7 | 90 | 2 |
| 1 | 8 | 92 | 3 |
| 1 | 9 | 10 | 0 |
| 1 | 10 | 60 | 1 |
| 1 | 11 | 80 | 2 |
| 1 | 12 | 10 | 0 |



Two nested sub-queries are needed to support the Reset When functionality in Snowflake.

In the inner sub-query, a dynamic partition indicator (dynamic\_part) is created and populated. dynamic\_part is set to 1 if one month’s balance is less than or equal to the preceding month’s balance; otherwise, it’s set to 0.

In the next layer, a new\_dynamic\_part attribute is generated as the result of a SUM window function.

Finally, a new\_dynamic\_part is added as a new partition attribute (dynamic partition) to the existing partition attribute (account\_id) and applies the same ROW\_NUMBER() window function as in Teradata.

After these changes, Snowflake generates the same output as Teradata.

#### Reset When when conditional window function is a column[¶](#reset-when-when-conditional-window-function-is-a-column "Link to this heading")

Same example as above, except that now the window function used in the RESET WHEN condition is defined as a column called `previous`. This variation changes the transformation slightly since it is no longer necessary to define the `previous_value` as in the previous example. It is the same workaround.

##### Teradata[¶](#id85 "Link to this heading")

**Query**

```
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

Copy



**Result**

| account\_id | month\_id | balance | previous | balance\_increase |
| --- | --- | --- | --- | --- |
| 1 | 1 | 60 |  | 0 |
| 1 | 2 | 99 | 60 | 1 |
| 1 | 3 | 94 | 99 | 0 |
| 1 | 4 | 90 | 94 | 0 |
| 1 | 5 | 80 | 90 | 0 |
| 1 | 6 | 88 | 80 | 1 |
| 1 | 7 | 90 | 88 | 2 |
| 1 | 8 | 92 | 90 | 3 |
| 1 | 9 | 10 | 92 | 0 |
| 1 | 10 | 60 | 10 | 1 |
| 1 | 11 | 80 | 60 | 2 |
| 1 | 12 | 10 | 80 | 0 |

##### Snowflake[¶](#id86 "Link to this heading")

**Query**

```
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

Copy



**Untitled**

| account\_id | month\_id | balance | previous | balance\_increase |
| --- | --- | --- | --- | --- |
| 1 | 1 | 60 |  | 0 |
| 1 | 2 | 99 | 60 | 1 |
| 1 | 3 | 94 | 99 | 0 |
| 1 | 4 | 90 | 94 | 0 |
| 1 | 5 | 80 | 90 | 0 |
| 1 | 6 | 88 | 80 | 1 |
| 1 | 7 | 90 | 88 | 2 |
| 1 | 8 | 92 | 90 | 3 |
| 1 | 9 | 10 | 92 | 0 |
| 1 | 10 | 60 | 10 | 1 |
| 1 | 11 | 80 | 60 | 2 |
| 1 | 12 | 10 | 80 | 0 |

### Known Issues[¶](#id87 "Link to this heading")

The RESET WHEN clause could have some variations such as its condition. Currently, SnowConvert AI only supports binary conditions (<=, >=, <> or =), in any other type, as `IS NOT NULL`, SnowConvert AI will remove the RESET WHEN clause and add an error message since it is not supported in Snowflake, as shown in the following example.

#### Teradata[¶](#id88 "Link to this heading")

**Query**

```
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

Copy

#### Snowflake[¶](#id89 "Link to this heading")

**Query**

```
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

Copy

### Related EWIs[¶](#id90 "Link to this heading")

* [SSC-EWI-TD0077](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/teradataEWI.html#ssc-ewi-td0077): RESET WHEN clause is not supported in this scenario due to its condition.

## SAMPLE clause[¶](#sample-clause "Link to this heading")

### Description[¶](#id91 "Link to this heading")

The SAMPLE clause in Teradata reduces the number of rows to be processed and it returns one or more samples of rows as a list of fractions or as a list of numbers of rows. The clause is used in the SELECT query. Please review the following [Teradata documentation](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/SQL-Data-Manipulation-Language/SELECT-Statements/SAMPLE-Clause) for more information.

**Teradata syntax**

```
SAMPLE
  [ WITH REPLACEMENT ]
  [ RANDOMIZED LOCALIZATION ]
  { { fraction_description | count_description } [,...] |
    when_clause ]
  }
```

Copy

**Snowflake syntax**

Review the following [Snowflake documentation](https://docs.snowflake.com/en/sql-reference/constructs/sample) for more information. `SAMPLE` and `TABLESAMPLE` are synonymous.

```
SELECT ...
FROM ...
  { SAMPLE | TABLESAMPLE } [ samplingMethod ]
[ ... ]
```

Copy

Where:

```
samplingMethod ::= { 
{ BERNOULLI | ROW } ( { <probability> | <num> ROWS } ) |
{ SYSTEM | BLOCK } ( <probability> ) [ { REPEATABLE | SEED } ( <seed> ) ] }
```

Copy

* In Snowflake, the following keywords can be used interchangeably:

  > + `SAMPLE | TABLESAMPLE`
  > + `BERNOULLI | ROW`
  > + `SYSTEM | BLOCK`
  > + `REPEATABLE | SEED`

Review the following table to check on key differences.

| SAMPLE behavior | Teradata | Snowflake |
| --- | --- | --- |
| Sample by probability | Also known as fraction description. It must be a fractional number between 0,1 and 1. | Decimal number between 0 and 100. |
| Fixed number of rows | Also known as count description. It is a positive integer that determines the number of rows to be sampled. | It specifies the number of rows (up to 1,000,000) to sample from the table. Can be any integer between `0` (no rows selected) and `1000000` inclusive. |
| Repeated rows | It is known as `WITH REPLACEMENT.` This is used to query more samples than there are rows in the table. | It is known as `REPEATABLE` or `SEED`. This is used to make the query deterministic. It means that the same set of rows will be the same for each query run. |
| Sampling methods | *Proportional* and `RANDOMIZED ALLOCATION.` | `BERNOULLI` or `SYSTEM`. |

### Sample Source Patterns[¶](#id92 "Link to this heading")

#### Sample data[¶](#id93 "Link to this heading")

##### Teradata[¶](#id94 "Link to this heading")

**Query**

```
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

Copy

##### Snowflake[¶](#id95 "Link to this heading")

**Query**

```
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

Copy

#### SAMPLE clause[¶](#id96 "Link to this heading")

##### Fixed number of rows[¶](#fixed-number-of-rows "Link to this heading")

Notice that for this example, the number of rows are a fixed number but not necessarily are the same result for each run.

**Teradata**

**Input**

```
SELECT * FROM Employee SAMPLE 2;
```

Copy

**Output**
2 rows.



**Snowflake**

**Input**

```
SELECT * FROM Employee SAMPLE (2 ROWS);
```

Copy

**Output**
2 rows.

##### Rows number based on probability[¶](#rows-number-based-on-probability "Link to this heading")

This option will return a variety of rows depending on the probability set.

**Teradata**

**Input**

```
SELECT * FROM Employee SAMPLE 0.25;
```

Copy

**Output**
25% of probability for each row: 1 output row.



**Snowflake**

**Input**

```
SELECT * FROM Employee SAMPLE (25);
```

Copy

**Output**
25% of probability for each row: 1 output row.

### Known Issues[¶](#id97 "Link to this heading")

#### Fixed number of rows with replacement[¶](#fixed-number-of-rows-with-replacement "Link to this heading")

This option will return a fixed number of rows and will allows the repetition of the rows. In Snowflake, it is not possible to request more samples than rows in a table.

**Teradata sample**

**Input**

```
SELECT * FROM Employee SAMPLE WITH REPLACEMENT 8;
```

Copy

**Output**

| EmpNo | Name | DeptNo |
| --- | --- | --- |
| 5 | Eve | 100 |
| 5 | Eve | 100 |
| 5 | Eve | 100 |
| 4 | David | 200 |
| 4 | David | 200 |
| 3 | Charlie | 500 |
| 1 | Alice | 100 |
| 1 | Alice | 100 |

#### SAMPLEID related functionality[¶](#sampleid-related-functionality "Link to this heading")

In Teradata, it is possible to assign a unique ID to each sample that is specified. It helps to identify which belongs to which sample. This is not ANSI grammar, instead it is an extension of Teradata.

**Teradata sample**

**Input**

```
SELECT name, SAMPLEID FROM employee SAMPLE 0.5, 0.25, 0.25;
```

Copy

**Output**

| Name | SampleId |
| --- | --- |
| Eve | 3 |
| Charlie | 1 |
| Alice | 1 |
| David | 2 |
| Bob | 1 |



In Snowflake, there is not a SAMPLEID function. A possible workaround may be the following, but it has to be adaptaed to each single case:

**Snowflake possible workaround**

**Input**

```
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

Copy

**Output**

| Name | SAMPLE\_ID |
| --- | --- |
| Alice | 1 |
| Bob | 1 |
| Charlie | 2 |
| David | 3 |
| Eve | 3 |

#### Conditional sampling[¶](#conditional-sampling "Link to this heading")

In Snowflake there is not conditional sampling. This can be achieve by using CTE’s.

**Teradata sample**

**Input**

```
SELECT * FROM employee
SAMPLE WHEN DeptNo > 100 then 0.9 
ELSE 0.1 END;
```

Copy

**Output**

| EmpNo | Name | DeptNo |
| --- | --- | --- |
| 3 | Charlie | 500 |
| 4 | David | 200 |
| 2 | Bob | 300 |

### Related EWIs[¶](#id98 "Link to this heading")

[SSC-EWI-0021](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0021): Syntax not supported in Snowflake.

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

1. [Delete Statement](#delete-statement)
2. [Set Operators](#set-operators)
3. [Update Statement](#update-statement)
4. [With Modifier](#with-modifier)
5. [Insert Statement](#insert-statement)
6. [LOGGING ERRORS](#logging-errors)
7. [Select Statement](#select-statement)
8. [ANY Predicate](#any-predicate)
9. [Expand On Clause](#expand-on-clause)
10. [Normalize](#normalize)
11. [Reset When](#reset-when)
12. [SAMPLE clause](#sample-clause)