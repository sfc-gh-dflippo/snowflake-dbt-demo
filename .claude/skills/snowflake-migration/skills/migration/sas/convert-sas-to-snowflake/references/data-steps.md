# SAS DATA Step to Snowflake Conversion

## When to Load

Load when SAS code contains: `DATA` step, `SET`, `MERGE`, `RETAIN`, `BY`-group processing, `OUTPUT`, arrays, or `FIRST.`/`LAST.` logic.

---

## SQL-First Decision Tree

```
DATA step detected
       │
       ▼
┌──────────────────────────────────────────────────────────────┐
│ Does it use RETAIN, FIRST./LAST., ARRAY, or complex IF?      │
└──────────────────────────────────────────────────────────────┘
       │
       ├── NO ──► Pure SQL (SELECT/CREATE TABLE AS)
       │
       └── YES ──► Check pattern below
                    │
       ┌────────────┴────────────┐
       │                         │
       ▼                         ▼
 Can use Window         Needs row-by-row
 Functions?             state management?
       │                         │
       ├── YES ──► SQL           └── Stored Procedure
       │    (LAG, SUM OVER,           (DECLARE, BEGIN/END)
       │     ROW_NUMBER)
       │
       └── NO ──► Stored Procedure
```

---

## TIER 1: Pure SQL Patterns

### Simple Column Transformations

**SAS:**
```sas
DATA customers_clean;
  SET customers;
  full_name = CATX(' ', first_name, last_name);
  age = INTCK('YEAR', birth_date, TODAY());
RUN;
```

**Snowflake SQL:**
```sql
CREATE OR REPLACE TABLE customers_clean AS
SELECT *,
  CONCAT_WS(' ', first_name, last_name) AS full_name,
  DATEDIFF('YEAR', birth_date, CURRENT_DATE()) AS age
FROM customers;
```

### Filtering (WHERE/IF)

**SAS:**
```sas
DATA active;
  SET customers;
  WHERE status = 'ACTIVE';
  IF age >= 18;
RUN;
```

**Snowflake SQL:**
```sql
CREATE OR REPLACE TABLE active AS
SELECT * FROM customers
WHERE status = 'ACTIVE' AND age >= 18;
```

### RETAIN - Running Totals (SQL with Window Functions)

**SAS:**
```sas
DATA running_totals;
  SET transactions;
  BY customer_id;
  RETAIN running_sum 0;
  IF FIRST.customer_id THEN running_sum = 0;
  running_sum = running_sum + amount;
RUN;
```

**Snowflake SQL (NOT stored procedure):**
```sql
CREATE OR REPLACE TABLE running_totals AS
SELECT *,
  SUM(amount) OVER (
    PARTITION BY customer_id 
    ORDER BY transaction_date 
    ROWS UNBOUNDED PRECEDING
  ) AS running_sum
FROM transactions;
```

### FIRST./LAST. Flags (SQL with Window Functions)

**SAS:**
```sas
DATA first_last;
  SET sorted_data;
  BY group_var;
  IF FIRST.group_var THEN first_flag = 1; ELSE first_flag = 0;
  IF LAST.group_var THEN last_flag = 1; ELSE last_flag = 0;
RUN;
```

**Snowflake SQL:**
```sql
CREATE OR REPLACE TABLE first_last AS
SELECT *,
  CASE WHEN ROW_NUMBER() OVER (PARTITION BY group_var ORDER BY sort_col) = 1 
       THEN 1 ELSE 0 END AS first_flag,
  CASE WHEN ROW_NUMBER() OVER (PARTITION BY group_var ORDER BY sort_col DESC) = 1 
       THEN 1 ELSE 0 END AS last_flag
FROM sorted_data;
```

### Keep Only Last Row per Group (SQL with QUALIFY)

**SAS:**
```sas
DATA last_per_group;
  SET data;
  BY customer_id;
  IF LAST.customer_id THEN OUTPUT;
RUN;
```

**Snowflake SQL:**
```sql
CREATE OR REPLACE TABLE last_per_group AS
SELECT * FROM data
QUALIFY ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY sort_col DESC) = 1;
```

### MERGE (Joins) - SQL

