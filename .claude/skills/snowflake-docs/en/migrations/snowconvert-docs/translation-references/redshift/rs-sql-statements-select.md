---
auto_generated: true
description: Returns rows from tables, views, and user-defined functions. (Redshift
  SQL Language Reference SELECT statement)
last_scraped: '2026-01-14T16:53:42.879717+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/redshift/rs-sql-statements-select
title: SnowConvert AI - Redshift - SELECT | Snowflake Documentation
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
          + [SQL Server-Azure Synapse](../transact/README.md)
          + [Sybase IQ](../sybase/README.md)
          + [Hive-Spark-Databricks SQL](../hive/README.md)
          + [Redshift](README.md)

            - [Basic Elements](redshift-basic-elements.md)
            - [Expressions](redshift-expressions.md)
            - [Conditions](redshift-conditions.md)
            - [Data types](redshift-data-types.md)
            - [SQL Statements](redshift-sql-statements.md)

              * [CONTINUE HANDLER](redshift-continue-handler.md)
              * [EXIT HANDLER](redshift-exit-handler.md)
              * [CREATE TABLE](redshift-sql-statements-create-table.md)
              * [CREATE TABLE AS](redshift-sql-statements-create-table-as.md)
              * [CREATE PROCEDURE](rs-sql-statements-create-procedure.md)
              * [SELECT](rs-sql-statements-select.md)
              * [SELECT INTO](rs-sql-statements-select-into.md)
            - [Functions](redshift-functions.md)
            - [System Catalog Tables](redshift-system-catalog.md)
            - ETL And BI Repointing

              - [Power BI Redshift Repointing](etl-bi-repointing/power-bi-redshift-repointing.md)
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)Translation References[Redshift](README.md)[SQL Statements](redshift-sql-statements.md)SELECT

# SnowConvert AI - Redshift - SELECT[¶](#snowconvert-ai-redshift-select "Link to this heading")

## SELECT[¶](#select "Link to this heading")

### Description[¶](#description "Link to this heading")

