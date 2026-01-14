---
description: 1. Unsupported table options
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/bigquery/bigquery-create-table
title: SnowConvert AI - BigQuery - CREATE TABLE | Snowflake Documentation
---

## Grammar syntax[¶](#grammar-syntax)

```
CREATE [ OR REPLACE ] [ TEMP | TEMPORARY ] TABLE [ IF NOT EXISTS ]
table_name
[(
  column | constraint_definition[, ...]
)]
[DEFAULT COLLATE collate_specification]
[PARTITION BY partition_expression]
[CLUSTER BY clustering_column_list]
[OPTIONS(table_option_list)]
[AS query_statement]
```

### Sample Source Patterns[¶](#sample-source-patterns)

#### DEFAULT COLLATE[¶](#default-collate)

##### BigQuery[¶](#bigquery)

```
CREATE TABLE table1 (
    col1 STRING
)
DEFAULT COLLATE 'und:ci';
```

##### Snowflake[¶](#snowflake)

```
CREATE TABLE table1 (
    col1 STRING
)
DEFAULT_DDL_COLLATION='und-ci';
```

#### Labels table option[¶](#labels-table-option)

##### BigQuery[¶](#id1)

```
CREATE TABLE table1
(
  col1 INT,
  col2 DATE
)
OPTIONS(
  labels=[("org_unit", "development")]
);
```

##### Snowflake[¶](#id2)

```
CREATE TAG IF NOT EXISTS "org_unit";

CREATE TABLE table1
(
  col1 INT,
  col2 DATE
)
WITH TAG( "org_unit" = "development" )
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "bigquery",  "convertedOn": "04/09/2025",  "domain": "test" }}'
;
```

#### Description table option[¶](#description-table-option)

##### BigQuery[¶](#id3)

```
CREATE TABLE table1
(
  col1 INT,
  col2 DATE
)
OPTIONS(
  description = 'My table comment'
);
```

##### Snowflake[¶](#id4)

```
CREATE TABLE table1
(
  col1 INT,
  col2 DATE
)
COMMENT = '{ "description": "My table comment", "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "bigquery",  "convertedOn": "04/09/2025",  "domain": "test" }}'
;
```

#### Description table option[¶](#id5)

##### BigQuery[¶](#id6)

```
CREATE TABLE table1
(
  col1 INT,
  col2 DATE
)
OPTIONS(
  friendly_name = 'Some_table'
);
```

##### Snowflake[¶](#id7)

```
CREATE TABLE table1
(
  col1 INT,
  col2 DATE
)
COMMENT = '{ "friendly_name": "Some_table", "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "bigquery",  "convertedOn": "04/09/2025",  "domain": "test" }}'
;
```

### Known Issues[¶](#known-issues)

**1. Unsupported table options**

Not all table options are supported in Snowflake, when an unsupported table option is encountered in
the OPTIONS clause, an EWI will be generated to warn about this.

#### BigQuery[¶](#id8)

```
 CREATE TABLE table1
(
  col1 INT,
  col2 DATE
)
OPTIONS(
  expiration_timestamp=TIMESTAMP "2025-01-01 00:00:00 UTC",
  partition_expiration_days=1,
  description="a table that expires in 2025, with each partition living for 24 hours",
  labels=[("org_unit", "development")]
);
```

#### Snowflake[¶](#id9)

```
 CREATE TAG IF NOT EXISTS "org_unit";

CREATE TABLE table1
(
  col1 INT,
  col2 DATE
)
WITH TAG( "org_unit" = "development" )
!!!RESOLVE EWI!!! /*** SSC-EWI-BQ0001 - SNOWFLAKE DOES NOT SUPPORT THE OPTIONS: EXPIRATION_TIMESTAMP, PARTITION_EXPIRATION_DAYS. ***/!!!
OPTIONS(
  expiration_timestamp=TIMESTAMP "2025-01-01 00:00:00 UTC",
  partition_expiration_days=1
)
COMMENT = '{ "description": "a table that expires in 2025, with each partition living for 24 hours", "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "bigquery",  "convertedOn": "04/09/2025",  "domain": "test" }}'
;
```

**2. Micro-partitioning is automatically managed by Snowflake**

Snowflake performs automatic partitioning of data. User defined partitioning is not supported.

##### BigQuery[¶](#id10)

```
 CREATE TABLE table1(
    transaction_id INT,
    transaction_date DATE
)
PARTITION BY transaction_date;
```

##### Snowflake[¶](#id11)

```
 CREATE TABLE table1 (
    transaction_id INT,
    transaction_date DATE
)
!!!RESOLVE EWI!!! /*** SSC-EWI-BQ0002 - MICRO-PARTITIONING IS AUTOMATICALLY PERFORMED ON ALL SNOWFLAKE TABLES. ***/!!!
PARTITION BY transaction_date;
```

## Related EWIs[¶](#related-ewis)

