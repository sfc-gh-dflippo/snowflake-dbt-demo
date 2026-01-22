{{ config(
    tags=['staging', 'economic_essentials']
) }}

-- Staging model for Economic Essentials FX_RATES_TIMESERIES source
-- One-to-one relationship with source, basic cleaning and renaming

with source as (
    select * from {{ source('ECONOMIC_ESSENTIALS', 'FX_RATES_TIMESERIES') }}
),

renamed as (
    select
        -- Keys
        DATE as rate_date,
        BASE_CURRENCY_ID as base_currency,
        QUOTE_CURRENCY_ID as quote_currency,

        -- Attributes
        VALUE as exchange_rate,

        -- Audit columns
        current_timestamp() as _loaded_at

    from source
)

select * from renamed
