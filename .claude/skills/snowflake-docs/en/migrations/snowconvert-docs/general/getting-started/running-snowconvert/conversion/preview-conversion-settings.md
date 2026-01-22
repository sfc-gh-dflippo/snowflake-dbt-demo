---
auto_generated: true
description: The Preview Features Settings in SnowConvert AI allow you to enable conversions
  that utilize Snowflake Public Preview features. By entering any of the available
  flags in the textbox, SnowConvert AI ca
last_scraped: '2026-01-14T16:52:03.349241+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/general/getting-started/running-snowconvert/conversion/preview-conversion-settings
title: SnowConvert AI - Preview Features Settings | Snowflake Documentation
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
          + [Getting Started](../../README.md)

            - [System Requirements](../../system-requirements.md)
            - [Best Practices](../../best-practices.md)
            - [Download And Access](../../download-and-access.md)
            - [Code Extraction](../../code-extraction/README.md)
            - [Running Snowconvert AI](../README.md)

              * [Supported Languages](../supported-languages/README.md)
              * [Validation](../validation/README.md)
              * [Conversion](README.md)

                + [SQL Server Conversion Settings](sql-server-conversion-settings.md)
                + [General Conversion Settings](general-conversion-settings.md)
                + [Converting Subfolders](converting-subfolders.md)
                + [Oracle Conversion Settings](oracle-conversion-settings.md)
                + [Teradata Conversion Settings](teradata-conversion-settings.md)
                + [Preview Features Settings](preview-conversion-settings.md)
              * [Review Results](../review-results/README.md)
            - [Training And Support](../../training-and-support.md)
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
          + [Technical Documentation](../../../technical-documentation/README.md)
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

[Guides](../../../../../../guides/README.md)[Migrations](../../../../../README.md)Tools[SnowConvert AI](../../../../overview.md)General[Getting Started](../../README.md)[Running Snowconvert AI](../README.md)[Conversion](README.md)Preview Features Settings

# SnowConvert AI - Preview Features Settings[¶](#snowconvert-ai-preview-features-settings "Link to this heading")

## Preview Features Settings[¶](#preview-features-settings "Link to this heading")

The Preview Features Settings in SnowConvert AI allow you to enable conversions that utilize **Snowflake Public Preview features**. By entering any of [the available flags](#available-preview-features) in the textbox, SnowConvert AI can generate code that takes advantage of Snowflake features that are currently in public preview status, rather than being limited to only generally available (GA) Snowflake features.

![image](../../../../../../_images/ConversionPreviewFlags.png)

Warning

Preview features are Snowflake features that are available for evaluation and testing purposes but are not yet generally available (GA). They should not be used in production systems. For more details about Snowflake preview features, see the [Snowflake Preview Terms of Service](https://www.snowflake.com/legal/preview-terms-of-service/).

### Understanding Snowflake Preview Features[¶](#understanding-snowflake-preview-features "Link to this heading")

Snowflake Public Preview features are new capabilities that have been implemented and tested in Snowflake but may not have complete usability or corner-case handling. When you enable preview features in SnowConvert AI, the conversion process can generate code that uses these preview features when they provide better conversion results.

### How to Use Preview Features[¶](#how-to-use-preview-features "Link to this heading")

1. **Enable in SnowConvert AI**: Enter any of [the available flags](#available-preview-features) in the textbox within the Preview Features Settings to allow SnowConvert AI to generate code using Snowflake preview features
2. **Enable in Snowflake**: Ensure that preview features are enabled in your Snowflake account using system functions like `SYSTEM_ENABLE_PREVIEW_ACCESS`
3. **Test thoroughly**: Always test the converted code in a non-production Snowflake environment when using preview features

### Important Considerations[¶](#important-considerations "Link to this heading")

* **Snowflake account compatibility**: Your Snowflake account must have preview features enabled to use the generated code
* **Feature stability**: Snowflake preview features may change behavior or be removed in future Snowflake releases
* **Production restrictions**: Code using preview features should not be deployed to production Snowflake environments
* **Documentation**: SnowConvert AI may add comments indicating when preview features are being used

### Accessing Preview Features Settings[¶](#accessing-preview-features-settings "Link to this heading")

To configure preview features in SnowConvert AI:

1. Navigate to the **Conversion Settings** section in the SnowConvert AI interface
2. Select the **Preview Features** tab or section
3. Enter any of [the available flags](#available-preview-features) in the textbox to allow SnowConvert AI to use Snowflake preview features. Please be sure that each flag is spelled correctly; if any flag is misspelled, all flags will be ignored during conversion.
4. Proceed with conversion - SnowConvert AI will automatically use preview features when they improve conversion results.

### Using Preview Features from CLI[¶](#using-preview-features-from-cli "Link to this heading")

When using SnowConvert AI from the command line interface (CLI), you can enable preview features by using the `--previewFlags` argument. The value must be wrapped with quotes and contain the flags in the following format:

```
--previewFlags "\"--enableFlag1 --enableFlag2\""
```

Copy

**Example:**

```
snowct [command] --previewFlags "\"--enableFlag\"" [other arguments]
```

Copy

For multiple flags:

```
snowct [command] --previewFlags "\"--enableFlag --enableAnotherFlag\"" [other arguments]
```

Copy

### Best Practices[¶](#best-practices "Link to this heading")

* **Understand implications**: Ensure you understand that the converted code will require Snowflake preview features to be enabled

Note

For the most current information about which Snowflake preview features SnowConvert AI can utilize, consult the latest SnowConvert AI release notes or contact support.

## Available Preview Features[¶](#available-preview-features "Link to this heading")

The following section lists the preview feature flags that can be entered in the textbox to enable specific Snowflake preview features during conversion. Each flag enables SnowConvert AI to use particular Snowflake preview capabilities.

### **`--enableSnowScriptUDF`**[¶](#enablesnowscriptudf "Link to this heading")

*Deprecated since version 1.19.7 This feature is already in General Availability*

This option enables SnowConvert AI to translate User-Defined Functions, taking advantage of the SnowScript UDF Preview Feature. Learn more from the documentation here: [Snowflake Scripting UDFs](../../../../../../developer-guide/udf/sql/udf-sql-procedural-functions).

Available only for the following languages:

* Sql Server.
* Azure Synapse.

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

1. [Preview Features Settings](#preview-features-settings)
2. [Available Preview Features](#available-preview-features)