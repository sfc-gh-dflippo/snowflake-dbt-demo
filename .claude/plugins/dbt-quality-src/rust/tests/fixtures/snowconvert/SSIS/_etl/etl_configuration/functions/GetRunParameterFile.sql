-- <copyright file="GetRunParameterFile.sql" company="Snowflake Inc">
--        Copyright (c) 2019-2026 Snowflake Inc. All rights reserved.
-- </copyright>

-- ==========================================================================
-- DESCRIPTION:
--   Generated for ETL conversion.
--   Returns the parameter-file stage path for the current run, read from the
--   task-graph CONFIG ("param_file" key) supplied per run via
--   EXECUTE TASK ... USING CONFIG. Returns NULL when no param_file is present.
--
--   Used as the single source of the workflow parameter-file path: the
--   per-instance worklet wrapper hoists this into its :paramfile_path LET so the
--   worklet's own LoadParameterFile CALL and the relayed p_paramfile_path that
--   threads into inner sessions/worklets all reference the per-run CONFIG value
--   instead of a compile-time literal.
--
--   Only callable from within a task graph (SYSTEM$GET_TASK_GRAPH_CONFIG()).
-- ==========================================================================

CREATE OR REPLACE FUNCTION public.GetRunParameterFile()
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
  PARSE_JSON(SYSTEM$GET_TASK_GRAPH_CONFIG()):param_file::VARCHAR
$$;
