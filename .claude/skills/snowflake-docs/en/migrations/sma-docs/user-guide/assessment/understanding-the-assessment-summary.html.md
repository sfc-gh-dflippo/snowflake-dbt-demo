---
auto_generated: true
description: After running an assessment, you can view the initial results and summary
  in the Assessment Summary Report. To access this report, click the View Results
  button.
last_scraped: '2026-01-14T16:55:03.599953+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/sma-docs/user-guide/assessment/understanding-the-assessment-summary.html
title: 'Snowpark Migration Accelerator: Understanding the Assessment Summary | Snowflake
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[Snowpark Migration Accelerator](../../README.md)User guide[Assessment](README.md)Understanding the assessment summary

# Snowpark Migration Accelerator: Understanding the Assessment Summary[¶](#snowpark-migration-accelerator-understanding-the-assessment-summary "Link to this heading")

After running an assessment, you can view the initial results and summary in the Assessment Summary Report. To access this report, click the **View Results** button.

![View Results](../../../../_images/01-ViewResults.png)

This will display your assessment report. Keep in mind that this report summarizes the information from the inventory files created in the [Output Reports](output-reports/README) folder during the SMA execution. For a comprehensive analysis, please review the [Detailed Report](output-reports/README) in the output directory.

The Assessment Results section of the application contains several components, which are explained in detail below.

## Standard Assessment Summary[¶](#standard-assessment-summary "Link to this heading")

The summary will appear as shown below:

![Assessment Summary](../../../../_images/AssessmentSummary.png)

In the top-right corner of the report, there is a date dropdown menu showing when your analysis was run. If you have executed the accelerator several times within the same project, the dropdown menu will display multiple dates. These dates correspond only to executions from your currently open project.

### Snowpark Connect Readiness Score[¶](#snowpark-connect-readiness-score "Link to this heading")

The Snowpark Connect Readiness Score will look something like this:

![Snowpark Connect Readiness Score](../../../../_images/understanding-the-assessment-summary-snowpark-connect-readiness-score.png)

