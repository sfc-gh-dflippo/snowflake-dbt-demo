---
auto_generated: true
description: When preparing source code for analysis with the Snowpark Migration Accelerator
  (SMA), please note that the tool can only process code located in the input directory.
  Before running SMA, ensure all re
last_scraped: '2026-01-14T16:51:56.761290+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/sma-docs/user-guide/before-using-the-sma/pre-processing-considerations
title: 'Snowpark Migration Accelerator:  Pre-Processing Considerations | Snowflake
  Documentation'
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[Snowpark Migration Accelerator](../../README.md)User guide[Before using the SMA](README.md)Pre-processing considerations

# Snowpark Migration Accelerator: Pre-Processing Considerations[¶](#snowpark-migration-accelerator-pre-processing-considerations "Link to this heading")

When preparing source code for analysis with the Snowpark Migration Accelerator (SMA), please note that the tool can only process code located in the input directory. Before running SMA, ensure all relevant source files are placed in this directory.

## Size[¶](#size "Link to this heading")

The SMA tool analyzes source code and text files, not data files. When scanning large codebases or numerous files, the tool may experience memory limitations on your local machine. For example, if you include exported code from all dependent libraries as input files, the analysis will take significantly longer. Keep in mind that SMA will only identify Spark-specific code references, regardless of how much code you include in the scan.

We recommend collecting all code files that:

* Are executed regularly as part of an automated process
* Were used to create the process (if separate from regular execution)
* Are custom libraries developed by your organization that are referenced by either the process or its creation scripts

You do not need to include code that creates established third-party libraries (such as Pandas, Scikit-Learn, or others). The tool automatically catalogs these references without requiring their defining code.

## It should work[¶](#it-should-work "Link to this heading")

The Snowpark Migration Accelerator (SMA) requires complete and valid source code to function properly. It cannot process incomplete code fragments or snippets that don’t execute independently in Scala or Python. If you encounter numerous parsing errors while running SMA, it likely means the source code is incomplete or contains syntax errors. To ensure successful analysis, make sure your input directory contains only working, syntactically correct code from your source platform.

## Use Case[¶](#use-case "Link to this heading")

Understanding the SMA output goes beyond the tool itself. While SMA analyzes your codebase, it’s important to understand your specific use case to identify potential migration challenges. For example, if you have a notebook that uses SQL and a database connector without any Spark references, SMA will only report the third-party libraries used in that notebook. This information is useful, but the tool won’t provide a readiness score for such files. Having context about your application helps you interpret these findings more effectively.

## Code from Databricks Notebooks[¶](#code-from-databricks-notebooks "Link to this heading")

Databricks notebooks allow you to write code in multiple programming languages (SQL, Scala, and PySpark) within the same notebook. When you export a notebook, the file extension will match the primary language category (.ipynb or .py for Python notebooks, .sql for SQL notebooks). Any code written in a different language than the notebook’s primary language will be automatically commented out during export. For example, if you write SQL code in a Python notebook, that SQL code will be commented out when you export the notebook.

![DBX Notebook Example](../../../../_images/commentedCodeWhenExported.png)

Comments containing code are not analyzed by the SMA tool. If you want the code within comments to be analyzed, you must first preprocess it to expose the code in a file format that the tool can recognize.

When working with notebooks, SMA can analyze and recognize code written in languages different from the notebook’s file extension. For example, if you have SQL code in a Jupyter notebook (.ipynb file), SMA will detect and process it even if the code is not commented.

For non-notebook files, make sure your code is saved with the correct file extension that matches the source language (for example, save Python code with a .py extension). This ensures the code can be properly analyzed.

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

1. [Size](#size)
2. [It should work](#it-should-work)
3. [Use Case](#use-case)
4. [Code from Databricks Notebooks](#code-from-databricks-notebooks)