# SSC-FDM-SSIS0005 — Package Converted to Stored Procedure

An SSIS package was converted to a Snowflake stored procedure (PROCEDURE) instead of a task (TASK) because it is called by Execute Package tasks from other packages. The CALL pattern matches SSIS behavior: synchronous, blocking execution.

## Quick Reference

| Aspect | Detail |
|--------|--------|
| Marker type | Inline FDM comment (not `!!!RESOLVE EWI!!!`) |
| Breaks compilation? | **No** |
| Frequency | Low-to-moderate (once per child package) |
| Common action | No code change needed — informational |

## Identification

Look for the marker:
```
--** SSC-FDM-SSIS0005 - PACKAGE CONVERTED TO PROCEDURE INSTEAD OF TASK BECAUSE IT IS CALLED BY EXECUTEPACKAGE TASKS FROM OTHER PACKAGES. THE CALL PATTERN MATCHES SSIS SYNCHRONOUS EXECUTION BEHAVIOR. **
```

It appears before the `CREATE OR REPLACE PROCEDURE` statement for the converted package:

```sql
--** SSC-FDM-SSIS0005 - PACKAGE CONVERTED TO PROCEDURE INSTEAD OF TASK BECAUSE IT IS CALLED BY EXECUTEPACKAGE TASKS FROM OTHER PACKAGES. THE CALL PATTERN MATCHES SSIS SYNCHRONOUS EXECUTION BEHAVIOR. **
CREATE OR REPLACE PROCEDURE public.child_package_load_data()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
BEGIN
   -- ... converted package logic ...
   RETURN 'SUCCESS';
END;
$$;
```

The calling parent package invokes it via:
```sql
CALL public.child_package_load_data();
```

## Fix Patterns

### Pattern 1: No change needed (most common)

The PROCEDURE + CALL pattern correctly replicates SSIS Execute Package Task behavior. The child package runs synchronously inside the parent, just like in SSIS.

```sql
-- No change needed. The conversion is correct.
--** SSC-FDM-SSIS0005 - PACKAGE CONVERTED TO PROCEDURE INSTEAD OF TASK ... **
CREATE OR REPLACE PROCEDURE public.child_package_load_data()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
BEGIN
   INSERT INTO target_table SELECT * FROM staging_table;
   RETURN 'SUCCESS';
END;
$$;
```

### Pattern 2: Verify parameter passing

If the SSIS parent package passed parameters to the child package, verify they are correctly mapped as procedure arguments:

```sql
-- SSIS: ExecutePackage with parameter bindings
-- Snowflake: Parameters become procedure arguments
CALL public.child_package_load_data(:User_BatchId, :User_LoadDate);
```

## Key Points

- This marker is **purely informational**. No code change is needed.
- Do **NOT** remove the FDM comment.
- The PROCEDURE (not TASK) choice is intentional — TASKs run on schedules or triggers, while PROCEDUREs support synchronous CALL semantics matching SSIS ExecutePackage behavior.
- If the same package is also invoked independently (not only as a child), it may need both a PROCEDURE and a TASK wrapper.
