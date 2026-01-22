---
auto_generated: true
description: SnowConvert AI allows you to run a conversion over a specific portion
  of your code, ignoring the parts that do not need to be converted.
last_scraped: '2026-01-14T16:52:02.424489+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/general/getting-started/running-snowconvert/conversion/converting-subfolders
title: SnowConvert AI - Converting subfolders | Snowflake Documentation
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

[Guides](../../../../../../guides/README.md)[Migrations](../../../../../README.md)Tools[SnowConvert AI](../../../../overview.md)General[Getting Started](../../README.md)[Running Snowconvert AI](../README.md)[Conversion](README.md)Converting Subfolders

# SnowConvert AI - Converting subfolders[¶](#snowconvert-ai-converting-subfolders "Link to this heading")

SnowConvert AI allows you to run a conversion over a specific portion of your code, ignoring the parts that do not need to be converted.

## How to execute a conversion over a subfolder[¶](#how-to-execute-a-conversion-over-a-subfolder "Link to this heading")

The ‘**Project Creation**’ page will show a checkbox called ‘**Convert a subfolder’** below the input folder path field.

![Convert a subfolder option in SnowConvert AI](../../../../../../_images/Screenshot2025-01-06at2.09.26PM.png)

Click on it to open the **folder explorer** where a specific folder could be selected for conversion.

![Folder explorer of SnowConvert AI](../../../../../../_images/Screenshot2025-01-06at2.10.31PM.png)

Note

The folders shown on the folder explorer component, are the ones that contain files with allowed extensions (depending on the selected source platform). So, if a folder does not show up on the folder explorer, it means it does not contain files with the allowed extensions.

To select a subfolder, click on the radio button located on the left side of the subfolder list item. You can expand or collapse the subfolder to review the files within it by clicking on the subfolder name or clicking on the expand/collapse icon on each item.

After selecting a subfolder, the selected folder path can be viewed on the “**Convert the following**” section above the folder explorer component.

![Selected path in file explorer of SnowConvert AI](../../../../../../_images/Screenshot2025-01-06at2.11.20PM.png)

Note

Hovering on the path label will show a tooltip with the full path, this applies to any field that contains a shortened path (input folder path, output folder path, etc.).

Then, enter your access code and click on the ‘**Save & Start Conversion’** button. The conversion will be executed using **only** the selected subfolder as the input.

![image](../../../../../../_images/Screenshot2025-01-03at9.48.22PM.png)

When this process is completed you will be able to see:

1. **Conversion Results:** Conversion reports will be open as soon as your conversion is finished and you click on the ‘**View Results**’ button.  
     
   The selected subfolder will appear below the ‘**Execution Summary**’ section along with other information.\

   ![image](../../../../../../_images/Screenshot2025-01-06at2.15.31PM.png)
2. **Conversion Output Code**: To check this you only need to click on ‘**View Output**’ on the Conversion Results page and the folder that contains your converted code will be opened.
3. **Retry Conversion**: After you execute a conversion, on the Conversion Results page you can select the **Retry Conversion** button to run again the conversion. That is useful if you change the source code and want to convert the new source code again, or even if you want to select another subfolder to convert.

   ![Options in Conversion Results page of SnowConvert AI](../../../../../../_images/Screenshot2025-01-06at2.17.31PM.png)

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

1. [How to execute a conversion over a subfolder](#how-to-execute-a-conversion-over-a-subfolder)