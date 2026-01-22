---
auto_generated: true
description: This user-defined function (UDF) is used to multiply an interval of time
  with a value of ‘N’ times.
last_scraped: '2026-01-14T16:52:36.473591+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/function-references/shared/README
title: SnowConvert AI - Function References - Shared | Snowflake Documentation
---

1. [Overview](../../../../../../guides/README.md)
2. [Snowflake Horizon Catalog](../../../../../../user-guide/snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../../../../../../guides/overview-connecting.md)
6. [Virtual warehouses](../../../../../../user-guide/warehouses.md)
7. [Databases, Tables, & Views](../../../../../../guides/overview-db.md)
8. [Data types](../../../../../../data-types.md)
10. Data Integration

    - [Snowflake Openflow](../../../../../../user-guide/data-integration/openflow/about.md)
    - Apache Iceberg™

      - [Apache Iceberg™ Tables](../../../../../../user-guide/tables-iceberg.md)
      - [Snowflake Open Catalog](../../../../../../user-guide/opencatalog/overview.md)
11. Data engineering

    - [Data loading](../../../../../../guides/overview-loading-data.md)
    - [Dynamic Tables](../../../../../../user-guide/dynamic-tables-about.md)
    - [Streams and Tasks](../../../../../../user-guide/data-pipelines-intro.md)
    - [dbt Projects on Snowflake](../../../../../../user-guide/data-engineering/dbt-projects-on-snowflake.md)
    - [Data Unloading](../../../../../../guides/overview-unloading-data.md)
12. [Storage Lifecycle Policies](../../../../../../user-guide/storage-management/storage-lifecycle-policies.md)
13. [Migrations](../../../../../README.md)

    * Tools

      * [SnowConvert AI](../../../../overview.md)

        + General

          + [About](../../../about.md)
          + [Getting Started](../../../getting-started/README.md)
          + [Terms And Conditions](../../../terms-and-conditions/README.md)
          + [Release Notes](../../../release-notes/release-notes/README.md)
          + User Guide

            + [SnowConvert AI](../../../user-guide/snowconvert/README.md)
            + [Project Creation](../../../user-guide/project-creation.md)
            + [Extraction](../../../user-guide/extraction.md)
            + [Deployment](../../../user-guide/deployment.md)
            + [Data Migration](../../../user-guide/data-migration.md)
            + [Data Validation](../../../user-guide/data-validation.md)
            + [Power BI Repointing](../../../user-guide/power-bi-repointing-general.md)
            + [ETL Migration](../../../user-guide/etl-migration-replatform.md)
          + [Technical Documentation](../../README.md)

            - [Considerations](../../considerations/README.md)
            - [Issues And Troubleshooting](../../issues-and-troubleshooting/README.md)
            - Function References

              - [SnowConvert AI Udfs](../snowconvert-udfs.md)
              - [Teradata](../teradata/README.md)
              - [Oracle](../oracle/README.md)
              - [Shared](README.md)
              - [SQL Server](../sql-server/README.md)
          + [Contact Us](../../../contact-us.md)
          + Others

            + [Using SnowConvert AI In A Ubuntu Docker Image](../../../others/using-snowconvert-in-a-ubuntu-docker-image.md)
          + [Frequently Asked Questions (FAQ)](../../../frequently-asked-questions-faq.md)")
        + Translation References

          + [General](../../../../translation-references/general/README.md)
          + [Teradata](../../../../translation-references/teradata/README.md)
          + [Oracle](../../../../translation-references/oracle/README.md)
          + [SQL Server-Azure Synapse](../../../../translation-references/transact/README.md)
          + [Sybase IQ](../../../../translation-references/sybase/README.md)
          + [Hive-Spark-Databricks SQL](../../../../translation-references/hive/README.md)
          + [Redshift](../../../../translation-references/redshift/README.md)
          + [PostgreSQL-Greenplum-Netezza](../../../../translation-references/postgres/README.md)
          + [BigQuery](../../../../translation-references/bigquery/README.md)
          + [Vertica](../../../../translation-references/vertica/README.md)
          + [IBM DB2](../../../../translation-references/db2/README.md)
          + [SSIS](../../../../translation-references/ssis/README.md)
        + [Migration Assistant](../../../../migration-assistant/README.md)
        + [Data Validation CLI](../../../../data-validation-cli/index.md)
        + [AI Verification](../../../../snowconvert-ai-verification.md)
      * [Snowpark Migration Accelerator](../../../../../sma-docs/README.md)
    * Guides

      * [Teradata](../../../../../guides/teradata.md)
      * [Databricks](../../../../../guides/databricks.md)
      * [SQL Server](../../../../../guides/sqlserver.md)
      * [Amazon Redshift](../../../../../guides/redshift.md)
      * [Oracle](../../../../../guides/oracle.md)
      * [Azure Synapse](../../../../../guides/azuresynapse.md)
