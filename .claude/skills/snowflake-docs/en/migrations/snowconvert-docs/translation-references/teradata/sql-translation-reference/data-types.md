---
auto_generated: true
description: This section shows equivalents between data types in Teradata and in
  Snowflake.
last_scraped: '2026-01-14T16:53:50.967732+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/teradata/sql-translation-reference/data-types
title: SnowConvert AI - Teradata - Data Types | Snowflake Documentation
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

[Guides](../../../../../guides/README.md)[Migrations](../../../../README.md)Tools[SnowConvert AI](../../../overview.md)Translation References[Teradata](../README.md)[Sql Translation Reference](README.md)Data Types

# SnowConvert AI - Teradata - Data Types[¶](#snowconvert-ai-teradata-data-types "Link to this heading")

This section shows equivalents between data types in Teradata and in Snowflake.

## Conversion Table[¶](#conversion-table "Link to this heading")

| Teradata | Snowflake | Notes |
| --- | --- | --- |
| `ARRAY` | `ARRAY` |  |
| `BIGINT` | `BIGINT` | `BIGINT`in Snowflake is an alias for `NUMBER(38,0).`[Check out [note](#integer-data-types)] |
| `BLOB` | `BINARY` | Limited to 8MB. `BLOB`is not supported, warning [SSC-FDM-TD0001](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/teradataFDM.html#ssc-fdm-td0001) is generated |
| `BYTE` | `BINARY` |  |
| `BYTEINT` | `BYTEINT` |  |
| `CHAR` | `CHAR` |  |
| `CLOB` | `VARCHAR` | ​Limited to 16MB. `CLOB`is not supported, warning [SSC-FDM-TD0002](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/teradataFDM.html#ssc-fdm-td0002) is generated |
| `DATE` | `DATE` |  |
| `DECIMAL` | `DECIMAL` |  |
| `DOUBLE PRECISION` | `DOUBLE PRECISION` |  |
| `FLOAT` | `FLOAT` |  |
| `INTEGER` | `INTEGER` | `INTEGER`in Snowflake is an alias for `NUMBER(38,0)`. [Check out [note](#integer-data-types)] |
| `INTERVAL DAY [TO HOUR | MINUTE | SECOND]` | `VARCHAR(20)` | ​Intervals are stored as`VARCHAR`in Snowflake except when used in addition/subtraction. [Check out [note](#integer-data-types)]. |
| `INTERVAL HOUR [TO MINUTE | SECOND]` | `VARCHAR(20)` | ​Intervals are stored as`VARCHAR`in Snowflake except when used in addition/subtraction. [Check out [note](#integer-data-types)]. |
| `INTERVAL MINUTE [TO SECOND]` | `VARCHAR(20)` | ​Intervals are stored as`VARCHAR`in Snowflake except when used in addition/subtraction. [Check out [note](#integer-data-types)]. |
| `INTERVAL SECOND` | `VARCHAR(20)` | ​Intervals are stored as`VARCHAR`in Snowflake except when used in addition/subtraction. [Check out [note](#integer-data-types)]. |
| `INTERVAL YEAR [TO SECOND]` | `VARCHAR(20)` | ​Intervals are stored as`VARCHAR`in Snowflake except when used in addition/subtraction. [Check out [note](#integer-data-types)]. |
| `JSON` | `VARIANT` | Elements inside a JSON are ordered by their keys when inserted in a table. [Check out [note](data-types.md#json-data-type)]. |
| `MBR` | `---` | Not supported |
| `NUMBER` | `NUMBER(38, 18)` |  |
| `PERIOD(DATE)` | `VARCHAR(24)` | Periods are stored as`VARCHAR`in Snowflake. [Check out [note](#integer-data-types)]. |
| `PERIOD(TIME)` | `VARCHAR(34)` | Periods are stored as`VARCHAR`in Snowflake. [Check out [note](#integer-data-types)]. |
| `PERIOD(TIME WITH TIME ZONE)` | `VARCHAR(46)` | Periods are stored as`VARCHAR`in Snowflake. [Check out [note](#integer-data-types)]. |
| `PERIOD(TIMESTAMP)` | `VARCHAR(58)` | Periods are stored as`VARCHAR`in Snowflake. [Check out [note](#integer-data-types)]. |
| `PERIOD(TIMESTAMP WITH TIME ZONE)` | `VARCHAR(58)` | Periods are stored as`VARCHAR`in Snowflake. [Check out [note](#integer-data-types)]. |
| `REAL` | `REAL` |  |
| `SMALLINT` | `​SMALLINT`​ | `SMALLINT` in Snowflake is an alias for `NUMBER(38,0).` [Check out [note](#integer-data-types)] |
| `ST_GEOMETRY` | `GEOGRAPHY` |  |
| `TIME` | `TIME` |  |
| `TIME WITH TIME ZONE` | `TIME` | Warning [SSC-FDM-0005](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0005) is generated. |
| `TIMESTAMP` | `TIMESTAMP` |  |
| `TIMESTAMP WITH TIME ZONE` | `TIMESTAMP_TZ` |  |
| `VARBYTE` | `BINARY` |  |
| `VARCHAR` | `VARCHAR` |  |
| `XML` | `VARIANT` | ​ |

## Notes[¶](#notes "Link to this heading")

Note

See the documentation on Teradata [data types](https://docs.teradata.com/reader/~_sY_PYVxZzTnqKq45UXkQ/I_xWuywcishQ9U3Xal6zjA)

### Integer Data Types[¶](#integer-data-types "Link to this heading")

For the conversion of integer data types (`INTEGER`, `SMALLINT`, and `BIGINT`), each one is converted to the alias in Snowflake with the same name. Each of those aliases converts to `NUMBER(38,0)`, a data type that is considerably larger than the integer datatype. Below is a comparison of the range of values that can be present in each data type:

* Teradata `INTEGER`: -2,147,483,648 to 2,147,483,647
* Teradata `SMALLINT`: -32768 to 32767
* Teradata `BIGINT`: -9,223,372,036,854,775,808 to 9,223,372,036,854,775,807
* Snowflake `NUMBER(38,0)`: -99999999999999999999999999999999999999 to +99999999999999999999999999999999999999

Warning [SSC-EWI-0036](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0036) is generated.

### Interval/Period Data Types[¶](#interval-period-data-types "Link to this heading")

Intervals and Periods are stored as a string (`VARCHAR`) in Snowflake. When converting, SnowConvert AI creates a UDF that recreates the same expression as a string. Warning [SSC-EWI-TD0053](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/teradataEWI.html#ssc-ewi-td0053) is generated.

You can see more of the UDF’s in the public repository of UDF’s currently created by Snowflake SnowConvert.

These UDF’s assume that periods are stored in a `VARCHAR` where the data/time parts are separated by an `*`. For example for a Teradata period like `PERIOD('2018-01-01','2018-01-20')` it should be stored in Snowflake as a `VARCHAR` like `'2018-01-01`\*`2018-01-20'`.

The only exception to the `VARCHAR` transformation for intervals are interval literals used to add/subtract values from a Datetime expression, Snowflake does not have an `INTERVAL` datatype but [interval constants](https://docs.snowflake.com/en/sql-reference/data-types-datetime.html#interval-constants) exist for the specific purpose mentioned. Examples:

Input code:

```
 SELECT TIMESTAMP '2018-05-13 10:30:45' + INTERVAL '10 05:30' DAY TO MINUTE;
```

Copy

Output code:

```
 SELECT
TIMESTAMP '2018-05-13 10:30:45' + INTERVAL '10 DAY, 05 HOUR, 30 MINUTE';
```

Copy

Cases where the interval is being multiplied/divided by a numerical expression are transformed to equivalent `DATEADD` function calls instead:

Input code:

```
 SELECT TIME '03:45:15' - INTERVAL '15:32:01' HOUR TO SECOND * 10;
```

Copy

Output code:

```
 SELECT
DATEADD('SECOND', 10 * -1, DATEADD('MINUTE', 10 * -32, DATEADD('HOUR', 10 * -15, TIME '03:45:15')));
```

Copy

### JSON Data Type[¶](#json-data-type "Link to this heading")

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

## Known Issues [¶](#known-issues "Link to this heading")

No issues were found.

## Related EWIs [¶](#related-ewis "Link to this heading")

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

1. [Conversion Table](#conversion-table)
2. [Notes](#notes)
3. [Known Issues](#known-issues)
4. [Related EWIs](#related-ewis)