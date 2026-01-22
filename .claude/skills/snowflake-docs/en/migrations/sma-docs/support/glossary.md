---
auto_generated: true
description: The Snowpark Migration Accelerator (SMA) uses some technical terms that
  might be unfamiliar. Please refer to our glossary page to learn more about these
  terms.
last_scraped: '2026-01-14T16:51:30.276137+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/sma-docs/support/glossary
title: 'Snowpark Migration Accelerator:  Glossary | Snowflake Documentation'
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

      * [SnowConvert AI](../../snowconvert-docs/overview.md)
      * [Snowpark Migration Accelerator](../README.md)

        + General

          + [Introduction](../general/introduction.md)
          + [Getting started](../general/getting-started/README.md)
          + [Conversion software terms of use](../general/conversion-software-terms-of-use/README.md)
          + [Release notes](../general/release-notes/README.md)
          + [Roadmap](../general/roadmap.md)
        + User guide

          + [Overview](../user-guide/overview.md)
          + [Before using the SMA](../user-guide/before-using-the-sma/README.md)
          + [Project overview](../user-guide/project-overview/README.md)
          + [Technical discovery](../user-guide/project-overview/optional-technical-discovery.md)
          + [AI assistant](../user-guide/chatbot.md)
          + [Assessment](../user-guide/assessment/README.md)
          + [Conversion](../user-guide/conversion/README.md)
          + [Using the SMA CLI](../user-guide/using-the-sma-cli/README.md)
        + Use cases

          + Snowflake VS Code extension

            + [SMA checkpoints walkthrough](../use-cases/sma-checkpoints-walkthrough/README.md)
            + [SMA EWI Assistant walkthrough](../use-cases/sma-ewi-assistant-walkthrough/README.md)
          + [Assessment walkthrough](../use-cases/assessment-walkthrough/README.md)
          + [Conversion walkthrough](../use-cases/conversion-walkthrough.md)
          + [Migration lab](../use-cases/migration-lab/README.md)
          + [Sample project](../use-cases/sample-project.md)
          + [Using SMA in an Ubuntu Docker image](../use-cases/using-snowconvert-in-a-ubuntu-docker-image.md)
          + [SMA CLI walkthrough](../use-cases/sma-cli-walkthrough.md)
          + [Snowpark Connect](../use-cases/snowpark-connect/README.md)
        + Issue analysis

          + [Approach](../issue-analysis/approach.md)
          + [Issue code categorization](../issue-analysis/issue-code-categorization.md)
          + [Issue codes by source](../issue-analysis/issue-codes-by-source/README.md)
          + [Troubleshooting the output code](../issue-analysis/troubleshooting-the-output-code/README.md)
          + [Workarounds](../issue-analysis/workarounds.md)
          + [Deploying the output code](../issue-analysis/deploying-the-output-code.md)
        + Translation reference

          + [Translation reference overview](../translation-reference/translation-reference-overview.md)
          + [SIT tagging](../translation-reference/sit-tagging/README.md)
          + [SQL embedded code](../translation-reference/sql-embedded-code.md)
          + [HiveSQL](../translation-reference/hivesql/README.md)
          + [Spark SQL](../translation-reference/spark-sql/README.md)
        + Workspace estimator

          + [Overview](../workspace-estimator/overview.md)
          + [Getting started](../workspace-estimator/getting-started.md)
        + Interactive assessment application

          + [Overview](../interactive-assessment-application/overview.md)
          + [Installation guide](../interactive-assessment-application/installation-guide.md)
        + Support

          + [General troubleshooting](general-troubleshooting/README.md)
          + [Frequently asked questions](frequently-asked-questions-faq/README.md)
          + [Glossary](glossary.md)
          + [Contact us](contact-us.md)
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

[Guides](../../../guides/README.md)[Migrations](../../README.md)Tools[Snowpark Migration Accelerator](../README.md)SupportGlossary

