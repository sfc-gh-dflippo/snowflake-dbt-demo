# Override Guide

When test results show differences that are **not** actual bugs, document the reason in the git commit message and mark the object as passed. This guide defines override categories and the evidence required for each.

## Override Types

| Override | When to Use | Counts As | Documentation Required |
|----------|-------------|-----------|----------------------|
| `MANUAL_PASS` | Output differs but verified equivalent | Pass | Moderate |
| `IGNORED` | Invalid test case (bad params, corrupted) | Excluded | Low |
| `DATA_DRIFT` | Source data changed since baseline | Excluded | **Extensive** |
| `CODE_DRIFT` | Source code changed intentionally | Pass | **Extensive** |

## CRITICAL: Override is a LAST RESORT

Before marking ANY failing test as an override, you MUST:

1. **Verify the source data** — Query underlying tables to confirm what data exists
2. **Explain the exact difference** — Document specifically which rows/columns differ and why
3. **Rule out code issues** — Confirm Snowflake procedure logic matches source intent
4. **Check for normalization issues** — If it's formatting (timestamps, numbers), flag for framework improvement

**DO NOT add overrides based on hunches.** Every override must be backed by evidence.

## MANUAL_PASS

**Use when:** Output differs but values are functionally equivalent.

**Common scenarios:**
- Rounding differences (e.g., `11.336666` vs `11.336667`)
- Decimal precision (e.g., `6.50` vs `6.5000`)
- Both platforms error identically on invalid input
- Timestamp precision differences that don't affect business logic

**Required documentation in commit message:**
```
Override MANUAL_PASS for RPT.DetailedSales:
- Issue: Rounding difference in AVGPRICEPERUNIT column
- Baseline: 11.336666, Actual: 11.336667
- Cause: SQL Server banker's rounding vs Snowflake standard rounding
- Impact: 1 in 6th decimal place, functionally equivalent
```

## DATA_DRIFT

**Use when:** Source data changed since baseline was captured.

**REQUIRES EXTENSIVE DOCUMENTATION**

You MUST document:
1. **Which table(s)** — Fully qualified table name
2. **Which column(s)** — Exact column names
3. **What changed** — Old value -> New value
4. **When changed** — Date or date range if known
5. **Why changed** — Business event, correction, etc.
6. **How verified** — Queries you ran to confirm

**Required documentation in commit message:**
```
Override DATA_DRIFT for RPT.ProductSales (params_hash: def456):
- Table: DBO.tbl_Products pricing updated since baseline capture
- Column: UnitPrice
- Product ID 1234: Baseline=$6.50, Current=$7.50 (price increase 2025-01-20)
- Product ID 5678: Baseline=$13.00, Current=$15.00 (price increase 2025-01-20)
- Verified via: SELECT product_id, unit_price, modified_date FROM source
- Confirmed procedure logic is correct; only source data changed
```

**REJECTED comments (insufficient detail):**
- `DATA_DRIFT: Data changed since baseline`
- `DATA_DRIFT: Prices are different`
- `DATA_DRIFT: New records added`

## CODE_DRIFT

**Use when:** Source code was intentionally changed after baseline capture.

**REQUIRES EXTENSIVE DOCUMENTATION**

You MUST document:
1. **Which code element** — Exact procedure/function name
2. **What changed** — Before vs after comparison
3. **Why changed** — Business requirement, bug fix, etc.
4. **How verified correct** — Manual testing, business validation
5. **Evidence Snowflake is correct** — Not just different, but *correctly different*

**Required documentation in commit message:**
```
Override CODE_DRIFT for RPT.InvoiceReport (params_hash: ghi789):
- Source procedure updated on 2025-01-15 per JIRA-1234
- Change: Added TAX_AMOUNT column, TOTAL now includes tax
- Baseline captured: 2025-01-10 (before change)
- Verified: Snowflake matches updated source logic
- Confirmed with business owner that new behavior is correct
```

**REJECTED comments (insufficient detail):**
- `CODE_DRIFT: Logic is different but correct`
- `CODE_DRIFT: Procedure was updated`

## IGNORED

**Use when:** Test case is invalid and should not be counted.

**Common scenarios:**
- Invalid parameters that shouldn't have been tested
- Corrupted baseline data
- Test case for removed functionality

## Flagging Normalization Issues

If the difference is purely formatting (same logical value, different representation), **consider flagging for framework improvement** instead of overriding:

```
NORMALIZATION ISSUE DETECTED:
- Procedure: RPT.PackageExpiration
- Column: EXPIRY_DATE
- Baseline: 2024-01-22T00:00:00
- Actual: 2024-01-22T20:00:04.330000
- Recommendation: Comparison framework should normalize timestamps
```

This improves the framework rather than accumulating overrides.

## Pre-Override Investigation Checklist

Before adding any override, read the latest case from Snowflake
(`<metadata_database>.VALIDATION.LATEST` — not the migration target):

```sql
-- Difference details for one case
SELECT differences, error_message, parameters, status
FROM <metadata_database>.VALIDATION.LATEST
WHERE UPPER(procedure_name) = UPPER('RPT.Name') AND params_hash = 'abc12345';

-- 3. Run the procedure to see actual output
CALL <PREFIX>.Name(param1 => value1, param2 => value2);

-- 4. Query source tables to verify data state
SELECT * FROM <SCHEMA>.SourceTable WHERE id = 'suspicious_value';
```
