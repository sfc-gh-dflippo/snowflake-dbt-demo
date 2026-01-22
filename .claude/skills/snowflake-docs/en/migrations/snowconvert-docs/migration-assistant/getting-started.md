---
auto_generated: true
description: This guide will walk you through the SnowConvert AI Migration Assistant’s
  basic steps to resolve post-conversion issues in your SQL code.
last_scraped: '2026-01-14T16:53:00.936320+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/migration-assistant/getting-started
title: SnowConvert AI - Migration Assistant - Getting Started | Snowflake Documentation
---

1. [Overview](../../../guides/README.md)
2. [Snowflake Horizon Catalog](../../../user-guide/snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../../../guides/overview-connecting.md)
6. [Virtual warehouses](../../../user-guide/warehouses.md)
7. [Databases, Tables, & Views](../../../guides/overview-db.md)
8. [Data types](../../../data-types.md)
10. Data Integration

    - [Snowflake Openflow](../../../user-guide/data-integration/openflow/about.md)
    - Apache Iceberg™

      - [Apache Iceberg™ Tables](../../../user-guide/tables-iceberg.md)
      - [Snowflake Open Catalog](../../../user-guide/opencatalog/overview.md)
11. Data engineering

    - [Data loading](../../../guides/overview-loading-data.md)
    - [Dynamic Tables](../../../user-guide/dynamic-tables-about.md)
    - [Streams and Tasks](../../../user-guide/data-pipelines-intro.md)
    - [dbt Projects on Snowflake](../../../user-guide/data-engineering/dbt-projects-on-snowflake.md)
    - [Data Unloading](../../../guides/overview-unloading-data.md)
12. [Storage Lifecycle Policies](../../../user-guide/storage-management/storage-lifecycle-policies.md)
13. [Migrations](../../README.md)

    * Tools

      * [SnowConvert AI](../overview.md)

        + General

          + [About](../general/about.md)
          + [Getting Started](../general/getting-started/README.md)
          + [Terms And Conditions](../general/terms-and-conditions/README.md)
          + [Release Notes](../general/release-notes/release-notes/README.md)
          + User Guide

            + [SnowConvert AI](../general/user-guide/snowconvert/README.md)
            + [Project Creation](../general/user-guide/project-creation.md)
            + [Extraction](../general/user-guide/extraction.md)
            + [Deployment](../general/user-guide/deployment.md)
            + [Data Migration](../general/user-guide/data-migration.md)
            + [Data Validation](../general/user-guide/data-validation.md)
            + [Power BI Repointing](../general/user-guide/power-bi-repointing-general.md)
            + [ETL Migration](../general/user-guide/etl-migration-replatform.md)
          + [Technical Documentation](../general/technical-documentation/README.md)
          + [Contact Us](../general/contact-us.md)
          + Others

            + [Using SnowConvert AI In A Ubuntu Docker Image](../general/others/using-snowconvert-in-a-ubuntu-docker-image.md)
          + [Frequently Asked Questions (FAQ)](../general/frequently-asked-questions-faq.md)")
        + Translation References

          + [General](../translation-references/general/README.md)
          + [Teradata](../translation-references/teradata/README.md)
          + [Oracle](../translation-references/oracle/README.md)
          + [SQL Server-Azure Synapse](../translation-references/transact/README.md)
          + [Sybase IQ](../translation-references/sybase/README.md)
          + [Hive-Spark-Databricks SQL](../translation-references/hive/README.md)
          + [Redshift](../translation-references/redshift/README.md)
          + [PostgreSQL-Greenplum-Netezza](../translation-references/postgres/README.md)
          + [BigQuery](../translation-references/bigquery/README.md)
          + [Vertica](../translation-references/vertica/README.md)
          + [IBM DB2](../translation-references/db2/README.md)
          + [SSIS](../translation-references/ssis/README.md)
        + [Migration Assistant](README.md)

          - [Getting Started](getting-started.md)

            * [Model Preference](model-preference.md)
          - [Troubleshooting](troubleshooting.md)
          - [Billing](billing.md)
          - [Legal Notices](legal-notices.md)
        + [Data Validation CLI](../data-validation-cli/index.md)
        + [AI Verification](../snowconvert-ai-verification.md)
      * [Snowpark Migration Accelerator](../../sma-docs/README.md)
    * Guides

      * [Teradata](../../guides/teradata.md)
      * [Databricks](../../guides/databricks.md)
      * [SQL Server](../../guides/sqlserver.md)
      * [Amazon Redshift](../../guides/redshift.md)
      * [Oracle](../../guides/oracle.md)
      * [Azure Synapse](../../guides/azuresynapse.md)
