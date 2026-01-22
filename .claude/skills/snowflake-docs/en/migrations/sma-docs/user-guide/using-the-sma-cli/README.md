---
auto_generated: true
description: 'The Snowpark Migration Accelerator (SMA) provides a Command Line Interface
  (CLI) that allows you to perform various operations. Using this CLI, you can execute
  the code processor, manage access codes '
last_scraped: '2026-01-14T16:51:41.012750+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/sma-docs/user-guide/using-the-sma-cli/README
title: 'Snowpark Migration Accelerator:  Using the SMA CLI | Snowflake Documentation'
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
          + [Conversion](../conversion/README.md)
          + [Using the SMA CLI](README.md)

            - [Additional parameters](additional-parameters.md)
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[Snowpark Migration Accelerator](../../README.md)User guideUsing the SMA CLI

# Snowpark Migration Accelerator: Using the SMA CLI[¶](#snowpark-migration-accelerator-using-the-sma-cli "Link to this heading")

## Description[¶](#description "Link to this heading")

The Snowpark Migration Accelerator (SMA) provides a Command Line Interface (CLI) that allows you to perform various operations. Using this CLI, you can execute the code processor, manage access codes (install or display them), and perform any other task that’s available in the SMA application.

The SMA uses a single code processor that works with all [supported source platforms](../before-using-the-sma/supported-platforms). You don’t need to provide any additional arguments for this processor.

## Installation[¶](#installation "Link to this heading")

