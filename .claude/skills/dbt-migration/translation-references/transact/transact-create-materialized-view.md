---
description: Translation reference to convert Materialized View to Snowflake Dynamic Table
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/transact/transact-create-materialized-view
title: SnowConvert AI - SQL Server-Azure Synapse - Materialized View | Snowflake Documentation
---

## Description[¶](#description)

In SnowConvert AI, Materialized Views are transformed into Snowflake Dynamic Tables. To properly
configure Dynamic Tables, two essential parameters must be defined: TARGET_LAG and WAREHOUSE. If
these parameters are left unspecified in the configuration options, SnowConvert AI will default to
preassigned values during the conversion, as demonstrated in the example below.

For more information on Materialized Views, click
[here](https://learn.microsoft.com/en-us/sql/t-sql/statements/create-materialized-view-as-select-transact-sql?view=azure-sqldw-latest).

For details on the necessary parameters for Dynamic Tables, click
[here](https://docs.snowflake.com/en/sql-reference/sql/create-dynamic-table).

## Sample Source Patterns[¶](#sample-source-patterns)

### SQL Server[¶](#sql-server)

```
CREATE MATERIALIZED VIEW sales_total
AS
SELECT SUM(amount) AS total_sales
FROM sales;
```

Copy

### Snowflake[¶](#snowflake)

```
 CREATE OR REPLACE DYNAMIC TABLE sales_total
--** SSC-FDM-0031 - DYNAMIC TABLE REQUIRED PARAMETERS SET BY DEFAULT **
TARGET_LAG='1 day'
WAREHOUSE=UPDATE_DUMMY_WAREHOUSE
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
AS
SELECT SUM(amount) AS total_sales
FROM
sales;
```

Copy

## Related EWIs[¶](#related-ewis)

1. [SSC-FMD-0031](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0031):
   Dynamic Table required parameters set by default
