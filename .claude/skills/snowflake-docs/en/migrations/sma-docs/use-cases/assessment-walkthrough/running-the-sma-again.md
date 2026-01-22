---
auto_generated: true
description: To demonstrate the limitations of the tool, let’s analyze a less suitable
  workload. We’ll run the tool on a codebase that may not be an ideal candidate for
  migration.
last_scraped: '2026-01-14T16:51:58.381838+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/sma-docs/use-cases/assessment-walkthrough/running-the-sma-again
title: 'Snowpark Migration Accelerator:  Running the SMA Again | Snowflake Documentation'
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[Snowpark Migration Accelerator](../../README.md)Use cases[Assessment walkthrough](README.md)Running the SMA again

# Snowpark Migration Accelerator: Running the SMA Again[¶](#snowpark-migration-accelerator-running-the-sma-again "Link to this heading")

To demonstrate the limitations of the tool, let’s analyze a less suitable workload. We’ll run the tool on a codebase that may not be an ideal candidate for migration.

## Running on the Second Codebase[¶](#running-on-the-second-codebase "Link to this heading")

You can rerun the tool using either of these methods:

* Close and reopen the Snowpark Migration Accelerator (SMA). You can either open your previously created project or create a new one.
* Click the “RETRY ASSESSMENT” button at the bottom of the application window, as shown in the image.

![Retry Assessment](../../../../_images/retryAssessment.png)

For this lab, select the first option. Exit the SMA application and repeat the previous steps from the “Running the Tool” section. This time, when selecting the input folder, choose the directory containing the “needs\_more\_analysis” codebase.

After repeating the same steps, you will return to the “Analysis Complete” screen. This time, you will notice a different message in the result panel.

![Further Analysis Output Screen](../../../../_images/furtherAnalysis.png)

A low Readiness Score (below 60%) doesn’t automatically disqualify a workload from migration. Additional analysis is needed to make a proper assessment. Just like in our earlier example, there are several other factors we need to evaluate before making a final decision.

## Considerations[¶](#considerations "Link to this heading")

When reviewing a “needs more analysis” result, remember that we previously evaluated successful migrations based on three key factors: the Readiness Score, codebase size, and third-party imports. Let’s examine these same factors for cases requiring additional analysis.

### Possible code that could not be analyzed:[¶](#possible-code-that-could-not-be-analyzed "Link to this heading")

If you see numerous parsing errors (where the tool cannot understand the input code), your readiness score will be lower. While this could mean the code contains unfamiliar patterns, it’s more likely that there are issues with the exported code or the code is not valid in the original platform.

The tool displays accuracy information in multiple ways. The easiest method is to check the margin of error shown in the summary section on the first page of the report.

![Margin of Error](../../../../_images/marginError.png)

If the percentage of parsing errors is high (above 5%), follow these steps:

1. Verify that your source code runs correctly in the original platform
2. Contact the Snowpark Migration Accelerator team to identify the cause of the parsing errors

To check if there are parsing issues in your code, review the Snowpark Migration Accelerator Issue Summary at the end of the report. Pay special attention to error code SPRKPY1001. If this error appears in more than 5% of your files, it indicates that some code cannot be parsed. First, verify that the problematic code works in your source environment. If it does work, reach out to the Snowpark Migration Accelerator team for assistance.

### Non-Supported Spark Libraries[¶](#non-supported-spark-libraries "Link to this heading")

A low score indicates that your codebase contains functions that Snowpark does not yet support. Pay special attention if you see many instances of Spark ML, MLlib, or streaming functions, as these are key indicators of machine learning and streaming operations in your code. Currently, Snowpark has limited support for these features, which may impact your migration plans.

### Size[¶](#size "Link to this heading")

A low migration score may not always indicate a complex migration. Consider the context of your codebase. For example, if you have a score of 20% but only five references across 100 lines of code, this represents a small, manageable project that can be manually migrated with minimal effort.

If you have a large codebase (over 100,000 lines of code) with only a few Spark references, some of the code might not need conversion. This could include custom libraries created by your organization. In such cases, additional analysis would be needed to determine what code requires conversion.

In this example, the size is manageable. The project contains 150 files, with most containing Spark API references, and less than 1,000 lines of code.

## Summary[¶](#summary "Link to this heading")

In this example, the readiness score is low due to extensive use of Spark’s ml, mllib, and streaming libraries, rather than issues with third-party libraries or size inconsistencies. Given these complexities, we recommend:

1. Contacting [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) for guidance
2. Posting your questions in the [Snowflake Community forums on Spark Migration](https://community.snowflake.com/s/topic/0TO3r000000bskWGAQ/spark-migrations)

These resources will help you better understand the challenges in your specific workload.

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

1. [Running on the Second Codebase](#running-on-the-second-codebase)
2. [Considerations](#considerations)
3. [Summary](#summary)