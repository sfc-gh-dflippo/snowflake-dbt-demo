---
auto_generated: true
description: Translation spec for ROWID pseudocolumn
last_scraped: '2026-01-14T16:53:26.300498+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/oracle/pseudocolumns
title: SnowConvert AI - Oracle - Pseudocolumns | Snowflake Documentation
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

          + [About](../../general/about.md)
          + [Getting Started](../../general/getting-started/README.md)
          + [Terms And Conditions](../../general/terms-and-conditions/README.md)
          + [Release Notes](../../general/release-notes/release-notes/README.md)
          + User Guide

            + [SnowConvert AI](../../general/user-guide/snowconvert/README.md)
            + [Project Creation](../../general/user-guide/project-creation.md)
            + [Extraction](../../general/user-guide/extraction.md)
            + [Deployment](../../general/user-guide/deployment.md)
            + [Data Migration](../../general/user-guide/data-migration.md)
            + [Data Validation](../../general/user-guide/data-validation.md)
            + [Power BI Repointing](../../general/user-guide/power-bi-repointing-general.md)
            + [ETL Migration](../../general/user-guide/etl-migration-replatform.md)
          + [Technical Documentation](../../general/technical-documentation/README.md)
          + [Contact Us](../../general/contact-us.md)
          + Others

            + [Using SnowConvert AI In A Ubuntu Docker Image](../../general/others/using-snowconvert-in-a-ubuntu-docker-image.md)
          + [Frequently Asked Questions (FAQ)](../../general/frequently-asked-questions-faq.md)")
        + Translation References

          + [General](../general/README.md)
          + [Teradata](../teradata/README.md)
          + [Oracle](README.md)

            - [Sample Data](sample-data.md)
            - Basic Elements of Oracle SQL

              - [Literals](basic-elements-of-oracle-sql/literals.md)
              - [Data Types](basic-elements-of-oracle-sql/data-types/README.md)
            - [Pseudocolumns](pseudocolumns.md)
            - [Built-in Functions](functions/README.md)
            - [Built-in Packages](built-in-packages.md)
            - [SQL Queries and Subqueries](sql-queries-and-subqueries/selects.md)
            - [SQL Statements](sql-translation-reference/README.md)
            - [PL/SQL to Snowflake Scripting](pl-sql-to-snowflake-scripting/README.md)
            - [PL/SQL to Javascript](pl-sql-to-javascript/README.md)
            - [SQL Plus](sql-plus.md)
            - [Wrapped Objects](wrapped-objects.md)
            - ETL And BI Repointing

              - [Power BI Oracle Repointing](etl-bi-repointing/power-bi-oracle-repointing.md)
          + [SQL Server-Azure Synapse](../transact/README.md)
          + [Sybase IQ](../sybase/README.md)
          + [Hive-Spark-Databricks SQL](../hive/README.md)
          + [Redshift](../redshift/README.md)
          + [PostgreSQL-Greenplum-Netezza](../postgres/README.md)
          + [BigQuery](../bigquery/README.md)
          + [Vertica](../vertica/README.md)
          + [IBM DB2](../db2/README.md)
          + [SSIS](../ssis/README.md)
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)Translation References[Oracle](README.md)Pseudocolumns

# SnowConvert AI - Oracle - Pseudocolumns[¶](#snowconvert-ai-oracle-pseudocolumns "Link to this heading")

## ROWID[¶](#rowid "Link to this heading")

Translation spec for ROWID pseudocolumn

### Description[¶](#description "Link to this heading")

