---
description: T-SQL (SQL Server) subquery patterns and their Snowflake equivalents
title: T-SQL Subqueries to Snowflake
---

# Subquery Patterns

## Overview

A subquery is a query within another query. Subqueries can be:

- **Correlated**: Reference columns from the outer query (executed per row)
- **Uncorrelated**: Independent of the outer query (executed once)
- **Scalar**: Return a single value
- **Non-scalar**: Return multiple values

## Setup Data

### T-SQL (SQL Server)

```sql
CREATE TABLE tableA (
    col1 INT,
    col2 VARCHAR(20)
);

CREATE TABLE tableB (
    col3 INT,
    col4 VARCHAR(20)
);

INSERT INTO tableA VALUES (50, 'Hey'), (20, 'Example');
INSERT INTO tableB VALUES (50, 'Hey'), (20, 'Bye');
GO
```

### Snowflake Equivalent

```sql
CREATE OR REPLACE TABLE tableA (
    col1 INTEGER,
    col2 VARCHAR(20)
);

CREATE OR REPLACE TABLE tableB (
    col3 INTEGER,
    col4 VARCHAR(20)
);

INSERT INTO tableA VALUES (50, 'Hey'), (20, 'Example');
INSERT INTO tableB VALUES (50, 'Hey'), (20, 'Bye');
```

## Correlated Scalar Subqueries

Snowflake evaluates correlated subqueries at compile time. Use `ANY_VALUE()` to ensure single-value
return.

### T-SQL

```sql
SELECT col2
FROM tableA
WHERE col1 = (SELECT col3 FROM tableB WHERE col2 = col4);
```

### Snowflake

```sql
SELECT col2
FROM tableA
WHERE col1 = (
    SELECT ANY_VALUE(col3)
    FROM tableB
    WHERE col2 = col4
);
```

## Uncorrelated Scalar Subqueries

Fully supported in Snowflake without modification.

### T-SQL

```sql
SELECT col2, (SELECT AVG(col3) FROM tableB) AS avgTableB
FROM tableA
WHERE col1 = (SELECT MAX(col3) FROM tableB);
```

### Snowflake

```sql
SELECT col2, (SELECT AVG(col3) FROM tableB) AS avg_table_b
FROM tableA
WHERE col1 = (SELECT MAX(col3) FROM tableB);
```

## Non-Scalar Subqueries

Subqueries with IN/ANY/ALL/EXISTS operators are supported.

### T-SQL

```sql
-- IN operator
SELECT col2
FROM tableA
WHERE col1 IN (SELECT col3 FROM tableB);

-- EXISTS operator
SELECT col2
FROM tableA a
WHERE EXISTS (SELECT 1 FROM tableB b WHERE a.col1 = b.col3);

-- Derived table
SELECT col2, derived_table.col4
FROM tableA, (SELECT * FROM tableB) AS derived_table
WHERE col1 = derived_table.col3;
```

### Snowflake

```sql
-- IN operator (direct conversion)
SELECT col2
FROM tableA
WHERE col1 IN (SELECT col3 FROM tableB);

-- EXISTS operator (direct conversion)
SELECT col2
FROM tableA a
WHERE EXISTS (SELECT 1 FROM tableB b WHERE a.col1 = b.col3);

-- Derived table (direct conversion)
SELECT col2, derived_table.col4
FROM tableA, (SELECT * FROM tableB) AS derived_table
WHERE col1 = derived_table.col3;
```

## T-SQL-Specific Subquery Patterns

### TOP N Queries

### T-SQL

```sql
-- TOP in main query
SELECT TOP 10 col2
FROM tableA
ORDER BY col1;

-- TOP with PERCENT
SELECT TOP 10 PERCENT col2
FROM tableA
ORDER BY col1;

-- TOP in subquery
SELECT col2
FROM tableA
WHERE col1 = (SELECT TOP 1 col3 FROM tableB ORDER BY col3 DESC);
```

