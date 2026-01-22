---
auto_generated: true
description: The Snowpark Migration Accelerator (SMA) evaluates your code and produces
  detailed assessment data. To make this information more accessible, SMA calculates
  Readiness Scores that measure how easily yo
last_scraped: '2026-01-14T16:54:58.905684+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/sma-docs/user-guide/assessment/readiness-scores.html
title: 'Snowpark Migration Accelerator: Readiness Scores | Snowflake Documentation'
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
          + [Before using the SMA](../before-using-the-sma/README.md)
          + [Project overview](../project-overview/README.md)
          + [Technical discovery](../project-overview/optional-technical-discovery.md)
          + [AI assistant](../chatbot.md)
          + [Assessment](README.md)

            - [How the assessment works](how-the-assessment-works.md)
            - [Assessment quick start](assessment-quick-start.md)
            - [Understanding the assessment summary](understanding-the-assessment-summary.md)
            - [Readiness scores](readiness-scores.md)
            - [Output reports](output-reports/README.md)
            - [Output logs](output-logs.md)
            - [Spark reference categories](spark-reference-categories.md)
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[Snowpark Migration Accelerator](../../README.md)User guide[Assessment](README.md)Readiness scores

# Snowpark Migration Accelerator: Readiness Scores[¶](#snowpark-migration-accelerator-readiness-scores "Link to this heading")

The Snowpark Migration Accelerator (SMA) evaluates your code and produces detailed assessment data. To make this information more accessible, SMA calculates Readiness Scores that measure how easily your code can be migrated to Snowflake. These scores act as compatibility indicators - the higher the score, the more compatible your code is with Snowflake’s platform. You can obtain these scores by simply running the SMA tool.

The SMA generates the following Readiness Scores:

