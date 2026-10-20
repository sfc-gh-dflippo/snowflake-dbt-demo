-- <copyright file="BuildDbtVarsJsonUDF.sql" company="Snowflake Inc">
--        Copyright (c) 2019-2026 Snowflake Inc. All rights reserved.
-- </copyright>

-- ==========================================================================
-- DESCRIPTION:
--   Generated for ETL conversion
--   This function builds a JSON object from control_variables for use with EXECUTE DBT PROJECT --vars
--   It properly escapes quotes in VARCHAR values (SQL queries) for shell/YAML parsing
--   Execute this script once before running any orchestration that uses variables with DBT
--
--   Run-isolation: the effective scope is prefixed with the run_id for the
--   current run via public.GetRunScopePrefix(), which reads it from
--   public.run_context (populated by SetRunContext). When no run_id is present
--   the prefix collapses to '' and this targets today's unprefixed scope. The
--   prefix read never throws, so this is safe to call outside a task graph.
-- ==========================================================================

CREATE OR REPLACE FUNCTION public.BuildDbtVarsJsonUDF(p_variable_scope VARCHAR)
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
  SELECT OBJECT_AGG(
    variable_name,
    CASE
      WHEN variable_type = 'VARCHAR'
      THEN TO_VARIANT(
             REPLACE(REPLACE(REPLACE(REPLACE(variable_value::VARCHAR, '\\', '\\u005c\\u005c'), '"', '\\"'), '''', '\\u0027'), '\n', '\\u000a')
           )
      ELSE variable_value
    END
  )::VARCHAR
  FROM public.control_variables
  WHERE variable_scope = public.GetRunScopePrefix() || p_variable_scope
$$;
