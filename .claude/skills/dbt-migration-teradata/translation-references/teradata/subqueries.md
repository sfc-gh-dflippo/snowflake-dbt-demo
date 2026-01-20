---
description: Teradata subquery patterns and their Snowflake equivalents
title: Teradata Subqueries to Snowflake
---

# Subquery Patterns

## Overview

A subquery is a query within another query. Subqueries can be:

- **Correlated**: Reference columns from the outer query (executed per row)
- **Uncorrelated**: Independent of the outer query (executed once)
- **Scalar**: Return a single value
- **Non-scalar**: Return multiple values

## Setup Data

### Teradata

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

### Teradata

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
    WHERE RTRIM(col2) = RTRIM(col4)
);
```

**Note**: Teradata's implicit VARCHAR trimming requires explicit `RTRIM()` in Snowflake.

## Uncorrelated Scalar Subqueries

Fully supported in Snowflake without modification.

### Teradata

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

### Teradata

```sql
-- IN operator
SELECT col2
FROM tableA
WHERE col1 IN (SELECT col3 FROM tableB);

-- ALL operator
SELECT col2
FROM tableA
WHERE col1 >= ALL(SELECT col3 FROM tableB);

-- Derived table
SELECT col2, myDerivedTable.col4
FROM tableA, (SELECT * FROM tableB) AS myDerivedTable
WHERE col1 = myDerivedTable.col3;
```

### Snowflake

```sql
-- IN operator (direct conversion)
SELECT col2
FROM tableA
WHERE col1 IN (SELECT col3 FROM tableB);

-- ALL operator (direct conversion)
SELECT col2
FROM tableA
WHERE col1 >= ALL(SELECT col3 FROM tableB);

-- Derived table (direct conversion)
SELECT col2, derived_table.col4
FROM tableA, (SELECT * FROM tableB) AS derived_table
WHERE col1 = derived_table.col3;
```

## Key Conversion Notes

| Teradata Pattern           | Snowflake Equivalent              |
| -------------------------- | --------------------------------- |
| Correlated scalar subquery | Add `ANY_VALUE()` wrapper         |
| VARCHAR comparisons        | Add `RTRIM()` for trailing spaces |
| QUALIFY with ROW_NUMBER    | Supported natively                |
| Derived tables             | Direct conversion                 |
