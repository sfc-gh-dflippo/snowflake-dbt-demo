!!!RESOLVE EWI!!! /*** SSC-EWI-DS0002 - IBM DATASTAGE STAGE IS NOT SUPPORTED BY SNOWCONVERT ***/!!!
--BEGIN DSRECORD
--Identifier "V0S15"
--  OLEType "CCustomStage"
--  Readonly "0"
--  Name "LockingSink"
--  NextID "1"
--  InputPins "V0S15P1"
--  StageType "PxDataSet"
--  NextRecordID "0"
--END DSRECORD
--BEGIN DSRECORD
--Identifier "V0S15P1"
--  OLEType "CCustomInput"
--  Readonly "0"
--  Name "DSLinkF"
--  Partner "V0S14|V0S14P1"
--END DSRECORD
--
SELECT
   null AS COL1,
   null AS COL2
FROM
   {{ ref('stg_raw__TDLockingInput') }}
