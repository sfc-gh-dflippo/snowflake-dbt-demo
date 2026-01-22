---
auto_generated: true
description: An expression used to evaluate and compare each element of an array against
  a specified expression. (Vertica Language Reference ANY & ALL (array))
last_scraped: '2026-01-14T16:54:12.860739+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/vertica/vertica-predicates
title: SnowConvert AI - Vertica - Predicates | Snowflake Documentation
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)Translation References[Vertica](README.md)Predicates

# SnowConvert AI - Vertica - Predicates[¶](#snowconvert-ai-vertica-predicates "Link to this heading")

## ALL & ANY array expressions[¶](#all-any-array-expressions "Link to this heading")

### Description[¶](#description "Link to this heading")

An expression used to **evaluate and compare** each element of an array against a specified expression. ([Vertica Language Reference ANY & ALL (array)](https://docs.vertica.com/23.4.x/en/sql-reference/language-elements/predicates/any-and-all/))

### Grammar Syntax[¶](#grammar-syntax "Link to this heading")

```
expression operator ANY (array expression)
expression operator ALL (array expression)
```

Copy

To support this expression SnowConvert AI translates the `<> ALL` to `NOT IN` and the `= ANY` to `IN`

### Sample Source Patterns[¶](#sample-source-patterns "Link to this heading")

#### Input Code:[¶](#input-code "Link to this heading")

```
SELECT some_column <> ALL (ARRAY[1, 2, 3]) 
FROM some_table;

SELECT *
FROM someTable
WHERE column_name = ANY (ARRAY[1, 2, 3]);
```

Copy

#### Output Code:[¶](#output-code "Link to this heading")

```
SELECT some_column NOT IN (1, 2, 3)
FROM some_table;

SELECT *
 FROM someTable
 WHERE column_name IN (1, 2, 3);
```

Copy

#### Known Issues[¶](#known-issues "Link to this heading")

There are no known issues

#### Related EWIs[¶](#related-ewis "Link to this heading")

There are no related EWIs.

## LIKE[¶](#like "Link to this heading")

LIKE Predicate

### Description[¶](#id1 "Link to this heading")

> Retrieves rows where a string expression—typically a column—matches the specified pattern or, if qualified by ANY or ALL, set of patterns ([Vertica SQL Language Reference Like Predicate](https://docs.vertica.com/23.4.x/en/sql-reference/language-elements/predicates/like/))

### Grammar Syntax[¶](#id2 "Link to this heading")

```
 string-expression [ NOT ] { LIKE | ILIKE | LIKEB | ILIKEB }
   { pattern | { ANY | SOME | ALL } ( pattern,... ) } [ ESCAPE 'char' ]
```

Copy

#### Vertica Substitute symbols[¶](#vertica-substitute-symbols "Link to this heading")

| Symbol | Vertica Equivalent | Snowflake Equivalent |
| --- | --- | --- |
| ~~ | LIKE | LIKE |
| ~# | LIKEB | LIKE |
| ~~\* | ILIKE | ILIKE |
| ~#\* | ILIKEB | ILIKE |
| !~~ | NOT LIKE | NOT LIKE |
| !~# | NOT LIKEB | NOT LIKE |
| !~~\* | NOT ILIKE | NOT ILIKE |
| !~#\* | NOT ILIKEB | NOT ILIKE |

In Vertica, the default escape character is the backslash (`\`). Snowflake doesn’t have a default escape character. SnowConvert AI will automatically add the `ESCAPE` clause when needed.

It’s important to know that Snowflake requires the backslash to be escaped (`\\`) when you use it as an escape character within both the expression and the `ESCAPE` clause. This means you’ll need two backslashes to represent a single literal backslash escape character in Snowflake queries. SnowConvert AI handles this by automatically escaping the backslash for you.

### Sample Source Patterns[¶](#id3 "Link to this heading")

Success

This syntax is fully supported in [Snowflake](https://docs.snowflake.com/en/sql-reference/sql/create-view).

#### Vertica[¶](#vertica "Link to this heading")

```
 SELECT path_name
FROM file_paths
WHERE path_name ~~ '/report/sales_2025_q_.csv';

-- Find a path containing the literal '50%'
SELECT path_name
FROM file_paths
WHERE path_name LIKE '%50\%%';

-- Find a path starting with 'C:\'
SELECT path_name
FROM file_paths
WHERE path_name ILIKEB 'C:\\%' ESCAPE'\';
```

Copy

#### Snowflake[¶](#snowflake "Link to this heading")

```
SELECT path_name
FROM file_paths
WHERE path_name LIKE '/report/sales_2025_q_.csv';

-- Find a path containing the literal '50%'
SELECT path_name
FROM file_paths
WHERE path_name LIKE '%50\\%%' ESCAPE'\\';

-- Find a path starting with 'C:\'
SELECT path_name
FROM file_paths
WHERE path_name ILIKE 'C:\\\\%' ESCAPE'\\';
```

Copy

#### Known Issues[¶](#id4 "Link to this heading")

While SnowConvert AI handles most backslash patterns, some **complex expressions** may still cause **query failures**. We recommend reviewing complex patterns to prevent these issues.

#### Related EWIs[¶](#id5 "Link to this heading")

There are no related EWIs.

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

1. [ALL & ANY array expressions](#all-any-array-expressions)
2. [LIKE](#like)