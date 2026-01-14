---
description: Hive SQL
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/hive/ddls/tables
title: SnowConvert AI - Hive - CREATE TABLE | Snowflake Documentation
---

## Description[¶](#description)

Creates a new table in the current database. You define a list of columns, which each hold data of a
distinct type. The owner of the table is the issuer of the CREATE TABLE command.

For more information, please refer to
[`CREATE TABLE`](https://spark.apache.org/docs/3.5.3/sql-ref-syntax-ddl-create-table.html)
documentation.

## Grammar Syntax [¶](#grammar-syntax)

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

## IF NOT EXISTS [¶](#if-not-exists)

## Description[¶](#id1)

> Ensures the table is created only if it does not already exist, preventing duplication and errors
> in your SQL script.

Hint

This syntax is fully supported in Snowflake.

## Applies to[¶](#applies-to)

- Hive
- Spark
- Databricks

## Grammar Syntax[¶](#id2)

```
IF NOT EXISTS
```

## Sample Source Patterns[¶](#sample-source-patterns)

## Input Code:[¶](#input-code)

```
CREATE TABLE IF NOT EXISTS table1 (
    col1 INTEGER
);
```

## Output Code:[¶](#output-code)

```
CREATE TABLE IF NOT EXISTS table1 (
    col1 INTEGER
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "sybase",  "convertedOn": "03/19/2024" }}';
```

## PARTITION BY[¶](#partition-by)

## Description[¶](#id3)

> Partitions are created on the table, based on the columns specified.

This syntax is not needed in Snowflake.

## Applies to[¶](#id4)

- Hive
- Spark
- Databricks

## Grammar Syntax[¶](#id5)

```
PARTITIONED BY ( { partition_column [ column_type ] } [, ...] )
```

## Sample Source Patterns[¶](#id6)

## Input Code:[¶](#id7)

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

## Output Code:[¶](#id8)

```
CREATE TABLE orders (
    order_id INT,
    customer_id INT,
    order_date DATE,
    total_amount DECIMAL(10, 2),
    order_status STRING
);
```

## CLUSTERED BY[¶](#clustered-by)

## Description[¶](#id9)

> Partitions created on the table will be bucketed into fixed buckets based on the column specified
> for bucketing.

This grammar is partially supported

## Applies to[¶](#id10)

- Hive
- Spark
- Databricks

## Grammar Syntax[¶](#id11)

```
CLUSTERED BY (column_name1 [ASC|DESC], ...)
[SORTED BY (sort_column1 [ASC|DESC], ...)]
INTO num_buckets BUCKETS
```

- The **`CLUSTERED BY`** clause, used for performance optimization, will be converted to
  **`CLUSTER BY`** in Snowflake. Performance may vary between the two architectures.
- The **`SORTED BY`** clause can be removed during migration, as Snowflake automatically handles
  data sorting within its micro-partitions.
- The **`INTO BUCKETS`** clause, a SparkSQL/Databrick specific partitioning setting, should be
  entirely eliminated, as it’s not applicable in Snowflake.

## Sample Source Patterns[¶](#id12)

## Input Code:[¶](#id13)

```
CREATE TABLE table_name (
column1 data_type, column2 data_type, ... ) USING format CLUSTERED BY (bucketing_column1) SORTED BY (sorting_column1 DESC, sorting_column2 ASC) INTO 10 BUCKETS;
```

## Output Code:[¶](#id14)

```
CREATE TABLE table_name ( column1 data_type, column2 data_type, ... ) USING format
CLUSTER BY (bucketing_column1);
```

## ROW FORMAT[¶](#row-format)

## Description[¶](#id15)

> Specifies the row format for input and output.

This grammar is not supported in Snowflake

## Applies to[¶](#id16)

- Hive
- Spark
- Databricks

## Grammar Syntax[¶](#id17)

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

## Sample Source Patterns[¶](#id18)

## Input Code:[¶](#id19)

```
CREATE TABLE parquet_table ( id INT, data STRING )  STORED AS TEXTFILE LOCATION '/mnt/delimited/target' ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' ESCAPED BY '\\' COLLECTION ITEMS TERMINATED BY ';' MAP KEYS TERMINATED BY ':' LINES TERMINATED BY '\n' NULL DEFINED AS 'NULL_VALUE';
```

## Output Code:[¶](#id20)

```
CREATE TABLE delimited_like_delta LIKE source_delta_table STORED AS TEXTFILE LOCATION '/mnt/delimited/target'
!!!RESOLVE EWI!!! /*** SSC-EWI-HV0002 - THE ROW FORMAT CLAUSE IS NOT SUPPORTED IN SNOWFLAKE ***/!!! ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' ESCAPED BY '\\' COLLECTION ITEMS TERMINATED BY ';' MAP KEYS TERMINATED BY ':' LINES TERMINATED BY '\n' NULL DEFINED AS 'NULL_VALUE';
```

## STORED AS[¶](#stored-as)

## Description[¶](#id21)

> File format for table storage.

This grammar is not supported in Snowflake

## Applies to[¶](#id22)

- Hive
- Spark
- Databricks