15. [Queries](../../../../../../guides/overview-queries.md)
16. [Listings](../../../../../../collaboration/collaboration-listings-about.md)
17. [Collaboration](../../../../../../guides/overview-sharing.md)
19. [Snowflake AI & ML](../../../../../../guides/overview-ai-features.md)
21. [Snowflake Postgres](../../../../../../user-guide/snowflake-postgres/about.md)
23. [Alerts & Notifications](../../../../../../guides/overview-alerts.md)
25. [Security](../../../../../../guides/overview-secure.md)
26. [Data Governance](../../../../../../guides/overview-govern.md)
27. [Privacy](../../../../../../guides/overview-privacy.md)
29. [Organizations & Accounts](../../../../../../guides/overview-manage.md)
30. [Business continuity & data recovery](../../../../../../user-guide/replication-intro.md)
32. [Performance optimization](../../../../../../guides/overview-performance.md)
33. [Cost & Billing](../../../../../../guides/overview-cost.md)

[Guides](../../../../../../guides/README.md)[Migrations](../../../../../README.md)Tools[SnowConvert AI](../../../../overview.md)General[Technical Documentation](../../README.md)Function ReferencesShared

# SnowConvert AI - Function References - Shared[¶](#snowconvert-ai-function-references-shared "Link to this heading")

## INTERVAL\_MULTIPLY\_UDF (VARCHAR, VARCHAR, INTEGER)[¶](#interval-multiply-udf-varchar-varchar-integer "Link to this heading")

### Definition[¶](#definition "Link to this heading")

This user-defined function (UDF) is used to multiply an interval of time with a value of ‘N’ times.

```
INTERVAL_MULTIPLY_UDF
(INPUT_PART VARCHAR(30), INPUT_VALUE VARCHAR(), INPUT_MULT INTEGER)
```

Copy

### Parameters[¶](#parameters "Link to this heading")

`INPUT_PART` VARCHAR

The format of the operation. E.g.: `DAY`, `HOUR TO SECOND,` `YEAR TO MONTH`.

`INPUT_VALUE` VARCHAR

The interval of time to be multiplied.

`INPUT_MULT` INTEGER

The time to multiply the interval of time.

### Returns[¶](#returns "Link to this heading")

Returns a varchar with the result of the multiplication.

### Usage example[¶](#usage-example "Link to this heading")

Input:

```
SELECT INTERVAL_MULTIPLY_UDF('DAY', '2', 100);
```

Copy

Output:

```
200
```

Copy

## TRUNC\_UDF (TIMESTAMP\_LTZ, VARCHAR)[¶](#trunc-udf-timestamp-ltz-varchar "Link to this heading")

### Definition[¶](#id1 "Link to this heading")

This user-defined function (UDF) reproduces the Teradata and Oracle TRUNC(Date) functionality when the format parameter is specified.

```
TRUNC_UDF(DATE_TO_TRUNC TIMESTAMP_LTZ, DATE_FMT VARCHAR(5))
```

Copy

### Parameters[¶](#id2 "Link to this heading")

`DATE_TO_TRUNC` TIMESTAMP\_LTZ

A `timestamp_ltz` value to truncate which must be a date, timestamp, or timestamp with timezone.

`DATE_FMT` VARCHAR

A varchar value that should be one of the date formats supported by the `trunc` function.

### Returns[¶](#id3 "Link to this heading")

