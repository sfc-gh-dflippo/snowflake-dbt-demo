---
description: DB2 subquery patterns and their Snowflake equivalents
title: DB2 Subqueries to Snowflake
---

## Subquery Patterns

## Overview

A subquery is a query within another query. Subqueries can be:

- **Correlated**: Reference columns from the outer query (executed per row)
- **Uncorrelated**: Independent of the outer query (executed once)
- **Scalar**: Return a single value
- **Non-scalar**: Return multiple values

## Setup Data

### DB2

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

### DB2 2

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

### DB2 3

```sql
SELECT col2, (SELECT AVG(col3) FROM tableB) AS avgTableB
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

### DB2 4

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

## DB2-Specific Subquery Patterns

### FETCH FIRST with Subqueries

### DB2 5

```sql
-- FETCH FIRST in subquery
SELECT col2
FROM tableA
WHERE col1 = (SELECT col3 FROM tableB ORDER BY col3 FETCH FIRST 1 ROW ONLY);
```

### Snowflake 4

```sql
-- Use LIMIT instead
SELECT col2
FROM tableA
WHERE col1 = (SELECT col3 FROM tableB ORDER BY col3 LIMIT 1);
```

### Common Table Expressions

### DB2 6

```sql
WITH filtered_data AS (
    SELECT col3 FROM tableB WHERE col3 > 10
)
SELECT col2
FROM tableA
WHERE col1 IN (SELECT col3 FROM filtered_data);
```

### Snowflake 5

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

| DB2 Pattern                | Snowflake Equivalent               |
| -------------------------- | ---------------------------------- |
| Correlated scalar subquery | Add `ANY_VALUE()` wrapper          |
| `FETCH FIRST n ROWS ONLY`  | `LIMIT n`                          |
| `VALUES` clause            | `SELECT ... UNION ALL` or `VALUES` |
| `DECIMAL(p,s)`             | `NUMBER(p,s)`                      |
| `CLOB`                     | `VARCHAR` (up to 16MB)             |
| `BLOB`                     | `BINARY`                           |
| `CURRENT DATE`             | `CURRENT_DATE()`                   |
| `CURRENT TIMESTAMP`        | `CURRENT_TIMESTAMP()`              |
