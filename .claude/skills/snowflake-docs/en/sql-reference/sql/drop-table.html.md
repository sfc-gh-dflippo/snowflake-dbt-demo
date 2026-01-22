---
auto_generated: true
description: Removes a table from the current or specified schema, but retains a version
  of the table so that it can be recovered by using UNDROP TABLE. For information,
  see Usage Notes.
last_scraped: '2026-01-14T16:56:47.066984+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/sql/drop-table.html
title: DROP TABLE | Snowflake Documentation
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
   * [Tables, views, & sequences](../commands-table.md)

     + [SHOW OBJECTS](show-objects.md)
     + Table
     + [CREATE TABLE](create-table.md)
     + [ALTER TABLE](alter-table.md)
     + [DROP TABLE](drop-table.md)
     + [UNDROP TABLE](undrop-table.md)
     + [SHOW TABLES](show-tables.md)
     + [SHOW COLUMNS](show-columns.md)
     + [SHOW PRIMARY KEYS](show-primary-keys.md)
     + [DESCRIBE TABLE](desc-table.md)
     + [DESCRIBE SEARCH OPTIMIZATION](desc-search-optimization.md)
     + [TRUNCATE TABLE](truncate-table.md)
     + Dynamic table
     + [CREATE DYNAMIC TABLE](create-dynamic-table.md)
     + [ALTER DYNAMIC TABLE](alter-dynamic-table.md)
     + [DESCRIBE DYNAMIC TABLE](desc-dynamic-table.md)
     + [DROP DYNAMIC TABLE](drop-dynamic-table.md)
     + [UNDROP DYNAMIC TABLE](undrop-dynamic-table.md)
     + [SHOW DYNAMIC TABLES](show-dynamic-tables.md)
     + Event table
     + [CREATE EVENT TABLE](create-event-table.md)
     + [ALTER TABLE (Event Table)](alter-table-event-table.md)")
     + [SHOW EVENT TABLES](show-event-tables.md)
     + [DESCRIBE EVENT TABLE](desc-event-table.md)
     + External table
     + [CREATE EXTERNAL TABLE](create-external-table.md)
     + [ALTER EXTERNAL TABLE](alter-external-table.md)
     + [DROP EXTERNAL TABLE](drop-external-table.md)
     + [SHOW EXTERNAL TABLES](show-external-tables.md)
     + [DESCRIBE EXTERNAL TABLE](desc-external-table.md)
     + Hybrid table
     + [CREATE HYBRID TABLE](create-hybrid-table.md)
     + [CREATE INDEX](create-index.md)
     + [DROP INDEX](drop-index.md)
     + [SHOW HYBRID TABLES](show-hybrid-tables.md)
     + [SHOW INDEXES](show-indexes.md)
     + Apache Iceberg™ table
     + [CREATE ICEBERG TABLE](create-iceberg-table.md)
     + [ALTER ICEBERG TABLE](alter-iceberg-table.md)
     + [DROP ICEBERG TABLE](drop-iceberg-table.md)
     + [UNDROP ICEBERG TABLE](undrop-iceberg-table.md)
     + [SHOW ICEBERG TABLES](show-iceberg-tables.md)
     + [DESCRIBE ICEBERG TABLE](desc-iceberg-table.md)
     + Interactive tables and warehouses
     + [CREATE INTERACTIVE TABLE](create-interactive-table.md)
     + [CREATE INTERACTIVE WAREHOUSE](create-interactive-warehouse.md)
     + View
     + [CREATE VIEW](create-view.md)
     + [ALTER VIEW](alter-view.md)
     + [DROP VIEW](drop-view.md)
     + [SHOW VIEWS](show-views.md)
     + [DESCRIBE VIEW](desc-view.md)
     + Materialized view
     + [CREATE MATERIALIZED VIEW](create-materialized-view.md)
     + [ALTER MATERIALIZED VIEW](alter-materialized-view.md)
     + [DROP MATERIALIZED VIEW](drop-materialized-view.md)
     + [SHOW MATERIALIZED VIEWS](show-materialized-views.md)
     + [DESCRIBE MATERIALIZED VIEW](desc-materialized-view.md)
     + [TRUNCATE MATERIALIZED VIEW](truncate-materialized-view.md)
     + Semantic view
     + [CREATE SEMANTIC VIEW](create-semantic-view.md)
     + [ALTER SEMANTIC VIEW](alter-semantic-view.md)
     + [DROP SEMANTIC VIEW](drop-semantic-view.md)
     + [SHOW SEMANTIC VIEWS](show-semantic-views.md)
     + [SHOW SEMANTIC DIMENSIONS](show-semantic-dimensions.md)
     + [SHOW SEMANTIC DIMENSIONS FOR METRIC](show-semantic-dimensions-for-metric.md)
     + [SHOW SEMANTIC FACTS](show-semantic-facts.md)
     + [SHOW SEMANTIC METRICS](show-semantic-metrics.md)
     + [DESCRIBE SEMANTIC VIEW](desc-semantic-view.md)
     + Sequence
     + [CREATE SEQUENCE](create-sequence.md)
     + [ALTER SEQUENCE](alter-sequence.md)
     + [DROP SEQUENCE](drop-sequence.md)
     + [SHOW SEQUENCES](show-sequences.md)
     + [DESCRIBE SEQUENCE](desc-sequence.md)
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

