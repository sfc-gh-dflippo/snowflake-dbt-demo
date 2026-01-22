---
auto_generated: true
description: UDF (User-Defined Function) that calculates the quarter number of a given
  date according to the ISO calendar year, similar to Teradata’s QUARTERNUMBER_OF_YEAR_UDF(date,
  ‘ISO’) function.
last_scraped: '2026-01-14T16:52:37.655375+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/function-references/teradata/README
title: SnowConvert AI - Function References for Teradata | Snowflake Documentation
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
              - [Teradata](README.md)
              - [Oracle](../oracle/README.md)
              - [Shared](../shared/README.md)
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

[Guides](../../../../../../guides/README.md)[Migrations](../../../../../README.md)Tools[SnowConvert AI](../../../../overview.md)General[Technical Documentation](../../README.md)Function ReferencesTeradata

# SnowConvert AI - Function References for Teradata[¶](#snowconvert-ai-function-references-for-teradata "Link to this heading")

## QUARTERNUMBER\_OF\_YEAR\_UDF[¶](#quarternumber-of-year-udf "Link to this heading")

### Definition[¶](#definition "Link to this heading")

UDF (User-Defined Function) that calculates the quarter number of a given date according to the ISO calendar year, similar to Teradata’s QUARTERNUMBER\_OF\_YEAR\_UDF(date, ‘ISO’) function.

```
PUBLIC.QUARTERNUMBER_OF_YEAR_UDF(INPUT TIMESTAMP_TZ)
```

Copy

### Parameters[¶](#parameters "Link to this heading")

`INPUT` TimeSTAMP\_TZ

The method to extract the quarter number.

### Returns[¶](#returns "Link to this heading")

An integer (1-4) indicating which quarter of the year the date falls into.

### Usage example[¶](#usage-example "Link to this heading")

Input:

```
SELECT PUBLIC.QUARTERNUMBER_OF_YEAR_UDF(DATE '2022-01-01'),
PUBLIC.QUARTERNUMBER_OF_YEAR_UDF(DATE '2025-12-31');
```

Copy

Output:

```
4, 1
```

Copy

## DAYNUMBER\_OF\_YEAR\_UDF[¶](#daynumber-of-year-udf "Link to this heading")

### Definition[¶](#id1 "Link to this heading")

Returns the day number within the year for a given timestamp. The day number ranges from 1 to 365 (or 366 in leap years). This function behaves the same way as DAYNUMBER\_OF\_YEAR(DATE, ‘ISO’).

```
PUBLIC.DAYNUMBER_OF_YEAR_UDF(INPUT TIMESTAMP_TZ)
```

Copy

### Parameters[¶](#id2 "Link to this heading")

`INPUT` TIMESTAMP\_TZ

To get the day number of the year from a date.

### Returns[¶](#id3 "Link to this heading")

A whole number from 1 to 371.

### Example[¶](#example "Link to this heading")

Input:

```
SELECT DAYNUMBER_OF_YEAR(CURRENT_DATE,'ISO');
```

Copy

Output:

```
SELECT
PUBLIC.DAYNUMBER_OF_YEAR_UDF(CURRENT_DATE());
```

Copy

## SUBSTR\_UDF (STRING, FLOAT)[¶](#substr-udf-string-float "Link to this heading")

Warning

This user-defined function (UDF) accepts two parameters (overloaded function).

### Definition[¶](#id4 "Link to this heading")

Retrieves a portion of text from a specified string by using a starting position and length.

```
PUBLIC.SUBSTR_UDF(BASE_EXPRESSION STRING, START_POSITION FLOAT)
```

Copy

### Parameters[¶](#id5 "Link to this heading")

`BASE_EXPRESSION` is a string parameter that defines the base expression for the operation.

The source text from which you want to extract a portion.

`START_POSITION` - A floating-point number that specifies the starting position in the input string.

The position where you want to begin extracting characters from the string.

### Returns[¶](#id6 "Link to this heading")

The substring that must be included.

### Migration example[¶](#migration-example "Link to this heading")

Input:

```
SELECT SUBSTRING('Hello World!' FROM -2);
```

Copy

Output:

```
SELECT
PUBLIC.SUBSTR_UDF('Hello World!', -2);
```

Copy

## CHKNUM\_UDF[¶](#chknum-udf "Link to this heading")

### Definition[¶](#id7 "Link to this heading")

Verify whether a string contains a valid numeric value.

```
PUBLIC.CHKNUM_UDF(NUM STRING);
```

Copy

### Parameters[¶](#id8 "Link to this heading")

`NUM` A string representing a number

The text string that needs to be validated.

### Returns[¶](#id9 "Link to this heading")

Returns 1 if the input parameter is a valid numeric value. If the input is not a valid number (for example, text or special characters), returns 0.

### Example[¶](#id10 "Link to this heading")

```
SELECT CHKNUM('1032');
```

Copy

Output:

```
SELECT
PUBLIC.CHKNUM_UDF('1032');
```

Copy

## TD\_YEAR\_END\_UDF[¶](#td-year-end-udf "Link to this heading")

### Definition[¶](#id11 "Link to this heading")

UDF (User-Defined Function) that replicates Teradata’s TD\_YEAR\_END(DATE) or TD\_YEAR\_END(DATE, ‘COMPATIBLE’) function, which returns the last day of the year for a given date.

```
PUBLIC.TD_YEAR_END_UDF(INPUT date)
```

Copy

### Parameters[¶](#id12 "Link to this heading")

`INPUT` DATE

Get the last day of the current year.

### Returns[¶](#id13 "Link to this heading")

The final day of December (December 31st).

### Usage example[¶](#id14 "Link to this heading")

Input:

```
SELECT  PUBLIC.TD_YEAR_END_UDF(DATE '2022-01-01'),
PUBLIC.TD_YEAR_END_UDF(DATE '2022-04-12');
```

Copy

Output:

```
2022-12-31, 2022-12-31
```

Copy

## PERIOD\_OVERLAPS\_UDF[¶](#period-overlaps-udf "Link to this heading")

### Definition[¶](#id15 "Link to this heading")

A user-defined function (UDF) that implements the OVERLAPS OPERATOR functionality. This function compares two or more time periods and determines whether they have any overlapping time ranges.

```
PERIOD_OVERLAPS_UDF(PERIODS ARRAY)
```

Copy

### Parameters[¶](#id16 "Link to this heading")

`PERIODS` is an array that contains time periods

All period expressions that will be compared.

### Returns[¶](#id17 "Link to this heading")

TRUE if all time periods in the set have at least one point in common (overlap), FALSE otherwise.

### Migration example[¶](#id18 "Link to this heading")

```
SELECT
	PERIOD(DATE '2009-01-01', DATE '2010-09-24')
	OVERLAPS
	PERIOD(DATE '2009-02-01', DATE '2009-06-24');
```

Copy

Output:

```
SELECT
	PUBLIC.PERIOD_OVERLAPS_UDF(ARRAY_CONSTRUCT(PUBLIC.PERIOD_UDF(DATE '2009-01-01', DATE '2010-09-24') !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!, PUBLIC.PERIOD_UDF(DATE '2009-02-01', DATE '2009-06-24') !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!)) !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!;
```

Copy

## WEEK\_NUMBER\_OF\_QUARTER\_COMPATIBLE\_UDF[¶](#week-number-of-quarter-compatible-udf "Link to this heading")

### Definition[¶](#id19 "Link to this heading")

Calculates which week number within the current quarter a specified date falls into.

```
PUBLIC.WEEK_NUMBER_OF_QUARTER_COMPATIBLE_UDF(INPUT TIMESTAMP_TZ)
```

Copy

### Parameters[¶](#id20 "Link to this heading")

`INPUT` TIMESTAMP\_TZ

The date used to calculate which week of the quarter it falls into.

### Returns[¶](#id21 "Link to this heading")

An integer indicating which week of the quarter the date falls in (1-13).

### Usage example[¶](#id22 "Link to this heading")

Input:

```
SELECT WEEK_NUMBER_OF_QUARTER_COMPATIBLE_UDF(DATE '2022-05-01', 'COMPATIBLE'),
WEEK_NUMBER_OF_QUARTER_COMPATIBLE_UDF(DATE '2022-07-06', 'COMPATIBLE')
```

Copy

Output:

```
5, 1
```

Copy

## ROMAN\_NUMERALS\_MONTH\_UDF[¶](#roman-numerals-month-udf "Link to this heading")

### Definition[¶](#id23 "Link to this heading")

Converts a date into its corresponding month in Roman numerals.

```
PUBLIC.ROMAN_NUMERALS_MONTH_UDF(INPUT TIMESTAMP_TZ)
```

Copy

### Parameters[¶](#id24 "Link to this heading")

`INPUT` TIMESTAMP\_TZ

The input date from which to extract the month.

### Returns[¶](#id25 "Link to this heading")

A `varchar` representing the month extracted from a given date.

### Usage example[¶](#id26 "Link to this heading")

Input:

```
SELECT PUBLIC.ROMAN_NUMERALS_MONTH_UDF(DATE '2021-10-26');
```

Copy

Output:

```
'X'
```

Copy

## TD\_YEAR\_BEGIN\_UDF[¶](#td-year-begin-udf "Link to this heading")

### Definition[¶](#id27 "Link to this heading")

A user-defined function (UDF) that mimics the behavior of TD\_YEAR\_BEGIN or TD\_YEAR\_BEGIN(DATE, ‘COMPATIBLE’) by returning the first day of the year for a given date.

```
PUBLIC.TD_YEAR_BEGIN_UDF(INPUT DATE)
```

Copy

### Parameters[¶](#id28 "Link to this heading")

`INPUT` DATE

Get the first day of the current year.

### Returns[¶](#id29 "Link to this heading")

The first day of January.

### Usage example[¶](#id30 "Link to this heading")

Input:

```
SELECT TD_YEAR_BEGIN(DATE '2022-01-01', 'COMPATIBLE'),
TD_YEAR_BEGIN(DATE '2022-04-12');
```

Copy

Output:

```
2022-01-01, 2022-01-01
```

Copy

## FULL\_MONTH\_NAME\_UDF[¶](#full-month-name-udf "Link to this heading")

### Definition[¶](#id31 "Link to this heading")

Returns the full name of a month in your choice of formatting: all uppercase letters, all lowercase letters, or with only the first letter capitalized.

```
PUBLIC.FULL_MONTH_NAME_UDF(INPUT TIMESTAMP_TZ, RESULTCASE VARCHAR)
```

Copy

### Parameters[¶](#id32 "Link to this heading")

`INPUT` TIMESTAMP\_TZ

The date format should display the month name.

`RESULTCASE` VARCHAR

The format in which the result should be displayed. Valid options are ‘uppercase’, ‘lowercase’, or ‘capitalized’.

### Returns[¶](#id33 "Link to this heading")

Returns a `varchar` containing the full name of a month

### Usage example[¶](#id34 "Link to this heading")

Input:

```
SELECT PUBLIC.FULL_MONTH_NAME_UDF(DATE '2021-10-26', 'uppercase');
SELECT PUBLIC.FULL_MONTH_NAME_UDF(DATE '2021-10-26', 'lowercase');
SELECT PUBLIC.FULL_MONTH_NAME_UDF(DATE '2021-10-26', 'firstOnly');
```

Copy

Output:

```
OCTOBER
october
October
```

Copy

## TO\_BYTES\_HEX\_UDF[¶](#to-bytes-hex-udf "Link to this heading")

### Definition[¶](#id35 "Link to this heading")

Converts a decimal (base 10) number into its hexadecimal (base 16) representation.

```
TO_BYTES_HEX_UDF(INPUT FLOAT)
```

Copy

### Parameters[¶](#id36 "Link to this heading")

`INPUT` is a floating-point number parameter.

The number that will be converted into hexadecimal format.

### Returns[¶](#id37 "Link to this heading")

A string representing the hexadecimal value.

### Usage example[¶](#id38 "Link to this heading")

Input:

```
SELECT TO_BYTES_HEX_UDF('448');
```

Copy

Output:

```
01c0
```

Copy

## PERIOD\_INTERSECT\_UDF[¶](#period-intersect-udf "Link to this heading")

### Definition[¶](#id39 "Link to this heading")

A user-defined function (UDF) that replicates the P\_INTERSECT operator. This function compares two or more time periods and identifies where they overlap, returning the common time interval between them.

