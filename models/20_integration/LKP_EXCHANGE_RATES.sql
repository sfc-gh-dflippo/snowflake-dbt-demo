/*
    This model will figure out the exchange rates between many different currencies
*/
{{ config(
    materialized='table'
) }}
with exch_rates as (
    select
        ex_rates.quote_currency_id as currency,
        ex_rates.value as from_usd,
        (1 / from_usd) as to_usd,
        -- The start date is the day after the previous close
        coalesce(lag(dateadd(day, 1, DATE), 1) over (partition by currency order by DATE asc), '1900-01-01'::date) as start_date,
        case -- when it is the last row, make the end date tomorrow to ensure we can't lose same-day records
            when lag(dateadd(day, 1, DATE), -1) over (partition by currency order by DATE asc) is null then dateadd(year, 100, current_date())
            else DATE
        end as end_date
    from {{ source('ECONOMIC_ESSENTIALS', 'FX_RATES_TIMESERIES') }} ex_rates
    where
        base_currency_id = 'USD'
        and quote_currency_id in ('EUR')
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
    first_rate.to_usd * second_rate.from_usd as conversion_rate,
    first_rate.from_usd * second_rate.to_usd as inverse_conversion_rate
from {{ ref('DIM_CALENDAR_DAY') }} as cal_day
inner join exch_rates as first_rate on cal_day.day_dt between first_rate.start_date and first_rate.end_date
inner join exch_rates as second_rate on cal_day.day_dt between second_rate.start_date and second_rate.end_date