> For each row in the database, the `ROWID` pseudocolumn returns the address of the row. ([Oracle SQL Language Reference Rowid pseudocolumn](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/ROWID-Pseudocolumn.html#GUID-F6E0FBD2-983C-495D-9856-5E113A17FAF1))

Snowflake does not have an equivalent for ROWID. The pseudocolumn is transformed to *NULL* in order to avoid runtime errors.

```
ROWID
```

Copy

### Sample Source Patterns[¶](#sample-source-patterns "Link to this heading")

#### Oracle[¶](#oracle "Link to this heading")

```
CREATE TABLE sample_table
(
    sample_column varchar(10)
);

INSERT INTO sample_table(sample_column) VALUES ('text 1');
INSERT INTO sample_table(sample_column) VALUES ('text 2');

SELECT ROWID FROM sample_table;
SELECT MAX(ROWID) FROM sample_table;
```

Copy

##### Result Query 1[¶](#result-query-1 "Link to this heading")

```
|ROWID             |
|------------------|
|AAASfCAABAAAIcpAAA|
|AAASfCAABAAAIcpAAB|
```

Copy

##### Result Query 2[¶](#result-query-2 "Link to this heading")

```
|MAX(ROWID)        |
|------------------|
|AAASfCAABAAAIcpAAB|
```

Copy

##### Snowflake[¶](#snowflake "Link to this heading")

```
CREATE OR REPLACE TABLE sample_table
    (
        sample_column varchar(10)
    )
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
;

INSERT INTO sample_table(sample_column) VALUES ('text 1');

INSERT INTO sample_table(sample_column) VALUES ('text 2');

SELECT
--** SSC-FDM-OR0030 - ROWID PSEUDOCOLUMN IS NOT SUPPORTED IN SNOWFLAKE, IT WAS CONVERTED TO NULL TO AVOID RUNTIME ERRORS **
'' AS ROWID
FROM
sample_table;

SELECT MAX(
--** SSC-FDM-OR0030 - ROWID PSEUDOCOLUMN IS NOT SUPPORTED IN SNOWFLAKE, IT WAS CONVERTED TO NULL TO AVOID RUNTIME ERRORS **
'' AS ROWID) FROM
sample_table;
```

Copy

##### Result Query 1[¶](#id1 "Link to this heading")

| NULL |
| --- |
|  |
|  |

### Known Issues[¶](#known-issues "Link to this heading")

No issues were found.

### Related EWIs[¶](#related-ewis "Link to this heading")

* [SSC-FDM-OR0030](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM.html#ssc-fdm-or0030): ROWID pseudocolumn is not supported in Snowflake

## ROWNUM[¶](#rownum "Link to this heading")

Translation spec for ROWNUM pseudocolumn

### Description[¶](#id2 "Link to this heading")

> For each row returned by a query, the `ROWNUM` pseudocolumn returns a number indicating the order in which Oracle selects the row from a table or set of joined rows. ([Oracle SQL Language Reference Rownum pseudocolumn](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/ROWNUM-Pseudocolumn.html#GUID-2E40EC12-3FCF-4A4F-B5F2-6BC669021726))

Snowflake does not have an equivalent for ROWNUM. The approach for the transformation is taking advantage of the Snowflake [seq8](https://docs.snowflake.com/en/sql-reference/functions/seq1.html) function to emulate the functionality.

```
ROWNUM
```

Copy

### Sample Source Patterns[¶](#id3 "Link to this heading")

#### Oracle[¶](#id4 "Link to this heading")

```
-- Table with sample data
CREATE TABLE TABLE1(COL1 VARCHAR(20), COL2 NUMBER);
INSERT INTO TABLE1 (COL1, COL2) VALUES('ROWNUM: ', null);
INSERT INTO TABLE1 (COL1, COL2) VALUES('ROWNUM: ', null);

-- Query 1: ROWNUM in a select

@@ -159,10 +171,10 @@ SELECT ROWNUM FROM TABLE1;
-- Query 2: ROWNUM in DML
UPDATE TABLE1 SET COL2 = ROWNUM;
SELECT * FROM TABLE1;
```

Copy

##### Result Query 1[¶](#id5 "Link to this heading")

```
|ROWNUM|
|------|
|1     |
|2     |
```

Copy

##### Result Query 2[¶](#id6 "Link to this heading")

```
|COL1    |COL2|
|--------|----|
|ROWNUM: |1   |
|ROWNUM: |2   |
```

Copy

##### Snowflake[¶](#id7 "Link to this heading")

```
-- Table with sample data
CREATE OR REPLACE TABLE TABLE1 (COL1 VARCHAR(20),
COL2 NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}}'
;

INSERT INTO TABLE1(COL1, COL2) VALUES('ROWNUM: ', null);

INSERT INTO TABLE1(COL1, COL2) VALUES('ROWNUM: ', null);

-- Query 1: ROWNUM in a select
SELECT
seq8() + 1
FROM
TABLE1;

-- Query 2: ROWNUM in DML
UPDATE TABLE1
SET COL2 = seq8() + 1;

SELECT * FROM
TABLE1;
```

Copy

##### Result Query 1[¶](#id8 "Link to this heading")

```
|SEQ8() + 1|
|----------|
|1         |
|2         |
```

Copy

##### Result Query 2[¶](#id9 "Link to this heading")

```
|COL1    |COL2|
|--------|----|
|ROWNUM: |1   |
|ROWNUM: |2   |
```

Copy

### Known Issues[¶](#id10 "Link to this heading")

No issues were found.

### Related EWIs[¶](#id11 "Link to this heading")

1. [SSC-FDM-0006:](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0006) Number type column may not behave similarly in Snowflake

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

1. [ROWID](#rowid)
2. [ROWNUM](#rownum)