15. [Queries](../../../guides/overview-queries.md)
16. [Listings](../../../collaboration/collaboration-listings-about.md)
17. [Collaboration](../../../guides/overview-sharing.md)
19. [Snowflake AI & ML](../../../guides/overview-ai-features.md)
21. [Snowflake Postgres](../../../user-guide/snowflake-postgres/about.md)
23. [Alerts & Notifications](../../../guides/overview-alerts.md)
25. [Security](../../../guides/overview-secure.md)
26. [Data Governance](../../../guides/overview-govern.md)
27. [Privacy](../../../guides/overview-privacy.md)
29. [Organizations & Accounts](../../../guides/overview-manage.md)
30. [Business continuity & data recovery](../../../user-guide/replication-intro.md)
32. [Performance optimization](../../../guides/overview-performance.md)
33. [Cost & Billing](../../../guides/overview-cost.md)

[Guides](../../../guides/README.md)[Migrations](../../README.md)Tools[SnowConvert AI](../overview.md)[Migration Assistant](README.md)Getting Started

# SnowConvert AI - Migration Assistant - Getting Started[¶](#snowconvert-ai-migration-assistant-getting-started "Link to this heading")

This guide will walk you through the SnowConvert AI Migration Assistant’s basic steps to resolve post-conversion issues in your SQL code.

## Prerequisites[¶](#prerequisites "Link to this heading")

* You have installed the Snowflake Visual Studio Code extension version **GA** **1.14.0** or later.

Warning

Please be aware that the documentation has been updated to reflect changes in version 1.17.0. The streaming feature, along with some instructions changes, e.g, [Billing](billing), are only available in version 1.17.0 or newer.

* You have **.sql** files that contain EWIs from SnowConvert.
* You have a Snowflake account with access to any of the supported models. For more information, please check the [Model Preference documentation](model-preference).

## Steps[¶](#steps "Link to this heading")



### 1. Install the Snowflake Visual Studio Code extension[¶](#install-the-snowflake-visual-studio-code-extension "Link to this heading")

