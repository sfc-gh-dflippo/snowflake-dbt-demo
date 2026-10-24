{#- dbt-quality: ignore-file SSC-EWI-DBTARC0005, SSC-EWI-DBTARC0003 -#}
{#- Legacy input of the fact_order_line_full_reload demo. int_fx_rates__daily replaces it for new models. -#}
/*
    This model will figure out the exchange rates between many different currencies
*/
{{ config(
    materialized='table',
    alias='LKP_EXCHANGE_RATES_LEGACY'
) }}
with exch_rates as (
    select
        ex_rates.quote_currency as currency,
        ex_rates.exchange_rate as from_usd,
        (1 / from_usd) as to_usd,
        -- The start date is the day after the previous close
        coalesce(lag(dateadd(day, 1, rate_date), 1) over (partition by currency order by rate_date asc), '1900-01-01'::date) as start_date,
        case -- when it is the last row, make the end date tomorrow to ensure we can't lose same-day records
            when lag(dateadd(day, 1, rate_date), -1) over (partition by currency order by rate_date asc) is null then dateadd(year, 100, current_date())
            else rate_date
        end as end_date
    from {{ ref('stg_economic_essentials__fx_rates') }} ex_rates
    where
        base_currency = 'USD'
        and quote_currency in ('EUR')
    union all -- JUST IN CASE THE LOCAL CURRENCY IS USD
    select
        'USD',
        1,
        1,
        '1900-01-01'::date,
        dateadd(year, 100, current_date())
)

select
    cal_day.day_dt,
    first_rate.currency as from_currency,
    second_rate.currency as to_currency,
    first_rate.to_usd * second_rate.from_usd as exchange_rate,
    first_rate.from_usd * second_rate.to_usd as inverse_conversion_rate
-- dbt-quality: ignore SSC-EWI-DBTARC0005 (dim_calendar_day is a generated calendar with no source; this legacy lookup is a demo of a silver-to-gold edge)
from {{ ref('dim_calendar_day') }} as cal_day
inner join exch_rates as first_rate on cal_day.day_dt between first_rate.start_date and first_rate.end_date
inner join exch_rates as second_rate on cal_day.day_dt between second_rate.start_date and second_rate.end_date
