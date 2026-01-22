---
auto_generated: true
description: Translation reference for SELECT statement inside procedures in Transact-SQL.
last_scraped: '2026-01-14T16:54:09.234586+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/transact/transact-select
title: SnowConvert AI - SQL Server-Azure Synapse - SELECT | Snowflake Documentation
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)Translation References[SQL Server-Azure Synapse](README.md)SELECT

# SnowConvert AI - SQL Server-Azure Synapse - SELECT[¶](#snowconvert-ai-sql-server-azure-synapse-select "Link to this heading")

## SELECT[¶](#select "Link to this heading")

Translation reference for SELECT statement inside procedures in Transact-SQL.

Applies to

* SQL Server
* Azure Synapse Analytics

Note

Multiple result sets are returned in temporary tables

### Description[¶](#description "Link to this heading")

Snowflake SQL support returning tables in as a return type for Stored Procedures, but unlike Transact-SQL, Snowflake does not support returning multiple resultsets in the same procedure. For this scenario, all the query IDs are stored in a temporary table and returned as an array.

### Sample Source Patterns[¶](#sample-source-patterns "Link to this heading")

The following example details the transformation when there is only one SELECT statement in the procedure.

#### Transact-SQL[¶](#transact-sql "Link to this heading")

##### Single Resultset[¶](#single-resultset "Link to this heading")

```
CREATE PROCEDURE SOMEPROC()
AS
BEGIN
        SELECT * from AdventureWorks.HumanResources.Department;
END
```

Copy

##### Output[¶](#output "Link to this heading")

| DepartmentID | Name | GroupName |
| --- | --- | --- |
| 1 | Engineering | Research and Development |
| 2 | Tool Design | Research and Development |
| 3 | Sales | Sales and Marketing |
| 4 | Marketing | Sales and Marketing |
| 5 | Purchasing | Inventory Management |
| 6 | Research and Development | Research and Development |
| 7 | Production | Manufacturing |
| 8 | Production Control | Manufacturing |
| 9 | Human Resources | Executive General and Administration |
| 10 | Finance | Executive General and Administration |
| 11 | Information Services | Executive General and Administration |
| 12 | Document Control | Quality Assurance |
| 13 | Quality Assurance | Quality Assurance |
| 14 | Facilities and Maintenance | Executive General and Administration |
| 15 | Shipping and Receiving | Inventory Management |
| 16 | Executive | Executive General and Administration |

##### Snowflake SQL[¶](#snowflake-sql "Link to this heading")

##### Single Resultset[¶](#id1 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE SOMEPROC ()
RETURNS TABLE()
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
        DECLARE
                ProcedureResultSet RESULTSET;
        BEGIN
                ProcedureResultSet := (
                SELECT
                        *
                from
                        AdventureWorks.HumanResources.Department);
                RETURN TABLE(ProcedureResultSet);
        END;
$$;
```

Copy

##### Output[¶](#id2 "Link to this heading")

| DepartmentID | Name | GroupName |
| --- | --- | --- |
| 1 | Engineering | Research and Development |
| 2 | Tool Design | Research and Development |
| 3 | Sales | Sales and Marketing |
| 4 | Marketing | Sales and Marketing |
| 5 | Purchasing | Inventory Management |
| 6 | Research and Development | Research and Development |
| 7 | Production | Manufacturing |
| 8 | Production Control | Manufacturing |
| 9 | Human Resources | Executive General and Administration |
| 10 | Finance | Executive General and Administration |
| 11 | Information Services | Executive General and Administration |
| 12 | Document Control | Quality Assurance |
| 13 | Quality Assurance | Quality Assurance |
| 14 | Facilities and Maintenance | Executive General and Administration |
| 15 | Shipping and Receiving | Inventory Management |
| 16 | Executive | Executive General and Administration |

The following example details the transformation when there are many SELECT statements in the procedure.

##### Transact-SQL[¶](#id3 "Link to this heading")

##### Multiple Resultset[¶](#multiple-resultset "Link to this heading")

```
 CREATE PROCEDURE SOMEPROC()
