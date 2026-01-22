---
auto_generated: true
description: 2023-10-24 Added Add condensed ID for filenames and use it in the log.
last_scraped: '2026-01-14T16:51:19.702374+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/sma-docs/general/release-notes/old-version-release-notes/sc-spark-scala-release-notes/README
title: 'Snowpark Migration Accelerator:  SC Spark Scala Release Notes | Snowflake
  Documentation'
---

1. [Overview](../../../../../../guides/README.md)
2. [Snowflake Horizon Catalog](../../../../../../user-guide/snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../../../../../../guides/overview-connecting.md)
6. [Virtual warehouses](../../../../../../user-guide/warehouses.md)
7. [Databases, Tables, & Views](../../../../../../guides/overview-db.md)
8. [Data types](../../../../../../data-types.md)
10. Data Integration

    - [Snowflake Openflow](../../../../../../user-guide/data-integration/openflow/about.md)
    - Apache Iceberg™

      - [Apache Iceberg™ Tables](../../../../../../user-guide/tables-iceberg.md)
      - [Snowflake Open Catalog](../../../../../../user-guide/opencatalog/overview.md)
11. Data engineering

    - [Data loading](../../../../../../guides/overview-loading-data.md)
    - [Dynamic Tables](../../../../../../user-guide/dynamic-tables-about.md)
    - [Streams and Tasks](../../../../../../user-guide/data-pipelines-intro.md)
    - [dbt Projects on Snowflake](../../../../../../user-guide/data-engineering/dbt-projects-on-snowflake.md)
    - [Data Unloading](../../../../../../guides/overview-unloading-data.md)
12. [Storage Lifecycle Policies](../../../../../../user-guide/storage-management/storage-lifecycle-policies.md)
13. [Migrations](../../../../../README.md)

    * Tools

      * [SnowConvert AI](../../../../../snowconvert-docs/overview.md)
      * [Snowpark Migration Accelerator](../../../../README.md)

        + General

          + [Introduction](../../../introduction.md)
          + [Getting started](../../../getting-started/README.md)
          + [Conversion software terms of use](../../../conversion-software-terms-of-use/README.md)
          + [Release notes](../../README.md)

            - [Old version release notes](../README.md)

              * [SC Spark Scala release notes](README.md)

                + [Known issues](known-issues.md)
              * [SC Spark Python release notes](../sc-spark-python-release-notes/README.md)
          + [Roadmap](../../../roadmap.md)
        + User guide

          + [Overview](../../../../user-guide/overview.md)
          + [Before using the SMA](../../../../user-guide/before-using-the-sma/README.md)
          + [Project overview](../../../../user-guide/project-overview/README.md)
          + [Technical discovery](../../../../user-guide/project-overview/optional-technical-discovery.md)
          + [AI assistant](../../../../user-guide/chatbot.md)
          + [Assessment](../../../../user-guide/assessment/README.md)
          + [Conversion](../../../../user-guide/conversion/README.md)
          + [Using the SMA CLI](../../../../user-guide/using-the-sma-cli/README.md)
        + Use cases

          + Snowflake VS Code extension

            + [SMA checkpoints walkthrough](../../../../use-cases/sma-checkpoints-walkthrough/README.md)
            + [SMA EWI Assistant walkthrough](../../../../use-cases/sma-ewi-assistant-walkthrough/README.md)
          + [Assessment walkthrough](../../../../use-cases/assessment-walkthrough/README.md)
          + [Conversion walkthrough](../../../../use-cases/conversion-walkthrough.md)
          + [Migration lab](../../../../use-cases/migration-lab/README.md)
          + [Sample project](../../../../use-cases/sample-project.md)
          + [Using SMA in an Ubuntu Docker image](../../../../use-cases/using-snowconvert-in-a-ubuntu-docker-image.md)
          + [SMA CLI walkthrough](../../../../use-cases/sma-cli-walkthrough.md)
          + [Snowpark Connect](../../../../use-cases/snowpark-connect/README.md)
        + Issue analysis

          + [Approach](../../../../issue-analysis/approach.md)
          + [Issue code categorization](../../../../issue-analysis/issue-code-categorization.md)
          + [Issue codes by source](../../../../issue-analysis/issue-codes-by-source/README.md)
          + [Troubleshooting the output code](../../../../issue-analysis/troubleshooting-the-output-code/README.md)
          + [Workarounds](../../../../issue-analysis/workarounds.md)
          + [Deploying the output code](../../../../issue-analysis/deploying-the-output-code.md)
        + Translation reference

          + [Translation reference overview](../../../../translation-reference/translation-reference-overview.md)
          + [SIT tagging](../../../../translation-reference/sit-tagging/README.md)
          + [SQL embedded code](../../../../translation-reference/sql-embedded-code.md)
          + [HiveSQL](../../../../translation-reference/hivesql/README.md)
          + [Spark SQL](../../../../translation-reference/spark-sql/README.md)
        + Workspace estimator

          + [Overview](../../../../workspace-estimator/overview.md)
          + [Getting started](../../../../workspace-estimator/getting-started.md)
        + Interactive assessment application

          + [Overview](../../../../interactive-assessment-application/overview.md)
          + [Installation guide](../../../../interactive-assessment-application/installation-guide.md)
        + Support

          + [General troubleshooting](../../../../support/general-troubleshooting/README.md)
          + [Frequently asked questions](../../../../support/frequently-asked-questions-faq/README.md)
          + [Glossary](../../../../support/glossary.md)
          + [Contact us](../../../../support/contact-us.md)
    * Guides

      * [Teradata](../../../../../guides/teradata.md)
      * [Databricks](../../../../../guides/databricks.md)
      * [SQL Server](../../../../../guides/sqlserver.md)
      * [Amazon Redshift](../../../../../guides/redshift.md)
      * [Oracle](../../../../../guides/oracle.md)
      * [Azure Synapse](../../../../../guides/azuresynapse.md)
