!!!RESOLVE EWI!!! /*** SSC-EWI-DS0002 - IBM DATASTAGE STAGE IS NOT SUPPORTED BY SNOWCONVERT ***/!!!
--BEGIN DSRECORD
--Identifier "V0S19"
--  OLEType "CCustomStage"
--  Readonly "0"
--  Name "CommentSink"
--  NextID "1"
--  InputPins "V0S19P1"
--  StageType "PxDataSet"
--  NextRecordID "0"
--END DSRECORD
--BEGIN DSRECORD
--Identifier "V0S19P1"
--  OLEType "CCustomInput"
--  Readonly "0"
--  Name "DSLinkH"
--  Partner "V0S18|V0S18P1"
--END DSRECORD
--
SELECT
   null AS COL1,
   null AS COL2
FROM
   {{ ref('stg_raw__TDCommentInput') }}
