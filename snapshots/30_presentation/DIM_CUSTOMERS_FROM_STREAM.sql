{% snapshot DIM_CUSTOMERS_STREAM_SCD %}
{{
    config(
        unique_key='c_custkey',
        strategy='timestamp',
        updated_at='c_last_update_date')
}}
/*
Type 2 Customers dimension based on stream and simulated CDC
    */
    select
        -- Use the customer_cdc_stream model with column aliases to match snapshot table structure
        customer_cdc_stream.CUSTOMER_KEY as c_custkey,
        customer_cdc_stream.CUSTOMER_NAME as c_name,
        customer_cdc_stream.ACCOUNT_BALANCE as c_acctbal,
        customer_cdc_stream."METADATA$ACTION",
        customer_cdc_stream."METADATA$ISUPDATE",
        customer_cdc_stream."METADATA$ROW_ID",
        current_timestamp() as c_last_update_date,
        iff(customer_cdc_stream."METADATA$ACTION" = 'DELETE', 'Y', 'N') as delete_flag
    from {{ ref('customer_cdc_stream') }} as customer_cdc_stream

    -- We do not want the DELETE rows from the stream for updates
    where not (customer_cdc_stream."METADATA$ACTION" = 'DELETE' and customer_cdc_stream."METADATA$ISUPDATE")

    -- It is possible the same key was deleted and inserted
    -- The following will deduplicate records, keeping the newest record and keeping INSERT over DELETE
    qualify 1 = row_number() over (partition by customer_cdc_stream.CUSTOMER_KEY order by c_last_update_date desc, customer_cdc_stream."METADATA$ACTION" desc)

{% endsnapshot %}
