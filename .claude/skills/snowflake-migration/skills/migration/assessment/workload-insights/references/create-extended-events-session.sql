-- SUGGESTED STARTER SCRIPT — review every value below with your DBA
-- before you run it. These are defaults that fit a typical host, not
-- a guarantee for this instance. This capture uses CPU and disk; it
-- is not free. Needs permission to create a server event session.
--
-- REQUIRED before execute:
--   * Replace YourDatabase in all three database_name predicates with
--     the one database you want to profile.
--   * Replace <dedicated volume> in the target filename with a path on
--     a volume that is not a data or log disk.
--   * If a session named WorkloadReport_XE already exists, change that
--     name in the CREATE statement and in the commented START / STOP
--     statements.
--   * CREATE only defines the session. Uncomment and run START when you
--     want capture to begin.
--
-- Review and change as needed (suggested values):
--   Session name            WorkloadReport_XE
--   Duration threshold      500000 microseconds (0.5 s). Raise to write
--                           less; lowering it costs more CPU and disk.
--   Filters                 one database, is_system = 0, no SSMS /
--                           telemetry, error severity >= 11. Removing
--                           the database predicate traces the instance.
--   filename                path + base name on a dedicated volume, not
--                           data or log disks.
--   max_file_size           200 MB per file
--   max_rollover_files      5  (1 GB cap at the default file size).
--                           Confirm more than that is free.
--   MAX_MEMORY              8192 KB. Keep this from competing with the
--                           buffer pool.
--   MAX_DISPATCH_LATENCY    30 seconds
--   STARTUP_STATE           OFF (session does not return after a
--                           restart; set ON only if you want it to)
--   MEMORY_PARTITION_MODE   Not set, which is right for a typical host.
--                           On a busy many-core server, partitioning
--                           buffers PER_CPU reduces contention when many
--                           queries finish at once. It splits MAX_MEMORY
--                           across cores, so raise MAX_MEMORY (16-32 MB)
--                           if you turn it on — 8192 KB spread over many
--                           cores drops more events.
--
-- Do not change:
--   The three events and their ACTION lists, or this report loses
--   columns. EVENT_RETENTION_MODE = ALLOW_SINGLE_EVENT_LOSS — do not
--   switch to NO_EVENT_LOSS (that can stall user queries).

-- Create the session
CREATE EVENT SESSION [WorkloadReport_XE] ON SERVER

-- Event 1: ad-hoc SQL statements completed
ADD EVENT sqlserver.sql_statement_completed(
    ACTION(
        sqlserver.database_name,
        sqlserver.username,
        sqlserver.client_app_name,
        sqlserver.client_hostname,
        sqlserver.session_id
    )
    WHERE (
        [duration] >= 500000 -- microseconds, so 0.5 s
        AND [sqlserver].[is_system] = 0
        AND [sqlserver].[database_name] = N'YourDatabase'
        AND [sqlserver].[client_app_name] <> N'SQLServerCEIP'
        AND [sqlserver].[username] <> N'NT SERVICE\SQLTELEMETRY'
        AND [sqlserver].[client_app_name] <> N'Microsoft SQL Server Management Studio'
    )
),

-- Event 2: stored procedure and RPC calls completed
ADD EVENT sqlserver.rpc_completed(
    ACTION(
        sqlserver.database_name,
        sqlserver.username,
        sqlserver.client_app_name,
        sqlserver.client_hostname,
        sqlserver.session_id
    )
    WHERE (
        [duration] >= 500000
        AND [sqlserver].[is_system] = 0
        AND [sqlserver].[database_name] = N'YourDatabase'
        AND [sqlserver].[client_app_name] <> N'SQLServerCEIP'
        AND [sqlserver].[username] <> N'NT SERVICE\SQLTELEMETRY'
        AND [sqlserver].[client_app_name] <> N'Microsoft SQL Server Management Studio'
    )
),

-- Event 3: application and query errors
ADD EVENT sqlserver.error_reported(
    ACTION(
        sqlserver.database_name,
        sqlserver.username,
        sqlserver.client_app_name,
        sqlserver.session_id,
        sqlserver.sql_text
    )
    WHERE (
        [severity] >= 11
        AND [sqlserver].[is_system] = 0
        AND [sqlserver].[database_name] = N'YourDatabase'
        AND [sqlserver].[client_app_name] <> N'Microsoft SQL Server Management Studio'
    )
)

-- Target: binary rollover files on disk. Point this at a volume that is
-- not a data or log disk; SQL Server appends its own suffix and .xel.
ADD TARGET package0.event_file(
    SET filename = N'<dedicated volume>\XETraces\WorkloadReport_XE',
    max_file_size = (200),   -- MB per file
    max_rollover_files = (5) -- 1 GB total at the default size
)
WITH (
    MAX_MEMORY = 8192 KB,                          -- session RAM cap
    EVENT_RETENTION_MODE = ALLOW_SINGLE_EVENT_LOSS, -- do not change to NO_EVENT_LOSS
    MAX_DISPATCH_LATENCY = 30 SECONDS,             -- flush cadence
    STARTUP_STATE = OFF                            -- does not return after restart
    -- On a busy many-core host, add the line below and raise MAX_MEMORY
    -- to 16-32 MB first:
    -- , MEMORY_PARTITION_MODE = PER_CPU
);
GO

-- CREATE leaves the session stopped. Uncomment and run this to start
-- capture. Nothing is recorded until you do.
--
-- ALTER EVENT SESSION [WorkloadReport_XE] ON SERVER STATE = START;
-- GO

-- After you have collected data for the time you need, copy every .xel
-- file off the server, then run the statement below to stop the session.
-- Leaving it running keeps using CPU and disk. Use the same session name
-- as CREATE / START.
--
-- ALTER EVENT SESSION [WorkloadReport_XE] ON SERVER STATE = STOP;
-- GO
