---
auto_generated: true
description: 'We highly recommend you use our scripts to extract your workload:'
last_scraped: '2026-01-14T16:51:15.224222+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/general/getting-started/best-practices
title: SnowConvert AI - Best practices | Snowflake Documentation
---

1. [Overview](../../../../guides/README.md)
2. [Snowflake Horizon Catalog](../../../../user-guide/snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../../../../guides/overview-connecting.md)
6. [Virtual warehouses](../../../../user-guide/warehouses.md)
7. [Databases, Tables, & Views](../../../../guides/overview-db.md)
8. [Data types](../../../../data-types.md)
10. Data Integration

    - [Snowflake Openflow](../../../../user-guide/data-integration/openflow/about.md)
    - Apache Iceberg™

      - [Apache Iceberg™ Tables](../../../../user-guide/tables-iceberg.md)
      - [Snowflake Open Catalog](../../../../user-guide/opencatalog/overview.md)
11. Data engineering

    - [Data loading](../../../../guides/overview-loading-data.md)
    - [Dynamic Tables](../../../../user-guide/dynamic-tables-about.md)
    - [Streams and Tasks](../../../../user-guide/data-pipelines-intro.md)
    - [dbt Projects on Snowflake](../../../../user-guide/data-engineering/dbt-projects-on-snowflake.md)
    - [Data Unloading](../../../../guides/overview-unloading-data.md)
12. [Storage Lifecycle Policies](../../../../user-guide/storage-management/storage-lifecycle-policies.md)
13. [Migrations](../../../README.md)

    * Tools

      * [SnowConvert AI](../../overview.md)

        + General

          + [About](../about.md)
          + [Getting Started](README.md)

            - [System Requirements](system-requirements.md)
            - [Best Practices](best-practices.md)
            - [Download And Access](download-and-access.md)
            - [Code Extraction](code-extraction/README.md)
            - [Running Snowconvert AI](running-snowconvert/README.md)
            - [Training And Support](training-and-support.md)
          + [Terms And Conditions](../terms-and-conditions/README.md)
          + [Release Notes](../release-notes/release-notes/README.md)
          + User Guide

            + [SnowConvert AI](../user-guide/snowconvert/README.md)
            + [Project Creation](../user-guide/project-creation.md)
            + [Extraction](../user-guide/extraction.md)
            + [Deployment](../user-guide/deployment.md)
            + [Data Migration](../user-guide/data-migration.md)
            + [Data Validation](../user-guide/data-validation.md)
            + [Power BI Repointing](../user-guide/power-bi-repointing-general.md)
            + [ETL Migration](../user-guide/etl-migration-replatform.md)
          + [Technical Documentation](../technical-documentation/README.md)
          + [Contact Us](../contact-us.md)
          + Others

            + [Using SnowConvert AI In A Ubuntu Docker Image](../others/using-snowconvert-in-a-ubuntu-docker-image.md)
          + [Frequently Asked Questions (FAQ)](../frequently-asked-questions-faq.md)")
        + Translation References

          + [General](../../translation-references/general/README.md)
          + [Teradata](../../translation-references/teradata/README.md)
          + [Oracle](../../translation-references/oracle/README.md)
          + [SQL Server-Azure Synapse](../../translation-references/transact/README.md)
          + [Sybase IQ](../../translation-references/sybase/README.md)
          + [Hive-Spark-Databricks SQL](../../translation-references/hive/README.md)
          + [Redshift](../../translation-references/redshift/README.md)
          + [PostgreSQL-Greenplum-Netezza](../../translation-references/postgres/README.md)
          + [BigQuery](../../translation-references/bigquery/README.md)
          + [Vertica](../../translation-references/vertica/README.md)
          + [IBM DB2](../../translation-references/db2/README.md)
          + [SSIS](../../translation-references/ssis/README.md)
        + [Migration Assistant](../../migration-assistant/README.md)
        + [Data Validation CLI](../../data-validation-cli/index.md)
        + [AI Verification](../../snowconvert-ai-verification.md)
      * [Snowpark Migration Accelerator](../../../sma-docs/README.md)
    * Guides

      * [Teradata](../../../guides/teradata.md)
      * [Databricks](../../../guides/databricks.md)
      * [SQL Server](../../../guides/sqlserver.md)
      * [Amazon Redshift](../../../guides/redshift.md)
      * [Oracle](../../../guides/oracle.md)
      * [Azure Synapse](../../../guides/azuresynapse.md)
