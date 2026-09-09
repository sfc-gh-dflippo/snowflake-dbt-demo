# SSC-EWI-TS0077 — COLLATE Not Supported

The COLLATE clause is not supported in Snowflake. The `!!!RESOLVE EWI!!!` marker **breaks compilation**. Snowflake handles string comparisons using database/session-level collation settings rather than inline COLLATE clauses.

## Quick Reference

| Aspect | Detail |
|--------|--------|
| Marker type | `!!!RESOLVE EWI!!!` (compilation-breaking) |
| Breaks compilation? | **Yes** |
| Frequency | Low-to-moderate (once per COLLATE usage) |
| Common action | Remove the COLLATE clause entirely |

## Identification

Look for the marker:
```
!!!RESOLVE EWI!!! /*** SSC-EWI-TS0077 - COLLATE CLAUSE IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
```

It appears on or near the line containing the COLLATE clause:

```sql
SELECT
   CustomerName
      !!!RESOLVE EWI!!! /*** SSC-EWI-TS0077 - COLLATE CLAUSE IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
      COLLATE Latin1_General_CI_AS
   AS CustomerName
FROM customers
```

## Fix Patterns

### Pattern 1: Remove COLLATE from column expression

```sql
-- Before (breaks compilation)
SELECT
   CustomerName
      !!!RESOLVE EWI!!! /*** SSC-EWI-TS0077 - COLLATE CLAUSE IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
      COLLATE Latin1_General_CI_AS
   AS CustomerName
FROM customers

-- After
SELECT
   CustomerName
FROM customers
```

### Pattern 2: Remove COLLATE from comparison

```sql
-- Before (breaks compilation)
WHERE
   col_a
      !!!RESOLVE EWI!!! /*** SSC-EWI-TS0077 - COLLATE CLAUSE IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
      COLLATE SQL_Latin1_General_CP1_CI_AS
   = col_b

-- After
WHERE col_a = col_b
```

### Pattern 3: Remove COLLATE from ORDER BY

```sql
-- Before (breaks compilation)
ORDER BY
   LastName
      !!!RESOLVE EWI!!! /*** SSC-EWI-TS0077 - COLLATE CLAUSE IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
      COLLATE Latin1_General_BIN

-- After
ORDER BY LastName
```

## Key Points

- **Must** remove both the `!!!RESOLVE EWI!!!` marker line **and** the `COLLATE ...` line — the marker breaks compilation, and COLLATE is unsupported syntax.
- Removing COLLATE usually causes **no functional issues**. Snowflake uses UTF-8 by default and supports collation specification at the column level via `COLLATE` in `CREATE TABLE` DDL, but not inline in queries.
- If case-insensitive comparison was the intent of the COLLATE clause, Snowflake is case-sensitive by default. Use `UPPER()` / `LOWER()` or `COLLATE 'en-ci'` in the column DDL if needed.
- Multiple `SSC-EWI-TS0077` markers may appear in a single query if several columns used COLLATE.
