---
auto_generated: true
description: This user-defined function (UDF) is used to subtract a number (which
  is a number of days) from a timestamp.
last_scraped: '2026-01-14T16:52:35.901329+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/function-references/oracle/README
title: SnowConvert AI - Function References for Oracle | Snowflake Documentation
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
              - [Oracle](README.md)
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

[Guides](../../../../../../guides/README.md)[Migrations](../../../../../README.md)Tools[SnowConvert AI](../../../../overview.md)General[Technical Documentation](../../README.md)Function ReferencesOracle

# SnowConvert AI - Function References for Oracle[¶](#snowconvert-ai-function-references-for-oracle "Link to this heading")

## DATEDIFF\_UDF(TIMESTAMP, NUMBER)[¶](#datediff-udf-timestamp-number "Link to this heading")

### Definition[¶](#definition "Link to this heading")

This user-defined function (UDF) is used to subtract a `number` (which is a number of days) from a `timestamp`.

```
PUBLIC.DATEDIFF_UDF(FIRST_PARAM TIMESTAMP, SECOND_PARAM NUMBER)
```

Copy

### Parameters[¶](#parameters "Link to this heading")

`FIRST_PARAM` TIMESTAMP

The `timestamp` that represents the minuend.

`SECOND_PARAM` NUMBER

The number of days that represents the subtrahend.

### Returns[¶](#returns "Link to this heading")

Returns a timestamp with the difference between the `timestamp` and the `number`.

### Usage example[¶](#usage-example "Link to this heading")

Input:

```
SELECT PUBLIC.DATEDIFF_UDF('2024-01-26 22:00:50.708 -0800', 3);
```

Copy

Output:

```
2024-01-23
```

Copy

## DATEDIFF\_UDF(TIMESTAMP, DATE)[¶](#datediff-udf-timestamp-date "Link to this heading")

### Definition[¶](#id1 "Link to this heading")

This user-defined function (UDF) is used to subtract a `date` from a `timestamp`.

```
PUBLIC.DATEDIFF_UDF(FIRST_PARAM TIMESTAMP, SECOND_PARAM DATE)
```

Copy

### Parameters[¶](#id2 "Link to this heading")

`FIRST_PARAM` TIMESTAMP

The `timestamp` that represents the minuend.

`SECOND_PARAM` DATE

The `date` that represents the subtrahend.

### Returns[¶](#id3 "Link to this heading")

Returns an integer with the difference between the `timestamp` and the `date`.

### Usage example[¶](#id4 "Link to this heading")

Input:

```
SELECT PUBLIC.DATEDIFF_UDF('2024-01-26 22:00:50.708 -0800', TO_DATE('2023-01-26'));
```

Copy

Output:

```
365
```

Copy

## DATE\_TO\_JULIAN\_DAYS\_UDF[¶](#date-to-julian-days-udf "Link to this heading")

### Definition[¶](#id5 "Link to this heading")

This user-defined function (UDF) transforms from Gregorian date to Julian date (The number of days since January 1, 4712 BC.).

```
PUBLIC.DATE_TO_JULIAN_DAYS_UDF(INPUT_DATE DATE)
```

Copy

### Parameters[¶](#id6 "Link to this heading")

`INPUT_DATE` DATE

The Gregorian date to transform.

### Returns[¶](#id7 "Link to this heading")

Returns the date representation of the Julian date.

### Migration example[¶](#migration-example "Link to this heading")

Input:

```
Select TO_CHAR(SYSDATE, 'J') as A from DUAL;
```

Copy

Output:

```
Select
PUBLIC.DATE_TO_JULIAN_DAYS_UDF(CURRENT_TIMESTAMP()) as A from DUAL;
```

Copy

### Usage example[¶](#id8 "Link to this heading")

Input:

```
SELECT PUBLIC.DATE_TO_JULIAN_DAYS_UDF(DATE '1998-12-25');
```

Copy

Output:

```
2451173
```

Copy

## UTL\_FILE.PUT\_LINE\_UDF[¶](#utl-file-put-line-udf "Link to this heading")

### Definition[¶](#id9 "Link to this heading")

This user-defined function (UDF) is used to replicate the functionality of the Oracle UTL\_FILE\_PUT\_LINE procedure.

```
UTL_FILE.PUT_LINE_UDF(FILE VARCHAR,BUFFER VARCHAR)
```

Copy

### Parameters[¶](#id10 "Link to this heading")

`FILE` VARCHAR

The file to open and save the new buffer.

`BUFFER` VARCHAR

The buffer to be saved on the defined file.

### Returns[¶](#id11 "Link to this heading")

Returns a varchar with the result.

### Usage example[¶](#id12 "Link to this heading")

Warning

To review the lines in the file, there are two ways: Downloading the file from the Snowflake CLI or briefly review the information with `SELECT * FROM UTL_FILE.FOPEN_TABLES_LINES;` but only if the file has not been closed.

Input:

```
CREATE OR REPLACE PROCEDURE PROC()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
   DECLARE
    file_data  VARIANT;
   BEGIN

    CALL UTL_FILE.FOPEN_UDF('test2.csv','a');

    SELECT
      *
    INTO
      file_data
    FROM
      TABLE(RESULT_SCAN(LAST_QUERY_ID()));

    CALL UTL_FILE.PUT_LINE_UDF(:file_data,'New line');


    CALL UTL_FILE.FCLOSE_UDF(:file_data);


   END
$$;

CALL PROC();
```

Copy

Output:

```
null
```

Copy

## UTL\_FILE.FOPEN\_UDF (VARCHAR,VARCHAR)[¶](#utl-file-fopen-udf-varchar-varchar "Link to this heading")

### Definition[¶](#id13 "Link to this heading")

This user-defined function (UDF) is used to replicate the functionality of the Oracle `UTL_FILE_FOPEN` procedure.

```
UTL_FILE.FOPEN_UDF(FILENAME VARCHAR,OPEN_MODE VARCHAR)
```

Copy

### Parameters[¶](#id14 "Link to this heading")

`FILENAME` VARCHAR

The file to be opened.

`OPEN_MODE` VARCHAR

Indicates de mode on which the file will be available.

### Returns[¶](#id15 "Link to this heading")

Returns a varchar with the result.

### Usage example[¶](#id16 "Link to this heading")

Warning

The `UTL_FILE.FOPEN_UDF` allows to open a .csv file. To access the file it is required to create a `stage` for the file and use the Snowflakr CLI to upload it.

Input:

```
CREATE OR REPLACE PROCEDURE PROC()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
   DECLARE
    file_data  VARIANT;
   BEGIN

    CALL UTL_FILE.FOPEN_UDF('test2.csv','a');

    SELECT
      *
    INTO
      file_data
    FROM
      TABLE(RESULT_SCAN(LAST_QUERY_ID()));


   END
$$;

CALL PROC();
```

Copy

Output:

```
null
```

Copy

## JSON\_VALUE\_UDF[¶](#json-value-udf "Link to this heading")

### Definition[¶](#id17 "Link to this heading")

This user-defined function (UDF) reproduces the JSON\_VALUE function to extract a single result out of a JSON variable.

```
JSON_VALUE_UDF(JSON_OBJECT VARIANT, JSON_PATH STRING, RETURNING_TYPE STRING, ON_ERROR_MESSAGE VARIANT, ON_EMPTY_MESSAGE VARIANT)
```

Copy

### Parameters[¶](#id18 "Link to this heading")

`JSON_OBJECT` VARIANT

The JSON variable from which to extract the values.

`JSON_PATH` STRING

The JSON path that indicates where the values are located inside the JSON\_OBJECT.

`RETURNING_TYPE` STRING

The type to return.

`ON_ERROR_MESSAGE` VARIANT

The error message to add if needed.

`ON_EMPTY_MESSAGE` VARIANT

The error message to add in case of empty message.

### Returns[¶](#id19 "Link to this heading")

