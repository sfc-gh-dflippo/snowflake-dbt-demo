---
auto_generated: true
description: In general, Snowflake produces well-clustered data in tables; however,
  over time, particularly as DML occurs on very large tables (as defined by the amount
  of data in the table, not the number of rows
last_scraped: '2026-01-14T16:55:58.360198+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/tables-clustering-keys.html
title: Clustering Keys & Clustered Tables | Snowflake Documentation
---

1. [Overview](../guides/README.md)
2. [Snowflake Horizon Catalog](snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../guides/overview-connecting.md)
6. [Virtual warehouses](warehouses.md)
7. [Databases, Tables, & Views](../guides/overview-db.md)

   * [Table Structures](tables-micro-partitions.md)

     + [Micro-Partitions & Data Clustering](tables-clustering-micropartitions.md)
     + [Cluster Keys & Clustered Tables](tables-clustering-keys.md)
     + [Automatic Clustering](tables-auto-reclustering.md)
   * [Temporary And Transient Tables](tables-temp-transient.md)
   * [External Tables](tables-external-intro.md)
   * [Hybrid Tables](tables-hybrid.md)
   * [Interactive tables](interactive.md)
   * [Working with tables in Snowsight](ui-snowsight-data-databases-table.md)
   * [Search optimization service](search-optimization-service.md)
   * Views
   * [Views](views-introduction.md)
   * [Secure Views](views-secure.md)
   * [Materialized Views](views-materialized.md)
   * [Semantic Views](views-semantic/overview.md)
   * [Working with Views in Snowsight](ui-snowsight-data-databases-view.md)
   * Considerations
   * [Views, Materialized Views, and Dynamic Tables](overview-view-mview-dts.md)
   * [Table Design](table-considerations.md)
   * [Cloning](object-clone.md)
   * [Data Storage](tables-storage-considerations.md)
8. [Data types](../data-types.md)
10. Data Integration

    - [Snowflake Openflow](data-integration/openflow/about.md)
    - Apache Iceberg™

      - [Apache Iceberg™ Tables](tables-iceberg.md)
      - [Snowflake Open Catalog](opencatalog/overview.md)
11. Data engineering

    - [Data loading](../guides/overview-loading-data.md)
    - [Dynamic Tables](dynamic-tables-about.md)
    - [Streams and Tasks](data-pipelines-intro.md)
    - [dbt Projects on Snowflake](data-engineering/dbt-projects-on-snowflake.md)
    - [Data Unloading](../guides/overview-unloading-data.md)
12. [Storage Lifecycle Policies](storage-management/storage-lifecycle-policies.md)
13. [Migrations](../migrations/README.md)
15. [Queries](../guides/overview-queries.md)
16. [Listings](../collaboration/collaboration-listings-about.md)
17. [Collaboration](../guides/overview-sharing.md)
19. [Snowflake AI & ML](../guides/overview-ai-features.md)
21. [Snowflake Postgres](snowflake-postgres/about.md)
23. [Alerts & Notifications](../guides/overview-alerts.md)
25. [Security](../guides/overview-secure.md)
26. [Data Governance](../guides/overview-govern.md)
27. [Privacy](../guides/overview-privacy.md)
29. [Organizations & Accounts](../guides/overview-manage.md)
30. [Business continuity & data recovery](replication-intro.md)
32. [Performance optimization](../guides/overview-performance.md)
33. [Cost & Billing](../guides/overview-cost.md)

[Guides](../guides/README.md)[Databases, Tables, & Views](../guides/overview-db.md)[Table Structures](tables-micro-partitions.md)Cluster Keys & Clustered Tables

# Clustering Keys & Clustered Tables[¶](#clustering-keys-clustered-tables "Link to this heading")

In general, Snowflake produces well-clustered data in tables; however, over time, particularly as DML occurs on very large tables (as defined by the amount of data in the table,
not the number of rows), the data in some table rows might no longer cluster optimally on desired dimensions.

To improve the clustering of the underlying table micro-partitions, you can always manually sort rows on key table columns and re-insert them into the table; however, performing
these tasks could be cumbersome and expensive.

Instead, Snowflake supports automating these tasks by designating one or more table columns/expressions as a *clustering key* for the table. A table with a clustering key defined
is considered to be *clustered*.

You can cluster [materialized views](views-materialized), as well as tables. The rules for
clustering tables and materialized views are generally the same. For a few additional tips specific to materialized
views, see [Materialized Views and Clustering](views-materialized.html#label-clustering-base-table-and-materialized-view) and
[Best Practices for Materialized Views](views-materialized.html#label-best-practices-for-materialized-views).

Attention

Clustering keys are not intended for all tables due to the costs of initially clustering the data and
maintaining the clustering. Clustering is optimal when either:

* You require the fastest possible response times, regardless of cost.
* Your improved query performance offsets the credits required to cluster and maintain the table.

For more information about choosing which tables to cluster, see: [Considerations for Choosing Clustering for a Table](#label-considerations-for-choosing-clustering).

## What is a Clustering Key?[¶](#what-is-a-clustering-key "Link to this heading")

A clustering key is a subset of columns in a table (or expressions on a table) that are explicitly designated to co-locate the data in the table in the same
[micro-partitions](tables-clustering-micropartitions). This is useful for very large tables where the ordering was not ideal (at the time the data was inserted/loaded) or
extensive DML has caused the table’s natural clustering to degrade.

Some general indicators that can help determine whether to define a clustering key for a table include:

* Queries on the table are running slower than expected or have noticeably degraded over time.
* The [clustering depth](tables-clustering-micropartitions.html#label-clustering-depth) for the table is large.

A clustering key can be defined at table creation (using the [CREATE TABLE](../sql-reference/sql/create-table) command) or afterward (using the [ALTER TABLE](../sql-reference/sql/alter-table) command).
The clustering key for a table can also be altered or dropped at any time.

Attention

Clustering keys cannot be defined for [hybrid tables](tables-hybrid). In hybrid tables, data is always ordered by primary key.

## Benefits of Defining Clustering Keys (for Very Large Tables)[¶](#benefits-of-defining-clustering-keys-for-very-large-tables "Link to this heading")

Using a clustering key to co-locate similar rows in the same micro-partitions enables several benefits for very large tables, including:

* Improved scan efficiency in queries by skipping data that does not match filtering predicates.
* Better column compression than in tables with no clustering. This is especially true when other columns are strongly correlated with the columns that comprise the clustering key.
* After a key has been defined on a table, no additional administration is required, unless you chose to drop or modify the key. All future maintenance on the rows in the table
  (to ensure optimal clustering) is performed automatically by Snowflake.

Although clustering can substantially improve the performance and reduce the cost of some queries, the compute resources used to perform clustering consume credits. As such, you
should cluster only when queries will benefit substantially from the clustering.

Typically, queries benefit from clustering when the queries filter or sort on the clustering key for the table. Sorting is commonly done for `ORDER BY` operations,
for `GROUP BY` operations, and for some joins. For example, the following join would likely cause Snowflake to perform a sort operation:

> ```
> SELECT ...
>     FROM my_table INNER JOIN my_materialized_view
>         ON my_materialized_view.col1 = my_table.col1
>     ...
> ```
>
> Copy

In this pseudo-example, Snowflake is likely to sort the values in either `my_materialized_view.col1` or `my_table.col1`. For example, if the values in `my_table.col1` are
sorted, then as the materialized view is being scanned, Snowflake can quickly find the corresponding row in `my_table`.

The more frequently a table is queried, the more benefit clustering provides. However, the more frequently a table changes, the more expensive it will be to keep it
clustered. Therefore, clustering is generally most cost-effective for tables that are queried frequently and do not change frequently.

Note

After you define a clustering key for a table, the rows are not necessarily updated immediately. Snowflake only performs automated maintenance if the table will benefit from
the operation. For more details, see [Reclustering](#reclustering) (in this topic) and [Automatic Clustering](tables-auto-reclustering).

## Considerations for Choosing Clustering for a Table[¶](#considerations-for-choosing-clustering-for-a-table "Link to this heading")

Whether you want faster response times or lower overall costs, clustering is best for a table that meets all of
the following criteria:

* The table contains a large number of [micro-partitions](tables-clustering-micropartitions). Typically, this means that
  the table contains multiple terabytes (TB) of data.
* The queries can take advantage of clustering. Typically, this means that one or both of the following are true:

  + The queries are selective. In other words, the queries need to read only a small percentage of rows (and thus usually a small
    percentage of micro-partitions) in the table.
  + The queries sort the data. (For example, the query contains an ORDER BY clause on the table.)
* A high percentage of the queries can benefit from the same clustering key(s). In other words, many/most queries select on,
  or sort on, the same few column(s).

If your goal is primarily to reduce overall costs, then each clustered table should have a high ratio of queries to DML operations
(INSERT/UPDATE/DELETE). This typically means that the table is queried frequently and updated infrequently. If you want to
cluster a table that experiences a lot of DML, then consider grouping DML statements in large, infrequent batches.

Also, before choosing to cluster a table, Snowflake strongly recommends that you test a representative set of queries on
the table to establish some performance baselines.

## Strategies for Selecting Clustering Keys[¶](#strategies-for-selecting-clustering-keys "Link to this heading")

A single clustering key can contain one or more columns or expressions. For most tables, Snowflake recommends a
maximum of 3 or 4 columns (or expressions) per key. Adding more than 3-4 columns tends to increase costs more than
benefits.

Selecting the right columns/expressions for a clustering key can dramatically impact query performance. Analysis of
your workload will usually yield good clustering key candidates.

Snowflake recommends prioritizing keys in the order below:

1. Cluster columns that are most actively used in selective filters. For many fact tables involved in date-based
   queries (for example “WHERE invoice\_date > x AND invoice date <= y”), choosing the date column is a good idea.
   For event tables, event type might be a good choice, if there are a large number of different event types. (If your
   table has only a small number of different event types, then see the comments on cardinality below before choosing
   an event column as a clustering key.)
2. If there is room for additional cluster keys, then consider columns frequently used in join predicates, for example
   “FROM table1 JOIN table2 ON table2.column\_A = table1.column\_B”.

If you typically filter queries by two dimensions (e.g. `application_id` and `user_status` columns), then
clustering on both columns can improve performance.

The number of distinct values (i.e. cardinality) in a column/expression is a critical aspect of selecting it as a clustering key. It is important to choose a clustering key that has:

* A large enough number of distinct values to enable effective pruning on the table.
* A small enough number of distinct values to allow Snowflake to effectively group rows in the same micro-partitions.

A column with very low cardinality might yield only minimal pruning, such as a column named `IS_NEW_CUSTOMER`
that contains only Boolean values.
At the other extreme, a column with very high cardinality is also typically not a good candidate to use as a clustering key directly.
For example, a column that contains nanosecond timestamp values would not make a good clustering key.

Tip

In general, if a column (or expression) has higher cardinality, then maintaining clustering on that column is
more expensive.

The cost of clustering on a unique key might be more than the benefit of clustering on that key,
especially if point lookups are not the primary use case for that table.

If you want to use a column with very high cardinality as a clustering key, Snowflake recommends defining the key as an
expression on the column, rather than on the column directly, to reduce the number of distinct values. The
expression should preserve the original ordering of the column so that the minimum and maximum values in each
partition still enable pruning.

For example, if a fact table has a TIMESTAMP column `c_timestamp` containing many discrete values (many more than
the number of micro-partitions in the table), then a clustering key could be defined on the column by casting the
values to dates instead of timestamps (e.g. `to_date(c_timestamp)`). This would reduce the cardinality to the
total number of days, which typically produces much better pruning results.

As another example, you can truncate a number to fewer significant digits by using the `TRUNC` functions and a
negative value for the scale (e.g. `TRUNC(123456789, -5)`).

Tip

If you are defining a multi-column clustering key for a table, the order in which the columns are specified in
the `CLUSTER BY` clause is important. As a general rule, Snowflake recommends ordering the columns from
lowest cardinality to highest cardinality. Putting a higher cardinality column before a lower
cardinality column will generally reduce the effectiveness of clustering on the latter column.

Tip

When clustering on a text field, the cluster key metadata tracks only the first several bytes (typically 5 or 6 bytes).
Note that for multi-byte character sets, this can be fewer than 5 characters.

In some cases, clustering on columns used in `GROUP BY` or `ORDER BY` clauses can be helpful. However, clustering
on these columns is usually less helpful than clustering on columns that are heavily used in filter or `JOIN`
operations. If you have some columns that are heavily used in filter/join operations and different columns that are
used in `ORDER BY` or `GROUP BY` operations, then favor the columns used in the filter and join operations.

## Reclustering[¶](#reclustering "Link to this heading")

As DML operations (INSERT, UPDATE, DELETE, MERGE, COPY) are performed on a clustered table, the data in the table might become less clustered. Periodic/regular reclustering of the table is required to
maintain optimal clustering.

During reclustering, Snowflake uses the clustering key for a clustered table to reorganize the column data, so that related records are relocated to the same micro-partition. This DML operation deletes the
affected records and re-inserts them, grouped according to the clustering key.

Note

Reclustering in Snowflake is automatic; no maintenance is needed. For more details, see [Automatic Clustering](tables-auto-reclustering).

However, for certain accounts, manual reclustering has been deprecated, but is still allowed. For more details see [Manual Reclustering](tables-clustering-manual).

### Credit and Storage Impact of Reclustering[¶](#credit-and-storage-impact-of-reclustering "Link to this heading")

Similar to all DML operations in Snowflake, reclustering consumes credits. The number of credits consumed depends on the size of the table and the amount of data that needs to be reclustered.

Reclustering also results in storage costs. Each time data is reclustered, the rows are physically grouped based on the clustering key for the table, which results in Snowflake generating new
micro-partitions for the table. Adding even a small number of rows to a table can cause all micro-partitions that contain those values to be recreated.

This process can create significant data turnover because the original micro-partitions are marked as deleted, but retained in the system to enable Time Travel and Fail-safe. The original micro-partitions
are purged only after both the Time Travel retention period and the subsequent Fail-safe period have passed (i.e. minimum of 8 days and up to 97 days for extended Time Travel, if you are using Snowflake
Enterprise Edition (or higher)). This typically results in increased storage costs. For more information, see [Snowflake Time Travel & Fail-safe](data-availability).

Important

Before defining a clustering key for a table, you should consider the associated credit and storage costs.

### Reclustering Example[¶](#reclustering-example "Link to this heading")

Building on the [clustering diagram](tables-clustering-micropartitions.html#label-data-clustering) from the previous topic, this diagram illustrates how reclustering a table can help reduce scanning of micro-partitions to improve
query performance:

![Logical table structures after reclustering](../_images/tables-clustered2.png)

* To start, table `t1` is naturally clustered by `date` across micro-partitions 1-4.
* The query (in the diagram) requires scanning micro-partitions 1, 2, and 3.
* `date` and `type` are defined as the clustering key. When the table is reclustered, new micro-partitions (5-8) are created.
* After reclustering, the same query only scans micro-partition 5.

In addition, after reclustering:

* Micro-partition 5 has reached a *constant state* (i.e. it cannot be improved by reclustering) and is therefore excluded when computing depth and overlap for future maintenance. In a well-clustered
  large table, most micro-partitions will fall into this category.
* The original micro-partitions (1-4) are marked as deleted, but are not purged from the system; they are retained for [Time Travel and Fail-safe](data-availability).

Note

This example illustrates the impact of reclustering on an extremely small scale. Extrapolated to a very large table (i.e. consisting of millions of micro-partitions or more), reclustering can have a
significant impact on scanning and, therefore, query performance.

## Defining Clustered Tables[¶](#defining-clustered-tables "Link to this heading")

### Calculating the Clustering Information for a Table[¶](#calculating-the-clustering-information-for-a-table "Link to this heading")

Use the system function, [SYSTEM$CLUSTERING\_INFORMATION](../sql-reference/functions/system_clustering_information), to calculate clustering details, including clustering depth, for a given table. This function can be run on
any columns on any table, regardless of whether the table has an explicit clustering key:

* If a table has an explicit clustering key, the function doesn’t require any input arguments other than the name of the table.
* If a table doesn’t have an explicit clustering key (or a table has a clustering key, but you want to calculate the ratio on other columns in the table), the function takes the desired column(s) as an
  additional input argument.

### Defining a Clustering Key for a Table[¶](#defining-a-clustering-key-for-a-table "Link to this heading")

A clustering key can be defined when a table is created by appending a `CLUSTER BY` clause to [CREATE TABLE](../sql-reference/sql/create-table):

```
CREATE TABLE <name> ... CLUSTER BY ( <expr1> [ , <expr2> ... ] )
```

Copy

Where each clustering key consists of one or more table columns/expressions, which can be of any data type, except
GEOGRAPHY, VARIANT, OBJECT, or ARRAY. A clustering key can contain any of the following:

* Base columns.
* Expressions on base columns.
* Expressions on paths in VARIANT columns.

For example:

> ```
> -- cluster by base columns
> CREATE OR REPLACE TABLE t1 (c1 DATE, c2 STRING, c3 NUMBER) CLUSTER BY (c1, c2);
>
> SHOW TABLES LIKE 't1';
>
> +-------------------------------+------+---------------+-------------+-------+---------+----------------+------+-------+----------+----------------+----------------------+
> | created_on                    | name | database_name | schema_name | kind  | comment | cluster_by     | rows | bytes | owner    | retention_time | automatic_clustering |
> |-------------------------------+------+---------------+-------------+-------+---------+----------------+------+-------+----------+----------------+----------------------|
> | 2019-06-20 12:06:07.517 -0700 | T1   | TESTDB        | PUBLIC      | TABLE |         | LINEAR(C1, C2) |    0 |     0 | SYSADMIN | 1              | ON                   |
> +-------------------------------+------+---------------+-------------+-------+---------+----------------+------+-------+----------+----------------+----------------------+
>
> -- cluster by expressions
> CREATE OR REPLACE TABLE t2 (c1 timestamp, c2 STRING, c3 NUMBER) CLUSTER BY (TO_DATE(C1), substring(c2, 0, 10));
>
> SHOW TABLES LIKE 't2';
>
> +-------------------------------+------+---------------+-------------+-------+---------+------------------------------------------------+------+-------+----------+----------------+----------------------+
> | created_on                    | name | database_name | schema_name | kind  | comment | cluster_by                                     | rows | bytes | owner    | retention_time | automatic_clustering |
> |-------------------------------+------+---------------+-------------+-------+---------+------------------------------------------------+------+-------+----------+----------------+----------------------|
> | 2019-06-20 12:07:51.307 -0700 | T2   | TESTDB        | PUBLIC      | TABLE |         | LINEAR(CAST(C1 AS DATE), SUBSTRING(C2, 0, 10)) |    0 |     0 | SYSADMIN | 1              | ON                   |
> +-------------------------------+------+---------------+-------------+-------+---------+------------------------------------------------+------+-------+----------+----------------+----------------------+
>
> -- cluster by paths in variant columns
> CREATE OR REPLACE TABLE T3 (t timestamp, v variant) cluster by (v:"Data":id::number);
>
> SHOW TABLES LIKE 'T3';
>
> +-------------------------------+------+---------------+-------------+-------+---------+-------------------------------------------+------+-------+----------+----------------+----------------------+
> | created_on                    | name | database_name | schema_name | kind  | comment | cluster_by                                | rows | bytes | owner    | retention_time | automatic_clustering |
> |-------------------------------+------+---------------+-------------+-------+---------+-------------------------------------------+------+-------+----------+----------------+----------------------|
> | 2019-06-20 16:30:11.330 -0700 | T3   | TESTDB        | PUBLIC      | TABLE |         | LINEAR(TO_NUMBER(GET_PATH(V, 'Data.id'))) |    0 |     0 | SYSADMIN | 1              | ON                   |
> +-------------------------------+------+---------------+-------------+-------+---------+-------------------------------------------+------+-------+----------+----------------+----------------------+
> ```
>
> Copy

#### Important Usage Notes[¶](#important-usage-notes "Link to this heading")

* For each VARCHAR column, the current implementation of clustering uses only the first 5 bytes.

  If the first N characters are the same for every row, or do not provide sufficient cardinality, then consider clustering on a
  substring that starts after the characters that are identical, and that has optimal cardinality. (For more information about
  optimal cardinality, see [Strategies for Selecting Clustering Keys](#label-clustering-keys-strategies).) For example:

  > ```
  > create or replace table t3 (vc varchar) cluster by (SUBSTRING(vc, 5, 5));
  > ```
  >
  > Copy
* If you define two or more columns/expressions as the clustering key for a table, the order has an impact on how the data is clustered in micro-partitions.

  For more details, see [Strategies for Selecting Clustering Keys](#strategies-for-selecting-clustering-keys) (in this topic).
* An existing clustering key is copied when a table is created using CREATE TABLE … CLONE. However, Automatic Clustering is
  [suspended for the cloned table](object-clone.html#label-cloning-and-clustering-keys) and must be resumed.
* An existing clustering key is not supported when a table is created using CREATE TABLE … AS SELECT; however, you can define a clustering key after the table is created.
* Defining a clustering key directly on top of VARIANT columns is not supported; however, you can specify a VARIANT column in a clustering key if you provide an expression consisting of
  the path and the target type.

### Changing the Clustering Key for a Table[¶](#changing-the-clustering-key-for-a-table "Link to this heading")

At any time, you can add a clustering key to an existing table or change the existing clustering key for a table using [ALTER TABLE](../sql-reference/sql/alter-table):

```
ALTER TABLE <name> CLUSTER BY ( <expr1> [ , <expr2> ... ] )
```

Copy

For example:

> ```
> -- cluster by base columns
> ALTER TABLE t1 CLUSTER BY (c1, c3);
>
> SHOW TABLES LIKE 't1';
>
> +-------------------------------+------+---------------+-------------+-------+---------+----------------+------+-------+----------+----------------+----------------------+
> | created_on                    | name | database_name | schema_name | kind  | comment | cluster_by     | rows | bytes | owner    | retention_time | automatic_clustering |
> |-------------------------------+------+---------------+-------------+-------+---------+----------------+------+-------+----------+----------------+----------------------|
> | 2019-06-20 12:06:07.517 -0700 | T1   | TESTDB        | PUBLIC      | TABLE |         | LINEAR(C1, C3) |    0 |     0 | SYSADMIN | 1              | ON                   |
> +-------------------------------+------+---------------+-------------+-------+---------+----------------+------+-------+----------+----------------+----------------------+
>
> -- cluster by expressions
> ALTER TABLE T2 CLUSTER BY (SUBSTRING(C2, 5, 15), TO_DATE(C1));
>
> SHOW TABLES LIKE 't2';
>
> +-------------------------------+------+---------------+-------------+-------+---------+------------------------------------------------+------+-------+----------+----------------+----------------------+
> | created_on                    | name | database_name | schema_name | kind  | comment | cluster_by                                     | rows | bytes | owner    | retention_time | automatic_clustering |
> |-------------------------------+------+---------------+-------------+-------+---------+------------------------------------------------+------+-------+----------+----------------+----------------------|
> | 2019-06-20 12:07:51.307 -0700 | T2   | TESTDB        | PUBLIC      | TABLE |         | LINEAR(SUBSTRING(C2, 5, 15), CAST(C1 AS DATE)) |    0 |     0 | SYSADMIN | 1              | ON                   |
> +-------------------------------+------+---------------+-------------+-------+---------+------------------------------------------------+------+-------+----------+----------------+----------------------+
>
> -- cluster by paths in variant columns
> ALTER TABLE T3 CLUSTER BY (v:"Data":name::string, v:"Data":id::number);
>
> SHOW TABLES LIKE 'T3';
>
> +-------------------------------+------+---------------+-------------+-------+---------+------------------------------------------------------------------------------+------+-------+----------+----------------+----------------------+
> | created_on                    | name | database_name | schema_name | kind  | comment | cluster_by                                                                   | rows | bytes | owner    | retention_time | automatic_clustering |
> |-------------------------------+------+---------------+-------------+-------+---------+------------------------------------------------------------------------------+------+-------+----------+----------------+----------------------|
> | 2019-06-20 16:30:11.330 -0700 | T3   | TESTDB        | PUBLIC      | TABLE |         | LINEAR(TO_CHAR(GET_PATH(V, 'Data.name')), TO_NUMBER(GET_PATH(V, 'Data.id'))) |    0 |     0 | SYSADMIN | 1              | ON                   |
> +-------------------------------+------+---------------+-------------+-------+---------+------------------------------------------------------------------------------+------+-------+----------+----------------+----------------------+
> ```
>
> Copy

#### Important Usage Notes[¶](#id1 "Link to this heading")

* When adding a clustering key to a table already populated with data, not all expressions are allowed to be specified in the key. You can check whether a specific function is supported using
  [SHOW FUNCTIONS](../sql-reference/sql/show-functions):

  > `show functions like 'function_name';`

  The output includes a column, `valid_for_clustering`, at the end of the output. This column displays whether the function can be used in a clustering key for a populated table.
* Changing the clustering key for a table does not affect existing records in the table until the table has been reclustered by Snowflake.

### Dropping the Clustering Keys for a Table[¶](#dropping-the-clustering-keys-for-a-table "Link to this heading")

At any time, you can drop the clustering key for a table using [ALTER TABLE](../sql-reference/sql/alter-table):

```
ALTER TABLE <name> DROP CLUSTERING KEY
```

Copy

For example:

> ```
> ALTER TABLE t1 DROP CLUSTERING KEY;
>
> SHOW TABLES LIKE 't1';
>
> +-------------------------------+------+---------------+-------------+-------+---------+------------+------+-------+----------+----------------+----------------------+
> | created_on                    | name | database_name | schema_name | kind  | comment | cluster_by | rows | bytes | owner    | retention_time | automatic_clustering |
> |-------------------------------+------+---------------+-------------+-------+---------+------------+------+-------+----------+----------------+----------------------|
> | 2019-06-20 12:06:07.517 -0700 | T1   | TESTDB        | PUBLIC      | TABLE |         |            |    0 |     0 | SYSADMIN | 1              | OFF                  |
> +-------------------------------+------+---------------+-------------+-------+---------+------------+------+-------+----------+----------------+----------------------+
> ```
>
> Copy

Was this page helpful?

YesNo

[Visit Snowflake](https://www.snowflake.com)

[Join the conversation](https://community.snowflake.com/s/)

[Develop with Snowflake](https://developers.snowflake.com)

[Share your feedback](/feedback)

[Read the latest on our blog](https://www.snowflake.com/blog/)

[Get your own certification](https://learn.snowflake.com)

[Privacy Notice](https://www.snowflake.com/privacy-policy/)[Site Terms](https://www.snowflake.com/legal/snowflake-site-terms/)Cookies Settings© 2026 Snowflake, Inc. All Rights Reserved.

On this page

1. [What is a Clustering Key?](#what-is-a-clustering-key)
2. [Benefits of Defining Clustering Keys (for Very Large Tables)](#benefits-of-defining-clustering-keys-for-very-large-tables)
3. [Considerations for Choosing Clustering for a Table](#considerations-for-choosing-clustering-for-a-table)
4. [Strategies for Selecting Clustering Keys](#strategies-for-selecting-clustering-keys)
5. [Reclustering](#reclustering)
6. [Defining Clustered Tables](#defining-clustered-tables)