---
auto_generated: true
description: Translation reference to convert Materialized View to Snowflake Dynamic
  Table
last_scraped: '2026-01-14T16:54:03.908730+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/transact/transact-create-materialized-view
title: SnowConvert AI - SQL Server-Azure Synapse - Materialized View | Snowflake Documentation
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)Translation References[SQL Server-Azure Synapse](README.md)Data Definition LanguageCREATE MATERIALIZED VIEW

# SnowConvert AI - SQL Server-Azure Synapse - Materialized View[¶](#snowconvert-ai-sql-server-azure-synapse-materialized-view "Link to this heading")

Translation reference to convert Materialized View to Snowflake Dynamic Table

Applies to

* Azure Synapse Analytics

## Description[¶](#description "Link to this heading")

In SnowConvert AI, Materialized Views are transformed into Snowflake Dynamic Tables. To properly configure Dynamic Tables, two essential parameters must be defined: TARGET\_LAG and WAREHOUSE. If these parameters are left unspecified in the configuration options, SnowConvert AI will default to preassigned values during the conversion, as demonstrated in the example below.

For more information on Materialized Views, click [here](https://learn.microsoft.com/en-us/sql/t-sql/statements/create-materialized-view-as-select-transact-sql?view=azure-sqldw-latest).

For details on the necessary parameters for Dynamic Tables, click [here](https://docs.snowflake.com/en/sql-reference/sql/create-dynamic-table).

## Sample Source Patterns[¶](#sample-source-patterns "Link to this heading")

### SQL Server[¶](#sql-server "Link to this heading")

```
CREATE MATERIALIZED VIEW sales_total
AS
SELECT SUM(amount) AS total_sales
FROM sales;
```

Copy

### Snowflake[¶](#snowflake "Link to this heading")

```
 CREATE OR REPLACE DYNAMIC TABLE sales_total
--** SSC-FDM-0031 - DYNAMIC TABLE REQUIRED PARAMETERS SET BY DEFAULT **
TARGET_LAG='1 day'
WAREHOUSE=UPDATE_DUMMY_WAREHOUSE
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
AS
SELECT SUM(amount) AS total_sales
FROM
sales;
```

Copy

## Related EWIs[¶](#related-ewis "Link to this heading")

1. [SSC-FMD-0031](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0031): Dynamic Table required parameters set by default

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
2. [Sample Source Patterns](#sample-source-patterns)
3. [Related EWIs](#related-ewis)