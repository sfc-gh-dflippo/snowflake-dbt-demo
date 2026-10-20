--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "dimCustomer" **
SELECT
   *
FROM
   {{ source('raw', 'dimCustomer') }}
WHERE
   BirthDate < '1970-01-01 00:00:00'