15. [Queries](../../../../../../guides/overview-queries.md)
16. [Listings](../../../../../../collaboration/collaboration-listings-about.md)
17. [Collaboration](../../../../../../guides/overview-sharing.md)
19. [Snowflake AI & ML](../../../../../../guides/overview-ai-features.md)
21. [Snowflake Postgres](../../../../../../user-guide/snowflake-postgres/about.md)
23. [Alerts & Notifications](../../../../../../guides/overview-alerts.md)
25. [Security](../../../../../../guides/overview-secure.md)
26. [Data Governance](../../../../../../guides/overview-govern.md)
27. [Privacy](../../../../../../guides/overview-privacy.md)
29. [Organizations & Accounts](../../../../../../guides/overview-manage.md)
30. [Business continuity & data recovery](../../../../../../user-guide/replication-intro.md)
32. [Performance optimization](../../../../../../guides/overview-performance.md)
33. [Cost & Billing](../../../../../../guides/overview-cost.md)

[Guides](../../../../../../guides/README.md)[Migrations](../../../../../README.md)Tools[Snowpark Migration Accelerator](../../../../README.md)General[Release notes](../../README.md)[Old version release notes](../README.md)SC Spark Scala release notes

# Snowpark Migration Accelerator: SC Spark Scala Release Notes[¶](#snowpark-migration-accelerator-sc-spark-scala-release-notes "Link to this heading")

## 2.14.0[¶](#id1 "Link to this heading")

2023-10-24   
  
Added  
  
Add condensed ID for filenames and use it in the log.

Changed

Refactor output folder hierarchy of the TrialMode.

Generate Reports locally in Assessment mode when the score hits 90 or higher.

Generate Reports locally in Assessment mode when it’s a Snowflake user.

Create inventories as .csv files.

Move inventories to the Reports folder.

## 2.13.0[¶](#id2 "Link to this heading")

2023-10-19\

Added\

* Add a flag to enable more logging messages.
* Add a flag to disable the execution of the conversion.
* Add a timeout mechanism for Scala symbol table resolution.
* Add a timeout mechanism for Scala parsing phase.
* Add progress log messages in parsing phase for Scala.

Changed\

* Adjustments to reports (HTML and docx): renaming readiness score and updating appendix and imports call table.
* Bump `AssessmentMode` from 8.1.6 to 9.0.4
* Bump `Common.AssessmentModel` from 3.1.12 to 3.1.14
* Add lock to avoid race condition

Fixed\

* Fix an inconsistent number of SparkReferences between assessment and conversion modes.
* Fix issue causing .sql files to not be recognized as supported files.
* Fix parsing error when a backslash is between AtomElement and BracedSlices.
* Fix issue when parsing code with a big quantity of nested expressions took a lot of time.

## 2.12.0[¶](#id3 "Link to this heading")

2023-10-13

Added

* Add Trial Mode support.

Changed

* Bump `Snowflake.SnowConvert.Python` from 1.1.79 to 1.1.80
* Add a variant of ResolveType to avoid stack overflow at some scenarios.

