---
auto_generated: true
description: When you run a conversion using the Snowpark Migration Accelerator (SMA),
  it generates detailed information similar to what you get in assessment mode. The
  process is identical in both cases (as expla
last_scraped: '2026-01-14T16:52:02.117617+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/sma-docs/user-guide/conversion/understanding-the-conversion-assessment-and-reporting
title: 'Snowpark Migration Accelerator: Understanding the Conversion Assessment and
  Reporting | Snowflake Documentation'
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
          + [Assessment](../assessment/README.md)
          + [Conversion](README.md)

            - [How the conversion works](how-the-conversion-works.md)
            - [Conversion quick start](conversion-quick-start.md)
            - [Conversion setup](conversion-setup.md)
            - [Understanding the conversion assessment and reporting](understanding-the-conversion-assessment-and-reporting.md)
            - [Output code](output-code.md)
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[Snowpark Migration Accelerator](../../README.md)User guide[Conversion](README.md)Understanding the conversion assessment and reporting

# Snowpark Migration Accelerator: Understanding the Conversion Assessment and Reporting[¶](#snowpark-migration-accelerator-understanding-the-conversion-assessment-and-reporting "Link to this heading")

When you run a conversion using the Snowpark Migration Accelerator (SMA), it generates detailed information similar to what you get in assessment mode. The process is identical in both cases (as explained in [How the Conversion Works](how-the-conversion-works.html#conversion-in-the-sma)), but during conversion, the tool also produces the converted code as part of its output.

To ensure accurate code conversion, SMA generates the same information twice because source code can be modified between the initial assessment and the final conversion. This approach provides the most reliable way to verify that the conversion matches the current state of your codebase.

Note

The assessment and conversion modes produce identical log files, reports, and assessment summary screens. The only difference between these modes is the converted code that is generated when running in conversion mode.

## Conversion Summary[¶](#conversion-summary "Link to this heading")

The conversion results will be displayed in the Results panel of the application.

![Conversion Summary](../../../../_images/ConversionSummary.png)

This section provides the same information as the Assessment Summary. For more details about interpreting the conversion assessment results, please refer to the [Understanding the Assessment Summary](../assessment/understanding-the-assessment-summary) section.

## Conversion Output Reports[¶](#conversion-output-reports "Link to this heading")

To access the reports generated by the Snowpark Migration Accelerator (SMA), click the “View Reports” button on the Results page.

![Conversion Reports](../../../../_images/ConversionReports.png)

The tool creates a directory containing all reports. These reports are identical to those generated during the Assessment phase. For detailed information about each report, please refer to the [Output Reports](../assessment/output-reports/README) section in the Assessment documentation.

## Conversion Logs[¶](#conversion-logs "Link to this heading")

The logs are generated automatically during the assessment process, similar to how summaries and reports are created. To access these logs, click the “View Log Folder” option.

![View Log Folder](../../../../_images/ViewLogFolder.png)

To view detailed information about available logs, please refer to the [Output Logs](../assessment/output-logs) section in the Assessment documentation.

---

Let’s explore where the converted code will be stored after the conversion process is complete.

![View Output](../../../../_images/ViewOutput.png)

To see the converted code, click **View Output** on the Results page.

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

1. [Conversion Summary](#conversion-summary)
2. [Conversion Output Reports](#conversion-output-reports)
3. [Conversion Logs](#conversion-logs)