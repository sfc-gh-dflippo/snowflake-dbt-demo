---
description: Oracle subquery patterns and their Snowflake equivalents
title: Oracle Subqueries to Snowflake
---

## Subquery Patterns

## Overview

A subquery is a query within another query. Subqueries can be:

- **Correlated**: Reference columns from the outer query (executed per row)
- **Uncorrelated**: Independent of the outer query (executed once)
- **Scalar**: Return a single value
- **Non-scalar**: Return multiple values

## Setup Data

### Oracle

```sql
CREATE TABLE tableA (
    col1 NUMBER,
    col2 VARCHAR2(20)
);

CREATE TABLE tableB (
    col3 NUMBER,
    col4 VARCHAR2(20)
);

INSERT INTO tableA VALUES (50, 'Hey');
INSERT INTO tableA VALUES (20, 'Example');
INSERT INTO tableB VALUES (50, 'Hey');
INSERT INTO tableB VALUES (20, 'Bye');
COMMIT;
```

### Snowflake Equivalent

```sql
CREATE OR REPLACE TABLE tableA (
    col1 NUMBER,
    col2 VARCHAR(20)
);

CREATE OR REPLACE TABLE tableB (
    col3 NUMBER,
    col4 VARCHAR(20)
);

INSERT INTO tableA VALUES (50, 'Hey'), (20, 'Example');
INSERT INTO tableB VALUES (50, 'Hey'), (20, 'Bye');
```

## Correlated Scalar Subqueries

Snowflake evaluates correlated subqueries at compile time. Use `ANY_VALUE()` to ensure single-value
return.

### Oracle 2

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

### Oracle 3

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

### Oracle 4

```sql
-- IN operator
SELECT col2
FROM tableA
WHERE col1 IN (SELECT col3 FROM tableB);

-- EXISTS operator
SELECT col2
FROM tableA a
WHERE EXISTS (SELECT 1 FROM tableB b WHERE a.col1 = b.col3);

-- Derived table (inline view)
SELECT col2, derived_table.col4
FROM tableA, (SELECT * FROM tableB) derived_table
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

## FETCH FIRST Clause in Subqueries

**Important**: Oracle allows FETCH in any subquery; Snowflake only allows it in uncorrelated scalar
subqueries.

### Oracle 5

```sql
-- Correlated scalar with FETCH (NOT supported in Snowflake)
SELECT col2
FROM tableA
WHERE col2 = (SELECT col4 FROM tableB WHERE col3 = col1 FETCH FIRST ROW ONLY);

-- Uncorrelated scalar with FETCH (supported)
SELECT col2
FROM tableA
WHERE col2 = (SELECT col4 FROM tableB FETCH FIRST ROW ONLY);
```

### Snowflake Workaround for Correlated FETCH

```sql
-- Use ROW_NUMBER() window function instead
SELECT a.col2
FROM tableA a
WHERE a.col2 = (
    SELECT col4
    FROM (
        SELECT col4, ROW_NUMBER() OVER (ORDER BY col3) AS rn
        FROM tableB
        WHERE col3 = a.col1
    )
    WHERE rn = 1
);

-- Or use QUALIFY
SELECT a.col2
FROM tableA a
INNER JOIN tableB b ON a.col1 = b.col3
QUALIFY ROW_NUMBER() OVER (PARTITION BY a.col2 ORDER BY b.col3) = 1;
```

## Key Conversion Notes

| Oracle Pattern             | Snowflake Equivalent               |
| -------------------------- | ---------------------------------- |
| Correlated scalar subquery | Add `ANY_VALUE()` wrapper          |
| `FETCH FIRST n ROWS ONLY`  | `LIMIT n` (uncorrelated only)      |
| `(+)` outer join syntax    | Convert to ANSI JOIN               |
| `ROWNUM` in subquery       | Use `ROW_NUMBER()` window function |
| `CONNECT BY` hierarchical  | Convert to recursive CTE           |
| `VARCHAR2`                 | `VARCHAR`                          |
| `NUMBER`                   | `NUMBER` (compatible)              |