Returns a single value specified by the JSON\_PATH inside the JSON\_OBJECT. If the result is not a single value, returns a default error message or an error message defined in the input parameters.

### Usage example[¶](#id20 "Link to this heading")

Input:

```
   SELECT
     JSON_VALUE_UDF(

     PARSE_JSON('{
  "iceCreamOrders": [
    {
      "customerID": "CUST001",
      "orderID": "ORD001",
      "productID": "PROD001",
      "quantity": 2
    }
  ]
}'),

JSON_EXTRACT_PATH_TEXT('{
  "iceCreamOrders": [
    {
      "customerID": "CUST001",
      "orderID": "ORD001",
      "productID": "PROD001",
      "quantity": 2
    }
  ]
}', 'iceCreamOrders'), 'VARIANT', TO_VARIANT('There was an error'), TO_VARIANT('Empty message'));
```

Copy

Output:

```
"Empty message"
```

Copy

## DATEADD\_UDF (FLOAT, TIMESTAMP)[¶](#dateadd-udf-float-timestamp "Link to this heading")

### Definition[¶](#id21 "Link to this heading")

This user-defined function (UDF) is used in cases when there is an addition between a `float` number and a `timestamp`.

```
PUBLIC.DATEADD_UDF(FIRST_PARAM FLOAT, SECOND_PARAM TIMESTAMP)
```

Copy

### Parameters[¶](#id22 "Link to this heading")

`FIRST_PARAM` FLOAT

The timestamp number that is going to be added with the second float parameter.

`SECOND_PARAM` DATE

The float number to be added with the timestamp in the first parameter.

### Returns[¶](#id23 "Link to this heading")

Returns a timestamp with the addition between the timestamp and the float number specified.

### Usage example[¶](#id24 "Link to this heading")

Input:

```
SELECT DATEADD_UDF(1, current_timestamp);
```

Copy

Output:

```
2024-01-30 18:47:16.988
```

Copy

## FETCH\_BULK\_COLLECTIONS\_UDF (OBJECT)[¶](#fetch-bulk-collections-udf-object "Link to this heading")

### Definition[¶](#id25 "Link to this heading")

This user-defined function (UDF) is used to replicate the functionality of fetching bulk for collections in Oracle. This function version receives the cursor only.

```
FETCH_BULK_COLLECTIONS_UDF(CURSOR OBJECT)
```

Copy

### Parameters[¶](#id26 "Link to this heading")

`CURSOR` OBJECT

The cursor that is processed and filled with the data in the `fetch bulk collection`.

### Returns[¶](#id27 "Link to this heading")

Returns an object with information related to the logic of fetching bulk collections.

### Usage example[¶](#id28 "Link to this heading")

Input:

```
CREATE OR REPLACE TABLE MY_TABLE (test VARCHAR(100));
INSERT INTO MY_TABLE VALUES ('TEST_A');

CREATE OR REPLACE PROCEDURE MY_PROCEDURE ()
RETURNS OBJECT
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
    DECLARE
        MY_CURSOR OBJECT := INIT_CURSOR_UDF('MY_CURSOR', '   SELECT * FROM
      MY_TABLE');

    BEGIN
        MY_CURSOR := (
            CALL OPEN_BULK_CURSOR_UDF(:MY_CURSOR)
        );
        MY_CURSOR := (
            CALL FETCH_BULK_COLLECTIONS_UDF(:MY_CURSOR)
        );

        Return MY_CURSOR;
    END;
$$;

CALL MY_PROCEDURE();
```

Copy

Output:

```
{
  "FOUND": true,
  "ISOPEN": true,
  "NAME": "MY_CURSOR",
  "NOTFOUND": false,
  "QUERY": "   SELECT * FROM\n      MY_TABLE",
  "RESULT": [
    [
      "TEST_A"
    ]
  ],
  "ROWCOUNT": 1
}
```

Copy

## DATEADD\_UDF (DATE, FLOAT)[¶](#dateadd-udf-date-float "Link to this heading")

### Definition[¶](#id29 "Link to this heading")

This user-defined function (UDF) is used in cases when there is an addition between a date and a type as `float` or `timestamp`.

```
PUBLIC.DATEADD_UDF(FIRST_PARAM DATE, SECOND_PARAM FLOAT)
```

Copy

### Parameters[¶](#id30 "Link to this heading")

`FIRST_PARAM` DATE

The date to be added with the number in the second parameter.

`SECOND_PARAM` FLOAT

The float number that is going to be added with the first date parameter.

### Returns[¶](#id31 "Link to this heading")

Returns the addition between the date and the float number specified.

### Migration example[¶](#id32 "Link to this heading")

Input:

```
SELECT TO_DATE('05/11/21', 'dd/mm/yy') + 3.4 from dual;
```

Copy

Output:

```
SELECT
PUBLIC.DATEADD_UDF( TO_DATE('05/11/21', 'dd/mm/yy'), 3.4) from dual;
```

Copy

### Usage example[¶](#id33 "Link to this heading")

Input:

```
SELECT DATEADD_UDF('2022-02-14',6);
```

Copy

Output:

```
2022-02-20
```

Copy

## DATEDIFF\_UDF(DATE, TIMESTAMP)[¶](#datediff-udf-date-timestamp "Link to this heading")

### Definition[¶](#id34 "Link to this heading")

This user-defined function (UDF) is used to subtract a `timestamp` from a `date`.

```
PUBLIC.DATEDIFF_UDF(FIRST_PARAM DATE, SECOND_PARAM TIMESTAMP)
```

Copy

### Parameters[¶](#id35 "Link to this heading")

`FIRST_PARAM` DATE

The date over the subtraction is done.

`SECOND_PARAM` TIMESTAMP

The `timestamp` to subtract from the first parameter.

### Returns[¶](#id36 "Link to this heading")

Returns an integer with the days between the first and the second parameter.

### Usage example[¶](#id37 "Link to this heading")

Input:

```
SELECT PUBLIC.DATEDIFF_UDF(TO_DATE('2024-01-26'), '2022-02-14 15:31:00');
```

Copy

Output:

```
711
```

Copy

## DBMS\_RANDOM.VALUE\_UDF[¶](#dbms-random-value-udf "Link to this heading")

### Definition[¶](#id38 "Link to this heading")

This user-defined function (UDF) is to replicate the functionality of the Oracle DBMS\_RANDOM.VALUE function.

```
DBMS_RANDOM.VALUE_UDF()
```

Copy

### Parameters[¶](#id39 "Link to this heading")

No input parameters.

### Returns[¶](#id40 "Link to this heading")

Returns a `double` number with a random number.

### Usage example[¶](#id41 "Link to this heading")

Input:

```
SELECT DBMS_RANDOM.VALUE_UDF();
```

Copy

Output:

```
0.6666235896
```

Copy

## DBMS\_RANDOM.VALUE\_UDF (DOUBLE, DOUBLE)[¶](#dbms-random-value-udf-double-double "Link to this heading")

### Definition[¶](#id42 "Link to this heading")

This user-defined function (UDF) is to replicate the functionality of the Oracle DBMS\_RANDOM.VALUE function.

```
DBMS_RANDOM.VALUE_UDF(low DOUBLE, high DOUBLE)
```

Copy

### Parameters[¶](#id43 "Link to this heading")

`low` DOUBLE

The initial limit to be considered.

`high` DOUBLE

The delimiting limit that coordinates with the first parameter.

### Returns[¶](#id44 "Link to this heading")

Returns a `double` number with a random number between the limits specified.

### Usage example[¶](#id45 "Link to this heading")

Input:

```
SELECT DBMS_RANDOM.VALUE_UDF(1.1, 2.2);
```

Copy

Output:

```
1.637802374
```

Copy

## FETCH\_BULK\_RECORD\_COLLECTIONS\_UDF (OBJECT, ARRAY)[¶](#fetch-bulk-record-collections-udf-object-array "Link to this heading")

### Definition[¶](#id46 "Link to this heading")

