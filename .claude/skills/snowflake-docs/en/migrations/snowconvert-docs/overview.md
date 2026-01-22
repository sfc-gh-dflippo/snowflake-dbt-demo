---
auto_generated: true
description: ''
last_scraped: '2026-01-14T16:52:59.825672+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/overview
title: Snowflake SnowConvert AI Documentation | Snowflake Documentation
---

1. [Overview](../../guides/README.md)
2. [Snowflake Horizon Catalog](../../user-guide/snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../../guides/overview-connecting.md)
6. [Virtual warehouses](../../user-guide/warehouses.md)
7. [Databases, Tables, & Views](../../guides/overview-db.md)
8. [Data types](../../data-types.md)
10. Data Integration

    - [Snowflake Openflow](../../user-guide/data-integration/openflow/about.md)
    - Apache Iceberg™

      - [Apache Iceberg™ Tables](../../user-guide/tables-iceberg.md)
      - [Snowflake Open Catalog](../../user-guide/opencatalog/overview.md)
11. Data engineering

    - [Data loading](../../guides/overview-loading-data.md)
    - [Dynamic Tables](../../user-guide/dynamic-tables-about.md)
    - [Streams and Tasks](../../user-guide/data-pipelines-intro.md)
    - [dbt Projects on Snowflake](../../user-guide/data-engineering/dbt-projects-on-snowflake.md)
    - [Data Unloading](../../guides/overview-unloading-data.md)
12. [Storage Lifecycle Policies](../../user-guide/storage-management/storage-lifecycle-policies.md)
13. [Migrations](../README.md)

    * Tools

      * [SnowConvert AI](overview.md)

        + General

          + [About](general/about.md)
          + [Getting Started](general/getting-started/README.md)
          + [Terms And Conditions](general/terms-and-conditions/README.md)
          + [Release Notes](general/release-notes/release-notes/README.md)
          + User Guide

            + [SnowConvert AI](general/user-guide/snowconvert/README.md)
            + [Project Creation](general/user-guide/project-creation.md)
            + [Extraction](general/user-guide/extraction.md)
            + [Deployment](general/user-guide/deployment.md)
            + [Data Migration](general/user-guide/data-migration.md)
            + [Data Validation](general/user-guide/data-validation.md)
            + [Power BI Repointing](general/user-guide/power-bi-repointing-general.md)
            + [ETL Migration](general/user-guide/etl-migration-replatform.md)
          + [Technical Documentation](general/technical-documentation/README.md)
          + [Contact Us](general/contact-us.md)
          + Others

            + [Using SnowConvert AI In A Ubuntu Docker Image](general/others/using-snowconvert-in-a-ubuntu-docker-image.md)
          + [Frequently Asked Questions (FAQ)](general/frequently-asked-questions-faq.md)")
        + Translation References

          + [General](translation-references/general/README.md)
          + [Teradata](translation-references/teradata/README.md)
          + [Oracle](translation-references/oracle/README.md)
          + [SQL Server-Azure Synapse](translation-references/transact/README.md)
          + [Sybase IQ](translation-references/sybase/README.md)
          + [Hive-Spark-Databricks SQL](translation-references/hive/README.md)
          + [Redshift](translation-references/redshift/README.md)
          + [PostgreSQL-Greenplum-Netezza](translation-references/postgres/README.md)
          + [BigQuery](translation-references/bigquery/README.md)
          + [Vertica](translation-references/vertica/README.md)
          + [IBM DB2](translation-references/db2/README.md)
          + [SSIS](translation-references/ssis/README.md)
        + [Migration Assistant](migration-assistant/README.md)
        + [Data Validation CLI](data-validation-cli/index.md)
        + [AI Verification](snowconvert-ai-verification.md)
      * [Snowpark Migration Accelerator](../sma-docs/README.md)
    * Guides

      * [Teradata](../guides/teradata.md)
      * [Databricks](../guides/databricks.md)
      * [SQL Server](../guides/sqlserver.md)
      * [Amazon Redshift](../guides/redshift.md)
      * [Oracle](../guides/oracle.md)
      * [Azure Synapse](../guides/azuresynapse.md)
15. [Queries](../../guides/overview-queries.md)
16. [Listings](../../collaboration/collaboration-listings-about.md)
17. [Collaboration](../../guides/overview-sharing.md)
19. [Snowflake AI & ML](../../guides/overview-ai-features.md)
21. [Snowflake Postgres](../../user-guide/snowflake-postgres/about.md)
23. [Alerts & Notifications](../../guides/overview-alerts.md)
25. [Security](../../guides/overview-secure.md)
26. [Data Governance](../../guides/overview-govern.md)
27. [Privacy](../../guides/overview-privacy.md)
29. [Organizations & Accounts](../../guides/overview-manage.md)
30. [Business continuity & data recovery](../../user-guide/replication-intro.md)
32. [Performance optimization](../../guides/overview-performance.md)
33. [Cost & Billing](../../guides/overview-cost.md)

[Guides](../../guides/README.md)[Migrations](../README.md)ToolsSnowConvert AI

# Snowflake SnowConvert AI Documentation[¶](#snowflake-snowconvert-ai-documentation "Link to this heading")

![image](../../_images/SnowConvert.png)

Traditional data platforms and big data solutions often fail to meet their main goal: allowing users to work with data without restrictions on size, speed, or adaptability. Snowflake’s modern cloud-based data warehouse offers benefits for all data professionals, including analysts, scientists, engineers, and business users. Here are the key advantages of moving to Snowflake, the leading cloud data platform:

* *Multi-cluster and shared data*: enables fast and efficient processing of large data volumes using multiple clusters simultaneously.
* *Micro-Partitioning*: provides secure and efficient data storage with automatic organization.
* *Delivered as a service*: eliminates the need for manual administration and management of data infrastructure.
* *Data Platform built for any cloud*: separates storage from compute, allowing multiple compute clusters to work on the same data simultaneously.
* *Better Performance and throughput*: delivers faster data processing compared to traditional data platforms.
* *Support for all data*: processes both structured data and semi-structured formats (JSON, Avro, XML, Parquet) in a single platform.

*SnowConvert AI* is a user-friendly tool that helps you modernize your traditional data platform by migrating it to Snowflake’s Data Warehousing Architecture. *SnowConvert AI* analyzes your existing SQL code (from platforms like Oracle, SQL Server, and Teradata) and converts it to [**Snowflake SQL**](../../sql-reference-commands). After conversion, you can immediately take advantage of all Snowflake’s features and capabilities.

Currently, *SnowConvert AI* supports converting code from these source platforms:

* **Teradata**
* **Oracle**
* **SQL Server**
* **Sybase IQ**
* **Redshift**
* **Azure Synapse**
* **Spark SQL**
* **Databricks SQL**
* **BigQuery**
* **PostgreSQL & Based Languages**
* **Vertica**
* **Hive**
* **IBM DB2**

Looking to migrate to a new platform? [Please contact us](general/contact-us) to discuss your needs.

## Additional Resources[¶](#additional-resources "Link to this heading")

For more information, see our [Getting Started Guide](general/getting-started/README)

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

1. [Additional Resources](#additional-resources)