/*
    Use the `ref` function to select from other models
    Because we aren't overriding the materialization, it will be a view by default
*/
select *
from {{ ref('DIM_CURRENT_YEAR_ORDERS') }}
where o_orderstatus = 'O'
