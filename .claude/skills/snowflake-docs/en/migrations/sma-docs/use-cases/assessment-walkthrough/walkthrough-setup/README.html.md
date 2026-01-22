---
auto_generated: true
description: This guide offers practical experience with the Snowpark Migration Accelerator
  (SMA). Through real-world examples, you will learn how to evaluate code and interpret
  assessment results, giving you a cl
last_scraped: '2026-01-14T16:54:55.877975+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/sma-docs/use-cases/assessment-walkthrough/walkthrough-setup/README.html
title: 'Snowpark Migration Accelerator: Walkthrough Setup | Snowflake Documentation'
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

      * [SnowConvert AI](../../../../snowconvert-docs/overview.md)
      * [Snowpark Migration Accelerator](../../../README.md)

        + General

          + [Introduction](../../../general/introduction.md)
          + [Getting started](../../../general/getting-started/README.md)
          + [Conversion software terms of use](../../../general/conversion-software-terms-of-use/README.md)
          + [Release notes](../../../general/release-notes/README.md)
          + [Roadmap](../../../general/roadmap.md)
        + User guide

          + [Overview](../../../user-guide/overview.md)
          + [Before using the SMA](../../../user-guide/before-using-the-sma/README.md)
          + [Project overview](../../../user-guide/project-overview/README.md)
          + [Technical discovery](../../../user-guide/project-overview/optional-technical-discovery.md)
          + [AI assistant](../../../user-guide/chatbot.md)
          + [Assessment](../../../user-guide/assessment/README.md)
          + [Conversion](../../../user-guide/conversion/README.md)
          + [Using the SMA CLI](../../../user-guide/using-the-sma-cli/README.md)
        + Use cases

          + Snowflake VS Code extension

            + [SMA checkpoints walkthrough](../../sma-checkpoints-walkthrough/README.md)
            + [SMA EWI Assistant walkthrough](../../sma-ewi-assistant-walkthrough/README.md)
          + [Assessment walkthrough](../README.md)

            - [Walkthrough setup](README.md)

              * [Notes on code preparation](notes-on-code-preparation.md)
            - [Running the tool](../running-the-tool.md)
            - [Interpreting the assessment output](../interpreting-the-assessment-output/README.md)
            - [Running the SMA again](../running-the-sma-again.md)
          + [Conversion walkthrough](../../conversion-walkthrough.md)
          + [Migration lab](../../migration-lab/README.md)
          + [Sample project](../../sample-project.md)
          + [Using SMA in an Ubuntu Docker image](../../using-snowconvert-in-a-ubuntu-docker-image.md)
          + [SMA CLI walkthrough](../../sma-cli-walkthrough.md)
          + [Snowpark Connect](../../snowpark-connect/README.md)
        + Issue analysis

          + [Approach](../../../issue-analysis/approach.md)
          + [Issue code categorization](../../../issue-analysis/issue-code-categorization.md)
          + [Issue codes by source](../../../issue-analysis/issue-codes-by-source/README.md)
          + [Troubleshooting the output code](../../../issue-analysis/troubleshooting-the-output-code/README.md)
          + [Workarounds](../../../issue-analysis/workarounds.md)
          + [Deploying the output code](../../../issue-analysis/deploying-the-output-code.md)
        + Translation reference

          + [Translation reference overview](../../../translation-reference/translation-reference-overview.md)
          + [SIT tagging](../../../translation-reference/sit-tagging/README.md)
          + [SQL embedded code](../../../translation-reference/sql-embedded-code.md)
          + [HiveSQL](../../../translation-reference/hivesql/README.md)
          + [Spark SQL](../../../translation-reference/spark-sql/README.md)
        + Workspace estimator

          + [Overview](../../../workspace-estimator/overview.md)
          + [Getting started](../../../workspace-estimator/getting-started.md)
        + Interactive assessment application

          + [Overview](../../../interactive-assessment-application/overview.md)
          + [Installation guide](../../../interactive-assessment-application/installation-guide.md)
        + Support

          + [General troubleshooting](../../../support/general-troubleshooting/README.md)
          + [Frequently asked questions](../../../support/frequently-asked-questions-faq/README.md)
          + [Glossary](../../../support/glossary.md)
          + [Contact us](../../../support/contact-us.md)
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

[Guides](../../../../../guides/README.md)[Migrations](../../../../README.md)Tools[Snowpark Migration Accelerator](../../../README.md)Use cases[Assessment walkthrough](../README.md)Walkthrough setup

