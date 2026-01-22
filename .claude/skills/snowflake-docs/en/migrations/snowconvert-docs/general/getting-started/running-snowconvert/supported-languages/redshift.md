---
auto_generated: true
description: SnowConvert AI is a software that understands SQL Redshift scripts and
  converts this source code into functionally equivalent Snowflake code.
last_scraped: '2026-01-14T16:52:30.456811+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/general/getting-started/running-snowconvert/supported-languages/redshift
title: SnowConvert AI - Redshift | Snowflake Documentation
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

      * [SnowConvert AI](../../../../overview.md)

        + General

          + [About](../../../about.md)
          + [Getting Started](../../README.md)

            - [System Requirements](../../system-requirements.md)
            - [Best Practices](../../best-practices.md)
            - [Download And Access](../../download-and-access.md)
            - [Code Extraction](../../code-extraction/README.md)
            - [Running Snowconvert AI](../README.md)

              * [Supported Languages](README.md)

                + [Teradata](teradata.md)
                + [Oracle](oracle.md)
                + [SQL Server](sql-server.md)
                + [Redshift](redshift.md)
                + [Google BigQuery](google-bigquery.md)
                + [Azure Synapse](azure-synapse.md)
                + [Sybase IQ](sybase-iq.md)
                + [PostgreSQL-Greenplum-Netezza](postgresql-and-based-languages.md)
                + [Hive-Spark-Databricks SQL](hive-spark-databricks-sql.md)
                + [Vertica](vertica.md)
                + [IBM DB2](ibm-db2.md)
              * [Validation](../validation/README.md)
              * [Conversion](../conversion/README.md)
              * [Review Results](../review-results/README.md)
            - [Training And Support](../../training-and-support.md)
          + [Terms And Conditions](../../../terms-and-conditions/README.md)
          + [Release Notes](../../../release-notes/release-notes/README.md)
          + User Guide

            + [SnowConvert AI](../../../user-guide/snowconvert/README.md)
            + [Project Creation](../../../user-guide/project-creation.md)
            + [Extraction](../../../user-guide/extraction.md)
            + [Deployment](../../../user-guide/deployment.md)
            + [Data Migration](../../../user-guide/data-migration.md)
            + [Data Validation](../../../user-guide/data-validation.md)
            + [Power BI Repointing](../../../user-guide/power-bi-repointing-general.md)
            + [ETL Migration](../../../user-guide/etl-migration-replatform.md)
          + [Technical Documentation](../../../technical-documentation/README.md)
          + [Contact Us](../../../contact-us.md)
          + Others

            + [Using SnowConvert AI In A Ubuntu Docker Image](../../../others/using-snowconvert-in-a-ubuntu-docker-image.md)
          + [Frequently Asked Questions (FAQ)](../../../frequently-asked-questions-faq.md)")
        + Translation References

          + [General](../../../../translation-references/general/README.md)
          + [Teradata](../../../../translation-references/teradata/README.md)
          + [Oracle](../../../../translation-references/oracle/README.md)
          + [SQL Server-Azure Synapse](../../../../translation-references/transact/README.md)
          + [Sybase IQ](../../../../translation-references/sybase/README.md)
          + [Hive-Spark-Databricks SQL](../../../../translation-references/hive/README.md)
          + [Redshift](../../../../translation-references/redshift/README.md)
          + [PostgreSQL-Greenplum-Netezza](../../../../translation-references/postgres/README.md)
          + [BigQuery](../../../../translation-references/bigquery/README.md)
          + [Vertica](../../../../translation-references/vertica/README.md)
          + [IBM DB2](../../../../translation-references/db2/README.md)
          + [SSIS](../../../../translation-references/ssis/README.md)
        + [Migration Assistant](../../../../migration-assistant/README.md)
        + [Data Validation CLI](../../../../data-validation-cli/index.md)
        + [AI Verification](../../../../snowconvert-ai-verification.md)
      * [Snowpark Migration Accelerator](../../../../../sma-docs/README.md)
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

[Guides](../../../../../../guides/README.md)[Migrations](../../../../../README.md)Tools[SnowConvert AI](../../../../overview.md)General[Getting Started](../../README.md)[Running Snowconvert AI](../README.md)[Supported Languages](README.md)Redshift

# SnowConvert AI - Redshift[¶](#snowconvert-ai-redshift "Link to this heading")

## What is SnowConvert AI for Redshift?[¶](#what-is-snowconvert-ai-for-redshift "Link to this heading")

SnowConvert AI is a software that understands SQL Redshift scripts and converts this source code into functionally equivalent Snowflake code.

## Conversion Types[¶](#conversion-types "Link to this heading")

Specifically, SnowConvert AI for Redshift performs the following conversions:

### Redshift to Snowflake SQL[¶](#redshift-to-snowflake-sql "Link to this heading")

SnowConvert AI recognizes the Redshift source code and converts the different statements into the appropriate SQL for the Snowflake target.

### Sample code[¶](#sample-code "Link to this heading")

#### Input Code[¶](#input-code "Link to this heading")

```
CREATE TABLE table1 (
    col1 INTEGER GENERATED BY DEFAULT AS IDENTITY(1,1)
);
```

Copy

#### Output Code[¶](#output-code "Link to this heading")

```
CREATE TABLE table1 (
    col1 INTEGER IDENTITY(1,1) ORDER
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/17/2024" }}'
;
```

Copy

As you can see, most of the structure remains the same, but some column properties have to be transformed to Snowflake equivalents. For more information please refer to [Redshift Translation References documentation](../../../../translation-references/redshift/README).

### SnowConvert AI Terminology[¶](#snowconvert-ai-terminology "Link to this heading")

Before we get lost in the magic of these code conversions, here are a few terms/definitions so you know what we mean when we start dropping them all over the documentation:

* *SQL (Structured Query Language):* the standard language for storing, manipulating, and retrieving data in most modern database architectures.
* *SnowConvert AI*: the software that converts securely and automatically your Redshift files to the Snowflake cloud data platform.
* *Conversion rule* or *transformation rule:* rules that allow SnowConvert AI to convert from a portion of source code to the expected target code.
* *Parse:* parse or parsing is an initial process done by SnowConvert AI to understand the source code and build up an internal data structure required for executing the conversion rules.

In the next few pages, you’ll learn more about the kind of conversions that SnowConvert AI for Redshift is capable of. If you’re ready to get started, visit the [**Getting Started**](../../README) page in this documentation.

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

1. [What is SnowConvert AI for Redshift?](#what-is-snowconvert-ai-for-redshift)
2. [Conversion Types](#conversion-types)