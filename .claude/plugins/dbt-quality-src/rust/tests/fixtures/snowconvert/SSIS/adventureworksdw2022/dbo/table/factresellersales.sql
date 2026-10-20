USE DATABASE AdventureWorksDW2022;

CREATE OR REPLACE TABLE dbo.FactResellerSales (
    ProductKey INT NOT NULL,
    OrderDateKey INT NOT NULL,
    DueDateKey INT NOT NULL,
    ShipDateKey INT NOT NULL,
    ResellerKey INT NOT NULL,
    EmployeeKey INT NOT NULL,
    PromotionKey INT NOT NULL,
    CurrencyKey INT NOT NULL,
    SalesTerritoryKey INT NOT NULL,
    SalesOrderNumber NVARCHAR(20) COLLATE 'EN-CI-AS' /*** SSC-PRF-0002 - CASE INSENSITIVE COLUMNS CAN DECREASE THE PERFORMANCE OF QUERIES ***/ /*** SSC-FDM-TS0002 - COLLATION FOR VALUE CP1 NOT SUPPORTED ***/ NOT NULL,
    SalesOrderLineNumber TINYINT NOT NULL,
    RevisionNumber TINYINT NULL,
    OrderQuantity SMALLINT NULL,
    UnitPrice NUMBER(38, 4) NULL,
    ExtendedAmount NUMBER(38, 4) NULL,
    UnitPriceDiscountPct FLOAT NULL,
    DiscountAmount FLOAT NULL,
    ProductStandardCost NUMBER(38, 4) NULL,
    TotalProductCost NUMBER(38, 4) NULL,
    SalesAmount NUMBER(38, 4) NULL,
    TaxAmt NUMBER(38, 4) NULL,
    Freight NUMBER(38, 4) NULL,
    CarrierTrackingNumber NVARCHAR(25) COLLATE 'EN-CI-AS' /*** SSC-PRF-0002 - CASE INSENSITIVE COLUMNS CAN DECREASE THE PERFORMANCE OF QUERIES ***/ /*** SSC-FDM-TS0002 - COLLATION FOR VALUE CP1 NOT SUPPORTED ***/ NULL,
    CustomerPONumber NVARCHAR(25) COLLATE 'EN-CI-AS' /*** SSC-PRF-0002 - CASE INSENSITIVE COLUMNS CAN DECREASE THE PERFORMANCE OF QUERIES ***/ /*** SSC-FDM-TS0002 - COLLATION FOR VALUE CP1 NOT SUPPORTED ***/ NULL,
    OrderDate TIMESTAMP_NTZ(3) NULL,
    DueDate TIMESTAMP_NTZ(3) NULL,
    ShipDate TIMESTAMP_NTZ(3) NULL,
    CONSTRAINT PK_FactResellerSales_SalesOrderNumber_SalesOrderLineNumber PRIMARY KEY (SalesOrderNumber, SalesOrderLineNumber)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 2,  "minor": 42,  "patch": "5-Pr.112" }, "attributes": {  "component": "transact",  "convertedOn": "08/31/2026",  "domain": "no-domain-provided",  "migrationid": "AFqgAYoc4nmXmiUg6NUuiQ==" }}'
;

ALTER TABLE dbo.FactResellerSales
    ADD CONSTRAINT FK_FactResellerSales_DimCurrency FOREIGN KEY (CurrencyKey) REFERENCES dbo.DimCurrency (CurrencyKey);

ALTER TABLE dbo.FactResellerSales
ADD CONSTRAINT FK_FactResellerSales_DimDate FOREIGN KEY (OrderDateKey) REFERENCES dbo.DimDate (DateKey);

ALTER TABLE dbo.FactResellerSales
ADD CONSTRAINT FK_FactResellerSales_DimDate1 FOREIGN KEY (DueDateKey) REFERENCES dbo.DimDate (DateKey);

ALTER TABLE dbo.FactResellerSales
ADD CONSTRAINT FK_FactResellerSales_DimDate2 FOREIGN KEY (ShipDateKey) REFERENCES dbo.DimDate (DateKey);

ALTER TABLE dbo.FactResellerSales
ADD CONSTRAINT FK_FactResellerSales_DimEmployee FOREIGN KEY (EmployeeKey) REFERENCES dbo.DimEmployee (EmployeeKey);

ALTER TABLE dbo.FactResellerSales
ADD CONSTRAINT FK_FactResellerSales_DimProduct FOREIGN KEY (ProductKey) REFERENCES dbo.DimProduct (ProductKey);

ALTER TABLE dbo.FactResellerSales
ADD CONSTRAINT FK_FactResellerSales_DimPromotion FOREIGN KEY (PromotionKey) REFERENCES dbo.DimPromotion (PromotionKey);

ALTER TABLE dbo.FactResellerSales
ADD CONSTRAINT FK_FactResellerSales_DimReseller FOREIGN KEY (ResellerKey) REFERENCES dbo.DimReseller (ResellerKey);

ALTER TABLE dbo.FactResellerSales
ADD CONSTRAINT FK_FactResellerSales_DimSalesTerritory FOREIGN KEY (SalesTerritoryKey) REFERENCES dbo.DimSalesTerritory (SalesTerritoryKey);