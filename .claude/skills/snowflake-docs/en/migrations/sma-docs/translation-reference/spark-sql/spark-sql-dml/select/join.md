---
auto_generated: true
description: Merges rows from two table references using specified join conditions.
  For more details, see the Databricks SQL Language Reference JOIN.
last_scraped: '2026-01-14T16:51:55.253374+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/sma-docs/translation-reference/spark-sql/spark-sql-dml/select/join
title: 'Snowpark Migration Accelerator:  Join | Snowflake Documentation'
---

1. [Overview](../../../../../../guides/README.md)
2. [Snowflake Horizon Catalog](../../../../../../user-guide/snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../../../../../../guides/overview-connecting.md)
6. [Virtual warehouses](../../../../../../user-guide/warehouses.md)
7. [Databases, Tables, & Views](../../../../../../guides/overview-db.md)
8. [Data types](../../../../../../data-types.md)
10. Data Integration

    - [Snowflake Openflow](../../../../../../user-guide/data-integration/openflow/about.md)
    - Apache Iceberg™

      - [Apache Iceberg™ Tables](../../../../../../user-guide/tables-iceberg.md)
      - [Snowflake Open Catalog](../../../../../../user-guide/opencatalog/overview.md)
11. Data engineering

    - [Data loading](../../../../../../guides/overview-loading-data.md)
    - [Dynamic Tables](../../../../../../user-guide/dynamic-tables-about.md)
    - [Streams and Tasks](../../../../../../user-guide/data-pipelines-intro.md)
    - [dbt Projects on Snowflake](../../../../../../user-guide/data-engineering/dbt-projects-on-snowflake.md)
    - [Data Unloading](../../../../../../guides/overview-unloading-data.md)
