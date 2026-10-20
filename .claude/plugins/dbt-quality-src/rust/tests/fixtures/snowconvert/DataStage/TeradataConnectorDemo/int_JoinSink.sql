!!!RESOLVE EWI!!! /*** SSC-EWI-DS0002 - IBM DATASTAGE STAGE IS NOT SUPPORTED BY SNOWCONVERT ***/!!!
--BEGIN DSRECORD
--Identifier "V0S11"
--  OLEType "CCustomStage"
--  Readonly "0"
--  Name "JoinSink"
--  NextID "1"
--  InputPins "V0S11P1"
--  StageType "PxDataSet"
--  NextRecordID "0"
--END DSRECORD
--BEGIN DSRECORD
--Identifier "V0S11P1"
--  OLEType "CCustomInput"
--  Readonly "0"
--  Name "DSLinkD"
--  Partner "V0S10|V0S10P1"
--END DSRECORD
--
SELECT
   null AS COL1,
   null AS COL2
FROM
   {{ ref('stg_raw__TDJoinInput') }}