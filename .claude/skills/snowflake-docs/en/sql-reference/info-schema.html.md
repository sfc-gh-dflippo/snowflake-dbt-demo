---
auto_generated: true
description: The Snowflake Information Schema (aka “Data Dictionary”) consists of
  a set of system-defined views and table functions that provide extensive metadata
  information about the objects created in your acc
last_scraped: '2026-01-14T16:55:33.987341+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/info-schema.html
title: Snowflake Information Schema | Snowflake Documentation
---

1. [Overview](../reference.md)
2. [SQL data types reference](../sql-reference-data-types.md)
3. [SQL command reference](../sql-reference-commands.md)
4. [Function and stored procedure reference](../sql-reference-functions.md)
5. [Class reference](../sql-reference-classes.md)
6. [Scripting reference](../sql-reference-snowflake-scripting.md)
7. [General reference](../sql-reference.md)

   * [Parameters](parameters.md)
   * [References](references.md)
   * [Ternary logic](ternary-logic.md)
   * [Collation support](collation.md)
   * [SQL format models](sql-format-models.md)
   * [Object identifiers](identifiers.md)
   * [Constraints](constraints.md)
   * [SQL variables](session-variables.md)
   * [Bind variables](bind-variables.md)
   * [Transactions](transactions.md)
   * [Table literals](literals-table.md)
   * [SNOWFLAKE database](snowflake-db.md)
   * [Snowflake Information Schema](info-schema.md)

     + [APPLICABLE\_ROLES](info-schema/applicable_roles.md)
     + [APPLICATION\_SPECIFICATIONS](info-schema/application_specifications.md)
     + [BACKUP\_POLICIES](info-schema/backup_policies.md)
     + [BACKUP\_SETS](info-schema/backup_sets.md)
     + [BACKUPS](info-schema/backups.md)
     + [CLASS\_INSTANCE\_FUNCTIONS](info-schema/class_instance_functions.md)
     + [CLASS\_INSTANCE\_PROCEDURES](info-schema/class_instance_procedures.md)
     + [CLASS\_INSTANCES](info-schema/class_instances.md)
     + [CLASSES](info-schema/classes.md)
     + [COLUMNS](info-schema/columns.md)
     + [CORTEX\_SEARCH\_SERVICES](info-schema/cortex_search.md)
     + [CORTEX\_SEARCH\_SERVICE\_SCORING\_PROFILES](info-schema/cortex_search_service_scoring_profiles.md)
     + [CURRENT\_PACKAGES\_POLICY](info-schema/current_packages_policy.md)
     + [DATABASES](info-schema/databases.md)
     + [ELEMENT\_TYPES](info-schema/element_types.md)
     + [ENABLED\_ROLES](info-schema/enabled_roles.md)
     + [EVENT\_TABLES](info-schema/event_tables.md)
     + [EXTERNAL\_TABLES](info-schema/external_tables.md)
     + [FIELDS](info-schema/fields.md)
     + [FILE\_FORMATS](info-schema/file_formats.md)
     + [FUNCTIONS](info-schema/functions.md)
     + [HYBRID\_TABLES](info-schema/hybrid_tables.md)
     + [INDEXES](info-schema/indexes.md)
     + [INDEX\_COLUMNS](info-schema/index_columns.md)
     + [INFORMATION\_SCHEMA\_CATALOG\_NAME](info-schema/information_schema_catalog_name.md)
     + [LOAD\_HISTORY](info-schema/load_history.md)
     + [MODEL\_VERSIONS](info-schema/model_versions.md)
     + [OBJECT\_PRIVILEGES](info-schema/object_privileges.md)
     + [PACKAGES](info-schema/packages.md)
     + [PIPES](info-schema/pipes.md)
     + [PROCEDURES](info-schema/procedures.md)
     + [REFERENTIAL\_CONSTRAINTS](info-schema/referential_constraints.md)
     + [REPLICATION\_DATABASES](info-schema/replication_databases.md)
     + [REPLICATION\_GROUPS](info-schema/replication_groups.md)
     + [SCHEMATA](info-schema/schemata.md)
     + [SEMANTIC\_DIMENSIONS](info-schema/semantic_dimensions.md)
     + [SEMANTIC\_FACTS](info-schema/semantic_facts.md)
     + [SEMANTIC\_METRICS](info-schema/semantic_metrics.md)
     + [SEMANTIC\_RELATIONSHIPS](info-schema/semantic_relationships.md)
     + [SEMANTIC\_TABLES](info-schema/semantic_tables.md)
     + [SEMANTIC\_VIEWS](info-schema/semantic_views.md)
     + [SEQUENCES](info-schema/sequences.md)
     + [SERVICES](info-schema/services.md)
     + [SNAPSHOT\_POLICIES — Deprecated](info-schema/snapshot_policies.md)
     + [SNAPSHOT\_SETS — Deprecated](info-schema/snapshot_sets.md)
     + [SNAPSHOTS — Deprecated](info-schema/snapshots.md)
     + [STAGES](info-schema/stages.md)
     + [TABLE\_CONSTRAINTS](info-schema/table_constraints.md)
     + [TABLE\_PRIVILEGES](info-schema/table_privileges.md)
     + [TABLE\_STORAGE\_METRICS](info-schema/table_storage_metrics.md)
     + [TABLES](info-schema/tables.md)
     + [USAGE\_PRIVILEGES](info-schema/usage_privileges.md)
     + [VIEWS](info-schema/views.md)
   * [Metadata fields](metadata.md)
   * [Conventions](conventions.md)
   * [Reserved keywords](reserved-keywords.md)
