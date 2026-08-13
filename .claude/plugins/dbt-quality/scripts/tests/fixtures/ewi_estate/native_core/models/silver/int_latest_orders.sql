-- SQL001: derived-table subquery in FROM
-- SQL003: deeply nested subqueries
-- SQL004: window function wrapper instead of QUALIFY
-- SQL008: non-deterministic ORDER BY
-- SQL009: generic CTE name
-- SQL010: unused CTE
select *
from (
    select *,
        row_number() over (
            partition by customer_id
            order by (select null)
        ) as rn
    from (
        select customer_id, order_id, amount
        from {{ ref('stg_orders') }}
        where amount > 0
    ) sub_inner
) ranked
where rn = 1
