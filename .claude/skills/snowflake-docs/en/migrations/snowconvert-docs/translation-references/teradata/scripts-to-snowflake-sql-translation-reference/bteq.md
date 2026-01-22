---
auto_generated: true
description: Translation references to convert Teradata BTEQ files to Snowflake SQL
last_scraped: '2026-01-14T16:53:48.034383+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/teradata/scripts-to-snowflake-sql-translation-reference/bteq
title: SnowConvert AI - Teradata - BTEQ | Snowflake Documentation
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

[Guides](../../../../../guides/README.md)[Migrations](../../../../README.md)Tools[SnowConvert AI](../../../overview.md)Translation References[Teradata](../README.md)[Scripts to Snowflake SQL](README.md)BTEQ

# SnowConvert AI - Teradata - BTEQ[¶](#snowconvert-ai-teradata-bteq "Link to this heading")

Translation references to convert Teradata BTEQ files to Snowflake SQL

## Description[¶](#description "Link to this heading")

Note

Some parts in the output code are omitted for clarity reasons.

> Basic Teradata Query (BTEQ) is a general-purpose, command-based program that enables users on a workstation to communicate with one or more Teradata Database systems and to format reports for both print and screen output.

For more information regarding BTEQ, check [here](https://docs.teradata.com/r/Basic-Teradata-Query-Reference/October-2018).

### Sample Source Patterns[¶](#sample-source-patterns "Link to this heading")

#### 1. Basic BTEQ Example[¶](#basic-bteq-example "Link to this heading")

The BTEQ content is relocated within an `EXECUTE IMMEDIATE` block of to transfer the BTEQ script functionality to Snowflake SQL executable code.

All the DML and DDL statements inside BTEQ scripts are supported by SnowConvert AI and successfully translated to Snowflake SQL. The commands that do not have support yet, or do not have support at all, are being marked with a warning message and commented out.

##### Teradata BTEQ[¶](#teradata-bteq "Link to this heading")

```
 -- Additional Params: -q SnowScript
.LOGON 0/dbc,dbc;
   DATABASE tduser;

   CREATE TABLE employee_bkup ( 
      EmployeeNo INTEGER, 
      FirstName CHAR(30), 
      LastName CHAR(30), 
      DepartmentNo SMALLINT, 
      NetPay INTEGER 
   )
   Unique Primary Index(EmployeeNo);

   DROP TABLE employee_bkup;

   .IF ERRORCODE <> 0 THEN .EXIT ERRORCODE; 
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
    --.LOGON 0/dbc,dbc
    !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'BTLogOn' NODE ***/!!!
    null;
    BEGIN
      USE DATABASE tduser;
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLROWCOUNT', SQLROWCOUNT);
    EXCEPTION
      WHEN OTHER THEN
        STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
    END;
    BEGIN
      CREATE OR REPLACE TABLE employee_bkup (
        EmployeeNo INTEGER,
        FirstName CHAR(30),
        LastName CHAR(30),
        DepartmentNo SMALLINT,
        NetPay INTEGER,
        UNIQUE (EmployeeNo)
      );
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLROWCOUNT', SQLROWCOUNT);
    EXCEPTION
      WHEN OTHER THEN
        STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
    END;
    BEGIN
      DROP TABLE employee_bkup;
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLROWCOUNT', SQLROWCOUNT);
    EXCEPTION
      WHEN OTHER THEN
        STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
    END;
    IF (STATUS_OBJECT['SQLCODE'] /*** SSC-FDM-TD0013 - THE SNOWFLAKE ERROR CODE MISMATCH THE ORIGINAL TERADATA ERROR CODE ***/ != 0) THEN
      RETURN STATUS_OBJECT['SQLCODE'] /*** SSC-FDM-TD0013 - THE SNOWFLAKE ERROR CODE MISMATCH THE ORIGINAL TERADATA ERROR CODE ***/;
    END IF;
    --.LOGOFF
    !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'LogOff' NODE ***/!!!
    null;
  END
$$
```

Copy

#### 2. Bash Variable Placeholders Example[¶](#bash-variable-placeholders-example "Link to this heading")

SnowConvert AI supports the migration of BTEQ code with Bash Variable Placeholders used for shell scripts, these placeholders will be migrated to its SnowSQL equivalent and [SSC-FDM-TD0003](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/teradataFDM.html#ssc-fdm-td0003) will be added to the code. Please consider the following when migrating code with these placeholders:

* SnowConvert AI does **not** support the migration of shell scripts, to migrate the BTEQ code please isolate it in a BTEQ file and supply it as input for the tool.
* SnowSQL with variable substitution enabled is required to execute the migrated code, for more information on how to use SnowSQL please check [SSC-FDM-TD0003](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/teradataFDM.html#ssc-fdm-td0003) and the [official documentation for SnowSQ](https://docs.snowflake.com/en/user-guide/snowsql-use.html#using-snowsql)L.

##### Teradata BTEQ[¶](#id1 "Link to this heading")

```
 -- Additional Params: -q SnowScript
.LOGON dbc, dbc;

DATABASE testing;

SELECT $columnVar FROM $tableVar WHERE col2 = $nameExprVar;
INSERT INTO $tableName values ('$myString', $numValue);
UPDATE $dbName.$tableName SET col1 = $myValue;
DELETE FROM $tableName;

.LOGOFF;
```

Copy

##### Snowflake SQL[¶](#id2 "Link to this heading")

```
 EXECUTE IMMEDIATE
$$
  --** SSC-FDM-TD0003 - BASH VARIABLES FOUND, USING SNOWSQL WITH VARIABLE SUBSTITUTION ENABLED IS REQUIRED TO RUN THIS SCRIPT **
  DECLARE
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0);
  BEGIN
    -- Additional Params: -q SnowScript
    --.LOGON dbc, dbc
    !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'BTLogOn' NODE ***/!!!
    null;
    BEGIN
      USE DATABASE testing;
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLROWCOUNT', SQLROWCOUNT);
    EXCEPTION
      WHEN OTHER THEN
        STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
    END;
    BEGIN
      SELECT
        &columnVar
      FROM
        &tableVar
      WHERE
        col2 = &nameExprVar;
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLROWCOUNT', SQLROWCOUNT);
    EXCEPTION
      WHEN OTHER THEN
        STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
    END;
    BEGIN
      INSERT INTO &tableName
      VALUES ('&myString', &numValue);
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLROWCOUNT', SQLROWCOUNT);
    EXCEPTION
      WHEN OTHER THEN
        STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
    END;
    BEGIN
      UPDATE &dbName.&tableName
        SET
          col1 = &myValue
        ;
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLROWCOUNT', SQLROWCOUNT);
    EXCEPTION
      WHEN OTHER THEN
        STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
    END;
    BEGIN
      DELETE FROM
        &tableName;
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLROWCOUNT', SQLROWCOUNT);
    EXCEPTION
      WHEN OTHER THEN
        STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
    END;
    --.LOGOFF
    !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'LogOff' NODE ***/!!!
    null;
  END
$$
```

Copy

### Known Issues[¶](#known-issues "Link to this heading")

1. **There may be BTEQ commands that do not have an equivalent in Snowflake SQL**

Since BTEQ is a command-based program, there may be some commands in your input code that do not have a hundred percent functional equivalence in Snowflake SQL. Those particular cases are identified, marked with warnings in the output code, and documented in the further pages.

### Related EWIs [¶](#related-ewis "Link to this heading")

1. [SSC-EWI-0073](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0073): Pending Functional Equivalence Review.
2. [SSC-FDM-TD0003](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/teradataFDM.html#ssc-fdm-td0003): Bash variables found, using Snow SQL with variable substitution enabled is required to run this script.
3. [SSC-FDM-TD0013](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/teradataFDM.html#ssc-fdm-td0013): The Snowflake error code mismatch the original Teradata error code.

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

1. [Description](#description)