---
auto_generated: true
description: This concept introduces the ability to execute the tool and persist the
  status of a project and all its configurations like Source Platform, Conversion
  Settings, Status of the latest successfully exec
last_scraped: '2026-01-14T16:52:55.765900+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/general/user-guide/snowconvert/what-is-a-snowconvert-project
title: SnowConvert AI - What is a Project? | Snowflake Documentation
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

      * [SnowConvert AI](../../../overview.md)

        + General

          + [About](../../about.md)
          + [Getting Started](../../getting-started/README.md)
          + [Terms And Conditions](../../terms-and-conditions/README.md)
          + [Release Notes](../../release-notes/release-notes/README.md)
          + User Guide

            + [SnowConvert AI](README.md)

              - [How To Install The Tool](how-to-install-the-tool/README.md)
              - [How To Request An Access Code](how-to-request-an-access-code/README.md)
              - [Command Line Interface](command-line-interface/README.md)
              - [What Is A SnowConvert AI Project](what-is-a-snowconvert-project.md)
              - [How To Update The Tool](how-to-update-the-tool.md)
              - [How To Use The SnowConvert AI Cli](how-to-use-the-snowconvert-cli.md)
            + [Project Creation](../project-creation.md)
            + [Extraction](../extraction.md)
            + [Deployment](../deployment.md)
            + [Data Migration](../data-migration.md)
            + [Data Validation](../data-validation.md)
            + [Power BI Repointing](../power-bi-repointing-general.md)
            + [ETL Migration](../etl-migration-replatform.md)
          + [Technical Documentation](../../technical-documentation/README.md)
          + [Contact Us](../../contact-us.md)
          + Others

            + [Using SnowConvert AI In A Ubuntu Docker Image](../../others/using-snowconvert-in-a-ubuntu-docker-image.md)
          + [Frequently Asked Questions (FAQ)](../../frequently-asked-questions-faq.md)")
        + Translation References

          + [General](../../../translation-references/general/README.md)
          + [Teradata](../../../translation-references/teradata/README.md)
          + [Oracle](../../../translation-references/oracle/README.md)
          + [SQL Server-Azure Synapse](../../../translation-references/transact/README.md)
          + [Sybase IQ](../../../translation-references/sybase/README.md)
          + [Hive-Spark-Databricks SQL](../../../translation-references/hive/README.md)
          + [Redshift](../../../translation-references/redshift/README.md)
          + [PostgreSQL-Greenplum-Netezza](../../../translation-references/postgres/README.md)
          + [BigQuery](../../../translation-references/bigquery/README.md)
          + [Vertica](../../../translation-references/vertica/README.md)
          + [IBM DB2](../../../translation-references/db2/README.md)
          + [SSIS](../../../translation-references/ssis/README.md)
        + [Migration Assistant](../../../migration-assistant/README.md)
        + [Data Validation CLI](../../../data-validation-cli/index.md)
        + [AI Verification](../../../snowconvert-ai-verification.md)
      * [Snowpark Migration Accelerator](../../../../sma-docs/README.md)
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

[Guides](../../../../../guides/README.md)[Migrations](../../../../README.md)Tools[SnowConvert AI](../../../overview.md)GeneralUser Guide[SnowConvert AI](README.md)What Is A SnowConvert AI Project

# SnowConvert AI - What is a Project?[¶](#snowconvert-ai-what-is-a-project "Link to this heading")

## What is a SnowConvert AI Project (.snowct)?[¶](#what-is-a-snowconvert-ai-project-snowct "Link to this heading")

This concept introduces the ability to execute the tool and persist the status of a project and all its configurations like Source Platform, Conversion Settings, Status of the latest successfully executed step, and others.

Each time that you click on “Save & Start Assessment” a project file (with the extension .snowct) will be created in the same folder that you chose as the input folder that contains the source code that you want to convert.

![.snowct file](../../../../../_images/image%28226%29.png)

As a user, you will be able to:

1. Open the SnowConvert AI project by double-clicking the .snowct file
2. Open the SnowConvert AI project by clicking on “Open Project”

   ![image](../../../../../_images/Screenshot2025-01-06at2.32.28PM.png)
3. Clicking on File -> Open Recents, this will show you the list of projects that you recently open in SnowConvert AI\

   ![image](../../../../../_images/openproject.gif)

Once you execute any of these flows the tool will redirect you to the same state of the tool that you were executing when you closed the tool.

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

The SnowConvert AI tool is subject to the [Conversion Software Terms of Use](https://www.snowflake.com/en/legal/technical-services-and-education/conversion-software-terms/).

On this page

1. [What is a SnowConvert AI Project (.snowct)?](#what-is-a-snowconvert-ai-project-snowct)