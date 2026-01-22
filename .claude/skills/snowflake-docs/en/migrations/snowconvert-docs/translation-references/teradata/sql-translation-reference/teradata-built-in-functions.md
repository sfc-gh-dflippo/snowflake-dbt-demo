---
auto_generated: true
description: This page provides a description of the translation for the built-in
  functions in Teradata to Snowflake
last_scraped: '2026-01-14T16:53:53.632105+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/teradata/sql-translation-reference/teradata-built-in-functions
title: SnowConvert AI - Teradata - Built-in Functions | Snowflake Documentation
---

1. [Overview](../../../../../guides/README.md)
2. [Snowflake Horizon Catalog](../../../../../user-guide/snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../../../../../guides/overview-connecting.md)
6. [Virtual warehouses](../../../../../user-guide/warehouses.md)
7. [Databases, Tables, & Views](../../../../../guides/overview-db.md)
8. [Data types](../../../../../data-types.md)
10. Data Integration

    - [Snowflake Openflow](../../../../../user-guide/data-integration/openflow/about.md)
    - Apache Iceberg™

      - [Apache Iceberg™ Tables](../../../../../user-guide/tables-iceberg.md)
      - [Snowflake Open Catalog](../../../../../user-guide/opencatalog/overview.md)
11. Data engineering

    - [Data loading](../../../../../guides/overview-loading-data.md)
    - [Dynamic Tables](../../../../../user-guide/dynamic-tables-about.md)
    - [Streams and Tasks](../../../../../user-guide/data-pipelines-intro.md)
    - [dbt Projects on Snowflake](../../../../../user-guide/data-engineering/dbt-projects-on-snowflake.md)
    - [Data Unloading](../../../../../guides/overview-unloading-data.md)
12. [Storage Lifecycle Policies](../../../../../user-guide/storage-management/storage-lifecycle-policies.md)
13. [Migrations](../../../../README.md)

    * Tools

      * [SnowConvert AI](../../../overview.md)

        + General

          + [About](../../../general/about.md)
          + [Getting Started](../../../general/getting-started/README.md)
          + [Terms And Conditions](../../../general/terms-and-conditions/README.md)
          + [Release Notes](../../../general/release-notes/release-notes/README.md)
          + User Guide

            + [SnowConvert AI](../../../general/user-guide/snowconvert/README.md)
            + [Project Creation](../../../general/user-guide/project-creation.md)
            + [Extraction](../../../general/user-guide/extraction.md)
            + [Deployment](../../../general/user-guide/deployment.md)
            + [Data Migration](../../../general/user-guide/data-migration.md)
            + [Data Validation](../../../general/user-guide/data-validation.md)
            + [Power BI Repointing](../../../general/user-guide/power-bi-repointing-general.md)
            + [ETL Migration](../../../general/user-guide/etl-migration-replatform.md)
          + [Technical Documentation](../../../general/technical-documentation/README.md)
          + [Contact Us](../../../general/contact-us.md)
          + Others

            + [Using SnowConvert AI In A Ubuntu Docker Image](../../../general/others/using-snowconvert-in-a-ubuntu-docker-image.md)
          + [Frequently Asked Questions (FAQ)](../../../general/frequently-asked-questions-faq.md)")
        + Translation References

          + [General](../../general/README.md)
          + [Teradata](../README.md)

            - [Data Migration Considerations](../data-migration-considerations.md)
            - [Session Modes in Teradata](../session-modes.md)
            - [Sql Translation Reference](README.md)

              * [Built-in Functions](teradata-built-in-functions.md)
              * [Data Types](data-types.md)
              * [Database DBC](database-dbc.md)
              * [DDL Statements](ddl-teradata.md)
              * [DML Statements](dml-teradata.md)
              * [Analytic](analytic.md)
              * [Iceberg Table Transformations](Iceberg-tables-transformations.md)
            - [SQL to JavaScript (Procedures)](../teradata-to-javascript-translation-reference.md)")
            - [SQL to Snowflake Scripting (Procedures)](../teradata-to-snowflake-scripting-translation-reference.md)")
            - [Scripts To Python](../scripts-to-python/README.md)
            - [Scripts to Snowflake SQL](../scripts-to-snowflake-sql-translation-reference/README.md)
            - ETL And BI Repointing

              - [Power BI Teradata Repointing](../etl-bi-repointing/power-bi-teradata-repointing.md)
          + [Oracle](../../oracle/README.md)
          + [SQL Server-Azure Synapse](../../transact/README.md)
          + [Sybase IQ](../../sybase/README.md)
          + [Hive-Spark-Databricks SQL](../../hive/README.md)
          + [Redshift](../../redshift/README.md)
          + [PostgreSQL-Greenplum-Netezza](../../postgres/README.md)
          + [BigQuery](../../bigquery/README.md)
          + [Vertica](../../vertica/README.md)
          + [IBM DB2](../../db2/README.md)
          + [SSIS](../../ssis/README.md)
        + [Migration Assistant](../../../migration-assistant/README.md)
        + [Data Validation CLI](../../../data-validation-cli/index.md)
        + [AI Verification](../../../snowconvert-ai-verification.md)
      * [Snowpark Migration Accelerator](../../../../sma-docs/README.md)
    * Guides

      * [Teradata](../../../../guides/teradata.md)
      * [Databricks](../../../../guides/databricks.md)
      * [SQL Server](../../../../guides/sqlserver.md)
      * [Amazon Redshift](../../../../guides/redshift.md)
      * [Oracle](../../../../guides/oracle.md)
      * [Azure Synapse](../../../../guides/azuresynapse.md)
15. [Queries](../../../../../guides/overview-queries.md)
16. [Listings](../../../../../collaboration/collaboration-listings-about.md)
17. [Collaboration](../../../../../guides/overview-sharing.md)
19. [Snowflake AI & ML](../../../../../guides/overview-ai-features.md)
21. [Snowflake Postgres](../../../../../user-guide/snowflake-postgres/about.md)
23. [Alerts & Notifications](../../../../../guides/overview-alerts.md)
25. [Security](../../../../../guides/overview-secure.md)
26. [Data Governance](../../../../../guides/overview-govern.md)
27. [Privacy](../../../../../guides/overview-privacy.md)
29. [Organizations & Accounts](../../../../../guides/overview-manage.md)
30. [Business continuity & data recovery](../../../../../user-guide/replication-intro.md)
32. [Performance optimization](../../../../../guides/overview-performance.md)
33. [Cost & Billing](../../../../../guides/overview-cost.md)

[Guides](../../../../../guides/README.md)[Migrations](../../../../README.md)Tools[SnowConvert AI](../../../overview.md)Translation References[Teradata](../README.md)[Sql Translation Reference](README.md)Built-in Functions

# SnowConvert AI - Teradata - Built-in Functions[¶](#snowconvert-ai-teradata-built-in-functions "Link to this heading")

This page provides a description of the translation for the built-in functions in Teradata to Snowflake

Note

This page only lists the functions that are already transformed by SnowConvert AI, if a function from the Teradata documentation is not listed there then it should be taken as unsupported.

For more information about built-in functions and their Snowflake equivalents, also see [Common built-in functions](../../general/built-in-functions).

Note

