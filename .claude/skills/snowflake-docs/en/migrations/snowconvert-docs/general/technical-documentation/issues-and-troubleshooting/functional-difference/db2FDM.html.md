---
auto_generated: true
description: FUNCTIONALITY MIGHT BE DIFFERENT DEPENDING ON THE DB2 DATABASE.
last_scraped: '2026-01-14T16:56:20.088193+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/db2FDM.html
title: SnowConvert AI - IBM DB2 Functional Differences | Snowflake Documentation
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

            + [SnowConvert AI](../../../user-guide/snowconvert/README.md)
            + [Project Creation](../../../user-guide/project-creation.md)
            + [Extraction](../../../user-guide/extraction.md)
            + [Deployment](../../../user-guide/deployment.md)
            + [Data Migration](../../../user-guide/data-migration.md)
            + [Data Validation](../../../user-guide/data-validation.md)
            + [Power BI Repointing](../../../user-guide/power-bi-repointing-general.md)
            + [ETL Migration](../../../user-guide/etl-migration-replatform.md)
          + [Technical Documentation](../../README.md)

            - [Considerations](../../considerations/README.md)
            - [Issues And Troubleshooting](../README.md)

              * [Conversion Issues](../conversion-issues/README.md)
              * [Functional Difference](README.md)

                + [General](generalFDM.md)
                + [BigQuery](bigqueryFDM.md)
                + [DB2](db2FDM.md)
                + [Greenplum](greenplumFDM.md)
                + [Hive](hiveFDM.md)
                + [Oracle](oracleFDM.md)
                + [PostgreSQL](postgresqlFDM.md)
                + [Redshift](redshiftFDM.md)
                + [SQL Server-Azure Synapse](sqlServerFDM.md)
                + [Sybase IQ](sybaseFDM.md)
                + [Teradata](teradataFDM.md)
                + [Vertica](verticaFDM.md)
                + [SSIS](ssisFDM.md)
              * [Out Of Scope](../out-of-scope/README.md)
              * [Performance Review](../performance-review/README.md)
            - Function References

              - [SnowConvert AI Udfs](../../function-references/snowconvert-udfs.md)
              - [Teradata](../../function-references/teradata/README.md)
              - [Oracle](../../function-references/oracle/README.md)
              - [Shared](../../function-references/shared/README.md)
              - [SQL Server](../../function-references/sql-server/README.md)
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

[Guides](../../../../../../guides/README.md)[Migrations](../../../../../README.md)Tools[SnowConvert AI](../../../../overview.md)General[Technical Documentation](../../README.md)[Issues And Troubleshooting](../README.md)[Functional Difference](README.md)DB2

# SnowConvert AI - IBM DB2 Functional Differences[¶](#snowconvert-ai-ibm-db2-functional-differences "Link to this heading")

## SSC-FDM-DB0001[¶](#ssc-fdm-db0001 "Link to this heading")

FUNCTIONALITY MIGHT BE DIFFERENT DEPENDING ON THE DB2 DATABASE.

### Severity[¶](#severity "Link to this heading")

Low

### Description[¶](#description "Link to this heading")

