---
auto_generated: true
description: 'The Snowpark Migration Accelerator (SMA) offers two installation options:'
last_scraped: '2026-01-14T16:51:17.391248+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/sma-docs/general/getting-started/installation/linux-installation
title: 'Snowpark Migration Accelerator:  Linux Installation | Snowflake Documentation'
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

[Guides](../../../../../guides/README.md)[Migrations](../../../../README.md)Tools[Snowpark Migration Accelerator](../../../README.md)General[Getting started](../README.md)[Installation](README.md)Linux installation

# Snowpark Migration Accelerator: Linux Installation[¶](#snowpark-migration-accelerator-linux-installation "Link to this heading")

The Snowpark Migration Accelerator (SMA) offers two installation options:

* Desktop application (available for Windows and macOS users)
* Command Line Interface (CLI, available for Windows, macOS, and Linux users)

Note: Linux users can only use the CLI version.

If you need the CLI files, please check the [Downloading and Accessing page](../download-and-access) for detailed instructions on how to get them.

## Installing the SMA CLI on Linux[¶](#installing-the-sma-cli-on-linux "Link to this heading")

Here’s how to install the Snowpark Migration Accelerator (SMA) Command Line Interface (CLI) on your Linux system:

1. **Verify the Download:** Download the SMA CLI installation file that matches your Linux system. You can find the correct download link in the [Downloading and Accessing page](../download-and-access).
2. **Open a Terminal:** Open a terminal window and navigate to the folder containing the `SMA-CLI-linux.tar` file.
3. **Run Installation Commands:** Enter the following commands in your terminal. Note: You may need administrator privileges (sudo) to execute these commands.

```
    sudo mkdir /usr/local/share/.SMA-CLI-linux
    sudo tar -xf SMA-CLI-linux.tar -C /usr/local/share/.SMA-CLI-linux
    sudo ln -s /usr/local/share/.SMA-CLI-linux/orchestrator/sma /usr/local/bin/sma
```

Copy

After installation is complete, you can begin using the SMA Command Line Interface (CLI). For detailed instructions, please refer to the [SMA User Guide](../../../user-guide/overview).

**Important Note:**

When using SMA on Windows or Mac, you will see an “UPDATE NOW” notification in the top right corner if a newer version is available. Simply click the notification to download and install the latest version.

**Troubleshooting Guide:**

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

1. [Installing the SMA CLI on Linux](#installing-the-sma-cli-on-linux)