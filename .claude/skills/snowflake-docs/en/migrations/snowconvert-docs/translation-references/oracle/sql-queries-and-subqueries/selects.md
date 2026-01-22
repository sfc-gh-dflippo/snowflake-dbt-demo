---
auto_generated: true
description: In this section you could find information about the select query syntax
  and its convertions.
last_scraped: '2026-01-14T16:53:28.385750+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/oracle/sql-queries-and-subqueries/selects
title: SnowConvert AI - Oracle - Select | Snowflake Documentation
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
          + [Teradata](../../teradata/README.md)
          + [Oracle](../README.md)

            - [Sample Data](../sample-data.md)
            - Basic Elements of Oracle SQL

              - [Literals](../basic-elements-of-oracle-sql/literals.md)
              - [Data Types](../basic-elements-of-oracle-sql/data-types/README.md)
            - [Pseudocolumns](../pseudocolumns.md)
            - [Built-in Functions](../functions/README.md)
            - [Built-in Packages](../built-in-packages.md)
            - [SQL Queries and Subqueries](selects.md)

              * [Joins](joins.md)
            - [SQL Statements](../sql-translation-reference/README.md)
            - [PL/SQL to Snowflake Scripting](../pl-sql-to-snowflake-scripting/README.md)
            - [PL/SQL to Javascript](../pl-sql-to-javascript/README.md)
            - [SQL Plus](../sql-plus.md)
            - [Wrapped Objects](../wrapped-objects.md)
            - ETL And BI Repointing

              - [Power BI Oracle Repointing](../etl-bi-repointing/power-bi-oracle-repointing.md)
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

[Guides](../../../../../guides/README.md)[Migrations](../../../../README.md)Tools[SnowConvert AI](../../../overview.md)Translation References[Oracle](../README.md)SQL Queries and Subqueries

# SnowConvert AI - Oracle - Select[¶](#snowconvert-ai-oracle-select "Link to this heading")

In this section you could find information about the select query syntax and its convertions.

Note

Some parts in the output codes are omitted for clarity reasons.

## Overall Select Translation[¶](#overall-select-translation "Link to this heading")

### Simple select[¶](#simple-select "Link to this heading")

#### Oracle:[¶](#oracle "Link to this heading")

```
select * from table1;
select col1 from schema1.table1;
```

Copy

#### Snowflake:[¶](#snowflake "Link to this heading")

```
select * from
table1;

select col1 from
schema1.table1;
```

Copy

### Where clause[¶](#where-clause "Link to this heading")

#### Oracle:[¶](#id1 "Link to this heading")

```
select col1 from schema1.table1 WHERE col1 = 1 and id > 0 or id < 1;
```

Copy

#### Snowflake:[¶](#id2 "Link to this heading")

```
select col1 from
schema1.table1
WHERE col1 = 1 and id > 0 or id < 1;
```

Copy

### Order By clause[¶](#order-by-clause "Link to this heading")

#### Oracle:[¶](#id3 "Link to this heading")

```
select col1 from schema1.table1 order by id ASC;
```

Copy

#### Snowflake:[¶](#id4 "Link to this heading")

```
select col1 from
schema1.table1
order by id ASC;
```

Copy

### Group by[¶](#group-by "Link to this heading")

#### Oracle:[¶](#id5 "Link to this heading")

```
select col1 from schema1.table1 GROUP BY id;
```

Copy

#### Snowflake:[¶](#id6 "Link to this heading")

```
select col1 from
schema1.table1
GROUP BY id;
```

Copy

### Model Clause[¶](#model-clause "Link to this heading")

The model clause is not supported yet.

### Row Limiting Clause[¶](#row-limiting-clause "Link to this heading")

#### Oracle:[¶](#id7 "Link to this heading")

