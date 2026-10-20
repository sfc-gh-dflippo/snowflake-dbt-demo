-- <copyright file="ClearVariables.sql" company="Snowflake Inc">
--        Copyright (c) 2019-2026 Snowflake Inc. All rights reserved.
-- </copyright>

-- ==========================================================================
-- DESCRIPTION:
--   Generated for ETL conversion
--   This procedure deletes non-persistent variables for a scope, preserving persistent values
--   Execute this script once before running any orchestration that uses variable management
--
--   Run-isolation: this first calls SetRunContext to resolve the run_id prefix
--   for the session (from the task-graph CONFIG), then targets the prefixed
--   scope. When no run_id is present, or the proc runs outside a task graph, the
--   prefix collapses to '' and this targets today's unprefixed scope without
--   failing.
-- ==========================================================================

CREATE OR REPLACE PROCEDURE public.ClearVariables(p_variable_scope VARCHAR)
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
DECLARE
    v_effective_scope VARCHAR;
BEGIN
    CALL public.SetRunContext();
    v_effective_scope := public.GetRunScopePrefix() || :p_variable_scope;

    DELETE FROM public.control_variables
    WHERE variable_scope = :v_effective_scope
      AND is_persistent = FALSE;

    RETURN 'Cleared non-persistent variables for scope: ' || :v_effective_scope;
END;
$$;
