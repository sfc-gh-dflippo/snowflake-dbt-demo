---
auto_generated: true
description: The following CLI arguments are specific for executing migrations with
  SnowConvert AI for Teradata
last_scraped: '2026-01-14T16:52:57.654245+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/general/user-guide/snowconvert/command-line-interface/teradata
title: SnowConvert AI - Teradata | Snowflake Documentation
---

1. [Overview](../../../../../../guides/README.md)
2. [Snowflake Horizon Catalog](../../../../../../user-guide/snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../../../../../../guides/overview-connecting.md)
6. [Virtual warehouses](../../../../../../user-guide/warehouses.md)
7. [Databases, Tables, & Views](../../../../../../guides/overview-db.md)
8. [Data types](../../../../../../data-types.md)
10. Data Integration

    - [Snowflake Openflow](../../../../../../user-guide/data-integration/openflow/about.md)
    - Apache Iceberg™

      - [Apache Iceberg™ Tables](../../../../../../user-guide/tables-iceberg.md)
      - [Snowflake Open Catalog](../../../../../../user-guide/opencatalog/overview.md)
11. Data engineering

    - [Data loading](../../../../../../guides/overview-loading-data.md)
    - [Dynamic Tables](../../../../../../user-guide/dynamic-tables-about.md)
    - [Streams and Tasks](../../../../../../user-guide/data-pipelines-intro.md)
    - [dbt Projects on Snowflake](../../../../../../user-guide/data-engineering/dbt-projects-on-snowflake.md)
    - [Data Unloading](../../../../../../guides/overview-unloading-data.md)
12. [Storage Lifecycle Policies](../../../../../../user-guide/storage-management/storage-lifecycle-policies.md)
13. [Migrations](../../../../../README.md)

    * Tools

      * [SnowConvert AI](../../../../overview.md)

        + General

          + [About](../../../about.md)
          + [Getting Started](../../../getting-started/README.md)
          + [Terms And Conditions](../../../terms-and-conditions/README.md)
          + [Release Notes](../../../release-notes/release-notes/README.md)
          + User Guide

            + [SnowConvert AI](../README.md)

              - [How To Install The Tool](../how-to-install-the-tool/README.md)
              - [How To Request An Access Code](../how-to-request-an-access-code/README.md)
              - [Command Line Interface](README.md)

                * [Renaming Feature](renaming-feature.md)
                * [Oracle](oracle.md)
                * [Teradata](teradata.md)
                * [SQL Server](sql-server.md)
                * [Redshift](redshift.md)
              - [What Is A SnowConvert AI Project](../what-is-a-snowconvert-project.md)
              - [How To Update The Tool](../how-to-update-the-tool.md)
              - [How To Use The SnowConvert AI Cli](../how-to-use-the-snowconvert-cli.md)
            + [Project Creation](../../project-creation.md)
            + [Extraction](../../extraction.md)
            + [Deployment](../../deployment.md)
            + [Data Migration](../../data-migration.md)
            + [Data Validation](../../data-validation.md)
            + [Power BI Repointing](../../power-bi-repointing-general.md)
            + [ETL Migration](../../etl-migration-replatform.md)
          + [Technical Documentation](../../../technical-documentation/README.md)
          + [Contact Us](../../../contact-us.md)
          + Others

            + [Using SnowConvert AI In A Ubuntu Docker Image](../../../others/using-snowconvert-in-a-ubuntu-docker-image.md)
          + [Frequently Asked Questions (FAQ)](../../../frequently-asked-questions-faq.md)")
        + Translation References

          + [General](../../../../translation-references/general/README.md)
          + [Teradata](../../../../translation-references/teradata/README.md)
          + [Oracle](../../../../translation-references/oracle/README.md)
          + [SQL Server-Azure Synapse](../../../../translation-references/transact/README.md)
          + [Sybase IQ](../../../../translation-references/sybase/README.md)
          + [Hive-Spark-Databricks SQL](../../../../translation-references/hive/README.md)
          + [Redshift](../../../../translation-references/redshift/README.md)
          + [PostgreSQL-Greenplum-Netezza](../../../../translation-references/postgres/README.md)
          + [BigQuery](../../../../translation-references/bigquery/README.md)
          + [Vertica](../../../../translation-references/vertica/README.md)
          + [IBM DB2](../../../../translation-references/db2/README.md)
          + [SSIS](../../../../translation-references/ssis/README.md)
        + [Migration Assistant](../../../../migration-assistant/README.md)
        + [Data Validation CLI](../../../../data-validation-cli/index.md)
        + [AI Verification](../../../../snowconvert-ai-verification.md)
      * [Snowpark Migration Accelerator](../../../../../sma-docs/README.md)
    * Guides

      * [Teradata](../../../../../guides/teradata.md)
      * [Databricks](../../../../../guides/databricks.md)
      * [SQL Server](../../../../../guides/sqlserver.md)
      * [Amazon Redshift](../../../../../guides/redshift.md)
      * [Oracle](../../../../../guides/oracle.md)
      * [Azure Synapse](../../../../../guides/azuresynapse.md)
