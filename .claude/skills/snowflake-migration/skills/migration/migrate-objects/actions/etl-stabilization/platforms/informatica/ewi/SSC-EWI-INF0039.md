# SSC-EWI-INF0039 — dbt Folder Hooks Execute Per-Model, Not Per-Session

Disconnected stored procedures translated to dbt folder-level hooks (`+pre-hook` / `+post-hook`) execute once per model in the folder, not once per session as in Informatica. This can cause issues for non-idempotent operations.

## Quick Reference

| Aspect | Detail |
|--------|--------|
| Marker type | Inline FDM comment (embedded in SQL) |
| Breaks compilation? | **No** |
| Frequency | Low (only emitted when mapping has >1 target) |
| Common action | Make hook idempotent, or move to `on-run-start`/`on-run-end` |

## Identification

Look for the marker in `dbt_project.yml` hook entries or inline in SQL:
```sql
CALL dbo.TRUNCATE_TABLE('EMPLOYEES_STG') /*SSC-EWI-INF0039[dbt folder hooks execute once per model, not once per session.]*/
```

## Context

| Aspect | Informatica | dbt |
|--------|-------------|-----|
| Granularity | Executes **once per session** (beginning/end of workflow) | Executes **once per model** in the folder |
| Scope | Session-wide side effect | Model-scoped side effect |
| Idempotency | Not required (runs exactly once) | **Required** (runs N times for N models) |

### Why This Matters

If an Informatica pre-load procedure performs a one-time operation (e.g., truncating a staging table), the dbt equivalent will execute that truncation before **every model** in the folder. The second run would truncate data inserted by the first model.

## Fix Patterns

### Pattern 1: Make the hook idempotent

If the SP truncates a table, ensure it's safe to call multiple times:
```sql
-- The TRUNCATE is already idempotent — truncating an empty table is a no-op
CALL dbo.TRUNCATE_TABLE('EMPLOYEES_STG')
```

### Pattern 2: Move to on-run-start / on-run-end

For truly session-scoped operations that must run exactly once:
```yaml
# dbt_project.yml
on-run-start:
  - "CALL dbo.INIT_SESSION()"
on-run-end:
  - "CALL dbo.CLEANUP_SESSION()"
```

### Pattern 3: Add guard logic

Add conditional logic to prevent re-execution:
```sql
-- Only truncate if the table has data from a previous run
BEGIN
  IF ((SELECT COUNT(*) FROM EMPLOYEES_STG) > 0) THEN
    TRUNCATE TABLE EMPLOYEES_STG;
  END IF;
END;
```

## Key Points

- This EWI does **not** break compilation.
- It only appears when the mapping has multiple targets (single-target mappings have no difference).
- The core issue is **idempotency** — ensure hooks are safe to call repeatedly.
- For session-scoped operations, prefer `on-run-start`/`on-run-end` over folder hooks.
