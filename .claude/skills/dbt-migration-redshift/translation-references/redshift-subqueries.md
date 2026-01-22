---
description: Redshift subquery patterns and their Snowflake equivalents
title: Redshift Subqueries to Snowflake
---

## Subquery Patterns

## Overview

A subquery is a query within another query. Subqueries can be:

- **Correlated**: Reference columns from the outer query (executed per row)
- **Uncorrelated**: Independent of the outer query (executed once)
- **Scalar**: Return a single value
- **Non-scalar**: Return multiple values

Redshift is PostgreSQL-based, so most patterns convert directly to Snowflake.

## Setup Data

### Redshift

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

### Redshift 2

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

### Redshift 3

```sql
SELECT col2, (SELECT AVG(col3) FROM tableB) AS avg_table_b
FROM tableA
WHERE col1 = (SELECT MAX(col3) FROM tableB);
```

### Snowflake 2

```sql
SELECT col2, (SELECT AVG(col3) FROM tableB) AS avg_table_b
FROM tableA
WHERE col1 = (SELECT MAX(col3) FROM tableB);
```

## Non-Scalar Subqueries

Subqueries with IN/ANY/ALL/EXISTS operators are supported.

### Redshift 4

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

-- Derived table (direct conversion)
SELECT col2, derived_table.col4
FROM tableA, (SELECT * FROM tableB) AS derived_table
WHERE col1 = derived_table.col3;
```

## Redshift-Specific Subquery Patterns

### WITH Clause and Materialization Hints

### Redshift 5

```sql
-- Redshift may use WITH NO SCHEMA BINDING for late binding views
WITH filtered AS (
    SELECT col3 FROM tableB WHERE col3 > 10
)
SELECT col2
FROM tableA
WHERE col1 IN (SELECT col3 FROM filtered);
```

### Snowflake 4

```sql
-- Direct conversion (materialization handled automatically)
WITH filtered AS (
    SELECT col3 FROM tableB WHERE col3 > 10
)
SELECT col2
FROM tableA
WHERE col1 IN (SELECT col3 FROM filtered);
```

### LISTAGG in Subqueries

### Redshift 6

```sql
SELECT col2,
       (SELECT LISTAGG(col4, ', ') WITHIN GROUP (ORDER BY col4)
        FROM tableB WHERE col3 = col1) AS col4_list
FROM tableA;
```

### Snowflake 5

```sql
SELECT col2,
       (SELECT LISTAGG(col4, ', ') WITHIN GROUP (ORDER BY col4)
        FROM tableB WHERE col3 = col1) AS col4_list
FROM tableA;
```

### Window Functions as Subquery Alternative

### Redshift 7

```sql
-- Using subquery for row numbering
SELECT *
FROM (
    SELECT col2, col1,
           ROW_NUMBER() OVER (ORDER BY col1) AS rn
    FROM tableA
) subq
WHERE rn = 1;
```

### Snowflake 6

```sql
-- Use QUALIFY instead of subquery
SELECT col2, col1
FROM tableA
QUALIFY ROW_NUMBER() OVER (ORDER BY col1) = 1;
```

## Key Conversion Notes

| Redshift Pattern           | Snowflake Equivalent              |
| -------------------------- | --------------------------------- |
| Correlated scalar subquery | Add `ANY_VALUE()` wrapper         |
| `DISTKEY` / `SORTKEY`      | Remove (Snowflake auto-optimizes) |
| `DISTSTYLE`                | Remove                            |
| `ENCODE` compression       | Remove                            |
| `GETDATE()`                | `CURRENT_TIMESTAMP()`             |
| `DATEDIFF(unit, a, b)`     | `DATEDIFF(unit, a, b)` (same)     |
| `NVL(a, b)`                | `COALESCE(a, b)` or `NVL(a, b)`   |
| `NVL2(a, b, c)`            | `IFF(a IS NOT NULL, b, c)`        |
| `CONVERT(type, expr)`      | `expr::type`                      |
| Window + ROW_NUMBER filter | Use `QUALIFY` clause              |