15. [Queries](../../../../../../guides/overview-queries.md)
16. [Listings](../../../../../../collaboration/collaboration-listings-about.md)
17. [Collaboration](../../../../../../guides/overview-sharing.md)
19. [Snowflake AI & ML](../../../../../../guides/overview-ai-features.md)
21. [Snowflake Postgres](../../../../../../user-guide/snowflake-postgres/about.md)
23. [Alerts & Notifications](../../../../../../guides/overview-alerts.md)
25. [Security](../../../../../../guides/overview-secure.md)
26. [Data Governance](../../../../../../guides/overview-govern.md)
27. [Privacy](../../../../../../guides/overview-privacy.md)
29. [Organizations & Accounts](../../../../../../guides/overview-manage.md)
30. [Business continuity & data recovery](../../../../../../user-guide/replication-intro.md)
32. [Performance optimization](../../../../../../guides/overview-performance.md)
33. [Cost & Billing](../../../../../../guides/overview-cost.md)

[Guides](../../../../../../guides/README.md)[Migrations](../../../../../README.md)Tools[SnowConvert AI](../../../../overview.md)GeneralUser Guide[SnowConvert AI](../README.md)[Command Line Interface](README.md)Teradata

# SnowConvert AI - Teradata[¶](#snowconvert-ai-teradata "Link to this heading")

## Specific CLI arguments[¶](#specific-cli-arguments "Link to this heading")

The following CLI arguments are specific for executing migrations with **SnowConvert AI for Teradata**

### `--displaceDatabaseAsSchema`[¶](#displacedatabaseasschema "Link to this heading")

This flag must be used with the `-s` parameter. When used it will maintain Teradata’s database name qualification as Snowflake’s data warehouse, contrary to it’s default behavior where it becomes a schema on Snowflake code. Let’s look and example where `-s customSchema` is included:

```
SELECT * FROM databaseName.tableName;
```

Copy

```
-- Additional Params: -s customSchema
SELECT
* FROM
customSchema.tableName;
```

Copy

```
-- Additional Params: -s customSchema --displaceDatabaseAsSchema
SELECT
* FROM
databaseName.customSchema.tableName;
```

Copy

#### `--CharacterToApproximateNumber <NUMBER>`[¶](#charactertoapproximatenumber-number "Link to this heading")

An integer value for the CHARACTER to Approximate Number transformation (Default: `10`).

#### `--DefaultDateFormat <STRING>`[¶](#defaultdateformat-string "Link to this heading")

String value for the Default DATE format (Default: `"YYYY/MM/DD"`).

#### `--DefaultTimeFormat <STRING>`[¶](#defaulttimeformat-string "Link to this heading")

String value for the Default TIME format (Default: `"HH:MI:SS.FF6"`).

#### `--DefaultTimestampFormat <STRING>`[¶](#defaulttimestampformat-string "Link to this heading")

String value for the Default TIMESTAMP format (Default: `"YYYY/MM/DD HH:MI:SS.FF6"`).

#### `--DefaultTimezoneFormat <STRING>`[¶](#defaulttimezoneformat-string "Link to this heading")

String value for the Default TIMEZONE format (Default: `"GMT-5"`).

#### `-p, --scriptTargetLanguage <TARGET_LANGUAGE>`[¶](#p-scripttargetlanguage-target-language "Link to this heading")