# Snowpark Migration Accelerator: Walkthrough Setup[¶](#snowpark-migration-accelerator-walkthrough-setup "Link to this heading")

This guide offers practical experience with the Snowpark Migration Accelerator (SMA). Through real-world examples, you will learn how to evaluate code and interpret assessment results, giving you a clear understanding of the tool’s capabilities.

## Materials[¶](#materials "Link to this heading")

To complete this tutorial, you will need the following:

* A computer that has Snowpark Migration Accelerator (SMA) software installed
* Access to the sample code files on the same computer

To begin, you will need two items on your computer:

1. The Snowpark Migration Accelerator (SMA) tool
2. Code samples

Let’s walk through how to obtain these essential resources.

### SMA Application[¶](#sma-application "Link to this heading")

The Snowpark Migration Accelerator (SMA) helps developers convert their PySpark and Spark Scala applications to run on Snowflake. It automatically detects Spark API calls in your Python or Scala code and transforms them into equivalent Snowpark API calls. This guide will demonstrate basic SMA functionality by analyzing sample Spark code and showing how it assists with migration projects.

During the initial assessment phase, Snowpark Migration Accelerator (SMA) examines your source code and builds a detailed model that captures all the functionality in your code. Based on this analysis, SMA creates several reports, including a detailed assessment report that we’ll review in this walkthrough. These reports help you understand how ready your code is for migration to Snowpark and estimate the effort needed for the transition. We’ll look at these findings in more detail as we continue through this lab.

#### Download and Installation[¶](#download-and-installation "Link to this heading")

To begin an assessment with the Snowpark Migration Accelerator (SMA), you only need to complete the installation process. While Snowflake provides optional [helpful training on using the SMA](https://learn.snowflake.com/en/courses/spark-to-snowpark-sma/), you can proceed without it. No special access codes are needed. Simply:

1. Visit our [Download and Access](../../../general/getting-started/download-and-access) section
2. [Download the installer](https://www.snowflake.com/en/data-cloud/snowpark/migration-accelerator/)
3. Follow our [Installation instructions](../../../general/getting-started/installation/README) to set up the application on your computer

### Sample Codebase[¶](#sample-codebase "Link to this heading")

This guide uses Python code examples to demonstrate the migration process. We have selected two publicly available sample codebases from third-party Git repositories as unbiased, real-world examples. You can access these codebases at:

* PySpark Data Engineering Examples: <https://github.com/spark-examples/pyspark-examples>
* Apache Spark Machine Learning Examples: <https://github.com/apache/spark/tree/master/examples/src/main/python>

To analyze codebases using the Snowpark Migration Accelerator (SMA), follow these steps:

1. Download the codebases as zip files from GitHub. You can find instructions on how to do this in the [GitHub documentation](https://docs.github.com/en/repositories/working-with-files/using-files/downloading-source-code-archives).
2. Create separate folders on your computer for each codebase.
3. Extract each zip file into its designated folder, as shown in the image below:

![Directory with Codebases](../../../../../_images/image%28542%29.png)

These sample codebases demonstrate how SMA evaluates Spark API references to calculate the [Spark API Readiness Score](../../../user-guide/assessment/readiness-scores.html#snowpark-api-readiness-score). Let’s look at two scenarios:

1. A codebase that received a high score, indicating it is highly compatible with Snowpark and ready for migration
2. A codebase that received a low score, indicating it requires additional review and potential modifications before migration

While the readiness score provides valuable insight, it should not be the only factor considered when planning a migration. A comprehensive evaluation of all aspects is necessary for both high and low scoring assessments to ensure a successful migration.

After unzipping the directories, SMA will analyze only files that use supported code formats and notebook formats. These files are checked for references to Spark API and other Third Party APIs. To see which file types are supported, please check the list [here](../../../user-guide/before-using-the-sma/supported-filetypes).

Throughout the rest of this walkthrough, we will analyze how these two codebases execute.

## Support[¶](#support "Link to this heading")

For help with installation or to get access to the code, please email [sma-support@snowflake.com](mailto:sma-support%40snowflake.com).

---

After downloading and unzipping the codebases into separate directories, you can either:

* Move on to [running the tool](../running-the-tool)
* Review [the code preparation notes](notes-on-code-preparation)

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

1. [Materials](#materials)
2. [Support](#support)