/*
    Simulate a query for the last year of sales orders
*/
{{ config(materialized='table') }}

SELECT *
FROM {{ ref('DIM_ORDERS') }}

-- This filter will limit rows to the last year of orders in the table
WHERE O_ORDERDATE >= (
    SELECT DATEADD(YEAR, -1, DATE_TRUNC('DAY', MAX(O_ORDERDATE)))
    FROM {{ ref('DIM_ORDERS') }}
)

ORDER BY O_ORDERKEY
