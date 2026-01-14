---
description: Hive SQL
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/hive/ddls/create-external-table
title: SnowConvert AI - Hive - CREATE EXTERNAL TABLE | Snowflake Documentation
---

## Description[¶](#description)

> External Tables defines a new table using a Data Source.
> ([Spark SQL Language Reference CREATE DATASOURCE TABLE](https://spark.apache.org/docs/latest/sql-ref-syntax-ddl-create-table-datasource.html))

```
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
```

The CREATE EXTERNAL TABLE statement from Spark/Databricks will be transformed to a CREATE EXTERNAL
TABLE statement from
[Snowflake](https://docs.snowflake.com/en/sql-reference/sql/create-external-table); however, this
transformation requires user intervention.

In order to complete the transformation performed by SnowConvert AI, it is necessary to define a
[Storage Integration](https://docs.snowflake.com/en/sql-reference/sql/create-storage-integration),
an [External Stage](https://docs.snowflake.com/en/sql-reference/sql/create-stage), and (optionally)
a
[Notification Integration](https://docs.snowflake.com/en/sql-reference/sql/create-notification-integration)
that have access to the external source where files are located. Please refer to the following
guides on how to set up the connection for each provider:

- [For external tables referencing Amazon S3](https://docs.snowflake.com/en/user-guide/tables-external-s3)
- [For external tables referencing Google Cloud Storage](https://docs.snowflake.com/en/user-guide/tables-external-gcs)
- [For external tables referencing Azure Blob Storage](https://docs.snowflake.com/en/user-guide/tables-external-azure)

Important considerations for the transformations shown on this page:

- The @EXTERNAL_STAGE placeholder must be replaced with the external stage created after following
  the previous guide.
- It is assumed that the external stage will point to the root of the bucket. This is important to
  consider because the PATTERN clause generated for each table specifies the file/folder paths
  starting at the base of the bucket, defining the external stage pointing to a different location
  in the bucket might produce undesired behavior.
- The `AUTO_REFRESH = FALSE` clause is generated to avoid errors. Please note that automatic refresh
  of external table metadata is only valid if your Snowflake account cloud provider and the bucket
  provider are the same, and a Notification Integration was created.

## Sample Source Patterns[¶](#sample-source-patterns)

### Create External Table with explicit column list[¶](#create-external-table-with-explicit-column-list)

When the column list is provided, SnowConvert AI will automatically generate the AS expression
column options for each column in order to extract the file values.

#### Input Code:[¶](#input-code)

```
CREATE EXTERNAL TABLE IF NOT EXISTS external_table
(
  order_id int,
  date string,
  client_name string,
  total float
)
USING AVRO
LOCATION 'gs://sc_external_table_bucket/folder_with_avro/orders.avro';
```

#### Output Code:[¶](#output-code)

```
CREATE EXTERNAL TABLE IF NOT EXISTS external_table
(
  order_id int AS CAST(GET_IGNORE_CASE($1, 'order_id') AS int),
  date string AS CAST(GET_IGNORE_CASE($1, 'date') AS string),
  client_name string AS CAST(GET_IGNORE_CASE($1, 'client_name') AS string),
  total float AS CAST(GET_IGNORE_CASE($1, 'total') AS float)
)
!!!RESOLVE EWI!!! /*** SSC-EWI-0032 - EXTERNAL TABLE REQUIRES AN EXTERNAL STAGE TO ACCESS gs:, DEFINE AND REPLACE THE EXTERNAL_STAGE PLACEHOLDER ***/!!!
LOCATION = @EXTERNAL_STAGE
AUTO_REFRESH = false
FILE_FORMAT = (TYPE = AVRO)
PATTERN = '/sc_external_table_bucket/folder_with_avro/orders.avro'
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "spark",  "convertedOn": "06/18/2025",  "domain": "no-domain-provided" }}';
```

### CREATE EXTERNAL TABLE without an explicit column list [¶](#create-external-table-without-an-explicit-column-list)

When the column list is not provided, BigQuery automatically detects the schema of the columns from
the file structure. To replicate this behavior, SnowConvert AI will generate a USING TEMPLATE clause
that makes use of the
[INFER_SCHEMA](https://docs.snowflake.com/en/sql-reference/functions/infer_schema) function to
generate the column definitions.

Since the INFER_SCHEMA function requires a file format to work, SnowConvert AI will generate a
temporary file format for this purpose. This file format is only required when running the CREATE
EXTERNAL TABLE statement, and it will be automatically dropped when the session ends.

#### Input Code:[¶](#id1)

```
CREATE EXTERNAL TABLE IF NOT EXISTS external_table_No_Columns
using AVRO
LOCATION 'gs://sc_external_table_bucket/folder_with_avro/orders.avro';
```

#### Output Code:[¶](#id2)

```
CREATE OR REPLACE TEMPORARY FILE FORMAT SC_HIVE_FORMAT_ORDERS_NO_COLUMNS_FORMAT
TYPE = AVRO;
CREATE EXTERNAL TABLE IF NOT EXISTS hive_format_orders_No_Columns USING TEMPLATE (
SELECT
  ARRAY_AGG(OBJECT_CONSTRUCT('COLUMN_NAME', COLUMN_NAME, 'TYPE', TYPE, 'NULLABLE', NULLABLE, 'EXPRESSION', EXPRESSION))
FROM
  --** SSC-FDM-0035 - THE INFER_SCHEMA FUNCTION REQUIRES A FILE PATH WITHOUT WILDCARDS TO GENERATE THE TABLE TEMPLATE, REPLACE THE FILE_PATH PLACEHOLDER WITH IT **
  TABLE(INFER_SCHEMA(LOCATION => '@EXTERNAL_STAGE/FILE_PATH', FILE_FORMAT => 'SC_HIVE_FORMAT_ORDERS_NO_COLUMNS_FORMAT'))
)
!!!RESOLVE EWI!!! /*** SSC-EWI-0032 - EXTERNAL TABLE REQUIRES AN EXTERNAL STAGE TO ACCESS gs:, DEFINE AND REPLACE THE EXTERNAL_STAGE PLACEHOLDER ***/!!!
LOCATION = @EXTERNAL_STAGE
AUTO_REFRESH = false
FILE_FORMAT = (TYPE = AVRO)
PATTERN = '/sc_external_table_bucket/folder_with_avro/orders.avro'
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "spark",  "convertedOn": "06/18/2025",  "domain": "no-domain-provided" }}';
```

### CREATE EXTERNAL TABLE using Hive format[¶](#create-external-table-using-hive-format)

The creation of External Tables using
[Hive Format](https://spark.apache.org/docs/latest/sql-ref-syntax-ddl-create-table-hiveformat.html)
is also supported. They will have an FDM added informing the user that inserting into those tables
is not supported.

#### Input Code:[¶](#id3)

```
CREATE EXTERNAL TABLE IF NOT EXISTS External_table_hive_format
(
  order_id int,
  date string,
  client_name string,
  total float
)
stored as AVRO
LOCATION 'gs://sc_external_table_bucket/folder_with_avro/orders.avro';
```

#### Output Code:[¶](#id4)

```
--** SSC-FDM-HV0001 - INSERTING VALUES INTO AN EXTERNAL TABLE IS NOT SUPPORTED IN SNOWFLAKE **
CREATE EXTERNAL TABLE IF NOT EXISTS hive_format_orders_Andres
(
  order_id int AS CAST(GET_IGNORE_CASE($1, 'order_id') AS int),
  date string AS CAST(GET_IGNORE_CASE($1, 'date') AS string),
  client_name string AS CAST(GET_IGNORE_CASE($1, 'client_name') AS string),
  total float AS CAST(GET_IGNORE_CASE($1, 'total') AS float)
)
!!!RESOLVE EWI!!! /*** SSC-EWI-0032 - EXTERNAL TABLE REQUIRES AN EXTERNAL STAGE TO ACCESS gs:, DEFINE AND REPLACE THE EXTERNAL_STAGE PLACEHOLDER ***/!!!
LOCATION = @EXTERNAL_STAGE
AUTO_REFRESH = false
FILE_FORMAT = (TYPE = AVRO)
PATTERN = '/sc_external_table_bucket/folder_with_avro/orders.avro'
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "spark",  "convertedOn": "06/18/2025",  "domain": "no-domain-provided" }}';
```

## Known Issues[¶](#known-issues)

**1. External tables with unsupported file formats**

Snowflake supports the following Spark formats:

- CSV
- PARQUET
- ORC
- XML
- JSON
- AVRO

Other formats will be marked as not supported.

**2. Unsupported table options**

Some table options are not supported by SnowConvert AI and are marked with an EWI.

## Input Code:[¶](#id5)

```
CREATE EXTERNAL TABLE IF NOT EXISTS hive_format_orders_Andres
(
  order_id int,
  date string,
  client_name string,
  total float
)
using AVRO
LOCATION 'gs://sc_external_table_bucket/folder_with_avro/orders.avro'
Tblproperties (
    'unsupported_table_option' = 'value'
);
```

## Output Code:[¶](#id6)

```
CREATE EXTERNAL TABLE IF NOT EXISTS hive_format_orders_Andres
(
  order_id int AS CAST(GET_IGNORE_CASE($1, 'order_id') AS int),
  date string AS CAST(GET_IGNORE_CASE($1, 'date') AS string),
  client_name string AS CAST(GET_IGNORE_CASE($1, 'client_name') AS string),
  total float AS CAST(GET_IGNORE_CASE($1, 'total') AS float)
)
    !!!RESOLVE EWI!!! /*** SSC-EWI-0032 - EXTERNAL TABLE REQUIRES AN EXTERNAL STAGE TO ACCESS gs:, DEFINE AND REPLACE THE EXTERNAL_STAGE PLACEHOLDER ***/!!!
    LOCATION = @EXTERNAL_STAGE
    AUTO_REFRESH = false
    PATTERN = '/sc_external_table_bucket/folder_with_avro/orders.avro'
    FILE_FORMAT = (TYPE = AVRO)
    !!!RESOLVE EWI!!! /*** SSC-EWI-0016 - SNOWFLAKE DOES NOT SUPPORT THE OPTIONS: 'UNSUPPORTED_TABLE_OPTION'. ***/!!!
    TBLPROPERTIES (
  'unsupported_table_option' = 'value'
    )
    COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "spark",  "convertedOn": "06/19/2025",  "domain": "no-domain-provided" }}';
```

## Related EWIs [¶](#related-ewis)

1. [SSC-EWI-0029](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0029):
   External table data format not supported in Snowflake
2. [SSC-EWI-0032](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0032):
   External table requires an external stage to access an external location, define and replace the
   EXTERNAL_STAGE placeholder
3. [SSC-FDM-0034](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0034):
   The INFER_SCHEMA function requires a file path without wildcards to generate the table template,
   replace the FILE_PATH placeholder with it
4. [SSC-EWI-0016](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0016):
   Snowflake does not support the options clause.
5. [SSC-FDM-HV0001](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/hiveFDM.html#ssc-fdm-hv0001):
   Inserting values into an external table is not supported in Snowflake.