Returns a date truncated using the format specified.

### Usage example[¶](#id4 "Link to this heading")

Input:

```
SELECT TRUNC_UDF(TIMESTAMP '2015-08-18 12:30:00', 'Q')
```

Copy

Output:

```
2015-07-01
```

Copy

## INTERVAL\_TO\_SECONDS\_UDF (VARCHAR, VARCHAR)[¶](#interval-to-seconds-udf-varchar-varchar "Link to this heading")

### Definition[¶](#id5 "Link to this heading")

This user-defined function (UDF) is used to determine the quantity of seconds from an interval which is also correlated to the processed time type. This is an auxiliary function.

```
INTERVAL_TO_SECONDS_UDF
(INPUT_PART VARCHAR(30), INPUT_VALUE VARCHAR())
```

Copy

### Parameters[¶](#id6 "Link to this heading")

`INPUT_PART` VARCHAR

The related type of the second parameter. E.g. `DAY`, `DAY TO HOUR`, `HOUR`, `MINUTE`.

`INPUT_VALUE` VARCHAR

The value to be converted to seconds.

### Returns[¶](#id7 "Link to this heading")

Returns a decimal value type with the number of seconds.

### Usage example[¶](#id8 "Link to this heading")

Input:

```
SELECT INTERVAL_TO_SECONDS_UDF('DAY', '1');
```

Copy

Output:

```
86400.000000
```

Copy

## DATEDIFF\_UDF (DATE, STRING)[¶](#datediff-udf-date-string "Link to this heading")

### Definition[¶](#id9 "Link to this heading")

This user-defined function (UDF) is used to generate the difference between an interval value and a date.

```
DATEDIFF_UDF(D DATE, INTERVAL_VALUE STRING)
```

Copy

### Parameters[¶](#id10 "Link to this heading")

`D` DATE

The date to be used to process the difference with the interval.

`INTERVAL_VALUE` STRING

The interval value that will be used to create the difference from.

### Returns[¶](#id11 "Link to this heading")

Returns a date with the resulting value of the subtraction of time.

### Usage example[¶](#id12 "Link to this heading")

Input:

```
SELECT DATEDIFF_UDF('2024-01-30', 'INTERVAL ''2-1'' YEAR(2) TO MONTH');
```

Copy

Output:

```
2021-12-30
```

Copy

## SECONDS\_TO\_INTERVAL\_UDF (VARCHAR, NUMBER)[¶](#seconds-to-interval-udf-varchar-number "Link to this heading")

### Definition[¶](#id13 "Link to this heading")

This user-defined function (UDF) is used to transform seconds into intervals. This is an auxiliary function.

```
SECONDS_TO_INTERVAL_UDF
(INPUT_PART VARCHAR(30), INPUT_VALUE NUMBER)
```

Copy

### Parameters[¶](#id14 "Link to this heading")

`INPUT_PART` VARCHAR

The related type of the second parameter. E.g. `DAY`, `DAY TO HOUR`, `HOUR`, `MINUTE`, `MINUTE TO SECOND`.

`INPUT_VALUE` VARCHAR

The seconds to be converted to intervals.

### Returns[¶](#id15 "Link to this heading")

Returns

### Usage example[¶](#id16 "Link to this heading")

Input:

```
SELECT SECONDS_TO_INTERVAL_UDF('DAY TO SECOND', '86400');
```

Copy

Output:

```
1 000:000:000
```

Copy

## DATEADD\_UDF (STRING, DATE)[¶](#dateadd-udf-string-date "Link to this heading")

### Definition[¶](#id17 "Link to this heading")

This user-defined function (UDF) is used to add a date with an interval of time.

```
DATEADD_UDF(INTERVAL_VALUE STRING,D DATE)
```

Copy

### Parameters[¶](#id18 "Link to this heading")

`INTERVAL_VALUE` STRING

The interval of time to be added.

`D` DATE

The date to be added with the interval of time.

### Returns[¶](#id19 "Link to this heading")

Returns a date with the addition of the interval of time and the date.

### Usage example[¶](#id20 "Link to this heading")

Input:

