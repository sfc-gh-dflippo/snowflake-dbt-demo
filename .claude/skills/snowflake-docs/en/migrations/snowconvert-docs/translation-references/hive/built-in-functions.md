---
auto_generated: true
description: Hive SQL
last_scraped: '2026-01-14T16:53:09.970807+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/hive/built-in-functions
title: SnowConvert AI - Hive - Built-in functions | Snowflake Documentation
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
          + [Hive-Spark-Databricks SQL](README.md)

            - [DDLs](ddls/README.md)
            - [Built-in Functions](built-in-functions.md)
            - [Data Types](data-types.md)
          + [Redshift](../redshift/README.md)
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)Translation References[Hive-Spark-Databricks SQL](README.md)Built-in Functions

# SnowConvert AI - Hive - Built-in functions[¶](#snowconvert-ai-hive-built-in-functions "Link to this heading")

Applies to

* Hive SQL
* Spark SQL
* Databricks SQL

Note

For more information about built-in functions and their Snowflake equivalents, also see [Common built-in functions](../general/built-in-functions).

## Built-in Functions[¶](#built-in-functions "Link to this heading")

> This article provides an alphabetically-ordered list of built-in functions and operators in Databricks. ([Databricks SQL Language Reference Built-in functions](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-functions-builtin-alpha)).

