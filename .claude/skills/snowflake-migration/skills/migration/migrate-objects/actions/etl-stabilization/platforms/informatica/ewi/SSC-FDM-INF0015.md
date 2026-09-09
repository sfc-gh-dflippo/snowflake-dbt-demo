# SSC-FDM-INF0015 — Update Strategy Logic Moved to Target Model

The Update Strategy transformation's DML operation logic has been moved from the intermediate model to the target model. This is an optimization for the common case where an Update Strategy connects directly to a single Target.

## Quick Reference

| Aspect | Detail |
|--------|--------|
| Marker type | Inline FDM comment (not `!!!RESOLVE EWI!!!`) |
| Breaks compilation? | **No** |
| Frequency | Common (97% of Update Strategy transformations) |
| Common action | Informational — verify target model's WHERE clauses match the intended DML strategy |

## Identification

Look for the marker in the target model:
```sql
--** SSC-FDM-INF0015 - UPDATE STRATEGY LOGIC HAS BEEN MOVED TO THE TARGET MODEL. **
```

## Context

When an Update Strategy connects directly to a single Target (97.1% of cases), the translator uses the **optimized path**:

- The Update Strategy model is `ephemeral` (no intermediate table)
- The DD_ expression is inlined as WHERE clauses in the target model
- No `etl_dml_operation__` control column is propagated

### Optimized vs Non-Optimized Paths

| Path | Condition | Update Strategy Model | Target Model |
|------|-----------|----------------------|-------------|
| **Optimized** | Exactly 1 downstream Target | `ephemeral` passthrough | Inlines expression into WHERE |
| **Non-optimized** | Multiple Targets or not directly connected | `table` with `etl_dml_operation__` column | Filters on control column |

### DML Operation Mapping

| DD_ Constant | Numeric Value | DML Operation |
|-------------|---------------|---------------|
| `DD_INSERT` | 0 | INSERT new rows |
| `DD_UPDATE` | 1 | UPDATE existing rows |
| `DD_DELETE` | 2 | DELETE rows (via pre_hook) |
| `DD_REJECT` | 3 | Reject/skip rows |

## Fix Patterns

### Pattern 1: Verify inlined WHERE clauses

Check that the target model's WHERE clauses correctly implement the intended DML strategy:

```sql
-- For DD_INSERT: rows where expression = 0
{{ config(materialized='incremental', incremental_strategy='append') }}
SELECT * FROM {{ ref('int_UPDTRANS') }}
WHERE /* DD_INSERT = 0 */ update_strategy_expr = 0

-- For DD_UPDATE: rows where expression = 1
{{ config(materialized='incremental', incremental_strategy='merge', unique_key='id') }}
SELECT * FROM {{ ref('int_UPDTRANS') }}
WHERE /* DD_UPDATE = 1 */ update_strategy_expr = 1
```

### Pattern 2: Non-optimized path with control column

When multiple targets consume the same Update Strategy:
```sql
-- Update Strategy intermediate model (materialized as table)
SELECT *, CASE
  WHEN condition THEN 'DD_INSERT'
  ELSE 'DD_REJECT'
END AS etl_dml_operation__
FROM {{ ref('upstream') }}

-- Target model filters on the control column
SELECT col1, col2  -- etl_dml_operation__ is NOT selected
FROM {{ ref('int_UPDTRANS') }}
WHERE etl_dml_operation__ != 'DD_REJECT'
  AND etl_dml_operation__ != 'DD_DELETE'
```

### Pattern 3: Conditional Update Strategy expression

When the Informatica XML uses a conditional expression:
```xml
<TABLEATTRIBUTE NAME="Update Strategy Expression"
  VALUE="IIF(ORDER_STATUS = 'NEW', DD_INSERT, DD_UPDATE)"/>
```

**Optimized path** (single target) — the expression is inlined into the target model:
```sql
{{ config(materialized='incremental', incremental_strategy='merge', unique_key='order_id') }}

SELECT * FROM {{ ref('int_Orders') }}
WHERE
  /* DD_INSERT (0) or DD_UPDATE (1): IIF(ORDER_STATUS = 'NEW', 0, 1) */
  CASE WHEN ORDER_STATUS = 'NEW' THEN 0 ELSE 1 END IN (0, 1)
```

**Non-optimized path** (multiple targets) — the expression becomes a CASE in the control column:
```sql
SELECT *,
  CASE
    WHEN ORDER_STATUS = 'NEW' THEN 'DD_INSERT'
    ELSE 'DD_UPDATE'
  END AS etl_dml_operation__
FROM {{ ref('upstream') }}
```

### Pattern 4: Variable-based Update Strategy expression

When the expression references mapping variables:
```xml
<TABLEATTRIBUTE NAME="Update Strategy Expression"
  VALUE="IIF($$UpdateFlag = 'Y', DD_UPDATE, DD_REJECT)"/>
```

The `$$variable` reference is resolved via `GetControlVariableUDF` or an equivalent mechanism. Verify the variable binding is correct in the converted SQL.

### Pattern 5: DELETE handling via pre_hook

`DD_DELETE` (value 2) is handled differently from INSERT/UPDATE because dbt models produce `SELECT` output — they cannot directly delete rows. Instead, DELETE rows are processed via a `pre_hook`:

```sql
{{ config(
    materialized='incremental',
    incremental_strategy='merge',
    unique_key='order_id',
    pre_hook="DELETE FROM {{ this }} WHERE order_id IN (SELECT order_id FROM {{ ref('int_UPDTRANS') }} WHERE etl_dml_operation__ = 'DD_DELETE')"
) }}

SELECT col1, col2
FROM {{ ref('int_UPDTRANS') }}
WHERE etl_dml_operation__ != 'DD_REJECT'
  AND etl_dml_operation__ != 'DD_DELETE'
```

For the **optimized path**, the Update Strategy model must be materialized as `table` (not `ephemeral`) when DELETE is involved, because the `pre_hook` needs to query it.

## Key Points

- This FDM does **not** break compilation — it's informational.
- The optimized path produces cleaner SQL by eliminating the intermediate table and control column.
- For DELETE operations, even the optimized path may use `table` materialization (needed for `pre_hook` reference).
- Conditional expressions (`IIF`, `DECODE`) are translated to `CASE WHEN` in SQL.
- Variable-based expressions require verifying the variable binding mechanism.
- Do **NOT** remove the FDM comment — it documents where the DML logic lives.
