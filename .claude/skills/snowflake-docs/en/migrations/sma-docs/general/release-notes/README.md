---
auto_generated: true
description: Note that the release notes below are organized by release date. Version
  numbers for both the application and the conversion core will appear below.
last_scraped: '2026-01-14T16:51:07.734160+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/sma-docs/general/release-notes/README
title: 'Snowpark Migration Accelerator: Release Notes | Snowflake Documentation'
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

          + [Introduction](../introduction.md)
          + [Getting started](../getting-started/README.md)
          + [Conversion software terms of use](../conversion-software-terms-of-use/README.md)
          + [Release notes](README.md)

            - [Old version release notes](old-version-release-notes/README.md)
          + [Roadmap](../roadmap.md)
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[Snowpark Migration Accelerator](../../README.md)GeneralRelease notes

# Snowpark Migration Accelerator: Release Notes[¶](#snowpark-migration-accelerator-release-notes "Link to this heading")

Note that the release notes below are organized by release date. Version numbers for both the application and the conversion core will appear below.

## Version 2.11.0 (January 9, 2026)[¶](#version-2-11-0-january-9-2026 "Link to this heading")

### Application & CLI Version: 2.11.0[¶](#application-cli-version-2-11-0 "Link to this heading")

#### Included SMA Core Version[¶](#included-sma-core-version "Link to this heading")

* Snowpark Conversion Core: 8.1.43

#### Included SnowConvert AI Version[¶](#included-snowconvert-ai-version "Link to this heading")

