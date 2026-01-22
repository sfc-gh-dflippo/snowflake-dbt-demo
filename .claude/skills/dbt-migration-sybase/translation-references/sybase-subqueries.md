---
description: Sybase IQ subquery patterns and their Snowflake equivalents
title: Sybase IQ Subqueries to Snowflake
---

## Subquery Patterns

## Overview

A subquery is a query within another query. Subqueries can be:

- **Correlated**: Reference columns from the outer query (executed per row)
- **Uncorrelated**: Independent of the outer query (executed once)
- **Scalar**: Return a single value
- **Non-scalar**: Return multiple values

## Setup Data

### Sybase IQ

```sql
CREATE TABLE tableA (
    col1 INTEGER,
    col2 VARCHAR(20)
);

CREATE TABLE tableB (
    col3 INTEGER,
    col4 VARCHAR(20)
);

INSERT INTO tableA VALUES (50, 'Hey');
INSERT INTO tableA VALUES (20, 'Example');
INSERT INTO tableB VALUES (50, 'Hey');
INSERT INTO tableB VALUES (20, 'Bye');
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

### Sybase IQ 2

```sql
SELECT col2
FROM tableA
WHERE col1 = (SELECT col3 FROM tableB WHERE col2 = col4)
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

### Sybase IQ 3

```sql
SELECT col2, (SELECT AVG(col3) FROM tableB) AS avgTableB
FROM tableA
WHERE col1 = (SELECT MAX(col3) FROM tableB)
```

### Snowflake 2

```sql
SELECT col2, (SELECT AVG(col3) FROM tableB) AS avg_table_b
FROM tableA
WHERE col1 = (SELECT MAX(col3) FROM tableB);
```

## Non-Scalar Subqueries

Subqueries with IN/ANY/ALL/EXISTS operators are supported.

### Sybase IQ 4

```sql
-- IN operator
SELECT col2
FROM tableA
WHERE col1 IN (SELECT col3 FROM tableB)

-- EXISTS operator
SELECT col2
FROM tableA a
WHERE EXISTS (SELECT 1 FROM tableB b WHERE a.col1 = b.col3)

-- Derived table
SELECT col2, derived_table.col4
FROM tableA, (SELECT * FROM tableB) derived_table
WHERE col1 = derived_table.col3
```

### Snowflake 3

```sql
-- IN operator (direct conversion)
SELECT col2
FROM tableA
WHERE col1 IN (SELECT col3 FROM tableB);

-- EXISTS operator (direct conversion)
SELECT col2
FROM tableA a
WHERE EXISTS (SELECT 1 FROM tableB b WHERE a.col1 = b.col3);

-- Derived table (add AS keyword)
SELECT col2, derived_table.col4
FROM tableA, (SELECT * FROM tableB) AS derived_table
WHERE col1 = derived_table.col3;
```

## Sybase IQ-Specific Subquery Patterns

### TOP N Queries

### Sybase IQ 5

```sql
-- TOP in main query
SELECT TOP 10 col2
FROM tableA
ORDER BY col1

-- TOP in subquery
SELECT col2
FROM tableA
WHERE col1 = (SELECT TOP 1 col3 FROM tableB ORDER BY col3 DESC)
```

### Snowflake 4

```sql
-- Use LIMIT instead of TOP
SELECT col2
FROM tableA
ORDER BY col1
LIMIT 10;

-- LIMIT in subquery
SELECT col2
FROM tableA
WHERE col1 = (SELECT col3 FROM tableB ORDER BY col3 DESC LIMIT 1);
```

### FIRST_VALUE / NUMBER() Functions

### Sybase IQ 6

```sql
-- Using NUMBER(*) for row numbering in subquery
SELECT *
FROM (
    SELECT col2, col1, NUMBER(*) AS row_num
    FROM tableA
    ORDER BY col1
) subq
WHERE row_num <= 5
```

### Snowflake 5

```sql
-- Use ROW_NUMBER() and QUALIFY
SELECT
    col2,
    col1
FROM tableA
QUALIFY ROW_NUMBER() OVER (ORDER BY col1) <= 5;
```

### Common Table Expressions

### Sybase IQ 7

```sql
WITH filtered_data AS (
    SELECT col3 FROM tableB WHERE col3 > 10
)
SELECT col2
FROM tableA
WHERE col1 IN (SELECT col3 FROM filtered_data)
```

### Snowflake 6

```sql
-- Direct conversion (CTEs supported)
WITH filtered_data AS (
    SELECT col3 FROM tableB WHERE col3 > 10
)
SELECT col2
FROM tableA
WHERE col1 IN (SELECT col3 FROM filtered_data);
```

## Key Conversion Notes

| Sybase IQ Pattern          | Snowflake Equivalent               |
| -------------------------- | ---------------------------------- |
| Correlated scalar subquery | Add `ANY_VALUE()` wrapper          |
| `TOP n`                    | `LIMIT n`                          |
| `NUMBER(*)`                | `ROW_NUMBER() OVER (...)`          |
| `FIRST_VALUE()`            | `FIRST_VALUE() OVER (...)`         |
| `CONVERT(type, expr)`      | `expr::type`                       |
| `ISNULL(a, b)`             | `COALESCE(a, b)` or `IFNULL(a, b)` |
| `GETDATE()`                | `CURRENT_TIMESTAMP()`              |
| `DATEADD(unit, n, date)`   | `DATEADD(unit, n, date)` (same)    |
| `DATEDIFF(unit, a, b)`     | `DATEDIFF(unit, a, b)` (same)      |
| No trailing semicolon      | Add semicolons                     |
