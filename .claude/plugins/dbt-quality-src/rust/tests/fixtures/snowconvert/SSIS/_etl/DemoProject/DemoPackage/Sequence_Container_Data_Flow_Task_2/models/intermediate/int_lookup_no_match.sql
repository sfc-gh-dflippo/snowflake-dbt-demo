WITH lookup_reference AS
(
   SELECT
      ProductKey ,
      OrderDateKey ,
      DueDateKey ,
      ShipDateKey ,
      CustomerKey ,
      PromotionKey ,
      CurrencyKey ,
      SalesTerritoryKey ,
      SalesOrderNumber ,
      SalesOrderLineNumber ,
      RevisionNumber ,
      OrderQuantity ,
      UnitPrice ,
      ExtendedAmount ,
      UnitPriceDiscountPct ,
      DiscountAmount ,
      ProductStandardCost ,
      TotalProductCost ,
      SalesAmount ,
      TaxAmt ,
      Freight ,
      CarrierTrackingNumber ,
      CustomerPONumber ,
      OrderDate ,
      DueDate ,
      ShipDate
   FROM
      {{ ref('stg_raw__lookup') }}
),
input_data AS
(
   SELECT
      BirthDateString ,
      CustomerKey ,
      GeographyKey ,
      CustomerAlternateKey ,
      Title ,
      FirstName ,
      MiddleName ,
      LastName ,
      NameStyle ,
      BirthDate ,
      MaritalStatus ,
      Suffix ,
      Gender ,
      EmailAddress ,
      YearlyIncome ,
      TotalChildren ,
      NumberChildrenAtHome ,
      EnglishEducation ,
      SpanishEducation ,
      FrenchEducation ,
      EnglishOccupation ,
      SpanishOccupation ,
      FrenchOccupation ,
      HouseOwnerFlag ,
      NumberCarsOwned ,
      AddressLine1 ,
      AddressLine2 ,
      Phone ,
      DateFirstPurchase ,
      CommuteDistance
   FROM
      {{ ref('int_data_conversion') }}
)
SELECT
   input_data.BirthDateString,
   input_data.CustomerKey,
   input_data.GeographyKey,
   input_data.CustomerAlternateKey,
   input_data.Title,
   input_data.FirstName,
   input_data.MiddleName,
   input_data.LastName,
   input_data.NameStyle,
   input_data.BirthDate,
   input_data.MaritalStatus,
   input_data.Suffix,
   input_data.Gender,
   input_data.EmailAddress,
   input_data.YearlyIncome,
   input_data.TotalChildren,
   input_data.NumberChildrenAtHome,
   input_data.EnglishEducation,
   input_data.SpanishEducation,
   input_data.FrenchEducation,
   input_data.EnglishOccupation,
   input_data.SpanishOccupation,
   input_data.FrenchOccupation,
   input_data.HouseOwnerFlag,
   input_data.NumberCarsOwned,
   input_data.AddressLine1,
   input_data.AddressLine2,
   input_data.Phone,
   input_data.DateFirstPurchase,
   input_data.CommuteDistance
FROM
   input_data
   LEFT JOIN
      lookup_reference
      ON EQUAL_NULL(lookup_reference.CurrencyKey, input_data.CustomerKey)
WHERE
   lookup_reference.CurrencyKey IS NULL