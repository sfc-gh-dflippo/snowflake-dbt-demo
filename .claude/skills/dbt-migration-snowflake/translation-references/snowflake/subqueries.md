---
description: Snowflake subquery patterns for dbt model conversion
title: Snowflake Subqueries in dbt Models
---

# Subquery Patterns for dbt Conversion

## Overview

When converting Snowflake views and tables to dbt models, subqueries should often be refactored into
CTEs or separate models for better maintainability and testing.

A subquery is a query within another query. Subqueries can be:

- **Correlated**: Reference columns from the outer query (executed per row)
- **Uncorrelated**: Independent of the outer query (executed once)
- **Scalar**: Return a single value
- **Non-scalar**: Return multiple values

## Setup Data

### Snowflake

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

Use `ANY_VALUE()` to ensure single-value return in correlated subqueries.

### Snowflake (Original)

```sql
SELECT col2
FROM tableA
WHERE col1 = (SELECT col3 FROM tableB WHERE col2 = col4);
```

### dbt Model (Refactored to CTE)

```sql
WITH matched_values AS (
    SELECT
        col4,
        ANY_VALUE(col3)::INTEGER AS col3
    FROM {{ ref('table_b') }}
    GROUP BY col4
)

SELECT
    a.col2::VARCHAR(20) AS col2
FROM {{ ref('table_a') }} a
INNER JOIN matched_values m ON a.col2 = m.col4 AND a.col1 = m.col3
```

## Uncorrelated Scalar Subqueries

Can be converted to CTEs for clarity.

### Snowflake (Original)

```sql
SELECT col2, (SELECT AVG(col3) FROM tableB) AS avg_table_b
FROM tableA
WHERE col1 = (SELECT MAX(col3) FROM tableB);
```

### dbt Model (Refactored)

```sql
WITH table_b_stats AS (
    SELECT
        AVG(col3)::NUMBER(18,6) AS avg_col3,
        MAX(col3)::INTEGER AS max_col3
    FROM {{ ref('table_b') }}
)

SELECT
    a.col2::VARCHAR(20) AS col2,
    s.avg_col3 AS avg_table_b
FROM {{ ref('table_a') }} a
CROSS JOIN table_b_stats s
WHERE a.col1 = s.max_col3
```

## Non-Scalar Subqueries

Convert to CTEs or separate models for reusability.

### Snowflake (Original)

```sql
-- IN operator
SELECT col2
FROM tableA
WHERE col1 IN (SELECT col3 FROM tableB);

-- Derived table
SELECT col2, derived_table.col4
FROM tableA, (SELECT * FROM tableB) AS derived_table
WHERE col1 = derived_table.col3;
```

### dbt Model (Refactored)

```sql
-- IN operator as CTE
WITH valid_col3_values AS (
    SELECT DISTINCT col3::INTEGER AS col3
    FROM {{ ref('table_b') }}
)

SELECT
    a.col2::VARCHAR(20) AS col2
FROM {{ ref('table_a') }} a
WHERE a.col1 IN (SELECT col3 FROM valid_col3_values)

-- Or convert derived table to explicit join
SELECT
    a.col2::VARCHAR(20) AS col2,
    b.col4::VARCHAR(20) AS col4
FROM {{ ref('table_a') }} a
INNER JOIN {{ ref('table_b') }} b ON a.col1 = b.col3
```

## QUALIFY Clause

Snowflake's QUALIFY eliminates need for subqueries with window functions.

### Snowflake (Subquery Pattern)

```sql
SELECT *
FROM (
    SELECT col2, col1,
           ROW_NUMBER() OVER (ORDER BY col1) AS rn
    FROM tableA
) subq
WHERE rn = 1;
```

### dbt Model (Using QUALIFY)

```sql
SELECT
    col2::VARCHAR(20) AS col2,
    col1::INTEGER AS col1
FROM {{ ref('table_a') }}
QUALIFY ROW_NUMBER() OVER (ORDER BY col1) = 1
```

## Best Practices for dbt Conversion

### 1. Extract Repeated Subqueries to Separate Models

```sql
-- Instead of embedding this subquery multiple times:
-- (SELECT MAX(col3) FROM tableB)

-- Create a separate model: models/intermediate/int_table_b_stats.sql
SELECT
    MAX(col3)::INTEGER AS max_col3,
    MIN(col3)::INTEGER AS min_col3,
    AVG(col3)::NUMBER(18,6) AS avg_col3
FROM {{ ref('table_b') }}
```

### 2. Use CTEs for Complex Subqueries

```sql
-- Original with nested subqueries
SELECT col2
FROM tableA
WHERE col1 > (SELECT AVG(col3) FROM tableB WHERE col3 IN (SELECT col1 FROM tableA));

-- Refactored with CTEs
WITH relevant_col1 AS (
    SELECT DISTINCT col1::INTEGER AS col1
    FROM {{ ref('table_a') }}
),

filtered_avg AS (
    SELECT AVG(col3)::NUMBER(18,6) AS avg_col3
    FROM {{ ref('table_b') }}
    WHERE col3 IN (SELECT col1 FROM relevant_col1)
)

SELECT
    a.col2::VARCHAR(20) AS col2
FROM {{ ref('table_a') }} a
CROSS JOIN filtered_avg f
WHERE a.col1 > f.avg_col3
```

### 3. Replace Correlated Subqueries with Joins

```sql
-- Correlated subquery (less efficient)
SELECT col2,
       (SELECT MAX(col4) FROM tableB WHERE col3 = col1) AS max_col4
FROM tableA;

-- Join pattern (more efficient in dbt)
WITH max_col4_by_col3 AS (
    SELECT
        col3::INTEGER AS col3,
        MAX(col4)::VARCHAR(20) AS max_col4
    FROM {{ ref('table_b') }}
    GROUP BY col3
)

SELECT
    a.col2::VARCHAR(20) AS col2,
    m.max_col4
FROM {{ ref('table_a') }} a
LEFT JOIN max_col4_by_col3 m ON a.col1 = m.col3
```

## Key Patterns

| Original Pattern        | dbt Best Practice         |
| ----------------------- | ------------------------- |
| Repeated subquery       | Extract to separate model |
| Complex nested subquery | Refactor to CTEs          |
| Correlated subquery     | Convert to JOIN           |
| Derived table           | Use CTE or `ref()`        |
| Window + WHERE filter   | Use QUALIFY               |
| SELECT in SELECT list   | Use CTE + CROSS JOIN      |
