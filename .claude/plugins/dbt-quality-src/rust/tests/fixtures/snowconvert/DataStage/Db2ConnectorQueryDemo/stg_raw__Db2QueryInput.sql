SELECT
   E.EMP_ID,
   D.DEPT_NAME,
   CURRENT_TIMESTAMP() AS EXTRACT_DATE
FROM
   {{ source('raw_InputSchema', 'EMP') }} E,
   {{ source('raw_InputSchema', 'DEPT') }} D
WHERE
   E.DEPT_ID = D.DEPT_ID
