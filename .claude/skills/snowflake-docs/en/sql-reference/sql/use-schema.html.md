---
auto_generated: true
description: 'Specifies the active/current schema for the session:'
last_scraped: '2026-01-14T16:55:49.239949+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/sql/use-schema.html
title: USE SCHEMA | Snowflake Documentation
---

1. [Overview](../../reference.md)
2. [SQL data types reference](../../sql-reference-data-types.md)
3. [SQL command reference](../../sql-reference-commands.md)

   * [Query syntax](../constructs.md)
   * [Query operators](../operators.md)
   * [General DDL](../sql-ddl-summary.md)
   * [General DML](../sql-dml.md)
   * [All commands (alphabetical)](../sql-all.md)")
   * [Accounts](../commands-account.md)
   * [Users, roles, & privileges](../commands-user-role.md)
   * [Integrations](../commands-integration.md)
   * [Business continuity & disaster recovery](../commands-replication.md)
   * [Sessions](../commands-session.md)
   * [Transactions](../commands-transaction.md)
   * [Virtual warehouses & resource monitors](../commands-warehouse.md)
   * [Databases, schemas, & shares](../commands-database.md)

     + Database
     + [CREATE DATABASE](create-database.md)
     + [ALTER DATABASE](alter-database.md)
     + [DESCRIBE DATABASE](desc-database.md)
     + [DROP DATABASE](drop-database.md)
     + [UNDROP DATABASE](undrop-database.md)
     + [USE DATABASE](use-database.md)
     + [SHOW DATABASES](show-databases.md)
     + Schema
     + [ALTER SCHEMA](alter-schema.md)
     + [DESCRIBE SCHEMA](desc-schema.md)
     + [CREATE SCHEMA](create-schema.md)
     + [DROP SCHEMA](drop-schema.md)
     + [UNDROP SCHEMA](undrop-schema.md)
     + [USE SCHEMA](use-schema.md)
     + [SHOW SCHEMAS](show-schemas.md)
     + Share
     + [ALTER SHARE](alter-share.md)
     + [CREATE SHARE](create-share.md)
     + [DROP SHARE](drop-share.md)
     + [SHOW SHARES](show-shares.md)
     + [DESCRIBE SHARE](desc-share.md)
   * [Tables, views, & sequences](../commands-table.md)
   * [Functions, procedures, & scripting](../commands-function.md)
   * [Streams & tasks](../commands-stream.md)
   * [dbt Projects on Snowflake](../commands-dbt-projects-on-snowflake.md)
   * [Classes & instances](../commands-class.md)
   * [Machine learning](../commands-ml.md)
   * [Cortex](../commands-cortex.md)
   * [Listings](../commands-listings.md)
   * [Openflow data plane integration](../commands-ofdata-plane.md)
   * [Organization profiles](../commands-organization-profiles.md)
   * [Security](../commands-security.md)
   * [Data Governance](../commands-data-governance.md)
   * [Privacy](../commands-privacy.md)
   * [Data loading & unloading](../commands-data-loading.md)
   * [File staging](../commands-file.md)
   * [Storage lifecycle policies](../commands-storage-lifecycle-policies.md)
   * [Git](../commands-git.md)
   * [Alerts](../commands-alert.md)
   * [Native Apps Framework](../commands-native-apps.md)
   * [Streamlit](../commands-streamlit.md)
   * [Notebook](../commands-notebook.md)
   * [Snowpark Container Services](../commands-snowpark-container-services.md)
4. [Function and stored procedure reference](../../sql-reference-functions.md)
5. [Class reference](../../sql-reference-classes.md)
6. [Scripting reference](../../sql-reference-snowflake-scripting.md)
7. [General reference](../../sql-reference.md)
8. [API reference](../../api-reference.md)

[Reference](../../reference.md)[SQL command reference](../../sql-reference-commands.md)[Databases, schemas, & shares](../commands-database.md)USE SCHEMA

# USE SCHEMA[¶](#use-schema "Link to this heading")

Specifies the active/current schema for the session:

* If a database is not specified for a session, any objects referenced in queries and other SQL statements executed in
  the session must be fully qualified with the database and schema, also known as the *namespace*, for the object
  (in the form of `db_name.schema_name.object_name`). For more information about fully-qualified object names,
  see [Object name resolution](../name-resolution).
* If a database is specified for a session but the schema is not specified for a session, any objects referenced in queries
  and other SQL statements executed in the session must be qualified with the schema for the object (in the form of
  `schema_name.object_name`).
