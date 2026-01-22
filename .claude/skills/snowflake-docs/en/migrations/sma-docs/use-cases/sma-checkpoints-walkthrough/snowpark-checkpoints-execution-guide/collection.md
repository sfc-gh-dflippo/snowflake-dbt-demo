---
auto_generated: true
description: 'To follow the collection process, please proceed with the steps outlined
  below:'
last_scraped: '2026-01-14T16:52:08.289830+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/sma-docs/use-cases/sma-checkpoints-walkthrough/snowpark-checkpoints-execution-guide/collection
title: 'Snowpark Migration Accelerator: Collection | Snowflake Documentation'
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
              - [SMA execution guide](../sma-execution-guide/README.md)
              - [Snowpark-checkpoints execution guide](README.md)

                * [Collection](collection.md)
                * [Validation](validation.md)
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

[Guides](../../../../../guides/README.md)[Migrations](../../../../README.md)Tools[Snowpark Migration Accelerator](../../../README.md)Use casesSnowflake VS Code extension[SMA checkpoints walkthrough](../README.md)[Snowpark-checkpoints execution guide](README.md)Collection

# Snowpark Migration Accelerator: Collection[¶](#snowpark-migration-accelerator-collection "Link to this heading")

To follow the collection process, please proceed with the steps outlined below:

1. Open the collection workload in VS Code to begin the process.

   ![Collection Workload](../../../../../_images/image%28574%29.png)
2. Generate checkpoints using the `checkpoints.json` file.

To generate checkpoints, you can perform one of the following actions:

1. Generate checkpoints by accepting the suggested message:

   ![Load found checkpoints message](../../../../../_images/image%28575%29.png)
2. Execute the “Snowflake: Load All Checkpoints” command:

   ![Load All Checkpoints Command](../../../../../_images/image%28576%29.png)

   Once all checkpoints are successfully loaded, your files should appear as shown below:

   ![File with checkpoints](../../../../../_images/image%28577%29.png)
3. Run the Python file to execute the checkpoints collection process.

When running a Python file that includes checkpoints, a folder named `snowpark-checkpoints-output` will be created, containing the collection results.

![Collection results output folder](../../../../../_images/image%28578%29.png)

The `checkpoints_collection_results.json` file contains the consolidated results of the collection process.

```
{
  "results": [
    {
      "timestamp": "2025-05-05 15:06:43",
      "file": "sample.py",
      "line_of_code": 57,
      "checkpoint_name": "sample$BBVOC7$df1$1",
      "result": "PASS"
    },
    {
      "timestamp": "2025-05-05 15:06:53",
      "file": "sample.py",
      "line_of_code": 57,
      "checkpoint_name": "sample$BBVOC7$df2$1",
      "result": "PASS"
    },
    {
      "timestamp": "2025-05-05 15:06:58",
      "file": "sample.py",
      "line_of_code": 57,
      "checkpoint_name": "sample$BBVOC7$df3$1",
      "result": "PASS"
    }
  ]
}
```

Copy

The `snowpark-checkpoints-output` folder should be copied into the validation workload to grant access to the collection results. For details on how to proceed with the validation process, refer to the [Validation Section](https://app.gitbook.com/o/-MB4z_O8Sl--Tfl3XVml/s/6on4bNAZUZGzMpdEum8X/~/changes/499/use-cases/sma-checkpoints-walkthrough/snowpark-checkpoints-execution-guide/validation).

Was this page helpful?

YesNo

[Visit Snowflake](https://www.snowflake.com)

[Join the conversation](https://community.snowflake.com/s/)

[Develop with Snowflake](https://developers.snowflake.com)

[Share your feedback](/feedback)

[Read the latest on our blog](https://www.snowflake.com/blog/)

[Get your own certification](https://learn.snowflake.com)

[Privacy Notice](https://www.snowflake.com/privacy-policy/)[Site Terms](https://www.snowflake.com/legal/snowflake-site-terms/)Cookies Settings© 2026 Snowflake, Inc. All Rights Reserved.