Fixed

* Fix scenario when resolving a FullName causes stack overflow.

## 2.11.0[¶](#id4 "Link to this heading")

Added

* Add support for Snowpark API version 1.7.0 on Python.
* Add support for Snowpark API version 1.6.1 on Python.
* A new workaround added
* Four (4) new mappings added

Changed

* Update Scala integration test validations.
* Reduce Scala integration tests time.
* Update the remaining assembly name references in the internal code.
* Update source file headers to match company guidelines.

Fixed

* Fix multiple executions with same ExecutionId by adding SessionId and ExecutionId to inventories and reports.
* Fix failing CopyOtherFiles task with storage.lck file.
* Fix issue generating .HTML reports when some values are null.

## 2.09.0[¶](#id5 "Link to this heading")

2023-10-03

Added

* Add FilesInventory.pam
* Four (4) new mappings added

Changed

* Change assembly names.
* Bump `Snowflake.SnowConvert.Python` from 1.1.70 to 1.1.79
* Add a backslash in three different rules to solve parsing errors.
* Add a new spark reference symbol.
* Support two (2) new resolutions.
* Support empty commands in .sql DBX notebooks.
* Improve robustness in the StopIfDedent function.

Fixed

* Fix a parsing error in a backslash scenario with param and commas.
* Fix expression between parentheses symbol resolution issue.
* Fix parsing error with empty command in .sql DBX notebooks.
* Fix empty brackets symbol resolution issue.
* Fix Regex timeout error when collecting the SQL statements inventory.
* Fix parsing error related to mixed indentation.
* Fix false crash message when a parsing error was found.
* Fix an inconsistent number of SparkReferences between assessment and conversion modes.

## 2.8.0[¶](#id6 "Link to this heading")

2023-09-27

Added

* Add support for Snowpark API version 1.5.1 on Python.
* Add support for Python 3.10.10 syntax.
* Add CellId column in the inventories (for both notebooks, Databricks and Jupyter).
* Add four (4) new mappings

Changed

* Bump `Mobilize.Python` from 1.1.64 to 1.1.70
* Add support for Python 3.10.10 syntax.
* Add three (3) new backslash scenarios to solved a parsing error.
* Add an explicit return type to some Pandas symbols to avoid a loading error.

Fixed

* Fix a parsing error when a backslash in a square bracket, colon and param scenarios.
* Fix error loading Pandas symbols.

## 2.7.0[¶](#id7 "Link to this heading")

2023-09-20\

Added\

* Add support for Snowpark API version 1.5.0 on Python.
* 3 new mappings added

Changed\

* Avoid processing hidden files
* Bump `Mobilize.SparkCommon.Utils` from 1.3.188 to 1.3.189
* Bump `Mobilize.Common.Utils` from 3.2.0 to 3.2.2

Fixed\

* Fix PackageVersionInventory collection phase getting stuck.
* Fix incorrect percentage in Spark Usage Summary table in the detailed report when using DBC files.
* Fix File Sizing table in the detailed report shown empty or not shown at all.

## 2.6.0[¶](#id8 "Link to this heading")

2023-09-12\

Added\

* Add support of %SQL cells (from notebooks) to the SQL statements inventory.

Changed\

* Bump `Mobilize.Python` from 1.1.62 to 1.1.64
* Adds support to magic sql.
* Avoid updating function parameter type when inferred type is `None`.

Fixed\

* Fix issue causing infinite loading of symbols for specific files.
* Fix issue of GenericScanner files not being generated.

Security\

* Secure test passwords in Python transformation tests.

## 2.5.0[¶](#id9 "Link to this heading")

2023-09-05

Added

* Add Notebook Sizing inventory. (SCT-3876)
* Add Snowflake.SparkCommon.MappingLoader project (uses the new Snowflake.SnowMapGrammar). (SCT-4281)

Changed

* Bump Mobilize.Python from 1.1.59 to 1.1.62

  + Add a timeout mechanism at Python symbol resolution for GetSymbol methods.
* Bump Mobilize.SparkCommon.Utils from 1.3.186 to 1.3.187

  + Update Mobilize.SparkCommon.Utils.FilesHelper.CopyFilesRecursively method to handle hidden files.

Fixed

* Fix the issue of not receiving the email after a run (decreasing the log file size by avoiding logging Debug messages by default). (SCT-5320)

Removed

