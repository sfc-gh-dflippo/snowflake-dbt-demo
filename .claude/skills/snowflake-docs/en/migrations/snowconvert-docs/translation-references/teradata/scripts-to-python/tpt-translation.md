---
auto_generated: true
description: This section illustrates TPT translation from Teradata to Snowflake.
last_scraped: '2026-01-14T16:53:47.315019+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/teradata/scripts-to-python/tpt-translation
title: SnowConvert AI - Teradata - TPT | Snowflake Documentation
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
            - [Scripts To Python](README.md)

              * [BTEQ](bteq-translation.md)
              * [FLOAD](fastload-translation.md)
              * [MLOAD](multiload-translation.md)
              * [TPT](tpt-translation.md)
              * [Script helpers](snowconvert-script-helpers.md)
            - [Scripts to Snowflake SQL](../scripts-to-snowflake-sql-translation-reference/README.md)
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

[Guides](../../../../../guides/README.md)[Migrations](../../../../README.md)Tools[SnowConvert AI](../../../overview.md)Translation References[Teradata](../README.md)[Scripts To Python](README.md)TPT

# SnowConvert AI - Teradata - TPT[¶](#snowconvert-ai-teradata-tpt "Link to this heading")

This section illustrates TPT translation from Teradata to Snowflake.

## TPT statements transformation[¶](#tpt-statements-transformation "Link to this heading")

All TPT statements, like other Teradata scripting languages, are being converted to python code. Here are some examples of transformations already supported.

### Define Job header transformation[¶](#define-job-header-transformation "Link to this heading")

The job statement is translated to a python class with all the statements like operators, schema definitions, and steps inside of it.

Source code

```
 /* Some comments on the job  */
DEFINE JOB LOADJOB
DESCRIPTION 'LOAD AC_SCHEMA TABLE FROM A FILE'
JobBody
```

Copy

Translated code

```
 # Some comments on the job
class LOADJOB:
    # DESCRIPTION 'LOAD AC_SCHEMA TABLE FROM A FILE'
    JobBody
```

Copy

### Define Schema transformation[¶](#define-schema-transformation "Link to this heading")

The schema statement is translated to an attribute in the class created for the job statement.

Source code

```
 DEFINE SCHEMA DCS_SCHEMA
DESCRIPTION 'DCS DATA'
(
PNRHEADER_ID   PERIOD(DATE),
PNRLOCPERIOD   PERIOD(TIMESTAMP(0)),
CRTDATE        CLOB,
REQTYP         JSON(100000),
seqno          INTEGER,
resdata        INTEGER
);
```

Copy

Translated code

```
 class JOBNAME:
    DCS_SCHEMA = """(
    PNRHEADER_ID VARCHAR(24),
    PNRLOCPERIOD VARCHAR(58),
    CRTDATE VARCHAR /*** MSC-WARNING - SSC-FDM-TD0002 - COLUMN CONVERTED FROM CLOB DATA TYPE ***/,
    REQTYP VARIANT,
    seqno INTEGER,
    resdata INTEGER,
    );"""
```

Copy

### Define Operator transformation[¶](#define-operator-transformation "Link to this heading")

The operators are translated to python functions inside the class generated for the job. The examples provided are the operators that SnowConvert AI currently supports

#### DDL Operator[¶](#ddl-operator "Link to this heading")

Source code for DDL operator

```
 DEFINE OPERATOR DDL_OPERATOR()
DESCRIPTION 'TERADATA PARALLEL TRANSPORTER DDL OPERATOR'
TYPE DDL
ATTRIBUTES
(
  VARCHAR PrivateLogName ,
  VARCHAR TdpId          = @MyTdpId,
  VARCHAR UserName       = @MyUserName,
  VARCHAR UserPassword   = 'SomePassWord',
  VARCHAR AccountID,
  VARCHAR ErrorList      = ['3807','2580']
);
```

Copy

Translated code

```
 class JobName:
    def DDL_OPERATOR(self):
        #'TERADATA PARALLEL TRANSPORTER DDL OPERATOR'
        global args
        self.con = log_on(user = args.MyUserName, password = 'SomePassWord')
```

Copy

#### UPDATE Operator[¶](#update-operator "Link to this heading")

Source code for UPDATE operator

```
 DEFINE OPERATOR LOAD_OPERATOR()
DESCRIPTION 'TERADATA PARALLEL TRANSPORTER LOAD OPERATOR'
TYPE UPDATE
SCHEMA AC_MASTER_SCHEMA
ATTRIBUTES
(
    VARCHAR PrivateLogName ,
    INTEGER MaxSessions       =  32,
    INTEGER MinSessions       =  1,
    VARCHAR TargetTable       = '&TARGET_TABLE',
    VARCHAR TdpId             = @MyTdpId,
    VARCHAR UserName          = @MyUserName,
    VARCHAR UserPassword      = @MyPassword,
    VARCHAR AccountId,
    VARCHAR ErrorTable1       = '&LOG_DB_NAME.ERR1',
    VARCHAR ErrorTable2       = '&LOG_DB_NAME.ERR2',
    VARCHAR LogTable          = '&LOG_DB_NAME.LOG_TABLE'
);
```

