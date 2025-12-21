-- Singular test: Ensure customer balance distribution is reasonable
-- This test will fail if more than 10% of customers have negative balances

select
    'negative_balance_check' as test_name,
    count(*) as negative_balance_customers,
    (select count(*) from {{ source('TPC_H', 'CUSTOMER') }}) as total_customers,
    round((count(*)::float / (select count(*) from {{ source('TPC_H', 'CUSTOMER') }})) * 100, 2) as negative_balance_percentage

from {{ source('TPC_H', 'CUSTOMER') }}
where c_acctbal < 0

having negative_balance_percentage > 10
