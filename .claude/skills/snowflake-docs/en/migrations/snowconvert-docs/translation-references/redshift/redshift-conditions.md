---
auto_generated: true
description: A BETWEEN condition tests expressions for inclusion in a range of values,
  using the keywords BETWEEN and AND. (Redshift SQL Language Reference BETWEEN condition)
last_scraped: '2026-01-14T16:53:37.751781+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/redshift/redshift-conditions
title: SnowConvert AI - Redshift - Conditions | Snowflake Documentation
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)Translation References[Redshift](README.md)Conditions

# SnowConvert AI - Redshift - Conditions[¶](#snowconvert-ai-redshift-conditions "Link to this heading")

## BETWEEN[¶](#between "Link to this heading")

### Description[¶](#description "Link to this heading")

> A `BETWEEN` condition tests expressions for inclusion in a range of values, using the keywords `BETWEEN` and `AND`. ([Redshift SQL Language Reference BETWEEN condition](https://docs.aws.amazon.com/redshift/latest/dg/r_range_condition.html))

### Grammar Syntax[¶](#grammar-syntax "Link to this heading")

```
 expression [ NOT ] BETWEEN expression AND expression
```

Copy

Note

This function is fully supported by [Snowflake](https://docs.snowflake.com/en/sql-reference/functions/coalesce).

### Sample Source Patterns[¶](#sample-source-patterns "Link to this heading")

#### Setup Table[¶](#setup-table "Link to this heading")

##### Redshift[¶](#redshift "Link to this heading")

```
 CREATE TABLE sales (
    id INTEGER IDENTITY(1,1),
    price FLOAT,
    departmentId INTEGER,
    saleDate DATE
);

INSERT INTO sales (price, departmentId, saleDate) VALUES
(5000, 1, '2008-01-01'),
(8000, 1, '2018-01-01'),
(5000, 2, '2010-01-01'),
(7000, 3, '2010-01-01'),
(5000, 1, '2018-01-01'),
(4000, 4, '2010-01-01'),
(3000, 4, '2018-01-01'),
(9000, 5, '2008-01-01'),
(7000, 5, '2018-01-01'),
(6000, 5, '2006-01-01'),
(5000, 5, '2008-01-01'),
(5000, 4, '2018-01-01'),
(8000, 3, '2006-01-01'),
(7000, 3, '2016-01-01'),
(2000, 2, '2018-01-01');
```

Copy

##### Snowflake[¶](#snowflake "Link to this heading")

```
 CREATE TABLE sales (
    id INTEGER IDENTITY(1,1) ORDER,
    price FLOAT,
    departmentId INTEGER,
    saleDate DATE
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "01/08/2025",  "domain": "test" }}';

INSERT INTO sales (price, departmentId, saleDate) VALUES
(5000, 1, '2008-01-01'),
(8000, 1, '2018-01-01'),
(5000, 2, '2010-01-01'),
(7000, 3, '2010-01-01'),
(5000, 1, '2018-01-01'),
(4000, 4, '2010-01-01'),
(3000, 4, '2018-01-01'),
(9000, 5, '2008-01-01'),
(7000, 5, '2018-01-01'),
(6000, 5, '2006-01-01'),
(5000, 5, '2008-01-01'),
(5000, 4, '2018-01-01'),
(8000, 3, '2006-01-01'),
(7000, 3, '2016-01-01'),
(2000, 2, '2018-01-01');
```

Copy

##### Input Code:[¶](#input-code "Link to this heading")

##### Redshift[¶](#id1 "Link to this heading")

```
 SELECT COUNT(*) FROM sales
WHERE departmentId BETWEEN 2 AND 4;

SELECT * FROM sales
WHERE departmentId BETWEEN 4 AND 2;

SELECT * FROM sales
WHERE departmentId NOT BETWEEN 4 AND 2;

SELECT * FROM sales
WHERE departmentId BETWEEN 2 AND 4
AND saleDate BETWEEN '2010-01-01' and '2016-01-01';

select 'some ' between c_start and c_end 
from( select 'same' as c_start, 'some' as c_end );
```

Copy

##### Results[¶](#results "Link to this heading")

| count |
| --- |
| 8 |

| id | price | departmentid | saledate |
| --- | --- | --- | --- |
|  |  |  |  |

| id | price | departmentid | saledate |
| --- | --- | --- | --- |
| 1 | 5000 | 1 | 2008-01-01 |
| 2 | 8000 | 1 | 2018-01-01 |
| 3 | 5000 | 2 | 2010-01-01 |
| 4 | 7000 | 3 | 2010-01-01 |
| 5 | 5000 | 1 | 2018-01-01 |
| 6 | 4000 | 4 | 2010-01-01 |
| 7 | 3000 | 4 | 2018-01-01 |
| 8 | 9000 | 5 | 2008-01-01 |
| 9 | 7000 | 5 | 2018-01-01 |
| 10 | 6000 | 5 | 2006-01-01 |
| 11 | 5000 | 5 | 2008-01-01 |
| 12 | 5000 | 4 | 2018-01-01 |
| 13 | 8000 | 3 | 2006-01-01 |
| 14 | 7000 | 3 | 2016-01-01 |
| 15 | 2000 | 2 | 2018-01-01 |

| id | price | departmentid | saledate |
| --- | --- | --- | --- |
| 3 | 5000 | 2 | 2010-01-01 |
| 4 | 7000 | 3 | 2010-01-01 |
| 6 | 4000 | 4 | 2010-01-01 |
| 14 | 7000 | 3 | 2016-01-01 |

##### Output Code:[¶](#output-code "Link to this heading")

##### Snowflake[¶](#id2 "Link to this heading")

```
 SELECT COUNT(*) FROM
    sales
WHERE departmentId BETWEEN 2 AND 4;

SELECT * FROM
    sales
WHERE departmentId BETWEEN 4 AND 2;

SELECT * FROM
    sales
WHERE departmentId NOT BETWEEN 4 AND 2;

SELECT * FROM
    sales
WHERE departmentId BETWEEN 2 AND 4
AND saleDate BETWEEN '2010-01-01' and '2016-01-01';

select
    RTRIM( 'some ') between c_start and c_end
from( select 'same' as c_start, 'some' as c_end );
```

Copy

##### Results[¶](#id3 "Link to this heading")

| count |
| --- |
| 8 |

| id | price | departmentid | saledate |
| --- | --- | --- | --- |
|  |  |  |  |

| id | price | departmentid | saledate |
| --- | --- | --- | --- |
| 1 | 5000 | 1 | 2008-01-01 |
| 2 | 8000 | 1 | 2018-01-01 |
| 3 | 5000 | 2 | 2010-01-01 |
| 4 | 7000 | 3 | 2010-01-01 |
| 5 | 5000 | 1 | 2018-01-01 |
| 6 | 4000 | 4 | 2010-01-01 |
| 7 | 3000 | 4 | 2018-01-01 |
| 8 | 9000 | 5 | 2008-01-01 |
| 9 | 7000 | 5 | 2018-01-01 |
| 10 | 6000 | 5 | 2006-01-01 |
| 11 | 5000 | 5 | 2008-01-01 |
| 12 | 5000 | 4 | 2018-01-01 |
| 13 | 8000 | 3 | 2006-01-01 |
| 14 | 7000 | 3 | 2016-01-01 |
| 15 | 2000 | 2 | 2018-01-01 |

| id | price | departmentid | saledate |
| --- | --- | --- | --- |
| 3 | 5000 | 2 | 2010-01-01 |
| 4 | 7000 | 3 | 2010-01-01 |
| 6 | 4000 | 4 | 2010-01-01 |
| 14 | 7000 | 3 | 2016-01-01 |

### Known Issues [¶](#known-issues "Link to this heading")

No issues were found.

### Related EWIs[¶](#related-ewis "Link to this heading")

No related EWIs.

## Comparison Condition[¶](#comparison-condition "Link to this heading")

Conditions

### Description [¶](#id4 "Link to this heading")

> Comparison conditions state logical relationships between two values. All comparison conditions are binary operators with a Boolean return type.
>
> ([RedShift SQL Language Reference Comparison Condition](https://docs.aws.amazon.com/redshift/latest/dg/r_comparison_condition.html))

### Grammar Syntax [¶](#id5 "Link to this heading")

Redshift supports the comparison operators described in the following table:

| Operator | Syntax | Description |
| --- | --- | --- |
| < | a < b | Value a is less than value b. |
| > | a > b | Value a is greater than value b. |
| <= | a <= b | Value a is less than or equal to value b. |
| >= | a >= b | Value a is greater than or equal to value b. |
| = | a = b | Value a is equal to value b. |
| <> | != | a <> b | a != b | Value a is not equal to value b. |
| ANY | SOME | a = ANY(subquery) | Value a is equal to any value returned by the subquery. |
| ALL | a <> ALL or != ALL (subquery) | Value a is not equal to any value returned by the subquery. |
| IS TRUE | FALSE | UNKNOWN | a IS TRUE | Value a is Boolean TRUE. |

### Use of comparison operators on Strings[¶](#use-of-comparison-operators-on-strings "Link to this heading")

It is important to note that in Redshift, comparison operators on strings ignore trailing blank spaces. To replicate this behavior in Snowflake, the transformation applies the `RTRIM` function to remove trailing spaces, ensuring equivalent functionality. For more information: [Significance of trailing blanks](https://docs.aws.amazon.com/redshift/latest/dg/r_Character_types.html#r_Character_types-significance-of-trailing-blanks)

### Conversion Table[¶](#conversion-table "Link to this heading")

Most of the operators are directly supported by Snowflake; however, the following operators require transformation:

| Redshift | Snowflake | Comments |
| --- | --- | --- |
| (expression) IS TRUE | expression | Condition is `TRUE`. |
| (expression) IS FALSE | NOT (expression) | Condition is `FALSE`. |
| (expression) IS UNKNOWN | expression IS NULL | Expression evaluates to `NULL` (same as `UNKNOWN`). |

### Sample Source Patterns[¶](#id6 "Link to this heading")

#### Input Code:[¶](#id7 "Link to this heading")

##### Redshift[¶](#id8 "Link to this heading")

```
 CREATE TABLE example_data (
    id INT,
    value INT,
    status BOOLEAN,
    category VARCHAR(10)
);

INSERT INTO example_data (id, value, status, category) VALUES
(1, 50, TRUE, 'A'),
(2, 30, FALSE, 'B'),
(3, 40, NULL, 'C'),
(4, 70, TRUE, 'A '),
(5, 60, FALSE, 'B');

SELECT *
FROM example_data
WHERE value < 60 AND value > 40;

SELECT *
FROM example_data
WHERE value <= 60 AND value >= 40;

SELECT *
FROM example_data
WHERE category = 'A';

SELECT *
FROM example_data
WHERE category != 'A' AND category <> 'B';

SELECT *
FROM example_data
WHERE category = ANY(SELECT category FROM example_data WHERE value > 60); --SOME

SELECT *
FROM example_data
WHERE value <> ALL (SELECT value FROM example_data WHERE status = TRUE);

SELECT *
FROM example_data
WHERE status IS TRUE;

SELECT *
FROM example_data
WHERE status IS FALSE;

SELECT *
FROM example_data
WHERE status IS UNKNOWN;
```

Copy

##### Results[¶](#id9 "Link to this heading")

| id | value | status | category |
| --- | --- | --- | --- |
| 1 | 50 | true | A |

| id | value | status | category |
| --- | --- | --- | --- |
| 1 | 50 | true | A |
| 3 | 40 | null | C |
| 5 | 60 | false | B |

| id | value | status | category |
| --- | --- | --- | --- |
| 1 | 50 | true | A |
| 4 | 70 | true | A |

| id | value | status | category |
| --- | --- | --- | --- |
| 3 | 40 | null | C |

| id | value | status | category |
| --- | --- | --- | --- |
| 1 | 50 | true | A |
| 4 | 70 | true | A |

| id | value | status | category |
| --- | --- | --- | --- |
| 2 | 30 | false | B |
| 4 | 40 | null | C |
| 5 | 60 | false | B |

| id | value | status | category |
| --- | --- | --- | --- |
| 1 | 50 | true | A |
| 4 | 70 | true | A |

| id | value | status | category |
| --- | --- | --- | --- |
| 2 | 30 | false | B |
| 5 | 60 | false | B |

| id | value | status | category |
| --- | --- | --- | --- |
| 4 | 40 | null | C |

**Output Code:**

##### Snowflake[¶](#id10 "Link to this heading")

```
 CREATE TABLE example_data (
    id INT,
    value INT,
    status BOOLEAN,
    category VARCHAR(10)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}';

INSERT INTO example_data (id, value, status, category) VALUES
(1, 50, TRUE, 'A'),
(2, 30, FALSE, 'B'),
(3, 40, NULL, 'C'),
(4, 70, TRUE, 'A '),
(5, 60, FALSE, 'B');

SELECT *
FROM
    example_data
WHERE value < 60 AND value > 40;

SELECT *
FROM
    example_data
WHERE value <= 60 AND value >= 40;

SELECT *
FROM
    example_data
WHERE category = 'A';

SELECT *
FROM
    example_data
WHERE category != 'A' AND category <> 'B';

SELECT *
FROM
    example_data
WHERE category = ANY(SELECT category FROM
            example_data
        WHERE value > 60); --SOME

SELECT *
FROM
    example_data
WHERE value <> ALL (SELECT value FROM
            example_data
        WHERE status = TRUE);

SELECT *
FROM
    example_data
WHERE status;

SELECT *
FROM
    example_data
WHERE
    NOT status;

SELECT *
FROM
    example_data
WHERE status IS NULL;
```

Copy

##### Results[¶](#id11 "Link to this heading")

| id | value | status | category |
| --- | --- | --- | --- |
| 1 | 50 | true | A |

| id | value | status | category |
| --- | --- | --- | --- |
| 1 | 50 | true | A |
| 3 | 40 | null | C |
| 5 | 60 | false | B |

| id | value | status | category |
| --- | --- | --- | --- |
| 1 | 50 | true | A |
| 4 | 70 | true | A |

| id | value | status | category |
| --- | --- | --- | --- |
| 3 | 40 | null | C |

| id | value | status | category |
| --- | --- | --- | --- |
| 1 | 50 | true | A |
| 4 | 70 | true | A |

| id | value | status | category |
| --- | --- | --- | --- |
| 2 | 30 | false | B |
| 4 | 40 | null | C |
| 5 | 60 | false | B |

| id | value | status | category |
| --- | --- | --- | --- |
| 1 | 50 | true | A |
| 4 | 70 | true | A |

| id | value | status | category |
| --- | --- | --- | --- |
| 2 | 30 | false | B |
| 5 | 60 | false | B |

| id | value | status | category |
| --- | --- | --- | --- |
| 4 | 40 | null | C |

### Known Issues[¶](#id12 "Link to this heading")

No issues were found.

### Related EWIs[¶](#id13 "Link to this heading")

There are no known issues.

## EXISTS[¶](#exists "Link to this heading")

### Description[¶](#id14 "Link to this heading")

> EXISTS conditions test for the existence of rows in a subquery, and return true if a subquery returns at least one row. If NOT is specified, the condition returns true if a subquery returns no rows. ([Redshift SQL Language Reference EXISTS condition](https://docs.aws.amazon.com/redshift/latest/dg/r_exists_condition.html))

### Grammar Syntax[¶](#id15 "Link to this heading")

```
 [ NOT ] EXISTS (table_subquery)
```

Copy

Note

This function is fully supported by [Snowflake](https://docs.snowflake.com/en/sql-reference/functions/coalesce).

### Sample Source Patterns[¶](#id16 "Link to this heading")

#### Setup Table[¶](#id17 "Link to this heading")

```
 CREATE TABLE ExistsTest (
    id INTEGER,
    name VARCHAR(30),
    lastname VARCHAR(30)
);

INSERT INTO ExistsTest (id, name, lastname) VALUES
 (1, 'name1', 'lastname1'),
 (2, 'name2', NULL),
 (3, 'name3', 'lastname3'),
 (4, 'name4', NULL);
```

Copy

```
 CREATE TABLE ExistsTest (
    id INTEGER,
    name VARCHAR(30),
    lastname VARCHAR(30)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "01/08/2025",  "domain": "test" }}'

INSERT INTO ExistsTest (id, name, lastname) VALUES
 (1, 'name1', 'lastname1'),
 (2, 'name2', NULL),
 (3, 'name3', 'lastname3'),
 (4, 'name4', NULL);
```

Copy

##### Input Code:[¶](#id18 "Link to this heading")

##### Redshift[¶](#id19 "Link to this heading")

```
 SELECT * FROM ExistsTest
WHERE EXISTS (
SELECT 1 FROM ExistsTest
WHERE lastname = 'lastname1'
)
ORDER BY id;
```

Copy

##### Results[¶](#id20 "Link to this heading")

| ID | NAME | LASTNAME |
| --- | --- | --- |
| 1 | name1 | lastname1 |
| 2 | name2 | NULL |
| 3 | name3 | lastname3 |
| 4 | name4 | NULL |

##### Output Code:[¶](#id21 "Link to this heading")

##### Snowflake[¶](#id22 "Link to this heading")

```
 SELECT * FROM
ExistsTest
WHERE EXISTS (
SELECT 1 FROM
ExistsTest
WHERE lastname = 'lastname1'
)
ORDER BY id;
```

Copy

##### Results[¶](#id23 "Link to this heading")

| ID | NAME | LASTNAME |
| --- | --- | --- |
| 1 | name1 | lastname1 |
| 2 | name2 | NULL |
| 3 | name3 | lastname3 |
| 4 | name4 | NULL |

### Related EWIs[¶](#id24 "Link to this heading")

No related EWIs.

### Known Issues [¶](#id25 "Link to this heading")

No issues were found.

## IN[¶](#in "Link to this heading")

### Description[¶](#id26 "Link to this heading")

> An IN condition tests a value for membership in a set of values or in a subquery. ([Redshift SQL Language Reference IN condition](https://docs.aws.amazon.com/redshift/latest/dg/r_in_condition.html))

### Grammar Syntax[¶](#id27 "Link to this heading")

```
 expression [ NOT ] IN (expr_list | table_subquery)
```

Copy

Note

This function is fully supported by [Snowflake](https://docs.snowflake.com/en/sql-reference/functions/coalesce).

### Sample Source Patterns[¶](#id28 "Link to this heading")

#### Setup Table[¶](#id29 "Link to this heading")

##### Redshift[¶](#id30 "Link to this heading")

```
 CREATE TABLE sales (
    id INTEGER IDENTITY(1,1),
    price FLOAT,
    saleDate DATE
);

INSERT INTO sales (price, saleDate) VALUES
(5000, '12/19/2024'),
(4000, '12/18/2024'),
(2000, '12/17/2024'),
(1000, '11/11/2024'),
(7000, '10/10/2024'),
(7000, '05/12/2024');

CREATE TABLE InTest (
col1 Varchar(20) COLLATE CASE_INSENSITIVE,
col2 Varchar(30) COLLATE CASE_SENSITIVE,
d1 date,
num integer,
idx integer);

INSERT INTO InTest values ('A', 'A', ('2012-03-02'), 4,6);
INSERT INTO InTest values ('a', 'a', ('2014-01-02'), 41,7);
```

Copy

##### Snowflake[¶](#id31 "Link to this heading")

```
 CREATE TABLE InTest (
    id INTEGER IDENTITY(1,1) ORDER,
    price FLOAT,
    saleDate DATE
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "01/09/2025",  "domain": "test" }}';

INSERT INTO InTest (price, saleDate) VALUES
(5000, '12/19/2024'),
(4000, '12/18/2024'),
(2000, '12/17/2024'),
(1000, '11/11/2024'),
(7000, '10/10/2024'),
(7000, '05/12/2024');

CREATE TABLE InTest (
col1 Varchar(20) COLLATE 'en-ci',
col2 Varchar(30) COLLATE 'en-cs',
d1 date,
num integer,
idx integer)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "01/16/2025",  "domain": "test" }}';

INSERT INTO InTest
values ('A', 'A', ('2012-03-02'), 4,6);
INSERT INTO InTest
values ('a', 'a', ('2014-01-02'), 41,7);
```

Copy

##### Input Code:[¶](#id32 "Link to this heading")

##### Redshift[¶](#id33 "Link to this heading")

```
 SELECT * FROM sales
WHERE id IN (2,3);

SELECT 5 IN (
SELECT id FROM sales
WHERE price = 7000
) AS ValidId;

select t.col1 in ('a ','b','c') as r1, t.col2 in ('a ','b','c') as r2 from InTest t order by t.idx;
```

Copy

##### Results[¶](#id34 "Link to this heading")

| ID | PRICE | SALEDATE |
| --- | --- | --- |
| 2 | 4000 | 2024-12-18 |
| 3 | 2000 | 2024-12-17 |

| VALIDID |
| --- |
| TRUE |

| R1 | R2 |
| --- | --- |
| TRUE | FALSE |
| TRUE | TRUE |

##### Output Code:[¶](#id35 "Link to this heading")

##### Snowflake[¶](#id36 "Link to this heading")

```
 SELECT * FROM
    sales
WHERE id IN (2,3);

SELECT 5 IN (
SELECT id FROM
 sales
WHERE price = 7000
) AS ValidId;

select t.col1 in (RTRIM('a '), RTRIM('b'), RTRIM('c')) as r1, t.col2 in (RTRIM('a '), RTRIM('b'), RTRIM('c')) as r2 from
InTest t order by t.idx;
```

Copy

##### Results[¶](#id37 "Link to this heading")

| ID | PRICE | SALEDATE |
| --- | --- | --- |
| 2 | 4000 | 2024-12-18 |
| 3 | 2000 | 2024-12-17 |

| VALIDID |
| --- |
| TRUE |

| R1 | R2 |
| --- | --- |
| TRUE | FALSE |
| TRUE | TRUE |

### Related EWIs[¶](#id38 "Link to this heading")

No related EWIs.

### Known Issues [¶](#id39 "Link to this heading")

No issues were found.

## Logical Conditions[¶](#logical-conditions "Link to this heading")

### Description [¶](#id40 "Link to this heading")

> Logical conditions combine the result of two conditions to produce a single result. All logical conditions are binary operators with a Boolean return type. ([Redshift SQL Language reference Logical Conditions](https://docs.aws.amazon.com/redshift/latest/dg/r_logical_condition.html)).

Note

This grammar is fully supported in [Snowflake](https://docs.snowflake.com/en/sql-reference/operators-logical).

### Grammar Syntax [¶](#id41 "Link to this heading")

```
expression
{ AND | OR }
expression
NOT expression
```

Copy

| E1 | E2 | E1 AND E2 | E1 OR E2 | NOT E2 |
| --- | --- | --- | --- | --- |
| TRUE | TRUE | TRUE | TRUE | FALSE |
| TRUE | FALSE | FALSE | TRUE | TRUE |
| TRUE | UNKNOWN | UNKNOWN | TRUE | UNKNOWN |
| FALSE | TRUE | FALSE | TRUE |  |
| FALSE | FALSE | FALSE | FALSE |  |
| FALSE | UNKNOWN | FALSE | UNKNOWN |  |
| UNKNOWN | TRUE | UNKNOWN | TRUE |  |
| UNKNOWN | FALSE | FALSE | UNKNOWN |  |
| UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |  |

### Sample Source Patterns[¶](#id42 "Link to this heading")

#### Setup data[¶](#setup-data "Link to this heading")

##### Redshift[¶](#id43 "Link to this heading")

```
 CREATE TABLE employee (
    employee_id INT,
    active BOOLEAN,
    department VARCHAR(100),
    hire_date DATE,
    salary INT
);

INSERT INTO employee (employee_id, active, department, hire_date, salary) VALUES
    (1, TRUE, 'Engineering', '2021-01-15', 70000),
    (2, FALSE, 'HR', '2020-03-22', 50000),
    (3, NULL, 'Marketing', '2019-05-10', 60000),
    (4, TRUE, 'Engineering', NULL, 65000),
    (5, TRUE, 'Sales', '2018-11-05', NULL);
```

Copy

##### Input Code:[¶](#id44 "Link to this heading")

##### Redshift[¶](#id45 "Link to this heading")

```
 SELECT
    employee_id,
    (active AND department = 'Engineering') AS is_active_engineering,
    (department = 'HR' OR salary > 60000) AS hr_or_high_salary,
    NOT active AS is_inactive,
    (hire_date IS NULL) AS hire_date_missing,
    (salary IS NULL OR salary < 50000) AS low_salary_or_no_salary
FROM employee;
```

Copy

##### Results[¶](#id46 "Link to this heading")

| EMPLOYEE\_ID | IS\_ACTIVE\_ENGINEERING | HR\_OR\_HIGH\_SALARY | IS\_INACTIVE | HIRE\_DATE\_MISSING | LOW\_SALARY\_OR\_NO\_SALARY |
| --- | --- | --- | --- | --- | --- |
| 1 | TRUE | TRUE | FALSE | FALSE | FALSE |
| 2 | FALSE | TRUE | TRUE | FALSE | FALSE |
| 3 | FALSE | FALSE | NULL | FALSE | FALSE |
| 4 | TRUE | TRUE | FALSE | TRUE | FALSE |
| 5 | FALSE | NULL | FALSE | FALSE | TRUE |

**Output Code:**

##### Snowflake[¶](#id47 "Link to this heading")

```
 SELECT
    employee_id,
    (active AND department = 'Engineering') AS is_active_engineering,
    (department = 'HR' OR salary > 60000) AS hr_or_high_salary,
    NOT active AS is_inactive,
    (hire_date IS NULL) AS hire_date_missing,
    (salary IS NULL OR salary < 50000) AS low_salary_or_no_salary
FROM
    employee;
```

Copy

##### Results[¶](#id48 "Link to this heading")

| EMPLOYEE\_ID | IS\_ACTIVE\_ENGINEERING | HR\_OR\_HIGH\_SALARY | IS\_INACTIVE | HIRE\_DATE\_MISSING | LOW\_SALARY\_OR\_NO\_SALARY |
| --- | --- | --- | --- | --- | --- |
| 1 | TRUE | TRUE | FALSE | FALSE | FALSE |
| 2 | FALSE | TRUE | TRUE | FALSE | FALSE |
| 3 | FALSE | FALSE | NULL | FALSE | FALSE |
| 4 | TRUE | TRUE | FALSE | TRUE | FALSE |
| 5 | FALSE | NULL | FALSE | FALSE | TRUE |

### Known Issues[¶](#id49 "Link to this heading")

No issues were found.

### Related EWIs[¶](#id50 "Link to this heading")

There are no known issues.

## NULL[¶](#null "Link to this heading")

### Description[¶](#id51 "Link to this heading")

> The null condition tests for nulls, when a value is missing or unknown. ([Redshift SQL Language Reference NULL condition](https://docs.aws.amazon.com/redshift/latest/dg/r_null_condition.html))

### Grammar Syntax[¶](#id52 "Link to this heading")

```
 expression IS [ NOT ] NULL
```

Copy

Note

This function is fully supported by [Snowflake](https://docs.snowflake.com/en/sql-reference/functions/coalesce).

### Sample Source Patterns[¶](#id53 "Link to this heading")

#### Setup Table[¶](#id54 "Link to this heading")

##### Redshift[¶](#id55 "Link to this heading")

```
 CREATE TABLE NullTest (
    id INTEGER,
    name VARCHAR(30),
    lastname VARCHAR(30)
);

INSERT INTO NullTest (id, name, lastname) VALUES 
 (1, 'name1', 'lastname1'),
 (2, 'name2', NULL),
 (3, 'name3', 'lastname3'),
 (4, 'name4', NULL);
```

Copy

##### Snowflake[¶](#id56 "Link to this heading")

```
 CREATE TABLE NullTest (
    id INTEGER,
    name VARCHAR(30),
    lastname VARCHAR(30)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "01/08/2025",  "domain": "test" }}';

INSERT INTO NullTest (id, name, lastname) VALUES
 (1, 'name1', 'lastname1'),
 (2, 'name2', NULL),
 (3, 'name3', 'lastname3'),
 (4, 'name4', NULL);
```

Copy

##### Input Code:[¶](#id57 "Link to this heading")

##### Redshift[¶](#id58 "Link to this heading")

```
 SELECT * FROM nulltest
WHERE lastname IS NULL;
```

Copy

##### Results[¶](#id59 "Link to this heading")

| ID | NAME | LASTNAME |
| --- | --- | --- |
| 2 | name2 | NULL |
| 4 | name4 | NULL |

##### Output Code:[¶](#id60 "Link to this heading")

##### Snowflake[¶](#id61 "Link to this heading")

```
 SELECT * FROM
    nulltest
WHERE lastname IS NULL;
```

Copy

##### Results[¶](#id62 "Link to this heading")

| ID | NAME | LASTNAME |
| --- | --- | --- |
| 2 | name2 | NULL |
| 4 | name4 | NULL |

### Known Issues [¶](#id63 "Link to this heading")

No issues were found.

### Related EWIs[¶](#id64 "Link to this heading")

No related EWIs.

## Pattern-matching conditions[¶](#pattern-matching-conditions "Link to this heading")

### Description [¶](#id65 "Link to this heading")

A pattern-matching operator searches a string for a pattern specified in the conditional expression and returns true or false depend on whether it finds a match. Amazon Redshift uses three methods for pattern matching:

* [LIKE expressions](#like) The LIKE operator compares a string expression, such as a column name, with a pattern that uses the wildcard characters `%` (percent) and `_` (underscore). LIKE pattern matching always covers the entire string. LIKE performs a case-sensitive match and ILIKE performs a case-insensitive match.
* [SIMILAR TO regular expressions](#similar-to) The SIMILAR TO operator matches a string expression with a SQL standard regular expression pattern, which can include a set of pattern-matching metacharacters that includes the two supported by the LIKE operator. SIMILAR TO matches the entire string and performs a case-sensitive match.
* [POSIX-style regular expressions](#posix-operators) POSIX regular expressions provide a more powerful means for pattern matching than the LIKE and SIMILAR TO operators. POSIX regular expression patterns can match any portion of the string and performs a case-sensitive match.
  ([Redshift SQL Language reference Pattern-matching conditions](https://docs.aws.amazon.com/redshift/latest/dg/pattern-matching-conditions.html)).

### Known Issues[¶](#id66 "Link to this heading")

* In Snowflake, the behavior for scenarios such as (`LIKE`, `SIMILAR` TO, and `POSIX Operators`) can vary when the column is of type CHAR. For example:

### Code[¶](#code "Link to this heading")

```
 CREATE TEMPORARY TABLE pattern_matching_sample (
  col1 CHAR(10),
  col2 VARCHAR(10)
);

INSERT INTO pattern_matching_sample VALUES ('1','1');
INSERT INTO pattern_matching_sample VALUES ('1234567891','1234567891');
INSERT INTO pattern_matching_sample VALUES ('234567891','234567891');

SELECT
col1 LIKE '%1' as "like(CHAR(10))",
COL2 LIKE '%1' as "like(VARCHAR(10))"
FROM
pattern_matching_sample;
```

Copy

#### Redshift Results[¶](#redshift-results "Link to this heading")

| like(CHAR(10)) | like(VARCHAR(10)) |
| --- | --- |
| FALSE | TRUE |
| TRUE | TRUE |
| FALSE | TRUE |

##### Snowflake Results[¶](#snowflake-results "Link to this heading")

| like(CHAR(10)) | like(VARCHAR(10)) |
| --- | --- |
| TRUE | TRUE |
| TRUE | TRUE |
| TRUE | TRUE |

It appears that, because CHAR(10) is “fixed-length,” it assumes the ‘%1’ pattern must match a ‘1’ in the 10th position of a CHAR(10) column. However, in Snowflake, it matches if a ‘1’ exists in the string, with any sequence of zero or more characters preceding it.

## LIKE[¶](#like "Link to this heading")

Pattern-matching conditions

### Description [¶](#id67 "Link to this heading")

> The LIKE operator compares a string expression, such as a column name, with a pattern that uses the wildcard characters % (percent) and \_ (underscore). LIKE pattern matching always covers the entire string. To match a sequence anywhere within a string, the pattern must start and end with a percent sign. ([Redshift SQL Language reference LIKE](https://docs.aws.amazon.com/redshift/latest/dg/r_patternmatching_condition_like.html)).

Note

This grammar is fully supported in [Snowflake](https://docs.snowflake.com/en/sql-reference/operators-logical).

Note

In Snowflake the cases where the escape character is not provided, the default Redshift escape character `'\\'` will be added for full equivalence.

### Grammar Syntax [¶](#id68 "Link to this heading")

```
 expression [ NOT ] LIKE | ILIKE pattern [ ESCAPE 'escape_char' ]
```

Copy

### Sample Source Patterns[¶](#id69 "Link to this heading")

#### **Setup data**[¶](#id70 "Link to this heading")

##### Redshift[¶](#id71 "Link to this heading")

```
 CREATE TABLE like_ex(name VARCHAR(20));

INSERT INTO like_ex VALUES
  ('John  Dddoe'),
  ('Joe   Doe'),
  ('Joe   Doe '),
  (' Joe   Doe '),
  (' Joe \n Doe '),
  ('John_down'),
  ('Joe down'),
  ('Elaine'),
  (''),
  (null),
  ('1000 times'),
  ('100%');
```

Copy

#### Like[¶](#id72 "Link to this heading")

##### Input Code:[¶](#id73 "Link to this heading")

##### Redshift[¶](#id74 "Link to this heading")

```
SELECT name
  FROM like_ex
  WHERE name LIKE '%Jo%oe%'
  ORDER BY name;
```

Copy

##### Results[¶](#id75 "Link to this heading")

| NAME |
| --- |
| Joe Doe |
| Joe Doe |
| Joe Doe |
| Joe Doe |
| John Dddoe |

**Output Code:**

##### Snowflake[¶](#id76 "Link to this heading")

```
 SELECT name
  FROM like_ex
  WHERE name LIKE '%Jo%oe%' ESCAPE '\\'
  ORDER BY name;
```

Copy

##### Results[¶](#id77 "Link to this heading")

| NAME |
| --- |
| Joe Doe |
| Joe Doe |
| Joe Doe |
| Joe Doe |
| John Dddoe |

#### Not like[¶](#not-like "Link to this heading")

##### Input Code:[¶](#id78 "Link to this heading")

##### Redshift[¶](#id79 "Link to this heading")

```
 SELECT name
  FROM like_ex
  WHERE name NOT LIKE '%Jo%oe%'
  ORDER BY name;
```

Copy

##### Results[¶](#id80 "Link to this heading")

| NAME |
| --- |
|  |
| 100% |
| 1000 times |
| Elaine |
| Joe down |
| John\_down |

dd

**Output Code:**

##### Snowflake[¶](#id81 "Link to this heading")

```
 SELECT name
  FROM like_ex
  WHERE name NOT LIKE '%Jo%oe%' ESCAPE '\\'
  ORDER BY name;
```

Copy

##### Results[¶](#id82 "Link to this heading")

| NAME |
| --- |
|  |
| 100% |
| 1000 times |
| Elaine |
| Joe down |
| John\_down |

#### Escape characters[¶](#escape-characters "Link to this heading")

##### Input Code:[¶](#id83 "Link to this heading")

##### Redshift[¶](#id84 "Link to this heading")

```
 SELECT name
  FROM like_ex
  WHERE name LIKE '%J%h%^_do%' ESCAPE '^'
  ORDER BY name;
 
SELECT name
 FROM like_ex
 WHERE name LIKE '100\\%'
 ORDER BY 1;
```

Copy

##### Results[¶](#id85 "Link to this heading")

| NAME |
| --- |
| John\_down |

| NAME |
| --- |
| 100% |

**Output Code:**

##### Snowflake[¶](#id86 "Link to this heading")

```
 SELECT name
  FROM like_ex
  WHERE name LIKE '%J%h%^_do%' ESCAPE '^'
  ORDER BY name;
 
SELECT name
 FROM like_ex
 WHERE name LIKE '100\\%' ESCAPE '\\'
 ORDER BY 1;
```

Copy

##### Results[¶](#id87 "Link to this heading")

| NAME |
| --- |
| John\_down |

| NAME |
| --- |
| 100% |

#### ILike[¶](#ilike "Link to this heading")

##### Input Code:[¶](#id88 "Link to this heading")

##### Redshift[¶](#id89 "Link to this heading")

```
 SELECT 'abc' LIKE '_B_' AS r1,
       'abc' ILIKE '_B_' AS r2;
```

Copy

##### Results[¶](#id90 "Link to this heading")

| R1 | R2 |
| --- | --- |
| FALSE | TRUE |

**Output Code:**

##### Snowflake[¶](#id91 "Link to this heading")

```
 SELECT 'abc' LIKE '_B_' ESCAPE '\\' AS r1,
       'abc' ILIKE '_B_' ESCAPE '\\' AS r2;
```

Copy

##### Results[¶](#id92 "Link to this heading")

| R1 | R2 |
| --- | --- |
| FALSE | TRUE |

#### Operators[¶](#operators "Link to this heading")

The following operators are translated as follows:

| Redshift | Snowflake |
| --- | --- |
| ~~ | LIKE |
| !~~ | NOT LIKE |
| ~~\* | ILIKE |
| !~~\* | NOT ILIKE |

##### Input Code:[¶](#id93 "Link to this heading")

##### Redshift[¶](#id94 "Link to this heading")

```
 SELECT 'abc' ~~ 'abc' AS r1,
       'abc' !~~ 'a%' AS r2,
       'abc' ~~* '_B_' AS r3,
       'abc' !~~* '_B_' AS r4;
```

Copy

##### Results[¶](#id95 "Link to this heading")

| R1 | R2 | R3 | R4 |
| --- | --- | --- | --- |
| TRUE | FALSE | TRUE | FALSE |

**Output Code:**

##### Snowflake[¶](#id96 "Link to this heading")

```
 SELECT 'abc' LIKE 'abc' ESCAPE '\\' AS r1,
       'abc' NOT LIKE 'a%' ESCAPE '\\' AS r2,
       'abc' ILIKE '_B_' ESCAPE '\\' AS r3,
       'abc' NOT ILIKE '_B_' ESCAPE '\\' AS r4;
```

Copy

##### Results[¶](#id97 "Link to this heading")

| R1 | R2 | R3 | R4 |
| --- | --- | --- | --- |
| TRUE | FALSE | TRUE | FALSE |

### Known Issues[¶](#id98 "Link to this heading")

1. The behavior of fixed char types may differ. Click [here](#id12) for more information.

### Related EWIs[¶](#id99 "Link to this heading")

There are no known issues.

## POSIX Operators[¶](#posix-operators "Link to this heading")

Pattern-matching conditions

### Description [¶](#id100 "Link to this heading")

> A POSIX regular expression is a sequence of characters that specifies a match pattern. A string matches a regular expression if it is a member of the regular set described by the regular expression. POSIX regular expression patterns can match any portion of a string. ([Redshift SQL Language reference POSIX Operators](https://docs.aws.amazon.com/redshift/latest/dg/pattern-matching-conditions-posix.html)).

Warning

This grammar is partially supported in [Snowflake](https://docs.snowflake.com/en/sql-reference/operators-logical). POSIX Operators are transformed to [REGEXP\_COUNT](https://docs.snowflake.com/en/sql-reference/functions/regexp_count) in Snowflake.

### Grammar Syntax [¶](#id101 "Link to this heading")

```
 expression [ ! ] ~ pattern
```

Copy

### POSIX pattern-matching metacharacters[¶](#posix-pattern-matching-metacharacters "Link to this heading")

POSIX pattern matching supports the following metacharacters (all the cases are supported in Snowflake):

| POSIX | Description |
| --- | --- |
| . | Matches any single character. |
| `*` | Matches zero or more occurrences. |
| `+` | Matches one or more occurrences. |
| `?` | Matches zero or one occurrence. |
| `|` | Specifies alternative matches. |
| `^` | Matches the beginning-of-line character. |
| `$` | Matches the end-of-line character. |
| `$` | Matches the end of the string. |
| [ ] | Brackets specify a matching list, that should match one expression in the list. |
| `( )` | Parentheses group items into a single logical item. |
| `{m}` | Repeat the previous item exactly *m* times. |
| `{m,}` | Repeat the previous item *m* or more times. |
| `{m,n}` | Repeat the previous item at least *m* and not more than *n* times. |
| `[: :]` | Matches any character within a POSIX character class. In the following character classes, Amazon Redshift supports only ASCII characters, just like Snowflake: `[:alnum:]`, `[:alpha:]`, `[:lower:]`, `[:upper:]` |

The parameters ‘m’ (enables multiline mode) and ‘s’ (allows the POSIX wildcard character `.` to match new lines) are used to achieve full equivalence in Snowflake. For more information please refer to [Specifying the parameters for the regular expression in Snowflake](https://docs.snowflake.com/en/sql-reference/functions-regexp#specifying-the-parameters-for-the-regular-expression).

### Sample Source Patterns[¶](#id102 "Link to this heading")

#### **Setup data**[¶](#id103 "Link to this heading")

##### Redshift[¶](#id104 "Link to this heading")

```
 CREATE TABLE posix_test_table (
    id INT,
    column_name VARCHAR(255)
);

INSERT INTO posix_test_table (id, column_name)
VALUES
    (1, 'abc123\nhello world'),
    (2, 'test string\nwith multiple lines\nin this entry'),
    (3, '123abc\nanother line\nabc123'),
    (4, 'line1\nline2\nline3'),
    (5, 'start\nmiddle\nend'),
    (6, 'a@b#c!\nmore text here'),
    (7, 'alpha\nbeta\ngamma'),
    (8, 'uppercase\nlowercase'),
    (9, 'line1\nline2\nline3\nline4'),
    (10, '1234567890\nmore digits'),
    (11, 'abc123\nabc456\nabc789'),
    (12, 'start\nend\nmiddle'),
    (13, 'this is the first line\nthis is the second line'),
    (14, 'special characters\n!@#$%^&*()');
```

Copy

#### . : Matches any character[¶](#matches-any-character "Link to this heading")

##### Input Code:[¶](#id105 "Link to this heading")

##### Redshift[¶](#id106 "Link to this heading")

```
 SELECT id, column_name
FROM posix_test_table
WHERE column_name ~ 'a.c';
```

Copy

##### Results[¶](#id107 "Link to this heading")

| ID | COLUMN\_NAME |
| --- | --- |
| 1 | abc123 hello world |
| 3 | 123abc another line abc123 |
| 11 | abc123 abc456 abc789 |

**Output Code:**

##### Snowflake[¶](#id108 "Link to this heading")

```
 SELECT id, column_name
FROM posix_test_table
WHERE REGEXP_COUNT(column_name, 'a.c', 1, 'ms') > 0;
```

Copy

##### Results[¶](#id109 "Link to this heading")

| ID | COLUMN\_NAME |
| --- | --- |
| 1 | abc123 hello world |
| 3 | 123abc another line abc123 |
| 11 | abc123 abc456 abc789 |

#### \* : Matches zero or more occurrences.[¶](#matches-zero-or-more-occurrences "Link to this heading")

##### Input Code:[¶](#id110 "Link to this heading")

##### Redshift[¶](#id111 "Link to this heading")

```
 SELECT id, column_name
FROM posix_test_table
WHERE column_name ~ 'a*b';
```

Copy

##### Results[¶](#id112 "Link to this heading")

| ID | COLUMN\_NAME |
| --- | --- |
| 1 | abc123 hello world |
| 3 | 123abc another line abc123 |
| 6 | a@b#c! more text here |
| 7 | alpha beta gamma |
| 11 | abc123 abc456 abc789 |

**Output Code:**

##### Snowflake[¶](#id113 "Link to this heading")

```
 SELECT id, column_name
FROM posix_test_table
WHERE REGEXP_COUNT(column_name, 'a*b', 1, 'ms') > 0;
```

Copy

##### Results[¶](#id114 "Link to this heading")

| ID | COLUMN\_NAME |
| --- | --- |
| 1 | abc123 hello world |
| 3 | 123abc another line abc123 |
| 6 | a@b#c! more text here |
| 7 | alpha beta gamma |
| 11 | abc123 abc456 abc789 |

#### ? : Matches zero or one occurrence[¶](#matches-zero-or-one-occurrence "Link to this heading")

##### Input Code:[¶](#id115 "Link to this heading")

##### Redshift[¶](#id116 "Link to this heading")

```
 SELECT id, column_name
FROM posix_test_table
WHERE column_name !~ 'a?b';
```

Copy

##### Results[¶](#id117 "Link to this heading")

| ID | COLUMN\_NAME |
| --- | --- |
| 2 | test string with multiple lines in this entry |
| 4 | line1 line2 line3 |
| 5 | start middle end |
| 8 | uppercase lowercase |
| 9 | line1 line2 line3 line4 |
| 10 | 1234567890 more digits |
| 12 | start end middle |
| 13 | this is the first line this is the second line |
| 14 | special characters !@#$%^&\*() |

**Output Code:**

##### Snowflake[¶](#id118 "Link to this heading")

```
 SELECT id, column_name
FROM posix_test_table
WHERE REGEXP_COUNT(column_name, 'a?b', 1, 'ms') = 0;
```

Copy

##### Results[¶](#id119 "Link to this heading")

| ID | COLUMN\_NAME |
| --- | --- |
| 2 | test string with multiple lines in this entry |
| 4 | line1 line2 line3 |
| 5 | start middle end |
| 8 | uppercase lowercase |
| 9 | line1 line2 line3 line4 |
| 10 | 1234567890 more digits |
| 12 | start end middle |
| 13 | this is the first line this is the second line |
| 14 | special characters !@#$%^&\*() |

#### ^ : Matches the beginning-of-line character[¶](#matches-the-beginning-of-line-character "Link to this heading")

##### Input Code:[¶](#id120 "Link to this heading")

##### Redshift[¶](#id121 "Link to this heading")

```
 SELECT id, column_name
FROM posix_test_table
WHERE column_name ~ '^abc';
```

Copy

##### Results[¶](#id122 "Link to this heading")

| ID | COLUMN\_NAME |
| --- | --- |
| 1 | abc123 hello world |
| 3 | 123abc another line abc123 |
| 11 | abc123 abc456 abc789 |

**Output Code:**

##### Snowflake[¶](#id123 "Link to this heading")

```
 SELECT id, column_name
FROM posix_test_table
WHERE REGEXP_COUNT(column_name, '^abc', 1, 'ms') > 0;
```

Copy

##### Results[¶](#id124 "Link to this heading")

| ID | COLUMN\_NAME |
| --- | --- |
| 1 | abc123 hello world |
| 3 | 123abc another line abc123 |
| 11 | abc123 abc456 abc789 |

#### $ : Matches the end of the string.[¶](#matches-the-end-of-the-string "Link to this heading")

##### Input Code:[¶](#id125 "Link to this heading")

##### Redshift[¶](#id126 "Link to this heading")

```
 SELECT id, column_name
FROM posix_test_table
WHERE column_name !~ '123$';
```

Copy

##### Results[¶](#id127 "Link to this heading")

| ID | COLUMN\_NAME |
| --- | --- |
| 2 | test string with multiple lines in this entry |
| 4 | line1 line2 line3 |
| 5 | start middle end |
| 6 | a@b#c! more text here |
| 7 | alpha beta gamma |
| 8 | uppercase lowercase |
| 9 | line1 line2 line3 line4 |
| 10 | 1234567890 more digits |
| 12 | start end middle |
| 13 | this is the first line this is the second line |
| 14 | special characters !@#$%^&\*() |

**Output Code:**

##### Snowflake[¶](#id128 "Link to this heading")

```
 SELECT id, column_name
FROM posix_test_table
WHERE REGEXP_COUNT(column_name, '123$', 1, 'ms') = 0;
```

Copy

##### Results[¶](#id129 "Link to this heading")

| ID | COLUMN\_NAME |
| --- | --- |
| 2 | test string with multiple lines in this entry |
| 4 | line1 line2 line3 |
| 5 | start middle end |
| 6 | a@b#c! more text here |
| 7 | alpha beta gamma |
| 8 | uppercase lowercase |
| 9 | line1 line2 line3 line4 |
| 10 | 1234567890 more digits |
| 12 | start end middle |
| 13 | this is the first line this is the second line |
| 14 | special characters !@#$%^&\*() |

#### Usage of collate columns[¶](#usage-of-collate-columns "Link to this heading")

Arguments with COLLATE specifications are not currently supported in the RLIKE function. As a result, the COLLATE clause must be disabled to use this function. However, this may lead to differences in the results.

##### Input Code:[¶](#id130 "Link to this heading")

##### Redshift[¶](#id131 "Link to this heading")

```
 CREATE TABLE collateTable (
col1 VARCHAR(20) COLLATE CASE_INSENSITIVE,
col2 VARCHAR(30) COLLATE CASE_SENSITIVE);

INSERT INTO collateTable values ('HELLO WORLD!', 'HELLO WORLD!');

SELECT
col1 ~ 'Hello.*' as ci,
col2 ~ 'Hello.*' as cs
FROM collateTable;
```

Copy

##### Results[¶](#id132 "Link to this heading")

| CI | CS |
| --- | --- |
| TRUE | FALSE |

**Output Code:**

##### Snowflake[¶](#id133 "Link to this heading")

```
 CREATE TABLE collateTable (
col1 VARCHAR(20) COLLATE 'en-ci',
col2 VARCHAR(30) COLLATE 'en-cs'
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "01/16/2025",  "domain": "test" }}';

INSERT INTO collateTable
values ('HELLO WORLD!', 'HELLO WORLD!');

SELECT
REGEXP_COUNT(COLLATE(
--** SSC-FDM-PG0011 - THE USE OF THE COLLATE COLUMN CONSTRAINT HAS BEEN DISABLED FOR THIS PATTERN-MATCHING CONDITION. **
col1, ''), 'Hello.*', 1, 'ms') > 0 as ci,
REGEXP_COUNT(COLLATE(
--** SSC-FDM-PG0011 - THE USE OF THE COLLATE COLUMN CONSTRAINT HAS BEEN DISABLED FOR THIS PATTERN-MATCHING CONDITION. **
col2, ''), 'Hello.*', 1, 'ms') > 0 as cs
FROM
collateTable;
```

Copy

##### Results[¶](#id134 "Link to this heading")

| CI | CS |
| --- | --- |
| FALSE | FALSE |

If you require equivalence for these scenarios, you can manually add the following parameters to the function to achieve functional equivalence:

| Parameter | Description |
| --- | --- |
| `c` | Case-sensitive matching |
| `i` | Case-insensitive matching |

### Known Issues[¶](#id135 "Link to this heading")

### Known Issues[¶](#id136 "Link to this heading")

1. The behavior of fixed char types may differ. Click [here](#id12) for more information.
2. Arguments with COLLATE specifications are not currently supported in the REGEXP\_COUNT function.

### Related EWIs[¶](#id137 "Link to this heading")

* [SSC-FDM-PG0011](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/postgresqlFDM.html#ssc-fdm-pg0011): The use of the COLLATE column constraint has been disabled for this pattern-matching condition.

## SIMILAR TO[¶](#similar-to "Link to this heading")

Pattern-matching conditions

### Description [¶](#id138 "Link to this heading")

> The SIMILAR TO operator matches a string expression, such as a column name, with a SQL standard regular expression pattern. A SQL regular expression pattern can include a set of pattern-matching metacharacters, including the two supported by the [LIKE](https://docs.aws.amazon.com/redshift/latest/dg/r_patternmatching_condition_like.html) operator. ([Redshift SQL Language reference SIMILAR TO](https://docs.aws.amazon.com/redshift/latest/dg/pattern-matching-conditions-similar-to.html)).

Warning

This grammar is partially supported in [Snowflake](https://docs.snowflake.com/en/sql-reference/operators-logical). SIMILAR TO is transformed to [RLIKE](https://docs.snowflake.com/en/sql-reference/functions/rlike) in Snowflake.

### Grammar Syntax [¶](#id139 "Link to this heading")

```
 expression [ NOT ] SIMILAR TO pattern [ ESCAPE 'escape_char' ]
```

Copy

### Pattern-matching metacharacters[¶](#pattern-matching-metacharacters "Link to this heading")

| Redshift | Snowflake | Notes |
| --- | --- | --- |
| ```{code} sql :force: % ``` | ```{code} sql :force: .\* ``` | Matches any sequence of zero or more characters. To achieve full equivalence in Snowflake, we need to replace the '%' operator with '.\*' in the pattern. |
| ```{code} sql :force: \_ ``` | ```{code} sql :force: . ``` | Matches any single character. To achieve full equivalence in Snowflake, we need to replace the `_` operator with `.` and add the `s` parameter to enable the POSIX wildcard character `.` to match newline characters. |
| ```{code} sql :force: | ``` | ```{code} sql :force: | ``` | Denotes alternation. This case is fully supported in Snowflake. |
| ```{code} sql :force: \* ``` | ```{code} sql :force: \* ``` | Repeat the previous item zero or more times. This can have a different behavior when newline characters are included. |
| ```{code} sql :force: + ``` | ```{code} sql :force: + ``` | Repeat the previous item one or more times. This can have a different behavior when newline characters are included. |
| ```{code} sql :force: ? ``` | ```{code} sql :force: ? ``` | Repeat the previous item zero or one time. This can have a different behavior when newline characters are included. |
| ```{code} sql :force: {m} ``` | ```{code} sql :force: {m} ``` | Repeat the previous item exactly *m* times and it is fully supported in Snowflake. |
| ```{code} sql :force: {m,} ``` | ```{code} sql :force: {m,} ``` | Repeat the previous item at least *m* and not more than *n* times and it is fully supported in Snowflake. |
| ```{code} sql :force: {m,n} ``` | ```{code} sql :force: {m,n} ``` | Repeat the previous item *m* or more times and it is fully supported in Snowflake. |
| ```{code} sql :force: () ``` | ```{code} sql :force: () ``` | Parentheses group items into a single logical item and it is fully supported in Snowflake. |
| ```{code} sql :force: [...] ``` | ```{code} sql :force: [...] ``` | A bracket expression specifies a character class, just as in POSIX regular expressions. |

### Sample Source Patterns[¶](#id140 "Link to this heading")

#### **Setup data**[¶](#id141 "Link to this heading")

##### Redshift[¶](#id142 "Link to this heading")

```
 CREATE TABLE similar_table_ex (
    column_name VARCHAR(255)
);

INSERT INTO similar_table_ex (column_name)
VALUES
    ('abc_123'),
    ('a_cdef'),
    ('bxyz'),
    ('abcc'),
    ('start_hello'),
    ('apple'),
    ('banana'),
    ('xyzabc'),
    ('abc\ncccc'),
    ('\nabccc'),
    ('abc%def'),
    ('abc_xyz'),
    ('abc_1_xyz'),
    ('applepie'),
    ('start%_abc'),
    ('ab%_xyz'),
    ('abcs_123_xyz'),
    ('aabc123'),
    ('xyzxyz'),
    ('123abc\nanother line\nabc123');
```

Copy

#### % : Matches any sequence of zero or more characters[¶](#matches-any-sequence-of-zero-or-more-characters "Link to this heading")

##### Input Code:[¶](#id143 "Link to this heading")

##### Redshift[¶](#id144 "Link to this heading")

```
 SELECT column_name
FROM similar_table_ex
WHERE column_name SIMILAR TO '%abc%';
```

Copy

##### Results[¶](#id145 "Link to this heading")

| COLUMN\_NAME |
| --- |
| abc\_123 |
| abcc |
| xyzabc |
| abc cccc |
| abc%def |
| abc\_xyz |
| abc\_1\_xyz |
| start%\_abc |
| abcs\_123\_xyz |
| aabc123 |

**Output Code:**

##### Snowflake[¶](#id146 "Link to this heading")

```
 SELECT column_name
FROM similar_table_ex
WHERE RLIKE (column_name, '.*abc.*', 's');
```

Copy

##### Results[¶](#id147 "Link to this heading")

| COLUMN\_NAME |
| --- |
| abc\_123 |
| abcc |
| xyzabc |
| abc cccc |
| abc%def |
| abc\_xyz |
| abc\_1\_xyz |
| start%\_abc |
| abcs\_123\_xyz |
| aabc123 |

#### \_ : Matches any single character[¶](#matches-any-single-character "Link to this heading")

##### Input Code:[¶](#id148 "Link to this heading")

##### Redshift[¶](#id149 "Link to this heading")

```
 SELECT column_name
FROM similar_table_ex
WHERE column_name SIMILAR TO 'a_c%';
```

Copy

##### Results[¶](#id150 "Link to this heading")

| COLUMN\_NAME |
| --- |
| abc\_123 |
| a\_cdef |
| abcc |
| abc cccc |
| abc%def |
| abc\_xyz |
| abc\_1\_xyz |
| abcs\_123\_xyz |

**Output Code:**

##### Snowflake[¶](#id151 "Link to this heading")

```
 SELECT column_name
FROM similar_table_ex
WHERE RLIKE (column_name, 'a.c.*', 's');
```

Copy

##### Results[¶](#id152 "Link to this heading")

| COLUMN\_NAME |
| --- |
| abc\_123 |
| a\_cdef |
| abcc |
| abc cccc |
| abc%def |
| abc\_xyz |
| abc\_1\_xyz |
| abcs\_123\_xyz |

#### | : Denotes alternation[¶](#denotes-alternation "Link to this heading")

##### Input Code:[¶](#id153 "Link to this heading")

##### Redshift[¶](#id154 "Link to this heading")

```
 SELECT column_name
FROM similar_table_ex
WHERE column_name SIMILAR TO 'a|b%';
```

Copy

##### Results[¶](#id155 "Link to this heading")

| COLUMN\_NAME |
| --- |
| bxyz |
| banana |

**Output Code:**

##### Snowflake[¶](#id156 "Link to this heading")

```
 SELECT column_name
FROM similar_table_ex
WHERE RLIKE (column_name, 'a|b.*', 's');
```

Copy

##### Results[¶](#id157 "Link to this heading")

| COLUMN\_NAME |
| --- |
| bxyz |
| banana |

#### {m, n} : Repeat the previous item exactly *m* times.[¶](#m-n-repeat-the-previous-item-exactly-m-times "Link to this heading")

##### Input Code:[¶](#id158 "Link to this heading")

##### Redshift[¶](#id159 "Link to this heading")

```
 SELECT column_name
FROM similar_table_ex
WHERE column_name SIMILAR TO 'abc{2,4}';
```

Copy

##### Results[¶](#id160 "Link to this heading")

| COLUMN\_NAME |
| --- |
| abcc |

**Output Code:**

##### Snowflake[¶](#id161 "Link to this heading")

```
 SELECT column_name
FROM similar_table_ex
WHERE RLIKE (column_name, 'abc{2,4}', 's');
```

Copy

##### Results[¶](#id162 "Link to this heading")

| COLUMN\_NAME |
| --- |
| abcc |

#### + : Repeat the previous item one or more times[¶](#repeat-the-previous-item-one-or-more-times "Link to this heading")

##### Input Code:[¶](#id163 "Link to this heading")

##### Redshift[¶](#id164 "Link to this heading")

```
 SELECT column_name
FROM similar_table_ex
WHERE column_name SIMILAR TO 'abc+';
```

Copy

##### Results[¶](#id165 "Link to this heading")

| COLUMN\_NAME |
| --- |
| abcc |
| abc cccc |

**Output Code:**

##### Snowflake[¶](#id166 "Link to this heading")

```
 SELECT column_name
FROM similar_table_ex
WHERE RLIKE (column_name, 'abc+', 's');
```

Copy

##### Results[¶](#id167 "Link to this heading")

| COLUMN\_NAME |
| --- |
| abcc |

#### \* : Repeat the previous item zero or more times[¶](#repeat-the-previous-item-zero-or-more-times "Link to this heading")

##### Input Code:[¶](#id168 "Link to this heading")

##### Redshift[¶](#id169 "Link to this heading")

```
 SELECT column_name
FROM similar_table_ex
WHERE column_name SIMILAR TO 'abc*c';
```

Copy

##### Results[¶](#id170 "Link to this heading")

| COLUMN\_NAME |
| --- |
| abcc |
| abc cccc |

**Output Code:**

##### Snowflake[¶](#id171 "Link to this heading")

```
 SELECT column_name
FROM similar_table_ex
WHERE RLIKE (column_name, 'abc*c', 's');
```

Copy

##### Results[¶](#id172 "Link to this heading")

| COLUMN\_NAME |
| --- |
| abcc |

#### ? : Repeat the previous item zero or one time[¶](#repeat-the-previous-item-zero-or-one-time "Link to this heading")

##### Input Code:[¶](#id173 "Link to this heading")

##### Redshift[¶](#id174 "Link to this heading")

```
 SELECT column_name
FROM similar_table_ex
WHERE column_name SIMILAR TO 'abc?c';
```

Copy

##### Results[¶](#id175 "Link to this heading")

| COLUMN\_NAME |
| --- |
| abcc |
| abc ccc |

**Output Code:**

##### Snowflake[¶](#id176 "Link to this heading")

```
 SELECT column_name
FROM
similar_table_ex
WHERE
RLIKE( column_name, 'abc?c', 's');
```

Copy

##### Results[¶](#id177 "Link to this heading")

| COLUMN\_NAME |
| --- |
| abcc |

#### () : Parentheses group items into a single logical item[¶](#parentheses-group-items-into-a-single-logical-item "Link to this heading")

##### Input Code:[¶](#id178 "Link to this heading")

##### Redshift[¶](#id179 "Link to this heading")

```
 SELECT column_name
FROM similar_table_ex
WHERE column_name SIMILAR TO '(abc|xyz)%';
```

Copy

##### Results[¶](#id180 "Link to this heading")

| COLUMN\_NAME |
| --- |
| abc\_123 |
| abcc |
| xyzabc |
| abc cccc |
| abc%def |
| abc\_xyz |
| abc\_1\_xyz |
| abcs\_123\_xyz |
| xyzxyz |

**Output Code:**

##### Snowflake[¶](#id181 "Link to this heading")

```
 SELECT column_name
FROM similar_table_ex
WHERE RLIKE (column_name, '(abc|xyz).*', 's');
```

Copy

##### Results[¶](#id182 "Link to this heading")

| COLUMN\_NAME |
| --- |
| abc\_123 |
| abcc |
| xyzabc |
| abc cccc |
| abc%def |
| abc\_xyz |
| abc\_1\_xyz |
| abcs\_123\_xyz |
| xyzxyz |

#### […] : Specifies a character class[¶](#specifies-a-character-class "Link to this heading")

##### Input Code:[¶](#id183 "Link to this heading")

##### Redshift[¶](#id184 "Link to this heading")

```
 SELECT column_name
FROM similar_table_ex
WHERE column_name SIMILAR TO '[a-c]%';
```

Copy

##### Results[¶](#id185 "Link to this heading")

| COLUMN\_NAME |
| --- |
| abc\_123 |
| a\_cdef |
| bxyz |
| abcc |
| apple |
| banana |
| abc cccc |
| abc%def |
| abc\_xyz |
| abc\_1\_xyz |
| applepie |
| ab%\_xyz |
| abcs\_123\_xyz |
| aabc123 |

**Output Code:**

##### Snowflake[¶](#id186 "Link to this heading")

```
 SELECT column_name
FROM similar_table_ex
WHERE RLIKE (column_name, '[a-c].*', 's');
```

Copy

##### Results[¶](#id187 "Link to this heading")

| COLUMN\_NAME |
| --- |
| abc\_123 |
| a\_cdef |
| bxyz |
| abcc |
| apple |
| banana |
| abc cccc |
| abc%def |
| abc\_xyz |
| abc\_1\_xyz |
| applepie |
| ab%\_xyz |
| abcs\_123\_xyz |
| aabc123 |

#### Escape characters[¶](#id188 "Link to this heading")

The following characters will be escaped if they appear in the pattern and are not the escape character itself:

* .
* $
* ^

##### Input Code:[¶](#id189 "Link to this heading")

##### Redshift[¶](#id190 "Link to this heading")

```
 SELECT column_name
FROM similar_table_ex
WHERE column_name SIMILAR TO '%abc^_%' ESCAPE '^';

SELECT '$0.87' SIMILAR TO '$[0-9]+(.[0-9][0-9])?' r1;
```

Copy

##### Results[¶](#id191 "Link to this heading")

| COLUMN\_NAME |
| --- |
| abc\_123 |
| abc\_xyz |
| abc\_1\_xyz |

| R1 |
| --- |
| TRUE |

**Output Code:**

##### Snowflake[¶](#id192 "Link to this heading")

```
 SELECT column_name
FROM
similar_table_ex
WHERE
RLIKE( column_name, '.*abc\\_.*', 's');

SELECT
RLIKE( '$0.87', '\\$[0-9]+(\\.[0-9][0-9])?', 's') r1;
```

Copy

##### Results[¶](#id193 "Link to this heading")

| COLUMN\_NAME |
| --- |
| abc\_123 |
| abc\_xyz |
| abc\_1\_xyz |

| R1 |
| --- |
| TRUE |

#### Pattern stored in a variable[¶](#pattern-stored-in-a-variable "Link to this heading")

If these patterns are stored in a variable, the required adjustments for equivalence will not be applied. You can refer to the recommendations outlined in the [table](#pattern-matching-metacharacters) at the beginning of this document for additional equivalence guidelines.

##### Input Code:[¶](#id194 "Link to this heading")

##### Redshift[¶](#id195 "Link to this heading")

```
 WITH pattern AS (
    SELECT '%abc%'::VARCHAR AS search_pattern
)
SELECT column_name
FROM similar_table_ex, pattern
WHERE column_name SIMILAR TO pattern.search_pattern;
```

Copy

##### Results[¶](#id196 "Link to this heading")

| COLUMN\_NAME |
| --- |
| abc\_123 |
| abcc |
| xyzabc |
| abc cccc |
| abccc |
| abc%def |
| abc\_xyz |
| abc\_1\_xyz |
| start%\_abc |
| abcs\_123\_xyz |
| aabc123 |
| 123abc another line abc123 |

**Output Code:**

##### Snowflake[¶](#id197 "Link to this heading")

```
 WITH pattern AS (
    SELECT '%abc%'::VARCHAR AS search_pattern
)
SELECT column_name
FROM
similar_table_ex,
pattern
WHERE
RLIKE( column_name,
                    --** SSC-FDM-0032 - PARAMETER 'search_pattern' IS NOT A LITERAL VALUE, TRANSFORMATION COULD NOT BE FULLY APPLIED **
                    pattern.search_pattern, 's');
```

Copy

##### Results[¶](#id198 "Link to this heading")

| COLUMN\_NAME |
| --- |
| Query produced no results |

#### Usage of collate columns[¶](#id199 "Link to this heading")

Arguments with COLLATE specifications are not currently supported in the RLIKE function. As a result, the COLLATE clause must be disabled to use this function. However, this may lead to differences in the results.

##### Input Code:[¶](#id200 "Link to this heading")

##### Redshift[¶](#id201 "Link to this heading")

```
 CREATE TABLE collateTable (
col1 VARCHAR(20) COLLATE CASE_INSENSITIVE,
col2 VARCHAR(30) COLLATE CASE_SENSITIVE);

INSERT INTO collateTable values ('HELLO WORLD!', 'HELLO WORLD!');

SELECT
col1 SIMILAR TO 'Hello%' as ci,
col2 SIMILAR TO 'Hello%' as cs
FROM collateTable;
```

Copy

##### Results[¶](#id202 "Link to this heading")

| CI | CS |
| --- | --- |
| TRUE | FALSE |

**Output Code:**

##### Snowflake[¶](#id203 "Link to this heading")

```
 CREATE TABLE collateTable (
col1 VARCHAR(20) COLLATE 'en-ci',
col2 VARCHAR(30) COLLATE 'en-cs'
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "01/16/2025",  "domain": "test" }}';

INSERT INTO collateTable
values ('HELLO WORLD!', 'HELLO WORLD!');

SELECT
RLIKE(COLLATE(
--** SSC-FDM-PG0011 - THE USE OF THE COLLATE COLUMN CONSTRAINT HAS BEEN DISABLED FOR THIS PATTERN-MATCHING CONDITION. **
col1, ''), 'Hello.*', 's') as ci,
RLIKE(COLLATE(
--** SSC-FDM-PG0011 - THE USE OF THE COLLATE COLUMN CONSTRAINT HAS BEEN DISABLED FOR THIS PATTERN-MATCHING CONDITION. **
col2, ''), 'Hello.*', 's') as cs
FROM
collateTable;
```

Copy

##### Results[¶](#id204 "Link to this heading")

| CI | CS |
| --- | --- |
| FALSE | FALSE |

If you require equivalence for these scenarios, you can manually add the following parameters to the function to achieve functional equivalence:

| Parameter | Description |
| --- | --- |
| `c` | Case-sensitive matching |
| `i` | Case-insensitive matching |

### Known Issues[¶](#id205 "Link to this heading")

1. The behavior of fixed char types may differ.
2. The `RLIKE` function uses POSIX extended regular expressions, which may result in different behavior in certain cases, especially when line breaks are involved. It appears that when line breaks are present in the string and a match occurs on one line, it returns a positive result for the entire string, even though the match only occurred on a single line and not across the whole string. For example:

#### Redshift code[¶](#redshift-code "Link to this heading")

```
 CREATE TABLE table1 (
col1 VARCHAR(20)
);

INSERT INTO table1 values ('abcccc'), ('abc\neab'), ('abc\nccc');

SELECT col1
FROM table1
WHERE col1 SIMILAR TO 'abc*c';
```

Copy

##### Snowflake code[¶](#snowflake-code "Link to this heading")

```
 CREATE TABLE table1 (
col1 VARCHAR(20)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "01/14/2025",  "domain": "test" }}';

INSERT INTO table1
values ('abcccc'), ('abc\neab'), ('abc\nccc');

SELECT col1
FROM
table1
WHERE
RLIKE( col1, 'abc*c', 's');
```

Copy

##### Redshift Results[¶](#id206 "Link to this heading")

| COL1 |
| --- |
| abcccc |
| abc eab |
| abc ccc |

##### Snowflake Results[¶](#id207 "Link to this heading")

| COL1 |
| --- |
| abcccc |

1. To achieve maximum equivalence, some modifications are made to the pattern operators.
2. If these patterns are stored in a variable, SnowConvert AI does not apply the necessary adjustments for equivalence.
3. Arguments with COLLATE specifications are not currently supported in the RLIKE function.

### Related EWIs[¶](#id208 "Link to this heading")

* [SSC-FDM-0032](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0032): Parameter is not a literal value, transformation could not be fully applied.
* [SSC-FDM-PG0011](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/postgresqlFDM.html#ssc-fdm-pg0011): The use of the COLLATE column constraint has been disabled for this pattern-matching condition.

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
2. [Comparison Condition](#comparison-condition)
3. [EXISTS](#exists)
4. [IN](#in)
5. [Logical Conditions](#logical-conditions)
6. [NULL](#null)
7. [Pattern-matching conditions](#pattern-matching-conditions)
8. [LIKE](#like)
9. [POSIX Operators](#posix-operators)
10. [SIMILAR TO](#similar-to)