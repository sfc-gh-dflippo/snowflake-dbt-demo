-- ARC005 trigger: bronze model incorrectly depends on gold model dim_customers
-- Requires manifest entry with depends_on.nodes pointing to dim_customers
select *
from {{ ref('dim_customers') }}
