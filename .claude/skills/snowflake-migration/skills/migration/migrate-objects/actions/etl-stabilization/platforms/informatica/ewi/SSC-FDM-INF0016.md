# SSC-FDM-INF0016 — Sequence Generator Ordering Non-Deterministic

Sequence Generator transformation produces sequential values via `ROW_NUMBER() OVER (ORDER BY 1)`, which does not guarantee a specific row ordering. In Informatica, the Sequence Generator assigns values in the order rows arrive from the upstream transformation.

## Quick Reference

| Aspect | Detail |
|--------|--------|
| Marker type | Inline FDM comment (not `!!!RESOLVE EWI!!!`) |
| Breaks compilation? | **No** |
| Frequency | Low-moderate (once per Sequence Generator transformation) |
| Common action | Replace `ORDER BY 1` with a meaningful column if ordering matters |

## Identification

Look for the marker in the sequence CTE:
```sql
--** SSC-FDM-INF0016 - ... non-deterministic ordering ... **
WITH source_data AS (
   SELECT * FROM {{ ref('stg_raw__SQ_Source') }}
),
sequence_data AS (
   SELECT
      *,
      ROW_NUMBER()
      OVER (
      ORDER BY
         1) - 1 AS NEXTVAL
   FROM
      source_data
)
SELECT * FROM sequence_data
```

## Context

The Sequence Generator in Informatica:
- Produces NEXTVAL (next sequential integer) and CURRVAL (last NEXTVAL value)
- NEXTVAL is translated to `ROW_NUMBER() OVER (ORDER BY 1) + (StartValue - 1)`
- CURRVAL is not supported (EWI emitted if connected downstream)
- `ORDER BY 1` means Snowflake picks any row ordering — the sequence values are assigned arbitrarily

### Start Value Offset

| Start Value | Generated Expression |
|-------------|---------------------|
| 0 (default) | `ROW_NUMBER() OVER (ORDER BY 1) - 1` |
| 1 | `ROW_NUMBER() OVER (ORDER BY 1)` |
| N (N > 1) | `ROW_NUMBER() OVER (ORDER BY 1) + (N - 1)` |

## Fix Patterns

### Pattern 1: Add meaningful ORDER BY

If the sequence should follow a specific order (e.g., by date):
```sql
-- Before (non-deterministic)
ROW_NUMBER() OVER (ORDER BY 1) - 1 AS NEXTVAL

-- After (deterministic)
ROW_NUMBER() OVER (ORDER BY created_date) - 1 AS NEXTVAL
```

### Pattern 2: Leave as-is when order doesn't matter

If the sequence is used as a surrogate key (any unique integer is acceptable), the non-deterministic ordering is fine:
```sql
-- Surrogate key — any ordering produces valid unique values
ROW_NUMBER() OVER (ORDER BY 1) AS row_key
```

## Key Points

- This FDM does **not** break compilation — the SQL is valid.
- The sequence values will be unique and sequential regardless of ordering.
- The issue is only relevant when the **assignment** of specific sequence values to specific rows matters.
- `Increment By` values other than 1 emit a separate FDM since `ROW_NUMBER()` always increments by 1.
- CURRVAL port is not translated — if connected downstream, a separate EWI is emitted.
- Do **NOT** remove the FDM comment — it documents a behavioral difference.
