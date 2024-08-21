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
    select try_parse_json(query_tag) as v, *
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
    v:app::varchar as app,
    v:app_version::varchar as app_version,
    v:module_name::varchar as module_name,
    v:module_type::varchar as module_type,
    query_type,
    query_text,
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
    v:project_name::varchar as project_name,
    v:run_id::varchar as run_id,
    v:run_details as run_details,
    v:module_id::varchar as module_id,
    v:module_details as module_details,
    v:module_tags as module_tags,
    v:run_started_at::varchar as run_started_at,
    v:environment_name::varchar as environment_name,
    v:environment_details as environment_details,
from query_history qh
LEFT OUTER JOIN WAREHOUSE_SIZE WS ON WS.WAREHOUSE_SIZE = upper(QH.WAREHOUSE_SIZE)
where 1=1
-- and app = 'dbt'
-- and query_type not in ('ALTER_SESSION', 'DESCRIBE')
-- and node_resource_type in ('model')
and total_elapsed_time > 500 -- Only show queries over .5 second
order by start_time desc
