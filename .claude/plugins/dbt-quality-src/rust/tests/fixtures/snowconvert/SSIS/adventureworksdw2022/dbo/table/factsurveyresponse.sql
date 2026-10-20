USE DATABASE AdventureWorksDW2022;

CREATE OR REPLACE TABLE dbo.FactSurveyResponse (
    SurveyResponseKey INT IDENTITY(1,1) ORDER NOT NULL,
    DateKey INT NOT NULL,
    CustomerKey INT NOT NULL,
    ProductCategoryKey INT NOT NULL,
    EnglishProductCategoryName NVARCHAR(50) COLLATE 'EN-CI-AS' /*** SSC-PRF-0002 - CASE INSENSITIVE COLUMNS CAN DECREASE THE PERFORMANCE OF QUERIES ***/ /*** SSC-FDM-TS0002 - COLLATION FOR VALUE CP1 NOT SUPPORTED ***/ NOT NULL,
    ProductSubcategoryKey INT NOT NULL,
    EnglishProductSubcategoryName NVARCHAR(50) COLLATE 'EN-CI-AS' /*** SSC-PRF-0002 - CASE INSENSITIVE COLUMNS CAN DECREASE THE PERFORMANCE OF QUERIES ***/ /*** SSC-FDM-TS0002 - COLLATION FOR VALUE CP1 NOT SUPPORTED ***/ NOT NULL,
    Date TIMESTAMP_NTZ(3) NULL,
    CONSTRAINT PK_FactSurveyResponse_SurveyResponseKey PRIMARY KEY (SurveyResponseKey)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 2,  "minor": 42,  "patch": "5-Pr.112" }, "attributes": {  "component": "transact",  "convertedOn": "08/31/2026",  "domain": "no-domain-provided",  "migrationid": "AFqgAYoc4nmXmiUg6NUuiQ==" }}'
;

ALTER TABLE dbo.FactSurveyResponse
    ADD CONSTRAINT FK_FactSurveyResponse_CustomerKey FOREIGN KEY (CustomerKey) REFERENCES dbo.DimCustomer (CustomerKey);

ALTER TABLE dbo.FactSurveyResponse
ADD CONSTRAINT FK_FactSurveyResponse_DateKey FOREIGN KEY (DateKey) REFERENCES dbo.DimDate (DateKey);