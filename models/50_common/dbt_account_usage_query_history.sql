{{ config(
    materialized = "incremental"
) }}

with WAREHOUSE_SIZE AS (
    SELECT *, FROM (
        VALUES
        ('X-SMALL', 1, 8),
        ('SMALL', 2, 16),
        ('MEDIUM', 4, 32),
        ('LARGE', 8, 64),
        ('X-LARGE', 16, 128),
        ('2X-LARGE', 32, 256),
        ('3X-LARGE', 64, 512),
        ('4X-LARGE', 128, 1024),
        ('5X-LARGE', 256, 2048),
        ('6X-LARGE', 512, 4096)
    ) AS v1 (WAREHOUSE_SIZE, CREDITS_PER_HOUR, VCPU)
), query_history as (
    select
    * REPLACE (try_parse_json(query_tag) as query_tag)
    from {{ source("account_usage", "query_history") }} qh
    where qh.query_tag is not null

    {% if is_incremental() -%}
    and qh.start_time > (select max(t.start_time) from {{ this }} t)
    {%- else %}
    and qh.start_time > DATEADD(DAY, -90, DATE_TRUNC(DAY, CURRENT_TIMESTAMP()))
    {%- endif %}

)
select
    query_id,
    start_time,
    end_time,
    total_elapsed_time/1000 as total_elapsed_sec,
    execution_status,
    query_tag,
    upper(query_tag:target_name::varchar) as target_name,
    try_to_boolean(query_tag:module_details:is_incremental::varchar) as is_incremental,
    query_tag:app::varchar as app,
    query_tag:app_version::varchar as app_version,
    query_tag:module_name::varchar as module_name,
    query_tag:module_type::varchar as module_type,
    query_type,
    query_text,
    user_name,
    role_name,
    warehouse_name,
    qh.warehouse_size,
    WS.CREDITS_PER_HOUR as warehouse_nodes,
    WS.VCPU as warehouse_vcpu,
    cluster_number,
    error_message,
    bytes_scanned,
    rows_produced,
    (compilation_time/1000) as compilation_sec,
    (execution_time/1000) as execution_sec,
    nvl( (QH.EXECUTION_TIME/(1000*60*60))*WS.CREDITS_PER_HOUR, 0) as RELATIVE_PERFORMANCE_COST,
    credits_used_cloud_services,
    partitions_scanned,
    partitions_total,
    bytes_spilled_to_local_storage,
    bytes_spilled_to_remote_storage,
    query_load_percent,
    query_hash,
    bytes_written,
    bytes_written_to_result,
    rows_written_to_result,
    rows_inserted,
    rows_updated,
    rows_deleted,
    query_tag:project_name::varchar as project_name,
    query_tag:run_id::varchar as run_id,
    query_tag:run_details as run_details,
    run_details:full_refresh::varchar as full_refresh,
    query_tag:module_id::varchar as module_id,
    query_tag:module_details as module_details,
    query_tag:module_tags as module_tags,
    query_tag:run_started_at::varchar as run_started_at,
    query_tag:environment_name::varchar as environment_name,
    query_tag:environment_details as environment_details
from query_history qh
LEFT OUTER JOIN WAREHOUSE_SIZE WS ON WS.WAREHOUSE_SIZE = upper(QH.WAREHOUSE_SIZE)
where app = 'dbt'
    and project_name = '{{ project_name }}'
-- and query_type not in ('ALTER_SESSION', 'DESCRIBE')
-- and module_type in ('model')
-- and total_elapsed_time > 500 -- Only show queries over .5 second
