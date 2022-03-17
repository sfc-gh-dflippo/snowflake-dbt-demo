{{ config(materialized = 'view') }}
select
    DBT_MANIFEST_NODES.node_id,
    DBT_MANIFEST_NODES.package_name,
    DBT_MANIFEST_NODES.resource_type,
    DBT_MANIFEST_NODES.node_database,
    DBT_MANIFEST_NODES.node_schema,
    DBT_MANIFEST_NODES.name,
    DBT_MANIFEST_NODES.command_invocation_id,
    DBT_MANIFEST_NODES.dbt_cloud_run_id,
    DBT_MANIFEST_NODES.artifact_generated_at manifest_generated_at,
    DBT_MANIFEST_NODES.depends_on_nodes,
    DBT_MANIFEST_NODES.depends_on_sources,
    DBT_MANIFEST_NODES.exposure_type,
    DBT_MANIFEST_NODES.exposure_owner,
    DBT_MANIFEST_NODES.exposure_maturity,
    DBT_MANIFEST_NODES.source_name,
    DBT_MANIFEST_NODES.relation_name,
    DBT_MANIFEST_NODES.node_path,
    DBT_MANIFEST_NODES.checksum,
    DBT_MANIFEST_NODES.materialization,
    DBT_RUN_RESULTS_NODES.artifact_generated_at run_results_generated_at,
    DBT_RUN_RESULTS_NODES.was_full_refresh,
    DBT_RUN_RESULTS_NODES.thread_id,
    DBT_RUN_RESULTS_NODES.status,
    DBT_RUN_RESULTS_NODES.message,
    DBT_RUN_RESULTS_NODES.compile_started_at,
    DBT_RUN_RESULTS_NODES.query_completed_at,
    DBT_RUN_RESULTS_NODES.total_node_runtime,
    DBT_RUN_RESULTS_NODES.rows_affected,
    DBT_RUN_RESULTS.ENV AS RUN_ENV,
    DBT_RUN_RESULTS.ELAPSED_TIME AS RUN_ELAPSED_TIME,
    DBT_RUN_RESULTS.EXECUTION_COMMAND AS RUN_EXECUTION_COMMAND,
    DBT_RUN_RESULTS.SELECTED_MODELS AS RUN_SELECTED_MODELS,
    DBT_RUN_RESULTS.TARGET AS RUN_TARGET,
    DBT_RUN_RESULTS.METADATA AS RUN_METADATA,
    DBT_RUN_RESULTS.ARGS AS RUN_ARGS
from {{ source('dbt_artifacts', 'dbt_run_results') }} DBT_RUN_RESULTS
    INNER JOIN {{ source('dbt_artifacts', 'dbt_manifest_nodes') }} DBT_MANIFEST_NODES on (
        DBT_MANIFEST_NODES.artifact_run_id = DBT_RUN_RESULTS.artifact_run_id)
    LEFT OUTER join {{ source('dbt_artifacts', 'dbt_run_results_nodes') }} DBT_RUN_RESULTS_NODES on (
        DBT_MANIFEST_NODES.artifact_run_id = DBT_RUN_RESULTS_NODES.artifact_run_id
        and DBT_MANIFEST_NODES.node_id = DBT_RUN_RESULTS_NODES.node_id)
