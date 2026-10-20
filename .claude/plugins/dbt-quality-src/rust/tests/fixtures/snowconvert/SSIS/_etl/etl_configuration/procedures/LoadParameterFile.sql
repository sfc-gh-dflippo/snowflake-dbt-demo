-- <copyright file="LoadParameterFile.sql" company="Snowflake Inc">
--        Copyright (c) 2019-2026 Snowflake Inc. All rights reserved.
-- </copyright>

-- ==========================================================================
-- DESCRIPTION:
--   Generated for ETL conversion.
--   Loads variable overrides from a JSON parameter file on a stage and applies
--   them to the row identified by p_target_scope in public.control_variables.
--
--   Cascading scopes (most-specific wins, applied in this order):
--     1. "*global*"                   -> applied to every targeted row
--     2. p_ancestor_scopes[i]         -> applied for each ancestor scope
--                                        (least-specific first), bridging
--                                        dotted JSON keys via REPLACE
--     3. p_target_scope (exact)       -> applied to that one row only
--
--   Each step is a separate UPDATE; the last UPDATE that touches a
--   (variable_scope, variable_name) row wins. The ancestor loop iterates
--   over its input array in order, so passing the workflow scope first
--   then the worklet scope, etc., produces the intended outermost-to-
--   innermost cascade for sessions inside (nested) worklets.
--
--   p_ancestor_scopes is optional (DEFAULT ARRAY_CONSTRUCT()) so callers
--   that only need the Global + Exact passes (e.g., a workflow root row
--   that has no ancestors) can omit it. The converter's emit sites pass
--   the appropriate ancestor chain: empty for the workflow root,
--   [<workflow_scope>] for workflow-direct sessions and worklet
--   instances, ARRAY_APPEND-composed at runtime for nested contexts.
--
--   Expected JSON format:
--     {
--       "*global*":                                { "shared_var":   100 },
--       "WORKFLOWNAME":                            { "wf_country":   "Canada" },
--       "WORKFLOWNAME.WORKLETINST":                { "wklt_var":     42 },
--       "WORKFLOWNAME.WORKLETINST.s_m_mapping":    { "m_vacation_bonus": 10 }
--     }
--
--   The "*global*" outer key matches case-insensitively (also "*Global*",
--   "*GLOBAL*"). The asterisks make the sentinel structurally impossible to
--   collide with a real Informatica workflow name (PowerCenter rejects "*"
--   in workflow names), so no workflow can ever be misinterpreted as the
--   cascade marker.
--
--   Translating an Informatica .prm parameter-file section header to a JSON
--   outer key:
--     [GLOBAL]                                                 -> "*global*"
--     [FOLDER.WF:wkf_name]                                     -> "wkf_name"
--     [FOLDER.WF:wkf_name.WT:wklt_inst]                        -> "wkf_name.wklt_inst"
--     [FOLDER.WF:wkf_name.WT:wklt_inst.ST:s_session_name]      -> "wkf_name.wklt_inst.s_session_name"
--   Drop the FOLDER prefix and the WF:/WT:/ST: tokens; keep the dots.
--
-- Notes on inner-key shape:
--   - Mapping variables use the bare variable name (e.g. "m_vacation_bonus").
--   - Mapplet variables are prefixed with their canonical mapplet name
--     (e.g. "mplt_GET_NEXT_VAL_SEQ_NAME"), since a single mapplet macro is
--     shared across all consumers and the prefix disambiguates per-mapplet
--     state. Per-session isolation is provided by `variable_scope`, not by
--     the variable name.
--   - When a mapping consumes a mapplet through a <SHORTCUT> alias, the
--     canonical mapplet name (NOT the shortcut alias) is what appears in
--     control_variables and dbt_project.yml. Use the canonical key, e.g.
--     "mplt_GET_NEXT_VAL_SEQ_NAME", NOT "Shortcut_to_mplt_GET_NEXT_VAL_SEQ_NAME".
--   - Canonical keys are listed as defaults in the consuming mapping's
--     dbt_project.yml -- copy from there.
-- ==========================================================================

