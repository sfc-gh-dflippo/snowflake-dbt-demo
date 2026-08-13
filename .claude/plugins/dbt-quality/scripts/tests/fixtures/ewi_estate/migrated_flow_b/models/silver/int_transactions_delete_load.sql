-- INC002: pre-hook deletes from own table
{{ config(
    materialized='table',
    pre_hook="delete from {{ this }} where transaction_date >= dateadd(day, -7, current_date())"
) }}

select
    transaction_id,
    account_id,
    amount,
    transaction_date
from {{ ref('stg_transactions') }}
where transaction_date >= dateadd(day, -7, current_date())
