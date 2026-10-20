USE DATABASE AdventureWorksDW2022;

CREATE OR REPLACE TABLE dbo.FactSalesQuota (
    SalesQuotaKey INT IDENTITY(1,1) ORDER NOT NULL,
    EmployeeKey INT NOT NULL,
    DateKey INT NOT NULL,
    CalendarYear SMALLINT NOT NULL,
    CalendarQuarter TINYINT NOT NULL,
    SalesAmountQuota NUMBER(38, 4) NOT NULL,
    Date TIMESTAMP_NTZ(3) NULL,
    CONSTRAINT PK_FactSalesQuota_SalesQuotaKey PRIMARY KEY (SalesQuotaKey)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 2,  "minor": 42,  "patch": "5-Pr.112" }, "attributes": {  "component": "transact",  "convertedOn": "08/31/2026",  "domain": "no-domain-provided",  "migrationid": "AFqgAYoc4nmXmiUg6NUuiQ==" }}'
;

ALTER TABLE dbo.FactSalesQuota
    ADD CONSTRAINT FK_FactSalesQuota_DimDate FOREIGN KEY (DateKey) REFERENCES dbo.DimDate (DateKey);

ALTER TABLE dbo.FactSalesQuota
ADD CONSTRAINT FK_FactSalesQuota_DimEmployee FOREIGN KEY (EmployeeKey) REFERENCES dbo.DimEmployee (EmployeeKey);