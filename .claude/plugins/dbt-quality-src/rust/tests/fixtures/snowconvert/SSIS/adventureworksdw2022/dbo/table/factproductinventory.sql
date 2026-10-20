USE DATABASE AdventureWorksDW2022;

CREATE OR REPLACE TABLE dbo.FactProductInventory (
    ProductKey INT NOT NULL,
    DateKey INT NOT NULL,
    MovementDate DATE NOT NULL,
    UnitCost NUMBER(38, 4) NOT NULL,
    UnitsIn INT NOT NULL,
    UnitsOut INT NOT NULL,
    UnitsBalance INT NOT NULL,
    CONSTRAINT PK_FactProductInventory PRIMARY KEY (ProductKey, DateKey)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 2,  "minor": 42,  "patch": "5-Pr.112" }, "attributes": {  "component": "transact",  "convertedOn": "08/31/2026",  "domain": "no-domain-provided",  "migrationid": "AFqgAYoc4nmXmiUg6NUuiQ==" }}'
;

ALTER TABLE dbo.FactProductInventory
    ADD CONSTRAINT FK_FactProductInventory_DimDate FOREIGN KEY (DateKey) REFERENCES dbo.DimDate (DateKey);

ALTER TABLE dbo.FactProductInventory
ADD CONSTRAINT FK_FactProductInventory_DimProduct FOREIGN KEY (ProductKey) REFERENCES dbo.DimProduct (ProductKey);