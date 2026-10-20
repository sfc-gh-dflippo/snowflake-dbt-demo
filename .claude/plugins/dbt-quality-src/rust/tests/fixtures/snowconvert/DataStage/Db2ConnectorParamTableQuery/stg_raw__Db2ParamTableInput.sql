/* {{ var('pvSQLID', 'pvSQLID') }}-Db2ParamTableInput */ SELECT
   E.EMP_ID
FROM
   {{ source('raw_pvDB2Schema', 'jpTableName01') }} E
WHERE
   E.EMP_ID = '{{ var('jpRegion', 'jpRegion') }}'