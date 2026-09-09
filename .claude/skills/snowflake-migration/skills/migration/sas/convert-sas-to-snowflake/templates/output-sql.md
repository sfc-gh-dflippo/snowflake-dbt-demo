# SQL Output Template

Use this template when presenting SQL conversion results.

---

## File Header Format (MANDATORY)

All output `.sql` files MUST begin with this standard header:

```sql
-- ============================================================
-- Converted from: script_name.sas
-- Target Schema: DATABASE.SCHEMA
-- Translation Tier: SQL (all blocks) | Mixed (SQL + Stored Procedure)
-- ============================================================

USE SCHEMA DATABASE.SCHEMA;
```

---

## Single File Conversion

```markdown
## Original SAS Code

**File:** `{filename}.sas`

```sas
{original_sas_code}
```

---

## Snowflake SQL Conversion

**File:** `{filename}.sql`

```sql
{converted_sql_code}
```

---

## Conversion Notes

| Aspect | Details |
|--------|---------|
| **Translation Method** | SQL / Window Functions / Stored Procedure |
| **Confidence Level** | HIGH / MEDIUM / LOW |
| **Blocks Converted** | {count} |
| **PySpark Fallback** | None / {blocks requiring PySpark} |

### Key Transformations

- {transformation_1}
- {transformation_2}

### Assumptions Made

- {assumption_1}
- {assumption_2}

### Validation Status

- [ ] Compiled successfully
- [ ] Syntax verified
```

---

## Batch Conversion Summary

```markdown
## Batch Conversion Results

**Source Directory:** `{source_path}`
**Target Schema:** `{target_schema}`
**Total Scripts:** {count}

### Conversion Summary

| Original File | Output File | Method | Confidence |
|---------------|-------------|--------|------------|
| script_a.sas | script_a.sql | SQL | HIGH |
| script_b.sas | script_b.sql | Window Functions | HIGH |
| script_c.sas | script_c_notebook.py | PySpark | MEDIUM |

### Statistics

- **SQL translations:** {sql_count}
- **PySpark fallbacks:** {pyspark_count}
- **High confidence:** {high_count}
- **Medium confidence:** {medium_count}
- **Low confidence:** {low_count}

### Files Generated

#### SQL Files
- `sql/script_a.sql`
- `sql/script_b.sql`

#### PySpark Notebooks
- `notebooks/script_c_notebook.py`
```

---

## Stored Procedure Output

```markdown
## Snowflake Stored Procedure

**Procedure Name:** `{schema}.{procedure_name}`

```sql
CREATE OR REPLACE PROCEDURE {schema}.{procedure_name}()
RETURNS STRING
LANGUAGE SQL
AS
$$
DECLARE
    -- Variable declarations
BEGIN
    -- Procedure body
    
    RETURN 'Success';
END;
$$;
```

### Execution

```sql
CALL {schema}.{procedure_name}();
```

### Notes

- {note_1}
- {note_2}
```

---

## Untranslated Section Template

```sql
-- ============================================================
-- WARNING: UNTRANSLATED/LOW CONFIDENCE SECTION
-- Reason: {specific_reason}
-- Original SAS Code:
-- {original_sas_code_commented}
-- ============================================================
-- TODO: Manual review required
-- Suggested approach: {suggestion}
-- ============================================================
```

---

## Validation Report

```markdown
## Validation Results

| File | Compile Status | Errors |
|------|----------------|--------|
| script_a.sql | ✅ Success | None |
| script_b.sql | ❌ Failed | {error_message} |

### Error Details

**File:** `script_b.sql`
**Error:** {detailed_error}
**Fix Applied:** {fix_description}
**Revalidation:** ✅ Success
```
