---
auto_generated: true
description: The Snowpark Migration Accelerator (SMA) analyzes Python, Scala, and
  SQL code in your project to identify what can be converted from Spark API to Snowpark
  API. This analysis provides detailed insights
last_scraped: '2026-01-14T16:51:34.062251+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/sma-docs/use-cases/assessment-walkthrough/README
title: 'Snowpark Migration Accelerator: Assessment Walkthrough | Snowflake Documentation'
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

          + [Overview](../../user-guide/overview.md)
          + [Before using the SMA](../../user-guide/before-using-the-sma/README.md)
          + [Project overview](../../user-guide/project-overview/README.md)
          + [Technical discovery](../../user-guide/project-overview/optional-technical-discovery.md)
          + [AI assistant](../../user-guide/chatbot.md)
          + [Assessment](../../user-guide/assessment/README.md)
          + [Conversion](../../user-guide/conversion/README.md)
          + [Using the SMA CLI](../../user-guide/using-the-sma-cli/README.md)
        + Use cases

          + Snowflake VS Code extension

            + [SMA checkpoints walkthrough](../sma-checkpoints-walkthrough/README.md)
            + [SMA EWI Assistant walkthrough](../sma-ewi-assistant-walkthrough/README.md)
          + [Assessment walkthrough](README.md)

            - [Walkthrough setup](walkthrough-setup/README.md)
            - [Running the tool](running-the-tool.md)
            - [Interpreting the assessment output](interpreting-the-assessment-output/README.md)
            - [Running the SMA again](running-the-sma-again.md)
          + [Conversion walkthrough](../conversion-walkthrough.md)
          + [Migration lab](../migration-lab/README.md)
          + [Sample project](../sample-project.md)
          + [Using SMA in an Ubuntu Docker image](../using-snowconvert-in-a-ubuntu-docker-image.md)
          + [SMA CLI walkthrough](../sma-cli-walkthrough.md)
          + [Snowpark Connect](../snowpark-connect/README.md)
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[Snowpark Migration Accelerator](../../README.md)Use casesAssessment walkthrough

# Snowpark Migration Accelerator: Assessment Walkthrough[¶](#snowpark-migration-accelerator-assessment-walkthrough "Link to this heading")

The Snowpark Migration Accelerator (SMA) analyzes Python, Scala, and SQL code in your project to identify what can be converted from Spark API to Snowpark API. This analysis provides detailed insights about your source code and highlights which components are ready to be migrated to Snowflake.

This guide will help you maximize the value of your assessment. You will learn:

* How to access and run the assessment tool
* How to review your source code to ensure optimal conversion results
* How to understand and analyze the assessment report
* What actions to take after completing the assessment

This walkthrough specifically covers Python code written for Spark. While the Snowpark Migration Accelerator (SMA) supports multiple programming languages and platforms (see [supported languages and platforms](../../user-guide/before-using-the-sma/supported-platforms)), we will focus exclusively on Python. To explore how SMA works with other platforms, you can refer to [the sample project](../sample-project) included in the application.

Before you begin, please review the prerequisites on [the next page](walkthrough-setup/README). Although we strongly recommend performing an assessment first, you can proceed directly to the conversion process by following our [conversion walkthrough](../conversion-walkthrough).

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