```
SELECT DATEADD_UDF('INTERVAL ''2-1'' YEAR(2) TO MONTH', '2024-01-30');
```

Copy

Output:

```
2026-02-28
```

Copy

## DATEDIFF\_UDF (STRING, DATE)[¶](#datediff-udf-string-date "Link to this heading")

### Definition[¶](#id21 "Link to this heading")

This user-defined function (UDF) is used to generate the difference between an interval value and a date.

```
DATEDIFF_UDF(INTERVAL_VALUE STRING,D DATE)
```

Copy

### Parameters[¶](#id22 "Link to this heading")

`INTERVAL_VALUE` STRING

The interval value that will be used to create the difference from.

`D` DATE

The date to be used to process the difference with the interval.

### Returns[¶](#id23 "Link to this heading")

Returns a date with the resulting value of the subtraction of time.

### Usage example[¶](#id24 "Link to this heading")

Input:

```
SELECT DATEDIFF_UDF('INTERVAL ''2-1'' YEAR(2) TO MONTH', '2024-01-30');
```

Copy

Output:

```
2021-12-30
```

Copy

## DATEADD\_UDF (DATE, STRING)[¶](#dateadd-udf-date-string "Link to this heading")

### Definition[¶](#id25 "Link to this heading")

This user-defined function (UDF) is used to add a date with an interval of time.

```
DATEADD_UDF(D DATE, INTERVAL_VALUE STRING)
```

Copy

### Parameters[¶](#id26 "Link to this heading")

`D` DATE

The date to be added with the interval of time.

`INTERVAL_VALUE` STRING

The interval of time to be added.

### Returns[¶](#id27 "Link to this heading")

Returns a date with the addition of the interval of time and the date.

### Usage example[¶](#id28 "Link to this heading")

Input:

```
SELECT DATEADD_UDF('2024-01-30', 'INTERVAL ''1-1'' YEAR(2) TO MONTH');
```

Copy

Output:

```
2025-02-28
```

Copy

## TO\_INTERVAL\_UDF (TIME)[¶](#to-interval-udf-time "Link to this heading")

### Definition[¶](#id29 "Link to this heading")

This user-defined function (UDF) is used to generate a separate interval of time from the current time.

```
TO_INTERVAL_UDF(D2 TIME)
```

Copy

### Parameters[¶](#id30 "Link to this heading")

`D2` TIME

The input time to converts into a separate interval.

### Returns[¶](#id31 "Link to this heading")

Returns a string with the information of the input time separated.

### Usage example[¶](#id32 "Link to this heading")

Input:

```
SELECT TO_INTERVAL_UDF(CURRENT_TIME);
```

Copy

Output:

```
INTERVAL '4 HOURS,33 MINUTES,33 SECOND'
```

Copy

## INTERVAL\_TO\_MONTHS\_UDF (VARCHAR)[¶](#interval-to-months-udf-varchar "Link to this heading")

### Definition[¶](#id33 "Link to this heading")

This user-defined function (UDF) is used to generate an integer with the quantity of a month from an interval. This is an auxiliary function.

```
INTERVAL_TO_MONTHS_UDF
(INPUT_VALUE VARCHAR())
```

Copy

### Parameters[¶](#id34 "Link to this heading")

`INPUT_VALUE` VARCHAR

The interval value to be transformed into months.

### Returns[¶](#id35 "Link to this heading")

Returns an integer with the processed information about months.

### Usage example[¶](#id36 "Link to this heading")

Input:

```
SELECT PUBLIC.INTERVAL_TO_MONTHS_UDF('1-6');
```

Copy

Output:

```
18
```

Copy

## DATEDIFF\_UDF (STRING, TIMESTAMP)[¶](#datediff-udf-string-timestamp "Link to this heading")

### Definition[¶](#id37 "Link to this heading")

This user-defined function (UDF) is used to subtract an interval of time with a timestamp.

```
DATEADD_UDF(INTERVAL_VALUE STRING,D TIMESTAMP)
```

Copy

### Parameters[¶](#id38 "Link to this heading")

`INTERVAL_VALUE` STRING

The interval of time to be subtracted.

