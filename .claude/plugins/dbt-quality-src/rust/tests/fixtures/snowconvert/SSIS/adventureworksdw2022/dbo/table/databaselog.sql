USE DATABASE AdventureWorksDW2022;

CREATE OR REPLACE TABLE dbo.DatabaseLog (
    DatabaseLogID INT IDENTITY(1,1) ORDER NOT NULL,
    PostTime TIMESTAMP_NTZ(3) NOT NULL,
    DatabaseUser VARCHAR(128) NOT NULL,
    Event VARCHAR(128) NOT NULL,
    SCHEMA VARCHAR(128) NULL,
    Object VARCHAR(128) NULL,
    TSQL NVARCHAR COLLATE 'EN-CI-AS' /*** SSC-PRF-0002 - CASE INSENSITIVE COLUMNS CAN DECREASE THE PERFORMANCE OF QUERIES ***/ /*** SSC-FDM-TS0002 - COLLATION FOR VALUE CP1 NOT SUPPORTED ***/ NOT NULL,
    XmlEvent VARIANT NOT NULL, -- SSC-EWI-0036: XML converted to VARIANT
    CONSTRAINT PK_DatabaseLog_DatabaseLogID PRIMARY KEY (DatabaseLogID)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 2,  "minor": 42,  "patch": "5-Pr.112" }, "attributes": {  "component": "transact",  "convertedOn": "08/31/2026",  "domain": "no-domain-provided",  "migrationid": "AFqgAYoc4nmXmiUg6NUuiQ==" }}'
;