This user-defined function (UDF) is used to cover the functionality of `fetch bulk records` with different input parameters that determine the information added or the behavior of the cursor.

```
FETCH_BULK_RECORD_COLLECTIONS_UDF(CURSOR OBJECT, COLUMN_NAMES ARRAY)
```

Copy

### Parameters[¶](#id47 "Link to this heading")

`CURSOR` OBJECT

The cursor that is being processed.

`COLUMN_NAMES` ARRAY

The column names that are associated with the cursor.

### Returns[¶](#id48 "Link to this heading")

Returns an object with the processed information.

### Usage example[¶](#id49 "Link to this heading")

Input:

```
CREATE OR REPLACE TABLE BULKCOLLECTTABLE(test VARCHAR(100));
INSERT INTO BULKCOLLECTTABLE VALUES ('TEST_A');

CREATE OR REPLACE PROCEDURE MY_PROCEDURE ()
RETURNS OBJECT
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
    DECLARE
        MY_CURSOR OBJECT := INIT_CURSOR_UDF('MY_CURSOR', '   SELECT * FROM
      BULKCOLLECTTABLE');

    BEGIN
        MY_CURSOR := (
            CALL OPEN_BULK_CURSOR_UDF(:MY_CURSOR)
        );
        MY_CURSOR := (
            CALL FETCH_BULK_RECORD_COLLECTIONS_UDF(:MY_CURSOR, NULL)
        );

        Return MY_CURSOR;
    END;
$$;

CALL MY_PROCEDURE();
```

Copy

Output:

```
{
  "FOUND": true,
  "ISOPEN": true,
  "NAME": "MY_CURSOR",
  "NOTFOUND": false,
  "QUERY": "   SELECT * FROM\n      BULKCOLLECTTABLE",
  "RESULT": {
    "TEST": [
      "TEST_A"
    ]
  },
  "ROWCOUNT": 1
}
```

Copy

## FETCH\_BULK\_COLLECTION\_RECORDS\_UDF (OBJECT, ARRAY)[¶](#fetch-bulk-collection-records-udf-object-array "Link to this heading")

### Definition[¶](#id50 "Link to this heading")

This user-defined function (UDF) is used to replicate the functionality of FETCH in Oracle. This is the variation where it receives the cursor and the column names.

```
FETCH_BULK_COLLECTION_RECORDS_UDF(CURSOR OBJECT, COLUMN_NAMES ARRAY)
```

Copy

### Parameters[¶](#id51 "Link to this heading")

`CURSOR` OBJECT

The cursor that is processed and filled with the data in the `fetch bulk`.

`COLUMN_NAMES` ARRAY

The name associated with the column is not the initial name.

### Returns[¶](#id52 "Link to this heading")

Returns an object with the records from the `fetch bulk`.

### Usage example[¶](#id53 "Link to this heading")

Input:

```
CREATE OR REPLACE TABLE MY_TABLE (test VARCHAR(100));
INSERT INTO MY_TABLE VALUES ('TEST_A');

CREATE OR REPLACE PROCEDURE MY_PROCEDURE ()
RETURNS OBJECT
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
    DECLARE
        MY_CURSOR OBJECT := INIT_CURSOR_UDF('MY_CURSOR', '   SELECT * FROM
      MY_TABLE');

    BEGIN
        MY_CURSOR := (
            CALL OPEN_BULK_CURSOR_UDF(:MY_CURSOR)
        );
        MY_CURSOR := (
            CALL FETCH_BULK_COLLECTION_RECORDS_UDF(:MY_CURSOR, NULL)
        );

        Return MY_CURSOR;
    END;
$$;

CALL MY_PROCEDURE();
```

Copy

Output:

```
{
  "FOUND": true,
  "ISOPEN": true,
  "NAME": "MY_CURSOR",
  "NOTFOUND": false,
  "QUERY": "   SELECT * FROM\n      MY_TABLE",
  "RESULT": [
    {
      "TEST": "TEST_A"
    }
  ],
  "ROWCOUNT": 1
}
```

Copy

## JULIAN\_TO\_GREGORIAN\_DATE\_UDF[¶](#julian-to-gregorian-date-udf "Link to this heading")

### Definition[¶](#id54 "Link to this heading")

This user-defined function (UDF) is used to transform a Julian date into the formats: JD Edwards, YYYYDDD (astronomical), and YYYYDDD (ordinal).

```
JULIAN_TO_GREGORIAN_DATE_UDF(JULIAN_DATE CHAR(7), FORMAT_SELECTED CHAR(1))
```

Copy

### Parameters[¶](#id55 "Link to this heading")

`JULIAN_DATE` CHAR

The Julian date to transform.

`FORMAT_SELECTED` CHAR

The format required for the logic. E.g. `'E'`, `'J'`, `'R'`. Astronomy standardized or `'J'` is the default format.

### Returns[¶](#id56 "Link to this heading")

Returns a variant with the date representation of the Julian date.

### Usage example[¶](#id57 "Link to this heading")

Input:

```
SELECT JULIAN_TO_GREGORIAN_DATE_UDF('098185');
```

Copy

Output:

```
'1998-07-04' --(a.k.a Sat Jul 04 1998)
```

Copy

## TIMESTAMP\_DIFF\_UDF[¶](#timestamp-diff-udf "Link to this heading")

### Definition[¶](#id58 "Link to this heading")

This user-defined function (UDF) is used for the timestamps arithmetic operations and the equivalence functionality in Snowflake.

```
TIMESTAMP_DIFF_UDF(LEFT_TS TIMESTAMP, RIGHT_TS TIMESTAMP )
```

Copy

### Parameters[¶](#id59 "Link to this heading")

LEFT\_TS TIMESTAMP

The minuend value.

RIGHT\_TS TIMESTAMP

The subtrahend value.

### Returns[¶](#id60 "Link to this heading")

Returns a varchar with the resulting difference between timestamps.

### Usage example[¶](#id61 "Link to this heading")

Input:

```
SELECT TIMESTAMP_DIFF_UDF(TO_TIMESTAMP('2024-01-31 11:47:20.532 -0800'), TO_TIMESTAMP('2024-01-31 11:47:20.532 -0800'));
```

Copy

Output:

```
-000000000  00:00:00.00000000
```

Copy

## REGEXP\_LIKE\_UDF (STRING, STRING, STRING)[¶](#regexp-like-udf-string-string-string "Link to this heading")

### Definition[¶](#id62 "Link to this heading")

This user-defined function (UDF) is

```
REGEXP_LIKE_UDF(COL STRING, PATTERN STRING, MATCHPARAM STRING)
```

Copy

### Parameters[¶](#id63 "Link to this heading")

COL STRING

The string to be evaluated with the pattern.

PATTERN STRING

The pattern to be checked.

MATCHPARAM STRING

The match parameter that will determine whether the case-sensitive or not.

### Returns[¶](#id64 "Link to this heading")

Returns

### Usage example[¶](#id65 "Link to this heading")

Input:

```
SELECT REGEXP_LIKE_UDF('san Francisco', 'San* [fF].*', 'i');
```

Copy

Output:

```
TRUE
```

Copy

## FETCH\_BULK\_COLLECTIONS\_UDF (OBJECT, FLOAT)[¶](#fetch-bulk-collections-udf-object-float "Link to this heading")

### Definition[¶](#id66 "Link to this heading")

This user-defined function (UDF) is used to replicate the functionality of fetching bulk for collections in Oracle. This function version receives the cursor and the limit value for the row count.

```
FETCH_BULK_COLLECTIONS_UDF(CURSOR OBJECT, LIMIT FLOAT)
```

Copy

### Parameters[¶](#id67 "Link to this heading")

`CURSOR` OBJECT

The cursor that is processed and filled with the data in the `fetch bulk collection`.

`LIMIT` FLOAT

The limit for the records to call.

### Returns[¶](#id68 "Link to this heading")

Returns an object with information related to the logic of fetching bulk collections.

