-- ARC005 trigger: bronze model incorrectly depends on gold model dim_customers
-- The ref() call below creates the dependency on dim_customers
select *
from {{ ref('dim_customers') }}
