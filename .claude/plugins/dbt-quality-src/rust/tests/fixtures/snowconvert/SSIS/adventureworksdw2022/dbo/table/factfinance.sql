USE DATABASE AdventureWorksDW2022;

CREATE OR REPLACE TABLE dbo.FactFinance (
    FinanceKey INT IDENTITY(1,1) ORDER NOT NULL,
    DateKey INT NOT NULL,
    OrganizationKey INT NOT NULL,
    DepartmentGroupKey INT NOT NULL,
    ScenarioKey INT NOT NULL,
    AccountKey INT NOT NULL,
    Amount FLOAT NOT NULL,
    Date TIMESTAMP_NTZ(3) NULL
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 2,  "minor": 42,  "patch": "5-Pr.112" }, "attributes": {  "component": "transact",  "convertedOn": "08/31/2026",  "domain": "no-domain-provided",  "migrationid": "AFqgAYoc4nmXmiUg6NUuiQ==" }}'
;

ALTER TABLE dbo.FactFinance
    ADD CONSTRAINT FK_FactFinance_DimAccount FOREIGN KEY (AccountKey) REFERENCES dbo.DimAccount (AccountKey);

ALTER TABLE dbo.FactFinance
ADD CONSTRAINT FK_FactFinance_DimDate FOREIGN KEY (DateKey) REFERENCES dbo.DimDate (DateKey);

ALTER TABLE dbo.FactFinance
ADD CONSTRAINT FK_FactFinance_DimDepartmentGroup FOREIGN KEY (DepartmentGroupKey) REFERENCES dbo.DimDepartmentGroup (DepartmentGroupKey);

ALTER TABLE dbo.FactFinance
ADD CONSTRAINT FK_FactFinance_DimOrganization FOREIGN KEY (OrganizationKey) REFERENCES dbo.DimOrganization (OrganizationKey);

ALTER TABLE dbo.FactFinance
ADD CONSTRAINT FK_FactFinance_DimScenario FOREIGN KEY (ScenarioKey) REFERENCES dbo.DimScenario (ScenarioKey);