### Usage example[¶](#id69 "Link to this heading")

Input:

```
CREATE OR REPLACE TABLE MY_TABLE (test VARCHAR(100));
INSERT INTO MY_TABLE VALUES ('TEST_A');

CREATE OR REPLACE PROCEDURE MY_PROCEDURE ()
RETURNS OBJECT
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
    DECLARE
        MY_CURSOR OBJECT := INIT_CURSOR_UDF('MY_CURSOR', '   SELECT * FROM
      MY_TABLE');

    BEGIN
        MY_CURSOR := (
            CALL OPEN_BULK_CURSOR_UDF(:MY_CURSOR)
        );
        MY_CURSOR := (
            CALL FETCH_BULK_COLLECTIONS_UDF(:MY_CURSOR, 1.0)
        );

        Return MY_CURSOR;
    END;
$$;

CALL MY_PROCEDURE();
```

Copy

Output:

```
{
  "FOUND": true,
  "ISOPEN": true,
  "NAME": "MY_CURSOR",
  "NOTFOUND": false,
  "QUERY": "   SELECT * FROM\n      MY_TABLE",
  "RESULT": [
    [
      "TEST_A"
    ]
  ],
  "ROWCOUNT": 1
}
```

Copy

## INIT\_CURSOR\_UDF[¶](#init-cursor-udf "Link to this heading")

### Definition[¶](#id70 "Link to this heading")

This user-defined function (UDF) is to initialize a cursor object with the equivalent functionality.

```
INIT_CURSOR_UDF(NAME VARCHAR, QUERY VARCHAR)
```

Copy

### Parameters[¶](#id71 "Link to this heading")

`NAME` VARCHAR

The name of the cursor.

`QUERY` VARCHAR

The query that is associated with the cursor.

### Returns[¶](#id72 "Link to this heading")

Returns an object with the cursor information.

### Usage example[¶](#id73 "Link to this heading")

Input:

```
CREATE OR REPLACE TABLE BULKCOLLECTTABLE(test VARCHAR(100));

CREATE OR REPLACE PROCEDURE MY_PROCEDURE ()
RETURNS OBJECT
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
    DECLARE
        MY_CURSOR OBJECT := INIT_CURSOR_UDF('MY_CURSOR', '   SELECT * FROM
      BULKCOLLECTTABLE');

    BEGIN
        Return MY_CURSOR;
    END;
$$;

CALL MY_PROCEDURE();
```

Copy

Output:

```
{
  "ISOPEN": false,
  "NAME": "MY_CURSOR",
  "QUERY": "   SELECT * FROM\n      BULKCOLLECTTABLE",
  "ROWCOUNT": -1
}
```

Copy

## UPDATE\_PACKAGE\_VARIABLE\_STATE\_UDF[¶](#update-package-variable-state-udf "Link to this heading")

### Definition[¶](#id74 "Link to this heading")

This user-defined function (UDF) updates the given package variable values. It is a wrapper for the Snowflake SETVARIABLE() function.

```
UPDATE_PACKAGE_VARIABLE_STATE_UDF (VARIABLE VARCHAR, NEW_VALUE VARCHAR)
```

Copy

### Parameters[¶](#id75 "Link to this heading")

`VARIABLE` VARCHAR

The variable name to set the value.

`NEW_VALUE` VARCHAR

The value that will be stored.

### Returns[¶](#id76 "Link to this heading")

Returns a varchar with the information of the updated variable.

### Usage example[¶](#id77 "Link to this heading")

Warning

Please, review the existence of the variable.

Input:

```
CALL PUBLIC.UPDATE_PACKAGE_VARIABLE_STATE_UDF('MY_LOCAL_VARIABLE', '1');
```

Copy

Output:

```
1
```

Copy

## OPEN\_BULK\_CURSOR\_UDF (OBJECT)[¶](#open-bulk-cursor-udf-object "Link to this heading")

### Definition[¶](#id78 "Link to this heading")

This user-defined function (UDF) is used to pen a cursor without bindings.

```
OPEN_BULK_CURSOR_UDF(CURSOR OBJECT)
```

Copy

### Parameters[¶](#id79 "Link to this heading")

`CURSOR` OBJECT

The cursor to process as open.

### Returns[¶](#id80 "Link to this heading")

Returns an object with the current information of the cursor.

### Usage example[¶](#id81 "Link to this heading")

Input:

```
CREATE OR REPLACE TABLE BULKCOLLECTTABLE(test VARCHAR(100));

CREATE OR REPLACE PROCEDURE MY_PROCEDURE ()
RETURNS OBJECT
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
    DECLARE
        MY_CURSOR OBJECT := INIT_CURSOR_UDF('MY_CURSOR', '   SELECT * FROM
      BULKCOLLECTTABLE');

    BEGIN
        MY_CURSOR := (
            CALL OPEN_BULK_CURSOR_UDF(:MY_CURSOR)
        );
        Return MY_CURSOR;
    END;
$$;

CALL MY_PROCEDURE();
```

Copy

Output:

```
{
  "ISOPEN": true,
  "NAME": "MY_CURSOR",
  "QUERY": "   SELECT * FROM\n      BULKCOLLECTTABLE",
  "ROWCOUNT": 0
}
```

Copy

## DATEADD\_UDF (TIMESTAMP, FLOAT)[¶](#dateadd-udf-timestamp-float "Link to this heading")

### Definition[¶](#id82 "Link to this heading")

This user-defined function (UDF) is used in cases when there is an addition between a `timestamp` and a `float` number.

```
PUBLIC.DATEADD_UDF(FIRST_PARAM TIMESTAMP, SECOND_PARAM FLOAT)
```

Copy

### Parameters[¶](#id83 "Link to this heading")

`FIRST_PARAM` TIMESTAMP

The timestamp number that is going to be added with the second float parameter.

`SECOND_PARAM` FLOAT

The float number to be added with the timestamp in the first parameter.

### Returns[¶](#id84 "Link to this heading")

Returns a timestamp with the addition between the timestamp and the float number specified.

### Usage example[¶](#id85 "Link to this heading")

Input:

```
SELECT DATEADD_UDF(current_timestamp, 1);
```

Copy

Output:

```
2024-01-26 13:22:49.354
```

Copy

## DATEDIFF\_UDF(TIMESTAMP, TIMESTAMP)[¶](#datediff-udf-timestamp-timestamp "Link to this heading")

### Definition[¶](#id86 "Link to this heading")

This user-defined function (UDF) subtracts a `timestamp` from another `timestamp`.

```
PUBLIC.DATEDIFF_UDF(FIRST_PARAM TIMESTAMP, SECOND_PARAM TIMESTAMP)
```

Copy

### Parameters[¶](#id87 "Link to this heading")

`FIRST_PARAM` TIMESTAMP

The `timestamp` that represents the minuend.

`SECOND_PARAM` TIMESTAMP

The `timestamp` that represents the subtrahend.

### Returns[¶](#id88 "Link to this heading")

Returns an integer with the difference of days between the first and the second timestamps.

### Usage example[¶](#id89 "Link to this heading")

Input:

```
SELECT PUBLIC.DATEDIFF_UDF('2024-01-26 22:00:50.708 -0800','2023-01-26 22:00:50.708 -0800');
```

Copy

Output:

```
365
```

Copy

## UTL\_FILE.FCLOSE\_UDF[¶](#utl-file-fclose-udf "Link to this heading")

### Definition[¶](#id90 "Link to this heading")

This user-defined function (UDF) is used to replicate the functionality of the Oracle `UTL_FILE_FCLOSE` procedure.

```
UTL_FILE.FCLOSE_UDF(FILE VARCHAR)
```

Copy

### Parameters[¶](#id91 "Link to this heading")

`FILE` VARCHAR

The file to process and close.

### Returns[¶](#id92 "Link to this heading")

Returns a varchar with the result.

### Usage example[¶](#id93 "Link to this heading")

Warning