Returns rows from tables, views, and user-defined functions. ([Redshift SQL Language Reference SELECT statement](https://docs.aws.amazon.com/redshift/latest/dg/r_SELECT_synopsis.html))

### Grammar Syntax[¶](#grammar-syntax "Link to this heading")

```
 [ WITH with_subquery [, ...] ]
SELECT
[ TOP number | [ ALL | DISTINCT ]
* | expression [ AS output_name ] [, ...] ]
[ FROM table_reference [, ...] ]
[ WHERE condition ]
[ [ START WITH expression ] CONNECT BY expression ]
[ GROUP BY expression [, ...] ]
[ HAVING condition ]
[ QUALIFY condition ]
[ { UNION | ALL | INTERSECT | EXCEPT | MINUS } query ]
[ ORDER BY expression [ ASC | DESC ] ]
[ LIMIT { number | ALL } ]
[ OFFSET start ]
```

Copy

For more information please refer to each of the following links:

1. [WITH clause](#with-clause)
2. [SELECT list](#select-list)
3. [FROM clause](#from-clause)
4. [WHERE clause](#where-clause)
5. [CONNECT BY clause](#connect-by-clause)
6. [GROUP BY clause](#group-by-clause)
7. [HAVING clause](#having-clause)
8. [QUALIFY clause](#qualify-clause)
9. [UNION, INTERSECT, and EXCEPT](#union-intersect-and-except)
10. [ORDER BY clause](#order-by-clause)

## CONNECT BY clause[¶](#connect-by-clause "Link to this heading")

### Description[¶](#id1 "Link to this heading")

The `CONNECT BY` clause specifies the relationship between rows in a hierarchy. You can use `CONNECT BY` to select rows in a hierarchical order by joining the table to itself and processing the hierarchical data. ([Redshift SQL Language Reference CONNECT BY Clause](https://docs.aws.amazon.com/redshift/latest/dg/r_CONNECT_BY_clause.html))

Note

The [CONNECT BY clause](https://docs.snowflake.com/en/sql-reference/constructs/connect-by) is supported in Snowflake.

### Grammar Syntax[¶](#id2 "Link to this heading")

```
 [START WITH start_with_conditions]
CONNECT BY connect_by_conditions
```

Copy

### Sample Source Patterns[¶](#sample-source-patterns "Link to this heading")

#### Input Code:[¶](#input-code "Link to this heading")

##### Redshift[¶](#redshift "Link to this heading")

```
 CREATE TABLE employee (
  id INT,
  name VARCHAR(20),
  manager_id INT
);
  
INSERT INTO employee(id, name, manager_id) VALUES
(100, 'Carlos', null),
(101, 'John', 100),
(102, 'Jorge', 101),
(103, 'Kwaku', 101),
(110, 'Liu', 101),
(106, 'Mateo', 102),
(110, 'Nikki', 103),
(104, 'Paulo', 103),
(105, 'Richard', 103),
(120, 'Saanvi', 104),
(200, 'Shirley', 104),
(201, 'Sofía', 102),
(205, 'Zhang', 104);

SELECT COUNT(*)
FROM
Employee "start"
CONNECT BY PRIOR id = manager_id
START WITH name = 'John';
```

Copy

##### Results[¶](#results "Link to this heading")

| COUNT(\*) |
| --- |
| 12 |

##### Output Code:[¶](#output-code "Link to this heading")

##### Snowflake[¶](#snowflake "Link to this heading")

```
 CREATE TABLE employee (
  id INT,
  name VARCHAR(20),
  manager_id INT
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}';

INSERT INTO employee (id, name, manager_id) VALUES
(100, 'Carlos', null),
(101, 'John', 100),
(102, 'Jorge', 101),
(103, 'Kwaku', 101),
(110, 'Liu', 101),
(106, 'Mateo', 102),
(110, 'Nikki', 103),
(104, 'Paulo', 103),
(105, 'Richard', 103),
(120, 'Saanvi', 104),
(200, 'Shirley', 104),
(201, 'Sofía', 102),
(205, 'Zhang', 104);

SELECT
  COUNT(*)
FROM
  Employee "start"
CONNECT BY PRIOR id = manager_id
START WITH name = 'John';
```

Copy

##### Results[¶](#id3 "Link to this heading")

| COUNT(\*) |
| --- |
| 12 |

### Related EWIs[¶](#related-ewis "Link to this heading")

There are no known issues.

## FROM clause[¶](#from-clause "Link to this heading")

### Description[¶](#id4 "Link to this heading")

The `FROM` clause in a query lists the table references (tables, views, and subqueries) that data is selected from. If multiple table references are listed, the tables must be joined, using appropriate syntax in either the `FROM` clause or the `WHERE` clause. If no join criteria are specified, the system processes the query as a cross-join. ([Redshift SQL Language Reference FROM Clause](https://docs.aws.amazon.com/redshift/latest/dg/r_FROM_clause30.html))

Warning

The [FROM clause](https://docs.snowflake.com/en/sql-reference/constructs/from) is partially supported in Snowflake. [Object unpivoting](https://docs.aws.amazon.com/redshift/latest/dg/query-super.html#unpivoting) is not currently supported.

### Grammar Syntax[¶](#id5 "Link to this heading")

```
 FROM table_reference [, ...]

<table_reference> ::=
with_subquery_table_name [ table_alias ]
table_name [ * ] [ table_alias ]
( subquery ) [ table_alias ]
table_reference [ NATURAL ] join_type table_reference
   [ ON join_condition | USING ( join_column [, ...] ) ]
table_reference PIVOT ( 
   aggregate(expr) [ [ AS ] aggregate_alias ]
   FOR column_name IN ( expression [ AS ] in_alias [, ...] )
) [ table_alias ]
table_reference UNPIVOT [ INCLUDE NULLS | EXCLUDE NULLS ] ( 
   value_column_name 
   FOR name_column_name IN ( column_reference [ [ AS ]
   in_alias ] [, ...] )
) [ table_alias ]
UNPIVOT expression AS value_alias [ AT attribute_alias ]
```

Copy

### Sample Source Patterns[¶](#id6 "Link to this heading")

#### Join types[¶](#join-types "Link to this heading")

Snowflake supports all types of joins. For more information, see [the JOIN documentation.](https://docs.snowflake.com/en/sql-reference/constructs/join)

##### Input Code:[¶](#id7 "Link to this heading")

##### Redshift[¶](#id8 "Link to this heading")

```
 CREATE TABLE employee (
  id INT,
  name VARCHAR(20),
  manager_id INT
);
  
INSERT INTO employee(id, name, manager_id) VALUES
(100, 'Carlos', null),
(101, 'John', 100),
(102, 'Jorge', 101),
(103, 'Kwaku', 101),
(110, 'Liu', 101),
(106, 'Mateo', 102),
(110, 'Nikki', 103),
(104, 'Paulo', 103),
(105, 'Richard', 103),
(120, 'Saanvi', 104),
(200, 'Shirley', 104),
(201, 'Sofía', 102),
(205, 'Zhang', 104);

CREATE TABLE department (
    id INT,
    name VARCHAR(50),
    manager_id INT
);

INSERT INTO department(id, name, manager_id) VALUES
(1, 'HR', 100),
(2, 'Sales', 101),
(3, 'Engineering', 102),
(4, 'Marketing', 103);

SELECT e.name AS employee_name, d.name AS department_name
FROM employee e
INNER JOIN department d ON e.manager_id = d.manager_id;

SELECT e.name AS employee_name, d.name AS department_name
FROM employee e
LEFT JOIN department d ON e.manager_id = d.manager_id;

SELECT d.name AS department_name, e.name AS manager_name
FROM department d
RIGHT JOIN employee e ON d.manager_id = e.id;

SELECT e.name AS employee_name, d.name AS department_name
FROM employee e
FULL JOIN department d ON e.manager_id = d.manager_id;
```

Copy

##### Results[¶](#id9 "Link to this heading")

##### Inner Join[¶](#inner-join "Link to this heading")

| EMPLOYEE\_NAME | DEPARTMENT\_NAME |
| --- | --- |
| John | HR |
| Jorge | Sales |
| Kwaku | Sales |
| Liu | Sales |
| Mateo | Engineering |
| Nikki | Marketing |
| Paulo | Marketing |
| Richard | Marketing |
| Sofía | Engineering |

##### Left Join[¶](#left-join "Link to this heading")

| EMPLOYEE\_NAME | DEPARTMENT\_NAME |
| --- | --- |
| Carlos | null |
| John | HR |
| Jorge | Sales |
| Kwaku | Sales |
| Liu | Sales |
| Mateo | Engineering |
| Nikki | Marketing |
| Paulo | Marketing |
| Richard | Marketing |
| Saanvi | null |
| Shirley | null |
| Sofía | Engineering |
| Zhang | null |

##### Right Join[¶](#right-join "Link to this heading")

| DEPARTMENT\_NAME | MANAGER\_NAME |
| --- | --- |
| HR | Carlos |
| Sales | John |
| Engineering | Jorge |
| Marketing | Kwaku |
| null | Liu |
| null | Mateo |
| null | Nikki |
| null | Paulo |
| null | Richard |
| null | Saanvi |
| null | Shirley |
| null | Sofía |
| null | Zhang |

##### Full Join[¶](#full-join "Link to this heading")

| EMPLOYEE\_NAME | DEPARTMENT\_NAME |
| --- | --- |
| Carlos | null |
| John | HR |
| Jorge | Sales |
| Kwaku | Sales |
| Liu | Sales |
| Mateo | Engineering |
| Nikki | Marketing |
| Paulo | Marketing |
| Richard | Marketing |
| Saanvi | null |
| Shirley | null |
| Sofía | Engineering |
| Zhang | null |

##### Output Code:[¶](#id10 "Link to this heading")

##### Snowflake[¶](#id11 "Link to this heading")

```
 CREATE TABLE employee (
  id INT,
  name VARCHAR(20),
  manager_id INT
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "11/05/2024",  "domain": "test" }}';

INSERT INTO employee (id, name, manager_id) VALUES
(100, 'Carlos', null),
(101, 'John', 100),
(102, 'Jorge', 101),
(103, 'Kwaku', 101),
(110, 'Liu', 101),
(106, 'Mateo', 102),
(110, 'Nikki', 103),
(104, 'Paulo', 103),
(105, 'Richard', 103),
(120, 'Saanvi', 104),
(200, 'Shirley', 104),
(201, 'Sofía', 102),
(205, 'Zhang', 104);

CREATE TABLE department (
    id INT,
    name VARCHAR(50),
    manager_id INT
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "11/05/2024",  "domain": "test" }}';

INSERT INTO department (id, name, manager_id) VALUES
(1, 'HR', 100),
(2, 'Sales', 101),
(3, 'Engineering', 102),
(4, 'Marketing', 103);

SELECT e.name AS employee_name, d.name AS department_name
FROM
employee e
INNER JOIN
  department d ON e.manager_id = d.manager_id;

SELECT e.name AS employee_name, d.name AS department_name
FROM
employee e
LEFT JOIN
  department d ON e.manager_id = d.manager_id;

SELECT d.name AS department_name, e.name AS manager_name
FROM
department d
RIGHT JOIN
  employee e ON d.manager_id = e.id;

SELECT e.name AS employee_name, d.name AS department_name
FROM
employee e
FULL JOIN
  department d ON e.manager_id = d.manager_id;
```

Copy

##### Results[¶](#id12 "Link to this heading")

##### Inner Join[¶](#id13 "Link to this heading")

| EMPLOYEE\_NAME | DEPARTMENT\_NAME |
| --- | --- |
| John | HR |
| Jorge | Sales |
| Kwaku | Sales |
| Liu | Sales |
| Mateo | Engineering |
| Nikki | Marketing |
| Paulo | Marketing |
| Richard | Marketing |
| Sofía | Engineering |

##### Left Join[¶](#id14 "Link to this heading")

| EMPLOYEE\_NAME | DEPARTMENT\_NAME |
| --- | --- |
| Carlos | null |
| John | HR |
| Jorge | Sales |
| Kwaku | Sales |
| Liu | Sales |
| Mateo | Engineering |
| Nikki | Marketing |
| Paulo | Marketing |
| Richard | Marketing |
| Saanvi | null |
| Shirley | null |
| Sofía | Engineering |
| Zhang | null |

##### Right Join[¶](#id15 "Link to this heading")

| DEPARTMENT\_NAME | MANAGER\_NAME |
| --- | --- |
| HR | Carlos |
| Sales | John |
| Engineering | Jorge |
| Marketing | Kwaku |
| null | Liu |
| null | Mateo |
| null | Nikki |
| null | Paulo |
| null | Richard |
| null | Saanvi |
| null | Shirley |
| null | Sofía |
| null | Zhang |

##### Full Join[¶](#id16 "Link to this heading")

| EMPLOYEE\_NAME | DEPARTMENT\_NAME |
| --- | --- |
| Carlos | null |
| John | HR |
| Jorge | Sales |
| Kwaku | Sales |
| Liu | Sales |
| Mateo | Engineering |
| Nikki | Marketing |
| Paulo | Marketing |
| Richard | Marketing |
| Saanvi | null |
| Shirley | null |
| Sofía | Engineering |
| Zhang | null |

#### Pivot Clause[¶](#pivot-clause "Link to this heading")

Note

Column aliases cannot be used in the IN clause of the PIVOT query in Snowflake.

##### Input Code:[¶](#id17 "Link to this heading")

##### Redshift[¶](#id18 "Link to this heading")

```
 SELECT *
FROM
    (SELECT e.manager_id, d.name AS department, e.id AS employee_id
     FROM employee e
     JOIN department d ON e.manager_id = d.manager_id) AS SourceTable
PIVOT
    (
     COUNT(employee_id)
     FOR department IN ('HR', 'Sales', 'Engineering', 'Marketing')
    ) AS PivotTable;
```

Copy

##### Results[¶](#id19 "Link to this heading")

| MANAGER\_ID | ‘HR’ | ‘Sales’ | ‘Engineering’ | ‘Marketing’ |
| --- | --- | --- | --- | --- |
| 100 | 1 | 0 | 0 | 0 |
| 101 | 0 | 3 | 0 | 0 |
| 102 | 0 | 0 | 2 | 0 |
| 103 | 0 | 0 | 0 | 3 |

##### Output Code:[¶](#id20 "Link to this heading")

##### Snowflake[¶](#id21 "Link to this heading")

```
 SELECT *
FROM
    (SELECT e.manager_id, d.name AS department, e.id AS employee_id
     FROM
     employee e
     JOIN
         department d ON e.manager_id = d.manager_id) AS SourceTable
PIVOT
    (
     COUNT(employee_id)
     FOR department IN ('HR', 'Sales', 'Engineering', 'Marketing')
    ) AS PivotTable;
```

Copy

##### Results[¶](#id22 "Link to this heading")

| MANAGER\_ID | ‘HR’ | ‘Sales’ | ‘Engineering’ | ‘Marketing’ |
| --- | --- | --- | --- | --- |
| 100 | 1 | 0 | 0 | 0 |
| 101 | 0 | 3 | 0 | 0 |
| 102 | 0 | 0 | 2 | 0 |
| 103 | 0 | 0 | 0 | 3 |

#### Unpivot Clause[¶](#unpivot-clause "Link to this heading")

Note

Column aliases cannot be used in the IN clause of the UNPIVOT query in Snowflake.

##### Input Code:[¶](#id23 "Link to this heading")

##### Redshift[¶](#id24 "Link to this heading")

```
 CREATE TABLE count_by_color (quality VARCHAR, red INT, green INT, blue INT);

INSERT INTO count_by_color VALUES ('high', 15, 20, 7);
INSERT INTO count_by_color VALUES ('normal', 35, NULL, 40);
INSERT INTO count_by_color VALUES ('low', 10, 23, NULL);


SELECT *
FROM (SELECT red, green, blue FROM count_by_color) UNPIVOT (
    cnt FOR color IN (red, green, blue)
);

SELECT *
FROM (SELECT red, green, blue FROM count_by_color) UNPIVOT (
    cnt FOR color IN (red r, green as g, blue)
);
```

Copy

##### Results[¶](#id25 "Link to this heading")

| COLOR | CNT |
| --- | --- |
| RED | 15 |
| RED | 35 |
| RED | 10 |
| GREEN | 20 |
| GREEN | 23 |
| BLUE | 7 |
| BLUE | 40 |

##### Output Code:[¶](#id26 "Link to this heading")

##### Snowflake[¶](#id27 "Link to this heading")

```
 CREATE TABLE count_by_color (quality VARCHAR, red INT, green INT, blue INT)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "11/05/2024",  "domain": "test" }}';

INSERT INTO count_by_color
VALUES ('high', 15, 20, 7);
INSERT INTO count_by_color
VALUES ('normal', 35, NULL, 40);
INSERT INTO count_by_color
VALUES ('low', 10, 23, NULL);


SELECT *
FROM (SELECT red, green, blue FROM
            count_by_color
    ) UNPIVOT (
    cnt FOR color IN (red, green, blue)
);

SELECT *
FROM (SELECT red, green, blue FROM
            count_by_color
) UNPIVOT (
    cnt FOR color IN (red
                          !!!RESOLVE EWI!!! /*** SSC-EWI-RS0005 - COLUMN ALIASES CANNOT BE USED IN THE IN CLAUSE OF THE PIVOT/UNPIVOT QUERY IN SNOWFLAKE. ***/!!!
 r, green
          !!!RESOLVE EWI!!! /*** SSC-EWI-RS0005 - COLUMN ALIASES CANNOT BE USED IN THE IN CLAUSE OF THE PIVOT/UNPIVOT QUERY IN SNOWFLAKE. ***/!!!
 as g, blue)
);
```

Copy

##### Results[¶](#id28 "Link to this heading")

| COLOR | CNT |
| --- | --- |
| RED | 15 |
| GREEN | 20 |
| BLUE | 7 |
| RED | 35 |
| BLUE | 40 |
| RED | 10 |
| GREEN | 23 |

### Related EWIs[¶](#id29 "Link to this heading")

1. [SSC-EWI-RS0005](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/redshiftEWI.html#ssc-ewi-rs0005): Column aliases cannot be used in the IN clause of the PIVOT/UNPIVOT query in Snowflake.

## GROUP BY clause[¶](#group-by-clause "Link to this heading")

### Description[¶](#id30 "Link to this heading")

The `GROUP BY` clause identifies the grouping columns for the query. Grouping columns must be declared when the query computes aggregates with standard functions such as `SUM`, `AVG`, and `COUNT`. ([Redshift SQL Language Reference GROUP BY Clause](https://docs.aws.amazon.com/redshift/latest/dg/r_GROUP_BY_clause.html))

Note

The [GROUP BY clause](https://docs.snowflake.com/en/sql-reference/constructs/group-by) is fully supported in Snowflake.

### Grammar Syntax[¶](#id31 "Link to this heading")

```
 GROUP BY group_by_clause [, ...]

group_by_clause := {
    expr |
    GROUPING SETS ( () | group_by_clause [, ...] ) |
    ROLLUP ( expr [, ...] ) |
    CUBE ( expr [, ...] )
    }
```

Copy

### Sample Source Patterns[¶](#id32 "Link to this heading")

#### Grouping sets[¶](#grouping-sets "Link to this heading")

##### Input Code:[¶](#id33 "Link to this heading")

##### Redshift[¶](#id34 "Link to this heading")

```
 CREATE TABLE employee (
  id INT,
  name VARCHAR(20),
  manager_id INT
);
  
INSERT INTO employee(id, name, manager_id) VALUES
(100, 'Carlos', null),
(101, 'John', 100),
(102, 'Jorge', 101),
(103, 'Kwaku', 101),
(110, 'Liu', 101),
(106, 'Mateo', 102),
(110, 'Nikki', 103),
(104, 'Paulo', 103),
(105, 'Richard', 103),
(120, 'Saanvi', 104),
(200, 'Shirley', 104),
(201, 'Sofía', 102),
(205, 'Zhang', 104);

SELECT 
    manager_id,
    COUNT(id) AS total_employees
FROM employee
GROUP BY GROUPING SETS 
    ((manager_id), ())
ORDER BY manager_id;
```

Copy

##### Results[¶](#id35 "Link to this heading")

| MANAGER\_ID | TOTAL\_EMPLOYEES |
| --- | --- |
| 100 | 1 |
| 101 | 3 |
| 102 | 2 |
| 103 | 3 |
| 104 | 3 |
| null | 1 |
| null | 13 |

##### Output Code:[¶](#id36 "Link to this heading")

##### Snowflake[¶](#id37 "Link to this heading")

```
 CREATE TABLE employee (
  id INT,
  name VARCHAR(20),
  manager_id INT
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "11/05/2024",  "domain": "test" }}';

INSERT INTO employee (id, name, manager_id) VALUES
(100, 'Carlos', null),
(101, 'John', 100),
(102, 'Jorge', 101),
(103, 'Kwaku', 101),
(110, 'Liu', 101),
(106, 'Mateo', 102),
(110, 'Nikki', 103),
(104, 'Paulo', 103),
(105, 'Richard', 103),
(120, 'Saanvi', 104),
(200, 'Shirley', 104),
(201, 'Sofía', 102),
(205, 'Zhang', 104);

SELECT
    manager_id,
    COUNT(id) AS total_employees
FROM
    employee
GROUP BY GROUPING SETS
    ((manager_id), ())
ORDER BY manager_id;
```

Copy

##### Results[¶](#id38 "Link to this heading")

| MANAGER\_ID | TOTAL\_EMPLOYEES |
| --- | --- |
| 100 | 1 |
| 101 | 3 |
| 102 | 2 |
| 103 | 3 |
| 104 | 3 |
| null | 1 |
| null | 13 |

#### Group by Cube[¶](#group-by-cube "Link to this heading")

##### Input Code:[¶](#id39 "Link to this heading")

##### Redshift[¶](#id40 "Link to this heading")

```
 SELECT
    manager_id,
    COUNT(id) AS total_employees
FROM
    employee
GROUP BY CUBE(manager_id)
ORDER BY manager_id;
```

Copy

##### Results[¶](#id41 "Link to this heading")

| MANAGER\_ID | TOTAL\_EMPLOYEES |
| --- | --- |
| 100 | 1 |
| 101 | 3 |
| 102 | 2 |
| 103 | 3 |
| 104 | 3 |
| null | 1 |
| null | 13 |

##### Output Code:[¶](#id42 "Link to this heading")

##### Snowflake[¶](#id43 "Link to this heading")

```
 SELECT
    manager_id,
    COUNT(id) AS total_employees
FROM
    employee
GROUP BY CUBE(manager_id)
ORDER BY manager_id;
```

Copy

##### Results[¶](#id44 "Link to this heading")

| MANAGER\_ID | TOTAL\_EMPLOYEES |
| --- | --- |
| 100 | 1 |
| 101 | 3 |
| 102 | 2 |
| 103 | 3 |
| 104 | 3 |
| null | 1 |
| null | 13 |

#### Group by Rollup[¶](#group-by-rollup "Link to this heading")

##### Input Code:[¶](#id45 "Link to this heading")

##### Redshift[¶](#id46 "Link to this heading")

```
 SELECT
    manager_id,
    COUNT(id) AS total_employees
FROM
    employee
GROUP BY ROLLUP(manager_id)
ORDER BY manager_id;
```

Copy

##### Results[¶](#id47 "Link to this heading")

| MANAGER\_ID | TOTAL\_EMPLOYEES |
| --- | --- |
| 100 | 1 |
| 101 | 3 |
| 102 | 2 |
| 103 | 3 |
| 104 | 3 |
| null | 1 |
| null | 13 |

##### Output Code:[¶](#id48 "Link to this heading")

##### Snowflake[¶](#id49 "Link to this heading")

```
 SELECT
    manager_id,
    COUNT(id) AS total_employees
FROM
    employee
GROUP BY ROLLUP(manager_id)
ORDER BY manager_id;
```

Copy

##### Results[¶](#id50 "Link to this heading")

| MANAGER\_ID | TOTAL\_EMPLOYEES |
| --- | --- |
| 100 | 1 |
| 101 | 3 |
| 102 | 2 |
| 103 | 3 |
| 104 | 3 |
| null | 1 |
| null | 13 |

### Related EWIs[¶](#id51 "Link to this heading")

There are no known issues.

## HAVING clause[¶](#having-clause "Link to this heading")

### Description[¶](#id52 "Link to this heading")

The `HAVING` clause applies a condition to the intermediate grouped result set that a query returns. ([Redshift SQL Language Reference HAVING Clause](https://docs.aws.amazon.com/redshift/latest/dg/r_HAVING_clause.html))

Note

The [HAVING clause](https://docs.snowflake.com/en/sql-reference/constructs/having) is fully supported in Snowflake.

### Grammar Syntax[¶](#id53 "Link to this heading")

```
 [ HAVING condition ]
```

Copy

### Sample Source Patterns[¶](#id54 "Link to this heading")

#### Input Code:[¶](#id55 "Link to this heading")

##### Redshift[¶](#id56 "Link to this heading")

```
 CREATE TABLE employee (
  id INT,
  name VARCHAR(20),
  manager_id INT
);
  
INSERT INTO employee(id, name, manager_id) VALUES
(100, 'Carlos', null),
(101, 'John', 100),
(102, 'Jorge', 101),
(103, 'Kwaku', 101),
(110, 'Liu', 101),
(106, 'Mateo', 102),
(110, 'Nikki', 103),
(104, 'Paulo', 103),
(105, 'Richard', 103),
(120, 'Saanvi', 104),
(200, 'Shirley', 104),
(201, 'Sofía', 102),
(205, 'Zhang', 104);

SELECT manager_id, COUNT(id) AS total_employees
FROM
employee
GROUP BY manager_id
HAVING COUNT(id) > 2
ORDER BY manager_id;
```

Copy

##### Results[¶](#id57 "Link to this heading")

| MANAGER\_ID | TOTAL\_EMPLOYEES |
| --- | --- |
| 101 | 3 |
| 103 | 3 |
| 104 | 3 |

##### Output Code:[¶](#id58 "Link to this heading")

##### Snowflake[¶](#id59 "Link to this heading")

```
 CREATE TABLE employee (
  id INT,
  name VARCHAR(20),
  manager_id INT
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "11/05/2024",  "domain": "test" }}';

INSERT INTO employee (id, name, manager_id) VALUES
(100, 'Carlos', null),
(101, 'John', 100),
(102, 'Jorge', 101),
(103, 'Kwaku', 101),
(110, 'Liu', 101),
(106, 'Mateo', 102),
(110, 'Nikki', 103),
(104, 'Paulo', 103),
(105, 'Richard', 103),
(120, 'Saanvi', 104),
(200, 'Shirley', 104),
(201, 'Sofía', 102),
(205, 'Zhang', 104);

SELECT manager_id, COUNT(id) AS total_employees
FROM
employee
GROUP BY manager_id
HAVING COUNT(id) > 2
ORDER BY manager_id;
```

Copy

##### Results[¶](#id60 "Link to this heading")

| MANAGER\_ID | TOTAL\_EMPLOYEES |
| --- | --- |
| 101 | 3 |
| 103 | 3 |
| 104 | 3 |

### Related EWIs[¶](#id61 "Link to this heading")

There are no known issues.

## ORDER BY clause[¶](#order-by-clause "Link to this heading")

### Description[¶](#id62 "Link to this heading")

The `ORDER BY` clause sorts the result set of a query. ([Redshift SQL Language Reference Order By Clause](https://docs.aws.amazon.com/redshift/latest/dg/r_ORDER_BY_clause.html))

Note

The [ORDER BY clause](https://docs.snowflake.com/en/sql-reference/constructs/order-by) is fully supported in Snowflake.

### Grammar Syntax[¶](#id63 "Link to this heading")

```
 [ ORDER BY expression [ ASC | DESC ] ]
[ NULLS FIRST | NULLS LAST ]
[ LIMIT { count | ALL } ]
[ OFFSET start ]
```

Copy

### Sample Source Patterns[¶](#id64 "Link to this heading")

#### Input Code:[¶](#id65 "Link to this heading")

##### Redshift[¶](#id66 "Link to this heading")

```
 CREATE TABLE employee (
    id INT,
    name VARCHAR(20),
    manager_id INT,
    salary DECIMAL(10, 2)
);

INSERT INTO employee (id, name, manager_id, salary) VALUES
(100, 'Carlos', NULL, 120000.00),
(101, 'John', 100, 90000.00),
(102, 'Jorge', 101, 95000.00),
(103, 'Kwaku', 101, 105000.00),
(104, 'Paulo', 102, 110000.00),
(105, 'Richard', 102, 85000.00),
(106, 'Mateo', 103, 95000.00),
(107, 'Liu', 103, 108000.00),
(108, 'Zhang', 104, 95000.00);

SELECT id, name, manager_id, salary
FROM employee
ORDER BY salary DESC NULLS LAST, name ASC NULLS FIRST
LIMIT 5                                        
OFFSET 2;
```

Copy

##### Results[¶](#id67 "Link to this heading")

| ID | NAME | MANAGER\_ID | SALARY |
| --- | --- | --- | --- |
| 107 | Liu | 103 | 108000.00 |
| 103 | Kwaku | 101 | 105000.00 |
| 102 | Jorge | 101 | 95000.00 |
| 106 | Mateo | 103 | 95000.00 |
| 108 | Zhang | 104 | 95000.00 |

##### Output Code:[¶](#id68 "Link to this heading")

##### Snowflake[¶](#id69 "Link to this heading")

```
 CREATE TABLE employee (
    id INT,
    name VARCHAR(20),
    manager_id INT,
    salary DECIMAL(10, 2)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "11/05/2024",  "domain": "test" }}';

INSERT INTO employee (id, name, manager_id, salary) VALUES
(100, 'Carlos', NULL, 120000.00),
(101, 'John', 100, 90000.00),
(102, 'Jorge', 101, 95000.00),
(103, 'Kwaku', 101, 105000.00),
(104, 'Paulo', 102, 110000.00),
(105, 'Richard', 102, 85000.00),
(106, 'Mateo', 103, 95000.00),
(107, 'Liu', 103, 108000.00),
(108, 'Zhang', 104, 95000.00);

SELECT id, name, manager_id, salary
FROM
    employee
ORDER BY salary DESC NULLS LAST, name ASC NULLS FIRST
LIMIT 5
OFFSET 2;
```

Copy

##### Results[¶](#id70 "Link to this heading")

| ID | NAME | MANAGER\_ID | SALARY |
| --- | --- | --- | --- |
| 107 | Liu | 103 | 108000.00 |
| 103 | Kwaku | 101 | 105000.00 |
| 102 | Jorge | 101 | 95000.00 |
| 106 | Mateo | 103 | 95000.00 |
| 108 | Zhang | 104 | 95000.00 |

### Related EWIs[¶](#id71 "Link to this heading")

There are no known issues.

## QUALIFY clause[¶](#qualify-clause "Link to this heading")

### Description[¶](#id72 "Link to this heading")

The `QUALIFY` clause filters results of a previously computed window function according to user‑specified search conditions. You can use the clause to apply filtering conditions to the result of a window function without using a subquery. ([Redshift SQL Language Reference QUALIFY Clause](https://docs.aws.amazon.com/redshift/latest/dg/r_QUALIFY_clause.html))

Note

The [QUALIFY clause](https://docs.snowflake.com/en/sql-reference/constructs/qualify) is supported in Snowflake.

### Grammar Syntax[¶](#id73 "Link to this heading")

```
 QUALIFY condition
```

Copy

### Sample Source Patterns[¶](#id74 "Link to this heading")

#### Input Code:[¶](#id75 "Link to this heading")

##### Redshift[¶](#id76 "Link to this heading")

```
 CREATE TABLE store_sales 
(
    ss_sold_date DATE, 
    ss_sold_time TIME, 
    ss_item TEXT, 
    ss_sales_price FLOAT
);

INSERT INTO store_sales VALUES ('2022-01-01', '09:00:00', 'Product 1', 100.0),
                               ('2022-01-01', '11:00:00', 'Product 2', 500.0),
                               ('2022-01-01', '15:00:00', 'Product 3', 20.0),
                               ('2022-01-01', '17:00:00', 'Product 4', 1000.0),
                               ('2022-01-01', '18:00:00', 'Product 5', 30.0),
                               ('2022-01-02', '10:00:00', 'Product 6', 5000.0),
                               ('2022-01-02', '16:00:00', 'Product 7', 5.0);

SELECT *
FROM store_sales ss
WHERE ss_sold_time > time '12:00:00'
QUALIFY row_number()
OVER (PARTITION BY ss_sold_date ORDER BY ss_sales_price DESC) <= 2;
```

Copy

##### Results[¶](#id77 "Link to this heading")

| SS\_SOLD\_DATE | SS\_SOLD\_TIME | SS\_ITEM | SS\_SALES\_PRICE |
| --- | --- | --- | --- |
| 2022-01-01 | 17:00:00 | Product 4 | 1000 |
| 2022-01-01 | 18:00:00 | Product 5 | 30 |
| 2022-01-02 | 16:00:00 | Product 7 | 5 |

##### Output Code:[¶](#id78 "Link to this heading")

##### Snowflake[¶](#id79 "Link to this heading")

```
 CREATE TABLE store_sales
(
    ss_sold_date DATE,
    ss_sold_time TIME,
    ss_item TEXT,
    ss_sales_price FLOAT
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}';

INSERT INTO store_sales
VALUES ('2022-01-01', '09:00:00', 'Product 1', 100.0),
                               ('2022-01-01', '11:00:00', 'Product 2', 500.0),
                               ('2022-01-01', '15:00:00', 'Product 3', 20.0),
                               ('2022-01-01', '17:00:00', 'Product 4', 1000.0),
                               ('2022-01-01', '18:00:00', 'Product 5', 30.0),
                               ('2022-01-02', '10:00:00', 'Product 6', 5000.0),
                               ('2022-01-02', '16:00:00', 'Product 7', 5.0);

SELECT *
FROM
    store_sales ss
WHERE ss_sold_time > time '12:00:00'
QUALIFY
    ROW_NUMBER()
OVER (PARTITION BY ss_sold_date ORDER BY ss_sales_price DESC) <= 2;
```

Copy

##### Results[¶](#id80 "Link to this heading")

| SS\_SOLD\_DATE | SS\_SOLD\_TIME | SS\_ITEM | SS\_SALES\_PRICE |
| --- | --- | --- | --- |
| 2022-01-02 | 16:00:00 | Product 7 | 5 |
| 2022-01-01 | 17:00:00 | Product 4 | 1000 |
| 2022-01-01 | 18:00:00 | Product 5 | 30 |

### Related EWIs[¶](#id81 "Link to this heading")

There are no known issues.

## SELECT list[¶](#select-list "Link to this heading")

### Description[¶](#id82 "Link to this heading")

> The SELECT list names the columns, functions, and expressions that you want the query to return. The list represents the output of the query. ([Redshift SQL Language Reference SELECT list](https://docs.aws.amazon.com/redshift/latest/dg/r_SELECT_list.html))

Note

The [query start options](https://docs.snowflake.com/en/sql-reference/sql/select) are fully supported in Snowflake. Just keep in mind that in Snowflake the `DISTINCT` and `ALL` options must go at the beginning of the query.

Note

In Redshift, if your application allows foreign keys or invalid primary keys, it can cause queries to return incorrect results. For example, a SELECT DISTINCT query could return duplicate rows if the primary key column does not contain all unique values. ([Redshift SQL Language Reference SELECT list](https://docs.aws.amazon.com/redshift/latest/dg/r_SELECT_list.html))

### Grammar Syntax[¶](#id83 "Link to this heading")

```
 SELECT
[ TOP number ]
[ ALL | DISTINCT ] * | expression [ AS column_alias ] [, ...]
```

Copy

### Sample Source Patterns[¶](#id84 "Link to this heading")

#### Top clause[¶](#top-clause "Link to this heading")

##### Input Code:[¶](#id85 "Link to this heading")

##### Redshift[¶](#id86 "Link to this heading")

```
 CREATE TABLE employee (
  id INT,
  name VARCHAR(20),
  manager_id INT
);
  
INSERT INTO employee(id, name, manager_id) VALUES
(100, 'Carlos', null),
(101, 'John', 100),
(102, 'Jorge', 101),
(103, 'Kwaku', 101),
(110, 'Liu', 101),
(106, 'Mateo', 102),
(110, 'Nikki', 103),
(104, 'Paulo', 103),
(105, 'Richard', 103),
(120, 'Saanvi', 104),
(200, 'Shirley', 104),
(201, 'Sofía', 102),
(205, 'Zhang', 104);
  
SELECT TOP 5 id, name, manager_id
FROM employee;
```

Copy

##### Results[¶](#id87 "Link to this heading")

| ID | NAME | MANAGER\_ID |
| --- | --- | --- |
| 100 | Carlos | null |
| 101 | John | 100 |
| 102 | Jorge | 101 |
| 103 | Kwaku | 101 |
| 110 | Liu | 101 |

##### Output Code:[¶](#id88 "Link to this heading")

##### Snowflake[¶](#id89 "Link to this heading")

```
 CREATE TABLE employee (
  id INT,
  name VARCHAR(20),
  manager_id INT
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "11/05/2024",  "domain": "test" }}';

INSERT INTO employee (id, name, manager_id) VALUES
(100, 'Carlos', null),
(101, 'John', 100),
(102, 'Jorge', 101),
(103, 'Kwaku', 101),
(110, 'Liu', 101),
(106, 'Mateo', 102),
(110, 'Nikki', 103),
(104, 'Paulo', 103),
(105, 'Richard', 103),
(120, 'Saanvi', 104),
(200, 'Shirley', 104),
(201, 'Sofía', 102),
(205, 'Zhang', 104);

SELECT TOP 5 id, name, manager_id
FROM
    employee;
```

Copy

##### Results[¶](#id90 "Link to this heading")

| ID | NAME | MANAGER\_ID |
| --- | --- | --- |
| 100 | Carlos | null |
| 101 | John | 100 |
| 102 | Jorge | 101 |
| 103 | Kwaku | 101 |
| 110 | Liu | 101 |

#### ALL [¶](#all "Link to this heading")

##### Input Code:[¶](#id91 "Link to this heading")

##### Redshift[¶](#id92 "Link to this heading")

```
SELECT ALL manager_id
FROM employee;
```

Copy

##### Results[¶](#id93 "Link to this heading")

| MANAGER\_ID |
| --- |
| null |
| 100 |
| 101 |
| 101 |
| 101 |
| 102 |
| 103 |
| 103 |
| 103 |
| 104 |
| 104 |
| 102 |
| 104 |

##### Output Code:[¶](#id94 "Link to this heading")

##### Snowflake[¶](#id95 "Link to this heading")

```
 SELECT ALL manager_id
FROM
    employee;
```

Copy

##### Results[¶](#id96 "Link to this heading")

| MANAGER\_ID |
| --- |
| null |
| 100 |
| 101 |
| 101 |
| 101 |
| 102 |
| 103 |
| 103 |
| 103 |
| 104 |
| 104 |
| 102 |
| 104 |

#### DISTINCT[¶](#distinct "Link to this heading")

##### Input Code:[¶](#id97 "Link to this heading")

##### Redshift[¶](#id98 "Link to this heading")

```
SELECT DISTINCT manager_id
FROM employee;
```

Copy

##### Results[¶](#id99 "Link to this heading")

| MANAGER\_ID |
| --- |
| null |
| 100 |
| 101 |
| 102 |
| 103 |
| 104 |

##### Output Code:[¶](#id100 "Link to this heading")

##### Snowflake[¶](#id101 "Link to this heading")

```
SELECT DISTINCT manager_id
FROM 
    employee;
```

Copy

##### Results[¶](#id102 "Link to this heading")

| MANAGER\_ID |
| --- |
| null |
| 100 |
| 101 |
| 102 |
| 103 |
| 104 |

### Related EWIs[¶](#id103 "Link to this heading")

There are no known issues.

## UNION, INTERSECT, and EXCEPT[¶](#union-intersect-and-except "Link to this heading")

### Description[¶](#id104 "Link to this heading")

The `UNION`, `INTERSECT`, and `EXCEPT` *set operators* are used to compare and merge the results of two separate query expressions. ([Redshift SQL Language Reference Set Operators](https://docs.aws.amazon.com/redshift/latest/dg/r_UNION.html))

Note

[Set operators](https://docs.snowflake.com/en/sql-reference/operators-query) are fully supported in Snowflake.

### Grammar Syntax[¶](#id105 "Link to this heading")

```
 query
{ UNION [ ALL ] | INTERSECT | EXCEPT | MINUS }
query
```

Copy

### Sample Source Patterns[¶](#id106 "Link to this heading")

#### Input Code:[¶](#id107 "Link to this heading")

##### Redshift[¶](#id108 "Link to this heading")

```
 SELECT id, name, manager_id
FROM
employee
WHERE manager_id = 101

UNION

SELECT id, name, manager_id
FROM
employee
WHERE manager_id = 102

UNION ALL

SELECT id, name, manager_id
FROM
employee
WHERE manager_id = 101

INTERSECT

SELECT id, name, manager_id
FROM
employee
WHERE manager_id = 103

EXCEPT

SELECT id, name, manager_id
FROM
employee
WHERE manager_id = 104;
```

Copy

##### Results[¶](#id109 "Link to this heading")

| ID | NAME | MANAGER\_ID |
| --- | --- | --- |
| 103 | Kwaku | 101 |
| 110 | Liu | 101 |
| 102 | Jorge | 101 |
| 106 | Mateo | 102 |
| 201 | Sofía | 102 |

##### Output Code:[¶](#id110 "Link to this heading")

##### Snowflake[¶](#id111 "Link to this heading")

```
 SELECT id, name, manager_id
FROM
employee
WHERE manager_id = 101

UNION

SELECT id, name, manager_id
FROM
employee
WHERE manager_id = 102

UNION ALL

SELECT id, name, manager_id
FROM
employee
WHERE manager_id = 101

INTERSECT

SELECT id, name, manager_id
FROM
employee
WHERE manager_id = 103

EXCEPT

SELECT id, name, manager_id
FROM
employee
WHERE manager_id = 104;
```

Copy

##### Results[¶](#id112 "Link to this heading")

| ID | NAME | MANAGER\_ID |
| --- | --- | --- |
| 102 | Jorge | 101 |
| 103 | Kwaku | 101 |
| 110 | Liu | 101 |
| 106 | Mateo | 102 |
| 201 | Sofía | 102 |

### Related EWIs[¶](#id113 "Link to this heading")

There are no known issues.

## WHERE clause[¶](#where-clause "Link to this heading")

### Description[¶](#id114 "Link to this heading")

> The `WHERE` clause contains conditions that either join tables or apply predicates to columns in tables. ([Redshift SQL Language Reference WHERE Clause](https://docs.aws.amazon.com/redshift/latest/dg/r_WHERE_clause.html))

Note

The [WHERE clause](https://docs.snowflake.com/en/sql-reference/constructs/where) is fully supported in Snowflake.

### Grammar Syntax[¶](#id115 "Link to this heading")

```
 [ WHERE condition ]
```

Copy

### Sample Source Patterns[¶](#id116 "Link to this heading")

#### Input Code:[¶](#id117 "Link to this heading")

##### Redshift[¶](#id118 "Link to this heading")

```
 CREATE TABLE employee (
  id INT,
  name VARCHAR(20),
  manager_id INT
);
  
INSERT INTO employee(id, name, manager_id) VALUES
(100, 'Carlos', null),
(101, 'John', 100),
(102, 'Jorge', 101),
(103, 'Kwaku', 101),
(110, 'Liu', 101),
(106, 'Mateo', 102),
(110, 'Nikki', 103),
(104, 'Paulo', 103),
(105, 'Richard', 103),
(120, 'Saanvi', 104),
(200, 'Shirley', 104),
(201, 'Sofía', 102),
(205, 'Zhang', 104);

SELECT id, name, manager_id
FROM employee
WHERE name LIKE 'J%';
```

Copy

##### Results[¶](#id119 "Link to this heading")

| ID | NAME | MANAGER\_ID |
| --- | --- | --- |
| 101 | John | 100 |
| 102 | Jorge | 101 |

##### Output Code:[¶](#id120 "Link to this heading")

##### Snowflake[¶](#id121 "Link to this heading")

```
 CREATE TABLE employee (
  id INT,
  name VARCHAR(20),
  manager_id INT
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "11/05/2024",  "domain": "test" }}';

INSERT INTO employee (id, name, manager_id) VALUES
(100, 'Carlos', null),
(101, 'John', 100),
(102, 'Jorge', 101),
(103, 'Kwaku', 101),
(110, 'Liu', 101),
(106, 'Mateo', 102),
(110, 'Nikki', 103),
(104, 'Paulo', 103),
(105, 'Richard', 103),
(120, 'Saanvi', 104),
(200, 'Shirley', 104),
(201, 'Sofía', 102),
(205, 'Zhang', 104);

SELECT id, name, manager_id
FROM
  employee
WHERE name LIKE 'J%' ESCAPE '\\';
```

Copy

##### Results[¶](#id122 "Link to this heading")

| ID | NAME | MANAGER\_ID |
| --- | --- | --- |
| 101 | John | 100 |
| 102 | Jorge | 101 |

### Related EWIs[¶](#id123 "Link to this heading")

There are no known issues.

## WITH clause[¶](#with-clause "Link to this heading")

### Description[¶](#id124 "Link to this heading")

A `WITH` clause is an optional clause that precedes the SELECT list in a query. The `WITH` clause defines one or more *common\_table\_expressions*. Each common table expression (CTE) defines a temporary table, which is similar to a view definition. You can reference these temporary tables in the `FROM` clause. ([Redshift SQL Language Reference WITH Clause](https://docs.aws.amazon.com/redshift/latest/dg/r_WITH_clause.html))

Note

The [WITH clause](https://docs.snowflake.com/en/sql-reference/constructs/with) is fully supported in Snowflake.

### Grammar Syntax[¶](#id125 "Link to this heading")

```
 [ WITH [RECURSIVE] common_table_expression [, common_table_expression , ...] ]

--Where common_table_expression can be either non-recursive or recursive. 
--Following is the non-recursive form:
CTE_table_name [ ( column_name [, ...] ) ] AS ( query )

--Following is the recursive form of common_table_expression:
CTE_table_name (column_name [, ...] ) AS ( recursive_query )
```

Copy

### Sample Source Patterns[¶](#id126 "Link to this heading")

#### Recursive form[¶](#recursive-form "Link to this heading")

##### Input Code:[¶](#id127 "Link to this heading")

##### Redshift[¶](#id128 "Link to this heading")

```
 CREATE TABLE employee (
  id INT,
  name VARCHAR(20),
  manager_id INT
);
  
INSERT INTO employee(id, name, manager_id) VALUES
(100, 'Carlos', null),
(101, 'John', 100),
(102, 'Jorge', 101),
(103, 'Kwaku', 101),
(110, 'Liu', 101),
(106, 'Mateo', 102),
(110, 'Nikki', 103),
(104, 'Paulo', 103),
(105, 'Richard', 103),
(120, 'Saanvi', 104),
(200, 'Shirley', 104),
(201, 'Sofía', 102),
(205, 'Zhang', 104);
  

WITH RECURSIVE john_org(id, name, manager_id, level) AS
( SELECT id, name, manager_id, 1 AS level
  FROM employee
  WHERE name = 'John'
  UNION ALL
  SELECT e.id, e.name, e.manager_id, level + 1 AS next_level
  FROM employee e, john_org j
  WHERE e.manager_id = j.id and level < 4
)
SELECT DISTINCT id, name, manager_id FROM john_org ORDER BY manager_id;
```

Copy

##### Results[¶](#id129 "Link to this heading")

| ID | NAME | MANAGER\_ID |
| --- | --- | --- |
| 101 | John | 100 |
| 110 | Liu | 101 |
| 102 | Jorge | 101 |
| 103 | Kwaku | 101 |
| 201 | Sofía | 102 |
| 106 | Mateo | 102 |
| 105 | Richard | 103 |
| 104 | Paulo | 103 |
| 110 | Nikki | 103 |
| 205 | Zhang | 104 |
| 120 | Saanvi | 104 |
| 200 | Shirley | 104 |

##### Output Code:[¶](#id130 "Link to this heading")

##### Snowflake[¶](#id131 "Link to this heading")

```
 CREATE TABLE employee (
  id INT,
  name VARCHAR(20),
  manager_id INT
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}';

INSERT INTO employee (id, name, manager_id) VALUES
(100, 'Carlos', null),
(101, 'John', 100),
(102, 'Jorge', 101),
(103, 'Kwaku', 101),
(110, 'Liu', 101),
(106, 'Mateo', 102),
(110, 'Nikki', 103),
(104, 'Paulo', 103),
(105, 'Richard', 103),
(120, 'Saanvi', 104),
(200, 'Shirley', 104),
(201, 'Sofía', 102),
(205, 'Zhang', 104);


WITH RECURSIVE john_org(id, name, manager_id, level) AS
( SELECT id, name, manager_id, 1 AS level
  FROM
    employee
  WHERE name = 'John'
  UNION ALL
  SELECT e.id, e.name, e.manager_id, level + 1 AS next_level
  FROM
    employee e,
    john_org j
  WHERE e.manager_id = j.id and level < 4
)
SELECT DISTINCT id, name, manager_id FROM
  john_org
ORDER BY manager_id;
```

Copy

##### Results[¶](#id132 "Link to this heading")

| ID | NAME | MANAGER\_ID |
| --- | --- | --- |
| 101 | John | 100 |
| 102 | Jorge | 101 |
| 103 | Kwaku | 101 |
| 110 | Liu | 101 |
| 106 | Mateo | 102 |
| 201 | Sofía | 102 |
| 110 | Nikki | 103 |
| 104 | Paulo | 103 |
| 105 | Richard | 103 |
| 120 | Saanvi | 104 |
| 200 | Shirley | 104 |
| 205 | Zhang | 104 |

#### Non recursive form[¶](#non-recursive-form "Link to this heading")

##### Input Code:[¶](#id133 "Link to this heading")

##### Redshift[¶](#id134 "Link to this heading")

```
 WITH ManagerHierarchy AS (
    SELECT id AS employee_id, name AS employee_name, manager_id
    FROM employee
)
SELECT e.employee_name AS employee, m.employee_name AS manager
FROM ManagerHierarchy e
LEFT JOIN ManagerHierarchy m ON e.manager_id = m.employee_id;
```

Copy

##### Results[¶](#id135 "Link to this heading")

| EMPLOYEE | MANAGER |
| --- | --- |
| Carlos | null |
| John | Carlos |
| Jorge | John |
| Kwaku | John |
| Liu | John |
| Mateo | Jorge |
| Sofía | Jorge |
| Nikki | Kwaku |
| Paulo | Kwaku |
| Richard | Kwaku |
| Saanvi | Paulo |
| Shirley | Paulo |
| Zhang | Paulo |

##### Output Code:[¶](#id136 "Link to this heading")

##### Snowflake[¶](#id137 "Link to this heading")

```
 WITH ManagerHierarchy AS (
    SELECT id AS employee_id, name AS employee_name, manager_id
    FROM
    employee
)
SELECT e.employee_name AS employee, m.employee_name AS manager
FROM
    ManagerHierarchy e
LEFT JOIN
    ManagerHierarchy m ON e.manager_id = m.employee_id;
```

Copy

##### Results[¶](#id138 "Link to this heading")

| EMPLOYEE | MANAGER |
| --- | --- |
| John | Carlos |
| Jorge | John |
| Kwaku | John |
| Liu | John |
| Mateo | Jorge |
| Sofía | Jorge |
| Nikki | Kwaku |
| Paulo | Kwaku |
| Richard | Kwaku |
| Saanvi | Paulo |
| Shirley | Paulo |
| Zhang | Paulo |
| Carlos | null |

### Related EWIs[¶](#id139 "Link to this heading")

There are no known issues.

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

1. [SELECT](#select)
2. [CONNECT BY clause](#connect-by-clause)
3. [FROM clause](#from-clause)
4. [GROUP BY clause](#group-by-clause)
5. [HAVING clause](#having-clause)
6. [ORDER BY clause](#order-by-clause)
7. [QUALIFY clause](#qualify-clause)
8. [SELECT list](#select-list)
9. [UNION, INTERSECT, and EXCEPT](#union-intersect-and-except)
10. [WHERE clause](#where-clause)
11. [WITH clause](#with-clause)