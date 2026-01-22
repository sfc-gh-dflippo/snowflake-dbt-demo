---
auto_generated: true
description: Translation references to convert Teradata MLOAD files to Snowflake SQL
last_scraped: '2026-01-14T16:53:48.761260+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/teradata/scripts-to-snowflake-sql-translation-reference/mload
title: SnowConvert AI - Teradata - MLOAD | Snowflake Documentation
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

          + [About](../../../general/about.md)
          + [Getting Started](../../../general/getting-started/README.md)
          + [Terms And Conditions](../../../general/terms-and-conditions/README.md)
          + [Release Notes](../../../general/release-notes/release-notes/README.md)
          + User Guide

            + [SnowConvert AI](../../../general/user-guide/snowconvert/README.md)
            + [Project Creation](../../../general/user-guide/project-creation.md)
            + [Extraction](../../../general/user-guide/extraction.md)
            + [Deployment](../../../general/user-guide/deployment.md)
            + [Data Migration](../../../general/user-guide/data-migration.md)
            + [Data Validation](../../../general/user-guide/data-validation.md)
            + [Power BI Repointing](../../../general/user-guide/power-bi-repointing-general.md)
            + [ETL Migration](../../../general/user-guide/etl-migration-replatform.md)
          + [Technical Documentation](../../../general/technical-documentation/README.md)
          + [Contact Us](../../../general/contact-us.md)
          + Others

            + [Using SnowConvert AI In A Ubuntu Docker Image](../../../general/others/using-snowconvert-in-a-ubuntu-docker-image.md)
          + [Frequently Asked Questions (FAQ)](../../../general/frequently-asked-questions-faq.md)")
        + Translation References

          + [General](../../general/README.md)
          + [Teradata](../README.md)

            - [Data Migration Considerations](../data-migration-considerations.md)
            - [Session Modes in Teradata](../session-modes.md)
            - [Sql Translation Reference](../sql-translation-reference/README.md)
            - [SQL to JavaScript (Procedures)](../teradata-to-javascript-translation-reference.md)")
            - [SQL to Snowflake Scripting (Procedures)](../teradata-to-snowflake-scripting-translation-reference.md)")
            - [Scripts To Python](../scripts-to-python/README.md)
            - [Scripts to Snowflake SQL](README.md)

              * [BTEQ](bteq.md)
              * [Common statements](common-statements.md)
              * [MLOAD](mload.md)
            - ETL And BI Repointing

              - [Power BI Teradata Repointing](../etl-bi-repointing/power-bi-teradata-repointing.md)
          + [Oracle](../../oracle/README.md)
          + [SQL Server-Azure Synapse](../../transact/README.md)
          + [Sybase IQ](../../sybase/README.md)
          + [Hive-Spark-Databricks SQL](../../hive/README.md)
          + [Redshift](../../redshift/README.md)
          + [PostgreSQL-Greenplum-Netezza](../../postgres/README.md)
          + [BigQuery](../../bigquery/README.md)
          + [Vertica](../../vertica/README.md)
          + [IBM DB2](../../db2/README.md)
          + [SSIS](../../ssis/README.md)
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

[Guides](../../../../../guides/README.md)[Migrations](../../../../README.md)Tools[SnowConvert AI](../../../overview.md)Translation References[Teradata](../README.md)[Scripts to Snowflake SQL](README.md)MLOAD

# SnowConvert AI - Teradata - MLOAD[¶](#snowconvert-ai-teradata-mload "Link to this heading")

Translation references to convert Teradata MLOAD files to Snowflake SQL

## Import[¶](#import "Link to this heading")

### Description[¶](#description "Link to this heading")

> The IMPORT command specifies a source for data input.