[Reference](../../reference.md)[SQL command reference](../../sql-reference-commands.md)[Tables, views, & sequences](../commands-table.md)DROP TABLE

# DROP TABLE[¶](#drop-table "Link to this heading")

Removes a table from the current or specified schema, but retains a version of the table so that it can be recovered by using
[UNDROP TABLE](undrop-table). For information, see [Usage Notes](#usage-notes).

See also:
:   [CREATE TABLE](create-table) , [ALTER TABLE](alter-table) , [SHOW TABLES](show-tables) , [TRUNCATE TABLE](truncate-table) , [DESCRIBE TABLE](desc-table)

## Syntax[¶](#syntax "Link to this heading")

```
DROP TABLE [ IF EXISTS ] <name> [ CASCADE | RESTRICT ]
```

Copy

## Parameters[¶](#parameters "Link to this heading")

`name`
:   Specifies the identifier for the table to drop. If the identifier contains spaces, special characters, or mixed-case characters, the
    entire string must be enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive
    (for example, `"My Object"`).

    If the table identifier is not fully-qualified (in the form of `db_name.schema_name.table_name` or
    `schema_name.table_name`), the command looks for the table in the current schema for the session.

`CASCADE | RESTRICT`
:   Specifies whether the table can be dropped if foreign keys exist that reference the table:

    * CASCADE: Drops the table even if the table has primary or unique keys that are referenced by foreign keys in other tables.
    * RESTRICT: Returns a warning about existing foreign key references and doesn’t drop the table.

    Default: CASCADE for standard tables; RESTRICT for hybrid tables. See also [Dropping hybrid tables](#label-dropping-hybrid-tables).

## Access control requirements[¶](#access-control-requirements "Link to this heading")

A [role](../../user-guide/security-access-control-overview.html#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](../../user-guide/security-access-control-overview.html#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Table | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](../../user-guide/security-access-control-configure.html#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](../../user-guide/security-access-control-overview.html#label-access-control-securable-objects), see [Overview of Access Control](../../user-guide/security-access-control-overview).

## Usage notes[¶](#usage-notes "Link to this heading")

* Dropping a table does not permanently remove it from the system. A version of the dropped table is retained in
  [Time Travel](../../user-guide/data-time-travel) for the number of days specified by the
  [data retention period](../../user-guide/data-time-travel.html#label-time-travel-data-retention-period) for the table:

  > + Within the Time Travel retention period, you can restore a dropped table by using the [UNDROP TABLE](undrop-table) command.
  > + Changing the Time Travel retention period for the account or for a parent object (a database or a schema) *after*
  >   you drop a table doesn’t change the Time Travel retention period for the dropped table.
  >   For more information, see the [note in the Time Travel topic](../../user-guide/data-time-travel.html#label-data-retention-for-dropped-table).
  > + When the Time Travel retention period ends, the next state for the dropped table depends on whether it is permanent, transient, or
  >   temporary:
  >
  >   - A permanent table moves into [Fail-safe](../../user-guide/data-failsafe). In Fail-safe (7 days), a dropped table can be recovered,
  >     but only by Snowflake. When the table leaves Fail-safe, it is purged.
  >   - A transient or temporary table has no Fail-safe, so it is purged when it moves out of Time Travel.
  >
  >     Note
  >
  >     A long-running Time Travel query delays the movement of any data and objects (tables, schemas, and databases) in the account into
  >     Fail-safe, until the query completes. The purging of temporary and transient tables is delayed in the same way.
  >   - After a dropped table is purged, it can’t be recovered; it must be recreated.
* After you drop a table, creating a table with the same name creates a new version of the table. You can still restore the dropped version of the
  previous table by following these steps:

  1. Rename the current version of the table.
  2. Use the [UNDROP TABLE](undrop-table) command to restore the previous version of the table.
* Before dropping a table, verify that *no views reference the table*. Dropping a table referenced by a view invalidates the view
  (that is, querying the view returns an “object does not exist” error).
* To drop a table, you must use a role that has OWNERSHIP privilege on the table.

* When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

## Dropping hybrid tables[¶](#dropping-hybrid-tables "Link to this heading")

When you drop a hybrid table without specifying the RESTRICT or CASCADE option, and the hybrid table
has a primary-key/foreign-key or unique-key/foreign-key relationship with another table, the DROP TABLE
command fails with an error. The default behavior is RESTRICT.

For example:

```
CREATE OR REPLACE HYBRID TABLE ht1(
  col1 NUMBER(38,0) NOT NULL,
  col2 NUMBER(38,0) NOT NULL,
  CONSTRAINT pkey_ht1 PRIMARY KEY (col1, col2));

CREATE OR REPLACE HYBRID TABLE ht2(
  cola NUMBER(38,0) NOT NULL,
  colb NUMBER(38,0) NOT NULL,
  colc NUMBER(38,0) NOT NULL,
  CONSTRAINT pkey_ht2 PRIMARY KEY (cola),
  CONSTRAINT fkey_ht1 FOREIGN KEY (colb, colc) REFERENCES ht1(col1,col2));

DROP TABLE ht1;
```

Copy

```
SQL compilation error:
Cannot drop the table because of dependencies
```

The DROP TABLE command fails in this case. If necessary, you can override the default behavior by specifying
CASCADE in the DROP TABLE command.

```
DROP TABLE ht1 CASCADE;
```

Copy

Alternatively in this case, you could drop the dependent table `ht2` first, then drop table `ht1`.

## Examples[¶](#examples "Link to this heading")

Drop a table:

> ```
> SHOW TABLES LIKE 't2%';
>
> +---------------------------------+------+---------------+-------------+-----------+------------+------------+------+-------+--------------+----------------+
> | created_on                      | name | database_name | schema_name | kind      | comment    | cluster_by | rows | bytes | owner        | retention_time |
> |---------------------------------+------+---------------+-------------+-----------+------------+------------+------+-------+--------------+----------------+
> | Tue, 17 Mar 2015 16:48:16 -0700 | T2   | TESTDB        | PUBLIC      | TABLE     |            |            |    5 | 4096  | PUBLIC       |              1 |
> +---------------------------------+------+---------------+-------------+-----------+------------+------------+------+-------+--------------+----------------+
>
> DROP TABLE t2;
>
> +--------------------------+
> | status                   |
> |--------------------------|
> | T2 successfully dropped. |
> +--------------------------+
>
> SHOW TABLES LIKE 't2%';
>
> +------------+------+---------------+-------------+------+---------+------------+------+-------+-------+----------------+
> | created_on | name | database_name | schema_name | kind | comment | cluster_by | rows | bytes | owner | retention_time |
> |------------+------+---------------+-------------+------+---------+------------+------+-------+-------+----------------|
> +------------+------+---------------+-------------+------+---------+------------+------+-------+-------+----------------+
> ```
>
> Copy

Drop the table again, but don’t raise an error if the table does not exist:

> ```
> DROP TABLE IF EXISTS t2;
>
> +------------------------------------------------------------+
> | status                                                     |
> |------------------------------------------------------------|
> | Drop statement executed successfully (T2 already dropped). |
> +------------------------------------------------------------+
> ```
>
> Copy

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
3. [Access control requirements](#access-control-requirements)
4. [Usage notes](#usage-notes)
5. [Dropping hybrid tables](#dropping-hybrid-tables)
6. [Examples](#examples)