### Snowflake

```sql
-- Use LIMIT instead of TOP
SELECT col2
FROM tableA
ORDER BY col1
LIMIT 10;

-- PERCENT requires calculation
SELECT col2
FROM tableA
QUALIFY ROW_NUMBER() OVER (ORDER BY col1) <= (SELECT COUNT(*) * 0.10 FROM tableA);

-- LIMIT in subquery
SELECT col2
FROM tableA
WHERE col1 = (SELECT col3 FROM tableB ORDER BY col3 DESC LIMIT 1);
```

### CROSS APPLY / OUTER APPLY

### T-SQL

```sql
-- CROSS APPLY (like INNER JOIN LATERAL)
SELECT a.col2, b.col4
FROM tableA a
CROSS APPLY (
    SELECT TOP 1 col4
    FROM tableB
    WHERE col3 = a.col1
    ORDER BY col4
) b;

-- OUTER APPLY (like LEFT JOIN LATERAL)
SELECT a.col2, b.col4
FROM tableA a
OUTER APPLY (
    SELECT TOP 1 col4
    FROM tableB
    WHERE col3 = a.col1
    ORDER BY col4
) b;
```

### Snowflake

```sql
-- CROSS APPLY to LATERAL
SELECT a.col2, b.col4
FROM tableA a,
LATERAL (
    SELECT col4
    FROM tableB
    WHERE col3 = a.col1
    ORDER BY col4
    LIMIT 1
) b;

-- OUTER APPLY to LEFT JOIN LATERAL
SELECT a.col2, b.col4
FROM tableA a
LEFT JOIN LATERAL (
    SELECT col4
    FROM tableB
    WHERE col3 = a.col1
    ORDER BY col4
    LIMIT 1
) b ON TRUE;
```

### Common Table Expressions with Hints

### T-SQL

```sql
WITH filtered_data AS (
    SELECT col3 FROM tableB WHERE col3 > 10
)
SELECT col2
FROM tableA WITH (NOLOCK)
WHERE col1 IN (SELECT col3 FROM filtered_data);
```

### Snowflake

```sql
-- Remove table hints (Snowflake handles locking automatically)
WITH filtered_data AS (
    SELECT col3 FROM tableB WHERE col3 > 10
)
SELECT col2
FROM tableA
WHERE col1 IN (SELECT col3 FROM filtered_data);
```

### Row Limiting with OFFSET/FETCH

### T-SQL

```sql
SELECT col2
FROM tableA
ORDER BY col1
OFFSET 10 ROWS FETCH NEXT 5 ROWS ONLY;
```

### Snowflake

```sql
SELECT col2
FROM tableA
ORDER BY col1
LIMIT 5 OFFSET 10;
```

## Key Conversion Notes

| T-SQL Pattern                          | Snowflake Equivalent               |
| -------------------------------------- | ---------------------------------- |
| Correlated scalar subquery             | Add `ANY_VALUE()` wrapper          |
| `TOP n`                                | `LIMIT n`                          |
| `TOP n PERCENT`                        | Use `QUALIFY` with percentage calc |
| `CROSS APPLY`                          | `LATERAL` or `, LATERAL (...)`     |
| `OUTER APPLY`                          | `LEFT JOIN LATERAL ... ON TRUE`    |
| `OFFSET n ROWS FETCH NEXT m ROWS ONLY` | `LIMIT m OFFSET n`                 |
| `WITH (NOLOCK)`                        | Remove (not needed)                |
| `ISNULL(a, b)`                         | `COALESCE(a, b)` or `IFNULL(a, b)` |
| `GETDATE()`                            | `CURRENT_TIMESTAMP()`              |
| `CONVERT(type, expr)`                  | `expr::type`                       |
| `CAST(expr AS type)`                   | `expr::type`                       |
| `GO` batch separator                   | Remove                             |