**SAS:**
```sas
DATA merged;
  MERGE table_a (IN=a) table_b (IN=b);
  BY key_var;
  IF a AND b;  /* Inner join */
RUN;
```

**Snowflake SQL:**
```sql
-- IF a AND b = INNER JOIN
CREATE OR REPLACE TABLE merged AS
SELECT a.*, b.col1, b.col2
FROM table_a a
INNER JOIN table_b b ON a.key_var = b.key_var;

-- IF a = LEFT JOIN
SELECT a.*, b.col1, b.col2
FROM table_a a
LEFT JOIN table_b b ON a.key_var = b.key_var;

-- IF a OR b = FULL OUTER JOIN
SELECT COALESCE(a.key_var, b.key_var) AS key_var, a.*, b.*
FROM table_a a
FULL OUTER JOIN table_b b ON a.key_var = b.key_var;
```

### MERGE with IN= Conditional (SQL with CASE)

**SAS:**
```sas
DATA result;
  MERGE master(IN=a) updates(IN=b);
  BY id;
  IF a AND NOT b THEN source = 'MASTER_ONLY';
  ELSE IF NOT a AND b THEN source = 'UPDATE_ONLY';
  ELSE source = 'BOTH';
RUN;
```

**Snowflake SQL:**
```sql
CREATE OR REPLACE TABLE result AS
SELECT 
  COALESCE(a.id, b.id) AS id,
  a.*,
  b.*,
  CASE 
    WHEN a.id IS NOT NULL AND b.id IS NULL THEN 'MASTER_ONLY'
    WHEN a.id IS NULL AND b.id IS NOT NULL THEN 'UPDATE_ONLY'
    ELSE 'BOTH'
  END AS source
FROM master a
FULL OUTER JOIN updates b ON a.id = b.id;
```

### Simple Arrays (Same Operation) - SQL

**SAS:**
```sas
DATA transformed;
  SET input;
  ARRAY nums[3] var1 var2 var3;
  DO i = 1 TO 3;
    IF nums[i] < 0 THEN nums[i] = 0;
  END;
RUN;
```

**Snowflake SQL:**
```sql
CREATE OR REPLACE TABLE transformed AS
SELECT 
  * EXCLUDE (var1, var2, var3),
  GREATEST(var1, 0) AS var1,
  GREATEST(var2, 0) AS var2,
  GREATEST(var3, 0) AS var3
FROM input;
```

### LAG/LEAD Comparisons - SQL

**SAS:**
```sas
DATA with_prev;
  SET data;
  prev_value = LAG(value);
  change = value - prev_value;
RUN;
```

**Snowflake SQL:**
```sql
CREATE OR REPLACE TABLE with_prev AS
SELECT *,
  LAG(value) OVER (ORDER BY sort_col) AS prev_value,
  value - LAG(value) OVER (ORDER BY sort_col) AS change
FROM data;
```

### OUTPUT to Multiple Datasets - SQL

**SAS:**
```sas
DATA high_value low_value;
  SET customers;
  IF total_spend > 1000 THEN OUTPUT high_value;
  ELSE OUTPUT low_value;
RUN;
```

**Snowflake SQL (separate statements):**
```sql
CREATE OR REPLACE TABLE high_value AS
SELECT * FROM customers WHERE total_spend > 1000;

CREATE OR REPLACE TABLE low_value AS
SELECT * FROM customers WHERE total_spend <= 1000;
```

---

## TIER 2: Stored Procedures (When SQL Window Functions Insufficient)

Use stored procedures ONLY when:
- Multiple complex calculations depend on each other row-by-row
- RETAIN resets conditionally based on complex logic (not just BY group)
- Multiple OUTPUT with overlapping conditions
- >5 branching conditions with state

### Complex RETAIN with Conditional Reset

**SAS:**
```sas
DATA flagged;
  SET transactions;
  BY customer_id;
  RETAIN prev_amount consecutive_count;
  IF FIRST.customer_id THEN DO;
    prev_amount = .;
    consecutive_count = 0;
  END;
  IF amount > prev_amount > . THEN consecutive_count + 1;
  ELSE consecutive_count = 0;
  flag = (consecutive_count >= 3);
  prev_amount = amount;
RUN;
```

