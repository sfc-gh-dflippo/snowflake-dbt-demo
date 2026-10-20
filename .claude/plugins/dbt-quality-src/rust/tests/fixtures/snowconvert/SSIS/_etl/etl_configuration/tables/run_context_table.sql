-- <copyright file="run_context_table.sql" company="Snowflake Inc">
--        Copyright (c) 2019-2026 Snowflake Inc. All rights reserved.
-- </copyright>

-- ==========================================================================
-- DESCRIPTION:
--   Generated for ETL conversion.
--   Holds the run-scope prefix for the current session so the control-variable
--   helpers can resolve it WITHOUT calling SYSTEM$GET_TASK_GRAPH_CONFIG()
--   inline (that function throws outside a task graph, and a scalar SQL UDF
--   cannot catch it). SetRunContext writes a row here, keyed by
--   CURRENT_SESSION(); GetRunScopePrefix reads it back. When no row exists for
--   the session (a proc/UDF invoked outside any task graph) the prefix resolves
--   to '' and the helpers target today's unprefixed scope instead of failing.
--
--   Rows are keyed by CURRENT_SESSION(); each task in a graph populates its own
--   session's row via a MERGE. There is deliberately no UNIQUE constraint on
--   session_id and no automatic purge: correctness does not need them, because
--   CURRENT_SESSION() is unique per session and SetRunContext runs serially within
--   a session, so at most one live row is ever read (GetRunScopePrefix selects by
--   CURRENT_SESSION()). Rows from ended sessions are never read again but are not
--   auto-removed, so the table grows one row per session over time. Operators
--   should purge stale rows periodically (e.g. a scheduled task deleting rows older
--   than a retention window); emitting that purge automatically is a tracked
--   follow-up, not required for correctness.
--   Execute this script once before running any orchestration that uses
--   variable management.
-- ==========================================================================

CREATE TABLE IF NOT EXISTS public.run_context (
    session_id       VARCHAR NOT NULL,
    run_scope_prefix VARCHAR,
    last_updated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);