The `UTL_FILE.FCLOSE_UDF` closes the file that is being processed. To review the result or handle files, it is required to use the Snowflake CLI console. The Snowflake CLI console allows the upload or download of a file.

Input:

```
CREATE OR REPLACE PROCEDURE PROC()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
   DECLARE
    file_data  VARIANT;
   BEGIN

    CALL UTL_FILE.FOPEN_UDF('test2.csv','a');

    SELECT
      *
    INTO
      file_data
    FROM
      TABLE(RESULT_SCAN(LAST_QUERY_ID()));

    CALL UTL_FILE.PUT_LINE_UDF(:file_data,'New line');


    CALL UTL_FILE.FCLOSE_UDF(:file_data);


   END
$$;

CALL PROC();
```

Copy

Output:

```
null
```

Copy

## FETCH\_BULK\_RECORD\_COLLECTIONS\_UDF (OBJECT)[¶](#fetch-bulk-record-collections-udf-object "Link to this heading")

### Definition[¶](#id94 "Link to this heading")

This user-defined function (UDF) is used to cover the functionality of `fetch bulk records` with different input parameters that determine the information added or the behavior of the cursor.

```
FETCH_BULK_RECORD_COLLECTIONS_UDF(CURSOR OBJECT)
```

Copy

### Parameters[¶](#id95 "Link to this heading")

`CURSOR` OBJECT

The cursor that is being processed.

### Returns[¶](#id96 "Link to this heading")

Returns an object with the processed information.

### Usage example[¶](#id97 "Link to this heading")

Input:

```
CREATE OR REPLACE TABLE BULKCOLLECTTABLE(test VARCHAR(100));
INSERT INTO BULKCOLLECTTABLE VALUES ('TEST_A');

CREATE OR REPLACE PROCEDURE MY_PROCEDURE ()
RETURNS OBJECT
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
    DECLARE
        MY_CURSOR OBJECT := INIT_CURSOR_UDF('MY_CURSOR', '   SELECT * FROM
      BULKCOLLECTTABLE');

    BEGIN
        MY_CURSOR := (
            CALL OPEN_BULK_CURSOR_UDF(:MY_CURSOR)
        );
        MY_CURSOR := (
            CALL FETCH_BULK_RECORD_COLLECTIONS_UDF(:MY_CURSOR)
        );

        Return MY_CURSOR;
    END;
$$;

CALL MY_PROCEDURE();
```

Copy

Output:

```
{
  "FOUND": true,
  "ISOPEN": true,
  "NAME": "MY_CURSOR",
  "NOTFOUND": false,
  "QUERY": "   SELECT * FROM\n      BULKCOLLECTTABLE",
  "RESULT": {
    "TEST": [
      "TEST_A"
    ]
  },
  "ROWCOUNT": 1
}
```

Copy

## CAST\_DATE\_UDF[¶](#cast-date-udf "Link to this heading")

### Definition[¶](#id98 "Link to this heading")

The function processes a timestamp in string format to a date. It returns a date with the specified format.

```
PUBLIC.CAST_DATE_UDF(DATESTR STRING)
```

Copy

### Parameters[¶](#id99 "Link to this heading")

`DATESTR` STRING

The date as a `string` to be formatted. The format should be ‘`YYYY-MM-DD"T"HH24:MI:SS.FF'` e.g. `'2024-01-25T23:25:11.120'`.