`D` TIMESTAMP

The timestamp to be subtracted with the interval of time.

### Returns[¶](#id39 "Link to this heading")

Returns a date with the subtraction of the interval of time and the date.

### Usage example[¶](#id40 "Link to this heading")

Input:

```
SELECT PUBLIC.DATEDIFF_UDF('INTERVAL ''1-1'' YEAR(2) TO MONTH', TO_TIMESTAMP('2024-01-31 05:09:09.799 -0800'));
```

Copy

Output:

```
2022-12-31 05:09:09.799
```

Copy

## MONTHS\_TO\_INTERVAL\_UDF (VARCHAR, NUMBER)[¶](#months-to-interval-udf-varchar-number "Link to this heading")

### Definition[¶](#id41 "Link to this heading")

This user-defined function (UDF) is used to transform month values to intervals. This is an auxiliary function.

```
MONTHS_TO_INTERVAL_UDF
(INPUT_PART VARCHAR(30), INPUT_VALUE NUMBER)
```

Copy

### Parameters[¶](#id42 "Link to this heading")

`INPUT_PART` VARCHAR

The related type of the second parameter. E.g. `YEAR TO MONTH`, `YEAR`, `MONTH`.

`INPUT_VALUE` VARCHAR

The month to be converted to intervals.

### Returns[¶](#id43 "Link to this heading")

Returns a varchar with the input value transform to an interval.

### Usage example[¶](#id44 "Link to this heading")

Input:

```
SELECT MONTHS_TO_INTERVAL_UDF('YEAR TO MONTH', 2);
```

Copy

Output:

```
2
```

Copy

## DATEDIFF\_UDF (TIMESTAMP, STRING)[¶](#datediff-udf-timestamp-string "Link to this heading")

### Definition[¶](#id45 "Link to this heading")

This user-defined function (UDF) is used to subtract a timestamp with an interval of time.

```
DATEDIFF_UDF(D TIMESTAMP, INTERVAL_VALUE STRING)
```

Copy

### Parameters[¶](#id46 "Link to this heading")

`D` TIMESTAMP

The timestamp that will be subtracted with the interval of time.

`INTERVAL_VALUE` STRING

The interval of time to be subtracted.

### Returns[¶](#id47 "Link to this heading")

Returns a date with the subtraction of the interval of time and the date.

### Usage example[¶](#id48 "Link to this heading")

Input:

```
SELECT PUBLIC.DATEDIFF_UDF(TO_TIMESTAMP('2024-01-31 05:09:09.799 -0800'), 'INTERVAL ''1-1'' YEAR(2) TO MONTH');
```

Copy

Output:

```
2022-12-31 05:09:09.799
```

Copy

## TRUNC\_UDF (NUMBER)[¶](#trunc-udf-number "Link to this heading")

### Definition[¶](#id49 "Link to this heading")

This user-defined function (UDF) reproduces the Teradata and Oracle `TRUNC(Numeric)` functionality when a scale is **not** specified.

```
TRUNC_UDF(INPUT NUMBER)
```

Copy

### Parameters[¶](#id50 "Link to this heading")

`INPUT` NUMBER

The number to truncate.

### Returns[¶](#id51 "Link to this heading")

Returns an int as the input truncated to zero decimal places.

### Usage example[¶](#id52 "Link to this heading")

Input:

```
SELECT TRUNC_UDF(25122.3368)
```

Copy

Output:

```
25122
```

Copy

## TRUNC\_UDF (NUMBER, NUMBER)[¶](#trunc-udf-number-number "Link to this heading")

### Definition[¶](#id53 "Link to this heading")

This user-defined function (UDF) reproduces the Teradata and Oracle `TRUNC(Numeric)` functionality when a scale is specified.

```
TRUNC_UDF(INPUT NUMBER, SCALE NUMBER)
```

Copy

### Parameters[¶](#id54 "Link to this heading")

`INPUT` NUMBER

The number to truncate.

`SCALE` NUMBER

The amount of places to truncate (between -38 and 38).

### Returns[¶](#id55 "Link to this heading")

Returns an int as the input truncated to scale places.

