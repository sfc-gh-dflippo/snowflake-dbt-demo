USE DATABASE SampleStoreDB;

CREATE OR REPLACE TABLE Store.Categories (
    CategoryID INT IDENTITY(1,1) ORDER NOT NULL,
    CategoryName NVARCHAR(200) COLLATE 'EN-CI-AS' /*** SSC-PRF-0002 - CASE INSENSITIVE COLUMNS CAN DECREASE THE PERFORMANCE OF QUERIES ***/ /*** SSC-FDM-TS0002 - COLLATION FOR VALUE CP1 NOT SUPPORTED ***/ NOT NULL,
    Description NVARCHAR(1000) COLLATE 'EN-CI-AS' /*** SSC-PRF-0002 - CASE INSENSITIVE COLUMNS CAN DECREASE THE PERFORMANCE OF QUERIES ***/ /*** SSC-FDM-TS0002 - COLLATION FOR VALUE CP1 NOT SUPPORTED ***/ NULL,
    IsActive BOOLEAN NULL DEFAULT true,
    CreatedDate TIMESTAMP_NTZ(3) NULL DEFAULT (CURRENT_TIMESTAMP() :: TIMESTAMP_NTZ(3)),
    ModifiedDate TIMESTAMP_NTZ(3) NULL
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 2,  "minor": 10,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "02/26/2026",  "domain": "no-domain-provided",  "migrationid": "j5ucAW36yneHx8K6CNvJhw==" }}'
;