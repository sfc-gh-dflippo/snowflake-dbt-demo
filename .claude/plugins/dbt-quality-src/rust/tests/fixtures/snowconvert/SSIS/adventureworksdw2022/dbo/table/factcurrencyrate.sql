USE DATABASE AdventureWorksDW2022;

CREATE OR REPLACE TABLE dbo.FactCurrencyRate (
    CurrencyKey INT NOT NULL,
    DateKey INT NOT NULL,
    AverageRate FLOAT NOT NULL,
    EndOfDayRate FLOAT NOT NULL,
    Date TIMESTAMP_NTZ(3) NULL,
    CONSTRAINT PK_FactCurrencyRate_CurrencyKey_DateKey PRIMARY KEY (CurrencyKey, DateKey)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 2,  "minor": 42,  "patch": "5-Pr.112" }, "attributes": {  "component": "transact",  "convertedOn": "08/31/2026",  "domain": "no-domain-provided",  "migrationid": "AFqgAYoc4nmXmiUg6NUuiQ==" }}'
;

ALTER TABLE dbo.FactCurrencyRate
    ADD CONSTRAINT FK_FactCurrencyRate_DimCurrency FOREIGN KEY (CurrencyKey) REFERENCES dbo.DimCurrency (CurrencyKey);

ALTER TABLE dbo.FactCurrencyRate
ADD CONSTRAINT FK_FactCurrencyRate_DimDate FOREIGN KEY (DateKey) REFERENCES dbo.DimDate (DateKey);