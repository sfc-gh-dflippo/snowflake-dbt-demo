/*
 Queries in the sensitive folder will be created as secure views
 */
select
    c_custkey,
    c_name,
    c_mktsegment,
    c_comment,
    c_active_customer_flag,
    c_open_order_cusotmer_flag
from {{ ref('DIM_CUSTOMERS') }}
