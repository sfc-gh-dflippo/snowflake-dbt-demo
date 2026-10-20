-- <copyright file="ssis_task_table_usage.sql" company="Snowflake Inc">
--        Copyright (c) 2019-2025 Snowflake Inc. All rights reserved.
-- </copyright>

-- ==========================================================================
-- DESCRIPTION: CONTROL_FLOW_TABLE_USAGE(file_stage_path VARCHAR)
--   Table for tracking the tables affected by the execution of an SSIS task. 
--
--   Load data into this table using the "READ_CONTROL_FLOW_CONFIG_FROM_STAGE" procedure.
-- ==========================================================================  

CREATE OR REPLACE TABLE PUBLIC.CONTROL_FLOW_TABLE_USAGE (
    task_name VARCHAR,              -- Simple name of the task
    task_refid VARCHAR,             -- Ref Id (SSIS) of the task
    task_guid VARCHAR,              -- The unique identifier of the task (SSIS DTSID).
    table_name VARCHAR,             -- Name of the table.
    schema_name VARCHAR,            -- Schema of the table.
    db_name VARCHAR                 -- Database name.
);
