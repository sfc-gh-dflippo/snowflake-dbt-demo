!!!RESOLVE EWI!!! /*** SSC-EWI-DS0002 - IBM DATASTAGE STAGE IS NOT SUPPORTED BY SNOWCONVERT ***/!!!
--BEGIN DSRECORD
--Identifier "V0S1"
--  OLEType "CCustomStage"
--  Readonly "0"
--  Name "QuerySink"
--  NextID "1"
--  InputPins "V0S1P1"
--  StageType "PxDataSet"
--  NextRecordID "0"
--END DSRECORD
--BEGIN DSRECORD
--Identifier "V0S1P1"
--  OLEType "CCustomInput"
--  Readonly "0"
--  Name "DSLink0"
--  Partner "V0S0|V0S0P1"
--END DSRECORD
--
SELECT
   null AS EMP_ID
FROM
   {{ ref('stg_raw__OdbcQueryInput') }}