---
auto_generated: true
description: This user-defined function (UDF) determines whether an expression is
  a valid numeric type.
last_scraped: '2026-01-14T16:57:36.459836+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/function-references/sql-server/README.html
title: SnowConvert AI - Function References for SQL-Server | Snowflake Documentation
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
              - [Oracle](../oracle/README.md)
              - [Shared](../shared/README.md)
              - [SQL Server](README.md)
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

[Guides](../../../../../../guides/README.md)[Migrations](../../../../../README.md)Tools[SnowConvert AI](../../../../overview.md)General[Technical Documentation](../../README.md)Function ReferencesSQL Server

# SnowConvert AI - Function References for SQL-Server[¶](#snowconvert-ai-function-references-for-sql-server "Link to this heading")

## ISNUMERIC\_UDF[¶](#isnumeric-udf "Link to this heading")

### Definition[¶](#definition "Link to this heading")

This user-defined function (UDF) determines whether an expression is a valid numeric type.

```
ISNUMERIC_UDF(EXPR VARCHAR)
```

Copy

### Parameters[¶](#parameters "Link to this heading")

`EXPR` VARCHAR

The expression to be evaluated.

### Returns[¶](#returns "Link to this heading")

Returns 1 when the input expression evaluates to a valid numeric data type; otherwise, it returns 0.

### Usage example[¶](#usage-example "Link to this heading")

Input:

```
SELECT ISNUMERIC_UDF('5');
```

Copy

Output:

```
1
```

Copy

## PATINDEX\_UDF[¶](#patindex-udf "Link to this heading")

### Definition[¶](#id1 "Link to this heading")

This user-defined function (UDF) returns the starting position of the first occurrence of a pattern in a specified expression or zeros if the pattern is not found.

```
PATINDEX_UDF(PATTERN VARCHAR, EXPRESSION VARCHAR)
```

Copy

### Parameters[¶](#id2 "Link to this heading")

`PATTERN` VARCHAR

The pattern to search for.

`EXPRESSION` VARCHAR

The expression that is being evaluated.

### Returns[¶](#id3 "Link to this heading")

Returns an integer with the starting position of the pattern.

### Usage example[¶](#id4 "Link to this heading")

Input:

```
SELECT PATINDEX_UDF('an', 'banana');
```

Copy

Output:

```
2
```

Copy

## ERROR\_SEVERITY\_UDF[¶](#error-severity-udf "Link to this heading")

### Definition[¶](#id5 "Link to this heading")

This user-defined function (UDF) gets a value indicating the severity of an error. The default value will always be 16.

```
ERROR_SEVERITY_UDF()
```

Copy

### Parameters[¶](#id6 "Link to this heading")

No input parameters.

### Returns[¶](#id7 "Link to this heading")

Returns a `string` with the value associated with the SQL variable name `ERROR_SEVERITY`.

### Usage example[¶](#id8 "Link to this heading")

Input:

```
SELECT ERROR_SEVERITY_UDF();
```

Copy

Output:

```
null -- No information set.
```

Copy

## TRANSFORM\_SP\_EXECUTE\_SQL\_STRING\_UDF(STRING, STRING, ARRAY, ARRAY)[¶](#transform-sp-execute-sql-string-udf-string-string-array-array "Link to this heading")

### Definition[¶](#id9 "Link to this heading")

This user-defined function (UDF) emulates the behavior of embedded parameters (Data Binding) in the SP\_EXECUTESQL system procedure by directly replacing their values in the SQL string.

Additionally, it removes the OUTPUT parameters from the string as this is done outside the EXECUTE IMMEDIATE to which the SP\_EXECUTESQL will be transformed.

For more information, check the SP\_EXECUTESQL translation specification.

```
TRANSFORM_SP_EXECUTE_SQL_STRING_UDF(
    _SQL_STRING STRING,
    _PARAMS_DEFINITION STRING,
    _PARAMS_NAMES ARRAY,
    _PARAMS_VALUES ARRAY
)
```

Copy

### Parameters[¶](#id10 "Link to this heading")

`_SQL_STRING` STRING

The string to be transformed.

`_PARAMS_DEFINITION` STRING

The original parameters definition checks the order in which parameter values must be assigned.

`_PARAMS_NAMES` ARRAY

The array of parameter names to replace the values in the SQL string.

`_PARAMS_VALUES` ARRAY

The array of the parameter values to be replaced in the SQL string.

### Returns[¶](#id11 "Link to this heading")

Returns a STRING with the embedded parameters values replaced.

### Usage example[¶](#id12 "Link to this heading")

Input:

```
SELECT TRANSFORM_SP_EXECUTE_SQL_STRING_UDF(
    'SELECT * FROM PERSONS WHERE NAME LIKE (@NAME) AND ID < @id AND AGE < @age;', '@age INT, @id INT, @name VARCHAR(25)',
    ARRAY_CONSTRUCT('', '', ''),
    ARRAY_CONSTRUCT(30, 100, 'John Smith'));
```

Copy

Output:

```
SELECT * FROM PERSONS WHERE NAME LIKE ('John Smith') AND ID < 100 AND AGE < 30;
```

Copy

## TABLE\_OBJECT\_ID\_UDF (VARCHAR)[¶](#table-object-id-udf-varchar "Link to this heading")

### Definition[¶](#id13 "Link to this heading")

This user-defined function (UDF) checks if a table with a specific name has been created before.

```
TABLE_OBJECT_ID_UDF(NAME VARCHAR)
```

Copy

### Parameters[¶](#id14 "Link to this heading")

`NAME` VARCHAR

The table name to be evaluated.

### Returns[¶](#id15 "Link to this heading")

Returns a boolean expression depending on the existence of the table.

### Usage example[¶](#id16 "Link to this heading")

Input:

```
SELECT TABLE_OBJECT_ID_UDF('Test');
```

Copy

Output:

```
FALSE
```

Copy

## ERROR\_PROCEDURE\_UDF[¶](#error-procedure-udf "Link to this heading")

### Definition[¶](#id17 "Link to this heading")

This user-defined function (UDF) returns the value associated with the SQL variable name `ERROR_PROCEDURE`.

```
ERROR_PROCEDURE_UDF()
```

Copy

### Parameters[¶](#id18 "Link to this heading")

No input parameters.

### Returns[¶](#id19 "Link to this heading")

