---
description: Translation reference for all the supported statements by SnowConvert AI for Redshift.
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/redshift/redshift-sql-statements
title: SnowConvert AI - Redshift - SQL Statements | Snowflake Documentation
---

## CALL[¶](#call)

### Description[¶](#description)

> Runs a stored procedure. The CALL command must include the procedure name and the input argument
> values. You must call a stored procedure by using the CALL statement.
> ([Redshift SQL Language Reference CALL](https://docs.aws.amazon.com/redshift/latest/dg/r_CALL_procedure.html)).

### Grammar Syntax[¶](#grammar-syntax)

```
 CALL sp_name ( [ argument ] [, ...] )
```

Copy

### Sample Source Patterns[¶](#sample-source-patterns)

#### Base scenario[¶](#base-scenario)

##### Input Code:[¶](#input-code)

##### Redshift[¶](#redshift)

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

##### Output Code:[¶](#output-code)

##### Redshift[¶](#id1)

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

#### Call using Output Parameters Mode (INOUT, OUT)[¶](#call-using-output-parameters-mode-inout-out)

##### Input Code:[¶](#id2)

##### Redshift[¶](#id3)

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

##### Output Code:[¶](#id4)

##### Redshift[¶](#id5)

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

### Known Issues[¶](#known-issues)

- Output parameters from calls outside procedures won’t work.

### Related EWIs.[¶](#related-ewis)

1. [SSC-EWI-0073](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0073):
   Pending Functional Equivalence Review

## CREATE DATABASE[¶](#create-database)

### Grammar Syntax[¶](#id6)

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

For more information please refer to Redshift
[`CREATE DATABASE` documentation](https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_DATABASE.html).

### Sample Source Patterns[¶](#id7)

#### Basic samples[¶](#basic-samples)

##### Input Code:[¶](#id8)

##### Redshift[¶](#id9)

```
 CREATE DATABASE database_name;
```

Copy

##### Output Code:[¶](#id10)

##### Snowflake[¶](#snowflake)

```
 CREATE DATABASE IF NOT EXISTS database_name
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/25/2024" }}';
```

Copy

#### Collate Clause[¶](#collate-clause)

##### Input Code:[¶](#id11)

##### Redshift[¶](#id12)

```
 CREATE DATABASE database_collate
COLLATE CASE_INSENSITIVE;
```

Copy

##### Output Code:[¶](#id13)

##### Snowflake[¶](#id14)

```
 CREATE DATABASE IF NOT EXISTS database_collate
DEFAULT_DDL_COLLATION='en-ci'
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/24/2024" }}';
```

Copy

#### Connection Limit Clause[¶](#connection-limit-clause)

##### Input Code:[¶](#id15)

##### Redshift[¶](#id16)

```
 CREATE DATABASE database_connection
CONNECTION LIMIT UNLIMITED;
```

Copy

##### Output Code:[¶](#id17)

##### Snowflake[¶](#id18)

```
 CREATE DATABASE IF NOT EXISTS database_connection
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/24/2024" }}';
```

Copy

Warning

The connection limit clause is removed since the connection concurrency in snowflake is managed by
warehouse. More information
[here](https://docs.snowflake.com/en/sql-reference/parameters#label-max-concurrency-level).

#### From ARN Clause[¶](#from-arn-clause)

##### Input Code:[¶](#id19)

##### Redshift[¶](#id20)

```
 CREATE DATABASE database_fromARN
FROM ARN 'arn' WITH NO DATA CATALOG SCHEMA IAM_ROLE 'arn:aws:iam::<account-id>:role/<role-name';
```

Copy

##### Output Code:[¶](#id21)

##### Snowflake[¶](#id22)

```
 CREATE DATABASE IF NOT EXISTS database_fromARN
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/24/2024" }}';
```

Copy

Warning

This clause is removed since it is used to reference
[Amazon Resources](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference-arns.html), not valid
in Snowflake.

#### From Datashare Clause[¶](#from-datashare-clause)

##### Input Code[¶](#id23)

##### Redshift[¶](#id24)

```
 CREATE DATABASE database_fromDatashare
FROM DATASHARE datashare_name OF NAMESPACE 'namespace_guid';
```

Copy

##### Output Code[¶](#id25)

##### Snowflake[¶](#id26)

```
 CREATE DATABASE IF NOT EXISTS  database_fromDatashare
FROM DATASHARE datashare_name OF NAMESPACE 'namespace_guid' !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'FromDatashareAttribute' NODE ***/!!!
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/24/2024" }}';
```

Copy

Note

The transformation for Datashare is planned to be delivered in the future.

#### Owner Clause[¶](#owner-clause)

##### Input Code[¶](#id27)

##### Redshift[¶](#id28)

```
 CREATE DATABASE database_Owner
OWNER db_owner
ENCODING 'encoding';
```

Copy

##### Output Code[¶](#id29)

##### Snowflake[¶](#id30)

```
 CREATE DATABASE IF NOT EXISTS database_Owner
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/24/2024" }}';
```

Copy

Warning

Please be aware that for this case, the owner clause is removed from the code since Snowflake
databases are owned by roles, not individual users. For more information please refer to
[Snowflake `GRANT OWNERSHIP` documentation](https://docs.snowflake.com/en/sql-reference/sql/grant-ownership).

#### Isolation Level Clause[¶](#isolation-level-clause)

##### Input Code[¶](#id31)

##### Redshift[¶](#id32)

```
 CREATE DATABASE database_Isolation
ISOLATION LEVEL SNAPSHOT;
```

Copy

##### Output Code[¶](#id33)

##### Snowflake[¶](#id34)

```
 CREATE DATABASE IF NOT EXISTS database_Isolation
ISOLATION LEVEL SNAPSHOT !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'IsolationLevelAttribute' NODE ***/!!!
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/24/2024" }}';
```

Copy

Note

The transformation for Isolation Level is planned to be delivered in the future.

### Related EWIs[¶](#id35)

- [SSC-EWI-0073](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0073):
  Pending Functional Equivalence Review

## CREATE EXTERNAL TABLE[¶](#create-external-table)

### Description [¶](#id36)

Currently SnowConvert AI is transforming `CREATE EXTERNAL TABLES` to regular tables, that implies
additional effort because data stored in external RedShift tables must be transferred to the
Snowflake database.

### Grammar Syntax [¶](#id37)

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

Click [here](https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_EXTERNAL_TABLE.html) to go to
the specification for this syntax.

### Sample Source Patterns[¶](#id38)

#### Input Code:[¶](#id39)

##### Redshift[¶](#id40)

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

##### Output Code:[¶](#id41)

##### Snowflake[¶](#id42)

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

#### Create External Table AS[¶](#create-external-table-as)

##### Input Code:[¶](#id43)

##### Redshift[¶](#id44)

```
 CREATE EXTERNAL TABLE spectrum.partitioned_lineitem
PARTITIONED BY (l_shipdate, l_shipmode)
STORED AS parquet
LOCATION 'S3://amzn-s3-demo-bucket/cetas/partitioned_lineitem/'
AS SELECT l_orderkey, l_shipmode, l_shipdate, l_partkey FROM local_table;
```

Copy

##### Output Code:[¶](#id45)

##### Snowflake[¶](#id46)

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

### Recommendations[¶](#recommendations)

- For the usage of Create External Table in Snowflake you may refer to
  [Snowflake’s documentation.](https://docs.snowflake.com/en/sql-reference/sql/create-external-table)

### Related EWIs[¶](#id47)

1. [SSC-FDM-0004](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0004):
   External table translated to regular table

## CREATE MATERIALIZED VIEW[¶](#create-materialized-view)

### Description[¶](#id48)

In SnowConvert AI, Redshift Materialized Views are transformed into Snowflake Dynamic Tables. To
properly configure Dynamic Tables, two essential parameters must be defined: TARGET_LAG and
WAREHOUSE. If these parameters are left unspecified in the configuration options, SnowConvert AI
will default to preassigned values during the conversion, as demonstrated in the example below.

For more information on Materialized Views, click
[here](https://docs.aws.amazon.com/redshift/latest/dg/materialized-view-create-sql-command.html).

For details on the necessary parameters for Dynamic Tables, click
[here](https://docs.snowflake.com/en/sql-reference/sql/create-dynamic-table).

### Grammar Syntax[¶](#id49)

The following is the SQL syntax to create a view in Amazon Redshift. Click
[here](https://docs.aws.amazon.com/redshift/latest/dg/materialized-view-create-sql-command.html) to
here to go to Redshifts specification for this syntax.

```
 CREATE MATERIALIZED VIEW mv_name
[ BACKUP { YES | NO } ]
[ table_attributes ]
[ AUTO REFRESH { YES | NO } ]
AS query
```

Copy

### Sample Source Patterns[¶](#id50)

#### Input Code:[¶](#id51)

##### Redshift[¶](#id52)

```
 CREATE MATERIALIZED VIEW mv_baseball AS
SELECT ball AS baseball FROM baseball_table;
```

Copy

##### Output Code:[¶](#id53)

##### Snowflake[¶](#id54)

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

- [Sortkey](redshift-sql-statements-create-table.html#sortkey)
- [DistKey](redshift-sql-statements-create-table.html#distkey)
- [DistStyle](redshift-sql-statements-create-table.html#diststyle)

Warning

The BACKUP and AUTO REFRESH clauses are deleted since they are not applicable in a Snowflake’s
Dynamic Table

### Related Ewis[¶](#id55)

- [SSC-FDM-0031](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0031):
  Dynamic Table required parameters set by default

## CREATE SCHEMA[¶](#create-schema)

### Grammar Syntax[¶](#id56)

```
 CREATE SCHEMA [ IF NOT EXISTS ] schema_name [ AUTHORIZATION username ]
           [ QUOTA {quota [MB | GB | TB] | UNLIMITED} ] [ schema_element [ ... ]

CREATE SCHEMA AUTHORIZATION username [ QUOTA {quota [MB | GB | TB] | UNLIMITED} ]
[ schema_element [ ... ] ]
```

Copy

For more information please refer to
[Redshift `CREATE SCHEMA` documentation](https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_SCHEMA.html).

### Sample Source Patterns[¶](#id57)

#### Basic samples[¶](#id58)

##### Input Code:[¶](#id59)

##### Redshift[¶](#id60)

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

##### Output Code:[¶](#id61)

##### Snowflake[¶](#id62)

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

#### Authorization Clause[¶](#authorization-clause)

##### Input Code:[¶](#id63)

##### Redshift[¶](#id64)

```
 CREATE SCHEMA s1 AUTHORIZATION miller;
```

Copy

##### Output Code:[¶](#id65)

##### Snowflake[¶](#id66)

```
 CREATE SCHEMA IF NOT EXISTS s1
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/23/2024" }}'
;
```

Copy

Warning

Please be aware that for this case, the authorization clause is removed from the code since
Snowflake schemas are owned by roles, not individual users. For more information please refer to
[Snowflake `GRANT OWNERSHIP` documentation](https://docs.snowflake.com/en/sql-reference/sql/grant-ownership).

#### Quota Clause[¶](#quota-clause)

##### Input Code:[¶](#id67)

##### Redshift[¶](#id68)

```
 CREATE SCHEMA s1 QUOTA UNLIMITED;

CREATE SCHEMA s2 QUOTA 10 TB;
```

Copy

##### Output Code:[¶](#id69)

##### Snowflake[¶](#id70)

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

In Snowflake is not allowed to define a quota per scheme. Storage management is done at the account
and warehouse level, and Snowflake handles it automatically. For this reason it is removed from the
code.

#### Create Schema Authorization[¶](#create-schema-authorization)

In Redshift when the schema name is not specified but the authorization clause is defined, a new
schema is created with the owner’s name. For this reason this behavior is replicated in Snowflake.

##### Input Code:[¶](#id71)

##### Redshift[¶](#id72)

```
 CREATE SCHEMA AUTHORIZATION miller;
```

Copy

##### Output Code:[¶](#id73)

##### Snowflake[¶](#id74)

```
 CREATE SCHEMA IF NOT EXISTS miller
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/23/2024" }}'
;
```

Copy

### Related EWIs[¶](#id75)

There are no known issues.

## CREATE FUNCTION[¶](#create-function)

### Description[¶](#id76)

This command defines a user-defined function (UDF) within the database. These functions encapsulate
reusable logic that can be invoked within SQL queries.

### Grammar Syntax[¶](#id77)

The following is the SQL syntax to create a view in Amazon Redshift. Click
[here](https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_VIEW.html) to here to go to Redshifts
specification for this syntax.

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

### SQL Language[¶](#sql-language)

#### Volatility category[¶](#volatility-category)

In Snowflake, `VOLATILE` and `IMMUTABLE` function volatility are functionally equivalent. Given that
`STABLE` is inherently transformed to the default `VOLATILE` behavior, explicit use of `STABLE` will
be delete.

##### Input Code:[¶](#id78)

##### Redshift[¶](#id79)

```
 CREATE OR REPLACE FUNCTION get_sale(INTEGER)
RETURNS FLOAT
STABLE
AS $$
SELECT price FROM sales where id = $1
$$ LANGUAGE SQL;
```

Copy

##### Output Code:[¶](#id80)

##### Snowflake[¶](#id81)

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

### Python Language[¶](#python-language)

Within the SnowConvert AI scope, the Python language for `CREATE FUNCTION` statements is not
supported. Consequently, the language `plpythonu` will be flagged with an EWI (SSC-EWI-0073), and
its body could appear with parsing errors.

#### Input Code:[¶](#id82)

##### Redshift[¶](#id83)

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

##### Output Code:[¶](#id84)

##### Snowflake[¶](#id85)

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

### Related EWIs[¶](#id86)

There are no known issues.

## CREATE VIEW[¶](#create-view)

### Description[¶](#id87)

This command creates a view in a database, which is run every time the view is referenced in a
query. Using the WITH NO SCHEMA BINDING clause, you can create views to an external table or objects
that don’t exist yet. This clause, however, requires you to specify the qualified name of the object
or table that you are referencing.

### Grammar Syntax[¶](#id88)

The following is the SQL syntax to create a view in Amazon Redshift. Click
[here](https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_VIEW.html) to here to go to Redshifts
specification for this syntax.

```
 CREATE [ OR REPLACE ] VIEW name [ ( column_name [, ...] ) ] AS query
[ WITH NO SCHEMA BINDING ]
```

Copy

### Sample Source Patterns[¶](#id89)

Considering the obligatory and optional clauses in Redshifts command, the output after migration to
Snowflake is very similar.

#### Input Code:[¶](#id90)

##### Redshift[¶](#id91)

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

##### Output Code:[¶](#id92)

##### Snowflake[¶](#id93)

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

There are some exceptions, however, of one unsupported clause from Redshift, therefore an EWI was
implemented to cover this case.

### Related EWIs[¶](#id94)

- [SSC-EWI-RS0003](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/redshiftEWI.html#ssc-ewi-rs0003):
  With no schema binding statement is not supported in Snowflake.

## DELETE[¶](#delete)

### Description[¶](#id95)

> Deletes rows from tables.
> ([Redshift SQL Language Reference Delete Statement](https://docs.aws.amazon.com/redshift/latest/dg/r_DELETE.html)).

Note

This syntax is fully supported in Snowflake.

### Grammar Syntax[¶](#id96)

```
 [ WITH [RECURSIVE] common_table_expression [, common_table_expression , ...] ]
DELETE [ FROM ] { table_name | materialized_view_name }
    [ USING table_name, ... ]
    [ WHERE condition ]
```

Copy

### Sample Source Patterns[¶](#id97)

#### **Setup data**[¶](#setup-data)

##### Redshift[¶](#id98)

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

#### From Clause[¶](#from-clause)

Update a table by referencing information from other tables. In Redshift, the FROM keyword is
optional, but in Snowflake, it is mandatory. Therefore, it will be added in cases where it’s
missing.

##### Input Code:[¶](#id99)

##### Redshift[¶](#id100)

```
 DELETE employees;

SELECT * FROM employees ORDER BY id;
```

Copy

##### Result[¶](#result)

<!-- prettier-ignore -->
|ID|NAME|DEPARTMENT|MANAGER_ID|
|---|---|---|---|
|     |      |            |            |

##### Output Code:[¶](#id101)

##### Snowflake[¶](#id102)

```
 DELETE FROM
    employees;

SELECT * FROM employees ORDER BY id;
```

Copy

##### Result[¶](#id103)

<!-- prettier-ignore -->
|ID|NAME|DEPARTMENT|MANAGER_ID|
|---|---|---|---|
|     |      |            |            |

#### Where Clause[¶](#where-clause)

Restricts updates to rows that match a condition. When the condition returns true, the specified SET
columns are updated. The condition can be a simple predicate on a column or a condition based on the
result of a subquery. This clause is fully equivalent in Snowflake.

##### Input Code:[¶](#id104)

##### Redshift[¶](#id105)

```
 DELETE FROM employees
WHERE department = 'Marketing';

SELECT * FROM employees
ORDER BY id;
```

Copy

##### Result[¶](#id106)

<!-- prettier-ignore -->
|ID|NAME|DEPARTMENT|MANAGER_ID|
|---|---|---|---|
|1|Alice|Sales|2|
|2|Bob|Sales|1|
|3|Charlie|Sales|1|
|7|Grace|Engineering|6|
|8|Helen|Engineering|7|
|9|Ivy|Engineering|7|
|10|John|Sales|3|
|11|Joe|Engineering|5|

##### Output Code:[¶](#id107)

##### Snowflake[¶](#id108)

```
 DELETE FROM
    employees
WHERE department = 'Marketing';

SELECT * FROM
    employees
ORDER BY id;
```

Copy

##### Result[¶](#id109)

<!-- prettier-ignore -->
|ID|NAME|DEPARTMENT|MANAGER_ID|
|---|---|---|---|
|1|Alice|Sales|2|
|2|Bob|Sales|1|
|3|Charlie|Sales|1|
|7|Grace|Engineering|6|
|8|Helen|Engineering|7|
|9|Ivy|Engineering|7|
|10|John|Sales|3|
|11|Joe|Engineering|5|

#### Using Clause[¶](#using-clause)

This clause introduces a list of tables when additional tables are referenced in the WHERE clause
condition. This clause is fully equivalent in Snowflake.

##### Input Code:[¶](#id110)

##### Redshift[¶](#id111)

```
 DELETE FROM employees
USING departments d
WHERE employees.department = d.department_name
AND d.department_name = 'Sales';

SELECT * FROM employees ORDER BY id;
```

Copy

##### Result[¶](#id112)

<!-- prettier-ignore -->
|ID|NAME|DEPARTMENT|MANAGER_ID|
|---|---|---|---|
|4|David|Marketing|2|
|5|Eve|Marketing|4|
|6|Frank|Marketing|4|
|7|Grace|Engineering|6|
|8|Helen|Engineering|7|
|9|Ivy|Engineering|7|
|11|Joe|Engineering|5|

##### Output Code:[¶](#id113)

##### Snowflake[¶](#id114)

```
 DELETE FROM employees
USING departments d
WHERE employees.department = d.department_name
AND d.department_name = 'Sales';

SELECT * FROM employees ORDER BY id;
```

Copy

##### Result[¶](#id115)

<!-- prettier-ignore -->
|ID|NAME|DEPARTMENT|MANAGER_ID|
|---|---|---|---|
|4|David|Marketing|2|
|5|Eve|Marketing|4|
|6|Frank|Marketing|4|
|7|Grace|Engineering|6|
|8|Helen|Engineering|7|
|9|Ivy|Engineering|7|
|11|Joe|Engineering|5|

#### WITH clause[¶](#with-clause)

This clause specifies one or more Common Table Expressions (CTE). The output column names are
optional for non-recursive CTEs, but mandatory for recursive ones.

Since this clause cannot be used in an DELETE statement, it is transformed into temporary tables
with their corresponding queries. After the DELETE statement is executed, these temporary tables are
dropped to clean up, release resources, and avoid name collisions when creating tables within the
same session. Additionally, if a regular table with the same name exists, it will take precedence
again, since the temporary table
[has priority](https://docs.snowflake.com/en/user-guide/tables-temp-transient#potential-naming-conflicts-with-other-table-types)
over any other table with the same name in the same session.

##### Non-Recursive CTE[¶](#non-recursive-cte)

##### Input Code:[¶](#id116)

##### Redshift[¶](#id117)

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

##### Result[¶](#id118)

<!-- prettier-ignore -->
|ID|NAME|DEPARTMENT|MANAGER_ID|
|---|---|---|---|
|4|David|Marketing|2|
|5|Eve|Marketing|4|
|6|Frank|Marketing|4|

##### Output Code:[¶](#id119)

##### Snowflake[¶](#id120)

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

##### Result[¶](#id121)

<!-- prettier-ignore -->
|ID|NAME|DEPARTMENT|MANAGER_ID|
|---|---|---|---|
|4|David|Marketing|2|
|5|Eve|Marketing|4|
|6|Frank|Marketing|4|

##### Recursive CTE[¶](#recursive-cte)

##### Input Code:[¶](#id122)

##### Redshift[¶](#id123)

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

##### Result[¶](#id124)

<!-- prettier-ignore -->
|ID|NAME|DEPARTMENT|MANAGER_ID|
|---|---|---|---|
|1|Alice|Sales|2|
|2|Bob|Sales|1|
|3|Charlie|Sales|1|
|10|John|Sales|3|

##### Output Code:[¶](#id125)

##### Snowflake[¶](#id126)

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

##### Result[¶](#id127)

<!-- prettier-ignore -->
|ID|NAME|DEPARTMENT|MANAGER_ID|
|---|---|---|---|
|1|Alice|Sales|2|
|2|Bob|Sales|1|
|3|Charlie|Sales|1|
|10|John|Sales|3|

#### Delete Materialized View[¶](#delete-materialized-view)

In Redshift, you can apply the DELETE statement to materialized views used for
[streaming ingestion](https://docs.aws.amazon.com/redshift/latest/dg/materialized-view-streaming-ingestion.html).
In Snowflake, these views are transformed into dynamic tables, and the DELETE statement cannot be
used on dynamic tables. For this reason, an EWI will be added.

##### Input Code:[¶](#id128)

##### Redshift[¶](#id129)

```
 CREATE MATERIALIZED VIEW emp_mv AS
SELECT id, name, department FROM employees WHERE department = 'Engineering';

DELETE FROM emp_mv
WHERE id = 2;
```

Copy

##### Output Code:[¶](#id130)

##### Snowflake[¶](#id131)

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

### Known Issues [¶](#id132)

- Replicating the functionality of the `WITH` clause requires creating temporary tables mirroring
  each Common Table Expression (CTE). However, this approach fails if a temporary table with the
  same name already exists within the current session, causing an error.

### Related EWIs[¶](#id133)

1. [SSC-FDM-0031](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0031):
   Dynamic Table required parameters set by default.
2. [SSC-EWI-RS0008](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/redshiftEWI.html#ssc-ewi-rs0008):
   Delete statement cannot be used on dynamic tables.

## EXECUTE[¶](#execute)

### Description[¶](#id134)

> The `EXECUTE` `IMMEDIATE` statement builds and runs a dynamic SQL statement in a single operation.
>
> Native dynamic SQL uses the `EXECUTE` `IMMEDIATE` statement to process most dynamic SQL
> statements.
> ([Redshift Language Reference EXECUTE Statement](https://docs.aws.amazon.com/redshift/latest/dg/c_PLpgSQL-statements.html#r_PLpgSQL-dynamic-sql))

### Grammar Syntax[¶](#id135)

```
 EXECUTE command-string [ INTO target ];
```

Copy

### Sample Source Patterns[¶](#id136)

Concated Example

Input Code

#### Redshift[¶](#id137)

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

##### Snowflake[¶](#id138)

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

#### Function Transformation[¶](#function-transformation)

##### Input Code[¶](#id139)

##### Redshift[¶](#id140)

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

##### Output Code[¶](#id141)

##### Snowflake[¶](#id142)

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

#### Error In Query Parsing[¶](#error-in-query-parsing)

##### Input Code[¶](#id143)

##### Redshift[¶](#id144)

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

##### Output Code[¶](#id145)

##### Snowflake[¶](#id146)

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

#### INTO Clause[¶](#into-clause)

##### Input Code[¶](#id147)

##### Redshift[¶](#id148)

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

##### Output Code[¶](#id149)

##### Snowflake[¶](#id150)

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

### Known Issues[¶](#id151)

#### 1. Execution results cannot be stored in variables.[¶](#execution-results-cannot-be-stored-in-variables)

SnowScripting does not support INTO nor BULK COLLECT INTO clauses. For this reason, results will
need to be passed through other means.

##### 2. Dynamic SQL Execution queries may be marked incorrectly as non-runnable.[¶](#dynamic-sql-execution-queries-may-be-marked-incorrectly-as-non-runnable)

In some scenarios there an execute statement may be commented regardless of being safe or non-safe
to run so please take this into account:

### Related EWIs[¶](#id152)

1. [SSC-EWI-0027](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0027):
   Variable with invalid query.
2. [SSC-EWI-0030](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0030):
   The statement below has usages of dynamic SQL.

## INSERT[¶](#insert)

### Description[¶](#id153)

> Inserts new rows into a table.
> ([Redshift SQL Language Reference Insert Statement](https://docs.aws.amazon.com/redshift/latest/dg/r_INSERT_30.html#r_INSERT_30-synopsis)).

Warning

This syntax is partially supported in Snowflake.

### Grammar Syntax[¶](#id154)

```
 INSERT INTO table_name [ ( column [, ...] ) ]
{DEFAULT VALUES |
VALUES ( { expression | DEFAULT } [, ...] )
[, ( { expression | DEFAULT } [, ...] )
[, ...] ] |
query }
```

Copy

### Sample Source Patterns[¶](#id155)

#### **Setup data**[¶](#id156)

##### Redshift[¶](#id157)

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

#### Default Values[¶](#default-values)

It inserts a complete row with its default values. If any columns do not have default values, NULL
values are inserted in those columns.

This clause cannot specify individual columns; it always inserts a complete row with its default
values. Additionally, columns with the NOT NULL constraint cannot be included in the table
definition. To replicate this behavior in Snowflake, SnowConvert AI insert a column with a DEFAULT
value in the table. This action inserts a complete row, using the default value for every column.

##### Input Code:[¶](#id158)

##### Redshift[¶](#id159)

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

##### Result[¶](#id160)

<!-- prettier-ignore -->
|ID|NAME|SALARY|DEPARTMENT|
|---|---|---|---|
|1|NULL|20000|Marketing|

##### Output Code:[¶](#id161)

##### Snowflake[¶](#id162)

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

##### Result[¶](#id163)

<!-- prettier-ignore -->
|ID|NAME|SALARY|DEPARTMENT|
|---|---|---|---|
|1|NULL|20000|Marketing|

#### Query[¶](#query)

Insert one or more rows into the table by using a query. All rows produced by the query will be
inserted into the table. The query must return a column list that is compatible with the table’s
columns, although the column names do not need to match. This functionality is fully equivalent in
Snowflake.

##### Input Code:[¶](#id164)

##### Redshift[¶](#id165)

```
 INSERT INTO employees (name, salary, department)
SELECT name, salary, department FROM new_employees;
```

Copy

##### Result[¶](#id166)

<!-- prettier-ignore -->
|ID|NAME|SALARY|DEPARTMENT|
|---|---|---|---|
|1|Grace Lee|32000|Operations|
|2|Hannah Gray|26000|Finance|

##### Output Code:[¶](#id167)

##### Snowflake[¶](#id168)

```
 INSERT INTO employees (name, salary, department)
SELECT name, salary, department FROM
    new_employees;
```

Copy

##### Result[¶](#id169)

<!-- prettier-ignore -->
|ID|NAME|SALARY|DEPARTMENT|
|---|---|---|---|
|1|Grace Lee|32000|Operations|
|2|Hannah Gray|26000|Finance|

### Known Issues [¶](#id170)

- Certain expressions cannot be used in the VALUES clause in Snowflake. For example, in Redshift,
  the [JSON_PARSE](https://docs.aws.amazon.com/redshift/latest/dg/JSON_PARSE.html) function can be
  used within the VALUES clause to insert a JSON value into a SUPER data type. In Snowflake,
  however, the [PARSE_JSON](https://docs.snowflake.com/en/sql-reference/functions/parse_json)
  function cannot be used in the VALUES clause to insert a JSON value into a VARIANT data type.
  Instead, a query can be used in place of the VALUES clause. For more details, please refer to the
  [Snowflake documentation](https://docs.snowflake.com/en/sql-reference/sql/insert#usage-notes). You
  can also check the
  [following article](https://community.snowflake.com/s/article/Cannot-use-DATE-FROM-PARTS-function-inside-the-VALUES-clause)
  for further information.

### Related EWIs[¶](#id171)

There are no known issues.

## MERGE[¶](#merge)

### Grammar Syntax[¶](#id172)

```
 MERGE INTO target_table
USING source_table [ [ AS ] alias ]
ON match_condition
[ WHEN MATCHED THEN { UPDATE SET col_name = { expr } [,...] | DELETE }
WHEN NOT MATCHED THEN INSERT [ ( col_name [,...] ) ] VALUES ( { expr } [, ...] ) |
REMOVE DUPLICATES ]
```

Copy

For more information please refer to Redshift
[MERGE documentation](https://docs.aws.amazon.com/redshift/latest/dg/r_MERGE.html).

### Sample Source Patterns[¶](#id173)

#### UPDATE - INSERT[¶](#update-insert)

There are no differences between both languages. The code is kept in its original form.

##### Input Code:[¶](#id174)

##### Redshift[¶](#id175)

```
 MERGE INTO target USING source ON target.id = source.id
WHEN MATCHED THEN UPDATE SET id = source.id, name = source.name
WHEN NOT MATCHED THEN INSERT VALUES (source.id, source.name);
```

Copy

##### Output Code:[¶](#id176)

##### Snowflake[¶](#id177)

```
 --** SSC-FDM-RS0005 - REDSHIFT MERGE STATEMENT DOESN'T ALLOW DUPLICATES IN THE SOURCE TABLE. SNOWFLAKE BEHAVIOR MAY DIFFER IF THERE ARE DUPLICATE VALUES. **
MERGE INTO target USING source ON target.id = source.id
WHEN MATCHED THEN UPDATE SET id = source.id, name = source.name
WHEN NOT MATCHED THEN INSERT VALUES (source.id, source.name);
```

Copy

#### DELETE - INSERT[¶](#delete-insert)

There are no differences between both languages. The code is kept in its original form.

##### Input Code:[¶](#id178)

##### Redshift[¶](#id179)

```
 MERGE INTO target USING source ON target.id = source.id
WHEN MATCHED THEN DELETE
WHEN NOT MATCHED THEN INSERT VALUES (source.id, source.name);
```

Copy

##### Output Code:[¶](#id180)

##### Snowflake[¶](#id181)

```
 --** SSC-FDM-RS0005 - REDSHIFT MERGE STATEMENT DOESN'T ALLOW DUPLICATES IN THE SOURCE TABLE. SNOWFLAKE BEHAVIOR MAY DIFFER IF THERE ARE DUPLICATE VALUES. **
MERGE INTO target USING source ON target.id = source.id
WHEN MATCHED THEN DELETE
WHEN NOT MATCHED THEN INSERT VALUES (source.id, source.name);
```

Copy

#### REMOVE DUPLICATES[¶](#remove-duplicates)

The REMOVE DUPLICATES clause is not supported in Snowflake, however, there is a workaround that
could emulate the original behavior.

The output code will have three new statements:

- A TEMPORARY TABLE with the duplicate values from the source and target table that matches the
  condition
- An INSERT statement that adds the pending values to the target table after the merge
- A DROP statement that drops the generated temporary table.

These are necessary since the DROP DUPLICATES behavior removes the duplicate values from the target
table and then inserts the values that match the condition from the source table.

##### Input Code:[¶](#id182)

##### Redshift[¶](#id183)

```
 CREATE TABLE target (id INT, name CHAR(10));
CREATE TABLE source (id INT, name CHAR(10));

INSERT INTO target VALUES (30, 'Tony'), (30, 'Daisy'), (11, 'Alice'), (23, 'Bill'), (23, 'Nikki');
INSERT INTO source VALUES (23, 'David'), (22, 'Clarence');

MERGE INTO target USING source ON target.id = source.id REMOVE DUPLICATES;
```

Copy

##### Results[¶](#results)

<!-- prettier-ignore -->
|ID|NAME|
|---|---|
|30|Daisy|
|22|Clarence|
|30|Tony|
|11|Alice|
|23|David|

##### Output Code:[¶](#id184)

##### Snowflake[¶](#id185)

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

##### Results[¶](#id186)

<!-- prettier-ignore -->
|ID|NAME|
|---|---|
|22|Clarence|
|30|Tony|
|30|Daisy|
|11|Alice|
|23|David|

### Known Issues[¶](#id187)

There are no known issues.

### Related EWIs[¶](#id188)

1. [SSC-EWI-RS0009](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/redshiftEWI.html#ssc-ewi-rs0009):
   Semantic information not found for the source table.
2. [SSC-FDM-RS0005](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/redshiftFDM.html#ssc-fdm-rs0005):
   Duplicates not allowed in source table.

## UPDATE[¶](#update)

### Description[¶](#id189)

> Updates values in one or more table columns when a condition is satisfied.
> ([Redshift SQL Language Reference Update Statement](https://docs.aws.amazon.com/redshift/latest/dg/r_UPDATE.html)).

Note

This syntax is fully supported in Snowflake.

### Grammar Syntax[¶](#id190)

```
 [ WITH [RECURSIVE] common_table_expression [, common_table_expression , ...] ]
            UPDATE table_name [ [ AS ] alias ] SET column = { expression | DEFAULT } [,...]

[ FROM fromlist ]
[ WHERE condition ]
```

Copy

### Sample Source Patterns[¶](#id191)

#### **Setup data**[¶](#id192)

##### Redshift[¶](#id193)

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

#### Alias[¶](#alias)

Although Snowflake’s grammar does not specify that a table alias can be used, it’s valid code in
Snowflake.

##### Input Code:[¶](#id194)

##### Redshift[¶](#id195)

```
 UPDATE employees AS e
SET salary = salary + 5000
WHERE e.salary < 600000;
```

Copy

##### Result[¶](#id196)

<!-- prettier-ignore -->
|ID|NAME|SALARY|DEPARTMENT|
|---|---|---|---|
|1|Alice|505000|HR|
|2|Bob|600000|Engineering|
|3|Charlie|700000|Engineering|
|4|David|405000|Marketing|
|5|Eve|455000|HR|
|6|Frank|750000|Engineering|
|7|Grace|650000|Engineering|
|8|Helen|395000|Marketing|
|9|Ivy|485000|HR|
|10|Jack|425000|Engineering|
|11|Ken|700000|Marketing|
|12|Liam|600000|Engineering|
|13|Mona|475000|HR|

##### Output Code:[¶](#id197)

##### Snowflake[¶](#id198)

```
 UPDATE employees AS e
SET salary = salary + 5000
WHERE e.salary < 600000;
```

Copy

##### Result[¶](#id199)

<!-- prettier-ignore -->
|ID|NAME|SALARY|DEPARTMENT|
|---|---|---|---|
|1|Alice|505000|HR|
|2|Bob|600000|Engineering|
|3|Charlie|700000|Engineering|
|4|David|405000|Marketing|
|5|Eve|455000|HR|
|6|Frank|750000|Engineering|
|7|Grace|650000|Engineering|
|8|Helen|395000|Marketing|
|9|Ivy|485000|HR|
|10|Jack|425000|Engineering|
|11|Ken|700000|Marketing|
|12|Liam|600000|Engineering|
|13|Mona|475000|HR|

#### WITH clause[¶](#id200)

This clause specifies one or more Common Table Expressions (CTE). The output column names are
optional for non-recursive CTEs, but mandatory for recursive ones.

Since this clause cannot be used in an UPDATE statement, it is transformed into temporary tables
with their corresponding queries. After the UPDATE statement is executed, these temporary tables are
dropped to clean up, release resources, and avoid name collisions when creating tables within the
same session. Additionally, if a regular table with the same name exists, it will take precedence
again, since the temporary table
[has priority](https://docs.snowflake.com/en/user-guide/tables-temp-transient#potential-naming-conflicts-with-other-table-types)
over any other table with the same name in the same session.

##### Non-Recursive CTE[¶](#id201)

##### Input Code:[¶](#id202)

##### Redshift[¶](#id203)

```
 WITH avg_salary_cte AS (
    SELECT AVG(salary) AS avg_salary FROM employees
)
UPDATE employees
SET salary = (SELECT avg_salary FROM avg_salary_cte)
WHERE salary < 500000;
```

Copy

##### Result[¶](#id204)

<!-- prettier-ignore -->
|ID|NAME|SALARY|DEPARTMENT|
|---|---|---|---|
|1|Alice|500000|HR|
|2|Bob|600000|Engineering|
|3|Charlie|700000|Engineering|
|4|David|546923|Marketing|
|5|Eve|546923|HR|
|6|Frank|750000|Engineering|
|7|Grace|650000|Engineering|
|8|Helen|546923|Marketing|
|9|Ivy|546923|HR|
|10|Jack|546923|Engineering|
|11|Ken|700000|Marketing|
|12|Liam|600000|Engineering|
|13|Mona|546923|HR|

##### Output Code:[¶](#id205)

##### Snowflake[¶](#id206)

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

##### Result[¶](#id207)

<!-- prettier-ignore -->
|ID|NAME|SALARY|DEPARTMENT|
|---|---|---|---|
|1|Alice|500000|HR|
|2|Bob|600000|Engineering|
|3|Charlie|700000|Engineering|
|4|David|546923|Marketing|
|5|Eve|546923|HR|
|6|Frank|750000|Engineering|
|7|Grace|650000|Engineering|
|8|Helen|546923|Marketing|
|9|Ivy|546923|HR|
|10|Jack|546923|Engineering|
|11|Ken|700000|Marketing|
|12|Liam|600000|Engineering|
|13|Mona|546923|HR|

##### Recursive CTE[¶](#id208)

##### Input Code:[¶](#id209)

##### Redshift[¶](#id210)

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

##### Result[¶](#id211)

<!-- prettier-ignore -->
|ID|NAME|SALARY|DEPARTMENT|
|---|---|---|---|
|1|Alice|526666|HR|
|2|Bob|670000|Engineering|
|3|Charlie|773333|Engineering|
|4|David|433333|Marketing|
|5|Eve|475000|HR|
|6|Frank|825000|Engineering|
|7|Grace|721666|Engineering|
|8|Helen|423000|Marketing|
|9|Ivy|506000|HR|
|10|Jack|484000|Engineering|
|11|Ken|743333|Marketing|
|12|Liam|670000|Engineering|
|13|Mona|495668|HR|

##### Output Code:[¶](#id212)

##### Snowflake[¶](#id213)

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

##### Result[¶](#id214)

<!-- prettier-ignore -->
|ID|NAME|SALARY|DEPARTMENT|
|---|---|---|---|
|1|Alice|526667|HR|
|2|Bob|670000|Engineering|
|3|Charlie|773333|Engineering|
|4|David|433333|Marketing|
|5|Eve|475000|HR|
|6|Frank|825000|Engineering|
|7|Grace|721667|Engineering|
|8|Helen|423000|Marketing|
|9|Ivy|506000|HR|
|10|Jack|484000|Engineering|
|11|Ken|743333|Marketing|
|12|Liam|670000|Engineering|
|13|Mona|495667|HR|

#### SET DEFAULT values[¶](#set-default-values)

##### Input Code:[¶](#id215)

##### Redshift[¶](#id216)

```
 UPDATE employees
SET salary = DEFAULT, department = 'Sales'
WHERE department = 'HR';
```

Copy

##### Result[¶](#id217)

<!-- prettier-ignore -->
|ID|NAME|SALARY|DEPARTMENT|
|---|---|---|---|
|1|Alice|20000|Sales|
|2|Bob|600000|Engineering|
|3|Charlie|700000|Engineering|
|4|David|400000|Marketing|
|5|Eve|20000|Sales|
|6|Frank|750000|Engineering|
|7|Grace|650000|Engineering|
|8|Helen|390000|Marketing|
|9|Ivy|20000|Sales|
|10|Jack|420000|Engineering|
|11|Ken|700000|Marketing|
|12|Liam|600000|Engineering|
|13|Mona|20000|Sales|

##### Output Code:[¶](#id218)

##### Snowflake[¶](#id219)

```
 UPDATE employees
SET salary = DEFAULT, department = 'Sales'
WHERE
    department = 'HR';
```

Copy

##### Result[¶](#id220)

<!-- prettier-ignore -->
|ID|NAME|SALARY|DEPARTMENT|
|---|---|---|---|
|1|Alice|20000|Sales|
|2|Bob|600000|Engineering|
|3|Charlie|700000|Engineering|
|4|David|400000|Marketing|
|5|Eve|20000|Sales|
|6|Frank|750000|Engineering|
|7|Grace|650000|Engineering|
|8|Helen|390000|Marketing|
|9|Ivy|20000|Sales|
|10|Jack|420000|Engineering|
|11|Ken|700000|Marketing|
|12|Liam|600000|Engineering|
|13|Mona|20000|Sales|

#### SET clause[¶](#set-clause)

It is responsible for modifying values in the columns. Similar to Snowflake, update queries with
multiple matches per row will throw an error when the configuration parameter
[ERROR_ON_NONDETERMINISTIC_UPDATE](https://docs.aws.amazon.com/redshift/latest/dg/r_error_on_nondeterministic_update.html)
is set to true. This flag works the same way in Snowflake, and it even uses the same name,
[ERROR_ON_NONDETERMINISTIC_UPDATE](https://docs.snowflake.com/en/sql-reference/parameters#label-error-on-nondeterministic-update).

However, when this flag is turned off, no error is returned, and one of the matched rows is used to
update the target row. The selected joined row is nondeterministic and arbitrary in both languages;
the behavior may not be consistent across executions, which could lead to data inconsistencies.

##### Setup data:[¶](#id221)

##### Redshift[¶](#id222)

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

##### Input Code:[¶](#id223)

##### Redshift[¶](#id224)

```
 UPDATE target
  SET v = src.v
  FROM src
  WHERE target.k = src.k;


SELECT * FROM target;
```

Copy

##### Result[¶](#id225)

<!-- prettier-ignore -->
|K|V|
|---|---|
|0|16|

##### Output Code:[¶](#id226)

##### Snowflake[¶](#id227)

```
 UPDATE target
  SET v = src.v
  FROM src
  WHERE target.k = src.k;


SELECT * FROM target;
```

Copy

##### Result[¶](#id228)

<!-- prettier-ignore -->
|K|V|
|---|---|
|0|14|

### Known Issues [¶](#id229)

- Update queries with multiple matches per row may cause data inconsistencies. Although both
  platforms have the flag
  [ERROR_ON_NONDETERMINISTIC_UPDATE](https://docs.aws.amazon.com/redshift/latest/dg/r_error_on_nondeterministic_update.html),
  these values will always be nondeterministic. Snowflake offers recommendations for handling these
  scenarios. Click [here](https://docs.snowflake.com/en/sql-reference/sql/update#examples) for more
  details.
- Replicating the functionality of the `WITH` clause requires creating temporary tables mirroring
  each Common Table Expression (CTE). However, this approach fails if a temporary table with the
  same name already exists within the current session, causing an error.

### Related EWIs[¶](#id230)

There are no known issues.
