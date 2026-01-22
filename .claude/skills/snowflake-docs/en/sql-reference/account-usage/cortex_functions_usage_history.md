---
auto_generated: true
description: ACCOUNT_USAGE
last_scraped: '2026-01-14T16:56:01.950705+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/account-usage/cortex_functions_usage_history
title: CORTEX_FUNCTIONS_USAGE_HISTORY view | Snowflake Documentation
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

     + [Account Usage](../account-usage.md)

       - [ACCESS\_HISTORY](access_history.md)
       - [AGGREGATE\_ACCESS\_HISTORY](aggregate_access_history.md)
       - [AGGREGATE\_QUERY\_HISTORY](aggregate_query_history.md)
       - [AGGREGATION\_POLICIES](aggregation_policies.md)
       - [ALERT\_HISTORY](alert_history.md)
       - [ANOMALIES\_DAILY](anomalies_daily.md)
       - [APPLICATION\_DAILY\_USAGE\_HISTORY](application_daily_usage_history.md)
       - [APPLICATION\_SPECIFICATION\_STATUS\_HISTORY](application_specification_status_history.md)
       - [APPLICATION\_SPECIFICATIONS](application_specifications.md)
       - [ARCHIVE\_STORAGE\_DATA\_RETRIEVAL\_USAGE\_HISTORY](archive_storage_data_retrieval_usage_history.md)
       - [AUTOMATIC\_CLUSTERING\_HISTORY](automatic_clustering_history.md)
       - [BACKUP\_OPERATION\_HISTORY](backup_operation_history.md)
       - [BACKUP\_POLICIES](backup_policies.md)
       - [BACKUP\_SETS](backup_sets.md)
       - [BACKUP\_STORAGE\_USAGE](backup_storage_usage.md)
       - [BACKUPS](backups.md)
       - [BLOCK\_STORAGE\_HISTORY](block_storage_history.md)
       - [BLOCK\_STORAGE\_SNAPSHOTS](block_storage_snapshots.md)
       - [CATALOG\_LINKED\_DATABASE\_USAGE\_HISTORY](catalog_linked_database_usage_history.md)
       - [CLASS\_INSTANCES](class_instances.md)
       - [CLASSES](classes.md)
       - [COLUMNS](columns.md)
       - [COLUMN\_QUERY\_PRUNING\_HISTORY](column_query_pruning_history.md)
       - [COMPLETE\_TASK\_GRAPHS](complete_task_graphs.md)
       - [COMPUTE\_POOLS](compute_pools.md)
       - [CONTACT\_REFERENCES](contact_references.md)
       - [CONTACTS](contacts.md)
       - [COPY\_FILES\_HISTORY](copy_files_history.md)
       - [COPY\_HISTORY](copy_history.md)
       - [CORTEX\_AISQL\_USAGE\_HISTORY](cortex_aisql_usage_history.md)
       - [CORTEX\_ANALYST\_USAGE\_HISTORY](cortex_analyst_usage_history.md)
       - [CORTEX\_DOCUMENT\_PROCESSING\_USAGE\_HISTORY](cortex_document_processing_usage_history.md)
       - [CORTEX\_FINE\_TUNING\_USAGE\_HISTORY](cortex_fine_tuning_usage_history.md)
       - [CORTEX\_FUNCTIONS\_QUERY\_USAGE\_HISTORY](cortex_functions_query_usage_history.md)
       - [CORTEX\_FUNCTIONS\_USAGE\_HISTORY](cortex_functions_usage_history.md)
       - [CORTEX\_PROVISIONED\_THROUGHPUT\_USAGE\_HISTORY](cortex_provisioned_throughput_usage_history.md)
       - [CORTEX\_REST\_API\_USAGE\_HISTORY](cortex_rest_api_usage_history.md)
       - [CORTEX\_SEARCH\_DAILY\_USAGE\_HISTORY](cortex_search_daily_usage_history.md)
       - [CORTEX\_SEARCH\_SERVING\_USAGE\_HISTORY](cortex_search_serving_usage_history.md)
       - [CREDENTIALS](credentials.md)
       - [DATA\_CLASSIFICATION\_LATEST](data_classification_latest.md)
       - [DATA\_METRIC\_FUNCTION\_EXPECTATIONS](data_metric_function_expectations.md)
       - [DATA\_METRIC\_FUNCTION\_REFERENCES](data_metric_function_references.md)
       - [DATA\_QUALITY\_MONITORING\_USAGE\_HISTORY](data_quality_monitoring_usage_history.md)
       - [DATA\_TRANSFER\_HISTORY](data_transfer_history.md)
       - [DATABASE\_REPLICATION\_USAGE\_HISTORY](database_replication_usage_history.md)
       - [DATABASE\_STORAGE\_USAGE\_HISTORY](database_storage_usage_history.md)
       - [DATABASES](databases.md)
       - [DOCUMENT\_AI\_USAGE\_HISTORY](document_ai_usage_history.md)
       - [DYNAMIC\_TABLE\_REFRESH\_HISTORY](dynamic_table_refresh_history.md)
       - [ELEMENT\_TYPES](element_types.md)
       - [EVENT\_USAGE\_HISTORY](event_usage_history.md)
       - [EXTERNAL\_ACCESS\_HISTORY](external_access_history.md)
       - [FEATURE\_POLICIES](feature_policies.md)
       - [FIELDS](fields.md)
       - [FILE\_FORMATS](file_formats.md)
       - [FUNCTIONS](functions.md)
       - [GRANTS\_TO\_ROLES](grants_to_roles.md)
       - [GRANTS\_TO\_USERS](grants_to_users.md)
       - [HYBRID\_TABLES](hybrid_tables.md)
       - [HYBRID\_TABLE\_USAGE\_HISTORY](hybrid_table_usage_history.md)
       - [ICEBERG\_STORAGE\_OPTIMIZATION\_HISTORY](iceberg_storage_optimization_history.md)
       - [INDEX\_COLUMNS](index_columns.md)
       - [INDEXES](indexes.md)
       - [INGRESS\_NETWORK\_ACCESS\_HISTORY](ingress_network_access_history.md)
       - [INTERNAL\_DATA\_TRANSFER\_HISTORY](internal_data_transfer_history.md)
       - [INTERNAL\_STAGE\_NETWORK\_ACCESS\_HISTORY](internal_stage_network_access_history.md)
       - [JOIN\_POLICIES](join_policies.md)
       - [LOAD\_HISTORY](load_history.md)
       - [LOCK\_WAIT\_HISTORY](lock_wait_history.md)
       - [LOGIN\_HISTORY](login_history.md)
       - [MASKING\_POLICIES](masking_policies.md)
       - [MATERIALIZED\_VIEW\_REFRESH\_HISTORY](materialized_view_refresh_history.md)
       - [METERING\_DAILY\_HISTORY](metering_daily_history.md)
       - [METERING\_HISTORY](metering_history.md)
       - [NETWORK\_POLICIES](network_policies.md)
       - [NETWORK\_RULE\_REFERENCES](network_rule_references.md)
       - [NETWORK\_RULES](network_rules.md)
       - [NOTEBOOKS\_CONTAINER\_RUNTIME\_HISTORY](notebooks_container_runtime_history.md)
       - [OBJECT\_ACCESS\_REQUEST\_HISTORY](object_access_request_history.md)
       - [OBJECT\_DEPENDENCIES](object_dependencies.md)
       - [OPENFLOW\_USAGE\_HISTORY](openflow_usage_history.md)
       - [ONLINE\_FEATURE\_TABLE\_REFRESH\_HISTORY](online_feature_table_refresh_history.md)
       - [OUTBOUND\_PRIVATELINK\_ENDPOINTS](outbound_privatelink_endpoints.md)
       - [PASSWORD\_POLICIES](password_policies.md)
       - [PIPE\_USAGE\_HISTORY](pipe_usage_history.md)
       - [PIPES](pipes.md)
       - [POLICY\_REFERENCES](policy_references.md)
       - [POSTGRES\_STORAGE\_USAGE\_HISTORY](postgres_storage_usage_history.md)
       - [PRIVACY\_BUDGETS](privacy_budgets.md)
       - [PRIVACY\_POLICIES](privacy_policies.md)
       - [PROCEDURES](procedures.md)
       - [PROJECTION\_POLICIES](projection_policies.md)
       - [QUERY\_ACCELERATION\_ELIGIBLE](query_acceleration_eligible.md)
       - [QUERY\_ACCELERATION\_HISTORY](query_acceleration_history.md)
       - [QUERY\_ATTRIBUTION\_HISTORY](query_attribution_history.md)
       - [QUERY\_HISTORY](query_history.md)
       - [QUERY\_INSIGHTS](query_insights.md)
       - [REFERENTIAL\_CONSTRAINTS](referential_constraints.md)
       - [REPLICATION\_GROUP\_REFRESH\_HISTORY](replication_group_refresh_history.md)
       - [REPLICATION\_GROUP\_USAGE\_HISTORY](replication_group_usage_history.md)
       - [REPLICATION\_GROUPS](replication_groups.md)
       - [REPLICATION\_USAGE\_HISTORY](replication_usage_history.md)
       - [RESOURCE\_MONITORS](resource_monitors.md)
       - [ROLES](roles.md)
       - [ROW\_ACCESS\_POLICIES](row_access_policies.md)
       - [SCHEMATA](schemata.md)
       - [SEARCH\_OPTIMIZATION\_BENEFITS](search_optimization_benefits.md)
       - [SEARCH\_OPTIMIZATION\_HISTORY](search_optimization_history.md)
       - [SECRETS](secrets.md)
       - [SEMANTIC\_DIMENSIONS](semantic_dimensions.md)
       - [SEMANTIC\_FACTS](semantic_facts.md)
       - [SEMANTIC\_METRICS](semantic_metrics.md)
       - [SEMANTIC\_RELATIONSHIPS](semantic_relationships.md)
       - [SEMANTIC\_TABLES](semantic_tables.md)
       - [SEMANTIC\_VIEWS](semantic_views.md)
       - [SEQUENCES](sequences.md)
       - [SERVERLESS\_ALERT\_HISTORY](serverless_alert_history.md)
       - [SERVERLESS\_TASK\_HISTORY](serverless_task_history.md)
       - [SERVICES](services.md)
       - [SESSION\_POLICIES](session_policies.md)
       - [SESSIONS](sessions.md)
       - [SNAPSHOT\_OPERATION\_HISTORY — Deprecated](snapshot_operation_history.md)
       - [SNAPSHOT\_POLICIES — Deprecated](snapshot_policies.md)
       - [SNAPSHOT\_SETS — Deprecated](snapshot_sets.md)
       - [SNAPSHOT\_STORAGE\_USAGE — Deprecated](snapshot_storage_usage.md)
       - [SNAPSHOTS — Deprecated](snapshots.md)
       - [SNOWPARK\_CONTAINER\_SERVICES\_HISTORY](snowpark_container_services_history.md)
       - [SNOWPIPE\_STREAMING\_CHANNEL\_HISTORY](snowpipe_streaming_channel_history.md)
       - [SNOWPIPE\_STREAMING\_CLIENT\_HISTORY](snowpipe_streaming_client_history.md)
       - [SNOWPIPE\_STREAMING\_FILE\_MIGRATION\_HISTORY](snowpipe_streaming_file_migration_history.md)
       - [STAGE\_STORAGE\_USAGE\_HISTORY](stage_storage_usage_history.md)
       - [STAGES](stages.md)
       - [STORAGE\_LIFECYCLE\_POLICIES](storage_lifecycle_policies.md)
       - [STORAGE\_LIFECYCLE\_POLICY\_HISTORY](storage_lifecycle_policy_history.md)
       - [STORAGE\_USAGE](storage_usage.md)
       - [TABLE\_CONSTRAINTS](table_constraints.md)
       - [TABLE\_DML\_HISTORY](table_dml_history.md)
       - [TABLE\_PRUNING\_HISTORY](table_pruning_history.md)
       - [TABLE\_QUERY\_PRUNING\_HISTORY](table_query_pruning_history.md)
       - [TABLE\_STORAGE\_METRICS](table_storage_metrics.md)
       - [TABLES](tables.md)
       - [TAG\_REFERENCES](tag_references.md)
       - [TAGS](tags.md)
       - [TASK\_HISTORY](task_history.md)
       - [TASK\_VERSIONS](task_versions.md)
       - [TRUST\_CENTER\_FINDINGS](trust_center_findings.md)
       - [USERS](users.md)
       - [VIEWS](views.md)
       - [WAREHOUSE\_EVENTS\_HISTORY](warehouse_events_history.md)
       - [WAREHOUSE\_LOAD\_HISTORY](warehouse_load_history.md)
       - [WAREHOUSE\_METERING\_HISTORY](warehouse_metering_history.md)
     + [Billing](../billing.md)
     + [Data Sharing Usage](../data-sharing-usage.md)
     + [Local](../local.md)
     + [Monitoring](../monitoring.md)
     + [Organization Usage](../organization-usage.md)
     + [Telemetry](../telemetry.md)
     + [Trust Center](../trust_center.md)
     + [SNOWFLAKE database roles](../snowflake-db-roles.md)
     + [Snowflake classes](../snowflake-db-classes.md)
   * [Snowflake Information Schema](../info-schema.md)
   * [Metadata fields](../metadata.md)
   * [Conventions](../conventions.md)
   * [Reserved keywords](../reserved-keywords.md)
