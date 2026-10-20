CREATE OR REPLACE TABLE dbo.Employees (
    EmployeeID INT PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Email VARCHAR(200) NOT NULL UNIQUE,
    Department VARCHAR(100),
    HireDate DATE NOT NULL DEFAULT CURRENT_DATE(),
    IsActive BOOLEAN DEFAULT true
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 2,  "minor": 46,  "patch": "0-Pr.305" }, "attributes": {  "component": "transact",  "convertedOn": "09/25/2026",  "domain": "no-domain-provided",  "migrationid": "PNugAcH15XaIL/Tn1HztAg==" }}'
;