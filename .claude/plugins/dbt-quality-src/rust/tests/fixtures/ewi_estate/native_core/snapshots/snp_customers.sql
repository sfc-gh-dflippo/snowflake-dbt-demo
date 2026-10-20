-- TST009: snapshot with incomplete config (missing updated_at for timestamp strategy)
{% snapshot snp_customers %}

{{ config(
    target_schema='snapshots',
    unique_key='customer_id',
    strategy='timestamp'
) }}

select * from {{ source('raw', 'customers') }}

{% endsnapshot %}
