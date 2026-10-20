USE DATABASE AdventureWorksDW2022;

CREATE OR REPLACE TABLE dbo.sysdiagrams (
    name VARCHAR(128) NOT NULL,
    principal_id INT NOT NULL,
    diagram_id INT IDENTITY(1,1) ORDER NOT NULL,
    version INT NULL,
    definition VARBINARY NULL,
    CONSTRAINT PK__sysdiagr__C2B05B616B24EA82 PRIMARY KEY (diagram_id)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 2,  "minor": 42,  "patch": "5-Pr.112" }, "attributes": {  "component": "transact",  "convertedOn": "08/31/2026",  "domain": "no-domain-provided",  "migrationid": "AFqgAYoc4nmXmiUg6NUuiQ==" }}'
;