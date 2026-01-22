---
auto_generated: true
description: 'In addition to permanent tables, which is the default table type when
  creating tables, Snowflake supports defining tables as either temporary or transient.
  These types of tables are especially useful '
last_scraped: '2026-01-14T16:54:46.963240+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/tables-temp-transient
title: Working with Temporary and Transient Tables | Snowflake Documentation
---

1. [Overview](../guides/README.md)
2. [Snowflake Horizon Catalog](snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../guides/overview-connecting.md)
6. [Virtual warehouses](warehouses.md)
7. [Databases, Tables, & Views](../guides/overview-db.md)

   * [Table Structures](tables-micro-partitions.md)
   * [Temporary And Transient Tables](tables-temp-transient.md)
   * [External Tables](tables-external-intro.md)
   * [Hybrid Tables](tables-hybrid.md)
   * [Interactive tables](interactive.md)
   * [Working with tables in Snowsight](ui-snowsight-data-databases-table.md)
   * [Search optimization service](search-optimization-service.md)
   * Views
   * [Views](views-introduction.md)
   * [Secure Views](views-secure.md)
   * [Materialized Views](views-materialized.md)
   * [Semantic Views](views-semantic/overview.md)
   * [Working with Views in Snowsight](ui-snowsight-data-databases-view.md)
   * Considerations
   * [Views, Materialized Views, and Dynamic Tables](overview-view-mview-dts.md)
   * [Table Design](table-considerations.md)
   * [Cloning](object-clone.md)
   * [Data Storage](tables-storage-considerations.md)
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

[Guides](../guides/README.md)[Databases, Tables, & Views](../guides/overview-db.md)Temporary And Transient Tables

# Working with Temporary and Transient Tables[¶](#working-with-temporary-and-transient-tables "Link to this heading")

In addition to permanent tables, which is the default table type when creating tables, Snowflake supports defining tables as either temporary or
transient. These types of tables are especially useful for storing data that does not need to be maintained for extended periods of time
(i.e. transitory data).

Note

You cannot create [hybrid tables](tables-hybrid) that are temporary or transient. In turn, you cannot create hybrid tables within transient schemas or databases.

## Temporary Tables[¶](#temporary-tables "Link to this heading")

Snowflake supports creating temporary tables for storing non-permanent, transitory data (e.g. ETL data, session-specific data). Temporary tables
only exist within the session in which they were created and persist only for the remainder of the session. As such, they are not visible to other
users or sessions. Once the session ends, data stored in the table is purged completely from the system and, therefore, is not recoverable, either
by the user who created the table or Snowflake.

Note

In addition to tables, Snowflake supports creating certain other database objects as temporary (e.g. stages). These objects follow the same
semantics (i.e. they are session-based, persisting only for the remainder of the session).

### Data Storage Usage for Temporary Tables[¶](#data-storage-usage-for-temporary-tables "Link to this heading")

For the duration of the existence of a temporary table, the data stored in the table contributes to the overall storage charges that Snowflake bills
your account. To prevent any unexpected storage changes, particularly if you create large temporary tables in sessions that you maintain for periods
longer than 24 hours, Snowflake recommends explicitly dropping these tables once they are no longer needed. You can also explicitly exit the session
in which the table was created to ensure no additional charges are accrued.

