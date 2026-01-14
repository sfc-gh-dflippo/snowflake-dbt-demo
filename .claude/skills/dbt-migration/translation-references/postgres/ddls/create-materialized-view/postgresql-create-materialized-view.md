---
description:
  Translation reference to convert PostgreSQL Materialized View to Snowflake Dynamic Table
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/postgres/ddls/create-materialized-view/postgresql-create-materialized-view
title: SnowConvert AI - PostgreSQL - CREATE MATERIALIZED VIEW | Snowflake Documentation
---

## Applies to[¶](#applies-to)

- PostgreSQL
- Greenplum
- Netezza

## Description[¶](#description)

In SnowConvert AI, Materialized Views are transformed into Snowflake Dynamic Tables. To properly
configure Dynamic Tables, two essential parameters must be defined: TARGET_LAG and WAREHOUSE. If
these parameters are left unspecified in the configuration options, SnowConvert AI will default to
preassigned values during the conversion, as demonstrated in the example below.

## Grammar Syntax[¶](#grammar-syntax)

```
CREATE MATERIALIZED VIEW [ IF  NOT EXISTS ] <table_name>
    [ (<column_name> [, ...] ) ]
    [ USING <method> ]
    [ WITH ( <storage_parameter> [= <value>] [, ... ] ) ]
    [ TABLESPACE <tablespace_name> ]
    AS <query>
    [ WITH [ NO ] DATA ]
```

## Code Examples[¶](#code-examples)

### Simple Case[¶](#simple-case)

Input Code:

#### PostgreSQL[¶](#postgresql)

```
CREATE MATERIALIZED VIEW product_summary AS
SELECT
    category,
    COUNT(*) AS total_products,
    MAX(price) AS max_price
FROM products
GROUP BY category;
```

Output Code:

##### Snowflake[¶](#snowflake)

```
CREATE OR REPLACE DYNAMIC TABLE product_summary
--** SSC-FDM-0031 - DYNAMIC TABLE REQUIRED PARAMETERS SET BY DEFAULT **
TARGET_LAG='1 day'
WAREHOUSE=UPDATE_DUMMY_WAREHOUSE
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "postgresql",  "convertedOn": "05/14/2025",  "domain": "no-domain-provided" }}'
AS
SELECT
    category,
    COUNT(*) AS total_products,
    MAX(price) AS max_price
FROM
    products
GROUP BY category;
```

### IF NOT EXISTS[¶](#if-not-exists)

Hint

This syntax is fully supported in Snowflake.

This clause has been removed during the migration from PostgreSQL to Snowflake.

### USING, TABLESPACE, and WITH[¶](#using-tablespace-and-with)

**Note:**

This syntax is not needed in Snowflake.

These clauses are removed during the conversion process. In PostgreSQL, they are used to further
customize data storage manually. This is something that Snowflake handles automatically (micro
partitions), and it is typically not a concern.

## Related EWIs[¶](#related-ewis)

1. [SSC-FDM-0031](../../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0031):
   Dynamic Table required parameters set by default
