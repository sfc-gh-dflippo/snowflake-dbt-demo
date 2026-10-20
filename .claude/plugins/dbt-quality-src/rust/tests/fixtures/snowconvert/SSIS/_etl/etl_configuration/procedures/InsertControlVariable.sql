-- <copyright file="InsertControlVariable.sql" company="Snowflake Inc">
--        Copyright (c) 2019-2026 Snowflake Inc. All rights reserved.
-- </copyright>

-- ==========================================================================
-- DESCRIPTION:
--   Generated for ETL conversion
--   This procedure inserts a variable into the control_variables table
--   if it does not already exist for the given name and scope.
--   Used for built-in variables (e.g., SESSSTARTTIME) that are injected
--   at runtime and are not part of the CONFIG JSON.
--   Execute this script once before running any orchestration that uses
--   built-in variable injection.
--
--   Run-isolation: the effective scope is prefixed with the run_id for the
--   current run via public.GetRunScopePrefix(), which reads it from
--   public.run_context (populated by SetRunContext). When no run_id is present
--   the prefix collapses to '' and rows land at today's unprefixed scope.
--   Built-ins must share the same prefixed scope the readers use, or
--   GetControlVariableUDF would miss them. The prefix read never throws, so
--   this is safe to call outside a task graph.
-- ==========================================================================

CREATE OR REPLACE PROCEDURE public.InsertControlVariable(p_variable_name VARCHAR, p_variable_scope VARCHAR, p_variable_value VARIANT, p_variable_type VARCHAR)
RETURNS INTEGER
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
DECLARE
    v_effective_scope VARCHAR;
BEGIN
    v_effective_scope := public.GetRunScopePrefix() || :p_variable_scope;

    INSERT INTO public.control_variables
        (variable_name, variable_value, variable_type, variable_scope,
         is_parameter, is_persistent, last_updated_at)
    SELECT
        :p_variable_name,
        :p_variable_value,
        :p_variable_type,
        :v_effective_scope,
        FALSE,
        FALSE,
        CURRENT_TIMESTAMP()
    WHERE NOT EXISTS (
        SELECT 1 FROM public.control_variables
        WHERE variable_name = :p_variable_name
          AND variable_scope = :v_effective_scope
    );
    RETURN SQLROWCOUNT;
END;
$$;
