# SSC-FDM-SSIS0006 — Event Handler Not Triggered

SnowConvert successfully converted an SSIS event handler (OnError, OnPreExecute, OnPostExecute, etc.) into a Snowflake stored procedure, but nothing automatically calls it. In SSIS, these handlers fire automatically on events. In Snowflake, they must be invoked explicitly.

## Quick Reference

| Aspect | Detail |
|--------|--------|
| Marker type | Inline FDM comment (not `!!!RESOLVE EWI!!!`) |
| Breaks compilation? | **No** |
| Frequency | Low-to-moderate (once per event handler per package) |
| Common action | Wire up error handler or mark logging handlers as optional |

## Identification

Look for the marker:
```
--** SSC-FDM-SSIS0006 - EVENT HANDLER STORED PROCEDURE CREATED BUT NOT AUTOMATICALLY TRIGGERED. MANUAL INVOCATION OR TRIGGERING MECHANISM IMPLEMENTATION REQUIRED. **
```

It appears immediately before a `CREATE OR REPLACE PROCEDURE` statement that contains the converted event handler logic:

```sql
--** SSC-FDM-SSIS0006 - EVENT HANDLER STORED PROCEDURE CREATED BUT NOT AUTOMATICALLY TRIGGERED. MANUAL INVOCATION OR TRIGGERING MECHANISM IMPLEMENTATION REQUIRED. **
CREATE OR REPLACE PROCEDURE public.package_onerror_handler ()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
   BEGIN
      -- Converted event handler logic here
      insert INTO ErrorTable (PackageName, StepName, ErrorDescription)
      VALUES (:System_ErrorDescription, :System_PackageName, :System_SourceName);
      RETURN 'SUCCESS';
   END;
$$;
```

## Decision Tree

1. **Is this an OnError handler?**
   - The handler contains error logging or notification logic.
   - **Action:** Add `EXCEPTION WHEN OTHER THEN CALL handler()` in the task(s) that should trigger it. See Fix Pattern 1.

2. **Is this an OnPreExecute or OnPostExecute handler?**
   - Often used for audit logging (start/end timestamps, row counts).
   - Snowflake tasks have built-in execution history via `TASK_HISTORY()`.
   - **Action:** Evaluate if the logging is redundant. If the logic writes to a custom audit table that downstream reports consume, wire it up. Otherwise, mark as optional.

3. **Is this an OnWarning or OnInformation handler?**
   - Typically logging-only with no business logic impact.
   - **Action:** Usually not needed. Mark as informational.

4. **Does the handler contain business logic beyond logging?**
   - Rarely, event handlers perform compensating actions (e.g., cleanup on error).
   - **Action:** Wire up the handler call. For OnError, use the EXCEPTION pattern.

## Fix Patterns

### Pattern 1: Wire up OnError handler in calling tasks

```sql
-- Before: Task has no error handling
CREATE OR REPLACE TASK public.package_load_data
WAREHOUSE=DUMMY_WAREHOUSE
AFTER public.package_init
AS
BEGIN
   INSERT INTO target_table SELECT * FROM staging_table;
END;

-- After: Task calls the OnError handler on failure
CREATE OR REPLACE TASK public.package_load_data
WAREHOUSE=DUMMY_WAREHOUSE
AFTER public.package_init
AS
BEGIN
   INSERT INTO target_table SELECT * FROM staging_table;
EXCEPTION
   WHEN OTHER THEN
      CALL public.package_onerror_handler();
      RAISE;
END;
```

### Pattern 2: OnPreExecute/OnPostExecute — often not needed

```sql
-- The handler procedure exists but may not need wiring.
-- Snowflake provides built-in task monitoring:
--   SELECT * FROM TABLE(INFORMATION_SCHEMA.TASK_HISTORY())
--   WHERE NAME = 'PACKAGE_LOAD_DATA';

-- If the audit table IS consumed by downstream processes, wire it up:
CREATE OR REPLACE TASK public.package_load_data
WAREHOUSE=DUMMY_WAREHOUSE
AFTER public.package_init
AS
BEGIN
   CALL public.package_onpreexecute_handler();
   -- ... main task logic ...
   CALL public.package_onpostexecute_handler();
EXCEPTION
   WHEN OTHER THEN
      CALL public.package_onerror_handler();
      RAISE;
END;
```

### Pattern 3: Mark handler as informational (no wiring needed)

```sql
-- No code change to the procedure or tasks.
-- The procedure is preserved for reference but not called.
-- If needed later, it can be wired up manually.

--** SSC-FDM-SSIS0006 - EVENT HANDLER STORED PROCEDURE CREATED BUT NOT AUTOMATICALLY TRIGGERED. MANUAL INVOCATION OR TRIGGERING MECHANISM IMPLEMENTATION REQUIRED. **
CREATE OR REPLACE PROCEDURE public.package_onerror_handler ()
-- Procedure preserved as-is. Snowflake task history provides equivalent monitoring.
```

## Key Points

- Do **NOT** delete the handler procedure. It contains converted business logic that may be needed.
- Do **NOT** remove the FDM comment.
- Handler procedure names typically follow the pattern `package_on<event>_handler`.
- For the PoC, the most pragmatic approach is to wire up OnError handlers (Pattern 1) and mark other handlers as informational unless the user confirms they are needed.
- The handler procedure may itself contain other EWI/FDM markers (e.g., SSC-FDM-0007 for missing tables) that need separate evaluation.
