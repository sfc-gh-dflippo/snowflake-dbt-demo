---
auto_generated: true
description: Before running Snowpark Migration Accelerator (SMA), make sure all your
  source code files are located on the computer where you installed SMA. You don’t
  need to connect to any source database or Spark
last_scraped: '2026-01-14T16:52:00.103747+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/sma-docs/use-cases/assessment-walkthrough/walkthrough-setup/notes-on-code-preparation
title: 'Snowpark Migration Accelerator: Notes on Code Preparation | Snowflake Documentation'
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

[Guides](../../../../../guides/README.md)[Migrations](../../../../README.md)Tools[Snowpark Migration Accelerator](../../../README.md)Use cases[Assessment walkthrough](../README.md)[Walkthrough setup](README.md)Notes on code preparation

# Snowpark Migration Accelerator: Notes on Code Preparation[¶](#snowpark-migration-accelerator-notes-on-code-preparation "Link to this heading")

Before running Snowpark Migration Accelerator (SMA), make sure all your source code files are located on the computer where you installed SMA. You don’t need to connect to any source database or Spark environment since SMA only performs code analysis.

The source code must be in a readable format for SMA to process it correctly, as the tool relies completely on the source code you provide.

## Extraction[¶](#extraction "Link to this heading")

Before running the Snowpark Migration Accelerator (SMA), organize all your source code files into a single main folder. You can maintain your existing subfolder structure within this main folder, but all code files must be located under this one directory. This requirement applies to:

The following file types are supported:

* GitHub repositories (downloaded as ZIP files and extracted to your local machine)
* Python script files
* Scala project files
* Databricks notebook files
* Jupyter notebooks run on your local computer

Before starting your migration, gather all source code files into a single main folder. While your source code may come from different locations, having it organized in one place will make the migration process more efficient. If you already have an established file organization structure, keep it intact within the main folder.

[Export GitHub repositories to ZIP files](https://docs.github.com/en/repositories/working-with-files/using-files/downloading-source-code-archives)

To generate accurate and complete reports using the Snowpark Migration Accelerator (SMA), scan only the code that is relevant to your migration project. Rather than scanning all available code, identify and include only the essential code files that you plan to migrate. For more information, refer to [**Size**](#size) in the [**Considerations**](#considerations) section.

## Considerations[¶](#considerations "Link to this heading")

Let’s review which file types are compatible with Snowpark Migration Accelerator (SMA) and understand the key considerations when preparing your source code for analysis with SMA.

### Filetypes[¶](#filetypes "Link to this heading")

The Snowpark Migration Accelerator (SMA) examines all files in your source directory, but only processes files with specific extensions that may contain Spark API code. This includes both regular code files and Jupyter notebooks.

You can find a list of file types that SMA supports in the [Supported Filetypes section of this documentation](../../../user-guide/before-using-the-sma/supported-filetypes).

### Exported Files[¶](#exported-files "Link to this heading")

If your code is stored in a source control platform instead of local files, you need to export it into a format that SMA can process. Here’s how you can export your code:

For Databricks users: To use the Snowpark Migration Accelerator (SMA), you need to export your notebooks to .dbc format. You can find detailed instructions on how to export notebooks in [the Databricks documentation on exporting notebooks](https://docs.databricks.com/en/notebooks/notebook-export-import.html#export-notebooks.).

Need help exporting files? Visit [the export scripts in the Snowflake Labs Github repo](https://github.com/Snowflake-Labs/SC.DDLExportScripts/tree/main), where Snowflake Professional Services maintains scripts for Databricks, Hive, and other platforms.

* If you are using a different platform, please refer to the [Code Extraction page](../../../user-guide/before-using-the-sma/code-extraction) for specific instructions for your platform. If you need assistance converting your code into a format that works with SMA, please contact [sma-support@snowflake.com](mailto:sma-support%40snowflake.com).

### Size[¶](#size "Link to this heading")

The Snowpark Migration Accelerator (SMA) is designed to analyze source code, not data. To ensure optimal performance and prevent system resource exhaustion, we recommend:

1. Only include the specific code files you want to migrate
2. Avoid including unnecessary library dependencies

While you can include dependent library code files, doing so will significantly increase processing time without adding value, since SMA specifically focuses on identifying Spark code that requires migration.

We recommend gathering all code files that…

* Run automatically as part of a scheduled process
* Were used to create or configure that process (if they are separate)
* Are custom libraries created by your organization that are used in either of the above scenarios

You don’t need to include code for common third-party libraries such as Pandas or Sci-Kit Learn. The tool will automatically detect and catalog these library references without requiring their source code.

### Does it run?[¶](#does-it-run "Link to this heading")

The Snowpark Migration Accelerator (SMA) can only process complete and syntactically correct source code. Your code must be able to run successfully in [a supported source platform](../../../user-guide/before-using-the-sma/supported-platforms). If the SMA reports multiple [parsing errors](../../../issue-analysis/issue-code-categorization.html#parsing-error), this usually indicates that your source code contains syntax errors. To achieve the best results, ensure that your input directory contains only valid code that can be executed on the source platform.

### Use Case[¶](#use-case "Link to this heading")

Understanding your codebase’s purpose is essential when reviewing scan results. It will help you:

1. Determine which applications or processes may not work well with Snowpark
2. Understand and analyze readiness assessment results more effectively
3. Check if your existing code and systems are compatible with Snowflake

When scanning a notebook that uses an unsupported SQL dialect and a database connector without Spark, the SMA will only display imported third-party libraries. While this information is helpful, the notebook will not receive a Spark API Readiness Score. Understanding how you plan to use your code will help you better understand these limitations and make better decisions during migration.

### Exports from Databricks Notebooks[¶](#exports-from-databricks-notebooks "Link to this heading")

Databricks notebooks support multiple programming languages such as SQL, Scala, and PySpark in a single notebook. When you export a notebook, the file extension will reflect its primary language:

* Python notebooks: .ipynb or .py
* SQL notebooks: .sql

Any code written in a language different from the notebook’s primary language will be automatically converted to comments during export. For instance, if you include SQL code in a Python notebook, the SQL code will appear as comments in the exported file.

![Commented Code when Exported](../../../../../_images/commentedCodeWhenExported.png)

Code comments are excluded from SMA analysis. To ensure your code is properly analyzed, place it in a file with the correct file extension matching the source language. For example:

* Python code should be in .py files
* SQL code should be in .sql files

Note that even uncommented code will not be analyzed if it’s in a file with the wrong extension (such as Python code in a .sql file).

Before using the tool, please read the [Pre-Processing Considerations](../../../user-guide/before-using-the-sma/pre-processing-considerations) section in our documentation. This section contains essential information that you need to know before proceeding.

## Walkthrough Codebase[¶](#walkthrough-codebase "Link to this heading")

Select one of the extracted sample codebase directories as the input for the Snowpark Migration Accelerator (SMA).

When migrating code, maintain your original folder structure. This preserves file organization and helps developers understand the code architecture. Both the code conversion process and assessment analysis are performed one file at a time.

For this tutorial, we will work with small, functional Spark code samples (each less than 1MB). These samples showcase different scenarios and functions that can be converted. Although these examples are simplified versions and not production code, they effectively demonstrate various conversion possibilities.

The source directory can contain Jupyter notebooks (.ipynb), Python scripts (.py), and text files. While SMA examines all files in your codebase, it only searches for Spark API references in Python (.py) files and Jupyter notebook (.ipynb) files.

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

1. [Extraction](#extraction)
2. [Considerations](#considerations)
3. [Walkthrough Codebase](#walkthrough-codebase)