1. **Readiness Score** - It will show you the readiness score you obtained. The Snowpark Connect readiness score indicates the proportion of Spark API references that are supported by Snowpark Connect. This score is calculated by dividing the number of supported Spark API references by the total Spark API references. You can learn more about this score in the [Snowpark Connect Readiness Score](readiness-scores.html#snowpark-connect-readiness-score) section.
2. **Score Explanation** - An explanation of what the Snowpark Connect Readiness score is and how to interpret it.
3. **Next Steps** - Depending on the readiness score obtained, the SMA will advise you on what actions you should take before proceeding to the next step.
4. **Score Breakdown** - A detailed explanation of how the Snowpark Connect Readiness Score was calculated. In this case, it will show you the number of Spark API references supported by Snowpark Connect divided by the total number of Spark API references.

**Supported Usages** refers to the number of Spark API references in a workload that are supported by Snowpark Connect. In contrast, **identified usages** represents the total count of Spark API references found within that workload.

### Spark API Readiness Score[¶](#spark-api-readiness-score "Link to this heading")

This report includes several items, with the Readiness Score being the most important metric.

Let’s examine each section in detail:

![Spark API Readiness Score](../../../../_images/understanding-the-assessment-summary-snowpark-readiness-score.png)

1. **Readiness Score** - The [Spark API Readiness Score](readiness-scores) is the main metric that SMA uses to evaluate how ready your code is for migration. This score represents the percentage of Spark API references that can be converted to Snowpark API. While this score is useful, it only considers Spark API references and doesn’t account for third-party libraries or other factors. Therefore, use it as an initial assessment rather than a complete evaluation.

   The score is calculated by dividing the number of convertible Spark API references by the total number of Spark API references found in your code. For example, if the score shows 3541/3746, it means 3541 references can be converted out of 3746 total references. A higher score indicates better compatibility with Snowpark API. You can find this score on the first page of the detailed report.
2. **Score Explanation** - This section provides details about what the Spark API Readiness score means and how to interpret your results.
3. **Next Steps** - Depending on the readiness score obtained, the SMA will advise you on what actions you should take before proceeding to the next step.
4. **Score Breakdown** - This section shows how your score was calculated using two key metrics:

   * **Usages ready for conversion**: The number of Spark API references (functions, elements, or import statements) that can be converted to Snowpark
   * **Identified usages**: The total number of Spark API references found in your code

### Third-Party Libraries Readiness Score[¶](#third-party-libraries-readiness-score "Link to this heading")

The Third-Party Libraries Readiness Score will be displayed in the following format:

![Third-Party Libraries Readiness Score](../../../../_images/ThirdPartyLibraries.png)

1. **Readiness Score** - Displays your readiness score and its category (green, yellow, or red). The Third-Party Libraries Readiness Score shows what percentage of your imported libraries are supported by Snowflake. For more details, see the [Third-Party API Readiness Score](readiness-scores.html#third-party-api-readiness-score) section.
2. **Next Steps** - Depending on the readiness score obtained, the SMA will advise you on what actions you should take before proceeding to the next step.
3. **Score Explanation** - Describes what the Third-Party Libraries Readiness score means and how to interpret your results.
4. **Score Breakdown** - Shows how your Third-Party Libraries Readiness Score was calculated using this formula:
   (Number of library calls supported in Snowpark) ÷ (Total number of identified library calls)

   Where:

   * “Library calls supported in Snowpark” means libraries that Snowpark can use
   * “Identified library calls” means all third-party library calls found in your code, including both Spark and non-Spark libraries, whether supported or not

### SQL Readiness Score[¶](#sql-readiness-score "Link to this heading")

The SQL Readiness Score will be displayed in the following format:

![SQL Readiness Score](../../../../_images/SQL.png)

* **Readiness Score** - Displays your readiness score and its category (green, yellow, or red). This score indicates how many SQL elements in your code can be successfully converted to Snowflake SQL. For more details, see the [SQL Readiness Score](readiness-scores.html#sql-readiness-score) section.
* **Next Steps** - Based on your readiness score, SMA provides recommendations for actions to take before proceeding.
* **Score Explanation** - Provides a clear explanation of the SQL Readiness score and how to interpret your results.
* **Score Breakdown** - Shows a detailed calculation of your SQL Readiness Score, calculated as: (number of supported elements) ÷ (total number of elements).

### Spark API Usages[¶](#spark-api-usages "Link to this heading")

Danger

The **Spark API Usages** section has been deprecated since version **2.0.2**. You can now find:

* A summary of Spark API usage in [the Detailed Report](output-reports/curated-reports)
* A complete list of all Spark API usage instances in [the Spark API Usages Inventory](output-reports/sma-inventories)

The report contains three main sections displayed as tabs:

1. Overall Usage Classification
2. Spark API Usage Categorization
3. Spark API Usages By Status

We will examine each section in detail below.

#### Overall Usage Classification[¶](#overall-usage-classification "Link to this heading")

This tab displays a table containing three rows that show:

* Supported operations
* Unsupported operations
* Total usage statistics

![Overall Usage Classification](../../../../_images/image%2855%29.png)

Additional details are provided in the following section:

1. **Usages Count** - The total number of times Spark API functions are referenced in your code. Each reference is classified as either supported or unsupported, with totals shown at the bottom.
2. **Files with at least 1 usage** - The number of files that contain at least one Spark API reference. If this number is less than your total file count, it means some files don’t use Spark API at all.
3. **Percentage of All Files** - Shows what portion of your files use Spark API. This is calculated by dividing the number of files with Spark API usage by the total number of code files, expressed as a percentage.

#### Spark API Usage Categorization[¶](#spark-api-usage-categorization "Link to this heading")

This tab displays the different types of Spark references detected in your codebase. It shows the overall Readiness Score (which is the same score shown at the top of the page) and provides a detailed breakdown of this score by category.

![Spark API Usage Categorization](../../../../_images/image%2848%29.png)

You can find all available categorizations in the [Spark Reference Categories](spark-reference-categories) section.

#### Spark API Usages By Status[¶](#spark-api-usages-by-status "Link to this heading")

The final tab displays a categorical breakdown organized by mapping status.

![Spark API Usages by Status](../../../../_images/image%2849%29.png)

The SMA tool uses seven main mapping statuses, which indicate how well Spark code can be converted to Snowpark. For detailed information about these statuses, refer to the [Spark Reference Categories](spark-reference-categories) section.

### Import Calls[¶](#import-calls "Link to this heading")

Danger

The **Import Calls** section has been removed since version **2.0.2**. You can now find:

* A summary of import statements in [the Detailed Report](output-reports/curated-reports.html#detailed-report)
* A complete list of all import calls in [the Import Usages Inventory](output-reports/sma-inventories)

The “Import Calls” section displays frequently used external library imports found in your codebase. Note that Spark API imports are excluded from this section, as they are covered separately in the “Spark API” section.

![Import Calls](../../../../_images/image%2846%29.png)

This table contains the following information:

The report displays the following information:

1. A table with 5 rows showing:

   * The 3 most frequently imported Python libraries
   * An “Other” row summarizing all remaining packages
   * A “Total” row showing the sum of all imports
2. A “Supported in Snowpark” column indicating whether each library is included in Snowflake’s [list of supported packages in Snowpark](https://repo.anaconda.com/pkgs/snowflake/).
3. An “Import Count” column showing how many times each library was imported across all files.
4. A “File Coverage” column showing the percentage of files that contain at least one import of each library. For example:

   * If ‘sys’ appears 29 times in the import statements but is only used in 28.16% of files, this suggests it’s typically imported once per file where it’s used.
   * The “Other” category might show 56 imports occurring across 100% of files.

For detailed import information per file, refer to the ImportUsagesInventory.csv file in the [Output Reports](output-reports/README).

### File Summary[¶](#file-summary "Link to this heading")

Danger

The **File Summary** section has been removed since version **2.0.2**. You can now find:

* A summary of files and file types in [the Detailed Report](output-reports/curated-reports)
* A complete list of all files (both analyzed and not analyzed) in [the File Inventory](output-reports/sma-inventories.html#files-inventory)

The summary report contains multiple tables displaying metrics organized by file type and size. These metrics provide insights into the codebase’s volume and help estimate the required effort for the migration project.

The Snowpark Migration Accelerator analyzes all files in your source codebase, including both code and non-code files. You can find detailed information about the scanned files in the [files.csv](output-reports/README) report.

The File Summary contains multiple sections. Let’s examine each section in detail.

#### File Type Summary[¶](#file-type-summary "Link to this heading")

The File Type Summary displays a list of all file extensions found in your scanned code repository.

![File Type Summary](../../../../_images/image%2841%29.png)

The file extensions listed indicate which types of code files SMA can analyze. For each file extension, you will find the following information:

* **Lines of Code** - The total number of executable code lines across all files with this extension. This count excludes comments and empty lines.
* **File Count** - The total number of files found with this extension.
* **Percentage of Total Files** - The percentage that files with this extension represent out of all files in the project.

To analyze your workload, you can easily identify whether it primarily consists of script files (such as Python or R), notebook files (like Jupyter notebooks), or SQL files. This information helps determine the main types of code files in your project.

#### Notebook Sizing by Language[¶](#notebook-sizing-by-language "Link to this heading")

The tool evaluates notebooks in your codebase and assigns them a “t-shirt” size (S, M, L, XL) based on the number of code lines they contain. This sizing helps estimate the complexity and scope of each notebook.

![Notebook Sizing By Language](../../../../_images/image%2842%29.png)

The notebook sizes are categorized according to the main programming language used within each notebook.

#### Notebook Stats By Language[¶](#notebook-stats-by-language "Link to this heading")

This table displays the total number of code lines and cells in all notebooks, organized by programming language.

![Notebook Stats by Language](../../../../_images/image%2843%29.png)

These notebooks are organized by the primary programming language used within them.

#### Code File Content[¶](#code-file-content "Link to this heading")

When running SMA, the tab name will change based on your source language:

* For Python source files, the tab will display “Python File Content”
* For Scala source files, the tab will display “Scala File Content”

This row shows how many files contain Spark API references. The “Spark Usages” row displays:

1. The number of files that use Spark APIs
2. What percentage these files represent of the total codebase files analyzed

![Code File Content](../../../../_images/image%2844%29.png)

This metric helps identify what percentage of files do not contain Spark API references. A low percentage suggests that many code files lack Spark dependencies, which could mean the migration effort might be smaller than initially estimated.

#### Code File Sizing[¶](#code-file-sizing "Link to this heading")

The File Sizing tab name changes based on your source language:

* For Python source files, it displays as “Python File Sizing”
* For Scala source files, it displays as “Scala File Sizing”

The codebase files are categorized using “t-shirt” sizes (S, M, L, XL). Each size has specific criteria described in the “Size” column. The table also shows what percentage of all Python files falls into each size category.

![Code File Sizing](../../../../_images/image%2845%29.png)

Understanding the file size distribution in your codebase can help assess workload complexity. A high percentage of small files typically suggests simpler, less complex workloads.

### Issues Summary[¶](#issues-summary "Link to this heading")

The Issues Summary provides critical information about potential problems found during code scanning. When transitioning from assessment to conversion, you’ll see a list of EWIs (Errors, Warnings, and Issues) detected in your codebase. For a detailed explanation of these issues, please refer to the Issue Analysis section in the documentation.

![Issues Summary](../../../../_images/04-IssuesSummary.png)

At the top of the issue summary, you will find a table that provides an overview of all identified issues.

![Issues Summary - Summary Table](../../../../_images/05-IssuesSummary-SummaryTable.png)

The table contains two rows.

* The “Number of issues” represents the total count of all issue codes found in each category.
* The “Number of unique issues” represents the count of distinct error codes found in each category.

The problems are divided into three main categories:

* **Warnings** indicate potential differences between source and target platforms that may not require immediate action but should be considered during testing. These could include slight variations in behavior for edge cases or notifications about changes in appearance compared to the source platform.
* **Conversion issues** highlight elements that either failed to convert or need additional configuration to work properly in the target platform.
* **Parsing issues** occur when the tool cannot interpret specific code elements. These are critical issues requiring immediate attention, typically caused by non-compiling source code or incorrect code extraction. If you believe your source code is correct but still receive parsing errors, it may be due to an unrecognized pattern in SMA. In such cases, please [report an issue](../project-overview/configuration-and-settings.html#report-an-issue) and include the problematic source code section.

The table summarizes the total count for each item.

Below this table, you will find a list of unique issue codes and their descriptions.

![Issue Summary - Issue Code Table](../../../../_images/06-IssueSummary-IssueCodeTable.png)

Each issue code entry provides:

* The unique issue identifier
* A description of the issue
* The number of occurrences
* The severity level (Warning, Conversion Error, or Parsing Error)

You can click any issue code to view detailed documentation that includes:

* A full description of the issue
* Example code
* Recommended solutions

For instance, clicking the first issue code shown above (SPRKPY1002) will take you to its dedicated documentation page.

By default, the table displays only the top 5 issues. To view all issues, click the SHOW ALL ISSUES button located below the table. You can also use the search bar above the table to find specific issues.

Understanding the remaining conversion work is crucial during assessment mode. You can find detailed information about each issue and its location in the issue inventory within the [Reports folder](output-reports/README).

### Execution Summary[¶](#execution-summary "Link to this heading")

The execution summary provides a comprehensive overview of the tool’s recent analysis. It includes:

* The code analysis score
* User details
* The unique execution ID
* Version information for both SMA and Snowpark API
* Project folder locations that were specified during [Project Creation](../project-overview/project-setup.html#creating-a-new-project)

![Execution Summary](../../../../_images/ExecutionSummary%281%29.png)

### Appendixes[¶](#appendixes "Link to this heading")

The appendixes contain additional reference information that can help you better understand the output generated by the SMA tool.

![image (512).png](../../../../_images/image%28512%29.png)

This guide contains general reference information about using the Snowpark Migration Accelerator (SMA). While the content may be updated periodically, it focuses on universal SMA usage rather than details about specific codebases.

---

This is what most users will see when they run the Snowpark Migration Accelerator (SMA). If you are using an older version, you might see the Abbreviated Assessment Summary instead, which is shown below.

## Abbreviated Assessment Summary [Deprecated][¶](#abbreviated-assessment-summary-deprecated "Link to this heading")

If your readiness score is low, your migration summary might appear as follows:

![Assessment Summary](../../../../_images/image%28495%29.png)

This summary contains the following information:

* **Execution Date**: Shows when your analysis was performed. You can view results from any previous execution for this project.
* **Result**: Indicates if your workload is suitable for migration based on the [readiness score](../../support/glossary.html#readiness-score). The readiness score is a preliminary assessment tool and does not guarantee migration success.
* **Input Folder**: Location of the source files that were analyzed.
* **Output Folder**: Location where analysis reports and converted code files are stored.
* **Total Files**: Number of files analyzed.
* **Execution Time**: Duration of the analysis process.
* **Identified Spark References**: Number of Spark API calls found in your code.
* **Count of Python (or Scala) Files**: Number of source code files in the specified programming language.

---

## Next Steps[¶](#next-steps "Link to this heading")

The application provides several additional features, which can be accessed through the interface shown in the image below.
![](../../../../_images/image%2854%29.png)

* **Retry Assessment** - You can run the assessment again by clicking the **Retry Assessment** button on the Assessment Results page. This is useful when you make changes to the source code and want to see updated results.
* **View Log Folder** - Opens the folder containing assessment execution logs. These text files provide detailed information about the assessment process and are essential for troubleshooting if the assessment fails. If technical support is needed, you may be asked to share these logs.
* **View Reports** - Opens the folder containing assessment output reports. These include the detailed assessment report, Spark reference inventory, and other analyses of your source codebase. Each report type is explained in detail in this documentation.
* **Continue to Conversion** - While this may seem like the next logical step, it’s important to review the assessment results thoroughly before proceeding. Note that running a conversion requires an access code. For more information, see the [conversion section of this documentation](../conversion/README).

The following pages provide detailed information about the reports generated each time the tool runs.

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

1. [Standard Assessment Summary](#standard-assessment-summary)
2. [Abbreviated Assessment Summary [Deprecated]](#abbreviated-assessment-summary-deprecated)
3. [Next Steps](#next-steps)