---
auto_generated: true
description: SnowConvert AI is a specialized tool that accurately converts source
  code from various platforms to Snowflake exclusively.
last_scraped: '2026-01-14T16:51:08.052665+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/general/about
title: SnowConvert AI - About | Snowflake Documentation
---

1. [Overview](../../../guides/README.md)
2. [Snowflake Horizon Catalog](../../../user-guide/snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../../../guides/overview-connecting.md)
6. [Virtual warehouses](../../../user-guide/warehouses.md)
7. [Databases, Tables, & Views](../../../guides/overview-db.md)
8. [Data types](../../../data-types.md)
10. Data Integration

    - [Snowflake Openflow](../../../user-guide/data-integration/openflow/about.md)
    - Apache Iceberg™

      - [Apache Iceberg™ Tables](../../../user-guide/tables-iceberg.md)
      - [Snowflake Open Catalog](../../../user-guide/opencatalog/overview.md)
11. Data engineering

    - [Data loading](../../../guides/overview-loading-data.md)
    - [Dynamic Tables](../../../user-guide/dynamic-tables-about.md)
    - [Streams and Tasks](../../../user-guide/data-pipelines-intro.md)
    - [dbt Projects on Snowflake](../../../user-guide/data-engineering/dbt-projects-on-snowflake.md)
    - [Data Unloading](../../../guides/overview-unloading-data.md)
12. [Storage Lifecycle Policies](../../../user-guide/storage-management/storage-lifecycle-policies.md)
13. [Migrations](../../README.md)

    * Tools

      * [SnowConvert AI](../overview.md)

        + General

          + [About](about.md)
          + [Getting Started](getting-started/README.md)
          + [Terms And Conditions](terms-and-conditions/README.md)
          + [Release Notes](release-notes/release-notes/README.md)
          + User Guide

            + [SnowConvert AI](user-guide/snowconvert/README.md)
            + [Project Creation](user-guide/project-creation.md)
            + [Extraction](user-guide/extraction.md)
            + [Deployment](user-guide/deployment.md)
            + [Data Migration](user-guide/data-migration.md)
            + [Data Validation](user-guide/data-validation.md)
            + [Power BI Repointing](user-guide/power-bi-repointing-general.md)
            + [ETL Migration](user-guide/etl-migration-replatform.md)
          + [Technical Documentation](technical-documentation/README.md)
          + [Contact Us](contact-us.md)
          + Others

            + [Using SnowConvert AI In A Ubuntu Docker Image](others/using-snowconvert-in-a-ubuntu-docker-image.md)
          + [Frequently Asked Questions (FAQ)](frequently-asked-questions-faq.md)")
        + Translation References

          + [General](../translation-references/general/README.md)
          + [Teradata](../translation-references/teradata/README.md)
          + [Oracle](../translation-references/oracle/README.md)
          + [SQL Server-Azure Synapse](../translation-references/transact/README.md)
          + [Sybase IQ](../translation-references/sybase/README.md)
          + [Hive-Spark-Databricks SQL](../translation-references/hive/README.md)
          + [Redshift](../translation-references/redshift/README.md)
          + [PostgreSQL-Greenplum-Netezza](../translation-references/postgres/README.md)
          + [BigQuery](../translation-references/bigquery/README.md)
          + [Vertica](../translation-references/vertica/README.md)
          + [IBM DB2](../translation-references/db2/README.md)
          + [SSIS](../translation-references/ssis/README.md)
        + [Migration Assistant](../migration-assistant/README.md)
        + [Data Validation CLI](../data-validation-cli/index.md)
        + [AI Verification](../snowconvert-ai-verification.md)
      * [Snowpark Migration Accelerator](../../sma-docs/README.md)
    * Guides

      * [Teradata](../../guides/teradata.md)
      * [Databricks](../../guides/databricks.md)
      * [SQL Server](../../guides/sqlserver.md)
      * [Amazon Redshift](../../guides/redshift.md)
      * [Oracle](../../guides/oracle.md)
      * [Azure Synapse](../../guides/azuresynapse.md)
15. [Queries](../../../guides/overview-queries.md)
16. [Listings](../../../collaboration/collaboration-listings-about.md)
17. [Collaboration](../../../guides/overview-sharing.md)
19. [Snowflake AI & ML](../../../guides/overview-ai-features.md)
21. [Snowflake Postgres](../../../user-guide/snowflake-postgres/about.md)
23. [Alerts & Notifications](../../../guides/overview-alerts.md)
25. [Security](../../../guides/overview-secure.md)
26. [Data Governance](../../../guides/overview-govern.md)
27. [Privacy](../../../guides/overview-privacy.md)
29. [Organizations & Accounts](../../../guides/overview-manage.md)
30. [Business continuity & data recovery](../../../user-guide/replication-intro.md)
32. [Performance optimization](../../../guides/overview-performance.md)
33. [Cost & Billing](../../../guides/overview-cost.md)

[Guides](../../../guides/README.md)[Migrations](../../README.md)Tools[SnowConvert AI](../overview.md)GeneralAbout

# SnowConvert AI - About[¶](#snowconvert-ai-about "Link to this heading")

SnowConvert AI is a specialized tool that accurately converts source code from various platforms to Snowflake exclusively.

SnowConvert AI is a proven tool that has successfully processed millions of objects and billions of lines of code for Snowflake migrations. Its extensive experience results in high-quality conversions that maintain functional equivalence with the source code. Based on historical data, SnowConvert AI achieves the following typical conversion rates for supported object types:

* Database tables
* Database views
* User-Defined Functions (UDFs)
* Stored procedures
* Database packages
* Additional database objects (including triggers, sequences, indexes, and other native objects)

## SnowConvert AI capabilities[¶](#snowconvert-ai-capabilities "Link to this heading")

| Source Technology | Availability | Supported Code Conversion | Source DB Connection | Data Migration | Snowflake Deployment |
| --- | --- | --- | --- | --- | --- |
| Teradata | GA | Tables, views, stored procedures, functions, Basic Teradata Query (BTEQ), Teradata MultiLoad (MLOAD), Teradata Parallel Data Pump (TPUMP) | Extraction script | No | No |
| Oracle | GA | Tables, views, stored procedures, functions, packages | Extraction script | No | No |
| SQL Server | GA | Tables, views, stored procedures, functions | Extraction script, direct DB connection | Yes | No |
| Redshift | GA | Tables, views, stored procedures, functions | Extraction script, direct DB connection | Yes | Direct connection to Snowflake |
| Azure Synapse | GA | Tables, views, stored procedures, functions | Extraction script | No | No |
| Sybase IQ | GA | Tables, views | Extraction script | No | No |
| Google BigQuery | GA | Tables, views | Extraction script | No | No |
| Greenplum | GA | Tables, views | No | No | No |
| Netezza | GA | Tables, views | No | No | No |
| PostgreSQL | GA | Tables, views | No | No | No |
| Spark SQL | GA | Tables, views | No | No | No |
| Databricks SQL | GA | Tables, views | No | No | No |
| Vertica | GA | Tables, views | No | No | No |
| Hive | GA | Tables, views | No | No | No |
| IBM DB2 | GA | Tables, views, stored procedures, functions | No | No | No |

SnowConvert AI is a code conversion tool that Snowflake acquired through Mobilize. It operates independently from the Snowflake Service and has its own terms of use. The Snowflake support team does not provide assistance for SnowConvert AI, and it is not covered by Snowflake’s standard support and service level agreements. For more information, contact [snowconvert-info@snowflake.com](mailto:snowconvert-info%40snowflake.com).

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

1. [SnowConvert AI capabilities](#snowconvert-ai-capabilities)