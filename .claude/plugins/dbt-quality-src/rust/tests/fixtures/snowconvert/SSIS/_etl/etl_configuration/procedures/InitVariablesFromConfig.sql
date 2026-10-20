-- <copyright file="InitVariablesFromConfig.sql" company="Snowflake Inc">
--        Copyright (c) 2019-2026 Snowflake Inc. All rights reserved.
-- </copyright>

-- ==========================================================================
-- DESCRIPTION:
--   Generated for ETL conversion
--   This procedure loads variable defaults from CONFIG JSON into the control_variables table
--   Only inserts variables that do not already exist (respects persistent values)
--   Execute this script once before running any orchestration that uses variable management
--
--   Run-isolation: this first calls SetRunContext to resolve the run_id prefix
--   for the session (from the task-graph CONFIG), then writes rows at the
--   prefixed scope. When no run_id is present, or the proc runs outside a task
--   graph, the prefix collapses to '' and rows land at today's unprefixed scope
--   without failing.
-- ==========================================================================

CREATE OR REPLACE PROCEDURE public.InitVariablesFromConfig(p_variable_scope VARCHAR, p_config_json VARCHAR)
RETURNS INTEGER
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
DECLARE
    config_defaults VARIANT;
    variable_scope_count INTEGER := 0;
    v_effective_scope VARCHAR;
BEGIN
    CALL public.SetRunContext();
    v_effective_scope := public.GetRunScopePrefix() || :p_variable_scope;

    config_defaults := PARSE_JSON(:p_config_json);

    IF (config_defaults IS NULL) THEN
        RETURN 0;
    END IF;

    INSERT INTO public.control_variables
        (variable_name, variable_value, variable_type, variable_scope,
         is_parameter, is_persistent, last_updated_at)
    SELECT
        key,
        value:value,
        value:type::VARCHAR,
        :v_effective_scope,
        COALESCE(value:is_parameter::BOOLEAN, FALSE),
        COALESCE(value:is_persistent::BOOLEAN, FALSE),
        CURRENT_TIMESTAMP()
    FROM TABLE(FLATTEN(input => :config_defaults))
    WHERE NOT EXISTS (
        SELECT 1 FROM public.control_variables
        WHERE variable_name = key
          AND variable_scope = :v_effective_scope
    );

    SELECT COUNT(*) INTO variable_scope_count
    FROM public.control_variables
    WHERE variable_scope = :v_effective_scope;

    RETURN variable_scope_count;
END;
$$;
