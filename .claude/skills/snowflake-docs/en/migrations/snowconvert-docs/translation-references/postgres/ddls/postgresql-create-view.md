---
auto_generated: true
description: Translation from PostgreSQL to Snowflake
last_scraped: '2026-01-14T16:53:33.697956+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/postgres/ddls/postgresql-create-view
title: SnowConvert AI - PostgreSQL - CREATE VIEW | Snowflake Documentation
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
          + [Teradata](../../teradata/README.md)
          + [Oracle](../../oracle/README.md)
          + [SQL Server-Azure Synapse](../../transact/README.md)
          + [Sybase IQ](../../sybase/README.md)
          + [Hive-Spark-Databricks SQL](../../hive/README.md)
          + [Redshift](../../redshift/README.md)
          + [PostgreSQL-Greenplum-Netezza](../README.md)

            - [Built-in Functions](../postgresql-built-in-functions.md)
            - [Data Types](../data-types/postgresql-data-types.md)
            - [String Comparison](../postgresql-string-comparison.md)
            - DDLs

              - [CREATE MATERIALIZED VIEW](create-materialized-view/postgresql-create-materialized-view.md)
              - [CREATE TABLE](create-table/postgresql-create-table.md)
              - [CREATE VIEW](postgresql-create-view.md)
            - [Expressions](../postgresql-expressions.md)
            - [Interactive Terminal](../postgresql-interactive-terminal.md)
            - ETL And BI Repointing

              - [Power BI PostgreSQL Repointing](../etl-bi-repointing/power-bi-postgres-repointing.md)
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

[Guides](../../../../../guides/README.md)[Migrations](../../../../README.md)Tools[SnowConvert AI](../../../overview.md)Translation References[PostgreSQL-Greenplum-Netezza](../README.md)DDLsCREATE VIEW

# SnowConvert AI - PostgreSQL - CREATE VIEW[¶](#snowconvert-ai-postgresql-create-view "Link to this heading")

Translation from PostgreSQL to Snowflake

## Applies to[¶](#applies-to "Link to this heading")

* PostgreSQL
* Greenplum
* Netezza

## Description[¶](#description "Link to this heading")

This command creates a view in a database, which is run every time the view is referenced in a query.

For more information, please refer to [`CREATE VIEW`](https://www.postgresql.org/docs/current/sql-createview.html) documentation.

## Grammar Syntax[¶](#grammar-syntax "Link to this heading")

```
CREATE [OR REPLACE] [TEMP | TEMPORARY] [RECURSIVE] VIEW <name> [ ( <column_name> [, ...] ) ]
    [ WITH ( view_option_name [= view_option_value] [, ... ] ) ]
    AS <query>
    [ WITH [ CASCADED | LOCAL ] CHECK OPTION ]
```

Copy

## Code Examples[¶](#code-examples "Link to this heading")

### [OR REPLACE] [TEMP | TEMPORARY] [RECURSIVE][¶](#or-replace-temp-temporary-recursive "Link to this heading")

Hint

This syntax is fully supported in Snowflake.

#### Input Code:[¶](#input-code "Link to this heading")

##### PostgreSQL[¶](#postgresql "Link to this heading")

```
CREATE OR REPLACE VIEW view1 AS
    SELECT
        product_id,
        SUM(quantity) AS sum_quantity
    FROM
        table1
    GROUP BY
        product_id;

CREATE TEMPORARY RECURSIVE VIEW view2 AS
    SELECT
        product_id,
        SUM(quantity) AS sum_quantity
    FROM
        table1
    GROUP BY
        product_id;
```

Copy

#### Output Code:[¶](#output-code "Link to this heading")

##### Snowflake[¶](#snowflake "Link to this heading")

```
CREATE OR REPLACE VIEW view1
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "postgresql",  "convertedOn": "05/14/2025",  "domain": "no-domain-provided" }}'
AS
    SELECT
        product_id,
        SUM(quantity) AS sum_quantity
    FROM
table1
    GROUP BY
        product_id;

CREATE TEMPORARY RECURSIVE VIEW view2
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "postgresql",  "convertedOn": "05/14/2025",  "domain": "no-domain-provided" }}'
AS
    SELECT
        product_id,
        SUM(quantity) AS sum_quantity
    FROM
table1
    GROUP BY
        product_id;
```

Copy

### WITH CHECK CLAUSE[¶](#with-check-clause "Link to this heading")

This WITH CHECK CLAUSE clause on a view enforces that any data inserted or updated through the view must satisfy the view’s defining conditions. LOCAL checks only the current view’s conditions, while CASCADED checks conditions of the view and all underlying views. It prevents creating rows that are invisible through the view and cannot be used with recursive views.

Danger

This syntax is not supported in Snowflake.

#### Input Code:[¶](#id1 "Link to this heading")

##### PostgreSQL[¶](#id2 "Link to this heading")

```
CREATE VIEW updatable_products AS
    SELECT id, name, price
    FROM products
    WHERE price > 0
WITH LOCAL CHECK OPTION;
```

Copy

#### Output Code:[¶](#id3 "Link to this heading")

##### Snowflake[¶](#id4 "Link to this heading")

```
CREATE VIEW updatable_products
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "postgresql",  "convertedOn": "05/14/2025",  "domain": "no-domain-provided" }}'
AS
    SELECT id, name, price
    FROM
products
    WHERE price > 0;
```

Copy

### WITH PARAMETERS OPTIONS[¶](#with-parameters-options "Link to this heading")

This WITH PARAMETERS OPTIONS allows setting optional properties for the view, such as how modifications through the view are checked (check\_option) and whether to enforce row-level security (security\_barrier).

Danger

This syntax is not supported in Snowflake.

#### Input Code:[¶](#id5 "Link to this heading")

##### PostgreSQL[¶](#id6 "Link to this heading")

```
CREATE VIEW large_orders WITH (security_barrier=true, check_option=local) AS
    SELECT order_id, customer_id, total_amount
    FROM orders
    WHERE total_amount > 1000;
```

Copy

#### Output Code:[¶](#id7 "Link to this heading")

##### Snowflake[¶](#id8 "Link to this heading")

```
CREATE VIEW large_orders
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "postgresql",  "convertedOn": "05/14/2025",  "domain": "no-domain-provided" }}'
AS
    SELECT order_id, customer_id, total_amount
    FROM
orders
    WHERE total_amount > 1000;
```

Copy

### VALUES OPTION[¶](#values-option "Link to this heading")

Hint

This syntax is fully supported in Snowflake.

#### Input Code:[¶](#id9 "Link to this heading")

##### PostgreSQL[¶](#id10 "Link to this heading")

```
CREATE VIEW numbers_view (number_1) AS
    VALUES (1,2), (2,2), (3,2), (4,2), (5,2);
```

Copy

#### Output Code:[¶](#id11 "Link to this heading")

##### Snowflake[¶](#id12 "Link to this heading")

```
CREATE VIEW numbers_view
AS
SELECT
*
FROM
(
        VALUES (1,2), (2,2), (3,2), (4,2), (5,2)
) AS numbers_view (
        number_1
);
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

1. [Applies to](#applies-to)
2. [Description](#description)
3. [Grammar Syntax](#grammar-syntax)
4. [Code Examples](#code-examples)