Before installing the Command Line Interface (CLI), you need to [download it](../../general/getting-started/download-and-access.html#downloading-the-sma-command-line-interface-cli) to a location you can access. Choose the installation guide that matches your operating system:

* [Linux](../../general/getting-started/installation/linux-installation)
* [Windows](../../general/getting-started/installation/windows-installation)
* [MacOS](../../general/getting-started/installation/macos-installation)

## Commands[¶](#commands "Link to this heading")

To run the tool, you need to set up a sequence of commands based on your requirements. You can use either the **long-command** or **short-command** options with the following syntax:

```
sma [command] [argument] [command] [argument] ...
```

Copy

The following commands are available. Click any command to view its detailed explanation.

| Long-command | Short-Command | Description |
| --- | --- | --- |
| [–help](#need-more-help) | -h | Displays help documentation. |
| [–version](#checking-the-tool-version) | -v | Displays current tool version. |
| [install-access-code](#installing-an-access-code) | install-ac | Installs a new access code. |
| [show-access-code](#checking-which-access-codes-are-installed) | show-ac | Displays all installed access codes. |
| [–input](#converting) | -i | Specifies the input folder location. |
| [–output](#converting) | -o | Specifies the output folder location. |
| [–assessment](#performing-an-assessment) | -a | Runs the tool in assessment mode. |
| [–mapDirectory](additional-parameters) | -m | Specifies the folder containing custom mapping files. |
| [–enableJupyter](#enabling-conversion-of-databricks-notebooks-to-jupyter-notebooks) | -j | Enables or disables conversion of Databricks notebooks to Jupyter format. |
| [–sql](#setting-the-sql-flavor-of-the-source-code) | -f | Specifies which database engine syntax to use for SQL commands. |
| [–customerEmail](#project-information) | -e | Sets the customer email address. |
| [–customerCompany](#project-information) | -c | Sets the customer company name. |
| [–projectName](#project-information) | -p | Sets the project name. |
| [–yes](#skipping-the-project-confirmation) | -y | Skips confirmation prompts during execution. |

### Installing an access code[¶](#installing-an-access-code "Link to this heading")

To begin the code conversion process, you must first install an access code. You can do this in two ways:

1. Enter the access code directly
2. Provide the path to a file containing the access code (This method is helpful when you’re working offline or behind a restrictive firewall)

You can install the access code by running the following command:

```
sma install-access-code <access-code>
```

Copy

This command produces the same result as the previous command.

```
sma install-ac <access-code>
```

Copy

To install an access code from a file, use either the `--file` or `-f` option with your command, like this:

```
sma install-access-code --file <path-to-file>
or
sma install-access-code -f <path-to-file>
```

Copy

If an error occurs while installing the license, an error message will be displayed.

To request an access code, please contact sma-support@snowflake.com

### Checking which access codes are installed[¶](#checking-which-access-codes-are-installed "Link to this heading")

To check which access codes are currently installed on your computer, use this command:

```
sma show-access-code
```

Copy

This command displays details about all access codes that are currently installed on your computer.

### Converting[¶](#converting "Link to this heading")

After installing a valid license, you can run the code processor to convert your code. To start the conversion process, you need to provide the following required arguments:

* **Input path:** The folder containing your original source code
* **Output path:** The folder where you want the converted code to be saved

#### Project Information[¶](#project-information "Link to this heading")

When you run the code processor for the first time, you need to provide certain arguments. These arguments will be saved and used for future executions. The required arguments are the same as those needed when [creating a new project in the application](../project-overview/project-setup.html#creating-a-new-project).

* **Customer Email:** Enter a valid email address
* **Customer Company:** Enter your company name
* **Project Name:** Enter a name for your project

This example demonstrates how to execute the code processor using only the essential requirements:

```
sma -i <input-path> -o <output-path> -e <client email> -c <client company> -p <project name> <additional-parameters>
```

Copy

After entering the sequence of commands and pressing “Enter”, the tool will display your current settings and ask you to confirm before starting the process.

![Current configuration before start process.](../../../../_images/image%2815%29.png)

Would you like to add or modify any arguments? Type “n” to cancel or “y” to proceed.

#### Skipping the Project Confirmation[¶](#skipping-the-project-confirmation "Link to this heading")

To bypass the confirmation prompt shown above, add either **–yes** or **-y** as an argument. This is particularly important when using the tool programmatically, as the confirmation prompt will appear every time without these parameters.

For more information about all available parameters, please refer to this [link](additional-parameters).

### Performing an Assessment[¶](#performing-an-assessment "Link to this heading")

When performing an assessment, add the `--assessment` or `-a` option to the standard conversion commands. Here are examples of how the commands should look:

```
sma --input <input-path> --output <output-path> --assessment <additional-parameters>
```

Copy

Each of these commands can accept additional parameters. For more details, please refer to the “Converting” section.

### Checking the tool version[¶](#checking-the-tool-version "Link to this heading")

To check the tool version and code-processing engine, you can use any of these commands:

```
sma --version
sma -v
```

Copy

### Enabling conversion of Databricks notebooks to Jupyter Notebooks[¶](#enabling-conversion-of-databricks-notebooks-to-jupyter-notebooks "Link to this heading")

This option converts Python (.python) and/or Scala (.scala) source files into Jupyter Notebook (.ipynb) files. The conversion works regardless of whether the original files were exported from notebooks or were regular code files.

To convert Jupyter notebooks, add either the `'--enableJupyter'` flag or its shorthand version `'-j'` to your command.

```
sma -i <input-path> -o <output-path> --enableJupyter
```

Copy

### Setting the SQL Flavor of the source code[¶](#setting-the-sql-flavor-of-the-source-code "Link to this heading")

You can specify which SQL syntax to use when a SQL command is detected. Use either the command `'--sql'` or its shortcut `'-f'`. The supported syntax options are ‘SparkSql’ (which is the default) and ‘HiveSql’.

```
sma --input <input-path> --output <output-path> --sql SparkSql
sma --input <input-path> --output <output-path> --sql HiveSql
```

Copy

### Need more help?[¶](#need-more-help "Link to this heading")

To view general help information for the Command Line Interface (CLI), you can use any of these commands:

```
sma --help
sma -h
```

Copy

![Help information](../../../../_images/image%2816%291.png)

To learn more about specific commands, you can execute this command:

```
sma <command> --help
```

Copy

To learn more about installing an access code, run the command `sma install-access-code --help`.

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

1. [Description](#description)
2. [Installation](#installation)
3. [Commands](#commands)