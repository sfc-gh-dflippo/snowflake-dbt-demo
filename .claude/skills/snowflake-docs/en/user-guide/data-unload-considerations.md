---
auto_generated: true
description: This topic provides best practices, general guidelines, and important
  considerations for unloading data from a table. It is intended to help simplify
  exporting data from Snowflake tables into files in
last_scraped: '2026-01-14T16:57:46.395927+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/data-unload-considerations
title: Data unloading considerations | Snowflake Documentation
---

1. [Overview](../guides/README.md)
2. [Snowflake Horizon Catalog](snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../guides/overview-connecting.md)
6. [Virtual warehouses](warehouses.md)
7. [Databases, Tables, & Views](../guides/overview-db.md)
8. [Data types](../data-types.md)
10. Data Integration

    - [Snowflake Openflow](data-integration/openflow/about.md)
    - Apache Iceberg™

      - [Apache Iceberg™ Tables](tables-iceberg.md)
      - [Snowflake Open Catalog](opencatalog/overview.md)
11. Data engineering

    - [Data loading](../guides/overview-loading-data.md)
    - [Dynamic Tables](dynamic-tables-about.md)
    - [Streams and Tasks](data-pipelines-intro.md)
    - [dbt Projects on Snowflake](data-engineering/dbt-projects-on-snowflake.md)
    - [Data Unloading](../guides/overview-unloading-data.md)

      * [Overview](data-unload-overview.md)
      * [Features](intro-summary-unloading.md)
      * [Considerations](data-unload-considerations.md)
      * [Preparing to Unload Data](data-unload-prepare.md)
      * [Unloading into a Snowflake Stage](data-unload-snowflake.md)
      * [Unloading into Amazon S3](data-unload-s3.md)
      * [Unloading into Google Cloud Storage](data-unload-gcs.md)
      * [Unloading into Microsoft Azure](data-unload-azure.md)
12. [Storage Lifecycle Policies](storage-management/storage-lifecycle-policies.md)
13. [Migrations](../migrations/README.md)
15. [Queries](../guides/overview-queries.md)
16. [Listings](../collaboration/collaboration-listings-about.md)
17. [Collaboration](../guides/overview-sharing.md)
19. [Snowflake AI & ML](../guides/overview-ai-features.md)
21. [Snowflake Postgres](snowflake-postgres/about.md)
23. [Alerts & Notifications](../guides/overview-alerts.md)
25. [Security](../guides/overview-secure.md)
26. [Data Governance](../guides/overview-govern.md)
27. [Privacy](../guides/overview-privacy.md)
29. [Organizations & Accounts](../guides/overview-manage.md)
30. [Business continuity & data recovery](replication-intro.md)
32. [Performance optimization](../guides/overview-performance.md)
33. [Cost & Billing](../guides/overview-cost.md)

[Guides](../guides/README.md)Data engineering[Data Unloading](../guides/overview-unloading-data.md)Considerations

# Data unloading considerations[¶](#data-unloading-considerations "Link to this heading")

This topic provides best practices, general guidelines, and important considerations for unloading data from a table. It is intended to help simplify
exporting data from Snowflake tables into files in stages using the [COPY INTO <location>](../sql-reference/sql/copy-into-location) command.

## Empty strings and NULL values[¶](#empty-strings-and-null-values "Link to this heading")

An empty string is a string with zero length or no characters, whereas NULL values represent an absence of data. In CSV files, a NULL value is typically represented by two successive delimiters (e.g. `,,`) to indicate that the field contains no data; however, you can use string values to denote NULL (e.g. `null`) or any unique string. An empty string is typically represented by a quoted empty string (e.g. `''`) to indicate that the string contains zero characters.

The following file format options enable you to differentiate between empty strings and NULL values when unloading or loading data. For more information about these file formats, see [CREATE FILE FORMAT](../sql-reference/sql/create-file-format):

