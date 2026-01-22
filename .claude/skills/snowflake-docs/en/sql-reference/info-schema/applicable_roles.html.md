---
auto_generated: true
description: This Information Schema view displays one row for each role grant applied
  to the currently authenticated user.
last_scraped: '2026-01-14T16:55:55.700736+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/info-schema/applicable_roles.html
title: APPLICABLE_ROLES view | Snowflake Documentation
---

1. [Overview](../../reference.md)
2. [SQL data types reference](../../sql-reference-data-types.md)
3. [SQL command reference](../../sql-reference-commands.md)
4. [Function and stored procedure reference](../../sql-reference-functions.md)
5. [Class reference](../../sql-reference-classes.md)
6. [Scripting reference](../../sql-reference-snowflake-scripting.md)
7. [General reference](../../sql-reference.md)

   * [Parameters](../parameters.md)
   * [References](../references.md)
   * [Ternary logic](../ternary-logic.md)
   * [Collation support](../collation.md)
   * [SQL format models](../sql-format-models.md)
   * [Object identifiers](../identifiers.md)
   * [Constraints](../constraints.md)
   * [SQL variables](../session-variables.md)
   * [Bind variables](../bind-variables.md)
   * [Transactions](../transactions.md)
   * [Table literals](../literals-table.md)
   * [SNOWFLAKE database](../snowflake-db.md)
   * [Snowflake Information Schema](../info-schema.md)

     + [APPLICABLE\_ROLES](applicable_roles.md)
     + [APPLICATION\_SPECIFICATIONS](application_specifications.md)
     + [BACKUP\_POLICIES](backup_policies.md)
     + [BACKUP\_SETS](backup_sets.md)
     + [BACKUPS](backups.md)
     + [CLASS\_INSTANCE\_FUNCTIONS](class_instance_functions.md)
     + [CLASS\_INSTANCE\_PROCEDURES](class_instance_procedures.md)
     + [CLASS\_INSTANCES](class_instances.md)
     + [CLASSES](classes.md)
     + [COLUMNS](columns.md)
     + [CORTEX\_SEARCH\_SERVICES](cortex_search.md)
     + [CORTEX\_SEARCH\_SERVICE\_SCORING\_PROFILES](cortex_search_service_scoring_profiles.md)
     + [CURRENT\_PACKAGES\_POLICY](current_packages_policy.md)
     + [DATABASES](databases.md)
     + [ELEMENT\_TYPES](element_types.md)
     + [ENABLED\_ROLES](enabled_roles.md)
     + [EVENT\_TABLES](event_tables.md)
     + [EXTERNAL\_TABLES](external_tables.md)
     + [FIELDS](fields.md)
     + [FILE\_FORMATS](file_formats.md)
     + [FUNCTIONS](functions.md)
     + [HYBRID\_TABLES](hybrid_tables.md)
     + [INDEXES](indexes.md)
     + [INDEX\_COLUMNS](index_columns.md)
     + [INFORMATION\_SCHEMA\_CATALOG\_NAME](information_schema_catalog_name.md)
     + [LOAD\_HISTORY](load_history.md)
     + [MODEL\_VERSIONS](model_versions.md)
     + [OBJECT\_PRIVILEGES](object_privileges.md)
     + [PACKAGES](packages.md)
     + [PIPES](pipes.md)
     + [PROCEDURES](procedures.md)
     + [REFERENTIAL\_CONSTRAINTS](referential_constraints.md)
     + [REPLICATION\_DATABASES](replication_databases.md)
     + [REPLICATION\_GROUPS](replication_groups.md)
     + [SCHEMATA](schemata.md)
     + [SEMANTIC\_DIMENSIONS](semantic_dimensions.md)
     + [SEMANTIC\_FACTS](semantic_facts.md)
     + [SEMANTIC\_METRICS](semantic_metrics.md)
     + [SEMANTIC\_RELATIONSHIPS](semantic_relationships.md)
     + [SEMANTIC\_TABLES](semantic_tables.md)
     + [SEMANTIC\_VIEWS](semantic_views.md)
     + [SEQUENCES](sequences.md)
     + [SERVICES](services.md)
     + [SNAPSHOT\_POLICIES — Deprecated](snapshot_policies.md)
     + [SNAPSHOT\_SETS — Deprecated](snapshot_sets.md)
     + [SNAPSHOTS — Deprecated](snapshots.md)
     + [STAGES](stages.md)
     + [TABLE\_CONSTRAINTS](table_constraints.md)
     + [TABLE\_PRIVILEGES](table_privileges.md)
     + [TABLE\_STORAGE\_METRICS](table_storage_metrics.md)
     + [TABLES](tables.md)
     + [USAGE\_PRIVILEGES](usage_privileges.md)
     + [VIEWS](views.md)
   * [Metadata fields](../metadata.md)
   * [Conventions](../conventions.md)
   * [Reserved keywords](../reserved-keywords.md)
8. [API reference](../../api-reference.md)

[Reference](../../reference.md)[General reference](../../sql-reference.md)[Snowflake Information Schema](../info-schema.md)APPLICABLE\_ROLES

# APPLICABLE\_ROLES view[¶](#applicable-roles-view "Link to this heading")

This Information Schema view displays one row for each role grant applied to the currently authenticated user.

For more information about roles and grants, see [Overview of Access Control](../../user-guide/security-access-control-overview).

See also:
:   [ENABLED\_ROLES view](enabled_roles) , [OBJECT\_PRIVILEGES view](object_privileges) , [TABLE\_PRIVILEGES view](table_privileges) , [GRANTS\_TO\_USERS view](../account-usage/grants_to_users) ,
    [GRANTS\_TO\_ROLES view](../account-usage/grants_to_roles) , [SHOW GRANTS](../sql/show-grants)

## Columns[¶](#columns "Link to this heading")

| Column Name | Data Type | Description |
| --- | --- | --- |
| GRANTEE | VARCHAR | Role or user to whom the privilege is granted |
| ROLE\_NAME | VARCHAR | Name of the role |
| ROLE\_OWNER | VARCHAR | Owner of the role |
| IS\_GRANTABLE | VARCHAR | Whether this role can be granted to others |

## Usage notes[¶](#usage-notes "Link to this heading")

The view does not display any information about [database roles](../../user-guide/security-access-control-considerations.html#label-access-control-considerations-database-roles).

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

1. [Columns](#columns)
2. [Usage notes](#usage-notes)