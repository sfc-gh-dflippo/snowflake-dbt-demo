---
auto_generated: true
description: This setting in SnowConvert AI determines how the tool reads and interprets
  the text within your source files. Choosing the correct encoding is important to
  ensure that all characters, especially acce
last_scraped: '2026-01-14T16:52:02.618323+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/general/getting-started/running-snowconvert/conversion/general-conversion-settings
title: SnowConvert AI - General Conversion Settings | Snowflake Documentation
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

[Guides](../../../../../../guides/README.md)[Migrations](../../../../../README.md)Tools[SnowConvert AI](../../../../overview.md)General[Getting Started](../../README.md)[Running Snowconvert AI](../README.md)[Conversion](README.md)General Conversion Settings

# SnowConvert AI - General Conversion Settings[¶](#snowconvert-ai-general-conversion-settings "Link to this heading")

## File encoding settings[¶](#file-encoding-settings "Link to this heading")

This setting in SnowConvert AI determines how the tool reads and interprets the text within your source files. Choosing the correct encoding is important to ensure that all characters, especially accented letters, symbols, or text from various languages, are processed correctly during conversion. By default SnowConvert AI uses `UTF-8`.

![image](../../../../../../_images/image%28402%29.png)

**Manually Selecting an Encoding**

You can choose to override this automatic process by selecting a specific encoding from the dropdown menu. If you select an encoding manually (even if you select `UTF-8` explicitly), SnowConvert AI will use *only* that chosen encoding to read the files.

**Available Encoding Options**

The dropdown list allows you to force SnowConvert AI to use one of these specific encodings:

| Code Page | Name | Display Name |
| --- | --- | --- |
| 1200 | utf-16 | Unicode |
| 1201D | unicodeFFFE | Unicode (Big endian) |
| 12000 | utf-32 | Unicode (UTF-32) |
| 12001 | utf-32BE | Unicode (UTF-32 Big endian) |
| 20127 | us-ascii | US-ASCII |
| 28591 | iso-8859-1 | Western European (ISO) |
| 65000 | utf-7 | Unicode (UTF-7). *Not available in .NET 5* |
| 65001 | utf-8 | Unicode (UTF-8). ***Default encoding*** |

**Understanding `System Default (Preview)`**

When selecting the **`System Default (Preview)`** , SnowConvert AI uses a flexible approach:

1. It first tries to automatically detect the specific character encoding of each input file.
2. If auto-detection doesn’t identify the encoding, SnowConvert AI proceeds using `UTF-8`, which handles a very wide range of characters and is common for modern files.
3. As a fallback, if the `UTF-8` interpretation fails because it finds characters that aren’t valid in UTF-8, SnowConvert AI will then attempt to use your computer’s default system encoding.

It’s marked “Preview” because this behavior is experimental. System defaults can vary significantly between different computers and operating systems, potentially leading to inconsistent results or unsupported encodings.

**Recommendation**

If you encounter errors related to text interpretation or see garbled characters in your results, manually selecting the correct encoding is the best solution. If you know your files use a specific format (like `Western European`), select that. If you’re unsure but suspect encoding issues, explicitly selecting `UTF-8` is often a good starting point as it’s the most common standard for modern files.

## Materialized views conversion settings[¶](#materialized-views-conversion-settings "Link to this heading")

On this page, you will find the necessary options to customize the parameters for translating Materialized Views (or join indexes in Teradata) to Dynamic Tables during your conversion.

![image](../../../../../../_images/Screenshot2024-05-30at8.54.16AM.png)

![image](../../../../../../_images/Screenshot2024-05-30at8.54.26AM.png)

To preserve the full functionality of Materialized Views, or Teradata’s Join Indexes, SnowConvert AI generates Dynamic Tables instead of creating a one-to-one Materialized View or transforming a Join Index into a Materialized View. This approach is necessary because Snowflake lacks certain configuration options available in other systems’ Materialized Views.

For further details on the limitations of Snowflake’s Materialized Views, please refer to [Materialized Views Limitations](https://docs.snowflake.com/en/user-guide/views-materialized#label-limitations-on-creating-materialized-views).

### Transformation[¶](#transformation "Link to this heading")

The settings defined here will apply to every instance of a Dynamic Table generated during the conversion process.

Dynamic Table Conversion Settings:

* **Target Lag**: This setting specifies the maximum allowable time for the dynamic table’s content to lag behind updates in the base table. For example, setting this to 5 minutes ensures that the data in the dynamic table is no more than 5 minutes behind the base table’s updates.
* **Warehouse**: This setting specifies the name of the Warehouse that supplies the computing resources for refreshing the dynamic table. You must have the USAGE privilege on this warehouse to create the dynamic table. By default, SnowConvert AI will use a placeholder value.

For more information, please refer to the Snowflake Dynamic Table [documentation](https://docs.snowflake.com/en/sql-reference/sql/create-dynamic-table).

## **Next steps for Amazon Redshift databases**[¶](#next-steps-for-amazon-redshift-databases "Link to this heading")

For Amazon Redshift databases, you can use SnowConvert AI to complete the following tasks after conversion:

* [Deployment](../../../user-guide/deployment)
* [Data migration](../../../user-guide/data-migration)

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

1. [File encoding settings](#file-encoding-settings)
2. [Materialized views conversion settings](#materialized-views-conversion-settings)
3. [Next steps for Amazon Redshift databases](#next-steps-for-amazon-redshift-databases)