8. [API reference](../../api-reference.md)

[Reference](../../reference.md)[General reference](../../sql-reference.md)[SNOWFLAKE database](../snowflake-db.md)[Account Usage](../account-usage.md)CORTEX\_FUNCTIONS\_USAGE\_HISTORY

Schema:
:   [ACCOUNT\_USAGE](../account-usage.html#label-account-usage-views)

# CORTEX\_FUNCTIONS\_USAGE\_HISTORY view[¶](#cortex-functions-usage-history-view "Link to this heading")

Important

This view is no longer updated. Use the [CORTEX\_AISQL\_USAGE\_HISTORY](cortex_aisql_usage_history) view instead.

This Account Usage view can be used to query the usage history of [Cortex Functions](../../user-guide/snowflake-cortex/aisql) such
as COMPLETE and TRANSLATE. The information in the view includes the number of tokens and credits consumed each time a Cortex Function is
called, aggregated in one hour increments based on function and model. The view also includes relevant metadata, such as the warehouse ID,
start and end times of the function execution, and the name of the function and the model, if specified.

Note

The view might not include usage information on functions called with recently added models. A new model can take up to 2 weeks to
be included in this view.

## Columns[¶](#columns "Link to this heading")

| Column Name | Data Type | Description |
| --- | --- | --- |
| START\_TIME | TIMESTAMP\_LTZ | Start of the specified time range in which the Cortex LLM function usage took place. |
| END\_TIME | TIMESTAMP\_LTZ | End of the specified time range in which the Cortex LLM function usage took place. |
| FUNCTION\_NAME | VARCHAR | Name of the Cortex LLM function. |
| MODEL\_NAME | VARCHAR | Model name. Empty for Cortex LLM functions where a model is not specified as an argument. |
| WAREHOUSE\_ID | NUMBER | System-generated identifier for the warehouse used by the query calling the Cortex LLM function. |
| TOKENS | NUMBER | Number of tokens billed. |
| TOKEN\_CREDITS | NUMBER | Number of credits billed for Cortex LLM functions usage based on tokens processed for the specified function and model (if applicable) during the START\_TIME and END\_TIME window. |

## Usage notes[¶](#usage-notes "Link to this heading")

* The view provides up-to-date credit usage for an account within the last 365 days (1 year).
* The credit rate usage is determined based on the function called, model used and the tokens processed as outlined in the
  [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).
* In some cases where a model is used but is not billed, the model column may be empty.

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