{# If run regularly, this can allow you to build up a longer history of your own queries #}
{# We have set `full_refresh = false` to prevent losing history when full-loading other tables #}
{{- config(
    materialized='incremental',
    full_refresh = false,
    on_schema_change='sync_all_columns'
) -}}

with warehouse_size as
(
    select *, from (
        values
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
    ) as v1 (warehouse_size, warehouse_nodes, warehouse_vcpu)
), query_history as (
    select
    * replace (try_parse_json(query_tag) as query_tag)
    from table({{ this.database }}.information_schema.query_history_by_user(
        end_time_range_start => dateadd(day, -1, date_trunc(day, current_timestamp())),
        result_limit => 10000
    )) qh
    {% if is_incremental() -%}

    where qh.start_time > (select max(t.start_time) from {{ this }} t)

    {%- endif %}
)
select
    'https://app.snowflake.com/' ||
        current_organization_name() || '/' || current_account_name() ||
        '/#/compute/history/queries/' || query_id as query_profile_url,
    total_elapsed_time/1000 as total_elapsed_sec,
    upper(query_tag:target_name::varchar) as target_name,
    try_to_boolean(query_tag:module_details:is_incremental::varchar) as is_incremental,
    query_tag:app::varchar as app,
    query_tag:app_version::varchar as app_version,
    query_tag:module_name::varchar as module_name,
    query_tag:module_type::varchar as module_type,
    (compilation_time/1000) as compilation_sec,
    (execution_time/1000) as execution_sec,
    nvl( (qh.execution_time/(1000*60*60))*ws.warehouse_nodes, 0) as relative_performance_cost,
    query_tag:project_name::varchar as project_name,
    query_tag:run_id::varchar as run_id,
    query_tag:run_details as run_details,
    query_tag:module_id::varchar as module_id,
    query_tag:module_details as module_details,
    query_tag:module_tags as module_tags,
    query_tag:run_started_at::varchar as run_started_at,
    query_tag:environment_name::varchar as environment_name,
    query_tag:environment_details as environment_details,
    ws.*,
    qh.* exclude (warehouse_size)
from query_history qh
left outer join warehouse_size ws on ws.warehouse_size = upper(qh.warehouse_size)
where app = 'dbt'
-- Sample Filters:
-- AND QUERY_TYPE NOT IN ('ALTER_SESSION', 'DESCRIBE')
-- AND MODULE_TYPE IN ('model')
-- AND TOTAL_ELAPSED_TIME > 500 -- Only show queries over .5 second
