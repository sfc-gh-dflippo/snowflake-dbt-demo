---
auto_generated: true
description: AI verification strengthens SnowConvert AI by automating functional validation
  of converted database code. AI verification uses synthetic data generation, AI-driven
  unit testing, and AI-driven resolut
last_scraped: '2026-01-14T16:53:00.164962+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/snowconvert-ai-verification
title: SnowConvert AI Verification | Snowflake Documentation
---

1. [Overview](../../guides/README.md)
2. [Snowflake Horizon Catalog](../../user-guide/snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../../guides/overview-connecting.md)
6. [Virtual warehouses](../../user-guide/warehouses.md)
7. [Databases, Tables, & Views](../../guides/overview-db.md)
8. [Data types](../../data-types.md)
10. Data Integration

    - [Snowflake Openflow](../../user-guide/data-integration/openflow/about.md)
    - Apache Iceberg™

      - [Apache Iceberg™ Tables](../../user-guide/tables-iceberg.md)
      - [Snowflake Open Catalog](../../user-guide/opencatalog/overview.md)
11. Data engineering

    - [Data loading](../../guides/overview-loading-data.md)
    - [Dynamic Tables](../../user-guide/dynamic-tables-about.md)
    - [Streams and Tasks](../../user-guide/data-pipelines-intro.md)
    - [dbt Projects on Snowflake](../../user-guide/data-engineering/dbt-projects-on-snowflake.md)
    - [Data Unloading](../../guides/overview-unloading-data.md)
12. [Storage Lifecycle Policies](../../user-guide/storage-management/storage-lifecycle-policies.md)
13. [Migrations](../README.md)

    * Tools

      * [SnowConvert AI](overview.md)

        + General

          + [About](general/about.md)
          + [Getting Started](general/getting-started/README.md)
          + [Terms And Conditions](general/terms-and-conditions/README.md)
          + [Release Notes](general/release-notes/release-notes/README.md)
          + User Guide

            + [SnowConvert AI](general/user-guide/snowconvert/README.md)
            + [Project Creation](general/user-guide/project-creation.md)
            + [Extraction](general/user-guide/extraction.md)
            + [Deployment](general/user-guide/deployment.md)
            + [Data Migration](general/user-guide/data-migration.md)
            + [Data Validation](general/user-guide/data-validation.md)
            + [Power BI Repointing](general/user-guide/power-bi-repointing-general.md)
            + [ETL Migration](general/user-guide/etl-migration-replatform.md)
          + [Technical Documentation](general/technical-documentation/README.md)
          + [Contact Us](general/contact-us.md)
          + Others

            + [Using SnowConvert AI In A Ubuntu Docker Image](general/others/using-snowconvert-in-a-ubuntu-docker-image.md)
          + [Frequently Asked Questions (FAQ)](general/frequently-asked-questions-faq.md)")
        + Translation References

          + [General](translation-references/general/README.md)
          + [Teradata](translation-references/teradata/README.md)
          + [Oracle](translation-references/oracle/README.md)
          + [SQL Server-Azure Synapse](translation-references/transact/README.md)
          + [Sybase IQ](translation-references/sybase/README.md)
          + [Hive-Spark-Databricks SQL](translation-references/hive/README.md)
          + [Redshift](translation-references/redshift/README.md)
          + [PostgreSQL-Greenplum-Netezza](translation-references/postgres/README.md)
          + [BigQuery](translation-references/bigquery/README.md)
          + [Vertica](translation-references/vertica/README.md)
          + [IBM DB2](translation-references/db2/README.md)
          + [SSIS](translation-references/ssis/README.md)
        + [Migration Assistant](migration-assistant/README.md)
        + [Data Validation CLI](data-validation-cli/index.md)
        + [AI Verification](snowconvert-ai-verification.md)

          - [With Source System Verification](ai-verification/snowconvert-ai-twosided-verification.md)
      * [Snowpark Migration Accelerator](../sma-docs/README.md)
    * Guides

      * [Teradata](../guides/teradata.md)
      * [Databricks](../guides/databricks.md)
      * [SQL Server](../guides/sqlserver.md)
      * [Amazon Redshift](../guides/redshift.md)
      * [Oracle](../guides/oracle.md)
      * [Azure Synapse](../guides/azuresynapse.md)
