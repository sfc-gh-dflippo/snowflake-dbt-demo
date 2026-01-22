---
auto_generated: true
description: Setting up a new project with the Snowpark Migration Accelerator (SMA)
  is a simple process. This page explains all available settings, updates, and customization
  options within the application.
last_scraped: '2026-01-14T16:52:08.903192+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/sma-docs/user-guide/project-overview/configuration-and-settings
title: 'Snowpark Migration Accelerator: Configuration and Settings | Snowflake Documentation'
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[Snowpark Migration Accelerator](../../README.md)User guide[Project overview](README.md)Configuration and settings

# Snowpark Migration Accelerator: Configuration and Settings[¶](#snowpark-migration-accelerator-configuration-and-settings "Link to this heading")

Setting up a new project with the Snowpark Migration Accelerator (SMA) is a simple process. This page explains all available settings, updates, and customization options within the application.

## Updating the Application[¶](#updating-the-application "Link to this heading")

The Snowpark Migration Accelerator (SMA) automatically checks for new versions when you start the program. If a newer version is available, you’ll see a notification message in the upper-right corner of your screen.

![Pending Updates](../../../../_images/1-PendingUpdates.png)

If you select “Update Now,” the application will immediately download and install the latest version.

![Downloading Update](../../../../_images/2-DownloadingUpdate%281%29.png)

After the download completes, click “Close and Install” to update the application.

![Download Successful](../../../../_images/3-DownloadSuccessful.png)

After the application restarts, you can verify the current version number in the top-right corner of the window.

![Update Complete](../../../../_images/4-UpdateComplete.png)

### Check for Updates[¶](#check-for-updates "Link to this heading")

To check for a new version of the application, click the “Check for Updates” option in the menu.

If your application is up to date, you will see a notification in the top right corner confirming this status.

![Check for Updates - Up to Date](../../../../_images/5.1-CheckforUpdates-UptoDate.png)

If your application is not running the latest version, you will be prompted to update it.

![Check for Updates - Update](../../../../_images/5.2-CheckforUpdates-Update.png)

### Conversion Settings[¶](#conversion-settings "Link to this heading")

Before starting a conversion process, you can configure your conversion settings using one of these two options:

From the menu bar at the top of the screen:

![Menu bar option for Conversion Settings](../../../../_images/image%28547%29.png)

On the Conversion Screen:

![Conversion setting option](../../../../_images/image%28548%29.png)

The conversion settings section contains a list of available conversion settings. To access these settings:

Convert Pandas to Snowpark: Choose whether to automatically convert Pandas code to Snowpark’s equivalent Pandas API (Snow Pandas). When enabled, the tool will transform any Pandas operations it finds in your code to their Snowpark counterparts.

![Conversion settings](../../../../_images/image%28549%29.png)

## About[¶](#about "Link to this heading")

To view the version information for your Snowpark Migration Accelerator installation, click the **About Snowpark Migration Accelerator** option in the menu.

![About Snowpark Migration Accelerator](../../../../_images/AboutSMA.png)

To review changes between different versions, please check the release notes.

## File Menu[¶](#file-menu "Link to this heading")

From the File menu, you can either:

* Create a new project by selecting **New Project**
* Open a previously used project from the **Open Recents** menu

![File Menu](../../../../_images/7-FileMenu.png)

When you select either “New Project” or open a different project, a prompt will appear asking if you want to “Save Changes & Create New Project”.

## Help Menu[¶](#help-menu "Link to this heading")

The help menu provides several support options tailored to your specific needs.

![Help Menu](../../../../_images/8-HelpMenu.png)

The following sections describe each option available in the help menu.

### Documentation[¶](#documentation "Link to this heading")

To return to the main documentation page (Welcome!), click [here](../../README).

### Release Notes[¶](#release-notes "Link to this heading")

The release notes can be found in the general section of our documentation site. Click [here](../../general/release-notes/README) to view them.

### Glossary[¶](#glossary "Link to this heading")

