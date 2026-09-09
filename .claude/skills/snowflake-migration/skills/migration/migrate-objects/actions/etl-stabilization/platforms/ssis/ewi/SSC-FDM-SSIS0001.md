# SSC-FDM-SSIS0001 — Lookup ORDER BY Required for Deterministic Results

Lookup transformation converted to SQL JOIN requires ORDER BY for deterministic results. In SSIS, the Lookup transformation returns the first matching row based on the order rows are read from the reference table. In standard SQL, when multiple rows match the join condition without an ORDER BY clause, any matching row may be returned, making the result non-deterministic.

## Quick Reference

| Aspect | Detail |
|--------|--------|
| Marker type | Inline FDM comment (not `!!!RESOLVE EWI!!!`) |
| Breaks compilation? | **No** |
| Frequency | Common (once per Lookup transformation with potential duplicates) |
| Common action | Replace `ORDER BY (SELECT null)` with a meaningful column |

## Identification

Look for the marker:
```
--** SSC-FDM-SSIS0001 - REPLACE NULL WITH APPROPRIATE ORDER BY COLUMN(S) TO ENSURE DETERMINISTIC FIRST MATCH SELECTION. SSIS LOOKUP RETURNS THE FIRST MATCHING ROW, SO PROPER ORDERING IS REQUIRED WHEN MULTIPLE ROWS MATCH THE JOIN CONDITION. **
```

It appears inside a `QUALIFY ROW_NUMBER()` pattern where `ORDER BY (SELECT null)` is used as a placeholder:

```sql
QUALIFY ROW_NUMBER() OVER (
   PARTITION BY USER_ID
   ORDER BY (
      SELECT
         --** SSC-FDM-SSIS0001 - REPLACE NULL WITH APPROPRIATE ORDER BY COLUMN(S) ... **
         null
   )) = 1
```

## Fix Patterns

### Pattern 1: Replace with timestamp column (most common)

```sql
-- Before (compiles but non-deterministic)
WITH lookup_ref AS (
   SELECT USER_ID, LOGON, EXPIRY_DATE
   FROM {{ ref('stg_raw__lookup') }}
   QUALIFY ROW_NUMBER() OVER (
      PARTITION BY USER_ID
      ORDER BY (
         SELECT
            --** SSC-FDM-SSIS0001 - REPLACE NULL WITH APPROPRIATE ORDER BY COLUMN(S) TO ENSURE DETERMINISTIC FIRST MATCH SELECTION. SSIS LOOKUP RETURNS THE FIRST MATCHING ROW, SO PROPER ORDERING IS REQUIRED WHEN MULTIPLE ROWS MATCH THE JOIN CONDITION. **
            null
      )) = 1
)

-- After (deterministic ordering)
WITH lookup_ref AS (
   SELECT USER_ID, LOGON, EXPIRY_DATE
   FROM {{ ref('stg_raw__lookup') }}
   QUALIFY ROW_NUMBER() OVER (
      PARTITION BY USER_ID
      ORDER BY EXPIRY_DATE DESC
   ) = 1
)
```

### Pattern 2: No natural ordering column available

When no timestamp or sequence column exists, use a primary key for stable (though arbitrary) selection:

```sql
-- After (stable selection by PK)
QUALIFY ROW_NUMBER() OVER (
   PARTITION BY CUSTOMER_ID
   ORDER BY RECORD_ID DESC
) = 1
```

### How to choose the ORDER BY column

- **Timestamp** (e.g., `MODIFIED_DATE`, `CREATED_AT`) — gets the most recent match.
- **Primary / surrogate key** (e.g., `ID`, `RECORD_ID`) — stable but arbitrary.
- If no suitable column exists, leave `ORDER BY (SELECT null)` and mark as needs-user.

## Key Points

- The `QUALIFY ROW_NUMBER()` pattern is correct — only the ORDER BY placeholder needs fixing.
- Do **NOT** remove the FDM comment.
- When the PARTITION BY key is unique in the reference table (no duplicates), the ORDER BY value doesn't matter — any column works. Consider marking as informational in that case.
- When multiple lookups reference the same table, use the same ORDER BY column for consistency.
