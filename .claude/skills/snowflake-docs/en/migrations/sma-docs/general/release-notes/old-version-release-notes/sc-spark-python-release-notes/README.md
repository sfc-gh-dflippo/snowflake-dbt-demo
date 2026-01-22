---
auto_generated: true
description: 2023-10-24 Added Add condensed ID for filenames and use it in the log.
last_scraped: '2026-01-14T16:51:19.324094+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/sma-docs/general/release-notes/old-version-release-notes/sc-spark-python-release-notes/README
title: 'Snowpark Migration Accelerator:  SC Spark Python Release Notes | Snowflake
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

              * [SC Spark Scala release notes](../sc-spark-scala-release-notes/README.md)
              * [SC Spark Python release notes](README.md)

                + [Known issues](known-issues.md)
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

[Guides](../../../../../../guides/README.md)[Migrations](../../../../../README.md)Tools[Snowpark Migration Accelerator](../../../../README.md)General[Release notes](../../README.md)[Old version release notes](../README.md)SC Spark Python release notes

# Snowpark Migration Accelerator: SC Spark Python Release Notes[¶](#snowpark-migration-accelerator-sc-spark-python-release-notes "Link to this heading")

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

## [¶](#id2 "Link to this heading")

## 2.13.0[¶](#id3 "Link to this heading")

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

## 2.12.0[¶](#id4 "Link to this heading")

2023-10-13

Added

* Add Trial Mode support.

Changed

* Bump `Snowflake.SnowConvert.Python` from 1.1.79 to 1.1.80
* Add a variant of ResolveType to avoid stack overflow at some scenarios.

Fixed

* Fix scenario when resolving a FullName causes stack overflow.

## 2.11.0[¶](#id5 "Link to this heading")

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

## 2.09.0[¶](#id6 "Link to this heading")

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

## 2.8.0[¶](#id7 "Link to this heading")

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

## 2.7.0[¶](#id8 "Link to this heading")

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

## 2.6.0[¶](#id9 "Link to this heading")

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

## [¶](#id10 "Link to this heading")

## 2.5.0[¶](#id11 "Link to this heading")

2023-09-05

Added

* Add Notebook Sizing inventory.
* Add Snowflake.SparkCommon.MappingLoader project (uses the new Snowflake.SnowMapGrammar).

Changed

* Bump Mobilize.Python from 1.1.59 to 1.1.62

  + Add a timeout mechanism at Python symbol resolution for GetSymbol methods.
* Bump Mobilize.SparkCommon.Utils from 1.3.186 to 1.3.187

  + Update Mobilize.SparkCommon.Utils.FilesHelper.CopyFilesRecursively method to handle hidden files.

Fixed

* Fix the issue of not receiving the email after a run (decreasing the log file size by avoiding logging Debug messages by default).

Removed

* Remove Mobilize.SparkCommon.TransformationCore project (used the old Mobilize.MapGrammar).

## 2.4.0[¶](#id12 "Link to this heading")

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

\

## 2.2.001[¶](#id13 "Link to this heading")

2023-07-19

Added

* Adding six (6) new mappings

Changed

* Assessment Model update from 3.1.10 to 3.1.11

Fixed

* Fix Databricks processing not working in Assessment mode

Security

* Added subresource integrity to HTML links

## 2.1.161[¶](#id14 "Link to this heading")

2023-07-06

Fixed

* Fixing and enabling Scala Spark functional tests

## 2.1.160[¶](#id15 "Link to this heading")

2023-07-05

Changed

* Assessment Model update from 3.1.9 to 3.1.10

## 2.1.159[¶](#id16 "Link to this heading")

2023-07-05

Changed

* Assessment Model update from 3.1.7 to 3.1.9

## 2.1.158[¶](#id17 "Link to this heading")

2023-07-05

Added

* Added tool stability by improving the handling of the exceptions in tasks

## 2.1.157[¶](#id18 "Link to this heading")

2023-07-05

Changed

* Spark Common update from 1.3.178 to 1.3.181

## 2.1.155[¶](#id19 "Link to this heading")

2023-07-05

Changed

* Common Build update from 2.0.2 to 3.0.4
* Improvements building the solution in MacOs

## 2.1.148[¶](#id20 "Link to this heading")

2023-07-04

Changed

* Spark Common update from 1.3.177 to 1.3.178
* Common Utils update from 4.0.0-alpha.DevOps.9 to 3.1.6