* Remove Mobilize.SparkCommon.TransformationCore project (used the old Mobilize.MapGrammar).

## 2.4.0[¶](#id10 "Link to this heading")

2023-08-28

Added

* Add NotebookCells inventory.
* Collect the argument values of DataFrameReader.option and DataFrameWriter.option for Scala and Python.
* Add 2 new mappings and a better alias type info collection
* Encrypt output files when additional parameters are provided.
* Re-enable SQLStatements inventory.
* Re-enable parallelization for Collectors.

Changed

* Update File Type Summary section of the detailed report (docx and html). (SCT-3867)
* Update for 2 mappings
* Bump Mobilize.SparkCommon.Utils from 1.3.181 to 1.3.186.
* Improve support of sorting CSV files.
* Bump Mobilize.Common.Utils from 3.1.6 to 3.2.0.

  + Improve support of sorting CSV files.
  + Bump Mobilize.Common.Utils from 3.1.6 to 3.2.0.
  + Update NuGet package versions.
* Refactor on Load Mappings Task.
* Refacto on SparkCommon Utils project references.
* Group solution projects.
* Merge Scala integration tests JupyterTest, InventoryTests and TransformationTest.

Fixed

* Fix issue that caused the Python conversion tool to get stuck when collecting the SQL statements inventory items.
* Fix missing GenericScanner files in the output.
* Fix issue of migrated DBC files that were not loading in Databricks.
* Fix error at the end of the tool process.

Removed

* Remove InventoryStorageTemp.
* Remove redundant StyleCop.Analyzers project references.

## 2.2.001[¶](#id11 "Link to this heading")

2023-07-19

Added

* Adding six (6) new mappings

Changed

* Assessment Model update from 3.1.10 to 3.1.11

Fixed

* Fix Databricks processing not working in Assessment mode

Security

* Added subresource integrity to HTML links

## 2.1.161[¶](#id12 "Link to this heading")

2023-07-06

Fixed

* Fixing and enabling Scala Spark functional tests

## 2.1.160[¶](#id13 "Link to this heading")

2023-07-05

Changed

* Assessment Model update from 3.1.9 to 3.1.10

## 2.1.159[¶](#id14 "Link to this heading")

2023-07-05

Changed

* Assessment Model update from 3.1.7 to 3.1.9

## 2.1.158[¶](#id15 "Link to this heading")

2023-07-05

Added

* Added tool stability by improving the handling of the exceptions in tasks

## 2.1.157[¶](#id16 "Link to this heading")

2023-07-05

Changed

* Spark Common update from 1.3.178 to 1.3.181

## 2.1.155[¶](#id17 "Link to this heading")

2023-07-05

Changed

* Common Build update from 2.0.2 to 3.0.4
* Improvements building the solution in MacOs

## 2.1.148[¶](#id18 "Link to this heading")

2023-07-04

Changed

* Spark Common update from 1.3.177 to 1.3.178
* Common Utils update from 4.0.0-alpha.DevOps.9 to 3.1.6

## 2.1.147[¶](#id19 "Link to this heading")

2023-07-03

Security

* Remove non-licensed package references in `Spark Common` projects.

## 2.1.146[¶](#id20 "Link to this heading")

2023-07-03

Changed

* Bump `coverlet.collector` from 3.2.0 to 6.0.0
* Bump `FluentAssertions` from 6.9.0 to 6.11.0
* Bump `Scriban.Signed` from 5.5.2 to 5.7.0
* Bump `DocumentFormat.OpenXml` from 2.19.0 to 2.20.0

Security

* Remove non-licensed package references in `SparkCommon` projects.

## 2.1.145[¶](#id21 "Link to this heading")

2023-06-28

Changed

* `Mobilize.Python` update from 1.1.49 to 1.1.50
* Fix Databricks notebook whole file parsing issue when not parsing single cell

## 2.1.144[¶](#id22 "Link to this heading")

2023-06-27

Fixed

* Fix .dbc file extraction on MacOS

## 2.1.143[¶](#id23 "Link to this heading")

2023-06-26

Fixed

* Fix tests errors because of different data formats.

## 2.1.142[¶](#id24 "Link to this heading")

2023-06-26

Changed

* Refactor inventory storage.

## 2.1.141[¶](#id25 "Link to this heading")

2023-06-23

Changed

* `Mobilize.Python` update from 1.1.46 to 1.1.49
* Detecting and stopping recursive cycles while resolving a symbol
* Fix StackOverflow exception involving \\_\\_init\\_\\_.py files
* Fix PyArgExpr node with backslash

