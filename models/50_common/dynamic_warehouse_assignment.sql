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
        qh.bytes_scanned,
        iff(bytes_spilled_to_local_storage > 0, true, false) as local_spillage,
        iff(bytes_spilled_to_remote_storage > 0, true, false) as remote_spillage
    from {{ ref('dbt_account_usage_query_history') }} qh
    where qh.target_name is not null
        and qh.is_incremental is not null
        and qh.partitions_scanned > 0
        -- Exclude modules that have an override
        and not exists(
            select null
            from dwao
            where dwao.target_name = qh.target_name
        )
),
max_micropartitions as (
    -- Query the largest number of micropartitions in our query history for each module
    select qh.target_name as target_name,
        max(qh.partitions_scanned) as max_partitions_scanned,
        -- Use the number of micropartitions from an incremental run if it exists
        coalesce(
            max(case when qh.is_incremental = true then qh.partitions_scanned end),
            max(qh.partitions_scanned)) as max_incremental_partitions_scanned
    from query_history qh
    group by all
),
best_warehouses as (
    -- Join the max micropartitions with the dynamic warehouses csv to find the smallest allowable warehouse
    select m.target_name,
        full_refresh_warehouse.warehouse_name as full_refresh_warehouse,
        incremental_warehouse.warehouse_name as incremental_warehouse
        --full_refresh_warehouse.micropartition_capacity as full_micropartition_capacity,
        --incremental_warehouse.micropartition_capacity as incremental_micropartition_capacity
    from max_micropartitions m
        join {{ ref("dynamic_warehouses") }} full_refresh_warehouse on
            m.max_partitions_scanned < full_refresh_warehouse.micropartition_capacity
        join {{ ref("dynamic_warehouses") }} incremental_warehouse on
            m.max_incremental_partitions_scanned < incremental_warehouse.micropartition_capacity
    qualify 1 = row_number() over (
            partition by m.target_name
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
