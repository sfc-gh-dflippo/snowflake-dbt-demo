---
auto_generated: true
description: 'The Teradata database has different modes for running queries: ANSI
  Mode (rules based on the ANSI SQL: 2011 specifications) and TERA mode (rules defined
  by Teradata). Please review the following Terad'
last_scraped: '2026-01-14T16:53:50.050656+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/teradata/session-modes
title: SnowConvert AI - Teradata - Session Modes in Teradata | Snowflake Documentation
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
          + [Teradata](README.md)

            - [Data Migration Considerations](data-migration-considerations.md)
            - [Session Modes in Teradata](session-modes.md)
            - [Sql Translation Reference](sql-translation-reference/README.md)
            - [SQL to JavaScript (Procedures)](teradata-to-javascript-translation-reference.md)")
            - [SQL to Snowflake Scripting (Procedures)](teradata-to-snowflake-scripting-translation-reference.md)")
            - [Scripts To Python](scripts-to-python/README.md)
            - [Scripts to Snowflake SQL](scripts-to-snowflake-sql-translation-reference/README.md)
            - ETL And BI Repointing

              - [Power BI Teradata Repointing](etl-bi-repointing/power-bi-teradata-repointing.md)
          + [Oracle](../oracle/README.md)
          + [SQL Server-Azure Synapse](../transact/README.md)
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)Translation References[Teradata](README.md)Session Modes in Teradata

# SnowConvert AI - Teradata - Session Modes in Teradata[¶](#snowconvert-ai-teradata-session-modes-in-teradata "Link to this heading")

## Teradata session modes description[¶](#teradata-session-modes-description "Link to this heading")

The Teradata database has different modes for running queries: ANSI Mode (rules based on the ANSI SQL: 2011 specifications) and TERA mode (rules defined by Teradata). Please review the following [Teradata documentation](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/SQL-Request-and-Transaction-Processing/Transaction-Processing/Transaction-Semantics-Differences-in-ANSI-and-Teradata-Session-Modes) for more information.

### Teradata mode for strings informative table[¶](#teradata-mode-for-strings-informative-table "Link to this heading")

For strings, the Teradata Mode works differently. As it is explained in the following table based on the [Teradata documentation](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/SQL-Request-and-Transaction-Processing/Transaction-Processing/Comparison-of-Transactions-in-ANSI-and-Teradata-Session-Modes):

| Feature | ANSI mode | Teradata mode |
| --- | --- | --- |
| Default attribute for character comparisons | CASESPECIFIC | NOT CASESPECIFIC |
| Default TRIM behavior | TRIM(BOTH FROM) | TRIM(BOTH FROM) |

#### Translation specification summary[¶](#translation-specification-summary "Link to this heading")

| Mode | Column constraint values | Teradata behavior | SC expected behavior |
| --- | --- | --- | --- |
| ANSI Mode | CASESPECIFIC | CASESPECIFIC | No constraint added. |
|  | NOT CASESPECIFIC | CASESPECIFIC | Add `COLLATE 'en-cs'` in column definition. |
| Teradata Mode | CASESPECIFIC | CASESPECIFIC | In most cases, do not add COLLATE, and convert its usages of string comparison to `RTRIM( expression )` |
|  | NOT CASESPECIFIC | NOT CASESPECIFIC | In most cases, do not add COLLATE, and convert its usages of string comparison to `RTRIM(UPPER( expression ))` |

### Available translation specification options[¶](#available-translation-specification-options "Link to this heading")

