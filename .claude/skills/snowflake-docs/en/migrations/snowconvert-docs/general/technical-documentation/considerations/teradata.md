---
auto_generated: true
description: 'Teradata and Snowflake handle calculations differently:'
last_scraped: '2026-01-14T16:52:35.242761+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/considerations/teradata
title: SnowConvert AI - Teradata | Snowflake Documentation
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

          + [About](../../about.md)
          + [Getting Started](../../getting-started/README.md)
          + [Terms And Conditions](../../terms-and-conditions/README.md)
          + [Release Notes](../../release-notes/release-notes/README.md)
          + User Guide

            + [SnowConvert AI](../../user-guide/snowconvert/README.md)
            + [Project Creation](../../user-guide/project-creation.md)
            + [Extraction](../../user-guide/extraction.md)
            + [Deployment](../../user-guide/deployment.md)
            + [Data Migration](../../user-guide/data-migration.md)
            + [Data Validation](../../user-guide/data-validation.md)
            + [Power BI Repointing](../../user-guide/power-bi-repointing-general.md)
            + [ETL Migration](../../user-guide/etl-migration-replatform.md)
          + [Technical Documentation](../README.md)

            - [Considerations](README.md)

              * [Teradata](teradata.md)
            - [Issues And Troubleshooting](../issues-and-troubleshooting/README.md)
            - Function References

              - [SnowConvert AI Udfs](../function-references/snowconvert-udfs.md)
              - [Teradata](../function-references/teradata/README.md)
              - [Oracle](../function-references/oracle/README.md)
              - [Shared](../function-references/shared/README.md)
              - [SQL Server](../function-references/sql-server/README.md)
          + [Contact Us](../../contact-us.md)
          + Others

            + [Using SnowConvert AI In A Ubuntu Docker Image](../../others/using-snowconvert-in-a-ubuntu-docker-image.md)
          + [Frequently Asked Questions (FAQ)](../../frequently-asked-questions-faq.md)")
        + Translation References

          + [General](../../../translation-references/general/README.md)
          + [Teradata](../../../translation-references/teradata/README.md)
          + [Oracle](../../../translation-references/oracle/README.md)
          + [SQL Server-Azure Synapse](../../../translation-references/transact/README.md)
          + [Sybase IQ](../../../translation-references/sybase/README.md)
          + [Hive-Spark-Databricks SQL](../../../translation-references/hive/README.md)
          + [Redshift](../../../translation-references/redshift/README.md)
          + [PostgreSQL-Greenplum-Netezza](../../../translation-references/postgres/README.md)
          + [BigQuery](../../../translation-references/bigquery/README.md)
          + [Vertica](../../../translation-references/vertica/README.md)
          + [IBM DB2](../../../translation-references/db2/README.md)
          + [SSIS](../../../translation-references/ssis/README.md)
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

[Guides](../../../../../guides/README.md)[Migrations](../../../../README.md)Tools[SnowConvert AI](../../../overview.md)General[Technical Documentation](../README.md)[Considerations](README.md)Teradata

# SnowConvert AI - Teradata[¶](#snowconvert-ai-teradata "Link to this heading")

## Numeric Data Operations[¶](#numeric-data-operations "Link to this heading")

### Calculation Precision[¶](#calculation-precision "Link to this heading")

Teradata and Snowflake handle calculations differently:

* Teradata rounds numbers after each calculation step based on the data type:

  + For decimal types, it maintains the larger precision
  + For NUMBER types, it keeps full precision
* Snowflake stores all numbers using the NUMBER data type, maintaining full precision throughout calculations. This can lead to different results compared to Teradata, especially when working with decimal, integer, or float types.

This difference in behavior is not adjusted during code conversion since it’s typically not what developers intend to change.

Teradata: SELECT (1.00/28) \* 15.00 /\* Returns 0.60 \*/

Snowflake will round the result of the division (1.00/28) \* 15.00 to two decimal places:
SELECT (1.00/28) \* 15.00 = 0.535710 = 0.54

### Integer-Integer Division[¶](#integer-integer-division "Link to this heading")

When dividing two integer values, Teradata performs truncation (floor), while Snowflake performs rounding. To maintain consistent behavior during migration, the automated code conversion automatically adds a TRUNC statement in these cases.

Teradata: SELECT (5/3) = 1 /\* Returns 1 since integer division rounds down \*/

Snowflake: When dividing 5 by 3, the result is 1.6666666, which rounds to 2

Truncated Division in Snowflake: SELECT TRUNC(5/3) returns 1

### Banker Rounding[¶](#banker-rounding "Link to this heading")

