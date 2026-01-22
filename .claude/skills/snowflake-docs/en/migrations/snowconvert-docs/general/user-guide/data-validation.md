---
auto_generated: true
description: SnowConvert AI, as part of the end-to-end migration experience, provides
  the capability to validate your migrated data to ensure that both the structure
  of the data and the data itself match the origi
last_scraped: '2026-01-14T16:51:41.546482+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/general/user-guide/data-validation
title: 'SnowConvert AI: Data validation | Snowflake Documentation'
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)GeneralUser GuideData Validation

# SnowConvert AI: Data validation[¶](#snowconvert-ai-data-validation "Link to this heading")

SnowConvert AI, as part of the end-to-end migration experience, provides the capability to validate your migrated data to ensure
that both the structure of the data and the data itself match the original source. This data validation feature is available for SQL Server databases.

## Data validation modes[¶](#data-validation-modes "Link to this heading")

To ensure that your data is successfully migrated to Snowflake, the data validation employs two distinct validation levels: schema validation and metrics validation.

### Schema validation[¶](#schema-validation "Link to this heading")

Schema validation confirms that the basic structure of your migrated table is preserved in Snowflake. It validates the following table attributes:

* Table name
* Column names
* Ordinal position of each column
* Data types
* Character maximum length for text columns
* Numeric precision and scale for numeric columns
* Row Count

### Metrics validation[¶](#metrics-validation "Link to this heading")

Metrics validation confirms that the data itself matches the original source. Metrics validation compares aggregate metrics between each original table and the corresponding new Snowflake table. Although the specific metrics can vary by column data type, metrics validation evaluates the following items:

* Minimum value
* Maximum value
* Average
* Nulls count
* Distinct count
* Standard deviation
* Variance

## Validate migrated data[¶](#validate-migrated-data "Link to this heading")

Warning

For accurate validation and to avoid false negatives, don’t alter the migrated data during the validation process.

For SQL Server migrations, validation includes an optional step within the process. This step validates the data after you
use SnowConvert AI to move it.

### Prerequisites[¶](#prerequisites "Link to this heading")

This feature requires a version of Python that meets the following requirements to be installed and available in your PATH:

* Greater than or equal to 3.10.
* Lower than or equal to 3.13.

To verify that a supported Python version is available in your PATH:

1. In your terminal (or Command Prompt on Windows), run `python --version`.
2. Confirm that the Python version meets the requirements that are mentioned earlier.

Complete the following steps to validate your migrated data:

1. In SnowConvert AI, open **Validate data** in one of the following ways:

   * Complete the [data migration process](data-migration), and then select **Go to data validation**.
   * In your project, select **Data validation**.
2. On the **Connect to source database** page, complete the fields with the connection information for your source
   database, select **Test connection**, and then select **Continue**.
3. Select the objects that you want to validate.

   The following image is an example of the page:

   ![](../../../../_images/validate-objects.png)
4. Select **Validate data**.

   The validation process starts.

   When validation completes successfully and no differences are found, SnowConvert AI displays a message confirming that no
   differences were found.

   If differences are found in the migrated data, SnowConvert AI generates a report and displays a summary of the discrepancies in the tables.

   The following image is an example of a validation report:

   ![](../../../../_images/data-validation-report.png)

   Also, a CSV file report is generated so you can visualize and share it.

   The validation results are classified into three categories:

   | Category | Description |
   | --- | --- |
   |  | Values match exactly between the source database and Snowflake. |
   |  | Snowflake table has minor differences that don’t affect the data, such as higher numeric precision. |
   |  | Values don’t match between the original database and the Snowflake database. |

   Finally, you can open the reports folder to access the generated CSV reports:

   ![](../../../../_images/data-validation-csv.png)

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

1. [Data validation modes](#data-validation-modes)
2. [Validate migrated data](#validate-migrated-data)