```
-- Using ONLY
select * from TableFetch1 FETCH FIRST 2 ROWS ONLY;
select * from TableFetch1 FETCH FIRST 20 percent ROWS ONLY;
select * from TableFetch1 order by col1 FETCH FIRST 2 ROWS with ties;
select * from TableFetch1 order by col1 FETCH FIRST 20 percent ROWS with ties;

-- Using OFFSET clause
select * from TableFetch1 offset 2 rows FETCH FIRST 2 ROWS ONLY;
select * from TableFetch1 offset 2 rows FETCH FIRST 60 percent rows ONLY;
select * from TableFetch1 
order by col1 offset 2 rows FETCH NEXT 2 ROWs with ties;
select * from TableFetch1 
order by col1 offset 2 rows FETCH FIRST 60 percent ROWs with ties;

-- Using WITH TIES clause
select * from TableFetch1 FETCH FIRST 2 ROWS with ties;
select * from TableFetch1 FETCH FIRST 20 percent ROWS with ties;
select * from TableFetch1 offset 2 rows FETCH NEXT 2 ROWs with ties;
select * from TableFetch1 offset 2 rows FETCH FIRST 60 percent ROWs with ties;

-- Using ORDER BY clause
select * from TableFetch1 order by col1 FETCH FIRST 2 ROWS ONLY;
select * from TableFetch1 order by col1 FETCH FIRST 20 percent ROWS ONLY;
select * from TableFetch1 order by col1 offset 2 rows FETCH FIRST 2 ROWS ONLY;
select * from TableFetch1 
order by col1 offset 2 rows FETCH FIRST 60 percent ROWS ONLY;

select * from TableFetch1 FETCH FIRST ROWS ONLY;

select * from TableFetch1 offset 2 rows;
```

Copy

#### Snowflake:[¶](#id8 "Link to this heading")

```
-- Using ONLY
select * from
TableFetch1
FETCH FIRST 2 ROWS ONLY;

select * from
TableFetch1
QUALIFY
(ROW_NUMBER() OVER (
ORDER BY
NULL) - 1) / COUNT(*) OVER () < 20 / 100;

select * from
TableFetch1
QUALIFY
RANK() OVER (
order by col1) <= 2;

select * from
TableFetch1
QUALIFY
(RANK() OVER (
order by col1) - 1) / COUNT(*) OVER () < 20 / 100;

-- Using OFFSET clause
select * from
TableFetch1
offset 2 rows FETCH FIRST 2 ROWS ONLY;

select * from
TableFetch1
QUALIFY
(ROW_NUMBER() OVER (
ORDER BY
NULL) - 1 - 2) / COUNT(*) OVER () < 60 / 100
LIMIT NULL OFFSET 2;

select * from
TableFetch1
QUALIFY
RANK() OVER (
order by col1) - 2 <= 2
LIMIT NULL OFFSET 2;

select * from
TableFetch1
QUALIFY
(RANK() OVER (
order by col1) - 1 - 2) / COUNT(*) OVER () < 60 / 100
LIMIT NULL OFFSET 2;

-- Using WITH TIES clause
select * from
TableFetch1
FETCH FIRST 2 ROWS ONLY;

select * from
TableFetch1
QUALIFY
(ROW_NUMBER() OVER (
ORDER BY
NULL) - 1) / COUNT(*) OVER () < 20 / 100;

select * from
TableFetch1
offset 2 rows FETCH NEXT 2 ROWS ONLY;

select * from
TableFetch1
QUALIFY
(ROW_NUMBER() OVER (
ORDER BY
NULL) - 1 - 2) / COUNT(*) OVER () < 60 / 100
LIMIT NULL OFFSET 2;

-- Using ORDER BY clause
select * from
TableFetch1
order by col1
FETCH FIRST 2 ROWS ONLY;

select * from
TableFetch1
QUALIFY
(ROW_NUMBER() OVER (
order by col1) - 1) / COUNT(*) OVER () < 20 / 100;

select * from
TableFetch1
order by col1 offset 2 rows FETCH FIRST 2 ROWS ONLY;

select * from
TableFetch1
QUALIFY
(ROW_NUMBER() OVER (
order by col1) - 1 - 2) / COUNT(*) OVER () < 60 / 100
LIMIT NULL OFFSET 2;

select * from
TableFetch1
FETCH FIRST 1 ROWS ONLY;

select * from
TableFetch1
LIMIT NULL OFFSET 2;
```

