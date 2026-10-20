!!!RESOLVE EWI!!! /*** SSC-EWI-DS0002 - IBM DATASTAGE STAGE IS NOT SUPPORTED BY SNOWCONVERT ***/!!!
--BEGIN DSRECORD
--Identifier "V0S5"
--  OLEType "CCustomStage"
--  Readonly "0"
--  Name "CollideSinkA"
--  NextID "1"
--  InputPins "V0S5P1"
--  StageType "PxDataSet"
--  NextRecordID "0"
--END DSRECORD
--BEGIN DSRECORD
--Identifier "V0S5P1"
--  OLEType "CCustomInput"
--  Readonly "0"
--  Name "DSLinkA"
--  Partner "V0S4|V0S4P1"
--END DSRECORD
--
SELECT
   null AS COL_A
FROM
   {{ ref('stg_raw__TDCollide') }}