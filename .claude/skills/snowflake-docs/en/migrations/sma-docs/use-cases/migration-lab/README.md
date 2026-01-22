---
auto_generated: true
description: '[Note that this is also part of the Snowflake End-to-End Migration Quickstart
  available in the Snowflake quickstarts.]'
last_scraped: '2026-01-14T16:51:34.816848+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/sma-docs/use-cases/migration-lab/README
title: 'Snowpark Migration Accelerator: Migration Lab | Snowflake Documentation'
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
          + [Migration lab](README.md)

            - [Compatibility and assessment](compatibility-and-assessment.md)
            - [Pipeline conversion](pipeline-conversion.md)
            - [Notebook conversion](notebook-conversion.md)
            - [Conclusions](conclusions.md)
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[Snowpark Migration Accelerator](../../README.md)Use casesMigration lab

# Snowpark Migration Accelerator: Migration Lab[¶](#snowpark-migration-accelerator-migration-lab "Link to this heading")

[Note that this is also part of [the Snowflake End-to-End Migration Quickstart](https://quickstarts.snowflake.com/guide/end2endmigration/index.html?index=..%2F..index#0) available in the Snowflake quickstarts.]

Moving the logic and data in a data warehouse is essential to getting an operational database on a new platform. But to take advantage of the new platform in a functional way, any pipelines running moving data in or out of that data platform need to be repointed or replatformed as well. This can often be challenging as there are usually a variety of pipelines being used. This HoL will focus on just one for which Snowflake can provide some acceleration. But note that new ETL and pipeline accelerators are constantly being developed.

Let’s talk about the pipeline and the notebook we are moving in this scenario. As a reminder, this a SQL Server database migration, but scoped to a Proof of Concept. A small data mart in SQL Server has been moved by AdventureWorks to Snowflake. There is a basic pipeline script and a reporting notebook that AdventureWorks has included as part of this POC. Here is a summary of each artifact:

* The pipeline script is written in Python using Spark. This script is reading an accessible file generated by an older POS system in a local directory at regular intervals run by an orchestration tool. (Something like Airflow, but the orchestration is not part of the POC, so we’re not 100% sure what it is.)
* The notebook is a reporting notebook that reads from the existing SQL Server database and reports on a few summary metrics.

Neither of these are too complex, but both are just the tip of the iceberg. There are hundreds more pipeline scripts and notebooks related to other data marts. This POC will just move these two.

Both of these use Spark and access the SQL Server database. So our goal is essentially to move the operations in Spark into Snowpark. Let’s see how we would do this using [the Snowpark Migration Accelerator (SMA)](https://www.snowflake.com/en/migrate-to-the-cloud/migration-accelerator/). The SMA is a sister tool to SnowConvert and is built on the same foundation. We are going to walk through many steps (most of which will be similar to what we did with SnowConvert), but note that we are still essentially working through the same assessment -> conversion -> validation flow that we have already walked through.

## Notes on this Lab Environment[¶](#notes-on-this-lab-environment "Link to this heading")

This lab uses the Snowpark Migration Accelerator and the Snowflake VS Code Extension. But to make the most of this, you will need to run Python with a PySpark. The simplest way to start this would be to start an environment with [the anaconda distribution](https://www.anaconda.com/docs/getting-started/anaconda/main). This will have most of the packages needed to run the code in this lab.

You will still need to make available the following resources:

* Python Libraries

  + [PySpark](https://pypi.org/project/pyspark/)
  + [Snowpark Python](https://pypi.org/project/snowflake-snowpark-python/)
  + [Snowflake](https://pypi.org/project/snowflake/)
* VS Code Extensions

  + [Snowflake](https://marketplace.visualstudio.com/items?itemName=snowflake.snowflake-vsc)
  + [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
  + [Jupyter](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter)
* Other

  + [PySpark JDBC Driver of SQL Server](https://learn.microsoft.com/en-us/sql/connect/jdbc/download-microsoft-jdbc-driver-for-sql-server?view=sql-server-ver17)

Having said all of this, you can still run this lab with just a Snowflake account, the SMA, and the Snowflake VS Code Extension. You will not be able to run everything (particularly, the source code), but you will be able to use all of the converted elements in Snowflake.

Now let’s get started by assessing what we have.

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

1. [Notes on this Lab Environment](#notes-on-this-lab-environment)