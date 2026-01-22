---
auto_generated: true
description: The SMA-Checkpoints feature requires a PySpark workload as its entry
  point, since it depends on detecting the use of PySpark DataFrames. This walkthrough
  will guide you through the feature using a sin
last_scraped: '2026-01-14T16:52:06.399419+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/sma-docs/use-cases/sma-checkpoints-walkthrough/sma-execution-guide/README
title: 'Snowpark Migration Accelerator: SMA Execution Guide | Snowflake Documentation'
---

1. [Overview](../../../../../guides/README.md)
2. [Snowflake Horizon Catalog](../../../../../user-guide/snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../../../../../guides/overview-connecting.md)
6. [Virtual warehouses](../../../../../user-guide/warehouses.md)
7. [Databases, Tables, & Views](../../../../../guides/overview-db.md)
8. [Data types](../../../../../data-types.md)
10. Data Integration

    - [Snowflake Openflow](../../../../../user-guide/data-integration/openflow/about.md)
    - Apache Iceberg™

      - [Apache Iceberg™ Tables](../../../../../user-guide/tables-iceberg.md)
      - [Snowflake Open Catalog](../../../../../user-guide/opencatalog/overview.md)
11. Data engineering

    - [Data loading](../../../../../guides/overview-loading-data.md)
    - [Dynamic Tables](../../../../../user-guide/dynamic-tables-about.md)
    - [Streams and Tasks](../../../../../user-guide/data-pipelines-intro.md)
    - [dbt Projects on Snowflake](../../../../../user-guide/data-engineering/dbt-projects-on-snowflake.md)
    - [Data Unloading](../../../../../guides/overview-unloading-data.md)
12. [Storage Lifecycle Policies](../../../../../user-guide/storage-management/storage-lifecycle-policies.md)
13. [Migrations](../../../../README.md)

    * Tools

      * [SnowConvert AI](../../../../snowconvert-docs/overview.md)
      * [Snowpark Migration Accelerator](../../../README.md)

        + General

          + [Introduction](../../../general/introduction.md)
          + [Getting started](../../../general/getting-started/README.md)
          + [Conversion software terms of use](../../../general/conversion-software-terms-of-use/README.md)
          + [Release notes](../../../general/release-notes/README.md)
          + [Roadmap](../../../general/roadmap.md)
        + User guide

          + [Overview](../../../user-guide/overview.md)
          + [Before using the SMA](../../../user-guide/before-using-the-sma/README.md)
          + [Project overview](../../../user-guide/project-overview/README.md)
          + [Technical discovery](../../../user-guide/project-overview/optional-technical-discovery.md)
          + [AI assistant](../../../user-guide/chatbot.md)
          + [Assessment](../../../user-guide/assessment/README.md)
          + [Conversion](../../../user-guide/conversion/README.md)
          + [Using the SMA CLI](../../../user-guide/using-the-sma-cli/README.md)
        + Use cases

          + Snowflake VS Code extension

            + [SMA checkpoints walkthrough](../README.md)

              - [Prerequisites](../prerequisites.md)
              - [SMA execution guide](README.md)

                * [Feature settings](feature-settings/README.md)
                * [SMA checkpoints inventories](sma-checkpoints-inventories.md)
              - [Snowpark-checkpoints execution guide](../snowpark-checkpoints-execution-guide/README.md)
            + [SMA EWI Assistant walkthrough](../../sma-ewi-assistant-walkthrough/README.md)
          + [Assessment walkthrough](../../assessment-walkthrough/README.md)
          + [Conversion walkthrough](../../conversion-walkthrough.md)
          + [Migration lab](../../migration-lab/README.md)
          + [Sample project](../../sample-project.md)
          + [Using SMA in an Ubuntu Docker image](../../using-snowconvert-in-a-ubuntu-docker-image.md)
          + [SMA CLI walkthrough](../../sma-cli-walkthrough.md)
          + [Snowpark Connect](../../snowpark-connect/README.md)
        + Issue analysis

          + [Approach](../../../issue-analysis/approach.md)
          + [Issue code categorization](../../../issue-analysis/issue-code-categorization.md)
          + [Issue codes by source](../../../issue-analysis/issue-codes-by-source/README.md)
          + [Troubleshooting the output code](../../../issue-analysis/troubleshooting-the-output-code/README.md)
          + [Workarounds](../../../issue-analysis/workarounds.md)
          + [Deploying the output code](../../../issue-analysis/deploying-the-output-code.md)
        + Translation reference

          + [Translation reference overview](../../../translation-reference/translation-reference-overview.md)
          + [SIT tagging](../../../translation-reference/sit-tagging/README.md)
          + [SQL embedded code](../../../translation-reference/sql-embedded-code.md)
          + [HiveSQL](../../../translation-reference/hivesql/README.md)
          + [Spark SQL](../../../translation-reference/spark-sql/README.md)
        + Workspace estimator

          + [Overview](../../../workspace-estimator/overview.md)
          + [Getting started](../../../workspace-estimator/getting-started.md)
        + Interactive assessment application

          + [Overview](../../../interactive-assessment-application/overview.md)
          + [Installation guide](../../../interactive-assessment-application/installation-guide.md)
        + Support

          + [General troubleshooting](../../../support/general-troubleshooting/README.md)
          + [Frequently asked questions](../../../support/frequently-asked-questions-faq/README.md)
          + [Glossary](../../../support/glossary.md)
          + [Contact us](../../../support/contact-us.md)
    * Guides

      * [Teradata](../../../../guides/teradata.md)
      * [Databricks](../../../../guides/databricks.md)
      * [SQL Server](../../../../guides/sqlserver.md)
      * [Amazon Redshift](../../../../guides/redshift.md)
      * [Oracle](../../../../guides/oracle.md)
      * [Azure Synapse](../../../../guides/azuresynapse.md)
