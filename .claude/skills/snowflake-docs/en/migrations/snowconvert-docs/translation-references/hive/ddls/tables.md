---
auto_generated: true
description: Hive SQL
last_scraped: '2026-01-14T16:53:12.505457+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/hive/ddls/tables
title: SnowConvert AI - Hive - CREATE TABLE | Snowflake Documentation
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

[Guides](../../../../../guides/README.md)[Migrations](../../../../README.md)Tools[SnowConvert AI](../../../overview.md)Translation References[Hive-Spark-Databricks SQL](../README.md)[DDLs](README.md)CREATE TABLE

# SnowConvert AI - Hive - CREATE TABLE[¶](#snowconvert-ai-hive-create-table "Link to this heading")

Applies to

* Hive SQL
* Spark SQL
* Databricks SQL

## Description[¶](#description "Link to this heading")

Creates a new table in the current database. You define a list of columns, which each hold data of a distinct type. The owner of the table is the issuer of the CREATE TABLE command.

For more information, please refer to [`CREATE TABLE`](https://spark.apache.org/docs/3.5.3/sql-ref-syntax-ddl-create-table.html) documentation.

## Grammar Syntax [¶](#grammar-syntax "Link to this heading")

```
--DATASOURCE TABLE
CREATE TABLE [ IF NOT EXISTS ] table_identifier
    [ ( col_name1 col_type1 [ COMMENT col_comment1 ], ... ) ]
    USING data_source
    [ OPTIONS ( key1=val1, key2=val2, ... ) ]
    [ PARTITIONED BY ( col_name1, col_name2, ... ) ]
    [ CLUSTERED BY ( col_name3, col_name4, ... ) 
        [ SORTED BY ( col_name [ ASC | DESC ], ... ) ] 
        INTO num_buckets BUCKETS ]
    [ LOCATION path ]
    [ COMMENT table_comment ]
    [ TBLPROPERTIES ( key1=val1, key2=val2, ... ) ]
    [ AS select_statement ]
    
--HIVE FORMAT TABLE
CREATE [ EXTERNAL ] TABLE [ IF NOT EXISTS ] table_identifier
    [ ( col_name1[:] col_type1 [ COMMENT col_comment1 ], ... ) ]
    [ COMMENT table_comment ]
    [ PARTITIONED BY ( col_name2[:] col_type2 [ COMMENT col_comment2 ], ... ) 
        | ( col_name1, col_name2, ... ) ]
    [ CLUSTERED BY ( col_name1, col_name2, ...) 
        [ SORTED BY ( col_name1 [ ASC | DESC ], col_name2 [ ASC | DESC ], ... ) ] 
        INTO num_buckets BUCKETS ]
    [ ROW FORMAT row_format ]
    [ STORED AS file_format ]
    [ LOCATION path ]
    [ TBLPROPERTIES ( key1=val1, key2=val2, ... ) ]
    [ AS select_statement ]
    
--LIKE TABLE
CREATE TABLE [IF NOT EXISTS] table_identifier LIKE source_table_identifier
    USING data_source
    [ ROW FORMAT row_format ]
    [ STORED AS file_format ]
    [ TBLPROPERTIES ( key1=val1, key2=val2, ... ) ]
    [ LOCATION path ]
```

Copy

## IF NOT EXISTS [¶](#if-not-exists "Link to this heading")

## Description[¶](#id1 "Link to this heading")

> Ensures the table is created only if it does not already exist, preventing duplication and errors in your SQL script.

Hint

This syntax is fully supported in Snowflake.

## Applies to[¶](#applies-to "Link to this heading")

* Hive
* Spark
* Databricks

## Grammar Syntax[¶](#id2 "Link to this heading")

```
IF NOT EXISTS
```

Copy

## Sample Source Patterns[¶](#sample-source-patterns "Link to this heading")

## Input Code:[¶](#input-code "Link to this heading")

```
CREATE TABLE IF NOT EXISTS table1 (
    col1 INTEGER
);
```

Copy

## Output Code:[¶](#output-code "Link to this heading")

```
CREATE TABLE IF NOT EXISTS table1 (
    col1 INTEGER
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "sybase",  "convertedOn": "03/19/2024" }}';
```

Copy

## PARTITION BY[¶](#partition-by "Link to this heading")

## Description[¶](#id3 "Link to this heading")

> Partitions are created on the table, based on the columns specified.

This syntax is not needed in Snowflake.

## Applies to[¶](#id4 "Link to this heading")

* Hive
* Spark
* Databricks

## Grammar Syntax[¶](#id5 "Link to this heading")

```
PARTITIONED BY ( { partition_column [ column_type ] } [, ...] )
```

Copy

## Sample Source Patterns[¶](#id6 "Link to this heading")

## Input Code:[¶](#id7 "Link to this heading")

```
CREATE TABLE orders (
    order_id INT,
    customer_id INT,
    order_date DATE,
    total_amount DECIMAL(10, 2),
    order_status STRING
)
PARTITIONED BY (order_status);
```

Copy

## Output Code:[¶](#id8 "Link to this heading")

```
CREATE TABLE orders (
    order_id INT,
    customer_id INT,
    order_date DATE,
    total_amount DECIMAL(10, 2),
    order_status STRING
);
```

Copy

## CLUSTERED BY[¶](#clustered-by "Link to this heading")

## Description[¶](#id9 "Link to this heading")

> Partitions created on the table will be bucketed into fixed buckets based on the column specified for bucketing.

This grammar is partially supported

## Applies to[¶](#id10 "Link to this heading")

* Hive
* Spark
* Databricks

## Grammar Syntax[¶](#id11 "Link to this heading")

```
CLUSTERED BY (column_name1 [ASC|DESC], ...)
[SORTED BY (sort_column1 [ASC|DESC], ...)]
INTO num_buckets BUCKETS
```

Copy

* The **`CLUSTERED BY`** clause, used for performance optimization, will be converted to **`CLUSTER BY`** in Snowflake. Performance may vary between the two architectures.
* The **`SORTED BY`** clause can be removed during migration, as Snowflake automatically handles data sorting within its micro-partitions.
* The **`INTO BUCKETS`** clause, a SparkSQL/Databrick specific partitioning setting, should be entirely eliminated, as it’s not applicable in Snowflake.

## Sample Source Patterns[¶](#id12 "Link to this heading")

## Input Code:[¶](#id13 "Link to this heading")

```
CREATE TABLE table_name ( 
column1 data_type, column2 data_type, ... ) USING format CLUSTERED BY (bucketing_column1) SORTED BY (sorting_column1 DESC, sorting_column2 ASC) INTO 10 BUCKETS;
```

Copy

## Output Code:[¶](#id14 "Link to this heading")

```
CREATE TABLE table_name ( column1 data_type, column2 data_type, ... ) USING format
CLUSTER BY (bucketing_column1);
```

Copy

## ROW FORMAT[¶](#row-format "Link to this heading")

## Description[¶](#id15 "Link to this heading")

> Specifies the row format for input and output.

This grammar is not supported in Snowflake

## Applies to[¶](#id16 "Link to this heading")

* Hive
* Spark
* Databricks

## Grammar Syntax[¶](#id17 "Link to this heading")

```
ROW FORMAT fow_format

row_format:
   { SERDE serde_class [ WITH SERDEPROPERTIES (serde_key = serde_val [, ...] ) ] |
     { DELIMITED [ FIELDS TERMINATED BY fields_terminated_char [ ESCAPED BY escaped_char ] ]
       [ COLLECTION ITEMS TERMINATED BY collection_items_terminated_char ]
       [ MAP KEYS TERMINATED BY map_key_terminated_char ]
       [ LINES TERMINATED BY row_terminated_char ]
       [ NULL DEFINED AS null_char ] } }
```

Copy

## Sample Source Patterns[¶](#id18 "Link to this heading")

## Input Code:[¶](#id19 "Link to this heading")

```
CREATE TABLE parquet_table ( id INT, data STRING )  STORED AS TEXTFILE LOCATION '/mnt/delimited/target' ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' ESCAPED BY '\\' COLLECTION ITEMS TERMINATED BY ';' MAP KEYS TERMINATED BY ':' LINES TERMINATED BY '\n' NULL DEFINED AS 'NULL_VALUE';
```

Copy

## Output Code:[¶](#id20 "Link to this heading")

```
CREATE TABLE delimited_like_delta LIKE source_delta_table STORED AS TEXTFILE LOCATION '/mnt/delimited/target'
!!!RESOLVE EWI!!! /*** SSC-EWI-HV0002 - THE ROW FORMAT CLAUSE IS NOT SUPPORTED IN SNOWFLAKE ***/!!! ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' ESCAPED BY '\\' COLLECTION ITEMS TERMINATED BY ';' MAP KEYS TERMINATED BY ':' LINES TERMINATED BY '\n' NULL DEFINED AS 'NULL_VALUE';
```

Copy

## STORED AS[¶](#stored-as "Link to this heading")

## Description[¶](#id21 "Link to this heading")

> File format for table storage.

This grammar is not supported in Snowflake

## Applies to[¶](#id22 "Link to this heading")

* Hive
* Spark
* Databricks

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
3. [IF NOT EXISTS](#if-not-exists)
4. [Description](#id1)
5. [Applies to](#applies-to)
6. [Grammar Syntax](#id2)
7. [Sample Source Patterns](#sample-source-patterns)
8. [Input Code:](#input-code)
9. [Output Code:](#output-code)
10. [PARTITION BY](#partition-by)
11. [Description](#id3)
12. [Applies to](#id4)
13. [Grammar Syntax](#id5)
14. [Sample Source Patterns](#id6)
15. [Input Code:](#id7)
16. [Output Code:](#id8)
17. [CLUSTERED BY](#clustered-by)
18. [Description](#id9)
19. [Applies to](#id10)
20. [Grammar Syntax](#id11)
21. [Sample Source Patterns](#id12)
22. [Input Code:](#id13)
23. [Output Code:](#id14)
24. [ROW FORMAT](#row-format)
25. [Description](#id15)
26. [Applies to](#id16)
27. [Grammar Syntax](#id17)
28. [Sample Source Patterns](#id18)
29. [Input Code:](#id19)
30. [Output Code:](#id20)
31. [STORED AS](#stored-as)
32. [Description](#id21)
33. [Applies to](#id22)