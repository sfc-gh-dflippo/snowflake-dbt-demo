-- TST007: singular test that should be generic (simple null check)
select count(*)
from {{ ref('dim_customers') }}
where customer_sk is null
having count(*) > 0
