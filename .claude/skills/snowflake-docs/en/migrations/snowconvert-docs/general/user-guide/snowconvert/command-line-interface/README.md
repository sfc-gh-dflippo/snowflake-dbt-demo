---
auto_generated: true
description: To execute a conversion with the SnowConvert AI CLI you have to have
  an active access code. Currently, the access codes for the CLI are different than
  the UI, but if you already have an access code fo
last_scraped: '2026-01-14T16:52:53.939576+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/general/user-guide/snowconvert/command-line-interface/README
title: SnowConvert AI - Command Line Interface | Snowflake Documentation
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
          + [Getting Started](../../../getting-started/README.md)
          + [Terms And Conditions](../../../terms-and-conditions/README.md)
          + [Release Notes](../../../release-notes/release-notes/README.md)
          + User Guide

            + [SnowConvert AI](../README.md)

              - [How To Install The Tool](../how-to-install-the-tool/README.md)
              - [How To Request An Access Code](../how-to-request-an-access-code/README.md)
              - [Command Line Interface](README.md)

                * [Renaming Feature](renaming-feature.md)
                * [Oracle](oracle.md)
                * [Teradata](teradata.md)
                * [SQL Server](sql-server.md)
                * [Redshift](redshift.md)
              - [What Is A SnowConvert AI Project](../what-is-a-snowconvert-project.md)
              - [How To Update The Tool](../how-to-update-the-tool.md)
              - [How To Use The SnowConvert AI Cli](../how-to-use-the-snowconvert-cli.md)
            + [Project Creation](../../project-creation.md)
            + [Extraction](../../extraction.md)
            + [Deployment](../../deployment.md)
            + [Data Migration](../../data-migration.md)
            + [Data Validation](../../data-validation.md)
            + [Power BI Repointing](../../power-bi-repointing-general.md)
            + [ETL Migration](../../etl-migration-replatform.md)
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

[Guides](../../../../../../guides/README.md)[Migrations](../../../../../README.md)Tools[SnowConvert AI](../../../../overview.md)GeneralUser Guide[SnowConvert AI](../README.md)Command Line Interface

# SnowConvert AI - Command Line Interface[¶](#snowconvert-ai-command-line-interface "Link to this heading")

## Quick start[¶](#quick-start "Link to this heading")

To execute a conversion with the SnowConvert AI CLI you have to have an active access code. Currently, the access codes for the CLI are different than the UI, but if you already have an access code for the UI you should be able to reuse the same access code. In the section below we show how to install an access code.

There are several Command Line Arguments documented below, but the main ones are `-i` for the input folder and `-o` for the output folder.

### Install an access code[¶](#install-an-access-code "Link to this heading")

To install an access code just execute SnowConvert AI CLI program with the `install-ac` argument and the access code.

```
$: snowct install-ac <access-code>
```

Copy

### CLI useful commands[¶](#cli-useful-commands "Link to this heading")

* **`snowct --help or snowct -h`**: Will show help.
* **`snowct --version or snowct -v`**`:` Will show the version of the CLI (and the code processors).
* **`snowct install-ac <access-code>:`** Will install the corresponding access code provided.
* **`snowct install-ac --file <file-with-access-code>:`** Will install the corresponding access code in the machine (using an access code file).
* **`snowct show-ac:`** Will show the active access codes currently installed.
* **`snowct {Language} -i ./input -o ./output:`** Will convert the input code.

  + Supported Languages: Teradata, Oracle, SQL-server.
* You can check the help for a specific command just by using the -h or –help option. For example:

  + snowct install-ac –help
  + snowct show-ac –help
  + snowct teradata –help

### Common CLI Arguments[¶](#common-cli-arguments "Link to this heading")

The following arguments can be used in all the languages

#### `-i, --input <PATH>` **(Required)**[¶](#i-input-path-required "Link to this heading")

The path to the folder or file containing the input source code.

#### `-o, --output <PATH>` (Required)[¶](#o-output-path-required "Link to this heading")

The path to the output folder where the converted code and reports will be stored.

#### `-t, --PLTargetLanguage <TARGET_LANGUAGE>`[¶](#t-pltargetlanguage-target-language "Link to this heading")

String value specifying the target language to convert Stored procedures and Macros. Currently supported are: **SnowScript** and **JavaScript**. The default value is set to **SnowScript**.

#### `-e, --encoding <CODE PAGE>`[¶](#e-encoding-code-page "Link to this heading")

The encoding code page number is used for parsing the source files. We only accept [encodings supported by .NET Core](https://docs.microsoft.com/en-us/dotnet/api/system.text.encoding?view=net-5.0#list-of-encodings). Here are the ones supported at the moment:

| Code Page | Name | Display Name |
| --- | --- | --- |
| Code Page | Name | Display Name |
| 1200 | utf-16 | Unicode |
| 1201D | unicodeFFFE | Unicode (Big endian) |
| 12000 | utf-32 | Unicode (UTF-32) |
| 12001 | utf-32BE | Unicode (UTF-32 Big endian) |
| 20127 | us-ascii | US-ASCII |
| 28591 | iso-8859-1 | Western European (ISO) |
| 65000 | utf-7 | Unicode (UTF-7). *Not available in .NET 5* |
| 65001 | utf-8 | Unicode (UTF-8). *Default encoding* |

#### `-s, --customschema <SCHEMA_NAME>`[¶](#s-customschema-schema-name "Link to this heading")

The string value specifies the custom schema name to apply. If not specified, the original database name will be used. Example: DB1.***MyCustomSchema***.Table1.

#### `-d, --database <DB_NAME>`[¶](#d-database-db-name "Link to this heading")

The string value specifies the custom database name to apply. Example: ***MyCustomDB***.PUBLIC.Table1.

**`--useExistingNameQualification`**

This flag must be used in conjunction with the **`-d`** or **`-s`** parameters. When used, it preserves the existing name qualification from the input code when previous parameters are used.   
Let’s take a look at this example where `-s newSchema` was included:

```
SELECT * FROM mySchema.myObject;
```

Copy

```
SELECT * FROM newSchema.myObject;
```

Copy

```
SELECT * FROM mySchema.myObject;
```

Copy

The same applies to databases.

#### `--rate`[¶](#rate "Link to this heading")

The string value specifies the conversion rate mode. Currently supported are: **LoC** (Lines of Code) and **Character**. The default value is set to **LoC**.

#### `-m, --comments`[¶](#m-comments "Link to this heading")

Flag to indicate if the user wants to comment on nodes that have missing dependencies.

#### `--disableEWIsGeneration`[¶](#disableewisgeneration "Link to this heading")

Flag to indicate whether EWIs comments (Errors, Warnings, and Issues) will not be generated on the converted code. The default is false.

#### `--terms`[¶](#terms "Link to this heading")

Show access code terms information.

#### `--help`[¶](#help "Link to this heading")

Display the help information.

### Additional Parameters[¶](#additional-parameters "Link to this heading")

Each tool has its own optional parameters that you can provide in order to customize the conversion/assessment.

Visit the following links to read more about the additional parameters that are available for each tool:

* [Teradata](teradata)
* [Oracle](oracle)
* [Sql Server](sql-server)
* [Redshift](redshift)
* [Azure Synapse](sql-server)

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

1. [Quick start](#quick-start)