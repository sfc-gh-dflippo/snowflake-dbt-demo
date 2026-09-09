# SSC-EWI-SSIS0002 — SSIS Expression Cannot Be Converted

An SSIS expression used in a Data Flow column derivation could not be automatically translated to Snowflake SQL. The `!!!RESOLVE EWI!!!` marker and a placeholder `_` are emitted in place of the expression, which **breaks compilation**.

## Quick Reference

| Aspect | Detail |
|--------|--------|
| Marker type | `!!!RESOLVE EWI!!!` (compilation-breaking) |
| Breaks compilation? | **Yes** |
| Frequency | Moderate (once per unconverted expression) |
| Action required | Replace placeholder with valid Snowflake SQL |

## Identification

Look for the marker:
```
!!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0002 - SSIS EXPRESSION CANNOT BE CONVERTED TO SNOWFLAKE SQL: <original SSIS expression> ***/!!!
```

Followed by a placeholder in the SELECT column list:
```sql
!!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0002 - SSIS EXPRESSION CANNOT BE CONVERTED TO SNOWFLAKE SQL: (DT_WSTR,50)@[User::varBatchTagAppend] ***/!!!
_ AS BatchTag,
```

The `_` is not valid SQL and will cause a compilation error. The original SSIS expression is preserved in the marker comment.

## Fix Process

1. **Read the original SSIS expression** from the marker comment
2. **Check the CONFIG block** at the top of the parent task graph file for variable definitions (SSIS `User::VarName` becomes `User_VarName`)
3. **Translate the expression** to Snowflake SQL using the patterns below
4. **Remove the `!!!RESOLVE EWI!!!` marker line entirely**
5. **Replace the `_` placeholder** with the translated expression

## SSIS Expression → Snowflake SQL Mappings

| SSIS Expression | Snowflake SQL |
|-----------------|---------------|
| `@[User::VarName]` | `{{ var('User_VarName') }}` (in dbt model) or `:User_VarName` (in task) |
| `(DT_WSTR,50)expr` | `expr::VARCHAR(50)` |
| `(DT_I4)expr` | `expr::INT` |
| `(DT_DBTIMESTAMP)expr` | `expr::TIMESTAMP_NTZ` |
| `(DT_DBDATE)expr` | `expr::DATE` |
| `(DT_R8)expr` | `expr::DOUBLE` |
| `(DT_DECIMAL,2)expr` | `expr::DECIMAL(38,2)` |
| `GETDATE()` | `CURRENT_TIMESTAMP()` |
| `(DT_WSTR,10)GETDATE()` | `CURRENT_TIMESTAMP()::VARCHAR(10)` |
| `@[User::Var1] + @[User::Var2]` | String: `User_Var1 \|\| User_Var2`; Numeric: `User_Var1 + User_Var2` |
| `ISNULL(expr) ? replacement : expr` | `NVL(expr, replacement)` |
| `TRIM(expr)` | `TRIM(expr)` |
| `UPPER(expr)` | `UPPER(expr)` |
| `SUBSTRING(expr,start,len)` | `SUBSTR(expr, start, len)` |

## Fix Patterns

### Pattern 1: Variable reference with type cast (most common)

The SSIS expression `(DT_WSTR,50)@[User::varBatchTagAppend]` means "cast the SSIS variable varBatchTagAppend to a 50-character string."

```sql
-- Before (in dbt model file — breaks compilation)
SELECT
   '1' AS ImportType,
   !!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0002 - SSIS EXPRESSION CANNOT BE CONVERTED TO SNOWFLAKE SQL: (DT_WSTR,50)@[User::varBatchTagAppend] ***/!!!
   _ AS BatchTag,
   SourcePracticeCode

-- After (valid Snowflake SQL)
SELECT
   '1' AS ImportType,
   {{ var('User_varBatchTagAppend') }}::VARCHAR(50) AS BatchTag,
   SourcePracticeCode
```

### Pattern 2: Same variable in a task (not a dbt model)

```sql
-- Before (in task body — breaks compilation)
SELECT
   !!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0002 - SSIS EXPRESSION CANNOT BE CONVERTED TO SNOWFLAKE SQL: (DT_WSTR,50)@[User::varBatchTag] ***/!!!
   _ AS BatchTag
FROM source_table;

-- After
SELECT
   :User_varBatchTag::VARCHAR(50) AS BatchTag
FROM source_table;
```

### Pattern 3: Date/time expression

```sql
-- Before
!!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0002 - SSIS EXPRESSION CANNOT BE CONVERTED TO SNOWFLAKE SQL: (DT_DBTIMESTAMP)GETDATE() ***/!!!
_ AS LoadDate,

-- After
CURRENT_TIMESTAMP()::TIMESTAMP_NTZ AS LoadDate,
```

### Pattern 4: Concatenation expression

```sql
-- Before
!!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0002 - SSIS EXPRESSION CANNOT BE CONVERTED TO SNOWFLAKE SQL: @[User::Prefix] + "_" + @[User::TableName] ***/!!!
_ AS FullName,

-- After (in dbt model)
{{ var('User_Prefix') }} || '_' || {{ var('User_TableName') }} AS FullName,
```

## Where to Find Variable Definitions

SSIS variables are declared in the `CONFIG` block at the top of the parent task graph `.sql` file:

```sql
CONFIG = $${
  "package": {
    "User_varBatchTagAppend": {"value": "BatchTag_2025", "type": "VARCHAR", "is_parameter": false},
    "User_FilterYear": {"value": 0, "type": "NUMBER", "is_parameter": false}
  }
}$$
```

The naming convention: SSIS `User::varBatchTagAppend` → Snowflake `User_varBatchTagAppend`.

## Key Points

- **Must** remove the `!!!RESOLVE EWI!!!` marker line — it breaks compilation.
- **Must** replace the `_` placeholder with a valid SQL expression.
- Always check the `CONFIG` block in the parent task graph file to find variable names and types.
- In dbt models, use `{{ var('Variable_Name') }}`; in task bodies, use `:Variable_Name`.
- The SSIS type cast syntax `(DT_TYPE,precision)` maps to Snowflake `::TYPE(precision)`.
- When unsure about the intended semantics of a complex expression, mark as needs-user with the original SSIS expression quoted in a comment.