## 2.1.147[¶](#id21 "Link to this heading")

2023-07-03

Security

* Remove non-licensed package references in `Spark Common` projects.

## 2.1.146[¶](#id22 "Link to this heading")

2023-07-03

Changed

* Bump `coverlet.collector` from 3.2.0 to 6.0.0
* Bump `FluentAssertions` from 6.9.0 to 6.11.0
* Bump `Scriban.Signed` from 5.5.2 to 5.7.0
* Bump `DocumentFormat.OpenXml` from 2.19.0 to 2.20.0

Security

* Remove non-licensed package references in `SparkCommon` projects.

## 2.1.145[¶](#id23 "Link to this heading")

2023-06-28

Changed

* `Mobilize.Python` update from 1.1.49 to 1.1.50
* Fix Databricks notebook whole file parsing issue when not parsing single cell

## 2.1.144[¶](#id24 "Link to this heading")

2023-06-27

Fixed

* Fix .dbc file extraction on MacOS

## 2.1.143[¶](#id25 "Link to this heading")

2023-06-26

Fixed

* Fix tests errors because of different data formats.

## 2.1.142[¶](#id26 "Link to this heading")

2023-06-26

Changed

* Refactor inventory storage.

## 2.1.141[¶](#id27 "Link to this heading")

2023-06-23

Changed

* `Mobilize.Python` update from 1.1.46 to 1.1.49
* Detecting and stopping recursive cycles while resolving a symbol
* Fix StackOverflow exception involving \\_\\_init\\_\\_.py files
* Fix PyArgExpr node with backslash

## 2.1.140[¶](#id28 "Link to this heading")

2023-06-22

Changed

* `Mobilize.Python` update from 1.1.44 to 1.1.46
* Fix PyTerm node with backslash

## 2.1.138[¶](#id29 "Link to this heading")

2023-06-22

Changed

* Spark Common update from 1.3.176 to 1.3.177

Fixed

* Fix building Scala code processor.

## 2.1.137[¶](#id30 "Link to this heading")

2023-06-22

Security

* Secure credentials in functional tests.
* Remove non-licensed package references.

## 2.1.136[¶](#id31 "Link to this heading")

2023-06-21

Changed

* `Snowflake.Data` update from 2.0.15 to 2.0.25
* Spark Common update from 1.3.175 to 1.3.176

Security

Upgrading references in the functional tests.

## 2.1.135[¶](#id32 "Link to this heading")

2023-06-21

Added

* Add .dbc extension as supported by Python and Scala code processor tools.
* Add tests for the Contracts project.

Security

* Remove non-licensed package references in `SparkCommon.Contracts.Test`.

## 2.1.132[¶](#id33 "Link to this heading")

2023-06-21

Removed

* Remove the `Supported` column from IOFiles inventory in assessment mode.

## 2.1.131[¶](#id34 "Link to this heading")

2023-06-20

Fixed

* Fix tests on Mac.

## 2.1.130[¶](#id35 "Link to this heading")

2023-06-19

Changed

* Merge SparkCommon repo with this repo.

## 2.1.126[¶](#id36 "Link to this heading")

2023-06-16

Fixed

* Fix building the repo.

## 2.1.124[¶](#id37 "Link to this heading")

2023-06-15

Fixed

* Fix building the repo.

## 2.1.123[¶](#id38 "Link to this heading")

2023-06-15

Changed

* `Mobilize.Scala` update from 0.2.34 to 0.2.37
* Fix parsing error involving generic type with underscore and restriction
* Fix parsing error involving expressions with quote marks and interpolation

Security

* Remove of unsecure package references.

## 2.1.121[¶](#id39 "Link to this heading")

2023-06-15

Security

* Remove credential files.

## 2.1.120[¶](#id40 "Link to this heading")

2023-06-15

Changed

* Minor change in the version configuration for both Scala and Python.

## 1.0.877[¶](#id41 "Link to this heading")

April 26th, 2023

Python 1.1.25

PythonSnowConvert Core 2.01.090

SparkCommon 1.3.151

Added

* Added support for Snowpark 1.3.0

  + Four new mappings
  + EWI [SPRKPY1048](../../../../issue-analysis/issue-codes-by-source/python/README) was deprecated
* Added transformations for

  + DataFrameReader chain
  + SparkSession.sparkContext
* Added Severity column to the Issues Summary table of the detailed report

Improvements

