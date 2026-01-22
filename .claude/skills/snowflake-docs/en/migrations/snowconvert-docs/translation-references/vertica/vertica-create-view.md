---
auto_generated: true
description: Creates a new view. (Vertica SQL Language Reference Create view statement)
last_scraped: '2026-01-14T16:54:11.344058+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/vertica/vertica-create-view
title: SnowConvert AI - Vertica - CREATE VIEW | Snowflake Documentation
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
          + [PostgreSQL-Greenplum-Netezza](../postgres/README.md)
          + [BigQuery](../bigquery/README.md)
          + [Vertica](README.md)

            - [CREATE TABLE](vertica-create-table.md)
            - [CREATE VIEW](vertica-create-view.md)
            - [Built-in Functions](vertica-built-in-functions.md)
            - [Data Types](vertica-data-types.md)
            - [Operators](vertica-operators.md)
            - [Predicates](vertica-predicates.md)
            - [Identifier differences between Vertica and Snowflake](vertica-identifier-between-vertica-and-snowflake.md)
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)Translation References[Vertica](README.md)CREATE VIEW

# SnowConvert AI - Vertica - CREATE VIEW[¶](#snowconvert-ai-vertica-create-view "Link to this heading")

## Description[¶](#description "Link to this heading")

Creates a new view. ([Vertica SQL Language Reference Create view statement](https://docs.vertica.com/25.2.x/en/sql-reference/statements/create-statements/create-view/))

## Grammar Syntax[¶](#grammar-syntax "Link to this heading")

```
CREATE [ OR REPLACE ] VIEW [[database.]schema.]view [ (column[,...]) ]
  [ {INCLUDE|EXCLUDE} [SCHEMA] PRIVILEGES ] AS query
```

Copy

## Sample Source Patterns[¶](#sample-source-patterns "Link to this heading")

Success

This syntax is fully supported in [Snowflake](https://docs.snowflake.com/en/sql-reference/sql/create-view).

### Vertica[¶](#vertica "Link to this heading")

```
CREATE OR REPLACE VIEW mySchema.myuser(
userlastname
)
AS 
SELECT lastname FROM users;
```

Copy

#### Snowflake[¶](#snowflake "Link to this heading")

```
CREATE OR REPLACE VIEW mySchema.myuser
(
userlastname
)
AS
SELECT lastname FROM
    users;
```

Copy

### Inherited Schema Privileges Clause[¶](#inherited-schema-privileges-clause "Link to this heading")

`INCLUDE SCHEMA PRIVILEGES` is a Vertica-specific feature that governs how privileges are inherited, in this case, potentially from the schema level. Snowflake does not have a direct equivalent for this clause within its `CREATE VIEW` syntax. Privileges in Snowflake are managed explicitly through `GRANT` statements.

Warning

This syntax is not supported in Snowflake.

#### BigQuery[¶](#bigquery "Link to this heading")

```
CREATE OR REPLACE VIEW mySchema.myuser(
userlastname
)
INCLUDE SCHEMA PRIVILEGES
AS 
SELECT lastname FROM users;
```

Copy

#### Snowflake[¶](#id1 "Link to this heading")

```
CREATE OR REPLACE VIEW mySchema.myuser
(
userlastname
)
!!!RESOLVE EWI!!! /*** SSC-EWI-VT0001 - INHERITED PRIVILEGES CLAUSE IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
INCLUDE SCHEMA PRIVILEGES
AS
SELECT lastname FROM
    users;
```

Copy

### Known Issues[¶](#known-issues "Link to this heading")

There are no known Issues.

### Related EWIs[¶](#related-ewis "Link to this heading")

1. [SSC-EWI-VT0001](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/verticaEWI.html#ssc-ewi-vt0001): Inherited privileges clause is not supported in Snowflake.

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
2. [Grammar Syntax](#grammar-syntax)
3. [Sample Source Patterns](#sample-source-patterns)