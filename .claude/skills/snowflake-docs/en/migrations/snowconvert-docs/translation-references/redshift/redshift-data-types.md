---
auto_generated: true
description: Current Data types conversion for Redshift in SnowConvert AI.
last_scraped: '2026-01-14T16:53:38.253396+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/redshift/redshift-data-types
title: SnowConvert AI - Redshift - Data types | Snowflake Documentation
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)Translation References[Redshift](README.md)Data types

# SnowConvert AI - Redshift - Data types[¶](#snowconvert-ai-redshift-data-types "Link to this heading")

Current Data types conversion for Redshift in SnowConvert AI.

Snowflake supports most basic [SQL data types](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types) (with some restrictions) for use in columns, local variables, expressions, parameters, and any other appropriate/suitable locations.

## Numeric Data Types [¶](#numeric-data-types "Link to this heading")

| Redshift | Snowflake | Notes |
| --- | --- | --- |
| INT | INT | Snowflake’s INT is an alias for NUMBER. |
| INT2 | SMALLINT | Snowflake’s INT2 is an alias for NUMBER. |
| INT4 | INTEGER | Snowflake’s INT4 is an alias for NUMBER. |
| INT8 | INTEGER | Snowflake’s INT8 is an alias for NUMBER. |
| INTEGER | INTEGER | Snowflake’s INTEGER is an alias for NUMBER. |
| BIGINT | BIGINT | Snowflake’s BIGINT is an alias for NUMBER. |
| DECIMAL | DECIMAL | Snowflake’s DECIMAL is an alias for NUMBER. |
| DOUBLE PRECISION | DOUBLE PRECISION | Snowflake’s DOUBLE PRECISION is an alias for FLOAT. |
| NUMERIC​ | NUMERIC | Snowflake’s NUMERIC is an alias for NUMBER. |
| SMALLINT | SMALLINT | Snowflake’s SMALLINT is an alias for NUMBER. |
| FLOAT | FLOAT | Snowflake uses double-precision (64 bit) IEEE 754 floating-point numbers. |
| FLOAT4 | FLOAT4 | Snowflake’s FLOAT4 is an alias for FLOAT. |
| FLOAT8 | FLOAT8 | Snowflake’s FLOAT8 is an alias for FLOAT. |
| REAL | REAL​ | Snowflake’s REAL is an alias for FLOAT. |

## Character Types [¶](#character-types "Link to this heading")

