---
description: Equivalents for DBC objects and columns
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/teradata/sql-translation-reference/database-dbc
title: SnowConvert AI - Teradata - Database DBC | Snowflake Documentation
---

## DBC database

<!-- prettier-ignore -->
|Teradata|Snowflake|Notes|
|---|---|---|
|DBC|INFORMATION_SCHEMA||

> See
> [DBC database](https://docs.teradata.com/r/Teradata-DSA-User-Guide/November-2022/Database-DBC-Info/Database-DBC)

## DBC tables

<!-- prettier-ignore -->
|Teradata|Snowflake|Notes|
|---|---|---|
|COLUMNS|COLUMNS||
|COLUMNSV|COLUMNS||
|DATABASES|DATABASES||
|DBQLOGTBL|TABLE(INFORMATION_SCHEMA.QUERY_HISTORY())||
|TABLES|TABLES||

## DBC columns

<!-- prettier-ignore -->
|Teradata|Snowflake|Notes|
|---|---|---|
|ALLRIGHTS|APPLICABLE_ROLES||
|COLUMNNAME|COLUMN_NAME||
|COLUMNUDTNAME|UDT_NAME||
|COMMENT_STRING|COMMENT||
|CREATETIMESTAMP|CREATED||
|COLUMNTYPE|DATA_TYPE||
|COLUMNLENGTH|CHARACTER_MAXIMUM_LENGTH||
|CONSTRAINTNAME|CONSTRAINT_NAME||
|CONSTRAINTTEXT|CONSTRAINT_TYPE||
|DATABASENAME|TABLE_SCHEMA||
|FINALWDNAME|SESSION_ID||
|FIRSTSTEPTIME|DATEADD(MILLISECOND, TOTAL_ELAPSED_TIME - EXECUTION_TIME, START_TIME)||
|LASTALTERTIMESTAMP|LAST_ALTERED||
|NULLABLE|IS_NULLABLE||
|STARTTIME|START_TIME||
|TABLEKIND|TABLE_TYPE||
|TABLE_LEVELCONSTRAINTS|TABLE_CONSTRAINTS||
|TABLENAME|TABLE_NAME||
|USER_NAME|GRANTEE||

> For more information about DBC tables and columns see the
> [Teradata documentation.](https://docs.teradata.com/r/hNI_rA5LqqKLxP~Y8vJPQg/jwOyftGqfH5vIH1ZRVNW6A)
