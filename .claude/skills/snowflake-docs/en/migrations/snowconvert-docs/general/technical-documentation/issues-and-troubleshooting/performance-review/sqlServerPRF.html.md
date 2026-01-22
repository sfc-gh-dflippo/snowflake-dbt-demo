---
auto_generated: true
description: SQL Server
last_scraped: '2026-01-14T16:55:36.089456+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/performance-review/sqlServerPRF.html
title: SnowConvert AI - SQL Server-Azure Synapse Performance Review Messages | Snowflake
  Documentation
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

          + [About](../../../about.md)
          + [Getting Started](../../../getting-started/README.md)
          + [Terms And Conditions](../../../terms-and-conditions/README.md)
          + [Release Notes](../../../release-notes/release-notes/README.md)
          + User Guide

            + [SnowConvert AI](../../../user-guide/snowconvert/README.md)
            + [Project Creation](../../../user-guide/project-creation.md)
            + [Extraction](../../../user-guide/extraction.md)
            + [Deployment](../../../user-guide/deployment.md)
            + [Data Migration](../../../user-guide/data-migration.md)
            + [Data Validation](../../../user-guide/data-validation.md)
            + [Power BI Repointing](../../../user-guide/power-bi-repointing-general.md)
            + [ETL Migration](../../../user-guide/etl-migration-replatform.md)
          + [Technical Documentation](../../README.md)

            - [Considerations](../../considerations/README.md)
            - [Issues And Troubleshooting](../README.md)

              * [Conversion Issues](../conversion-issues/README.md)
              * [Functional Difference](../functional-difference/README.md)
              * [Out Of Scope](../out-of-scope/README.md)
              * [Performance Review](README.md)

                + [General](generalPRF.md)
                + [SQL Server-Azure Synapse](sqlServerPRF.md)
            - Function References

              - [SnowConvert AI Udfs](../../function-references/snowconvert-udfs.md)
              - [Teradata](../../function-references/teradata/README.md)
              - [Oracle](../../function-references/oracle/README.md)
              - [Shared](../../function-references/shared/README.md)
              - [SQL Server](../../function-references/sql-server/README.md)
          + [Contact Us](../../../contact-us.md)
          + Others

            + [Using SnowConvert AI In A Ubuntu Docker Image](../../../others/using-snowconvert-in-a-ubuntu-docker-image.md)
          + [Frequently Asked Questions (FAQ)](../../../frequently-asked-questions-faq.md)")
        + Translation References

          + [General](../../../../translation-references/general/README.md)
          + [Teradata](../../../../translation-references/teradata/README.md)
          + [Oracle](../../../../translation-references/oracle/README.md)
          + [SQL Server-Azure Synapse](../../../../translation-references/transact/README.md)
          + [Sybase IQ](../../../../translation-references/sybase/README.md)
          + [Hive-Spark-Databricks SQL](../../../../translation-references/hive/README.md)
          + [Redshift](../../../../translation-references/redshift/README.md)
          + [PostgreSQL-Greenplum-Netezza](../../../../translation-references/postgres/README.md)
          + [BigQuery](../../../../translation-references/bigquery/README.md)
          + [Vertica](../../../../translation-references/vertica/README.md)
          + [IBM DB2](../../../../translation-references/db2/README.md)
          + [SSIS](../../../../translation-references/ssis/README.md)
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

[Guides](../../../../../../guides/README.md)[Migrations](../../../../../README.md)Tools[SnowConvert AI](../../../../overview.md)General[Technical Documentation](../../README.md)[Issues And Troubleshooting](../README.md)[Performance Review](README.md)SQL Server-Azure Synapse

# SnowConvert AI - SQL Server-Azure Synapse Performance Review Messages[¶](#snowconvert-ai-sql-server-azure-synapse-performance-review-messages "Link to this heading")

Applies to

* SQL Server
* Azure Synapse Analytics

## SSC-PRF-TS0001[¶](#ssc-prf-ts0001 "Link to this heading")

Performance warning - recursion for CTE not checked. Might require a recursive keyword.

### Description[¶](#description "Link to this heading")

This warning appears when SnowConvert AI detects a Common Table Expression (CTE) but has not verified whether the CTE contains recursive operations in its query definition.

Snowflake SQL requires the RECURSIVE keyword for recursive Common Table Expressions (CTEs). Currently, SnowConvert AI does not automatically detect recursive queries to determine whether the RECURSIVE keyword should be included. This warning notifies you that you may need to manually add the RECURSIVE keyword for recursive CTEs.

Support for this validation may be added in future releases as requirements evolve.

### Code Example[¶](#code-example "Link to this heading")

#### Input Code:[¶](#input-code "Link to this heading")

```
 WITH Sales_CTE (SalesPersonID, NumberOfOrders)  
AS  
(  
    SELECT SalesPersonID, 2  
    FROM Sales.SalesOrderHeader  
    WHERE SalesPersonID IS NOT NULL  
    GROUP BY SalesPersonID  
)  
SELECT 2 AS "Average Sales Per Person"  
FROM Sales_CTE;
```

Copy

#### Generated Code:[¶](#generated-code "Link to this heading")

```
 --** SSC-PRF-TS0001 - PERFORMANCE WARNING - RECURSION FOR CTE NOT CHECKED. MIGHT REQUIRE RECURSIVE KEYWORD **
WITH Sales_CTE (
    SalesPersonID,
    NumberOfOrders
) AS
(
    SELECT
        SalesPersonID, 2
    FROM
        Sales.SalesOrderHeader
    WHERE
        SalesPersonID IS NOT NULL
    GROUP BY
        SalesPersonID
)
SELECT 2 AS "Average Sales Per Person"
FROM
    Sales_CTE;
```

Copy

### Best Practices[¶](#best-practices "Link to this heading")

* The RECURSIVE keyword is optional and won’t affect your query results. However, it may influence how Snowflake allocates resources during execution. We recommend reviewing Snowflake’s CTE documentation and contacting us if you’d like automatic RECURSIVE keyword addition for compatible CTE queries.
* For additional assistance, please email us at [snowconvert-support@snowflake.com](mailto:snowconvert-support%40snowflake.com)

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

1. [SSC-PRF-TS0001](#ssc-prf-ts0001)