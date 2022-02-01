
-- Use the `ref` function to select from other models

select *
from {{ ref('DIM_CURRENT_YEAR_ORDERS') }}
where O_ORDERSTATUS = 'O'
