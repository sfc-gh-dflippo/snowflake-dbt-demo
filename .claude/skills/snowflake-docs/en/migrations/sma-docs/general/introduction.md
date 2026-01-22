---
auto_generated: true
description: The Snowpark Migration Accelerator (SMA), formerly SnowConvert for Spark,
  helps developers convert code from various platforms to Snowflake. It uses a proven
  migration framework with 30 years of devel
last_scraped: '2026-01-14T16:51:06.925108+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/sma-docs/general/introduction
title: 'Snowpark Migration Accelerator: Introduction | Snowflake Documentation'
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

          + [Introduction](introduction.md)
          + [Getting started](getting-started/README.md)
          + [Conversion software terms of use](conversion-software-terms-of-use/README.md)
          + [Release notes](release-notes/README.md)
          + [Roadmap](roadmap.md)
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

          + [General troubleshooting](../support/general-troubleshooting/README.md)
          + [Frequently asked questions](../support/frequently-asked-questions-faq/README.md)
          + [Glossary](../support/glossary.md)
          + [Contact us](../support/contact-us.md)
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

[Guides](../../../guides/README.md)[Migrations](../../README.md)Tools[Snowpark Migration Accelerator](../README.md)GeneralIntroduction

# Snowpark Migration Accelerator: Introduction[¶](#snowpark-migration-accelerator-introduction "Link to this heading")

## Overview of the Snowpark Migration Accelerator [¶](#overview-of-the-snowpark-migration-accelerator "Link to this heading")

The Snowpark Migration Accelerator (SMA), formerly *SnowConvert for Spark*, helps developers convert code from various platforms to Snowflake. It uses a proven migration framework with 30 years of development to analyze code that contains Spark API calls. The tool creates an Abstract Syntax Tree (AST) and Symbol Table to build a detailed model of how the code works. This model helps convert the original code into equivalent Snowflake code automatically, maintaining the same functionality as the source code.

![SMA High Level Diagram](../../../_images/image%28503%29.png)

The Snowpark Migration Accelerator (SMA) analyzes your source code by creating a detailed model that captures its meaning and purpose. This allows SMA to understand how your code works at a deeper level than basic tools that only search and replace text or match patterns.

The SMA scans your source code and notebook files to find all Spark API calls. It then converts these Spark API calls to their matching Snowpark API functions when possible.

## Assessment and Conversion [¶](#assessment-and-conversion "Link to this heading")

The Snowpark Migration Accelerator (SMA) has two operating modes:

1. *Assessment* (or *Qualification*) - A free analysis tool that evaluates your code before conversion
2. *Conversion* - Transforms your code to Snowpark

We strongly recommend running the Assessment mode first before starting any code conversion.

### Assessment Mode[¶](#assessment-mode "Link to this heading")

Assessment mode helps users find and analyze Spark API usage in their code. SMA scans the source code and builds a *semantic model* using our specialized framework. This model helps SMA understand how the code works and what it does. As a result, SMA can generate detailed and accurate reports about the code’s components.

The SMA analyzes your code to help plan the migration process. It identifies Spark API dependencies and evaluates how ready your code is for migration. Once the assessment is complete, you can move forward with converting your code.

For more information about how SMA assesses your code, please see the [Assessment section of the SMA User Guide](../user-guide/assessment/README).

### Conversion Mode[¶](#conversion-mode "Link to this heading")

During the conversion phase, SMA uses the semantic model created in the assessment phase to automatically generate Snowflake-compatible code. The tool replaces Spark API calls with equivalent Snowpark API calls whenever possible. When direct conversion isn’t possible, SMA adds detailed comments to the output code explaining why certain elements couldn’t be converted and provides helpful context for manual conversion.

To use Conversion mode, you need an access code. You can find detailed information about access codes in the [Access Codes and Licensing section](getting-started/download-and-access.html#access-codes-and-licensing). To get an access code, fill out the [Request an Access Code](../support/frequently-asked-questions-faq/how-to-request-an-access-code) form in the SMA tool. If you have any questions, please email [sma-info@snowflake.com](mailto:sma-info%40snowflake.com).

## Outline[¶](#outline "Link to this heading")

This section provides comprehensive guidance on the Snowpark Migration Accelerator (SMA), covering the following key areas:

* **Getting Started:**

  + Learn how to [Download and Access](getting-started/download-and-access) SMA.
  + Step-by-step [Installation](getting-started/installation/README) guide.
* **End User License Agreement (EULA):** Review the [Conversion Software Terms of Use](conversion-software-terms-of-use/README).
* **Release Notes:** View the latest [Release Notes](release-notes/README) to see recent updates and changes.

For assistance or questions, please [Contact Us](../support/contact-us).

We invite you to start exploring the features and functionalities of the Snowpark Migration Accelerator (SMA).

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

1. [Overview of the Snowpark Migration Accelerator](#overview-of-the-snowpark-migration-accelerator)
2. [Assessment and Conversion](#assessment-and-conversion)
3. [Outline](#outline)