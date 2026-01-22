---
auto_generated: true
description: 'Specifies the active/current database for the session:'
last_scraped: '2026-01-14T16:57:35.839244+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/sql/use-database.html
title: USE DATABASE | Snowflake Documentation
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

[Reference](../../reference.md)[SQL command reference](../../sql-reference-commands.md)[Databases, schemas, & shares](../commands-database.md)USE DATABASE

# USE DATABASE[¶](#use-database "Link to this heading")

Specifies the active/current database for the session:

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
:   [CREATE DATABASE](create-database) , [ALTER DATABASE](alter-database) , [DROP DATABASE](drop-database) , [SHOW DATABASES](show-databases)

## Syntax[¶](#syntax "Link to this heading")

```
USE [ DATABASE ] <name>
```

Copy

## Parameters[¶](#parameters "Link to this heading")

`name`
:   Specifies the identifier for the database to use for the session. If the identifier contains spaces or special characters, the
    entire string must be enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

## Usage notes[¶](#usage-notes "Link to this heading")

* The DATABASE keyword does not need to be specified.
* USE DATABASE automatically specifies PUBLIC as the current schema, unless the PUBLIC schema doesn’t exist (e.g. it has been dropped).
  To specify a different schema for a session, use the [USE SCHEMA](use-schema) command.

## Examples[¶](#examples "Link to this heading")

The following example specifies the database to use for subsequent SQL commands:

```
USE DATABASE mydb;
```

Copy

The following example shows how commands that refer to objects using unqualified names
produce different output after a USE command to switch databases. The schemas, tables,
table data, and so on can differ from one database to another.

When the [SHOW SCHEMAS](show-schemas) command is run in the context of `database_one`,
it produces output reflecting the objects in that database:

```
USE DATABASE database_one;
SHOW SCHEMAS ->> SELECT "created_on", "name" FROM $1 ORDER BY "created_on";

+-------------------------------+--------------------+
| 2025-07-11 14:34:24.386 -0700 | PUBLIC             |
| 2025-07-11 14:42:23.509 -0700 | TEST_SCHEMA        |
| 2025-07-11 14:42:29.158 -0700 | STAGING_SCHEMA     |
| 2025-07-11 14:45:43.124 -0700 | INFORMATION_SCHEMA |
+-------------------------------+--------------------+
```

Copy

After a USE command switches to the `database_two` database, the SHOW SCHEMAS
command produces output reflecting a different set of objects:

```
USE DATABASE database_two;
SHOW SCHEMAS ->> SELECT "created_on", "name" FROM $1 ORDER BY "created_on";
```

Copy

```
+-------------------------------+--------------------+
| 2025-07-11 14:34:31.496 -0700 | PUBLIC             |
| 2025-07-11 14:43:04.394 -0700 | PRODUCTION_SCHEMA  |
| 2025-07-11 14:44:23.006 -0700 | DASHBOARDS_SCHEMA  |
| 2025-07-11 14:45:54.372 -0700 | INFORMATION_SCHEMA |
+-------------------------------+--------------------+
```

The following example changes from one database to another, then back to
the original database. The name of the original database is stored in a
variable. Run the following commands:

```
SELECT CURRENT_DATABASE();
SET original_database = (SELECT CURRENT_DATABASE());
USE DATABASE database_two;
SELECT CURRENT_DATABASE();
USE DATABASE IDENTIFIER($original_database);
SELECT CURRENT_DATABASE();
```

Copy

The output for these commands shows how the current database value changes:

```
>SELECT CURRENT_DATABASE();
+--------------+
| DATABASE_ONE |
+--------------+

>SET original_database = (SELECT CURRENT_DATABASE());

>USE DATABASE database_two;
>SELECT CURRENT_DATABASE();
+--------------+
| DATABASE_TWO |
+--------------+

>USE DATABASE IDENTIFIER($original_database);
>SELECT CURRENT_DATABASE();
+--------------+
| DATABASE_ONE |
+--------------+
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
3. [Usage notes](#usage-notes)
4. [Examples](#examples)