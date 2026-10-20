-- <copyright file="ssis_read_control_flow_config_from_stage.sql" company="Snowflake Inc">
--        Copyright (c) 2019-2025 Snowflake Inc. All rights reserved.
-- </copyright>

-- ==========================================================================
-- DESCRIPTION: READ_CONTROL_FLOW_CONFIG_FROM_STAGE(file_stage_path VARCHAR)
--   Loads the configuration generated for the current package that details the tables 
--   that need to be measured after the execution of each task. The procedure reads an 
--   XML configuration file from a Snowflake stage, parses the task-to-table mappings, 
--   and populates the CONTROL_FLOW_TABLE_USAGE table with this metadata. 
--
--   SnowConvert generates this XML configuration file for each .DTSX file in the "InstrumentedSource" directory.
--   This file is generated with the following name: "<package file name>_control_flow_configuration.xml"
-- ==========================================================================  

CREATE OR REPLACE PROCEDURE PUBLIC.READ_CONTROL_FLOW_CONFIG_FROM_STAGE(file_stage_path VARCHAR)
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
BEGIN
   CREATE or REPLACE TEMPORARY TABLE TMP_TBL (xml VARIANT);
   COPY INTO TMP_TBL FROM :file_stage_path
   FILE_FORMAT=(TYPE=XML, Strip_outer_element = true,PRESERVE_SPACE=FALSE);
   INSERT INTO  PUBLIC.CONTROL_FLOW_TABLE_USAGE
   SELECT 
       TaskConfig.xml:"@TaskName" as TASK_NAME,
       TaskConfig.xml:"@TaskRefId" as TASK_REFID,
       TaskConfig.xml:"@TaskGuid" as TASK_GUID,
       TRIM(TblToMonitor.Value:"@Name",'[]') as TABLE_NAME,
       TRIM(TblToMonitor.Value:"@Schema",'[]') as SCHEMA_NAME,
       TRIM(TblToMonitor.Value:"@Database",'[]') as DB_NAME
   FROM TMP_TBL TaskConfig, LATERAL FLATTEN(to_array(TaskConfig.XML:"$")) TblToMonitor;
   DROP TABLE TMP_TBL;
END;
$$;
