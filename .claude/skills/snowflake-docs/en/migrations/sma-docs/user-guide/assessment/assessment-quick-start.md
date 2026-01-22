---
auto_generated: true
description: The Snowpark Migration Accelerator (SMA) helps you analyze your source
  code by generating detailed reports and inventories. This guide will show you how
  to begin the assessment process.
last_scraped: '2026-01-14T16:51:44.593197+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/sma-docs/user-guide/assessment/assessment-quick-start
title: 'Snowpark Migration Accelerator: Assessment Quick Start | Snowflake Documentation'
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

      * [SnowConvert AI](../../../snowconvert-docs/overview.md)
      * [Snowpark Migration Accelerator](../../README.md)

        + General

          + [Introduction](../../general/introduction.md)
          + [Getting started](../../general/getting-started/README.md)
          + [Conversion software terms of use](../../general/conversion-software-terms-of-use/README.md)
          + [Release notes](../../general/release-notes/README.md)
          + [Roadmap](../../general/roadmap.md)
        + User guide

          + [Overview](../overview.md)
          + [Before using the SMA](../before-using-the-sma/README.md)
          + [Project overview](../project-overview/README.md)
          + [Technical discovery](../project-overview/optional-technical-discovery.md)
          + [AI assistant](../chatbot.md)
          + [Assessment](README.md)

            - [How the assessment works](how-the-assessment-works.md)
            - [Assessment quick start](assessment-quick-start.md)
            - [Understanding the assessment summary](understanding-the-assessment-summary.md)
            - [Readiness scores](readiness-scores.md)
            - [Output reports](output-reports/README.md)
            - [Output logs](output-logs.md)
            - [Spark reference categories](spark-reference-categories.md)
          + [Conversion](../conversion/README.md)
          + [Using the SMA CLI](../using-the-sma-cli/README.md)
        + Use cases

          + Snowflake VS Code extension

            + [SMA checkpoints walkthrough](../../use-cases/sma-checkpoints-walkthrough/README.md)
            + [SMA EWI Assistant walkthrough](../../use-cases/sma-ewi-assistant-walkthrough/README.md)
          + [Assessment walkthrough](../../use-cases/assessment-walkthrough/README.md)
          + [Conversion walkthrough](../../use-cases/conversion-walkthrough.md)
          + [Migration lab](../../use-cases/migration-lab/README.md)
          + [Sample project](../../use-cases/sample-project.md)
          + [Using SMA in an Ubuntu Docker image](../../use-cases/using-snowconvert-in-a-ubuntu-docker-image.md)
          + [SMA CLI walkthrough](../../use-cases/sma-cli-walkthrough.md)
          + [Snowpark Connect](../../use-cases/snowpark-connect/README.md)
        + Issue analysis

          + [Approach](../../issue-analysis/approach.md)
          + [Issue code categorization](../../issue-analysis/issue-code-categorization.md)
          + [Issue codes by source](../../issue-analysis/issue-codes-by-source/README.md)
          + [Troubleshooting the output code](../../issue-analysis/troubleshooting-the-output-code/README.md)
          + [Workarounds](../../issue-analysis/workarounds.md)
          + [Deploying the output code](../../issue-analysis/deploying-the-output-code.md)
        + Translation reference

          + [Translation reference overview](../../translation-reference/translation-reference-overview.md)
          + [SIT tagging](../../translation-reference/sit-tagging/README.md)
          + [SQL embedded code](../../translation-reference/sql-embedded-code.md)
          + [HiveSQL](../../translation-reference/hivesql/README.md)
          + [Spark SQL](../../translation-reference/spark-sql/README.md)
        + Workspace estimator

          + [Overview](../../workspace-estimator/overview.md)
          + [Getting started](../../workspace-estimator/getting-started.md)
        + Interactive assessment application

          + [Overview](../../interactive-assessment-application/overview.md)
          + [Installation guide](../../interactive-assessment-application/installation-guide.md)
        + Support

          + [General troubleshooting](../../support/general-troubleshooting/README.md)
          + [Frequently asked questions](../../support/frequently-asked-questions-faq/README.md)
          + [Glossary](../../support/glossary.md)
          + [Contact us](../../support/contact-us.md)
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[Snowpark Migration Accelerator](../../README.md)User guide[Assessment](README.md)Assessment quick start

# Snowpark Migration Accelerator: Assessment Quick Start[¶](#snowpark-migration-accelerator-assessment-quick-start "Link to this heading")

The Snowpark Migration Accelerator (SMA) helps you analyze your source code by generating detailed reports and inventories. This guide will show you how to begin the assessment process.

## How to Execute an Assessment[¶](#how-to-execute-an-assessment "Link to this heading")

To begin assessing your code, create a new project in the Snowpark Migration Accelerator (SMA) tool.

1. Begin by selecting the **New Project** button.

![New Project](../../../../_images/1-NewProject.png)

After you fill in all required project information, the **Save & Start Assessment** button becomes active and clickable.

![Start Assessment](../../../../_images/2-StartAssessment.png)

The progress screen displays the current status of the assessment. Once the assessment is complete, click **View Results** to continue.

![Progress Screen](../../../../_images/3-ProgressScreen.png)

The results screen provides detailed information to help you understand your current code and its potential migration to Snowpark. For a complete walkthrough of this output, please refer to the [Understanding the Assessment Summary](understanding-the-assessment-summary) section.

![Results Screen](../../../../_images/ResultsScreen%282%29.png)

Note that while you can find basic information in the [assessment summary](understanding-the-assessment-summary) page above, the complete [output folder](output-reports/README) contains much more detailed information, including a comprehensive multi-page report.

## Next Steps[¶](#next-steps "Link to this heading")

After the tool completes its analysis, you’ll need to review the results and determine your next steps. Here are some helpful tips to guide you:

* Consider the Readiness Score as an Initial Guide: While the readiness score evaluates Spark API compatibility, it’s important to understand that successful migration depends on multiple factors. These include compatibility with third-party libraries and whether Snowpark is the optimal solution for your specific workload.
* Take Time to Analyze the Assessment Results: The assessment provides valuable insights that can help you create an effective migration strategy. Carefully review the assessment data before starting the conversion process to avoid unnecessary rework and ensure a more efficient migration.

Additional options are available in the application menu, as shown in the image below:
![](../../../../_images/image%2854%29.png)

* **Retry Assessment** - You can run the assessment again by clicking the **Retry Assessment** button on the Assessment Results page. This is useful when you’ve made changes to your source code and want to see updated results.
* **View Log Folder** - Opens the folder containing assessment execution logs. These logs are text files that show detailed information about the assessment process. They are particularly helpful for troubleshooting failed executions. If you need support, you may be asked to share these logs.
* **View Reports** - Opens the folder containing assessment output reports. These include the detailed assessment report, Spark reference inventory, and other analyses of your source codebase. Each report type is explained in detail in this documentation.
* **Continue to Conversion** - While this is the next step in the process, we recommend reviewing the assessment results thoroughly before proceeding. Note that you’ll need an access code to run the conversion. For more details, see the [conversion section of this documentation](../conversion/README).

For a detailed review of the assessment summary information, continue reading. However, if you’re ready to begin the conversion process, you can proceed directly to the conversion quick start guide.

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

The Snowpark Migration Accelerator tool (SMA) is subject to the [Conversion Software Terms of Use](https://www.snowflake.com/en/legal/technical-services-and-education/conversion-software-terms/).

On this page

1. [How to Execute an Assessment](#how-to-execute-an-assessment)
2. [Next Steps](#next-steps)