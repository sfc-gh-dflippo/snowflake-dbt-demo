---
auto_generated: true
description: Translation reference for all the supported statements by SnowConvert
  AI for Redshift.
last_scraped: '2026-01-14T16:53:40.416649+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/redshift/redshift-sql-statements
title: SnowConvert AI - Redshift - SQL Statements | Snowflake Documentation
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
          + [Redshift](README.md)

            - [Basic Elements](redshift-basic-elements.md)
            - [Expressions](redshift-expressions.md)
            - [Conditions](redshift-conditions.md)
            - [Data types](redshift-data-types.md)
            - [SQL Statements](redshift-sql-statements.md)

              * [CONTINUE HANDLER](redshift-continue-handler.md)
              * [EXIT HANDLER](redshift-exit-handler.md)
              * [CREATE TABLE](redshift-sql-statements-create-table.md)
              * [CREATE TABLE AS](redshift-sql-statements-create-table-as.md)
              * [CREATE PROCEDURE](rs-sql-statements-create-procedure.md)
              * [SELECT](rs-sql-statements-select.md)
              * [SELECT INTO](rs-sql-statements-select-into.md)
            - [Functions](redshift-functions.md)
            - [System Catalog Tables](redshift-system-catalog.md)
            - ETL And BI Repointing

              - [Power BI Redshift Repointing](etl-bi-repointing/power-bi-redshift-repointing.md)
          + [PostgreSQL-Greenplum-Netezza](../postgres/README.md)
          + [BigQuery](../bigquery/README.md)
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)Translation References[Redshift](README.md)SQL Statements

# SnowConvert AI - Redshift - SQL Statements[¶](#snowconvert-ai-redshift-sql-statements "Link to this heading")

Translation reference for all the supported statements by SnowConvert AI for Redshift.

## CALL[¶](#call "Link to this heading")

### Description[¶](#description "Link to this heading")