For more details about the source function, please refer to the [documentation](https://docs.teradata.com/r/SQL-Date-and-Time-Functions-and-Expressions/July-2021/Period-Functions-and-Operators/P_INTERSECT/P_INTERSECT-Syntax).

```
PERIOD_INTERSECT_UDF(PERIODS ARRAY)
```

Copy

### Parameters[¶](#id40 "Link to this heading")

`PERIODS` is an array that contains time periods.

All period expressions that need to be compared.

### Returns[¶](#id41 "Link to this heading")

The section where two time periods intersect or share common dates.

### Migration example[¶](#id42 "Link to this heading")

Input:

```
SELECT
	PERIOD(DATE '2009-01-01', DATE '2010-09-24')
	P_INTERSECT
	PERIOD(DATE '2009-02-01', DATE '2009-06-24');
```

Copy

Output:

```
SELECT
	PUBLIC.PERIOD_INTERSECT_UDF(ARRAY_CONSTRUCT(PUBLIC.PERIOD_UDF(DATE '2009-01-01', DATE '2010-09-24') !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!, PUBLIC.PERIOD_UDF(DATE '2009-02-01', DATE '2009-06-24') !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!)) !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!;
```

Copy

## INTERVAL\_TO\_SECONDS\_UDF[¶](#interval-to-seconds-udf "Link to this heading")

### Definition[¶](#id43 "Link to this heading")

Converts a time interval into seconds.

```
PUBLIC.INTERVAL_TO_SECONDS_UDF
(INPUT_PART VARCHAR(30), INPUT_VALUE VARCHAR())
```

Copy

### Parameters[¶](#id44 "Link to this heading")

`INPUT_PART` is a variable of type VARCHAR that stores input data.

The time duration that will be converted into seconds.

`INPUT_VALUE` VARCHAR - The input parameter that accepts text data. - The input parameter that accepts text data.

The time interval type for conversion. Examples include ‘DAY’, ‘DAY TO HOUR’, and other valid interval types.

### Returns[¶](#id45 "Link to this heading")

A decimal number representing the time interval in seconds.

## TIMESTAMP\_ADD\_UDF[¶](#timestamp-add-udf "Link to this heading")

### Definition[¶](#id46 "Link to this heading")

Combines two timestamps into a single value.

```
PUBLIC.TIMESTAMP_ADD_UDF(FIRST_DATE TIMESTAMP_LTZ, SECOND_DATE TIMESTAMP_LTZ)
```

Copy

### Parameters[¶](#id47 "Link to this heading")

`FIRST_DATE` is a timestamp field that includes both date and time information, with timezone support (TIMESTAMP\_LTZ)

The initial date when this was added.

`SECOND_DATE` is a timestamp column that includes timezone information (TIMESTAMP\_LTZ) (Timestamp with local time zone)

The date when the item was added for the second time.

### Returns[¶](#id48 "Link to this heading")

A timestamp generated by combining the input date parameters.

## INTERVAL\_MULTIPLY\_UDF[¶](#interval-multiply-udf "Link to this heading")

### Definition[¶](#id49 "Link to this heading")

A user-defined function (UDF) that performs multiplication operations on time intervals.

```
PUBLIC.INTERVAL_MULTIPLY_UDF
(INPUT_PART VARCHAR(30), INPUT_VALUE VARCHAR(), INPUT_MULT INTEGER)
```

Copy

### Parameters[¶](#id50 "Link to this heading")

`INPUT_PART` is a variable of type VARCHAR that stores input data.

The value used for multiplication, specified as ‘YEAR TO MONTH’.

`INPUT_VALUE` VARCHAR

The interval to multiply by.

`INPUT_MULT` is an integer parameter that serves as a multiplier for input values.

The number that will be used in the multiplication operation.

### Returns[¶](#id51 "Link to this heading")

The output is calculated by multiplying a time interval by a numeric value.

### Migration example[¶](#id52 "Link to this heading")

Input:

```
SELECT INTERVAL '6-10' YEAR TO MONTH * 8;
```

Copy

Output:

```
SELECT
PUBLIC.INTERVAL_MULTIPLY_UDF('YEAR TO MONTH', '6-10', 8);
```

Copy

## TD\_DAY\_OF\_WEEK\_UDF[¶](#td-day-of-week-udf "Link to this heading")

### Definition[¶](#id53 "Link to this heading")

User-defined function (UDF) that replicates Teradata’s `TD_DAY_OF_WEEK` functionality. For details about the original Teradata function, see [here](https://docs.teradata.com/r/SQL-Date-and-Time-Functions-and-Expressions/July-2021/Calendar-Functions/td_day_of_week/DayOfWeek).

```
PUBLIC.TD_DAY_OF_WEEK_UDF(INPUT TIMESTAMP_TZ)
```

Copy

### Parameters[¶](#id54 "Link to this heading")

`INPUT` TIMESTAMP\_TZ

Date from which to get the day of the week.

### Returns[¶](#id55 "Link to this heading")

An integer from 1 to 7 representing the day of the week, where:

* 1 = Sunday
* 2 = Monday
* 3 = Tuesday
* 4 = Wednesday
* 5 = Thursday
* 6 = Friday
* 7 = Saturday

### Migration example[¶](#id56 "Link to this heading")

Input:

```
SELECT td_day_of_week(DATE '2022-03-02');
```

Copy

Output:

```
SELECT
PUBLIC.TD_DAY_OF_WEEK_UDF(DATE '2022-03-02');
```

Copy

## ISO\_YEAR\_PART\_UDF[¶](#iso-year-part-udf "Link to this heading")

### Definition[¶](#id57 "Link to this heading")

Calculates the ISO calendar year from a given date. The result can be shortened by specifying the number of digits to keep.

```
PUBLIC.ISO_YEAR_PART_UDF(INPUT TIMESTAMP_TZ, DIGITS INTEGER)
```

Copy

### Parameters[¶](#id58 "Link to this heading")

`INPUT` TIMESTAMP\_TZ

The date from which to extract the ISO year.

`DIGITS` A whole number that represents the maximum number of digits to display

The number of decimal places desired in the output.

### Returns[¶](#id59 "Link to this heading")

Returns a string (varchar) representing the ISO year of a given date.

### Usage example[¶](#id60 "Link to this heading")

Input:

```
SELECT PUBLIC.ISO_YEAR_PART_UDF(DATE '2021-10-26', 3);
SELECT PUBLIC.ISO_YEAR_PART_UDF(DATE '2021-10-26', 2);
SELECT PUBLIC.ISO_YEAR_PART_UDF(DATE '2021-10-26', 1);
```

Copy

Output:

```
'021'
'21'
'1'
```

Copy

## DIFF\_TIME\_PERIOD\_UDF[¶](#diff-time-period-udf "Link to this heading")

### Definition[¶](#id61 "Link to this heading")

Computes the time interval between two dates based on the specified time unit parameter.

```
PUBLIC.DIFF_TIME_PERIOD_UDF(TIME STRING, PERIOD VARCHAR(50))
```

Copy

### Parameters[¶](#id62 "Link to this heading")

`TIME` is a data type used to store time values in hours, minutes, seconds, and fractions of seconds. is a data type that represents a time value stored as a text string.

The timestamp that will be used as an anchor point.

`PERIOD` A text field (VARCHAR) that represents a time period

The period column used for expansion.

### Returns[¶](#id63 "Link to this heading")

A numerical value indicating the time interval between two dates.

### Usage example[¶](#id64 "Link to this heading")

Input:

```
SELECT DIFF_TIME_PERIOD_UDF('SECONDS','2022-11-26 10:15:20.000*2022-11-26 10:15:25.000');
```

Copy

Output:

```
5
```

Copy

## WEEK\_NUMBER\_OF\_QUARTER\_ISO\_UDF[¶](#week-number-of-quarter-iso-udf "Link to this heading")

### Definition[¶](#id65 "Link to this heading")

Calculates which week number a date falls into within its quarter, using ISO calendar standards. This function behaves identically to Teradata’s `WEEKNUMBER_OF_QUARTER(DATE, 'ISO')` function.

```
PUBLIC.WEEK_NUMBER_OF_QUARTER_ISO_UDF(INPUT TIMESTAMP_TZ)
```

Copy

### Parameters[¶](#id66 "Link to this heading")

`INPUT` TIMESTAMP\_TZ

The date used to calculate which week of the quarter it falls into.

### Returns[¶](#id67 "Link to this heading")

An integer indicating which week of the quarter (1-13) this represents.

### Usage example[¶](#id68 "Link to this heading")

Input:

```
SELECT WEEKNUMBER_OF_QUARTER(DATE '2022-05-01', 'ISO'),
WEEKNUMBER_OF_QUARTER(DATE '2022-07-06', 'ISO')
```

Copy

Output:

```
SELECT
PUBLIC.SUBSTR_UDF('Hello World!', -2);
```

Copy

## NVP\_UDF[¶](#nvp-udf "Link to this heading")

### Definition[¶](#id69 "Link to this heading")

Performs the same function as Teradata’s [NVP function](https://docs.teradata.com/r/SQL-Functions-Expressions-and-Predicates/June-2020/String-Operators-and-Functions/NVP/NVP-Function-Syntax).

```
NVP_UDF(INSTRING VARCHAR, NAME_TO_SEARCH VARCHAR, NAME_DELIMITERS VARCHAR, VALUE_DELIMITERS VARCHAR, OCCURRENCE FLOAT)
```

Copy

### Parameters[¶](#id70 "Link to this heading")

`INSTRING` VARCHAR

Name-value pairs are data elements that consist of a name and its corresponding value.

`NAME_TO_SEARCH` of type VARCHAR

The name parameter used to search within the Name-Value Pair (NVP) function.

`NAME_DELIMITERS` VARCHAR

The character used to separate names from their corresponding values.

`VALUE_DELIMITERS` VARCHAR

The character used to connect a name with its corresponding value.

`OCCURRENCE` represents a floating-point number that indicates how many times something occurs

The number of matching patterns to search for.

### Returns[¶](#id71 "Link to this heading")

A text string (VARCHAR) containing identical data as the input string.

### Usage example[¶](#id72 "Link to this heading")

Input:

```
SELECT PUBLIC.NVP_UDF('entree=-orange chicken&entree+.honey salmon', 'entree', '&', '=- +.', 1);
```

Copy

Output:

```
orange chicken
```

Copy

## MONTH\_SHORT\_UDF[¶](#month-short-udf "Link to this heading")

### Definition[¶](#id73 "Link to this heading")

Returns the abbreviated name of a month (three letters) in your choice of uppercase, lowercase, or capitalized format. For example: “Jan”, “jan”, or “JAN”.

```
PUBLIC.MONTH_SHORT_UDF(INPUT TIMESTAMP_TZ, RESULTCASE VARCHAR)
```

Copy

### Parameters[¶](#id74 "Link to this heading")

`INPUT` TIMESTAMP\_TZ

The date formatted to display the abbreviated month name.

`RESULTCASE` VARCHAR

The letter case format to be used. Valid options are:

* ‘uppercase’: converts text to all capital letters
* ‘lowercase’: converts text to all small letters
* ‘firstOnly’: capitalizes only the first letter

### Returns[¶](#id75 "Link to this heading")

A `varchar` containing the abbreviated name of a month (e.g., “Jan”, “Feb”, etc.).

### Usage example[¶](#id76 "Link to this heading")

Input:

```
SELECT PUBLIC.MONTH_SHORT_UDF(DATE '2021-10-26', 'uppercase');
SELECT PUBLIC.MONTH_SHORT_UDF(DATE '2021-10-26', 'lowercase');
SELECT PUBLIC.MONTH_SHORT_UDF(DATE '2021-10-26', 'firstOnly');
```

Copy

Output:

```
OCT
oct
Oct
```

Copy

## DATE\_TO\_INT\_UDF[¶](#date-to-int-udf "Link to this heading")

### Definition[¶](#id77 "Link to this heading")

UDF (User-Defined Function) that converts a date value to its numeric representation, similar to Teradata’s DATE-TO-NUMERIC function.

```
PUBLIC.DATE_TO_INT_UDF(DATE_TO_CONVERT DATE)
```

Copy

### Parameters[¶](#id78 "Link to this heading")

`DATE_TO_CONVERT` represents a date value that needs to be converted

Convert the date value to an integer format.

### Returns[¶](#id79 "Link to this heading")

Returns a date value in numeric format.

### Example[¶](#id80 "Link to this heading")

Input:

```
SELECT mod(date '2015-11-26', 5890), sin(current_date);

CREATE TABLE SAMPLE_TABLE
(
    VARCHAR_TYPE VARCHAR,
    CHAR_TYPE CHAR(11),
    INTEGER_TYPE INTEGER,
    DATE_TYPE DATE,
    TIMESTAMP_TYPE TIMESTAMP,
    TIME_TYPE TIME,
    PERIOD_TYPE PERIOD(DATE)
);

REPLACE VIEW SAMPLE_VIEW
AS
SELECT
CAST(DATE_TYPE AS SMALLINT),
CAST(DATE_TYPE AS DECIMAL),
CAST(DATE_TYPE AS NUMBER),
CAST(DATE_TYPE AS FLOAT),
CAST(DATE_TYPE AS INTEGER)
FROM SAMPLE_TABLE;
```

Copy

Output:

```
SELECT
mod(PUBLIC.DATE_TO_INT_UDF(date '2015-11-26'), 5890),
sin(PUBLIC.DATE_TO_INT_UDF(CURRENT_DATE()));

CREATE TABLE PUBLIC.SAMPLE_TABLE
(
    VARCHAR_TYPE VARCHAR,
    CHAR_TYPE CHAR(11),
    INTEGER_TYPE INTEGER,
    DATE_TYPE DATE,
    TIMESTAMP_TYPE TIMESTAMP,
    TIME_TYPE TIME,
    PERIOD_TYPE VARCHAR(24) COMMENT 'PERIOD(DATE)' /*** MSC-WARNING - MSCEWI1036 - PERIOD DATA TYPE "PERIOD(DATE)" CONVERTED TO VARCHAR ***/
);

CREATE OR REPLACE VIEW PUBLIC.SAMPLE_VIEW
AS
SELECT
PUBLIC.DATE_TO_INT_UDF(DATE_TYPE),
PUBLIC.DATE_TO_INT_UDF(DATE_TYPE),
PUBLIC.DATE_TO_INT_UDF(DATE_TYPE),
PUBLIC.DATE_TO_INT_UDF(DATE_TYPE),
PUBLIC.DATE_TO_INT_UDF(DATE_TYPE)
FROM PUBLIC.SAMPLE_TABLE;
```

Copy

## PERIOD\_UDF[¶](#period-udf "Link to this heading")

### Definition[¶](#id81 "Link to this heading")

A user-defined function (UDF) that replicates the P\_INTERSECT operator. This function compares two or more time periods and identifies where they overlap, returning the common time interval between them.

Creates a string representation of a period’s start and end values (for `TIMESTAMP` represents a data type that stores both date and time information., `TIME`, or `DATE` is a data type used to store calendar dates (year, month, and day) without time information. data types). This function emulates Teradata’s period value constructor function. The output string follows Snowflake’s default format for `PERIOD` values. To adjust the precision of the output, you can either:

* Modify the session parameter `timestamp_output_format`
* Use the three-parameter version of this UDF

More details about the source function can be found in the [Teradata documentation](https://docs.teradata.com/r/SQL-External-Routine-Programming/July-2021/SQL-Data-Type-Mapping/C-Data-Types/PERIOD-DATE/PERIOD-TIME/PERIOD-TIMESTAMP).

```
PERIOD_UDF(D1 TIMESTAMP_NTZ, D2 TIMESTAMP_NTZ)
PERIOD_UDF(D1 DATE, D2 DATE)
PERIOD_UDF(D1 TIME, D2 TIME)
PERIOD_UDF(D1 TIMESTAMP_NTZ, D2 TIMESTAMP_NTZ, PRECISIONDIGITS INT)
PERIOD_UDF(D1 TIME, D2 TIME, PRECISIONDIGITS INT)
PERIOD_UDF(D1 TIMESTAMP_NTZ)
PERIOD_UDF(D1 DATE)
PERIOD_UDF(D1 TIME)
```

Copy

### Parameters[¶](#id82 "Link to this heading")

`TIMESTAMP`

The TimeStamp data type represents a specific point in time, including both the date and time components.

`TIME`

The Time data type represents a specific time of day without a date component.

`DATE`

The Date data type represents a calendar date without a time component.

`PRECISIONDIGITS` specifies the number of decimal places to display in numeric values.

The number of digits to display in the time format.

### Returns[¶](#id83 "Link to this heading")

Returns a string representation of a `PERIOD` type value

### Usage example[¶](#id84 "Link to this heading")

Input:

```
SELECT
PERIOD_UDF('2005-02-03'),
PERIOD_UDF(date '2005-02-03'),
PERIOD_UDF(TIMESTAMP '2005-02-03 12:12:12.340000'),
PERIOD_UDF(TIMESTAMP '2005-02-03 12:12:12.340000');
```

Copy

Output:

```
2005-02-03*2005-02-04,
2005-02-03*2005-02-04,
2005-02-03 12:12:12.340000*2005-02-03 12:12:12.340001,
2005-02-03 12:12:12.340000*2005-02-03 12:12:12.340001
```

Copy

## DAYNAME\_LONG\_UDF (TIMESTAMP\_TZ, VARCHAR)[¶](#dayname-long-udf-timestamp-tz-varchar "Link to this heading")

Warning

This is the user-defined function (UDF) that accepts **two** **different parameter types.**

### Definition[¶](#id85 "Link to this heading")

Returns the full name of a weekday in your choice of uppercase, lowercase, or capitalized format (e.g., “MONDAY”, “monday”, or “Monday”).

```
PUBLIC.DAYNAME_LONG_UDF(INPUT TIMESTAMP_TZ, RESULTCASE VARCHAR)
```

Copy

### Parameters[¶](#id86 "Link to this heading")

`INPUT` TIMESTAMP\_TZ

The input date from which to determine the day of the week.

`RESULTCASE` VARCHAR

The expected outcome or scenario that will be demonstrated.

### Returns[¶](#id87 "Link to this heading")

Returns a string containing the full name of a day of the week.

### Usage example[¶](#id88 "Link to this heading")

Input:

```
SELECT PUBLIC.DAYNAME_LONG_UDF(DATE '2021-10-26', 'uppercase');
SELECT PUBLIC.DAYNAME_LONG_UDF(DATE '2021-10-26', 'lowercase');
SELECT PUBLIC.DAYNAME_LONG_UDF(DATE '2021-10-26', 'firstOnly');
```

Copy

Output:

```
'TUESDAY'
'tuesday'
'Tuesday'
```

Copy

## TD\_DAY\_OF\_WEEK\_COMPATIBLE\_UDF[¶](#td-day-of-week-compatible-udf "Link to this heading")

### Definition[¶](#id89 "Link to this heading")

Process a timestamp to determine which day of the week it falls on. This function behaves identically to `DAYNUMBER_OF_WEEK(DATE, 'COMPATIBLE')`.

```
PUBLIC.TD_DAY_OF_WEEK_COMPATIBLE_UDF(INPUT TIMESTAMP_TZ)
```

Copy

### Parameters[¶](#id90 "Link to this heading")

`INPUT` TIMESTAMP\_TZ

The input date used to determine the day of the week.

### Returns[¶](#id91 "Link to this heading")

Returns a number from 1 to 7 representing the day of the week, where 1 represents the first day of the week. For example, if January 1st falls on a Wednesday, then Wednesday = 1, Thursday = 2, Friday = 3, Saturday = 4, Sunday = 5, Monday = 6, and Tuesday = 7.

### Usage example[¶](#id92 "Link to this heading")

Input:

```
SELECT PUBLIC.TD_DAY_OF_WEEK_COMPATIBLE_UDF(DATE '2022-01-01'),
PUBLIC.TD_DAY_OF_WEEK_COMPATIBLE_UDF(DATE '2023-05-05');
```

Copy

Output:

```
1, 6
```

Copy

## JAROWINKLER\_UDF[¶](#jarowinkler-udf "Link to this heading")

### Definition[¶](#id93 "Link to this heading")

Calculates how similar two strings are using the Jaro-Winkler algorithm. This algorithm gives a score between 0 (completely different) and 1 (identical).

```
PUBLIC.JAROWINKLER_UDF (string1 VARCHAR, string2 VARCHAR)
```

Copy

### Parameters[¶](#id94 "Link to this heading")

`string1` of type VARCHAR

The text to be processed

`string2` of type VARCHAR

The text to be processed

### Returns[¶](#id95 "Link to this heading")

The function returns either 0 or 1.

### Usage example[¶](#id96 "Link to this heading")

Input:

```
SELECT PUBLIC.JAROWINKLER_UDF('święta', 'swieta')
```

Copy

Output:

```
0.770000
```

Copy

## YEAR\_BEGIN\_ISO\_UDF[¶](#year-begin-iso-udf "Link to this heading")

### Definition[¶](#id97 "Link to this heading")

UDF that calculates the first day of the ISO year for a given date. It works by finding the Monday closest to January 1st of the year, using the `DAYOFWEEKISO` function in combination with `PUBLIC.FIRST_DAY_JANUARY_OF_ISO_UDF`. The function either adds or subtracts days to locate this Monday.

```
PUBLIC.YEAR_BEGIN_ISO_UDF(INPUT DATE)
```

Copy

### Parameters[¶](#id98 "Link to this heading")

`INPUT` TIMESTAMP\_TZ

The date that represents January 1st of the current year according to the ISO calendar standard.

### Returns[¶](#id99 "Link to this heading")

The first day of the year according to the ISO calendar standard.

### Usage example[¶](#id100 "Link to this heading")

Input:

```
SELECT  PUBLIC.YEAR_BEGIN_ISO_UDF(DATE '2022-01-01'),
PUBLIC.YEAR_BEGIN_ISO_UDF(DATE '2022-04-12');
```

Copy

Output:

```
2021-01-04, 2022-01-03
```

Copy

## YEAR\_PART\_UDF[¶](#year-part-udf "Link to this heading")

### Definition[¶](#id101 "Link to this heading")

Extract the year from a date and truncate it to a specified number of digits.

```
PUBLIC.YEAR_PART_UDF(INPUT TIMESTAMP_TZ, DIGITS INTEGER)
```

Copy

### Parameters[¶](#id102 "Link to this heading")

`INPUT` TIMESTAMP\_TZ

The date from which to extract the year.

`DIGITS` A whole number that represents the maximum number of digits to display

The number of decimal places desired in the output.

### Returns[¶](#id103 "Link to this heading")

Extracts the year component from a specified date.

### Usage example[¶](#id104 "Link to this heading")

Input:

```
SELECT PUBLIC.YEAR_PART_UDF(DATE '2021-10-26', 3);
SELECT PUBLIC.YEAR_PART_UDF(DATE '2021-10-26', 2);
SELECT PUBLIC.YEAR_PART_UDF(DATE '2021-10-26', 1);
```

Copy

Output:

```
'021'
'21'
'1'
```

Copy

## YEAR\_WITH\_COMMA\_UDF[¶](#year-with-comma-udf "Link to this heading")

### Definition[¶](#id105 "Link to this heading")

Extracts the year from a date and adds a comma between the first and second digits. For example, if the year is 2023, it returns “2,023”.

```
PUBLIC.YEAR_WITH_COMMA_UDF(INPUT TIMESTAMP_TZ)
```

Copy

### Parameters[¶](#id106 "Link to this heading")

`INPUT` TIMESTAMP\_TZ

The input date from which to extract the year.

### Returns[¶](#id107 "Link to this heading")

Returns the year portion of a date value as a varchar (text) with a comma separator.

### Usage example[¶](#id108 "Link to this heading")

Input:

```
SELECT PUBLIC.YEAR_WITH_COMMA_UDF(DATE '2021-10-26');
```

Copy

Output:

```
'2,021'
```

Copy

## MONTHS\_BETWEEN\_UDF[¶](#months-between-udf "Link to this heading")

### Definition[¶](#id109 "Link to this heading")

Calculate the Number of Months Between Two Dates

```
MONTHS_BETWEEN_UDF(FIRST_DATE TIMESTAMP_LTZ, SECOND_DATE TIMESTAMP_LTZ)
```

Copy

### Parameters[¶](#id110 "Link to this heading")

`FIRST_DATE` is a timestamp column that includes both date and time information, with timezone support (TIMESTAMP\_LTZ)

The initial date from which the function will begin processing data.

`SECOND_DATE` TIMESTAMP\_LTZ

The ending date that defines when to stop counting.

### Returns[¶](#id111 "Link to this heading")

The duration in months between two dates.

### Usage example[¶](#id112 "Link to this heading")

Input:

```
SELECT MONTHS_BETWEEN_UDF('2022-02-14', '2021-02-14');
```

Copy

Output:

```
12
```

Copy

## SECONDS\_PAST\_MIDNIGHT\_UDF[¶](#seconds-past-midnight-udf "Link to this heading")

### Definition[¶](#id113 "Link to this heading")

Calculate the number of seconds elapsed since midnight for a specified time.

```
PUBLIC.SECONDS_PAST_MIDNIGHT_UDF(INPUT TIME)
```

Copy

### Parameters[¶](#id114 "Link to this heading")

`INPUT` TIME

The function calculates the total number of seconds elapsed since midnight (00:00:00) until the current time.

### Returns[¶](#id115 "Link to this heading")

A `varchar` value representing the number of seconds elapsed since midnight.

### Usage example[¶](#id116 "Link to this heading")

Input:

```
SELECT PUBLIC.SECONDS_PAST_MIDNIGHT_UDF(TIME'10:30:45');
```

Copy

Output:

```
'37845'
```

Copy

## CHAR2HEXINT\_UDF[¶](#char2hexint-udf "Link to this heading")

### Definition[¶](#id117 "Link to this heading")

Returns a string containing the hexadecimal (base-16) representation of each character in the input string.

```
PUBLIC.CHAR2HEXINT_UDF(INPUT_STRING VARCHAR);
```

Copy

### Parameters[¶](#id118 "Link to this heading")

`INPUT_STRING` is a variable of type VARCHAR that stores text data.

The input string that needs to be converted.

### Returns[¶](#id119 "Link to this heading")

Returns a string containing the hexadecimal representation of the input string.

### Example[¶](#id120 "Link to this heading")

Input:

```
SELECT CHAR2HEXINT('1234') from t1;
```

Copy

Output:

```
SELECT
PUBLIC.CHAR2HEXINT_UDF('1234') from
t1;
```

Copy

### More information from the source function[¶](#more-information-from-the-source-function "Link to this heading")

Function documentation is available in the [Teradata documentation](https://docs.teradata.com/r/SQL-Functions-Expressions-and-Predicates/June-2020/String-Operators-and-Functions/CHAR2HEXINT).

## INTERVAL\_ADD\_UDF[¶](#interval-add-udf "Link to this heading")

### Definition[¶](#id121 "Link to this heading")

UDFs (User-Defined Functions) that handle subtraction operations between an interval value and a column reference of type interval.

```
PUBLIC.INTERVAL_ADD_UDF
(INPUT_VALUE1 VARCHAR(), INPUT_PART1 VARCHAR(30), INPUT_VALUE2 VARCHAR(), INPUT_PART2 VARCHAR(30), OP CHAR, OUTPUT_PART VARCHAR())
```

Copy

### Parameters[¶](#id122 "Link to this heading")

`INPUT_VALUE1` of type VARCHAR

The input data that will be processed by the system.

`INPUT_PART1` of type VARCHAR

The time unit to be used, such as ‘`HOUR`’.

`INPUT_VALUE2` is a VARCHAR data type parameter.

The name of the referenced column, such as ‘`INTERVAL_HOUR_TYPE`’

`INPUT_PART2` VARCHAR

The data type assigned to the referenced column.

`OP` character

The symbol or operator that is currently being analyzed.

`OUTPUT_PART` VARCHAR

The data type of the returned value.

### Returns[¶](#id123 "Link to this heading")

A `varchar` value that represents the result of subtracting two time intervals.

### Migration example[¶](#id124 "Link to this heading")

Input:

```
CREATE TABLE INTERVAL_TABLE
(
    INTERVAL_YEAR_TYPE INTERVAL YEAR
);

SELECT INTERVAL_YEAR_TYPE - INTERVAL '7' MONTH FROM INTERVAL_TABLE;
```

Copy

Output:

```
CREATE OR REPLACE TABLE INTERVAL_TABLE
(
    INTERVAL_YEAR_TYPE VARCHAR(21) !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - INTERVAL YEAR DATA TYPE CONVERTED TO VARCHAR ***/!!!
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"teradata"}}'
;

SELECT
    PUBLIC.INTERVAL_ADD_UDF(INTERVAL_YEAR_TYPE, 'YEAR', '7', 'MONTH', '-', 'YEAR TO MONTH')
    FROM
    INTERVAL_TABLE;
```

Copy

## DAY\_OF\_WEEK\_LONG\_UDF[¶](#day-of-week-long-udf "Link to this heading")

### Definition[¶](#id125 "Link to this heading")

A user-defined function (UDF) that converts a timestamp into the full name of the day (for example, “Monday”, “Tuesday”, etc.).

```
PUBLIC.DAY_OF_WEEK_LONG_UDF(INPUT_DATE TIMESTAMP)
```

Copy

### Parameters[¶](#id126 "Link to this heading")

`INPUT_DATE` represents a timestamp value

The timestamp will be converted into a full day name (for example, “Monday”, “Tuesday”, etc.).

### Returns[¶](#id127 "Link to this heading")

The name of the day in English.

## TD\_WEEK\_OF\_CALENDAR\_UDF[¶](#td-week-of-calendar-udf "Link to this heading")

### Definition[¶](#id128 "Link to this heading")

The user-defined function (UDF) serves as a direct replacement for Teradata’s [TD\_WEEK\_OF\_CALENDAR](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/SQL-Date-and-Time-Functions-and-Expressions/Calendar-Functions/td_week_of_calendar) function, providing the same functionality in Snowflake.

```
PUBLIC.TD_WEEK_OF_CALENDAR_UDF(INPUT TIMESTAMP_TZ)
```

Copy

### Parameters[¶](#id129 "Link to this heading")

`INPUT` TIMESTAMP\_TZ

Date used to calculate the number of weeks that have elapsed since January 1, 1900.

### Returns[¶](#id130 "Link to this heading")

An integer representing the number of complete weeks between January 1, 1900, and the specified date

### Migration example[¶](#id131 "Link to this heading")

Input:

```
SELECT TD_WEEK_OF_CALENDAR(DATE '2023-11-30')
```

Copy

Output:

```
SELECT
PUBLIC.TD_WEEK_OF_CALENDAR_UDF(DATE '2023-11-30');
```

Copy

## WRAP\_NEGATIVE\_WITH\_ANGLE\_BRACKETS\_UDF[¶](#wrap-negative-with-angle-brackets-udf "Link to this heading")

### Definition[¶](#id132 "Link to this heading")

Converts negative numbers to use angle brackets (< >) instead of the minus sign (-). This conversion occurs when the PR (parentheses) format element is present in the original Teradata format string.

```
PUBLIC.WRAP_NEGATIVE_WITH_ANGLE_BRACKETS_UDF(INPUT NUMBER, FORMATARG VARCHAR)
```

Copy

### Parameters[¶](#id133 "Link to this heading")

`INPUT` is a numeric value

The numeric value that will be converted into a text string (varchar).

`FORMATARG` is a parameter of type VARCHAR that specifies the format of the data.

The format parameter specifies how to convert the INPUT value into a text (varchar) representation.

### Returns[¶](#id134 "Link to this heading")

A `varchar` containing negative numbers enclosed in angle brackets (< >).

### Usage example[¶](#id135 "Link to this heading")

Input:

```
SELECT PUBLIC.WRAP_NEGATIVE_WITH_ANGLE_BRACKETS_UDF(8456, '9999');
SELECT PUBLIC.WRAP_NEGATIVE_WITH_ANGLE_BRACKETS_UDF(-8456, '9999');
```

Copy

Output:

```
'8456'
'<8456>'
```

Copy

## INSTR\_UDF (STRING, STRING)[¶](#instr-udf-string-string "Link to this heading")

Warning

This is the user-defined function (UDF) that accepts **two** **different parameter sets**.

### Definition[¶](#id136 "Link to this heading")

Finds all instances where search\_string appears within source\_string.

```
PUBLIC.INSTR_UDF(SOURCE_STRING STRING, SEARCH_STRING STRING)
```

Copy

### Parameters[¶](#id137 "Link to this heading")

`SOURCE_STRING` represents the input string that needs to be processed

The text that will be searched.

`SEARCH_STRING` is a parameter of type STRING that specifies the text to search for.

The text pattern that the function will look for and match.

### Returns[¶](#id138 "Link to this heading")

The index position where the pattern is found in the source string (starting from position 1).

### Usage example[¶](#id139 "Link to this heading")

Input:

```
SELECT INSTR_UDF('INSTR FUNCTION','N');
```

Copy

Output:

```
2
```

Copy

## TRANSLATE\_CHK\_UDF[¶](#translate-chk-udf "Link to this heading")

### Definition[¶](#id140 "Link to this heading")

Checks whether the code can be successfully converted without generating any errors.

```
PUBLIC.TRANSLATE_CHK_UDF(COL_NAME STRING, SOURCE_REPERTOIRE_NAME STRING)
```

Copy

### Parameters[¶](#id141 "Link to this heading")

`COL_NAME` is a string variable that represents a column name.

The column that needs to be validated.

`SOURCE_REPERTOIRE_NAME` is a string parameter that specifies the name of the source directory.

The name of the source collection or library.

### Returns[¶](#id142 "Link to this heading")

0: The translation was successful and completed without errors.
NULL: No result was returned (null value).

The first character’s position in the string is causing a translation error.

### Usage example[¶](#id143 "Link to this heading")

Input:

```
SELECT PUBLIC.TRANSLATE_CHK_UDF('ABC', 'UNICODE_TO_LATIN');
```

Copy

Output:

```
0
```

Copy

## EXPAND\_ON\_UDF[¶](#expand-on-udf "Link to this heading")

Note

For better readability, we have simplified some sections of the code in this example.

### Definition[¶](#id144 "Link to this heading")

Replicates the behavior of Teradata’s expand-on function.

```
PUBLIC.EXPAND_ON_UDF(TIME STRING, SEQ NUMBER, PERIOD STRING)
```

Copy

### Parameters[¶](#id145 "Link to this heading")

`TIME` is a data type that stores time values as text (STRING).

The time required for the anchor to fully expand.

`SEQ` Sequence Number

The order in which each row’s values are computed.

`PERIOD` A text value representing a time period

The date for the specified time period.

### Returns[¶](#id146 "Link to this heading")

A `VARCHAR` value that defines how to calculate the expansion period in the expand-on clause.

### Migration example[¶](#id147 "Link to this heading")

Input:

```
SELECT bg FROM table1 EXPAND ON pd AS bg BY ANCHOR ANCHOR_SECOND;
```

Copy

Output:

```
WITH
ExpandOnCTE AS
(
SELECT
PUBLIC.EXPAND_ON_UDF('ANCHOR_SECOND', VALUE, pd) bg
FROM
table1,
TABLE(FLATTEN(PUBLIC.ROW_COUNT_UDF(PUBLIC.DIFF_TIME_PERIOD_UDF('ANCHOR_SECOND', pd))))
)
SELECT
bg
FROM
table1,
ExpandOnCTE;
```

Copy

## ROW\_COUNT\_UDF[¶](#row-count-udf "Link to this heading")

### Definition[¶](#id148 "Link to this heading")

Returns an array containing sequential numbers from 1 to the value returned by DIFF\_TIME\_PERIOD\_UDF.

```
PUBLIC.ROW_COUNT_UDF(NROWS DOUBLE)
```

Copy

### Parameters[¶](#id149 "Link to this heading")

`NROWS` represents the total number of rows in a dataset as a decimal number (DOUBLE)

The value returned by the DIFF\_TIME\_PERIOD\_UDF function.

### Returns[¶](#id150 "Link to this heading")

An array that determines the number of rows required to replicate the functionality of the EXPAND ON clause.

### Usage example[¶](#id151 "Link to this heading")

Input:

```
SELECT ROW_COUNT_UDF(DIFFTTIME_PERIOD('SECONDS','2022-11-26 10:15:20.000*2022-11-26 10:15:25.000'));
```

Copy

Output:

```
[1, 2, 3, 4, 5]
```

Copy

### Migration example[¶](#id152 "Link to this heading")

Input:

```
SELECT NORMALIZE emp_id, duration FROM project EXPAND ON duration AS bg BY ANCHOR ANCHOR_SECOND;
```

Copy

Output:

```
WITH ExpandOnCTE AS
(
SELECT
    PUBLIC.EXPAND_ON_UDF('ANCHOR_SECOND', VALUE, duration) bg
FROM
    project,
TABLE(FLATTEN(PUBLIC.ROW_COUNT_UDF(PUBLIC.DIFF_TIME_PERIOD_UDF('ANCHOR_SECOND', duration))))
)
SELECT NORMALIZE emp_id,
    duration
FROM
    project,
    ExpandOnCTE;
```

Copy

## CENTURY\_UDF[¶](#century-udf "Link to this heading")

### Definition[¶](#id153 "Link to this heading")

Calculates the century for a given date.

```
PUBLIC.CENTURY_UDF(INPUT TIMESTAMP_TZ)
```

Copy

### Parameters[¶](#id154 "Link to this heading")

`INPUT` TIMESTAMP\_TZ

The input date used to determine the century.

### Returns[¶](#id155 "Link to this heading")

Returns the century number as a varchar for a given date.

### Usage example[¶](#id156 "Link to this heading")

Input:

```
SELECT PUBLIC.CENTURY_UDF(DATE '1915-02-23');
```

Copy

Output:

```
'20'
```

Copy

## TIME\_DIFFERENCE\_UDF[¶](#time-difference-udf "Link to this heading")

Warning

This UDF has been deprecated as Snowflake now provides a built-in equivalent function. For more details, please refer to the [TIMEDIFF documentation](../../../../../../sql-reference/functions/timediff).

### Definition[¶](#id157 "Link to this heading")

Calculates the time interval between two given timestamps.

```
PUBLIC.TIME_DIFFERENCE_UDF
(MINUEND TIME, SUBTRAHEND TIME, INPUT_PART VARCHAR)
```

Copy

### Parameters[¶](#id158 "Link to this heading")

`MINUEND` A timestamp value that will be subtracted from

Time to be subtracted from the original value.

`SUBTRAHEND` The timestamp value to be subtracted from another timestamp

Time has been subtracted.

`INPUT_PART` is a variable of type VARCHAR that stores input data.

`EXTRACT_PART` is a variable of type VARCHAR that stores the extracted portion of a string.

Extract a numeric value from a time interval.

### Returns[¶](#id159 "Link to this heading")

A text value (VARCHAR) representing a specific time.

### Example[¶](#id160 "Link to this heading")

Input:

```
select extract(day from (timestampColumn1 - timestampColumn2 day to hour)) from tableName;
```

Copy

Output:

```
SELECT
EXTRACT_TIMESTAMP_DIFFERENCE_UDF(timestampColumn1, timestampColumn2, 'DAY TO HOUR', 'DAY')
                                 from
tableName;
```

Copy

## INTERVAL\_DIVIDE\_UDF[¶](#interval-divide-udf "Link to this heading")

### Definition[¶](#id161 "Link to this heading")

A custom function (UDF) that performs interval division calculations.

```
PUBLIC.INTERVAL_DIVIDE_UDF
(INPUT_PART VARCHAR(30), INPUT_VALUE VARCHAR(), INPUT_DIV INTEGER)
```

Copy

### Parameters[¶](#id162 "Link to this heading")

`INPUT_PART` is a variable of type VARCHAR that represents the input portion of the data.

The value that specifies the interval type, such as ‘YEAR TO MONTH’.

`INPUT_VALUE` VARCHAR

The time interval to be divided.

`INPUT_DIV` is an integer value that represents the input divisor.

The number that will be divided by another number.

### Returns[¶](#id163 "Link to this heading")

The output is calculated by dividing a time interval by a numeric value.

### Migration example[¶](#id164 "Link to this heading")

Input:

```
SELECT INTERVAL '6-10' YEAR TO MONTH / 8;
```

Copy

Output:

```
SELECT
PUBLIC.INTERVAL_DIVIDE_UDF('YEAR TO MONTH', '6-10', 8);
```

Copy

## DAYNUMBER\_OF\_MONTH\_UDF[¶](#daynumber-of-month-udf "Link to this heading")

### Definition[¶](#id165 "Link to this heading")

The UDF determines which day of the month a given timestamp falls on. It functions similarly to Teradata’s DAYNUMBER\_OF\_MONTH(DATE, ‘ISO’) function.

```
PUBLIC.DAYNUMBER_OF_MONTH_UDF(INPUT TIMESTAMP_TZ)
```

Copy

### Parameters[¶](#id166 "Link to this heading")

`INPUT` TIMESTAMP\_TZ

A date value that will be used to determine the corresponding day of the week.

### Returns[¶](#id167 "Link to this heading")

A whole number from 1 to 33 (inclusive).

### Example[¶](#id168 "Link to this heading")

Input:

```
SELECT DAYNUMBER_OF_MONTH (DATE'2022-12-22', 'ISO');
```

Copy

Output:

```
SELECT
PUBLIC.DAYNUMBER_OF_MONTH_UDF(DATE'2022-12-22');
```

Copy

## LAST\_DAY\_DECEMBER\_OF\_ISO\_UDF[¶](#last-day-december-of-iso-udf "Link to this heading")

### Definition[¶](#id169 "Link to this heading")

UDF (User-Defined Function) that processes December 31st and returns the corresponding ISO year. This function is used as a component of the PUBLIC.YEAR\_END\_IDO\_UDF calculation.

```
PUBLIC.LAST_DAY_DECEMBER_OF_ISO_UDF(INPUT TIMESTAMP_TZ)
```

Copy

### Parameters[¶](#id170 "Link to this heading")

`INPUT` TIMESTAMP\_TZ

To get the last day of December using the ISO year format, use December 31st.

### Returns[¶](#id171 "Link to this heading")

A date representing December 31st in ISO year format.

### Usage example[¶](#id172 "Link to this heading")

Input:

```
SELECT PUBLIC.LAST_DAY_DECEMBER_OF_ISO_UDF(DATE '2022-01-01');
```

Copy

Output:

```
2021-12-31
```

Copy

## DATEADD\_UDF[¶](#dateadd-udf "Link to this heading")

Note

For better readability, we have simplified some sections of the code in this example.

### Definition[¶](#id173 "Link to this heading")

Function to Calculate the Sum of Two Dates

```
PUBLIC.DATE_ADD_UDF(FIRST_DATE DATE, SECOND_DATE DATE)
```

Copy

### Parameters[¶](#id174 "Link to this heading")

`FIRST_DATE` represents a column of type DATE

The initial date value to be included.

`SECOND_DATE` represents a column of type DATE

Add the second date value together with first\_date.

### [¶](#id175 "Link to this heading")

### Returns[¶](#id176 "Link to this heading")

The result is a date calculated by combining both input parameters.

### Example[¶](#id177 "Link to this heading")

Input:

```
SELECT
    CAST(CAST (COLUMNB AS DATE FORMAT 'MM/DD/YYYY') AS TIMESTAMP(0))
    +
    CAST (COLUMNA AS TIME(0) FORMAT 'HHMISS' )
FROM TIMEDIFF;
```

Copy

Output:

```
SELECT
    PUBLIC.DATEADD_UDF(CAST(CAST(COLUMNB AS DATE) !!!RESOLVE EWI!!! /*** SSC-EWI-0033 - FORMAT 'MM/DD/YYYY' REMOVED, SEMANTIC INFORMATION NOT FOUND. ***/!!! AS TIMESTAMP(0)), PUBLIC.TO_INTERVAL_UDF(CAST(COLUMNA AS TIME(0)) !!!RESOLVE EWI!!! /*** SSC-EWI-0033 - FORMAT 'HHMISS' REMOVED, SEMANTIC INFORMATION NOT FOUND. ***/!!!))
    FROM
    TIMEDIFF;
```

Copy

## JULIAN\_TO\_DATE\_UDF[¶](#julian-to-date-udf "Link to this heading")

### Definition[¶](#id178 "Link to this heading")

A user-defined function (UDF) that converts a Julian Date format (YYYYDDD) into a standard Gregorian calendar date (YYYY-MM-DD).

```
PUBLIC.JULIAN_TO_DATE_UDF(JULIAN_DATE CHAR(7))
```

Copy

### Parameters[¶](#id179 "Link to this heading")

`JULIAN_DATE` CHAR - A character data type used to store dates in Julian format.

The date to be converted from Julian format.

### Returns[¶](#id180 "Link to this heading")

Returns the date representation of the Julian date, or null if the conversion cannot be performed.

### Usage example[¶](#id181 "Link to this heading")

Input:

```
SELECT JULIAN_TO_DATE_UDF('2022045');
```

Copy

Output:

```
'2022-02-14'
```

Copy

### Migration example[¶](#id182 "Link to this heading")

Input:

```
SELECT TO_DATE('2020002', 'YYYYDDD');
```

Copy

Output:

```
SELECT
PUBLIC.JULIAN_TO_DATE_UDF('2020002');
```

Copy

## FIRST\_DAY\_JANUARY\_OF\_ISO\_UDF[¶](#first-day-january-of-iso-udf "Link to this heading")

### Definition[¶](#id183 "Link to this heading")

The first day of January in the ISO calendar year, which is used by the `PUBLIC.YEAR_BEGIN_ISO_UDF` function to calculate its result.

```
FUNCTION PUBLIC.FIRST_DAY_JANUARY_OF_ISO_UDF(INPUT TIMESTAMP_TZ)
```

Copy

### Parameters[¶](#id184 "Link to this heading")

`INPUT` TIMESTAMP\_TZ

The date that represents January 1st using the ISO calendar year format.

### Returns[¶](#id185 "Link to this heading")

A date representing January 1st of the specified ISO calendar year.

### Usage example[¶](#id186 "Link to this heading")

Input:

```
SELECT PUBLIC.FIRST_DAY_JANUARY_OF_ISO_UDF(DATE '2022-01-01');
```

Copy

Output:

```
2021-01-01
```

Copy

## TIMESTAMP\_DIFFERENCE\_UDF[¶](#timestamp-difference-udf "Link to this heading")

### Definition[¶](#id187 "Link to this heading")

How to Subtract Two Dates Using a User-Defined Function (UDF)

```
PUBLIC.TIMESTAMP_DIFFERENCE_UDF
(MINUEND TIMESTAMP, SUBTRAHEND TIMESTAMP, INPUT_PART VARCHAR)
```

Copy

### Differences between Teradata and Snowflake date time subtraction[¶](#differences-between-teradata-and-snowflake-date-time-subtraction "Link to this heading")

Teradata and Snowflake use different methods for date and time calculations. They differ in their syntax, output data types, and precision levels.

* **Syntax:** In Teradata, DATE, TIMESTAMP, and TIME subtraction uses a minus sign and interval to specify the result’s format. For more details, see <https://docs.teradata.com/r/w19R4KsuHIiEqyxz0WYfgA/7kLLsWrP0kHxbk3iida0mA>. Snowflake handles these operations differently using three functions:

  + DATEDIFF (works with all date types)
  + TIMESTAMPDIFF
  + TIMEDIFF
    Each function requires the two dates to compare and the date part to return. For DATE types, you can also use the minus sign, which returns the difference in days.
* **Return Type:** Teradata returns various Interval types (see <https://www.docs.teradata.com/r/T5QsmcznbJo1bHmZT2KnFw/z~5iW7rYVstcmNYbd6Dsjg>). Snowflake’s functions return an Integer representing the number of units. For details, see <https://docs.snowflake.com/en/sql-reference/functions/datediff.html>
* **Rounding:** The way DATEDIFF handles date parts may produce different results than Teradata. Check <https://docs.snowflake.com/en/sql-reference/functions/datediff.html#usage-notes> for specific rounding behavior.

Warning

When performing date calculations, results may differ by one day due to rounding or timezone differences.

### Parameters[¶](#id188 "Link to this heading")

`MINUEND` A timestamp value that will be subtracted from represents the timestamp value that will be subtracted from

The date being used as the starting point for subtraction.

`SUBTRAHEND` is a timestamp value that will be subtracted from another timestamp.

The date has been removed.

`INPUT_PART` is a variable of type VARCHAR (variable-length character string)

Parts that need to be returned.

### Returns[¶](#id189 "Link to this heading")

Format the string value based on the specified `INPUT_PART` parameter.

### Example[¶](#id190 "Link to this heading")

Input:

```
select (timestampColumn1 - timestampColumn2 YEAR) from tableName;
```

Copy

```
SELECT
(
PUBLIC.TIMESTAMP_DIFFERENCE_UDF(timestampColumn1, timestampColumn2, 'YEAR')) from
tableName;
```

Copy

## FIRST\_DAY\_OF\_MONTH\_ISO\_UDF[¶](#first-day-of-month-iso-udf "Link to this heading")

### Definition[¶](#id191 "Link to this heading")

The User-defined function (UDF) returns the first day of a given month in ISO format (YYYY-MM-DD).

```
PUBLIC.FIRST_DAY_OF_MONTH_ISO_UDF(YEAR NUMBER, MONTH NUMBER)
```

Copy

### Parameters[¶](#id192 "Link to this heading")

`YEAR` is a numeric data type used to store a four-digit year value.

A numeric value representing a calendar year (e.g., 2023).

`MONTH` A numeric value representing a month (1-12)

A numeric value (1-12) representing a calendar month.

### Returns[¶](#id193 "Link to this heading")

Returns the first day of the current month in ISO format (YYYY-MM-DD).

### Example[¶](#id194 "Link to this heading")

Note

This UDF is a helper function that is used within the [**`DAYNUMBER_OF_MONTH_UDF`**](#) function.

## INT\_TO\_DATE\_UDF[¶](#int-to-date-udf "Link to this heading")

### Definition[¶](#id195 "Link to this heading")

UDF to Convert Numeric Values to Dates (Teradata Compatibility Function)

```
PUBLIC.INT_TO_DATE_UDF(NUMERIC_EXPRESSION INTEGER)
```

Copy

### Parameters[¶](#id196 "Link to this heading")

`NUMERIC_EXPRESSION` represents a numeric value or expression that evaluates to an integer

A value that represents a date in a specific format, such as YYYY-MM-DD

### Returns[¶](#id197 "Link to this heading")

Number converted to a date format.

### Example[¶](#id198 "Link to this heading")

Input:

```
SELECT * FROM table1
WHERE date_column > 1011219
```

Copy

Output:

```
SELECT
* FROM
table1
WHERE date_column > PUBLIC.INT_TO_DATE_UDF( 1011219);
```

Copy

## NULLIFZERO\_UDF[¶](#nullifzero-udf "Link to this heading")

### Definition[¶](#id199 "Link to this heading")

Replaces zero values with NULL in the data to prevent division by zero errors.

```
PUBLIC.NULLIFZERO_UDF(NUMBER_TO_VALIDATE NUMBER)
```

Copy

### Parameters[¶](#id200 "Link to this heading")

`NUMBER_TO_VALIDATE` NUMBER

The number that needs to be validated.

### Returns[¶](#id201 "Link to this heading")

Returns null if the input number is zero; otherwise, returns the original number.

### Usage example[¶](#id202 "Link to this heading")

```
SELECT NULLIFZERO_UDF(0);
```

Copy

Output:

```
NULL
```

Copy

## DATE\_LONG\_UDF[¶](#date-long-udf "Link to this heading")

### Definition[¶](#id203 "Link to this heading")

Converts a date into the format ‘Day, Month DD, YYYY’ (for example, ‘Monday, January 01, 2024’). This format matches Teradata’s DL date format element.

```
PUBLIC.DATE_LONG_UDF(INPUT TIMESTAMP_TZ)
```

Copy

### Parameters[¶](#id204 "Link to this heading")

`INPUT` TIMESTAMP\_TZ

The date should be displayed in a long date format (for example: “September 15, 2023”).

### Returns[¶](#id205 "Link to this heading")

A `VARCHAR` data type that represents the Teradata DL format element.

### Usage example[¶](#id206 "Link to this heading")

Input:

```
SELECT PUBLIC.DATE_LONG_UDF(DATE '2021-10-26');
```

Copy

Output:

```
'Tuesday, October 26, 2021'
```

Copy

## TD\_MONTH\_OF\_CALENDAR\_UDF[¶](#td-month-of-calendar-udf "Link to this heading")

### Definition[¶](#id207 "Link to this heading")

The user-defined function (UDF) serves as a replacement for Teradata’s [TD\_MONTH\_OF\_CALENDAR](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/SQL-Date-and-Time-Functions-and-Expressions/Calendar-Functions/td_month_of_calendar) function, providing the same functionality.

```
PUBLIC.TD_MONTH_OF_CALENDAR_UDF(INPUT TIMESTAMP_TZ)
```

Copy

### Parameters[¶](#id208 "Link to this heading")

`INPUT` TIMESTAMP\_TZ

Date used to calculate the number of months elapsed since January 1, 1900.

### Returns[¶](#id209 "Link to this heading")

An integer representing the number of months between January 1, 1900 and the specified date

### Migration example[¶](#id210 "Link to this heading")

Input:

```
SELECT TD_MONTH_OF_CALENDAR(DATE '2023-11-30')
```

Copy

Output:

```
SELECT
PUBLIC.TD_MONTH_OF_CALENDAR_UDF(DATE '2023-11-30');
```

Copy

## MONTH\_NAME\_LONG\_UDF[¶](#month-name-long-udf "Link to this heading")

### Definition[¶](#id211 "Link to this heading")

A user-defined function (UDF) that converts a timestamp into its corresponding full month name.

```
PUBLIC.MONTH_NAME_LONG_UDF(INPUT_DATE TIMESTAMP)
```

Copy

### Parameters[¶](#id212 "Link to this heading")

`INPUT` DATE

The timestamp should be converted to display the full month name.

### Returns[¶](#id213 "Link to this heading")

The name of the month in English.

## TD\_DAY\_OF\_CALENDAR\_UDF[¶](#td-day-of-calendar-udf "Link to this heading")

### Definition[¶](#id214 "Link to this heading")

User-defined function (UDF) that replicates Teradata’s `TO_DAY_OF_CALENDAR` functionality

```
PUBLIC.TD_DAY_OF_CALENDAR_UDF(INPUT TIMESTAMP_TZ)
```

Copy

### Parameters[¶](#id215 "Link to this heading")

`INPUT` TIMESTAMP\_TZ

Date used to calculate the number of days elapsed since January 1, 1900.

### Returns[¶](#id216 "Link to this heading")

An integer representing the number of days between January 1, 1900 and the `INPUT` date

### Migration example[¶](#id217 "Link to this heading")

Input:

```
SELECT td_day_of_calendar(current_date)
```

Copy

Output:

```
SELECT
PUBLIC.TD_DAY_OF_CALENDAR_UDF(CURRENT_DATE());
```

Copy

## PERIOD\_TO\_TIME\_UDF[¶](#period-to-time-udf "Link to this heading")

### Definition[¶](#id218 "Link to this heading")

Function that converts a Teradata PERIOD value to a TIME value, maintaining Teradata’s casting behavior.

```
PERIOD_TO_TIME_UDF(PERIOD_VAL VARCHAR(22))
```

Copy

### Parameters[¶](#id219 "Link to this heading")

`PERIOD_VAL` represents a time period value

The time period that needs to be converted.

### Returns[¶](#id220 "Link to this heading")

The function returns a `TIME` value representing the `PERIOD`. If the conversion cannot be completed, it returns null.

### Usage example[¶](#id221 "Link to this heading")

Input:

```
SELECT PERIOD_TO_TIME_UDF(PERIOD_UDF(CURRENT_TIME()));
```

Copy

Output:

```
08:42:04
```

Copy

## INSTR\_UDF (STRING, STRING, DOUBLE, DOUBLE)[¶](#instr-udf-string-string-double-double "Link to this heading")

Warning

This user-defined function (UDF) accepts **four** **input parameters**.

### Definition[¶](#id222 "Link to this heading")

Finds all instances where search\_string appears within source\_string.

```
PUBLIC.INSTR_UDF(SOURCE_STRING STRING, SEARCH_STRING STRING, POSITION DOUBLE, OCCURRENCE DOUBLE)
```

Copy

### Parameters[¶](#id223 "Link to this heading")

`SOURCE_STRING` represents the input string that needs to be processed

The text string that will be searched.

`SEARCH_STRING` is a text value that you want to search for.

The text pattern that the function will look for and match.

`POSITION` DOUBLE - A numeric data type that stores decimal numbers with double precision.

The position in the text where the search will begin (starting from position 1).

`OCCURRENCE` DOUBLE - A numeric data type that represents the number of times an event occurs, stored as a double-precision floating-point number.

The position in the text where the search will begin (starting from position 1).

### Returns[¶](#id224 "Link to this heading")

The index position where the specified text is found within the source string.

### Usage example[¶](#id225 "Link to this heading")

Input:

```
SELECT INSTR_UDF('CHOOSE A CHOCOLATE CHIP COOKIE','CH',2,2);
```

Copy

Output:

```
20
```

Copy

## ROUND\_DATE\_UDF[¶](#round-date-udf "Link to this heading")

### Definition[¶](#id226 "Link to this heading")

A user-defined function (UDF) that processes a DATE\_VALUE by rounding the time portion to a specified unit (UNIT\_TO\_ROUND\_BY). This function is similar to the Teradata ROUND(date) function.

```
PUBLIC.ROUND_DATE_UDF(DATE_TO_ROUND TIMESTAMP_LTZ, UNIT_TO_ROUND_BY VARCHAR(5))
```

Copy

### Parameters[¶](#id227 "Link to this heading")

`DATE_TO_ROUND` TIMESTAMP\_TZ (A timestamp value with timezone information that needs to be rounded)

The date value that needs to be rounded.

`UNIT_TO_ROUND_BY` VARCHAR - Specifies the time unit used for rounding

The time unit used for rounding the date.

### Returns[¶](#id228 "Link to this heading")

Returns a date rounded to the specified time unit. The UNIT\_TO\_ROUND\_BY parameter determines how the date will be rounded.

### Migration example[¶](#id229 "Link to this heading")

Input:

```
SELECT ROUND(CURRENT_DATE, 'RM') RND_DATE
```

Copy

Output:

```
SELECT
PUBLIC.ROUND_DATE_UDF(CURRENT_DATE(), 'RM') RND_DATE;
```

Copy

## SUBSTR\_UDF (STRING, FLOAT, FLOAT)[¶](#substr-udf-string-float-float "Link to this heading")

Warning

This is the user-defined function (UDF) that accepts **three** **parameters**.

### Definition[¶](#id230 "Link to this heading")

Retrieves a portion of text from a specified string by using starting and ending positions.

```
PUBLIC.SUBSTR_UDF(BASE_EXPRESSION STRING, START_POSITION FLOAT, LENGTH FLOAT)
```

Copy

### Parameters[¶](#id231 "Link to this heading")

`BASE_EXPRESSION` is a string parameter that defines the base expression.

The source text from which you want to extract a portion.

`START_POSITION` is a floating-point number that defines the initial position.

The position where you want to begin extracting characters from the string.

`LENGTH` is a floating-point number that represents the length value.

The position where you want to begin extracting characters from the string.

### Returns[¶](#id232 "Link to this heading")

The substring that must be included.

### Usage example[¶](#id233 "Link to this heading")

Input:

```
SELECT 
    PUBLIC.SUBSTR_UDF('ABC', -1, 1),
    PUBLIC.SUBSTR_UDF('ABC', -1, 2),
    PUBLIC.SUBSTR_UDF('ABC', -1, 3),
    PUBLIC.SUBSTR_UDF('ABC', 0, 1),
    PUBLIC.SUBSTR_UDF('ABC', 0, 2);
```

Copy

Output:

```
'','','A','','A'
```

Copy

## GETQUERYBANDVALUE\_UDF (VARCHAR)[¶](#getquerybandvalue-udf-varchar "Link to this heading")

Warning

This is the user-defined function (UDF) that accepts **one** **parameter**.

### Definition[¶](#id234 "Link to this heading")

Returns a value from a name-value pair stored in the transaction, session, or profile query band.

```
GETQUERYBANDVALUE_UDF(SEARCHNAME VARCHAR)
```

Copy

### Parameters[¶](#id235 "Link to this heading")

`SEARCHNAME` VARCHAR - A variable of type VARCHAR used to store search terms or names. - A variable of type VARCHAR used to store search terms or names.

The name to search for within the key-value pairs.

### Returns[¶](#id236 "Link to this heading")

The session query band’s “name” key value, or null if not present.

### Usage example[¶](#id237 "Link to this heading")

Input:

```
ALTER SESSION SET QUERY_TAG = 'user=Tyrone;role=security';
SELECT GETQUERYBANDVALUE_UDF('role');
```

Copy

Output:

```
security
```

Copy

### Migration example[¶](#id238 "Link to this heading")

Input:

```
SELECT GETQUERYBANDVALUE(1, 'group');
```

Copy

Output:

```
/** MSC-ERROR - MSCEWI2084 - TRANSACTION AND PROFILE LEVEL QUERY TAGS NOT SUPPORTED IN SNOWFLAKE, REFERENCING SESSION QUERY TAG INSTEAD **/
SELECT GETQUERYBANDVALUE_UDF('group');
```

Copy

## TD\_WEEK\_OF\_YEAR\_UDF[¶](#td-week-of-year-udf "Link to this heading")

### Definition[¶](#id239 "Link to this heading")

User-defined function (UDF) that calculates the full week number of a given date within the year. This function provides the same functionality as Teradata’s `TD_WEEK_OF_YEAR` and `WEEKNUMBER_OF_YEAR` functions.

```
PUBLIC.TD_WEEK_OF_YEAR_UDF(INPUT TIMESTAMP_TZ)
```

Copy

### Parameters[¶](#id240 "Link to this heading")

`INPUT` TIMESTAMP\_TZ

Date used to calculate the week number.

### Returns[¶](#id241 "Link to this heading")

A numerical value indicating which week of the year the specified date falls into.

### Usage example[¶](#id242 "Link to this heading")

Input:

```
SELECT PUBLIC.WEEK_OF_YEAR_UDF(DATE '2024-05-10'),
PUBLIC.WEEK_OF_YEAR_UDF(DATE '2020-01-03')
```

Copy

Output:

```
18, 0
```

Copy

## EXTRACT\_TIMESTAMP\_DIFFERENCE\_UDF[¶](#extract-timestamp-difference-udf "Link to this heading")

Note

For better readability, we have simplified the code examples by showing only the most relevant parts.

### Definition[¶](#id243 "Link to this heading")

Retrieves the ‘Data’ portion from the result of subtracting `SUBTRAHEND` from `MINUEND`

```
PUBLIC.EXTRACT_TIMESTAMP_DIFFERENCE_UDF
(MINUEND TIMESTAMP, SUBTRAHEND TIMESTAMP, INPUT_PART VARCHAR, EXTRACT_PART VARCHAR)
```

Copy

### Differences between Teradata and Snowflake date-time extraction[¶](#differences-between-teradata-and-snowflake-date-time-extraction "Link to this heading")

Teradata and Snowflake functions may have different parameter requirements and return different data types.

* **Parameters:** The key distinction between Teradata and Snowflake’s EXTRACT functions is that Snowflake only works with dates and times, while Teradata also supports intervals. For more details, refer to [Snowflake’s EXTRACT function documentation](https://docs.snowflake.com/en/sql-reference/functions/extract.html) and [Teradata’s EXTRACT function documentation](https://docs.teradata.com/r/kmuOwjp1zEYg98JsB8fu_A/SIkE2wnHyQBnU4AGWRZSRw).
* **Return type:** The functions return values differently: Teradata’s EXTRACT returns either an integer or decimal(8, 2), while Snowflake’s EXTRACT returns a number representing the requested date-time part.

Teradata and Snowflake functions may have different input parameters and output types.

### Parameters[¶](#id244 "Link to this heading")

`MINUEND` TIMESTAMP

The date being used as the starting point for subtraction.

`SUBTRAHEND` The timestamp value to be subtracted from another timestamp

The date has been removed.

`INPUT_PART` VARCHAR

The formatted varchar must match the original requested part (which is the same as `TIMESTAMP_DIFERENCE` `INPUT_PART`) and must be one of the following:

* `'DAY TO HOUR'`
* `'DAY TO MINUTE'`
* `'DAY TO SECOND'`
* `'DAY TO MINUTE'`
* `'HOUR TO MINUTE'`
* `'HOUR TO SECOND'`
* `'MINUTE TO SECOND'`

`EXTRACT_PART` is a VARCHAR data type that represents the extracted portion of a string.

The time unit for extraction must be one of the following values: `'DAY'`, `'HOUR'`, `'MINUTE'`, or `'SECOND'`. The requested time unit should fall within the input time interval.

### Returns[¶](#id245 "Link to this heading")

The number of requests included in the extraction process.

### Example[¶](#id246 "Link to this heading")

Input:

```
select extract(day from (timestampColumn1 - timestampColumn2 day to hour)) from tableName;
```

Copy

Output:

```
SELECT
EXTRACT_TIMESTAMP_DIFFERENCE_UDF(timestampColumn1, timestampColumn2, 'DAY TO HOUR', 'DAY')
from
tableName;
```

Copy

## JSON\_EXTRACT\_DOT\_NOTATION\_UDF[¶](#json-extract-dot-notation-udf "Link to this heading")

### Definition[¶](#id247 "Link to this heading")

A user-defined function (UDF) that allows you to query JSON objects using dot notation, similar to how you would access nested properties in JavaScript or Python.

```
JSON_EXTRACT_DOT_NOTATION_UDF(JSON_OBJECT VARIANT, JSON_PATH STRING)
```

Copy

### Differences between Teradata JSON Entity Reference (dot notation ) and Snowflake JSON query method.[¶](#differences-between-teradata-json-entity-reference-dot-notation-and-snowflake-json-query-method "Link to this heading")

Teradata and Snowflake use different methods to traverse JSON data. Teradata uses a JavaScript-based approach with dot notation, array indexing, and special operators like wildcard access and double dot notation. In contrast, Snowflake has more limited JSON traversal capabilities, only supporting direct member access and array indexing.

### Parameters[¶](#id248 "Link to this heading")

`JSON_OBJECT` A data type that represents a JSON object, which can contain nested key-value pairs of varying data types.

The JSON object containing the values you want to extract.

`JSON_PATH` A string parameter that specifies the path to extract data from a JSON document

The location within the JSON\_OBJECT where the values can be found, specified using JSON path notation.

### Returns[¶](#id249 "Link to this heading")

The data elements within the JSON\_OBJECT that match the specified JSON\_PATH.

### Migration example[¶](#id250 "Link to this heading")

Input:

```
SELECT CAST(varcharColumn AS JSON(2000))..name FROM variantTest;
```

Copy

Output:

```
SELECT
JSON_EXTRACT_DOT_NOTATION_UDF(CAST(varcharColumn AS VARIANT), '$..name')
FROM
variantTest;
```

Copy

## WEEK\_OF\_MONTH\_UDF[¶](#week-of-month-udf "Link to this heading")

### Definition[¶](#id251 "Link to this heading")

Calculates which week of the month a specific date falls into.

```
PUBLIC.WEEK_OF_MONTH_UDF(INPUT TIMESTAMP_TZ)
```

Copy

### Parameters[¶](#id252 "Link to this heading")

`INPUT` TIMESTAMP\_TZ

The date used to determine which week of the month it falls into.

### Returns[¶](#id253 "Link to this heading")

A VARCHAR column that displays which week of the month a specific date falls in.

### Usage example[¶](#id254 "Link to this heading")

Input:

```
SELECT PUBLIC.WEEK_OF_MONTH_UDF(DATE '2021-10-26');
```

Copy

Output:

```
'4'
```

Copy

## DAYNAME\_LONG\_UDF (TIMESTAMP\_TZ)[¶](#dayname-long-udf-timestamp-tz "Link to this heading")

Warning

This is the user-defined function (UDF) that accepts **one** **parameter**.

### Definition[¶](#id255 "Link to this heading")

UDF that creates a variant of the DAYNAME\_LONG\_UDF function which returns day names with the first letter capitalized (default format).

```
PUBLIC.DAYNAME_LONG_UDF(INPUT TIMESTAMP_TZ)
```

Copy

### Parameters[¶](#id256 "Link to this heading")

`INPUT` TIMESTAMP\_TZ

The date from which you want to get the day of the week.

### Returns[¶](#id257 "Link to this heading")

Returns a string containing the full name of a day of the week.

### Usage example[¶](#id258 "Link to this heading")

Input:

```
SELECT PUBLIC.DAYNAME_LONG_UDF(DATE '2022-06-30');
```

Copy

Output:

```
'Thursday'
```

Copy

## INTERVAL\_TO\_MONTHS\_UDF[¶](#interval-to-months-udf "Link to this heading")

### Definition[¶](#id259 "Link to this heading")

Converts a time interval into months.

```
PUBLIC.INTERVAL_TO_MONTHS_UDF
(INPUT_VALUE VARCHAR())
```

Copy

### Parameters[¶](#id260 "Link to this heading")

`INPUT_VALUE` VARCHAR

The time period that will be changed into months.

### Returns[¶](#id261 "Link to this heading")

The number of months to be processed, specified as an integer.

## GETQUERYBANDVALUE\_UDF (VARCHAR, FLOAT, VARCHAR)[¶](#getquerybandvalue-udf-varchar-float-varchar "Link to this heading")

Warning

This user-defined function (UDF) accepts three parameters.

### Definition[¶](#id262 "Link to this heading")

Returns a value from a name-value pair stored in the transaction, session, or profile query band. The value is associated with a specific name in the query band.

```
GETQUERYBANDVALUE_UDF(QUERYBAND VARCHAR, SEARCHTYPE FLOAT, SEARCHNAME VARCHAR)
```

Copy

### Parameters[¶](#id263 "Link to this heading")

`QUERYBAND` is a VARCHAR data type that stores query band information.

The query band combines transaction, session, and profile query bands into a single string.

`SEARCHTYPE` is a floating-point number data type.

The maximum depth at which matching pairs will be searched.

0 represents a wildcard value that matches any input.

A transaction represents a single unit of work in a database.

A Session object represents a connection to Snowflake.

3 = Create a profile.

`SEARCHNAME` VARCHAR

The name to search for within the key-value pairs.

### Returns[¶](#id264 "Link to this heading")

Returns the value of the ‘name’ key at the specified level in the hierarchy. If no value is found, returns null.

### Usage example[¶](#id265 "Link to this heading")

Input:

```
SELECT GETQUERYBANDVALUE_UDF('=T> account=Matt;user=Matt200; =S> account=SaraDB;user=Sara;role=DbAdmin;', 0, 'account');
SELECT GETQUERYBANDVALUE_UDF('=T> account=Matt;user=Matt200; =S> account=SaraDB;user=Sara;role=DbAdmin;', 2, 'account');
SELECT GETQUERYBANDVALUE_UDF('=T> account=Matt;user=Matt200; =S> account=SaraDB;user=Sara;role=DbAdmin;', 0, 'role');
SELECT GETQUERYBANDVALUE_UDF('=T> account=Matt;user=Matt200; =S> account=SaraDB;user=Sara;role=DbAdmin;', 1, 'role');
```

Copy

Output:

```
      Matt
      SaraDB
      DbAdmin
      NULL
```

Copy

### Migration example[¶](#id266 "Link to this heading")

Input:

```
SELECT GETQUERYBANDVALUE('=T> account=Matt;user=Matt200; =S> account=SaraDB;user=Sara;role=DbAdmin;', 0, 'account')
```

Copy

Output:

```
WITH
--** MSC-WARNING - MSCEWI2078 - THE EXPAND ON CLAUSE FUNCTIONALITY IS TRANSFORMED INTO A CTE BLOCK **
ExpandOnCTE AS
(
SELECT
PUBLIC.EXPAND_ON_UDF('ANCHOR_SECOND', VALUE, duration) bg
FROM
project,
TABLE(FLATTEN(PUBLIC.ROW_COUNT_UDF(PUBLIC.DIFF_TIME_PERIOD_UDF('ANCHOR_SECOND', duration))))
)
SELECT NORMALIZE emp_id,
duration
FROM
project,
ExpandOnCTE;
```

Copy

## JULIAN\_DAY\_UDF[¶](#julian-day-udf "Link to this heading")

### Definition[¶](#id267 "Link to this heading")

Calculates the Julian day number, which represents the continuous count of days since January 1, 4713 BCE (Before Common Era). The Julian day is used in astronomy and calendar calculations.

```
PUBLIC.JULIAN_DAY_UDF(INPUT TIMESTAMP_TZ)
```

Copy

### Parameters[¶](#id268 "Link to this heading")

`INPUT` TIMESTAMP\_TZ

The date that will be converted to a Julian day number.

### Returns[¶](#id269 "Link to this heading")

A `varchar` value representing the calculated Julian date.

### Usage example[¶](#id270 "Link to this heading")

Input:

```
SELECT PUBLIC.JULIAN_DAY_UDF(DATE '2021-10-26');
```

Copy

Output:

```
'2459514'
```

Copy

## WEEKNUMBER\_OF\_MONTH\_UDF[¶](#weeknumber-of-month-udf "Link to this heading")

### Definition[¶](#id271 "Link to this heading")

Identify the month from a given date.

```
PUBLIC.WEEKNUMBER_OF_MONTH_UDF(INPUT TIMESTAMP_TZ)
```

Copy

### Parameters[¶](#id272 "Link to this heading")

`INPUT` TIMESTAMP\_TZ

The date from which to calculate the month number.

### Returns[¶](#id273 "Link to this heading")

A numeric value representing the month (1-12) of a given date.

### Usage example[¶](#id274 "Link to this heading")

Input:

```
SELECT PUBLIC.WEEKNUMBER_OF_MONTH_UDF(DATE '2022-05-21')
```

Copy

Output:

```
3
```

Copy

## JSON\_EXTRACT\_UDF[¶](#json-extract-udf "Link to this heading")

### Definition[¶](#id275 "Link to this heading")

A user-defined function (UDF) that mimics the behavior of `JSONExtract`, `JSONExtractValue`, and `JSONExtractLargeValue` functions. This UDF allows you to extract multiple values from a JSON object.

```
JSON_EXTRACT_UDF(JSON_OBJECT VARIANT, JSON_PATH STRING, SINGLE_VALUE BOOLEAN)
```

Copy

### Parameters[¶](#id276 "Link to this heading")

`JSON_OBJECT` is a data type that stores JSON-formatted data in a structured format.

The JSON object containing the values you want to extract.

`JSON_PATH` A string that specifies the path to extract data from a JSON document

The location within the JSON\_OBJECT where the desired values can be found, specified using JSON path notation.

`SINGLE_VALUE` A boolean flag that indicates whether to return a single value or multiple values.

BOOLEAN parameter: When set to true, returns a single value (required for JSONExtractValue and JSONExtractLargeValue functions). When set to false, returns an array of values (used with JSONExtract).

### Returns[¶](#id277 "Link to this heading")

The data values found at the specified JSON path within the JSON object.

### Migration example[¶](#id278 "Link to this heading")

Input:

```
SELECT
    Store.JSONExtract('$..author') as AllAuthors
FROM BookStores;
```

Copy

Output:

```
SELECT
    JSON_EXTRACT_UDF(Store, '$..author', FALSE) as AllAuthors
    FROM
    BookStores;
```

Copy

## COMPUTE\_EXPAND\_ON\_UDF[¶](#compute-expand-on-udf "Link to this heading")

### Definition[¶](#id279 "Link to this heading")

Determines how to expand data based on the specified time period type.

```
PUBLIC.COMPUTE_EXPAND_ON_UDF(TIME STRING, SEQ NUMBER, PERIOD TIMESTAMP, PERIODTYPE STRING)
```

Copy

### Parameters[¶](#id280 "Link to this heading")

`TIME` STRING

The timestamp used in the anchor.

`SEQ` sequence number

The order in which each row’s calculations are performed.

`PERIOD` represents a timestamp value that indicates a specific point in time.

The date for the specified time period.

`PERIODTYPE` is a string value that defines the type of time period.

The time period used for the calculation (either ‘`BEGIN`’ or ‘`END`’)

### Returns[¶](#id281 "Link to this heading")

A timestamp indicating when each row in the EXPAND-ON operation was processed.

### Example[¶](#id282 "Link to this heading")

Warning

This UDF is a derived function that extends the functionality of [EXPAND\_ON\_UDF](#).

## WEEK\_NUMBER\_OF\_QUARTER\_UDF[¶](#week-number-of-quarter-udf "Link to this heading")

### Definition[¶](#id283 "Link to this heading")

Returns the week number within the current quarter for a specified date. This function follows the same behavior as Teradata’s `WEEKNUMBER_OF_QUARTER(DATE, 'ISO')` function, using the ISO calendar system.

```
PUBLIC.WEEK_NUMBER_OF_QUARTER_UDF(INPUT TIMESTAMP_TZ)
```

Copy

### Parameters[¶](#id284 "Link to this heading")

`INPUT` TIMESTAMP\_TZ

The date used to calculate which week of the quarter it falls into.

### Returns[¶](#id285 "Link to this heading")

An integer indicating which week of the quarter (1-13) is being referenced.

### Usage example[¶](#id286 "Link to this heading")

Input:

```
SELECT WEEK_NUMBER_OF_QUARTER_UDF(DATE '2023-01-01'),
WEEK_NUMBER_OF_QUARTER_UDF(DATE '2022-10-27')
```

Copy

Output:

```
1, 4
```

Copy

## YEAR\_END\_ISO\_UDF[¶](#year-end-iso-udf "Link to this heading")

### Definition[¶](#id287 "Link to this heading")

User-defined function (UDF) that calculates the last day of the year for a given date using ISO calendar standards, similar to Teradata’s TD\_YEAR\_END function.

```
PUBLIC.YEAR_END_ISO_UDF(INPUT date)
```

Copy

### Parameters[¶](#id288 "Link to this heading")

`INPUT` DATE

The date that represents the last day of the year according to the ISO calendar standard.

### Returns[¶](#id289 "Link to this heading")

The last day of the year according to the ISO calendar system.

### Usage example[¶](#id290 "Link to this heading")

Input:

```
SELECT  PUBLIC.YEAR_END_ISO_UDF(DATE '2022-01-01'),
PUBLIC.YEAR_END_ISO_UDF(DATE '2022-04-12');
```

Copy

Output:

```
2022-01-02, 2023-01-01
```

Copy

## INSERT\_CURRENCY\_UDF[¶](#insert-currency-udf "Link to this heading")

### Definition[¶](#id291 "Link to this heading")

Insert the currency symbol directly before the first digit of the number to ensure there are no spaces or symbols between the currency symbol and the number.

```
PUBLIC.INSERT_CURRENCY_UDF(INPUT VARCHAR, CURRENCYINDEX INTEGER, CURRENCYVALUE VARCHAR)
```

Copy

### Parameters[¶](#id292 "Link to this heading")

`INPUT` VARCHAR

The output of TO\_CHAR when converting a numeric value that requires currency formatting.

`CURRENCYINDEX` is an integer value that represents the index of a currency.

The position in the array where the currency should be inserted.

`CURRENCYVALUE` A VARCHAR field that stores currency values

The text that will be used as the currency value.

### Returns[¶](#id293 "Link to this heading")

A `varchar` field containing the currency text at a defined position.

### Usage example[¶](#id294 "Link to this heading")

Input:

```
SELECT PUBLIC.INSERT_CURRENCY_UDF(to_char(823, 'S999999'), '1', 'CRC');
```

Copy

Output:

```
'+CRC823'
```

Copy

## INSTR\_UDF (STRING, STRING, INT)[¶](#instr-udf-string-string-int "Link to this heading")

Warning

This user-defined function (UDF) accepts three parameters.

### Definition[¶](#id295 "Link to this heading")

Finds all instances where search\_string appears within source\_string.

```
PUBLIC.INSTR_UDF(SOURCE_STRING STRING, SEARCH_STRING STRING, POSITION INT)
```

Copy

### Parameters[¶](#id296 "Link to this heading")

`SOURCE_STRING` represents a string value that will be used as input

The text that will be searched.

`SEARCH_STRING` is a text value that you want to search for.

The text pattern that the function will look for and match.

`POSITION` is an integer data type that represents a position in a sequence.

The position in the text where the search begins (starting from position 1).

### Returns[¶](#id297 "Link to this heading")

The location within the original string where the match is found.

### Usage example[¶](#id298 "Link to this heading")

Input:

```
SELECT INSTR_UDF('FUNCTION','N', 3);
```

Copy

Output:

```
8
```

Copy

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

1. [QUARTERNUMBER\_OF\_YEAR\_UDF](#quarternumber-of-year-udf)
2. [DAYNUMBER\_OF\_YEAR\_UDF](#daynumber-of-year-udf)
3. [SUBSTR\_UDF (STRING, FLOAT)](#substr-udf-string-float)
4. [CHKNUM\_UDF](#chknum-udf)
5. [TD\_YEAR\_END\_UDF](#td-year-end-udf)
6. [PERIOD\_OVERLAPS\_UDF](#period-overlaps-udf)
7. [WEEK\_NUMBER\_OF\_QUARTER\_COMPATIBLE\_UDF](#week-number-of-quarter-compatible-udf)
8. [ROMAN\_NUMERALS\_MONTH\_UDF](#roman-numerals-month-udf)
9. [TD\_YEAR\_BEGIN\_UDF](#td-year-begin-udf)
10. [FULL\_MONTH\_NAME\_UDF](#full-month-name-udf)
11. [TO\_BYTES\_HEX\_UDF](#to-bytes-hex-udf)
12. [PERIOD\_INTERSECT\_UDF](#period-intersect-udf)
13. [INTERVAL\_TO\_SECONDS\_UDF](#interval-to-seconds-udf)
14. [TIMESTAMP\_ADD\_UDF](#timestamp-add-udf)
15. [INTERVAL\_MULTIPLY\_UDF](#interval-multiply-udf)
16. [TD\_DAY\_OF\_WEEK\_UDF](#td-day-of-week-udf)
17. [ISO\_YEAR\_PART\_UDF](#iso-year-part-udf)
18. [DIFF\_TIME\_PERIOD\_UDF](#diff-time-period-udf)
19. [WEEK\_NUMBER\_OF\_QUARTER\_ISO\_UDF](#week-number-of-quarter-iso-udf)
20. [NVP\_UDF](#nvp-udf)
21. [MONTH\_SHORT\_UDF](#month-short-udf)
22. [DATE\_TO\_INT\_UDF](#date-to-int-udf)
23. [PERIOD\_UDF](#period-udf)
24. [DAYNAME\_LONG\_UDF (TIMESTAMP\_TZ, VARCHAR)](#dayname-long-udf-timestamp-tz-varchar)
25. [TD\_DAY\_OF\_WEEK\_COMPATIBLE\_UDF](#td-day-of-week-compatible-udf)
26. [JAROWINKLER\_UDF](#jarowinkler-udf)
27. [YEAR\_BEGIN\_ISO\_UDF](#year-begin-iso-udf)
28. [YEAR\_PART\_UDF](#year-part-udf)
29. [YEAR\_WITH\_COMMA\_UDF](#year-with-comma-udf)
30. [MONTHS\_BETWEEN\_UDF](#months-between-udf)
31. [SECONDS\_PAST\_MIDNIGHT\_UDF](#seconds-past-midnight-udf)
32. [CHAR2HEXINT\_UDF](#char2hexint-udf)
33. [INTERVAL\_ADD\_UDF](#interval-add-udf)
34. [DAY\_OF\_WEEK\_LONG\_UDF](#day-of-week-long-udf)
35. [TD\_WEEK\_OF\_CALENDAR\_UDF](#td-week-of-calendar-udf)
36. [WRAP\_NEGATIVE\_WITH\_ANGLE\_BRACKETS\_UDF](#wrap-negative-with-angle-brackets-udf)
37. [INSTR\_UDF (STRING, STRING)](#instr-udf-string-string)
38. [TRANSLATE\_CHK\_UDF](#translate-chk-udf)
39. [EXPAND\_ON\_UDF](#expand-on-udf)
40. [ROW\_COUNT\_UDF](#row-count-udf)
41. [CENTURY\_UDF](#century-udf)
42. [TIME\_DIFFERENCE\_UDF](#time-difference-udf)
43. [INTERVAL\_DIVIDE\_UDF](#interval-divide-udf)
44. [DAYNUMBER\_OF\_MONTH\_UDF](#daynumber-of-month-udf)
45. [LAST\_DAY\_DECEMBER\_OF\_ISO\_UDF](#last-day-december-of-iso-udf)
46. [DATEADD\_UDF](#dateadd-udf)
47. [JULIAN\_TO\_DATE\_UDF](#julian-to-date-udf)
48. [FIRST\_DAY\_JANUARY\_OF\_ISO\_UDF](#first-day-january-of-iso-udf)
49. [TIMESTAMP\_DIFFERENCE\_UDF](#timestamp-difference-udf)
50. [FIRST\_DAY\_OF\_MONTH\_ISO\_UDF](#first-day-of-month-iso-udf)
51. [INT\_TO\_DATE\_UDF](#int-to-date-udf)
52. [NULLIFZERO\_UDF](#nullifzero-udf)
53. [DATE\_LONG\_UDF](#date-long-udf)
54. [TD\_MONTH\_OF\_CALENDAR\_UDF](#td-month-of-calendar-udf)
55. [MONTH\_NAME\_LONG\_UDF](#month-name-long-udf)
56. [TD\_DAY\_OF\_CALENDAR\_UDF](#td-day-of-calendar-udf)
57. [PERIOD\_TO\_TIME\_UDF](#period-to-time-udf)
58. [INSTR\_UDF (STRING, STRING, DOUBLE, DOUBLE)](#instr-udf-string-string-double-double)
59. [ROUND\_DATE\_UDF](#round-date-udf)
60. [SUBSTR\_UDF (STRING, FLOAT, FLOAT)](#substr-udf-string-float-float)
61. [GETQUERYBANDVALUE\_UDF (VARCHAR)](#getquerybandvalue-udf-varchar)
62. [TD\_WEEK\_OF\_YEAR\_UDF](#td-week-of-year-udf)
63. [EXTRACT\_TIMESTAMP\_DIFFERENCE\_UDF](#extract-timestamp-difference-udf)
64. [JSON\_EXTRACT\_DOT\_NOTATION\_UDF](#json-extract-dot-notation-udf)
65. [WEEK\_OF\_MONTH\_UDF](#week-of-month-udf)
66. [DAYNAME\_LONG\_UDF (TIMESTAMP\_TZ)](#dayname-long-udf-timestamp-tz)
67. [INTERVAL\_TO\_MONTHS\_UDF](#interval-to-months-udf)
68. [GETQUERYBANDVALUE\_UDF (VARCHAR, FLOAT, VARCHAR)](#getquerybandvalue-udf-varchar-float-varchar)
69. [JULIAN\_DAY\_UDF](#julian-day-udf)
70. [WEEKNUMBER\_OF\_MONTH\_UDF](#weeknumber-of-month-udf)
71. [JSON\_EXTRACT\_UDF](#json-extract-udf)
72. [COMPUTE\_EXPAND\_ON\_UDF](#compute-expand-on-udf)
73. [WEEK\_NUMBER\_OF\_QUARTER\_UDF](#week-number-of-quarter-udf)
74. [YEAR\_END\_ISO\_UDF](#year-end-iso-udf)
75. [INSERT\_CURRENCY\_UDF](#insert-currency-udf)
76. [INSTR\_UDF (STRING, STRING, INT)](#instr-udf-string-string-int)