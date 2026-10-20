USE DATABASE AdventureWorksDW2022;

CREATE OR REPLACE TABLE dbo.FactInternetSalesReason (
    SalesOrderNumber NVARCHAR(20) COLLATE 'EN-CI-AS' /*** SSC-PRF-0002 - CASE INSENSITIVE COLUMNS CAN DECREASE THE PERFORMANCE OF QUERIES ***/ /*** SSC-FDM-TS0002 - COLLATION FOR VALUE CP1 NOT SUPPORTED ***/ NOT NULL,
    SalesOrderLineNumber TINYINT NOT NULL,
    SalesReasonKey INT NOT NULL,
    CONSTRAINT PK_FactInternetSalesReason_SalesOrderNumber_SalesOrderLineNumber_SalesReasonKey PRIMARY KEY (SalesOrderNumber, SalesOrderLineNumber, SalesReasonKey)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 2,  "minor": 42,  "patch": "5-Pr.112" }, "attributes": {  "component": "transact",  "convertedOn": "08/31/2026",  "domain": "no-domain-provided",  "migrationid": "AFqgAYoc4nmXmiUg6NUuiQ==" }}'
;

ALTER TABLE dbo.FactInternetSalesReason
    ADD CONSTRAINT FK_FactInternetSalesReason_DimSalesReason FOREIGN KEY (SalesReasonKey) REFERENCES dbo.DimSalesReason (SalesReasonKey);

ALTER TABLE dbo.FactInternetSalesReason
ADD CONSTRAINT FK_FactInternetSalesReason_FactInternetSales FOREIGN KEY (SalesOrderNumber, SalesOrderLineNumber) REFERENCES dbo.FactInternetSales (SalesOrderNumber, SalesOrderLineNumber);