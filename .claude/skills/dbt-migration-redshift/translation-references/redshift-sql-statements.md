---
description: Translation reference for all the supported statements by SnowConvert AI for Redshift.
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/redshift/redshift-sql-statements
title: SnowConvert AI - Redshift - SQL Statements | Snowflake Documentation
---

## CALL

### Description

> Runs a stored procedure. The CALL command must include the procedure name and the input argument
> values. You must call a stored procedure by using the CALL statement.
> ([Redshift SQL Language Reference CALL](https://docs.aws.amazon.com/redshift/latest/dg/r_CALL_procedure.html)).

### Grammar Syntax

```sql
 CALL sp_name ( [ argument ] [, ...] )
```

### Sample Source Patterns

#### Base scenario

##### Input Code

##### Redshift

```sql
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

##### Output Code

##### Redshift 2

```sql
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

#### Call using Output Parameters Mode (INOUT, OUT)

##### Input Code: 2

##### Redshift 3

```sql
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

##### Output Code: 2

##### Redshift 4

```sql
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

### Known Issues

- Output parameters from calls outside procedures won’t work.

### Related EWIs

1. [SSC-EWI-0073](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0073):
   Pending Functional Equivalence Review

## CREATE DATABASE

### Grammar Syntax 2

```sql
 CREATE DATABASE database_name
[ { [ WITH ]
    [ OWNER [=] db_owner ]
    [ CONNECTION LIMIT { limit | UNLIMITED } ]
    [ COLLATE { CASE_SENSITIVE | CASE_INSENSITIVE } ]
    [ ISOLATION LEVEL { SERIALIZABLE | SNAPSHOT } ]
  }
  | { [ WITH PERMISSIONS ] FROM DATASHARE datashare_name ] OF [ ACCOUNT account_id ] NAMESPACE namespace_guid }
  | { FROM { { ARN '`<arn>`' } { WITH DATA CATALOG SCHEMA '`<schema>`' | WITH NO DATA CATALOG SCHEMA } }
             | { INTEGRATION '`<integration_id>`'} }
  | { IAM_ROLE  {default | 'SESSION' | 'arn:aws:iam::<account-id>:role/<role-name>' } }
```

For more information please refer to Redshift
[`CREATE DATABASE` documentation](https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_DATABASE.html).

### Sample Source Patterns 2

#### Basic samples

##### Input Code: 3

##### Redshift 5

```sql
 CREATE DATABASE database_name;
```

##### Output Code: 3

##### Snowflake

```sql
 CREATE DATABASE IF NOT EXISTS database_name
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/25/2024" }}';
```

#### Collate Clause

##### Input Code: 4

##### Redshift 6

```sql
 CREATE DATABASE database_collate
COLLATE CASE_INSENSITIVE;
```

##### Output Code: 4

##### Snowflake 2

```sql
 CREATE DATABASE IF NOT EXISTS database_collate
DEFAULT_DDL_COLLATION='en-ci'
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/24/2024" }}';
```

#### Connection Limit Clause

##### Input Code: 5

##### Redshift 7

```sql
 CREATE DATABASE database_connection
CONNECTION LIMIT UNLIMITED;
```

##### Output Code: 5

##### Snowflake 3

```sql
 CREATE DATABASE IF NOT EXISTS database_connection
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/24/2024" }}';
```

Warning

The connection limit clause is removed since the connection concurrency in snowflake is managed by
warehouse. More information
[here](https://docs.snowflake.com/en/sql-reference/parameters#label-max-concurrency-level).

#### From ARN Clause

##### Input Code: 6

##### Redshift 8

```sql
 CREATE DATABASE database_fromARN
FROM ARN 'arn' WITH NO DATA CATALOG SCHEMA IAM_ROLE 'arn:aws:iam::<account-id>:role/<role-name';
```

##### Output Code: 6

##### Snowflake 4

```sql
 CREATE DATABASE IF NOT EXISTS database_fromARN
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/24/2024" }}';
```

Warning

This clause is removed since it is used to reference
[Amazon Resources](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference-arns.html), not valid
in Snowflake.

#### From Datashare Clause

##### Input Code 2

##### Redshift 9

```sql
 CREATE DATABASE database_fromDatashare
FROM DATASHARE datashare_name OF NAMESPACE 'namespace_guid';
```

##### Output Code 2

##### Snowflake 5

```sql
 CREATE DATABASE IF NOT EXISTS  database_fromDatashare
FROM DATASHARE datashare_name OF NAMESPACE 'namespace_guid' !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'FromDatashareAttribute' NODE ***/!!!
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/24/2024" }}';
```

###### Note

The transformation for Datashare is planned to be delivered in the future.

#### Owner Clause

##### Input Code 2 2

##### Redshift 10

```sql
 CREATE DATABASE database_Owner
OWNER db_owner
ENCODING 'encoding';
```

##### Output Code 2 2

##### Snowflake 6

```sql
 CREATE DATABASE IF NOT EXISTS database_Owner
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/24/2024" }}';
```

Warning

Please be aware that for this case, the owner clause is removed from the code since Snowflake
databases are owned by roles, not individual users. For more information please refer to
[Snowflake `GRANT OWNERSHIP` documentation](https://docs.snowflake.com/en/sql-reference/sql/grant-ownership).

#### Isolation Level Clause

##### Input Code 3

##### Redshift 11

```sql
 CREATE DATABASE database_Isolation
ISOLATION LEVEL SNAPSHOT;
```

##### Output Code 3

##### Snowflake 7

```sql
 CREATE DATABASE IF NOT EXISTS database_Isolation
ISOLATION LEVEL SNAPSHOT !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'IsolationLevelAttribute' NODE ***/!!!
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/24/2024" }}';
```

###### Note 2

The transformation for Isolation Level is planned to be delivered in the future.

### Related EWIs 2

- [SSC-EWI-0073](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0073):
  Pending Functional Equivalence Review

## CREATE EXTERNAL TABLE

### Description 2

Currently SnowConvert AI is transforming `CREATE EXTERNAL TABLES` to regular tables, that implies
additional effort because data stored in external RedShift tables must be transferred to the
Snowflake database.

### Grammar Syntax 3

```sql
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

Click [here](https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_EXTERNAL_TABLE.html) to go to
the specification for this syntax.

### Sample Source Patterns 3

#### Input Code: 7

##### Redshift 12

```sql
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

##### Output Code: 7

##### Snowflake 8

```sql
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

#### Create External Table AS

##### Input Code: 8

##### Redshift 13

```sql
 CREATE EXTERNAL TABLE spectrum.partitioned_lineitem
PARTITIONED BY (l_shipdate, l_shipmode)
STORED AS parquet
LOCATION 'S3://amzn-s3-demo-bucket/cetas/partitioned_lineitem/'
AS SELECT l_orderkey, l_shipmode, l_shipdate, l_partkey FROM local_table;
```

##### Output Code: 8

##### Snowflake 9

```sql
 --** SSC-FDM-0004 - EXTERNAL TABLE TRANSLATED TO REGULAR TABLE **
CREATE TABLE spectrum.partitioned_lineitem
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/17/2024" }}'
--PARTITIONED BY (l_shipdate, l_shipmode)
--STORED AS parquet
--LOCATION 'S3://amzn-s3-demo-bucket/cetas/partitioned_lineitem/'
AS SELECT l_orderkey, l_shipmode, l_shipdate, l_partkey FROM
local_table;
```

### Recommendations

- For the usage of Create External Table in Snowflake you may refer to
  [Snowflake’s documentation.](https://docs.snowflake.com/en/sql-reference/sql/create-external-table)

### Related EWIs 2 2

1. [SSC-FDM-0004](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0004):
   External table translated to regular table

## CREATE MATERIALIZED VIEW

### Description 3

In SnowConvert AI, Redshift Materialized Views are transformed into Snowflake Dynamic Tables. To
properly configure Dynamic Tables, two essential parameters must be defined: TARGET_LAG and
WAREHOUSE. If these parameters are left unspecified in the configuration options, SnowConvert AI
will default to preassigned values during the conversion, as demonstrated in the example below.

For more information on Materialized Views, click
[here](https://docs.aws.amazon.com/redshift/latest/dg/materialized-view-create-sql-command.html).

For details on the necessary parameters for Dynamic Tables, click
[here](https://docs.snowflake.com/en/sql-reference/sql/create-dynamic-table).

### Grammar Syntax 4

The following is the SQL syntax to create a view in Amazon Redshift. Click
[here](https://docs.aws.amazon.com/redshift/latest/dg/materialized-view-create-sql-command.html) to
here to go to Redshifts specification for this syntax.

```sql
 CREATE MATERIALIZED VIEW mv_name
[ BACKUP { YES | NO } ]
[ table_attributes ]
[ AUTO REFRESH { YES | NO } ]
AS query
```

### Sample Source Patterns 4

#### Input Code: 9

##### Redshift 14

```sql
 CREATE MATERIALIZED VIEW mv_baseball AS
SELECT ball AS baseball FROM baseball_table;
```

##### Output Code: 9

##### Snowflake 10

```sql
 CREATE DYNAMIC TABLE mv_baseball
--** SSC-FDM-0031 - DYNAMIC TABLE REQUIRED PARAMETERS SET BY DEFAULT **
TARGET_LAG='1 day'
WAREHOUSE=UPDATE_DUMMY_WAREHOUSE
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "11/26/2024",  "domain": "test" }}'
AS
    SELECT ball AS baseball FROM
        baseball_table;
```

###### Note 3

For the table attributes documentation you can check de following documentation:

- [Sortkey](redshift-sql-statements-create-table.html#sortkey)
- [DistKey](redshift-sql-statements-create-table.html#distkey)
- [DistStyle](redshift-sql-statements-create-table.html#diststyle)

Warning

The BACKUP and AUTO REFRESH clauses are deleted since they are not applicable in a Snowflake’s
Dynamic Table

### Related Ewis 3

- [SSC-FDM-0031](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0031):
  Dynamic Table required parameters set by default

## CREATE SCHEMA

### Grammar Syntax 5

```sql
 CREATE SCHEMA [ IF NOT EXISTS ] schema_name [ AUTHORIZATION username ]
           [ QUOTA {quota [MB | GB | TB] | UNLIMITED} ] [ schema_element [ ... ]

CREATE SCHEMA AUTHORIZATION username [ QUOTA {quota [MB | GB | TB] | UNLIMITED} ]
[ schema_element [ ... ] ]
```

For more information please refer to
[Redshift `CREATE SCHEMA` documentation](https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_SCHEMA.html).

### Sample Source Patterns 5

#### Basic samples 2

##### Input Code: 10

##### Redshift 15

```sql
 CREATE SCHEMA s1;

CREATE SCHEMA IF NOT EXISTS s2;

CREATE SCHEMA s3
CREATE TABLE t1
(
    col1 INT
)
CREATE VIEW v1 AS SELECT * FROM t1;
```

##### Output Code: 10

##### Snowflake 11

```sql
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

#### Authorization Clause

##### Input Code: 11

##### Redshift 16

```sql
 CREATE SCHEMA s1 AUTHORIZATION miller;
```

##### Output Code: 11

##### Snowflake 12

```sql
 CREATE SCHEMA IF NOT EXISTS s1
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/23/2024" }}'
;
```

Warning

Please be aware that for this case, the authorization clause is removed from the code since
Snowflake schemas are owned by roles, not individual users. For more information please refer to
[Snowflake `GRANT OWNERSHIP` documentation](https://docs.snowflake.com/en/sql-reference/sql/grant-ownership).

#### Quota Clause

##### Input Code: 12

##### Redshift 17

```sql
 CREATE SCHEMA s1 QUOTA UNLIMITED;

CREATE SCHEMA s2 QUOTA 10 TB;
```

##### Output Code: 12

##### Snowflake 13

```sql
 CREATE SCHEMA IF NOT EXISTS s1
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/23/2024" }}'
;

CREATE SCHEMA IF NOT EXISTS s2
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/23/2024" }}'
;
```

###### Note 4

In Snowflake is not allowed to define a quota per scheme. Storage management is done at the account
and warehouse level, and Snowflake handles it automatically. For this reason it is removed from the
code.

#### Create Schema Authorization

In Redshift when the schema name is not specified but the authorization clause is defined, a new
schema is created with the owner’s name. For this reason this behavior is replicated in Snowflake.

##### Input Code: 13

##### Redshift 18

```sql
 CREATE SCHEMA AUTHORIZATION miller;
```

##### Output Code: 13

##### Snowflake 14

```sql
 CREATE SCHEMA IF NOT EXISTS miller
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/23/2024" }}'
;
```

### Related EWIs 4

There are no known issues.

## CREATE FUNCTION

### Description 4

This command defines a user-defined function (UDF) within the database. These functions encapsulate
reusable logic that can be invoked within SQL queries.

### Grammar Syntax 6

The following is the SQL syntax to create a view in Amazon Redshift. Click
[here](https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_VIEW.html) to here to go to Redshifts
specification for this syntax.

```sql
 CREATE [ OR REPLACE ] FUNCTION f_function_name
( { [py_arg_name  py_arg_data_type |
sql_arg_data_type } [ , ... ] ] )
RETURNS data_type
{ VOLATILE | STABLE | IMMUTABLE }
AS $$
  { python_program | SELECT_clause }
$$ LANGUAGE { plpythonu | sql }
```

### SQL Language

#### Volatility category

In Snowflake, `VOLATILE` and `IMMUTABLE` function volatility are functionally equivalent. Given that
`STABLE` is inherently transformed to the default `VOLATILE` behavior, explicit use of `STABLE` will
be delete.

##### Input Code: 14

##### Redshift 19

```sql
 CREATE OR REPLACE FUNCTION get_sale(INTEGER)
RETURNS FLOAT
STABLE
AS $$
SELECT price FROM sales where id = $1
$$ LANGUAGE SQL;
```

##### Output Code: 14

##### Snowflake 15

```sql
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

### Python Language

Within the SnowConvert AI scope, the Python language for `CREATE FUNCTION` statements is not
supported. Consequently, the language `plpythonu` will be flagged with an EWI (SSC-EWI-0073), and
its body could appear with parsing errors.

#### Input Code: 15

##### Redshift 20

```sql
 create function f_py_greater (a float, b float)
  returns float
stable
as $$
  if a > b:
    return a
  return b
$$ language plpythonu;
```

##### Output Code: 15

##### Snowflake 16

```sql
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

### Related EWIs 5

There are no known issues.

## CREATE VIEW

### Description 5

This command creates a view in a database, which is run every time the view is referenced in a
query. Using the WITH NO SCHEMA BINDING clause, you can create views to an external table or objects
that don’t exist yet. This clause, however, requires you to specify the qualified name of the object
or table that you are referencing.

### Grammar Syntax 7

The following is the SQL syntax to create a view in Amazon Redshift. Click
[here](https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_VIEW.html) to here to go to Redshifts
specification for this syntax.

```sql
 CREATE [ OR REPLACE ] VIEW name [ ( column_name [, ...] ) ] AS query
[ WITH NO SCHEMA BINDING ]
```

### Sample Source Patterns 6

Considering the obligatory and optional clauses in Redshifts command, the output after migration to
Snowflake is very similar.

#### Input Code: 16

##### Redshift 21

```sql
 CREATE VIEW myuser
AS
SELECT lastname FROM users;

CREATE VIEW myuser2
AS
SELECT lastname FROM users2
WITH NO SCHEMA BINDING;
```

##### Output Code: 16

##### Snowflake 17

```sql
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

There are some exceptions, however, of one unsupported clause from Redshift, therefore an EWI was
implemented to cover this case.

### Related EWIs 6

- [SSC-EWI-RS0003](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/redshiftEWI#ssc-ewi-rs0003):
  With no schema binding statement is not supported in Snowflake.

## DELETE

### Description 6

> Deletes rows from tables.
> ([Redshift SQL Language Reference Delete Statement](https://docs.aws.amazon.com/redshift/latest/dg/r_DELETE.html)).

#### Note 5

This syntax is fully supported in Snowflake.

### Grammar Syntax 8

```sql
 [ WITH [RECURSIVE] common_table_expression [, common_table_expression , ...] ]
DELETE [ FROM ] { table_name | materialized_view_name }
    [ USING table_name, ... ]
    [ WHERE condition ]
```

### Sample Source Patterns 7

#### **Setup data**

##### Redshift 22

```sql
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

#### From Clause

Update a table by referencing information from other tables. In Redshift, the FROM keyword is
optional, but in Snowflake, it is mandatory. Therefore, it will be added in cases where it’s
missing.

##### Input Code: 17

##### Redshift 23

```sql
 DELETE employees;

SELECT * FROM employees ORDER BY id;
```

##### Result

<!-- prettier-ignore -->
|ID|NAME|DEPARTMENT|MANAGER_ID|
|---|---|---|---|
|     |      |            |            |

##### Output Code: 17

##### Snowflake 18

```sql
 DELETE FROM
    employees;

SELECT * FROM employees ORDER BY id;
```

##### Result 2

<!-- prettier-ignore -->
|ID|NAME|DEPARTMENT|MANAGER_ID|
|---|---|---|---|
|     |      |            |            |

#### Where Clause

Restricts updates to rows that match a condition. When the condition returns true, the specified SET
columns are updated. The condition can be a simple predicate on a column or a condition based on the
result of a subquery. This clause is fully equivalent in Snowflake.

##### Input Code: 18

##### Redshift 24

```sql
 DELETE FROM employees
WHERE department = 'Marketing';

SELECT * FROM employees
ORDER BY id;
```

##### Result 3

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

##### Output Code: 18

##### Snowflake 19

```sql
 DELETE FROM
    employees
WHERE department = 'Marketing';

SELECT * FROM
    employees
ORDER BY id;
```

##### Result 4

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

#### Using Clause

This clause introduces a list of tables when additional tables are referenced in the WHERE clause
condition. This clause is fully equivalent in Snowflake.

##### Input Code: 19

##### Redshift 25

```sql
 DELETE FROM employees
USING departments d
WHERE employees.department = d.department_name
AND d.department_name = 'Sales';

SELECT * FROM employees ORDER BY id;
```

##### Result 5

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

##### Output Code: 19

##### Snowflake 20

```sql
 DELETE FROM employees
USING departments d
WHERE employees.department = d.department_name
AND d.department_name = 'Sales';

SELECT * FROM employees ORDER BY id;
```

##### Result 6

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

#### WITH clause

This clause specifies one or more Common Table Expressions (CTE). The output column names are
optional for non-recursive CTEs, but mandatory for recursive ones.

Since this clause cannot be used in an DELETE statement, it is transformed into temporary tables
with their corresponding queries. After the DELETE statement is executed, these temporary tables are
dropped to clean up, release resources, and avoid name collisions when creating tables within the
same session. Additionally, if a regular table with the same name exists, it will take precedence
again, since the temporary table
[has priority](https://docs.snowflake.com/en/user-guide/tables-temp-transient#potential-naming-conflicts-with-other-table-types)
over any other table with the same name in the same session.

##### Non-Recursive CTE

##### Input Code: 20

##### Redshift 26

```sql
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

##### Result 7

<!-- prettier-ignore -->
|ID|NAME|DEPARTMENT|MANAGER_ID|
|---|---|---|---|
|4|David|Marketing|2|
|5|Eve|Marketing|4|
|6|Frank|Marketing|4|

##### Output Code: 20

##### Snowflake 21

```sql
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

##### Result 8

<!-- prettier-ignore -->
|ID|NAME|DEPARTMENT|MANAGER_ID|
|---|---|---|---|
|4|David|Marketing|2|
|5|Eve|Marketing|4|
|6|Frank|Marketing|4|

##### Recursive CTE

##### Input Code: 21

##### Redshift 27

```sql
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

##### Result 9

<!-- prettier-ignore -->
|ID|NAME|DEPARTMENT|MANAGER_ID|
|---|---|---|---|
|1|Alice|Sales|2|
|2|Bob|Sales|1|
|3|Charlie|Sales|1|
|10|John|Sales|3|

##### Output Code: 21

##### Snowflake 22

```sql
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

##### Result 10

<!-- prettier-ignore -->
|ID|NAME|DEPARTMENT|MANAGER_ID|
|---|---|---|---|
|1|Alice|Sales|2|
|2|Bob|Sales|1|
|3|Charlie|Sales|1|
|10|John|Sales|3|

#### Delete Materialized View

In Redshift, you can apply the DELETE statement to materialized views used for
[streaming ingestion](https://docs.aws.amazon.com/redshift/latest/dg/materialized-view-streaming-ingestion.html).
In Snowflake, these views are transformed into dynamic tables, and the DELETE statement cannot be
used on dynamic tables. For this reason, an EWI will be added.

##### Input Code: 22

##### Redshift 28

```sql
 CREATE MATERIALIZED VIEW emp_mv AS
SELECT id, name, department FROM employees WHERE department = 'Engineering';

DELETE FROM emp_mv
WHERE id = 2;
```

##### Output Code: 22

##### Snowflake 23

```sql
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

### Known Issues 2

- Replicating the functionality of the `WITH` clause requires creating temporary tables mirroring
  each Common Table Expression (CTE). However, this approach fails if a temporary table with the
  same name already exists within the current session, causing an error.

### Related EWIs 7

1. [SSC-FDM-0031](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0031):
   Dynamic Table required parameters set by default.
2. [SSC-EWI-RS0008](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/redshiftEWI#ssc-ewi-rs0008):
   Delete statement cannot be used on dynamic tables.

## EXECUTE

### Description 7

> The `EXECUTE` `IMMEDIATE` statement builds and runs a dynamic SQL statement in a single operation.
>
> Native dynamic SQL uses the `EXECUTE` `IMMEDIATE` statement to process most dynamic SQL
> statements.
> ([Redshift Language Reference EXECUTE Statement](https://docs.aws.amazon.com/redshift/latest/dg/c_PLpgSQL-statements.html#r_PLpgSQL-dynamic-sql))

### Grammar Syntax 9

```sql
 EXECUTE command-string [ INTO target ];
```

### Sample Source Patterns 8

Concated Example

Input Code

#### Redshift 29

```sql
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

Output Code

##### Snowflake 24

```sql
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

#### Function Transformation

##### Input Code 4

##### Redshift 30

```sql
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

##### Output Code 4

##### Snowflake 25

```sql
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

#### Error In Query Parsing

##### Input Code 5

##### Redshift 31

```sql
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

##### Output Code 5

##### Snowflake 26

```sql
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

#### INTO Clause

##### Input Code 6

##### Redshift 32

```sql
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

##### Output Code 6

##### Snowflake 27

```sql
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

### Known Issues 3

#### 1. Execution results cannot be stored in variables

SnowScripting does not support INTO nor BULK COLLECT INTO clauses. For this reason, results will
need to be passed through other means.

##### 2. Dynamic SQL Execution queries may be marked incorrectly as non-runnable

In some scenarios there an execute statement may be commented regardless of being safe or non-safe
to run so please take this into account:

### Related EWIs 8

1. [SSC-EWI-0027](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0027):
   Variable with invalid query.
2. [SSC-EWI-0030](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0030):
   The statement below has usages of dynamic SQL.

## INSERT

### Description 8

> Inserts new rows into a table.
> ([Redshift SQL Language Reference Insert Statement](https://docs.aws.amazon.com/redshift/latest/dg/r_INSERT_30.html#r_INSERT_30-synopsis)).

Warning

This syntax is partially supported in Snowflake.

### Grammar Syntax 10

```sql
 INSERT INTO table_name [ ( column [, ...] ) ]
{DEFAULT VALUES |
VALUES ( { expression | DEFAULT } [, ...] )
[, ( { expression | DEFAULT } [, ...] )
[, ...] ] |
query }
```

### Sample Source Patterns 9

#### **Setup data** 2

##### Redshift 33

```sql
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

#### Default Values

It inserts a complete row with its default values. If any columns do not have default values, NULL
values are inserted in those columns.

This clause cannot specify individual columns; it always inserts a complete row with its default
values. Additionally, columns with the NOT NULL constraint cannot be included in the table
definition. To replicate this behavior in Snowflake, SnowConvert AI insert a column with a DEFAULT
value in the table. This action inserts a complete row, using the default value for every column.

##### Input Code: 23

##### Redshift 34

```sql
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

##### Result 11

<!-- prettier-ignore -->
|ID|NAME|SALARY|DEPARTMENT|
|---|---|---|---|
|1|NULL|20000|Marketing|

##### Output Code: 23

##### Snowflake 28

```sql
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

##### Result 12

<!-- prettier-ignore -->
|ID|NAME|SALARY|DEPARTMENT|
|---|---|---|---|
|1|NULL|20000|Marketing|

#### Query

Insert one or more rows into the table by using a query. All rows produced by the query will be
inserted into the table. The query must return a column list that is compatible with the table’s
columns, although the column names do not need to match. This functionality is fully equivalent in
Snowflake.

##### Input Code: 24

##### Redshift 35

```sql
 INSERT INTO employees (name, salary, department)
SELECT name, salary, department FROM new_employees;
```

##### Result 13

<!-- prettier-ignore -->
|ID|NAME|SALARY|DEPARTMENT|
|---|---|---|---|
|1|Grace Lee|32000|Operations|
|2|Hannah Gray|26000|Finance|

##### Output Code: 24

##### Snowflake 29

```sql
 INSERT INTO employees (name, salary, department)
SELECT name, salary, department FROM
    new_employees;
```

##### Result 14

<!-- prettier-ignore -->
|ID|NAME|SALARY|DEPARTMENT|
|---|---|---|---|
|1|Grace Lee|32000|Operations|
|2|Hannah Gray|26000|Finance|

### Known Issues 4

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

### Related EWIs 9

There are no known issues.

## MERGE

### Grammar Syntax 11

```sql
 MERGE INTO target_table
USING source_table [ [ AS ] alias ]
ON match_condition
[ WHEN MATCHED THEN { UPDATE SET col_name = { expr } [,...] | DELETE }
WHEN NOT MATCHED THEN INSERT [ ( col_name [,...] ) ] VALUES ( { expr } [, ...] ) |
REMOVE DUPLICATES ]
```

For more information please refer to Redshift
[MERGE documentation](https://docs.aws.amazon.com/redshift/latest/dg/r_MERGE.html).

### Sample Source Patterns 10

#### UPDATE - INSERT

There are no differences between both languages. The code is kept in its original form.

##### Input Code: 25

##### Redshift 36

```sql
 MERGE INTO target USING source ON target.id = source.id
WHEN MATCHED THEN UPDATE SET id = source.id, name = source.name
WHEN NOT MATCHED THEN INSERT VALUES (source.id, source.name);
```

##### Output Code: 25

##### Snowflake 30

```sql
 --** SSC-FDM-RS0005 - REDSHIFT MERGE STATEMENT DOESN'T ALLOW DUPLICATES IN THE SOURCE TABLE. SNOWFLAKE BEHAVIOR MAY DIFFER IF THERE ARE DUPLICATE VALUES. **
MERGE INTO target USING source ON target.id = source.id
WHEN MATCHED THEN UPDATE SET id = source.id, name = source.name
WHEN NOT MATCHED THEN INSERT VALUES (source.id, source.name);
```

#### DELETE - INSERT

There are no differences between both languages. The code is kept in its original form.

##### Input Code: 26

##### Redshift 37

```sql
 MERGE INTO target USING source ON target.id = source.id
WHEN MATCHED THEN DELETE
WHEN NOT MATCHED THEN INSERT VALUES (source.id, source.name);
```

##### Output Code: 26

##### Snowflake 31

```sql
 --** SSC-FDM-RS0005 - REDSHIFT MERGE STATEMENT DOESN'T ALLOW DUPLICATES IN THE SOURCE TABLE. SNOWFLAKE BEHAVIOR MAY DIFFER IF THERE ARE DUPLICATE VALUES. **
MERGE INTO target USING source ON target.id = source.id
WHEN MATCHED THEN DELETE
WHEN NOT MATCHED THEN INSERT VALUES (source.id, source.name);
```

#### REMOVE DUPLICATES

The REMOVE DUPLICATES clause is not supported in Snowflake, however, there is a workaround that
could emulate the original behavior.

The output code will have three new statements:

- A TEMPORARY TABLE with the duplicate values from the source and target table that matches the
  condition
- An INSERT statement that adds the pending values to the target table after the merge
- A DROP statement that drops the generated temporary table.

These are necessary since the DROP DUPLICATES behavior removes the duplicate values from the target
table and then inserts the values that match the condition from the source table.

##### Input Code: 27

##### Redshift 38

```sql
 CREATE TABLE target (id INT, name CHAR(10));
CREATE TABLE source (id INT, name CHAR(10));

INSERT INTO target VALUES (30, 'Tony'), (30, 'Daisy'), (11, 'Alice'), (23, 'Bill'), (23, 'Nikki');
INSERT INTO source VALUES (23, 'David'), (22, 'Clarence');

MERGE INTO target USING source ON target.id = source.id REMOVE DUPLICATES;
```

##### Results

<!-- prettier-ignore -->
|ID|NAME|
|---|---|
|30|Daisy|
|22|Clarence|
|30|Tony|
|11|Alice|
|23|David|

##### Output Code: 27

##### Snowflake 32

```sql
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

##### Results 2

<!-- prettier-ignore -->
|ID|NAME|
|---|---|
|22|Clarence|
|30|Tony|
|30|Daisy|
|11|Alice|
|23|David|

### Known Issues 5

There are no known issues.

### Related EWIs 10

1. [SSC-EWI-RS0009](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/redshiftEWI#ssc-ewi-rs0009):
   Semantic information not found for the source table.
2. [SSC-FDM-RS0005](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/redshiftFDM#ssc-fdm-rs0005):
   Duplicates not allowed in source table.

## UPDATE

### Description 9

> Updates values in one or more table columns when a condition is satisfied.
> ([Redshift SQL Language Reference Update Statement](https://docs.aws.amazon.com/redshift/latest/dg/r_UPDATE.html)).

#### Note 6

This syntax is fully supported in Snowflake.

### Grammar Syntax 12

```sql
 [ WITH [RECURSIVE] common_table_expression [, common_table_expression , ...] ]
            UPDATE table_name [ [ AS ] alias ] SET column = { expression | DEFAULT } [,...]

[ FROM fromlist ]
[ WHERE condition ]
```

### Sample Source Patterns 11

#### **Setup data** 3

##### Redshift 39

```sql
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

#### Alias

Although Snowflake’s grammar does not specify that a table alias can be used, it’s valid code in
Snowflake.

##### Input Code: 28

##### Redshift 40

```sql
 UPDATE employees AS e
SET salary = salary + 5000
WHERE e.salary < 600000;
```

##### Result 15

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

##### Output Code: 28

##### Snowflake 33

```sql
 UPDATE employees AS e
SET salary = salary + 5000
WHERE e.salary < 600000;
```

##### Result 16

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

#### WITH clause 2

This clause specifies one or more Common Table Expressions (CTE). The output column names are
optional for non-recursive CTEs, but mandatory for recursive ones.

Since this clause cannot be used in an UPDATE statement, it is transformed into temporary tables
with their corresponding queries. After the UPDATE statement is executed, these temporary tables are
dropped to clean up, release resources, and avoid name collisions when creating tables within the
same session. Additionally, if a regular table with the same name exists, it will take precedence
again, since the temporary table
[has priority](https://docs.snowflake.com/en/user-guide/tables-temp-transient#potential-naming-conflicts-with-other-table-types)
over any other table with the same name in the same session.

##### Non-Recursive CTE 2

##### Input Code: 29

##### Redshift 41

```sql
 WITH avg_salary_cte AS (
    SELECT AVG(salary) AS avg_salary FROM employees
)
UPDATE employees
SET salary = (SELECT avg_salary FROM avg_salary_cte)
WHERE salary < 500000;
```

##### Result 17

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

##### Output Code: 29

##### Snowflake 34

```sql
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

##### Result 18

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

##### Recursive CTE 2

##### Input Code: 30

##### Redshift 42

```sql
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

##### Result 19

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

##### Output Code: 30

##### Snowflake 35

```sql
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

##### Result 20

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

#### SET DEFAULT values

##### Input Code: 31

##### Redshift 43

```sql
 UPDATE employees
SET salary = DEFAULT, department = 'Sales'
WHERE department = 'HR';
```

##### Result 21

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

##### Output Code: 31

##### Snowflake 36

```sql
 UPDATE employees
SET salary = DEFAULT, department = 'Sales'
WHERE
    department = 'HR';
```

##### Result 22

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

#### SET clause

It is responsible for modifying values in the columns. Similar to Snowflake, update queries with
multiple matches per row will throw an error when the configuration parameter
[ERROR_ON_NONDETERMINISTIC_UPDATE](https://docs.aws.amazon.com/redshift/latest/dg/r_error_on_nondeterministic_update.html)
is set to true. This flag works the same way in Snowflake, and it even uses the same name,
[ERROR_ON_NONDETERMINISTIC_UPDATE](https://docs.snowflake.com/en/sql-reference/parameters#label-error-on-nondeterministic-update).

However, when this flag is turned off, no error is returned, and one of the matched rows is used to
update the target row. The selected joined row is nondeterministic and arbitrary in both languages;
the behavior may not be consistent across executions, which could lead to data inconsistencies.

##### Setup data

##### Redshift 44

```sql
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

##### Input Code: 32

##### Redshift 45

```sql
 UPDATE target
  SET v = src.v
  FROM src
  WHERE target.k = src.k;

SELECT * FROM target;
```

##### Result 23

<!-- prettier-ignore -->
|K|V|
|---|---|
|0|16|

##### Output Code: 32

##### Snowflake 37

```sql
 UPDATE target
  SET v = src.v
  FROM src
  WHERE target.k = src.k;

SELECT * FROM target;
```

##### Result 24

<!-- prettier-ignore -->
|K|V|
|---|---|
|0|14|

### Known Issues 6

- Update queries with multiple matches per row may cause data inconsistencies. Although both
  platforms have the flag
  [ERROR_ON_NONDETERMINISTIC_UPDATE](https://docs.aws.amazon.com/redshift/latest/dg/r_error_on_nondeterministic_update.html),
  these values will always be nondeterministic. Snowflake offers recommendations for handling these
  scenarios. Click [here](https://docs.snowflake.com/en/sql-reference/sql/update#examples) for more
  details.
- Replicating the functionality of the `WITH` clause requires creating temporary tables mirroring
  each Common Table Expression (CTE). However, this approach fails if a temporary table with the
  same name already exists within the current session, causing an error.

### Related EWIs 11

There are no known issues.
