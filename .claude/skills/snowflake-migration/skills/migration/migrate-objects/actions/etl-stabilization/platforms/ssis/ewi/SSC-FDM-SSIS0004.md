# SSC-FDM-SSIS0004 — Merge Join to SQL JOIN

SSIS Merge Join transformation converted to SQL JOIN. In SSIS, Merge Join requires both inputs to be pre-sorted on the join key; the join processes rows in sorted order. The converted SQL JOIN does not require or guarantee sorted input/output. If downstream logic depends on sorted output from the join, an explicit ORDER BY must be added.

## Quick Reference

| Aspect | Detail |
|--------|--------|
| Marker type | Inline FDM comment (not `!!!RESOLVE EWI!!!`) |
| Breaks compilation? | **No** |
| Frequency | Low-medium (once per Merge Join transformation) |
| Common action | Verify JOIN correctness; add ORDER BY if downstream depends on sorted output |

## Identification

Look for the marker:
```
--** SSC-FDM-SSIS0004 - SSIS MERGE JOIN TRANSFORMATION CONVERTED TO SQL JOIN. VERIFY JOIN CORRECTNESS AND ADD ORDER BY IF ROW ORDER IS REQUIRED. **
```

It appears before or within a JOIN query:

```sql
--** SSC-FDM-SSIS0004 - ... **
SELECT a.col1, a.col2, b.col3
FROM source_left a
INNER JOIN source_right b
    ON a.join_key = b.join_key
```

## Fix Patterns

### Pattern 1: Verify JOIN type and add ORDER BY

The SSIS Merge Join supports INNER, LEFT OUTER, and FULL OUTER joins. Verify that the converted JOIN type matches the original:

```sql
-- Before
--** SSC-FDM-SSIS0004 - SSIS MERGE JOIN TRANSFORMATION CONVERTED TO SQL JOIN. VERIFY JOIN CORRECTNESS AND ADD ORDER BY IF ROW ORDER IS REQUIRED. **
SELECT a.patient_id, a.visit_date, b.diagnosis_code
FROM visits a
INNER JOIN diagnoses b
    ON a.patient_id = b.patient_id

-- After (order restored to match original sorted output)
--** SSC-FDM-SSIS0004 - SSIS MERGE JOIN TRANSFORMATION CONVERTED TO SQL JOIN. VERIFY JOIN CORRECTNESS AND ADD ORDER BY IF ROW ORDER IS REQUIRED. **
SELECT a.patient_id, a.visit_date, b.diagnosis_code
FROM visits a
INNER JOIN diagnoses b
    ON a.patient_id = b.patient_id
ORDER BY a.patient_id
```

### Pattern 2: Order not needed — verify JOIN only

```sql
-- If the result feeds into an INSERT, aggregation, or another transformation
-- that doesn't depend on row order, just verify the JOIN is correct.
-- No ORDER BY needed.
INSERT INTO patient_diagnoses
SELECT a.patient_id, a.visit_date, b.diagnosis_code
FROM visits a
INNER JOIN diagnoses b
    ON a.patient_id = b.patient_id;
```

### Pattern 3: Multi-column join key

SSIS Merge Joins can use composite keys. Verify all join columns are present:

```sql
--** SSC-FDM-SSIS0004 - ... **
SELECT a.col1, b.col2
FROM source_a a
INNER JOIN source_b b
    ON a.key1 = b.key1 AND a.key2 = b.key2
ORDER BY a.key1, a.key2
```

## Key Points

- Do **NOT** remove the FDM comment.
- The original SSIS Merge Join sort keys are usually the same as the join keys. Check the SSIS source if the sort columns are not obvious.
- Verify the JOIN type (INNER, LEFT, FULL) matches the original SSIS Merge Join type.
- If the JOIN result is consumed by an INSERT, GROUP BY, or another JOIN, row order typically doesn't matter — mark as informational.
- If the result is returned to a client or feeds a cursor/loop that assumes sorted input, add ORDER BY on the join key columns.
