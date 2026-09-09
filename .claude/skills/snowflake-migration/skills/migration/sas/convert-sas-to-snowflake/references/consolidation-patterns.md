# Consolidation Patterns for SAS to Snowflake Migration

## When to Load

Load when user selects **Optimize & Consolidate** migration mode.

---

## Dependency Analysis

### Building the Dependency Graph

For each script, extract:

```python
def extract_dependencies(sas_content):
    """Extract input/output tables from SAS code"""
    inputs = set()
    outputs = set()
    
    # DATA step outputs
    for match in re.findall(r'(?i)data\s+(\w+(?:\.\w+)?)\s*;', sas_content):
        outputs.add(match.lower())
    
    # DATA step inputs (SET, MERGE)
    for match in re.findall(r'(?i)(?:set|merge)\s+(\w+(?:\.\w+)?)', sas_content):
        inputs.add(match.lower())
    
    # PROC SQL CREATE TABLE
    for match in re.findall(r'(?i)create\s+table\s+(\w+(?:\.\w+)?)', sas_content):
        outputs.add(match.lower())
    
    # PROC SQL FROM
    for match in re.findall(r'(?i)from\s+(\w+(?:\.\w+)?)', sas_content):
        inputs.add(match.lower())
    
    return {'inputs': inputs, 'outputs': outputs}
```

### Dependency Matrix

| Script | Inputs | Outputs | Depends On |
|--------|--------|---------|------------|
| script_a.sas | source_data | staging_1 | - |
| script_b.sas | staging_1 | staging_2 | script_a |
| script_c.sas | staging_2 | final_output | script_b |

---

## Consolidation Patterns

### Pattern 1: Sequential Pipeline Merge

**Detection:**
- Script A output is Script B's only input
- Script B output is Script C's only input
- Linear chain of dependencies

**Before (3 scripts):**
```sas
/* script_a.sas */
DATA staging_1;
    SET source_data;
    new_col = col1 * 2;
RUN;

/* script_b.sas */
DATA staging_2;
    SET staging_1;
    WHERE new_col > 100;
RUN;

/* script_c.sas */
PROC SQL;
    CREATE TABLE final_output AS
    SELECT * FROM staging_2 WHERE status = 'ACTIVE';
QUIT;
```

**After (1 script with CTEs):**
```sql
-- consolidated_pipeline.sql
CREATE OR REPLACE TABLE final_output AS
WITH staging_1 AS (
    -- From script_a.sas
    SELECT *, col1 * 2 AS new_col
    FROM source_data
),
staging_2 AS (
    -- From script_b.sas
    SELECT * FROM staging_1
    WHERE new_col > 100
)
-- From script_c.sas
SELECT * FROM staging_2
WHERE status = 'ACTIVE';
```

**Savings:** 2 intermediate tables eliminated, 1 file instead of 3

---

### Pattern 2: Shared Source Consolidation

**Detection:**
- Multiple scripts read from same source table
- Apply different filters/transformations
- Create separate output tables

**Before (2 scripts):**
```sas
/* active_customers.sas */
DATA active_customers;
    SET customers;
    WHERE status = 'ACTIVE';
    segment = 'Active';
RUN;

/* vip_customers.sas */
DATA vip_customers;
    SET customers;
    WHERE total_spend > 10000;
    segment = 'VIP';
RUN;
```

**After (1 script):**
```sql
-- customer_segments.sql
CREATE OR REPLACE TABLE active_customers AS
SELECT *, 'Active' AS segment
FROM customers
WHERE status = 'ACTIVE';

CREATE OR REPLACE TABLE vip_customers AS
SELECT *, 'VIP' AS segment
FROM customers
WHERE total_spend > 10000;

-- OR if both needed in single table:
CREATE OR REPLACE TABLE customer_segments AS
SELECT *,
    CASE 
        WHEN status = 'ACTIVE' THEN 'Active'
        WHEN total_spend > 10000 THEN 'VIP'
    END AS segment
FROM customers
WHERE status = 'ACTIVE' OR total_spend > 10000;
```

---

### Pattern 3: Duplicate PROC SORT Elimination

**Detection:**
- Same `PROC SORT DATA=X BY Y` appears in multiple scripts
- Sorted result used for different purposes

**Before (3 scripts with same sort):**
```sas
/* report_1.sas */
PROC SORT DATA=transactions;
    BY customer_id date;
RUN;
/* ... use sorted data ... */

/* report_2.sas */
PROC SORT DATA=transactions;
    BY customer_id date;
RUN;
/* ... use sorted data ... */

/* report_3.sas */
PROC SORT DATA=transactions;
    BY customer_id date;
RUN;
/* ... use sorted data ... */
```

**After (1 sorted view, 3 scripts reference it):**
```sql
-- 00_common_views.sql (run first)
CREATE OR REPLACE VIEW transactions_sorted AS
SELECT * FROM transactions
ORDER BY customer_id, date;

-- report_1.sql
SELECT ... FROM transactions_sorted ...;

-- report_2.sql  
SELECT ... FROM transactions_sorted ...;

-- report_3.sql
SELECT ... FROM transactions_sorted ...;
```

**Savings:** Sort executed once instead of 3x

---

### Pattern 4: Intermediate Table to CTE

**Detection:**
- Table created in one block
- Used in immediately following block
- Never referenced elsewhere

**Before:**
```sas
DATA temp_calc;
    SET source;
    calculated_field = complex_formula;
RUN;

DATA final;
    SET temp_calc;
    WHERE calculated_field > threshold;
RUN;
```

