---
auto_generated: true
description: This section guides you through deploying the Interactive Assessment
  Application (IAA) in your Snowflake account. The IAA is a Streamlit app that leverages
  the power of Snowflake within Snowflake to a
last_scraped: '2026-01-14T16:51:20.837629+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/sma-docs/interactive-assessment-application/installation-guide
title: 'Snowpark Migration Accelerator: Interactive Assessment Application Installation
  Guide | Snowflake Documentation'
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

            + [SMA checkpoints walkthrough](../use-cases/sma-checkpoints-walkthrough/README.md)
            + [SMA EWI Assistant walkthrough](../use-cases/sma-ewi-assistant-walkthrough/README.md)
          + [Assessment walkthrough](../use-cases/assessment-walkthrough/README.md)
          + [Conversion walkthrough](../use-cases/conversion-walkthrough.md)
          + [Migration lab](../use-cases/migration-lab/README.md)
          + [Sample project](../use-cases/sample-project.md)
          + [Using SMA in an Ubuntu Docker image](../use-cases/using-snowconvert-in-a-ubuntu-docker-image.md)
          + [SMA CLI walkthrough](../use-cases/sma-cli-walkthrough.md)
          + [Snowpark Connect](../use-cases/snowpark-connect/README.md)
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

          + [Overview](overview.md)
          + [Installation guide](installation-guide.md)
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

[Guides](../../../guides/README.md)[Migrations](../../README.md)Tools[Snowpark Migration Accelerator](../README.md)Interactive assessment applicationInstallation guide

# Snowpark Migration Accelerator: Interactive Assessment Application Installation Guide[¶](#snowpark-migration-accelerator-interactive-assessment-application-installation-guide "Link to this heading")

This section guides you through deploying the Interactive Assessment Application (IAA) in your Snowflake account. The IAA is a Streamlit app that leverages the power of Snowflake within Snowflake to analyze the output data from the Snowpark Migration Accelerator (SMA). This document provides the necessary steps and resources to analyze your workload within your Snowflake environment using the IAA.

## Step-by-step Guide[¶](#step-by-step-guide "Link to this heading")

Before deploying the IAA, ensure you have the following prerequisites:

