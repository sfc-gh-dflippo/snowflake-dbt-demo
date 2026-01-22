---
description: Hive SQL
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/hive/ddls/create-view
title: SnowConvert AI - Hive - CREATE VIEW | Snowflake Documentation
---

## Description

> Views are based on the result-set of an `SQL` query. `CREATE VIEW` constructs a virtual table that
> has no physical data therefore other operations like `ALTER VIEW` and `DROP VIEW` only change
> metadata.
> ([Spark SQL Language Reference CREATE VIEW](https://spark.apache.org/docs/latest/sql-ref-syntax-ddl-create-view.html))

## Grammar Syntax

```sql
CREATE [ OR REPLACE ] [ [ GLOBAL ] TEMPORARY ] VIEW [ IF NOT EXISTS ] view_identifier
    create_view_clauses AS query

create_view_clauses :=
[ ( column_name [ COMMENT column_comment ], ... ) ]
[ COMMENT view_comment ]
[ TBLPROPERTIES ( property_name = property_value [ , ... ] ) ]
```

## Sample Source Patterns

### COMMENT clause

#### Input Code

```sql
CREATE VIEW my_view
COMMENT 'This view selects specific columns from person'
AS
SELECT
   name,
   age,
   address
FROM
   person;
```

#### Output Code

```sql
CREATE VIEW my_view
COMMENT = '{ "Description": "This view selects specific columns from person", "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "databricks",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
AS
SELECT
   name,
   age,
   address
FROM
   person;
```

### OR REPLACE

#### Note

This clause is fully supported in Snowflake

### TEMPORARY (non-GLOBAL) VIEW

#### Note 2

This clause is fully supported in Snowflake

### IF NOT EXISTS

#### Note 3

This clause is fully supported in Snowflake

### Columns list

#### Note 4

This clause is fully supported in Snowflake