Teradata offers Banker’s rounding through the ROUNDHALFWAYMAGUP parameter, while Snowflake uses standard rounding methods only.

| SQL | Teradata | Snowflake |
| --- | --- | --- |
| CAST( 1.05 AS DECIMAL(9,1)) | 1.0 | 1.1 |
| CAST( 1.15 AS DECIMAL(9,1)) | 1.2 | 1.2 |
| CAST( 1.25 AS DECIMAL(9,1)) | 1.2 | 1.3 |
| CAST( 1.35 AS DECIMAL(9,1)) | 1.4 | 1.4 |
| CAST( 1.45 AS DECIMAL(9,1)) | 1.4 | 1.5 |
| CAST( 1.55 AS DECIMAL(9,1)) | 1.6 | 1.6 |
| CAST( 1.65 AS DECIMAL(9,1)) | 1.6 | 1.7 |
| CAST( 1.75 AS DECIMAL(9,1)) | 1.8 | 1.8 |
| CAST( 1.85 AS DECIMAL(9,1)) | 1.8 | 1.9 |
| CAST( 1.95 AS DECIMAL(9,1)) | 2.0 | 2.0 |

### Decimal to Integer Conversion[¶](#decimal-to-integer-conversion "Link to this heading")

Teradata and Snowflake handle decimal values differently. While Teradata truncates decimal values, Snowflake rounds them to the nearest integer. To maintain consistency with Teradata’s behavior, the conversion process automatically adds a TRUNC statement.

| SQL | Teradata | Snowflake |
| --- | --- | --- |
| CAST( 1.0 AS INTEGER) | 1 | 1 |
| CAST( 1.1 AS INTEGER) | 1 | 1 |
| CAST( 1.2 AS INTEGER) | 1 | 1 |
| CAST( 1.3 AS INTEGER) | 1 | 1 |
| CAST( 1.4 AS INTEGER) | 1 | 1 |
| CAST( 1.5 AS INTEGER) | 1 | 2 |
| CAST( 1.6 AS INTEGER) | 1 | 2 |
| CAST( 1.7 AS INTEGER) | 1 | 2 |
| CAST( 1.8 AS INTEGER) | 1 | 2 |
| CAST( 1.9 AS INTEGER) | 1 | 2 |

### Number without Precision/Scale[¶](#number-without-precision-scale "Link to this heading")

When a Teradata NUMBER column is defined without specifying scale or precision, it can store decimal values with varying scale (from 0 to 38), as long as the total precision stays within 38 digits. However, Snowflake requires fixed scale and precision values for NUMBER columns. Here’s an example of how numbers are defined in a Teradata table with this flexible format:

```
CREATE MULTISET TABLE DATABASEXYZ.TABLE_NUMS
     (NUM_COL1 NUMBER(*),
      NUM_COL2 NUMBER,
      NUM_COL3 NUMBER(38,*));
```

Copy

The following table shows two examples of values that exceed Snowflake’s column size limits. These values could appear in any of the previously shown Teradata columns.

Value 1: 123,345,678,901,234,567,891,012.0123456789

Value 2: 123.12345678901234567890

These numeric values would require a NUMBER(42, 20) data type, which exceeds Snowflake’s maximum precision limit of 38. Snowflake is currently working on implementing flexible precision and scale functionality.

### Truncation on INSERT for SQL DML Statements[¶](#truncation-on-insert-for-sql-dml-statements "Link to this heading")

Teradata automatically truncates string values that exceed the defined field length during insertion. While SnowConvert AI maintains the same field lengths during conversion (for example, VARCHAR(20) remains VARCHAR(20)), Snowflake does not automatically truncate oversized strings. If your data ingestion process depends on automatic truncation, you will need to manually modify it by adding a LEFT() function. SnowConvert AI intentionally does not add truncation automatically due to the potential impact across the entire codebase.

### Float Default Issue Example:[¶](#float-default-issue-example "Link to this heading")

```
/* <sc-table> TABLE DUMMY.EXAMPLE </sc-table> */
/**** WARNING: SET TABLE FUNCTIONALITY NOT SUPPORTED ****/
CREATE TABLE DUMMY.PUBLIC.EXAMPLE (
LOGTYPE INTEGER,
OPERSEQ INTEGER DEFAULT 0,
RUNTIME FLOAT /**** ERROR: DEFAULT CURRENT_TIME NOT VALID FOR DATA TYPE ****/
);
```

Copy

### Float Data Aggregation[¶](#float-data-aggregation "Link to this heading")

Floating-point numbers are approximate representations of decimal values. Due to these approximations, different database systems may produce slightly different results when performing calculations and aggregations with float data types. This variation occurs because each database system handles floating-point arithmetic and rounding in its own way.

