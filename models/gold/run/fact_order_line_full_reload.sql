{#- dbt-quality: ignore-file SSC-EWI-DBTINC0002, SSC-PRF-DBTINC0005, SSC-EWI-DBTARC0003 -#}
{#-
    Simulate a query for the current year sales orders
    This demonstrates some of the Snowflake specific options

    DELIBERATE PATTERN - delete by less than the unique key.

    The pre_hook removes the entire SOURCE_SYSTEM_CODE slice before the insert
    reloads it. Deleting at a coarser grain than the row key is what lets this
    model account for deletes: a line that disappeared upstream is gone from the
    target, because the whole slice was removed first. A merge on
    (source_system_code, l_orderkey, l_linenumber) cannot do that - it restates
    matched rows and leaves absent ones behind.

    The slice delete is also what makes the load idempotent, so no unique_key is
    needed and none should be added. Do not "fix" this into a merge or a
    delete+insert strategy. INC0002 and INC0005 are waived above because they
    flag this pattern, which is the pattern the model exists to demonstrate.
    ARC0003 is waived because the model reads raw LINEITEM columns (L_ORDERKEY)
    on purpose; stg_tpc_h__lineitem renames them.
-#}

{{ config(
    incremental_strategy="append",
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
