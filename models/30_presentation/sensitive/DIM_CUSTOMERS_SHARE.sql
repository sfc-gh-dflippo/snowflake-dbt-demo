/*
 Queries in the sensitive folder will be created as secure views
 */
SELECT C_CUSTKEY,
    C_NAME,
    C_MKTSEGMENT,
    C_COMMENT,
    C_ACTIVE_CUSTOMER_FLAG,
    C_OPEN_ORDER_CUSOTMER_FLAG
FROM {{ ref('DIM_CUSTOMERS') }}
