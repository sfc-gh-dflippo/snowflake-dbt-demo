{#- Surrogate key snapshots. run_test.sh enables them with MACROS=improvements. -#}

{% snapshot snap_sk_check_invalidate %}
{{ config(unique_key='id', strategy='check', check_cols=['name', 'amt'], hard_deletes='invalidate',
          meta={'surrogate_key': 'sk'}, enabled=var('surrogate', false)) }}
select * from {{ var('test_database') }}.{{ var('test_schema') }}.SRC
{% endsnapshot %}

{% snapshot snap_sk_ts_new_record %}
{{ config(unique_key='id', strategy='timestamp', updated_at='updated_at', hard_deletes='new_record',
          meta={'surrogate_key': 'sk'}, enabled=var('surrogate', false)) }}
select * from {{ var('test_database') }}.{{ var('test_schema') }}.SRC
{% endsnapshot %}
