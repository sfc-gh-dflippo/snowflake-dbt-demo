# SAS PROC SQL to Snowflake Conversion

## When to Load

Load when SAS code contains: `PROC SQL`, `QUIT`, `CALCULATED` keyword, or SAS-specific SQL functions.

---

## Overview

PROC SQL is mostly ANSI SQL compliant, so conversion is often straightforward. Key differences are SAS-specific extensions and functions.

## Basic Structure

**SAS:**
```sas
PROC SQL;
  CREATE TABLE output AS
  SELECT column1, column2
  FROM input
  WHERE condition;
QUIT;
```

**Snowflake:**
```sql
CREATE TABLE output AS
SELECT column1, column2
FROM input
WHERE condition;
```

## Key Differences

### Table Creation

**SAS:**
```sas
PROC SQL;
  CREATE TABLE new_table AS
  SELECT * FROM source;
QUIT;
```

**Snowflake:**
```sql
CREATE OR REPLACE TABLE new_table AS
SELECT * FROM source;
```

### Calculated Columns Reference

**SAS allows referencing calculated columns:**
```sas
PROC SQL;
  SELECT a, b, a+b AS total, CALCULATED total * 0.1 AS tax
  FROM mytable;
QUIT;
```

**Snowflake requires subquery or CTE:**
```sql
WITH base AS (
  SELECT a, b, a + b AS total
  FROM mytable
)
SELECT *, total * 0.1 AS tax
FROM base;
```

### Case Sensitivity

**SAS:** Case-insensitive by default
**Snowflake:** Case-insensitive for unquoted identifiers, case-sensitive for quoted

```sql
-- These are equivalent in Snowflake:
SELECT column1 FROM TABLE1;
SELECT COLUMN1 FROM table1;

-- This preserves case:
SELECT "Column1" FROM "Table1";
```

## Function Mappings

> **Note:** Basic function mappings are in `common-patterns.md`. Below are comprehensive PROC SQL-specific mappings.

### String Functions (Extended)

| SAS PROC SQL | Snowflake |
|--------------|-----------|
| `PROPCASE(str)` | `INITCAP(str)` |
| `LENGTH(str)` | `LENGTH(str)` |
| `COMPRESS(str, 'ad')` | `REGEXP_REPLACE(str, '[^a-zA-Z0-9]', '')` |
| `CAT(a, b)` | `CONCAT(a, b)` |
| `CATS(a, b)` | `CONCAT(TRIM(a), TRIM(b))` |
| `TRANWRD(str, find, rep)` | `REPLACE(str, find, rep)` |

### Numeric Functions

| SAS PROC SQL | Snowflake |
|--------------|-----------|
| `ABS(x)` | `ABS(x)` |
| `CEIL(x)` | `CEIL(x)` |
| `FLOOR(x)` | `FLOOR(x)` |
| `ROUND(x, d)` | `ROUND(x, d)` |
| `INT(x)` | `TRUNC(x)` |
| `MOD(x, y)` | `MOD(x, y)` |
| `SQRT(x)` | `SQRT(x)` |
| `LOG(x)` | `LN(x)` |
| `LOG10(x)` | `LOG(10, x)` |
| `EXP(x)` | `EXP(x)` |
| `RANUNI(seed)` | `RANDOM()` / `UNIFORM(0::FLOAT, 1::FLOAT, RANDOM())` |

### Date Functions

| SAS PROC SQL | Snowflake |
|--------------|-----------|
| `TODAY()` | `CURRENT_DATE()` |
| `DATETIME()` | `CURRENT_TIMESTAMP()` |
| `DATEPART(datetime)` | `DATE(datetime)` or `datetime::DATE` |
| `TIMEPART(datetime)` | `TIME(datetime)` or `datetime::TIME` |
| `INTCK('unit', a, b)` | `DATEDIFF(unit, a, b)` |
| `INTNX('unit', date, n)` | `DATEADD(unit, n, date)` |
| `YEAR(date)` | `YEAR(date)` |
| `QTR(date)` | `QUARTER(date)` |
| `MONTH(date)` | `MONTH(date)` |
| `WEEK(date)` | `WEEKOFYEAR(date)` |
| `DAY(date)` | `DAY(date)` |
| `WEEKDAY(date)` | `DAYOFWEEK(date)` |

### Aggregate Functions