## 2.1.140[¶](#id26 "Link to this heading")

2023-06-22

Changed

* `Mobilize.Python` update from 1.1.44 to 1.1.46
* Fix PyTerm node with backslash

## 2.1.138[¶](#id27 "Link to this heading")

2023-06-22

Changed

* Spark Common update from 1.3.176 to 1.3.177

Fixed

* Fix building Scala code processor.

## 2.1.137[¶](#id28 "Link to this heading")

2023-06-22

Security

* Secure credentials in functional tests.
* Remove non-licensed package references.

## 2.1.136[¶](#id29 "Link to this heading")

2023-06-21

Changed

* `Snowflake.Data` update from 2.0.15 to 2.0.25
* Spark Common update from 1.3.175 to 1.3.176

Security

Upgrading references in the functional tests.

## 2.1.135[¶](#id30 "Link to this heading")

2023-06-21

Added

* Add .dbc extension as supported by Python and Scala code processor tools.
* Add tests for the Contracts project.

Security

* Remove non-licensed package references in `SparkCommon.Contracts.Test`.

## 2.1.132[¶](#id31 "Link to this heading")

2023-06-21

Removed

* Remove the `Supported` column from IOFiles inventory in assessment mode.

## 2.1.131[¶](#id32 "Link to this heading")

2023-06-20

Fixed

* Fix tests on Mac.

## 2.1.130[¶](#id33 "Link to this heading")

2023-06-19

Changed

* Merge SparkCommon repo with this repo.

## 2.1.126[¶](#id34 "Link to this heading")

2023-06-16

Fixed

* Fix building the repo.

## 2.1.124[¶](#id35 "Link to this heading")

2023-06-15

Fixed

* Fix building the repo.

## 2.1.123[¶](#id36 "Link to this heading")

2023-06-15

Changed

* `Mobilize.Scala` update from 0.2.34 to 0.2.37
* Fix parsing error involving generic type with underscore and restriction
* Fix parsing error involving expressions with quote marks and interpolation

Security

* Remove of unsecure package references.

## 2.1.121[¶](#id37 "Link to this heading")

2023-06-15

Security

* Remove credential files.

## 2.1.120[¶](#id38 "Link to this heading")

2023-06-15

Changed

* Minor change in the version configuration for both Scala and Python.

## 1.0.306[¶](#id39 "Link to this heading")

February 14, 2023

Scala 0.2.13

SparkSnowConvert Core 1.1.27

\

New Features

* Jupyter notebooks (.ipynb) processing
* EWI generation when a dependency couldn’t be added to the project config file

Improvements

* Lambda scopes opening and closing

Bug Fixes

* Bug 680497: The remaning to full qualified for functions is not working fine
* Bug 681704: Unable to generate final report

\

## 1.0.273[¶](#id40 "Link to this heading")

February 2, 2023

Scala 0.2.4

SparkSnowConvert Core 1.1.8.0

Hotfix

* API endpoints update

## 1.0.263[¶](#id41 "Link to this heading")

January 31, 2023

Scala 0.2.4

SparkSnowConvert Core 1.1.8.0

Added

* .NET Core 6 Upgrade
* ElementPackage column added to imports inventory
* Sizing table added to assessment reports
* Add conversion percentage in the reports synced with BDS
* Add issues.csv file in the output
* Generate SummaryReport.html and DetailedReport.html (mirror docx html) locally on Reports folder
* Add ConversionStatus keywords to GenericScanner
* Support full name conversion

Improvements

* org.apache.spark.mllib mappings added to the core reference table
* [UI] Fix wording when cancelling the execution
* [UI] Change UI phase titles
* Group issues by EWI code
* Update TOOL\_VERSION column value format on Execution info table
* Simplified the Issue summary table so it is not too big

Bug Fixes

* Resolved Issue with backslash
* Resolved BreakLine Issue
* Resolved Lambda blocks corner case
* Remove AssessmentReport.html generation (local html report)

## 1.0.191[¶](#id42 "Link to this heading")

December 27, 2022

Scala 0.1.493

SparkSnowConvert Core 1.0.117.0

Added

* Uploading packages inventory to cloud telemetry

Improvements

* Detailed report

  + Minor visual improvements
  + Sorting issue table by:

    - Instances
    - Code
    - Description

## 1.0.166[¶](#id43 "Link to this heading")

December 21, 2022

Scala 0.1.492

SparkSnowConvert Core 1.0.105.0

