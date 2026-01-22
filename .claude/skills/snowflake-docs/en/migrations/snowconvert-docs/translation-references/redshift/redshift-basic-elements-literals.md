---
auto_generated: true
description: A literal or constant is a fixed data value, composed of a sequence of
  characters or a numeric constant. (Redshift SQL Language reference Literals).
last_scraped: '2026-01-14T16:53:37.053951+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/redshift/redshift-basic-elements-literals
title: SnowConvert AI - Redshift - Literals | Snowflake Documentation
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

              * [Literals](redshift-basic-elements-literals.md)
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)Translation References[Redshift](README.md)[Basic Elements](redshift-basic-elements.md)Literals

# SnowConvert AI - Redshift - Literals[¶](#snowconvert-ai-redshift-literals "Link to this heading")

## Description [¶](#description "Link to this heading")

> A literal or constant is a fixed data value, composed of a sequence of characters or a numeric constant. ([Redshift SQL Language reference Literals](https://docs.aws.amazon.com/redshift/latest/dg/r_Literals.html)).

Amazon Redshift supports several types of literals, including:

* Numeric literals for integer, decimal, and floating-point numbers.
* Character literals, also referred to as strings, character strings, or character constants.
* Datetime and interval literals, used with datetime data types.

### Sample Source Patterns[¶](#sample-source-patterns "Link to this heading")

#### Input Code:[¶](#input-code "Link to this heading")

##### Redshift[¶](#redshift "Link to this heading")

```
 -- Number literals.
SELECT 42 AS integer_literal, -- Simple integer
    -123 AS negative_integer, -- Negative integer
    3.14159 AS decimal_literal, -- Decimal number
    1E0 AS simple_float; -- Floating-point representation of 1

-- Character literals.   
SELECT 'Hello, World!' AS simple_string,
    'Line1\nLine2' AS newline_character, -- Interprets \n as literal
    'Tab\tCharacter' AS tab_character, -- Interprets \t as literal
    'The value is ' || 42 AS mixed_literal;
```

Copy

##### Result[¶](#result "Link to this heading")

| integer\_literal | negative\_integer | decimal\_literal | simple\_float |
| --- | --- | --- | --- |
| 42 | -123 | 3.14159 | 1 |

| simple\_string | newline\_character | tab\_character | mixed\_literal |
| --- | --- | --- | --- |
| 42 | Line1  Line2 | Tab Character | The value is 42 |

Output Code:

##### Snowflake[¶](#snowflake "Link to this heading")

```
 -- Number literals.
SELECT 42 AS integer_literal, -- Simple integer
    -123 AS negative_integer, -- Negative integer
    3.14159 AS decimal_literal, -- Decimal number
    1E0 AS simple_float; -- Floating-point representation of 1

-- Character literals.   
SELECT 'Hello, World!' AS simple_string,
    'Line1\nLine2' AS newline_character, -- Interprets \n as literal
    'Tab\tCharacter' AS tab_character, -- Interprets \t as literal
    'The value is ' || 42 AS mixed_literal;
```

Copy

##### Result[¶](#id1 "Link to this heading")

| integer\_literal | negative\_integer | decimal\_literal | simple\_float |
| --- | --- | --- | --- |
| 42 | -123 | 3.14159 | 1 |

| simple\_string | newline\_character | tab\_character | mixed\_literal |
| --- | --- | --- | --- |
| 42 | Line1  Line2 | Tab Character | The value is 42 |

## Know Issues[¶](#know-issues "Link to this heading")

This functionality is not currently supported in Snowflake, but it will be supported through a future migration.

```
 select $MyTagForLiteral$
This is
a test
of a tag literal
$MyTagForLiteral$ as c1;
```

Copy

## Related EWIs[¶](#related-ewis "Link to this heading")

There are no known issues.

## Date, time, and timestamp literals[¶](#date-time-and-timestamp-literals "Link to this heading")

### Description [¶](#id2 "Link to this heading")

> Date, time, and timestamp literals supported by Amazon Redshift.([Redshift SQL Language reference Date, Time, Timestamp Literals](https://docs.aws.amazon.com/redshift/latest/dg/r_Date_and_time_literals.html)).

#### Sample Source Patterns[¶](#id3 "Link to this heading")

##### Input Code:[¶](#id4 "Link to this heading")

##### Redshift[¶](#id5 "Link to this heading")

```
 --invalid
SELECT
DATEADD(month, 1, 'January 8, 1999'),
DATEADD(month, 1, '2000-Jan-31'),
DATEADD(month, 1, 'Jan-31-2000'),
DATEADD(month, 1, '20000215'),
DATEADD(month, 1, '080215'),
DATEADD(month, 1, '2008.366'),
DATEADD(month, 1, 'now');

--valid
SELECT
DATEADD(month, 1, '1999-01-08'),
DATEADD(month, 1, '1/8/1999'),
DATEADD(month, 1, '01/02/00'),
DATEADD(month, 1, '31-Jan-2000');
```

Copy

Output Code:

##### Snowflake[¶](#id6 "Link to this heading")

```
 --invalid
SELECT
 DATEADD(month, 1,
                   !!!RESOLVE EWI!!! /*** SSC-EWI-RS0007 - 'January 8, 1999' DATE LITERAL IS NOT SUPPORTED IN SNOWFLAKE. ***/!!! 'January 8, 1999'),
 DATEADD(month, 1,
                   !!!RESOLVE EWI!!! /*** SSC-EWI-RS0007 - '2000-Jan-31' DATE LITERAL IS NOT SUPPORTED IN SNOWFLAKE. ***/!!! '2000-Jan-31'),
 DATEADD(month, 1,
                   !!!RESOLVE EWI!!! /*** SSC-EWI-RS0007 - 'Jan-31-2000' DATE LITERAL IS NOT SUPPORTED IN SNOWFLAKE. ***/!!! 'Jan-31-2000'),
 DATEADD(month, 1,
                   !!!RESOLVE EWI!!! /*** SSC-EWI-RS0007 - '20000215' DATE LITERAL IS NOT SUPPORTED IN SNOWFLAKE. ***/!!! '20000215'),
 DATEADD(month, 1,
                   !!!RESOLVE EWI!!! /*** SSC-EWI-RS0007 - '080215' DATE LITERAL IS NOT SUPPORTED IN SNOWFLAKE. ***/!!! '080215'),
 DATEADD(month, 1,
                   !!!RESOLVE EWI!!! /*** SSC-EWI-RS0007 - '2008.366' DATE LITERAL IS NOT SUPPORTED IN SNOWFLAKE. ***/!!! '2008.366'),
 DATEADD(month, 1,
                   !!!RESOLVE EWI!!! /*** SSC-EWI-RS0007 - 'now' DATE LITERAL IS NOT SUPPORTED IN SNOWFLAKE. ***/!!! 'now');

--valid
SELECT
 DATEADD(month, 1, '1999-01-08'),
 DATEADD(month, 1, '1/8/1999'),
 DATEADD(month, 1, '01/02/00'),
 DATEADD(month, 1, '31-Jan-2000');
```

Copy

### Know Issues[¶](#id7 "Link to this heading")

Some DATE, TIME, and TIMESTAMP formats may produce different results in Redshift compared to Snowflake.

### Related EWIs[¶](#id8 "Link to this heading")

* [SSC-EWI-RS0007](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/redshiftEWI.html#ssc-ewi-rs0008): Date literal is not supported in Snowflake.

## Interval Literals[¶](#interval-literals "Link to this heading")

### Description [¶](#id9 "Link to this heading")

> Interval literals can be used in datetime calculations, such as, adding intervals to dates and timestamps, summing intervals, and subtracting an interval from a date or timestamp. Interval literals can be used as input values to interval data type columns in a table.. ([Redshift SQL Language reference Interval Literals](https://docs.aws.amazon.com/redshift/latest/dg/r_interval_data_types.html#r_interval_data_types-syntax-literal)).

Warning

This grammar is partially supported in [Snowflake](https://docs.snowflake.com/en/sql-reference/operators-logical).

### Grammar Syntax [¶](#grammar-syntax "Link to this heading")

```
 INTERVAL quoted-string [ year_to_month_qualifier ]
INTERVAL quoted-string [ day_to_second_qualifier ] [ (fractional_precision) ]
```

Copy

[Snowflake Intervals](https://docs.snowflake.com/en/sql-reference/data-types-datetime#interval-constants) can only be used in arithmetic operations. Intervals used in any other scenario are not supported.

The following formats are the only ones recognized and fully transformed by SnowConvert AI, allowing optional fields and most of the abbreviations without interval styles:

```
 1. 1 year 1 month 1 day 2 hour 3 minutes 4 seconds 123 ms
2. hh:mm:ss.ms
3. 1 year 1 month 1 day hh:mm:ss.ms
```

Copy

Snowflake does not support literals with arithmetic signs. If the Literal contains an hour expression the expression can be partially transformed.

### Sample Source Patterns[¶](#id10 "Link to this heading")

#### Supported scenarios[¶](#supported-scenarios "Link to this heading")

##### Input Code:[¶](#id11 "Link to this heading")

##### Redshift[¶](#id12 "Link to this heading")

```
 SELECT 
'2024-01-01 00:00:00' ::TIMESTAMP + INTERVAL '1year 1month 1day 2hour 3 minute 4.1233455second' AS c1,
'2024-01-01 00:00:00' ::TIMESTAMP + INTERVAL '1year 1month 1day 2hour 3 minute 4.123second' AS c2,
'2024-01-01 00:00:00' ::TIMESTAMP +  INTERVAL '1.234567' AS c3,
'2024-01-01 00:00:00' ::TIMESTAMP + INTERVAL '13 months' AS c4,
('2024-01-01 00:00:00'::timestamp without time zone + '1 day 02:03:04.123'::interval) AS c5,
('2024-01-01 00:00:00'::timestamp without time zone + '1 year 1 mon 00:00:01'::interval) AS c6,
('2024-01-01 00:00:00'::timestamp without time zone + '1 year 1 mon'::interval) AS c7,
('2024-01-01 00:00:00'::timestamp without time zone + '00:00:01.234567'::interval) AS c8,
('2024-01-01 00:00:00'::timestamp without time zone + '1 year 1 mon 1 day 02:03:04.123'::interval) AS c9,
('2024-01-01 00:00:00'::timestamp without time zone + '00:03:04.5678'::interval) AS c10,
('2024-01-01 00:00:00'::timestamp without time zone + '1 day 02:03:00'::interval) AS c11,
('2024-01-01 00:00:00'::timestamp without time zone + '3 days 01:59:00'::interval) AS c11,
('2024-01-01 00:00:00'::timestamp without time zone + '1 year 1 mon'::interval) AS c12,
('2024-01-01 00:00:00'::timestamp without time zone + '10 years'::interval) AS c13,
('2024-01-01 00:00:00'::timestamp without time zone + '1000 years'::interval) AS c14,
('2024-01-01 00:00:00'::timestamp without time zone + '100 years'::interval) AS c15,
('2024-01-01 00:00:00'::timestamp without time zone + '1 year 1 mon'::interval) AS c16
;
```

Copy

##### Output Code:[¶](#output-code "Link to this heading")

##### Snowflake[¶](#id13 "Link to this heading")

```
 SELECT
'2024-01-01 00:00:00' ::TIMESTAMP + INTERVAL '1year, 1month, 1day, 2hour, 3 minute, 4 seconds, 123 ms' AS c1,
'2024-01-01 00:00:00' ::TIMESTAMP + INTERVAL '1year, 1month, 1day, 2hour, 3 minute, 4 seconds, 123 ms' AS c2,
'2024-01-01 00:00:00' ::TIMESTAMP + INTERVAL '1 seconds, 234 ms' AS c3,
'2024-01-01 00:00:00' ::TIMESTAMP + INTERVAL '13 months' AS c4,
('2024-01-01 00:00:00':: TIMESTAMP_NTZ + INTERVAL '1 day, 02 hour, 03 minutes, 04 seconds, 123 ms') AS c5,
('2024-01-01 00:00:00':: TIMESTAMP_NTZ + INTERVAL '1 year, 1 mon, 00 hour, 00 minutes, 01 seconds') AS c6,
('2024-01-01 00:00:00':: TIMESTAMP_NTZ + INTERVAL '1 year, 1 mon') AS c7,
('2024-01-01 00:00:00':: TIMESTAMP_NTZ + INTERVAL '00 hour, 00 minutes, 01 seconds, 234 ms') AS c8,
('2024-01-01 00:00:00':: TIMESTAMP_NTZ + INTERVAL '1 year, 1 mon, 1 day, 02 hour, 03 minutes, 04 seconds, 123 ms') AS c9,
('2024-01-01 00:00:00':: TIMESTAMP_NTZ + INTERVAL '00 hour, 03 minutes, 04 seconds, 567 ms') AS c10,
('2024-01-01 00:00:00':: TIMESTAMP_NTZ + INTERVAL '1 day, 02 hour, 03 minutes, 00 seconds') AS c11,
('2024-01-01 00:00:00':: TIMESTAMP_NTZ + INTERVAL '3 days , 01 hour, 59 minutes, 00 seconds') AS c11,
('2024-01-01 00:00:00':: TIMESTAMP_NTZ + INTERVAL '1 year, 1 mon') AS c12,
('2024-01-01 00:00:00':: TIMESTAMP_NTZ + INTERVAL '10 years') AS c13,
('2024-01-01 00:00:00':: TIMESTAMP_NTZ + INTERVAL '1000 years') AS c14,
('2024-01-01 00:00:00':: TIMESTAMP_NTZ + INTERVAL '100 years') AS c15,
('2024-01-01 00:00:00':: TIMESTAMP_NTZ + INTERVAL '1 year, 1 mon') AS c16
;
```

Copy

#### Pending translation scenarios[¶](#pending-translation-scenarios "Link to this heading")

##### Input Code:[¶](#id14 "Link to this heading")

##### Redshift[¶](#id15 "Link to this heading")

```
 SELECT
INTERVAL '1year 1month 1day 2hour 3 minute 4.1233455second',
'2024-01-01 00:00:00' ::TIMESTAMP +  INTERVAL '1.234567' SECOND AS c2,
'2024-01-01 00:00:00' ::TIMESTAMP +  INTERVAL '1.234567' SECOND (3) AS c3,
'2024-01-01 00:00:00' ::TIMESTAMP + INTERVAL '13 months' YEAR AS c4,
'2024-01-01 00:00:00' ::TIMESTAMP + INTERVAL '13 months' MONTH AS c5,
'2024-01-01 00:00:00' ::TIMESTAMP + INTERVAL '1 2:3:4.5678' DAY TO MINUTE AS c6,
'2024-01-01 00:00:00' ::TIMESTAMP + INTERVAL '1 2:3:4.5678' DAY TO SECOND AS c7,
'2024-01-01 00:00:00' ::TIMESTAMP + INTERVAL '1 2:3' AS c8,
'2024-01-01 00:00:00' ::TIMESTAMP + INTERVAL '1 49:59:0' AS c9,
'2024-01-01 00:00:00' ::TIMESTAMP + INTERVAL '1 49:59:0' DAY AS c10,
'2024-01-01 00:00:00' ::TIMESTAMP + INTERVAL '1 - 1 1'  AS c11,
'2024-01-01 00:00:00' ::TIMESTAMP + INTERVAL '1-1' AS c12,
'2024-01-01 00:00:00' ::TIMESTAMP + INTERVAL '1 year -1 day' AS c13,
'2024-01-01 00:00:00' ::TIMESTAMP + INTERVAL '3:4.5678' AS c14,
'2024-01-01 00:00:00' ::TIMESTAMP + INTERVAL '1-1 0 second 0 millisecond' AS c15,
'2024-01-01 00:00:00' ::TIMESTAMP + INTERVAL '1 decade' AS c16,
'2024-01-01 00:00:00' ::TIMESTAMP + INTERVAL '1 millenium' AS c17,
'2024-01-01 00:00:00' ::TIMESTAMP + INTERVAL '1 century' AS c18,
('2024-01-01 00:00:00'::timestamp without time zone + ('00:00:01.234567')::interval second) AS c19,
('2024-01-01 00:00:00'::timestamp without time zone + ('00:00:01.235')::interval second (3)) AS c20,
('2024-01-01 00:00:00'::timestamp without time zone + ('1 year')::interval year) AS c21,
('2024-01-01 00:00:00'::timestamp without time zone + ('1 year 1 mon')::interval month) AS c22,
('2024-01-01 00:00:00'::timestamp without time zone + ('1 day 02:03:00')::interval day to minute) AS c23,
('2024-01-01 00:00:00'::timestamp without time zone + ('1 day 02:03:04.5678')::interval day to second) AS c24,
('2024-01-01 00:00:00'::timestamp without time zone + '-01:56:55.877'::interval) AS c25,
('2024-01-01 00:00:00'::timestamp without time zone + ('3 days')::interval day) AS c26;
```

Copy

##### Output Code:[¶](#id16 "Link to this heading")

##### Snowflake[¶](#id17 "Link to this heading")

```
 SELECT
INTERVAL '1year 1month 1day 2hour 3 minute 4.1233455second' !!!RESOLVE EWI!!! /*** SSC-EWI-0107 - INTERVAL LITERAL IS NOT SUPPORTED BY SNOWFLAKE IN THIS SCENARIO  ***/!!!,
'2024-01-01 00:00:00' ::TIMESTAMP + INTERVAL '1 seconds, 234 ms' SECOND !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'INTERVAL FORMAT' NODE ***/!!! AS c2,
'2024-01-01 00:00:00' ::TIMESTAMP + INTERVAL '1 seconds, 234 ms' SECOND (3) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'INTERVAL FORMAT' NODE ***/!!! AS c3,
'2024-01-01 00:00:00' ::TIMESTAMP + INTERVAL '13 months' YEAR !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'INTERVAL FORMAT' NODE ***/!!! AS c4,
'2024-01-01 00:00:00' ::TIMESTAMP + INTERVAL '13 months' MONTH !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'INTERVAL FORMAT' NODE ***/!!! AS c5,
'2024-01-01 00:00:00' ::TIMESTAMP + INTERVAL '1 , 2 hour, 3 minutes, 4 seconds, 567 ms' DAY TO MINUTE !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'INTERVAL FORMAT' NODE ***/!!!!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'INTERVAL FORMAT' NODE ***/!!! AS c6,
'2024-01-01 00:00:00' ::TIMESTAMP + INTERVAL '1 , 2 hour, 3 minutes, 4 seconds, 567 ms' DAY TO SECOND !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'INTERVAL FORMAT' NODE ***/!!!!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'INTERVAL FORMAT' NODE ***/!!! AS c7,
'2024-01-01 00:00:00' ::TIMESTAMP + INTERVAL '1 2:3' !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'INTERVAL FORMAT' NODE ***/!!! AS c8,
'2024-01-01 00:00:00' ::TIMESTAMP + INTERVAL '1 , 49 hour, 59 minutes, 0 seconds' !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'INTERVAL FORMAT' NODE ***/!!! AS c9,
'2024-01-01 00:00:00' ::TIMESTAMP + INTERVAL '1 , 49 hour, 59 minutes, 0 seconds' DAY !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'INTERVAL FORMAT' NODE ***/!!!!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'INTERVAL FORMAT' NODE ***/!!! AS c10,
'2024-01-01 00:00:00' ::TIMESTAMP + INTERVAL '1 - 1 1' !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'INTERVAL FORMAT' NODE ***/!!!  AS c11,
'2024-01-01 00:00:00' ::TIMESTAMP + INTERVAL '1-1' !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'INTERVAL FORMAT' NODE ***/!!! AS c12,
'2024-01-01 00:00:00' ::TIMESTAMP + INTERVAL '1 year -1 day' !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'INTERVAL FORMAT' NODE ***/!!! AS c13,
'2024-01-01 00:00:00' ::TIMESTAMP + INTERVAL '3:4.5678' !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'INTERVAL FORMAT' NODE ***/!!! AS c14,
'2024-01-01 00:00:00' ::TIMESTAMP + INTERVAL '1-1 0 second 0 millisecond' !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'INTERVAL FORMAT' NODE ***/!!! AS c15,
'2024-01-01 00:00:00' ::TIMESTAMP + INTERVAL '1 decade' !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'INTERVAL FORMAT' NODE ***/!!! AS c16,
'2024-01-01 00:00:00' ::TIMESTAMP + INTERVAL '1 millenium' !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'INTERVAL FORMAT' NODE ***/!!! AS c17,
'2024-01-01 00:00:00' ::TIMESTAMP + INTERVAL '1 century' !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'INTERVAL FORMAT' NODE ***/!!! AS c18,
('2024-01-01 00:00:00':: TIMESTAMP_NTZ + INTERVAL '00 hour, 00 minutes, 01 seconds, 234 ms' second !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'INTERVAL FORMAT' NODE ***/!!!) AS c19,
('2024-01-01 00:00:00':: TIMESTAMP_NTZ + INTERVAL '00 hour, 00 minutes, 01 seconds, 235 ms' second (3) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'INTERVAL FORMAT' NODE ***/!!!) AS c20,
('2024-01-01 00:00:00':: TIMESTAMP_NTZ + INTERVAL '1 year' year !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'INTERVAL FORMAT' NODE ***/!!!) AS c21,
('2024-01-01 00:00:00':: TIMESTAMP_NTZ + INTERVAL '1 year, 1 mon' month !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'INTERVAL FORMAT' NODE ***/!!!) AS c22,
('2024-01-01 00:00:00':: TIMESTAMP_NTZ + INTERVAL '1 day, 02 hour, 03 minutes, 00 seconds' day to minute !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'INTERVAL FORMAT' NODE ***/!!!) AS c23,
('2024-01-01 00:00:00':: TIMESTAMP_NTZ + INTERVAL '1 day, 02 hour, 03 minutes, 04 seconds, 567 ms' day to second !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'INTERVAL FORMAT' NODE ***/!!!) AS c24,
('2024-01-01 00:00:00':: TIMESTAMP_NTZ + '-01:56:55.877':: VARCHAR !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - INTERVAL DATA TYPE CONVERTED TO VARCHAR ***/!!!!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'INTERVAL FORMAT' NODE ***/!!!) AS c25,
('2024-01-01 00:00:00':: TIMESTAMP_NTZ + ('3 days'):: VARCHAR !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - INTERVAL DATA TYPE CONVERTED TO VARCHAR ***/!!!!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'INTERVAL FORMAT' NODE ***/!!!) AS c26;
```

Copy

### Know Issues[¶](#id18 "Link to this heading")

No issues were found.

### Related EWIs[¶](#id19 "Link to this heading")

1. [SSC-EWI-0107](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0107): Interval Literal Not Supported In Current Scenario.
2. [SSC-EWI-0073](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0073): Pending Functional Equivalence Review.

## NULLS[¶](#nulls "Link to this heading")

### Description [¶](#id20 "Link to this heading")

> If a column in a row is missing, unknown, or not applicable, it is a null value or is said to contain null. ([Redshift SQL Language reference Nulls Literals](https://docs.aws.amazon.com/redshift/latest/dg/r_Nulls.html)).

Nulls can appear in fields of any data type that are not restricted by primary key or NOT NULL constraints. A null is not equivalent to the value zero or to an empty string.

#### Sample Source Patterns[¶](#id21 "Link to this heading")

##### Input Code:[¶](#id22 "Link to this heading")

##### Redshift[¶](#id23 "Link to this heading")

```
 SELECT NULL IN (NULL, 0, 1, 2 ,3, 4);
SELECT 1 + NULL, 1 - NULL, 1 * NULL, 1 / NULL, 1 % NULL;
```

Copy

##### Result[¶](#id24 "Link to this heading")

| Select1 |
| --- |
| NULL |

| 1+NULL | 1\*NULL |
| --- | --- |
| NULL | NULL |

Output Code:

##### Snowflake[¶](#id25 "Link to this heading")

```
 SELECT NULL IN (NULL, 0, 1, 2 ,3, 4);
SELECT 1 + NULL, 1 - NULL, 1 * NULL, 1 / NULL, 1 % NULL;
```

Copy

##### Result[¶](#id26 "Link to this heading")

| Select1 |
| --- |
| NULL |

| 1+NULL | 1\*NULL |
| --- | --- |
| NULL | NULL |

### Know Issues[¶](#id27 "Link to this heading")

No issues were found.

### Related EWIs[¶](#id28 "Link to this heading")

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

1. [Description](#description)
2. [Know Issues](#know-issues)
3. [Related EWIs](#related-ewis)
4. [Date, time, and timestamp literals](#date-time-and-timestamp-literals)
5. [Interval Literals](#interval-literals)
6. [NULLS](#nulls)