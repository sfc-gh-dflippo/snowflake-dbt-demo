{{ config(materialized = 'table') }}

with dwao as (
    -- CSV with specific assignments to use instead of dynamic ones
    select
        upper(target_name) as target_name,
        full_refresh_warehouse,
        incremental_warehouse
    from {{ ref('dynamic_warehouse_assignment_overrides') }}
),
query_history as (
    select qh.target_name,
        qh.warehouse_size,
        qh.is_incremental,
        qh.partitions_scanned,
        -- We don't use these now but may add logic in the future
        qh.bytes_scanned,
        iff(bytes_spilled_to_local_storage > 0, true, false) as local_spillage,
        iff(bytes_spilled_to_remote_storage > 0, true, false) as remote_spillage
    from {{ ref('dbt_account_usage_query_history') }} qh
    where qh.target_name is not null
        and qh.is_incremental is not null
        and qh.partitions_scanned > 0
        -- Depending on the number of jobs, we may want more or less history for the max()
        and qh.start_time > DATEADD(DAY, -30, DATE_TRUNC(DAY, CURRENT_TIMESTAMP()))
        -- Exclude modules that have an override
        and not exists(
            select null
            from dwao
            where dwao.target_name = qh.target_name
        )
),
max_micropartitions as (
    -- Query the largest number of micropartitions in our query history for each target
    select qh.target_name as target_name,
        max(qh.partitions_scanned) as max_partitions_scanned,
        -- Use the number of micropartitions from an incremental run if it exists
        coalesce(
            max(case when qh.is_incremental = true then qh.partitions_scanned end),
            max_partitions_scanned ) as max_incremental_partitions_scanned
    from query_history qh
    group by all
),
best_warehouses as (
    -- Join the max micropartitions with the dynamic warehouses csv to find the smallest allowable warehouse
    select max_micro.target_name,
        full_refresh_warehouse.warehouse_name as full_refresh_warehouse,
        incremental_warehouse.warehouse_name as incremental_warehouse
    from max_micropartitions max_micro
        join {{ ref("dynamic_warehouses") }} full_refresh_warehouse on
            max_micro.max_partitions_scanned < full_refresh_warehouse.micropartition_capacity
        join {{ ref("dynamic_warehouses") }} incremental_warehouse on
            max_micro.max_incremental_partitions_scanned < incremental_warehouse.micropartition_capacity
    qualify 1 = row_number() over (
            partition by max_micro.target_name
            order by full_refresh_warehouse.micropartition_capacity, incremental_warehouse.micropartition_capacity
        )
),
combined as (
    select target_name,
        full_refresh_warehouse,
        incremental_warehouse
    from dwao
    union all
    select target_name,
        full_refresh_warehouse,
        incremental_warehouse
    from best_warehouses
)
select *
from combined
ORDER BY 1