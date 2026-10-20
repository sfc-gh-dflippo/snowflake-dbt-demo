-- <copyright file="GetControlVariableUDF.sql" company="Snowflake Inc">
--        Copyright (c) 2019-2025 Snowflake Inc. All rights reserved.
-- </copyright>

-- ==========================================================================
-- DESCRIPTION:
--   Generated for ETL conversion
--   This function provides a reusable way to retrieve variable values from control_variables table
--   Execute this script once before running any orchestration that uses container variable declarations
--
--   Run-isolation: the effective scope is prefixed with the run_id for the
--   current run via public.GetRunScopePrefix(), which reads it from
--   public.run_context (populated by SetRunContext). When no run_id is present
--   the prefix collapses to '' and the lookup targets today's unprefixed scope
--   -- bit-for-bit backwards compatible. The prefix read never throws, so this
--   UDF is safe to call outside a task graph (it returns the unprefixed value).
-- ==========================================================================

CREATE OR REPLACE FUNCTION public.GetControlVariableUDF(p_variable_name VARCHAR, p_variable_scope VARCHAR)
RETURNS VARIANT
LANGUAGE SQL
AS
$$
  SELECT variable_value
  FROM public.control_variables
  WHERE variable_name = p_variable_name
    AND variable_scope = public.GetRunScopePrefix() || p_variable_scope
  LIMIT 1
$$;