| SAS PROC SQL | Snowflake |
|--------------|-----------|
| `SUM(x)` | `SUM(x)` |
| `AVG(x)` | `AVG(x)` |
| `MIN(x)` | `MIN(x)` |
| `MAX(x)` | `MAX(x)` |
| `COUNT(*)` | `COUNT(*)` |
| `COUNT(DISTINCT x)` | `COUNT(DISTINCT x)` |
| `STD(x)` | `STDDEV(x)` |
| `VAR(x)` | `VARIANCE(x)` |
| `N(x)` | `COUNT(x)` |
| `NMISS(x)` | `COUNT(*) - COUNT(x)` |
| `USS(x)` | `SUM(x * x)` |
| `CSS(x)` | Use CTE: `WITH s AS (SELECT AVG(x) AS m FROM t) SELECT SUM(POWER(x-s.m,2)) FROM t,s` |

### NULL/Missing Handling

| SAS PROC SQL | Snowflake |
|--------------|-----------|
| `COALESCE(a, b, c)` | `COALESCE(a, b, c)` |
| `NULLIF(a, b)` | `NULLIF(a, b)` |
| `IFNULL(a, b)` | `IFNULL(a, b)` or `NVL(a, b)` |
| `MISSING(x)` | `x IS NULL` |

## Join Syntax

### Inner Join

**SAS:**
```sas
PROC SQL;
  SELECT a.*, b.col1
  FROM table_a a, table_b b
  WHERE a.key = b.key;
QUIT;
```

**Snowflake (explicit JOIN preferred):**
```sql
SELECT a.*, b.col1
FROM table_a a
INNER JOIN table_b b ON a.key = b.key;
```

### Left Join

**SAS:**
```sas
PROC SQL;
  SELECT a.*, b.col1
  FROM table_a a LEFT JOIN table_b b
  ON a.key = b.key;
QUIT;
```

**Snowflake:**
```sql
SELECT a.*, b.col1
FROM table_a a
LEFT JOIN table_b b ON a.key = b.key;
```

## Subqueries

**SAS:**
```sas
PROC SQL;
  SELECT * FROM orders
  WHERE customer_id IN (SELECT customer_id FROM vip_customers);
QUIT;
```

**Snowflake (identical):**
```sql
SELECT * FROM orders
WHERE customer_id IN (SELECT customer_id FROM vip_customers);
```

## GROUP BY with HAVING

**SAS:**
```sas
PROC SQL;
  SELECT customer_id, SUM(amount) AS total
  FROM orders
  GROUP BY customer_id
  HAVING CALCULATED total > 1000;
QUIT;
```

**Snowflake:**
```sql
SELECT customer_id, SUM(amount) AS total
FROM orders
GROUP BY customer_id
HAVING SUM(amount) > 1000;
```

## UNION Operations

**SAS:**
```sas
PROC SQL;
  SELECT * FROM table1
  UNION
  SELECT * FROM table2;
QUIT;
```

**Snowflake (identical):**
```sql
SELECT * FROM table1
UNION
SELECT * FROM table2;

-- UNION ALL (keep duplicates)
SELECT * FROM table1
UNION ALL
SELECT * FROM table2;
```

### Heterogeneous schemas → `UNION ALL BY NAME`

Positional `UNION` / `UNION ALL` requires every branch to have the **same column count and order**. When a SAS `SET table1 table2 table3;` (or set-operation) stacks datasets with **different column sets** — common when the tables were built by separate `PROC IMPORT`/transformation paths or come from different vendors — use `UNION ALL BY NAME`, which aligns columns by name and fills missing columns with NULL.

```sql
-- Datasets with different/extra columns:
SELECT * FROM table1
UNION ALL BY NAME
SELECT * FROM table2
UNION ALL BY NAME
SELECT * FROM table3;
```

- Use `... BY NAME` whenever the stacked sources may have differing columns (different vendors, different import blocks, different transformation paths).
- Keep plain positional `UNION ALL` only when all sources share an identical schema (same columns, same order — e.g., built from one DDL template).
- Do not silently deduplicate: SAS `SET` stacks rows (like `UNION ALL`), so preserve `ALL` unless the SAS logic explicitly removes duplicates.

## INTO Clause (Creating Macro Variables)

**SAS:**
```sas
PROC SQL NOPRINT;
  SELECT COUNT(*) INTO :row_count FROM mytable;
QUIT;
```

**Snowflake (use variables in stored procedures):**
```sql
CREATE OR REPLACE PROCEDURE get_row_count(table_name STRING)
RETURNS INTEGER
LANGUAGE SQL
AS
$$
DECLARE
  row_count INTEGER;
BEGIN
  SELECT COUNT(*) INTO :row_count FROM IDENTIFIER(:table_name);
  RETURN row_count;
END;
$$;
```

## PROC SQL Options

| SAS Option | Snowflake Equivalent |
|------------|---------------------|
| `NOPRINT` | Don't display (default in scripts) |
| `OUTOBS=n` | `LIMIT n` |
| `NUMBER` | `ROW_NUMBER() OVER()` |
| `DOUBLE` | N/A (formatting) |