* Improved name of the Spark usages inventory file
* Improved readiness score displayed value when no Spark references were found

Fixed

* Fixed button URLs
* Fixed inconsistencies of the Spark usages inventory locally and in telemetry
* Fixed RDD metrics in the Spark Usage Summary table of the detailed report
* Fixed inconsistencies with zero and dash symbols in the reports

## 1.0.826[¶](#id42 "Link to this heading")

March 29th, 2023

Python 1.1.25

PythonSnowConvert Core 2.01.068

SparkCommon 1.3.131

Added

* Added support for convert DBC files

  Improvements
* Added transformation for DataFrameReader.format and DataFrameReader.load

Fixed

* Fixed SnowConvert/Snowpark version values transposed

## 1.0.725[¶](#id43 "Link to this heading")

February 15th, 2023

Python 1.1.11

PythonSnowConvert Core 2.01.022

SparkCommon 1.3.113

Added

* Added support for Databricks archive files (.dbc extension)
* Added support for Databricks notebook files (.python extension)
* Added parallelism to the Spark usages identification process
* Added support for SnowPark API version 1.1.0
* Added mapping elements:
* twelve direct mappings
* two conversions using helper

Improvements

* Improved SPRKPY1038 EWI message
* Improved registration of EWIs in conversion for columns using attribute access
* Improved local report names

## 1.0.691[¶](#id44 "Link to this heading")

February 1st, 2023

Python 1.1.3

PythonSnowConvert Core 2.1.4

SparkCommon 1.3.105

Added

* Added Net6 compatibility (internal)
* Added issues.csv report
* Added sizing table to the detailed report
* Added support for global variable declaration
* Added support for inherited symbol identification
* Added support for accessing columns using attribute access
* Added in telemetry the version of the mapping that was used
* Added support for Jupyter Notebooks in GenericScanner
* Added mapping elements:

  + one direct mapping
  + one conversion using helper
  + six workarounds
  + five not supported identification

Improvements

* Improved tool version format in reports, inventories and telemetry
* Improved syncing of local and remote HTML reports
* Improved HTML detailed report sync with DOCX detailed report
* Improved issues table grouping by EWI code
* Improved import table grouping by package
* Improved commented output code
* Improved UI progress phase titles

Bug Fixes

* Fixed location of EWI messages for complex statements
* Fixed UI wording when cancelling the execution
* Fixed typos on reports

## 1.0.594[¶](#id45 "Link to this heading")

December 28th, 2022

Python 1.0.457

PythonSnowConvert Core 2.0.280

Added

* Added support for Jupyter Notebooks in Generic Scanner
* Added conversion percentage in the reports
* Added ‘ElementPackage’ column to the import usages inventory
* Added one direct mapping
* Added four helpers
* Added two workarounds
* Added minor visual improvements to the detailed report

Improvements

* Improved one mapping from rename to direct
* Improved sorting of issues table in the detailed report

Bugs

* Fixed columns size of the issue table in the detailed report
* Fixed an error when adding EWI comment for Column.contains function usage
* Fixed six mapping statuses that didn’t match in the Spark usages inventory

## 1.0.555[¶](#id46 "Link to this heading")

December 21st, 2022

Python 1.0.457

PythonSnowConvert Core 2.0.259

New Features

* Added three new workarounds
* Added margin of error in the Detailed Report description

Improvements

* Improved two mapping from rename to direct
* Improved sorting of issues table in the detailed report
* Improved displaying of percentages in the detailed report
* Conversion stage logging messages improved

Bugs

* Fixed two mappings
* Fixed identification of a not supported element

## 1.0.515[¶](#id47 "Link to this heading")

December 14th, 2022

Python 1.0.457

PythonSnowConvert Core 2.0.241

New Features

* Support for ‘snowpark\_extensions’
* Twelve conversions using the ‘snowpark\_extensions’
* Two workarounds added
* A new spark reference added to the table reference database, including its status.
* Customer info added to the detailed report

Improvements

* EWI SPRKPY1038 wording improvement
* A spark reference status improved from *rename* to *direct*

Bug Fixes

* A bug in a mapping fixed
* A broken Spark Core Mapping table fixed

## 1.0.492[¶](#id48 "Link to this heading")

December 07th, 2022

Python 1.0.455

PythonSnowConvert Core 2.0.233

New Features

* Addd margin of error in the readiness score
* Added two new mappings
* Added EWI for PySpark elements that were not recognized

Improvements

