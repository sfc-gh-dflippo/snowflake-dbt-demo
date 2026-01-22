---
auto_generated: true
description: 'SnowConvert AI requires a UUID to validate the license for offline activation
  in Linux. Follow these steps to find and provide the UUID:'
last_scraped: '2026-01-14T16:52:59.192193+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/general/user-guide/snowconvert/how-to-request-an-access-code/how-to-retrieve-your-uuid-for-offline-activation-in-linux
title: SnowConvert AI - How to Retrieve Your UUID for Offline Activation in Linux
  | Snowflake Documentation
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

            + [SnowConvert AI](../README.md)

              - [How To Install The Tool](../how-to-install-the-tool/README.md)
              - [How To Request An Access Code](README.md)

                * [How to Retrieve Your UUID for Offline Activation in Linux](how-to-retrieve-your-uuid-for-offline-activation-in-linux.md)
              - [Command Line Interface](../command-line-interface/README.md)
              - [What Is A SnowConvert AI Project](../what-is-a-snowconvert-project.md)
              - [How To Update The Tool](../how-to-update-the-tool.md)
              - [How To Use The SnowConvert AI Cli](../how-to-use-the-snowconvert-cli.md)
            + [Project Creation](../../project-creation.md)
            + [Extraction](../../extraction.md)
            + [Deployment](../../deployment.md)
            + [Data Migration](../../data-migration.md)
            + [Data Validation](../../data-validation.md)
            + [Power BI Repointing](../../power-bi-repointing-general.md)
            + [ETL Migration](../../etl-migration-replatform.md)
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

[Guides](../../../../../../guides/README.md)[Migrations](../../../../../README.md)Tools[SnowConvert AI](../../../../overview.md)GeneralUser Guide[SnowConvert AI](../README.md)[How To Request An Access Code](README.md)How to Retrieve Your UUID for Offline Activation in Linux

# SnowConvert AI - How to Retrieve Your UUID for Offline Activation in Linux[¶](#snowconvert-ai-how-to-retrieve-your-uuid-for-offline-activation-in-linux "Link to this heading")

SnowConvert AI requires a **UUID** to validate the license for offline activation in Linux. Follow these steps to find and provide the UUID:

## **Step 1: Open a Terminal**[¶](#step-1-open-a-terminal "Link to this heading")

To begin, open a terminal on your Linux system by:

* Pressing **Ctrl + Alt + T**
* Searching for **“Terminal”** in your application menu

## **Step 2: Retrieve the UUID of the Root Device**[¶](#step-2-retrieve-the-uuid-of-the-root-device "Link to this heading")

You need to obtain the **UUID** of your root device. Try the following commands in the given order until you get a valid UUID.

### **Option 1: Primary Command**[¶](#option-1-primary-command "Link to this heading")

Run the following command first:

```
findmnt / -o UUID -n
```

Copy

If successful, it will return a UUID similar to this:

```
5a14ccf7-6bac-47b7-a3d6-6c10822fb10d
```

Copy

### **Option 2: Alternative Command (If Option 1 Fails)**[¶](#option-2-alternative-command-if-option-1-fails "Link to this heading")

If the first command does not return a UUID in a single line, try:

```
blkid -s UUID -o value $(findmnt -n -o SOURCE /)
```

Copy

Expected output:

```
5a14ccf7-6bac-47b7-a3d6-6c10822fb10d
```

Copy

### **Option 3: Last Resort (If the Previous Commands Fail)**[¶](#option-3-last-resort-if-the-previous-commands-fail "Link to this heading")

If neither of the above commands work, use:

```
lsblk -nro UUID
```

Copy

This must return **only one UUID**. If multiple UUIDs are listed, this method **will not work**. Ensure that the output contains a **single valid UUID**, or try one of the previous methods again.

## **Step 3: Send the UUID**[¶](#step-3-send-the-uuid "Link to this heading")

Once you have retrieved the correct UUID, copy it and send it to the **SnowConvert AI support team** for activation.

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

1. [Step 1: Open a Terminal](#step-1-open-a-terminal)
2. [Step 2: Retrieve the UUID of the Root Device](#step-2-retrieve-the-uuid-of-the-root-device)
3. [Step 3: Send the UUID](#step-3-send-the-uuid)