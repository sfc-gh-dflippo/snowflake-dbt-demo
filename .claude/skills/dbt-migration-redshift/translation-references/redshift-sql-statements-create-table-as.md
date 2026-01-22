---
description: Create Table As Syntax Grammar.
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/redshift/redshift-sql-statements-create-table-as
title: SnowConvert AI - Redshift - CREATE TABLE AS | Snowflake Documentation
---

## Description

Creates a new table based on a query. The owner of this table is the user that issues the command.

For more information please refer to
[`CREATE TABLE AS`](https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_TABLE_AS.html)
documentation.

## Grammar Syntax

```sql
 CREATE [ [ LOCAL ] { TEMPORARY | TEMP } ]
TABLE table_name
[ ( column_name [, ... ] ) ]
[ BACKUP { YES | NO } ]
[ table_attributes ]
AS query

where table_attributes are:
[ DISTSTYLE { AUTO | EVEN | ALL | KEY } ]
[ DISTKEY( distkey_identifier ) ]
[ [ COMPOUND | INTERLEAVED ] SORTKEY( column_name [, ...] ) ]
```

## SnowConvert AI - Redshift - Table Start

## BACKUP

### Description 2

Enables Amazon Redshift to automatically adjust the encoding type for all columns in the table to
optimize query performance. In Snowflake, the concept of `BACKUP` as seen in other databases is not
directly applicable. Snowflake automatically handles data backup and recovery through its built-in
features like Time Travel and Fail-safe, eliminating the need for manual backup operations. For
these reasons, the statement `BACKUP` is removed during the transformation process