* You have executed the [SMA](../user-guide/assessment/output-reports/README) have the output data ready for analysis.
* You have a Snowflake account. (This is required to host and run the IAA.) If not, a [Snowflake Trial Account](https://signup.snowflake.com/?utm_cta=sit-iaa-signup?) will work.
* You have VSCode or Jupyter installed to run the notebook: [VSCode](https://code.visualstudio.com/) or [Jupyter](https://jupyter.org/).
* Ensure you have Python 3.11 or later installed. This version is required for compatibility with the IAA notebook.

  + You may already have Python installed on your system. If not, follow one of the options below.

    - For Linux or Mac, you can use the script: [deployment/pre\_req\_install\_python\_3.sh](https://github.com/Snowflake-Labs/IAA-Support/blob/main/deployment/pre_req_install_python_3.sh).
    - For Windows, you can get it from the [official Python website](https://www.python.org/downloads/) if you don’t have Python.
    - Another alternative is to install with Miniconda [docs.conda.io](https://docs.conda.io/projects/miniconda/en/latest/)

Uploading all the mappings table might take longer than selecting just the latest. We recomend uploading the latest if you are not interest in comparing your execution with previous versions

In VS Code you can select the Map folder, that contains all the folders with the APIs and EWIs versions and delete those that you would not like to upload, in this case you can leave only the 7.1.2 version.

![Mappings available to upload](../../../_images/image%28556%29.png)

Once you’ve completed checking the prerequisites, proceed to Deployment.

## Let’s deploy the IAA!

Note

**This step by step guide applies to VS Code**

### Repository[¶](#repository "Link to this heading")

1. Go to the Snowflake Labs’ open-source GitHub: [https://github.com/Snowflake-Labs/IAA-Support](https://www.google.com/url?q=https://www.google.com/url?q=https://github.com/Snowflake-Labs/IAA-Support&amp;source=gmail&amp;sa=D&amp;sa=E&amp;source=gmail&amp;sa=D&amp;sa=E).
2. Click the “Code” button, and copy your preferred method for cloning the repository (e.g., HTTPS or SSH)
3. Choose the directory where you want to save the repository on your local machine, if applicable

### Executing the Notebook in VS Code[¶](#executing-the-notebook-in-vs-code "Link to this heading")

Note

Note: This deployment process uses the Snowflake CLI.

1. Open the downloaded repo in the VSCode environment.
2. In VS Code click `Yes, I trust the authors`

### iaa\_config.toml file[¶](#iaa-config-toml-file "Link to this heading")

**Part 1**: Getting Credentials from “Connect a tool to Snowflake”

1. In your Snowflake account, click your initials in the bottom-left corner.
2. Select “Connect a tool to Snowflake”.
3. Open the file `iaa\_config.toml`.
4. Copy the following information from the “Connect a tool to Snowflake” window and paste it into the `iaa\_config.toml` file:

   1. Account Identifier
   2. User Name

**Part 2:** Providing Additional Details

In the `iaa\_config.toml` file, also provide the following information:

1. Password: Enter your Snowflake password.
2. Database Name: Enter the name of the database you want to use for the IAA.
3. Schema Name: Enter the name of the schema you want to use for the IAA.
4. Warehouse Name: Enter the name of the warehouse running in your Snowflake account.

Save the changes in the `iaa\_config.toml` file.

Warning

Warning: The cell that validates the connection entries may fail if the .toml information is wrong, in that case, verify the input information.

### Kernel[¶](#kernel "Link to this heading")

In order to executes the .ipynb file you need to install the Python and Jupyter extensions in VS Code.

1. Select the python environment that comply with the version required to execute the notebook. (3.11 or later).

### Executing the Notebook[¶](#executing-the-notebook "Link to this heading")

To deploy the app in your Snowflake account, please select “Run all” the cells.

These cells configure automatically the local environment and establish the connection to your Snowflake account to prepare for the Streamlit app deployment. Specifically, these cells will:

1. Verify the Python3.11 requirement
2. Verify check the Snowflake CLI Requirement
3. Execute the iaa\_config.toml file is executed to connect with the Snowflake Account Configuration:

   1. Read the local .toml file
   2. Validate connection Entries
   3. Establish a connection to Snowflake
4. Prepare the environment to deploy the Streamlit app in Snowflake

   1. Configure local environment
   2. Retrieve Connection Entries
5. Deploy the Streamlit app to Snowflake using the Snowflake CLI:

   1. Deploy the App Schema to SiS.
   2. Deploy the Maps Stage to SiS.
   3. Deploy the APP to SiS.
   4. Refresh the Deployment
   5. Retrieve the app information and provide an access button.

   That’s it! It’s time to upload your output.

## It is time to upload your SMA Output! [¶](#it-is-time-to-upload-your-sma-output "Link to this heading")

Locate the SMA output zip file, named in the format ‘AssessmentFiles\_\*.zip’, in the output folder.

1. Go to your Snowflake Account

```
Data > Databases > [Your IAA Database] > Stages > SMA_EXECUTIONS
```

Copy

![SMA_EXECUTIONS stage in your Snowflake account.](../../../_images/explore_executions_upload_sma_output.png)

2. Upload your *AssessmentFiles.zip.*

![Uploading SMA output into the SMA_EXECUTIONS stage](../../../_images/explore_executions_upload_assessmentFiles.png)

3. Open the IAA to explore your execution information. This step can take around 30 seconds.

![IAA](../../../_images/explore_executions_open_iaa.png)

4. Once open the IAA the landing page will look like this:

![IAA Landing Page](../../../_images/iaa_landing.png)

Now you can explore your execution using the IAA.

## Exploring the IAA[¶](#exploring-the-iaa "Link to this heading")

The Interactive Assessment Application (IAA) is now installed in your Snowflake account. You have successfully uploaded your SMA output executions and are ready to explore the compatibility of your Spark code with Snowpark.

Note

Remember how to access the IAA in your Snowflake account:

`Projects > Streamlit > Interactive Assessment Application`

The IAA will allow you to identify which parts of your code are directly compatible and which parts require manual intervention or further optimization. It is recommended touse the latest SMA version. However, if you have older executions, the IAA will compare them against the latest API mapping versions.

## Navigating the IAA[¶](#navigating-the-iaa "Link to this heading")

There are 2 differents sections in the IAA. Explore my executions and Explore the compatibility between Spark and Snowpark

![IAA home screen.](../../../_images/image%28555%29.png)

### Explore my executions[¶](#explore-my-executions "Link to this heading")

Select an execution from the list. Your selection will be maintained as you navigate through the different sections of the IAA.

![Select an execution](../../../_images/select-execution.png)

A readiness score will be provided for:

* Spark API
* Third-Party
* SQL

Code metrics by technology:

* Total lines of code
* Total files

![Readiness Scores](../../../_images/image%28554%29.png)

In the left bar you can navigate throught the sections that will guide you to understand how to better plan your migration.

![Navigate](../../../_images/image%28553%29.png)

### Explore the compatibility between Spark and Snowpark. [¶](#explore-the-compatibility-between-spark-and-snowpark "Link to this heading")

How compatible is my Spark code to Snowpark?

This section provides access to the latest API mappings to Spark, PySpark, and Pandas. The SMA team researches these mapping tables and reflects the current compatibility status for each unique element shown below.

![Available mapping tables.](../../../_images/image%28557%29.png)

This tables helps users to assess compatibility between the source API and/or the third party libraries to Snowflake library/ Snowpark API:

* API Module Mappings
* Spark API Mappings
* PySpark API Mappings
* Pandas API Mappings

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

1. [Step-by-step Guide](#step-by-step-guide)
2. [Let’s deploy the IAA!](#)
3. [It is time to upload your SMA Output!](#it-is-time-to-upload-your-sma-output)
4. [Exploring the IAA](#exploring-the-iaa)
5. [Navigating the IAA](#navigating-the-iaa)