Some Teradata functions do not have a direct equivalent in Snowflake so they are transformed into a functional equivalent UDF, these can be easily spotted by the \_UDF postfix in the name of the function. For more information on the UDFs SnowConvert AI uses check this [git repository](https://github.com/MobilizeNet/SnowConvert_Support_Library/tree/main/UDFs).

## Aggregate Functions[¶](#aggregate-functions "Link to this heading")

| Teradata | Snowflake | Note |
| --- | --- | --- |
| AVG | AVG |  |
| CORR | CORR |  |
| COUNT | COUNT |  |
| COVAR\_POP | COVAR\_POP |  |
| COVAR\_SAMP | COVAR\_SAMP |  |
| GROUPING | GROUPING |  |
| KURTOSIS | KURTOSIS |  |
| MAXIMUM  MAX | MAX |  |
| MINIMUM  MIN | MIN |  |
| PIVOT | PIVOT | Check [PIVOT.](#pivot) |
| REGR\_AVGX | REGR\_AVGX |  |
| REGR\_AVGY | REGR\_AVGY |  |
| REGR\_COUNT | REGR\_COUNT |  |
| REGR\_INTERCEPT | REGR\_INTERCEPT |  |
| REGR\_R2 | REGR\_R2 |  |
| REGR\_SLOPE | REGR\_SLOPE |  |
| REGR\_SXX | REGR\_SXX |  |
| REGR\_SXY | REGR\_SXY |  |
| REGR\_SYY | REGR\_SYY |  |
| SKEW | SKEW |  |
| STDDEV\_POP | STDDEV\_POP |  |
| STDDEV\_SAMP | STDDEV\_SAMP |  |
| SUM | SUM |  |
| UNPIVOT | UNPIVOT | Unpivot with multiple functions not supported in Snowflake |
| VAR\_POP | VAR\_POP |  |
| VAR\_SAMP | VAR\_SAMP |  |

> See [Aggregate functions​](https://docs.teradata.com/r/Teradata-VantageTM-SQL-Functions-Expressions-and-Predicates-17.20/Aggregate-Functions)

## Arithmetic, Trigonometric, Hyperbolic Operators/Functions[¶](#arithmetic-trigonometric-hyperbolic-operators-functions "Link to this heading")

| Teradata | Snowflake | Note |
| --- | --- | --- |
| ABS | ABS |  |
| CEILING | CEIL |  |
| DEGREES | DEGREES |  |
| EXP | EXP |  |
| FLOOR | FLOOR |  |
| ***HYPERBOLIC***  ACOSH  ASINH  ATANH  COSH  SINH  TANH | ***HYPERBOLIC***  ACOSH  ASINH  ATANH  COSH  SINH  TANH |  |
| LOG | LOG |  |
| LN | LN |  |
| MOD | MOD |  |
| NULLIFZERO(param) | CASE WHEN param=0 THEN null ELSE param END |  |
| POWER | POWER |  |
| RANDOM | RANDOM |  |
| RADIANS | RADIANS |  |
| ROUND | ROUND |  |
| SIGN | SIGN |  |
| SQRT | SQRT |  |
| TRUNC | TRUNC\_UDF |  |
| ***TRIGONOMETRIC***  ACOS  ASIN  ATAN  ATAN2  COS  SIN  TAN | ***TRIGONOMETRIC***  ACOS  ASIN  ATAN  ATAN2  COS  SIN  TAN |  |
| ZEROIFNULL | ZEROIFNULL |  |

> See [Arithmetic, Trigonometric, Hyperbolic Operators/Functions](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/Teradata-VantageTM-SQL-Functions-Expressions-and-Predicates-17.20/Arithmetic-Trigonometric-Hyperbolic-Operators/Functions)​

## Attribute Functions[¶](#attribute-functions "Link to this heading")

| Teradata | Snowflake | Note |
| --- | --- | --- |
| BIT\_LENGTH | BIT\_LENGTH |  |
| BYTE  BYTES | LENGTH |  |
| CHAR  CHARS  CHARACTERS | LEN |  |
| CHAR\_LENGTH  CHARACTER\_LENGTH | LEN |  |
| MCHARACTERS | LENGTH |  |
| OCTECT\_LENGTH | OCTECT\_LENGTH |  |

> See [Attribute functions](https://docs.teradata.com/r/Teradata-VantageTM-SQL-Functions-Expressions-and-Predicates-17.20/Attribute-Functions)

## Bit/Byte Manipulation Functions[¶](#bit-byte-manipulation-functions "Link to this heading")

| Teradata | Snowflake | Note |
| --- | --- | --- |
| BITAND | BITAND |  |
| BITNOT | BITNOT |  |
| BITOR | BITOR |  |
| BITXOR | BITXOR |  |
| GETBIT | GETBIT |  |

> See [Bit/Byte functions](https://docs.teradata.com/r/Teradata-VantageTM-SQL-Functions-Expressions-and-Predicates-17.20/Bit/Byte-Manipulation-Functions)

## Built-In (System Functions)[¶](#built-in-system-functions "Link to this heading")

| Teradata | Snowflake | Note |
| --- | --- | --- |
| ACCOUNT | CURRENT\_ACCOUNT |  |
| CURRENT\_DATE  CURDATE | CURRENT\_DATE |  |
| CURRENT\_ROLE | CURRENT\_ROLE |  |
| CURRENT\_TIME CURTIME | CURRENT\_TIME |  |
| CURRENT\_TIMESTAMP | CURRENT\_TIMESTAMP |  |
| DATABASE | CURRENT\_DATABASE |  |
| DATE | CURRENT\_DATE |  |
| NOW | CURRENT\_TIMESTAMP |  |
| PROFILE | CURRENT\_ROLE | Check [SSC-EWI-TD0068](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/teradataEWI.html#ssc-ewi-td0068) for more details on this transformation |
| SESSION | CURRENT\_SESSION |  |
| TIME | CURRENT\_TIME |  |
| USER | CURRENT\_USER |  |

> See [Built-In Functions](https://docs.teradata.com/r/Teradata-VantageTM-SQL-Functions-Expressions-and-Predicates-17.20/Built-In-Functions)

## Business Calendars[¶](#business-calendars "Link to this heading")

| Teradata | Snowflake | Note |
| --- | --- | --- |
| DAYNUMBER\_OF\_MONTH(DatetimeValue, ‘COMPATIBLE’) | DAYOFMONTH |  |
| DAYNUMBER\_OF\_MONTH(DatetimeValue, ‘ISO’) | DAYNUMBER\_OF\_MONTH\_ISO\_UDF |  |
| DAYNUMBER\_OF\_MONTH(DatetimeValue, ‘TERADATA’) | DAYOFMONTH |  |
| DAYNUMBER\_OF\_WEEK(DatetimeValue, ‘ISO’) | DAYOFWEEKISO |  |
| DAYNUMBER\_OF\_WEEK(DatetimeValue, ‘COMPATIBLE’) | DAY\_OF\_WEEK\_COMPATIBLE\_UDF |  |
| DAYNUMBER\_OF\_WEEK(DatetimeValue, ‘TERADATA’) DAYNUMBER\_OF\_WEEK(DatetimeValue) | TD\_DAY\_OF\_WEEK\_UDF |  |
| DAYNUMBER\_OF\_YEAR(DatetimeValue, ‘ISO’) | PUBLIC.DAY\_OF\_YEAR\_ISO\_UDF |  |
| DAYNUMBER\_OF\_YEAR(DatetimeValue) | DAYOFYEAR |  |
| QUARTERNUMBER\_OF\_YEAR | QUARTER |  |
| TD\_SUNDAY(DateTimeValue) | PREVIOUS\_DAY(DateTimeValue, ‘Sunday’) |  |
| WEEKNUMBER\_OF\_MONTH | WEEKNUMBER\_OF\_MONTH\_UDF |  |
| WEEKNUMBER\_OF\_QUARTER(dateTimeValue) | WEEKNUMBER\_OF\_QUARTER\_UDF |  |
| WEEKNUMBER\_OF\_QUARTER(dateTimeValue, ‘ISO’) | WEEKNUMBER\_OF\_QUARTER\_ISO\_UDF |  |
| WEEKNUMBER\_OF\_QUARTER(dateTimeValue, ‘COMPATIBLE’) | WEEKNUMBER\_OF\_QUARTER\_COMPATIBLE\_UDF |  |
| WEEKNUMBER\_OF\_YEAR(DateTimeValue, ‘ISO’) | WEEKISO |  |
| YEARNUMBER\_OF\_CALENDAR(DATETIMEVALUE, ‘COMPATIBLE’) | YEAR |  |
| YEARNUMBER\_OF\_CALENDAR(DATETIMEVALUE, ‘ISO’) | YEAROFWEEKISO |  |

> See [Business Calendars](https://docs.teradata.com/r/Teradata-VantageTM-SQL-Date-and-Time-Functions-and-Expressions-17.20/Business-Calendars)

## Calendar Functions[¶](#calendar-functions "Link to this heading")

| Teradata | Snowflake | Note |
| --- | --- | --- |
| DAYNUMBER\_OF\_WEEK(DatetimeValue) | TD\_DAY\_OF\_WEEK\_UDF |  |
| DAYNUMBER\_OF\_WEEK(DatetimeValue, ‘COMPATIBLE’) | DAY\_OF\_WEEK\_COMPATIBLE\_UDF |  |
| QuarterNumber\_Of\_Year(DatetimeValue, ‘ISO’) | QUARTER\_OF\_YEAR\_ISO\_UDF(DatetimeValue) |  |
| TD\_DAY\_OF\_CALENDAR | TD\_DAY\_OF\_CALENDAR\_UDF |  |
| TD\_DAY\_OF\_MONTH DAYOFMONTH | DAYOFMONTH |  |
| TD\_DAY\_OF\_WEEK DAYOFWEEK | TD\_DAY\_OF\_WEEK\_UDF |  |
| TD\_DAY\_OF\_YEAR | DAYOFYEAR |  |
| TD\_MONTH\_OF\_CALENDAR(DateTimeValue) MONTH\_CALENDAR(DateTimeValue) | TD\_MONTH\_OF\_CALENDAR\_UDF(DateTimeValue) |  |
| TD\_WEEK\_OF\_CALENDAR(DateTimeValue) WEEK\_OF\_CALENDAR(DateTimeValue) | TD\_WEEK\_OF\_CALENDAR\_UDF(DateTimeValue) |  |
| TD\_WEEK\_OF\_YEAR | WEEK\_OF\_YEAR\_UDF |  |
| TD\_YEAR\_BEGIN(DateTimeValue) | YEAR\_BEGIN\_UDF(DateTimeValue) |  |
| TD\_YEAR\_BEGIN(DateTimeValue, ‘ISO’) | YEAR\_BEGIN\_ISO\_UDF(DateTimeValue) |  |
| TD\_YEAR\_END(DateTimeValue) | YEAR\_END\_UDF(DateTimeValue) |  |
| TD\_YEAR\_END(DateTimeValue, ‘ISO’) | YEAR\_END\_ISO\_UDF(DateTimeValue) |  |
| WEEKNUMBER\_OF\_MONTH(DateTimeValue) | WEEKNUMBER\_OF\_MONTH\_UDF(DateTimeValue) |  |
| WEEKNUMBER\_OF\_QUARTER(DateTimeValue) | WEEKNUMBER\_OF\_QUARTER\_UDF(DateTimeValue) |  |
| WEEKNUMBER\_OF\_QUARTER(DateTimeValue, ‘ISO’) | WEEKNUMBER\_OF\_QUARTER\_ISO\_UDF(DateTimeValue) |  |
| WEEKNUMBER\_OF\_QUARTER(DateTimeValue, ‘COMPATIBLE’) | WEEKNUMBER\_OF\_QUARTER\_COMPATIBLE\_UDF(DateTimeValue) |  |
| WEEKNUMBER\_OF\_YEAR(DateTimeValue) | WEEK\_OF\_YEAR\_UDF(DateTimeValue) |  |
| WEEKNUMBER\_OF\_YEAR(DateTimeValue, ‘COMPATIBLE’) | WEEK\_OF\_YEAR\_COMPATIBLE\_UDF(DateTimeValue) |  |

> See [Calendar Functions](https://docs.teradata.com/r/WX0vkeB8F3JQXZ0HTR~d0Q/~8TzAjUr3AFwohWtu8ndxQ)

## Case Functions[¶](#case-functions "Link to this heading")

| Teradata | Snowflake | Note |
| --- | --- | --- |
| COALESCE | COALESCE | Check [Coalesce](#coalesce). |
| NULLIF | NULLIF |  |

> See [case functions](https://docs.teradata.com/r/Teradata-VantageTM-SQL-Functions-Expressions-and-Predicates-17.20/CASE-Expressions)

## Comparison Functions[¶](#comparison-functions "Link to this heading")

| Teradata | Snowflake | Note |
| --- | --- | --- |
| DECODE | DECODE |  |
| GREATEST | GREATEST |  |
| LEAST | LEAST |  |

> See [comparison functions](https://docs.teradata.com/r/Teradata-VantageTM-SQL-Functions-Expressions-and-Predicates-17.20/Comparison-Operators-and-Functions)

## Data type conversions[¶](#data-type-conversions "Link to this heading")

| Teradata | Snowflake | Note |
| --- | --- | --- |
| CAST | CAST |  |
| CAST(DatetimeValue AS INT) | DATE\_TO\_INT\_UDF |  |
| CAST (VarcharValue AS INTERVAL) | INTERVAL\_UDF | Check [Cast to INTERVAL datatype](#cast-to-interval-datatype) |
| TRYCAST | TRY\_CAST |  |
| FROM\_BYTES | TO\_NUMBER TO\_BINARY | [FROM\_BYTES](#from-bytes) with ASCII parameter not supported in Snowflake. |

> See [Data Type Conversions](https://docs.teradata.com/reader/~_sY_PYVxZzTnqKq45UXkQ/iZ57TG_CtznEu1JdSbFNsQ)

## Data Type Conversion Functions[¶](#data-type-conversion-functions "Link to this heading")

| Teradata | Snowflake | Note |
| --- | --- | --- |
| TO\_BYTES(Input, ‘Base10’) | INT2HEX\_UDF(Input) |  |
| TO\_NUMBER | TO\_NUMBER |  |
| TO\_CHAR | TO\_CHAR or equivalent expression | Check [TO\_CHAR](#to-char). |
| TO\_DATE | TO\_DATE |  |
| TO\_DATE(input, ‘YYYYDDD’) | JULIAN\_TO\_DATE\_UDF |  |

> See [Data Type Conversion Functions](https://docs.teradata.com/r/Teradata-VantageTM-Data-Types-and-Literals/March-2019/Data-Type-Conversion-Functions)

## DateTime and Interval functions[¶](#datetime-and-interval-functions "Link to this heading")

| Teradata | Snowflake | Note |
| --- | --- | --- |
| ADD\_MONTHS | ADD\_MONTHS |  |
| EXTRACT | EXTRACT |  |
| LAST\_DAY | LAST\_DAY |  |
| MONTH | MONTH |  |
| MONTHS\_BETWEEN | MONTHS\_BETWEEN\_UDF |  |
| NEXT\_DAY | NEXT\_DAY |  |
| OADD\_MONTHS | ADD\_MONTHS |  |
| ROUND(Numeric) | ROUND |  |
| ROUND(Date) | ROUND\_DATE\_UDF |  |
| TRUNC(Date) | TRUNC\_UDF |  |
| YEAR | YEAR |  |

> See [DateTime and Interval Functions and Expressions](https://docs.teradata.com/r/kmuOwjp1zEYg98JsB8fu_A/JhmMJqd9vWURvHYeTRgQLQ)

## Hash functions[¶](#hash-functions "Link to this heading")

| Teradata | Snowflake | Note |
| --- | --- | --- |
| HASH\_MD5 | MD5 |  |
| HASHAMP  HASHBACKAM  HASHBUCKET  HASHROW | Not supported | Check notes on [the architecture differences between Teradata and Snowflake](#architecture-differences-between-teradata-and-snowflake) |

> See [Hash functions](https://docs.teradata.com/r/756LNiPSFdY~4JcCCcR5Cw/jslafnqlE8bGpg~wXQiEFw)

## JSON functions[¶](#json-functions "Link to this heading")

| Teradata | Snowflake | Note |
| --- | --- | --- |
| NEW JSON | TO\_JSON(PARSE\_JSON()**)** | Check [NEW JSON](#new-json) |
| JSON\_CHECK | CHECK\_JSON | Check JSON\_CHECK |
| JSON\_TABLE | Equivalent query | Check [JSON\_TABLE](#json-table) |
| JSONExtract  JSONExtractValue JSONExtractLargeValue | JSON\_EXTRACT\_UDF | Check [JSON\_EXTRACT](#json-extract) |

> See [JSON documentation](https://docs.teradata.com/r/C8cVEJ54PO4~YXWXeXGvsA/_aeoMCG0XgMNegNj0oy5cg)

## Null-Handling functions[¶](#null-handling-functions "Link to this heading")

| Teradata | Snowflake | Note |
| --- | --- | --- |
| NVL | NVL |  |
| NVL2 | NVL2 |  |

> See [Null-Handling functions](https://docs.teradata.com/r/756LNiPSFdY~4JcCCcR5Cw/4di35TY_6SqRNEGk4vv0ww)

## Ordered Analytical/Window Aggregate functions[¶](#ordered-analytical-window-aggregate-functions "Link to this heading")

| Teradata | Snowflake | Note |
| --- | --- | --- |
| CSUM(col1, col2) | SUM(col\_1) OVER (PARTITION BY null ORDER BY col\_2 ROWS UNBOUNDED PRECEDING) |  |
| CUME\_DIST | CUME\_DIST |  |
| DENSE\_RANK | DENSE\_RANK |  |
| FIRST\_VALUE | FIRST\_VALUE |  |
| LAG | LAG |  |
| LAST\_VALUE | LAST\_VALUE |  |
| LEAD | LEAD |  |
| MAVG(csales, 2, cdate, csales) | AVG(csales) OVER ( ORDER BY cdate, csales ROWS 1 PRECEDING) |  |
| MEDIAN | MEDIAN |  |
| MSUM(csales, 2, cdate, csales) | SUM(csales) OVER(ORDER BY cdate, csales ROWS 1 PRECEDING) |  |
| PERCENT\_RANK | PERCENT\_RANK |  |
| PERCENTILE\_CONT | PERCENTILE\_CONT |  |
| PERCENTILE\_DISC | PERCENTILE\_DISC |  |
| QUANTILE | QUANTILE |  |
| RANK | RANK |  |
| ROW\_NUMBER | ROW\_NUMBER |  |

> See [Window functions](https://docs.teradata.com/r/756LNiPSFdY~4JcCCcR5Cw/qbFqalW6IF5Fryz47~iqJQ)

## Period functions and operators[¶](#period-functions-and-operators "Link to this heading")

| Teradata | Snowflake | Note |
| --- | --- | --- |
| BEGIN | PERIOD\_BEGIN\_UDF |  |
| END | PERIOD\_END\_UDF |  |
| INTERVAL | TIMESTAMPDIFF |  |
| LAST | PERIOD\_LAST\_UDF |  |
| LDIFF | PERIOD\_LDIFF\_UDF |  |
| OVERLAPS | PUBLIC.PERIOD\_OVERLAPS\_UDF |  |
| PERIOD | PERIOD\_UDF |  |
| PERIOD(datetimeValue, UNTIL\_CHANGED)  PERIOD(datetimeValue, UNTIL\_CLOSED) | PERIOD\_UDF(datetimeValue, ‘9999-12-31 23:59:59.999999’) | See notes about [ending bound constants](#ending-bound-constants-until-changed-and-until-closed) |
| RDIFF | PERIOD\_RDIFF\_UDF |  |

> See [Period Functions and Operators](https://docs.teradata.com/r/Teradata-Database-SQL-Functions-Operators-Expressions-and-Predicates/June-2017/Period-Functions-and-Operators)

## Query band functions[¶](#query-band-functions "Link to this heading")

| Teradata | Snowflake | Note |
| --- | --- | --- |
| GETQUERYBANDVALUE | GETQUERYBANDVALUE\_UDF | Check G[ETQUERYBANDVALUE](#getquerybandvalue) |

> See [Query band functions](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/Teradata-VantageTM-Application-Programming-Reference-17.20/Workload-Management-Query-Band-APIs/Open-APIs-SQL-Interfaces)

## Regex functions[¶](#regex-functions "Link to this heading")

| Teradata | Snowflake | Note |
| --- | --- | --- |
| REGEXP\_INSTR | REGEXP\_INSTR | Check [Regex functions](#regex-functions) |
| REGEXP\_REPLACE | REGEXP\_REPLACE | Check [Regex functions](#regex-functions) |
| REGEXP\_SIMILAR | REGEXP\_LIKE | Check [Regex functions](#regex-functions) |
| REGEXP\_SUBSTR | REGEXP\_SUBSTR | Check [Regex functions](#regex-functions) |

> See [Regex functions](https://docs.teradata.com/r/756LNiPSFdY~4JcCCcR5Cw/yL2xT~elOTehmwVmwVBRHA)

## String operators and functions[¶](#string-operators-and-functions "Link to this heading")

| Teradata | Snowflake | Note |
| --- | --- | --- |
| ASCII | ASCII |  |
| CHAR2HEXINT | CHAR2HEXINT\_UDF |  |
| CHR | CHR/CHAR |  |
| CHAR\_LENGTH | LEN |  |
| CONCAT | CONCAT |  |
| EDITDISTANCE | EDITDISTANCE |  |
| INDEX | CHARINDEX | Check notes about [implicit conversion](#implicit-conversion) |
| INITCAP | INITCAP |  |
| INSTR | REGEXP\_INSTR |  |
| INSTR(StringValue, StringValue ,NumericNegativeValue, NumericValue) | INSTR\_UDF(StringValue, StringValue ,NumericNegativeValue, NumericValue) |  |
| LEFT | LEFT |  |
| LENGTH | LENGTH |  |
| LOWER | LOWER |  |
| LPAD | LPAD |  |
| LTRIM | LTRIM |  |
| OREPLACE | REPLACE |  |
| OTRANSLATE | TRANSLATE |  |
| POSITION | POSITION | Check notes about [implicit conversion](#implicit-conversion) |
| REVERSE | REVERSE |  |
| RIGHT | RIGHT |  |
| RPAD | RPAD |  |
| RTRIM | RTRIM |  |
| SOUNDEX | SOUNDEX\_P123 |  |
| STRTOK | STRTOK |  |
| STRTOK\_SPLIT\_TO\_TABLE | STRTOK\_SPLIT\_TO\_TABLE | Check [Strtok\_split\_to\_table](#strtok-split-to-table) |
| SUBSTRING | SUBSTR/SUBSTR\_UDF | Check [Substring](#substring) |
| TRANSLATE\_CHK | TRANSLATE\_CHK\_UDF |  |
| TRIM(LEADING ‘0’ FROM aTABLE) | LTRIM(aTABLE, ‘0’) |  |
| TRIM(TRAILING ‘0’ FROM aTABLE) | RTRIM(aTABLE, ‘0’) |  |
| TRIM(BOTH ‘0’ FROM aTABLE) | TRIM(aTABLE, ‘0’) |  |
| TRIM(CAST(numericValue AS FORMAT ‘999’)) | LPAD(numericValue, 3, 0) |  |
| UPPER | UPPER |  |

> See [String operators and functions](https://docs.teradata.com/reader/756LNiPSFdY~4JcCCcR5Cw/5nyfztBE7gDQVCVU2MFTnA)​​​

## St\_Point functions[¶](#st-point-functions "Link to this heading")

| Teradata | Snowflake | Note |
| --- | --- | --- |
| ST\_SPHERICALDISTANCE | HAVERSINE ST\_DISTANCE |  |

See [St\_Point functions](https://docs.teradata.com/r/W1AEeHO2cxTi3Sn7dtj8hg/JDVMx04qe~mo1mIm2h7NWQ)

## Table operators[¶](#table-operators "Link to this heading")

| Teradata | Snowflake | Note |
| --- | --- | --- |
| TD\_UNPIVOT | Equivalent query | Check [Td\_unpivot](#td-unpivot) |

> See [Table Operators](https://docs.teradata.com/r/Teradata-Database-SQL-Functions-Operators-Expressions-and-Predicates/June-2017/Table-Operators)

## XML functions[¶](#xml-functions "Link to this heading")

| Teradata | Snowflake | Note |
| --- | --- | --- |
| XMLAGG | LISTAGG | Check [Xmlagg](#xmlagg) |
| XMLQUERY | Not Supported |  |

> See [XML functions](https://docs.teradata.com/r/JTydkOYDksSy26sxlEtMvg/GhlIYri~mxyncdX5BV3jWA)

## Extensibility UDFs[¶](#extensibility-udfs "Link to this heading")

This section contains UDFs and other extensibility functions that are not offered as system built-in functions by Teradata but are transformed by SnowConvert AI

| Teradata | Snowflake | Note |
| --- | --- | --- |
| CHKNUM | CHKNUM\_UDF | Check [this UDF download page](https://downloads.teradata.com/download/extensibility/isnumeric-udf) |

## Notes[¶](#notes "Link to this heading")

### Architecture differences between Teradata and Snowflake[¶](#architecture-differences-between-teradata-and-snowflake "Link to this heading")

Teradata has a shared-nothing architecture with Access Module Processors (AMP) where each AMP manages their own share of disk storage and is accessed through hashing when doing queries. To take advantage of parallelism the stored information should be evenly distributed among AMPs and to do this Teradata offers a group of hash-related functions that can be used to determine how good the actual primary indexes are.

On the other hand, Snowflake architecture is different, and it manages how the data is stored on its own, meaning users do not need to worry about optimizing their data distribution.

### Ending bound constants (UNTIL\_CHANGED and UNTIL\_CLOSED)[¶](#ending-bound-constants-until-changed-and-until-closed "Link to this heading")

Both UNTIL\_CHANGED and UNTIL\_CLOSED are Teradata constants that represent an undefined ending bound for periods. Internally, these constants are represented as the maximum value a timestamp can have i.e ‘9999-12-31 23:59:59.999999’. During the migration of the PERIOD function, the ending bound is checked if present to determine if it is one of these constants and to replace it with varchar of value ‘9999-12-31 23:59:59.999999’ in case it is, Snowflake then casts the varchar to date or timestamp depending on the type of the beginning bound when calling PERIOD\_\_\_UDF.

### Implicit conversion[¶](#implicit-conversion "Link to this heading")

Some Teradata string functions like INDEX or POSITION accept non-string data types and implicitly convert them to string, this can cause inconsistencies in the results of those functions between Teradata and Snowflake. For example, the following Teradata code:

```
 SELECT INDEX(35, '5');
```

Copy

Returns 4, while the CHARINDEX equivalent in Snowflake:

```
 SELECT CHARINDEX('5', 35);
```

Copy

Returns 2, this happens because Teradata has its own [default formats](https://docs.teradata.com/r/S0Fw2AVH8ff3MDA0wDOHlQ/Xh8u4~A7KI46wOdMG9DSHQ) which are used during implicit conversion. In the above example, Teradata [interprets the numeric constant](https://docs.teradata.com/r/T5QsmcznbJo1bHmZT2KnFw/TEOJhlyP6az05SdTK9JHMg) 35 as BYTEINT and uses BYTEINT default format`'-999'` for the implicit conversion to string, causing the converted value to be `' 35'`. On the other hand, Snowflake uses its own [default formats](https://docs.snowflake.com/en/sql-reference/sql-format-models.html#default-formats-for-parsing), creating inconsistencies in the result.

To solve this, the following changes are done to those function parameters:

* If the parameter does **not** have a cast with format, then a snowflake`TO_VARCHAR`function with the default Teradata format equivalent in Snowflake is added instead.
* If the parameter does have a cast with format, then the format is converted to its Snowflake equivalent and the`TO_VARCHAR`function is added.

  + As a side note, Teradata ignores the sign of a number if it is not explicitly put inside a format, while Snowflake always adds spaces to insert the sign even when not specified, for those cases a check is done to see if the sign was specified and to remove it from the Snowflake string in case it was not.

After these changes, the resulting code would be:

```
 SELECT CHARINDEX( '5', TO_VARCHAR(35, 'MI999'));
```

Copy

Which returns 4, the same as the Teradata code.

## Known Issues [¶](#known-issues "Link to this heading")

No issues were found.

## Related EWIs [¶](#related-ewis "Link to this heading")

No related EWIs.

## COALESCE[¶](#coalesce "Link to this heading")

### Description[¶](#description "Link to this heading")

The coalesce function is used to return the first non-null element in a list. For more information check [COALESCE](https://docs.teradata.com/r/kmuOwjp1zEYg98JsB8fu_A/Wo3afkb7dFsUUAO5AwQOkQ).

```
COALESCE(element_1, element_2 [, element_3, ..., element_n])
```

Copy

Both Teradata and Snowflake COALESCE functions allow mixing numeric with string and date with timestamp parameters. However, they handle these two cases differently:

* Numeric along with string parameters: Teradata converts all numeric parameters to varchar while Snowflake does the opposite
* Timestamp along with date parameters: Teradata converts all timestamps to date while Snowflake does the opposite

To ensure functional equivalence in the first case, all numeric parameters are cast to`string`using`to_varchar`function, this takes the format of the numbers into account. In the second case, all timestamps are casted to date using `to_date`, Teradata ignores the format of timestamps when casting them so it is removed during transformation.

### Sample Source Patterns[¶](#sample-source-patterns "Link to this heading")

#### Numeric mixed with string parameters[¶](#numeric-mixed-with-string-parameters "Link to this heading")

##### *Teradata*[¶](#teradata "Link to this heading")

**Query**

```
 SELECT COALESCE(125, 'hello', cast(850 as format '-999'));
```

Copy



**Result**

```
COLUMN1|
-------+
125    |
```

Copy

##### *Snowflake*[¶](#snowflake "Link to this heading")

**Query**

```
SELECT
 COALESCE(TO_VARCHAR(125), 'hello', TO_VARCHAR(850, '9000'));
```

Copy



**Result**

```
COLUMN1|
-------+
125    |
```

Copy

#### Timestamp mixed with date parameters[¶](#timestamp-mixed-with-date-parameters "Link to this heading")

##### *Teradata*[¶](#id1 "Link to this heading")

**Query**

```
 SELECT COALESCE(cast(TIMESTAMP '2021-09-14 10:14:59' as format 'HH:MI:SSBDD-MM-YYYY'), current_date);
```

**Result**

```
COLUMN1    |
-----------+
2021-09-14 |
```

Copy

##### *Snowflake*[¶](#id2 "Link to this heading")

**Query**

```
SELECT
 COALESCE(TO_DATE(TIMESTAMP '2021-09-14 10:14:59' !!!RESOLVE EWI!!! /*** SSC-EWI-TD0025 - OUTPUT FORMAT 'HH:MI:SSBDD-MM-YYYY' NOT SUPPORTED. ***/!!!), CURRENT_DATE());
```

Copy



**Result**

```
COLUMN1    |
-----------+
2021-09-14 |
```

Copy

### Known Issues[¶](#id3 "Link to this heading")

No known issues\_.\_

### Related EWIs[¶](#id4 "Link to this heading")

* [SSC-EWI-TD0025](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/teradataEWI.html#ssc-ewi-td0025): Output format not supported.

## CURRENT\_TIMESTAMP[¶](#current-timestamp "Link to this heading")

### Severity[¶](#severity "Link to this heading")

Low

### Description[¶](#id5 "Link to this heading")

Fractional seconds are only displayed if it is explicitly set in the TIME\_OUTPUT\_FORMAT session parameter.

#### Input code:[¶](#input-code "Link to this heading")

```
SELECT current_timestamp(4) at local;
```

Copy

#### Output code:[¶](#output-code "Link to this heading")

```
SELECT
CURRENT_TIMESTAMP(4);
```

Copy

### Recommendations[¶](#recommendations "Link to this heading")

* Check if the TIME\_OUTPUT\_\_\_FORMAT session parameter is set to get the behavior that you want.
* If you need more support, you can email us at [snowconvert-support@snowflake.com](mailto:snowconvert-support%40snowflake.com)

### Known Issues [¶](#id6 "Link to this heading")

No issues were found.

### Related EWIs [¶](#id7 "Link to this heading")

No related EWIs.

## DAYNUMBER\_OF\_MONTH[¶](#daynumber-of-month "Link to this heading")

### Description[¶](#id8 "Link to this heading")

Returns the number of days elapsed from the beginning of the month to the given date. For more information check [DAYNUMBER\_OF\_MONTH](https://docs.teradata.com/r/kmuOwjp1zEYg98JsB8fu_A/msvzanlVHZUHwFv5LYpqzg).

```
DAYNUMBER_OF_MONTH(expression [, calendar_name])
```

Copy

Both Teradata and Snowflake handle the DAYNUMBER\_OF\_MONTH function in the same way, except in one case:

* The ISO calendar: An ISO month has 4 or 5 complete weeks. For more information check [About ISO Computation](https://docs.teradata.com/r/kmuOwjp1zEYg98JsB8fu_A/RdZQp3YPJ1WrBpj8b3uljA).

To ensure functional equivalence, a user-defined function (UDF) is added for the ISO calendar case.

### Sample Source Patterns[¶](#id9 "Link to this heading")

#### *Teradata*[¶](#id10 "Link to this heading")

**Query**

```
SELECT
    DAYNUMBER_OF_MONTH (DATE'2022-12-22'),
    DAYNUMBER_OF_MONTH (DATE'2022-12-22', NULL),
    DAYNUMBER_OF_MONTH (DATE'2022-12-22', 'Teradata'),
    DAYNUMBER_OF_MONTH (DATE'2022-12-22', 'COMPATIBLE');
```

Copy



**Result**

```
COLUMN1|COLUMN2|COLUMN3|COLUMN4|
-------+-------+-------+-------+
22     |22     |22     |22     |
```

Copy

#### *Snowflake*[¶](#id11 "Link to this heading")

**Query**

```
SELECT
    DAYOFMONTH(DATE'2022-12-22'),
    DAYOFMONTH(DATE'2022-12-22'),
    DAYOFMONTH(DATE'2022-12-22'),
    DAYOFMONTH(DATE'2022-12-22');
```

Copy



**Result**

```
COLUMN1|COLUMN2|COLUMN3|COLUMN4|
-------+-------+-------+-------+
22     |22     |22     |22     |
```

Copy

#### ISO calendar[¶](#iso-calendar "Link to this heading")

##### *Teradata*[¶](#id12 "Link to this heading")

**Query**

```
SELECT DAYNUMBER_OF_MONTH (DATE'2022-12-22', 'ISO');
```

Copy



**Result**

```
COLUMN1|
-------+
25     |
```

Copy

##### *Snowflake*[¶](#id13 "Link to this heading")

**Query**

```
SELECT
PUBLIC.DAYNUMBER_OF_MONTH_UDF(DATE'2022-12-22');
```

Copy



**Result**

```
COLUMN1|
-------+
25     |
```

Copy

### Known Issues [¶](#id14 "Link to this heading")

No issues were found.

### Related EWIs [¶](#id15 "Link to this heading")

No related EWIs.

## FROM\_BYTES[¶](#from-bytes "Link to this heading")

Translation specification for transforming the TO\_CHAR function into an equivalent function concatenation in Snowflake

### Description[¶](#id16 "Link to this heading")

The FROM\_BYTES function encodes a sequence of bits into a sequence of characters representing its encoding. For more information check [FROM\_BYTES(Encoding)](https://www.docs.teradata.com/r/Teradata-VantageTM-Data-Types-and-Literals/March-2019/Data-Type-Conversion-Functions/FROM_BYTES).

Snowflake does not have support for FROM\_BYTES function, however, some workarounds can be done for the most common occurrences of this function.

### Sample Source Patterns[¶](#id17 "Link to this heading")

#### Teradata[¶](#id18 "Link to this heading")

##### Query[¶](#query "Link to this heading")

```
 SELECT 
FROM_BYTES('5A1B'XB, 'base10'), --returns '23067'
FROM_BYTES('5A3F'XB, 'ASCII'), --returns 'Z\ESC '
FROM_BYTES('5A1B'XB, 'base16'); -- returns '5A1B'
```

Copy

##### Result[¶](#result "Link to this heading")

```
COLUMN1    | COLUMN2    | COLUMN3 |
-----------+------------+---------+
23067      |  Z\ESC     | 5A1B    |
```

Copy

##### Snowflake[¶](#id19 "Link to this heading")

##### Query[¶](#id20 "Link to this heading")

```
 SELECT
--returns '23067'
TO_NUMBER('5A1B', 'XXXX'),
--returns 'Z\ESC '
!!!RESOLVE EWI!!! /*** SSC-EWI-0031 - FROM_BYTES FUNCTION NOT SUPPORTED ***/!!!
FROM_BYTES(TO_BINARY('5A3F'), 'ASCII'),
TO_BINARY('5A1B', 'HEX'); -- returns '5A1B'
```

Copy

##### Result[¶](#id21 "Link to this heading")

```
COLUMN1    | COLUMN2    | COLUMN3 |
-----------+------------+---------+
23067      |  Z\ESC     | 5A1B    |
```

Copy

Note

Some parts in the output code are omitted for clarity reasons.

### Known Issues[¶](#id22 "Link to this heading")

1. TO\_NUMBER format parameter must match with the digits on the input string.
2. There is no functional equivalent built-in function for FROM\_BYTES when encoding to ANSI

### Related EWIs[¶](#id23 "Link to this heading")

1. [SSC-EWI-0031](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0031): FUNCTION NOT SUPPORTED

## GETQUERYBANDVALUE[¶](#getquerybandvalue "Link to this heading")

Translation specification for the transformation of GetQueryBandValue to Snowflake

### Description[¶](#id24 "Link to this heading")

The GetQueryBandValue function searches a name key inside of the query band and returns its associated value if present. It can be used to search inside the transaction, session, profile, or any of the key-value pairs of the query band.

For more information on this function check [GetQueryBandValue](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/Teradata-VantageTM-Application-Programming-Reference-17.20/Workload-Management-Query-Band-APIs/Open-APIs-SQL-Interfaces/GetQueryBandValue) in the Teradata documentation.

```
[SYSLIB.]GetQueryBandValue([QueryBandIn,] SearchType, Name);
```

Copy

### Sample Source Patterns[¶](#id25 "Link to this heading")

#### Setup data[¶](#setup-data "Link to this heading")

##### Teradata[¶](#id26 "Link to this heading")

##### Query[¶](#id27 "Link to this heading")

```
 SET QUERY_BAND = 'hola=hello;adios=bye;' FOR SESSION;
```

Copy

##### *Snowflake*[¶](#id28 "Link to this heading")

##### Query[¶](#id29 "Link to this heading")

```
 ALTER SESSION SET QUERY_TAG = 'hola=hello;adios=bye;';
```

Copy

#### GetQueryBandValue with QueryBandIn parameter[¶](#getquerybandvalue-with-querybandin-parameter "Link to this heading")

##### *Teradata*[¶](#id30 "Link to this heading")

##### Query[¶](#id31 "Link to this heading")

```
 SELECT
GETQUERYBANDVALUE('=T> user=Mark;account=Mark200; =S> user=Sara;account=SaraDB;role=DbAdmin =P> user=Peter;account=Peter3;', 0, 'account') as Example1,
GETQUERYBANDVALUE('=T> user=Mark;account=Mark200; =S> user=Sara;account=SaraDB;role=DbAdmin =P> user=Peter;account=Peter3;', 1, 'account') as Example2,
GETQUERYBANDVALUE('=T> user=Mark;account=Mark200; =S> user=Sara;account=SaraDB;role=DbAdmin =P> user=Peter;account=Peter3;', 2, 'account') as Example3,
GETQUERYBANDVALUE('=T> user=Mark;account=Mark200; =S> user=Sara;account=SaraDB;role=DbAdmin =P> user=Peter;account=Peter3;', 3, 'account') as Example4,
GETQUERYBANDVALUE('=T> user=Mark;account=Mark200; =S> user=Sara;account=SaraDB;role=DbAdmin =P> user=Peter;account=Peter3;', 0, 'role') as Example5,
GETQUERYBANDVALUE('=T> user=Mark;account=Mark200; =S> user=Sara;account=SaraDB;role=DbAdmin =P> user=Peter;account=Peter3;', 1, 'role') as Example6;
```

Copy

##### Result[¶](#id32 "Link to this heading")

```
+----------+----------+----------+----------+----------+----------+
| EXAMPLE1 | EXAMPLE2 | EXAMPLE3 | EXAMPLE4 | EXAMPLE5 | EXAMPLE6 |
+----------+----------+----------+----------+----------+----------+
| Mark200  | Mark200  | SaraDB   | Peter3   | DbAdmin  |          |
+----------+----------+----------+----------+----------+----------+
```

Copy

##### *Snowflake*[¶](#id33 "Link to this heading")

##### Query[¶](#id34 "Link to this heading")

```
 SELECT
GETQUERYBANDVALUE_UDF('=T> user=Mark;account=Mark200; =S> user=Sara;account=SaraDB;role=DbAdmin =P> user=Peter;account=Peter3;', 0, 'account') as Example1,
GETQUERYBANDVALUE_UDF('=T> user=Mark;account=Mark200; =S> user=Sara;account=SaraDB;role=DbAdmin =P> user=Peter;account=Peter3;', 1, 'account') as Example2,
GETQUERYBANDVALUE_UDF('=T> user=Mark;account=Mark200; =S> user=Sara;account=SaraDB;role=DbAdmin =P> user=Peter;account=Peter3;', 2, 'account') as Example3,
GETQUERYBANDVALUE_UDF('=T> user=Mark;account=Mark200; =S> user=Sara;account=SaraDB;role=DbAdmin =P> user=Peter;account=Peter3;', 3, 'account') as Example4,
GETQUERYBANDVALUE_UDF('=T> user=Mark;account=Mark200; =S> user=Sara;account=SaraDB;role=DbAdmin =P> user=Peter;account=Peter3;', 0, 'role') as Example5,
GETQUERYBANDVALUE_UDF('=T> user=Mark;account=Mark200; =S> user=Sara;account=SaraDB;role=DbAdmin =P> user=Peter;account=Peter3;', 1, 'role') as Example6;
```

Copy

##### Result[¶](#id35 "Link to this heading")

```
+----------+----------+----------+----------+----------+----------+
| EXAMPLE1 | EXAMPLE2 | EXAMPLE3 | EXAMPLE4 | EXAMPLE5 | EXAMPLE6 |
+----------+----------+----------+----------+----------+----------+
| Mark200  | Mark200  | SaraDB   | Peter3   | DbAdmin  |          |
+----------+----------+----------+----------+----------+----------+
```

Copy

#### GetQueryBandValue without QueryBandIn parameter[¶](#getquerybandvalue-without-querybandin-parameter "Link to this heading")

##### *Teradata*[¶](#id36 "Link to this heading")

##### Query[¶](#id37 "Link to this heading")

```
 SELECT
GETQUERYBANDVALUE(2, 'hola') as Example1,
GETQUERYBANDVALUE(2, 'adios') as Example2;
```

Copy

##### Result[¶](#id38 "Link to this heading")

```
+----------+----------+
| EXAMPLE1 | EXAMPLE2 |
+----------+----------+
| hello    | bye      |
+----------+----------+
```

Copy

##### *Snowflake*[¶](#id39 "Link to this heading")

##### Query[¶](#id40 "Link to this heading")

```
 SELECT
GETQUERYBANDVALUE_UDF('hola') as Example1,
GETQUERYBANDVALUE_UDF('adios') as Example2;
```

Copy

##### Result[¶](#id41 "Link to this heading")

```
+----------+----------+
| EXAMPLE1 | EXAMPLE2 |
+----------+----------+
| hello    | bye      |
+----------+----------+
```

Copy

Note

Some parts in the output code are omitted for clarity reasons.

### Known Issues[¶](#id42 "Link to this heading")

**1. GetQueryBandValue without QueryBandIn parameter only supported for session**

Teradata allows defining query bands at transaction, session or profile levels. If GetQueryBandValue is called without specifying an input query band Teradata will automatically check the transaction, session or profile query bands depending on the value of the SearchType parameter.

In Snowflake the closest equivalent to query bands are query tags, which can be specified for session, user and account.

Due to these differences, the implementation of GetQueryBandValue without QueryBandIn parameter only considers the session query tag and may not work as expected for other search types.

### Related EWIs[¶](#id43 "Link to this heading")

No related EWIs.

## JSON\_CHECK[¶](#json-check "Link to this heading")

### Description[¶](#id44 "Link to this heading")

The JSON\_CHECK function checks a string for valid JSON.

For more information regarding Teradata JSON\_CHECK, check [here](https://docs.teradata.com/r/Teradata-Database-JSON-Data-Type/June-2017/JSON-Functions-and-Operators/JSON_CHECK).

```
[TD_SYSFNLIB.]JSON_CHECK(string_expr);
```

Copy

### Sample Source Pattern[¶](#sample-source-pattern "Link to this heading")

#### Basic Source Pattern[¶](#basic-source-pattern "Link to this heading")

##### Teradata[¶](#id45 "Link to this heading")

**Query**

```
SELECT JSON_CHECK('{"key": "value"}');
```

Copy

##### Snowflake Scripting[¶](#snowflake-scripting "Link to this heading")

**Query**

```
SELECT
IFNULL(CHECK_JSON('{"key": "value"}'), 'OK');
```

Copy

#### JSON\_CHECK inside CASE transformation[¶](#json-check-inside-case-transformation "Link to this heading")

##### Teradata[¶](#id46 "Link to this heading")

**Query**

```
SELECT CASE WHEN JSON_CHECK('{}') = 'OK' then 'OKK' ELSE 'NOT OK' END;
```

Copy

##### Snowflake Scripting[¶](#id47 "Link to this heading")

**Query**

```
SELECT
CASE
WHEN UPPER(RTRIM(IFNULL(CHECK_JSON('{}'), 'OK'))) = UPPER(RTRIM('OK'))
THEN 'OKK' ELSE 'NOT OK'
END;
```

Copy

### Known Issues [¶](#id48 "Link to this heading")

No issues were found.

### Related EWIs [¶](#id49 "Link to this heading")

No related EWIs.

## JSON\_EXTRACT[¶](#json-extract "Link to this heading")

Translation reference to convert the Teradata functions JSONExtractValue, JSONExtractLargeValue and JSONExtract to Snowflake Scripting.

### Description[¶](#id50 "Link to this heading")

As per Teradata’s documentation, these functions use the [JSONPath Query Syntax](https://docs.teradata.com/r/Teradata-VantageTM-JSON-Data-Type/March-2019/Operations-on-the-JSON-Type/JSONPath-Request-Syntax) to request information about a portion of a JSON instance. The entity desired can be any portion of a JSON instance, such as a name/value pair, an object, an array, an array element, or a value.

For more information regarding Teradata JSONExtractValue, JSONExtractLargeValue and JSONExtract, check [here](https://docs.teradata.com/r/Teradata-VantageTM-JSON-Data-Type/March-2019/JSON-Methods/Comparison-of-JSONExtract-and-JSONExtractValue).

```
 JSON_expr.JSONExtractValue(JSONPath_expr)

JSON_expr.JSONExtractLargeValue(JSONPath_expr)

JSON_expr.JSONExtract(JSONPath_expr)
```

Copy

The JSON\_EXTRACT\_UDF is a Snowflake implementation of the JSONPath specification that uses a modified version of the original JavaScript implementation developed by [Stefan Goessner](https://goessner.net/index.html).

#### Sample Source Pattern[¶](#id51 "Link to this heading")

##### Teradata[¶](#id52 "Link to this heading")

##### Query[¶](#id53 "Link to this heading")

```
 SELECT
    Store.JSONExtract('$..author') as AllAuthors,
    Store.JSONExtractValue('$..book[2].title') as ThirdBookTitle,
    Store.JSONExtractLargeValue('$..book[2].price') as ThirdBookPrice
FROM BookStores;
```

Copy

##### Snowflake Scripting[¶](#id54 "Link to this heading")

##### Query[¶](#id55 "Link to this heading")

```
 SELECT
    JSON_EXTRACT_UDF(Store, '$..author', FALSE) as AllAuthors,
    JSON_EXTRACT_UDF(Store, '$..book[2].title', TRUE) as ThirdBookTitle,
    JSON_EXTRACT_UDF(Store, '$..book[2].price', TRUE) as ThirdBookPrice
    FROM
    BookStores;
```

Copy

Note

Some parts in the output code are omitted for clarity reasons.

### Known Issues[¶](#id56 "Link to this heading")

#### 1. Elements inside JSONs may not retain their original order.[¶](#elements-inside-jsons-may-not-retain-their-original-order "Link to this heading")

Elements inside a JSON are ordered by their keys when inserted in a table. Thus, the query results might differ. However, this does not affect the order of arrays inside the JSON.

For example, if the original JSON is:

```
 { 
   "firstName":"Peter",
   "lastName":"Andre",
   "age":31,
   "cities": ["Los Angeles", "Lima", "Buenos Aires"]
}
```

Copy

Using the Snowflake [PARSE\_JSON()](https://docs.snowflake.com/en/sql-reference/functions/parse_json.html) that interprets an input string as a JSON document, producing a VARIANT value. The inserted JSON will be:

```
 { 
   "age": 31,
   "cities": ["Los Angeles", "Lima", "Buenos Aires"],
   "firstName": "Peter",
   "lastName": "Andre" 
}
```

Copy

Note how “age” is now the first element. However, the array of “cities” maintains its original order.

### Related EWIs[¶](#id57 "Link to this heading")

No related EWIs.

## JSON\_TABLE[¶](#json-table "Link to this heading")

Translation specification for the transformation of JSON\_TABLE into a equivalent query in Snowflake

Note

Some parts in the output code are omitted for clarity reasons.

### Description[¶](#id58 "Link to this heading")

Creates a table based on the contents of a JSON document. See [JSON\_TABLE documentation](https://docs.teradata.com/r/Teradata-VantageTM-JSON-Data-Type-17.20/JSON-Shredding/JSON_TABLE).

```
[TD_SYSFNLIB.]JSON_TABLE(
  ON (json_documents_retrieving_expr)
  USING 
      ROWEXPR (row_expr_literal) 
      COLEXPR (column_expr_literal)
  [AS] correlation_name [(column_name [,...])]
)
```

Copy

The conversion of JSON\_TABLE has the considerations shown below:

* ROW\_NUMBER() is an equivalent of ordinal columns in Snowflake.
* In Teradata, the second column of JSON\_TABLE must be JSON type because the generated columns replace the second column, for that reason, SnowConvert AI assumes that the column has the right type, and uses it for the transformation.

### Sample Source Patterns[¶](#id59 "Link to this heading")

#### Setup data[¶](#id60 "Link to this heading")

##### Teradata[¶](#id61 "Link to this heading")

##### Query[¶](#id62 "Link to this heading")

```
 create table myJsonTable(
 col1 integer,
 col2 JSON(1000)
 );
 
 
insert into myJsonTable values(1, 
new json('{
"name": "Matt",
"age" : 30,
"songs" : [
	{"name" : "Late night", "genre" : "Jazz"},
	{"name" : "Wake up", "genre" : "Rock"},
	{"name" : "Who am I", "genre" : "Rock"},
	{"name" : "Raining", "genre" : "Blues"}
]
}'));
```

Copy

##### *Snowflake*[¶](#id63 "Link to this heading")

##### Query[¶](#id64 "Link to this heading")

```
 CREATE OR REPLACE TABLE myJsonTable (
 col1 integer,
 col2 VARIANT
 )
 COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;

INSERT INTO myJsonTable
VALUES (1, TO_JSON(PARSE_JSON('{
"name": "Matt",
"age" : 30,
"songs" : [
	{"name" : "Late night", "genre" : "Jazz"},
	{"name" : "Wake up", "genre" : "Rock"},
	{"name" : "Who am I", "genre" : "Rock"},
	{"name" : "Raining", "genre" : "Blues"}
]
}')));
```

Copy

#### Pattern code 1[¶](#pattern-code-1 "Link to this heading")

##### *Teradata*[¶](#id65 "Link to this heading")

##### Query[¶](#id66 "Link to this heading")

```
 SELECT * FROM
JSON_TABLE(ON (SELECT COL1, COL2 FROM myJsonTable WHERE col1 = 1)
USING rowexpr('$.songs[*]')
colexpr('[ {"jsonpath" : "$.name",
            "type" : "CHAR(20)"},
            {"jsonpath" : "$.genre",
             "type" : "VARCHAR(20)"}]')) AS JT(ID, "Song name", Genre);
```

Copy

##### Result[¶](#id67 "Link to this heading")

```
ID | Song name  | Genre |
---+------------+-------+
1  | Late night | Jazz  |
---+------------+-------+
1  | Wake up    | Rock  |
---+------------+-------+
1  | Who am I   | Rock  |
---+------------+-------+
1  | Raining    | Blues |
```

Copy

##### *Snowflake*[¶](#id68 "Link to this heading")

##### Query[¶](#id69 "Link to this heading")

```
 SELECT
* FROM
(
SELECT
COL1 AS ID,
rowexpr.value:name :: CHAR(20) AS "Song name",
rowexpr.value:genre :: VARCHAR(20) AS Genre
FROM
myJsonTable,
TABLE(FLATTEN(INPUT => COL2:songs)) rowexpr
WHERE col1 = 1
) JT;
```

Copy

##### Result[¶](#id70 "Link to this heading")

```
ID | Song name  | Genre |
---+------------+-------+
1  | Late night | Jazz  |
---+------------+-------+
1  | Wake up    | Rock  |
---+------------+-------+
1  | Who am I   | Rock  |
---+------------+-------+
1  | Raining    | Blues |
```

Copy

### Known Issues[¶](#id71 "Link to this heading")

**1. The JSON path in COLEXPR can not have multiple asterisk accesses**

The columns JSON path cannot have multiple lists with asterisk access, for example: `$.Names[*].FullNames[*]`. On the other hand, the JSON path of ROWEXP can have it.

**2. JSON structure defined in the COLEXPR literal must be a valid JSON**

When it is not the case the user will be warned about the JSON being badly formed.

### Related EWIs[¶](#id72 "Link to this heading")

No related EWIs.

## NEW JSON[¶](#new-json "Link to this heading")

### Description[¶](#id73 "Link to this heading")

Allocates a new instance of a JSON datatype. For more information check [NEW JSON Constructor Expression.](https://docs.teradata.com/r/Teradata-Database-JSON-Data-Type/June-2017/The-JSON-Data-Type/About-JSON-Type-Constructor/NEW-JSON-Constructor-Expression)

```
NEW JSON ( [ JSON_string_spec | JSON_binary_data_spec ] )

JSON_string_spec := JSON_String_literal [, { LATIN | UNICODE | BSON | UBJSON } ]

JSON_binary_data_spec := JSON_binary_literal [, { BSON | UBJSON } ]
```

Copy

The second parameter of the NEW JSON function is always omitted by SnowConvert AI since Snowflake works only with UTF-8.

### Sample Source Patterns[¶](#id74 "Link to this heading")

#### NEW JSON with string data[¶](#new-json-with-string-data "Link to this heading")

##### *Teradata*[¶](#id75 "Link to this heading")

**Query**

```
SELECT NEW JSON ('{"name" : "cameron", "age" : 24}'),
NEW JSON ('{"name" : "cameron", "age" : 24}', LATIN);
```

Copy



**Result**

| COLUMN1 | COLUMN2 |
| --- | --- |
| {“age”:24,”name”:”cameron”} | {“age”:24,”name”:”cameron”} |

##### *Snowflake*[¶](#id76 "Link to this heading")

**Query**

```
SELECT
TO_JSON(PARSE_JSON('{"name" : "cameron", "age" : 24}')),
!!!RESOLVE EWI!!! /*** SSC-EWI-TD0039 - INPUT FORMAT 'LATIN' NOT SUPPORTED ***/!!!
TO_JSON(PARSE_JSON('{"name" : "cameron", "age" : 24}'));
```

Copy



**Result**

| COLUMN1 | COLUMN2 |
| --- | --- |
| {“age”:24,”name”:”cameron”} | {“age”:24,”name”:”cameron”} |

### Known Issues[¶](#id77 "Link to this heading")

**1. The second parameter is not supported**

The second parameter of the function used to specify the format of the resulting JSON is not supported because Snowflake only supports UTF-8, this may result in functional differences for some uses of the function.

**2. JSON with BINARY data is not supported**

Snowflake does not support parsing binary data to create a JSON value, the user will be warned when SnowConvert AI finds a NEW JSON with binary data.

### Related EWIs[¶](#id78 "Link to this heading")

1. [SSC-EWI-TD0039](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/teradataEWI.html#ssc-ewi-td0039): Input format not supported.

## NVP[¶](#nvp "Link to this heading")

### Description[¶](#id79 "Link to this heading")

Extracts the value of the key-value pair where the key matches the nth occurrence of the specified name to search. See [NVP](https://docs.teradata.com/r/Teradata-VantageTM-SQL-Functions-Expressions-and-Predicates-17.20/String-Operators-and-Functions/NVP).

```
[TD_SYSFNLIB.] NVP (
in_string,
name_to_search
[, name_delimiters ]
[, value_delimiters ]
[, occurrence ]
)
```

Copy

### Sample Source Patterns[¶](#id80 "Link to this heading")

#### NVP basic case[¶](#nvp-basic-case "Link to this heading")

##### *Teradata*[¶](#id81 "Link to this heading")

**Query**

```
SELECT
NVP('entree=-orange chicken&entree+.honey salmon', 'entree', '&', '=- +.', 1),
NVP('Hello=bye|name=Lucas|Hello=world!', 'Hello', '|', '=', 2),
NVP('Player=Mario$Game&Tenis%Player/Susana$Game=Chess', 'Player', '% $', '= & /', 2);
```

Copy



**Result**

```
COLUMN1        | COLUMN2 | COLUMN3 |
---------------+---------+---------+
orange chicken | world!  | Susana  |
```

Copy

##### *Snowflake*[¶](#id82 "Link to this heading")

**Query**

```
SELECT
PUBLIC.NVP_UDF('entree=-orange chicken&entree+.honey salmon', 'entree', '&', '=- +.', 1),
PUBLIC.NVP_UDF('Hello=bye|name=Lucas|Hello=world!', 'Hello', '|', '=', 2),
PUBLIC.NVP_UDF('Player=Mario$Game&Tenis%Player/Susana$Game=Chess', 'Player', '% $', '= & /', 2);
```

Copy



**Result**

```
COLUMN1        | COLUMN2 | COLUMN3 |
---------------+---------+---------+
orange chicken | world!  | Susana  |
```

Copy

#### NVP with optional parameters ignored[¶](#nvp-with-optional-parameters-ignored "Link to this heading")

##### *Teradata*[¶](#id83 "Link to this heading")

**Query**

```
SELECT
NVP('City=Los Angeles&Color=Green&Color=Blue&City=San Jose', 'Color'),
NVP('City=Los Angeles&Color=Green&Color=Blue&City=San Jose', 'Color', 2),
NVP('City=Los Angeles#Color=Green#Color=Blue#City=San Jose', 'City', '#', '=');
```

Copy



**Result**

```
COLUMN1 | COLUMN2 | COLUMN3     |
--------+---------+-------------+
Green   | Blue    | Los Angeles |
```

Copy

##### *Snowflake*[¶](#id84 "Link to this heading")

**Query**

```
SELECT
    PUBLIC.NVP_UDF('City=Los Angeles&Color=Green&Color=Blue&City=San Jose', 'Color', '&', '=', 1),
    PUBLIC.NVP_UDF('City=Los Angeles&Color=Green&Color=Blue&City=San Jose', 'Color', '&', '=', 2),
    PUBLIC.NVP_UDF('City=Los Angeles#Color=Green#Color=Blue#City=San Jose', 'City', '#', '=', 1);
```

Copy



**Result**

```
COLUMN1 | COLUMN2 | COLUMN3     |
--------+---------+-------------+
Green   | Blue    | Los Angeles |
```

Copy

#### NVP with spaces in delimiters[¶](#nvp-with-spaces-in-delimiters "Link to this heading")

##### *Teradata*[¶](#id85 "Link to this heading")

**Query**

```
SELECT
NVP('store = whole foods&&store: ?Bristol farms','store', '&&', '\ =\  :\ ?', 2),
NVP('Hello = bye|name = Lucas|Hello = world!', 'Hello', '|', '\ =\ ', 2);
```

Copy



**Result**

```
COLUMN1       | COLUMN2 |
--------------+---------+
Bristol farms | world!  |
```

Copy

##### *Snowflake*[¶](#id86 "Link to this heading")

**Query**

```
SELECT
PUBLIC.NVP_UDF('store = whole foods&&store: ?Bristol farms', 'store', '&&', '\\ =\\  :\\ ?', 2),
PUBLIC.NVP_UDF('Hello = bye|name = Lucas|Hello = world!', 'Hello', '|', '\\ =\\ ', 2);
```

Copy



**Result**

```
COLUMN1       | COLUMN2 |
--------------+---------+
Bristol farms | world!  |
```

Copy

#### NVP with non-literal delimiters[¶](#nvp-with-non-literal-delimiters "Link to this heading")

##### *Teradata*[¶](#id87 "Link to this heading")

**Query**

```
SELECT NVP('store = whole foods&&store: ?Bristol farms','store', '&&', valueDelimiter, 2);
```

Copy

##### *Snowflake*[¶](#id88 "Link to this heading")

**Query**

```
SELECT
PUBLIC.NVP_UDF('store = whole foods&&store: ?Bristol farms', 'store', '&&', valueDelimiter, 2) /*** SSC-FDM-TD0008 - WHEN NVP_UDF FOURTH PARAMETER IS NON-LITERAL AND IT CONTAINS A BACKSLASH, THAT BACKSLASH NEEDS TO BE ESCAPED ***/;
```

Copy

### Known Issues[¶](#id89 "Link to this heading")

**1. Delimiters with spaces (\ ) need to have the backslash scaped in Snowflake**

In Teradata, delimiters including space specify them using “\ “ (see [NVP with spaces in delimiters](#nvp-with-spaces-in-delimiters)), as shown in the examples, in Teradata it is not necessary to escape the backslash, however, it is necessary in Snowflake. Escaping the backslashes in the delimiter can be done automatically by SnowConvert AI but only if the delimiter values are literal strings, otherwise the user will be warned that the backlashes could not be escaped and that it may cause different results in Snowflake.

### Related EWIs[¶](#id90 "Link to this heading")

1. [SSC-FDM-TD0008](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/teradataFDM.html#ssc-fdm-td0008): Non-literal delimiters with spaces need their backslash scaped in snowflake.

## OVERLAPS[¶](#overlaps "Link to this heading")

### Description[¶](#id91 "Link to this heading")

According to Teradata’s documentation, the OVERLAPS operator compares two or more period expressions. If they overlap, it returns true.

For more information regarding Teradata’s OVERLAPS, check [here](https://docs.teradata.com/r/kmuOwjp1zEYg98JsB8fu_A/3VIgdwHNVU~tsnNiIR1aEw).

```
period_expression
OVERLAPS
period_expression
```

Copy

The PERIOD\_OVERLAPS\_UDF is a Snowflake implementation of the OVERLAPS operator in Teradata.

### Sample Source Pattern[¶](#id92 "Link to this heading")

#### Teradata[¶](#id93 "Link to this heading")

**Query**

```
SELECT 
    PERIOD(DATE '2009-01-01', DATE '2010-09-24') 
    OVERLAPS
    PERIOD(DATE '2009-02-01', DATE '2009-06-24');
```

Copy

#### Snowflake Scripting[¶](#id94 "Link to this heading")

**Query**

```
SELECT
    PUBLIC.PERIOD_OVERLAPS_UDF(ARRAY_CONSTRUCT(PUBLIC.PERIOD_UDF(DATE '2009-01-01', DATE '2010-09-24') !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!, PUBLIC.PERIOD_UDF(DATE '2009-02-01', DATE '2009-06-24') !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!)) !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!;
```

Copy

### Known Issues[¶](#id95 "Link to this heading")

#### 1. Unsupported Period Expressions[¶](#unsupported-period-expressions "Link to this heading")

The *PERIOD(TIME WITH TIME ZONE)* and *PERIOD(TIMESTAMP WITH TIME ZONE)* expressions are not supported yet.

### Related EWIs[¶](#id96 "Link to this heading")

1. [SSC-EWI-TD0053](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/teradataEWI.html#ssc-ewi-td0053): Snowflake does not support the period datatype, all periods are handled as varchar instead

## P\_INTERSECT[¶](#p-intersect "Link to this heading")

### Description[¶](#id97 "Link to this heading")

According to Teradata’s documentation, the P\_INTERSECT operator compares two or more period expressions. If they overlap, it returns the common portion of the period expressions.

For more information regarding Teradata’s P\_INTERSECT, check [here](https://docs.teradata.com/r/kmuOwjp1zEYg98JsB8fu_A/iW6iefgeyOypFOMY2qGG_A).

```
period_expression
P_INTERSECT
period_expression
```

Copy

The PERIOD\_INTERSECT\_UDF is a Snowflake implementation of the P\_INTERSECT operator in Teradata.

### Sample Source Pattern[¶](#id98 "Link to this heading")

#### Teradata[¶](#id99 "Link to this heading")

**Query**

```
SELECT 
    PERIOD(DATE '2009-01-01', DATE '2010-09-24') 
    P_INTERSECT 
    PERIOD(DATE '2009-02-01', DATE '2009-06-24');
```

Copy

#### Snowflake Scripting[¶](#id100 "Link to this heading")

**Query**

```
SELECT
    PUBLIC.PERIOD_INTERSECT_UDF(ARRAY_CONSTRUCT(PUBLIC.PERIOD_UDF(DATE '2009-01-01', DATE '2010-09-24') !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!, PUBLIC.PERIOD_UDF(DATE '2009-02-01', DATE '2009-06-24') !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!)) !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!;
```

Copy

### Known Issues[¶](#id101 "Link to this heading")

#### 1. Unsupported Period Expressions[¶](#id102 "Link to this heading")

The *PERIOD(TIME WITH TIME ZONE)* and *PERIOD(TIMESTAMP WITH TIME ZONE)* expressions are not supported yet.

### Related EWIs[¶](#id103 "Link to this heading")

1. [SSC-EWI-TD0053](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/teradataEWI.html#ssc-ewi-td0053): Snowflake does not support the period datatype, all periods are handled as varchar instead

## PIVOT[¶](#pivot "Link to this heading")

Translation specification for the PIVOT function form Teradata to Snowflake

Note

Some parts in the output code are omitted for clarity reasons.

### Description[¶](#id104 "Link to this heading")

The pivot function is used to transform rows of a table into columns. For more information check the [PIVOT Teradata documentation.](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/Teradata-VantageTM-SQL-Functions-Expressions-and-Predicates-17.20/Aggregate-Functions/PIVOT)

```
PIVOT ( pivot_spec )
  [ WITH with_spec [,...] ]
  [AS] derived_table_name [ ( cname [,...] ) ]
  
pivot_spec := aggr_fn_spec [,...] FOR for_spec

aggr_fn_spec := aggr_fn ( cname ) [ [AS] pvt_aggr_alias ]

for_spec := { cname IN ( expr_spec_1 [,...] ) |
( cname [,...] ) IN ( expr_spec_2 [,...] ) |
cname IN ( subquery )
}

expr_spec_1 := expr [ [AS] expr_alias_name ]

expr_spec_2 := ( expr [,...] ) [ [AS] expr_alias_name ]

with_spec := aggr_fn ( { cname [,...] | * } ) [AS] aggr_alias
```

Copy

### Sample Source Patterns[¶](#id105 "Link to this heading")

#### Setup data[¶](#id106 "Link to this heading")

##### Teradata[¶](#id107 "Link to this heading")

##### Query[¶](#id108 "Link to this heading")

```
 CREATE TABLE star1(
	country VARCHAR(20),
	state VARCHAR(10), 
	yr INTEGER,
	qtr VARCHAR(3),
	sales INTEGER,
	cogs INTEGER
);

insert into star1 values ('USA', 'CA', 2001, 'Q1', 30, 15);
insert into star1 values ('Canada', 'ON', 2001, 'Q2', 10, 0);
insert into star1 values ('Canada', 'BC', 2001, 'Q3', 10, 0);
insert into star1 values ('USA', 'NY', 2001, 'Q1', 45, 25);
insert into star1 values ('USA', 'CA', 2001, 'Q2', 50, 20);
```

Copy

##### *Snowflake*[¶](#id109 "Link to this heading")

##### Query[¶](#id110 "Link to this heading")

```
 CREATE OR REPLACE TABLE star1 (
	country VARCHAR(20),
	state VARCHAR(10),
	yr INTEGER,
	qtr VARCHAR(3),
	sales INTEGER,
	cogs INTEGER
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;

INSERT INTO star1
VALUES ('USA', 'CA', 2001, 'Q1', 30, 15);

INSERT INTO star1
VALUES ('Canada', 'ON', 2001, 'Q2', 10, 0);

INSERT INTO star1
VALUES ('Canada', 'BC', 2001, 'Q3', 10, 0);

INSERT INTO star1
VALUES ('USA', 'NY', 2001, 'Q1', 45, 25);

INSERT INTO star1
VALUES ('USA', 'CA', 2001, 'Q2', 50, 20);
```

Copy

#### Basic PIVOT transformation[¶](#basic-pivot-transformation "Link to this heading")

##### *Teradata*[¶](#id111 "Link to this heading")

##### Query[¶](#id112 "Link to this heading")

```
 SELECT *
FROM star1 PIVOT (
	SUM(sales) FOR qtr                                                                                               
    IN ('Q1',                                                                                                     
    	'Q2', 
        'Q3')
)Tmp;
```

Copy

##### Result[¶](#id113 "Link to this heading")

```
Country | State | yr   | cogs | 'Q1' | 'Q2' | 'Q3' |
--------+-------+------+------+------+------+------+
Canada	| BC	| 2001 | 0    | null | null | 10   |
--------+-------+------+------+------+------+------+
USA 	| NY	| 2001 | 25   | 45   | null | null |
--------+-------+------+------+------+------+------+
Canada 	| ON 	| 2001 | 0    | null | 10   | null |
--------+-------+------+------+------+------+------+
USA 	| CA 	| 2001 | 20   | null | 50   | null |
--------+-------+------+------+------+------+------+
USA 	| CA 	| 2001 | 15   | 30   | null | null |
--------+-------+------+------+------+------+------+
```

Copy

##### *Snowflake*[¶](#id114 "Link to this heading")

##### Query[¶](#id115 "Link to this heading")

```
 SELECT
	*
FROM
	star1 PIVOT(
	SUM(sales) FOR qtr IN ('Q1',
	   	'Q2',
	       'Q3'))Tmp;
```

Copy

##### Result[¶](#id116 "Link to this heading")

```
Country | State | yr   | cogs | 'Q1' | 'Q2' | 'Q3' |
--------+-------+------+------+------+------+------+
Canada	| BC	| 2001 | 0    | null | null | 10   |
--------+-------+------+------+------+------+------+
USA 	| NY	| 2001 | 25   | 45   | null | null |
--------+-------+------+------+------+------+------+
Canada 	| ON 	| 2001 | 0    | null | 10   | null |
--------+-------+------+------+------+------+------+
USA 	| CA 	| 2001 | 20   | null | 50   | null |
--------+-------+------+------+------+------+------+
USA 	| CA 	| 2001 | 15   | 30   | null | null |
--------+-------+------+------+------+------+------+
```

Copy

#### PIVOT with aliases transformation[¶](#pivot-with-aliases-transformation "Link to this heading")

##### *Teradata*[¶](#id117 "Link to this heading")

##### Query[¶](#id118 "Link to this heading")

```
 SELECT *
FROM star1 PIVOT (
	SUM(sales) as ss1 FOR qtr                                                                                               
    IN ('Q1' AS Quarter1,                                                                                                     
    	'Q2' AS Quarter2, 
        'Q3' AS Quarter3)
)Tmp;
```

Copy

##### Result[¶](#id119 "Link to this heading")

```
Country | State | yr   | cogs | Quarter1_ss1 | Quarter2_ss1 | Quarter3_ss1 |
--------+-------+------+------+--------------+--------------+--------------+
Canada	| BC	| 2001 | 0    | null 	     | null         | 10           |
--------+-------+------+------+--------------+--------------+--------------+
USA 	| NY	| 2001 | 25   | 45 	     | null 	    | null         |
--------+-------+------+------+--------------+--------------+--------------+
Canada 	| ON 	| 2001 | 0    | null 	     | 10 	    | null 	   |
--------+-------+------+------+--------------+--------------+--------------+
USA 	| CA 	| 2001 | 20   | null         | 50           | null         |
--------+-------+------+------+--------------+--------------+--------------+
USA 	| CA 	| 2001 | 15   | 30           | null         | null         |
--------+-------+------+------+--------------+--------------+--------------+
```

Copy

##### *Snowflake*[¶](#id120 "Link to this heading")

##### Query[¶](#id121 "Link to this heading")

```
 SELECT
	*
FROM
	!!!RESOLVE EWI!!! /*** SSC-EWI-0015 - PIVOT/UNPIVOT RENAME COLUMN NOT SUPPORTED ***/!!!
	star1 PIVOT(
	SUM(sales) FOR qtr IN (
	                       !!!RESOLVE EWI!!! /*** SSC-EWI-0015 - PIVOT/UNPIVOT RENAME COLUMN NOT SUPPORTED ***/!!!
	                       'Q1',
	!!!RESOLVE EWI!!! /*** SSC-EWI-0015 - PIVOT/UNPIVOT RENAME COLUMN NOT SUPPORTED ***/!!!
	   	'Q2',
	!!!RESOLVE EWI!!! /*** SSC-EWI-0015 - PIVOT/UNPIVOT RENAME COLUMN NOT SUPPORTED ***/!!!
	       'Q3'))Tmp;
```

Copy

##### Result[¶](#id122 "Link to this heading")

```
 Country | State | yr   | cogs | Quarter1_ss1 | Quarter2_ss1 | Quarter3_ss1 |
--------+-------+------+------+--------------+--------------+--------------+
Canada	| BC	| 2001 | 0    | null 	     | null         | 10           |
--------+-------+------+------+--------------+--------------+--------------+
USA 	| NY	| 2001 | 25   | 45 	     | null 	    | null         |
--------+-------+------+------+--------------+--------------+--------------+
Canada 	| ON 	| 2001 | 0    | null 	     | 10 	    | null 	   |
--------+-------+------+------+--------------+--------------+--------------+
USA 	| CA 	| 2001 | 20   | null         | 50           | null         |
--------+-------+------+------+--------------+--------------+--------------+
USA 	| CA 	| 2001 | 15   | 30           | null         | null         |
--------+-------+------+------+--------------+--------------+--------------+
```

Copy

### Known Issues[¶](#id123 "Link to this heading")

**1. WITH clause not supported**

Using the WITH clause is not currently supported.

**2. Pivot over multiple pivot columns not supported**

SnowConvert AI is transforming the PIVOT function into the PIVOT function in Snowflake, which only supports applying the function over a single column.

**3. Pivot with multiple aggregate functions not supported**

The PIVOT function in Snowflake only supports applying one aggregate function over the data.

**4. Subquery in the IN clause not supported**

The IN clause of the Snowflake PIVOT function does not accept subqueries.

**5. Aliases only supported if all IN clause elements have it and table specification is present**

For the column names with aliases to be equivalent, SnowConvert AI requires that all the values specified in the IN clause have one alias specified and the table specification is present in the input code, this is necessary so SnowConvert AI can successfully create the alias list for the resulting table.

### Related EWIs[¶](#id124 "Link to this heading")

1. [SSC-EWI-0015](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0015): The input pivot/unpivot statement form is not supported

## RANK[¶](#rank "Link to this heading")

Translation specification for the transformation of the RANK() function

### Description[¶](#id125 "Link to this heading")

RANK sorts a result set and identifies the numeric rank of each row in the result. The only argument for RANK is the sort column or columns, and the function returns an integer that represents the rank of each row in the result. ([RANK in Teradata](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/SQL-Functions-Expressions-and-Predicates/Ordered-Analytical/Window-Aggregate-Functions/RANK-Teradata))

#### Teradata syntax[¶](#teradata-syntax "Link to this heading")

```
 RANK ( sort_expression [ ASC | DESC ] [,...] )
```

Copy

#### Snowflake syntax[¶](#snowflake-syntax "Link to this heading")

```
 RANK() OVER 
( 
    [ PARTITION BY <expr1> ]
    ORDER BY <expr2> [ { ASC | DESC } ] 
    [ <window_frame> ]
)
```

Copy

### Sample Source Pattern[¶](#id126 "Link to this heading")

#### Setup data[¶](#id127 "Link to this heading")

##### Teradata[¶](#id128 "Link to this heading")

##### Query[¶](#id129 "Link to this heading")

```
 CREATE TABLE Sales (
  Product VARCHAR(255),
  Sales INT
);

INSERT INTO Sales (Product, Sales) VALUES ('A', 100);
INSERT INTO Sales (Product, Sales) VALUES ('B', 150);
INSERT INTO Sales (Product, Sales) VALUES ('C', 200);
INSERT INTO Sales (Product, Sales) VALUES ('D', 150);
INSERT INTO Sales (Product, Sales) VALUES ('E', 120);
INSERT INTO Sales (Product, Sales) VALUES ('F', NULL);
```

Copy

##### Snowflake[¶](#id130 "Link to this heading")

##### Query[¶](#id131 "Link to this heading")

```
 CREATE OR REPLACE TABLE Sales (
  Product VARCHAR(255),
  Sales INT
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;

INSERT INTO Sales (Product, Sales)
VALUES ('A', 100);

INSERT INTO Sales (Product, Sales)
VALUES ('B', 150);

INSERT INTO Sales (Product, Sales)
VALUES ('C', 200);

INSERT INTO Sales (Product, Sales)
VALUES ('D', 150);

INSERT INTO Sales (Product, Sales)
VALUES ('E', 120);

INSERT INTO Sales (Product, Sales)
VALUES ('F', NULL);
```

Copy

#### RANK() using ASC, DESC, and DEFAULT order[¶](#rank-using-asc-desc-and-default-order "Link to this heading")

##### Teradata[¶](#id132 "Link to this heading")

Warning

Notice that Teradata’s ordering default value when calling RANK() is DESC. However, the default in Snowflake is ASC. Thus, DESC is added in the conversion of RANK() when no order is specified.

##### Query[¶](#id133 "Link to this heading")

```
 SELECT
  Sales,
  RANK(Sales ASC) AS SalesAsc,
  RANK(Sales DESC) AS SalesDesc,
  RANK(Sales) AS SalesDefault
FROM
  Sales;
```

Copy

##### Result[¶](#id134 "Link to this heading")

| SALES | SALESASC | SALESDESC | SALESDEFAULT |
| --- | --- | --- | --- |
| NULL | 6 | 6 | 6 |
| 200 | 5 | 1 | 1 |
| 150 | 3 | 2 | 2 |
| 150 | 3 | 2 | 2 |
| 120 | 2 | 4 | 4 |
| 100 | 1 | 5 | 5 |

##### Snowflake[¶](#id135 "Link to this heading")

##### Query[¶](#id136 "Link to this heading")

```
 SELECT
  Sales,
  RANK() OVER (
  ORDER BY
    Sales ASC) AS SalesAsc,
    RANK() OVER (
    ORDER BY
    Sales DESC NULLS LAST) AS SalesDesc,
    RANK() OVER (
    ORDER BY
    Sales DESC NULLS LAST) AS SalesDefault
    FROM
    Sales;
```

Copy

##### Result[¶](#id137 "Link to this heading")

| SALES | SALESASC | SALESDESC | SALESDEFAULT |
| --- | --- | --- | --- |
| NULL | 6 | 6 | 6 |
| 200 | 5 | 1 | 1 |
| 150 | 3 | 2 | 2 |
| 150 | 3 | 2 | 2 |
| 120 | 2 | 4 | 4 |
| 100 | 1 | 5 | 5 |

### Known Issues [¶](#id138 "Link to this heading")

No issues were found.

### Related EWIs [¶](#id139 "Link to this heading")

No related EWIs.

## Regex functions[¶](#id140 "Link to this heading")

### Description[¶](#id141 "Link to this heading")

Both Teradata and Snowflake offer support for functions that apply regular expressions over varchar inputs. See the [Teradata documentation](https://docs.teradata.com/r/Teradata-VantageTM-SQL-Functions-Expressions-and-Predicates/March-2019/Regular-Expression-Functions) and [Snowflake documentation](https://docs.snowflake.com/en/sql-reference/functions-regexp.html) for more details.

```
REGEXP_SUBSTR(source. regexp [, position, occurrence, match])
REGEXP_REPLACE(source. regexp [, replace_string, position, occurrence, match])
REGEXP_INSTR(source. regexp [, position, occurrence, return_option, match])
REGEXP_SIMILAR(source. regexp [, match])
REGEXP_SPLIT_TO_TABLE(inKey. source. regexp, match)
```

Copy

### Sample Source Patterns[¶](#id142 "Link to this heading")

#### Setup data[¶](#id143 "Link to this heading")

##### Teradata[¶](#id144 "Link to this heading")

**Query**

```
CREATE TABLE regexpTable
(
    col1 CHAR(35)
);

INSERT INTO regexpTable VALUES('hola');
```

Copy

##### *Snowflake*[¶](#id145 "Link to this heading")

**Query**

```
CREATE OR REPLACE TABLE regexpTable
(
    col1 CHAR(35)
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;

INSERT INTO regexpTable
VALUES ('hola');
```

Copy

#### Regex transformation example[¶](#regex-transformation-example "Link to this heading")

##### *Teradata*[¶](#id146 "Link to this heading")

**Query**

```
SELECT
REGEXP_REPLACE(col1,'.*(h(i|o))','ha', 1, 0, 'x'),
REGEXP_SUBSTR(COL1,'.*(h(i|o))', 2, 1, 'x'),
REGEXP_INSTR(COL1,'.*(h(i|o))',1, 1, 0, 'x'),
REGEXP_SIMILAR(COL1,'.*(h(i|o))', 'xl')
FROM regexpTable;
```

Copy



**Result**

```
COLUMN1|COLUMN2|COLUMN3|COLUMN4|
-------+-------+-------+-------+
hala   |null   |1      |0      |
```

Copy

##### *Snowflake*[¶](#id147 "Link to this heading")

**Query**

```
--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "regexpTable" **
SELECT
REGEXP_REPLACE(col1, '.*(h(i|o))', 'ha', 1, 0),
REGEXP_SUBSTR(COL1, '.*(h(i|o))', 2, 1),
REGEXP_INSTR(COL1, '.*(h(i|o))', 1, 1, 0),
--** SSC-FDM-TD0016 - VALUE 'l' FOR PARAMETER 'match_arg' IS NOT SUPPORTED IN SNOWFLAKE **
REGEXP_LIKE(COL1, '.*(h(i|o))')
FROM
regexpTable;
```

Copy



**Result**

```
COLUMN1|COLUMN2|COLUMN3|COLUMN4|
-------+-------+-------+-------+
hala   |null   |1      |FALSE  |
```

Copy

### Known Issues[¶](#id148 "Link to this heading")

**1. Snowflake only supports POSIX regular expressions**

The user will be warned when SnowConvert AI finds a non-POSIX regular expression.

**2. Teradata “match\_arg” option ‘l’ is unsupported in Snowflake**

The option ‘l’ has no counterpart in Snowflake and the user will be warned if SnowConvert AI finds them.

**3. Fixed size of the CHAR datatype may cause different behavior**

Some regex functions in Teradata will try to match the whole column of CHAR datatype in a table even if some of the characters in the column were left empty due to a smaller string being inserted. In Snowflake this does not happen because the CHAR datatype is of variable size.

**4. REGEXP\_SPLIT\_TO\_TABLE not supported**

The function is currently not supported by Snowflake.

### Related EWIs[¶](#id149 "Link to this heading")

1. [SSC-FDM-0007](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0007): Element with missing dependencies.
2. [SSC-FDM-TD0016](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/teradataFDM.html#ssc-fdm-td0016): Value ‘l’ for parameter ‘match\_arg’ is not supported in Snowflake.

## STRTOK\_SPLIT\_TO\_TABLE[¶](#strtok-split-to-table "Link to this heading")

### Description[¶](#id150 "Link to this heading")

Split a string into a table using the provided delimiters. For more information check [STRTOK\_SPLIT\_TO\_TABLE](https://docs.teradata.com/r/Teradata-VantageTM-SQL-Functions-Expressions-and-Predicates-17.20/String-Operators-and-Functions/STRTOK_SPLIT_TO_TABLE).

```
[TD_SYSFNLIB.] STRTOK_SPLIT_TO_TABLE ( inkey, instring, delimiters )
  RETURNS ( outkey, tokennum, token )
```

Copy

### Sample Source Patterns[¶](#id151 "Link to this heading")

#### Setup data[¶](#id152 "Link to this heading")

##### Teradata[¶](#id153 "Link to this heading")

**Query**

```
CREATE TABLE strtokTable
(
	col1 INTEGER,
	col2 VARCHAR(100)
);

INSERT INTO strtokTable VALUES(4, 'hello-world-split-me');
INSERT INTO strtokTable VALUES(1, 'string$split$by$dollars');
```

Copy

##### *Snowflake*[¶](#id154 "Link to this heading")

**Query**

```
CREATE OR REPLACE TABLE strtokTable
(
	col1 INTEGER,
	col2 VARCHAR(100)
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;

INSERT INTO strtokTable
VALUES (4, 'hello-world-split-me');

INSERT INTO strtokTable
VALUES (1, 'string$split$by$dollars');
```

Copy

#### STRTOK\_SPLIT\_TO\_TABLE transformation[¶](#strtok-split-to-table-transformation "Link to this heading")

##### *Teradata*[¶](#id155 "Link to this heading")

**Query**

```
SELECT outkey, tokennum, token FROM table(STRTOK_SPLIT_TO_TABLE(strtokTable.col1, strtokTable.col2, '-$')
RETURNS (outkey INTEGER, tokennum INTEGER, token VARCHAR(100))) AS testTable
ORDER BY outkey, tokennum;
```

Copy



**Result**

```
outkey |tokennum | token  |
-------+---------+--------+
1      |1        |string  |
-------+---------+--------+
1      |2        |split   |
-------+---------+--------+
1      |3        |by      |
-------+---------+--------+
1      |4        |dollars |
-------+---------+--------+
4      |1        |hello   |
-------+---------+--------+
4      |2        |world   |
-------+---------+--------+
4      |3        |split   |
-------+---------+--------+
4      |4        |me      |
```

Copy

##### *Snowflake*[¶](#id156 "Link to this heading")

**Query**

```
SELECT
CAST(strtokTable.col1 AS INTEGER) AS outkey,
CAST(INDEX AS INTEGER) AS tokennum,
CAST(VALUE AS VARCHAR) AS token
FROM
strtokTable,
table(STRTOK_SPLIT_TO_TABLE(strtokTable.col2, '-$')) AS testTable
ORDER BY outkey, tokennum;
```

Copy



**Result**

```
outkey |tokennum | token  |
-------+---------+--------+
1      |1        |string  |
-------+---------+--------+
1      |2        |split   |
-------+---------+--------+
1      |3        |by      |
-------+---------+--------+
1      |4        |dollars |
-------+---------+--------+
4      |1        |hello   |
-------+---------+--------+
4      |2        |world   |
-------+---------+--------+
4      |3        |split   |
-------+---------+--------+
4      |4        |me      |
```

Copy

### Known Issues[¶](#id157 "Link to this heading")

No known issues.

### Related EWIs [¶](#id158 "Link to this heading")

No related EWIs.

## SUBSTRING[¶](#substring "Link to this heading")

### Description[¶](#id159 "Link to this heading")

Extracts a substring from a given input string. For more information check [SUBSTRING/SUBSTR.](https://docs.teradata.com/r/kmuOwjp1zEYg98JsB8fu_A/lxOd~YrdVkJGt0_anAEXFQ)

```
SUBSTRING(string_expr FROM n1 [FOR n2])

SUBSTR(string_expr, n1, [, n2])
```

Copy

When the value to start getting the substring (n1) is less than one SUBSTR\_UDF is inserted instead.

### Sample Source Patterns[¶](#id160 "Link to this heading")

#### SUBSTRING transformation[¶](#substring-transformation "Link to this heading")

##### *Teradata*[¶](#id161 "Link to this heading")

**Query**

```
SELECT SUBSTR('Hello World!', 2, 6),
SUBSTR('Hello World!', -2, 6),
SUBSTRING('Hello World!' FROM 2 FOR 6),
SUBSTRING('Hello World!' FROM -2 FOR 6);
```

Copy



**Result**

```
COLUMN1 |COLUMN2 |COLUMN3 | COLUMN4 |
--------+--------+--------+---------+
ello W  |Hel     |ello W  |Hel      |
```

Copy

##### *Snowflake*[¶](#id162 "Link to this heading")

**Query**

```
SELECT
SUBSTR('Hello World!', 2, 6),
PUBLIC.SUBSTR_UDF('Hello World!', -2, 6),
SUBSTRING('Hello World!', 2, 6),
PUBLIC.SUBSTR_UDF('Hello World!', -2, 6);
```

Copy



**Result**

```
COLUMN1 |COLUMN2 |COLUMN3 | COLUMN4 |
--------+--------+--------+---------+
ello W  |Hel     |ello W  |Hel      |
```

Copy

### Related EWIs[¶](#id163 "Link to this heading")

No related EWIs.

## TD\_UNPIVOT[¶](#td-unpivot "Link to this heading")

Translation specification for the transformation of TD\_UNPIVOT into an equivalent query in Snowflake

Note

Some parts in the output code are omitted for clarity reasons.

### Description[¶](#id164 "Link to this heading")

`TD_UNPIVOT` in Teradata can unpivot multiple columns at once, while Snowflake `UNPIVOT` can only unpivot a single column\*\*.\*\* The *unpivot* functionality is used to transform columns of the specified table into rows. For more information see [TD\_UNPIVOT](https://docs.teradata.com/r/Teradata-VantageTM-SQL-Operators-and-User-Defined-Functions-17.20/Table-Operators/TD_UNPIVOT).

```
[TD_SYSFNLIB.] TD_UNPIVOT (
  ON { tableName | ( query_expression ) }
  USING VALUE_COLUMNS ( 'value_columns_value' [,...] )
  UNPIVOT_COLUMN ( 'unpivot_column_value' )
  COLUMN_LIST ( 'column_list_value' [,...] )
  [ COLUMN_ALIAS_LIST ( 'column_alias_list_value' [,...] )
      INCLUDE_NULLS ( { 'No' | 'Yes' } )
  ]
)
```

Copy

The following transformation is able to generate a SQL query in Snowflake that unpivots multiple columns at the same time, the same way it works in Teradata.

### Sample Source Patterns[¶](#id165 "Link to this heading")

#### Setup data title[¶](#setup-data-title "Link to this heading")

##### Teradata[¶](#id166 "Link to this heading")

##### Query[¶](#id167 "Link to this heading")

```
 CREATE TABLE superunpivottest (
	myKey INTEGER NOT NULL PRIMARY KEY,
	firstSemesterIncome DECIMAL(10,2),
	secondSemesterIncome DECIMAL(10,2),
	firstSemesterExpenses DECIMAL(10,2),
	secondSemesterExpenses DECIMAL(10,2)
);

INSERT INTO superUnpivottest VALUES (2020, 15440, 25430.57, 10322.15, 12355.36);
INSERT INTO superUnpivottest VALUES (2018, 18325.25, 25220.65, 15560.45, 15680.33);
INSERT INTO superUnpivottest VALUES (2019, 23855.75, 34220.22, 14582.55, 24122);
```

Copy

##### *Snowflake*[¶](#id168 "Link to this heading")

##### Query[¶](#id169 "Link to this heading")

```
 CREATE OR REPLACE TABLE superunpivottest (
	myKey INTEGER NOT NULL PRIMARY KEY,
	firstSemesterIncome DECIMAL(10,2),
	secondSemesterIncome DECIMAL(10,2),
	firstSemesterExpenses DECIMAL(10,2),
	secondSemesterExpenses DECIMAL(10,2)
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;

INSERT INTO superUnpivottest
VALUES (2020, 15440, 25430.57, 10322.15, 12355.36);

INSERT INTO superUnpivottest
VALUES (2018, 18325.25, 25220.65, 15560.45, 15680.33);

INSERT INTO superUnpivottest
VALUES (2019, 23855.75, 34220.22, 14582.55, 24122);
```

Copy

#### TD\_UNPIVOT transformation[¶](#td-unpivot-transformation "Link to this heading")

##### *Teradata*[¶](#id170 "Link to this heading")

##### Query[¶](#id171 "Link to this heading")

```
 SELECT * FROM
 TD_UNPIVOT(
 	ON superunpivottest
 	USING
 	VALUE_COLUMNS('Income', 'Expenses')
 	UNPIVOT_COLUMN('Semester')
 	COLUMN_LIST('firstSemesterIncome, firstSemesterExpenses', 'secondSemesterIncome, secondSemesterExpenses')
    COLUMN_ALIAS_LIST('First', 'Second')
 )X ORDER BY mykey, Semester;
```

Copy

##### Result[¶](#id172 "Link to this heading")

```
myKey |Semester |Income   | Expenses |
------+---------+---------+----------+
2018  |First    |18325.25 |15560.45  |
------+---------+---------+----------+
2018  |Second   |25220.65 |15680.33  |
------+---------+---------+----------+
2019  |First    |23855.75 |14582.55  |
------+---------+---------+----------+
2019  |Second   |34220.22 |24122.00  |
------+---------+---------+----------+
2020  |First    |15440.00 |10322.15  |
------+---------+---------+----------+
2020  |Second   |25430.57 |12355.36  |
```

Copy

##### *Snowflake*[¶](#id173 "Link to this heading")

##### Query[¶](#id174 "Link to this heading")

```
 SELECT
 * FROM
 !!!RESOLVE EWI!!! /*** SSC-EWI-TD0061 - TD_UNPIVOT TRANSFORMATION REQUIRES COLUMN INFORMATION THAT COULD NOT BE FOUND, COLUMNS MISSING IN RESULT ***/!!!
 (
  SELECT
   TRIM(GET_IGNORE_CASE(OBJECT_CONSTRUCT('FIRSTSEMESTERINCOME', 'First', 'FIRSTSEMESTEREXPENSES', 'First', 'SECONDSEMESTERINCOME', 'Second', 'SECONDSEMESTEREXPENSES', 'Second'), Semester), '"') AS Semester,
   Income,
   Expenses
  FROM
   superunpivottest UNPIVOT(Income FOR Semester IN (
    firstSemesterIncome,
    secondSemesterIncome
   )) UNPIVOT(Expenses FOR Semester1 IN (
    firstSemesterExpenses,
    secondSemesterExpenses
   ))
  WHERE
   Semester = 'FIRSTSEMESTERINCOME'
   AND Semester1 = 'FIRSTSEMESTEREXPENSES'
   OR Semester = 'SECONDSEMESTERINCOME'
   AND Semester1 = 'SECONDSEMESTEREXPENSES'
 ) X ORDER BY mykey, Semester;
```

Copy

##### Result[¶](#id175 "Link to this heading")

```
myKey |Semester |Income   | Expenses |
------+---------+---------+----------+
2018  |First    |18325.25 |15560.45  |
------+---------+---------+----------+
2018  |Second   |25220.65 |15680.33  |
------+---------+---------+----------+
2019  |First    |23855.75 |14582.55  |
------+---------+---------+----------+
2019  |Second   |34220.22 |24122.00  |
------+---------+---------+----------+
2020  |First    |15440.00 |10322.15  |
------+---------+---------+----------+
2020  |Second   |25430.57 |12355.36  |
```

Copy

### Known Issues[¶](#id176 "Link to this heading")

1. **TD\_UNPIVOT with INCLUDE\_NULLS clause set to YES is not supported**

Snowflake UNPIVOT function used in the transformation will ignore null values always, and the user will be warned that the INCLUDE\_NULLS clause is not supported when it is set to YES.

2. **Table information is required to correctly transform the function**

SnowConvert AI needs the name of the columns that are being used in the TD\_UNPIVOT function; if the user does not include the columns list in the query\_expression of the function but provides the name of the table being unpivoted, then it will try to retrieve the column names from the table definition. If the names can not be found then the user will be warned that the resulting query might be losing columns in the result.

### Related EWIs[¶](#id177 "Link to this heading")

1. [SSC-EWI-TD0061](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/teradataEWI.html#ssc-ewi-td0061): TD\_UNPIVOT transformation requires column information that could not be found, columns missing in result.

## TO\_CHAR[¶](#to-char "Link to this heading")

### Description[¶](#id178 "Link to this heading")

The TO\_CHAR function casts a DateTime or numeric value to a string. For more information check [TO\_CHAR(Numeric)](https://docs.teradata.com/r/kmuOwjp1zEYg98JsB8fu_A/4xbLyOA_385QLYctkj~hjw) and [TO\_CHAR(DateTime)](https://docs.teradata.com/r/kmuOwjp1zEYg98JsB8fu_A/he2a_fFPveMN9cjMlF3Tqg).

```
-- Numeric version
[TD_SYSFNLIB.]TO_CHAR(numeric_expr [, format_arg [, nls_param]])

-- DateTime version
[TD_SYSFNLIB.]TO_CHAR(dateTime_expr [, format_arg])
```

Copy

Both Snowflake and Teradata have their own version of the TO\_CHAR function, however, Teradata supports plenty of formats that are not natively supported by Snowflake. To support these format elements SnowConvert AI uses Snowflake built-in functions and custom UDFs to generate a concatenation expression that produces the same string as the original TO\_CHAR function in Teradata.

### Sample Source Patterns[¶](#id179 "Link to this heading")

#### TO\_CHAR(DateTime) transformation[¶](#to-char-datetime-transformation "Link to this heading")

##### *Teradata*[¶](#id180 "Link to this heading")

**Query**

```
SELECT 
TO_CHAR(date '2012-12-23'),
TO_CHAR(date '2012-12-23', 'DS'),
TO_CHAR(date '2012-12-23', 'DAY DD, MON YY');
```

Copy



**Result**

```
COLUMN1    | COLUMN2    | COLUMN3           |
-----------+------------+-------------------+
2012/12/23 | 12/23/2012 | SUNDAY 23, DEC 12 |
```

Copy

##### *Snowflake*[¶](#id181 "Link to this heading")

**Query**

```
SELECT
TO_CHAR(date '2012-12-23') /*** SSC-FDM-TD0029 - SNOWFLAKE SUPPORTED FORMATS FOR TO_CHAR DIFFER FROM TERADATA AND MAY FAIL OR HAVE DIFFERENT BEHAVIOR ***/,
TO_CHAR(date '2012-12-23', 'MM/DD/YYYY') /*** SSC-FDM-TD0029 - SNOWFLAKE SUPPORTED FORMATS FOR TO_CHAR DIFFER FROM TERADATA AND MAY FAIL OR HAVE DIFFERENT BEHAVIOR ***/,
PUBLIC.DAYNAME_LONG_UDF(date '2012-12-23', 'uppercase') || TO_CHAR(date '2012-12-23', ' DD, ') || PUBLIC.MONTH_SHORT_UDF(date '2012-12-23', 'uppercase') || TO_CHAR(date '2012-12-23', ' YY') /*** SSC-FDM-TD0029 - SNOWFLAKE SUPPORTED FORMATS FOR TO_CHAR DIFFER FROM TERADATA AND MAY FAIL OR HAVE DIFFERENT BEHAVIOR ***/;
```

Copy



**Result**

```
COLUMN1    | COLUMN2    | COLUMN3           |
-----------+------------+-------------------+
2012/12/23 | 12/23/2012 | SUNDAY 23, DEC 12 |
```

Copy

#### TO\_CHAR(Numeric) transformation[¶](#to-char-numeric-transformation "Link to this heading")

##### *Teradata*[¶](#id182 "Link to this heading")

**Query**

```
SELECT
TO_CHAR(1255.495),
TO_CHAR(1255.495, '9.9EEEE'),
TO_CHAR(1255.495, 'SC9999.9999', 'nls_iso_currency = ''EUR''');
```

Copy



**Result**

```
COLUMN1  | COLUMN2 | COLUMN3       |
---------+---------+---------------+
1255.495 | 1.3E+03 | +EUR1255.4950 |
```

Copy

##### *Snowflake*[¶](#id183 "Link to this heading")

**Query**

```
SELECT
TO_CHAR(1255.495) /*** SSC-FDM-TD0029 - SNOWFLAKE SUPPORTED FORMATS FOR TO_CHAR DIFFER FROM TERADATA AND MAY FAIL OR HAVE DIFFERENT BEHAVIOR ***/,
TO_CHAR(1255.495, '9.0EEEE') /*** SSC-FDM-TD0029 - SNOWFLAKE SUPPORTED FORMATS FOR TO_CHAR DIFFER FROM TERADATA AND MAY FAIL OR HAVE DIFFERENT BEHAVIOR ***/,
PUBLIC.INSERT_CURRENCY_UDF(TO_CHAR(1255.495, 'S9999.0000'), 2, 'EUR') /*** SSC-FDM-TD0029 - SNOWFLAKE SUPPORTED FORMATS FOR TO_CHAR DIFFER FROM TERADATA AND MAY FAIL OR HAVE DIFFERENT BEHAVIOR ***/;
```

Copy



**Result**

```
COLUMN1  | COLUMN2 | COLUMN3       |
---------+---------+---------------+
1255.495 | 1.3E+03 | +EUR1255.4950 |
```

Copy

### Known Issues[¶](#id184 "Link to this heading")

**1. Formats with different or unsupported behaviors**

Teradata offers an extensive list of format elements that may show different behavior in Snowflake after the transformation of the TO\_CHAR function. For the list of elements with different or unsupported behaviors check [SSC-EWI-TD0029](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/teradataEWI.html#ssc-ewi-td0029).

### Related EWIs[¶](#id185 "Link to this heading")

1. [SSC-FDM-TD0029](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/teradataFDM.html#ssc-fdm-td0029): Snowflake supported formats for TO\_CHAR differ from Teradata and may fail or have different behavior.

## XMLAGG[¶](#xmlagg "Link to this heading")

### Description[¶](#id186 "Link to this heading")

Construct an XML value by performing an aggregation of multiple rows. For more information check [XMLAGG](https://docs.teradata.com/r/Teradata-VantageTM-XML-Data-Type/June-2020/Functions-for-XML-Type-and-XQuery/XMLAGG).

```
XMLAGG (
  XML_value_expr
  [ ORDER BY order_by_spec [,...] ]
  [ RETURNING { CONTENT | SEQUENCE } ]
)

order_by_spec := sort_key [ ASC | DESC ] [ NULLS { FIRST | LAST } ]
```

Copy

### Sample Source Patterns[¶](#id187 "Link to this heading")

#### Setup data[¶](#id188 "Link to this heading")

##### Teradata[¶](#id189 "Link to this heading")

**Query**

```
create table orders (
	o_orderkey int, 
	o_totalprice float);

insert into orders values (1,500000);
insert into orders values (2,100000);
insert into orders values (3,600000);
insert into orders values (4,700000);
```

Copy

##### *Snowflake*[¶](#id190 "Link to this heading")

**Query**

```
CREATE OR REPLACE TABLE orders (
	o_orderkey int,
	o_totalprice float)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;

INSERT INTO orders
VALUES (1,500000);

INSERT INTO orders
VALUES (2,100000);

INSERT INTO orders
VALUES (3,600000);

INSERT INTO orders
VALUES (4,700000);
```

Copy

#### XMLAGG transformation[¶](#xmlagg-transformation "Link to this heading")

##### *Teradata*[¶](#id191 "Link to this heading")

**Query**

```
select 
    xmlagg(o_orderkey order by o_totalprice desc) (varchar(10000))
from orders
where o_totalprice > 5;
```

Copy



**Result**

```
COLUMN1 |
--------+
4 3 1 2 |
```

Copy

##### *Snowflake*[¶](#id192 "Link to this heading")

**Query**

```
SELECT
    LEFT(TO_VARCHAR(LISTAGG ( o_orderkey, ' ')
    WITHIN GROUP(
 order by o_totalprice DESC NULLS LAST)), 10000)
    from
    orders
    where o_totalprice > 5;
```

Copy



**Result**

```
COLUMN1 |
--------+
4 3 1 2 |
```

Copy

### Known Issues[¶](#id193 "Link to this heading")

**1. The RETURNING clause is currently not supported.**

The user will be warned that the translation of the returning clause will be added in the future.

### Related EWIs [¶](#id194 "Link to this heading")

No related EWIs.

## CAST[¶](#cast "Link to this heading")

## Cast from Number Datatypes to Varchar Datatype[¶](#cast-from-number-datatypes-to-varchar-datatype "Link to this heading")

Teradata when casts to varchar uses default formats for each number datatype, so SnowConvert AI adds formats to keep the equivalence among platforms.

### Sample Source Patterns[¶](#id195 "Link to this heading")

#### BYTEINT[¶](#byteint "Link to this heading")

##### *Teradata*[¶](#id196 "Link to this heading")

**Query**

```
SELECT '"'||cast(cast(12 as BYTEINT) as varchar(10))||'"';
```

Copy



**Result**

```
(('"'||12)||'"')|
----------------+
"12"            |
```

Copy

##### *Snowflake*[¶](#id197 "Link to this heading")

**Query**

```
SELECT
'"'|| LEFT(TO_VARCHAR(cast(12 as BYTEINT), 'TM'), 10) ||'"';
```

Copy



**Result**

```
"'""'|| LEFT(TO_VARCHAR(CAST(12 AS BYTEINT), 'TM'), 10) ||'""'"
---------------------------------------------------------------
"12"
```

Copy

#### SMALLINT[¶](#smallint "Link to this heading")

##### *Teradata*[¶](#id198 "Link to this heading")

**Query**

```
SELECT '"'||cast(cast(123 as SMALLINT) as varchar(10))||'"';
```

Copy



**Result**

```
(('"'||123)||'"')|
-----------------+
"123"            |
```

Copy

##### *Snowflake*[¶](#id199 "Link to this heading")

**Query**

```
SELECT
'"'|| LEFT(TO_VARCHAR(CAST(123 AS SMALLINT), 'TM'), 10) ||'"';
```

Copy



**Result**

```
"'""'|| LEFT(TO_VARCHAR(CAST(123 AS SMALLINT), 'TM'), 10) ||'""'"
-----------------------------------------------------------------
"123"
```

#### INTEGER[¶](#integer "Link to this heading")

##### *Teradata*[¶](#id200 "Link to this heading")

**Query**

```
SELECT '"'||cast(cast(12345 as INTEGER) as varchar(10))||'"';
```

Copy



**Result**

```
(('"'||12345)||'"')|
-------------------+
"12345"            |
```

Copy

##### *Snowflake*[¶](#id201 "Link to this heading")

**Query**

```
SELECT
'"'|| LEFT(TO_VARCHAR(CAST(12345 AS INTEGER), 'TM'), 10) ||'"';
```

Copy



**Result**

```
"'""'|| LEFT(TO_VARCHAR(CAST(12345 AS INTEGER), 'TM'), 10) ||'""'"
------------------------------------------------------------------
"12345"
```

Copy

#### BIGINT[¶](#bigint "Link to this heading")

##### *Teradata*[¶](#id202 "Link to this heading")

**Query**

```
SELECT '"'||cast(cast(12345 as BIGINT) as varchar(10))||'"';
```

Copy



**Result**

```
(('"'||12345)||'"')|
-------------------+
"12345"            |
```

Copy

##### *Snowflake*[¶](#id203 "Link to this heading")

**Query**

```
SELECT
       '"'|| LEFT(TO_VARCHAR(CAST(12345 AS BIGINT), 'TM'), 10) ||'"';
```

Copy



**Result**

```
"'""'|| LEFT(TO_VARCHAR(CAST(12345 AS BIGINT), 'TM'), 10) ||'""'"
-----------------------------------------------------------------
"12345"
```

Copy

#### DECIMAL[(n[,m])] or NUMERIC[(n[,m])][¶](#decimal-n-m-or-numeric-n-m "Link to this heading")

##### *Teradata*[¶](#id204 "Link to this heading")

**Query**

```
SELECT '"'||cast(cast(12345 as DECIMAL) as varchar(10))||'"',
       '"'||cast(cast(12345 as DECIMAL(12, 2)) as varchar(10))||'"';
```

Copy



**Result**

```
(('"'||12345)||'"')|(('"'||12345)||'"')|
-------------------+-------------------+
"12345."           |"12345.00"         |
```

Copy

##### *Snowflake*[¶](#id205 "Link to this heading")

**Query**

```
SELECT
'"'|| LEFT(TO_VARCHAR(CAST(12345 AS DECIMAL), 'TM.'), 10) ||'"',
'"'|| LEFT(TO_VARCHAR(CAST(12345 AS DECIMAL(12, 2)), 'TM'), 10) ||'"';
```

Copy



**Result**

```
'"'|| LEFT(TO_VARCHAR(CAST(12345 AS DECIMAL), 'TM.'), 10) ||'"'	'"'|| LEFT(TO_VARCHAR(CAST(12345 AS DECIMAL(12, 2)), 'TM'), 10) ||'"'
"12345."	"12345.00"
```

### Known Issues [¶](#id206 "Link to this heading")

* Teradata treats the numbers between 0 and 1 differently than Snowflake. For those values, Teradata does not add the zero before the dot; meanwhile, Snowflake does.

#### *Teradata*[¶](#id207 "Link to this heading")

**Query**

```
SELECT '"'||cast(cast(-0.1 as DECIMAL(12, 2)) as varchar(10))||'"' AS column1,
       '"'||cast(cast(0.1 as DECIMAL(12, 2)) as varchar(10))||'"' AS column2;
```

Copy



**Result**

```
COLUMN1          |COLUMN2
-----------------+--------------+
"-.10"           |".10"         |
```

Copy

#### *Snowflake*[¶](#id208 "Link to this heading")

**Query**

```
SELECT
'"'|| LEFT(TO_VARCHAR(CAST(-0.1 AS DECIMAL(12, 2)), 'TM'), 10) ||'"' AS column1,
'"'|| LEFT(TO_VARCHAR(CAST(0.1 AS DECIMAL(12, 2)), 'TM'), 10) ||'"' AS column2;
```

Copy



**Result**

```
COLUMN1           |COLUMN2
------------------+---------------+
"-0.10"           |"0.10"         |
```

Copy

### Related EWIs [¶](#id209 "Link to this heading")

No related EWIs.

## Cast to DATE using { }[¶](#cast-to-date-using "Link to this heading")

### Description[¶](#id210 "Link to this heading")

The following syntax casts a date-formatted string to DATE datatype by putting a d before the string definition inside curly braces.

```
SELECT {d '1233-10-10'}
```

Copy

### Sample Source Patterns[¶](#id211 "Link to this heading")

#### Cast to DATE using curly braces[¶](#cast-to-date-using-curly-braces "Link to this heading")

**Teradata**

**Cast to Date**

```
SELECT * FROM RESOURCE_DETAILS where change_ts >= {d '2022-09-10'};
```

Copy



**Snowflake**

**Cast to Date**

```
SELECT
* FROM
PUBLIC.RESOURCE_DETAILS
where change_ts >= DATE('2022-09-10');
```

Copy

## Cast to INTERVAL datatype[¶](#cast-to-interval-datatype "Link to this heading")

### Description[¶](#id212 "Link to this heading")

Snowflake does not support the Interval data type, but it has INTERVAL constants that can be used in DateTime operations and other uses can be emulated using VARCHAR, SnowConvert AI will transform CAST functions to the INTERVAL datatype into an equivalent depending on the case:

* When the value being casted is of type interval an UDF will be generated to produce the new interval equivalent as a string
* When the value is a literal, an Snowflake interval constant will be generated if the cast is used in a datetime operation, otherwise a literal string will be generated
* When the value is non-literal then a cast to string will be generated

### Sample Source Patterns[¶](#id213 "Link to this heading")

#### Non-interval literals[¶](#non-interval-literals "Link to this heading")

##### *Teradata*[¶](#id214 "Link to this heading")

**Query**

```
SELECT TIMESTAMP '2022-10-15 10:30:00' + CAST ('12:34:56.78' AS INTERVAL HOUR(2) TO SECOND(2)) AS VARCHAR_TO_INTERVAL,
TIMESTAMP '2022-10-15 10:30:00' + CAST(-5 AS INTERVAL YEAR(4)) AS NUMBER_TO_INTERVAL,
CAST('07:00' AS INTERVAL HOUR(2) TO MINUTE) AS OUTSIDE_DATETIME_OPERATION;
```

Copy



**Result**

```
VARCHAR_TO_INTERVAL | NUMBER_TO_INTERVAL | OUTSIDE_DATETIME_OPERATION |
--------------------+--------------------+----------------------------+
2022-10-15 23:04:56 |2017-10-15 10:30:00 | 7:00                       |
```

Copy

##### *Snowflake*[¶](#id215 "Link to this heading")

**Query**

```
SELECT
TIMESTAMP '2022-10-15 10:30:00' + INTERVAL '12 HOUR, 34 MINUTE, 56 SECOND, 780000 MICROSECOND' AS VARCHAR_TO_INTERVAL,
TIMESTAMP '2022-10-15 10:30:00' + INTERVAL '-5 YEAR' AS NUMBER_TO_INTERVAL,
'07:00' AS OUTSIDE_DATETIME_OPERATION;
```

Copy



**Result**

```
VARCHAR_TO_INTERVAL     | NUMBER_TO_INTERVAL     | OUTSIDE_DATETIME_OPERATION |
------------------------+------------------------+----------------------------+
2022-10-15 23:04:56.780 |2017-10-15 10:30:00.000 | 07:00                      |
```

Copy

#### Non-literal and non-interval values[¶](#non-literal-and-non-interval-values "Link to this heading")

##### *Teradata*[¶](#id216 "Link to this heading")

**Query**

```
SELECT TIMESTAMP '2022-10-15 10:30:00' + CAST('20 ' || '10' AS INTERVAL DAY TO HOUR) AS DATETIME_OPERATION,
CAST('20 ' || '10' AS INTERVAL DAY TO HOUR) AS OUTSIDE_DATETIME_OPERATION;
```

Copy



**Result**

```
DATETIME_OPERATION  | OUTSIDE_DATETIME_OPERATION |
--------------------+----------------------------+
2022-11-04 20:30:00 | 20 10                      |
```

Copy

##### *Snowflake*[¶](#id217 "Link to this heading")

**Query**

```
SELECT
PUBLIC.DATETIMEINTERVALADD_UDF(TIMESTAMP '2022-10-15 10:30:00', CAST('20 ' || '10' AS VARCHAR(21)), 'DAY', '+') AS DATETIME_OPERATION,
CAST('20 ' || '10' AS VARCHAR(21)) AS OUTSIDE_DATETIME_OPERATION;
```

Copy



**Result**

```
DATETIME_OPERATION      | OUTSIDE_DATETIME_OPERATION |
------------------------+----------------------------+
2022-11-04 20:30:00.000 | 20 10                      |
```

Copy

#### Cast of interval to another interval[¶](#cast-of-interval-to-another-interval "Link to this heading")

##### *Teradata*[¶](#id218 "Link to this heading")

**Query**

```
SELECT
TIMESTAMP '2022-10-15 10:30:00' + CAST(INTERVAL '5999' MINUTE AS INTERVAL DAY TO HOUR) AS DATETIME_OPERATION,
CAST(INTERVAL '5999' MINUTE AS INTERVAL DAY TO HOUR) AS OUTSIDE_DATETIME_OPERATION;
```

Copy



**Result**

```
DATETIME_OPERATION  | OUTSIDE_DATETIME_OPERATION |
--------------------+----------------------------+
2022-10-19 13:30:00 | 4 03                       |
```

Copy

##### *Snowflake*[¶](#id219 "Link to this heading")

**Query**

```
SELECT
PUBLIC.DATETIMEINTERVALADD_UDF(
TIMESTAMP '2022-10-15 10:30:00', PUBLIC.INTERVALTOINTERVAL_UDF('5999', 'MINUTE', 'MINUTE', 'DAY', 'HOUR'), 'DAY', '+') AS DATETIME_OPERATION,
PUBLIC.INTERVALTOINTERVAL_UDF('5999', 'MINUTE', 'MINUTE', 'DAY', 'HOUR') AS OUTSIDE_DATETIME_OPERATION;
```

Copy



**Result**

```
DATETIME_OPERATION      | OUTSIDE_DATETIME_OPERATION |
------------------------+----------------------------+
2022-10-19 13:30:00.000 | 4 03                       |
```

Copy

### Known Issues[¶](#id220 "Link to this heading")

**No known issues.**

### Related EWIs[¶](#id221 "Link to this heading")

No related EWIs.

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

1. [Aggregate Functions](#aggregate-functions)
2. [Arithmetic, Trigonometric, Hyperbolic Operators/Functions](#arithmetic-trigonometric-hyperbolic-operators-functions)
3. [Attribute Functions](#attribute-functions)
4. [Bit/Byte Manipulation Functions](#bit-byte-manipulation-functions)
5. [Built-In (System Functions)](#built-in-system-functions)
6. [Business Calendars](#business-calendars)
7. [Calendar Functions](#calendar-functions)
8. [Case Functions](#case-functions)
9. [Comparison Functions](#comparison-functions)
10. [Data type conversions](#data-type-conversions)
11. [Data Type Conversion Functions](#data-type-conversion-functions)
12. [DateTime and Interval functions](#datetime-and-interval-functions)
13. [Hash functions](#hash-functions)
14. [JSON functions](#json-functions)
15. [Null-Handling functions](#null-handling-functions)
16. [Ordered Analytical/Window Aggregate functions](#ordered-analytical-window-aggregate-functions)
17. [Period functions and operators](#period-functions-and-operators)
18. [Query band functions](#query-band-functions)
19. [Regex functions](#regex-functions)
20. [String operators and functions](#string-operators-and-functions)
21. [St\_Point functions](#st-point-functions)
22. [Table operators](#table-operators)
23. [XML functions](#xml-functions)
24. [Extensibility UDFs](#extensibility-udfs)
25. [Notes](#notes)
26. [Known Issues](#known-issues)
27. [Related EWIs](#related-ewis)
28. [COALESCE](#coalesce)
29. [CURRENT\_TIMESTAMP](#current-timestamp)
30. [DAYNUMBER\_OF\_MONTH](#daynumber-of-month)
31. [FROM\_BYTES](#from-bytes)
32. [GETQUERYBANDVALUE](#getquerybandvalue)
33. [JSON\_CHECK](#json-check)
34. [JSON\_EXTRACT](#json-extract)
35. [JSON\_TABLE](#json-table)
36. [NEW JSON](#new-json)
37. [NVP](#nvp)
38. [OVERLAPS](#overlaps)
39. [P\_INTERSECT](#p-intersect)
40. [PIVOT](#pivot)
41. [RANK](#rank)
42. [Regex functions](#id140)
43. [STRTOK\_SPLIT\_TO\_TABLE](#strtok-split-to-table)
44. [SUBSTRING](#substring)
45. [TD\_UNPIVOT](#td-unpivot)
46. [TO\_CHAR](#to-char)
47. [XMLAGG](#xmlagg)
48. [CAST](#cast)
49. [Cast from Number Datatypes to Varchar Datatype](#cast-from-number-datatypes-to-varchar-datatype)
50. [Cast to DATE using { }](#cast-to-date-using)
51. [Cast to INTERVAL datatype](#cast-to-interval-datatype)