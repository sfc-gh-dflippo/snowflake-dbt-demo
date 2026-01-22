---
auto_generated: true
description: Hive SQL
last_scraped: '2026-01-14T16:53:12.136946+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/hive/ddls/select
title: SnowConvert AI - Hive - SELECT | Snowflake Documentation
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
          + [Hive-Spark-Databricks SQL](../README.md)

            - [DDLs](README.md)

              * [CREATE TABLE](tables.md)
              * [CREATE EXTERNAL TABLE](create-external-table.md)
              * [CREATE VIEW](create-view.md)
              * [SELECT](select.md)
            - [Built-in Functions](../built-in-functions.md)
            - [Data Types](../data-types.md)
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

[Guides](../../../../../guides/README.md)[Migrations](../../../../README.md)Tools[SnowConvert AI](../../../overview.md)Translation References[Hive-Spark-Databricks SQL](../README.md)[DDLs](README.md)SELECT

# SnowConvert AI - Hive - SELECT[¶](#snowconvert-ai-hive-select "Link to this heading")

Applies to

* Hive SQL
* Spark SQL
* Databricks SQL

## Description[¶](#description "Link to this heading")

Spark supports a `SELECT` statement and conforms to the ANSI SQL standard. Queries are used to retrieve result sets from one or more tables. ([Spark SQL Language Reference SELECT](https://spark.apache.org/docs/latest/sql-ref-syntax-qry-select.html))

Warning

This grammar is partially supported in Snowflake. Translation pending for these CREATE VIEW elements:

```
[ SORT BY { expression [ ASC | DESC ] [ NULLS { FIRST | LAST } ] [ , ... ] } ]
[ CLUSTER BY { expression [ , ... ] } ]
[ DISTRIBUTE BY { expression [, ... ] } ]
[ WINDOW { named_window [ , WINDOW named_window, ... ] } ]
[ PIVOT clause ]
[ UNPIVOT clause ]
[ LATERAL VIEW clause ] [ ... ]
[ regex_column_names ]
[ TRANSFORM (...) ]
[ LIMIT non_literal_expression ]

from_item :=
join_relation
table_value_function
LATERAL(subquery)
file_format.`file_path`

select_statement { INTERSECT | EXCEPT } { ALL | DISTINCT } select_statement
```

Copy

## Grammar Syntax[¶](#grammar-syntax "Link to this heading")

```
[ WITH with_query [ , ... ] ]
select_statement [ { UNION | INTERSECT | EXCEPT } [ ALL | DISTINCT ] select_statement, ... ]
    [ ORDER BY { expression [ ASC | DESC ] [ NULLS { FIRST | LAST } ] [ , ... ] } ]
    [ SORT BY { expression [ ASC | DESC ] [ NULLS { FIRST | LAST } ] [ , ... ] } ]
    [ CLUSTER BY { expression [ , ... ] } ]
    [ DISTRIBUTE BY { expression [, ... ] } ]
    [ WINDOW { named_window [ , WINDOW named_window, ... ] } ]
    [ LIMIT { ALL | expression } ]

select_statement :=
SELECT [ hints , ... ] [ ALL | DISTINCT ] { [ [ named_expression | regex_column_names ] [ , ... ] | TRANSFORM (...) ] }
    FROM { from_item [ , ... ] }
    [ PIVOT clause ]
    [ UNPIVOT clause ]
    [ LATERAL VIEW clause ] [ ... ] 
    [ WHERE boolean_expression ]
    [ GROUP BY expression [ , ... ] ]
    [ HAVING boolean_expression ]
    
with_query :=
expression_name [ ( column_name [ , ... ] ) ] [ AS ] ( query )

from_item :=
table_relation |
join_relation |
table_value_function |
inline_table |
LATERAL(subquery) |
file_format.`file_path`
```

Copy

## Sample Source Patterns[¶](#sample-source-patterns "Link to this heading")

### GROUP BY[¶](#group-by "Link to this heading")

The `WITH { CUBE | ROLLUP }` syntax is transformed to its `CUBE(expr1, ...)` or `ROLLUP(expr1, ...)` equivalent

#### Input Code:[¶](#input-code "Link to this heading")

```
-- Basic case of GROUP BY
SELECT id, sum(quantity) FROM dealer GROUP BY 1;

-- Grouping by GROUPING SETS
SELECT city, car_model, sum(quantity) AS sum FROM dealer
    GROUP BY GROUPING SETS ((city, car_model), (city), (car_model), ());

-- Grouping by ROLLUP
SELECT city, car_model, sum(quantity) AS sum FROM dealer
    GROUP BY ROLLUP(city, car_model);

SELECT city, car_model, sum(quantity) AS sum FROM dealer
    GROUP BY city, car_model WITH ROLLUP;

-- Grouping by CUBE
SELECT city, car_model, sum(quantity) AS sum FROM dealer
    GROUP BY CUBE(city, car_model);

SELECT city, car_model, sum(quantity) AS sum FROM dealer
    GROUP BY city, car_model WITH CUBE;
```

Copy

#### Output Code:[¶](#output-code "Link to this heading")

```
-- Basic case of GROUP BY
SELECT id,
    SUM(quantity) FROM
    dealer
GROUP BY 1;

-- Grouping by GROUPING SETS
SELECT city, car_model,
    SUM(quantity) AS sum FROM
    dealer
    GROUP BY GROUPING SETS ((city, car_model), (city), (car_model), () !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'EmptyGroupingSet' NODE ***/!!!);

-- Grouping by ROLLUP
SELECT city, car_model,
    SUM(quantity) AS sum FROM
    dealer
    GROUP BY
    ROLLUP(city, car_model);

SELECT city, car_model,
    SUM(quantity) AS sum FROM
    dealer
GROUP BY
    ROLLUP(city, car_model);

-- Grouping by CUBE
SELECT city, car_model,
    SUM(quantity) AS sum FROM
    dealer
    GROUP BY CUBE(city, car_model) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'CUBE' NODE ***/!!!;

SELECT city, car_model,
    SUM(quantity) AS sum FROM
    dealer
GROUP BY
    CUBE(city, car_model);
```

Copy

### Hints[¶](#hints "Link to this heading")

Snowflake performs automatic optimization of JOINs and partitioning, meaning that hints are unnecessary, they are preserved as comments in the output code.

#### Input Code:[¶](#id1 "Link to this heading")

```
SELECT
/*+ REBALANCE */ /*+ COALESCE(2) */
*
FROM my_table;
```

Copy

#### Output Code:[¶](#id2 "Link to this heading")

```
SELECT
/*+ REBALANCE */ /*+ COALESCE(2) */
*
FROM
my_table;
```

Copy

### CTE[¶](#cte "Link to this heading")

The `AS` keyword is optional in Spark/Databricks, however in Snowflake is required so it is added.

#### Input Code:[¶](#id3 "Link to this heading")

```
WITH my_cte (
   SELECT id, name FROM my_table
)
SELECT *
FROM my_cte
WHERE id = 1;
```

Copy

#### Output Code:[¶](#id4 "Link to this heading")

```
WITH my_cte AS (
     SELECT id, name FROM
        my_table
  )
SELECT *
FROM
     my_cte
WHERE id = 1;
```

Copy

### LIMIT[¶](#limit "Link to this heading")

`LIMIT ALL` is removed as it is not needed in Snowflake, LIMIT with a literal value is preserved as-is.

#### Input Code:[¶](#id5 "Link to this heading")

```
SELECT * FROM my_table LIMIT ALL;

SELECT * FROM my_table LIMIT 5;
```

Copy

#### Output Code:[¶](#id6 "Link to this heading")

```
SELECT * FROM
my_table;

SELECT * FROM
my_table
LIMIT 5;
```

Copy

### ORDER BY[¶](#order-by "Link to this heading")

Note

This clause is fully supported in Snowflake

### WHERE[¶](#where "Link to this heading")

Note

This clause is fully supported in Snowflake

### HAVING[¶](#having "Link to this heading")

Note

This clause is fully supported in Snowflake

### FROM table\_relation[¶](#from-table-relation "Link to this heading")

Note

This clause is fully supported in Snowflake

### FROM inline\_table[¶](#from-inline-table "Link to this heading")

Note

This clause is fully supported in Snowflake

### UNION [ALL | DISTINCT][¶](#union-all-distinct "Link to this heading")

Note

This clause is fully supported in Snowflake

### INTERSECT (no keywords)[¶](#intersect-no-keywords "Link to this heading")

Note

This clause is fully supported in Snowflake

### EXCEPT (no keywords)[¶](#except-no-keywords "Link to this heading")

Note

This clause is fully supported in Snowflake

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