15. [Queries](../../guides/overview-queries.md)
16. [Listings](../../collaboration/collaboration-listings-about.md)
17. [Collaboration](../../guides/overview-sharing.md)
19. [Snowflake AI & ML](../../guides/overview-ai-features.md)
21. [Snowflake Postgres](../../user-guide/snowflake-postgres/about.md)
23. [Alerts & Notifications](../../guides/overview-alerts.md)
25. [Security](../../guides/overview-secure.md)
26. [Data Governance](../../guides/overview-govern.md)
27. [Privacy](../../guides/overview-privacy.md)
29. [Organizations & Accounts](../../guides/overview-manage.md)
30. [Business continuity & data recovery](../../user-guide/replication-intro.md)
32. [Performance optimization](../../guides/overview-performance.md)
33. [Cost & Billing](../../guides/overview-cost.md)

[Guides](../../guides/README.md)[Migrations](../README.md)Tools[SnowConvert AI](overview.md)AI Verification

# SnowConvert AI Verification[¶](#snowconvert-ai-verification "Link to this heading")

## Introduction[¶](#introduction "Link to this heading")

AI verification strengthens SnowConvert AI by automating functional validation of converted database code. AI verification uses synthetic data generation, AI-driven unit testing, and AI-driven resolution of errors identified in the conversion. It extends the existing deterministic conversion process — where error warnings and issues (EWIs) and feature detection messages (FDMs) flag conversion issues — with an intelligent layer in the Snowflake Service that proactively verifies correctness, resolves the errors, and accelerates confidence.

During migration, AI verification first applies deterministic logic to translate source code, surfacing EWIs and FDMs when it can’t automatically resolve certain patterns. Next, AI verification connects to the Snowflake test account you have configured and generates synthetic datasets, builds and executes unit tests tailored to the converted code, reports outcomes, and tries to rectify the errors. AI verification reduces manual remediation effort, identifies and resolves issues earlier in the process, and assures users that the converted objects behave as expected.

## Key features of SnowConvert AI Verification[¶](#key-features-of-snowconvert-ai-verification "Link to this heading")

* **Accelerated AI validation**: Dramatically reduce the time and resources you spend on manual testing.
* **Automated Test generation**: The agent automatically generates test cases based on your existing queries and business logic.
* **Agentic Repair suggestions**: The agent suggests patches to your existing code to produce consistent results between your legacy system and Snowflake.

## Prerequisites for SnowConvert AI Verification[¶](#prerequisites-for-snowconvert-ai-verification "Link to this heading")

Before you get started with SnowConvert AI Verification, complete the following steps:

1. Download and install [SnowConvert AI](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/getting-started/download-and-access).
2. [Recommended] Convert your legacy SQL Server code by using [SnowConvert AI](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/getting-started/download-and-access).
3. Connect an account specifically designated for testing and development and avoid using a production account.

   Some objects will be created as part of the AI verification process.
4. Ensure the PUBLIC role in the account you connect doesn’t have access to any production data and doesn’t have privileges to execute any sensitive operations, such as CREATE USER commands.
5. Ensure that the role used for AI verification has the following privileges on the account:

   * CREATE DATABASE
   * CREATE MIGRATION