* SnowConvert AI Version 2.2.0 ([Release Notes](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/release-notes/release-notes/README#version-2-2-0-jan-07-2026))

### Engine Release Notes[¶](#engine-release-notes "Link to this heading")

#### Added[¶](#added "Link to this heading")

* **Enhanced Notebook Setup for Assessment:** When running an assessment on Databricks notebooks, a Snowpark Connect session is now automatically added to the first cell to simplify your setup.
* **Automatic Snowpark Connect Conversion:** The tool now automatically converts both `SparkSession` and `SparkContext` initializations in Python code to their equivalent Snowpark Connect sessions.
* **Improved Error Identification:**

  + Added a new warning code, `SPRKCNTPY4000`, to clearly flag any `SparkContext` elements that are not yet supported by Snowpark Connect.
  + The tool now automatically detects and flags unsupported Databricks utility calls (`dbutils` API) with the new warning code `SPRKDBX1004` during conversion.
* **More Detailed Reporting:**

  + The SparkUsagesInventory.csv report now includes a new column called `IS_SNOWPARK_CONNECT_TOOL_SUPPORTED`
  + This new column is to clearly indicate if a Spark element is supported directly by Snowpark Connect, or supported throught an SMA transformation.
  + The Snowpark Connect readiness score calculation has been updated to use the new `IS_SNOWPARK_CONNECT_TOOL_SUPPORTED` column in the SparkUsagesInventory.csv report.
* **Next-Generation Notebook Support:** Enhanced support for the VNext Snowflake Notebooks format when converting Databricks or Jupyter notebooks.

  + **Full VNext Compatibility:** The SMA can now generate output files that fully adhere to the VNext Snowflake Notebooks standard, regardless of whether the source was a Databricks or a previous-generation Jupyter notebook.
  + **Smarter Language Handling:** The conversion engine has been updated with enhanced logic to accurately detect and manage the specific language (such as Python or Scala) within each individual notebook cell. This allows for more precise and reliable cell-by-cell conversion.
  + **Enhanced Metadata for Cells:** The process now correctly incorporates necessary language and type metadata at the cell level during generation, which is essential for VNext Notebooks to function as expected.

#### Changed[¶](#changed "Link to this heading")

* **Simplified Python Code:** For Snowpark Connect, unnecessary `.sparkContext` references in Python method calls are now removed to streamline your code.
* **Clearer Warning Codes:** Snowpark Connect warning codes are now renamed to include language-specific prefixes (e.g., `SPRKCNTPY` for Python, `SPRKCNTSCL` for Scala) for easier error identification.
* **More Accurate Notebook Conversions:** The conversion process for notebooks has been improved to correctly distinguish between Databricks and Jupyter formats, preventing incorrect modifications.

#### Fixed[¶](#fixed "Link to this heading")

* Fixed a bug in the artifact dependency inventory that incorrectly reported `.options()` configuration as a data source.

### Desktop Release Notes[¶](#desktop-release-notes "Link to this heading")

#### Added[¶](#id1 "Link to this heading")

* **Technical Discovery View:** A new Technical Discovery View is now available in the desktop application.
* **SMA Assessment AI:** SMA desktop application is now directly integrated with an optional LLM interface.

  + Ask questions about your assessment results
  + Get help with how to approach the migration
  + Connect and deploy your assessment results directly into your Snowflake account.

#### Changed[¶](#id2 "Link to this heading")

* The Command Line Interface (CLI) parameter for controlling Jupyter conversion has been updated from `--enableJupyter` to `--disableJupyterConversion` for clearer functionality.

## Version 2.10.5 (December 3rd, 2025)[¶](#version-2-10-5-december-3rd-2025 "Link to this heading")

### Application & CLI Version: 2.10.5[¶](#application-cli-version-2-10-5 "Link to this heading")

#### Included SMA Core Versions[¶](#included-sma-core-versions "Link to this heading")

* Snowpark Conversion Core: 8.1.26

#### Included SnowConvert AI Version[¶](#id3 "Link to this heading")

* SnowConvert AI Version 2.0.57 (Release Notes: [SnowConvert AI - Recent Release Notes | Snowflake Documentation](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/release-notes/release-notes/README))

### Engine Release Notes[¶](#id4 "Link to this heading")

#### Added[¶](#id5 "Link to this heading")

* The **Execution Summary** section of the `DetailedReport.docx` now indicates whether the SMA was run in Assessment or Conversion mode.

#### Changed[¶](#id6 "Link to this heading")

* Bumped the supported versions of Snowpark Python API and Snowpark Pandas API from `1.39.0` to `1.40.0`.

**PySpark Function Mapping Updates:**

**NotSupported** to **Rename**:

* `pyspark.sql.functions.unhex` → `snowflake.snowpark.functions.hex_decode_binary`

**Direct** to **Rename**:

* `pyspark.sql.functions.greatest` → `snowflake.snowpark.functions.greatest_ignore_nulls`
* `pyspark.sql.functions.least` → `snowflake.snowpark.functions.least_ignore_nulls`

**NotDefined** to **Rename**:

* `pyspark.sql.functions.bool_or` → `snowflake.snowpark.functions.boolor_agg`
* `pyspark.sql.functions.char` → `snowflake.snowpark.functions.chr`

**NotDefined** to **Direct**:

* `pyspark.sql.functions.nullif` → `snowflake.snowpark.functions.nullif`
* `pyspark.sql.functions.nvl2` → `snowflake.snowpark.functions.nvl2`

**Snowpark Pandas Function Mapping Updates:**

**NotSupported** to **Partial**:

* `modin.pandas.DataFrame.query` → `snowflake.snowpark.pandas.core.frame.DataFrame.query`
* Added a new EWI `PNDSPY1012` to indicate that `modin.pandas.DataFrame.query` does not support MultiIndex. The following example scenario illustrating this limitation is also included in the EWI documentation.

  ```
  from snowflake.snowpark.modin import plugin
  import modin.pandas as pd # Snowpark pandas

  # Create a DataFrame with single-level index
  data = {
      'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank'],
      'age': [25, 30, 35, 28, 32, 45],
      'salary': [50000, 60000, 75000, 55000, 80000, 90000],
      'department': ['Sales', 'IT', 'HR', 'Sales', 'IT', 'HR']
  }
  df = pd.DataFrame(data)

  # Set a single-level index
  df = df.set_index('name')
  print("DataFrame with single-level index:")
  print(df)

  # Use query() - This works fine!
  #EWI: PNDSPY1012 => pandas.core.frame.DataFrame.query does not support DataFrames that have a row MultiIndex. Check Snowpark Pandas documentation for more details.
  result = df.query("age > 30 and salary < 85000")

  # Create a DataFrame with MultiIndex on rows
  data = {
      'A': [1, 2, 3, 4, 5, 6],
      'B': [10, 20, 30, 40, 50, 60],
      'C': ['x', 'y', 'x', 'y', 'x', 'y']
  }
  df = pd.DataFrame(data)

  # Create MultiIndex
  df = df.set_index([
      pd.Index(['group1', 'group1', 'group2', 'group2', 'group3', 'group3']),
      pd.Index(['a', 'b', 'a', 'b', 'a', 'b'])
  ])
  df.index.names = ['group', 'subgroup']

  # This will ERROR in Snowpark pandas!
  #EWI: PNDSPY1012 => pandas.core.frame.DataFrame.query does not support DataFrames that have
  ```

  Copy

  **Recommended fix:** If the DataFrame contains a MultiIndex, it is necessary to validate the behavior of the `query()` method in Snowpark pandas. Ensure that the DataFrame structure is compatible with Snowpark pandas’ limitations, as MultiIndex rows are not supported. Consider restructuring the DataFrame to use a single-level index or alternative filtering methods.
* Updated all documentation links in the `DetailedReport.docx` to point to the official Snowflake documentation, replacing the legacy Snowpark Migration Accelerator site.
* Updated the Snowpark Connect readiness score descriptions in the `DetailedReport.docx` to match the SMA UI.
* Usages of `pyspark.sql.window.WindowSpec.orderBy` are now reported as supported by Snowpark Connect.

#### Fixed[¶](#id7 "Link to this heading")

* Fixed broken internal links in the `DetailedReport.docx` to ensure proper navigation between document sections.
* Added a `CellId` column to the issues inventory to easily identify the location of EWIs within notebook files.

## Version 2.10.4 (November 18, 2025)[¶](#version-2-10-4-november-18-2025 "Link to this heading")

### Application & CLI Version: 2.10.4[¶](#application-cli-version-2-10-4 "Link to this heading")

#### Included SMA Core Versions[¶](#id8 "Link to this heading")

* Snowpark Conversion Core: 8.1.8

### Engine Release Notes[¶](#id9 "Link to this heading")

#### Fixed[¶](#id10 "Link to this heading")

* Fixed an issue where the SMA generated corrupted Databricks notebook files in the output directory during Assessment mode execution.
* Fixed an issue where the SMA would crash if the input directory contained folders named “SMA\_ConvertedNotebooks”.

## Version 2.10.3 (October 30, 2025)[¶](#version-2-10-3-october-30-2025 "Link to this heading")

### Application & CLI Version: 2.10.3[¶](#application-cli-version-2-10-3 "Link to this heading")

#### Included SMA Core Versions[¶](#id11 "Link to this heading")

* Snowpark Conversion Core: 8.1.7

### Engine Release Notes[¶](#id12 "Link to this heading")

#### Added[¶](#id13 "Link to this heading")

* Added the [Snowpark Connect readiness score](https://docs.snowflake.com/en/migrations/sma-docs/user-guide/assessment/readiness-scores#snowpark-connect-readiness-score). This new score measures the percentage of Spark API references in your codebase that are supported by [Snowpark Connect for Spark](https://docs.snowflake.com/en/developer-guide/snowpark-connect/snowpark-connect-overview).

  + This will now be the **only** score shown in assessment mode. To generate the [Snowpark API Readiness Score](https://docs.snowflake.com/en/migrations/sma-docs/user-guide/assessment/readiness-scores#snowpark-api-readiness-score), run the SMA in [conversion mode](https://docs.snowflake.com/en/migrations/sma-docs/user-guide/conversion/README).
* Added support for SQL embedded migration for literal string concatenations assigned to a local variable in the same scope of execution.

  + Included scenarios now include:

    ```
    sqlStat = "SELECT colName " + "FROM myTable" 
    session.sql(sqlStat)
    ```

    Copy

#### Changed[¶](#id14 "Link to this heading")

* Updated the EWI URLs in the [Issues.csv](https://docs.snowflake.com/en/migrations/sma-docs/user-guide/assessment/output-reports/sma-inventories#issue-inventory) inventory to point to the [main Snowflake documentation site](https://docs.snowflake.com/en/migrations/sma-docs/issue-analysis/approach).

#### Fixed[¶](#id15 "Link to this heading")

* Fixed a code issue that caused inner project configuration files (e.g., pom.xml, build.sbt, build.gradle) to be incorrectly placed in the root of the output directory instead of the correct inner directories after migration.

### Desktop Release Notes[¶](#id16 "Link to this heading")

#### Added[¶](#id17 "Link to this heading")

* Added the Snowpark Connect readiness score and updated the assessment execution flow.

  + When running the application in assessment mode, **only** the Snowpark Connect readiness score is now displayed.
  + When running the application in conversion mode, the Snowpark API readiness score is displayed (the Snowpark Connect Readiness will **not** be shown).

#### Changed[¶](#id18 "Link to this heading")

Updated all in-application documentation links to point to the official [Snowflake documentation](https://docs.snowflake.com/en/migrations/sma-docs/README), replacing the legacy [SnowConvert](https://docs.snowconvert.com/sma) site.

## Version 2.10.2 (Oct 27, 2025)[¶](#version-2-10-2-oct-27-2025 "Link to this heading")

### Application & CLI Version 2.10.2[¶](#application-cli-version-2-10-2 "Link to this heading")

#### Included SMA Core Versions[¶](#id19 "Link to this heading")

* Snowpark Conversion Core 8.0.73

#### Fixed[¶](#id20 "Link to this heading")

* Fixed an issue where the Snowpark Migration Accelerator failed converting DBC files into Jupyter Notebooks properly.

## Version 2.10.1 (Oct 23, 2025)[¶](#version-2-10-1-oct-23-2025 "Link to this heading")

### Application & CLI Version 2.10.1[¶](#application-cli-version-2-10-1 "Link to this heading")

#### Included SMA Core Versions[¶](#id21 "Link to this heading")

* Snowpark Conversion Core 8.0.72

#### Added[¶](#id22 "Link to this heading")

* Added support for Snowpark Scala v1.17.0:

**From Not Supported to Direct:**

**Dataset:**

* `org.apache.spark.sql.Dataset.isEmpty` → `com.snowflake.snowpark.DataFrame.isEmpty`

**Row:**

* `org.apache.spark.sql.Row.mkString` → `com.snowflake.snowpark.Row.mkString`

**StructType:**

* `org.apache.spark.sql.types.StructType.fieldNames` → `com.snowflake.snowpark.types.StructType.fieldNames`

**From Not Supported to Rename:**

**Functions:**

* `org.apache.spark.functions.flatten` → `com.snowflake.snowpark.functions.array_flatten`

**From Direct to Rename:**

**Functions:**

* `org.apache.spark.functions.to_date` → `com.snowflake.snowpark.functions.try_to_date`
* `org.apache.spark.functions.to_timestamp` → `com.snowflake.snowpark.functions.try_to_timestamp`

**From Direct Helper to Rename:**

**Functions:**

* `org.apache.spark.sql.functions.concat_ws` → `com.snowflake.snowpark.functions.concat_ws_ignore_nulls`

**From Not Defined to Direct:**

**Functions:**

* `org.apache.spark.functions.try_to_timestamp` → `com.snowflake.snowpark.functions.try_to_timestamp`
* Embedded SQL is now migrated when a SQL statement literal is assigned to a local variable.

Example:
sqlStat = “SELECT colName FROM myTable”
session.sql(sqlStat)

* Embedded SQL is now supported for literal strings concatenations.

Example:
session.sql(“SELECT colName “ + “FROM myTable”)

#### Changed[¶](#id23 "Link to this heading")

* Updated the supported versions of Snowpark Python API and Snowpark Pandas API from 1.36.0 to 1.39.0.
* Updated the mapping status for the following PySpark xpath functions from NotSupported to Direct with EWI SPRKPY1103:

  + `pyspark.sql.functions.xpath`
  + `pyspark.sql.functions.xpath_boolean`
  + `pyspark.sql.functions.xpath_double`
  + `pyspark.sql.functions.xpath_float`
  + `pyspark.sql.functions.xpath_int`
  + `pyspark.sql.functions.xpath_long`
  + `pyspark.sql.functions.xpath_number`
  + `pyspark.sql.functions.xpath_short`
  + `pyspark.sql.functions.xpath_string`
* Updated the mapping status for the following PySpark elements from NotDefined to Direct:

  + `pyspark.sql.functions.bit_and` → `snowflake.snowpark.functions.bitand_agg`
  + `pyspark.sql.functions.bit_or` → `snowflake.snowpark.functions.bitor_agg`
  + `pyspark.sql.functions.bit_xor` → `snowflake.snowpark.functions.bitxor_agg`
  + `pyspark.sql.functions.getbit` → `snowflake.snowpark.functions.getbit`
* Updated the mapping status for the following Pandas elements from NotSupported to Direct:

  + `pandas.core.indexes.base.Index` → `modin.pandas.Index`
  + `pandas.core.indexes.base.Index.get_level_values` → `modin.pandas.Index.get_level_values`
* Updated the mapping status for the following PySpark functions from NotSupported to Rename:

  + `pyspark.sql.functions.now` → `snowflake.snowpark.functions.current_timestamp`

#### Fixed[¶](#id24 "Link to this heading")

* Fixed Scala not migrating imports when there’s a rename.

  **Example:**

  **Source code:**

  .. code-block:: scala

  package com.example.functions  
  import org.apache.spark.sql.functions.{to\_timestamp, lit}  
  object ToTimeStampTest extends App {
  to\_timestamp(lit(“sample”))
  to\_timestamp(lit(“sample”), “yyyy-MM-dd”)
  }

  **Output code:**

  .. code-block:: scala

  package com.example.functions  
  import com.snowflake.snowpark.functions.{try\_to\_timestamp, lit}
  import com.snowflake.snowpark\_extensions.Extensions.\_
  import com.snowflake.snowpark\_extensions.Extensions.functions.\_  
  object ToTimeStampTest extends App {
  try\_to\_timestamp(lit(“sample”))
  try\_to\_timestamp(lit(“sample”), “yyyy-MM-dd”)
  }

## Version 2.10.0 (Sep 24, 2025)[¶](#version-2-10-0-sep-24-2025 "Link to this heading")

### Application & CLI Version 2.10.0[¶](#application-cli-version-2-10-0 "Link to this heading")

#### Included SMA Core Versions[¶](#id25 "Link to this heading")

* Snowpark Conversion Core 8.0.62

#### Added[¶](#id26 "Link to this heading")

* Added functionality to migrate SQL embedded with Python format interpolation.
* Added support for `DataFrame.select` and `DataFrame.sort` transformations for greater data processing flexibility.

#### Changed[¶](#id27 "Link to this heading")

* Bumped the supported versions of Snowpark Python API and Snowpark Pandas API to 1.36.0.
* Updated the mapping status of `pandas.core.frame.DataFrame.boxplot` from Not Supported to Direct.
* Updated the mapping status of `DataFrame.select`, `Dataset.select`, `DataFrame.sort` and `Dataset.sort` from Direct to Transformation.
* Snowpark Scala allows a sequence of columns to be passed directly to the select and sort functions, so this transformation changes all the usages such as `df.select(cols: _*)` to `df.select(cols)` and `df.sort(cols: _*)` to `df.sort(cols)`.
* Bumped Python AST and Parser version to 149.1.9.
* Updated the status to Direct for pandas functions:

  + `pandas.core.frame.DataFrame.to_excel`
  + `pandas.core.series.Series.to_excel`
  + `pandas.io.feather_format.read_feather`
  + `pandas.io.orc.read_orc`
  + `pandas.io.stata.read_stata`
* Updated the status for `pyspark.sql.pandas.map_ops.PandasMapOpsMixin.mapInPandas` to workaround using the EWI SPRKPY1102.

#### Fixed[¶](#id28 "Link to this heading")

* Fixed issue that affected SqlEmbedded transformations when using chained method calls.
* Fixed transformations involving PySqlExpr using the new PyLiteralSql to avoid losing Tails.
* Resolved internal stability issues to improve tool robustness and reliability.

## Version 2.7.7 (Aug 28, 2025)[¶](#version-2-7-7-aug-28-2025 "Link to this heading")

### Application & CLI Version 2.7.7[¶](#application-cli-version-2-7-7 "Link to this heading")

#### Included SMA Core Versions[¶](#id29 "Link to this heading")

* Snowpark Conversion Core 8.0.46

#### Added[¶](#id30 "Link to this heading")

* Added new Pandas EWI documentation PNDSPY1011.
* Added support to the following Pandas functions:

  + pandas.core.algorithms.unique
  + pandas.core.dtypes.missing.isna
  + pandas.core.dtypes.missing.isnull
  + pandas.core.dtypes.missing.notna
  + pandas.core.dtypes.missing.notnull
  + pandas.core.resample.Resampler.count
  + pandas.core.resample.Resampler.max
  + pandas.core.resample.Resampler.mean
  + pandas.core.resample.Resampler.median
  + pandas.core.resample.Resampler.min
  + pandas.core.resample.Resampler.size
  + pandas.core.resample.Resampler.sum
  + pandas.core.arrays.timedeltas.TimedeltaArray.total\_seconds
  + pandas.core.series.Series.get
  + pandas.core.series.Series.to\_frame
  + pandas.core.frame.DataFrame.assign
  + pandas.core.frame.DataFrame.get
  + pandas.core.frame.DataFrame.to\_numpy
  + pandas.core.indexes.base.Index.is\_unique
  + pandas.core.indexes.base.Index.has\_duplicates
  + pandas.core.indexes.base.Index.shape
  + pandas.core.indexes.base.Index.array
  + pandas.core.indexes.base.Index.str
  + pandas.core.indexes.base.Index.equals
  + pandas.core.indexes.base.Index.identical
  + pandas.core.indexes.base.Index.unique

Added support to the following Spark Scala functions:

* org.apache.spark.sql.functions.format\_number
* org.apache.spark.sql.functions.from\_unixtime
* org.apache.spark.sql.functions.instr
* org.apache.spark.sql.functions.months\_between
* org.apache.spark.sql.functions.pow
* org.apache.spark.sql.functions.to\_unix\_timestamp
* org.apache.spark.sql.Row.getAs

#### Changed[¶](#id31 "Link to this heading")

* Bumped the version of Snowpark Pandas API supported by the SMA to 1.33.0.
* Bumped the version of Snowpark Scala API supported by the SMA to 1.16.0.
* Updated the mapping status of pyspark.sql.group.GroupedData.pivot from Transformation to Direct.
* Updated the mapping status of org.apache.spark.sql.Builder.master from NotSupported to Transformation. This transformation removes all the identified usages of this element during code conversion.
* Updated the mapping status of org.apache.spark.sql.types.StructType.fieldIndex from NotSupported to Direct.
* Updated the mapping status of org.apache.spark.sql.Row.fieldIndex from NotSupported to Direct.
* Updated the mapping status of org.apache.spark.sql.SparkSession.stop from NotSupported to Rename. All the identified usages of this element are renamed to com.snowflake.snowpark.Session.close during code conversion.
* Updated the mapping status of org.apache.spark.sql.DataFrame.unpersist and org.apache.spark.sql.Dataset.unpersist from NotSupported to Transformation. This transformation removes all the identified usages of this element during code conversion.

#### Fixed[¶](#id32 "Link to this heading")

* Fixed continuation backslash on removed tailed functions.
* Fix the LIBRARY\_PREFIX column in the ConversionStatusLibraries.csv file to use the right identifier for scikit-learn
  library family (scikit-\*).
* Fixed bug not parsing multiline grouped operations.

## Version 2.9.0 (Sep 09, 2025)[¶](#version-2-9-0-sep-09-2025 "Link to this heading")

### Included SMA Core Versions[¶](#id33 "Link to this heading")

* Snowpark Conversion Core 8.0.53

#### Added[¶](#id34 "Link to this heading")

* The following mappings are now performed for `org.apache.spark.sql.Dataset[T]`:

  + `org.apache.spark.sql.Dataset.union` is now `com.snowflake.snowpark.DataFrame.unionAll`
  + `org.apache.spark.sql.Dataset.unionByName` is now `com.snowflake.snowpark.DataFrame.unionAllByName`
* Added support for `org.apache.spark.sql.functions.broadcast` as a transformation.

#### Changed[¶](#id35 "Link to this heading")

* Increased the supported Snowpark Python API version for SMA from `1.27.0` to `1.33.0`.
* The status for the `pyspark.sql.function.randn` function has been updated to Direct.

#### Fixed[¶](#id36 "Link to this heading")

* Resolved an issue where `org.apache.spark.SparkContext.parallelize` was not resolving and now supports it as a transformation.
* Fixed the `Dataset.persist` transformation to work with any type of Dataset, not just `Dataset[Row]`.

## Version 2.7.6 (Jul 17, 2025)[¶](#version-2-7-6-jul-17-2025 "Link to this heading")

### Included SMA Core Versions[¶](#id37 "Link to this heading")

* Snowpark Conversion Core 8.0.30

#### Added[¶](#id38 "Link to this heading")

* Adjusted mappings for spark.DataReader methods.
* `DataFrame.union` is now `DataFrame.unionAll`.
* `DataFrame.unionByName` is now `DataFrame.unionAllByName`.
* Added multi-level artifact dependency columns in artifact inventory
* Added new Pandas EWIs documentation, from `PNDSPY1005` to `PNDSPY1010`.
* Added a specific EWI for `pandas.core.series.Series.apply`.

#### Changed[¶](#id39 "Link to this heading")

* Bumped the version of Snowpark Pandas API supported by the SMA from `1.27.0` to `1.30.0`.

#### Fixed[¶](#id40 "Link to this heading")

* Fixed an issue with missing values in the formula to get the SQL readiness score.
* Fixed a bug that was causing some Pandas elements to have the default EWI message from PySpark.

## Version 2.7.5 (Jul 2, 2025)[¶](#version-2-7-5-jul-2-2025 "Link to this heading")

### Application & CLI Version 2.7.5[¶](#application-cli-version-2-7-5 "Link to this heading")

#### Included SMA Core Versions[¶](#id41 "Link to this heading")

* Snowpark Conversion Core 8.0.19

#### Changed[¶](#id42 "Link to this heading")

* **Refactored Pandas Imports:** Pandas imports now use `modin.pandas` instead of `snowflake.snowpark.modin.pandas`.
* **Improved `dbutils` and Magic Commands Transformation:**

  + A new `sfutils.py` file is now generated, and all `dbutils` prefixes are replaced with `sfutils`.
  + For Databricks (DBX) notebooks, an implicit import for `sfutils` is automatically added.
  + The `sfutils` module simulates various `dbutils` methods, including file system operations (`dbutils.fs`) via a defined Snowflake FileSystem (SFFS) stage, and handles notebook execution (`dbutils.notebook.run`) by transforming it to `EXECUTE NOTEBOOK` SQL functions.
  + `dbutils.notebook.exit` is removed as it is not required in Snowflake.

#### Fixed[¶](#id43 "Link to this heading")

* **Updates in SnowConvert Reports:** SnowConvert reports now include the *CellId* column when instances originate from SMA, and the *FileName* column displays the full path.
* **Updated Artifacts Dependency for SnowConvert Reports:** The SMA’s artifact inventory report, which was previously impacted by the integration of SnowConvert, has been restored. This update enables the SMA tool to accurately capture and analyze *Object References* and *Missing Object References* directly from SnowConvert reports, thereby ensuring the correct retrieval of SQL dependencies for the inventory.

## Version 2.7.4 (Jun 26, 2025)[¶](#version-2-7-4-jun-26-2025 "Link to this heading")

### Application & CLI Version 2.7.4[¶](#application-cli-version-2-7-4 "Link to this heading")

**Desktop App**

#### Added[¶](#id44 "Link to this heading")

* Added telemetry improvements.

#### Fixed[¶](#id45 "Link to this heading")

* Fix documentation links in conversion settings pop-up and Pandas EWIs.

#### Included SMA Core Versions[¶](#id46 "Link to this heading")

* Snowpark Conversion Core 8.0.16

#### Added[¶](#id47 "Link to this heading")

* Transforming Spark XML to Snowpark
* Databricks SQL option in the SQL source language
* Transform JDBC read connections.

#### Changed[¶](#id48 "Link to this heading")

* All the SnowConvert reports are copied to the backup Zip file.
* The folder is renamed from `SqlReports` to `SnowConvertReports`.
* `SqlFunctionsInventory` is moved to the folder `Reports`.
* All the SnowConvert Reports are sent to Telemetry.

#### Fixed[¶](#id49 "Link to this heading")

* Non-deterministic issue with SQL Readiness Score.
* Fixed a false-positive critical result that made the desktop crash.
* Fixed issue causing the Artifacts dependency report not to show the SQL objects.

## Version 2.7.2 (Jun 10, 2025)[¶](#version-2-7-2-jun-10-2025 "Link to this heading")

### Application & CLI Version 2.7.2[¶](#application-cli-version-2-7-2 "Link to this heading")

### Included SMA Core Versions[¶](#id50 "Link to this heading")

* Snowpark Conversion Core 8.0.2

#### Fixed[¶](#id51 "Link to this heading")

* Addressed an issue with SMA execution on the latest Windows OS, as previously reported. This fix resolves the issues encountered in version 2.7.1.

## Version 2.7.1 (Jun 9, 2025)[¶](#version-2-7-1-jun-9-2025 "Link to this heading")

### Application & CLI Version 2.7.1[¶](#application-cli-version-2-7-1 "Link to this heading")

#### Included SMA Core Versions[¶](#id52 "Link to this heading")

* Snowpark Conversion Core 8.0.1

#### Added[¶](#id53 "Link to this heading")

The Snowpark Migration Accelerator (SMA) now orchestrates [SnowConvert](https://docs.snowconvert.com/sc/general/about) to process SQL found in user workloads, including embedded SQL in Python / Scala code, Notebook SQL cells, `.sql` files, and `.hql` files.

The SnowConvert now enhances the previous SMA capabilities:

* [Spark SQL](https://docs.snowconvert.com/sc/translation-references/spark-dbx)

A new folder in the Reports called SQL Reports contains the reports generated by SnowConvert.

#### Known Issues[¶](#known-issues "Link to this heading")

The previous SMA version for SQL reports will appear empty for the following:

* For `Reports/SqlElementsInventory.csv`, partially covered by the `Reports/SqlReports/Elements.yyyymmdd.hhmmss.csv.`
* For `Reports/SqlFunctionsInventory.csv` refer to the new location with the same name at `Reports/SqlReports/SqlFunctionsInventory.csv`

The artifact dependency inventory:

* In the `ArtifactDependencyInventory` the column for the SQL Object will appear empty

## Version 2.6.10 (May 5, 2025)[¶](#version-2-6-10-may-5-2025 "Link to this heading")

### Application & CLI Version 2.6.10[¶](#application-cli-version-2-6-10 "Link to this heading")

#### Included SMA Core Versions[¶](#id54 "Link to this heading")

* Snowpark Conversion Core 7.4.0

#### Fixed[¶](#id55 "Link to this heading")

* Fixed wrong values in the ‘checkpoints.json’ file.

  + The ‘sample’ value was without decimals (for integer values) and quotes.
  + The ‘entryPoint’ value had dots instead of slashes and was missing the file extension.
* Updated the default value to TRUE for the setting ‘Convert DBX notebooks to Snowflake notebooks’

## Version 2.6.8 (Apr 28, 2025)[¶](#version-2-6-8-apr-28-2025 "Link to this heading")

### Application & CLI Version 2.6.8[¶](#application-cli-version-2-6-8 "Link to this heading")

#### Desktop App[¶](#desktop-app "Link to this heading")

* Added checkpoints execution settings mechanism recognition.
* Added a mechanism to collect DBX magic commands into DbxElementsInventory.csv
* Added ‘checkpoints.json’ generation into the input directory.
* Added a new EWI for all not supported magic command.
* Added the collection of dbutils into DbxElementsInventory.csv from scala source notebooks

#### Included SMA Core Versions[¶](#id56 "Link to this heading")

* Snowpark Conversion Core 7.2.53

#### Changed[¶](#id57 "Link to this heading")

* Updates made to handle transformations from DBX Scala elements to Jupyter Python elements, and to comment the entire code from the cell.
* Updates made to handle transformations from dbutils.notebook.run and “r” commands, for the last one, also comment out the entire code from the cell.
* Updated the name and the letter of the key to make the conversion of the notebook files.

#### Fixed[¶](#id58 "Link to this heading")

* Fixed the bug that was causing the transformation of DBX notebooks into .ipynb files to have the wrong format.
* Fixed the bug that was causing .py DBX notebooks to not be transformable into .ipynb files.
* Fixed a bug that was causing comments to be missing in the output code of DBX notebooks.
* Fixed a bug that was causing raw Scala files to be converted into ipynb files.

## Version 2.6.7 (Apr 21, 2025)[¶](#version-2-6-7-apr-21-2025 "Link to this heading")

### Application & CLI Version 2.6.7[¶](#application-cli-version-2-6-7 "Link to this heading")

#### Included SMA Core Versions[¶](#id59 "Link to this heading")

* Snowpark Conversion Core 7.2.42

#### Changed[¶](#id60 "Link to this heading")

Updated DataFramesInventory to fill EntryPoints column

## Version 2.6.6 (Apr 7, 2025)[¶](#version-2-6-6-apr-7-2025 "Link to this heading")

### Application & CLI Version 2.6.6[¶](#application-cli-version-2-6-6 "Link to this heading")

#### Desktop App[¶](#id61 "Link to this heading")

#### Added[¶](#id62 "Link to this heading")

* Update DBx EWI link in the UI results page

#### Included SMA Core Versions[¶](#id63 "Link to this heading")

* Snowpark Conversion Core 7.2.39

#### Added[¶](#id64 "Link to this heading")

* Added Execution Flow inventory generation.
* Added implicit session setup in every DBx notebook transformation

#### Changed[¶](#id65 "Link to this heading")

* Renamed the DbUtilsUsagesInventory.csv to DbxElementsInventory.csv

#### Fixed[¶](#id66 "Link to this heading")

* Fixed a bug that caused a Parsing error when a backslash came after a type hint.
* Fixed relative imports that do not start with a dot and relative imports with a star.

## Version 2.6.5 (Mar 27, 2025)[¶](#version-2-6-5-mar-27-2025 "Link to this heading")

### Application & CLI Version 2.6.5[¶](#application-cli-version-2-6-5 "Link to this heading")

#### Desktop App[¶](#id67 "Link to this heading")

#### Added[¶](#id68 "Link to this heading")

* Added a new conversion setting toggle to enable or disable Sma-Checkpoints feature.
* Fix report issue to not crash when post api returns 500

#### Included SMA Core Versions[¶](#id69 "Link to this heading")

* Snowpark Conversion Core 7.2.26

#### Added[¶](#id70 "Link to this heading")

* Added generation of the checkpoints.json file into the output folder based on the DataFramesInventory.csv.
* Added “disableCheckpoints” flag into the CLI commands and additional parameters of the code processor.
* Added a new replacer for Python to transform the dbutils.notebook.run node.
* Added new replacers to transform the magic %run command.
* Added new replacers (Python and Scala) to remove the dbutils.notebook.exit node.
* Added Location column to artifacts inventory.

#### Changed[¶](#id71 "Link to this heading")

* Refactored the normalized directory separator used in some parts of the solution.
* Centralized the DBC extraction working folder name handling.
* Updated Snowpark and Pandas version to v1.27.0
* Updated the artifacts inventory columns to:

  + Name -> Dependency
  + File -> FileId
  + Status -> Status\_detail
* Added new column to the artifacts inventory:

  + Success

#### Fixed[¶](#id72 "Link to this heading")

* Dataframes inventory was not being uploaded to the stage correctly.

## Version 2.6.4 (Mar 12, 2025)[¶](#version-2-6-4-mar-12-2025 "Link to this heading")

### Application & CLI Version 2.6.4[¶](#application-cli-version-2-6-4 "Link to this heading")

#### Included SMA Core Versions [¶](#id73 "Link to this heading")

* Snowpark Conversion Core 7.2.0

#### Added [¶](#id74 "Link to this heading")

* An Artifact Dependency Inventory
* A replacer and EWI for pyspark.sql.types.StructType.fieldNames method to snowflake.snowpark.types.StructType.fieldNames attribute.
* The following **PySpark** functions with the status:

Direct Status

* `pyspark.sql.functions.bitmap_bit_position`
* `pyspark.sql.functions.bitmap_bucket_number`
* `pyspark.sql.functions.bitmap_construct_agg`
* `pyspark.sql.functions.equal_null`
* `pyspark.sql.functions.ifnull`
* `pyspark.sql.functions.localtimestamp`
* `pyspark.sql.functions.max_by`
* `pyspark.sql.functions.min_by`
* `pyspark.sql.functions.nvl`
* `pyspark.sql.functions.regr_avgx`
* `pyspark.sql.functions.regr_avgy`
* `pyspark.sql.functions.regr_count`
* `pyspark.sql.functions.regr_intercept`
* `pyspark.sql.functions.regr_slope`
* `pyspark.sql.functions.regr_sxx`
* `pyspark.sql.functions.regr_sxy`
* `pyspark.sql.functions.regr`

NotSupported

* `pyspark.sql.functions.map_contains_key`
* `pyspark.sql.functions.position`
* `pyspark.sql.functions.regr_r2`
* `pyspark.sql.functions.try_to_binary`

The following **Pandas** functions with status

* `pandas.core.series.Series.str.ljust`
* `pandas.core.series.Series.str.center`
* `pandas.core.series.Series.str.pad`
* `pandas.core.series.Series.str.rjust`

Update the following **Pyspark** functions with the status

From WorkAround to Direct

* `pyspark.sql.functions.acosh`
* `pyspark.sql.functions.asinh`
* `pyspark.sql.functions.atanh`
* `pyspark.sql.functions.instr`
* `pyspark.sql.functions.log10`
* `pyspark.sql.functions.log1p`
* `pyspark.sql.functions.log2`

From NotSupported to Direct

* `pyspark.sql.functions.bit_length`
* `pyspark.sql.functions.cbrt`
* `pyspark.sql.functions.nth_value`
* `pyspark.sql.functions.octet_length`
* `pyspark.sql.functions.base64`
* `pyspark.sql.functions.unbase64`

Updated the folloing **Pandas** functions with the status

From NotSupported to Direct

* `pandas.core.frame.DataFrame.pop`
* `pandas.core.series.Series.between`
* `pandas.core.series.Series.pop`

## Version 2.6.3 (Mar 6, 2025)[¶](#version-2-6-3-mar-6-2025 "Link to this heading")

### Application & CLI Version 2.6.3[¶](#application-cli-version-2-6-3 "Link to this heading")

#### Included SMA Core Versions [¶](#id75 "Link to this heading")

* Snowpark Conversion Core 7.1.13

#### Added [¶](#id76 "Link to this heading")

* Added csv generator class for new inventory creation.
* Added “full\_name” column to import usages inventory.
* Added transformation from pyspark.sql.functions.concat\_ws to snowflake.snowpark.functions.\_concat\_ws\_ignore\_nulls.
* Added logic for generation of checkpoints.json.
* Added the inventories:

  + DataFramesInventory.csv.
  + CheckpointsInventory.csv

## Version 2.6.0 (Feb 21, 2025)[¶](#version-2-6-0-feb-21-2025 "Link to this heading")

### Application & CLI Version 2.6.0[¶](#application-cli-version-2-6-0 "Link to this heading")

#### Desktop App [¶](#id77 "Link to this heading")

* Updated the licensing agreement, acceptance is required.

#### Included SMA Core Versions[¶](#id78 "Link to this heading")

* Snowpark Conversion Core 7.1.2

Added

Updated the mapping status for the following PySpark elements, from `NotSupported` to `Direct`

* `pyspark.sql.types.ArrayType.json`
* `pyspark.sql.types.ArrayType.jsonValue`
* `pyspark.sql.types.ArrayType.simpleString`
* `pyspark.sql.types.ArrayType.typeName`
* `pyspark.sql.types.AtomicType.json`
* `pyspark.sql.types.AtomicType.jsonValue`
* `pyspark.sql.types.AtomicType.simpleString`
* `pyspark.sql.types.AtomicType.typeName`
* `pyspark.sql.types.BinaryType.json`
* `pyspark.sql.types.BinaryType.jsonValue`
* `pyspark.sql.types.BinaryType.simpleString`
* `pyspark.sql.types.BinaryType.typeName`
* `pyspark.sql.types.BooleanType.json`
* `pyspark.sql.types.BooleanType.jsonValue`
* `pyspark.sql.types.BooleanType.simpleString`
* `pyspark.sql.types.BooleanType.typeName`
* `pyspark.sql.types.ByteType.json`
* `pyspark.sql.types.ByteType.jsonValue`
* `pyspark.sql.types.ByteType.simpleString`
* `pyspark.sql.types.ByteType.typeName`
* `pyspark.sql.types.DecimalType.json`
* `pyspark.sql.types.DecimalType.jsonValue`
* `pyspark.sql.types.DecimalType.simpleString`
* `pyspark.sql.types.DecimalType.typeName`
* `pyspark.sql.types.DoubleType.json`
* `pyspark.sql.types.DoubleType.jsonValue`
* `pyspark.sql.types.DoubleType.simpleString`
* `pyspark.sql.types.DoubleType.typeName`
* `pyspark.sql.types.FloatType.json`
* `pyspark.sql.types.FloatType.jsonValue`
* `pyspark.sql.types.FloatType.simpleString`
* `pyspark.sql.types.FloatType.typeName`
* `pyspark.sql.types.FractionalType.json`
* `pyspark.sql.types.FractionalType.jsonValue`
* `pyspark.sql.types.FractionalType.simpleString`
* `pyspark.sql.types.FractionalType.typeName`
* `pyspark.sql.types.IntegerType.json`
* `pyspark.sql.types.IntegerType.jsonValue`
* `pyspark.sql.types.IntegerType.simpleString`
* `pyspark.sql.types.IntegerType.typeName`
* `pyspark.sql.types.IntegralType.json`
* `pyspark.sql.types.IntegralType.jsonValue`
* `pyspark.sql.types.IntegralType.simpleString`
* `pyspark.sql.types.IntegralType.typeName`
* `pyspark.sql.types.LongType.json`
* `pyspark.sql.types.LongType.jsonValue`
* `pyspark.sql.types.LongType.simpleString`
* `pyspark.sql.types.LongType.typeName`
* `pyspark.sql.types.MapType.json`
* `pyspark.sql.types.MapType.jsonValue`
* `pyspark.sql.types.MapType.simpleString`
* `pyspark.sql.types.MapType.typeName`
* `pyspark.sql.types.NullType.json`
* `pyspark.sql.types.NullType.jsonValue`
* `pyspark.sql.types.NullType.simpleString`
* `pyspark.sql.types.NullType.typeName`
* `pyspark.sql.types.NumericType.json`
* `pyspark.sql.types.NumericType.jsonValue`
* `pyspark.sql.types.NumericType.simpleString`
* `pyspark.sql.types.NumericType.typeName`
* `pyspark.sql.types.ShortType.json`
* `pyspark.sql.types.ShortType.jsonValue`
* `pyspark.sql.types.ShortType.simpleString`
* `pyspark.sql.types.ShortType.typeName`
* `pyspark.sql.types.StringType.json`
* `pyspark.sql.types.StringType.jsonValue`
* `pyspark.sql.types.StringType.simpleString`
* `pyspark.sql.types.StringType.typeName`
* `pyspark.sql.types.StructType.json`
* `pyspark.sql.types.StructType.jsonValue`
* `pyspark.sql.types.StructType.simpleString`
* `pyspark.sql.types.StructType.typeName`
* `pyspark.sql.types.TimestampType.json`
* `pyspark.sql.types.TimestampType.jsonValue`
* `pyspark.sql.types.TimestampType.simpleString`
* `pyspark.sql.types.TimestampType.typeName`
* `pyspark.sql.types.StructField.simpleString`
* `pyspark.sql.types.StructField.typeName`
* `pyspark.sql.types.StructField.json`
* `pyspark.sql.types.StructField.jsonValue`
* `pyspark.sql.types.DataType.json`
* `pyspark.sql.types.DataType.jsonValue`
* `pyspark.sql.types.DataType.simpleString`
* `pyspark.sql.types.DataType.typeName`
* `pyspark.sql.session.SparkSession.getActiveSession`
* `pyspark.sql.session.SparkSession.version`
* `pandas.io.html.read_html`
* `pandas.io.json._normalize.json_normalize`
* `pyspark.sql.types.ArrayType.fromJson`
* `pyspark.sql.types.MapType.fromJson`
* `pyspark.sql.types.StructField.fromJson`
* `pyspark.sql.types.StructType.fromJson`
* `pandas.core.groupby.generic.DataFrameGroupBy.pct_change`
* `pandas.core.groupby.generic.SeriesGroupBy.pct_change`

Updated the mapping status for the following Pandas elements, from `NotSupported` to `Direct`

* `pandas.io.html.read_html`
* `pandas.io.json._normalize.json_normalize`
* `pandas.core.groupby.generic.DataFrameGroupBy.pct_change`
* `pandas.core.groupby.generic.SeriesGroupBy.pct_change`

Updated the mapping status for the following PySpark elements, from `Rename` to `Direct`

* `pyspark.sql.functions.collect_list`
* `pyspark.sql.functions.size`

#### Fixed [¶](#id79 "Link to this heading")

* Standardized the format of the version number in the inventories.

## Version 2.5.2 (Feb 5, 2025)[¶](#version-2-5-2-feb-5-2025 "Link to this heading")

### Hotfix: Application & CLI Version 2.5.2[¶](#hotfix-application-cli-version-2-5-2 "Link to this heading")

### Desktop App[¶](#id80 "Link to this heading")

* Fixed an issue when converting in the sample project option.

### Included SMA Core Versions[¶](#id81 "Link to this heading")

* Snowpark Conversion Core 5.3.0

## Version 2.5.1 (Feb 4, 2025)[¶](#version-2-5-1-feb-4-2025 "Link to this heading")

### Application & CLI Version 2.5.1[¶](#application-cli-version-2-5-1 "Link to this heading")

### Desktop App[¶](#id82 "Link to this heading")

* Added a new modal when the user does not have write permission.
* Updated the licensing aggrement, acceptance is required.

### CLI[¶](#cli "Link to this heading")

* Fixed the year in the CLI screen when showing “–version” or “-v”

### Included SMA Core Versions included-sma-core-versions[¶](#included-sma-core-versions-included-sma-core-versions "Link to this heading")

* Snowpark Conversion Core 5.3.0

#### Added[¶](#id83 "Link to this heading")

Added the following Python Third-Party libraries with Direct status:

* `about-time`
* `affinegap`
* `aiohappyeyeballs`
* `alibi-detect`
* `alive-progress`
* `allure-nose2`
* `allure-robotframework`
* `anaconda-cloud-cli`
* `anaconda-mirror`
* `astropy-iers-data`
* `asynch`
* `asyncssh`
* `autots`
* `autoviml`
* `aws-msk-iam-sasl-signer-python`
* `azure-functions`
* `backports.tarfile`
* `blas`
* `bottle`
* `bson`
* `cairo`
* `capnproto`
* `captum`
* `categorical-distance`
* `census`
* `clickhouse-driver`
* `clustergram`
* `cma`
* `conda-anaconda-telemetry`
* `configspace`
* `cpp-expected`
* `dask-expr`
* `data-science-utils`
* `databricks-sdk`
* `datetime-distance`
* `db-dtypes`
* `dedupe`
* `dedupe-variable-datetime`
* `dedupe_lehvenshtein_search`
* `dedupe_levenshtein_search`
* `diff-cover`
* `diptest`
* `dmglib`
* `docstring_parser`
* `doublemetaphone`
* `dspy-ai`
* `econml`
* `emcee`
* `emoji`
* `environs`
* `eth-abi`
* `eth-hash`
* `eth-typing`
* `eth-utils`
* `expat`
* `filetype`
* `fitter`
* `flask-cors`
* `fpdf2`
* `frozendict`
* `gcab`
* `geojson`
* `gettext`
* `glib-tools`
* `google-ads`
* `google-ai-generativelanguage`
* `google-api-python-client`
* `google-auth-httplib2`
* `google-cloud-bigquery`
* `google-cloud-bigquery-core`
* `google-cloud-bigquery-storage`
* `google-cloud-bigquery-storage-core`
* `google-cloud-resource-manager`
* `google-generativeai`
* `googlemaps`
* `grapheme`
* `graphene`
* `graphql-relay`
* `gravis`
* `greykite`
* `grpc-google-iam-v1`
* `harfbuzz`
* `hatch-fancy-pypi-readme`
* `haversine`
* `hiclass`
* `hicolor-icon-theme`
* `highered`
* `hmmlearn`
* `holidays-ext`
* `httplib2`
* `icu`
* `imbalanced-ensemble`
* `immutabledict`
* `importlib-metadata`
* `importlib-resources`
* `inquirerpy`
* `iterative-telemetry`
* `jaraco.context`
* `jaraco.test`
* `jiter`
* `jiwer`
* `joserfc`
* `jsoncpp`
* `jsonpath`
* `jsonpath-ng`
* `jsonpath-python`
* `kagglehub`
* `keplergl`
* `kt-legacy`
* `langchain-community`
* `langchain-experimental`
* `langchain-snowflake`
* `langchain-text-splitters`
* `libabseil`
* `libflac`
* `libgfortran-ng`
* `libgfortran5`
* `libglib`
* `libgomp`
* `libgrpc`
* `libgsf`
* `libmagic`
* `libogg`
* `libopenblas`
* `libpostal`
* `libprotobuf`
* `libsentencepiece`
* `libsndfile`
* `libstdcxx-ng`
* `libtheora`
* `libtiff`
* `libvorbis`
* `libwebp`
* `lightweight-mmm`
* `litestar`
* `litestar-with-annotated-types`
* `litestar-with-attrs`
* `litestar-with-cryptography`
* `litestar-with-jinja`
* `litestar-with-jwt`
* `litestar-with-prometheus`
* `litestar-with-structlog`
* `lunarcalendar-ext`
* `matplotlib-venn`
* `metricks`
* `mimesis`
* `modin-ray`
* `momepy`
* `mpg123`
* `msgspec`
* `msgspec-toml`
* `msgspec-yaml`
* `msitools`
* `multipart`
* `namex`
* `nbconvert-all`
* `nbconvert-core`
* `nbconvert-pandoc`
* `nlohmann_json`
* `numba-cuda`
* `numpyro`
* `office365-rest-python-client`
* `openapi-pydantic`
* `opentelemetry-distro`
* `opentelemetry-instrumentation`
* `opentelemetry-instrumentation-system-metrics`
* `optree`
* `osmnx`
* `pathlib`
* `pdf2image`
* `pfzy`
* `pgpy`
* `plumbum`
* `pm4py`
* `polars`
* `polyfactory`
* `poppler-cpp`
* `postal`
* `pre-commit`
* `prompt-toolkit`
* `propcache`
* `py-partiql-parser`
* `py_stringmatching`
* `pyatlan`
* `pyfakefs`
* `pyfhel`
* `pyhacrf-datamade`
* `pyiceberg`
* `pykrb5`
* `pylbfgs`
* `pymilvus`
* `pymoo`
* `pynisher`
* `pyomo`
* `pypdf`
* `pypdf-with-crypto`
* `pypdf-with-full`
* `pypdf-with-image`
* `pypng`
* `pyprind`
* `pyrfr`
* `pysoundfile`
* `pytest-codspeed`
* `pytest-trio`
* `python-barcode`
* `python-box`
* `python-docx`
* `python-gssapi`
* `python-iso639`
* `python-magic`
* `python-pandoc`
* `python-zstd`
* `pyuca`
* `pyvinecopulib`
* `pyxirr`
* `qrcode`
* `rai-sdk`
* `ray-client`
* `ray-observability`
* `readline`
* `rich-click`
* `rouge-score`
* `ruff`
* `scikit-criteria`
* `scikit-mobility`
* `sentencepiece-python`
* `sentencepiece-spm`
* `setuptools-markdown`
* `setuptools-scm`
* `setuptools-scm-git-archive`
* `shareplum`
* `simdjson`
* `simplecosine`
* `sis-extras`
* `slack-sdk`
* `smac`
* `snowflake-sqlalchemy`
* `snowflake_legacy`
* `socrata-py`
* `spdlog`
* `sphinxcontrib-images`
* `sphinxcontrib-jquery`
* `sphinxcontrib-youtube`
* `splunk-opentelemetry`
* `sqlfluff`
* `squarify`
* `st-theme`
* `statistics`
* `streamlit-antd-components`
* `streamlit-condition-tree`
* `streamlit-echarts`
* `streamlit-feedback`
* `streamlit-keplergl`
* `streamlit-mermaid`
* `streamlit-navigation-bar`
* `streamlit-option-menu`
* `strictyaml`
* `stringdist`
* `sybil`
* `tensorflow-cpu`
* `tensorflow-text`
* `tiledb-ptorchaudio`
* `torcheval`
* `trio-websocket`
* `trulens-connectors-snowflake`
* `trulens-core`
* `trulens-dashboard`
* `trulens-feedback`
* `trulens-otel-semconv`
* `trulens-providers-cortex`
* `tsdownsample`
* `typing`
* `typing-extensions`
* `typing_extensions`
* `unittest-xml-reporting`
* `uritemplate`
* `us`
* `uuid6`
* `wfdb`
* `wsproto`
* `zlib`
* `zope.index`

Added the following Python BuiltIn libraries with Direct status:

* `aifc`
* `array`
* `ast`
* `asynchat`
* `asyncio`
* `asyncore`
* `atexit`
* `audioop`
* `base64`
* `bdb`
* `binascii`
* `bitsect`
* `builtins`
* `bz2`
* `calendar`
* `cgi`
* `cgitb`
* `chunk`
* `cmath`
* `cmd`
* `code`
* `codecs`
* `codeop`
* `colorsys`
* `compileall`
* `concurrent`
* `contextlib`
* `contextvars`
* `copy`
* `copyreg`
* `cprofile`
* `crypt`
* `csv`
* `ctypes`
* `curses`
* `dbm`
* `difflib`
* `dis`
* `distutils`
* `doctest`
* `email`
* `ensurepip`
* `enum`
* `errno`
* `faulthandler`
* `fcntl`
* `filecmp`
* `fileinput`
* `fnmatch`
* `fractions`
* `ftplib`
* `functools`
* `gc`
* `getopt`
* `getpass`
* `gettext`
* `graphlib`
* `grp`
* `gzip`
* `hashlib`
* `heapq`
* `hmac`
* `html`
* `http`
* `idlelib`
* `imaplib`
* `imghdr`
* `imp`
* `importlib`
* `inspect`
* `ipaddress`
* `itertools`
* `keyword`
* `linecache`
* `locale`
* `lzma`
* `mailbox`
* `mailcap`
* `marshal`
* `math`
* `mimetypes`
* `mmap`
* `modulefinder`
* `msilib`
* `multiprocessing`
* `netrc`
* `nis`
* `nntplib`
* `numbers`
* `operator`
* `optparse`
* `ossaudiodev`
* `pdb`
* `pickle`
* `pickletools`
* `pipes`
* `pkgutil`
* `platform`
* `plistlib`
* `poplib`
* `posix`
* `pprint`
* `profile`
* `pstats`
* `pty`
* `pwd`
* `py_compile`
* `pyclbr`
* `pydoc`
* `queue`
* `quopri`
* `random`
* `re`
* `reprlib`
* `resource`
* `rlcompleter`
* `runpy`
* `sched`
* `secrets`
* `select`
* `selectors`
* `shelve`
* `shlex`
* `signal`
* `site`
* `sitecustomize`
* `smtpd`
* `smtplib`
* `sndhdr`
* `socket`
* `socketserver`
* `spwd`
* `sqlite3`
* `ssl`
* `stat`
* `string`
* `stringprep`
* `struct`
* `subprocess`
* `sunau`
* `symtable`
* `sysconfig`
* `syslog`
* `tabnanny`
* `tarfile`
* `telnetlib`
* `tempfile`
* `termios`
* `test`
* `textwrap`
* `threading`
* `timeit`
* `tkinter`
* `token`
* `tokenize`
* `tomllib`
* `trace`
* `traceback`
* `tracemalloc`
* `tty`
* `turtle`
* `turtledemo`
* `types`
* `unicodedata`
* `urllib`
* `uu`
* `uuid`
* `venv`
* `warnings`
* `wave`
* `weakref`
* `webbrowser`
* `wsgiref`
* `xdrlib`
* `xml`
* `xmlrpc`
* `zipapp`
* `zipfile`
* `zipimport`
* `zoneinfo`

Added the following Python BuiltIn libraries with NotSupported status:

* `msvcrt`
* `winreg`
* `winsound`

#### Changed[¶](#id84 "Link to this heading")

* Update .NET version to v9.0.0.
* Improved EWI SPRKPY1068.
* Bumped the version of Snowpark Python API supported by the SMA from 1.24.0 to 1.25.0.
* Updated the detailed report template, now has the Snowpark version for Pandas.
* Changed the following libraries from **ThirdPartyLib** to **BuiltIn**.

  + `configparser`
  + `dataclasses`
  + `pathlib`
  + `readline`
  + `statistics`
  + `zlib`

Updated the mapping status for the following Pandas elements, from Direct to Partial:

* `pandas.core.frame.DataFrame.add`
* `pandas.core.frame.DataFrame.aggregate`
* `pandas.core.frame.DataFrame.all`
* `pandas.core.frame.DataFrame.apply`
* `pandas.core.frame.DataFrame.astype`
* `pandas.core.frame.DataFrame.cumsum`
* `pandas.core.frame.DataFrame.div`
* `pandas.core.frame.DataFrame.dropna`
* `pandas.core.frame.DataFrame.eq`
* `pandas.core.frame.DataFrame.ffill`
* `pandas.core.frame.DataFrame.fillna`
* `pandas.core.frame.DataFrame.floordiv`
* `pandas.core.frame.DataFrame.ge`
* `pandas.core.frame.DataFrame.groupby`
* `pandas.core.frame.DataFrame.gt`
* `pandas.core.frame.DataFrame.idxmax`
* `pandas.core.frame.DataFrame.idxmin`
* `pandas.core.frame.DataFrame.inf`
* `pandas.core.frame.DataFrame.join`
* `pandas.core.frame.DataFrame.le`
* `pandas.core.frame.DataFrame.loc`
* `pandas.core.frame.DataFrame.lt`
* `pandas.core.frame.DataFrame.mask`
* `pandas.core.frame.DataFrame.merge`
* `pandas.core.frame.DataFrame.mod`
* `pandas.core.frame.DataFrame.mul`
* `pandas.core.frame.DataFrame.ne`
* `pandas.core.frame.DataFrame.nunique`
* `pandas.core.frame.DataFrame.pivot_table`
* `pandas.core.frame.DataFrame.pow`
* `pandas.core.frame.DataFrame.radd`
* `pandas.core.frame.DataFrame.rank`
* `pandas.core.frame.DataFrame.rdiv`
* `pandas.core.frame.DataFrame.rename`
* `pandas.core.frame.DataFrame.replace`
* `pandas.core.frame.DataFrame.resample`
* `pandas.core.frame.DataFrame.rfloordiv`
* `pandas.core.frame.DataFrame.rmod`
* `pandas.core.frame.DataFrame.rmul`
* `pandas.core.frame.DataFrame.rolling`
* `pandas.core.frame.DataFrame.round`
* `pandas.core.frame.DataFrame.rpow`
* `pandas.core.frame.DataFrame.rsub`
* `pandas.core.frame.DataFrame.rtruediv`
* `pandas.core.frame.DataFrame.shift`
* `pandas.core.frame.DataFrame.skew`
* `pandas.core.frame.DataFrame.sort_index`
* `pandas.core.frame.DataFrame.sort_values`
* `pandas.core.frame.DataFrame.sub`
* `pandas.core.frame.DataFrame.to_dict`
* `pandas.core.frame.DataFrame.transform`
* `pandas.core.frame.DataFrame.transpose`
* `pandas.core.frame.DataFrame.truediv`
* `pandas.core.frame.DataFrame.var`
* `pandas.core.indexes.datetimes.date_range`
* `pandas.core.reshape.concat.concat`
* `pandas.core.reshape.melt.melt`
* `pandas.core.reshape.merge.merge`
* `pandas.core.reshape.pivot.pivot_table`
* `pandas.core.reshape.tile.cut`
* `pandas.core.series.Series.add`
* `pandas.core.series.Series.aggregate`
* `pandas.core.series.Series.all`
* `pandas.core.series.Series.any`
* `pandas.core.series.Series.cumsum`
* `pandas.core.series.Series.div`
* `pandas.core.series.Series.dropna`
* `pandas.core.series.Series.eq`
* `pandas.core.series.Series.ffill`
* `pandas.core.series.Series.fillna`
* `pandas.core.series.Series.floordiv`
* `pandas.core.series.Series.ge`
* `pandas.core.series.Series.gt`
* `pandas.core.series.Series.lt`
* `pandas.core.series.Series.mask`
* `pandas.core.series.Series.mod`
* `pandas.core.series.Series.mul`
* `pandas.core.series.Series.multiply`
* `pandas.core.series.Series.ne`
* `pandas.core.series.Series.pow`
* `pandas.core.series.Series.quantile`
* `pandas.core.series.Series.radd`
* `pandas.core.series.Series.rank`
* `pandas.core.series.Series.rdiv`
* `pandas.core.series.Series.rename`
* `pandas.core.series.Series.replace`
* `pandas.core.series.Series.resample`
* `pandas.core.series.Series.rfloordiv`
* `pandas.core.series.Series.rmod`
* `pandas.core.series.Series.rmul`
* `pandas.core.series.Series.rolling`
* `pandas.core.series.Series.rpow`
* `pandas.core.series.Series.rsub`
* `pandas.core.series.Series.rtruediv`
* `pandas.core.series.Series.sample`
* `pandas.core.series.Series.shift`
* `pandas.core.series.Series.skew`
* `pandas.core.series.Series.sort_index`
* `pandas.core.series.Series.sort_values`
* `pandas.core.series.Series.std`
* `pandas.core.series.Series.sub`
* `pandas.core.series.Series.subtract`
* `pandas.core.series.Series.truediv`
* `pandas.core.series.Series.value_counts`
* `pandas.core.series.Series.var`
* `pandas.core.series.Series.where`
* `pandas.core.tools.numeric.to_numeric`

Updated the mapping status for the following Pandas elements, from NotSupported to Direct:

* `pandas.core.frame.DataFrame.attrs`
* `pandas.core.indexes.base.Index.to_numpy`
* `pandas.core.series.Series.str.len`
* `pandas.io.html.read_html`
* `pandas.io.xml.read_xml`
* `pandas.core.indexes.datetimes.DatetimeIndex.mean`
* `pandas.core.resample.Resampler.indices`
* `pandas.core.resample.Resampler.nunique`
* `pandas.core.series.Series.items`
* `pandas.core.tools.datetimes.to_datetime`
* `pandas.io.sas.sasreader.read_sas`
* `pandas.core.frame.DataFrame.attrs`
* `pandas.core.frame.DataFrame.style`
* `pandas.core.frame.DataFrame.items`
* `pandas.core.groupby.generic.DataFrameGroupBy.head`
* `pandas.core.groupby.generic.DataFrameGroupBy.median`
* `pandas.core.groupby.generic.DataFrameGroupBy.min`
* `pandas.core.groupby.generic.DataFrameGroupBy.nunique`
* `pandas.core.groupby.generic.DataFrameGroupBy.tail`
* `pandas.core.indexes.base.Index.is_boolean`
* `pandas.core.indexes.base.Index.is_floating`
* `pandas.core.indexes.base.Index.is_integer`
* `pandas.core.indexes.base.Index.is_monotonic_decreasing`
* `pandas.core.indexes.base.Index.is_monotonic_increasing`
* `pandas.core.indexes.base.Index.is_numeric`
* `pandas.core.indexes.base.Index.is_object`
* `pandas.core.indexes.base.Index.max`
* `pandas.core.indexes.base.Index.min`
* `pandas.core.indexes.base.Index.name`
* `pandas.core.indexes.base.Index.names`
* `pandas.core.indexes.base.Index.rename`
* `pandas.core.indexes.base.Index.set_names`
* `pandas.core.indexes.datetimes.DatetimeIndex.day_name`
* `pandas.core.indexes.datetimes.DatetimeIndex.month_name`
* `pandas.core.indexes.datetimes.DatetimeIndex.time`
* `pandas.core.indexes.timedeltas.TimedeltaIndex.ceil`
* `pandas.core.indexes.timedeltas.TimedeltaIndex.days`
* `pandas.core.indexes.timedeltas.TimedeltaIndex.floor`
* `pandas.core.indexes.timedeltas.TimedeltaIndex.microseconds`
* `pandas.core.indexes.timedeltas.TimedeltaIndex.nanoseconds`
* `pandas.core.indexes.timedeltas.TimedeltaIndex.round`
* `pandas.core.indexes.timedeltas.TimedeltaIndex.seconds`
* `pandas.core.reshape.pivot.crosstab`
* `pandas.core.series.Series.dt.round`
* `pandas.core.series.Series.dt.time`
* `pandas.core.series.Series.dt.weekday`
* `pandas.core.series.Series.is_monotonic_decreasing`
* `pandas.core.series.Series.is_monotonic_increasing`

Updated the mapping status for the following Pandas elements, from NotSupported to Partial:

* `pandas.core.frame.DataFrame.align`
* `pandas.core.series.Series.align`
* `pandas.core.frame.DataFrame.tz_convert`
* `pandas.core.frame.DataFrame.tz_localize`
* `pandas.core.groupby.generic.DataFrameGroupBy.fillna`
* `pandas.core.groupby.generic.SeriesGroupBy.fillna`
* `pandas.core.indexes.datetimes.bdate_range`
* `pandas.core.indexes.datetimes.DatetimeIndex.std`
* `pandas.core.indexes.timedeltas.TimedeltaIndex.mean`
* `pandas.core.resample.Resampler.asfreq`
* `pandas.core.resample.Resampler.quantile`
* `pandas.core.series.Series.map`
* `pandas.core.series.Series.tz_convert`
* `pandas.core.series.Series.tz_localize`
* `pandas.core.window.expanding.Expanding.count`
* `pandas.core.window.rolling.Rolling.count`
* `pandas.core.groupby.generic.DataFrameGroupBy.aggregate`
* `pandas.core.groupby.generic.SeriesGroupBy.aggregate`
* `pandas.core.frame.DataFrame.applymap`
* `pandas.core.series.Series.apply`
* `pandas.core.groupby.generic.DataFrameGroupBy.bfill`
* `pandas.core.groupby.generic.DataFrameGroupBy.ffill`
* `pandas.core.groupby.generic.SeriesGroupBy.bfill`
* `pandas.core.groupby.generic.SeriesGroupBy.ffill`
* `pandas.core.frame.DataFrame.backfill`
* `pandas.core.frame.DataFrame.bfill`
* `pandas.core.frame.DataFrame.compare`
* `pandas.core.frame.DataFrame.unstack`
* `pandas.core.frame.DataFrame.asfreq`
* `pandas.core.series.Series.backfill`
* `pandas.core.series.Series.bfill`
* `pandas.core.series.Series.compare`
* `pandas.core.series.Series.unstack`
* `pandas.core.series.Series.asfreq`
* `pandas.core.series.Series.argmax`
* `pandas.core.series.Series.argmin`
* `pandas.core.indexes.accessors.CombinedDatetimelikeProperties.microsecond`
* `pandas.core.indexes.accessors.CombinedDatetimelikeProperties.nanosecond`
* `pandas.core.indexes.accessors.CombinedDatetimelikeProperties.day_name`
* `pandas.core.indexes.accessors.CombinedDatetimelikeProperties.month_name`
* `pandas.core.indexes.accessors.CombinedDatetimelikeProperties.month_start`
* `pandas.core.indexes.accessors.CombinedDatetimelikeProperties.month_end`
* `pandas.core.indexes.accessors.CombinedDatetimelikeProperties.is_year_start`
* `pandas.core.indexes.accessors.CombinedDatetimelikeProperties.is_year_end`
* `pandas.core.indexes.accessors.CombinedDatetimelikeProperties.is_quarter_start`
* `pandas.core.indexes.accessors.CombinedDatetimelikeProperties.is_quarter_end`
* `pandas.core.indexes.accessors.CombinedDatetimelikeProperties.is_leap_year`
* `pandas.core.indexes.accessors.CombinedDatetimelikeProperties.floor`
* `pandas.core.indexes.accessors.CombinedDatetimelikeProperties.ceil`
* `pandas.core.groupby.generic.DataFrameGroupBy.idxmax`
* `pandas.core.groupby.generic.DataFrameGroupBy.idxmin`
* `pandas.core.groupby.generic.DataFrameGroupBy.std`
* `pandas.core.indexes.timedeltas.TimedeltaIndex.mean`
* `pandas.core.tools.timedeltas.to_timedelta`

#### Known Issue[¶](#known-issue "Link to this heading")

* **This version includes an issue when converting the sample project will not work on this version, it** will be fixed on the next release

## Version 2.4.3 (Jan 9, 2025)[¶](#version-2-4-3-jan-9-2025 "Link to this heading")

### Application & CLI Version 2.4.3[¶](#application-cli-version-2-4-3 "Link to this heading")

#### Desktop App[¶](#id85 "Link to this heading")

* Added link to the troubleshooting guide in the crash report modal.

#### Included SMA Core Versions[¶](#id86 "Link to this heading")

* Snowpark Conversion Core 4.15.0

#### Added[¶](#id87 "Link to this heading")

* Added the following PySpark elements to ConversionStatusPySpark.csv file as `NotSupported:`

  + `pyspark.sql.streaming.readwriter.DataStreamReader.table`
  + `pyspark.sql.streaming.readwriter.DataStreamReader.schema`
  + `pyspark.sql.streaming.readwriter.DataStreamReader.options`
  + `pyspark.sql.streaming.readwriter.DataStreamReader.option`
  + `pyspark.sql.streaming.readwriter.DataStreamReader.load`
  + `pyspark.sql.streaming.readwriter.DataStreamReader.format`
  + `pyspark.sql.streaming.query.StreamingQuery.awaitTermination`
  + `pyspark.sql.streaming.readwriter.DataStreamWriter.partitionBy`
  + `pyspark.sql.streaming.readwriter.DataStreamWriter.toTable`
  + `pyspark.sql.streaming.readwriter.DataStreamWriter.trigger`
  + `pyspark.sql.streaming.readwriter.DataStreamWriter.queryName`
  + `pyspark.sql.streaming.readwriter.DataStreamWriter.outputMode`
  + `pyspark.sql.streaming.readwriter.DataStreamWriter.format`
  + `pyspark.sql.streaming.readwriter.DataStreamWriter.option`
  + `pyspark.sql.streaming.readwriter.DataStreamWriter.foreachBatch`
  + `pyspark.sql.streaming.readwriter.DataStreamWriter.start`

#### Changed[¶](#id88 "Link to this heading")

* Updated Hive SQL EWIs format.

  + SPRKHVSQL1001
  + SPRKHVSQL1002
  + SPRKHVSQL1003
  + SPRKHVSQL1004
  + SPRKHVSQL1005
  + SPRKHVSQL1006
* Updated Spark SQL EWIs format.

  + SPRKSPSQL1001
  + SPRKSPSQL1002
  + SPRKSPSQL1003
  + SPRKSPSQL1004
  + SPRKSPSQL1005
  + SPRKSPSQL1006

#### Fixed[¶](#id89 "Link to this heading")

* Fixed a bug that was causing some PySpark elements not identified by the tool.
* Fixed the mismatch in the ThirdParty identified calls and the ThirdParty import Calls number.

## Version 2.4.2 (Dec 13, 2024)[¶](#version-2-4-2-dec-13-2024 "Link to this heading")

### Application & CLI **Version 2.4.2**[¶](#application-cli-version-2-4-2 "Link to this heading")

#### Included SMA Core Versions[¶](#id90 "Link to this heading")

* Snowpark Conversion Core 4.14.0

#### Added added[¶](#added-added "Link to this heading")

* Added the following Spark elements to ConversionStatusPySpark.csv:

  + `pyspark.broadcast.Broadcast.value`
  + `pyspark.conf.SparkConf.getAll`
  + `pyspark.conf.SparkConf.setAll`
  + `pyspark.conf.SparkConf.setMaster`
  + `pyspark.context.SparkContext.addFile`
  + `pyspark.context.SparkContext.addPyFile`
  + `pyspark.context.SparkContext.binaryFiles`
  + `pyspark.context.SparkContext.setSystemProperty`
  + `pyspark.context.SparkContext.version`
  + `pyspark.files.SparkFiles`
  + `pyspark.files.SparkFiles.get`
  + `pyspark.rdd.RDD.count`
  + `pyspark.rdd.RDD.distinct`
  + `pyspark.rdd.RDD.reduceByKey`
  + `pyspark.rdd.RDD.saveAsTextFile`
  + `pyspark.rdd.RDD.take`
  + `pyspark.rdd.RDD.zipWithIndex`
  + `pyspark.sql.context.SQLContext.udf`
  + `pyspark.sql.types.StructType.simpleString`

#### Changed[¶](#id91 "Link to this heading")

* Updated the documentation of the Pandas EWIs, `PNDSPY1001`, `PNDSPY1002` and `PNDSPY1003` `SPRKSCL1137` to align with a standardized format, ensuring consistency and clarity across all the EWIs.
* Updated the documentation of the following Scala EWIs: `SPRKSCL1106` and `SPRKSCL1107`. To be aligned with a standardized format, ensuring consistency and clarity across all the EWIs.

#### Fixed[¶](#id92 "Link to this heading")

* Fixed the bug the was causing the UserDefined symbols showing in the third party usages inventory.

## Version 2.4.1 (Dec 4, 2024)[¶](#version-2-4-1-dec-4-2024 "Link to this heading")

### Application & CLI **Version 2.4.1**[¶](#application-cli-version-2-4-1 "Link to this heading")

#### Included SMA Core Versions[¶](#id93 "Link to this heading")

* Snowpark Conversion Core 4.13.1

#### Command Line Interface[¶](#command-line-interface "Link to this heading")

**Changed**

* Added timestamp to the output folder.

### Snowpark Conversion Core 4.13.1[¶](#snowpark-conversion-core-4-13-1 "Link to this heading")

#### Added[¶](#id94 "Link to this heading")

* Added ‘Source Language’ column to Library Mappings Table
* Added `Others` as a new category in the Pandas API Summary table of the DetailedReport.docx

#### Changed[¶](#id95 "Link to this heading")

* Updated the documentation for Python EWI `SPRKPY1058`.
* Updated the message for the pandas EWI `PNDSPY1002` to show the relate pandas element.
* Updated the way we created the .csv reports, now are overwritten after a second run .

#### Fixed[¶](#id96 "Link to this heading")

* Fixed a bug that was causing Notebook files not being generated in the output.
* Fixed the replacer for `get` and `set` methods from `pyspark.sql.conf.RuntimeConfig`, the replacer now match the correct full names.
* Fixed query tag incorrect version.
* Fixed UserDefined packages reported as ThirdPartyLib.

\

## Version 2.3.1 (Nov 14, 2024)[¶](#version-2-3-1-nov-14-2024 "Link to this heading")

### Application & CLI **Version 2.3.1**[¶](#application-cli-version-2-3-1 "Link to this heading")

#### Included SMA Core Versions[¶](#id97 "Link to this heading")

* Snowpark Conversion Core 4.12.0

#### Desktop App[¶](#id98 "Link to this heading")

**Fixed**

* Fix case-sensitive issues in –sql options.

**Removed**

* Remove platform name from show-ac message.

### Snowpark Conversion Core 4.12.0[¶](#snowpark-conversion-core-4-12-0 "Link to this heading")

#### Added[¶](#id99 "Link to this heading")

* Added support for Snowpark Python 1.23.0 and 1.24.0.
* Added a new EWI for the `pyspark.sql.dataframe.DataFrame.writeTo` function. All the usages of this function will now have the EWI SPRKPY1087.

#### Changed[¶](#id100 "Link to this heading")

* Updated the documentation of the Scala EWIs from `SPRKSCL1137` to `SPRKSCL1156` to align with a standardized format, ensuring consistency and clarity across all the EWIs.
* Updated the documentation of the Scala EWIs from `SPRKSCL1117` to `SPRKSCL1136` to align with a standardized format, ensuring consistency and clarity across all the EWIs.
* Updated the message that is shown for the following EWIs:

  + SPRKPY1082
  + SPRKPY1083
* Updated the documentation of the Scala EWIs from `SPRKSCL1100` to `SPRKSCL1105`, from `SPRKSCL1108` to `SPRKSCL1116`; from `SPRKSCL1157` to `SPRKSCL1175`; to align with a standardized format, ensuring consistency and clarity across all the EWIs.
* Updated the mapping status of the following PySpark elements from **NotSupported** to **Direct** with EWI:

  + `pyspark.sql.readwriter.DataFrameWriter.option` => `snowflake.snowpark.DataFrameWriter.option`: All the usages of this function now have the EWI SPRKPY1088
  + `pyspark.sql.readwriter.DataFrameWriter.options` => `snowflake.snowpark.DataFrameWriter.options`: All the usages of this function now have the EWI SPRKPY1089
* Updated the mapping status of the following PySpark elements from **Workaround** to **Rename**:

  + `pyspark.sql.readwriter.DataFrameWriter.partitionBy` => `snowflake.snowpark.DataFrameWriter.partition_by`
* Updated EWI documentation: SPRKSCL1000, SPRKSCL1001, SPRKSCL1002, SPRKSCL1100, SPRKSCL1101, SPRKSCL1102, SPRKSCL1103, SPRKSCL1104, SPRKSCL1105.

#### Removed[¶](#removed "Link to this heading")

* Removed the `pyspark.sql.dataframe.DataFrameStatFunctions.writeTo` element from the conversion status, this element does not exist.

#### Deprecated[¶](#deprecated "Link to this heading")

* Deprecated the following EWI codes:

  + SPRKPY1081
  + SPRKPY1084

## Version 2.3.0 (Oct 30, 2024)[¶](#version-2-3-0-oct-30-2024 "Link to this heading")

### Application & CLI Version 2.3.0[¶](#application-cli-version-2-3-0 "Link to this heading")

* Snowpark Conversion Core 4.11.0

### Snowpark Conversion Core 4.11.0[¶](#snowpark-conversion-core-4-11-0 "Link to this heading")

#### Added[¶](#id101 "Link to this heading")

* Added a new column called `Url` to the `Issues.csv` file, which redirects to the corresponding EWI documentation.
* Added new EWIs for the following Spark elements:

  + [SPRKPY1082] pyspark.sql.readwriter.DataFrameReader.load
  + [SPRKPY1083] pyspark.sql.readwriter.DataFrameWriter.save
  + [SPRKPY1084] pyspark.sql.readwriter.DataFrameWriter.option
  + [SPRKPY1085] pyspark.ml.feature.VectorAssembler
  + [SPRKPY1086] pyspark.ml.linalg.VectorUDT
* Added 38 new Pandas elements:

  + pandas.core.frame.DataFrame.select
  + andas.core.frame.DataFrame.str
  + pandas.core.frame.DataFrame.str.replace
  + pandas.core.frame.DataFrame.str.upper
  + pandas.core.frame.DataFrame.to\_list
  + pandas.core.frame.DataFrame.tolist
  + pandas.core.frame.DataFrame.unique
  + pandas.core.frame.DataFrame.values.tolist
  + pandas.core.frame.DataFrame.withColumn
  + pandas.core.groupby.generic.\_SeriesGroupByScalar
  + pandas.core.groupby.generic.\_SeriesGroupByScalar[S1].agg
  + pandas.core.groupby.generic.\_SeriesGroupByScalar[S1].aggregate
  + pandas.core.indexes.datetimes.DatetimeIndex.year
  + pandas.core.series.Series.columns
  + pandas.core.tools.datetimes.to\_datetime.date
  + pandas.core.tools.datetimes.to\_datetime.dt.strftime
  + pandas.core.tools.datetimes.to\_datetime.strftime
  + pandas.io.parsers.readers.TextFileReader.apply
  + pandas.io.parsers.readers.TextFileReader.astype
  + pandas.io.parsers.readers.TextFileReader.columns
  + pandas.io.parsers.readers.TextFileReader.copy
  + pandas.io.parsers.readers.TextFileReader.drop
  + pandas.io.parsers.readers.TextFileReader.drop\_duplicates
  + pandas.io.parsers.readers.TextFileReader.fillna
  + pandas.io.parsers.readers.TextFileReader.groupby
  + pandas.io.parsers.readers.TextFileReader.head
  + pandas.io.parsers.readers.TextFileReader.iloc
  + pandas.io.parsers.readers.TextFileReader.isin
  + pandas.io.parsers.readers.TextFileReader.iterrows
  + pandas.io.parsers.readers.TextFileReader.loc
  + pandas.io.parsers.readers.TextFileReader.merge
  + pandas.io.parsers.readers.TextFileReader.rename
  + pandas.io.parsers.readers.TextFileReader.shape
  + pandas.io.parsers.readers.TextFileReader.to\_csv
  + pandas.io.parsers.readers.TextFileReader.to\_excel
  + pandas.io.parsers.readers.TextFileReader.unique
  + pandas.io.parsers.readers.TextFileReader.values
  + pandas.tseries.offsets

## Version 2.2.3 (Oct 24, 2024)[¶](#version-2-2-3-oct-24-2024 "Link to this heading")

### Application Version 2.2.3[¶](#application-version-2-2-3 "Link to this heading")

#### Included SMA Core Versions[¶](#id102 "Link to this heading")

* Snowpark Conversion Core 4.10.0

#### Desktop App[¶](#id103 "Link to this heading")

#### Fixed[¶](#id104 "Link to this heading")

* Fixed a bug that caused the SMA to show the label **SnowConvert** instead of **Snowpark Migration Accelerator** in the menu bar of the Windows version.
* Fixed a bug that caused the SMA to crash when it did not have read and write permissions to the `.config` directory in macOS and the `AppData` directory in Windows.

#### Command Line Interface[¶](#id105 "Link to this heading")

**Changed**

* Renamed the CLI executable name from `snowct` to `sma`.
* Removed the source language argument so you no longer need to specify if you are running a Python or Scala assessment / conversion.
* Expanded the command line arguments supported by the CLI by adding the following new arguments:

  + `--enableJupyter` | `-j`: Flag to indicate if the conversion of Databricks notebooks to Jupyter is enabled or not.
  + `--sql` | `-f`: Database engine syntax to be used when a SQL command is detected.
  + `--customerEmail` | `-e`: Configure the customer email.
  + `--customerCompany` | `-c`: Configure the customer company.
  + `--projectName` | `-p`: Configure the customer project.
* Updated some texts to reflect the correct name of the application, ensuring consistency and clarity in all the messages.
* Updated the terms of use of the application.
* Updated and expanded the documentation of the CLI to reflect the latests features, enhancements and changes.
* Updated the text that is shown before proceeding with the execution of the SMA to improve
* Updated the CLI to accept **“Yes”** as a valid argument when prompting for user confirmation.
* Allowed the CLI to continue the execution without waiting for user interaction by specifying the argument `-y` or `--yes`.
* Updated the help information of the `--sql` argument to show the values that this argument expects.

### Snowpark Conversion Core Version 4.10.0[¶](#snowpark-conversion-core-version-4-10-0 "Link to this heading")

#### Added[¶](#id106 "Link to this heading")

* Added a new EWI for the `pyspark.sql.readwriter.DataFrameWriter.partitionBy` function. All the usages of this function will now have the EWI SPRKPY1081.
* Added a new column called `Technology` to the `ImportUsagesInventory.csv` file.

#### Changed[¶](#id107 "Link to this heading")

* Updated the Third-Party Libraries readiness score to also take into account the `Unknown` libraries.
* Updated the `AssessmentFiles.zip` file to include `.json` files instead of `.pam` files.
* Improved the CSV to JSON conversion mechanism to make processing of inventories more performant.
* Improved the documentation of the following EWIs:

  + SPRKPY1029
  + SPRKPY1054
  + SPRKPY1055
  + SPRKPY1063
  + SPRKPY1075
  + SPRKPY1076
* Updated the mapping status of the following Spark Scala elements from `Direct` to `Rename`.

  + `org.apache.spark.sql.functions.shiftLeft` => `com.snowflake.snowpark.functions.shiftleft`
  + `org.apache.spark.sql.functions.shiftRight` => `com.snowflake.snowpark.functions.shiftright`
* Updated the mapping status of the following Spark Scala elements from `Not Supported` to `Direct`.

  + `org.apache.spark.sql.functions.shiftleft` => `com.snowflake.snowpark.functions.shiftleft`
  + `org.apache.spark.sql.functions.shiftright` => `com.snowflake.snowpark.functions.shiftright`

#### Fixed[¶](#id108 "Link to this heading")

* Fixed a bug that caused the SMA to incorrectly populate the `Origin` column of the `ImportUsagesInventory.csv` file.
* Fixed a bug that caused the SMA to not classify imports of the libraries `io`, `json`, `logging` and `unittest` as Python built-in imports in the `ImportUsagesInventory.csv` file and in the `DetailedReport.docx` file.

## Version 2.2.2 (Oct 11, 2024)[¶](#version-2-2-2-oct-11-2024 "Link to this heading")

### Application Version 2.2.2[¶](#application-version-2-2-2 "Link to this heading")

Features Updates include:

* Snowpark Conversion Core 4.8.0

### Snowpark Conversion Core Version 4.8.0[¶](#snowpark-conversion-core-version-4-8-0 "Link to this heading")

#### Added[¶](#id109 "Link to this heading")

* Added `EwiCatalog.csv` and .md files to reorganize documentation
* Added the mapping status of `pyspark.sql.functions.ln` Direct.
* Added a transformation for `pyspark.context.SparkContext.getOrCreate`

  + Please check the EWI SPRKPY1080 for further details.
* Added an improvement for the SymbolTable, infer type for parameters in functions.
* Added SymbolTable supports static methods and do not assume the first parameter will be self for them.
* Added documentation for missing EWIs

  + SPRKHVSQL1005
  + SPRKHVSQL1006
  + SPRKSPSQL1005
  + SPRKSPSQL1006
  + SPRKSCL1002
  + SPRKSCL1170
  + SPRKSCL1171
  + SPRKPY1057
  + SPRKPY1058
  + SPRKPY1059
  + SPRKPY1060
  + SPRKPY1061
  + SPRKPY1064
  + SPRKPY1065
  + SPRKPY1066
  + SPRKPY1067
  + SPRKPY1069
  + SPRKPY1070
  + SPRKPY1077
  + SPRKPY1078
  + SPRKPY1079
  + SPRKPY1101

#### Changed[¶](#id110 "Link to this heading")

* Updated the mapping status of:

  + `pyspark.sql.functions.array_remove` from `NotSupported` to `Direct`.

#### Fixed[¶](#id111 "Link to this heading")

* Fixed the Code File Sizing table in the Detail Report to exclude .sql and .hql files and added the Extra Large row in the table.
* Fixed missing the `update_query_tag` when `SparkSession` is defined into multiple lines on `Python`.
* Fixed missing the `update_query_tag` when `SparkSession` is defined into multiple lines on `Scala`.
* Fixed missing EWI `SPRKHVSQL1001` to some SQL statements with parsing errors.
* Fixed keep new lines values inside string literals
* Fixed the Total Lines of code showed in the File Type Summary Table
* Fixed Parsing Score showed as 0 when recognize files successfully
* Fixed LOC count in the cell inventory for Databricks Magic SQL Cells

## Version 2.2.0 (Sep 26, 2024)[¶](#version-2-2-0-sep-26-2024 "Link to this heading")

### Application Version 2.2.0[¶](#application-version-2-2-0 "Link to this heading")

Feature Updates include:

* Snowpark Conversion Core 4.6.0

### Snowpark Conversion Core Version 4.6.0[¶](#snowpark-conversion-core-version-4-6-0 "Link to this heading")

#### Added[¶](#id112 "Link to this heading")

* Add transformation for `pyspark.sql.readwriter.DataFrameReader.parquet`.
* Add transformation for `pyspark.sql.readwriter.DataFrameReader.option` when it is a Parquet method.

#### Changed[¶](#id113 "Link to this heading")

* Updated the mapping status of:

  + `pyspark.sql.types.StructType.fields` from `NotSupported` to `Direct`.
  + `pyspark.sql.types.StructType.names` from `NotSupported` to `Direct`.
  + `pyspark.context.SparkContext.setLogLevel` from `Workaround` to `Transformation`.

    - More detail can be found in EWIs SPRKPY1078 and SPRKPY1079
  + `org.apache.spark.sql.functions.round` from `WorkAround` to `Direct`.
  + `org.apache.spark.sql.functions.udf` from `NotDefined` to `Transformation`.

    - More detail can be found in EWIs SPRKSCL1174 and SPRKSCL1175
* Updated the mapping status of the following Spark elements from `DirectHelper` to `Direct`:

  + `org.apache.spark.sql.functions.hex`
  + `org.apache.spark.sql.functions.unhex`
  + `org.apache.spark.sql.functions.shiftleft`
  + `org.apache.spark.sql.functions.shiftright`
  + `org.apache.spark.sql.functions.reverse`
  + `org.apache.spark.sql.functions.isnull`
  + `org.apache.spark.sql.functions.unix_timestamp`
  + `org.apache.spark.sql.functions.randn`
  + `org.apache.spark.sql.functions.signum`
  + `org.apache.spark.sql.functions.sign`
  + `org.apache.spark.sql.functions.collect_list`
  + `org.apache.spark.sql.functions.log10`
  + `org.apache.spark.sql.functions.log1p`
  + `org.apache.spark.sql.functions.base64`
  + `org.apache.spark.sql.functions.unbase64`
  + `org.apache.spark.sql.functions.regexp_extract`
  + `org.apache.spark.sql.functions.expr`
  + `org.apache.spark.sql.functions.date_format`
  + `org.apache.spark.sql.functions.desc`
  + `org.apache.spark.sql.functions.asc`
  + `org.apache.spark.sql.functions.size`
  + `org.apache.spark.sql.functions.locate`
  + `org.apache.spark.sql.functions.ntile`

#### Fixed[¶](#id114 "Link to this heading")

* Fixed value showed in the Percentage of total Pandas Api
* Fixed Total percentage on ImportCalls table in the DetailReport

### Deprecated[¶](#id115 "Link to this heading")

* Deprecated the following EWI code:

  + SPRKSCL1115

## Version 2.1.7 (Sep 12, 2024)[¶](#version-2-1-7-sep-12-2024 "Link to this heading")

### Application Version 2.1.7[¶](#application-version-2-1-7 "Link to this heading")

Feature Updates include:

* Snowpark Conversion Core 4.5.7
* Snowpark Conversion Core 4.5.2

### Snowpark Conversion Core Version 4.5.7[¶](#snowpark-conversion-core-version-4-5-7 "Link to this heading")

#### Hotfixed[¶](#hotfixed "Link to this heading")

* Fixed Total row added on Spark Usages Summaries when there are not usages
* Bumped of Python Assembly to Version=`1.3.111`

  + Parse trail comma in multiline arguments

### Snowpark Conversion Core Version 4.5.2[¶](#snowpark-conversion-core-version-4-5-2 "Link to this heading")

#### Added[¶](#id116 "Link to this heading")

* Added transformation for `pyspark.sql.readwriter.DataFrameReader.option`:

  + When the chain is from a CSV method call.
  + When the chain is from a JSON method call.
* Added transformation for `pyspark.sql.readwriter.DataFrameReader.json`.

#### Changed[¶](#id117 "Link to this heading")

* Executed SMA on SQL strings passed to Python/Scala functions

  + Create AST in Scala/Python to emit temporary SQL unit
  + Create SqlEmbeddedUsages.csv inventory
  + Deprecate SqlStatementsInventroy.csv and SqlExtractionInventory.csv
  + Integrate EWI when the SQL literal could not be processed
  + Create new task to process SQL-embedded code
  + Collect info for SqlEmbeddedUsages.csv inventory in Python
  + Replace SQL transformed code to Literal in Python
  + Update test cases after implementation
  + Create table, views for telemetry in SqlEmbeddedUsages inventory
  + Collect info for SqlEmbeddedUsages.csv report in Scala
  + Replace SQL transformed code to Literal in Scala
  + Check line number order for Embedded SQL reporting
* Filled the `SqlFunctionsInfo.csv` with the SQL functions documented for SparkSQL and HiveSQL
* Updated the mapping status for:

  + `org.apache.spark.sql.SparkSession.sparkContext` from NotSupported to Transformation.
  + `org.apache.spark.sql.Builder.config` from `NotSupported` to `Transformation`. With this new mapping status, the SMA will remove all the usages of this function from the source code.

## Version 2.1.6 (Sep 5, 2024)[¶](#version-2-1-6-sep-5-2024 "Link to this heading")

### Application Version 2.1.6[¶](#application-version-2-1-6 "Link to this heading")

* Hotfix change for Snowpark Engines Core version 4.5.1

### Spark Conversion Core Version 4.5.1[¶](#spark-conversion-core-version-4-5-1 "Link to this heading")

**Hotfix**

* Added a mechanism to convert the temporal Databricks notebooks generated by SMA in exported Databricks notebooks

## Version 2.1.5 (Aug 29, 2024)[¶](#version-2-1-5-aug-29-2024 "Link to this heading")

### Application Version 2.1.5[¶](#application-version-2-1-5 "Link to this heading")

Feature Updates include:

* Updated Spark Conversion Core: 4.3.2

### Spark Conversion Core Version 4.3.2[¶](#spark-conversion-core-version-4-3-2 "Link to this heading")

#### Added[¶](#id118 "Link to this heading")

* Added the mechanism (via decoration) to get the line and the column of the elements identified in notebooks cells
* Added an EWI for pyspark.sql.functions.from\_json.
* Added a transformation for pyspark.sql.readwriter.DataFrameReader.csv.
* Enabled the query tag mechanism for Scala files.
* Added the Code Analysis Score and additional links to the Detailed Report.
* Added a column called OriginFilePath to InputFilesInventory.csv

#### Changed[¶](#id119 "Link to this heading")

* Updated the mapping status of pyspark.sql.functions.from\_json from Not Supported to Transformation.
* Updated the mapping status of the following Spark elements from Workaround to Direct:

  + org.apache.spark.sql.functions.countDistinct
  + org.apache.spark.sql.functions.max
  + org.apache.spark.sql.functions.min
  + org.apache.spark.sql.functions.mean

#### Deprecated[¶](#id120 "Link to this heading")

* Deprecated the following EWI codes:

  + SPRKSCL1135
  + SPRKSCL1136
  + SPRKSCL1153
  + SPRKSCL1155

#### Fixed[¶](#id121 "Link to this heading")

* Fixed a bug that caused an incorrect calculation of the Spark API score.
* Fixed an error that avoid copy SQL empty or commented files in the output folder.
* Fixed a bug in the DetailedReport, the notebook stats LOC and Cell count is not accurate.

## Version 2.1.2 (Aug 14, 2024)[¶](#version-2-1-2-aug-14-2024 "Link to this heading")

### Application Version 2.1.2[¶](#application-version-2-1-2 "Link to this heading")

Feature Updates include:

* Updated Spark Conversion Core: 4.2.0

### Spark Conversion Core Version 4.2.0[¶](#spark-conversion-core-version-4-2-0 "Link to this heading")

#### Added[¶](#id122 "Link to this heading")

* Add technology column to SparkUsagesInventory
* Added an EWI for not defined SQL elements .
* Added SqlFunctions Inventory
* Collect info for SqlFunctions Inventory

#### Changed[¶](#id123 "Link to this heading")

* The engine now processes and prints partially parsed Python files instead of leaving original file without modifications.
* Python notebook cells that have parsing errors will also be processed and printed.

#### Fixed[¶](#id124 "Link to this heading")

* Fixed `pandas.core.indexes.datetimes.DatetimeIndex.strftime` was being reported wrongly.
* Fix mismatch between SQL readiness score and SQL Usages by Support Status.
* Fixed a bug that caused the SMA to report `pandas.core.series.Series.empty` with an incorrect mapping status.
* Fix mismatch between Spark API Usages Ready for Conversion in DetailedReport.docx is different than UsagesReadyForConversion row in Assessment.json.

## Version 2.1.1 (Aug 8, 2024)[¶](#version-2-1-1-aug-8-2024 "Link to this heading")

### Application Version 2.1.1[¶](#application-version-2-1-1 "Link to this heading")

Feature Updates include:

* Updated Spark Conversion Core: 4.1.0

### Spark Conversion Core Version 4.1.0[¶](#spark-conversion-core-version-4-1-0 "Link to this heading")

#### Added[¶](#id125 "Link to this heading")

* Added the following information to the `AssessmentReport.json` file

  + The third-party libraries readiness score.
  + The number of third-party library calls that were identified.
  + The number of third-party library calls that are supported in Snowpark.
  + The color code associated with the third-party readiness score, the Spark API readiness score, and the SQL readiness score.
* Transformed `SqlSimpleDataType` in Spark create tables.
* Added the mapping of `pyspark.sql.functions.get` as direct.
* Added the mapping of `pyspark.sql.functions.to_varchar` as direct.
* As part of the changes after unification, the tool now generates an execution info file in the Engine.
* Added a replacer for `pyspark.sql.SparkSession.builder.appName`.

#### Changed[¶](#id126 "Link to this heading")

* Updated the mapping status for the following Spark elements

  + From Not Supported to Direct mapping:

    - `pyspark.sql.functions.sign`
    - `pyspark.sql.functions.signum`
* Changed the Notebook Cells Inventory report to indicate the kind of content for every cell in the column Element
* Added a `SCALA_READINESS_SCORE` column that reports the readiness score as related only to references to the Spark API in Scala files.
* Partial support to transform table properties in `ALTER TABLE` and `ALTER VIEW`
* Updated the conversion status of the node `SqlSimpleDataType` from Pending to Transformation in Spark create tables
* Updated the version of the Snowpark Scala API supported by the SMA from `1.7.0` to `1.12.1`:

  + Updated the mapping status of:

    - `org.apache.spark.sql.SparkSession.getOrCreate` from Rename to Direct
    - `org.apache.spark.sql.functions.sum` from Workaround to Direct
* Updated the version of the Snowpark Python API supported by the SMA from `1.15.0` to `1.20.0`:

  + Updated the mapping status of:

    - `pyspark.sql.functions.arrays_zip` from Not Supported to Direct
* Updated the mapping status for the following Pandas elements:

  + Direct mappings:

    - `pandas.core.frame.DataFrame.any`
    - `pandas.core.frame.DataFrame.applymap`
* Updated the mapping status for the following Pandas elements:

  + From Not Supported to Direct mapping:

    - `pandas.core.frame.DataFrame.groupby`
    - `pandas.core.frame.DataFrame.index`
    - `pandas.core.frame.DataFrame.T`
    - `pandas.core.frame.DataFrame.to_dict`
  + From Not Supported to Rename mapping:

    - `pandas.core.frame.DataFrame.map`
* Updated the mapping status for the following Pandas elements:

  + Direct mappings:

    - `pandas.core.frame.DataFrame.where`
    - `pandas.core.groupby.generic.SeriesGroupBy.agg`
    - `pandas.core.groupby.generic.SeriesGroupBy.aggregate`
    - `pandas.core.groupby.generic.DataFrameGroupBy.agg`
    - `pandas.core.groupby.generic.DataFrameGroupBy.aggregate`
    - `pandas.core.groupby.generic.DataFrameGroupBy.apply`
  + Not Supported mappings:

    - `pandas.core.frame.DataFrame.to_parquet`
    - `pandas.core.generic.NDFrame.to_csv`
    - `pandas.core.generic.NDFrame.to_excel`
    - `pandas.core.generic.NDFrame.to_sql`
* Updated the mapping status for the following Pandas elements:

  + Direct mappings:

    - `pandas.core.series.Series.empty`
    - `pandas.core.series.Series.apply`
    - `pandas.core.reshape.tile.qcut`
  + Direct mappings with EWI:

    - `pandas.core.series.Series.fillna`
    - `pandas.core.series.Series.astype`
    - `pandas.core.reshape.melt.melt`
    - `pandas.core.reshape.tile.cut`
    - `pandas.core.reshape.pivot.pivot_table`
* Updated the mapping status for the following Pandas elements:

  + Direct mappings:

    - `pandas.core.series.Series.dt`
    - `pandas.core.series.Series.groupby`
    - `pandas.core.series.Series.loc`
    - `pandas.core.series.Series.shape`
    - `pandas.core.tools.datetimes.to_datetime`
    - `pandas.io.excel._base.ExcelFile`
  + Not Supported mappings:

    - `pandas.core.series.Series.dt.strftime`
* Updated the mapping status for the following Pandas elements:

  + From Not Supported to Direct mapping:

    - `pandas.io.parquet.read_parquet`
    - `pandas.io.parsers.readers.read_csv`
* Updated the mapping status for the following Pandas elements:

  + From Not Supported to Direct mapping:

    - `pandas.io.pickle.read_pickle`
    - `pandas.io.sql.read_sql`
    - `pandas.io.sql.read_sql_query`
* Updated the description of Understanding the SQL Readiness Score.
* Updated `PyProgramCollector` to collect the packages and populate the current packages inventory with data from Python source code.
* Updated the mapping status of `pyspark.sql.SparkSession.builder.appName` from Rename to Transformation.
* Removed the following Scala integration tests:

  + `AssesmentReportTest_AssessmentMode.ValidateReports_AssessmentMode`
  + `AssessmentReportTest_PythonAndScala_Files.ValidateReports_PythonAndScala`
  + `AssessmentReportTestWithoutSparkUsages.ValidateReports_WithoutSparkUsages`
* Updated the mapping status of `pandas.core.generic.NDFrame.shape` from Not Supported to Direct.
* Updated the mapping status of `pandas.core.series` from Not Supported to Direct.

#### Deprecated[¶](#id127 "Link to this heading")

* Deprecated the EWI code `SPRKSCL1160` since `org.apache.spark.sql.functions.sum` is now a direct mapping.

#### Fixed[¶](#id128 "Link to this heading")

* Fixed a bug by not supporting Custom Magics without arguments in Jupyter Notebook cells.
* Fixed incorrect generation of EWIs in the issues.csv report when parsing errors occur.
* Fixed a bug that caused the SMA not to process the Databricks exported notebook as Databricks notebooks.
* Fixed a stack overflow error while processing clashing type names of declarations created inside package objects.
* Fixed the processing of complex lambda type names involving generics, e.g., `def func[X,Y](f: (Map[Option[X], Y] => Map[Y, X]))...`
* Fixed a bug that caused the SMA to add a PySpark EWI code instead of a Pandas EWI code to the Pandas elements that are not yet recognized.
* Fixed a typo in the detailed report template: renaming a column from “Percentage of all Python Files” to “Percentage of all files”.
* Fixed a bug where `pandas.core.series.Series.shape` was wrongly reported.

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

1. [Version 2.11.0 (January 9, 2026)](#version-2-11-0-january-9-2026)
2. [Version 2.10.5 (December 3rd, 2025)](#version-2-10-5-december-3rd-2025)
3. [Version 2.10.4 (November 18, 2025)](#version-2-10-4-november-18-2025)
4. [Version 2.10.3 (October 30, 2025)](#version-2-10-3-october-30-2025)
5. [Version 2.10.2 (Oct 27, 2025)](#version-2-10-2-oct-27-2025)
6. [Version 2.10.1 (Oct 23, 2025)](#version-2-10-1-oct-23-2025)
7. [Version 2.10.0 (Sep 24, 2025)](#version-2-10-0-sep-24-2025)
8. [Version 2.7.7 (Aug 28, 2025)](#version-2-7-7-aug-28-2025)
9. [Version 2.9.0 (Sep 09, 2025)](#version-2-9-0-sep-09-2025)
10. [Version 2.7.6 (Jul 17, 2025)](#version-2-7-6-jul-17-2025)
11. [Version 2.7.5 (Jul 2, 2025)](#version-2-7-5-jul-2-2025)
12. [Version 2.7.4 (Jun 26, 2025)](#version-2-7-4-jun-26-2025)
13. [Version 2.7.2 (Jun 10, 2025)](#version-2-7-2-jun-10-2025)
14. [Version 2.7.1 (Jun 9, 2025)](#version-2-7-1-jun-9-2025)
15. [Version 2.6.10 (May 5, 2025)](#version-2-6-10-may-5-2025)
16. [Version 2.6.8 (Apr 28, 2025)](#version-2-6-8-apr-28-2025)
17. [Version 2.6.7 (Apr 21, 2025)](#version-2-6-7-apr-21-2025)
18. [Version 2.6.6 (Apr 7, 2025)](#version-2-6-6-apr-7-2025)
19. [Version 2.6.5 (Mar 27, 2025)](#version-2-6-5-mar-27-2025)
20. [Version 2.6.4 (Mar 12, 2025)](#version-2-6-4-mar-12-2025)
21. [Version 2.6.3 (Mar 6, 2025)](#version-2-6-3-mar-6-2025)
22. [Version 2.6.0 (Feb 21, 2025)](#version-2-6-0-feb-21-2025)
23. [Version 2.5.2 (Feb 5, 2025)](#version-2-5-2-feb-5-2025)
24. [Version 2.5.1 (Feb 4, 2025)](#version-2-5-1-feb-4-2025)
25. [Version 2.4.3 (Jan 9, 2025)](#version-2-4-3-jan-9-2025)
26. [Version 2.4.2 (Dec 13, 2024)](#version-2-4-2-dec-13-2024)
27. [Version 2.4.1 (Dec 4, 2024)](#version-2-4-1-dec-4-2024)
28. [Version 2.3.1 (Nov 14, 2024)](#version-2-3-1-nov-14-2024)
29. [Version 2.3.0 (Oct 30, 2024)](#version-2-3-0-oct-30-2024)
30. [Version 2.2.3 (Oct 24, 2024)](#version-2-2-3-oct-24-2024)
31. [Version 2.2.2 (Oct 11, 2024)](#version-2-2-2-oct-11-2024)
32. [Version 2.2.0 (Sep 26, 2024)](#version-2-2-0-sep-26-2024)
33. [Version 2.1.7 (Sep 12, 2024)](#version-2-1-7-sep-12-2024)
34. [Version 2.1.6 (Sep 5, 2024)](#version-2-1-6-sep-5-2024)
35. [Version 2.1.5 (Aug 29, 2024)](#version-2-1-5-aug-29-2024)
36. [Version 2.1.2 (Aug 14, 2024)](#version-2-1-2-aug-14-2024)
37. [Version 2.1.1 (Aug 8, 2024)](#version-2-1-1-aug-8-2024)