The Glossary option directs you to the [Glossary](../../support/glossary) section, where you can find definitions of terms used throughout this documentation.

### Request New Access Code[¶](#request-new-access-code "Link to this heading")

Access codes are required to use SMA’s conversion features. You must have a valid access code to perform any conversions.

You can obtain an access code by clicking **Inquire about an access code** in the help menu.

![Inquire about an access code from the Help Menu](../../../../_images/9-InquireaboutanaccesscodefromtheHelpMenu.png)

The **Request Access Code** form will appear (as shown below). If you need an access code or are unsure if you have one, contact the Snowpark Migration Accelerator (SMA) support team at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com).

When requesting an access code, the Snowpark Migration Accelerator (SMA) will ask you to provide the following information:

![Request an Access Code](../../../../_images/10-RequestandAccessCode.png)

The access code will be sent to the email address you provide. All fields must be completed to receive your access code.

### Contact Us[¶](#contact-us "Link to this heading")

The Contact Us button opens your default email application. When clicked, it allows you to send an email to [sma-info@snowflake.com](mailto:sma-info%40snowflake.com) to discuss any questions or concerns about the Snowpark Migration Accelerator.

For additional ways to reach the Snowpark Migration Accelerator (SMA) team, please visit our [contact us section](../../support/contact-us).

### Report an Issue[¶](#report-an-issue "Link to this heading")

You can report issues at any time. This includes problems encountered while running the tool or any other concerns related to using the tool.

When you select this issue, a form will be displayed.

![Report an Issue](../../../../_images/image%28472%29.png)

To help us resolve your issue quickly, please provide:

1. A detailed description of the problem
2. Your email address so we can contact you
3. Any relevant files, such as screenshots showing the problem
4. Log files from when you ran the tool

After submitting the issue, the SMA support team will be notified. If you provided your email address, our team will contact you promptly.

### Online Settings[¶](#online-settings "Link to this heading")

The Snowpark Migration Accelerator (SMA) connects to Snowflake to perform specific operations. It’s important to note that your code is never transmitted to Snowflake. The tool communicates with Snowflake in three specific situations:

1. When a user requests validation or makes a specific request
2. When an execution is initiated
3. During tool startup

You can disable the second and third types of communication through the **Online Settings** menu. Let’s examine the details of each communication scenario.

The SMA tool communicates with Snowflake through a telemetry API for the following activities:

* Request an [access code](#request-new-access-code)
* Check if the access code is valid
* Submit issues to Snowflake when users fill out the [Report an Issue](#report-an-issue) form
* Send crash reports and fatal error logs to Snowflake when users agree to report them
* Download and install tool updates

The SMA sends summary information to a telemetry API each time the tool runs. This information includes:

* Project assessment details, including project information and statistics on Spark usage patterns
* Tool usage metrics, including button interaction data and operational logs

When you start the tool, it makes a single connection to Snowflake to verify your credentials and access.

Check if a newer version is available.

You can enable or disable all of these information settings. To modify these settings, follow these steps:

1. Open the Help menu in SMA
2. Select **Online Settings**

Note that SMA can operate completely offline after configuring these settings.

![Choosing Online Settings from the Help Menu](../../../../_images/image%28551%29.png)

When you click **Online Settings**, a menu appears with the following options:

![The online settings menu](../../../../_images/image%28552%29.png)

You can enable or disable any of these settings according to your needs.

The tool can operate without an internet connection. In offline mode, you can run assessments without any issues. However, to perform conversions, the tool needs to validate your access code online. If you cannot connect to the internet, contact the SMA team at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) to request a special offline access code.

### EULA[¶](#eula "Link to this heading")

This link directs you to the [End User License Agreement (EULA) page](../../general/conversion-software-terms-of-use/README) where you can review the terms of use.

---

Let’s start using the Snowpark Migration Accelerator (SMA) tool to convert your code.

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

1. [Updating the Application](#updating-the-application)
2. [About](#about)
3. [File Menu](#file-menu)
4. [Help Menu](#help-menu)