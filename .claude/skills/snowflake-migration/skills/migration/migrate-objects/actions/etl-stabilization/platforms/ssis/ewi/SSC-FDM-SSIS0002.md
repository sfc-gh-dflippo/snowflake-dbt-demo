# SSC-FDM-SSIS0002 — Merge to UNION ALL ORDER BY

SSIS Merge transformation converted to UNION ALL. In SSIS, Merge produces sorted output from two pre-sorted inputs. UNION ALL does not guarantee row order. If downstream logic depends on sorted output, an explicit ORDER BY must be added.

## Quick Reference

| Aspect | Detail |
|--------|--------|
| Marker type | Inline FDM comment (not `!!!RESOLVE EWI!!!`) |
| Breaks compilation? | **No** |
| Frequency | Low (once per Merge transformation) |
| Common action | Add ORDER BY matching original sort keys if order matters downstream |

## Identification

Look for the marker:
```
--** SSC-FDM-SSIS0002 - SSIS MERGE TRANSFORMATION CONVERTED TO UNION ALL. ORIGINAL MERGE PRODUCED SORTED OUTPUT; UNION ALL DOES NOT GUARANTEE ORDER. ADD ORDER BY IF ROW ORDER IS REQUIRED. **
```

It appears before or within a UNION ALL query that combines two or more source queries:

```sql
--** SSC-FDM-SSIS0002 - ... **
SELECT col_a, col_b, col_c FROM source_one
UNION ALL
SELECT col_a, col_b, col_c FROM source_two
```

## Fix Patterns

### Pattern 1: Add ORDER BY to match original sort keys

```sql
-- Before (no guaranteed order)
--** SSC-FDM-SSIS0002 - SSIS MERGE TRANSFORMATION CONVERTED TO UNION ALL. ORIGINAL MERGE PRODUCED SORTED OUTPUT; UNION ALL DOES NOT GUARANTEE ORDER. ADD ORDER BY IF ROW ORDER IS REQUIRED. **
SELECT customer_id, order_date, amount FROM orders_current
UNION ALL
SELECT customer_id, order_date, amount FROM orders_archive

-- After (order restored)
--** SSC-FDM-SSIS0002 - SSIS MERGE TRANSFORMATION CONVERTED TO UNION ALL. ORIGINAL MERGE PRODUCED SORTED OUTPUT; UNION ALL DOES NOT GUARANTEE ORDER. ADD ORDER BY IF ROW ORDER IS REQUIRED. **
SELECT customer_id, order_date, amount FROM orders_current
UNION ALL
SELECT customer_id, order_date, amount FROM orders_archive
ORDER BY customer_id, order_date
```

### Pattern 2: Order not needed — no change

```sql
-- If the result feeds into an INSERT, aggregation, or another transformation
-- that doesn't depend on row order, no change is needed.
INSERT INTO target_table
SELECT customer_id, order_date, amount FROM orders_current
UNION ALL
SELECT customer_id, order_date, amount FROM orders_archive;
```

## Key Points

- Do **NOT** remove the FDM comment.
- The original SSIS Merge sort keys may be documented in the commented SSIS XML or in the package metadata. Check the SSIS source if the sort columns are not obvious.
- If the UNION ALL result is consumed by an INSERT, GROUP BY, or JOIN, row order typically doesn't matter — mark as informational.
- If the result is returned to a client or feeds a cursor/loop that assumes sorted input, add ORDER BY.
