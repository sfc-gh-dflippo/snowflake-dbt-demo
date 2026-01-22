---
description: Specifies the data type of the column
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/db2/db2-data-types
title: SnowConvert AI - IBM DB2 - Data Types | Snowflake Documentation
---

## Description

> Specifies the data type of the column

Click
[here](https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-table#sdx-synid_built-in-type)
to navigate to the IBM DB2 documentation page for this syntax.

## Transformations

The following table shows the transformation from Db2 to Snowflake.

<!-- prettier-ignore -->
|Db2|Snowflake|EWI|
|---|---|---|
|SMALLINT|SMALLINT||
|INTEGER|INTEGER||
|INT|INT||
|BIGINT|BIGINT||
|DECIMAL|DECIMAL||
|DEC|DEC||
|NUMERIC|NUMERIC||
|NUM|NUMERIC||
|FLOAT|FLOAT||
|REAL|REAL||
|DOUBLE|DOUBLE||
|DECFLOAT|DECFLOAT||
|CHARACTER|CHARACTER||
|CHAR|CHAR||
|VARCHAR|VARCHAR||
|CHARACTER VARYING|CHARACTER VARYING||
|CHAR VARYING|CHAR VARYING||
|CLOB|VARCHAR||
|CHARACTER LARGE OBJECT|VARCHAR||
|CHAR LARGE OBJECT|VARCHAR||
|CLOB|VARCHAR||
|CHARACTER LARGE OBJECT|VARCHAR||
|CHAR LARGE OBJECT|VARCHAR||
|GRAPHIC|BINARY||
|VARGRAPHIC|BINARY||
|DBCLOB|VARCHAR||
|NCHAR|NCHAR||
|NATIONAL CHAR|NCHAR||
|NATIONAL CHARACTER|NCHAR||
|NVARCHAR|NVARCHAR||
|NCHAR VARYING|NCHAR VARYING||
|NATIONAL CHAR VARYING|NCHAR VARYING||
|NATIONAL CHARACTER VARYING|NCHAR VARYING||
|NCLOB|VARCHAR||
|NCHAR LARGE OBJECT|VARCHAR||
|NATIONAL CHARACTER LARGE OBJECT|VARCHAR||
|BINARY|BINARY||
|VARBINARY|VARBINARY||
|BINARY VARYING|BINARY VARYING||
|BLOB|BINARY||
|BINARY LARGE OBJECT|BINARY||
|DATE|DATE||
|TIME|TIME||
|TIMESTAMP|TIMESTAMP||
|XML|VARIANT|[SSC-EWI-0036](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0036)|
|BOOLEAN|BOOLEAN||

## Sample Source Patterns

### IBM DB2

```sql
 CREATE TABLE T1
(
    COL1 SMALLINT,
    COL2 INTEGER,
    COL3 INT,
    COL4 BIGINT,
    COL55 DECIMAL,
    COl5 DECIMAL(5,0),
    COL66 DEC,
    COL6 DEC(5,0),
    COL77 NUMERIC,
    COL7 NUMERIC(5,0),
    COL88 NUM,
    COL8 NUM(5,0),
    COL9 FLOAT,
    COL10 FLOAT(53),
    COL11 REAL,
    COL12 DOUBLE,
    COL13 DOUBLE PRECISION,
    COL14 DECFLOAT(34),
    COL144 DECFLOAT,
    COL153 CHARACTER(8 OCTETS) FOR BIT DATA,
    COL163 CHAR(8 OCTETS) FOR BIT DATA,
    COL164 CHAR(8 OCTETS) CCSID ASCII,
    COL171 VARCHAR(8 OCTETS),
    COL172 VARCHAR(8) FOR BIT DATA,
    COL18 CHARACTER VARYING(8),
    COL180 CHARACTER VARYING(8) FOR BIT DATA,
    COL19 CHAR VARYING(8),
    COL199 CHAR VARYING(8) FOR BIT DATA,
    COL20 CLOB(1M),
    COL21 CHARACTER LARGE OBJECT(8K OCTETS),
    COL22 CHAR LARGE OBJECT,
    COL23 GRAPHIC(1),
    COL233 GRAPHIC(1 CODEUNITS16),
    COL234 GRAPHIC(1 CODEUNITS32),
    COL24 VARGRAPHIC(8 CODEUNITS16),
    COL25 DBCLOB(1M),
    COL255 DBCLOB(1K),
    COL26 NCHAR(1),
    COL27 NATIONAL CHAR(2),
    COL28 NATIONAL CHARACTER(3),
    COL29 NVARCHAR(8),
    COL30 NCHAR VARYING(8),
    COL31 NATIONAL CHAR VARYING(8),
    COL32 NATIONAL CHARACTER VARYING(8),
    COL333 NCLOB(1M),
    COL334 NCHAR LARGE OBJECT(5),
    COL335 NATIONAL CHARACTER LARGE OBJECT(1M),
    COL33 BINARY,
    COL34 VARBINARY(14),
    COL35 BINARY VARYING(10),
    COL36 BLOB(1M),
    COL37 BINARY LARGE OBJECT(1M),
    COL38 DATE,
    COL39 TIME,
    COL40 TIMESTAMP,
    COL41 XML,
    COL42 BOOLEAN
);
```

#### Snowflake

```sql
 CREATE TABLE T1
 (

    COL88 NUMERIC,
    COL8 NUMERIC(5,0),
    COL9 FLOAT,
    COL10 FLOAT(53),
    COL11 REAL,
    COL12 DOUBLE,
    COL13 DOUBLE PRECISION,
    COL14 DECFLOAT,
    COL144 DECFLOAT,
    COL153 BINARY,
    COL163 BINARY,
    COL164 CHAR(8),
    COL171 VARCHAR(8),
    COL172 BINARY,
    COL18 CHARACTER VARYING(8),
    COL180 BINARY,
    COL19 CHAR VARYING(8),
    COL199 BINARY,
    COL20 VARCHAR,
    COL21 VARCHAR,
    COL22 VARCHAR,
    COL23 BINARY,
    COL233 BINARY,
    COL234 BINARY,
    COL24 BINARY,
    COL25 VARCHAR,
    COL255 VARCHAR,
    COL26 NCHAR(1),
    COL27 NCHAR(2),
    COL28 NCHAR(3),
    COL29 NVARCHAR(8),
    COL30 NCHAR VARYING(8),
    COL31 NCHAR VARYING(8),
    COL32 NCHAR VARYING(8),
    COL333 VARCHAR,
    COL334 VARCHAR,
    COL335 VARCHAR,
    COL33 BINARY,
    COL34 VARBINARY(14),
    COL35 BINARY VARYING(10),
    COL36 BINARY,
    COL37 BINARY,
    COL38 DATE,
    COL39 TIME,
    COL40 TIMESTAMP,
    COL41 VARIANT !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - XMLTYPE DATA TYPE CONVERTED TO VARIANT ***/!!!,
    COL42 BOOLEAN
)
 COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "08/29/2025",  "domain": "no-domain-provided" }}';
```

## DECFLOAT Data Type

### Description 2

The `DECFLOAT` data type in IBM DB2 is a decimal floating-point data type that can store decimal
numbers with high precision. DB2 supports `DECFLOAT(16)` and `DECFLOAT(34)` precisions.

SnowConvert AI transforms DB2 `DECFLOAT` columns to Snowflake’s native `DECFLOAT` data type in table
column definitions and `CAST` expressions.

### Supported Contexts

`DECFLOAT` is supported in the following contexts:

- **Table column definitions**: `DECFLOAT` columns in `CREATE TABLE` statements are transformed to
  Snowflake `DECFLOAT`
- **CAST expressions**: `CAST(value AS DECFLOAT)` is preserved in Snowflake

### Unsupported Contexts

`DECFLOAT` is **not** supported in the following contexts and will be transformed to
`NUMBER(38, 37)` with an FDM warning:

- Procedure parameters
- Function parameters
- Local variable declarations

### INSERT Statement Handling

When inserting data into `DECFLOAT` columns, SnowConvert AI automatically adds `CAST` expressions to
ensure proper data type handling:

#### INSERT with VALUES

Numeric literals in `INSERT ... VALUES` statements targeting `DECFLOAT` columns are wrapped with
`CAST(... AS DECFLOAT)`:

##### DB2

```sql
CREATE TABLE prices (
    product_id INT,
    price DECFLOAT(34)
);

INSERT INTO prices VALUES (1, 99.99);
```

##### Snowflake 2

```sql
CREATE OR REPLACE TABLE prices (
    product_id INT,
    price DECFLOAT
);

INSERT INTO prices VALUES (1, CAST(99.99 AS DECFLOAT));
```

#### INSERT with SELECT

Column references in `INSERT ... SELECT` statements are also cast when the target column is
`DECFLOAT`:

##### DB2 2

```sql
CREATE TABLE prices (
    product_id INT,
    price DECFLOAT(34)
);

INSERT INTO prices (product_id, price)
SELECT id, amount FROM source_table;
```

##### Snowflake 3

```sql
CREATE OR REPLACE TABLE prices (
    product_id INT,
    price DECFLOAT
);

INSERT INTO prices (product_id, price)
SELECT id, CAST(amount AS DECFLOAT) FROM source_table;
```

### Related EWIs

1. [SSC-FDM-DB0002](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/db2FDM#ssc-fdm-db0002):
   DECFLOAT is not supported in this context.

## Related EWIs 2

1. [SSC-EWI-0036](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0036):
   Data type converted to another data type.
