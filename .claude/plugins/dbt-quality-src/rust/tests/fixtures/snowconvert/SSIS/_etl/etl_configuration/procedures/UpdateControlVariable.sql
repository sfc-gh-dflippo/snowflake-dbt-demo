-- <copyright file="UpdateControlVariable.sql" company="Snowflake Inc">
--        Copyright (c) 2019-2026 Snowflake Inc. All rights reserved.
-- </copyright>

-- ==========================================================================
-- DESCRIPTION:
--   Generated for ETL conversion
--   This procedure provides a reusable way to update variable values in control_variables table
--   Execute this script once before running any orchestration that uses container variable updates
--
--   Run-isolation: the effective scope is prefixed with the run_id for the
--   current run via public.GetRunScopePrefix(), which reads it from
--   public.run_context (populated by SetRunContext). When no run_id is present
--   the prefix collapses to '' and this targets today's unprefixed scope. The
--   prefix read never throws, so this is safe to call outside a task graph.
-- ==========================================================================

CREATE OR REPLACE PROCEDURE public.UpdateControlVariable(p_variable_name VARCHAR, p_variable_scope VARCHAR, p_variable_value VARIANT)
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
DECLARE
  v_effective_scope VARCHAR;
BEGIN
  v_effective_scope := public.GetRunScopePrefix() || :p_variable_scope;

  UPDATE public.control_variables
  SET variable_value = :p_variable_value,
      last_updated_at = CURRENT_TIMESTAMP()
  WHERE variable_name = :p_variable_name
    AND variable_scope = :v_effective_scope;

  RETURN 'Variable updated successfully';
END;
$$;
