--** SSC-FDM-DS0006 - DATASTAGE JOB PARAMETER 'pRunDate' HAS NO DECLARED VALUE AT CONVERSION TIME; IT IS DECLARED EMPTY IN dbt_project.yml. SUPPLY A VALUE UNDER vars: BEFORE RUNNING. **
SELECT
   RecordType,
   Data
FROM
   {{ ref('stg_flat_file__Src') }}
WHERE
   RecordType = '{{ var('pRunDate', 'pRunDate') }}'
