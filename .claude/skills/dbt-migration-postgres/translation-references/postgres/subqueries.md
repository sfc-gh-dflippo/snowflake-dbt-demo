---
description: PostgreSQL subquery patterns and their Snowflake equivalents
title: PostgreSQL Subqueries to Snowflake
---

# Subquery Patterns

## Overview

A subquery is a query within another query. Subqueries can be:

- **Correlated**: Reference columns from the outer query (executed per row)
- **Uncorrelated**: Independent of the outer query (executed once)
- **Scalar**: Return a single value
- **Non-scalar**: Return multiple values

PostgreSQL has excellent subquery support, most patterns convert directly to Snowflake.

## Setup Data

### PostgreSQL

```sql
CREATE TABLE tableA (
    col1 INTEGER,
    col2 VARCHAR(20)
);

CREATE TABLE tableB (
    col3 INTEGER,
    col4 VARCHAR(20)
);

INSERT INTO tableA VALUES (50, 'Hey'), (20, 'Example');
INSERT INTO tableB VALUES (50, 'Hey'), (20, 'Bye');
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

### PostgreSQL

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

### PostgreSQL

```sql
SELECT col2, (SELECT AVG(col3) FROM tableB) AS avg_table_b
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

### PostgreSQL

```sql
-- IN operator
SELECT col2
FROM tableA
WHERE col1 IN (SELECT col3 FROM tableB);

-- ANY operator
SELECT col2
FROM tableA
WHERE col1 = ANY(SELECT col3 FROM tableB);

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

-- ANY operator (direct conversion)
SELECT col2
FROM tableA
WHERE col1 = ANY(SELECT col3 FROM tableB);

-- EXISTS operator (direct conversion)
SELECT col2
FROM tableA a
WHERE EXISTS (SELECT 1 FROM tableB b WHERE a.col1 = b.col3);

-- Derived table (direct conversion)
SELECT col2, derived_table.col4
FROM tableA, (SELECT * FROM tableB) AS derived_table
WHERE col1 = derived_table.col3;
```

## PostgreSQL-Specific Subquery Patterns

### LATERAL Joins

### PostgreSQL

```sql
SELECT a.col2, b_latest.col4
FROM tableA a
CROSS JOIN LATERAL (
    SELECT col4
    FROM tableB b
    WHERE b.col3 = a.col1
    ORDER BY col3 DESC
    LIMIT 1
) b_latest;
```

### Snowflake

```sql
-- LATERAL is supported in Snowflake
SELECT a.col2, b_latest.col4
FROM tableA a,
LATERAL (
    SELECT col4
    FROM tableB b
    WHERE b.col3 = a.col1
    ORDER BY col3 DESC
    LIMIT 1
) b_latest;
```

### Array Subqueries with ARRAY()

### PostgreSQL

```sql
SELECT col2, ARRAY(SELECT col3 FROM tableB WHERE col3 > 10) AS col3_array
FROM tableA;
```

### Snowflake

```sql
SELECT col2, (SELECT ARRAY_AGG(col3) FROM tableB WHERE col3 > 10) AS col3_array
FROM tableA;
```

### Common Table Expressions (CTEs)

### PostgreSQL

```sql
WITH RECURSIVE hierarchy AS (
    SELECT col1, col2, 1 AS level
    FROM tableA
    WHERE col1 = 50
    UNION ALL
    SELECT a.col1, a.col2, h.level + 1
    FROM tableA a
    JOIN hierarchy h ON a.col1 = h.col1 - 10
    WHERE h.level < 5
)
SELECT * FROM hierarchy;
```

### Snowflake

```sql
-- Recursive CTEs supported in Snowflake
WITH RECURSIVE hierarchy AS (
    SELECT col1, col2, 1 AS level
    FROM tableA
    WHERE col1 = 50
    UNION ALL
    SELECT a.col1, a.col2, h.level + 1
    FROM tableA a
    JOIN hierarchy h ON a.col1 = h.col1 - 10
    WHERE h.level < 5
)
SELECT * FROM hierarchy;
```

## Key Conversion Notes

| PostgreSQL Pattern         | Snowflake Equivalent      |
| -------------------------- | ------------------------- |
| Correlated scalar subquery | Add `ANY_VALUE()` wrapper |
| `ARRAY(SELECT ...)`        | `(SELECT ARRAY_AGG(...))` |
| `LATERAL` subquery         | Supported directly        |
| `WITH RECURSIVE`           | Supported directly        |
| `SERIAL` / `BIGSERIAL`     | `AUTOINCREMENT`           |
| `TEXT`                     | `VARCHAR`                 |
| `JSONB`                    | `VARIANT`                 |
| `::type` casting           | Supported directly        |
| `ILIKE`                    | Supported directly        |
