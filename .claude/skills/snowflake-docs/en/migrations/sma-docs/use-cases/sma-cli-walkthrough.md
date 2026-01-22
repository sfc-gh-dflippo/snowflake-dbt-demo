---
auto_generated: true
description: 'The Snowpark Migration Accelerator (SMA) helps developers migrate their
  Python or Scala Spark code to Snowpark. It analyzes your code and:'
last_scraped: '2026-01-14T16:51:35.925808+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/sma-docs/use-cases/sma-cli-walkthrough
title: 'Snowpark Migration Accelerator: SMA CLI Walkthrough | Snowflake Documentation'
---

1. [Overview](../../../guides/README.md)
2. [Snowflake Horizon Catalog](../../../user-guide/snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../../../guides/overview-connecting.md)
6. [Virtual warehouses](../../../user-guide/warehouses.md)
7. [Databases, Tables, & Views](../../../guides/overview-db.md)
8. [Data types](../../../data-types.md)
10. Data Integration

    - [Snowflake Openflow](../../../user-guide/data-integration/openflow/about.md)
    - Apache Iceberg™

      - [Apache Iceberg™ Tables](../../../user-guide/tables-iceberg.md)
      - [Snowflake Open Catalog](../../../user-guide/opencatalog/overview.md)
11. Data engineering

    - [Data loading](../../../guides/overview-loading-data.md)
    - [Dynamic Tables](../../../user-guide/dynamic-tables-about.md)
    - [Streams and Tasks](../../../user-guide/data-pipelines-intro.md)
    - [dbt Projects on Snowflake](../../../user-guide/data-engineering/dbt-projects-on-snowflake.md)
    - [Data Unloading](../../../guides/overview-unloading-data.md)
12. [Storage Lifecycle Policies](../../../user-guide/storage-management/storage-lifecycle-policies.md)
13. [Migrations](../../README.md)

    * Tools

      * [SnowConvert AI](../../snowconvert-docs/overview.md)
      * [Snowpark Migration Accelerator](../README.md)

        + General

          + [Introduction](../general/introduction.md)
          + [Getting started](../general/getting-started/README.md)
          + [Conversion software terms of use](../general/conversion-software-terms-of-use/README.md)
          + [Release notes](../general/release-notes/README.md)
          + [Roadmap](../general/roadmap.md)
        + User guide

          + [Overview](../user-guide/overview.md)
          + [Before using the SMA](../user-guide/before-using-the-sma/README.md)
          + [Project overview](../user-guide/project-overview/README.md)
          + [Technical discovery](../user-guide/project-overview/optional-technical-discovery.md)
          + [AI assistant](../user-guide/chatbot.md)
          + [Assessment](../user-guide/assessment/README.md)
          + [Conversion](../user-guide/conversion/README.md)
          + [Using the SMA CLI](../user-guide/using-the-sma-cli/README.md)
        + Use cases

          + Snowflake VS Code extension

            + [SMA checkpoints walkthrough](sma-checkpoints-walkthrough/README.md)
            + [SMA EWI Assistant walkthrough](sma-ewi-assistant-walkthrough/README.md)
          + [Assessment walkthrough](assessment-walkthrough/README.md)
          + [Conversion walkthrough](conversion-walkthrough.md)
          + [Migration lab](migration-lab/README.md)
          + [Sample project](sample-project.md)
          + [Using SMA in an Ubuntu Docker image](using-snowconvert-in-a-ubuntu-docker-image.md)
          + [SMA CLI walkthrough](sma-cli-walkthrough.md)
          + [Snowpark Connect](snowpark-connect/README.md)
        + Issue analysis

          + [Approach](../issue-analysis/approach.md)
          + [Issue code categorization](../issue-analysis/issue-code-categorization.md)
          + [Issue codes by source](../issue-analysis/issue-codes-by-source/README.md)
          + [Troubleshooting the output code](../issue-analysis/troubleshooting-the-output-code/README.md)
          + [Workarounds](../issue-analysis/workarounds.md)
          + [Deploying the output code](../issue-analysis/deploying-the-output-code.md)
        + Translation reference

          + [Translation reference overview](../translation-reference/translation-reference-overview.md)
          + [SIT tagging](../translation-reference/sit-tagging/README.md)
          + [SQL embedded code](../translation-reference/sql-embedded-code.md)
          + [HiveSQL](../translation-reference/hivesql/README.md)
          + [Spark SQL](../translation-reference/spark-sql/README.md)
        + Workspace estimator

          + [Overview](../workspace-estimator/overview.md)
          + [Getting started](../workspace-estimator/getting-started.md)
        + Interactive assessment application

          + [Overview](../interactive-assessment-application/overview.md)
          + [Installation guide](../interactive-assessment-application/installation-guide.md)
        + Support

          + [General troubleshooting](../support/general-troubleshooting/README.md)
          + [Frequently asked questions](../support/frequently-asked-questions-faq/README.md)
          + [Glossary](../support/glossary.md)
          + [Contact us](../support/contact-us.md)
    * Guides

      * [Teradata](../../guides/teradata.md)
      * [Databricks](../../guides/databricks.md)
      * [SQL Server](../../guides/sqlserver.md)
      * [Amazon Redshift](../../guides/redshift.md)
      * [Oracle](../../guides/oracle.md)
      * [Azure Synapse](../../guides/azuresynapse.md)
