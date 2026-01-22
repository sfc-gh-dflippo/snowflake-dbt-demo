---
auto_generated: true
description: 'Depending on your Operating System, you can review the corresponding
  installation guide:'
last_scraped: '2026-01-14T16:52:55.545662+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/general/user-guide/snowconvert/how-to-use-the-snowconvert-cli
title: SnowConvert AI - How to use the SnowConvert AI CLI | Snowflake Documentation
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

[Guides](../../../../../guides/README.md)[Migrations](../../../../README.md)Tools[SnowConvert AI](../../../overview.md)GeneralUser Guide[SnowConvert AI](README.md)How To Use The SnowConvert AI Cli

# SnowConvert AI - How to use the SnowConvert AI CLI[¶](#snowconvert-ai-how-to-use-the-snowconvert-ai-cli "Link to this heading")

## Installation[¶](#installation "Link to this heading")

Depending on your Operating System, you can review the corresponding installation guide:

* [Linux](how-to-install-the-tool/linux)
* [Windows](how-to-install-the-tool/windows)
* [MacOS](how-to-install-the-tool/macos)

## Commands[¶](#commands "Link to this heading")

### Summary[¶](#summary "Link to this heading")

Each command can be used with the following syntax:

```
snowct [command] [arguments]
```

Copy

The available commands are listed below. If you want to check a detailed explanation for a command, you can click on the command.

| Command | Alias | Description |
| --- | --- | --- |
| `install-access-code` | `install-ac` | Install an access code. |
| `show-access-code` | `show-ac` | Show the installed access code(s). |
| `teradata` |  | Perform a Teradata conversion/assessment. |
| `oracle` |  | Perform an Oracle conversion/assessment. |
| `sql-server` |  | Perform a SQL Server conversion/assessment. |
| `redshift` |  | Perform a Redshift conversion/assessment. |
| `azuresynapse` |  | Perform an Azure Synapse conversion/assessment. |
| `sybase` |  | Perform a Sybase IQ conversion/assessment. |
| `greenplum` |  | Perform a Greenplum conversion/assessment. |
| `postgresql` |  | Perform a PostgreSQL conversion/assessment. |
| `netezza` |  | Perform a Netezza conversion/assessment. |
| `spark` |  | Perform a Spark SQL conversion/assessment. |
| `databricks` |  | Perform a Databricks SQL conversion/assessment. |
| `vertica` |  | Perform a Vertica conversion/assessment. |
| `hive` |  | Perform a Hive conversion/assessment. |
| `--help` | `-h` | Show help. |
| `--version` | `-v` | Show the version of the tool. |

### Installing an access code[¶](#installing-an-access-code "Link to this heading")

Before converting your code, you need to install an access code. You can do this by specifying the access code, or by specifying the path to the file that contains the access code information (this is useful when installing the access code without an Internet connection or under restrictive firewall settings).

You can use the following command to install the access code by writing the code:

```
snowct install-access-code <access-code>
```

Copy

This command is equivalent to the previous command:

```
snowct install-ac <access-code>
```

Copy

If you want to install an access code using a file, you can use the `--file` / `-f` option, as shown in the following commands:

```
snowct install-access-code --file <path-to-file>
snowct install-access-code -f <path-to-file>
snowct install-a --file <path-to-file>
snowct install-ac -f <path-to-file>
```

Copy

Note

If there is an error during the installation of the license, an error will be shown. If you need an access code, you can reach out to **[snowconvert-support@snowflake.com](mailto:snowconvert-support%40snowflake.com) .**

### Converting[¶](#converting "Link to this heading")

You can use the following commands to convert your source code. You must provide an input path (where the source code is) and an output path (where the converted code will be placed). There is a different command for each product:

* SnowConvert AI Teradata: **teradata**
* SnowConvert AI Oracle: **oracle**
* SnowConvert AI SQL Server**: sql-server**
* SnowConvert AI Redshift**: redshift**
* SnowConvert AI Azure Synapse**: azuresynapse**
* SnowConvert AI Sybase IQ**: sybase**
* SnowConvert AI Greenplum: **greenplum**
* SnowConvert AI PostgreSQL: **postgresql**
* SnowConvert AI Netezza: **netezza**
* SnowConvert AI Spark SQL: **spark**
* SnowConvert AI Databricks SQL: **databricks**
* SnowConvert AI Vertica: **vertica**
* SnowConvert AI Hive: **hive**

```
snowct teradata --input <input-path> --output <output-path> <additional-parameters>
snowct oracle --input <input-path> --output <output-path> <additional-parameters>
snowct sql-server --input <input-path> --output <output-path> <additional-parameters>
snowct redshift --input <input-path> --output <output-path> <additional-parameters>
snowct azuresynapse --input <input-path> --output <output-path> <additional-parameters>
snowct sybase --input <input-path> --output <output-path> <additional-parameters>
snowct greenplum --input <input-path> --output <output-path> <additional-parameters>
snowct postgresql --input <input-path> --output <output-path> <additional-parameters>
snowct netezza --input <input-path> --output <output-path> <additional-parameters>
snowct spark --input <input-path> --output <output-path> <additional-parameters>
snowct databricks --input <input-path> --output <output-path> <additional-parameters>
snowct vertica --input <input-path> --output <output-path> <additional-parameters>
snowct hive --input <input-path> --output <output-path> <additional-parameters>
```

Copy

In each of these cases, you can use `-i` instead of `--input`, or `-o` instead of `--output`. For example, instead of writing `snowct teradata --input <input-path> --output <output-path>` you can write `snowct teradata -i <input-path> -o <output-path>`.

Each of these commands might also receive additional parameters. In the following links, you can review which additional parameters are available for each product:

* [SnowConvert AI Teradata](command-line-interface/teradata)
* [SnowConvert AI Oracle](command-line-interface/oracle)
* [SnowConvert AI SQL Server](command-line-interface/sql-server)
* [SnowConvert AI Redshift](command-line-interface/redshift)
* [SnowConvert AI Azure Synapse](command-line-interface/sql-server)

### Checking which access codes are installed[¶](#checking-which-access-codes-are-installed "Link to this heading")

If you want to know which access codes are installed on your computer, you can use the following command:

```
snowct show-access-code
```

Copy

This command is equivalent to the previous command:

```
snowct show-ac
```

Copy

This command will show the information for each access code that is installed on your computer.

### Checking the version of the tool[¶](#checking-the-version-of-the-tool "Link to this heading")

You can use any of the following commands to check the version of the tool and the version for each code processing engine (SnowConvert AI Teradata, SnowConvert AI Oracle, SnowConvert AI SQL Server):

```
snowct --version
snowct -v
```

Copy

### Need more help?[¶](#need-more-help "Link to this heading")

If you want to see general help for the CLI, you can use the following commands:

```
snowct --help
snowct -h
```

Copy

You can get more information about a command by executing this command:

```
snowct <command> --help
```

Copy

For example, you can execute `snowct install-access-code --help` to get more information about how to install an access code, or you can execute `snowct teradata --help` to get more information about how to execute conversions using SnowConvert AI Teradata. This will also show information about the additional options that are available for SnowConvert AI Teradata.

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

1. [Installation](#installation)
2. [Commands](#commands)