Copy

Translated code

```
 class JobName:
    def LOAD_OPERATOR(self, query):
        #'TERADATA PARALLEL TRANSPORTER LOAD OPERATOR'
        #USES SCHEMA AC_MASTER_SCHEMA
        operator_name = "LOAD_OPERATOR"
        return query
```

Copy

#### DATA CONNECTOR PRODUCER Operator[¶](#data-connector-producer-operator "Link to this heading")

Source code for Data Connector Producer operator

```
 DEFINE OPERATOR FILE_READER()
DESCRIPTION 'TERADATA PARALLEL TRANSPORTER DATA CONNECTOR OPERATOR'
TYPE DATACONNECTOR PRODUCER
SCHEMA AC_MASTER_SCHEMA
ATTRIBUTES
(
  VARCHAR PrivateLogName ,
  VARCHAR DirectoryPath   = '&INPUTFILEPATH' ,
  VARCHAR FileName        = '&INPUTTEXTFILE' ,
  VARCHAR Format          = 'delimited',
  VARCHAR OpenMode        = 'Read',
  VARCHAR TextDelimiter     = '~',
  VARCHAR IndicatorMode   = 'N'
);
```

Copy

Translated code

```
 class JobName:
    def FILE_READER(self):
        #'TERADATA PARALLEL TRANSPORTER DATA CONNECTOR OPERATOR'
        #USES SCHEMA AC_MASTER_SCHEMA
        operator_name = "FILE_READER"
        stage_name = f"{self.jobname}_{operator_name}"
        format_name = f"{self.jobname}_{operator_name}_FILEFORMAT"
        exec(f"""CREATE OR REPLACE FILE FORMAT {format_name} TYPE = 'CSV' FIELD_DELIMITER = '~' TRIM_SPACE = TRUE SKIP_HEADER = 0""")
        exec(f"""CREATE STAGE IF NOT EXISTS {self.jobname}_STAGE""")
        exec(f"""PUT file://{INPUTFILEPATH}/{INPUTTEXTFILE} @{stage_name} OVERWRITE = TRUE AUTO_COMPRESS = FALSE;""")
        temp_table_name = f"{self.jobname}_{operator_name}_TEMP"
        exec(f"""DROP TABLE IF EXISTS {temp_table_name}""")
        exec(f"""CREATE TEMPORARY TABLE {temp_table_name} {self.AC_MASTER_SCHEMA}""")
        exec(f"""COPY INTO {temp_table_name} FROM @{stage_name} FILE_FORMAT = (format_name = '{format_name}')""")
        return temp_table_name
```

Copy

### Define step transformation[¶](#define-step-transformation "Link to this heading")

Steps are too translated to python functions inside the class generated for the job, they will be called in the main function of the translated code.

Step source code

```
 STEP setup_tables
(
  APPLY
  ('DELETE FROM  &STAGE_DB_NAME.EMS_AC_MASTER_STG;')
   TO OPERATOR (DDL_OPERATOR() );
);

STEP stLOAD_FILE_NAME
(
  APPLY
  ('INSERT INTO CRASHDUMPS.EMP_NAME
  (EMP_NAME, EMP_YEARS, EMP_TEAM)
  VALUES
  (:EMP_NAME, :EMP_YEARS, :EMP_TEAM);')
  TO OPERATOR (ol_EMP_NAME() [1])
  SELECT * FROM OPERATOR(op_EMP_NAME);
);
```

Copy

Translated code

```
 def setup_tables(self):
    self.DDL_OPERATOR()
    exec(f"""DELETE FROM DATABASE1.{STAGE_DB_NAME}.EMS_AC_MASTER_STG""")

def stLOAD_FILE_NAME(self):
    exec(f"""INSERT INTO DATABASE1.CRASHDUMPS.EMP_NAME (EMP_NAME, EMP_YEARS, EMP_TEAM)
SELECT EMP_NAME, EMP_YEARS, EMP_TEAM
FROM (
{self.ol_EMP_NAME('SELECT * FROM ' + self.op_EMP_NAME() )})""")
```

Copy

### Main function[¶](#main-function "Link to this heading")

The main function is always generated for any scripting language, for TPT the main function contains an instance of the job class and calls to the steps in the job

Main function sample code

```
 def main():
  _LOADJOB = LOADJOB()
  _LOADJOB.setup_tables()
  _LOADJOB.stLOAD_FILE_NAME()
  snowconvert.helpers.quit_application()
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

1. [TPT statements transformation](#tpt-statements-transformation)