| Redshift | Snowflake | Notes |
| --- | --- | --- |
| VARCHAR | VARCHAR | VARCHAR holds Unicode UTF-8 characters. If no length is specified, the default is the maximum allowed length (16,777,216). |
| CHAR | CHAR | Snowflake’s CHAR is an alias for VARCHAR. |
| CHARACTER | CHARACTER | Snowflake’s CHARACTER is an alias for VARCHAR. |
| NCHAR | NCHAR | Snowflake’s NCHAR is an alias for VARCHAR. |
| BPCHAR | VARCHAR | BPCHAR data type is **not supported** in Snowflake. VARCHAR is used instead. For more information please refer to [SSC-FDM-PG0002](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/postgresqlFDM.html#ssc-fdm-pg0002). |
| NVARCHAR | NVARCHAR | Snowflake’s NVARCHAR is an alias for VARCHAR. |
| CHARACTER VARYING | CHARACTER VARYING | Snowflake’s CHARACTER VARYING is an alias for VARCHAR. |
| NATIONAL CHARACTER | NCHAR | Snowflake’s NCHAR is an alias for VARCHAR. |
| NATIONAL CHARACTER VARYING | NCHAR VARYING | Snowflake’s NCHAR VARYING is an alias for VARCHAR. |
| TEXT | TEXT | Snowflake’s TEXT is an alias for VARCHAR. |
| [NAME](https://www.postgresql.org/docs/current/datatype-character.html) (Special character type) | VARCHAR | VARCHAR holds Unicode UTF-8 characters. If no length is specified, the default is the maximum allowed length (16,777,216). |

Note

When the MAX precision argument is present in the Redshift data types, they are transformed to the default max precision supported by Snowflake.

## Boolean Types [¶](#boolean-types "Link to this heading")

| Redshift | Snowflake | Notes |
| --- | --- | --- |
| BOOL | BOOLEAN |  |
| BOOLEAN | BOOLEAN |  |

## Binary Data Types [¶](#binary-data-types "Link to this heading")

| Redshift | Snowflake | Notes |
| --- | --- | --- |
| VARBYTE | VARBINARY | VARBINARY is synonymous with BINARY. |
| VARBINARY | VARBINARY | VARBINARY is synonymous with BINARY. |
| BINARY | BINARY | The maximum length is 8 MB (8,388,608 bytes) |
| BINARY VARYING | BINARY VARYING | BINARY VARYING is synonymous with BINARY. |

Warning

The maximum length for binary types in Redshift is 16 MB (16,777,216 bytes), however in [Snowflake](https://docs.snowflake.com/en/sql-reference/data-types-text#data-types-for-binary-strings) it is 8 MB (8,388,608 bytes). Please consider this reduction in the maximum length.

## Date & Time Data Types [¶](#date-time-data-types "Link to this heading")

| Redshift | Snowflake | Notes |
| --- | --- | --- |
| DATE | DATE | DATE accepts dates in the most common forms (`YYYY-MM-DD`, `DD-MON-YYYY`, etc.) |
| TIME | TIME | Storing times in the form of `HH:MI:SS`. Time precision can range from 0 (seconds) to 9 (nanoseconds). The default precision is 9. |
| TIMETZ | TIME | Time zone not supported for time data type. For more information please refer to [SSC-FDM-0005](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0005). |
| TIME WITH TIME ZONE | TIME | Time zone not supported for time data type. For more information please refer to [SSC-FDM-0005](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0005). |
| TIME WITHOUT TIME ZONE | TIME | Snowflake supports a single TIME data type for storing times in the form of `HH:MI:SS`. |
| TIMESTAMP | TIMESTAMP | Timestamp precision can range from 0 (seconds) to 9 (nanoseconds). |
| TIMESTAMPTZ | TIMESTAMP\_TZ | TIMESTAMP\_TZ internally stores UTC time together with an associated *time zone offset*. |
| TIMESTAMP WITH TIME ZONE | TIMESTAMP\_TZ | TIMESTAMP\_TZ internally stores UTC time together with an associated *time zone offset*. |
| TIMESTAMP WITHOUT TIME ZONE | TIMESTAMP\_NTZ | TIMESTAMP\_NTZ internally stores “wallclock” time with a specified precision. |
| INTERVAL YEAR TO MONTH | VARCHAR | The interval data type is not supported by Snowflake. Transformed to VARCHAR. |
| INTERVAL DAY TO SECOND | VARCHAR | The interval data type is not supported by Snowflake. Transformed to VARCHAR. |

## Other data types [¶](#other-data-types "Link to this heading")

| Redshift | Snowflake | Notes |
| --- | --- | --- |
| GEOMETRY | GEOMETRY | The coordinates are represented as pairs of real numbers (x, y). Currently, only 2D coordinates are supported. |
| GEOGRAPHY | GEOGRAPHY | The GEOGRAPHY data type follows the WGS 84 standard. |
| HLLSKETCH | N/A | Data type not supported in Snowflake. For more information please refer to [SSC-EWI-RS0004](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/redshiftEWI.html#ssc-ewi-rs0004). |
| SUPER | VARIANT | Can contain a value of any other data type, including OBJECT and ARRAY values. |

## Related EWIs[¶](#related-ewis "Link to this heading")

1. [SSC-FDM-PG0002](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/postgresqlFDM.html#ssc-fdm-pg0002): Bpchar converted to varchar.
2. [SSC-FDM-0005](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0005): TIME ZONE not supported for time data type.
3. [SSC-EWI-0036](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0036): Data type converted to another data type.
4. [SSC-EWI-RS0004](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/redshiftEWI.html#ssc-ewi-rs0004): HLLSKETCH data type not supported in Snowflake.

## INTERVAL DAY TO SECOND Data Type[¶](#interval-day-to-second-data-type "Link to this heading")

### Description[¶](#description "Link to this heading")

> INTERVAL DAY TO SECOND specify an interval literal to define a duration in days, hours, minutes, and seconds. ([RedShift SQL Language Reference Interval data type](https://docs.aws.amazon.com/redshift/latest/dg/r_interval_data_types.html#r_interval_data_types-syntax))

There is no equivalent for this data type in Snowflake, it is currently transformed to `VARCHAR`.

### Grammar Syntax [¶](#grammar-syntax "Link to this heading")

```
 INTERVAL day_to_second_qualifier [ (fractional_precision) ]

day_to_second_qualifier:
{ DAY | HOUR | MINUTE | SECOND | DAY TO HOUR | DAY TO MINUTE | DAY TO SECOND | 
HOUR TO MINUTE | HOUR TO SECOND | MINUTE TO SECOND }
```

Copy

Warning

The use of the Interval data type is planned for implementation in future updates.

### Sample Source Patterns[¶](#sample-source-patterns "Link to this heading")

#### Interval Day to Second in Create Table[¶](#interval-day-to-second-in-create-table "Link to this heading")

##### Input[¶](#input "Link to this heading")

##### Redshift[¶](#redshift "Link to this heading")

```
 CREATE TABLE interval_day_to_second_table
(
	interval_day_col1 INTERVAL DAY TO HOUR,
	interval_day_col2 INTERVAL DAY TO SECOND(4)
);

INSERT INTO interval_day_to_second_table(interval_day_col1) VALUES ( INTERVAL '1 2' DAY TO HOUR ); 
INSERT INTO interval_day_to_second_table(interval_day_col2) VALUES ( INTERVAL '1 2:3:4.56' DAY TO SECOND(4));
```

Copy

##### Output[¶](#output "Link to this heading")

##### Snowflake[¶](#snowflake "Link to this heading")

```
 CREATE TABLE interval_day_to_second_table
(
	interval_day_col1 VARCHAR !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - INTERVAL DAY TO HOUR DATA TYPE CONVERTED TO VARCHAR ***/!!!,
	interval_day_col2 VARCHAR !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - INTERVAL DAY TO SECOND(4) DATA TYPE CONVERTED TO VARCHAR ***/!!!
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"redshift"}}'
;

INSERT INTO interval_day_to_second_table(interval_day_col1) VALUES ('1days, 2hours');

INSERT INTO interval_day_to_second_table(interval_day_col2) VALUES ('1days, 2hours, 3mins, 4secs, 56ms');
```

Copy

The Interval value is transformed to a supported Snowflake format and then inserted as text inside the column. Since Snowflake does not support **Interval** as a data type, it is only supported in arithmetic operations. In order to use the value, it needs to be extracted and used as an [Interval constant](https://docs.snowflake.com/en/sql-reference/data-types-datetime.html#interval-constants) (if possible).

**Original Oracle value:** `INTERVAL '1 2:3:4.567' DAY TO SECOND`

**Value stored in Snowflake column:** `'1days, 2hours, 3mins, 4secs, 56ms'`

**Value as Snowflake Interval constant:** `INTERVAL '1days, 2hours, 3mins, 4secs, 56ms'`

#### Retrieving data from an Interval Day to Second column[¶](#retrieving-data-from-an-interval-day-to-second-column "Link to this heading")

##### Input[¶](#id1 "Link to this heading")

##### Redshift[¶](#id2 "Link to this heading")

```
 SELECT * FROM interval_day_to_second_table;
```

Copy

##### Result[¶](#result "Link to this heading")

| interval\_day\_col1 | interval\_day\_col2 |
| --- | --- |
| 1 days 2 hours 0 mins 0.0 secs | NULL |
| NULL | 1 days 2 hours 3 mins 4.56 secs |

##### Output[¶](#id3 "Link to this heading")

##### Snowflake[¶](#id4 "Link to this heading")

```
 SELECT * FROM
interval_day_to_second_table;
```

Copy

##### Result[¶](#id5 "Link to this heading")

| interval\_day\_col1 | interval\_day\_col2 |
| --- | --- |
| 1d, 2h | NULL |
| NULL | 1d, 2h, 3m, 4s, 56ms |

### Known Issues[¶](#known-issues "Link to this heading")

#### 1. Only arithmetic operations are supported[¶](#only-arithmetic-operations-are-supported "Link to this heading")

Snowflake Intervals have several limitations. Only arithmetic operations between `DATE` or `TIMESTAMP` and [Interval Constants](https://docs.snowflake.com/en/sql-reference/data-types-datetime.html#interval-constants) are supported, every other scenario is not supported.

### Related EWIs[¶](#id6 "Link to this heading")

1. [SSC-EWI-0036](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0036): Data type converted to another data type.

## INTERVAL YEAR TO MONTH Data Type[¶](#interval-year-to-month-data-type "Link to this heading")

### Description[¶](#id7 "Link to this heading")

> INTERVAL YEAR TO MONTH specify an interval data type to store a duration of time in years and months. ([RedShift SQL Language Reference Interval data type](https://docs.aws.amazon.com/redshift/latest/dg/r_interval_data_types.html#r_interval_data_types-syntax))

There is no equivalent for this data type in Snowflake, it is currently transformed to VARCHAR.

### Grammar Syntax [¶](#id8 "Link to this heading")

```
 INTERVAL {YEAR | MONTH | YEAR TO MONTH}
```

Copy

Warning

The use of the Interval data type is planned for implementation in future updates.

### Sample Source Patterns[¶](#id9 "Link to this heading")

#### Interval Year To Month in Create Table[¶](#interval-year-to-month-in-create-table "Link to this heading")

##### Input:[¶](#id10 "Link to this heading")

##### Redshift[¶](#id11 "Link to this heading")

```
 CREATE TABLE interval_year_to_month_table
(
	interval_year_col1 INTERVAL YEAR,
	interval_year_col2 INTERVAL MONTH,
 	interval_year_col3 INTERVAL YEAR TO MONTH
);

INSERT INTO interval_year_to_month_table(interval_year_col1) VALUES ( INTERVAL '12' YEAR);
INSERT INTO interval_year_to_month_table(interval_year_col2) VALUES ( INTERVAL '5' MONTH);
INSERT INTO interval_year_to_month_table(interval_year_col3) VALUES ( INTERVAL '1000-11' YEAR TO MONTH );
```

Copy

##### Output[¶](#id12 "Link to this heading")

##### Snowflake[¶](#id13 "Link to this heading")

```
 CREATE TABLE interval_year_to_month_table
(
	interval_year_col1 VARCHAR !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - INTERVAL YEAR DATA TYPE CONVERTED TO VARCHAR ***/!!!,
	interval_year_col2 VARCHAR !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - INTERVAL MONTH DATA TYPE CONVERTED TO VARCHAR ***/!!!,
	interval_year_col3 VARCHAR !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - INTERVAL YEAR TO MONTH DATA TYPE CONVERTED TO VARCHAR ***/!!!
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"redshift"}}'
;

INSERT INTO interval_year_to_month_table(interval_year_col1) VALUES ('12year, 0mons');

INSERT INTO interval_year_to_month_table(interval_year_col2) VALUES ('0year, 5mons');

INSERT INTO interval_year_to_month_table(interval_year_col3) VALUES ('1000year, 11mons');
```

Copy

The Interval value is transformed to a supported Snowflake format and then inserted as text inside the column. Since Snowflake does not support **Interval** as a data type, it is only supported in arithmetic operations. In order to use the value, it needs to be extracted and used as an [Interval constant](https://docs.snowflake.com/en/sql-reference/data-types-datetime.html#interval-constants) (if possible).

**Original Redshift value:** `INTERVAL '1-2' YEAR TO MONTH`

**Value stored in Snowflake column:** `'1y, 2m'`

**Value as Snowflake Interval constant:** `INTERVAL '1y, 2m'`

#### Retrieving data from an Interval Year To Month column[¶](#retrieving-data-from-an-interval-year-to-month-column "Link to this heading")

##### Input[¶](#id14 "Link to this heading")

##### Redshift[¶](#id15 "Link to this heading")

```
 SELECT * FROM interval_year_to_month_table;
```

Copy

##### Result[¶](#id16 "Link to this heading")

| interval\_year\_col1 | interval\_year\_col2 | interval\_year\_col2 |
| --- | --- | --- |
| 12 years 0 mons | NULL | NULL |
| NULL | 0 years 5 mons | NULL |
| NULL | NULL | 1000 years 11 mons |

##### Output[¶](#id17 "Link to this heading")

##### Snowflake[¶](#id18 "Link to this heading")

```
 SELECT * FROM
interval_year_to_month_table;
```

Copy

##### Result[¶](#id19 "Link to this heading")

| interval\_year\_col1 | interval\_year\_col2 | interval\_year\_col2 |
| --- | --- | --- |
| 12 y 0 mm | NULL | NULL |
| NULL | 0 y 5 mm | NULL |
| NULL | NULL | 1000 y 11 mons |

### Known Issues[¶](#id20 "Link to this heading")

#### 1. Only arithmetic operations are supported[¶](#id21 "Link to this heading")

Snowflake Intervals have several limitations. Only arithmetic operations between `DATE` or `TIMESTAMP` and [Interval Constants](https://docs.snowflake.com/en/sql-reference/data-types-datetime.html#interval-constants) are supported, every other scenario is not supported.

### Related EWIs[¶](#id22 "Link to this heading")

* [SSC-EWI-0036](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0036): Data type converted to another data type.

## Numeric Format Models[¶](#numeric-format-models "Link to this heading")

### Description[¶](#id23 "Link to this heading")

These are the different Numeric Formats supported by [Redshift](https://docs.aws.amazon.com/redshift/latest/dg/r_Numeric_formating.html) and its equivalent in [Snowflake](https://docs.snowflake.com/en/sql-reference/sql-format-models#numeric-format-models).

| Redshift | Snowflake | Comments |
| --- | --- | --- |
| 0 | 0 |  |
| 9 | 9 |  |
| . (period), D | . (period), D |  |
| , (comma) | , (comma) |  |
| CC |  | Currently there is no equivalent for Century Code in Snowflake. |
| FM | FM |  |
| PR |  | Currently there is no equivalent for this format in Snowflake. |
| S | S | Explicit numeric sign. |
| L | $ | Currency symbol placeholder. |
| G | G |  |
| MI | MI | Minus sign (for negative numbers) |
| PL | S | Currently there is no equivalent for plus sign in Snowflake. So it is translated to the explicit numeric sign. |
| SG | S | Explicit numeric Sign in the specified position. |
| RN |  | Currently there is no equivalent for Roman Numerals in Snowflake. |
| TH |  | Currently there is no equivalent for Ordinal suffix in Snowflake |

### Sample Source Patterns[¶](#id24 "Link to this heading")

#### Uses in To\_Number function[¶](#uses-in-to-number-function "Link to this heading")

##### Input:[¶](#id25 "Link to this heading")

##### Redshift[¶](#id26 "Link to this heading")

```
 select to_number('09423', '999999999') as multiple_nines
    , to_number('09423', '00000') as exact_zeros
    , to_number('123.456', '999D999') as decimals
    , to_number('123,031.30', 'FM999,999D999') as fill_mode
    , to_number('$ 12,454.88', '$999,999.99') as currency
;
```

Copy

##### Results[¶](#results "Link to this heading")

| multiple\_nines | exact\_zeros | decimals | fill\_mode | currency |
| --- | --- | --- | --- | --- |
| 9423 | 9423 | 123.456 | 123031.30 | 1254.88 |

##### Output[¶](#id27 "Link to this heading")

##### Snowflake[¶](#id28 "Link to this heading")

```
 select to_number('09423', '999999999') !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR ''999999999'' NODE ***/!!! as multiple_nines
    , to_number('09423', '00000') !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR ''00000'' NODE ***/!!! as exact_zeros
    , to_number('123.456', '999D999') !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR ''999D999'' NODE ***/!!! as decimals
    , to_number('123,031.30', 'FM999,999D999') !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR ''FM999,999D999'' NODE ***/!!! as fill_mode
    , to_number('$ 12,454.88', '$999,999.99') !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR ''$999,999.99'' NODE ***/!!! as currency
;
```

Copy

##### Results[¶](#id29 "Link to this heading")

| multiple\_nines | exact\_zeros | decimals | fill\_mode | currency |
| --- | --- | --- | --- | --- |
| 9423 | 9423 | 123.456 | 123031.300 | 12454.88 |

##### Input:[¶](#id30 "Link to this heading")

##### Redshift[¶](#id31 "Link to this heading")

```
 select to_number('$ 12,454.88', 'FML99G999D99') as currency_L
    , to_number('123-', '999S') as signed_number_end
    , to_number('+12454.88', 'PL99G999D99') as plus_sign
    , to_number('-12,454.88', 'MI99G999D99') as minus_sign
    , to_number('-12,454.88', 'SG99G999D99') as signed_number
;
```

Copy

##### Results[¶](#id32 "Link to this heading")

| currency\_L | signed\_number\_end | plus\_sign | minus\_sign | signed\_number |
| --- | --- | --- | --- | --- |
| 12454.8 | -123 | 1254.88 | -12454.88 | -12454.88 |

##### Output:[¶](#id33 "Link to this heading")

##### Snowflake[¶](#id34 "Link to this heading")

```
 select to_number('$ 12,454.88', 'FML99G999D99') !!!RESOLVE EWI!!! /*** SSC-EWI-0006 - 'FML99G999D99' FORMAT MAY FAIL OR MAY HAVE A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/!!! as currency_L
    , to_number('123-', '999S') !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR ''999S'' NODE ***/!!! as signed_number_end
    , to_number('+12454.88', 'PL99G999D99') !!!RESOLVE EWI!!! /*** SSC-EWI-0006 - 'PL99G999D99' FORMAT MAY FAIL OR MAY HAVE A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/!!! as plus_sign
    , to_number('-12,454.88', 'MI99G999D99') !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR ''MI99G999D99'' NODE ***/!!! as minus_sign
    , to_number('-12,454.88', 'SG99G999D99') !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR ''SG99G999D99'' NODE ***/!!! as signed_number
;
```

Copy

##### Results[¶](#id35 "Link to this heading")

| currency\_L | signed\_number\_end | plus\_sign | minus\_sign | signed\_number |
| --- | --- | --- | --- | --- |
| 12454.8 | -123 | 1254.88 | -12454.88 | -12454.88 |

#### Uses in To\_Char function[¶](#uses-in-to-char-function "Link to this heading")

##### Input:[¶](#id36 "Link to this heading")

##### Redshift[¶](#id37 "Link to this heading")

```
 select to_char(-123, '999S') as signed_number
    , to_char(12454.88, 'FM99G999D99') as decimal_number
    , to_char(-12454.88, '99G999D99') as negative
    , to_char(-12454.88, 'MI99G999D99') as minus_sign
    , to_char(+12454.88, 'PL99G999D99') as plus_sign
    , to_char(09423, '999999999') as multiple_nines
    , to_char(09423, '00000') as exact_zeros
;
```

Copy

##### Results[¶](#id38 "Link to this heading")

| signed\_number | decimal\_number | negative | minus\_sign | plus\_sign | multiple\_ninesmultiple\_nines | exact\_zerosexact\_zeros |
| --- | --- | --- | --- | --- | --- | --- |
| '123-' | '12,454.88' | '-12,454.88' | '12454.88' | '-12,454.88' | '09423' | '09423' |

##### Output:[¶](#id39 "Link to this heading")

##### Snowflake[¶](#id40 "Link to this heading")

```
 select
    TO_CHAR(-123, '999S') as signed_number,
    TO_CHAR(12454.88, 'FM99G999D99') as decimal_number,
    TO_CHAR(-12454.88, '99G999D99') as negative,
    TO_CHAR(-12454.88, 'MI99G999D99') as minus_sign,
    TO_CHAR(+12454.88, 'S99G999D99') as plus_sign,
    TO_CHAR(09423, '999999999') as multiple_nines,
    TO_CHAR(09423, '00000') as exact_zeros
;
```

Copy

##### Results[¶](#id41 "Link to this heading")

| signed\_number | decimal\_number | negative | minus\_sign | plus\_sign | multiple\_ninesmultiple\_nines | exact\_zerosexact\_zeros |
| --- | --- | --- | --- | --- | --- | --- |
| '123-' | '12,454.88' | '-12,454.88' | '12454.88' | '-12,454.88' | '09423' | '09423' |

#### Unsupported format[¶](#unsupported-format "Link to this heading")

The following format is not supported, for which it will be marked with an EWI.

##### Input:[¶](#id42 "Link to this heading")

```
 SELECT to_char(123031, 'th999,999')
```

Copy

##### Output:[¶](#id43 "Link to this heading")

```
 SELECT
TO_CHAR(123031, 'th999,999') !!!RESOLVE EWI!!! /*** SSC-EWI-0006 - th999,999 FORMAT MAY FAIL OR MAY HAVE A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/!!!
```

Copy

### Know Issues[¶](#know-issues "Link to this heading")

#### 1. Using numeric signs inside the number not supported.[¶](#using-numeric-signs-inside-the-number-not-supported "Link to this heading")

When any numeric sign format (MI, SG or PL) is used inside the number, instead of at the start, or at the end of the number is not supported in snowflake

Example

```
 select to_number('12,-454.88', '99GMI999D99')
```

Copy

### Related EWIs[¶](#id44 "Link to this heading")

* [SSC-EWI-0006](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0006): The current date/numeric format may have a different behavior in Snowflake.

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

1. [Numeric Data Types](#numeric-data-types)
2. [Character Types](#character-types)
3. [Boolean Types](#boolean-types)
4. [Binary Data Types](#binary-data-types)
5. [Date & Time Data Types](#date-time-data-types)
6. [Other data types](#other-data-types)
7. [Related EWIs](#related-ewis)
8. [INTERVAL DAY TO SECOND Data Type](#interval-day-to-second-data-type)
9. [INTERVAL YEAR TO MONTH Data Type](#interval-year-to-month-data-type)
10. [Numeric Format Models](#numeric-format-models)