| Spark SQL - Databricks SQL | Snowflake |
| --- | --- |
| ABS | ABS |
| ACOS | ACOS |
| ACOSH | ACOSH |
| ADD\_MONTHS | ADD\_MONTHS |
| ANY\_VALUE | ANY\_VALUE |
| ANY | BOOLOR\_AGG |
| APPROX\_COUNT\_DISTINCT | APPROX\_COUNT\_DISTINCT |
| APPROX\_PERCENTILE | APPROX\_PERCENTILE |
| ARRAY\_AGG | ARRAY\_AGG |
| ARRAY\_APPEND | ARRAY\_APPEND |
| ARRAY\_COMPACT | ARRAY\_COMPACT |
| ARRAY\_CONTAINS | ARRAY\_CONTAINS |
| ARRAY\_DISTINCT | ARRAY\_DISTINCT |
| ARRAY\_EXCEPT | ARRAY\_EXCEPT |
| ARRAY\_INSERT | ARRAY\_INSERT\_UDF  *Note: A User Defined Function is created to replicate the source behaviour.* |
| ARRAY\_INTERSECT | ARRAY\_INTERSECTION |
| ARRAY\_JOIN | ARRAY\_TO\_STRING |
| ARRAY\_MAX | ARRAY\_MAX |
| ARRAY\_MIN | ARRAY\_MIN |
| ARRAY\_POSITION(array, element) | ARRAY\_POSITION(element, array)  *Note: Parameters are inverted.* |
| ARRAY\_PREPEND | ARRAY\_PREPEND |
| ARRAY\_REMOVE | ARRAY\_REMOVE |
| ARRAY\_SIZE | ARRAY\_SIZE |
| ARRAY | ARRAY\_CONSTRUCT |
| ARRAYS\_OVERLAP | ARRAYS\_OVERLAP |
| ARRAYS\_ZIP | ARRAYS\_ZIP |
| ASCII | ASCII |
| ASIN | ASIN |
| ASINH | ASINH |
| ATAN | ATAN |
| ATAN2 | ATAN2 |
| ATANH | ATANH |
| AVG | AVG |
| BIT\_COUNT | BITCOUNT |
| BIT\_GET | GETBIT |
| BOOL\_AND | BOOLAND\_AGG |
| BOOL\_OR | BOOLOR\_AGG |
| BTRIM | TRIM |
| CBRT | CBRT |
| CEIL | CEIL |
| CEILING | CEIL |
| CHAR\_LENGTH | LENGTH |
| CHARACTER\_LENGTH | LENGTH |
| CHR | CHR |
| COALESCE | COALESCE |
| COLLECT\_LIST | ARRAY\_AGG |
| CONCAT\_WS | CONCAT\_WS\_UDF  Note: A User Defined Function is created to emulate the source behaviour. |
| CONCAT | CONCAT |
| CONTAINS | CONTAINS |
| CORR | CORR |
| COS | COS |
| COSH | COSH |
| COT | COT |
| COUNT\_IF | COUNT\_IF |
| COUNT | COUNT |
| COVAR\_POP | COVAR\_POP |
| COVAR\_SAMP | COVAR\_SAMP |
| CUME\_DIST | CUME\_DIST |
| CURDATE | CURRENT\_DATE |
| CURRENT\_DATABASE | CURRENT\_DATABASE |
| CURRENT\_DATE | CURRENT\_DATE |
| CURRENT\_SCHEMA | CURRENT\_SCHEMA |
| CURRENT\_TIMESTAMP | CURRENT\_TIMESTAMP |
| CURRENT\_USER | CURRENT\_USER |
| DATE\_ADD | DATEADD |
| DATE\_DIFF | DATEDIFF |
| DATE\_TRUNC | DATE\_TRUNC |
| DATE | DATE |
| DAY | DAY |
| DAYNAME | DAYNAME |
| DAYOFWEEK | DAYOFWEEK |
| DAYOFYEAR | DAYOFYEAR |
| DECODE | DECODE |
| DEGREES | DEGREES |
| DENSE\_RANK | DENSE\_RANK |
| ENDSWITH | ENDSWITH |
| EVERY | BOOLAND\_AGG |
| EXP | EXP |
| FIRST\_VALUE | FIRST\_VALUE |
| FLOOR | FLOOR |
| GET | GET |
| GETBIT | GETBIT |
| GETDATE | CURRENT\_TIMESTAMP |
| GREATEST | GREATEST |
| GROUPING | GROUPING |
| HASH | HASH |
| HEX | HEX\_ENCODE |
| HLL\_SKETCH\_ESTIMATE | HLL\_ESTIMATE |
| HOUR | HOUR |
| HOUR | HOUR |
| IF | IFF |
| IFF | IFF |
| IFNULL | IFNULL |
| INITCAP | INITCAP |
| KURTOSIS | KURTOSIS |
| LAG | LAG |
| LAST\_DAY | LAST\_DAY |
| LAST\_DAY | LAST\_DAY |
| LAST\_VALUE | LAST\_VALUE |
| LCASE | LOWER |
| LEAD | LEAD |
| LEAST | LEAST |
| LEFT | LEFT |
| LEN | LEN |
| LENGTH | LENGTH |
| LEVENSHTEIN | EDITDISTANCE |
| LISTAGG | LISTAGG |
| LN | LN |
| LOCATE | CHARINDEX |
| LOG | LOG |
| LOWER | LOWER |
| LPAD | LPAD |
| LTRIM | LTRIM |
| MAP\_KEYS | OBJECT\_KEYS |
| MAP(key, value, …) | OBJECT\_CONSTRUCT(key, value, …)  *Note: The keys are casted to VARCHAR since Snowflake does not allow another type as keys.* |
| MAX\_BY | MAX\_BY |
| MAX | MAX |
| MD5 | MD5 |
| MEAN | AVG |
| MEDIAN | MEDIAN |
| MIN\_BY | MIN\_BY |
| MIN | MIN |
| MINUTE | MINUTE |
| MOD | MOD |
| MODE | MODE |
| MONTH | MONTH |
| MONTHS\_BETWEEN | MONTHS\_BETWEEN |
| NAMED\_STRUCT | OBJECT\_CONSTRUCT |
| NOW | CURRENT\_TIMESTAMP |
| NTH\_VALUE | NTH\_VALUE |
| NTILE | NTILE |
| NULLIF | NULLIF |
| NULLIFZERO | NULLIFZERO |
| NVL | NVL |
| NVL2 | NVL2 |
| OCTET\_LENGTH | OCTET\_LENGTH |
| PARSE\_JSON | PARSE\_JSON |
| PERCENT\_RANK | PERCENT\_RANK |
| PERCENTILE\_APPROX | APPROX\_PERCENTILE |
| PERCENTILE\_CONT | PERCENTILE\_CONT |
| PERCENTILE\_DISC | PERCENTILE\_DISC |
| PI | PI |
| POSITION | POSITION |
| POW | POW |
| POWER | POWER |
| QUARTER | QUARTER |
| RADIANS | RADIANS |
| RANDOM | RANDOM |
| RANK | RANK |
| REGEXP\_COUNT | REGEXP\_COUNT |
| REGEXP\_INSTR | REGEXP\_INSTR |
| REGEXP\_REPLACE | REGEXP\_REPLACE |
| REGEXP\_SUBSTR | REGEXP\_SUBSTR |
| REGR\_AVGX | REGR\_AVGX |
| REGR\_AVGY | REGR\_AVGY |
| REGR\_COUNT | REGR\_COUNT |
| REGR\_INTERCEPT | REGR\_INTERCEPT |
| REGR\_R2 | REGR\_R2 |
| REGR\_SLOPE | REGR\_SLOPE |
| REGR\_SXX | REGR\_SXX |
| REGR\_SXY | REGR\_SXY |
| REGR\_SYY | REGR\_SYY |
| REPEAT | REPEAT |
| REPLACE | REPLACE |
| REVERSE | REVERSE |
| RIGHT | RIGHT |
| ROUND | ROUND |
| ROW\_NUMBER | ROW\_NUMBER |
| RPAD | RPAD |
| RTRIM | RTRIM |
| SECOND | SECOND |
| SESSION\_USER | CURRENT\_USER |
| SHA1 | SHA1 |
| SHA2 | SHA2 |
| SHIFTLEFT | BITSHIFTLEFT |
| SHIFTRIGHT | BITSHIFTRIGHT |
| SIGN | SIGN |
| SIGNUM | SIGN |
| SIN | SIN |
| SINH | SINH |
| SKEWNESS | SKEW |
| SOME | BOOLOR\_AGG |
| SOUNDEX | SOUNDEX |
| SPACE | SPACE |
| SPLIT\_PART | SPLIT\_PART |
| SQRT | SQRT |
| STARTSWITH | STARTSWITH |
| STD | STDDEV\_SAMP |
| STDDEV\_POP | STDDEV\_POP |
| STDDEV\_SAMP | STDDEV\_SAMP |
| STDDEV | STDDEV\_SAMP |
| STRING | TO\_VARCHAR |
| STRUCT | OBJECT\_CONSTRUCT |
| SUBSTR | SUBSTR |
| SUBSTRING | SUBSTRING |
| SUM | SUM |
| TAN | TAN |
| TANH | TANH |
| TIMESTAMP | TO\_TIMESTAMP |
| TO\_CHAR | TO\_CHAR |
| TO\_DATE | TO\_DATE |
| TO\_NUMBER | TO\_NUMBER |
| TO\_TIMESTAMP | TO\_TIMESTAMP |
| TO\_VARCHAR | TO\_VARCHAR |
| TRANSLATE | TRANSLATE |
| TRIM | TRIM |
| TRUNC | TRUNC |
| TRUNC | TRUNC |
| TRY\_AVG | AVG |
| TRY\_CAST | TRY\_CAST |
| TRY\_SUM | TRY\_SUM |
| TRY\_TO\_NUMBER | TRY\_TO\_NUMBER |
| TRY\_TO\_TIMESTAMP | TRY\_TO\_TIMESTAMP |
| TYPEOF | TYPEOF |
| UCASE | UPPER |
| UPPER | UPPER |
| USER | CURRENT\_USER |
| UUID | UUID\_STRING |
| VAR\_POP | VAR\_POP |
| VAR\_SAMP | VAR\_SAMP |
| VARIANCE\_POP | VARIANCE\_POP |
| VARIANCE\_SAMP | VARIANCE\_SAMP |
| VARIANCE | VARIANCE |
| WIDTH\_BUCKET | WIDTH\_BUCKET |
| YEAR | YEAR |
| ZEROIFNULL | ZEROIFNULL |

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

1. [Built-in Functions](#built-in-functions)