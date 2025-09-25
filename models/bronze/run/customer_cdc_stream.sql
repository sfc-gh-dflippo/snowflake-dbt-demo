{{ config(
    materialized='incremental',
    unique_key='customer_key',
    pre_hook=[
        "{% if not is_incremental() %} drop stream if exists {{this.database}}.{{this.schema}}.{{this.identifier}}_ST {% endif %}"
    ],
    post_hook=[
        "create stream if not exists {{this.database}}.{{this.schema}}.{{this.identifier}}_ST on table {{this}} SHOW_INITIAL_ROWS = TRUE"
    ]
    )
}}
select
    c_custkey as customer_key,
    c_name as customer_name,
    c_acctbal as account_balance,
    'INSERT' as "METADATA$ACTION",
    false as "METADATA$ISUPDATE",
    c_custkey::varchar as "METADATA$ROW_ID"
from
    {{ source('TPC_H', 'CUSTOMER') }}

    {% if is_incremental() %}
    -- The following will randomly pick 10% of the rows
        sample (10)
    {% endif %}
