---
auto_generated: true
description: With Snowpark Connect for Spark, you can run your Spark code with Snowflake.
last_scraped: '2026-01-14T16:51:36.493574+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/sma-docs/use-cases/snowpark-connect/identifying-fully-compatible-files
title: 'Snowpark Migration Accelerator: Determining Compatibility with Snowpark Connect
  | Snowflake Documentation'
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
          + [Assessment walkthrough](../assessment-walkthrough/README.md)
          + [Conversion walkthrough](../conversion-walkthrough.md)
          + [Migration lab](../migration-lab/README.md)
          + [Sample project](../sample-project.md)
          + [Using SMA in an Ubuntu Docker image](../using-snowconvert-in-a-ubuntu-docker-image.md)
          + [SMA CLI walkthrough](../sma-cli-walkthrough.md)
          + [Snowpark Connect](README.md)

            - [Compatible files](identifying-fully-compatible-files.md)
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[Snowpark Migration Accelerator](../../README.md)Use cases[Snowpark Connect](README.md)Compatible files

# Snowpark Migration Accelerator: Determining Compatibility with Snowpark Connect[¶](#snowpark-migration-accelerator-determining-compatibility-with-snowpark-connect "Link to this heading")

With [Snowpark Connect for Spark](../../../../developer-guide/snowpark-connect/snowpark-connect-overview), you can run your Spark code with
Snowflake.

You can determine if a Spark workload is a good fit for Snowpark Connect for Spark by using the following steps:

1. Take a moment to understand what you have and what you are looking to do.

   Snowpark Connect for Spark will be a great choice for many Spark workloads, but not all.
2. Run the Snowpark Migration Accelerator (SMA), as described below.

   Currently, the SMA will report on compatibility for Snowpark Connect for Spark for any code written in Python with references to the
   Spark API.
3. Use the SMA to identify all references to the Spark API that are present in the codebase you’ve scanned with it.

## Analyze compatibility with the SMA[¶](#analyze-compatibility-with-the-sma "Link to this heading")

### Accessing the SMA[¶](#accessing-the-sma "Link to this heading")

The Snowpark Migration Accelerator (SMA) is a tool that accelerates the migration of pipelines written in or with Spark. The SMA assesses
the compatibility of references of the Spark API in Python and Scala code, and can convert some references to the Snowpark API.

### Installation[¶](#installation "Link to this heading")

You can download the SMA from the Snowflake website as described in [Installation](../../general/getting-started/installation/README).

### Before running the SMA[¶](#before-running-the-sma "Link to this heading")

Once you have installed the SMA, you can assess a codebase. As you do, keep in mind the following:

* The SMA can only analyze [certain extensions](../../user-guide/before-using-the-sma/supported-filetypes) for references
  to the Spark API. However, only Python code can be analyzed for Snowpark Connect.

  Notebooks and code files can be processed at the same time.
* The SMA reads files from a local directory. You will need to put them all in a root directory (there can be as many subdirectories as you
  like) for the SMA to analyze them. You can run many files or a single file through as much as you like.

For more SMA considerations, see [Before Using the SMA](../../user-guide/before-using-the-sma/README).

## Generating the assessment[¶](#generating-the-assessment "Link to this heading")

