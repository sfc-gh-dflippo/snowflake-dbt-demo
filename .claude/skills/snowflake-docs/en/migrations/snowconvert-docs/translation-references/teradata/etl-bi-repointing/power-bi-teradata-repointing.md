---
auto_generated: true
description: The Power BI repointing is a feature that provides an easy way to redefine
  the connections from the M language in the Power Query Editor. This means that the
  connection parameters will be redefined to
last_scraped: '2026-01-14T16:53:43.921585+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/teradata/etl-bi-repointing/power-bi-teradata-repointing
title: SnowConvert AI - Teradata - Power BI Repointing | Snowflake Documentation
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
            - [Sql Translation Reference](../sql-translation-reference/README.md)
            - [SQL to JavaScript (Procedures)](../teradata-to-javascript-translation-reference.md)")
            - [SQL to Snowflake Scripting (Procedures)](../teradata-to-snowflake-scripting-translation-reference.md)")
            - [Scripts To Python](../scripts-to-python/README.md)
            - [Scripts to Snowflake SQL](../scripts-to-snowflake-sql-translation-reference/README.md)
            - ETL And BI Repointing

              - [Power BI Teradata Repointing](power-bi-teradata-repointing.md)
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

[Guides](../../../../../guides/README.md)[Migrations](../../../../README.md)Tools[SnowConvert AI](../../../overview.md)Translation References[Teradata](../README.md)ETL And BI RepointingPower BI Teradata Repointing

# SnowConvert AI - Teradata - Power BI Repointing[¶](#snowconvert-ai-teradata-power-bi-repointing "Link to this heading")

## Description[¶](#description "Link to this heading")

The Power BI repointing is a feature that provides an easy way to redefine the connections from the [M language in the Power Query Editor](https://learn.microsoft.com/en-us/powerquery-m/). This means that the connection parameters will be redefined to point to the Snowflake migration database context. For Teradata, the method in [M Language](https://learn.microsoft.com/en-us/powerquery-m/) that defined the connection is `Teradata.Database(...)`. In Snowflake, there is a connector that depends on some other parameters and the main connection is defined by `Snowflake.Database(...)` method. In addition, there is a limited support to `ODBC.Query` connector only for Teradata as a source languge in the migration. This means that the source connection parameters (of Teradata connections) will be redefine to point to the Snowflake migration database context.

## Source Pattern Samples[¶](#source-pattern-samples "Link to this heading")

### Entity Repointing Case: Table[¶](#entity-repointing-case-table "Link to this heading")

This case refers to connections that do not contain embedded SQL. This means that the user has established a connection from Power BI to a table.

**Teradata Connection in the Power Query Editor**

```
let
    Source = Teradata.Database("the_teradata_server", [HierarchicalNavigation=true]),
    databaseTest = Source{[Schema="databaseTest"]}[Data],
    employees1 = databaseTest{[Name="employees"]}[Data]
in
    employees1
```

Copy

**Snowflake Connection in the Power Query Editor**

```
let
    Source = Snowflake.Databases(SF_SERVER_LINK, SF_WAREHOUSE_NAME),
    SourceSfDb = Source{[Name=SF_DB_NAME, Kind="Database"]}[Data],
    SourceSfSchema = SourceSfDb{[Name="databaseTest", Kind="Schema"]}[Data],
    SourceSfTbl = SourceSfSchema{[Name="EMPLOYEES", Kind="Table"]}[Data],
    Employees1 = Table.RenameColumns(SourceSfTbl, {{ "EMPLOYEEID", "EmployeeID"}, { "FIRSTNAME", "FirstName"}, { "LASTNAME", "LastName"}, { "HIREDATE", "HireDate"}, { "SALARY", "Salary"}, { "DEPARTMENTID", "DepartmentID"}})
in
    Employees1
```

Copy

### Entity Repointing Case: View[¶](#entity-repointing-case-view "Link to this heading")

This case refers to connections that do not contain embedded SQL. This means that the user has established a connection from Power BI to a view.

**Teradata Connection in the Power Query Editor**

```
let
    Source = Teradata.Database("the_teradata_server", [HierarchicalNavigation=true]),
    databaseTest = Source{[Schema="databaseTest"]}[Data],
    EmployeeSalaryBonusView1 = databaseTest{[Name="EmployeeSalaryBonusView"]}[Data]
in
    EmployeeSalaryBonusView1
```

Copy

**Snowflake Connection in the Power Query Editor**

```
let
    Source = Snowflake.Databases(SF_SERVER_LINK, SF_WAREHOUSE_NAME),
    SourceSfDb = Source{[Name=SF_DB_NAME, Kind="Database"]}[Data],
    SourceSfSchema = SourceSfDb{[Name="databaseTest", Kind="Schema"]}[Data],
    SourceSfTbl = SourceSfSchema{[Name="EMPLOYEESALARYBONUSVIEW", Kind="Table"]}[Data],
    EmployeeSalaryBonusView1 = Table.RenameColumns(SourceSfTbl, {{ "FIRSTNAME", "FirstName"}, { "LASTNAME", "LastName"}, { "HIREDATE", "HireDate"}})
in
    EmployeeSalaryBonusView1
```

Copy

### Embedded SQL Case[¶](#embedded-sql-case "Link to this heading")

This case refers to connections that contains embedded SQL inside of them. This sample show a simple query but SnowConvert AI covers a range of more larger scenarios. Besides, there may be warning messages knows as EWI- PRF - FDM depending on the migrated query. This will help the user identifies patterns that needs extra attention.

**Teradata Connection in the Power Query Editor**

```
let
    Source = Teradata.Database("the_teradata_server", [HierarchicalNavigation=true, Query="SELECT *#(lf)FROM databaseTest.employees"])
in
    Source
```

Copy

**Snowflake Connection in the Power Query Editor**

```
let
    SfSource = Value.NativeQuery(Snowflake.Databases(SF_SERVER_LINK,SF_WAREHOUSE_NAME,[Implementation="2.0"]){[Name=SF_DB_NAME]}[Data], "SELECT * FROM databaseTest.employees", null, [EnableFolding=true]),
    Source = Table.RenameColumns(SfSource, {{ "EMPLOYEEID", "EmployeeID"}, { "FIRSTNAME", "FirstName"}, { "LASTNAME", "LastName"}, { "HIREDATE", "HireDate"}, { "SALARY", "Salary"}, { "DEPARTMENTID", "DepartmentID"}})
in
    Source
```

Copy

### ODBC.Query Case[¶](#odbc-query-case "Link to this heading")

At the moment it is supported only `ODBC.Query` connector. Other connectors as `ODBC.DataSource` are not supported.

This case refers to connections that contains embedded SQL inside of an `ODBC.Query` connector. Notice that all connections with `ODBC.Query` will be taken as Teradata source when migrating Teradata. Please, be aware of your report connection definitions.

**Teradata Connection in the Power Query Editor**

```
let
  Source = Odbc.Query("dsn=TERADATA_TEST", "SELECT * FROM TEST_TABLE")
in
  Source
```

Copy

**Snowflake Connection in the Power Query Editor**

```
let
   Source = Value.NativeQuery(Snowflake.Databases(SF_SERVER_LINK,SF_WAREHOUSE_NAME,[Implementation="2.0"]){[Name=SF_DB_NAME]}[Data], "SELECT * FROM TEST_TABLE", null, [EnableFolding=true])
in
   Source
```

Copy

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
2. [Source Pattern Samples](#source-pattern-samples)