USE DATABASE AdventureWorksDW2022;

CREATE OR REPLACE TABLE dbo.DimOrganization (
    OrganizationKey INT IDENTITY(1,1) ORDER NOT NULL,
    ParentOrganizationKey INT NULL,
    PercentageOfOwnership NVARCHAR(16) COLLATE 'EN-CI-AS' /*** SSC-PRF-0002 - CASE INSENSITIVE COLUMNS CAN DECREASE THE PERFORMANCE OF QUERIES ***/ /*** SSC-FDM-TS0002 - COLLATION FOR VALUE CP1 NOT SUPPORTED ***/ NULL,
    OrganizationName NVARCHAR(50) COLLATE 'EN-CI-AS' /*** SSC-PRF-0002 - CASE INSENSITIVE COLUMNS CAN DECREASE THE PERFORMANCE OF QUERIES ***/ /*** SSC-FDM-TS0002 - COLLATION FOR VALUE CP1 NOT SUPPORTED ***/ NULL,
    CurrencyKey INT NULL,
    CONSTRAINT PK_DimOrganization PRIMARY KEY (OrganizationKey)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 2,  "minor": 42,  "patch": "5-Pr.112" }, "attributes": {  "component": "transact",  "convertedOn": "08/31/2026",  "domain": "no-domain-provided",  "migrationid": "AFqgAYoc4nmXmiUg6NUuiQ==" }}'
;

ALTER TABLE dbo.DimOrganization
    ADD CONSTRAINT FK_DimOrganization_DimCurrency FOREIGN KEY (CurrencyKey) REFERENCES dbo.DimCurrency (CurrencyKey);

ALTER TABLE dbo.DimOrganization
ADD CONSTRAINT FK_DimOrganization_DimOrganization FOREIGN KEY (ParentOrganizationKey) REFERENCES dbo.DimOrganization (OrganizationKey);