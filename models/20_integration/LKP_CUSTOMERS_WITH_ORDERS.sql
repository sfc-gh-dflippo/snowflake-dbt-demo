{{ config(materialized = 'ephemeral') }}
/*
 List of customers and how many orders they have
 */
SELECT O_CUSTKEY,
    count(*) as ORDER_COUNT,
    sum(
        case
            when O_ORDERSTATUS = 'O' THEN 1
            ELSE 0
        END
    ) AS OPEN_ORDER_COUNT
FROM {{ source('TPC_H', 'ORDERS') }}
GROUP BY 1
