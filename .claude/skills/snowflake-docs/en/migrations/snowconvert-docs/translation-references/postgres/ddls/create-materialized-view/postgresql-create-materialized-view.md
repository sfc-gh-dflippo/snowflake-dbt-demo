---
auto_generated: true
description: Translation reference to convert PostgreSQL Materialized View to Snowflake
  Dynamic Table
last_scraped: '2026-01-14T16:53:32.212826+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/postgres/ddls/create-materialized-view/postgresql-create-materialized-view
title: SnowConvert AI - PostgreSQL - CREATE MATERIALIZED VIEW | Snowflake Documentation
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

      * [SnowConvert AI](../../../../overview.md)

        + General

          + [About](../../../../general/about.md)
          + [Getting Started](../../../../general/getting-started/README.md)
          + [Terms And Conditions](../../../../general/terms-and-conditions/README.md)
          + [Release Notes](../../../../general/release-notes/release-notes/README.md)
          + User Guide

            + [SnowConvert AI](../../../../general/user-guide/snowconvert/README.md)
            + [Project Creation](../../../../general/user-guide/project-creation.md)
            + [Extraction](../../../../general/user-guide/extraction.md)
            + [Deployment](../../../../general/user-guide/deployment.md)
            + [Data Migration](../../../../general/user-guide/data-migration.md)
            + [Data Validation](../../../../general/user-guide/data-validation.md)
            + [Power BI Repointing](../../../../general/user-guide/power-bi-repointing-general.md)
            + [ETL Migration](../../../../general/user-guide/etl-migration-replatform.md)
          + [Technical Documentation](../../../../general/technical-documentation/README.md)
          + [Contact Us](../../../../general/contact-us.md)
          + Others

            + [Using SnowConvert AI In A Ubuntu Docker Image](../../../../general/others/using-snowconvert-in-a-ubuntu-docker-image.md)
          + [Frequently Asked Questions (FAQ)](../../../../general/frequently-asked-questions-faq.md)")
        + Translation References

          + [General](../../../general/README.md)
          + [Teradata](../../../teradata/README.md)
          + [Oracle](../../../oracle/README.md)
          + [SQL Server-Azure Synapse](../../../transact/README.md)
          + [Sybase IQ](../../../sybase/README.md)
          + [Hive-Spark-Databricks SQL](../../../hive/README.md)
          + [Redshift](../../../redshift/README.md)
          + [PostgreSQL-Greenplum-Netezza](../../README.md)

            - [Built-in Functions](../../postgresql-built-in-functions.md)
            - [Data Types](../../data-types/postgresql-data-types.md)
            - [String Comparison](../../postgresql-string-comparison.md)
            - DDLs

              - [CREATE MATERIALIZED VIEW](postgresql-create-materialized-view.md)

                * [Greenplum](greenplum-create-materialized-view.md)
              - [CREATE TABLE](../create-table/postgresql-create-table.md)
              - [CREATE VIEW](../postgresql-create-view.md)
            - [Expressions](../../postgresql-expressions.md)
            - [Interactive Terminal](../../postgresql-interactive-terminal.md)
            - ETL And BI Repointing

              - [Power BI PostgreSQL Repointing](../../etl-bi-repointing/power-bi-postgres-repointing.md)
          + [BigQuery](../../../bigquery/README.md)
          + [Vertica](../../../vertica/README.md)
          + [IBM DB2](../../../db2/README.md)
          + [SSIS](../../../ssis/README.md)
        + [Migration Assistant](../../../../migration-assistant/README.md)
        + [Data Validation CLI](../../../../data-validation-cli/index.md)
        + [AI Verification](../../../../snowconvert-ai-verification.md)
      * [Snowpark Migration Accelerator](../../../../../sma-docs/README.md)
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

[Guides](../../../../../../guides/README.md)[Migrations](../../../../../README.md)Tools[SnowConvert AI](../../../../overview.md)Translation References[PostgreSQL-Greenplum-Netezza](../../README.md)DDLsCREATE MATERIALIZED VIEW

# SnowConvert AI - PostgreSQL - CREATE MATERIALIZED VIEW[¶](#snowconvert-ai-postgresql-create-materialized-view "Link to this heading")

Translation reference to convert PostgreSQL Materialized View to Snowflake Dynamic Table

## Applies to[¶](#applies-to "Link to this heading")

* PostgreSQL
* Greenplum
* Netezza

## Description[¶](#description "Link to this heading")

In SnowConvert AI, Materialized Views are transformed into Snowflake Dynamic Tables. To properly configure Dynamic Tables, two essential parameters must be defined: TARGET\_LAG and WAREHOUSE. If these parameters are left unspecified in the configuration options, SnowConvert AI will default to preassigned values during the conversion, as demonstrated in the example below.

## Grammar Syntax[¶](#grammar-syntax "Link to this heading")

```
CREATE MATERIALIZED VIEW [ IF  NOT EXISTS ] <table_name>
    [ (<column_name> [, ...] ) ]
    [ USING <method> ]
    [ WITH ( <storage_parameter> [= <value>] [, ... ] ) ]
    [ TABLESPACE <tablespace_name> ]
    AS <query>
    [ WITH [ NO ] DATA ]
```

Copy

## Code Examples[¶](#code-examples "Link to this heading")

### Simple Case[¶](#simple-case "Link to this heading")

Input Code:

#### PostgreSQL[¶](#postgresql "Link to this heading")

```
CREATE MATERIALIZED VIEW product_summary AS
SELECT
    category,
    COUNT(*) AS total_products,
    MAX(price) AS max_price
FROM products
GROUP BY category;
```

Copy

Output Code:

##### Snowflake[¶](#snowflake "Link to this heading")

```
CREATE OR REPLACE DYNAMIC TABLE product_summary
--** SSC-FDM-0031 - DYNAMIC TABLE REQUIRED PARAMETERS SET BY DEFAULT **
TARGET_LAG='1 day'
WAREHOUSE=UPDATE_DUMMY_WAREHOUSE
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "postgresql",  "convertedOn": "05/14/2025",  "domain": "no-domain-provided" }}'
AS
SELECT
    category,
    COUNT(*) AS total_products,
    MAX(price) AS max_price
FROM
    products
GROUP BY category;
```

Copy

### IF NOT EXISTS[¶](#if-not-exists "Link to this heading")

Hint

This syntax is fully supported in Snowflake.

This clause has been removed during the migration from PostgreSQL to Snowflake.

### USING, TABLESPACE, and WITH[¶](#using-tablespace-and-with "Link to this heading")

Note

This syntax is not needed in Snowflake.

These clauses are removed during the conversion process. In PostgreSQL, they are used to further customize data storage manually. This is something that Snowflake handles automatically (micro partitions), and it is typically not a concern.

## Related EWIs[¶](#related-ewis "Link to this heading")

1. [SSC-FDM-0031](../../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0031): Dynamic Table required parameters set by default

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

1. [Applies to](#applies-to)
2. [Description](#description)
3. [Grammar Syntax](#grammar-syntax)
4. [Code Examples](#code-examples)
5. [Related EWIs](#related-ewis)