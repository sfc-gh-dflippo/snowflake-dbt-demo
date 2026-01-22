---
auto_generated: true
description: 'You can install the Snowpark Migration Accelerator (SMA) on Windows
  in two ways:'
last_scraped: '2026-01-14T16:51:18.024107+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/sma-docs/general/getting-started/installation/windows-installation
title: 'Snowpark Migration Accelerator: Windows Installation | Snowflake Documentation'
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

          + [Introduction](../../introduction.md)
          + [Getting started](../README.md)

            - [Download and access](../download-and-access.md)
            - [Installation](README.md)

              * [Linux installation](linux-installation.md)
              * [Macos installation](macos-installation.md)
              * [Windows installation](windows-installation.md)
          + [Conversion software terms of use](../../conversion-software-terms-of-use/README.md)
          + [Release notes](../../release-notes/README.md)
          + [Roadmap](../../roadmap.md)
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

            + [SMA checkpoints walkthrough](../../../use-cases/sma-checkpoints-walkthrough/README.md)
            + [SMA EWI Assistant walkthrough](../../../use-cases/sma-ewi-assistant-walkthrough/README.md)
          + [Assessment walkthrough](../../../use-cases/assessment-walkthrough/README.md)
          + [Conversion walkthrough](../../../use-cases/conversion-walkthrough.md)
          + [Migration lab](../../../use-cases/migration-lab/README.md)
          + [Sample project](../../../use-cases/sample-project.md)
          + [Using SMA in an Ubuntu Docker image](../../../use-cases/using-snowconvert-in-a-ubuntu-docker-image.md)
          + [SMA CLI walkthrough](../../../use-cases/sma-cli-walkthrough.md)
          + [Snowpark Connect](../../../use-cases/snowpark-connect/README.md)
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

[Guides](../../../../../guides/README.md)[Migrations](../../../../README.md)Tools[Snowpark Migration Accelerator](../../../README.md)General[Getting started](../README.md)[Installation](README.md)Windows installation

# Snowpark Migration Accelerator: Windows Installation[¶](#snowpark-migration-accelerator-windows-installation "Link to this heading")

You can install the Snowpark Migration Accelerator (SMA) on Windows in two ways:

* As a desktop application with a graphical interface
* As a Command Line Interface (CLI)

Instructions for both installation methods are provided below.

If you need the application or CLI files, please check the [Downloading and License Access page](../download-and-access) for detailed instructions on how to obtain them.

## Installing the SMA Application on Windows[¶](#installing-the-sma-application-on-windows "Link to this heading")

Follow these steps to install the Snowpark Migration Accelerator (SMA) application on Windows:

1. **Run the Installer:** Double-click the downloaded installer file (with .exe extension).
2. **Follow the Installation Wizard:** A setup wizard will appear. Simply follow the prompts to install the software.
3. **Open the SMA:** After installation completes, launch the Snowpark Migration Accelerator (SMA) from your Windows Start menu.

![SMA in Windows App Menu](../../../../../_images/image%28506%29.png)

After launching the application, you have two options:

* Create a new assessment or conversion project
* Open a project you have previously created

![SMA Start Screen](../../../../../_images/image%28507%29.png)

Great! Now that you’ve completed the installation, you can start using the Snowpark Migration Accelerator (SMA) application. For detailed instructions on how to use SMA, please refer to the [SMA User Guide](../../../user-guide/overview).

**Important Note:**

When a newer version of SMA is available, you will see an “UPDATE NOW” button in the top right corner of your screen. Simply click this button to download and install the latest version.

If you experience any problems while installing the software, please email our support team at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com).

## Installing the SMA CLI on Windows[¶](#installing-the-sma-cli-on-windows "Link to this heading")

Here’s how to install the Snowpark Migration Accelerator (SMA) Command Line Interface on Windows:

1. **Download the .zip File:** Download the SMA CLI `.zip` file from the [Downloading and License Access page](../download-and-access).
2. **Extract the Files:** Unzip the downloaded file to a location on your computer (for example, `C:sma-cli`).
3. **Copy the Orchestrator Path:** Find and copy the full path to the `orchestrator` folder in the extracted files.
   ![Orchestrator Folder Path](../../../../../_images/image%2812%291.png)
4. **Open Environment Variables:** Type “environment variables for your account” in the Windows search bar and select **Edit environment variables for your account**.
   ![Environment Variables Search](../../../../../_images/image%2811%291.png)
5. **Edit the Path Variable:** Find and select the “Path” variable in the “User variables” section, then click **Edit**.
6. **Add the Orchestrator Path:** Click **New** and paste the copied orchestrator path.
   ![Add Path Variable](../../../../../_images/image.png)
7. **Save Changes:** Click **OK** twice to save and close both windows.
8. **Open a Command Prompt:** Launch a new command prompt window.
9. **Verify Installation:** Run `sma --version` to confirm the installation was successful.

![SMA CLI Version](../../../../../_images/image%2813%29.png)

After installing either the application or Command Line Interface (CLI), you can begin using the Snowpark Migration Accelerator (SMA). For detailed instructions, please refer to the [SMA User Guide](../../../user-guide/overview).

If you experience any problems while installing the software, please email our support team at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com).

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

1. [Installing the SMA Application on Windows](#installing-the-sma-application-on-windows)
2. [Installing the SMA CLI on Windows](#installing-the-sma-cli-on-windows)