* Improved appendix A wording in the detailed report
* Improved EWI message for PySpark elements that are not defined in the tool’s conversion database

Bug Fixes

* Fixed ‘alias’ column name in the inventory

## 1.0.457[¶](#id49 "Link to this heading")

December 01st, 2022

Python 1.0.452

Python SnowConvert Core 2.0.217

New Features

* Added support to SnowPark API version 1.0.0
* Added five new workarounds documentation
* Added execution info to telemetry
* Added margin of error to the readiness score

Improvements

* Improved accuracy in code symbols identification
* Improvement in the assessment step when logging messages.

## 1.0.441[¶](#id50 "Link to this heading")

November 23rd, 2022

Python 1.0.449

PythonSnowConvert Core 2.0.210

New Features

* Added EWI comments to the output code for not defined PySpark elements
* Added support for inherited symbols
* Three new mappings added
* One workaround added

Improvements

* Improved readiness score when all the files have errors
* Improved error message when loading the symbol table
* Improved handling of generic types
* One mapping status changed from rename to direct
* One conversion status changed from workaround to direct mapping

Bug Fixes

* Fixed markdown conversion issue
* Fixed syncing issues between PySpark\_Mappings\_Core table and the tool

## 1.0.425[¶](#id51 "Link to this heading")

November 17th, 2022

Python 1.0.445

PythonSnowConvert Core 2.0.203

Improvements

* Robustness at the loading symbol table

Bug Fixes

* Fixed detailed report summary table for spark usage values
* Fixed some parsing errors
* Fixed EWI code sync issues between the tool and PySpark\_Mappings\_Core Snowflake DB table and

## 1.0.415[¶](#id52 "Link to this heading")

November 15th, 2022

Python 1.0.441

PythonSnowConvert Core 2.0.199

New Features

* Added EWI record when an error is detected at loading the symbol table

Bug fixes

* Fixed new lines issue when converting Jupyter notebook files

## 1.0.404[¶](#id53 "Link to this heading")

November 11th, 2022

Python 1.0.436

PythonSnowConvert Core 2.0.195

New Features

* Added basic support to convert Jupyter notebook files
* Added a value for tracking import usages as an inventory
* Improve the detailed report (Spark usages grouped by support category and Python Import Call Summary)
* New mappings added
* New workarounds added for ‘SparkSession.Builder.appName’
* New EWIs added as comments in the output code
* Added support to copy non-Python files to the output directory
* Added PySpark usages identification for id expressions
* Added an error message when symbol table loading fails

Improvements

* Improved imports mapping
* Improved type hints mapping
* Improved rename mappings to direct mappings

Bug Fixes

* Parsing errors
* The output directory structure for files with parsing errors
* Fixed ‘pyspark.streaming’ full names
* Fixed CLI crashing

## 1.0.315[¶](#id54 "Link to this heading")

October 21st, 2022

Python 1.0.422

PythonSnowConvert Core 2.0.152

Added

* Added type inference
* 5 New mappings supported

Improvements

* Detailed report
* Import Statement conversion
* Transformation documentation

Fixed

* EWIs related to a Project ID logging
* 4 Pyspark elements conversion status

## 1.0.280[¶](#id55 "Link to this heading")

October 12th, 2022

Python 1.0.417

PythonSnowConvert Core 2.0.135

Added

* New transformations
* Handling unsupported Pyspark elements used in imports
* Improvements in logging message

## 1.0.271[¶](#id56 "Link to this heading")

October 05th, 2022

Python 1.0.417

PythonSnowConvert Core 2.0.132

Added

* Robustness to symbol identification
* Improving in type resolution

Fixed

* Settings button is not refreshing with license change
* Documentation link in Python version reference

## 1.0.247[¶](#id57 "Link to this heading")

September 27th, 2022

Python 1.0.410

PythonSnowConvert Core 2.0.126

Added

* Robustness when parsing Jupypter Notebook files
* Improvements in resolving symbols with Generics
* New transformations

Fixed

* Total Python files in the report

## 1.0.220[¶](#id58 "Link to this heading")

September 15th, 2022

Python 1.0.399

PythonSnowConvert Core 2.0.112

Added

* New support for imports
* Alias name in inventories for the imports

Fixed

* Wrong line number in the inventory for macOS files
* Identified usages table percentages in the html report
* Qualification tool showing zero PySpark references
* Update contact information in the email template

## 1.0.190[¶](#id59 "Link to this heading")

