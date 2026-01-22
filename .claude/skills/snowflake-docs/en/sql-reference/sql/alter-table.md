---
auto_generated: true
description: Modifies the properties, columns, or constraints for an existing table.
last_scraped: '2026-01-14T16:55:53.807278+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/sql/alter-table
title: ALTER TABLE | Snowflake Documentation
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

       - [ALTER TABLE ... ALTER COLUMN](alter-table-column.md)
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

[Reference](../../reference.md)[SQL command reference](../../sql-reference-commands.md)[Tables, views, & sequences](../commands-table.md)ALTER TABLE

# ALTER TABLE[¶](#alter-table "Link to this heading")

Modifies the properties, columns, or constraints for an existing table.

See also:
:   [ALTER TABLE … ALTER COLUMN](alter-table-column) , [CREATE TABLE](create-table) , [DROP TABLE](drop-table) , [SHOW TABLES](show-tables) , [DESCRIBE TABLE](desc-table)

## Syntax[¶](#syntax "Link to this heading")

```
 ALTER TABLE [ IF EXISTS ] <name> RENAME TO <new_table_name>

 ALTER TABLE [ IF EXISTS ] <name> SWAP WITH <target_table_name>

 ALTER TABLE [ IF EXISTS ] <name> { clusteringAction | tableColumnAction | constraintAction  }

 ALTER TABLE [ IF EXISTS ] <name> dataMetricFunctionAction

 ALTER TABLE [ IF EXISTS ] <name> dataGovnPolicyTagAction

 ALTER TABLE [ IF EXISTS ] <name> extTableColumnAction

 ALTER TABLE [ IF EXISTS ] <name> searchOptimizationAction

 ALTER TABLE [ IF EXISTS ] <name> ADD STORAGE LIFECYCLE POLICY <policy_name>
   ON ( <col_name> [ , <col_name> ... ] )

ALTER TABLE [ IF EXISTS ] <name> DROP STORAGE LIFECYCLE POLICY

 ALTER TABLE [ IF EXISTS ] <name> SET
   [ DATA_RETENTION_TIME_IN_DAYS = <integer> ]
   [ MAX_DATA_EXTENSION_TIME_IN_DAYS = <integer> ]
   [ CHANGE_TRACKING = { TRUE | FALSE  } ]
   [ DEFAULT_DDL_COLLATION = '<collation_specification>' ]
   [ ENABLE_SCHEMA_EVOLUTION = { TRUE | FALSE } ]
   [ CONTACT <purpose> = <contact_name> [ , <purpose> = <contact_name> ... ] ]
   [ COMMENT = '<string_literal>' ]

 ALTER TABLE [ IF EXISTS ] <name> UNSET {
                                        DATA_RETENTION_TIME_IN_DAYS         |
                                        MAX_DATA_EXTENSION_TIME_IN_DAYS     |
                                        CHANGE_TRACKING                     |
                                        DEFAULT_DDL_COLLATION               |
                                        ENABLE_SCHEMA_EVOLUTION             |
                                        CONTACT <purpose>                   |
                                        COMMENT                             |
                                        }
                                        [ , ... ]
```

Copy

Where:

> ```
> clusteringAction ::=
>   {
>      CLUSTER BY ( <expr> [ , <expr> , ... ] )
>      /* RECLUSTER is deprecated */
>    | RECLUSTER [ MAX_SIZE = <budget_in_bytes> ] [ WHERE <condition> ]
>      /* { SUSPEND | RESUME } RECLUSTER is valid action */
>    | { SUSPEND | RESUME } RECLUSTER
>    | DROP CLUSTERING KEY
>   }
> ```
>
> Copy
>
> ```
> tableColumnAction ::=
>   {
>      ADD [ COLUMN ] [ IF NOT EXISTS ] <col_name> <col_type>
>         [
>            {
>               DEFAULT <default_value>
>               | { AUTOINCREMENT | IDENTITY }
>                  /* AUTOINCREMENT (or IDENTITY) is supported only for           */
>                  /* columns with numeric data types (NUMBER, INT, FLOAT, etc.). */
>                  /* Also, if the table is not empty (that is, if the table contains */
>                  /* any rows), only DEFAULT can be altered.                     */
>                  [
>                     {
>                        ( <start_num> , <step_num> )
>                        | START <num> INCREMENT <num>
>                     }
>                  ]
>                  [  { ORDER | NOORDER } ]
>            }
>         ]
>         [ inlineConstraint ]
>         [ COLLATE '<collation_specification>' ]
>
>    | RENAME COLUMN <col_name> TO <new_col_name>
>
>    | ALTER | MODIFY [ ( ]
>                             [ COLUMN ] <col1_name> DROP DEFAULT
>                           , [ COLUMN ] <col1_name> SET DEFAULT <seq_name>.NEXTVAL
>                           , [ COLUMN ] <col1_name> { [ SET ] NOT NULL | DROP NOT NULL }
>                           , [ COLUMN ] <col1_name> [ [ SET DATA ] TYPE ] <type>
>                           , [ COLUMN ] <col1_name> COMMENT '<string>'
>                           , [ COLUMN ] <col1_name> UNSET COMMENT
>                         [ , [ COLUMN ] <col2_name> ... ]
>                         [ , ... ]
>                     [ ) ]
>
>    | DROP [ COLUMN ] [ IF EXISTS ] <col1_name> [, <col2_name> ... ]
>   }
>
>   inlineConstraint ::=
>     [ NOT NULL ]
>     [ CONSTRAINT <constraint_name> ]
>     { UNIQUE | PRIMARY KEY | { [ FOREIGN KEY ] REFERENCES <ref_table_name> [ ( <ref_col_name> ) ] } }
>     [ <constraint_properties> ]
> ```
>
> Copy
>
> For detailed syntax and examples for altering columns, see [ALTER TABLE … ALTER COLUMN](alter-table-column). .
>
> For detailed syntax and examples for creating/altering inline constraints, see [CREATE | ALTER TABLE … CONSTRAINT](create-table-constraint).
>
> ```
> dataMetricFunctionAction ::=
>
>     SET DATA_METRIC_SCHEDULE = {
>         '<num> MINUTE'
>       | 'USING CRON <expr> <time_zone>'
>       | 'TRIGGER_ON_CHANGES'
>     }
>
>   | UNSET DATA_METRIC_SCHEDULE
>
>   | { ADD | DROP } DATA METRIC FUNCTION <metric_name>
>       ON ( <col_name> [ , ... ] [ , TABLE <table_name>( <col_name> [ , ... ] ) ] )
>       [ EXPECTATION <expectation_name> ( <expression> )
>         [, <expectation_name> ( <expression> ) [ , ... ] ] ]
>       [ EXECUTE AS ROLE <role_name> ]
>       [ ANOMALY_DETECTION = { TRUE | FALSE } ]
>       [ SENSITIVITY = { 'LOW' | 'MEDIUM' | 'HIGH' } ]
>       [ , <metric_name_2> ON ( <col_name> [ , ... ] [ , TABLE <table_name>( <col_name> [ , ... ] ) ] ) ]
>         [ EXPECTATION <expectation_name> ( <expression> )
>           [, <expectation_name> ( <expression> ) [ , ... ] ] ]
>         [ EXECUTE AS ROLE <role_name> ]
>         [ ANOMALY_DETECTION = { TRUE | FALSE } ]
>         [ SENSITIVITY = { 'LOW' | 'MEDIUM' | 'HIGH' } ]
>
>   | MODIFY DATA METRIC FUNCTION <metric_name>
>       ON ( <col_name> [ , ... ] [ , TABLE <table_name>( <col_name> [ , ... ] ) ] )
>         { SUSPEND | RESUME }
>       [ , <metric_name_2> ON ( <col_name> [ , ... ] [ , TABLE <table_name>( <col_name> [ , ... ] ) ] )
>         { SUSPEND | RESUME } ]
>
>   | MODIFY DATA METRIC FUNCTION <metric_name>
>       ON ( <col_name> [ , ... ] [ , TABLE <table_name>( <col_name> [ , ... ] ) ] )
>       { ADD | MODIFY } EXPECTATION <expectation_name> ( <expression> )
>           [, <expectation_name> ( <expression> ) [ , ... ] ]
>
>   | MODIFY DATA METRIC FUNCTION <metric_name>
>       ON ( <col_name> [ , ... ] [ , TABLE <table_name>( <col_name> [ , ... ] ) ] )
>       DROP EXPECTATION <expectation_name> [ , <expectation_name> [ , ... ] ]
>
>   | MODIFY DATA METRIC FUNCTION <metric_name>
>       SET <list_of_properties>
> ```
>
> Copy
>
> ```
> dataGovnPolicyTagAction ::=
>   {
>       SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]
>     | UNSET TAG <tag_name> [ , <tag_name> ... ]
>   }
>   |
>   {
>       ADD ROW ACCESS POLICY <policy_name> ON ( <col_name> [ , ... ] )
>     | DROP ROW ACCESS POLICY <policy_name>
>     | DROP ROW ACCESS POLICY <policy_name> ,
>         ADD ROW ACCESS POLICY <policy_name> ON ( <col_name> [ , ... ] )
>     | DROP ALL ROW ACCESS POLICIES
>   }
>   |
>   {
>       SET AGGREGATION POLICY <policy_name>
>         [ ENTITY KEY ( <col_name> [, ... ] ) ]
>         [ FORCE ]
>     | UNSET AGGREGATION POLICY
>   }
>   |
>   {
>       SET JOIN POLICY <policy_name>
>         [ FORCE ]
>     | UNSET JOIN POLICY
>   }
>   |
>   ADD [ COLUMN ] [ IF NOT EXISTS ] <col_name> <col_type>
>     [ [ WITH ] MASKING POLICY <policy_name>
>           [ USING ( <col1_name> , <cond_col_1> , ... ) ] ]
>     [ [ WITH ] PROJECTION POLICY <policy_name> ]
>     [ [ WITH ] TAG ( <tag_name> = '<tag_value>'
>           [ , <tag_name> = '<tag_value>' , ... ] ) ]
>   |
>   {
>     { ALTER | MODIFY } [ COLUMN ] <col1_name>
>         SET MASKING POLICY <policy_name>
>           [ USING ( <col1_name> , <cond_col_1> , ... ) ] [ FORCE ]
>       | UNSET MASKING POLICY
>   }
>   |
>   {
>     { ALTER | MODIFY } [ COLUMN ] <col1_name>
>         SET PROJECTION POLICY <policy_name>
>           [ FORCE ]
>       | UNSET PROJECTION POLICY
>   }
>   |
>   { ALTER | MODIFY } [ COLUMN ] <col1_name> SET TAG
>       <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]
>       , [ COLUMN ] <col2_name> SET TAG
>           <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]
>   |
>   { ALTER | MODIFY } [ COLUMN ] <col1_name> UNSET TAG <tag_name> [ , <tag_name> ... ]
>                    , [ COLUMN ] <col2_name> UNSET TAG <tag_name> [ , <tag_name> ... ]
> ```
>
> Copy
>
> ```
> extTableColumnAction ::=
>   {
>      ADD [ COLUMN ] [ IF NOT EXISTS ] <col_name> <col_type> AS ( <expr> )
>
>    | RENAME COLUMN <col_name> TO <new_col_name>
>
>    | DROP [ COLUMN ] [ IF EXISTS ] <col1_name> [, <col2_name> ... ]
>   }
> ```
>
> Copy
>
> ```
> constraintAction ::=
>   {
>      ADD outoflineConstraint
>    | RENAME CONSTRAINT <constraint_name> TO <new_constraint_name>
>    | { ALTER | MODIFY } { CONSTRAINT <constraint_name> | PRIMARY KEY | UNIQUE | FOREIGN KEY } ( <col_name> [ , ... ] )
>                          [ [ NOT ] ENFORCED ] [ VALIDATE | NOVALIDATE ] [ RELY | NORELY ]
>    | DROP { CONSTRAINT <constraint_name> | PRIMARY KEY | UNIQUE | FOREIGN KEY } ( <col_name> [ , ... ] )
>                          [ CASCADE | RESTRICT ]
>   }
>
>   outoflineConstraint ::=
>     [ CONSTRAINT <constraint_name> ]
>     {
>        UNIQUE [ ( <col_name> [ , <col_name> , ... ] ) ]
>      | PRIMARY KEY [ ( <col_name> [ , <col_name> , ... ] ) ]
>      | [ FOREIGN KEY ] [ ( <col_name> [ , <col_name> , ... ] ) ]
>                           REFERENCES <ref_table_name> [ ( <ref_col_name> [ , <ref_col_name> , ... ] ) ]
>     }
>     [ <constraint_properties> ]
> ```
>
> Copy
>
> For detailed syntax and examples for creating/altering out-of-line constraints, see [CREATE | ALTER TABLE … CONSTRAINT](create-table-constraint).
>
> ```
> searchOptimizationAction ::=
>   {
>      ADD SEARCH OPTIMIZATION [
>        ON <search_method_with_target> [ , <search_method_with_target> ... ]
>      ]
>
>    | DROP SEARCH OPTIMIZATION [
>        ON { <search_method_with_target> | <column_name> | <expression_id> }
>           [ , ... ]
>      ]
>   }
> ```
>
> Copy
>
> For details, see [Search optimization actions (searchOptimizationAction)](#label-alter-table-searchoptimizationaction).

## Parameters[¶](#parameters "Link to this heading")

`name`
:   Identifier for the table to alter. If the identifier contains spaces or special characters, the entire string must be enclosed in double
    quotes. Identifiers enclosed in double quotes are also case sensitive.

`RENAME TO new_table_name`
:   Renames the specified table with a new identifier that is not currently used by any other tables in the schema.

    For more information about table identifiers, see [Identifier requirements](../identifiers-syntax).

    You can move the object to a different database and/or schema while optionally renaming the object. To do so, specify
    a qualified `new_name` value that includes the new database and/or schema name in the form
    `db_name.schema_name.object_name` or `schema_name.object_name`, respectively.

    Note

    * The destination database and/or schema must already exist. In addition, an object with the same name cannot already
      exist in the new location; otherwise, the statement returns an error.
    * Moving an object to a managed access schema is prohibited unless the object owner (that is, the role that has
      the OWNERSHIP privilege on the object) also owns the target schema.

    When an object (table, column, etc.) is renamed, other objects that reference it must be updated with the new name.

`SWAP WITH target_table_name`
:   Swap renames two tables in a single transaction.

    Note that swapping a permanent or transient table with a temporary table, which persists only for the duration of the user session in which
    it was created, is not allowed. This restriction prevents a naming conflict that could occur when a temporary table is swapped with a permanent
    or transient table, and an existing permanent or transient table has the same name as the temporary table. To swap a permanent or transient
    table with a temporary table, use three `ALTER TABLE ... RENAME TO` statements: Rename table `a` to `c`, `b`
    to `a`, and then `c` to `b`.

Note

To rename a table or swap two tables, the role used to perform the operation must have OWNERSHIP privileges on the table or tables. In addition,
renaming a table requires the CREATE TABLE privilege on the schema for the table.

`ADD STORAGE LIFECYCLE POLICY policy_name ON ( col_name [ , col_name ... ] )`
:   Attaches a [storage lifecycle policy](../../user-guide/storage-management/storage-lifecycle-policies) to
    the table.

    For more information about creating and managing storage lifecycle policies, see
    [Create and manage storage lifecycle policies](../../user-guide/storage-management/storage-lifecycle-policies-create-manage).

    Important

    If you attach an archival storage policy to a table, the table is permanently assigned to the specified archive tier for its lifetime. You can’t change the archive tier by applying a new policy. For example, you can’t specify a policy created with a COOL archive tier in ALTER TABLE…DROP STORAGE LIFECYCLE POLICY and then subsequently alter the table to add a policy created with a COLD archive tier. To alter the archive tier for a table, contact Snowflake Support to request deletion of the currently archived data. For additional considerations, see [Archival storage policies](../../user-guide/storage-management/storage-lifecycle-policies.html#label-slp-archive-limitations).

`DROP STORAGE LIFECYCLE POLICY`
:   Removes the storage lifecycle policy from the table.

    For more information, see [Remove a policy from a table](../../user-guide/storage-management/storage-lifecycle-policies-create-manage.html#label-slp-remove-slp).

`SET ...`
:   Specifies one or more properties/parameters to set for the table (separated by blank spaces, commas, or new lines):

    `DATA_RETENTION_TIME_IN_DAYS = integer`
    :   Object-level parameter that modifies the retention period for the table for Time Travel. For more information, see
        [Understanding & using Time Travel](../../user-guide/data-time-travel) and [Working with Temporary and Transient Tables](../../user-guide/tables-temp-transient).

        For a detailed description of this parameter, as well as more information about object parameters, see [Parameters](../parameters).

        Values:

        > * Standard Edition: `0` or `1`
        > * Enterprise Edition:
        >
        >   + `0` to `90` for permanent tables
        >   + `0` or `1` for temporary and transient tables

        Note

        A value of `0` effectively disables Time Travel for the table.

    `MAX_DATA_EXTENSION_TIME_IN_DAYS = integer`
    :   Object parameter that specifies the maximum number of days for which Snowflake can extend the data retention period for the table to
        prevent streams on the table from becoming stale.

        For a detailed description of this parameter, see [MAX\_DATA\_EXTENSION\_TIME\_IN\_DAYS](../parameters.html#label-max-data-extension-time-in-days).

    `CHANGE_TRACKING = TRUE | FALSE`
    :   Specifies to enable or disable change tracking on the table.

        * `TRUE` enables change tracking on the table. This option adds several hidden columns to the source table and begins storing
          change tracking metadata in the columns. These columns consume a small amount of storage.

          The change tracking metadata can be queried using the [CHANGES](../constructs/changes) clause for [SELECT](select)
          statements, or by creating and querying one or more streams on the table.
        * `FALSE` disables change tracking on the table. Associated hidden columns are dropped from the table.

    `DEFAULT_DDL_COLLATION = 'collation_specification'`
    :   Specifies a default [collation specification](../collation.html#label-collation-specification) for any new columns added to the table.

        Setting the parameter does not change the collation specification for any existing columns.

        For more information about the parameter, see [DEFAULT\_DDL\_COLLATION](../parameters.html#label-default-ddl-collation).

    `ENABLE_SCHEMA_EVOLUTION = { TRUE | FALSE }`
    :   Enables or disables automatic changes to the table schema from data loaded into the table from source files, including:

        > * Added columns.
        >
        >   By default, schema evolution is limited to a maximum of 100 added columns per load operation. To request more than 100 added columns per load operation, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).
        > * The NOT NULL constraint can be dropped from any number of columns missing in new data files.

        Setting it to `TRUE` enables automatic table schema evolution. The default `FALSE` disables automatic table schema evolution.

        Note

        Loading data from files evolves the table columns when all of the following are true:

        * The [COPY INTO <table>](copy-into-table) statement includes the `MATCH_BY_COLUMN_NAME` option.
        * The role used to load the data has the EVOLVE SCHEMA or OWNERSHIP privilege on the table.

        Additionally, for schema evolution with CSV, when used with `MATCH_BY_COLUMN_NAME` and `PARSE_HEADER`, `ERROR_ON_COLUMN_COUNT_MISMATCH` must be set to false.

    `CONTACT purpose = contact [ , purpose = contact ... ]`
    :   Associate the existing object with one or more [contacts](../../user-guide/contacts-using).

        You cannot set the CONTACT property with other properties in the same statement.

    `COMMENT = 'string_literal'`
    :   Adds a comment or overwrites the existing comment for the table.

Note

Do not specify copy options using the CREATE STAGE, ALTER STAGE, CREATE TABLE, or ALTER TABLE commands. We recommend that you use the [COPY INTO <table>](copy-into-table) command to specify copy options.

`UNSET ...`
:   Specifies one or more properties/parameters to unset for the table, which resets them back to their defaults:

    * `DATA_RETENTION_TIME_IN_DAYS`
    * `MAX_DATA_EXTENSION_TIME_IN_DAYS`
    * `CHANGE_TRACKING`
    * `DEFAULT_DDL_COLLATION`
    * `ENABLE_SCHEMA_EVOLUTION`
    * `CONTACT purpose`
    * `COMMENT`

    You cannot unset the CONTACT property with other properties in the same statement.

## Clustering actions (`clusteringAction`)[¶](#clustering-actions-clusteringaction "Link to this heading")

`CLUSTER BY ( expr [ , expr , ... ] )`
:   Specifies (or modifies) one or more table columns or column expressions as the clustering key for the table. These are the
    columns/expressions for which clustering is maintained by Automatic Clustering.

    Important

    Clustering keys are not intended or recommended for all tables; they typically benefit very large (that is, multi-terabyte) tables.

    Before you specify a clustering key for a table, please see [Understanding Snowflake Table Structures](../../user-guide/tables-micro-partitions).

`RECLUSTER ...`
:   Deprecated

    Performs manual, incremental reclustering of a table that has a clustering key defined:

    > `MAX_SIZE = budget_in_bytes`
    > :   Deprecated — use a larger warehouse to achieve more effective manual reclustering
    >
    >     Specifies the upper-limit on the amount of data (in bytes) in the table to recluster.
    >
    > `WHERE condition`
    > :   Specifies a condition or range on which to recluster data in the table.

    Note

    Only roles with the OWNERSHIP or INSERT privilege on a table can recluster the table.

`SUSPEND | RESUME RECLUSTER`
:   Enables or disables [Automatic Clustering](../../user-guide/tables-auto-reclustering) for the table.

`DROP CLUSTERING KEY`
:   Drops the clustering key for the table.

For more information about clustering keys and reclustering, see [Understanding Snowflake Table Structures](../../user-guide/tables-micro-partitions).

## Table column actions (`tableColumnAction`)[¶](#table-column-actions-tablecolumnaction "Link to this heading")

`ADD [ COLUMN ] [ IF NOT EXISTS ] col_name col_data_type` . `[ DEFAULT default_value | AUTOINCREMENT ... ]` . `[ inlineConstraint ]` `[ COLLATE 'collation_specification' ]` . `[ [ WITH ] MASKING POLICY policy_name ]` . `[ [ WITH ] PROJECTION POLICY policy_name ]` . `[ [ WITH ] TAG ( tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ] ) ] [ , ...]`
:   Adds a new column. You can specify a default value, an inline constraint, a [collation specification](../collation.html#label-collate-clause),
    a masking policy, and/or one or more tags.

    A default value for a column that you are adding must be a literal value; it cannot be an expression or a value
    returned by a function. For example, the following command returns an expected error:

    ```
    ALTER TABLE t1 ADD COLUMN c5 VARCHAR DEFAULT 12345::VARCHAR;
    ```

    Copy

    ```
    002263 (22000): SQL compilation error:
    Invalid column default expression [CAST(12345 AS VARCHAR(134217728))]
    ```

    When you first create a table, you can use expressions as default values, but not when you add columns.

    The default value for a column must match the data type of the column. An attempt to
    set a default value with a non-matching data type fails with an error. For example:

    ```
    ALTER TABLE t1 ADD COLUMN c6 DATE DEFAULT '20230101';
    ```

    Copy

    ```
    002023 (22000): SQL compilation error:
    Expression type does not match column data type, expecting DATE but got VARCHAR(8) for column C6
    ```

    For additional details about table column actions, see:

    * [CREATE TABLE](create-table)
    * [CREATE | ALTER TABLE … CONSTRAINT](create-table-constraint)
    * [CREATE MASKING POLICY](create-masking-policy)
    * [CREATE TAG](create-tag)

    ADD COLUMN operations can be performed on multiple columns in the same command.

    If you are not sure if the column already exists, you can specify IF NOT EXISTS when adding the column. If the column already
    exists, ADD COLUMN has no effect on the existing column and does not result in an error.

    Note

    You cannot specify IF NOT EXISTS if you are also specifying any of the following for the new column:

    * DEFAULT, AUTOINCREMENT, or IDENTITY
    * UNIQUE, PRIMARY KEY, or FOREIGN KEY

`RENAME COLUMN col_name to new_col_name`
:   Renames the specified column to a new name that is not currently used for any other columns in the table.

    You cannot rename a column that is part of a clustering key.

    When an object (table, column, etc.) is renamed, other objects that reference it must be updated with the new name.

`DROP COLUMN [ IF EXISTS ] col_name [ CASCADE | RESTRICT ]`
:   Removes the specified column from the table.

    If you are not sure if the column already exists, you can specify IF EXISTS when dropping the column. If the column does not
    exist, DROP COLUMN has no effect and does not result in an error.

    Dropping a column is a metadata-only operation. It does not immediately re-write the micro-partition(s) and
    therefore does not immediately free up the space used by the column. Typically, the space within an individual
    micro-partition is freed the next time that the micro-partition is re-written, which is typically when a write is
    done either due to DML (INSERT, UPDATE, DELETE) or re-clustering.

## Data metric function actions (`dataMetricFunctionAction`)[¶](#data-metric-function-actions-datametricfunctionaction "Link to this heading")

`DATA_METRIC_SCHEDULE ...`
:   Specifies the schedule to run the data metric function periodically.

    `'num MINUTE'`
    :   Specifies an interval (in minutes) of wait time inserted between runs of the data metric function. Accepts positive integers only.

        Also supports `num M` syntax.

        For data metric functions, use one of the following values: `5`, `15`, `30`, `60`, `720`, or `1440`.

    `'USING CRON expr time_zone'`
    :   Specifies a cron expression and time zone for periodically running the data metric function. Supports a subset of standard cron utility
        syntax.

        For a list of time zones, see the [list of tz database time zones](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones).

        The cron expression consists of the following fields, and the periodic interval must be at least 5 minutes:

        ```
        # __________ minute (0-59)
        # | ________ hour (0-23)
        # | | ______ day of month (1-31, or L)
        # | | | ____ month (1-12, JAN-DEC)
        # | | | | _ day of week (0-6, SUN-SAT, or L)
        # | | | | |
        # | | | | |
          * * * * *
        ```

        Copy

        The following special characters are supported:

        `*`
        :   Wildcard. Specifies any occurrence of the field.

        `L`
        :   Stands for “last”. When used in the day-of-week field, it allows you to specify constructs such as “the last Friday” (“5L”) of
            a given month. In the day-of-month field, it specifies the last day of the month.

        `/{n}`
        :   Indicates the *nth* instance of a given unit of time. Each quanta of time is computed independently. For example, if `4/3` is
            specified in the month field, then the data metric function is scheduled for April, July and October (i.e. every 3 months, starting
            with the 4th month of the year). The same schedule is maintained in subsequent years. That is, the data metric function is
            not scheduled to run in January (3 months after the October run).

        Note

        * The cron expression currently evaluates against the specified time zone only. Altering the [TIMEZONE](../parameters.html#label-timezone) parameter value
          for the account (or setting the value at the user or session level) does not change the time zone for the data metric
          function.
        * The cron expression defines all valid run times for the data metric function. Snowflake attempts to run a data metric
          function based on this schedule; however, any valid run time is skipped if a previous run has not completed before the next valid
          run time starts.
        * When both a specific day of month and day of week are included in the cron expression, then the data metric function is scheduled
          on days satisfying either the day of month or day of week. For example,
          `DATA_METRIC_SCHEDULE = 'USING CRON 0 0 10-20 * TUE,THU UTC'` schedules a data metric function at 0AM on any 10th to 20th day
          of the month and also on any Tuesday or Thursday outside of those dates.
        * The shortest granularity of time in cron is minutes.

          If a data metric function is resumed during the minute defined in its cron expression, the first scheduled run of the data metric
          function is the next occurrence of the instance of the cron expression. For example, if data metric function scheduled to run daily
          at midnight (`USING CRON 0 0 * * *`) is resumed at midnight plus 5 seconds (`00:00:05`), the first data metric function run
          is scheduled for the following midnight.

    `'TRIGGER_ON_CHANGES'`
    :   Specifies that the DMF runs when a [DML operation](../sql-dml) modifies the table, such as inserting a new row or
        deleting a row.

        You can specify `'TRIGGER_ON_CHANGES'` for the following objects:

        * Dynamic tables
        * External tables
        * Apache Iceberg™ tables
        * Regular tables
        * Temporary tables
        * Transient tables

        You cannot specify `'TRIGGER_ON_CHANGES'` for views.

        Changes to the table as a result of [reclustering](../../user-guide/tables-auto-reclustering) do not trigger the DMF to run.

`{ ADD | DROP } DATA METRIC FUNCTION metric_name`
:   Identifier of the data metric function to add to the table or view or drop from the table or view.

    `ON ( col_name [ , ... ] [ , TABLE( table_name( col_name [ , ... ] ) ) ] )`
    :   The table or view columns on which to associate the data metric function. The data types of the columns must match the data types of
        the columns specified in the data metric function definition.

        If the data metric function accepts a second table as an argument, specify the fully qualified name of the table and its columns.

    `EXPECTATION expectation_name ( expression ) [, expectation_name ( expression ) [ , ... ] ]`
    :   Defines one or more [expectations](../../user-guide/data-quality-expectations) for the association between the column and the DMF.

    `[ , metric_name_2 ON ( col_name [ , ... ] [ , TABLE( table_name( col_name [ , ... ] ) ) ] ) ]`
    :   Additional data metric functions to add to the table or view. Use a comma to separate each data metric function and its specified
        columns.

        If the data metric function accepts a second table as an argument, specify the fully qualified name of the table and its columns.

    `ANOMALY_DETECTION = { TRUE | FALSE }`
    :   [![Snowflake logo in black (no text)](../../_images/logo-snowflake-black.png)](../../_images/logo-snowflake-black.png) [Preview Feature](../../release-notes/preview-features) — Open

        Available to all accounts that are Enterprise Edition (or higher).

        To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

        Specifies whether Snowflake uses the DMF to [automatically detect anomalies](../../user-guide/data-quality-anomaly) in the table.

        Default: `FALSE`

    `SENSITIVITY = { LOW | MEDIUM | HIGH }`
    :   [![Snowflake logo in black (no text)](../../_images/logo-snowflake-black.png)](../../_images/logo-snowflake-black.png) [Preview Feature](../../release-notes/preview-features) — Open

        Available to all accounts that are Enterprise Edition (or higher).

        To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

        Specifies the sensitivity of the anomaly-detecting algorithm. For more information, see [Adjust the sensitivity level of anomaly detection](../../user-guide/data-quality-anomaly.html#label-data-quality-anomaly-sensitivity-level).

        Default: `'MEDIUM'`

    `EXECUTE AS ROLE role_name`
    :   [![Snowflake logo in black (no text)](../../_images/logo-snowflake-black.png)](../../_images/logo-snowflake-black.png) [Preview Feature](../../release-notes/preview-features) — Open

        Available to all accounts that are Enterprise Edition (or higher).

        To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

        Specifies which role the DMF runs with. The role must have the SELECT privilege on the table or view.

        For more information, see [Required privilege on the table or view](../../user-guide/data-quality-access-control.html#label-data-quality-access-control-object-privilege).

`MODIFY DATA METRIC FUNCTION metric_name`
:   Identifier of the data metric function to modify.

    `ON ( col_name [ , ... ] [ , TABLE( table_name( col_name [ , ... ] ) ) ] )`
    :   Specifies the columns associated with the data metric function. If the data metric function accepts a second table as an argument,
        specify the fully qualified name of the table and its columns.

    `{ SUSPEND | RESUME }`
    :   Suspends or resumes the data metric function on the specified columns. When a data metric function is set for a table or view, the data
        metric function is automatically included in the schedule.

        * `SUSPEND` removes the data metric function from the schedule.
        * `RESUME` brings a suspended date metric function back into the schedule.

    `{ ADD | MODIFY } EXPECTATION expectation_name ( expression ) [, expectation_name ( expression ) [ , ... ] ]`
    :   Defines or modifies one or more [expectations](../../user-guide/data-quality-expectations) for the association between the column and
        the DMF.

    `DROP EXPECTATION expectation_name [ , expectation_name [ , ... ] ]`
    :   Removes the specified expectations from the association between the column and the DMF.

    `[ , metric_name_2 ON ( col_name [ , ... ] [ , TABLE(col_name [ , ... ] ) ] ) ]`
    :   Additional data metric functions to modify. Use a comma to separate each data metric function and its specified
        columns. If the data metric function accepts a second table as an argument, specify the fully qualified name of the table and its
        columns.

    `SET list_of_properties`
    :   Sets one or more properties of the association between the DMF and the object. You set more than one property by using a space-delimited list.

        `ANOMALY_DETECTION = { TRUE | FALSE }`
        :   [![Snowflake logo in black (no text)](../../_images/logo-snowflake-black.png)](../../_images/logo-snowflake-black.png) [Preview Feature](../../release-notes/preview-features) — Open

            Available to all accounts that are Enterprise Edition (or higher).

            To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

            Controls whether Snowflake uses the DMF to [automatically detect anomalies](../../user-guide/data-quality-anomaly) in the table.

        `SENSITIVITY = { 'LOW' | 'MEDIUM' | 'HIGH' }`
        :   [![Snowflake logo in black (no text)](../../_images/logo-snowflake-black.png)](../../_images/logo-snowflake-black.png) [Preview Feature](../../release-notes/preview-features) — Open

            Available to all accounts that are Enterprise Edition (or higher).

            To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

            Sets the sensitivity of the anomaly-detecting algorithm. For more information, see [Adjust the sensitivity level of anomaly detection](../../user-guide/data-quality-anomaly.html#label-data-quality-anomaly-sensitivity-level).

        `DATA_QUALITY_NOTIFICATION = { TRUE | FALSE }`
        :   [![Snowflake logo in black (no text)](../../_images/logo-snowflake-black.png)](../../_images/logo-snowflake-black.png) [Preview Feature](../../release-notes/preview-features) — Open

            Available to all accounts that are Enterprise Edition (or higher).

            To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

            Controls whether notifications are sent when the value returned by the DMF is an expectation violation or an anomaly.

            Notifications are sent if the parameter is set to `TRUE` *and* notifications are turned on for the object’s database. Specify `FALSE` to turn off notifications for this object-DMF association even though notifications are sent for other associations in the database.

            For more information about configuring notifications, see [Sending notifications for data quality issues](../../user-guide/data-quality-notifications).

            Default: `TRUE`

## External table column actions (`extTableColumnAction`)[¶](#external-table-column-actions-exttablecolumnaction "Link to this heading")

For all other external table modifications, see [ALTER EXTERNAL TABLE](alter-external-table).

`ADD [ COLUMN ] [ IF NOT EXISTS ] <col_name> <col_type> AS ( <expr> ) [, ...]`
:   Adds a new column to the external table.

    If you are not sure if the column already exists, you can specify IF NOT EXISTS when adding the column. If the column already
    exists, ADD COLUMN has no effect on the existing column and does not result in an error.

    This operation can be performed on multiple columns in the same command.

    `col_name`
    :   String that specifies the column identifier (that is, name). All the requirements for table identifiers also apply to column identifiers.

        For more information, see [Identifier requirements](../identifiers-syntax).

    `col_type`
    :   String (constant) that specifies the data type for the column. The data type must match the result of `expr` for the column.

        For details about the data types that can be specified for table columns, see [SQL data types reference](../../sql-reference-data-types).

    `expr`
    :   String that specifies the expression for the column. When queried, the column returns results derived from this expression.

        External table columns are virtual columns, which are defined using an explicit expression. Add virtual columns as expressions using the
        VALUE column and/or the METADATA$FILENAME pseudocolumn:

        VALUE:
        :   A VARIANT type column that represents a single row in the external file.

            CSV:
            :   The VALUE column structures each row as an object with elements identified by column position (that is,
                `{c1: <column_1_value>, c2: <column_2_value>, c3: <column_1_value> ...}`).

                For example, add a VARCHAR column named `mycol` that references the first column in the staged CSV files:

                ```
                mycol varchar as (value:c1::varchar)
                ```

                Copy

            Semi-structured data:
            :   Enclose element names and values in double-quotes. Traverse the path in the VALUE column using dot notation.

                For example, suppose the following represents a single row of semi-structured data in a staged file:

                ```
                { "a":"1", "b": { "c":"2", "d":"3" } }
                ```

                Copy

                Add a VARCHAR column named `mycol` that references the nested repeating `c` element in the staged file:

                ```
                mycol varchar as (value:"b"."c"::varchar)
                ```

                Copy

        METADATA$FILENAME:
        :   A pseudocolumn that identifies the name of each staged data file included in the external table, including its path in the stage.

`RENAME COLUMN col_name to new_col_name`
:   Renames the specified column to a new name that is not currently used for any other columns in the external table.

`DROP COLUMN [ IF EXISTS ] col_name`
:   Removes the specified column from the external table.

    If you are not sure if the column already exists, you can specify IF EXISTS when dropping the column. If the column does not
    exist, DROP COLUMN has no effect and does not result in an error.

## Constraint actions (`constraintAction`)[¶](#constraint-actions-constraintaction "Link to this heading")

`ADD CONSTRAINT`
:   Adds an out-of-line integrity constraint to one or more columns in the table. To add an inline constraint (for a column), see
    [Column Actions](#label-alter-table-columnaction) (in this topic).

`RENAME CONSTRAINT constraint_name TO new_constraint_name`
:   Renames the specified constraint.

`ALTER | MODIFY CONSTRAINT ...`
:   Alters the properties for the specified constraint.

`DROP CONSTRAINT constraint_name | PRIMARY KEY | UNIQUE | FOREIGN KEY ( col_name [ , ... ] ) [ CASCADE | RESTRICT ]`
:   Drops the specified constraint for the specified column or set of columns.

For detailed syntax and examples for adding or altering constraints, see [CREATE | ALTER TABLE … CONSTRAINT](create-table-constraint).

## Data Governance policy and tag actions (`dataGovnPolicyTagAction`)[¶](#data-governance-policy-and-tag-actions-datagovnpolicytagaction "Link to this heading")

`TAG tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ]`
:   Specifies the [tag](../../user-guide/object-tagging/introduction) name and the tag string value.

    The tag value is always a string, and the maximum number of characters for the tag value is 256.

    For information about specifying tags in a statement, see [Tag quotas](../../user-guide/object-tagging/introduction.html#label-object-tagging-quota).

`policy_name`
:   Identifier for the policy; must be unique for your schema.

The following clauses apply to all table kinds that support row access policies, such as but not limited to tables, views, and event tables.
To simplify, the clauses just refer to “table.”

> `ADD ROW ACCESS POLICY policy_name ON (col_name [ , ... ])`
> :   Adds a row access policy to the table.
>
>     At least one column name must be specified. Additional columns can be specified with a comma separating each column name. Use this
>     expression to add a row access policy to both an event table and an external table.
>
> `DROP ROW ACCESS POLICY policy_name`
> :   Drops a row access policy from the table.
>
>     Use this clause to drop the policy from the table.
>
> `DROP ROW ACCESS POLICY policy_name, ADD ROW ACCESS POLICY policy_name ON ( col_name [ , ... ] )`
> :   Drops the row access policy that is set on the table and adds a row access policy to the same table in a single SQL statement.
>
> `DROP ALL ROW ACCESS POLICIES`
> :   Drops all [row access policy](../../user-guide/security-row-using) associations from the table.
>
>     This expression is helpful when a row access policy is dropped from a schema before dropping the policy from an event table. Use this expression to drop row access policy associations from the table.
>
>     Suppose that a row access policy applied to the table when the backup was created, and the policy was later dropped. After you
>     restore the table from a [backup](../../user-guide/backups), you can’t query it until you run an ALTER TABLE command with the
>     DROP ALL ROW ACCESS POLICIES clause.
>
> `SET AGGREGATION POLICY policy_name`
> :   `[ ENTITY KEY (col_name [ , ... ]) ] [ FORCE ]`
>     :   Assigns an [aggregation policy](../../user-guide/aggregation-policies) to the table.
>
>         Use the optional ENTITY KEY parameter to define which columns uniquely identity an entity within the table. For more information, see
>         [Implementing entity-level privacy with aggregation policies](../../user-guide/aggregation-policies-entity-privacy).
>
>         Use the optional FORCE parameter to atomically replace an existing aggregation policy with the new aggregation policy.
>
> `UNSET AGGREGATION POLICY`
> :   Detaches an aggregation policy from the table.
>
> `SET JOIN POLICY policy_name`
> :   `[ FORCE ]`
>     :   Assigns a [join policy](../../user-guide/join-policies) to the table.
>
>         Use the optional FORCE parameter to atomically replace an existing join policy with the new join policy.
>
> `UNSET JOIN POLICY`
> :   Detaches a join policy from the table.

`{ ALTER | MODIFY } [ COLUMN ] ...`
:   `USING ( col_name , cond_col_1 ... )`
    :   Specifies the arguments to pass into the conditional masking policy SQL expression.

        The first column in the list specifies the column for the policy conditions to mask or tokenize the data and must match the
        column to which the masking policy is set.

        The additional columns specify the columns to evaluate to determine whether to mask or tokenize the data in each row of the query
        result when a query is made on the first column.

        If the USING clause is omitted, Snowflake treats the conditional masking policy as a normal
        [masking policy](../../user-guide/security-column-intro).

    `FORCE`
    :   Replaces a masking or projection policy that is currently set on a column with a different policy in a single statement.

        Note that using the `FORCE` keyword with a masking policy requires the [data type](../../sql-reference-data-types) of the policy
        in the ALTER TABLE statement (i.e. STRING) to match the data type of the masking policy currently set on the column (i.e. STRING).

        If a masking policy is not currently set on the column, specifying this keyword has no effect.

        For details, see: [Replace a masking policy on a column](../../user-guide/security-column-intro.html#label-security-column-intro-replace-policy) or [Replace a projection policy](../../user-guide/projection-policies.html#label-projection-policy-replace).

## Search optimization actions (`searchOptimizationAction`)[¶](#search-optimization-actions-searchoptimizationaction "Link to this heading")

`ADD SEARCH OPTIMIZATION`
:   Adds [search optimization](../../user-guide/search-optimization-service) for the entire table or, if you specify the optional
    ON clause, for specific columns.

    Note

    * Search optimization can be expensive to maintain, especially if the data in the table changes frequently.
      For more information, see [Search optimization cost estimation and management](../../user-guide/search-optimization/cost-estimation.html#label-search-optimization-maintenance-billing).
    * If you try to add search optimization on a materialized view, Snowflake returns an error message.

`ON search_method_with_target [, search_method_with_target ... ]`
:   Specifies that you want to configure search optimization for specific columns or VARIANT fields (instead of the entire table).

    For `search_method_with_target`, use an expression with the following syntax:

    ```
    <search_method>( <target> [ , <target> , ... ] [ , ANALYZER => '<analyzer_name>' ] )
    ```

    Copy

    Where:

    * `search_method` specifies one of the following methods that optimizes queries for a particular type of predicate:

      | Search method | Description |
      | --- | --- |
      | `FULL_TEXT` | Predicates that use VARCHAR (text), VARIANT, ARRAY, and OBJECT types. |
      | `EQUALITY` | Equality and IN predicates. |
      | `SUBSTRING` | Predicates that match substrings and regular expressions (for example, [[ NOT ] LIKE](../functions/like), [[ NOT ] ILIKE](../functions/ilike), [[ NOT ] RLIKE](../functions/rlike), and [REGEXP\_LIKE](../functions/regexp_like)). |
      | `GEO` | Predicates that use GEOGRAPHY types. |
    * `target` specifies the column, VARIANT field, or an asterisk (\*).

      Depending on the value of `search_method`, you can specify a column or VARIANT field of one of the following types:

      | Search method | Supported targets |
      | --- | --- |
      | `FULL_TEXT` | Columns of VARCHAR (text), VARIANT, ARRAY, and OBJECT data types, including paths to fields in VARIANTs. |
      | `EQUALITY` | Columns of numerical, string, binary, and VARIANT data types, including paths to fields in VARIANTs. |
      | `SUBSTRING` | Columns of string or VARIANT data types, including paths to fields in VARIANTs. Specify paths to fields as described above under `EQUALITY`; searches on nested fields are improved in the same way. |
      | `GEO` | Columns of the GEOGRAPHY data type. |

      To specify a VARIANT field, use [dot or bracket notation](../../user-guide/querying-semistructured.html#label-traversing-semistructured-data) (for example,
      `my_column:my_field_name.my_nested_field_name` or `my_column['my_field_name']['my_nested_field_name']`).
      You can also use a colon-delimited path to the field (for example, `my_column:my_field_name:my_nested_field_name`).

      When you specify a VARIANT field, the configuration applies to all nested fields under that field.
      For example, if you specify `ON EQUALITY(src:a.b)`:

      + This configuration can improve queries `on src:a.b` and on any nested fields (for example, `src:a.b.c`, `src:a.b.c.d`,
        etc.).
      + This configuration does not affect queries that do not use the `src:a.b` prefix (for example, `src:a`, `src:z`, etc.).

      To specify all applicable columns in the table as targets, use an asterisk (`*`).

      Note that you cannot specify both an asterisk and specific column names for a given search method. However, you can
      specify an asterisk in different search methods.

      For example, you can specify the following expressions:

      ```
      -- Allowed
      ON SUBSTRING(*)
      ON EQUALITY(*), SUBSTRING(*), GEO(*)
      ```

      Copy

      You cannot specify the following expressions:

      ```
      -- Not allowed
      ON EQUALITY(*, c1)
      ON EQUALITY(c1, *)
      ON EQUALITY(v1:path, *)
      ON EQUALITY(c1), EQUALITY(*)
      ```

      Copy

    * `ANALYZER => 'analyzer_name'` specifies the name of the text analyzer, if `search_method`
      is `FULL_TEXT`.

      When the `FULL_TEXT` search method is used and queries are executed with the
      [SEARCH](../functions/search) or [SEARCH\_IP](../functions/search_ip) function, the analyzer
      breaks the search terms (and the text from the column being searched) into tokens. A row matches if any of
      the tokens extracted from the search string matches a token extracted from any of the columns or fields
      being searched. The analyzer isn’t relevant when the `FULL_TEXT` search method isn’t used or for queries
      that don’t use the SEARCH or SEARCH\_IP function.

      The analyzer tokenizes a string by breaking it where it finds certain delimiters. These delimiters are not
      included in the resulting tokens, and empty tokens are not extracted.

      This parameter accepts one of the following values:

      + DEFAULT\_ANALYZER: Breaks text into tokens based on the following delimiters:

        | Character | Unicode code | Description |
        | --- | --- | --- |
        |  | `U+0020` | Space |
        | `[` | `U+005B` | Left square bracket |
        | `]` | `U+005D` | Right square bracket |
        | `;` | `U+003B` | Semicolon |
        | `<` | `U+003C` | Less-than sign |
        | `>` | `U+003E` | Greater-than sign |
        | `(` | `U+0028` | Left parenthesis |
        | `)` | `U+0029` | Right parenthesis |
        | `{` | `U+007B` | Left curly bracket |
        | `}` | `U+007D` | Right curly bracket |
        | `|` | `U+007C` | Vertical bar |
        | `!` | `U+0021` | Exclamation mark |
        | `,` | `U+002C` | Comma |
        | `'` | `U+0027` | Apostrophe |
        | `"` | `U+0022` | Quotation mark |
        | `*` | `U+002A` | Asterisk |
        | `&` | `U+0026` | Ampersand |
        | `?` | `U+003F` | Question mark |
        | `+` | `U+002B` | Plus sign |
        | `/` | `U+002F` | Slash |
        | `:` | `U+003A` | Colon |
        | `=` | `U+003D` | Equal sign |
        | `@` | `U+0040` | At sign |
        | `.` | `U+002E` | Period (full stop) |
        | `-` | `U+002D` | Hyphen |
        | `$` | `U+0024` | Dollar sign |
        | `%` | `U+0025` | Percent sign |
        | `\` | `U+005C` | Backslash |
        | `_` | `U+005F` | Underscore (low line) |
        | `\n` | `U+000A` | New line (line feed) |
        | `\r` | `U+000D` | Carriage return |
        | `\t` | `U+0009` | Horizontal tab |
      + UNICODE\_ANALYZER: Tokenizes based on Unicode segmentation rules that treat spaces and certain
        punctuation characters as delimiters. These internal rules are designed for natural language searches (in
        many different languages). For example, the default analyzer treats periods in IP addresses and
        apostrophes in contractions as delimiters, but the Unicode analyzer does not.
        See [Using an analyzer to adjust search behavior](../functions/search.html#label-search-function-adjust-search-behavior).

        For more information about the Unicode Text Segmentation algorithm, see <https://unicode.org/reports/tr29/>.
      + NO\_OP\_ANALYZER: Tokenizes neither the data nor the query string. A search term must exactly match the full text
        in a column or field, including case sensitivity; otherwise, the SEARCH function returns FALSE. Even if the query
        string looks like it contains multiple tokens (for example, `'sky blue'`), the column or field must equal the
        entire query string exactly. In this case, only `'sky blue'` is a match; `'sky'` and `'blue'` are not matches.
      + ENTITY\_ANALYZER: Tokenizes the data for IP address searches.

        This analyzer is used only for queries executed with the SEARCH\_IP function.

    To specify more than one search method on a target, use a comma to separate each subsequent method and target:

    ```
    ALTER TABLE t1 ADD SEARCH OPTIMIZATION ON EQUALITY(c1), EQUALITY(c2, c3);
    ```

    Copy

    If you run the ALTER TABLE … ADD SEARCH OPTIMIZATION ON … command multiple times on the same table, each subsequent command
    adds to the existing configuration for the table. For example, suppose that you run the following commands:

    ```
    ALTER TABLE t1 ADD SEARCH OPTIMIZATION ON EQUALITY(c1, c2);
    ALTER TABLE t1 ADD SEARCH OPTIMIZATION ON EQUALITY(c3, c4);
    ```

    Copy

    This adds equality predicates for the columns c1, c2, c3, and c4 to the configuration for the table. This is equivalent to
    running the command:

    ```
    ALTER TABLE t1 ADD SEARCH OPTIMIZATION ON EQUALITY(c1, c2, c3, c4);
    ```

    Copy

    For examples, see [Enabling search optimization for specific columns](../../user-guide/search-optimization/enabling.html#label-search-optimization-service-configuration-adding).

`DROP SEARCH OPTIMIZATION`
:   Removes [search optimization](../../user-guide/search-optimization-service) for the entire table or, if you specify the
    optional ON clause, from specific columns.

    Note

    * If a table has the search optimization property, then dropping the table and undropping it preserves the
      search optimization property.
    * Removing the search optimization property from a table and then adding it back incurs the same cost as adding it the first
      time.

`ON search_method_with_target | column_name | expression_id [ , ... ]`
:   Specifies that you want to drop the search optimization configuration for specific columns or VARIANT fields (instead of
    dropping search optimization for the entire table).

    To identify the column configuration to drop, specify one of the following:

    * For `search_method_with_target`, specify a method for optimizing queries for one or more specific targets, which can
      be columns or VARIANT fields. Use the
      [syntax described earlier](alter-table-event-table.html#label-alter-table-searchoptimizationaction-search-method-target).
    * For `column_name`, specify the name of the column configured for search optimization. Specifying the column name drops
      all expressions for that column, including expressions that use VARIANT fields in the column.
    * For `expression_id`, specify the ID for an expression listed in the output of the
      [DESCRIBE SEARCH OPTIMIZATION](../../user-guide/search-optimization/enabling.html#label-search-optimization-service-configuration-displaying) command.

    To specify more than one of these, use a comma between items.

    You can specify any combination of search methods with targets, column names, and expression IDs.

    For examples, see [Dropping search optimization for specific columns](../../user-guide/search-optimization/enabling.html#label-search-optimization-service-configuration-dropping).

## Usage notes: General[¶](#usage-notes-general "Link to this heading")

* Changes to a table are not automatically propagated to views created on that table. For example, if you drop a
  column in a table, and a view is defined to include that column, the view becomes invalid; the view is not
  adjusted to remove the column.

* Dropping a column does not immediately free up the column’s storage space.

  + The space in each micro-partition is not reclaimed until that micro-partition is re-written. Write
    operations (insert, update, delete, etc.) on 1 or more rows in that micro-partition cause the micro-partition to
    be re-written. If you want to force space to be reclaimed, you can follow these steps:

    1. Use a [CREATE TABLE AS SELECT (CTAS)](create-table) statement to create a new table that contains
       only the columns of the old table you want to keep.
    2. Set the [DATA\_RETENTION\_TIME\_IN\_DAYS](../parameters.html#label-data-retention-time-in-days) parameter to `0` for the old table (optional).
    3. Drop the old table.
  + If the table is protected by the Time Travel feature, the space used by the Time Travel storage is not reclaimed
    until the Time Travel retention period expires.
* If a new column with a default value is added to a table with existing rows, all of the existing rows are populated with the default value.
* Adding a new column with a default value containing a function is not currently supported. The following error is returned:

  > `Invalid column default expression (expr)`
* To alter a table, you must be using a role that has ownership privilege on the table.
* To add clustering to a table, you must also have USAGE or OWNERSHIP privileges on the schema and database that
  contain the table.

* For masking policies:

  + The `USING` clause and the `FORCE` keyword are both optional; neither are required to set a masking policy on a column. The
    `USING` clause and the `FORCE` keyword can be used separately or together. For details, see:

    - [Apply a conditional masking policy on a column](../../user-guide/security-column-intro.html#label-security-column-intro-apply-cond-cols)
    - [Replace a masking policy on a column](../../user-guide/security-column-intro.html#label-security-column-intro-replace-policy)
  + A single masking policy that uses conditional columns can be applied to multiple tables provided that the column structure of the table
    matches the columns specified in the policy.
  + When modifying one or more table columns with a masking policy or the table itself with a row access policy, use the
    [POLICY\_CONTEXT](../functions/policy_context) function to simulate a query on the column(s) protected by a masking policy and the
    table protected by a row access policy.

* For row access policies:

  + Snowflake supports adding and dropping row access policies in a single SQL statement.

    For example, to replace a row access policy that is already set on a table with a different policy, drop the row access policy first
    and then add the new row access policy.
  + For a given resource (i.e. table or view), to `ADD` or `DROP` a row access policy you must have either the
    [APPLY ROW ACCESS POLICY](../../user-guide/security-row-intro.html#label-security-row-privileges) privilege on the schema, or the
    [OWNERSHIP](../../user-guide/security-row-intro.html#label-security-row-privileges) privilege on the resource and the APPLY privilege on the row access policy resource.
  + A table or view can only be protected by one row access policy at a time. Adding a policy fails if the policy body refers to a table or
    view column that is protected by a row access policy or the column protected by a masking policy.

    Similarly, adding a masking policy to a table column fails if the masking policy body refers to a table that is protected by a row
    access policy or another masking policy.
  + Row access policies cannot be applied to system views or table functions.
  + Similar to other [DROP <object>](drop) operations, Snowflake returns an error if attempting to drop a row access policy from a
    resource that does not have a row access policy added to it.
  + If an object has both a row access policy and one or more masking policies, the row access policy is evaluated first.

* When you attach a [storage lifecycle policy](../../user-guide/storage-management/storage-lifecycle-policies) to a table by
  using the ADD STORAGE LIFECYCLE POLICY option:

  + You must have the necessary privileges to apply the policy. For information about required privileges, see
    [Storage lifecycle policy privileges](../../user-guide/security-access-control-privileges.html#label-security-access-control-slp-privileges).
  + A table can have only one attached storage lifecycle policy.
  + The number of columns must match the argument count in the policy function signature, and the column data must be compatible with the argument types.
  + Associated policies aren’t affected if you rename table columns. Snowflake associates policies to tables by using the column IDs.
  + In order to evaluate and apply storage lifecycle policy expressions, Snowflake internally and temporarily bypasses any governance policies on a table.

* If you create a foreign key, the columns in the REFERENCES clause must be listed in the same order as they were
  listed for the primary key. For example:

  ```
  CREATE TABLE parent ... CONSTRAINT primary_key_1 PRIMARY KEY (c_1, c_2) ...
  CREATE TABLE child  ... CONSTRAINT foreign_key_1 FOREIGN KEY (...) REFERENCES parent (c_1, c_2) ...
  ```

  Copy

  In both cases, the order of the columns is `c_1, c_2`. If the order of the columns in the foreign key had been different
  (for example, `c_2, c_1`), the attempt to create the foreign key would have failed.

* Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](../metadata).
* ALTER TABLE … CHANGE\_TRACKING = TRUE

  > + When a table is altered to enable change tracking, the table is locked for the duration of the operation.
  >   Locks can cause latency with some associated DDL/DML operations.
  >   For more information, refer to [Resource locking](../transactions.html#label-txn-locking).
* Indexes in hybrid tables:

  > + When you use the ALTER TABLE command to add or drop a UNIQUE or
  >   FOREIGN KEY constraint in a hybrid table, the corresponding index is
  >   also created or dropped. For more information about hybrid
  >   table indexes, see [CREATE INDEX](create-index).
  > + FOREIGN KEY constraints are supported only across hybrid tables that are
  >   stored in the same database. You cannot move a hybrid table from
  >   one database to another. The PRIMARY KEY, UNIQUE, and
  >   FOREIGN KEY constraints defined on hybrid tables have their RELY
  >   property marked as `TRUE`.
  > + A column that is used by an index cannot be dropped before the
  >   corresponding index is dropped.
* The only operation that you can perform on an [interactive table](../../user-guide/interactive)
  using ALTER TABLE is to rename that table.

## Usage notes: Data metric functions[¶](#usage-notes-data-metric-functions "Link to this heading")

Add a DMF to a table:
:   Prior to adding a data metric function to a table, you must:

    * Set the schedule for the data metric function to run. For details, see
      [DATA\_METRIC\_SCHEDULE](../parameters.html#label-data-metric-schedule).
    * Configure the event table to store the results of calling the data metric function. For details, see
      [View results of a data metric function](../../user-guide/data-quality-results).
    * Ensure that the table is view is not granted to a share because you cannot set a data metric function on a shared table or view.

    Additionally:

    * When you specify a column, Snowflake uses the ordinal position. If you rename a column after adding a data metric function to the table
      or view, the association of the data metric function to the column remains valid.
    * Only one data metric function of its kind can be added to a column. For example, a NULL\_COUNT data metric function cannot be added to a
      single column twice.
    * If you drop a column after adding a data metric function that references the column, Snowflake cannot evaluate the data metric function.
    * Referencing a virtual column is not supported.

Schedule a DMF
:   It takes ten minutes for the schedule to become effective once the schedule is set.

    Similarly, it takes ten minutes once the DMF is unset for the scheduling changes to take effect. For more information, see
    [Schedule the DMF to run](../../user-guide/data-quality-working.html#label-data-quality-schedule).

## Examples[¶](#examples "Link to this heading")

The following sections provide examples of using the ALTER COLUMN command:

* [Renaming a table](#label-alter-table-examples-rename)
* [Swapping tables](#label-alter-table-examples-swap)
* [Adding columns](#label-alter-table-examples-columns-adding)
* [Renaming columns](#label-alter-table-examples-columns-renaming)
* [Dropping columns](#label-alter-table-examples-columns-dropping)
* [Adding, renaming, and dropping columns in an external table](#label-alter-table-examples-columns-external)
* [Changing the order of clustering keys](#label-alter-table-examples-clustering-keys)
* [Adding and dropping row access policies](#label-alter-table-examples-row-access-policies)

### Renaming a table[¶](#renaming-a-table "Link to this heading")

The following creates a table named `t1`:

```
CREATE OR REPLACE TABLE t1(a1 number);
```

Copy

```
SHOW TABLES LIKE 't1';
```

Copy

```
+-------------------------------+------+---------------+-------------+-------+---------+------------+------+-------+--------+----------------+-----------------+-------------+-------------------------+-----------------+----------+--------+
| created_on                    | name | database_name | schema_name | kind  | comment | cluster_by | rows | bytes | owner  | retention_time | change_tracking | is_external | enable_schema_evolution | owner_role_type | is_event | budget |
|-------------------------------+------+---------------+-------------+-------+---------+------------+------+-------+--------+----------------+-----------------+-------------+-------------------------+-----------------+----------+--------|
| 2023-10-19 10:37:04.858 -0700 | T1   | TESTDB        | MY_SCHEMA   | TABLE |         |            |    0 |     0 | PUBLIC | 1              | OFF             | N           | N                       | ROLE            | N        | NULL   |
+-------------------------------+------+---------------+-------------+-------+---------+------------+------+-------+--------+----------------+-----------------+-------------+-------------------------+-----------------+----------+--------+
```

The following statement changes the name of the table to `tt1`:

```
ALTER TABLE t1 RENAME TO tt1;
```

Copy

```
SHOW TABLES LIKE 'tt1';
```

Copy

```
+-------------------------------+------+---------------+-------------+-------+---------+------------+------+-------+--------+----------------+-----------------+-------------+-------------------------+-----------------+----------+--------+
| created_on                    | name | database_name | schema_name | kind  | comment | cluster_by | rows | bytes | owner  | retention_time | change_tracking | is_external | enable_schema_evolution | owner_role_type | is_event | budget |
|-------------------------------+------+---------------+-------------+-------+---------+------------+------+-------+--------+----------------+-----------------+-------------+-------------------------+-----------------+----------+--------|
| 2023-10-19 10:37:04.858 -0700 | TT1  | TESTDB        | MY_SCHEMA   | TABLE |         |            |    0 |     0 | PUBLIC | 1              | OFF             | N           | N                       | ROLE            | N        | NULL   |
+-------------------------------+------+---------------+-------------+-------+---------+------------+------+-------+--------+----------------+-----------------+-------------+-------------------------+-----------------+----------+--------+
```

### Swapping tables[¶](#swapping-tables "Link to this heading")

The following statements create tables named `t1` and `t2`:

```
CREATE OR REPLACE TABLE t1(a1 NUMBER, a2 VARCHAR, a3 DATE);
CREATE OR REPLACE TABLE t2(b1 VARCHAR);
```

Copy

```
DESC TABLE t1;
```

Copy

```
+------+-------------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+
| name | type              | kind   | null? | default | primary key | unique key | check | expression | comment | policy name |
|------+-------------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------|
| A1   | NUMBER(38,0)      | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        |
| A2   | VARCHAR(16777216) | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        |
| A3   | DATE              | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        |
+------+-------------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+
```

```
DESC TABLE t2;
```

Copy

```
+------+-------------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+
| name | type              | kind   | null? | default | primary key | unique key | check | expression | comment | policy name |
|------+-------------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------|
| B1   | VARCHAR(16777216) | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        |
+------+-------------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+
```

The following statement swaps table `t1` with table `t2`:

```
ALTER TABLE t1 SWAP WITH t2;
```

Copy

```
DESC TABLE t1;
```

Copy

```
+------+-------------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+
| name | type              | kind   | null? | default | primary key | unique key | check | expression | comment | policy name |
|------+-------------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------|
| B1   | VARCHAR(16777216) | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        |
+------+-------------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+
```

```
DESC TABLE t2;
```

Copy

```
+------+-------------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+
| name | type              | kind   | null? | default | primary key | unique key | check | expression | comment | policy name |
|------+-------------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------|
| A1   | NUMBER(38,0)      | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        |
| A2   | VARCHAR(16777216) | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        |
| A3   | DATE              | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        |
+------+-------------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+
```

### Adding columns[¶](#adding-columns "Link to this heading")

The following creates a table named `t1`:

```
CREATE OR REPLACE TABLE t1(a1 NUMBER);
```

Copy

```
DESC TABLE t1;
```

Copy

```
+------+--------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+
| name | type         | kind   | null? | default | primary key | unique key | check | expression | comment | policy name |
|------+--------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------|
| A1   | NUMBER(38,0) | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        |
+------+--------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+
```

The following statement adds a column named `a2` to this table:

```
ALTER TABLE t1 ADD COLUMN a2 NUMBER;
```

Copy

The following statement adds a column named `a3` with a NOT NULL constraint:

```
ALTER TABLE t1 ADD COLUMN a3 NUMBER NOT NULL;
```

Copy

The following statement adds a column named `a4` with a default value and a NOT NULL constraint:

```
ALTER TABLE t1 ADD COLUMN a4 NUMBER DEFAULT 0 NOT NULL;
```

Copy

The following statement adds a VARCHAR column named `a5` with a language-specific
[collation specification](../collation.html#label-collate-clause):

```
ALTER TABLE t1 ADD COLUMN a5 VARCHAR COLLATE 'en_US';
```

Copy

```
DESC TABLE t1;
```

Copy

```
+------+-----------------------------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+
| name | type                              | kind   | null? | default | primary key | unique key | check | expression | comment | policy name |
|------+-----------------------------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------|
| A1   | NUMBER(38,0)                      | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        |
| A2   | NUMBER(38,0)                      | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        |
| A3   | NUMBER(38,0)                      | COLUMN | N     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        |
| A4   | NUMBER(38,0)                      | COLUMN | N     | 0       | N           | N          | NULL  | NULL       | NULL    | NULL        |
| A5   | VARCHAR(16777216) COLLATE 'en_us' | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        |
+------+-----------------------------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+
```

The following statement uses the IF NOT EXISTS clause to add a column named `a2` only if the column does not exist. There is
an existing column named `a2`. Specifying the IF NOT EXISTS clause prevents the statement from failing with an error.

```
ALTER TABLE t1 ADD COLUMN IF NOT EXISTS a2 NUMBER;
```

Copy

As shown in the output of the [DESCRIBE TABLE](desc-table) command, the statement above has no effect on the existing column named `a2`:

```
DESC TABLE t1;
```

Copy

```
+------+-----------------------------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+
| name | type                              | kind   | null? | default | primary key | unique key | check | expression | comment | policy name |
|------+-----------------------------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------|
| A1   | NUMBER(38,0)                      | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        |
| A2   | NUMBER(38,0)                      | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        |
| A3   | NUMBER(38,0)                      | COLUMN | N     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        |
| A4   | NUMBER(38,0)                      | COLUMN | N     | 0       | N           | N          | NULL  | NULL       | NULL    | NULL        |
| A5   | VARCHAR(16777216) COLLATE 'en_us' | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        |
+------+-----------------------------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+
```

### Renaming columns[¶](#renaming-columns "Link to this heading")

The following statement changes the name of the column `a1` to `b1`:

```
ALTER TABLE t1 RENAME COLUMN a1 TO b1;
```

Copy

```
DESC TABLE t1;
```

Copy

```
+------+--------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+
| name | type         | kind   | null? | default | primary key | unique key | check | expression | comment | policy name |
|------+--------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------|
| B1   | NUMBER(38,0) | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        |
| A2   | NUMBER(38,0) | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        |
| A3   | NUMBER(38,0) | COLUMN | N     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        |
| A4   | NUMBER(38,0) | COLUMN | N     | 0       | N           | N          | NULL  | NULL       | NULL    | NULL        |
+------+--------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+
```

### Dropping columns[¶](#dropping-columns "Link to this heading")

The following statement drops the column `a2`:

```
ALTER TABLE t1 DROP COLUMN a2;
```

Copy

```
DESC TABLE t1;
```

Copy

```
+------+--------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+
| name | type         | kind   | null? | default | primary key | unique key | check | expression | comment | policy name |
|------+--------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------|
| B1   | NUMBER(38,0) | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        |
| A3   | NUMBER(38,0) | COLUMN | N     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        |
| A4   | NUMBER(38,0) | COLUMN | N     | 0       | N           | N          | NULL  | NULL       | NULL    | NULL        |
+------+--------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+
```

The following statement uses the IF EXISTS clause to drop a column named `a2` only if the column exists. There is no existing
column named `a2`. Specifying the IF EXISTS clause prevents the statement from failing with an error.

```
ALTER TABLE t1 DROP COLUMN IF EXISTS a2;
```

Copy

As shown in the output of the [DESCRIBE TABLE](desc-table) command, the statement above has no effect on the existing table:

```
+------+--------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+
| name | type         | kind   | null? | default | primary key | unique key | check | expression | comment | policy name |
|------+--------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------|
| B1   | NUMBER(38,0) | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        |
| A3   | NUMBER(38,0) | COLUMN | N     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        |
| A4   | NUMBER(38,0) | COLUMN | N     | 0       | N           | N          | NULL  | NULL       | NULL    | NULL        |
+------+--------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+
```

Copy

### Adding, renaming, and dropping columns in an external table[¶](#adding-renaming-and-dropping-columns-in-an-external-table "Link to this heading")

The following statement creates an external table named `exttable1`:

```
CREATE EXTERNAL TABLE exttable1
  LOCATION=@mystage/logs/
  AUTO_REFRESH = true
  FILE_FORMAT = (TYPE = PARQUET)
  ;
```

Copy

```
DESC EXTERNAL TABLE exttable1;
```

Copy

```
+-----------+-------------------+-----------+-------+---------+-------------+------------+-------+----------------------------------------------------------+-----------------------+
| name      | type              | kind      | null? | default | primary key | unique key | check | expression                                               | comment               |
|-----------+-------------------+-----------+-------+---------+-------------+------------+-------+----------------------------------------------------------+-----------------------|
| VALUE     | VARIANT           | COLUMN    | Y     | NULL    | N           | N          | NULL  | NULL                                                     | The value of this row |
+-----------+-------------------+-----------+-------+---------+-------------+------------+-------+----------------------------------------------------------+-----------------------+
```

The following statement adds a new column named `a1` to the external table:

```
ALTER TABLE exttable1 ADD COLUMN a1 VARCHAR AS (value:a1::VARCHAR);
```

Copy

```
DESC EXTERNAL TABLE exttable1;
```

Copy

```
+-----------+-------------------+-----------+-------+---------+-------------+------------+-------+----------------------------------------------------------+-----------------------+
| name      | type              | kind      | null? | default | primary key | unique key | check | expression                                               | comment               |
|-----------+-------------------+-----------+-------+---------+-------------+------------+-------+----------------------------------------------------------+-----------------------|
| VALUE     | VARIANT           | COLUMN    | Y     | NULL    | N           | N          | NULL  | NULL                                                     | The value of this row |
| A1        | VARCHAR(16777216) | VIRTUAL   | Y     | NULL    | N           | N          | NULL  | TO_CHAR(GET(VALUE, 'a1'))                                | NULL                  |
+-----------+-------------------+-----------+-------+---------+-------------+------------+-------+----------------------------------------------------------+-----------------------+
```

The following statement changes the name of the `a1` column to `b1`:

```
ALTER TABLE exttable1 RENAME COLUMN a1 TO b1;
```

Copy

```
DESC EXTERNAL TABLE exttable1;
```

Copy

```
+-----------+-------------------+-----------+-------+---------+-------------+------------+-------+----------------------------------------------------------+-----------------------+
| name      | type              | kind      | null? | default | primary key | unique key | check | expression                                               | comment               |
|-----------+-------------------+-----------+-------+---------+-------------+------------+-------+----------------------------------------------------------+-----------------------|
| VALUE     | VARIANT           | COLUMN    | Y     | NULL    | N           | N          | NULL  | NULL                                                     | The value of this row |
| B1        | VARCHAR(16777216) | VIRTUAL   | Y     | NULL    | N           | N          | NULL  | TO_CHAR(GET(VALUE, 'a1'))                                | NULL                  |
+-----------+-------------------+-----------+-------+---------+-------------+------------+-------+----------------------------------------------------------+-----------------------+
```

The following statement drops the column named `b1`:

```
ALTER TABLE exttable1 DROP COLUMN b1;
```

Copy

```
DESC EXTERNAL TABLE exttable1;
```

Copy

```
+-----------+-------------------+-----------+-------+---------+-------------+------------+-------+----------------------------------------------------------+-----------------------+
| name      | type              | kind      | null? | default | primary key | unique key | check | expression                                               | comment               |
|-----------+-------------------+-----------+-------+---------+-------------+------------+-------+----------------------------------------------------------+-----------------------|
| VALUE     | VARIANT           | COLUMN    | Y     | NULL    | N           | N          | NULL  | NULL                                                     | The value of this row |
+-----------+-------------------+-----------+-------+---------+-------------+------------+-------+----------------------------------------------------------+-----------------------+
```

### Changing the order of clustering keys[¶](#changing-the-order-of-clustering-keys "Link to this heading")

The following statement creates a table named `t1` that clusters by the `id` and `date` columns:

```
CREATE OR REPLACE TABLE T1 (id NUMBER, date TIMESTAMP_NTZ, name STRING) CLUSTER BY (id, date);
```

Copy

```
SHOW TABLES LIKE 'T1';
```

Copy

```
---------------------------------+------+---------------+-------------+-------+---------+------------+------+-------+--------------+----------------+
           created_on            | name | database_name | schema_name | kind  | comment | cluster_by | rows | bytes |    owner     | retention_time |
---------------------------------+------+---------------+-------------+-------+---------+------------+------+-------+--------------+----------------+
 Tue, 21 Jun 2016 15:42:12 -0700 | T1   | TESTDB        | TESTSCHEMA  | TABLE |         | (ID,DATE)  | 0    | 0     | ACCOUNTADMIN | 1              |
---------------------------------+------+---------------+-------------+-------+---------+------------+------+-------+--------------+----------------+
```

The following statement changes the order of the clustering key:

```
ALTER TABLE t1 CLUSTER BY (date, id);
```

Copy

```
SHOW TABLES LIKE 'T1';
```

Copy

```
---------------------------------+------+---------------+-------------+-------+---------+------------+------+-------+--------------+----------------+
           created_on            | name | database_name | schema_name | kind  | comment | cluster_by | rows | bytes |    owner     | retention_time |
---------------------------------+------+---------------+-------------+-------+---------+------------+------+-------+--------------+----------------+
 Tue, 21 Jun 2016 15:42:12 -0700 | T1   | TESTDB        | TESTSCHEMA  | TABLE |         | (DATE,ID)  | 0    | 0     | ACCOUNTADMIN | 1              |
---------------------------------+------+---------------+-------------+-------+---------+------------+------+-------+--------------+----------------+
```

### Adding and dropping row access policies[¶](#adding-and-dropping-row-access-policies "Link to this heading")

The following example adds a row access policy on a table while specifying a single column. After setting the policy, you can verify by checking
the [information schema](../../user-guide/security-row-intro.html#label-security-row-policy-refs).

```
ALTER TABLE t1 ADD ROW ACCESS POLICY rap_t1 ON (empl_id);
```

Copy

The following example adds a row access policy while specifying two columns in a single table.

```
ALTER TABLE t1 ADD ROW ACCESS POLICY rap_test2 ON (cost, item);
```

Copy

The following example drops a row access policy from a table. Verify the policies were dropped by querying the
[information schema](../../user-guide/security-row-intro.html#label-security-row-policy-refs).

```
ALTER TABLE t1 DROP ROW ACCESS POLICY rap_v1;
```

Copy

The following example shows how to combine adding and dropping row access policies in a single SQL statement for a table. Verify the
results by checking the [information schema](../../user-guide/security-row-intro.html#label-security-row-policy-refs).

> ```
> alter table t1
>   drop row access policy rap_t1_version_1,
>   add row access policy rap_t1_version_2 on (empl_id);
> ```
>
> Copy

### Schedule for a data metric function to run[¶](#schedule-for-a-data-metric-function-to-run "Link to this heading")

Set the data metric function schedule to run every 5 minutes:

> ```
> ALTER TABLE hr.tables.empl_info SET
>   DATA_METRIC_SCHEDULE = '5 MINUTE';
> ```
>
> Copy

Set the data metric function schedule to run at 8:00 AM daily:

> ```
> ALTER TABLE hr.tables.empl_info SET
>   DATA_METRIC_SCHEDULE = 'USING CRON 0 8 * * * UTC';
> ```
>
> Copy

Set the data metric function schedule to run at 8:00 AM on weekdays only:

> ```
> ALTER TABLE hr.tables.empl_info SET
>   DATA_METRIC_SCHEDULE = 'USING CRON 0 8 * * MON,TUE,WED,THU,FRI UTC';
> ```
>
> Copy

Set the data metric function schedule to run three times daily at 0600, 1200, and 1800 UTC:

> ```
> ALTER TABLE hr.tables.empl_info SET
>   DATA_METRIC_SCHEDULE = 'USING CRON 0 6,12,18 * * * UTC';
> ```
>
> Copy

Set the data metric function to run when a general DML operation, such as inserting a new row, modifies the table:

> ```
> ALTER TABLE hr.tables.empl_info SET
>   DATA_METRIC_SCHEDULE = 'TRIGGER_ON_CHANGES';
> ```
>
> Copy

### Apply a join policy on a table[¶](#apply-a-join-policy-on-a-table "Link to this heading")

Alter a table to apply a [join policy](../../user-guide/join-policies) with an allowed joining column:

```
ALTER TABLE join_table_2
  SET JOIN POLICY jp1 ALLOWED JOIN KEYS (col1);
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
2. [Parameters](#parameters)
3. [Clustering actions (clusteringAction)](#clustering-actions-clusteringaction)
4. [Table column actions (tableColumnAction)](#table-column-actions-tablecolumnaction)
5. [Data metric function actions (dataMetricFunctionAction)](#data-metric-function-actions-datametricfunctionaction)
6. [External table column actions (extTableColumnAction)](#external-table-column-actions-exttablecolumnaction)
7. [Constraint actions (constraintAction)](#constraint-actions-constraintaction)
8. [Data Governance policy and tag actions (dataGovnPolicyTagAction)](#data-governance-policy-and-tag-actions-datagovnpolicytagaction)
9. [Search optimization actions (searchOptimizationAction)](#search-optimization-actions-searchoptimizationaction)
10. [Usage notes: General](#usage-notes-general)
11. [Usage notes: Data metric functions](#usage-notes-data-metric-functions)
12. [Examples](#examples)