* [Snowpark API Readiness Score](#snowpark-api-readiness-score)
* [Snowpark Connect Readiness Score](#snowpark-connect-readiness-score)
* [Third Party API Readiness Score](#third-party-api-readiness-score)
* [SQL Readiness Score](#sql-readiness-score)

The Readiness Scores indicate how compatible your code is with Snowflake, not how much work remains to be done. Even with a high readiness score, the remaining incompatible code might still require significant effort to migrate. To accurately estimate the work needed for migration, review the complete assessment report. If you need help creating a migration plan or estimating the effort required, please [reach out](../../support/contact-us) to our team.

## Levels[¶](#levels "Link to this heading")

The Snowpark Migration Accelerator (SMA) uses a color-coded scoring system similar to a traffic light:

* **Red** - Critical issue detected. Stop immediately and resolve the problem, as it significantly impacts the migration process or prevents accurate code analysis. Follow the provided action steps before proceeding.
* **Yellow** - Warning detected. Review the action steps carefully and understand the potential impact on your migration. Once you understand the implications, you may continue to the next step.
* **Green** - No major issues detected. While this indicates there are no significant blockers for migration, the code may still need adjustments. Review the action steps and continue with the migration process.

## How to Interpret the Scores[¶](#how-to-interpret-the-scores "Link to this heading")

For each score, you will receive:

* A numerical value
* A status indicator (red, yellow, or green as explained earlier)
* A recommended next action

We strongly recommend that you:

* **Review scores sequentially** - When you encounter a red score, investigate and address that issue right away
* **Review all recommended actions for every score** - Check the suggested next steps for all results, including green scores, as they contain important action items

Let’s examine the readiness scores currently available in the system.

## Snowpark API Readiness Score[¶](#snowpark-api-readiness-score "Link to this heading")

The Snowpark Migration Accelerator (SMA) generates a Snowpark API Readiness Score, which indicates how ready your code is for migration. It’s important to note that this score only evaluates the usage of Spark API components and does not assess other elements such as third-party libraries or external dependencies in your code.

When SMA analyzes your code, it identifies all Spark API references, including both import statements and function calls. These references are documented in [the Spark API Usages Inventory](output-reports/sma-inventories), which you can find in your local output directory. Each reference is classified as either “supported” or “not supported” according to [the Spark Reference Categories](spark-reference-categories). The readiness score is calculated by dividing the number of supported references by the total number of references found in your code.

![Snowpark API Readiness Score Calculation](../../../../_images/image%28528%29.png)

This score is displayed as a percentage, indicating how well Snowflake supports the Spark API references found in your code. A higher percentage means better compatibility with Snowflake. You can view this score in both the [detailed report](output-reports/curated-reports) and the [assessment summary](understanding-the-assessment-summary) sections of the application.

The Readiness Score shown here is the original score generated by the SMA. For newer SMA versions that display only one Readiness Score, this score specifically measures Spark API compatibility.

### Snowpark API Readiness Levels[¶](#snowpark-api-readiness-levels "Link to this heading")

Based on the calculated score, the result will be classified into one of three categories: green, yellow, or red. The application and output report will provide specific recommendations based on your score category.

The Snowpark API Readiness Score will be assigned one of these levels:

* Green: Most Spark API references are supported, making this workload a strong candidate for migration. If other indicators are also green, consider proceeding with a Proof of Concept.
* Yellow: Some Spark API references are not supported, which will require additional migration effort. Next steps should include creating an inventory of unsupported items and estimating the conversion effort needed.

## Snowpark Connect Readiness Score[¶](#snowpark-connect-readiness-score "Link to this heading")

The Snowpark Connect Readiness Score measures the percentage of Spark API references in your codebase that are supported by Snowpark Connect. This score provides an assessment of your existing Spark API code’s readiness for execution within the Snowpark Connect environment.

### How It’s Calculated[¶](#how-it-s-calculated "Link to this heading")

During its execution, the SMA scans your codebase to identify all references to the Spark API. Examples of such references include import statements, function calls, and class instantiations. All discovered references are then logged in the [Spark API Usages Inventory](output-reports/sma-inventories.html#spark-usages-inventory). This inventory is generated as a file in your local output directory. For every reference listed in the inventory, the SMA populates the `IsSnowparkConnectToolSupported` column, setting it to `True` if the API usage is supported by Snowpark Connect, or `False` if it is not.

To calculate the readiness score, the SMA takes all of the supported references and divides them by the total references found in the codebase:

![Snowpark Connect Readiness Score Calculation](../../../../_images/snowpark-connect-readiness-score-formula.png)

For example, if your codebase has 100 Spark API references and 90 of them are supported by Snowpark Connect, your Snowpark Connect Readiness Score would be 90%.

A higher percentage for the Snowpark Connect Readiness Score indicates a greater degree of compatibility with Snowpark Connect, suggesting that a larger portion of your Spark code aligns with functionalities supported by Snowpark Connect.

### Readiness Levels[¶](#readiness-levels "Link to this heading")

The compatibility analysis yields a readiness score, which is categorized into one of three distinct levels: **Green**, **Yellow**, or **Red**. Both the application’s [assessment summary](understanding-the-assessment-summary) and the generated [detailed report](output-reports/curated-reports) will display this readiness level, accompanied by specific guidance tailored to the findings:

* Green - This workload is highly compatible with Snowpark Connect as the majority of references to the Spark API are supported without any code changes. [Files that are fully compatible](../../use-cases/snowpark-connect/identifying-fully-compatible-files) can be run immediately, though some files will still require [issue resolution](../../issue-analysis/approach).

  A good next step would be to try to [run some of the files in Snowflake](../../../../developer-guide/snowpark-connect/snowpark-connect-overview). View the [reports](output-reports/README) generated by the SMA and select a file that might be [ready to run with Snowpark Connect](../../use-cases/snowpark-connect/README).
* Yellow - There are some elements of the Spark API in this workload that are not supported in Snowpark Connect or are incompatible with [Snowpark Connect for Spark](../../../../developer-guide/snowpark-connect/snowpark-connect-compatibility). This workload may still be able to run with Snowpark Connect, but there are elements that will require [issue resolution](../../issue-analysis/approach) or even re-architecture.

  The recommended next step would be to evaluate if code conversion makes more sense. You can do this by [converting this workload to the Snowpark API](../conversion/README), and reviewing the Snowpark API Readiness Score. You can also dive deeper into this workload’s compatibility with Snowpark Connect by viewing the [reports](output-reports/README) generated by the SMA. You can explore the compatibility with Snowpark by [understanding which files may be ready to run](../../use-cases/snowpark-connect/README) and working through the Spark elements that have [issues that need resolution](../../issue-analysis/approach).
* Red - This workload has a significant number of references to the Spark API that are not supported in Snowpark Connect. However, this workload may still be a good candidate for conversion to the Snowpark API. The recommended next step would be to [convert this workload](../conversion/README), and take a look at the [Snowpark API Readiness Score](#snowpark-api-readiness-score). If you need help, feel free to reach out to sma-support@snowflake.com.

  If you would still like to further explore the compatibility with Snowpark Connect, you can view the [reports](output-reports/README) generated by the SMA. A good place to start would be to [understand which files may be ready to run](../../use-cases/snowpark-connect/README).

## Third-Party API Readiness Score[¶](#third-party-api-readiness-score "Link to this heading")

The Third-Party Readiness Score shows how many of your imported libraries can be used in Snowflake. To better understand this score, let’s first explain what we mean by “Third Party”:

**Third Party Library**: Any software package or library that is not developed, maintained, or controlled by Snowflake (or Snowpark in Snowflake).

The readiness score indicates the percentage of external libraries and packages that are compatible with Snowflake. For Python code, compatibility means the package is available through the [Anaconda package collection in Snowpark](../../../../developer-guide/udf/python/udf-python-packages.html#label-python-udfs-anaconda). For Scala or Java code, compatibility means the package is already included in Snowpark’s core functionality.

The readiness score is calculated by dividing the number of supported third-party library imports by the total number of third-party library imports in your code.

![Third Party API Readiness Score Calculation](../../../../_images/image%2820%291.png)

Important Information About the Readiness Score:

* **Supported Third-Party Libraries in Snowpark**: This includes all libraries that Snowpark supports (including org.apache.spark)
* **Total Third-Party Library Calls**: The sum of all third-party library calls found in the code, including both Spark and non-Spark libraries, whether supported or unsupported by Snowpark.
* Only imports marked as “ThirdPartyLib” in the Import Usages Inventory are counted. Internal dependencies and imports from within the codebase are excluded.
* This metric counts the total number of calls, not unique library references. For example, if your code has 100 library calls total, with 80 calls to an unsupported library and 20 calls to a supported library, the support score would be 20%. This shows the actual usage frequency of supported vs. unsupported libraries in the code, rather than the ratio of unique library references.

### Third Party API Readiness Levels[¶](#third-party-api-readiness-levels "Link to this heading")

Based on the calculated score, the result will be classified into one of three categories: green, yellow, or red. The application and output report will provide specific recommendations based on your score category.

The Third Party API Readiness Score will be assigned one of these levels:

* Green - The codebase uses Python libraries that are fully supported in Snowflake. No additional configuration is required.
* Yellow - The codebase contains at least one Python package or library that is not currently supported in Snowpark. You can add unsupported third-party packages using several methods described in the [third-party package documentation](../../../../developer-guide/udf/python/udf-python-packages.html#label-python-udfs-anaconda). To identify unsupported packages, review the [Import Usages Inventory](output-reports/sma-inventories.html#import-usages-inventory) generated by SMA. Then analyze how these packages are used in your code and plan their implementation in Snowflake.
* Red - The codebase heavily relies on packages or libraries not supported in Snowpark. This could mean either a single unsupported library is used extensively throughout the code, or multiple unsupported libraries are used across different parts of the codebase. A thorough assessment of these import statements is necessary to understand their impact. For guidance or assistance with package support, contact [sma-support@snowflake.com](mailto:sma-support%40snowflake.com).

## SQL Readiness Score[¶](#sql-readiness-score "Link to this heading")

The SQL Readiness Score indicates what percentage of SQL elements in your source code can be automatically converted to Snowflake SQL using the Snowpark Migration Accelerator (SMA). A higher score means more of your code can be converted automatically, which makes the migration process easier and faster.

The readiness score is calculated by dividing the number of SQL elements that can be converted by the total number of SQL elements found in the source code.

![SQL Readiness Score Calculation](../../../../_images/Readiness.png)

### SQL Readiness Score Levels[¶](#sql-readiness-score-levels "Link to this heading")

The SQL Readiness Score will be assigned one of these levels:

* Green - Most SQL in this codebase is either directly supported by Snowflake or can be automatically converted by the SMA. While no conversion is perfect, this workload requires minimal manual adjustments for Snowflake migration.
* Yellow - Some SQL elements in this codebase are not supported by Snowflake, requiring additional effort for migration. Review the SQL Element Inventory for unsupported features and check the EWI’s in the issues output to create an action plan. You may need to make minor code adjustments or partially redesign some components.
* Red - A large portion of SQL in this codebase is not compatible with Snowflake, suggesting significant redesign may be necessary. To proceed, review the SQL Element Inventory for unsupported features and examine the EWI’s in the issues output to develop a migration strategy. For assistance, contact [sma-support@snowflake.com](mailto:sma-support%40snowflake.com).

---

While readiness scores provide valuable insights, they should not be the only factor in determining a workload’s migration readiness. Consider multiple aspects of your migration plan alongside these scores, as they serve as an initial assessment rather than a complete evaluation. If you notice any readiness metrics that could be improved or aren’t accurately represented in the tool, please [let us know](../../support/contact-us). The SMA team continuously works to enhance and refine these readiness measurements.

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

1. [Levels](#levels)
2. [How to Interpret the Scores](#how-to-interpret-the-scores)
3. [Snowpark API Readiness Score](#snowpark-api-readiness-score)
4. [Snowpark Connect Readiness Score](#snowpark-connect-readiness-score)
5. [Third-Party API Readiness Score](#third-party-api-readiness-score)
6. [SQL Readiness Score](#sql-readiness-score)