Click [here](https://docs.aws.amazon.com/redshift/latest/dg/t_Distributing_data.html) to navigate to
the Amazon Redshift docs page for this syntax.

### Grammar Syntax 2

```sql
 BACKUP { YES | NO }
```

### Sample Source Patterns

#### NO option

An FDM is added since Snowflake, by default, always creates a backup of the created table.

##### Input Code

##### Redshift

```sql
 CREATE TABLE table1
BACKUP NO
AS SELECT * FROM table_test;
```

##### Output Code

##### Snowflake

```sql
 CREATE TABLE table1
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/10/2025",  "domain": "test" }}'
----** SSC-FDM-RS0001 - BACKUP NO OPTION NOT SUPPORTED. DATA STORAGE IS AUTOMATICALLY HANDLED BY SNOWFLAKE. **
--BACKUP NO
AS SELECT * FROM
table_test;
```

#### YES option

The option is removed since Snowflake, by default, applies a backup to the created table.

##### Input Code: 2

##### Redshift 2

```sql
 CREATE TABLE table1
BACKUP YES
AS SELECT * FROM table_test;
```

##### Output Code: 2

##### Snowflake 2

```sql
 CREATE TABLE table1
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/10/2025",  "domain": "test" }}'
AS SELECT * FROM
table_test;
```

###

### Related EWIs

- [SSC-FDM-RS0001](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/redshiftFDM#ssc-fdm-rs0001):
  “Option” not supported. Data storage is automatically handled by Snowflake.

## COLUMNS

### Description 3

The name of a column in the new table. If no column names are provided, the column names are taken
from the output column names of the query.

Click [here](https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_TABLE_NEW.html) to navigate to
the Amazon Redshift docs page for this syntax.

### Grammar Syntax 3

```sql
 ( column_name [, ... ] )
```

### Sample Source Patterns 2

#### Input Code: 3

##### Redshift 3

```sql
 CREATE TABLE table1
(
    col1, col2, col3
)
AS SELECT col1, col2, col3 FROM table_test;
```

##### Output Code: 3

##### Snowflake 3

```sql
 CREATE TABLE table1
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/17/2024" }}'
(
    col1, col2, col3
)
AS SELECT col1, col2, col3 FROM
        table_test;
```

### Related EWIs 2

There are no known issues.

## LOCAL

### Description 4

In Amazon Redshift, `LOCAL TEMPORARY` or `TEMP` are used to create temporary tables that exist only
for the duration of the session. These tables are session-specific and automatically deleted when
the session ends. They are useful for storing intermediate results or working data without affecting
the permanent database schema.

Click [here](https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_TABLE_NEW.html) to navigate to
the Amazon Redshift docs page for this syntax.

### Grammar Syntax 4

```sql
 LOCAL { TEMPORARY | TEMP }
```

### Sample Source Patterns 3

#### Input Code: 4

##### Redshift 4

```sql
 CREATE LOCAL TEMP TABLE table1
AS SELECT FROM table_test;
```

##### Output Code: 4

##### Snowflake 4

```sql
 CREATE LOCAL TEMP TABLE table1
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/17/2024" }}'
AS SELECT FROM
table_test;
```

### Related EWIs 3

There are no known issues.

## SnowConvert AI - Redshift - Tabla Attributes

## DISTKEY

### Description 5

In Amazon Redshift, `DISTKEY` is used to distribute data across cluster nodes to optimize query
performance. Snowflake, however, automatically handles data distribution and storage without needing
explicit distribution keys. Due to differences in architecture and data management approaches,
Snowflake does not have a direct equivalent to Redshift’s `DISTKEY`. For these reasons, the
statement `DISTKEY` is removed during the transformation process

Click [here](https://docs.aws.amazon.com/redshift/latest/dg/t_Distributing_data.html) to navigate to
the Amazon Redshift docs page for this syntax.

### Grammar Syntax 5

```sql
 DISTKEY ( column_name )
```

### Sample Source Patterns 4

#### Input Code: 5

##### Redshift 5

```sql
 CREATE TABLE table1
DISTKEY (col1)
AS SELECT * FROM table_test;
```

##### Output Code: 5

##### Snowflake 5

```sql
 CREATE TABLE table1
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/10/2025",  "domain": "test" }}'
----** SSC-FDM-RS0001 - DISTKEY OPTION NOT SUPPORTED. DATA STORAGE IS AUTOMATICALLY HANDLED BY SNOWFLAKE. **
--DISTKEY (col1)
AS SELECT * FROM
table_test;
```

### Related EWIs 4

- [SSC-FDM-RS0001](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/redshiftFDM#ssc-fdm-rs0001):
  “Option” not supported. Data storage is automatically handled by Snowflake.

## DISTSTYLE

### Description 6

Keyword that defines the data distribution style for the whole table.

Click [here](https://docs.aws.amazon.com/redshift/latest/dg/t_Distributing_data.html) to navigate to
the Amazon Redshift docs page for this syntax.

### Grammar Syntax 6

```sql
 DISTSTYLE { AUTO | EVEN | KEY | ALL }
```

### Sample Source Patterns 5

#### Input Code: 6

##### Redshift 6

```sql
 CREATE TABLE table1
DISTSTYLE AUTO
AS SELECT * FROM table_test;

CREATE TABLE table2
DISTSTYLE EVEN
AS SELECT * FROM table_test;

CREATE TABLE table3
DISTSTYLE ALL
AS SELECT * FROM table_test;

CREATE TABLE table4
DISTSTYLE KEY
DISTKEY (col1)
AS SELECT * FROM table_test;
```

##### Output Code: 6

##### Snowflake 6

```sql
 CREATE TABLE table1
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/17/2024" }}'
----** SSC-FDM-RS0001 - DISTSTYLE AUTO OPTION NOT SUPPORTED. DATA STORAGE IS AUTOMATICALLY HANDLED BY SNOWFLAKE. **
--DISTSTYLE AUTO
AS SELECT * FROM
table_test;

CREATE TABLE table2
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/17/2024" }}'
----** SSC-FDM-RS0001 - DISTSTYLE EVEN OPTION NOT SUPPORTED. DATA STORAGE IS AUTOMATICALLY HANDLED BY SNOWFLAKE. **
--DISTSTYLE EVEN
AS SELECT * FROM
table_test;

CREATE TABLE table3
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/17/2024" }}'
----** SSC-FDM-RS0001 - DISTSTYLE ALL OPTION NOT SUPPORTED. DATA STORAGE IS AUTOMATICALLY HANDLED BY SNOWFLAKE. **
--DISTSTYLE ALL
AS SELECT * FROM
table_test;

CREATE TABLE table4
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/17/2024" }}'
----** SSC-FDM-RS0001 - DISTSTYLE KEY OPTION NOT SUPPORTED. DATA STORAGE IS AUTOMATICALLY HANDLED BY SNOWFLAKE. **
--DISTSTYLE KEY
----** SSC-FDM-RS0001 - DISTKEY OPTION NOT SUPPORTED. DATA STORAGE IS AUTOMATICALLY HANDLED BY SNOWFLAKE. **
--DISTKEY (col1)
AS SELECT * FROM
table_test;
```

### Related EWIs 5

1. [SSC-FDM-RS0001](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/redshiftFDM#ssc-fdm-rs0001):
   “Option” not supported. Data storage is automatically handled by Snowflake.

## SORTKEY

### Description 7

The keyword that specifies that the column is the sort key for the table. In Snowflake, `SORTKEY`
from Redshift can be migrated to `CLUSTER BY` because both optimize data storage for query
performance. `CLUSTER BY` in Snowflake organizes data on specified columns, similar to how `SORTKEY`
orders data in Redshift.

Click [here](https://docs.aws.amazon.com/redshift/latest/dg/t_Distributing_data.html) to navigate to
the Amazon Redshift docs page for this syntax.

### Grammar Syntax 7

```sql
 [ COMPOUND | INTERLEAVED ] SORTKEY( column_name [, ...] )
```

### Sample Source Patterns 6

#### Input Code: 7

##### Redshift 7

```sql
 CREATE TABLE table1 (
    col1,
    col2,
    col3,
    col4
)
COMPOUND SORTKEY (col1, col3)
AS SELECT * FROM table_test;

CREATE TABLE table2 (
    col1
)
INTERLEAVED SORTKEY (col1)
AS SELECT * FROM table_test;

CREATE TABLE table3 (
    col1
)
SORTKEY (col1)
AS SELECT * FROM table_test;
```

##### Output Code: 7

##### Snowflake 7

```sql
 CREATE TABLE table1
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/17/2024" }}'
(
    col1,
    col2,
    col3,
    col4
)
--** SSC-FDM-RS0002 - THE PERFORMANCE OF THE CLUSTER BY MAY VARY COMPARED TO THE PERFORMANCE OF SORTKEY **
CLUSTER BY (col1, col3)
AS SELECT * FROM
        table_test;

CREATE TABLE table2
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/17/2024" }}'
(
    col1
)
--** SSC-FDM-RS0002 - THE PERFORMANCE OF THE CLUSTER BY MAY VARY COMPARED TO THE PERFORMANCE OF SORTKEY **
CLUSTER BY (col1)
AS SELECT * FROM
        table_test;

CREATE TABLE table3
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/17/2024" }}'
(
    col1
)
--** SSC-FDM-RS0002 - THE PERFORMANCE OF THE CLUSTER BY MAY VARY COMPARED TO THE PERFORMANCE OF SORTKEY **
CLUSTER BY (col1)
AS SELECT * FROM
        table_test;
```

### Related EWIs 6

1. [SSC-FDM-RS0002](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/redshiftFDM#ssc-fdm-rs0002):
   The performance of the CLUSTER BY may vary compared to the performance of Sortkey.
