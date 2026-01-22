---
auto_generated: true
description: If you have already downloaded and installed the Snowpark Migration Accelerator
  (SMA), this section will show you how to use it effectively.
last_scraped: '2026-01-14T16:51:39.949674+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/sma-docs/user-guide/overview
title: 'Snowpark Migration Accelerator: Overview | Snowflake Documentation'
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

          + [Overview](overview.md)
          + [Before using the SMA](before-using-the-sma/README.md)
          + [Project overview](project-overview/README.md)
          + [Technical discovery](project-overview/optional-technical-discovery.md)
          + [AI assistant](chatbot.md)
          + [Assessment](assessment/README.md)
          + [Conversion](conversion/README.md)
          + [Using the SMA CLI](using-the-sma-cli/README.md)
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

[Guides](../../../guides/README.md)[Migrations](../../README.md)Tools[Snowpark Migration Accelerator](../README.md)User guideOverview

# Snowpark Migration Accelerator: Overview[¶](#snowpark-migration-accelerator-overview "Link to this heading")

If you have already [downloaded](../general/getting-started/download-and-access) and [installed](../general/getting-started/installation/README) the Snowpark Migration Accelerator (SMA), this section will show you how to use it effectively.

If you haven’t downloaded and installed the software yet, or if you’re unsure where to begin, please visit our [Getting Started page](../general/getting-started/README) for step-by-step instructions.

The following sections will explain these topics:

* [**Before using the SMA**](before-using-the-sma/README) - Learn about the prerequisites and requirements needed to ensure the tool works effectively.
* [**Project Overview**](project-overview/README) - Understand how projects work in SMA and learn how to create and configure them.
* [**Optional Technical Discovery**](project-overview/optional-technical-discovery) - Gather high-level information about your workload.
* [**Assessment Overview**](assessment/README) - Learn how to use the tool to analyze your source code and generate an assessment report.
* [**Conversion Overview**](conversion/README) - Learn how to use the tool to convert your source code into the target format.

Let’s explore the key requirements needed for successful execution.

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