1. [SSC-EWI-BQ0001](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/bigqueryEWI.html#ssc-ewi-bq0001):
   Snowflake does not support the options clause.
2. [SSC-EWI-BQ0002](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/bigqueryEWI.html#ssc-ewi-bq0002):
   Micro-partitioning is automatically performed on all Snowflake tables.

## COLUMN DEFINITION[¶](#column-definition)

### Grammar syntax[¶](#id12)

```
 column :=
  column_name column_schema

column_schema :=
   {
     simple_type
     | STRUCT<field_list>
     | ARRAY<array_element_schema>
   }
   [PRIMARY KEY NOT ENFORCED | REFERENCES table_name(column_name) NOT ENFORCED]
   [DEFAULT default_expression]
   [NOT NULL]
   [OPTIONS(column_option_list)]

simple_type :=
  { data_type | STRING COLLATE collate_specification }

field_list :=
  field_name column_schema [, ...]

array_element_schema :=
  { simple_type | STRUCT<field_list> }
  [NOT NULL]
```

### Sample Source Patterns[¶](#id13)

#### Description option[¶](#description-option)

##### BigQuery[¶](#id14)

```
CREATE TABLE table1 (
  col1 VARCHAR(20) OPTIONS(description="A repeated STRING field")
);
```

##### Snowflake[¶](#id15)

```
CREATE TABLE table1 (
  col1 VARCHAR(20) COMMENT = 'A repeated STRING field'
);
```

#### COLLATE[¶](#collate)

##### BigQuery[¶](#id16)

```
CREATE TABLE table1 (
  col1 STRING COLLATE 'und:ci'
);
```

##### Snowflake[¶](#id17)

```
CREATE TABLE table1 (
  col1 STRING COLLATE 'und-ci'
);
```

### Known Issues[¶](#id18)

**1. Rounding mode not supported**

Snowflake does not support specifying a default rounding mode on columns.

#### BigQuery[¶](#id19)

```
CREATE TABLE table1 (
  col1 STRING OPTIONS(rounding_mode = "ROUND_HALF_EVEN")
);
```

#### Snowflake[¶](#id20)

```
CREATE TABLE table1 (
    col1 STRING
    !!!RESOLVE EWI!!! /*** SSC-EWI-BQ0001 - SNOWFLAKE DOES NOT SUPPORT THE OPTIONS: ROUNDING_MODE. ***/!!!
    OPTIONS(
        rounding_mode = "ROUND_HALF_EVEN"
    )
)
```

### Related EWIs[¶](#id21)

1. [SSC-EWI-BQ0001](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/bigqueryEWI.html#ssc-ewi-bq0001):
   Snowflake does not support the options clause.

## CREATE EXTERNAL TABLE[¶](#create-external-table)

### Description[¶](#description)

External tables let BigQuery query data that is stored outside of BigQuery storage.
([BigQuery SQL Language Reference CREATE EXTERNAL TABLE](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#create_external_table_statement))

Syntax

```
CREATE [ OR REPLACE ] EXTERNAL TABLE [ IF NOT EXISTS ] table_name
[(
  column_name column_schema,
  ...
)]
[WITH CONNECTION {connection_name | DEFAULT}]
[WITH PARTITION COLUMNS
  [(
      partition_column_name partition_column_type,
      ...
  )]
]
OPTIONS (
  external_table_option_list,
  ...
);
```

The CREATE EXTERNAL TABLE statement from BigQuery will be transformed to a CREATE EXTERNAL TABLE
statement from [Snowflake](https://docs.snowflake.com/en/sql-reference/sql/create-external-table),
however, this transformation requires user intervention.

In order to complete the transformation performed by SnowConvert AI, it is necessary to define a
[Storage Integration](https://docs.snowflake.com/en/sql-reference/sql/create-storage-integration), a
[External Stage](https://docs.snowflake.com/en/sql-reference/sql/create-stage) and (optional)
[Notification Integration](https://docs.snowflake.com/en/sql-reference/sql/create-notification-integration)
that have access to the external source were files are located. Please refer to the following guides
on how to set up the connection for each provider:

- [For external tables referencing Amazon S3](https://docs.snowflake.com/en/user-guide/tables-external-s3)
- [For external tables referencing Google Cloud Storage](https://docs.snowflake.com/en/user-guide/tables-external-gcs)
- [For external tables referencing Azure Blob Storage](https://docs.snowflake.com/en/user-guide/tables-external-azure)

Important considerations for the transformations shown in this page:

- The @EXTERNAL_STAGE placeholder must be replaced with the external stage created after following
  the previous guide.
- It is assumed that the external stage will point to the root of the bucket. This is important to
  consider because the PATTERN clause generated for each table specifies the file/folder paths
  starting at the base of the bucket, defining the external stage pointing to a different location
  in the bucket might produce undesired behavior.
- The `AUTO_REFRESH = FALSE` clause is generated to avoid errors, please note that automatic refresh
  of external table metadata is only valid if your Snowflake account cloud provider and the bucket
  provider are the same and a Notification Integration was created.

### Sample Source Patterns[¶](#id22)

#### CREATE EXTERNAL TABLE with explicit column list[¶](#create-external-table-with-explicit-column-list)

When the column list is provided, SnowConvert AI will automatically generate the AS expression
column options for each column in order to extract the file values.

##### BigQuery[¶](#id23)

```
 CREATE OR REPLACE EXTERNAL TABLE test.Employees_test
(
  Employee_id INTEGER,
  Name STRING,
  Mail STRING,
  Position STRING,
  Salary INTEGER
)
OPTIONS(
  FORMAT='CSV',
  SKIP_LEADING_ROWS=1,
  URIS=['gs://sc_external_table_bucket/folder_with_csv/Employees.csv']
);
```

##### Snowflake[¶](#id24)

```
 CREATE OR REPLACE EXTERNAL TABLE test.Employees_test
(
  Employee_id INTEGER AS CAST(GET_IGNORE_CASE($1, 'c1') AS INTEGER),
  Name STRING AS CAST(GET_IGNORE_CASE($1, 'c2') AS STRING),
  Mail STRING AS CAST(GET_IGNORE_CASE($1, 'c3') AS STRING),
  Position STRING AS CAST(GET_IGNORE_CASE($1, 'c4') AS STRING),
  Salary INTEGER AS CAST(GET_IGNORE_CASE($1, 'c5') AS INTEGER)
)
!!!RESOLVE EWI!!! /*** SSC-EWI-BQ0015 - EXTERNAL TABLE REQUIRES AN EXTERNAL STAGE TO ACCESS gs://sc_external_table_bucket, DEFINE AND REPLACE THE EXTERNAL_STAGE PLACEHOLDER ***/!!!
LOCATION = @EXTERNAL_STAGE
AUTO_REFRESH = false
PATTERN = 'folder_with_csv/Employees.csv'
FILE_FORMAT = (TYPE = CSV SKIP_HEADER =1);
```

#### CREATE EXTERNAL TABLE without explicit column list[¶](#create-external-table-without-explicit-column-list)

When the column list is not provided, BigQuery automatically detects the schema of the columns from
the file structure. To replicate this behavior, SnowConvert AI will generate a USING TEMPLATE clause
that makes use of the
[INFER_SCHEMA](https://docs.snowflake.com/en/sql-reference/functions/infer_schema) function to
generate the column definitions.

Since the INFER_SCHEMA function requires a file format to work, SnowConvert AI will generate a
temporary file format for this purpose, this file format is only required when running the CREATE
EXTERNAL TABLE statement and it will be automatically dropped when the session ends.

##### BigQuery[¶](#id25)

```
 CREATE OR REPLACE EXTERNAL TABLE test.my_external_table_json
OPTIONS(
  FORMAT='JSON',
  URIS=['gs://sc_external_table_bucket/folder_with_json/Cars.jsonl']
);
```

##### Snowflake[¶](#id26)

```
CREATE OR REPLACE TEMPORARY FILE FORMAT SC_TEST_MY_EXTERNAL_TABLE_JSON_FORMAT
TYPE = JSON;

CREATE OR REPLACE EXTERNAL TABLE test.my_external_table_json USING TEMPLATE (
SELECT
  ARRAY_AGG(OBJECT_CONSTRUCT('COLUMN_NAME', COLUMN_NAME, 'TYPE', TYPE, 'NULLABLE', NULLABLE, 'EXPRESSION', EXPRESSION))
FROM
  TABLE(INFER_SCHEMA(LOCATION => '@EXTERNAL_STAGE/folder_with_json/Cars.jsonl', FILE_FORMAT => 'SC_TEST_MY_EXTERNAL_TABLE_JSON_FORMAT'))
)
!!!RESOLVE EWI!!! /*** SSC-EWI-BQ0015 - EXTERNAL TABLE REQUIRES AN EXTERNAL STAGE TO ACCESS gs://sc_external_table_bucket, DEFINE AND REPLACE THE EXTERNAL_STAGE PLACEHOLDER ***/!!!
LOCATION = @EXTERNAL_STAGE
AUTO_REFRESH = false
PATTERN = 'folder_with_json/Cars.jsonl'
FILE_FORMAT = (TYPE = JSON);
```

#### CREATE EXTERNAL TABLE with multiple URIs[¶](#create-external-table-with-multiple-uris)

When multiple source URIs are specified, they will be joined in the regex of the PATTERN clause in
Snowflake, the wildcard `*` characters used will be transformed to its `.*` equivalent in Snowflake.

##### BigQuery[¶](#id27)

```
 CREATE OR REPLACE EXTERNAL TABLE test.multipleFilesTable
(
  Name STRING,
  Code STRING,
  Price NUMERIC,
  Expiration_date DATE
)

OPTIONS(
  format="CSV",
  skip_leading_rows = 1,
  uris=['gs://sc_external_table_bucket/folder_with_csv/Food.csv', 'gs://sc_external_table_bucket/folder_with_csv/other_products/*']
);
```

##### Snowflake[¶](#id28)

```
 CREATE OR REPLACE EXTERNAL TABLE test.multipleFilesTable
(
  Name STRING AS CAST(GET_IGNORE_CASE($1, 'c1') AS STRING),
  Code STRING AS CAST(GET_IGNORE_CASE($1, 'c2') AS STRING),
  Price NUMERIC AS CAST(GET_IGNORE_CASE($1, 'c3') AS NUMERIC),
  Expiration_date DATE AS CAST(GET_IGNORE_CASE($1, 'c4') AS DATE)
)
!!!RESOLVE EWI!!! /*** SSC-EWI-BQ0015 - EXTERNAL TABLE REQUIRES AN EXTERNAL STAGE TO ACCESS gs://sc_external_table_bucket, DEFINE AND REPLACE THE EXTERNAL_STAGE PLACEHOLDER ***/!!!
LOCATION = @EXTERNAL_STAGE
AUTO_REFRESH = false
PATTERN = 'folder_with_csv/Food.csv|folder_with_csv/other_products/.*'
FILE_FORMAT = (TYPE = CSV SKIP_HEADER = 1);
```

#### WITH CONNECTION clause[¶](#with-connection-clause)

The WITH CONNECTION clause is removed because the connection information is already provided to
Snowflake using the Storage Integration.

##### BigQuery[¶](#id29)

```
 CREATE EXTERNAL TABLE test.awsTable
  WITH CONNECTION `aws-us-east-1.s3-read-connection`
  OPTIONS (
    format="JSON",
    uris=["s3://s3-bucket/json_files/example.jsonl"]
);
```

##### Snowflake[¶](#id30)

```
CREATE OR REPLACE TEMPORARY FILE FORMAT SC_TEST_AWSTABLE_FORMAT
TYPE = JSON;

CREATE EXTERNAL TABLE test.awsTable USING TEMPLATE (
SELECT
  ARRAY_AGG(OBJECT_CONSTRUCT('COLUMN_NAME', COLUMN_NAME, 'TYPE', TYPE, 'NULLABLE', NULLABLE, 'EXPRESSION', EXPRESSION))
FROM
  TABLE(INFER_SCHEMA(LOCATION => '@EXTERNAL_STAGE/json_files/example.jsonl', FILE_FORMAT => 'SC_TEST_AWSTABLE_FORMAT'))
)
!!!RESOLVE EWI!!! /*** SSC-EWI-BQ0015 - EXTERNAL TABLE REQUIRES AN EXTERNAL STAGE TO ACCESS s3://s3-bucket, DEFINE AND REPLACE THE EXTERNAL_STAGE PLACEHOLDER ***/!!!
LOCATION = @EXTERNAL_STAGE
AUTO_REFRESH = false
PATTERN = 'json_files/example.jsonl'
FILE_FORMAT = (TYPE = JSON);
```

#### Supported table options[¶](#supported-table-options)

The following external table options are supported in Snowflake and transformed by SnowConvert AI:

- FORMAT
- ENCODING
- SKIP_LEADING_ROWS
- FIELD_DELIMITER
- COMPRESSION

##### BigQuery[¶](#id31)

```
CREATE OR REPLACE EXTERNAL TABLE test.songs_test
(
  Name STRING,
  Release_date INTEGER,
  Songs INT,
  Genre STRING
)
OPTIONS(
  FORMAT='CSV',
  ENCODING='UTF-8',
  SKIP_LEADING_ROWS=1,
  FIELD_DELIMITER='|',
  COMPRESSION='GZIP',
  URIS=['gs://sc_external_table_bucket/folder_with_csv/Albums.csv']
);
```

##### Snowflake[¶](#id32)

```
CREATE OR REPLACE EXTERNAL TABLE test.songs_test
(
  Name STRING AS CAST(GET_IGNORE_CASE($1, 'c1') AS STRING),
  Release_date INTEGER AS CAST(GET_IGNORE_CASE($1, 'c2') AS INTEGER),
  Songs INT AS CAST(GET_IGNORE_CASE($1, 'c3') AS INT),
  Genre STRING AS CAST(GET_IGNORE_CASE($1, 'c4') AS STRING)
)
!!!RESOLVE EWI!!! /*** SSC-EWI-BQ0015 - EXTERNAL TABLE REQUIRES AN EXTERNAL STAGE TO ACCESS gs://sc_external_table_bucket, DEFINE AND REPLACE THE EXTERNAL_STAGE PLACEHOLDER ***/!!!
LOCATION = @EXTERNAL_STAGE
AUTO_REFRESH = false
PATTERN = 'folder_with_csv/Albums.csv'
FILE_FORMAT = (TYPE = CSV
  ENCODING= 'UTF8' SKIP_HEADER =1
  FIELD_DELIMITER='|'
  COMPRESSION= GZIP);
```

### Known Issues[¶](#id33)

**1. CREATE EXTERNAL TABLE without explicit column list and CSV file format**

Currently, Snowflake external tables do not support parsing the header of CSV files. When a external
table with no explicit column list and CSV file format is found, SnowConvert AI will produce the
SKIP_HEADER file format option to avoid runtime errors, however, this will cause the table column
names to have the autogenerated names c1, c2, …, cN.

An FDM is generated to notify that the header can not be parsed and that manually renaming the
columns is necessary to preserve the names.

#### BigQuery[¶](#id34)

```
 CREATE OR REPLACE EXTERNAL TABLE test.my_external_table_csv
OPTIONS(
  FORMAT='CSV',
  URIS=['gs://sc_external_table_bucket/folder_with_csv/Employees.csv']
);
```

#### Snowflake[¶](#id35)

```
CREATE OR REPLACE TEMPORARY FILE FORMAT SC_TEST_MY_EXTERNAL_TABLE_CSV_FORMAT
TYPE = CSV
SKIP_HEADER = 1;

CREATE OR REPLACE EXTERNAL TABLE test.my_external_table_csv
--** SSC-FDM-BQ0005 - PARSING THE CSV HEADER IS NOT SUPPORTED IN EXTERNAL TABLES, COLUMNS MUST BE RENAMED TO MATCH THE ORIGINAL NAMES **
USING TEMPLATE (
SELECT
  ARRAY_AGG(OBJECT_CONSTRUCT('COLUMN_NAME', COLUMN_NAME, 'TYPE', TYPE, 'NULLABLE', NULLABLE, 'EXPRESSION', EXPRESSION))
FROM
  TABLE(INFER_SCHEMA(LOCATION => '@EXTERNAL_STAGE/folder_with_csv/Employees.csv', FILE_FORMAT => 'SC_TEST_MY_EXTERNAL_TABLE_CSV_FORMAT'))
)
!!!RESOLVE EWI!!! /*** SSC-EWI-BQ0015 - EXTERNAL TABLE REQUIRES AN EXTERNAL STAGE TO ACCESS gs://sc_external_table_bucket, DEFINE AND REPLACE THE EXTERNAL_STAGE PLACEHOLDER ***/!!!
LOCATION = @EXTERNAL_STAGE
AUTO_REFRESH = false
PATTERN = 'folder_with_csv/Employees.csv'
FILE_FORMAT = (TYPE = CSV SKIP_HEADER = 1);
```

**2. External tables referencing Google Drive sources**

Snowflake does not support reading data from files hosted in Google Drive, an FDM will be generated
to notify about this and request that the files are uploaded to the bucket and accessed through the
external stage.

The PATTERN clause will hold autogenerated placeholders FILE_PATH0, FILE_PATH1, …, FILE_PATHN that
should be replaced with the file/folder path after the files were moved to the external location.

##### BigQuery[¶](#id36)

```
 CREATE OR REPLACE EXTERNAL TABLE test.my_external_table_drive_test
OPTIONS(
  FORMAT='JSON',
  URIS=['https://drive.google.com/open?id=someFileId']
);
```

##### Snowflake[¶](#id37)

```
 CREATE OR REPLACE TEMPORARY FILE FORMAT SC_TEST_MY_EXTERNAL_TABLE_DRIVE_TEST_FORMAT
TYPE = JSON;

CREATE OR REPLACE EXTERNAL TABLE test.my_external_table_drive_test USING TEMPLATE (
SELECT
  ARRAY_AGG(OBJECT_CONSTRUCT('COLUMN_NAME', COLUMN_NAME, 'TYPE', TYPE, 'NULLABLE', NULLABLE, 'EXPRESSION', EXPRESSION))
FROM
  --** SSC-FDM-BQ0008 - THE INFER_SCHEMA FUNCTION REQUIRES A FILE PATH WITHOUT WILDCARDS TO GENERATE THE TABLE TEMPLATE, REPLACE THE FILE_PATH PLACEHOLDER WITH IT **
  TABLE(INFER_SCHEMA(LOCATION => '@EXTERNAL_STAGE/FILE_PATH', FILE_FORMAT => 'SC_TEST_MY_EXTERNAL_TABLE_DRIVE_TEST_FORMAT'))
)
!!!RESOLVE EWI!!! /*** SSC-EWI-BQ0015 - EXTERNAL TABLE REQUIRES AN EXTERNAL STAGE TO ACCESS A EXTERNAL LOCATION, DEFINE AND REPLACE THE EXTERNAL_STAGE PLACEHOLDER ***/!!!
LOCATION = @EXTERNAL_STAGE
AUTO_REFRESH = false
--** SSC-FDM-BQ0006 - READING FROM GOOGLE DRIVE IS NOT SUPPORTED IN SNOWFLAKE, UPLOAD THE FILES TO THE EXTERNAL LOCATION AND REPLACE THE FILE_PATH PLACEHOLDERS **
PATTERN = 'FILE_PATH0'
FILE_FORMAT = (TYPE = JSON);
```

**3. External tables with the GOOGLE_SHEETS file format**

Snowflake does not support Google Sheets as a file format, however, its structure is similar to CSV
files, which are supported by Snowflake.

When SnowConvert AI detects a external table using the GOOGLE_SHEETS format, it will produce a
external table with the CSV file format instead.

Since Google Sheets are stored in Google Drive, it would be necessary to upload the files as CSV to
the external location and specify the file paths in the PATTERN clause, just as mentioned in the
previous issue.

##### BigQuery[¶](#id38)

```
 CREATE OR REPLACE EXTERNAL TABLE test.spreadsheetTable
(
  Name STRING,
  Code INTEGER,
  Price INTEGER,
  Expiration_date DATE
)
OPTIONS(
  format="GOOGLE_SHEETS",
  skip_leading_rows = 1,
  uris=['https://docs.google.com/spreadsheets/d/someFileId/edit?usp=sharing']
);
```

##### Snowflake[¶](#id39)

```
 --** SSC-FDM-BQ0007 - READING FROM SPREADSHEETS IS NOT SUPPORTED IN SNOWFLAKE, USE THE CSV FILE TYPE INSTEAD **
CREATE OR REPLACE EXTERNAL TABLE test.spreadsheetTable
(
  Name STRING AS CAST(GET_IGNORE_CASE($1, 'c1') AS STRING),
  Code INTEGER AS CAST(GET_IGNORE_CASE($1, 'c2') AS INTEGER),
  Price INTEGER AS CAST(GET_IGNORE_CASE($1, 'c3') AS INTEGER),
  Expiration_date DATE AS CAST(GET_IGNORE_CASE($1, 'c4') AS DATE)
)
!!!RESOLVE EWI!!! /*** SSC-EWI-BQ0015 - EXTERNAL TABLE REQUIRES AN EXTERNAL STAGE TO ACCESS A EXTERNAL LOCATION, DEFINE AND REPLACE THE EXTERNAL_STAGE PLACEHOLDER ***/!!!
LOCATION = @EXTERNAL_STAGE
AUTO_REFRESH = false
--** SSC-FDM-BQ0006 - READING FROM GOOGLE DRIVE IS NOT SUPPORTED IN SNOWFLAKE, UPLOAD THE FILES TO THE EXTERNAL LOCATION AND REPLACE THE FILE_PATH PLACEHOLDERS **
PATTERN = 'FILE_PATH0'
FILE_FORMAT = (TYPE = CSV SKIP_HEADER = 1);
```

**4. External tables with unsupported file formats**

Snowflake supports the following BigQuery formats:

<!-- prettier-ignore -->
|BigQuery|Snowflake|
|---|---|
|AVRO|AVRO|
|CSV GOOGLE_SHEETS|CSV|
|NEWLINE_DELIMITED_JSON JSON|JSON|
|ORC|ORC|
|PARQUET|PARQUET|

Other formats will be marked as not supported.

##### BigQuery[¶](#id40)

```
 CREATE OR REPLACE EXTERNAL TABLE test.backup_restore_table
OPTIONS (
  format = 'DATASTORE_BACKUP',
  uris = ['gs://backup_bucket/backup_folder/*']
);
```

##### Snowflake[¶](#id41)

```
 !!!RESOLVE EWI!!! /*** SSC-EWI-BQ0013 - EXTERNAL TABLE DATA FORMAT NOT SUPPORTED IN SNOWFLAKE ***/!!!
CREATE OR REPLACE EXTERNAL TABLE test.backup_restore_table
OPTIONS (
  format = 'DATASTORE_BACKUP',
  uris = ['gs://backup_bucket/backup_folder/*']
);
```

**5. Hive partitioned external tables**

Snowflake does not support hive partitioned external tables, the WITH PARTITION COLUMNS clause will
be marked as not supported.

##### BigQuery[¶](#id42)

```
CREATE EXTERNAL TABLE test.CustomHivePartitionedTable
WITH PARTITION COLUMNS (
  field_1 STRING,
  field_2 INT64)
OPTIONS (
  uris = ['gs://sc_external_table_bucket/folder_with_parquet/*'],
  format = 'PARQUET',
  hive_partition_uri_prefix = 'gs://sc_external_table_bucket/folder_with_parquet',
  require_hive_partition_filter = false);
```

##### Snowflake[¶](#id43)

```
CREATE OR REPLACE TEMPORARY FILE FORMAT SC_TEST_CUSTOMHIVEPARTITIONEDTABLE_FORMAT
TYPE = PARQUET;

CREATE EXTERNAL TABLE test.CustomHivePartitionedTable USING TEMPLATE (
SELECT
  ARRAY_AGG(OBJECT_CONSTRUCT('COLUMN_NAME', COLUMN_NAME, 'TYPE', TYPE, 'NULLABLE', NULLABLE, 'EXPRESSION', EXPRESSION))
FROM
  --** SSC-FDM-BQ0008 - THE INFER_SCHEMA FUNCTION REQUIRES A FILE PATH WITHOUT WILDCARDS TO GENERATE THE TABLE TEMPLATE, REPLACE THE FILE_PATH PLACEHOLDER WITH IT **
  TABLE(INFER_SCHEMA(LOCATION => '@EXTERNAL_STAGE/FILE_PATH', FILE_FORMAT => 'SC_TEST_CUSTOMHIVEPARTITIONEDTABLE_FORMAT'))
)
!!!RESOLVE EWI!!! /*** SSC-EWI-BQ0015 - EXTERNAL TABLE REQUIRES AN EXTERNAL STAGE TO ACCESS gs://sc_external_table_bucket, DEFINE AND REPLACE THE EXTERNAL_STAGE PLACEHOLDER ***/!!!
LOCATION = @EXTERNAL_STAGE
AUTO_REFRESH = false
!!!RESOLVE EWI!!! /*** SSC-EWI-BQ0014 - HIVE PARTITIONED EXTERNAL TABLES ARE NOT SUPPORTED IN SNOWFLAKE ***/!!!
WITH PARTITION COLUMNS (
  field_1 STRING,
  field_2 INT64)
PATTERN = 'folder_with_parquet/.*'
FILE_FORMAT = (TYPE = PARQUET)
!!!RESOLVE EWI!!! /*** SSC-EWI-BQ0001 - SNOWFLAKE DOES NOT SUPPORT THE OPTIONS: HIVE_PARTITION_URI_PREFIX, REQUIRE_HIVE_PARTITION_FILTER. ***/!!!
OPTIONS(
  hive_partition_uri_prefix = 'gs://sc_external_table_bucket/folder_with_parquet',
  require_hive_partition_filter = false
);
```

**6. External table without columns list and no valid file URI for the INFER_SCHEMA function**

The INFER_SCHEMA function requires a LOCATION parameter that specifies the path to a file or folder
that will be used to construct the table columns, however, this path does not support regex, meaning
that the wildcard `*` character is not supported.

When the table has no columns, SnowConvert AI will check all URIS in order to find one that does not
use wildcards and use it in the INFER_SCHEMA function, when no URI meets such criteria an FDM and
FILE_PATH placeholder will be generated, the placeholder has to be replaced with the path of one of
the files referenced by the external table to generate the table columns.

##### BigQuery[¶](#id44)

```
CREATE OR REPLACE EXTERNAL TABLE test.my_external_table_json2
OPTIONS(
  FORMAT='JSON',
  URIS=['gs://sc_external_table_bucket/folder_with_json/*']
);
```

##### Snowflake[¶](#id45)

```
CREATE OR REPLACE TEMPORARY FILE FORMAT SC_TEST_MY_EXTERNAL_TABLE_JSON2_FORMAT
TYPE = JSON;

CREATE OR REPLACE EXTERNAL TABLE test.my_external_table_json2 USING TEMPLATE (
SELECT
  ARRAY_AGG(OBJECT_CONSTRUCT('COLUMN_NAME', COLUMN_NAME, 'TYPE', TYPE, 'NULLABLE', NULLABLE, 'EXPRESSION', EXPRESSION))
FROM
  --** SSC-FDM-BQ0008 - THE INFER_SCHEMA FUNCTION REQUIRES A FILE PATH WITHOUT WILDCARDS TO GENERATE THE TABLE TEMPLATE, REPLACE THE FILE_PATH PLACEHOLDER WITH IT **
  TABLE(INFER_SCHEMA(LOCATION => '@EXTERNAL_STAGE/FILE_PATH', FILE_FORMAT => 'SC_TEST_MY_EXTERNAL_TABLE_JSON2_FORMAT'))
)
!!!RESOLVE EWI!!! /*** SSC-EWI-BQ0015 - EXTERNAL TABLE REQUIRES AN EXTERNAL STAGE TO ACCESS gs://sc_external_table_bucket, DEFINE AND REPLACE THE EXTERNAL_STAGE PLACEHOLDER ***/!!!
LOCATION = @EXTERNAL_STAGE
AUTO_REFRESH = false
PATTERN = 'folder_with_json/.*'
FILE_FORMAT = (TYPE = JSON);
```

**7. Unsupported table options**

Any other table option not mentioned in the [Supported table options](#supported-table-options)
pattern will be marked as not supported.

##### BigQuery[¶](#id46)

```
CREATE OR REPLACE EXTERNAL TABLE dataset.CsvTable
(
  x INTEGER,
  y STRING
)
OPTIONS (
  format = 'CSV',
  uris = ['gs://bucket/example.csv'],
  field_delimiter = '|',
  max_bad_records = 5
);
```

##### Snowflake[¶](#id47)

```
CREATE OR REPLACE EXTERNAL TABLE dataset.CsvTable
(
  x INTEGER AS CAST(GET_IGNORE_CASE($1, 'c1') AS INTEGER),
  y STRING AS CAST(GET_IGNORE_CASE($1, 'c2') AS STRING)
)
!!!RESOLVE EWI!!! /*** SSC-EWI-BQ0015 - EXTERNAL TABLE REQUIRES AN EXTERNAL STAGE TO ACCESS gs://bucket, DEFINE AND REPLACE THE EXTERNAL_STAGE PLACEHOLDER ***/!!!
LOCATION = @EXTERNAL_STAGE
AUTO_REFRESH = false
PATTERN = 'example.csv'
FILE_FORMAT = (TYPE = CSV
  field_delimiter = '|')
!!!RESOLVE EWI!!! /*** SSC-EWI-BQ0001 - SNOWFLAKE DOES NOT SUPPORT THE OPTIONS: MAX_BAD_RECORDS. ***/!!!
OPTIONS(
  max_bad_records = 5
);
```

### Related EWIs[¶](#id48)

1. [SSC-EWI-BQ0013](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/bigqueryEWI.html#ssc-ewi-bq0013):
   External table data format not supported in snowflake
2. [SSC-EWI-BQ0014](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/bigqueryEWI.html#ssc-ewi-bq0014):
   Hive partitioned external tables are not supported in snowflake
3. [SSC-EWI-BQ0015](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/bigqueryEWI.html#ssc-ewi-bq0015):
   External table requires an external stage to access a external location, define and replace the
   EXTERNAL_STAGE placeholder
4. [SSC-FDM-BQ0004](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/bigqueryFDM.html#ssc-fdm-bq0004):
   The INFER_SCHEMA function requires a file path without wildcards to generate the table template,
   replace the FILE_PATH placeholder with it
5. [SSC-FDM-BQ0005](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/bigqueryFDM.html#ssc-fdm-bq0005):
   Parsing the CSV header is not supported in external tables, columns must be renamed to match the
   original names
6. [SSC-FDM-BQ0006](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/bigqueryFDM.html#ssc-fdm-bq0006):
   Reading from Google Drive is not supported in Snowflake, upload the files to the external
   location and replace the FILE_PATH placeholders
7. [SSC-FDM-BQ0007](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/bigqueryFDM.html#ssc-fdm-bq0007):
   Reading from spreadsheets is not supported in snowflake, use the CSV file type instead

## CREATE TABLE CLONE[¶](#create-table-clone)

### Grammar syntax[¶](#id49)

```
CREATE TABLE [ IF NOT EXISTS ]
destination_table_name
CLONE source_table_name [FOR SYSTEM_TIME AS OF time_expression]
...
[OPTIONS(table_option_list)]
```

### Sample Source Patterns[¶](#id50)

#### FOR SYSTEM TIME AS OF[¶](#for-system-time-as-of)

##### BigQuery[¶](#id51)

```
CREATE TABLE my_clone_table
CLONE some_table_name2
FOR SYSTEM_TIME AS OF TIMESTAMP "2025-01-01 00:00:00 UTC";
```

##### Snowflake[¶](#id52)

```
CREATE TABLE my_clone_table
CLONE some_table_name2 AT (TIMESTAMP => TIMESTAMP "2025-01-01 00:00:00 UTC");
```

::{note} The LABELS option in CREATE TABLE CLONE statements are not transformed into TAGs because
the TAGs of the source table are copied, they cannot be changed during the copy of the table.
Transformation of other table options are the same as specified for the
[CREATE TABLE](#labels-table-option) statement.

## CREATE TABLE COPY

### Grammar syntax

```
CREATE [ OR REPLACE ] TABLE [ IF NOT EXISTS ] table_name
COPY source_table_name
...
[OPTIONS(table_option_list)]
```

### Sample Source Patterns

#### General case

CREATE TABLE CLONE in Snowflake is functionally equivalent to CREATE TABLE COPY.

##### Input Code

##### BigQuery

```
CREATE TABLE newtable
COPY sourceTable;
```

##### Snowflake

```
CREATE TABLE newtable CLONE sourceTable;
```

**Note:**

The LABELS option in CREATE TABLE COPY statements are not transformed into TAGs because the TAGs of
the source table are copied, they cannot be changed during the copy of the table. Transformation of
other table options are the same as specified for the [CREATE TABLE](#labels-table-option)
statement.

## CREATE TABLE LIKE[¶](#create-table-like)

### Grammar syntax[¶](#id57)

```
CREATE [ OR REPLACE ] TABLE [ IF NOT EXISTS ]
table_name
LIKE [[project_name.]dataset_name.]source_table_name
...
[OPTIONS(table_option_list)]
```

Success

CREATE TABLE LIKE is fully supported by Snowflake.

**Note:**

The LABELS option in CREATE TABLE LIKE statements are not transformed into TAGs because the TAGs of
the source table are copied, they cannot be changed during the copy of the table. Transformation of
other table options are the same as specified for the [CREATE TABLE](#labels-table-option)
statement.

## CREATE TABLE SNAPSHOT[¶](#create-table-snapshot)

### Grammar syntax[¶](#id58)

```
CREATE SNAPSHOT TABLE [ IF NOT EXISTS ] table_snapshot_name
CLONE source_table_name
[FOR SYSTEM_TIME AS OF time_expression]
[OPTIONS(snapshot_option_list)]
```

### Sample Source Patterns[¶](#id59)

#### General case[¶](#id60)

The Snapshot keyword is removed in Snowflake, transforming the table into a CREATE TABLE CLONE.

The two differences between snapshot and clones are that snapshots are not editable and usually have
an expiration date. Expiration dates are not supported, this is handled as specified for the
[CREATE TABLE](#labels-table-option) statement unsupported options.

##### BigQuery[¶](#id61)

```
CREATE SNAPSHOT TABLE mytablesnapshot
CLONE mytable;
```

##### Snowflake[¶](#id62)

```
CREATE TABLE mytablesnapshot CLONE mytable;
```

#### FOR SYSTEM TIME AS OF[¶](#id63)

##### BigQuery[¶](#id64)

```
CREATE SNAPSHOT TABLE IF NOT EXISTS my_snapshot_table2
CLONE some_table_name2
FOR SYSTEM_TIME AS OF TIMESTAMP "2025-01-01 00:00:00 UTC";
```

##### Snowflake[¶](#id65)

```
CREATE TABLE IF NOT EXISTS my_snapshot_table2
CLONE some_table_name2 AT (TIMESTAMP => TIMESTAMP "2025-01-01 00:00:00 UTC");
```

**Note:**

The LABELS option in CREATE TABLE COPY statements are not transformed into TAGs because the TAGs of
the source table are copied, they cannot be changed during the copy of the table.

Transformation of other table options are the same as specified for the
[CREATE TABLE](#labels-table-option) statement.
