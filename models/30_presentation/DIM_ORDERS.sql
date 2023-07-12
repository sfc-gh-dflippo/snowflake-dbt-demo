{%- set wid_col_name = "O_ORDER_WID" -%}
{{ config(
    materialized = "incremental",
    unique_key=wid_col_name,
    merge_exclude_columns = [wid_col_name, "DBT_INSERT_TS"],
    transient=false,
    post_hook=[ "{%- do insert_ghost_key( 'O_ORDER_WID', 0,
        {'O_CUST_WID': '0'}
    ) -%}" ]
    )
}}
/*
    Simulate a query for the sales orders
*/
WITH INCOMING_DATA AS (

    SELECT
        COALESCE(C_CUST_WID, 0) AS O_CUST_WID,
        O_ORDERSTATUS,
        O_TOTALPRICE,
        O_ORDERDATE,
        O_ORDERPRIORITY,
        O_CLERK,
        O_SHIPPRIORITY,
        O_COMMENT,
        O_CUSTKEY,
        O_ORDERKEY,
        {{ surrogate_key(["O_ORDERKEY"]) }} AS INTEGRATION_ID,
        HASH(O_CUST_WID,
            O_ORDERSTATUS,
            O_TOTALPRICE,
            O_ORDERDATE,
            O_ORDERPRIORITY,
            O_CLERK,
            O_SHIPPRIORITY,
            O_COMMENT,
            O_CUSTKEY) AS CDC_HASH_KEY
    FROM
    {{ source("TPC_H", "ORDERS") }} O
    LEFT OUTER JOIN {{ ref("DIM_CUSTOMERS") }} C on C.C_CUSTKEY = O.O_CUSTKEY

    {%- if is_incremental() %}
    -- this filter will only be applied on an incremental run
    WHERE O_ORDERDATE >= DATEADD(DAY, -90, SYSDATE() )
        OR O_ORDERSTATUS = 'O'
    {%- endif %}

),

EXISTING_KEYS AS (
    {%- if is_incremental() %}
    SELECT {{ wid_col_name }} EXISTING_WID, INTEGRATION_ID, CDC_HASH_KEY FROM {{ this }}
    {%- else -%}
    SELECT NULL::INTEGER EXISTING_WID, NULL::VARCHAR INTEGRATION_ID, NULL::INTEGER CDC_HASH_KEY
    LIMIT 0
    {%- endif %}
)

SELECT
    COALESCE(EXISTING_WID, {{ sequence_get_nextval() }} ) AS {{ wid_col_name }},
    D.*,
    SYSDATE() as DBT_INSERT_TS,
    SYSDATE() as DBT_LAST_UPDATE_TS
FROM INCOMING_DATA D
LEFT OUTER JOIN EXISTING_KEYS ON D.INTEGRATION_ID = EXISTING_KEYS.INTEGRATION_ID
WHERE EXISTING_KEYS.INTEGRATION_ID IS NULL
    OR EXISTING_KEYS.CDC_HASH_KEY <> D.CDC_HASH_KEY


-- Uncomment this line to cause a FK violation
--LIMIT 100
