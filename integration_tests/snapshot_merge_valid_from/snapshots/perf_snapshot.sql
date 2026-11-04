{#- Large snapshot for run_perf.sh only. run_perf.sh creates the target and source tables first. -#}
{% snapshot snap_big %}
{{ config(unique_key='id', strategy='timestamp', updated_at='updated_at', enabled=var('perf', false)) }}
select * from {{ var('test_database') }}.{{ var('test_schema') }}.BIG_SRC
{% endsnapshot %}
