---
auto_generated: true
description: 'Now that you have installed the Snowpark Migration Accelerator (SMA)
  and prepared your codebase, you can begin the execution process. Return to the SMA
  application if it’s still open, or launch it if '
last_scraped: '2026-01-14T16:51:58.723619+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/sma-docs/use-cases/assessment-walkthrough/running-the-tool
title: 'Snowpark Migration Accelerator: Running the Tool | Snowflake Documentation'
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

          + [Overview](../../user-guide/overview.md)
          + [Before using the SMA](../../user-guide/before-using-the-sma/README.md)
          + [Project overview](../../user-guide/project-overview/README.md)
          + [Technical discovery](../../user-guide/project-overview/optional-technical-discovery.md)
          + [AI assistant](../../user-guide/chatbot.md)
          + [Assessment](../../user-guide/assessment/README.md)
          + [Conversion](../../user-guide/conversion/README.md)
          + [Using the SMA CLI](../../user-guide/using-the-sma-cli/README.md)
        + Use cases

          + Snowflake VS Code extension

            + [SMA checkpoints walkthrough](../sma-checkpoints-walkthrough/README.md)
            + [SMA EWI Assistant walkthrough](../sma-ewi-assistant-walkthrough/README.md)
          + [Assessment walkthrough](README.md)

            - [Walkthrough setup](walkthrough-setup/README.md)
            - [Running the tool](running-the-tool.md)
            - [Interpreting the assessment output](interpreting-the-assessment-output/README.md)
            - [Running the SMA again](running-the-sma-again.md)
          + [Conversion walkthrough](../conversion-walkthrough.md)
          + [Migration lab](../migration-lab/README.md)
          + [Sample project](../sample-project.md)
          + [Using SMA in an Ubuntu Docker image](../using-snowconvert-in-a-ubuntu-docker-image.md)
          + [SMA CLI walkthrough](../sma-cli-walkthrough.md)
          + [Snowpark Connect](../snowpark-connect/README.md)
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[Snowpark Migration Accelerator](../../README.md)Use cases[Assessment walkthrough](README.md)Running the tool

# Snowpark Migration Accelerator: Running the Tool[¶](#snowpark-migration-accelerator-running-the-tool "Link to this heading")

Now that you have installed the Snowpark Migration Accelerator (SMA) and prepared your codebase, you can begin the execution process. Return to the SMA application if it’s still open, or launch it if you’ve closed it.

## Project Setup[¶](#project-setup "Link to this heading")

When you first open the tool, you may see a Start/Activate page. If you do, click the “Start” button to begin.

![Start or Activate](../../../../_images/image%28526%29.png)

If you are a returning SMA user, you may bypass the welcome page and go directly to the project page. New users will see the welcome page and can click “Start” to access the project page.

![Project Page](../../../../_images/01-ProjectPage.png)

From the menu, select “New Project” to begin. If you have already created a project for this walkthrough, you can access it by selecting “Open Project” instead.

The “Project Creation” page allows you to create a new project file, which is essential for both assessment and code conversion tasks in SMA. The project file (with a .snowma extension) is stored in your selected source directory and keeps track of all your SMA executions. If you want to link multiple executions together, you can reopen an existing project file. All project information is saved both on your local machine and in the shared database. For more details about projects, see [the “project” file](../../user-guide/project-overview/project-setup).

All fields shown are required for configuring the assessment tool and managing the project after running the analysis. The following image explains each available option:

![Project Creation Page](../../../../_images/image%28537%29.png)

For this walkthrough, we will use the “Spark Data Engineering Examples” codebase. You can find it in the [sample codebases section](walkthrough-setup/README). Follow these steps:

1. Download and unzip the codebase
2. Locate the root directory containing all files - this will be your input directory
3. Choose any project name you prefer
4. Select an output directory (the tool will suggest a default location, but you can change it as needed)

Before starting the assessment, make sure your input directory contains the correct source code files with the proper file extensions, as explained in the [code preparation](walkthrough-setup/notes-on-code-preparation) section.

When you are ready to begin, click the “SAVE & START ASSESSMENT” button located in the bottom right corner of the screen.

### Execution and Assessment Output[¶](#execution-and-assessment-output "Link to this heading")

When you start the assessment process, SMA analyzes your source code in three steps:

1. First, it performs a basic scan to create an inventory of all files and keywords in your codebase.
2. Then, it parses the code according to your source language and creates a semantic model that represents the code’s functionality.
3. Finally, it uses this model to generate detailed information, including the [Spark Reference Inventory](../../user-guide/assessment/output-reports/sma-inventories) and [Import Library Analysis](../../user-guide/assessment/output-reports/sma-inventories). In conversion mode, it also produces the converted code.

During this process, you will see three progress indicators on the screen:

* Loading Source Code
* Analyzing Source Code
* Writing Results

These indicators will light up as each step is completed.

![Execution Page](../../../../_images/04-ExecutionandAssessmentOutput.png)

After the analysis is complete, click “View Results” to see the analysis output.

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

1. [Project Setup](#project-setup)