## Other Considerations[¶](#other-considerations "Link to this heading")

### Join Elimination[¶](#join-elimination "Link to this heading")

Snowflake executes SQL queries exactly as written, including all specified joins, regardless of whether they affect the final results. Unlike Snowflake, Teradata can automatically remove unnecessary joins by using primary and foreign key relationships defined in the table structure. This feature in Teradata primarily helps prevent poorly written queries, and it’s usually only a concern when code was specifically written to use this capability. If your existing code was designed to take advantage of Teradata’s join elimination feature, automated code conversion tools cannot address this limitation. In such cases, you may need to redesign parts of your solution.

**Using Window Functions with max() and order by**

#### Teradata behavior and defaults:[¶](#teradata-behavior-and-defaults "Link to this heading")

**Default**: When an ORDER BY clause is present but no ROWS or ROWS BETWEEN clause is specified, Teradata SQL window aggregate functions automatically use **ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING**.

#### Snowflake behavior and defaults:[¶](#snowflake-behavior-and-defaults "Link to this heading")

**Default**: When you use a window aggregate function with an ORDER BY clause but without specifying ROWS or ROWS BETWEEN, Snowflake automatically applies **ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW** as the window frame.

**Example:**

Below is a sample table named TEST\_WIN that shows employee salary data across various departments.

| DEPT\_NM | DEPT\_NO | EMP\_NO | SALARY |
| --- | --- | --- | --- |
| SALES | 10 | 11 | 5000 |
| SALES | 10 | 12 | 6000 |
| HR | 20 | 21 | 1000 |
| HR | 20 | 22 | 2000 |
| PS | 30 | 31 | 7000 |
| PS | 30 | 32 | 9000 |

The following code, when executed in Teradata, calculates the highest salary among all employees, grouped by department.

```
SELECT DEPT_NM, SALARY ,DEPT_NO,
MAX(SALARY) OVER ( ORDER BY DEPT_NO  ) AS MAX_DEPT_SALARY
FROM TEST_WIN;
```

Copy

| DEPT\_NM | SALARY | DEPT\_NO | MAX\_DEPT\_SALARY |
| --- | --- | --- | --- |
| SALES | 6000 | 10 | 9000 |
| SALES | 5000 | 10 | 9000 |
| HR | 2000 | 20 | 9000 |
| HR | 1000 | 20 | 9000 |
| PS | 7000 | 30 | 9000 |
| PS | 9000 | 30 | 9000 |

When executing the converted code using Snowflake-SnowConvert AI, you may notice different results (highlighted values). These differences are expected and align with Snowflake’s default settings.

```
SELECT DEPT_NM, SALARY ,DEPT_NO,
MAX(SALARY) OVER ( ORDER BY DEPT_NO  ) AS MAX_DEPT_SALARY
FROM TEST_WIN;
```

Copy

| DEPT\_NM | SALARY | DEPT\_NO | MAX\_DEPT\_SALARY |
| --- | --- | --- | --- |
| SALES | 5000 | 10 | 6000 |
| SALES | 6000 | 10 | 6000 |
| HR | 1000 | 20 | 6000 |
| HR | 2000 | 20 | 6000 |
| PS | 7000 | 30 | 9000 |
| PS | 9000 | 30 | 9000 |

To achieve identical results as in Teradata, you must specify the ROWS/RANGE value as shown in the code below.

```
SELECT DEPT_NM, SALARY ,DEPT_NO,
MAX(SALARY) OVER ( ORDER BY DEPT_NO RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS MAX_DEPT_SALARY
FROM TEST WIN;
```

Copy

| DEPT\_NM | SALARY | DEPT\_NO | MAX\_DEPT\_SALARY |
| --- | --- | --- | --- |
| SALES | 5000 | 10 | 9000 |
| SALES | 6000 | 10 | 9000 |
| HR | 1000 | 20 | 9000 |
| HR | 2000 | 20 | 9000 |
| PS | 7000 | 30 | 9000 |
| PS | 9000 | 30 | 9000 |

The RANGE/ROWS clause explicitly defines how rows are ordered. You can achieve similar results by removing the ORDER BY clause completely.

## References[¶](#references "Link to this heading")

Snowflake: <https://docs.snowflake.com/en/sql-reference/functions-analytic.html>
Teradata: <https://docs.teradata.com/r/756LNiPSFdY~4JcCCcR5Cw/dIV_fAtkK3UeUIQ5_uucQw>

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

1. [Numeric Data Operations](#numeric-data-operations)
2. [Other Considerations](#other-considerations)
3. [References](#references)