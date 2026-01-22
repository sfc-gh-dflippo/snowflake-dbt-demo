---
auto_generated: true
description: 'The following dependencies must be installed on the machine:'
last_scraped: '2026-01-14T16:52:34.223787+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/general/others/using-snowconvert-in-a-ubuntu-docker-image
title: SnowConvert AI - How to Use SnowConvert AI with Docker | Snowflake Documentation
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

      * [SnowConvert AI](../../overview.md)

        + General

          + [About](../about.md)
          + [Getting Started](../getting-started/README.md)
          + [Terms And Conditions](../terms-and-conditions/README.md)
          + [Release Notes](../release-notes/release-notes/README.md)
          + User Guide

            + [SnowConvert AI](../user-guide/snowconvert/README.md)
            + [Project Creation](../user-guide/project-creation.md)
            + [Extraction](../user-guide/extraction.md)
            + [Deployment](../user-guide/deployment.md)
            + [Data Migration](../user-guide/data-migration.md)
            + [Data Validation](../user-guide/data-validation.md)
            + [Power BI Repointing](../user-guide/power-bi-repointing-general.md)
            + [ETL Migration](../user-guide/etl-migration-replatform.md)
          + [Technical Documentation](../technical-documentation/README.md)
          + [Contact Us](../contact-us.md)
          + Others

            + [Using SnowConvert AI In A Ubuntu Docker Image](using-snowconvert-in-a-ubuntu-docker-image.md)
          + [Frequently Asked Questions (FAQ)](../frequently-asked-questions-faq.md)")
        + Translation References

          + [General](../../translation-references/general/README.md)
          + [Teradata](../../translation-references/teradata/README.md)
          + [Oracle](../../translation-references/oracle/README.md)
          + [SQL Server-Azure Synapse](../../translation-references/transact/README.md)
          + [Sybase IQ](../../translation-references/sybase/README.md)
          + [Hive-Spark-Databricks SQL](../../translation-references/hive/README.md)
          + [Redshift](../../translation-references/redshift/README.md)
          + [PostgreSQL-Greenplum-Netezza](../../translation-references/postgres/README.md)
          + [BigQuery](../../translation-references/bigquery/README.md)
          + [Vertica](../../translation-references/vertica/README.md)
          + [IBM DB2](../../translation-references/db2/README.md)
          + [SSIS](../../translation-references/ssis/README.md)
        + [Migration Assistant](../../migration-assistant/README.md)
        + [Data Validation CLI](../../data-validation-cli/index.md)
        + [AI Verification](../../snowconvert-ai-verification.md)
      * [Snowpark Migration Accelerator](../../../sma-docs/README.md)
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)GeneralOthersUsing SnowConvert AI In A Ubuntu Docker Image

# SnowConvert AI - How to Use SnowConvert AI with Docker[¶](#snowconvert-ai-how-to-use-snowconvert-ai-with-docker "Link to this heading")

## Dependencies[¶](#dependencies "Link to this heading")

The following dependencies must be installed on the machine:

* [Docker desktop](https://docs.docker.com/desktop/windows/install/)
* [Visual Code](https://code.visualstudio.com/download)
* [Docker Extension in Visual Code](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker)

## Steps[¶](#steps "Link to this heading")

### Create the image config file[¶](#create-the-image-config-file "Link to this heading")

Create a file called *“Dockerfile” (no extension)* with the following content. This configuration will be used to build the Docker image.

```
FROM ubuntu
COPY snowCli /dockerDestinationFolder
ENV DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=1
RUN apt-get update
RUN apt-get install -y ca-certificates openssl
```

Copy

When using the [Ubuntu](https://hub.docker.com/_/ubuntu) image to run the SnowConvert AI CLI for Linux a couple of dependencies must be added to the Dockerfile in order to activate the license, for this purpose [System.Globalization.Invariant](https://docs.microsoft.com/en-us/dotnet/core/run-time-config/globalization) must be turned ON and the OpenSSL must be installed to be able to establish an HTTPS connection for the license validation.

In addition to the dependencies installation, the second line (`COPY` command) is used to copy files from the local machine inside the image. In this case, the *snowCLI* file (located in the same folder as the Dockerfile) will be copied to`/dockerDestinationFolder`inside the image.

### Build the image[¶](#build-the-image "Link to this heading")

Launch Docker Desktop app.

Open Visual Code where the “*Dockerfile”* is located. If you have previously installed the Docker extension for Visual Code, the *“Dockerfile”* will be automatically recognized as a docker configuration file by Visual Code. Right-click on the “Dockerfile” and hit *“Build image…”*

![](../../../../_images/image%28212%29.png)

This will prompt for a name to give the image, at the top of Visual Code.

![](../../../../_images/image%28152%29.png)

Use any name you want and hit “*Enter”.* That causes Docker to set up the container, by pulling the Ubuntu image, installing dependencies, copying the specified files. Wait for the terminal to finish. Once you see a message like this one, it means the image was successfully built.

```
> Executing task: docker build --pull --rm -f "Dockerfile" -t release:Ubuntu "." <

[+] Building 2.0s (11/11) FINISHED                                                                                           0.0s 
.
.
.
```

Copy

### Run the image[¶](#run-the-image "Link to this heading")

Go to Docker Desktop in the Images tab, and hit run on the recently created image.

![](../../../../_images/image%28162%29.png)

Go back to Visual Code, and go to the Docker tab. You should see, under *Containers* the image that was just run. You can expand it and explore the file directory.

![](../../../../_images/image%28297%29.png)

### Connect to the container[¶](#connect-to-the-container "Link to this heading")

Finally, if you right-click on the running container and hit *“Attach shell”* you will be able to connect to the container in the Terminal and use all your favorite commands.

![](../../../../_images/image%28104%29.png)

You should see your personal files here that were specified to be copied by the COPY command in the configuration file.

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

1. [Dependencies](#dependencies)
2. [Steps](#steps)