8. [API reference](../api-reference.md)

[Reference](../reference.md)[General reference](../sql-reference.md)Snowflake Information Schema

# Snowflake Information Schema[¶](#snowflake-information-schema "Link to this heading")

The Snowflake Information Schema (aka “Data Dictionary”) consists of a set of system-defined views and table functions that provide
extensive metadata information about the objects created in your account. The Snowflake Information Schema is based on the SQL-92 ANSI
Information Schema, but with the addition of views and functions that are specific to Snowflake.

The Information Schema is implemented as a schema named INFORMATION\_SCHEMA that Snowflake automatically creates in every database in
an account.

Note

ANSI uses the term “catalog” to refer to databases. To maintain compatibility with the standard, the Snowflake Information Schema
topics use “catalog” in place of “database” where applicable. For all intents and purposes, the terms are conceptually equivalent
and interchangeable.

## What is INFORMATION\_SCHEMA?[¶](#what-is-information-schema "Link to this heading")

Each database created in your account automatically includes a built-in, read-only schema named INFORMATION\_SCHEMA. The schema contains
the following objects:

* Views for all the objects contained in the database, as well as views for account-level objects (i.e. non-database objects such as
  roles, warehouses, and databases)
* Table functions for historical and usage data across your account.

## List of Information Schema views[¶](#list-of-information-schema-views "Link to this heading")

The views in INFORMATION\_SCHEMA display metadata about objects defined in the database, as well as metadata for non-database,
account-level objects that are common across all databases. Each instance of INFORMATION\_SCHEMA includes:

> * ANSI-standard views for the database and account-level objects that are relevant to Snowflake.
> * Snowflake-specific views for the non-standard objects that Snowflake supports (stages, file formats, etc.).

Information Schema views that are Snowflake-specific (that is, that are **not** ANSI-standard) are marked with ✔ in
the “Snowflake-specific” column in the following table.

