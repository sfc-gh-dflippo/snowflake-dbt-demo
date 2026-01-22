---
auto_generated: true
description: Translation reference for all the supported built-in functions by SnowConvert
  AI for BigQuery.
last_scraped: '2026-01-14T16:53:04.095813+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/bigquery/bigquery-functions
title: SnowConvert AI - BigQuery - Built-in functions | Snowflake Documentation
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
          + [Redshift](../redshift/README.md)
          + [PostgreSQL-Greenplum-Netezza](../postgres/README.md)
          + [BigQuery](README.md)

            - [Built-in Functions](bigquery-functions.md)
            - [Data Types](bigquery-data-types.md)
            - [CREATE TABLE](bigquery-create-table.md)
            - [CREATE VIEW](bigquery-create-view.md)
            - [Identifier differences between BigQuery and Snowflake](bigquery-identifiers.md)
            - [Operators](bigquery-operators.md)
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)Translation References[BigQuery](README.md)Built-in Functions

# SnowConvert AI - BigQuery - Built-in functions[¶](#snowconvert-ai-bigquery-built-in-functions "Link to this heading")

Translation reference for all the supported built-in functions by SnowConvert AI for BigQuery.

Note

For more information about built-in functions and their Snowflake equivalents, also see [Common built-in functions](../general/built-in-functions).

## Aggregate Functions[¶](#aggregate-functions "Link to this heading")

