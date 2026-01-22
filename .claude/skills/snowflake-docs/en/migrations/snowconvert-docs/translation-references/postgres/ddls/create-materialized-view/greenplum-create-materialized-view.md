---
auto_generated: true
description: Translation from Greenplum to Snowflake
last_scraped: '2026-01-14T16:53:31.784738+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/postgres/ddls/create-materialized-view/greenplum-create-materialized-view
title: SnowConvert AI - Greenplum - CREATE MATERIALIZED VIEW | Snowflake Documentation
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

[Guides](../../../../../../guides/README.md)[Migrations](../../../../../README.md)Tools[SnowConvert AI](../../../../overview.md)Translation References[PostgreSQL-Greenplum-Netezza](../../README.md)DDLs[CREATE MATERIALIZED VIEW](postgresql-create-materialized-view.md)Greenplum

# SnowConvert AI - Greenplum - CREATE MATERIALIZED VIEW[¶](#snowconvert-ai-greenplum-create-materialized-view "Link to this heading")

Translation from Greenplum to Snowflake

## Description[¶](#description "Link to this heading")

This section explains features exclusive to Greenplum.

For more information, please refer to [`CREATE MATERIALIZE VIEW`](https://techdocs.broadcom.com/us/en/vmware-tanzu/data-solutions/tanzu-greenplum/7/greenplum-database/ref_guide-sql_commands-CREATE_MATERIALIZED_VIEW.html) the documentation.

## Grammar Syntax[¶](#grammar-syntax "Link to this heading")

```
CREATE MATERIALIZED VIEW <table_name>
AS <query>
[
    DISTRIBUTED { 
        BY <column> [<opclass>], [ ... ] | RANDOMLY | REPLICATED 
        }
]
```

Copy

## DISTRIBUTED BY[¶](#distributed-by "Link to this heading")

Hint

This syntax is translated to its most equivalent form in Snowflake.

The DISTRIBUTED BY clause in Greenplum controls how data is physically distributed across the system’s segments. Meanwhile, CLUSTER BY is a subset of columns in a dynamic table (or expressions on a dynamic table) explicitly designated to co-locate the data in the table in the same micro-partitions. While they operate at different architectural levels, they aim to improve query performance by distributing data efficiently.

### Grammar Syntax[¶](#id1 "Link to this heading")

```
DISTRIBUTED BY ( <column> [<opclass>] [, ... ] )
```

Copy

### Sample Source[¶](#sample-source "Link to this heading")

Input Code:

#### Greenplum[¶](#greenplum "Link to this heading")

```
CREATE MATERIALIZED VIEW product_summary AS
SELECT
    category,
    COUNT(*) AS total_products,
    MAX(price) AS max_price
FROM products
GROUP BY category
DISTRIBUTED BY (category);
```

Copy

Output Code:

##### Snowflake[¶](#snowflake "Link to this heading")

```
CREATE OR REPLACE DYNAMIC TABLE product_summary
--** SSC-FDM-0031 - DYNAMIC TABLE REQUIRED PARAMETERS SET BY DEFAULT **
TARGET_LAG='1 day'
WAREHOUSE=UPDATE_DUMMY_WAREHOUSE
--** SSC-FDM-GP0001 - THE PERFORMANCE OF THE CLUSTER BY MAY VARY COMPARED TO THE PERFORMANCE OF DISTRIBUTED BY **
CLUSTER BY (category)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "greenplum",  "convertedOn": "04/24/2025",  "domain": "test" }}'
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

## DISTRIBUTED RANDOMLY - REPLICATED[¶](#distributed-randomly-replicated "Link to this heading")

Note

This syntax is not needed in Snowflake.

The DISTRIBUTED REPLICATED or DISTRIBUTED RANDOMLY clause in Greenplum controls how data is physically distributed across the system’s segments. As Snowflake automatically handles data storage, these options will be removed in the migration.

## Related EWIs[¶](#related-ewis "Link to this heading")

1. [SSC-FDM-GP0001](../../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/greenplumFDM.html#ssc-fdm-gp0001): The performance of the CLUSTER BY may vary compared to the performance of Distributed By.

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
3. [DISTRIBUTED BY](#distributed-by)
4. [DISTRIBUTED RANDOMLY - REPLICATED](#distributed-randomly-replicated)
5. [Related EWIs](#related-ewis)