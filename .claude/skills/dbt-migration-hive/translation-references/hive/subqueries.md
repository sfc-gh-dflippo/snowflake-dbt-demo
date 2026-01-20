---
description: Hive subquery patterns and their Snowflake equivalents
title: Hive Subqueries to Snowflake
---

# Subquery Patterns

## Overview

A subquery is a query within another query. Subqueries can be:

- **Correlated**: Reference columns from the outer query (executed per row)
- **Uncorrelated**: Independent of the outer query (executed once)
- **Scalar**: Return a single value
- **Non-scalar**: Return multiple values

**Note**: Hive has limited subquery support compared to traditional databases. Correlated subqueries
were added in Hive 0.13+.

## Setup Data

### Hive

```sql
CREATE TABLE tableA (
    col1 INT,
    col2 STRING
);

CREATE TABLE tableB (
    col3 INT,
    col4 STRING
);

INSERT INTO tableA VALUES (50, 'Hey'), (20, 'Example');
INSERT INTO tableB VALUES (50, 'Hey'), (20, 'Bye');
```

### Snowflake Equivalent

```sql
CREATE OR REPLACE TABLE tableA (
    col1 INTEGER,
    col2 VARCHAR
);

CREATE OR REPLACE TABLE tableB (
    col3 INTEGER,
    col4 VARCHAR
);

INSERT INTO tableA VALUES (50, 'Hey'), (20, 'Example');
INSERT INTO tableB VALUES (50, 'Hey'), (20, 'Bye');
```

## Correlated Scalar Subqueries

Snowflake evaluates correlated subqueries at compile time. Use `ANY_VALUE()` to ensure single-value
return.

### Hive

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

### Hive

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

Subqueries with IN/EXISTS operators are supported in both platforms.

### Hive

```sql
-- IN operator (most common in Hive)
SELECT col2
FROM tableA
WHERE col1 IN (SELECT col3 FROM tableB);

-- EXISTS operator (Hive 0.13+)
SELECT col2
FROM tableA a
WHERE EXISTS (SELECT 1 FROM tableB b WHERE a.col1 = b.col3);

-- Derived table (supported in Hive)
SELECT col2, derived_table.col4
FROM tableA
JOIN (SELECT * FROM tableB) derived_table
ON col1 = derived_table.col3;
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
FROM tableA
JOIN (SELECT * FROM tableB) AS derived_table
ON col1 = derived_table.col3;
```

## Hive-Specific Subquery Patterns

### LATERAL VIEW with Subqueries

Hive's LATERAL VIEW for array explosion needs conversion.

### Hive

```sql
SELECT col2, exploded_val
FROM tableA
LATERAL VIEW explode(split(col2, ',')) t AS exploded_val;
```

### Snowflake

```sql
SELECT col2, f.value::VARCHAR AS exploded_val
FROM tableA,
LATERAL FLATTEN(input => SPLIT(col2, ',')) f;
```

### Semi-Joins (LEFT SEMI JOIN)

### Hive

```sql
-- Hive LEFT SEMI JOIN (returns rows from left where match exists)
SELECT a.col1, a.col2
FROM tableA a
LEFT SEMI JOIN tableB b ON a.col1 = b.col3;
```

### Snowflake

```sql
-- Convert to EXISTS or IN
SELECT col1, col2
FROM tableA
WHERE col1 IN (SELECT col3 FROM tableB);

-- Or use EXISTS
SELECT a.col1, a.col2
FROM tableA a
WHERE EXISTS (SELECT 1 FROM tableB b WHERE a.col1 = b.col3);
```

## Key Conversion Notes

| Hive Pattern               | Snowflake Equivalent         |
| -------------------------- | ---------------------------- |
| Correlated scalar subquery | Add `ANY_VALUE()` wrapper    |
| `LEFT SEMI JOIN`           | `WHERE EXISTS` or `WHERE IN` |
| `LATERAL VIEW explode()`   | `LATERAL FLATTEN()`          |
| `INT`                      | `INTEGER`                    |
| `STRING`                   | `VARCHAR`                    |
| `BIGINT`                   | `NUMBER(38,0)` or `BIGINT`   |
| `DOUBLE`                   | `DOUBLE` or `FLOAT`          |
| `array<type>`              | `ARRAY`                      |
| `map<k,v>`                 | `OBJECT`                     |
