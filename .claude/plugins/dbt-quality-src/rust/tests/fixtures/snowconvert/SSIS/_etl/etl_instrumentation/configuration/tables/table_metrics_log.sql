-- <copyright file="table_metrics_log.sql" company="Snowflake Inc">
--        Copyright (c) 2019-2025 Snowflake Inc. All rights reserved.
-- </copyright>

-- ==========================================================================
-- DESCRIPTION: TABLE_METRICS_LOG
--   Table to keep track of metrics generated from the execution of converted code.
-- ==========================================================================  

CREATE OR REPLACE TABLE PUBLIC.TABLE_METRICS_LOG (    
    package_name VARCHAR,           -- Name of the original ssis package
    task_name VARCHAR,              -- Name of the original ssis task
    task_guid VARCHAR,              -- The guid of the original transformation
    subtask_name VARCHAR,           -- Name of a subtask (used for dbt projects that replace a component output with a dbt model)
    database_name VARCHAR,          -- Name of the database 
    schema_name VARCHAR,            -- Name of the schema
    table_name VARCHAR,             -- Name of the table
    rowcount INT,                   -- Number of rows that resulted for the execution of the current element
    kind CHAR(2),                   -- Kind 'df' for dbt project,  NULL or 'cf' for task graph element
    timestamp TIMESTAMP_NTZ         -- Time stamp of the measurement.
);