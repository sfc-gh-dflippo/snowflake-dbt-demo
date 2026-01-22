---
auto_generated: true
description: Creates a dynamic table, based on a specified query.
last_scraped: '2026-01-14T16:55:05.196365+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/sql/create-dynamic-table
title: CREATE DYNAMIC TABLE | Snowflake Documentation
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

[Reference](../../reference.md)[SQL command reference](../../sql-reference-commands.md)[Tables, views, & sequences](../commands-table.md)CREATE DYNAMIC TABLE

# CREATE DYNAMIC TABLE[¶](#create-dynamic-table "Link to this heading")

Creates a [dynamic table](../../user-guide/dynamic-tables-about), based on a specified query.

This command supports the following variants:

* [CREATE OR ALTER DYNAMIC TABLE](#label-create-or-alter-dt-syntax): Creates a dynamic table if it doesn’t exist or alters an existing dynamic table.
* [CREATE DYNAMIC TABLE FROM BACKUP SET](#label-create-dt-backup-syntax): Restores a dynamic table from a back up.
* [CREATE DYNAMIC TABLE … CLONE](#label-create-dt-clone-syntax): Creates a clone of an existing dynamic table.
* [CREATE DYNAMIC ICEBERG TABLE](#label-create-dt-iceberg-syntax): Creates a dynamic Apache Iceberg™ table.

See also:
:   [ALTER DYNAMIC TABLE](alter-dynamic-table), [DESCRIBE DYNAMIC TABLE](desc-dynamic-table), [DROP DYNAMIC TABLE](drop-dynamic-table) , [SHOW DYNAMIC TABLES](show-dynamic-tables),
    [CREATE OR ALTER <object>](create-or-alter)

## Syntax[¶](#syntax "Link to this heading")

```
CREATE [ OR REPLACE ] [ TRANSIENT ] DYNAMIC TABLE [ IF NOT EXISTS ] <name> (
    -- Column definition
    <col_name> <col_type>
      [ [ WITH ] MASKING POLICY <policy_name> [ USING ( <col_name> , <cond_col1> , ... ) ] ]
      [ [ WITH ] PROJECTION POLICY <policy_name> ]
      [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
      [ WITH CONTACT ( <purpose> = <contact_name> [ , <purpose> = <contact_name> ... ] ) ]
      [ COMMENT '<string_literal>' ]

    -- Additional column definitions
    [ , <col_name> <col_type> [ ... ] ]

  )
  TARGET_LAG = { '<num> { seconds | minutes | hours | days }' | DOWNSTREAM }
  WAREHOUSE = <warehouse_name>
  [ INITIALIZATION_WAREHOUSE = <warehouse_name> ]
  [ REFRESH_MODE = { AUTO | FULL | INCREMENTAL } ]
  [ INITIALIZE = { ON_CREATE | ON_SCHEDULE } ]
  [ CLUSTER BY ( <expr> [ , <expr> , ... ] ) ]
  [ DATA_RETENTION_TIME_IN_DAYS = <integer> ]
  [ MAX_DATA_EXTENSION_TIME_IN_DAYS = <integer> ]
  [ COMMENT = '<string_literal>' ]
  [ COPY GRANTS ]
  [ [ WITH ] ROW ACCESS POLICY <policy_name> ON ( <col_name> [ , <col_name> ... ] ) ]
  [ [ WITH ] AGGREGATION POLICY <policy_name> [ ENTITY KEY ( <col_name> [ , <col_name> ... ] ) ] ]
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
  [ REQUIRE USER ]
  [ IMMUTABLE WHERE ( <expr> ) ]
  [ BACKFILL FROM ]
  AS <query>
```

Copy

## Variant syntax[¶](#variant-syntax "Link to this heading")

### CREATE OR ALTER DYNAMIC TABLE[¶](#create-or-alter-dynamic-table "Link to this heading")

```
CREATE OR ALTER DYNAMIC TABLE <name> (
  -- Column definition
  <col_name> <col_type>
    [ COLLATE '<collation_specification>' ]
    [ COMMENT '<string_literal>' ]

  -- Additional column definitions
  [ , <col_name> <col_type> [ ... ] ]
  )
  TARGET_LAG = { '<num> { seconds | minutes | hours | days }' | DOWNSTREAM }
  WAREHOUSE = <warehouse_name>
  [ REFRESH_MODE = FULL | INCREMENTAL | AUTO ]
  [ IMMUTABLE WHERE ( <expr> ) ]
  [ CLUSTER BY ( <expr> [ , <expr> , ... ] ) ]
  [ DATA_RETENTION_TIME_IN_DAYS = <integer> ]
  [ MAX_DATA_EXTENSION_TIME_IN_DAYS = <integer> ]
  [ COMMENT = '<string_literal>' ]
```

Copy

Creates a dynamic table if it doesn’t exist, or alters it according to the dynamic table
definition. The CREATE OR ALTER DYNAMIC TABLE syntax follows the rules of a
[CREATE DYNAMIC TABLE](#) statement and has the same limitations as
an [ALTER DYNAMIC TABLE](alter-dynamic-table) statement.

For more information, see [CREATE OR ALTER <object>](create-or-alter).

Changes to the following dynamic table properties and parameters preserve data:

* TARGET\_LAG
* WAREHOUSE
* CLUSTER BY
* DATA\_RETENTION\_TIME\_IN\_DAYS
* MAX\_DATA\_EXTENSION\_TIME\_IN\_DAYS
* COMMENT
* IMMUTABLE WHERE

  + When specified, only the mutable region is reinitialized and data in the immutable region is preserved. For more information, see [Use immutability constraints on dynamic tables](../../user-guide/dynamic-tables-immutability-constraints).

Changes to the following dynamic table properties and parameters trigger a [reinitialization](../../user-guide/dynamic-tables-refresh.html#label-dynamic-tables-initialization):

* REFRESH\_MODE
* Changes to the query or column list:

  + Dropping existing columns is supported.
  + Adding new columns is supported, but they can only be added at the end of existing columns.
  + Dropping columns that are used in an IMMUTABLE WHERE predicate or as clustering keys isn’t supported.

For more information, see [CREATE OR ALTER TABLE usage notes](create-table.html#label-create-or-alter-table-usage-notes).

### CREATE DYNAMIC TABLE FROM BACKUP SET[¶](#create-dynamic-table-from-backup-set "Link to this heading")

[![Snowflake logo in black (no text)](../../_images/logo-snowflake-black.png)](../../_images/logo-snowflake-black.png) [Preview Feature](../../release-notes/preview-features) — Open

Available to all accounts.

```
CREATE DYNAMIC TABLE <name> FROM BACKUP SET <backup_set> IDENTIFIER '<backup_id>'
```

Copy

The FROM BACKUP SET clause restores a dynamic table from a backup. You don’t specify other table
properties because they’re all the same as in the backed-up table.

This form doesn’t have a CREATE OR REPLACE clause. You typically either restore the
dynamic table under a new name and recover any data or other objects from this new table,
or rename the original table and then restore the table under the original name.

Note

The backup set is associated with the internal table ID of the original table.
Any more backups you add to the backup set use the original table, even if you
changed its name. If you want to make backups of the newly restored table, create a
new backup set for it.

When you restore a dynamic table from a backup, Snowflake
[automatically initializes](../../user-guide/dynamic-tables-refresh.html#label-dynamic-tables-initialization)
the new table during its first refresh.

For more information about backups, see [Backups for disaster recovery and immutable storage](../../user-guide/backups).

`backup_set`
:   Specifies the name of a backup set created for a specific dynamic table.
    You can use the SHOW BACKUP SETS command to locate the right backup set.

`backup_id`
:   Specifies the identifier of a specific backup within that backup set.
    You can use the SHOW BACKUPS IN BACKUP SET command to locate the right identifier within the backup
    set, based on the creation date and time for the backup.

### CREATE DYNAMIC TABLE … CLONE[¶](#create-dynamic-table-clone "Link to this heading")

Creates a new dynamic table with the same column definitions and containing all the
existing data from the source dynamic table, without actually copying the data.

Cloned dynamic tables, whether cloned directly or as part of a cloned database or schema, are suspended by default. In [DYNAMIC\_TABLE\_GRAPH\_HISTORY](../functions/dynamic_table_graph_history),
this appears as CLONED\_AUTO\_SUSPENDED in the SCHEDULING\_STATE column. Any downstream dynamic tables are also suspended, shown as UPSTREAM\_CLONED\_AUTO\_SUSPENDED.
For more information, see [Automatic dynamic table suspension](../../user-guide/dynamic-tables-suspend-resume.html#label-dynamic-tables-manage-understanidng-auto-suspend).

You can also clone a dynamic table as it existed at a specific point in the past. For
more information, see [Cloning considerations](../../user-guide/object-clone).

```
CREATE [ OR REPLACE ] [ TRANSIENT ] DYNAMIC TABLE <name>
  CLONE <source_dynamic_table>
        [ { AT | BEFORE } ( { TIMESTAMP => <timestamp> | OFFSET => <time_difference> | STATEMENT => <id> } ) ]
  [
    COPY GRANTS
    TARGET_LAG = { '<num> { seconds | minutes | hours | days }' | DOWNSTREAM }
    WAREHOUSE = <warehouse_name>
  ]
```

Copy

If the source dynamic table has clustering keys, then the cloned dynamic table has
clustering keys. By default, Automatic Clustering is suspended for the new table, even
if Automatic Clustering was not suspended for the source table.

For more details about cloning, see [CREATE <object> … CLONE](create-clone).

### CREATE DYNAMIC ICEBERG TABLE[¶](#create-dynamic-iceberg-table "Link to this heading")

Creates a new dynamic Apache Iceberg™ table. For information about Iceberg tables, see
[Apache Iceberg™ tables](../../user-guide/tables-iceberg) and [CREATE ICEBERG TABLE (Snowflake as the Iceberg catalog)](create-iceberg-table-snowflake).

```
CREATE [ OR REPLACE ] DYNAMIC ICEBERG TABLE <name> (
  -- Column definition
  <col_name> <col_type>
    [ [ WITH ] MASKING POLICY <policy_name> [ USING ( <col_name> , <cond_col1> , ... ) ] ]
    [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
    [ COMMENT '<string_literal>' ]

  -- Additional column definitions
  [ , <col_name> <col_type> [ ... ] ]

)
TARGET_LAG = { '<num> { seconds | minutes | hours | days }' | DOWNSTREAM }
WAREHOUSE = <warehouse_name>
[ EXTERNAL_VOLUME = '<external_volume_name>' ]
[ CATALOG = 'SNOWFLAKE' ]
[ BASE_LOCATION = '<optional_directory_for_table_files>' ]
[ REFRESH_MODE = { AUTO | FULL | INCREMENTAL } ]
[ INITIALIZE = { ON_CREATE | ON_SCHEDULE } ]
[ CLUSTER BY ( <expr> [ , <expr> , ... ] ) ]
[ DATA_RETENTION_TIME_IN_DAYS = <integer> ]
[ MAX_DATA_EXTENSION_TIME_IN_DAYS = <integer> ]
[ COMMENT = '<string_literal>' ]
[ COPY GRANTS ]
[ [ WITH ] ROW ACCESS POLICY <policy_name> ON ( <col_name> [ , <col_name> ... ] ) ]
[ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
[ REQUIRE USER ]
AS <query>
```

Copy

For more information about usage and limitations, see
[Create dynamic Apache Iceberg™ tables](../../user-guide/dynamic-tables-create-iceberg).

## Required parameters[¶](#required-parameters "Link to this heading")

`name`
:   Specifies the identifier (i.e. name) for the dynamic table; must be unique for the schema in which the dynamic table is created.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the
    entire identifier string is enclosed in double quotes (e.g. `"My object"`). Identifiers enclosed in double quotes are also
    case-sensitive.

    For more details, see [Identifier requirements](../identifiers-syntax).

`TARGET_LAG = { num { seconds | minutes | hours | days } | DOWNSTREAM }`
:   Specifies the lag for the dynamic table:

    > `'num seconds | minutes | hours | days'`
    > :   Specifies the maximum amount of time that the dynamic table’s content should lag behind updates to the source tables.
    >
    >     For example:
    >
    >     * If the data in the dynamic table should lag by no more than 5 minutes, specify `5 minutes`.
    >     * If the data in the dynamic table should lag by no more than 5 hours, specify `5 hours`.
    >
    >     Must be a minimum of 60 seconds. If the dynamic table depends on another dynamic table, the minimum target lag must
    >     be greater than or equal to the target lag of the dynamic table it depends on.
    >
    > `DOWNSTREAM`
    > :   Specifies that the dynamic table should be refreshed only when dynamic tables that depend on it are refreshed.

`WAREHOUSE = warehouse_name`
:   Specifies the name of the warehouse that provides the compute resources for refreshing the dynamic table.

    You must use a role that has the USAGE privilege on this warehouse in order to create the dynamic table. For limitations and more
    information, see [Privileges to create a dynamic table](../../user-guide/dynamic-tables-privileges.html#label-dynamic-tables-privileges).

`AS query`
:   Specifies the query whose results the dynamic table should contain.

## Optional parameters[¶](#optional-parameters "Link to this heading")

`INITIALIZATION_WAREHOUSE = warehouse_name`
:   Specifies a warehouse to use for all dynamic table [initializations and reinitializations](../../user-guide/dynamic-tables-refresh.html#label-dynamic-tables-initialization).

    If this parameter isn’t included in the CREATE DYNAMIC TABLE statement, the dynamic table uses the warehouse that is specified by the
    required WAREHOUSE parameter for all refreshes.

    You must use a role that has the USAGE privilege on this warehouse for you to create the dynamic table. For limitations and more
    information, see [Privileges to create a dynamic table](../../user-guide/dynamic-tables-privileges.html#label-dynamic-tables-privileges).

`TRANSIENT`
:   Specifies that the table is transient.

    Like permanent dynamic tables, [transient](../../user-guide/tables-temp-transient) dynamic tables exist until
    they’re explicitly dropped, and are available to any user with the appropriate privileges. Transient dynamic
    tables don’t retain data in fail-safe storage, which helps reduce storage costs, especially for tables that
    refresh frequently. Due to this reduced level of durability, transient dynamic tables are best used for
    transitory data that doesn’t need the same level of data protection and recovery provided by permanent tables.

    Default: No value. If a dynamic table is not declared as `TRANSIENT`, it is permanent.

`REFRESH_MODE = { AUTO | FULL | INCREMENTAL }`
:   Specifies the [refresh mode](../../user-guide/dynamic-tables-refresh) for the dynamic table.

    This property cannot be altered after you create the dynamic table. To modify the property, recreate the dynamic table with a CREATE OR
    REPLACE DYNAMIC TABLE command.

    > `AUTO`
    > :   When refresh mode is `AUTO`, the system attempts to apply an incremental refresh by default. However, when incremental refresh isn’t
    >     supported or expected to perform well, the dynamic table automatically selects full refresh instead. For more information, see
    >     [Dynamic table refresh modes](../../user-guide/dynamic-tables-refresh.html#label-dynamic-tables-intro-refresh-modes) and [Best practices for choosing dynamic table refresh modes](../../user-guide/dynamic-tables-refresh.html#label-best-practices-performance-refresh-modes).
    >
    >     To determine the best mode for your use case, experiment with refresh modes and automatic recommendations. For consistent behavior across
    >     Snowflake releases, explicitly set the refresh mode on all dynamic tables.
    >
    >     To verify the refresh mode for your dynamic tables, see [View dynamic table refresh mode](../../user-guide/dynamic-tables-refresh.html#label-dynamic-tables-monitoring-refresh-mode).
    >
    > `FULL`
    > :   Enforces a full refresh of the dynamic table, even if the dynamic table can be incrementally refreshed.
    >
    > `INCREMENTAL`
    > :   Enforces an incremental refresh of the dynamic table. If the query that underlies the dynamic table can’t perform an incremental refresh,
    >     dynamic table creation fails and displays an error message.
    >
    > Default: `AUTO`

`INITIALIZE`
:   Specifies the behavior of the [initial refresh](../../user-guide/dynamic-tables-refresh) of the dynamic table. This property cannot be
    altered after you create the dynamic table. To modify the property, replace the dynamic table with a CREATE OR REPLACE DYNAMIC TABLE command.

    > `ON_CREATE`
    > :   Refreshes the dynamic table synchronously at creation. If this refresh fails, dynamic table creation fails and displays an error message.
    >
    > `ON_SCHEDULE`
    > :   Refreshes the dynamic table at the next scheduled refresh.
    >
    >     The dynamic table is populated when the refresh schedule process runs. No data is populated when the dynamic table is created. If you try to
    >     query the table using `SELECT * FROM DYNAMIC TABLE`, you might see the following error because the first scheduled refresh has not yet
    >     occurred.
    >
    >     ```
    >     Dynamic Table is not initialized. Please run a manual refresh or wait for a scheduled refresh before querying.
    >     ```
    >
    > Default: `ON_CREATE`

`COMMENT 'string_literal'`
:   Specifies a comment for the column.

    (Note that comments can be specified at the column level or the table level. The syntax for each is slightly different.)

`MASKING POLICY = policy_name`
:   Specifies the [masking policy](../../user-guide/security-column-intro) to set on a column.

`PROJECTION POLICY policy_name`
:   Specifies the [projection policy](../../user-guide/projection-policies) to set on a column.

    This parameter is not supported by the CREATE OR ALTER variant syntax.

`column_list`
:   If you want to change the name of a column or add a comment to a column in the dynamic table,
    include a column list that specifies the column names and, if needed, comments about
    the columns. You do not need to specify the data types of the columns.

    If any of the columns in the dynamic table are based on expressions - for example, not simple column names -
    then you must supply a column name for each column in the dynamic table. For instance, the column names are
    required in the following case:

    ```
    CREATE DYNAMIC TABLE my_dynamic_table (pre_tax_profit, taxes, after_tax_profit)
      TARGET_LAG = '20 minutes'
        WAREHOUSE = mywh
        AS
          SELECT revenue - cost, (revenue - cost) * tax_rate, (revenue - cost) * (1.0 - tax_rate)
          FROM staging_table;
    ```

    Copy

    You can specify an optional comment for each column. For example:

    ```
    CREATE DYNAMIC TABLE my_dynamic_table (pre_tax_profit COMMENT 'revenue minus cost',
                    taxes COMMENT 'assumes taxes are a fixed percentage of profit',
                    after_tax_profit)
      TARGET_LAG = '20 minutes'
        WAREHOUSE = mywh
        AS
          SELECT revenue - cost, (revenue - cost) * tax_rate, (revenue - cost) * (1.0 - tax_rate)
          FROM staging_table;
    ```

    Copy

`WITH CONTACT ( purpose = contact [ , purpose = contact ...] )`
:   Associate the new object with one or more [contacts](../../user-guide/contacts-using).

`CLUSTER BY ( expr [ , expr , ... ] )`
:   Specifies one or more columns or column expressions in the dynamic table as the clustering key. Before you specify a clustering
    key for a dynamic table, you should understand micro-partitions. For more information, see [Understanding Snowflake Table Structures](../../user-guide/tables-micro-partitions).

    Note the following when using clustering keys with dynamic tables:

    * Column definitions are required and must be explicitly specified in the statement.
    * By default, Automatic Clustering is not suspended for the new dynamic table, even if Automatic Clustering is suspended for the
      source table.
    * Clustering keys are not intended or recommended for all tables; they typically benefit very large (for example
      multi-terabyte) tables.
    * Specifying CLUSTER BY doesn’t cluster the data at creation time; instead, CLUSTER BY relies on
      Automatic Clustering to recluster the data over time.

    For more information, see [Clustering Keys & Clustered Tables](../../user-guide/tables-clustering-keys).

    Default: No value (no clustering key is defined for the table)

`DATA_RETENTION_TIME_IN_DAYS = integer`
:   Specifies the retention period for the dynamic table so that Time Travel actions (SELECT, CLONE) can be performed on historical
    data in the dynamic table. Time Travel behaves the same way for dynamic tables as it behaves for traditional tables. For more
    information, see [Understanding & using Time Travel](../../user-guide/data-time-travel).

    For a detailed description of this object-level parameter, as well as more information about object parameters, see
    [Parameters](../parameters).

    Values:

    * Standard Edition: `0` or `1`
    * Enterprise Edition:

      + `0` to `90` for permanent tables
      + `0` or `1` for temporary and transient tables

    Default:

    * Standard Edition: `1`
    * Enterprise Edition (or higher): `1` (unless a different default value was specified at the schema, database, or account level)

    Note

    A value of `0` effectively disables Time Travel for the table.

`MAX_DATA_EXTENSION_TIME_IN_DAYS = integer`
:   An object parameter that sets the maximum number of days Snowflake can extend the data retention period to prevent streams on the dynamic
    table from becoming stale.

    For a detailed description of this parameter, see [MAX\_DATA\_EXTENSION\_TIME\_IN\_DAYS](../parameters.html#label-max-data-extension-time-in-days).

`COMMENT = 'string_literal'`
:   Specifies a comment for the dynamic table.

    (Note that comments can be specified at the column level or the table level. The syntax for each is slightly different.)

    Default: No value.

`COPY GRANTS`
:   Specifies to retain the access privileges from the original table when a new dynamic table is created using any of the following CREATE DYNAMIC TABLE variants:

    * CREATE OR REPLACE DYNAMIC TABLE
    * CREATE OR REPLACE DYNAMIC ICEBERG TABLE
    * CREATE OR REPLACE DYNAMIC TABLE … CLONE

    This parameter copies all privileges except OWNERSHIP from the existing dynamic table to the new dynamic table. The new dynamic
    table does not inherit any future grants defined for the object type in the schema. By default, the role that executes the
    CREATE DYNAMIC TABLE statement owns the new dynamic table.

    If this parameter is not included in the CREATE DYNAMIC TABLE statement, then the new table does not inherit any explicit access
    privileges granted on the original dynamic table, but does inherit any future grants defined for the object type in the schema.

    If the statement is replacing an existing table of the same name, then the grants are copied from the table being replaced. If there is
    no existing table of that name, then the grants are copied.

    For example, the following statement creates a dynamic table `dt1` cloned from `dt0` with all grants copied from `dt0`. The first
    time you run the command, `dt1` copies all grants from `dt0`. If you run the same command again, `dt1` will copy all grants from
    `dt1` and not `dt0`.

    ```
    CREATE OR REPLACE DYNAMIC TABLE dt1 CLONE dt0
      COPY GRANTS;
    ```

    Copy

    Note the following:

    * With [data sharing](../../guides-overview-sharing):

      + If the existing dynamic table was shared to another account, the replacement dynamic table is also shared.
      + If the existing dynamic table was shared with your account as a data consumer, and access was further granted to other roles in
        the account (using `GRANT IMPORTED PRIVILEGES` on the parent database), access is also granted to the replacement dynamic
        table.
    * The [SHOW GRANTS](show-grants) output for the replacement dynamic table lists the grantee for the copied privileges as the
      role that executed the CREATE TABLE statement, with the current timestamp when the statement was executed.
    * The [SHOW GRANTS](show-grants) output for the replacement dynamic table lists the grantee for the copied privileges as the
      role that executed the CREATE TABLE statement, with the current timestamp when the statement was executed.
    * The operation to copy grants occurs atomically in the CREATE DYNAMIC TABLE command (i.e. within the same transaction).

    Important

    The COPY GRANTS parameter can be placed anywhere in a CREATE [ OR REPLACE ] DYNAMIC TABLE command, except after the query
    definition.

    For example, the following dynamic table will fail to create:

    ```
    CREATE OR REPLACE DYNAMIC TABLE my_dynamic_table
      TARGET_LAG = DOWNSTREAM
      WAREHOUSE = mywh
      AS
        SELECT * FROM staging_table
        COPY GRANTS;
    ```

    Copy

`ROW ACCESS POLICY policy_name ON ( col_name [ , col_name ... ] )`
:   Specifies the [row access policy](../../user-guide/security-row-intro) to set on a dynamic table.

`TAG ( tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ] )`
:   Specifies the [tag](../../user-guide/object-tagging/introduction) name and the tag string value.

    The tag value is always a string, and the maximum number of characters for the tag value is 256.

    For information about specifying tags in a statement, see [Tag quotas](../../user-guide/object-tagging/introduction.html#label-object-tagging-quota).

`AGGREGATION POLICY policy_name [ ENTITY KEY ( col_name [ , col_name ... ] ) ]`
:   Specifies an [aggregation policy](../../user-guide/aggregation-policies) to set on a dynamic table. You can apply one or more aggregation
    policies on a table.

    Use the optional ENTITY KEY parameter to define which columns uniquely identity an entity within the dynamic table. For more information,
    see [Implementing entity-level privacy with aggregation policies](../../user-guide/aggregation-policies-entity-privacy). You can specify one or more entity keys for an aggregation policy.

    This parameter is not supported by the CREATE OR ALTER variant syntax.

`REQUIRE USER`
:   When specified, the dynamic table cannot run unless a user is specified. The dynamic table is not able to refresh unless a user is set
    in a manual refresh with the [COPY SESSION](alter-dynamic-table.html#label-alter-dynamic-table-refresh) parameter specified.

    If this option is enabled, the dynamic table must be created with the [ON\_SCHEDULE](#label-create-dt-initialize) parameter for
    `INITIALIZE`.

`IMMUTABLE WHERE`
:   Specifies a condition that defines the immutable portion of the dynamic table. For more information, see [Use immutability constraints on dynamic tables](../../user-guide/dynamic-tables-immutability-constraints).

`BACKFILL FROM <name>`
:   Specifies the table to backfill data from.

    Only data defined by the [IMMUTABLE WHERE immutability constraint](../../user-guide/dynamic-tables-immutability-constraints) can be backfilled because
    the backfill data must remain unchanged, even if it differs from the upstream source.

    For more information, see [Create dynamic tables by using backfill](../../user-guide/dynamic-tables-create.html#label-create-dt-using-backfill).

## Access control requirements[¶](#access-control-requirements "Link to this heading")

A [role](../../user-guide/security-access-control-overview.html#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](../../user-guide/security-access-control-overview.html#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE DYNAMIC TABLE | Schema in which you plan to create the dynamic table. |  |
| SELECT | Tables, views, and dynamic tables that you plan to query for the new dynamic table. |  |
| USAGE | Warehouse that you plan to use to refresh the table. |  |

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](../../user-guide/security-access-control-configure.html#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](../../user-guide/security-access-control-overview.html#label-access-control-securable-objects), see [Overview of Access Control](../../user-guide/security-access-control-overview).

## Usage notes[¶](#usage-notes "Link to this heading")

* When you execute the CREATE DYNAMIC TABLE command, the current role in use becomes
  the owner of the dynamic table. This role is used to perform refreshes of the dynamic
  table in the background.
* You cannot make changes to the schema after you create a dynamic table.
* Dynamic tables are updated as underlying database objects change. Change tracking must
  be enabled on all underlying objects used by a dynamic table. See
  [Enable change tracking](../../user-guide/dynamic-tables-create.html#label-dynamic-tables-and-change-tracking).
* If you want to replace an existing dynamic table and need to see its current definition,
  call the [GET\_DDL](../functions/get_ddl) function.
* Using [ORDER BY](../constructs/order-by) in the definition of a dynamic table
  might produce results sorted in an unexpected order. You can use ORDER BY when querying
  your dynamic table to ensure that rows selected return in a specific order.
* Snowflake doesn’t support using ORDER BY to create a view that selects from a dynamic
  table.
* To influence the order in which rows are stored in a dynamic table, consider enabling [clustering](#label-cluster-dts).
* Some expressions, clauses, and functions are not currently supported in dynamic tables.
  For a complete list, see [Dynamic table limitations](../../user-guide/dynamic-tables-limitations).
* Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](../metadata).

* The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
* CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

## CREATE OR ALTER DYNAMIC TABLE usage notes[¶](#create-or-alter-dynamic-table-usage-notes "Link to this heading")

[![Snowflake logo in black (no text)](../../_images/logo-snowflake-black.png)](../../_images/logo-snowflake-black.png) [Preview Feature](../../release-notes/preview-features) — Open

Available to all accounts.

* All limitations of the [ALTER DYNAMIC TABLE](alter-dynamic-table) command apply.

## Limitations[¶](#limitations "Link to this heading")

The following actions *aren’t* supported:

> * Swapping dynamic tables by using the SWAP WITH parameter.
> * Renaming a dynamic table by using the RENAME TO parameter.
> * Creating a clone of a dynamic table by using the CLONE parameter.
> * Suspending or resuming by using the SUSPEND and RESUME parameters.
> * Converting a TRANSIENT dynamic table into a non-TRANSIENT dynamic table, or vice versa.
> * Adding or changing tags and policies. Any existing tags and policies are preserved,
>   and other statements might still add or remove tags and policies.
> * Creating or altering dynamic Apache Iceberg™ tables.
> * Time Travel clone for times that are before the latest definition or refresh mode change.

Additionally, modifying the values for the REFRESH\_MODE and INITIALIZE properties after
the dynamic table has been created isn’t supported. You can switch between the `AUTO`
refresh mode and the specific `INCREMENTAL` and `FULL` refresh modes, but doing so
doesn’t change the actual physical refresh mode of the dynamic table.

For example:

* If you create a dynamic table with `AUTO` refresh mode, the system immediately assigns
  a concrete mode (`INCREMENTAL` or `FULL`). When you run a subsequent CREATE OR ALTER
  DYNAMIC TABLE statement, you can specify `AUTO` or the concrete refresh mode that is chosen by
  the engine at creation. However, this doesn’t alter the assigned refresh mode; it
  remains the same.
* If you create a dynamic table with a specific refresh mode (`INCREMENTAL` or `FULL`),
  you can later specify `AUTO` in a CREATE OR ALTER DYNAMIC TABLE statement to enable
  forward compatibility. For example, if your dynamic table was created with `FULL`
  mode and is version-controlled, specifying `AUTO` in a CREATE OR ALTER DYNAMIC TABLE
  statement enables new tables to use `AUTO`, while existing tables remain in `FULL`
  mode without breaking compatibility.

## No implicit refreshes[¶](#no-implicit-refreshes "Link to this heading")

If you change an existing dynamic table by using the CREATE OR ALTER DYNAMIC TABLE
command, the command doesn’t trigger a refresh of the dynamic table. The dynamic table is
refreshes according to its normal schedule.

However, if you create a new dynamic table by using the CREATE OR ALTER DYNAMIC TABLE
command and you specify `INITIALIZE = ON_CREATE`, the command triggers a refresh of the
dynamic table.

## Atomicity[¶](#atomicity "Link to this heading")

The CREATE OR ALTER DYNAMIC TABLE command doesn’t guarantee *atomicity*. This means that if
a CREATE OR ALTER DYNAMIC TABLE statement fails during execution, it’s possible that a
subset of changes might have been applied to the table. If there’s a possibility of
partial changes, in most cases, the error message includes the following text:

```
CREATE OR ALTER execution failed. Partial updates may have been applied.
```

For example, suppose that you wanted to change the `TARGET_LAG` property and add a
clustering key for a dynamic table, but you change your mind and terminate the statement. In
this case, the `TARGET_LAG` property might still change while the clustering key isn’t
applied.

When changes are partially applied, the resulting table is in a valid state. In the
previous example, you can use additional ALTER DYNAMIC TABLE statements to complete the
original set of changes.

To recover from partial updates, try the following recovery methods:

* **Fix forward**: Re-execute the CREATE OR ALTER DYNAMIC TABLE statement. If the
  statement succeeds on the second attempt, the target state is achieved.

  If the statement doesn’t succeed, investigate the error message. If possible, fix the
  error and re-execute the CREATE OR ALTER DYNAMIC TABLE statement.
* **Roll back**: If it isn’t possible to fix forward, manually roll back the partial
  changes:

  + Investigate the state of the table by using the [DESCRIBE DYNAMIC TABLE](desc-dynamic-table)
    and [SHOW DYNAMIC TABLES](show-dynamic-tables) commands. Determine which partial
    changes were applied, if any.

    If partial changes were applied, execute the appropriate ALTER DYNAMIC TABLE
    statements to transform the dynamic table back to its original statement.

For additional help, contact [Snowflake Support](../../user-guide/contacting-support).

## Examples[¶](#examples "Link to this heading")

Create a dynamic table named `my_dynamic_table`:

```
CREATE OR REPLACE DYNAMIC TABLE my_dynamic_table
  TARGET_LAG = '20 minutes'
  WAREHOUSE = mywh
  AS
    SELECT product_id, product_name FROM staging_table;
```

Copy

In the example above:

* The dynamic table materializes the results of a query of the `product_id` and `product_name` columns of the
  `staging_table` table.
* The target lag time is 20 minutes, which means that the data in the dynamic table should ideally be no more than 20 minutes
  older than the data in `staging_table`.
* The automated refresh process uses the compute resources in warehouse `mywh` to refresh the data in the dynamic table.

Create a dynamic Iceberg table named `my_dynamic_table` that reads from `my_iceberg_table`:

```
CREATE DYNAMIC ICEBERG TABLE my_dynamic_table (date TIMESTAMP_NTZ, id NUMBER, content STRING)
  TARGET_LAG = '20 minutes'
  WAREHOUSE = mywh
  EXTERNAL_VOLUME = 'my_external_volume'
  CATALOG = 'SNOWFLAKE'
  BASE_LOCATION = 'my_iceberg_table'
  AS
    SELECT product_id, product_name FROM staging_table;
```

Copy

Create a dynamic table with a multi-column clustering key:

```
CREATE DYNAMIC TABLE my_dynamic_table (date TIMESTAMP_NTZ, id NUMBER, content VARIANT)
  TARGET_LAG = '20 minutes'
  WAREHOUSE = mywh
  CLUSTER BY (date, id)
  AS
    SELECT product_id, product_name FROM staging_table;
```

Copy

Clone a dynamic table as it existed exactly at the date and time of the specified timestamp:

```
CREATE DYNAMIC TABLE my_cloned_dynamic_table CLONE my_dynamic_table AT (TIMESTAMP => TO_TIMESTAMP_TZ('04/05/2013 01:02:03', 'mm/dd/yyyy hh24:mi:ss'));
```

Copy

Configure a dynamic table to require a user for refreshes and then refresh the dynamic table:

```
CREATE DYNAMIC TABLE my_dynamic_table
  TARGET_LAG = 'DOWNSTREAM'
  WAREHOUSE = mywh
  INITIALIZE = on_schedule
  REQUIRE USER
  AS
    SELECT product_id, product_name FROM staging_table;
```

Copy

```
ALTER DYNAMIC TABLE my_dynamic_table REFRESH COPY SESSION;
```

Copy

Create a dynamic table by using the CREATE OR ALTER DYNAMIC TABLE command:

```
CREATE OR ALTER DYNAMIC TABLE my_dynamic_table
  TARGET_LAG = DOWNSTREAM
  WAREHOUSE = mywh
  AS
    SELECT a, b FROM t;
```

Copy

Note

CREATE OR ALTER TABLE statements for existing tables can only be executed by a role with the OWNERSHIP privilege on `my_dynamic_table`.

Alter a dynamic table to set the DATA\_RETENTION\_TIME\_IN\_DAYS parameter and add a clustering key:

```
CREATE OR ALTER DYNAMIC TABLE my_dynamic_table
 TARGET_LAG = DOWNSTREAM
 WAREHOUSE = mywh
 DATA_RETENTION_TIME_IN_DAYS = 2
 CLUSTER BY (a)
 AS
   SELECT a, b FROM t;
```

Copy

Modify the target lag and change the warehouse:

```
CREATE OR ALTER DYNAMIC TABLE my_dynamic_table
 TARGET_LAG = '5 minutes'
 WAREHOUSE = my_other_wh
 DATA_RETENTION_TIME_IN_DAYS = 2
 CLUSTER BY (a)
 AS
   SELECT a, b FROM t;
```

Copy

Unset the DATA\_RETENTION\_TIME\_IN\_DAYS parameter. The absence of a parameter in the
modified CREATE OR ALTER DYNAMIC TABLE statement results in unsetting it. In this case,
unsetting the DATA\_RETENTION\_TIME\_IN\_DAYS parameter for the dynamic table resets it to
the default value of 1:

```
CREATE OR ALTER DYNAMIC TABLE my_dynamic_table
 TARGET_LAG = '5 minutes'
 WAREHOUSE = my_other_wh
 CLUSTER BY (a)
 AS
   SELECT a, b FROM t;
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

### Alternative interfaces

[Snowflake Python APIs](/developer-guide/snowflake-python-api/snowflake-python-overview)[Snowflake REST APIs](/developer-guide/snowflake-rest-api/snowflake-rest-api)[Snowflake CLI](/developer-guide/snowflake-cli/index)

See all interfaces

On this page

1. [Syntax](#syntax)
2. [Variant syntax](#variant-syntax)
3. [Required parameters](#required-parameters)
4. [Optional parameters](#optional-parameters)
5. [Access control requirements](#access-control-requirements)
6. [Usage notes](#usage-notes)
7. [CREATE OR ALTER DYNAMIC TABLE usage notes](#create-or-alter-dynamic-table-usage-notes)
8. [Limitations](#limitations)
9. [No implicit refreshes](#no-implicit-refreshes)
10. [Atomicity](#atomicity)
11. [Examples](#examples)

Related content

1. [Dynamic tables](/sql-reference/sql/../../user-guide/dynamic-tables-about)