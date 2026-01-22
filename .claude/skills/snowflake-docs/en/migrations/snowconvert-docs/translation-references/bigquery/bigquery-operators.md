---
auto_generated: true
description: IS operators return TRUE or FALSE for the condition they are testing.
  They never return NULL, even for NULL inputs. (BigQuery SQL Language Reference IS
  operators)
last_scraped: '2026-01-14T16:53:04.812061+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/bigquery/bigquery-operators
title: SnowConvert AI - BigQuery - Operators | Snowflake Documentation
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
          + [BigQuery](README.md)

            - [Built-in Functions](bigquery-functions.md)
            - [Data Types](bigquery-data-types.md)
            - [CREATE TABLE](bigquery-create-table.md)
            - [CREATE VIEW](bigquery-create-view.md)
            - [Identifier differences between BigQuery and Snowflake](bigquery-identifiers.md)
            - [Operators](bigquery-operators.md)
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)Translation References[BigQuery](README.md)Operators

# SnowConvert AI - BigQuery - Operators[¶](#snowconvert-ai-bigquery-operators "Link to this heading")

## IS operators[¶](#is-operators "Link to this heading")

IS operators return `TRUE` or `FALSE` for the condition they are testing. They never return `NULL`, even for `NULL` inputs. ([BigQuery SQL Language Reference IS operators](https://cloud.google.com/bigquery/docs/reference/standard-sql/operators?hl=en#is_operators))

| BigQuery | Snowflake |
| --- | --- |
| `X IS TRUE` | `NVL(X, FALSE)` |
| `X IS NOT TRUE` | `NVL(NOT X, TRUE)` |
| `X IS FALSE` | `NVL(NOT X, FALSE)` |
| `X IS NOT FALSE` | `NVL(X, TRUE)` |
| `X IS NULL` | `X IS NULL` |
| `X IS NOT NULL` | `X IS NOT NULL` |
| `X IS UNKNOWN` | `X IS NULL` |
| `X IS NOT UNKNOWN` | `X IS NOT NULL` |

## UNNEST operator[¶](#unnest-operator "Link to this heading")

The UNNEST operator takes an array and returns a table with one row for each element in the array. ([BigQuery SQL Language Reference UNNEST operator](https://cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax#unnest_operator)).

This operator will be emulated using the [FLATTEN](../../../../sql-reference/functions/flatten) function, the `VALUE` and `INDEX` columns returned by the function will be renamed accordingly to match the UNNEST operator aliases

| BigQuery | Snowflake |
| --- | --- |
| `UNNEST(arrayExpr)` | `FLATTEN(INPUT => arrayExpr) AS F0_(SEQ, KEY, PATH, INDEX, F0_, THIS)` |
| `UNNEST(arrayExpr) AS alias` | `FLATTEN(INPUT => arrayExpr) AS alias(SEQ, KEY, PATH, INDEX, alias, THIS)` |
| `UNNEST(arrayExpr) AS alias WITH OFFSET` | `FLATTEN(INPUT => arrayExpr) AS alias(SEQ, KEY, PATH, OFFSET, alias, THIS)` |
| `UNNEST(arrayExpr) AS alias WITH OFFSET AS offsetAlias` | `FLATTEN(INPUT => arrayExpr) AS alias(SEQ, KEY, PATH, offsetAlias, alias, THIS)` |

### SELECT \* with UNNEST[¶](#select-with-unnest "Link to this heading")

When the UNNEST operator is used inside a SELECT \* statement the `EXCLUDE` keyword will be used to remove the unnecessary FLATTEN columns.

Input:

```
SELECT * FROM UNNEST ([10,20,30]) AS numbers WITH OFFSET position;
```

Copy

Generated code:

```
 SELECT
* EXCLUDE(SEQ, KEY, PATH, THIS)
FROM
TABLE(FLATTEN(INPUT => [10,20,30])) AS numbers (
SEQ,
KEY,
PATH,
position,
numbers,
THIS
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

1. [IS operators](#is-operators)
2. [UNNEST operator](#unnest-operator)