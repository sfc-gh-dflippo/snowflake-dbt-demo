{{ config(
    materialized='table',
    tags=['intermediate', 'fx_rates'],
    alias='LKP_EXCHANGE_RATES'
) }}

-- Intermediate model: Daily FX rates with business logic
-- Following best practices: business transformations in intermediate layer

with fx_rates_transformed as (
    select
        rate_date as day_dt,
        base_currency as from_currency,
        quote_currency as to_currency,
        exchange_rate as conversion_rate,
        
        -- Business logic: calculate end date for rate validity
        case 
            when lead(rate_date) over (
                partition by base_currency, quote_currency 
                order by rate_date
            ) is not null 
            then dateadd(day, -1, lead(rate_date) over (
                partition by base_currency, quote_currency 
                order by rate_date
            ))
            else date('2099-12-31')
        end as end_date,
        
        _loaded_at

    from {{ ref('stg_economic_essentials__fx_rates') }}
    where base_currency = 'USD'  -- Focus on USD base rates
)

select * from fx_rates_transformed
