---
auto_generated: true
description: The Snowpark Migration Accelerator (SMA) analyzes your codebase and generates
  issue codes. While these codes provide detailed information, they fall into three
  main categories.
last_scraped: '2026-01-14T16:55:03.882439+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/sma-docs/issue-analysis/issue-code-categorization.html
title: 'Snowpark Migration Accelerator: Issue Code Categorization | Snowflake Documentation'
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

          + [Approach](approach.md)
          + [Issue code categorization](issue-code-categorization.md)
          + [Issue codes by source](issue-codes-by-source/README.md)
          + [Troubleshooting the output code](troubleshooting-the-output-code/README.md)
          + [Workarounds](workarounds.md)
          + [Deploying the output code](deploying-the-output-code.md)
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

[Guides](../../../guides/README.md)[Migrations](../../README.md)Tools[Snowpark Migration Accelerator](../README.md)Issue analysisIssue code categorization

# Snowpark Migration Accelerator: Issue Code Categorization[¶](#snowpark-migration-accelerator-issue-code-categorization "Link to this heading")

The Snowpark Migration Accelerator (SMA) analyzes your codebase and generates issue codes. While these codes provide detailed information, they fall into three main categories.

## Parsing Error[¶](#parsing-error "Link to this heading")

A parsing error occurs when SMA cannot understand or process a section of your source code. This happens when SMA encounters code that it either doesn’t recognize or considers invalid. These errors typically stem from one of two sources:

1. An issue within the SMA tool itself
2. Problems in your source code

This type of error can occur for various reasons.

* **Invalid Source Code**: The code must be executable in the source platform. If you provide code snippets or partial code that cannot run independently in the source platform, SMA will not be able to parse them.
* **Circular Dependencies**: When analyzing large codebases, SMA may encounter circular references between code elements. This can cause the tool to skip or fail to parse some of these interdependent references.
* **New Code Patterns**: While SMA is regularly updated, source platforms also evolve continuously. There might be cases where newly introduced code patterns are not yet supported by the tool.
* **Encoding Issues**: If your source code contains inconsistent encoding or unexpected characters at the beginning or end of files, SMA may generate parsing errors, even if the code runs successfully in the source platform.

When parsing errors occur, they are identified by specific error codes. To understand what these codes mean and how they relate to parsing errors, please refer to [the issue codes by source section](issue-codes-by-source/README) in our documentation.

## Conversion Error[¶](#conversion-error "Link to this heading")

A conversion error happens when SMA successfully identifies the code but is unable to convert it. Unlike parsing errors, conversion errors do not indicate problems with your source code. Instead, they show that SMA is working as intended by identifying code segments that are beyond its conversion capabilities.

There are several common reasons why code cannot be converted. These include:

* **The element from the source code cannot be implemented in Snowflake**. Currently, there is no equivalent functionality available in Snowflake for this source code element.
* **The specific usage of an element is not supported in Snowflake**. While Snowflake may support a particular element from the source platform, the way it’s being used in the source code is not compatible with Snowflake’s implementation.
* **Required parameters are not supported**. SMA creates a detailed functional model of the source code by analyzing how each element is used, rather than just identifying and categorizing elements. Sometimes, essential function parameters from the source code don’t have corresponding support in Snowflake.
* **Certain function combinations are incompatible**. SMA’s functional model analyzes how functions work together. Even when individual functions are supported in Snowflake, their combined usage might not be possible. In such cases, SMA will flag this as a conversion error.

Most error messages include specific recommendations or next steps to help you resolve the conversion issue. You can find these suggestions on the corresponding error page.

When SMA encounters a conversion error, it adds an EWI (Error, Warning, Info) comment in the converted code and records the error in [the issues inventory file](../user-guide/assessment/output-reports/sma-inventories.html#issue-inventory). The system will then:

* Add a comment symbol to the line containing the conversion error.
* Keep the line uncommented to prevent the file from executing.

When encountering conversion errors, each error has a unique error code. To understand what these codes mean and how to resolve them, please refer to [the issue codes by source section](issue-codes-by-source/README) in our documentation.

## Warning[¶](#warning "Link to this heading")

A warning differs from an error in SMA. Warnings appear when the tool detects changes that you should be aware of. While these changes won’t prevent your code from running, they indicate that certain aspects of your code may look or behave differently in the converted output compared to the source code.

Common reasons for warning messages:

* **The code appears different**. SMA performs transformations that generate an EWI (Error, Warning, or Information) message.
* **Some specific scenarios may not convert successfully**. The tool will generate a warning if a particular feature works in 99.9% of test cases but fails in certain parameter combinations. If your code uses these specific parameter combinations, you will receive a conversion error.
* **Elements were omitted**. This is the most frequent type of warning. Many functions or parameters that are essential in the source system are not required in Snowflake.

Warnings are informational messages that typically don’t require immediate action. However, we strongly recommend reviewing all warnings before deploying code to the target environment. These warnings should be considered during the testing phase of the converted code.

Warnings are identified by specific error codes. To understand what these codes mean, refer to [the issue codes by source section](issue-codes-by-source/README) in this documentation.

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

1. [Parsing Error](#parsing-error)
2. [Conversion Error](#conversion-error)
3. [Warning](#warning)