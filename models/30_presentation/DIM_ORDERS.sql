
/*
    Simulate a query for the sales orders
    Because we aren't overriding the materialization, it will be a view by default
*/

SELECT O_ORDERKEY,
    O_CUSTKEY,
    O_ORDERSTATUS,
    O_TOTALPRICE,
    O_ORDERDATE,
    O_ORDERPRIORITY,
    O_CLERK,
    O_SHIPPRIORITY,
    O_COMMENT
FROM
{{ source('TPC_H', 'ORDERS') }}

-- Uncomment this line to cause a FK violation
--LIMIT 100
