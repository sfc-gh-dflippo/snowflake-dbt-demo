---
auto_generated: true
description: Visual Studio Code Extension
last_scraped: '2026-01-14T16:52:59.465239+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/migration-assistant/README
title: SnowConvert AI - Migration Assistant | Snowflake Documentation
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

          + [About](../general/about.md)
          + [Getting Started](../general/getting-started/README.md)
          + [Terms And Conditions](../general/terms-and-conditions/README.md)
          + [Release Notes](../general/release-notes/release-notes/README.md)
          + User Guide

            + [SnowConvert AI](../general/user-guide/snowconvert/README.md)
            + [Project Creation](../general/user-guide/project-creation.md)
            + [Extraction](../general/user-guide/extraction.md)
            + [Deployment](../general/user-guide/deployment.md)
            + [Data Migration](../general/user-guide/data-migration.md)
            + [Data Validation](../general/user-guide/data-validation.md)
            + [Power BI Repointing](../general/user-guide/power-bi-repointing-general.md)
            + [ETL Migration](../general/user-guide/etl-migration-replatform.md)
          + [Technical Documentation](../general/technical-documentation/README.md)
          + [Contact Us](../general/contact-us.md)
          + Others

            + [Using SnowConvert AI In A Ubuntu Docker Image](../general/others/using-snowconvert-in-a-ubuntu-docker-image.md)
          + [Frequently Asked Questions (FAQ)](../general/frequently-asked-questions-faq.md)")
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
        + [Migration Assistant](README.md)

          - [Getting Started](getting-started.md)
          - [Troubleshooting](troubleshooting.md)
          - [Billing](billing.md)
          - [Legal Notices](legal-notices.md)
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

[Guides](../../../guides/README.md)[Migrations](../../README.md)Tools[SnowConvert AI](../overview.md)Migration Assistant

# SnowConvert AI - Migration Assistant[¶](#snowconvert-ai-migration-assistant "Link to this heading")

Visual Studio Code Extension

The SnowConvert AI Migration Assistant is an AI-powered tool designed to streamline the resolution of errors, warnings, and issues ([EWIs](../general/technical-documentation/issues-and-troubleshooting/conversion-issues/README)) encountered after converting SQL code using SnowConvert.

Integrated within the Snowflake Visual Studio Code extension, the Migration Assistant offers an interactive workflow for navigating, understanding, and fixing EWIs, accelerating your migration to Snowflake.

The assistant leverages the [Snowflake REST API](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-rest-api) to provide explanations and actionable suggestions for EWIs that SnowConvert AI cannot automatically resolve.

Warning

* The SnowConvert AI Migration Assistant uses **Snowflake Cortex AI** to provide helpful suggestions. Large language models can make mistakes, so it’s essential to review and validate all explanations and fixes before implementation.
* Using this tool requires signing in to your Snowflake account and having access to **SNOWFLAKE.CORTEX.COMPLETE** and at least one of the [supported models](model-preference.html#supported-models) by the Assistant.
* You can use [cross-region inference](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cross-region-inference) if your preferred models are not available in your default region.

## Key Features[¶](#key-features "Link to this heading")

* AI-driven analysis of EWIs using the Snowflake REST API.
* Explanations of EWI root causes.
* Chat interaction about SQL-related topics
* Actionable solutions and recommendations.
* Seamless integration with the Snowflake Visual Studio Code extension.

## Supported sources[¶](#supported-sources "Link to this heading")

SnowConvert AI Migration Assistant has been optimized for migrations with Microsoft SQL Server as a source database, and we recommend using it for migrations from this source.

The assistant is designed to work with all supported SnowConvert AI source databases, and in **future releases**, we will optimize results for a wider set of source databases.

## Learn More[¶](#learn-more "Link to this heading")

* [Getting Started](getting-started)
* [Troubleshooting](troubleshooting)
* [Legal Notices](legal-notices)

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

1. [Key Features](#key-features)
2. [Supported sources](#supported-sources)
3. [Learn More](#learn-more)