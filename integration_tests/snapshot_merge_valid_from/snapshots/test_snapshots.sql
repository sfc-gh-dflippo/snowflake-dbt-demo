{#- One snapshot per strategy and hard_deletes mode. All read the same source table. -#}

{% snapshot snap_ts_ignore %}
{{ config(unique_key='id', strategy='timestamp', updated_at='updated_at') }}
select * from {{ var('test_database') }}.{{ var('test_schema') }}.SRC
{% endsnapshot %}

{% snapshot snap_check_invalidate %}
{{ config(unique_key='id', strategy='check', check_cols=['name', 'amt'], hard_deletes='invalidate') }}
select * from {{ var('test_database') }}.{{ var('test_schema') }}.SRC
{% endsnapshot %}

{% snapshot snap_ts_new_record %}
{{ config(unique_key='id', strategy='timestamp', updated_at='updated_at', hard_deletes='new_record') }}
select * from {{ var('test_database') }}.{{ var('test_schema') }}.SRC
{% endsnapshot %}

{% snapshot snap_ts_valid_to_current %}
{{ config(unique_key='id', strategy='timestamp', updated_at='updated_at',
          dbt_valid_to_current="to_timestamp_ntz('9999-12-31')") }}
select * from {{ var('test_database') }}.{{ var('test_schema') }}.SRC
{% endsnapshot %}

{% snapshot snap_check_composite_key %}
{{ config(unique_key=['id', 'grp'], strategy='check', check_cols='all', hard_deletes='invalidate') }}
select * from {{ var('test_database') }}.{{ var('test_schema') }}.SRC
{% endsnapshot %}

{% snapshot snap_ts_renamed_cols %}
{{ config(unique_key='id', strategy='timestamp', updated_at='updated_at', hard_deletes='new_record',
          snapshot_meta_column_names={'dbt_valid_from': 'valid_from', 'dbt_valid_to': 'valid_to',
                                      'dbt_scd_id': 'scd_id', 'dbt_updated_at': 'row_updated_at',
                                      'dbt_is_deleted': 'is_deleted'}) }}
select * from {{ var('test_database') }}.{{ var('test_schema') }}.SRC
{% endsnapshot %}
