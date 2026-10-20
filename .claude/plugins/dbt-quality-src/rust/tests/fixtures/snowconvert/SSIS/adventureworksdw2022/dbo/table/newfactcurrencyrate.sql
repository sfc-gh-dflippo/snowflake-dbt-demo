USE DATABASE AdventureWorksDW2022;

CREATE OR REPLACE TABLE dbo.NewFactCurrencyRate (
    AverageRate REAL NULL,
    CurrencyID NVARCHAR(3) COLLATE 'EN-CI-AS' /*** SSC-PRF-0002 - CASE INSENSITIVE COLUMNS CAN DECREASE THE PERFORMANCE OF QUERIES ***/ /*** SSC-FDM-TS0002 - COLLATION FOR VALUE CP1 NOT SUPPORTED ***/ NULL,
    CurrencyDate DATE NULL,
    EndOfDayRate REAL NULL,
    CurrencyKey INT NULL,
    DateKey INT NULL
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 2,  "minor": 42,  "patch": "5-Pr.112" }, "attributes": {  "component": "transact",  "convertedOn": "08/31/2026",  "domain": "no-domain-provided",  "migrationid": "AFqgAYoc4nmXmiUg6NUuiQ==" }}'
;