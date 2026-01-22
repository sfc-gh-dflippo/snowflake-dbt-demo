---
description: Translation reference to convert Oracle Materialized View to Snowflake Dynamic Table
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/oracle/sql-translation-reference/create-materialized-view
title: SnowConvert AI - Oracle - Create Materialized Views | Snowflake Documentation
---

## Description

In SnowConvert AI, Oracle Materialized Views are transformed into Snowflake Dynamic Tables. To
properly configure Dynamic Tables, two essential parameters must be defined: TARGET_LAG and
WAREHOUSE. If these parameters are left unspecified in the configuration options, SnowConvert AI
will default to preassigned values during the conversion, as demonstrated in the example below.

For more information on Materialized Views, click
[here](https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/CREATE-MATERIALIZED-VIEW.html).

For details on the necessary parameters for Dynamic Tables, click
[here](https://docs.snowflake.com/en/sql-reference/sql/create-dynamic-table).

## Sample Source Patterns

### Oracle

```sql
CREATE MATERIALIZED VIEW sales_total
AS
SELECT SUM(amount) AS total_sales
FROM sales;
```

### Snowflake

```sql
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

### Refresh Modes

Snowflake dynamic tables support an equivalent to Oracle’s materialized view refresh modes. The
corresponding modes are as follows:

- **Oracle**:

  - **FAST**: Refreshes only the rows that have changed.
  - **COMPLETE**: Refreshes the entire materialized view.
  - **FORCE**: Uses FAST if possible, otherwise uses COMPLETE.

- **Snowflake**:
  - **AUTO**: Automatically determines the best refresh method.
  - **FULL**: Refreshes the entire table, equivalent to Oracle’s COMPLETE mode.
  - **INCREMENTAL**: Refreshes only the changed rows.

#### Default Refresh Mode

When using SnowConvert AI, the dynamic table’s default refresh mode is **AUTO**.

#### Mode Mappings

- **Oracle FAST** and **FORCE** -> **Snowflake AUTO**
- **Oracle COMPLETE** -> **Snowflake FULL**

For more details, refer to the official documentation on
[Oracle Refresh Modes](https://docs.oracle.com/en/database/oracle/oracle-database/12.2/dwhsg/refreshing-materialized-views.html)
and
[Snowflake Refresh Modes](https://docs.snowflake.com/en/sql-reference/sql/create-dynamic-table#optional-parameters).

##### Oracle 2

```sql
CREATE MATERIALIZED VIEW CUSTOMER_SALES_SUMMARY
REFRESH COMPLETE
AS
SELECT
    CUSTOMER_ID,
    SUM(AMOUNT) AS TOTAL_AMOUNT
FROM
    SALES
GROUP BY
    CUSTOMER_ID;
```

##### Snowflake 2

```sql
CREATE OR REPLACE DYNAMIC TABLE CUSTOMER_SALES_SUMMARY
--** SSC-FDM-0031 - DYNAMIC TABLE REQUIRED PARAMETERS SET BY DEFAULT **
TARGET_LAG='1 day'
WAREHOUSE=UPDATE_DUMMY_WAREHOUSE
REFRESH_MODE=FULL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
AS
SELECT
   CUSTOMER_ID,
   SUM(AMOUNT) AS TOTAL_AMOUNT
FROM
   SALES
GROUP BY
   CUSTOMER_ID;
```

## Known Issues

No known errors detected at this time.

## Related EWIs

1. [SSC-FDM-0031](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0031):
   Dynamic Table required parameters set by default