15. [Queries](../../../../../guides/overview-queries.md)
16. [Listings](../../../../../collaboration/collaboration-listings-about.md)
17. [Collaboration](../../../../../guides/overview-sharing.md)
19. [Snowflake AI & ML](../../../../../guides/overview-ai-features.md)
21. [Snowflake Postgres](../../../../../user-guide/snowflake-postgres/about.md)
23. [Alerts & Notifications](../../../../../guides/overview-alerts.md)
25. [Security](../../../../../guides/overview-secure.md)
26. [Data Governance](../../../../../guides/overview-govern.md)
27. [Privacy](../../../../../guides/overview-privacy.md)
29. [Organizations & Accounts](../../../../../guides/overview-manage.md)
30. [Business continuity & data recovery](../../../../../user-guide/replication-intro.md)
32. [Performance optimization](../../../../../guides/overview-performance.md)
33. [Cost & Billing](../../../../../guides/overview-cost.md)

[Guides](../../../../../guides/README.md)[Migrations](../../../../README.md)Tools[Snowpark Migration Accelerator](../../../README.md)Use casesSnowflake VS Code extension[SMA checkpoints walkthrough](../README.md)SMA execution guide

# Snowpark Migration Accelerator: SMA Execution Guide[¶](#snowpark-migration-accelerator-sma-execution-guide "Link to this heading")

## PySpark Input[¶](#pyspark-input "Link to this heading")

The SMA-Checkpoints feature requires a PySpark workload as its entry point, since it depends on detecting the use of PySpark DataFrames. This walkthrough will guide you through the feature using a single Python script, providing a straightforward example of how checkpoints are generated and utilized within a typical PySpark workflow.

**Input workload**

![Input workload](../../../../../_images/image%28560%29.png)

**Sample.py file content**

```
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.appName("SparkFunctionsExample2").getOrCreate()

df1 = spark.createDataFrame([("Alice", "NY"), ("Bob", "LA")], ["name", "city"])
df2 = spark.createDataFrame([(10,), (20,)], ["number"])

df1_with_index = df1.withColumn("index", F.monotonically_increasing_id())
df2_with_index = df2.withColumn("index", F.monotonically_increasing_id())

df3 = df1_with_index.join(df2_with_index, on="index").drop("index")
df3.show()
```

Copy

## **Migrating Workload**[¶](#migrating-workload "Link to this heading")

