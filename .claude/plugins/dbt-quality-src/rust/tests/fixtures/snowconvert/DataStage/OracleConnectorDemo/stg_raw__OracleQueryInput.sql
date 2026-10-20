SELECT
   E.EMP_ID,
   D.DEPT_NAME
FROM
   {{ source('raw_InputSchema', 'EMP') }} E,
   {{ source('raw_InputSchema', 'DEPT') }} D
WHERE
   E.DEPT_ID = D.DEPT_ID
   AND seq8() + 1 <= 10