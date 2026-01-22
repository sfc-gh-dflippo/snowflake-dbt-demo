---
auto_generated: true
description: 'SnowConvert AI, as part of the end-to-end migration experience, provides
  the capability to migrate your actual data from source tables to Snowflake after
  the database structure is deployed. This data '
last_scraped: '2026-01-14T16:51:41.253710+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/general/user-guide/data-migration
title: 'SnowConvert AI: Data migration | Snowflake Documentation'
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)GeneralUser GuideData Migration

# SnowConvert AI: Data migration[¶](#snowconvert-ai-data-migration "Link to this heading")

SnowConvert AI, as part of the end-to-end migration experience, provides the capability to migrate your actual data from source tables to Snowflake after the database structure is deployed. This data migration feature ensures that your data is transferred efficiently and accurately to complete the data migration process. This data migration feature is available for SQL Server and Amazon Redshift databases.

## Data migration process overview[¶](#data-migration-process-overview "Link to this heading")

The data migration process varies depending on your source database platform.

### Amazon Redshift to Snowflake[¶](#amazon-redshift-to-snowflake "Link to this heading")

SnowConvert AI migrates data from Redshift tables by unloading it to PARQUET files in an S3 bucket, then copying the data directly from those files to the deployed tables in Snowflake.

![](../../../../_images/SnowConvertStudioHighLevelDataMigrationArchitecture-Page5%282%29.png)

### SQL Server to Snowflake[¶](#sql-server-to-snowflake "Link to this heading")

Data migration from SQL Server utilizes optimized data transfer methods to move your table data efficiently to the corresponding Snowflake tables.

## Prerequisites[¶](#prerequisites "Link to this heading")

Ensure that you meet the following general prerequisites:

* You completed the deployment process with database structure in Snowflake.
* You have active connections to both a source database and Snowflake account.
* You have sufficient permissions for data operations on both source and target systems.

In addition, ensure that the prerequisites are complete for your source database platform:

* [Prerequisites for Amazon Redshift Sources](#prerequisites-for-amazon-redshift-sources)
* [Prerequisites for SQL Server Sources](#prerequisites-for-sql-server-sources)

### Prerequisites for Amazon Redshift sources[¶](#prerequisites-for-amazon-redshift-sources "Link to this heading")

Before executing data migration from Redshift, ensure that you meet the following prerequisites:

#### S3 bucket requirements[¶](#s3-bucket-requirements "Link to this heading")

* An S3 bucket in AWS in the same region as your Redshift cluster.
* Empty bucket path; the process fails if files exist in the specified path.

#### IAM role for Redshift[¶](#iam-role-for-redshift "Link to this heading")

Create an IAM role associated with your Redshift cluster that can unload data to your S3 bucket:

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "VisualEditor0",
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:GetBucketLocation",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::<your_bucket_name>/*",
        "arn:aws:s3:::<your_bucket_name>"
      ]
    }
  ]
}
```

Copy

#### IAM user for S3 access[¶](#iam-user-for-s3-access "Link to this heading")

Create an IAM user with permissions to read and delete objects from your S3 bucket:

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:GetObjectVersion",
        "s3:DeleteObject",
        "s3:DeleteObjectVersion",
        "s3:ListBucket",
        "s3:GetBucketLocation"
      ],
      "Resource": [
        "arn:aws:s3:::<your_bucket_name>/*",
        "arn:aws:s3:::<your_bucket_name>"
      ]
    }
  ]
}
```

Copy

Warning

If you don’t provide `s3:DeleteObject` and `s3:DeleteObjectVersion` permissions, the temporary data files won’t be deleted from the S3 bucket even if the migration succeeds.

### Prerequisites for SQL Server sources[¶](#prerequisites-for-sql-server-sources "Link to this heading")

* Valid connection to your SQL Server source database.
* Appropriate permissions to read data from source tables.
* Network connectivity between the migration tool and both source and target systems.

## Migrate your data[¶](#migrate-your-data "Link to this heading")

Complete the end-to-end data migration process by transferring your actual data to the deployed database structure in Snowflake:

* [Migrate Amazon Redshift Data](#migrate-amazon-redshift-data)
* [Migrate SQL Server data](#migrate-sql-server-data)

### Migrate Amazon Redshift data[¶](#migrate-amazon-redshift-data "Link to this heading")

1. In SnowConvert AI, open the project, and then select **Migrate data**.
2. On the **Connect to source database** page, complete the fields with the connection information for your source
   database, and then select **Continue**.
3. On the **Connect to Snowflake** page, complete the fields with your connection information, and then select **Continue**.
4. On the **Set up S3 bucket** page, specify the following information:

   * **Database**: Select the database that contains the tables that you want to migrate.
   * **Schema**: Select the schema that contains the tables that you want to migrate.
   * **Stage**: Select the stage where data files will be stored.
   * **S3 bucket URI**: Enter the Uniform Resource Identifier for the Amazon S3 bucket that contains the source data. The URL must end with `/`.
   * **Data unloading IAM role ARN**: Enter the Amazon Resource Name (ARN) for the IAM role that you used to unload the data to Amazon S3.

   The following image is an example of the page:

   ![](../../../../_images/data-migration-redshift-s3.png)
5. On the **Select tables to migrate data** page, select the tables that you want to migrate.

   The following image is an example of the page:

   ![](../../../../_images/data-migration-select-objects.png)
6. Select **Migrate data**.

   When the migration completes successfully, the **Results** page appears.

   If the results don’t look correct, you can select **Retry data migration** to run the data migration process again.
7. When the results look correct on the **Results** page, select **Go to data validation** to start the
   [validation process](data-validation).

### Migrate SQL Server data[¶](#migrate-sql-server-data "Link to this heading")

1. In SnowConvert AI, open the project, and then select **Migrate data**.
2. On the **Connect to source database** page, complete the fields with the connection information for your source
   database, and then select **Continue**.
3. On the **Connect to Snowflake** page, complete the fields with your connection information, and then select **Continue**.
4. On the **Select tables to migrate data** page, select the tables that you want to migrate.

   The following image is an example of the page:

   ![](../../../../_images/data-migration-select-objects.png)
5. Select **Migrate data**.

   When the migration completes successfully, the **Results** page appears.

   If the results don’t look correct, you can select **Retry data migration** to run the data migration process again.
6. When the results look correct on the **Results** page, select **Go to data validation** to start the
   [validation process](data-validation).

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

1. [Data migration process overview](#data-migration-process-overview)
2. [Prerequisites](#prerequisites)
3. [Migrate your data](#migrate-your-data)