12. [Storage Lifecycle Policies](../../../../../../user-guide/storage-management/storage-lifecycle-policies.md)
13. [Migrations](../../../../../README.md)

    * Tools

      * [SnowConvert AI](../../../../../snowconvert-docs/overview.md)
      * [Snowpark Migration Accelerator](../../../../README.md)

        + General

          + [Introduction](../../../../general/introduction.md)
          + [Getting started](../../../../general/getting-started/README.md)
          + [Conversion software terms of use](../../../../general/conversion-software-terms-of-use/README.md)
          + [Release notes](../../../../general/release-notes/README.md)
          + [Roadmap](../../../../general/roadmap.md)
        + User guide

          + [Overview](../../../../user-guide/overview.md)
          + [Before using the SMA](../../../../user-guide/before-using-the-sma/README.md)
          + [Project overview](../../../../user-guide/project-overview/README.md)
          + [Technical discovery](../../../../user-guide/project-overview/optional-technical-discovery.md)
          + [AI assistant](../../../../user-guide/chatbot.md)
          + [Assessment](../../../../user-guide/assessment/README.md)
          + [Conversion](../../../../user-guide/conversion/README.md)
          + [Using the SMA CLI](../../../../user-guide/using-the-sma-cli/README.md)
        + Use cases

          + Snowflake VS Code extension

            + [SMA checkpoints walkthrough](../../../../use-cases/sma-checkpoints-walkthrough/README.md)
            + [SMA EWI Assistant walkthrough](../../../../use-cases/sma-ewi-assistant-walkthrough/README.md)
          + [Assessment walkthrough](../../../../use-cases/assessment-walkthrough/README.md)
          + [Conversion walkthrough](../../../../use-cases/conversion-walkthrough.md)
          + [Migration lab](../../../../use-cases/migration-lab/README.md)
          + [Sample project](../../../../use-cases/sample-project.md)
          + [Using SMA in an Ubuntu Docker image](../../../../use-cases/using-snowconvert-in-a-ubuntu-docker-image.md)
          + [SMA CLI walkthrough](../../../../use-cases/sma-cli-walkthrough.md)
          + [Snowpark Connect](../../../../use-cases/snowpark-connect/README.md)
        + Issue analysis

          + [Approach](../../../../issue-analysis/approach.md)
          + [Issue code categorization](../../../../issue-analysis/issue-code-categorization.md)
          + [Issue codes by source](../../../../issue-analysis/issue-codes-by-source/README.md)
          + [Troubleshooting the output code](../../../../issue-analysis/troubleshooting-the-output-code/README.md)
          + [Workarounds](../../../../issue-analysis/workarounds.md)
          + [Deploying the output code](../../../../issue-analysis/deploying-the-output-code.md)
        + Translation reference

          + [Translation reference overview](../../../translation-reference-overview.md)
          + [SIT tagging](../../../sit-tagging/README.md)
          + [SQL embedded code](../../../sql-embedded-code.md)
          + [HiveSQL](../../../hivesql/README.md)
          + [Spark SQL](../../README.md)

            - [Spark SQL DDL](../../spark-sql-ddl/README.md)
            - [Spark SQL DML](../README.md)

              * [MERGE](../merge.md)
              * [SELECT](README.md)

                + [DISTINCT](distinct.md)
                + [VALUES](values.md)
                + [JOIN](join.md)
                + [WHERE](where.md)
                + [GROUP BY](group-by.md)
                + [UNION](union.md)
            - [Spark SQL data types](../../spark-sql-data-types.md)
            - [Supported functions](../../supported-functions.md)
        + Workspace estimator

          + [Overview](../../../../workspace-estimator/overview.md)
          + [Getting started](../../../../workspace-estimator/getting-started.md)
        + Interactive assessment application

          + [Overview](../../../../interactive-assessment-application/overview.md)
          + [Installation guide](../../../../interactive-assessment-application/installation-guide.md)
        + Support

          + [General troubleshooting](../../../../support/general-troubleshooting/README.md)
          + [Frequently asked questions](../../../../support/frequently-asked-questions-faq/README.md)
          + [Glossary](../../../../support/glossary.md)
          + [Contact us](../../../../support/contact-us.md)
    * Guides

      * [Teradata](../../../../../guides/teradata.md)
      * [Databricks](../../../../../guides/databricks.md)
      * [SQL Server](../../../../../guides/sqlserver.md)
      * [Amazon Redshift](../../../../../guides/redshift.md)
      * [Oracle](../../../../../guides/oracle.md)
      * [Azure Synapse](../../../../../guides/azuresynapse.md)
15. [Queries](../../../../../../guides/overview-queries.md)
16. [Listings](../../../../../../collaboration/collaboration-listings-about.md)
17. [Collaboration](../../../../../../guides/overview-sharing.md)
19. [Snowflake AI & ML](../../../../../../guides/overview-ai-features.md)
21. [Snowflake Postgres](../../../../../../user-guide/snowflake-postgres/about.md)
23. [Alerts & Notifications](../../../../../../guides/overview-alerts.md)
25. [Security](../../../../../../guides/overview-secure.md)
26. [Data Governance](../../../../../../guides/overview-govern.md)
27. [Privacy](../../../../../../guides/overview-privacy.md)
29. [Organizations & Accounts](../../../../../../guides/overview-manage.md)
30. [Business continuity & data recovery](../../../../../../user-guide/replication-intro.md)
32. [Performance optimization](../../../../../../guides/overview-performance.md)
33. [Cost & Billing](../../../../../../guides/overview-cost.md)

[Guides](../../../../../../guides/README.md)[Migrations](../../../../../README.md)Tools[Snowpark Migration Accelerator](../../../../README.md)Translation reference[Spark SQL](../../README.md)[Spark SQL DML](../README.md)[SELECT](README.md)JOIN

# Snowpark Migration Accelerator: Join[¶](#snowpark-migration-accelerator-join "Link to this heading")

## Description[¶](#description "Link to this heading")

Merges rows from two [table references](https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-qry-select-table-reference.html) using specified join conditions. For more details, see the [Databricks SQL Language Reference JOIN](https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-qry-select-join.html).

