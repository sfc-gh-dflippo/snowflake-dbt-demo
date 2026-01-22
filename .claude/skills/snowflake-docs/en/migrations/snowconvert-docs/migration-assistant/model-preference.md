---
auto_generated: true
description: The SnowConvert AI Migration Assistant supports configurable AI model
  preferences with automatic fallback functionality. This feature allows you to customize
  which AI models are used for generating fi
last_scraped: '2026-01-14T16:53:01.595185+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/migration-assistant/model-preference
title: SnowConvert AI - Migration Assistant - Model Preference | Snowflake Documentation
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

            * [Model Preference](model-preference.md)
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

[Guides](../../../guides/README.md)[Migrations](../../README.md)Tools[SnowConvert AI](../overview.md)[Migration Assistant](README.md)[Getting Started](getting-started.md)Model Preference

# SnowConvert AI - Migration Assistant - Model Preference[¶](#snowconvert-ai-migration-assistant-model-preference "Link to this heading")

The SnowConvert AI Migration Assistant supports configurable AI model preferences with automatic fallback functionality. This feature allows you to customize which AI models are used for generating fixes and in what order they should be attempted.

## Supported Models[¶](#supported-models "Link to this heading")

The Migration Assistant supports the following AI models through Snowflake Cortex AI:

| Model | Status | Description |
| --- | --- | --- |
| Claude 3.7 Sonnet | Recommended | Best quality responses, optimized for migration assistance |
| Claude 3.5 Sonnet | Stable | High quality alternative if Claude 3.7 is unavailable |
| Claude 4 Sonnet | Experimental | Improved quality over Claude 3.7 Sonnet, latest Claude model |
| Llama 3.1 70B | Experimental | Results may vary, assistant optimized for Claude models |
| Mistral Large 2 | Experimental | Results may vary, assistant optimized for Claude models |

Warning

The Migration Assistant has been primarily optimized for Claude models. While other models are supported, they may provide varying quality results compared to the Claude models.

## How to Configure Model Preferences[¶](#how-to-configure-model-preferences "Link to this heading")



Open VS Code Settings

* Go to File > Preferences > Settings (or Code > Preferences > Settings on macOS)
* Or use the keyboard shortcut: `Ctrl + ,` (Windows/Linux) or `Cmd + ,` (macOS)



Navigate to the Settings

* Search for **Snowflake: Snow Convert Migration Assistant: Model Preference**
* Or navigate to Extensions > Snowflake > **Snowflake: Snow Convert Migration Assistant: Model Preference**



Configure Your Preferences

* **Add models**

  + Select any model from the dropdown list to add it to your preferences
  + The model will be added to the end of your current list
* **Remove models**

  + Click the “X” next to any model to remove it from your preferences
  + You must have at least one model configured to use the assistant
* **Reorder models**

  + You can either:

    - Remove or add models to your desired order.
    - Change the model by clicking the “pencil” icon and selecting one of the available models.
  + The first model in the list will always be attempted first



### Default Configuration[¶](#default-configuration "Link to this heading")

By default, the Migration Assistant comes configured with this model preference order:

1. Claude 3.7 Sonnet (recommended)
2. Claude 3.5 Sonnet (high quality alternative)
3. Llama 3.1 70B (experimental)
4. Mistral Large 2 (experimental)

## Execution Order and Fallback Mechanism[¶](#execution-order-and-fallback-mechanism "Link to this heading")

The Migration Assistant uses an intelligent fallback system that works as follows:

1. **Sequential Execution**: Models are tried in the exact order you specify in your preference list
2. **Automatic Fallback**: If the first model fails or is unavailable, the assistant automatically attempts the next model in your list
3. **Complete Cycle**: The process continues through your entire model list until one succeeds or all models have been exhausted
4. **Error Handling**: If all models fail, you’ll receive detailed error information and suggestions for each attempted model

Example Execution Flow:

```
1. Attempt: Claude 3.7 Sonnet → Failed (model unavailable in region)
2. Attempt: Claude 3.5 Sonnet → Failed (budget exceeded)  
3. Attempt: Llama 3.1 70B → Success → Response generated
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

1. [Supported Models](#supported-models)
2. [How to Configure Model Preferences](#how-to-configure-model-preferences)
3. [Execution Order and Fallback Mechanism](#execution-order-and-fallback-mechanism)