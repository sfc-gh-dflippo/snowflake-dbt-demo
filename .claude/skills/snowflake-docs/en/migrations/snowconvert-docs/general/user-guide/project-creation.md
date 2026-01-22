---
auto_generated: true
description: SnowConvert AI manages migrations by using SnowConvert AI projects. A
  SnowConvert AI project contains metadata about migrating a data set into Snowflake,
  such as the source database platform, input fi
last_scraped: '2026-01-14T16:51:43.564968+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/general/user-guide/project-creation
title: 'SnowConvert AI: Project Creation | Snowflake Documentation'
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
          + [Getting Started](../getting-started/README.md)
          + [Terms And Conditions](../terms-and-conditions/README.md)
          + [Release Notes](../release-notes/release-notes/README.md)
          + User Guide

            + [SnowConvert AI](snowconvert/README.md)
            + [Project Creation](project-creation.md)
            + [Extraction](extraction.md)
            + [Deployment](deployment.md)
            + [Data Migration](data-migration.md)
            + [Data Validation](data-validation.md)
            + [Power BI Repointing](power-bi-repointing-general.md)
            + [ETL Migration](etl-migration-replatform.md)
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)GeneralUser GuideProject Creation

# SnowConvert AI: Project Creation[¶](#snowconvert-ai-project-creation "Link to this heading")

SnowConvert AI manages migrations by using SnowConvert AI projects. A SnowConvert AI project contains metadata about migrating a data set into Snowflake, such as the source database platform, input files, and output location. You can save and reuse these settings for multiple conversion runs.

To create a new project, complete the following steps:

1. Open SnowConvert AI, and then select **New Project**.

   The **New Project** page appears:

   ![](../../../../_images/snowconvert-create-project.png)
2. Enter the following information:

   * **Project name**: The name of the project.
   * **Select source**: The type of the source database system; for example, SQL Server, Oracle, and so on.
   * **Select or enter access code**: Enter the access code that you obtained previously. If you don’t have
     an access code, select the **Request access code** link. For more information, see
     [SnowConvert AI - How to get an access code](snowconvert/how-to-request-an-access-code/README).
3. To use Snowflake Cortex to help verify and fix migration objects, turn on **AI features**.

   If you don’t want to use Snowflake Cortex for the migration, turn off **AI features**.

   For more information about Snowflake Cortex, see [Snowflake AI and ML](https://docs.snowflake.com/en/guides-overview-ai-features).
4. For **Snowflake connection**, optionally enter the information required to connect to your Snowflake account.
5. Select **Save Project**.

After creating a project, you can proceed to the [extraction process](extraction) to extract database objects from your source system to prepare them for the conversion process.

Was this page helpful?

YesNo

[Visit Snowflake](https://www.snowflake.com)

[Join the conversation](https://community.snowflake.com/s/)

[Develop with Snowflake](https://developers.snowflake.com)

[Share your feedback](/feedback)

[Read the latest on our blog](https://www.snowflake.com/blog/)

[Get your own certification](https://learn.snowflake.com)

[Privacy Notice](https://www.snowflake.com/privacy-policy/)[Site Terms](https://www.snowflake.com/legal/snowflake-site-terms/)Cookies Settings© 2026 Snowflake, Inc. All Rights Reserved.