Please review the following information about formatting [here](https://docs.snowflake.com/en/sql-reference/date-time-input-output#timestamp-formats).

### Returns[¶](#id100 "Link to this heading")

Returns a `date` with the new format applied.

### Usage example[¶](#id101 "Link to this heading")

Input:

```
SELECT PUBLIC.CAST_DATE_UDF('2024-01-25T23:25:11.120');
```

Copy

Output:

```
2024-01-25
```

Copy

## FETCH\_BULK\_COLLECTION\_RECORDS\_UDF (OBJECT, FLOAT, ARRAY)[¶](#fetch-bulk-collection-records-udf-object-float-array "Link to this heading")

### Definition[¶](#id102 "Link to this heading")

This user-defined function (UDF) is used to replicate the functionality of FETCH in Oracle. This is the variation where it receives the cursor, the limit, and the column names.

```
FETCH_BULK_COLLECTION_RECORDS_UDF(CURSOR OBJECT, LIMIT FLOAT, COLUMN_NAMES ARRAY)
```

Copy

### Parameters[¶](#id103 "Link to this heading")

`CURSOR` OBJECT

The cursor that is processed and filled with the data in the `fetch bulk`.

`LIMIT` FLOAT

The limit for the records to call.

`COLUMN_NAMES` ARRAY

The name associated with the column is not the initial name.

### Returns[¶](#id104 "Link to this heading")

Returns an object with the records from the `fetch bulk`.

### Usage example[¶](#id105 "Link to this heading")

Input:

```
CREATE OR REPLACE TABLE MY_TABLE (test VARCHAR(100));
INSERT INTO MY_TABLE VALUES ('TEST_A');

CREATE OR REPLACE PROCEDURE MY_PROCEDURE ()
RETURNS OBJECT
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
    DECLARE
        MY_CURSOR OBJECT := INIT_CURSOR_UDF('MY_CURSOR', '   SELECT * FROM
      MY_TABLE');

    BEGIN
        MY_CURSOR := (
            CALL OPEN_BULK_CURSOR_UDF(:MY_CURSOR)
        );
        MY_CURSOR := (
            CALL FETCH_BULK_COLLECTION_RECORDS_UDF(:MY_CURSOR, 1.0, NULL)
        );

        Return MY_CURSOR;
    END;
$$;

CALL MY_PROCEDURE();
```

Copy

Output:

```
{
  "FOUND": true,
  "ISOPEN": true,
  "NAME": "MY_CURSOR",
  "NOTFOUND": false,
  "QUERY": "   SELECT * FROM\n      MY_TABLE",
  "RESULT": [
    {
      "TEST": "TEST_A"
    }
  ],
  "ROWCOUNT": 1
}
```

Copy

## DATEDIFF\_UDF(DATE, INTEGER)[¶](#datediff-udf-date-integer "Link to this heading")

### Definition[¶](#id106 "Link to this heading")

This user-defined function (UDF) applies a subtraction of days over a date.

```
PUBLIC.DATEDIFF_UDF(FIRST_PARAM DATE, SECOND_PARAM INTEGER)
```

Copy

### Parameters[¶](#id107 "Link to this heading")

`FIRST_PARAM` DATE

The initial date to apply the subtraction.

`SECOND_PARAM` INTEGER

The number of days to be subtracted from the first date parameter.

### Returns[¶](#id108 "Link to this heading")

Returns the date after subtracting the indicated number of days.

### Usage example[¶](#id109 "Link to this heading")

Input:

```
SELECT PUBLIC.DATEDIFF_UDF(TO_DATE('2024-01-26'), 365);
```

Copy

Output:

```
2023-01-26
```

Copy

## DATE\_TO\_RR\_FORMAT\_UDF[¶](#date-to-rr-format-udf "Link to this heading")

### Definition[¶](#id110 "Link to this heading")

This user-defined function (UDF) transforms from date to oracle RR datetime format date

```
PUBLIC.DATE_TO_RR_FORMAT_UDF(INPUT_DATE DATE)
```

Copy

### Parameters[¶](#id111 "Link to this heading")

`INPUT_DATE` DATE

The date to transform.

### Returns[¶](#id112 "Link to this heading")

The input date with years adjusted to RR format.

### Migration example[¶](#id113 "Link to this heading")

Input:

```
Select TO_DATE('17-NOV-30','DD-MON-RR') as A from DUAL;
```

Copy

Output:

```
Select
PUBLIC.DATE_TO_RR_FORMAT_UDF( TO_DATE('17-NOV-30', 'DD-MON-YY')) as A from DUAL;
```

Copy

### Usage example[¶](#id114 "Link to this heading")

Input:

```
PUBLIC.CONVERT_DATE_WITH_RR_FORMAT_UDF(TO_DATE('17-NOV-30','DD-MON-YY')) as A from DUAL;
```

Copy

Output:

```
2030-11-17
```

Copy

## FETCH\_BULK\_RECORD\_COLLECTIONS\_UDF (OBJECT, INTEGER)[¶](#fetch-bulk-record-collections-udf-object-integer "Link to this heading")

### Definition[¶](#id115 "Link to this heading")

This user-defined function (UDF) is used to cover the functionality of `fetch bulk records` with different input parameters that determine the information added or the behavior of the cursor.

```
FETCH_BULK_RECORD_COLLECTIONS_UDF(CURSOR OBJECT, LIMIT INTEGER)
```

Copy

### Parameters[¶](#id116 "Link to this heading")

`CURSOR` OBJECT

The cursor that is being processed.

`LIMIT` INTEGER

The limit of the row count.

### Returns[¶](#id117 "Link to this heading")

Returns an object with the processed information.

### Usage example[¶](#id118 "Link to this heading")

Input:

```
CREATE OR REPLACE TABLE BULKCOLLECTTABLE(test VARCHAR(100));
INSERT INTO BULKCOLLECTTABLE VALUES ('TEST_A');

CREATE OR REPLACE PROCEDURE MY_PROCEDURE ()
RETURNS OBJECT
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
    DECLARE
        MY_CURSOR OBJECT := INIT_CURSOR_UDF('MY_CURSOR', '   SELECT * FROM
      BULKCOLLECTTABLE');

    BEGIN
        MY_CURSOR := (
            CALL OPEN_BULK_CURSOR_UDF(:MY_CURSOR)
        );
        MY_CURSOR := (
            CALL FETCH_BULK_RECORD_COLLECTIONS_UDF(:MY_CURSOR, 0)
        );

        Return MY_CURSOR;
    END;
$$;

CALL MY_PROCEDURE();
```

Copy

Output:

```
{
  "FOUND": false,
  "ISOPEN": true,
  "NAME": "MY_CURSOR",
  "NOTFOUND": true,
  "QUERY": "   SELECT * FROM\n      BULKCOLLECTTABLE",
  "RESULT": {
    "TEST": []
  },
  "ROWCOUNT": 0
}
```

Copy

## DBMS\_OUTPUT.PUT\_LINE\_UDF[¶](#dbms-output-put-line-udf "Link to this heading")

### Definition[¶](#id119 "Link to this heading")

This user-defined function (UDF) is used to replicate the functionality of the Oracle DBMS\_OUTPUT\_PUT\_LINE function.

```
DBMS_OUTPUT.PUT_LINE_UDF(LOG VARCHAR)
```

Copy

Warning

Notice that performance may be affected by using this UDF. To start logging information uncomment the implementation inside the function.

### Parameters[¶](#id120 "Link to this heading")

`LOG` VARCHAR

The information to be shown in the command line.

### Returns[¶](#id121 "Link to this heading")

Returns a `varchar` with the information logged.

### Usage example[¶](#id122 "Link to this heading")

Input:

```
SELECT DBMS_OUTPUT.PUT_LINE_UDF(to_varchar(123));
```

Copy

Output:

```
123
```

Copy

## DATEDIFF\_UDF(DATE, DATE)[¶](#datediff-udf-date-date "Link to this heading")

### Definition[¶](#id123 "Link to this heading")

This user-defined function (UDF) is used when there is a subtraction between two dates.

```
PUBLIC.DATEDIFF_UDF(FIRST_PARAM DATE, SECOND_PARAM DATE)
```

Copy

### Parameters[¶](#id124 "Link to this heading")

`FIRST_PARAM` DATE

The date that represents the minuend in the subtraction.

`SECOND_PARAM` DATE

The date that represents the subtrahen in the subtraction.

### Returns[¶](#id125 "Link to this heading")

Returns an integer with the number of days between the dates.

### Usage example[¶](#id126 "Link to this heading")

Input:

```
SELECT PUBLIC.DATEDIFF_UDF(TO_DATE('2024-01-26'), TO_DATE('2023-01-26'));
```

Copy

Output:

```
365
```

Copy

## OPEN\_BULK\_CURSOR\_UDF (OBJECT, ARRAY)[¶](#open-bulk-cursor-udf-object-array "Link to this heading")

### Definition[¶](#id127 "Link to this heading")

This user-defined function (UDF) is used to open a cursor with bindings.

```
OPEN_BULK_CURSOR_UDF(CURSOR OBJECT, BINDINGS ARRAY)
```

Copy

### Parameters[¶](#id128 "Link to this heading")

`CURSOR` OBJECT

The cursor to process as open.

`BINDINGS` ARRAY

The binding that is related to the cursor.

### Returns[¶](#id129 "Link to this heading")

Returns an object with the current information of the cursor.

### Usage example[¶](#id130 "Link to this heading")

Input:

```
CREATE OR REPLACE TABLE BULKCOLLECTTABLE(test VARCHAR(100));

CREATE OR REPLACE PROCEDURE MY_PROCEDURE ()
RETURNS OBJECT
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
    DECLARE
        MY_CURSOR OBJECT := INIT_CURSOR_UDF('MY_CURSOR', '   SELECT * FROM
      BULKCOLLECTTABLE');

    BEGIN
        MY_CURSOR := (
            CALL OPEN_BULK_CURSOR_UDF(:MY_CURSOR, NULL)
        );
        Return MY_CURSOR;
    END;
$$;

CALL MY_PROCEDURE();
```

Copy

Output:

```
{
  "ISOPEN": true,
  "NAME": "MY_CURSOR",
  "QUERY": "   SELECT * FROM\n      BULKCOLLECTTABLE",
  "ROWCOUNT": 0
}
```

Copy

## CLOSE\_BULK\_CURSOR\_UDF[¶](#close-bulk-cursor-udf "Link to this heading")

### Definition[¶](#id131 "Link to this heading")

This user-defined function (UDF) deletes the temporary table that stores the result set of the cursor and resets the cursor properties to their initial state.

```
CLOSE_BULK_CURSOR_UDF(CURSOR OBJECT)
```

Copy

### Parameters[¶](#id132 "Link to this heading")

`CURSOR` OBJECT

The cursor that is checked and closed.

### Returns[¶](#id133 "Link to this heading")

Returns an object with the cursor properties reset.

### Migration example[¶](#id134 "Link to this heading")

Input:

```
-- [procedure initial logic]
CLOSE C1;
-- [procedure ending logic]
```

Copy

Output:

```
C1 := (
            CALL CLOSE_BULK_CURSOR_UDF(:C1)
        );
```

Copy

### Usage example[¶](#id135 "Link to this heading")

Input:

```
CREATE OR REPLACE TABLE BULKCOLLECTTABLE(test VARCHAR(100));

CREATE OR REPLACE PROCEDURE MY_PROCEDURE ()
RETURNS OBJECT
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
    DECLARE
        MY_CURSOR OBJECT := INIT_CURSOR_UDF('MY_CURSOR', '   SELECT * FROM
      BULKCOLLECTTABLE');

    BEGIN
        MY_CURSOR := (
            CALL OPEN_BULK_CURSOR_UDF(:MY_CURSOR)
        );
        MY_CURSOR := (
            CALL CLOSE_BULK_CURSOR_UDF(:MY_CURSOR)
        );

        RETURN MY_CURSOR;
    END;
$$;
```

Copy

Output:

```
{
  "FOUND": null,
  "ISOPEN": false,
  "NAME": "MY_CURSOR",
  "NOTFOUND": null,
  "QUERY": "   SELECT * FROM\n      BULKCOLLECTTABLE",
  "ROWCOUNT": -1
}
```

Copy

## DATEADD\_UDF (FLOAT, DATE)[¶](#dateadd-udf-float-date "Link to this heading")

### Definition[¶](#id136 "Link to this heading")

This user-defined function (UDF) is used in cases when there is an addition between a type as `float` or `timestamp` and a `date`.

```
PUBLIC.DATEADD_UDF(FIRST_PARAM FLOAT, SECOND_PARAM DATE)
```

Copy

### Parameters[¶](#id137 "Link to this heading")

`FIRST_PARAM` FLOAT

The float number that is going to be added with the second date parameter.

`SECOND_PARAM` DATE

The date to be added with the number in the first parameter.

### Returns[¶](#id138 "Link to this heading")

Returns the addition between the float number and the date specified.

### Usage example[¶](#id139 "Link to this heading")

Input:

```
SELECT DATEADD_UDF(6, '2022-02-14');
```

Copy

Output:

```
2022-02-20
```

Copy

## BFILENAME\_UDF[¶](#bfilename-udf "Link to this heading")

### Definition[¶](#id140 "Link to this heading")

The function takes the directory name and the filename parameter as a `string`. Then, it returns a concatenation using the `'\'.`

Warning

The character `'\'` must be changed to match the Operating System file concatenation character.

```
PUBLIC.BFILENAME_UDF (DIRECTORYNAME STRING, FILENAME STRING);
```

Copy

### Parameters[¶](#id141 "Link to this heading")

`DIRECTORYNAME` STRING

The directory name to be processed as a `string`.

`FILENAME` STRING

The filename to be concatenated.

### Returns[¶](#id142 "Link to this heading")

Returns a `string` that contains the directory name and filename concatenated by a `'\'`.

### Migration example[¶](#id143 "Link to this heading")

Input:

```
SELECT BFILENAME ('directory', 'filename.jpg') FROM DUAL;
```

Copy

Output:

```
SELECT
PUBLIC.BFILENAME_UDF('directory', 'filename.jpg') FROM DUAL;
```

Copy

### Usage example[¶](#id144 "Link to this heading")

Input:

```
SELECT PUBLIC.BFILENAME_UDF('directory', 'filename.jpg');
```

Copy

Output:

```
directory\filename.jpg
```

Copy

## REGEXP\_LIKE\_UDF (STRING, STRING)[¶](#regexp-like-udf-string-string "Link to this heading")

### Definition[¶](#id145 "Link to this heading")

This user-defined function (UDF) is used to support the Oracle `REGEXP_LIKE` functionality.

```
REGEXP_LIKE_UDF(COL STRING, PATTERN STRING)
```

Copy

### Parameters[¶](#id146 "Link to this heading")

COL STRING

The string to be evaluated with the pattern.

PATTERN STRING

The pattern to be checked.

### Returns[¶](#id147 "Link to this heading")

Returns a boolean expression. True if the pattern matches the string; otherwise, false.

### Usage example[¶](#id148 "Link to this heading")

Input:

```
SELECT REGEXP_LIKE_UDF('San Francisco', 'San* [fF].*');
```

Copy

Output:

```
TRUE
```

Copy

## UTL\_FILE.FOPEN\_UDF (VARCHAR, VARCHAR, VARCHAR)[¶](#utl-file-fopen-udf-varchar-varchar-varchar "Link to this heading")

### Definition[¶](#id149 "Link to this heading")

This user-defined function (UDF) is used to replicate the functionality of the Oracle `UTL_FILE_FOPEN` procedure.

```
UTL_FILE.FOPEN_UDF(PACKAGE_VARIABLE VARCHAR, FILENAME VARCHAR, OPEN_MODE VARCHAR)
```

Copy

### Parameters[¶](#id150 "Link to this heading")

`PACKAGE_VARIABLE` VARCHAR

The variable related to the file opening.

`FILENAME` VARCHAR

The file to be opened.

`OPEN_MODE` VARCHAR

Indicates de mode on which the file will be available.

### Returns[¶](#id151 "Link to this heading")

Returns a varchar with the result.

### Usage example[¶](#id152 "Link to this heading")

Warning

The `UTL_FILE.FOPEN_UDF` allows to open a .csv file. To access the file it is required to create a `stage` for the file and use the Snowflakr CLI to upload it.

Input:

```
CREATE OR REPLACE PROCEDURE PROC()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
   DECLARE
    file_data  VARIANT;
   BEGIN

    CALL UTL_FILE.FOPEN_UDF(NULL, 'test2.csv','a');

    SELECT
      *
    INTO
      file_data
    FROM
      TABLE(RESULT_SCAN(LAST_QUERY_ID()));

    CALL UTL_FILE.PUT_LINE_UDF(:file_data,'New line');


    CALL UTL_FILE.FCLOSE_UDF(:file_data);


   END
$$;

CALL PROC();
```

Copy

Output:

```
null
```

Copy

## FETCH\_BULK\_COLLECTION\_RECORDS\_UDF (OBJECT)[¶](#fetch-bulk-collection-records-udf-object "Link to this heading")

### Definition[¶](#id153 "Link to this heading")

This user-defined function (UDF) is used to replicate the functionality of FETCH in Oracle. This is the variation where it receives the cursor only.

```
FETCH_BULK_COLLECTION_RECORDS_UDF(CURSOR OBJECT)
```

Copy

### Parameters[¶](#id154 "Link to this heading")

`CURSOR` OBJECT

The cursor that is processed and filled with the data in the `fetch bulk`.

### Returns[¶](#id155 "Link to this heading")

Returns an object with the records from the `fetch bulk`.

### Usage example[¶](#id156 "Link to this heading")

Input:

```
CREATE OR REPLACE TABLE MY_TABLE (test VARCHAR(100));
INSERT INTO MY_TABLE VALUES ('TEST_A');

CREATE OR REPLACE PROCEDURE MY_PROCEDURE ()
RETURNS OBJECT
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
    DECLARE
        MY_CURSOR OBJECT := INIT_CURSOR_UDF('MY_CURSOR', '   SELECT * FROM
      MY_TABLE');

    BEGIN
        MY_CURSOR := (
            CALL OPEN_BULK_CURSOR_UDF(:MY_CURSOR)
        );
        MY_CURSOR := (
            CALL FETCH_BULK_COLLECTION_RECORDS_UDF(:MY_CURSOR)
        );

        Return MY_CURSOR;
    END;
$$;

CALL MY_PROCEDURE();
```

Copy

Output:

```
{
  "FOUND": true,
  "ISOPEN": true,
  "NAME": "MY_CURSOR",
  "NOTFOUND": false,
  "QUERY": "   SELECT * FROM\n      MY_TABLE",
  "RESULT": [
    {
      "TEST": "TEST_A"
    }
  ],
  "ROWCOUNT": 1
}
```

Copy

## FETCH\_BULK\_RECORD\_COLLECTIONS\_UDF (OBJECT, FLOAT, ARRAY)[¶](#fetch-bulk-record-collections-udf-object-float-array "Link to this heading")

### Definition[¶](#id157 "Link to this heading")

This user-defined function (UDF) is used to cover the functionality of `fetch bulk records` with different input parameters that determine the information added or the behavior of the cursor.

```
FETCH_BULK_RECORD_COLLECTIONS_UDF(CURSOR OBJECT, LIMIT FLOAT, COLUMN_NAMES ARRAY)
```

Copy

### Parameters[¶](#id158 "Link to this heading")

`CURSOR` OBJECT

The cursor that is being processed.

`LIMIT` FLOAT

The limit of the row count.

`COLUMN_NAMES` ARRAY

The column names that are associated with the cursor.

### Returns[¶](#id159 "Link to this heading")

Returns an object with the processed information.

### Usage example[¶](#id160 "Link to this heading")

Input:

```
CREATE OR REPLACE TABLE BULKCOLLECTTABLE(test VARCHAR(100));
INSERT INTO BULKCOLLECTTABLE VALUES ('TEST_A');

CREATE OR REPLACE PROCEDURE MY_PROCEDURE ()
RETURNS OBJECT
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
    DECLARE
        MY_CURSOR OBJECT := INIT_CURSOR_UDF('MY_CURSOR', '   SELECT * FROM
      BULKCOLLECTTABLE');

    BEGIN
        MY_CURSOR := (
            CALL OPEN_BULK_CURSOR_UDF(:MY_CURSOR)
        );
        MY_CURSOR := (
            CALL FETCH_BULK_RECORD_COLLECTIONS_UDF(:MY_CURSOR, 1.0, NULL)
        );

        RETURN MY_CURSOR;
    END;
$$;

CALL MY_PROCEDURE();
```

Copy

Output:

```
{
  "FOUND": true,
  "ISOPEN": true,
  "NAME": "MY_CURSOR",
  "NOTFOUND": false,
  "QUERY": "   SELECT * FROM\n      BULKCOLLECTTABLE",
  "RESULT": {
    "TEST": [
      "TEST_A"
    ]
  },
  "ROWCOUNT": 1
}
```

Copy

## FETCH\_BULK\_COLLECTION\_RECORDS\_UDF (OBJECT, INTEGER)[¶](#fetch-bulk-collection-records-udf-object-integer "Link to this heading")

### Definition[¶](#id161 "Link to this heading")

This user-defined function (UDF) is used to replicate the functionality of FETCH in Oracle. This is the variation where it receives the cursor and the limit.

```
FETCH_BULK_COLLECTION_RECORDS_UDF(CURSOR OBJECT, LIMIT INTEGER)
```

Copy

### Parameters[¶](#id162 "Link to this heading")

`CURSOR` OBJECT

The cursor that is processed and filled with the data in the `fetch bulk`.

`LIMIT` FLOAT

The limit for the records to call.

### Returns[¶](#id163 "Link to this heading")

Returns an object with the records from the `fetch bulk`.

### Usage example[¶](#id164 "Link to this heading")

Input:

```
CREATE OR REPLACE TABLE MY_TABLE (test VARCHAR(100));
INSERT INTO MY_TABLE VALUES ('TEST_A');

CREATE OR REPLACE PROCEDURE MY_PROCEDURE ()
RETURNS OBJECT
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
    DECLARE
        MY_CURSOR OBJECT := INIT_CURSOR_UDF('MY_CURSOR', '   SELECT * FROM
      MY_TABLE');

    BEGIN
        MY_CURSOR := (
            CALL OPEN_BULK_CURSOR_UDF(:MY_CURSOR)
        );
        MY_CURSOR := (
            CALL FETCH_BULK_COLLECTION_RECORDS_UDF(:MY_CURSOR, 0)
        );

        Return MY_CURSOR;
    END;
$$;

CALL MY_PROCEDURE();
```

Copy

Output:

```
{
  "FOUND": false,
  "ISOPEN": true,
  "NAME": "MY_CURSOR",
  "NOTFOUND": true,
  "QUERY": "   SELECT * FROM\n      MY_TABLE",
  "RESULT": [],
  "ROWCOUNT": 0
}
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

1. [DATEDIFF\_UDF(TIMESTAMP, NUMBER)](#datediff-udf-timestamp-number)
2. [DATEDIFF\_UDF(TIMESTAMP, DATE)](#datediff-udf-timestamp-date)
3. [DATE\_TO\_JULIAN\_DAYS\_UDF](#date-to-julian-days-udf)
4. [UTL\_FILE.PUT\_LINE\_UDF](#utl-file-put-line-udf)
5. [UTL\_FILE.FOPEN\_UDF (VARCHAR,VARCHAR)](#utl-file-fopen-udf-varchar-varchar)
6. [JSON\_VALUE\_UDF](#json-value-udf)
7. [DATEADD\_UDF (FLOAT, TIMESTAMP)](#dateadd-udf-float-timestamp)
8. [FETCH\_BULK\_COLLECTIONS\_UDF (OBJECT)](#fetch-bulk-collections-udf-object)
9. [DATEADD\_UDF (DATE, FLOAT)](#dateadd-udf-date-float)
10. [DATEDIFF\_UDF(DATE, TIMESTAMP)](#datediff-udf-date-timestamp)
11. [DBMS\_RANDOM.VALUE\_UDF](#dbms-random-value-udf)
12. [DBMS\_RANDOM.VALUE\_UDF (DOUBLE, DOUBLE)](#dbms-random-value-udf-double-double)
13. [FETCH\_BULK\_RECORD\_COLLECTIONS\_UDF (OBJECT, ARRAY)](#fetch-bulk-record-collections-udf-object-array)
14. [FETCH\_BULK\_COLLECTION\_RECORDS\_UDF (OBJECT, ARRAY)](#fetch-bulk-collection-records-udf-object-array)
15. [JULIAN\_TO\_GREGORIAN\_DATE\_UDF](#julian-to-gregorian-date-udf)
16. [TIMESTAMP\_DIFF\_UDF](#timestamp-diff-udf)
17. [REGEXP\_LIKE\_UDF (STRING, STRING, STRING)](#regexp-like-udf-string-string-string)
18. [FETCH\_BULK\_COLLECTIONS\_UDF (OBJECT, FLOAT)](#fetch-bulk-collections-udf-object-float)
19. [INIT\_CURSOR\_UDF](#init-cursor-udf)
20. [UPDATE\_PACKAGE\_VARIABLE\_STATE\_UDF](#update-package-variable-state-udf)
21. [OPEN\_BULK\_CURSOR\_UDF (OBJECT)](#open-bulk-cursor-udf-object)
22. [DATEADD\_UDF (TIMESTAMP, FLOAT)](#dateadd-udf-timestamp-float)
23. [DATEDIFF\_UDF(TIMESTAMP, TIMESTAMP)](#datediff-udf-timestamp-timestamp)
24. [UTL\_FILE.FCLOSE\_UDF](#utl-file-fclose-udf)
25. [FETCH\_BULK\_RECORD\_COLLECTIONS\_UDF (OBJECT)](#fetch-bulk-record-collections-udf-object)
26. [CAST\_DATE\_UDF](#cast-date-udf)
27. [FETCH\_BULK\_COLLECTION\_RECORDS\_UDF (OBJECT, FLOAT, ARRAY)](#fetch-bulk-collection-records-udf-object-float-array)
28. [DATEDIFF\_UDF(DATE, INTEGER)](#datediff-udf-date-integer)
29. [DATE\_TO\_RR\_FORMAT\_UDF](#date-to-rr-format-udf)
30. [FETCH\_BULK\_RECORD\_COLLECTIONS\_UDF (OBJECT, INTEGER)](#fetch-bulk-record-collections-udf-object-integer)
31. [DBMS\_OUTPUT.PUT\_LINE\_UDF](#dbms-output-put-line-udf)
32. [DATEDIFF\_UDF(DATE, DATE)](#datediff-udf-date-date)
33. [OPEN\_BULK\_CURSOR\_UDF (OBJECT, ARRAY)](#open-bulk-cursor-udf-object-array)
34. [CLOSE\_BULK\_CURSOR\_UDF](#close-bulk-cursor-udf)
35. [DATEADD\_UDF (FLOAT, DATE)](#dateadd-udf-float-date)
36. [BFILENAME\_UDF](#bfilename-udf)
37. [REGEXP\_LIKE\_UDF (STRING, STRING)](#regexp-like-udf-string-string)
38. [UTL\_FILE.FOPEN\_UDF (VARCHAR, VARCHAR, VARCHAR)](#utl-file-fopen-udf-varchar-varchar-varchar)
39. [FETCH\_BULK\_COLLECTION\_RECORDS\_UDF (OBJECT)](#fetch-bulk-collection-records-udf-object)
40. [FETCH\_BULK\_RECORD\_COLLECTIONS\_UDF (OBJECT, FLOAT, ARRAY)](#fetch-bulk-record-collections-udf-object-float-array)
41. [FETCH\_BULK\_COLLECTION\_RECORDS\_UDF (OBJECT, INTEGER)](#fetch-bulk-collection-records-udf-object-integer)