{% snapshot DIM_CUSTOMERS_SCD %}

{{
    config(
      unique_key='integration_id',
      strategy='check',
      check_cols=['cdc_hash_key'],
      dbt_current_flag_column='dbt_current_flag',
      surrogate_key='dim_customers_scd_wid',
      invalidate_hard_deletes=true
    )
}}

/*
Type 2 Customers dimension based on name and flags
    */
    select
        customer.c_custkey,
        customer.c_name,
        customer.c_address,
        customer.c_nationkey,
        customer.c_phone,
        customer.c_acctbal,
        customer.c_mktsegment,
        customer.c_comment,
        case
            when lkp_customers_with_orders.order_count > 0 then 'Y'
            else 'Y'
        end as c_active_customer_flag,
        case
            when lkp_customers_with_orders.open_order_count > 0 then 'Y'
            else 'N'
        end as c_open_order_customer_flag,
        customer.c_custkey as integration_id,
        hash(customer.c_name, c_active_customer_flag, c_open_order_customer_flag) as cdc_hash_key
    from {{ source('TPC_H', 'CUSTOMER') }} as customer
    left outer join {{ ref('LKP_CUSTOMERS_WITH_ORDERS') }} as lkp_customers_with_orders on
        lkp_customers_with_orders.o_custkey = customer.c_custkey

{% endsnapshot %}