This message is shown whenever a SQL element behaves differently depending on the DB2 database version ([DB2 for i](https://www.ibm.com/docs/en/i/7.4?topic=database), [DB2 for z/OS](https://www.ibm.com/docs/en/db2-for-zos/12?topic=db2-sql), or [DB2 for Linux, Unix, and Windows](https://www.ibm.com/docs/en/db2/11.5?topic=database-fundamentals)). SnowConvert AI treats all DB2 versions as one and therefore, the translation for the element might have functionality differences when compared to the original platform.

### Cases[¶](#cases "Link to this heading")

Listed below are all the SQL elements so far identified, that behave differently depending on the DB2 database version.

#### CURRENT MEMBER[¶](#current-member "Link to this heading")

DB2 for z/OS: [CURRENT MEMBER](https://www.ibm.com/docs/en/db2-for-zos/11?topic=registers-current-member) specifies the member name of a current Db2 data sharing member on which a statement is executing. The value of CURRENT MEMBER is a character string.

Db2 for LUW: The [CURRENT MEMBER](https://www.ibm.com/docs/en/db2/11.5?topic=registers-current-member) special register specifies an INTEGER value that identifies the coordinator member for the statement.

##### Code example[¶](#code-example "Link to this heading")

##### Input code:[¶](#input-code "Link to this heading")

```
 CREATE TABLE T1
(
  COL1 INT,
  COL2 CHAR(8) WITH DEFAULT CURRENT MEMBER
);
```

Copy

##### Output code:[¶](#output-code "Link to this heading")

```
 CREATE TABLE T1
 (
  COL1 INT,
  COL2 CHAR(8) DEFAULT
  --** SSC-FDM-DB0001 - FUNCTIONALITY FOR CURRENT_ROLE MIGHT BE DIFFERENT DEPENDING ON THE DB2 DATABASE. **
  CURRENT_ROLE()
)
 COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/02/2025",  "domain": "no-domain-provided" }}';
```

Copy

### Recommendations[¶](#recommendations "Link to this heading")

* Review your code and keep in mind that the result transformation can behave differently according to the Db2 version that is being used.
* If you need more support, you can email us at [snowconvert-support@snowflake.com](mailto:snowconvert-support%40snowflake.com)

## SSC-FDM-DB0002[¶](#ssc-fdm-db0002 "Link to this heading")

DECFLOAT TYPE CHANGED TO NUMBER BECAUSE IT IS ONLY SUPPORTED IN TABLE COLUMNS AND CAST EXPRESSIONS IN SNOWFLAKE.

### Severity[¶](#id1 "Link to this heading")

Low

### Description[¶](#id2 "Link to this heading")

This message is shown when a `DECFLOAT` data type is used in a context not supported by Snowflake. In Snowflake, `DECFLOAT` is only permitted in:

* Table column definitions (`CREATE TABLE`)
* `CAST` expressions (`CAST(value AS DECFLOAT)`)

When `DECFLOAT` is used in other contexts such as procedure parameters, function parameters, or local variable declarations, SnowConvert AI transforms it to `NUMBER(38, 37)` and adds this FDM to indicate the functional difference.

### Code Example[¶](#id3 "Link to this heading")

#### DB2[¶](#db2 "Link to this heading")

```
CREATE PROCEDURE TestProc (param1 DECFLOAT)
BEGIN
  DECLARE local_var DECFLOAT;
  SET local_var = param1;
END;
```

Copy

#### Snowflake[¶](#snowflake "Link to this heading")

```
CREATE OR REPLACE PROCEDURE TestProc (param1 NUMBER(38, 37) --** SSC-FDM-DB0002 - DECFLOAT TYPE CHANGED TO NUMBER BECAUSE IT IS ONLY SUPPORTED IN TABLE COLUMNS AND CAST EXPRESSIONS IN SNOWFLAKE. **
)
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
BEGIN
  LET local_var NUMBER(38, 37) --** SSC-FDM-DB0002 - DECFLOAT TYPE CHANGED TO NUMBER BECAUSE IT IS ONLY SUPPORTED IN TABLE COLUMNS AND CAST EXPRESSIONS IN SNOWFLAKE. **
  := NULL;
  local_var := param1;
END;
$$;
```

Copy

### Recommendations[¶](#id4 "Link to this heading")

* Review the converted code to ensure that using `NUMBER(38, 37)` instead of `DECFLOAT` does not affect your application logic.
* If precise decimal floating-point arithmetic is critical for these parameters or variables, consider refactoring your code to use table columns or `CAST` expressions where `DECFLOAT` is supported.
* If you need more support, you can email us at [snowconvert-support@snowflake.com](mailto:snowconvert-support%40snowflake.com)

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

1. [SSC-FDM-DB0001](#ssc-fdm-db0001)
2. [SSC-FDM-DB0002](#ssc-fdm-db0002)