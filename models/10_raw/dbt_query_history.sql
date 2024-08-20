/* This view will show you realtime query history for the last couple days and break out dbt query tag information.
{{- config( materialized='view') }} */
with WAREHOUSE_SIZE AS
(
     SELECT WAREHOUSE_SIZE, NODES
       FROM (
              SELECT 'X-SMALL' AS WAREHOUSE_SIZE, 1 AS NODES
              UNION ALL
              SELECT 'SMALL' AS WAREHOUSE_SIZE, 2 AS NODES
              UNION ALL
              SELECT 'MEDIUM' AS WAREHOUSE_SIZE, 4 AS NODES
              UNION ALL
              SELECT 'LARGE' AS WAREHOUSE_SIZE, 8 AS NODES
              UNION ALL
              SELECT 'X-LARGE' AS WAREHOUSE_SIZE, 16 AS NODES
              UNION ALL
              SELECT '2X-LARGE' AS WAREHOUSE_SIZE, 32 AS NODES
              UNION ALL
              SELECT '3X-LARGE' AS WAREHOUSE_SIZE, 64 AS NODES
              UNION ALL
              SELECT '4X-LARGE' AS WAREHOUSE_SIZE, 128 AS NODES
              UNION ALL
              SELECT '5X-LARGE' AS WAREHOUSE_SIZE, 256 AS NODES
              UNION ALL
              SELECT '6X-LARGE' AS WAREHOUSE_SIZE, 512 AS NODES
            )
), QUERY_HISTORY as (
    select try_parse_json(query_tag) as query_tag_object, *
    from table(information_schema.QUERY_HISTORY_BY_WAREHOUSE(
        WAREHOUSE_NAME => current_warehouse(),
        END_TIME_RANGE_START => DATEADD(DAY, -1, DATE_TRUNC(DAY, CURRENT_TIMESTAMP())),
        RESULT_LIMIT => 10000
    ))
)
select
    query_id,
    start_time,
    end_time,
    total_elapsed_time/1000 as total_elapsed_sec,
    execution_status,
    query_tag_object:node_name::varchar as node_name,
    query_type,
    query_text,
    query_tag_object:node_resource_type::varchar as node_resource_type,
    query_tag_object:node_alias::varchar as node_alias,
    user_name,
    role_name,
    warehouse_name,
    qh.warehouse_size,
    WS.NODES as warehouse_nodes,
    cluster_number,
    error_message,
    bytes_scanned,
    rows_produced,
    (compilation_time/1000) as compilation_sec,
    (execution_time/1000) as execution_sec,
    nvl( (QH.EXECUTION_TIME/(1000*60*60))*WS.NODES, 0) as RELATIVE_PERFORMANCE_COST,
    credits_used_cloud_services,
    query_hash,
    bytes_written_to_result,
    rows_written_to_result,
    rows_inserted,
    query_tag_object:materialized::varchar as materialized,
    query_tag_object:full_refresh::varchar as full_refresh,
    query_tag_object:invocation_command::varchar as invocation_command,
    query_tag_object:invocation_id::varchar as invocation_id,
    query_tag_object:node_database::varchar as node_database,
    query_tag_object:node_unique_id::varchar as node_unique_id,
    to_json(query_tag_object:node_meta) as node_meta,
    query_tag_object:node_original_file_path::varchar as node_original_file_path,
    query_tag_object:node_package_name::varchar as node_package_name,
    to_json(query_tag_object:node_refs) as node_refs,
    query_tag_object:node_schema::varchar as node_schema,
    query_tag_object:node_tags::varchar as node_tags,
    query_tag_object:project_name::varchar as project_name,
    query_tag_object:raw_code_hash::varchar as raw_code_hash,
    query_tag_object:run_started_at::varchar as run_started_at,
    query_tag_object:target_database::varchar as target_database,
    query_tag_object:target_name::varchar as target_name,
    query_tag_object:target_schema::varchar as target_schema,
    query_tag_object:thread_id::varchar as thread_id,
    query_tag_object:which::varchar as which,
    query_tag_object:app::varchar as app,
    query_tag_object:dbt_version::varchar as dbt_version,
from query_history qh
LEFT OUTER JOIN WAREHOUSE_SIZE WS ON WS.WAREHOUSE_SIZE = upper(QH.WAREHOUSE_SIZE)
where 1=1
-- and app = 'dbt'
-- and query_type not in ('ALTER_SESSION', 'DESCRIBE')
-- and node_resource_type in ('model')
and total_elapsed_time > 500 -- Only show queries over .5 second
order by start_time desc