| View | Type | Snowflake-specific | Notes |
| --- | --- | --- | --- |
| [APPLICABLE\_ROLES](info-schema/applicable_roles) | Account |  |  |
| [APPLICATION\_SPECIFICATIONS](info-schema/application_specifications) | Database | ✔ |  |
| [CLASS\_INSTANCE\_FUNCTIONS](info-schema/class_instance_functions) | Database | ✔ |  |
| [CLASS\_INSTANCE\_PROCEDURES](info-schema/class_instance_procedures) | Database | ✔ |  |
| [CLASS\_INSTANCES](info-schema/class_instances) | Database | ✔ |  |
| [CLASSES](info-schema/classes) | Database | ✔ |  |
| [COLUMNS](info-schema/columns) | Database |  |  |
| [CORTEX\_SEARCH\_SERVICE](info-schema/cortex_search) | Database | ✔ |  |
| [CORTEX\_SEARCH\_SERVICE\_SCORING\_PROFILES](info-schema/cortex_search_service_scoring_profiles) | Database | ✔ |  |
| [CURRENT\_PACKAGES\_POLICY](info-schema/current_packages_policy) | Database | ✔ |  |
| [DATABASES](info-schema/databases) | Account | ✔ |  |
| [ELEMENT\_TYPES](info-schema/element_types) | Database |  |  |
| [ENABLED\_ROLES](info-schema/enabled_roles) | Account |  |  |
| [EVENT\_TABLES](info-schema/event_tables) | Database | ✔ |  |
| [EXTERNAL\_TABLES](info-schema/external_tables) | Database | ✔ |  |
| [FIELDS](info-schema/fields) | Database |  |  |
| [FILE FORMATS](info-schema/file_formats) | Database | ✔ |  |
| [FUNCTIONS](info-schema/functions) | Database |  |  |
| [HYBRID\_TABLES](info-schema/hybrid_tables) | Database | ✔ |  |
| [INDEXES](info-schema/indexes) | Database | ✔ |  |
| [INDEX\_COLUMNS](info-schema/index_columns) | Database | ✔ |  |
| [INFORMATION\_SCHEMA\_CATALOG\_NAME](info-schema/information_schema_catalog_name) | Account |  |  |
| [LOAD\_HISTORY](info-schema/load_history) | Account | ✔ | Data retained for 14 days. |
| [MODEL\_VERSIONS](info-schema/model_versions) | Database | ✔ |  |
| [OBJECT\_PRIVILEGES](info-schema/object_privileges) | Account |  |  |
| [PACKAGES](info-schema/packages) | Database | ✔ |  |
| [PIPES](info-schema/pipes) | Database | ✔ |  |
| [PROCEDURES](info-schema/procedures) | Database | ✔ |  |
| [REFERENTIAL\_CONSTRAINTS](info-schema/referential_constraints) | Database |  |  |
| [REPLICATION\_DATABASES](info-schema/replication_databases) | Account | ✔ |  |
| [REPLICATION\_GROUPS](info-schema/replication_groups) | Account | ✔ |  |
| [SCHEMATA](info-schema/schemata) | Database |  |  |
| [SEMANTIC\_DIMENSIONS](info-schema/semantic_dimensions) | Database | ✔ |  |
| [SEMANTIC\_FACTS](info-schema/semantic_facts) | Database | ✔ |  |
| [SEMANTIC\_METRICS](info-schema/semantic_metrics) | Database | ✔ |  |
| [SEMANTIC\_RELATIONSHIPS](info-schema/semantic_relationships) | Database | ✔ |  |
| [SEMANTIC\_TABLES](info-schema/semantic_tables) | Database | ✔ |  |
| [SEMANTIC\_VIEW](info-schema/semantic_views) | Database | ✔ |  |
| [SEQUENCES](info-schema/sequences) | Database |  |  |
| [SERVICES](info-schema/services) | Database | ✔ |  |
| [STAGES](info-schema/stages) | Database | ✔ |  |
| [TABLE\_CONSTRAINTS](info-schema/table_constraints) | Database |  |  |
| [TABLE\_PRIVILEGES](info-schema/table_privileges) | Database |  |  |
| [TABLE\_STORAGE\_METRICS](info-schema/table_storage_metrics) | Database | ✔ |  |
| [TABLES](info-schema/tables) | Database |  | Displays tables and views. |
| [USAGE\_PRIVILEGES](info-schema/usage_privileges) | Database |  | Displays privileges on sequences only; to view privileges on other types of objects, use OBJECT\_PRIVILEGES. |
| [VIEWS](info-schema/views) | Database |  |  |

