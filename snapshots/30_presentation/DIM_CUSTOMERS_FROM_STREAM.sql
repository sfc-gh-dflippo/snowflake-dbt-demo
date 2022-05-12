{% snapshot DIM_CUSTOMERS_STREAM_SCD %}

{{
    config(
      unique_key='C_CUSTKEY',
      strategy='timestamp',
      updated_at='C_LAST_UPDATE_DATE'
    )
}}

/*
Type 2 Customers dimension based on stream and simulated CDC
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
    END AS C_OPEN_ORDER_CUSOTMER_FLAG,
    C_LAST_UPDATE_DATE
FROM {{ source('SNOWFLAKE_TABLE_STREAM', 'customer_cdc_st') }}
    LEFT OUTER JOIN {{ ref('LKP_CUSTOMERS_WITH_ORDERS') }} ON ( O_CUSTKEY = C_CUSTKEY )

-- We do not want the DELETE rows from the stream for updates
WHERE NOT (METADATA$ACTION = 'DELETE' AND METADATA$ISUPDATE)

-- It is possible the same key was deleted and inserted
-- The following will deduplicate records, keeping the newest record and keeping INSERT over DELETE
qualify 1 = row_number() over (partition by C_CUSTKEY order by C_LAST_UPDATE_DATE DESC, METADATA$ACTION DESC)

{% endsnapshot %}
