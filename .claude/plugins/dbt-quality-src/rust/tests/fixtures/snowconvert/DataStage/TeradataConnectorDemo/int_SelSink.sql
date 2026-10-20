!!!RESOLVE EWI!!! /*** SSC-EWI-DS0002 - IBM DATASTAGE STAGE IS NOT SUPPORTED BY SNOWCONVERT ***/!!!
--BEGIN DSRECORD
--Identifier "V0S17"
--  OLEType "CCustomStage"
--  Readonly "0"
--  Name "SelSink"
--  NextID "1"
--  InputPins "V0S17P1"
--  StageType "PxDataSet"
--  NextRecordID "0"
--END DSRECORD
--BEGIN DSRECORD
--Identifier "V0S17P1"
--  OLEType "CCustomInput"
--  Readonly "0"
--  Name "DSLinkG"
--  Partner "V0S16|V0S16P1"
--END DSRECORD
--
SELECT
   null AS COL1,
   null AS COL2
FROM
   {{ ref('stg_raw__TDSelInput') }}
