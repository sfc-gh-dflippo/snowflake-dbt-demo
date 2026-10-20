USE DATABASE AdventureWorksDW2022;

-- vTargetMail supports targeted mailing data model
-- Uses vDMPrep to determine if a customer buys a bike and joins to DimCustomer
CREATE OR REPLACE VIEW dbo.vTargetMail
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 2,  "minor": 42,  "patch": "5-Pr.112" }, "attributes": {  "component": "transact",  "convertedOn": "08/31/2026",  "domain": "no-domain-provided",  "migrationid": "AFqgAYoc4nmXmiUg6NUuiQ==" }}'
AS
SELECT
    c.CustomerKey,
    c.GeographyKey,
    c.CustomerAlternateKey,
    c.Title,
    c.FirstName,
    c.MiddleName,
    c.LastName,
    c.NameStyle,
    c.BirthDate,
    c.MaritalStatus,
    c.Suffix,
    c.Gender,
    c.EmailAddress,
    c.YearlyIncome,
    c.TotalChildren,
    c.NumberChildrenAtHome,
    c.EnglishEducation,
    c.SpanishEducation,
    c.FrenchEducation,
    c.EnglishOccupation,
    c.SpanishOccupation,
    c.FrenchOccupation,
    c.HouseOwnerFlag,
    c.NumberCarsOwned,
    c.AddressLine1,
    c.AddressLine2,
    c.Phone,
    c.DateFirstPurchase,
    c.CommuteDistance,
    x.Region,
    x.Age,
    CASE
        x.Bikes
        WHEN 0 THEN 0
        ELSE 1
    END AS BikeBuyer
FROM
    dbo.DimCustomer c
    INNER JOIN (
        SELECT
                CustomerKey
            ,
                Region
            ,
                Age
            ,
                SUM(
                CASE
                    EnglishProductCategoryName
                    WHEN 'Bikes' THEN 1
                    ELSE 0
                END) AS Bikes
        FROM
                dbo.vDMPrep
        GROUP BY
                CustomerKey
            ,
                Region
            ,
                Age
        ) AS x
    ON c.CustomerKey = x.CustomerKey
                ;