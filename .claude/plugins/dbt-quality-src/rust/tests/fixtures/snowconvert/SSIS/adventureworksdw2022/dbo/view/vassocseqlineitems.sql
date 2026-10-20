USE DATABASE AdventureWorksDW2022;

CREATE OR REPLACE VIEW dbo.vAssocSeqLineItems
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 2,  "minor": 42,  "patch": "5-Pr.112" }, "attributes": {  "component": "transact",  "convertedOn": "08/31/2026",  "domain": "no-domain-provided",  "migrationid": "AFqgAYoc4nmXmiUg6NUuiQ==" }}'
AS
SELECT
OrderNumber,
LineNumber,
Model
FROM
dbo.vDMPrep
WHERE     (FiscalYear = '2013');