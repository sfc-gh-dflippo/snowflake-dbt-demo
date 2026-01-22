---
auto_generated: true
description: In PostgreSQL and PostgreSQL-based languages (Greenplum, RedShift, Netezza),
  when comparing fixed-length data types (CHAR, CHARACTER, etc) or comparing fixed-length
  data types against varchar data typ
last_scraped: '2026-01-14T16:53:35.544053+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/postgres/postgresql-string-comparison
title: SnowConvert AI - PostgreSQL - String Comparison | Snowflake Documentation
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
          + [Oracle](../oracle/README.md)
          + [SQL Server-Azure Synapse](../transact/README.md)
          + [Sybase IQ](../sybase/README.md)
          + [Hive-Spark-Databricks SQL](../hive/README.md)
          + [Redshift](../redshift/README.md)
          + [PostgreSQL-Greenplum-Netezza](README.md)

            - [Built-in Functions](postgresql-built-in-functions.md)
            - [Data Types](data-types/postgresql-data-types.md)
            - [String Comparison](postgresql-string-comparison.md)
            - DDLs

              - [CREATE MATERIALIZED VIEW](ddls/create-materialized-view/postgresql-create-materialized-view.md)
              - [CREATE TABLE](ddls/create-table/postgresql-create-table.md)
              - [CREATE VIEW](ddls/postgresql-create-view.md)
            - [Expressions](postgresql-expressions.md)
            - [Interactive Terminal](postgresql-interactive-terminal.md)
            - ETL And BI Repointing

              - [Power BI PostgreSQL Repointing](etl-bi-repointing/power-bi-postgres-repointing.md)
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)Translation References[PostgreSQL-Greenplum-Netezza](README.md)String Comparison

# SnowConvert AI - PostgreSQL - String Comparison[¶](#snowconvert-ai-postgresql-string-comparison "Link to this heading")

In PostgreSQL and PostgreSQL-based languages (Greenplum, RedShift, Netezza), when comparing fixed-length data types (CHAR, CHARACTER, etc) or comparing fixed-length data types against varchar data types, trailing spaces are ignored. This means that a string like `'water '` (value with a trailing space) would be considered equal to `'water'` (value without a trailing space).

If you compare

```
CHAR(6) 'hello', which is stored as 'hello ', with one padded character
```

Copy

against

```
CHAR(6) 'hello ', with no need to add any padding character
```

Copy

They are effectively the same after trailing spaces.

Meanwhile, Snowflake does not have fixed-length character types and takes a more literal approach for its `VARCHAR` data type, treating strings exactly as they are stored, including any trailing blanks. Therefore, in Snowflake, `'water '` is *not* considered equal to `'water'`.

To prevent trailing spaces from affecting string comparison outcomes in PostgreSQL to Snowflake conversions, SnowConvert AI automatically adds `BTRIM` to relevant comparisons as our team has identified. This ensures consistent behavior.

## Sample Source Patterns[¶](#sample-source-patterns "Link to this heading")

Let’s use the following script data to explain string comparison.

```
create table table1(c1 char(2), c2 char(2), c3 VARCHAR(2), c4 VARCHAR(2));

insert into table1 values ('a','a ','a','a ');

insert into table1 values ('b','b','b','b');
```

Copy

### NULLIF[¶](#nullif "Link to this heading")

#### Varchar Data Type[¶](#varchar-data-type "Link to this heading")

Input Code:

##### PostgreSQL[¶](#postgresql "Link to this heading")

```
SELECT NULLIF(c3,c4) FROM table1;
```

Copy

Output Code:

##### Snowflake[¶](#snowflake "Link to this heading")

```
SELECT
NULLIF(c3,c4) FROM
table1;
```

Copy

#### Char Data Types[¶](#char-data-types "Link to this heading")

Input Code:

##### PostgreSQL[¶](#id1 "Link to this heading")

```
select nullif(c1,c2) AS case2 from table1;
```

Copy

Output Code:

##### Snowflake[¶](#id2 "Link to this heading")

```
--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "table1" **
select
nullif(c1,c2) AS case2 from
table1;
```

Copy

### GREATEST or LEAST[¶](#greatest-or-least "Link to this heading")

Input Code:

#### PostgreSQL[¶](#id3 "Link to this heading")

```
select '"' || greatest(c1, c2) || '"' AS greatest, '"' || least(c1, c2) || '"' AS least from table1;
```

Copy

Output Code:

##### Snowflake[¶](#id4 "Link to this heading")

```
--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "table1" **
select '"' || GREATEST_IGNORE_NULLS(c1, c2) || '"' AS greatest, '"' || LEAST_IGNORE_NULLS(c1, c2) || '"' AS least from
table1;
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

1. [Sample Source Patterns](#sample-source-patterns)