/*
    Simulate a query for the current year sales orders
    This demonstrates some of the Snowflake specific options
*/

{{ config(
    materialized="incremental",
    unique_key="INTEGRATION_ID",
    merge_exclude_columns = ["DBT_INSERT_TS"],
    transient=false
    )
}}

select
    '{{ env_var("SOURCE_SYSTEM_CODE", "UNKNOWN") }}' as source_system_code,
    coalesce(orders.o_order_wid, 0) as l_order_wid,
    coalesce(orders.o_cust_wid, 0) as l_cust_wid,
    lineitem.*,
    lkp_exchange_rates.conversion_rate as eur_conversion_rate,
    {{ surrogate_key(["L_ORDERKEY", "L_LINENUMBER"]) }} as integration_id,
    sysdate() as dbt_insert_ts,
    sysdate() as dbt_last_update_ts
from {{ source("TPC_H", "LINEITEM") }} lineitem
left outer join {{ ref("DIM_ORDERS") }} orders on l_orderkey = o_orderkey
left outer join {{ ref("LKP_EXCHANGE_RATES") }} lkp_exchange_rates
    on
        lkp_exchange_rates.from_currency = 'USD'
        and lkp_exchange_rates.to_currency = 'EUR'
        and lkp_exchange_rates.day_dt = o_orderdate

{% if is_incremental() %}
    -- this filter will only be applied on an incremental run
    -- the filter uses a global variable to know how many days to reprocess
    where l_shipdate
        >= dateadd(day, -3, (select date_trunc('DAY', max(l_shipdate)) from {{ this }}))
        or o_orderstatus = 'O'
{% endif %}