**Snowflake Stored Procedure:**
```sql
CREATE OR REPLACE PROCEDURE sp_flag_consecutive()
RETURNS STRING
LANGUAGE SQL
AS
$$
BEGIN
  CREATE OR REPLACE TABLE flagged AS
  WITH lagged AS (
    SELECT *,
      LAG(amount) OVER (PARTITION BY customer_id ORDER BY trans_date) AS prev_amount,
      ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY trans_date) AS rn
    FROM transactions
  ),
  increasing_flag AS (
    SELECT *,
      CASE WHEN amount > prev_amount AND prev_amount IS NOT NULL THEN 1 ELSE 0 END AS is_increasing
    FROM lagged
  ),
  streak_groups AS (
    SELECT *,
      SUM(CASE WHEN is_increasing = 0 THEN 1 ELSE 0 END) 
        OVER (PARTITION BY customer_id ORDER BY trans_date) AS streak_id
    FROM increasing_flag
  ),
  streak_counts AS (
    SELECT *,
      SUM(is_increasing) OVER (
        PARTITION BY customer_id, streak_id 
        ORDER BY trans_date
      ) AS consecutive_count
    FROM streak_groups
  )
  SELECT 
    customer_id, trans_date, amount, prev_amount,
    consecutive_count,
    CASE WHEN consecutive_count >= 3 THEN TRUE ELSE FALSE END AS flag
  FROM streak_counts;
  
  RETURN 'Success';
END;
$$;
```

### Multiple OUTPUT with Complex Conditions

**SAS:**
```sas
DATA good bad review;
  SET applications;
  IF score >= 700 AND income > 50000 THEN OUTPUT good;
  ELSE IF score < 500 OR debt_ratio > 0.5 THEN OUTPUT bad;
  ELSE OUTPUT review;
RUN;
```

**Snowflake Stored Procedure:**
```sql
CREATE OR REPLACE PROCEDURE sp_categorize_applications()
RETURNS STRING
LANGUAGE SQL
AS
$$
DECLARE
  v_good INT; v_bad INT; v_review INT;
BEGIN
  CREATE OR REPLACE TABLE good AS
  SELECT * FROM applications WHERE score >= 700 AND income > 50000;
  
  CREATE OR REPLACE TABLE bad AS
  SELECT * FROM applications 
  WHERE NOT (score >= 700 AND income > 50000)
    AND (score < 500 OR debt_ratio > 0.5);
  
  CREATE OR REPLACE TABLE review AS
  SELECT * FROM applications
  WHERE NOT (score >= 700 AND income > 50000)
    AND NOT (score < 500 OR debt_ratio > 0.5);
  
  SELECT COUNT(*) INTO :v_good FROM good;
  SELECT COUNT(*) INTO :v_bad FROM bad;
  SELECT COUNT(*) INTO :v_review FROM review;
  
  RETURN 'Good: ' || v_good || ', Bad: ' || v_bad || ', Review: ' || v_review;
END;
$$;
```

---

## Date Handling

| SAS Function | Snowflake Equivalent |
|--------------|---------------------|
| `TODAY()` | `CURRENT_DATE()` |
| `DATETIME()` | `CURRENT_TIMESTAMP()` |
| `INTCK('DAY', a, b)` | `DATEDIFF('DAY', a, b)` |
| `INTNX('MONTH', date, 1)` | `DATEADD('MONTH', 1, date)` |
| `INTNX('MONTH', date, 1, 'B')` | `DATE_TRUNC('month', DATEADD('month', 1, date))` |
| `INTNX('MONTH', date, 1, 'E')` | `LAST_DAY(DATEADD('month', 1, date))` |
| `INTNX('MONTH', date, 0, 'B')` | `DATE_TRUNC('month', date)` |
| `INTNX('MONTH', date, 0, 'E')` | `LAST_DAY(date)` |
| `YEAR(date)` | `YEAR(date)` |
| `MONTH(date)` | `MONTH(date)` |
| `DAY(date)` | `DAY(date)` |
| `WEEKDAY(date)` | `DAYOFWEEK(date)` |
| `MDY(m, d, y)` | `DATE_FROM_PARTS(y, m, d)` |

