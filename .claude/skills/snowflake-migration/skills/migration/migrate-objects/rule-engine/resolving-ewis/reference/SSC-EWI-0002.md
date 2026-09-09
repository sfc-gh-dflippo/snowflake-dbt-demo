# SSC-EWI-0002 - Default Parameters Must Be Reordered

Snowflake requires all parameters with default values to be declared **at the end** of the parameter list. Non-default (required) parameters cannot appear after parameters with defaults.

## Quick Reference

| SQL Server | Snowflake Requirement |
|------------|----------------------|
| Default params can be anywhere | Default params must be at the end |
| `@param1 INT = NULL, @param2 INT, @param3 INT = 0` | `param2 INT, param1 INT DEFAULT NULL, param3 INT DEFAULT 0` |

## Identification

Look for the marker:
```
!!!RESOLVE EWI!!! /*** SSC-EWI-0002 - DEFAULT PARAMETERS MAY NEED TO BE REORDERED. SNOWFLAKE ONLY SUPPORTS DEFAULT PARAMETERS AT THE END OF THE PARAMETERS DECLARATIONS ***/!!!
```

## Fix Process

1. **Identify all parameters** in the procedure declaration
2. **Categorize each parameter:**
   - **Required** (no default value)
   - **Optional** (has `DEFAULT` clause)
3. **Reorder parameters:**
   - All required parameters first
   - All optional parameters last
4. **Preserve parameter names and types** - only change the order
5. **Remove** the `!!!RESOLVE EWI!!!` marker

## Example

### Before (Invalid in Snowflake)
```sql
CREATE OR REPLACE PROCEDURE my_procedure (
    IMPORTSOURCE STRING,              -- No default ✓
    FILEPATH STRING DEFAULT NULL,     -- Has default
    FORMATFILEPATH STRING DEFAULT NULL, -- Has default
    BUDGETDATA VARIANT,               -- No default ✗ (after defaults!)
    TARGETID INT,                     -- No default ✗ (after defaults!)
    BATCHSIZE INT DEFAULT 10000       -- Has default
)
```

### After (Valid in Snowflake)
```sql
CREATE OR REPLACE PROCEDURE my_procedure (
    -- Required parameters (no defaults) first
    IMPORTSOURCE STRING,
    BUDGETDATA VARIANT,
    TARGETID INT,
    -- Optional parameters (with defaults) last
    FILEPATH STRING DEFAULT NULL,
    FORMATFILEPATH STRING DEFAULT NULL,
    BATCHSIZE INT DEFAULT 10000
)
```

## Impact on Callers

Reordering parameters is a **breaking change** for callers using positional arguments.

| Calling Style | Impact |
|---------------|--------|
| Positional: `CALL proc('a', 'b', 'c')` | **Breaks** - must update argument order |
| Named: `CALL proc(param1 => 'a', param2 => 'b')` | **Safe** - order doesn't matter |

### Mitigation

- Update all callers to use the new parameter order, OR
- Convert callers to use named parameters (recommended for resilience)

## Boolean Defaults

When reordering, also fix boolean default values:

| SQL Server | Snowflake |
|------------|-----------|
| `@flag BIT = 1` | `FLAG BOOLEAN DEFAULT TRUE` |
| `@flag BIT = 0` | `FLAG BOOLEAN DEFAULT FALSE` |

## Key Points

- Required parameters **must** come before optional parameters
- Search the codebase for procedure calls before reordering
- Consider using named parameters in callers to avoid future issues
- Remove the `!!!RESOLVE EWI!!!` marker after fixing

## Resources

**Snowflake:**
- [CREATE PROCEDURE](https://docs.snowflake.com/en/sql-reference/sql/create-procedure)
- [Stored Procedures Overview](https://docs.snowflake.com/en/developer-guide/stored-procedures/stored-procedures-overview)
- [Calling Stored Procedures](https://docs.snowflake.com/en/sql-reference/sql/call)
