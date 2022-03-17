{# This macro is a modified version from DBT_ARTIFACTS but logic is now in a stored procedure #}

{% macro create_artifact_resources() %}

{% set src_dbt_artifacts = source('dbt_artifacts', 'artifacts') %}
{% set artifact_stage = src_dbt_artifacts.database ~ "." ~ src_dbt_artifacts.schema ~ "." ~ var('dbt_artifacts_stage', 'dbt_artifacts_stage') %}

{% set src_results = source('dbt_artifacts', 'dbt_run_results') %}
{% set src_results_nodes = source('dbt_artifacts', 'dbt_run_results_nodes') %}
{% set src_manifest_nodes = source('dbt_artifacts', 'dbt_manifest_nodes') %}

{{ create_schema(src_dbt_artifacts) }}

{% set create_v1_stage_query %}
create stage if not exists {{ src_dbt_artifacts }}
file_format = (type = json);
{% endset %}

{% set create_v2_stage_query %}
create stage if not exists {{ artifact_stage }}
file_format = (type = json);
{% endset %}

{% set create_v1_table_query %}
create table if not exists {{ src_dbt_artifacts }} (
    data variant,
    generated_at timestamp,
    path string,
    artifact_type string
);
{% endset %}

{% set create_v2_results_query %}
create table if not exists {{ src_results }} (
    command_invocation_id string,
    dbt_cloud_run_id int,
    artifact_run_id string,
    artifact_generated_at timestamp_tz,
    dbt_version string,
    env variant,
    elapsed_time double,
    execution_command string,
    was_full_refresh boolean,
    selected_models variant,
    target string,
    metadata variant,
    args variant
);
{% endset %}

{% set create_v2_result_nodes_table_query %}
create table if not exists {{ src_results_nodes }} (
    command_invocation_id string,
    dbt_cloud_run_id int,
    artifact_run_id string,
    artifact_generated_at timestamp_tz,
    execution_command string,
    was_full_refresh boolean,
    node_id string,
    thread_id integer,
    status string,
    message string,
    compile_started_at timestamp_tz,
    query_completed_at timestamp_tz,
    total_node_runtime float,
    rows_affected int,
    result_json variant
);
{% endset %}

{% set create_v2_manifest_nodes_table_query %}
create table if not exists {{ src_manifest_nodes }} (
    command_invocation_id string,
    dbt_cloud_run_id int,
    artifact_run_id string,
    artifact_generated_at timestamp_tz,
    node_id string,
    resource_type string,
    node_database string,
    node_schema string,
    name string,
    depends_on_nodes array,
    depends_on_sources array,
    exposure_type string,
    exposure_owner string,
    exposure_maturity string,
    source_name string,
    package_name string,
    relation_name string,
    node_path string,
    checksum string,
    materialization string,
    node_json variant
);
{% endset %}

{# {% do log("Creating V1 Stage: " ~ create_v1_stage_query, info=True) %}
{% do run_query(create_v1_stage_query) %}

{% do log("Creating V2 Stage: " ~ create_v2_stage_query, info=True) %}
{% do run_query(create_v2_stage_query) %}

{% do log("Creating V1 Table: " ~ create_v1_table_query, info=True) %}
{% do run_query(create_v1_table_query) %} #}

{% do log("Creating V2 Results Table: " ~ create_v2_results_query, info=True) %}
{% do run_query(create_v2_results_query) %}

{% do log("Creating V2 Result Nodes Table: " ~ create_v2_result_nodes_table_query, info=True) %}
{% do run_query(create_v2_result_nodes_table_query) %}

{% do log("Creating V2 Manifest Nodes Table: " ~ create_v2_manifest_nodes_table_query, info=True) %}
{% do run_query(create_v2_manifest_nodes_table_query) %}

{% set create_stored_procedure %}
CREATE OR REPLACE PROCEDURE LOG_DBT_ARTIFACTS(
    STAGE_LOCATION VARCHAR
)
RETURNS VARCHAR
LANGUAGE JAVASCRIPT
AS
$$

    snowflake.execute({sqlText: `insert into DBT_RUN_RESULTS(
          command_invocation_id,
          dbt_cloud_run_id,
          artifact_run_id,
          artifact_generated_at,
          dbt_version,
          env,
          elapsed_time,
          execution_command,
          was_full_refresh,
          selected_models,
          target,
          metadata,
          args
        )
        with raw_data as (
            select
                $1:metadata as metadata,
                $1:args as args,
                $1:elapsed_time::float as elapsed_time
            from @` + STAGE_LOCATION + `/run_results.json.gz
            
        )
        
        select
            metadata:invocation_id::string as command_invocation_id,
            -- NOTE: DBT_CLOUD_RUN_ID is case sensitive here 
            metadata:env:DBT_CLOUD_RUN_ID::int as dbt_cloud_run_id,
            coalesce(dbt_cloud_run_id::string, command_invocation_id::string) as artifact_run_id,
            metadata:generated_at::timestamp_tz as artifact_generated_at,
            metadata:dbt_version::string as dbt_version,
            metadata:env as env,
            elapsed_time,
            args:which::string as execution_command,
            coalesce(args:full_refresh, 'false')::boolean as was_full_refresh,
            args:models as selected_models,
            args:target::string as target,
            metadata,
            args
        from raw_data
        where not exists (
                select null
                from DBT_RUN_RESULTS existing_rows
                where existing_rows.artifact_generated_at = metadata:generated_at::timestamp_tz
                    and (existing_rows.dbt_cloud_run_id = metadata:env:DBT_CLOUD_RUN_ID::int
                        or existing_rows.command_invocation_id = metadata:invocation_id::string))
    `});
        
        
    snowflake.execute({sqlText: `insert into DBT_RUN_RESULTS_NODES(
            command_invocation_id,
            dbt_cloud_run_id,
            artifact_run_id,
            artifact_generated_at,
            execution_command,
            was_full_refresh,
            node_id,
            thread_id,
            status,
            message,
            compile_started_at,
            query_completed_at,
            total_node_runtime,
            rows_affected,
            result_json
        )
        with raw_data as (
            select
                $1:metadata as metadata,
                $1 as data
            from @` + STAGE_LOCATION + `/run_results.json.gz
            ),
        deduplicated_data as (
            select
                metadata,
                data,
                metadata:invocation_id::string as command_invocation_id,
                -- NOTE: DBT_CLOUD_RUN_ID is case sensitive here 
                metadata:env:DBT_CLOUD_RUN_ID::int as dbt_cloud_run_id,
                coalesce(dbt_cloud_run_id::string, command_invocation_id::string) as artifact_run_id,
                metadata:generated_at::timestamp_tz as generated_at
            from raw_data
            where not exists (
                select null
                from DBT_RUN_RESULTS_NODES existing_rows
                where existing_rows.artifact_generated_at = metadata:generated_at::timestamp_tz
                    and (existing_rows.dbt_cloud_run_id = metadata:env:DBT_CLOUD_RUN_ID::int
                        or existing_rows.command_invocation_id = metadata:invocation_id::string)
            )
        )
        select
            run_results.command_invocation_id,
            run_results.dbt_cloud_run_id,
            run_results.artifact_run_id,
            run_results.generated_at::timestamp_tz as artifact_generated_at,
            run_results.data:args:which::string as execution_command,
            coalesce(run_results.data:args:full_refresh, 'false')::boolean as was_full_refresh,
            result.value:unique_id::string as node_id,
            split(result.value:thread_id::string, '-')[1]::integer as thread_id,
            result.value:status::string as status,
            result.value:message::string as message,
            -- The first item in the timing array is the model-level "compile"
            result.value:timing[0]:started_at::timestamp_tz as compile_started_at,
            -- The second item in the timing array is "execute".
            result.value:timing[1]:completed_at::timestamp_tz as query_completed_at,
            -- Confusingly, this does not match the delta of the above two timestamps.
            -- should we calculate it instead?
            coalesce(result.value:execution_time::float, 0) as total_node_runtime,
            result.value:adapter_response:rows_affected::int as rows_affected,
            -- Include the raw JSON for future proofing.
            result.value as result_json
        from deduplicated_data as run_results,
            lateral flatten(input => run_results.data:results) as result
     `});


    snowflake.execute({sqlText: `insert into DBT_MANIFEST_NODES(
            command_invocation_id,
            dbt_cloud_run_id,
            artifact_run_id,
            artifact_generated_at,
            node_id,
            resource_type,
            node_database,
            node_schema,
            name,
            depends_on_nodes,
            depends_on_sources,
            exposure_type,
            exposure_owner,
            exposure_maturity,
            source_name,
            package_name,
            relation_name,
            node_path,
            checksum,
            materialization,
            node_json
        )
        with raw_data as (
            select
                $1:metadata as metadata,
                $1 as data
            from @` + STAGE_LOCATION + `/manifest.json.gz
        ), 
        deduplicated_data as (
            select
                metadata,
                metadata:invocation_id::string as command_invocation_id,
                -- NOTE: DBT_CLOUD_RUN_ID is case sensitive here 
                metadata:env:DBT_CLOUD_RUN_ID::int as dbt_cloud_run_id,
                coalesce(dbt_cloud_run_id::string, command_invocation_id::string) as artifact_run_id,
                metadata:generated_at::timestamp_tz as generated_at,
                data
            from raw_data
            where not exists (
                select null
                from DBT_MANIFEST_NODES existing_rows
                where existing_rows.artifact_generated_at = metadata:generated_at::timestamp_tz
                    and (existing_rows.dbt_cloud_run_id = metadata:env:DBT_CLOUD_RUN_ID::int
                        or existing_rows.command_invocation_id = metadata:invocation_id::string)
            ) 
        )
        select
            manifests.command_invocation_id,
            manifests.dbt_cloud_run_id,
            manifests.artifact_run_id,
            manifests.generated_at::timestamp_tz as artifact_generated_at,
            node.key as node_id,
            node.value:resource_type::string as resource_type,
            node.value:database::string as node_database,
            node.value:schema::string as node_schema,
            node.value:name::string as name,
            to_array(node.value:depends_on:nodes) as depends_on_nodes,
            null as depends_on_sources,
            null as exposure_type,
            null as exposure_owner,
            null as exposure_maturity,
            null as source_name,
            node.value:package_name::string as package_name,
            null as relation_name,
            node.value:path::string as node_path,
            node.value:checksum.checksum::string as checksum,
            node.value:config.materialized::string as materialization,
            -- Include the raw JSON for future proofing.
            node.value as node_json
        from deduplicated_data as manifests,
            lateral flatten(input => manifests.data:nodes) as node

        union all

        select
            manifests.command_invocation_id,
            manifests.dbt_cloud_run_id,
            manifests.artifact_run_id,
            manifests.generated_at::timestamp_tz as artifact_generated_at,
            exposure.key as node_id,
            'exposure' as resource_type,
            null as node_database,
            null as node_schema,
            exposure.value:name::string as name,
            to_array(exposure.value:depends_on:nodes) as depends_on_nodes,
            to_array(exposure.value:sources:nodes) as depends_on_sources,
            exposure.value:type::string as exposure_type,
            exposure.value:owner:name::string as exposure_owner,
            exposure.value:maturity::string as exposure_maturity,
            null as source_name,
            exposure.value:package_name::string as package_name,
            null as relation_name,
            null as node_path,
            null as checksum,
            null as materialization,
            -- Include the raw JSON for future proofing.
            exposure.value as node_json
        from deduplicated_data as manifests,
            lateral flatten(input => manifests.data:exposures) as exposure

        union all

        select
            manifests.command_invocation_id,
            manifests.dbt_cloud_run_id,
            manifests.artifact_run_id,
            manifests.generated_at::timestamp_tz as artifact_generated_at,
            source.key as node_id,
            'source' as resource_type,
            source.value:database::string as node_database,
            source.value:schema::string as node_schema,
            source.value:name::string::string as name,
            null as depends_on_nodes,
            null as depends_on_sources,
            null as exposure_type,
            null as exposure_owner,
            null as exposure_maturity,
            source.value:source_name::string as source_name,
            source.value:package_name::string as package_name,
            source.value:relation_name::string as relation_name,
            source.value:path::string as node_path,
            null as checksum,
            null as materialization,
            -- Include the raw JSON for future proofing.
            source.value as node_json
        from deduplicated_data as manifests,
            lateral flatten(input => manifests.data:sources) as source
        `});

    return 'SUCCESS';

$$
{% endset %}

{% do log("Creating dbt artifacts load procedure: " ~ create_stored_procedure, info=True) %}
{% do run_query(create_stored_procedure) %}

{% endmacro %}