**INTNX alignment parameter:**
- `'B'` (Beginning) → `DATE_TRUNC` on the interval
- `'M'` (Middle) → `DATEADD` then adjust to midpoint (flag MANUAL_REVIEW if complex)
- `'E'` (End) → `LAST_DAY` for month, or `DATEADD - 1 day` from next period start
- `'S'` (Same day, default) → plain `DATEADD`

**SAS date literal conversion:**
- SAS dates = days since Jan 1, 1960
- Convert: `DATEADD('DAY', sas_date_num, '1960-01-01')`

---

## SAS Sum Statement (CRITICAL)

The SAS sum statement `x + y;` (with `+` and `;`, no `=` sign) is NOT a simple assignment:
- It **adds y to x's retained value**
- It **treats missing values as 0** (unlike regular SAS arithmetic where missing propagates)

```sas
/* SAS sum statement - x accumulates, missing treated as 0 */
x + amount;  /* equivalent to: RETAIN x 0; x = SUM(x, amount); */
```

**Snowflake equivalent:**
```sql
-- In window function context:
SUM(COALESCE(amount, 0)) OVER (PARTITION BY group_col ORDER BY sort_col ROWS UNBOUNDED PRECEDING) AS x

-- In stored procedure context:
v_x := COALESCE(v_x, 0) + COALESCE(v_amount, 0);
```

---

## DELETE / RETURN / STOP Behavior

| SAS Statement | Meaning | Snowflake Equivalent |
|---------------|---------|---------------------|
| `DELETE;` | Remove current row from output | Add `WHERE NOT (condition)` to exclude |
| `RETURN;` | Skip remaining statements, go to next iteration | Restructure with CASE or separate CTEs |
| `STOP;` | Stop processing immediately | Not needed in set-based SQL; flag if logic depends on partial processing |
| `OUTPUT;` (explicit) | Write current row to output | Row passes the WHERE/CASE filter |
| No explicit OUTPUT | Implicit output at end of DATA step | Default SELECT behavior |

When multiple of these interact, use a stored procedure with explicit cursor logic.

---

## _N_ and _ERROR_ Automatic Variables

| SAS Variable | Meaning | Snowflake Equivalent |
|-------------|---------|---------------------|
| `_N_` | Current iteration number (1-based) | `ROW_NUMBER() OVER (ORDER BY 1)` or explicit ordering |
| `_ERROR_` | Error flag (0/1) | No direct equivalent; use TRY_* functions |
| `END=last_obs` | Flag set on last observation | `ROW_NUMBER() OVER (ORDER BY sort_col DESC) = 1` |

---

## MERGE with UPDATE Semantics

SAS UPDATE statement differs from MERGE:
```sas
DATA master;
  UPDATE master transactions;
  BY key_col;
RUN;
```

This **overwrites** master columns with non-missing transaction values. Snowflake equivalent:
```sql
MERGE INTO master m
USING transactions t ON m.key_col = t.key_col
WHEN MATCHED THEN UPDATE SET
  m.col1 = COALESCE(t.col1, m.col1),
  m.col2 = COALESCE(t.col2, m.col2);
```

### Many-to-Many MERGE Warning

SAS MERGE with many-to-many BY keys produces unexpected results (last value wins per group). Add MANUAL_REVIEW_REQUIRED when:
- Both datasets have duplicates on the BY key
- The SAS log would show "NOTE: MERGE statement has more than one data set with repeats of BY values"

---

## Missing Value Handling

| SAS | Snowflake |
|-----|-----------|
| `.` (numeric missing) | `NULL` |
| `' '` (character missing) | `NULL` or `''` |
| `IF var = .` | `WHERE var IS NULL` |
| `IF var NE .` | `WHERE var IS NOT NULL` |
| `COALESCE(a, b)` | `COALESCE(a, b)` |
| `MISSING(var)` | `var IS NULL` |

**Important:** SAS treats missing as less than any value. Snowflake NULLs sort last by default. Use `NULLS FIRST` if needed:

```sql
SELECT * FROM data ORDER BY col NULLS FIRST;
```
