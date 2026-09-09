# SSC-EWI-SSIS0003 — Embedded SQL Not Converted

Embedded SQL statements within SSIS could not be converted due to T-SQL dialect incompatibilities. The `!!!RESOLVE EWI!!!` marker **breaks compilation**. The original T-SQL is preserved in the marker comment or as commented-out code.

## Quick Reference

| Aspect | Detail |
|--------|--------|
| Marker type | `!!!RESOLVE EWI!!!` (compilation-breaking) |
| Breaks compilation? | **Yes** |
| Frequency | Moderate (once per unconverted SQL statement) |
| Common action | Manually rewrite T-SQL to Snowflake SQL |

## Identification

Look for the marker:
```
!!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0003 - EMBEDDED SQL STATEMENT COULD NOT BE CONVERTED: <original T-SQL> ***/!!!
```

The original T-SQL appears inside the marker comment:

```sql
!!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0003 - EMBEDDED SQL STATEMENT COULD NOT BE CONVERTED: EXEC sp_rename @objname='dbo.Temp_Table', @newname='Final_Table' ***/!!!
```

## Fix Patterns

### Pattern 1: Stored procedure call (EXEC → CALL)

```sql
-- Before (breaks compilation)
!!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0003 - EMBEDDED SQL STATEMENT COULD NOT BE CONVERTED: EXEC dbo.usp_LoadCustomers @BatchId=1 ***/!!!

-- After
CALL dbo.usp_LoadCustomers(1);
```

### Pattern 2: T-SQL system procedure

```sql
-- Before (breaks compilation)
!!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0003 - EMBEDDED SQL STATEMENT COULD NOT BE CONVERTED: EXEC sp_rename @objname='dbo.Temp_Table', @newname='Final_Table' ***/!!!

-- After
ALTER TABLE dbo.Temp_Table RENAME TO dbo.Final_Table;
```

### Pattern 3: T-SQL syntax with no direct equivalent

```sql
-- Before (breaks compilation)
!!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0003 - EMBEDDED SQL STATEMENT COULD NOT BE CONVERTED: SELECT TOP 1 @Result = StatusCode FROM dbo.BatchStatus WITH (NOLOCK) WHERE BatchId = @BatchId ORDER BY CreateDate DESC ***/!!!

-- After
SELECT StatusCode INTO :Result
FROM dbo.BatchStatus
WHERE BatchId = :BatchId
ORDER BY CreateDate DESC
LIMIT 1;
```

### Common T-SQL → Snowflake mappings

| T-SQL | Snowflake |
|-------|-----------|
| `EXEC proc @param=val` | `CALL proc(val)` |
| `SELECT TOP N` | `SELECT ... LIMIT N` |
| `WITH (NOLOCK)` | Remove (Snowflake has no lock hints) |
| `sp_rename` | `ALTER TABLE ... RENAME TO` |
| `ISNULL(a, b)` | `NVL(a, b)` or `COALESCE(a, b)` |
| `GETDATE()` | `CURRENT_TIMESTAMP()` |
| `CONVERT(type, expr)` | `expr::type` or `TRY_CAST(expr AS type)` |

## Key Points

- **Must** remove the `!!!RESOLVE EWI!!!` marker line — it breaks compilation.
- Read the original T-SQL from inside the marker comment and rewrite it in Snowflake SQL.
- If the T-SQL is complex or references system procedures with no Snowflake equivalent, mark as needs-user.
- Multiple `SSC-EWI-SSIS0003` markers may appear in sequence when a single Execute SQL Task contained multiple statements.
