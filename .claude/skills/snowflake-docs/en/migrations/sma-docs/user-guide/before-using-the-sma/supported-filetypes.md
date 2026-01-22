---
auto_generated: true
description: The Snowpark Migration Accelerator (SMA) scans files in your selected
  source directory during project creation. While some files are excluded based on
  their type, SMA generates a summary report showin
last_scraped: '2026-01-14T16:51:57.112017+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/sma-docs/user-guide/before-using-the-sma/supported-filetypes
title: 'Snowpark Migration Accelerator:  Supported Filetypes | Snowflake Documentation'
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
          + [Before using the SMA](README.md)

            - [Supported platforms](supported-platforms.md)
            - [Supported filetypes](supported-filetypes.md)
            - [Code extraction](code-extraction.md)
            - [Pre-processing considerations](pre-processing-considerations.md)
          + [Project overview](../project-overview/README.md)
          + [Technical discovery](../project-overview/optional-technical-discovery.md)
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[Snowpark Migration Accelerator](../../README.md)User guide[Before using the SMA](README.md)Supported filetypes

# Snowpark Migration Accelerator: Supported Filetypes[¶](#snowpark-migration-accelerator-supported-filetypes "Link to this heading")

The Snowpark Migration Accelerator (SMA) scans files in your selected source directory during project creation. While some files are [excluded](#excluded-files-and-folders) based on their type, SMA generates a summary report showing the count of files by extension.

The SMA tool searches for specific file extensions when analyzing references to the Spark API, SQL Statements, and other elements that contribute to the [Readiness Scores](../assessment/readiness-scores). The tool can analyze both code files and notebooks located in any directory or subdirectory of your project.

## Code Files[¶](#code-files "Link to this heading")

The Snowpark Migration Accelerator scans the following file types to identify references to Spark API and other third-party APIs:

* Files with the extension .scala
* Files with the extension .py
* Files with the extension .python

SQL statements written in Spark SQL or HiveQL can be detected in the following file types:

* SQL files with the extension .sql
* Hive Query Language files with the extension .hql

## Notebooks[¶](#notebooks "Link to this heading")

Both the Spark Scala and PySpark parsers in the Snowpark Migration Accelerator (SMA) automatically scan and process Jupyter Notebook files and exported Databricks files when they are present in the source code directory.

* Jupyter Notebook files (\*.ipynb)
* Databricks Notebook files (\*.dbc)

The SMA will analyze notebook files to identify:

* References to the Spark API
* References to other third-party APIs
* SQL statements

The analysis is performed based on the cell type within each notebook. Notebooks can contain a mix of SQL, Python, and Scala cells. The SMA will create an [inventory of all cell types](../assessment/output-reports/sma-inventories.html#notebook-cells-inventory) in its output report.

### Excluded Files and folders[¶](#excluded-files-and-folders "Link to this heading")

By default, certain files and folders are excluded from scanning. These exclusions primarily consist of project configuration files and their associated directories.

#### Folders type excluded from the scanning:[¶](#folders-type-excluded-from-the-scanning "Link to this heading")

* Python package installer (pip) - A tool for installing Python packages
* Distribution packages (dist) - A directory containing Python packages ready for distribution
* Virtual environment (venv) - An isolated Python environment for managing project dependencies
* Site-packages - A directory where Python packages are installed for use across the system

#### Files type excluded from the scanning:[¶](#files-type-excluded-from-the-scanning "Link to this heading")

* input.wsp - Workspace input file
* .DS\_Store - macOS system file that stores custom folder attributes
* build.gradle - Gradle build configuration file
* build.sbt - Scala Build Tool configuration file
* pom.xml - Maven Project Object Model configuration file
* storage.lck - Storage lock file

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

1. [Code Files](#code-files)
2. [Notebooks](#notebooks)