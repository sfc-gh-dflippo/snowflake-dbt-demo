---
description: Translation from Greenplum to Snowflake
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/postgres/ddls/create-materialized-view/greenplum-create-materialized-view
title: SnowConvert AI - Greenplum - CREATE MATERIALIZED VIEW | Snowflake Documentation
---

## Description[¶](#description)

This section explains features exclusive to Greenplum.

For more information, please refer to
[`CREATE MATERIALIZE VIEW`](https://techdocs.broadcom.com/us/en/vmware-tanzu/data-solutions/tanzu-greenplum/7/greenplum-database/ref_guide-sql_commands-CREATE_MATERIALIZED_VIEW.html)
the documentation.

## Grammar Syntax[¶](#grammar-syntax)

```
CREATE MATERIALIZED VIEW <table_name>
AS <query>
[
    DISTRIBUTED {
        BY <column> [<opclass>], [ ... ] | RANDOMLY | REPLICATED
        }
]
```

## DISTRIBUTED BY[¶](#distributed-by)

Hint

This syntax is translated to its most equivalent form in Snowflake.

The DISTRIBUTED BY clause in Greenplum controls how data is physically distributed across the
system’s segments. Meanwhile, CLUSTER BY is a subset of columns in a dynamic table (or expressions
on a dynamic table) explicitly designated to co-locate the data in the table in the same
micro-partitions. While they operate at different architectural levels, they aim to improve query
performance by distributing data efficiently.

### Grammar Syntax[¶](#id1)

```
DISTRIBUTED BY ( <column> [<opclass>] [, ... ] )
```

### Sample Source[¶](#sample-source)

Input Code:

#### Greenplum[¶](#greenplum)

```
CREATE MATERIALIZED VIEW product_summary AS
SELECT
    category,
    COUNT(*) AS total_products,
    MAX(price) AS max_price
FROM products
GROUP BY category
DISTRIBUTED BY (category);
```

Output Code:

##### Snowflake[¶](#snowflake)

```
CREATE OR REPLACE DYNAMIC TABLE product_summary
--** SSC-FDM-0031 - DYNAMIC TABLE REQUIRED PARAMETERS SET BY DEFAULT **
TARGET_LAG='1 day'
WAREHOUSE=UPDATE_DUMMY_WAREHOUSE
--** SSC-FDM-GP0001 - THE PERFORMANCE OF THE CLUSTER BY MAY VARY COMPARED TO THE PERFORMANCE OF DISTRIBUTED BY **
CLUSTER BY (category)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "greenplum",  "convertedOn": "04/24/2025",  "domain": "test" }}'
AS
    SELECT
    category,
    COUNT(*) AS total_products,
    MAX(price) AS max_price
FROM
    products
    GROUP BY category;
```

## DISTRIBUTED RANDOMLY - REPLICATED[¶](#distributed-randomly-replicated)

**Note:**

This syntax is not needed in Snowflake.

The DISTRIBUTED REPLICATED or DISTRIBUTED RANDOMLY clause in Greenplum controls how data is
physically distributed across the system’s segments. As Snowflake automatically handles data
storage, these options will be removed in the migration.

## Related EWIs[¶](#related-ewis)

1. [SSC-FDM-GP0001](../../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/greenplumFDM.html#ssc-fdm-gp0001):
   The performance of the CLUSTER BY may vary compared to the performance of Distributed By.
