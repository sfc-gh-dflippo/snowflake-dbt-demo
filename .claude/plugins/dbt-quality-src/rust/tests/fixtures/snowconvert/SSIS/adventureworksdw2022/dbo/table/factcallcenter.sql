USE DATABASE AdventureWorksDW2022;

CREATE OR REPLACE TABLE dbo.FactCallCenter (
    FactCallCenterID INT IDENTITY(1,1) ORDER NOT NULL,
    DateKey INT NOT NULL,
    WageType NVARCHAR(15) COLLATE 'EN-CI-AS' /*** SSC-PRF-0002 - CASE INSENSITIVE COLUMNS CAN DECREASE THE PERFORMANCE OF QUERIES ***/ /*** SSC-FDM-TS0002 - COLLATION FOR VALUE CP1 NOT SUPPORTED ***/ NOT NULL,
    Shift NVARCHAR(20) COLLATE 'EN-CI-AS' /*** SSC-PRF-0002 - CASE INSENSITIVE COLUMNS CAN DECREASE THE PERFORMANCE OF QUERIES ***/ /*** SSC-FDM-TS0002 - COLLATION FOR VALUE CP1 NOT SUPPORTED ***/ NOT NULL,
    LevelOneOperators SMALLINT NOT NULL,
    LevelTwoOperators SMALLINT NOT NULL,
    TotalOperators SMALLINT NOT NULL,
    Calls INT NOT NULL,
    AutomaticResponses INT NOT NULL,
    Orders INT NOT NULL,
    IssuesRaised SMALLINT NOT NULL,
    AverageTimePerIssue SMALLINT NOT NULL,
    ServiceGrade FLOAT NOT NULL,
    Date TIMESTAMP_NTZ(3) NULL,
    CONSTRAINT AK_FactCallCenter_DateKey_Shift UNIQUE (DateKey, Shift),
    CONSTRAINT PK_FactCallCenter_FactCallCenterID PRIMARY KEY (FactCallCenterID)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 2,  "minor": 42,  "patch": "5-Pr.112" }, "attributes": {  "component": "transact",  "convertedOn": "08/31/2026",  "domain": "no-domain-provided",  "migrationid": "AFqgAYoc4nmXmiUg6NUuiQ==" }}'
;

ALTER TABLE dbo.FactCallCenter
    ADD CONSTRAINT FK_FactCallCenter_DimDate FOREIGN KEY (DateKey) REFERENCES dbo.DimDate (DateKey);