6. Enable Cortex AI SQL functions in the account, specifically for model `claude-4-sonnet`.

   * To enable the model if it’s not available in your region, see [Cross-region inference](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cross-region-inference#any-region).

## Getting started with SnowConvert AI Verification[¶](#getting-started-with-snowconvert-ai-verification "Link to this heading")

To begin a migration validation project, complete the following steps:

1. **Start AI verification**. Execute the [code conversion of SnowConvert AI](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/getting-started/running-snowconvert/conversion/README) on your SQL Server database.
2. **Open AI verification**. After code conversion is complete, select **GO TO AI VERIFICATION**.

   ![](../../_images/snowconvert-ai-verification-start.png)

   | (i) All AI processing happens in the Snowflake account you connect to and consumes Snowflake charges. |
   | --- |
3. **Select objects to verify with AI.** After you are redirected to a page where the converted objects are available for selection for AI verification, select the objects you want to verify with AI verification.

   ![](../../_images/snowconvert-ai-verification-select.png)

   SnowConvert automatically performs the following actions:

   1. Automatically selects and validates dependent objects when they are associated with your chosen objects.
   2. Reviews a summary of the selected objects, their dependencies, and the estimated time and Snowflake credit cost.
   3. Confirms the selection to proceed with code verification.

   ![](../../_images/snowconvert-ai-verification-actions.png)
4. **Verify code with AI verification.** Select **VERIFY CODE**. Or, select **SKIP AI VERIFICATION** if you don’t want to use AI capabilities.

   If you select **VERIFY CODE**, SnowConvert AI connects to your Snowflake account, where it relies on [Cortex AI Functions](https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql) to review your code and suggest resolutions to any problems. AI verification might take a few minutes to start, and it might run for several minutes or hours depending on the complexity of the code being verified.

   ![](../../_images/snowconvert-ai-verification-review.png)
5. **Review the status of objects.** On the AI verification screen, review the status for the AI verification selected objects.

   On this screen is the status of each of the selected objects, whether they were already verified, and which changes the AI verification feature made.

   After the objects are validated, you can see their corresponding status, and you can check which changes in the code were made.

   ![](../../_images/snowconvert-ai-verification-check.png)

   | (i) Review the code generated by AI before deploying it. Code generated by AI might not be correct. |
   | --- |

   * Status of the AI verification:

     + Fixed with AI
     + Could not verify
     + Verified
     + Error in original object
   * **OPEN CODE**:

     + By default, this option opens and compares your original source code and the code generated by AI after the verification in VS Code.
     + If you click the arrow next to **OPEN CODE**, you also have the option to open and compare in VS Code:

       - The converted code from SnowConvert and the code generated and fixed by AI.

## Billing and cost considerations with SnowConvert AI Verification[¶](#billing-and-cost-considerations-with-snowconvert-ai-verification "Link to this heading")

AI Verification consumes Snowflake credits based on the compute resources it uses in your Snowflake account. The following features contribute to the cost:

* AI SQL - AI verification uses Cortex AI SQL.
* Warehouse - Test queries are executed in a warehouse.
* Snowflake stages - Input and outputs for AI verification are stored in a stage, which incurs storage costs.
* Snowpark Container Services - AI verification might consume a small amount of credits to use Snowpark Container
  Services. To find the costs associated with AI verification, look for compute pools with names that start with
  `AI_MIGRATOR`. For more information, see [Snowpark Container Services costs](https://docs.snowflake.com/en//developer-guide/snowpark-container-services/accounts-orgs-usage-views).

For more information, see [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

## Limitations of SnowConvert AI Verification[¶](#limitations-of-snowconvert-ai-verification "Link to this heading")

The initial version is optimized for standard SQL Server migrations. While it can handle many query types, all the changes generated by SnowConvert AI Verification must be reviewed by the customer before deploying them to any account.

## Legal notices for AI features[¶](#legal-notices-for-ai-features "Link to this heading")

Your use of Snowflake AI features is subject to all agreements, terms or policies that apply to such usage, including but not limited to those documented in the [Snowflake AI & ML Documentation](https://docs.snowflake.com/en/guides-overview-ai-features).

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

1. [Introduction](#introduction)
2. [Key features of SnowConvert AI Verification](#key-features-of-snowconvert-ai-verification)
3. [Prerequisites for SnowConvert AI Verification](#prerequisites-for-snowconvert-ai-verification)
4. [Getting started with SnowConvert AI Verification](#getting-started-with-snowconvert-ai-verification)
5. [Billing and cost considerations with SnowConvert AI Verification](#billing-and-cost-considerations-with-snowconvert-ai-verification)
6. [Limitations of SnowConvert AI Verification](#limitations-of-snowconvert-ai-verification)
7. [Legal notices for AI features](#legal-notices-for-ai-features)