AS
BEGIN
        SELECT * from AdventureWorks.HumanResources.Department;
        SELECT * from AdventureWorks.HumanResources.Shift;
END
```

Copy

##### Output[¶](#id4 "Link to this heading")

| DepartmentID | Name | GroupName |
| --- | --- | --- |
| 1 | Engineering | Research and Development |
| 2 | Tool Design | Research and Development |
| 3 | Sales | Sales and Marketing |
| 4 | Marketing | Sales and Marketing |
| 5 | Purchasing | Inventory Management |
| 6 | Research and Development | Research and Development |
| 7 | Production | Manufacturing |
| 8 | Production Control | Manufacturing |
| 9 | Human Resources | Executive General and Administration |
| 10 | Finance | Executive General and Administration |
| 11 | Information Services | Executive General and Administration |
| 12 | Document Control | Quality Assurance |
| 13 | Quality Assurance | Quality Assurance |
| 14 | Facilities and Maintenance | Executive General and Administration |
| 15 | Shipping and Receiving | Inventory Management |
| 16 | Executive | Executive General and Administration |

| ShiftID | Name | StartTime | EndTime | ModifiedDate |
| --- | --- | --- | --- | --- |
| 1 | Day | 07:00:00 | 15:00:00 | 2008-04-30 00:00:00.000 |
| 2 | Evening | 15:00:00 | 23:00:00 | 2008-04-30 00:00:00.000 |
| 3 | Night | 23:00:00 | 07:00:00 | 2008-04-30 00:00:00.000 |

##### Snowflake SQL[¶](#id5 "Link to this heading")

##### Single Resultset[¶](#id6 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE SOMEPROC ()
RETURNS ARRAY
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
        DECLARE
                ProcedureResultSet1 VARCHAR;
                ProcedureResultSet2 VARCHAR;
                return_arr ARRAY := array_construct();
        BEGIN
                ProcedureResultSet1 := 'RESULTSET_' || REPLACE(UPPER(UUID_STRING()), '-', '_');
                CREATE OR REPLACE TEMPORARY TABLE IDENTIFIER(:ProcedureResultSet1) AS
                        SELECT
                                *
                        from
                                AdventureWorks.HumanResources.Department;
                return_arr := array_append(return_arr, :ProcedureResultSet1);
                ProcedureResultSet2 := 'RESULTSET_' || REPLACE(UPPER(UUID_STRING()), '-', '_');
                CREATE OR REPLACE TEMPORARY TABLE IDENTIFIER(:ProcedureResultSet2) AS
                        SELECT
                                *
                        from
                                AdventureWorks.HumanResources.Shift;
                return_arr := array_append(return_arr, :ProcedureResultSet2);
                --** SSC-FDM-0020 - MULTIPLE RESULT SETS ARE RETURNED IN TEMPORARY TABLES **
                RETURN return_arr;
        END;
$$;
```

Copy

##### Output[¶](#id7 "Link to this heading")

| DepartmentID | Name | GroupName |
| --- | --- | --- |
| 1 | Engineering | Research and Development |
| 2 | Tool Design | Research and Development |
| 3 | Sales | Sales and Marketing |
| 4 | Marketing | Sales and Marketing |
| 5 | Purchasing | Inventory Management |
| 6 | Research and Development | Research and Development |
| 7 | Production | Manufacturing |
| 8 | Production Control | Manufacturing |
| 9 | Human Resources | Executive General and Administration |
| 10 | Finance | Executive General and Administration |
| 11 | Information Services | Executive General and Administration |
| 12 | Document Control | Quality Assurance |
| 13 | Quality Assurance | Quality Assurance |
| 14 | Facilities and Maintenance | Executive General and Administration |
| 15 | Shipping and Receiving | Inventory Management |
| 16 | Executive | Executive General and Administration |