Added

* Added a margin of error description in the detailed report

Improvements

* Improved sorting of issues table in the detailed report
* Improved display of percentages in the detailed report

Bug Fixes

* <#> character is showing issues
* Compose is not recognized as a keyword
* Parser is not working on ‘join’ argument
* Scala code processor throwing critical error

## 1.0.132[¶](#id44 "Link to this heading")

December 13, 2022

Scala 0.1.487

SparkSnowConvert Core 1.0.88

Improvements

* Customer information added to the detailed assessment report
* Transformation logging messages

Bug fixes

* An issue with expressions like (a, b) =>val c
* *compose* not being recognized as a keyword

## 1.0.107[¶](#id45 "Link to this heading")

December 7, 2022

Scala 0.1.484

SparkSnowConvert Core 1.0.77

Added

* Snowpark mappings update to 1.6.2 version
* Functions without parentheses collection improvements on assessment
* Maven project (pom.xml) file processing
* ClassName column renamed to ‘alias’ on SparkUsagesInventory.pam and ImportUsagesInventory.pam
* Added margin of error to the readiness score

Fixed

* Snowpark Python and Scala posted version update
* Issue with a new line after the name of functions

## 1.0.59[¶](#id46 "Link to this heading")

November 29, 2022

Scala 0.1.478

SparkSnowConvert Core 1.0.60

Added

* Basic companion object support
* org.apache.spark.sql.Column mappings update
* org.apache.spark.sql.Expression mappings update
* org.apache.spark.sql.functions mappings update
* Reference extensions dependency from project config file (SBT)
* Reference extensions dependency from project config file (Gradle)

Fixed

* “Script” code is not supported

## 1.0.17[¶](#id47 "Link to this heading")

November 23, 2022

Scala 0.1.472

SparkSnowConvert Core 1.0.44

Added

* Spark mappings update
* Trim “FileId” column value on all .pam files
* ConversionStatus and scala\_spark\_mappings\_core.csv unification

## 1.0.1[¶](#id48 "Link to this heading")

November 17, 2022

Scala 0.1.472

SparkSnowConvert Core 1.0.37

Added

* SparkSession, DataFrameReader, and DataFrameWriter mappings update
* EWI Generation for unary and binary expressions

Fixed

* Writer replacer supports csv, parquet, json, and options
* Reader replacer is not supporting functions without parentheses
* Writer replacer is not supporting functions without parentheses
* Currently, the transformation of InsertInto is not a valid code.
* Writer replacer is not including all functions.

## 0.1.873[¶](#id49 "Link to this heading")

November 11, 2022

Scala 0.1.468

SparkSnowConvert Core 1.0.23

Added:

* Symbol resolution for function calls without parentheses
* Scopes opening/closing exceptions handling(at Replacers)
* EWI generation for not supported imports (complex cases)
* EWI generation for not defined imports
* SparkSession transformation improvements
* DataFrame reader/writer transformation improvements
* “Spark Usages by Support Category”, “Scala Import Call Summary” sections added to Detailed report
* RDD mappings update

Fixed:

* Stack Overflow, output files were not generated
* Expression without parentheses on Spark Session replacer transformation

## 0.1.770[¶](#id50 "Link to this heading")

October 21, 2022

Scala 0.1.458

SparkSnowConvert Core 0.1.530

Added:

* Updated helper/extension .jar to latest version
* Updated assessment .docx report template
* Import usages inventory generation
* Generating EWIs for not supported imports (simple case)

Fixed:

* Indeterminism issue on SymblTable
* Error when sorting spark usages inventory files
* SclSingleExprPath must not contain null members
* The collection was modified; the enumeration operation may not execute
* Parsing does not finish when there are multiple closing multi-line in a row
* Issue with expression
* Error FileNotGenerated

## 0.1.705[¶](#id51 "Link to this heading")

October 04, 2022

Scala 0.1.442

SparkSnowConvert Core 0.1.499

Fixed:

* The setting button is not refreshing when the license is changed.

## 0.1.702[¶](#id52 "Link to this heading")

September 28, 2022

Scala 0.1.442

SparkSnowConvert Core 0.1.498

Added:

* Symbol table built ins loading improvements
* Adding robustness to symbol table loaders

Fixed:

* Error in the total of Scala files in the AssessmentReport
* Symbol resolving for generic functions using an asterisk
* Comments inside comments and id prefix and interpolation parsing error
* The comma after identifier parsing error
* Parsing error of the expression when the first statement is taking the pattern of the second statement
* “and”, “::”,”++” and “or” operators parsing errors

