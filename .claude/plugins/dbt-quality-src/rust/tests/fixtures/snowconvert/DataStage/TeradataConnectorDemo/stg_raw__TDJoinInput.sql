SELECT
   A.COL1,
   B.COL2
FROM
   {{ source('raw_DbParams_schema', 'TABLE_A') }} A,
   {{ source('raw_DbParams_schema', 'TABLE_B') }} B
WHERE
   A.ID = B.ID