> Runs a stored procedure. The CALL command must include the procedure name and the input argument values. You must call a stored procedure by using the CALL statement. ([Redshift SQL Language Reference CALL](https://docs.aws.amazon.com/redshift/latest/dg/r_CALL_procedure.html)).

### Grammar Syntax[¶](#grammar-syntax "Link to this heading")

```
 CALL sp_name ( [ argument ] [, ...] )
```

Copy

### Sample Source Patterns[¶](#sample-source-patterns "Link to this heading")

#### Base scenario[¶](#base-scenario "Link to this heading")

##### Input Code:[¶](#input-code "Link to this heading")

##### Redshift[¶](#redshift "Link to this heading")

```
 CREATE PROCEDURE sp_insert_values(IN arg1 INT, IN arg2 DATE)
LANGUAGE plpgsql
AS
$$
BEGIN
    INSERT INTO event VALUES (arg1, arg2);
END;
$$;

CALL sp_insert_values(1, CURRENT_DATE);
```

Copy

##### Output Code:[¶](#output-code "Link to this heading")

##### Redshift[¶](#id1 "Link to this heading")

```
 CREATE PROCEDURE sp_insert_values (arg1 INT, arg2 DATE)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
AS
$$
BEGIN
    INSERT INTO event
    VALUES (:arg1, : arg2);
END;
$$;

CALL sp_insert_values(1, CURRENT_DATE());
```

Copy

#### Call using Output Parameters Mode (INOUT, OUT)[¶](#call-using-output-parameters-mode-inout-out "Link to this heading")

##### Input Code:[¶](#id2 "Link to this heading")

##### Redshift[¶](#id3 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE sp_calculate_sum_product(IN a NUMERIC, IN b NUMERIC, INOUT sum_result NUMERIC, INOUT product_result NUMERIC)
LANGUAGE plpgsql
AS $$
BEGIN
    sum_result := a + b;
    product_result := a * b;
END;
$$;

CREATE OR REPLACE PROCEDURE call_sp_calculate_sum_product()
LANGUAGE plpgsql
AS $$
DECLARE
    sum_value NUMERIC DEFAULT null;
    product_value NUMERIC DEFAULT null;
BEGIN
    CALL sp_calculate_sum_product(FLOOR(20.5)::NUMERIC, CEIL(20.7)::NUMERIC, sum_value, product_value);
    INSERT INTO test VALUES (sum_value, product_value);
END;
$$;

CALL call_sp_calculate_sum_product();
```

Copy

##### Output Code:[¶](#id4 "Link to this heading")

##### Redshift[¶](#id5 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE sp_calculate_sum_product (a NUMERIC, b NUMERIC, sum_result OUT NUMERIC, product_result OUT NUMERIC)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
AS $$
BEGIN
    sum_result := a + b;
    product_result := a * b;
END;
$$;

CREATE OR REPLACE PROCEDURE call_sp_calculate_sum_product ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
AS $$
DECLARE
    sum_value NUMERIC DEFAULT null;
    product_value NUMERIC DEFAULT null;
BEGIN
    CALL sp_calculate_sum_product(FLOOR(20.5)::NUMERIC, CEIL(20.7)::NUMERIC, : sum_value, : product_value);
    INSERT INTO test
    VALUES (:sum_value, : product_value);
END;
$$;

CALL call_sp_calculate_sum_product();
```

Copy

### Known Issues[¶](#known-issues "Link to this heading")

* Output parameters from calls outside procedures won’t work.

### Related EWIs.[¶](#related-ewis "Link to this heading")

1. [SSC-EWI-0073](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0073): Pending Functional Equivalence Review

## CREATE DATABASE[¶](#create-database "Link to this heading")

### Grammar Syntax[¶](#id6 "Link to this heading")

```
 CREATE DATABASE database_name 
[ { [ WITH ]
    [ OWNER [=] db_owner ]
    [ CONNECTION LIMIT { limit | UNLIMITED } ]
    [ COLLATE { CASE_SENSITIVE | CASE_INSENSITIVE } ]
    [ ISOLATION LEVEL { SERIALIZABLE | SNAPSHOT } ]
  }
  | { [ WITH PERMISSIONS ] FROM DATASHARE datashare_name ] OF [ ACCOUNT account_id ] NAMESPACE namespace_guid }
  | { FROM { { ARN '<arn>' } { WITH DATA CATALOG SCHEMA '<schema>' | WITH NO DATA CATALOG SCHEMA } }
             | { INTEGRATION '<integration_id>'} }
  | { IAM_ROLE  {default | 'SESSION' | 'arn:aws:iam::<account-id>:role/<role-name>' } }
```

Copy

For more information please refer to Redshift [`CREATE DATABASE` documentation](https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_DATABASE.html).

### Sample Source Patterns[¶](#id7 "Link to this heading")

#### Basic samples[¶](#basic-samples "Link to this heading")

##### Input Code:[¶](#id8 "Link to this heading")

##### Redshift[¶](#id9 "Link to this heading")

```
 CREATE DATABASE database_name;
```

Copy

##### Output Code:[¶](#id10 "Link to this heading")

##### Snowflake[¶](#snowflake "Link to this heading")

```
 CREATE DATABASE IF NOT EXISTS database_name
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/25/2024" }}';
```

Copy

#### Collate Clause[¶](#collate-clause "Link to this heading")

##### Input Code:[¶](#id11 "Link to this heading")

##### Redshift[¶](#id12 "Link to this heading")

```
 CREATE DATABASE database_collate
COLLATE CASE_INSENSITIVE;
```

Copy

##### Output Code:[¶](#id13 "Link to this heading")

##### Snowflake[¶](#id14 "Link to this heading")

```
 CREATE DATABASE IF NOT EXISTS database_collate
DEFAULT_DDL_COLLATION='en-ci'
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/24/2024" }}';
```

Copy

#### Connection Limit Clause[¶](#connection-limit-clause "Link to this heading")

##### Input Code:[¶](#id15 "Link to this heading")

##### Redshift[¶](#id16 "Link to this heading")

```
 CREATE DATABASE database_connection
CONNECTION LIMIT UNLIMITED;
```

Copy

##### Output Code:[¶](#id17 "Link to this heading")

##### Snowflake[¶](#id18 "Link to this heading")

```
 CREATE DATABASE IF NOT EXISTS database_connection
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/24/2024" }}';
```

Copy

Warning

The connection limit clause is removed since the connection concurrency in snowflake is managed by warehouse. More information [here](https://docs.snowflake.com/en/sql-reference/parameters#label-max-concurrency-level).

#### From ARN Clause[¶](#from-arn-clause "Link to this heading")

##### Input Code:[¶](#id19 "Link to this heading")

##### Redshift[¶](#id20 "Link to this heading")

```
 CREATE DATABASE database_fromARN
FROM ARN 'arn' WITH NO DATA CATALOG SCHEMA IAM_ROLE 'arn:aws:iam::<account-id>:role/<role-name';
```

Copy

##### Output Code:[¶](#id21 "Link to this heading")

##### Snowflake[¶](#id22 "Link to this heading")

```
 CREATE DATABASE IF NOT EXISTS database_fromARN
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/24/2024" }}';
```

Copy

Warning

This clause is removed since it is used to reference [Amazon Resources](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference-arns.html), not valid in Snowflake.

#### From Datashare Clause[¶](#from-datashare-clause "Link to this heading")

##### Input Code[¶](#id23 "Link to this heading")

##### Redshift[¶](#id24 "Link to this heading")

```
 CREATE DATABASE database_fromDatashare
FROM DATASHARE datashare_name OF NAMESPACE 'namespace_guid';
```

Copy

##### Output Code[¶](#id25 "Link to this heading")

##### Snowflake[¶](#id26 "Link to this heading")

```
 CREATE DATABASE IF NOT EXISTS  database_fromDatashare
FROM DATASHARE datashare_name OF NAMESPACE 'namespace_guid' !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'FromDatashareAttribute' NODE ***/!!!
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/24/2024" }}';
```

Copy

Note

The transformation for Datashare is planned to be delivered in the future.

#### Owner Clause[¶](#owner-clause "Link to this heading")

##### Input Code[¶](#id27 "Link to this heading")

##### Redshift[¶](#id28 "Link to this heading")

```
 CREATE DATABASE database_Owner
OWNER db_owner
ENCODING 'encoding';
```

Copy

##### Output Code[¶](#id29 "Link to this heading")

##### Snowflake[¶](#id30 "Link to this heading")

```
 CREATE DATABASE IF NOT EXISTS database_Owner
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/24/2024" }}';
```

Copy

Warning

Please be aware that for this case, the owner clause is removed from the code since Snowflake databases are owned by roles, not individual users. For more information please refer to [Snowflake `GRANT OWNERSHIP` documentation](https://docs.snowflake.com/en/sql-reference/sql/grant-ownership).

#### Isolation Level Clause[¶](#isolation-level-clause "Link to this heading")

##### Input Code[¶](#id31 "Link to this heading")

##### Redshift[¶](#id32 "Link to this heading")

```
 CREATE DATABASE database_Isolation
ISOLATION LEVEL SNAPSHOT;
```

Copy

##### Output Code[¶](#id33 "Link to this heading")

##### Snowflake[¶](#id34 "Link to this heading")

```
 CREATE DATABASE IF NOT EXISTS database_Isolation
ISOLATION LEVEL SNAPSHOT !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'IsolationLevelAttribute' NODE ***/!!!
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/24/2024" }}';
```

Copy

Note

The transformation for Isolation Level is planned to be delivered in the future.

### Related EWIs[¶](#id35 "Link to this heading")

* [SSC-EWI-0073](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0073): Pending Functional Equivalence Review

## CREATE EXTERNAL TABLE[¶](#create-external-table "Link to this heading")

### Description [¶](#id36 "Link to this heading")

Currently SnowConvert AI is transforming `CREATE EXTERNAL TABLES` to regular tables, that implies additional effort because data stored in external RedShift tables must be transferred to the Snowflake database.

### Grammar Syntax [¶](#id37 "Link to this heading")

```
 CREATE EXTERNAL TABLE
external_schema.table_name
(column_name data_type [, …] )
[ PARTITIONED BY (col_name data_type [, … ] )]
[ { ROW FORMAT DELIMITED row_format |
  ROW FORMAT SERDE 'serde_name'
  [ WITH SERDEPROPERTIES ( 'property_name' = 'property_value' [, ...] ) ] } ]
STORED AS file_format
LOCATION { 's3://bucket/folder/' | 's3://bucket/manifest_file' }
[ TABLE PROPERTIES ( 'property_name'='property_value' [, ...] ) ]

CREATE EXTERNAL TABLE
external_schema.table_name
[ PARTITIONED BY (col_name [, … ] ) ]
[ ROW FORMAT DELIMITED row_format ]
STORED AS file_format
LOCATION { 's3://bucket/folder/' }
[ TABLE PROPERTIES ( 'property_name'='property_value' [, ...] ) ]
 AS
 { select_statement }
```

Copy

Click [here](https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_EXTERNAL_TABLE.html) to go to the specification for this syntax.

### Sample Source Patterns[¶](#id38 "Link to this heading")

#### Input Code:[¶](#id39 "Link to this heading")

##### Redshift[¶](#id40 "Link to this heading")

```
 CREATE EXTERNAL TABLE
external_schema.sales_data
(
    sales_id INT,
    product_id INT,
    sales_amount DECIMAL(10, 2),
    sales_date DATE
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION 's3://mybucket/sales_data/';
```

Copy

##### Output Code:[¶](#id41 "Link to this heading")

##### Snowflake[¶](#id42 "Link to this heading")

```
 --** SSC-FDM-0004 - EXTERNAL TABLE TRANSLATED TO REGULAR TABLE **
CREATE TABLE external_schema.sales_data
(
    sales_id INT,
    product_id INT,
    sales_amount DECIMAL(10, 2),
    sales_date DATE
)
--ROW FORMAT DELIMITED
--FIELDS TERMINATED BY ','
--STORED AS TEXTFILE
--LOCATION 's3://mybucket/sales_data/'
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/17/2024" }}'
;
```

Copy

#### Create External Table AS[¶](#create-external-table-as "Link to this heading")

##### Input Code:[¶](#id43 "Link to this heading")

##### Redshift[¶](#id44 "Link to this heading")

```
 CREATE EXTERNAL TABLE spectrum.partitioned_lineitem
PARTITIONED BY (l_shipdate, l_shipmode)
STORED AS parquet
LOCATION 'S3://amzn-s3-demo-bucket/cetas/partitioned_lineitem/'
AS SELECT l_orderkey, l_shipmode, l_shipdate, l_partkey FROM local_table;
```

Copy

##### Output Code:[¶](#id45 "Link to this heading")

##### Snowflake[¶](#id46 "Link to this heading")

```
 --** SSC-FDM-0004 - EXTERNAL TABLE TRANSLATED TO REGULAR TABLE **
CREATE TABLE spectrum.partitioned_lineitem
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/17/2024" }}'
--PARTITIONED BY (l_shipdate, l_shipmode)
--STORED AS parquet
--LOCATION 'S3://amzn-s3-demo-bucket/cetas/partitioned_lineitem/'
AS SELECT l_orderkey, l_shipmode, l_shipdate, l_partkey FROM
local_table;
```

Copy

### Recommendations[¶](#recommendations "Link to this heading")

* For the usage of Create External Table in Snowflake you may refer to [Snowflake’s documentation.](https://docs.snowflake.com/en/sql-reference/sql/create-external-table)

### Related EWIs[¶](#id47 "Link to this heading")

1. [SSC-FDM-0004](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0004): External table translated to regular table

## CREATE MATERIALIZED VIEW[¶](#create-materialized-view "Link to this heading")

### Description[¶](#id48 "Link to this heading")

In SnowConvert AI, Redshift Materialized Views are transformed into Snowflake Dynamic Tables. To properly configure Dynamic Tables, two essential parameters must be defined: TARGET\_LAG and WAREHOUSE. If these parameters are left unspecified in the configuration options, SnowConvert AI will default to preassigned values during the conversion, as demonstrated in the example below.

For more information on Materialized Views, click [here](https://docs.aws.amazon.com/redshift/latest/dg/materialized-view-create-sql-command.html).

For details on the necessary parameters for Dynamic Tables, click [here](https://docs.snowflake.com/en/sql-reference/sql/create-dynamic-table).

### Grammar Syntax[¶](#id49 "Link to this heading")

The following is the SQL syntax to create a view in Amazon Redshift. Click [here](https://docs.aws.amazon.com/redshift/latest/dg/materialized-view-create-sql-command.html) to here to go to Redshifts specification for this syntax.

```
 CREATE MATERIALIZED VIEW mv_name
[ BACKUP { YES | NO } ]
[ table_attributes ]
[ AUTO REFRESH { YES | NO } ]
AS query
```

Copy

### Sample Source Patterns[¶](#id50 "Link to this heading")

#### Input Code:[¶](#id51 "Link to this heading")

##### Redshift[¶](#id52 "Link to this heading")

```
 CREATE MATERIALIZED VIEW mv_baseball AS
SELECT ball AS baseball FROM baseball_table;
```

Copy

##### Output Code:[¶](#id53 "Link to this heading")

##### Snowflake[¶](#id54 "Link to this heading")

```
 CREATE DYNAMIC TABLE mv_baseball
--** SSC-FDM-0031 - DYNAMIC TABLE REQUIRED PARAMETERS SET BY DEFAULT **
TARGET_LAG='1 day'
WAREHOUSE=UPDATE_DUMMY_WAREHOUSE
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "11/26/2024",  "domain": "test" }}'
AS
    SELECT ball AS baseball FROM
        baseball_table;
```

Copy

Note

For the table attributes documentation you can check de following documentation:

* [Sortkey](redshift-sql-statements-create-table.html#sortkey)
* [DistKey](redshift-sql-statements-create-table.html#distkey)
* [DistStyle](redshift-sql-statements-create-table.html#diststyle)

Warning

The BACKUP and AUTO REFRESH clauses are deleted since they are not applicable in a Snowflake’s Dynamic Table

### Related Ewis[¶](#id55 "Link to this heading")

* [SSC-FDM-0031](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0031): Dynamic Table required parameters set by default

## CREATE SCHEMA[¶](#create-schema "Link to this heading")

### Grammar Syntax[¶](#id56 "Link to this heading")

```
 CREATE SCHEMA [ IF NOT EXISTS ] schema_name [ AUTHORIZATION username ]
           [ QUOTA {quota [MB | GB | TB] | UNLIMITED} ] [ schema_element [ ... ]

CREATE SCHEMA AUTHORIZATION username [ QUOTA {quota [MB | GB | TB] | UNLIMITED} ] 
[ schema_element [ ... ] ]
```

Copy

For more information please refer to [Redshift `CREATE SCHEMA` documentation](https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_SCHEMA.html).

### Sample Source Patterns[¶](#id57 "Link to this heading")

#### Basic samples[¶](#id58 "Link to this heading")

##### Input Code:[¶](#id59 "Link to this heading")

##### Redshift[¶](#id60 "Link to this heading")

```
 CREATE SCHEMA s1;

CREATE SCHEMA IF NOT EXISTS s2;

CREATE SCHEMA s3
CREATE TABLE t1
(
    col1 INT
)
CREATE VIEW v1 AS SELECT * FROM t1;
```

Copy

##### Output Code:[¶](#id61 "Link to this heading")

##### Snowflake[¶](#id62 "Link to this heading")

```
 CREATE SCHEMA IF NOT EXISTS s1
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/23/2024" }}'
;

CREATE SCHEMA IF NOT EXISTS s2
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/23/2024" }}'
;

CREATE SCHEMA IF NOT EXISTS s3
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/23/2024" }}'
;
CREATE TABLE t1
(
    col1 INT
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/23/2024" }}'
;
CREATE VIEW v1
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/23/2024" }}'
AS SELECT * FROM
    t1;
```

Copy

#### Authorization Clause[¶](#authorization-clause "Link to this heading")

##### Input Code:[¶](#id63 "Link to this heading")

##### Redshift[¶](#id64 "Link to this heading")

```
 CREATE SCHEMA s1 AUTHORIZATION miller;
```

Copy

##### Output Code:[¶](#id65 "Link to this heading")

##### Snowflake[¶](#id66 "Link to this heading")

```
 CREATE SCHEMA IF NOT EXISTS s1
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/23/2024" }}'
;
```

Copy

Warning

Please be aware that for this case, the authorization clause is removed from the code since Snowflake schemas are owned by roles, not individual users. For more information please refer to [Snowflake `GRANT OWNERSHIP` documentation](https://docs.snowflake.com/en/sql-reference/sql/grant-ownership).

#### Quota Clause[¶](#quota-clause "Link to this heading")

##### Input Code:[¶](#id67 "Link to this heading")

##### Redshift[¶](#id68 "Link to this heading")

```
 CREATE SCHEMA s1 QUOTA UNLIMITED;

CREATE SCHEMA s2 QUOTA 10 TB;
```

Copy

##### Output Code:[¶](#id69 "Link to this heading")

##### Snowflake[¶](#id70 "Link to this heading")

```
 CREATE SCHEMA IF NOT EXISTS s1
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/23/2024" }}'
;

CREATE SCHEMA IF NOT EXISTS s2
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/23/2024" }}'
;
```

Copy

Note

In Snowflake is not allowed to define a quota per scheme. Storage management is done at the account and warehouse level, and Snowflake handles it automatically. For this reason it is removed from the code.

#### Create Schema Authorization[¶](#create-schema-authorization "Link to this heading")

In Redshift when the schema name is not specified but the authorization clause is defined, a new schema is created with the owner’s name. For this reason this behavior is replicated in Snowflake.

##### Input Code:[¶](#id71 "Link to this heading")

##### Redshift[¶](#id72 "Link to this heading")

```
 CREATE SCHEMA AUTHORIZATION miller;
```

Copy

##### Output Code:[¶](#id73 "Link to this heading")

##### Snowflake[¶](#id74 "Link to this heading")

```
 CREATE SCHEMA IF NOT EXISTS miller
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/23/2024" }}'
;
```

Copy

### Related EWIs[¶](#id75 "Link to this heading")

There are no known issues.

## CREATE FUNCTION[¶](#create-function "Link to this heading")

### Description[¶](#id76 "Link to this heading")

This command defines a user-defined function (UDF) within the database. These functions encapsulate reusable logic that can be invoked within SQL queries.

### Grammar Syntax[¶](#id77 "Link to this heading")

The following is the SQL syntax to create a view in Amazon Redshift. Click [here](https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_VIEW.html) to here to go to Redshifts specification for this syntax.

```
 CREATE [ OR REPLACE ] FUNCTION f_function_name
( { [py_arg_name  py_arg_data_type |
sql_arg_data_type } [ , ... ] ] )
RETURNS data_type
{ VOLATILE | STABLE | IMMUTABLE }
AS $$
  { python_program | SELECT_clause }
$$ LANGUAGE { plpythonu | sql }
```

Copy

### SQL Language[¶](#sql-language "Link to this heading")

#### Volatility category[¶](#volatility-category "Link to this heading")

In Snowflake, `VOLATILE` and `IMMUTABLE` function volatility are functionally equivalent. Given that `STABLE` is inherently transformed to the default `VOLATILE` behavior, explicit use of `STABLE` will be delete.

##### Input Code:[¶](#id78 "Link to this heading")

##### Redshift[¶](#id79 "Link to this heading")

```
 CREATE OR REPLACE FUNCTION get_sale(INTEGER)
RETURNS FLOAT
STABLE
AS $$
SELECT price FROM sales where id = $1
$$ LANGUAGE SQL;
```

Copy

##### Output Code:[¶](#id80 "Link to this heading")

##### Snowflake[¶](#id81 "Link to this heading")

```
 CREATE OR REPLACE FUNCTION get_sale (SC_ARG1 INTEGER)
RETURNS FLOAT
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
AS $$
SELECT price FROM
sales
where id = SC_ARG1
$$
;
```

Copy

### Python Language[¶](#python-language "Link to this heading")

Within the SnowConvert AI scope, the Python language for `CREATE FUNCTION` statements is not supported. Consequently, the language `plpythonu` will be flagged with an EWI (SSC-EWI-0073), and its body could appear with parsing errors.

#### Input Code:[¶](#id82 "Link to this heading")

##### Redshift[¶](#id83 "Link to this heading")

```
 create function f_py_greater (a float, b float)
  returns float
stable
as $$
  if a > b:
    return a
  return b
$$ language plpythonu;
```

Copy

##### Output Code:[¶](#id84 "Link to this heading")

##### Snowflake[¶](#id85 "Link to this heading")

```
 create function f_py_greater (a float, b float)
returns float
language plpythonu !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'LANGUAGE PLPythonU' NODE ***/!!!
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
as $$
-- ** SSC-EWI-0001 - UNRECOGNIZED TOKEN ON LINE '5' COLUMN '3' OF THE SOURCE CODE STARTING AT 'if'. EXPECTED 'STATEMENT' GRAMMAR. LAST MATCHING TOKEN WAS 'if' ON LINE '5' COLUMN '3'. **
--  if a > b:
--    return a
--  return b
$$
;
```

Copy

### Related EWIs[¶](#id86 "Link to this heading")

There are no known issues.

## CREATE VIEW[¶](#create-view "Link to this heading")

### Description[¶](#id87 "Link to this heading")

This command creates a view in a database, which is run every time the view is referenced in a query. Using the WITH NO SCHEMA BINDING clause, you can create views to an external table or objects that don’t exist yet. This clause, however, requires you to specify the qualified name of the object or table that you are referencing.

### Grammar Syntax[¶](#id88 "Link to this heading")

The following is the SQL syntax to create a view in Amazon Redshift. Click [here](https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_VIEW.html) to here to go to Redshifts specification for this syntax.

```
 CREATE [ OR REPLACE ] VIEW name [ ( column_name [, ...] ) ] AS query
[ WITH NO SCHEMA BINDING ]
```

Copy

### Sample Source Patterns[¶](#id89 "Link to this heading")

Considering the obligatory and optional clauses in Redshifts command, the output after migration to Snowflake is very similar.

#### Input Code:[¶](#id90 "Link to this heading")

##### Redshift[¶](#id91 "Link to this heading")

```
 CREATE VIEW myuser
AS 
SELECT lastname FROM users;


CREATE VIEW myuser2
AS 
SELECT lastname FROM users2
WITH NO SCHEMA BINDING;
```

Copy

##### Output Code:[¶](#id92 "Link to this heading")

##### Snowflake[¶](#id93 "Link to this heading")

```
 CREATE VIEW myuser
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "01/16/2025",  "domain": "test" }}'
AS
SELECT lastname FROM
users;

CREATE VIEW myuser2
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "01/16/2025",  "domain": "test" }}'
AS
SELECT lastname FROM
users2
!!!RESOLVE EWI!!! /*** SSC-EWI-RS0003 - WITH NO SCHEMA BINDING STATEMENT CAN NOT BE REMOVED DUE TO MISSING REFERENCES. ***/!!!
WITH NO SCHEMA BINDING;
```

Copy

There are some exceptions, however, of one unsupported clause from Redshift, therefore an EWI was implemented to cover this case.

### Related EWIs[¶](#id94 "Link to this heading")

* [SSC-EWI-RS0003](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/redshiftEWI.html#ssc-ewi-rs0003): With no schema binding statement is not supported in Snowflake.

## DELETE[¶](#delete "Link to this heading")

### Description[¶](#id95 "Link to this heading")

> Deletes rows from tables. ([Redshift SQL Language Reference Delete Statement](https://docs.aws.amazon.com/redshift/latest/dg/r_DELETE.html)).

Note

This syntax is fully supported in Snowflake.

### Grammar Syntax[¶](#id96 "Link to this heading")

```
 [ WITH [RECURSIVE] common_table_expression [, common_table_expression , ...] ]
DELETE [ FROM ] { table_name | materialized_view_name }
    [ USING table_name, ... ]
    [ WHERE condition ]
```

Copy

### Sample Source Patterns[¶](#id97 "Link to this heading")

#### **Setup data**[¶](#setup-data "Link to this heading")

##### Redshift[¶](#id98 "Link to this heading")

```
 CREATE TABLE employees (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    department VARCHAR(255),
    manager_id INT REFERENCES employees(id)
);

INSERT INTO employees (id, name, department, manager_id) VALUES
(1, 'Alice', 'Sales', 2),
(2, 'Bob', 'Sales', 1),
(3, 'Charlie', 'Sales', 1),
(4, 'David', 'Marketing', 2),
(5, 'Eve', 'Marketing', 4),
(6, 'Frank', 'Marketing', 4),
(7, 'Grace', 'Engineering', 6),
(8, 'Helen', 'Engineering', 7),
(9, 'Ivy', 'Engineering', 7),
(10, 'John', 'Sales', 3),
(11, 'Joe', 'Engineering', 5);


CREATE TABLE departments (
    department_name VARCHAR(255)
);

INSERT INTO departments (department_name) VALUES
('Sales'), 
('Marketing'), 
('Engineering');
```

Copy

#### From Clause[¶](#from-clause "Link to this heading")

Update a table by referencing information from other tables. In Redshift, the FROM keyword is optional, but in Snowflake, it is mandatory. Therefore, it will be added in cases where it’s missing.

##### Input Code:[¶](#id99 "Link to this heading")

##### Redshift[¶](#id100 "Link to this heading")

```
 DELETE employees;

SELECT * FROM employees ORDER BY id;
```

Copy

##### Result[¶](#result "Link to this heading")

| ID | NAME | DEPARTMENT | MANAGER\_ID |
| --- | --- | --- | --- |
|  |  |  |  |

##### Output Code:[¶](#id101 "Link to this heading")

##### Snowflake[¶](#id102 "Link to this heading")

```
 DELETE FROM
    employees;
    
SELECT * FROM employees ORDER BY id;
```

Copy

##### Result[¶](#id103 "Link to this heading")

| ID | NAME | DEPARTMENT | MANAGER\_ID |
| --- | --- | --- | --- |
|  |  |  |  |

#### Where Clause[¶](#where-clause "Link to this heading")

Restricts updates to rows that match a condition. When the condition returns true, the specified SET columns are updated. The condition can be a simple predicate on a column or a condition based on the result of a subquery. This clause is fully equivalent in Snowflake.

##### Input Code:[¶](#id104 "Link to this heading")

##### Redshift[¶](#id105 "Link to this heading")

```
 DELETE FROM employees
WHERE department = 'Marketing';

SELECT * FROM employees
ORDER BY id;
```

Copy

##### Result[¶](#id106 "Link to this heading")

| ID | NAME | DEPARTMENT | MANAGER\_ID |
| --- | --- | --- | --- |
| 1 | Alice | Sales | 2 |
| 2 | Bob | Sales | 1 |
| 3 | Charlie | Sales | 1 |
| 7 | Grace | Engineering | 6 |
| 8 | Helen | Engineering | 7 |
| 9 | Ivy | Engineering | 7 |
| 10 | John | Sales | 3 |
| 11 | Joe | Engineering | 5 |

##### Output Code:[¶](#id107 "Link to this heading")

##### Snowflake[¶](#id108 "Link to this heading")

```
 DELETE FROM
    employees
WHERE department = 'Marketing';

SELECT * FROM
    employees
ORDER BY id;
```

Copy

##### Result[¶](#id109 "Link to this heading")

| ID | NAME | DEPARTMENT | MANAGER\_ID |
| --- | --- | --- | --- |
| 1 | Alice | Sales | 2 |
| 2 | Bob | Sales | 1 |
| 3 | Charlie | Sales | 1 |
| 7 | Grace | Engineering | 6 |
| 8 | Helen | Engineering | 7 |
| 9 | Ivy | Engineering | 7 |
| 10 | John | Sales | 3 |
| 11 | Joe | Engineering | 5 |

#### Using Clause[¶](#using-clause "Link to this heading")

This clause introduces a list of tables when additional tables are referenced in the WHERE clause condition. This clause is fully equivalent in Snowflake.

##### Input Code:[¶](#id110 "Link to this heading")

##### Redshift[¶](#id111 "Link to this heading")

```
 DELETE FROM employees
USING departments d
WHERE employees.department = d.department_name
AND d.department_name = 'Sales';

SELECT * FROM employees ORDER BY id;
```

Copy

##### Result[¶](#id112 "Link to this heading")

| ID | NAME | DEPARTMENT | MANAGER\_ID |
| --- | --- | --- | --- |
| 4 | David | Marketing | 2 |
| 5 | Eve | Marketing | 4 |
| 6 | Frank | Marketing | 4 |
| 7 | Grace | Engineering | 6 |
| 8 | Helen | Engineering | 7 |
| 9 | Ivy | Engineering | 7 |
| 11 | Joe | Engineering | 5 |

##### Output Code:[¶](#id113 "Link to this heading")

##### Snowflake[¶](#id114 "Link to this heading")

```
 DELETE FROM employees
USING departments d
WHERE employees.department = d.department_name
AND d.department_name = 'Sales';

SELECT * FROM employees ORDER BY id;
```

Copy

##### Result[¶](#id115 "Link to this heading")

| ID | NAME | DEPARTMENT | MANAGER\_ID |
| --- | --- | --- | --- |
| 4 | David | Marketing | 2 |
| 5 | Eve | Marketing | 4 |
| 6 | Frank | Marketing | 4 |
| 7 | Grace | Engineering | 6 |
| 8 | Helen | Engineering | 7 |
| 9 | Ivy | Engineering | 7 |
| 11 | Joe | Engineering | 5 |

#### WITH clause[¶](#with-clause "Link to this heading")

This clause specifies one or more Common Table Expressions (CTE). The output column names are optional for non-recursive CTEs, but mandatory for recursive ones.

Since this clause cannot be used in an DELETE statement, it is transformed into temporary tables with their corresponding queries. After the DELETE statement is executed, these temporary tables are dropped to clean up, release resources, and avoid name collisions when creating tables within the same session. Additionally, if a regular table with the same name exists, it will take precedence again, since the temporary table [has priority](https://docs.snowflake.com/en/user-guide/tables-temp-transient#potential-naming-conflicts-with-other-table-types) over any other table with the same name in the same session.

##### Non-Recursive CTE[¶](#non-recursive-cte "Link to this heading")

##### Input Code:[¶](#id116 "Link to this heading")

##### Redshift[¶](#id117 "Link to this heading")

```
 WITH sales_employees AS (
    SELECT id
    FROM employees
    WHERE department = 'Sales'
), engineering_employees AS (
    SELECT id
    FROM employees
    WHERE department = 'Engineering'
)
DELETE FROM employees
WHERE id IN (SELECT id FROM sales_employees)
   OR id IN (SELECT id FROM engineering_employees);

SELECT * FROM employees ORDER BY id;
```

Copy

##### Result[¶](#id118 "Link to this heading")

| ID | NAME | DEPARTMENT | MANAGER\_ID |
| --- | --- | --- | --- |
| 4 | David | Marketing | 2 |
| 5 | Eve | Marketing | 4 |
| 6 | Frank | Marketing | 4 |

##### Output Code:[¶](#id119 "Link to this heading")

##### Snowflake[¶](#id120 "Link to this heading")

```
 CREATE TEMPORARY TABLE sales_employees AS
SELECT id
FROM employees
WHERE department = 'Sales';

CREATE TEMPORARY TABLE engineering_employees AS
SELECT id
FROM employees
WHERE department = 'Engineering';

DELETE FROM
    employees
WHERE id IN (SELECT id FROM sales_employees)
   OR id IN (SELECT id FROM engineering_employees);
   
DROP TABLE sales_employees;
DROP TABLE engineering_employees;

SELECT * FROM
    employees
ORDER BY id;
```

Copy

##### Result[¶](#id121 "Link to this heading")

| ID | NAME | DEPARTMENT | MANAGER\_ID |
| --- | --- | --- | --- |
| 4 | David | Marketing | 2 |
| 5 | Eve | Marketing | 4 |
| 6 | Frank | Marketing | 4 |

##### Recursive CTE[¶](#recursive-cte "Link to this heading")

##### Input Code:[¶](#id122 "Link to this heading")

##### Redshift[¶](#id123 "Link to this heading")

```
 WITH RECURSIVE subordinate_hierarchy(id, name, department, level) AS (
    SELECT id, name, department, 0 as level
    FROM employees
    WHERE department = 'Marketing'

    UNION ALL

    SELECT e.id, e.name, e.department, sh.level + 1
    FROM employees e
    INNER JOIN subordinate_hierarchy sh ON e.manager_id = sh.id
)
DELETE FROM employees
WHERE id IN (SELECT id FROM subordinate_hierarchy);
```

Copy

##### Result[¶](#id124 "Link to this heading")

| ID | NAME | DEPARTMENT | MANAGER\_ID |
| --- | --- | --- | --- |
| 1 | Alice | Sales | 2 |
| 2 | Bob | Sales | 1 |
| 3 | Charlie | Sales | 1 |
| 10 | John | Sales | 3 |

##### Output Code:[¶](#id125 "Link to this heading")

##### Snowflake[¶](#id126 "Link to this heading")

```
 CREATE TEMPORARY TABLE subordinate_hierarchy AS
   WITH RECURSIVE subordinate_hierarchy(id, name, department, level) AS (
       SELECT id, name, department, 0 as level
       FROM
           employees
       WHERE department = 'Marketing'

       UNION ALL

       SELECT e.id, e.name, e.department, sh.level + 1
       FROM
           employees e
       INNER JOIN
               subordinate_hierarchy sh ON e.manager_id = sh.id
   )
   SELECT
       id,
       name,
       department,
       level
   FROM
       subordinate_hierarchy;
       
   DELETE FROM
   employees
   WHERE id IN (SELECT id FROM
           subordinate_hierarchy
   );
   
   DROP TABLE subordinate_hierarchy;
```

Copy

##### Result[¶](#id127 "Link to this heading")

| ID | NAME | DEPARTMENT | MANAGER\_ID |
| --- | --- | --- | --- |
| 1 | Alice | Sales | 2 |
| 2 | Bob | Sales | 1 |
| 3 | Charlie | Sales | 1 |
| 10 | John | Sales | 3 |

#### Delete Materialized View[¶](#delete-materialized-view "Link to this heading")

In Redshift, you can apply the DELETE statement to materialized views used for [streaming ingestion](https://docs.aws.amazon.com/redshift/latest/dg/materialized-view-streaming-ingestion.html). In Snowflake, these views are transformed into dynamic tables, and the DELETE statement cannot be used on dynamic tables. For this reason, an EWI will be added.

##### Input Code:[¶](#id128 "Link to this heading")

##### Redshift[¶](#id129 "Link to this heading")

```
 CREATE MATERIALIZED VIEW emp_mv AS
SELECT id, name, department FROM employees WHERE department = 'Engineering';

DELETE FROM emp_mv
WHERE id = 2;
```

Copy

##### Output Code:[¶](#id130 "Link to this heading")

##### Snowflake[¶](#id131 "Link to this heading")

```
 CREATE DYNAMIC TABLE emp_mv
--** SSC-FDM-0031 - DYNAMIC TABLE REQUIRED PARAMETERS SET BY DEFAULT **
TARGET_LAG='1 day'
WAREHOUSE=UPDATE_DUMMY_WAREHOUSE
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/11/2025",  "domain": "test" }}'
AS
SELECT id, name, department FROM
employees
WHERE department = 'Engineering';
        
        
!!!RESOLVE EWI!!! /*** SSC-EWI-RS0008 - MATERIALIZED VIEW IS TRANSFORMED INTO A DYNAMIC TABLE, AND THE DELETE STATEMENT CANNOT BE USED ON DYNAMIC TABLES. ***/!!!
DELETE FROM
emp_mv
WHERE id = 2;
```

Copy

### Known Issues [¶](#id132 "Link to this heading")

* Replicating the functionality of the `WITH` clause requires creating temporary tables mirroring each Common Table Expression (CTE). However, this approach fails if a temporary table with the same name already exists within the current session, causing an error.

### Related EWIs[¶](#id133 "Link to this heading")

1. [SSC-FDM-0031](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0031): Dynamic Table required parameters set by default.
2. [SSC-EWI-RS0008](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/redshiftEWI.html#ssc-ewi-rs0008): Delete statement cannot be used on dynamic tables.

## EXECUTE[¶](#execute "Link to this heading")

### Description[¶](#id134 "Link to this heading")

> The `EXECUTE` `IMMEDIATE` statement builds and runs a dynamic SQL statement in a single operation.
>
> Native dynamic SQL uses the `EXECUTE` `IMMEDIATE` statement to process most dynamic SQL statements. ([Redshift Language Reference EXECUTE Statement](https://docs.aws.amazon.com/redshift/latest/dg/c_PLpgSQL-statements.html#r_PLpgSQL-dynamic-sql))

### Grammar Syntax[¶](#id135 "Link to this heading")

```
 EXECUTE command-string [ INTO target ];
```

Copy

### Sample Source Patterns[¶](#id136 "Link to this heading")

Concated Example

Input Code

#### Redshift[¶](#id137 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE create_dynamic_table(table_name VARCHAR) 
AS $$ 
DECLARE 
sql_statement VARCHAR; 
BEGIN 
sql_statement := 'CREATE TABLE IF NOT EXISTS ' || table_name || ' (id INT, value VARCHAR);'; 
EXECUTE sql_statement; 
END;
$$ LANGUAGE plpgsql;
```

Copy

Output Code

##### Snowflake[¶](#id138 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE create_dynamic_table (table_name VARCHAR)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
AS $$
DECLARE
sql_statement VARCHAR;
BEGIN
sql_statement := 'CREATE TABLE IF NOT EXISTS ' || table_name || ' (id INT, value VARCHAR)';
!!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!
EXECUTE IMMEDIATE sql_statement;
END;
$$;
```

Copy

#### Function Transformation[¶](#function-transformation "Link to this heading")

##### Input Code[¶](#id139 "Link to this heading")

##### Redshift[¶](#id140 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE insert_with_dynamic()
AS $$
DECLARE
sql_statement VARCHAR;
BEGIN
sql_statement := 'insert into orders(order_date) values ("getdate"());';
EXECUTE sql_statement;
END;
$$ LANGUAGE plpgsql;
```

Copy

##### Output Code[¶](#id141 "Link to this heading")

##### Snowflake[¶](#id142 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE insert_with_dynamic ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
AS $$
DECLARE
sql_statement VARCHAR;
BEGIN
sql_statement := 'insert into orders (order_date) values (GETDATE())';
!!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!
EXECUTE IMMEDIATE sql_statement;
END;
$$;
```

Copy

#### Error In Query Parsing[¶](#error-in-query-parsing "Link to this heading")

##### Input Code[¶](#id143 "Link to this heading")

##### Redshift[¶](#id144 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE bad_statement(table_name VARCHAR) 
AS $$ 
DECLARE 
sql_statement VARCHAR; 
BEGIN 
sql_statement := 'bad statement goes here'; 
EXECUTE sql_statement; 
END;
$$ LANGUAGE plpgsql;
```

Copy

##### Output Code[¶](#id145 "Link to this heading")

##### Snowflake[¶](#id146 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE bad_statement (table_name VARCHAR)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
AS $$
DECLARE
sql_statement VARCHAR;
BEGIN
sql_statement := 'bad statement goes here';
!!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!!!!RESOLVE EWI!!! /*** SSC-EWI-0027 - THE FOLLOWING STATEMENT USES A VARIABLE/LITERAL WITH AN INVALID QUERY AND IT WILL NOT BE EXECUTED ***/!!!
EXECUTE IMMEDIATE sql_statement;
END;
$$;
```

Copy

#### INTO Clause[¶](#into-clause "Link to this heading")

##### Input Code[¶](#id147 "Link to this heading")

##### Redshift[¶](#id148 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE get_max_id(table_name VARCHAR, OUT max_id INTEGER)
AS $$
DECLARE
    sql_statement VARCHAR;
BEGIN
    sql_statement := 'SELECT MAX(id) FROM ' || table_name || ';';
    EXECUTE sql_statement INTO max_id;
END;
$$ LANGUAGE plpgsql;
```

Copy

##### Output Code[¶](#id149 "Link to this heading")

##### Snowflake[¶](#id150 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE get_max_id (table_name VARCHAR, max_id OUT INTEGER)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
AS $$
        DECLARE
            sql_statement VARCHAR;
BEGIN
    sql_statement := 'SELECT
   MAX(id) FROM
   ' || table_name;
            !!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!
            EXECUTE IMMEDIATE sql_statement
                                            !!!RESOLVE EWI!!! /*** SSC-EWI-PG0007 - INTO CLAUSE IN DYNAMIC SQL IS NOT SUPPORTED IN SNOWFLAKE. ***/!!! INTO max_id;
END;
$$;
```

Copy

### Known Issues[¶](#id151 "Link to this heading")

#### 1. Execution results cannot be stored in variables.[¶](#execution-results-cannot-be-stored-in-variables "Link to this heading")

SnowScripting does not support INTO nor BULK COLLECT INTO clauses. For this reason, results will need to be passed through other means.

##### 2. Dynamic SQL Execution queries may be marked incorrectly as non-runnable.[¶](#dynamic-sql-execution-queries-may-be-marked-incorrectly-as-non-runnable "Link to this heading")

In some scenarios there an execute statement may be commented regardless of being safe or non-safe to run so please take this into account:

### Related EWIs[¶](#id152 "Link to this heading")

1. [SSC-EWI-0027](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0027): Variable with invalid query.
2. [SSC-EWI-0030](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0030): The statement below has usages of dynamic SQL.

## INSERT[¶](#insert "Link to this heading")

### Description[¶](#id153 "Link to this heading")

> Inserts new rows into a table. ([Redshift SQL Language Reference Insert Statement](https://docs.aws.amazon.com/redshift/latest/dg/r_INSERT_30.html#r_INSERT_30-synopsis)).

Warning

This syntax is partially supported in Snowflake.

### Grammar Syntax[¶](#id154 "Link to this heading")

```
 INSERT INTO table_name [ ( column [, ...] ) ]
{DEFAULT VALUES |
VALUES ( { expression | DEFAULT } [, ...] )
[, ( { expression | DEFAULT } [, ...] )
[, ...] ] |
query }
```

Copy

### Sample Source Patterns[¶](#id155 "Link to this heading")

#### **Setup data**[¶](#id156 "Link to this heading")

##### Redshift[¶](#id157 "Link to this heading")

```
 CREATE TABLE employees (
    id INTEGER IDENTITY(1,1),
    name VARCHAR(100),
    salary INT DEFAULT 20000,
    department VARCHAR(50) DEFAULT 'Marketing'
);

CREATE TABLE new_employees (
    name VARCHAR(100),
    salary INT,
    department VARCHAR(50)
);

INSERT INTO new_employees (name, salary, department)
VALUES
    ('Grace Lee', 32000, 'Operations'),
    ('Hannah Gray', 26000, 'Finance');
```

Copy

#### Default Values[¶](#default-values "Link to this heading")

It inserts a complete row with its default values. If any columns do not have default values, NULL values are inserted in those columns.

This clause cannot specify individual columns; it always inserts a complete row with its default values. Additionally, columns with the NOT NULL constraint cannot be included in the table definition. To replicate this behavior in Snowflake, SnowConvert AI insert a column with a DEFAULT value in the table. This action inserts a complete row, using the default value for every column.

##### Input Code:[¶](#id158 "Link to this heading")

##### Redshift[¶](#id159 "Link to this heading")

```
 CREATE TABLE employees (
    id INTEGER IDENTITY(1,1),
    name VARCHAR(100),
    salary INT DEFAULT 20000,
    department VARCHAR(50) DEFAULT 'Marketing'
);

INSERT INTO employees
DEFAULT VALUES;

SELECT * FROM employees ORDER BY id;
```

Copy

##### Result[¶](#id160 "Link to this heading")

| ID | NAME | SALARY | DEPARTMENT |
| --- | --- | --- | --- |
| 1 | NULL | 20000 | Marketing |

##### Output Code:[¶](#id161 "Link to this heading")

##### Snowflake[¶](#id162 "Link to this heading")

```
 CREATE TABLE employees (
    id INTEGER IDENTITY(1,1) ORDER,
    name VARCHAR(100),
    salary INT DEFAULT 20000,
    department VARCHAR(50) DEFAULT 'Marketing'
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}';

INSERT INTO employees (id)
VALUES (DEFAULT);

SELECT * FROM
    employees
ORDER BY id;
```

Copy

##### Result[¶](#id163 "Link to this heading")

| ID | NAME | SALARY | DEPARTMENT |
| --- | --- | --- | --- |
| 1 | NULL | 20000 | Marketing |

#### Query[¶](#query "Link to this heading")

Insert one or more rows into the table by using a query. All rows produced by the query will be inserted into the table. The query must return a column list that is compatible with the table’s columns, although the column names do not need to match. This functionality is fully equivalent in Snowflake.

##### Input Code:[¶](#id164 "Link to this heading")

##### Redshift[¶](#id165 "Link to this heading")

```
 INSERT INTO employees (name, salary, department)
SELECT name, salary, department FROM new_employees;
```

Copy

##### Result[¶](#id166 "Link to this heading")

| ID | NAME | SALARY | DEPARTMENT |
| --- | --- | --- | --- |
| 1 | Grace Lee | 32000 | Operations |
| 2 | Hannah Gray | 26000 | Finance |

##### Output Code:[¶](#id167 "Link to this heading")

##### Snowflake[¶](#id168 "Link to this heading")

```
 INSERT INTO employees (name, salary, department)
SELECT name, salary, department FROM
    new_employees;
```

Copy

##### Result[¶](#id169 "Link to this heading")

| ID | NAME | SALARY | DEPARTMENT |
| --- | --- | --- | --- |
| 1 | Grace Lee | 32000 | Operations |
| 2 | Hannah Gray | 26000 | Finance |

### Known Issues [¶](#id170 "Link to this heading")

* Certain expressions cannot be used in the VALUES clause in Snowflake. For example, in Redshift, the [JSON\_PARSE](https://docs.aws.amazon.com/redshift/latest/dg/JSON_PARSE.html) function can be used within the VALUES clause to insert a JSON value into a SUPER data type. In Snowflake, however, the [PARSE\_JSON](https://docs.snowflake.com/en/sql-reference/functions/parse_json) function cannot be used in the VALUES clause to insert a JSON value into a VARIANT data type. Instead, a query can be used in place of the VALUES clause. For more details, please refer to the [Snowflake documentation](https://docs.snowflake.com/en/sql-reference/sql/insert#usage-notes). You can also check the [following article](https://community.snowflake.com/s/article/Cannot-use-DATE-FROM-PARTS-function-inside-the-VALUES-clause) for further information.

### Related EWIs[¶](#id171 "Link to this heading")

There are no known issues.

## MERGE[¶](#merge "Link to this heading")

### Grammar Syntax[¶](#id172 "Link to this heading")

```
 MERGE INTO target_table 
USING source_table [ [ AS ] alias ] 
ON match_condition 
[ WHEN MATCHED THEN { UPDATE SET col_name = { expr } [,...] | DELETE }
WHEN NOT MATCHED THEN INSERT [ ( col_name [,...] ) ] VALUES ( { expr } [, ...] ) |
REMOVE DUPLICATES ]
```

Copy

For more information please refer to Redshift [MERGE documentation](https://docs.aws.amazon.com/redshift/latest/dg/r_MERGE.html).

### Sample Source Patterns[¶](#id173 "Link to this heading")

#### UPDATE - INSERT[¶](#update-insert "Link to this heading")

There are no differences between both languages. The code is kept in its original form.

##### Input Code:[¶](#id174 "Link to this heading")

##### Redshift[¶](#id175 "Link to this heading")

```
 MERGE INTO target USING source ON target.id = source.id
WHEN MATCHED THEN UPDATE SET id = source.id, name = source.name
WHEN NOT MATCHED THEN INSERT VALUES (source.id, source.name);
```

Copy

##### Output Code:[¶](#id176 "Link to this heading")

##### Snowflake[¶](#id177 "Link to this heading")

```
 --** SSC-FDM-RS0005 - REDSHIFT MERGE STATEMENT DOESN'T ALLOW DUPLICATES IN THE SOURCE TABLE. SNOWFLAKE BEHAVIOR MAY DIFFER IF THERE ARE DUPLICATE VALUES. **
MERGE INTO target USING source ON target.id = source.id
WHEN MATCHED THEN UPDATE SET id = source.id, name = source.name
WHEN NOT MATCHED THEN INSERT VALUES (source.id, source.name);
```

Copy

#### DELETE - INSERT[¶](#delete-insert "Link to this heading")

There are no differences between both languages. The code is kept in its original form.

##### Input Code:[¶](#id178 "Link to this heading")

##### Redshift[¶](#id179 "Link to this heading")

```
 MERGE INTO target USING source ON target.id = source.id
WHEN MATCHED THEN DELETE
WHEN NOT MATCHED THEN INSERT VALUES (source.id, source.name);
```

Copy

##### Output Code:[¶](#id180 "Link to this heading")

##### Snowflake[¶](#id181 "Link to this heading")

```
 --** SSC-FDM-RS0005 - REDSHIFT MERGE STATEMENT DOESN'T ALLOW DUPLICATES IN THE SOURCE TABLE. SNOWFLAKE BEHAVIOR MAY DIFFER IF THERE ARE DUPLICATE VALUES. **
MERGE INTO target USING source ON target.id = source.id
WHEN MATCHED THEN DELETE
WHEN NOT MATCHED THEN INSERT VALUES (source.id, source.name);
```

Copy

#### REMOVE DUPLICATES[¶](#remove-duplicates "Link to this heading")

The REMOVE DUPLICATES clause is not supported in Snowflake, however, there is a workaround that could emulate the original behavior.

The output code will have three new statements:

* A TEMPORARY TABLE with the duplicate values from the source and target table that matches the condition
* An INSERT statement that adds the pending values to the target table after the merge
* A DROP statement that drops the generated temporary table.

These are necessary since the DROP DUPLICATES behavior removes the duplicate values from the target table and then inserts the values that match the condition from the source table.

##### Input Code:[¶](#id182 "Link to this heading")

##### Redshift[¶](#id183 "Link to this heading")

```
 CREATE TABLE target (id INT, name CHAR(10));
CREATE TABLE source (id INT, name CHAR(10));

INSERT INTO target VALUES (30, 'Tony'), (30, 'Daisy'), (11, 'Alice'), (23, 'Bill'), (23, 'Nikki');
INSERT INTO source VALUES (23, 'David'), (22, 'Clarence');

MERGE INTO target USING source ON target.id = source.id REMOVE DUPLICATES;
```

Copy

##### Results[¶](#results "Link to this heading")

| ID | NAME |
| --- | --- |
| 30 | Daisy |
| 22 | Clarence |
| 30 | Tony |
| 11 | Alice |
| 23 | David |

##### Output Code:[¶](#id184 "Link to this heading")

##### Snowflake[¶](#id185 "Link to this heading")

```
 CREATE TABLE target (id INT, name CHAR(10))
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}';

CREATE TABLE source (id INT, name CHAR(10))
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}';

INSERT INTO target
VALUES (30, 'Tony'), (30, 'Daisy'), (11, 'Alice'), (23, 'Bill'), (23, 'Nikki');

INSERT INTO source
VALUES (23, 'David'), (22, 'Clarence');

CREATE TEMPORARY TABLE source_duplicates AS
SELECT DISTINCT
source.*
FROM
source
INNER JOIN
target
ON target.id = source.id;
--** SSC-FDM-RS0005 - REDSHIFT MERGE STATEMENT DOESN'T ALLOW DUPLICATES IN THE SOURCE TABLE. SNOWFLAKE BEHAVIOR MAY DIFFER IF THERE ARE DUPLICATE VALUES. **
MERGE INTO target
USING source ON target.id = source.id
WHEN MATCHED THEN
DELETE
WHEN NOT MATCHED THEN
INSERT
VALUES (source.id, source.name);
INSERT INTO target

SELECT
*
FROM
source_duplicates;

DROP TABLE IF EXISTS source_duplicates CASCADE;
```

Copy

##### Results[¶](#id186 "Link to this heading")

| ID | NAME |
| --- | --- |
| 22 | Clarence |
| 30 | Tony |
| 30 | Daisy |
| 11 | Alice |
| 23 | David |

### Known Issues[¶](#id187 "Link to this heading")

There are no known issues.

### Related EWIs[¶](#id188 "Link to this heading")

1. [SSC-EWI-RS0009](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/redshiftEWI.html#ssc-ewi-rs0009): Semantic information not found for the source table.
2. [SSC-FDM-RS0005](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/redshiftFDM.html#ssc-fdm-rs0005): Duplicates not allowed in source table.

## UPDATE[¶](#update "Link to this heading")

### Description[¶](#id189 "Link to this heading")

> Updates values in one or more table columns when a condition is satisfied. ([Redshift SQL Language Reference Update Statement](https://docs.aws.amazon.com/redshift/latest/dg/r_UPDATE.html)).

Note

This syntax is fully supported in Snowflake.

### Grammar Syntax[¶](#id190 "Link to this heading")

```
 [ WITH [RECURSIVE] common_table_expression [, common_table_expression , ...] ]
            UPDATE table_name [ [ AS ] alias ] SET column = { expression | DEFAULT } [,...]

[ FROM fromlist ]
[ WHERE condition ]
```

Copy

### Sample Source Patterns[¶](#id191 "Link to this heading")

#### **Setup data**[¶](#id192 "Link to this heading")

##### Redshift[¶](#id193 "Link to this heading")

```
 CREATE TABLE employees (
    id INTEGER IDENTITY(1,1),
    name VARCHAR(100),
    salary DECIMAL DEFAULT 20000,
    department VARCHAR(50) DEFAULT 'Marketing'
);

INSERT INTO employees (name, salary, department)
VALUES
    ('Alice', 500000, 'HR'),
    ('Bob', 600000, 'Engineering'),
    ('Charlie', 700000, 'Engineering'),
    ('David', 400000, 'Marketing'),
    ('Eve', 450000, 'HR'),
    ('Frank', 750000, 'Engineering'),
    ('Grace', 650000, 'Engineering'),
    ('Helen', 390000, 'Marketing'),
    ('Ivy', 480000, 'HR'),
    ('Jack', 420000, 'Engineering'),
    ('Ken', 700000, 'Marketing'),
    ('Liam', 600000, 'Engineering'),
    ('Mona', 470000, 'HR');

CREATE TABLE department_bonus (
    department VARCHAR(100),
    bonus DECIMAL
);

INSERT INTO department_bonus (department, bonus)
VALUES
    ('HR', 10000),
    ('Engineering', 50000),
    ('Marketing', 20000),
    ('Sales', 5000);
```

Copy

#### Alias[¶](#alias "Link to this heading")

Although Snowflake’s grammar does not specify that a table alias can be used, it’s valid code in Snowflake.

##### Input Code:[¶](#id194 "Link to this heading")

##### Redshift[¶](#id195 "Link to this heading")

```
 UPDATE employees AS e
SET salary = salary + 5000
WHERE e.salary < 600000;
```

Copy

##### Result[¶](#id196 "Link to this heading")

| ID | NAME | SALARY | DEPARTMENT |
| --- | --- | --- | --- |
| 1 | Alice | 505000 | HR |
| 2 | Bob | 600000 | Engineering |
| 3 | Charlie | 700000 | Engineering |
| 4 | David | 405000 | Marketing |
| 5 | Eve | 455000 | HR |
| 6 | Frank | 750000 | Engineering |
| 7 | Grace | 650000 | Engineering |
| 8 | Helen | 395000 | Marketing |
| 9 | Ivy | 485000 | HR |
| 10 | Jack | 425000 | Engineering |
| 11 | Ken | 700000 | Marketing |
| 12 | Liam | 600000 | Engineering |
| 13 | Mona | 475000 | HR |

##### Output Code:[¶](#id197 "Link to this heading")

##### Snowflake[¶](#id198 "Link to this heading")

```
 UPDATE employees AS e
SET salary = salary + 5000
WHERE e.salary < 600000;
```

Copy

##### Result[¶](#id199 "Link to this heading")

| ID | NAME | SALARY | DEPARTMENT |
| --- | --- | --- | --- |
| 1 | Alice | 505000 | HR |
| 2 | Bob | 600000 | Engineering |
| 3 | Charlie | 700000 | Engineering |
| 4 | David | 405000 | Marketing |
| 5 | Eve | 455000 | HR |
| 6 | Frank | 750000 | Engineering |
| 7 | Grace | 650000 | Engineering |
| 8 | Helen | 395000 | Marketing |
| 9 | Ivy | 485000 | HR |
| 10 | Jack | 425000 | Engineering |
| 11 | Ken | 700000 | Marketing |
| 12 | Liam | 600000 | Engineering |
| 13 | Mona | 475000 | HR |

#### WITH clause[¶](#id200 "Link to this heading")

This clause specifies one or more Common Table Expressions (CTE). The output column names are optional for non-recursive CTEs, but mandatory for recursive ones.

Since this clause cannot be used in an UPDATE statement, it is transformed into temporary tables with their corresponding queries. After the UPDATE statement is executed, these temporary tables are dropped to clean up, release resources, and avoid name collisions when creating tables within the same session. Additionally, if a regular table with the same name exists, it will take precedence again, since the temporary table [has priority](https://docs.snowflake.com/en/user-guide/tables-temp-transient#potential-naming-conflicts-with-other-table-types) over any other table with the same name in the same session.

##### Non-Recursive CTE[¶](#id201 "Link to this heading")

##### Input Code:[¶](#id202 "Link to this heading")

##### Redshift[¶](#id203 "Link to this heading")

```
 WITH avg_salary_cte AS (
    SELECT AVG(salary) AS avg_salary FROM employees
)
UPDATE employees
SET salary = (SELECT avg_salary FROM avg_salary_cte)
WHERE salary < 500000;
```

Copy

##### Result[¶](#id204 "Link to this heading")

| ID | NAME | SALARY | DEPARTMENT |
| --- | --- | --- | --- |
| 1 | Alice | 500000 | HR |
| 2 | Bob | 600000 | Engineering |
| 3 | Charlie | 700000 | Engineering |
| 4 | David | 546923 | Marketing |
| 5 | Eve | 546923 | HR |
| 6 | Frank | 750000 | Engineering |
| 7 | Grace | 650000 | Engineering |
| 8 | Helen | 546923 | Marketing |
| 9 | Ivy | 546923 | HR |
| 10 | Jack | 546923 | Engineering |
| 11 | Ken | 700000 | Marketing |
| 12 | Liam | 600000 | Engineering |
| 13 | Mona | 546923 | HR |

##### Output Code:[¶](#id205 "Link to this heading")

##### Snowflake[¶](#id206 "Link to this heading")

```
 CREATE TEMPORARY TABLE avg_salary_cte AS
SELECT AVG(salary) AS avg_salary FROM
employees;

UPDATE employees
SET salary = (SELECT avg_salary FROM
      avg_salary_cte
)
WHERE salary < 500000;

DROP TABLE avg_salary_cte;
```

Copy

##### Result[¶](#id207 "Link to this heading")

| ID | NAME | SALARY | DEPARTMENT |
| --- | --- | --- | --- |
| 1 | Alice | 500000 | HR |
| 2 | Bob | 600000 | Engineering |
| 3 | Charlie | 700000 | Engineering |
| 4 | David | 546923 | Marketing |
| 5 | Eve | 546923 | HR |
| 6 | Frank | 750000 | Engineering |
| 7 | Grace | 650000 | Engineering |
| 8 | Helen | 546923 | Marketing |
| 9 | Ivy | 546923 | HR |
| 10 | Jack | 546923 | Engineering |
| 11 | Ken | 700000 | Marketing |
| 12 | Liam | 600000 | Engineering |
| 13 | Mona | 546923 | HR |

##### Recursive CTE[¶](#id208 "Link to this heading")

##### Input Code:[¶](#id209 "Link to this heading")

##### Redshift[¶](#id210 "Link to this heading")

```
 WITH RECURSIVE bonus_updates(id, name, department, salary, level) AS (
    SELECT e.id,
           e.name,
           e.department,
           e.salary + CASE
                          WHEN db.bonus IS NOT NULL THEN db.bonus
                          ELSE 0
               END AS new_salary,
           1 AS level
    FROM employees e
    LEFT JOIN department_bonus db ON e.department = db.department
    UNION ALL
    SELECT e.id,
           e.name,
           e.department,
           e.salary + CASE
                          WHEN db.bonus IS NOT NULL THEN db.bonus
                          ELSE 0
               END + (e.salary * 0.05) AS new_salary,
           bu.level + 1
    FROM employees e
    JOIN department_bonus db ON e.department = db.department
    JOIN bonus_updates bu ON e.id = bu.id
    WHERE bu.level < 3
)
UPDATE employees
SET salary = bu.new_salary
FROM (SELECT id, AVG(salary) as new_salary FROM bonus_updates GROUP BY id) as bu
WHERE employees.id = bu.id
  AND bu.new_salary > employees.salary;
```

Copy

##### Result[¶](#id211 "Link to this heading")

| ID | NAME | SALARY | DEPARTMENT |
| --- | --- | --- | --- |
| 1 | Alice | 526666 | HR |
| 2 | Bob | 670000 | Engineering |
| 3 | Charlie | 773333 | Engineering |
| 4 | David | 433333 | Marketing |
| 5 | Eve | 475000 | HR |
| 6 | Frank | 825000 | Engineering |
| 7 | Grace | 721666 | Engineering |
| 8 | Helen | 423000 | Marketing |
| 9 | Ivy | 506000 | HR |
| 10 | Jack | 484000 | Engineering |
| 11 | Ken | 743333 | Marketing |
| 12 | Liam | 670000 | Engineering |
| 13 | Mona | 495668 | HR |

##### Output Code:[¶](#id212 "Link to this heading")

##### Snowflake[¶](#id213 "Link to this heading")

```
 CREATE TEMPORARY TABLE bonus_updates AS
  --** SSC-FDM-0007 - MISSING DEPENDENT OBJECTS "employees", "department_bonus" **
 WITH RECURSIVE bonus_updates(id, name, department, salary, level) AS (
     SELECT e.id,
            e.name,
            e.department,
            e.salary + CASE
                           WHEN db.bonus IS NOT NULL THEN db.bonus
                           ELSE 0
                END AS new_salary,
            1 AS level
     FROM
            employees e
     LEFT JOIN
                           department_bonus db ON e.department = db.department
     UNION ALL
     SELECT e.id,
            e.name,
            e.department,
            e.salary + CASE
                           WHEN db.bonus IS NOT NULL THEN db.bonus
                           ELSE 0
                END + (e.salary * 0.05) AS new_salary,
            bu.level + 1
     FROM
            employees e
     JOIN
                           department_bonus db ON e.department = db.department
     JOIN
                           bonus_updates bu ON e.id = bu.id
     WHERE bu.level < 3
 )
 SELECT
     id,
     name,
     department,
     salary,
     level
 FROM
     bonus_updates;
     
UPDATE employees
SET salary = bu.new_salary
FROM (SELECT id, AVG(salary) as new_salary 
FROM bonus_updates 
GROUP BY id) as bu
WHERE employees.id = bu.id
  AND bu.new_salary > employees.salary;
 
DROP TABLE bonus_updates;
```

Copy

##### Result[¶](#id214 "Link to this heading")

| ID | NAME | SALARY | DEPARTMENT |
| --- | --- | --- | --- |
| 1 | Alice | 526667 | HR |
| 2 | Bob | 670000 | Engineering |
| 3 | Charlie | 773333 | Engineering |
| 4 | David | 433333 | Marketing |
| 5 | Eve | 475000 | HR |
| 6 | Frank | 825000 | Engineering |
| 7 | Grace | 721667 | Engineering |
| 8 | Helen | 423000 | Marketing |
| 9 | Ivy | 506000 | HR |
| 10 | Jack | 484000 | Engineering |
| 11 | Ken | 743333 | Marketing |
| 12 | Liam | 670000 | Engineering |
| 13 | Mona | 495667 | HR |

#### SET DEFAULT values[¶](#set-default-values "Link to this heading")

##### Input Code:[¶](#id215 "Link to this heading")

##### Redshift[¶](#id216 "Link to this heading")

```
 UPDATE employees
SET salary = DEFAULT, department = 'Sales'
WHERE department = 'HR';
```

Copy

##### Result[¶](#id217 "Link to this heading")

| ID | NAME | SALARY | DEPARTMENT |
| --- | --- | --- | --- |
| 1 | Alice | 20000 | Sales |
| 2 | Bob | 600000 | Engineering |
| 3 | Charlie | 700000 | Engineering |
| 4 | David | 400000 | Marketing |
| 5 | Eve | 20000 | Sales |
| 6 | Frank | 750000 | Engineering |
| 7 | Grace | 650000 | Engineering |
| 8 | Helen | 390000 | Marketing |
| 9 | Ivy | 20000 | Sales |
| 10 | Jack | 420000 | Engineering |
| 11 | Ken | 700000 | Marketing |
| 12 | Liam | 600000 | Engineering |
| 13 | Mona | 20000 | Sales |

##### Output Code:[¶](#id218 "Link to this heading")

##### Snowflake[¶](#id219 "Link to this heading")

```
 UPDATE employees
SET salary = DEFAULT, department = 'Sales'
WHERE
    department = 'HR';
```

Copy

##### Result[¶](#id220 "Link to this heading")

| ID | NAME | SALARY | DEPARTMENT |
| --- | --- | --- | --- |
| 1 | Alice | 20000 | Sales |
| 2 | Bob | 600000 | Engineering |
| 3 | Charlie | 700000 | Engineering |
| 4 | David | 400000 | Marketing |
| 5 | Eve | 20000 | Sales |
| 6 | Frank | 750000 | Engineering |
| 7 | Grace | 650000 | Engineering |
| 8 | Helen | 390000 | Marketing |
| 9 | Ivy | 20000 | Sales |
| 10 | Jack | 420000 | Engineering |
| 11 | Ken | 700000 | Marketing |
| 12 | Liam | 600000 | Engineering |
| 13 | Mona | 20000 | Sales |

#### SET clause[¶](#set-clause "Link to this heading")

It is responsible for modifying values in the columns. Similar to Snowflake, update queries with multiple matches per row will throw an error when the configuration parameter [ERROR\_ON\_NONDETERMINISTIC\_UPDATE](https://docs.aws.amazon.com/redshift/latest/dg/r_error_on_nondeterministic_update.html) is set to true. This flag works the same way in Snowflake, and it even uses the same name, [ERROR\_ON\_NONDETERMINISTIC\_UPDATE](https://docs.snowflake.com/en/sql-reference/parameters#label-error-on-nondeterministic-update).

However, when this flag is turned off, no error is returned, and one of the matched rows is used to update the target row. The selected joined row is nondeterministic and arbitrary in both languages; the behavior may not be consistent across executions, which could lead to data inconsistencies.

##### Setup data:[¶](#id221 "Link to this heading")

##### Redshift[¶](#id222 "Link to this heading")

```
 CREATE TABLE target (
  k INT,
  v INT
);

CREATE TABLE src (
  k INT,
  v INT
);

INSERT INTO target (k, v) VALUES (0, 10);

INSERT INTO src (k, v) VALUES
  (0, 14),
  (0, 15),
  (0, 16);
```

Copy

##### Input Code:[¶](#id223 "Link to this heading")

##### Redshift[¶](#id224 "Link to this heading")

```
 UPDATE target
  SET v = src.v
  FROM src
  WHERE target.k = src.k;


SELECT * FROM target;
```

Copy

##### Result[¶](#id225 "Link to this heading")

| K | V |
| --- | --- |
| 0 | 16 |

##### Output Code:[¶](#id226 "Link to this heading")

##### Snowflake[¶](#id227 "Link to this heading")

```
 UPDATE target
  SET v = src.v
  FROM src
  WHERE target.k = src.k;


SELECT * FROM target;
```

Copy

##### Result[¶](#id228 "Link to this heading")

| K | V |
| --- | --- |
| 0 | 14 |

### Known Issues [¶](#id229 "Link to this heading")

* Update queries with multiple matches per row may cause data inconsistencies. Although both platforms have the flag [ERROR\_ON\_NONDETERMINISTIC\_UPDATE](https://docs.aws.amazon.com/redshift/latest/dg/r_error_on_nondeterministic_update.html), these values will always be nondeterministic. Snowflake offers recommendations for handling these scenarios. Click [here](https://docs.snowflake.com/en/sql-reference/sql/update#examples) for more details.
* Replicating the functionality of the `WITH` clause requires creating temporary tables mirroring each Common Table Expression (CTE). However, this approach fails if a temporary table with the same name already exists within the current session, causing an error.

### Related EWIs[¶](#id230 "Link to this heading")

There are no known issues.

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

1. [CALL](#call)
2. [CREATE DATABASE](#create-database)
3. [CREATE EXTERNAL TABLE](#create-external-table)
4. [CREATE MATERIALIZED VIEW](#create-materialized-view)
5. [CREATE SCHEMA](#create-schema)
6. [CREATE FUNCTION](#create-function)
7. [CREATE VIEW](#create-view)
8. [DELETE](#delete)
9. [EXECUTE](#execute)
10. [INSERT](#insert)
11. [MERGE](#merge)
12. [UPDATE](#update)