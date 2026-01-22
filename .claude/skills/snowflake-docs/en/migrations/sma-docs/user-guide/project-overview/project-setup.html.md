---
auto_generated: true
description: 'When you first open the Snowpark Migration Accelerator (SMA), you will
  see two options:'
last_scraped: '2026-01-14T16:54:56.146182+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/sma-docs/user-guide/project-overview/project-setup.html
title: 'Snowpark Migration Accelerator:  Project Setup | Snowflake Documentation'
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
          + [Project overview](README.md)

            - [Project setup](project-setup.md)
            - [Configuration and settings](configuration-and-settings.md)
            - [Tool execution](tool-execution.md)
          + [Technical discovery](optional-technical-discovery.md)
          + [AI assistant](../chatbot.md)
          + [Assessment](../assessment/README.md)
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[Snowpark Migration Accelerator](../../README.md)User guide[Project overview](README.md)Project setup

# Snowpark Migration Accelerator: Project Setup[¶](#snowpark-migration-accelerator-project-setup "Link to this heading")

When you first open the Snowpark Migration Accelerator (SMA), you will see two options:

* **Start**: Begin working on a new project
* **Activate**: Enter an access code to use the conversion features only

## Start Page[¶](#start-page "Link to this heading")

![Start or Activate](../../../../_images/image%2856%29.png)

The following section explains each available option:

* **Start** - Opens the Project Page where you can create a new project, open an existing one, or explore a sample project.
* **Activate** - Opens the activation page where you can enter or request an access code if you or your organization is eligible.

Note

If you have previously entered an access code, you will skip this screen and be directed to the Project Page.

## Project Page[¶](#project-page "Link to this heading")

On the project page, you will find the following three options:

![Accelerator Project Page](../../../../_images/01-AcceleratorProjectPage.png)

On this page, you will find three available options:

* **Open Project** - Browse and select a previously created project file. For more details about opening an existing project, see [more information on opening an existing project](#open-a-project).
* **New Project** - Select this option to create a new project. Learn more about [creating a new project](#creating-a-new-project).
* **See sample project** - Try out a sample project to familiarize yourself with SMA. For step-by-step instructions, visit the [running the sample project](../../use-cases/sample-project) guide.

## Creating a New Project[¶](#creating-a-new-project "Link to this heading")

Clicking the “New Project” button will open the project creation screen.

![Project Creation Page](../../../../_images/image%28536%29.png)

The Project Creation page contains multiple fields that you need to complete.

1. **Project Name**: Enter a name for your project. This name will be used to store your settings and track multiple executions. More details about project files are provided below.
2. **Input Folder Path**: Select the folder containing your source code. Note that SMA will only analyze [supported file types](../before-using-the-sma/supported-filetypes). You can:

   * Choose a specific subfolder or file by using the radio buttons next to folder names
   * Analyze only part of your codebase by selecting a specific subdirectory

![Subfolder Drop Down Menu](../../../../_images/image%28487%29.png)

* **Note:** When you hover over a path label, a tooltip displays the complete path. This applies to all fields containing shortened paths (input folder path, output folder path, etc.).

  + The .snowma project file is created in this directory when you create the project. See below for more details about this folder.

3. **Output Folder Path**: Select the directory where SMA will store output files, including logs, reports, and converted code (in conversion mode).
4. **SQL Language**: Select either SparkSQL or HiveSQL based on your source code. (Optional)
5. **Email Address**: Enter your email address to identify yourself as a tool user. Snowflake will only use this email to send you the Snowpark qualification report and your conversion access code if you proceed to conversion mode.
6. **Customer’s Company**: Enter the name of the organization whose code you are working with. If you are analyzing your own code, enter your organization’s name. If you are working with another organization’s code, enter their name. This helps organize projects by organization.

All fields must be completed to run the tool.

After completing your project setup, you have three options:

* Click “Save & Start Assessment” to save your project and begin the assessment process
* Click “Save & Skip Assessment” to save your project without running an assessment
* Click “Cancel” to exit without saving

![Project Creation Next Steps](../../../../_images/image%28488%29.png)

Before proceeding with the conversion process, you need to decide whether to perform an assessment. We recommend starting with the assessment unless you are certain that you want to skip directly to conversion. If you have any doubts, it’s best to begin with the assessment phase.

Clicking “Cancel” returns you to the main screen. If you choose “Start” or “Skip,” your project settings will be saved in a .snowma file. This file allows you to reopen the project later with all your configured settings intact.

## Notes on the SMA Project File (.snowma)[¶](#notes-on-the-sma-project-file-snowma "Link to this heading")

The .snowma file is a project configuration file that stores your project settings and assessment history. This file allows you to:

* Rerun the tool using the same configuration settings
* Access and review assessment data from previous runs

Each time you click “Save & Skip Assessment” or “Save & Start Assessment,” SMA creates a project file (with a .snowma extension) in your selected input folder. This project file, marked with the SMA icon, contains the source code you want to convert.

![.snowma project file](../../../../_images/image%2847%29.png)

As a user, you will have the following capabilities:

* Double-click the .snowma file to open an existing project
* Click “Open Project” on the main screen to open an existing project

![Project Page](../../../../_images/03-ProjectPage.png)

Viewing Recently Opened Projects:
To see a list of your recently opened projects in SMA, click File > Open Recents in the menu bar.

![Open Recents](../../../../_images/image%2859%29.png)

When you resume any of these workflows, the tool will return you to the same point where you left off in your previous session.

## Open a Project[¶](#open-a-project "Link to this heading")

From the main screen, click **Open Project** to launch your file browser. Select a project file with a .snowma extension to open the Project Creation page. This action works regardless of your project’s completion status.

The navigation panel on the Project Creation page allows you to revisit any previously accessed screens.

![Navigation Panel](../../../../_images/04-NavigationPanel.png)

After completing your project details, click “Save & Start Assessment” to begin running the accelerator.

The following section explains the available configuration options and settings when using the application.

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

1. [Start Page](#start-page)
2. [Project Page](#project-page)
3. [Creating a New Project](#creating-a-new-project)
4. [Notes on the SMA Project File (.snowma)](#notes-on-the-sma-project-file-snowma)
5. [Open a Project](#open-a-project)