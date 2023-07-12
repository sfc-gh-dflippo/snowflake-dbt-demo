{{ config(
    materialized = "incremental",
    unique_key="C_CUST_WID",
    merge_exclude_columns = ["C_CUST_WID", "DBT_INSERT_TS"],
    transient=false,
    post_hook=[ "{%- do insert_ghost_key( 'C_CUST_WID', 0,
        {'C_CUSTKEY': '0',
         'C_NAME': \"'Unknown'\",
         'C_ACTIVE_CUSTOMER_FLAG': \"'N'\",
         'C_OPEN_ORDER_CUSOTMER_FLAG': \"'N'\"}
    ) -%}" ]
    )
}}
/*
 All Customers
 */
WITH INCOMING_DATA AS (

    SELECT
        C_NAME,
        C_ADDRESS,
        C_NATIONKEY,
        C_PHONE,
        C_ACCTBAL,
        C_MKTSEGMENT,
        C_COMMENT,
        CASE
            WHEN LKP.ORDER_COUNT > 0 THEN 'Y'
            ELSE 'N'
        END AS C_ACTIVE_CUSTOMER_FLAG,
        CASE
            WHEN LKP.OPEN_ORDER_COUNT > 0 THEN 'Y'
            ELSE 'N'
        END AS C_OPEN_ORDER_CUSOTMER_FLAG,
        C_CUSTKEY,

        {{ surrogate_key(["C_CUSTKEY"]) }} AS INTEGRATION_ID,
        HASH(C_NAME,
            C_ADDRESS,
            C_NATIONKEY,
            C_PHONE,
            C_ACCTBAL,
            C_MKTSEGMENT,
            C_COMMENT,
            C_ACTIVE_CUSTOMER_FLAG,
            C_OPEN_ORDER_CUSOTMER_FLAG) AS CDC_HASH_KEY
    FROM {{ source("TPC_H", "CUSTOMER") }} C
    LEFT OUTER JOIN {{ ref("LKP_CUSTOMERS_WITH_ORDERS") }} LKP ON ( LKP.O_CUSTKEY = C.C_CUSTKEY )
    -- Ideally we would have a filter here to limit changes based on a source table timestamp

),

EXISTING_KEYS AS (
    {%- if is_incremental() %}
    SELECT C_CUST_WID EXISTING_WID, INTEGRATION_ID, CDC_HASH_KEY FROM {{ this }}
    {%- else -%}
    SELECT NULL::INTEGER EXISTING_WID, NULL::VARCHAR INTEGRATION_ID, NULL::INTEGER CDC_HASH_KEY
    LIMIT 0
    {%- endif %}
)

SELECT
    COALESCE(EXISTING_WID, {{ sequence_get_nextval() }} ) AS C_CUST_WID,
    D.*,
    SYSDATE() as DBT_INSERT_TS,
    SYSDATE() as DBT_LAST_UPDATE_TS
FROM INCOMING_DATA D
LEFT OUTER JOIN EXISTING_KEYS ON D.INTEGRATION_ID = EXISTING_KEYS.INTEGRATION_ID
WHERE EXISTING_KEYS.INTEGRATION_ID IS NULL
    OR EXISTING_KEYS.CDC_HASH_KEY <> D.CDC_HASH_KEY
