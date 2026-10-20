CREATE OR REPLACE TABLE dbo.DeprecatedTasks (
    TaskID INT PRIMARY KEY NOT NULL,
    Title VARCHAR(255) NOT NULL,
    Status VARCHAR(50) NULL,
    CreatedAt TIMESTAMP_NTZ(3) NULL,
    DeprecatedAt TIMESTAMP_NTZ(3) NULL
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 2,  "minor": 46,  "patch": "0-Pr.305" }, "attributes": {  "component": "transact",  "convertedOn": "09/25/2026",  "domain": "no-domain-provided",  "migrationid": "PNugAcH15XaIL/Tn1HztAg==" }}'
;