`FIELD_OPTIONALLY_ENCLOSED_BY = 'character' | NONE`
:   Use this option to enclose strings in the specified character: single quote (`'`), double quote (`"`), or NONE.

    Enclosing string values in quotes while unloading data is not required. The COPY INTO location command can unload empty string values without enclosing quotes, with the EMPTY\_FIELD\_AS\_NULL option set to
    FALSE. If the EMPTY\_FIELD\_AS\_NULL option is TRUE (which is prohibited), then empty strings and NULL values are indistinguishable in the output file.

    When a field contains this character, escape it using the same character. For example, if the value is the double quote character and a field contains the string `"A"`, escape the double quotes as
    follows: `""A""`.

    Default: `NONE`

`EMPTY_FIELD_AS_NULL = TRUE | FALSE`
:   * When unloading empty string data from tables, choose one of the following options:

      + Preferred: Enclose strings in quotes by setting the `FIELD_OPTIONALLY_ENCLOSED_BY` option, to distinguish empty strings from NULLs in output CSV files.
      + Leave string fields unenclosed by setting the `FIELD_OPTIONALLY_ENCLOSED_BY` option to `NONE` (default), and set the `EMPTY_FIELD_AS_NULL` value to `FALSE` to unload empty strings as empty fields.

        Important

        If you choose this option, make sure to specify a replacement string for NULL data using the `NULL_IF` option, to distinguish NULL values from empty strings in the output file. If you later choose
        to load data from the output files, you will specify the same `NULL_IF` value to identify the NULL values in the data files.
    * When loading data into tables, use this option to specify whether to insert SQL NULL for empty fields in an input file. If set to FALSE, Snowflake attempts to cast an empty field to the corresponding
      column type. An empty string is inserted into columns of data type STRING. For other column types, the COPY command produces an error.

    Default: `TRUE`

`NULL_IF = ( 'string1' [ , 'string2' ... ] )`
:   When unloading data from tables: Snowflake converts SQL NULL values to the first value in the list. Be careful to specify a value that you want interpreted as NULL. For example, if you are unloading data to a file that will get read by another system, make sure to specify a value that will be interpreted as NULL by that system.

    Default: `\\N` (i.e. NULL, which assumes the `ESCAPE_UNENCLOSED_FIELD` value is `\\` (default))

### Example: Unloading and loading data with enclosing quotes[¶](#example-unloading-and-loading-data-with-enclosing-quotes "Link to this heading")

In the following example, a set of data is unloaded from the `null_empty1` table to the user’s stage. The output data file is then used to load data into the `null_empty2` table:

```
-- Source table (null_empty1) contents
+---+------+--------------+
| i | V    | D            |
|---+------+--------------|
| 1 | NULL | NULL value   |
| 2 |      | Empty string |
+---+------+--------------+

-- Create a file format that describes the data and the guidelines for processing it
create or replace file format my_csv_format
  field_optionally_enclosed_by='0x27' null_if=('null');

-- Unload table data into a stage
copy into @mystage
  from null_empty1
  file_format = (format_name = 'my_csv_format');

-- Output the data file contents
1,'null','NULL value'
2,'','Empty string'

-- Load data from the staged file into the target table (null_empty2)
copy into null_empty2
    from @mystage/data_0_0_0.csv.gz
    file_format = (format_name = 'my_csv_format');

select * from null_empty2;

+---+------+--------------+
| i | V    | D            |
|---+------+--------------|
| 1 | NULL | NULL value   |
| 2 |      | Empty string |
+---+------+--------------+
```

Copy

### Example: Unloading and loading data without enclosing quotes[¶](#example-unloading-and-loading-data-without-enclosing-quotes "Link to this heading")

In the following example, a set of data is unloaded from the `null_empty1` table to the user’s stage. The output data file is then used to load data into the `null_empty2` table:

