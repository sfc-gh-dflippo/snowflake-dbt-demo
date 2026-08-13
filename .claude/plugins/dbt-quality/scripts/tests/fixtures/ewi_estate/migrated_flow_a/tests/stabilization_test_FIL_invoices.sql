-- MIG006: stabilization_test scaffolding in test
-- tags: stabilization_test
select count(*)
from {{ ref('FIL_invoices') }}
having count(*) <> 42