* [TERA Mode For Strings Comparison - NO COLLATE](#tera-mode-for-string-comparison-and-no-collate-usages)
* [TERA Mode For Strings Comparison - COLLATE](#tera-mode-for-string-comparison-and-collate-usage)
* [ANSI Mode For Strings Comparison - NO COLLATE](#ansi-mode-for-string-comparison-and-no-colate-usages)
* [ANSI Mode For Strings Comparison - COLLATE](#ansi-mode-for-string-comparison-and-collate-usage)

## ANSI Mode For Strings Comparison - COLLATE[¶](#ansi-mode-for-strings-comparison-collate "Link to this heading")

This section defines the translation specification for a string in ANSI mode with the use of COLLATE.

### Description [¶](#description "Link to this heading")

#### ANSI mode for string comparison and COLLATE usage[¶](#ansi-mode-for-string-comparison-and-collate-usage "Link to this heading")

The ANSI mode string comparison will apply the COLLATE constraint to the columns or statements as required. The default case specification trim behavior may be taken into account.

Notice that in Teradata, the default case specification is ‘`CASESPECIFIC`’, the same default as in Snowflake ‘`case-sensitive'`. Thus, these cases will not be translated with a `COLLATE` because it will be redundant.

### Sample Source Patterns [¶](#sample-source-patterns "Link to this heading")

#### Setup data[¶](#setup-data "Link to this heading")

##### Teradata[¶](#teradata "Link to this heading")

```
 CREATE TABLE employees (
    employee_id INTEGER NOT NULL,
    first_name VARCHAR(50) NOT CASESPECIFIC,
    last_name VARCHAR(50) CASESPECIFIC,
    department VARCHAR(50)
);

INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (1, 'George', 'Snow', 'Sales');
INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (2, 'John', 'SNOW', 'Engineering');
INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (3, 'WIlle', 'SNOW', 'Human resources   ');
INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (4, 'Marco', 'SnoW   ', 'EngineerinG');
INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (5, 'Mary', '   ', 'SaleS  ');
INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (6, 'GEORGE', '  ', 'sales  ');
INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (7, 'GEORGE   ', '  ', 'salEs  ');
INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (8, '    GeorgE   ', '  ', 'SalEs  ');
INSERT INTO employees (employee_id, first_name, last_name, department) VALUES (9, 'JOHN', '   SnoW', 'IT');
INSERT INTO employees (employee_id, first_name, last_name, department) VALUES (10, 'JOHN    ', 'snow', 'Finance   ');

CREATE TABLE departments (
    department_id INTEGER NOT NULL,
    department_name VARCHAR(50) NOT CASESPECIFIC,
    location VARCHAR(100) CASESPECIFIC,
    PRIMARY KEY (department_id)
);


INSERT INTO departments (department_id, department_name, location) VALUES (101, 'Information Technology', 'New York');
INSERT INTO departments (department_id, department_name, location) VALUES (102, 'Human Resources', 'Chicago');
INSERT INTO departments (department_id, department_name, location) VALUES (103, 'Sales', 'San Francisco');
INSERT INTO departments (department_id, department_name, location) VALUES (104, 'Finance', 'Boston');
```

Copy

##### Snowflake[¶](#snowflake "Link to this heading")

```
 CREATE OR REPLACE TABLE employees (
    employee_id INTEGER NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    department VARCHAR(50)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/02/2025",  "domain": "no-domain-provided" }}'
;

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (1, 'George', 'Snow', 'Sales');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (2, 'John', 'SNOW', 'Engineering');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (3, 'WIlle', 'SNOW', 'Human resources   ');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (4, 'Marco', 'SnoW   ', 'EngineerinG');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (5, 'Mary', '   ', 'SaleS  ');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (6, 'GEORGE', '  ', 'sales  ');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (7, 'GEORGE   ', '  ', 'salEs  ');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (8, '    GeorgE   ', '  ', 'SalEs  ');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (9, 'JOHN', '   SnoW', 'IT');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (10, 'JOHN    ', 'snow', 'Finance   ');

CREATE OR REPLACE TABLE departments (
    department_id INTEGER NOT NULL,
    department_name VARCHAR(50),
    location VARCHAR(100),
       PRIMARY KEY (department_id)
   )
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/02/2025",  "domain": "no-domain-provided" }}'
;

INSERT INTO departments (department_id, department_name, location)
VALUES (101, 'Information Technology', 'New York');

INSERT INTO departments (department_id, department_name, location)
VALUES (102, 'Human Resources', 'Chicago');

INSERT INTO departments (department_id, department_name, location)
VALUES (103, 'Sales', 'San Francisco');

INSERT INTO departments (department_id, department_name, location)
VALUES (104, 'Finance', 'Boston');
```

Copy

#### Comparison operation[¶](#comparison-operation "Link to this heading")

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is ANSI Mode[¶](#case-1-column-constraint-is-not-casespecific-and-database-mode-is-ansi-mode "Link to this heading")

##### Teradata[¶](#id1 "Link to this heading")

##### Query[¶](#query "Link to this heading")

```
 SELECT *
FROM employees
WHERE first_name = 'GEorge ';
```

Copy

##### Output[¶](#output "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 1 | George | Snow | Sales |

##### Snowflake[¶](#id2 "Link to this heading")

##### Query[¶](#id3 "Link to this heading")

```
 SELECT
    *
FROM
    employees
WHERE
    COLLATE(first_name, 'en-cs-rtrim') = RTRIM('George');
```

Copy

##### Output[¶](#id4 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 1 | George | Snow | Sales |

##### Case 2: Column constraint is CASESPECIFIC and database mode is ANSI Mode[¶](#case-2-column-constraint-is-casespecific-and-database-mode-is-ansi-mode "Link to this heading")

##### Teradata[¶](#id5 "Link to this heading")

##### Query[¶](#id6 "Link to this heading")

```
 SELECT *
FROM employees
WHERE last_name = 'SNOW ';
```

Copy

##### Output[¶](#id7 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 3 | WIlle | SNOW | Human resources |
| 2 | John | SNOW | Engineering |

##### Snowflake[¶](#id8 "Link to this heading")

##### Query[¶](#id9 "Link to this heading")

```
SELECT
 *
FROM
 employees
WHERE
 RTRIM(last_name) = RTRIM('SNOW ');
```

Copy

##### Output[¶](#id10 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 3 | WIlle | SNOW | Human resources |
| 2 | John | SNOW | Engineering |

##### Case 3: CAST NOT CASESPECIFIC column to CASESPECIFIC and database mode is ANSI Mode[¶](#case-3-cast-not-casespecific-column-to-casespecific-and-database-mode-is-ansi-mode "Link to this heading")

##### Teradata[¶](#id11 "Link to this heading")

##### Query[¶](#id12 "Link to this heading")

```
 SELECT * FROM employees WHERE first_name = 'George   ' (CASESPECIFIC);
```

Copy

##### Output[¶](#id13 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 1 | George | Snow | Sales |

##### Snowflake[¶](#id14 "Link to this heading")

Note

COLLATE ‘en-cs’ is required for functional equivalence.

##### Query[¶](#id15 "Link to this heading")

```
 SELECT
    *
FROM
    employees
WHERE
    COLLATE(first_name, 'en-cs-rtrim') = 'George   ' /*** SSC-FDM-TD0032 - CASESPECIFIC CLAUSE WAS REMOVED ***/;
```

Copy

##### Output[¶](#id16 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 1 | George | Snow | Sales |

##### Case 4: CAST CASESPECIFIC column to NOT CASESPECIFIC and database mode is ANSI Mode[¶](#case-4-cast-casespecific-column-to-not-casespecific-and-database-mode-is-ansi-mode "Link to this heading")

##### Teradata[¶](#id17 "Link to this heading")

##### Query[¶](#id18 "Link to this heading")

```
 SELECT * FROM employees WHERE first_name = 'GEorge   ' (NOT CASESPECIFIC) ;
```

Copy

##### Output[¶](#id19 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 1 | George | Snow | Sales |
| 6 | GEORGE |  | sales |
| 7 | GEORGE |  | salEs |

##### Snowflake[¶](#id20 "Link to this heading")

##### Query[¶](#id21 "Link to this heading")

```
 SELECT
   *
FROM
   employees
WHERE
   RTRIM(first_name) = RTRIM('GEorge   ' /*** SSC-FDM-TD0032 - NOT CASESPECIFIC CLAUSE WAS REMOVED ***/);
```

Copy

##### Output[¶](#id22 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 1 | George | Snow | Sales |
| 6 | GEORGE |  | sales |
| 7 | GEORGE |  | salEs |

##### Case 5: CAST NOT CASESPECIFIC column to NOT CASESPECIFIC and database mode is ANSI Mode[¶](#case-5-cast-not-casespecific-column-to-not-casespecific-and-database-mode-is-ansi-mode "Link to this heading")

##### Teradata[¶](#id23 "Link to this heading")

##### Query[¶](#id24 "Link to this heading")

```
 SELECT * FROM employees WHERE first_name (NOT CASESPECIFIC)  = 'George    ';
```

Copy

##### Output[¶](#id25 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 1 | George | Snow | Sales |

##### Snowflake[¶](#id26 "Link to this heading")

Note

It requires COLLATE.

##### Query[¶](#id27 "Link to this heading")

```
 SELECT
   * 
FROM
   employees
WHERE
   COLLATE(first_name /*** SSC-FDM-TD0032 - NOT CASESPECIFIC CLAUSE WAS REMOVED ***/, 'en-cs-rtrim') = 'George    ';
```

Copy

##### Output[¶](#id28 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 1 | George | Snow | Sales |

#### LIKE operation[¶](#like-operation "Link to this heading")

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is ANSI Mode[¶](#id29 "Link to this heading")

##### Teradata[¶](#id30 "Link to this heading")

##### Query[¶](#id31 "Link to this heading")

```
 SELECT *
FROM employees
WHERE first_name LIKE 'George';
```

Copy

##### Output[¶](#id32 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 1 | George | Snow | Sales |

##### Snowflake[¶](#id33 "Link to this heading")

##### Query[¶](#id34 "Link to this heading")

```
 SELECT *
FROM employees
WHERE COLLATE(first_name, 'en-cs-rtrim') LIKE 'George';
```

Copy

##### Output[¶](#id35 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 1 | George | Snow | Sales |

##### Case 2: Column constraint is CASESPECIFIC and database mode is ANSI Mode[¶](#id36 "Link to this heading")

##### Teradata[¶](#id37 "Link to this heading")

##### Query[¶](#id38 "Link to this heading")

```
 SELECT *
FROM employees
WHERE last_name LIKE 'Snow';
```

Copy

##### Output[¶](#id39 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 2 | John | SNOW | Engineering |
| 3 | WIlle | SNOW | Human resources |

##### Snowflake[¶](#id40 "Link to this heading")

##### Query[¶](#id41 "Link to this heading")

```
 SELECT *
FROM employees
WHERE RTRIM(last_name) LIKE RTRIM('Snow');
```

Copy

##### Output[¶](#id42 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 2 | John | SNOW | Engineering |
| 3 | WIlle | SNOW | Human resources |

##### Case 3: CAST NOT CASESPECIFIC column to CASESPECIFIC and database mode is ANSI Mode[¶](#id43 "Link to this heading")

##### Teradata[¶](#id44 "Link to this heading")

##### Query[¶](#id45 "Link to this heading")

```
 SELECT *
FROM employees
WHERE first_name LIKE 'Mary' (CASESPECIFIC);
```

Copy

##### Output[¶](#id46 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 5 | Mary |  | SaleS |

##### Snowflake[¶](#id47 "Link to this heading")

##### Query[¶](#id48 "Link to this heading")

```
 SELECT
   *
FROM
   employees
WHERE
   COLLATE(first_name, 'en-cs-rtrim') LIKE 'Mary' /*** SSC-FDM-TD0032 - CASESPECIFIC CLAUSE WAS REMOVED ***/;
```

Copy

##### Output[¶](#id49 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 5 | Mary |  | SaleS |

##### Case 4: CAST CASESPECIFC column to NOT CASESPECIFIC and database mode is ANSI Mode[¶](#case-4-cast-casespecifc-column-to-not-casespecific-and-database-mode-is-ansi-mode "Link to this heading")

##### Teradata[¶](#id50 "Link to this heading")

##### Query[¶](#id51 "Link to this heading")

```
 SELECT *
FROM employees
WHERE last_name LIKE 'SNO%' (NOT CASESPECIFIC);
```

Copy

##### Output[¶](#id52 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 2 | John | SNOW | Engineering |
| 3 | WIlle | SNOW | Human resources |

##### Snowflake[¶](#id53 "Link to this heading")

##### Query[¶](#id54 "Link to this heading")

```
 SELECT
   *
FROM
   employees
WHERE
   RTRIM(last_name) LIKE RTRIM('SNO%' /*** SSC-FDM-TD0032 - NOT CASESPECIFIC CLAUSE WAS REMOVED ***/);
```

Copy

##### Output[¶](#id55 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 2 | John | SNOW | Engineering |
| 3 | WIlle | SNOW | Human resources |

#### IN Operation[¶](#in-operation "Link to this heading")

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is ANSI Mode[¶](#id56 "Link to this heading")

##### Teradata[¶](#id57 "Link to this heading")

##### Query[¶](#id58 "Link to this heading")

```
 SELECT *
FROM employees
WHERE first_name IN ('George   ');
```

Copy

##### Output[¶](#id59 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 1 | George | Snow | Sales |

##### Snowflake[¶](#id60 "Link to this heading")

Note

This case requires `COLLATE(`*`column_name`*`, 'en-cs-rtrim')`

##### Query[¶](#id61 "Link to this heading")

```
 SELECT
   *
FROM
   employees
WHERE
   RTRIM(first_name) IN (COLLATE('George   ', 'en-cs-rtrim'));
```

Copy

##### Output[¶](#id62 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 1 | George | Snow | Sales |

##### Case 2: Column constraint is CASESPECIFIC and database mode is ANSI Mode[¶](#id63 "Link to this heading")

##### Teradata[¶](#id64 "Link to this heading")

Note

For this case, the column does not have a column constraint, but the default constraint in Teradata ANSI mode is `CASESPECIFIC`.

##### Query[¶](#id65 "Link to this heading")

```
 SELECT *
FROM employees
WHERE department IN ('EngineerinG    ');
```

Copy

##### Output[¶](#id66 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 4 | Marco | SnoW | EngineerinG |

##### Snowflake[¶](#id67 "Link to this heading")

##### Query[¶](#id68 "Link to this heading")

```
 SELECT
   *
FROM
   employees
WHERE
   RTRIM(department) IN (RTRIM('EngineerinG    '));
```

Copy

##### Output[¶](#id69 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 4 | Marco | SnoW | EngineerinG |

#### ORDER BY clause[¶](#order-by-clause "Link to this heading")

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is ANSI Mode[¶](#id70 "Link to this heading")

##### Teradata[¶](#id71 "Link to this heading")

##### Query[¶](#id72 "Link to this heading")

```
 SELECT first_name
FROM employees
ORDER BY first_name;
```

Copy

##### Output[¶](#id73 "Link to this heading")

| first\_name |
| --- |
| GeorgE |
| GEORGE |
| GEORGE |
| **George** |
| John |
| JOHN |
| JOHN |
| Marco |
| Mary |
| WIlle |

##### Snowflake[¶](#id74 "Link to this heading")

Warning

Please review FDM. ***Pending to add.***

##### Query[¶](#id75 "Link to this heading")

```
 SELECT
   first_name
FROM
   employees
ORDER BY first_name;
```

Copy

##### Output[¶](#id76 "Link to this heading")

| first\_name |
| --- |
| GeorgE |
| **George** |
| GEORGE |
| GEORGE |
| John |
| JOHN |
| JOHN |
| Marco |
| Mary |
| WIlle |

##### Case 2: Column constraint is CASESPECIFIC and database mode is ANSI Mode[¶](#id77 "Link to this heading")

##### Teradata[¶](#id78 "Link to this heading")

##### Query[¶](#id79 "Link to this heading")

```
 SELECT last_name
FROM employees
ORDER BY last_name;
```

Copy

##### Output[¶](#id80 "Link to this heading")

| department |
| --- |
| EngineerinG |
| Engineering |
| Finance |
| Human resources |
| IT |
| SalEs |
| SaleS |
| Sales |
| salEs |
| sales |

##### Snowflake[¶](#id81 "Link to this heading")

##### Query[¶](#id82 "Link to this heading")

```
 SELECT
   last_name
FROM
   employees
ORDER BY last_name;
```

Copy

##### Output[¶](#id83 "Link to this heading")

| department |
| --- |
| EngineerinG |
| Engineering |
| Finance |
| Human resources |
| IT |
| SalEs |
| SaleS |
| Sales |
| salEs |
| sales |

#### GROUP BY clause[¶](#group-by-clause "Link to this heading")

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is ANSI Mode[¶](#id84 "Link to this heading")

##### Teradata[¶](#id85 "Link to this heading")

##### Query[¶](#id86 "Link to this heading")

```
 SELECT first_name
FROM employees
GROUP BY first_name;
```

Copy

##### Output[¶](#id87 "Link to this heading")

| first\_name |
| --- |
| Mary |
| GeorgE |
| WIlle |
| **JOHN** |
| Marco |
| GEORGE |

##### Snowflake[¶](#id88 "Link to this heading")

Warning

**The case or order may differ in output.**

Note

`RTRIM` is required in selected columns.

##### Query[¶](#id89 "Link to this heading")

```
   SELECT
   first_name
  FROM
   employees
  GROUP BY first_name;
```

Copy

##### Output[¶](#id90 "Link to this heading")

| first\_name |
| --- |
| **John** |
| Marco |
| **George** |
| GeorgE |
| WIlle |
| Mary |

##### Case 2: Column constraint is CASESPECIFIC and database mode is ANSI Mode[¶](#id91 "Link to this heading")

##### Teradata[¶](#id92 "Link to this heading")

##### Query[¶](#id93 "Link to this heading")

```
 SELECT last_name
FROM employees
GROUP BY last_name;
```

Copy

##### Output[¶](#id94 "Link to this heading")

| last\_name |
| --- |
| SnoW |
|  |
| SNOW |
| SnoW |
| Snow |
| snow |

##### Snowflake[¶](#id95 "Link to this heading")

Note

*The order may differ.*

##### Query[¶](#id96 "Link to this heading")

```
 SELECT
   last_name
  FROM
   employees
  GROUP BY last_name;
```

Copy

##### Output[¶](#id97 "Link to this heading")

| first\_name |
| --- |
| Snow |
| SNOW |
| SnoW |
|  |
| SnoW |
| snow |

#### HAVING clause[¶](#having-clause "Link to this heading")

The HAVING clause will use the patterns in:

* Evaluation operations.

  + For example: `=, !=, <, >.`
* LIKE operation.
* IN Operation.
* CAST to evaluation operation.
* CAST to LIKE operation.

The following sample showcases a pattern with evaluation operation.

##### Sample: Column constraint is NOT CASESPECIFIC and database mode is ANSI Mode[¶](#sample-column-constraint-is-not-casespecific-and-database-mode-is-ansi-mode "Link to this heading")

##### Teradata[¶](#id98 "Link to this heading")

##### Query[¶](#id99 "Link to this heading")

```
 SELECT first_name
FROM employees
GROUP BY first_name
HAVING first_name = 'Mary';
```

Copy

##### Output[¶](#id100 "Link to this heading")

```
Mary
```

Copy

##### Snowflake[¶](#id101 "Link to this heading")

##### Query[¶](#id102 "Link to this heading")

```
 SELECT
  first_name
FROM
  employees
GROUP BY first_name
HAVING
   COLLATE(first_name, 'en-cs-rtrim') = 'Mary';
```

Copy

##### Output[¶](#id103 "Link to this heading")

```
Mary
```

Copy

#### CASE WHEN statement[¶](#case-when-statement "Link to this heading")

The `CASE WHEN` statement will use the patterns described in:

* Evaluation operations.

  + For example: `=, !=, <, >.`
* LIKE operation.
* IN Operation.
* CAST to evaluation operation.
* CAST to LIKE operation.

The following sample showcases a pattern with evaluation operation.

##### Teradata[¶](#id104 "Link to this heading")

##### Query[¶](#id105 "Link to this heading")

```
 SELECT first_name,
      last_name,
      CASE
          WHEN department = 'EngineerinG' THEN 'Information Technology'
          WHEN first_name = '    GeorgE   ' THEN 'GLOBAL SALES'
          ELSE 'Other'
      END AS department_full_name
FROM employees
WHERE last_name = '';
```

Copy

##### Output[¶](#id106 "Link to this heading")

| first\_name | last\_name | department\_full\_name |
| --- | --- | --- |
| GEORGE |  | Other |
| Mary |  | Other |
| GeorgE |  | GLOBAL SALES |
| GEORGE |  | Other |

##### Snowflake[¶](#id107 "Link to this heading")

##### Query[¶](#id108 "Link to this heading")

```
    SELECT
   first_name,
   last_name,
   CASE
         WHEN RTRIM(department) = RTRIM('EngineerinG')
            THEN 'Information Technology'
         WHEN COLLATE(first_name, 'en-cs-rtrim')  = '    GeorgE   '
            THEN 'GLOBAL SALES'
       ELSE 'Other'
   END AS department_full_name
FROM
   employees
WHERE RTRIM(last_name) = RTRIM('');
```

Copy

##### Output[¶](#id109 "Link to this heading")

| first\_name | last\_name | department\_full\_name |
| --- | --- | --- |
| Mary |  | Other |
| GEORGE |  | Other |
| GEORGE |  | Other |
| GeorgE |  | GLOBAL SALES |

#### JOIN clause[¶](#join-clause "Link to this heading")

Warning

Simple scenarios with evaluation operations are supported.

The `JOIN` statement will use the patterns described in:

* Evaluation operations.

  + For example: `=, !=, <, >.`
* LIKE operation.
* IN Operation.
* CAST to evaluation operation.
* CAST to LIKE operation.

The following sample showcases a pattern with evaluation operation.

##### Sample: Column constraint is NOT CASESPECIFIC and database mode is ANSI Mode[¶](#id110 "Link to this heading")

##### Teradata[¶](#id111 "Link to this heading")

##### Query[¶](#id112 "Link to this heading")

```
 SELECT
    e.employee_id,
    e.first_name,
    e.last_name,
    d.department_name
FROM
    employees e
JOIN
    departments d
ON
    e.department = d.department_name;
```

Copy

##### Output[¶](#id113 "Link to this heading")

| employee\_id | first\_name | last\_name | department\_name |
| --- | --- | --- | --- |
| 1 | George | Snow | Sales |
| 10 | JOHN | snow | Finance |

##### Snowflake[¶](#id114 "Link to this heading")

Note

`d.department_name` is `NOT CASESPECIFIC`, so it requires `COLLATE`.

##### Query[¶](#id115 "Link to this heading")

```
    SELECT
   e.employee_id,
   e.first_name,
   e.last_name,
   d.department_name
FROM
   employees e
JOIN
   departments d
ON COLLATE(e.department, 'en-cs-rtrim') = d.department_name;
```

Copy

##### Output[¶](#id116 "Link to this heading")

| employee\_id | first\_name | last\_name | department\_name |
| --- | --- | --- | --- |
| 1 | George | Snow | Sales |
| 10 | JOHN | snow | Finance |

#### Related EWIs[¶](#related-ewis "Link to this heading")

[SSC-EWI-TD0007](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/teradataEWI.html#ssc-ewi-td0007): GROUP BY IS NOT EQUIVALENT IN TERADATA MODE

[SC-FDM-TD0032](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/teradataFDM.html#ssc-fdm-td0032) : [NOT] CASESPECIFIC CLAUSE WAS REMOVED

## ANSI Mode For Strings Comparison - NO COLLATE[¶](#ansi-mode-for-strings-comparison-no-collate "Link to this heading")

This section defines the translation specification for a string in ANSI mode without the use of COLLATE.

### Description [¶](#id117 "Link to this heading")

#### ANSI mode for string comparison and NO COLATE usages.[¶](#ansi-mode-for-string-comparison-and-no-colate-usages "Link to this heading")

The ANSI mode string comparison without the use of COLLATE will apply RTRIM and UPPER as needed. The default case specification trim behavior may be taken into account, so if a column does not have a case specification in Teradata ANSI mode, Teradata will have as default `CASESPECIFIC`.

### Sample Source Patterns [¶](#id118 "Link to this heading")

#### Setup data[¶](#id119 "Link to this heading")

##### Teradata[¶](#id120 "Link to this heading")

```
 CREATE TABLE employees (
    employee_id INTEGER NOT NULL,
    first_name VARCHAR(50) NOT CASESPECIFIC,
    last_name VARCHAR(50) CASESPECIFIC,
    department VARCHAR(50)
);

INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (1, 'George', 'Snow', 'Sales');
INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (2, 'John', 'SNOW', 'Engineering');
INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (3, 'WIlle', 'SNOW', 'Human resources   ');
INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (4, 'Marco', 'SnoW   ', 'EngineerinG');
INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (5, 'Mary', '   ', 'SaleS  ');
INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (6, 'GEORGE', '  ', 'sales  ');
INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (7, 'GEORGE   ', '  ', 'salEs  ');
INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (8, '    GeorgE   ', '  ', 'SalEs  ');
INSERT INTO employees (employee_id, first_name, last_name, department) VALUES (9, 'JOHN', '   SnoW', 'IT');
INSERT INTO employees (employee_id, first_name, last_name, department) VALUES (10, 'JOHN    ', 'snow', 'Finance   ');

CREATE TABLE departments (
    department_id INTEGER NOT NULL,
    department_name VARCHAR(50) NOT CASESPECIFIC,
    location VARCHAR(100) CASESPECIFIC,
    PRIMARY KEY (department_id)
);


INSERT INTO departments (department_id, department_name, location) VALUES (101, 'Information Technology', 'New York');
INSERT INTO departments (department_id, department_name, location) VALUES (102, 'Human Resources', 'Chicago');
INSERT INTO departments (department_id, department_name, location) VALUES (103, 'Sales', 'San Francisco');
INSERT INTO departments (department_id, department_name, location) VALUES (104, 'Finance', 'Boston');
```

Copy

##### Snowflake[¶](#id121 "Link to this heading")

```
 CREATE OR REPLACE TABLE employees (
    employee_id INTEGER NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    department VARCHAR(50)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "10/30/2024",  "domain": "test" }}'
;

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (1, 'George', 'Snow', 'Sales');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (2, 'John', 'SNOW', 'Engineering');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (3, 'WIlle', 'SNOW', 'Human resources   ');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (4, 'Marco', 'SnoW   ', 'EngineerinG');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (5, 'Mary', '   ', 'SaleS  ');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (6, 'GEORGE', '  ', 'sales  ');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (7, 'GEORGE   ', '  ', 'salEs  ');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (8, '    GeorgE   ', '  ', 'SalEs  ');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (9, 'JOHN', '   SnoW', 'IT');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (10, 'JOHN    ', 'snow', 'Finance   ');

CREATE OR REPLACE TABLE departments (
    department_id INTEGER NOT NULL,
    department_name VARCHAR(50),
    location VARCHAR(100),
       PRIMARY KEY (department_id)
   )
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "10/30/2024",  "domain": "test" }}'
;

INSERT INTO departments (department_id, department_name, location)
VALUES (101, 'Information Technology', 'New York');

INSERT INTO departments (department_id, department_name, location)
VALUES (102, 'Human Resources', 'Chicago');

INSERT INTO departments (department_id, department_name, location)
VALUES (103, 'Sales', 'San Francisco');

INSERT INTO departments (department_id, department_name, location)
VALUES (104, 'Finance', 'Boston');
```

Copy

#### Comparison operation[¶](#id122 "Link to this heading")

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is ANSI Mode[¶](#id123 "Link to this heading")

##### Teradata[¶](#id124 "Link to this heading")

##### Query[¶](#id125 "Link to this heading")

```
 SELECT *
FROM employees
WHERE first_name = 'George      ';
```

Copy

##### Output[¶](#id126 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 1 | George | Snow | Sales |

##### Snowflake[¶](#id127 "Link to this heading")

##### Query[¶](#id128 "Link to this heading")

```
 SELECT
 *
FROM
employees
WHERE
RTRIM(first_name) = RTRIM('George      ');
```

Copy

##### Output[¶](#id129 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 1 | George | Snow | Sales |

##### Case 2: Column constraint is CASESPECIFIC and database mode is ANSI Mode[¶](#id130 "Link to this heading")

##### Teradata[¶](#id131 "Link to this heading")

##### Query[¶](#id132 "Link to this heading")

```
 SELECT *
FROM employees
WHERE last_name = 'SNOW ';
```

Copy

##### Output[¶](#id133 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 3 | WIlle | SNOW | Human resources |
| 2 | John | SNOW | Engineering |

##### Snowflake[¶](#id134 "Link to this heading")

##### Query[¶](#id135 "Link to this heading")

```
 SELECT
 *
FROM
employees
WHERE
 RTRIM(last_name) = RTRIM('SNOW ');
```

Copy

##### Output[¶](#id136 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 3 | WIlle | SNOW | Human resources |
| 2 | John | SNOW | Engineering |

##### Case 3: CAST NOT CASESPECIFIC column to CASESPECIFIC and database mode is ANSI Mode[¶](#id137 "Link to this heading")

Warning

The (`CASESPECIFIC`) overwrite the column constraint in the table definition.

##### Teradata[¶](#id138 "Link to this heading")

##### Query[¶](#id139 "Link to this heading")

```
 SELECT * FROM employees WHERE first_name = 'GEorge   ' (CASESPECIFIC);
```

Copy

##### Output[¶](#id140 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 7 | GEORGE |  | salEs |
| 6 | GEORGE |  | sales |

##### Snowflake[¶](#id141 "Link to this heading")

##### Query[¶](#id142 "Link to this heading")

```
 SELECT * FROM workers
WHERE RTRIM(first_name) = RTRIM(UPPER('GEorge   '));
```

Copy

##### Output[¶](#id143 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 7 | GEORGE |  | salEs |
| 6 | GEORGE |  | sales |

##### Case 4: CAST CASESPECIFIC column to NOT CASESPECIFIC and database mode is ANSI Mode[¶](#id144 "Link to this heading")

##### Teradata[¶](#id145 "Link to this heading")

##### Query[¶](#id146 "Link to this heading")

```
 SELECT * FROM employees
WHERE last_name = 'SnoW   ' (NOT CASESPECIFIC) ;
```

Copy

##### Output[¶](#id147 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 4 | Marco | SnoW | EngineerinG |

##### Snowflake[¶](#id148 "Link to this heading")

##### Query[¶](#id149 "Link to this heading")

```
 SELECT * FROM employees
WHERE RTRIM(last_name) = RTRIM('SnoW   ');
```

Copy

##### Output[¶](#id150 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 4 | Marco | SnoW | EngineerinG |

#### LIKE operation[¶](#id151 "Link to this heading")

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is ANSI Mode[¶](#id152 "Link to this heading")

##### Teradata[¶](#id153 "Link to this heading")

##### Query[¶](#id154 "Link to this heading")

```
 SELECT *
FROM employees
WHERE first_name LIKE 'Georg%';
```

Copy

##### Output[¶](#id155 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 1 | George | Snow | Sales |

##### Snowflake[¶](#id156 "Link to this heading")

##### Query[¶](#id157 "Link to this heading")

```
 SELECT *
FROM employees
WHERE first_name LIKE 'Georg%';
```

Copy

##### Output[¶](#id158 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 1 | George | Snow | Sales |

##### Case 2: Column constraint is CASESPECIFIC and database mode is ANSI Mode[¶](#id159 "Link to this heading")

##### Teradata[¶](#id160 "Link to this heading")

##### Query[¶](#id161 "Link to this heading")

```
 SELECT *
FROM employees
WHERE last_name LIKE 'Snow';
```

Copy

##### Output[¶](#id162 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 1 | George | Snow | Sales |

##### Snowflake[¶](#id163 "Link to this heading")

##### Query[¶](#id164 "Link to this heading")

```
 SELECT *
FROM employees
WHERE last_name LIKE 'Snow';
```

Copy

##### Output[¶](#id165 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 1 | George | Snow | Sales |

##### Case 3: CAST NOT CASESPECIFIC column to NOT CASESPECIFIC and database mode is ANSI Mode[¶](#case-3-cast-not-casespecific-column-to-not-casespecific-and-database-mode-is-ansi-mode "Link to this heading")

##### Teradata[¶](#id166 "Link to this heading")

##### Query[¶](#id167 "Link to this heading")

```
 SELECT *
FROM employees
WHERE first_name LIKE 'George' (NOT CASESPECIFIC);
```

Copy

##### Output[¶](#id168 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 1 | George | Snow | Sales |
| 6 | GEORGE |  | sales |

##### Snowflake[¶](#id169 "Link to this heading")

##### Query[¶](#id170 "Link to this heading")

```
 SELECT
   *
FROM
   employees
WHERE
   first_name ILIKE 'George' /*** SSC-FDM-TD0032 - NOT CASESPECIFIC CLAUSE WAS REMOVED ***/;
```

Copy

##### Output[¶](#id171 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 1 | George | Snow | Sales |
| 6 | GEORGE |  | sales |

##### Case 4: CAST CASESPECIFIC column to NOT CASESPECIFIC and database mode is ANSI Mode[¶](#id172 "Link to this heading")

##### Teradata[¶](#id173 "Link to this heading")

##### Query[¶](#id174 "Link to this heading")

```
 SELECT *
FROM employees
WHERE last_name LIKE 'SNO%' (NOT CASESPECIFIC);
```

Copy

##### Output[¶](#id175 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 2 | John | SNOW | Engineering |
| 3 | WIlle | SNOW | Human resources |

##### Snowflake[¶](#id176 "Link to this heading")

##### Query[¶](#id177 "Link to this heading")

```
 SELECT
   *
FROM
   employees
WHERE
   last_name LIKE 'SNO%' /*** SSC-FDM-TD0032 - NOT CASESPECIFIC CLAUSE WAS REMOVED ***/;
```

Copy

##### Output[¶](#id178 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 2 | John | SNOW | Engineering |
| 3 | WIlle | SNOW | Human resources |

#### IN Operation[¶](#id179 "Link to this heading")

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is ANSI Mode[¶](#id180 "Link to this heading")

##### Teradata[¶](#id181 "Link to this heading")

##### Query[¶](#id182 "Link to this heading")

```
 SELECT *
FROM employees
WHERE first_name IN ('GEORGE   ');
```

Copy

##### Output[¶](#id183 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 6 | GEORGE |  | sales |
| 7 | GEORGE |  | salEs |

##### Snowflake[¶](#id184 "Link to this heading")

##### Query[¶](#id185 "Link to this heading")

```
 SELECT *
FROM employees
WHERE RTRIM(first_name) IN (RTRIM('GEORGE   '));
```

Copy

##### Output[¶](#id186 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 6 | GEORGE |  | sales |
| 7 | GEORGE |  | salEs |

##### Case 2: Column constraint is CASESPECIFIC and database mode is ANSI Mode[¶](#id187 "Link to this heading")

##### Teradata[¶](#id188 "Link to this heading")

##### Query[¶](#id189 "Link to this heading")

```
 SELECT *
FROM employees
WHERE department IN ('SaleS');
```

Copy

##### Output[¶](#id190 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 5 | Mary |  | SaleS |

##### Snowflake[¶](#id191 "Link to this heading")

##### Query[¶](#id192 "Link to this heading")

```
 SELECT *
FROM employees
WHERE RTRIM(department) IN (RTRIM('SaleS'));
```

Copy

##### Output[¶](#id193 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 5 | Mary |  | SaleS |

#### ORDER BY clause[¶](#id194 "Link to this heading")

Note

**Notice that this functional equivalence can differ.**

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is ANSI Mode[¶](#id195 "Link to this heading")

##### Teradata[¶](#id196 "Link to this heading")

##### Query[¶](#id197 "Link to this heading")

```
 SELECT department_name
FROM departments
ORDER BY department_name;
```

Copy

##### Output[¶](#id198 "Link to this heading")

| department |
| --- |
| EngineerinG |
| Engineering |
| Finance |
| Human resources |
| IT |
| SalEs |
| SaleS |
| Sales |
| salEs |
| sales |

##### Snowflake[¶](#id199 "Link to this heading")

Note

**Please review FDM. The order differs in the order of insertion of data.**

##### Query[¶](#id200 "Link to this heading")

```
 SELECT
   department_name
FROM
   departments
ORDER BY
   UPPER(department_name);
```

Copy

##### Output[¶](#id201 "Link to this heading")

| department |
| --- |
| EngineerinG |
| Engineering |
| Finance |
| Human resources |
| IT |
| SalEs |
| SaleS |
| Sales |
| salEs |
| sales |

##### Case 2: Column constraint is CASESPECIFIC and database mode is ANSI Mode[¶](#id202 "Link to this heading")

##### Teradata[¶](#id203 "Link to this heading")

##### Query[¶](#id204 "Link to this heading")

```
 SELECT last_name
FROM employees
ORDER BY last_name;
```

Copy

##### Output[¶](#id205 "Link to this heading")

| department |
| --- |
| Finance |
| Human Resources |
| Information Technology |
| Sales |

##### Snowflake[¶](#id206 "Link to this heading")

##### Query[¶](#id207 "Link to this heading")

```
 SELECT last_name
FROM employees
ORDER BY last_name;
```

Copy

##### Output[¶](#id208 "Link to this heading")

| department |
| --- |
| Finance |
| Human Resources |
| Information Technology |
| Sales |

#### GROUP BY clause[¶](#id209 "Link to this heading")

Warning

**To ensure a functional equivalence, it is required to use the COLLATE expression.**

Please review the [SSC-EWI-TD0007](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/teradataEWI.html#ssc-ewi-td0007) for more information.

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is ANSI Mode[¶](#id210 "Link to this heading")

##### Teradata[¶](#id211 "Link to this heading")

##### Query[¶](#id212 "Link to this heading")

```
 SELECT first_name
FROM employees
GROUP BY first_name;
```

Copy

##### Output[¶](#id213 "Link to this heading")

| first\_name |
| --- |
| Mary |
| GeorgE |
| WIlle |
| John |
| Marco |
| GEORGE |

##### Snowflake[¶](#id214 "Link to this heading")

##### Query[¶](#id215 "Link to this heading")

```
 SELECT
   first_name
FROM
   employees
!!!RESOLVE EWI!!! /*** SSC-EWI-TD0007 - GROUP BY IS NOT EQUIVALENT IN TERADATA MODE ***/!!!
GROUP BY first_name;
```

Copy

##### Output[¶](#id216 "Link to this heading")

| FIRST\_NAME |
| --- |
| George |
| John |
| WIlle |
| Marco |
| Mary |
| GEORGE |
| GEORGE |
| GeorgE |
| JOHN |
| JOHN |

##### Case 2: Column constraint is CASESPECIFIC and database mode is ANSI Mode[¶](#id217 "Link to this heading")

##### Teradata[¶](#id218 "Link to this heading")

##### Query[¶](#id219 "Link to this heading")

```
 SELECT last_name
FROM employees
GROUP BY last_name;
```

Copy

##### Output[¶](#id220 "Link to this heading")

| last\_name |
| --- |
| SnoW |
|  |
| SNOW |
| SnoW |
| Snow |
| snow |

##### Snowflake[¶](#id221 "Link to this heading")

##### Query[¶](#id222 "Link to this heading")

```
 SELECT
   last_name
FROM
   employees
!!!RESOLVE EWI!!! /*** SSC-EWI-TD0007 - GROUP BY IS NOT EQUIVALENT IN TERADATA MODE ***/!!!
GROUP BY last_name;
```

Copy

##### Output[¶](#id223 "Link to this heading")

| last\_name |
| --- |
| SnoW |
|  |
| SNOW |
| SnoW |
| Snow |
| snow |

#### HAVING clause[¶](#id224 "Link to this heading")

The HAVING clause will use the patterns in:

* Evaluation operations.

  + For example: `=, !=, <, >.`
* LIKE operation.
* IN Operation.
* CAST to evaluation operation.
* CAST to LIKE operation.

The following sample showcases a pattern with evaluation operation.

##### Sample: Column constraint is NOT CASESPECIFIC and database mode is ANSI Mode[¶](#id225 "Link to this heading")

##### Teradata[¶](#id226 "Link to this heading")

##### Query[¶](#id227 "Link to this heading")

```
 SELECT first_name
FROM employees
GROUP BY first_name
HAVING first_name = 'GEORGE';
```

Copy

##### Output[¶](#id228 "Link to this heading")

```
GEORGE
```

Copy

##### Snowflake[¶](#id229 "Link to this heading")

##### Query[¶](#id230 "Link to this heading")

```
 SELECT
   first_name
FROM
   employees
GROUP BY first_name
HAVING
   RTRIM(first_name) = RTRIM('GEORGE');
```

Copy

##### Output[¶](#id231 "Link to this heading")

```
GEORGE
```

Copy

#### CASE WHEN statement[¶](#id232 "Link to this heading")

The `CASE WHEN` statement will use the patterns described in:

* Evaluation operations.

  + For example: `=, !=, <, >.`
* LIKE operation.
* IN Operation.
* CAST to evaluation operation.
* CAST to LIKE operation.

The following sample showcases a pattern with evaluation operation.

##### Teradata[¶](#id233 "Link to this heading")

##### Query[¶](#id234 "Link to this heading")

```
 SELECT first_name,
      last_name,
      CASE
          WHEN department = 'SaleS  ' THEN 'GLOBAL SALES'
          WHEN first_name = 'GEORGE   ' THEN 'Department Full Name'
          ELSE 'Other'
      END AS department_full_name
FROM employees
WHERE last_name = '   ';
```

Copy

##### Output[¶](#id235 "Link to this heading")

| first\_name | last\_name | department\_full\_name |
| --- | --- | --- |
| GEORGE |  | Department Full Name |
| Mary |  | GLOBAL SALES |
| GeorgE |  | Other |
| GEORGE |  | Department Full Name |

##### Snowflake[¶](#id236 "Link to this heading")

##### Query[¶](#id237 "Link to this heading")

```
 SELECT
      first_name,
      last_name,
      CASE
            WHEN UPPER(RTRIM(department)) = UPPER(RTRIM('SaleS  '))
                  THEN 'GLOBAL SALES'
            WHEN UPPER(RTRIM(first_name)) = UPPER(RTRIM('GEORGE   '))
                  THEN 'Department Full Name'
          ELSE 'Other'
      END AS department_full_name
FROM
      employees
WHERE
      UPPER(RTRIM( last_name)) = UPPER(RTRIM('   '));
```

Copy

##### Output[¶](#id238 "Link to this heading")

| first\_name | last\_name | department\_full\_name |
| --- | --- | --- |
| GEORGE |  | Department Full Name |
| Mary |  | GLOBAL SALES |
| GeorgE |  | Other |
| GEORGE |  | Department Full Name |

#### JOIN clause[¶](#id239 "Link to this heading")

Warning

Simple scenarios are supported.

The `JOIN` statement will use the patterns described in:

* Evaluation operations.

  + For example: `=, !=, <, >.`
* LIKE operation.
* IN Operation.
* CAST to evaluation operation.
* CAST to LIKE operation.

The following sample showcases a pattern with evaluation operation.

##### Sample: Column constraint is CASESPECIFIC and database mode is ANSI Mode[¶](#sample-column-constraint-is-casespecific-and-database-mode-is-ansi-mode "Link to this heading")

##### Teradata[¶](#id240 "Link to this heading")

##### Query[¶](#id241 "Link to this heading")

```
 SELECT
    e.employee_id,
    e.first_name,
    e.last_name,
    d.department_name
FROM
    employees e
JOIN
    departments d
ON
    e.department = d.department_name;
```

Copy

##### Output[¶](#id242 "Link to this heading")

| employee\_id | first\_name | last\_name | department\_name |
| --- | --- | --- | --- |
| 1 | George | Snow | Sales |
| 10 | JOHN | snow | Finance |

##### Snowflake[¶](#id243 "Link to this heading")

##### Query[¶](#id244 "Link to this heading")

```
 SELECT
   e.employee_id,
   e.first_name,
   e.last_name,
   d.department_name
FROM
   employees e
JOIN
      departments d
ON RTRIM(e.department) = RTRIM(d.department_name);
```

Copy

##### Output[¶](#id245 "Link to this heading")

| employee\_id | first\_name | last\_name | department\_name |
| --- | --- | --- | --- |
| 1 | George | Snow | Sales |
| 10 | JOHN | snow | Finance |

### Related EWIs[¶](#id246 "Link to this heading")

[SSC-EWI-TD0007](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/teradataEWI.html#ssc-ewi-td0007): GROUP BY IS NOT EQUIVALENT IN TERADATA MODE

## TERA Mode For Strings Comparison - COLLATE[¶](#tera-mode-for-strings-comparison-collate "Link to this heading")

This section defines the translation specification for string in Tera mode with the use of COLLATE.

### Description [¶](#id247 "Link to this heading")

#### Tera Mode for string comparison and COLLATE usage[¶](#tera-mode-for-string-comparison-and-collate-usage "Link to this heading")

The Tera Mode string comparison will apply the COLLATE constraint to the columns or statements as required. The default case specification trim behavior may be taken into account. The default case specification in Teradata for TERA mode is `NOT CASESPECIFIC`. Thus, the columns without case specification will have `COLLATE('en-ci')` constraints.

### Sample Source Patterns [¶](#id248 "Link to this heading")

#### Setup data[¶](#id249 "Link to this heading")

##### Teradata[¶](#id250 "Link to this heading")

```
 CREATE TABLE employees (
    employee_id INTEGER NOT NULL,
    first_name VARCHAR(50) NOT CASESPECIFIC,
    last_name VARCHAR(50) CASESPECIFIC,
    department VARCHAR(50)
);

INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (1, 'George', 'Snow', 'Sales');
INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (2, 'John', 'SNOW', 'Engineering');
INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (3, 'WIlle', 'SNOW', 'Human resources   ');
INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (4, 'Marco', 'SnoW   ', 'EngineerinG');
INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (5, 'Mary', '   ', 'SaleS  ');
INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (6, 'GEORGE', '  ', 'sales  ');
INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (7, 'GEORGE   ', '  ', 'salEs  ');
INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (8, '    GeorgE   ', '  ', 'SalEs  ');
INSERT INTO employees (employee_id, first_name, last_name, department) VALUES (9, 'JOHN', '   SnoW', 'IT');
INSERT INTO employees (employee_id, first_name, last_name, department) VALUES (10, 'JOHN    ', 'snow', 'Finance   ');

CREATE TABLE departments (
    department_id INTEGER NOT NULL,
    department_name VARCHAR(50) NOT CASESPECIFIC,
    location VARCHAR(100) CASESPECIFIC,
    PRIMARY KEY (department_id)
);


INSERT INTO departments (department_id, department_name, location) VALUES (101, 'Information Technology', 'New York');
INSERT INTO departments (department_id, department_name, location) VALUES (102, 'Human Resources', 'Chicago');
INSERT INTO departments (department_id, department_name, location) VALUES (103, 'Sales', 'San Francisco');
INSERT INTO departments (department_id, department_name, location) VALUES (104, 'Finance', 'Boston');
```

Copy

##### Snowflake[¶](#id251 "Link to this heading")

```
 CREATE OR REPLACE TABLE employees (
    employee_id INTEGER NOT NULL,
    first_name VARCHAR(50) COLLATE 'en-ci',
    last_name VARCHAR(50),
    department VARCHAR(50) COLLATE 'en-ci'
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "11/01/2024",  "domain": "test" }}'
;

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (1, 'George', 'Snow', 'Sales');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (2, 'John', 'SNOW', 'Engineering');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (3, 'WIlle', 'SNOW', 'Human resources   ');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (4, 'Marco', 'SnoW   ', 'EngineerinG');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (5, 'Mary', '   ', 'SaleS  ');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (6, 'GEORGE', '  ', 'sales  ');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (7, 'GEORGE   ', '  ', 'salEs  ');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (8, '    GeorgE   ', '  ', 'SalEs  ');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (9, 'JOHN', '   SnoW', 'IT');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (10, 'JOHN    ', 'snow', 'Finance   ');

CREATE OR REPLACE TABLE departments (
    department_id INTEGER NOT NULL,
    department_name VARCHAR(50) COLLATE 'en-ci',
    location VARCHAR(100),
       PRIMARY KEY (department_id)
   )
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "11/01/2024",  "domain": "test" }}'
;

INSERT INTO departments (department_id, department_name, location)
VALUES (101, 'Information Technology', 'New York');

INSERT INTO departments (department_id, department_name, location)
VALUES (102, 'Human Resources', 'Chicago');

INSERT INTO departments (department_id, department_name, location)
VALUES (103, 'Sales', 'San Francisco');

INSERT INTO departments (department_id, department_name, location)
VALUES (104, 'Finance', 'Boston');
```

Copy

#### Comparison operation[¶](#id252 "Link to this heading")

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is TERA Mode[¶](#case-1-column-constraint-is-not-casespecific-and-database-mode-is-tera-mode "Link to this heading")

##### Teradata[¶](#id253 "Link to this heading")

##### Query[¶](#id254 "Link to this heading")

```
 SELECT *
FROM employees
WHERE first_name = 'GEorge ';
```

Copy

##### Output[¶](#id255 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 7 | GEORGE |  | salEs |
| 1 | George | Snow | Sales |
| 6 | GEORGE |  | sales |

##### Snowflake[¶](#id256 "Link to this heading")

##### Query[¶](#id257 "Link to this heading")

```
 SELECT
 *
FROM
 employees
WHERE
 RTRIM(first_name) = RTRIM('GEorge ');
```

Copy

##### Output[¶](#id258 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 7 | GEORGE |  | salEs |
| 1 | George | Snow | Sales |
| 6 | GEORGE |  | sales |

##### Case 2: Column constraint is CASESPECIFIC and database mode is TERA Mode[¶](#case-2-column-constraint-is-casespecific-and-database-mode-is-tera-mode "Link to this heading")

##### Teradata[¶](#id259 "Link to this heading")

##### Query[¶](#id260 "Link to this heading")

```
 SELECT *
FROM employees
WHERE last_name = 'SNOW ';
```

Copy

##### Output[¶](#id261 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 3 | WIlle | SNOW | Human resources |
| 2 | John | SNOW | Engineering |

##### Snowflake[¶](#id262 "Link to this heading")

##### Query[¶](#id263 "Link to this heading")

```
SELECT
 *
FROM
 employees
WHERE
 RTRIM(last_name) = RTRIM('SNOW ');
```

Copy

##### Output[¶](#id264 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 3 | WIlle | SNOW | Human resources |
| 2 | John | SNOW | Engineering |

##### Case 3: CAST NOT CASESPECIFIC column to CASESPECIFIC and database mode is TERA Mode[¶](#case-3-cast-not-casespecific-column-to-casespecific-and-database-mode-is-tera-mode "Link to this heading")

Note

Notice that the following queries

* `SELECT * FROM employees WHERE first_name = 'JOHN ' (CASESPECIFIC)`
* `SELECT * FROM employees WHERE first_name (CASESPECIFIC) = 'JOHN '`

will return the same values.

##### Teradata[¶](#id265 "Link to this heading")

##### Query[¶](#id266 "Link to this heading")

```
 SELECT * FROM employees WHERE first_name = 'JOHN   ' (CASESPECIFIC);
```

Copy

##### Output[¶](#id267 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 9 | JOHN | SnoW | IT |
| 10 | JOHN | snow | Finance |

##### Snowflake[¶](#id268 "Link to this heading")

##### Query[¶](#id269 "Link to this heading")

```
 SELECT
    *
FROM
    employees
WHERE 
    COLLATE(first_name, 'en-cs-rtrim') = 'JOHN   ' /*** SSC-FDM-TD0032 - CASESPECIFIC CLAUSE WAS REMOVED ***/;
```

Copy

##### Output[¶](#id270 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 9 | JOHN | SnoW | IT |
| 10 | JOHN | snow | Finance |

##### Case 4: CAST CASESPECIFIC column to NOT CASESPECIFIC and database mode is TERA Mode[¶](#case-4-cast-casespecific-column-to-not-casespecific-and-database-mode-is-tera-mode "Link to this heading")

Note

CAST to a column on the left side of the comparison has priority.

For example:

* `SELECT * FROM employees WHERE last_name (NOT CASESPECIFIC) = 'snoW';` *will return **5 rows.***
* `SELECT * FROM employees WHERE last_name = 'snoW' (NOT CASESPECIFIC);` *will return **0 rows** with this setup data.*

##### Teradata[¶](#id271 "Link to this heading")

##### Query[¶](#id272 "Link to this heading")

```
 SELECT * FROM employees WHERE last_name (NOT CASESPECIFIC)  = 'snoW' ;
```

Copy

##### Output[¶](#id273 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 1 | George | Snow | Sales |
| 2 | John | SNOW | Engineering |
| 3 | WIlle | SNOW | Human resources |
| 4 | Marco | SnoW | EngineerinG |
| 10 | JOHN | snow | Finance |

##### Snowflake[¶](#id274 "Link to this heading")

##### Query[¶](#id275 "Link to this heading")

```
 SELECT
   *
FROM
   employees
WHERE
   COLLATE(last_name /*** SSC-FDM-TD0032 - NOT CASESPECIFIC CLAUSE WAS REMOVED ***/, 'en-ci-rtrim') = 'snoW' ;
```

Copy

##### Output[¶](#id276 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 1 | George | Snow | Sales |
| 2 | John | SNOW | Engineering |
| 3 | WIlle | SNOW | Human resources |
| 4 | Marco | SnoW | EngineerinG |
| 10 | JOHN | snow | Finance |

#### LIKE operation[¶](#id277 "Link to this heading")

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is TERA Mode[¶](#id278 "Link to this heading")

##### Teradata[¶](#id279 "Link to this heading")

##### Query[¶](#id280 "Link to this heading")

```
 SELECT *
FROM employees
WHERE first_name LIKE 'GeorgE';
```

Copy

##### Output[¶](#id281 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 1 | George | Snow | Sales |
| 6 | GEORGE |  | sales |

##### Snowflake[¶](#id282 "Link to this heading")

##### Query[¶](#id283 "Link to this heading")

```
 SELECT
   *
FROM
   employees
WHERE
   RTRIM(first_name) LIKE RTRIM('GeorgE');
```

Copy

##### Output[¶](#id284 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 1 | George | Snow | Sales |
| 6 | GEORGE |  | sales |

##### Case 2: Column constraint is CASESPECIFIC and database mode is TERA Mode[¶](#id285 "Link to this heading")

##### Teradata[¶](#id286 "Link to this heading")

##### Query[¶](#id287 "Link to this heading")

```
 SELECT *
FROM employees
WHERE last_name LIKE 'Snow';
```

Copy

##### Output[¶](#id288 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 1 | George | Snow | Sales |

##### Snowflake[¶](#id289 "Link to this heading")

##### Query[¶](#id290 "Link to this heading")

```
 SELECT
   *
FROM
   employees
WHERE
   RTRIM(last_name) LIKE RTRIM('Snow');
```

Copy

##### Output[¶](#id291 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 1 | George | Snow | Sales |

##### Case 3: CAST NOT CASESPECIFIC column to CASESPECIFIC and database mode is TERA Mode[¶](#id292 "Link to this heading")

##### Teradata[¶](#id293 "Link to this heading")

##### Query[¶](#id294 "Link to this heading")

```
 SELECT *
FROM employees
WHERE first_name LIKE 'George' (CASESPECIFIC);
```

Copy

##### Output[¶](#id295 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 1 | George | Snow | Sales |

##### Snowflake[¶](#id296 "Link to this heading")

##### Query[¶](#id297 "Link to this heading")

```
 SELECT
    *
FROM
    employees
WHERE
    COLLATE(first_name, 'en-cs-rtrim') LIKE 'George';
```

Copy

##### Output[¶](#id298 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 1 | George | Snow | Sales |

##### Case 4: CAST CASESPECIFIC column to NOT CASESPECIFIC and database mode is TERA Mode[¶](#id299 "Link to this heading")

##### Teradata[¶](#id300 "Link to this heading")

##### Query[¶](#id301 "Link to this heading")

```
 SELECT *
FROM employees
WHERE last_name LIKE 'SNO%' (NOT CASESPECIFIC);
```

Copy

##### Output[¶](#id302 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 3 | WIlle | SNOW | Human resources |
| 2 | John | SNOW | Engineering |

##### Snowflake[¶](#id303 "Link to this heading")

##### Query[¶](#id304 "Link to this heading")

```
 SELECT
   *
FROM
   employees
WHERE
   RTRIM(last_name) LIKE RTRIM('SNO%' /*** SSC-FDM-TD0032 - NOT CASESPECIFIC CLAUSE WAS REMOVED ***/);
```

Copy

##### Output[¶](#id305 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 3 | WIlle | SNOW | Human resources |
| 2 | John | SNOW | Engineering |

#### IN Operation[¶](#id306 "Link to this heading")

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is TERA Mode[¶](#id307 "Link to this heading")

##### Teradata[¶](#id308 "Link to this heading")

##### Query[¶](#id309 "Link to this heading")

```
 SELECT *
FROM employees
WHERE first_name IN ('George   ');
```

Copy

##### Output[¶](#id310 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 7 | GEORGE |  | salEs |
| 1 | George | Snow | Sales |
| 6 | GEORGE |  | sales |

##### Snowflake[¶](#id311 "Link to this heading")

##### Query[¶](#id312 "Link to this heading")

```
 SELECT
   *
FROM
   employees
WHERE
   RTRIM(first_name) IN (RTRIM('George   '));
```

Copy

##### Output[¶](#id313 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 7 | GEORGE |  | salEs |
| 1 | George | Snow | Sales |
| 6 | GEORGE |  | sales |

##### Case 2: Column constraint is not defined and database mode is TERA Mode[¶](#case-2-column-constraint-is-not-defined-and-database-mode-is-tera-mode "Link to this heading")

Note

In Tera mode, not defined case specification means `NOT CASESPECIFIC`.

##### Teradata[¶](#id314 "Link to this heading")

##### Query[¶](#id315 "Link to this heading")

```
 SELECT *
FROM employees
WHERE department IN ('Sales    ');
```

Copy

##### Output[¶](#id316 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 1 | George | Snow | Sales |
| 5 | Mary |  | SaleS |
| 6 | GEORGE |  | sales |
| 7 | GEORGE |  | salEs |
| 8 | GeorgE |  | SalEs |

##### Snowflake[¶](#id317 "Link to this heading")

##### Query[¶](#id318 "Link to this heading")

```
 SELECT
   *
FROM
   employees
WHERE
   RTRIM(department) IN (RTRIM('Sales    '));
```

Copy

##### Output[¶](#id319 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 1 | George | Snow | Sales |
| 5 | Mary |  | SaleS |
| 6 | GEORGE |  | sales |
| 7 | GEORGE |  | salEs |
| 8 | GeorgE |  | SalEs |

##### Case 3: Column constraint is CASESPECIFIC and database mode is TERA Mode[¶](#case-3-column-constraint-is-casespecific-and-database-mode-is-tera-mode "Link to this heading")

##### Teradata[¶](#id320 "Link to this heading")

##### Query[¶](#id321 "Link to this heading")

```
 SELECT *
FROM employees
WHERE last_name IN ('SNOW   ');
```

Copy

##### Output[¶](#id322 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 3 | WIlle | SNOW | Human resources |
| 2 | John | SNOW | Engineering |

##### Snowflake[¶](#id323 "Link to this heading")

##### Query[¶](#id324 "Link to this heading")

```
 SELECT
   *
FROM
   employees
WHERE
   RTRIM(last_name) IN (RTRIM('SNOW   '));
```

Copy

##### Output[¶](#id325 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 3 | WIlle | SNOW | Human resources |
| 2 | John | SNOW | Engineering |

#### ORDER BY clause[¶](#id326 "Link to this heading")

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is TERA Mode[¶](#id327 "Link to this heading")

##### Teradata[¶](#id328 "Link to this heading")

##### Query[¶](#id329 "Link to this heading")

```
 SELECT employee_id, first_name
FROM employees
ORDER BY employee_id, first_name;
```

Copy

##### Output[¶](#id330 "Link to this heading")

| employee\_id | first\_name |
| --- | --- |
| 1 | George |
| 2 | John |
| 3 | WIlle |
| 4 | Marco |
| 5 | Mary |
| 6 | GEORGE |
| 7 | GEORGE |
| 8 | GeorgE |
| 9 | JOHN |
| 10 | JOHN |

##### Snowflake[¶](#id331 "Link to this heading")

##### Query[¶](#id332 "Link to this heading")

```
 SELECT employee_id, first_name
FROM employees
ORDER BY employee_id, first_name;
```

Copy

##### Output[¶](#id333 "Link to this heading")

| employee\_id | first\_name |
| --- | --- |
| 1 | George |
| 2 | John |
| 3 | WIlle |
| 4 | Marco |
| 5 | Mary |
| 6 | GEORGE |
| 7 | GEORGE |
| 8 | GeorgE |
| 9 | JOHN |
| 10 | JOHN |

##### Case 2: Column constraint is CASESPECIFIC and database mode is TERA Mode[¶](#id334 "Link to this heading")

##### Teradata[¶](#id335 "Link to this heading")

##### Query[¶](#id336 "Link to this heading")

```
 SELECT employee_id, last_name
FROM employees
ORDER BY employee_id, last_name;
```

Copy

##### Output[¶](#id337 "Link to this heading")

| employee\_id | last\_name |
| --- | --- |
| 1 | Snow |
| 2 | SNOW |
| 3 | SNOW |
| 4 | SnoW |
| 5 |  |
| 6 |  |
| 7 |  |
| 8 |  |
| 9 | SnoW |
| 10 | snow |

##### Snowflake[¶](#id338 "Link to this heading")

##### Query[¶](#id339 "Link to this heading")

```
 SELECT employee_id, last_name
FROM employees
ORDER BY employee_id, last_name;
```

Copy

##### Output[¶](#id340 "Link to this heading")

| employee\_id | last\_name |
| --- | --- |
| 1 | Snow |
| 2 | SNOW |
| 3 | SNOW |
| 4 | SnoW |
| 5 |  |
| 6 |  |
| 7 |  |
| 8 |  |
| 9 | SnoW |
| 10 | snow |

#### GROUP BY clause[¶](#id341 "Link to this heading")

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is TERA Mode[¶](#id342 "Link to this heading")

##### Teradata[¶](#id343 "Link to this heading")

##### Query[¶](#id344 "Link to this heading")

```
 SELECT first_name
FROM employees
GROUP BY first_name;
```

Copy

##### Output[¶](#id345 "Link to this heading")

| first\_name |
| --- |
| Mary |
| GeorgE |
| WIlle |
| **JOHN** |
| Marco |
| **GEORGE** |

##### Snowflake[¶](#id346 "Link to this heading")

Warning

Case specification in output may vary depending on the number of columns selected.

##### Query[¶](#id347 "Link to this heading")

```
 SELECT
   first_name
FROM
   employees
GROUP BY first_name;
```

Copy

##### Output[¶](#id348 "Link to this heading")

| first\_name |
| --- |
| **John** |
| Marco |
| **George** |
| GeorgE |
| WIlle |
| Mary |

##### Case 2: Column constraint is CASESPECIFIC and database mode is TERA Mode[¶](#id349 "Link to this heading")

##### Teradata[¶](#id350 "Link to this heading")

##### Query[¶](#id351 "Link to this heading")

```
 SELECT last_name
FROM employees
GROUP BY last_name;
```

Copy

##### Output[¶](#id352 "Link to this heading")

| last\_name |
| --- |
| SnoW |
|  |
| SNOW |
| SnoW |
| Snow |
| snow |

##### Snowflake[¶](#id353 "Link to this heading")

##### Query[¶](#id354 "Link to this heading")

```
 SELECT
   last_name
FROM
   employees
GROUP BY last_name;
```

Copy

##### Output[¶](#id355 "Link to this heading")

| last\_name |
| --- |
| SnoW |
|  |
| SNOW |
| SnoW |
| Snow |
| snow |

#### HAVING clause[¶](#id356 "Link to this heading")

The HAVING clause will use the patterns in:

* Evaluation operations.

  + For example: `=, !=, <, >.`
* LIKE operation.
* IN Operation.
* CAST to evaluation operation.
* CAST to LIKE operation.

The following sample showcases a pattern with evaluation operation.

##### Sample: Column constraint is NOT CASESPECIFIC and database mode is TERA Mode[¶](#sample-column-constraint-is-not-casespecific-and-database-mode-is-tera-mode "Link to this heading")

##### Teradata[¶](#id357 "Link to this heading")

Note

Case specification in output may vary depending on the number of columns selected. This is also related to the `GROUP BY` clause.

##### Query[¶](#id358 "Link to this heading")

```
 SELECT first_name
FROM employees
GROUP BY first_name
HAVING first_name = 'George  ';
```

Copy

##### Output[¶](#id359 "Link to this heading")

| employee\_id | first\_name |
| --- | --- |
| 7 | GEORGE |
| 1 | George |
| 6 | GEORGE |

##### Snowflake[¶](#id360 "Link to this heading")

##### Query[¶](#id361 "Link to this heading")

```
 SELECT
  employee_id,
  first_name
FROM
  employees
GROUP BY employee_id, first_name
HAVING
   RTRIM(first_name) = RTRIM('George  ');
```

Copy

##### Output[¶](#id362 "Link to this heading")

| employee\_id | first\_name |
| --- | --- |
| 7 | GEORGE |
| 1 | George |
| 6 | GEORGE |

#### CASE WHEN statement[¶](#id363 "Link to this heading")

The `CASE WHEN` statement will use the patterns described in:

* Evaluation operations.

  + For example: `=, !=, <, >.`
* LIKE operation.
* IN Operation.
* CAST to evaluation operation.
* CAST to LIKE operation.

The following sample showcases a pattern with evaluation operation.

##### Teradata[¶](#id364 "Link to this heading")

##### Query[¶](#id365 "Link to this heading")

```
 SELECT first_name,
      last_name,
      CASE
          WHEN department = 'Engineering' THEN 'Information Technology'
          WHEN first_name = 'GeorgE' THEN 'GLOBAL SALES'
          ELSE 'Other'
      END AS department_full_name
FROM employees
WHERE last_name = '';
```

Copy

##### Output[¶](#id366 "Link to this heading")

| first\_name | last\_name | department\_full\_name |
| --- | --- | --- |
| GEORGE |  | GLOBAL SALES |
| Mary |  | Other |
| GeorgE |  | Other |
| GEORGE |  | GLOBAL SALES |

##### Snowflake[¶](#id367 "Link to this heading")

##### Query[¶](#id368 "Link to this heading")

```
 SELECT
   first_name,
   last_name,
   CASE
      WHEN RTRIM(department) = RTRIM('Engineering')
         THEN 'Information Technology'
      WHEN RTRIM(first_name) = RTRIM('GeorgE')
         THEN 'GLOBAL SALES'
      ELSE 'Other'
   END AS department_full_name
FROM
   employees
WHERE
   RTRIM( last_name) = RTRIM('');
```

Copy

##### Output[¶](#id369 "Link to this heading")

| first\_name | last\_name | department\_full\_name |
| --- | --- | --- |
| GEORGE |  | GLOBAL SALES |
| Mary |  | Other |
| GeorgE |  | Other |
| GEORGE |  | GLOBAL SALES |

#### JOIN clause[¶](#id370 "Link to this heading")

Warning

Simple scenarios with evaluation operations are supported.

The `JOIN` statement will use the patterns described in:

* EvaluaComparisonComparisontion operations.

  + For example: `=, !=, <, >.`
* LIKE operation.
* IN Operation.
* CAST to evaluation operation.
* CAST to LIKE operation.

The following sample showcases a pattern with evaluation operation.

##### Sample: Column constraint is NOT CASESPECIFIC and database mode is TERA Mode[¶](#id371 "Link to this heading")

##### Teradata[¶](#id372 "Link to this heading")

##### Query[¶](#id373 "Link to this heading")

```
 SELECT
    e.employee_id,
    e.first_name,
    e.last_name,
    d.department_name
FROM
    employees e
JOIN
    departments d
ON
    e.department = d.department_name;
```

Copy

##### Output[¶](#id374 "Link to this heading")

| employee\_id | first\_name | last\_name | department\_name |
| --- | --- | --- | --- |
| 1 | George | Snow | Sales |
| 3 | WIlle | SNOW | Human Resources |
| 5 | Mary |  | Sales |
| 6 | GEORGE |  | Sales |
| 7 | GEORGE |  | Sales |
| 8 | GeorgE |  | Sales |
| 10 | JOHN | snow | Finance |

##### Snowflake[¶](#id375 "Link to this heading")

##### Query[¶](#id376 "Link to this heading")

```
 SELECT
   e.employee_id,
   e.first_name,
   e.last_name,
   d.department_name
FROM
   employees e
JOIN
   departments d
ON RTRIM(e.department) = RTRIM(d.department_name);
```

Copy

##### Output[¶](#id377 "Link to this heading")

| employee\_id | first\_name | last\_name | department\_name |
| --- | --- | --- | --- |
| 1 | George | Snow | Sales |
| 3 | WIlle | SNOW | Human Resources |
| 5 | Mary |  | Sales |
| 6 | GEORGE |  | Sales |
| 7 | GEORGE |  | Sales |
| 8 | GeorgE |  | Sales |
| 10 | JOHN | snow | Finance |

### Related EWIs[¶](#id378 "Link to this heading")

[SSC-EWI-TD0007](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/teradataFDM.html#ssc-fdm-td0007): GROUP BY REQUIRED COLLATE FOR CASE INSENSITIVE COLUMNS

[SC-FDM-TD0032](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/teradataFDM.html#ssc-fdm-td0032) : [NOT] CASESPECIFIC CLAUSE WAS REMOVED

## TERA Mode For Strings Comparison - NO COLLATE[¶](#tera-mode-for-strings-comparison-no-collate "Link to this heading")

This section defines the translation specification for string in Tera mode without using COLLATE.

### Description [¶](#id379 "Link to this heading")

#### Tera Mode for string comparison and NO COLLATE usages[¶](#tera-mode-for-string-comparison-and-no-collate-usages "Link to this heading")

The Tera Mode string comparison without the use of COLLATE will apply `RTRIM` and `UPPER` as needed. The default case specification trim behavior may be taken into account.

### Sample Source Patterns [¶](#id380 "Link to this heading")

#### Setup data[¶](#id381 "Link to this heading")

##### Teradata[¶](#id382 "Link to this heading")

```
 CREATE TABLE employees (
    employee_id INTEGER NOT NULL,
    first_name VARCHAR(50) NOT CASESPECIFIC,
    last_name VARCHAR(50) CASESPECIFIC,
    department VARCHAR(50)
);

INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (1, 'George', 'Snow', 'Sales');
INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (2, 'John', 'SNOW', 'Engineering');
INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (3, 'WIlle', 'SNOW', 'Human resources   ');
INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (4, 'Marco', 'SnoW   ', 'EngineerinG');
INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (5, 'Mary', '   ', 'SaleS  ');
INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (6, 'GEORGE', '  ', 'sales  ');
INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (7, 'GEORGE   ', '  ', 'salEs  ');
INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (8, '    GeorgE   ', '  ', 'SalEs  ');
INSERT INTO employees (employee_id, first_name, last_name, department) VALUES (9, 'JOHN', '   SnoW', 'IT');
INSERT INTO employees (employee_id, first_name, last_name, department) VALUES (10, 'JOHN    ', 'snow', 'Finance   ');

CREATE TABLE departments (
    department_id INTEGER NOT NULL,
    department_name VARCHAR(50) NOT CASESPECIFIC,
    location VARCHAR(100) CASESPECIFIC,
    PRIMARY KEY (department_id)
);


INSERT INTO departments (department_id, department_name, location) VALUES (101, 'Information Technology', 'New York');
INSERT INTO departments (department_id, department_name, location) VALUES (102, 'Human Resources', 'Chicago');
INSERT INTO departments (department_id, department_name, location) VALUES (103, 'Sales', 'San Francisco');
INSERT INTO departments (department_id, department_name, location) VALUES (104, 'Finance', 'Boston');
```

Copy

##### Snowflake[¶](#id383 "Link to this heading")

```
 CREATE OR REPLACE TABLE employees (
    employee_id INTEGER NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    department VARCHAR(50)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "10/30/2024",  "domain": "test" }}'
;

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (1, 'George', 'Snow', 'Sales');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (2, 'John', 'SNOW', 'Engineering');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (3, 'WIlle', 'SNOW', 'Human resources   ');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (4, 'Marco', 'SnoW   ', 'EngineerinG');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (5, 'Mary', '   ', 'SaleS  ');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (6, 'GEORGE', '  ', 'sales  ');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (7, 'GEORGE   ', '  ', 'salEs  ');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (8, '    GeorgE   ', '  ', 'SalEs  ');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (9, 'JOHN', '   SnoW', 'IT');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (10, 'JOHN    ', 'snow', 'Finance   ');

CREATE OR REPLACE TABLE departments (
    department_id INTEGER NOT NULL,
    department_name VARCHAR(50),
    location VARCHAR(100),
       PRIMARY KEY (department_id)
   )
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "10/30/2024",  "domain": "test" }}'
;

INSERT INTO departments (department_id, department_name, location)
VALUES (101, 'Information Technology', 'New York');

INSERT INTO departments (department_id, department_name, location)
VALUES (102, 'Human Resources', 'Chicago');

INSERT INTO departments (department_id, department_name, location)
VALUES (103, 'Sales', 'San Francisco');

INSERT INTO departments (department_id, department_name, location)
VALUES (104, 'Finance', 'Boston');
```

Copy

#### Comparison operation[¶](#id384 "Link to this heading")

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is TERA Mode[¶](#id385 "Link to this heading")

This example demonstrates the usage of a column set up as `NOT CASESPECIFIC` as it is a `first_name` column. Even when asking for the string `'GEorge',` the query execution will retrieve results in Teradata because the case specification is not considered.

To emulate this scenario in Snowflake, there are implemented two functions: `RTRIM(UPPER(string_evaluation))`, `UPPER` is required in this scenario because the string does not review the case specification.

##### Teradata[¶](#id386 "Link to this heading")

##### Query[¶](#id387 "Link to this heading")

```
 SELECT *
FROM employees
WHERE first_name = 'GEorge ';
```

Copy

##### Output[¶](#id388 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 7 | GEORGE |  | salEs |
| 1 | George | Snow | Sales |
| 6 | GEORGE |  | sales |

##### Snowflake[¶](#id389 "Link to this heading")

##### Query[¶](#id390 "Link to this heading")

```
 SELECT
 *
FROM
 employees
WHERE
 RTRIM(UPPER(first_name)) = RTRIM(UPPER('GEorge '));
```

Copy

##### Output[¶](#id391 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 7 | GEORGE |  | salEs |
| 1 | George | Snow | Sales |
| 6 | GEORGE |  | sales |

##### Case 2: Column constraint is CASESPECIFIC and database mode is TERA Mode[¶](#id392 "Link to this heading")

For this example, the column constraint is `CASESPECIFIC`, for which the example does not retrieve rows in Teradata because ‘`Snow`’ is not equal to ‘`SNOW`’.

In Snowflake, the resulting migration points only to the use of the `RTRIM` function since the case specification is important.

##### Teradata[¶](#id393 "Link to this heading")

##### Query[¶](#id394 "Link to this heading")

```
 SELECT *
FROM employees
WHERE last_name = 'SNOW ';
```

Copy

##### Output[¶](#id395 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 3 | WIlle | SNOW | Human resources |
| 2 | John | SNOW | Engineering |

##### Snowflake[¶](#id396 "Link to this heading")

##### Query[¶](#id397 "Link to this heading")

```
SELECT
 *
FROM
 employees
WHERE
 RTRIM(last_name) = RTRIM('SNOW ');
```

Copy

##### Output[¶](#id398 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 3 | WIlle | SNOW | Human resources |
| 2 | John | SNOW | Engineering |

##### Case 3: CAST CASESPECIFIC column to NOT CASESPECIFIC and database mode is TERA Mode[¶](#case-3-cast-casespecific-column-to-not-casespecific-and-database-mode-is-tera-mode "Link to this heading")

##### Teradata[¶](#id399 "Link to this heading")

Warning

The (`CASESPECIFIC`) overrides the column constraint in the table definition.

##### Query[¶](#id400 "Link to this heading")

```
 SELECT * FROM employees WHERE first_name = 'GEORGE   ' (CASESPECIFIC);
```

Copy

##### Output[¶](#id401 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 7 | GEORGE |  | salEs |
| 6 | GEORGE |  | sales |

##### Snowflake[¶](#id402 "Link to this heading")

Note

RTRIM is required on the left side, and RTRIM is required on the right side.

##### Query[¶](#id403 "Link to this heading")

```
 SELECT
   * 
FROM
   employees
WHERE
   RTRIM(first_name) = RTRIM('GEORGE   ' /*** SSC-FDM-TD0032 - CASESPECIFIC CLAUSE WAS REMOVED ***/);
```

Copy

##### Output[¶](#id404 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 7 | GEORGE |  | salEs |
| 6 | GEORGE |  | sales |

##### Case 4: CAST NOT CASESPECIFIC column to NOT CASESPECIFIC and database mode is TERA Mode[¶](#case-4-cast-not-casespecific-column-to-not-casespecific-and-database-mode-is-tera-mode "Link to this heading")

##### Teradata[¶](#id405 "Link to this heading")

##### Query[¶](#id406 "Link to this heading")

```
 SELECT * FROM employees WHERE first_name = 'GEorge   ' (NOT CASESPECIFIC) ;
```

Copy

##### Output[¶](#id407 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 7 | GEORGE |  | salEs |
| 1 | George | Snow | Sales |
| 6 | GEORGE |  | sales |

##### Snowflake[¶](#id408 "Link to this heading")

##### Query[¶](#id409 "Link to this heading")

```
 SELECT
   * 
FROM
   employees
WHERE
   UPPER(RTRIM(first_name)) = UPPER(RTRIM('GEorge   ' /*** SSC-FDM-TD0032 - NOT CASESPECIFIC CLAUSE WAS REMOVED ***/));
```

Copy

##### Output[¶](#id410 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 7 | GEORGE |  | salEs |
| 1 | George | Snow | Sales |
| 6 | GEORGE |  | sales |

##### Case 5: Blank spaces case. Column constraint is NOT CASESPECIFIC, database mode is TERA Mode, and using equal operation[¶](#case-5-blank-spaces-case-column-constraint-is-not-casespecific-database-mode-is-tera-mode-and-using-equal-operation "Link to this heading")

##### Teradata[¶](#id411 "Link to this heading")

##### Query[¶](#id412 "Link to this heading")

```
 SELECT *
FROM employees
WHERE last_name = '   ';
```

Copy

##### Output[¶](#id413 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 7 | GEORGE |  | salEs |
| 5 | Mary |  | SaleS |
| 8 | GeorgE |  | SalEs |
| 6 | GEORGE |  | sales |

##### Snowflake[¶](#id414 "Link to this heading")

##### Query[¶](#id415 "Link to this heading")

```
 SELECT
   *
FROM
   employees
WHERE
   RTRIM(last_name) = RTRIM('   ');
```

Copy

##### Output[¶](#id416 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 7 | GEORGE |  | salEs |
| 5 | Mary |  | SaleS |
| 8 | GeorgE |  | SalEs |
| 6 | GEORGE |  | sales |

#### LIKE operation[¶](#id417 "Link to this heading")

Note

This operation works differently from another one. Blank spaces must be the same quantity to retrieve information.

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is TERA Mode[¶](#id418 "Link to this heading")

This example is expected to display one row because the case specification is not relevant.

Note

In Snowflake, the migration uses the [ILIKE](https://docs.snowflake.com/en/sql-reference/functions/ilike) operation. This performs a case-insensitive comparison.

##### Teradata[¶](#id419 "Link to this heading")

##### Query[¶](#id420 "Link to this heading")

```
 SELECT *
FROM employees
WHERE first_name LIKE 'GeorgE';
```

Copy

##### Output[¶](#id421 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 1 | George | Snow | Sales |
| 6 | GEORGE |  | sales |

##### Snowflake[¶](#id422 "Link to this heading")

##### Query[¶](#id423 "Link to this heading")

```
 SELECT *
FROM employees
WHERE first_name ILIKE 'GeorgE';
```

Copy

##### Output[¶](#id424 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 1 | George | Snow | Sales |
| 6 | GEORGE |  | sales |

##### Case 2: Column constraint is CASESPECIFIC and database mode is TERA Mode[¶](#id425 "Link to this heading")

##### Teradata[¶](#id426 "Link to this heading")

##### Query[¶](#id427 "Link to this heading")

```
 SELECT *
FROM employees
WHERE last_name LIKE 'Snow';
```

Copy

##### Output[¶](#id428 "Link to this heading")

| first\_name | last\_name | department |
| --- | --- | --- |
| George | Snow | Sales |
| Jonh | Snow | Engineering |

##### Snowflake[¶](#id429 "Link to this heading")

##### Query[¶](#id430 "Link to this heading")

```
 SELECT *
FROM employees
WHERE last_name LIKE 'Snow';
```

Copy

##### Output[¶](#id431 "Link to this heading")

| first\_name | last\_name | department |
| --- | --- | --- |
| George | Snow | Sales |
| Jonh | Snow | Engineering |

##### Case 3: CAST CASESPECIFIC column to NOT CASESPECIFIC and database mode is TERA Mode[¶](#id432 "Link to this heading")

##### Teradata[¶](#id433 "Link to this heading")

##### Query[¶](#id434 "Link to this heading")

```
 SELECT *
FROM employees
WHERE first_name LIKE 'George' (NOT CASESPECIFIC);
```

Copy

##### Output[¶](#id435 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 1 | George | Snow | Sales |
| 6 | GEORGE |  | sales |

##### Snowflake[¶](#id436 "Link to this heading")

##### Query[¶](#id437 "Link to this heading")

```
 SELECT
   *
FROM
   employees
WHERE 
   first_name ILIKE 'George' /*** SSC-FDM-TD0032 - NOT CASESPECIFIC CLAUSE WAS REMOVED ***/;
```

Copy

##### Output[¶](#id438 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 1 | George | Snow | Sales |
| 6 | GEORGE |  | sales |

##### Case 4: CAST NOT CASESPECIFIC column to NOT CASESPECIFIC and database mode is ANSI Mode[¶](#case-4-cast-not-casespecific-column-to-not-casespecific-and-database-mode-is-ansi-mode "Link to this heading")

Note

This case requires the translation to `ILIKE`.

##### Teradata[¶](#id439 "Link to this heading")

##### Query[¶](#id440 "Link to this heading")

```
 SELECT *
FROM employees
WHERE first_name LIKE 'GE%' (NOT CASESPECIFIC);
```

Copy

##### Output[¶](#id441 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 7 | GEORGE |  | salEs |
| 1 | George | Snow | Sales |
| 6 | GEORGE |  | sales |

##### Snowflake[¶](#id442 "Link to this heading")

##### Query[¶](#id443 "Link to this heading")

```
 SELECT
   *
FROM
   employees
WHERE
   first_name ILIKE 'GE%' /*** SSC-FDM-TD0032 - NOT CASESPECIFIC CLAUSE WAS REMOVED ***/;
```

Copy

##### Output[¶](#id444 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 7 | GEORGE |  | salEs |
| 1 | George | Snow | Sales |
| 6 | GEORGE |  | sales |

#### IN Operation[¶](#id445 "Link to this heading")

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is TERA Mode[¶](#id446 "Link to this heading")

##### Teradata[¶](#id447 "Link to this heading")

##### Query[¶](#id448 "Link to this heading")

```
 SELECT *
FROM employees
WHERE first_name IN ('GeorgE');
```

Copy

##### Output[¶](#id449 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 7 | GEORGE |  | salEs |
| 1 | George | Snow | Sales |
| 6 | GEORGE |  | sales |

##### Snowflake[¶](#id450 "Link to this heading")

##### Query[¶](#id451 "Link to this heading")

```
 SELECT *
FROM employees
WHERE RTRIM(UPPER(first_name)) IN (RTRIM(UPPER('GeorgE')));
```

Copy

##### Output[¶](#id452 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 7 | GEORGE |  | salEs |
| 1 | George | Snow | Sales |
| 6 | GEORGE |  | sales |

##### Case 2: Column constraint is CASESPECIFIC and database mode is TERA Mode[¶](#id453 "Link to this heading")

For this example, the usage of the UPPER function is not required since, in the Teradata database, the case specification is relevant to the results.

##### Teradata[¶](#id454 "Link to this heading")

##### Query[¶](#id455 "Link to this heading")

```
 SELECT *
FROM employees
WHERE last_name IN ('SnoW');
```

Copy

##### Output[¶](#id456 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 4 | Marco | SnoW | EngineerinG |

##### Snowflake[¶](#id457 "Link to this heading")

##### Query[¶](#id458 "Link to this heading")

```
 SELECT *
FROM employees
WHERE RTRIM(last_name) IN (RTRIM('SnoW'));
```

Copy

##### Output[¶](#id459 "Link to this heading")

| employee\_id | first\_name | last\_name | department |
| --- | --- | --- | --- |
| 4 | Marco | SnoW | EngineerinG |

#### ORDER BY clause[¶](#id460 "Link to this heading")

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is TERA Mode[¶](#id461 "Link to this heading")

Danger

**Notice that this output order can differ.**

##### Teradata[¶](#id462 "Link to this heading")

##### Query[¶](#id463 "Link to this heading")

```
 SELECT department
FROM employees
ORDER BY department;
```

Copy

##### Output[¶](#id464 "Link to this heading")

| department |
| --- |
| EngineerinG |
| Engineering |
| Finance |
| Human resources |
| IT |
| sales |
| SalEs |
| Sales |
| SaleS |
| salEs |

##### Snowflake[¶](#id465 "Link to this heading")

##### Query[¶](#id466 "Link to this heading")

```
 SELECT department
FROM employees
ORDER BY UPPER(department);
```

Copy

##### Output[¶](#id467 "Link to this heading")

| department |
| --- |
| EngineerinG |
| Engineering |
| Finance |
| Human resources |
| IT |
| sales |
| SalEs |
| Sales |
| SaleS |
| salEs |

##### Case 2: Column constraint is CASESPECIFIC and database mode is TERA Mode[¶](#id468 "Link to this heading")

Danger

**Notice that this output can differ in order.**

##### Teradata[¶](#id469 "Link to this heading")

##### Query[¶](#id470 "Link to this heading")

```
 SELECT last_name
FROM employees
ORDER BY last_name;
```

Copy

##### Output[¶](#id471 "Link to this heading")

| last\_name |
| --- |
|  |
|  |
|  |
|  |
| SnoW |
| SNOW |
| SNOW |
| SnoW |
| Snow |
| snow |

##### Snowflake[¶](#id472 "Link to this heading")

##### Query[¶](#id473 "Link to this heading")

```
 SELECT last_name
FROM employees
ORDER BY last_name;
```

Copy

##### Output[¶](#id474 "Link to this heading")

| last\_name |
| --- |
|  |
|  |
|  |
|  |
| SnoW |
| SNOW |
| SNOW |
| SnoW |
| Snow |
| snow |

#### GROUP BY clause[¶](#id475 "Link to this heading")

Warning

**Notice that this output can differ. To ensure a functional equivalence, it is required to use the COLLATE expression.**

Please review the SSC-EWI-TD0007 for more information.

*The following might be a workaround without `collate`:*

`SELECT RTRIM(UPPER(first_name))`

`FROM employees`

`GROUP BY RTRIM(UPPER(first_name));`

**About the column behavior**

Danger

Please review the insertion of data in Snowflake. Snowflake does allow the insertion of values as ‘`GEORGE`’ and ‘`georges`’ without showing errors because the case specification is not bound explicitly with the column.

Assume a table and data as follows:

```
 CREATE TABLE students (
   first_name VARCHAR(50) NOT CASESPECIFIC
);

INSERT INTO students(first_name) VALUES ('George');
INSERT INTO students(first_name) VALUES ('   George');
```

Copy

Notice that this sample does not allow inserting values with upper and lower case letters in the `NOT CASESPECIFIC` column because it takes it as the same value. Because the column does not supervise the case specification, the ‘GEORGE’ and ‘george’ values are checked as the same information.

The following rows are taken as ***duplicated row errors***:

```
 INSERT INTO students(first_name) VALUES ('GEORGE');
INSERT INTO students(first_name) VALUES ('GeorGe');
INSERT INTO students(first_name) VALUES ('George  ');
INSERT INTO students(first_name) VALUES ('GeOrge');
INSERT INTO students(first_name) VALUES ('GEorge');
INSERT INTO students(first_name) VALUES ('George');
```

Copy

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is TERA Mode[¶](#id476 "Link to this heading")

##### Teradata[¶](#id477 "Link to this heading")

##### Query[¶](#id478 "Link to this heading")

```
 SELECT first_name
FROM employees
GROUP BY first_name;
```

Copy

##### Output[¶](#id479 "Link to this heading")

| first\_name |
| --- |
| Mary |
| GeorgE |
| WIlle |
| JOHN |
| Marco |
| GEORGE |

##### Snowflake[¶](#id480 "Link to this heading")

##### Query[¶](#id481 "Link to this heading")

```
 SELECT
   first_name
FROM
   employees
!!!RESOLVE EWI!!! /*** SSC-EWI-TD0007 - GROUP BY IS NOT EQUIVALENT IN TERADATA MODE ***/!!!
GROUP BY first_name;
```

Copy

##### Output[¶](#id482 "Link to this heading")

| first\_name |
| --- |
| George |
| John |
| WIlle |
| Marco |
| Mary |
| GEORGE |
| GEORGE |
| GeorgE |
| JOHN |
| JOHN |

##### Case 2: Column constraint is CASESPECIFIC and database mode is TERA Mode[¶](#id483 "Link to this heading")

##### Teradata[¶](#id484 "Link to this heading")

##### Query[¶](#id485 "Link to this heading")

```
 SELECT last_name
FROM employees
GROUP BY last_name;
```

Copy

##### Output[¶](#id486 "Link to this heading")

| last\_name |
| --- |
| SnoW |
|  |
| SNOW |
| SnoW |
| Snow |
| snow |

##### Snowflake[¶](#id487 "Link to this heading")

##### Query[¶](#id488 "Link to this heading")

```
 SELECT
   last_name
FROM
   employees
!!!RESOLVE EWI!!! /*** SSC-EWI-TD0007 - GROUP BY IS NOT EQUIVALENT IN TERADATA MODE ***/!!!
GROUP BY last_name;
```

Copy

##### Output[¶](#id489 "Link to this heading")

| last\_name |
| --- |
| SnoW |
| SNOW |
| SnoW |
|  |
|  |
| Snow |
| snow |

#### HAVING clause[¶](#id490 "Link to this heading")

The HAVING clause will use the patterns in:

* Evaluation operations.

  + For example: `=, !=, <, >.`
* LIKE operation.
* IN Operation.
* CAST to evaluation operation.
* CAST to LIKE operation.

The following sample showcases a pattern with evaluation operation.

##### Sample: Column constraint is CASESPECIFIC and database mode is TERA Mode[¶](#sample-column-constraint-is-casespecific-and-database-mode-is-tera-mode "Link to this heading")

##### Teradata[¶](#id491 "Link to this heading")

##### Query[¶](#id492 "Link to this heading")

```
 SELECT last_name
FROM employees
GROUP BY last_name
HAVING last_name = 'Snow';
```

Copy

##### Output[¶](#id493 "Link to this heading")

| last\_name |
| --- |
| Snow |

##### Snowflake[¶](#id494 "Link to this heading")

##### Query[¶](#id495 "Link to this heading")

```
 SELECT last_name
FROM employees
GROUP BY last_name
HAVING RTRIM(last_name) = RTRIM('Snow');
```

Copy

##### Output[¶](#id496 "Link to this heading")

| last\_name |
| --- |
| Snow |

#### CASE WHEN statement[¶](#id497 "Link to this heading")

The `CASE WHEN` statement will use the patterns described in:

* Evaluation operations.

  + For example: `=, !=, <, >.`
* LIKE operation.
* IN Operation.
* CAST to evaluation operation.
* CAST to LIKE operation.

The following sample showcases a pattern with evaluation operation.

##### Teradata[¶](#id498 "Link to this heading")

##### Query[¶](#id499 "Link to this heading")

```
 SELECT first_name,
      last_name,
      CASE
          WHEN department = 'EngineerinG' THEN 'Information Technology'
          WHEN last_name = 'SNOW' THEN 'GLOBAL COOL SALES'
          ELSE 'Other'
      END AS department_full_name
FROM employees;
```

Copy

##### Output[¶](#id500 "Link to this heading")

| first\_name | last\_name | department\_full\_name |
| --- | --- | --- |
| GEORGE |  | Other |
| JOHN | SnoW | Other |
| Mary |  | Other |
| JOHN | snow | Other |
| WIlle | SNOW | GLOBAL COOL SALES |
| George | Snow | Other |
| GeorgE |  | Other |
| GEORGE |  | Other |
| Marco | SnoW | Information Technology |
| John | SNOW | Information Technology |

##### Snowflake[¶](#id501 "Link to this heading")

##### Query[¶](#id502 "Link to this heading")

```
 SELECT
   first_name,
   last_name,
   CASE
      WHEN UPPER(RTRIM(department)) = UPPER(RTRIM('EngineerinG'))
         THEN 'Information Technology'
      WHEN RTRIM(last_name) = RTRIM('SNOW')
         THEN 'GLOBAL COOL SALES'
      ELSE 'Other'
   END AS department_full_name
FROM
   employees;
```

Copy

##### Output[¶](#id503 "Link to this heading")

| first\_name | last\_name | department\_full\_name |
| --- | --- | --- |
| GEORGE |  | Other |
| JOHN | SnoW | Other |
| Mary |  | Other |
| JOHN | snow | Other |
| WIlle | SNOW | GLOBAL COOL SALES |
| George | Snow | Other |
| GeorgE |  | Other |
| GEORGE |  | Other |
| Marco | SnoW | Information Technology |
| John | SNOW | Information Technology |

#### JOIN clause[¶](#id504 "Link to this heading")

Warning

Simple scenarios are supported.

The `JOIN` statement will use the patterns described in:

* Evaluation operations.

  + For example: `=, !=, <, >.`
* LIKE operation.
* IN Operation.
* CAST to evaluation operation.
* CAST to LIKE operation.

The following sample showcases a pattern with evaluation operation.

##### Sample: Column constraint is NOT CASESPECIFIC and database mode is TERA Mode[¶](#id505 "Link to this heading")

##### Teradata[¶](#id506 "Link to this heading")

##### Query[¶](#id507 "Link to this heading")

```
 SELECT
    e.employee_id,
    e.first_name,
    e.last_name,
    d.department_name
FROM
    employees e
JOIN
    departments d
ON
    e.department = d.department_name;
```

Copy

##### Output[¶](#id508 "Link to this heading")

| employee\_id | first\_name | last\_name | department\_name |
| --- | --- | --- | --- |
| 1 | George | Snow | Sales |
| 3 | WIlle | SNOW | Human Resources |
| 5 | Mary |  | Sales |
| 6 | GEORGE |  | Sales |
| 7 | GEORGE |  | Sales |
| 8 | GeorgE |  | Sales |
| 10 | JOHN | snow | Finance |

##### Snowflake[¶](#id509 "Link to this heading")

##### Query[¶](#id510 "Link to this heading")

```
 SELECT
   e.employee_id,
   e.first_name,
   e.last_name,
   d.department_name
FROM
   employees e
JOIN
   departments d
ON UPPER(RTRIM(e.department)) = UPPER(RTRIM(d.department_name));
```

Copy

##### Output[¶](#id511 "Link to this heading")

| employee\_id | first\_name | last\_name | department\_name |
| --- | --- | --- | --- |
| 1 | George | Snow | Sales |
| 3 | WIlle | SNOW | Human Resources |
| 5 | Mary |  | Sales |
| 6 | GEORGE |  | Sales |
| 7 | GEORGE |  | Sales |
| 8 | GeorgE |  | Sales |
| 10 | JOHN | snow | Finance |

### Known Issues[¶](#known-issues "Link to this heading")

1. there are some mode-specific SQL statement restrictions: `BEGIN TRANSACTION`, `END TRANSACTION`, `COMMIT [WORK]`.
2. Data insertion may differ in Snowflake since the case specification is not bound to the column declaration.
3. `GROUP BY` may differ in order, but group the correct values.
4. `ORDER BY` behaves differently in Snowflake.
5. If a function has a TRIM() from the source code, this workaround will add the required functions to the source code. So, RTRIM will be applied to the TRIM() source function.

### Related EWIs[¶](#id512 "Link to this heading")

[SSC-EWI-TD0007](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/teradataEWI.html#ssc-ewi-td0007): GROUP BY IS NOT EQUIVALENT IN TERADATA MODE

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

1. [Teradata session modes description](#teradata-session-modes-description)
2. [ANSI Mode For Strings Comparison - COLLATE](#ansi-mode-for-strings-comparison-collate)
3. [ANSI Mode For Strings Comparison - NO COLLATE](#ansi-mode-for-strings-comparison-no-collate)
4. [TERA Mode For Strings Comparison - COLLATE](#tera-mode-for-strings-comparison-collate)
5. [TERA Mode For Strings Comparison - NO COLLATE](#tera-mode-for-strings-comparison-no-collate)