### Feature Enabled[¶](#feature-enabled "Link to this heading")

If the SMA-Checkpoints feature is enabled, a `checkpoints.json` file will be generated. If the feature is disabled, this file will not be created in either the input or output folders. Regardless of whether the feature is enabled, the following inventory files will always be generated: `DataFramesInventory.csv` and `CheckpointsInventory.csv`. These files provide metadata essential for analysis and debugging.

### Conversion Process[¶](#conversion-process "Link to this heading")

To create a convert your own project please follow up the following guide: [SMA User Guide](https://docs.snowconvert.com/sma/user-guide/overview).

#### SMA-Checkpoints Feature Settings[¶](#sma-checkpoints-feature-settings "Link to this heading")

As part of the conversion process you can customize your conversion settings, take a look on the [SMA-Checkpoints](https://app.gitbook.com/o/-MB4z_O8Sl--Tfl3XVml/s/6on4bNAZUZGzMpdEum8X/~/changes/499/use-cases/sma-checkpoints-walkthrough/usage-guide/feature-settings) feature settings.

**Note:** This user guide used the default conversion settings.

### Conversion Results[¶](#conversion-results "Link to this heading")

Once the migration process is complete, the SMA-Checkpoints feature should have created two new inventory files and added a `checkpoints.json` file to both the input and output folders.

Take a look on [SMA-Checkpoints inventories](https://app.gitbook.com/o/-MB4z_O8Sl--Tfl3XVml/s/t950HWwa5FvNA71Qes8u/) to review the related inventories.

#### Input Folder[¶](#input-folder "Link to this heading")

![Input folder](../../../../../_images/image%28567%29.png)

**checkpoints.json file content**

```
{
  "createdBy": "Snowpark Migration Accelerator",
  "comment": "This file was automatically generated by the SMA tool as checkpoints collection was enabled in the tool settings. This file may also be modified or deleted during SMA execution.",
  "type": "Collection",
  "pipelines": [
    {
      "entryPoint": "sample.py",
      "checkpoints": [
        {
          "name": "sample$BBVOC7$df1$1",
          "file": "sample.py",
          "df": "df1",
          "location": 1,
          "enabled": true,
          "mode": 1,
          "sample": "1.0"
        },
        {
          "name": "sample$BBVOC7$df2$1",
          "file": "sample.py",
          "df": "df2",
          "location": 1,
          "enabled": true,
          "mode": 1,
          "sample": "1.0"
        },
        {
          "name": "sample$BBVOC7$df3$1",
          "file": "sample.py",
          "df": "df3",
          "location": 1,
          "enabled": true,
          "mode": 1,
          "sample": "1.0"
        }
      ]
    }
  ]
}
```

Copy

#### Output Folder[¶](#output-folder "Link to this heading")

![Output folder](../../../../../_images/image%28568%29.png)

**checkpoints.json file content**

```
{
  "createdBy": "Snowpark Migration Accelerator",
  "comment": "This file was automatically generated by the SMA tool as checkpoints collection was enabled in the tool settings. This file may also be modified or deleted during SMA execution.",
  "type": "Validation",
  "pipelines": [
    {
      "entryPoint": "sample.py",
      "checkpoints": [
        {
          "name": "sample$BBVOC7$df1$1",
          "file": "sample.py",
          "df": "df1",
          "location": 1,
          "enabled": true,
          "mode": 1,
          "sample": "1.0"
        },
        {
          "name": "sample$BBVOC7$df2$1",
          "file": "sample.py",
          "df": "df2",
          "location": 1,
          "enabled": true,
          "mode": 1,
          "sample": "1.0"
        },
        {
          "name": "sample$BBVOC7$df3$1",
          "file": "sample.py",
          "df": "df3",
          "location": 1,
          "enabled": true,
          "mode": 1,
          "sample": "1.0"
        }
      ]
    }
  ]
}
```

Copy

Once the SMA execution flow is complete and both the input and output folders contain their respective `checkpoints.json` files, you are ready to begin the Snowpark-Checkpoints execution process.

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

1. [PySpark Input](#pyspark-input)
2. [Migrating Workload](#migrating-workload)