## 0.1.687[¶](#id53 "Link to this heading")

September 20, 2022

Scala 0.1.430

SparkSnowConvert Core 0.1.491.0

Added

* Symbol loading/resolving - Add support for generic methods with asterisk params**.**
* Symbol loading/resolving - Add type inference for type defs.
* Symbol loading/resolving general improvements

Fixed

Issue related to the import usages not being stored if there are no Spark references.

## 0.1.677[¶](#id54 "Link to this heading")

September 15, 2022

Scala 0.1.427

SparkSnowConvert Core 0.1.486.0

Added

* Cloud telemetry and sending email mechanism now available in Conversion Mode
* Update contact information in the email template

## 0.1.653[¶](#id55 "Link to this heading")

September 06, 2022

Scala 0.1.426

SparkSnowConvert Core 0.1.476.0

Added

* ‘SnowConvert Version’ and ‘Snowpark version’ columns to SparkUsagesInventory
* Improvements to speed analysis

## 0.1.624[¶](#id56 "Link to this heading")

August 31st, 2022

Scala 0.1.422

SparkSnowConvert Core 0.1.454.0

Added

* Automated and Status columns added to SparkReferenceInventory.csv
* Summary and detailed html report uploading to Snowflake
* Mappings update

Fixed:

* Summary and detailed report wordings fixes
* Email template wording fixes.

## 0.1.579[¶](#id57 "Link to this heading")

August 23th, 2022

Scala 0.1.421 Spark

SnowConvert Core 0.1.414

Added

* Email template update
* Adding “Version information” section to Summary report
* Adding “Resources” section to Detailed report
* Final screen UI changes

Fixed

* Report missing spark functions on sparkUsagesInventory.pam
* Detailed report logos update
* Percentage values precision on summary and detailed assessment reports

## 0.1.595[¶](#id58 "Link to this heading")

August 17th, 2022

Scala 0.1.421

SparkSnowConvert Core 0.1.396

Added

* Spark read and write transformations improvement
* Session id column to spark usages inventory

## 0.1.479[¶](#id59 "Link to this heading")

June 30th, 2022

Scala 0.1.411

SparkSnowConvert Core 0.1.279

Added

* Spark read and write transformations
* Spark trim, rtrim and ltrim function transformations
* String interpolation parsing
* Increasing sql extraction match patterns

## 0.1.447[¶](#id60 "Link to this heading")

June 14th, 2022

Scala 0.1.402

SparkSnowConvert Core 0.1.274

Added

* File operations robustness
* Output folders reorganization
* SparkSession builder transformation
* Adding “Scala files with embedded sql” count in assessment reports

Fixed

* Cyclic dependencies issue on Symbol Table
* Empty case clause parsing
* Multiple statements on lambda block parsing
* Case clause pattern parsing

## 0.1.380[¶](#id61 "Link to this heading")

June 1st, 2022

Scala 0.1.391

SparkSnowConvert Core 0.1.229

Added

* Parsing robustness
* .sbt configuration files processing
* Issues breakdown section added in assessment html report
* Look and feel improvements in assessment html report
* Using RapidScanner inventories to calculate the spark usages assessment
* macOS CLI & UI support
* Improvements in import statements mappings

## 0.1.7[¶](#id62 "Link to this heading")

May 17th, 2022

Scala 0.1.380

Added

* Scala Parser

  + Double exclamation mark support
* Conversion tool

  + Sql extraction
  + object\_struct function transformation
  + avg function transformation
  + Snowpark extensions .jar update
  + Lines of code report
  + Import mappings
  + Docx and html assessment reports
  + RapidScan integration
  + Linux OS support

**Fixed**

* Binary expressions special cases parsing

## 0.1.3[¶](#id63 "Link to this heading")

March 18th, 2022

Scala 0.1.358

Added

* Scala Parser

  + Support underscore followed by newline when parsing expressions
  + Improve parsing errors handling
* Symbols

  + Improve support of Unresolved Symbols
  + Improve creation of Generic Symbols to reuse existing ones
  + Support Loading and Resolution of Lambda Expressions
* Mappings:

  + Support custom mappings for functions and types via .map files
  + Added custom map directory parameter

**Fixed**

* Fill missing columns at notification .pam file.
* Generate metrics data files (.pam) to specified reports folder

## 0.1.2[¶](#id64 "Link to this heading")