| BigQuery | Snowflake |
| --- | --- |
| [ANY\_VALUE](https://cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions#any_value) | [ANY\_VALUE](https://docs.snowflake.com/en/sql-reference/functions/any_value)  *Note: Unlike BigQuery, Snowflake does not ignore NULLs . Additionally, Snowflake’s `OVER()` clause does not support the use of `ORDER BY` or explicit window frames.* |
| [ANY\_VALUE](https://cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions#any_value)( expr1, HAVING MAX expr2)  [ANY\_VALUE](https://cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions#any_value)( expr1, HAVING MIN expr2) | [MAX\_BY](https://docs.snowflake.com/en/sql-reference/functions/max_by)(expr1, expr1)  [MIN\_BY](https://docs.snowflake.com/en/sql-reference/functions/min_by)(expr1, expr2) |
| [AVG](https://cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions#avg) | [AVG](https://docs.snowflake.com/en/sql-reference/functions/avg) |
| [COUNT](https://cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions#count) | [COUNT](https://docs.snowflake.com/en/sql-reference/functions/count) |
| [COUNTIF](https://cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions#countif) | [COUNT\_IF](https://docs.snowflake.com/en/sql-reference/functions/count_if) |
| [LOGICAL\_AND](https://cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions#logical_and) | [BOOLAND\_AGG](https://docs.snowflake.com/en/sql-reference/functions/booland_agg) |
| [LOGICAL\_OR](https://cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions#logical_or) | [BOOLOR\_AGG](https://docs.snowflake.com/en/sql-reference/functions/boolor_agg) |
| [MAX](https://cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions#max) | [MAX](https://docs.snowflake.com/en/sql-reference/functions/max) |
| [MIN](https://cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions#min) | [MIN](https://docs.snowflake.com/en/sql-reference/functions/min) |
| [SUM](https://cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions#sum) | [SUM](https://docs.snowflake.com/en/sql-reference/functions/sum) |

## Array Functions[¶](#array-functions "Link to this heading")

| BigQuery | Snowflake |
| --- | --- |
| [ARRAY\_AGG](https://cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions#array_agg) | [ARRAY\_AGG](https://docs.snowflake.com/en/sql-reference/functions/array_agg) |
| [ARRAY\_CONCAT](https://cloud.google.com/bigquery/docs/reference/standard-sql/array_functions#array_concat) | [ARRAY\_CAT](https://docs.snowflake.com/en/sql-reference/functions/array_cat) |
| [ARRAY\_CONCAT\_AGG](https://cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions#array_concat_agg) | [ARRAY\_FLATTEN](https://docs.snowflake.com/en/sql-reference/functions/array_flatten) |
| [ARRAY\_TO\_STRING](https://cloud.google.com/bigquery/docs/reference/standard-sql/array_functions#array_to_string)(expr, delimiter) | [ARRAY\_TO\_STRING](https://docs.snowflake.com/en/sql-reference/functions/array_to_string)(ARRAY\_COMPACT(expr), delimiter) |
| [ARRAY\_TO\_STRING](https://cloud.google.com/bigquery/docs/reference/standard-sql/array_functions#array_to_string)(expr, delimiter, null\_text) | ARRAY\_TO\_STRING\_UDF(expr, delimiter, null\_text)  *Notes: SnowConvert AI generates a UDF to handle the NULL replacement parameter which is not natively supported in Snowflake’s ARRAY\_TO\_STRING function.* |
| [SELECT ARRAY](https://cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax#array_subquery) (SELECT query) | SELECT (SELECT ARRAY\_AGG(\*) FROM (SELECT query))  *Notes: BigQuery’s ARRAY subquery syntax is transformed to use ARRAY\_AGG with a subquery in Snowflake.* |

## Conditional Expressions[¶](#conditional-expressions "Link to this heading")

| BigQuery | Snowflake |
| --- | --- |
| [COALESCE](https://cloud.google.com/bigquery/docs/reference/standard-sql/conditional_expressions#coalesce) | [COALESCE](https://docs.snowflake.com/en/sql-reference/functions/coalesce) |
| [IF](https://cloud.google.com/bigquery/docs/reference/standard-sql/conditional_expressions#if) | [IFF](https://docs.snowflake.com/en/sql-reference/functions/iff) |
| [IFNULL](https://cloud.google.com/bigquery/docs/reference/standard-sql/conditional_expressions#ifnull) | [IFNULL](https://docs.snowflake.com/en/sql-reference/functions/ifnull) |
| [NULLIF](https://cloud.google.com/bigquery/docs/reference/standard-sql/conditional_expressions#nullif) | [NULLIF](https://docs.snowflake.com/en/sql-reference/functions/nullif) |

## Conversion Functions[¶](#conversion-functions "Link to this heading")

| BigQuery | Snowflake |
| --- | --- |
| [SAFE\_CAST](https://cloud.google.com/bigquery/docs/reference/standard-sql/conversion_functions#safe_casting) | [TRY\_CAST](https://docs.snowflake.com/en/sql-reference/functions/try_cast) |

## Date Functions[¶](#date-functions "Link to this heading")

| BigQuery | Snowflake |
| --- | --- |
| [CURRENT\_DATE](https://cloud.google.com/bigquery/docs/reference/standard-sql/date_functions#current_date) [CURRENT\_DATE](https://cloud.google.com/bigquery/docs/reference/standard-sql/date_functions#current_date)() | [CURRENT\_DATE](https://docs.snowflake.com/en/sql-reference/functions/current_date)  [CURRENT\_DATE](https://docs.snowflake.com/en/sql-reference/functions/current_date)() |
| [FORMAT\_DATE](https://cloud.google.com/bigquery/docs/reference/standard-sql/date_functions#format_date) | [TO\_CHAR](https://docs.snowflake.com/en/sql-reference/functions/to_char)  *Note: For further details on this translation, please consult this* [*page*](format_date.md)*.* |

## Datetime Functions[¶](#datetime-functions "Link to this heading")

| BigQuery | Snowflake |
| --- | --- |
| [CURRENT\_DATETIME](https://cloud.google.com/bigquery/docs/reference/standard-sql/datetime_functions#current_datetime)  [CURRENT\_DATETIME](https://cloud.google.com/bigquery/docs/reference/standard-sql/datetime_functions#current_datetime)() | [CURRENT\_TIMESTAMP](https://docs.snowflake.com/en/sql-reference/functions/current_timestamp) :: TIMESTAMP\_NTZ [CURRENT\_TIMESTAMP](https://docs.snowflake.com/en/sql-reference/functions/current_timestamp)() :: TIMESTAMP\_NTZ |

## Geography Functions[¶](#geography-functions "Link to this heading")

| BigQuery | Snowflake |
| --- | --- |
| [ST\_GEOGFROMTEXT](https://cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions#st_geogfromtext) | [ST\_GEOGFROMTEXT](https://docs.snowflake.com/en/sql-reference/functions/st_geographyfromwkt)  *Note: For further details on this translation, please consult this* [*page*](st_geogfromtext.md)*.* |
| [ST\_GEOGPOINT](https://cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions#st_geogpoint) | [ST\_POINT](https://docs.snowflake.com/en/sql-reference/functions/st_makepoint)  *Note: For further details on this translation, please consult this* [*page*](st_geogpoint.md)*.* |

## JSON Functions[¶](#json-functions "Link to this heading")

| BigQuery | Snowflake |
| --- | --- |
| [JSON\_VALUE](https://cloud.google.com/bigquery/docs/reference/standard-sql/json_functions#json_value) / [JSON\_EXTRACT\_SCALAR](https://cloud.google.com/bigquery/docs/reference/standard-sql/json_functions#json_extract_scalar) | [JSON\_EXTRACT\_PATH\_TEXT](https://docs.snowflake.com/en/sql-reference/functions/json_extract_path_text)  *Notes: SnowConvert AI automatically translates BigQuery JSON paths to their Snowflake equivalents.* |
| [JSON\_VALUE\_ARRAY](https://cloud.google.com/bigquery/docs/reference/standard-sql/json_functions#json_value_array) | JSON\_VALUE\_ARRAY\_UDF  *Notes: SnowConvert AI generates a UDF to obtain an equivalent behavior for extracting arrays from JSON.* |
| [LAX\_INT64](https://cloud.google.com/bigquery/docs/reference/standard-sql/json_functions#lax_int64) | PUBLIC.LAX\_INT64\_UDF  *Notes: SnowConvert AI generates a UDF to obtain an equivalent behavior.* |
| [LAX\_BOOL](https://cloud.google.com/bigquery/docs/reference/standard-sql/json_functions#lax_bool) | PUBLIC.LAX\_BOOL\_UDF  *Notes: SnowConvert AI generates a UDF to obtain an equivalent behavior.* |

## Mathematical Functions[¶](#mathematical-functions "Link to this heading")

| BigQuery | Snowflake |
| --- | --- |
| [ABS](https://cloud.google.com/bigquery/docs/reference/standard-sql/mathematical_functions#abs) | [ABS](https://docs.snowflake.com/en/sql-reference/functions/abs) |
| [LEAST](https://cloud.google.com/bigquery/docs/reference/standard-sql/mathematical_functions#least) | [LEAST](https://docs.snowflake.com/en/sql-reference/functions/least) |
| [MOD](https://cloud.google.com/bigquery/docs/reference/standard-sql/mathematical_functions#mod) | [MOD](https://docs.snowflake.com/en/sql-reference/functions/mod) |
| [ROUND](https://cloud.google.com/bigquery/docs/reference/standard-sql/mathematical_functions#round)(X) [ROUND](https://cloud.google.com/bigquery/docs/reference/standard-sql/mathematical_functions#round)(X, Y) [ROUND](https://cloud.google.com/bigquery/docs/reference/standard-sql/mathematical_functions#round)(X, Y, ‘ROUND\_HALF\_EVEN’) [ROUND](https://cloud.google.com/bigquery/docs/reference/standard-sql/mathematical_functions#round)(X, Y, ‘ROUND\_HALF\_AWAY\_FROM\_ZERO’) | [ROUND](https://docs.snowflake.com/en/sql-reference/functions/round)(X) [ROUND](https://docs.snowflake.com/en/sql-reference/functions/round)(X, Y) [ROUND](https://docs.snowflake.com/en/sql-reference/functions/round)(X, Y, ‘HALF\_TO\_EVEN’) [ROUND](https://docs.snowflake.com/en/sql-reference/functions/round)(X, Y, ‘HALF\_AWAY\_FROM\_ZERO’) |

## Navigation Functions[¶](#navigation-functions "Link to this heading")

| BigQuery | Snowflake |
| --- | --- |
| [FIRST\_VALUE](https://cloud.google.com/bigquery/docs/reference/standard-sql/navigation_functions#first_value) | [FIRST\_VALUE](https://docs.snowflake.com/en/sql-reference/functions/first_value) |
| [LAG](https://cloud.google.com/bigquery/docs/reference/standard-sql/navigation_functions#lag) | [LAG](https://docs.snowflake.com/en/sql-reference/functions/lag) |
| [LEAD](https://cloud.google.com/bigquery/docs/reference/standard-sql/navigation_functions#lead) | [LEAD](https://docs.snowflake.com/en/sql-reference/functions/lead) |
| [LAST\_VALUE](https://cloud.google.com/bigquery/docs/reference/standard-sql/navigation_functions#last_value) | [LAST\_VALUE](https://docs.snowflake.com/en/sql-reference/functions/last_value) |

## Numbering Functions[¶](#numbering-functions "Link to this heading")

| BigQuery | Snowflake |
| --- | --- |
| [RANK](https://cloud.google.com/bigquery/docs/reference/standard-sql/numbering_functions#rank) | [RANK](https://docs.snowflake.com/en/sql-reference/functions/rank) |
| [ROW\_NUMBER](https://cloud.google.com/bigquery/docs/reference/standard-sql/numbering_functions#row_number) | [ROW\_NUMBER](https://docs.snowflake.com/en/sql-reference/functions/row_number) |

## String Functions[¶](#string-functions "Link to this heading")

| BigQuery | Snowflake |
| --- | --- |
| [BYTE\_LENGTH](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#byte_length)(expr) | LENGTH(TO\_BINARY(HEX\_ENCODE(expr)))  *Notes: BigQuery’s BYTE\_LENGTH returns the number of bytes in a encoded string. Snowflake equivalent converts to binary after hex encoding to get byte length.* |
| [CHARACTER\_LENGTH](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#character_length) [CHAR\_LENGTH](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#char_length) | [LENGTH](https://docs.snowflake.com/en/sql-reference/functions/length) |
| [CONCAT](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#concat) | [CONCAT](https://docs.snowflake.com/en/sql-reference/functions/concat) |
| [ENDS\_WITH](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#ends_with) | [ENDSWITH](https://docs.snowflake.com/en/sql-reference/functions/endswith) |
| [FROM\_BASE64](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#from_base64) | [TRY\_BASE64\_DECODE\_BINARY](https://docs.snowflake.com/en/sql-reference/functions/try_base64_decode_binary)  *Notes: BigQuery defaults to BASE64 for binary data output, but Snowflake uses HEX. In Snowflake, you can use the* [*`BASE64_ENCODE`*](https://docs.snowflake.com/en/sql-reference/functions/base64_encode) *function or set* [*`BINARY_OUTPUT_FORMAT`*](https://docs.snowflake.com/en/sql-reference/parameters#binary-output-format) *to `’BASE64’` to view binary data in BASE64.* |
| [FROM\_HEX](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#from_hex) | [TRY\_HEX\_DECODE\_BINARY](https://docs.snowflake.com/en/sql-reference/functions/try_hex_decode_binary)  *Notes: BigQuery defaults to BASE64 for binary data output, but Snowflake uses HEX. In Snowflake, you can use the* [*`BASE64_ENCODE`*](https://docs.snowflake.com/en/sql-reference/functions/base64_encode) *function or set* [*`BINARY_OUTPUT_FORMAT`*](https://docs.snowflake.com/en/sql-reference/parameters#binary-output-format) *to `’BASE64’` to view binary data in BASE64.* |
| [LEFT](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#left) | [LEFT](https://docs.snowflake.com/en/sql-reference/functions/left) |
| [LENGTH](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#length) | [LENGTH](https://docs.snowflake.com/en/sql-reference/functions/length) |
| [LOWER](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#lower) | [LOWER](https://docs.snowflake.com/en/sql-reference/functions/lower) |
| [LPAD](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#lpad) | [LPAD](https://docs.snowflake.com/en/sql-reference/functions/lpad) |
| [LTRIM](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#ltrim) | [LTRIM](https://docs.snowflake.com/en/sql-reference/functions/ltrim) |
| [REGEXP\_CONTAINS](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#regexp_contains)(value, regexp) | [REGEXP\_INSTR](../../../../sql-reference/functions/regexp_instr)(value, regexp) > 0 |
| [REGEXP\_EXTRACT\_ALL](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#regexp_extract_all) | [REGEXP\_SUBSTR\_ALL](https://docs.snowflake.com/en/sql-reference/functions/regexp_substr_all) |
| [REPLACE](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#replace) | [REPLACE](https://docs.snowflake.com/en/sql-reference/functions/replace) |
| [RIGHT](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#right) | [RIGHT](https://docs.snowflake.com/en/sql-reference/functions/right) |
| [RPAD](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#rpad) | [RPAD](https://docs.snowflake.com/en/sql-reference/functions/rpad) |
| [RTRIM](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#rtrim) | [RTRIM](https://docs.snowflake.com/en/sql-reference/functions/rtrim) |
| [SPLIT](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#split) | [SPLIT](https://docs.snowflake.com/en/sql-reference/functions/split) |
| [STARTS\_WITH](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#starts_with) | [STARTSWITH](https://docs.snowflake.com/en/sql-reference/functions/startswith) |
| [SUBSTR](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#substr)(string, position)  [SUBSTRING](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#substring)(string, position)  [SUBSTR](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#substr)(sttring, position, length)  [SUBSTRING](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#substring)(sttring, position, length) | [SUBSTR](https://docs.snowflake.com/en/sql-reference/functions/substr)(string, IFF(position < -LENGTH(string), 1, position))  [SUBSTRING](https://docs.snowflake.com/en/sql-reference/functions/substr)(string, IFF(position < -LENGTH(string), 1, position))  [SUBSTR](https://docs.snowflake.com/en/sql-reference/functions/substr)(sttring, IFF(position < -LENGTH(string), 1, position), length)  [SUBSTRING](https://docs.snowflake.com/en/sql-reference/functions/substr)(sttring, IFF(position < -LENGTH(string), 1, position), length) |
| [TO\_HEX](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#to_hex) | [HEX\_ENCODE](https://docs.snowflake.com/en/sql-reference/functions/hex_encode) |
| [UPPER](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#upper) | [UPPER](https://docs.snowflake.com/en/sql-reference/functions/upper) |

## Timestamp Functions[¶](#timestamp-functions "Link to this heading")

| BigQuery | Snowflake |
| --- | --- |
| [CURRENT\_TIMESTAMP](https://cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions#current_timestamp) [CURRENT\_TIMESTAMP](https://cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions#current_timestamp)() | [CURRENT\_TIMESTAMP](https://docs.snowflake.com/en/sql-reference/functions/current_timestamp)  [CURRENT\_TIMESTAMP](https://docs.snowflake.com/en/sql-reference/functions/current_timestamp)() |
| [SAFE.TIMESTAMP\_MILLIS](https://cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions#timestamp_millis) | IFF(expr BETWEEN -62135596800000 AND 253402300799999, TO\_TIMESTAMP(expr / 1000), null)  *Notes: Safe version with range validation to prevent overflow errors.* |
| [SAFE.TIMESTAMP\_SECONDS](https://cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions#timestamp_seconds) | SAFE\_TIMESTAMP\_SECONDS\_UDF(expr)  *Notes: SnowConvert AI generates a UDF to provide safe timestamp conversion with error handling.* |
| [TIMESTAMP\_MILLIS](https://cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions#timestamp_millis) | TO\_TIMESTAMP(expr / 1000)  *Notes: Converts milliseconds since epoch to timestamp by dividing by 1000.* |
| [TIMESTAMP\_SECONDS](https://cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions#timestamp_seconds)(expr) | DATEADD(‘seconds’, expr, ‘1970-01-01’)  *Notes: Adds seconds to Unix epoch start date.* |
| [UNIX\_MICROS](https://cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions#unix_micros)(timestamp) | DATE\_PART(‘epoch\_microsecond’, CONVERT\_TIMEZONE(‘UTC’, timestamp))  *Notes: Extracts microseconds since Unix epoch from timestamp converted to UTC.* |
| [UNIX\_MILLIS](https://cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions#unix_millis)(timestamp) | DATE\_PART(‘epoch\_millisecond’, CONVERT\_TIMEZONE(‘UTC’, timestamp))  *Notes: Extracts milliseconds since Unix epoch from timestamp converted to UTC.* |
| [UNIX\_SECONDS](https://cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions#unix_seconds)(timestamp) | DATE\_PART(‘epoch\_seconds’, CONVERT\_TIMEZONE(‘UTC’, timestamp))  *Notes: Extracts seconds since Unix epoch from timestamp converted to UTC.* |

## FORMAT\_DATE[¶](#format-date "Link to this heading")

Format\_date function

### Description[¶](#description "Link to this heading")

Formats a `DATE` value according to a specified format string.

For more information, please refer to [FORMAT\_DATE](https://cloud.google.com/bigquery/docs/reference/standard-sql/date_functions#format_date) function.

### Grammar Syntax[¶](#grammar-syntax "Link to this heading")

```
 FORMAT_DATE(format_string, date_expr)
```

Copy

#### Sample Source[¶](#sample-source "Link to this heading")

##### BigQuery[¶](#bigquery "Link to this heading")

```
CREATE TABLE TEST_DATE (col1 DATE);
SELECT FORMAT_DATE('%Y', col1);
```

Copy

##### Snowflake[¶](#snowflake "Link to this heading")

```
CREATE TABLE TEST_DATE (col1 DATE);
SELECT
  TO_CHAR(col1, 'YYYY')
FROM
  TEST_DATE;
```

Copy

#### BigQuery Formats Equivalents[¶](#bigquery-formats-equivalents "Link to this heading")

| BigQuery | Snowflake |
| --- | --- |
| %A | PUBLIC.DAYNAME\_LONG\_UDF(date\_expr)  *Note: Generate UDF in conversion for support.* |
| %a | DY |
| %B | MMMM |
| %b | MON |
| %C | PUBLIC.CENTURY\_UDF(date\_expr)  *Note: Generate UDF in conversion for support.* |
| %c | DY MON DD HH24:MI:SS YYYY |
| %D | MM/DD/YY |
| %d | DD |
| %e | DD |
| %F | YYYY-MM-DD |
| %G | YEAROFWEEKISO(date\_expr) |
| %g | PUBLIC.ISO\_YEAR\_PART\_UDF(date\_expr, 2)  *Note: Generate UDF in conversion for support.* |
| %H | HH24 |
| %h | MON |
| %I | HH12 |
| %J | PUBLIC.DAY\_OF\_YEAR\_ISO\_UDF(date\_expr)  *Note: Generate UDF in conversion for support.* |
| %j | DAYOFYEAR(date\_expr) |
| %k | HH24 |
| %l | HH12 |
| %M | MI |
| %m | MM |
| %n | *Not equivalent format* |
| %P | pm |
| %p | AM |
| %Q | QUARTER(date\_expr) |
| %R | HH24:MI |
| %S | SS |
| %s | *Not equivalent format* |
| %T | HH24:MI:SS |
| %t | *Not equivalent format* |
| %U | WEEK(date\_expr) |
| %u | DAYOFWEEKISO(date\_expr) |
| %V | WEEKISO(date\_expr) |
| %W | WEEK(date\_expr)   *Note: Unlike BigQuery, Snowflake results are dictated by the values set for the WEEK\_OF\_YEAR\_POLICY and/or WEEK\_START session parameters. So, results could differ from BigQuery based on those parameters.* |
| %w | DAYOFWEEK(date\_expr)  *Note: Unlike BigQuery, Snowflake results are dictated by the values set for the WEEK\_OF\_YEAR\_POLICY and/or WEEK\_START session parameters. So, results could differ from BigQuery based on those parameters.* |
| %X | HH24:MI:SS |
| %x | MM/DD/YY |
| %Y | YYYY |
| %y | YY |
| %Z | *Not equivalent format* |
| %z | *Not equivalent format* |
| %Ez | *Not equivalent format* |
| %E<number>S | *Not equivalent format* |
| %E\*S | *Not equivalent format* |
| %EY4 | YYYY |

Warning

In BigQuery, the format related to time is not applied when the type is DATE, but Snowflake applies the format with values in zero for HH:MI:SS usages.

Note

For more information, please refer to [BigQuery DateTime formats](https://cloud.google.com/bigquery/docs/reference/standard-sql/format-elements#format_elements_date_time).

## ST\_GEOGFROMTEXT[¶](#st-geogfromtext "Link to this heading")

Geography Function.

### Description[¶](#id1 "Link to this heading")

> Returns a `GEOGRAPHY` value that corresponds to the input [WKT](https://en.wikipedia.org/wiki/Well-known_text) representation.

For more information, please refer to [ST\_GEOGFROMTEXT](https://cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions#st_geogfromtext) function.

SuccessPlaceholder

ST\_GEOGFROMTEXT function is supported in Snowflake.

### Grammar Syntax[¶](#id2 "Link to this heading")

```
 ST_GEOGFROMTEXT(wkt_string[, oriented])
```

Copy

#### Sample Source[¶](#id3 "Link to this heading")

The oriented parameter in the ST\_GEOGFROMTEXT function is not supported in Snowflake.

##### BigQuery[¶](#id4 "Link to this heading")

```
 SELECT ST_GEOGFROMTEXT('POINT(-122.35 37.55)');
SELECT ST_GEOGFROMTEXT('POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))', TRUE);
```

Copy

##### Snowflake[¶](#id5 "Link to this heading")

```
 SELECT ST_GEOGFROMTEXT('POINT(-122.35 37.55)');
SELECT
!!!RESOLVE EWI!!! /*** SSC-EWI-BQ0006 - ORIENTED PARAMETER IN THE ST_GEOGFROMTEXT FUNCTION IS NOT SUPPORTED IN SNOWFLAKE. ***/!!! 
ST_GEOGFROMTEXT('POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))');
```

Copy

Please keep in mind that the default output format for geography data types is **WKT** **(Well-Known Text)** and in Snowflake **WKB (Well-Known Binary)**. You can use the [ST\_ASWKT](https://docs.snowflake.com/en/sql-reference/functions/st_aswkt) function or set the [GEOGRAPHY\_OUTPUT\_FORMAT](https://docs.snowflake.com/en/sql-reference/parameters#geography-output-format) format if you want to view the data in **WKT** format.

#### Using ST\_GEOGFROMTEXT function to insert geography data[¶](#using-st-geogfromtext-function-to-insert-geography-data "Link to this heading")

This function is not allowed in the values clause and is not required in Snowflake.

##### BigQuery[¶](#id6 "Link to this heading")

```
 CREATE OR REPLACE TABLE test.geographyType
(
  COL1 GEOGRAPHY
);

INSERT INTO test.geographyType VALUES
    (ST_GEOGFROMTEXT('POINT(-122.35 37.55)')), 
    (ST_GEOGFROMTEXT('LINESTRING(-124.20 42.00, -120.01 41.99)'));
```

Copy

##### Snowflake[¶](#id7 "Link to this heading")

```
 CREATE OR REPLACE TABLE test.geographyType
(
  COL1 GEOGRAPHY
);

INSERT INTO test.geographyType
VALUES
    (
     --** SSC-FDM-BQ0010 - THE FUNCTION 'ST_GEOGFROMTEXT' IS NOT REQUIRED IN SNOWFLAKE. **
     'POINT(-122.35 37.55)'),
    (
     --** SSC-FDM-BQ0010 - THE FUNCTION 'ST_GEOGFROMTEXT' IS NOT REQUIRED IN SNOWFLAKE. **
     'LINESTRING(-124.20 42.00, -120.01 41.99)');
```

Copy

### Related EWI’s[¶](#related-ewi-s "Link to this heading")

1. [SSC-EWI-BQ0006](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/bigqueryEWI.html#ssc-ewi-bq0006): Oriented parameter in the ST\_GEOGFROMTEXT function is not supported in Snowflake.
2. [SSC-FDM-BQ0010](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/bigqueryFDM.html#ssc-fdm-bq0010): Geography function is not required in Snowflake.

## ST\_GEOGPOINT[¶](#st-geogpoint "Link to this heading")

Geography Function.

### Description[¶](#id8 "Link to this heading")

> Creates a `GEOGRAPHY` with a single point. `ST_GEOGPOINT` creates a point from the specified `FLOAT64` longitude (in degrees, negative west of the Prime Meridian, positive east) and latitude (in degrees, positive north of the Equator, negative south) parameters and returns that point in a `GEOGRAPHY` value.

For more information, please refer to [ST\_GEOGPOINT](https://cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions#st_geogpoint) function.

Note

The function ST\_GEOGPOINT is translated to ST\_POINT in Snowflake.

### Grammar Syntax[¶](#id9 "Link to this heading")

```
 ST_GEOGPOINT(longitude, latitude)
```

Copy

#### Sample Source[¶](#id10 "Link to this heading")

##### BigQuery[¶](#id11 "Link to this heading")

```
 SELECT ST_GEOGPOINT(-122.0838, 37.3860);
```

Copy

##### Snowflake[¶](#id12 "Link to this heading")

```
 SELECT ST_POINT(-122.0838, 37.3860);
```

Copy

Please keep in mind that the default output format for geography data types is **WKT** **(Well-Known Text)** and in Snowflake **WKB (Well-Known Binary)**. You can use the [ST\_ASWKT](https://docs.snowflake.com/en/sql-reference/functions/st_aswkt) function or set the [GEOGRAPHY\_OUTPUT\_FORMAT](https://docs.snowflake.com/en/sql-reference/parameters#geography-output-format) format if you want to view the data in **WKT** format.

#### Using ST\_POINT function to insert geography data[¶](#using-st-point-function-to-insert-geography-data "Link to this heading")

This function is not allowed in the values clause and is not required in Snowflake.

##### BigQuery[¶](#id13 "Link to this heading")

```
 CREATE OR REPLACE TABLE test.geographyType
(
  COL1 GEOGRAPHY
);

INSERT INTO test.geographyType
VALUES (ST_GEOGPOINT(-122.0838, 37.3860));
```

Copy

##### Snowflake[¶](#id14 "Link to this heading")

```
 CREATE OR REPLACE TABLE test.geographyType
(
  COL1 GEOGRAPHY
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "bigquery",  "convertedOn": "04/03/2025",  "domain": "test" }}';

INSERT INTO test.geographyType
VALUES (
--** SSC-FDM-BQ0010 - THE FUNCTION 'ST_GEOGFROMTEXT' IS NOT REQUIRED IN SNOWFLAKE. **
'POINT(122.0838 37.3860)');
```

Copy

### Related EWI’s[¶](#id15 "Link to this heading")

1. [SSC-FDM-BQ0010](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/bigqueryFDM.html#ssc-fdm-bq0010): Geography function is not required in Snowflake.

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
2. [Array Functions](#array-functions)
3. [Conditional Expressions](#conditional-expressions)
4. [Conversion Functions](#conversion-functions)
5. [Date Functions](#date-functions)
6. [Datetime Functions](#datetime-functions)
7. [Geography Functions](#geography-functions)
8. [JSON Functions](#json-functions)
9. [Mathematical Functions](#mathematical-functions)
10. [Navigation Functions](#navigation-functions)
11. [Numbering Functions](#numbering-functions)
12. [String Functions](#string-functions)
13. [Timestamp Functions](#timestamp-functions)
14. [FORMAT\_DATE](#format-date)
15. [ST\_GEOGFROMTEXT](#st-geogfromtext)
16. [ST\_GEOGPOINT](#st-geogpoint)