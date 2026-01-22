---
auto_generated: true
description: Translation references to convert Teradata script statements that are
  in common among all scripts syntaxes to Snowflake SQL
last_scraped: '2026-01-14T16:53:48.360976+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/teradata/scripts-to-snowflake-sql-translation-reference/common-statements
title: SnowConvert AI - Teradata - COMMON STATEMENTS | Snowflake Documentation
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

[Guides](../../../../../guides/README.md)[Migrations](../../../../README.md)Tools[SnowConvert AI](../../../overview.md)Translation References[Teradata](../README.md)[Scripts to Snowflake SQL](README.md)Common statements

# SnowConvert AI - Teradata - COMMON STATEMENTS[¶](#snowconvert-ai-teradata-common-statements "Link to this heading")

Translation references to convert Teradata script statements that are in common among all scripts syntaxes to Snowflake SQL

## ERROR HANDLING[¶](#error-handling "Link to this heading")

> The BTEQ error handling capabilities are based on the Teradata Database error codes. These are the standard error codes and messages produced in response to user-specified Teradata SQL statements. A BTEQ user cannot change, modify or delete these messages.

For more information regarding BTEQ Error Handling, check [here](https://docs.teradata.com/r/Basic-Teradata-Query-Reference/October-2018/Using-BTEQ/Error-Handling).

### Sample Source Patterns[¶](#sample-source-patterns "Link to this heading")

#### Basic BTEQ Error Handling Example[¶](#basic-bteq-error-handling-example "Link to this heading")

The error conditions content is relocated in different statements in case ERRORCODE is different to zero, otherwise it can be located as the original code. First, the query above the if statement is relocated within a BEGIN - END block, where in case of an exception it will be caught in the EXCEPTION block. Second of all, the ERRORCODE variable will be changed to the variable declared indicating their SQLCODE with an EWI indicating that the exact number of the SQLCODE is not the same as the ERRORCODE in BTEQ.

##### Teradata BTEQ[¶](#teradata-bteq "Link to this heading")

```
-- Additional Params: -q SnowScript
SELECT * FROM table1;
 
.IF ERRORCODE<>0 THEN .EXIT 1

.QUIT 0
```

Copy

##### Snowflake SQL[¶](#snowflake-sql "Link to this heading")

```
EXECUTE IMMEDIATE
$$
  DECLARE
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0);
  BEGIN
    BEGIN
      -- Additional Params: -q SnowScript
      SELECT
        *
      FROM
        table1;
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLROWCOUNT', SQLROWCOUNT);
    EXCEPTION
      WHEN OTHER THEN
        STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
    END;
    IF (STATUS_OBJECT['SQLCODE'] /*** SSC-FDM-TD0013 - THE SNOWFLAKE ERROR CODE MISMATCH THE ORIGINAL TERADATA ERROR CODE ***/ != 0) THEN
      RETURN 1;
    END IF;
    RETURN 0;
  END
$$
```

Copy

### Known Issues[¶](#known-issues "Link to this heading")

No issues were found.

### Related EWIs[¶](#related-ewis "Link to this heading")

1. [SSC-FDM-TD0013](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/teradataFDM.html#ssc-fdm-td0013): The Snowflake error code mismatch the original Teradata error code.

## EXIT or QUIT[¶](#exit-or-quit "Link to this heading")

Logs off all database sessions and then exits BTEQ.

The highest severity value encountered during BTEQ’s execution will by default be used as BTEQ’s return code value unless an argument is explicitly supplied. ([Teradata Basic Query Reference EXIT or QUIT Command](https://docs.teradata.com/r/Basic-Teradata-Query-Reference/October-2018/BTEQ-Commands/BTEQ-Command-Descriptions/ERROROUT))

```
.<ExitCommand> [<Result>];
<ExitCommand> := EXIT | QUIT
<Result> := <Status_variable> | Number 
<Status_variable> := ACTIVITY_COUNT | ERRORCODE | ERRORLEVEL
```

Copy

### Sample Source Patterns[¶](#id1 "Link to this heading")

#### Basic IF example[¶](#basic-if-example "Link to this heading")

##### Teradata BTEQ[¶](#id2 "Link to this heading")

```
-- Additional Params: -q SnowScript
.QUIT ERRORCODE;
```

Copy

##### Snowflake SQL[¶](#id3 "Link to this heading")

```
EXECUTE IMMEDIATE
$$
  DECLARE
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0);
  BEGIN
    RETURN STATUS_OBJECT['SQLCODE'] /*** SSC-FDM-TD0013 - THE SNOWFLAKE ERROR CODE MISMATCH THE ORIGINAL TERADATA ERROR CODE ***/;
  END
$$
```

Copy

### Known Issues[¶](#id4 "Link to this heading")

When the EXIT or QUIT command doesn’t have an input, it returns the ERRORLEVEL as default. However, SnowConvert AI transforms it to return 0.

### Related EWIS[¶](#id5 "Link to this heading")

1. [SSC-FDM-TD0013](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/teradataFDM.html#ssc-fdm-td0013): The Snowflake error code mismatch the original Teradata error code.

## GOTO[¶](#goto "Link to this heading")

### Description[¶](#description "Link to this heading")

> The BTEQ Goto command skips over all intervening BTEQ commands and SQL statements until a specified label is encountered, then resumes processing as usual. ([Teradata Basic Query Reference Goto Command](https://docs.teradata.com/r/1fdhoBglKXYl~W_OyMEtGQ/KzhGjSojGrSjKxfWnYYrMw))

```
.GOTO LabelName;
```

Copy

### Sample Source Patterns[¶](#id6 "Link to this heading")

#### Basic GOTO example[¶](#basic-goto-example "Link to this heading")

Snowflake scripting doesn’t have an equivalent statement for Teradata BTEQ Goto command, but fortunately it can be removed from the input code and get an equivalent code, due to the sequence of Goto and Labels commands in reverse topological order always. In other words, the definitions come after their uses. Thus, SnowConvert AI just needs to copy bottom-up all Label section code to its corresponding Goto statements.

##### Teradata BTEQ[¶](#id7 "Link to this heading")

```
-- Additional Params: -q SnowScript
.LOGON 0/dbc,dbc;
   DATABASE tduser;
.LOGON 127.0.0.1/dbc,dbc;

INSERT INTO TABLEB VALUES (1);
.IF activitycount = 0 then .GOTO SECTIONA
.IF activitycount >= 1 then .GOTO SECTIONB

.label SECTIONA
.REMARK 'Zero Hours on Account'
.GOTO SECTIONC

.label SECTIONB
.REMARK 'Total Hours on Account'

.label SECTIONC
.logoff      
.exit
```

Copy

##### Snowflake[¶](#snowflake "Link to this heading")

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
    --.LOGON
    !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'BTLogOn' NODE ***/!!!
    null;
    /*** SSC-EWI-0001 - UNRECOGNIZED TOKEN ON LINE '4' COLUMN '8' OF THE SOURCE CODE STARTING AT '127.0'. EXPECTED 'STATEMENT' GRAMMAR. LAST MATCHING TOKEN WAS 'LOGON' ON LINE '4' COLUMN '2'. FAILED TOKEN WAS '127.0' ON LINE '4' COLUMN '8'. CODE '81'. ***/
    /*--127.0.0.1/dbc,dbc*/
     
    BEGIN
      INSERT INTO TABLEB
      VALUES (1);
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLROWCOUNT', SQLROWCOUNT);
    EXCEPTION
      WHEN OTHER THEN
        STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
    END;
    IF (NOT (STATUS_OBJECT['SQLROWCOUNT'] = 0)) THEN
      --** SSC-FDM-TD0026 - GOTO SECTIONA WAS REMOVED DUE TO IF STATEMENT INVERSION **
       
      IF (STATUS_OBJECT['SQLROWCOUNT'] >= 1) THEN
         
        /*.label SECTIONB*/
         
        --.REMARK 'Total Hours on Account'
        null;
        /*.label SECTIONC*/
         
        --.logoff
        null;
        RETURN 0;
      END IF;
    END IF;
    /*.label SECTIONA*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
     
    --.REMARK 'Zero Hours on Account'
    !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'Remark' NODE ***/!!!
    null;
     
    /*.label SECTIONC*/
     
    --.logoff
    null;
    RETURN 0;
    /*.label SECTIONB*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
     
    --.REMARK 'Total Hours on Account'
    !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'Remark' NODE ***/!!!
    null;
    /*.label SECTIONC*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
     
    --.logoff
    !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'LogOff' NODE ***/!!!
    null;
    RETURN 0;
  END
$$
```

Copy

### Known Issues [¶](#id8 "Link to this heading")

No issues were found.

### Related EWIS[¶](#id9 "Link to this heading")

1. [SSC-EWI-0001](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0001): Unrecognized token on the line of the source code.
2. [SSC-FDM-0027](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0027): Removed next statement, not applicable in SnowFlake.
3. [SSC-EWI-0073](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0073): Pending Functional Equivalence Review
4. [SSC-FDM-TD0026](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/teradataFDM.html#ssc-fdm-td0026): GOTO statement was removed due to if statement inversion.

## IF… THEN…[¶](#if-then "Link to this heading")

### Description[¶](#id10 "Link to this heading")

> The IF statement validates a condition and executes an action when the action is true. ([Teradata SQL Language reference IF…THEN…](https://docs.teradata.com/r/1fdhoBglKXYl~W_OyMEtGQ/92K64CKQxrkuO4Hm7P8IEA))

```
.IF <Condition> THEN <Action>;

<Condition> := <Status_variable> <Operator> Number
<Status_variable> := ACTIVITY_COUNT | ERRORCODE | ERRORLEVEL
<Operator> := ^= | != | ~= | <> | = | < | > | <= | >=
<Action> := BTEQ_command | SQL_request
```

Copy

### Sample Source Patterns[¶](#id11 "Link to this heading")

#### Basic IF example[¶](#id12 "Link to this heading")

##### Teradata BTEQ[¶](#id13 "Link to this heading")

```
-- Additional Params: -q SnowScript
.IF ACTIVITYCOUNT <> 0 THEN .GOTO InsertEmployee;
```

Copy

##### Snowflake SQL[¶](#id14 "Link to this heading")

```
EXECUTE IMMEDIATE
$$
  DECLARE
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0);
  BEGIN
    IF (STATUS_OBJECT['SQLROWCOUNT'] != 0) THEN
       
      RETURN 1;
    END IF;
  END
$$
```

Copy

### Related EWIS[¶](#id15 "Link to this heading")

No related EWIs.

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

1. [ERROR HANDLING](#error-handling)
2. [EXIT or QUIT](#exit-or-quit)
3. [GOTO](#goto)
4. [IF… THEN…](#if-then)