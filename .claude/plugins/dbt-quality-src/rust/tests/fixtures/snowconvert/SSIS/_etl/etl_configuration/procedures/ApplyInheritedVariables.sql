-- <copyright file="ApplyInheritedVariables.sql" company="Snowflake Inc">
--        Copyright (c) 2019-2026 Snowflake Inc. All rights reserved.
-- </copyright>

-- ==========================================================================
-- DESCRIPTION:
--   Generated for ETL conversion
--   This procedure applies inherited variables passed from a parent package
--   to a child stored procedure. It updates existing variables in the
--   control_variables table with values from the JSON parameter.
--   Execute this script once before running any orchestration that uses
--   Execute Package Task parameter bindings.
--
--   Run-isolation: the effective scope is prefixed with the run_id for the
--   current run via public.GetRunScopePrefix(), which reads it from
--   public.run_context (populated by SetRunContext). When no run_id is present
--   the prefix collapses to '' and this targets today's unprefixed scope. The
--   prefix read never throws, so this is safe to call outside a task graph.
-- ==========================================================================

CREATE OR REPLACE PROCEDURE public.ApplyInheritedVariables(
  p_variable_scope VARCHAR,
  p_inherited_vars_json VARCHAR
)
RETURNS INTEGER
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
DECLARE
  inherited_vars VARIANT;
  updated_count INTEGER := 0;
  v_effective_scope VARCHAR;
BEGIN
  -- If no inherited variables were passed, nothing to do
  IF (p_inherited_vars_json IS NULL OR p_inherited_vars_json = '') THEN
    RETURN 0;
  END IF;

  -- Parse the JSON containing inherited variable values
  inherited_vars := PARSE_JSON(:p_inherited_vars_json);

  IF (inherited_vars IS NULL) THEN
    RETURN 0;
  END IF;

  v_effective_scope := public.GetRunScopePrefix() || :p_variable_scope;

  -- Update existing variables with inherited values from parent
  -- JSON structure: {"VarName": <value>, ...}
  UPDATE public.control_variables cv
  SET variable_value = f.value,
      last_updated_at = CURRENT_TIMESTAMP()
  FROM TABLE(FLATTEN(input => :inherited_vars)) f
  WHERE cv.variable_name = f.key
    AND cv.variable_scope = :v_effective_scope;

  updated_count := SQLROWCOUNT;
  RETURN updated_count;
END;
$$;
