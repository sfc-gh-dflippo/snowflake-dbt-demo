---
auto_generated: true
description: 'The Scope Validator step checks if the entry code meets the basic requirements
  to execute a successful conversion. These requirements are:'
last_scraped: '2026-01-14T16:52:18.289321+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/general/getting-started/running-snowconvert/validation/README
title: SnowConvert AI - Validation | Snowflake Documentation
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
              * [Validation](README.md)

                + [Ambiguos Comments Validation](ambiguous-comments-validations.md)
                + [File Encoding Validation](file-encoding-validation.md)
                + [System Object Naming Validation](system-object-naming-validation.md)
                + [File Extension Validation](file-extension-validation.md)
                + [File Format Validation](file-format-validation.md)
                + [Extraction Validation](extraction-validation.md)
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

[Guides](../../../../../../guides/README.md)[Migrations](../../../../../README.md)Tools[SnowConvert AI](../../../../overview.md)General[Getting Started](../../README.md)[Running Snowconvert AI](../README.md)Validation

# SnowConvert AI - Validation[¶](#snowconvert-ai-validation "Link to this heading")

The Scope Validator step checks if the entry code meets the basic requirements to execute a successful conversion. These requirements are:

* Valid extension file
* Valid file encoding
* The entry code is extracted
* Valid entry file format
* Valid files and folder naming
* Valid Comments

Note

If one of these validations is not met, it does not mean that the conversion can not be executed. These validations only warn that something is not okay with the entry code, and thus, something could be wrong with the migration results.

## How to execute the validation[¶](#how-to-execute-the-validation "Link to this heading")

The Scope Validator is a step that starts once the configuration for the [Conversion](../conversion/README) process is done. It means that it is always executed.

### View validation results[¶](#view-validation-results "Link to this heading")

Once the validation step finishes, a window with the information about what validations failed is displayed like the next one:

![Scope Validator Window With Results](../../../../../../_images/image%288%29.png)

In this case, the validation that failed is to check if the entry code was extracted or not. Please visit their sections to get more information about each validation.

Also, a report called *FilesOutOfScope* is generated inside a folder called *Scope Validations* inside the output folder.

```
Output Folder > Reports > SnowConvert AI > Scope Validations > ScopeValidation.{timeStamp}.csv
```

Copy

Note

The Out of scope report link could redirect you to this report.

This report enumerates all the invalid files with their respective paths/names, sizes, and reasons. E.g.:

| File Path/Name | File Size | Reason |
| --- | --- | --- |
| file1.bat | 40.0 B | File Type |

The last one was an example of an invalid file because of the extension.

### How to proceed[¶](#how-to-proceed "Link to this heading")

As you can see in the *Scope Validator Window With Results* image, there are two options: one is to continue with the Assessment or Conversion Process, and the other is to cancel it. The recommendation is to cancel the process, check the warnings, and try to resolve them. But if you decide to continue with the conversion, you will also be able to find the information related to the Scope Validation in the Assessment.csv report and the AssessmentReport.docx. In the Assessment.csv, you will find the following fields: the total validated files, total invalid files, total of files with wrong encoding, total of files with wrong extension, total of files with invalid naming, and an out-of-scope percentage (a calculation of the pending work to do to have a valid entry code). In the docx report, you will find a section with the same information that is in the FilesOutOfScope report.

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

1. [How to execute the validation](#how-to-execute-the-validation)