March 4th, 2022

Scala 0.1.351

Added

* Updated logos and text in UI and Documentation
* Symbols

  + Support Generic Identifiers on Type Parameters for Generic Symbol
  + Exclusion of not required dependencies
* ScalaParser:

  + Backticks idents
  + ArgAssign expressions

Fixed

* ScalaParser:

  + ExprLambda with ColonType next to ident
  + Try expression when try is not referring a keyword
  + Empty lambda expr with args
  + Underscore (“\_”) in TypeArgs
  + Files with all commented out source
  + New lines at SimpleExpr, SingleExpr, TailExpr nodes
* ConversionTool:

  + Fix Crash of conversion due to javap parsing errors (related with jar dependencies)

## 0.1.1[¶](#id65 "Link to this heading")

February 14th, 2022

Scala 0.1.333

Features

* Command line interface.
* Scala code assessment feature.
* Consume multiple files or single files with multiple objects.
* Conversion of basic Scala programs as defined by functions and syntax to be mutually agreed during the first 3 development sprints.
* Comments in Scala code are re-inserted inline.
* Insert comments in-line with any errors/warning/reviews.
* Basic reporting including

  + Number of spark elements processed
  + Summary of elements transformed, files and locations of
  + Summary of errors/warnings/reviews encountered.
  + Summary of unsupported Spark APIs
* Demonstrated inclusion of the following defined scenarios:

  + API mappings
  + Recreate project as SnowPark projects

    - Setup Proper project structure
    - Update to SnowPark supported Scala version
  + Helper Creation to reduce impedance mismatch
  + Define some pattern rewrite
  + Document guidelines for non-automatable concepts (e.g.: file usage patterns, data source configuration, or spark libraries without a direct equivalent, like Kafka stream reading)
* Greater than 90% successful conversion rate for initial two customer code bases (basis code for the above scenarios) to be provided to Mobilize by Snowflake on the Effective Date.

  + Measured based upon number of compilable objects in Snowflake
  + Objects with unsupported/untranslatable functions not counted
  + Conversion rate for code will be based upon a complete code base containing all dependent objects.
  + Snowflake will provide access to all available private preview features for Mobilize development benefit

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

1. [2.14.0](#id1)
2. [2.13.0](#id2)
3. [2.12.0](#id3)
4. [2.11.0](#id4)
5. [2.09.0](#id5)
6. [2.8.0](#id6)
7. [2.7.0](#id7)
8. [2.6.0](#id8)
9. [2.5.0](#id9)
10. [2.4.0](#id10)
11. [2.2.001](#id11)
12. [2.1.161](#id12)
13. [2.1.160](#id13)
14. [2.1.159](#id14)
15. [2.1.158](#id15)
16. [2.1.157](#id16)
17. [2.1.155](#id17)
18. [2.1.148](#id18)
19. [2.1.147](#id19)
20. [2.1.146](#id20)
21. [2.1.145](#id21)
22. [2.1.144](#id22)
23. [2.1.143](#id23)
24. [2.1.142](#id24)
25. [2.1.141](#id25)
26. [2.1.140](#id26)
27. [2.1.138](#id27)
28. [2.1.137](#id28)
29. [2.1.136](#id29)
30. [2.1.135](#id30)
31. [2.1.132](#id31)
32. [2.1.131](#id32)
33. [2.1.130](#id33)
34. [2.1.126](#id34)
35. [2.1.124](#id35)
36. [2.1.123](#id36)
37. [2.1.121](#id37)
38. [2.1.120](#id38)
39. [1.0.306](#id39)
40. [1.0.273](#id40)
41. [1.0.263](#id41)
42. [1.0.191](#id42)
43. [1.0.166](#id43)
44. [1.0.132](#id44)
45. [1.0.107](#id45)
46. [1.0.59](#id46)
47. [1.0.17](#id47)
48. [1.0.1](#id48)
49. [0.1.873](#id49)
50. [0.1.770](#id50)
51. [0.1.705](#id51)
52. [0.1.702](#id52)
53. [0.1.687](#id53)
54. [0.1.677](#id54)
55. [0.1.653](#id55)
56. [0.1.624](#id56)
57. [0.1.579](#id57)
58. [0.1.595](#id58)
59. [0.1.479](#id59)
60. [0.1.447](#id60)
61. [0.1.380](#id61)
62. [0.1.7](#id62)
63. [0.1.3](#id63)
64. [0.1.2](#id64)
65. [0.1.1](#id65)