| ShiftID | Name | StartTime | EndTime | ModifiedDate |
| --- | --- | --- | --- | --- |
| 1 | Day | 07:00:00 | 15:00:00 | 2008-04-30 00:00:00.000 |
| 2 | Evening | 15:00:00 | 23:00:00 | 2008-04-30 00:00:00.000 |
| 3 | Night | 23:00:00 | 07:00:00 | 2008-04-30 00:00:00.000 |

### Known Issues[¶](#known-issues "Link to this heading")

1. The query results should be accessed by using the IDs returned by the Stored Procedure

### Related EWIs[¶](#related-ewis "Link to this heading")

1. [SSC-FDM-0020](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0020): Multiple result sets are returned in temporary tables.

## TOP[¶](#top "Link to this heading")

Applies to

* SQL Server
* Azure Synapse Analytics

### Description[¶](#id8 "Link to this heading")

Note

Some parts in the output code are omitted for clarity reasons.

Limits the rows returned in a query result set to a specified number of rows or percentage of rows. When you use `TOP` with the `ORDER BY` clause, the result set is limited to the first *N* number of ordered rows. Otherwise, `TOP` returns the first ***N*** number of rows in an undefined order. Use this clause to specify the number of rows returned from a `SELECT` statement. Or, use `TOP` to specify the rows affected by an `INSERT`, `UPDATE`, `MERGE`, or `DELETE` statement. ([Transact-SQL TOP documentation](https://learn.microsoft.com/en-us/sql/t-sql/queries/top-transact-sql?view=sql-server-ver16))

#### Syntax in Transact-SQL[¶](#syntax-in-transact-sql "Link to this heading")

```
 TOP (expression) [PERCENT] [ WITH TIES ]
```

Copy

Note

To get more information about the **`TOP`** arguments please check the [Transact-SQL TOP documentation](https://learn.microsoft.com/en-us/sql/t-sql/queries/top-transact-sql?view=sql-server-ver16#arguments).

##### Syntax in Snowflake[¶](#syntax-in-snowflake "Link to this heading")

```
 TOP <n>
```

Copy

Note

To get more information about **`TOP`** arguments please check the [Snowflake TOP documentation](https://docs.snowflake.com/en/sql-reference/constructs/top_n#parameters).

### Sample Source Patterns[¶](#id9 "Link to this heading")

To execute correctly the following samples it is required run the next `CREATE TABLE` statement:

#### Transact-SQL[¶](#id10 "Link to this heading")

```
 CREATE TABLE Cars(
    Model VARCHAR(15), 
    Price MONEY, 
    Color VARCHAR(10)
);

INSERT Cars VALUES ('sedan', 10000, 'red'), 
('convertible', 15000, 'blue'),
('coupe', 20000, 'red'), 
('van', 8000, 'blue'),
('sub', 8000, 'green');
```

Copy

##### Snowflake[¶](#snowflake "Link to this heading")

```
 CREATE OR REPLACE TABLE Cars (
    Model VARCHAR(15),
    Price NUMBER(38, 4),
    Color VARCHAR(10)
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
;

INSERT INTO Cars VALUES ('sedan', 10000, 'red'),
('convertible', 15000, 'blue'),
('coupe', 20000, 'red'),
('van', 8000, 'blue'),
('sub', 8000, 'green');
```

Copy

#### Common Case[¶](#common-case "Link to this heading")

##### Transact-SQL[¶](#id11 "Link to this heading")

##### Query[¶](#query "Link to this heading")

```
 SELECT TOP(1) Model, Color, Price
FROM Cars
WHERE Color = 'red'
```

Copy

##### Result[¶](#result "Link to this heading")

| Model | Color | Price |
| --- | --- | --- |
| sedan | red | 10000.0000 |

##### Snowflake[¶](#id12 "Link to this heading")

##### Query[¶](#id13 "Link to this heading")

```
 SELECT
TOP 1
Model,
Color,
Price
FROM
Cars
WHERE
Color = 'red';
```

Copy

##### Result[¶](#id14 "Link to this heading")

| MODEL | COLOR | PRICE |
| --- | --- | --- |
| sedan | red | 10,000 |

#### TOP using PERCENT[¶](#top-using-percent "Link to this heading")

##### Transact-SQL[¶](#id15 "Link to this heading")

##### Query[¶](#id16 "Link to this heading")

```
 SELECT TOP(50)PERCENT Model, Color, Price FROM Cars
```

Copy

##### Result[¶](#id17 "Link to this heading")

| Model | Color | Prices |
| --- | --- | --- |
| sedan | red | 10000.0000 |
| convertible | blue | 15000.0000 |
| coupe | green | 20000.0000 |

##### Snowflake[¶](#id18 "Link to this heading")

##### Query[¶](#id19 "Link to this heading")

```
SELECT
TOP 50 !!!RESOLVE EWI!!! /*** SSC-EWI-0040 - THE 'TOP PERCENT' CLAUSE IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
Model,
Color,
Price
FROM
Cars;
```

Copy

##### Result[¶](#id20 "Link to this heading")

| MODEL | COLOR | PRICE |
| --- | --- | --- |
| sedan | red | 10,000 |
| convertible | blue | 15,000 |
| coupe | red | 20,000 |
| van | blue | 8,000 |
| sub | green | 8,000 |

Warning

Since `PERCENT` argument is not supported by Snowflake it is being removed from the `TOP` clause, that’s why the result of executing the query in Snowflake is not equivalent to Transact-SQL.

#### TOP WITH TIES[¶](#top-with-ties "Link to this heading")

##### Transact-SQL[¶](#id21 "Link to this heading")

##### Query[¶](#id22 "Link to this heading")

```
 SELECT TOP(50)PERCENT WITH TIES Model, Color, Price FROM Cars ORDER BY Price;
```

Copy

##### Result[¶](#id23 "Link to this heading")

| Model | Color | Price |
| --- | --- | --- |
| van | blue | 8000.0000 |
| sub | green | 8000.0000 |
| sedan | red | 10000.0000 |

##### Snowflake[¶](#id24 "Link to this heading")

##### Query[¶](#id25 "Link to this heading")

```
 SELECT
 TOP 50 !!!RESOLVE EWI!!! /*** SSC-EWI-0040 - THE 'TOP PERCENT AND WITH TIES' CLAUSE IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
  Model,
  Color,
  Price
 FROM
  Cars
 ORDER BY Price;
```

Copy

##### Result[¶](#id26 "Link to this heading")

| MODEL | COLOR | PRICE |
| --- | --- | --- |
| sub | green | 8,000 |
| van | blue | 8,000 |
| sedan | red | 10,000 |
| convertible | blue | 15,000 |
| coupe | red | 20,000 |

Warning

Since `WITH TIES` argument is not supported by Snowflake it is being removed from the `TOP` clause, that’s why the result of executing the query in Snowflake is not equivalent to Transact-SQL.

### Known Issues[¶](#id27 "Link to this heading")

#### 1. PERCENT argument is not supported by Snowflake[¶](#percent-argument-is-not-supported-by-snowflake "Link to this heading")

Since the `PERCENT` argument is not supported by Snowflake it is being removed from the `TOP` clause and a warning is being added. Functional equivalence mismatches in the results could happen.

##### 2. WITH TIES argument is not supported by Snowflake[¶](#with-ties-argument-is-not-supported-by-snowflake "Link to this heading")

Since the `WITH TIES` argument is not supported by Snowflake it is being removed from the `TOP` clause and a warning is being added. Functional equivalence mismatches in the results could happen.

### Related EWIs[¶](#id28 "Link to this heading")

1. [SSC-EWI-0040](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0040): Statement Not Supported.

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
2. [TOP](#top)