* If the database and schema are specified for a user session, unqualified object names are allowed in SQL statements and
  queries.

See also:
:   [CREATE SCHEMA](create-schema) , [ALTER SCHEMA](alter-schema) , [DROP SCHEMA](drop-schema) , [SHOW SCHEMAS](show-schemas)

## Syntax[¶](#syntax "Link to this heading")

```
USE [ SCHEMA ] [<db_name>.]<name>
```

Copy

## Parameters[¶](#parameters "Link to this heading")

`[db_name.]name`
:   Specifies the identifier for the schema to use for the session. If the identifier contains spaces or special characters, the entire
    string must be enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

    The SCHEMA keyword is optional if the schema name is fully qualified (in the form of `db_name.schema_name`).

    The database name (`db_name`) is optional if the database is specified in the user session and the SCHEMA keyword
    is included.

## Examples[¶](#examples "Link to this heading")

Use the `myschema` schema with the database specified in the user session:

```
USE SCHEMA myschema;
```

Copy

Use the `myschema` schema in the `mydb` database:

```
USE mydb.myschema;
```

Copy

The following example shows how commands that refer to objects using unqualified names
produce different output after a USE command to switch schemas. The tables, table data,
views, user-defined functions, and so on can differ from one schema to another.

When the [SHOW TABLES](show-tables) command is run in the context of `schema_one`,
it produces output reflecting the objects in that schema:

```
USE SCHEMA schema_one;
SHOW TABLES ->> SELECT "created_on", "name" FROM $1 ORDER BY "created_on";
```

Copy

```
+-------------------------------+-----------+
| created_on                    | name      |
|-------------------------------+-----------|
| 2025-07-13 23:48:49.129 -0700 | TABLE_ABC |
| 2025-07-13 23:49:50.329 -0700 | TABLE_DEF |
+-------------------------------+-----------+
```

After a USE command switches to the `schema_two` schema, the SHOW TABLES command
produces output reflecting a different set of objects:

```
USE SCHEMA schema_two;
SHOW TABLES ->> SELECT "created_on", "name" FROM $1 ORDER BY "created_on";
```

Copy

```
+-------------------------------+-----------+
| created_on                    | name      |
|-------------------------------+-----------|
| 2025-07-13 23:52:06.144 -0700 | TABLE_IJK |
| 2025-07-13 23:53:29.851 -0700 | TABLE_XYZ |
+-------------------------------+-----------+
```

The following example changes from one schema to another, then back to
the original schema. The name of the original schema is stored in a
variable. Run the following commands:

```
SELECT CURRENT_SCHEMA();
SET original_schema = (SELECT CURRENT_SCHEMA());
USE SCHEMA schema_two;
SELECT CURRENT_SCHEMA();
USE SCHEMA IDENTIFIER($original_schema);
SELECT CURRENT_SCHEMA();
```

Copy

The output for these commands shows how the current schema value changes:

```
>SELECT CURRENT_SCHEMA();
+------------+
| SCHEMA_ONE |
+------------+

>SET original_schema = (SELECT CURRENT_SCHEMA());

>USE SCHEMA schema_two;
>SELECT CURRENT_SCHEMA();
+------------+
| SCHEMA_TWO |
+------------+

>USE SCHEMA IDENTIFIER($original_schema);
>SELECT CURRENT_SCHEMA();
+------------+
| SCHEMA_ONE |
+------------+
```

Was this page helpful?

YesNo

[Visit Snowflake](https://www.snowflake.com)

[Join the conversation](https://community.snowflake.com/s/)

[Develop with Snowflake](https://developers.snowflake.com)

[Share your feedback](/feedback)

[Read the latest on our blog](https://www.snowflake.com/blog/)

[Get your own certification](https://learn.snowflake.com)

[Privacy Notice](https://www.snowflake.com/privacy-policy/)[Site Terms](https://www.snowflake.com/legal/snowflake-site-terms/)Cookies Settings© 2026 Snowflake, Inc. All Rights Reserved.

### Alternative interfaces

[Snowflake Python APIs](/developer-guide/snowflake-python-api/snowflake-python-overview)[Snowflake REST APIs](/developer-guide/snowflake-rest-api/snowflake-rest-api)[Snowflake CLI](/developer-guide/snowflake-cli/index)

See all interfaces

On this page

1. [Syntax](#syntax)
2. [Parameters](#parameters)
3. [Examples](#examples)