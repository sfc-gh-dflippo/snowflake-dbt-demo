-- <copyright file="ssis_baseline_metrics_log_table.sql" company="Snowflake Inc">
--        Copyright (c) 2019-2025 Snowflake Inc. All rights reserved.
-- </copyright>

-- ==========================================================================
-- DESCRIPTION: The BASELINE_TABLE_METRICS_LOG table is used to store baseline data generated from 
--   the instrumentation of source SSIS packages.
-- ==========================================================================

CREATE OR REPLACE TABLE PUBLIC.BASELINE_TABLE_METRICS_LOG (
    -- Package and Task Identifiers
    package_name VARCHAR(255),                           -- Name of the SSIS package (may be NULL)
    task_name VARCHAR(255) NOT NULL,                     -- Name of the control flow task
    task_guid VARCHAR(40),                               -- GUID of the control flow task
    component_name VARCHAR(255),                         -- Name of the component (for kind='df')
    component_output_name VARCHAR(255),                  -- Name of the component output
    database_name VARCHAR(128),                          -- Database name (for kind='cf')
    schema_name VARCHAR(128),                            -- Schema name (for kind='cf')
    table_name VARCHAR(128),                             -- Table name (for kind='cf')
    
    -- Metrics
    rowcount BIGINT NOT NULL DEFAULT 0,                  -- Number of rows processed
    
    -- Metadata
    kind CHAR(2) NULL, -- 'cf' = control flow, 'df' = data flow
    timestamp TIMESTAMP_LTZ NOT NULL DEFAULT CURRENT_TIMESTAMP() -- Event timestamp with timezone
);