September 06th, 2022

Python 1.0.392

PythonSnowConvert Core 2.0.100  
\

Added

* ‘SnowConvert Version’ and ‘Snowpark version’ columns to SparkUsagesInventory
* More functions from pyspark supported
* Improvements to speed analysis

Fixed

* Direct mapping updating

## 1.0.148[¶](#id60 "Link to this heading")

August 31st, 2022

Python 1.0.381

PythonSnowConvert Core 2.0.71

Added

* 10 new mappings supported
* 17 new workaround conversions detected
* Support for identification of PySpark usages in Jupyter notebook files
* Automated and Status columns added to SparkReferenceInventory.csv
* Summary and detailed html report uploading to snowflake

Fixed

* Summary and detailed report wordings fixes
* Email template wording fixes

## 1.0.107[¶](#id61 "Link to this heading")

August 24th, 2022

Python 1.0.380

**PythonSnowConvert Core 2.0.30**

Added

* 30 new mappings supported
* Identification of pyspark.streaming and pyspark.rdd packages
* Improvements in identifying imported symbols
* Email template update
* Adding “Version information” section to Summary Report
* Adding “Resources” section to Detailed Report
* Final screen UI changes
* Sort SparkReferenceInventory report file

Fixed

* Settings button removed
* Detailed report logos update
* Percentage values precision on summary and detailed assessment reports

## 1.0.66[¶](#id62 "Link to this heading")

August 17th, 2022

Python 1.0.377

PythonSnowConvert Core 1.0.61

Added

* 136 new mappings supported
* Supported status updated for all functions listed as “Corrected” in the shared spreadsheet
* Information collected from the requirements.txt file
* Improvements in identifying chained symbols

Fixed

* Line number in SparkReferenceInventory report

## 1.0.30[¶](#id63 "Link to this heading")

August 9th, 2022

Python 1.0.373

PythonSnowConvert Core 1.0.29

Added

* Collect all the import usages
* Improvements identifying PySpark usages (import without module, import with star)
* Identifying more DataFrame functions as supported

Fixed

Logging parsing errors

## 0.1.172[¶](#id64 "Link to this heading")

July 20th, 2022

Python 0.1.172

Added

* Command line interface.
* Python code Qualification tool feature.

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
3. [2.13.0](#id3)
4. [2.12.0](#id4)
5. [2.11.0](#id5)
6. [2.09.0](#id6)
7. [2.8.0](#id7)
8. [2.7.0](#id8)
9. [2.6.0](#id9)
11. [2.5.0](#id11)
12. [2.4.0](#id12)
13. [2.2.001](#id13)
14. [2.1.161](#id14)
15. [2.1.160](#id15)
16. [2.1.159](#id16)
17. [2.1.158](#id17)
18. [2.1.157](#id18)
19. [2.1.155](#id19)
20. [2.1.148](#id20)
21. [2.1.147](#id21)
22. [2.1.146](#id22)
23. [2.1.145](#id23)
24. [2.1.144](#id24)
25. [2.1.143](#id25)
26. [2.1.142](#id26)
27. [2.1.141](#id27)
28. [2.1.140](#id28)
29. [2.1.138](#id29)
30. [2.1.137](#id30)
31. [2.1.136](#id31)
32. [2.1.135](#id32)
33. [2.1.132](#id33)
34. [2.1.131](#id34)
35. [2.1.130](#id35)
36. [2.1.126](#id36)
37. [2.1.124](#id37)
38. [2.1.123](#id38)
39. [2.1.121](#id39)
40. [2.1.120](#id40)
41. [1.0.877](#id41)
42. [1.0.826](#id42)
43. [1.0.725](#id43)
44. [1.0.691](#id44)
45. [1.0.594](#id45)
46. [1.0.555](#id46)
47. [1.0.515](#id47)
48. [1.0.492](#id48)
49. [1.0.457](#id49)
50. [1.0.441](#id50)
51. [1.0.425](#id51)
52. [1.0.415](#id52)
53. [1.0.404](#id53)
54. [1.0.315](#id54)
55. [1.0.280](#id55)
56. [1.0.271](#id56)
57. [1.0.247](#id57)
58. [1.0.220](#id58)
59. [1.0.190](#id59)
60. [1.0.148](#id60)
61. [1.0.107](#id61)
62. [1.0.66](#id62)
63. [1.0.30](#id63)
64. [0.1.172](#id64)