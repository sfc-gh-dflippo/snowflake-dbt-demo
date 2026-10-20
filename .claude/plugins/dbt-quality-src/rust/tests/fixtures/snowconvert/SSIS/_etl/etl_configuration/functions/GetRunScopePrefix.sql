-- <copyright file="GetRunScopePrefix.sql" company="Snowflake Inc">
--        Copyright (c) 2019-2026 Snowflake Inc. All rights reserved.
-- </copyright>

-- ==========================================================================
-- DESCRIPTION:
--   Generated for ETL conversion.
--   Returns the run-scope prefix for the current run. The prefix is resolved
--   once per session by SetRunContext (from the task-graph CONFIG "run_id" key)
--   and stored in public.run_context; this UDF just reads it back, keyed by
--   CURRENT_SESSION(). With a non-empty run_id the prefix is "<run_id>__"; when
--   no row exists for the session (a proc/UDF invoked outside any task graph,
--   or before SetRunContext ran) it resolves to '' so the scope is unprefixed.
--
--   Reading from the table instead of calling SYSTEM$GET_TASK_GRAPH_CONFIG()
--   here is deliberate: that function throws outside a task graph and a scalar
--   SQL UDF cannot catch it, so a direct call would make every helper that
--   reaches this UDF fail when invoked outside a task. The table read never
--   throws, so callers degrade gracefully to the unprefixed scope.
--
--   Used as the single source of the run-scope prefix that namespaces control
--   variables per run, so concurrent runs of the same task graph do not collide
--   on shared variable_scope rows. Each caller appends its own scope argument:
--   public.GetRunScopePrefix() || <scope>.
-- ==========================================================================

CREATE OR REPLACE FUNCTION public.GetRunScopePrefix()
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
  COALESCE((SELECT run_scope_prefix FROM public.run_context WHERE session_id = CURRENT_SESSION()), '')
$$;