# Snowpark Migration Accelerator: Glossary[¶](#snowpark-migration-accelerator-glossary "Link to this heading")

The Snowpark Migration Accelerator (SMA) uses some technical terms that might be unfamiliar. Please refer to our glossary page to learn more about these terms.

## Snowpark Migration Accelerator (SMA)[¶](#snowpark-migration-accelerator-sma "Link to this heading")

This software documentation explains how to automatically convert Spark API code written in Scala or Python to equivalent Snowflake Snowpark code. The conversion process is secure and maintains the functionality of your original code.

The Snowpark Migration Accelerator (SMA) was previously known as SnowConvert and SnowConvert for Spark. Please note that SnowConvert (SC) continues to be available as a tool for SQL conversions.

## Readiness Score[¶](#readiness-score "Link to this heading")

The Readiness Score helps you understand how ready your code is for migration to Snowpark. It calculates the percentage of Spark API references that can be converted to Snowpark API. For example, if 3413 out of 3748 Spark API references can be converted, the readiness score would be 91%.

However, it’s important to note that this score:

* Only considers Spark API references
* Does not evaluate third-party libraries
* Should be used as an initial assessment, not the final decision factor

While a higher score indicates better compatibility with Snowpark, you should also evaluate other factors, such as third-party library dependencies, before proceeding with the migration.

## Spark Reference Categories[¶](#spark-reference-categories "Link to this heading")

The Snowpark Migration Accelerator (SMA) classifies Spark components according to how they map to Snowpark functionality. For each Spark reference, SMA provides:

* A categorization of how it translates to Snowpark
* A detailed description
* Example code
* Information about automatic conversion capability
* Details about Snowpark support

You can find the complete reference guide [on this page](../user-guide/assessment/spark-reference-categories).

## SnowConvert Qualification Tool[¶](#snowconvert-qualification-tool "Link to this heading")

SnowConvert for Spark’s assessment mode analyzes your codebase to automatically detect and identify all instances of Apache Spark Python code.

## File Inventory[¶](#file-inventory "Link to this heading")

A complete list of all files found in the tool’s input directory, regardless of file type. The inventory provides a detailed breakdown organized by file type, including:

* The original technology or platform
* Number of lines of code
* Number of comment lines
* File sizes of the source files

## Keyword Counts[¶](#keyword-counts "Link to this heading")

A summary of keyword occurrences organized by technology type. For example, when analyzing a .py file containing PySpark code, the system tracks and counts each PySpark keyword. The report shows the total number of keywords found for each file extension.

## Spark Reference Inventory[¶](#spark-reference-inventory "Link to this heading")

After analyzing your code, you will receive a comprehensive list of all Spark API references found in your Python code.

## Readiness Score[¶](#id1 "Link to this heading")

The Spark code references will help determine how much of your codebase can be automatically converted.

## Conversion Score[¶](#conversion-score "Link to this heading")

The conversion score is calculated by dividing the number of automatically converted Spark operations by the total number of Spark references detected in the code.

## Conversion/Transformation Rule[¶](#conversion-transformation-rule "Link to this heading")

Rules that define how SnowConvert transforms source code into the desired target code format.

## Parse[¶](#parse "Link to this heading")

The parsing phase is the first step where SnowConvert analyzes the source code and creates an internal data structure. This structure is then used to apply conversion rules during the migration process.

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

1. [Snowpark Migration Accelerator (SMA)](#snowpark-migration-accelerator-sma)
2. [Readiness Score](#readiness-score)
3. [Spark Reference Categories](#spark-reference-categories)
4. [SnowConvert Qualification Tool](#snowconvert-qualification-tool)
5. [File Inventory](#file-inventory)
6. [Keyword Counts](#keyword-counts)
7. [Spark Reference Inventory](#spark-reference-inventory)
8. [Readiness Score](#id1)
9. [Conversion Score](#conversion-score)
10. [Conversion/Transformation Rule](#conversion-transformation-rule)
11. [Parse](#parse)