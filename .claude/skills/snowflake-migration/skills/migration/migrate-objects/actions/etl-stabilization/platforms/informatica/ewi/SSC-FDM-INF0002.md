# SSC-FDM-INF0002 — Aggregator Input Column Ordering Non-Deterministic

Aggregator transformation uses all input columns to determine group ordering. In Informatica, the Aggregator processes rows in arrival order and uses `LAST_VALUE` semantics for non-aggregated columns. In SQL, there is no guaranteed row arrival order, so all input columns are used as a tiebreaker in the `ORDER BY` clause.

## Quick Reference

| Aspect | Detail |
|--------|--------|
| Marker type | Inline FDM comment (not `!!!RESOLVE EWI!!!`) |
| Breaks compilation? | **No** |
| Frequency | Common (once per Aggregator transformation) |
| Common action | Review ORDER BY columns; replace with meaningful ordering if possible |

## Identification

Look for the marker inside a `QUALIFY ROW_NUMBER()` pattern:
```sql
QUALIFY
   --** SSC-FDM-INF0002 - ALL INPUT COLUMNS WILL BE USED TO DETERMINE GROUP ORDER. **
   ROW_NUMBER()
   OVER (
   PARTITION BY (
      DEPARTMENT)
   ORDER BY
      NAME,
      SALARY,
      DEPARTMENT) = 1
```

## Context

Informatica Aggregators use window functions with `QUALIFY ROW_NUMBER() = 1` to select one row per group. The translation uses `LAST_VALUE ... OVER (PARTITION BY group_keys ORDER BY all_input_columns)` to approximate Informatica's row-by-row processing. Since SQL has no guaranteed row ordering, the `ORDER BY` uses all input columns as a best-effort tiebreaker.

## Fix Patterns

### Pattern 1: Replace with meaningful ORDER BY

If there's a natural ordering column (timestamp, sequence):
```sql
-- Before (all columns as tiebreaker)
QUALIFY ROW_NUMBER() OVER (
   PARTITION BY DEPARTMENT
   ORDER BY NAME, SALARY, DEPARTMENT
) = 1

-- After (meaningful ordering)
QUALIFY ROW_NUMBER() OVER (
   PARTITION BY DEPARTMENT
   ORDER BY HIRE_DATE DESC
) = 1
```

### Pattern 2: Leave as-is when ordering doesn't matter

If the aggregation only produces aggregate values (SUM, COUNT, MAX, MIN) and no `LAST_VALUE` passthrough columns, the ordering is irrelevant:
```sql
-- Only aggregate outputs — ordering doesn't affect results
SELECT
   SUM(SALARY) OVER (PARTITION BY DEPARTMENT) AS total_salary,
   DEPARTMENT
```

## Key Points

- This FDM does **not** break compilation — the SQL is valid.
- The core issue is **determinism** — different row orderings may produce different `LAST_VALUE` results for non-aggregated columns.
- If all output ports use aggregate functions (SUM, COUNT, MAX, MIN, AVG), this FDM is informational only.
- Do **NOT** remove the FDM comment — it documents a behavioral difference.