Returns a `string` with the value associated with the SQL variable name `ERROR_PROCEDURE`.

### Usage example[¶](#id20 "Link to this heading")

Input:

```
SELECT ERROR_PROCEDURE_UDF();
```

Copy

Output:

```
null -- No information set.
```

Copy

## DB\_ID\_UDF(STRING)[¶](#db-id-udf-string "Link to this heading")

### Definition[¶](#id21 "Link to this heading")

This user-defined function (UDF) emulates the [DB\_ID](https://learn.microsoft.com/en-us/sql/t-sql/functions/db-id-transact-sql?view=sql-server-ver16) functionality.

```
DB_ID_UDF(p_database_name STRING)
```

Copy

### Parameters[¶](#id22 "Link to this heading")

`p_database_name` STRING

The name of the database to obtain the id.

### Returns[¶](#id23 "Link to this heading")

Returns an id which correspond to the number assigned to the database when it is created. This number is assigned consecutively.

### Usage example[¶](#id24 "Link to this heading")

Input:

```
SELECT DB_ID_UDF('MY_DATABASE')
```

Copy

Output:

```
6
```

Copy

Warning

If the database does not exist, it returns null.

## ERROR\_LINE\_UDF[¶](#error-line-udf "Link to this heading")

### Definition[¶](#id25 "Link to this heading")

This user-defined function (UDF) returns the value associated with the SQL variable name `ERROR_LINE`.

```
ERROR_LINE_UDF()
```

Copy

### Parameters[¶](#id26 "Link to this heading")

No input parameters.

### Returns[¶](#id27 "Link to this heading")

Returns a `string` with the value associated with the SQL variable name `ERROR_LINE`.

### Usage example[¶](#id28 "Link to this heading")

Input:

```
SELECT ERROR_LINE_UDF();
```

Copy

Output:

```
null -- No information set.
```

Copy

## FUNCTION\_OBJECT\_ID\_UDF (VARCHAR)[¶](#function-object-id-udf-varchar "Link to this heading")

### Definition[¶](#id29 "Link to this heading")

This user-defined function (UDF) checks if a function with a specific name has been created before.

```
VIEW_OBJECT_ID_UDF(NAME VARCHAR)
```

Copy

### Parameters[¶](#id30 "Link to this heading")

`NAME` VARCHAR

The function name to be evaluated.

### Returns[¶](#id31 "Link to this heading")

Returns a boolean expression depending on the existence of the function.

### Usage example[¶](#id32 "Link to this heading")

Input:

```
SELECT FUNCTION_OBJECT_ID_UDF('Test');
```

Copy

Output:

```
FALSE
```

Copy

## CONSTRAINT\_OBJECT\_ID\_UDF (VARCHAR)[¶](#constraint-object-id-udf-varchar "Link to this heading")

### Definition[¶](#id33 "Link to this heading")

This user-defined function (UDF) checks if a constraint with a specific name has been created before.

```
CONSTRAINT_OBJECT_ID_UDF(NAME VARCHAR)
```

Copy

### Parameters[¶](#id34 "Link to this heading")

`NAME` VARCHAR

The constraint name to be evaluated.

### Returns[¶](#id35 "Link to this heading")

Returns a boolean expression depending on the existence of the constraint.

### Usage example[¶](#id36 "Link to this heading")

Input:

```
SELECT CONSTRAINT_OBJECT_ID_UDF('Test');
```

Copy

Output:

```
FALSE
```

Copy

## FOR\_XML\_UDF (OBJECT, VARCHAR, VARCHAR)[¶](#for-xml-udf-object-varchar-varchar "Link to this heading")

### Definition[¶](#id37 "Link to this heading")

This user-defined function (UDF) converts an object to XML.

```
FOR_XML_UDF(OBJ OBJECT, ELEMENT_NAME VARCHAR, ROOT_NAME VARCHAR)
```

Copy

### Parameters[¶](#id38 "Link to this heading")

`OBJ` OBJECT

Object to be converted.

`ELEMENT_NAME` VARCHAR

Element name to be given the object.

`ROOT_NAME` VARCHAR

The root name for XML.

### Returns[¶](#id39 "Link to this heading")

Returns a varchar in the format of XML.

### Usage example[¶](#id40 "Link to this heading")

Input:

```
SELECT
FOR_XML_UDF(OBJECT_CONSTRUCT('id', 1, 'name', 'David'), 'employee', 'employees');
```

Copy

Output:

```
<employees>
    <employee type="OBJECT">
        <id type="INTEGER">1</id>
        <name type="VARCHAR">David</name>
    </employee>
<employees>
```

Copy

## OBJECT\_ID\_UDF (VARCHAR)[¶](#object-id-udf-varchar "Link to this heading")

### Definition[¶](#id41 "Link to this heading")

This user-defined function (UDF) checks if an object with a specific name has been created before.

```
OBJECT_ID_UDF(NAME VARCHAR)
```

Copy

### Parameters[¶](#id42 "Link to this heading")

`NAME` VARCHAR

The object name to be evaluated.

### Returns[¶](#id43 "Link to this heading")

Returns a boolean expression depending on the existence of the object.

### Usage example[¶](#id44 "Link to this heading")

Input:

```
SELECT OBJECT_ID_UDF('Test');
```

Copy

Output:

```
FALSE
```

Copy

## PROCEDURE\_OBJECT\_ID\_UDF (VARCHAR)[¶](#procedure-object-id-udf-varchar "Link to this heading")

### Definition[¶](#id45 "Link to this heading")

This user-defined function (UDF) checks if a procedure with a specific name has been created before.

```
PROCEDURE_OBJECT_ID_UDF(NAME VARCHAR)
```

Copy

### Parameters[¶](#id46 "Link to this heading")

`NAME` VARCHAR

The procedure name to be evaluated.

### Returns[¶](#id47 "Link to this heading")

Returns a boolean expression depending on the existence of the procedure.

### Usage example[¶](#id48 "Link to this heading")

Input:

```
SELECT PROCEDURE_OBJECT_ID_UDF('Test');
```

Copy

Output:

```
FALSE
```

Copy

## ISDATE\_UDF[¶](#isdate-udf "Link to this heading")

### Definition[¶](#id49 "Link to this heading")

This user-defined function (UDF) determines whether the input value is a valid date.

```
ISDATE_UDF(DATE_VALUE STRING)
```

Copy

### Parameters[¶](#id50 "Link to this heading")

`DATE_VALUE` STRING

The date that is going to be evaluated.

### Returns[¶](#id51 "Link to this heading")

Returns 1 when the input expression evaluates to a valid date data type; otherwise, it returns 0.

### Usage example[¶](#id52 "Link to this heading")

Input:

```
SELECT ISDATE_UDF('2024-01-26');
```

Copy

Output:

```
1
```

Copy

## ERROR\_NUMBER\_UDF[¶](#error-number-udf "Link to this heading")

### Definition[¶](#id53 "Link to this heading")

This user-defined function (UDF) returns the value associated with the SQL variable name `ERROR_NUMBER`.

```
ERROR_NUMBER_UDF()
```

Copy

### Parameters[¶](#id54 "Link to this heading")

No input parameters.

### Returns[¶](#id55 "Link to this heading")

Returns a `string` with the value associated with the SQL variable name `ERROR_NUMBER`.

### Usage example[¶](#id56 "Link to this heading")

Input:

```
SELECT ERROR_NUMBER_UDF();
```

Copy

Output:

```
null -- No information set.
```

Copy

## OFFSET\_FORMATTER (VARCHAR)[¶](#offset-formatter-varchar "Link to this heading")

### Definition[¶](#id57 "Link to this heading")

This user-defined function (UDF) is an **auxiliary function** to format the offset hour and its prefix operator.

```
OFFSET_FORMATTER(offset_hrs VARCHAR)
```

Copy

### Parameters[¶](#id58 "Link to this heading")

`offset_hrs` VARCHAR

The value to be formatted.

### Returns[¶](#id59 "Link to this heading")

Returns a varchar value with the formatted output for the offset.

### Usage example[¶](#id60 "Link to this heading")

Input:

```
 SELECT OFFSET_FORMATTER('2024-01-26 22:00:50.708 -0800');
```

Copy

Output:

```
2024-01-26 22:00:50.708 -0800
```

Copy

## OPENXML\_UDF[¶](#openxml-udf "Link to this heading")

### Definition[¶](#id61 "Link to this heading")

This user-defined function (UDF) generates a query from an XML reading.

```
OPENXML_UDF(XML VARCHAR, PATH VARCHAR)
```

Copy

### Parameters[¶](#id62 "Link to this heading")

`XML` VARCHAR

The XML content as a `varchar`.

`PATH` VARCHAR

The path of the node to extract.

### Returns[¶](#id63 "Link to this heading")

Returns a table with the data generated by the XML reading.

### Usage example[¶](#id64 "Link to this heading")

Input:

```
SELECT * FROM TABLE(OPENXML_UDF('<iceCreamOrders>
    <order>
        <customer customerID="CUST001" contactName="Test ABC">
            <iceCreamOrder orderID="ORD001" employeeID="101" orderDate="2023-05-15T14:30:00">
                <iceCreamDetail productID="001" quantity="2"/>
                <iceCreamDetail productID="003" quantity="1"/>
            </iceCreamOrder>
        </customer>
    </order>
    <order>
        <customer customerID="CUST002" contactName="Test XYZ">
            <iceCreamOrder orderID="ORD002" employeeID="102" orderDate="2023-06-20T12:45:00">
                <iceCreamDetail productID="005" quantity="3"/>
                <iceCreamDetail productID="007" quantity="2"/>
            </iceCreamOrder>
        </customer>
    </order>
</iceCreamOrders>
', 'iceCreamOrders:order'));
```

Copy

Output:

|  | Value |
| --- | --- |
| 1 | { "order": { "$name": "order", "customer": [ { "customer": { "$name": "customer", "@contactName": "Test ABC", "@customerID": "CUST001", "iceCreamOrder": [ { "iceCreamOrder": { "$name": "iceCreamOrder", "@employeeID": 101, "@orderDate": "2023-05-15T14:30:00", "@orderID": "ORD001", "iceCreamDetail": [ { "iceCreamDetail": { "$name": "iceCreamDetail", "@productID": "001", "@quantity": 2 } }, { "iceCreamDetail": { "$name": "iceCreamDetail", "@productID": "003", "@quantity": 1 } } ] } } ] } } ] } } |
| 2 | { "order": { "$name": "order", "customer": [ { "customer": { "$name": "customer", "@contactName": "Test XYZ", "@customerID": "CUST002", "iceCreamOrder": [ { "iceCreamOrder": { "$name": "iceCreamOrder", "@employeeID": 102, "@orderDate": "2023-06-20T12:45:00", "@orderID": "ORD002", "iceCreamDetail": [ { "iceCreamDetail": { "$name": "iceCreamDetail", "@productID": "005", "@quantity": 3 } }, { "iceCreamDetail": { "$name": "iceCreamDetail", "@productID": "007", "@quantity": 2 } } ] } } ] } } ] } } |

## QUOTENAME\_UDF (VARCHAR, VARCHAR)[¶](#quotename-udf-varchar-varchar "Link to this heading")

### Definition[¶](#id65 "Link to this heading")

This user-defined function (UDF) creates a valid SQL Server delimited identifier by returning a Unicode string with the delimiters added.

```
QUOTENAME_UDF(STR VARCHAR, QUOTECHAR VARCHAR)
```

Copy

### Parameters[¶](#id66 "Link to this heading")

`STR` VARCHAR

The string to be transformed.

`QUOTECHAR` VARCHAR

The delimiter to add to the first parameter.

### Returns[¶](#id67 "Link to this heading")

Returns a varchar with the second parameter identifier added as delimiter.

### Usage example[¶](#id68 "Link to this heading")

Input:

```
SELECT QUOTENAME_UDF('test', '?');
```

Copy

Output:

```
?test?
```

Copy

## UPDATE\_ERROR\_VARS\_UDF (STRING, STRING, STRING)[¶](#update-error-vars-udf-string-string-string "Link to this heading")

### Definition[¶](#id69 "Link to this heading")

This user-defined function (UDF) updates the error variables in an environment in order to know when the procedure throws an error.

```
UPDATE_ERROR_VARS_UDF(MESSAGE STRING, SEVERITY STRING, STATE STRING)
```

Copy

### Parameters[¶](#id70 "Link to this heading")

`STATE` STRING

The state of the error message.

`MESSAGE` STRING

The message to be shown in the error.

`SEVERITY` STRING

The severity of the error.

### Returns[¶](#id71 "Link to this heading")

Returns a `string` value with the new error message information.

### Usage example[¶](#id72 "Link to this heading")

Input:

```
  SELECT UPDATE_ERROR_VARS_UDF('Message', '1', '1');
```

Copy

Output:

```
1ABC1
```

Copy

## ROUND\_MILLISECONDS\_UDF (TIMESTAMP\_TZ)[¶](#round-milliseconds-udf-timestamp-tz "Link to this heading")

### Definition[¶](#id73 "Link to this heading")

This user-defined function (UDF) is a function that rounds milliseconds to increments of 0, 3, or 7 milliseconds. Transact automatically rounds the milliseconds of datetime values.

```
ROUND_MILLISECONDS_UDF(INPUT TIMESTAMP_TZ)
```

Copy

### Parameters[¶](#id74 "Link to this heading")

`INPUT` TIMESTAMP\_TZ

The input time to be rounded.

### Returns[¶](#id75 "Link to this heading")

Returns the same input `TIMESTAMP_TZ` value but with the milliseconds rounded.

### Usage example[¶](#id76 "Link to this heading")

Input:

```
SELECT PUBLIC.ROUND_MILLISECONDS_UDF('1900-01-01 00:00:00.995 +0100')
```

Copy

Output:

```
'1900-01-01 00:00:00.997 +0100'
```

Copy

## CAST\_NUMERIC\_TO\_TIMESTAMP\_TZ\_UDF (NUMBER)[¶](#cast-numeric-to-timestamp-tz-udf-number "Link to this heading")

### Definition[¶](#id77 "Link to this heading")

This user-defined function (UDF) is used to cast a numeric value to `timestamp_tz`.

```
CAST_NUMERIC_TO_TIMESTAMP_TZ_UDF(INPUT NUMBER)
```

Copy

### Parameters[¶](#id78 "Link to this heading")

`INPUT` NUMBER

The number to be cast.

### Returns[¶](#id79 "Link to this heading")

Returns a `timestamp_tz` with the current timezone.

### Usage example[¶](#id80 "Link to this heading")

Input:

```
SELECT PUBLIC.CAST_NUMERIC_TO_TIMESTAMP_TZ_UDF(0)
```

Copy

Output:

```
1900-01-01 01:00:00.000 +0100
```

Copy

## IDENTITY\_UDF[¶](#identity-udf "Link to this heading")

### Definition[¶](#id81 "Link to this heading")

This user-defined function (UDF) determines whether an expression is a valid numeric type.

```
IDENTITY_UDF()
```

Copy

### Parameters[¶](#id82 "Link to this heading")

No input parameters.

### Returns[¶](#id83 "Link to this heading")

Returns an integer expression.

### Usage example[¶](#id84 "Link to this heading")

Warning

A sequence is generated to support the logic.

Input:

```
IDENTITY_UDF()
```

Copy

Output:

```
1
```

Copy

## FOR\_XML\_UDF (OBJECT, VARCHAR)[¶](#for-xml-udf-object-varchar "Link to this heading")

### Definition[¶](#id85 "Link to this heading")

This user-defined function (UDF) converts an object to XML.

```
FOR_XML_UDF(OBJ OBJECT, ELEMENT_NAME VARCHAR)
```

Copy

### Parameters[¶](#id86 "Link to this heading")

`OBJ` OBJECT

Object to be converted.

`ELEMENT_NAME` VARCHAR

Element name to be given the object.

### Returns[¶](#id87 "Link to this heading")

Returns a varchar in the format of XML.

### Usage example[¶](#id88 "Link to this heading")

Input:

```
SELECT
FOR_XML_UDF(OBJECT_CONSTRUCT('id', 1, 'name', 'David'), 'employee');
```

Copy

Output:

```
<employee type="OBJECT">
    <id type="INTEGER">1</id>
    <name type="VARCHAR">David</name>
</employee>
```

Copy

## QUOTENAME\_UDF (VARCHAR)[¶](#quotename-udf-varchar "Link to this heading")

### Definition[¶](#id89 "Link to this heading")

This user-defined function (UDF) creates a valid SQL Server delimited identifier by returning a Unicode string with the delimiters added.

```
QUOTENAME_UDF(STR VARCHAR)
```

Copy

### Parameters[¶](#id90 "Link to this heading")

`STR` VARCHAR

The string to be transformed.

### Returns[¶](#id91 "Link to this heading")

Returns a varchar with the delimited identifier added.

### Usage example[¶](#id92 "Link to this heading")

Input:

```
SELECT QUOTENAME_UDF('test');
```

Copy

Output:

```
"test"
```

Copy

## VIEW\_OBJECT\_ID\_UDF (VARCHAR)[¶](#view-object-id-udf-varchar "Link to this heading")

### Definition[¶](#id93 "Link to this heading")

This user-defined function (UDF) checks if a view with a specific name has been created before.

```
VIEW_OBJECT_ID_UDF(NAME VARCHAR)
```

Copy

### Parameters[¶](#id94 "Link to this heading")

`NAME` VARCHAR

The view name to be evaluated.

### Returns[¶](#id95 "Link to this heading")

Returns a boolean expression depending on the existence of the view.

### Usage example[¶](#id96 "Link to this heading")

Input:

```
SELECT VIEW_OBJECT_ID_UDF('Test');
```

Copy

Output:

```
FALSE
```

Copy

## SUBTRACT\_TIMESTAMP\_TZ\_UDF (TIMESTAMP\_TZ, TIMESTAMP\_TZ)[¶](#subtract-timestamp-tz-udf-timestamp-tz-timestamp-tz "Link to this heading")

### Definition[¶](#id97 "Link to this heading")

This user-defined function (UDF) converts both inputs to the system session timezone and subtracts the dates (`FIRST_DATE` - `SECOND_DATE`) taking 1900-01-01 00:00:00.000 as the zero value. If any value does not include the timezone, the current session timezone is used.

```
PUBLIC.SUBTRACT_TIMESTAMP_TZ_UDF(FIRST_DATE TIMESTAMP_TZ, SECOND_DATE TIMESTAMP_TZ)
```

Copy

### Parameters[¶](#id98 "Link to this heading")

`FIRST_DATE` TIMESTAMP\_TZ

The first date to be subtracted from.

`SECOND_DATE` TIMESTAMP\_TZ

The second date to be subtracted to.

### Returns[¶](#id99 "Link to this heading")

Returns the difference between the two input dates.

### Usage example[¶](#id100 "Link to this heading")

Input:

```
SELECT SUBTRACT_TIMESTAMP_TZ_UDF('1900-01-01 00:00:00.000 +0100', '1900-01-01 00:00:00.003 -0100')
```

Copy

Output:

```
1899-12-31 13:59:59.997 -0800
```

Copy

## STR\_UDF (FLOAT, VARCHAR)[¶](#str-udf-float-varchar "Link to this heading")

### Definition[¶](#id101 "Link to this heading")

This user-defined function (UDF) is a template for translating the functionality of SQL Server STR() to Snowflake when it’s used with one or two optional parameters

```
STR_UDF(FLOAT_EXPR FLOAT, FORMAT VARCHAR)
```

Copy

### Parameters[¶](#id102 "Link to this heading")

`FLOAT_EXPR` FLOAT

The expression to be processed.

`FORMAT` VARCHAR

The format to apply.

### Returns[¶](#id103 "Link to this heading")

Returns a varchar with the formatted expression.

### Usage example[¶](#id104 "Link to this heading")

Input:

```
SELECT STR_UDF(1.5, '99');
```

Copy

Output:

```
2
```

Copy

## XML\_JSON\_SIMPLE[¶](#xml-json-simple "Link to this heading")

### Definition[¶](#id105 "Link to this heading")

This user-defined function (UDF) generates an object with the information from executing a reading from an XML value.

```
XML_JSON_SIMPLE(XML VARIANT)
```

Copy

### Parameters[¶](#id106 "Link to this heading")

`XML` VARIANT

The XML to be read.

### Returns[¶](#id107 "Link to this heading")

Returns an object with the processed information from the XML.

### Usage example[¶](#id108 "Link to this heading")

Input:

```
SELECT XML_JSON_SIMPLE(TO_VARIANT(PARSE_XML('<iceCreamOrders>
    <order>
        <customer customerID="CUST001" contactName="Test ABC">
            <iceCreamOrder orderID="ORD001" employeeID="101" orderDate="2023-05-15T14:30:00">
                <iceCreamDetail productID="001" quantity="2"/>
                <iceCreamDetail productID="003" quantity="1"/>
            </iceCreamOrder>
        </customer>
    </order>
    <order>
        <customer customerID="CUST002" contactName="Test XYZ">
            <iceCreamOrder orderID="ORD002" employeeID="102" orderDate="2023-06-20T12:45:00">
                <iceCreamDetail productID="005" quantity="3"/>
                <iceCreamDetail productID="007" quantity="2"/>
            </iceCreamOrder>
        </customer>
    </order>
</iceCreamOrders>
')));
```

Copy

Output:

```
{
  "iceCreamOrders": {
    "$name": "iceCreamOrders",
    "order": [
      {
        "order": {
          "$name": "order",
          "customer": [
            {
              "customer": {
                "$name": "customer",
                "@contactName": "Test ABC",
                "@customerID": "CUST001",
                "iceCreamOrder": [
                  {
                    "iceCreamOrder": {
                      "$name": "iceCreamOrder",
                      "@employeeID": 101,
                      "@orderDate": "2023-05-15T14:30:00",
                      "@orderID": "ORD001",
                      "iceCreamDetail": [
                        {
                          "iceCreamDetail": {
                            "$name": "iceCreamDetail",
                            "@productID": "001",
                            "@quantity": 2
                          }
                        },
                        {
                          "iceCreamDetail": {
                            "$name": "iceCreamDetail",
                            "@productID": "003",
                            "@quantity": 1
                          }
                        }
                      ]
                    }
                  }
                ]
              }
            }
          ]
        }
      },
      {
        "order": {
          "$name": "order",
          "customer": [
            {
              "customer": {
                "$name": "customer",
                "@contactName": "Test XYZ",
                "@customerID": "CUST002",
                "iceCreamOrder": [
                  {
                    "iceCreamOrder": {
                      "$name": "iceCreamOrder",
                      "@employeeID": 102,
                      "@orderDate": "2023-06-20T12:45:00",
                      "@orderID": "ORD002",
                      "iceCreamDetail": [
                        {
                          "iceCreamDetail": {
                            "$name": "iceCreamDetail",
                            "@productID": "005",
                            "@quantity": 3
                          }
                        },
                        {
                          "iceCreamDetail": {
                            "$name": "iceCreamDetail",
                            "@productID": "007",
                            "@quantity": 2
                          }
                        }
                      ]
                    }
                  }
                ]
              }
            }
          ]
        }
      }
    ]
  }
}
```

Copy

## FORMATMESSAGE\_UDF[¶](#formatmessage-udf "Link to this heading")

### Definition[¶](#id109 "Link to this heading")

This user-defined function (UDF) provides the functionality of the SQL Server FORMATMESSAGE function. It constructs a message from an existing message from a provided string.

```
FORMATMESSAGE_UDF(MESSAGE STRING, ARGS ARRAY)
```

Copy

### Parameters[¶](#id110 "Link to this heading")

`MESSAGE` STRING

The existing message string.

`ARGS` ARRAY

The arguments to be added on the first message string.

### Returns[¶](#id111 "Link to this heading")

Returns a string with the corresponding concatenated message related to the argument’s positions.

### Usage example[¶](#id112 "Link to this heading")

Input:

```
SELECT FORMATMESSAGE_UDF('Test %s!', TO_ARRAY('a'));
```

Copy

Output:

```
Test a!
```

Copy

## IS\_MEMBER\_UDF[¶](#is-member-udf "Link to this heading")

### Definition[¶](#id113 "Link to this heading")

This user-defined function (UDF) determines the windows group membership by examining an access token.

```
IS_MEMBER_UDF(ROLE STRING)
```

Copy

### Parameters[¶](#id114 "Link to this heading")

`ROLE` STRING

The role name to be checked.

### Returns[¶](#id115 "Link to this heading")

Returns a boolean expression on true when the current user is a member of the role; otherwise returns false.

### Usage example[¶](#id116 "Link to this heading")

Input:

```
SELECT IS_MEMBER_UDF('TEST');
```

Copy

Output:

```
FALSE
```

Copy

## RAISERROR\_UDF (DOUBLE, DOUBLE, DOUBLE, ARRAY)[¶](#raiserror-udf-double-double-double-array "Link to this heading")

### Definition[¶](#id117 "Link to this heading")

This user-defined function (UDF) throws an exception with a specific message.

```
RAISERROR_UDF(MSG_ID DOUBLE, SEVERITY DOUBLE, STATE DOUBLE, PARAMS ARRAY)
```

Copy

### Parameters[¶](#id118 "Link to this heading")

`MSG_ID` DOUBLE

The message ID of the error message.

`SEVERITY` DOUBLE

The severity number for the error.

`STATE` DOUBLE

The state number for the error message.

`PARAMS` ARRAY

The additional information of the error message.

### Returns[¶](#id119 "Link to this heading")

Returns a varchar with an error message.

### Usage example[¶](#id120 "Link to this heading")

Input:

```
SELECT RAISERROR_UDF(2.1, 1.6, 1.0, array_construct('More information'));
```

Copy

Output:

```
MESSAGE: 2.1, LEVEL: 1.6, STATE: 1
```

Copy

## STR\_UDF(FLOAT)[¶](#str-udf-float "Link to this heading")

### Definition[¶](#id121 "Link to this heading")

This user-defined function (UDF) is a template for translating the functionality of SQL Server STR() to Snowflake when it’s used with one or two optional parameters

```
STR_UDF(FLOAT_EXPR FLOAT, FORMAT VARCHAR)
```

Copy

### Parameters[¶](#id122 "Link to this heading")

`FLOAT_EXPR` FLOAT

The expression to be processed.

### Returns[¶](#id123 "Link to this heading")

Returns a varchar with the formatted expression.

### Usage example[¶](#id124 "Link to this heading")

Input:

```
SELECT STR_UDF(1.5);
```

Copy

Output:

```
2
```

Copy

## SWITCHOFFSET\_UDF (TIMESTAMP\_TZ, VARCHAR)[¶](#switchoffset-udf-timestamp-tz-varchar "Link to this heading")

### Definition[¶](#id125 "Link to this heading")

This user-defined function (UDF) returns a new timestamp\_tz with the adjusted time taken for parameter target\_tz.

```
SWITCHOFFSET_UDF(source_timestamp TIMESTAMP_TZ, target_tz varchar)
```

Copy

### Parameters[¶](#id126 "Link to this heading")

`source_timestamp` TIMESTAMP\_TZ

The source timestamp to adjust.

`target_tz` varchar

The target time to take.

### Returns[¶](#id127 "Link to this heading")

Returns the formatted target time as TIMESTAMP\_TZ.

### Usage example[¶](#id128 "Link to this heading")

Input:

```
SELECT SWITCHOFFSET_UDF(time_in_paris, '-0600') as time_in_costa_rica;
```

Copy

Output:

| time\_in\_paris | time\_in\_costa\_rica |
| --- | --- |
| 2022-10-05 22:00:24.467 +02:00 | 2022-10-05 14:00:24.467 -06:00 |

## GET\_CURRENT\_TIMEZONE\_UDF[¶](#get-current-timezone-udf "Link to this heading")

### Definition[¶](#id129 "Link to this heading")

This user-defined function (UDF) gets the current session or system timezone as a literal.

```
GET_CURRENT_TIMEZONE_UDF()
```

Copy

### Parameters[¶](#id130 "Link to this heading")

No parameters.

### Returns[¶](#id131 "Link to this heading")

Returns a literal value with the current session or system timezone as a literal.

### Usage example[¶](#id132 "Link to this heading")

Input:

```
SELECT PUBLIC.GET_CURRENT_TIMEZONE_UDF();
```

Copy

Output:

```
'Europe/London'
```

Copy

## UPDATE\_ERROR\_VARS\_UDF (STRING, STRING, STRING, STRING, STRING, STRING)[¶](#update-error-vars-udf-string-string-string-string-string-string "Link to this heading")

### Definition[¶](#id133 "Link to this heading")

This user-defined function (UDF) updates the error variables in an environment in order to know when the procedure throws an error.

```
UPDATE_ERROR_VARS_UDF(LINE STRING,CODE STRING, STATE STRING, MESSAGE STRING, PROC_NAME STRING, SEVERITY STRING)
```

Copy

### Parameters[¶](#id134 "Link to this heading")

`LINE` STRING

The line related to the error.

`CODE` STRING

The error code associated with the error message.

`STATE` STRING

The state of the error message.

`MESSAGE` STRING

The message to be shown in the error.

`PROC_NAME` STRING

The procedure name.

`SEVERITY` STRING

The severity of the error.

### Returns[¶](#id135 "Link to this heading")

Returns a `string` value with the new error message information.

### Usage example[¶](#id136 "Link to this heading")

Input:

```
  SELECT UPDATE_ERROR_VARS_UDF('1', '1', '1', 'ABC', 'TEST', '1');
```

Copy

Output:

```
111ABCTEST1
```

Copy

## SEQUENCE\_OBJECT\_ID\_UDF (VARCHAR)[¶](#sequence-object-id-udf-varchar "Link to this heading")

### Definition[¶](#id137 "Link to this heading")

This user-defined function (UDF) checks if a sequence with a specific name has been created before.

```
SEQUENCE_OBJECT_ID_UDF(NAME VARCHAR)
```

Copy

### Parameters[¶](#id138 "Link to this heading")

`NAME` VARCHAR

The sequence name to be evaluated.

### Returns[¶](#id139 "Link to this heading")

Returns a boolean expression depending on the existence of the sequence.

### Usage example[¶](#id140 "Link to this heading")

Input:

```
SELECT SEQUENCE_OBJECT_ID_UDF('Test');
```

Copy

Output:

```
FALSE
```

Copy

## CAST\_TIMESTAMP\_TZ\_TO\_NUMERIC\_UDF (TIMESTAMP\_TZ)[¶](#cast-timestamp-tz-to-numeric-udf-timestamp-tz "Link to this heading")

### Definition[¶](#id141 "Link to this heading")

This user-defined function (UDF) is used to cast `timestamp_tz` to numeric. It converts the current timezone to UTC because the numeric value cannot save the `timestamp` information.

```
CAST_TIMESTAMP_TZ_TO_NUMERIC_UDF(INPUT TIMESTAMP_TZ)
```

Copy

### Parameters[¶](#id142 "Link to this heading")

`INPUT` TIMESTAMP\_TZ

The `timestamp` input that is going to be cast.

### Returns[¶](#id143 "Link to this heading")

Returns a numeric with a decimal point. The integer part represents the number of days from 1900-01-01 and the decimal part is the percentage of milliseconds in 24 hours.

### Usage example[¶](#id144 "Link to this heading")

Input:

```
SELECT PUBLIC.CAST_TIMESTAMP_TZ_TO_NUMERIC_UDF('1900-01-01 01:00:00.000 +0100')
```

Copy

Output:

```
0
```

Copy

## RAISERROR\_UDF (VARCHAR, DOUBLE, DOUBLE, ARRAY)[¶](#raiserror-udf-varchar-double-double-array "Link to this heading")

### Definition[¶](#id145 "Link to this heading")

This user-defined function (UDF) throws an exception with a specific message.

```
RAISERROR_UDF(MSG_TEXT VARCHAR, SEVERITY DOUBLE, STATE DOUBLE, PARAMS ARRAY)
```

Copy

### Parameters[¶](#id146 "Link to this heading")

`MSG_TEXT` VARCHAR

The message text of the error message.

`SEVERITY` DOUBLE

The severity number for the error.

`STATE` DOUBLE

The state number for the error message.

`PARAMS` ARRAY

The additional information of the error message.

### Returns[¶](#id147 "Link to this heading")

Returns a varchar with an error message.

### Usage example[¶](#id148 "Link to this heading")

Input:

```
SELECT RAISERROR_UDF('<\<%*.*s>> TEST', 1.0, 1, array_construct());
```

Copy

Output:

```
MESSAGE: <<undefined>> TEST, LEVEL: 1, STATE: 1
```

Copy

## PARSENAME\_UDF[¶](#parsename-udf "Link to this heading")

### Definition[¶](#id149 "Link to this heading")

This user-defined function (UDF) gets the PART\_NUMBER index of a `string` separated by `'.'`.

```
PARSENAME_UDF(STR VARCHAR, PART_NUMBER INT)
```

Copy

### Parameters[¶](#id150 "Link to this heading")

`STR` VARCHAR

The object name as a `string`.

`PART_NUMBER` INT

The part of the object name to be checked.

### Returns[¶](#id151 "Link to this heading")

Returns the specified part of an object name.

### Usage example[¶](#id152 "Link to this heading")

Input:

```
SELECT PARSENAME_UDF('Test_A.Test_B.Test_C]', 2);
```

Copy

Output:

```
Test_B
```

Copy

## ERROR\_STATE\_UDF[¶](#error-state-udf "Link to this heading")

### Definition[¶](#id153 "Link to this heading")

This user-defined function (UDF) gets the error state regardless of how many times it is run, or where it is run within the scope of the `CATCH` block.

```
ERROR_STATE_UDF()
```

Copy

### Parameters[¶](#id154 "Link to this heading")

No input parameters.

### Returns[¶](#id155 "Link to this heading")

Returns the `string` with the error state regardless of how many times it is run, or where it is run within the scope of the `CATCH` block.

### Usage example[¶](#id156 "Link to this heading")

Input:

```
SELECT ERROR_STATE_UDF();
```

Copy

Output:

```
null -- No information set.
```

Copy

## CAST\_TIME\_TO\_TIMESTAMP\_TZ\_UDF (TIME)[¶](#cast-time-to-timestamp-tz-udf-time "Link to this heading")

### Definition[¶](#id157 "Link to this heading")

This user-defined function (UDF) casts `time` to `timestamp_tz`.

```
CAST_TIME_TO_TIMESTAMP_TZ_UDF(INPUT TIME)
```

Copy

### Parameters[¶](#id158 "Link to this heading")

`INPUT` TIME

The input time to be cast to `timestamp_tz`.

### Returns[¶](#id159 "Link to this heading")

Returns a `timestamp_tz` with the date as 1900-01-01 and the same time as the input.

### Usage example[¶](#id160 "Link to this heading")

Input:

```
SELECT PUBLIC.CAST_TIME_TO_TIMESTAMP_TZ_UDF('00:00:00.995')
```

Copy

Output:

```
1900-01-01 00:00:00.997
```

Copy

## SUM\_TIMESTAMP\_TZ\_UDF (TIMESTAMP\_TZ, TIMESTAMP\_TZ)[¶](#sum-timestamp-tz-udf-timestamp-tz-timestamp-tz "Link to this heading")

### Definition[¶](#id161 "Link to this heading")

This user-defined function (UDF) converts both inputs to the system or session timezone and sums the dates taking 1900-01-01 00:00:00.000 as the zero value. If any value does not include the timezone, the current session timezone is used.

```
SUM_TIMESTAMP_TZ_UDF(FIRST_DATE TIMESTAMP_TZ, SECOND_DATE TIMESTAMP_TZ)
```

Copy

### Parameters[¶](#id162 "Link to this heading")

`FIRST_DATE` TIMESTAMP\_TZ

The first date to sum to.

`SECOND_DATE` TIMESTAMP\_TZ

The second date to sum to.

### Returns[¶](#id163 "Link to this heading")

Returns the sum between the two input dates.

### Usage example[¶](#id164 "Link to this heading")

Input:

```
SELECT SUM_TIMESTAMP_TZ_UDF('1900-01-01 00:00:00.000 +0100', '1900-01-01 00:00:00.003 -0100')
```

Copy

Output:

```
1900-01-01 00:00:00.003 +0000
```

Copy

## GET\_WEEK\_START\_UDF[¶](#get-week-start-udf "Link to this heading")

### Definition[¶](#id165 "Link to this heading")

This user-defined function (UDF) retrieves the WEEK\_START configuration, which is equivalent to the @@FIRSTDATE function. To maintain consistency across platforms, ensure the [WEEK\_START](https://docs.snowflake.com/en/sql-reference/parameters#week-start) parameter matches the DATEFIRST setting in Transact-SQL.

```
GET_WEEK_START_UDF()
```

Copy

### Returns[¶](#id166 "Link to this heading")

Returns a number representing the first day of the week.

### Usage example[¶](#id167 "Link to this heading")

Snowflake’s default value for WEEK\_START is `0`. However, this function returns `7` to align with the default DATEFIRST value in Transact-SQL, ensuring consistent behavior.

Input:

```
SELECT GET_WEEK_START_UDF();
```

Copy

Output:

```
7
```

Copy

## DATE\_PART\_WEEK\_DAY\_UDF[¶](#date-part-week-day-udf "Link to this heading")

### Definition[¶](#id168 "Link to this heading")

This user-defined function (UDF) gets the day of the week as a number (1-7) To ensure the consistency across platforms, please set the [WEEK\_START](https://docs.snowflake.com/en/sql-reference/parameters#week-start) parameter to the same value as the DATEFIRST setting in Transact-SQL.

```
DATE_PART_WEEK_DAY_UDF(INPUT DATE)
```

Copy

### Parameters[¶](#id169 "Link to this heading")

`INPUT` DATE

Date to get the day.

### Returns[¶](#id170 "Link to this heading")

Returns a number representing the day of the week where Monday=1, Tuesday=2, …, Sunday=7.

### Usage example[¶](#id171 "Link to this heading")

The WEEK\_START parameter is 0, which causes the DATE\_PART\_WEEK\_DAY\_UDF to return a value of 1.

Input:

```
SELECT PUBLIC.DATE_PART_WEEK_DAY_UDF('2025-08-17') AS "Sunday";
```

Copy

Output:

```
1
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

1. [ISNUMERIC\_UDF](#isnumeric-udf)
2. [PATINDEX\_UDF](#patindex-udf)
3. [ERROR\_SEVERITY\_UDF](#error-severity-udf)
4. [TRANSFORM\_SP\_EXECUTE\_SQL\_STRING\_UDF(STRING, STRING, ARRAY, ARRAY)](#transform-sp-execute-sql-string-udf-string-string-array-array)
5. [TABLE\_OBJECT\_ID\_UDF (VARCHAR)](#table-object-id-udf-varchar)
6. [ERROR\_PROCEDURE\_UDF](#error-procedure-udf)
7. [DB\_ID\_UDF(STRING)](#db-id-udf-string)
8. [ERROR\_LINE\_UDF](#error-line-udf)
9. [FUNCTION\_OBJECT\_ID\_UDF (VARCHAR)](#function-object-id-udf-varchar)
10. [CONSTRAINT\_OBJECT\_ID\_UDF (VARCHAR)](#constraint-object-id-udf-varchar)
11. [FOR\_XML\_UDF (OBJECT, VARCHAR, VARCHAR)](#for-xml-udf-object-varchar-varchar)
12. [OBJECT\_ID\_UDF (VARCHAR)](#object-id-udf-varchar)
13. [PROCEDURE\_OBJECT\_ID\_UDF (VARCHAR)](#procedure-object-id-udf-varchar)
14. [ISDATE\_UDF](#isdate-udf)
15. [ERROR\_NUMBER\_UDF](#error-number-udf)
16. [OFFSET\_FORMATTER (VARCHAR)](#offset-formatter-varchar)
17. [OPENXML\_UDF](#openxml-udf)
18. [QUOTENAME\_UDF (VARCHAR, VARCHAR)](#quotename-udf-varchar-varchar)
19. [UPDATE\_ERROR\_VARS\_UDF (STRING, STRING, STRING)](#update-error-vars-udf-string-string-string)
20. [ROUND\_MILLISECONDS\_UDF (TIMESTAMP\_TZ)](#round-milliseconds-udf-timestamp-tz)
21. [CAST\_NUMERIC\_TO\_TIMESTAMP\_TZ\_UDF (NUMBER)](#cast-numeric-to-timestamp-tz-udf-number)
22. [IDENTITY\_UDF](#identity-udf)
23. [FOR\_XML\_UDF (OBJECT, VARCHAR)](#for-xml-udf-object-varchar)
24. [QUOTENAME\_UDF (VARCHAR)](#quotename-udf-varchar)
25. [VIEW\_OBJECT\_ID\_UDF (VARCHAR)](#view-object-id-udf-varchar)
26. [SUBTRACT\_TIMESTAMP\_TZ\_UDF (TIMESTAMP\_TZ, TIMESTAMP\_TZ)](#subtract-timestamp-tz-udf-timestamp-tz-timestamp-tz)
27. [STR\_UDF (FLOAT, VARCHAR)](#str-udf-float-varchar)
28. [XML\_JSON\_SIMPLE](#xml-json-simple)
29. [FORMATMESSAGE\_UDF](#formatmessage-udf)
30. [IS\_MEMBER\_UDF](#is-member-udf)
31. [RAISERROR\_UDF (DOUBLE, DOUBLE, DOUBLE, ARRAY)](#raiserror-udf-double-double-double-array)
32. [STR\_UDF(FLOAT)](#str-udf-float)
33. [SWITCHOFFSET\_UDF (TIMESTAMP\_TZ, VARCHAR)](#switchoffset-udf-timestamp-tz-varchar)
34. [GET\_CURRENT\_TIMEZONE\_UDF](#get-current-timezone-udf)
35. [UPDATE\_ERROR\_VARS\_UDF (STRING, STRING, STRING, STRING, STRING, STRING)](#update-error-vars-udf-string-string-string-string-string-string)
36. [SEQUENCE\_OBJECT\_ID\_UDF (VARCHAR)](#sequence-object-id-udf-varchar)
37. [CAST\_TIMESTAMP\_TZ\_TO\_NUMERIC\_UDF (TIMESTAMP\_TZ)](#cast-timestamp-tz-to-numeric-udf-timestamp-tz)
38. [RAISERROR\_UDF (VARCHAR, DOUBLE, DOUBLE, ARRAY)](#raiserror-udf-varchar-double-double-array)
39. [PARSENAME\_UDF](#parsename-udf)
40. [ERROR\_STATE\_UDF](#error-state-udf)
41. [CAST\_TIME\_TO\_TIMESTAMP\_TZ\_UDF (TIME)](#cast-time-to-timestamp-tz-udf-time)
42. [SUM\_TIMESTAMP\_TZ\_UDF (TIMESTAMP\_TZ, TIMESTAMP\_TZ)](#sum-timestamp-tz-udf-timestamp-tz-timestamp-tz)
43. [GET\_WEEK\_START\_UDF](#get-week-start-udf)
44. [DATE\_PART\_WEEK\_DAY\_UDF](#date-part-week-day-udf)