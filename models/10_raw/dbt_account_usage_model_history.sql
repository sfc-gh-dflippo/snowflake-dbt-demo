with largest_query as (
    select
    project_name,
    module_name,
    listagg(distinct warehouse_size, ',') within group (order by warehouse_size) as past_warehouse_sizes,
    max(partitions_scanned) as max_partitions_scanned
    from {{ ref("dbt_account_usage_query_history") }} query_history
    where module_type = 'model'
    and warehouse_size is not null
    group by all
)
select
    project_name,
    module_name,
    warehouse_name
from largest_query
join {{ ref("dynamic_warehouses") }} dynamic_warehouses on
   max_partitions_scanned >= minimum_micropartitions
qualify 1 = row_number() over (partition by project_name, module_name order by minimum_micropartitions desc)
order by 1, 2, 3
