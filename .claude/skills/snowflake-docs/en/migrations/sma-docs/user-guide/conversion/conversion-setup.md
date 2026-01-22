---
auto_generated: true
description: 'When you first launch the Snowpark Migration Accelerator (SMA), you
  need to either create a new project or open an existing one. Each project can store
  multiple SMA executions for both Assessment and '
last_scraped: '2026-01-14T16:52:01.086425+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/sma-docs/user-guide/conversion/conversion-setup
title: 'Snowpark Migration Accelerator:  Conversion Setup | Snowflake Documentation'
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
          + [Assessment](../assessment/README.md)
          + [Conversion](README.md)

            - [How the conversion works](how-the-conversion-works.md)
            - [Conversion quick start](conversion-quick-start.md)
            - [Conversion setup](conversion-setup.md)
            - [Understanding the conversion assessment and reporting](understanding-the-conversion-assessment-and-reporting.md)
            - [Output code](output-code.md)
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[Snowpark Migration Accelerator](../../README.md)User guide[Conversion](README.md)Conversion setup

# Snowpark Migration Accelerator: Conversion Setup[¶](#snowpark-migration-accelerator-conversion-setup "Link to this heading")

When you first launch the Snowpark Migration Accelerator (SMA), you need to either create a new project or open an existing one. Each project can store multiple SMA executions for both Assessment and Conversion phases. After completing the Assessment phase, you will need to configure your project for the Conversion phase.

## Conversion Setup Page[¶](#conversion-setup-page "Link to this heading")

During the conversion process, you have several configuration options available, although most default settings should work well for most cases.

![Conversion Setup](../../../../_images/1-ConversionSetup.png)

**Input Folder Path** - This is the directory containing the code files you want to analyze. While this path can be the same as specified during [project creation](../project-overview/project-setup.html#creating-a-new-project), you can also choose a different directory. SMA will run a new assessment to ensure accurate conversion results, even if your code has changed since the initial assessment.

Note

* The tool only analyzes specific file extensions
* You can select specific subfolders or individual files by using the radio buttons next to folder names
* The assessment report will be generated again as part of this process

![Subfolder Drop Down Menu](../../../../_images/SubFolderMenu.png)

Note

When you hover your mouse over any path label in the interface, a tooltip will display the complete file path. This feature works for all fields containing shortened paths, such as input and output folder locations.

**Output Folder Path** - Select the destination folder where SMA will save all generated files, including logs, reports, and converted code.

**Enter a New Access Code** - Enter your access code in this field. If you don’t have an access code, you can request one. The process for obtaining an access code is explained in the next section.

Select **Change Conversion Settings** to change settings that govern details of the conversion. For more information, see [Conversion settings](#conversion-settings).

## Entering and Requesting an Access Code[¶](#entering-and-requesting-an-access-code "Link to this heading")

To perform a conversion using the Snowpark Migration Accelerator (SMA), you need an access code. These codes are typically linked to individual users or email addresses and determine which SMA features you can use. Note that you can run an Assessment without an access code - you’ll only be asked for one when you reach the Conversion Setup stage.

### Requesting an Access Code[¶](#requesting-an-access-code "Link to this heading")

An access code can be requested [through the help menu](../project-overview/configuration-and-settings.html#request-new-access-code) at any time. Alternatively, you can click **Inquire about an access code** on the Conversion Setup page.

![Inquire About an Access Code](../../../../_images/2-InquireAboutanAccessCode.png)

A request form for the access code will appear.

![Access Code Request Form](../../../../_images/3-AccessCodeRequestForm.png)

### Entering an Access Code[¶](#entering-an-access-code "Link to this heading")

After requesting an access code, it will be sent to the email address you provided in the form. The email will come from [sma-notifications@snowflake.com](mailto:sma-notifications%40snowflake.com). Please note that the access code will not appear automatically in the SMA interface - you must check your email to retrieve it.

![SMA Access Code Email](../../../../_images/4-SMAAccessCodeEmail.png)

Copy the access code from your email and paste it into the “Enter new access code or select one” field in the Conversion Setup. The access code consists of letters, dashes, and numbers, and must be entered exactly as shown in the email.

![Enter a New Access Code](../../../../_images/5-EnteraNewAccessCode.png)

Important Information for Access Code Validation:

* When entering the access code, press “**Enter**” (or “**Return**”) to activate it. Simply pasting the code is not enough - you must press “**Enter**”. The tool will display a message indicating whether the access code was successfully activated or failed. If you don’t see any message, click on the access code field and press “**Enter**” again.
* SMA validates access codes through the SMA Access API, which requires an internet connection. Without internet access, code validation and conversion features will not work. If your network security requires whitelisting the Access API, contact [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) for assistance with access code validation.

After validating your license, SMA displays a summary of your access code details. This includes the expiration date and the associated email address, as shown in the image above.

To obtain an access code for the Snowpark Migration Accelerator (SMA), please refer to the Access section in this documentation.

## Setup Complete[¶](#setup-complete "Link to this heading")

After configuring your conversion settings, click **Start Conversion** at the bottom of the application. This action will initiate both the SMA Assessment and Conversion processes. You will see the status screen, which is identical to the one displayed during the [Assessment phase](../assessment/understanding-the-assessment-summary).

![Conversion Complete](../../../../_images/6-ConversionComplete.png)

Click **View Results** to proceed to the Conversion Output screen.

## Conversion Settings[¶](#conversion-settings "Link to this heading")

With the following settings from the user interface, you can more finely control how the SMA performs conversion.

* **Pandas**

  **Convert Pandas API to Snowpark API** - Specifies to automatically convert Pandas code to the Snowpark equivalent Pandas API
  (Snowpark Pandas). When enabled, the tool transforms any Pandas operations it finds in your code into their Snowpark counterparts.
* **DBX**

  **Convert DBX notebooks to Snowflake notebooks** - Specifies to convert the .dbc into Jupyter files in a new folder with the .dbc name.

  Note

  When exporting notebooks, consider exporting them as Databricks, rather than Jupyter. When Jupyter files contain different sources than Python, SMA behavior may be unexpected.
* **Checkpoints**

  + **Identify and collect checkpoints** - Activates the feature.
  + **Collect checkpoints as active** - Specifies to execute the collected checkpoint in VS Code when running the workload.
  + **Collect user-defined functions returning data frame type** - Specifies to validate that dataframes should be collected if the user has their own functions that return DataFrames.
  + **Mode** - Specifies the mode type to validate (Schema or DataFrame).
  + **Sample** - Specifies the sampling percentage of each DataFrame to validate.
  + **Relevant PySpark functions to collect** - Specifies the PySpark packages to collect (by default, all of them are checked). You can also add more packages by adding the package’s full name.

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

1. [Conversion Setup Page](#conversion-setup-page)
2. [Entering and Requesting an Access Code](#entering-and-requesting-an-access-code)
3. [Setup Complete](#setup-complete)
4. [Conversion Settings](#conversion-settings)