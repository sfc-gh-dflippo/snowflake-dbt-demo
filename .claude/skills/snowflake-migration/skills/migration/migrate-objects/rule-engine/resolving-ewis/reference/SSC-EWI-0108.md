# SSC-EWI-0108 - Invalid Subquery Pattern

SnowConvert flags subqueries that match patterns considered potentially invalid in Snowflake, which may produce compilation errors. In practice, many of these are **valid Snowflake SQL** and only require removing the marker.

## Quick Reference

| SQL Server | Snowflake |
|------------|-----------|
| Correlated scalar subquery in CASE | Same syntax - works as-is |
| `SELECT COUNT(col) FROM @table_var t WHERE t.key = outer.key` | `SELECT COUNT(col) FROM temp_table t WHERE t.key = outer.key` |

## Identification

Look for the marker:
```sql
!!!RESOLVE EWI!!! /*** SSC-EWI-0108 - THE FOLLOWING SUBQUERY MATCHES AT LEAST ONE OF THE PATTERNS CONSIDERED INVALID AND MAY PRODUCE COMPILATION ERRORS ***/!!!
```

This typically appears before a correlated scalar subquery inside a CASE expression or SELECT list that references a temporary table.

## Fix Process

1. **Examine the subquery** - Determine if it is a valid Snowflake correlated scalar subquery
2. **Check for valid patterns** - Snowflake supports correlated scalar subqueries that return a single row/column, including:
   - `SELECT COUNT(col) FROM table WHERE correlation_predicate`
   - `SELECT SUM(col) FROM table WHERE correlation_predicate`
   - `SELECT MAX(col) FROM table WHERE correlation_predicate`
   - `SELECT ANY_VALUE(agg_expr) FROM table WHERE correlation_predicate`
3. **If valid** - Simply remove the `!!!RESOLVE EWI!!!` marker line. No code changes needed.
4. **If invalid** - Rewrite using a LEFT JOIN to a pre-aggregated subquery (see examples below)

## Examples

### Pattern 1: Valid correlated scalar subquery (most common)

The subquery is inside a CASE expression and references a temp table with a correlation predicate. This is valid Snowflake SQL.

#### Before (with EWI marker)
```sql
CASE
    WHEN period <= :DATE_TO THEN
    !!!RESOLVE EWI!!! /*** SSC-EWI-0108 - THE FOLLOWING SUBQUERY MATCHES AT LEAST ONE OF THE PATTERNS CONSIDERED INVALID AND MAY PRODUCE COMPILATION ERRORS ***/!!!
        (SELECT COUNT(part) FROM T_wrnty t WHERE t.period = s.period)
    ELSE 0
END AS kpi_parts
```

#### After (marker removed, no code changes)
```sql
CASE
    WHEN period <= :DATE_TO THEN
        (SELECT COUNT(part) FROM T_wrnty t WHERE t.period = s.period)
    ELSE 0
END AS kpi_parts
```

### Pattern 2: Rewrite as LEFT JOIN (if subquery causes errors)

If the correlated subquery does cause compilation errors (e.g., returns multiple rows), rewrite using a pre-aggregated LEFT JOIN:

#### Before
```sql
SELECT s.period,
    (SELECT COUNT(part) FROM T_wrnty t WHERE t.period = s.period) AS kpi_parts
FROM T_sps s
```

#### After
```sql
SELECT s.period,
    NVL(agg.kpi_parts, 0) AS kpi_parts
FROM T_sps s
LEFT JOIN (
    SELECT period, COUNT(part) AS kpi_parts
    FROM T_wrnty
    GROUP BY period
) agg ON agg.period = s.period
```

## Key Points

- Most SSC-EWI-0108 flagged subqueries are **valid Snowflake SQL** and only need the marker removed
- Correlated scalar subqueries with aggregate functions (COUNT, SUM, MAX, MIN, AVG) that return exactly one row are supported in Snowflake
- The EWI is a **conservative warning** - SnowConvert flags patterns it cannot guarantee are valid, but many are
- If SnowConvert added `ANY_VALUE()` around an aggregate expression in a similar subquery nearby, that is also valid and should be kept
- Always test the query after removing the marker to confirm it compiles

## Resources

- [Snowflake Subqueries](https://docs.snowflake.com/en/sql-reference/operators-subquery)
- [Snowflake Scalar Subqueries](https://docs.snowflake.com/en/sql-reference/operators-subquery#scalar-subqueries)
