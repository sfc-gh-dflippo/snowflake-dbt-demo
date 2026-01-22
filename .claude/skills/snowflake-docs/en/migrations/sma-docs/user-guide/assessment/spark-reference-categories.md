---
auto_generated: true
description: 'SnowConvert for Spark categorizes Spark elements based on how they can
  be mapped to Snowpark. The following categories describe how each Spark reference
  is translated, including:'
last_scraped: '2026-01-14T16:51:46.912111+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/sma-docs/user-guide/assessment/spark-reference-categories
title: 'Snowpark Migration Accelerator:  Spark Reference Categories | Snowflake Documentation'
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[Snowpark Migration Accelerator](../../README.md)User guide[Assessment](README.md)Spark reference categories

# Snowpark Migration Accelerator: Spark Reference Categories[¶](#snowpark-migration-accelerator-spark-reference-categories "Link to this heading")

SnowConvert for Spark categorizes Spark elements based on how they can be mapped to Snowpark. The following categories describe how each Spark reference is translated, including:

* Whether SnowConvert can automatically convert it
* Whether it’s possible to implement in Snowpark
  Also it provides
* Examples of the translation
* Description of the mapping process

The sections below explain each status type and provide examples.

## Direct[¶](#direct "Link to this heading")

Direct translation means the function works exactly the same way in both PySpark and Snowpark, requiring no modifications to the code.

* Snowpark Support: Available
* Tool Support: Available
* Spark Example:

```
col("col1")
```

Copy

* Snowpark Example:

```
col("col1")
```

Copy

## Rename[¶](#rename "Link to this heading")

The PySpark function has an equivalent in Snowpark, but you need to use a different function name.

* Snowpark Support: Available
* Tool Support: Available
* Spark Example:

```
orderBy("date")
```

Copy

* Snowpark Example:

```
sort("date")
```

Copy

## Helper[¶](#helper "Link to this heading")

Note

Starting from Spark Conversion Core V2.40.0, the Python extensions library is no longer supported. Python Spark elements will not be classified as extensions from this version onward. However, helper classes in the Snowpark extensions library will continue to be available for Spark Scala.

To address the difference between Spark and Snowpark functionality, you can create a helper function in an extension file. This helper function will have the same signature as the original Spark function and can be called from any file where needed. The extension library will contain this function to resolve the compatibility issue.

For more information about the Snowpark extensions library, visit our GitHub repository at <https://github.com/Snowflake-Labs/snowpark-extensions>.

Examples include fixed additional parameters and changes to parameter order.

* Snowpark Support: Available
* Tool Support: Available
* Spark Example:

```
instr(str, substr)
```

Copy

* Snowpark Example:

```
# creating a helper function named instr with an 
# identical signature as the pyspark function, like:

def instr(source: str, substr: str) -> str:
    """
    Returns the position of a substring within a source string.
    Similar to the CHARINDEX function in SQL.
    
    Args:
        source: The string to search in
        substr: The string to search for
        
    Returns:
        The position where the substring is found, or 0 if not found
    """
    return charindex(substr, str)

## Transformation

The function is rebuilt in Snowpark to achieve the same results as the original, though it may look different. The new version might use multiple functions or additional code lines to accomplish the same task.

* Snowpark Support: Yes
* Tool Support: Yes
* Spark Example:

```{code} python
:force:
col1 = col("col1")
col2 = col("col2")
col1.contains(col2)
```

Copy

* Snowpark Example:

```
col1 = col("col1")
col2 = col("col2")
from snowflake.snowpark.functions as f
f.contains(col, col2)
```

Copy

## WorkAround[¶](#workaround "Link to this heading")

This category applies when SMA cannot automatically convert a PySpark element, but there is a documented manual solution available in the tool’s documentation to help you complete the conversion.

* Snowpark Support: Available
* Tool Support: Not Available
* Spark Example:

```
instr(str, substr)
```

Copy

* Snowpark Example:

```
#EWI: SPRKPY#### => pyspark function has a workaround, see documentation for more info
charindex(substr, str)
```

Copy

## NotSupported[¶](#notsupported "Link to this heading")

This category applies when a PySpark element cannot be converted because there is no matching equivalent in Snowflake.

* Snowpark Support: Not Available
* Tool Support: Not Available
* Spark Example:

```
df:DataFrame = spark.createDataFrame(rowData, columns)
df.alias("d")
```

Copy

* Snowpark Example:

```
df:DataFrame = spark.createDataFrame(rowData, columns)
# EWI: SPRKPY11XX => DataFrame.alias is not supported
# df.alias("d")
```

Copy

## NotDefined[¶](#notdefined "Link to this heading")

This error occurs when the tool identifies a PySpark element but cannot convert it because the element is not included in the tool’s supported conversion database.

This category applies when a PySpark element cannot be converted because there is no corresponding feature or functionality in Snowflake.

* Snowpark Support: Not Available
* Tool Support: Not Available
* Spark Example: Not Applicable
* Snowpark Example: Not Applicable

The assessment results will classify all detected Spark API references into the following categories.

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

1. [Direct](#direct)
2. [Rename](#rename)
3. [Helper](#helper)
4. [WorkAround](#workaround)
5. [NotSupported](#notsupported)
6. [NotDefined](#notdefined)