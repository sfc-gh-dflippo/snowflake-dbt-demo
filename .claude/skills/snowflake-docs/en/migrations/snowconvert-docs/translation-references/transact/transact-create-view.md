---
auto_generated: true
description: SQL Server
last_scraped: '2026-01-14T16:54:06.201448+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/transact/transact-create-view
title: SnowConvert AI - SQL Server-Azure Synapse - Views | Snowflake Documentation
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)Translation References[SQL Server-Azure Synapse](README.md)Data Definition LanguageCREATE VIEW

# SnowConvert AI - SQL Server-Azure Synapse - Views[¶](#snowconvert-ai-sql-server-azure-synapse-views "Link to this heading")

Applies to

* SQL Server
* Azure Synapse Analytics

Note

Some parts in the output code are omitted for clarity reasons.

In this section, we will check the transformation for the create view.

## Sample Source Patterns[¶](#sample-source-patterns "Link to this heading")

### SIMPLE CREATE VIEW[¶](#simple-create-view "Link to this heading")

The following example shows a transformation for a simple `CREATE VIEW` statement.

#### Transact[¶](#transact "Link to this heading")

```
CREATE VIEW VIEWNAME
AS
SELECT AValue from ATable;
```

Copy

##### Snowflake[¶](#snowflake "Link to this heading")

```
CREATE OR REPLACE VIEW VIEWNAME
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
AS
SELECT
AValue
from
ATable;
```

Copy

## CREATE OR ALTER VIEW[¶](#create-or-alter-view "Link to this heading")

The **CREATE OR ALTER** definition used in SqlServer is transformed to **CREATE OR REPLACE** in Snowflake.

### Transact[¶](#id1 "Link to this heading")

```
CREATE OR ALTER VIEW VIEWNAME
AS
SELECT AValue from ATable;
```

Copy

#### Snowflake[¶](#id2 "Link to this heading")

```
CREATE OR REPLACE VIEW VIEWNAME
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
AS
SELECT
AValue
from
ATable;
```

Copy

## CREATE VIEW WITH[¶](#create-view-with "Link to this heading")

In this type of View, after the name of the View, the following clauses can come

* `WITH ENCRYPTION`
* `WITH SCHEMABINDING`
* `WITH VIEW_METADATA`

Warning

Notice that the above clauses are removed from the translation. because are not relevant in Snowflake syntax.

### Transact[¶](#id3 "Link to this heading")

```
CREATE OR ALTER VIEW VIEWNAME
WITH ENCRYPTION  
AS
SELECT AValue from ATable;
```

Copy

### Snowflake[¶](#id4 "Link to this heading")

```
CREATE OR REPLACE VIEW VIEWNAME
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
AS
SELECT
AValue
from
ATable;
```

Copy

## CREATE VIEW AS SELECT WITH CHECK OPTION[¶](#create-view-as-select-with-check-option "Link to this heading")

In this type of View, the clause **`WITH CHECK OPTION`** comes after the end of the Select statement used in the Create View.

Warning

Notice that `WITH CHECK OPTION`is removed from the translation, because is not relevant in Snowflake syntax.

### Transact[¶](#id5 "Link to this heading")

```
CREATE OR ALTER VIEW VIEWNAME
AS
SELECT AValue from ATable
WITH CHECK OPTION;
```

Copy

### Snowflake[¶](#id6 "Link to this heading")

```
CREATE OR REPLACE VIEW VIEWNAME
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
AS
SELECT
AValue
from
ATable;
```

Copy

## CREATE VIEW AS COMMON TABLE EXPRESSION[¶](#create-view-as-common-table-expression "Link to this heading")

Common Table Expressions must be used to retrieve the data:

### Transact[¶](#id7 "Link to this heading")

```
CREATE VIEW EMPLOYEEIDVIEW
AS
WITH CTE AS ( SELECT NationalIDNumber from [HumanResources].[Employee] 
UNION ALL 
SELECT BusinessEntityID FROM [HumanResources].[EmployeeDepartmentHistory] )
SELECT * FROM MyCTE;
```

Copy

### Snowflake[¶](#id8 "Link to this heading")

```
CREATE OR REPLACE VIEW EMPLOYEEIDVIEW
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
AS
--** SSC-PRF-TS0001 - PERFORMANCE WARNING - RECURSION FOR CTE NOT CHECKED. MIGHT REQUIRE RECURSIVE KEYWORD **
WITH CTE AS ( SELECT
NationalIDNumber
from
HumanResources.Employee
UNION ALL
SELECT
BusinessEntityID
FROM
HumanResources.EmployeeDepartmentHistory
)
SELECT
*
FROM
MyCTE;
```

Copy

## UNSUPPORTED SCENARIOS[¶](#unsupported-scenarios "Link to this heading")

Common table expressions with Update, Insert or Delete statements will be commented out because they are not supported in Snowflake and SQLServer.

In the case where an invalid CTE is added to the view, this will be completely commented out.

```
 --!!!RESOLVE EWI!!! /*** SSC-EWI-0021 - COMMON TABLE EXPRESSION IN VIEW NOT SUPPORTED ***/!!!
--CREATE OR REPLACE VIEW PUBLIC.EmployeeInsertVew
--AS
--WITH MyCTE AS ( SELECT
--NationalIDNumber
--from
--HumanResources.Employee
--UNION ALL
--SELECT
--BusinessEntityID
--FROM
--HumanResources.EmployeeDepartmentHistory
--)
--INSERT INTO PUBLIC.Dummy
```

Copy

### FINAL SAMPLE[¶](#final-sample "Link to this heading")

Let’s see a final sample, let’s put together all the cases that we have seen so far and see how the transformation would be

#### Transact[¶](#id9 "Link to this heading")

```
CREATE OR ALTER VIEW VIEWNAME
WITH ENCRYPTION  
AS  
Select AValue from ATable
WITH CHECK OPTION;
```

Copy

##### Snowflake[¶](#id10 "Link to this heading")

```
CREATE OR REPLACE VIEW VIEWNAME
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
AS
Select
AValue
from
ATable;
```

Copy

As you can see, we changed the **OR ALTER** with **OR REPLACE** and we removed the clause **WITH ENCRYPTION** that comes after the view name and the **WITH CHECK OPTION** that comes after the Select.

### Related EWIs[¶](#related-ewis "Link to this heading")

1. [SSC-PRF-TS0001](../../general/technical-documentation/issues-and-troubleshooting/performance-review/sqlServerPRF.html#ssc-prf-ts0001): Performance warning - recursion for CTE not checked. Might require a recursive keyword.

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

1. [Sample Source Patterns](#sample-source-patterns)
2. [CREATE OR ALTER VIEW](#create-or-alter-view)
3. [CREATE VIEW WITH](#create-view-with)
4. [CREATE VIEW AS SELECT WITH CHECK OPTION](#create-view-as-select-with-check-option)
5. [CREATE VIEW AS COMMON TABLE EXPRESSION](#create-view-as-common-table-expression)
6. [UNSUPPORTED SCENARIOS](#unsupported-scenarios)