### Usage example[¶](#id56 "Link to this heading")

Input:

```
SELECT TRUNC_UDF(25122.3368, -2);
```

Copy

Output:

```
25100
```

Copy

## INTERVAL\_ADD\_UDF (VARCHAR, VARCHAR, VARCHAR, VARCHAR, CHAR, VARCHAR)[¶](#interval-add-udf-varchar-varchar-varchar-varchar-char-varchar "Link to this heading")

### Definition[¶](#id57 "Link to this heading")

This user-defined function (UDF) is used to add or subtract intervals with a specific time type.

```
INTERVAL_ADD_UDF
(INPUT_VALUE1 VARCHAR(), INPUT_PART1 VARCHAR(30), INPUT_VALUE2 VARCHAR(), INPUT_PART2 VARCHAR(30), OP CHAR, OUTPUT_PART VARCHAR())
```

Copy

### Parameters[¶](#id58 "Link to this heading")

`INPUT_VALUE1` VARCHAR

The quantity referenced to a time type.

`INPUT_PART1` VARCHAR

The time type of the *`INPUT_VALUE1`*. E.g.: `HOUR`.

`INPUT_VALUE2` VARCHAR

The second quantity referenced to a time type.

`INPUT_PART2` VARCHAR

The time type of the *`INPUT_VALUE2`*. E.g.: `HOUR`.

`OP` CHAR

The operation. I can be a ‘+’ or a ‘-‘.

`OUTPUT_PART` VARCHAR

The time type of the output operation.

### Returns[¶](#id59 "Link to this heading")

Returns a varchar with the result of the indicated operation and values.

### Usage example[¶](#id60 "Link to this heading")

Input:

```
SELECT INTERVAL_ADD_UDF('7', 'HOUR', '1', 'HOUR', '+', 'HOUR');
```

Copy

Output:

```
8
```

Copy

## DATEADD\_UDF (STRING, TIMESTAMP)[¶](#dateadd-udf-string-timestamp "Link to this heading")

### Definition[¶](#id61 "Link to this heading")

This user-defined function (UDF) is used to add a timestamp with an interval of time.

```
DATEADD_UDF(INTERVAL_VALUE STRING,D TIMESTAMP)
```

Copy

### Parameters[¶](#id62 "Link to this heading")

`INTERVAL_VALUE` STRING

The interval of time to be added.

`D` TIMESTAMP

The timestamp to be added with the interval of time.

### Returns[¶](#id63 "Link to this heading")

Returns a date with the addition of the interval of time and the date.

### Usage example[¶](#id64 "Link to this heading")

Input:

```
SELECT PUBLIC.DATEADD_UDF('INTERVAL ''1-1'' YEAR(2) TO MONTH', TO_TIMESTAMP('2024-01-31 05:09:09.799 -0800'));
```

Copy

Output:

```
2025-02-28 05:09:09.799
```

Copy

## TRUNC\_UDF (TIMESTAMP\_LTZ)[¶](#trunc-udf-timestamp-ltz "Link to this heading")

### Definition[¶](#id65 "Link to this heading")

This user-defined function (UDF) reproduces the Teradata and Oracle TRUNC(Date) functionality when the format parameter is **not** specified.

```
TRUNC_UDF(INPUT TIMESTAMP_LTZ)
```

Copy

### Parameters[¶](#id66 "Link to this heading")

`DATE_TO_TRUNC` TIMESTAMP\_LTZ

A `timestamp_ltz` value to truncate which must be a date, timestamp, or timestamp with timezone.

### Returns[¶](#id67 "Link to this heading")

Returns a date part of `DATE_TO_TRUNC`.

### Usage example[¶](#id68 "Link to this heading")

Input:

```
SELECT TRUNC_UDF(TIMESTAMP '2015-08-18 12:30:00')
```

Copy

Output:

```
2015-08-18
```

Copy

## DATEADD\_UDF (TIMESTAMP, STRING)[¶](#dateadd-udf-timestamp-string "Link to this heading")

### Definition[¶](#id69 "Link to this heading")

This user-defined function (UDF) is used to add a timestamp with an interval of time.

