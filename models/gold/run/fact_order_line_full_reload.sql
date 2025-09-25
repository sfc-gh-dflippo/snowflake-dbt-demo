/*
    Simulate a query for the current year sales orders
    This demonstrates some of the Snowflake specific options
*/
{{ config(
    materialized="incremental",
    merge_exclude_columns = ["DBT_INSERT_TS"],
    pre_hook="{% if is_incremental() %} DELETE FROM {{this}} WHERE SOURCE_SYSTEM_CODE = '{{ env_var('SOURCE_SYSTEM_CODE', 'UNKNOWN') }}' {% endif %}",
    alias='FACT_ORDER_LINE_FULL_RELOAD'
    )
}}

select
    '{{ env_var("SOURCE_SYSTEM_CODE", "UNKNOWN") }}' as source_system_code,
    -- Lookup the surrogate keys for orders and customers
    coalesce(orders.order_key, 0) as l_order_wid,
    coalesce(orders.customer_key, 0) as l_cust_wid,
    lineitem.*,
    lkp_exchange_rates.exchange_rate as eur_conversion_rate,
    {{ integration_key(["lineitem.L_ORDERKEY", "lineitem.L_LINENUMBER"]) }} as integration_id,
    sysdate() as dbt_insert_ts,
    sysdate() as dbt_last_update_ts
from {{ source("TPC_H", "LINEITEM") }} lineitem
-- Joining on the integration key for orders
left outer join {{ ref("dim_orders") }} orders on lineitem.l_orderkey = orders.order_key
left outer join {{ ref("lookup_exchange_rates") }} lkp_exchange_rates on
    lkp_exchange_rates.from_currency = 'USD'
    and lkp_exchange_rates.to_currency = 'EUR'
    and lkp_exchange_rates.day_dt = orders.order_date
