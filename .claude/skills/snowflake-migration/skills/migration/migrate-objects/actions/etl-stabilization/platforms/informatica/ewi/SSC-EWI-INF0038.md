# SSC-EWI-INF0038 — Stored Procedure Uses Named Connection

A stored procedure transformation references a named database connection (not `$Source` or `$Target`). The hook SQL is still generated, but the user must verify the procedure exists on the Snowflake target connection.

## Quick Reference

| Aspect | Detail |
|--------|--------|
| Marker type | Inline EWI comment (embedded in SQL) |
| Breaks compilation? | **No** |
| Frequency | Low (only when SP uses a custom named connection) |
| Common action | Verify SP exists on target, update connection if needed |

## Identification

Look for the marker in hook SQL or model SQL:
```sql
CALL dbo.MY_PROCEDURE('arg1') /*SSC-EWI-INF0038*/
```

Or in intermediate models for connected stored procedures:
```sql
!!!RESOLVE EWI!!! /*** SSC-EWI-INF0038 - STORED PROCEDURE 'SP_ConvertCurrency' USES NAMED CONNECTION 'MyCustomDB'. ***/!!!
```

## Context

In Informatica PowerCenter, stored procedure transformations can reference connections by:

| Connection Reference | Meaning | EWI? |
|---------------------|---------|------|
| `$Source` | Default source connection | No |
| `$Target` | Default target connection | No |
| `$DBConnectionName` | Default DB connection | No |
| Named (e.g., `EDWLOAD`, `MyCustomDB`) | Custom connection | **Yes — SSC-EWI-INF0038** |

Named connections indicate the SP may reside on a different database server than the primary source/target. In Snowflake, all hooks run against the dbt connection (a single Snowflake account).

## Fix Patterns

### Pattern 1: SP exists on Snowflake target

If the stored procedure has been migrated to Snowflake:
```sql
-- No change needed — the CALL will work if the SP exists
CALL dbo.MY_PROCEDURE('arg1')
```

### Pattern 2: SP is on a different database

If the SP is on a separate database not migrated to Snowflake:
```sql
-- NEEDS-USER: Original Informatica SP used connection 'MyCustomDB'.
-- The procedure may not exist on the Snowflake target.
-- Options:
--   1. Migrate the SP to Snowflake
--   2. Use an external function to call the remote procedure
--   3. Remove the hook if the SP is no longer needed
CALL dbo.MY_PROCEDURE('arg1')
```

## Key Points

- This EWI does **not** break compilation — the SQL is valid.
- The risk is runtime failure if the SP doesn't exist on Snowflake.
- Always verify the SP has been migrated before marking as resolved.
