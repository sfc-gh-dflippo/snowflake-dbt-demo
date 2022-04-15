{% snapshot DIM_CUSTOMERS_SCD %}

{{
    config(
      unique_key='C_CUSTKEY',
      strategy='check',
      check_cols=['C_NAME', 'C_ACTIVE_CUSTOMER_FLAG', 'C_OPEN_ORDER_CUSOTMER_FLAG'],
    )
}}

/*
Type 2 Customers dimension based on name and flags
 */
SELECT C_CUSTKEY,
    C_NAME,
    C_ADDRESS,
    C_NATIONKEY,
    C_PHONE,
    C_ACCTBAL,
    C_MKTSEGMENT,
    C_COMMENT,
    CASE
        WHEN ORDER_COUNT > 0 THEN 'Y'
        ELSE 'Y'
    END AS C_ACTIVE_CUSTOMER_FLAG,
    CASE
        WHEN OPEN_ORDER_COUNT > 0 THEN 'Y'
        ELSE 'N'
    END AS C_OPEN_ORDER_CUSOTMER_FLAG
FROM {{ source('TPC_H', 'CUSTOMER') }}
    LEFT OUTER JOIN {{ ref('LKP_CUSTOMERS_WITH_ORDERS') }} ON ( O_CUSTKEY = C_CUSTKEY )

{% endsnapshot %}
