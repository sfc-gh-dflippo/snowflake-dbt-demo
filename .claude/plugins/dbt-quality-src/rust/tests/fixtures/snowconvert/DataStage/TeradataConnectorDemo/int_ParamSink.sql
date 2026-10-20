!!!RESOLVE EWI!!! /*** SSC-EWI-DS0002 - IBM DATASTAGE STAGE IS NOT SUPPORTED BY SNOWCONVERT ***/!!!
--BEGIN DSRECORD
--Identifier "V0S3"
--  OLEType "CCustomStage"
--  Readonly "0"
--  Name "ParamSink"
--  NextID "1"
--  InputPins "V0S3P1"
--  StageType "PxDataSet"
--  NextRecordID "0"
--END DSRECORD
--BEGIN DSRECORD
--Identifier "V0S3P1"
--  OLEType "CCustomInput"
--  Readonly "0"
--  Name "DSLink1"
--  Partner "V0S2|V0S2P1"
--END DSRECORD
--
SELECT
   null AS ROUTE_ID
FROM
   {{ ref('stg_raw__TDParamInput') }}