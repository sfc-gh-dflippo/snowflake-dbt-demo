-- ARC003: source() used outside staging layer
-- SQL005: SELECT * outside staging
-- SQL006: hardcoded table reference
-- SQL007: implicit comma join
-- SQL011: no CTE structure (has join + aggregate)
-- SQL012: UNION without ALL
-- SQL013: SELECT DISTINCT
select distinct
    c.customer_id,
    c.first_name,
    o.order_id,
    o.amount
from {{ source('raw', 'customers') }} c, {{ ref('stg_orders') }} o
where c.customer_id = o.customer_id

union

select
    customer_id,
    first_name,
    order_id,
    amount
from analytics.staging.archived_orders