## List of Information Schema table functions[¶](#list-of-information-schema-table-functions "Link to this heading")

The table functions in INFORMATION\_SCHEMA can be used to return account-level usage and historical information for storage, warehouses,
user logins, and queries:

| Table Function | Data Retention | Notes |
| --- | --- | --- |
| [ALERT\_HISTORY](functions/alert_history) | 14 days | Results depend on MONITOR USAGE privilege. [1] |
| [AUTOMATIC\_CLUSTERING\_HISTORY](functions/automatic_clustering_history) | 14 days | Results depend on MONITOR USAGE privilege. [1] |
| [AUTO\_REFRESH\_REGISTRATION\_HISTORY](functions/auto_refresh_registration_history) | 14 days | Results depend on MONITOR USAGE privilege. [1] |
| [AVAILABLE\_LISTING\_REFRESH\_HISTORY](functions/available_listing_refresh_history) | 14 days | Results are only returned for consumers of listings who have any privilege on the available listing or mounted database. |
| [COMPLETE\_TASK\_GRAPHS](functions/complete_task_graphs) | 60 minutes | Results returned only for the ACCOUNTADMIN role, the task owner (i.e. the role with the OWNERSHIP privilege on the task), or a role with the global MONITOR EXECUTION privilege. |
| [COPY\_HISTORY](functions/copy_history) | 14 days | Results depend on the privileges assigned to the user’s current role. |
| [CURRENT\_TASK\_GRAPHS](functions/current_task_graphs) | N/A | Results returned only for the ACCOUNTADMIN role, the task owner (i.e. the role with the OWNERSHIP privilege on the task), or a role with the global MONITOR EXECUTION privilege. |
| [DATA\_METRIC\_FUNCTION\_REFERENCES](functions/data_metric_function_references) | N/A | Results depend on the privileges or database role assigned to the user’s current role. |
| [DATA\_TRANSFER\_HISTORY](functions/data_transfer_history) | 14 days | Results depend on MONITOR USAGE privilege. [1] |
| [DATABASE\_REFRESH\_HISTORY](functions/database_refresh_history) | 14 days | Results depend on the privileges assigned to the user’s current role. |
| [DATABASE\_REFRESH\_PROGRESS , DATABASE\_REFRESH\_PROGRESS\_BY\_JOB](functions/database_refresh_progress) | 14 days | Results depend on the privileges assigned to the user’s current role. |
| [DATABASE\_REPLICATION\_USAGE\_HISTORY](functions/database_replication_usage_history) | 14 days | Results returned only for the ACCOUNTADMIN role. |
| [DATABASE\_STORAGE\_USAGE\_HISTORY](functions/database_storage_usage_history) | 6 months | Results depend on MONITOR USAGE privilege. [1] |
| [DBT\_PROJECT\_EXECUTION\_HISTORY](functions/dbt_project_execution_history). | 7 days. | Results depend on MONITOR, OWNERSHIP, or USAGE privilege. |
| [DYNAMIC\_TABLES](functions/dynamic_tables) | 7 days | Results depend on the privileges assigned to the user’s current role. For more information, see [Dynamic table access control](../user-guide/dynamic-tables-privileges). [1] |
| [DYNAMIC\_TABLE\_GRAPH\_HISTORY](functions/dynamic_table_graph_history) | 7 days | Results depend on the privileges assigned to the user’s current role. For more information, see [Dynamic table access control](../user-guide/dynamic-tables-privileges). [1] |
| [DYNAMIC\_TABLE\_REFRESH\_HISTORY](functions/dynamic_table_refresh_history) | 7 days | Results depend on the privileges assigned to the user’s current role. For more information, see [Dynamic table access control](../user-guide/dynamic-tables-privileges). [1] |
| [EXTERNAL\_FUNCTIONS\_HISTORY](functions/external_functions_history) | 14 days | Results depend on MONITOR USAGE privilege. [1] |
| [EXTERNAL\_TABLE\_FILES](functions/external_table_files) | N/A | Results depend on the privileges assigned to the user’s current role. |
| [EXTERNAL\_TABLE\_FILE\_REGISTRATION\_HISTORY](functions/external_table_registration_history) | 30 days | Results depend on the privileges assigned to the user’s current role. |
| [ICEBERG\_TABLE\_FILES](functions/iceberg_table_files) | Varies | Results depend on the value of the [DATA\_RETENTION\_TIME\_IN\_DAYS](parameters.html#label-data-retention-time-in-days) parameter set for the table. For more information, see [Metadata and retention for Apache Iceberg™ tables](../user-guide/tables-iceberg-metadata). |
| [ICEBERG\_TABLE\_SNAPSHOT\_REFRESH\_HISTORY](functions/iceberg_table_snapshot_refresh_history) | Varies | Results depend on the value of the [DATA\_RETENTION\_TIME\_IN\_DAYS](parameters.html#label-data-retention-time-in-days) parameter set for the table. For more information, see [Metadata and retention for Apache Iceberg™ tables](../user-guide/tables-iceberg-metadata). |
| [LISTING\_REFRESH\_HISTORY](functions/listing_refresh_history) | 14 days | Results are only returned for a role with any privilege on Listing Auto-Fulfillment. |
| [LOGIN\_HISTORY , LOGIN\_HISTORY\_BY\_USER](functions/login_history) | 7 days | Results depend on the privileges assigned to the user’s current role. |
| [MATERIALIZED\_VIEW\_REFRESH\_HISTORY](functions/materialized_view_refresh_history) | 14 days | Results depend on MONITOR USAGE privilege. [1] |
| [NOTIFICATION\_HISTORY](functions/notification_history) | 14 days | Results returned only for the ACCOUNTADMIN role, the integration owner (i.e. the role with the OWNERSHIP privilege on the integration) or a role with the USAGE privilege on the integration. |
| [ONLINE\_FEATURE\_TABLE\_REFRESH\_HISTORY](functions/online-feature-table-refresh-history) | 7 days | Results depend on the privileges assigned to the user’s current role. |
| [PIPE\_USAGE\_HISTORY](functions/pipe_usage_history) | 14 days | Results depend on MONITOR USAGE privilege. [1] |
| [POLICY\_REFERENCES](functions/policy_references) | N/A | Results returned only for the ACCOUNTADMIN role. |
| [QUERY\_ACCELERATION\_HISTORY](functions/query_acceleration_history) | 14 days | Results depend on MONITOR USAGE privilege. [1] |
| [QUERY\_HISTORY , QUERY\_HISTORY\_BY\_\*](functions/query_history) | 7 days | Results depend on the privileges assigned to the user’s current role. |
| [REPLICATION\_GROUP\_DANGLING\_REFERENCES](functions/replication_group_dangling_references) | N/A |  |
| [REPLICATION\_GROUP\_REFRESH\_HISTORY, REPLICATION\_GROUP\_REFRESH\_HISTORY\_ALL](functions/replication_group_refresh_history) | 14 days | Results are only returned for a role with any privilege on the replication or failover group. |
| [REPLICATION\_GROUP\_REFRESH\_PROGRESS, REPLICATION\_GROUP\_REFRESH\_PROGRESS\_BY\_JOB, REPLICATION\_GROUP\_REFRESH\_PROGRESS\_ALL](functions/replication_group_refresh_progress) | 14 days | Results are only returned for a role with any privilege on the replication or failover group. |
| [REPLICATION\_GROUP\_USAGE\_HISTORY](functions/replication_group_usage_history) | 14 days | Results depend on the MONITOR USAGE privilege. [1] |
| [REPLICATION\_USAGE\_HISTORY](functions/replication_usage_history) | 14 days | Results returned only for the ACCOUNTADMIN role. |
| [REST\_EVENT\_HISTORY](functions/rest_event_history) | 7 days | Results returned only for the ACCOUNTADMIN role. |
| [SEARCH\_OPTIMIZATION\_HISTORY](functions/search_optimization_history) | 14 days | Results depend on MONITOR USAGE privilege. [1] |
| [SERVERLESS\_ALERT\_HISTORY](functions/serverless_alert_history) | 14 days | Results depend on MONITOR USAGE privilege. [1] |
| [SERVERLESS\_TASK\_HISTORY](functions/serverless_task_history) | 14 days | Results depend on MONITOR USAGE privilege. [1] |
| [STAGE\_DIRECTORY\_FILE\_REGISTRATION\_HISTORY](functions/stage_directory_file_registration_history) | 14 days | Results depend on the privileges assigned to the user’s current role. |
| [STAGE\_STORAGE\_USAGE\_HISTORY](functions/stage_storage_usage_history) | 6 months | Results depend on MONITOR USAGE privilege. [1] |
| [STORAGE\_LIFECYCLE\_POLICY\_HISTORY](functions/storage_lifecycle_policy_history) | 14 days | Results depend on the privileges assigned to the user’s current role. |
| [TAG\_REFERENCES](functions/tag_references) | N/A | Results are only returned for the role that has access to the specified object. |
| [TAG\_REFERENCES\_ALL\_COLUMNS](functions/tag_references_all_columns) | N/A | Results are only returned for the role that has access to the specified object. |
| [TASK\_DEPENDENTS](functions/task_dependents) | N/A | Results returned only for the ACCOUNTADMIN role or task owner (role with OWNERSHIP privilege on task). |
| [TASK\_HISTORY](functions/task_history) | 7 days | Results returned only for the ACCOUNTADMIN role, the task owner (i.e. the role with the OWNERSHIP privilege on the task), or a role with the global MONITOR EXECUTION privilege. |
| [VALIDATE\_PIPE\_LOAD](functions/validate_pipe_load) | 14 days | Results depend on the privileges assigned to the user’s current role. |
| [WAREHOUSE\_LOAD\_HISTORY](functions/warehouse_load_history) | 14 days | Results depend on MONITOR USAGE privilege. [1] |
| [WAREHOUSE\_METERING\_HISTORY](functions/warehouse_metering_history) | 6 months | Results depend on MONITOR USAGE privilege. [1] |

[1] Returns results if role has been assigned the MONITOR USAGE global privilege; otherwise, returns results only for the ACCOUNTADMIN role.

## General usage notes[¶](#general-usage-notes "Link to this heading")

* Each INFORMATION\_SCHEMA schema is read-only (i.e. the schema, and all the views and table functions in the schema, cannot be modified
  or dropped).
* Queries on INFORMATION\_SCHEMA views do not guarantee consistency with respect to concurrent DDL. For example, if a set of tables are
  created while a long-running INFORMATION\_SCHEMA query is being executed, the result of the query may include some, none, or all of
  the tables created.
* The output of a view or table function depend on the privileges granted to the user’s current role. When querying an INFORMATION\_SCHEMA
  view or table function, only objects for which the current role has been granted access privileges are returned.
* To prevent performance issues, the following error is returned if the filters specified in an INFORMATION\_SCHEMA query are not
  sufficiently selective:

  > `Information schema query returned too much data. Please repeat query with more selective predicates.`
* The Snowflake-specific views are subject to change. Avoid selecting all columns from these views. Instead, select the columns that you want.
  For example, if you want the `name` column, use `SELECT name`, rather than `SELECT *`.

Tip

The Information Schema views are optimized for queries that retrieve a small subset of objects from the dictionary. Whenever possible,
maximize the performance of your queries by filtering on schema and object names.

For more usage information and details, see the
[Snowflake Information Schema blog post](https://www.snowflake.com/blog/using-snowflake-information-schema/).

## Considerations for replacing SHOW commands with Information Schema views[¶](#considerations-for-replacing-show-commands-with-information-schema-views "Link to this heading")

The INFORMATION\_SCHEMA views provide a SQL interface to the same information provided by the [SHOW <objects>](sql/show) commands.
You can use the views to replace these commands; however, there are some key differences to consider before switching:

| Considerations | SHOW Commands | Information Schema Views |
| --- | --- | --- |
| Warehouses | Not required to execute. | Warehouse must be running and currently in use to query the views. |
| Pattern matching/filtering | Case-insensitive (when filtering using LIKE). | Standard (case-sensitive) SQL semantics. Snowflake automatically converts unquoted, case-insensitive identifiers to uppercase internally, so unquoted object names must be queried in uppercase in the Information Schema views. |
| Query results | Most SHOW commands limit results to the current schema by default. | Views display all objects in the current/specified database. To query against a particular schema, you must use a filter predicate (e.g. `... WHERE table_schema = CURRENT_SCHEMA()...`). Note that Information Schema queries lacking sufficiently selective filters return an error and do not execute (see [General Usage Notes](#general-usage-notes) in this topic). |

## Qualifying the names of Information Schema views and table functions in queries[¶](#qualifying-the-names-of-information-schema-views-and-table-functions-in-queries "Link to this heading")

When querying an INFORMATION\_SCHEMA view or table function, you must use the qualified name of the view/table function or the
INFORMATION\_SCHEMA schema must be in use for the session.

For example:

* To query using the fully-qualified names of the view and table function, in the form of `database.information_schema.name`:

  ```
  SELECT table_name, comment FROM testdb.INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'PUBLIC' ... ;

  SELECT event_timestamp, user_name FROM TABLE(testdb.INFORMATION_SCHEMA.LOGIN_HISTORY( ... ));
  ```

  Copy
* To query using the qualified names of the view and table function, in the form of `information_schema.name`:

  ```
  USE DATABASE testdb;

  SELECT table_name, comment FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'PUBLIC' ... ;

  SELECT event_timestamp, user_name FROM TABLE(INFORMATION_SCHEMA.LOGIN_HISTORY( ... ));
  ```

  Copy
* To query with the INFORMATION\_SCHEMA schema in use for the session:

  ```
  USE SCHEMA testdb.INFORMATION_SCHEMA;

  SELECT table_name, comment FROM TABLES WHERE TABLE_SCHEMA = 'PUBLIC' ... ;

  SELECT event_timestamp, user_name FROM TABLE(LOGIN_HISTORY( ... ));
  ```

  Copy

  Note

  If you are using a database that was created from a share and you have selected INFORMATION\_SCHEMA as the current schema for the
  session, the SELECT statement might fail with the following error:

  INFORMATION\_SCHEMA does not exist or is not authorized

  If this occurs, select a different schema for the current schema for the session.

For more detailed examples, see the reference documentation for each view/table function.

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

1. [What is INFORMATION\_SCHEMA?](#what-is-information-schema)
2. [List of Information Schema views](#list-of-information-schema-views)
3. [List of Information Schema table functions](#list-of-information-schema-table-functions)
4. [General usage notes](#general-usage-notes)
5. [Considerations for replacing SHOW commands with Information Schema views](#considerations-for-replacing-show-commands-with-information-schema-views)
6. [Qualifying the names of Information Schema views and table functions in queries](#qualifying-the-names-of-information-schema-views-and-table-functions-in-queries)

Related content

1. [Account Usage](/sql-reference/account-usage)