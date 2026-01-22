---
auto_generated: true
description: This section shows equivalents between functions in Oracle and in Snowflake.
last_scraped: '2026-01-14T16:53:18.274116+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/oracle/functions/README
title: SnowConvert AI - Oracle - Built-in functions | Snowflake Documentation
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
          + [Teradata](../../teradata/README.md)
          + [Oracle](../README.md)

            - [Sample Data](../sample-data.md)
            - Basic Elements of Oracle SQL

              - [Literals](../basic-elements-of-oracle-sql/literals.md)
              - [Data Types](../basic-elements-of-oracle-sql/data-types/README.md)
            - [Pseudocolumns](../pseudocolumns.md)
            - [Built-in Functions](README.md)

              * [Custom UDFs](custom_udfs.md)
            - [Built-in Packages](../built-in-packages.md)
            - [SQL Queries and Subqueries](../sql-queries-and-subqueries/selects.md)
            - [SQL Statements](../sql-translation-reference/README.md)
            - [PL/SQL to Snowflake Scripting](../pl-sql-to-snowflake-scripting/README.md)
            - [PL/SQL to Javascript](../pl-sql-to-javascript/README.md)
            - [SQL Plus](../sql-plus.md)
            - [Wrapped Objects](../wrapped-objects.md)
            - ETL And BI Repointing

              - [Power BI Oracle Repointing](../etl-bi-repointing/power-bi-oracle-repointing.md)
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

[Guides](../../../../../guides/README.md)[Migrations](../../../../README.md)Tools[SnowConvert AI](../../../overview.md)Translation References[Oracle](../README.md)Built-in Functions

# SnowConvert AI - Oracle - Built-in functions[¶](#snowconvert-ai-oracle-built-in-functions "Link to this heading")

This section shows equivalents between functions in Oracle and in Snowflake.