```
-- Source table (null_empty1) contents
+---+------+--------------+
| i | V    | D            |
|---+------+--------------|
| 1 | NULL | NULL value   |
| 2 |      | Empty string |
+---+------+--------------+

-- Create a file format that describes the data and the guidelines for processing it
create or replace file format my_csv_format
  empty_field_as_null=false null_if=('null');

-- Unload table data into a stage
copy into @mystage
  from null_empty1
  file_format = (format_name = 'my_csv_format');

-- Output the data file contents
1,null,NULL value
2,,Empty string

-- Load data from the staged file into the target table (null_empty2)
copy into null_empty2
    from @mystage/data_0_0_0.csv.gz
    file_format = (format_name = 'my_csv_format');

select * from null_empty2;

+---+------+--------------+
| i | V    | D            |
|---+------+--------------|
| 1 | NULL | NULL value   |
| 2 |      | Empty string |
+---+------+--------------+
```

Copy

## Unloading to a single file[¶](#unloading-to-a-single-file "Link to this heading")

By default, COPY INTO location statements separate table data into a set of output files to take advantage of parallel operations. The maximum size for each file is set using the `MAX_FILE_SIZE` copy option. The default value is `16777216` (16 MB) but can be increased to accommodate larger files. The maximum file size supported is 5 GB for Amazon S3, Google Cloud Storage, or Microsoft Azure stages.

To unload data to a single output file (at the potential cost of decreased performance), specify the `SINGLE = true` copy option in your statement. You can optionally specify a name for the file in the path.

Note

If the `COMPRESSION` option is set to true, specify a filename with the appropriate file extension for the compression method so that the output file can be decompressed. For example, specify the GZ file extension if the `GZIP` compression method is specified.

For example, unload the `mytable` table data to a single file named `myfile.csv` in a named stage. Increase the `MAX_FILE_SIZE` limit to accommodate the large data set:

```
copy into @mystage/myfile.csv.gz from mytable
file_format = (type=csv compression='gzip')
single=true
max_file_size=4900000000;
```

Copy

## Unloading a relational table to JSON[¶](#unloading-a-relational-table-to-json "Link to this heading")

You can use the OBJECT\_CONSTRUCT function combined with the COPY command to convert the rows in a relational table to a single VARIANT column and unload the rows into a file.

For example:

```
-- Create a table
CREATE OR REPLACE TABLE mytable (
 id number(8) NOT NULL,
 first_name varchar(255) default NULL,
 last_name varchar(255) default NULL,
 city varchar(255),
 state varchar(255)
);

-- Populate the table with data
INSERT INTO mytable (id,first_name,last_name,city,state)
 VALUES
 (1,'Ryan','Dalton','Salt Lake City','UT'),
 (2,'Upton','Conway','Birmingham','AL'),
 (3,'Kibo','Horton','Columbus','GA');

-- Unload the data to a file in a stage
COPY INTO @mystage
 FROM (SELECT OBJECT_CONSTRUCT('id', id, 'first_name', first_name, 'last_name', last_name, 'city', city, 'state', state) FROM mytable)
 FILE_FORMAT = (TYPE = JSON);

-- The COPY INTO location statement creates a file named data_0_0_0.json.gz in the stage.
-- The file contains the following data:

{"city":"Salt Lake City","first_name":"Ryan","id":1,"last_name":"Dalton","state":"UT"}
{"city":"Birmingham","first_name":"Upton","id":2,"last_name":"Conway","state":"AL"}
{"city":"Columbus","first_name":"Kibo","id":3,"last_name":"Horton","state":"GA"}
```

Copy

## Unloading a relational table to Parquet with multiple columns[¶](#unloading-a-relational-table-to-parquet-with-multiple-columns "Link to this heading")

You can unload data in a relational table to a multi-column Parquet file by using a [SELECT](../sql-reference/sql/select) statement as input to the COPY statement. The SELECT statement specifies the column data in the relational table to include in the unloaded file. Use the `HEADER = TRUE` copy option to include the column headers in the output files.

For example, unload the rows from three columns (`id`, `name`, `start_date`) in the `mytable` table into one or more files that have the naming format `myfile.parquet`:

