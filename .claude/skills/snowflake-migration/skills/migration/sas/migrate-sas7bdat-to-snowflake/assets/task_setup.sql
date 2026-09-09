-- task_setup.sql
-- Ongoing scheduled load. Wraps LOAD_SAS7BDAT (with incremental=TRUE) in a Task.
-- Pick ONE variant below. Replace <DB>, <SCHEMA>, <STAGE>, <WAREHOUSE>, and the
-- schedule/encoding before running. Deploy control_table.sql + loader_sproc.sql first.

-- =====================================================================
-- VARIANT 1: Time-based (simplest). Runs on a fixed schedule; the proc's
-- incremental logic + control table make each run a no-op when nothing is new.
-- The proc REFRESHES the stage's directory table itself at the start of every run,
-- so no separate refresh task is needed for this variant.
-- =====================================================================
CREATE OR REPLACE TASK <DB>.<SCHEMA>.LOAD_SAS7BDAT_TASK
    WAREHOUSE = <WAREHOUSE>
    SCHEDULE  = 'USING CRON 0 * * * * UTC'   -- every hour on the hour; adjust as needed
AS
    CALL <DB>.<SCHEMA>.LOAD_SAS7BDAT(
        '@<DB>.<SCHEMA>.<STAGE>',
        '<DB>.<SCHEMA>',
        'append',        -- default write mode for ongoing
        NULL,            -- per-table overrides JSON, or NULL
        TRUE,            -- incremental: only load new/changed files
        'latin-1'
    );

ALTER TASK <DB>.<SCHEMA>.LOAD_SAS7BDAT_TASK RESUME;


-- =====================================================================
-- VARIANT 2: Stream-triggered. A stream on the stage's directory table detects new
-- files; the Task fires on a schedule but only does work WHEN the stream has data,
-- so idle cycles cost almost nothing. Requires the directory table to be enabled.
-- Use this INSTEAD OF Variant 1 (don't create both tasks with the same name).
-- IMPORTANT: the WHEN gate is evaluated BEFORE the task body runs, so the proc's own
-- refresh can't feed the stream. This variant therefore needs the directory table
-- refreshed by something external to populate the stream: either enable stage
-- auto-refresh (cloud notifications), or run a small predecessor REFRESH task, e.g.:
--   CREATE OR REPLACE TASK <DB>.<SCHEMA>.REFRESH_STAGE_TASK
--       WAREHOUSE=<WAREHOUSE> SCHEDULE='USING CRON */15 * * * * UTC'
--   AS ALTER STAGE <DB>.<SCHEMA>.<STAGE> REFRESH;
-- =====================================================================
-- CREATE OR REPLACE STREAM <DB>.<SCHEMA>.SAS_DIR_STREAM
--     ON STAGE <DB>.<SCHEMA>.<STAGE>;
--
-- CREATE OR REPLACE TASK <DB>.<SCHEMA>.LOAD_SAS7BDAT_TASK
--     WAREHOUSE = <WAREHOUSE>
--     SCHEDULE  = 'USING CRON */15 * * * * UTC'          -- check every 15 min
--     WHEN SYSTEM$STREAM_HAS_DATA('<DB>.<SCHEMA>.SAS_DIR_STREAM')
-- AS
--     BEGIN
--         ALTER STAGE <DB>.<SCHEMA>.<STAGE> REFRESH;
--         CALL <DB>.<SCHEMA>.LOAD_SAS7BDAT(
--             '@<DB>.<SCHEMA>.<STAGE>', '<DB>.<SCHEMA>', 'append', NULL, TRUE, 'latin-1');
--         -- Advance the stream offset so it stops firing until the next new file.
--         CREATE OR REPLACE TEMP TABLE _sas_stream_drain AS
--             SELECT * FROM <DB>.<SCHEMA>.SAS_DIR_STREAM;
--     END;
--
-- ALTER TASK <DB>.<SCHEMA>.LOAD_SAS7BDAT_TASK RESUME;


-- =====================================================================
-- Operations
-- =====================================================================
-- Manual run:      EXECUTE TASK <DB>.<SCHEMA>.LOAD_SAS7BDAT_TASK;
-- Recent history:  SELECT * FROM TABLE(<DB>.INFORMATION_SCHEMA.TASK_HISTORY(
--                    TASK_NAME => 'LOAD_SAS7BDAT_TASK')) ORDER BY scheduled_time DESC;
-- Pause:           ALTER TASK <DB>.<SCHEMA>.LOAD_SAS7BDAT_TASK SUSPEND;
-- Grant to run:    the task owner role needs EXECUTE TASK (account-level) to be scheduled.
