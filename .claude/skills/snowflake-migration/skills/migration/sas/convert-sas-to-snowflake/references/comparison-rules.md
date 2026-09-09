# SAS-to-Snowflake Output Comparison Rules

Rules for determining equivalence between SAS expected output and Snowflake actual output during validation testing.

## Value Equivalence Rules

| SAS Value | Snowflake Value | Equivalent? | Rule |
|-----------|----------------|-------------|------|
| `.` (numeric missing) | `NULL` | YES | SAS numeric missing maps to SQL NULL |
| `' '` (character missing) | `NULL` | YES | SAS character missing maps to NULL |
| `' '` (character missing) | `''` (empty string) | YES | Both represent absent character values |
| `''` (empty string) | `NULL` | YES | Treat empty string and NULL as equivalent for character columns |
| `0` | `NULL` | NO | Zero is a valid numeric value, not missing |
| `0` | `0.0` | YES | Integer and float representations of zero are equivalent |

## Numeric Precision

| Scenario | Tolerance | Rationale |
|----------|-----------|-----------|
| Integer arithmetic | Exact match | No precision loss expected |
| Float arithmetic (SUM, MEAN) | abs(diff) < 1e-10 | SAS 8-byte float vs Snowflake NUMBER(38,x) |
| Division results | abs(diff) < 1e-8 | Division may differ at low-order digits |
| Currency/money columns | abs(diff) < 0.01 | Round to 2 decimal places before comparing |
| Percentage calculations | abs(diff) < 1e-6 | Intermediate rounding differences |

### Comparison SQL Pattern for Numeric Tolerance

```sql
SELECT
  e.row_key,
  e.col_name AS column_name,
  e.val AS expected,
  a.val AS actual,
  ABS(e.val - a.val) AS diff
FROM expected_unpivoted e
JOIN actual_unpivoted a ON e.row_key = a.row_key AND e.col_name = a.col_name
WHERE ABS(e.val - a.val) > 1e-10;
```

## Character Value Rules

| Rule | Behavior |
|------|----------|
| Trailing spaces | TRIM both sides before comparing (SAS fixed-length pads with spaces) |
| Leading spaces | Preserve -- leading spaces are significant in SAS |
| Case sensitivity | Case-sensitive comparison (SAS preserves case in character values) |
| Character encoding | UTF-8 assumed on both sides |

## Date Value Rules

| SAS Representation | Snowflake Representation | Equivalence |
|--------------------|--------------------------|-------------|
| SAS date value (days since 1960-01-01) | DATE type | Convert SAS numeric to calendar date for comparison |
| SAS datetime value (seconds since 1960-01-01) | TIMESTAMP | Convert SAS numeric to timestamp for comparison |
| SAS time value (seconds since midnight) | TIME | Convert SAS numeric to time for comparison |
| Formatted date string (`'01JAN2024'`) | `'2024-01-01'` | Compare as DATE after parsing both formats |

### Date Conversion Reference

```
SAS date value 0 = 1960-01-01
SAS date value 23376 = 2024-01-01
Formula: Snowflake DATE = DATEADD(day, sas_date_value, '1960-01-01')
```

## Sort Order and Row Ordering

| Rule | Details |
|------|---------|
| Row ordering | Do NOT compare row order -- sort both result sets by key columns before comparison |
| If no key columns exist | Sort by ALL columns (left to right) to produce deterministic order |
| NULL sort position | SAS sorts missing LOW (before all values); Snowflake sorts NULL HIGH (after all values) by default. Sorting differences are NOT comparison failures. |

### Key Column Selection for Sorting

Priority order for choosing sort keys:
1. Primary key columns (if identifiable from schema)
2. Columns used in BY statements in the original SAS code
3. All non-computed columns (exclude aggregated/derived columns)
4. All columns as last resort

## Schema Comparison Rules

| Check | Pass Condition |
|-------|---------------|
| Column count | Must match exactly |
| Column names | Case-insensitive match required |
| Column order | Must match (SAS preserves column order from PDV) |
| Column types | Compatible types pass (see compatibility table below) |