```
COPY INTO @mystage/myfile.parquet FROM (SELECT id, name, start_date FROM mytable)
  FILE_FORMAT=(TYPE='parquet')
  HEADER = TRUE;
```

Copy

## Explicitly converting numeric columns to Parquet data types[¶](#explicitly-converting-numeric-columns-to-parquet-data-types "Link to this heading")

By default, when table data is unloaded to Parquet files, [fixed-point number](../sql-reference/data-types-numeric.html#label-data-types-for-fixed-point-numbers) columns are
unloaded as DECIMAL columns, while [floating-point number](../sql-reference/data-types-numeric.html#label-data-types-for-floating-point-numbers) columns are unloaded as
DOUBLE columns.

To choose the Parquet data types for sets of unloaded data, call the [CAST , ::](../sql-reference/functions/cast) function in the COPY INTO
*<location>* statement to convert specific table columns to explicit data types. A query in a COPY INTO *<location>* statement
enables selecting specific columns to unload and accepts conversion SQL functions to transform the column data.

Queries in COPY INTO *<location>* statements support the syntax and semantics of SELECT statements to query specific Snowflake table
columns to unload. Convert the data in numeric columns to specific data types using the [CAST , ::](../sql-reference/functions/cast) function.

The following table maps Snowflake numeric data types to Parquet physical and logical data types:

| Snowflake Logical Data Type | Parquet Physical Data Type | Parquet Logical Data Type |
| --- | --- | --- |
| TINYINT | INT32 | INT(8) |
| SMALLINT | INT32 | INT(16) |
| INT | INT32 | INT(32) |
| BIGINT | INT64 | INT(64) |
| FLOAT | FLOAT | N/A |
| DOUBLE | DOUBLE | N/A |

The following example shows a COPY INTO *<location>* statement that converts the numeric data in each unloaded column to a different data type to explicitly choose the data types in the Parquet files:

```
COPY INTO @mystage
FROM (SELECT CAST(C1 AS TINYINT) ,
             CAST(C2 AS SMALLINT) ,
             CAST(C3 AS INT),
             CAST(C4 AS BIGINT) FROM mytable)
FILE_FORMAT=(TYPE=PARQUET);
```

Copy

## Floating-point numbers truncated[¶](#floating-point-numbers-truncated "Link to this heading")

When [floating-point number](../sql-reference/data-types-numeric.html#label-data-types-for-floating-point-numbers) columns are unloaded to CSV or JSON files, Snowflake
truncates the values to approximately (15,9).

The values are not truncated when unloading floating-point number columns to Parquet files.

Was this page helpful?

YesNo

[Visit Snowflake](https://www.snowflake.com)

[Join the conversation](https://community.snowflake.com/s/)

[Develop with Snowflake](https://developers.snowflake.com)

[Share your feedback](/feedback)

[Read the latest on our blog](https://www.snowflake.com/blog/)

[Get your own certification](https://learn.snowflake.com)

[Privacy Notice](https://www.snowflake.com/privacy-policy/)[Site Terms](https://www.snowflake.com/legal/snowflake-site-terms/)Cookies Settings© 2026 Snowflake, Inc. All Rights Reserved.

On this page

1. [Empty strings and NULL values](#empty-strings-and-null-values)
2. [Unloading to a single file](#unloading-to-a-single-file)
3. [Unloading a relational table to JSON](#unloading-a-relational-table-to-json)
4. [Unloading a relational table to Parquet with multiple columns](#unloading-a-relational-table-to-parquet-with-multiple-columns)
5. [Explicitly converting numeric columns to Parquet data types](#explicitly-converting-numeric-columns-to-parquet-data-types)
6. [Floating-point numbers truncated](#floating-point-numbers-truncated)

Related content

1. [COPY INTO <table>](/user-guide/../sql-reference/sql/copy-into-table)
2. [CREATE FILE FORMAT](/user-guide/../sql-reference/sql/create-file-format)
3. [Virtual warehouses](/user-guide/warehouses)