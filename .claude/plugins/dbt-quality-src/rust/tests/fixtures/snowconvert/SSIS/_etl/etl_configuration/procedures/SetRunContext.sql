-- <copyright file="SetRunContext.sql" company="Snowflake Inc">
--        Copyright (c) 2019-2026 Snowflake Inc. All rights reserved.
-- </copyright>

-- ==========================================================================
-- DESCRIPTION:
--   Generated for ETL conversion.
--   Resolves the run-scope prefix for the CURRENT session and stores it in
--   public.run_context, so the inline control-variable helpers (GetRunScopePrefix
--   and everything that calls it) can read the prefix from a table instead of
--   calling SYSTEM$GET_TASK_GRAPH_CONFIG() themselves.
--
--   The run_id comes from the task-graph CONFIG ("run_id" key) supplied per run
--   via EXECUTE TASK ... USING CONFIG. With a non-empty run_id the prefix is
--   "<run_id>__"; otherwise it is ''. SYSTEM$GET_TASK_GRAPH_CONFIG() throws
--   outside a task graph, so the read is wrapped in an EXCEPTION handler: when
--   this proc is called outside a task (a standalone CALL of a converted proc),
--   it records an empty prefix and returns normally instead of failing.
--
--   Folded into ClearVariables / InitVariablesFromConfig (which every
--   parameterized task body calls), and called explicitly at the top of the
--   SSIS reusable-package procedure (which writes control_variables directly
--   without those helpers). Idempotent: re-running for the same session simply
--   refreshes the row.
--   Execute this script once before running any orchestration that uses
--   variable management.
-- ==========================================================================

CREATE OR REPLACE PROCEDURE public.SetRunContext()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
DECLARE
    v_prefix VARCHAR := '';
BEGIN
    BEGIN
        v_prefix := COALESCE(NULLIF(PARSE_JSON(SYSTEM$GET_TASK_GRAPH_CONFIG()):run_id::VARCHAR, '') || '__', '');
    EXCEPTION
        WHEN OTHER THEN
            -- Not running inside a task graph: no run_id, leave the prefix empty
            -- so the helpers fall back to today's unprefixed scope.
            v_prefix := '';
    END;

    MERGE INTO public.run_context t
    USING (SELECT CURRENT_SESSION() AS sid) s
       ON t.session_id = s.sid
    WHEN MATCHED THEN
        UPDATE SET run_scope_prefix = :v_prefix, last_updated_at = CURRENT_TIMESTAMP()
    WHEN NOT MATCHED THEN
        INSERT (session_id, run_scope_prefix, last_updated_at)
        VALUES (s.sid, :v_prefix, CURRENT_TIMESTAMP());

    RETURN :v_prefix;
END;
$$;