The string value specifies the target language to convert Bteq and Mload script files. Currently supported values are **SnowScript** and **Python**. The default value is set to **Python**.

#### `-n, --SessionMode <SESSION_MODE>`[¶](#n-sessionmode-session-mode "Link to this heading")

SnowConvert AI handles Teradata code in both TERA and ANSI modes. Currently, this is limited to the default case specification of character data and how it affects comparisons.

The string value specifies the Session Mode of the input code. Currently supported values are **TERA** and **ANSI**. The default value is set to **TERA**.

You can learn more about how SnowConvert AI handles and converts code depending on the session mode, check here.

#### `--replaceDeleteAllToTruncate`[¶](#replacedeletealltotruncate "Link to this heading")

Flag to indicate whether Delete All statements must be replaced with Truncate or not. This will generate SSC-EWI-TD0037 when the replacement is done. Example:

```
create table testTable(
    column1 varchar(30)
);

delete testTable all;

delete from testTable;
```

Copy

```
CREATE OR REPLACE TABLE testTable (
    column1 varchar(30)
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;

DELETE FROM testTable;

DELETE FROM 
    testTable;
```

Copy

```
-- Additional Params: --replaceDeleteAllToTruncate
CREATE OR REPLACE TABLE testTable (
    column1 varchar(30)
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;

TRUNCATE TABLE testTable;

DELETE FROM 
    testTable;
```

Copy

#### `--generateStoredProcedureTags`[¶](#generatestoredproceduretags "Link to this heading")

Flag to indicate whether the SQL statements SELECT, INSERT, CREATE, DELETE, UPDATE, DROP, MERGE in Stored Procedures will be tagged on the converted code. This feature is used for easy statement identification on the migrated code. Wrapping these statements within these XML-like tags allows for other programs to quickly find and extract them. The decorated code looks like this:

```
//<SQL_DELETE
EXEC(DELETE FROM SB_EDP_SANDBOX_LAB.PUBLIC.USER_LIST,[])
//SQL_DELETE!>
```

Copy

#### `--splitPeriodDatatype`[¶](#splitperioddatatype "Link to this heading")

This flag is used to indicate that the tool should migrate any use of the `PERIOD` datatype as two separate `DATETIME` fields that will hold the original period begin and end values, anytime a period field or function is migrated using this flag SSC-FDM-TD0004 will be added to warn about this change.

```
CREATE TABLE myTable(
   col1 PERIOD(DATE),
   col2 VARCHAR(50),
   col3 PERIOD(TIMESTAMP)
);
```

Copy

```
CREATE OR REPLACE TABLE myTable (
   col1 VARCHAR(24) !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!,
   col2 VARCHAR(50),
   col3 VARCHAR(58) !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;
```

Copy

```
-- Additional Params: --splitPeriodDatatype
CREATE OR REPLACE TABLE myTable (
   col1_begin DATE,
   col1_end DATE /*** SSC-FDM-TD0004 - PERIOD DATA TYPES ARE HANDLED AS TWO DATA FIELDS ***/,
   col2 VARCHAR(50),
   col3_begin TIMESTAMP,
   col3_end TIMESTAMP /*** SSC-FDM-TD0004 - PERIOD DATA TYPES ARE HANDLED AS TWO DATA FIELDS ***/
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;
```

Copy

#### `--arrange`[¶](#arrange "Link to this heading")

Flag to indicate whether the input code should be processed before parsing and transformation.

#### `--RenamingFile`[¶](#renamingfile "Link to this heading")

The path to a .json file that specifies new names for certain objects such as Tables, Views, Procedures, Functions, and Macros. This parameter can’t be used with the `customSchema` argument. Navigate to the [Renaming Feature](renaming-feature) to learn more about this argument.

#### `--UseCollateForCaseSpecification`[¶](#usecollateforcasespecification "Link to this heading")

This flag indicates whether to use COLLATE or UPPER to preserve Case Specification functionality, e.g. CASESPECIFIC or NOT CASESPECIFIC. By default, it is turned off, meaning that the UPPER function will be used to emulate case insensitivity (NOT CASESPECIFIC). To learn more about how Case Specification is handled by SnowConvert AI check here.

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

1. [Specific CLI arguments](#specific-cli-arguments)