```
DATEADD_UDF(D TIMESTAMP, INTERVAL_VALUE STRING)
```

Copy

### Parameters[¶](#id70 "Link to this heading")

`D` TIMESTAMP

The timestamp to be added with the interval of time.

`INTERVAL_VALUE` STRING

The interval of time to be added.

### Returns[¶](#id71 "Link to this heading")

Returns a date with the addition of the interval of time and the date.

### Usage example[¶](#id72 "Link to this heading")

Input:

```
SELECT PUBLIC.DATEADD_UDF(TO_TIMESTAMP('2024-01-31 05:09:09.799 -0800'), 'INTERVAL ''1-1'' YEAR(2) TO MONTH');
```

Copy

Output:

```
2025-02-28 05:09:09.799
```

Copy

## LOG\_INFO\_UDP (VARCHAR)[¶](#log-info-udp-varchar "Link to this heading")

### Definition[¶](#id73 "Link to this heading")

This user-defined store procedure (UDP) is used to log messages using the Snowflake [SYSTEM$LOG](../../../../../../developer-guide/logging-tracing/logging-snowflake-scripting) functions.

```
DATEADD_UDF(D TIMESTAMP, INTERVAL_VALUE STRING)
```

Copy

### Parameters[¶](#id74 "Link to this heading")

`MESSAGE` VARCHAR

The message to be logged.

### Returns[¶](#id75 "Link to this heading")

A success message indicating the log operation was completed.

### Usage example[¶](#id76 "Link to this heading")

Input:

```
CALL PUBLIC.LOG_INFO_UDP('My log message');
```

Copy

Output:

| RESULT |
| --- |
| ‘Message logged successfully’ |

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

1. [INTERVAL\_MULTIPLY\_UDF (VARCHAR, VARCHAR, INTEGER)](#interval-multiply-udf-varchar-varchar-integer)
2. [TRUNC\_UDF (TIMESTAMP\_LTZ, VARCHAR)](#trunc-udf-timestamp-ltz-varchar)
3. [INTERVAL\_TO\_SECONDS\_UDF (VARCHAR, VARCHAR)](#interval-to-seconds-udf-varchar-varchar)
4. [DATEDIFF\_UDF (DATE, STRING)](#datediff-udf-date-string)
5. [SECONDS\_TO\_INTERVAL\_UDF (VARCHAR, NUMBER)](#seconds-to-interval-udf-varchar-number)
6. [DATEADD\_UDF (STRING, DATE)](#dateadd-udf-string-date)
7. [DATEDIFF\_UDF (STRING, DATE)](#datediff-udf-string-date)
8. [DATEADD\_UDF (DATE, STRING)](#dateadd-udf-date-string)
9. [TO\_INTERVAL\_UDF (TIME)](#to-interval-udf-time)
10. [INTERVAL\_TO\_MONTHS\_UDF (VARCHAR)](#interval-to-months-udf-varchar)
11. [DATEDIFF\_UDF (STRING, TIMESTAMP)](#datediff-udf-string-timestamp)
12. [MONTHS\_TO\_INTERVAL\_UDF (VARCHAR, NUMBER)](#months-to-interval-udf-varchar-number)
13. [DATEDIFF\_UDF (TIMESTAMP, STRING)](#datediff-udf-timestamp-string)
14. [TRUNC\_UDF (NUMBER)](#trunc-udf-number)
15. [TRUNC\_UDF (NUMBER, NUMBER)](#trunc-udf-number-number)
16. [INTERVAL\_ADD\_UDF (VARCHAR, VARCHAR, VARCHAR, VARCHAR, CHAR, VARCHAR)](#interval-add-udf-varchar-varchar-varchar-varchar-char-varchar)
17. [DATEADD\_UDF (STRING, TIMESTAMP)](#dateadd-udf-string-timestamp)
18. [TRUNC\_UDF (TIMESTAMP\_LTZ)](#trunc-udf-timestamp-ltz)
19. [DATEADD\_UDF (TIMESTAMP, STRING)](#dateadd-udf-timestamp-string)
20. [LOG\_INFO\_UDP (VARCHAR)](#log-info-udp-varchar)