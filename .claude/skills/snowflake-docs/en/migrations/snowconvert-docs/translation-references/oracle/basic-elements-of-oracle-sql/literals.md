---
auto_generated: true
description: The terms literal and constant value are synonymous and refer to a fixed
  data value. (Oracle SQL Language Reference Literals)
last_scraped: '2026-01-14T16:53:16.609357+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/oracle/basic-elements-of-oracle-sql/literals
title: SnowConvert AI - Oracle - Literals | Snowflake Documentation
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

              - [Literals](literals.md)
              - [Data Types](data-types/README.md)
            - [Pseudocolumns](../pseudocolumns.md)
            - [Built-in Functions](../functions/README.md)
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

[Guides](../../../../../guides/README.md)[Migrations](../../../../README.md)Tools[SnowConvert AI](../../../overview.md)Translation References[Oracle](../README.md)Basic Elements of Oracle SQLLiterals

# SnowConvert AI - Oracle - Literals[¶](#snowconvert-ai-oracle-literals "Link to this heading")

> The terms literal and constant value are synonymous and refer to a fixed data value.  
> ([Oracle SQL Language Reference Literals](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/Literals.html#GUID-192417E8-A79D-4A1D-9879-68272D925707))

## Interval Literal[¶](#interval-literal "Link to this heading")

Interval Literal Not Supported In Current Scenario

### Description[¶](#description "Link to this heading")

Snowflake Intervals can only be used in arithmetic operations. Intervals used in any other scenario are not supported.

#### Example Code[¶](#example-code "Link to this heading")

##### Oracle[¶](#oracle "Link to this heading")

```
SELECT INTERVAL '1-5' YEAR TO MONTH FROM DUAL;
```

Copy

##### Snowflake[¶](#snowflake "Link to this heading")

```
SELECT
!!!RESOLVE EWI!!! /*** SSC-EWI-0107 - INTERVAL LITERAL IS NOT SUPPORTED BY SNOWFLAKE IN THIS SCENARIO  ***/!!!
 INTERVAL '1-5' YEAR TO MONTH FROM DUAL;
```

Copy

### Known Issues[¶](#known-issues "Link to this heading")

No issues were found.

### Related EWIS[¶](#related-ewis "Link to this heading")

1. [SSC-EWI-0107](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0107): Interval Literal Not Supported In Current Scenario.

## Interval Type and Date Type[¶](#interval-type-and-date-type "Link to this heading")

Operation Between Interval Type and Date Type not Supported

### Description[¶](#id1 "Link to this heading")

`INTERVAL YEAR TO MONTH` and `INTERVAL DAY TO SECOND` are not a supported data type, they are transformed to `VARCHAR(20)`. Therefore all arithmetic operations between **Date Types** and the original **Interval Type Columns** are not supported.

Furthermore, operations between an Interval Type and Date Type (in this order) are not supported in Snowflake; and these operations use this EWI as well.

#### Example Code[¶](#id2 "Link to this heading")

##### Oracle[¶](#id3 "Link to this heading")

```
CREATE TABLE table_with_intervals
(
    date_col DATE,
    time_col TIMESTAMP,
    intervalYearToMonth_col INTERVAL YEAR TO MONTH,
    intervalDayToSecond_col INTERVAL DAY TO SECOND
);

-- Date + Interval Y to M
SELECT date_col + intervalYearToMonth_col FROM table_with_intervals;

-- Date - Interval D to S
SELECT date_col - intervalDayToSecond_col FROM table_with_intervals;

-- Timestamp + Interval D to S
SELECT time_col + intervalDayToSecond_col FROM table_with_intervals;

-- Timestamp - Interval Y to M
SELECT time_col - intervalYearToMonth_col FROM table_with_intervals;
```

Copy

##### Snowflake[¶](#id4 "Link to this heading")

```
CREATE OR REPLACE TABLE table_with_intervals
    (
        date_col TIMESTAMP /*** SSC-FDM-OR0042 - DATE TYPE COLUMN HAS A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/,
        time_col TIMESTAMP(6),
        intervalYearToMonth_col VARCHAR(20) !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - INTERVAL YEAR TO MONTH DATA TYPE CONVERTED TO VARCHAR ***/!!!,
        intervalDayToSecond_col VARCHAR(20) !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - INTERVAL DAY TO SECOND DATA TYPE CONVERTED TO VARCHAR ***/!!!
    )
    COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
    ;

    -- Date + Interval Y to M
    SELECT
    !!!RESOLVE EWI!!! /*** SSC-EWI-OR0095 - OPERATION BETWEEN INTERVAL TYPE AND DATE TYPE NOT SUPPORTED ***/!!! date_col + intervalYearToMonth_col FROM
    table_with_intervals;

    -- Date - Interval D to S
SELECT
    !!!RESOLVE EWI!!! /*** SSC-EWI-OR0095 - OPERATION BETWEEN INTERVAL TYPE AND DATE TYPE NOT SUPPORTED ***/!!! date_col - intervalDayToSecond_col FROM
    table_with_intervals;

    -- Timestamp + Interval D to S
SELECT
    !!!RESOLVE EWI!!! /*** SSC-EWI-OR0095 - OPERATION BETWEEN INTERVAL TYPE AND DATE TYPE NOT SUPPORTED ***/!!! time_col + intervalDayToSecond_col FROM
    table_with_intervals;

    -- Timestamp - Interval Y to M
SELECT
    !!!RESOLVE EWI!!! /*** SSC-EWI-OR0095 - OPERATION BETWEEN INTERVAL TYPE AND DATE TYPE NOT SUPPORTED ***/!!! time_col - intervalYearToMonth_col FROM
    table_with_intervals;
```

Copy

#### Recommendations[¶](#recommendations "Link to this heading")

* Implement the UDF to simulate the Oracle behavior.
* Extract the already transformed value that was stored in the column during migration, and use it as a Snowflake [**Interval Constant**](https://docs.snowflake.com/en/sql-reference/data-types-datetime.html#interval-constants) when possible.
* If you need more support, you can email us at [snowconvert-support@snowflake.com](mailto:snowconvert-support%40snowflake.com)

### Related EWIS[¶](#id5 "Link to this heading")

1. [SSC-EWI-0036](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0036): Data type converted to another data type.
2. [SSC-EWI-OR0095](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI.html#ssc-ewi-or0095): Operation Between Interval Type and Date Type not Supported.
3. [SSC-FDM-OR0042](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM.html#ssc-fdm-or0042): Date Type Transformed To Timestamp Has A Different Behavior.

## Text literals[¶](#text-literals "Link to this heading")

### Description[¶](#id6 "Link to this heading")

> Use the text literal notation to specify values whenever `string` appears in the syntax of expressions, conditions, SQL functions, and SQL statements in other parts of this reference.
>
> ([Oracle SQL Language Reference Text literals](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/Literals.html#GUID-1824CBAA-6E16-4921-B2A6-112FB02248DA))

```
[ {N | n} ]
{ '[ c ]...'
| { Q | q } 'quote_delimiter c [ c ]... quote_delimiter'
}
```

Copy

### Sample Source Patterns[¶](#sample-source-patterns "Link to this heading")

#### Empty string (‘’)[¶](#empty-string "Link to this heading")

The empty strings are equivalent to *NULL* in Oracle, so in order to emulate the behavior in Snowflake, the empty strings are converted to *NULL* or *undefined* depending if the literal is used inside a procedure or not.

##### Oracle[¶](#id7 "Link to this heading")

```
SELECT UPPER('') FROM DUAL;
```

Copy

##### Result[¶](#result "Link to this heading")

| UPPER(‘’) |
| --- |
|  |

##### Snowflake[¶](#id8 "Link to this heading")

```
SELECT UPPER(NULL) FROM DUAL;
```

Copy

##### Result[¶](#id9 "Link to this heading")

| UPPER(NULL) |
| --- |
|  |

#### Empty string in stored procedures[¶](#empty-string-in-stored-procedures "Link to this heading")

##### Oracle[¶](#id10 "Link to this heading")

```
CREATE TABLE empty_string_table(
col1 VARCHAR(10),
col2 VARCHAR(10));

CREATE OR REPLACE PROCEDURE null_proc AS
    var1 INTEGER := '';
    var3 INTEGER := null;
    var2 VARCHAR(20) := 'hello';
BEGIN
    var1 := var1 + 456;
    var2 := var2 || var1;
    IF var1 IS NULL THEN
        INSERT INTO empty_string_table VALUES (var1, var2);
    END IF;
END;

CALL null_proc();

SELECT * FROM empty_string_table;
```

Copy

##### Result[¶](#id11 "Link to this heading")

| COL1 | COL2 |
| --- | --- |
|  | hello |

##### Snowflake[¶](#id12 "Link to this heading")

```
CREATE OR REPLACE TABLE empty_string_table (
    col1 VARCHAR(10),
    col2 VARCHAR(10))
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}}'
;

CREATE OR REPLACE PROCEDURE null_proc ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        var1 INTEGER := NULL;
        var3 INTEGER := null;
        var2 VARCHAR(20) := 'hello';
    BEGIN
        var1 := :var1 + 456;
        var2 := NVL(:var2 :: STRING, '') || NVL(:var1 :: STRING, '');
        IF (:var1 IS NULL) THEN
            INSERT INTO empty_string_table
            VALUES (:var1, :var2);
        END IF;
    END;
$$;

CALL null_proc();

SELECT * FROM
    empty_string_table;
```

Copy

##### Result[¶](#id13 "Link to this heading")

| COL1 | COL2 |
| --- | --- |
|  | hello |

#### Empty string in built-in functions[¶](#empty-string-in-built-in-functions "Link to this heading")

Warning

The transformation does not apply when the empty string is used as an argument of the *REPLACE* and *CONCAT* functions in order to keep the functional equivalence.

##### Oracle[¶](#id14 "Link to this heading")

```
SELECT REPLACE('Hello world', '', 'l'), CONCAT('A','') FROM DUAL;
```

Copy

##### Result[¶](#id15 "Link to this heading")

| REPLACE(‘HELLOWORLD’,’’,’L’) | CONCAT(‘A’,’’) |
| --- | --- |
| Hello world | A |

##### Snowflake[¶](#id16 "Link to this heading")

```
SELECT REPLACE('Hello world', '', 'l'), CONCAT('A','') FROM DUAL;
```

Copy

##### Result[¶](#id17 "Link to this heading")

| REPLACE(‘HELLO WORLD’, ‘’, ‘L’) | CONCAT(‘A’,’’) |
| --- | --- |
| Hello world | A |

Note

If the empty strings are replaced by NULL for these cases, the results of the queries will be different.

### Known Issues[¶](#id18 "Link to this heading")

No issues were found.

### Related EWIs[¶](#id19 "Link to this heading")

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

1. [Interval Literal](#interval-literal)
2. [Interval Type and Date Type](#interval-type-and-date-type)
3. [Text literals](#text-literals)