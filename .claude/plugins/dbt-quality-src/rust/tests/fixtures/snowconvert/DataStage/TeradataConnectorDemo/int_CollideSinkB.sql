!!!RESOLVE EWI!!! /*** SSC-EWI-DS0002 - IBM DATASTAGE STAGE IS NOT SUPPORTED BY SNOWCONVERT ***/!!!
--BEGIN DSRECORD
--Identifier "V0S7"
--  OLEType "CCustomStage"
--  Readonly "0"
--  Name "CollideSinkB"
--  NextID "1"
--  InputPins "V0S7P1"
--  StageType "PxDataSet"
--  NextRecordID "0"
--END DSRECORD
--BEGIN DSRECORD
--Identifier "V0S7P1"
--  OLEType "CCustomInput"
--  Readonly "0"
--  Name "DSLinkB"
--  Partner "V0S6|V0S6P1"
--END DSRECORD
--
SELECT
   null AS COL_B
FROM
   {{ ref('stg_raw__tdcollide') }}