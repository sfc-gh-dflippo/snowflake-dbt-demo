USE DATABASE AdventureWorksDW2022;

CREATE OR REPLACE TABLE dbo.DimProductSubcategory (
    ProductSubcategoryKey INT IDENTITY(1,1) ORDER NOT NULL,
    ProductSubcategoryAlternateKey INT NULL,
    EnglishProductSubcategoryName NVARCHAR(50) COLLATE 'EN-CI-AS' /*** SSC-PRF-0002 - CASE INSENSITIVE COLUMNS CAN DECREASE THE PERFORMANCE OF QUERIES ***/ /*** SSC-FDM-TS0002 - COLLATION FOR VALUE CP1 NOT SUPPORTED ***/ NOT NULL,
    SpanishProductSubcategoryName NVARCHAR(50) COLLATE 'EN-CI-AS' /*** SSC-PRF-0002 - CASE INSENSITIVE COLUMNS CAN DECREASE THE PERFORMANCE OF QUERIES ***/ /*** SSC-FDM-TS0002 - COLLATION FOR VALUE CP1 NOT SUPPORTED ***/ NOT NULL,
    FrenchProductSubcategoryName NVARCHAR(50) COLLATE 'EN-CI-AS' /*** SSC-PRF-0002 - CASE INSENSITIVE COLUMNS CAN DECREASE THE PERFORMANCE OF QUERIES ***/ /*** SSC-FDM-TS0002 - COLLATION FOR VALUE CP1 NOT SUPPORTED ***/ NOT NULL,
    ProductCategoryKey INT NULL,
    CONSTRAINT AK_DimProductSubcategory_ProductSubcategoryAlternateKey UNIQUE (ProductSubcategoryAlternateKey),
    CONSTRAINT PK_DimProductSubcategory_ProductSubcategoryKey PRIMARY KEY (ProductSubcategoryKey)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 2,  "minor": 42,  "patch": "5-Pr.112" }, "attributes": {  "component": "transact",  "convertedOn": "08/31/2026",  "domain": "no-domain-provided",  "migrationid": "AFqgAYoc4nmXmiUg6NUuiQ==" }}'
;

ALTER TABLE dbo.DimProductSubcategory
    ADD CONSTRAINT FK_DimProductSubcategory_DimProductCategory FOREIGN KEY (ProductCategoryKey) REFERENCES dbo.DimProductCategory (ProductCategoryKey);