See Snowflake documentation on how to install from the [Visual Studio Marketplace](https://docs.snowflake.com/en/user-guide/vscode-ext#install-the-vs-code-extension-from-visual-studio-marketplace) or from a [.vsix file](https://docs.snowflake.com/en/user-guide/vscode-ext#install-the-vs-code-extension-from-a-vsix-file).

Be sure you’re using version **GA** **1.14.0** or later.

### 2. Sign in to Snowflake with the Visual Studio Code extension[¶](#sign-in-to-snowflake-with-the-visual-studio-code-extension "Link to this heading")

See Snowflake documentation on how to [sign in](https://docs.snowflake.com/en/user-guide/vscode-ext#sign-in-to-snowflake-with-the-vs-code-extension) to Snowflake using the VS Code extension.

### 3. Enable SnowConvert AI Migration Assistant in the Snowflake VS Code Extension Settings[¶](#enable-snowconvert-ai-migration-assistant-in-the-snowflake-vs-code-extension-settings "Link to this heading")

Open the VS Code settings panel and navigate to Extensions. Select the Snowflake extension, and open the settings panel for the Snowflake extension.

![Settings panel > Extensions](../../../_images/MigrationAssistantSettingsPanelExtension.png)

Settings panel > Extensions

![Snowflake extension > settings](../../../_images/MigrationAssistantSnowflakeExtensionSettings.png)

Snowflake extension > settings

In the Snowflake extension settings, you must:

* Check “Enable SnowConvert AI Migration Assistant”

![Enable SnowConvert AI Migration Assistant setting](../../../_images/MigrationAssistantEnableMigrationAssistant.png)

Enable SnowConvert AI Migration Assistant setting

### 4. Set up Model Preference[¶](#set-up-model-preference "Link to this heading")

For more information about how to set up the model preference, please check the [Model Preference](model-preference) documentation.

### 5. Open a workspace folder containing SnowConvert AI migration results[¶](#open-a-workspace-folder-containing-snowconvert-ai-migration-results "Link to this heading")

First, ensure you have a workspace folder open in Visual Studio Code. Then, access the Snowflake extension by selecting its icon from the activity bar on the left. A “SnowConvert AI Issues” panel will appear at the bottom within the Snowflake extension’s view. This panel automatically populates with a list of all folders and files in the current workspace that have SnowConvert AI migration issues. If no workspace is selected, the following message is prompted on the SnowConvert AI Issues panel: “No SnowConvert AI Migration issues found.”

![SnowConvert AI Issue panel](../../../_images/MigrationAssistantSnowConvertIssuePanel.png)

SnowConvert AI Issue panel

Once your workspace folder containing SnowConvert AI migration issues is open, you can access the toolbar by hovering over the “SnowConvert AI Issues” panel. This toolbar in the panel’s top-left corner allows you to interact with the list of migration issues identified.

![SnowConvert AI Issues panel toolbar](../../../_images/MigrationAssistantSnowConvertIssuePanelToolbar.png)

SnowConvert AI Issues panel toolbar

* **🏠 (Return to Workspace Root):** Clicking this icon resets the view to display the entire workspace folder’s initial state.
* **📁 (Select Folder):** Allows you to navigate to and select a specific subfolder within your workspace to focus the issue list.
* **🔄 (Refresh Issues):** Use this to update the list of SnowConvert AI migration issues manually. The list will also update automatically whenever an issue is resolved or a new one is detected.
* **➖ (Collapse All):** Collapses all expanded items in the issues list for a more compact view.

### 6. See SnowConvert AI Migration Issues and click the sparkles for help resolving[¶](#see-snowconvert-ai-migration-issues-and-click-the-sparkles-for-help-resolving "Link to this heading")

Once you’ve opened a folder containing .sql files with migration issues, you will see a list of all the EWIs, FDMs, and PRFs in that folder and the files containing them. Clicking on a migration issue from the list will focus the code editor on the line of code where the issue was found.

![SnowConvert AI Migration Issues panel](../../../_images/MigrationAssistantSnowconvertMigrationIssuesPanel.png)

SnowConvert AI Migration Issues panel

Note

**EWIs** are indicated by the ⚠️ icon.

**FDMs and PRFs** are indicated by the ℹ️ icon.

The folder icon changes from 📁 (collapsed) to 📂 (expanded) to reflect its state.

There are two ways to get AI-powered assistance and recommended solutions for a migration issue:

1. Click the sparkles icon located next to the migration issue in the list.

![Get explanation and suggestion by sparkles icon](../../../_images/MigrationAssistantSuggestionSparklesIcon.png)

Get explanation and suggestion by sparkles icon

2. Click on the CodeLenses identified by *SnowConvert AI, which are* located above every migration issue.

![Get explanation and suggestion by CodeLens](../../../_images/MigrationAssistantSuggestionCodeLens.png)

Get explanation and suggestion by CodeLens

### 7. Get help[¶](#get-help "Link to this heading")

Once you click the sparkles icon or the CodeLenses, the SnowConvert AI Migration Assistant will query Snowflake Cortex AI with the migration issue and a snippet of the code context surrounding the migration issue. The call to Cortex happens entirely within your Snowflake account, using the connection details you configured in the Snowflake VS Code Extension.

Once a result has been generated, it will appear in a panel to the right of the code editor. The result will contain an explanation of the migration issue in the context of your code, and a suggested fix to make the code run correctly on Snowflake. If the assistant is unable to generate a response with high confidence, it will abstain from providing a recommended solution.

![Explanation and suggestion panel](../../../_images/MigrationAssistantExplanationSuggestionPanel.png)

Explanation and suggestion panel

### 8. Interacting with the Migration Assistant[¶](#interacting-with-the-migration-assistant "Link to this heading")

* **Refine Solutions:** If an AI suggestion is incorrect or you prefer a different approach, enter your preferred changes or instructions into the chatbox.
* **Ask SQL-Related Questions:** If the suggestion is correct, you can still ask for clarifications or further explanations on any SQL-related topic.
* **Request Code Modifications:** You can also ask for specific code changes, such as adding a header to your script.

![SnowConvert AI Migration Assistant chat interaction](../../../_images/MigrationAssistantChatInteraction.png)

SnowConvert AI Migration Assistant chat interaction

Note

The assistant will refrain from answering non-SQL-related questions.

![Non-SQL related question abstension message](../../../_images/MigrationAssistantNonSqlRelatedQuestion.png)

Non-SQL related question abstension message

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

The SnowConvert AI tool is subject to the [Conversion Software Terms of Use](https://www.snowflake.com/en/legal/technical-services-and-education/conversion-software-terms/).

On this page

1. [Prerequisites](#prerequisites)
2. [Steps](#steps)