{{ config(
    alias='newDimCustomer'
) }}
WITH source_data AS
(
   SELECT
      CustomerKey,
      BirthDateString,
      FullName,
      AddressLine1,
      AddressLine2
   FROM
      {{ ref('int_derived_column') }}
)
SELECT
   sd.CustomerKey AS CustomerKey,
   sd.BirthDateString AS BirthDateString,
   sd.FullName AS FullName,
   sd.AddressLine1 AS AddressLine2,
   sd.AddressLine2 AS AddressLine1
FROM
   source_data AS sd