### Type Compatibility Matrix

| Expected (SAS-derived) | Actual (Snowflake) | Compatible? |
|------------------------|--------------------|-------------|
| NUMBER | NUMBER | YES |
| NUMBER | FLOAT | YES |
| NUMBER | DECIMAL | YES |
| NUMBER | INTEGER | YES |
| VARCHAR | VARCHAR | YES |
| VARCHAR | STRING | YES (same in Snowflake) |
| VARCHAR | CHAR | YES (compare after TRIM) |
| DATE | DATE | YES |
| DATE | TIMESTAMP_NTZ | YES (compare date part only) |
| TIMESTAMP | TIMESTAMP_NTZ | YES |
| BOOLEAN | NUMBER | YES (0/1 mapping) |

## Row Count Rules

| Scenario | Expected Behavior |
|----------|-------------------|
| Simple filter (WHERE) | Output rows <= input rows |
| GROUP BY / aggregation | Output rows <= distinct groups |
| JOIN (inner) | Output rows <= product of input rows |
| LEFT JOIN | Output rows >= left table rows |
| UNION / SET operations | Depends on UNION vs UNION ALL |
| MERGE (SAS) | Output rows = max(left rows, right rows) for one-to-one; flag if > max |
| Many-to-many join | Flag if output_rows > 2x max(input_rows) |

## Comparison Execution SQL

### Full Table Comparison (MINUS/EXCEPT approach)

```sql
-- Rows in expected but NOT in actual (missing from Snowflake output)
SELECT 'MISSING_FROM_ACTUAL' AS diff_type, *
FROM expected_<table>
MINUS
SELECT 'MISSING_FROM_ACTUAL' AS diff_type, *
FROM actual_<table>;

-- Rows in actual but NOT in expected (extra in Snowflake output)
SELECT 'EXTRA_IN_ACTUAL' AS diff_type, *
FROM actual_<table>
MINUS
SELECT 'EXTRA_IN_ACTUAL' AS diff_type, *
FROM expected_<table>;
```

### Column-Level Comparison (for numeric tolerance)

```sql
WITH expected_numbered AS (
  SELECT *, ROW_NUMBER() OVER (ORDER BY <key_cols>) AS _rn
  FROM expected_<table>
),
actual_numbered AS (
  SELECT *, ROW_NUMBER() OVER (ORDER BY <key_cols>) AS _rn
  FROM actual_<table>
)
SELECT
  e._rn AS row_num,
  '<col>' AS column_name,
  e.<col> AS expected_val,
  a.<col> AS actual_val
FROM expected_numbered e
JOIN actual_numbered a ON e._rn = a._rn
WHERE NOT (
  (e.<col> IS NULL AND a.<col> IS NULL)
  OR (TRIM(e.<col>::VARCHAR) = TRIM(a.<col>::VARCHAR))
  OR (TRY_TO_DOUBLE(e.<col>) IS NOT NULL
      AND ABS(e.<col> - a.<col>) < 1e-10)
);
```

## Mismatch Classification

When reporting mismatches, classify the likely root cause:

| Mismatch Pattern | Likely Root Cause |
|------------------|-------------------|
| NULL vs non-NULL value | Missing value handling (SAS `.` not mapped to NULL, or COALESCE missing) |
| NULL vs empty string | Character missing value conversion |
| Row count: actual > expected | Many-to-many join (SAS MERGE vs SQL JOIN) |
| Row count: actual < expected | Incorrect INNER JOIN (should be LEFT/FULL) or WHERE filter too restrictive |
| Numeric difference < 0.01 | Float precision (acceptable for most cases) |
| Numeric difference > 0.01 | Wrong aggregation, missing COALESCE(x,0), or SAS sum statement vs assignment |
| Date off by 1 | INTNX alignment parameter (B vs E vs S) |
| All values shifted by N rows | Window function ROWS vs RANGE, or missing ORDER BY |
| Duplicate rows in actual | Missing DISTINCT or QUALIFY (SAS NODUPKEY equivalent) |
| Column missing | PDV variable not carried forward (check KEEP/DROP/RENAME) |