15. [Queries](../../../guides/overview-queries.md)
16. [Listings](../../../collaboration/collaboration-listings-about.md)
17. [Collaboration](../../../guides/overview-sharing.md)
19. [Snowflake AI & ML](../../../guides/overview-ai-features.md)
21. [Snowflake Postgres](../../../user-guide/snowflake-postgres/about.md)
23. [Alerts & Notifications](../../../guides/overview-alerts.md)
25. [Security](../../../guides/overview-secure.md)
26. [Data Governance](../../../guides/overview-govern.md)
27. [Privacy](../../../guides/overview-privacy.md)
29. [Organizations & Accounts](../../../guides/overview-manage.md)
30. [Business continuity & data recovery](../../../user-guide/replication-intro.md)
32. [Performance optimization](../../../guides/overview-performance.md)
33. [Cost & Billing](../../../guides/overview-cost.md)

[Guides](../../../guides/README.md)[Migrations](../../README.md)Tools[Snowpark Migration Accelerator](../README.md)Use casesSMA CLI walkthrough

# Snowpark Migration Accelerator: SMA CLI Walkthrough[¶](#snowpark-migration-accelerator-sma-cli-walkthrough "Link to this heading")

The [Snowpark Migration Accelerator (SMA)](https://www.snowflake.com/en/data-cloud/snowpark/migration-accelerator/) helps developers migrate their Python or Scala Spark code to Snowpark. It analyzes your code and:

1. Evaluates compatibility with Snowpark
2. Automatically converts compatible Spark API calls to Snowpark API
3. Identifies code that cannot be automatically converted
4. Creates an inventory of third-party library imports from scripts and notebooks
5. Generates an editable compatibility report comparing Spark and Snowpark code

Snowflake has released a Command Line Interface (CLI) for the Snowpark Migration Accelerator (SMA). This guide will demonstrate how to use the CLI both as a standalone tool and within a script.

## Using the CLI[¶](#using-the-cli "Link to this heading")

You can download the Command Line Interface (CLI) from [the Download and Access section](../general/getting-started/download-and-access.html#downloading-the-sma-command-line-interface-cli). Select the version that matches your operating system. You can store the CLI in any accessible location on your machine or container.

Note

**NOTE**: While this walkthrough uses screenshots from a Mac computer, the process is similar for Windows and Linux users.

After downloading the package file (.zip or .tar format), extract its contents. The Command Line Interface (CLI) tool is located in the “orchestrator” folder within the extracted files.

![SMA CLI in the Orchestrator Directory](../../../_images/OrchestratorDirectory.png)

Open a terminal or command prompt in the installation folder and verify the CLI installation by running the following command to check its version:

./sma –version

You will see results that look like this:

![SMA Version Information](../../../_images/versionInformation.png)

The SMA Command Line Interface (CLI) is a local application that runs on your computer, similar to the SMA desktop application. To analyze your code files using the SMA CLI, these files must be stored on your local machine where the CLI can access them. The CLI supports the same file types as the regular SMA application. For a complete list of supported file types, please refer to [the supported filetypes in the SMA documentation](../user-guide/before-using-the-sma/supported-filetypes).

Note

**NOTE**: To test the CLI functionality, you can use the sample codebase provided in [the Assessment](assessment-walkthrough/walkthrough-setup/README.html#sample-codebase) section or refer to the Conversion walkthroughs in the SMA documentation.

The SMA documentation contains a complete list of CLI arguments. Let’s explore the most important ones in this section.

The SMA CLI runs in [Conversion mode](../user-guide/conversion/README) by default, rather than [Assessment mode](../user-guide/assessment/README). To run the CLI in assessment mode, use [the -a argument](assessment-walkthrough/README). For conversion operations, you’ll need a valid access code. To verify if you have a valid access code, use the following command:

```
./sma show-ac
```

Copy

![License Information](../../../_images/licenseInformation.png)

If you need an access code, you can request one by following [the instructions in the SMA documentation](../user-guide/project-overview/configuration-and-settings.html#request-new-access-code). After receiving the code by email, use [the install access code](../user-guide/project-overview/configuration-and-settings.html#request-new-access-code) parameter in the CLI to complete the installation.

To run a conversion, you need to provide:

1. Input directory (required)
2. Output directory (required)

If you haven’t created a project file before, you’ll also need to provide:

* User email
* Organization name
* Project name

Once you’ve set up these parameters for the first time, you only need to specify the input and output directories for future conversions.

```
./sma -i '/your/INput/directory/path/here' -o '/your/OUTput/directory/path/here' -e your@email.com -c Your-Organization -p Your-Project-Name
```

Copy

This screen displays a summary of your execution settings and prompts you to confirm whether you want to proceed.

![Project Information Section](../../../_images/informationSection.png)

To skip the confirmation prompt, add the –yes or -y parameter. This is particularly important when running the CLI from automated scripts.

The tool provides detailed progress information during its execution.

![Project Information Printed](../../../_images/informationPrinted.png)

While the tool is running, it will continuously print output to the screen. When the process is complete, you will see the prompt again. The tool generates detailed output that includes all processes, issues, and completed or failed steps. You don’t need to read through all of this information while it’s running, as you can review it later in [the Logs output folder](../user-guide/assessment/output-logs).

## Viewing the Output[¶](#viewing-the-output "Link to this heading")

The SMA CLI produces the same output as the SMA application. When you run the tool, it creates three folders in your specified output directory:

* [Reports](../user-guide/assessment/output-reports/README)
* [Logs](../user-guide/assessment/output-logs)
* Output (contains the converted code)

![Output Directory from the SMA](../../../_images/outputDirectory.png)

For detailed guidance on working with code that has been converted by the Snowpark Migration Accelerator (SMA), please refer to [the conversion walkthrough](conversion-walkthrough).

## Running the CLI Programmatically[¶](#running-the-cli-programmatically "Link to this heading")

Coming soon! The SMA team will provide a script that enables you to run the SMA Command Line Interface (CLI) automatically across multiple directories.

---

Try out the Command Line Interface (CLI) today. If you need help or have questions, contact the Snowpark Migration Accelerator team at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com).

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

1. [Using the CLI](#using-the-cli)
2. [Viewing the Output](#viewing-the-output)
3. [Running the CLI Programmatically](#running-the-cli-programmatically)