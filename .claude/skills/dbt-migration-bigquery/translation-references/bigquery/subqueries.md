---
description: BigQuery subquery patterns and their Snowflake equivalents
title: BigQuery Subqueries to Snowflake
---

# Subquery Patterns

## Overview

A subquery is a query within another query. Subqueries can be:

- **Correlated**: Reference columns from the outer query (executed per row)
- **Uncorrelated**: Independent of the outer query (executed once)
- **Scalar**: Return a single value
- **Non-scalar**: Return multiple values

## Setup Data

### BigQuery

```sql
CREATE TABLE dataset.tableA (
    col1 INT64,
    col2 STRING
);

CREATE TABLE dataset.tableB (
    col3 INT64,
    col4 STRING
);

INSERT INTO dataset.tableA VALUES (50, 'Hey'), (20, 'Example');
INSERT INTO dataset.tableB VALUES (50, 'Hey'), (20, 'Bye');
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

### BigQuery

```sql
SELECT col2
FROM dataset.tableA
WHERE col1 = (SELECT col3 FROM dataset.tableB WHERE col2 = col4);
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

### BigQuery

```sql
SELECT col2, (SELECT AVG(col3) FROM dataset.tableB) AS avgTableB
FROM dataset.tableA
WHERE col1 = (SELECT MAX(col3) FROM dataset.tableB);
```

### Snowflake

```sql
SELECT col2, (SELECT AVG(col3) FROM tableB) AS avg_table_b
FROM tableA
WHERE col1 = (SELECT MAX(col3) FROM tableB);
```

## Non-Scalar Subqueries

Subqueries with IN/ANY/ALL/EXISTS operators are supported.

### BigQuery

```sql
-- IN operator
SELECT col2
FROM dataset.tableA
WHERE col1 IN (SELECT col3 FROM dataset.tableB);

-- EXISTS operator
SELECT col2
FROM dataset.tableA a
WHERE EXISTS (SELECT 1 FROM dataset.tableB b WHERE a.col1 = b.col3);

-- Derived table
SELECT col2, derived_table.col4
FROM dataset.tableA, (SELECT * FROM dataset.tableB) AS derived_table
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

## BigQuery-Specific Subquery Patterns

### ARRAY Subqueries

BigQuery's ARRAY subqueries need conversion to Snowflake's ARRAY_AGG.

### BigQuery

```sql
SELECT col2,
       ARRAY(SELECT col3 FROM dataset.tableB WHERE col3 > 10) AS col3_array
FROM dataset.tableA;
```

### Snowflake

```sql
SELECT col2,
       (SELECT ARRAY_AGG(col3) FROM tableB WHERE col3 > 10) AS col3_array
FROM tableA;
```

### WITH Clause (CTE)

Both platforms support CTEs with similar syntax.

### BigQuery

```sql
WITH filtered AS (
    SELECT col3 FROM dataset.tableB WHERE col3 > 10
)
SELECT col2
FROM dataset.tableA
WHERE col1 IN (SELECT col3 FROM filtered);
```

### Snowflake

```sql
WITH filtered AS (
    SELECT col3 FROM tableB WHERE col3 > 10
)
SELECT col2
FROM tableA
WHERE col1 IN (SELECT col3 FROM filtered);
```

## Key Conversion Notes

| BigQuery Pattern           | Snowflake Equivalent                |
| -------------------------- | ----------------------------------- |
| Correlated scalar subquery | Add `ANY_VALUE()` wrapper           |
| `ARRAY(SELECT ...)`        | `(SELECT ARRAY_AGG(...))`           |
| `dataset.table` reference  | Remove dataset prefix or use schema |
| `INT64`                    | `INTEGER` or `NUMBER`               |
| `STRING`                   | `VARCHAR`                           |
| `SAFE_DIVIDE(a, b)`        | `IFF(b = 0, NULL, a / b)`           |
| `IFNULL(a, b)`             | `COALESCE(a, b)` or `IFNULL(a, b)`  |