Copy

Note

In Oracle, the `FETCH` / `OFFSET WITH TIES` is ignored when no `ORDER BY` is specified in the `SELECT`. This case will be transformed to a `FETCH` / `OFFSET` with the ONLY keyword in Snowflake, please note that in Snowflake the `ONLY` keyword has no effect in the results and is used just for readability.

## Pivot[¶](#pivot "Link to this heading")

Snowflake does not support the following statements:  
- Rename columns  
- Multiple Columns

### Oracle:[¶](#id9 "Link to this heading")

```
select * from schema1.table1
PIVOT(count(*) as count1 FOR (column1, column2) IN (row1 as rowName));
```

Copy

#### Snowflake:[¶](#id10 "Link to this heading")

```
select * from
schema1.table1
!!!RESOLVE EWI!!! /*** SSC-EWI-0015 - PIVOT/UNPIVOT RENAME COLUMN NOT SUPPORTED ***/!!!
PIVOT (count(*)
                !!!RESOLVE EWI!!! /*** SSC-EWI-0015 - PIVOT/UNPIVOT MULTIPLE COLUMN NOT SUPPORTED ***/!!!
                FOR (column1, column2)
!!!RESOLVE EWI!!! /*** SSC-EWI-0015 - PIVOT/UNPIVOT RENAME COLUMN NOT SUPPORTED ***/!!!
IN (row1 as rowName));
```

Copy

## Unpivot[¶](#unpivot "Link to this heading")

Snowflake does not support the following statements:  
- INCLUDE / EXCLUDE NULLS

### Oracle:[¶](#id11 "Link to this heading")

```
select * from schema1.table1 
UNPIVOT INCLUDE NULLS (column1 FOR column2 IN (ANY, ANY));
```

Copy

#### Snowflake:[¶](#id12 "Link to this heading")

```
select * from
schema1.table1
!!!RESOLVE EWI!!! /*** SSC-EWI-0015 - PIVOT/UNPIVOT INCLUDE NULLS NOT SUPPORTED ***/!!!
UNPIVOT ( column1 FOR column2 IN (
ANY,
ANY));
```

Copy

## Transformation of JOIN (+) to ANSI Syntax[¶](#transformation-of-join-to-ansi-syntax "Link to this heading")

Danger

This translation is currently deactivated and it’s only meant for reference for translations done with previous versions of SnowConvert AI. For the current translation check the section above.

SnowConvert AI translates the NON-ANSI special outer join (+) syntax to ANSI outer join syntax. This subsection shows some examples:

### To LEFT OUTER JOIN[¶](#to-left-outer-join "Link to this heading")

Example 1:

#### Oracle:[¶](#id13 "Link to this heading")

```
-- Additional Params: --OuterJoinsToOnlyAnsiSyntax
SELECT d.department_name,
       e.employee_name      
FROM   departments d, employees e
WHERE  d.department_id = e.department_id (+) 
AND    d.department_id >= 30;
```

Copy

#### Snowflake:[¶](#id14 "Link to this heading")

```
SELECT d.department_name,
       e.employee_name
FROM
       departments d
       LEFT OUTER JOIN
              employees e
              ON d.department_id = e.department_id
WHERE
       d.department_id >= 30;
```

Copy

Example 2:

#### Oracle:[¶](#id15 "Link to this heading")

```
-- Additional Params: --OuterJoinsToOnlyAnsiSyntax
SELECT d.department_name,
       e.employee_name      
FROM   departments d, employees e
WHERE  d.department_id(+)  = e.department_id 
AND    d.department_id >= 30;
```

Copy

#### Snowflake:[¶](#id16 "Link to this heading")

```
SELECT d.department_name,
       e.employee_name
FROM
       employees e
       LEFT OUTER JOIN
              departments d
              ON d.department_id = e.department_id
WHERE
       d.department_id >= 30;
```

Copy

Example 3: Multiple join

#### Oracle:[¶](#id17 "Link to this heading")

