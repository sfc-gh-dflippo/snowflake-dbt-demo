{{ config(
    materialized='incremental',
    unique_key='C_CUSTKEY',
    pre_hook=[
        "{% if not is_incremental() %} drop stream if exists {{this.database}}.{{this.schema}}.{{this.identifier}}_ST {% endif %}"
    ],
    post_hook=[
        "create stream if not exists {{this.database}}.{{this.schema}}.{{this.identifier}}_ST on table {{this}} SHOW_INITIAL_ROWS = TRUE"
    ]
    )
}}
select
    c_custkey,
    c_name,
    c_address,
    c_nationkey,
    c_phone,
    c_acctbal,
    c_mktsegment,
    c_comment,
    current_timestamp() as c_last_update_date
from
    {{ source('TPC_H', 'CUSTOMER') }}

    {% if is_incremental() %}
    -- The following will randomly pick 10% of the rows
        sample (10)
    {% endif %}
