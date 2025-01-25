{% snapshot DIM_CUSTOMERS_STREAM_SCD %}
{{
    config(
        unique_key='integration_id',
        strategy='timestamp',
        updated_at='dim_customers_updated_ts')
}}
/*
Type 2 Customers dimension based on stream and simulated CDC
    */
    select
        -- We need to rename the upstream dbt_updated_ts so it won't conflict with the snapshot column
        dim_customers_st.* RENAME (dbt_updated_ts AS dim_customers_updated_ts),
        iff(dim_customers_st.metadata$action = 'DELETE', 'Y', 'N') as delete_flag
    from {{ get_stream( ref('DIM_CUSTOMERS') ) }} as dim_customers_st

    -- We do not want the DELETE rows from the stream for updates
    where not (dim_customers_st.metadata$action = 'DELETE' and dim_customers_st.metadata$isupdate)

    -- It is possible the same key was deleted and inserted
    -- The following will deduplicate records, keeping the newest record and keeping INSERT over DELETE
    qualify 1 = row_number() over (partition by dim_customers_st.c_custkey order by dim_customers_st.dbt_updated_ts desc, dim_customers_st.metadata$action desc)

{% endsnapshot %}
