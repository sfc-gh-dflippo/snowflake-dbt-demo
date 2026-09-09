# SQL Server Query Logging

Capture real stored procedure and function invocations from SQL Server using Extended Events. The captured query logs can be exported as CSV and fed into the [baseline-capture](../baseline-capture/SKILL.md) tool to generate test configs.

## Enable Query Logging

Create an Extended Events session that captures all queries to a specific database.

**Replace `YOUR_DATABASE` with the actual database name.**

```sql
-- Drop existing session if exists
IF EXISTS (SELECT * FROM sys.server_event_sessions WHERE name = 'QueryCapture')
BEGIN
    DROP EVENT SESSION [QueryCapture] ON SERVER;
END
GO

-- Create Extended Events session
CREATE EVENT SESSION [QueryCapture] ON SERVER
ADD EVENT sqlserver.sql_statement_completed(
    ACTION(
        sqlserver.sql_text,
        sqlserver.database_name,
        sqlserver.username,
        sqlserver.client_app_name,
        sqlserver.session_id
    )
    WHERE ([database_name] = N'YOUR_DATABASE')
),
ADD EVENT sqlserver.rpc_completed(
    ACTION(
        sqlserver.sql_text,
        sqlserver.database_name,
        sqlserver.username,
        sqlserver.client_app_name,
        sqlserver.session_id
    )
    WHERE ([database_name] = N'YOUR_DATABASE')
)
ADD TARGET package0.event_file(
    SET filename = N'/var/opt/mssql/log/query_capture.xel',
    max_file_size = 100,
    max_rollover_files = 5
)
WITH (
    MAX_MEMORY = 4096 KB,
    EVENT_RETENTION_MODE = ALLOW_SINGLE_EVENT_LOSS,
    MAX_DISPATCH_LATENCY = 5 SECONDS,
    STARTUP_STATE = ON
);
GO

-- Start the session
ALTER EVENT SESSION [QueryCapture] ON SERVER STATE = START;
GO

-- Verify session is running
SELECT 
    name,
    create_time,
    CASE WHEN ses.session_id IS NOT NULL THEN 'RUNNING' ELSE 'STOPPED' END AS status
FROM sys.server_event_sessions s
LEFT JOIN sys.dm_xe_sessions ses ON s.name = ses.name
WHERE s.name = 'QueryCapture';
GO
```

**Notes:**
- The `filename` path is for Linux-based SQL Server. For Windows, use a path like `C:\temp\query_capture.xel`.
- Adjust `max_file_size` (MB) and `max_rollover_files` based on expected query volume.
- `STARTUP_STATE = ON` means the session will auto-start on SQL Server restart.

## Export Captured Queries

After letting the session run for a representative period (e.g., during normal application usage), export the captured queries.

### View All Captured Queries

```sql
SELECT 
    Timestamp = event_data.value('(@timestamp)[1]', 'datetime2'),
    EventType = event_data.value('(@name)[1]', 'nvarchar(50)'),
    DatabaseName = event_data.value('(action[@name="database_name"]/value)[1]', 'nvarchar(128)'),
    Username = event_data.value('(action[@name="username"]/value)[1]', 'nvarchar(128)'),
    ClientApp = event_data.value('(action[@name="client_app_name"]/value)[1]', 'nvarchar(128)'),
    SessionID = event_data.value('(action[@name="session_id"]/value)[1]', 'int'),
    Statement = event_data.value('(data[@name="statement"]/value)[1]', 'nvarchar(max)'),
    DurationMicroseconds = event_data.value('(data[@name="duration"]/value)[1]', 'bigint'),
    CPUTime = event_data.value('(data[@name="cpu_time"]/value)[1]', 'bigint'),
    LogicalReads = event_data.value('(data[@name="logical_reads"]/value)[1]', 'bigint'),
    RowCount = event_data.value('(data[@name="row_count"]/value)[1]', 'bigint')
FROM (
    SELECT CAST(event_data AS XML) AS event_data
    FROM sys.fn_xe_file_target_read_file('/var/opt/mssql/log/query_capture*.xel', NULL, NULL, NULL)
) AS events
ORDER BY Timestamp;
GO
```

### Summary by Query Type

```sql
SELECT 
    QueryType = CASE 
        WHEN Statement LIKE 'EXEC%' THEN 'Stored Procedure'
        WHEN Statement LIKE 'SELECT%' THEN 'SELECT'
        WHEN Statement LIKE 'INSERT%' THEN 'INSERT'
        WHEN Statement LIKE 'UPDATE%' THEN 'UPDATE'
        WHEN Statement LIKE 'DELETE%' THEN 'DELETE'
        ELSE 'Other'
    END,
    QueryCount = COUNT(*),
    AvgDurationMs = AVG(DurationMicroseconds) / 1000.0
FROM (
    SELECT 
        Statement = event_data.value('(data[@name="statement"]/value)[1]', 'nvarchar(max)'),
        DurationMicroseconds = event_data.value('(data[@name="duration"]/value)[1]', 'bigint')
    FROM (
        SELECT CAST(event_data AS XML) AS event_data
        FROM sys.fn_xe_file_target_read_file('/var/opt/mssql/log/query_capture*.xel', NULL, NULL, NULL)
    ) AS events
) AS parsed
GROUP BY CASE 
    WHEN Statement LIKE 'EXEC%' THEN 'Stored Procedure'
    WHEN Statement LIKE 'SELECT%' THEN 'SELECT'
    WHEN Statement LIKE 'INSERT%' THEN 'INSERT'
    WHEN Statement LIKE 'UPDATE%' THEN 'UPDATE'
    WHEN Statement LIKE 'DELETE%' THEN 'DELETE'
    ELSE 'Other'
END
ORDER BY QueryCount DESC;
GO
```

### Export Unique Procedure Calls (for Baseline Capture)

This is the query most useful for generating baseline configs:

```sql
SELECT DISTINCT
    Statement = event_data.value('(data[@name="statement"]/value)[1]', 'nvarchar(max)')
FROM (
    SELECT CAST(event_data AS XML) AS event_data
    FROM sys.fn_xe_file_target_read_file('/var/opt/mssql/log/query_capture*.xel', NULL, NULL, NULL)
) AS events
WHERE event_data.value('(data[@name="statement"]/value)[1]', 'nvarchar(max)') LIKE 'exec %'
ORDER BY Statement;
GO
```

Export the results to CSV, then feed it to `scai test seed --execution-log <path>` to populate test YAML stubs. See [`references/step-based-yaml.md`](step-based-yaml.md) for the YAML schema.

## Stop Query Logging

```sql
-- Stop the session (keeps it for later restart)
ALTER EVENT SESSION [QueryCapture] ON SERVER STATE = STOP;
GO

-- Or drop entirely
-- DROP EVENT SESSION [QueryCapture] ON SERVER;
-- GO
```

## Tips

- Run the session during **representative application usage** (not just idle time) to capture realistic procedure calls with realistic parameters.
- The `rpc_completed` event captures parameterized stored procedure calls (from application code using `SqlCommand.CommandType = StoredProcedure`).
- The `sql_statement_completed` event captures ad-hoc SQL including `EXEC` statements.
- For high-volume databases, consider adding duration filters to capture only slower queries: `WHERE ([duration] > 1000)` (microseconds).