```
-- Additional Params: --OuterJoinsToOnlyAnsiSyntax
SELECT d.department_name,
       e.employee_name      
FROM   departments d, employees e, projects p
WHERE  e.department_id(+) = d.department_id
AND    p.department_id(+) = d.department_id
AND    d.department_id >= 30;
```

Copy

#### Snowflake:[¶](#id18 "Link to this heading")

```
SELECT d.department_name,
       e.employee_name
FROM
       departments d
       LEFT OUTER JOIN
              employees e
              ON e.department_id = d.department_id
       LEFT OUTER JOIN
              projects p
              ON p.department_id = d.department_id
WHERE
       d.department_id >= 30;
```

Copy

Example 4: Join with other kinds of conditional

#### Oracle:[¶](#id19 "Link to this heading")

```
-- Additional Params: --OuterJoinsToOnlyAnsiSyntax
SELECT d.department_name,
       e.employee_name      
FROM   departments d, employees e
WHERE  d.department_id(+)  = e.department_id 
AND    d.location(+) IN ('CHICAGO', 'BOSTON', 'NEW YORK')
AND    d.department_id >= 30;
```

Copy

#### Snowflake:[¶](#id20 "Link to this heading")

```
SELECT d.department_name,
       e.employee_name
FROM
       employees e
       LEFT OUTER JOIN
              departments d
              ON d.department_id = e.department_id
              AND d.location IN ('CHICAGO', 'BOSTON', 'NEW YORK')
WHERE
       d.department_id >= 30;
```

Copy

Example 5: Join with (+) inside a function

#### Oracle:[¶](#id21 "Link to this heading")

```
-- Additional Params: --OuterJoinsToOnlyAnsiSyntax
SELECT d.department_name,
       e.employee_name
FROM   departments d, employees e
WHERE SUBSTR(d.department_name, 1, NVL(e.department_id, 1) ) = e.employee_name(+);
```

Copy

#### Snowflake:[¶](#id22 "Link to this heading")

```
SELECT d.department_name,
       e.employee_name
FROM
       departments d
       LEFT OUTER JOIN
              employees e
              ON SUBSTR(d.department_name, 1, NVL(e.department_id, 1) ) = e.employee_name;
```

Copy

Warning

Please be aware that some of the patterns that were translated to LEFT OUTER JOIN could retrieve the rows in a different order.

### To CROSS JOIN[¶](#to-cross-join "Link to this heading")

Example 6: Complex case that requires the use of CROSS JOIN

#### Oracle:[¶](#id23 "Link to this heading")

```
SELECT d.department_name,
       e.employee_name,
       p.project_name,
       c.course_name 
FROM   departments d, employees e, projects p, courses c
WHERE
e.salary (+) >= 2000 AND
d.department_id = e.department_id (+)
AND p.department_id = e.department_id(+)
AND c.course_id  = e.department_id(+)
AND d.department_id >= 30;
```

Copy

#### Snowflake:[¶](#id24 "Link to this heading")

```
SELECT d.department_name,
       e.employee_name,
       p.project_name,
       c.course_name
FROM
       departments d
       CROSS JOIN projects p
       CROSS JOIN courses c
       LEFT OUTER JOIN
              employees e
              ON
              e.salary >= 2000
              AND
              d.department_id = e.department_id
              AND p.department_id = e.department_id
              AND c.course_id  = e.department_id
WHERE
       d.department_id >= 30;
```

Copy

## Hierarchical Queries[¶](#hierarchical-queries "Link to this heading")