A `JOIN` combines data from two sources (such as tables or views) into a single result set. Each row in the result contains columns from both sources based on a specified condition. For a detailed explanation of joins, see [Working with Joins](https://docs.snowflake.com/en/user-guide/querying-joins). ([Snowflake SQL Language Reference JOIN](https://docs.snowflake.com/en/sql-reference/constructs/join))

### Syntax[¶](#syntax "Link to this heading")

```
left_table_reference { [ join_type ] JOIN right_table_reference join_criteria |
           NATURAL join_type JOIN right_table_reference |
           CROSS JOIN right_table_reference }

join_type
  { [ INNER ] |
    LEFT [ OUTER ] |
    [ LEFT ] SEMI |
    RIGHT [ OUTER ] |
    FULL [ OUTER ] |
    [ LEFT ] ANTI |
    CROSS }

join_criteria
  { ON boolean_expression |
    USING ( column_name [, ...] ) }
```

Copy

```
SELECT ...
FROM <object_ref1> [
                     {
                       INNER
                       | { LEFT | RIGHT | FULL } [ OUTER ]
                     }
                   ]
                   JOIN <object_ref2>
  [ ON <condition> ]
[ ... ]

SELECT *
FROM <object_ref1> [
                     {
                       INNER
                       | { LEFT | RIGHT | FULL } [ OUTER ]
                     }
                   ]
                   JOIN <object_ref2>
  [ USING( <column_list> ) ]
[ ... ]

SELECT ...
FROM <object_ref1> [
                     {
                       | NATURAL [ { LEFT | RIGHT | FULL } [ OUTER ] ]
                       | CROSS
                     }
                   ]
                   JOIN <object_ref2>
[ ... ]
```

Copy

## Sample Source Patterns[¶](#sample-source-patterns "Link to this heading")

### Setup data[¶](#setup-data "Link to this heading")

#### Databricks[¶](#databricks "Link to this heading")

```
-- Use employee and department tables to demonstrate different type of joins.
CREATE TEMP VIEW employee(id, name, deptno) AS
     VALUES(105, 'Chloe', 5),
           (103, 'Paul', 3),
           (101, 'John', 1),
           (102, 'Lisa', 2),
           (104, 'Evan', 4),
           (106, 'Amy', 6);

CREATE TEMP VIEW department(deptno, deptname) AS
    VALUES(3, 'Engineering'),
          (2, 'Sales'      ),
          (1, 'Marketing'  );
```

Copy

#### Snowflake[¶](#snowflake "Link to this heading")

```
-- Use employee and department tables to demonstrate different type of joins.
CREATE TEMPORARY TABLE employee(id, name, deptno) AS
SELECT id, name, deptno
  FROM (VALUES (105, 'Chloe', 5),
           (103, 'Paul' , 3),
           (101, 'John' , 1),
           (102, 'Lisa' , 2),
           (104, 'Evan' , 4),
           (106, 'Amy'  , 6)) AS v1 (id, name, deptno);

CREATE TEMP VIEW department(deptno, deptname) AS
SELECT deptno, deptname
  FROM (VALUES(3, 'Engineering'),
          (2, 'Sales'      ),
          (1, 'Marketing'  )) AS v1 (deptno, deptname);
```

Copy

### Pattern code[¶](#pattern-code "Link to this heading")

#### Databricks[¶](#id1 "Link to this heading")

```
-- 1. Use employee and department tables to demonstrate inner join.
SELECT id, name, employee.deptno, deptname
   FROM employee
   INNER JOIN department ON employee.deptno = department.deptno;
 
-- 2. We will use the employee and department tables to show how a left join works. This example will help you understand how to combine data from two tables while keeping all records from the left (first) table.
SELECT id, name, employee.deptno, deptname
   FROM employee
   LEFT JOIN department ON employee.deptno = department.deptno;

-- 3. Demonstrate a RIGHT JOIN using employee and department tables. This query retrieves all departments and matching employees.
SELECT id, name, employee.deptno, deptname
    FROM employee
    RIGHT JOIN department ON employee.deptno = department.deptno;

-- 4. Demonstrate a FULL JOIN operation using the employee and department tables.
SELECT id, name, employee.deptno, deptname
    FROM employee
    FULL JOIN department ON employee.deptno = department.deptno;

-- 5. Demonstrate a cross join operation using the employee and department tables. This query returns all possible combinations of employees and departments.
SELECT id, name, employee.deptno, deptname
    FROM employee
    CROSS JOIN department;

-- 6. This example shows how to use a semi join between employee and department tables. A semi join returns records from the first table (employee) where there is a matching record in the second table (department).
```{code} sql
SELECT *
    FROM employee
    SEMI JOIN department ON employee.deptno = department.deptno;
```

Copy

1. We will use two sample tables - “employee” and “department” - to show how an inner join works. An inner join combines rows from both tables where there is a match between specified columns.

| id | name | deptno | deptname |
| --- | --- | --- | --- |
| 103 | Paul | 3 | Engineering |
| 101 | John | 1 | Marketing |
| 102 | Lisa | 2 | Sales |

---

2. We will use the employee and department tables to show how a left join works. This example will help you understand how to combine data from two tables while keeping all records from the left (first) table.

| id | name | deptno | deptname |
| --- | --- | --- | --- |
| 105 | Chloe | 5 | null |
| 103 | Paul | 3 | Engineering |
| 101 | John | 1 | Marketing |
| 102 | Lisa | 2 | Sales |
| 104 | Evan | 4 | null |
| 106 | Amy | 6 | null |

---

3. Let’s use the employee and department tables to show how a RIGHT JOIN works in SQL.

| id | name | deptno | deptname |
| --- | --- | --- | --- |
| 103 | Paul | 3 | Engineering |
| 102 | Lisa | 2 | Sales |
| 101 | John | 1 | Marketing |

---

4. Let’s use the employee and department tables to show how a full join works. A full join combines all records from both tables, including unmatched rows from either table.

| id | name | deptno | deptname |
| --- | --- | --- | --- |
| 101 | John | 1 | Marketing |
| 102 | Lisa | 2 | Sales |
| 103 | Paul | 3 | Engineering |
| 104 | Evan | 4 | null |
| 105 | Chloe | 5 | null |
| 106 | Amy | 6 | null |

---

5. Create a cross join between the employee and department tables to show how to combine every row from one table with every row from another table.

| id | name | deptno | deptname |
| --- | --- | --- | --- |
| 105 | Chloe | 5 | Engineering |
| 105 | Chloe | 5 | Sales |
| 105 | Chloe | 5 | Marketing |
| 103 | Paul | 3 | Engineering |
| 103 | Paul | 3 | Sales |
| 103 | Paul | 3 | Marketing |
| 101 | John | 1 | Engineering |
| 101 | John | 1 | Sales |
| 101 | John | 1 | Marketing |
| 102 | Lisa | 2 | Engineering |
| 102 | Lisa | 2 | Sales |
| 102 | Lisa | 2 | Marketing |
| 104 | Evan | 4 | Engineering |
| 104 | Evan | 4 | Sales |
| 104 | Evan | 4 | Marketing |
| 106 | Amy | 6 | Engineering |
| 106 | Amy | 6 | Sales |
| 106 | Amy | 6 | Marketing |

---

6. Let’s use the employee and department tables to show how a semi join works. A semi join returns records from the first table where there is a matching record in the second table.

| id | name | deptno |
| --- | --- | --- |
| 103 | Paul | 3 |
| 101 | John | 1 |
| 102 | Lisa | 2 |

#### Snowflake[¶](#id2 "Link to this heading")

```
-- 1. Use employee and department tables to demonstrate inner join.
SELECT id, name, employee.deptno, deptname
   FROM employee
   INNER JOIN department ON employee.deptno = department.deptno;
 
-- 2. Use employee and department tables to demonstrate left join.
SELECT id, name, employee.deptno, deptname
   FROM employee
   LEFT JOIN department ON employee.deptno = department.deptno;


-- 3. Use employee and department tables to demonstrate right join.
SELECT id, name, employee.deptno, deptname
    FROM employee
    RIGHT JOIN department ON employee.deptno = department.deptno;


-- 4. Use employee and department tables to demonstrate full join.
SELECT id, name, employee.deptno, deptname
    FROM employee
    FULL JOIN department ON employee.deptno = department.deptno;


-- 5. Use employee and department tables to demonstrate cross join.
SELECT id, name, employee.deptno, deptname
    FROM employee
    CROSS JOIN department;

-- 6. Use employee and department tables to demonstrate semi join.
SELECT e.*
    FROM employee e, department d
    WHERE e.deptno = d.deptno;
```

Copy

1. We will use two sample tables - “employee” and “department” - to show how an inner join works. An inner join combines records from both tables where there is a matching value in the specified columns.

| id | name | deptno | deptname |
| --- | --- | --- | --- |
| 103 | Paul | 3 | Engineering |
| 101 | John | 1 | Marketing |
| 102 | Lisa | 2 | Sales |

---

2. Use employee and department tables to demonstrate left join.

| id | name | deptno | deptname |
| --- | --- | --- | --- |
| 105 | Chloe | 5 | null |
| 103 | Paul | 3 | Engineering |
| 101 | John | 1 | Marketing |
| 102 | Lisa | 2 | Sales |
| 104 | Evan | 4 | null |
| 106 | Amy | 6 | null |

---

3. Let’s use the employee and department tables to show how a right join works.

| id | name | deptno | deptname |
| --- | --- | --- | --- |
| 103 | Paul | 3 | Engineering |
| 102 | Lisa | 2 | Sales |
| 101 | John | 1 | Marketing |

---

4. Let’s use the employee and department tables to show how a full join works. A full join combines all records from both tables, including unmatched rows from either table.

| id | name | deptno | deptname |
| --- | --- | --- | --- |
| 105 | Chloe | 5 | null |
| 103 | Paul | 3 | Engineering |
| 101 | John | 1 | Marketing |
| 102 | Lisa | 2 | Sales |
| 104 | Evan | 4 | null |
| 106 | Amy | 6 | null |

---

5. Create a cross join between the employee and department tables to show how each employee can be paired with every department. This example demonstrates how cross joins work by combining all possible combinations of rows from both tables.

| id | name | deptno | deptname |
| --- | --- | --- | --- |
| 105 | Chloe | 5 | Engineering |
| 105 | Chloe | 5 | Sales |
| 105 | Chloe | 5 | Marketing |
| 103 | Paul | 3 | Engineering |
| 103 | Paul | 3 | Sales |
| 103 | Paul | 3 | Marketing |
| 101 | John | 1 | Engineering |
| 101 | John | 1 | Sales |
| 101 | John | 1 | Marketing |
| 102 | Lisa | 2 | Engineering |
| 102 | Lisa | 2 | Sales |
| 102 | Lisa | 2 | Marketing |
| 104 | Evan | 4 | Engineering |
| 104 | Evan | 4 | Sales |
| 104 | Evan | 4 | Marketing |
| 106 | Amy | 6 | Engineering |
| 106 | Amy | 6 | Sales |
| 106 | Amy | 6 | Marketing |

---

6. Let’s use the employee and department tables to show how a semi join works. A semi join returns records from the first table where there is a matching record in the second table.

| id | name | deptno |
| --- | --- | --- |
| 103 | Paul | 3 |
| 101 | John | 1 |
| 102 | Lisa | 2 |

### Known Issues[¶](#known-issues "Link to this heading")

No issues were found

### Related EWIs[¶](#related-ewis "Link to this heading")

No related EWIs

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

The Snowpark Migration Accelerator tool (SMA) is subject to the [Conversion Software Terms of Use](https://www.snowflake.com/en/legal/technical-services-and-education/conversion-software-terms/).

On this page

1. [Description](#description)
2. [Sample Source Patterns](#sample-source-patterns)