For more information regarding Import MLoad, check [here](https://docs.teradata.com/r/Teradata-MultiLoad-Reference/May-2017/Teradata-MultiLoad-Commands/IMPORT)

### Sample Source Patterns[¶](#sample-source-patterns "Link to this heading")

As BTEQ content also MLoad is relocated in an `EXECUTE IMMEDIATE` block. Import transformation with take each layout field an added to a select. Inserts in dml label will be transform to **COPY INTO** and upserts (Update and insert) will be transform to **MERGE INTO.**

#### 1. DML label with insert[¶](#dml-label-with-insert "Link to this heading")

##### Teradata MLoad[¶](#teradata-mload "Link to this heading")

```
-- Additional Params: -q SnowScript
.LOGTABLE my_table_log;
.LOGON my_teradata_system/username,password;

BEGIN IMPORT MLOAD TABLES my_table
WORKTABLES my_table_work
ERRORTABLES my_table_err;

.LAYOUT my_layout;
.FIELD col1 * VARCHAR(2);
.FIELD col2 * VARCHAR(5);

.dml label insert_into_my_table
  IGNORE DUPLICATE INSERT ROWS ;
INSERT INTO my_table(col1, col2) VALUES (:col1, :col2);

.IMPORT INFILE C:\USER\user\my_tr_file_1.tr
  FORMAT UNFORMAT 
  LAYOUT my_layout APPLY insert_into_my_table;

.END MLOAD;
.LOGOFF;
```

Copy

##### Snowflake SQL[¶](#snowflake-sql "Link to this heading")

```
EXECUTE IMMEDIATE
$$
  DECLARE
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0);
  BEGIN
    -- Additional Params: -q SnowScript
    /*.LOGTABLE my_table_log;*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
     
    /*.LOGON my_teradata_system/username,password;*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
     
    /*BEGIN IMPORT MLOAD TABLES my_table
    WORKTABLES my_table_work*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
     
    /*** SSC-EWI-0001 - UNRECOGNIZED TOKEN ON LINE '7' COLUMN '1' OF THE SOURCE CODE STARTING AT 'ERRORTABLES'. EXPECTED 'STATEMENT' GRAMMAR. LAST MATCHING TOKEN WAS 'my_table_err' ON LINE '7' COLUMN '13'. CODE '81'. ***/
    /*--ERRORTABLES my_table_err*/
     
    /*.LAYOUT my_layout;*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE. INFORMATION MAY BE USED IN A TRANSFORMED IMPORT CLAUSE **
     
    /*.dml label insert_into_my_table
      IGNORE DUPLICATE INSERT ROWS ;*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE. INFORMATION MAY BE USED IN A TRANSFORMED IMPORT CLAUSE **
     
     
    BEGIN
      CREATE OR REPLACE STAGE &{stagename};
      PUT file://C:\USER\user\my_tr_file_1.tr &{stagename};
       
      COPY INTO my_table (
        col1,
        col2
      )
      FROM
      (
        SELECT DISTINCT
          SUBSTRING($1, 1, 2) col1,
          SUBSTRING($1, 3, 5) col2
        FROM
          @&{stagename}/my_tr_file_1.tr
      );
    END;
    /*.END MLOAD;*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
     
    /*.LOGOFF;*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
     
  END
$$
```

Copy

##### 2. DML label with upsert[¶](#dml-label-with-upsert "Link to this heading")

###### Teradata MLoad[¶](#id1 "Link to this heading")

```
-- Additional Params: -q SnowScript
.LOGTABLE my_table_log;
.LOGON my_teradata_system/username,password;

BEGIN IMPORT MLOAD TABLES my_table
WORKTABLES my_table_work
ERRORTABLES my_table_err;

.LAYOUT my_layout;
.FIELD col1 * VARCHAR(2);
.FIELD col2 * VARCHAR(5);

.dml label upsert_into_my_table;
UPDATE my_table  
 SET     
  col1 = :col1,     
  col2 = :col2  
 WHERE col2 = :col2 
INSERT INTO my_table (
col1, col2)  
VALUES (:col1, :col2);

.IMPORT INFILE C:\USER\user\my_tr_file_1.tr
  FORMAT UNFORMAT 
  LAYOUT my_layout APPLY upsert_into_my_table;

.END MLOAD;
.LOGOFF;
```

Copy

###### Snowflake SQL[¶](#id2 "Link to this heading")

```
EXECUTE IMMEDIATE
$$
  DECLARE
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0);
  BEGIN
    -- Additional Params: -q SnowScript
    /*.LOGTABLE my_table_log;*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
     
    /*.LOGON my_teradata_system/username,password;*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
     
    /*BEGIN IMPORT MLOAD TABLES my_table
    WORKTABLES my_table_work*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
     
    /*** SSC-EWI-0001 - UNRECOGNIZED TOKEN ON LINE '7' COLUMN '1' OF THE SOURCE CODE STARTING AT 'ERRORTABLES'. EXPECTED 'STATEMENT' GRAMMAR. LAST MATCHING TOKEN WAS 'my_table_err' ON LINE '7' COLUMN '13'. CODE '81'. ***/
    /*--ERRORTABLES my_table_err*/
     
    /*.LAYOUT my_layout;*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE. INFORMATION MAY BE USED IN A TRANSFORMED IMPORT CLAUSE **
     
    /*.dml label upsert_into_my_table;*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE. INFORMATION MAY BE USED IN A TRANSFORMED IMPORT CLAUSE **
     
     
     
    BEGIN
      CREATE OR REPLACE STAGE &{stagename};
      PUT file://C:\USER\user\my_tr_file_1.tr &{stagename};
       
      MERGE INTO my_table merge_table
      USING (
        SELECT
          SUBSTRING($1, 1, 2) col1,
          SUBSTRING($1, 3, 5) col2
        FROM
          @&{stagename}/my_tr_file_1.tr
      ) load_temp ON merge_table.col2 = load_temp.col2
      WHEN MATCHED THEN
        UPDATE SET
          merge_table.col1 = load_temp.col1,
          merge_table.col2 = load_temp.col2
      WHEN NOT MATCHED THEN
        INSERT (col1, col2)
        VALUES (load_temp.col1, load_temp.col2);
    END;
    /*.END MLOAD;*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
     
    /*.LOGOFF;*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
     
  END
$$
```

Copy

##### 3. Layout or DML label not found[¶](#layout-or-dml-label-not-found "Link to this heading")

###### Teradata MLoad[¶](#id3 "Link to this heading")

```
-- Additional Params: -q SnowScript
.LOGTABLE my_table_log;
.LOGON my_teradata_system/username,password;

BEGIN IMPORT MLOAD TABLES my_table
WORKTABLES my_table_work
ERRORTABLES my_table_err;

.LAYOUT my_layout;
.FIELD col1 * VARCHAR(2);
.FIELD col2 * VARCHAR(5);

.dml label insert_into_my_table
  IGNORE DUPLICATE INSERT ROWS ;
INSERT INTO my_table(col1, col2)VALUES (:col1, :col2);

.IMPORT INFILE C:\USER\user\my_tr_file_1.tr
  FORMAT UNFORMAT 
  LAYOUT not_layout APPLY insert_into_my_table;

.IMPORT INFILE C:\USER\user\my_tr_file_1.tr
  FORMAT UNFORMAT 
  LAYOUT my_layout APPLY insert_not_my_table;

.END MLOAD;
.LOGOFF;pl
```

Copy

###### Snowflake SQL[¶](#id4 "Link to this heading")

```
EXECUTE IMMEDIATE
$$
  DECLARE
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0);
  BEGIN
    -- Additional Params: -q SnowScript
    /*.LOGTABLE my_table_log;*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
     
    /*.LOGON my_teradata_system/username,password;*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
     
    /*BEGIN IMPORT MLOAD TABLES my_table
    WORKTABLES my_table_work*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
     
    /*** SSC-EWI-0001 - UNRECOGNIZED TOKEN ON LINE '7' COLUMN '1' OF THE SOURCE CODE STARTING AT 'ERRORTABLES'. EXPECTED 'STATEMENT' GRAMMAR. LAST MATCHING TOKEN WAS 'my_table_err' ON LINE '7' COLUMN '13'. CODE '81'. ***/
    /*--ERRORTABLES my_table_err*/
     
    /*.LAYOUT my_layout;*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE. INFORMATION MAY BE USED IN A TRANSFORMED IMPORT CLAUSE **
     
    /*.dml label insert_into_my_table
      IGNORE DUPLICATE INSERT ROWS ;*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE. INFORMATION MAY BE USED IN A TRANSFORMED IMPORT CLAUSE **
     
     
     
--      .IMPORT INFILE C:\USER\user\my_tr_file_1.tr FORMAT UNFORMAT LAYOUT not_layout APPLY insert_into_my_table
                                                                                                              ;
    BEGIN
      CREATE OR REPLACE STAGE &{stagename};
      PUT file://C:\USER\user\my_tr_file_1.tr &{stagename};
       
    END;
    /*.END MLOAD;*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
     
    /*.LOGOFF;*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
     
    /*** SSC-EWI-0001 - UNRECOGNIZED TOKEN ON LINE '26' COLUMN '9' OF THE SOURCE CODE STARTING AT 'pl'. EXPECTED 'STATEMENT' GRAMMAR. LAST MATCHING TOKEN WAS 'pl' ON LINE '26' COLUMN '9'. CODE '81'. ***/
    /*--pl*/
     
  END
$$
```

Copy

##### 4. Conditions not found in update statement[¶](#conditions-not-found-in-update-statement "Link to this heading")

###### Teradata MLoad[¶](#id5 "Link to this heading")

```
-- Additional Params: -q SnowScript
.LOGTABLE my_table_log;
.LOGON my_teradata_system/username,password;

BEGIN IMPORT MLOAD TABLES my_table
WORKTABLES my_table_work
ERRORTABLES my_table_err;

.LAYOUT my_layout;
.FIELD col1 * VARCHAR(2);
.FIELD col2 * VARCHAR(5);

.dml label upsert_into_my_table;
UPDATE my_table  
 SET     
  col1 = :col1,     
  col2 = :col2
INSERT INTO my_table (
col1, col2)  
VALUES (:col1, :col2);

.IMPORT INFILE C:\USER\user\my_tr_file_1.tr
  FORMAT UNFORMAT 
  LAYOUT my_layout APPLY upsert_into_my_table;

.END MLOAD;
.LOGOFF;
```

Copy

###### Snowflake SQL[¶](#id6 "Link to this heading")

```
EXECUTE IMMEDIATE
$$
  DECLARE
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0);
  BEGIN
    -- Additional Params: -q SnowScript
    /*.LOGTABLE my_table_log;*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
     
    /*.LOGON my_teradata_system/username,password;*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
     
    /*BEGIN IMPORT MLOAD TABLES my_table
    WORKTABLES my_table_work*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
     
    /*** SSC-EWI-0001 - UNRECOGNIZED TOKEN ON LINE '7' COLUMN '1' OF THE SOURCE CODE STARTING AT 'ERRORTABLES'. EXPECTED 'STATEMENT' GRAMMAR. LAST MATCHING TOKEN WAS 'my_table_err' ON LINE '7' COLUMN '13'. CODE '81'. ***/
    /*--ERRORTABLES my_table_err*/
     
    /*.LAYOUT my_layout;*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE. INFORMATION MAY BE USED IN A TRANSFORMED IMPORT CLAUSE **
     
    /*.dml label upsert_into_my_table;*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE. INFORMATION MAY BE USED IN A TRANSFORMED IMPORT CLAUSE **
     
     
     
     
--      .IMPORT INFILE C:\USER\user\my_tr_file_1.tr FORMAT UNFORMAT LAYOUT my_layout APPLY upsert_into_my_table
                                                                                                             ;
    /*.END MLOAD;*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
     
    /*.LOGOFF;*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
     
  END
$$
```

Copy

### Known Issues[¶](#known-issues "Link to this heading")

Some statements from import clause where not supported yet:

* AXSMOD statement
* INMODE statement
* FORMAT (only FORMAT UNFORMAT is supported)
* WHERE condition of APPLY label

### Related EWIS[¶](#related-ewis "Link to this heading")

1. [SSC-EWI-0001](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0001): Unrecognized token on the line of the source code.
2. [SSC-FDM-0027](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0027): Removed next statement, not applicable in SnowFlake.

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

1. [Import](#import)