Hierarchical queries in Snowflake allow to organize and retrieve data in a tree-like structure, typically using the [`CONNECT BY`](https://docs.snowflake.com/en/sql-reference/constructs/connect-by) clause. This clause Joins a table to itself to process hierarchical data in the table.

### Sample Source Patterns[¶](#sample-source-patterns "Link to this heading")

#### Oracle:[¶](#id25 "Link to this heading")

```
SELECT employee_ID, manager_ID, title
FROM employees
START WITH manager_ID = 1
CONNECT BY manager_ID = PRIOR employee_id;
```

Copy

#### Snowflake:[¶](#id26 "Link to this heading")

```
SELECT employee_ID, manager_ID, title
FROM
employees
START WITH manager_ID = 1
CONNECT BY
manager_ID = PRIOR employee_id;
```

Copy

### Related EWIs[¶](#related-ewis "Link to this heading")

1. [SSC-EWI-0015](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0015): Pivot/Unpivot multiple functions not supported.

## Select Flashback Query[¶](#select-flashback-query "Link to this heading")

### Description[¶](#description "Link to this heading")

**Oracle**

The flashback query claused in Oracle retrieves past data from a table, view, or materialized view. In Oracle, the uses can include:

* Restoring deleted data or undoing an incorrect commit, comparing current data with the corresponding data at an earlier time, checking the state of transactional data at a particular time, and reporting generation tools to past data, among others. ([Oracle Flashback query documentation](https://docs.oracle.com/cd/E11882_01/appdev.112/e41502/adfns_flashback.htm#ADFNS01003)).

**Snowflake**

The equivalent mechanism in Snowflake to query data from the past is the `AT | BEGIN` query. Notice that the only equivalent is for the `AS OF` statements.

Furthermore, Snowflake has complete “Time Travel” documentation that allows querying data to clone objects such as tables, views, and schemas. There are limitations on the days to access the past or deleted data (90 days before passing to Fail-safe status). For more information, review the [Snowflake Time Travel Documentation](https://docs.snowflake.com/en/user-guide/data-time-travel).

**Oracle syntax**

```
{ VERSIONS BETWEEN
  { SCN | TIMESTAMP }
  { expr | MINVALUE } AND { expr | MAXVALUE }
| AS OF { SCN | TIMESTAMP } expr
}
```

Copy

**Snowflake Syntax**

```
SELECT ...
FROM ...
  {
   AT( { TIMESTAMP => <timestamp> | OFFSET => <time_difference> | STATEMENT => <id> | STREAM => '<name>' } ) |
   BEFORE( STATEMENT => <id> )
  }
[ ... ]
```

Copy

Note

Notice that the query ID must reference a query executed within 14 days. If the query ID references a query over 14 days old, the following error is returned: `Error: statement <query_id> not found`. To work around this limitation, use the time stamp for the referenced query. ([Snowflake AT | Before documentation](https://docs.snowflake.com/en/sql-reference/constructs/at-before#syntax))

### Sample Source Patterns[¶](#id27 "Link to this heading")

The following data is used in the following examples to generate the query outputs.

#### Oracle[¶](#id28 "Link to this heading")

```
CREATE TABLE Employee (
    EmployeeID NUMBER PRIMARY KEY,
    FirstName VARCHAR2(50),
    LastName VARCHAR2(50),
    EmailAddress VARCHAR2(100),
    HireDate DATE,
    SalaryAmount NUMBER(10, 2)
);

INSERT INTO Employee VALUES (1, 'Bob', 'SampleNameA', 'sample@example.com', TO_DATE('2023-01-15', 'YYYY-MM-DD'), 11111.00);
INSERT INTO Employee VALUES (2, 'Bob', 'SampleNameB', 'sample@example.com', TO_DATE('2023-01-15', 'YYYY-MM-DD'), 11111.00);
INSERT INTO Employee VALUES (3, 'Bob', 'SampleNameC', 'sample@example.com', TO_DATE('2022-03-10', 'YYYY-MM-DD'), 11111.00);
INSERT INTO Employee VALUES (4, 'Bob', 'SampleNameD', 'sample@example.com', TO_DATE('2022-03-10', 'YYYY-MM-DD'), 11111.00);
INSERT INTO Employee VALUES (5, 'Bob', 'SampleNameE', 'sample@example.com', TO_DATE('2022-03-10', 'YYYY-MM-DD'), 11111.00);
```

Copy

##### Snowflake[¶](#id29 "Link to this heading")

```
CREATE OR REPLACE TABLE Employee (
       EmployeeID NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/ PRIMARY KEY,
       FirstName VARCHAR(50),
       LastName VARCHAR(50),
       EmailAddress VARCHAR(100),
       HireDate TIMESTAMP /*** SSC-FDM-OR0042 - DATE TYPE COLUMN HAS A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/,
       SalaryAmount NUMBER(10, 2) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/
   )
   COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
   ;

   INSERT INTO Employee
   VALUES (1, 'Bob', 'SampleNameA', 'sample@example.com', TO_DATE('2023-01-15', 'YYYY-MM-DD'), 11111.00);

   INSERT INTO Employee
   VALUES (2, 'Bob', 'SampleNameB', 'sample@example.com', TO_DATE('2023-01-15', 'YYYY-MM-DD'), 11111.00);

   INSERT INTO Employee
   VALUES (3, 'Bob', 'SampleNameC', 'sample@example.com', TO_DATE('2022-03-10', 'YYYY-MM-DD'), 11111.00);

   INSERT INTO Employee
   VALUES (4, 'Bob', 'SampleNameD', 'sample@example.com', TO_DATE('2022-03-10', 'YYYY-MM-DD'), 11111.00);

   INSERT INTO Employee
   VALUES (5, 'Bob', 'SampleNameE', 'sample@example.com', TO_DATE('2022-03-10', 'YYYY-MM-DD'), 11111.00);
```

Copy

#### 1. AS OF with TIMESTAMP case[¶](#as-of-with-timestamp-case "Link to this heading")

##### Oracle[¶](#id30 "Link to this heading")

```
SELECT * FROM employees
AS OF TIMESTAMP
TO_TIMESTAMP('2023-09-27 07:00:00', 'YYYY-MM-DD HH:MI:SS')
WHERE last_name = 'SampleName';
```

Copy

##### Snowflake[¶](#id31 "Link to this heading")

```
SELECT * FROM
employees
!!!RESOLVE EWI!!! /*** SSC-EWI-OR0135 - DATA RETENTION PERIOD MAY PRODUCE NO RESULTS ***/!!!
AT (TIMESTAMP =>
TO_TIMESTAMP('2023-09-27 07:00:00', 'YYYY-MM-DD HH:MI:SS'))
WHERE last_name = 'SampleName';
```

Copy

#### 2. AS OF with SCN case[¶](#as-of-with-scn-case "Link to this heading")

##### Oracle[¶](#id32 "Link to this heading")

```
SELECT * FROM employees
AS OF SCN
TO_TIMESTAMP('2023-09-27 07:00:00', 'YYYY-MM-DD HH:MI:SS')
WHERE last_name = 'SampleName';
```

Copy

##### Snowflake[¶](#id33 "Link to this heading")

```
SELECT * FROM
employees
!!!RESOLVE EWI!!! /*** SSC-EWI-0040 - THE 'FLASHBACK QUERY' CLAUSE IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
AS OF SCN
TO_TIMESTAMP('2023-09-27 07:00:00', 'YYYY-MM-DD HH:MI:SS')
WHERE last_name = 'SampleName';
```

Copy

### Known Issues[¶](#known-issues "Link to this heading")

1. The option when it is using SCN is not supported.
2. The VERSION statement is not supported in Snowflake.

### Related EWIS[¶](#id34 "Link to this heading")

1. [SSC-EWI-0040](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0040): Statement Not Supported.
2. [SSC-EWI-OR0135](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI.html#ssc-ewi-or0135): Current of clause is not supported in Snowflake.
3. [SSC-FDM-0006](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0006): Number type column may not behave similarly in Snowflake.
4. [SSC-FDM-OR0042](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM.html#ssc-fdm-or0042): Date Type Transformed To Timestamp Has A Different Behavior.

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

1. [Overall Select Translation](#overall-select-translation)
2. [Pivot](#pivot)
3. [Unpivot](#unpivot)
4. [Transformation of JOIN (+) to ANSI Syntax](#transformation-of-join-to-ansi-syntax)
5. [Hierarchical Queries](#hierarchical-queries)
6. [Select Flashback Query](#select-flashback-query)