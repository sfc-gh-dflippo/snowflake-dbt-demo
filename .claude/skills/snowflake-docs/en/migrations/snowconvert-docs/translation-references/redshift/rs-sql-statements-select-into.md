---
auto_generated: true
description: Returns rows from tables, views, and user-defined functions and inserts
  them into a new table. (Redshift SQL Language Reference SELECT statement)
last_scraped: '2026-01-14T16:53:43.357601+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/redshift/rs-sql-statements-select-into
title: SnowConvert AI - Redshift - SELECT INTO | Snowflake Documentation
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)Translation References[Redshift](README.md)[SQL Statements](redshift-sql-statements.md)SELECT INTO

# SnowConvert AI - Redshift - SELECT INTO[¶](#snowconvert-ai-redshift-select-into "Link to this heading")

## Description[¶](#description "Link to this heading")

> Returns rows from tables, views, and user-defined functions and inserts them into a new table. ([Redshift SQL Language Reference SELECT statement](https://docs.aws.amazon.com/redshift/latest/dg/r_SELECT_synopsis.html))

## Grammar Syntax[¶](#grammar-syntax "Link to this heading")

```
 [ WITH with_subquery [, ...] ]
SELECT
[ TOP number ] [ ALL | DISTINCT ]
* | expression [ AS output_name ] [, ...]
INTO [ TEMPORARY | TEMP ] [ TABLE ] new_table
[ FROM table_reference [, ...] ]
[ WHERE condition ]
[ GROUP BY expression [, ...] ]
[ HAVING condition [, ...] ]
[ { UNION | INTERSECT | { EXCEPT | MINUS } } [ ALL ] query ]
[ ORDER BY expression
[ ASC | DESC ]
[ LIMIT { number | ALL } ]
[ OFFSET start ]
```

Copy

For more information please refer to each of the following links:

1. [WITH clause](rs-sql-statements-select.html#with-clause)
2. [SELECT list](rs-sql-statements-select.html#select-list)
3. [FROM clause](rs-sql-statements-select.html#from-clause)
4. [WHERE clause](rs-sql-statements-select.html#where-clause)
5. [CONNECT BY clause](rs-sql-statements-select.html#connect-by-clause)
6. [GROUP BY clause](rs-sql-statements-select.html#group-by-clause)
7. [HAVING clause](rs-sql-statements-select.html#having-clause)
8. [QUALIFY clause](rs-sql-statements-select.html#qualify-clause)
9. [UNION, INTERSECT, and EXCEPT](rs-sql-statements-select.html#union-intersect-and-except)
10. [ORDER BY clause](rs-sql-statements-select.html#order-by-clause)
11. [LIMIT and OFFSET clauses](#limit-and-offset-clauses)
12. [Local Variables and Parameters](#local-variables-and-parameters)

## FROM clause[¶](#from-clause "Link to this heading")

### Description[¶](#id1 "Link to this heading")

> The `FROM` clause in a query lists the table references (tables, views, and subqueries) that data is selected from. If multiple table references are listed, the tables must be joined, using appropriate syntax in either the `FROM` clause or the `WHERE` clause. If no join criteria are specified, the system processes the query as a cross-join. ([Redshift SQL Language Reference FROM Clause](https://docs.aws.amazon.com/redshift/latest/dg/r_FROM_clause30.html))

Warning

The [FROM clause](https://docs.snowflake.com/en/sql-reference/constructs/from) is partially supported in Snowflake. [Object unpivoting](https://docs.aws.amazon.com/redshift/latest/dg/query-super.html#unpivoting) is not currently supported.

### Grammar Syntax[¶](#id2 "Link to this heading")

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
INTO employees_in_department
FROM employee e
INNER JOIN department d ON e.manager_id = d.manager_id;
```

Copy

##### Results[¶](#results "Link to this heading")

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

##### Output Code:[¶](#output-code "Link to this heading")

##### Redshift[¶](#id3 "Link to this heading")

```
 CREATE TABLE employee (
  id INT,
  name VARCHAR(20),
  manager_id INT
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/06/2025",  "domain": "test" }}';

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
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/06/2025",  "domain": "test" }}';

INSERT INTO department (id, name, manager_id) VALUES
(1, 'HR', 100),
(2, 'Sales', 101),
(3, 'Engineering', 102),
(4, 'Marketing', 103);

CREATE TABLE IF NOT EXISTS employees_in_department AS
  SELECT e.name AS employee_name, d.name AS department_name
  FROM
    employee e
  INNER JOIN
      department d ON e.manager_id = d.manager_id;
```

Copy

##### Results[¶](#id4 "Link to this heading")

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

### Known Issues[¶](#known-issues "Link to this heading")

There are no known issues.

### Related EWIs.[¶](#related-ewis "Link to this heading")

See [SELECT](rs-sql-statements-select.html#select) transformation for related EWIs.

## GROUP BY clause[¶](#group-by-clause "Link to this heading")

### Description[¶](#id5 "Link to this heading")

> The `GROUP BY` clause identifies the grouping columns for the query. Grouping columns must be declared when the query computes aggregates with standard functions such as `SUM`, `AVG`, and `COUNT`. ([Redshift SQL Language Reference GROUP BY Clause](https://docs.aws.amazon.com/redshift/latest/dg/r_GROUP_BY_clause.html))

Note

The [GROUP BY clause](https://docs.snowflake.com/en/sql-reference/constructs/group-by) is fully supported in Snowflake.

### Grammar Syntax[¶](#id6 "Link to this heading")

```
 GROUP BY expression [, ...]
```

Copy

### Sample Source Patterns[¶](#id7 "Link to this heading")

#### Input Code:[¶](#id8 "Link to this heading")

##### Redshift[¶](#id9 "Link to this heading")

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
INTO manager_employees
FROM employee
GROUP BY manager_id
ORDER BY manager_id;
```

Copy

##### Results[¶](#id10 "Link to this heading")

| MANAGER\_ID | TOTAL\_EMPLOYEES |
| --- | --- |
| 100 | 1 |
| 101 | 3 |
| 102 | 2 |
| 103 | 3 |
| 104 | 3 |
|  | 1 |

##### Output Code:[¶](#id11 "Link to this heading")

##### Snowflake[¶](#snowflake "Link to this heading")

```
 CREATE TABLE employee (
  id INT,
  name VARCHAR(20),
  manager_id INT
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/06/2025",  "domain": "test" }}';

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

CREATE TABLE IF NOT EXISTS manager_employees AS
  SELECT
      manager_id,
      COUNT(id) AS total_employees
  FROM
      employee
  GROUP BY manager_id
  ORDER BY manager_id;
```

Copy

##### Results[¶](#id12 "Link to this heading")

| MANAGER\_ID | TOTAL\_EMPLOYEES |
| --- | --- |
| 100 | 1 |
| 101 | 3 |
| 102 | 2 |
| 103 | 3 |
| 104 | 3 |
|  | 1 |

### Known Issues[¶](#id13 "Link to this heading")

There are no known issues.

### Related EWIs.[¶](#id14 "Link to this heading")

There are no related EWIs.

## HAVING clause[¶](#having-clause "Link to this heading")

### Description[¶](#id15 "Link to this heading")

> The `HAVING` clause applies a condition to the intermediate grouped result set that a query returns. ([Redshift SQL Language Reference HAVING Clause](https://docs.aws.amazon.com/redshift/latest/dg/r_HAVING_clause.html))

Note

The [HAVING clause](https://docs.snowflake.com/en/sql-reference/constructs/having) is fully supported in Snowflake.

### Grammar Syntax[¶](#id16 "Link to this heading")

```
 [ HAVING condition ]
```

Copy

### Sample Source Patterns[¶](#id17 "Link to this heading")

#### Input Code:[¶](#id18 "Link to this heading")

##### Redshift[¶](#id19 "Link to this heading")

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
INTO manager_employees
FROM
employee
GROUP BY manager_id
HAVING COUNT(id) > 2
ORDER BY manager_id;
```

Copy

##### Results[¶](#id20 "Link to this heading")

| MANAGER\_ID | TOTAL\_EMPLOYEES |
| --- | --- |
| 101 | 3 |
| 103 | 3 |
| 104 | 3 |

##### Output Code:[¶](#id21 "Link to this heading")

##### Snowflake[¶](#id22 "Link to this heading")

```
 CREATE TABLE employee (
  id INT,
  name VARCHAR(20),
  manager_id INT
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/06/2025",  "domain": "test" }}';

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

CREATE TABLE IF NOT EXISTS manager_employees AS
  SELECT manager_id, COUNT(id) AS total_employees
  FROM
    employee
  GROUP BY manager_id
  HAVING COUNT(id) > 2
  ORDER BY manager_id;
```

Copy

##### Results[¶](#id23 "Link to this heading")

| MANAGER\_ID | TOTAL\_EMPLOYEES |
| --- | --- |
| 101 | 3 |
| 103 | 3 |
| 104 | 3 |

### Known Issues[¶](#id24 "Link to this heading")

There are no known issues.

### Related EWIs.[¶](#id25 "Link to this heading")

There are no related EWIs.

## LIMIT and OFFSET clauses[¶](#limit-and-offset-clauses "Link to this heading")

### Description[¶](#id26 "Link to this heading")

> The LIMIT and OFFSET clauses retrieves and skips the number of rows specified in the number.

Note

The [LIMIT and OFFSET](https://docs.snowflake.com/en/sql-reference/constructs/limit) clauses are fully supported in Snowflake.

### Grammar Syntax[¶](#id27 "Link to this heading")

```
 [ LIMIT { number | ALL } ]
[ OFFSET start ]
```

Copy

### Sample Source Patterns[¶](#id28 "Link to this heading")

#### LIMIT number[¶](#limit-number "Link to this heading")

##### Input Code:[¶](#id29 "Link to this heading")

##### Redshift[¶](#id30 "Link to this heading")

```
 SELECT id, name, manager_id, salary
INTO limited_employees
FROM employee
LIMIT 5;
```

Copy

##### Results[¶](#id31 "Link to this heading")

| ID | NAME | MANAGER\_ID | SALARY |
| --- | --- | --- | --- |
| 100 | Carlos |  | 120000.00 |
| 101 | John | 100 | 90000.00 |
| 102 | Jorge | 101 | 95000.00 |
| 103 | Kwaku | 101 | 105000.00 |
| 104 | Paulo | 102 | 110000.00 |

##### Output Code:[¶](#id32 "Link to this heading")

##### Snowflake[¶](#id33 "Link to this heading")

```
 CREATE TABLE IF NOT EXISTS limited_employees AS
SELECT id, name, manager_id, salary
FROM
employee
LIMIT 5;
```

Copy

##### Results[¶](#id34 "Link to this heading")

| ID | NAME | MANAGER\_ID | SALARY |
| --- | --- | --- | --- |
| 100 | Carlos |  | 120000.00 |
| 101 | John | 100 | 90000.00 |
| 102 | Jorge | 101 | 95000.00 |
| 103 | Kwaku | 101 | 105000.00 |
| 104 | Paulo | 102 | 110000.00 |

#### LIMIT ALL[¶](#limit-all "Link to this heading")

##### Input Code:[¶](#id35 "Link to this heading")

##### Redshift[¶](#id36 "Link to this heading")

```
 SELECT id, name, manager_id, salary
INTO limited_employees
FROM employee
LIMIT ALL;
```

Copy

##### Results[¶](#id37 "Link to this heading")

| ID | NAME | MANAGER\_ID | SALARY |
| --- | --- | --- | --- |
| 100 | Carlos |  | 120000.00 |
| 101 | John | 100 | 90000.00 |
| 102 | Jorge | 101 | 95000.00 |
| 103 | Kwaku | 101 | 105000.00 |
| 104 | Paulo | 102 | 110000.00 |
| 105 | Richard | 102 | 85000.00 |
| 106 | Mateo | 103 | 95000.00 |
| 107 | Liu | 103 | 108000.00 |
| 108 | Zhang | 104 | 95000.00 |

##### Output Code:[¶](#id38 "Link to this heading")

##### Snowflake[¶](#id39 "Link to this heading")

```
 CREATE TABLE IF NOT EXISTS limited_employees AS
SELECT id, name, manager_id, salary
FROM
employee
LIMIT NULL;
```

Copy

##### Results[¶](#id40 "Link to this heading")

| ID | NAME | MANAGER\_ID | SALARY |
| --- | --- | --- | --- |
| 100 | Carlos |  | 120000.00 |
| 101 | John | 100 | 90000.00 |
| 102 | Jorge | 101 | 95000.00 |
| 103 | Kwaku | 101 | 105000.00 |
| 104 | Paulo | 102 | 110000.00 |
| 105 | Richard | 102 | 85000.00 |
| 106 | Mateo | 103 | 95000.00 |
| 107 | Liu | 103 | 108000.00 |
| 108 | Zhang | 104 | 95000.00 |

#### OFFSET without LIMIT[¶](#offset-without-limit "Link to this heading")

Snowflake doesn’t support OFFSET without LIMIT. The LIMIT is added after transformation with NULL, which is the default LIMIT.

##### Input Code:[¶](#id41 "Link to this heading")

##### Redshift[¶](#id42 "Link to this heading")

```
 SELECT id, name, manager_id, salary
INTO limited_employees
FROM employee
OFFSET 5;
```

Copy

##### Results[¶](#id43 "Link to this heading")

| ID | NAME | MANAGER\_ID | SALARY |
| --- | --- | --- | --- |
| 105 | Richard | 102 | 85000.00 |
| 106 | Mateo | 103 | 95000.00 |
| 107 | Liu | 103 | 108000.00 |
| 108 | Zhang | 104 | 95000.00 |

##### Output Code:[¶](#id44 "Link to this heading")

##### Snowflake[¶](#id45 "Link to this heading")

```
 CREATE TABLE IF NOT EXISTS limited_employees AS
SELECT id, name, manager_id, salary
FROM
employee
LIMIT NULL
OFFSET 5;
```

Copy

##### Results[¶](#id46 "Link to this heading")

| ID | NAME | MANAGER\_ID | SALARY |
| --- | --- | --- | --- |
| 105 | Richard | 102 | 85000.00 |
| 106 | Mateo | 103 | 95000.00 |
| 107 | Liu | 103 | 108000.00 |
| 108 | Zhang | 104 | 95000.00 |

### Known Issues[¶](#id47 "Link to this heading")

There are no known issues.

### Related EWIs.[¶](#id48 "Link to this heading")

There are no related EWIs.

## Local Variables and Parameters[¶](#local-variables-and-parameters "Link to this heading")

### Description[¶](#id49 "Link to this heading")

> Redshift also allow to SELECT INTO variables when the statement is executed inside stored procedures.

Note

This pattern is fully supported in Snowflake.

### Grammar Syntax[¶](#id50 "Link to this heading")

```
 SELECT [ select_expressions ] INTO target [ select_expressions ] FROM ...;
```

Copy

### Sample Source Patterns[¶](#id51 "Link to this heading")

#### SELECT INTO with expressions at the left[¶](#select-into-with-expressions-at-the-left "Link to this heading")

##### Input Code:[¶](#id52 "Link to this heading")

##### Redshift[¶](#id53 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE test_sp1(out param1 int)
AS $$
DECLARE
    var1 int;
BEGIN
     select 10, 100 into param1, var1;
END;
$$ LANGUAGE plpgsql;
```

Copy

##### Results[¶](#id54 "Link to this heading")

| param1 |
| --- |
| 10 |

##### Output Code:[¶](#id55 "Link to this heading")

##### Snowflake[¶](#id56 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE test_sp1 (param1 OUT int)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
AS $$
        DECLARE
            var1 int;
BEGIN
     select 10, 100 into
                : param1,
                : var1;
END;
$$;
```

Copy

##### Results[¶](#id57 "Link to this heading")

| TEST\_SP1 |
| --- |
| { “param1”: 10 } |

#### SELECT INTO with expressions at the right[¶](#select-into-with-expressions-at-the-right "Link to this heading")

##### Input Code:[¶](#id58 "Link to this heading")

##### Redshift[¶](#id59 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE test_sp1(out param1 int)
AS $$
DECLARE
    var1 int;
BEGIN
     select into param1, var1 10, 100;
END;
$$ LANGUAGE plpgsql;
```

Copy

##### Results[¶](#id60 "Link to this heading")

| param1 |
| --- |
| 10 |

##### Output Code:[¶](#id61 "Link to this heading")

Since Snowflake doesn’t support this grammar for SELECT INTO, the expressions are moved to the left of the INTO.

##### Snowflake[¶](#id62 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE test_sp1 (param1 OUT int)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
AS $$
        DECLARE
            var1 int;
BEGIN
     select
                10, 100
            into
                : param1,
                : var1;
END;
$$;
```

Copy

##### Results[¶](#id63 "Link to this heading")

| TEST\_SP1 |
| --- |
| { “param1”: 10 } |

### Known Issues[¶](#id64 "Link to this heading")

There are no known issues.

### Related EWIs.[¶](#id65 "Link to this heading")

There are no related EWIs.

## ORDER BY clause[¶](#order-by-clause "Link to this heading")

### Description[¶](#id66 "Link to this heading")

> The `ORDER BY` clause sorts the result set of a query. ([Redshift SQL Language Reference Order By Clause](https://docs.aws.amazon.com/redshift/latest/dg/r_ORDER_BY_clause.html))

Note

The [ORDER BY clause](https://docs.snowflake.com/en/sql-reference/constructs/order-by) is fully supported in Snowflake.

### Grammar Syntax[¶](#id67 "Link to this heading")

```
 [ ORDER BY expression [ ASC | DESC ] ]
[ NULLS FIRST | NULLS LAST ]
[ LIMIT { count | ALL } ]
[ OFFSET start ]
```

Copy

### Sample Source Patterns[¶](#id68 "Link to this heading")

#### Input Code:[¶](#id69 "Link to this heading")

##### Redshift[¶](#id70 "Link to this heading")

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
INTO salaries
FROM employee
ORDER BY salary DESC NULLS LAST, name ASC NULLS FIRST
LIMIT 5                                        
OFFSET 2;
```

Copy

##### Results[¶](#id71 "Link to this heading")

| ID | NAME | MANAGER\_ID | SALARY |
| --- | --- | --- | --- |
| 107 | Liu | 103 | 108000.00 |
| 103 | Kwaku | 101 | 105000.00 |
| 102 | Jorge | 101 | 95000.00 |
| 106 | Mateo | 103 | 95000.00 |
| 108 | Zhang | 104 | 95000.00 |

##### Output Code:[¶](#id72 "Link to this heading")

##### Snowflake[¶](#id73 "Link to this heading")

```
 CREATE TABLE employee (
    id INT,
    name VARCHAR(20),
    manager_id INT,
    salary DECIMAL(10, 2)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/06/2025",  "domain": "test" }}';

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

CREATE TABLE IF NOT EXISTS salaries AS
    SELECT id, name, manager_id, salary
    FROM
        employee
    ORDER BY salary DESC NULLS LAST, name ASC NULLS FIRST
    LIMIT 5
    OFFSET 2;
```

Copy

##### Results[¶](#id74 "Link to this heading")

| ID | NAME | MANAGER\_ID | SALARY |
| --- | --- | --- | --- |
| 107 | Liu | 103 | 108000.00 |
| 103 | Kwaku | 101 | 105000.00 |
| 102 | Jorge | 101 | 95000.00 |
| 106 | Mateo | 103 | 95000.00 |
| 108 | Zhang | 104 | 95000.00 |

### Known Issues[¶](#id75 "Link to this heading")

There are no known issues.

### Related EWIs.[¶](#id76 "Link to this heading")

There are no related EWIs.

## SELECT list[¶](#select-list "Link to this heading")

### Description[¶](#id77 "Link to this heading")

> The SELECT list names the columns, functions, and expressions that you want the query to return. The list represents the output of the query. ([Redshift SQL Language Reference SELECT list](https://docs.aws.amazon.com/redshift/latest/dg/r_SELECT_list.html))

Note

The [query start options](https://docs.snowflake.com/en/sql-reference/sql/select) are fully supported in Snowflake. Just keep in mind that in Snowflake the `DISTINCT` and `ALL` options must go at the beginning of the query.

Note

In Redshift, if your application allows foreign keys or invalid primary keys, it can cause queries to return incorrect results. For example, a SELECT DISTINCT query could return duplicate rows if the primary key column does not contain all unique values. ([Redshift SQL Language Reference SELECT list](https://docs.aws.amazon.com/redshift/latest/dg/r_SELECT_list.html))

### Grammar Syntax[¶](#id78 "Link to this heading")

```
 SELECT
[ TOP number ]
[ ALL | DISTINCT ] * | expression [ AS column_alias ] [, ...]
```

Copy

### Sample Source Patterns[¶](#id79 "Link to this heading")

#### Top clause[¶](#top-clause "Link to this heading")

##### Input Code:[¶](#id80 "Link to this heading")

##### Redshift[¶](#id81 "Link to this heading")

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
INTO top_employees
FROM employee;

SELECT * FROM top_employees;
```

Copy

##### Results[¶](#id82 "Link to this heading")

| ID | NAME | MANAGER\_ID |
| --- | --- | --- |
| 100 | Carlos | null |
| 101 | John | 100 |
| 102 | Jorge | 101 |
| 103 | Kwaku | 101 |
| 110 | Liu | 101 |

##### Output Code:[¶](#id83 "Link to this heading")

##### Snowflake[¶](#id84 "Link to this heading")

```
 CREATE TABLE employee
(
  id INT,
  name VARCHAR(20),
  manager_id INT
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/06/2025",  "domain": "test" }}';

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

CREATE TABLE IF NOT EXISTS top_employees AS
SELECT TOP 5 id, name, manager_id
  FROM
    employee;

SELECT * FROM
  top_employees;
```

Copy

##### Results[¶](#id85 "Link to this heading")

| ID | NAME | MANAGER\_ID |
| --- | --- | --- |
| 100 | Carlos | null |
| 101 | John | 100 |
| 102 | Jorge | 101 |
| 103 | Kwaku | 101 |
| 110 | Liu | 101 |

#### ALL[¶](#all "Link to this heading")

##### Input Code:[¶](#id86 "Link to this heading")

##### Redshift[¶](#id87 "Link to this heading")

```
SELECT ALL manager_id
INTO manager
FROM employee;
```

Copy

##### Results[¶](#id88 "Link to this heading")

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

##### Output Code:[¶](#id89 "Link to this heading")

##### Snowflake[¶](#id90 "Link to this heading")

```
 CREATE TABLE IF NOT EXISTS manager AS
SELECT ALL manager_id
FROM
employee;
```

Copy

##### Results[¶](#id91 "Link to this heading")

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

##### Input Code:[¶](#id92 "Link to this heading")

##### Redshift[¶](#id93 "Link to this heading")

```
SELECT DISTINCT manager_id
INTO manager
FROM employee;
```

Copy

##### Results[¶](#id94 "Link to this heading")

| MANAGER\_ID |
| --- |
| null |
| 100 |
| 101 |
| 102 |
| 103 |
| 104 |

##### Output Code:[¶](#id95 "Link to this heading")

##### Snowflake[¶](#id96 "Link to this heading")

```
 CREATE TABLE IF NOT EXISTS manager AS
SELECT DISTINCT manager_id
FROM
employee;
```

Copy

##### Results[¶](#id97 "Link to this heading")

| MANAGER\_ID |
| --- |
| null |
| 100 |
| 101 |
| 102 |
| 103 |
| 104 |

### Known Issues[¶](#id98 "Link to this heading")

There are no known issues.

### Related EWIs.[¶](#id99 "Link to this heading")

There are no related EWIs.

## UNION, INTERSECT, and EXCEPT[¶](#union-intersect-and-except "Link to this heading")

### Description[¶](#id100 "Link to this heading")

> The `UNION`, `INTERSECT`, and `EXCEPT` *set operators* are used to compare and merge the results of two separate query expressions. ([Redshift SQL Language Reference Set Operators](https://docs.aws.amazon.com/redshift/latest/dg/r_UNION.html))

Note

[Set operators](https://docs.snowflake.com/en/sql-reference/operators-query) are fully supported in Snowflake.

### Grammar Syntax[¶](#id101 "Link to this heading")

```
 query
{ UNION [ ALL ] | INTERSECT | EXCEPT | MINUS }
query
```

Copy

### Sample Source Patterns[¶](#id102 "Link to this heading")

#### Input Code:[¶](#id103 "Link to this heading")

##### Redshift[¶](#id104 "Link to this heading")

```
 SELECT id, name, manager_id
INTO some_employees
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

##### Results[¶](#id105 "Link to this heading")

| ID | NAME | MANAGER\_ID |
| --- | --- | --- |
| 103 | Kwaku | 101 |
| 110 | Liu | 101 |
| 102 | Jorge | 101 |
| 106 | Mateo | 102 |
| 201 | Sofía | 102 |

##### Output Code:[¶](#id106 "Link to this heading")

##### Snowflake[¶](#id107 "Link to this heading")

```
 CREATE TABLE IF NOT EXISTS some_employees AS
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

##### Results[¶](#id108 "Link to this heading")

| ID | NAME | MANAGER\_ID |
| --- | --- | --- |
| 102 | Jorge | 101 |
| 103 | Kwaku | 101 |
| 110 | Liu | 101 |
| 106 | Mateo | 102 |
| 201 | Sofía | 102 |

### Known Issues[¶](#id109 "Link to this heading")

There are no known issues.

### Related EWIs.[¶](#id110 "Link to this heading")

There are no related EWIs.

## WHERE clause[¶](#where-clause "Link to this heading")

### Description[¶](#id111 "Link to this heading")

> The `WHERE` clause contains conditions that either join tables or apply predicates to columns in tables. ([Redshift SQL Language Reference WHERE Clause](https://docs.aws.amazon.com/redshift/latest/dg/r_WHERE_clause.html))

Note

The [WHERE clause](https://docs.snowflake.com/en/sql-reference/constructs/where) is fully supported in Snowflake.

### Grammar Syntax[¶](#id112 "Link to this heading")

```
 [ WHERE condition ]
```

Copy

### Sample Source Patterns[¶](#id113 "Link to this heading")

#### Input Code:[¶](#id114 "Link to this heading")

##### Redshift[¶](#id115 "Link to this heading")

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
INTO employee_names
FROM employee
WHERE name LIKE 'J%';
```

Copy

##### Results[¶](#id116 "Link to this heading")

| ID | NAME | MANAGER\_ID |
| --- | --- | --- |
| 101 | John | 100 |
| 102 | Jorge | 101 |

##### Output Code:[¶](#id117 "Link to this heading")

##### Snowflake[¶](#id118 "Link to this heading")

```
 CREATE TABLE employee (
  id INT,
  name VARCHAR(20),
  manager_id INT
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/06/2025",  "domain": "test" }}';

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

CREATE TABLE IF NOT EXISTS employee_names AS
  SELECT id, name, manager_id
  FROM
    employee
  WHERE name LIKE 'J%' ESCAPE '\\';
```

Copy

##### Results[¶](#id119 "Link to this heading")

| ID | NAME | MANAGER\_ID |
| --- | --- | --- |
| 101 | John | 100 |
| 102 | Jorge | 101 |

### Known Issues[¶](#id120 "Link to this heading")

There are no known issues.

### Related EWIs.[¶](#id121 "Link to this heading")

There are no related EWIs.

## WITH clause[¶](#with-clause "Link to this heading")

### Description[¶](#id122 "Link to this heading")

> A `WITH` clause is an optional clause that precedes the SELECT INTO in a query. The `WITH` clause defines one or more *common\_table\_expressions*. Each common table expression (CTE) defines a temporary table, which is similar to a view definition. You can reference these temporary tables in the `FROM` clause. ([Redshift SQL Language Reference WITH Clause](https://docs.aws.amazon.com/redshift/latest/dg/r_WITH_clause.html))

Note

The [WITH clause](https://docs.snowflake.com/en/sql-reference/constructs/with) is fully supported in Snowflake.

### Grammar Syntax[¶](#id123 "Link to this heading")

```
 [ WITH [RECURSIVE] common_table_expression [, common_table_expression , ...] ]

--Where common_table_expression can be either non-recursive or recursive. 
--Following is the non-recursive form:
CTE_table_name [ ( column_name [, ...] ) ] AS ( query )

--Following is the recursive form of common_table_expression:
CTE_table_name (column_name [, ...] ) AS ( recursive_query )
```

Copy

### Sample Source Patterns[¶](#id124 "Link to this heading")

#### Non-Recursive form[¶](#non-recursive-form "Link to this heading")

##### Input Code:[¶](#id125 "Link to this heading")

##### Redshift[¶](#id126 "Link to this heading")

```
 CREATE TABLE orders (
    order_id INT,
    customer_id INT,
    order_date DATE,
    total_amount DECIMAL(10,2)
);


INSERT INTO orders (order_id, customer_id, order_date, total_amount)
VALUES
(1, 101, '2024-02-01', 250.00),
(2, 102, '2024-02-02', 600.00),
(3, 103, '2024-02-03', 150.00),
(4, 104, '2024-02-04', 750.00),
(5, 105, '2024-02-05', 900.00);


WITH HighValueOrders AS (
    SELECT
        order_id,
        customer_id,
        order_date,
        total_amount
    FROM orders
    WHERE total_amount > 500
)
SELECT * INTO high_value_orders FROM HighValueOrders;

SELECT * FROM high_value_orders;
```

Copy

##### Results[¶](#id127 "Link to this heading")

| ORDER\_ID | CUSTOMER\_ID | ORDER\_DATE | TOTAL\_AMOUNT |
| --- | --- | --- | --- |
| 2 | 102 | 2024-02-02 | 600.00 |
| 4 | 104 | 2024-02-04 | 750.00 |
| 5 | 105 | 2024-02-05 | 900.00 |

##### Output Code:[¶](#id128 "Link to this heading")

##### Snowflake[¶](#id129 "Link to this heading")

```
 CREATE TABLE orders (
    order_id INT,
    customer_id INT,
    order_date DATE,
    total_amount DECIMAL(10,2)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}';


INSERT INTO orders (order_id, customer_id, order_date, total_amount)
VALUES
(1, 101, '2024-02-01', 250.00),
(2, 102, '2024-02-02', 600.00),
(3, 103, '2024-02-03', 150.00),
(4, 104, '2024-02-04', 750.00),
(5, 105, '2024-02-05', 900.00);

CREATE TABLE IF NOT EXISTS high_value_orders AS
WITH HighValueOrders AS (
    SELECT
        order_id,
        customer_id,
        order_date,
        total_amount
    FROM
        orders
    WHERE total_amount > 500
    )
    SELECT *
    FROM
    HighValueOrders;
    
SELECT * FROM
    high_value_orders;
```

Copy

##### Results[¶](#id130 "Link to this heading")

| ORDER\_ID | CUSTOMER\_ID | ORDER\_DATE | TOTAL\_AMOUNT |
| --- | --- | --- | --- |
| 2 | 102 | 2024-02-02 | 600.00 |
| 4 | 104 | 2024-02-04 | 750.00 |
| 5 | 105 | 2024-02-05 | 900.00 |

#### Recursive form[¶](#recursive-form "Link to this heading")

##### Input Code:[¶](#id131 "Link to this heading")

##### Redshift[¶](#id132 "Link to this heading")

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


WITH RECURSIVE john_org(id, name, manager_id, level) 
AS
( 
   SELECT id, name, manager_id, 1 AS level
   FROM employee
   WHERE name = 'John'
   UNION ALL
   SELECT e.id, e.name, e.manager_id, level + 1 AS next_level
   FROM employee e, john_org j
   WHERE e.manager_id = j.id and level < 4
)
SELECT DISTINCT id, name, manager_id into new_org FROM john_org ORDER BY manager_id;

SELECT * FROM new_org;
```

Copy

##### Results[¶](#id133 "Link to this heading")

| ID | NAME | MANAGER\_ID |
| --- | --- | --- |
| 101 | John | 100 |
| 103 | Kwaku | 101 |
| 102 | Jorge | 101 |
| 110 | Liu | 101 |
| 106 | Mateo | 102 |
| 201 | Sofía | 102 |
| 105 | Richard | 103 |
| 110 | Nikki | 103 |
| 104 | Paulo | 103 |
| 120 | Saanvi | 104 |
| 200 | Shirley | 104 |
| 205 | Zhang | 104 |

##### Output Code:[¶](#id134 "Link to this heading")

##### Snowflake[¶](#id135 "Link to this heading")

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
CREATE TABLE IF NOT EXISTS new_org AS
WITH RECURSIVE john_org(id, name, manager_id, level)
AS
(
   SELECT id, name, manager_id, 1 AS level
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
   SELECT DISTINCT id, name, manager_id
   FROM
   john_org
   ORDER BY manager_id;
SELECT * FROM
   new_org;
```

Copy

##### Results[¶](#id136 "Link to this heading")

| ID | NAME | MANAGER\_ID |
| --- | --- | --- |
| 101 | John | 100 |
| 103 | Kwaku | 101 |
| 102 | Jorge | 101 |
| 110 | Liu | 101 |
| 106 | Mateo | 102 |
| 201 | Sofía | 102 |
| 105 | Richard | 103 |
| 110 | Nikki | 103 |
| 104 | Paulo | 103 |
| 120 | Saanvi | 104 |
| 200 | Shirley | 104 |
| 205 | Zhang | 104 |

### Known Issues[¶](#id137 "Link to this heading")

There are no known issues.

### Related EWIs.[¶](#id138 "Link to this heading")

There are no related EWIs.

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

1. [Description](#description)
2. [Grammar Syntax](#grammar-syntax)
3. [FROM clause](#from-clause)
4. [GROUP BY clause](#group-by-clause)
5. [HAVING clause](#having-clause)
6. [LIMIT and OFFSET clauses](#limit-and-offset-clauses)
7. [Local Variables and Parameters](#local-variables-and-parameters)
8. [ORDER BY clause](#order-by-clause)
9. [SELECT list](#select-list)
10. [UNION, INTERSECT, and EXCEPT](#union-intersect-and-except)
11. [WHERE clause](#where-clause)
12. [WITH clause](#with-clause)