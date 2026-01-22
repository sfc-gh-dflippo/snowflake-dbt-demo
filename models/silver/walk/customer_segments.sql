{{ config(
    materialized='table',
    tags=['silver', 'walk', 'business_logic'],
    indexes=[
        {'columns': ['customer_segment'], 'type': 'hash'},
        {'columns': ['nation_key'], 'type': 'hash'}
    ]
) }}

-- SILVER WALK: Business logic and segmentation
-- Complexity: Intermediate - CTEs, window functions, business rules
-- Features demonstrated: CTEs, window functions, complex case statements

with customer_metrics as (
    select
        c_custkey,
        c_name,
        c_nationkey,
        c_acctbal,
        c_mktsegment,

        -- Window functions for ranking
        row_number() over (partition by c_nationkey order by c_acctbal desc) as balance_rank_in_nation,
        percent_rank() over (order by c_acctbal) as balance_percentile,

        -- Statistical measures
        avg(c_acctbal) over (partition by c_nationkey) as avg_nation_balance,
        stddev(c_acctbal) over (partition by c_nationkey) as stddev_nation_balance

    from {{ ref('stg_customers_with_tests') }}
    where data_quality_flag = 'VALID'
),

segmented_customers as (
    select
        *,
        -- Complex segmentation logic
        case
            when balance_percentile >= 0.9 then 'PREMIUM'
            when balance_percentile >= 0.7 then 'HIGH_VALUE'
            when balance_percentile >= 0.3 then 'STANDARD'
            when balance_percentile >= 0.1 then 'BASIC'
            else 'LOW_VALUE'
        end as customer_segment,

        -- Nation-specific ranking
        case
            when balance_rank_in_nation <= 10 then 'TOP_10_IN_NATION'
            when balance_rank_in_nation <= 100 then 'TOP_100_IN_NATION'
            else 'STANDARD_IN_NATION'
        end as nation_ranking,

        -- Statistical classification
        case
            when c_acctbal > (avg_nation_balance + stddev_nation_balance) then 'ABOVE_AVERAGE'
            when c_acctbal < (avg_nation_balance - stddev_nation_balance) then 'BELOW_AVERAGE'
            else 'AVERAGE'
        end as statistical_class

    from customer_metrics
)

select
    c_custkey as customer_key,
    c_name as customer_name,
    c_nationkey as nation_key,
    c_acctbal as account_balance,
    c_mktsegment as market_segment,
    customer_segment,
    nation_ranking,
    statistical_class,
    balance_percentile,
    balance_rank_in_nation,

    -- Derived business metrics
    round(avg_nation_balance, 2) as avg_nation_balance,
    round(c_acctbal - avg_nation_balance, 2) as balance_vs_nation_avg,

    current_timestamp() as processed_at

from segmented_customers