CREATE OR REPLACE PROCEDURE public.LoadParameterFile(
  p_stage_path      VARCHAR,
  p_target_scope    VARCHAR,
  p_ancestor_scopes ARRAY DEFAULT ARRAY_CONSTRUCT()
)
RETURNS INTEGER
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
DECLARE
    updated_count INTEGER := 0;
    n             INTEGER;
    i             INTEGER;
    anc           VARCHAR;
    v_effective_target VARCHAR;
BEGIN
    -- Resolve the parameter-file path. An explicit p_stage_path always
    -- wins -- this is how worklet stored-proc / always-emit callers pass their gated path.
    -- When the caller passes NULL (the workflow-root emit, which no longer hard-codes the
    -- stage literal), fall back to the "param_file" key in the task-graph CONFIG, supplied
    -- per run via EXECUTE TASK ... USING CONFIG. The default CONFIG carries the
    -- "@<STAGE_PLACEHOLDER>/<workflow>.json" placeholder, so an unmodified deployment hits
    -- the same "stage does not exist" runtime error it does today -- behavior preserved.
    -- SYSTEM$GET_TASK_GRAPH_CONFIG() throws outside a task graph, so the read is wrapped in
    -- an EXCEPTION handler: a standalone CALL of this proc (no task) resolves to no path and
    -- returns 0 below, rather than failing.
    IF (p_stage_path IS NULL OR TRIM(p_stage_path) = '') THEN
        BEGIN
            p_stage_path := PARSE_JSON(SYSTEM$GET_TASK_GRAPH_CONFIG()):param_file::VARCHAR;
        EXCEPTION
            WHEN OTHER THEN
                p_stage_path := NULL;
        END;
    END IF;

    -- If, after the CONFIG fallback, there is still no path or no scope, nothing to do.
    -- Note: callers from worklet stored-proc bodies (Method B / always-emit sites) gate this
    -- CALL with `IF (:p_paramfile_path IS NOT NULL AND TRIM(...) <> '') THEN CALL ...` before
    -- invoking the proc, so this guard is redundant on those paths. It is still load-bearing
    -- for the workflow-direct emit (the per-instance task wrapper invokes LoadParameterFile
    -- without an outer IF), so keep it.
    IF (p_stage_path IS NULL OR TRIM(p_stage_path) = '' OR p_target_scope IS NULL OR TRIM(p_target_scope) = '') THEN
        RETURN 0;
    END IF;

    -- Coerce a NULL ancestor array to empty so ARRAY_SIZE / GET behave predictably:
    -- today's callers always pass ARRAY_CONSTRUCT(...) or rely on the DEFAULT, but a
    -- future caller passing the result of ARRAY_APPEND(NULL, x) (NULL when the prior
    -- link in the chain is NULL) would otherwise silently skip the whole ancestor
    -- loop with no error or log line.
    IF (p_ancestor_scopes IS NULL) THEN
        p_ancestor_scopes := ARRAY_CONSTRUCT();
    END IF;

    -- Run-isolation: the rows in control_variables are stored at the
    -- run_id-prefixed scope (InitVariablesFromConfig writes them prefixed), so the
    -- cv.variable_scope row-targeting below must match the PREFIXED scope. The JSON
    -- outer keys (f1.key) come from the customer's .prm file and are LOGICAL section
    -- names with no run prefix, so they keep matching against the unprefixed
    -- p_target_scope / anc. When no run_id is present the prefix collapses to '' and
    -- v_effective_target == p_target_scope -- bit-for-bit backwards compatible. The prefix
    -- is read from public.run_context (populated by SetRunContext), so this never throws
    -- even when the proc runs outside a task graph.
    v_effective_target := public.GetRunScopePrefix() || :p_target_scope;

    -- Load the JSON file from stage into a temporary table
    CREATE OR REPLACE TEMPORARY TABLE __SNOWCONVERT_LOAD_PARAMETER_FILE_TMP (json_raw VARIANT);

    COPY INTO __SNOWCONVERT_LOAD_PARAMETER_FILE_TMP FROM :p_stage_path
    FILE_FORMAT = (TYPE = JSON);

    -- 1. Global section (least specific, applied first; case-insensitive).
    UPDATE public.control_variables cv
    SET    cv.variable_value  = j.value,
           cv.last_updated_at = CURRENT_TIMESTAMP()
    FROM   __SNOWCONVERT_LOAD_PARAMETER_FILE_TMP t,
           TABLE(FLATTEN(input => t.json_raw))     f1,
           TABLE(FLATTEN(input => f1.value))       j
    WHERE  UPPER(f1.key) = '*GLOBAL*'
      AND  cv.variable_name  = j.key
      AND  cv.variable_scope = :v_effective_target;

    updated_count := updated_count + SQLROWCOUNT;

    -- 2. Ancestor sections (least-specific to most-specific). The PRM-to-JSON spec
    --    encodes ancestor headers with dots (e.g. "wf.wklt"), while the runtime
    --    composes scopes with underscores (e.g. "wf_wklt"); REPLACE bridges the
    --    two so dotted ancestor keys can match. The (anc <> p_target_scope) guard
    --    prevents a double-write when an ancestor coincides with the target row
    --    (covered by step 3 anyway). Empty / NULL entries are skipped silently.
    --    Ordering contract (load-bearing): the cascade's "more-specific overrides
    --    less-specific" semantics rely on callers passing ancestors in
    --    least-specific-first order. The proc iterates the array as given and
    --    does NOT validate ordering; a caller that prepends instead of appends
    --    would silently invert the cascade.
    n := ARRAY_SIZE(:p_ancestor_scopes);
    i := 0;
    WHILE (i < n) DO
        anc := GET(:p_ancestor_scopes, :i)::VARCHAR;
        IF (anc IS NOT NULL AND anc <> '' AND anc <> :p_target_scope) THEN
            UPDATE public.control_variables cv
            SET    cv.variable_value  = j.value,
                   cv.last_updated_at = CURRENT_TIMESTAMP()
            FROM   __SNOWCONVERT_LOAD_PARAMETER_FILE_TMP t,
                   TABLE(FLATTEN(input => t.json_raw))     f1,
                   TABLE(FLATTEN(input => f1.value))       j
            WHERE  REPLACE(f1.key, '.', '_') = :anc
              AND  cv.variable_name  = j.key
              AND  cv.variable_scope = :v_effective_target;

            updated_count := updated_count + SQLROWCOUNT;
        END IF;
        i := i + 1;
    END WHILE;

    -- 3. Exact section (most specific, applied last; covers WF target and
    --    dotted Session target keys). The session-level JSON outer key uses
    --    a dot ("wfname.sessionname") per the PRM-to-JSON spec, while the
    --    runtime session scope joins with an underscore ("wfname_sessionname"
    --    via GetSessionScope). REPLACE bridges the two; without it, dotted
    --    session keys would never match.
    UPDATE public.control_variables cv
    SET    cv.variable_value  = j.value,
           cv.last_updated_at = CURRENT_TIMESTAMP()
    FROM   __SNOWCONVERT_LOAD_PARAMETER_FILE_TMP t,
           TABLE(FLATTEN(input => t.json_raw))     f1,
           TABLE(FLATTEN(input => f1.value))       j
    WHERE  REPLACE(f1.key, '.', '_') = :p_target_scope
      AND  cv.variable_name  = j.key
      AND  cv.variable_scope = :v_effective_target;

    updated_count := updated_count + SQLROWCOUNT;

    -- Clean up temporary table
    DROP TABLE IF EXISTS __SNOWCONVERT_LOAD_PARAMETER_FILE_TMP;

    RETURN updated_count;
END;
$$;
