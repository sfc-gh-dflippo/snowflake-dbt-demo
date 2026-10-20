-- <copyright file="control_variables_table.sql" company="Snowflake Inc">
--        Copyright (c) 2019-2025 Snowflake Inc. All rights reserved.
-- </copyright>

-- ==========================================================================
-- DESCRIPTION:
--   Generated for ETL conversion
--   This table stores variable values used by all ETL orchestrations
--   Execute this script once before running any orchestration
-- ==========================================================================

CREATE TRANSIENT TABLE IF NOT EXISTS public.control_variables (
  variable_name VARCHAR NOT NULL,
  variable_value VARIANT,
  variable_type VARCHAR NOT NULL,
  variable_scope VARCHAR NOT NULL,
  is_parameter BOOLEAN DEFAULT FALSE,
  is_persistent BOOLEAN DEFAULT FALSE,
  last_updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

