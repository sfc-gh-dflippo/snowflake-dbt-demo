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
    C_CUSTKEY,
    C_NAME,
    C_ADDRESS,
    C_NATIONKEY,
    C_PHONE,
    C_ACCTBAL,
    C_MKTSEGMENT,
    C_COMMENT,
    CURRENT_TIMESTAMP() AS C_LAST_UPDATE_DATE
from
    {{ source('TPC_H', 'CUSTOMER') }}

{% if is_incremental() %}
    -- The following will randomly pick 10% of the rows
    sample (10)
{% endif %}
