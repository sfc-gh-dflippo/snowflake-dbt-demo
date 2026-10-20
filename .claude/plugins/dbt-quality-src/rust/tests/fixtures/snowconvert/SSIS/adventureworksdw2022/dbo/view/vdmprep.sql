USE DATABASE AdventureWorksDW2022;

-- vDMPrep will be used as a data source by the other data mining views.  
-- Uses DW data at customer, product, day, etc. granularity and
-- gets region, model, year, month, etc.
CREATE OR REPLACE VIEW dbo.vDMPrep
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 2,  "minor": 42,  "patch": "5-Pr.112" }, "attributes": {  "component": "transact",  "convertedOn": "08/31/2026",  "domain": "no-domain-provided",  "migrationid": "AFqgAYoc4nmXmiUg6NUuiQ==" }}'
AS
SELECT
    pc.EnglishProductCategoryName
    ,
    COALESCE(p.ModelName, p.EnglishProductName) AS Model
    ,
    c.CustomerKey
    ,
    s.SalesTerritoryGroup AS Region
    ,CASE
        WHEN Month(CURRENT_TIMESTAMP() :: TIMESTAMP) < Month(c.BirthDate :: TIMESTAMP)
            THEN DATEDIFF(year, c.BirthDate, CURRENT_TIMESTAMP() :: TIMESTAMP) - 1
        WHEN Month(CURRENT_TIMESTAMP() :: TIMESTAMP) = Month(c.BirthDate :: TIMESTAMP)
        AND Day(CURRENT_TIMESTAMP() :: TIMESTAMP) < Day(c.BirthDate :: TIMESTAMP)
            THEN DATEDIFF(year, c.BirthDate, CURRENT_TIMESTAMP() :: TIMESTAMP) - 1
        ELSE DATEDIFF(year, c.BirthDate, CURRENT_TIMESTAMP() :: TIMESTAMP)
    END AS Age
    ,CASE
        WHEN c.YearlyIncome < 40000 THEN 'Low'
        WHEN c.YearlyIncome > 60000 THEN 'High'
        ELSE 'Moderate'
    END AS IncomeGroup
    ,
    d.CalendarYear
    ,
    d.FiscalYear
    ,
    d.MonthNumberOfYear AS Month
    ,
    f.SalesOrderNumber AS OrderNumber
    ,
    f.SalesOrderLineNumber AS LineNumber
    ,
    f.OrderQuantity AS Quantity
    ,
    f.ExtendedAmount AS Amount
FROM
    dbo.FactInternetSales f
INNER JOIN
        dbo.DimDate d
    ON f.OrderDateKey = d.DateKey
INNER JOIN
        dbo.DimProduct p
    ON f.ProductKey = p.ProductKey
INNER JOIN
        dbo.DimProductSubcategory psc
    ON p.ProductSubcategoryKey = psc.ProductSubcategoryKey
INNER JOIN
        dbo.DimProductCategory pc
    ON psc.ProductCategoryKey = pc.ProductCategoryKey
INNER JOIN
        dbo.DimCustomer c
    ON f.CustomerKey = c.CustomerKey
INNER JOIN
        dbo.DimGeography g
    ON c.GeographyKey = g.GeographyKey
INNER JOIN
        dbo.DimSalesTerritory s
    ON g.SalesTerritoryKey = s.SalesTerritoryKey
        ;