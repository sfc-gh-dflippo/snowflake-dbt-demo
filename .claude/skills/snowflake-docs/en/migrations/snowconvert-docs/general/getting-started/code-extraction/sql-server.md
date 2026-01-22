---
auto_generated: true
description: The first step for migration is getting the code that you need to migrate.
  There are many ways to extract the code from your database. However, we highly recommend
  using SQL Server Management Studio (
last_scraped: '2026-01-14T16:52:16.371948+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/general/getting-started/code-extraction/sql-server
title: SnowConvert AI - SQL Server | Snowflake Documentation
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
          + [Getting Started](../README.md)

            - [System Requirements](../system-requirements.md)
            - [Best Practices](../best-practices.md)
            - [Download And Access](../download-and-access.md)
            - [Code Extraction](README.md)

              * [Oracle](oracle.md)
              * [Teradata](teradata.md)
              * [Redshift](redshift.md)
              * [SQL Server](sql-server.md)
              * [Sybase IQ](sybase-iq.md)
            - [Running Snowconvert AI](../running-snowconvert/README.md)
            - [Training And Support](../training-and-support.md)
          + [Terms And Conditions](../../terms-and-conditions/README.md)
          + [Release Notes](../../release-notes/release-notes/README.md)
          + User Guide

            + [SnowConvert AI](../../user-guide/snowconvert/README.md)
            + [Project Creation](../../user-guide/project-creation.md)
            + [Extraction](../../user-guide/extraction.md)
            + [Deployment](../../user-guide/deployment.md)
            + [Data Migration](../../user-guide/data-migration.md)
            + [Data Validation](../../user-guide/data-validation.md)
            + [Power BI Repointing](../../user-guide/power-bi-repointing-general.md)
            + [ETL Migration](../../user-guide/etl-migration-replatform.md)
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

[Guides](../../../../../guides/README.md)[Migrations](../../../../README.md)Tools[SnowConvert AI](../../../overview.md)General[Getting Started](../README.md)[Code Extraction](README.md)SQL Server

# SnowConvert AI - SQL Server[¶](#snowconvert-ai-sql-server "Link to this heading")

The first step for migration is getting the code that you need to migrate. There are many ways to extract the code from your database. However, we highly recommend using [SQL Server Management Studio (SSMS)](https://learn.microsoft.com/en-us/sql/ssms/download-sql-server-management-studio-ssms?view=sql-server-ver16), nevertheless we provide an alternative for MacOS and Linux environments.

## Prerequisites[¶](#prerequisites "Link to this heading")

* Access to a server with an SQLServer database.

## Extraction Via SQL Server Management Studio (SSMS)[¶](#extraction-via-sql-server-management-studio-ssms "Link to this heading")

SQL Server Management Studio (SSMS) is only available for Windows. Go to the next section for Mac OS and Linux.

1. Open SSMS.
2. Connect to the desired server and server instance with credentials that allow
   visibility of the desired database(s).
3. In the main SSMS window, open **Object Explorer** if not already opened.
4. In the Object Explorer pane, expand **Databases** if not already expanded.
5. Right-click on the desired database and select **Tasks** -> **Generate Scripts**…

![Step1](../../../../../_images/Step1.png)

6. If the Introduction page of the Generate Scripts dialog is shown, click **Next**. Otherwise, proceed to the next step.

![Step2](../../../../../_images/Step2.png)

7. On the Choose Objects page of the Generate Scripts dialog:

* Select the **Select specific database objects** radio button and put a **check** in all the database object type **checkboxes** displayed **EXCEPT Users** (NOTE: the list of database object types presented depends on the presence of database objects in the chosen database. Thus, your list of database object types may look different. Just select all database object types EXCEPT Users).
* Click **Next**

![Step3](../../../../../_images/Step3.png)

8. On the Set Scripting Options page of the Generate Scripts dialog:

* Click the **Save as script file** button and **One script file per object**

![Step4](../../../../../_images/Step4.png)

* Click the **Advanced** button.

* In the Advanced Scripting Options dialog box, make sure the following Options are set as indicated, keeping the default for all other Option

![Step5](../../../../../_images/Step5.png)

| Section | Setting. | Value |
| --- | --- | --- |
| General | Include System Constraint names | True |
| empty | Script Extended Properties | True |
| Table/View Options | Script Indexes | True |
| - | Script Triggers | True |

* When done, click **OK** to return to the Set Scripting Options window of the Generate Scripts dialog.

* Select the **Save as script file** radio button.
* Click the **ellipsis** (…) to the right of the File name: field.
* Navigate to a suitable location, enter a descriptive value (e.g.,**<server\_name>**\_**<instance\_name>**\_**<database\_name>**) in the File Name: field, and click Save.
* Select the **ANSI text** radio button.
* Click Next.

9. On the Summary page of the Generate Scripts dialog, confirm the settings are correct and click **Next >** when ready to start the extraction (i.e., the extraction will
   commence when you click **Next >**). The Save Scripts page will appear and will show the extraction progress.

![Step6](../../../../../_images/Step6.png)

10. On the Save Scripts page of the Generate Scripts dialog box (not shown), confirm all Results were Success and click **Finish**.
11. Repeat steps 5 through 10 for each desired database (using a different file name for each). When all databases have been extracted successfully, proceed to the next step.
12. Transmit the resulting file(s) to Snowflake for further analysis.

### Package the results[¶](#package-the-results "Link to this heading")

When the extraction process is finished, compress the results and send them over.

## Table sizing report[¶](#table-sizing-report "Link to this heading")

1. Option A: For all databases in scope, right click on the database, Reports >
   Standard Reports > Disk Usage By Table. A report will be generated, right click on
   the report and export as Excel.

![Step6](../../../../../_images/TableSizing.png)

2. Option B: Run the following script:

```
USE <DB_NAME>;
SELECT
 t.NAME AS TableName,
 s.NAME AS SchemaName,
 SUM(a.total_pages) * 8 / 1024 AS TotalSpaceMB,
 SUM(a.used_pages) * 8 / 1024 AS UsedSpaceMB,
 (SUM(a.total_pages) - SUM(a.used_pages)) * 8 / 1024 AS
UnusedSpaceMB
FROM
 sys.tables t
INNER JOIN
 sys.indexes i ON t.OBJECT_ID = i.object_id
INNER JOIN
 sys.partitions p ON i.object_id = p.OBJECT_ID AND i.index_id =
p.index_id
INNER JOIN
 sys.allocation_units a ON p.partition_id = a.container_id
LEFT OUTER JOIN
 sys.schemas s ON t.schema_id = s.schema_id
GROUP BY
 t.NAME, s.NAME, p.Rows
ORDER BY
 TotalSpaceMB DESC;
```

Copy

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

1. [Prerequisites](#prerequisites)
2. [Extraction Via SQL Server Management Studio (SSMS)](#extraction-via-sql-server-management-studio-ssms)
3. [Table sizing report](#table-sizing-report)