15. [Queries](../../../../guides/overview-queries.md)
16. [Listings](../../../../collaboration/collaboration-listings-about.md)
17. [Collaboration](../../../../guides/overview-sharing.md)
19. [Snowflake AI & ML](../../../../guides/overview-ai-features.md)
21. [Snowflake Postgres](../../../../user-guide/snowflake-postgres/about.md)
23. [Alerts & Notifications](../../../../guides/overview-alerts.md)
25. [Security](../../../../guides/overview-secure.md)
26. [Data Governance](../../../../guides/overview-govern.md)
27. [Privacy](../../../../guides/overview-privacy.md)
29. [Organizations & Accounts](../../../../guides/overview-manage.md)
30. [Business continuity & data recovery](../../../../user-guide/replication-intro.md)
32. [Performance optimization](../../../../guides/overview-performance.md)
33. [Cost & Billing](../../../../guides/overview-cost.md)

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)General[Getting Started](README.md)Best Practices

# SnowConvert AI - Best practices[¶](#snowconvert-ai-best-practices "Link to this heading")

## 1. Extraction[¶](#extraction "Link to this heading")

We highly recommend you use our scripts to extract your workload:

* Teradata: [Click here](https://github.com/Snowflake-Labs/SC.DDLExportScripts/blob/main/Teradata/README.md).
* Oracle: [Click here](https://github.com/Snowflake-Labs/SC.DDLExportScripts/blob/main/Oracle/README.md).
* SQLServer: [Click here](https://github.com/Snowflake-Labs/SC.DDLExportScripts/blob/main/SQLServer/README.pdf).
* Redshift: [Click here](code-extraction/redshift).

## 2. Preprocess[¶](#preprocess "Link to this heading")

We highly recommend you use a Preprocess Script that aims to give you better results before starting an assessment or a conversion. This script performs the following tasks:

1. Create a single file for each top-level object
2. Organize each file by a defined folder hierarchy (The default is: Database Name -> Schema Name -> Object Type)
3. Generate an inventory report that provides information on all the objects that are in the workload.

### 2.1 Download[¶](#download "Link to this heading")

* Please [click here](https://sctoolsartifacts.z5.web.core.windows.net/tools/extractorscope/standardize_sql_files) to download the binary of the script for MacOs (make sure to follow the setup on 2.3).
* Please [click here](https://sctoolsartifacts.z5.web.core.windows.net/tools/extractorscope/standardize_sql_files.exe) to download the binary of the script for Windows.

### 2.2 Description[¶](#description "Link to this heading")

The following information is needed to run the script:

| **Script Argument** | **Example Value** | **Required** | **Usage** |
| --- | --- | --- | --- |
| Input folder | `/home/user/extracted_ddls` | Yes | `{ -i | ifolder= }` |
| Output folder | `/home/user/processed_extracted_ddls` | Yes | `{ -o | ofolder= }` |
| Database name | `sampleDataBase` | Yes | `{ -d | dname= }` |
| Database engine | `Microsoft SQL Server` | Yes | `{ -e | dengine= }` |
| Output folder structure | `Database name, top level object type and schema` | No | `[ { -s | structure= } ]` |
| Pivot tables generation | `Yes` | No | `[ -p ]` |

Note

The supported values for the database engine argument (-e) are: oracle, mssql and teradata

Note

The supported values for the output folder structure argument (-s) are: database\_name, schema\_name and top\_level\_object\_name\_type.  
When specifying this argument all the previous values need to be separated by a comma (e.g., `-s database_name,top_level_object_name_type,schema_name`).

This argument is optional and when it is not specified the default structure is the following: Database name, top-level object type and schema name.

Note

The pivot tables generation parameter (-p) is optional.

### 2.3 Setup the binary for Mac[¶](#setup-the-binary-for-mac "Link to this heading")

1. Set the binary as an executable:   
   `chmod +x standardize_sql_files`
2. Run the script by executing the following command:

   `./standardize_sql_files`

   * If this is the first time running the binary the following message will pop-up:  
     ![](../../../../_images/image%2823%29.png) Click OK.
   * Open Settings -> Privacy & Security -> Click Allow Anyway  
     ![](../../../../_images/image%2824%29.png)

### Running the script[¶](#running-the-script "Link to this heading")

1. Running the script using the following format:

   1. Mac format  
      `./standardize_sql_files -i "input path" -o "output path" -d Workload1 -e teradata`
   2. Windows format  
      `./standardize_sql_files.exe -i "input path" -o "output path" -d Workload1 -e teradata`
2. If the script is successfully executed the following output will be displayed:

   `Splitting process completed successfully!`   
   `Report successfully created!`   
   `Script successfully executed!`

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

1. [1. Extraction](#extraction)
2. [2. Preprocess](#preprocess)