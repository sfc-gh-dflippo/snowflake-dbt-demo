# SSC-EWI-INF0003 — Workflow Element Cannot Be Converted

An Informatica PowerCenter workflow element (Timer, unsupported task type, etc.) has no direct Snowflake equivalent. The `!!!RESOLVE EWI!!!` marker **breaks compilation**. The original XML is preserved as comments for reference.

## Quick Reference

| Aspect | Detail |
|--------|--------|
| Marker type | `!!!RESOLVE EWI!!!` (compilation-breaking) |
| Breaks compilation? | **Yes** |
| Frequency | Low-moderate (once per unconvertible workflow element) |
| Common action | Remove marker, keep XML comments, add needs-user recommendation |

## Identification

Look for the marker:
```
!!!RESOLVE EWI!!! /*** SSC-EWI-INF0003 - INFORMATICA POWERCENTER WORKFLOW ELEMENT <ElementType> CANNOT BE CONVERTED TO SNOWFLAKE SCRIPTING. ***/!!!
```

Followed by the original workflow XML commented out:
```sql
!!!RESOLVE EWI!!! /*** SSC-EWI-INF0003 - INFORMATICA POWERCENTER WORKFLOW ELEMENT Timer CANNOT BE CONVERTED TO SNOWFLAKE SCRIPTING. ***/!!!
--<TASK NAME="my_timer" TYPE="Timer" REUSABLE="NO" DESCRIPTION="" VERSIONNUMBER="1">
--  <ATTRIBUTE NAME="Variable" VALUE="" />
--  <TIMER TIMERTYPE="START_RELATIVE_TO_PREVIOUSTASK">
--    <RECURRING DAYS="0" HOURS="0" MINUTES="1" />
--  </TIMER>
--</TASK>
 ;
```

The trailing `;` is a placeholder statement to maintain syntactic structure.

## Decision Tree

1. **What type of workflow element is it?**
   - Identify the `TYPE` attribute from the commented XML.
   - Use the element type table below to determine the recommended approach.

2. **Is it a Timer task?**
   - Timers introduce wait/delay between tasks.
   - **Action:** Remove marker. If the delay is critical for orchestration, add a comment noting the original timing and suggest configuring the downstream Snowflake TASK with `SCHEDULE`. Avoid `SYSTEM$WAIT` — it blocks the warehouse and incurs compute costs.

3. **Is it a Command task?**
   - Runs shell/OS commands.
   - **Action:** Mark as needs-user. Evaluate if the command can be replaced with Snowflake stage operations or stored procedures.

4. **Is it an Email task?**
   - Sends notification emails.
   - **Action:** Mark as needs-user. Suggest `SYSTEM$SEND_EMAIL` or external notification service.

5. **Is it a Control (Stop/Abort) task?**
   - Stops or aborts the workflow.
   - **Action:** Replace with `SYSTEM$ABORT_SESSION` or error handling logic.

## Element Type Reference

| Informatica Element | Snowflake Approach | Auto-fixable? |
|--------------------|-------------------|---------------|
| `Timer` | Task `SCHEDULE` (preferred) or `SYSTEM$WAIT` (last resort — blocks warehouse) | Partially |
| `Command` | Stored procedure or external | No |
| `Email` | `SYSTEM$SEND_EMAIL` / external | No |
| `Control` (Stop/Abort) | `SYSTEM$ABORT_SESSION` | Partially |

## Fix Patterns

### Pattern 1: Timer — remove or replace with scheduling

```sql
-- Before (breaks compilation)
!!!RESOLVE EWI!!! /*** SSC-EWI-INF0003 - INFORMATICA POWERCENTER WORKFLOW ELEMENT Timer CANNOT BE CONVERTED TO SNOWFLAKE SCRIPTING. ***/!!!
--<TASK NAME="my_timer" TYPE="Timer" ...>
--  <TIMER TIMERTYPE="START_RELATIVE_TO_PREVIOUSTASK">
--    <RECURRING DAYS="0" HOURS="0" MINUTES="1" />
--  </TIMER>
--</TASK>
 ;

-- After (marker removed, timing noted)
-- NEEDS-USER: Original Informatica Timer waited 1 minute between tasks.
-- Preferred: configure the downstream Snowflake TASK with SCHEDULE = '1 MINUTE'.
-- Avoid SYSTEM$WAIT(60) — it blocks the warehouse for the duration, incurring
-- compute costs. Only use SYSTEM$WAIT for sub-minute delays where task
-- scheduling granularity is insufficient.
```

### Pattern 2: Command task — mark as needs-user

```sql
-- Before (breaks compilation)
!!!RESOLVE EWI!!! /*** SSC-EWI-INF0003 - INFORMATICA POWERCENTER WORKFLOW ELEMENT Command CANNOT BE CONVERTED TO SNOWFLAKE SCRIPTING. ***/!!!
--<TASK NAME="cmd_cleanup" TYPE="Command" ...>
--  <ATTRIBUTE NAME="Command" VALUE="rm -f /tmp/staging/*.csv"/>
--</TASK>
 ;

-- After (marker removed, needs-user recommendation)
-- NEEDS-USER: Original Informatica Command task ran: rm -f /tmp/staging/*.csv
-- If staging files are in a Snowflake stage, use REMOVE @stage/pattern.
-- Otherwise, move this to an external orchestrator.
```

### Pattern 3: Minimal fix — remove marker only

```sql
-- Before (breaks compilation)
!!!RESOLVE EWI!!! /*** SSC-EWI-INF0003 - INFORMATICA POWERCENTER WORKFLOW ELEMENT Email CANNOT BE CONVERTED TO SNOWFLAKE SCRIPTING. ***/!!!
--<TASK NAME="notify_admin" TYPE="Email" .../>
 ;

-- After (compiles, needs manual implementation)
-- NEEDS-USER: Informatica Email task requires manual replacement.
-- Consider SYSTEM$SEND_EMAIL or external notification service.
--<TASK NAME="notify_admin" TYPE="Email" .../>
```

## Key Points

- **Must** remove the `!!!RESOLVE EWI!!!` marker line — it breaks compilation.
- **Keep** the commented XML for reference unless the element is fully replaced.
- Ensure the surrounding task body remains syntactically valid after removing the marker.
- The trailing ` ;` after the commented XML is intentional — keep it as a no-op placeholder.