1. Open the Snowpark Migration Accelerator (SMA).
2. Start a new project.

   Fill out the fields on the [project creation screen](../../user-guide/project-overview/project-setup.html#creating-a-new-project),
   including the locally accessible directory where the source codebase is. The final field **Customer’s Company** helps Snowflake
   identify other runs of the SMA that may be related to your codebase or other codebases (depending on how you name it), both in the
   past or the future.

   ![Create new project](../../../../_images/new-project-scos.png)
3. Select **Start assessment**.

   ![Start assessment](../../../../_images/start-assessment-scos.png)
4. The SMA will show the following screen while assessing:

   ![Analysis in progress](../../../../_images/analysis-in-progress.png)
5. When assessment has finished, select **VIEW REPORTS** to view scores.

   ![Readiness scores](../../../../_images/readiness-scores-scos.png)
6. Determine a codebase’s compatibility with Snowpark Connect by looking at the Snowpark Connect Readiness Score.

   The number of [Readiness Scores](../../user-guide/assessment/readiness-scores) shown varies depending on the SMA version
   you run.

   The percentage shown is the count of references to the Spark API that are fully compatible with Snowpark Connect. Next to the
   percentage, you’ll find green (greater than 90 percent of references are supported), yellow (between 70 percent and 90 percent of references are
   supported), or red (less than 70 percent of references are supported) indicators.
7. Expand the score by selecting the dropdown arrow to the right of the score tab.

   ![Expand Snowpark Connect score](../../../../_images/expand-snowpark-connect-score.png)

   The following shows the expanded tab:

   ![Expanded Snowpark Connect score](../../../../_images/expanded-snowpark-connect-score.png)

   The following describes what the indicators mean:

   * **Green**: Good candidate for Snowpark Connect (less than 10 percent of references to the Spark API are not supported in Snowpark Connect).
   * **Yellow**: Possibly a good candidate.

     Determine if you can make what is not supported work with Snowpark Connect. You can use the SMA to convert to the Snowpark API
     and compare that result with the Snowpark Readiness Score to see which is a better fit.
   * **Red**: Could still work, but there’s a lot of incompatibility.

     Check the Snowpark API Readiness score. If that is high (greater than 90 percent), then it’s likely that Snowpark is the better route
     for migration for this workload.

   For the yellow and red options, reach out to sma-support@snowflake.com for more support, but for the green indicator you may want to
   see if you can take the next step and identify a POC.

Note

The SMA does not convert anything to Snowpark Connect. You can choose **Continue to Conversion** in the SMA user interface, but that will only
convert the code to the Snowpark API.

## Determining what files are ready to run with Snowpark Connect[¶](#determining-what-files-are-ready-to-run-with-snowpark-connect "Link to this heading")

The score is a high level indicator, but the SMA allows you to see exactly what elements of the Spark API are supported and what files are
fully supported.

Note

This guide shows you how to do this locally, but you can also use the [Interactive Assessment Application (IAA)](../../interactive-assessment-application/overview).

To determine what files are ready to run, you will have to use the `SparkUsagesInventory.csv` file generated in the
[local Reports output folder](../../user-guide/assessment/output-reports/README) by the SMA. This file lists every
reference to the Spark API found by the SMA.

1. Navigate to the reports directory from the application by selecting VIEW REPORTS.

   ![View reports button](../../../../_images/view-reports-button.png)

   This will take you to a local directory that has a large number of inventories and other reports that the SMA generates.

   ![Local directory with inventories and reports](../../../../_images/local-directory-inventories-reports.png)
2. Open the `SparkUsagesInventory.csv` file in a spreadsheet editor.
3. Locate the **IsSnowparkConnectSupported** field.

   This will give a TRUE or FALSE indicator of each element of the Spark API.

   ![IsSnowparkConnectSupported field](../../../../_images/is-snowpark-connect-supported-field.png)
4. Pivot this spreadsheet to determine if there are any files that are fully supported.

   1. Insert a pivot table with the entire spreadsheet in the range for the pivot.

      ![Insert pivot table](../../../../_images/insert-pivot-table.png)
   2. Select **FileId** as the row, and **IsSnowparkConnectSupported** as the column and values.

      ![Select FileId and IsSnowparkConnectSupported](../../../../_images/select-fileid-issnowparkconnectsupported.png)

      This will give you a result that looks like the following image:

      ![Filter result](../../../../_images/filter-result.png)
   3. Sort the result by FALSE ascending (meaning, lowest to highest).

      ![Sort result by FALSE ascending](../../../../_images/sort-result-by-false-ascending.png)
   4. If there are any files that have zero unsupported references in Snowpark Connect, they will show up at the top.

      ![Files with zero unsupported references](../../../../_images/files-with-zero-unsupported-references.png)

      There are none in this example (the lowest count of unsupported references in a specific file is 1).
   5. From this, you can use the artifact dependency output of the SMA to get the dependencies for the file list above.

      With those dependencies, you can see what inputs or outputs may be present in order to run the file, and ultimately build a POC.

Was this page helpful?

YesNo

[Visit Snowflake](https://www.snowflake.com)

[Join the conversation](https://community.snowflake.com/s/)

[Develop with Snowflake](https://developers.snowflake.com)

[Share your feedback](/feedback)

[Read the latest on our blog](https://www.snowflake.com/blog/)

[Get your own certification](https://learn.snowflake.com)

[Privacy Notice](https://www.snowflake.com/privacy-policy/)[Site Terms](https://www.snowflake.com/legal/snowflake-site-terms/)Cookies Settings© 2026 Snowflake, Inc. All Rights Reserved.

On this page

1. [Analyze compatibility with the SMA](#analyze-compatibility-with-the-sma)
2. [Generating the assessment](#generating-the-assessment)
3. [Determining what files are ready to run with Snowpark Connect](#determining-what-files-are-ready-to-run-with-snowpark-connect)