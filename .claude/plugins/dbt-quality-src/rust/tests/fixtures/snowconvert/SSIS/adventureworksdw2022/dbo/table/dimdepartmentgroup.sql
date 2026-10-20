USE DATABASE AdventureWorksDW2022;

CREATE OR REPLACE TABLE dbo.DimDepartmentGroup (
    DepartmentGroupKey INT IDENTITY(1,1) ORDER NOT NULL,
    ParentDepartmentGroupKey INT NULL,
    DepartmentGroupName NVARCHAR(50) COLLATE 'EN-CI-AS' /*** SSC-PRF-0002 - CASE INSENSITIVE COLUMNS CAN DECREASE THE PERFORMANCE OF QUERIES ***/ /*** SSC-FDM-TS0002 - COLLATION FOR VALUE CP1 NOT SUPPORTED ***/ NULL,
    CONSTRAINT PK_DimDepartmentGroup PRIMARY KEY (DepartmentGroupKey)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 2,  "minor": 42,  "patch": "5-Pr.112" }, "attributes": {  "component": "transact",  "convertedOn": "08/31/2026",  "domain": "no-domain-provided",  "migrationid": "AFqgAYoc4nmXmiUg6NUuiQ==" }}'
;

ALTER TABLE dbo.DimDepartmentGroup
    ADD CONSTRAINT FK_DimDepartmentGroup_DimDepartmentGroup FOREIGN KEY (ParentDepartmentGroupKey) REFERENCES dbo.DimDepartmentGroup (DepartmentGroupKey);