**After:**
```sql
CREATE OR REPLACE TABLE final AS
WITH temp_calc AS (
    SELECT *, complex_formula AS calculated_field
    FROM source
)
SELECT * FROM temp_calc
WHERE calculated_field > threshold;
```

**Savings:** 1 intermediate table eliminated

---

### Pattern 5: Inline Single-Use Macros

**Detection:**
- `%MACRO name` defined
- `%name` called only once in codebase
- Macro is simple enough to inline

**Before:**
```sas
%MACRO calc_tax(rate);
    tax_amount = gross_amount * &rate;
%MEND;

DATA with_tax;
    SET orders;
    %calc_tax(0.08);
RUN;
```

**After:**
```sql
CREATE OR REPLACE TABLE with_tax AS
SELECT *, 
    gross_amount * 0.08 AS tax_amount
FROM orders;
```

---

### Pattern 6: Redundant Table Creation

**Detection:**
- Same table name created with identical logic in multiple scripts
- Usually indicates copy-paste pattern

**Before (table created in 3 places):**
```sas
/* script_1.sas */
DATA customer_base;
    SET customers;
    WHERE active_flag = 'Y';
RUN;

/* script_2.sas */
DATA customer_base;
    SET customers;
    WHERE active_flag = 'Y';
RUN;

/* script_3.sas */
DATA customer_base;
    SET customers;
    WHERE active_flag = 'Y';
RUN;
```

**After (single source of truth):**
```sql
-- 00_base_tables.sql (run once)
CREATE OR REPLACE TABLE customer_base AS
SELECT * FROM customers
WHERE active_flag = 'Y';

-- Other scripts reference customer_base directly
```

---

### Pattern 7: PROC MEANS/FREQ Consolidation

**Detection:**
- Multiple scripts run similar PROC MEANS/FREQ on same data
- Different variables but same source

**Before:**
```sas
/* stats_1.sas */
PROC MEANS DATA=sales;
    VAR revenue;
RUN;

/* stats_2.sas */
PROC MEANS DATA=sales;
    VAR quantity;
RUN;

/* stats_3.sas */
PROC FREQ DATA=sales;
    TABLES region;
RUN;
```

**After:**
```sql
-- sales_statistics.sql
-- Revenue stats
SELECT 
    COUNT(revenue) AS revenue_n,
    AVG(revenue) AS revenue_mean,
    STDDEV(revenue) AS revenue_std,
    MIN(revenue) AS revenue_min,
    MAX(revenue) AS revenue_max
FROM sales;

-- Quantity stats  
SELECT 
    COUNT(quantity) AS quantity_n,
    AVG(quantity) AS quantity_mean,
    STDDEV(quantity) AS quantity_std,
    MIN(quantity) AS quantity_min,
    MAX(quantity) AS quantity_max
FROM sales;

-- Region frequency
SELECT region, COUNT(*) AS count
FROM sales
GROUP BY region
ORDER BY region;
```

---

## Consolidation Report Template

```markdown
# SAS Migration Consolidation Report

## Summary
| Metric | Before | After | Savings |
|--------|--------|-------|---------|
| Scripts | X | Y | Z fewer |
| Tables Created | A | B | C fewer |
| PROC SORTs | D | E | F fewer |
| Lines of Code | G | H | I fewer |

## Consolidation Groups

### Group 1: [Name]
**Pattern:** Sequential Pipeline Merge
**Scripts Merged:** script_a.sas, script_b.sas, script_c.sas
**Output:** consolidated_pipeline.sql
**Tables Eliminated:** staging_1, staging_2

### Group 2: [Name]
**Pattern:** Duplicate PROC SORT Elimination
**Scripts Affected:** report_1.sas, report_2.sas, report_3.sas
**Output:** 00_common_views.sql + 3 report scripts
**Sorts Reduced:** 3 → 1

## Traceability Matrix
| Original File | Original Block | Target File | Target Location |
|---------------|----------------|-------------|-----------------|
| script_a.sas | DATA staging_1 | pipeline.sql | CTE staging_1 |
| script_b.sas | DATA staging_2 | pipeline.sql | CTE staging_2 |
| script_c.sas | PROC SQL | pipeline.sql | Final SELECT |

## Behavioral Notes
- [Any differences in execution behavior]
- [Order dependencies that must be preserved]
- [Data that may differ due to consolidation]
```

---

## Consolidation Decision Matrix

| Scenario | Consolidate? | Reason |
|----------|--------------|--------|
| A → B → C linear chain | ✅ Yes | Perfect CTE candidate |
| A → B, A → C (fan-out) | ⚠️ Partial | Keep A, may merge B+C if similar |
| A → C, B → C (fan-in) | ⚠️ Partial | May combine A+B if similar sources |
| Independent scripts | ❌ No | No benefit |
| Same sort in N scripts | ✅ Yes | Create shared view |
| Macro called once | ✅ Yes | Inline |
| Macro called N times | ❌ No | Keep as UDF |
| Temp table used once | ✅ Yes | Convert to CTE |
| Temp table used N times | ❌ No | Keep as table |

---

## Risk Considerations

### When NOT to Consolidate

1. **Audit Requirements** - Need 1:1 traceability for compliance
2. **Different Schedules** - Scripts run at different times
3. **Different Owners** - Managed by different teams
4. **Error Isolation** - Want failures to be isolated
5. **Performance Testing** - Need to measure individual components

### Consolidation Risks

| Risk | Mitigation |
|------|------------|
| Behavioral change | Compare output row counts and checksums |
| Missing data | Validate all source tables exist |
| Order dependency | Document execution order |
| Increased complexity | Balance consolidation vs readability |
