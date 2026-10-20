{{ config(
    alias='newDimCustomer'
) }}
WITH source_data AS
(
   SELECT
      CustomerKey,
      BirthDateString,
      FirstName,
      AddressLine1,
      AddressLine2
   FROM
      {{ ref('int_lookup_no_match') }}
)
SELECT
   sd.CustomerKey AS CustomerKey,
   sd.BirthDateString AS BirthDateString,
   sd.FirstName :: VARCHAR(152) AS FullName,
   sd.AddressLine1 AS AddressLine2,
   sd.AddressLine2 AS AddressLine1
FROM
   source_data AS sd