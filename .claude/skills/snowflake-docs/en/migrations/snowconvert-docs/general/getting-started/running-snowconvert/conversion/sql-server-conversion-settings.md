---
auto_generated: true
description: 'This topic applies to the following sources:'
last_scraped: '2026-01-14T16:52:03.731633+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/general/getting-started/running-snowconvert/conversion/sql-server-conversion-settings
title: SnowConvert AI - SQL Server Conversion Settings | Snowflake Documentation
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

[Guides](../../../../../../guides/README.md)[Migrations](../../../../../README.md)Tools[SnowConvert AI](../../../../overview.md)General[Getting Started](../../README.md)[Running Snowconvert AI](../README.md)[Conversion](README.md)SQL Server Conversion Settings

# SnowConvert AI - SQL Server Conversion Settings[¶](#snowconvert-ai-sql-server-conversion-settings "Link to this heading")

This topic applies to the following sources:

* SQL Server
* Azure Synapse Analytics

Before conversion, you use SnowConvert AI to extract database objects from your source system to prepare them for
the conversion process. For more information, see [SnowConvert AI: Data Extraction](../../../user-guide/extraction).

## General conversion settings[¶](#general-conversion-settings "Link to this heading")

![General Conversion Settings page](../../../../../../_images/image%28397%29.png)

1. **Comment objects with missing dependencies:** Flag to indicate if the user wants to comment on nodes that have missing dependencies.
2. **Set encoding of the input files:** Check [General Conversion Settings](general-conversion-settings) for more details.

Note

To review the Settings that apply to all supported languages, go to the following [article](general-conversion-settings).

## DB objects names settings[¶](#db-objects-names-settings "Link to this heading")

![DB Objects Names Settings page](../../../../../../_images/image%28400%29.png)

1. **Schema:** The string value specifies the custom schema name to apply. If not specified, the original database name will be used. Example: DB1.**myCustomSchema**.Table1.
2. **Database:** The string value specifies the custom database name to apply. Example: **MyCustomDB**.PUBLIC.Table1.
3. **Default:** None of the above settings will be used in the objects names.

## Prepare Code Settings[¶](#prepare-code-settings "Link to this heading")

![Prepare Code Settings page](../../../../../../_images/image%28401%29.png)

### **Description**[¶](#description "Link to this heading")

**Prepare my code:** Flag to indicate whether the input code should be processed before parsing and transformation. This can be useful to improve the parsing process. By default, it’s set to FALSE.

Splits the input code top-level objects into multiple files. The containing folders would be organized as follows:

Copy

```
└───A new folder named ''[input_folder_name]_Processed''
    └───Top-level object type
        └───Schema name
```

Copy

### **Example**[¶](#example "Link to this heading")

#### **Input**[¶](#input "Link to this heading")

```
├───in
│       script_name.sql
```

Copy

#### **Output**[¶](#output "Link to this heading")

Assume that the name of the files is the name of the top-level objects in the input files.

```
├───in_Processed
    ├───procedure
    │   └───dbo
    │           A_PROCEDURE.sql
    │           ANOTHER_PROCEDURE.sql
    │           YET_ANOTHER_PROCEDURE.sql
    │
    └───table
        └───dbo
                MY_TABLE.sql
                ADDITIONAL_TABLE.sql
                THIRD_TABLE.sql
```

Copy

### Requirements [¶](#requirements "Link to this heading")

We highly recommend using [SQL Server Management Studio (SSMS)](https://learn.microsoft.com/en-us/sql/ssms/download-sql-server-management-studio-ssms?view=sql-server-ver16) to obtain the script.

## Stored Procedures Target Languages Settings[¶](#stored-procedures-target-languages-settings "Link to this heading")

![Stored Procedures Target Languages Settings page](../../../../../../_images/image%28403%29.png)

On this page, you can choose whether stored procedures are migrated to JavaScript embedded in Snow SQL, or to Snowflake Scripting. The default option is Snowflake Scripting.

**Reset Settings:** The reset settings option appears on every page. If you’ve made changes, you can reset SnowConvert AI to its original default settings.

## **Next steps for SQL Server databases**[¶](#next-steps-for-sql-server-databases "Link to this heading")

For SQL Server databases, you can use SnowConvert AI to complete the following tasks after conversion:

* [Deployment](../../../user-guide/deployment)
* [Data migration](../../../user-guide/data-migration)
* [Data validation](../../../user-guide/data-validation)

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

1. [General conversion settings](#general-conversion-settings)
2. [DB objects names settings](#db-objects-names-settings)
3. [Prepare Code Settings](#prepare-code-settings)
4. [Stored Procedures Target Languages Settings](#stored-procedures-target-languages-settings)
5. [Next steps for SQL Server databases](#next-steps-for-sql-server-databases)