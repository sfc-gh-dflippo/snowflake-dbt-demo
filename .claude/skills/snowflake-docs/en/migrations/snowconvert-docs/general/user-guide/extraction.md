---
auto_generated: true
description: 'SnowConvert AI provides the following options for extracting database
  objects:'
last_scraped: '2026-01-14T16:51:42.852798+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/general/user-guide/extraction
title: 'SnowConvert AI: Extraction | Snowflake Documentation'
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)GeneralUser GuideExtraction

# SnowConvert AI: Extraction[¶](#snowconvert-ai-extraction "Link to this heading")

SnowConvert AI provides the following options for extracting database objects:

* [Extract code](#extract-code): For SQL Server and Amazon Redshift databases, use this option if you don’t already have code for extracted database objects.
* [Load existing code](#load-existing-code): For any source database, use this option if you already have code for extracted database objects.
  You might already have code if you previously extracted the code by using SnowConvert AI or if you generated the code yourself.

## Extract code[¶](#extract-code "Link to this heading")

SnowConvert AI, as part of the end-to-end migration experience, offers the option to extract database objects from your source system to prepare them for the conversion process. This extraction feature is available for SQL Server and Amazon Redshift databases, letting you connect to your source database, browse the catalog, and select specific objects for migration.

The extraction process supports different database objects depending on your source database type:

**SQL Server Objects**

* Tables
* Views
* Functions
* Stored procedures

**Amazon Redshift Objects**

* Tables
* Views
* Materialized views
* Stored procedures

To extract database objects from a source system, complete the following steps:

1. [Create the project](project-creation), and then select **Continue**.
2. On the **Add code to your project** page,select **Extract code**.

   The **Set up code and ETL/BI projects** page appears. The following image is an example of the page
   for SQL Server:

   ![](../../../../_images/sql-standard.png)
3. In **Authentication Method**, select the authentication method that you want to use to connect to the source system.
   The following authentication methods are supported:

   * **SQL Server**

     + **Standard Authentication**
     + **Windows Authentication**
   * **Amazon Redshift**

     + **Standard Authentication**
     + **IAM Provisioned Cluster**
     + **IAM Serverless**

   When you select an authentication method, the other fields on the page are refreshed based on the method.
4. To provide appropriate information for your authentication method, complete the remaining fields.
5. For SQL Server migrations, both authentication methods require verification about whether the following security settings
   are configured for your source database:

   * **Trust server certificate**: Enable if the database requires trusted certificate validation.
   * **Encrypt connection**: Enable if the database requires encrypted connections.
6. In **Where should the converted code be saved?**, select **Browse**, and then choose a location for the code.
7. In **Have ETL projects or BI/reports?**, select the options that you want to use for
   [replatforming](etl-migration-replatform) or [repointing](power-bi-repointing-general), and then
   select the corresponding files.
8. Select **Continue**.
9. On the **Select objects to extract** page, choose the objects that you want to migrate.

   The system retrieves the metadata and structure information for the selected objects.

   The following image shows a sample **Select objects to extract** page:

   ![](../../../../_images/sql-extraction-objects.png)
10. Select **Extract objects**.
11. Review the extraction results.

    The following image shows a sample **Extraction resultst** window:

    ![](../../../../_images/sql-extraction-results.png)

When extraction is complete, move on to [Next steps](#next-steps).

## Load existing code[¶](#load-existing-code "Link to this heading")

To load existing code for extracted database objects, complete the following steps:

1. [Create the project](project-creation), and select **Continue**.
2. On the **Add code to your project** page, select **Already have code**.

   The **Set up code and ETL/BI projects** page appears. The following image is an example of the page
   for SQL Server:

   ![](../../../../_images/sql-standard-load-code.png)
3. On the **Set up code and ETL/BI projects** page, specify the following information:

   * **Where is your source code?**: Select **Browse**, and then choose the location of your source code.
   * **Where should the converted code be saved?**: Select **Browse**, and then choose the location of your converted code.
4. In **Have ETL projects or BI/reports?**, select the options that you want to use for
   [replatforming](etl-migration-replatform) or [repointing](power-bi-repointing-general), and then
   select the corresponding files.
5. Select **Continue**.

When extraction is complete, move on to [Next steps](#next-steps).

## Next steps[¶](#next-steps "Link to this heading")

Note

Only successfully extracted objects will be available for the subsequent conversion step.

After completing the extraction process, you can proceed to the [conversion process](../getting-started/running-snowconvert/conversion/README) to transform your database objects for Snowflake compatibility.

Was this page helpful?

YesNo

[Visit Snowflake](https://www.snowflake.com)

[Join the conversation](https://community.snowflake.com/s/)

[Develop with Snowflake](https://developers.snowflake.com)

[Share your feedback](/feedback)

[Read the latest on our blog](https://www.snowflake.com/blog/)

[Get your own certification](https://learn.snowflake.com)

[Privacy Notice](https://www.snowflake.com/privacy-policy/)[Site Terms](https://www.snowflake.com/legal/snowflake-site-terms/)Cookies Settings© 2026 Snowflake, Inc. All Rights Reserved.

On this page

1. [Extract code](#extract-code)
2. [Load existing code](#load-existing-code)
3. [Next steps](#next-steps)