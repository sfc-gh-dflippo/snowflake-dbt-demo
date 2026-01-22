---
auto_generated: true
description: 'Using the Linux Command Line Interface (CLI) for Snowpark Migration
  Accelerator with Docker: A Step-by-Step Guide'
last_scraped: '2026-01-14T16:51:33.711365+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/sma-docs/use-cases/using-snowconvert-in-a-ubuntu-docker-image
title: 'Snowpark Migration Accelerator:  Using SMA with Docker | Snowflake Documentation'
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

[Guides](../../../guides/README.md)[Migrations](../../README.md)Tools[Snowpark Migration Accelerator](../README.md)Use casesUsing SMA in an Ubuntu Docker image

# Snowpark Migration Accelerator: Using SMA with Docker[¶](#snowpark-migration-accelerator-using-sma-with-docker "Link to this heading")

Using the Linux Command Line Interface (CLI) for Snowpark Migration Accelerator with Docker: A Step-by-Step Guide

## Dependencies[¶](#dependencies "Link to this heading")

The following software must be installed on your computer before proceeding:

* [Docker desktop](https://docs.docker.com/desktop/windows/install/)
* [Visual Code](https://code.visualstudio.com/download)
* [Docker Extension in Visual Code](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker)

## Steps[¶](#steps "Link to this heading")

### Create the image config file[¶](#create-the-image-config-file "Link to this heading")

Create a file named “Dockerfile” (without a file extension). This file will contain the configuration needed to build the Docker image.

```
FROM ubuntu
COPY snowCli /dockerDestinationFolder
ENV DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=1
RUN apt-get update
RUN apt-get install -y ca-certificates openssl
```

Copy

When using the [Ubuntu](https://hub.docker.com/_/ubuntu) image to run the Snowpark Migration Accelerator CLI for Linux, you need to add two dependencies to the Dockerfile:

1. Enable [System.Globalization.Invariant](https://docs.microsoft.com/en-us/dotnet/core/run-time-config/globalization) setting
2. Install OpenSSL

These dependencies are required to activate the license and establish a secure HTTPS connection for license validation.

In addition to installing dependencies, the `COPY` command copies files from your local machine into the Docker image. For example, the *snowCLI* file (which must be in the same directory as the Dockerfile) will be copied to `/dockerDestinationFolder` within the Docker image.

### Build the image[¶](#build-the-image "Link to this heading")

Start the Docker Desktop application.

Open Visual Studio Code and locate the “Dockerfile”. If you have the Docker extension installed in Visual Studio Code, it will automatically recognize the Dockerfile as a Docker configuration file. To build the Docker image, right-click on the “Dockerfile” and select “Build image…”

![](../../../_images/image%28251%29.png)

Enter a name for the image when prompted at the top of Visual Studio Code.

![](../../../_images/image%28191%29.png)

Enter any name and press “Enter.” Docker will then create the container by downloading the Ubuntu image, installing required dependencies, and copying the specified files. Wait for the terminal to complete the process. A success message will appear when the image has been built correctly.

```
> Executing task: docker build --pull --rm -f "Dockerfile" -t release:Ubuntu "." <

[+] Build completed in 2.0 seconds. All 11 tasks finished successfully.
```

Copy

### Run the image[¶](#run-the-image "Link to this heading")

Launch the recently created image by navigating to the Images tab in Docker Desktop and clicking the Run button.

![](../../../_images/image%28201%29.png)

In Visual Studio Code, navigate to the Docker tab. Under the “Containers” section, you will find the recently executed image. Click the arrow next to it to expand and browse through its file directory structure.

![](../../../_images/image%28336%29.png)

### Connect to the container[¶](#connect-to-the-container "Link to this heading")

Finally, to access the container’s command line interface, right-click on the running container and select “Attach shell”. This will open a Terminal window where you can execute any command you need.

![](../../../_images/image%28143%29.png)

You will find your personal files in this location. These files were previously selected for copying using the COPY command in the configuration file.

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

1. [Dependencies](#dependencies)
2. [Steps](#steps)