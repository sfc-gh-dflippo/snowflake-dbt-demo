---
auto_generated: true
description: Every single file in the input path is considered the Submitted Scope.
  However, there can be files with unrecognized extensions or unsupported encodings
  that will not be processed by SnowConvert AI. E
last_scraped: '2026-01-14T16:52:19.420836+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/general/getting-started/running-snowconvert/review-results/snowconvert-scopes
title: SnowConvert AI - SnowConvert AI Scopes | Snowflake Documentation
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

              * [Supported Languages](../supported-languages/README.md)
              * [Validation](../validation/README.md)
              * [Conversion](../conversion/README.md)
              * [Review Results](README.md)

                + [SnowConvert AI Scopes](snowconvert-scopes.md)
                + [Output Code](output-code.md)
                + [Reports](reports/README.md)
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

[Guides](../../../../../../guides/README.md)[Migrations](../../../../../README.md)Tools[SnowConvert AI](../../../../overview.md)General[Getting Started](../../README.md)[Running Snowconvert AI](../README.md)[Review Results](README.md)SnowConvert AI Scopes

# SnowConvert AI - SnowConvert AI Scopes[¶](#snowconvert-ai-snowconvert-ai-scopes "Link to this heading")

## Scope definitions[¶](#scope-definitions "Link to this heading")

### Submitted Scope[¶](#submitted-scope "Link to this heading")

Every single file in the input path is considered the *Submitted Scope.* However, there can be files with unrecognized extensions or unsupported encodings that will not be processed by SnowConvert AI. Even though the assessment documents provide the list of excluded files, their content is not parsed (recognized).

For more information about unrecognized extensions and unsupported encodings, see the [Validation section](../validation/README).

### Assessment Scope[¶](#assessment-scope "Link to this heading")

The portion of the Submitted Scope that is seen as valid by SnowConvert AI is considered the *Assessment Scope, that is* all files with recognized extensions and supported encodings. SnowConvert AI will try to parse every single file in this scope in order to be able to provide assessment information.

### Conversion Scope[¶](#conversion-scope "Link to this heading")

There can be elements within the Assessment Scope that are not part of the conversion scope. SnowConvert AI classifies specific top-level code units as out-of-scope for multiple reasons, such as:

* they are not relevant in Snowflake
* there is no comparable code unit in Snowflake
* the code unit definition is not readable (ex: encrypted)
* the code unit definition is in a not supported programming language (ex: java)

Lines of code of code units out of the conversion scope will not be used to calculate conversion rates, but they will be used to provide some information in the assessment documents. For example, a Database Link object In Oracle is considered out of scope, however, references made to this object are still counted and reported in the [Object References Report](reports/object-references-report).

The following is the list of Code Units per language considered out of the conversion scope.

#### Teradata out-of-conversion scope code units[¶](#teradata-out-of-conversion-scope-code-units "Link to this heading")

* Triggers
* Grants
* Functions or procedures with unsupported language

#### Oracle out-of-conversion scope code units[¶](#oracle-out-of-conversion-scope-code-units "Link to this heading")

* Triggers
* Grants
* DB Links
* Wrapped Objects
* Functions or procedures with unsupported languages

#### Transact SQL out-of-conversion scope code units[¶](#transact-sql-out-of-conversion-scope-code-units "Link to this heading")

* Triggers
* Grants

#### Redshift out-of-conversion scope code units[¶](#redshift-out-of-conversion-scope-code-units "Link to this heading")

* Grants

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

1. [Scope definitions](#scope-definitions)