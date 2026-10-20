-- INC001: pre-hook truncates own table
-- INC010: post-hook writes to another table
{{ config(
    materialized='table',
    pre_hook="truncate table {{ this }}",
    post_hook="insert into analytics.audit.load_log select '{{ this }}', current_timestamp()"
) }}

select
    transaction_id,
    account_id,
    amount,
    transaction_date
from {{ ref('stg_transactions') }}
