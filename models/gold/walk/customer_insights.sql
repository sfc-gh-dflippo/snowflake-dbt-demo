{{ config(
    materialized='table',
    tags=['gold', 'walk', 'analytics']
) }}

-- GOLD WALK: Customer analytics for business intelligence
-- Complexity: Intermediate - Business metrics, KPIs, user-friendly views
-- Features demonstrated: Grants, business KPIs, user-friendly naming

with customer_base as (
    select
        cs.*,
        cn.nation_name,
        cn.government_type
    from {{ ref('customer_segments') }} cs
    left join {{ ref('clean_nations') }} cn
        on cs.nation_key = cn.nation_key
)

select
    -- Customer identifiers
    customer_key,
    customer_name,
    nation_name as country,

    -- Financial metrics
    account_balance,
    avg_nation_balance as country_average_balance,
    balance_vs_nation_avg as balance_vs_country_average,

    -- Segmentation
    customer_segment as customer_tier,
    market_segment,
    nation_ranking as country_ranking,
    statistical_class as statistical_classification,

    -- Performance metrics
    round(balance_percentile * 100, 1) as balance_percentile_score,
    balance_rank_in_nation as rank_in_country,

    -- Derived insights
    case
        when customer_segment = 'PREMIUM' and nation_ranking = 'TOP_10_IN_NATION'
        then 'VIP Customer'
        when customer_segment in ('PREMIUM', 'HIGH_VALUE')
        then 'High Value Customer'
        when statistical_class = 'ABOVE_AVERAGE'
        then 'Above Average Customer'
        else 'Standard Customer'
    end as customer_classification,

    -- Risk indicators
    case
        when account_balance < 0 then 'Credit Risk'
        when customer_segment = 'LOW_VALUE' then 'Retention Risk'
        when balance_vs_nation_avg < -1000 then 'Performance Risk'
        else 'Low Risk'
    end as risk_category,

    processed_at as last_updated

from customer_base
order by account_balance desc