For more information, see [Comparison of Table Types](#comparison-of-table-types) (in this topic).

### Maintenance of Temporary Tables[¶](#maintenance-of-temporary-tables "Link to this heading")

If your workload generates high volumes of temporary tables, you are very likely to experience degraded performance when you query the
[COLUMNS view](../sql-reference/info-schema/columns) or [TABLES view](../sql-reference/info-schema/tables) in the Information Schema.

Snowflake recommends the following best practices:

* [Drop temporary tables](../sql-reference/sql/drop-table) explicitly before sessions end.
* Make sure that users explicitly log out of sessions that are inactive. See [Snowflake sessions and session policies](session-policies).

Taking these actions consistently will help you avoid query performance degradation that is related to the presence of temporary tables.

### Potential Naming Conflicts with Other Table Types[¶](#potential-naming-conflicts-with-other-table-types "Link to this heading")

Similar to the other table types (transient and permanent), temporary tables belong to a specified database and schema; however, because they are
session-based, they aren’t bound by the same uniqueness requirements. This means you can create temporary and non-temporary tables with the same name
within the same schema.

However, note that the temporary table takes precedence in the session over any other table with the same name in the same schema. This can lead to
potential conflicts and unexpected behavior, particularly when performing DDL on both temporary and non-temporary tables. For example:

* You can create a temporary table that has the same name as an existing table in the same schema, effectively hiding the existing table.
* You can create a table that has the same name as an existing temporary table in the same schema; however, the newly-created table is hidden by the
  temporary table.

Subsequently, all queries and other operations performed in the session on the table affect only the temporary table.

Important

This behavior is particularly important to note when dropping a table in a session and then using Time Travel to restore the table. It is also
important to note this behavior when using CREATE OR REPLACE to create a table because this essentially drops a table (if it exists) and creates a
new table with the specified definition.

### Creating a Temporary Table[¶](#creating-a-temporary-table "Link to this heading")

To create a temporary table, simply specify the TEMPORARY keyword (or TEMP abbreviation) in [CREATE TABLE](../sql-reference/sql/create-table).
You can also use the [TableCollection.create](/developer-guide/snowflake-python-api/reference/latest/_autosummary/snowflake.core.table.TableCollection#snowflake.core.table.TableCollection.create) Python API.

Note that creating a temporary table does not require the CREATE TABLE privilege on the schema in which the object is created.

For example:

SQLPython

```
CREATE TEMPORARY TABLE mytemptable (id NUMBER, creation_date DATE);
```

Copy

```
from snowflake.core.table import Table, TableColumn

my_temp_table = Table(
  name="mytemptable",
  columns=[TableColumn(name="id", datatype="int"),
          TableColumn(name="creation_date", datatype="timestamp_tz")],
  kind="TEMPORARY"
)
root.databases["<database>"].schemas["<schema>"].tables.create(my_temp_table)
```

Copy

Note

After creation, temporary tables cannot be converted to any other table type.

## Transient Tables[¶](#transient-tables "Link to this heading")

Snowflake supports creating transient tables that persist until explicitly dropped and are available to all users with the appropriate privileges.
Transient tables are similar to permanent tables with the key difference that they do not have a Fail-safe period. As a result, transient tables
are specifically designed for transitory data that needs to be maintained beyond each session (in contrast to temporary tables), but does not
need the same level of data protection and recovery provided by permanent tables.

### Data Storage Usage for Transient Tables[¶](#data-storage-usage-for-transient-tables "Link to this heading")

Similar to permanent tables, transient tables contribute to the overall storage charges that Snowflake bills your account; however, because
transient tables do not utilize Fail-safe, there are no Fail-safe costs (i.e. the costs associated with maintaining the data required for
Fail-safe disaster recovery).

For more information, see [Comparison of Table Types](#comparison-of-table-types) (in this topic).

### Transient Tables Created as Clones of Permanent Tables[¶](#transient-tables-created-as-clones-of-permanent-tables "Link to this heading")

When you create a transient table as a clone of a permanent table, Snowflake creates a [zero-copy clone](tables-storage-considerations.html#label-cloning-tables).
This means when the transient table is created, it utilizes no data storage because it shares all of the existing
[micro-partitions](tables-clustering-micropartitions) of the original permanent table.
When rows are added, deleted, or updated in the clone, it results in new micro-partitions that belong exclusively
to the clone (in this case, the transient table).

When a permanent table is deleted, it enters Fail-safe for a 7-day period. Fail-safe bytes incur
[storage costs](data-cdp-storage-costs). If a transient table is created as a clone of a permanent table, this
might delay the time between when the permanent table is deleted and when all of its bytes enter Fail-safe. If the transient
table clone shares any micro-partitions with the permanent table when it is deleted, those shared bytes will only enter
Fail-safe when the transient table is deleted.

### Transient Databases and Schemas[¶](#transient-databases-and-schemas "Link to this heading")

Snowflake also supports creating transient databases and schemas. All tables created in a transient schema, as well as all schemas created in
a transient database, are transient by definition.

### Creating a Transient Table, Schema, or Database[¶](#creating-a-transient-table-schema-or-database "Link to this heading")

To create a transient table, schema, or database, simply specify the TRANSIENT keyword when creating the object:

SQLPython

* [CREATE TABLE](../sql-reference/sql/create-table)
* [CREATE SCHEMA](../sql-reference/sql/create-schema)
* [CREATE DATABASE](../sql-reference/sql/create-database)

* [DatabaseCollection.create](/developer-guide/snowflake-python-api/reference/latest/_autosummary/snowflake.core.database.DatabaseCollection#snowflake.core.database.DatabaseCollection.create)
* [SchemaCollection.create](/developer-guide/snowflake-python-api/reference/latest/_autosummary/snowflake.core.schema.SchemaCollection#snowflake.core.schema.SchemaCollection.create)
* [TableCollection.create](/developer-guide/snowflake-python-api/reference/latest/_autosummary/snowflake.core.table.TableCollection#snowflake.core.table.TableCollection.create)

For example, to create a transient table:

SQLPython

```
CREATE TRANSIENT TABLE mytranstable (id NUMBER, creation_date DATE);
```

Copy

```
from snowflake.core.table import Table, TableColumn

my_trans_table = Table(
  name="mytranstable",
  columns=[TableColumn(name="id", datatype="int"),
          TableColumn(name="creation_date", datatype="timestamp_tz")],
  kind="TRANSIENT"
)
root.databases["<database>"].schemas["<schema>"].tables.create(my_trans_table)
```

Copy

Note

After creation, transient tables cannot be converted to any other table type.

## Comparison of Table Types[¶](#comparison-of-table-types "Link to this heading")

The following table summarizes the differences between the three table types, particularly with regard to their impact on Time Travel and
Fail-safe:

| Type | Persistence | Cloning (source type => target type) | Time Travel Retention Period (Days) | Fail-safe Period (Days) |
| --- | --- | --- | --- | --- |
| Temporary | Remainder of session | Temporary => Temporary . . Temporary => Transient | 0 or 1 (default is 1) | 0 |
| Transient | Until explicitly dropped | Transient => Temporary . . Transient => Transient | 0 or 1 (default is 1) | 0 |
| Permanent ([Standard Edition](intro-editions)) | Until explicitly dropped | Permanent => Temporary . . Permanent => Transient . . Permanent => Permanent | 0 or 1 (default is 1) | 7 |
| Permanent ([Enterprise Edition and higher](intro-editions)) | Until explicitly dropped | Permanent => Temporary . . Permanent => Transient . . Permanent => Permanent | 0 to 90 (default is configurable) | 7 |

### Time Travel Notes[¶](#time-travel-notes "Link to this heading")

* The Time Travel retention period for a table can be specified when the table is created or any time afterwards. Within the retention period,
  all Time Travel operations can be performed on data in the table (e.g. queries) and the table itself (e.g. cloning and restoration).
* If the Time Travel retention period for a permanent table is set to 0, it will immediately enter the Fail-safe period when it is dropped.
* Temporary tables can have a Time Travel retention period of 1 day; however, a temporary table is purged once the session (in which the table
  was created) ends so the actual retention period is for 24 hours or the remainder of the session, whichever is shorter.
* A long-running Time Travel query will delay the purging of temporary and transient tables until the query completes.

### Fail-safe Notes[¶](#fail-safe-notes "Link to this heading")

* The Fail-safe period is not configurable for any table type.
* Transient and temporary tables have no Fail-safe period. As a result, no additional data storage charges are incurred beyond the
  Time Travel retention period.

Important

Because transient tables do not have a Fail-safe period, they provide a good option for managing the cost of very large tables used to store
transitory data; however, the data in these tables cannot be recovered after the Time Travel retention period passes.

For example, if a system failure occurs in which a transient table is dropped or lost, after 1 day, the data is not recoverable by you or
Snowflake. As such, we recommend using transient tables only for data that does not need to be protected against failures or data that
can be reconstructed outside of Snowflake.

For more information, see [Data storage considerations](tables-storage-considerations).

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

1. [Temporary Tables](#temporary-tables)
2. [Transient Tables](#transient-tables)
3. [Comparison of Table Types](#comparison-of-table-types)

Related content

1. [Understanding & using Time Travel](/user-guide/data-time-travel)
2. [Understanding and viewing Fail-safe](/user-guide/data-failsafe)
3. [Storage costs for Time Travel and Fail-safe](/user-guide/data-cdp-storage-costs)
4. [Managing Snowflake databases, schemas, tables, and views with Python](/user-guide/../developer-guide/snowflake-python-api/snowflake-python-managing-databases)