---
auto_generated: true
description: The first step for migration is getting the code that you need to migrate.
  There are many ways to extract the code from your database. However, we recommend
  using the extraction scripts provided by Sn
last_scraped: '2026-01-14T16:52:16.984886+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/general/getting-started/code-extraction/teradata
title: SnowConvert AI - Teradata | Snowflake Documentation
---

1. [Overview](../../../../../guides/README.md)
2. [Snowflake Horizon Catalog](../../../../../user-guide/snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../../../../../guides/overview-connecting.md)
6. [Virtual warehouses](../../../../../user-guide/warehouses.md)
7. [Databases, Tables, & Views](../../../../../guides/overview-db.md)
8. [Data types](../../../../../data-types.md)
10. Data Integration

    - [Snowflake Openflow](../../../../../user-guide/data-integration/openflow/about.md)
    - Apache Iceberg™

      - [Apache Iceberg™ Tables](../../../../../user-guide/tables-iceberg.md)
      - [Snowflake Open Catalog](../../../../../user-guide/opencatalog/overview.md)
11. Data engineering

    - [Data loading](../../../../../guides/overview-loading-data.md)
    - [Dynamic Tables](../../../../../user-guide/dynamic-tables-about.md)
    - [Streams and Tasks](../../../../../user-guide/data-pipelines-intro.md)
    - [dbt Projects on Snowflake](../../../../../user-guide/data-engineering/dbt-projects-on-snowflake.md)
    - [Data Unloading](../../../../../guides/overview-unloading-data.md)
12. [Storage Lifecycle Policies](../../../../../user-guide/storage-management/storage-lifecycle-policies.md)
13. [Migrations](../../../../README.md)

    * Tools

      * [SnowConvert AI](../../../overview.md)

        + General

          + [About](../../about.md)
          + [Getting Started](../README.md)

            - [System Requirements](../system-requirements.md)
            - [Best Practices](../best-practices.md)
            - [Download And Access](../download-and-access.md)
            - [Code Extraction](README.md)

              * [Oracle](oracle.md)
              * [Teradata](teradata.md)
              * [Redshift](redshift.md)
              * [SQL Server](sql-server.md)
              * [Sybase IQ](sybase-iq.md)
            - [Running Snowconvert AI](../running-snowconvert/README.md)
            - [Training And Support](../training-and-support.md)
          + [Terms And Conditions](../../terms-and-conditions/README.md)
          + [Release Notes](../../release-notes/release-notes/README.md)
          + User Guide

            + [SnowConvert AI](../../user-guide/snowconvert/README.md)
            + [Project Creation](../../user-guide/project-creation.md)
            + [Extraction](../../user-guide/extraction.md)
            + [Deployment](../../user-guide/deployment.md)
            + [Data Migration](../../user-guide/data-migration.md)
            + [Data Validation](../../user-guide/data-validation.md)
            + [Power BI Repointing](../../user-guide/power-bi-repointing-general.md)
            + [ETL Migration](../../user-guide/etl-migration-replatform.md)
          + [Technical Documentation](../../technical-documentation/README.md)
          + [Contact Us](../../contact-us.md)
          + Others

            + [Using SnowConvert AI In A Ubuntu Docker Image](../../others/using-snowconvert-in-a-ubuntu-docker-image.md)
          + [Frequently Asked Questions (FAQ)](../../frequently-asked-questions-faq.md)")
        + Translation References

          + [General](../../../translation-references/general/README.md)
          + [Teradata](../../../translation-references/teradata/README.md)
          + [Oracle](../../../translation-references/oracle/README.md)
          + [SQL Server-Azure Synapse](../../../translation-references/transact/README.md)
          + [Sybase IQ](../../../translation-references/sybase/README.md)
          + [Hive-Spark-Databricks SQL](../../../translation-references/hive/README.md)
          + [Redshift](../../../translation-references/redshift/README.md)
          + [PostgreSQL-Greenplum-Netezza](../../../translation-references/postgres/README.md)
          + [BigQuery](../../../translation-references/bigquery/README.md)
          + [Vertica](../../../translation-references/vertica/README.md)
          + [IBM DB2](../../../translation-references/db2/README.md)
          + [SSIS](../../../translation-references/ssis/README.md)
        + [Migration Assistant](../../../migration-assistant/README.md)
        + [Data Validation CLI](../../../data-validation-cli/index.md)
        + [AI Verification](../../../snowconvert-ai-verification.md)
      * [Snowpark Migration Accelerator](../../../../sma-docs/README.md)
    * Guides

      * [Teradata](../../../../guides/teradata.md)
      * [Databricks](../../../../guides/databricks.md)
      * [SQL Server](../../../../guides/sqlserver.md)
      * [Amazon Redshift](../../../../guides/redshift.md)
      * [Oracle](../../../../guides/oracle.md)
      * [Azure Synapse](../../../../guides/azuresynapse.md)
15. [Queries](../../../../../guides/overview-queries.md)
16. [Listings](../../../../../collaboration/collaboration-listings-about.md)
17. [Collaboration](../../../../../guides/overview-sharing.md)
19. [Snowflake AI & ML](../../../../../guides/overview-ai-features.md)
21. [Snowflake Postgres](../../../../../user-guide/snowflake-postgres/about.md)
23. [Alerts & Notifications](../../../../../guides/overview-alerts.md)
25. [Security](../../../../../guides/overview-secure.md)
26. [Data Governance](../../../../../guides/overview-govern.md)
27. [Privacy](../../../../../guides/overview-privacy.md)
29. [Organizations & Accounts](../../../../../guides/overview-manage.md)
30. [Business continuity & data recovery](../../../../../user-guide/replication-intro.md)
32. [Performance optimization](../../../../../guides/overview-performance.md)
33. [Cost & Billing](../../../../../guides/overview-cost.md)

[Guides](../../../../../guides/README.md)[Migrations](../../../../README.md)Tools[SnowConvert AI](../../../overview.md)General[Getting Started](../README.md)[Code Extraction](README.md)Teradata

# SnowConvert AI - Teradata[¶](#snowconvert-ai-teradata "Link to this heading")

The first step for migration is getting the code that you need to migrate. There are many ways to extract the code from your database. However, we recommend using the extraction scripts provided by Snowflake.

All the source code for these scripts is open source and is available on [GitHub](https://github.com/Snowflake-Labs/SC.DDLExportScripts/).

## Prerequisites[¶](#prerequisites "Link to this heading")

* Access to a server with a Teradata database.
* Permission to run shell scripts with access to the server.
* Teradata utilities like`bteq / tpt`.

## Installing the scripts[¶](#installing-the-scripts "Link to this heading")

Go to <https://github.com/Snowflake-Labs/SC.DDLExportScripts/>.

![image](../../../../../_images/DDLExportScripts.png)

From the Code option, select the drop-down and use the **Download ZIP** option to download the code.

Decompress the ZIP file. The code for Teradata should be under the Teradata folder

![](../../../../../_images/image%2832%29.png)

Follow the [Usage instructions](https://github.com/Snowflake-Labs/SC.DDLExportScripts/blob/main/Teradata/README.md) to modify the files and run them on your system.

### Package the results[¶](#package-the-results "Link to this heading")

When the script is done, the output folder will contain all the DDLs for the migration. You can then compress this folder to use it with [SnowConvert AI](../../../overview).

E.g. run:

```
zip -r output.zip ./output
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

1. [Prerequisites](#prerequisites)
2. [Installing the scripts](#installing-the-scripts)