| Oracle | Snowflake | Notes |
| --- | --- | --- |
| ABS | ABS |  |
| ACOS | ACOS |  |
| ADD\_MONTHS | ADD\_MONTHS |  |
| ANY\_VALUE | ANY\_VALUE | A warning is being added to indicate the Snowflake counterpart may not be functionally equivalent. |
| APPROX\_COUNT | *\*to be defined* |  |
| APPROX\_COUNT\_DISTINCT | APPROX\_COUNT\_DISTINCT |  |
| APPROX\_COUNT\_DISTINCT\_AGG | *\*to be defined* |  |
| APPROX\_COUNT\_DISTINCT\_DETAIL | *\*to be defined* |  |
| APPROX\_MEDIAN | *\*to be defined* |  |
| APPROX\_PERCENTILE | APPROX\_PERCENTILE |  |
| APPROX\_PERCENTILE\_AGG | *\*to be defined* |  |
| APPROX\_PERCENTILE\_DETAIL | *\*to be defined* |  |
| APPROX\_RANK | *\*to be defined* |  |
| APPROX\_SUM | *\*to be defined* |  |
| ASCII | ASCII |  |
| ASCIISTR | *\*to be defined* |  |
| ASIN | ASIN |  |
| ATAN | ATAN |  |
| ATAN2 | ATAN2 |  |
| AVG | AVG |  |
| BFILENAME | *\*to be defined* |  |
| BIN\_TO\_NUM | *\*to be defined* |  |
| BITAND | BITAND |  |
| BIT\_AND\_AGG | BITAND\_AGG | A warning is being added to indicate the Snowflake counterpart may not be functionally equivalent. |
| BITMAP\_BIT\_POSITION | BITMAP\_BIT\_POSITION |  |
| BITMAP\_BUCKET\_NUMBER | BITMAP\_BUCKET\_NUMBER |  |
| BITMAP\_CONSTRUCT\_\_\_AGG | BITMAP\_CONSTRUCT\_\_\_AGG | A warning is being added to indicate the Snowflake counterpart may not be functionally equivalent. |
| BITMAP\_COUNT | BITMAP\_BIT\_COUNT | A warning is being added to indicate the Snowflake counterpart may not be functionally equivalent. |
| BITMAP\_OR\_AGG | BITMAP\_OR\_\_\_AGG | A warning is being added to indicate the Snowflake counterpart may not be functionally equivalent. |
| BIT\_OR\_AGG | BIT\_OR\_AGG | A warning is being added to indicate the Snowflake counterpart may not be functionally equivalent. |
| BIT\_XOR\_AGG | BIT\_XOR\_AGG | A warning is being added to indicate the Snowflake counterpart may not be functionally equivalent. |
| CARDINALITY | *\*to be defined* |  |
| CAST | CAST  TO\_DATE  TO\_NUMBER  TO\_TIMESTAMP  Not Supported | The function is converted to stub ***‘CAST\_STUB’*** and outputs an error, when comes with one of the following not supported statement: ***‘DEFAULT ON CONVERSION ERROR’*** or ***‘MULTISET’***. Also, it is converted to a stub and outputs an **error** if the **data type** is not supported. The function is converted to the ***‘TO\_NUMBER’*** function when the expression to cast is of type ***number*** and outputs an **error** indicating that the explicit cast is not possible to be done. The function is converted to the ***‘TO\_DATE’*** function when the expression to cast is of type ***date*** and outputs an **error** indicating that the explicit cast is not possible to be done. The function is converted to the ***‘TO\_TIMESTAMP’*** function when the expression to cast is of type ***timestamp*** and outputs an error indicating that the explicit cast is not possible to be done. |
| CEIL | CEIL |  |
| CHARTOROWID | *\*to be defined* |  |
| CHECKSUM | *\*to be defined* |  |
| CHR | CHR | ***USING NCHAR\_CS*** statement is not supported by the Snowflake function equivalent. The clause is removed. |
| CLUSTER\_DETAILS | *\*to be defined* |  |
| CLUSTER\_DISTANCE | *\*to be defined* |  |
| CLUSTER\_ID | *\*to be defined* |  |
| CLUSTER\_PROBABILITY | *\*to be defined* |  |
| CLUSTER\_SET | *\*to be defined* |  |
| COALESCE | COALESCE |  |
| COLLATION | COLLATION |  |
| COLLECT | *\*to be defined* |  |
| COMPOSE | *\*to be defined* |  |
| CON\_DBID\_TO\_ID | *\*to be defined* |  |
| CON\_GUID\_TO\_ID | *\*to be defined* |  |
| CON\_NAME\_TO\_ID | *\*to be defined* |  |
| CON\_UID\_TO\_ID | *\*to be defined* |  |
| CONCAT | CONCAT | Every expression parameter will be inside of an ***NVL(expr, ‘ ‘)*** function to avoid an error in case one of the expressions is null. |
| CONVERT | *\*to be defined* |  |
| CORR | CORR | A warning is being added to indicate the Snowflake counterpart may not be functionally equivalent. |
| CORR\_S | *\*to be defined* |  |
| CORR\_K | *\*to be defined* |  |
| COS | COS |  |
| COSH | COSH |  |
| COUNT | COUNT |  |
| COVAR\_POP | COVAR\_POP | A warning is being added to indicate the Snowflake counterpart may not be functionally equivalent. |
| COVAR\_SAMP | COVAR\_SAMP | A warning is being added to indicate the Snowflake counterpart may not be functionally equivalent. |
| CUBE\_TABLE | Not Supported | Converted to a stub ***‘CUBE\_TABLE\_STUB’*** and an **error** is added. |
| CUME\_DIST | CUME\_DIST | A warning is being added to indicate the Snowflake counterpart may not be functionally equivalent. |
| CURRENT\_DATE | CURRENT\_DATE |  |
| CURRENT\_TIMESTAMP | CURRENT\_TIMESTAMP |  |
| CV | *\*to be defined* |  |
| DATAOBJ\_TO\_MAT\_PARTITION | *\*to be defined* |  |
| DATAOBJ\_TO\_PARTITION | *\*to be defined* |  |
| DBTIMEZONE | *\*to be defined* |  |
| DECODE | DECODE |  |
| DECOMPOSE | *\*to be defined* |  |
| DENSE\_RANK | DENSE\_RANK | There are two kinds of syntax, ***aggregate syntax***, and ***analytic syntax***. The ***aggregate syntax*** is not supported and an **error** is added. The analytic syntax is supported but the ***‘SIBLINGS’*** keyword is removed from the ***‘order by’*** ***clause*** and a **warning** is added. |
| DEPTH | *\*to be defined* |  |
| DEREF | *\*to be defined* |  |
| DUMP | *\*to be defined* |  |
| EMPTY\_BLOB | *\*to be defined* |  |
| EMPTY\_CLOB | *\*to be defined* |  |
| EXISTSNODE | *\*to be defined* |  |
| EXP | EXP |  |
| EXTRACT (datetime) | EXTRACT (datetime)  Not supported | Kept as an ***EXTRACT*** function but outputs a warning when the function has ***‘MINUTE’*** or ***‘TIMEZONE\_MINUTE’*** as the first keyword parameter. Converted to a stub ***‘EXTRACT\_STUB’*** and outputs an **error** when the first keyword parameter is ***‘TIMEZOME\_REGION’*** or ***‘TIMEZONE\_ABBR’*** |
| EXTRACT (XML) | Not Supported | Function related to **XML** is not supported. It is converted to a stub ***‘EXTRACT\_STUB’*** and an error is added. Please check the following link about how to handle the loading for XML: |
| EXTRACTVALUE | Not Supported | Converted to a stub ***‘EXTRACTVALUE\_STUB’*** and an **error** is added. |
| FEATURE\_COMPARE | *\*to be defined* |  |
| FEATURE\_DETAILS | *\*to be defined* |  |
| FEATURE\_ID | *\*to be defined* |  |
| FEATURE\_SET | *\*to be defined* |  |
| FEATURE\_VALUE | *\*to be defined* |  |
| FIRST | Not Supported | The statement used to indicate that only the **first** or **last** values of the ***aggregate function*** will be returned is not supported. Outputs an **error**. |
| FIRST\_VALUE | FIRST\_VALUE | A warning is being added to indicate the Snowflake counterpart may not be functionally equivalent. |
| FLOOR | FLOOR |  |
| FROM\_TZ | *\*to be defined* |  |
| GREATEST | GREATEST |  |
| GROUP\_ID | *\*to be defined* |  |
| GROUPING | GROUPING |  |
| GROUPING\_ID | GROUPING\_ID |  |
| HEXTORAW | *\*to be defined* |  |
| INITCAP | INITCAP |  |
| INSTR | POSITION | The order of the ***‘string’*** parameter and the ***‘substring’*** parameter is inverted. Also, the *‘**occurrence’*** parameter is removed because it is not supported and a **warning** is added. |
| ITERATION\_NUMBER | *\*to be defined* |  |
| JSON\_ARRAY | *\*to be defined* |  |
| JSON\_ARRAYAGG | *\*to be defined* |  |
| JSON | *\*to be defined* |  |
| JSON\_MERGE\_PATCH | *\*to be defined* |  |
| JSON\_OBJECT | *\*to be defined* |  |
| JSON\_OBJECTAGG | *\*to be defined* |  |
| JSON\_QUERY | *\*to be defined* |  |
| JSON\_SCALAR | *\*to be defined* |  |
| JSON\_SERIALIZE | *\*to be defined* |  |
| JSON\_TABLE | Not Supported | Outputs an error: ***JSON\_TABLE IS NOT SUPPORTED.*** |
| JSON\_TRANSFORM | *\*to be defined* |  |
| JSON\_VALUE | [*JSON\_VALUE\_UDF*](custom_udfs.html#json-value-udf) |  |
| KURTOSIS\_POP | *\*to be defined* |  |
| KURTOSIS\_SAMP | *\*to be defined* |  |
| LAG | LAG | When the value expression comes with the ***RESPECT*** |
| LAST | Not Supported | The statement used to indicate that only the **first** or **last** values of the ***aggregate function*** will be returned is not supported. Outputs an **error**. |
| LAST\_DAY | LAST\_DAY |  |
| LAST\_VALUE | LAST\_VALUE | A warning is being added to indicate the Snowflake counterpart may not be functionally equivalent. |
| LEAD | LEAD | When the value expression comes with the ***RESPECT | IGNORE NULLS** statement,* the statement is moved outside the parenthesis in order to match the Snowflake grammar. |
| LEAST | LEAST |  |
| LENGTH | LENGTH |  |
| LISTAGG | LISTAGG | The ***overflow clause*** is removed from the function. |
| LN | LN |  |
| LNNVL | *\*to be defined* |  |
| LOCALTIMESTAMP | LOCALTIMESTAMP |  |
| LOG | LOG |  |
| LOWER | LOWER |  |
| LPAD | LPAD |  |
| LTRIM | LTRIM |  |
| MAKE\_REF | *\*to be defined* |  |
| MAX | MAX |  |
| MEDIAN | MEDIAN |  |
| MIN | MIN |  |
| MOD | MOD |  |
| MONTHS\_BETWEEN | MONTHS\_BETWEEN\_UDF | Converted to a ***user-defined function***. |
| NANVL | *\*to be defined* |  |
| NCHR | *\*to be defined* |  |
| NEW\_TIME | *\*to be defined* |  |
| NEXT\_DAY | NEXT\_DAY |  |
| NLS\_CHARSET\_DESCL\_LEN | *\*to be defined* |  |
| NLS\_CHARSET\_ID | *\*to be defined* |  |
| NLS\_CHARSET\_NAME | *\*to be defined* |  |
| NLS\_COLLATION\_ID | *\*to be defined* |  |
| NLS\_COLLATION\_NAME | *\*to be defined* |  |
| NLS\_INITCAP | *\*to be defined* |  |
| NLS\_LOWER | *\*to be defined* |  |
| NLS\_UPPER | *\*to be defined* |  |
| NLSSORT | COLLATE  Not Supported | When the function is outside of a ***‘where’*** or ***‘order by’*** clause, it is not supported and it is converted to stub ***‘NLSSORT\_STUB’*** and an **error** is added. Otherwise, if the function is inside a ***‘where’*** or ***‘order by’*** clause, it is converted to the ***COLLATE*** function. |
| NTH\_VALUE | NTH\_VALUE |  |
| NTILE | NTILE |  |
| NULLIF | NULLIF |  |
| NUMTODSINTERVAL | Not Supported | While the function itself is not supported, some usages can be migrated manually. For example DATEADD can be used to manually migrate a sum between a Date/Timestamp and this function. |
| NUMTOYMINTERVAL | Not Supported | While the function itself is not supported, some usages can be migrated manually. For example DATEADD can be used to manually migrate a sum between a Date/Timestamp and this function. |
| NVL | NVL |  |
| NVL2 | NVL2 |  |
| ORA\_DM\_PARTITION\_NAME | *\*to be defined* |  |
| ORA\_DST\_AFFECTED | *\*to be defined* |  |
| ORA\_DST\_CONVERTED | *\*to be defined* |  |
| ORA\_DST\_ERROR | *\*to be defined* |  |
| ORA\_HASH | Not Supported | Converted to a stub ***‘ORA\_HASH\_STUB’*** and an **error** is added. |
| PATH | *\*to be defined* |  |
| PERCENT\_RANK | PERCENT\_RANK | A warning is being added to indicate the Snowflake counterpart may not be functionally equivalent. |
| PERCENTILE\_CONT | PERCENTILE\_CONT |  |
| PERCENTILE\_DISC | PERCENTILE\_DISC |  |
| POWER | POWER |  |
| POWERMULTISET | *\*to be defined* |  |
| POWERMULTISET\_BY\_CARDINALITY | *\*to be defined* |  |
| PREDICTION | *\*to be defined* |  |
| PREDICTION\_BOUNDS | *\*to be defined* |  |
| PREDICTION\_COST | *\*to be defined* |  |
| PREDICTION\_DETAILS | *\*to be defined* |  |
| PREDICTION\_PROBABILITY | *\*to be defined* |  |
| PREDICTION\_SET | *\*to be defined* |  |
| PRESENTNNV | *\*to be defined* |  |
| PRESENTV | *\*to be defined* |  |
| PREVIOUS | *\*to be defined* |  |
| RANK | RANK | There are two kinds of syntax, ***aggregate syntax***, and ***analytic syntax***. The ***aggregate syntax*** is not supported and an **error** is added. The analytic syntax is supported but the ***‘SIBLINGS’*** keyword is removed from the ***‘order by’*** ***clause*** and a **warning** is added. |
| RATIO\_TO\_REPORT | RATIO\_TO\_REPORT |  |
| RAWTOHEX | *\*to be defined* |  |
| RAWTONHEX | *\*to be defined* |  |
| REF | *\*to be defined* |  |
| REFTOHEX | *\*to be defined* |  |
| REGEXP\_COUNT | REGEXP\_COUNT |  |
| REGEXP\_INSTR | REGEXP\_INSTR |  |
| REGEXP\_REPLACE | REGEXP\_REPLACE | In the ***replace\_string*** parameter (the third one) is being added an extra **’’** symbol to escape the other one. In the ***match\_param*** parameter (last one) the equivalence works like this: **’c’ -> ‘c’** *specifies case-sensitive* **’i’ -> ‘i’** *specifies case-insensitive* **’n’ -> ‘s’** *allows the period(.), which is the match-any-character character, to match the newline character* **’m’ -> ‘m’** *treats the source string as multiple lines* **’x’ -> ‘e’** *ignores whitespace characters* |
| REGEXP\_SUBSTR | REGEXP\_SUBSTR | In the ***replace\_string*** parameter (the second one) is being added an extra **’’** symbol to escape the other one. In the ***match\_param*** parameter the equivalence works like this: **’c’ -> ‘c’** *specifies case-sensitive* **’i’ -> ‘i’** *specifies case-insensitive* **’n’ -> ‘s’** *allows the period(.), which is the match-any-character character, to match the newline character* **’m’ -> ‘m’** *treats the source string as multiple lines* **’x’ -> ‘e’** *ignores whitespace characters* |
| REGR | REGR | A warning is being added to indicate the Snowflake counterpart may not be functionally equivalent. |
| REMAINDER | *\*to be defined* |  |
| REPLACE | REPLACE |  |
| REVERSE | REVERSE |  |
| ROUND | ROUND |  |
| ROUND\_TIES\_TO\_EVEN | *\*to be defined* |  |
| ROW\_NUMBER | ROW\_NUMBER |  |
| RPAD | RPAD |  |
| ROWIDTOCHAR | *\*to be defined* |  |
| ROWIDTONCHAR | *\*to be defined* |  |
| RTRIM | RTRIM |  |
| SCN\_TO\_TIMESTAMP | *\*to be defined* |  |
| SESSIONTIMEZONE | *\*to be defined* |  |
| SET | *\*to be defined* |  |
| SIGN | SIGN |  |
| SINH | SINH |  |
| SKEWNESS\_POP | *\*to be defined* |  |
| SKEWNESS\_SAMP | *\*to be defined* |  |
| SOUNDEX | SOUNDEX |  |
| SQRT | SQRT |  |
| STANDARD\_HASH | *\*to be defined* |  |
| STATS\_BINOMIAL\_TEST | *\*to be defined* |  |
| STATS\_CROSSTAB | *\*to be defined* |  |
| STATS\_F\_TEST | *\*to be defined* |  |
| STATS\_KS\_TEST | *\*to be defined* |  |
| STATS\_MODE | *\*to be defined* |  |
| STATS\_MW\_TEST | *\*to be defined* |  |
| STATS\_ONE\_WAY\_ANOVA | *\*to be defined* |  |
| STATS\_T\_TEST | *\*to be defined* |  |
| STATS\_WSR\_TEST | *\*to be defined* |  |
| STDDEV | STDDEV |  |
| STDDEV\_POP | STDDEV\_POP |  |
| STDDEV\_SAMP | STDDEV\_SAMP |  |
| SUBSTR | SUBSTR | All the types of SUBSTR ***(SUBSTRB, SUBSTRC, SUBSTR2, SUBSTR4)*** are being converted to **SUBSTR** |
| SUM | SUM |  |
| SYS\_CONNECT\_BY\_PATH | *\*to be defined* |  |
| SYS\_CONTEXT | CURRENT\_USER CURRENT\_SCHEMA CURRENT\_DATABASE IS\_ROLE\_IN\_SESSION CURRENT\_CLIENT CURRENT\_SESSION Not supported | Depending on the parameters of the function SYS\_CONTEXT, it is converted to one of the specified functions. ***’CURRENT\_SCHEMA’*** converted to ***CURRENT\_SCHEMA()***  ***’CURRENT\_USER’*** converted to ***CURRENT\_USER()***  ***’DB\_NAME’*** converted to ***CURRENT\_DATABASE()***  ***’ISDBA’*** converted to ***IS\_ROLE\_IN\_SESSION(‘DBA’)***  ***’SERVICE\_NAME’*** converted to ***CURRENT\_CLIENT()***  ***’SESSIONID’*** converted to ***CURRENT\_SESSION()***  ***’GUEST’*** converted to ***IS\_ROLE\_IN\_SESSION(‘GUEST’)***  ***’SESSION\_USER’*** converted to ***CURRENT\_USER()***  ***’AUTHENTICATED\_IDENTITY’*** converted to ***CURENT\_USER()***  When a parameter is not supported it is converted to stub ***’SYS\_CONTEXT\_STUB’*** |
| SYS\_DBURIGEN | *\*to be defined* |  |
| SYS\_EXTRACT\_UTC | *\*to be defined* |  |
| SYS\_GUID | *\*to be defined* |  |
| SYS\_OP\_ZONE\_ID | *\*to be defined* |  |
| SYS\_TYPEID | *\*to be defined* |  |
| SYS\_XMLAGG | *\*to be defined* |  |
| SYS\_XMLGEN | *\*to be defined* |  |
| TAN | TAN |  |
| TANH | TANH |  |
| TIMESTAMP\_TO\_SCN | *\*to be defined* |  |
| TO\_APPROX\_COUNT\_DISTINCT | *\*to be defined* |  |
| TO\_APPROX\_PERCENTILE | *\*to be defined* |  |
| TO\_BINARY\_DOUBLE | *\*to be defined* |  |
| TO\_BINARY\_FLOAT | *\*to be defined* |  |
| TO\_BLOB (bfile) | *\*to be defined* |  |
| TO\_BLOB (raw) | *\*to be defined* |  |
| TO\_CHAR (character) | TO\_CHAR |  |
| TO\_CHAR (datetime) | TO\_CHAR(datetime) Conditional Expression(CASE) Not Supported | Depending on the format parameter, the function is converted to **conditional expression** ***(CASE WHEN)*** or a ***user-defined function*** or kept as ***TO\_CHAR(datetime)***. Sometimes the function will be between another function to get an equivalent result. When the function is not supported it is converted to stub ***‘TO\_CHAR\_STUB’***. Go to To\_Char(datetime) to get more information about this function. |
| TO\_CHAR (number) | TO\_CHAR (number) | If the ***numeric*** parameter is of type ***double*** or ***float*** the function is commented out and an error is added. When comes a format not supported, the ***format*** parameter is removed from the function and an error is added. Not supported formats: ***C L PR RN TM U V***. If the function has the ***nlsparam*** parameter, it is removed from the function and an error is added. |
| TO\_CLOB ( bfile | blob ) | TO\_VARCHAR | Outputs a **warning** to indicate the ***bfile/blob*** parameters are considered ***binary***. Also outputs an **error** when the function has more than one parameter. |
| TO\_CLOB (character) | TO\_VARCHAR | Outputs a **warning** to indicate the ***bfile/blob*** parameters are considered ***binary***. Also outputs an **error** when the function has more than one parameter. |
| TO\_DATE | TO\_DATE | When comes a ***format*** not supported, the function is commented out and an error is added. Not supported formats: ***FXFMDD-MON-YYYY*** ***J*** ***DDD*** ***MONTH*** ***RM*** ***DD-MON-RR*** ***DD-MON-RRRR*** ***SSSSS*** ***YYYY*** ***YYY*** ***Y*** |
| TO\_DSINTERVAL | *\*to be defined* |  |
| TO\_LOB | *\*to be defined* |  |
| TO\_MULTI\_BYTE | *\*to be defined* |  |
| TO\_NCHAR | *\*to be defined* |  |
| TO\_NCHAR (datetime) | *\*to be defined* |  |
| TO\_NCLOB | *\*to be defined* |  |
| TO\_NUMBER | TO\_NUMBER  Not Supported | The ‘***DEFAULT integer ON CONVERSION ERROR’*** statement is removed and outputs an error,  Converted to a stub ***TO\_NUMBER\_STUB*** and an error is added when the ***’format’*** parameter is not supported and also when the function has the ***’nlsparam’*** parameter. |
| TO\_SINGLE\_BYTE | *\*to be defined* |  |
| TO\_TIMESTAMP | TO\_DATE | When comes a ***format*** not supported, the function is commented out and an error is added. Not supported formats: ***FXFMDD-MON-YYYY*** ***J*** ***DDD*** ***MONTH*** ***RM*** ***DD-MON-RR*** ***DD-MON-RRRR*** ***SSSSS*** ***YYYY*** ***YYY*** ***Y*** |
| TO\_TIMESTAMP\_TZ | TO\_DATE | When comes a ***format*** not supported, the function is commented out and an error is added. Not supported formats: ***FXFMDD-MON-YYYY*** ***J*** ***DDD*** ***MONTH*** ***RM*** ***DD-MON-RR*** ***DD-MON-RRRR*** ***SSSSS*** ***YYYY*** ***YYY*** ***Y*** |
| TO\_UTC\_TIMESTAMP\_TZ | *\*to be defined* |  |
| TO\_YMINTERVAL | *\*to be defined* |  |
| TRANSLATE | TRANSLATE |  |
| TRANSLATE\_USING | TRANSLATE\_USING |  |
| TREAT | *\*to be defined* |  |
| TRIM | TRIM  LTRIM  RTRIM | Depending on the first parameter it will be converted to: ***LEADING*** keyword -> ***LTRIM TRAILING*** keyword -> ***RTRIM BOTH*** keyword -> ***TRIM*** None of these keywords -> keep as **TRIM** function. Also, the order of the ***’trimsource’*** parameter and the **’trimcharacter**’ parameter is inverted, and the ***FROM*** keyword is removed from the function. |
| TRUNC (date) | TRUNC(date) | *‘**DAY’*** expression is added as a second parameter of the function. |
| TRUNC (number) | TRUNC(number) |  |
| TZ\_OFFSET | *\*to be defined* |  |
| UID | *\*to be defined* |  |
| UNISTR | TO\_VARCHAR(expr) | In the ***expr*** parameter is being added the **‘u’** letter after every **‘'** symbol. |
| UPPER | UPPER |  |
| USER | *\*to be defined* |  |
| USERNV | *\*to be defined* |  |
| VALIDATE\_CONVERSION | *\*to be defined* |  |
| VALUE | Not Supported | Converted to a stub ***‘VALUE\_STUB’*** and an **error** is added. |
| VAR\_POP | VAR\_POP |  |
| VAR\_SAMP | VAR\_SAMP |  |
| VARIANCE | VARIANCE | A warning is being added to indicate the Snowflake counterpart may not be functionally equivalent. |
| VSIZE | *\*to be defined* |  |
| WIDTH\_BUCKET | WIDTH\_BUCKET |  |
| XMLAGG | *\*to be defined* |  |
| XMLCAST | *\*to be defined* |  |
| XMLCDATA | *\*to be defined* |  |
| XMLCOLATVAL | *\*to be defined* |  |
| XMLCOMMENT | *\*to be defined* |  |
| XMLCONCAT | *\*to be defined* |  |
| XMLDIFF | *\*to be defined* |  |
| XMLELEMENT | *\*to be defined* |  |
| XMLEXISTS | *\*to be defined* |  |
| XMLFOREST | *\*to be defined* |  |
| XMLISVALID | *\*to be defined* |  |
| XMLPARSE | *\*to be defined* |  |
| XMLPATCH | *\*to be defined* |  |
| XMLPI | *\*to be defined* |  |
| XMLQUERY | Not Supported |  |
| XMLSEQUENCE | Not Supported | Converted to a stub ***‘XMLSEQUENCE\_STUB’*** and an **error** is added. |
| XMLSERIALIZE | *\*to be defined* |  |
| XMLTABLE | Not Supported | Outputs an error: ***XMLTABLE IS NOT SUPPORTED***. |
| XMLTRANSFORM | *\*to be defined* |  |

## Functions Details.[¶](#functions-details "Link to this heading")

### To\_Char(datetime)[¶](#to-char-datetime "Link to this heading")

According to the format parameter, the function will be converted to:

| Format | Conversion |
| --- | --- |
| AD or BC  A.D. or B.C. | The function will be converted to a ***conditional expression*** ***(CASE)*** where the **format** is added as a result of the ***’when’*** condition. **For Example:** `from: To_Char(DATE ‘1998-12-25’, ‘AD’)` `to: CASE WHEN YEAR(DATE ‘1998-12-25’) < 0 THEN`**`’BC’`** |
| CC or SCC | The function will be converted to a ***conditional expression*** where the original function body is added as a ***when*** condition but it will be between  a ***MOD*** function, after that the original function is added as a ***then*** result but contained by a ***SUBSTR*** function. **For example:**  `from: To_Char(DATE ‘1998-12-25’,’CC’)` `to: CASE WHEN MOD(YEAR(DATE ‘1998-12-25’), 100) = 0` `THEN SUBSTR(TO_CHAR(DATE ‘1998-12-25’, ‘YYYY’), 1, 2)` |
| D | The function will be converted to the snowflake function equivalent but the function body will be between the ***DAYOFWEEK*** datetime part.  **For Example:**  `from: To_Char(DATE ‘1998-12-25’,’D’)`  `to: TO_CHAR(DAYOFWEEK(DATE ‘1998-12-25’) + 1)` |
| DAY | The function will be converted to a ***user-defined function*** inside of an ***UPPER*** function. **For Example:** `from: To_Char(DATE ‘1998-12-25’,’DAY’)`  `to: UPPER(SNOWCONVERT.PUBLIC.FULL_DAY_NAME_UDF(DATE ‘1998-12-25’))` |
| DDD | The function will be converted to the snowflake function equivalent but the function body will be between the ***DAYOFYEAR*** datetime part.  **For Example:** `from: To_Char(DATE ‘1998-12-25’,’DDD’)`  `to: TO_CHAR(DAYOFYEAR(DATE ‘1998-12-25’))` |
| DD-MON-RR | The function will be converted to the snowflake function equivalent keeping the  function body but changing the format to: *’DD-MON-YY’.*  **For Example:**  `from: To_Char(TIMESTAMP ‘1998-12-25 09:26:50.12’,’DD-MON-RR’)`  `to: To_Char(TIMESTAMP ‘1998-12-25 09:26:50.12’,’DD-MON-YY’)` |
| DL | The function will be converted to a ***user-defined function*** plus the ***’OR’*** operator plus snowflake equivalent keeping the function body but changing the format  to: *’**, MMM DD, YYYY***  **For example:**  `from: To_Char(DATE ‘1998-12-25’,’DL’)`  `to: SNOWCONVERT.PUBLIC.FULL_DAY_NAME_UDF(DATE ‘1998-12-25’)` |
| DS | The function will be converted to a combination of the snowflake function  equivalent inside of the ***LTRIM*** function and the snowflake function equivalent.  All the parts combined with the ***’OR’*** operator.  **For Example:**  `from: To_Char(DATE ‘1998-12-25’,’DS’)`  `to: LTRIM(TO_CHAR(DATE ‘1998-12-25’, ‘MM’), ‘0’)` |
| DY | The function will be converted to the snowflake function equivalent  inside of the ***UPPER*** function.  **For example:** `from: To_Char(DATE ‘1998-12-25’,’DY’)` `to: UPPER(TO_CHAR(DATE ‘1998-12-25’, ‘DY’))` |
| I | The function will be converted to into the snowflake function equivalent  inside of the ***SUBSTR*** function.  **For Example:**  `from: To_Char(DATE ‘1998-12-25’,’I’)`  `to: SUBSTR(TO_CHAR(DATE ‘1998-12-25’, ‘YYYY’), 4, 1)` |
| IW | The function will be converted to the snowflake function equivalent but the function body will be between the ***WEEKISO*** datetime part.  **For Example:**  `from:To_Char(DATE ‘1998-12-25’,’IW’)`  `to: TO_CHAR(WEEKISO(DATE ‘1998-12-25’))` |
| IY | The function will be converted to the snowflake function equivalent keeping the  function body but changing the format to: ***’YY’**.*  **For example:**  `from:To_Char(DATE ‘1998-12-25’, ‘IY’)`  `to: TO_CHAR(DATE ‘1998-12-25’, ‘YY’)` |
| IYY | The function will be converted to the snowflake function equivalent  inside of the ***SUBSTR*** function and change the format to: ***’YYYY’***.  **For Example:**  `from: To_Char(DATE ‘1998-12-25’,’IYY’)`  `to: SUBSTR(TO_CHAR(DATE ‘1998-12-25’, ‘YYYY’), 2, 3)` |
| IYYY | The function will be converted to the snowflake function equivalent keeping the  function body but changing the format to: ***’YYYY’**.*  **For example:**  `from:To_Char(DATE ‘1998-12-25’, ‘IYYY’)`  `to: TO_CHAR(DATE ‘1998-12-25’, ‘YYYY’)` |
| J | The function will be converted to a conditional expression with ‘B.C.’ as a ***’then’***  result and ***’A.D.***’ as an else result.  **For example:**  `from: To_Char(DATE ‘1998-12-25’,’J’)`  `to:` DATE\_TO\_JULIANDAYS\_UDF(DATE ‘1998-12-25’) |
| MI | The function will be converted to the snowflake equivalent. If the function  argument is ***SYSDATE*** it will be changed to ***CURRENT\_TIMESTAMP***, otherwise,  if it is of type date, the function will return null.  **For Example:**  `from: To_Char(SYSDATE,’MI’);`  `to: To_Char(CURRENT_TIMESTAMP,’MI’)` |
| MON | The function will be converted to the snowflake function equivalent inside of the ***UPPER*** function.  **For Example:**  `from: To_Char(DATE ‘1998-12-25’,’MON’)`  `to: UPPER(TO_CHAR(DATE ‘1998-12-25’, ‘MON’))` |
| MONTH | The function will be converted to the snowflake function equivalent  inside of the ***UPPER*** function and change the format to: ***’MMMM’***.  **For Example:**  `from: To_Char(DATE ‘1998-12-25’,’MONTH’)`  `to: UPPER(TO_CHAR(DATE ‘1998-12-25’, ‘MMMM’))` |
| Q | The function will be converted to the snowflake function equivalent inside of the ***QUARTER*** function.  **For Example:**  `from: To_Char(DATE ‘1998-12-25’,’Q’)`  `to: TO_CHAR(QUARTER(DATE ‘1998-12-25’))` |
| RM | The function will be converted to a ***user-defined function.***  **For Example:**  `from: To_Char(DATE ‘1998-12-25’,’RM’)`  `to: SNOWCONVERT.PUBLIC.ROMAN_MONTH_UDF(DATE ‘1998-12-25’)` |
| RR | The function will be converted to the snowflake function equivalent keeping the  function body but changing the format to: ***’YY’**.*  **For Example:**  `from: To_Char(DATE ‘1998-12-25’,’RR’)`  `to: TO_CHAR(DATE ‘1998-12-25’, ‘YY’)` |
| RR-MON-DD | The function will be converted to the snowflake function equivalent keeping the  function body but changing the format to: ***’YY-MON-DD’**.*  **For Example:**  `from: To_Char(TIMESTAMP ‘1998-12-25 09:26:50.12’,’RR-MON-DD’)`  `to: To_Char(TIMESTAMP ‘1998-12-25 09:26:50.12’,’YY-MON-DD’)` |
| RRRR | The function will be converted to the snowflake function equivalent keeping the  function body but changing the format to: ***’YYYY’**.*  **For Example:**  `from: To_Char(DATE ‘1998-12-25’,’RRRR’)`  `to: TO_CHAR(DATE ‘1998-12-25’, ‘YYYY’)` |
| SS | The function will be converted to a combination of a ***conditional expression*** and the snowflake function equivalent.  All the parts combined with the ***’OR’*** operator. **For Example:** `from: To_Char(TIMESTAMP ‘1998-12-25 09:26:50.12’,’SS’)`  `to: CASE WHEN SECOND(TIMESTAMP ‘1998-12-25 09:26:50.12’) = 0` `THEN ‘00’ WHEN SECOND(TIMESTAMP ‘1998-12-25 09:26:50.12’) < 10` `THEN ‘0’` |
| SSSS | The function will be converted to the snowflake function equivalent but the  function body will be a concatenation of ***SECOND***, ***MINUTE,*** and ***HOUR*** datetime parts.  **For Example:**  `from: To_Char(TIMESTAMP ‘1998-12-25 09:26:50.12’,’SSSS’)`  `to: TO_CHAR(SECOND(TIMESTAMP ‘1998-12-25 09:26:50.12’) +` `MINUTE(TIMESTAMP ‘1998-12-25 09:26:50.12’) * 60 +` `HOUR(TIMESTAMP ‘1998-12-25 09:26:50.12’) * 3600)` |
| TS | The function will be converted to the snowflake function equivalent keeping the  function body but changing the format to: ***’HH:MI:SS PM’**.*  **For Example:**  `from: To_Char(TIMESTAMP ‘1998-12-25 09:26:50.12’,’TS’)`  `to: TO_CHAR(TIMESTAMP ‘1998-12-25 09:26:50.12’, ‘HH:MI:SS PM’)` |
| W | The function will be converted to the ***TRUNC*** function with the ***DAYOFMONTH*** datetime part.  **For Example:**  `from: To_Char(DATE ‘1998-12-25’,’W’)`  `to: TRUNC(DAYOFMONTH(DATE ‘1998-12-25’) / 7 + 1)` |
| WW | The function will be converted to the ***TRUNC*** function with the ***DAYOFYEAR*** datetime part.  **For Example:**  `from: To_Char(DATE ‘1998-12-25’,’WW’)`  `to: TRUNC(DAYOFYEAR(DATE ‘1998-12-25’) / 7 + 1)` |
| Y  YYY | The function will be converted to the snowflake function equivalent  inside of the ***SUBSTR*** function and change the format to: ***’YYYY’***.  **For Example:**  `from: To_Char(DATE ‘1998-12-25’,’Y’)`  `to: SUBSTR(TO_CHAR(DATE ‘1998-12-25’, ‘YYYY’), 4, 1)` |
| Y,YYY | The function will be converted to a combination of the snowflake function equivalent inside of the **SUBSTR** function and a comma symbol. All the parts combined with the ***’OR’*** operator.  **For Example:**  `from: To_Char(DATE ‘1998-12-25’,’Y,YYY’)`  `to: SUBSTR(TO_CHAR(YEAR(DATE ‘1998-12-25’)), 1, 1)` |
| YEAR  SYEAR | The function will be converted to a ***user-defined function*** inside of an ***UPPER*** function.  **For Example:**  `from: To_Char(DATE ‘1998-12-25’,’YEAR’)`  `to: UPPER(SNOWCONVERT.PUBLIC.YEAR_NAME_UDF(DATE ‘1998-12-25’))` |

## MAX KEEP DENSE\_RANK[¶](#max-keep-dense-rank "Link to this heading")

### Description[¶](#description "Link to this heading")

The Oracle `MAX KEEP DENSE_RANK` function is an aggregate function that returns the maximum value from a set of values while considering only the rows that have the first (smallest) rank according to the specified ordering. The `KEEP (DENSE_RANK FIRST ORDER BY ...)` clause filters the rows to include only those with the smallest rank value before applying the MAX function. ([Oracle Aggregate Functions Documentation](https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/Aggregate-Functions.html#GUID-62BE676B-AF18-4E63-BD14-25206FEA0848)).

### Sample Source Pattern[¶](#sample-source-pattern "Link to this heading")

#### Syntax[¶](#syntax "Link to this heading")

##### Oracle[¶](#oracle "Link to this heading")

```
MAX(expression) KEEP (DENSE_RANK FIRST ORDER BY order_by_expression [ASC|DESC])
```

Copy

##### Snowflake SQL[¶](#snowflake-sql "Link to this heading")

```
FIRST_VALUE(expression) OVER (ORDER BY order_by_expression [ASC|DESC])
```

Copy

### Examples[¶](#examples "Link to this heading")

#### Oracle[¶](#id1 "Link to this heading")

**Code:**

```
SELECT department_id,
       MAX(salary) KEEP (DENSE_RANK FIRST ORDER BY hire_date) AS first_hired_max_salary
FROM employees
GROUP BY department_id;
```

Copy

#### Snowflake SQL[¶](#id2 "Link to this heading")

**Code:**

```
SELECT department_id,
       FIRST_VALUE(salary)
       OVER (
       ORDER BY hire_date) AS first_hired_max_salary
FROM
       employees
GROUP BY department_id;
```

Copy

Note

To ensure a deterministic order for the rows in a window function’s results, the ORDER BY clause must include a key or combination of keys that makes each row unique.

## MIN KEEP DENSE\_RANK[¶](#min-keep-dense-rank "Link to this heading")

### Description[¶](#id3 "Link to this heading")

The Oracle `MIN KEEP DENSE_RANK` function is an aggregate function that returns the minimum value from a set of values while considering only the rows that have the last (highest) rank according to the specified ordering. The `KEEP (DENSE_RANK LAST ORDER BY ...)` clause filters the rows to include only those with the highest rank value before applying the MIN function. ([Oracle Aggregate Functions Documentation](https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/Aggregate-Functions.html#GUID-62BE676B-AF18-4E63-BD14-25206FEA0848)).

### Sample Source Pattern[¶](#id4 "Link to this heading")

#### Syntax[¶](#id5 "Link to this heading")

##### Oracle[¶](#id6 "Link to this heading")

```
MIN(expression) KEEP (DENSE_RANK LAST ORDER BY order_by_expression [ASC|DESC])
```

Copy

##### Snowflake SQL[¶](#id7 "Link to this heading")

```
LAST_VALUE(expression) OVER (ORDER BY order_by_expression [ASC|DESC])
```

Copy

### Examples[¶](#id8 "Link to this heading")

#### Oracle[¶](#id9 "Link to this heading")

**Code:**

```
SELECT department_id,
       MIN(salary) KEEP (DENSE_RANK LAST ORDER BY hire_date) AS first_hired_min_salary
FROM employees
GROUP BY department_id;
```

Copy

#### Snowflake SQL[¶](#id10 "Link to this heading")

**Code:**

```
SELECT department_id,
       LAST_VALUE(salary)
       OVER (
       ORDER BY hire_date) AS first_hired_min_salary
FROM
       employees
GROUP BY department_id;
```

Copy

Note

To ensure a deterministic order for the rows in a window function’s results, the ORDER BY clause must include a key or combination of keys that makes each row unique.

## NLSSORT[¶](#nlssort "Link to this heading")

### Description[¶](#id11 "Link to this heading")

NLSSORT returns a collation key for the character value char and an explicitly or implicitly specified collation. A collation key is a string of bytes used to sort char according to the specified collation. The property of the collation keys is that mutual ordering of two such keys generated for the given collation when compared according to their binary order is the same as mutual ordering of the source character values when compared according to the given collation.. ([NLSSORT in Oracle](https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/NLSSORT.html#GUID-781C6FE8-0924-4617-AECB-EE40DE45096D)).

### Sample Source Pattern[¶](#id12 "Link to this heading")

#### Syntax[¶](#id13 "Link to this heading")

##### Oracle[¶](#id14 "Link to this heading")

```
NLSSORT(char [, 'nlsparam' ])
```

Copy

##### Snowflake SQL[¶](#id15 "Link to this heading")

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/collate)

```
COLLATE(<string_expression>, '<collation_specification>')
```

Copy

### Examples[¶](#id16 "Link to this heading")

#### Oracle[¶](#id17 "Link to this heading")

**Code:**

```
CREATE TABLE test (name VARCHAR2(15));
INSERT INTO test VALUES ('Gaardiner');
INSERT INTO test VALUES ('Gaberd');
INSERT INTO test VALUES ('Gaasten');

SELECT *
  FROM test
  ORDER BY NLSSORT(name, 'NLS_SORT = XDanish');
```

Copy

**Result:**

| NAME |
| --- |
| Gaberd |
| Gaardiner. |
| Gaasten |

##### Snowflake SQL[¶](#id18 "Link to this heading")

**Code:**

```
CREATE OR REPLACE TABLE test (name VARCHAR(15))
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

INSERT INTO test
VALUES ('Gaardiner');

INSERT INTO test
VALUES ('Gaberd');

INSERT INTO test
VALUES ('Gaasten');

SELECT *
  FROM
  test
ORDER BY
COLLATE(name, '');
```

Copy

**Result:**

| NAME |
| --- |
| Gaberd |
| Gaardiner |
| Gaasten |

## TO\_NUMBER[¶](#to-number "Link to this heading")

### Description[¶](#id19 "Link to this heading")

Converts an input expression to a fixed-point number. For NULL input, the output is NULL.

#### Arguments[¶](#arguments "Link to this heading")

**Required:**

&#xNAN;*`<expr>`*

An expression of a numeric, character, or variant type.

**Optional:**

*`<format>`*

The SQL format model used to parse the input *`expr`* and return. For more information, see [SQL Format Models](https://docs.snowflake.com/en/sql-reference/sql-format-models).

*`<precision>`*

The maximal number of decimal digits in the resulting number; from 1 to 38. In Snowflake, precision is not used for determination of the number of bytes needed to store the number and does not have any effect on efficiency, so the default is the maximum (38).

*`<scale>`*

The number of fractional decimal digits (from 0 to *`precision`* - 1). 0 indicates no fractional digits (i.e. an integer number). The default scale is 0.

#### Returns[¶](#returns "Link to this heading")

The function returns `NUMBER(`*`precision`*``` ,`` `` ```*`scale`*`)`.

* If the *`precision`* is not specified, then it defaults to 38.
* If the *`scale`* is not specified, then it defaults to 0.

To more information check the [TO\_NUMBER](https://docs.snowflake.com/en/sql-reference/functions/to_decimal) in snowflake documentation.

```
SELECT CAST('123,456E+40' AS NUMBER, '999,999EEE') FROM DUAL;
SELECT CAST('12sdsd3,456E+40' AS NUMBER, '999,999EEE') FROM DUAL;
SELECT CAST('12345sdsd' AS NUMBER, '99999') FROM DUAL;
SELECT CAST('12.345678912345678912345678912345678912' AS NUMBER, '99.999999999999999999999999999999999999') FROM DUAL;
SELECT CAST('               12.345678912345678912345678912345678912' AS NUMBER, '99.999999999999999999999999999999999999') FROM DUAL;
SELECT CAST('               -12.345678912345678912345678912345678912' AS NUMBER, '99.999999999999999999999999999999999999') FROM DUAL;
SELECT CAST('12.34567891234567891234567891234567891267' AS NUMBER, '99.999999999999999999999999999999999999') FROM DUAL;
SELECT CAST('123.456E-40' AS NUMBER, '999.9999EEE') FROM DUAL;
select cast('12,345,678,912,345,678,912,345,678,912,345,678,912' as number, '99,999,999,999,999,999,999,999,999,999,999,999,999') from dual;
SELECT CAST('  123.456E-40' AS NUMBER, '999.9999EEE') FROM DUAL;
select cast('       12,345,678,912,345,678,912,345,678,912,345.678912' as number, '99,999,999,999,999,999,999,999,999,999,999.999999') from dual;

SELECT CAST('12.34567891234567891234567891234567891267+' AS NUMBER, '99.999999999999999999999999999999999999S') FROM DUAL;
select cast('12,345,678,912,345,678,912,345,678,912,345,678,912+' as number, '99,999,999,999,999,999,999,999,999,999,999,999,999S') from dual;

select cast('12.48+' as number, '99.99S') from dual;
select cast('  12.48+' as number, '99.99S') from dual;
select cast('12.48+   ' as number, '99.99S') from dual;

SELECT CAST('123.456+E-2' AS NUMBER, '999.9999SEEE') FROM DUAL;
SELECT CAST('123.456+E-2-' AS NUMBER, '999.9999SEEE') FROM DUAL;

SELECT CAST('12356-' AS NUMBER, '99999S') FROM DUAL;

select cast(' 1.0E+123' as number, '9.9EEEE') from dual;
select cast('1.2E+02' as number, 'FM9.9EEEE') from dual;
select cast('123.45' as number, 'FM999.009') from dual;
select cast('123.00' as number, 'FM999.009') from dual;
select cast(' $123.45' as number, 'L999.99') from dual;
select cast('$123.45' as number, 'FML999.99') from dual;
select cast('1234567890+' as number, '9999999999S') from dual;
```

Copy

```
 SELECT
!!!RESOLVE EWI!!! /*** SSC-EWI-OR0050 - INPUT EXPRESSION IS OUT OF THE RANGE '123,456E+40' ***/!!!
 CAST('123,456E+40' AS NUMBER(38, 18) , '999,999EEE') FROM DUAL;

SELECT
 !!!RESOLVE EWI!!! /*** SSC-EWI-OR0053 - INCORRECT INPUT FORMAT '12sdsd3,456E+40' ***/!!! CAST('12sdsd3,456E+40' AS NUMBER(38, 18) , '999,999EEE') FROM DUAL;

SELECT
 !!!RESOLVE EWI!!! /*** SSC-EWI-OR0053 - INCORRECT INPUT FORMAT '12345sdsd' ***/!!! CAST('12345sdsd' AS NUMBER(38, 18) , '99999') FROM DUAL;

SELECT
 TO_NUMBER('12.345678912345678912345678912345678912', '99.999999999999999999999999999999999999', 38, 36)
FROM DUAL;

SELECT
 TO_NUMBER('               12.345678912345678912345678912345678912', '99.999999999999999999999999999999999999', 38, 36)
FROM DUAL;

SELECT
 TO_NUMBER('               -12.345678912345678912345678912345678912', '99.999999999999999999999999999999999999', 38, 36)
FROM DUAL;

SELECT
 !!!RESOLVE EWI!!! /*** SSC-EWI-OR0050 - INPUT EXPRESSION IS OUT OF THE RANGE '12.34567891234567891234567891234567891267' ***/!!! CAST('12.34567891234567891234567891234567891267' AS NUMBER(38, 18) , '99.999999999999999999999999999999999999') FROM DUAL;

SELECT
 TO_NUMBER('123.456E-40', '999.9999EEE', 38, 37)
FROM DUAL;

select
 TO_NUMBER('12,345,678,912,345,678,912,345,678,912,345,678,912', '99,999,999,999,999,999,999,999,999,999,999,999,999', 38, 0)
from dual;

SELECT
 TO_NUMBER('  123.456E-40', '999.9999EEE', 38, 37)
FROM DUAL;

select
 TO_NUMBER('       12,345,678,912,345,678,912,345,678,912,345.678912', '99,999,999,999,999,999,999,999,999,999,999.999999', 38, 6)
from dual;

SELECT
 !!!RESOLVE EWI!!! /*** SSC-EWI-OR0050 - INPUT EXPRESSION IS OUT OF THE RANGE '12.34567891234567891234567891234567891267+' ***/!!! CAST('12.34567891234567891234567891234567891267+' AS NUMBER(38, 18) , '99.999999999999999999999999999999999999S') FROM DUAL;

select
 TO_NUMBER('12,345,678,912,345,678,912,345,678,912,345,678,912+', '99,999,999,999,999,999,999,999,999,999,999,999,999S', 38, 0)
from dual;

select
 TO_NUMBER('12.48+', '99.99S', 38, 2)
from dual;

select
 TO_NUMBER('  12.48+', '99.99S', 38, 2)
from dual;

select
 TO_NUMBER('12.48+   ', '99.99S', 38, 2)
from dual;

SELECT
 TO_NUMBER('123.456+E-2', '999.9999SEEE', 38, 5)
FROM DUAL;

SELECT
 !!!RESOLVE EWI!!! /*** SSC-EWI-OR0053 - INCORRECT INPUT FORMAT '123.456+E-2-' ***/!!! CAST('123.456+E-2-' AS NUMBER(38, 18) , '999.9999SEEE') FROM DUAL;

SELECT
 TO_NUMBER('12356-', '99999S', 38, 0)
FROM DUAL;

select
 !!!RESOLVE EWI!!! /*** SSC-EWI-OR0050 - INPUT EXPRESSION IS OUT OF THE RANGE ' 1.0E+123' ***/!!! cast(' 1.0E+123' as NUMBER(38, 18) , '9.9EEEE') from dual;

select
 TO_NUMBER('1.2E+02', 'FM9.9EEEE', 38, 0)
from dual;

select
 TO_NUMBER('123.45', 'FM999.009', 38, 2)
from dual;

select
 TO_NUMBER('123.00', 'FM999.009', 38, 2)
from dual;

select
 !!!RESOLVE EWI!!! /*** SSC-EWI-OR0045 - CAST TYPE L AND FML NOT SUPPORTED ***/!!! cast(' $123.45' as NUMBER(38, 18) , 'L999.99') from dual;

select
 !!!RESOLVE EWI!!! /*** SSC-EWI-OR0045 - CAST TYPE L AND FML NOT SUPPORTED ***/!!! cast('$123.45' as NUMBER(38, 18) , 'FML999.99') from dual;

select
 TO_NUMBER('1234567890+', '9999999999S', 38, 0)
from dual;
```

Copy

#### Recommendations[¶](#recommendations "Link to this heading")

* No additional user actions are required.
* If you need more support, you can email us at [snowconvert-support@snowflake.com](mailto:snowconvert-support%40snowflake.com).

### Related EWIs[¶](#related-ewis "Link to this heading")

1. [SSC-EWI-OR0045](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI.html#ssc-ewi-or0045): Cast type L and FML are not supported.
2. [SSC-EWI-OR0050](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI.html#ssc-ewi-or0050): Input Expression is out of the range.
3. [SSC-EWI-OR0053](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI.html#ssc-ewi-or0053): Incorrect input format.

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

1. [Functions Details.](#functions-details)
2. [MAX KEEP DENSE\_RANK](#max-keep-dense-rank)
3. [MIN KEEP DENSE\_RANK](#min-keep-dense-rank)
4. [NLSSORT](#nlssort)
5. [TO\_NUMBER](#to-number)