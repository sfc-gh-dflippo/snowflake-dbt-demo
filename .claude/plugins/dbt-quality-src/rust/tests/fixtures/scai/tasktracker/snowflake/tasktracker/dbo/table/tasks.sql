CREATE OR REPLACE TABLE dbo.Tasks (
    TaskID INT PRIMARY KEY,
    Title VARCHAR(200) NOT NULL,
    Description VARCHAR(1000),
    AssigneeID INT NOT NULL REFERENCES dbo.Employees (EmployeeID),
    Priority VARCHAR(10) DEFAULT 'Medium',
    Status VARCHAR(20) DEFAULT 'Open',
    CreatedAt TIMESTAMP_NTZ(3) NOT NULL DEFAULT CURRENT_TIMESTAMP() :: TIMESTAMP_NTZ(3),
    DueDate DATE,
    CompletedAt TIMESTAMP_NTZ(3),
    CONSTRAINT CK_Tasks_Priority CHECK (Priority IN ('Low', 'Medium', 'High')),
    CONSTRAINT CK_Tasks_Status CHECK (Status IN ('Open', 'In Progress', 'Done', 'Cancelled'))
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 2,  "minor": 46,  "patch": "0-Pr.305" }, "attributes": {  "component": "transact",  "convertedOn": "09/25/2026",  "domain": "no-domain-provided",  "migrationid": "PNugAcH15XaIL/Tn1HztAg==" }}'
;