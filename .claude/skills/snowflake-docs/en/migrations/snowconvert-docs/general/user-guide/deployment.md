---
auto_generated: true
description: SnowConvert AI, as part of the end-to-end migration experience, offers
  the option to deploy converted database objects directly to your Snowflake environment.
  With this deployment feature, you can rev
last_scraped: '2026-01-14T16:51:41.965082+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/general/user-guide/deployment
title: 'SnowConvert AI: Deployment | Snowflake Documentation'
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)GeneralUser GuideDeployment

# SnowConvert AI: Deployment[¶](#snowconvert-ai-deployment "Link to this heading")

SnowConvert AI, as part of the end-to-end migration experience, offers the option to deploy converted database objects directly to your Snowflake environment. With this deployment feature, you can review conversion results, authenticate to Snowflake, and deploy selected objects with their proper dependencies and execution order. This deployment feature is available for SQL Server and Amazon Redshift databases.

## Conversion status indicators[¶](#conversion-status-indicators "Link to this heading")

Before deployment, SnowConvert AI provides visual indicators to help you understand the conversion status of each object:

### Ready for Deployment[¶](#ready-for-deployment "Link to this heading")

Objects that have been successfully converted and are ready for deployment without any issues.

### Functional Data Model (FDM) Warnings[¶](#functional-data-model-fdm-warnings "Link to this heading")

Objects with FDMs have been found in the conversion. It is recommended to review these before deployment, though they can still be deployed.

### Equivalent Work Item (EWI) Errors[¶](#equivalent-work-item-ewi-errors "Link to this heading")

Objects with EWIs have critical issues that must be fixed before deployment. These objects cannot be deployed until the issues are resolved.

Note

For detailed information about FDMs and EWIs, please refer to the [SnowConvert AI Technical Documentation](../technical-documentation/README).

## Supported authentication methods[¶](#supported-authentication-methods "Link to this heading")

The deployment process supports two authentication methods to connect to your Snowflake environment:

### SSO (Single Sign-On)[¶](#sso-single-sign-on "Link to this heading")

Allows authentication using your organization’s Single Sign-On provider configured with Snowflake. This method provides seamless integration with your existing identity management system.

### Standard authentication[¶](#standard-authentication "Link to this heading")

Traditional username and password authentication with the following security requirements:

* Multi-factor authentication (MFA) must be enabled for your Snowflake account
* Follows Snowflake’s security best practices and recommendations

Note

The account identifier must use **-** for separation instead of **.** (for example, **orgname-account-name**).

Warning

Ensure that you follow [Snowflake’s security recommendations](https://community.snowflake.com/s/article/Snowflake-Security-Overview-and-Best-Practices) and have [multi-factor authentication (MFA)](https://docs.snowflake.com/en/user-guide/ui-snowsight-profile.html#label-snowsight-set-up-mfa) enabled.

## Deployment execution order[¶](#deployment-execution-order "Link to this heading")

The deployment process executes database objects in a specific order to maintain proper dependencies:

1. **Databases**: Created first to establish the container structure.
2. **Schemas**: Created within databases to organize objects.
3. **Tables**: Created to establish data structures.
4. **Views**: Created after tables because they depend on table structures.
5. **Functions**: Deployed to provide reusable logic.
6. **Stored Procedures**: Deployed last as they may reference other objects.

## Deploy converted database objects to Snowflake[¶](#deploy-converted-database-objects-to-snowflake "Link to this heading")

You can deploy your converted database objects to Snowflake. After deployment, you can proceed with data migration
to complete the end-to-end migration process.

Ensure that you meet the following prerequisites before deploying converted objects:

* You completed conversion process with objects ready for deployment.
* You have a valid Snowflake account with appropriate permissions.
* You have multi-factor authentication (MFA) enabled (for Standard authentication).

Complete the following steps to deploy converted objects:

1. In SnowConvert AI, open the project, and then select **Deploy code**.
2. On the **Connect to Snowflake** page, complete the fields with your connection information, and then select **Sign in**.

   The **Select objects to deploy** page appears. The following image is an example of the page:

   ![](../../../../_images/deploy-objects.png)
3. Review the conversion status and resolve any errors before proceeding.

   Examine the status indicators for each object in your project. Resolve any EWI errors before proceeding.
4. Select the objects that you want to deploy to Snowflake.

   Only select objects with successful conversion status or acceptable FDM warnings.

   Note

   If you make changes to object files, you can refresh the conversion status by selecting **Refresh files**.
5. Select **Deploy**.

   The deployment process starts. Objects are deployed automatically, in the proper dependency order. When deployment
   finishes, the **Deployment results** window appears.
6. In **Deployment results**, review the results for success confirmations or error messages.

   The following image is an example of a **Deployment results** window:

   ![](../../../../_images/deploying-results.png)

Note

Only successfully converted objects are available for deployment. You must resolve objects with EWI errors before you can deploy them.

After completing the deployment process, your database objects are available in your Snowflake environment. You can then proceed
with [data migration](data-migration) to transfer your data to complete the full migration process and make everything ready for use in your
applications and workflows.

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

1. [Conversion status indicators](#conversion-status-indicators)
2. [Supported authentication methods](#supported-authentication-methods)
3. [Deployment execution order](#deployment-execution-order)
4. [Deploy converted database objects to Snowflake](#deploy-converted-database-objects-to-snowflake)